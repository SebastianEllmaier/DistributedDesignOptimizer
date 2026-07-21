---
title: PlotCanvas
---

← Back to [widgets](index.md)

# PlotCanvas

**Source:** [Distributed_Design_Optimizer\postprocess\widgets\PlotCanvas.py](PlotCanvas_source.md)

Central plot canvas widget with welcome card and Plotly figure display.

## Classes

### PlotCanvas

> **Inherits from:** `QWidget`

> Central plot area with welcome card and interactive Plotly figure display.

#### Methods

??? abstract "__init__(self, parent: QWidget | None) → None"
    Initialize the plot canvas with a welcome card and Plotly panel.


    **Args:**
    > parent: Optional parent widget.  

??? abstract "resizeEvent(self, event: QResizeEvent) → None"
    Adjust welcome card margins responsively on resize.


    **Args:**
    > event: The resize event.  

??? abstract "set_html(self, html: str, fig) → None"
    Display Plotly HTML content.


    **Args:**
    > html: Raw HTML string containing Plotly chart markup.  
    > fig: Optional Plotly figure object cached for image export.  

??? abstract "set_figure(self, fig) → None"
    Accept a Plotly go.Figure, convert and display.


    **Args:**
    > fig: A Plotly ``go.Figure`` to render.  

??? abstract "refresh(self) → None"
    Re-render the current Plotly HTML content.

??? abstract "clear(self) → None"
    Clear the current plot and show the welcome card.

??? abstract "get_figure(self)"
    Return the cached Plotly figure, or ``None`` if not set.

??? abstract "has_content(self) → bool"
    Return ``True`` if the panel currently holds HTML content.


    **Returns:**
    > Whether the panel currently has HTML content loaded.  

??? abstract "export_image(self, path: str, dpi: int) → None"
    Export the current plot to a static image file.


    **Args:**
    > path: Destination file path.  
    > dpi: Resolution in dots per inch.  

