# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""
Topology visualization panel using native PySide6 rendering.

Uses QGraphicsView for interactive network graphs, PlotlyPanel for
static charts, and QWebEngineView for interactive HTML visualizations
(Plotly, PyVis) displayed inline without external browser.

P2: Topology controls are embedded directly into this panel.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget, QMenu,
    QFileDialog, QFrame,
)
from PySide6.QtCore import Qt, QPoint, QUrl, Signal
from PySide6.QtGui import QAction, QColor

from ..models.AnalysisConfig import AnalysisConfig
from ..styles.Theme import get_accent_color
from .GraphWidget import GraphWidget
from .PlotlyPanel import PlotlyPanel

# Lazy import to handle environments without WebEngine gracefully
_QWebEngineView = None


def _get_web_engine_view():
    global _QWebEngineView
    if _QWebEngineView is None:
        from PySide6.QtWebEngineWidgets import QWebEngineView
        _QWebEngineView = QWebEngineView
    return _QWebEngineView


class TopologyPanel(QWidget):
    """Central tab for displaying topology analysis visualizations."""

    topology_launch_requested = Signal(AnalysisConfig)
    image_saved = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the topology panel with placeholder, graph, chart, and web views.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Visualization stack (no embedded controls — those live in the Settings panel)
        self._stack = QStackedWidget()

        # Page 0: Styled placeholder card (E2)
        self._placeholder = QWidget()
        ph_layout = QVBoxLayout(self._placeholder)
        ph_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._ph_divider = QFrame()
        self._ph_divider.setFrameShape(QFrame.Shape.HLine)
        self._ph_divider.setFixedWidth(140)
        self._ph_divider.setFixedHeight(2)

        self._ph_title = QLabel("Topology Analysis")
        self._ph_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._ph_title.setStyleSheet("font-size: 16pt; font-weight: bold;")
        ph_layout.addWidget(self._ph_title)
        ph_layout.addWidget(self._ph_divider, alignment=Qt.AlignmentFlag.AlignCenter)
        ph_layout.addSpacing(12)
        ph_desc = QLabel(
            "Explore the structure and coupling of your "
            "distributed optimization problem. "
            "Select an analysis type from the Settings panel "
            "on the left, then click \u2018Launch Visualization\u2019."
        )
        ph_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ph_desc.setWordWrap(True)
        ph_desc.setStyleSheet("color: gray; font-size: 10pt;")
        ph_layout.addWidget(ph_desc)
        self._apply_placeholder_accent()
        self._stack.addWidget(self._placeholder)

        # Page 1: Interactive graph (QGraphicsView)
        self._graph_widget = GraphWidget()
        self._stack.addWidget(self._graph_widget)

        # Page 2: Chart view (shared PlotlyPanel — interactive Plotly HTML)
        self._chart_panel = PlotlyPanel(parent=self)
        self._chart_panel.init_web_view()
        self._chart_panel.image_saved.connect(self.image_saved)
        self._stack.addWidget(self._chart_panel)

        # Page 3: Interactive HTML view (QWebEngineView) — created lazily
        self._web_view = None

        layout.addWidget(self._stack)

        # Context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def display_graph(self, graph_data: dict) -> None:
        """Display an interactive network graph from structured data.

        Args:
            graph_data: Dictionary containing node and edge data for the graph.
        """
        self._graph_widget.set_graph(graph_data)
        self._stack.setCurrentIndex(1)

    def display_chart(self, fig_or_html) -> None:
        """Display a Plotly figure or HTML string.

        Args:
            fig_or_html: A Plotly figure object or an HTML string to render.
        """
        self._stack.setCurrentIndex(2)
        from PySide6.QtCore import QTimer
        if isinstance(fig_or_html, str):
            QTimer.singleShot(50, lambda: self._chart_panel.set_html(fig_or_html))
        else:
            QTimer.singleShot(50, lambda: self._chart_panel.set_figure(fig_or_html))

    def display_html(self, html_content: str) -> None:
        """Display interactive HTML content (Plotly/PyVis) in embedded web view.

        Args:
            html_content: Raw HTML string to render in the embedded browser.
        """
        self._ensure_web_view()
        self._stack.setCurrentIndex(3)
        from PySide6.QtCore import QTimer
        # Inject white background to prevent black flash
        styled = html_content.replace(
            "<head>",
            "<head><style>body{background:#fff !important;}</style>",
            1,
        )
        QTimer.singleShot(50, lambda: self._web_view.setHtml(styled, QUrl("about:blank")))

    def clear(self) -> None:
        """Reset to placeholder state."""
        self._graph_widget.clear()
        self._chart_panel.clear()
        if self._web_view is not None:
            self._web_view.setHtml("")
        self._stack.setCurrentIndex(0)

    def update_theme(self) -> None:
        """Refresh theme-dependent colors on the graph widget."""
        self._graph_widget.update_theme()
        self._apply_placeholder_accent()

    def _apply_placeholder_accent(self) -> None:
        accent = get_accent_color()
        self._ph_title.setStyleSheet(f"color: {accent}; font-size: 16pt; font-weight: bold;")
        self._ph_divider.setStyleSheet(f"background-color: {accent};")

    def _ensure_web_view(self) -> None:
        """Lazily create the QWebEngineView on first use."""
        if self._web_view is None:
            WebView = _get_web_engine_view()
            self._web_view = WebView(self)
            self._web_view.page().setBackgroundColor(Qt.GlobalColor.white)
            self._web_view.setStyleSheet("background: white;")
            self._web_view.setHtml(
                "<html><body style='background:#fff;'></body></html>",
                QUrl("about:blank"),
            )
            self._stack.addWidget(self._web_view)

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _show_context_menu(self, pos: QPoint) -> None:
        menu = QMenu(self)
        current = self._stack.currentIndex()
        if current == 1:
            export_action = QAction("Export Graph as PNG...", self)
            export_action.triggered.connect(self._graph_widget.export_png)
            menu.addAction(export_action)
            fit_action = QAction("Fit to View", self)
            fit_action.triggered.connect(self._graph_widget.fit_to_view)
            menu.addAction(fit_action)
        elif current == 2 and self._chart_panel.html:
            export_action = QAction("Save Chart...", self)
            export_action.triggered.connect(self._export_chart)
            menu.addAction(export_action)
        if menu.actions():
            menu.exec(self.mapToGlobal(pos))

    def _export_chart(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Chart", "",
            "PNG (*.png);;SVG (*.svg);;PDF (*.pdf);;All Files (*)"
        )
        if path:
            try:
                self._chart_panel.export_image(path)
            except Exception as e:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.critical(self, "Export Error", f"Failed to save chart: {e}")
