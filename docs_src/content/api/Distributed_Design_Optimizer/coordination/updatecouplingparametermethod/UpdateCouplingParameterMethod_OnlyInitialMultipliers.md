---
title: UpdateCouplingParameterMethod_OnlyInitialMultipliers
---

← Back to [updatecouplingparametermethod](index.md)

# UpdateCouplingParameterMethod_OnlyInitialMultipliers

**Source:** [Distributed_Design_Optimizer\coordination\updatecouplingparametermethod\UpdateCouplingParameterMethod_OnlyInitialMultipliers.py](UpdateCouplingParameterMethod_OnlyInitialMultipliers_source.md)

Initial-multiplier-only coupling parameter update method.

This module implements an update strategy that performs no multiplier or
weight updates and only provides the initial Lagrange multiplier value.
Used by subsystems (e.g. SBDP) that recover the coordination multipliers
themselves (e.g. from the KKT system) but still need a seed value for the
initial multipliers.

## Classes

### UpdateCouplingParameterMethod_OnlyInitialMultipliers

> **Inherits from:** [UpdateCouplingParameterMethodInterface](UpdateCouplingParameterMethodInterface.md#updatecouplingparametermethodinterface)

> Update method that only provides the initial Lagrange multiplier value.

> All update and weight operations are no-ops; only get_InitialMultiplier
> returns a meaningful value. Intended for coordination methods that manage
> the coordination multipliers externally but require a seed value.


> **Attributes:**
> > _initialmultiplier: Initial value for Lagrange multipliers.

#### Methods

??? abstract "__init__(self, initialmultiplier: float) → None"
    Initialize the initial-multiplier-only update method.


    **Args:**
    > initialmultiplier: Initial value for Lagrange multipliers.  

??? abstract "validate_inputs(self) → None"
    Validate the hyperparameters of this update method.


    **Raises:**
    > ValueError: If any parameter is outside the allowed range.  

??? abstract "update_CoordinationMultipliers(self, multiplierin: List[float], inconsistencyin: List[float]) → None"
    No-op: does not update multipliers.


    **Args:**
    > multiplierin: Current multiplier values.  
    > inconsistencyin: Current inconsistency values.  

??? abstract "update_CoordinationWeights(self, weightin: List[float], inconsistencyIn: List[float], inconsistencyOldIn: List[float] | None) → None"
    No-op: does not update weights.


    **Args:**
    > weightin: Current penalty weights.  
    > inconsistencyIn: Current inconsistency values.  
    > inconsistencyOldIn: Previous inconsistency values, or None.  

??? abstract "get_InitialWeight(self) → float"
    No-op: this method does not provide an initial weight.


    **Returns:**
    > ``None``; this no-op method does not provide an initial weight.  

??? abstract "get_InitialMultiplier(self) → float"
    Get the initial Lagrange multiplier value.


    **Returns:**
    > The initial Lagrange multiplier value.  

??? abstract "print_startup_summary(self) → None"
    Print the initial multiplier value at startup.

??? abstract "print_termination_summary(self) → None"
    Print the initial multiplier value at the end.

??? abstract "update_state(self, other: [UpdateCouplingParameterMethod_OnlyInitialMultipliers](UpdateCouplingParameterMethod_OnlyInitialMultipliers.md#updatecouplingparametermethod_onlyinitialmultipliers)) → None"
    Update the state of this instance with values from another instance.


    **Args:**
    > other: The source instance containing updated values from parallel execution.  

