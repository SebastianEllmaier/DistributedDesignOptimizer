# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""
Native PySide6 interactive network graph visualization using QGraphicsView.

Replaces PyVis/HTML-based graph rendering with a built-in Qt widget that
supports zoom, pan, node tooltips, and color-coded nodes/edges.
"""

import math
from PySide6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsItem,
    QGraphicsLineItem, QGraphicsTextItem, QGraphicsPolygonItem,
    QMenu, QApplication, QWidget, QStyleOptionGraphicsItem,
)
from PySide6.QtCore import Qt, QPointF, QRectF, QPoint
from PySide6.QtGui import (
    QBrush, QPen, QColor, QFont, QPolygonF,
    QPainter, QWheelEvent, QAction,
)


# ======================================================================
# Graph item classes
# ======================================================================

class NodeItem(QGraphicsItem):
    """Interactive graph node that can render as ellipse, triangle, or square."""

    def __init__(self, node_id: str, x: float, y: float, radius: float = 12,
                 color: str = "#5B8FF9", tooltip: str = "", label: str = "",
                 shape: str = "dot") -> None:
        """Initialize a graph node item.

        Args:
            node_id: Unique identifier for this node.
            x: X position in the scene.
            y: Y position in the scene.
            radius: Node radius in pixels.
            color: Hex color string for the node fill.
            tooltip: Hover tooltip text.
            label: Text label displayed below the node.
            shape: Node shape ("dot", "triangle", or "square").
        """
        super().__init__()
        self.node_id = node_id
        self._radius = radius
        self._shape = shape
        self._color = QColor(color)
        self._pen = QPen(QColor("#ffffff"), 1.5)
        self._brush = QBrush(self._color)

        self.setPos(x, y)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        if tooltip:
            self.setToolTip(tooltip)

        # Label (always visible below the node)
        self._label: QGraphicsTextItem | None = None
        if label:
            from ..styles.Theme import get_chart_colors
            colors = get_chart_colors()
            self._label = QGraphicsTextItem(label, self)
            self._label.setDefaultTextColor(QColor(colors["text"]))
            self._label.setFont(QFont("Segoe UI", 8))
            br = self._label.boundingRect()
            label_y = self._bounding_bottom() + 2
            self._label.setPos(-br.width() / 2, label_y)

    def boundingRect(self) -> QRectF:
        """Return the bounding rectangle for the node shape.

        Returns:
            The bounding rectangle enclosing the node.
        """
        r = self._radius
        if self._shape == "triangle":
            h = r * 1.7
            w = r * 1.4
            return QRectF(-w / 2 - 1, -h / 2 - 1, w + 2, h + 2)
        else:
            return QRectF(-r - 1, -r - 1, 2 * r + 2, 2 * r + 2)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = None) -> None:
        """Paint the node shape onto the scene.

        Args:
            painter: The QPainter used for rendering.
            option: Style options for the graphics item.
            widget: The widget being painted on, if any.
        """
        painter.setPen(self._pen)
        painter.setBrush(self._brush)
        r = self._radius

        if self._shape == "triangle":
            h = r * 1.7
            w = r * 1.4
            triangle = QPolygonF([
                QPointF(0, -h / 2),
                QPointF(-w / 2, h / 2),
                QPointF(w / 2, h / 2),
            ])
            painter.drawPolygon(triangle)
        elif self._shape == "square":
            painter.drawRect(QRectF(-r, -r, 2 * r, 2 * r))
        else:  # "dot" / ellipse
            painter.drawEllipse(QRectF(-r, -r, 2 * r, 2 * r))

    def set_highlight(self, on: bool) -> None:
        """Toggle a gold highlight border on the node.

        Args:
            on: Whether to enable the highlight.
        """
        if on:
            self._pen = QPen(QColor("#FFD700"), 3)
        else:
            self._pen = QPen(QColor("#ffffff"), 1.5)
        self.update()

    def _bounding_bottom(self) -> float:
        """Y coordinate of the lowest rendered point."""
        if self._shape == "triangle":
            return self._radius * 1.7 / 2
        return self._radius


class EdgeItem(QGraphicsLineItem):
    """Graph edge rendered as a line with optional arrow and tooltip."""

    def __init__(self, x1: float, y1: float, x2: float, y2: float,
                 color: str = "#CCCCCC", width: float = 1.5,
                 tooltip: str = "") -> None:
        """Initialize a graph edge item.

        Args:
            x1: Source X coordinate.
            y1: Source Y coordinate.
            x2: Target X coordinate.
            y2: Target Y coordinate.
            color: Hex color string for the edge line.
            width: Line width in pixels.
            tooltip: Hover tooltip text.
        """
        super().__init__(x1, y1, x2, y2)
        self.setPen(QPen(QColor(color), width))
        if tooltip:
            self.setToolTip(tooltip)
        self._color = color
        self._arrow = None
        self._create_arrow(x1, y1, x2, y2, color, width)

    def _create_arrow(self, x1: float, y1: float, x2: float, y2: float, color: str, width: float) -> None:
        """Add arrowhead at the target end."""
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx * dx + dy * dy)
        if length < 1e-6:
            return

        # Normalize
        ux, uy = dx / length, dy / length
        # Arrow size
        arrow_len = min(12, length * 0.3)
        arrow_w = arrow_len * 0.4

        # Pull back from target node (leave room for node radius)
        pull_back = 14
        tip_x = x2 - ux * pull_back
        tip_y = y2 - uy * pull_back
        base_x = tip_x - ux * arrow_len
        base_y = tip_y - uy * arrow_len

        # Perpendicular
        px, py = -uy, ux

        arrow = QPolygonF([
            QPointF(tip_x, tip_y),
            QPointF(base_x + px * arrow_w, base_y + py * arrow_w),
            QPointF(base_x - px * arrow_w, base_y - py * arrow_w),
        ])
        self._arrow = QGraphicsPolygonItem(arrow, self)
        self._arrow.setBrush(QBrush(QColor(color)))
        self._arrow.setPen(QPen(Qt.PenStyle.NoPen))


# ======================================================================
# Main widget
# ======================================================================

class GraphWidget(QGraphicsView):
    """
    Interactive network graph widget using QGraphicsView/QGraphicsScene.

    Accepts a graph_data dict with the structure:
    {
        "nodes": [
            {"id": str, "x": float, "y": float, "color": str, "size": float,
             "shape": str, "label": str, "tooltip": str},
            ...
        ],
        "edges": [
            {"source_x": float, "source_y": float, "target_x": float, "target_y": float,
             "color": str, "width": float, "tooltip": str},
            ...
        ],
        "title": str (optional)
    }
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the graph widget.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)

        # Rendering quality
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # Interaction
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setInteractive(True)

        # Background — follows theme via palette
        self._update_background()

        # Context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

        # Zoom limits
        self._zoom_level = 0
        self._max_zoom = 15
        self._min_zoom = -15

    def set_graph(self, graph_data: dict) -> None:
        """Render a graph from structured data.

        Args:
            graph_data: Dict with "nodes", "edges", and optional "title" keys.
        """
        self._scene.clear()

        nodes = graph_data.get("nodes", [])
        edges = graph_data.get("edges", [])

        # Draw edges first (under nodes)
        for edge in edges:
            item = EdgeItem(
                edge["source_x"], edge["source_y"],
                edge["target_x"], edge["target_y"],
                color=edge.get("color", "#CCCCCC"),
                width=edge.get("width", 1.5),
                tooltip=edge.get("tooltip", ""),
            )
            item.setZValue(0)
            self._scene.addItem(item)

        # Draw nodes on top
        for node in nodes:
            item = NodeItem(
                node_id=node["id"],
                x=node["x"], y=node["y"],
                radius=node.get("size", 12),
                color=node.get("color", "#5B8FF9"),
                tooltip=node.get("tooltip", ""),
                label=node.get("label", ""),
                shape=node.get("shape", "dot"),
            )
            item.setZValue(1)
            self._scene.addItem(item)

        # Add title if provided
        title = graph_data.get("title", "")
        if title:
            title_item = QGraphicsTextItem(title)
            title_item.setDefaultTextColor(QColor("#dcdcdc"))
            title_item.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
            sr = self._scene.sceneRect()
            title_item.setPos(sr.left(), sr.top() - 40)
            self._scene.addItem(title_item)

        # Fit view to content
        self.fitInView(self._scene.sceneRect().adjusted(-50, -50, 50, 50),
                       Qt.AspectRatioMode.KeepAspectRatio)
        self._zoom_level = 0

    def clear(self) -> None:
        """Clear the scene."""
        self._scene.clear()

    def update_theme(self) -> None:
        """Refresh background and node label colors to match the current theme."""
        self._update_background()
        from ..styles.Theme import get_chart_colors
        colors = get_chart_colors()
        for item in self._scene.items():
            if isinstance(item, NodeItem) and item._label:
                item._label.setDefaultTextColor(QColor(colors["text"]))

    def _update_background(self) -> None:
        """Set background brush from current theme."""
        from ..styles.Theme import get_chart_colors
        colors = get_chart_colors()
        self.setBackgroundBrush(QBrush(QColor(colors["fig_face"])))

    # ------------------------------------------------------------------
    # Zoom via mouse wheel
    # ------------------------------------------------------------------

    def wheelEvent(self, event: QWheelEvent) -> None:
        """Handle mouse wheel zoom with clamped zoom levels.

        Args:
            event: The wheel event containing scroll delta.
        """
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            if self._zoom_level < self._max_zoom:
                self.scale(zoom_in_factor, zoom_in_factor)
                self._zoom_level += 1
        else:
            if self._zoom_level > self._min_zoom:
                self.scale(zoom_out_factor, zoom_out_factor)
                self._zoom_level -= 1

    # ------------------------------------------------------------------
    # Context menu
    # ------------------------------------------------------------------

    def _show_context_menu(self, pos: QPoint) -> None:
        menu = QMenu(self)

        fit_action = QAction("Fit to View", self)
        fit_action.triggered.connect(self.fit_to_view)
        menu.addAction(fit_action)

        reset_action = QAction("Reset Zoom", self)
        reset_action.triggered.connect(self._reset_zoom)
        menu.addAction(reset_action)

        menu.addSeparator()

        export_action = QAction("Export as PNG...", self)
        export_action.triggered.connect(self.export_png)
        menu.addAction(export_action)

        menu.exec(self.mapToGlobal(pos))

    def fit_to_view(self) -> None:
        """Fit the entire graph into the visible viewport."""
        self.fitInView(self._scene.sceneRect().adjusted(-50, -50, 50, 50),
                       Qt.AspectRatioMode.KeepAspectRatio)
        self._zoom_level = 0

    def _reset_zoom(self) -> None:
        self.resetTransform()
        self._zoom_level = 0

    def export_png(self) -> None:
        """Export the current graph scene to a PNG file via a save dialog."""
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        from PySide6.QtGui import QImage, QPainter as QPaint
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Graph", "", "PNG (*.png);;All Files (*)"
        )
        if path:
            try:
                rect = self._scene.sceneRect()
                from ..styles.Theme import get_chart_colors
                bg = get_chart_colors()["fig_face"]
                image = QImage(int(rect.width()) + 100, int(rect.height()) + 100,
                               QImage.Format.Format_ARGB32)
                image.fill(QColor(bg))
                painter = QPaint(image)
                painter.setRenderHint(QPaint.RenderHint.Antialiasing)
                self._scene.render(painter)
                painter.end()
                image.save(path)
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export: {e}")
