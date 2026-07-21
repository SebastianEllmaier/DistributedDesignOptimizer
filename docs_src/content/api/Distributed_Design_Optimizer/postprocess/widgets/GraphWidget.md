---
title: GraphWidget
---

← Back to [widgets](index.md)

# GraphWidget

**Source:** [Distributed_Design_Optimizer\postprocess\widgets\GraphWidget.py](GraphWidget_source.md)

Native PySide6 interactive network graph visualization using QGraphicsView.

Replaces PyVis/HTML-based graph rendering with a built-in Qt widget that
supports zoom, pan, node tooltips, and color-coded nodes/edges.

## Classes

### NodeItem

> **Inherits from:** `QGraphicsItem`

> Interactive graph node that can render as ellipse, triangle, or square.

#### Methods

??? abstract "__init__(self, node_id: str, x: float, y: float, radius: float, color: str, tooltip: str, label: str, shape: str) → None"
    Initialize a graph node item.


    **Args:**
    > node_id: Unique identifier for this node.  
    > x: X position in the scene.  
    > y: Y position in the scene.  
    > radius: Node radius in pixels.  
    > color: Hex color string for the node fill.  
    > tooltip: Hover tooltip text.  
    > label: Text label displayed below the node.  
    > shape: Node shape ("dot", "triangle", or "square").  

??? abstract "boundingRect(self) → QRectF"
    Return the bounding rectangle for the node shape.


    **Returns:**
    > The bounding rectangle enclosing the node.  

??? abstract "paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None) → None"
    Paint the node shape onto the scene.


    **Args:**
    > painter: The QPainter used for rendering.  
    > option: Style options for the graphics item.  
    > widget: The widget being painted on, if any.  

??? abstract "set_highlight(self, on: bool) → None"
    Toggle a gold highlight border on the node.


    **Args:**
    > on: Whether to enable the highlight.  

### EdgeItem

> **Inherits from:** `QGraphicsLineItem`

> Graph edge rendered as a line with optional arrow and tooltip.

#### Methods

??? abstract "__init__(self, x1: float, y1: float, x2: float, y2: float, color: str, width: float, tooltip: str) → None"
    Initialize a graph edge item.


    **Args:**
    > x1: Source X coordinate.  
    > y1: Source Y coordinate.  
    > x2: Target X coordinate.  
    > y2: Target Y coordinate.  
    > color: Hex color string for the edge line.  
    > width: Line width in pixels.  
    > tooltip: Hover tooltip text.  

### GraphWidget

> **Inherits from:** `QGraphicsView`

> Interactive network graph widget using QGraphicsView/QGraphicsScene.

> Accepts a graph_data dict with the structure:
> {
> 'nodes': [
> {'id': str, 'x': float, 'y': float, 'color': str, 'size': float,
> 'shape': str, 'label': str, 'tooltip': str},
> ...
> ],
> 'edges': [
> {'source_x': float, 'source_y': float, 'target_x': float, 'target_y': float,
> 'color': str, 'width': float, 'tooltip': str},
> ...
> ],
> 'title': str (optional)
> }

#### Methods

??? abstract "__init__(self, parent: QWidget | None) → None"
    Initialize the graph widget.


    **Args:**
    > parent: Optional parent widget.  

??? abstract "set_graph(self, graph_data: dict) → None"
    Render a graph from structured data.


    **Args:**
    > graph_data: Dict with "nodes", "edges", and optional "title" keys.  

??? abstract "clear(self) → None"
    Clear the scene.

??? abstract "update_theme(self) → None"
    Refresh background and node label colors to match the current theme.

??? abstract "wheelEvent(self, event: QWheelEvent) → None"
    Handle mouse wheel zoom with clamped zoom levels.


    **Args:**
    > event: The wheel event containing scroll delta.  

??? abstract "fit_to_view(self) → None"
    Fit the entire graph into the visible viewport.

??? abstract "export_png(self) → None"
    Export the current graph scene to a PNG file via a save dialog.

