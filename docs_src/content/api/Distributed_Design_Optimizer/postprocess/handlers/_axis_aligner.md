---
title: _axis_aligner
---

← Back to [handlers](index.md)

# _axis_aligner

**Source:** [Distributed_Design_Optimizer\postprocess\handlers\_axis_aligner.py](_axis_aligner_source.md)

X-axis generation and multi-file alignment logic for PlotHandler.

All functions are pure data transformations — no plotting library dependencies.

## Classes

### AlignedAxisData

> Result of :func:`build_aligned_data` — all data needed to render aligned plots.

#### Attributes

> `x_positions`: list[float]  
> `aligned_y`: list[list[float]]  
> `major_positions`: list[int]  
> `major_labels`: list[str]  
> `minor_positions`: list[float]  
> `hover_labels`: list[str]  

## Functions

??? abstract "generate_x_values(values: list[float], config: [PlotConfig](../models/PlotConfig.md#plotconfig), series_labels: list[dict] | None) → list[float]"
    Generate X-axis values based on the configured x_axis_type.


    **Args:**
    > values: Y-values whose length determines the number of x-positions.  
    > config: Plot configuration containing the x_axis_type setting.  
    > series_labels: Optional per-iteration metadata dicts for cumulative modes.  


    **Returns:**
    > List of float x-coordinates, one per value.  

??? abstract "cumulative_from_labels(n: int, key: str, labels: list[dict]) → list[float]"
    Build cumulative x-values from iteration label metadata.


    **Args:**
    > n: Number of data points to produce.  
    > key: Metadata key to accumulate (e.g. runtime or evaluation count).  
    > labels: Per-iteration metadata dicts containing the accumulation key.  


    **Returns:**
    > List of cumulative float values with length *n*.  

??? abstract "get_x_label(config: [PlotConfig](../models/PlotConfig.md#plotconfig)) → str"
    Return appropriate X-axis label based on x_axis_type.


    **Args:**
    > config: Plot configuration containing x_axis_type and custom_x_label.  


    **Returns:**
    > Human-readable axis label string.  

??? abstract "build_aligned_data(plottable_data: list[tuple[str, list[float]]], config: [PlotConfig](../models/PlotConfig.md#plotconfig), labels_map: dict[str, list[dict]]) → [AlignedAxisData](_axis_aligner.md#alignedaxisdata)"
    Build a unified x-axis across all series using outerloop/innerloop alignment.


    **Args:**
    > plottable_data: List of (item_path, y_values) tuples for each series.  
    > config: Plot configuration controlling axis type and spacing.  
    > labels_map: Mapping from entry ID to per-iteration metadata dicts.  


    **Returns:**
    > An :class:`AlignedAxisData` containing unified x-positions,  
    > NaN-padded y-arrays, and major/minor tick information.  

??? abstract "get_series_labels(item_path: str, labels_map: dict[str, list[dict]]) → list[dict]"
    Get iteration labels for the entry that owns this series.


    **Args:**
    > item_path: Slash-delimited path whose first segment is the entry ID.  
    > labels_map: Mapping from entry ID to per-iteration metadata dicts.  


    **Returns:**
    > List of label dicts for the matching entry, or an empty list.  

