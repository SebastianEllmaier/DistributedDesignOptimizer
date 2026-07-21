# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Local -> Controller coupling parameters module.

This module provides coupling parameters for the local subsystems 
regarding data communicated to ALADIN controller subsystem.
"""

import copy
from typing import List
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive
from Distributed_Design_Optimizer.subsystem.couplingparameters import LocalToController_CouplingParametersBasis
from Distributed_Design_Optimizer.subsystem.couplingparameters.aladin import LocalToLocalForController_CouplingParameters
from Distributed_Design_Optimizer.middlelevel.aladin import (ControllerToLocal_MiddleLevelCouplingALADIN,
                                                             LocalToController_MiddleLevelCouplingALADIN
                                                             )


class LocalToController_CouplingParametersALADIN(LocalToController_CouplingParametersBasis):
    """Coupling parameters for the ALADIN controller subsystem.

    Extends LocalToController_CouplingParametersBasis with delta_d, d_hat, Hessians,
    gradients, Jacobians of active constraints/bounds, equality constraints,
    and per-coupling local-to-controller / controller-to-local sub-parameters.
    """

    def __init__(self) -> None:
        """Initialize LocalToController_CouplingParametersALADIN."""
        super().__init__()
        
        # ALADIN Update coupling information for controller of ALADIN, e.g. auxiliary variables 
        # (from CouplingsParametersBasis.py, it is inherited as designvariables) and jacobian,...
        self._copy_delta_d: List[float] | None = None
        
        # The quantity d_hat build out of delta_d
        self._d_hat: List[float] | None = None
        
        # Hessian needed for controller QP problem
        self._hessian_localconstraints_lagrangian: List[List[float]] | None = None
        
        # Gradient of f
        self._gradient_localobjective: List[float] | None = None
        
        # List of local inequality values
        self._localinequalityconstraintsvalue: List[float] | None = None
        
        # Jacobian of local inequality constraints
        self._jacobian_localinequalityconstraints: List[List[float]] | None = None
        
        # List of lower bound constraint values
        self._lower_boundconstraints_value: List[float] | None = None
        
        # Jacobian of lower bounds
        self._jacobian_lowerbound: List[List[float]] | None = None
        
        # List of upper bound constraint values
        self._upper_boundconstraints_value: List[float] | None = None
        
        # Jacobian of upper bounds
        self._jacobian_upperbound: List[List[float]] | None = None
        
        # Jacobian of equality constraints
        self._jacobian_localequalityconstraints: List[List[float]] | None = None
        
        # Subinformation that is stored for i <-> j couplings, where the direction is local -> controller
        self._localtolocalforcontroller_couplingparameters: List[LocalToLocalForController_CouplingParameters] | None = None
        
        # Subinformation that is stored for i <-> j couplings, where the direction is controller -> local
        # There is no such exchange in ALADIN, hence, it is omitted
    
    def set_Copy_Delta_D(self, copy_delta_d_in: List[float]) -> None:
        """Set the copy of the delta_d variables.

        Args:
            copy_delta_d_in: The copy of the delta_d variables to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_delta_d = copy.copy(copy_delta_d_in)

    def get_Copy_Delta_D(self) -> List[float] | None:
        """Get the copy of the delta_d variables.

        Returns:
            The copy of the delta_d variables, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_delta_d)

    def set_D_hat(self, d_hat_in: List[float]) -> None:
        """Set the d_hat variables.

        Args:
            d_hat_in: The d_hat variables to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._d_hat = copy.copy(d_hat_in)

    def get_D_hat(self) -> List[float] | None:
        """Get the d_hat variables.

        Returns:
            The d_hat variables, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._d_hat)
    
    def set_Hessian_LocalConstraints_Lagrangian(self, hessian_localconstraints_lagrangian_in: List[List[float]]) -> None:
        """Set the Hessian of the Lagrangian w.r.t. local constraints needed for the controller QP problem.

        Args:
            hessian_localconstraints_lagrangian_in: The Hessian to set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._hessian_localconstraints_lagrangian = copy.deepcopy(hessian_localconstraints_lagrangian_in)

    def get_Hessian_LocalConstraints_Lagrangian(self) -> List[List[float]] | None:
        """Get the Hessian of the Lagrangian w.r.t. local constraints needed for the controller QP problem.

        Returns:
            The Hessian of the Lagrangian w.r.t. local constraints, or None if not set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._hessian_localconstraints_lagrangian)
    
    def set_Gradient_LocalObjective(self, gradient_localobjective_in: List[float]) -> None:
        """Set the gradient of the local objective function.

        Args:
            gradient_localobjective_in: The gradient of the local objective function to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._gradient_localobjective = copy.copy(gradient_localobjective_in)

    def get_Gradient_LocalObjective(self) -> List[float] | None:
        """Get the gradient of the local objective function.

        Returns:
            The gradient of the local objective function, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._gradient_localobjective)
    
    def set_LocalInequalityConstraintsValue(self, localinequalityconstraintsvalue_in: List[float]) -> None:
        """Set the local inequality constraint values.

        Args:
            localinequalityconstraintsvalue_in: The local inequality constraint values to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._localinequalityconstraintsvalue = copy.copy(localinequalityconstraintsvalue_in)

    def get_LocalInequalityConstraintsValue(self) -> List[float] | None:
        """Get the local inequality constraint values.

        Returns:
            The local inequality constraint values, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._localinequalityconstraintsvalue)

    def set_Lower_BoundConstraints_Value(self, lower_boundconstraints_value_in: List[float]) -> None:
        """Set the lower bound constraint values.

        Args:
            lower_boundconstraints_value_in: The lower bound constraint values to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._lower_boundconstraints_value = copy.copy(lower_boundconstraints_value_in)

    def get_Lower_BoundConstraints_Value(self) -> List[float] | None:
        """Get the lower bound constraint values.

        Returns:
            The lower bound constraint values, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._lower_boundconstraints_value)

    def set_Upper_BoundConstraints_Value(self, upper_boundconstraints_value_in: List[float]) -> None:
        """Set the upper bound constraint values.

        Args:
            upper_boundconstraints_value_in: The upper bound constraint values to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._upper_boundconstraints_value = copy.copy(upper_boundconstraints_value_in)

    def get_Upper_BoundConstraints_Value(self) -> List[float] | None:
        """Get the upper bound constraint values.

        Returns:
            The upper bound constraint values, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._upper_boundconstraints_value)

    def set_Jacobian_LocalInequalityConstraints(self, jacobian_localinequalityconstraints_in: List[List[float]]) -> None:
        """Set the Jacobian of the local inequality constraints.

        Args:
            jacobian_localinequalityconstraints_in: The Jacobian to set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_localinequalityconstraints = copy.deepcopy(jacobian_localinequalityconstraints_in)

    def get_Jacobian_LocalInequalityConstraints(self) -> List[List[float]] | None:
        """Get the Jacobian of the local inequality constraints.

        Returns:
            The Jacobian of the local inequality constraints, or None if not set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_localinequalityconstraints)
        
    def set_Jacobian_LowerBound(self, jacobian_lowerbound_in: List[List[float]]) -> None:
        """Set the Jacobian of the lower bounds of the subsystem's design variables.

        Args:
            jacobian_lowerbound_in: The Jacobian of the lower bounds to set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_lowerbound = copy.deepcopy(jacobian_lowerbound_in)

    def get_Jacobian_LowerBound(self) -> List[List[float]] | None:
        """Get the Jacobian of the lower bounds of the subsystem's design variables.

        Returns:
            The Jacobian of the lower bounds, or None if not set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_lowerbound)
        
    def set_Jacobian_UpperBound(self, jacobian_upperbound_in: List[List[float]]) -> None:
        """Set the Jacobian of the upper bounds of the subsystem's design variables.

        Args:
            jacobian_upperbound_in: The Jacobian of the upper bounds to set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_upperbound = copy.deepcopy(jacobian_upperbound_in)

    def get_Jacobian_UpperBound(self) -> List[List[float]] | None:
        """Get the Jacobian of the upper bounds of the subsystem's design variables.

        Returns:
            The Jacobian of the upper bounds, or None if not set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_upperbound)
        
    def set_Jacobian_LocalEqualityConstraints(self, jacobian_equalityconstraints_in: List[List[float]]) -> None:
        """Set the Jacobian of the equality constraints.

        Args:
            jacobian_equalityconstraints_in: The Jacobian of the equality constraints to set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_localequalityconstraints = copy.deepcopy(jacobian_equalityconstraints_in)

    def get_Jacobian_LocalEqualityConstraints(self) -> List[List[float]] | None:
        """Get the Jacobian of the equality constraints.

        Returns:
            The Jacobian of the equality constraints, or None if not set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_localequalityconstraints)
    
    def set_LocalToLocalForController_CouplingParameters(self, localtocontroller_couplingparametersin: List[LocalToLocalForController_CouplingParameters]) -> None:
        """Set the local-to-controller coupling parameters for each i <-> j coupling.

        Args:
            localtocontroller_couplingparametersin: The list of local-to-controller coupling parameters to set.
        """
        # No copy.copy() used - List[LocalToLocalForController_CouplingParameters] is a list of class objects
        # assigned by reference intentionally. This allows the caller to continue interacting with
        # the actual objects. If isolation is needed, the caller should explicitly copy.
        self._localtolocalforcontroller_couplingparameters = localtocontroller_couplingparametersin

    def get_LocalToLocalForController_CouplingParameters(self) -> List[LocalToLocalForController_CouplingParameters] | None:
        """Get the local-to-controller coupling parameters for each i <-> j coupling.

        Returns:
            The local-to-controller coupling parameters, or None if not set.
        """
        # No copy.copy() used - List[LocalToLocalForController_CouplingParameters] is a list of class objects
        # returned by reference intentionally. This allows the caller to interact with the actual
        # objects. If isolation is needed, the caller should explicitly copy.
        return self._localtolocalforcontroller_couplingparameters     
    
    def CopyToMiddleLevel_LocalToLocalForController_CouplingParameters(self, localtocontroller_couplingparameter: LocalToLocalForController_CouplingParameters, 
                                                              middlelevel_localtocontroller_couplingparameter: LocalToLocalForController_CouplingParameters) -> None:
        """Update a local-to-controller coupling parameter in the middlelevel coupling.

        Args:
            localtocontroller_couplingparameter: The source local-to-controller coupling parameter.
            middlelevel_localtocontroller_couplingparameter: The middle level coupling parameter to update.
        """
        
        # Local subsystem communicates every part of LocalToLocalForController_CouplingParameters
        # Hence, it copies every attribute to the middlelevel coupling parameters
        
        # No copy.copy()/copy.deepcopy() wrapper needed here - the getter methods in
        # LocalToLocalForController_CouplingParameters already return defensive copies, and the
        # setter methods also create defensive copies of the input.
        
        # Mapped responses parts
        if localtocontroller_couplingparameter.get_MappedResponses() is not None:
            middlelevel_localtocontroller_couplingparameter.set_MappedResponses(localtocontroller_couplingparameter.get_MappedResponses())
        
        if localtocontroller_couplingparameter.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable() is not None:
            middlelevel_localtocontroller_couplingparameter.set_Multipliers_MappedResponse_Minus_CopyCouplingVariable(localtocontroller_couplingparameter.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable())
        
        if localtocontroller_couplingparameter.get_Weights_MappedResponse_Minus_CopyCouplingVariable() is not None:
            middlelevel_localtocontroller_couplingparameter.set_Weights_MappedResponse_Minus_CopyCouplingVariable(localtocontroller_couplingparameter.get_Weights_MappedResponse_Minus_CopyCouplingVariable())
        
        if localtocontroller_couplingparameter.get_JacobianMappedResponses() is not None:
            middlelevel_localtocontroller_couplingparameter.set_JacobianMappedResponses(localtocontroller_couplingparameter.get_JacobianMappedResponses())
            
        if localtocontroller_couplingparameter.get_HessiansMappedResponses() is not None:
            middlelevel_localtocontroller_couplingparameter.set_HessiansMappedResponses(localtocontroller_couplingparameter.get_HessiansMappedResponses())
                
        # Coupling variables part
        if localtocontroller_couplingparameter.get_CouplingVariables() is not None:
            middlelevel_localtocontroller_couplingparameter.set_CouplingVariables(localtocontroller_couplingparameter.get_CouplingVariables())
        
        if localtocontroller_couplingparameter.get_Multipliers_CopyMappedResponse_Minus_CouplingVariable() is not None:
            middlelevel_localtocontroller_couplingparameter.set_Multipliers_CopyMappedResponse_Minus_CouplingVariable(localtocontroller_couplingparameter.get_Multipliers_CopyMappedResponse_Minus_CouplingVariable())
        
        if localtocontroller_couplingparameter.get_Weights_CopyMappedResponse_Minus_CouplingVariable() is not None:
            middlelevel_localtocontroller_couplingparameter.set_Weights_CopyMappedResponse_Minus_CouplingVariable(localtocontroller_couplingparameter.get_Weights_CopyMappedResponse_Minus_CouplingVariable())
        
        # Shared design variables part
        if localtocontroller_couplingparameter.get_SharedDesignVariables() is not None:
            middlelevel_localtocontroller_couplingparameter.set_SharedDesignVariables(localtocontroller_couplingparameter.get_SharedDesignVariables())
        
        if localtocontroller_couplingparameter.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable() is not None:
            middlelevel_localtocontroller_couplingparameter.set_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(localtocontroller_couplingparameter.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
        
        if localtocontroller_couplingparameter.get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable() is not None:
            middlelevel_localtocontroller_couplingparameter.set_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(localtocontroller_couplingparameter.get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
        
        # Target shared design variables
        if localtocontroller_couplingparameter.get_TargetSharedDesignVariables() is not None:
            middlelevel_localtocontroller_couplingparameter.set_TargetSharedDesignVariables(localtocontroller_couplingparameter.get_TargetSharedDesignVariables())
        
        if localtocontroller_couplingparameter.get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable() is not None:
            middlelevel_localtocontroller_couplingparameter.set_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(localtocontroller_couplingparameter.get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable())
        
        if localtocontroller_couplingparameter.get_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable() is not None:
            middlelevel_localtocontroller_couplingparameter.set_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(localtocontroller_couplingparameter.get_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable())
        
        # Indices of coupling, shared and target shared variables in total designvariables vector of local subsystem
        if localtocontroller_couplingparameter.get_Indices_CouplingVariables_In_DesignVariables() is not None:
            middlelevel_localtocontroller_couplingparameter.set_Indices_CouplingVariables_In_DesignVariables(localtocontroller_couplingparameter.get_Indices_CouplingVariables_In_DesignVariables())
            
        if localtocontroller_couplingparameter.get_Indices_SharedDesignVariables_In_DesignVariables() is not None:
            middlelevel_localtocontroller_couplingparameter.set_Indices_SharedDesignVariables_In_DesignVariables(localtocontroller_couplingparameter.get_Indices_SharedDesignVariables_In_DesignVariables())
            
        if localtocontroller_couplingparameter.get_Indices_TargetSharedDesignVariables_In_DesignVariables() is not None:
            middlelevel_localtocontroller_couplingparameter.set_Indices_TargetSharedDesignVariables_In_DesignVariables(localtocontroller_couplingparameter.get_Indices_TargetSharedDesignVariables_In_DesignVariables())
        
    def CopyFromMiddleLevelCoupling(self, middlelevelcouplingIn: ControllerToLocal_MiddleLevelCouplingALADIN) -> None:
        """Copy coupling parameters from the middle level.

        Args:
            middlelevelcouplingIn: The middle level coupling to copy from.

        Raises:
            ValueError: If middlelevelcouplingIn is not a ControllerToLocal or LocalToController MiddleLevelCouplingALADIN instance.
        """
        if not isinstance(middlelevelcouplingIn, ControllerToLocal_MiddleLevelCouplingALADIN):
            raise ValueError(f"{DDO_Color}%%% Error in LocalToController_CouplingParametersALADIN.CopyFromMiddleLevelCoupling(): type of MiddleLevelCoupling is not matching.{Reset}")
            
        # ALADIN_specific data

        # Delta_d
        # No copy.copy() wrapper needed - get_Delta_D() already returns a defensive copy,
        # and set_Copy_Delta_D() also creates a defensive copy of the input.
        if middlelevelcouplingIn.get_Delta_D() is not None:
            self.set_Copy_Delta_D(middlelevelcouplingIn.get_Delta_D())
            
            
    def CopyToMiddleLevelCoupling(self, middlelevelcouplingIn: LocalToController_MiddleLevelCouplingALADIN) -> None:
        """Copy coupling parameters to the middle level.

        Args:
            middlelevelcouplingIn: The middle level coupling to copy to.

        Raises:
            ValueError: If middlelevelcouplingIn is not a LocalToController or ControllerToLocal MiddleLevelCouplingALADIN instance.
        """
        if not isinstance(middlelevelcouplingIn, LocalToController_MiddleLevelCouplingALADIN):
            raise ValueError(f"{DDO_Color}%%% Error in LocalToController_CouplingParametersALADIN.CopyToMiddleLevelCoupling(): type of MiddleLevelCoupling is not matching.{Reset}")
            
        # ALADIN-specific data
        
        # Local -> controller
        
        # Perspective of local subsystem
            
        # Coupling parameters
            
        # Includes coupling parameters like e.g. mapped responses of (i,j)-coupling, local -> controller 
        localtocontroller_couplingparameters: List[LocalToLocalForController_CouplingParameters] = self.get_LocalToLocalForController_CouplingParameters()
            
        # Get reference pointers of middlelevel controller to local to controller couplingparameters to update each entry
        middlelevel_localtocontroller_couplingparameters: List[LocalToLocalForController_CouplingParameters] = middlelevelcouplingIn.get_LocalToLocalForController_CouplingParameters()
            
        if localtocontroller_couplingparameters is not None:

            # Loop over every coupling parameter between controller and local subsystem
            for i in range(len(localtocontroller_couplingparameters)):
                    
                # Update each subsystem object of the list from local subsystem / controller to middle level
                if isinstance(localtocontroller_couplingparameters[i], LocalToLocalForController_CouplingParameters):
                    self.CopyToMiddleLevel_LocalToLocalForController_CouplingParameters(localtocontroller_couplingparameters[i], middlelevel_localtocontroller_couplingparameters[i])
                        
        # If middlelevel coupling goes to controller
        # No copy.deepcopy() wrapper needed - the getter methods in LocalToController_CouplingParametersALADIN
        # already return defensive copies, and the setter methods in LocalToController_MiddleLevelCouplingALADIN
        # also create defensive copies of the input.
        if self.get_Hessian_LocalConstraints_Lagrangian() is not None:
            middlelevelcouplingIn.set_Hessian_LocalConstraints_Lagrangian(self.get_Hessian_LocalConstraints_Lagrangian())
        
        if self.get_Gradient_LocalObjective() is not None:
            middlelevelcouplingIn.set_Gradient_LocalObjective(self.get_Gradient_LocalObjective())
        
        if self.get_Jacobian_LocalInequalityConstraints() is not None:
            
            # Get Jacobian entries corresponding to local inequality constraints
            jacobian_localinequalityconstraints: List[List[float]] = self.get_Jacobian_LocalInequalityConstraints()
            
            # NOTE: Code commented out which would filter out the Jacobians of inactive constraints
            # Need to implement self._getActiveLocalInequalityConstraints and introduce 
            # different fields for that
            
            # localinequalityconstraints: List[bool] = self.get_ActiveInequalityConstraints()
            
            # jacobian_localinequalityconstraints_filtered: List[List[float | None]] = []
            
            # for i in range(len(localinequalityconstraints)):
                
            #     # Initialize new gradient for asscoiated i-th local inequality
            #     gradient_localinequalityconstraint_i: List[float | None] = []
                
            #     if localinequalityconstraints[i] is True:
                    
            #         gradient_localinequalityconstraint_i = jacobian_alllocalinequalityconstraints[i]
                
            #     else:
                    
            #         gradient_localinequalityconstraint_i = [None for j in range(primal_dimension)]
                
            #     # Append either the full gradient or the filtered out gradient
            #     jacobian_localinequalityconstraints_filtered.append(gradient_localinequalityconstraint_i)
                
            # # Communicate the filtered Jacobian of the local inequality constraints
            
            # Communicate the Jacobian
            middlelevelcouplingIn.set_Jacobian_LocalInequalityConstraints(jacobian_localinequalityconstraints)
        
        if self.get_LocalInequalityConstraintsValue() is not None:
            middlelevelcouplingIn.set_LocalInequalityConstraintsValue(self.get_LocalInequalityConstraintsValue())
            
        if self.get_Jacobian_LowerBound() is not None:
            
            # Get Jacobian entries corresponding to lower bounds
            jacobian_lowerbounds: List[List[float]] = self.get_Jacobian_LowerBound()
            
            # NOTE: Code commented out which would filter out the Jacobians of inactive bounds
            # Need to implement self._getActiveLowerBounds and introduce 
            # different fields for that
            # activelowerbounds: List[bool] = self.get_ActiveLowerBounds()
            
            # jacobian_activelowerbounds: List[List[float | None]] = []
            
            # for i in range(len(activelowerbounds)):
                
            #     # Initialize new gradient for associated i-th lower bound
            #     gradient_lowerbound_i: List[float | None] = []
                
            #     if activelowerbounds[i] is True:
                    
            #         gradient_lowerbound_i = jacobian_alllowerbounds[i]
                
            #     else:
                    
            #         gradient_lowerbound_i = [None for j in range(primal_dimension)]
                
            #     # Append either the full gradient or the filtered out gradient
            #     jacobian_activelowerbounds.append(gradient_lowerbound_i)
                
            # # Communicate the filtered Jacobian of the active lower bounds
            
            # Communicate the Jacobian
            middlelevelcouplingIn.set_Jacobian_LowerBound(jacobian_lowerbounds)
        
        if self.get_Lower_BoundConstraints_Value() is not None:
            middlelevelcouplingIn.set_Lower_BoundConstraints_Value(self.get_Lower_BoundConstraints_Value())
            
        if self.get_Jacobian_UpperBound() is not None:
            
            # Get Jacobian entries corresponding to upper bounds
            jacobian_upperbounds: List[List[float]] = self.get_Jacobian_UpperBound()
            # activeupperbounds: List[bool] = self.get_ActiveUpperBounds()
            
            # jacobian_activeupperbounds: List[List[float | None]] = []
            
            # for i in range(len(activeupperbounds)):
                
            #     # Initialize new gradient for associated i-th upper bound
            #     gradient_upperbound_i: List[float | None] = []
                
            #     if activeupperbounds[i] is True:
                    
            #         gradient_upperbound_i = jacobian_allupperbounds[i]
                
            #     else:
                    
            #         gradient_upperbound_i = [None for j in range(primal_dimension)]
                    
            #     # Append either the full gradient or the filtered out gradient
            #     jacobian_activeupperbounds.append(gradient_upperbound_i)
                    
            # # Communicate the filtered Jacobian of the active upper bounds
            
            # Communicate the Jacobian
            middlelevelcouplingIn.set_Jacobian_UpperBound(jacobian_upperbounds)
        
        if self.get_Upper_BoundConstraints_Value() is not None:
            middlelevelcouplingIn.set_Upper_BoundConstraints_Value(self.get_Upper_BoundConstraints_Value())
        
        if self.get_Jacobian_LocalEqualityConstraints() is not None:
            middlelevelcouplingIn.set_Jacobian_LocalEqualityConstraints(self.get_Jacobian_LocalEqualityConstraints())
            
            
    def update_state(self, other_coupling: 'LocalToController_CouplingParametersALADIN') -> None:
        """Update the state of this LocalToController_CouplingParametersALADIN with values from another instance.

        This method is necessary for multiprocessing. When subsystems are executed in parallel
        using multiprocessing.Pool, they are serialized and deserialized, creating new objects
        in separate memory spaces. After parallel execution completes, this method updates
        the original object's attribute values while preserving their memory addresses.

        The update preserves memory addresses by modifying list contents in-place rather than
        reassigning references. This is essential for maintaining object identity across the
        multiprocessing boundary.

        Args:
            other_coupling: The source LocalToController_CouplingParametersALADIN containing updated values
                from parallel execution.
        """
        # Call the base class update_state to handle inherited attributes
        super().update_state(other_coupling=other_coupling)
        
        self._copy_delta_d: List[float] | None = update_state_listprimitive(self._copy_delta_d, other_coupling.get_Copy_Delta_D())
        
        self._d_hat: List[float] | None = update_state_listprimitive(self._d_hat, other_coupling.get_D_hat())
        
        other_hessian_localconstraints_lagrangian: List[List[float]] | None = other_coupling.get_Hessian_LocalConstraints_Lagrangian()
        if other_hessian_localconstraints_lagrangian is None:
            self._hessian_localconstraints_lagrangian = None
        elif self._hessian_localconstraints_lagrangian is None:
            self._hessian_localconstraints_lagrangian = other_hessian_localconstraints_lagrangian
        else:
            for i in range(len(other_hessian_localconstraints_lagrangian)):
                self._hessian_localconstraints_lagrangian[i] = update_state_listprimitive(
                    self._hessian_localconstraints_lagrangian[i], other_hessian_localconstraints_lagrangian[i])
        
        self._gradient_localobjective: List[float] | None = update_state_listprimitive(
            self._gradient_localobjective, other_coupling.get_Gradient_LocalObjective())
        
        self._localinequalityconstraintsvalue: List[float] | None = update_state_listprimitive(
            self._localinequalityconstraintsvalue, other_coupling.get_LocalInequalityConstraintsValue())
        
        self._lower_boundconstraints_value: List[float] | None = update_state_listprimitive(
            self._lower_boundconstraints_value, other_coupling.get_Lower_BoundConstraints_Value())
        
        self._upper_boundconstraints_value: List[float] | None = update_state_listprimitive(
            self._upper_boundconstraints_value, other_coupling.get_Upper_BoundConstraints_Value())
        
        other_jacobian_localinequalityconstraints: List[List[float]] | None = other_coupling.get_Jacobian_LocalInequalityConstraints()
        if other_jacobian_localinequalityconstraints is None:
            self._jacobian_localinequalityconstraints = None
        elif self._jacobian_localinequalityconstraints is None:
            self._jacobian_localinequalityconstraints = other_jacobian_localinequalityconstraints
        else:
            for i in range(len(other_jacobian_localinequalityconstraints)):
                self._jacobian_localinequalityconstraints[i] = update_state_listprimitive(
                    self._jacobian_localinequalityconstraints[i], other_jacobian_localinequalityconstraints[i])
                
        other_jacobian_lowerbound: List[List[float]] | None = other_coupling.get_Jacobian_LowerBound()
        if other_jacobian_lowerbound is None:
            self._jacobian_lowerbound = None
        elif self._jacobian_lowerbound is None:
            self._jacobian_lowerbound = other_jacobian_lowerbound
        else:
            for i in range(len(other_jacobian_lowerbound)):
                self._jacobian_lowerbound[i] = update_state_listprimitive(
                    self._jacobian_lowerbound[i], other_jacobian_lowerbound[i])
        
        other_jacobian_upperbound: List[List[float]] | None = other_coupling.get_Jacobian_UpperBound()
        if other_jacobian_upperbound is None:
            self._jacobian_upperbound = None
        elif self._jacobian_upperbound is None:
            self._jacobian_upperbound = other_jacobian_upperbound
        else:
            for i in range(len(other_jacobian_upperbound)):
                self._jacobian_upperbound[i] = update_state_listprimitive(
                    self._jacobian_upperbound[i], other_jacobian_upperbound[i])
                
        other_jacobian_equalityconstraints: List[List[float]] | None = other_coupling.get_Jacobian_LocalEqualityConstraints()
        if other_jacobian_equalityconstraints is None:
            self._jacobian_localequalityconstraints = None
        elif self._jacobian_localequalityconstraints is None:
            self._jacobian_localequalityconstraints = other_jacobian_equalityconstraints
        else:
            for i in range(len(other_jacobian_equalityconstraints)):
                self._jacobian_localequalityconstraints[i] = update_state_listprimitive(
                    self._jacobian_localequalityconstraints[i], other_jacobian_equalityconstraints[i])
        
        other_localtocontroller_couplingparameters: List[LocalToLocalForController_CouplingParameters] | None = other_coupling.get_LocalToLocalForController_CouplingParameters()
        if other_localtocontroller_couplingparameters is None:
            self._localtolocalforcontroller_couplingparameters = None
        elif self._localtolocalforcontroller_couplingparameters is None:
            self._localtolocalforcontroller_couplingparameters = other_localtocontroller_couplingparameters
        else:
            for i in range(len(other_localtocontroller_couplingparameters)):
                self._localtolocalforcontroller_couplingparameters[i].update_state(other_localtocontroller_couplingparameters[i])
        

