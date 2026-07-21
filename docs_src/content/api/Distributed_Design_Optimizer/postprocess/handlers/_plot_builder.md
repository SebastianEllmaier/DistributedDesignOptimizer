---
title: _plot_builder
---

← Back to [handlers](index.md)

# _plot_builder

**Source:** [Distributed_Design_Optimizer\postprocess\handlers\_plot_builder.py](_plot_builder_source.md)

Plot type builders for PlotHandler — Plotly implementation.

Produces plotly.graph_objects.Figure objects for shared, independent, centered,
and stacked plot types.

## Functions

??? abstract "tick_width_for(tick_length: int | float) → float"
    Return the tick line width that preserves the fixed length:width ratio.


    **Args:**
    > tick_length: The tick marker length in px.  


    **Returns:**
    > The proportional tick line width in px so the length:width ratio stays  
    > constant regardless of the configured tick size.  

??? abstract "generate_colors(n: int) → list[str]"
    Generate n distinct colours using Plotly's qualitative palette.


    **Args:**
    > n: Number of distinct colours to generate.  


    **Returns:**
    > List of CSS colour strings from the Dark24 palette.  

??? abstract "get_line_style(item_path: str, config: [PlotConfig](../models/PlotConfig.md#plotconfig)) → tuple[str, float]"
    Get Plotly dash style and width from config.


    **Args:**
    > item_path: Data series identifier key.  
    > config: Plot configuration containing per-line style overrides.  


    **Returns:**
    > Tuple of (dash style string, line width).  

??? abstract "get_legend_label(item_path: str, config: [PlotConfig](../models/PlotConfig.md#plotconfig)) → str"
    Get display label for a data series.


    **Args:**
    > item_path: Data series identifier key.  
    > config: Plot configuration containing per-line label overrides.  


    **Returns:**
    > Human-readable legend label string.  

??? abstract "shared_axes_plot(plottable_data: list[tuple[str, list[float]]], config: [PlotConfig](../models/PlotConfig.md#plotconfig), canvas_size: tuple[int, int], labels_map: dict[str, list[dict]]) → go.Figure"
    Single shared Y-axis for all data series.


    **Args:**
    > plottable_data: List of (item_path, y_values) tuples to plot.  
    > config: Plot configuration controlling axes, styles, and layout.  
    > canvas_size: Width and height in pixels for the figure.  
    > labels_map: Mapping of item paths to per-point label metadata.  


    **Returns:**
    > Configured Plotly Figure with all series on a shared Y-axis.  

??? abstract "multi_axes_plot(plottable_data: list[tuple[str, list[float]]], config: [PlotConfig](../models/PlotConfig.md#plotconfig), canvas_size: tuple[int, int], labels_map: dict[str, list[dict]]) → go.Figure"
    Multiple independent or centered Y-axes (overlaid).


    **Args:**
    > plottable_data: List of (item_path, y_values) tuples to plot.  
    > config: Plot configuration controlling axes, styles, and layout.  
    > canvas_size: Width and height in pixels for the figure.  
    > labels_map: Mapping of item paths to per-point label metadata.  


    **Returns:**
    > Configured Plotly Figure with independent Y-axes per series.  

??? abstract "stacked_plot(plottable_data: list[tuple[str, list[float]]], config: [PlotConfig](../models/PlotConfig.md#plotconfig), canvas_size: tuple[int, int], labels_map: dict[str, list[dict]]) → go.Figure"
    Stacked subplots (one per data series).


    **Args:**
    > plottable_data: List of (item_path, y_values) tuples to plot.  
    > config: Plot configuration controlling axes, styles, and layout.  
    > canvas_size: Width and height in pixels for the figure.  
    > labels_map: Mapping of item paths to per-point label metadata.  


    **Returns:**
    > Configured Plotly Figure with vertically stacked subplots.  

