---
title: ScalerBasis
---

← Back to [tools](index.md)

# ScalerBasis

**Source:** [Distributed_Design_Optimizer\subsystem\tools\ScalerBasis.py](ScalerBasis_source.md)

Base scaler implementation for normalizing values to a scaled range.

## Classes

### ScalerBasis

> **Inherits from:** [ScalerInterface](ScalerInterface.md#scalerinterface)

> Base implementation for scalers that normalize values to a scaled range.

> Provides common initialization, transform, inverse_transform, and
> bound-violation warning logic. Subclasses set the scaled bounds and
> display name, and may add extra validation.

#### Methods

??? abstract "__init__(self, lower_scaler_bound_unscaled: float, upper_scaler_bound_unscaled: float, lower_scaler_bound_scaled: float, upper_scaler_bound_scaled: float) → None"
    Initialize the scaler.


    **Args:**
    > lower_scaler_bound_unscaled: The lower bound of the unscaled data range.  
    > upper_scaler_bound_unscaled: The upper bound of the unscaled data range.  
    > lower_scaler_bound_scaled: The lower bound of the scaled feature range.  
    > upper_scaler_bound_scaled: The upper bound of the scaled feature range.  


    **Raises:**
    > ValueError: If lower_scaler_bound_unscaled is not strictly less than upper_scaler_bound_unscaled.  

??? abstract "transform(self, value_unscaled: float) → float"
    Scale value_unscaled according to feature_range.


    **Args:**
    > value_unscaled: The value to transform.  


    **Returns:**
    > The scaled value.  

    Warns:
    UserWarning: If the input value is outside the fitted range (once per bound).

??? abstract "inverse_transform(self, value_scaled: float) → float"
    Undo the scaling of value_scaled according to feature_range.


    **Args:**
    > value_scaled: The scaled value to inverse transform.  


    **Returns:**
    > The original unscaled value.  

    Warns:
    UserWarning: If the input value is outside the feature_range (once per bound).

??? abstract "get_scale(self) → float"
    Return the constant affine scale factor d(scaled)/d(unscaled) of this scaler.

    Since the transform is affine (scaled = unscaled * scale + offset), this
    factor is a constant equal to ``self._scale``. Use it to map a derivative
    taken w.r.t. an unscaled quantity into scaled space, e.g. to convert
    d(response_unscaled) into d(response_scaled). The inverse mapping (into
    scaled design-variable space) is obtained at the call-site as ``1.0 / get_scale()``.


    **Returns:**
    > The derivative d(scaled)/d(unscaled).  

??? abstract "get_bound_violation_warnings(self) → List[str]"
    Get warning messages for observed values outside the fitted range.


    **Returns:**
    > List of warning message strings. Empty list if no violations.  

??? abstract "get_bound_utilization_report(self) → tuple[str, bool, bool]"
    Get a compact one-line bound utilization summary for this scaler.


    **Returns:**
    > A tuple of (summary_line, has_violation, has_conservative).  
    > summary_line is a compact string. has_violation / has_conservative  
    > indicate whether advisory footnotes should be printed.  
    > Returns ('No values observed.', False, False) if nothing was seen.  

