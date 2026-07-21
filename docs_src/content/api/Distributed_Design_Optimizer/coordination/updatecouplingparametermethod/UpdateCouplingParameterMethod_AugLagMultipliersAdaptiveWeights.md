---
title: UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights
---

← Back to [updatecouplingparametermethod](index.md)

# UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights

**Source:** [Distributed_Design_Optimizer\coordination\updatecouplingparametermethod\UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights.py](UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights_source.md)

Standard ALC coupling parameter update method.

This module implements the standard Augmented Lagrangian Coordination
update strategy for Lagrange multipliers and penalty weights.

## Classes

### UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights

> **Inherits from:** [UpdateCouplingParameterMethodInterface](UpdateCouplingParameterMethodInterface.md#updatecouplingparametermethodinterface)

> Standard ALC update method for coupling parameters.

> Implements the classic augmented Lagrangian update rules:
> - Multipliers: λ_new = λ_old + 2 * w² * c(x)
> - Weights: w_new = β * w_old if |c_new| > γ * |c_old|, else w_old


> **Attributes:**
> > _beta: Penalty weight update factor for increasing weights (must be > 1).  
> > _gamma: Inconsistency reduction threshold factor (must be in (0, 1)).  
> > _initialweight: Initial value for penalty weights (must be >= 0).  
> > _initialmultiplier: Initial value for Lagrange multipliers.

#### Methods

??? abstract "__init__(self, beta: float, gamma: float, initialweight: float, initialmultiplier: float) → None"
    Initialize the standard ALC update method.


    **Args:**
    > beta: Penalty weight update factor for increasing weights.  
    > gamma: Inconsistency reduction threshold factor.  
    > initialweight: Initial value for penalty weights.  
    > initialmultiplier: Initial value for Lagrange multipliers.  

??? abstract "validate_inputs(self) → None"
    Validate the hyperparameters of this update method.


    **Raises:**
    > ValueError: If any parameter is outside the allowed range.  

??? abstract "update_CoordinationMultipliers(self, multiplierin: List[float], weightsin: List[float], inconsistencyin: List[float]) → None"
    Update Lagrange multipliers using the standard ALC rule.

    Update formula: λ_new = λ_old + 2 * w² * c(x)


    **Args:**
    > multiplierin: Current multiplier values to update in place.  
    > weightsin: Current penalty weight values.  
    > inconsistencyin: Current inconsistency values.  

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

??? abstract "get_InitialMultiplier(self) → float"
    Get the initial Lagrange multiplier value.


    **Returns:**
    > The initial Lagrange multiplier value.  

??? abstract "print_startup_summary(self) → None"
    Print the augmented Lagrangian adaptive weight parameters beta and gamma at startup.

??? abstract "print_termination_summary(self) → None"
    Print the augmented Lagrangian adaptive weight parameters beta and gamma at the end.

??? abstract "update_state(self, other: [UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights](UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights.md#updatecouplingparametermethod_auglagmultipliersadaptiveweights)) → None"
    Update the state of this instance with values from another instance.


    **Args:**
    > other: The source instance containing updated values from parallel execution.  

