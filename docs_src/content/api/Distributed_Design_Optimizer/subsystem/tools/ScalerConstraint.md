---
title: ScalerConstraint
---

← Back to [tools](index.md)

# ScalerConstraint

**Source:** [Distributed_Design_Optimizer\subsystem\tools\ScalerConstraint.py](ScalerConstraint_source.md)

Scaler for normalizing constraint values to [-0.5, 0.5].

## Classes

### ScalerConstraint

> **Inherits from:** [ScalerBasis](ScalerBasis.md#scalerbasis)

> A scaler that normalizes constraint values to the range [-0.5, 0.5].

> Provides validation and scalar value support for optimization constraints.
> Requires symmetric data range about 0.

#### Methods

??? abstract "__init__(self, lower_scaler_bound_unscaled: float, upper_scaler_bound_unscaled: float) → None"
    Initialize the ScalerConstraint with feature range [-0.5, 0.5].

    Ensures that the data range is symmetric about 0, meaning -1*min = max.


    **Args:**
    > lower_scaler_bound_unscaled: The lower bound of the unscaled data range.  
    > upper_scaler_bound_unscaled: The upper bound of the unscaled data range.  


    **Raises:**
    > ValueError: If the data range is not symmetric about 0 or is zero.  

