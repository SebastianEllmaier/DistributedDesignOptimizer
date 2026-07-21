---
title: FiniteDifferencesJacobian (Source)
---

← Back to [FiniteDifferencesJacobian documentation](FiniteDifferencesJacobian.md)

# FiniteDifferencesJacobian - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\tools\FiniteDifferencesJacobian.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Finite differences Jacobian computation module.

This module provides utilities for computing Jacobians using
finite difference approximations.
"""

from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive
from typing import List, Dict
import copy
from Distributed_Design_Optimizer.subsystem import SubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis

from Distributed_Design_Optimizer.subsystem.couplingparameters import CouplingParametersInterface
from Distributed_Design_Optimizer.subsystem.couplingparameters import SubSysCouplingParametersBasis

class FiniteDifferencesJacobian():
    """
    Compute finite differences Jacobian approximations.
    """
    def __init__(self) -> None:
        
        """
        Instantiates placeholders for Jacobians / gradient of local constraints and local objective.
        """
        
        # Gradient of the local objective
        self._gradient_localobjective: List[float | None] | None = None
        
        # Gradient of the coordination objective
        self._gradient_coordinationobjective: List[float | None] | None = None
        
        # Jacobian of the local equality constraints
        self._jacobian_localequalityconstraints: List[List[float | None]] | None = None
        
        # Jacobian of the coordination equality constraints
        self._jacobian_coordinationequalityconstraints: List[List[float | None]] | None = None
        
        # Jacobian of the local inequality constraints
        self._jacobian_localinequalityconstraints: List[List[float | None]] | None = None
        
        # Jacobian of the coordination inequality constraints
        self._jacobian_coordinationinequalityconstraints: List[List[float | None]] | None = None
        
        # Jacobian of the mapped responses
        self._jacobians_mappedresponses: Dict[str, List[List[float | None]]] | None = None

##################################################################    
#  Getters and setters
##################################################################

    def get_Gradient_LocalObjective(self) -> List[float | None] | None:
        """
        Returns the gradient approximation of the local objective.

        Returns:
            List[float]: _description_
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._gradient_localobjective)
    
    def set_Gradient_LocalObjective(self, gradient_localobjective_in: List[float | None]):
        """
        Sets the gradient approximation of the local objective.

        Args:
            gradient_localobjective_in (List[float]): _description_
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._gradient_localobjective = copy.copy(gradient_localobjective_in)
        
    def get_Gradient_CoordinationObjective(self) -> List[float | None] | None:
        """
        Returns the gradient approximation of the local objective.

        Returns:
            List[float | None] | None: _description_
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._gradient_coordinationobjective)
    
    def set_Gradient_CoordinationObjective(self, gradient_coordinationobjective_in: List[float | None]):
        """
        Sets the gradient approximation of the coordination objective.

        Args:
            gradient_coordinationobjective_in (List[float  |  None]): _description_
        """
        # copy.copy() used - List[float | None] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._gradient_coordinationobjective = copy.copy(gradient_coordinationobjective_in)
        
    def get_Jacobian_LocalEqualityConstraints(self) -> List[List[float | None]] | None:
        """
        Returns the Jacobian approximation of the local equality constraints.

        Returns:
            List[List[float]]: _description_
        """
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_localequalityconstraints)
    
    def set_Jacobian_LocalEqualityConstraints(self, jacobian_localequalityconstraints_in: List[List[float | None]]) -> None:
        """
        Sets the Jacobian approximation of the local equality constraints.

        Args:
            jacobian_localequalityconstraints_in (List[List[float]]): _description_
        """
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_localequalityconstraints = copy.deepcopy(jacobian_localequalityconstraints_in)
    
    def get_Jacobian_CoordinationEqualityConstraints(self) -> List[List[float | None]] | None:
        """
        Returns the Jacobian approximation of the coordination equality constraints.

        Returns:
            List[List[float | None]] | None: _description_
        """
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_coordinationequalityconstraints)
    
    def set_Jacobian_CoordinationEqualityConstraints(self, jacobian_coordinationequalityconstraints_in: List[List[float | None]]) -> None:
        """
        Sets the Jacobian approximation of the coordination equality constraints.

        Args:
            jacobian_coordinationequalityconstraints_in (List[List[float | None]]): _description_
        """
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_coordinationequalityconstraints = copy.deepcopy(jacobian_coordinationequalityconstraints_in)
        
    def get_Jacobian_LocalInEqualityConstraints(self) -> List[List[float | None]] | None:
        """
        Returns the Jacobian approximation of the local inequality constraints.

        Returns:
            List[List[float]]: _description_
        """
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_localinequalityconstraints)
    
    def set_Jacobian_LocalInEqualityConstraints(self, jacobian_localinequalityconstraints_in: List[List[float | None]]) -> None:
        """
        Sets the Jacobian approximation of the local inequality constraints.

        Args:
            jacobian_localinequalityconstraints_in (List[List[float]]): _description_
        """
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_localinequalityconstraints = copy.deepcopy(jacobian_localinequalityconstraints_in)
    
    def get_Jacobian_CoordinationInEqualityConstraints(self) -> List[List[float | None]] | None:
        """
        Returns the Jacobian approximation of the coordination inequality constraints.

        Returns:
            List[List[float | None]] | None: _description_
        """
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobian_coordinationinequalityconstraints)
    
    def set_Jacobian_CoordinationInEqualityConstraints(self, jacobian_coordinationinequalityconstraints_in: List[List[float | None]]) -> None:
        """
        Sets the Jacobian approximation of the coordination inequality constraints.

        Args:
            jacobian_coordinationinequalityconstraints_in (List[List[float  |  None]]): _description_
        """
        # copy.deepcopy() used - List[List[float | None]] is mutable (nested list). This prevents
        # modifications in the caller from being reflected back to the class attribute.
        self._jacobian_coordinationinequalityconstraints = copy.deepcopy(jacobian_coordinationinequalityconstraints_in)
        
    def get_Jacobians_MappedResponses(self) -> Dict[str, List[List[float | None]]] | None:
        """
        Get the Jacobian approximation of the mapped responses.

        Returns:
            Dict[str, List[List[float | None]]]: _description_
        """
        # copy.deepcopy() used - Dict[str, List[List[float | None]]] is mutable (nested structure).
        # This prevents modifications in the caller from being reflected back to the class attribute.
        return copy.deepcopy(self._jacobians_mappedresponses)
        
    def set_Jacobians_MappedResponses(self, jacobians_mappedresponses_in: Dict[str, List[List[float | None]]]) -> None:
        """
        Sets the Jacobian approximation of the mapped responses.

        Args:
            jacobians_mappedresponses_in (Dict[str, List[List[float  |  None]]]): _description_
        """
        # copy.deepcopy() used - Dict[str, List[List[float | None]]] is mutable (nested structure).
        # This prevents modifications in the caller from being reflected back to the class attribute.
        self._jacobians_mappedresponses = copy.deepcopy(jacobians_mappedresponses_in)


    def run(self, subsystem: SubSystemBasis, perturbation_directions_indices_list: List[int]) -> None:
        """
        Computes the finite difference jacobian approximations and stores them.
        
        This is needed of all the following quantities: 
            - Gradient of local objective
            - Jacobian of local equality constraints
            - Jacobian of local inequality constraints
            - Jacobian of mapped responses

        Args:
            subsystem (SubSystemBasis): The subsystem to compute Jacobians for.
            perturbation_directions_indices_list (List[int]): Indices of design
                variable directions in which to compute finite differences.
        """
    
        # Store the data that is needed to restore the original state of 
        # the subsystem
        
        # Design variables
        # No copy.copy() needed - subsystem.get_DesignVariables() already returns a defensive copy
        original_designvariables: List[float] = subsystem.get_DesignVariables()  # These are [0,1]-scaled design variables
        dimension_designvariables: int = len(original_designvariables) 
        
        # Scalings
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        
        # Bounds
        
        lowerbounds: List[float] = subsystem.get_LowerBounds_Unscaled()
        lowerbounds_scaled: List[float] = [scalers[i].transform(lowerbounds[i]) for i in range(dimension_designvariables)]
        
        upperbounds: List[float] = subsystem.get_UpperBounds_Unscaled()
        upperbounds_scaled: List[float] = [scalers[i].transform(upperbounds[i]) for i in range(dimension_designvariables)]
        
        # Determine the mesh discretization based on user-specified granularity 
        # for difference quotients
        
        # initialize mesh size arrays with correct dimensions
        epsilon_scaled = [None] * dimension_designvariables
        granularities: List[float] = subsystem.get_DesignVariables_Granularity()
        
        # Loop over each component
        for i in range(dimension_designvariables):
            
            # Infer discretization
            
            # If the design variable component is continuous (0.0 means continuous)
            if granularities[i] == 0.0:
                
                # 1E-8 as minimal choice for continuous variables    
                epsilon_scaled[i] = 1E-8

            # If a discrete, positive granularity was chosen
            elif granularities[i] > 0.0:
                
                # Take the corresponding granularity as epsilon
                epsilon_scaled[i] = granularities[i]
            
            # If the granularity does not match any continuous or
            # discrete values
            else:
                
                # Inputs are not conform with the specification of usage
                raise ValueError(f"{DDO_Color}Invalid granularity at index {i} for subsystem {subsystem.get_SUBSYSTEMID()}: {granularities[i]}. Must be >= 0.0 (0.0 means continuous){Reset}")
        
        
        # Initialize List[List[float]] / List[float] for each of the quantities 
        # which we want to approximate of correct dimensions with None
        
        # Gradient of the local objective
        gradient_localobjective: List[float | None] | None
        
        if subsystem.get_LocalObjectiveValue() is None:
            gradient_localobjective = None
        else:
            gradient_localobjective = [None for j in range(dimension_designvariables)]

        # Gradient of the coordination objective
        gradient_coordinationobjective: List[float | None] | None
        
        if subsystem.get_CoordinationObjectiveValue() is None:
            gradient_coordinationobjective = None
        else:
            gradient_coordinationobjective = [None for j in range(dimension_designvariables)]
        
        # Jacobian of the local equality constraints
        jacobian_localequalityconstraints: List[List[float | None]] | None
        
        if subsystem.get_EqualityLocalConstraintsValue() is None:
            jacobian_localequalityconstraints = None
        else:
            jacobian_localequalityconstraints = [[None for j in range(dimension_designvariables)] for i in range(len(subsystem.get_EqualityLocalConstraintsValue()))]
        
        # Jacobian of the coordination equality constraints
        jacobian_coordinationequalityconstraints: List[List[float | None]] | None = None
        
        if subsystem.get_CoordinationEqualityConstraintValue() is None:
            jacobian_coordinationequalityconstraints = None
        else:
            jacobian_coordinationequalityconstraints = [[None for j in range(dimension_designvariables)] for i in range(len(subsystem.get_CoordinationEqualityConstraintValue()))]
        
        # Jacobian of the local inequality constraints
        jacobian_localinequalityconstraints: List[List[float | None]] | None
        
        if subsystem.get_InequalityLocalConstraintsValue() is None:
            jacobian_localinequalityconstraints = None
        else:
            jacobian_localinequalityconstraints = [[None for j in range(dimension_designvariables)] for i in range(len(subsystem.get_InequalityLocalConstraintsValue()))]
        
        # Jacobian of the coordination inequality constraints
        jacobian_coordinationinequalityconstraints: List[List[float | None]] | None = None
        
        if subsystem.get_CoordinationInequalityConstraintValue() is None:
            jacobian_coordinationinequalityconstraints = None
        else:
            jacobian_coordinationinequalityconstraints = [[None for j in range(dimension_designvariables)] for i in range(len(subsystem.get_CoordinationInequalityConstraintValue()))]
        
        # Jacobians of the mapped responses
        jacobians_mappedresponses: Dict[str, List[List[float | None]] | None] = {}
        
        # Initialize each jacobian of the mapped responses
        neighborids: List[str] = subsystem.get_NeighborId()
        couplingparameters: List[CouplingParametersInterface] = subsystem.get_CouplingParameters()
        
        for neighbor_index in range(len(neighborids)):
            
            # Get the corresponding coupling parameter
            couplingparameter: CouplingParametersInterface = couplingparameters[neighbor_index]
            
            # Get the corresponding ID
            neighborid: str = couplingparameter.get_ID()
            
            # If the coupling is between local subsystems
            if isinstance(couplingparameter, SubSysCouplingParametersBasis):
                
                # Get the mapped responses associated to this coupling
                mappedresponses: List[float] | None = couplingparameter.get_MappedResponses()
                
                # Check if mapped responses exist
                if mappedresponses is not None:
                    
                    # Initialize the corresponding Jacobian
                    jacobians_mappedresponses[neighborid] = [[None for j in range(dimension_designvariables)] for i in range(len(mappedresponses))]
                
                else:
                    
                    # Initialize the corresponding Jacobian to None
                    jacobians_mappedresponses[neighborid] = None
        
        # Compute the Jacobian approximations  
        
        # Create a local objective copy
        # No copy.copy() needed - float is immutable
        localobjective: float | None = subsystem.get_LocalObjectiveValue()
        
        if gradient_localobjective is not None:
            # No copy.copy() needed - float is immutable
            perturbed_localobjective_left: float = localobjective
            perturbed_localobjective_right: float = localobjective
            
        # Create a coordination objective copy
        # No copy.copy() needed - float is immutable
        coordinationobjective: float | None = subsystem.get_CoordinationObjectiveValue()

        if gradient_coordinationobjective is not None:
            # No copy.copy() needed - float is immutable
            perturbed_coordinationobjective_left: float = coordinationobjective
            perturbed_coordinationobjective_right: float = coordinationobjective
        # No copy.copy() needed - subsystem.get_EqualityLocalConstraintsValue() already returns a defensive copy
        localequalityconstraints: List[float] | None = subsystem.get_EqualityLocalConstraintsValue()
        
        if jacobian_localequalityconstraints is not None:
            # Two independent copies needed for left/right perturbation tracking.
            # Although getter already returns a defensive copy, we need copy.copy() on both
            # assignments to ensure left and right are independent lists.
            perturbed_localequalityconstraints_left: List[float] = copy.copy(localequalityconstraints)
            perturbed_localequalityconstraints_right: List[float] = copy.copy(localequalityconstraints)
        
        # Create a coordination equality constraints copy
        # No copy.copy() needed - subsystem.get_CoordinationEqualityConstraintValue() already returns a defensive copy
        coordinationequalityconstraints: List[float] | None = subsystem.get_CoordinationEqualityConstraintValue()
        
        if jacobian_coordinationequalityconstraints is not None:
            # Two independent copies needed for left/right perturbation tracking.
            # Although getter already returns a defensive copy, we need copy.copy() on both
            # assignments to ensure left and right are independent lists.
            perturbed_coordinationequalityconstraints_left: List[float] = copy.copy(coordinationequalityconstraints)
            perturbed_coordinationequalityconstraints_right: List[float] = copy.copy(coordinationequalityconstraints)
        
        # Create a local inequality constraints copy
        # No copy.copy() needed - subsystem.get_InequalityLocalConstraintsValue() already returns a defensive copy
        localinequalityconstraints: List[float] | None = subsystem.get_InequalityLocalConstraintsValue()
        
        if jacobian_localinequalityconstraints is not None:
            perturbed_localinequalityconstraints_left: List[float] = copy.copy(localinequalityconstraints)
            perturbed_localinequalityconstraints_right: List[float] = copy.copy(localinequalityconstraints)
                        
        # Create a coordination inequality constraints copy
        # No copy.copy() needed - subsystem.get_CoordinationInequalityConstraintValue() already returns a defensive copy
        coordinationinequalityconstraints: List[float] | None = subsystem.get_CoordinationInequalityConstraintValue()

        if jacobian_coordinationinequalityconstraints is not None:
            perturbed_coordinationinequalityconstraints_left: List[float] = copy.copy(coordinationinequalityconstraints)
            perturbed_coordinationinequalityconstraints_right: List[float] = copy.copy(coordinationinequalityconstraints)

        # Create a mapped responses dictionary, where only neighbor ids are keys 
        # if there exists mapped response associated to that i <-> j coupling
        perturbed_mappedresponses_left: Dict[str, List[float]] = {}
        perturbed_mappedresponses_right: Dict[str, List[float]] = {}
                
        for neighbor_index in range(len(neighborids)):
            
            # Get the corresponding coupling parameter
            couplingparameter: CouplingParametersInterface = couplingparameters[neighbor_index]
            
            # Get the corresponding ID
            neighborid: str = couplingparameter.get_ID()
            
            # If the coupling is between local subsystems
            if isinstance(couplingparameter, SubSysCouplingParametersBasis):
                
                # Get the mapped responses associated to this coupling
                mappedresponse: List[float] | None = couplingparameter.get_MappedResponses()
                
                # Check if mapped responses exist
                if mappedresponse is not None:
                    
                    # Two independent copies needed for left/right perturbation tracking.
                    # Although get_MappedResponseVariables() returns a defensive copy, we need
                    # copy.copy() on both assignments to ensure left and right are independent lists.
                    perturbed_mappedresponses_left[neighborid] = copy.copy(mappedresponse)
                    perturbed_mappedresponses_right[neighborid] = copy.copy(mappedresponse)

        # Create a designvariable copy for the perturbed vectors
        # Left returns to the terms that are usually on the left sides 
        # of both numerator and dneominator of the difference quotient
        # Right accordingly to the right side terms
        # Two independent copies needed for left/right perturbation tracking.
        # Although original_designvariables is already a defensive copy from the getter,
        # we need copy.copy() on both assignments to ensure left and right are independent lists.
        perturbed_designvariables_left = copy.copy(original_designvariables)
        perturbed_designvariables_right = copy.copy(original_designvariables)
        
        # TODO: Think about alternatives, where if upper or lower bound violated 
        # for perturbed in difference quotient "... - ... / ()... - ...)", then project d + epsilon to bound boundary
        # Currently, uses evaluation at d directly
        
        # Loop over the directions in which finite differences should be 
        # applied
        for j in perturbation_directions_indices_list:
            
            # Stepsize of difference gradients, depending on bounds' boundaries
            # If the bounds are nearby, currently, our stepsize will stay as zero
            # In future, add stepsize reduction
            stepsize = 0.0

            # Create a local objective copy
            
            # Based on bounds, determine appropriate perturbations
            if upperbounds_scaled[j] is not None and original_designvariables[j] + epsilon_scaled[j] <= upperbounds_scaled[j]:
                
                # The j-th component of the current designvariables is near the upper bound
                # Hence, Backwards differentiation
                perturbed_designvariables_left[j] += epsilon_scaled[j]
                
                # Update the subsystem based on the perturbation
                self.updateSubsystem(subsystem, perturbed_designvariables_left)
                
                # Get the needed quantities, if they exist
                
                perturbed_designvariables_left = subsystem.get_DesignVariables()
                
                if gradient_localobjective is not None:
                    perturbed_localobjective_left = subsystem.get_LocalObjectiveValue()
                
                if gradient_coordinationobjective is not None:
                    perturbed_coordinationobjective_left = subsystem.get_CoordinationObjectiveValue()
                    
                if jacobian_localequalityconstraints is not None:
                    perturbed_localequalityconstraints_left = subsystem.get_EqualityLocalConstraintsValue()
                    
                if jacobian_coordinationequalityconstraints is not None:
                    perturbed_coordinationequalityconstraints_left = subsystem.get_CoordinationEqualityConstraintValue()
                
                if jacobian_localinequalityconstraints is not None:
                    perturbed_localinequalityconstraints_left = subsystem.get_InequalityLocalConstraintsValue()

                if jacobian_coordinationinequalityconstraints is not None:
                    perturbed_coordinationinequalityconstraints_left = subsystem.get_CoordinationInequalityConstraintValue()
                
                for neighbor_index in range(len(neighborids)):
                
                    # Get the corresponding coupling parameter
                    couplingparameter: CouplingParametersInterface = couplingparameters[neighbor_index]

                    # Get the corresponding ID
                    neighborid: str = couplingparameter.get_ID()
                                        
                    # If the coupling is between local subsystems
                    if isinstance(couplingparameter, SubSysCouplingParametersBasis):
                        
                        # Get the mapped responses associated to this coupling
                        mappedresponse: List[float] | None = couplingparameter.get_MappedResponses()
                        
                        # Check if mapped responses exist
                        if mappedresponse is not None:
                            
                            # Initialize the corresponding Jacobian
                            perturbed_mappedresponses_left[neighborid] = copy.copy(mappedresponse)
                            
                # Reset the perturbed designvariables vector
                perturbed_designvariables_left[j] = original_designvariables[j]      
                
                # Update the stepsize
                stepsize += 1         
            
            if lowerbounds_scaled[j] is not None and original_designvariables[j] - epsilon_scaled[j] >= lowerbounds_scaled[j]:
                
                # The j-th component of the current designvariables is near the lower bound
                # Hence, Forward differentiation
                perturbed_designvariables_right[j] -= epsilon_scaled[j]
                
                # Update the subsystem based on the perturbation
                self.updateSubsystem(subsystem, perturbed_designvariables_right)
                
                # Get the needed quantities, if they exist
                
                perturbed_designvariables_right = subsystem.get_DesignVariables()
                
                if gradient_localobjective is not None:
                    perturbed_localobjective_right = subsystem.get_LocalObjectiveValue()
                
                if gradient_coordinationobjective is not None:
                    perturbed_coordinationobjective_right = subsystem.get_CoordinationObjectiveValue()
                    
                if jacobian_localequalityconstraints is not None:
                    perturbed_localequalityconstraints_right = subsystem.get_EqualityLocalConstraintsValue()
                    
                if jacobian_coordinationequalityconstraints is not None:
                    perturbed_coordinationequalityconstraints_right = subsystem.get_CoordinationEqualityConstraintValue()
                
                if jacobian_localinequalityconstraints is not None:
                    perturbed_localinequalityconstraints_right = subsystem.get_InequalityLocalConstraintsValue()

                if jacobian_coordinationinequalityconstraints is not None:
                    perturbed_coordinationinequalityconstraints_right = subsystem.get_CoordinationInequalityConstraintValue()
                
                for neighbor_index in range(len(neighborids)):
                
                    # Get the corresponding coupling parameter
                    couplingparameter: CouplingParametersInterface = couplingparameters[neighbor_index]

                    # Get the corresponding ID
                    neighborid: str = couplingparameter.get_ID()
                                        
                    # If the coupling is between local subsystems
                    if isinstance(couplingparameter, SubSysCouplingParametersBasis):
                        
                        # Get the mapped responses associated to this coupling
                        mappedresponse: List[float] | None = couplingparameter.get_MappedResponses()
                        
                        # Check if mapped responses exist
                        if mappedresponse is not None:
                            
                            # Initialize the corresponding Jacobian
                            perturbed_mappedresponses_right[neighborid] = copy.copy(mappedresponse)
                            
                # Reset the perturbed designvariables vector
                perturbed_designvariables_right[j] = original_designvariables[j]
                
                # Update the stepsize
                stepsize += 1
                
            # Update the empty-initialized quantities, if they exist
            
            if gradient_localobjective is not None:
                gradient_localobjective[j] = self.differencequotient(perturbed_localobjective_left, 
                                                                     perturbed_localobjective_right, 
                                                                     stepsize * epsilon_scaled[j] )   
                
            if gradient_coordinationobjective is not None:
                gradient_coordinationobjective[j] = self.differencequotient(perturbed_coordinationobjective_left, 
                                                                            perturbed_coordinationobjective_right, 
                                                                            stepsize * epsilon_scaled[j])
                
            if jacobian_localequalityconstraints is not None:
                
                # Iterate over the rows of the i-th column
                for i in range(len(jacobian_localequalityconstraints)):
                    jacobian_localequalityconstraints[i][j] = self.differencequotient(perturbed_localequalityconstraints_left[i], 
                                                                                      perturbed_localequalityconstraints_right[i], 
                                                                                      stepsize * epsilon_scaled[j] )                                                      
                
            if jacobian_coordinationequalityconstraints is not None:
                
                # Iterate over the rows of the j-th column
                for i in range(len(jacobian_coordinationequalityconstraints)):
                    jacobian_coordinationequalityconstraints[i][j] = self.differencequotient(perturbed_coordinationequalityconstraints_left[i], 
                                                                                             perturbed_coordinationequalityconstraints_right[i], 
                                                                                             stepsize * epsilon_scaled[j] )     
                
            if jacobian_localinequalityconstraints is not None:
                
                # Iterate over the rows of the j-th column
                for i in range(len(jacobian_localinequalityconstraints)):
                    jacobian_localinequalityconstraints[i][j] = self.differencequotient(perturbed_localinequalityconstraints_left[i], 
                                                                                        perturbed_localinequalityconstraints_right[i], 
                                                                                        stepsize * epsilon_scaled[j] )
                
            if jacobian_coordinationinequalityconstraints is not None:
                
                # Iterate over the rows of the j-th column
                for i in range(len(jacobian_coordinationinequalityconstraints)):
                    jacobian_coordinationinequalityconstraints[i][j] = self.differencequotient(perturbed_coordinationinequalityconstraints_left[i], 
                                                                                               perturbed_coordinationinequalityconstraints_right[i], 
                                                                                               stepsize)
            
            for neighbor_index in range(len(neighborids)):
                
                # Get the corresponding coupling parameter
                couplingparameter: CouplingParametersInterface = couplingparameters[neighbor_index]

                # Get the corresponding ID
                neighborid: str = couplingparameter.get_ID()
                                        
                # If the coupling is between local subsystems
                if isinstance(couplingparameter, SubSysCouplingParametersBasis):
                        
                    # Get the mapped responses associated to this coupling
                    mappedresponse: List[float] | None = couplingparameter.get_MappedResponses()
                        
                    # Check if mapped responses exist
                    if mappedresponse is not None:
                            
                        # Initialize the corresponding j-th column Jacobian associated 
                        # to the coupling with ID "neighborid"
                        
                        # Iterate over the rows of the j-th column
                        for i in range(len(jacobians_mappedresponses[neighborid])):
                            jacobians_mappedresponses[neighborid][i][j] = self.differencequotient(perturbed_mappedresponses_left[neighborid][i], 
                                                                                                  perturbed_mappedresponses_right[neighborid][i], 
                                                                                                  stepsize) 
        
        # Store current values
        
        if gradient_localobjective is not None:
            self.set_Gradient_LocalObjective(gradient_localobjective)
        if gradient_coordinationobjective is not None:
            self.set_Gradient_CoordinationObjective(gradient_coordinationobjective)
        if jacobian_localequalityconstraints is not None:
            self.set_Jacobian_LocalEqualityConstraints(jacobian_localequalityconstraints)
        if jacobian_coordinationequalityconstraints is not None:
            self.set_Jacobian_CoordinationEqualityConstraints(jacobian_coordinationequalityconstraints)
        if jacobian_localinequalityconstraints is not None:
            self.set_Jacobian_LocalInEqualityConstraints(jacobian_localinequalityconstraints)
            
        if jacobian_coordinationinequalityconstraints is not None:
            self.set_Jacobian_CoordinationInEqualityConstraints(jacobian_coordinationinequalityconstraints)
        
        if jacobians_mappedresponses is not None:
            
            # Filter out key-value pairs where the value is None
            filtered_jacobians_mappedresponses: Dict[str, List[List[float | None]]] = {neighborid: jacobian_mappedresponses 
                                                                                      for neighborid, jacobian_mappedresponses in jacobians_mappedresponses.items() 
                                                                                      if jacobian_mappedresponses is not None}    
            
            self.set_Jacobians_MappedResponses(filtered_jacobians_mappedresponses)

    def differencequotient(self, function_left: float, function_right: float,  
                           stepsize: float):
        """
        Compute the difference quotient of two function values.

        If stepsize > 0:
            - Takes the difference quotient 'function_left - function_right / stepsize'
        If stepsize = 0:
            - Returns 0
        Otherwise:
            - Raises error, since stepsize must be >= 0.

        Args:
            function_left (float): _description_
            function_right (float): _description_
            stepsize (float): _description_
        """
        
        # If 'left - right' order
        if stepsize > 0:
            
            # Return difference quotient of regular order
            return (function_left - function_right) / stepsize
        
        elif stepsize == 0:
            
            # Derivative not well-defined -> Return zero
            return 0

        else: 
            
            # There is no negative stepsize
            raise ValueError(f"{DDO_Color}Stepsize in the finite difference 1d-derivative needs to be a non-negative float, instead you provided: {stepsize}{Reset}")
        

    def updateSubsystem(self, subsystem: SubSystemBasis, perturbed_designvariables: List[float]):
        """
        Updates the subsystem based on the inputted design variables.

        Args:
            subsystem (SubSystemBasis): _description_
            perturbed_designvariables (List[float]): _description_
        """
        
        subsystem.set_DesignVariables(perturbed_designvariables)
        
        if subsystem.get_CoordinationObjectiveValue() is None:
            
            # execute analysis
            subsystem.runAnalysis()
                    
            # execute mapping
            subsystem.mapToCouplingParameters()
            
            # compute the local objective function
            subsystem.evaluateLocalObjective()
     
            localobjective: float | None = subsystem.get_LocalObjectiveValue()

            # With no coordination objective, the total objective equals the
            # local objective (None if the local objective does not exist either).
            subsystem.set_TotalObjectiveValue(localobjective)
            
        else:
            subsystem.evaluateTotalObjective()

        subsystem.evaluateTotalConstraint()

    def update_state(self, other_finite_differences_jacobian: 'FiniteDifferencesJacobian') -> None:
        """Update the state of this FiniteDifferencesJacobian with values from another instance.

        This method is necessary for multiprocessing. When subsystems are executed in parallel
        using multiprocessing.Pool, they are serialized and deserialized, creating new objects
        in separate memory spaces. After parallel execution completes, this method updates
        the original object's attribute values while preserving their memory addresses.

        The update preserves memory addresses by modifying list contents in-place rather than
        reassigning references. This is essential for maintaining object identity across the
        multiprocessing boundary.

        Args:
            other_finite_differences_jacobian: The source FiniteDifferencesJacobian containing
                updated values from parallel execution.
        """
        self._gradient_localobjective: List[float | None] | None = update_state_listprimitive(self._gradient_localobjective, other_finite_differences_jacobian.get_Gradient_LocalObjective())

        self._gradient_coordinationobjective: List[float | None] | None = update_state_listprimitive(self._gradient_coordinationobjective, other_finite_differences_jacobian.get_Gradient_CoordinationObjective())

        other_jacobian_localequalityconstraints: List[List[float | None]] | None = other_finite_differences_jacobian.get_Jacobian_LocalEqualityConstraints()
        if other_jacobian_localequalityconstraints is None:
            self._jacobian_localequalityconstraints: List[List[float | None]] | None = None
        else:
            if self._jacobian_localequalityconstraints is None:
                self._jacobian_localequalityconstraints = other_jacobian_localequalityconstraints
            else:
                for i in range(len(other_jacobian_localequalityconstraints)):
                    self._jacobian_localequalityconstraints[i] = update_state_listprimitive(self._jacobian_localequalityconstraints[i], other_jacobian_localequalityconstraints[i])

        other_jacobian_coordinationequalityconstraints: List[List[float | None]] | None = other_finite_differences_jacobian.get_Jacobian_CoordinationEqualityConstraints()
        if other_jacobian_coordinationequalityconstraints is None:
            self._jacobian_coordinationequalityconstraints: List[List[float | None]] | None = None
        else:
            if self._jacobian_coordinationequalityconstraints is None:
                self._jacobian_coordinationequalityconstraints = other_jacobian_coordinationequalityconstraints
            else:
                for i in range(len(other_jacobian_coordinationequalityconstraints)):
                    self._jacobian_coordinationequalityconstraints[i] = update_state_listprimitive(self._jacobian_coordinationequalityconstraints[i], other_jacobian_coordinationequalityconstraints[i])

        other_jacobian_localinequalityconstraints: List[List[float | None]] | None = other_finite_differences_jacobian.get_Jacobian_LocalInEqualityConstraints()
        if other_jacobian_localinequalityconstraints is None:
            self._jacobian_localinequalityconstraints: List[List[float | None]] | None = None
        else:
            if self._jacobian_localinequalityconstraints is None:
                self._jacobian_localinequalityconstraints = other_jacobian_localinequalityconstraints
            else:
                for i in range(len(other_jacobian_localinequalityconstraints)):
                    self._jacobian_localinequalityconstraints[i] = update_state_listprimitive(self._jacobian_localinequalityconstraints[i], other_jacobian_localinequalityconstraints[i])

        other_jacobian_coordinationinequalityconstraints: List[List[float | None]] | None = other_finite_differences_jacobian.get_Jacobian_CoordinationInEqualityConstraints()
        if other_jacobian_coordinationinequalityconstraints is None:    
            self._jacobian_coordinationinequalityconstraints: List[List[float | None]] | None = None
        else:
            if self._jacobian_coordinationinequalityconstraints is None:
                self._jacobian_coordinationinequalityconstraints = other_jacobian_coordinationinequalityconstraints
            else:
                for i in range(len(other_jacobian_coordinationinequalityconstraints)):
                    self._jacobian_coordinationinequalityconstraints[i] = update_state_listprimitive(self._jacobian_coordinationinequalityconstraints[i], other_jacobian_coordinationinequalityconstraints[i])

        other_jacobians_mappedresponses: Dict[str, List[List[float | None]]] | None = other_finite_differences_jacobian.get_Jacobians_MappedResponses()
        if other_jacobians_mappedresponses is None:
            self._jacobians_mappedresponses: Dict[str, List[List[float | None]]] | None = None
        else:
            if self._jacobians_mappedresponses is None:
                self._jacobians_mappedresponses = other_jacobians_mappedresponses
            else:
                for key in other_jacobians_mappedresponses.keys():
                    for i in range(len(other_jacobians_mappedresponses[key])):
                        self._jacobians_mappedresponses[key][i] = update_state_listprimitive(self._jacobians_mappedresponses[key][i], other_jacobians_mappedresponses[key][i])

```
