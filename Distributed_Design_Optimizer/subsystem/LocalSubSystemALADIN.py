# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""ALADIN local subsystem module.

This module provides the local subsystem implementation for the
ALADIN coordination method.
"""

from typing import List, Dict, Type
import copy
import numpy as np
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.optimization import AnalysisInterface, OptimizationInterface
from Distributed_Design_Optimizer.subsystem.optimization.optimizerdata import LocalSubSystemOptimData
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalObjectiveInterface, LocalConstraintsInterface
from Distributed_Design_Optimizer.subsystem.couplingparameters import CouplingParametersInterface
from Distributed_Design_Optimizer.subsystem.couplingparameters.aladin import (LocalCouplingParametersALADIN,
                                                                              LocalToLocalForController_CouplingParameters,
                                                                              LocalToController_CouplingParametersALADIN
                                                                              )
from Distributed_Design_Optimizer.subsystem.tools import HessianApproximationBFGS, update_state_listprimitive, ScalerBasis
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print, ddo_print_border
from Distributed_Design_Optimizer.coordination.convergence import (Local_ConvergenceIndicator_Innerloop_Interface,
                                                                   Local_ConvergenceIndicator_Innerloop_DeWit,
                                                                   Local_ConvergenceIndicator_Outerloop_Interface,
                                                                   Local_ConvergenceIndicator_Outerloop_DeWit
                                                                   )
from Distributed_Design_Optimizer.coordination.updatecouplingparametermethod import (UpdateCouplingParameterMethodInterface,
                                                                                     UpdateCouplingParameterMethod_AugLagProximal_MultipliersFixedWeights
                                                                                     )
from Distributed_Design_Optimizer.middlelevel.aladin import InConsistencySize


class LocalSubSystemALADIN(LocalSubSystemBasis):
    """Local subsystem for ALADIN coordination.

    Implements the local subsystem functionality for the ALADIN
    distributed optimization method.
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
        """Create a new instance of LocalSubSystemALADIN.

        Args:
            id: Identifier for the subsystem.
            level: Level identifier for the subsystem in the hierarchy.
            neighborid: List of identifiers for neighboring subsystems.
            analysis: Analysis interface for the subsystem.
            localobjective: Local objective function interface.
            localconstraints: Local constraints function interface.
            optimization: Optimization interface.
            local_convergenceindicator_innerloop: Local convergence indicator for inner loop.
            local_convergenceindicator_outerloop: Local convergence indicator for outer loop.
            updatecouplingparametermethod_outerloop: Strategy for updating coupling parameters in outer loop.
        """
        # Compatibility settings for the components handed to this subsystem by the
        # ALADIN coordination method. These are validated here (rather than in ALADIN)
        # because the corresponding objects are handed to this subsystem.

        # Allowed / recommended outerloop update coupling parameter methods for ALADIN
        self._allowedupdatemethods_outerloop: List[Type[UpdateCouplingParameterMethodInterface]] = [
            UpdateCouplingParameterMethod_AugLagProximal_MultipliersFixedWeights
        ]
        self._recommendedupdatemethods_outerloop: List[Type[UpdateCouplingParameterMethodInterface]] = [
            UpdateCouplingParameterMethod_AugLagProximal_MultipliersFixedWeights
        ]

        # Allowed / recommended local inner loop convergence indicators for ALADIN
        self._allowedconvergenceindicators_innerloop: List[Type[Local_ConvergenceIndicator_Innerloop_Interface]] = [
            Local_ConvergenceIndicator_Innerloop_DeWit
        ]
        self._recommendedconvergenceindicators_innerloop: List[Type[Local_ConvergenceIndicator_Innerloop_Interface]] = [
            Local_ConvergenceIndicator_Innerloop_DeWit
        ]

        # Allowed / recommended local outer loop convergence indicators for ALADIN
        self._allowedconvergenceindicators_outerloop: List[Type[Local_ConvergenceIndicator_Outerloop_Interface]] = [
            Local_ConvergenceIndicator_Outerloop_DeWit
        ]
        self._recommendedconvergenceindicators_outerloop: List[Type[Local_ConvergenceIndicator_Outerloop_Interface]] = [
            Local_ConvergenceIndicator_Outerloop_DeWit
        ]

        # First init couplingparameters with local coupling parameters
        self._couplingparameters: List[LocalCouplingParametersALADIN | LocalToController_CouplingParametersALADIN] = [LocalCouplingParametersALADIN(neighbor_id) for neighbor_id in neighborid]
        
        # super() initialization is not called at the top,
        # since evaluateAllJacobians needs optimdata, and initialization of optimdata needs couplingparameters
        super().__init__(id, level, neighborid, analysis, localobjective, localconstraints, optimization)
        
        # Convergence indicators - passed from ALADIN coordination method.
        # The annotations use the concrete types allowed for ALADIN (validated below in
        # validate_inputs()); the parameters stay typed as the interfaces so that
        # validate_inputs() remains the runtime gatekeeper with friendly error messages.
        self._local_convergenceindicator_innerloop: Local_ConvergenceIndicator_Innerloop_DeWit = local_convergenceindicator_innerloop
        self._local_convergenceindicator_outerloop: Local_ConvergenceIndicator_Outerloop_DeWit = local_convergenceindicator_outerloop

        self._updatecouplingparametermethod_outerloop: UpdateCouplingParameterMethod_AugLagProximal_MultipliersFixedWeights = updatecouplingparametermethod_outerloop

        # Validate the components handed to this subsystem
        self.validate_inputs()

        self._inconsistencies: List[InConsistencySize] = [InConsistencySize(self.get_CouplingParameters()[i].get_ID())
                                                          for i in range(len(self.get_CouplingParameters()))] 
        
        # \nu and \Sigma^{i} penalty parameters from primal subproblem in ALADIN-
        # \nu: float
        # \Sigma^{i}: List[List[float]] (which should be positive definite)

        self._nu: float | None = None
        self._sigma_i: List[List[float]] | None = None
        
        # The Hessian approximations that are stored 
        # each for local objective, local equality constraints, 
        # local inequality constraints, and *mapped responses*
        # The initialization happens in initializeCouplingParameters_BeforeCopyToMiddleLevel
        self._hessianapproximation_localobjective: HessianApproximationBFGS | None = None
        self._hessianapproximation_localequalityconstraints: List[HessianApproximationBFGS] | None = None
        self._hessianapproximation_localinequalityconstraints: List[HessianApproximationBFGS] | None = None
        
        # Also for mapped responses; since i -> j coupling does not necessarily include 
        # mapped response, also None is allowed for the corresponding couplings
        self._hessianapproximation_mappedresponses: List[List[HessianApproximationBFGS] | None] | None = None

    def validate_inputs(self) -> None:
        """Validate the components handed to this subsystem by the ALADIN coordination method.

        Validates that the outer-loop update coupling parameter method and the local
        inner/outer loop convergence indicators are compatible with ALADIN.

        Raises:
            ValueError: If a provided component is not compatible with ALADIN.
        """
        # ===== updatecouplingparametermethod_outerloop Validation =====
        if type(self._updatecouplingparametermethod_outerloop) not in self._allowedupdatemethods_outerloop:
            raise ValueError(
                f"{DDO_Color}Outerloop update method '{type(self._updatecouplingparametermethod_outerloop).__name__}' is not compatible with ALADIN. "
                f"Please choose one of the compatible methods: {[m.__name__ for m in self._allowedupdatemethods_outerloop]}{Reset}"
            )
        elif type(self._updatecouplingparametermethod_outerloop) not in self._recommendedupdatemethods_outerloop:
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: Outerloop update method '{type(self._updatecouplingparametermethod_outerloop).__name__}' is not recommended for ALADIN.")
            ddo_print(f"{type(self).__name__}: Recommended methods: {[m.__name__ for m in self._recommendedupdatemethods_outerloop]}")
            ddo_print_border()

        # ===== Convergence Indicator Inner Validation =====
        if type(self._local_convergenceindicator_innerloop) not in self._allowedconvergenceindicators_innerloop:
            raise ValueError(
                f"{DDO_Color}Inner loop convergence indicator '{type(self._local_convergenceindicator_innerloop).__name__}' is not compatible with ALADIN. "
                f"Please choose one of the compatible indicators: {[c.__name__ for c in self._allowedconvergenceindicators_innerloop]}{Reset}"
            )
        elif type(self._local_convergenceindicator_innerloop) not in self._recommendedconvergenceindicators_innerloop:
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: Inner loop convergence indicator '{type(self._local_convergenceindicator_innerloop).__name__}' is not recommended for ALADIN.")
            ddo_print(f"{type(self).__name__}: Recommended indicators: {[c.__name__ for c in self._recommendedconvergenceindicators_innerloop]}")
            ddo_print_border()

        # ===== Convergence Indicator Outer Validation =====
        if type(self._local_convergenceindicator_outerloop) not in self._allowedconvergenceindicators_outerloop:
            raise ValueError(
                f"{DDO_Color}Outer loop convergence indicator '{type(self._local_convergenceindicator_outerloop).__name__}' is not compatible with ALADIN. "
                f"Please choose one of the compatible indicators: {[c.__name__ for c in self._allowedconvergenceindicators_outerloop]}{Reset}"
            )
        elif type(self._local_convergenceindicator_outerloop) not in self._recommendedconvergenceindicators_outerloop:
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: Outer loop convergence indicator '{type(self._local_convergenceindicator_outerloop).__name__}' is not recommended for ALADIN.")
            ddo_print(f"{type(self).__name__}: Recommended indicators: {[c.__name__ for c in self._recommendedconvergenceindicators_outerloop]}")
            ddo_print_border()
    
################################################################################################################
#   Basics of the subsystem
################################################################################################################       
    
    # Getters and setters
    
    def get_Nu(self) -> float:
        """Return the hyperparameter nu of the proximal term in the primal subproblem.

        Returns:
            The hyperparameter nu value.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._nu
    
    def set_Nu(self, nu_in: float) -> None:
        """Set the hyperparameter nu of the proximal term in the primal subproblem.

        Args:
            nu_in: The hyperparameter nu value to set.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning the input value directly is safe because any subsequent changes
        # to the caller's variable cannot affect this class's attribute.
        self._nu = nu_in
        
    def get_Sigma_i(self) -> List[List[float]]:
        """Get the hyperparameter Sigma_i of the proximal term in the primal subproblem.

        Returns:
            The proximal matrix Sigma_i (positive definite).
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._sigma_i)
    
    def set_Sigma_i(self, sigma_i_in: List[List[float]]) -> None:
        """Set the hyperparameter Sigma_i of the proximal term in the primal subproblem.

        Args:
            sigma_i_in: The proximal matrix Sigma_i to set (positive definite).
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._sigma_i = copy.deepcopy(sigma_i_in)
    
    def get_HessianApproximation_LocalObjective(self) -> HessianApproximationBFGS | None:
        """Get the BFGS Hessian approximation of the local objective.

        Returns:
            The BFGS approximation object, or None if not initialized.
        """
        # No copy.copy() used - HessianApproximationBFGS is a class object returned by reference intentionally.
        # This allows the caller to interact with the actual object. If isolation is needed,
        # the caller should explicitly copy.
        return self._hessianapproximation_localobjective
    
    def set_HessianApproximation_LocalObjective(self, hessianapproximation_localobjective_in: HessianApproximationBFGS) -> None:
        """Set the BFGS Hessian approximation of the local objective.

        Args:
            hessianapproximation_localobjective_in: The BFGS approximation object to set.
        """
        # No copy.copy() used - HessianApproximationBFGS is a class object
        # assigned by reference intentionally. This allows the caller to continue interacting with
        # the actual object. If isolation is needed, the caller should explicitly copy.
        self._hessianapproximation_localobjective = hessianapproximation_localobjective_in
    
    def get_HessianApproximation_LocalEqualityConstraints(self) -> List[HessianApproximationBFGS] | None:
        """Get the list of BFGS Hessian approximations of the local equality constraints.

        Returns:
            One BFGS object per equality constraint, or None if not initialized.
        """
        # No copy.copy() used - List[HessianApproximationBFGS] is a list of class objects
        # returned by reference intentionally. This allows the caller to interact with
        # the actual objects. If isolation is needed, the caller should explicitly copy.
        return self._hessianapproximation_localequalityconstraints
    
    def set_HessianApproximation_LocalEqualityConstraints(self, hessianapproximation_localequalityconstraints_in: List[HessianApproximationBFGS]) -> None:
        """Set the list of BFGS Hessian approximations of the local equality constraints.

        Args:
            hessianapproximation_localequalityconstraints_in: One BFGS object per equality constraint.
        """
        # No copy.copy() used - List[HessianApproximationBFGS] is a list of class objects
        # assigned by reference intentionally. This allows the caller to continue interacting with
        # the actual objects. If isolation is needed, the caller should explicitly copy.
        self._hessianapproximation_localequalityconstraints = hessianapproximation_localequalityconstraints_in
    
    def get_HessianApproximation_LocalInequalityConstraints(self) -> List[HessianApproximationBFGS] | None:
        """Get the list of BFGS Hessian approximations of the local inequality constraints.

        Returns:
            One BFGS object per inequality constraint, or None if not initialized.
        """
        # No copy.copy() used - List[HessianApproximationBFGS] is a list of class objects
        # returned by reference intentionally. This allows the caller to interact with
        # the actual objects. If isolation is needed, the caller should explicitly copy.
        return self._hessianapproximation_localinequalityconstraints
    
    def set_HessianApproximation_LocalInequalityConstraints(self, hessianapproximation_localinequalityconstraints_in: List[HessianApproximationBFGS]) -> None:
        """Set the list of BFGS Hessian approximations of the local inequality constraints.

        Args:
            hessianapproximation_localinequalityconstraints_in: One BFGS object per inequality constraint.
        """
        # No copy.copy() used - List[HessianApproximationBFGS] is a list of class objects
        # assigned by reference intentionally. This allows the caller to continue interacting with
        # the actual objects. If isolation is needed, the caller should explicitly copy.
        self._hessianapproximation_localinequalityconstraints = hessianapproximation_localinequalityconstraints_in
    
    def get_HessianApproximation_MappedResponses(self) -> List[List[HessianApproximationBFGS] | None] | None:
        """Get the list of BFGS Hessian approximations of the mapped responses.

        Each entry corresponds to one local-to-local coupling. Since a coupling
        may not include mapped responses, entries can be None.

        Returns:
            Nested list of BFGS objects per coupling, or None.
        """
        
        return self._hessianapproximation_mappedresponses
        
    def set_HessianApproximation_MappedResponses(
        self, 
        hessianapproximations_mappedresponses_in: List[List[HessianApproximationBFGS] | None]
        ) -> None:
        """Set the list of BFGS Hessian approximations of the mapped responses.

        Args:
            hessianapproximations_mappedresponses_in: Nested list of BFGS objects per coupling.
        """
        
        self._hessianapproximation_mappedresponses = hessianapproximations_mappedresponses_in        
    
    # Controller handling methods    
        
    def append_Controller(self) -> None:
        """Update local subsystems by appending controller and adding necessary coupling parameters.
        """
        
        # Add "C" to neighborslist
        self._neighborid.append("C")
        
        # Instantiate new controller coupling parameters object
        localtocontroller_couplingparameters: LocalToController_CouplingParametersALADIN = LocalToController_CouplingParametersALADIN()
        
        # Get neighborid to loop over neighbors of i
        neighborid: List[str] = self.get_NeighborId()
        
        # Instantiate LocalToLocalForController_CouplingParameters for each i (current subsystem) <-> j coupling, with direction local -> controller
        localtocontroller_couplingparameters.set_LocalToLocalForController_CouplingParameters([LocalToLocalForController_CouplingParameters(id=j) for j in neighborid])
        
        # Add control coupling parameters object to local coupling parameters list
        self._couplingparameters.append(localtocontroller_couplingparameters)
        
        # Synchronize the LocalToLocalForController_CouplingParameters objects for each i (current subsystem) <-> j coupling
        self.synchronize_AllLocalGlobalCouplingParameters()
        
        
    def get_LocalToController_CouplingParameters(self) -> LocalToController_CouplingParametersALADIN:
        """Return the controller coupling parameters.

        Returns:
            The controller coupling parameters object.
        """
        # No copy.copy() used - LocalToController_CouplingParametersALADIN is a class object returned by reference intentionally.
        # This allows the caller to interact with the actual object. If isolation is needed,
        # the caller should explicitly copy.
        
        # Get the coupling parameters
        couplingparameters: List[CouplingParametersInterface] = self.get_CouplingParameters()
        
        # Loop over all coupling parameters to find the controller coupling parameter
        for couplingparameter in couplingparameters:
            
            # Check if the coupling parameter is of local -> controller type
            if isinstance(couplingparameter, LocalToController_CouplingParametersALADIN):
                
                # Return the LocalToController_CouplingParametersALADIN
                return couplingparameter
        
        # If no controller coupling parameter is found, raise an error
        raise ValueError(f"No controller coupling parameter found for subsystem {self.get_SUBSYSTEMID()}.")
    
        
    def synchronize_AllLocalGlobalCouplingParameters(self) -> None:
        """Synchronize all local-global coupling parameters to the controller.

        This method synchronizes every information that is needed by
        the controller and stored in the local couplings between i
        and j to the controller coupling parameters object's
        LocalToLocalForController_CouplingParameters objects.
        """
        
        # Get neighbors of local subsystem
        neighborid: List[str] = self.get_NeighborId()
        # Get coupling parameter list
        couplingparameters: List[CouplingParametersInterface] = self.get_CouplingParameters()
        # Get controller (it is the last entry of the list)
        localtocontroller_couplingparameters: LocalToController_CouplingParametersALADIN = self.get_LocalToController_CouplingParameters()
        # Get local to controller coupling parameters
        localtolocalforcontroller_couplingparameters: List[LocalToLocalForController_CouplingParameters] = localtocontroller_couplingparameters.get_LocalToLocalForController_CouplingParameters()
        
        # Synchronize CCP with optimdata Jacobians (local cost function, equality + inequality constr)
        if self._optimdata.get_Gradient_LocalObjective() is not None:
            localtocontroller_couplingparameters.set_Gradient_LocalObjective(self._optimdata.get_Gradient_LocalObjective())
        if self._optimdata.get_Jacobian_LocalEqualityConstraints() is not None:
            localtocontroller_couplingparameters.set_Jacobian_LocalEqualityConstraints(self._optimdata.get_Jacobian_LocalEqualityConstraints())
        if self._optimdata.get_Jacobian_LocalInequalityConstraints() is not None:
            
            # Communicate the Jacobian of all local inequality constraints (active and inactive)
            localtocontroller_couplingparameters.set_Jacobian_LocalInequalityConstraints(self._optimdata.get_Jacobian_LocalInequalityConstraints())
        
        if self._optimdata.get_Jacobian_LowerBounds() is not None:
            localtocontroller_couplingparameters.set_Jacobian_LowerBound(self._optimdata.get_Jacobian_LowerBounds())
        if self._optimdata.get_Jacobian_UpperBounds() is not None:
            localtocontroller_couplingparameters.set_Jacobian_UpperBound(self._optimdata.get_Jacobian_UpperBounds())
        # Synchronize LocalToLocalForController_CouplingParameters objects
        
        # NOTE: Notice that no entry exists for the controller
        # That's why in loops where we loop over the couplingparameters
        # and localtocontroller_couplingparameters, there is an additional 'index_helper' 
        # so that while the controller is skipped over in couplingparameters, 
        # the loop over the localtocontroller_couplingparameters works correctly
        # Example: couplingparameter = (1, C, 2), but localtocontroller_couplingparameters = (LTCP_1, LTCP_2)
        index_helper: int = 0
        
        # Loop over neighbors and synchronize corresponding entries
        # for i <-> j coupling
        for j in range(len(neighborid)):
            # Skip controller subsystem
            if isinstance(couplingparameters[j], LocalCouplingParametersALADIN):
                # Synchronize
                self.synchronize_LocalGlobalCouplingParameter(localtolocal_couplingparameter=couplingparameters[j], 
                                                              localtolocalforcontroller_couplingparameter=localtolocalforcontroller_couplingparameters[index_helper])
                
                # Synchronize Jacobian of mapped responses from optimdata into the LocalToLocalForController_CouplingParameters
                # (localtolocal_couplingparameter does not store the Jacobian; it lives in self._optimdata)
                id_j: str = couplingparameters[j].get_ID()
                jacobian_mappedresponse = self._optimdata.get_Jacobian_MappedResponse(id_j)
                if jacobian_mappedresponse is not None:
                    localtolocalforcontroller_couplingparameters[index_helper].set_JacobianMappedResponses(copy.copy(jacobian_mappedresponse))
                
                # Update the auxiliary counter
                index_helper += 1
    
    
    def synchronize_LocalGlobalCouplingParameter(self, localtolocal_couplingparameter: LocalCouplingParametersALADIN, 
                                                 localtolocalforcontroller_couplingparameter: LocalToLocalForController_CouplingParameters) -> None:
        """Synchronize a single local-global coupling parameter to the controller.

        This method synchronizes every information that is needed by
        the controller and stored in the local couplings between i
        and j to the controller coupling parameters object's
        LocalToLocalForController_CouplingParameters objects.

        Args:
            localtolocal_couplingparameter: Local coupling parameters between subsystems i and j.
            localtolocalforcontroller_couplingparameter: Coupling parameters from local subsystem to controller.
        """
        
        # Local coupling parameters object for i <-> j coupling
        localtolocal_couplingparameter: LocalCouplingParametersALADIN = localtolocal_couplingparameter
        
        # Controller coupling parameters object for i <-> controller
        localtolocalforcontroller_couplingparameter: LocalToLocalForController_CouplingParameters = localtolocalforcontroller_couplingparameter
        
        # Synchronize mapped responses / coupling variables / shared design variables / target shared design variables
        # Synchronize multipliers
        # Synchronize weights
        
        # No copy.copy() wrapper needed - getter returns defensive copy and setter creates its own copy
        if localtolocal_couplingparameter.get_MappedResponses() is not None:
            localtolocalforcontroller_couplingparameter.set_MappedResponses(localtolocal_couplingparameter.get_MappedResponses())
        if localtolocal_couplingparameter.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable() is not None:
            localtolocalforcontroller_couplingparameter.set_Multipliers_MappedResponse_Minus_CopyCouplingVariable(localtolocal_couplingparameter.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable())
        if localtolocal_couplingparameter.get_Weights_MappedResponse_Minus_CopyCouplingVariable() is not None:
            localtolocalforcontroller_couplingparameter.set_Weights_MappedResponse_Minus_CopyCouplingVariable(localtolocal_couplingparameter.get_Weights_MappedResponse_Minus_CopyCouplingVariable())
        
        if localtolocal_couplingparameter.get_CouplingVariable() is not None:
            localtolocalforcontroller_couplingparameter.set_CouplingVariables(localtolocal_couplingparameter.get_CouplingVariable())
        if localtolocal_couplingparameter.get_Multipliers_CopyMappedResponse_Minus_CouplingVariable() is not None:
            localtolocalforcontroller_couplingparameter.set_Multipliers_CopyMappedResponse_Minus_CouplingVariable(localtolocal_couplingparameter.get_Multipliers_CopyMappedResponse_Minus_CouplingVariable())
        if localtolocal_couplingparameter.get_Weights_CopyMappedResponse_Minus_CouplingVariable() is not None:
            localtolocalforcontroller_couplingparameter.set_Weights_CopyMappedResponse_Minus_CouplingVariable(localtolocal_couplingparameter.get_Weights_CopyMappedResponse_Minus_CouplingVariable())
        
        if localtolocal_couplingparameter.get_SharedDesignVariables() is not None:
            localtolocalforcontroller_couplingparameter.set_SharedDesignVariables(localtolocal_couplingparameter.get_SharedDesignVariables())
        if localtolocal_couplingparameter.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable() is not None:
            localtolocalforcontroller_couplingparameter.set_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(localtolocal_couplingparameter.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
        if localtolocal_couplingparameter.get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable() is not None:
            localtolocalforcontroller_couplingparameter.set_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(localtolocal_couplingparameter.get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
            
        if localtolocal_couplingparameter.get_TargetSharedDesignVariables() is not None:
            localtolocalforcontroller_couplingparameter.set_TargetSharedDesignVariables(localtolocal_couplingparameter.get_TargetSharedDesignVariables())
        if localtolocal_couplingparameter.get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable() is not None:
            localtolocalforcontroller_couplingparameter.set_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(localtolocal_couplingparameter.get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable())
        if localtolocal_couplingparameter.get_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable() is not None:
            localtolocalforcontroller_couplingparameter.set_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(localtolocal_couplingparameter.get_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable())
            
        # Indices of coupling, shared and target shared variables in total designvariables vector of local subsystem
        if localtolocal_couplingparameter.get_Indices_CouplingVariables_In_DesignVariables() is not None:
            localtolocalforcontroller_couplingparameter.set_Indices_CouplingVariables_In_DesignVariables(
                copy.copy(localtolocal_couplingparameter.get_Indices_CouplingVariables_In_DesignVariables())
            )
            
        if localtolocal_couplingparameter.get_Indices_SharedDesignVariables_In_DesignVariables() is not None:
            localtolocalforcontroller_couplingparameter.set_Indices_SharedDesignVariables_In_DesignVariables(
                copy.copy(localtolocal_couplingparameter.get_Indices_SharedDesignVariables_In_DesignVariables())
            )
        
        if localtolocal_couplingparameter.get_Indices_TargetSharedDesignVariables_In_DesignVariables() is not None:
            localtolocalforcontroller_couplingparameter.set_Indices_TargetSharedDesignVariables_In_DesignVariables(
                copy.copy(localtolocal_couplingparameter.get_Indices_TargetSharedDesignVariables_In_DesignVariables())
            )
            
        
##############################################################################################################
#   Functions to evaluate a subsystem's responses and map them onto coupling parameters
##############################################################################################################
    
    def mapToController(self) -> None:
        """Synchronize necessary information with the controller.

        Only subsystem i's information like e.g. Jacobians, 
        Hessians, local multipliers, ..., are computed and stored in 
        couplingparameters in postprocess_Optimization.
        """
        
        # Synchronize local to controller coupling parameters
        self.synchronize_AllLocalGlobalCouplingParameters()
        
##############################################################################################################
#   Functions to evaluate a subsystem's optimization objective and constraints for given responses
##############################################################################################################
 
    def evaluateCoordinationObjective(self) -> None:
        """Evaluate the coordination objective including inner product and proximal terms.
        """
        
        couplingin: List[LocalCouplingParametersALADIN | LocalToController_CouplingParametersALADIN] = self.get_CouplingParameters()
        normcoupl = np.zeros(len(couplingin))
        inconsistency: List[InConsistencySize] = [InConsistencySize(couplingin[i].get_ID())
                                                  for i in range(len(couplingin))]
        
        # 1st part of coordination objective
        
        # Loop over subsystems to build inner product term of 
        # multiplier estimate and coupling inconsistencies
        
        for i in range(len(couplingin)):
            
            # Skip over controller coupling
            if isinstance(couplingin[i], LocalCouplingParametersALADIN):

                lagrangian_copymapres_minus_coupl = None
                lagrangian_mapres_minus_copycoupl = None
                lagrangian_shared_minus_copytgtshared = None
                lagrangian_copyshared_minus_tgtshared = None
                
                if ((couplingin[i].get_CouplingVariable() is not None) and
                        (couplingin[i].get_Copy_MappedResponses() is not None)):
                    # Copied mapped response minus coupling variable inconsistency
                    couplingvariable: List[float] = couplingin[i].get_CouplingVariable()
                    copymappedresponse: List[float] = couplingin[i].get_Copy_MappedResponses()
                    
                    inconsistency[i].evaluate_CopyMappedResponse_Minus_CouplingVariable(couplingvariable=couplingvariable, copymappedresponse=copymappedresponse)
                    
                    lagrangian_copymapres_minus_coupl = np.array(couplingin[i].get_Multipliers_CopyMappedResponse_Minus_CouplingVariable()) * np.array(inconsistency[i].get_CopyMappedResponse_Minus_CouplingVariable())  # element-wise multiplication
                else:
                    lagrangian_copymapres_minus_coupl = np.array([0.0])

                if ((couplingin[i].get_Copy_CouplingVariable() is not None) and
                        (couplingin[i].get_MappedResponses() is not None)):
                    # Mapped response minus copied coupling variable inconsistency
                    copycouplingvariable: List[float] = couplingin[i].get_Copy_CouplingVariable()
                    mappedresponse: List[float] = couplingin[i].get_MappedResponses()
                    
                    inconsistency[i].evaluate_MappedResponse_Minus_CopyCouplingVariable(copycouplingvariable=copycouplingvariable, mappedresponse=mappedresponse)
                    
                    lagrangian_mapres_minus_copycoupl = np.array(couplingin[i].get_Multipliers_MappedResponse_Minus_CopyCouplingVariable()) * np.array(inconsistency[i].get_MappedResponse_Minus_CopyCouplingVariable())  # element-wise multiplication
                else:
                    lagrangian_mapres_minus_copycoupl = np.array([0.0])

                if ((couplingin[i].get_Copy_TargetSharedDesignVariables() is not None) and
                        (couplingin[i].get_SharedDesignVariables() is not None)):
                    # Shared design variable minus copied target shared design variable inconsistency
                    copytargetshareddesignvariable: List[float] = couplingin[i].get_Copy_TargetSharedDesignVariables()
                    shareddesignvariable: List[float] = couplingin[i].get_SharedDesignVariables()
                    
                    inconsistency[i].evaluate_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(copytargetshareddesignvariable=copytargetshareddesignvariable, shareddesignvariable=shareddesignvariable)
                                    
                    lagrangian_shared_minus_copytgtshared = np.array(couplingin[i].get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable()) * np.array(inconsistency[i].get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())  # element-wise multiplication
                else:
                    lagrangian_shared_minus_copytgtshared = np.array([0.0])

                if ((couplingin[i].get_Copy_SharedDesignVariables() is not None) and
                        (couplingin[i].get_TargetSharedDesignVariables() is not None)):
                    # Copied shared design variable minus target shared design variable inconsistency
                    copyshareddesignvariable: List[float] = couplingin[i].get_Copy_SharedDesignVariables()
                    targetshareddesignvariable: List[float] = couplingin[i].get_TargetSharedDesignVariables()
                    
                    inconsistency[i].evaluate_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(targetshareddesignvariable=targetshareddesignvariable, copyshareddesignvariable=copyshareddesignvariable)

                    lagrangian_copyshared_minus_tgtshared = np.array(couplingin[i].get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable()) * np.array(inconsistency[i].get_CopySharedDesignVariable_Minus_TargetSharedDesignVariable())  # element-wise multiplication
                else:
                    lagrangian_copyshared_minus_tgtshared = np.array([0.0])

                # Evaluate the objective inconsistency function
                normcoupl[i] = np.sum(lagrangian_copymapres_minus_coupl) + np.sum(lagrangian_mapres_minus_copycoupl) + np.sum(lagrangian_shared_minus_copytgtshared) + np.sum(lagrangian_copyshared_minus_tgtshared)

        # Compute the sum of all the penalty function contributions
        # to get the inner product part of the coordination objective
        phinorm_innerproduct = np.array(normcoupl)
        objective_innerproduct_inconsistency = float(np.sum(phinorm_innerproduct))
        
        
        # 2nd part of coordination objective value 
        # Compute the proximal term in ALADIN using \d and \d_hat, \nu and \Sigma_i
        
        # Local designvariables d
        d: List[float] = self.get_DesignVariables()
        
        # Controller influenced entity d_hat
        localtocontroller_couplingparameters: LocalToController_CouplingParametersALADIN = self.get_LocalToController_CouplingParameters()
        d_hat: List[float] = localtocontroller_couplingparameters.get_D_hat()
        
        # Get proximal matrix
        proximal_matrix: np.typing.ArrayLike = np.array(self.get_Sigma_i())       
        
        # Evaluate difference vector and store in numpy array
        difference_d_and_d_hat: np.typing.ArrayLike = np.array([d[i] - d_hat[i] for i in range(len(d))])
        
        # Compute proximal norm defined by \Sigma_i, @-operator is matrix-vector multiplication
        proximal_squared_distance: np.typing.ArrayLike = difference_d_and_d_hat @ proximal_matrix @ difference_d_and_d_hat
        
        # Multiply with \nu / 2
        objective_proximal_term: float = self._nu * float(proximal_squared_distance) / 2
        
        # Add inner product term and proximal objective
        coordinationobjectivevalue: float = objective_innerproduct_inconsistency + objective_proximal_term
        
        # set the objective inconsistency value to subsystem object
        self.set_CoordinationObjectiveValue(coordinationobjectivevalue=coordinationobjectivevalue)
    
    def evaluate_Gradient_CoordinationObjective(self) -> None:
        """Evaluate the analytical gradient of the coordination objective.

        Assumes the mapped responses Jacobian was evaluated already.
        """
        
        # TODO    
        pass
    
    def evaluateCoordinationEqualityConstraint(self) -> None:
        """Evaluate the coordination equality constraint for ALADIN.
        """
        couplingin: List[LocalCouplingParametersALADIN | LocalToController_CouplingParametersALADIN] = self.get_CouplingParameters()
        #########################################################################################################
        constraint_inconsistency = None
        #########################################################################################################
        self.set_CoordinationEqualityConstraintValue(constraint_inconsistency)
        
    def evaluateCoordinationInequalityConstraint(self) -> None:
        """Evaluate the coordination inequality constraint for ALADIN.
        """
        couplingin: List[LocalCouplingParametersALADIN | LocalToController_CouplingParametersALADIN] = self.get_CouplingParameters()
        #########################################################################################################
        constraint_inconsistency = None
        #########################################################################################################
        self.set_CoordinationInequalityConstraintValue(constraint_inconsistency)
        
        
    def evaluate_Jacobian_CoordinationEqualityConstraints(self) -> None:
        """Evaluate the Jacobian of the coordination equality constraints.

        ALADIN does not have coordination equality constraints, hence no-op.
        """
        
        pass
        
    def evaluate_Jacobian_CoordinationInEqualityConstraints(self) -> None:
        """Evaluate the Jacobian of the coordination inequality constraints.

        ALADIN does not have coordination inequality constraints, hence no-op.
        """
        
        # No coordination inequality constraints
        pass

##############################################################################################################
#   Functions to prepare, solve and postprocess a subsystem's optimization problem
##############################################################################################################

    def prepare_OptimizationProblem(self) -> None:
        """Update d_hat.
        """
        
        # Get controller coupling
        localtocontroller_couplingparameters: LocalToController_CouplingParametersALADIN = self.get_LocalToController_CouplingParameters()
        
        # Get delta_d
        copy_delta_d: List[float] = localtocontroller_couplingparameters.get_Copy_Delta_D()
        
        # Get designvariables
        designvariables: List[float] = self.get_DesignVariables()
        
        # ALADIN needs to update d_hat
        d_hat_new: List[float] = [designvariables[i] + copy_delta_d[i] for i in range(len(designvariables))]
        localtocontroller_couplingparameters.set_D_hat(d_hat_new)
    
    def postprocess_Optimization(self) -> None:
        """Perform ALADIN's postprocessing.
        """
        
        # Get the local -> controller coupling parameter
        localtocontroller_couplingparameters: LocalToController_CouplingParametersALADIN = self.get_LocalToController_CouplingParameters()
        
        # Get the coupling parameters
        couplingparameters: List[CouplingParametersInterface] = self.get_CouplingParameters() 
        
        localtolocalforcontroller_couplingparameters: List[LocalToLocalForController_CouplingParameters] = localtocontroller_couplingparameters.get_LocalToLocalForController_CouplingParameters()
        
        
        # Communicate the local inequality and bound constraint violations
        designvariables: List[float] | None = self.get_DesignVariables()
        scalers: List[ScalerBasis] = self.get_Scalers()
        
        # Check if there are designvariables
        if designvariables is not None:
            
            # Local inequality constraints
            localtocontroller_couplingparameters.set_LocalInequalityConstraintsValue(self.get_InequalityLocalConstraintsValue())
            
            # Lower bounds
            
            # Get scaled lower bounds
            lowerbounds = self.get_LowerBounds_Unscaled()
            lowerbounds_scaled = [scalers[index].transform(lowerbounds[index]) for index in range(len(lowerbounds))]
            
            # Store the deviation from lower bounds in local -> controller coupling parameters
            lowerbound_deviation: List[float] = [lowerbounds_scaled[index] - designvariables[index] for index in range(len(designvariables))]
            localtocontroller_couplingparameters.set_Lower_BoundConstraints_Value(lowerbound_deviation)
            
            # Upper bounds
            
            # Get scaled upper bounds
            upperbounds = self.get_UpperBounds_Unscaled()
            upperbounds_scaled = [scalers[index].transform(upperbounds[index]) for index in range(len(upperbounds))]
            
            # Store the deviation from upper bounds in local -> controller coupling parameters
            upperbound_deviation: List[float] = [designvariables[index] - upperbounds_scaled[index] for index in range(len(designvariables))]
            localtocontroller_couplingparameters.set_Upper_BoundConstraints_Value(upperbound_deviation)
            
         
        # Compute Jacobians of local equality and inequality constraints, as well as bounds, and write into LocalToController_CouplingParametersALADIN object
        # Including Jacobians of mapped responses into LocalToController_CouplingParametersALADIN.localtocontroller_couplingparameter
        # Synchronize subsystem
        self.evaluateAllJacobians()
        self.updateSubsystemfromOptimdata(self.get_OptimData())
        
        # Update the Hessians via the Hessian approximation method BFGS
        local_hessians: Dict[str, List[List[float]] | List[List[List[float]] | List[List[List[List[float]]]] |  None] | None] = self.evaluateAllHessians()         
            
        # Check if for existing local (bound / inequality / equality) constraints, corresponding multipliers are set
        # Synchronize subsystem
        if self.check_MultipliersNotSet():
            # If not all multipliers to existing constraints are set, we call the compute_KKT_multipliers method
            # This will update optimdata's corresponding fields
            self.compute_KKT_multipliers()
        self.updateSubsystemfromOptimdata(self.get_OptimData())

        # Using multipliers, compute the Hessian of the lagrangian w.r.t. local constraints and store in LocalToController_CouplingParametersALADIN.py
        # Bound constraints can be omitted here, because hessian is zero matrix
        
        hessian_lagrangian: List[List[float]] = self.evaluate_Hessian_Lagrangian(local_hessians)
        
        # Store the Hessian of the Lagrangian in the local -> controller coupling parameter
        localtocontroller_couplingparameters.set_Hessian_LocalConstraints_Lagrangian(hessian_lagrangian)
        
        
        # NOTE: Notice that no entry exists for the controller
        # That's why in loops where we loop over the couplingparameters
        # and BFGS objects, there is an additional 'index_helper' 
        # so that while the controller is skipped over in couplingparameters, 
        # the loop over the BFGS objects works correctly
        # Example: couplingparameter = (1, C, 2), but mappedresponsehessians = (None, BFGS_1)
        index_helper: int = 0
        
        # Store the Hessians of the mapped responses
        for i in range(len(couplingparameters)):
            
            # Check if it is a local <-> local coupling
            if isinstance(couplingparameters[i], LocalCouplingParametersALADIN):
                
                # Get the entry in local -> controller coupling parameters
                localtolocalforcontroller_couplingparameter: LocalToLocalForController_CouplingParameters = localtolocalforcontroller_couplingparameters[index_helper]
                
                # Check if there is a mapped response in a coupling
                if local_hessians["Mapped Responses"][index_helper] is not None:
                    
                    # Store the Hessian
                    localtolocalforcontroller_couplingparameter.set_HessiansMappedResponses(local_hessians["Mapped Responses"][index_helper])
                
                # Update the auxiliary counter
                index_helper += 1
    
    
    def evaluate_Hessian_Lagrangian(self, local_hessians: Dict[str, List[List[float]] | List[List[List[float]] | None] | None]
                                    ) -> List[List[float]]:
        """Compute the Hessian of the Lagrangian w.r.t. local and coordination constraints.

        Given the Hessians of each summand of the Lagrangian, this function computes
        the combined Hessian of the Lagrangian.

        Args:
            local_hessians: Dictionary mapping constraint type names to their Hessian
                matrices. Keys include "Local Objective", "Local Equality Constraints",
                and "Local Inequality Constraints".

        Returns:
            The combined Hessian of the Lagrangian as a 2D list.
        """
        
        # Compute the dimension(s) of the Hessian
        primal_dimension: int = len(self.get_DesignVariables())
        
        # Initialize the total Hessian as zeros-matrix
        hessian_lagrangian: np.typing.ArrayLike = np.array([[0.0] * primal_dimension] * primal_dimension)
        
        # Local objective Hessian
        if local_hessians["Local Objective"] is not None:
            
            # Add the Hessian of the local objective
            hessian_lagrangian += np.array(local_hessians["Local Objective"])
            
        # Local equality constraint Hessians weighted by corresponding multipliers
        
        # Get the multipliers
        multipliers_localequalityconstraints: List[float] | None = self._optimdata.get_Multipliers_Local_Equality_Constraints()
        
        # Check if any local equality constraints exist, and if this is consistent with the multipliers
        if (local_hessians["Local Equality Constraints"] is not None 
            and multipliers_localequalityconstraints is not None):
            
            # Loop over the local equality constraints
            for i in range(len(local_hessians["Local Equality Constraints"])):
                
                # Add the Hessian of the corresponding local equality constraint 
                # weighted by the associated multiplier component
                
                hessian_lagrangian += multipliers_localequalityconstraints[i] * np.array(local_hessians["Local Equality Constraints"][i])
        
        # Local inequality constraint Hessians weighted by corresponding multipliers
        
        # Get the multipliers
        multipliers_localinequalityconstraints: List[float | None] | None = self._optimdata.get_Multipliers_Local_Inequality_Constraints()
        
        # Check if any local inequality constraints exist, and if this is consistent with multipliers 
        if (local_hessians["Local Inequality Constraints"] is not None 
            and multipliers_localinequalityconstraints is not None):
            
            # Loop over the local inequality constraints
            for i in range(len(local_hessians["Local Inequality Constraints"])):
                
                # Check if the corresponding local inequality constraint is active
                if (local_hessians["Local Inequality Constraints"][i] is not None 
                    and multipliers_localinequalityconstraints[i] is not None):
                
                    # Add the Hessian of the corresponding local inequality constraint
                    # weighted by the associated multiplier
                    
                    hessian_lagrangian += multipliers_localinequalityconstraints[i] * np.array(local_hessians["Local Inequality Constraints"][i])
                    
        # Return the Hessian of the Lagrangian w.r.t. local constraints
        return hessian_lagrangian.tolist()
        
        
    
    def check_MultipliersNotSet(self) -> bool:
        """Return True if any existing constraint is missing its corresponding multiplier in optimdata.

        Returns:
            True if at least one constraint has no corresponding multiplier set.
        """
        
        # Get optimdata
        # Check if in self._optimdatabasis, multipliers are set; else, execute compute_KKT_system
        # compute_KKT_multipliers is defined in SubSystemBasis.py
        optimdata: LocalSubSystemOptimData = self.get_OptimData()
        
        return (self.get_LowerBounds_Unscaled() is not None and optimdata.get_Multipliers_LowerBounds() is None) or \
        (self.get_UpperBounds_Unscaled() is not None and optimdata.get_Multipliers_UpperBounds() is None) or \
        (self.get_InequalityLocalConstraintsValue() is not None and optimdata.get_Multipliers_Local_Inequality_Constraints() is None) or \
        (self.get_EqualityLocalConstraintsValue() is not None and optimdata.get_Multipliers_Local_Equality_Constraints() is None) or \
        (self.get_CoordinationEqualityConstraintValue() is not None and optimdata.get_Multipliers_Coordination_Equality_Constraints() is None) or \
        (self.get_CoordinationInequalityConstraintValue() is not None and optimdata.get_Multipliers_Coordination_Inequality_Constraints() is None)
    
    def evaluateAllHessians(self) -> Dict[str, List[List[float]] | List[List[List[float]] | List[List[List[List[float]]]] | None] | None]:
        """Evaluate all Hessians of local objective, local equality constraints and local inequality constraints.

        If they exist and were provided by the user, those are used;
        else, BFGS approximations are used.

        Returns:
            Dictionary with keys 'Local Objective', 'Local Equality Constraints',
                'Local Inequality Constraints', and 'Mapped Responses'.
        """
        
        # Create a dictionary to hold the corresponding Hessians
        local_hessians: Dict[str, List[List[float]] | List[List[List[float]] | List[List[List[List[float]]]] | None] | None] = {}
        
        # Hessian of the local objective
        
        hessian_localobjective: List[List[float]] | None = None 
        
        # Check if the local objective exists
        if self.get_LocalObjectiveValue() is not None:
            hessian_localobjective = self.evaluate_Complete_Hessian_LocalObjective() 
            
        # Store into dictionary
        local_hessians["Local Objective"] = hessian_localobjective
        
        # Hessians of the local equality constraints
        
        hessians_localequalityconstraints: List[List[List[float]]] | None = None
        
        # Check if the local equality constraints exist
        if self.get_EqualityLocalConstraintsValue() is not None:
            hessians_localequalityconstraints = self.evaluate_Complete_Hessian_LocalEqualityConstraints()

        # Store into dictionary
        local_hessians["Local Equality Constraints"] = hessians_localequalityconstraints
            
        # Hessians of the local inequality constraints
        
        hessians_localinequalityconstraints: List[List[List[float]]] | None = None
        
        # Check if the local inequality constraints exist
        if self.get_InequalityLocalConstraintsValue() is not None:
            hessians_localinequalityconstraints = self.evaluate_Hessian_LocalInequalityConstraints()
            
        # Store into dictionary
        local_hessians["Local Inequality Constraints"] = hessians_localinequalityconstraints
        
        # Hessians of the mapped responses
        
        # Get coupling parameters 
        couplingparameters: List[CouplingParametersInterface] = self.get_CouplingParameters()
        
        hessians_mappedresponses: List[List[List[List[float]]] | None] = self.evaluate_Complete_Hessian_MappedResponses()
        
        # Store into dictionary
        local_hessians["Mapped Responses"] = hessians_mappedresponses
        
        # Return the dictionary storage
        return local_hessians
        
    def evaluate_Complete_Hessian_LocalObjective(self) -> List[List[float]]:
        """Evaluate a complete Hessian of the local objective.

        - If the user-provided Hessian is complete, this will be used
        - Else, the BFGS-approximation of the Hessian of the local objective

        Returns:
            Complete Hessian matrix of the local objective.
        """
        
        # User provided Hessian of the local objective
        hessian_localobjective: List[List[float | None]] | None = self.evaluate_Hessian_LocalObjective()
        
        # Check if the local objective exists / local Hessian approximation BFGS object is already initialized
        if self._hessianapproximation_localobjective is not None:
            
            # Since BFGS update depends on the previous BFGS approximations over multiple iterations, 
            # and it could happen that the user provided a Hessian for one iteration, but could not 
            # provide for the other iteration (meaning that the BFGS approximation needs to be used then), 
            # we need to carry out the BFGS update in every iteration
            
            # Get the local design variables
            designvariables: List[float] = copy.copy(self._designvariables)
                
            # Get the gradient of the local objective
            # Since this function is only called after evaluateAllJacobians was called, 
            # The right hand side is not None
            # No copy.copy() wrapper needed - getter already returns defensive copy
            gradient_localobjective: List[float | None] | None = self._optimdata.get_Gradient_LocalObjective()
                
            # Update the Hessian approximation via BFGS
            self._hessianapproximation_localobjective.updateHessianApproximation(designvariables, gradient_localobjective)
        
            # Check if the Hessian of the local objective provided by the scripts of the user are complete
            if hessian_localobjective is None or any(entry is None for row in hessian_localobjective for entry in row):
            
                # Store the new BFGS iterate as the complete Hessian approximation
                hessian_localobjective = copy.deepcopy(self._hessianapproximation_localobjective.get_matrix().tolist())
                
        return hessian_localobjective
    
    def evaluate_Complete_Hessian_LocalEqualityConstraints(self) -> List[List[List[float]]]:
        """Evaluate complete Hessians of all local equality constraints.

        - If the user-provided Hessian for a constraint is complete, this will be used
        - Else, the BFGS-approximation of the Hessian of that equality constraint

        Returns:
            List of complete Hessian matrices, one per equality constraint.
        """
        
        # User provided Hessians of the local equality constraints
        hessians_localequalityconstraints: List[List[List[float | None]]] | None = self.evaluate_Hessian_EqualityLocalConstraints()
        
        hessians_complete: List[List[List[float]]] = []
        
        # Check if the local equality constraints exist / local BFGS approximation objects are initialized
        if self._hessianapproximation_localequalityconstraints is not None:
            
            # Get the local design variables
            designvariables: List[float] = copy.copy(self._designvariables)
            
            # Get the Jacobian of the local equality constraints once
            # Since this function is only called after evaluateAllJacobians was called,
            # the right hand side is not None
            # No copy wrapper needed - getter already returns copy.deepcopy()
            jacobian_localequalityconstraints: List[List[float | None]] | None = self._optimdata.get_Jacobian_LocalEqualityConstraints()
            
            for i in range(len(self._hessianapproximation_localequalityconstraints)):
                
                # Since BFGS update depends on the previous BFGS approximations over multiple iterations, 
                # and it could happen that the user provided a Hessian for one iteration, but could not 
                # provide for the other iteration (meaning that the BFGS approximation needs to be used then), 
                # we need to carry out the BFGS update in every iteration
                
                # Get the gradient of this equality constraint (row of the Jacobian)
                # No copy.copy() needed - jacobian_localequalityconstraints is already a deepcopy from the getter
                gradient_i: List[float] = jacobian_localequalityconstraints[i]
                
                # Update the Hessian via BFGS
                self._hessianapproximation_localequalityconstraints[i].updateHessianApproximation(designvariables, gradient_i)
                
                # Extract the user-provided Hessian for this constraint
                hessian_i: List[List[float | None]] | None = None
                if hessians_localequalityconstraints is not None:
                    hessian_i = hessians_localequalityconstraints[i]
                
                # Check if the user-provided Hessian is complete
                if hessian_i is None or any(entry is None for row in hessian_i for entry in row):
                    
                    # Store the new BFGS iterate Hessian approximation
                    hessian_i = copy.deepcopy(self._hessianapproximation_localequalityconstraints[i].get_matrix().tolist())
                
                hessians_complete.append(hessian_i)
        
        return hessians_complete
    
    def evaluate_Hessian_LocalInequalityConstraints(self) -> List[List[List[float]] | None]:
        """Evaluate the Hessians of all local inequality constraints.

        - If the user-provided Hessian for a constraint is complete, this will be used
        - Else, the BFGS-approximation of the Hessian of that inequality constraint

        Returns:
            List of complete Hessian matrices, one per inequality constraint.
        """
        
        # User provided Hessians of the local inequality constraints
        hessians_localinequalityconstraints: List[List[List[float | None]]] | None = self.evaluate_Hessian_InequalityLocalConstraints()
        
        hessians_complete: List[List[List[float]]] = []
        
        # Check if the local inequality constraints exist / local BFGS approximation objects are initialized
        if self._hessianapproximation_localinequalityconstraints is not None:
            
            # Get the local design variables
            designvariables: List[float] = copy.copy(self._designvariables)
            
            # Get the Jacobian of the local inequality constraints once
            # Since this function is only called after evaluateAllJacobians was called,
            # the right hand side is not None
            # No copy wrapper needed - getter already returns copy.deepcopy()
            jacobian_localinequalityconstraints: List[List[float | None]] = self._optimdata.get_Jacobian_LocalInequalityConstraints()
            
            for i in range(len(self._hessianapproximation_localinequalityconstraints)):
                
                # Since BFGS update depends on the previous BFGS approximations over multiple iterations, 
                # and it could happen that the user provided a Hessian for one iteration, but could not 
                # provide for the other iteration (meaning that the BFGS approximation needs to be used then), 
                # we need to carry out the BFGS update in every iteration
                
                # Get the gradient of this inequality constraint (row of the Jacobian)
                # No copy.copy() needed - jacobian_localinequalityconstraints is already a deepcopy from the getter
                gradient_i: List[float | None] = jacobian_localinequalityconstraints[i]
                    
                # Update the Hessian via BFGS
                self._hessianapproximation_localinequalityconstraints[i].updateHessianApproximation(designvariables, gradient_i)
                
                # Extract the user-provided Hessian for this constraint
                hessian_i: List[List[float | None]] | None = None
                if hessians_localinequalityconstraints is not None:
                    hessian_i = hessians_localinequalityconstraints[i]
                    
                # Check if the user-provided Hessian is incomplete
                if hessian_i is None or any(entry is None for row in hessian_i for entry in row):
                    
                    # Store the new BFGS iterate Hessian approximation
                    hessian_i = copy.deepcopy(self._hessianapproximation_localinequalityconstraints[i].get_matrix().tolist())
                
                hessians_complete.append(hessian_i)
        
        return hessians_complete
    
    def evaluate_Complete_Hessian_MappedResponses(self) -> List[List[List[List[float]]] | None]:
        """Compute the Hessians of the mapped responses for each local-to-local coupling.

        Returns:
            Hessian matrices per coupling, None if no mapped responses.
        """
        
        # User provided Hessians of the mapped responses
        hessians_mappedresponses: List[List[List[List[float | None]]]] | None = self.evaluate_Hessians_MappedResponses()
        
        # hessians_complete is indexed by position in couplingparameters (same as couplingparameters[j]).
        # Entries are None for controller couplings or local couplings without mapped responses.
        hessians_complete: List[List[List[List[float]]] | None] = []
        
        # Get couplingparameters
        couplingparameters: List[CouplingParametersInterface] = self.get_CouplingParameters()
        
        # Index helper, since the lists couplingparameters 
        # and hessians_mappedresponses are not aligned
        # NOTE: Notice that no entry exists for the controller
        # That's why in loops where we loop over the couplingparameters
        # and BFGS objects, there is an additional 'index_helper' 
        # so that while the controller is skipped over in couplingparameters, 
        # the loop over the BFGS objects works correctly
        # Example: couplingparameter = (1, C, 2), but mappedresponsehessians = (None, BFGS_1)
        index_helper: int = 0
        
        # Loop over all couplings i <-> j
        for j in range(len(couplingparameters)):
            
            coupling: CouplingParametersInterface = couplingparameters[j]
            id_j: str = coupling.get_ID()
            
            # Check if the subsystem is a local subsystem
            if isinstance(coupling, LocalCouplingParametersALADIN):
        
                # Check if the mapped responses exist / local BFGS approximation objects are initialized
                if self._hessianapproximation_mappedresponses[index_helper] is not None:
                    
                    # Initialize the inner list for this coupling's Hessians
                    hessians_complete_j: List[List[List[float]]] = []
                    
                    # Get the local design variables
                    designvariables: List[float] = copy.copy(self._designvariables)
                    
                    # Get the Jacobian of the mapped response once
                    # Since this function is only called after evaluateAllJacobians was called,
                    # the right hand side is not None
                    jacobian_mappedresponse: List[List[float]] = copy.copy(self._optimdata.get_Jacobian_MappedResponse(id_j))
                    
                    for index in range(len(self._hessianapproximation_mappedresponses[index_helper])):
                        
                        # Since BFGS update depends on the previous BFGS approximations over multiple iterations, 
                        # and it could happen that the user provided a Hessian for one iteration, but could not 
                        # provide for the other iteration (meaning that the BFGS approximation needs to be used then), 
                        # we need to carry out the BFGS update in every iteration
                        
                        # Get the gradient of this mapped response (row of the Jacobian)
                        gradient_index: List[float] = copy.copy(jacobian_mappedresponse[index])
                        
                        # Update the Hessian via BFGS
                        self._hessianapproximation_mappedresponses[index_helper][index].updateHessianApproximation(designvariables, gradient_index)
                        
                        # Extract the user-provided Hessian for this constraint
                        hessian_index: List[List[float | None]] | None = None
                        if hessians_mappedresponses is not None and hessians_mappedresponses[index_helper] is not None:
                            hessian_index = hessians_mappedresponses[index_helper][index]
                        
                        # Check if the user-provided Hessian is complete
                        if hessian_index is None or any(entry is None for row in hessian_index for entry in row):
                            
                            # Store the new BFGS iterate Hessian approximation
                            hessian_index = copy.deepcopy(self._hessianapproximation_mappedresponses[index_helper][index].get_matrix().tolist())
                        
                        hessians_complete_j.append(hessian_index)
                    
                    hessians_complete.append(hessians_complete_j)
                
                else:
                    # Mapped responses for this coupling do not exist
                    hessians_complete.append(None)
                    
                # Update the auxiliary counter
                index_helper += 1
                
        return hessians_complete
        
#############################################################################################################
#   Functions to handle reference data provided by user used to perform algorithm analysis
#############################################################################################################
    
###############################################################################################################
#   Functions to handle coupling parameters related to modelling a distributed optimization problem.
#   This only works on mappedresponses, couplingvariables, shareddesignvariables, targetshareddesignvariables
#   and their copy_-counterparts.
#   Nothing related to coupling parameters
###############################################################################################################
 
    def return_initialized_CouplingParameters(self) -> List[LocalToController_CouplingParametersALADIN | LocalCouplingParametersALADIN]:
        """Return a fresh set of initialized coupling parameters for this subsystem.

        Returns:
            Fresh coupling parameters, one per neighbor.
        """

        initialized_couplingparameters: List[LocalCouplingParametersALADIN] = [LocalCouplingParametersALADIN(self.get_CouplingParameters()[i].get_ID()) 
                                                                               for i in range(len(self.get_CouplingParameters())) 
                                                                               if isinstance(self.get_CouplingParameters()[i], LocalCouplingParametersALADIN)]
        
        # Append controller coupling parameters
        
        # Instantiate new controller coupling parameters object
        localtocontroller_couplingparameters: LocalToController_CouplingParametersALADIN = LocalToController_CouplingParametersALADIN()
        
        # Get neighborid to loop over neighbors of i
        neighborid: List[str] = self.get_NeighborId()
        
        # Initialize LocalToLocalForController_CouplingParameters for each i (current subsystem) <-> j coupling
        localtocontroller_couplingparameters.set_LocalToLocalForController_CouplingParameters([LocalToLocalForController_CouplingParameters(id=j) for j in neighborid])

        # Add control coupling parameters object to local coupling parameters list
        initialized_couplingparameters.append(localtocontroller_couplingparameters)

        return initialized_couplingparameters
    
########################################################################################################
#   Functions to handle coupling parameters
#######################################################################################################

    def initializeCouplingParameters_before_CopyToMiddleLevel(self) -> None:
        """Initialize coupling parameters before copying communicated information from neighboring subsystem.

        Create empty placeholders for coupling parameters, i.e. communicated quantities in the algorithms, 
        Lagrange multipliers, penalty weights, ...
        The sizes are read by already initialized quantities from the inner loop iteration
        """
        
        # proximal matrix and nu: user-specified via updatecouplingparametermethod_outerloop
        self._updatecouplingparametermethod_outerloop.initialize_ProximalParameters(self)
 
    
        # The options are: 
        # - exception_strategy: Defines how to proceed when the curvature condition is violated. 
        #                       Set it to ‘skip_update’ to just skip the update. 
        #                       Or, alternatively, set it to ‘damp_update’ to interpolate between the actual BFGS result and the unmodified matrix. 
        #                       Both exceptions strategies are explained in 
        #                       "Nocedal, Jorge, and Stephen J. Wright. “Numerical optimization” Second Edition (2006).", p. 538-539
        # - min_curvature:      This number, scaled by a normalization factor, defines the minimum curvature dot(delta_grad, delta_x) allowed to go 
        #                       unaffected by the exception strategy. 
        #                       By default is equal to 1e-8 when exception_strategy = 'skip_update' and 
        #                       equal to 0.2 when exception_strategy = 'damp_update'.
        # - init_scale: 'auto' -> This is an entry point for the future to use some Hessian 
        #                         approximation like e.g. via finite differences for the init
        
        # Compute the primal dimension, i.e. dimension of the designvariables
        primal_dimension: int = len(self.get_DesignVariables())
        
        # Check if the local objective exists
        if self.get_LocalObjectiveValue() is not None:
            
            # Initialize the BFGS object
            self._hessianapproximation_localobjective = HessianApproximationBFGS(exception_strategy='damp_update', 
                                                                                 min_curvature=0.2, 
                                                                                 init_scale='auto')
            self._hessianapproximation_localobjective.initialize(n=primal_dimension, approx_type='hess')
            
        # Check if the local equality constraints exist
        if self.get_EqualityLocalConstraintsValue() is not None:
            
            # Count the number of local equality constraints
            number_localequalityconstraints: int = len(self.get_EqualityLocalConstraintsValue())
            
            # Initialize empty list
            self._hessianapproximation_localequalityconstraints = []
            
            # Loop over the local equality constraints
            for i in range(number_localequalityconstraints):
                
                # Create new BFGS object
                localequalityconstraint_hessian_BFGS = HessianApproximationBFGS(exception_strategy='damp_update', 
                                                                                min_curvature=0.2, 
                                                                                init_scale='auto')
                
                # Initialize internal matrix representation of BFGS approximation
                localequalityconstraint_hessian_BFGS.initialize(n=primal_dimension, approx_type='hess')
                
                # Add the BFGS object to the list of Hessian approximations of the local equality constraints
                self._hessianapproximation_localequalityconstraints.append(localequalityconstraint_hessian_BFGS)
            
        # Check if the local inequality constraints exist
        if self.get_InequalityLocalConstraintsValue() is not None:
            
            # Count the number of local inequality constraints
            number_localinequalityconstraints: int = len(self.get_InequalityLocalConstraintsValue())
            
            # Initialize empty list
            self._hessianapproximation_localinequalityconstraints = []
            
            # Loop over the local inequality constraints
            for i in range(number_localinequalityconstraints):
                
                # Create new BFGS object
                localinequalityconstraint_hessian_BFGS = HessianApproximationBFGS(exception_strategy='damp_update', 
                                                                                  min_curvature=0.2, 
                                                                                  init_scale='auto')
                
                # Initialize internal matrix representation of BFGS approximation
                localinequalityconstraint_hessian_BFGS.initialize(n=primal_dimension, approx_type='hess')
                
                # Add the BFGS object to the list of Hessian approximations of the local inequality constraints
                self._hessianapproximation_localinequalityconstraints.append(localinequalityconstraint_hessian_BFGS)
        
        # Initialize Hessian objects for mapped responses
        # NOTE: Notice that no entry exists for the controller
        # That's why in loops where we loop over the couplingparameters
        # and BFGS objects, there is an additional 'index_helper' 
        # so that while the controller is skipped over in couplingparameters, 
        # the loop over the BFGS objects works correctly
        # Example: couplingparameter = (1, C, 2), but mappedresponsehessians = (None, BFGS_1)
            
        # Get the couplingparameters
        couplingparameters: List[CouplingParametersInterface] = self.get_CouplingParameters()
        
        # Initialize empty list; there exists at least one couplingparameter by assumption
        self._hessianapproximation_mappedresponses = []
        
        # Loop over all couplingparameters to check if the mapped response exists
        for i in range(len(couplingparameters)):
            
            # Get the corresponding coupling parameter
            couplingparameter: CouplingParametersInterface = couplingparameters[i]
            
            # Create object that stores the Hessian approximation objects, if mapped responses exist
            hessianapproximation_mappedresponse: List[HessianApproximationBFGS] | None = None 
            
            # Check if the coupling parameter is of local <-> local type 
            # and there is a mapped response in the corresponding coupling
            
            # Check if it is a local subsystem
            if isinstance(couplingparameter, LocalCouplingParametersALADIN): 
                
                if couplingparameter.get_MappedResponses() is not None:
                
                    # Initialize empty list for this specific i -> j coupling
                    hessianapproximation_mappedresponse: List[HessianApproximationBFGS] = [] 

                    # Get the mapped response values
                    mapped_response: List[float] = couplingparameter.get_MappedResponses()
                    
                    # Loop over all components of the mapped responses
                    for j in range(len(mapped_response)):
                    
                        # Create a new BFGS object
                        mappedresponses_hessian_BFGS: HessianApproximationBFGS = HessianApproximationBFGS(exception_strategy="damp_update", 
                                                                                                        min_curvature=0.2, 
                                                                                                        init_scale='auto')

                        # Initialize internal matrix representation of BFGS approximation
                        mappedresponses_hessian_BFGS.initialize(n=primal_dimension, approx_type="hess")
                        
                        # Add the BFGS object to the list of Hessian approximations of the mapped response 
                        # components associated to i -> j
                        hessianapproximation_mappedresponse.append(mappedresponses_hessian_BFGS)
                        
                # Add the list of Hessian approximations of all components w.r.t. 
                # the fixed  i -> j coupling to the list of all Hessian approximations
                # of all local <-> local coupling parameters
                # if there is such a mapped response
                    
                self._hessianapproximation_mappedresponses.append(hessianapproximation_mappedresponse)

        
        # For homogenity, synchronize the local to controller coupling parameters,
        # although no impact
        self.synchronize_AllLocalGlobalCouplingParameters()
    
    def initializeCouplingParameters_after_CopyFromMiddleLevel(self) -> None:
        """Initialize coupling parameters after copying communicated information from neighboring subsystems.

        Create empty placeholders for coupling parameters, i.e. communicated quantities in the algorithms, 
        Lagrange multipliers, penalty weights, ...
        The sizes are read by already initialized quantities from the inner loop iteration
        """
        coupling: List[LocalToController_CouplingParametersALADIN | LocalCouplingParametersALADIN] = self.get_CouplingParameters()

        for j in range(len(coupling)):
            # Only for local subsystems, the following coupling parameters are computed
            if isinstance(coupling[j], LocalCouplingParametersALADIN):
                neighborid: str = coupling[j].get_ID()
                # initialize the coupling-variable coupling parameters
                if ((coupling[j].get_CouplingVariable() is not None) and \
                        (coupling[j].get_Copy_MappedResponses() is not None)):
                    initpenaltyr: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialWeight()] * len(coupling[j].get_CouplingVariable())
                    initmultiplr: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialMultiplier()] * len(coupling[j].get_CouplingVariable())
                    self.set_CoordinationWeights_CopyMappedResponse_Minus_CouplingVariable(neighborid, initpenaltyr)
                    self.set_CoordinationMultipliers_CopyMappedResponse_Minus_CouplingVariable(neighborid, initmultiplr)
                    
                if ((coupling[j].get_Copy_CouplingVariable() is not None) and \
                        (coupling[j].get_MappedResponses() is not None)):
                    # initialize the mapped-response coupling parameters
                    initpenaltyl: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialWeight()] * len(coupling[j].get_MappedResponses())
                    initmultipll: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialMultiplier()] * len(coupling[j].get_MappedResponses())
                    self.set_CoordinationWeights_MappedResponse_Minus_CopyCouplingVariable(neighborid, initpenaltyl)
                    self.set_CoordinationMultipliers_MappedResponse_Minus_CopyCouplingVariable(neighborid, initmultipll)
                    
                if ((coupling[j].get_Copy_TargetSharedDesignVariables() is not None) and \
                        (coupling[j].get_SharedDesignVariables() is not None)):
                    # initialize the shared-design-variable coupling parameters
                    initpenaltysd: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialWeight()] * len(coupling[j].get_SharedDesignVariables())
                    initmultiplsd: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialMultiplier()] * len(coupling[j].get_SharedDesignVariables())
                    self.set_CoordinationWeights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(neighborid, initpenaltysd)
                    self.set_CoordinationMultipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(neighborid, initmultiplsd)
                    
                if ((coupling[j].get_Copy_SharedDesignVariables() is not None) and \
                        (coupling[j].get_TargetSharedDesignVariables() is not None)):
                    # initialize the target-shared-design-variable coupling parameters
                    initpenaltyst: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialWeight()] * len(coupling[j].get_TargetSharedDesignVariables())
                    initmultiplst: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialMultiplier()] * len(coupling[j].get_TargetSharedDesignVariables())
                    self.set_CoordinationWeights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(neighborid, initpenaltyst)
                    self.set_CoordinationMultipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(neighborid, initmultiplst)
                
        # Synchronize LocalToController coupling parameters
        self.synchronize_AllLocalGlobalCouplingParameters()
        
    def initializeCouplingParameters_after_Second_CopyFromMiddleLevel(self) -> None:
        """Initialize the rest of the coupling parameters by solving the controller QP in ALADIN.
        """
        
        # Create new objects for the BFGS approximation objects
        # Since, the ones initialized before used the non-optimal initial 
        # designvariables to update the BFGS approximation
        # Hence, now, the BFGS objects are reset such that 
        # they only reflect points deirved from an optimization
        
        # The options for the BFGS objects are: 
        # - exception_strategy: Defines how to proceed when the curvature condition is violated. 
        #                       Set it to ‘skip_update’ to just skip the update. 
        #                       Or, alternatively, set it to ‘damp_update’ to interpolate between the actual BFGS result and the unmodified matrix. 
        #                       Both exceptions strategies are explained in 
        #                       "Nocedal, Jorge, and Stephen J. Wright. “Numerical optimization” Second Edition (2006).", p. 538-539
        # - min_curvature:      This number, scaled by a normalization factor, defines the minimum curvature dot(delta_grad, delta_x) allowed to go 
        #                       unaffected by the exception strategy. 
        #                       By default is equal to 1e-8 when exception_strategy = 'skip_update' and 
        #                       equal to 0.2 when exception_strategy = 'damp_update'.
        # - init_scale: 'auto' -> This is an entry point for the future to use some Hessian 
        #                         approximation like e.g. via finite differences for the init
        
        # Compute the primal dimension, i.e. dimension of the designvariables
        primal_dimension: int = len(self.get_DesignVariables())
        
        # Check if the local objective exists
        if self.get_LocalObjectiveValue() is not None:
            
            # Initialize the BFGS object
            self._hessianapproximation_localobjective = HessianApproximationBFGS(exception_strategy='damp_update', min_curvature=0.2, init_scale='auto')
            self._hessianapproximation_localobjective.initialize(n=primal_dimension, approx_type='hess')
            
        # Check if the local equality constraints exist
        if self.get_EqualityLocalConstraintsValue() is not None:
            
            # Count the number of local equality constraints
            number_localequalityconstraints: int = len(self.get_EqualityLocalConstraintsValue())
            
            # Initialize empty list
            self._hessianapproximation_localequalityconstraints = []
            
            # Loop over the local equality constraints
            for i in range(number_localequalityconstraints):
                
                # Create new BFGS object
                localequalityconstraint_hessian_BFGS = HessianApproximationBFGS(exception_strategy='damp_update', min_curvature=0.2, init_scale='auto')
                
                # Initialize internal matrix representation of BFGS approximation
                localequalityconstraint_hessian_BFGS.initialize(n=primal_dimension, approx_type='hess')
                
                # Add the BFGS object to the list of Hessian approximations of the local equality constraints
                self._hessianapproximation_localequalityconstraints.append(localequalityconstraint_hessian_BFGS)
            
        # Check if the local inequality constraints exist
        if self.get_InequalityLocalConstraintsValue() is not None:
            
            # Count the number of local inequality constraints
            number_localinequalityconstraints: int = len(self.get_InequalityLocalConstraintsValue())
            
            # Initialize empty list
            self._hessianapproximation_localinequalityconstraints = []
            
            # Loop over the local inequality constraints
            for i in range(number_localinequalityconstraints):
                
                # Create new BFGS object
                localinequalityconstraint_hessian_BFGS = HessianApproximationBFGS(exception_strategy='damp_update', min_curvature=0.2, init_scale='auto')
                
                # Initialize internal matrix representation of BFGS approximation
                localinequalityconstraint_hessian_BFGS.initialize(n=primal_dimension, approx_type='hess')
                
                # Add the BFGS object to the list of Hessian approximations of the local inequality constraints
                self._hessianapproximation_localinequalityconstraints.append(localinequalityconstraint_hessian_BFGS)
        
        # The Hessian approximations for mapped responses
        # Get the couplingparameters
        couplingparameters: List[CouplingParametersInterface] = self.get_CouplingParameters()
        
        # Initialize empty list; there exists at least one couplingparameter by assumption
        self._hessianapproximation_mappedresponses = []
        
        # Loop over all couplingparameters to check if the mapped response exists
        for i in range(len(couplingparameters)):
            
            # Get the corresponding coupling parameter
            couplingparameter: CouplingParametersInterface = couplingparameters[i]
            
            # Create object that stores the Hessian approximation objects, if mapped responses exist
            hessianapproximation_mappedresponse: List[HessianApproximationBFGS] | None = None 
            
            # Check if the coupling parameter is of local <-> local type
            # NOTE: Notice that no entry exists for the controller in BFGS mapped response objects
            # That's why in loops where we loop over the couplingparameters
            # and BFGS objects, there is an additional 'index_helper' 
            # so that while the controller is skipped over in couplingparameters, 
            # the loop over the BFGS objects works correctly
            # Example: couplingparameter = (1, C, 2), but mappedresponsehessians = (None, BFGS_1)
            if isinstance(couplingparameter, LocalCouplingParametersALADIN):
                
                # Initialize veriable for hessians of mapped responses
                hessianapproximation_mappedresponse: List[HessianApproximationBFGS] | None = None
                
                # Check if there is a mapped response in the corresponding coupling
                if couplingparameter.get_MappedResponses() is not None:
                    
                    # Initialize empty list for this specific i -> j coupling
                    hessianapproximation_mappedresponse: List[HessianApproximationBFGS] = [] 

                    # Get the mapped response values
                    mapped_response: List[float] = couplingparameter.get_MappedResponses()
                    
                    # Loop over all components of the mapped responses
                    for j in range(len(mapped_response)):
                    
                        # Create a new BFGS object
                        mappedresponses_hessian_BFGS: HessianApproximationBFGS = HessianApproximationBFGS(exception_strategy="damp_update", 
                                                                                                          min_curvature=0.2, 
                                                                                                          init_scale='auto')

                        # Initialize internal matrix representation of BFGS approximation
                        mappedresponses_hessian_BFGS.initialize(n=primal_dimension, approx_type="hess")
                        
                        # Add the BFGS object to the list of Hessian approximations of the mapped response 
                        # components associated to i -> j
                        hessianapproximation_mappedresponse.append(mappedresponses_hessian_BFGS)
                
                # Add the list of Hessian approximations of all components w.r.t. 
                # the fixed  i -> j coupling to the list of all Hessian approximations
                # of all local <-> local coupling parameters
                # if there is such a mapped response
                    
                self._hessianapproximation_mappedresponses.append(hessianapproximation_mappedresponse)
        
        # Synchronize coupling parameters
        self.synchronize_AllLocalGlobalCouplingParameters()
        
                
    def prepare_updateCouplingParameters(self) -> None:
        """Synchronize all coupling parameters to controller.
        """
        
        # Update of _d_hat
        
        # Get controller coupling
        localtocontroller_couplingparameters: LocalToController_CouplingParametersALADIN = self.get_LocalToController_CouplingParameters()
        
        # Get delta_d
        copy_delta_d: List[float] = localtocontroller_couplingparameters.get_Copy_Delta_D()
        
        # Get designvariables
        original_designvariables: List[float] = self.get_DesignVariables()
        
        # Get the scaled bounds
        scaled_lowerbounds: List[float] = self._optimdata.get_LowerBounds_Scaled()
        scaled_upperbounds: List[float] = self._optimdata.get_UpperBounds_Scaled()
        
        # Compute d_hat
        d_hat: List[float] = [original_designvariables[i] + copy_delta_d[i] for i in range(len(original_designvariables))]
        
        # ALADIN needs to update d_hat, which is stored in controller coupling parameters
        localtocontroller_couplingparameters.set_D_hat(d_hat)
        
        # Update the subsystem and its physical responses for d_hat, 
        # which by the clipping are enforced to be within the scaled bounds        
        self.updateSubsystem(d_hat)
        
        # Store mapped responses and coupling quantities evaluated at d_hat 
        # into the d_hat fields of the local <-> local coupling parameters
        
        # Get the coupling parameters
        couplings: List[LocalToController_CouplingParametersALADIN | LocalCouplingParametersALADIN] = self.get_CouplingParameters()
        
        # loop over all the coupling circles/neighbors
        for j in range(len(couplings)):
            
            # Get the coupling
            coupling: LocalToController_CouplingParametersALADIN | LocalCouplingParametersALADIN = couplings[j]
            
            if isinstance(coupling, LocalCouplingParametersALADIN):
                    
                # mapped-response part of the couplng circle
                if ((coupling.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable() is not None) and (self._inconsistencies[j].get_MappedResponse_Minus_CopyCouplingVariable() is not None)):
                    coupling.set_MappedResponses_D_Hat(copy.copy(coupling.get_MappedResponses()))

                # coupling-variable part of the couplng circle
                if ((coupling.get_Multipliers_CopyMappedResponse_Minus_CouplingVariable() is not None) and (self._inconsistencies[j].get_CopyMappedResponse_Minus_CouplingVariable() is not None)):
                    coupling.set_CouplingVariable_D_Hat(copy.copy(coupling.get_CouplingVariable()))
                
                # shared-design-variable part of the couplng circle
                if ((coupling.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable() is not None) and (self._inconsistencies[j].get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable() is not None)):
                    coupling.set_SharedDesignVariables_D_Hat(copy.copy(coupling.get_SharedDesignVariables())) 
                
                # target-shared-design-variable part of the couplng circle
                if ((coupling.get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable() is not None) and (self._inconsistencies[j].get_CopySharedDesignVariable_Minus_TargetSharedDesignVariable() is not None)):
                    coupling.set_TargetSharedDesignVariables_D_Hat(copy.copy(coupling.get_TargetSharedDesignVariables()))
                    
        
        # Update the subsystem using optimdata
        self.updateSubsystemfromOptimdata(self.get_OptimData())
        
        self.synchronize_AllLocalGlobalCouplingParameters()
    
    def updateCouplingParameters_innerLoop(self) -> None:
        """Update coupling parameters in the inner loop.

        In ALADIN, empty, but synchronize.
        """
        self.synchronize_AllLocalGlobalCouplingParameters()
    
    def updateCouplingParameters_outerLoop(self) -> None:
        """Update coupling parameters during outer loop iteration.
        """
        
        # Dual multipliers w.r.t. d_hat
        
        # NOTE: ALADIN has no weights update, hence, inconsistencies are not needed
        # inconsistencies_previous_outerloop_itr: List[InConsistencySizeInterface] = self.copy_Inconsistencies_Previous_outerloop_itr(elementhistory=elementhistory, 
        #                                                                                                                            outerloop_itr=outerloop_itr)
        # Get the couplings
        couplings: List[LocalToController_CouplingParametersALADIN | LocalCouplingParametersALADIN] = self.get_CouplingParameters()
        
        # loop over all the coupling circles/neighbors
        for j in range(len(couplings)):
            
            # Get the coupling
            coupling: LocalToController_CouplingParametersALADIN | LocalCouplingParametersALADIN = couplings[j]
            
            if isinstance(coupling, LocalCouplingParametersALADIN):
                # get the identifier of the neighboring subsystem
                neighborid: str = coupling.get_ID()
                    
                # mapped-response part of the coupling circle
                if ((coupling.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable() is not None) and (self._inconsistencies[j].get_MappedResponse_Minus_CopyCouplingVariable() is not None)):
                    multipliersin: List[float] = coupling.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable()
                    penaltyweightsin: List[float] = coupling.get_Weights_MappedResponse_Minus_CopyCouplingVariable()
                    
                    mappedresponses_d_hat: List[float] = coupling.get_MappedResponses_D_Hat()
                    copy_couplingvariables_d_hat: List[float] = coupling.get_Copy_CouplingVariable_D_Hat()
                    
                    # Coupling inconsistencies w.r.t to d_hat
                    modified_inconsistency: List[float] = [mappedresponses_d_hat[i] - copy_couplingvariables_d_hat[i] for i in range(len(mappedresponses_d_hat))]
      
                    # update coordination multipliers using d_hat-inconsistencies (see ALADIN)
                    self._updatecouplingparametermethod_outerloop.update_CoordinationMultipliers(multipliersin, penaltyweightsin, modified_inconsistency)
                    self.set_CoordinationMultipliers_MappedResponse_Minus_CopyCouplingVariable(neighborid, multipliersin)
                    
                    # NOTE: ALADIN has no weights update, so the following code does not do any operation:
                    self._updatecouplingparametermethod_outerloop.update_CoordinationWeights(penaltyweightsin)
                    self.set_CoordinationWeights_MappedResponse_Minus_CopyCouplingVariable(neighborid, penaltyweightsin)

                # coupling-variable part of the coupling circle
                if ((coupling.get_Multipliers_CopyMappedResponse_Minus_CouplingVariable() is not None) and (self._inconsistencies[j].get_CopyMappedResponse_Minus_CouplingVariable() is not None)):
                    multipliersin: List[float] = coupling.get_Multipliers_CopyMappedResponse_Minus_CouplingVariable()
                    penaltyweightsin: List[float] = coupling.get_Weights_CopyMappedResponse_Minus_CouplingVariable()
                    
                    couplingvariable_d_hat: List[float] = coupling.get_CouplingVariable_D_Hat()
                    copy_mappedresponses_d_hat: List[float] = coupling.get_Copy_MappedResponses_D_Hat()
                    
                    # Coupling inconsistencies w.r.t. d_hat
                    modified_inconsistency: List[float] = [copy_mappedresponses_d_hat[i] - couplingvariable_d_hat[i] for i in range(len(couplingvariable_d_hat))]
         
                    # update coordination multipliers using d_hat-inconsistencies (see ALADIN)
                    self._updatecouplingparametermethod_outerloop.update_CoordinationMultipliers(multipliersin, penaltyweightsin, modified_inconsistency)
                    self.set_CoordinationMultipliers_CopyMappedResponse_Minus_CouplingVariable(neighborid, multipliersin)
                    
                    # NOTE: ALADIN has no weights update, so the following code does not do any operation:
                    self._updatecouplingparametermethod_outerloop.update_CoordinationWeights(penaltyweightsin)      
                    self.set_CoordinationWeights_CopyMappedResponse_Minus_CouplingVariable(neighborid, penaltyweightsin)
                
                # shared-design-variable part of the coupling circle
                if ((coupling.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable() is not None) and (self._inconsistencies[j].get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable() is not None)):
                    multipliersin: List[float] = coupling.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable()
                    penaltyweightsin: List[float] = coupling.get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable()
                    
                    shareddesignvariables_d_hat: List[float] = coupling.get_SharedDesignVariables_D_Hat()
                    copy_targetshareddesignvariables_d_hat: List[float] = coupling.get_Copy_TargetSharedDesignVariables_D_Hat()
                    
                    # Coupling inconsistencies w.r.t d_hat
                    modified_inconsistency: List[float] = [shareddesignvariables_d_hat[i] - copy_targetshareddesignvariables_d_hat[i] for i in range(len(shareddesignvariables_d_hat))]
                    
                    # update coordination multipliers using d_hat-inconsistencies (see ALADIN)
                    self._updatecouplingparametermethod_outerloop.update_CoordinationMultipliers(multipliersin, penaltyweightsin, modified_inconsistency)
                    self.set_CoordinationMultipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(neighborid, multipliersin)
                    
                    # NOTE: ALADIN has no weights update, so the following code does not do any operation:
                    self._updatecouplingparametermethod_outerloop.update_CoordinationWeights(penaltyweightsin)      
                    self.set_CoordinationWeights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(neighborid, penaltyweightsin)
                
                # target-shared-design-variable part of the coupling circle
                if ((coupling.get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable() is not None) and (self._inconsistencies[j].get_CopySharedDesignVariable_Minus_TargetSharedDesignVariable() is not None)):
                    multipliersin: List[float] = coupling.get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable()
                    penaltyweightsin: List[float] = coupling.get_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable()
                    
                    targetshareddesignvariables_d_hat: List[float] = coupling.get_TargetSharedDesignVariables_D_Hat()
                    copy_shareddesignvariables_d_hat: List[float] = coupling.get_Copy_SharedDesignVariables_D_Hat()
                    
                    # Coupling inconsistencies w.r.t d_hat
                    modified_inconsistency: List[float] = [copy_shareddesignvariables_d_hat[i] - targetshareddesignvariables_d_hat[i] for i in range(len(targetshareddesignvariables_d_hat))]
                 
                    # update coordination multipliers using d_hat-inconsistencies (see ALADIN)
                    self._updatecouplingparametermethod_outerloop.update_CoordinationMultipliers(multipliersin, penaltyweightsin, modified_inconsistency)
                    self.set_CoordinationMultipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(neighborid, multipliersin)
                    
                    # NOTE: ALADIN has no weights update, so the following code does not do any operation:
                    self._updatecouplingparametermethod_outerloop.update_CoordinationWeights(penaltyweightsin)      
                    self.set_CoordinationWeights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(neighborid, penaltyweightsin)
        
        # Update proximal term parameters \nu and \Sigma
        self._updatecouplingparametermethod_outerloop.update_Proximal_nu()
        self._updatecouplingparametermethod_outerloop.update_Proximal_Sigma_i() 
        
        # Synchronize with controller coupling parameters
        self.synchronize_AllLocalGlobalCouplingParameters()
    
    def updateSubsystem(self, perturbed_designvariables: List[float]) -> None:
        """Update the subsystem based on the inputted design variables.

        Args:
            perturbed_designvariables: Design variables to evaluate the subsystem at.
        """
        
        self.set_DesignVariables(perturbed_designvariables)
        self.evaluateTotalObjective()
        self.evaluateTotalConstraint()
    
    def evaluate_Inconsistencies(self) -> None:
        """Compute the difference between stored coupling and mapped variables.

        Compared to the latest available data from a subsystem.
        It returns a matrix containing three vectors. The first row vector are the mapped-response side differences of
        the coupling circle. The second row vector returns differences of the coupling-variable side of the coupling circle.
        The third row returns the difference between the shared design variable vector.
        """
        
        # Regular nonconsensus inconsistency, so, reference to LocalSubSystemBasis.
        # The base class already filters by isinstance(couplingsubsystem, SubSysCouplingParametersBasis),
        # which skips LocalToController_CouplingParametersALADIN (inherits from LocalToController_CouplingParametersBasis).
        super().evaluate_Inconsistencies()
        
    def return_initialized_Inconsistencies(self) -> List[InConsistencySize]:
        """Return a fresh set of initialized inconsistency objects.

        Returns:
            One inconsistency object per coupling parameter.
        """
        initialized_inconsistencies: List[InConsistencySize] = [InConsistencySize(self.get_CouplingParameters()[i].get_ID())
                                                                for i in range(len(self.get_CouplingParameters()))]
        return initialized_inconsistencies
    
    def set_CoordinationMultipliers_MappedResponse_Minus_CopyCouplingVariable(self, neighborid: str, multipliersin: List[float]) -> None:
        """Set coordination multipliers for the mapped response minus copied coupling variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            multipliersin: List of multiplier values to set.
        """
        # set coordination multipliers
        # No copy.copy() wrapper needed - setter creates its own defensive copy
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                couplingparameter.set_Multipliers_MappedResponse_Minus_CopyCouplingVariable(multipliersin)
                break

    def set_CoordinationMultipliers_CopyMappedResponse_Minus_CouplingVariable(self, neighborid: str, multipliersin: List[float]) -> None:
        """Set coordination multipliers for the copied mapped response minus coupling variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            multipliersin: List of multiplier values to set.
        """
        # set coordination multipliers
        # No copy.copy() wrapper needed - setter creates its own defensive copy
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                couplingparameter.set_Multipliers_CopyMappedResponse_Minus_CouplingVariable(multipliersin)
                break
                
    def set_CoordinationMultipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, neighborid: str, multipliersin: List[float]) -> None:
        """Set coordination multipliers for the shared design variable minus copied target shared design variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            multipliersin: List of multiplier values to set.
        """
        # set coordination multipliers
        # No copy.copy() wrapper needed - setter creates its own defensive copy
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                couplingparameter.set_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(multipliersin)
                break

    def set_CoordinationMultipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self, neighborid: str, multipliersin: List[float]) -> None:
        """Set coordination multipliers for the copied shared design variable minus target shared design variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            multipliersin: List of multiplier values to set.
        """
        # set coordination multipliers
        # No copy.copy() wrapper needed - setter creates its own defensive copy
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                couplingparameter.set_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(multipliersin)
                break
                
    def set_CoordinationWeights_MappedResponse_Minus_CopyCouplingVariable(self, neighborid: str, penaltyweightsin: List[float]) -> None:
        """Set coordination weights for the mapped response minus copied coupling variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            penaltyweightsin: List of penalty weight values to set.
        """
        # set coordination weights
        # No copy.copy() wrapper needed - setter creates its own defensive copy
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                couplingparameter.set_Weights_MappedResponse_Minus_CopyCouplingVariable(penaltyweightsin)
                break

    def set_CoordinationWeights_CopyMappedResponse_Minus_CouplingVariable(self, neighborid: str, penaltyweightsin: List[float]) -> None:
        """Set coordination weights for the copied mapped response minus coupling variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            penaltyweightsin: List of penalty weight values to set.
        """
        # set coordination weights
        # No copy.copy() wrapper needed - setter creates its own defensive copy
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                couplingparameter.set_Weights_CopyMappedResponse_Minus_CouplingVariable(penaltyweightsin)
                break
                
    def set_CoordinationWeights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, neighborid: str, penaltyweightsin: List[float]) -> None:
        """Set coordination weights for the shared design variable minus copied target shared design variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            penaltyweightsin: List of penalty weight values to set.
        """
        # set coordination weights
        # No copy.copy() wrapper needed - setter creates its own defensive copy
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                couplingparameter.set_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(penaltyweightsin)
                break

    def set_CoordinationWeights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self, neighborid: str, penaltyweightsin: List[float]) -> None:
        """Set coordination weights for the copied shared design variable minus target shared design variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            penaltyweightsin: List of penalty weight values to set.
        """
        # set coordination weights
        # No copy.copy() wrapper needed - setter creates its own defensive copy
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                couplingparameter.set_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(penaltyweightsin)
                break
    
########################################################################################################
#   Update State Function necessary for running multiprocessing
########################################################################################################
    def update_state(self, other_subsystem: 'LocalSubSystemALADIN') -> None:
        """Update the state of this LocalSubSystemALADIN instance with values from another instance.

        This method is necessary for multiprocessing. When subsystems are executed in parallel
        using multiprocessing.Pool, they are serialized and deserialized, creating new objects
        in separate memory spaces. After parallel execution completes, this method updates
        the original object's attribute values while preserving their memory addresses.

        The update preserves memory addresses by modifying attribute contents in-place where
        possible, rather than reassigning references. This is essential for maintaining object
        identity across the multiprocessing boundary.

        Args:
            other_subsystem: The source LocalSubSystemALADIN containing updated values
                from parallel execution.
        """
        # Update attributes inherited from LocalSubSystemBasis (and transitively SubSystemBasis)
        # This already handles: _couplingparameters, _local_convergenceindicator_innerloop,
        # _local_convergenceindicator_outerloop, _updatecouplingparametermethod_outerloop,
        # _inconsistencies, and all other parent attributes
        super().update_state(other_subsystem)

        # Update LocalSubSystemALADIN-specific attributes (in __init__ order)

        # No copy.copy() needed - float is a primitive/immutable type
        self._nu: float | None = other_subsystem._nu

        # Update nested list in-place to preserve memory addresses
        other_sigma_i: List[List[float]] | None = other_subsystem.get_Sigma_i()
        if other_sigma_i is None:
            self._sigma_i: List[List[float]] | None = None
        else:
            if self._sigma_i is None:
                # No copy.deepcopy() needed - getter already returns a deep copy
                self._sigma_i = other_sigma_i
            else:
                for index in range(len(other_sigma_i)):
                    self._sigma_i[index] = update_state_listprimitive(self._sigma_i[index], other_sigma_i[index])

        # We use copy.deepcopy instead of update_state, differening from general rule of update_state, 
        # since the internal state of the super class of HessianApproximationBFGS, namely scipy.BFGS, 
        # does not have such a method and therefore is not well exposed
        
        # copy.deepcopy() creates a deep copy
        self._hessianapproximation_localobjective: HessianApproximationBFGS | None = copy.deepcopy(other_subsystem.get_HessianApproximation_LocalObjective())

        other_hessianapproximations_localequalityconstraints: List[HessianApproximationBFGS] | None = other_subsystem.get_HessianApproximation_LocalEqualityConstraints()
        if other_hessianapproximations_localequalityconstraints is None:
            self._hessianapproximation_localequalityconstraints: List[HessianApproximationBFGS] | None = None
        else:
            if self._hessianapproximation_localequalityconstraints is None:
                # copy.deepcopy() creates a deep copy of the list container
                self._hessianapproximation_localequalityconstraints = copy.deepcopy(other_hessianapproximations_localequalityconstraints)
            else:
                for i in range(len(other_hessianapproximations_localequalityconstraints)):
                    self._hessianapproximation_localequalityconstraints[i] = copy.deepcopy(other_hessianapproximations_localequalityconstraints[i])

        other_hessianapproximations_localinequalityconstraints: List[HessianApproximationBFGS] | None = other_subsystem.get_HessianApproximation_LocalInequalityConstraints()
        if other_hessianapproximations_localinequalityconstraints is None:
            self._hessianapproximation_localinequalityconstraints: List[HessianApproximationBFGS] | None = None
        else:
            if self._hessianapproximation_localinequalityconstraints is None:
                # copy.deepcopy() creates a deep copy of the list container
                self._hessianapproximation_localinequalityconstraints = copy.deepcopy(other_hessianapproximations_localinequalityconstraints)
            else:
                for i in range(len(other_hessianapproximations_localinequalityconstraints)):
                    self._hessianapproximation_localinequalityconstraints[i] = copy.deepcopy(other_hessianapproximations_localinequalityconstraints[i])
            
        # Hessian approximations of mapped responses
        other_hessianapproximations_mappedresponses = other_subsystem.get_HessianApproximation_MappedResponses()
        
        if other_hessianapproximations_mappedresponses is None:
            self._hessianapproximation_mappedresponses = None
        else:
            
            # Check if self._hessianapproximation_mappedresponses is None
            if self._hessianapproximation_mappedresponses is None:
                
                # Deep-copy the other hessian approximations of the mapped responses
                self._hessianapproximation_mappedresponses = copy.deepcopy(other_hessianapproximations_mappedresponses)
            
            # Both are not None
            else:
                
                for i in range(len(other_hessianapproximations_mappedresponses)):
                    
                    # Check if the i-th entry is None
                    if other_hessianapproximations_mappedresponses[i] is None:
                        
                        self._hessianapproximation_mappedresponses[i] = None
                        
                    else:
                        
                        for j in range(len(other_hessianapproximations_mappedresponses[i])):
                            
                            self._hessianapproximation_mappedresponses[i][j] = copy.deepcopy(other_hessianapproximations_mappedresponses[i][j])
                
                
            
        
