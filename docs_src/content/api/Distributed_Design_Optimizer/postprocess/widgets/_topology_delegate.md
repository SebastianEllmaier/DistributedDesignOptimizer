---
title: _topology_delegate
---

← Back to [widgets](index.md)

# _topology_delegate

**Source:** [Distributed_Design_Optimizer\postprocess\widgets\_topology_delegate.py](_topology_delegate_source.md)

Delegate handling topology result dispatch for MainWindow.

## Classes

### TopologyDelegate

> **Inherits from:** `QObject`

> Handles topology launch, result dispatch, and error display.

#### Methods

??? abstract "__init__(self, data_handler: [DataHandler](../handlers/DataHandler.md#datahandler), topology_handler: [TopologyHandler](../handlers/TopologyHandler.md#topologyhandler), chat_handler: [ChatHandler](../handlers/ChatHandler.md#chathandler), topology_panel: [TopologyPanel](TopologyPanel.md#topologypanel), chat_panel: [ChatPanel](ChatPanel.md#chatpanel), central_stack: QStackedWidget, status_bar: QStatusBar, parent: QObject | None) → None"
    Initialize the topology delegate.


    **Args:**
    > data_handler: Handler for accessing loaded data entries.  
    > topology_handler: Handler that runs topology analyses.  
    > chat_handler: Handler for setting AI chat context.  
    > topology_panel: Panel displaying topology visualizations.  
    > chat_panel: Panel displaying the AI chat interface.  
    > central_stack: Stacked widget controlling the main view.  
    > status_bar: Status bar for displaying messages.  
    > parent: Optional parent QObject.  

??? abstract "on_launch(self, config: [AnalysisConfig](../models/AnalysisConfig.md#analysisconfig)) → None"
    Launch topology analysis.


    **Args:**
    > config: Configuration specifying the analysis type and mode.  

??? abstract "on_graph_ready(self, graph_data: dict, analysis_type: str, context_data: dict) → None"
    Handle completed graph analysis by displaying results.


    **Args:**
    > graph_data: Dictionary containing the graph structure data.  
    > analysis_type: The type of topology analysis performed.  
    > context_data: Additional context metadata for the analysis.  

??? abstract "on_chart_ready(self, fig_or_html, analysis_type: str, context_data: dict) → None"
    Handle completed chart analysis by displaying results.


    **Args:**
    > fig_or_html: A Plotly figure or HTML string to display.  
    > analysis_type: The type of topology analysis performed.  
    > context_data: Additional context metadata for the analysis.  

??? abstract "on_html_ready(self, html_content: str, analysis_type: str, context_data: dict) → None"
    Handle completed HTML analysis by displaying results.


    **Args:**
    > html_content: The HTML string to render in the panel.  
    > analysis_type: The type of topology analysis performed.  
    > context_data: Additional context metadata for the analysis.  

??? abstract "on_error(self, message: str) → None"
    Display a critical error dialog for a failed topology analysis.


    **Args:**
    > message: The error message to display.  

