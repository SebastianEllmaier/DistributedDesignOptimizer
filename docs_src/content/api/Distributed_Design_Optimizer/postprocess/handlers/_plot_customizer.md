---
title: _plot_customizer
---

← Back to [handlers](index.md)

# _plot_customizer

**Source:** [Distributed_Design_Optimizer\postprocess\handlers\_plot_customizer.py](_plot_customizer_source.md)

Plot customization helpers for PlotHandler — Plotly implementation.

## Functions

??? abstract "apply_font(fig: go.Figure, config: [PlotConfig](../models/PlotConfig.md#plotconfig)) → None"
    Apply per-element font settings to all text elements.


    **Args:**
    > fig: Plotly Figure to update in place.  
    > config: Plot configuration with font settings.  

??? abstract "apply_labels(fig: go.Figure, config: [PlotConfig](../models/PlotConfig.md#plotconfig)) → None"
    Apply custom axis labels and title.


    **Args:**
    > fig: Plotly Figure to update in place.  
    > config: Plot configuration with custom label text.  

??? abstract "apply_reference_lines(fig: go.Figure, config: [PlotConfig](../models/PlotConfig.md#plotconfig)) → None"
    Add / replace horizontal reference lines as traces (shown in legend).


    **Args:**
    > fig: Plotly Figure to update in place.  
    > config: Plot configuration with reference line definitions.  

??? abstract "apply_per_line_styles(fig: go.Figure, config: [PlotConfig](../models/PlotConfig.md#plotconfig)) → None"
    Update trace colors, dash styles, and widths from per-line config.


    **Args:**
    > fig: Plotly Figure to update in place.  
    > config: Plot configuration with per-line style overrides.  

??? abstract "apply_legend(fig: go.Figure, config: [PlotConfig](../models/PlotConfig.md#plotconfig)) → None"
    Show / hide legend and apply themed positioning.


    **Args:**
    > fig: Plotly Figure to update in place.  
    > config: Plot configuration with legend visibility and position.  

??? abstract "apply_all(fig: go.Figure, config: [PlotConfig](../models/PlotConfig.md#plotconfig)) → None"
    Apply all customizations to a Plotly figure in order.


    **Args:**
    > fig: Plotly Figure to update in place.  
    > config: Plot configuration with all customization settings.  

