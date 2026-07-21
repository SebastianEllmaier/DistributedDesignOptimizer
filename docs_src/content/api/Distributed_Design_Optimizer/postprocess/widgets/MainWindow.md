---
title: MainWindow
---

← Back to [widgets](index.md)

# MainWindow

**Source:** [Distributed_Design_Optimizer\postprocess\widgets\MainWindow.py](MainWindow_source.md)

Main application window for the DDO Viewer.

## Classes

### MainWindow

> **Inherits from:** `QMainWindow`

> Top-level application window.

> Layout:
> Left dock  — action bar + QTabWidget with Data / Settings / AI Chat tabs
> Central    — QTabWidget with Plot / Topology (with embedded controls)

#### Methods

??? abstract "__init__(self, llm_config: dict | None) → None"
    Initialize the main window and all child widgets.


    **Args:**
    > llm_config: Optional LLM configuration dict for the AI chat handler.  

??? abstract "closeEvent(self, event: QCloseEvent) → None"
    Persist window state and cancel background tasks before closing.


    **Args:**
    > event: The close event.  

