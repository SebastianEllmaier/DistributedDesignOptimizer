---
title: UpdateCouplingParameterMethod_AugLagMultipliersFixedWeights
---

← Back to [updatecouplingparametermethod](index.md)

# UpdateCouplingParameterMethod_AugLagMultipliersFixedWeights

**Source:** [Distributed_Design_Optimizer\coordination\updatecouplingparametermethod\UpdateCouplingParameterMethod_AugLagMultipliersFixedWeights.py](UpdateCouplingParameterMethod_AugLagMultipliersFixedWeights_source.md)

ALADIN coupling parameter update method.

This module implements the ALADIN update strategy for Lagrange multipliers.
ALADIN updates multipliers using the same augmented Lagrangian rule as ALC,
but does not update penalty weights.

## Classes

### UpdateCouplingParameterMethod_AugLagMultipliersFixedWeights

> **Inherits from:** [UpdateCouplingParameterMethodInterface](UpdateCouplingParameterMethodInterface.md#updatecouplingparametermethodinterface)

> ALADIN update method for coupling parameters.

> Implements the ALADIN multiplier update rule:
> - Multipliers: λ_new = λ_old + 2 * w² * c(x)
> - Weights: no update (ALADIN does not modify penalty weights)


> **Attributes:**
> > _initialweight: Initial value for penalty weights (must be >= 0).  
> > _initialmultiplier: Initial value for Lagrange multipliers.

#### Methods

??? abstract "__init__(self, initialweight: float, initialmultiplier: float) → None"
    Initialize the ALADIN update method.


    **Args:**
    > initialweight: Initial value for penalty weights.  
    > initialmultiplier: Initial value for Lagrange multipliers.  

??? abstract "validate_inputs(self) → None"
    Validate the hyperparameters of this update method.


    **Raises:**
    > ValueError: If any parameter is outside the allowed range.  

??? abstract "update_CoordinationMultipliers(self, multiplierin: List[float], weightsin: List[float], inconsistencyin: List[float]) → None"
    Update Lagrange multipliers using the augmented Lagrangian rule.

    Update formula: λ_new = λ_old + 2 * w² * c(x)


    **Args:**
    > multiplierin: Current multiplier values to update in place.  
    > weightsin: Current penalty weight values.  
    > inconsistencyin: Current inconsistency values.  

??? abstract "update_CoordinationWeights(self, weightin: List[float], inconsistencyIn: List[float], inconsistencyOldIn: List[float] | None) → None"
    No-op: ALADIN does not update penalty weights.


    **Args:**
    > weightin: Current penalty weights.  
    > inconsistencyIn: Current inconsistency values.  
    > inconsistencyOldIn: Previous inconsistency values, or None.  

??? abstract "get_InitialWeight(self) → float"
    Get the initial penalty weight value.


    **Returns:**
    > The initial penalty weight value.  

??? abstract "get_InitialMultiplier(self) → float"
    Get the initial Lagrange multiplier value.


    **Returns:**
    > The initial Lagrange multiplier value.  

??? abstract "print_startup_summary(self) → None"
    Print the fixed weight and initial multiplier values at startup.

??? abstract "print_termination_summary(self) → None"
    Print the fixed weight and initial multiplier values at the end.

??? abstract "update_state(self, other: [UpdateCouplingParameterMethod_AugLagMultipliersFixedWeights](UpdateCouplingParameterMethod_AugLagMultipliersFixedWeights.md#updatecouplingparametermethod_auglagmultipliersfixedweights)) → None"
    Update the state of this instance with values from another instance.


    **Args:**
    > other: The source instance containing updated values from parallel execution.  

