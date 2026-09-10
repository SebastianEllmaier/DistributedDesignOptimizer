---
title: OptimDataBasis (Source)
---

← Back to [OptimDataBasis documentation](OptimDataBasis.md)

# OptimDataBasis - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\optimization\optimizerdata\OptimDataBasis.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Optimization data basis module.

This module provides the base class for optimization data structures.
"""

import copy
from typing import List
import numpy as np
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print
from Distributed_Design_Optimizer.subsystem.couplingparameters import CouplingParametersBasis


class OptimDataBasis:
    """Base data structure for optimization results.

    Holds design variables, objectives, constraints, gradients, Jacobians,
    multipliers, and solver metadata after a completed optimization.
    """

    _DDO_PRINT_LABEL_WIDTH: int = 32

    def __init__(self,
                 optimizer_type: str | None,
                 designvariables: List[float] | None,
                 designvariables_unscaled: List[float] | None,
                 lowerbounds: List[float] | None,
                 lowerbounds_scaled: List[float] | None,
                 upperbounds: List[float] | None,
                 upperbounds_scaled: List[float] | None, 
                 totalobjectivevalue: float | None,
                 coordinationobjectivevalue: float | None,  # when running Matlab Optimizer, we do not have access to CoordinationObjectiveValue
                 totalconstrainteqvalue: List[float] | None,
                 totalconstraintineqvalue: List[float] | None,
                 coordinationequalityconstraintvalue: List[float] | None,
                 coordinationinequalityconstraintvalue: List[float] | None,
                 couplingparameters: List[CouplingParametersBasis] | None,
                 gradient_coordinationobjective: List[float | None] | None,
                 jacobian_coordinationequalityconstraints: List[List[float | None]] | None,
                 jacobian_coordinationinequalityconstraints: List[List[float | None]] | None,
                 gradient_totalobjective: List[float | None] | None,
                 jacobian_totalequalityconstraints: List[List[float | None]] | None,
                 jacobian_totalinequalityconstraints: List[List[float | None]] | None,
                 jacobian_lowerbounds: List[List[float | None]] | None,
                 jacobian_upperbounds: List[List[float | None]] | None,
                 multipliers_lowerbounds: List[float | None] | None,
                 multipliers_upperbounds: List[float | None] | None,
                 multipliers_coordination_equality_constraints: List[float | None] | None,
                 multipliers_coordination_inequality_constraints: List[float | None] | None,
                 activecoordinationinequalityconstraints: List[bool] | None,
                 activelowerbounds: List[bool] | None,
                 activeupperbounds: List[bool] | None,
                 exitflag: int | None,
                 message: str | None,
                 optimization_numberofdesignvariableevaluations: int | None,
                 optimization_runtime: float | None,
                 numberofactiveinequalityconstraints: int | None,
                 numberofactivebounds: int | None,
                 ) -> None:
        """Initialize OptimDataBasis.

        Args:
            optimizer_type: The type of optimizer algorithm used.
            designvariables: List of scaled design variable values in [0.0, 1.0].
            designvariables_unscaled: List of unscaled design variable values.
            lowerbounds: List of unscaled lower bounds.
            lowerbounds_scaled: List of scaled lower bounds.
            upperbounds: List of unscaled upper bounds.
            upperbounds_scaled: List of scaled upper bounds.
            totalobjectivevalue: The total objective function value.
            coordinationobjectivevalue: The coordination objective value, or None
                if not available (e.g., when running Matlab Optimizer).
            totalconstrainteqvalue: List of total equality constraint values.
            totalconstraintineqvalue: List of total inequality constraint values.
            coordinationequalityconstraintvalue: List of coordination equality
                constraint values, or None if not available.
            coordinationinequalityconstraintvalue: List of coordination inequality
                constraint values, or None if not available.
            couplingparameters: List of coupling parameters objects.
            gradient_coordinationobjective: Gradient of the coordination objective.
            jacobian_coordinationequalityconstraints: Jacobian of the coordination
                equality constraints.
            jacobian_coordinationinequalityconstraints: Jacobian of the coordination
                inequality constraints.
            gradient_totalobjective: Gradient of the total objective.
            jacobian_totalequalityconstraints: Jacobian of the total equality
                constraints.
            jacobian_totalinequalityconstraints: Jacobian of the total inequality
                constraints.
            jacobian_lowerbounds: Jacobian of the lower bound constraints.
            jacobian_upperbounds: Jacobian of the upper bound constraints.
            multipliers_lowerbounds: Multipliers for the lower bounds.
            multipliers_upperbounds: Multipliers for the upper bounds.
            multipliers_coordination_equality_constraints: Multipliers for the
                coordination equality constraints.
            multipliers_coordination_inequality_constraints: Multipliers for the
                coordination inequality constraints.
            activecoordinationinequalityconstraints: List of bools indicating
                active coordination inequality constraints.
            activelowerbounds: List of bools indicating active lower bounds.
            activeupperbounds: List of bools indicating active upper bounds.
            exitflag: The exit flag indicating optimization convergence status.
            message: The optimization result message.
            optimization_numberofdesignvariableevaluations: Number of design
                variable evaluations during optimization.
            optimization_runtime: The runtime of the optimization in seconds.
            numberofactiveinequalityconstraints: Number of active inequality
                constraints, or None if not available.
            numberofactivebounds: Number of active bounds, or None if not available.
        """
        self._optimizer_type = optimizer_type
        self._exitflag = exitflag
        self._message = message
        
        # 0-1-Check is done only for local subsystems, i.e. in LocalOptimDataBasis
        self._designvariables = designvariables
        self._designvariables_unscaled = designvariables_unscaled
        
        self._lowerbounds: List[float] | None = lowerbounds
        self._lowerbounds_scaled: List[float] | None = lowerbounds_scaled
        self._upperbounds: List[float] | None = upperbounds
        self._upperbounds_scaled: List[float] | None = upperbounds_scaled
         
        self._totalobjectivevalue = totalobjectivevalue
        self._totalconstrainteqvalue = totalconstrainteqvalue
        self._totalconstraintineqvalue = totalconstraintineqvalue
        
        self._coordinationobjectivevalue = coordinationobjectivevalue
        
        # Gradients and Jacobians of coordination objective / constraints and bounds
        self._gradient_coordinationobjective: List[float | None] | None = gradient_coordinationobjective
        self._jacobian_coordinationequalityconstraints: List[List[float | None]] | None = jacobian_coordinationequalityconstraints
        self._jacobian_coordinationinequalityconstraints: List[List[float | None]] | None = jacobian_coordinationinequalityconstraints
        
        # Gradients and Jacobians of total objective / constraints and bounds
        self._gradient_totalobjective: List[float | None] | None = gradient_totalobjective
        self._jacobian_totalequalityconstraints: List[List[float | None]] | None = jacobian_totalequalityconstraints
        self._jacobian_totalinequalityconstraints: List[List[float | None]] | None = jacobian_totalinequalityconstraints
        
        self._jacobian_lowerbounds: List[List[float | None]] | None = jacobian_lowerbounds
        self._jacobian_upperbounds: List[List[float | None]] | None = jacobian_upperbounds
        
        # local multipliers w.r.t. local lower bounds, upper bounds, coordinator equality constraints
        
        # Check for bounds, if array of active constraints and of multipliers are consistent; 
        # i.e., both are None (and non-None) at the same entries
        
        # Violation for Lower bounds 
        if ((multipliers_lowerbounds is not None and activelowerbounds is not None) and
            any(multipliers_lowerbounds[i] is None and activelowerbounds[i] is True
                or multipliers_lowerbounds[i] is not None and activelowerbounds[i] is False
                for i in range(len(multipliers_lowerbounds)))):
            
            # Violation
            raise ValueError(f"{DDO_Color}Your provided multipliers and activeness indicators for the lower bounds are not consistent: ", 
                             f"Multipliers for lower bounds: {multipliers_lowerbounds}, Active lower bounds: {activelowerbounds}{Reset}")
        
        # Violation for upper bounds
        if ((multipliers_upperbounds is not None and activeupperbounds is not None) and
            any(multipliers_upperbounds[i] is None and activeupperbounds[i] is True
                or multipliers_upperbounds[i] is not None and activeupperbounds[i] is False
                for i in range(len(multipliers_upperbounds)))):
            
            # Violation
            raise ValueError(f"{DDO_Color}Your provided multipliers and activeness indicators for the upper bounds are not consistent: ", 
                             f"Multipliers for upper bounds: {multipliers_upperbounds}, Active upper bounds: {activeupperbounds}{Reset}")
        
        self._multipliers_lowerbounds: List[float | None] | None = multipliers_lowerbounds
        self._multipliers_upperbounds: List[float | None] | None = multipliers_upperbounds
        
        self._multipliers_coordination_equality_constraints: List[float | None] | None = multipliers_coordination_equality_constraints
        self._multipliers_coordination_inequality_constraints: List[float | None] | None = multipliers_coordination_inequality_constraints
        
        self._coordinationequalityconstraintvalue = coordinationequalityconstraintvalue
        self._coordinationinequalityconstraintvalue = coordinationinequalityconstraintvalue
        
        # Jacobians of the mapped responses are stored in additional coupling parameters
        self._couplingparameters: List[CouplingParametersBasis] | None = couplingparameters
        
        self._optimization_numberofdesignvariableevaluations = optimization_numberofdesignvariableevaluations
        self._optimization_runtime = optimization_runtime
        
        # Store
        self._activelowerbounds: List[bool] | None = activelowerbounds
        self._activeupperbounds: List[bool] | None = activeupperbounds
        self._activecoordinationinequalityconstraints: List[bool] | None = activecoordinationinequalityconstraints
        
        self._numberofactiveinequalityconstraints = numberofactiveinequalityconstraints
        self._numberofactivebounds = numberofactivebounds
        
        # Compute ratio of active bounds and constraints
        self._ratioofactiveboundsandconstraints = None
        if (self._designvariables is not None and len(self._designvariables) != 0
                and self._numberofactiveinequalityconstraints is not None 
                and self._numberofactivebounds is not None
                and self._totalconstraintineqvalue is not None):
            self._ratioofactiveboundsandconstraints = (self._numberofactiveinequalityconstraints + self._numberofactivebounds) / (len(self._designvariables) + len(self._totalconstraintineqvalue))

    def set_Optimizer_Type(self, optimizer_type_in: str) -> None:
        """Set the type of optimization algorithm.

        Args:
            optimizer_type_in: Optimizer algorithm identifier.
        """
        # No copy.copy() needed - str is a primitive/immutable type.
        # Assigning the input value directly is safe because any subsequent changes
        # to the caller's variable cannot affect this class's attribute.
        self._optimizer_type = optimizer_type_in

    def get_Optimizer_Type(self) -> str:
        """Get the type of optimization algorithm.

        Returns:
            The optimizer algorithm identifier.
        """
        # No copy.copy() needed - str is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._optimizer_type

    def set_DesignVariables(self, designvariables_in: List[float]) -> None:
        """Set the design variables.

        Args:
            designvariables_in: Design variables.
        """

        if designvariables_in is None:
            raise ValueError(f"{DDO_Color}designvariables_in must not be None{Reset}")

        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._designvariables = copy.copy(designvariables_in)
    
    def get_DesignVariables(self) -> List[float] | None:
        """Get the design variables (scaled01 values).

        Returns:
            The scaled design variable values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._designvariables)

    def set_DesignVariables_Unscaled(self, designvariables_unscaled_in: List[float]) -> None:
        """Set the unscaled design variables.

        Args:
            designvariables_unscaled_in: Unscaled design variables.
        """

        if designvariables_unscaled_in is None:
            raise ValueError(f"{DDO_Color}designvariables_unscaled_in must not be None{Reset}")
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._designvariables_unscaled = copy.copy(designvariables_unscaled_in)

    def get_DesignVariables_Unscaled(self) -> List[float]:
        """Get the unscaled design variables.

        Returns:
            The unscaled design variable values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._designvariables_unscaled)
    
    def set_LowerBounds(self, lowerbounds_in: List[float]) -> None:
        """Set the lower bounds (unscaled).

        Args:
            lowerbounds_in: Lower bounds.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._lowerbounds = copy.copy(lowerbounds_in)

    def get_LowerBounds(self) -> List[float] | None:
        """Get the lower bounds (unscaled).

        Returns:
            The lower bounds.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._lowerbounds)

    def set_LowerBounds_Scaled(self, lowerbounds_scaled_in: List[float]) -> None:
        """Set the scaled lower bounds.

        Args:
            lowerbounds_scaled_in: Scaled lower bounds.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._lowerbounds_scaled = copy.copy(lowerbounds_scaled_in)

    def get_LowerBounds_Scaled(self) -> List[float] | None:
        """Get the scaled lower bounds.

        Returns:
            The scaled lower bounds.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._lowerbounds_scaled)

    def set_UpperBounds(self, upperbounds_in: List[float]) -> None:
        """Set the upper bounds (unscaled).

        Args:
            upperbounds_in: Upper bounds.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._upperbounds = copy.copy(upperbounds_in)

    def get_UpperBounds(self) -> List[float] | None:
        """Get the upper bounds (unscaled).

        Returns:
            The upper bounds.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._upperbounds)

    def set_UpperBounds_Scaled(self, upperbounds_scaled_in: List[float]) -> None:
        """Set the scaled upper bounds.

        Args:
            upperbounds_scaled_in: Scaled upper bounds.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._upperbounds_scaled = copy.copy(upperbounds_scaled_in)    

    def get_UpperBounds_Scaled(self) -> List[float] | None:
        """Get the scaled upper bounds.

        Returns:
            The scaled upper bounds.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._upperbounds_scaled)

    def set_TotalObjectiveValue(self, totalobjectivevalue_in: float) -> None:
        """Set the local objective function value of the optimization problem.

        Args:
            totalobjectivevalue_in: Total objective function value.
        """

        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning the input value directly is safe because any subsequent changes
        # to the caller's variable cannot affect this class's attribute.
        self._totalobjectivevalue = totalobjectivevalue_in
          
    def get_TotalObjectiveValue(self) -> float | None:
        """Get the total objective function value of the optimization problem.

        Returns:
            The total objective function value, or None if not set.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._totalobjectivevalue
    
    def set_CoordinationObjectiveValue(self, coordinationobjectivevalue_in: float) -> None:
        """Set the coordination objective value of the optimization problem.

        Args:
            coordinationobjectivevalue_in: Coordination objective function value.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning the input value directly is safe because any subsequent changes
        # to the caller's variable cannot affect this class's attribute.
        self._coordinationobjectivevalue = coordinationobjectivevalue_in
    
    def get_CoordinationObjectiveValue(self) -> float | None:  # when running Matlab Optimizer, we do not have access to CoordinationObjectiveValue
        """Gets the coordination objective value.

        Returns:
            The coordination objective value, or None if not available
            (e.g., when running Matlab Optimizer).
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._coordinationobjectivevalue

    def set_CouplingParameters(self, couplingparameters_in: List[CouplingParametersBasis]) -> None:
        """Set coupling parameters to update current information.

        Args:
            couplingparameters_in: The coupling parameters to set.
        """
        # No copy - List[CouplingParametersBasis] is a list of strategy objects
        # stored by reference intentionally.
        self._couplingparameters = couplingparameters_in

    def get_CouplingParameters(self) -> List[CouplingParametersBasis]:
        """Get the coupling parameters.

        Returns:
            The list of coupling parameters objects.
        """
        # No copy.copy() used - List[CouplingParametersBasis] is a list of class objects
        # returned by reference intentionally. This allows the caller to interact with
        # the actual objects. If isolation is needed, the caller should explicitly copy.
        return self._couplingparameters
    
    def set_Gradient_CoordinationObjective(self, gradient_coordinationobjective_in: List[float | None]) -> None:
        """Set the gradient of the coordination objective.

        Args:
            gradient_coordinationobjective_in: Gradient of the coordination
                objective.
        """        
        # Check if coordination objective exists
        if self.get_CoordinationObjectiveValue() is None:
            
            # There does not exist a coordination objective
            raise ValueError(f"{DDO_Color}There does not exist a coordination objective{Reset}")
        
        # Check if the input has correct dimension
        if np.array(gradient_coordinationobjective_in).shape != (len(self.get_DesignVariables()),):
            
            # The dimensions do not match
            raise ValueError(f"{DDO_Color}The dimension of your provided gradient of the coordination objective is incorrect; ",  
                             f"expected: {(len(self.get_DesignVariables()))}, provided: {np.array(gradient_coordinationobjective_in).shape}{Reset}")
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._gradient_coordinationobjective = copy.copy(gradient_coordinationobjective_in)
        
    def get_Gradient_CoordinationObjective(self) -> List[float | None] | None:
        """Get the gradient of the coordination objective.

        Returns:
            Gradient of the coordination objective, or None if not set.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._gradient_coordinationobjective)
    
    def set_Jacobian_CoordinationEqualityConstraints(self, 
                                                     jacobian_coordinationequalityconstraints_in: List[List[float | None]]) -> None:
        """Set the Jacobian of the coordination equality constraints.

        Args:
            jacobian_coordinationequalityconstraints_in: Jacobian of the
                coordination equality constraints.
        """
        
        # Check if coordination equality constraints exist
        if self.get_CoordinationEqualityConstraintValue() is None:
            
            # There does not exist any coordination equality constraint
            raise ValueError(f"{DDO_Color}There does not exist a coordination equality constraint{Reset}")
        
        # Check if the input has correct dimension
        if np.array(jacobian_coordinationequalityconstraints_in).shape != (len(self.get_CoordinationEqualityConstraintValue()), len(self.get_DesignVariables())):
            
            # The dimensions do not match
            raise ValueError(f"{DDO_Color}The dimensions of your provided Jacobian of the coordination equality constraints are incorrect; ",  
                             f"expected: {(len(self.get_CoordinationEqualityConstraintValue()), len(self.get_DesignVariables()))}, ",
                             f"provided: {np.array(jacobian_coordinationequalityconstraints_in).shape}{Reset}")
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_coordinationequalityconstraints = copy.deepcopy(jacobian_coordinationequalityconstraints_in)
    
    def get_Jacobian_CoordinationEqualityConstraints(self) -> List[List[float | None]] | None:
        """Get the Jacobian of the coordination equality constraints.

        Returns:
            Jacobian of the coordination equality constraints, or None if not
                set.
        """
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_coordinationequalityconstraints)
    
    def set_Jacobian_CoordinationInequalityConstraints(self, 
                                                       jacobian_coordinationinequalityconstraints_in: List[List[float | None]]) -> None:
        """Set the Jacobian of the coordination inequality constraints.

        Args:
            jacobian_coordinationinequalityconstraints_in: Jacobian of the
                coordination inequality constraints.
        """
        
        # Check if coordination inequality constraints exist
        if self.get_CoordinationInequalityConstraintValue() is None:
            
            # There does not exist any coordination inequality constraint
            raise ValueError(f"{DDO_Color}There does not exist a coordination inequality constraint{Reset}")
        
        # Check if the input has correct dimension
        if np.array(jacobian_coordinationinequalityconstraints_in).shape != (len(self.get_CoordinationInequalityConstraintValue()), len(self.get_DesignVariables())):
            
            # The dimensions do not match
            raise ValueError(f"{DDO_Color}The dimensions of your provided Jacobian of the coordination inequality constraints are incorrect; ",  
                             f"expected: {(len(self.get_CoordinationInequalityConstraintValue()), len(self.get_DesignVariables()))}, ",
                             f"provided: {np.array(jacobian_coordinationinequalityconstraints_in).shape}{Reset}")
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_coordinationinequalityconstraints = copy.deepcopy(jacobian_coordinationinequalityconstraints_in)

    def get_Jacobian_CoordinationInequalityConstraints(self) -> List[List[float | None]] | None:
        """Get the Jacobian of the coordination inequality constraints.

        Returns:
            Jacobian of the coordination inequality constraints, or None if
                not set.
        """
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_coordinationinequalityconstraints)
    
    def set_Gradient_TotalObjective(self, gradient_totalobjective_in: List[float | None]) -> None:
        """Set the gradient of the total objective.

        Args:
            gradient_totalobjective_in: Gradient of the total objective.
        """
        
        # Check if total objective exists
        if self.get_TotalObjectiveValue() is None:
            
            # There does not exist a total objective
            raise ValueError(f"{DDO_Color}There does not exist a total objective{Reset}")
        
        # Check if the input has correct dimension
        if np.array(gradient_totalobjective_in).shape != (len(self.get_DesignVariables()),):
            
            # The dimensions do not match
            raise ValueError(f"{DDO_Color}The dimension of your provided gradient of the total objective is incorrect; ",  
                             f"expected: {(len(self.get_DesignVariables()))}, provided: {np.array(gradient_totalobjective_in).shape}{Reset}")
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._gradient_totalobjective = copy.copy(gradient_totalobjective_in)
        
    def get_Gradient_TotalObjective(self) -> List[float | None] | None:
        """Get the gradient of the total objective.

        Returns:
            Gradient of the total objective, or None if not set.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._gradient_totalobjective)
    
    def set_Jacobian_TotalEqualityConstraints(self, 
                                              jacobian_totalequalityconstraints_in: List[List[float | None]]) -> None:
        """Set the Jacobian of the total equality constraints.

        Args:
            jacobian_totalequalityconstraints_in: Jacobian of the total equality
                constraints.
        """
        
        # Check if total equality constraints exist
        if self.get_TotalConstraintEqValue() is None:
            
            # There does not exist any total equality constraint
            raise ValueError(f"{DDO_Color}There does not exist a total equality constraint{Reset}")
        
        # Check if the input has correct dimension
        if np.array(jacobian_totalequalityconstraints_in).shape != (len(self.get_TotalConstraintEqValue()), len(self.get_DesignVariables())):
            
            # The dimensions do not match
            raise ValueError(f"{DDO_Color}The dimensions of your provided Jacobian of the total equality constraints are incorrect; ",  
                             f"expected: {(len(self.get_TotalConstraintEqValue()), len(self.get_DesignVariables()))}, ",
                             f"provided: {np.array(jacobian_totalequalityconstraints_in).shape}{Reset}")
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_totalequalityconstraints = copy.deepcopy(jacobian_totalequalityconstraints_in)
    
    def get_Jacobian_TotalEqualityConstraints(self) -> List[List[float | None]] | None:
        """Get the Jacobian of the total equality constraints.

        Returns:
            Jacobian of the total equality constraints, or None if not set.
        """
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_totalequalityconstraints)
    
    def set_Jacobian_TotalInequalityConstraints(self, 
                                                jacobian_totalinequalityconstraints_in: List[List[float | None]]) -> None:
        """Set the Jacobian of the total inequality constraints.

        Args:
            jacobian_totalinequalityconstraints_in: Jacobian of the total
                inequality constraints.
        """
        
        # Check if total inequality constraints exist
        if self.get_TotalConstraintIneqValue() is None:
            
            # There does not exist any total inequality constraint
            raise ValueError(f"{DDO_Color}There does not exist a total inequality constraint{Reset}")
        
        # Check if the input has correct dimension
        if np.array(jacobian_totalinequalityconstraints_in).shape != (len(self.get_TotalConstraintIneqValue()), len(self.get_DesignVariables())):
            
            # The dimensions do not match
            raise ValueError(f"{DDO_Color}The dimensions of your provided Jacobian of the total inequality constraints are incorrect; ",  
                             f"expected: {(len(self.get_TotalConstraintIneqValue()), len(self.get_DesignVariables()))}, ",
                             f"provided: {np.array(jacobian_totalinequalityconstraints_in).shape}{Reset}")
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_totalinequalityconstraints = copy.deepcopy(jacobian_totalinequalityconstraints_in)        

    def get_Jacobian_TotalInequalityConstraints(self) -> List[List[float | None]] | None:
        """Get the Jacobian of the total inequality constraints.

        Returns:
            Jacobian of the total inequality constraints, or None if not set.
        """
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_totalinequalityconstraints)
    
    def set_Jacobian_LowerBounds(self, jacobian_lowerbounds_in: List[List[float | None]]) -> None:
        """Set the Jacobian of the lower bounds.

        Args:
            jacobian_lowerbounds_in: Jacobian of the lower bounds.
        """
        
        # Check if the input has correct dimensions (n_designvars x n_designvars)
        expected_shape = (len(self.get_DesignVariables()), len(self.get_DesignVariables()))
        if np.array(jacobian_lowerbounds_in).shape != expected_shape:
            
            # The dimensions do not match
            raise ValueError(f"{DDO_Color}The dimensions of your provided Jacobian of the lower bounds are incorrect; ",
                             f"expected: {expected_shape}, ",
                             f"provided: {np.array(jacobian_lowerbounds_in).shape}{Reset}")
        
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_lowerbounds = copy.deepcopy(jacobian_lowerbounds_in)
    
    def get_Jacobian_LowerBounds(self) -> List[List[float | None]] | None:
        """Get the Jacobian of the active lower bound constraints.

        Returns:
            Jacobian of the active lower bounds, or None if not set.
        """
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_lowerbounds)
    
    def set_Jacobian_UpperBounds(self, jacobian_upperbounds_in: List[List[float | None]]) -> None:
        """Set the Jacobian of the upper bounds.

        Args:
            jacobian_upperbounds_in: Jacobian of the upper bounds.
        """
        
        # Check if the input has correct dimensions (n_designvars x n_designvars)
        expected_shape = (len(self.get_DesignVariables()), len(self.get_DesignVariables()))
        if np.array(jacobian_upperbounds_in).shape != expected_shape:
            
            # The dimensions do not match
            raise ValueError(f"{DDO_Color}The dimensions of your provided Jacobian of the upper bounds are incorrect; ",
                             f"expected: {expected_shape}, ",
                             f"provided: {np.array(jacobian_upperbounds_in).shape}{Reset}")
        
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_upperbounds = copy.deepcopy(jacobian_upperbounds_in)
    
    def get_Jacobian_UpperBounds(self) -> List[List[float | None]] | None:
        """Get the Jacobian of the active upper bound constraints.

        Returns:
            Jacobian of the active upper bounds, or None if not set.
        """
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_upperbounds)
    
    def set_Multipliers_LowerBounds(self, multipliers_lowerbounds_in: List[float | None]) -> None:
        """Set the multipliers w.r.t the lower bounds.

        Args:
            multipliers_lowerbounds_in: Multipliers for the lower bounds.
        """
        
        # Get the active lower bounds
        activelowerbounds: List[bool] = self.get_ActiveLowerBounds()
        
        # Check if the dimensions match
        if len(multipliers_lowerbounds_in) != len(self.get_DesignVariables()):
            
            # The dimensions do not match
            raise ValueError(f"{DDO_Color}The dimension of your provided multipliers w.r.t to the lower bound constraints is incorrect; ", 
                             f"expected: {len(self.get_DesignVariables())}, provided: {len(multipliers_lowerbounds_in)}{Reset}")

        # Check if for inactive lower bound constraints, the corresponding multipliers are None
        if any(multipliers_lowerbounds_in[i] is not None and activelowerbounds[i] is False 
               for i in range(len(multipliers_lowerbounds_in))):
            
            # If there is an inactive constraint for which the multiplier is not None
            raise ValueError(f"{DDO_Color}Your multiplier w.r.t. the lower bounds constraints is incorrect, ", 
                             "since you provided multipliers for inactive lower bounds.", 
                             f"Your multipliers for lower bounds: {multipliers_lowerbounds_in}, Active lower bounds: {activelowerbounds}{Reset}")
        
        # Check if for active lower bound constraints, the corresponding multipliers are not None
        if any(multipliers_lowerbounds_in[i] is None and activelowerbounds[i] is True 
               for i in range(len(multipliers_lowerbounds_in))):
            
            # If there is such a None-multiplier for an active constraint
            raise ValueError(f"{DDO_Color}Your provided multiplier is None for an active constraint. ", 
                             f"Your multipliers for lower bounds: {multipliers_lowerbounds_in}, Active lower bounds: {activelowerbounds}{Reset}")
        
        # Check if the multipliers are non-negative for the active inequality constraints
        if any(activelowerbounds[i] is True and multipliers_lowerbounds_in[i] < 0 
               for i in range(len(multipliers_lowerbounds_in))):
            
            # All multipliers for active constraints are non-negative
            raise ValueError(f"{DDO_Color}Your provided multipliers need to be non-negative for active lower bounds{Reset}")
        
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_lowerbounds = copy.copy(multipliers_lowerbounds_in) 
        
    def get_Multipliers_LowerBounds(self) -> List[float | None] | None:
        """Get the multipliers corresponding to the lower bounds.

        Returns:
            Multipliers for the lower bounds, or None if not set.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_lowerbounds)
    
    def set_Multipliers_UpperBounds(self, multipliers_upperbounds_in: List[float | None]) -> None:
        """Set the multipliers w.r.t the upper bounds.

        Args:
            multipliers_upperbounds_in: Multipliers for the upper bounds.
        """        
        
        # Get the active upper bounds
        activeupperbounds: List[bool] = self.get_ActiveUpperBounds()
        
        # Check if the dimensions match
        if len(multipliers_upperbounds_in) != len(self.get_DesignVariables()):
            
            # The dimensions do not match
            raise ValueError(f"{DDO_Color}The dimension of your provided multipliers w.r.t to the upper bound constraints is incorrect; ", 
                             f"expected: {len(self.get_DesignVariables())}, provided: {len(multipliers_upperbounds_in)}{Reset}")

        # Check if for inactive upper bound constraints, the corresponding multipliers are None
        if any(multipliers_upperbounds_in[i] is not None and activeupperbounds[i] is False 
               for i in range(len(multipliers_upperbounds_in))):
            
            # If there is an inactive constraint for which the multiplier is not None
            raise ValueError(f"{DDO_Color}Your multiplier w.r.t. the upper bounds constraints is incorrect, ", 
                             "since you provided multipliers for inactive upper bounds.", 
                             f"Your multipliers for upper bounds: {multipliers_upperbounds_in}, Active upper bounds: {activeupperbounds}{Reset}")
        
        # Check if for active upper bound constraints, the corresponding multipliers are not None
        if any(multipliers_upperbounds_in[i] is None and activeupperbounds[i] is True 
               for i in range(len(multipliers_upperbounds_in))):
            
            # If there is such a None-multiplier for an active constraint
            raise ValueError(f"{DDO_Color}Your provided multiplier is None for an active constraint. ", 
                             f"Your multipliers for upper bounds: {multipliers_upperbounds_in}, Active upper bounds: {activeupperbounds}{Reset}")
        
        # Check if the multipliers are non-negative for the active inequality constraints
        if any(activeupperbounds[i] is True and multipliers_upperbounds_in[i] < 0 
               for i in range(len(multipliers_upperbounds_in))):
            
            # All multipliers for active constraints are non-negative
            raise ValueError(f"{DDO_Color}Your provided multipliers need to be non-negative for active upper bounds{Reset}")

        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_upperbounds = copy.copy(multipliers_upperbounds_in)
    
    def get_Multipliers_UpperBounds(self) -> List[float | None] | None:
        """Get the multipliers corresponding to the upper bounds.

        Returns:
            Multipliers for the upper bounds, or None if not set.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_upperbounds)
    
    def set_Multipliers_Coordination_Equality_Constraints(self, multipliers_coordinationequalityconstraints_in: List[float | None]) -> None:
        """Set the multipliers w.r.t the coordination equality constraints.

        Args:
            multipliers_coordinationequalityconstraints_in: Multipliers for the
                coordination equality constraints.
        """
        
        # Check if there exist any coordination equality constraints
        if self.get_CoordinationEqualityConstraintValue() is None:
            
            # There does not exist any coordination equality constraint
            raise ValueError(f"{DDO_Color}There does not exist any coordination equality constraint{Reset}")
        
        # Check dimensions
        if len(multipliers_coordinationequalityconstraints_in) != len(self.get_CoordinationEqualityConstraintValue()):
            
            # Wrong dimension
            raise ValueError(f"{DDO_Color}Your provided multipliers w.r.t coordination equality constraints have the wrong dimensions. ",
                             f"expected: {len(self.get_CoordinationEqualityConstraintValue())}, provided: {len(multipliers_coordinationequalityconstraints_in)}{Reset}")
        
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_coordination_equality_constraints = copy.copy(multipliers_coordinationequalityconstraints_in)
    
    def get_Multipliers_Coordination_Equality_Constraints(self) -> List[float | None] | None:
        """Get the multipliers corresponding to the coordination equality constraints.

        Returns:
            Multipliers for the coordination equality constraints, or None if
                not set.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_coordination_equality_constraints)
    
    def set_Multipliers_Coordination_Inequality_Constraints(self, multipliers_coordinationinequalityconstraints_in: List[float | None]) -> None:
        """Set the multipliers w.r.t the coordination inequality constraints.

        Args:
            multipliers_coordinationinequalityconstraints_in: Multipliers for the
                coordination inequality constraints.
        """
        
        # Check if there are any coordination inequality constraints
        if self.get_CoordinationInequalityConstraintValue() is None:
            
            # There are no coordination inequality constraints
            raise ValueError(f"{DDO_Color}There does not exist any coordination inequality constraint{Reset}")
        
        # Get the active coordination inequality constraints
        activecoordinationinequalityconstraints: List[bool] = self.get_ActiveCoordinationInequalityConstraints()
        
        # Check if the dimensions match
        if len(multipliers_coordinationinequalityconstraints_in) != len(self.get_CoordinationInequalityConstraintValue()):
            
            # The dimensions do not match
            raise ValueError(f"{DDO_Color}The dimension of your provided multipliers w.r.t to the coordination inequality constraints is incorrect; ", 
                             f"expected: {len(self.get_CoordinationInequalityConstraintValue())}, provided: {len(multipliers_coordinationinequalityconstraints_in)}{Reset}")

        # Check if for inactive coordination inequality constraints, the corresponding multipliers are None
        if any(multipliers_coordinationinequalityconstraints_in[i] is not None and activecoordinationinequalityconstraints[i] is False 
               for i in range(len(multipliers_coordinationinequalityconstraints_in))):
            
            # If there is an inactive constraint for which the multiplier is not None
            raise ValueError(f"{DDO_Color}Your multiplier w.r.t. the coordination inequality constraints is incorrect, ", 
                             "since you provided multipliers for inactive inequality constraints.", 
                             f"Your multipliers for coordination inequality constraints: {multipliers_coordinationinequalityconstraints_in}, ",
                             f"Active coordination inequality constraints: {activecoordinationinequalityconstraints}{Reset}")
        
        # Check if for active coordination inequality constraints, the corresponding multipliers are not None
        if any(multipliers_coordinationinequalityconstraints_in[i] is None and activecoordinationinequalityconstraints[i] is True 
               for i in range(len(multipliers_coordinationinequalityconstraints_in))):
            
            # If there is such a None-multiplier for an active constraint
            raise ValueError(f"{DDO_Color}Your provided multiplier is None for an active constraint. ", 
                             f"Your multipliers for coordination inequality constraints: {multipliers_coordinationinequalityconstraints_in}, ",
                             f"Active coordination inequality constraints: {activecoordinationinequalityconstraints}{Reset}")
        
        # Check if the multipliers are non-negative for the active inequality constraints
        if any(activecoordinationinequalityconstraints[i] is True and multipliers_coordinationinequalityconstraints_in[i] < 0 
               for i in range(len(multipliers_coordinationinequalityconstraints_in))):
            
            # All multipliers for active constraints are non-negative
            raise ValueError(f"{DDO_Color}Your provided multipliers need to be non-negative for active coordination inequality constraints{Reset}")
        
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_coordination_inequality_constraints = copy.copy(multipliers_coordinationinequalityconstraints_in)
        
    def get_Multipliers_Coordination_Inequality_Constraints(self) -> List[float | None] | None:
        """Get the multipliers corresponding to the coordination inequality constraints.

        Returns:
            Multipliers for the coordination inequality constraints, or None
                if not set.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_coordination_inequality_constraints)
    
    def set_TotalConstraintEqValue(self, totalconstrainteqvalue_in: List[float]) -> None:
        """Set the total equality constraint values.

        Args:
            totalconstrainteqvalue_in: Total equality constraint values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._totalconstrainteqvalue = copy.copy(totalconstrainteqvalue_in)

    def get_TotalConstraintEqValue(self) -> List[float] | None:
        """Get the total equality constraint values.

        Returns:
            The total equality constraint values, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._totalconstrainteqvalue)

    def set_TotalConstraintIneqValue(self, totalconstraintineqvalue_in: List[float]) -> None:
        """Set the total inequality constraint values.

        Args:
            totalconstraintineqvalue_in: Total inequality constraint values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._totalconstraintineqvalue = copy.copy(totalconstraintineqvalue_in)

    def get_TotalConstraintIneqValue(self) -> List[float] | None:
        """Get the total inequality constraint values.

        Returns:
            The total inequality constraint values, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._totalconstraintineqvalue)

    def set_CoordinationEqualityConstraintValue(self, coordinationequalityconstraintvalue_in: List[float]) -> None:
        """Set the coordination equality constraint values.

        Args:
            coordinationequalityconstraintvalue_in: Coordination equality
                constraint values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._coordinationequalityconstraintvalue = copy.copy(coordinationequalityconstraintvalue_in)
    
    def get_CoordinationEqualityConstraintValue(self) -> List[float] | None:  # when running Matlab Optimizer, we do not have access to CoordinationEqualityConstraintValue
        """Gets the coordination equality constraint values.

        Returns:
            List of coordination equality constraint values, or None if not
            available (e.g., when running Matlab Optimizer).
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._coordinationequalityconstraintvalue)

    def set_CoordinationInequalityConstraintValue(self, coordinationinequalityconstraintvalue_in: List[float]) -> None:
        """Set the coordination inequality constraint values.

        Args:
            coordinationinequalityconstraintvalue_in: Coordination inequality
                constraint values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._coordinationinequalityconstraintvalue = copy.copy(coordinationinequalityconstraintvalue_in)

    def get_CoordinationInequalityConstraintValue(self) -> List[float] | None:  
        """Get the coordination inequality constraint values.

        Returns:
            The coordination inequality constraint values, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._coordinationinequalityconstraintvalue)

    def get_ExitFlag(self) -> int:
        """Return the optimizer exit flag.

        Returns:
            The optimizer exit flag.
        """
        # No copy.copy() needed - int is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._exitflag

    def get_Message(self) -> str:
        """Get the optimization message.

        Returns:
            The optimization result message.
        """
        # No copy.copy() needed - str is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._message
    
    def get_Optimization_NumberOfDesignVariableEvaluations(self) -> int | None:
        """Get the number of design variable evaluations.

        Returns:
            The number of design variable evaluations.
        """
        # No copy.copy() needed - int is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._optimization_numberofdesignvariableevaluations
    
    def get_Optimization_RunTime(self) -> float | None:
        """Get the optimization runtime.

        Returns:
            The optimization runtime in seconds.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._optimization_runtime
    
    def set_ActiveCoordinationInequalityConstraints(self, activecoordinationinequalityconstraints_in: List[bool]) -> None:
        """Set the list of bools indicating active coordination inequality constraints.

        Args:
            activecoordinationinequalityconstraints_in: Active coordination
                inequality constraints.
        """
        # copy.copy() used - List[bool] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._activecoordinationinequalityconstraints = copy.copy(activecoordinationinequalityconstraints_in)

    def get_ActiveCoordinationInequalityConstraints(self) -> List[bool] | None:
        """Get the list of bools indicating active coordination inequality constraints.

        Returns:
            Active coordination inequality constraints, or None if not set.
        """
        # copy.copy() used - List[bool] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._activecoordinationinequalityconstraints)
    
    def set_ActiveLowerBounds(self, activelowerbounds_in: List[bool]) -> None:
        """Set the list of bools indicating active lower bounds.

        Args:
            activelowerbounds_in: Active lower bounds.
        """
        # copy.copy() used - List[bool] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._activelowerbounds = copy.copy(activelowerbounds_in)
    
    def get_ActiveLowerBounds(self) -> List[bool] | None:
        """Get the list of bools indicating active lower bounds.

        Returns:
            The active lower bounds.
        """
        # copy.copy() used - List[bool] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._activelowerbounds)

    def set_ActiveUpperBounds(self, activeupperbounds_in: List[bool]) -> None:
        """Set the list of bools indicating active upper bounds.

        Args:
            activeupperbounds_in: Active upper bounds.
        """
        # copy.copy() used - List[bool] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._activeupperbounds = copy.copy(activeupperbounds_in)
    
    def get_ActiveUpperBounds(self) -> List[bool] | None:
        """Get the list of bools indicating active upper bounds.

        Returns:
            The active upper bounds.
        """
        # copy.copy() used - List[bool] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._activeupperbounds)

    def set_NumberofActiveInequalityConstraints(self, numberofactiveinequalityconstraints_in: int) -> None:
        """Set the number of active inequality constraints.

        Args:
            numberofactiveinequalityconstraints_in: Number of active inequality
                constraints.
        """
        # No copy.copy() needed - int is a primitive/immutable type.
        # Assigning the input value directly is safe because any subsequent changes
        # to the caller's variable cannot affect this class's attribute.
        self._numberofactiveinequalityconstraints = numberofactiveinequalityconstraints_in
        
    def get_NumberofActiveInequalityConstraints(self) -> int | None:
        """Gets the number of active inequality constraints.

        Returns:
            The number of active inequality constraints, or None if not available.
        """
        # No copy.copy() needed - int is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._numberofactiveinequalityconstraints

    def set_NumberofActiveBounds(self, numberofactivebounds_in: int) -> None:
        """Set the number of active bounds.

        Args:
            numberofactivebounds_in: Number of active bounds.
        """
        # No copy.copy() needed - int is a primitive/immutable type.
        # Assigning the input value directly is safe because any subsequent changes
        # to the caller's variable cannot affect this class's attribute.
        self._numberofactivebounds = numberofactivebounds_in
    
    def get_NumberofActiveBounds(self) -> int:
        """Gets the number of active bounds.

        Returns:
            The number of active bounds, or None if not available.
        """
        # No copy.copy() needed - int is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._numberofactivebounds

    def get_RatioofActiveBoundsandConstraints(self) -> float | None:
        """Gets the ratio of active bounds and constraints to total.

        Returns:
            The ratio of active constraints (input + output) to the total
            number of constraints and bounds, or None if not computable.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._ratioofactiveboundsandconstraints

    def _print_solver_and_designvariables(self) -> None:
        """Print common optimizer results: solver info and design variables."""
        ddo_print(f"       {self.get_Optimizer_Type()} solver took {self.get_Optimization_RunTime():.0f} sec. and tried {self.get_Optimization_NumberOfDesignVariableEvaluations()} design variables evaluations")
        ddo_print(f"       {'Solver Message:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self.get_Message()}")
        dvs = self.get_DesignVariables()
        index_width = len(f"[{len(dvs) - 1}]")
        ddo_print(f"       {'Design variables:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {f'[0]'.ljust(index_width)} {dvs[0]}")
        for i, v in enumerate(dvs[1:], start=1):
            ddo_print(f"       {' ' * self._DDO_PRINT_LABEL_WIDTH} {f'[{i}]'.ljust(index_width)} {v}")

    def print_results(self) -> None:
        """Print optimizer results."""
        self._print_solver_and_designvariables()
        ddo_print(f"       {'Total Objective Value:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self.get_TotalObjectiveValue()}")

```
