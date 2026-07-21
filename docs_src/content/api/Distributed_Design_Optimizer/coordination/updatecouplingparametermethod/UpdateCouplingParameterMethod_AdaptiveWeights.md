---
title: UpdateCouplingParameterMethod_AdaptiveWeights
---

← Back to [updatecouplingparametermethod](index.md)

# UpdateCouplingParameterMethod_AdaptiveWeights

**Source:** [Distributed_Design_Optimizer\coordination\updatecouplingparametermethod\UpdateCouplingParameterMethod_AdaptiveWeights.py](UpdateCouplingParameterMethod_AdaptiveWeights_source.md)

Standard PC coupling parameter update method.

This module implements the standard Penalty Coordination
update strategy for penalty weights (without Lagrange multipliers).

## Classes

### UpdateCouplingParameterMethod_AdaptiveWeights

> **Inherits from:** [UpdateCouplingParameterMethodInterface](UpdateCouplingParameterMethodInterface.md#updatecouplingparametermethodinterface)

> Standard PC update method for coupling parameters.

> Implements the penalty coordination update rules (without multipliers):
> - Weights: w_new = β * w_old if |c_new| > γ * |c_old|, else w_old


> **Attributes:**
> > _beta: Penalty weight update factor for increasing weights (must be > 1).  
> > _gamma: Inconsistency reduction threshold factor (must be in (0, 1)).  
> > _initialweight: Initial value for penalty weights (must be >= 0).

#### Methods

??? abstract "__init__(self, beta: float, gamma: float, initialweight: float) → None"
    Initialize the standard PC update method.


    **Args:**
    > beta: Penalty weight update factor for increasing weights.  
    > gamma: Inconsistency reduction threshold factor.  
    > initialweight: Initial value for penalty weights.  

??? abstract "validate_inputs(self) → None"
    Validate the hyperparameters of this update method.


    **Raises:**
    > ValueError: If any parameter is outside the allowed range.  

??? abstract "update_CoordinationWeights(self, weightin: List[float], inconsistencyIn: List[float], inconsistencyOldIn: List[float] | None) → None"
    Update penalty weights based on inconsistency progress.

    If the inconsistency has not decreased sufficiently (by factor gamma),
    the weight is increased by factor beta.


    **Args:**
    > weightin: Current weight values to update in place.  
    > inconsistencyIn: Current inconsistency values.  
    > inconsistencyOldIn: Previous iteration inconsistency values, or None.  

??? abstract "get_InitialWeight(self) → float"
    Get the initial penalty weight value.


    **Returns:**
    > The initial penalty weight value.  

??? abstract "print_startup_summary(self) → None"
    Print the adaptive weight parameters beta and gamma at startup.

??? abstract "print_termination_summary(self) → None"
    Print the adaptive weight parameters beta and gamma at the end.

??? abstract "update_state(self, other: [UpdateCouplingParameterMethod_AdaptiveWeights](UpdateCouplingParameterMethod_AdaptiveWeights.md#updatecouplingparametermethod_adaptiveweights)) → None"
    Update the state of this instance with values from another instance.


    **Args:**
    > other: The source instance containing updated values from parallel execution.  

