---
title: UpdateCouplingParameterMethod_SubgradientMultipliers
---

← Back to [updatecouplingparametermethod](index.md)

# UpdateCouplingParameterMethod_SubgradientMultipliers

**Source:** [Distributed_Design_Optimizer\coordination\updatecouplingparametermethod\UpdateCouplingParameterMethod_SubgradientMultipliers.py](UpdateCouplingParameterMethod_SubgradientMultipliers_source.md)

Standard LC coupling parameter update method.

This module implements the standard Lagrangian Coordination
update strategy for Lagrange multipliers (without penalty weights).

## Classes

### UpdateCouplingParameterMethod_SubgradientMultipliers

> **Inherits from:** [UpdateCouplingParameterMethodInterface](UpdateCouplingParameterMethodInterface.md#updatecouplingparametermethodinterface)

> Standard LC update method for coupling parameters.

> Implements the Lagrangian coordination update rules (without penalty weights):
> - Multipliers: λ_new = λ_old + beta * inconsistency

> Note: gamma is not used in LC since there are no penalty weights to update.


> **Attributes:**
> > _beta: Multiplier update step size (must be > 0).  
> > _initialmultiplier: Initial value for Lagrange multipliers.

#### Methods

??? abstract "__init__(self, beta: float, initialmultiplier: float) → None"
    Initialize the standard LC update method.


    **Args:**
    > beta: Multiplier update step size.  
    > initialmultiplier: Initial value for Lagrange multipliers.  

??? abstract "validate_inputs(self) → None"
    Validate the hyperparameters of this update method.


    **Raises:**
    > ValueError: If any parameter is outside the allowed range.  

??? abstract "update_CoordinationMultipliers(self, multiplierin: List[float], inconsistencyin: List[float]) → None"
    Update Lagrange multipliers using the standard LC subgradient rule.

    Update formula: λ_new = λ_old + beta * inconsistency

    **Args:**
    > multiplierin: Current multiplier values to update in place.  
    > inconsistencyin: Current inconsistency values.  

??? abstract "get_InitialMultiplier(self) → float"
    Get the initial Lagrange multiplier value.


    **Returns:**
    > The initial Lagrange multiplier value.  

??? abstract "print_startup_summary(self) → None"
    Print the subgradient multiplier parameters beta and initial multiplier at startup.

??? abstract "print_termination_summary(self) → None"
    Print the subgradient multiplier parameters beta and initial multiplier at the end.

??? abstract "update_state(self, other: [UpdateCouplingParameterMethod_SubgradientMultipliers](UpdateCouplingParameterMethod_SubgradientMultipliers.md#updatecouplingparametermethod_subgradientmultipliers)) → None"
    Update the state of this instance with values from another instance.


    **Args:**
    > other: The source instance containing updated values from parallel execution.  

