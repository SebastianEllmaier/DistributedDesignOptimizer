# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Central plot canvas widget with welcome card and Plotly figure display."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QMenu, QFileDialog,
    QStackedWidget, QFrame, QScrollArea,
)
from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtGui import QAction, QResizeEvent

from .PlotlyPanel import PlotlyPanel
from ._welcome_card import WelcomeCard


class PlotCanvas(QWidget):
    """Central plot area with welcome card and interactive Plotly figure display."""

    image_saved = Signal(str)  # forwarded from PlotlyPanel
    resized = Signal(int, int)  # (width, height) emitted on resize

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the plot canvas with a welcome card and Plotly panel.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._stack = QStackedWidget()
        layout.addWidget(self._stack)

        # Page 0: Welcome card inside scroll area for small windows
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._welcome = WelcomeCard()
        scroll.setWidget(self._welcome)
        self._stack.addWidget(scroll)

        # Page 1: Plotly panel (interactive HTML)
        self._panel = PlotlyPanel(parent=self)
        self._panel.init_web_view()  # Pre-init WebEngine to avoid window flash
        self._panel.image_saved.connect(self.image_saved)
        self._stack.addWidget(self._panel)

        self._stack.setCurrentIndex(0)

        # Context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Adjust welcome card margins responsively on resize.

        Args:
            event: The resize event.
        """
        super().resizeEvent(event)
        # Responsive margins based on width
        w = event.size().width()
        margin_h = max(20, int(w * 0.10))
        margin_v = max(20, int(w * 0.05))
        self._welcome.layout().setContentsMargins(margin_h, margin_v, margin_h, margin_v)
        self.resized.emit(event.size().width(), event.size().height())

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_html(self, html: str, fig=None) -> None:
        """Display Plotly HTML content.

        Args:
            html: Raw HTML string containing Plotly chart markup.
            fig: Optional Plotly figure object cached for image export.
        """
        self._stack.setCurrentIndex(1)
        # Defer HTML injection to let the QWebEngineView's render surface
        # initialize after the stack page becomes visible.
        from PySide6.QtCore import QTimer
        QTimer.singleShot(100, lambda: self._panel.set_html(html, fig))

    def set_figure(self, fig) -> None:
        """Accept a Plotly go.Figure, convert and display.

        Args:
            fig: A Plotly ``go.Figure`` to render.
        """
        self._stack.setCurrentIndex(1)
        from PySide6.QtCore import QTimer
        QTimer.singleShot(100, lambda: self._panel.set_figure(fig))

    def refresh(self) -> None:
        """Re-render the current Plotly HTML content."""
        self._panel.refresh()

    def clear(self) -> None:
        """Clear the current plot and show the welcome card."""
        self._panel.clear()
        self._stack.setCurrentIndex(0)

    def get_figure(self):
        """Return the cached Plotly figure, or ``None`` if not set."""
        return self._panel.figure

    def has_content(self) -> bool:
        """Return ``True`` if the panel currently holds HTML content.

        Returns:
            Whether the panel currently has HTML content loaded.
        """
        return self._panel.html is not None

    def export_image(self, path: str, dpi: int = 150) -> None:
        """Export the current plot to a static image file.

        Args:
            path: Destination file path.
            dpi: Resolution in dots per inch.
        """
        self._panel.export_image(path, dpi)

    # ------------------------------------------------------------------
    # Context menu
    # ------------------------------------------------------------------

    def _show_context_menu(self, pos: QPoint) -> None:
        menu = QMenu(self)
        if self._panel.html:
            save_action = QAction("Save Image...", self)
            save_action.triggered.connect(self._save_image_dialog)
            menu.addAction(save_action)

            copy_action = QAction("Copy to Clipboard", self)
            copy_action.triggered.connect(self._panel.copy_to_clipboard)
            menu.addAction(copy_action)
        menu.exec(self.mapToGlobal(pos))

    def _save_image_dialog(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG (*.png);;SVG (*.svg);;PDF (*.pdf);;All Files (*)"
        )
        if path:
            try:
                self.export_image(path)
            except Exception as e:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.critical(self, "Export Error", f"Failed to save image: {e}")
