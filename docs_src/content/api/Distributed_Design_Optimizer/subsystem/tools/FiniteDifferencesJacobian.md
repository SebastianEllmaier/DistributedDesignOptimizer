---
title: FiniteDifferencesJacobian
---

← Back to [tools](index.md)

# FiniteDifferencesJacobian

**Source:** [Distributed_Design_Optimizer\subsystem\tools\FiniteDifferencesJacobian.py](FiniteDifferencesJacobian_source.md)

Finite differences Jacobian computation module.

This module provides utilities for computing Jacobians using
finite difference approximations.

## Classes

### FiniteDifferencesJacobian

> Compute finite differences Jacobian approximations.

#### Methods

??? abstract "__init__(self) → None"
    Instantiates placeholders for Jacobians / gradient of local constraints and local objective.

??? abstract "get_Gradient_LocalObjective(self) → List[float | None] | None"
    Returns the gradient approximation of the local objective.


    **Returns:**
    > List[float]: _description_  

??? abstract "set_Gradient_LocalObjective(self, gradient_localobjective_in: List[float | None])"
    Sets the gradient approximation of the local objective.


    **Args:**
    > gradient_localobjective_in (List[float]): _description_  

??? abstract "get_Gradient_CoordinationObjective(self) → List[float | None] | None"
    Returns the gradient approximation of the local objective.


    **Returns:**
    > List[float | None] | None: _description_  

??? abstract "set_Gradient_CoordinationObjective(self, gradient_coordinationobjective_in: List[float | None])"
    Sets the gradient approximation of the coordination objective.


    **Args:**
    > gradient_coordinationobjective_in (List[float  |  None]): _description_  

??? abstract "get_Jacobian_LocalEqualityConstraints(self) → List[List[float | None]] | None"
    Returns the Jacobian approximation of the local equality constraints.


    **Returns:**
    > List[List[float]]: _description_  

??? abstract "set_Jacobian_LocalEqualityConstraints(self, jacobian_localequalityconstraints_in: List[List[float | None]]) → None"
    Sets the Jacobian approximation of the local equality constraints.


    **Args:**
    > jacobian_localequalityconstraints_in (List[List[float]]): _description_  

??? abstract "get_Jacobian_CoordinationEqualityConstraints(self) → List[List[float | None]] | None"
    Returns the Jacobian approximation of the coordination equality constraints.


    **Returns:**
    > List[List[float | None]] | None: _description_  

??? abstract "set_Jacobian_CoordinationEqualityConstraints(self, jacobian_coordinationequalityconstraints_in: List[List[float | None]]) → None"
    Sets the Jacobian approximation of the coordination equality constraints.


    **Args:**
    > jacobian_coordinationequalityconstraints_in (List[List[float | None]]): _description_  

??? abstract "get_Jacobian_LocalInEqualityConstraints(self) → List[List[float | None]] | None"
    Returns the Jacobian approximation of the local inequality constraints.


    **Returns:**
    > List[List[float]]: _description_  

??? abstract "set_Jacobian_LocalInEqualityConstraints(self, jacobian_localinequalityconstraints_in: List[List[float | None]]) → None"
    Sets the Jacobian approximation of the local inequality constraints.


    **Args:**
    > jacobian_localinequalityconstraints_in (List[List[float]]): _description_  

??? abstract "get_Jacobian_CoordinationInEqualityConstraints(self) → List[List[float | None]] | None"
    Returns the Jacobian approximation of the coordination inequality constraints.


    **Returns:**
    > List[List[float | None]] | None: _description_  

??? abstract "set_Jacobian_CoordinationInEqualityConstraints(self, jacobian_coordinationinequalityconstraints_in: List[List[float | None]]) → None"
    Sets the Jacobian approximation of the coordination inequality constraints.


    **Args:**
    > jacobian_coordinationinequalityconstraints_in (List[List[float  |  None]]): _description_  

??? abstract "get_Jacobians_MappedResponses(self) → Dict[str, List[List[float | None]]] | None"
    Get the Jacobian approximation of the mapped responses.


    **Returns:**
    > Dict[str, List[List[float | None]]]: _description_  

??? abstract "set_Jacobians_MappedResponses(self, jacobians_mappedresponses_in: Dict[str, List[List[float | None]]]) → None"
    Sets the Jacobian approximation of the mapped responses.


    **Args:**
    > jacobians_mappedresponses_in (Dict[str, List[List[float  |  None]]]): _description_  

??? abstract "run(self, subsystem: [SubSystemBasis](../SubSystemBasis.md#subsystembasis), perturbation_directions_indices_list: List[int]) → None"
    Computes the finite difference jacobian approximations and stores them.

    This is needed of all the following quantities:
    - Gradient of local objective
    - Jacobian of local equality constraints
    - Jacobian of local inequality constraints
    - Jacobian of mapped responses


    **Args:**
    > subsystem (SubSystemBasis): The subsystem to compute Jacobians for.  
    > perturbation_directions_indices_list (List[int]): Indices of design  
    > variable directions in which to compute finite differences.  

??? abstract "differencequotient(self, function_left: float, function_right: float, stepsize: float)"
    Compute the difference quotient of two function values.

    If stepsize > 0:
    - Takes the difference quotient 'function_left - function_right / stepsize'
    If stepsize = 0:
    - Returns 0
    Otherwise:
    - Raises error, since stepsize must be >= 0.


    **Args:**
    > function_left (float): _description_  
    > function_right (float): _description_  
    > stepsize (float): _description_  

??? abstract "updateSubsystem(self, subsystem: [SubSystemBasis](../SubSystemBasis.md#subsystembasis), perturbed_designvariables: List[float])"
    Updates the subsystem based on the inputted design variables.


    **Args:**
    > subsystem (SubSystemBasis): _description_  
    > perturbed_designvariables (List[float]): _description_  

??? abstract "update_state(self, other_finite_differences_jacobian: [FiniteDifferencesJacobian](FiniteDifferencesJacobian.md#finitedifferencesjacobian)) → None"
    Update the state of this FiniteDifferencesJacobian with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.

    The update preserves memory addresses by modifying list contents in-place rather than
    reassigning references. This is essential for maintaining object identity across the
    multiprocessing boundary.


    **Args:**
    > other_finite_differences_jacobian: The source FiniteDifferencesJacobian containing  
    > updated values from parallel execution.  

