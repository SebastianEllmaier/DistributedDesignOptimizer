---
title: TopologyControlsWidget (Source)
---

← Back to [TopologyControlsWidget documentation](TopologyControlsWidget.md)

# TopologyControlsWidget - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\widgets\TopologyControlsWidget.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Widget providing controls for selecting and launching topology analyses."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QRadioButton,
    QButtonGroup, QPushButton, QLabel, QComboBox, QStyle,
)
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor

from ..models.AnalysisConfig import AnalysisConfig
from ..styles.Theme import get_accent_color


# (key, display_label, group_header_or_None, description)
_ANALYSIS_OPTIONS: list[tuple[str, str, str | None, str]] = [
    ("master_graph", "Master Graph", "Structure",
     "Visualizes the full coordination graph with subsystem nodes and coupling edges."),
    ("clustering", "Clustering", None,
     "Groups tightly-coupled subsystems into clusters using spectral analysis."),
    ("weighted_degree", "Weighted Degree", "Centrality",
     "Measures total coupling strength (in + out) per subsystem node."),
    ("weighted_in_degree", "Weighted In-Degree", None,
     "Measures incoming coupling strength for each subsystem."),
    ("weighted_out_degree", "Weighted Out-Degree", None,
     "Measures outgoing coupling strength for each subsystem."),
    ("pagerank", "PageRank", None,
     "Ranks subsystems by importance using the PageRank algorithm."),
    ("primal_residual", "Primal Residual", "Residuals",
     "Shows primal feasibility convergence across iterations."),
    ("dual_residual", "Dual Residual", None,
     "Shows dual feasibility convergence across iterations."),
    ("compromise", "Compromise Measure", "Other",
     "Tracks the compromise variable evolution over the optimization."),
]

_HAS_SUB_OPTIONS = {"clustering", "weighted_degree", "weighted_in_degree",
                    "weighted_out_degree", "pagerank", "primal_residual",
                    "dual_residual", "compromise"}


class TopologyControlsWidget(QWidget):
    """Controls for selecting and launching topology analysis."""

    launch_requested = Signal(AnalysisConfig)

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the topology controls widget.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        # --- Analysis type combo (P14) ---
        layout.addWidget(QLabel("Analysis Type"))
        self._analysis_combo = QComboBox()
        current_group: str | None = None
        for key, label, group, _desc in _ANALYSIS_OPTIONS:
            if group is not None and group != current_group:
                current_group = group
                # Insert a disabled separator item for the group header
                self._analysis_combo.addItem(f"— {group} —", "")
                idx = self._analysis_combo.count() - 1
                model = self._analysis_combo.model()
                item = model.item(idx)
                item.setEnabled(False)
            self._analysis_combo.addItem(f"  {label}", key)

        self._analysis_combo.setCurrentIndex(1)  # first real item after header
        self._analysis_combo.currentIndexChanged.connect(self._on_analysis_changed)
        layout.addWidget(self._analysis_combo)

        # Description label (P16)
        self._desc_label = QLabel()
        self._desc_label.setWordWrap(True)
        self._desc_label.setStyleSheet("color: gray; font-size: 8pt; padding: 4px 0;")
        layout.addWidget(self._desc_label)

        # --- Mode group (P15: hidden when irrelevant, D2: flat label instead of QGroupBox) ---
        self._mode_container = QWidget()
        mode_container_layout = QVBoxLayout(self._mode_container)
        mode_container_layout.setContentsMargins(0, 8, 0, 0)
        mode_label = QLabel("Mode")
        mode_label.setStyleSheet("font-weight: bold; font-size: 9pt;")
        mode_container_layout.addWidget(mode_label)
        self._mode_group = QButtonGroup(self)
        self._mode_group.setExclusive(True)
        self._static_rb = QRadioButton("Static")
        self._dynamic_rb = QRadioButton("Dynamic")
        self._static_rb.setChecked(True)
        self._mode_group.addButton(self._static_rb, 0)
        self._mode_group.addButton(self._dynamic_rb, 1)
        mode_container_layout.addWidget(self._static_rb)
        mode_container_layout.addWidget(self._dynamic_rb)
        self._mode_container.setVisible(False)
        layout.addWidget(self._mode_container)

        # E4: Stretch pushes launch button to the bottom
        layout.addStretch()

        # E3: Styled launch button with icon and accent
        self._launch_btn = QPushButton("  Launch Visualization")
        self._launch_btn.setMinimumHeight(40)
        self._launch_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self._launch_btn.clicked.connect(self._on_launch_clicked)
        layout.addWidget(self._launch_btn)

        # Initialize description and accent
        self._on_analysis_changed(self._analysis_combo.currentIndex())
        self._apply_accent()

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def get_config(self) -> AnalysisConfig:
        """Build an AnalysisConfig from current widget state.

        Returns:
            AnalysisConfig populated with the selected analysis type and mode.
        """
        key = self._analysis_combo.currentData() or "master_graph"
        mode = "dynamic" if self._dynamic_rb.isChecked() else "static"
        return AnalysisConfig(analysis_type=key, mode=mode)

    def _apply_accent(self) -> None:
        accent = get_accent_color()
        base = QColor(accent)
        hover = base.lighter(120).name()
        pressed = base.darker(130).name()
        self._launch_btn.setStyleSheet(
            f"QPushButton {{ font-weight: bold; background-color: {accent}; color: white; "
            f"border-radius: 4px; padding: 8px 16px; }}"
            f"QPushButton:hover {{ background-color: {hover}; }}"
            f"QPushButton:pressed {{ background-color: {pressed}; }}"
        )

    def showEvent(self, event) -> None:
        """Re-apply accent color when the widget becomes visible.

        Args:
            event: The show event.
        """
        super().showEvent(event)
        self._apply_accent()

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _on_analysis_changed(self, index: int) -> None:
        key = self._analysis_combo.itemData(index) or ""
        # Skip disabled group headers
        if not key:
            return
        # Update description
        for k, _lbl, _grp, desc in _ANALYSIS_OPTIONS:
            if k == key:
                self._desc_label.setText(desc)
                break
        # P15: show/hide mode group
        self._mode_container.setVisible(key in _HAS_SUB_OPTIONS)

    def _on_launch_clicked(self) -> None:
        key = self._analysis_combo.currentData()
        if not key:
            return
        config = self.get_config()
        self.launch_requested.emit(config)

```
