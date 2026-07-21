---
title: ScalerZeroOne
---

← Back to [tools](index.md)

# ScalerZeroOne

**Source:** [Distributed_Design_Optimizer\subsystem\tools\ScalerZeroOne.py](ScalerZeroOne_source.md)

Scaler for normalizing values to the range [0, 1].

## Classes

### ScalerZeroOne

> **Inherits from:** [ScalerBasis](ScalerBasis.md#scalerbasis)

> A scaler that normalizes values to the range [0, 1].

> Provides validation and scalar value support for optimization design variables.

#### Methods

??? abstract "__init__(self, lower_scaler_bound_unscaled: float, upper_scaler_bound_unscaled: float) → None"
    Initialize the ScalerZeroOne with feature range [0, 1].


    **Args:**
    > lower_scaler_bound_unscaled: The lower bound of the unscaled data range.  
    > upper_scaler_bound_unscaled: The upper bound of the unscaled data range.  


    **Raises:**
    > ValueError: If lower_scaler_bound_unscaled is not strictly less than upper_scaler_bound_unscaled.  

