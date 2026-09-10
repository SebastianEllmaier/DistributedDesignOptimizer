---
title: LocalSubSystemBasis (Source)
---

← Back to [LocalSubSystemBasis documentation](LocalSubSystemBasis.md)

# LocalSubSystemBasis - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\LocalSubSystemBasis.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Local subsystem basis module.

This module provides the abstract base class for local subsystems in
distributed optimization.
"""

import copy
from abc import abstractmethod
from typing import List, Dict, Set, Tuple
import numpy as np
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print
from Distributed_Design_Optimizer.subsystem.optimization import AnalysisInterface, OptimizationInterface
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalObjectiveInterface, LocalConstraintsInterface
from Distributed_Design_Optimizer.subsystem.optimization.optimizerdata import OptimDataBasis, LocalSubSystemOptimData
from Distributed_Design_Optimizer.subsystem.couplingparameters import CouplingParametersInterface, SubSysCouplingParametersBasis
from Distributed_Design_Optimizer.subsystem import SubSystemBasis
from Distributed_Design_Optimizer.subsystem.historyentry import LocalSubSystemHistoryEntry
from Distributed_Design_Optimizer.subsystem.tools import FiniteDifferencesJacobian
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive, ScalerBasis, ScalerZeroOne, ScalerConstraint
from Distributed_Design_Optimizer.subsystem.optimization.solver import Solver_QP
from Distributed_Design_Optimizer.middlelevel import InConsistencySizeInterface
from Distributed_Design_Optimizer.postprocess import JacobianComputer


class LocalSubSystemBasis(SubSystemBasis):
    """A LocalSubSystemBasis object contains all necessary data for an individual subsystem.

    This includes methods to analyse its responses, to optimize the subsystem and to couple it
    to neighboring subsystems.
    """

    _DDO_PRINT_LABEL_WIDTH: int = 32

    def __init__(self,
                 id: str,
                 level: int,
                 neighborid: List[str],
                 analysis: AnalysisInterface,
                 localobjective: LocalObjectiveInterface,
                 localconstraints: LocalConstraintsInterface,
                 optimization: OptimizationInterface
                 ) -> None:
        """Create a new instance of LocalSubSystemBasis with neighbors.

        Args:
            id: Identifier for the subsystem.
            level: Level identifier for the subsystem.
            neighborid: Identifiers for the neighbors.
            analysis: Type of analysis class.
            localobjective: Type of local objective function class.
            localconstraints: Type of local constraint functions class.
            optimization: Type of optimization class.
        """

        # Call init of super
        super().__init__(id=id, neighborid=neighborid)

        self._SubsystemLevel: int = level

        if isinstance(optimization, Solver_QP):
            raise NotImplementedError(f"{DDO_Color}Currently not for local subsystems, since no P-q-A interface for QPs are enforced there; ",
                                      f"Currently tailored to black-box-optimizers.{Reset}")

        self._optimization: OptimizationInterface = optimization

        self._optimdata: LocalSubSystemOptimData = self.initialize_Initial_Optimdata_at_Beginning()
        self._couplingparameters: List[SubSysCouplingParametersBasis]  # to be initialized in child-class of LocalSubSystemBasis

        self._inconsistencies: List[InConsistencySizeInterface]  # to be initialized in child-class of SubSystemBasis

        self._maxinconsistencyvalue: float | None = None
        self._maxinconsistencycoupledsubsystemID: str | None = None

        self._analysis: AnalysisInterface = analysis
        self._jacobiancomputer: JacobianComputer = JacobianComputer()

        # This object is needed to compute Jacobians of quantities we do not know
        self._finite_differences_jacobian: FiniteDifferencesJacobian = FiniteDifferencesJacobian()

        self._localobjective: LocalObjectiveInterface = localobjective
        self._localconstraints: LocalConstraintsInterface = localconstraints

        self._referencedesignvariables: List[float] | List[None] | None = None  # scaled01 values
        self._referencedesignvariables_unscaled: List[float] | List[None] | None = None  # unscaled values
        self._referencelocalobjectivevalue: float | None = None  # scaled01 value
        self._referencelocalobjectivevalueunscaled: float | None = None

        self._responses_unscaled: List[float] | None = None  # unscaled values
        self._jacobian_mappedresponse_wrt_designvariables_value: List[List[List[float]] | None] | None = None  # scaled01 value
        self._localobjectivevalue: float | None = None  # scaled01 value
        self._localobjectivevalue_unscaled: float | None = None  # unscaled value

        self._equalitylocalconstraintsvalue: List[float] | None = None  # scaled01 value
        self._equalitylocalconstraintsvalue_unscaled: List[float] | None = None  # unscaled value
        self._inequalitylocalconstraintsvalue: List[float] | None = None  # scaled01 value
        self._inequalitylocalconstraintsvalue_unscaled: List[float] | None = None  # unscaled value

        self._ignore_couplingid_for_coordinationobjective: str | None = None

        # Warning flags for out-of-range values (one-time warnings)
        self._localobjectivevalue_lower_scaler_bound_warning_raised: bool = False
        self._localobjectivevalue_upper_scaler_bound_warning_raised: bool = False
        self._equalitylocalconstraintsvalue_lower_scaler_bound_warning_raised: bool = False
        self._equalitylocalconstraintsvalue_upper_scaler_bound_warning_raised: bool = False
        self._inequalitylocalconstraintsvalue_lower_scaler_bound_warning_raised: bool = False
        self._inequalitylocalconstraintsvalue_upper_scaler_bound_warning_raised: bool = False
        self._referencedesignvariables_lower_scaler_bound_warning_raised: bool = False
        self._referencedesignvariables_upper_scaler_bound_warning_raised: bool = False

        self._scalers: List[ScalerBasis] | None = None

    def initialize_Initial_Optimdata_at_Beginning(self) -> LocalSubSystemOptimData:
        """Return a LocalSubSystemOptimData object based on the subsystem's current state.

        Returns:
            A LocalSubSystemOptimData with all fields set to None.
        """

        return LocalSubSystemOptimData(optimizer_type="",
                                       designvariables=None,
                                       designvariables_unscaled=None,
                                       lowerbounds=None,
                                       lowerbounds_scaled=None,
                                       upperbounds=None,
                                       upperbounds_scaled=None,
                                       Responses_unscaled=None,
                                       localobjectivevalue=None,
                                       localobjectivevalue_unscaled=None,
                                       totalobjectivevalue=None,
                                       coordinationobjectivevalue=None,
                                       equalitylocalconstraintsvalue=None,
                                       equalitylocalconstraintsvalue_unscaled=None,
                                       inequalitylocalconstraintsvalue=None,
                                       inequalitylocalconstraintsvalue_unscaled=None,
                                       totalconstrainteqvalue=None,
                                       totalconstraintineqvalue=None,
                                       coordinationequalityconstraintvalue=None,
                                       coordinationinequalityconstraintvalue=None,
                                       couplingparameters=copy.deepcopy(self.get_CouplingParameters()),
                                       gradient_localobjective=None,
                                       gradient_coordinationobjective=None,
                                       gradient_totalobjective=None,
                                       jacobian_localequalityconstraints=None,
                                       jacobian_coordinationequalityconstraints=None,
                                       jacobian_totalequalityconstraints=None,
                                       jacobian_localinequalityconstraints=None,
                                       jacobian_coordinationinequalityconstraints=None,
                                       jacobian_totalinequalityconstraints=None,
                                       jacobian_lowerbounds=None,
                                       jacobian_upperbounds=None,
                                       multipliers_lowerbounds=None,  # placeholders if solver computes multipliers
                                       multipliers_upperbounds=None,  # placeholders if solver computes multipliers
                                       multipliers_local_inequality_constraints=None,  # placeholders if solver computes multipliers
                                       multipliers_local_equality_constraints=None,  # placeholders if solver computes multipliers
                                       multipliers_coordination_equality_constraints=None,  # placeholders if solver computes multipliers
                                       multipliers_coordination_inequality_constraints=None,  # placeholders if solver computes multipliers
                                       activelocalinequalityconstraints=None,
                                       activecoordinationinequalityconstraints=None,
                                       activelowerbounds=None,
                                       activeupperbounds=None,
                                       exitflag=None,
                                       message=None,
                                       optimization_numberofdesignvariableevaluations=None,
                                       optimization_runtime=None,
                                       numberofactiveinequalityconstraints=None,
                                       numberofactivebounds=None
                                       )

    def initialize_Optimdata(self) -> LocalSubSystemOptimData:
        """Return a LocalSubSystemOptimData object based on the subsystem's current state.

        Returns:
            A LocalSubSystemOptimData initialized from the current subsystem state.
        """

        return LocalSubSystemOptimData(optimizer_type="User-Provided Initial Values",
                                       designvariables=self.get_DesignVariables(),
                                       designvariables_unscaled=self.get_DesignVariables_Unscaled(),
                                       lowerbounds=None,
                                       lowerbounds_scaled=None,
                                       upperbounds=None,
                                       upperbounds_scaled=None,
                                       Responses_unscaled=self.get_Responses_Unscaled(),
                                       localobjectivevalue=self.get_LocalObjectiveValue(),
                                       localobjectivevalue_unscaled=self.get_LocalObjectiveValue_Unscaled(),
                                       totalobjectivevalue=self.get_TotalObjectiveValue(),
                                       coordinationobjectivevalue=self.get_CoordinationObjectiveValue(),
                                       equalitylocalconstraintsvalue=self.get_EqualityLocalConstraintsValue(),
                                       equalitylocalconstraintsvalue_unscaled=self.get_EqualityLocalConstraintsValue_Unscaled(),
                                       inequalitylocalconstraintsvalue=self.get_InequalityLocalConstraintsValue(),
                                       inequalitylocalconstraintsvalue_unscaled=self.get_InequalityLocalConstraintsValue_Unscaled(),
                                       totalconstrainteqvalue=self.get_TotalConstraintEqValue(),
                                       totalconstraintineqvalue=self.get_TotalConstraintIneqValue(),
                                       coordinationequalityconstraintvalue=self.get_CoordinationEqualityConstraintValue(),
                                       coordinationinequalityconstraintvalue=self.get_CoordinationInequalityConstraintValue(),
                                       couplingparameters=copy.deepcopy(self.get_CouplingParameters()),
                                       gradient_localobjective=None,
                                       gradient_coordinationobjective=None,
                                       gradient_totalobjective=None,
                                       jacobian_localequalityconstraints=None,
                                       jacobian_coordinationequalityconstraints=None,
                                       jacobian_totalequalityconstraints=None,
                                       jacobian_localinequalityconstraints=None,
                                       jacobian_coordinationinequalityconstraints=None,
                                       jacobian_totalinequalityconstraints=None,
                                       jacobian_lowerbounds=None,
                                       jacobian_upperbounds=None,
                                       multipliers_lowerbounds=None,  # placeholders if solver computes multipliers
                                       multipliers_upperbounds=None,  # placeholders if solver computes multipliers
                                       multipliers_local_inequality_constraints=None,  # placeholders if solver computes multipliers
                                       multipliers_local_equality_constraints=None,  # placeholders if solver computes multipliers
                                       multipliers_coordination_equality_constraints=None,  # placeholders if solver computes multipliers
                                       multipliers_coordination_inequality_constraints=None,  # placeholders if solver computes multipliers
                                       activelocalinequalityconstraints=np.isclose(np.array(self.get_InequalityLocalConstraintsValue()), 0.0, atol=1e-8).tolist(),
                                       activecoordinationinequalityconstraints=np.isclose(np.array(self.get_CoordinationInequalityConstraintValue()), 0.0, atol=1e-8).tolist() if self.get_CoordinationInequalityConstraintValue() is not None else None,
                                       activelowerbounds=np.isclose(np.array(self.get_DesignVariables_Unscaled()), np.array(self.get_LowerBounds_Unscaled()), atol=1e-8).tolist(),
                                       activeupperbounds=np.isclose(np.array(self.get_DesignVariables_Unscaled()), np.array(self.get_UpperBounds_Unscaled()), atol=1e-8).tolist(),
                                       exitflag=-1,
                                       message="",
                                       optimization_numberofdesignvariableevaluations=-1,
                                       optimization_runtime=0.0,
                                       numberofactiveinequalityconstraints=int(np.sum(np.isclose(np.array(self.get_InequalityLocalConstraintsValue()), 0.0, atol=1e-8))),
                                       numberofactivebounds=int(np.sum(np.isclose(np.array(self.get_DesignVariables_Unscaled()),
                                                                                  np.array(self.get_LowerBounds_Unscaled()),
                                                                                  atol=1e-8)) + \
                                                                np.sum(np.isclose(np.array(self.get_DesignVariables_Unscaled()),
                                                                                  np.array(self.get_UpperBounds_Unscaled()),
                                                                                  atol=1e-8)))
                                       )

########################################################################################################################
#   Getters
########################################################################################################################

    def get_Finite_Differences_Jacobian(self) -> FiniteDifferencesJacobian:
        """Get the finite differences Jacobian approximation object.

        Returns:
            The finite differences Jacobian approximation object.
        """
        # No copy.copy() used - FiniteDifferencesJacobian is a class object returned by reference intentionally.
        # This allows the caller to interact with the actual object. If isolation is needed,
        # the caller should explicitly copy.
        return self._finite_differences_jacobian

    def set_Scalers(self, scalers: List[ScalerBasis]) -> None:
        """Set the size of scaling for the design variables.

        Args:
            scalers: List of scalers for the design variables.
        """
        # No copy.copy() used - List[ScalerBasis | None] is a list of class objects
        # assigned by reference intentionally. This allows the caller to continue interacting with
        # the actual objects. If isolation is needed, the caller should explicitly copy.
        self._scalers = scalers

    def get_Scalers(self) -> List[ScalerBasis]:
        """Get the scalers for design variables and constraints.

        Returns:
            List of scalers for variables and constraints.
        """
        # No copy.copy() used - List[ScalerBasis] is a list of class objects
        # returned by reference intentionally. This allows the caller to interact with
        # the actual objects. If isolation is needed, the caller should explicitly copy.
        return self._scalers

########################################################################################################################
#   Functions to handle inconsistencies
########################################################################################################################

    def get_Inconsistencies(self) -> List[InConsistencySizeInterface]:
        """Get the inconsistencies.

        Returns:
            List of inconsistency objects for all neighbors.
        """
        # No copy.copy() used - List[InConsistencySizeInterface] is a list of class objects
        # returned by reference intentionally. This allows the caller to interact with
        # the actual objects. If isolation is needed, the caller should explicitly copy.
        return self._inconsistencies

    def evaluate_MaxInconsistency(self) -> None:
        """Evaluate the maximum inconsistency across the subsystems and the ID of it."""
        max_inconsistency = 0.0
        max_inconsistency_id = None
        for inconsistency in self._inconsistencies:
            if inconsistency.get_maxInconsistencyValue() is not None:
                if inconsistency.get_maxInconsistencyValue() > max_inconsistency:
                    max_inconsistency = inconsistency.get_maxInconsistencyValue()
                    max_inconsistency_id = inconsistency.get_ID()

        self._maxinconsistencyvalue = max_inconsistency
        self._maxinconsistencycoupledsubsystemID = max_inconsistency_id

    def get_maxInconsistencyValue(self) -> float | None:
        """Get the maximum inconsistency value across the subsystems.

        Returns:
            The maximum inconsistency value across all neighbors, or None if not yet computed.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._maxinconsistencyvalue

    def get_MaxInconsistencyCoupledSubsystemID(self) -> str | None:
        """Get the coupled subsystem ID with the maximum inconsistency value.

        Returns:
            The neighbor subsystem ID with the largest inconsistency, or None if not yet computed.
        """
        # No copy.copy() needed - str is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._maxinconsistencycoupledsubsystemID

    @abstractmethod
    def return_initialized_Inconsistencies(self) -> List[InConsistencySizeInterface]:
        """Return initialized inconsistencies.

        Returns:
            List of initialized InConsistencySizeInterface objects.
        """

########################################################################################################################
#   Basics of the subsystem
########################################################################################################################

    def get_SubsystemLevel(self) -> int:
        """Get the level of the subsystem.

        Returns:
            The level of the subsystem.
        """
        # No copy.copy() needed - int is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._SubsystemLevel

    @abstractmethod
    def append_Controller(self) -> None:
        """Update local subsystems by appending controller.
        """

        # If controller exists:
        # Add "C" to neighbors_id
        # In initializeCouplingParameters_before/after_CopyFromMiddleLevel:
        # Update inconsistencies, couplingparameters: Needs to be implemented in both
        # LocalSubSystemXXX and ControllerSubSystemXXX subclasses for specific
        # distributed optimization algorithms

        # If controller does not exist, leave it empty

    def updateSubsystemfromOptimdata(self, optimdata: OptimDataBasis) -> None:
        """Update subsystem state from optimization data.

        Updates design variables, objective values, constraint values, and runs
        analysis based on the provided optimization data.

        Args:
            optimdata: Optimization data containing updated values.
        """
        # update design variables
        # self.truncateVariables(subsystemin)  # this applies tau damping to the subsystems designvariables

        # Check if the subsystem and optimdata type are compatible
        if not isinstance(optimdata, LocalSubSystemOptimData):

            raise TypeError(f"{DDO_Color}The optimdata object should be of type LocalSubSystemOptimData.{Reset}")

        # Call the general update subsystem from optimdata
        super().updateSubsystemfromOptimdata(optimdata)

        # update the local objective function value
        if optimdata.get_LocalObjectiveValue() is not None:
            self.set_LocalObjectiveValue(optimdata.get_LocalObjectiveValue())

        # update the local equality constraint function value
        if optimdata.get_EqualityLocalConstraintsValue() is not None:
            self.set_EqualityLocalConstraintsValue(optimdata.get_EqualityLocalConstraintsValue())

        # update the local inequality constraint function value
        if optimdata.get_InequalityLocalConstraintsValue() is not None:
            self.set_InequalityLocalConstraintsValue(optimdata.get_InequalityLocalConstraintsValue())

        # Get the coupling parameters
        couplingparameters: List[CouplingParametersInterface] = self.get_CouplingParameters()

        # Update Jacobians of mapped responses in the couplingparameters
        for couplingparameter in couplingparameters:

            # Check if couplingparameter corresponds
            # to a local <-> local coupling
            if isinstance(couplingparameter, SubSysCouplingParametersBasis):

                # Get ID
                id: str = couplingparameter.get_ID()

                # Get the Jacobian of the mapped responses
                # No copy wrapper needed - getter returns copy.deepcopy() and setter creates its own copy.deepcopy()
                jacobian_mappedresponse: List[List[float | None]] | None = optimdata.get_Jacobian_MappedResponse(id)

                # Check if the mapped responses exist
                if jacobian_mappedresponse is not None:

                    # Update the Jacobian of the mapped responses
                    couplingparameter.set_Jacobian_MappedResponse(jacobian_mappedresponse)

        # update the responses information
        self.runAnalysis()

        # update the coupling information to neighbors
        self.mapToCouplingParameters()

    def updateOptimdatafromSubsystem(self) -> None:
        """Update the optimdata object with the information from the state of the subsystem.

        This should only be called if an optimdata object
        was created and should be modified afterwards
        (e.g. in initialization, where the optimdata object
        has None fields).
        """

        # Call the update Optimdata from the SubSystemBasis class
        super().updateOptimdatafromSubsystem()
        
        # Update active bounds
        # Lower and upper bounds always exist, hence, no check
        lowerbounds: List[float] | None = self.get_LowerBounds_Unscaled()
        if self._optimdata.get_LowerBounds() is None and lowerbounds is not None:
            self._optimdata.set_LowerBounds(lowerbounds)
        if self._optimdata.get_LowerBounds_Scaled() is None and lowerbounds is not None:
            lowerbounds_scaled: List[float] = [self.get_Scalers()[i].transform(lowerbounds[i]) for i in range(len(lowerbounds))]
            self._optimdata.set_LowerBounds_Scaled(lowerbounds_scaled)

        upperbounds: List[float] | None = self.get_UpperBounds_Unscaled()
        if self._optimdata.get_UpperBounds() is None and upperbounds is not None:
            self._optimdata.set_UpperBounds(upperbounds)
        if self._optimdata.get_UpperBounds_Scaled() is None and upperbounds is not None:
            upperbounds_scaled: List[float] = [self.get_Scalers()[i].transform(upperbounds[i]) for i in range(len(upperbounds))]
            self._optimdata.set_UpperBounds_Scaled(upperbounds_scaled)

        if self.get_DesignVariables() is not None:

            designvariables: List[float] = self.get_DesignVariables_Unscaled()

            # Active bounds

            activelowerbounds: List[bool] = np.isclose(np.array(designvariables), np.array(lowerbounds), atol=1e-8).tolist()
            self._optimdata.set_ActiveLowerBounds(activelowerbounds)

            activeupperbounds: List[bool] = np.isclose(np.array(designvariables), np.array(upperbounds), atol=1e-8).tolist()
            self._optimdata.set_ActiveUpperBounds(activeupperbounds)

            # Number of active bounds

            numberofactivebounds: int = int(np.sum(np.isclose(np.array(designvariables), np.array(lowerbounds), atol=1e-8)) +
                                            np.sum(np.isclose(np.array(designvariables), np.array(upperbounds), atol=1e-8)))
            self._optimdata.set_NumberofActiveBounds(numberofactivebounds)

        # Physical responses
        if self.get_Responses_Unscaled() is not None:
            self._optimdata.set_Responses_Unscaled(self.get_Responses_Unscaled())

        # Local objective
        if self.get_LocalObjectiveValue() is not None:
            self._optimdata.set_LocalObjectiveValue(self.get_LocalObjectiveValue())

        # Local objective unscaled
        if self.get_LocalObjectiveValue_Unscaled() is not None:
            self._optimdata.set_LocalObjectiveValue_Unscaled(self.get_LocalObjectiveValue_Unscaled())

        # Local equality constraints
        if self.get_EqualityLocalConstraintsValue() is not None:
            self._optimdata.set_EqualityLocalConstraintsValue(self.get_EqualityLocalConstraintsValue())

        # Local equality constraints unscaled
        if self.get_EqualityLocalConstraintsValue_Unscaled() is not None:
            self._optimdata.set_EqualityLocalConstraintsValue_Unscaled(self.get_EqualityLocalConstraintsValue_Unscaled())

        # Local inequality constraints
        if self.get_InequalityLocalConstraintsValue() is not None:
            self._optimdata.set_InequalityLocalConstraintsValue(self.get_InequalityLocalConstraintsValue())

            # Determine the active local constraints
            activelocalinequalityconstraints = np.isclose(np.array(self.get_InequalityLocalConstraintsValue()), 0.0, atol=1e-8).tolist()
            self._optimdata.set_ActiveLocalInequalityConstraints(activelocalinequalityconstraints)

        # Local inequality constraints unscaled
        if self.get_InequalityLocalConstraintsValue_Unscaled() is not None:
            self._optimdata.set_InequalityLocalConstraintsValue_Unscaled(self.get_InequalityLocalConstraintsValue_Unscaled())

########################################################################################################################
#   Functions to obtain past values from self._subsystemhistory
########################################################################################################################

    def copy_LocalObjectiveUnscaled_Past_outerloop_itr(self, outerloop_itr_before: int) -> float | None:
        """Copy unscaled local objective from past outer loop iteration.

        Args:
            outerloop_itr_before: The number of outer loop iterations to go back by.

        Returns:
            The unscaled local objective value from the past iteration, or None if not found.
        """
        previous_itr = self._outerloop_itr - outerloop_itr_before
        found_result = False
        # Search the self._subsystemhistory backwards
        for i in range(len(self._subsystemhistory) - 1, -1, -1):
            if self._subsystemhistory[i].get_OuterLoop_Itr() == previous_itr:
                # copy.deepcopy() intentional - protects self._subsystemhistory from modification by callers.
                # The history is a shared record; callers must not alter past iteration data.
                result_optimdata: LocalSubSystemOptimData | None = copy.deepcopy(self._subsystemhistory[i].get_OptimData())
                if result_optimdata is not None:
                    result: float | None = result_optimdata.get_LocalObjectiveValue_Unscaled()
                else:
                    result = None
                found_result = True
                break

        if not found_result:
            # There exists no LocalSubSystemOptimData._localobjectivevalue with fitting self._outerloop_itr or self._innerloop_itr, so just return a None
            result = None

        return result

    def copy_LocalObjectiveUnscaled_Previous_outerloop_itr(self) -> float | None:
        """Copy the unscaled local objective from the previous outer loop iteration.

        Returns:
            The unscaled local objective value from the previous iteration, or None if not found.
        """
        return self.copy_LocalObjectiveUnscaled_Past_outerloop_itr(outerloop_itr_before=1)

    def copy_LocalObjective_Past_outerloop_itr(self, outerloop_itr_before: int) -> float | None:
        """Copy local objective from past outer loop iteration.

        Args:
            outerloop_itr_before: The number of outer loop iterations to go back by.

        Returns:
            The scaled local objective value from the past iteration, or None if not found.
        """
        previous_itr = self._outerloop_itr - outerloop_itr_before
        found_result = False
        # Search the self._subsystemhistory backwards
        for i in range(len(self._subsystemhistory) - 1, -1, -1):
            if self._subsystemhistory[i].get_OuterLoop_Itr() == previous_itr:
                # copy.deepcopy() intentional - protects self._subsystemhistory from modification by callers.
                # The history is a shared record; callers must not alter past iteration data.
                result_optimdata: LocalSubSystemOptimData | None = copy.deepcopy(self._subsystemhistory[i].get_OptimData())
                if result_optimdata is not None:
                    result: float | None = result_optimdata.get_LocalObjectiveValue()
                else:
                    result = None
                found_result = True
                break

        if not found_result:
            # There exists no LocalSubSystemOptimData._localobjectivevalue with fitting self._outerloop_itr or self._innerloop_itr, so just return a None
            result = None

        return result

    def copy_LocalObjective_Previous_outerloop_itr(self) -> float | None:
        """Copy the scaled local objective from the previous outer loop iteration.

        Returns:
            The scaled local objective value from the previous iteration, or None if not found.
        """
        return self.copy_LocalObjective_Past_outerloop_itr(outerloop_itr_before=1)

    def copy_LocalObjective_Previous_innerloop_itr(self) -> float | None:
        """Copy the scaled local objective from the previous inner loop iteration.

        Returns:
            The scaled local objective value from the previous inner iteration, or None if not found.
        """
        previous_inner_itr = self._innerloop_itr - 1
        found_result = False

        # Search the self._subsystemhistory backwards
        for i in range(len(self._subsystemhistory) - 1, -1, -1):
            history_entry = self._subsystemhistory[i]
            # Match same outer loop but previous inner loop
            if (history_entry.get_OuterLoop_Itr() == self._outerloop_itr and
                    history_entry.get_InnerLoop_Itr() == previous_inner_itr):
                # copy.deepcopy() intentional - protects self._subsystemhistory from modification by callers.
                # The history is a shared record; callers must not alter past iteration data.
                result_optimdata: LocalSubSystemOptimData | None = copy.deepcopy(self._subsystemhistory[i].get_OptimData())
                if result_optimdata is not None:
                    result: float | None = result_optimdata.get_LocalObjectiveValue()
                else:
                    result = None
                found_result = True
                break

        if found_result is False:
            result = None

        return result

    def copy_LocalObjectiveUnscaled_Previous_innerloop_itr(self) -> float | None:
        """Copy the unscaled local objective from the previous inner loop iteration.

        Returns:
            The unscaled local objective value from the previous inner iteration, or None if not found.
        """
        previous_inner_itr = self._innerloop_itr - 1
        found_result = False

        # Search the self._subsystemhistory backwards
        for i in range(len(self._subsystemhistory) - 1, -1, -1):
            history_entry = self._subsystemhistory[i]
            # Match same outer loop but previous inner loop
            if (history_entry.get_OuterLoop_Itr() == self._outerloop_itr and
                    history_entry.get_InnerLoop_Itr() == previous_inner_itr):
                # copy.deepcopy() intentional - protects self._subsystemhistory from modification by callers.
                # The history is a shared record; callers must not alter past iteration data.
                result_optimdata: LocalSubSystemOptimData | None = copy.deepcopy(self._subsystemhistory[i].get_OptimData())
                if result_optimdata is not None:
                    result: float | None = result_optimdata.get_LocalObjectiveValue_Unscaled()
                else:
                    result = None
                found_result = True
                break

        if found_result is False:
            result = None

        return result

########################################################################################################################
#   Functions to evaluate a subsystem's responses and map them onto coupling parameters
########################################################################################################################

    def set_DesignVariables(self, designvariables: List[float]) -> None:
        """Set the scaled design variables.

        Args:
            designvariables: Scaled design variable values in [0, 1].
        """
        dv_array = np.array(designvariables)
        # Check lower bound
        if not np.all((dv_array >= 0.0) | np.isclose(dv_array, 0.0, atol=1e-8, rtol=0)):
            if not self._designvariables_lower_scaler_bound_warning_raised:
                self._designvariables_lower_scaler_bound_warning_raised = True
                ddo_print("WARNING: All design variables must be within the range [0.0, 1.0] (with tolerance 1e-8)")
        # Check upper bound
        if not np.all((dv_array <= 1.0) | np.isclose(dv_array, 1.0, atol=1e-8, rtol=0)):
            if not self._designvariables_upper_scaler_bound_warning_raised:
                self._designvariables_upper_scaler_bound_warning_raised = True
                ddo_print("WARNING: All design variables must be within the range [0.0, 1.0] (with tolerance 1e-8)")
        if len(designvariables) != len(self._designvariables_granularity):
            raise ValueError(f"{DDO_Color}Length of Design Variables doesn't match with Length of DesignVariables Granularity{Reset}")
        # Check whether the to-be-set designvariables fit with the specified granularity
        if self._designvariables_granularity is not None:
            for i in range(len(designvariables)):
                if self._designvariables_granularity[i] == 0.0:
                    # 0.0 means continuous - no granularity check needed
                    pass
                elif self._designvariables_granularity[i] > 0.0:
                    # Check if design variable is a multiple of the granularity using modulo
                    remainder = np.mod(designvariables[i], self._designvariables_granularity[i])
                    if np.isclose(remainder, 0.0) or np.isclose(remainder, self._designvariables_granularity[i]):
                        pass
                    else:
                        raise ValueError(f"{DDO_Color}Design variable at index {i} with value {designvariables[i]} does not match the required granularity of {self._designvariables_granularity[i]}{Reset}")
                else:
                    raise ValueError(f"{DDO_Color}Invalid granularity value at index {i}: {self._designvariables_granularity[i]}. Must be >= 0.0{Reset}")
        else:
            raise ValueError(f"{DDO_Color}DesignVariable Granularity must be defined before setting any design variables{Reset}")
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._designvariables = copy.copy(designvariables)  # scaled01 values

        # No additional copy.copy() needed as list comprehension already creates new list object
        designvariables_unscaled = [self.get_Scalers()[i].inverse_transform(designvariables[i]) for i in range(len(designvariables))]
        
        # Store the unscaled design variables
        self._designvariables_unscaled = designvariables_unscaled

    def runAnalysis(self) -> None:
        """Execute the analysis code associated with this subsystem."""
        self._analysis.evaluateLocalResponses(self)

    def set_Responses_Unscaled(self, Responsesin: List[float]) -> None:
        """Store the physical responses (unscaled values).

        Args:
            Responsesin: Physical response values (unscaled).
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._responses_unscaled = copy.copy(Responsesin)

    def get_Responses_Unscaled(self) -> List[float]:
        """Return the physical responses of a subsystem (unscaled values).

        Returns:
            Physical response values (unscaled).
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._responses_unscaled)

    def mapToCouplingParameters(self) -> None:
        """Map the physical responses onto the neighboring domains."""

        self._analysis.mapLocalResponsesDesignVariables_to_CouplingParameters(self)

        # If controller is in neighbor list (i.e. controller exists), map specifically to controller
        if "C" in self._neighborid:
            self.mapToController()

########################################################################################################################
#   Functions to evaluate a subsystem's optimization objective and constraints for given responses
########################################################################################################################

    def evaluateTotalObjective(self) -> None:
        """Evaluate the total objective function (local + coordination)."""
        # execute analysis
        self.runAnalysis()

        # execute mapping
        self.mapToCouplingParameters()

        # compute the local objective function
        self.evaluateLocalObjective()

        # compute any additional objective term due to the coordination method handling of inconsistencies
        self.evaluateCoordinationObjective()

        localobjective: float | None = self.get_LocalObjectiveValue()
        objective_incons: float | None = self.get_CoordinationObjectiveValue()

        f = None

        if localobjective is not None and objective_incons is not None:
            f = localobjective + objective_incons
        elif localobjective is None and objective_incons is None:
            f = None
        elif localobjective is None and objective_incons is not None:
            f = objective_incons
        elif localobjective is not None and objective_incons is None:
            f = localobjective

        # Store the combined total objective. When neither a local nor a
        # coordination objective exists, f is None and the total objective is
        # None accordingly (consistent with the None paradigm).
        self.set_TotalObjectiveValue(f)

    def evaluateLocalObjective(self) -> None:
        """Evaluate the local objective function."""
        self._localobjective.evaluateLocalObjective(self)

    def evaluate_Responses_and_LocalObjective(self) -> None:
        """Run the analysis, update the coupling parameters, and compute the local objective."""

        # execute analysis
        self.runAnalysis()

        # execute mapping
        self.mapToCouplingParameters()

        # compute the local objective function
        self.evaluateLocalObjective()

        # Set the total objective to the local objective function,
        # since the coordination objective does not exist yet
        self.set_TotalObjectiveValue(self.get_LocalObjectiveValue())

    def set_LocalObjectiveValue(self, localobjectivevaluein: float | None) -> None:
        """Set the scaled local objective value.

        Args:
            localobjectivevaluein: The scaled local objective value (in range [0.0, 1.0]).
        """

        # Only if the local objective of a subsystem exists
        if localobjectivevaluein is not None:

            # Check lower bound
            if localobjectivevaluein < 0.0:
                if not self._localobjectivevalue_lower_scaler_bound_warning_raised:
                    self._localobjectivevalue_lower_scaler_bound_warning_raised = True
                    ddo_print("WARNING: localobjectivalue must be within the range [0.0, 1.0]")
            # Check upper bound
            if localobjectivevaluein > 1.0:
                if not self._localobjectivevalue_upper_scaler_bound_warning_raised:
                    self._localobjectivevalue_upper_scaler_bound_warning_raised = True
                    ddo_print("WARNING: localobjectivalue must be within the range [0.0, 1.0]")
            # No copy.copy needed for float (immutable type)
            self._localobjectivevalue = localobjectivevaluein
            scl: ScalerZeroOne = self.get_Scalers()[len(self._designvariables)]  # the scaler for local objective function is right after the ones for the design variables
            # No copy.copy needed: inverse_transform returns a float (immutable type)
            self._localobjectivevalue_unscaled = scl.inverse_transform(localobjectivevaluein)

        # Else, if there is not local objective
        else:

            self._localobjectivevalue = None
            self._localobjectivevalue_unscaled = None

    def get_LocalObjectiveValue(self) -> float | None:
        """Get the scaled local objective value.

        Returns:
            The scaled local objective value.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._localobjectivevalue

    def get_LocalObjectiveValue_Unscaled(self) -> float | None:
        """Get the unscaled local objective value.

        Returns:
            The unscaled local objective value.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._localobjectivevalue_unscaled

    def evaluateTotalConstraint(self) -> None:
        """Evaluate the total constraints (local + coordination)."""
        # execute analysis
        self.runAnalysis()

        # execute mapping
        self.mapToCouplingParameters()

        # compute the local constraint functions
        self.evaluateLocalConstraints()

        # compute any additional constraints due to the coordination method handling of inconsistencies
        self.evaluateCoordinationEqualityConstraint()
        self.evaluateCoordinationInequalityConstraint()

        localequalitycon: List[float] | None = self.get_EqualityLocalConstraintsValue()
        localinequalitcon: List[float] | None = self.get_InequalityLocalConstraintsValue()
        equality_coordinationcons: List[float] | None = self.get_CoordinationEqualityConstraintValue()
        inequality_coordinationcons: List[float] | None = self.get_CoordinationInequalityConstraintValue()

        # outputs
        c = []
        if localinequalitcon is not None:
            c += localinequalitcon
        if inequality_coordinationcons is not None:
            c += inequality_coordinationcons  # concatenation of two List[float]

        # If no inequality constraints exist, set to None
        if len(c) == 0:
            c = None

        ceq = []
        if localequalitycon is not None:
            ceq += localequalitycon
        if equality_coordinationcons is not None:
            ceq += equality_coordinationcons  # concatenation of two List[float]

        # If no equality constraints exist, set to None
        if len(ceq) == 0:
            ceq = None

        # set the equality, inequality constraint values to the subsystem
        self.set_TotalConstraintEqValue(ceq)
        self.set_TotalConstraintIneqValue(c)

    def evaluateTotalObjectiveAndTotalConstraint(self) -> None:
        """Evaluate both total objective and total constraint in a single call.

        This method combines evaluateTotalObjective() and evaluateTotalConstraint()
        to avoid redundant analysis and mapping operations when both values
        are needed (e.g., during optimization blackbox evaluations).
        """
        # execute analysis ONCE
        self.runAnalysis()

        # execute mapping ONCE
        self.mapToCouplingParameters()

        # compute the local objective function
        self.evaluateLocalObjective()

        # compute any additional objective term due to the coordination method handling of inconsistencies
        self.evaluateCoordinationObjective()

        localobjective: float | None = self.get_LocalObjectiveValue()
        objective_incons: float | None = self.get_CoordinationObjectiveValue()

        f = None

        if localobjective is not None and objective_incons is not None:
            f = localobjective + objective_incons
        elif localobjective is None and objective_incons is None:
            f = None
        elif localobjective is None and objective_incons is not None:
            f = objective_incons
        elif localobjective is not None and objective_incons is None:
            f = localobjective

        # Store the combined total objective. When neither a local nor a
        # coordination objective exists, f is None and the total objective is
        # None accordingly (consistent with the None paradigm).
        self.set_TotalObjectiveValue(f)

        # compute the local constraint functions
        self.evaluateLocalConstraints()

        # compute any additional constraints due to the coordination method handling of inconsistencies
        self.evaluateCoordinationEqualityConstraint()
        self.evaluateCoordinationInequalityConstraint()

        localequalitycon: List[float] | None = self.get_EqualityLocalConstraintsValue()
        localinequalitcon: List[float] | None = self.get_InequalityLocalConstraintsValue()
        equality_coordinationcons: List[float] | None = self.get_CoordinationEqualityConstraintValue()
        inequality_coordinationcons: List[float] | None = self.get_CoordinationInequalityConstraintValue()

        # outputs
        c = []
        if localinequalitcon is not None:
            c += localinequalitcon
        if inequality_coordinationcons is not None:
            c += inequality_coordinationcons  # concatenation of two List[float]

        # If no inequality constraints exist, set to None
        if len(c) == 0:
            c = None

        ceq = []
        if localequalitycon is not None:
            ceq += localequalitycon
        if equality_coordinationcons is not None:
            ceq += equality_coordinationcons

        # If no equality constraints exist, set to None
        if len(ceq) == 0:
            ceq = None

        # set the equality, inequality constraint values to the subsystem
        self.set_TotalConstraintEqValue(ceq)
        self.set_TotalConstraintIneqValue(c)

    def evaluateLocalConstraints(self) -> None:
        """Evaluate the local equality and inequality constraints."""
        self._localconstraints.evaluateEqualityLocalConstraints(self)  # it needs to be exectued first
        self._localconstraints.evaluateInEqualityLocalConstraints(self)

    def set_EqualityLocalConstraintsValue(self, equalitylocalconstraintsin: List[float] | None) -> None:  # when running Matlab Optimizer, we do not have access to EqualityLocalConstraintsValue
        """Set the equality local constraints value (scaled01 value).

        Args:
            equalitylocalconstraintsin: Equality constraint values (scaled to [-0.5, 0.5]).
        """

        # Only if local equality constraints exist
        if equalitylocalconstraintsin is not None:

            # Check lower bound
            if not all(value >= -0.5 for value in equalitylocalconstraintsin):
                if not self._equalitylocalconstraintsvalue_lower_scaler_bound_warning_raised:
                    self._equalitylocalconstraintsvalue_lower_scaler_bound_warning_raised = True
                    ddo_print("WARNING: All equalitylocalconstraintsin must be within the range [-0.5, 0.5]")
            # Check upper bound
            if not all(value <= 0.5 for value in equalitylocalconstraintsin):
                if not self._equalitylocalconstraintsvalue_upper_scaler_bound_warning_raised:
                    self._equalitylocalconstraintsvalue_upper_scaler_bound_warning_raised = True
                    ddo_print("WARNING: All equalitylocalconstraintsin must be within the range [-0.5, 0.5]")
            # copy.copy() used - List[float] is mutable. This prevents modifications
            # in the caller from being reflected back to the class attribute.
            self._equalitylocalconstraintsvalue = copy.copy(equalitylocalconstraintsin)
            scl: List[ScalerConstraint] = self.get_Scalers()[len(self._designvariables)+1 : len(self._designvariables)+1+len(equalitylocalconstraintsin)]  # the scalers for local constraints are right after the ones for the design variables and local objective function
            self._equalitylocalconstraintsvalue_unscaled = copy.copy([scl[i].inverse_transform(equalitylocalconstraintsin[i]) for i in range(len(equalitylocalconstraintsin))])

        # Else, if there is no local equality constraint
        else:

            self._equalitylocalconstraintsvalue = None
            self._equalitylocalconstraintsvalue_unscaled = None

    def get_EqualityLocalConstraintsValue(self) -> List[float] | None:  # when running Matlab Optimizer, we do not have access to EqualityLocalConstraintsValue
        """Get the equality local constraints value (scaled01 value).

        Returns:
            Equality constraint values (scaled to [-0.5, 0.5]).
        """
        # copy.copy() needed: List is mutable, so changes by caller are not reflected back unless setter is called explicitly
        return copy.copy(self._equalitylocalconstraintsvalue)

    def get_EqualityLocalConstraintsValue_Unscaled(self) -> List[float] | None:  # when running Matlab Optimizer, we do not have access to EqualityLocalConstraintsValue
        """Get the equality local constraints value (unscaled value).

        Returns:
            Equality constraint values (unscaled).
        """
        # copy.copy() needed: List is mutable, so changes by caller are not reflected back unless setter is called explicitly
        return copy.copy(self._equalitylocalconstraintsvalue_unscaled)

    def set_InequalityLocalConstraintsValue(self, inequalitylocalconstraintsvaluein: List[float] | None) -> None:  # when running Matlab Optimizer, we do not have access to InEqualityLocalConstraintsValue
        """Set the inequality local constraints value (scaled01 value).

        Args:
            inequalitylocalconstraintsvaluein: Inequality constraint values (scaled to [-0.5, 0.5]).
        """

        # Only if local inequality constraints exist
        if inequalitylocalconstraintsvaluein is not None:

            # Check lower bound
            if not all(value >= -0.5 for value in inequalitylocalconstraintsvaluein):
                if not self._inequalitylocalconstraintsvalue_lower_scaler_bound_warning_raised:
                    self._inequalitylocalconstraintsvalue_lower_scaler_bound_warning_raised = True
                    ddo_print("WARNING: All inequalitylocalconstraintsvaluein must be within the range [-0.5, 0.5]")
            # Check upper bound
            if not all(value <= 0.5 for value in inequalitylocalconstraintsvaluein):
                if not self._inequalitylocalconstraintsvalue_upper_scaler_bound_warning_raised:
                    self._inequalitylocalconstraintsvalue_upper_scaler_bound_warning_raised = True
                    ddo_print("WARNING: All inequalitylocalconstraintsvaluein must be within the range [-0.5, 0.5]")
            # copy.copy() used - List[float] is mutable. This prevents modifications
            # in the caller from being reflected back to the class attribute.
            self._inequalitylocalconstraintsvalue = copy.copy(inequalitylocalconstraintsvaluein)

            # Since the inequality constraints need to be scaled with the correct scaling variable
            # Need to infer the correct length of the scaling variables of the local equality constraints
            # since the local equality constraints are None if no local equality constraints exist
            # Else use the length of the local inequality constraints
            # This is based on the decomposition of the scaling variables (see InputeFile.py)

            length_localequalityconstraints: int = 1
            if self.get_EqualityLocalConstraintsValue() is not None:
                length_localequalityconstraints = len(self.get_EqualityLocalConstraintsValue())

            scl: List[ScalerConstraint] = self.get_Scalers()[len(self._designvariables)+1+length_localequalityconstraints: len(self._designvariables)+1+length_localequalityconstraints+len(inequalitylocalconstraintsvaluein)]  # the scalers for local constraints are right after the ones for the design variables and local objective function and equality local constraints
            # No copy.copy needed: list comprehension over primitive types (float) already creates a new list
            self._inequalitylocalconstraintsvalue_unscaled = [scl[i].inverse_transform(inequalitylocalconstraintsvaluein[i]) for i in range(len(inequalitylocalconstraintsvaluein))]

        # Else, there are no local inequality constraints
        else:

            self._inequalitylocalconstraintsvalue = None
            self._inequalitylocalconstraintsvalue_unscaled = None

    def get_InequalityLocalConstraintsValue(self) -> List[float] | None:  # when running Matlab Optimizer, we do not have access to InEqualityLocalConstraintsValue
        """Get the inequality local constraints value (scaled01 value).

        Returns:
            Inequality constraint values (scaled to [-0.5, 0.5]).
        """
        # copy.copy() needed: List is mutable, so changes by caller are not reflected back unless setter is called explicitly
        return copy.copy(self._inequalitylocalconstraintsvalue)

    def get_InequalityLocalConstraintsValue_Unscaled(self) -> List[float] | None:  # when running Matlab Optimizer, we do not have access to InEqualityLocalConstraintsValue
        """Get the inequality local constraints value (unscaled value).

        Returns:
            Inequality constraint values (unscaled).
        """
        # copy.copy() needed: List is mutable, so changes by caller are not reflected back unless setter is called explicitly
        return copy.copy(self._inequalitylocalconstraintsvalue_unscaled)

########################################################################################################################
#   Functions to evaluate a subsystem's optimization objective's and constraints' gradients / Jacobians / Hessians for given responses
########################################################################################################################

    def evaluate_PerturbationDirectionsIndices_LocalObjectiveGradient(self,
                                                                      gradient_localobjective: List[float | None] | None,
                                                                      totalnumber_perturbationdirections: int) -> List[int]:
        """Return the perturbation direction indices for the local objective gradient.

        Args:
            gradient_localobjective: The local objective gradient with None entries
                where approximation is needed.
            totalnumber_perturbationdirections: Total number of perturbation
                directions.

        Returns:
            List of indices where gradient approximation is needed.
        """
        # Initialize empty List
        indices_gradient_localobjective: List[int] = []

        # Check if the user provided gradient approximations
        if gradient_localobjective is not None:

            # Infer the None-indices for the gradient
            indices_gradient_localobjective = [i for i, x in enumerate(gradient_localobjective) if x is None]

        else:

            # Return all indices, since user provided no gradient information
            indices_gradient_localobjective = list(range(totalnumber_perturbationdirections))

        # Return the inferred List of indices to be perturbed for a gradient approximation
        # No copy.copy() needed - this list is freshly created within this method, not a stored class attribute.
        return indices_gradient_localobjective

    def evaluate_PerturbationDirectionsIndices_CoordinationObjectiveGradient(self,
                                                                             gradient_coordinationobjective: List[float | None] | None,
                                                                             totalnumber_perturbationdirections: int) -> List[int]:
        """Return the perturbation direction indices for the coordination objective gradient.

        Args:
            gradient_coordinationobjective: The coordination objective gradient with None entries
                where approximation is needed.
            totalnumber_perturbationdirections: Total number of perturbation
                directions.

        Returns:
            List of indices where gradient approximation is needed.
        """
        # Initialize empty List
        indices_gradient_coordinationobjective: List[int] = []

        # Check if the user provided gradient approximations
        if gradient_coordinationobjective is not None:

            # Infer the None-indices for the gradient
            indices_gradient_coordinationobjective = [i for i, x in enumerate(gradient_coordinationobjective) if x is None]

        else:

            # Return all indices, since user provided no gradient information
            indices_gradient_coordinationobjective = list(range(totalnumber_perturbationdirections))

        # Return the inferred List of indices to be perturbed for a gradient approximation
        # No copy.copy() needed - this list is freshly created within this method, not a stored class attribute.
        return indices_gradient_coordinationobjective

    def evaluate_PerturbationDirectionsIndices_LocalEqualityConstraintsJacobian(self,
                                                                                jacobian_localequalityconstraints: List[List[float | None]] | None,
                                                                                totalnumber_perturbationdirections: int) -> List[int]:
        """Return the perturbation direction indices for the local equality constraints Jacobian.

        Args:
            jacobian_localequalityconstraints: The local equality constraints Jacobian
                with None entries where approximation is needed.
            totalnumber_perturbationdirections: Total number of perturbation directions.

        Returns:
            List of indices where Jacobian approximation is needed.
        """
        # Initialize empty List
        indices_jacobian_localequalityconstraints: List[int] = []

        # Check if the user provided Jacobian approximation
        if jacobian_localequalityconstraints is not None:

            # Infer the None-indices for the Jacobian
            # of the local equality constraints
            indices_jacobian_localequalityconstraints = [j for j in range(totalnumber_perturbationdirections)
                                                         if any(jacobian_localequalityconstraints[i][j] is None for i in range(len(jacobian_localequalityconstraints)))]

        else:

            # Return all indices, since user provided no Jacobian approximation
            indices_jacobian_localequalityconstraints = list(range(totalnumber_perturbationdirections))

        # Return the inferred list of indices to be perturbed for a Jacobian approximation
        # No copy.copy() needed - this list is freshly created within this method, not a stored class attribute.
        return indices_jacobian_localequalityconstraints

    def evaluate_PerturbationDirectionsIndices_CoordinationEqualityConstraintsJacobian(self,
                                                                                       jacobian_coordinationequalityconstraints: List[List[float | None]] | None,
                                                                                       totalnumber_perturbationdirections: int) -> List[int]:
        """Return the perturbation direction indices for the coordination equality constraints Jacobian.

        Args:
            jacobian_coordinationequalityconstraints: The coordination equality constraints
                Jacobian with None entries where approximation is needed.
            totalnumber_perturbationdirections: Total number of perturbation directions.

        Returns:
            List of indices where Jacobian approximation is needed.
        """
        # Initialize empty List
        indices_jacobian_coordinationequalityconstraints: List[int] = []

        # Check if the user provided Jacobian approximation
        if jacobian_coordinationequalityconstraints is not None:

            # Infer the None-indices for the Jacobian
            # of the coordination equality constraints
            indices_jacobian_coordinationequalityconstraints = [j for j in range(totalnumber_perturbationdirections)
                                                                if any(jacobian_coordinationequalityconstraints[i][j] is None
                                                                for i in range(len(jacobian_coordinationequalityconstraints)))]

        else:

            # Return all indices, since user provided no Jacobian approximation
            indices_jacobian_coordinationequalityconstraints = list(range(totalnumber_perturbationdirections))

        # Return the inferred list of indices to be perturbed for a Jacobian approximation
        # No copy.copy() needed - this list is freshly created within this method, not a stored class attribute.
        return indices_jacobian_coordinationequalityconstraints

    def evaluate_PerturbationDirectionsIndices_LocalInequalityConstraintsJacobian(self,
                                                                                   jacobian_localinequalityconstraints: List[List[float | None]] | None,
                                                                                   totalnumber_perturbationdirections: int) -> List[int]:
        """Return the perturbation direction indices for the active local inequality constraints Jacobian.

        Args:
            jacobian_localinequalityconstraints: The local inequality constraints
                Jacobian with None entries where approximation is needed.
            totalnumber_perturbationdirections: Total number of perturbation
                directions.

        Returns:
            List of indices where Jacobian approximation is needed.
        """
        # Initialize empty List
        indices_jacobian_activelocalinequalityconstraints: List[int] = []

        # Check if the user provided Jacobian approximation
        if jacobian_localinequalityconstraints is not None:

            # Infer the None-indices for the Jacobian
            # of the active local inequality constraints
            indices_jacobian_activelocalinequalityconstraints = [j for j in range(totalnumber_perturbationdirections)
                                                                if any(jacobian_localinequalityconstraints[i][j] is None
                                                                for i in range(len(jacobian_localinequalityconstraints)))]

        else:

            # Return all indices, since user provided no Jacobian approximation
            indices_jacobian_activelocalinequalityconstraints = list(range(totalnumber_perturbationdirections))

        # Return the inferred list of indices to be perturbed for a Jacobian approximation
        # No copy.copy() needed - this list is freshly created within this method, not a stored class attribute.
        return indices_jacobian_activelocalinequalityconstraints

    def evaluate_PerturbationDirectionsIndices_CoordinationInequalityConstraintsJacobian(self, jacobian_coordinationinequalityconstraints: List[List[float | None]] | None,
                                                                                          totalnumber_perturbationdirections: int) -> List[int]:
        """Return the perturbation direction indices for the coordination inequality constraints Jacobian.

        Args:
            jacobian_coordinationinequalityconstraints: The coordination inequality
                constraints Jacobian with None entries where approximation is needed.
            totalnumber_perturbationdirections: Total number of perturbation
                directions.

        Returns:
            List of indices where Jacobian approximation is needed.
        """
        # Initialize empty List
        indices_jacobian_coordinationinequalityconstraints: List[int] = []

        # Check if the user provided Jacobian approximation
        if jacobian_coordinationinequalityconstraints is not None:

            # Infer the None-indices for the Jacobian of all coordination inequality constraints
            indices_jacobian_coordinationinequalityconstraints = [j for j in range(totalnumber_perturbationdirections)
                                                                  if any(jacobian_coordinationinequalityconstraints[i][j] is None
                                                                         for i in range(len(jacobian_coordinationinequalityconstraints)))]

        else:

            # Return all indices, since user provided no Jacobian approximation
            indices_jacobian_coordinationinequalityconstraints = list(range(totalnumber_perturbationdirections))

        # Return the inferred list of indices to be perturbed for a Jacobian approximation
        # No copy.copy() needed - this list is freshly created within this method, not a stored class attribute.
        return indices_jacobian_coordinationinequalityconstraints

    def evaluate_PerturbationDirectionsIndices_MappedResponses(self, local_couplingparameters: List[SubSysCouplingParametersBasis],
                                                          totalnumber_perturbationsdirections: int) -> Dict[str, List[int]]:
        """Return the dictionary of the mapping 'neighborID' to perturbation direction indices.

        Maps 'neighborID' -> indices of coordinate directions
        where the Jacobian of the mapped responses to the
        subsystem w.r.t. ID 'neighborID' needs
        to be approximated.

        Args:
            local_couplingparameters: List of local coupling parameter objects.
            totalnumber_perturbationsdirections: Total number of perturbation directions.

        Returns:
            Dictionary mapping neighbor IDs to lists of perturbation direction indices.
        """
        # Initialize empty dict
        indices_jacobian_mappedresponses: Dict[str, List[int]] = {}

        # Iterate over the local -> controller coupling parameters
        for local_couplingparameter in local_couplingparameters:

            # Check if mapped responses exist
            if local_couplingparameter.get_MappedResponses() is not None:

                # Get ID of the local -> controller coupling parameter
                id: str = local_couplingparameter.get_ID()

                # Call the method for that local -> controller coupling parameter
                indices_jacobian_mappedresponses[id] = self.evaluate_PerturbationDirectionsIndices_MappedResponses_at_Neighbor(local_couplingparameter,
                                                                                                                          totalnumber_perturbationsdirections)

        # Return the inferred list of indices to be perturbed for a Jacobian approximation
        # for each mapped response
        # No copy.copy() needed - this dict is freshly created within this method, not a stored class attribute.
        return indices_jacobian_mappedresponses

    def evaluate_PerturbationDirectionsIndices_MappedResponses_at_Neighbor(self, local_couplingparameter: SubSysCouplingParametersBasis,
                                                                      totalnumber_perturbationsdirections: int) -> List[int]:
        """Return the indices of coordinate directions where the Jacobian of the mapped responses needs to be approximated.

        The Jacobian is for the mapped responses to the
        subsystem in the input 'local_couplingparameter'.
        Note that the Jacobian of mapped responses is stored in
        'local_couplingparameter' by Analysis_xxx.py.

        Args:
            local_couplingparameter: The coupling parameter object for a specific neighbor.
            totalnumber_perturbationsdirections: Total number of perturbation directions.

        Returns:
            List of indices where Jacobian approximation is needed.
        """
        # Initialize empty List
        indices_jacobian_mappedresponse: List[int] = []

        # Get the user defined Jacobian of the mapped responses
        jacobian_mappedresponse: List[List[float | None]] | None = local_couplingparameter.get_Jacobian_MappedResponse()

        # Check if the user provided some derivatives
        if jacobian_mappedresponse is not None:

            # Infer the None-indices for the Jacobian
            # of the mapped responses w.r.t. this
            # localtocontroller_couplingparameter object

            indices_jacobian_mappedresponse = [j for j in range(totalnumber_perturbationsdirections)
                                               if any(jacobian_mappedresponse[i][j] is None for i in range(len(jacobian_mappedresponse)))]

        else:

            # The user has not provided any
            # derivative information

            indices_jacobian_mappedresponse = list(range(totalnumber_perturbationsdirections))

        # Return the inferred list of indices to be perturbed for a Jacobian approximation
        # for the mapped response corresponding to this local -> controller coupling parameter
        # No copy.copy() needed - this list is freshly created within this method, not a stored class attribute.
        return indices_jacobian_mappedresponse

    def evaluate_Gradient_LocalObjective(self) -> None:
        """Evaluate the gradient of the local objective and store it in self._optimdata.
        """

        # Get gradient of local objective
        gradient_localobjective: List[float | None] | None = self._localobjective.evaluate_Gradient_LocalObjective(self)

        # Check if user provided any gradient estimation
        if gradient_localobjective is not None:

            # Store the gradient in optimdata (which checks if the dimensions match, ...)
            self._optimdata.set_Gradient_LocalObjective(gradient_localobjective)

    def evaluate_Gradient_TotalObjective(self) -> None:
        """Add get_Gradient_LocalObjective to get_Gradient_CoordinationObjective depending on subsystem type.

        The total objective gradient is stored in self._optimdata.
        """

        # Initialize local objective gradient
        gradient_localobjective: List[float] | None = None

        # Initialize coordination objective gradient
        gradient_coordinationobjective: List[float] | None = None

        # Initialize total gradient
        gradient_totalobjective: List[float] = []

        # Check if a coordination objective exists
        if self.get_CoordinationObjectiveValue() is not None:

            # Get the gradient of the coordination objective
            # No copy wrapper needed - getter already returns defensive copy
            gradient_coordinationobjective = self._optimdata.get_Gradient_CoordinationObjective()

        # Check if a local objective exists
        if self.get_LocalObjectiveValue() is not None:

            # Get the gradient of the local objective
            # No copy wrapper needed - getter already returns defensive copy
            gradient_localobjective = self._optimdata.get_Gradient_LocalObjective()

        # Compute the gradient of the total objective
        # (for all four cases gradient local / coordination objective is None / not None)

        # If local and coordination objectives exist
        if gradient_coordinationobjective is not None and gradient_localobjective is not None:

            # Store the sum as the total objective gradient
            gradient_totalobjective = [gradient_localobjective[i] + gradient_coordinationobjective[i] for i in range(len(gradient_coordinationobjective))]

        # If local objective does not exist
        elif gradient_localobjective is None:

            # No copy wrapper needed - getter already returns defensive copy and setter creates its own copy
            gradient_totalobjective = gradient_coordinationobjective

        # If coordination does not exist
        elif gradient_coordinationobjective is None:

            # No copy wrapper needed - getter already returns defensive copy and setter creates its own copy
            gradient_totalobjective = gradient_localobjective

        # Set the gradient of the total objective
        if gradient_totalobjective is not None:
            self._optimdata.set_Gradient_TotalObjective(gradient_totalobjective)

    def evaluate_Hessian_LocalObjective(self) -> List[List[float | None]] | None:
        """Evaluate the Hessian of the local objective.

        Returns:
            The Hessian matrix of the local objective, or None if not provided.
        """

        # Get Hessian of the local objective
        hessian_localobjective: List[List[float | None]] | None = self._localobjective.evaluate_Hessian_LocalObjective(self)

        # Check dimensions, if user gave Hessians themselves
        correct_shape = (len(self.get_DesignVariables()), len(self.get_DesignVariables()))
        if hessian_localobjective is not None and np.array(hessian_localobjective).shape != correct_shape:

            raise ValueError(f"{DDO_Color}The size of your Hessian of the local objective of your subsystem with ID {self.get_SUBSYSTEMID()} does not have the correct shape, expected: {correct_shape}, given: {np.array(hessian_localobjective).shape}{Reset}")

        # Return the value
        return hessian_localobjective

    def evaluate_Jacobian_LocalEqualityConstraints(self) -> None:
        """Evaluate the Jacobian of the local equality constraints and store it in self._optimdata.
        """

        # Get Jacobian of the local equality constraints
        jacobian_localequalityconstraints: List[List[float | None]] | None = self._localconstraints.evaluate_Jacobian_EqualityLocalConstraints(self)

        # Check if the user provided any Jacobian estimate
        if jacobian_localequalityconstraints is not None:

            # Store the Jacobian into optimdata (which check for correct dimensions, ...)
            self._optimdata.set_Jacobian_LocalEqualityConstraints(jacobian_localequalityconstraints)

    def evaluate_Jacobian_LocalInequalityConstraints(self) -> None:
        """Evaluate the Jacobian of the local inequality constraints and store it in self._optimdata.
        """

        # Get Jacobian of the local inequality constraints
        jacobian_localinequalityconstraints: List[List[float | None]] | None = self._localconstraints.evaluate_Jacobian_InEqualityLocalConstraints(self)

        # Check if the user provided any Jacobian estimate:
        if jacobian_localinequalityconstraints is not None:

            # Store the Jacobian inside of self._optimdata (which checks correct dimensions, ...)
            self._optimdata.set_Jacobian_LocalInequalityConstraints(jacobian_localinequalityconstraints)

    def evaluate_Hessian_EqualityLocalConstraints(self) -> List[List[List[float | None]]] | None:
        """Evaluate the Hessian of the local equality constraints.

        Returns:
            The Hessian tensor of the local equality constraints, or None if not provided.
        """

        # Get Hessian of the local equality constraints
        hessian_equalityconstraints: List[List[List[float | None]]] | None = self._localconstraints.evaluate_Hessians_EqualityLocalConstraints(self)

        # No existence check needed here: this method is only called after verifying
        # that local equality constraints exist (if-check at the call site)

        # Check dimensions, if user gave gradients themselves
        correct_shape = (len(self.get_EqualityLocalConstraintsValue()), len(self.get_DesignVariables()), len(self.get_DesignVariables()))

        if hessian_equalityconstraints is not None and np.array(hessian_equalityconstraints).shape != correct_shape:

            raise ValueError(f"{DDO_Color}The size of your Hessian of the local equality constraints does not have the correct shape, expected: {correct_shape}, given: {np.array(hessian_equalityconstraints).shape}{Reset}")

        # Return the value
        return hessian_equalityconstraints

    def evaluate_Hessian_InequalityLocalConstraints(self) -> List[List[List[float | None]]] | None:
        """Evaluate the Hessian of the local inequality constraints.

        Returns:
            The Hessian tensor of the local inequality constraints, or None if not provided.
        """

        # Get Hessian of the local inequality constraints
        hessian_inequalityconstraints: List[List[List[float | None]]] | None = self._localconstraints.evaluate_Hessians_InEqualityLocalConstraints(self)

        # Check dimensions, if user gave gradients themselves
        correct_shape = (len(self.get_InequalityLocalConstraintsValue()), len(self.get_DesignVariables()), len(self.get_DesignVariables()))

        if hessian_inequalityconstraints is not None and np.array(hessian_inequalityconstraints).shape != correct_shape:

            raise ValueError(f"{DDO_Color}The size of your Hessian of the local inequality constraints does not have the correct shape, expected: {correct_shape}, given: {np.array(hessian_inequalityconstraints).shape}{Reset}")

        # Return the value
        return hessian_inequalityconstraints

    def evaluate_Jacobian_TotalEqualityConstraints(self) -> None:
        """Evaluate the Jacobian of the total equality constraints if it exists.

        Includes both local and coordination equality constraints.
        The Jacobian is stored in self._optimdata.
        """

        # Initialize Jacobian of all equality constraints
        jacobian_totalequalityconstraints: List[List[float]] = []

        # Check if local equality constraints exist
        if self.get_EqualityLocalConstraintsValue() is not None:

            # Add the Jacobian of the local equality constraints
            # No copy wrapper needed - getter already returns copy.deepcopy()
            jacobian_totalequalityconstraints += self._optimdata.get_Jacobian_LocalEqualityConstraints()

        # Check if coordination equality constraints exist
        if self.get_CoordinationEqualityConstraintValue() is not None:

            # Get the Jacobian of the coordination equality constraints
            # No copy wrapper needed - getter already returns copy.deepcopy()
            jacobian_totalequalityconstraints += self._optimdata.get_Jacobian_CoordinationEqualityConstraints()

        # Check if there are no equality constraints
        if len(jacobian_totalequalityconstraints) == 0:

            # No equality constraints
            jacobian_totalequalityconstraints = None

        # Check if the Jacobian of the total equality constraints exists
        if jacobian_totalequalityconstraints is not None:
            # Store into optimdata
            self._optimdata.set_Jacobian_TotalEqualityConstraints(jacobian_totalequalityconstraints)

    def evaluate_Jacobian_TotalInEqualityConstraints(self) -> None:
        """Evaluate the Jacobian of the total inequality constraints if it exists.

        Includes both local and coordination inequality constraints.
        The Jacobian is stored in self._optimdata.
        """

        # Initialize Jacobian of all inequality constraints
        jacobian_totalinequalityconstraints: List[List[float]] = []

        # Check if local inequality constraints exist
        if self.get_InequalityLocalConstraintsValue() is not None:

            # Add the Jacobian of the local inequality constraints
            # No copy wrapper needed - getter already returns copy.deepcopy()
            jacobian_totalinequalityconstraints += self._optimdata.get_Jacobian_LocalInequalityConstraints()

        # Check if coordination inequality constraints exist
        if self.get_CoordinationInequalityConstraintValue() is not None:

            # Get the Jacobian of the coordination inequality constraints
            jacobian_totalinequalityconstraints += copy.deepcopy(self._optimdata.get_Jacobian_CoordinationInequalityConstraints())

        # Check if anything was appended
        if len(jacobian_totalinequalityconstraints) == 0:

            # No equality constraints
            jacobian_totalinequalityconstraints = None

        # Store the jacobian inside optimdata
        self._optimdata.set_Jacobian_TotalInequalityConstraints(jacobian_totalinequalityconstraints)

    def evaluate_Jacobian_MappedResponses(self) -> None:
        """Evaluate the Jacobians of the mapped responses and store them in the coupling parameters.

        This method calls the mapLocalResponsesDesignVariables_to_CouplingParameters_Jacobians function of self._analysis.
        The method in self._analysis directly calls set_MappedResponses_Jacobian of the
        local subsystem subclass which is abstractly defined, but this is defined in the
        userfiles for the specific design problems
        """

        self._analysis.mapLocalResponsesDesignVariables_to_CouplingParameters_Jacobians(self)

    def evaluate_Hessians_MappedResponses(self) -> List[List[List[List[float | None]]]] | None:
        """Evaluate the Hessians of the mapped responses.

        This method calls the mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian function of self._analysis.

        Returns:
            The Hessian tensor of the mapped responses, or None if not provided.
        """
        # Get Hessians of the mapped responses
        hessian_mappedresponses: List[List[List[List[float | None]]]] | None = self._analysis.mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian(self)

        if hessian_mappedresponses is None:
            return None

        # Get coupling parameters
        couplingparameters: List[CouplingParametersInterface] = self.get_CouplingParameters()

        # Check dimensions, if user gave Hessians themselves
        # NOTE: hessian_mappedresponses is indexed over local-to-local couplings only (no controller
        # entry), so we need index_helper to stay aligned with couplingparameters,
        # analogous to evaluate_Complete_Hessian_MappedResponses in LocalSubSystemALADIN.
        index_helper: int = 0
        for j in range(len(couplingparameters)):

            coupling_j: CouplingParametersInterface = couplingparameters[j]

            # Hessians only if coupling to local subsystem
            if isinstance(coupling_j, SubSysCouplingParametersBasis):

                mappedresponses_j: List[float] | None = coupling_j.get_MappedResponses()

                if mappedresponses_j is not None:

                    # The expected number of mapped-response Hessians equals the number of
                    # mapped responses this subsystem produces for coupling j.
                    correct_shape_j = (len(mappedresponses_j),
                                       len(self.get_DesignVariables()), len(self.get_DesignVariables()))

                    if np.array(hessian_mappedresponses[index_helper]).shape != correct_shape_j:

                        raise ValueError(f"{DDO_Color}The size of your Hessians of the mapped responses to subsystem {coupling_j.get_ID()} does not have the correct shape, expected: {correct_shape_j}, given: {np.array(hessian_mappedresponses[index_helper]).shape}{Reset}")

                index_helper += 1


        # Return the value
        return hessian_mappedresponses

    # Evaluate all Jacobians

    def evaluateAllJacobians(self) -> None:
        """Get the gradients, Jacobians, and Hessians needed for optimization.

        Calls evaluate_Gradient_xxx / evaluate_Jacobian_xxx /
        evaluate_Hessian_xxx of LocalSubSystemBasis.
        It fills in missing information (e.g. by using a jacobian approximator)
        and stores the results via setters into the LocalToControllerCouplingParamaters.
        """

        # Synchronize optimdata and self. coupllingparameters
        self._optimdata.set_CouplingParameters(copy.deepcopy(self.get_CouplingParameters()))

        # Get the number of directions in which perturbations are possible
        totalnumber_perturbationdirections: int = len(self.get_DesignVariables())

        # Evaluate all gradients / Jacobians

        # Local objective gradient
        self.evaluate_Gradient_LocalObjective()
        # Coordination objective gradient
        self.evaluate_Gradient_CoordinationObjective()

        # Jacobian of local equality constraints
        self.evaluate_Jacobian_LocalEqualityConstraints()
        # Jacobian of coordination equality constraints
        self.evaluate_Jacobian_CoordinationEqualityConstraints()

        # Jacobian of local inequality constraints
        self.evaluate_Jacobian_LocalInequalityConstraints()
        # Jacobian of coordination inequality constraints
        self.evaluate_Jacobian_CoordinationInEqualityConstraints()
        # Jacobian of total inequality constraints

        # Get the gradient of the local objective
        gradient_localobjective: List[float | None] | None = self._optimdata.get_Gradient_LocalObjective()
        # Get the indices that need to be perturbed
        indices_gradient_localobjective: List[int] = self.evaluate_PerturbationDirectionsIndices_LocalObjectiveGradient(gradient_localobjective,
                                                                                                                        totalnumber_perturbationdirections)

        # Get the gradient of the coordination objective
        gradient_coordinationobjective: List[float | None] | None = self._optimdata.get_Gradient_CoordinationObjective()
        # Get the indices that need to be perturbed
        indices_gradient_coordinationobjective: List[int] = self.evaluate_PerturbationDirectionsIndices_CoordinationObjectiveGradient(gradient_coordinationobjective,
                                                                                                                                      totalnumber_perturbationdirections)
        # Get the Jacobian of the local equality constraints
        jacobian_localequalityconstraints: List[List[float | None]] | None = self._optimdata.get_Jacobian_LocalEqualityConstraints()
        # Get the indices that need to be perturbed
        indices_jacobian_localequalityconstraints: List[int] = self.evaluate_PerturbationDirectionsIndices_LocalEqualityConstraintsJacobian(jacobian_localequalityconstraints,
                                                                                                                                            totalnumber_perturbationdirections)
        # Get the Jacobian of the coordination equality constraints
        jacobian_coordinationequalityconstraints: List[List[float | None]] | None = self._optimdata.get_Jacobian_CoordinationEqualityConstraints()
        # Get the indices that need to be perturbed
        indices_jacobian_coordinationequalityconstraints: List[int] = self.evaluate_PerturbationDirectionsIndices_CoordinationEqualityConstraintsJacobian(jacobian_coordinationequalityconstraints,
                                                                                                                                                          totalnumber_perturbationdirections)

        # Get the Jacobian of the (active) local inequality constraints
        jacobian_localinequalityconstraints: List[List[float | None]] | None = self._optimdata.get_Jacobian_LocalInequalityConstraints()
        # Get the indices that need to be perturbed
        indices_jacobian_localinequalityconstraints: List[int] = self.evaluate_PerturbationDirectionsIndices_LocalInequalityConstraintsJacobian(jacobian_localinequalityconstraints,
                                                                                                                                                totalnumber_perturbationdirections)

        # Get the Jacobian of the (active) coordination inequality constraints
        jacobian_coordinationinequalityconstraints: List[List[float | None]] | None = self._optimdata.get_Jacobian_CoordinationInequalityConstraints()
        # Get the indices that need to be perturbed
        indices_jacobian_coordinationinequalityconstraints: List[int] = self.evaluate_PerturbationDirectionsIndices_CoordinationInequalityConstraintsJacobian(jacobian_coordinationinequalityconstraints,
                                                                                                                                                             totalnumber_perturbationdirections)
        # Get the list of SubSysCouplingParametersBasis
        local_couplingparameters: List[SubSysCouplingParametersBasis] = self._optimdata.get_LocalCouplingParameters()

        # Get the indices that need to be perturbed
        dict_indices_jacobians_mappedresponses: Dict[str, List[int]] = self.evaluate_PerturbationDirectionsIndices_MappedResponses(local_couplingparameters,
                                                                                                                                   totalnumber_perturbationdirections)

        # No 'evaluate_Jacobian_MappedResponses' is called here, because the specific Analysis_xxx.py files
        # already set the user estimated of the Jacobians into the LocalToController_CouplingParameters


        # Unite all perturbation direction indices that are needed for all three quantities
        # gradient of local objective, Jacobian of local equality constraints and Jacobian
        # of local inequality constraints

        # Unite the indices to be perturbed of the mapped responses
        indices_jacobians_mappedresponses: Set[int] = set().union(*dict_indices_jacobians_mappedresponses.values())

        # Unite all to be perturbed indices
        perturbation_directions_indices: List[int] = sorted(set(indices_gradient_localobjective) |
                                                            set(indices_gradient_coordinationobjective) |
                                                            set(indices_jacobian_localequalityconstraints) |
                                                            set(indices_jacobian_coordinationequalityconstraints) |
                                                            set(indices_jacobian_localinequalityconstraints) |
                                                            set(indices_jacobian_coordinationinequalityconstraints) |
                                                            set(indices_jacobians_mappedresponses))

        # Run the finite differences jacobian approximator, which only executes finite differences
        # on the directions specified by perturbation_directions_indices
        # The self._finite_differences_jacobian will store the results in itself
        self._finite_differences_jacobian.run(subsystem=self, perturbation_directions_indices_list=perturbation_directions_indices)

        # In the following, the None fields in the initially user-returned will be
        # overwritten by the finite_differences_jacobian's entries
        # Already user-given values are not overwritten
        # The update only happens on the indices that were None

        # Write into gradient / Jacobians the approximations

        # Fill in the missing values of the gradient of the local objective
        if self._finite_differences_jacobian.get_Gradient_LocalObjective() is not None:
            self.update_LocalObjective_Gradient(gradient_localobjective,
                                                indices_gradient_localobjective)

        # Fill in the missing values of the gradient of the coordination objective
        if self._finite_differences_jacobian.get_Gradient_CoordinationObjective() is not None:
            self.update_CoordinationObjective_Gradient(gradient_coordinationobjective,
                                                       indices_gradient_coordinationobjective)

        # Fill in the missing values of the Jacobian of the local equality constraints
        if self._finite_differences_jacobian.get_Jacobian_LocalEqualityConstraints() is not None:
            self.update_Jacobian_LocalEqualityConstraints(jacobian_localequalityconstraints,
                                                          indices_jacobian_localequalityconstraints)

        # Fill in the missing values of the Jacobian of the coordination equality constraints
        if self._finite_differences_jacobian.get_Jacobian_CoordinationEqualityConstraints() is not None:
            self.update_Jacobian_CoordinationEqualityConstraints(jacobian_coordinationequalityconstraints,
                                                                 indices_jacobian_coordinationequalityconstraints)

        # Fill in the missing values of the Jacobian of the active local inequality constraints
        if self._finite_differences_jacobian.get_Jacobian_LocalInEqualityConstraints() is not None:
            self.update_Jacobian_LocalInequalityConstraints(jacobian_localinequalityconstraints,
                                                            indices_jacobian_localinequalityconstraints)

        # Fill in the missing values of the Jacobian of the coordination inequality constraints
        if self._finite_differences_jacobian.get_Jacobian_CoordinationInEqualityConstraints() is not None:
            self.update_Jacobian_CoordinationInequalityConstraints(jacobian_coordinationinequalityconstraints,
                                                                   indices_jacobian_coordinationinequalityconstraints)

        # Fill in the missing values of the Jacobian(s) of the mapped responses
        self.update_Jacobians_MappedResponses(local_couplingparameters,
                                              dict_indices_jacobians_mappedresponses)

        # Fill in the missing values of the Jacobian of the lower bounds
        self.update_Jacobian_LowerBounds(totalnumber_perturbationdirections)

        # Fill in the missing values of the Jacobian of the upper bounds
        self.update_Jacobian_UpperBounds(totalnumber_perturbationdirections)

        # Now evaluate the total gradients / Jacobians
        self.evaluate_Gradient_TotalObjective()
        self.evaluate_Jacobian_TotalEqualityConstraints()
        self.evaluate_Jacobian_TotalInEqualityConstraints()

    def update_LocalObjective_Gradient(self, gradient_localobjective: List[float | None] | None,
                                       indices_gradient_localobjective: List[int]) -> None:
        """Update the missing entries of the gradient of the local objective using finite differences.

        Args:
            gradient_localobjective: The local objective gradient with None entries
                where approximation is needed.
            indices_gradient_localobjective: Indices of coordinate directions to update.
        """

        # Finite differences approximation
        # No copy wrapper needed - get_Gradient_LocalObjective() already returns a defensive copy
        finite_differences_localobjective_gradient: List[float | None] = self._finite_differences_jacobian.get_Gradient_LocalObjective()

        # If user did not provide any gradient information
        if gradient_localobjective is None:

            # Use the self._finite_differences_jacobian approximator
            # No copy.copy() needed - getter already returned a defensive copy
            gradient_localobjective = finite_differences_localobjective_gradient

        # Else, the user provided some approximation
        else:

            # Update None fields of the gradient of the local objective
            for j in indices_gradient_localobjective:
                # No copy.copy() needed - float is immutable; assignment creates a new binding
                gradient_localobjective[j] = finite_differences_localobjective_gradient[j]

        # Store into the optimdata
        self._optimdata.set_Gradient_LocalObjective(gradient_localobjective)

    def update_CoordinationObjective_Gradient(self, gradient_coordinationobjective: List[float | None] | None,
                                              indices_gradient_coordinationobjective: List[int]) -> None:
        """Update the missing entries of the gradient of the coordination objective using finite differences.

        Args:
            gradient_coordinationobjective: The coordination objective gradient with None entries
                where approximation is needed.
            indices_gradient_coordinationobjective: Indices of coordinate directions to update.
        """

        # Finite differences approximation
        # No copy wrapper needed - get_Gradient_CoordinationObjective() already returns a defensive copy
        finite_differences_coordinationobjective_gradient: List[float | None] = self._finite_differences_jacobian.get_Gradient_CoordinationObjective()

        # If user did not provide any gradient information
        if gradient_coordinationobjective is None:

            # Use the self._finite_differences_jacobian approximator
            # No copy.copy() needed - getter already returned a defensive copy
            gradient_coordinationobjective = finite_differences_coordinationobjective_gradient

        # Else, the user provided some approximation
        else:

            # Update None fields of the gradient of the coordination objective
            for j in indices_gradient_coordinationobjective:
                # No copy.copy() needed - float is immutable; assignment creates a new binding
                gradient_coordinationobjective[j] = finite_differences_coordinationobjective_gradient[j]

        # Store into the optimdata
        self._optimdata.set_Gradient_CoordinationObjective(gradient_coordinationobjective)

    def update_Jacobian_LocalEqualityConstraints(self, jacobian_localequalityconstraints: List[List[float | None]] | None,
                                                 indices_jacobian_localequalityconstraints: List[int]) -> None:

        """Update the missing entries of the Jacobian of the local equality constraints using finite differences.

        Args:
            jacobian_localequalityconstraints: The Jacobian with None entries
                where approximation is needed.
            indices_jacobian_localequalityconstraints: Indices of coordinate directions to update.
        """

        # Finite differences approximation
        # No copy wrapper needed - get_Jacobian_LocalEqualityConstraints() already returns a defensive copy
        finite_differences_localequalityconstraints_jacobian: List[List[float | None]] = self._finite_differences_jacobian.get_Jacobian_LocalEqualityConstraints()

        # If user did not provide any Jacobian information
        if jacobian_localequalityconstraints is None:

            # Use the self._finite_differences_jacobian approximator
            # No copy.deepcopy() needed - getter already returned a defensive copy
            jacobian_localequalityconstraints = finite_differences_localequalityconstraints_jacobian

        # Else, the user provided some approximation
        else:

            # Iterate over the rows of the Jacobian of equality constraints
            for i in range(len(jacobian_localequalityconstraints)):

                # Iterate over all columns where finite differences were computed
                for j in indices_jacobian_localequalityconstraints:

                    # If the Jacobian entry is None
                    if jacobian_localequalityconstraints[i][j] is None:

                        # Update the associated entry
                        # No copy needed - float is immutable; assignment creates a new binding
                        jacobian_localequalityconstraints[i][j] = finite_differences_localequalityconstraints_jacobian[i][j]

        # Store into self._optimdata
        self._optimdata.set_Jacobian_LocalEqualityConstraints(jacobian_localequalityconstraints)

    def update_Jacobian_CoordinationEqualityConstraints(self, jacobian_coordinationequalityconstraints: List[List[float | None]] | None,
                                                        indices_jacobian_coordinationequalityconstraints: List[int]) -> None:

        """
        Update the missing entries of the Jacobian of the coordination equality constraints using finite differences.

        Args:
            jacobian_coordinationequalityconstraints: The Jacobian with None entries
                where approximation is needed.
            indices_jacobian_coordinationequalityconstraints: Indices of coordinate directions to update.
        """

        # Finite differences approximation
        # No copy wrapper needed - get_Jacobian_CoordinationEqualityConstraints() already returns a defensive copy
        finite_differences_coordinationequalityconstraints_jacobian: List[List[float | None]] = self._finite_differences_jacobian.get_Jacobian_CoordinationEqualityConstraints()

        # If user did not provide any Jacobian information
        if jacobian_coordinationequalityconstraints is None:

            # Use the self._finite_differences_jacobian approximator
            # No copy.deepcopy() needed - getter already returned a defensive copy
            jacobian_coordinationequalityconstraints = finite_differences_coordinationequalityconstraints_jacobian

        # Else, the user provided some approximation
        else:

            # Iterate over the rows of the Jacobian of equality constraints
            for i in range(len(jacobian_coordinationequalityconstraints)):

                # Iterate over all columns where finite differences were computed
                for j in indices_jacobian_coordinationequalityconstraints:

                    # If the Jacobian entry is None
                    if jacobian_coordinationequalityconstraints[i][j] is None:

                        # Update the associated entry
                        # No copy needed - float is immutable; assignment creates a new binding
                        jacobian_coordinationequalityconstraints[i][j] = finite_differences_coordinationequalityconstraints_jacobian[i][j]

        # Store into self._optimdata
        self._optimdata.set_Jacobian_CoordinationEqualityConstraints(jacobian_coordinationequalityconstraints)

    def update_Jacobian_LocalInequalityConstraints(self, 
                                                   jacobian_localinequalityconstraints: List[List[float | None]] | None,
                                                   indices_jacobian_localinequalityconstraints: List[int]) -> None:

        """
        Update the missing entries of the Jacobian of the local inequality constraints using finite differences.

        Args:
            jacobian_localinequalityconstraints: The Jacobian with None entries
                where approximation is needed.
            indices_jacobian_localinequalityconstraints: Indices of coordinate directions to update.
        """

        # Finite differences approximation
        # No copy wrapper needed - get_Jacobian_LocalInEqualityConstraints() already returns a defensive copy
        finite_differences_localinequalityconstraints_jacobian: List[List[float | None]] = self._finite_differences_jacobian.get_Jacobian_LocalInEqualityConstraints()

        # If user did not provide any Jacobian information
        if jacobian_localinequalityconstraints is None:

            # Use the self._finite_differences_jacobian approximator
            # No copy.deepcopy() needed - getter already returned a defensive copy
            jacobian_localinequalityconstraints = finite_differences_localinequalityconstraints_jacobian

        # Iterate over the rows of the Jacobian of the local inequality constraints
        for i in range(len(jacobian_localinequalityconstraints)):

            # Iterate over all columns where finite differences were computed
            for j in indices_jacobian_localinequalityconstraints:

                # If the Jacobian entry is None
                if jacobian_localinequalityconstraints[i][j] is None:

                    # Update the associated entry
                    # No copy needed - float is immutable; assignment creates a new binding
                    jacobian_localinequalityconstraints[i][j] = finite_differences_localinequalityconstraints_jacobian[i][j]

        # Store into the self._optimdata
        self._optimdata.set_Jacobian_LocalInequalityConstraints(jacobian_localinequalityconstraints)

    def update_Jacobian_CoordinationInequalityConstraints(self,
                                                          jacobian_coordinationinequalityconstraints: List[List[float | None]] | None,
                                                          indices_jacobian_coordinationinequalityconstraints: List[int]) -> None:

        """
        Update the missing entries of the Jacobian of all coordination inequality constraints using finite differences.

        Args:
            jacobian_coordinationinequalityconstraints: The Jacobian with None entries
                where approximation is needed.
            indices_jacobian_coordinationinequalityconstraints: Indices of coordinate directions to update.
        """

        # Finite differences approximation
        # No copy wrapper needed - get_Jacobian_CoordinationInEqualityConstraints() already returns a defensive copy
        finite_differences_coordinationinequalityconstraints_jacobian: List[List[float | None]] = self._finite_differences_jacobian.get_Jacobian_CoordinationInEqualityConstraints()

        # If user did not provide any Jacobian information
        if jacobian_coordinationinequalityconstraints is None:

            # Use the self._finite_differences_jacobian approximator
            # No copy.deepcopy() needed - getter already returned a defensive copy
            jacobian_coordinationinequalityconstraints = finite_differences_coordinationinequalityconstraints_jacobian

        # Iterate over all rows of the Jacobian of the coordination inequality constraints
        for i in range(len(jacobian_coordinationinequalityconstraints)):

            # Iterate over all columns where finite differences were computed
            for j in indices_jacobian_coordinationinequalityconstraints:

                # If the Jacobian entry is None
                if jacobian_coordinationinequalityconstraints[i][j] is None:

                    # Update the associated entry
                    # No copy needed - float is immutable; assignment creates a new binding
                    jacobian_coordinationinequalityconstraints[i][j] = finite_differences_coordinationinequalityconstraints_jacobian[i][j]

        # Store into the self._optimdata
        self._optimdata.set_Jacobian_CoordinationInequalityConstraints(jacobian_coordinationinequalityconstraints)

    def update_Jacobians_MappedResponses(self,
                                         local_couplingparameters: List[SubSysCouplingParametersBasis],
                                         dict_indices_jacobians_mappedresponses: Dict[str, List[int]]) -> None:
        """
        Update the missing entries of the Jacobians of the mapped responses using finite differences.

        Args:
            local_couplingparameters: List of local coupling parameters to update.
            dict_indices_jacobians_mappedresponses: Dictionary mapping neighbor IDs to
                indices of coordinate directions to update.
        """

        # Update the None fields of the Jacobians of the mapped responses

        # Get the finite differences approximation
        finite_differences_jacobians_mappedresponses: Dict[str, List[List[float | None]]] = self._finite_differences_jacobian.get_Jacobians_MappedResponses()

        # Iterate over each i <-> j coupling parameter
        for local_couplingparameter in local_couplingparameters:

            # Check if the mapped response exists
            if local_couplingparameter.get_MappedResponses() is not None:

                # Get the ID associated to the coupling
                coupling_id: str = local_couplingparameter.get_ID()

                # Get the user-given estimation of the Jacobian of the mapped responses corresponding
                # to the specific SubSysCouplingParametersBasis object
                jacobian_mappedresponses: List[List[float | None]] | None = local_couplingparameter.get_Jacobian_MappedResponse()

                # If the user did not provide any Jacobian estimation guess
                if jacobian_mappedresponses is None:

                    # Use the finite difference approximation
                    jacobian_mappedresponses = finite_differences_jacobians_mappedresponses[coupling_id]

                    # Store into the couplingparameter
                    local_couplingparameter.set_Jacobian_MappedResponse(jacobian_mappedresponses)

                # Else, the user does provide a Jacobian guess of the mapped responses
                else:

                    # Iterate over the rows of the Jacobian of the mapped responses
                    # associated to the coupling i <-> j

                    for i in range(len(jacobian_mappedresponses)):

                        # Iterate over all columns where the need for finite differences were identified
                        # for mapped responses

                        for j in dict_indices_jacobians_mappedresponses[coupling_id]:

                            # If the original Jacobian entry is None:
                            if jacobian_mappedresponses[i][j] is None:

                                # Update the associated entry
                                local_couplingparameter.set_Jacobian_MappedResponse_at_Position(i, j, finite_differences_jacobians_mappedresponses[coupling_id][i][j])

    def update_Jacobian_LowerBounds(self, totalnumber_perturbationdirections: int) -> None:
        """Compute and store the Jacobian of all lower bounds.

        The Jacobian of the lower bound constraints g_i(x) = -x_i + lb_i <= 0
        is a negative identity matrix: each row i has -1 on the diagonal and 0
        elsewhere. Computed for all bounds regardless of active set.

        Args:
            totalnumber_perturbationdirections: Total number of perturbation directions.
        """

        # Build the Jacobian: negative identity (number_bounds x number_designvariables)
        jacobian_lowerbounds: List[List[float]] = [[0.0 for j in range(totalnumber_perturbationdirections)] for i in range(totalnumber_perturbationdirections)]

        for i in range(totalnumber_perturbationdirections):
            jacobian_lowerbounds[i][i] = -1.0

        # Store into optimdata
        self._optimdata.set_Jacobian_LowerBounds(jacobian_lowerbounds)

    def update_Jacobian_UpperBounds(self, totalnumber_perturbationdirections: int) -> None:
        """Compute and store the Jacobian of all upper bounds.

        The Jacobian of the upper bound constraints g_i(x) = x_i - ub_i <= 0
        is a positive identity matrix: each row i has +1 on the diagonal and 0
        elsewhere. Computed for all bounds regardless of active set.

        Args:
            totalnumber_perturbationdirections: Total number of perturbation directions.
        """

        # Build the Jacobian: positive identity (number_bounds x number_designvariables)
        jacobian_upperbounds: List[List[float]] = [[0.0 for j in range(totalnumber_perturbationdirections)] for i in range(totalnumber_perturbationdirections)]

        for i in range(totalnumber_perturbationdirections):
            jacobian_upperbounds[i][i] = 1.0

        # Store into self._optimdata
        self._optimdata.set_Jacobian_UpperBounds(jacobian_upperbounds)

    def get_MappedResponse_Jacobian(self, id: str) -> List[List[float]]:
        """Get from the LocalToLocalForController_CouplingParameters the mapped responses Jacobian.

        Args:
            id: Identifier of the neighbor.

        Returns:
            The Jacobian matrix of the mapped responses for the given neighbor.
        """
        # Delegates to self._optimdata which handles defensive copying internally.
        return self._optimdata.get_Jacobian_MappedResponse(id)


    def set_MappedResponses_Jacobian(self, id: str, mappedresponses_jacobian_in: List[List[float | None]]) -> None:
        """Set the mapped responses Jacobian in the LocalToLocalForController_CouplingParameters.

        Only sets values if every entry is a float and the lengths are correct (which is not checked here,
        but typically in evaluateAllJacobians).

        Args:
            id: Identifier of the neighbor subsystem.
            mappedresponses_jacobian_in: The Jacobian matrix to set.
        """

        # Get the coupling parameter with the provided ID, if it exists
        couplingparameter: CouplingParametersInterface = self.get_CouplingParameter_with_ID(id)

        # Check if it is a local <-> local coupling parameter
        if not isinstance(couplingparameter, SubSysCouplingParametersBasis):

            # raise error
            raise TypeError(f"{DDO_Color}The coupling parameter corresponding to the ID {id} you provided "
                            f"is not a local <-> local coupling parameter. Please double check which ID "
                            f"is provided{Reset}")

        # Check if the dimensions of the Jacobian of the mapped responses are the same as expected
        if np.array(mappedresponses_jacobian_in).shape != (len(couplingparameter.get_MappedResponses()), len(self.get_DesignVariables())):

            # The dimensions do not match
            raise ValueError(f"{DDO_Color}Your provided Jacobian of the mapped response w.r.t subsystem {id} has wrong dimensions; "
                             f"Expected: {(len(couplingparameter.get_MappedResponses()), len(self.get_DesignVariables()))}, "
                             f"Provided: {np.array(mappedresponses_jacobian_in).shape}{Reset}")

        self._optimdata.set_Jacobian_MappedResponses(id, mappedresponses_jacobian_in)
        # Delegates to self._optimdata which handles defensive copying internally.

        # Also store into self._couplingparameters so that evaluateAllJacobians (which
        # deep-copies self._couplingparameters into optimdata at its start) preserves
        # the user-provided Jacobian instead of overwriting it with None.
        # No copy wrapper needed - setter creates its own defensive copy.
        couplingparameter.set_Jacobian_MappedResponse(mappedresponses_jacobian_in)

    def get_LocalObjective_Gradient(self) -> List[float]:
        """Return the local objective gradient from self._optimdata.

        Returns:
            The gradient of the local objective function.
        """
        # Delegates to self._optimdata which handles defensive copying internally.
        return self._optimdata.get_Gradient_LocalObjective()

    def set_LocalObjective_Gradient(self, localobjective_gradient_in: List[float]) -> None:
        """Set the local objective gradient in self._optimdata.

        Args:
            localobjective_gradient_in: The local objective gradient to set.
        """

        # Delegates to self._optimdata which handles defensive copying internally.
        # Set gradient of local objective
        self._optimdata.set_Gradient_LocalObjective(localobjective_gradient_in)

    def get_LocalEqualityConstraint_Jacobian(self) -> List[List[float]]:
        """Return the Jacobian of the local equality constraints from self._optimdata.

        Returns:
            The Jacobian matrix of the local equality constraints.
        """
        # Delegates to self._optimdata which handles defensive copying internally.
        return self._optimdata.get_Jacobian_LocalEqualityConstraints()

    def set_LocalEqualityConstraint_Jacobian(self, localequalityconstraints_gradient_in: List[List[float]]) -> None:
        """Set the Jacobian of the local equality constraints in self._optimdata.

        Args:
            localequalityconstraints_gradient_in: The Jacobian to set.
        """

        # Delegates to self._optimdata which handles defensive copying internally.
        # Sets the Jacobian of the local equality constraints
        self._optimdata.set_Jacobian_LocalEqualityConstraints(localequalityconstraints_gradient_in)

    def get_LocalActiveInequalityConstraint_Jacobian(self) -> List[List[float]]:
        """Return the Jacobian of the local inequality constraints from self._optimdata.

        Returns:
            The Jacobian matrix of the local inequality constraints.
        """
        # Delegates to self._optimdata which handles defensive copying internally.
        return self._optimdata.get_Jacobian_LocalInequalityConstraints()

    def set_LocalActiveInequalityConstraint_Jacobian(self, localactiveinequalityconstraints_gradient_in: List[List[float]]) -> None:
        """Set the Jacobian of the local inequality constraints in self._optimdata.

        Args:
            localactiveinequalityconstraints_gradient_in: The Jacobian to set.
        """

        # Delegates to self._optimdata which handles defensive copying internally.
        # Sets the Jacobian of the local inequality constraints
        self._optimdata.set_Jacobian_LocalInequalityConstraints(localactiveinequalityconstraints_gradient_in)

########################################################################################################################
#   Functions to handle reference data provided by user used to perform algorithm analysis
########################################################################################################################

    def set_ReferenceDesignVariables(self, refdesignvariables: List[float] | List[None]) -> None:
        """Set the reference design variables (scaled01 values).

        Args:
            refdesignvariables: Reference design variable values.
                Can be a list of floats in [0.0, 1.0] or a list of None values.
        """
        if len(self._designvariables) != len(refdesignvariables):
            raise ValueError(f"{DDO_Color}Length of Design Variables doesn't match with Length of reference design variables{Reset}")

        # Determine if this is a List[None] or List[float] case
        is_all_none = all(value is None for value in refdesignvariables)

        # List[float] case: validate range and granularity
        if not is_all_none:
            rdv_array = np.array(refdesignvariables)
            # Check lower bound
            if not np.all((rdv_array >= 0.0) | np.isclose(rdv_array, 0.0, atol=1e-8, rtol=0)):
                if not self._referencedesignvariables_lower_scaler_bound_warning_raised:
                    self._referencedesignvariables_lower_scaler_bound_warning_raised = True
                    ddo_print("WARNING: All reference design variables must be within the range [0.0, 1.0] (with tolerance 1e-8)")
            # Check upper bound
            if not np.all((rdv_array <= 1.0) | np.isclose(rdv_array, 1.0, atol=1e-8, rtol=0)):
                if not self._referencedesignvariables_upper_scaler_bound_warning_raised:
                    self._referencedesignvariables_upper_scaler_bound_warning_raised = True
                    ddo_print("WARNING: All reference design variables must be within the range [0.0, 1.0] (with tolerance 1e-8)")

            # Check whether the to-be-set designvariables fit with the specified granularity
            granularity = self._designvariables_granularity
            if granularity is not None:
                for i in range(len(refdesignvariables)):
                    granularity_i = granularity[i]
                    if granularity_i == 0.0:
                        # 0.0 means continuous - no check needed
                        pass
                    elif granularity_i > 0.0:
                        # Check if design variable is a multiple of the granularity using modulo
                        remainder = np.mod(refdesignvariables[i], granularity_i)
                        if np.isclose(remainder, 0.0) or np.isclose(remainder, granularity_i):
                            pass
                        else:
                            raise ValueError(f"{DDO_Color}Reference Design variable at index {i} with value {refdesignvariables[i]} does not match the required granularity of {granularity_i}{Reset}")
                    else:
                        raise ValueError(f"{DDO_Color}Invalid granularity value at index {i}: {granularity_i}. Must be >= 0.0{Reset}")
            else:
                raise ValueError(f"{DDO_Color}DesignVariable Granularity must be defined before setting any reference design variables{Reset}")

        # Assign reference design variables (single assignment point)
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._referencedesignvariables = copy.copy(refdesignvariables)  # scaled01 values
        if is_all_none:
            self._referencedesignvariables_unscaled = copy.copy(refdesignvariables)
        else:
            scaling_variables = self.get_Scalers()
            # No copy.copy needed: list comprehension over primitive types (float) already creates a new list
            self._referencedesignvariables_unscaled = [
                scaling_variables[i].inverse_transform(refdesignvariables[i])
                for i in range(len(refdesignvariables))
            ]

    def get_ReferenceDesignVariables(self) -> List[float] | List[None] | None:
        """Get the reference design variables.

        Returns:
            The reference design variables (scaled), or None if not set.
        """
        # copy.copy() needed: List is mutable, so changes by caller are not reflected back unless setter is called explicitly
        return copy.copy(self._referencedesignvariables)

    def get_ReferenceDesignVariables_Unscaled(self) -> List[float] | List[None] | None:
        """Get the unscaled reference design variables.

        Returns:
            The reference design variables (unscaled), or None if not set.
        """
        # copy.copy() needed: List is mutable, so changes by caller are not reflected back unless setter is called explicitly
        return copy.copy(self._referencedesignvariables_unscaled)

    def set_ReferenceLocalObjectiveValue(self, referencelocalobjectivevalue: float | None) -> None:
        """Set the reference local objective value.

        Args:
            referencelocalobjectivevalue: The reference local objective value to set.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        self._referencelocalobjectivevalue = referencelocalobjectivevalue

    def get_ReferenceLocalObjectiveValue(self) -> float | None:

        """Get the reference local objective value.

        Returns:
            The reference local objective value, or None if not set.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._referencelocalobjectivevalue

    def set_ReferenceLocalObjectiveValueUnscaled(self, referencelocalobjectivevalueunscaled: float | None) -> None:
        """Set the unscaled reference local objective value.

        Args:
            referencelocalobjectivevalueunscaled: The unscaled reference local objective value to set.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        self._referencelocalobjectivevalueunscaled = referencelocalobjectivevalueunscaled

    def get_ReferenceLocalObjectiveValueUnscaled(self) -> float | None:

        """Get the unscaled reference local objective value.

        Returns:
            The unscaled reference local objective value, or None if not set.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._referencelocalobjectivevalueunscaled

########################################################################################################################
#   Functions to handle coupling parameters related to modelling a distributed optimization problem.
#   This only works on mappedresponses, couplingvariables, shareddesignvariables, targetshareddesignvariables
#   and their copy_-counterparts.
#   Nothing related to coordination parameters
########################################################################################################################

    def set_MappedResponseVariables(self, id: str, mappedresponsesin: List[float], mappedresponsesin_unscaled: List[float]) -> None:
        """Store the mapped response variables for the neighboring subsystems.

        Args:
            id: Identifier of the neighbor.
            mappedresponsesin: Mapped response values (scaled to [0, 1]).
            mappedresponsesin_unscaled: Mapped response values (unscaled).
        """

        # Check that scaled and unscaled lists have the same length
        if len(mappedresponsesin_unscaled) != len(mappedresponsesin):
            raise ValueError(f"{DDO_Color}Length mismatch: mappedresponsesin has {len(mappedresponsesin)} elements, but mappedresponsesin_unscaled has {len(mappedresponsesin_unscaled)} elements!{Reset}")

        # couplingparameters
        couplingparameters: List[CouplingParametersInterface] = self.get_CouplingParameters()

        # Get all occurences of the id
        id_occurrences: List[int] = [i for i in range(len(couplingparameters)) if isinstance(couplingparameters[i], SubSysCouplingParametersBasis) and couplingparameters[i].get_ID() == id]

        # If no occurence of the id in the ids of couplingparameters
        if len(id_occurrences) == 0:
            raise ValueError(f"{DDO_Color}There exists no neighboring subsystem with the ID {id}!{Reset}")

        # If there are more than one occurences of the id within couplingparameters
        if len(id_occurrences) > 1:
            raise ValueError(f"{DDO_Color}There are duplicate coupling parameters to the neighbor with ID {id}. Please make sure that each neighbor only has one coupling parameter!{Reset}")

        # Now, the only item in this list gives the index of the associated coupling parameter
        id_index: int = id_occurrences[0]

        # Get the associated coupling parameter
        couplingparameter: CouplingParametersInterface = couplingparameters[id_index]

        if isinstance(couplingparameter, SubSysCouplingParametersBasis):
            # No copy.copy() wrapper needed - setter creates its own defensive copy
            # store mapped variables
            couplingparameter.set_MappedResponses(mappedresponsesin)
            couplingparameter.set_MappedResponses_Unscaled(mappedresponsesin_unscaled)

    def set_Copy_MappedResponseVariables(self, id: str, copymappedresponsesin: List[float]) -> None:
        """Copy the mapped variables from neighboring subsystems (scaled01 values).

        Args:
            id: Identifier of the neighbor.
            copymappedresponsesin: Copy of mapped response values (scaled to [0, 1]).
        """

        # couplingparameters
        couplingparameters: List[CouplingParametersInterface] = self.get_CouplingParameters()

        # Get all occurences of the id
        id_occurrences: List[int] = [i for i in range(len(couplingparameters)) if isinstance(couplingparameters[i], SubSysCouplingParametersBasis) and couplingparameters[i].get_ID() == id]

        # If no occurence of the id in the ids of couplingparameters
        if len(id_occurrences) == 0:
            raise ValueError(f"{DDO_Color}There exists no neighboring subsystem with the ID {id}!{Reset}")

        # If there are more than one occurences of the id within couplingparameters
        if len(id_occurrences) > 1:
            raise ValueError(f"{DDO_Color}There are duplicate coupling parameters to the neighbor with ID {id}. Please make sure that each neighbor only has one coupling parameter!{Reset}")

        # Now, the only item in this list gives the index of the associated coupling parameter
        id_index: int = id_occurrences[0]

        # Get the associated coupling parameter
        couplingparameter: CouplingParametersInterface = couplingparameters[id_index]

        if isinstance(couplingparameter, SubSysCouplingParametersBasis):
            # No copy.copy() wrapper needed - setter creates its own defensive copy
            # store copy mapped variables
            couplingparameter.set_Copy_MappedResponses(copymappedresponsesin)

    def get_Copy_MappedResponseVariables(self, id: str) -> List[float] | None:
        """Get the copy of mapped variables from neighboring subsystems (scaled01 values).

        Args:
            id: Identifier of the neighbor.

        Returns:
            Copy of mapped response values (scaled to [0, 1]).
        """

        # couplingparameters
        couplingparameters: List[CouplingParametersInterface] = self.get_CouplingParameters()

        # Get all occurences of the id
        id_occurrences: List[int] = [i for i in range(len(couplingparameters)) if isinstance(couplingparameters[i], SubSysCouplingParametersBasis) and couplingparameters[i].get_ID() == id]

        # If no occurence of the id in the ids of couplingparameters
        if len(id_occurrences) == 0:
            raise ValueError(f"{DDO_Color}There exists no neighboring subsystem with the ID {id}!{Reset}")

        # If there are more than one occurences of the id within couplingparameters
        if len(id_occurrences) > 1:
            raise ValueError(f"{DDO_Color}There are duplicate coupling parameters to the neighbor with ID {id}. Please make sure that each neighbor only has one coupling parameter!{Reset}")

        # Now, the only item in this list gives the index of the associated coupling parameter
        id_index: int = id_occurrences[0]

        # Get the associated coupling parameter
        couplingparameter: CouplingParametersInterface = couplingparameters[id_index]

        if isinstance(couplingparameter, SubSysCouplingParametersBasis):

            # get copy mapped variables
            # No copy wrapper needed - getter already returns defensive copy
            copymappedresponses: List[float] | None = couplingparameter.get_Copy_MappedResponses()

            return copymappedresponses

    def set_CouplingVariables(self, id: str, couplingvariablein: List[float], couplingvariablein_unscaled: List[float]) -> None:
        """Store the target coupling variables for each individual subsystem.

        Args:
            id: Identifier of the neighboring subsystem.
            couplingvariablein: Target variable for the physical response of the neighboring subsystem (scaled to [0, 1]).
            couplingvariablein_unscaled: Target variable for the physical response of the neighboring subsystem (unscaled).
        """

        # Check that scaled and unscaled lists have the same length
        if len(couplingvariablein_unscaled) != len(couplingvariablein):
            raise ValueError(f"{DDO_Color}Length mismatch: couplingvariablein has {len(couplingvariablein)} elements, but couplingvariablein_unscaled has {len(couplingvariablein_unscaled)} elements!{Reset}")

        # couplingparameters
        couplingparameters: List[CouplingParametersInterface] = self.get_CouplingParameters()

        # Get all occurences of the id
        id_occurrences: List[int] = [i for i in range(len(couplingparameters)) if isinstance(couplingparameters[i], SubSysCouplingParametersBasis) and couplingparameters[i].get_ID() == id]

        # If no occurence of the id in the ids of couplingparameters
        if len(id_occurrences) == 0:
            raise ValueError(f"{DDO_Color}There exists no neighboring subsystem with the ID {id}!{Reset}")

        # If there are more than one occurences of the id within couplingparameters
        if len(id_occurrences) > 1:
            raise ValueError(f"{DDO_Color}There are duplicate coupling parameters to the neighbor with ID {id}. Please make sure that each neighbor only has one coupling parameter!{Reset}")

        # Now, the only item in this list gives the index of the associated coupling parameter
        id_index: int = id_occurrences[0]

        # Get the associated coupling parameter
        couplingparameter: CouplingParametersInterface = couplingparameters[id_index]

        if isinstance(couplingparameter, SubSysCouplingParametersBasis):
            # No copy.copy() wrapper needed - setter creates its own defensive copy
            # store coupling variables (coupling-variable side)
            couplingparameter.set_CouplingVariable(couplingvariablein)
            couplingparameter.set_CouplingVariable_Unscaled(couplingvariablein_unscaled)

    def set_Copy_CouplingVariables(self, id: str, copycouplingvariablesin: List[float]) -> None:
        """Store a copy of the coupling variables from neighboring subsystems (scaled01 values).

        Args:
            id: Identifier of the subsystem from which the variables originate.
            copycouplingvariablesin: Copy of coupling variable values (scaled to [0, 1]).
        """

        # couplingparameters
        couplingparameters: List[CouplingParametersInterface] = self.get_CouplingParameters()

        # Get all occurences of the id
        id_occurrences: List[int] = [i for i in range(len(couplingparameters)) if isinstance(couplingparameters[i], SubSysCouplingParametersBasis) and couplingparameters[i].get_ID() == id]

        # If no occurence of the id in the ids of couplingparameters
        if len(id_occurrences) == 0:
            raise ValueError(f"{DDO_Color}There exists no neighboring subsystem with the ID {id}!{Reset}")

        # If there are more than one occurences of the id within couplingparameters
        if len(id_occurrences) > 1:
            raise ValueError(f"{DDO_Color}There are duplicate coupling parameters to the neighbor with ID {id}. Please make sure that each neighbor only has one coupling parameter!{Reset}")

        # Now, the only item in this list gives the index of the associated coupling parameter
        id_index: int = id_occurrences[0]

        # Get the associated coupling parameter
        couplingparameter: CouplingParametersInterface = couplingparameters[id_index]

        if isinstance(couplingparameter, SubSysCouplingParametersBasis):
            # No copy.copy() wrapper needed - setter creates its own defensive copy
            # store copy coupling variables (mapped-response side)
            couplingparameter.set_Copy_CouplingVariable(copycouplingvariablesin)

    def set_SharedDesignVariables(self, id: str, shareddesignvariablesin: List[float], shareddesignvariablesin_unscaled: List[float]) -> None:
        """Store the shared design variables for the neighboring subsystems (scaled01 values).

        Args:
            id: Identifier of the neighbor.
            shareddesignvariablesin: Shared design variable values (scaled to [0, 1]).
            shareddesignvariablesin_unscaled: Shared design variable values (unscaled).
        """

        # Check that scaled and unscaled lists have the same length
        if len(shareddesignvariablesin_unscaled) != len(shareddesignvariablesin):
            raise ValueError(f"{DDO_Color}Length mismatch: shareddesignvariablesin has {len(shareddesignvariablesin)} elements, but shareddesignvariablesin_unscaled has {len(shareddesignvariablesin_unscaled)} elements!{Reset}")

        # couplingparameters
        couplingparameters: List[CouplingParametersInterface] = self.get_CouplingParameters()

        # Get all occurences of the id
        id_occurrences: List[int] = [i for i in range(len(couplingparameters)) if isinstance(couplingparameters[i], SubSysCouplingParametersBasis) and couplingparameters[i].get_ID() == id]

        # If no occurence of the id in the ids of couplingparameters
        if len(id_occurrences) == 0:
            raise ValueError(f"{DDO_Color}There exists no neighboring subsystem with the ID {id}!{Reset}")

        # If there are more than one occurences of the id within couplingparameters
        if len(id_occurrences) > 1:
            raise ValueError(f"{DDO_Color}There are duplicate coupling parameters to the neighbor with ID {id}. Please make sure that each neighbor only has one coupling parameter!{Reset}")

        # Now, the only item in this list gives the index of the associated coupling parameter
        id_index: int = id_occurrences[0]

        # Get the associated coupling parameter
        couplingparameter: CouplingParametersInterface = couplingparameters[id_index]

        if isinstance(couplingparameter, SubSysCouplingParametersBasis):
            # No copy.copy() wrapper needed - setter creates its own defensive copy
            # store shared design variables
            couplingparameter.set_SharedDesignVariables(shareddesignvariablesin)
            couplingparameter.set_SharedDesignVariables_Unscaled(shareddesignvariablesin_unscaled)

    def set_Copy_SharedDesignVariables(self, id: str, copyshareddesignvariablesin: List[float]) -> None:
        """Store a copy of the shared design variables from neighboring subsystems (scaled01 values).

        Args:
            id: Identifier of the subsystem from which the variables originate.
            copyshareddesignvariablesin: Copy of shared design variable values (scaled to [0, 1]).
        """

        # couplingparameters
        couplingparameters: List[CouplingParametersInterface] = self.get_CouplingParameters()

        # Get all occurences of the id
        id_occurrences: List[int] = [i for i in range(len(couplingparameters)) if isinstance(couplingparameters[i], SubSysCouplingParametersBasis) and couplingparameters[i].get_ID() == id]

        # If no occurence of the id in the ids of couplingparameters
        if len(id_occurrences) == 0:
            raise ValueError(f"{DDO_Color}There exists no neighboring subsystem with the ID {id}!{Reset}")

        # If there are more than one occurences of the id within couplingparameters
        if len(id_occurrences) > 1:
            raise ValueError(f"{DDO_Color}There are duplicate coupling parameters to the neighbor with ID {id}. Please make sure that each neighbor only has one coupling parameter!{Reset}")

        # Now, the only item in this list gives the index of the associated coupling parameter
        id_index: int = id_occurrences[0]

        # Get the associated coupling parameter
        couplingparameter: CouplingParametersInterface = couplingparameters[id_index]

        if isinstance(couplingparameter, SubSysCouplingParametersBasis):
            # No copy.copy() wrapper needed - setter creates its own defensive copy
            # store copy shared design variables
            couplingparameter.set_Copy_SharedDesignVariables(copyshareddesignvariablesin)

    def set_TargetSharedDesignVariables(self, id: str, targetdesignvariablesin: List[float], targetdesignvariablesin_unscaled: List[float]) -> None:
        """Store the target shared design variables for the neighboring subsystems (scaled01 values).

        Args:
            id: Identifier of the neighbor.
            targetdesignvariablesin: Target design variable values (scaled to [0, 1]).
            targetdesignvariablesin_unscaled: Target design variable values (unscaled).
        """

        # Check that scaled and unscaled lists have the same length
        if len(targetdesignvariablesin_unscaled) != len(targetdesignvariablesin):
            raise ValueError(f"{DDO_Color}Length mismatch: targetdesignvariablesin has {len(targetdesignvariablesin)} elements, but targetdesignvariablesin_unscaled has {len(targetdesignvariablesin_unscaled)} elements!{Reset}")

        # couplingparameters
        couplingparameters: List[CouplingParametersInterface] = self.get_CouplingParameters()

        # Get all occurences of the id
        id_occurrences: List[int] = [i for i in range(len(couplingparameters)) if isinstance(couplingparameters[i], SubSysCouplingParametersBasis) and couplingparameters[i].get_ID() == id]

        # If no occurence of the id in the ids of couplingparameters
        if len(id_occurrences) == 0:
            raise ValueError(f"{DDO_Color}There exists no neighboring subsystem with the ID {id}!{Reset}")

        # If there are more than one occurences of the id within couplingparameters
        if len(id_occurrences) > 1:
            raise ValueError(f"{DDO_Color}There are duplicate coupling parameters to the neighbor with ID {id}. Please make sure that each neighbor only has one coupling parameter!{Reset}")

        # Now, the only item in this list gives the index of the associated coupling parameter
        id_index: int = id_occurrences[0]

        # Get the associated coupling parameter
        couplingparameter: CouplingParametersInterface = couplingparameters[id_index]

        if isinstance(couplingparameter, SubSysCouplingParametersBasis):
            # No copy.copy() wrapper needed - setter creates its own defensive copy
            # store target shared design variables
            couplingparameter.set_TargetSharedDesignVariables(targetdesignvariablesin)
            couplingparameter.set_TargetSharedDesignVariables_Unscaled(targetdesignvariablesin_unscaled)

    def set_Copy_TargetSharedDesignVariables(self, id: str, copytargetdesignvariablesin: List[float]) -> None:
        """Store a copy of the target design variables from neighboring subsystems (scaled01 values).

        Args:
            id: Identifier of the subsystem from which the variables originate.
            copytargetdesignvariablesin: Copy of target design variable values (scaled to [0, 1]).
        """

        # couplingparameters
        couplingparameters: List[CouplingParametersInterface] = self.get_CouplingParameters()

        # Get all occurences of the id
        id_occurrences: List[int] = [i for i in range(len(couplingparameters)) if isinstance(couplingparameters[i], SubSysCouplingParametersBasis) and couplingparameters[i].get_ID() == id]

        # If no occurence of the id in the ids of couplingparameters
        if len(id_occurrences) == 0:
            raise ValueError(f"{DDO_Color}There exists no neighboring subsystem with the ID {id}!{Reset}")

        # If there are more than one occurences of the id within couplingparameters
        if len(id_occurrences) > 1:
            raise ValueError(f"{DDO_Color}There are duplicate coupling parameters to the neighbor with ID {id}. Please make sure that each neighbor only has one coupling parameter!{Reset}")

        # Now, the only item in this list gives the index of the associated coupling parameter
        id_index: int = id_occurrences[0]

        # Get the associated coupling parameter
        couplingparameter: CouplingParametersInterface = couplingparameters[id_index]

        if isinstance(couplingparameter, SubSysCouplingParametersBasis):
            # No copy.copy() wrapper needed - setter creates its own defensive copy
            # store copy target shared design variables
            couplingparameter.set_Copy_TargetSharedDesignVariables(copy.copy(copytargetdesignvariablesin))

    def set_Indices_CouplingVariables_in_DesignVariables(self, id: str,
                                                         indices_couplingvariables_in_designvariables_in: List[int]) -> None:
        """Set the coupling variable indices within the design variables vector.

        Args:
            id: Identifier of the neighbor subsystem.
            indices_couplingvariables_in_designvariables_in: The indices to set.
        """

        # Get the coupling parameter corresponding to coupling with subsystem j
        couplingparameter_j: SubSysCouplingParametersBasis = self.get_CouplingParameter_with_ID(id)

        # Set the indices
        couplingparameter_j.set_Indices_CouplingVariables_In_DesignVariables(indices_couplingvariables_in_designvariables_in)


    def set_Indices_SharedDesignVariables_in_DesignVariables(self, id: str,
                                                             indices_shareddesignvariables_in_designvariables_in: List[int]) -> None:
        """Set the shared design variable indices within the design variables vector.

        Args:
            id: Identifier of the neighbor subsystem.
            indices_shareddesignvariables_in_designvariables_in: The indices to set.
        """

        # Get the coupling parameter corresponding to coupling with subsystem j
        couplingparameter_j: SubSysCouplingParametersBasis = self.get_CouplingParameter_with_ID(id)

        # Set the indices
        couplingparameter_j.set_Indices_SharedDesignVariables_In_DesignVariables(indices_shareddesignvariables_in_designvariables_in)


    def set_Indices_TargetSharedDesignVariables_in_DesignVariables(self, id: str,
                                                                   indices_targetshareddesignvariables_in_designvariables_in: List[int]) -> None:
        """Set the target shared design variable indices within the design variables vector.

        Args:
            id: Identifier of the neighbor subsystem.
            indices_targetshareddesignvariables_in_designvariables_in: The indices to set.
        """

        # Get the coupling parameter corresponding to coupling with subsystem j
        couplingparameter_j: SubSysCouplingParametersBasis = self.get_CouplingParameter_with_ID(id)

        # Set the indices
        couplingparameter_j.set_Indices_TargetSharedDesignVariables_In_DesignVariables(indices_targetshareddesignvariables_in_designvariables_in)



########################################################################################################################
#   Functions to handle coordination parameters
########################################################################################################################

    def run_updateCouplingParameters_outerLoop_job(self) -> None:
        """Update coupling parameters in the outer loop, including inconsistency evaluation."""
        self.set_DesignVariables(self.get_OptimData().get_DesignVariables())
        self.evaluateTotalObjective()
        self.evaluateTotalConstraint()
        self.CopyFromMiddleLevel()
        self.evaluate_Inconsistencies()
        self.updateCouplingParameters_outerLoop()
        self.CopyToMiddleLevel()

    def run_prepare_updateCouplingParameters_job(self) -> None:
        """Prepare coupling parameters update after inner loop, including inconsistency evaluation."""
        self.set_DesignVariables(self.get_OptimData().get_DesignVariables())
        self.evaluateTotalObjective()
        self.evaluateTotalConstraint()
        self.CopyFromMiddleLevel()
        self.evaluate_Inconsistencies()
        self.prepare_updateCouplingParameters()
        self.CopyToMiddleLevel()

    def evaluate_Inconsistencies(self) -> None:
        """Compute the difference between stored coupling and mapped variables compared to the latest available data.

        It returns a matrix containing fourvectors. The first row vector are the mapped-response side differences of
        the coupling circle. The second row vector returns differences of the coupling-variable side of the coupling circle.
        The third and fourth rows return the difference between the shared design variable vector.

        This method does not evaluate consensus inconsistencies;
        Current variant: This has to be specified in each LocalSubSystemBasis
        subclass, e.g. consensus ALC, after calling super().evaluate_Inconsistencies.
        """
        couplingsubsystems: List[CouplingParametersInterface] = self.get_CouplingParameters()

        for i in range(len(couplingsubsystems)):
            # Get the coupling parameter
            couplingsubsystem: CouplingParametersInterface = couplingsubsystems[i]

            # Only compute for local subsystems
            if isinstance(couplingsubsystem, SubSysCouplingParametersBasis):
                # Use the local copy-attributes (populated by CopyFromMiddleLevel)
                # instead of accessing the shared middle-level storage directly.
                # This avoids race conditions on the shared resource.

                # compute the inconsistencysizes
                if ((couplingsubsystem.get_CouplingVariable() is not None) and \
                        (couplingsubsystem.get_Copy_MappedResponses() is not None)):

                    couplingvariable: List[float] = couplingsubsystem.get_CouplingVariable()
                    copymappedresponse: List[float] = couplingsubsystem.get_Copy_MappedResponses()

                    self._inconsistencies[i].evaluate_CopyMappedResponse_Minus_CouplingVariable(couplingvariable=couplingvariable, copymappedresponse=copymappedresponse)

                if ((couplingsubsystem.get_MappedResponses() is not None) and \
                        (couplingsubsystem.get_Copy_CouplingVariable() is not None)):

                    mappedresponse: List[float] = couplingsubsystem.get_MappedResponses()
                    copycouplingvariable: List[float] = couplingsubsystem.get_Copy_CouplingVariable()

                    self._inconsistencies[i].evaluate_MappedResponse_Minus_CopyCouplingVariable(copycouplingvariable=copycouplingvariable, mappedresponse=mappedresponse)

                if ((couplingsubsystem.get_SharedDesignVariables() is not None) and \
                        (couplingsubsystem.get_Copy_TargetSharedDesignVariables() is not None)):

                    shareddesignvariable: List[float] = couplingsubsystem.get_SharedDesignVariables()
                    copytargetshareddesignvariable: List[float] = couplingsubsystem.get_Copy_TargetSharedDesignVariables()

                    self._inconsistencies[i].evaluate_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(copytargetshareddesignvariable=copytargetshareddesignvariable, shareddesignvariable=shareddesignvariable)

                if ((couplingsubsystem.get_TargetSharedDesignVariables() is not None) and \
                        (couplingsubsystem.get_Copy_SharedDesignVariables() is not None)):

                    targetshareddesignvariable: List[float] = couplingsubsystem.get_TargetSharedDesignVariables()
                    copyshareddesignvariable: List[float] = couplingsubsystem.get_Copy_SharedDesignVariables()

                    self._inconsistencies[i].evaluate_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(targetshareddesignvariable=targetshareddesignvariable, copyshareddesignvariable=copyshareddesignvariable)

                self._inconsistencies[i].evaluate_MaxInconsistency()

        self.evaluate_MaxInconsistency()

    def appendtohistory(self) -> None:
        """Append the current subsystem state to the history, including inconsistency data."""
        self._subsystemhistory.append(LocalSubSystemHistoryEntry(subsystem_id=self.get_SUBSYSTEMID(),
                                                                 outerloop_itr=self.get_OuterLoop_Itr(),
                                                                 innerloop_itr=self.get_InnerLoop_Itr(),
                                                                 innerloop_itr_runtime=self.get_InnerLoop_Itr_Runtime(),
                                                                 innerloop_itr_numberofdesignvariableevaluations=self.get_InnerLoop_Itr_NumberOfDesignVariableEvaluations(),
                                                                 optimdata=copy.deepcopy(self.get_OptimData()),
                                                                 convinnerloop=self.get_ConvInnerLoop(),
                                                                 convouterloop=self.get_ConvOuterLoop(),
                                                                 scalers=copy.deepcopy(self.get_Scalers()),
                                                                 inconsistencies=copy.deepcopy(self.get_Inconsistencies()),
                                                                 maxinconsistencyvalue=self.get_maxInconsistencyValue(),
                                                                 maxinconsistencysubsystemID=self.get_MaxInconsistencyCoupledSubsystemID()
                                                                 ))

########################################################################################################################
#   Functions to obtain past inconsistency values from self._subsystemhistory
########################################################################################################################

    # NOTE: In subclass, extend methods to get other data from self._subsystemhistory if needed

    def copy_Inconsistencies_at_Iteration(self, outerloop_itr: int, innerloop_itr: int) -> List[InConsistencySizeInterface]:
        """Copy the inconsistencies of the specified iteration at number (outerloop_itr, innerloop_itr).

        Args:
            outerloop_itr (int): outer loop iteration number
            innerloop_itr (int): inner loop iteration number

        Returns:
            The inconsistencies at the specified iteration, or initialized inconsistencies if not found.
        """
        # Boolean value to indicate if the iteration number was found
        found_result = False
        # Search the self._subsystemhistory backwards
        for i in range(len(self._subsystemhistory) - 1, -1, -1):
            if self._subsystemhistory[i].get_OuterLoop_Itr() == self._outerloop_itr and self._subsystemhistory[i].get_InnerLoop_Itr() == self._innerloop_itr:
                # copy.deepcopy() intentional - protects self._subsystemhistory from modification by callers.
                # The history is a shared record; callers must not alter past iteration data.
                result = copy.deepcopy(self._subsystemhistory[i].get_Inconsistencies())
                found_result = True
                break
        if not found_result:
            # There exist no List of Inconsistencies with fitting (self._outerloop_itr, self._innerloop_itr), so just return a List of initialized inconsistencies
            # result: List[InConsistencySizeInterface] = CreateInConsistencies_and_Measure.createInConsistencies_and_Measure(self._subsystem)[0]
            result = self.return_initialized_Inconsistencies()

        return result

    def copy_Inconsistencies_Past_outerloop_itr(self, outerloop_itr_before: int) -> List[InConsistencySizeInterface]:
        """Copy the inconsistencies from the self._outerloop_itr-th previous outer iteration.

        Args:
            outerloop_itr_before: The number of outer loop iterations to go to the history
            self._outerloop_itr (int): The current outer loop iteration number

        Returns:
            The inconsistencies from the specified past iteration, or initialized inconsistencies if not found.
        """

        previous_itr = self._outerloop_itr - outerloop_itr_before
        found_result = False
        # Search the self._subsystemhistory backwards
        for i in range(len(self._subsystemhistory) - 1, -1, -1):
            if self._subsystemhistory[i].get_OuterLoop_Itr() == previous_itr:
                # copy.deepcopy() intentional - protects self._subsystemhistory from modification by callers.
                # The history is a shared record; callers must not alter past iteration data.
                result = copy.deepcopy(self._subsystemhistory[i].get_Inconsistencies())
                found_result = True
                break
        if not found_result:
            # There exist no List of Inconsistencies with fitting self._outerloop_itr, so just return a List of initialized inconsistencies
            # result: List[InConsistencySizeInterface] = CreateInConsistencies_and_Measure.createInConsistencies_and_Measure(self._subsystem)[0]
            result = self.return_initialized_Inconsistencies()

        return result

    def copy_Inconsistencies_Previous_outerloop_itr(self) -> List[InConsistencySizeInterface]:
        """Copy the inconsistencies from the previous outer loop iteration.

        Returns:
            The inconsistencies from the previous outer loop iteration.
        """
        return self.copy_Inconsistencies_Past_outerloop_itr(outerloop_itr_before=1)

    def copy_Inconsistencies_Previous_Previous_outerloop_itr(self) -> List[InConsistencySizeInterface]:
        """Copy the inconsistencies from the previous previous outer loop iteration.

        Returns:
            The inconsistencies from two outer loop iterations ago.
        """
        return self.copy_Inconsistencies_Past_outerloop_itr(outerloop_itr_before=2)

########################################################################################################################
#   Functions necessary for Analysis of Coordination Methods
########################################################################################################################

    def get_Ignore_CouplingId_for_CoordinationObjective(self) -> str | None:
        """Get the coupling IDs to ignore for the coordination objective.

        Returns:
            The coupling ID to ignore, or None if all couplings are considered.
        """
        # No copy.copy() needed - str is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._ignore_couplingid_for_coordinationobjective

    def set_Ignore_CouplingId_for_CoordinationObjective(self, id: str | None) -> None:
        """Set the coupling ID to ignore for coordination objective calculation.

        Args:
            id: Coupling ID to ignore, or None to consider all couplings.
        """
        # No copy.copy() needed - str is a primitive/immutable type.
        self._ignore_couplingid_for_coordinationobjective = id

########################################################################################################################
#   Compute local KKT multipliers
########################################################################################################################

    def compute_KKT_system_matrix_and_bounds(self) -> List[List[List[float]] | List[Tuple[float | None, float | None]]]:
        """Return the total linear KKT system matrix.

        Returns:
            A list containing the constraint matrix and bounds for the KKT system.
        """

        # Define the constraint equality matrix
        # Form: ( local eq. | coordination eq. | local ineq. | coordination ineq. | lower bounds | upper bounds)
        constraint_matrix = []
        bounds: List[List[float] | None] = []

        # Get the dimension of each component Jacobian / gradient
        primal_dimension: int = len(self.get_DesignVariables())

        # Local equality constraints

        # If local equality constraints exist
        if self.get_EqualityLocalConstraintsValue() is not None:

            # Get the Jacobian of the local equality constraints
            jacobian_localequalityconstraints: List[List[float]] = self._optimdata.get_Jacobian_LocalEqualityConstraints()

            # Append the component Jacobians of the local equality constraints rowwise
            for component_jacobian in jacobian_localequalityconstraints:

                # Append the specific row
                constraint_matrix.append(component_jacobian)

                # Indicate no bound for dual multiplier w.r.t
                # this specific local equality constraint
                bounds.append((None, None))

        # If coordination equality constraints exist
        if self.get_CoordinationEqualityConstraintValue() is not None and self._optimdata.get_Jacobian_CoordinationEqualityConstraints() is not None:

            # Get the Jacobian of the coordination equality constraints
            jacobian_coordinationequalityconstraints: List[List[float]] = self._optimdata.get_Jacobian_CoordinationEqualityConstraints()

            # Append the Jacobian w.r.t the coordination equality constraint rowwise
            for component_jacobian in jacobian_coordinationequalityconstraints:

                # Append the specific row
                constraint_matrix.append(component_jacobian)

                # Indicate no bound for dual multiplier w.r.t
                # this specific coordination equality constraint
                bounds.append((None, None))

        # If local inequality constraints exist

        if self.get_InequalityLocalConstraintsValue() is not None:

            # Get the Jacobian and indicators of the (active) local inequality constraints
            jacobian_activelocalinequalityconstraints: List[List[float | None]] = self._optimdata.get_Jacobian_LocalInequalityConstraints()
            activelocalinequalityconstraints: List[bool] = self._optimdata.get_ActiveLocalInequalityConstraints()

            # Iterate over the Jacobians of each component function
            for i in range(len(jacobian_activelocalinequalityconstraints)):

                # Choose the corresponding component gradient as zero
                component_jacobian: List[float] = [0.0] * primal_dimension

                # Check if the constraint is inactive
                if activelocalinequalityconstraints[i] is not True:

                    # Do not change the component Jacobian from the zeros vector

                    # Indicate no bound for dual multiplier w.r.t.
                    # inactive local inequality constraints, since they
                    # have no impact in KKT system
                    bounds.append((None, None))

                # Active local inequality constraint
                else:

                    # Initialize the component gradient
                    component_jacobian: List[float] = jacobian_activelocalinequalityconstraints[i]

                    # Indicate nonnegativity bound for dual multiplier
                    # w.r.t. active local inequality constraints
                    bounds.append((0.0, None))

                # Add the component Jacobian
                constraint_matrix.append(component_jacobian)

        # If coordination inequality constraints exist
        if self.get_CoordinationInequalityConstraintValue() is not None:

            # Get the Jacobian and indicators of the (active) coordination inequality constraints
            jacobian_activecoordinationinequalityconstraints: List[List[float | None]] = self._optimdata.get_Jacobian_CoordinationInequalityConstraints()
            activecoordinationinequalityconstraints: List[bool] = self._optimdata.get_ActiveCoordinationInequalityConstraints()

            # Iterate over the Jacobians of each component function
            for i in range(len(jacobian_activecoordinationinequalityconstraints)):

                # Choose the corresponding component gradient as zero
                component_jacobian: List[float] = [0.0] * primal_dimension

                # Check if the constraint is inactive
                if activecoordinationinequalityconstraints[i] is not True:

                    # Do not change the component Jacobian from the zeros vector

                    # Indicate no bound for dual multiplier w.r.t.
                    # inactive coordination inequality constraints, since they
                    # have no impact in KKT system
                    bounds.append((None, None))

                # Active coordination inequality constraint
                else:

                    # Initialize the component gradient
                    component_jacobian: List[float] = jacobian_activecoordinationinequalityconstraints[i]

                    # Indicate nonnegativity bound for dual multiplier
                    # w.r.t. active coordination inequality constraints
                    bounds.append((0.0, None))

                # Add the component Jacobian
                constraint_matrix.append(component_jacobian)

        # For lower bounds

        # Get the Jacobian and indicators of the (active) lower bounds
        jacobian_activelowerbounds: List[List[float | None]] = self._optimdata.get_Jacobian_LowerBounds()
        activelowerbounds: List[bool] = self._optimdata.get_ActiveLowerBounds()

        # Iterate over the Jacobians of each component function
        for i in range(len(jacobian_activelowerbounds)):

            # Initialize the component gradient
            component_jacobian: List[float] = [0.0] * primal_dimension

            # Check if the constraint is inactive
            if activelowerbounds[i] is not True:

                # Do not change the Jacobian from the zeros vector,
                # since the bound is inactive

                # Indicate no bound for dual multiplier w.r.t.
                # inactive lower bound constraints, since they
                # have no impact in KKT system
                bounds.append((None, None))

            # Active lower bound constraint
            else:

                # Set the Jacobian approximation
                component_jacobian = jacobian_activelowerbounds[i]

                # Indicate nonnegativity bound for dual multiplier
                # w.r.t. active lower bound constraints
                bounds.append((0.0, None))

            # Add the component Jacobian
            constraint_matrix.append(component_jacobian)


        # For upper bounds

        # Get the Jacobian and indicators of the (active) upper bounds
        jacobian_activeupperbounds: List[List[float | None]] = self._optimdata.get_Jacobian_UpperBounds()
        activeupperbounds: List[bool] = self._optimdata.get_ActiveUpperBounds()

        # Iterate over the Jacobians of each component function
        for i in range(len(jacobian_activeupperbounds)):

            # Initialize the component gradient
            component_jacobian: List[float] = [0.0] * primal_dimension

            # Check if the constraint is inactive
            if activeupperbounds[i] is not True:

                # Do not change the Jacobian from the zeros vector,
                # since the bound is inactive

                # Indicate no bound for dual multiplier w.r.t.
                # inactive upper bound constraints, since they
                # have no impact in KKT system
                bounds.append((None, None))

            # Active upper bound constraint
            else:

                # Set the Jacobian approximation
                component_jacobian = jacobian_activeupperbounds[i]

                # Indicate nonnegativity bound for dual multiplier
                # w.r.t. active upper bound constraints
                bounds.append((0.0, None))

            # Add the component Jacobian
            constraint_matrix.append(component_jacobian)

        # Return the KKT system matrix
        return [constraint_matrix, bounds]

    def decompose_KKT_multipliers(self, all_multipliers: List[float]) -> None:
        """Decompose the solution of the KKT system and store the parts into self._optimdata.

        Decomposes the multipliers stored in optimization_result into different
        parts (e.g. local inequality constraints) and stores them
        into self._optimdata.

        Args:
            all_multipliers: Total accumulation of all multipliers (only for constraints, not for objective)
        """

        # Form of all_multipliers by definition:
        # ( local eq. | coordination eq. | local ineq. | coordination ineq. | lower bounds | upper bounds)

        # Define a pointer for the indices of all_multipliers
        index_pointer: int = 0

        # Local equality constraint

        # If local equality constraints exist
        if self.get_EqualityLocalConstraintsValue() is not None:

            # Get the number of local equality constraints
            number_localequalityconstraints: int = len(self.get_EqualityLocalConstraintsValue())

            # Store the corresponding multipliers
            self._optimdata.set_Multipliers_Local_Equality_Constraints(all_multipliers[index_pointer:index_pointer + number_localequalityconstraints])

            # Update the index pointer
            index_pointer += number_localequalityconstraints

        # Coordination equality constraint

        # If coordination equality constraints exist
        if self.get_CoordinationEqualityConstraintValue() is not None:

            # Get the number of coordination equality constraints
            number_coordinationequalityconstraints: int = len(self.get_CoordinationEqualityConstraintValue())

            # Store the corresponding multipliers
            self._optimdata.set_Multipliers_Coordination_Equality_Constraints(all_multipliers[index_pointer:index_pointer + number_coordinationequalityconstraints])

            # Update the index pointer
            index_pointer += number_coordinationequalityconstraints

        # Local inequality constraint

        # If local inequality constraints exist
        if self.get_InequalityLocalConstraintsValue() is not None:

            # Get the (active) lower bounds
            activelocalinequalityconstraints: List[bool] = self._optimdata.get_ActiveLocalInequalityConstraints()
            multipliers_localinequalityconstraints: List[float | None] = []

            # Iterate over the Jacobians of each component function
            for i in range(len(activelocalinequalityconstraints)):

                # Check if the constraint is inactive
                if activelocalinequalityconstraints[i] is False:

                    # Append a None field, since constraint is inactive
                    multipliers_localinequalityconstraints.append(None)

                # Active lower bound constraint
                else:

                    # Add the component Jacobian
                    multipliers_localinequalityconstraints.append(all_multipliers[index_pointer])

                # Move the index pointer to next component
                index_pointer += 1

            # Set the multiplier of the local inequality constraints
            self._optimdata.set_Multipliers_Local_Inequality_Constraints(multipliers_localinequalityconstraints)

        # Coordination inequality constraint

        # If coordination inequality constraints exist
        if self.get_CoordinationInequalityConstraintValue() is not None:

            # Get the (active) coordination inequality constraints
            activecoordinationinequalityconstraints: List[bool] = self._optimdata.get_ActiveCoordinationInequalityConstraints()
            multipliers_coordinationinequalityconstraints: List[float] = []

            # Iterate over each coordination inequality constraint
            for i in range(len(activecoordinationinequalityconstraints)):

                # Check if the constraint is inactive
                if activecoordinationinequalityconstraints[i] is False:

                    # Append a None field, since constraint is inactive
                    multipliers_coordinationinequalityconstraints.append(None)

                # Active coordination inequality constraint
                else:

                    # Add the corresponding multiplier
                    multipliers_coordinationinequalityconstraints.append(all_multipliers[index_pointer])

                # Move the index pointer to next component
                index_pointer += 1

            # Set the multiplier of the coordination inequality constraints
            self._optimdata.set_Multipliers_Coordination_Inequality_Constraints(multipliers_coordinationinequalityconstraints)

        # Lower bounds, upper bounds

        # For lower bounds

        # Get the (active) lower bounds
        activelowerbounds: List[bool] = self._optimdata.get_ActiveLowerBounds()
        multipliers_lowerbounds: List[float] = []

        # Iterate over the Jacobians of each component function
        for i in range(len(activelowerbounds)):

            # Check if the constraint is inactive
            if activelowerbounds[i] is False:

                # Append a None field, since constraint is inactive
                multipliers_lowerbounds.append(None)

            # Active lower bound constraint
            else:

                # Add the component Jacobian
                multipliers_lowerbounds.append(all_multipliers[index_pointer])

            # Move the index pointer to next component
            index_pointer += 1

        # Set the multiplier of the lower bounds
        self._optimdata.set_Multipliers_LowerBounds(multipliers_lowerbounds)

        # For upper bounds

        # Get the Jacobian and indicators of the (active) upper bounds
        activeupperbounds: List[bool] = self._optimdata.get_ActiveUpperBounds()
        multipliers_upperbounds: List[float] = []

        # Iterate over the Jacobians of each component function
        for i in range(len(activeupperbounds)):

            # Check if the constraint is inactive
            if activeupperbounds[i] is False:

                # Append a None field, since constraint is inactive
                multipliers_upperbounds.append(None)

            # Active upper bound constraint
            else:

                # Add the component Jacobian
                multipliers_upperbounds.append(all_multipliers[index_pointer])

            # Move the index pointer to next component
            index_pointer += 1

        # Set the multiplier of the upper bounds
        self._optimdata.set_Multipliers_UpperBounds(multipliers_upperbounds)

    ################################################################################################

    def compute_Jacobian_MappedResponse_Wrt_DesignVariables(self) -> None:
        """Compute the Jacobian of mapped responses with respect to design variables."""
        self._jacobiancomputer.execute(self)

    def set_Jacobian_MappedResponse_Wrt_DesignVariables_Value(self, jacobinain: List[List[List[float]] | None]) -> None:
        """Set the Jacobian matrix of mapped response variables with respect to design variables.

        Args:
            jacobinain: Jacobian matrix for each coupling.
        """
        # copy.deepcopy() used - List[List[List[float]] | None] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_mappedresponse_wrt_designvariables_value = copy.deepcopy(jacobinain)

    def get_Jacobian_MappedResponse_Wrt_DesignVariables_Value(self) -> List[List[List[float]] | None] | None:
        """Return the Jacobian matrix of mapped response variables with respect to design variables.

        Returns:
            Jacobian matrix for each coupling, or None if not computed.
        """
        # copy.deepcopy() used - List[List[List[float]] | None] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_mappedresponse_wrt_designvariables_value)

########################################################################################################################
#   Print methods for terminal output
########################################################################################################################

    def _print_inconsistencies(self, termination: bool = False) -> None:
        """Print inconsistencies for all coupled subsystems."""
        ddo_print("       Inconsistencies:")
        inconsistencies = self.get_Inconsistencies()
        if inconsistencies is not None:
            for inconsistency in inconsistencies:
                if termination:
                    inconsistency.print_termination_summary()
                else:
                    inconsistency.print_end_of_innerloop_iteration()

    def _print_distance_to_reference(self) -> None:
        """Print distance from reference local objective value if reference is set."""
        ref = self.get_ReferenceLocalObjectiveValueUnscaled()
        if ref is not None:
            current = self.get_LocalObjectiveValue_Unscaled()
            if current is not None:
                distance = ref - current
                ddo_print(f"       {'Dist. from Ref. Local Obj.:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {distance}")
            else:
                ddo_print(f"       {'Dist. from Ref. Local Obj.:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} N/A")

    def get_scaler_bound_violations(self) -> List[Tuple[int, str]]:
        """Collect scaler bound violations for this subsystem.

        Returns:
            List of (scaler_index, warning_message) tuples.
        """
        violations = []
        scalers = self.get_Scalers()
        if scalers is not None:
            for idx, scaler in enumerate(scalers):
                if scaler is not None and hasattr(scaler, 'get_bound_violation_warnings'):
                    for warning_msg in scaler.get_bound_violation_warnings():
                        violations.append((idx, warning_msg))
        return violations

    def print_scaler_bound_violations(self) -> None:
        """Print any scaler bound violations for this subsystem."""
        for idx, warning_msg in self.get_scaler_bound_violations():
            ddo_print(f"WARNING: Subsystem '{self.get_SUBSYSTEMID()}', Scaler index {idx}:", indent=1)
            ddo_print(warning_msg, indent=2)

    def print_scaler_bound_utilization_report(self) -> None:
        """Print a compact scaler bound utilization report for this subsystem."""
        scalers = self.get_Scalers()
        if scalers is None:
            return
        any_violations = False
        any_conservative = False
        ddo_print(f"   Subsystem '{self.get_SUBSYSTEMID()}':")
        for idx, scaler in enumerate(scalers):
            if scaler is not None and hasattr(scaler, 'get_bound_utilization_report'):
                line, violated, conservative = scaler.get_bound_utilization_report()
                any_violations = any_violations or violated
                any_conservative = any_conservative or conservative
                ddo_print(f"      [{idx}] {line}")
        if any_violations:
            ddo_print(f"      ! Violated bounds detected. Need to adapt scaler bounds in InputFile and re-run optimization.")
        if any_conservative:
            ddo_print(f"      * Too conservative bounds. Consider tightening scaler bounds in InputFile and re-run optimization.")

    def print_startup_summary(self) -> None:
        """Print local subsystem info at startup."""
        bounds = self.get_LowerBounds_Unscaled()
        dv_dim = len(bounds) if bounds is not None else 0
        ddo_print(f"   SubSystem {self.get_SUBSYSTEMID()} (Level {self.get_SubsystemLevel()}, {dv_dim} design variables)")

    def print_end_of_innerloop_iteration(self) -> None:
        """Print local subsystem results at the end of an inner loop iteration."""
        self._print_subsystem_header()
        self.get_OptimData().print_results()
        self._print_distance_to_reference()
        self._print_inconsistencies(termination=False)
        ddo_print("")

    def print_termination_summary(self) -> None:
        """Print local subsystem results at the end of the optimization run."""
        self._print_subsystem_header()
        self.get_OptimData().print_results()
        self._print_distance_to_reference()
        self._print_inconsistencies(termination=True)
        ddo_print("")

########################################################################################################################
#   Update State Function necessary for running multiprocessing
########################################################################################################################
    def update_state(self, other_subsystem: 'LocalSubSystemBasis') -> None:
        """Update the state of this LocalSubSystemBasis instance with values from another instance.

        This method is necessary for multiprocessing. When subsystems are executed in parallel
        using multiprocessing.Pool, they are serialized and deserialized, creating new objects
        in separate memory spaces. After parallel execution completes, this method updates
        the original object's attribute values while preserving their memory addresses.

        The update preserves memory addresses by modifying attribute contents in-place where
        possible, rather than reassigning references. This is essential for maintaining object
        identity across the multiprocessing boundary.

        Args:
            other_subsystem: The source LocalSubSystemBasis containing updated values
                from parallel execution.
        """
        # Update attributes inherited from SubSystemBasis
        super().update_state(other_subsystem=other_subsystem)

        # Update LocalSubSystemBasis-specific attributes (in __init__ order)

        # 1. _SubsystemLevel: int
        # No copy.copy() needed - int is a primitive/immutable type
        self._SubsystemLevel: int = other_subsystem.get_SubsystemLevel()

        # 2. _optimization: OptimizationInterface
        # No update needed - serves as a strategy object whose state is not changed

        # 3. _optimdata: LocalSubSystemOptimData
        # Handled by parent class (SubSystemBasis) with copy.deepcopy

        # 4. _couplingparameters: List[SubSysCouplingParametersBasis]
        # Handled by parent class (SubSystemBasis) via in-place update_state calls

        # 5. _inconsistencies: List[InConsistencySizeInterface]
        # Update each inconsistency object in-place to preserve memory addresses
        other_inconsistencies: List[InConsistencySizeInterface] = other_subsystem.get_Inconsistencies()
        for i in range(len(other_inconsistencies)):
            self._inconsistencies[i].update_state(other_inconsistencies[i])

        # 6. _maxinconsistencyvalue: float | None
        # No copy.copy() needed - float is a primitive/immutable type
        self._maxinconsistencyvalue: float | None = other_subsystem.get_maxInconsistencyValue()

        # 7. _maxinconsistencycoupledsubsystemID: str | None
        # No copy.copy() needed - str is a primitive/immutable type
        self._maxinconsistencycoupledsubsystemID: str | None = other_subsystem.get_MaxInconsistencyCoupledSubsystemID()

        # 8. _analysis: AnalysisInterface
        # No update needed - serves as a strategy object whose state is not changed

        # 9. _jacobiancomputer: JacobianComputer
        # No update needed - serves as a strategy object whose state is not changed

        # 10. _finite_differences_jacobian: FiniteDifferencesJacobian
        # Update via its own update_state method
        self._finite_differences_jacobian.update_state(other_subsystem.get_Finite_Differences_Jacobian())

        # 11. _localobjective: LocalObjectiveInterface
        # No update needed - serves as a strategy object whose state is not changed

        # 12. _localconstraints: LocalConstraintsInterface
        # No update needed - serves as a strategy object whose state is not changed

        # 13. _referencedesignvariables: List[float] | None
        self._referencedesignvariables: List[float] | None = update_state_listprimitive(self._referencedesignvariables, other_subsystem.get_ReferenceDesignVariables())

        # 14. _referencedesignvariables_unscaled: List[float] | None
        self._referencedesignvariables_unscaled: List[float] | None = update_state_listprimitive(self._referencedesignvariables_unscaled, other_subsystem.get_ReferenceDesignVariables_Unscaled())

        # 15. _referencelocalobjectivevalue: float | None
        # No copy.copy() needed - float is a primitive/immutable type
        self._referencelocalobjectivevalue: float | None = other_subsystem.get_ReferenceLocalObjectiveValue()

        # 16. _referencelocalobjectivevalueunscaled: float | None
        # No copy.copy() needed - float is a primitive/immutable type
        self._referencelocalobjectivevalueunscaled: float | None = other_subsystem.get_ReferenceLocalObjectiveValueUnscaled()

        # 17. _responses_unscaled: List[float] | None
        self._responses_unscaled: List[float] | None = update_state_listprimitive(self._responses_unscaled, other_subsystem.get_Responses_Unscaled())

        # 18. _jacobian_mappedresponse_wrt_designvariables_value: List[List[List[float]] | None] | None
        # Update nested structure in-place to preserve memory addresses
        other_jacobian: List[List[List[float]] | None] | None = other_subsystem.get_Jacobian_MappedResponse_Wrt_DesignVariables_Value()
        if other_jacobian is None:
            self._jacobian_mappedresponse_wrt_designvariables_value: List[List[List[float]] | None] | None = None
        elif self._jacobian_mappedresponse_wrt_designvariables_value is None:
            # No copy.deepcopy() needed - getter already returns a deep copy
            self._jacobian_mappedresponse_wrt_designvariables_value = other_jacobian
        else:
            for i in range(len(other_jacobian)):
                if other_jacobian[i] is None:
                    self._jacobian_mappedresponse_wrt_designvariables_value[i] = None
                elif self._jacobian_mappedresponse_wrt_designvariables_value[i] is None:
                    self._jacobian_mappedresponse_wrt_designvariables_value[i] = other_jacobian[i]
                else:
                    for j in range(len(other_jacobian[i])):
                        self._jacobian_mappedresponse_wrt_designvariables_value[i][j] = update_state_listprimitive(self._jacobian_mappedresponse_wrt_designvariables_value[i][j], other_jacobian[i][j])

        # 19. _localobjectivevalue: float | None
        # No copy.copy() needed - float is a primitive/immutable type
        self._localobjectivevalue: float | None = other_subsystem.get_LocalObjectiveValue()

        # 20. _localobjectivevalue_unscaled: float | None
        # No copy.copy() needed - float is a primitive/immutable type
        self._localobjectivevalue_unscaled: float | None = other_subsystem.get_LocalObjectiveValue_Unscaled()

        # 21. _equalitylocalconstraintsvalue: List[float] | None
        self._equalitylocalconstraintsvalue: List[float] | None = update_state_listprimitive(self._equalitylocalconstraintsvalue, other_subsystem.get_EqualityLocalConstraintsValue())

        # 22. _equalitylocalconstraintsvalue_unscaled: List[float] | None
        self._equalitylocalconstraintsvalue_unscaled: List[float] | None = update_state_listprimitive(self._equalitylocalconstraintsvalue_unscaled, other_subsystem.get_EqualityLocalConstraintsValue_Unscaled())

        # 23. _inequalitylocalconstraintsvalue: List[float] | None
        self._inequalitylocalconstraintsvalue: List[float] | None = update_state_listprimitive(self._inequalitylocalconstraintsvalue, other_subsystem.get_InequalityLocalConstraintsValue())

        # 24. _inequalitylocalconstraintsvalue_unscaled: List[float] | None
        self._inequalitylocalconstraintsvalue_unscaled: List[float] | None = update_state_listprimitive(self._inequalitylocalconstraintsvalue_unscaled, other_subsystem.get_InequalityLocalConstraintsValue_Unscaled())

        # 25. _ignore_couplingid_for_coordinationobjective: str | None
        # No copy.copy() needed - str is a primitive/immutable type
        self._ignore_couplingid_for_coordinationobjective: str | None = other_subsystem.get_Ignore_CouplingId_for_CoordinationObjective()

        # 26. _localobjectivevalue_lower_scaler_bound_warning_raised: bool
        # No copy.copy() needed - bool is a primitive/immutable type
        self._localobjectivevalue_lower_scaler_bound_warning_raised: bool = other_subsystem._localobjectivevalue_lower_scaler_bound_warning_raised

        # 27. _localobjectivevalue_upper_scaler_bound_warning_raised: bool
        # No copy.copy() needed - bool is a primitive/immutable type
        self._localobjectivevalue_upper_scaler_bound_warning_raised: bool = other_subsystem._localobjectivevalue_upper_scaler_bound_warning_raised

        # 28. _equalitylocalconstraintsvalue_lower_scaler_bound_warning_raised: bool
        # No copy.copy() needed - bool is a primitive/immutable type
        self._equalitylocalconstraintsvalue_lower_scaler_bound_warning_raised: bool = other_subsystem._equalitylocalconstraintsvalue_lower_scaler_bound_warning_raised

        # 29. _equalitylocalconstraintsvalue_upper_scaler_bound_warning_raised: bool
        # No copy.copy() needed - bool is a primitive/immutable type
        self._equalitylocalconstraintsvalue_upper_scaler_bound_warning_raised: bool = other_subsystem._equalitylocalconstraintsvalue_upper_scaler_bound_warning_raised

        # 30. _inequalitylocalconstraintsvalue_lower_scaler_bound_warning_raised: bool
        # No copy.copy() needed - bool is a primitive/immutable type
        self._inequalitylocalconstraintsvalue_lower_scaler_bound_warning_raised: bool = other_subsystem._inequalitylocalconstraintsvalue_lower_scaler_bound_warning_raised

        # 31. _inequalitylocalconstraintsvalue_upper_scaler_bound_warning_raised: bool
        # No copy.copy() needed - bool is a primitive/immutable type
        self._inequalitylocalconstraintsvalue_upper_scaler_bound_warning_raised: bool = other_subsystem._inequalitylocalconstraintsvalue_upper_scaler_bound_warning_raised

        # 32. _referencedesignvariables_lower_scaler_bound_warning_raised: bool
        # No copy.copy() needed - bool is a primitive/immutable type
        self._referencedesignvariables_lower_scaler_bound_warning_raised: bool = other_subsystem._referencedesignvariables_lower_scaler_bound_warning_raised

        # 33. _referencedesignvariables_upper_scaler_bound_warning_raised: bool
        # No copy.copy() needed - bool is a primitive/immutable type
        self._referencedesignvariables_upper_scaler_bound_warning_raised: bool = other_subsystem._referencedesignvariables_upper_scaler_bound_warning_raised

        # 34. _scalers: List[ScalerBasis]
        # copy.deepcopy() used - scalers contain mutable internal state.
        # Note: get/set_Scalers() intentionally share by reference for same-process use,
        # but update_state() needs deepcopy for multiprocessing isolation.
        self._scalers: List[ScalerBasis] = copy.deepcopy(other_subsystem.get_Scalers())

```
