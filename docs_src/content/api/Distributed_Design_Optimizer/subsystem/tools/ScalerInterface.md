---
title: ScalerInterface
---

← Back to [tools](index.md)

# ScalerInterface

**Source:** [Distributed_Design_Optimizer\subsystem\tools\ScalerInterface.py](ScalerInterface_source.md)

Abstract interface for all scaler implementations.

## Classes

### ScalerInterface

> **Inherits from:** `ABC`

> Abstract interface for all scaler implementations.

#### Methods

??? abstract "__init__(self, lower_scaler_bound_unscaled: float, upper_scaler_bound_unscaled: float) → None"
    Initialize the scaler with the unscaled data range.


    **Args:**
    > lower_scaler_bound_unscaled: The lower bound of the unscaled data range.  
    > upper_scaler_bound_unscaled: The upper bound of the unscaled data range.  

??? abstract "transform(self, value_unscaled: float) → float"
    Scale value_unscaled according to feature_range.


    **Args:**
    > value_unscaled: The value to transform.  


    **Returns:**
    > The scaled value.  

??? abstract "inverse_transform(self, value_scaled: float) → float"
    Undo the scaling of value_scaled according to feature_range.


    **Args:**
    > value_scaled: The scaled value to inverse transform.  


    **Returns:**
    > The original unscaled value.  

??? abstract "get_bound_violation_warnings(self) → List[str]"
    Get warning messages for observed values outside the fitted range.


    **Returns:**
    > List of warning message strings. Empty list if no violations.  

??? abstract "get_bound_utilization_report(self) → tuple[str, bool, bool]"
    Get a compact one-line bound utilization summary for this scaler.


    **Returns:**
    > A tuple of (summary_line, has_violation, has_conservative).  

