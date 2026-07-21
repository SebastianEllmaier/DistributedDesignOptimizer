---
title: LocalSubSystemOptimData (Source)
---

← Back to [LocalSubSystemOptimData documentation](LocalSubSystemOptimData.md)

# LocalSubSystemOptimData - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\optimization\optimizerdata\LocalSubSystemOptimData.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Local subsystem optimization data module.

This module provides data structures for local subsystem optimization.
"""

import copy
from typing import List
import numpy as np

from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print
from Distributed_Design_Optimizer.subsystem.optimization.optimizerdata import OptimDataBasis
from Distributed_Design_Optimizer.subsystem.couplingparameters import CouplingParametersBasis, SubSysCouplingParametersBasis


class LocalSubSystemOptimData(OptimDataBasis):
    """Optimization data for local subsystems.

    Extends OptimDataBasis with local-specific data including local objectives,
    local constraints, coupling parameters, and local multipliers.
    """

    def __init__(self,
                 optimizer_type: str | None,
                 designvariables: List[float] | None,
                 designvariables_unscaled: List[float] | None,
                 lowerbounds: List[float] | None,
                 lowerbounds_scaled: List[float] | None,
                 upperbounds: List[float] | None,
                 upperbounds_scaled: List[float] | None,
                 Responses_unscaled: List[float] | None,
                 localobjectivevalue: float | None,
                 localobjectivevalue_unscaled: float | None,
                 totalobjectivevalue: float | None,
                 coordinationobjectivevalue: float | None,  # when running Matlab Optimizer, we do not have access to CoordinationObjectiveValue
                 equalitylocalconstraintsvalue: List[float]  | None,  # when running Matlab Optimizer, we do not have access to EqualiyLocalConstraintsValue
                 equalitylocalconstraintsvalue_unscaled: List[float] | None,
                 inequalitylocalconstraintsvalue: List[float] | None,  # when running Matlab Optimizer, we do not have access to InEqualityLocalConstraintsValue
                 inequalitylocalconstraintsvalue_unscaled: List[float] | None,
                 totalconstrainteqvalue: List[float] | None,
                 totalconstraintineqvalue: List[float] | None,
                 coordinationequalityconstraintvalue: List[float] | None,
                 coordinationinequalityconstraintvalue: List[float] | None,
                 couplingparameters: List[CouplingParametersBasis] | None,
                 gradient_localobjective: List[float | None] | None,
                 gradient_coordinationobjective: List[float | None] | None,
                 gradient_totalobjective: List[float | None] | None,
                 jacobian_localequalityconstraints: List[List[float | None]] | None,
                 jacobian_coordinationequalityconstraints: List[List[float | None]] | None,
                 jacobian_totalequalityconstraints: List[List[float | None]] | None,
                 jacobian_localinequalityconstraints: List[List[float | None]] | None,
                 jacobian_coordinationinequalityconstraints: List[List[float | None]] | None,
                 jacobian_totalinequalityconstraints: List[List[float | None]] | None,
                 jacobian_lowerbounds: List[List[float | None]] | None,
                 jacobian_upperbounds: List[List[float | None]] | None,
                 multipliers_lowerbounds: List[float] | None,
                 multipliers_upperbounds: List[float] | None,
                 multipliers_local_inequality_constraints: List[float] | None,
                 multipliers_local_equality_constraints: List[float] | None,
                 multipliers_coordination_equality_constraints: List[float] | None,
                 multipliers_coordination_inequality_constraints: List[float] | None,
                 activelocalinequalityconstraints: List[bool] | None,
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
        """Initialize LocalSubSystemOptimData.

        Args:
            optimizer_type: The type of optimizer algorithm used.
            designvariables: List of scaled design variable values in [0.0, 1.0].
            designvariables_unscaled: List of unscaled design variable values.
            Responses_unscaled: List of unscaled physical response values.
            localobjectivevalue: The scaled local objective value in [0.0, 1.0].
            localobjectivevalue_unscaled: The unscaled local objective value.
            totalobjectivevalue: The total objective function value.
            coordinationobjectivevalue: The coordination objective value, or None
                if not available (e.g., when running Matlab Optimizer).
            equalitylocalconstraintsvalue: List of scaled equality local constraint
                values in [-0.5, 0.5], or None if not available.
            equalitylocalconstraintsvalue_unscaled: List of unscaled equality local
                constraint values.
            inequalitylocalconstraintsvalue: List of scaled inequality local
                constraint values in [-0.5, 0.5], or None if not available.
            inequalitylocalconstraintsvalue_unscaled: List of unscaled inequality
                local constraint values, or None.
            totalconstrainteqvalue: List of total equality constraint values.
            totalconstraintineqvalue: List of total inequality constraint values.
            coordinationequalityconstraintvalue: List of coordination equality
                constraint values, or None if not available.
            exitflag: The exit flag indicating optimization convergence status.
            message: The optimization result message.
            optimization_numberofdesignvariableevaluations: Number of design
                variable evaluations during optimization.
            optimization_runtime: The runtime of the optimization in seconds.
            numberofactiveinequalityconstraints: Number of active inequality
                constraints, or None if not available.
            numberofactivebounds: Number of active bounds, or None if not available.
            lowerbounds: List of lower bound values for the design variables.
            lowerbounds_scaled: List of scaled lower bound values.
            upperbounds: List of upper bound values for the design variables.
            upperbounds_scaled: List of scaled upper bound values.
            coordinationinequalityconstraintvalue: List of coordination inequality
                constraint values, or None if not available.
            couplingparameters: List of coupling parameters objects.
            gradient_localobjective: Gradient of the local objective function.
            gradient_coordinationobjective: Gradient of the coordination objective.
            gradient_totalobjective: Gradient of the total objective function.
            jacobian_localequalityconstraints: Jacobian of local equality constraints.
            jacobian_coordinationequalityconstraints: Jacobian of coordination
                equality constraints.
            jacobian_totalequalityconstraints: Jacobian of total equality constraints.
            jacobian_localinequalityconstraints: Jacobian of local inequality
                constraints.
            jacobian_coordinationinequalityconstraints: Jacobian of coordination
                inequality constraints.
            jacobian_totalinequalityconstraints: Jacobian of total inequality
                constraints.
            jacobian_lowerbounds: Jacobian of the lower bounds.
            jacobian_upperbounds: Jacobian of the upper bounds.
            multipliers_lowerbounds: Multipliers for the lower bounds.
            multipliers_upperbounds: Multipliers for the upper bounds.
            multipliers_local_inequality_constraints: Multipliers for local
                inequality constraints.
            multipliers_local_equality_constraints: Multipliers for local
                equality constraints.
            multipliers_coordination_equality_constraints: Multipliers for
                coordination equality constraints.
            multipliers_coordination_inequality_constraints: Multipliers for
                coordination inequality constraints.
            activelocalinequalityconstraints: List of bools indicating active
                local inequality constraints.
            activecoordinationinequalityconstraints: List of bools indicating
                active coordination inequality constraints.
            activelowerbounds: List of bools indicating active lower bounds.
            activeupperbounds: List of bools indicating active upper bounds.
        """
        
        # Check for local subsystem if designvariables are in [0,1]
        # TODO: Maybe migrate back to OptimDataBasis
        if designvariables is not None:
            assert all(0.0 <= value <= 1.0 for value in designvariables), f"{DDO_Color}All design variables must be within the range [0.0, 1.0]{Reset}"
            
        super().__init__(optimizer_type=optimizer_type, 
                         designvariables=designvariables,
                         designvariables_unscaled=designvariables_unscaled,
                         lowerbounds=lowerbounds,
                         lowerbounds_scaled=lowerbounds_scaled,
                         upperbounds=upperbounds,
                         upperbounds_scaled=upperbounds_scaled,
                         totalobjectivevalue=totalobjectivevalue,
                         coordinationobjectivevalue=coordinationobjectivevalue,
                         totalconstrainteqvalue=totalconstrainteqvalue,
                         totalconstraintineqvalue=totalconstraintineqvalue,
                         coordinationequalityconstraintvalue=coordinationequalityconstraintvalue,
                         coordinationinequalityconstraintvalue=coordinationinequalityconstraintvalue,
                         couplingparameters=couplingparameters,
                         gradient_coordinationobjective=gradient_coordinationobjective,
                         jacobian_coordinationequalityconstraints=jacobian_coordinationequalityconstraints, 
                         jacobian_coordinationinequalityconstraints=jacobian_coordinationinequalityconstraints,
                         gradient_totalobjective=gradient_totalobjective,
                         jacobian_totalequalityconstraints=jacobian_totalequalityconstraints,
                         jacobian_totalinequalityconstraints=jacobian_totalinequalityconstraints,
                         jacobian_lowerbounds=jacobian_lowerbounds,
                         jacobian_upperbounds=jacobian_upperbounds,
                         multipliers_lowerbounds=multipliers_lowerbounds,
                         multipliers_upperbounds=multipliers_upperbounds,
                         multipliers_coordination_equality_constraints=multipliers_coordination_equality_constraints,
                         multipliers_coordination_inequality_constraints=multipliers_coordination_inequality_constraints,
                         activecoordinationinequalityconstraints=activecoordinationinequalityconstraints,
                         activelowerbounds=activelowerbounds,
                         activeupperbounds=activeupperbounds,
                         exitflag=exitflag,
                         message=message,
                         optimization_numberofdesignvariableevaluations=optimization_numberofdesignvariableevaluations,
                         optimization_runtime=optimization_runtime,
                         numberofactiveinequalityconstraints=numberofactiveinequalityconstraints,
                         numberofactivebounds=numberofactivebounds) 
        
        self._responses_unscaled = Responses_unscaled
        
        self._localobjectivevalue = localobjectivevalue
        self._localobjectivevalue_unscaled = localobjectivevalue_unscaled

        self._equalitylocalconstraintsvalue = equalitylocalconstraintsvalue
        self._equalitylocalconstraintsvalue_unscaled = equalitylocalconstraintsvalue_unscaled
        
        self._inequalitylocalconstraintsvalue = inequalitylocalconstraintsvalue
        self._inequalitylocalconstraintsvalue_unscaled = inequalitylocalconstraintsvalue_unscaled
        
        # Gradients / Jacobians of local quantities (objective, equality + inequality constraints, mappedresponses)
        self._gradient_localobjective: List[float | None] | None = gradient_localobjective
        self._jacobian_localequalityconstraints: List[List[float | None]] | None = jacobian_localequalityconstraints
        self._jacobian_localinequalityconstraints: List[List[float | None]] | None = jacobian_localinequalityconstraints
        
        # Check for local inequality constraints, if array of active constraints and of multipliers are consistent; 
        # i.e., both are None (and non-None) at the same entries
        
        # Violation for local inequality constraints
        if ((multipliers_local_inequality_constraints is not None and activelocalinequalityconstraints is not None) and
            any(multipliers_local_inequality_constraints[i] is None and activelocalinequalityconstraints[i] is True
                or multipliers_local_inequality_constraints[i] is not None and activelocalinequalityconstraints[i] is False
                for i in range(len(multipliers_local_inequality_constraints)))):
            
            raise ValueError(f"{DDO_Color}Your provided multipliers and activeness indicators for the local inequality constraints are not consistent: ", 
                             f"Multipliers for local inequality constraints: {multipliers_local_inequality_constraints}, ", 
                             f"Active local inequality constraints: {activelocalinequalityconstraints}{Reset}")
            
        self._multipliers_local_inequality_constraints: List[float] | None = multipliers_local_inequality_constraints
        self._multipliers_local_equality_constraints: List[float] | None = multipliers_local_equality_constraints
        
        self._activelocalinequalityconstraints: List[bool] | None = activelocalinequalityconstraints


    def set_Responses_Unscaled(self, Responses_unscaled_in: List[float]) -> None:
        """Set the unscaled physical responses.

        Args:
            Responses_unscaled_in: Unscaled physical responses.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._responses_unscaled = copy.copy(Responses_unscaled_in)

    def get_Responses_Unscaled(self) -> List[float]:
        """Get the unscaled response values.

        Returns:
            The unscaled physical response values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._responses_unscaled)

    def set_LocalObjectiveValue(self, localobjectivevalue_in: float) -> None:
        """Set the local objective function value.

        Args:
            localobjectivevalue_in: Local objective function value.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning the input value directly is safe because any subsequent changes
        # to the caller's variable cannot affect this class's attribute.

        self._localobjectivevalue = localobjectivevalue_in

    def get_LocalObjectiveValue(self) -> float | None:  # when running Matlab Optimizer, we do not have access to LocalObjectiveValue
        """Gets the scaled local objective function value.

        Returns:
            The local objective value scaled to [0.0, 1.0], or None if not
            available (e.g., when running Matlab Optimizer).
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._localobjectivevalue

    def set_LocalObjectiveValue_Unscaled(self, localobjectivevalue_unscaled_in: float) -> None:
        """Set the unscaled local objective function value.

        Args:
            localobjectivevalue_unscaled_in: Unscaled local objective function value.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning the input value directly is safe because any subsequent changes
        # to the caller's variable cannot affect this class's attribute.
        self._localobjectivevalue_unscaled = localobjectivevalue_unscaled_in

    def get_LocalObjectiveValue_Unscaled(self) -> float | None:  # when running Matlab Optimizer, we do not have access to LocalObjectiveValue
        """Gets the unscaled local objective function value.

        Returns:
            The unscaled local objective value, or None if not available
            (e.g., when running Matlab Optimizer).
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._localobjectivevalue_unscaled

    def set_EqualityLocalConstraintsValue(self, equalitylocalconstraintsvalue_in: List[float]) -> None:
        """Set the equality local constraint values.

        Args:
            equalitylocalconstraintsvalue_in: Equality local constraint values.
        """

        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._equalitylocalconstraintsvalue = copy.copy(equalitylocalconstraintsvalue_in)

    def get_EqualityLocalConstraintsValue(self) -> List[float] | None:  # when running Matlab Optimizer, we do not have access to EqualiyLocalConstraintsValue
        """Gets the scaled equality local constraint values.

        Returns:
            List of equality constraint values scaled to [-0.5, 0.5], or None
            if not available (e.g., when running Matlab Optimizer).
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._equalitylocalconstraintsvalue)

    def set_EqualityLocalConstraintsValue_Unscaled(self, equalitylocalconstraintsvalue_unscaled_in: List[float]) -> None:
        """Set the unscaled equality local constraint values.

        Args:
            equalitylocalconstraintsvalue_unscaled_in: Unscaled equality local
                constraint values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._equalitylocalconstraintsvalue_unscaled = copy.copy(equalitylocalconstraintsvalue_unscaled_in)

    def set_InequalityLocalConstraintsValue(self, inequalitylocalconstraintsvalue_in: List[float]) -> None:
        """Set the inequality local constraint values.

        Args:
            inequalitylocalconstraintsvalue_in: Inequality local constraint values.
        """

        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._inequalitylocalconstraintsvalue = copy.copy(inequalitylocalconstraintsvalue_in)

    def get_InequalityLocalConstraintsValue(self) -> List[float] | None:  # when running Matlab Optimizer, we do not have access to InEqualityLocalConstraintsValue
        """Gets the scaled inequality local constraint values.

        Returns:
            List of inequality constraint values scaled to [-0.5, 0.5], or None
            if not available (e.g., when running Matlab Optimizer).
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._inequalitylocalconstraintsvalue)

    def set_InequalityLocalConstraintsValue_Unscaled(self, inequalitylocalconstraintsvalue_unscaled_in: List[float]) -> None:
        """Set the unscaled inequality local constraint values.

        Args:
            inequalitylocalconstraintsvalue_unscaled_in: Unscaled inequality
                local constraint values.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._inequalitylocalconstraintsvalue_unscaled = copy.copy(inequalitylocalconstraintsvalue_unscaled_in)

    def set_Gradient_LocalObjective(self, gradient_localobjective_in: List[float | None]) -> None:
        """Set the gradient of the local objective.

        Args:
            gradient_localobjective_in: Gradient of the local objective function.
        """
        
        # Check if local objective exists
        if self.get_LocalObjectiveValue() is None:
            
            # There does not exist the local objective
            raise ValueError(f"{DDO_Color}There does not exist a local objective{Reset}")
        
        # Check if the input has correct dimension
        if np.array(gradient_localobjective_in).shape[0] != (len(self.get_DesignVariables())):
            
            # The dimensions do not match
            raise ValueError(f"{DDO_Color}The dimension of your provided gradient of the local objective is incorrect; ",  
                             f"expected: {(len(self.get_DesignVariables()))}, provided: {np.array(gradient_localobjective_in).shape}{Reset}")
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._gradient_localobjective = copy.copy(gradient_localobjective_in)

    def get_Gradient_LocalObjective(self) -> List[float | None] | None:
        """Get the gradient of the local objective.

        Returns:
            The gradient of the local objective, or None if not available.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._gradient_localobjective)

    def set_Jacobian_LocalEqualityConstraints(self, jacobian_localequalityconstraints_in: List[List[float | None]]) -> None:
        """Set the Jacobian of the local equality constraints.

        Args:
            jacobian_localequalityconstraints_in: Jacobian of the local
                equality constraints.
        """
        
        # Check if local equality constraints exist
        if self.get_EqualityLocalConstraintsValue() is None:
            
            # There does not exist any local equality constraint
            raise ValueError(f"{DDO_Color}There does not exist a local equality constraint{Reset}")
        
        # Check if the input has correct dimension
        if np.array(jacobian_localequalityconstraints_in).shape != (len(self.get_EqualityLocalConstraintsValue()), len(self.get_DesignVariables())):
            
            # The dimensions do not match
            raise ValueError(f"{DDO_Color}The dimensions of your provided Jacobian of the local equality constraints are incorrect; ",  
                             f"expected: {(len(self.get_EqualityLocalConstraintsValue()), len(self.get_DesignVariables()))}, ",
                             f"provided: {np.array(jacobian_localequalityconstraints_in).shape}{Reset}")
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._jacobian_localequalityconstraints = copy.deepcopy(jacobian_localequalityconstraints_in)

    def get_Jacobian_LocalEqualityConstraints(self) -> List[List[float | None]] | None:
        """Get the Jacobian of the local equality constraints.

        Returns:
            The Jacobian of the local equality constraints, or None if not available.
        """
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_localequalityconstraints)

    def set_Jacobian_LocalInequalityConstraints(self, jacobian_localinequalityconstraints_in: List[List[float | None]]) -> None:
        """Set the Jacobian of the local inequality constraints.

        Args:
            jacobian_localinequalityconstraints_in: Jacobian of the local
                inequality constraints.
        """
        
        # Check if local inequality constraints exist
        if self.get_InequalityLocalConstraintsValue() is None:
            
            # There does not exist any local inequality constraint
            raise ValueError(f"{DDO_Color}There does not exist a local inequality constraint{Reset}")
        
        # Check if the input has correct dimension
        if np.array(jacobian_localinequalityconstraints_in).shape != (len(self.get_InequalityLocalConstraintsValue()), len(self.get_DesignVariables())):
            
            # The dimensions do not match
            raise ValueError(f"{DDO_Color}The dimensions of your provided Jacobian of the local inequality constraints are incorrect; ",  
                             f"expected: {(len(self.get_InequalityLocalConstraintsValue()), len(self.get_DesignVariables()))}, ",
                             f"provided: {np.array(jacobian_localinequalityconstraints_in).shape}{Reset}")
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._jacobian_localinequalityconstraints = copy.deepcopy(jacobian_localinequalityconstraints_in)

    def get_Jacobian_LocalInequalityConstraints(self) -> List[List[float | None]] | None:
        """Get the Jacobian of the local inequality constraints.

        Returns:
            The Jacobian of the local inequality constraints, or None if not available.
        """
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_localinequalityconstraints)

    def get_LocalCouplingParameters(self) -> List[SubSysCouplingParametersBasis] | None:
        """Get the local <-> local coupling parameters (excluding controller couplings).

        Returns:
            List of local coupling parameters, or None if no local <-> local
            couplings exist.
        """
        # No copy.copy() used - List[SubSysCouplingParametersBasis] is a list of class objects
        # returned by reference intentionally. This allows the caller to interact with
        # the actual objects. If isolation is needed, the caller should explicitly copy.
        
        # Get all couplingparameters
        couplingparameters: List[CouplingParametersBasis] = self.get_CouplingParameters()
        
        # Filter to keep only local <-> local coupling parameters (SubSysCouplingParametersBasis),
        # excluding any local <-> controller coupling parameters
        local_couplingparameters: List[SubSysCouplingParametersBasis] = [couplingparameter for couplingparameter in couplingparameters
                                                                         if isinstance(couplingparameter, SubSysCouplingParametersBasis)]
        
        # Return None if no local <-> local couplings exist, otherwise return the list
        return local_couplingparameters if local_couplingparameters else None        

    def get_CouplingParameter(self, id: str) -> SubSysCouplingParametersBasis | None:
        """Get the coupling parameter associated with id, if it is a local <-> local coupling.

        Args:
            id: The coupling parameter ID to search for.

        Returns:
            The coupling parameter matching the ID.
        """
        # No copy.copy() used - SubSysCouplingParametersBasis is a class object
        # returned by reference intentionally. This allows the caller to interact with
        # the actual object. If isolation is needed, the caller should explicitly copy.
        
        # Get all coupling parameters
        couplingparameters: List[CouplingParametersBasis] = self.get_CouplingParameters()
        
        # Iterate over the coupling parameters to 
        # find the one associated with id
        
        for couplingparameter in couplingparameters:
            
            # Check if the couplingparameter corresponds to a local <-> local coupling
            if isinstance(couplingparameter, SubSysCouplingParametersBasis) and couplingparameter.get_ID() == id:
                
                # Return the couplingparameter
                return couplingparameter
        
        # If the code reached here, the given id could not be identified
        raise ValueError(f"{DDO_Color}There is no coupling with your provided ID ({id}){Reset}")

    def get_Jacobian_MappedResponse(self, id: str) -> List[List[float | None]] | None:
        """Get the Jacobian of the mapped responses for the coupling with given ID.

        Args:
            id: The coupling parameter ID.

        Returns:
            The Jacobian of the mapped responses, or None if not available.
        """
        
        # Get the coupling parameter with the corresponding ID
        couplingparameter: SubSysCouplingParametersBasis = self.get_CouplingParameter(id) 
        
        # Return the Jacobian of the mapped response
        return couplingparameter.get_Jacobian_MappedResponse()

    def set_Jacobian_MappedResponses(self, id: str, jacobian_mappedresponses_in: List[List[float | None]]) -> None:
        """Set the Jacobian of the mapped responses associated with id.

        Args:
            id: The coupling parameter ID.
            jacobian_mappedresponses_in: Jacobian of the mapped responses.
        """
        
        # Get all couplingparameters
        couplingparameter: SubSysCouplingParametersBasis = self.get_CouplingParameter(id)
        
        # Check if there exist mapped responses in this coupling
        if couplingparameter.get_MappedResponses() is None:
            
            # Since there are no mapped responses, there should also be no Jacobian
            raise ValueError(f"{DDO_Color}There exist no mapped responses in the coupling associated with ID {id} that you provided; hence, no Jacobian of the mapped responses{Reset}")
        
        # If the mapped responses exist
        
        # Check correct dimensions
        if np.array(jacobian_mappedresponses_in).shape != (len(couplingparameter.get_MappedResponses()), len(self.get_DesignVariables())):
            
            # Dimensions to not match
            raise ValueError(f"{DDO_Color}The dimensions of your provided Jacobian of the mapped response to subsystem {id} are incorrect; ",
                             f" expected: {(len(couplingparameter.get_MappedResponses()), len(self.get_DesignVariables()))}, ",
                             f"provided: {np.array(jacobian_mappedresponses_in).shape}{Reset}")
        
        # Set the Jacobian of the mapped responses of this couplingparameter
        couplingparameter.set_Jacobian_MappedResponse(jacobian_mappedresponses_in)        

    def set_Multipliers_Local_Inequality_Constraints(self, multipliers_localinequalityconstraints_in: List[float | None]) -> None:
        """Set the multipliers for the local inequality constraints.

        Args:
            multipliers_localinequalityconstraints_in: Multipliers for local
                inequality constraints.
        """

        # Check if local inequality constraints exist
        if self.get_InequalityLocalConstraintsValue() is None:
            
            # There does not exist any local inequality constraint
            raise ValueError(f"{DDO_Color}There does not exist a local inequality constraint{Reset}")
        
        # Get the active lower bounds
        activelocalinequalityconstraints: List[bool] = self.get_ActiveLocalInequalityConstraints()
        
        # Check if the dimensions match
        if len(multipliers_localinequalityconstraints_in) != len(self.get_InequalityLocalConstraintsValue()):
            
            # The dimensions do not match
            raise ValueError(f"{DDO_Color}The dimension of your provided multipliers w.r.t to the local inequality constraints is incorrect; ", 
                             f"expected: {len(self.get_InequalityLocalConstraintsValue())}, provided: {len(multipliers_localinequalityconstraints_in)}{Reset}")

        # Check if for inactive local inequality constraints, the corresponding multipliers are None
        if any(multipliers_localinequalityconstraints_in[i] is not None and activelocalinequalityconstraints[i] is False 
               for i in range(len(multipliers_localinequalityconstraints_in))):
            
            # If there is an inactive constraint for which the multiplier is not None
            raise ValueError(f"{DDO_Color}Your multiplier w.r.t. the local inequality constraints is incorrect, ", 
                             "since you provided multipliers for inactive inequality constraints.", 
                             f"Your multipliers for local inequality constraints: {multipliers_localinequalityconstraints_in}, ",
                             f"Active lower bounds: {activelocalinequalityconstraints}{Reset}")
        
        # Check if for active local inequality constraints, the corresponding multipliers are not None
        if any(multipliers_localinequalityconstraints_in[i] is None and activelocalinequalityconstraints[i] is True 
               for i in range(len(multipliers_localinequalityconstraints_in))):
            
            # If there is such a None-multiplier for an active constraint
            raise ValueError(f"{DDO_Color}Your provided multiplier is None for an active constraint. ", 
                             f"Your multipliers for local inequality constraints: {multipliers_localinequalityconstraints_in}, ",
                             f"Active lower bounds: {activelocalinequalityconstraints}{Reset}")
        
        # Check if the multipliers are non-negative for the active inequality constraints
        if any(activelocalinequalityconstraints[i] is True and multipliers_localinequalityconstraints_in[i] < 0 
               for i in range(len(multipliers_localinequalityconstraints_in))):
            
            # All multipliers for active constraints are non-negative
            raise ValueError(f"{DDO_Color}Your provided multipliers need to be non-negative for active local inequality constraints{Reset}")
        
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_local_inequality_constraints = copy.copy(multipliers_localinequalityconstraints_in)

    def get_Multipliers_Local_Inequality_Constraints(self) -> List[float | None] | None:
        """Get the multipliers for the local inequality constraints.

        Returns:
            Multipliers for local inequality constraints, or None if not set.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_local_inequality_constraints)

    def set_Multipliers_Local_Equality_Constraints(self, multipliers_localequalityconstraints_in: List[float | None]) -> None:
        """Set the multipliers for the local equality constraints.

        Args:
            multipliers_localequalityconstraints_in: Multipliers for local
                equality constraints.
        """
        
        # Check if local equality constraints exist
        if self.get_EqualityLocalConstraintsValue() is None:
            
            # There does not exist any local equality constraint
            raise ValueError(f"{DDO_Color}There does not exist any local equality constraint{Reset}")
        
        # Check dimensions
        if len(multipliers_localequalityconstraints_in) != len(self.get_EqualityLocalConstraintsValue()):
            
            # Wrong dimension
            raise ValueError(f"{DDO_Color}Your provided multipliers w.r.t local equality constraints have the wrong dimensions. ",
                             f"expected: {len(self.get_EqualityLocalConstraintsValue())}, ",
                             f"provided: {len(multipliers_localequalityconstraints_in)}{Reset}")
        
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_local_equality_constraints = copy.copy(multipliers_localequalityconstraints_in)

    def get_Multipliers_Local_Equality_Constraints(self) -> List[float | None] | None:
        """Get the multipliers for the local equality constraints.

        Returns:
            Multipliers for local equality constraints, or None if not set.
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_local_equality_constraints)

    def set_ActiveLocalInequalityConstraints(self, activelocalinequalityconstraints_in: List[bool]) -> None:
        """Set the list of bools indicating active local inequality constraints.

        Args:
            activelocalinequalityconstraints_in: Active local inequality
                constraints.
        """
        # copy.copy() used - List[bool] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._activelocalinequalityconstraints = copy.copy(activelocalinequalityconstraints_in)

    def get_ActiveLocalInequalityConstraints(self) -> List[bool] | None:
        """Get the list of bools indicating active local inequality constraints.

        Returns:
            Active local inequality constraints, or None if not available.
        """
        # copy.copy() used - List[bool] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._activelocalinequalityconstraints)

    def _print_local_specific(self) -> None:
        """Print local-subsystem-specific optimizer results."""
        resp = self.get_Responses_Unscaled()
        index_width = len(f"[{len(resp) - 1}]")
        ddo_print(f"       {'Responses Unscaled:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {'[0]'.ljust(index_width)} {resp[0]}")
        for i, v in enumerate(resp[1:], start=1):
            ddo_print(f"       {' ' * self._DDO_PRINT_LABEL_WIDTH} {f'[{i}]'.ljust(index_width)} {v}")
        ddo_print(f"       {'Local Objective Value:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self.get_LocalObjectiveValue()}")
        ddo_print(f"       {'Local Obj. Value Unscaled:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self.get_LocalObjectiveValue_Unscaled()}")

    def print_results(self) -> None:
        """Print local subsystem optimizer results."""
        self._print_solver_and_designvariables()
        self._print_local_specific()
        ddo_print(f"       {'Total Objective Value:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self.get_TotalObjectiveValue()}")

```
