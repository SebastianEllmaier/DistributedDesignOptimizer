# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""ALADIN controller coupling parameters module.

This module provides coupling parameters for the ALADIN
controller subsystem.
"""

import copy
from typing import List
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive
from Distributed_Design_Optimizer.subsystem.couplingparameters import ControllerCouplingParametersBasis
from Distributed_Design_Optimizer.subsystem.couplingparameters.aladin import LocalToLocalForController_CouplingParameters
from Distributed_Design_Optimizer.middlelevel.aladin import (ControllerToLocal_MiddleLevelCouplingALADIN,
                                                             LocalToController_MiddleLevelCouplingALADIN
                                                             )


class ControllerCouplingParametersALADIN(ControllerCouplingParametersBasis):
    """Coupling parameters for the ALADIN controller subsystem.

    Extends ControllerCouplingParametersBasis with delta_d, d_hat, Hessians,
    gradients, Jacobians of active constraints/bounds, equality constraints,
    and per-coupling local-to-controller / controller-to-local sub-parameters.
    """

    def __init__(self, id: str) -> None:
        """Initialize ControllerCouplingParametersALADIN.

        Args:
            id: Identifier of the neighboring subsystem.
        """
        super().__init__(id)
        
        # ALADIN Update coupling information for controller of ALADIN, e.g. auxiliary variables 
        # (from CouplingsParametersBasis.py, it is inherited as designvariables) and jacobian,...

        self._delta_d: List[float] | None = None
        
        # Hessian needed for controller QP problem
        self._copy_hessian_localconstraints_lagrangian: List[List[float]] | None = None
        
        # Gradient of f
        self._copy_gradient_localobjective: List[float] | None = None
        
        # List of local inequality constraint values
        self._copy_localinequalityconstraintsvalue: List[float] | None = None
        
        # Jacobian of local inequality constraints
        self._copy_jacobian_localinequalityconstraints: List[List[float]] | None = None
        
        # List of lower bound constraint values
        self._copy_lower_boundconstraints_value: List[float] | None = None
        
        # Jacobian of lower bounds
        self._copy_jacobian_lowerbound: List[List[float]] | None = None
        
        # List of upper bound constraint values
        self._copy_upper_boundconstraints_value: List[float] | None = None
        
        # Jacobian of upper bounds
        self._copy_jacobian_upperbound: List[List[float]] | None = None
        
        # Jacobian of equality constraints
        self._copy_jacobian_localequalityconstraints: List[List[float]] | None = None
        
        # Subinformation that is stored for i <-> j couplings, where the direction is local -> controller
        self._copy_localtolocalforcontroller_couplingparameters: List[LocalToLocalForController_CouplingParameters] | None = None
        
        # Subinformation that is stored for i <-> j couplings, where the direction is controller -> local
        # There is no such exchange in ALADIN, hence, it is omitted
    
    def set_Delta_D(self, delta_d_in: List[float]) -> None:
        """Set the delta_d variables.

        Args:
            delta_d_in: The delta_d variables to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._delta_d = copy.copy(delta_d_in)

    def get_Delta_D(self) -> List[float] | None:
        """Get the delta_d variables.

        Returns:
            The delta_d variables, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._delta_d)
    
    def set_Copy_Hessian_LocalConstraints_Lagrangian(self, copy_hessian_localconstraints_lagrangian_in: List[List[float]]) -> None:
        """Set the copy of the Hessian of the Lagrangian w.r.t. local constraints.

        Args:
            copy_hessian_localconstraints_lagrangian_in: The copy of the Hessian to set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._copy_hessian_localconstraints_lagrangian = copy.deepcopy(copy_hessian_localconstraints_lagrangian_in)

    def get_Copy_Hessian_LocalConstraints_Lagrangian(self) -> List[List[float]] | None:
        """Get the copy of the Hessian of the Lagrangian w.r.t. local constraints.

        Returns:
            The copy of the Hessian of the Lagrangian, or None if not set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._copy_hessian_localconstraints_lagrangian)
    
    def set_Copy_Gradient_LocalObjective(self, copy_gradient_localobjective_in: List[float]) -> None:
        """Set the copy of the gradient of the local objective function.

        Args:
            copy_gradient_localobjective_in: The copy of the gradient to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_gradient_localobjective = copy.copy(copy_gradient_localobjective_in)

    def get_Copy_Gradient_LocalObjective(self) -> List[float] | None:
        """Get the copy of the gradient of the local objective function.

        Returns:
            The copy of the gradient of the local objective function, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_gradient_localobjective)
    
    def set_Copy_LocalInequalityConstraintsValue(self, copy_localinequalityconstraintsvalue_in: List[float]) -> None:
        """Set the copy of the local inequality constraint values.

        Args:
            copy_localinequalityconstraintsvalue_in: The copy of the local inequality constraint values to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_localinequalityconstraintsvalue = copy.copy(copy_localinequalityconstraintsvalue_in)

    def get_Copy_LocalInequalityConstraintsValue(self) -> List[float] | None:
        """Get the copy of the local inequality constraint values.

        Returns:
            The copy of the local inequality constraint values, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_localinequalityconstraintsvalue)

    def set_Copy_Jacobian_LocalInequalityConstraints(self, copy_jacobian_localinequalityconstraints_in: List[List[float]]) -> None:
        """Set the copy of the Jacobian of the local inequality constraints.

        Args:
            copy_jacobian_localinequalityconstraints_in: The copy of the Jacobian to set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._copy_jacobian_localinequalityconstraints = copy.deepcopy(copy_jacobian_localinequalityconstraints_in)

    def get_Copy_Jacobian_LocalInequalityConstraints(self) -> List[List[float]] | None:
        """Get the copy of the Jacobian of the local inequality constraints.

        Returns:
            The copy of the Jacobian of the local inequality constraints, or None if not set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._copy_jacobian_localinequalityconstraints)
        
    def set_Copy_Lower_BoundConstraints_Value(self, copy_lower_boundconstraints_value_in: List[float]) -> None:
        """Set the copy of the lower bound constraint values.

        Args:
            copy_lower_boundconstraints_value_in: The copy of the lower bound constraint values to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_lower_boundconstraints_value = copy.copy(copy_lower_boundconstraints_value_in)

    def get_Copy_Lower_BoundConstraints_Value(self) -> List[float] | None:
        """Get the copy of the lower bound constraint values.

        Returns:
            The copy of the lower bound constraint values, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_lower_boundconstraints_value)

    def set_Copy_Jacobian_LowerBound(self, copy_jacobian_lowerbound_in: List[List[float]]) -> None:
        """Set the copy of the Jacobian of the lower bounds of the subsystem's design variables.

        Args:
            copy_jacobian_lowerbound_in: The copy of the Jacobian to set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._copy_jacobian_lowerbound = copy.deepcopy(copy_jacobian_lowerbound_in)

    def get_Copy_Jacobian_LowerBound(self) -> List[List[float]] | None:
        """Get the copy of the Jacobian of the lower bounds of the subsystem's design variables.

        Returns:
            The copy of the Jacobian of the lower bounds, or None if not set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._copy_jacobian_lowerbound)
        
    def set_Copy_Upper_BoundConstraints_Value(self, copy_upper_boundconstraints_value_in: List[float]) -> None:
        """Set the copy of the upper bound constraint values.

        Args:
            copy_upper_boundconstraints_value_in: The copy of the upper bound constraint values to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_upper_boundconstraints_value = copy.copy(copy_upper_boundconstraints_value_in)

    def get_Copy_Upper_BoundConstraints_Value(self) -> List[float] | None:
        """Get the copy of the upper bound constraint values.

        Returns:
            The copy of the upper bound constraint values, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_upper_boundconstraints_value)

    def set_Copy_Jacobian_UpperBound(self, copy_jacobian_upperbound_in: List[List[float]]) -> None:
        """Set the copy of the Jacobian of the upper bounds of the subsystem's design variables.

        Args:
            copy_jacobian_upperbound_in: The copy of the Jacobian to set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._copy_jacobian_upperbound = copy.deepcopy(copy_jacobian_upperbound_in)

    def get_Copy_Jacobian_UpperBound(self) -> List[List[float]] | None:
        """Get the copy of the Jacobian of the upper bounds of the subsystem's design variables.

        Returns:
            The copy of the Jacobian of the upper bounds, or None if not set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._copy_jacobian_upperbound)
 
    def set_Copy_Jacobian_LocalEqualityConstraints(self, copy_jacobian_equalityconstraints_in: List[List[float]]) -> None:
        """Set the copy of the Jacobian of the equality constraints.

        Args:
            copy_jacobian_equalityconstraints_in: The copy of the Jacobian to set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._copy_jacobian_localequalityconstraints = copy.deepcopy(copy_jacobian_equalityconstraints_in)

    def get_Copy_Jacobian_LocalEqualityConstraints(self) -> List[List[float]] | None:
        """Get the copy of the Jacobian of the equality constraints.

        Returns:
            The copy of the Jacobian of the equality constraints, or None if not set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._copy_jacobian_localequalityconstraints)
        
    def set_Copy_LocalToLocalForController_CouplingParameters(self, copy_localtolocalforcontroller_couplingparametersin: List[LocalToLocalForController_CouplingParameters]) -> None:
        """Set the copy of the local-to-local-for-controller coupling parameters for each i <-> j coupling.

        Args:
            copy_localtolocalforcontroller_couplingparametersin: The copy of the local-to-local-for-controller coupling parameters to set.
        """
        # No copy.copy() used - List[LocalToLocalForController_CouplingParameters] is a list of class objects
        # assigned by reference intentionally. This allows the caller to continue interacting with
        # the actual objects. If isolation is needed, the caller should explicitly copy.
        self._copy_localtolocalforcontroller_couplingparameters = copy_localtolocalforcontroller_couplingparametersin

    def get_Copy_LocalToLocalForController_CouplingParameters(self) -> List[LocalToLocalForController_CouplingParameters] | None:
        """Get the copy of the local-to-local-for-controller coupling parameters for each i <-> j coupling.

        Returns:
            The copy of the local-to-local-for-controller coupling parameters, or None if not set.
        """
        # No copy.copy() used - List[LocalToLocalForController_CouplingParameters] is a list of class objects
        # returned by reference intentionally. This allows the caller to interact with the actual
        # objects. If isolation is needed, the caller should explicitly copy.
        return self._copy_localtolocalforcontroller_couplingparameters
    
        
    def CopyFromMiddleLevel_LocalToLocalForController_CouplingParameters(self, copy_localtolocalforcontroller_couplingparameter: LocalToLocalForController_CouplingParameters, 
                                                                middlelevel_localtolocalforcontroller_couplingparameter: LocalToLocalForController_CouplingParameters) -> None:
        """Update a local-to-local-for-controller coupling parameter from the middlelevel coupling.

        Args:
            copy_localtolocalforcontroller_couplingparameter: The local copy to update.
            middlelevel_localtolocalforcontroller_couplingparameter: The middle level coupling parameter source.
        """
        
        # Local subsystem communicates every part of LocalToLocalForController_CouplingParameters
        # Hence, the controller copies every attribute from the middlelevel coupling parameters
        
        # No copy.copy()/copy.deepcopy() wrapper needed here - the getter methods in
        # LocalToLocalForController_CouplingParameters already return defensive copies, and the
        # setter methods also create defensive copies of the input.
        
        # Mapped responses parts
        if middlelevel_localtolocalforcontroller_couplingparameter.get_MappedResponses() is not None:
            copy_localtolocalforcontroller_couplingparameter.set_MappedResponses(middlelevel_localtolocalforcontroller_couplingparameter.get_MappedResponses())
        
        if middlelevel_localtolocalforcontroller_couplingparameter.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable() is not None:
            copy_localtolocalforcontroller_couplingparameter.set_Multipliers_MappedResponse_Minus_CopyCouplingVariable(middlelevel_localtolocalforcontroller_couplingparameter.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable())
        
        if middlelevel_localtolocalforcontroller_couplingparameter.get_Weights_MappedResponse_Minus_CopyCouplingVariable() is not None:
            copy_localtolocalforcontroller_couplingparameter.set_Weights_MappedResponse_Minus_CopyCouplingVariable(middlelevel_localtolocalforcontroller_couplingparameter.get_Weights_MappedResponse_Minus_CopyCouplingVariable())
        
        if middlelevel_localtolocalforcontroller_couplingparameter.get_JacobianMappedResponses() is not None:
            copy_localtolocalforcontroller_couplingparameter.set_JacobianMappedResponses(middlelevel_localtolocalforcontroller_couplingparameter.get_JacobianMappedResponses())
            
        if middlelevel_localtolocalforcontroller_couplingparameter.get_HessiansMappedResponses() is not None:
            copy_localtolocalforcontroller_couplingparameter.set_HessiansMappedResponses(middlelevel_localtolocalforcontroller_couplingparameter.get_HessiansMappedResponses())
        
        # Coupling variables
        if middlelevel_localtolocalforcontroller_couplingparameter.get_CouplingVariables() is not None:
            copy_localtolocalforcontroller_couplingparameter.set_CouplingVariables(middlelevel_localtolocalforcontroller_couplingparameter.get_CouplingVariables())
        
        if middlelevel_localtolocalforcontroller_couplingparameter.get_Multipliers_CopyMappedResponse_Minus_CouplingVariable() is not None:
            copy_localtolocalforcontroller_couplingparameter.set_Multipliers_CopyMappedResponse_Minus_CouplingVariable(middlelevel_localtolocalforcontroller_couplingparameter.get_Multipliers_CopyMappedResponse_Minus_CouplingVariable())
        
        if middlelevel_localtolocalforcontroller_couplingparameter.get_Weights_CopyMappedResponse_Minus_CouplingVariable() is not None:
            copy_localtolocalforcontroller_couplingparameter.set_Weights_CopyMappedResponse_Minus_CouplingVariable(middlelevel_localtolocalforcontroller_couplingparameter.get_Weights_CopyMappedResponse_Minus_CouplingVariable())
        
        # Shared design variables
        if middlelevel_localtolocalforcontroller_couplingparameter.get_SharedDesignVariables() is not None:
            copy_localtolocalforcontroller_couplingparameter.set_SharedDesignVariables(middlelevel_localtolocalforcontroller_couplingparameter.get_SharedDesignVariables())
        
        if middlelevel_localtolocalforcontroller_couplingparameter.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable() is not None:
            copy_localtolocalforcontroller_couplingparameter.set_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(middlelevel_localtolocalforcontroller_couplingparameter.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
        
        if middlelevel_localtolocalforcontroller_couplingparameter.get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable() is not None:
            copy_localtolocalforcontroller_couplingparameter.set_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(middlelevel_localtolocalforcontroller_couplingparameter.get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
        
        # Target shared design variables
        if middlelevel_localtolocalforcontroller_couplingparameter.get_TargetSharedDesignVariables() is not None:
            copy_localtolocalforcontroller_couplingparameter.set_TargetSharedDesignVariables(middlelevel_localtolocalforcontroller_couplingparameter.get_TargetSharedDesignVariables())
        
        if middlelevel_localtolocalforcontroller_couplingparameter.get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable() is not None:
            copy_localtolocalforcontroller_couplingparameter.set_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(middlelevel_localtolocalforcontroller_couplingparameter.get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable())
        
        if middlelevel_localtolocalforcontroller_couplingparameter.get_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable() is not None:
            copy_localtolocalforcontroller_couplingparameter.set_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(middlelevel_localtolocalforcontroller_couplingparameter.get_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable())
        
        # Indices of coupling, shared and target shared variables in total designvariables vector of local subsystem
        if middlelevel_localtolocalforcontroller_couplingparameter.get_Indices_CouplingVariables_In_DesignVariables() is not None:
            copy_localtolocalforcontroller_couplingparameter.set_Indices_CouplingVariables_In_DesignVariables(middlelevel_localtolocalforcontroller_couplingparameter.get_Indices_CouplingVariables_In_DesignVariables())
            
        if middlelevel_localtolocalforcontroller_couplingparameter.get_Indices_SharedDesignVariables_In_DesignVariables() is not None:
            copy_localtolocalforcontroller_couplingparameter.set_Indices_SharedDesignVariables_In_DesignVariables(middlelevel_localtolocalforcontroller_couplingparameter.get_Indices_SharedDesignVariables_In_DesignVariables())
            
        if middlelevel_localtolocalforcontroller_couplingparameter.get_Indices_TargetSharedDesignVariables_In_DesignVariables() is not None:
            copy_localtolocalforcontroller_couplingparameter.set_Indices_TargetSharedDesignVariables_In_DesignVariables(middlelevel_localtolocalforcontroller_couplingparameter.get_Indices_TargetSharedDesignVariables_In_DesignVariables())
        
        
    def CopyFromMiddleLevelCoupling(self, middlelevelcouplingIn: LocalToController_MiddleLevelCouplingALADIN) -> None:
        """Copy coupling parameters from the middle level.

        Args:
            middlelevelcouplingIn: The middle level coupling to copy from.

        Raises:
            ValueError: If middlelevelcouplingIn is not a LocalToController_MiddleLevelCouplingALADIN instance.
        """
        if not isinstance(middlelevelcouplingIn, LocalToController_MiddleLevelCouplingALADIN):
            raise ValueError(f"{DDO_Color}Error in ControllerCouplingParametersALADIN.CopyFromMiddleLevelCoupling(): type of MiddleLevelCoupling is not matching.{Reset}")
            
        # ALADIN_specific data
            
        # Local -> controller                
        # Perspective of controller subsystem
            
        # Coupling parameters
            
        # Includes coupling parameters like e.g. mapped responses of (i,j)-coupling, local -> controller 
        copy_localtolocalforcontroller_couplingparameters: List[LocalToLocalForController_CouplingParameters] = self.get_Copy_LocalToLocalForController_CouplingParameters()
            
        # Get reference pointers of middlelevel controller to local to controller couplingparameters to update each entry
        middlelevel_localtocontroller_couplingparameters: List[LocalToLocalForController_CouplingParameters] = middlelevelcouplingIn.get_LocalToLocalForController_CouplingParameters()
            
        # If copy_localtolocalforcontroller_couplingparameters is instantiated
        if copy_localtolocalforcontroller_couplingparameters is not None:

            # Loop over every coupling parameter between controller and local subsystem
            for i in range(len(copy_localtolocalforcontroller_couplingparameters)):
                        
                # Update each subsystem object of the list from local subsystem / controller to middle level
                if isinstance(copy_localtolocalforcontroller_couplingparameters[i], LocalToLocalForController_CouplingParameters):
                    self.CopyFromMiddleLevel_LocalToLocalForController_CouplingParameters(copy_localtolocalforcontroller_couplingparameters[i], middlelevel_localtocontroller_couplingparameters[i])
                        
        # If middlelevel coupling comes from the local subsystem
        # No copy.deepcopy() wrapper needed - the getter methods in LocalToController_MiddleLevelCouplingALADIN
        # already return defensive copies, and the setter methods also create defensive copies of the input.
        if middlelevelcouplingIn.get_Hessian_LocalConstraints_Lagrangian() is not None:
            self.set_Copy_Hessian_LocalConstraints_Lagrangian(middlelevelcouplingIn.get_Hessian_LocalConstraints_Lagrangian())
            
        if middlelevelcouplingIn.get_Gradient_LocalObjective() is not None:
            self.set_Copy_Gradient_LocalObjective(middlelevelcouplingIn.get_Gradient_LocalObjective())
            
        if middlelevelcouplingIn.get_Jacobian_LocalInequalityConstraints() is not None:
            self.set_Copy_Jacobian_LocalInequalityConstraints(middlelevelcouplingIn.get_Jacobian_LocalInequalityConstraints())
        
        if middlelevelcouplingIn.get_LocalInequalityConstraintsValue() is not None:
            self.set_Copy_LocalInequalityConstraintsValue(middlelevelcouplingIn.get_LocalInequalityConstraintsValue())
            
        if middlelevelcouplingIn.get_Jacobian_LowerBound() is not None:
            self.set_Copy_Jacobian_LowerBound(middlelevelcouplingIn.get_Jacobian_LowerBound())
        
        if middlelevelcouplingIn.get_Lower_BoundConstraints_Value() is not None:
            self.set_Copy_Lower_BoundConstraints_Value(middlelevelcouplingIn.get_Lower_BoundConstraints_Value())
            
        if middlelevelcouplingIn.get_Jacobian_UpperBound() is not None:
            self.set_Copy_Jacobian_UpperBound(middlelevelcouplingIn.get_Jacobian_UpperBound())
        
        if middlelevelcouplingIn.get_Upper_BoundConstraints_Value() is not None:
            self.set_Copy_Upper_BoundConstraints_Value(middlelevelcouplingIn.get_Upper_BoundConstraints_Value())
            
        if middlelevelcouplingIn.get_Jacobian_LocalEqualityConstraints() is not None:
            self.set_Copy_Jacobian_LocalEqualityConstraints(middlelevelcouplingIn.get_Jacobian_LocalEqualityConstraints())
        
            
    def CopyToMiddleLevelCoupling(self, middlelevelcouplingIn: ControllerToLocal_MiddleLevelCouplingALADIN) -> None:
        """Copy coupling parameters to the middle level.

        Args:
            middlelevelcouplingIn: The middle level coupling to copy to.

        Raises:
            ValueError: If middlelevelcouplingIn is not a ControllerToLocal_MiddleLevelCouplingALADIN instance.
        """
        if not isinstance(middlelevelcouplingIn, ControllerToLocal_MiddleLevelCouplingALADIN):
            raise ValueError(f"{DDO_Color}Error in ControllerCouplingParametersALADIN.CopyToMiddleLevelCoupling(): type of MiddleLevelCoupling is not matching.{Reset}")
            
        # ALADIN-specific data

        # Controller -> local
        
        # Perspective of controller
        
        # Coupling parameters
        
        # No copy.copy() wrapper needed - get_Delta_D() already returns a defensive copy,
        # and set_Delta_D() also creates a defensive copy of the input.
        if self.get_Delta_D() is not None:
            middlelevelcouplingIn.set_Delta_D(self.get_Delta_D())
            
            
    def update_state(self, other_coupling: 'ControllerCouplingParametersALADIN') -> None:
        """Update the state of this ControllerCouplingParametersALADIN with values from another instance.

        This method is necessary for multiprocessing. When subsystems are executed in parallel
        using multiprocessing.Pool, they are serialized and deserialized, creating new objects
        in separate memory spaces. After parallel execution completes, this method updates
        the original object's attribute values while preserving their memory addresses.

        The update preserves memory addresses by modifying list contents in-place rather than
        reassigning references. This is essential for maintaining object identity across the
        multiprocessing boundary.

        Args:
            other_coupling: The source ControllerCouplingParametersALADIN containing updated values
                from parallel execution.
        """
        # Call the base class update_state to handle inherited attributes
        super().update_state(other_coupling=other_coupling)
        
        self._delta_d: List[float] | None = update_state_listprimitive(self._delta_d, other_coupling.get_Delta_D())
        
        other_copy_hessian_localconstraints_lagrangian: List[List[float]] | None = other_coupling.get_Copy_Hessian_LocalConstraints_Lagrangian()
        if other_copy_hessian_localconstraints_lagrangian is None:
            self._copy_hessian_localconstraints_lagrangian = None
        elif self._copy_hessian_localconstraints_lagrangian is None:
            self._copy_hessian_localconstraints_lagrangian = other_copy_hessian_localconstraints_lagrangian
        else:
            for i in range(len(other_copy_hessian_localconstraints_lagrangian)):
                self._copy_hessian_localconstraints_lagrangian[i] = update_state_listprimitive(
                    self._copy_hessian_localconstraints_lagrangian[i], other_copy_hessian_localconstraints_lagrangian[i])
        
        self._copy_gradient_localobjective: List[float] | None = update_state_listprimitive(
            self._copy_gradient_localobjective, other_coupling.get_Copy_Gradient_LocalObjective())
        
        self._copy_localinequalityconstraintsvalue: List[float] | None = update_state_listprimitive(
            self._copy_localinequalityconstraintsvalue, other_coupling.get_Copy_LocalInequalityConstraintsValue())
        
        other_copy_jacobian_localinequalityconstraints: List[List[float]] | None = other_coupling.get_Copy_Jacobian_LocalInequalityConstraints()
        if other_copy_jacobian_localinequalityconstraints is None:
            self._copy_jacobian_localinequalityconstraints = None
        elif self._copy_jacobian_localinequalityconstraints is None:
            self._copy_jacobian_localinequalityconstraints = other_copy_jacobian_localinequalityconstraints
        else:
            for i in range(len(other_copy_jacobian_localinequalityconstraints)):
                self._copy_jacobian_localinequalityconstraints[i] = update_state_listprimitive(
                    self._copy_jacobian_localinequalityconstraints[i], other_copy_jacobian_localinequalityconstraints[i])
        
        self._copy_lower_boundconstraints_value: List[float] | None = update_state_listprimitive(
            self._copy_lower_boundconstraints_value, other_coupling.get_Copy_Lower_BoundConstraints_Value())
                
        other_copy_jacobian_lowerbound: List[List[float]] | None = other_coupling.get_Copy_Jacobian_LowerBound()
        if other_copy_jacobian_lowerbound is None:
            self._copy_jacobian_lowerbound = None
        elif self._copy_jacobian_lowerbound is None:
            self._copy_jacobian_lowerbound = other_copy_jacobian_lowerbound
        else:
            for i in range(len(other_copy_jacobian_lowerbound)):
                self._copy_jacobian_lowerbound[i] = update_state_listprimitive(
                    self._copy_jacobian_lowerbound[i], other_copy_jacobian_lowerbound[i])
        
        self._copy_upper_boundconstraints_value: List[float] | None = update_state_listprimitive(
            self._copy_upper_boundconstraints_value, other_coupling.get_Copy_Upper_BoundConstraints_Value())
        
        other_copy_jacobian_upperbound: List[List[float]] | None = other_coupling.get_Copy_Jacobian_UpperBound()
        if other_copy_jacobian_upperbound is None:
            self._copy_jacobian_upperbound = None
        elif self._copy_jacobian_upperbound is None:
            self._copy_jacobian_upperbound = other_copy_jacobian_upperbound
        else:
            for i in range(len(other_copy_jacobian_upperbound)):
                self._copy_jacobian_upperbound[i] = update_state_listprimitive(
                    self._copy_jacobian_upperbound[i], other_copy_jacobian_upperbound[i])
                
        other_copy_jacobian_equalityconstraints: List[List[float]] | None = other_coupling.get_Copy_Jacobian_LocalEqualityConstraints()
        if other_copy_jacobian_equalityconstraints is None:
            self._copy_jacobian_localequalityconstraints = None
        elif self._copy_jacobian_localequalityconstraints is None:
            self._copy_jacobian_localequalityconstraints = other_copy_jacobian_equalityconstraints
        else:
            for i in range(len(other_copy_jacobian_equalityconstraints)):
                self._copy_jacobian_localequalityconstraints[i] = update_state_listprimitive(
                    self._copy_jacobian_localequalityconstraints[i], other_copy_jacobian_equalityconstraints[i])
        
        other_copy_localtolocalforcontroller_couplingparameters: List[LocalToLocalForController_CouplingParameters] | None = other_coupling.get_Copy_LocalToLocalForController_CouplingParameters()
        if other_copy_localtolocalforcontroller_couplingparameters is None:
            self._copy_localtolocalforcontroller_couplingparameters = None
        elif self._copy_localtolocalforcontroller_couplingparameters is None:
            self._copy_localtolocalforcontroller_couplingparameters = other_copy_localtolocalforcontroller_couplingparameters
        else:
            for i in range(len(other_copy_localtolocalforcontroller_couplingparameters)):
                self._copy_localtolocalforcontroller_couplingparameters[i].update_state(other_copy_localtolocalforcontroller_couplingparameters[i])
        

