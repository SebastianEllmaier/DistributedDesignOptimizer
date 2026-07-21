---
title: PlotSettingsPanel
---

← Back to [widgets](index.md)

# PlotSettingsPanel

**Source:** [Distributed_Design_Optimizer\postprocess\widgets\PlotSettingsPanel.py](PlotSettingsPanel_source.md)

Plot settings panel with collapsible sections for configuring chart appearance.

## Classes

### _PlotSketchWidget

> **Inherits from:** `QWidget`

> Greyed-out exemplary x-y line plot as visual guide.

#### Methods

??? abstract "__init__(self, parent: QWidget | None) → None"
    Initialize the sketch widget.


    **Args:**
    > parent: Optional parent widget.  

??? abstract "paintEvent(self, event) → None"
    Draw the exemplary convergence plot sketch.


    **Args:**
    > event: The paint event triggered by Qt.  

### PlotSettingsPanel

> **Inherits from:** `QWidget`

> Single scrollable panel with collapsible sections for all plot settings.

> All changes auto-apply (P13) — no manual Apply button needed.
> Topology controls are NOT included here (P2 — they live in TopologyPanel).

#### Methods

??? abstract "__init__(self, parent: QWidget | None) → None"
    Initialize the settings panel and build the UI.


    **Args:**
    > parent: Optional parent widget.  

??? abstract "get_plot_config(self) → [PlotConfig](../models/PlotConfig.md#plotconfig)"
    Collect all widget state into a PlotConfig dataclass.


    **Returns:**
    > A PlotConfig instance reflecting the current UI selections.  

??? abstract "refresh_line_entries(self, plottable_data: list[tuple[str, list]]) → None"
    Rebuild custom legend name fields and per-line style controls.

    P12: Auto-expand Legend and Per-Line sections when data is populated.


    **Args:**
    > plottable_data: List of (item_path, values) tuples for each series.  

