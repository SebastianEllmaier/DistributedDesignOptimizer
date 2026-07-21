# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Local-to-controller middle-level coupling module for ALADIN.

This module provides middle-level coupling management for local-to-controller
subsystem communication in ALADIN coordination.
"""

import copy
from typing import List
from Distributed_Design_Optimizer.middlelevel import LocalToController_MiddleLevelCouplingBasis
from Distributed_Design_Optimizer.subsystem.couplingparameters.aladin import LocalToLocalForController_CouplingParameters
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive


class LocalToController_MiddleLevelCouplingALADIN(LocalToController_MiddleLevelCouplingBasis):
    """Middle level coupling updated by the local subsystem.

    Handles the coupling between local subsystems and the controller
    (middlelevel between local subsystem and controller).
    """
    
    def __init__(self, id: str, local_neighbors_list: List[str]) -> None:
        """Initialize local-to-controller middle-level coupling.

        Args:
            id: Identifier for this coupling.
            local_neighbors_list: List of local neighbor identifiers.
        """
        # Call init of LocalToController_MiddleLevelCouplingBasis
        super().__init__(id)
        
        # Hessian needed for controller QP problem
        self._hessian_localconstraints_lagrangian: List[List[float]] | None = None
        
        # Gradient of the local objective
        self._gradient_localobjective: List[float] | None = None
        
        # List of local inequality constraint values
        self._localinequalityconstraintsvalue: List[float] | None = None
        
        # Jacobian of local inequalities
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
        
        # Subinformation that is stored for i <-> j couplings, direction local -> controller
        self._localtolocalforcontroller_couplingparameters: List[LocalToLocalForController_CouplingParameters] = []
        
        # Instantitate each entry
        for neighbor_id in local_neighbors_list:
            # Add new LocalToLocalForController_CouplingParameters object to self._localtolocalforcontroller_couplingparameters
            self._localtolocalforcontroller_couplingparameters.append(LocalToLocalForController_CouplingParameters(id=neighbor_id))
            
    
    # Getters and setters
    
    ###########################################################################
    # Hessian needed for controller QP problem
    ###########################################################################
    
    def get_Hessian_LocalConstraints_Lagrangian(self) -> List[List[float]] | None:
        """Return the Hessian of the Lagrangian w.r.t. local constraints.

        Needed for the controller QP problem.

        Returns:
            List[List[float]] | None: The Hessian matrix or None if not set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._hessian_localconstraints_lagrangian)
    
    def set_Hessian_LocalConstraints_Lagrangian(self, hessian_localconstraintslagrangian_in: List[List[float]]) -> None:
        """Set the Hessian of the Lagrangian w.r.t. local constraints.

        Needed for the controller QP problem.

        Args:
            hessian_localconstraintslagrangian_in (List[List[float]]): The Hessian matrix to set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._hessian_localconstraints_lagrangian = copy.deepcopy(hessian_localconstraintslagrangian_in)
    
    ###########################################################################
    # Gradient of the local objective function
    ###########################################################################
    
    def get_Gradient_LocalObjective(self) -> List[float] | None:
        """Return the gradient of the local objective function.

        Returns:
            List[float] | None: The gradient vector or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._gradient_localobjective)
    
    def set_Gradient_LocalObjective(self, gradient_localobjective_in: List[float]) -> None:
        """Set the gradient of the local objective function.

        Args:
            gradient_localobjective_in (List[float]): The gradient vector to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._gradient_localobjective = copy.copy(gradient_localobjective_in)
    
    ###########################################################################
    # Local inequality constraint values
    ###########################################################################
    
    def get_LocalInequalityConstraintsValue(self) -> List[float] | None:
        """Return the local inequality constraint values.

        Returns:
            List[float] | None: The local inequality constraint values or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._localinequalityconstraintsvalue)
    
    def set_LocalInequalityConstraintsValue(self, localinequalityconstraintvalues_in: List[float]) -> None:
        """Set the local inequality constraint values.

        Args:
            localinequalityconstraintvalues_in (List[float]): The local inequality constraint values to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._localinequalityconstraintsvalue = copy.copy(localinequalityconstraintvalues_in)
    
    ###########################################################################
    # Jacobian of local inequality constraints
    ###########################################################################
    
    def get_Jacobian_LocalInequalityConstraints(self) -> List[List[float]] | None:
        """Return the Jacobian of the local inequality constraints.

        Returns:
            List[List[float]] | None: The Jacobian matrix or None if not set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_localinequalityconstraints)
    
    def set_Jacobian_LocalInequalityConstraints(self, jacobian_localinequalityconstraints_in: List[List[float]]) -> None:
        """Set the Jacobian of the local inequality constraints.

        Args:
            jacobian_localinequalityconstraints_in (List[List[float]]): The Jacobian matrix to set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_localinequalityconstraints = copy.deepcopy(jacobian_localinequalityconstraints_in)
        
    ###########################################################################
    # Lower bound constraint values
    ###########################################################################
    
    def get_Lower_BoundConstraints_Value(self) -> List[float] | None:
        """Return the lower bound constraint values.

        Returns:
            List[float] | None: The lower bound constraint values or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._lower_boundconstraints_value)
    
    def set_Lower_BoundConstraints_Value(self, lower_boundconstraints_value_in: List[float]) -> None:
        """Set the lower bound constraint values.

        Args:
            lower_boundconstraints_value_in (List[float]): The lower bound constraint values to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._lower_boundconstraints_value = copy.copy(lower_boundconstraints_value_in)
    
    ###########################################################################
    # Jacobian of lower bounds
    ###########################################################################
    
    def get_Jacobian_LowerBound(self) -> List[List[float]] | None:
        """Return the Jacobian of the lower bounds.

        Returns:
            List[List[float]] | None: The Jacobian matrix or None if not set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_lowerbound)
    
    def set_Jacobian_LowerBound(self, jacobian_lowerbound_in: List[List[float]]) -> None:
        """Set the Jacobian of the lower bounds.

        Args:
            jacobian_lowerbound_in (List[List[float]]): The Jacobian matrix to set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_lowerbound = copy.deepcopy(jacobian_lowerbound_in)
        
    ###########################################################################
    # Upper bound constraint values
    ###########################################################################
    
    def get_Upper_BoundConstraints_Value(self) -> List[float] | None:
        """Return the upper bound constraint values.

        Returns:
            List[float] | None: The upper bound constraint values or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._upper_boundconstraints_value)
    
    def set_Upper_BoundConstraints_Value(self, upper_boundconstraints_value_in: List[float]) -> None:
        """Set the upper bound constraint values.

        Args:
            upper_boundconstraints_value_in (List[float]): The upper bound constraint values to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._upper_boundconstraints_value = copy.copy(upper_boundconstraints_value_in)
    
    ###########################################################################
    # Jacobian of upper bounds
    ###########################################################################
    
    def get_Jacobian_UpperBound(self) -> List[List[float]] | None:
        """Return the Jacobian of the upper bounds.

        Returns:
            List[List[float]] | None: The Jacobian matrix or None if not set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_upperbound)
    
    def set_Jacobian_UpperBound(self, jacobian_upperbound_in: List[List[float]]) -> None:
        """Set the Jacobian of the upper bounds.

        Args:
            jacobian_upperbound_in (List[List[float]]): The Jacobian matrix to set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_upperbound = copy.deepcopy(jacobian_upperbound_in)
        
    ###########################################################################
    # Jacobian of equality constraints
    ###########################################################################
    
    def get_Jacobian_LocalEqualityConstraints(self) -> List[List[float]] | None:
        """Return the Jacobian of the equality constraints.

        Returns:
            List[List[float]] | None: The Jacobian matrix or None if not set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_localequalityconstraints)
    
    def set_Jacobian_LocalEqualityConstraints(self, jacobian_equalityconstraints_in: List[List[float]]) -> None:
        """Set the Jacobian of the equality constraints.

        Args:
            jacobian_equalityconstraints_in (List[List[float]]): The Jacobian matrix to set.
        """
        # copy.deepcopy() used - List[List[float]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_localequalityconstraints = copy.deepcopy(jacobian_equalityconstraints_in)
    
    ###########################################################################
    # Local coupling parameters for i <-> j coupling, direction local -> controller
    ###########################################################################
    
    def get_LocalToLocalForController_CouplingParameters(self) -> List[LocalToLocalForController_CouplingParameters]:
        """Return the list of LocalToLocalForController_CouplingParameters.

        Returns all coupling parameters for each i <-> j coupling.

        Returns:
            List[LocalToLocalForController_CouplingParameters]: The coupling parameters list.
        """
        # No copy.copy() used - List[LocalToLocalForController_CouplingParameters] is a list of class objects
        # returned by reference intentionally. This allows the caller to interact with the actual
        # object. If isolation is needed, the caller should explicitly copy.
        return self._localtolocalforcontroller_couplingparameters
    
    def set_LocalToLocalForController_CouplingParameters(self, localtolocalforcontroller_couplingparametersin: List[LocalToLocalForController_CouplingParameters]) -> None:
        """Set the list of LocalToLocalForController_CouplingParameters.

        Sets all coupling parameters for each i <-> j coupling.

        Args:
            localtolocalforcontroller_couplingparametersin (List[LocalToLocalForController_CouplingParameters]): The coupling parameters list to set.
        """
        # No copy.copy() used - List[LocalToLocalForController_CouplingParameters] is a list of class objects
        # assigned by reference intentionally. This allows the caller to continue interacting with
        # the actual objects. If isolation is needed, the caller should explicitly copy.
        self._localtolocalforcontroller_couplingparameters = localtolocalforcontroller_couplingparametersin
        
    def update_state(self, other_middlelevelcoupling: 'LocalToController_MiddleLevelCouplingALADIN') -> None:
        """Update the state of this LocalToController_MiddleLevelCouplingALADIN with another instance.
        
        This method updates the numerical information stored in the class's attributes
        without changing the original memory address location. This is necessary for
        multiprocessing, where executed subsystems return from separate processes and
        their state must be transferred back to the original objects in the main process.
        
        Args:
            other_middlelevelcoupling: The source instance to copy state from.
        """
        # Call the base class update_state to handle common attributes
        super().update_state(other_middlelevelcoupling)
        
        other_hessian_localconstraints_lagrangian: List[List[float]] | None = other_middlelevelcoupling.get_Hessian_LocalConstraints_Lagrangian()
        if other_hessian_localconstraints_lagrangian is None:
            self._hessian_localconstraints_lagrangian = None
        elif self._hessian_localconstraints_lagrangian is None:
            self._hessian_localconstraints_lagrangian = [list(inner) for inner in other_hessian_localconstraints_lagrangian]
        else:
            for i in range(len(other_hessian_localconstraints_lagrangian)):
                self._hessian_localconstraints_lagrangian[i] = update_state_listprimitive(
                    self._hessian_localconstraints_lagrangian[i], other_hessian_localconstraints_lagrangian[i])
        
        self._gradient_localobjective: List[float] | None = update_state_listprimitive(
            self._gradient_localobjective, other_middlelevelcoupling.get_Gradient_LocalObjective())
       
        self._localinequalityconstraintsvalue: List[float] | None = update_state_listprimitive(
            self._localinequalityconstraintsvalue, other_middlelevelcoupling.get_LocalInequalityConstraintsValue())

        other_jacobian_localinequalityconstraints: List[List[float]] | None = other_middlelevelcoupling.get_Jacobian_LocalInequalityConstraints()
        if other_jacobian_localinequalityconstraints is None:
            self._jacobian_localinequalityconstraints = None
        elif self._jacobian_localinequalityconstraints is None:
            self._jacobian_localinequalityconstraints = [list(inner) for inner in other_jacobian_localinequalityconstraints]
        else:
            for i in range(len(other_jacobian_localinequalityconstraints)):
                self._jacobian_localinequalityconstraints[i] = update_state_listprimitive(
                    self._jacobian_localinequalityconstraints[i], other_jacobian_localinequalityconstraints[i])
        
        self._lower_boundconstraints_value: List[float] | None = update_state_listprimitive(
            self._lower_boundconstraints_value, other_middlelevelcoupling.get_Lower_BoundConstraints_Value())
                
        other_jacobian_lowerbound: List[List[float]] | None = other_middlelevelcoupling.get_Jacobian_LowerBound()
        if other_jacobian_lowerbound is None:
            self._jacobian_lowerbound = None
        elif self._jacobian_lowerbound is None:
            self._jacobian_lowerbound = [list(inner) for inner in other_jacobian_lowerbound]
        else:
            for i in range(len(other_jacobian_lowerbound)):
                self._jacobian_lowerbound[i] = update_state_listprimitive(
                    self._jacobian_lowerbound[i], other_jacobian_lowerbound[i])
        
        self._upper_boundconstraints_value: List[float] | None = update_state_listprimitive(
            self._upper_boundconstraints_value, other_middlelevelcoupling.get_Upper_BoundConstraints_Value())
                
        other_jacobian_upperbound: List[List[float]] | None = other_middlelevelcoupling.get_Jacobian_UpperBound()
        if other_jacobian_upperbound is None:
            self._jacobian_upperbound = None
        elif self._jacobian_upperbound is None:
            self._jacobian_upperbound = [list(inner) for inner in other_jacobian_upperbound]
        else:
            for i in range(len(other_jacobian_upperbound)):
                self._jacobian_upperbound[i] = update_state_listprimitive(
                    self._jacobian_upperbound[i], other_jacobian_upperbound[i])

        other_jacobian_equalityconstraints: List[List[float]] | None = other_middlelevelcoupling.get_Jacobian_LocalEqualityConstraints()
        if other_jacobian_equalityconstraints is None:
            self._jacobian_localequalityconstraints = None
        elif self._jacobian_localequalityconstraints is None:
            self._jacobian_localequalityconstraints = [list(inner) for inner in other_jacobian_equalityconstraints]
        else:
            for i in range(len(other_jacobian_equalityconstraints)):
                self._jacobian_localequalityconstraints[i] = update_state_listprimitive(
                    self._jacobian_localequalityconstraints[i], other_jacobian_equalityconstraints[i])
         
        other_localtolocalforcontroller_couplingparameters: List[LocalToLocalForController_CouplingParameters] = other_middlelevelcoupling.get_LocalToLocalForController_CouplingParameters()
        for i in range(len(other_localtolocalforcontroller_couplingparameters)):
            self._localtolocalforcontroller_couplingparameters[i].update_state(other_localtolocalforcontroller_couplingparameters[i])
