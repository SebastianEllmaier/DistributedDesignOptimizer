---
title: _welcome_card (Source)
---

← Back to [_welcome_card documentation](_welcome_card.md)

# _welcome_card - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\widgets\_welcome_card.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Welcome card widget shown on startup before any plot is active."""

import pathlib

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtSvgWidgets import QSvgWidget

from ..styles.Theme import get_accent_color, PRIMARY, PRIMARY_LIGHT


class WelcomeCard(QWidget):
    """Start page with quick-start guide shown when no plot is active."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the welcome card with logo, workflow steps, and accent styling.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo
        logo_path = pathlib.Path(__file__).resolve().parents[3] / "docs_src" / "content" / "DistributedDesignOptimizer_Viewer_Logo.svg"
        if logo_path.exists():
            self._logo = QSvgWidget(str(logo_path))
            self._logo.setMaximumSize(300, 200)
            self._logo.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
            self._logo.renderer().setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
            layout.addWidget(self._logo, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addSpacing(12)

        # Title
        self._title = QLabel("DDO Viewer")
        self._title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        layout.addWidget(self._title)

        self._subtitle = QLabel("Distributed Design Optimization — Post-Processing")
        self._subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._subtitle.setStyleSheet("color: gray; font-size: 11pt; margin-bottom: 24px;")
        layout.addWidget(self._subtitle)

        # Accent divider
        self._divider = QFrame()
        self._divider.setFrameShape(QFrame.Shape.HLine)
        self._divider.setFixedHeight(2)
        self._divider.setFixedWidth(200)
        layout.addWidget(self._divider, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(16)

        # Workflow heading
        workflow_label = QLabel("Workflow")
        workflow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        workflow_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #555; margin-bottom: 4px;")
        layout.addWidget(workflow_label)

        layout.addSpacing(8)

        # 4-step workflow matching the activity bar
        steps = [
            ("\U0001F4C2", "1. Data", "Load .dill history files using the side panel"),
            ("\U0001F4CA", "2. Visualization", "Choose between Line Plot or Topology view"),
            ("\U0001F527", "3. Settings", "Configure axes, fonts, legends, and line styles"),
            ("\U0001F916", "4. AI Chat", "Ask questions about the generated visualization"),
        ]
        self._step_icons: list[QLabel] = []
        self._arrow_labels: list[QLabel] = []
        for i, (icon, heading, desc) in enumerate(steps):
            step_widget = QWidget()
            step_row = QHBoxLayout(step_widget)
            step_row.setContentsMargins(0, 2, 0, 2)
            step_row.setSpacing(6)

            icon_label = QLabel(icon)
            icon_label.setFixedWidth(32)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_label.setStyleSheet("font-size: 16pt;")
            step_row.addWidget(icon_label)

            num_label = QLabel(heading)
            num_label.setStyleSheet(f"font-size: 10pt; font-weight: bold; color: {PRIMARY};")
            self._step_icons.append(num_label)
            step_row.addWidget(num_label)

            d_label = QLabel("— " + desc)
            d_label.setStyleSheet("color: #666; font-size: 9pt;")
            step_row.addWidget(d_label)

            layout.addWidget(step_widget, alignment=Qt.AlignmentFlag.AlignCenter)

            # Arrow between steps
            if i < len(steps) - 1:
                arrow = QLabel("▾")
                arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
                arrow.setStyleSheet(f"color: {PRIMARY_LIGHT}; font-size: 14pt;")
                arrow.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(arrow)
                self._arrow_labels.append(arrow)

        layout.addStretch()

        self._apply_accent()

    def _apply_accent(self) -> None:
        accent = get_accent_color()
        self._title.setStyleSheet(f"color: {accent}; margin-bottom: 8px;")
        self._divider.setStyleSheet(f"background-color: {accent};")

    def showEvent(self, event) -> None:
        """Re-apply accent color when the widget becomes visible.

        Args:
            event: The show event.
        """
        super().showEvent(event)
        self._apply_accent()

```
