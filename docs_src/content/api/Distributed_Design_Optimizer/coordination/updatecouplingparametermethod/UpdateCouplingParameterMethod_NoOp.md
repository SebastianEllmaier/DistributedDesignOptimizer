---
title: UpdateCouplingParameterMethod_NoOp
---

← Back to [updatecouplingparametermethod](index.md)

# UpdateCouplingParameterMethod_NoOp

**Source:** [Distributed_Design_Optimizer\coordination\updatecouplingparametermethod\UpdateCouplingParameterMethod_NoOp.py](UpdateCouplingParameterMethod_NoOp_source.md)

No-op coupling parameter update method.

This module implements a no-op update strategy that performs no updates.
Used by subsystems that manage coupling parameters externally or do not
require parameter updates (e.g., controller subsystems).

## Classes

### UpdateCouplingParameterMethod_NoOp

> **Inherits from:** [UpdateCouplingParameterMethodInterface](UpdateCouplingParameterMethodInterface.md#updatecouplingparametermethodinterface)

> No-op update method that performs no coupling parameter updates.

> Used as a placeholder for subsystems that do not update coupling
> parameters through the standard strategy interface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the no-op update method.

??? abstract "validate_inputs(self) → None"
    No-op: no parameters to validate.

??? abstract "update_CoordinationMultipliers(self, multiplierin: List[float], weightsin: List[float], inconsistencyin: List[float]) → None"
    No-op: does not update multipliers.


    **Args:**
    > multiplierin: Current multiplier values.  
    > weightsin: Current weight values.  
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
    No-op: this method does not provide an initial multiplier.


    **Returns:**
    > ``None``; this no-op method does not provide an initial multiplier.  

??? abstract "print_startup_summary(self) → None"
    Nothing to print.

??? abstract "print_termination_summary(self) → None"
    Nothing to print.

??? abstract "update_state(self, other: [UpdateCouplingParameterMethod_NoOp](UpdateCouplingParameterMethod_NoOp.md#updatecouplingparametermethod_noop)) → None"
    No-op: no state to update.


    **Args:**
    > other: The source instance (ignored).  

