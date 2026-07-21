---
title: LocalSubSystemSBDP (Source)
---

← Back to [LocalSubSystemSBDP documentation](LocalSubSystemSBDP.md)

# LocalSubSystemSBDP - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\LocalSubSystemSBDP.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Sensitivity Based Distributed Programming (SBDP) local subsystem module.

This module provides the local subsystem implementation for the Sensitivity
Based Distributed Programming (SBDP) method (Algorithm 3).

Each outer iteration every subsystem solves, in parallel, the local NLP

    min   v_f(r) + sum_j ( grad_d^j L^(k) )^T ( d - d^(k) )
    s.t.  local inequality constraints  g(r) <= 0
          local equality constraints    h(r)  = 0
          coordination equality constraint (hard):
                [ H(r) - h ; S_z d - z ] = 0   | lambda

The linear sensitivity term uses the neighbor's coordination-equality Lagrange
multipliers (communicated via the middle level and stored as copies). After the
solve, the subsystem's own coordination-equality multipliers ``lambda`` are
recovered from the KKT system and published to the neighbors.
"""

from typing import List, Type
import numpy as np
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print, ddo_print_border
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.optimization import AnalysisInterface, OptimizationInterface
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalObjectiveInterface, LocalConstraintsInterface
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive
from Distributed_Design_Optimizer.subsystem.couplingparameters.sbdp import CouplingParametersSBDP
from Distributed_Design_Optimizer.middlelevel.sbdp import InConsistencySize
from Distributed_Design_Optimizer.coordination.convergence import (Local_ConvergenceIndicator_Innerloop_Interface,
                                                                   Local_ConvergenceIndicator_Innerloop_AlwaysConverged,
                                                                   Local_ConvergenceIndicator_Outerloop_Interface,
                                                                   Local_ConvergenceIndicator_Outerloop_DeWit
                                                                   )
from Distributed_Design_Optimizer.coordination.updatecouplingparametermethod import (UpdateCouplingParameterMethodInterface,
                                                                                     UpdateCouplingParameterMethod_OnlyInitialMultipliers
                                                                                     )


class LocalSubSystemSBDP(LocalSubSystemBasis):
    """Local subsystem implementation using Sensitivity Based Distributed Programming.

    Implements the SBDP method (Algorithm 3) for distributed optimization. The
    coordination coupling is imposed as a hard equality constraint, whose Lagrange
    multipliers are recovered from the local KKT system and communicated to the
    neighbors, where they enter the linear sensitivity term of the local objective.
    """

    def __init__(self,
                 id: str,
                 level: int,
                 neighborid: List[str],
                 analysis: AnalysisInterface,
                 localobjective: LocalObjectiveInterface,
                 localconstraints: LocalConstraintsInterface,
                 optimization: OptimizationInterface,
                 local_convergenceindicator_innerloop: Local_ConvergenceIndicator_Innerloop_Interface,
                 local_convergenceindicator_outerloop: Local_ConvergenceIndicator_Outerloop_Interface,
                 updatecouplingparametermethod_outerloop: UpdateCouplingParameterMethodInterface
                 ) -> None:
        """Create a new LocalSubSystemSBDP instance.

        Args:
            id: Identifier for the subsystem.
            level: Level identifier for the subsystem in the hierarchy.
            neighborid: List of identifiers for neighboring subsystems.
            analysis: Analysis interface for subsystem evaluation.
            localobjective: Local objective function class.
            localconstraints: Local constraint functions class.
            optimization: Optimization interface for solving local problems.
            local_convergenceindicator_innerloop: Local convergence indicator for inner loop.
            local_convergenceindicator_outerloop: Local convergence indicator for outer loop.
            updatecouplingparametermethod_outerloop: Method for updating coupling parameters in outer loop.
        """
        # Compatibility settings for the components handed to this subsystem by the
        # SBDP coordination method. These are validated here (rather than in SBDP)
        # because the corresponding objects are handed to this subsystem.

        # Allowed / recommended outerloop update coupling parameter methods for SBDP.
        # SBDP recovers the coordination multipliers from the KKT system, so no
        # dedicated multiplier/weight update is performed.
        self._allowedupdatemethods_outerloop: List[Type[UpdateCouplingParameterMethodInterface]] = [
            UpdateCouplingParameterMethod_OnlyInitialMultipliers
        ]
        self._recommendedupdatemethods_outerloop: List[Type[UpdateCouplingParameterMethodInterface]] = [
            UpdateCouplingParameterMethod_OnlyInitialMultipliers
        ]

        # Allowed / recommended local inner loop convergence indicators for SBDP.
        # SBDP performs exactly one inner pass per outer iteration.
        self._allowedconvergenceindicators_innerloop: List[Type[Local_ConvergenceIndicator_Innerloop_Interface]] = [
            Local_ConvergenceIndicator_Innerloop_AlwaysConverged
        ]
        self._recommendedconvergenceindicators_innerloop: List[Type[Local_ConvergenceIndicator_Innerloop_Interface]] = [
            Local_ConvergenceIndicator_Innerloop_AlwaysConverged
        ]

        # Allowed / recommended local outer loop convergence indicators for SBDP
        self._allowedconvergenceindicators_outerloop: List[Type[Local_ConvergenceIndicator_Outerloop_Interface]] = [
            Local_ConvergenceIndicator_Outerloop_DeWit
        ]
        self._recommendedconvergenceindicators_outerloop: List[Type[Local_ConvergenceIndicator_Outerloop_Interface]] = [
            Local_ConvergenceIndicator_Outerloop_DeWit
        ]

        self._couplingparameters: List[CouplingParametersSBDP] = [CouplingParametersSBDP(neighbor_id) for neighbor_id in neighborid]

        # super() initialization is not called at the top,
        # since evaluateAllJacobians needs optimdata, and initialization of optimdata needs couplingparameters
        super().__init__(id, level, neighborid, analysis, localobjective, localconstraints, optimization)

        # Convergence indicators - passed from SBDP
        self._local_convergenceindicator_innerloop: Local_ConvergenceIndicator_Innerloop_AlwaysConverged = local_convergenceindicator_innerloop
        self._local_convergenceindicator_outerloop: Local_ConvergenceIndicator_Outerloop_DeWit = local_convergenceindicator_outerloop

        self._inconsistencies: List[InConsistencySize] = [InConsistencySize(self.get_CouplingParameters()[i].get_ID())
                                                          for i in range(len(self.get_CouplingParameters()))]

        self._updatecouplingparametermethod_outerloop: UpdateCouplingParameterMethod_OnlyInitialMultipliers = updatecouplingparametermethod_outerloop

        # Design variables of the previous outer loop iteration, d^(k), used as the
        # fixed linearization point of the sensitivity term.
        #
        # We cache d^(k) in a dedicated subsystem attribute (captured once per outer
        # iteration in prepare_OptimizationProblem()) rather than calling
        # copy_DesignVariables_Previous_outerloop_itr() inside evaluateCoordinationObjective().
        # copy_DesignVariables_Previous_outerloop_itr() deep-copies the entire subsystem
        # history on every call; since the coordination objective is evaluated once per
        # black-box optimizer (e.g. PyNomad) iteration - potentially thousands of times per
        # inner solve - recomputing it there would be prohibitively expensive. d^(k) is
        # constant throughout an inner solve, so caching it once is both correct and cheap.
        self._designvariables_previous_outerloop_itr: List[float] | None = None

        # The per-neighbor sensitivity gradient contributions grad_d^j L^(k) of the
        # coordination objective are stored on their respective CouplingParametersSBDP
        # (see prepare_OptimizationProblem). They depend only on the neighbor coordination
        # multipliers communicated at the start of the outer iteration, are constant
        # throughout an inner solve, and are summed on demand in _assemble_sensitivity_gradient().

        # Validate the components handed to this subsystem
        self.validate_inputs()

    def validate_inputs(self) -> None:
        """Validate the components handed to this subsystem by the SBDP coordination method.

        Validates that the outer-loop update coupling parameter method and the local
        inner/outer loop convergence indicators are compatible with SBDP.

        Raises:
            ValueError: If a provided component is not compatible with SBDP.
        """
        # ===== updatecouplingparametermethod_outerloop Validation =====
        if type(self._updatecouplingparametermethod_outerloop) not in self._allowedupdatemethods_outerloop:
            raise ValueError(
                f"{DDO_Color}Outerloop update method '{type(self._updatecouplingparametermethod_outerloop).__name__}' is not compatible with SBDP. "
                f"Please choose one of the compatible methods: {[m.__name__ for m in self._allowedupdatemethods_outerloop]}{Reset}"
            )
        elif type(self._updatecouplingparametermethod_outerloop) not in self._recommendedupdatemethods_outerloop:
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: Outerloop update method '{type(self._updatecouplingparametermethod_outerloop).__name__}' is not recommended for SBDP.")
            ddo_print(f"{type(self).__name__}: Recommended methods: {[m.__name__ for m in self._recommendedupdatemethods_outerloop]}")
            ddo_print_border()

        # ===== Convergence Indicator Inner Validation =====
        if type(self._local_convergenceindicator_innerloop) not in self._allowedconvergenceindicators_innerloop:
            raise ValueError(
                f"{DDO_Color}Inner loop convergence indicator '{type(self._local_convergenceindicator_innerloop).__name__}' is not compatible with SBDP. "
                f"Please choose one of the compatible indicators: {[c.__name__ for c in self._allowedconvergenceindicators_innerloop]}{Reset}"
            )
        elif type(self._local_convergenceindicator_innerloop) not in self._recommendedconvergenceindicators_innerloop:
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: Inner loop convergence indicator '{type(self._local_convergenceindicator_innerloop).__name__}' is not recommended for SBDP.")
            ddo_print(f"{type(self).__name__}: Recommended indicators: {[c.__name__ for c in self._recommendedconvergenceindicators_innerloop]}")
            ddo_print_border()

        # ===== Convergence Indicator Outer Validation =====
        if type(self._local_convergenceindicator_outerloop) not in self._allowedconvergenceindicators_outerloop:
            raise ValueError(
                f"{DDO_Color}Outer loop convergence indicator '{type(self._local_convergenceindicator_outerloop).__name__}' is not compatible with SBDP. "
                f"Please choose one of the compatible indicators: {[c.__name__ for c in self._allowedconvergenceindicators_outerloop]}{Reset}"
            )
        elif type(self._local_convergenceindicator_outerloop) not in self._recommendedconvergenceindicators_outerloop:
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: Outer loop convergence indicator '{type(self._local_convergenceindicator_outerloop).__name__}' is not recommended for SBDP.")
            ddo_print(f"{type(self).__name__}: Recommended indicators: {[c.__name__ for c in self._recommendedconvergenceindicators_outerloop]}")
            ddo_print_border()

################################################################################################################
#   Basics of the subsystem
################################################################################################################
    def append_Controller(self) -> None:
        """Update local subsystems by appending controller.
        """

        # SBDP does not have a controller, hence, this function is empty
        pass

##############################################################################################################
#   Functions to evaluate a subsystem's responses and map them onto coupling parameters
##############################################################################################################
    def mapToController(self) -> None:
        """Pass, since no controller in SBDP.
        """

        pass

##############################################################################################################
#   Functions to evaluate a subsystem's optimization objective and constraints for given responses
##############################################################################################################

    def evaluateCoordinationObjective(self) -> None:
        """Evaluate the coordination objective (linear sensitivity term).

        Computes ``grad^T (d - d^(k))`` where ``grad`` is the sensitivity gradient
        and ``d^(k)`` is the design of the previous outer loop iteration.
        """
        designvariables: List[float] = self.get_DesignVariables()

        designvariables_previous: List[float] | None = self._designvariables_previous_outerloop_itr
        if designvariables_previous is None:
            # First outer iteration: no previous design available, use the current
            # design as the linearization point (the linear term then contributes 0).
            designvariables_previous = designvariables

        # Assemble the total sensitivity gradient sum_j grad_d^j L^(k) by summing the
        # per-neighbor contributions stored on each coupling parameter (see
        # prepare_OptimizationProblem).
        n_d: int = len(designvariables)
        grad: np.ndarray = np.zeros(n_d)
        couplingparameters: List[CouplingParametersSBDP] = self.get_CouplingParameters()
        for cp in couplingparameters:
            sensitivity_gradient: List[float] | None = cp.get_Sensitivity_Gradient()
            if sensitivity_gradient is not None:
                grad += np.array(sensitivity_gradient)

        coordinationobjective: float = float(np.dot(grad, np.array(designvariables) - np.array(designvariables_previous)))

        self.set_CoordinationObjectiveValue(coordinationobjective)

    def evaluate_Gradient_CoordinationObjective(self) -> None:
        """Evaluate the analytical gradient of the coordination objective.

        The gradient of the linear sensitivity term is the constant sensitivity
        gradient, independent of the design variables. It is stored exactly, so no
        finite-difference approximation is required.
        """
        # TODO
        pass

    def evaluateCoordinationEqualityConstraint(self) -> None:
        """Evaluate the coordination equality constraint.

        Builds, per neighbor, the vertical stack ``[ H(r) - h ; S_z d - z ]``.

        Each block is obtained from an InConsistencySize object (as in
        LocalSubSystemPC.evaluateCoordinationObjective). The mapped-response block
        ``H(r) - h`` is the negated ``copy_couplingvariable - mappedresponse``
        inconsistency, and the shared-design-variable block ``S_z d - z`` is the
        negated ``copy_targetshareddesignvariable - shareddesignvariable``
        inconsistency, so that the stored values equal ``H(r) - h`` and ``S_z d - z``
        respectively.

        NOTE: The per-neighbor block-presence conditionals used here must stay
        identical to those in evaluate_Jacobian_CoordinationEqualityConstraints() and
        the multiplier distribution in postprocess_Optimization(), so that the
        constraint value, its Jacobian and the multiplier decomposition remain
        consistently ordered.
        """
        couplingin: List[CouplingParametersSBDP] = self.get_CouplingParameters()
        inconsistency: List[InConsistencySize] = [InConsistencySize(couplingin[i].get_ID())
                                                  for i in range(len(couplingin))]
        constraint: List[float] = []

        for i in range(len(couplingin)):
            # mapped-response block: H(r) - h = mappedresponse - copy_couplingvariable
            if ((couplingin[i].get_MappedResponses() is not None) and
                    (couplingin[i].get_Copy_CouplingVariable() is not None)):
                copycoupl: List[float] = couplingin[i].get_Copy_CouplingVariable()
                mapres: List[float] = couplingin[i].get_MappedResponses()
                inconsistency[i].evaluate_MappedResponse_Minus_CopyCouplingVariable(copycouplingvariable=copycoupl, mappedresponse=mapres)
                for value in inconsistency[i].get_MappedResponse_Minus_CopyCouplingVariable():
                    constraint.append(value)

            # shared-design-variable block: S_z*d - z = shareddesignvariable - copy_targetshareddesignvariable
            if ((couplingin[i].get_SharedDesignVariables() is not None) and
                    (couplingin[i].get_Copy_TargetSharedDesignVariables() is not None)):
                copytgtshared: List[float] = couplingin[i].get_Copy_TargetSharedDesignVariables()
                shared: List[float] = couplingin[i].get_SharedDesignVariables()
                inconsistency[i].evaluate_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(copytargetshareddesignvariable=copytgtshared, shareddesignvariable=shared)
                for value in inconsistency[i].get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable():
                    constraint.append(value)

        constraint_value: List[float] | None = constraint if len(constraint) > 0 else None
        self.set_CoordinationEqualityConstraintValue(constraint_value)

    def evaluateCoordinationInequalityConstraint(self) -> None:
        """Evaluate the coordination inequality constraint.

        SBDP does not use coordination inequality constraints.
        """
        self.set_CoordinationInequalityConstraintValue(None)

    def evaluate_Jacobian_CoordinationEqualityConstraints(self) -> None:
        """Evaluate the Jacobian of the coordination equality constraints.

        The rows are ordered exactly as in evaluateCoordinationEqualityConstraint().
        The mapped-response block rows ``d(H(r) - h)/dd = dH/dd`` are returned with
        ``None`` entries so that they are filled by finite differences. The
        shared-design-variable block rows ``d(S_z d - z)/dd`` are the exact selection
        rows (a single 1.0 at the shared-design position).
        """
        # TODO
        pass

    def evaluate_Jacobian_CoordinationInEqualityConstraints(self) -> None:
        """Evaluate the Jacobian of the coordination inequality constraints.

        SBDP does not have coordination inequality constraints, hence no-op.
        """
        # No coordination inequality constraints in SBDP
        pass

##############################################################################################################
#   Functions to prepare, solve and postprocess a subsystem's optimization problem
##############################################################################################################

    def prepare_OptimizationProblem(self) -> None:
        """Prepare the optimization problem.

        Captures the design of the previous outer loop iteration, d^(k), used as the
        fixed linearization point of the sensitivity term, and computes the constant
        per-neighbor sensitivity gradients of the coordination objective once for the
        whole inner solve, storing each on its coupling parameter.

        Each neighbor's sensitivity gradient ``grad_d^j L^(k)`` is obtained by scattering
        the negated neighbor coordination-equality multipliers into the design-variable
        space using the coupling / shared-design index maps. They depend only on the
        neighbor multipliers communicated at the start of the outer iteration and are
        therefore constant throughout the inner solve, so computing them once here avoids
        recomputing them on every black-box optimizer (e.g. PyNomad) evaluation.
        """
        self._designvariables_previous_outerloop_itr = self.copy_DesignVariables_Previous_outerloop_itr()

        n_d: int = len(self.get_DesignVariables())

        couplingparameters: List[CouplingParametersSBDP] = self.get_CouplingParameters()        
        for cp in couplingparameters:
            grad: np.ndarray = np.zeros(n_d)

            # Mapped-response block: scatter -lambda_h into the coupling-variable positions
            copy_lambda_h: List[float] | None = cp.get_Copy_Multipliers_MappedResponse_Minus_CopyCouplingVariable()
            indices_cv: List[int] | None = cp.get_Indices_CouplingVariables_In_DesignVariables()
            if copy_lambda_h is not None and indices_cv is not None:
                for p in range(len(indices_cv)):
                    grad[indices_cv[p]] += -copy_lambda_h[p]

            # Shared-design-variable block: scatter -lambda_z into the shared-design positions
            copy_lambda_z: List[float] | None = cp.get_Copy_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable()
            indices_sdv: List[int] | None = cp.get_Indices_SharedDesignVariables_In_DesignVariables()
            if copy_lambda_z is not None and indices_sdv is not None:
                for p in range(len(indices_sdv)):
                    grad[indices_sdv[p]] += -copy_lambda_z[p]

            cp.set_Sensitivity_Gradient(grad.tolist())

    def postprocess_Optimization(self) -> None:
        """Postprocess the optimization.

        Recovers the coordination-equality Lagrange multipliers from the local KKT
        system and distributes them into the coupling parameters, so that they are
        subsequently published to the neighbors via the middle level.
        """
        # Evaluate the coordination equality constraint value at the solution
        # (runs the analysis and maps to coupling parameters).
        self.evaluateTotalConstraint()

        # Compute gradients and Jacobians. The coordination-equality Jacobian's
        # mapped-response block is filled here via finite differences.
        self.evaluateAllJacobians()
        self.updateSubsystemfromOptimdata(self.get_OptimData())

        # Recover the KKT multipliers if the solver did not provide them.
        if self.check_MultipliersNotSet():
            self.compute_KKT_multipliers()
        self.updateSubsystemfromOptimdata(self.get_OptimData())

        # Distribute the coordination-equality multipliers into the coupling parameters.
        # The stacked KKT multiplier vector is split following exactly the same neighbor
        # ordering and block-presence conditionals used to assemble the coordination
        # equality constraint. The mapped-response block multipliers lambda_h and the
        # shared-design-variable block multipliers lambda_z are stored as the subsystem's
        # own multipliers on each coupling parameter.
        multipliers: List[float] | None = self.get_OptimData().get_Multipliers_Coordination_Equality_Constraints()

        if multipliers is not None:
            couplingin: List[CouplingParametersSBDP] = self.get_CouplingParameters()
            pointer: int = 0

            for i in range(len(couplingin)):
                neighborid: str = couplingin[i].get_ID()

                # mapped-response block multipliers lambda_h
                if ((couplingin[i].get_MappedResponses() is not None) and
                        (couplingin[i].get_Copy_CouplingVariable() is not None)):
                    number_h: int = len(couplingin[i].get_MappedResponses())
                    lambda_h: List[float] = list(multipliers[pointer:pointer + number_h])
                    pointer += number_h
                    self.set_Multipliers_MappedResponse_Minus_CopyCouplingVariable(neighborid, lambda_h)

                # shared-design-variable block multipliers lambda_z
                if ((couplingin[i].get_SharedDesignVariables() is not None) and
                        (couplingin[i].get_Copy_TargetSharedDesignVariables() is not None)):
                    number_z: int = len(couplingin[i].get_SharedDesignVariables())
                    lambda_z: List[float] = list(multipliers[pointer:pointer + number_z])
                    pointer += number_z
                    self.set_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(neighborid, lambda_z)

###############################################################################################################
#   Functions to handle coupling parameters related to modelling a distributed optimization problem.
###############################################################################################################

    def return_initialized_CouplingParameters(self) -> List[CouplingParametersSBDP]:
        """Return initialized coupling parameters.

        Returns:
            List of initialized CouplingParametersSBDP, one per neighbor.
        """
        initialized_couplingparameters: List[CouplingParametersSBDP] = [CouplingParametersSBDP(self.get_CouplingParameters()[i].get_ID())
                                                                        for i in range(len(self.get_CouplingParameters()))]
        return initialized_couplingparameters

########################################################################################################
#   Functions to handle coupling parameters
#######################################################################################################

    def initializeCouplingParameters_before_CopyToMiddleLevel(self) -> None:
        """Initialize coupling parameters before copying from neighboring subsystem.
        """
        pass

    def initializeCouplingParameters_after_CopyFromMiddleLevel(self) -> None:
        """Initialize coupling parameters after copying from neighboring subsystems.

        Seeds the subsystem's own coordination-equality multipliers, sized to match
        the corresponding coordination-equality blocks, so that they are communicated
        to the neighbors from the first iteration onwards.
        """
        coupling: List[CouplingParametersSBDP] = self.get_CouplingParameters()

        for i in range(len(coupling)):
            neighborid: str = coupling[i].get_ID()

            # Mapped-response block multipliers, sized to the mapped responses.
            if ((coupling[i].get_MappedResponses() is not None) and
                    (coupling[i].get_Copy_CouplingVariable() is not None)):
                initmultipliers_h: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialMultiplier()] * len(coupling[i].get_MappedResponses())
                self.set_Multipliers_MappedResponse_Minus_CopyCouplingVariable(neighborid, initmultipliers_h)

            # Shared-design-variable block multipliers, sized to the shared design variables.
            if ((coupling[i].get_SharedDesignVariables() is not None) and
                    (coupling[i].get_Copy_TargetSharedDesignVariables() is not None)):
                initmultipliers_z: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialMultiplier()] * len(coupling[i].get_SharedDesignVariables())
                self.set_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(neighborid, initmultipliers_z)

    def initializeCouplingParameters_after_Second_CopyFromMiddleLevel(self) -> None:
        """Initialize coupling parameters after two communication rounds between subsystems.
        """
        # SBDP does not need such a second communication round, hence skip
        pass

    def prepare_updateCouplingParameters(self) -> None:
        """Prepare coupling parameters before update operations.
        """
        pass

    def updateCouplingParameters_innerLoop(self) -> None:
        """Update coupling parameters in the inner loop.
        """
        pass

    def updateCouplingParameters_outerLoop(self) -> None:
        """Update coupling parameters during outer loop iteration.

        In SBDP the coordination multipliers are recomputed from the KKT system in
        each subsystem solve (see postprocess_Optimization) rather than by a dual
        ascent update, hence no outer-loop multiplier update is performed here.
        """
        pass

    def evaluate_Inconsistencies(self) -> None:
        """Compute the difference between stored coupling and mapped variables.

        Delegates to the base class implementation which computes inconsistency
        vectors for the mapped-response side, coupling-variable side, shared design
        variables, and target shared design variables of each coupling circle.
        """
        super().evaluate_Inconsistencies()

    def return_initialized_Inconsistencies(self) -> List[InConsistencySize]:
        """Return initialized inconsistencies.

        Returns:
            List of initialized InConsistencySize, one per coupling parameter.
        """
        initialized_inconsistencies: List[InConsistencySize] = [InConsistencySize(self.get_CouplingParameters()[i].get_ID())
                                                                for i in range(len(self.get_CouplingParameters()))]
        return initialized_inconsistencies

    def set_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self, neighborid: str, multipliersin: List[float]) -> None:
        """Set the mapped-response coordination multipliers of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            multipliersin: List of multiplier values to set.
        """
        # No copy.copy() wrapper needed - setter creates its own defensive copy
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                couplingparameter.set_Multipliers_MappedResponse_Minus_CopyCouplingVariable(multipliersin)
                break

    def set_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, neighborid: str, multipliersin: List[float]) -> None:
        """Set the shared-design-variable coordination multipliers of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            multipliersin: List of multiplier values to set.
        """
        # No copy.copy() wrapper needed - setter creates its own defensive copy
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                couplingparameter.set_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(multipliersin)
                break

########################################################################################################
#   Update State Function necessary for running multiprocessing
########################################################################################################
    def update_state(self, other_subsystem: 'LocalSubSystemSBDP') -> None:
        """Update the state of this LocalSubSystemSBDP instance with values from another instance.

        This method is necessary for multiprocessing. When subsystems are executed in parallel
        using multiprocessing.Pool, they are serialized and deserialized, creating new objects
        in separate memory spaces. After parallel execution completes, this method updates
        the original object's attribute values while preserving their memory addresses.

        Args:
            other_subsystem: The source LocalSubSystemSBDP containing updated values
                from parallel execution.
        """
        # Update attributes inherited from LocalSubSystemBasis (and transitively SubSystemBasis)
        super().update_state(other_subsystem)

        # Update LocalSubSystemSBDP-specific attributes (in __init__ order)

        # _designvariables_previous_outerloop_itr: List[float] | None
        # Cached linearization point d^(k) of the sensitivity term.
        self._designvariables_previous_outerloop_itr: List[float] | None = update_state_listprimitive(
            self._designvariables_previous_outerloop_itr, other_subsystem._designvariables_previous_outerloop_itr)

```
