---
title: TopologyPanel
---

← Back to [widgets](index.md)

# TopologyPanel

**Source:** [Distributed_Design_Optimizer\postprocess\widgets\TopologyPanel.py](TopologyPanel_source.md)

Topology visualization panel using native PySide6 rendering.

Uses QGraphicsView for interactive network graphs, PlotlyPanel for
static charts, and QWebEngineView for interactive HTML visualizations
(Plotly, PyVis) displayed inline without external browser.

P2: Topology controls are embedded directly into this panel.

## Classes

### TopologyPanel

> **Inherits from:** `QWidget`

> Central tab for displaying topology analysis visualizations.

#### Methods

??? abstract "__init__(self, parent: QWidget | None) → None"
    Initialize the topology panel with placeholder, graph, chart, and web views.


    **Args:**
    > parent: Optional parent widget.  

??? abstract "display_graph(self, graph_data: dict) → None"
    Display an interactive network graph from structured data.


    **Args:**
    > graph_data: Dictionary containing node and edge data for the graph.  

??? abstract "display_chart(self, fig_or_html) → None"
    Display a Plotly figure or HTML string.


    **Args:**
    > fig_or_html: A Plotly figure object or an HTML string to render.  

??? abstract "display_html(self, html_content: str) → None"
    Display interactive HTML content (Plotly/PyVis) in embedded web view.


    **Args:**
    > html_content: Raw HTML string to render in the embedded browser.  

??? abstract "clear(self) → None"
    Reset to placeholder state.

??? abstract "update_theme(self) → None"
    Refresh theme-dependent colors on the graph widget.

