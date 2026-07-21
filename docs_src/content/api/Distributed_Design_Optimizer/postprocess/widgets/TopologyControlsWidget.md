---
title: TopologyControlsWidget
---

← Back to [widgets](index.md)

# TopologyControlsWidget

**Source:** [Distributed_Design_Optimizer\postprocess\widgets\TopologyControlsWidget.py](TopologyControlsWidget_source.md)

Widget providing controls for selecting and launching topology analyses.

## Classes

### TopologyControlsWidget

> **Inherits from:** `QWidget`

> Controls for selecting and launching topology analysis.

#### Methods

??? abstract "__init__(self, parent: QWidget | None) → None"
    Initialize the topology controls widget.


    **Args:**
    > parent: Optional parent widget.  

??? abstract "get_config(self) → [AnalysisConfig](../models/AnalysisConfig.md#analysisconfig)"
    Build an AnalysisConfig from current widget state.


    **Returns:**
    > AnalysisConfig populated with the selected analysis type and mode.  

??? abstract "showEvent(self, event) → None"
    Re-apply accent color when the widget becomes visible.


    **Args:**
    > event: The show event.  

