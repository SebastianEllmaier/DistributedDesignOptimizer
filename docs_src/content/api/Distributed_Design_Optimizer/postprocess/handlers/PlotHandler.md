---
title: PlotHandler
---

← Back to [handlers](index.md)

# PlotHandler

**Source:** [Distributed_Design_Optimizer\postprocess\handlers\PlotHandler.py](PlotHandler_source.md)

Plotting engine — orchestrates figure creation and customization.

Delegates actual plot building to _plot_builder and customization to _plot_customizer.
Stores last plot state so theme toggles and auto-updates can regenerate the current figure.
Emits interactive Plotly HTML via the plot_ready signal.

## Classes

### PlotHandler

> **Inherits from:** `QObject`

> Plotting engine — creates Plotly figures and emits HTML strings.

#### Methods

??? abstract "__init__(self, parent: QObject | None) → None"
    Initialize the plot handler with default empty state.


    **Args:**
    > parent: Optional parent QObject for Qt ownership.  

??? abstract "last_plottable_data(self) → list[tuple[str, list[float]]]"
    Return the most recently plotted data series.


    **Returns:**
    > List of (series_name, values) tuples from the last plot.  

??? abstract "last_labels_map(self) → dict[str, list[dict]]"
    Return the most recently used labels map.


    **Returns:**
    > Mapping of series names to their label metadata dicts.  

??? abstract "last_figure(self) → go.Figure | None"
    The most recent Plotly figure (for export).


    **Returns:**
    > The last created Plotly figure, or None if no plot has been created.  

??? abstract "clear(self) → None"
    Reset all stored plot state.

??? abstract "set_canvas_size(self, width: int, height: int) → None"
    Set the canvas size used for figure creation.


    **Args:**
    > width: Canvas width in pixels.  
    > height: Canvas height in pixels.  

??? abstract "create_plot(self, plottable_data: list[tuple[str, list[float]]], config: [PlotConfig](../models/PlotConfig.md#plotconfig), labels_map: dict[str, list[dict]] | None) → None"
    Create a plot and emit plot_ready with the resulting HTML.


    **Args:**
    > plottable_data: List of (series_name, values) tuples to plot.  
    > config: Plot configuration controlling type, style, and layout.  
    > labels_map: Optional mapping of series names to label metadata.  

??? abstract "clear_customization(self) → None"
    Clear stored customization so it won't be re-applied on next plot.

??? abstract "apply_customization(self, fig: go.Figure, config: [PlotConfig](../models/PlotConfig.md#plotconfig)) → None"
    Apply font, labels, reference lines, per-line styles to an existing Figure.


    **Args:**
    > fig: The Plotly figure to customize.  
    > config: Plot configuration with customization settings.  

