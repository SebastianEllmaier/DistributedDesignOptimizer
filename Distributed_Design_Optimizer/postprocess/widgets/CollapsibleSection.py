# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Reusable collapsible section widget for panels with expandable groups."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QToolButton, QSizePolicy,
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QColor

from ..styles.Theme import get_accent_color


class CollapsibleSection(QWidget):
    """A section with a clickable header that expands/collapses its content."""

    user_toggled = Signal(bool)

    def __init__(self, title: str, parent: QWidget | None = None,
                 initially_expanded: bool = True) -> None:
        """Initialize the collapsible section.

        Args:
            title: Header text displayed on the toggle button.
            parent: Optional parent widget.
            initially_expanded: Whether the section starts expanded.
        """
        super().__init__(parent)
        self._programmatic = False
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header button
        self._toggle_btn = QToolButton()
        self._toggle_btn.setText(f"  {title}")
        self._toggle_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self._toggle_btn.setArrowType(
            Qt.ArrowType.DownArrow if initially_expanded else Qt.ArrowType.RightArrow
        )
        self._toggle_btn.setCheckable(True)
        self._toggle_btn.setChecked(initially_expanded)
        self._toggle_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._apply_header_style()
        self._toggle_btn.toggled.connect(self._on_toggle)
        layout.addWidget(self._toggle_btn)

        # Content area
        self._content = QWidget()
        self._content_layout = QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(8, 4, 4, 4)
        self._content.setVisible(initially_expanded)
        layout.addWidget(self._content)

    @property
    def content_layout(self) -> QVBoxLayout:
        """Return the layout for adding child widgets.

        Returns:
            The vertical box layout that holds the section's content.
        """
        return self._content_layout

    def set_expanded(self, expanded: bool) -> None:
        """Programmatically expand or collapse the section.

        Args:
            expanded: Whether the section should be expanded.
        """
        self._programmatic = True
        self._toggle_btn.setChecked(expanded)
        self._programmatic = False

    def showEvent(self, event) -> None:  # noqa: N802
        """Re-apply header styling when the widget becomes visible.

        Args:
            event: The show event triggered by Qt.
        """
        super().showEvent(event)
        self._apply_header_style()

    def _apply_header_style(self) -> None:
        accent = get_accent_color()
        c = QColor(accent)
        hover_bg = f"rgba({c.red()}, {c.green()}, {c.blue()}, 0.08)"
        self._toggle_btn.setStyleSheet(
            "QToolButton { font-weight: bold; font-size: 9pt; "
            "border: none; padding: 4px 6px; text-align: left; }"
            f"QToolButton:hover {{ background-color: {hover_bg}; border-radius: 3px; }}"
        )

    def _on_toggle(self, checked: bool) -> None:
        self._toggle_btn.setArrowType(
            Qt.ArrowType.DownArrow if checked else Qt.ArrowType.RightArrow
        )
        self._content.setVisible(checked)
        if not self._programmatic:
            self.user_toggled.emit(checked)
