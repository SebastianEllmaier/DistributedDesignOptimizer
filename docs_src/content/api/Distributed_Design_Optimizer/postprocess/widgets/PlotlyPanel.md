---
title: PlotlyPanel
---

← Back to [widgets](index.md)

# PlotlyPanel

**Source:** [Distributed_Design_Optimizer\postprocess\widgets\PlotlyPanel.py](PlotlyPanel_source.md)

Reusable widget for embedding interactive Plotly charts via QWebEngineView.

Provides the common set_html / clear / export pattern used by both
PlotCanvas and TopologyPanel's chart page.

## Classes

### _ImageSaveBridge

> **Inherits from:** `QObject`

> QWebChannel bridge for saving Plotly chart images via native file dialog.

#### Methods

??? abstract "saveImage(self, fmt: str, ext: str, data_url: str) → None"
    Handle an image-save request forwarded from JavaScript.


    **Args:**
    > fmt: Image format identifier (e.g. ``'png'``, ``'svg'``).  
    > ext: File extension including dot (e.g. ``'.png'``).  
    > data_url: Base64-encoded data URL of the image.  

### PlotlyPanel

> **Inherits from:** `QWidget`

> Embeds a Plotly chart rendered as HTML inside a QWebEngineView.

#### Methods

??? abstract "__init__(self, placeholder_text: str, parent: QWidget | None) → None"
    Initialize the Plotly panel.


    **Args:**
    > placeholder_text: Text shown when no chart is loaded.  
    > parent: Optional parent widget.  

??? abstract "html(self) → str | None"
    Return the current HTML string, or ``None`` if empty.


    **Returns:**
    > The current HTML content, or None if no content is set.  

??? abstract "figure(self)"
    Return the cached Plotly figure (if any) for export.

??? abstract "set_html(self, html: str, fig) → None"
    Display Plotly HTML content, replacing any existing view.


    **Args:**
    > html: Raw HTML string containing a Plotly chart.  
    > fig: Optional Plotly figure cached for later image export.  

??? abstract "set_figure(self, fig) → None"
    Accept a Plotly go.Figure, convert to HTML, and display.


    **Args:**
    > fig: A Plotly ``go.Figure`` to render.  

??? abstract "refresh(self) → None"
    Re-render the current HTML.

??? abstract "clear(self) → None"
    Remove the chart and show placeholder.

??? abstract "export_image(self, path: str, dpi: int, width: int, height: int) → None"
    Save the current figure to a static image file (PNG/SVG/PDF via kaleido).


    **Args:**
    > path: Destination file path.  
    > dpi: Resolution in dots per inch.  
    > width: Image width in pixels.  
    > height: Image height in pixels.  

??? abstract "copy_to_clipboard(self) → None"
    Copy the current web view content to the system clipboard as an image.

??? abstract "init_web_view(self) → None"
    Eagerly create the QWebEngineView (call during startup to avoid flash).

