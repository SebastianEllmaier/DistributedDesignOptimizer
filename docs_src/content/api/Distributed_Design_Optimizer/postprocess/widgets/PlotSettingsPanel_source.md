---
title: PlotSettingsPanel (Source)
---

← Back to [PlotSettingsPanel documentation](PlotSettingsPanel.md)

# PlotSettingsPanel - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\widgets\PlotSettingsPanel.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Plot settings panel with collapsible sections for configuring chart appearance."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QCheckBox,
    QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit,
    QPushButton, QScrollArea, QGridLayout, QLabel, QFrame,
    QSizePolicy, QMessageBox,
)
from PySide6.QtCore import Signal, Qt, QTimer, QLocale
from PySide6.QtGui import QColor, QPainter, QPen, QPainterPath

import math

from ..models.PlotConfig import PlotConfig, FontConfig, LineConfig, ReferenceLine
from ..styles.Theme import get_accent_color, PRIMARY, PRIMARY_LIGHT, PRIMARY_DARK, SECONDARY
from .CollapsibleSection import CollapsibleSection as _CollapsibleSection
from .ToggleSwitch import ToggleSwitch



# ======================================================================
# Plot sketch background widget
# ======================================================================


class _PlotSketchWidget(QWidget):
    """Greyed-out exemplary x-y line plot as visual guide."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the sketch widget.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.setMinimumSize(200, 160)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def paintEvent(self, event) -> None:  # noqa: ARG002
        """Draw the exemplary convergence plot sketch.

        Args:
            event: The paint event triggered by Qt.
        """
        p = QPainter()
        if not p.begin(self):
            return
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        m = 14
        al, ar, at, ab = m, w - m, m, h - m
        pw, ph = ar - al, ab - at

        # Axes
        axis_c = QColor(195, 195, 195)
        p.setPen(QPen(axis_c, 1.5))
        p.drawLine(al, at, al, ab)
        p.drawLine(al, ab, ar, ab)

        # Ticks & faint grid
        grid_pen = QPen(QColor(230, 230, 230), 1, Qt.PenStyle.DotLine)
        tick_pen = QPen(axis_c, 1)
        for i in range(1, 6):
            x = int(al + i * pw / 5)
            p.setPen(tick_pen); p.drawLine(x, ab, x, ab + 3)
            p.setPen(grid_pen); p.drawLine(x, at, x, ab)
        for i in range(1, 5):
            y = int(ab - i * ph / 4)
            p.setPen(tick_pen); p.drawLine(al - 3, y, al, y)
            p.setPen(grid_pen); p.drawLine(al, y, ar, y)

        # Sample convergence curve
        p.setPen(QPen(QColor(170, 200, 220), 2.5))
        path = QPainterPath()
        n = 60
        for i in range(n):
            t = i / (n - 1)
            val = 0.75 * math.exp(-3 * t) + 0.15 + 0.06 * math.sin(10 * t) * math.exp(-2 * t)
            xi = al + t * pw
            yi = ab - val * ph
            if i == 0:
                path.moveTo(xi, yi)
            else:
                path.lineTo(xi, yi)
        p.drawPath(path)
        p.end()


# ======================================================================
# Main settings panel
# ======================================================================

class PlotSettingsPanel(QWidget):
    """Single scrollable panel with collapsible sections for all plot settings.

    All changes auto-apply (P13) — no manual Apply button needed.
    Topology controls are NOT included here (P2 — they live in TopologyPanel).
    """

    settings_changed = Signal()
    customization_reset = Signal()

    # Debounce timer interval (ms) for auto-apply
    _DEBOUNCE_MS = 250
    # Common fixed width for text input fields
    _INPUT_WIDTH = 150

    @staticmethod
    def _make_combo(items: list[str] | None = None) -> QComboBox:
        """Create a QComboBox that auto-sizes to its widest content."""
        combo = QComboBox()
        combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        combo.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        if items:
            combo.addItems(items)
        return combo

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the settings panel and build the UI.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)

        self._ref_line_widgets: list[dict] = []
        self._legend_entries: dict[str, QLineEdit] = {}
        self._per_line_widgets: dict[str, dict] = {}
        self._user_collapsed_per_line = False

        # Debounce timer for auto-apply
        self._debounce_timer = QTimer(self)
        self._debounce_timer.setSingleShot(True)
        self._debounce_timer.setInterval(self._DEBOUNCE_MS)
        self._debounce_timer.timeout.connect(self._emit_settings)

        self._setup_ui()

    def _setup_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_content = QWidget()
        self._main_layout = QVBoxLayout(scroll_content)
        self._main_layout.setContentsMargins(4, 4, 4, 4)
        self._main_layout.setSpacing(2)

        self._build_plot_layout_section()
        self._build_per_line_section()

        # D5: Track user-initiated collapses
        self._per_line_section.user_toggled.connect(self._on_per_line_user_toggled)

        self._build_legend_section()
        self._build_ref_lines_section()
        self._build_reset_section()

        self._main_layout.addStretch()
        scroll.setWidget(scroll_content)
        outer.addWidget(scroll)

    # ------------------------------------------------------------------
    # Section: Plot Layout (visual arrangement around exemplary plot)
    # ------------------------------------------------------------------

    def _build_plot_layout_section(self) -> None:
        sec = _CollapsibleSection("Plot Layout", parent=self, initially_expanded=True)

        grid = QGridLayout()
        grid.setSpacing(8)

        # Row 0, Col 1: Title input + font (above the plot)
        title_col = QVBoxLayout()
        title_row = QHBoxLayout()
        title_lbl = QLabel("Title:")
        title_lbl.setStyleSheet("font-weight: bold; font-size: 9pt;")
        title_row.addWidget(title_lbl)
        self._title_edit = QLineEdit()
        self._title_edit.setMinimumWidth(self._INPUT_WIDTH)
        self._title_edit.setPlaceholderText("(no default title)")
        self._title_edit.textChanged.connect(self._schedule_change)
        title_row.addWidget(self._title_edit)
        title_col.addLayout(title_row)
        self._title_font_size = self._build_font_size_row(title_col)

        # Stacked titles container (shown when Y-axis = Stacked)
        self._stacked_titles_container = QWidget()
        self._stacked_titles_layout = QVBoxLayout(self._stacked_titles_container)
        self._stacked_titles_layout.setContentsMargins(0, 4, 0, 0)
        self._stacked_titles_container.hide()
        self._stacked_title_edits: list[QLineEdit] = []
        title_col.addWidget(self._stacked_titles_container)

        grid.addLayout(title_col, 0, 1)

        # Row 1, Col 0: Y-axis controls (along left / y-axis)
        grid.addLayout(self._build_y_axis_column(), 1, 0)

        # Row 1, Col 1: Exemplary plot sketch (background)
        self._sketch = _PlotSketchWidget()
        grid.addWidget(self._sketch, 1, 1)

        # Row 2, Col 0: Display options (origin corner)
        grid.addLayout(self._build_display_column(), 2, 0)

        # Row 2, Col 1: X-axis controls (along bottom / x-axis)
        grid.addLayout(self._build_x_axis_column(), 2, 1)

        # Let the sketch area expand
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 0)

        sec.content_layout.addLayout(grid)
        self._main_layout.addWidget(sec)

        # Initialize descriptions
        self._on_x_axis_changed(0)
        self._on_y_axis_changed(0)

    def _build_y_axis_column(self) -> QVBoxLayout:
        """Left side (along y-axis): segmented control, log toggle, label."""
        col = QVBoxLayout()

        y_header = QLabel("Y-Axis")
        y_header.setStyleSheet("font-weight: bold; font-size: 9pt; margin-bottom: 4px;")
        col.addWidget(y_header)

        self._y_axis_options = [
            ("shared", "Shared", "All series share one Y-axis"),
            ("independent", "Independent", "Each series gets its own Y-axis"),
            ("centered", "Centered", "Y-axis centered around zero"),
            ("stacked", "Stacked", "Series stacked in separate sub-plots"),
        ]
        self._y_axis_keys = [k for k, _, _ in self._y_axis_options]
        self._y_axis_tips = [t for _, _, t in self._y_axis_options]
        y_labels = [lbl for _, lbl, _ in self._y_axis_options]

        self._y_axis_segment = self._make_combo(y_labels)
        self._y_axis_segment.setCurrentIndex(0)
        self._y_axis_segment.setToolTip("Select Y-axis layout mode")
        self._y_axis_segment.currentIndexChanged.connect(self._on_y_axis_changed)
        col.addWidget(self._y_axis_segment)

        self._y_desc_label = QLabel()
        self._y_desc_label.setWordWrap(True)
        self._y_desc_label.setStyleSheet("color: gray; font-size: 8pt;")
        col.addWidget(self._y_desc_label)

        col.addSpacing(6)
        scale_row = QHBoxLayout()
        scale_lbl = QLabel("Scale:")
        scale_lbl.setStyleSheet("font-size: 8pt; color: black;")
        scale_row.addWidget(scale_lbl)
        self._scale_segment = self._make_combo(["Linear", "Log"])
        self._scale_segment.setCurrentIndex(0)
        self._scale_segment.setToolTip("Select y-axis scaling")
        self._scale_segment.currentIndexChanged.connect(self._schedule_change)
        scale_row.addWidget(self._scale_segment)
        scale_row.addStretch()
        col.addLayout(scale_row)

        col.addSpacing(6)
        # Unified y-label container: a single "Label" field for shared/centered
        # modes, or one field per data series for independent/stacked modes.
        # Rebuilt on Y-axis mode change and on data refresh; typed values are
        # cached per mode so they persist across mode switches.
        self._plottable_data: list[tuple[str, list]] = []
        self._y_label_edits: list[QLineEdit] = []
        self._y_label_cache: dict[str, list[str]] = {}
        self._y_labels_current_bucket: str | None = None
        self._y_labels_container = QWidget()
        self._y_labels_layout = QVBoxLayout(self._y_labels_container)
        self._y_labels_layout.setContentsMargins(0, 0, 0, 0)
        col.addWidget(self._y_labels_container)
        self._y_font_size = self._build_font_size_row(col)

        col.addSpacing(4)
        self._y_tick_label_size = self._build_size_row(col, "Tick label size:")
        self._y_tick_marker_size = self._build_size_row(col, "Tick marker size:", default=8, min_val=2, max_val=20)

        col.addStretch()
        return col

    def _build_display_column(self) -> QVBoxLayout:
        """Bottom-left (origin corner): display options."""
        col = QVBoxLayout()

        display_header = QLabel("Display")
        display_header.setStyleSheet("font-weight: bold; font-size: 9pt; margin-bottom: 4px;")
        col.addWidget(display_header)

        self._show_grid_cb = ToggleSwitch("Grid")
        self._show_grid_cb.setToolTip("Overlay grid lines on the plot background")
        self._show_grid_cb.toggled.connect(self._schedule_change)
        col.addWidget(self._show_grid_cb)

        col.addStretch()
        return col

    # ------------------------------------------------------------------
    # Section: Legend (toggle-activated)
    # ------------------------------------------------------------------

    def _build_legend_section(self) -> None:
        # Collapsible section with toggle switch in the header
        self._legend_collapsible = _CollapsibleSection(
            "Legend", parent=self, initially_expanded=False
        )

        # Insert toggle switch into the collapsible header row
        self._show_legend_cb = ToggleSwitch("")
        self._show_legend_cb.setChecked(False)
        self._show_legend_cb.setToolTip("Enable legend on the plot")
        self._show_legend_cb.toggled.connect(self._on_legend_show_toggled)
        # Add toggle to the right of the header button
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        header_layout.addWidget(self._legend_collapsible._toggle_btn)
        header_layout.addStretch()
        header_layout.addWidget(self._show_legend_cb)
        header_widget = QWidget()
        header_widget.setLayout(header_layout)
        # Replace the default toggle button in the collapsible's layout
        self._legend_collapsible.layout().removeWidget(self._legend_collapsible._toggle_btn)
        self._legend_collapsible.layout().insertWidget(0, header_widget)
        # Disable expand until toggle is switched on
        self._legend_collapsible._toggle_btn.setEnabled(False)

        legend_detail = self._legend_collapsible.content_layout
        legend_detail.setSpacing(4)

        self._legend_pos_options = [
            "upper right", "upper left", "lower left", "lower right",
            "upper center", "lower center", "center left",
            "center right",
        ]
        pos_lbl = QLabel("Position:")
        pos_lbl.setStyleSheet("font-size: 8pt; color: black;")
        legend_detail.addWidget(pos_lbl)
        self._legend_pos_segment = self._make_combo(self._legend_pos_options)
        self._legend_pos_segment.setCurrentIndex(0)
        self._legend_pos_segment.setToolTip("Legend placement")
        self._legend_pos_segment.currentIndexChanged.connect(self._schedule_change)
        legend_detail.addWidget(self._legend_pos_segment)

        self._legend_font_size = self._build_font_size_row(legend_detail)

        # Custom names title + scroll area
        custom_names_lbl = QLabel("Custom Names")
        custom_names_lbl.setStyleSheet("font-weight: bold; font-size: 9pt; margin-top: 6px;")
        legend_detail.addWidget(custom_names_lbl)
        self._legend_scroll = QScrollArea()
        self._legend_scroll.setWidgetResizable(True)
        self._legend_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._legend_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._legend_scroll_content = QWidget()
        self._legend_entries_layout = QVBoxLayout(self._legend_scroll_content)
        self._legend_scroll.setWidget(self._legend_scroll_content)
        self._legend_scroll.setMaximumHeight(120)
        legend_detail.addWidget(self._legend_scroll)

        self._main_layout.addWidget(self._legend_collapsible)

    def _build_x_axis_column(self) -> QVBoxLayout:
        """Bottom (along x-axis): segmented control, description, boundaries, label."""
        col = QVBoxLayout()

        x_header = QLabel("X-Axis")
        x_header.setStyleSheet("font-weight: bold; font-size: 9pt; margin-bottom: 4px;")
        col.addWidget(x_header)

        self._x_axis_options = [
            ("queue_count", "Sequential",
             "Simple 0,1,2,… index per data point"),
            ("combined_ticks", "Equispaced Outer/Inner Iterations",
             "Aligns series by outer-loop iteration with inner-loop minor ticks"),
            ("equispaced_major", "Equispaced Outer Iterations",
             "Equal spacing between outer-loop iterations"),
            ("cumulative_runtime", "Runtime",
             "X-axis shows accumulated wall-clock time"),
            ("cumulative_evaluations", "Number of Evaluations",
             "X-axis shows accumulated design variable evaluations"),
        ]
        self._x_axis_keys = [k for k, _, _ in self._x_axis_options]
        self._x_axis_tips = [t for _, _, t in self._x_axis_options]
        x_labels = [lbl for _, lbl, _ in self._x_axis_options]

        self._x_axis_segment = self._make_combo(x_labels)
        self._x_axis_segment.setCurrentIndex(0)
        self._x_axis_segment.setToolTip("Select how the x-axis is scaled")
        self._x_axis_segment.currentIndexChanged.connect(self._on_x_axis_changed)
        col.addWidget(self._x_axis_segment)

        self._x_desc_label = QLabel()
        self._x_desc_label.setWordWrap(True)
        self._x_desc_label.setStyleSheet("color: gray; font-size: 8pt;")
        col.addWidget(self._x_desc_label)

        col.addSpacing(4)
        x_lbl = QLabel("Label:")
        x_lbl.setStyleSheet("font-size: 8pt; color: black;")
        col.addWidget(x_lbl)
        self._x_label_edit = QLineEdit()
        self._x_label_edit.setMinimumWidth(self._INPUT_WIDTH)
        self._x_label_edit.setPlaceholderText("Sequence Index")
        self._x_label_edit.textChanged.connect(self._schedule_change)
        col.addWidget(self._x_label_edit)
        self._x_font_size = self._build_font_size_row(col)

        col.addSpacing(4)
        self._x_tick_label_size = self._build_size_row(col, "Tick label size:")
        self._x_tick_marker_size = self._build_size_row(col, "Tick marker size:", default=8, min_val=2, max_val=20)

        return col

    # ------------------------------------------------------------------
    # Helper: inline font size row
    # ------------------------------------------------------------------

    def _build_font_size_row(self, parent_layout: QVBoxLayout) -> QSpinBox:
        """Add a compact 'Font size: [spin]' row to a layout and return the spin box."""
        row = QHBoxLayout()
        lbl = QLabel("Font size:")
        lbl.setStyleSheet("font-size: 8pt; color: black;")
        row.addWidget(lbl)
        spin = QSpinBox()
        spin.setRange(6, 30)
        spin.setValue(12)
        spin.setFixedWidth(50)
        spin.valueChanged.connect(self._schedule_change)
        row.addWidget(spin)
        row.addStretch()
        parent_layout.addLayout(row)
        return spin

    def _build_size_row(self, parent_layout: QVBoxLayout, label: str,
                        default: int = 12, min_val: int = 6, max_val: int = 30) -> QSpinBox:
        """Add a compact labeled size spinbox row and return the spin box."""
        row = QHBoxLayout()
        lbl = QLabel(label)
        lbl.setStyleSheet("font-size: 8pt; color: black;")
        row.addWidget(lbl)
        spin = QSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(default)
        spin.setFixedWidth(50)
        spin.valueChanged.connect(self._schedule_change)
        row.addWidget(spin)
        row.addStretch()
        parent_layout.addLayout(row)
        return spin

    def _read_font_config(self, size_spin: QSpinBox) -> FontConfig:
        """Read a FontConfig from a font size spinbox."""
        return FontConfig(size=size_spin.value())

    def _reset_font_size(self, size_spin: QSpinBox) -> None:
        """Reset a font size spinbox to default."""
        size_spin.setValue(12)

    # ------------------------------------------------------------------
    # Section: Per-Line Settings
    # ------------------------------------------------------------------

    def _build_per_line_section(self) -> None:
        self._per_line_section = _CollapsibleSection(
            "Per-Line Settings", parent=self, initially_expanded=False
        )
        self._per_line_container = QVBoxLayout()
        self._per_line_placeholder = QLabel("Plot data to configure per-line styles")
        self._per_line_placeholder.setStyleSheet("color: gray;")
        self._per_line_container.addWidget(self._per_line_placeholder)
        self._per_line_section.content_layout.addLayout(self._per_line_container)
        self._main_layout.addWidget(self._per_line_section)

    # ------------------------------------------------------------------
    # Section: Reference Lines (toggle-activated)
    # ------------------------------------------------------------------

    def _build_ref_lines_section(self) -> None:
        # Collapsible section with toggle switch in the header
        self._ref_lines_collapsible = _CollapsibleSection(
            "Reference Lines", parent=self, initially_expanded=False
        )

        # Insert toggle switch into the collapsible header row
        self._show_ref_lines_cb = ToggleSwitch("")
        self._show_ref_lines_cb.setChecked(False)
        self._show_ref_lines_cb.setToolTip("Enable horizontal reference lines on the plot")
        self._show_ref_lines_cb.toggled.connect(self._on_ref_lines_toggled)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        header_layout.addWidget(self._ref_lines_collapsible._toggle_btn)
        header_layout.addStretch()
        header_layout.addWidget(self._show_ref_lines_cb)
        header_widget = QWidget()
        header_widget.setLayout(header_layout)
        self._ref_lines_collapsible.layout().removeWidget(self._ref_lines_collapsible._toggle_btn)
        self._ref_lines_collapsible.layout().insertWidget(0, header_widget)
        # Disable expand until toggle is switched on
        self._ref_lines_collapsible._toggle_btn.setEnabled(False)

        ref_detail = self._ref_lines_collapsible.content_layout
        ref_detail.setSpacing(4)

        self._ref_lines_container = QVBoxLayout()
        ref_detail.addLayout(self._ref_lines_container)
        add_ref_btn = QPushButton("+ Add Reference Line")
        add_ref_btn.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        add_ref_btn.setStyleSheet(
            f"QPushButton {{ background-color: {PRIMARY}; color: white; "
            f"font-weight: bold; padding: 5px 12px; border-radius: 3px; }}"
            f"QPushButton:hover {{ background-color: {PRIMARY_LIGHT}; }}"
        )
        add_ref_btn.clicked.connect(self._add_reference_line)
        ref_detail.addWidget(add_ref_btn)

        self._main_layout.addWidget(self._ref_lines_collapsible)

    # ------------------------------------------------------------------
    # Section: Reset
    # ------------------------------------------------------------------

    def _build_reset_section(self) -> None:
        self._reset_btn = QPushButton("Reset All Customization")
        self._reset_btn.setToolTip("Reset font, labels, legend, reference lines and per-line styles")
        self._reset_btn.setStyleSheet(
            "QPushButton { background-color: #cc4444; color: white; "
            "font-weight: bold; padding: 5px 12px; border-radius: 3px; }"
            "QPushButton:hover { background-color: #aa3333; }"
        )
        self._reset_btn.clicked.connect(self._on_reset_customization)
        self._main_layout.addWidget(self._reset_btn)

    # ==================================================================
    # Public API
    # ==================================================================

    def get_plot_config(self) -> PlotConfig:
        """Collect all widget state into a PlotConfig dataclass.

        Returns:
            A PlotConfig instance reflecting the current UI selections.
        """
        y_idx = self._y_axis_segment.currentIndex()
        plot_type = self._y_axis_keys[y_idx]
        x_idx = self._x_axis_segment.currentIndex()
        x_axis_type = self._x_axis_keys[x_idx]

        line_configs: dict[str, LineConfig] = {}
        for path, edit in self._legend_entries.items():
            style = "solid"
            width = 2.0
            color: str | None = None
            markers = True
            if path in self._per_line_widgets:
                style = self._per_line_widgets[path]["style"].currentText()
                width = self._per_line_widgets[path]["width"].value()
                c = self._per_line_widgets[path]["color"].currentText()
                color = None if c == "auto" else c
                markers = self._per_line_widgets[path]["markers"].isChecked()
            line_configs[path] = LineConfig(
                item_path=path,
                label=edit.text() or self._format_legend_label(path),
                style=style,
                width=width,
                color=color,
                markers=markers,
            )

        ref_lines: list[ReferenceLine] = []
        for i, w in enumerate(self._ref_line_widgets):
            ref_key = f"__ref_{i}"
            # Defaults
            r_style = "dash"
            r_color = "red"
            r_width = 1.5
            r_markers = False
            if ref_key in self._per_line_widgets:
                r_style = self._per_line_widgets[ref_key]["style"].currentText()
                c = self._per_line_widgets[ref_key]["color"].currentText()
                r_color = "red" if c == "auto" else c
                r_width = self._per_line_widgets[ref_key]["width"].value()
                r_markers = self._per_line_widgets[ref_key]["markers"].isChecked()
            ref_lines.append(ReferenceLine(
                name=w["name"].text() or w["name"].placeholderText(),
                value=w["value"].value(),
                color=r_color,
                style=r_style,
                width=r_width,
                enabled=w["enabled"].isChecked(),
                markers=r_markers,
            ))

        y_mode = self._y_axis_keys[self._y_axis_segment.currentIndex()]
        y_texts = [e.text() for e in self._y_label_edits]

        return PlotConfig(
            plot_type=plot_type,
            log_scale=(self._scale_segment.currentIndex() == 1),
            x_axis_type=x_axis_type,
            show_legend=self._show_legend_cb.isChecked(),
            show_grid=self._show_grid_cb.isChecked(),
            legend_position=self._legend_pos_options[
                self._legend_pos_segment.currentIndex()
            ],
            custom_x_label=self._x_label_edit.text(),
            custom_y_label=(y_texts[0] if y_mode == "shared" and y_texts else ""),
            custom_title=self._title_edit.text(),
            stacked_titles=[e.text() for e in self._stacked_title_edits],
            stacked_y_labels=(y_texts if y_mode == "stacked" else []),
            independent_y_labels=(y_texts if y_mode in ("independent", "centered") else []),
            title_font=self._read_font_config(self._title_font_size),
            x_label_font=self._read_font_config(self._x_font_size),
            y_label_font=self._read_font_config(self._y_font_size),
            legend_font=self._read_font_config(self._legend_font_size),
            x_tick_label_font=self._read_font_config(self._x_tick_label_size),
            y_tick_label_font=self._read_font_config(self._y_tick_label_size),
            x_tick_size=self._x_tick_marker_size.value(),
            y_tick_size=self._y_tick_marker_size.value(),
            line_configs=line_configs,
            reference_lines=ref_lines,
        )

    def refresh_line_entries(self, plottable_data: list[tuple[str, list]]) -> None:
        """Rebuild custom legend name fields and per-line style controls.

        P12: Auto-expand Legend and Per-Line sections when data is populated.

        Args:
            plottable_data: List of (item_path, values) tuples for each series.
        """
        self._legend_entries.clear()
        self._per_line_widgets.clear()
        self._plottable_data = plottable_data

        if not plottable_data:
            old_legend = self._legend_scroll.takeWidget()
            if old_legend:
                old_legend.deleteLater()
            new_legend = QWidget()
            QVBoxLayout(new_legend)
            self._legend_scroll.setWidget(new_legend)
            self._legend_entries_layout = new_legend.layout()
            self._replace_per_line_container(QLabel("Plot data to configure per-line styles"))

            self._per_line_section.set_expanded(False)
            self._rebuild_y_labels()
            return

        # P12: auto-expand sections when data is populated


        # Fresh legend scroll content
        old_legend = self._legend_scroll.takeWidget()
        if old_legend:
            old_legend.deleteLater()
        new_legend_content = QWidget()
        new_legend_layout = QVBoxLayout(new_legend_content)
        self._legend_scroll.setWidget(new_legend_content)
        self._legend_entries_layout = new_legend_layout

        # Fresh per-line content
        per_line_content = QWidget()
        per_line_layout = QVBoxLayout(per_line_content)
        per_line_layout.setContentsMargins(0, 0, 0, 0)

        color_options = [
            "auto", "red", "blue", "green", "orange", "purple",
            "black", "gray", "cyan", "magenta", "brown", "pink",
        ]

        for item_path, _ in plottable_data:
            label = self._format_legend_label(item_path)

            # Legend name entry
            row = QHBoxLayout()
            name_edit = QLineEdit(label)
            name_edit.setFixedWidth(400)
            name_edit.setPlaceholderText(label)
            name_edit.textChanged.connect(self._schedule_change)
            scroll_lbl = self._make_scrollable_label(f"{label}:")
            row.addWidget(scroll_lbl, 1)  # stretch factor 1
            row.addWidget(name_edit, 0)   # stretch factor 0: fixed, doesn't grow
            self._legend_entries_layout.addLayout(row)
            self._legend_entries[item_path] = name_edit

            # Per-line style/color/width
            pl_row = QHBoxLayout()
            pl_row.addWidget(self._make_scrollable_label(label))
            pl_row.addWidget(QLabel("Style:"))
            style_combo = self._make_combo(["solid", "dash", "dot", "dashdot"])
            style_combo.currentIndexChanged.connect(self._schedule_change)
            pl_row.addWidget(style_combo)
            pl_row.addWidget(QLabel("Color:"))
            color_combo = self._make_combo(color_options)
            color_combo.currentIndexChanged.connect(self._schedule_change)
            pl_row.addWidget(color_combo)
            pl_row.addWidget(QLabel("Width:"))
            width_spin = QDoubleSpinBox()
            width_spin.setFixedWidth(80)
            width_spin.setRange(0.5, 10.0)
            width_spin.setValue(2.0)
            width_spin.setSingleStep(0.5)
            width_spin.valueChanged.connect(self._schedule_change)
            pl_row.addWidget(width_spin)
            markers_switch = ToggleSwitch("Markers")
            markers_switch.setChecked(True)
            markers_switch.toggled.connect(self._schedule_change)
            pl_row.addWidget(markers_switch)
            per_line_layout.addLayout(pl_row)
            self._per_line_widgets[item_path] = {
                "style": style_combo, "color": color_combo, "width": width_spin,
                "markers": markers_switch,
            }

        # Include active reference lines in per-line settings
        for i, w in enumerate(self._ref_line_widgets):
            if w["enabled"].isChecked():
                ref_name = w["name"].text() or w["name"].placeholderText()
                ref_key = f"__ref_{i}"
                pl_row = QHBoxLayout()
                ref_label_widget = self._make_scrollable_label(f"[Ref] {ref_name}")
                pl_row.addWidget(ref_label_widget)
                pl_row.addWidget(QLabel("Style:"))
                style_combo = self._make_combo(["solid", "dash", "dot", "dashdot"])
                style_combo.setCurrentText("dash")
                style_combo.currentIndexChanged.connect(self._schedule_change)
                pl_row.addWidget(style_combo)
                pl_row.addWidget(QLabel("Color:"))
                color_combo = self._make_combo(color_options)
                color_combo.setCurrentText("red")
                color_combo.currentIndexChanged.connect(self._schedule_change)
                pl_row.addWidget(color_combo)
                pl_row.addWidget(QLabel("Width:"))
                width_spin = QDoubleSpinBox()
                width_spin.setFixedWidth(80)
                width_spin.setRange(0.5, 10.0)
                width_spin.setValue(1.5)
                width_spin.setSingleStep(0.5)
                width_spin.valueChanged.connect(self._schedule_change)
                pl_row.addWidget(width_spin)
                markers_switch = ToggleSwitch("Markers")
                markers_switch.toggled.connect(self._schedule_change)
                pl_row.addWidget(markers_switch)
                per_line_layout.addLayout(pl_row)
                self._per_line_widgets[ref_key] = {
                    "style": style_combo, "color": color_combo, "width": width_spin,
                    "markers": markers_switch,
                    "label": ref_label_widget.widget(),
                }

        self._replace_per_line_container(per_line_content)

        # Rebuild per-subplot title fields (stacked mode) and the unified
        # y-label field(s) for the current data series / Y-axis mode.
        self._rebuild_stacked_titles(plottable_data)
        self._rebuild_y_labels()

    # ==================================================================
    # Private helpers
    # ==================================================================

    def _rebuild_stacked_titles(self, plottable_data: list[tuple[str, list]]) -> None:
        """Rebuild per-subplot title fields for stacked mode."""
        # Clear old stacked title edits
        while self._stacked_titles_layout.count():
            item = self._stacked_titles_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._stacked_title_edits.clear()

        if not plottable_data:
            return

        # Add header
        title_header = QLabel("Per-subplot titles:")
        title_header.setStyleSheet("font-size: 8pt; color: black;")
        self._stacked_titles_layout.addWidget(title_header)

        for item_path, _ in plottable_data:
            label = self._format_legend_label(item_path)

            # Title field
            title_edit = QLineEdit()
            title_edit.setPlaceholderText(label)
            title_edit.setMinimumWidth(self._INPUT_WIDTH)
            title_edit.textChanged.connect(self._schedule_change)
            self._stacked_titles_layout.addWidget(title_edit)
            self._stacked_title_edits.append(title_edit)

    @staticmethod
    def _y_label_bucket(mode: str) -> str:
        """Cache bucket for a Y-axis mode (each mode keeps its own values)."""
        return mode

    def _snapshot_y_labels(self) -> None:
        """Save the currently displayed y-label texts into the per-mode cache."""
        if self._y_labels_current_bucket is not None:
            self._y_label_cache[self._y_labels_current_bucket] = [
                e.text() for e in self._y_label_edits
            ]

    def _rebuild_y_labels(self) -> None:
        """(Re)build the unified y-label field(s) for the current Y-axis mode.

        Shared/Centered show a single "Label" field; Independent/Stacked show
        one field per data series. Values are cached per mode so they persist
        across mode switches.
        """
        # Preserve whatever the user has currently typed before clearing.
        self._snapshot_y_labels()

        while self._y_labels_layout.count():
            item = self._y_labels_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._y_label_edits = []

        mode = self._y_axis_keys[self._y_axis_segment.currentIndex()]
        bucket = self._y_label_bucket(mode)
        saved = self._y_label_cache.get(bucket, [])
        per_series = mode in ("independent", "centered", "stacked")

        if per_series and self._plottable_data:
            header = QLabel(
                "Per-subplot Y-labels:" if mode == "stacked"
                else "Per-axis Y-labels:"
            )
            header.setStyleSheet("font-size: 8pt; color: black;")
            self._y_labels_layout.addWidget(header)
            placeholders = [
                self._format_legend_label(item_path)
                for item_path, _ in self._plottable_data
            ]
        else:
            lbl = QLabel("Label:")
            lbl.setStyleSheet("font-size: 8pt; color: black;")
            self._y_labels_layout.addWidget(lbl)
            placeholders = [self._Y_AXIS_DEFAULT_LABELS.get(mode, "Value")]

        for i, placeholder in enumerate(placeholders):
            edit = QLineEdit()
            edit.setFixedWidth(self._INPUT_WIDTH)
            edit.setPlaceholderText(placeholder)
            if i < len(saved):
                edit.setText(saved[i])
            edit.textChanged.connect(self._schedule_change)
            self._y_labels_layout.addWidget(edit)
            self._y_label_edits.append(edit)

        self._y_labels_current_bucket = bucket

    def _schedule_change(self, *_args) -> None:
        """Debounced auto-apply: restart timer on each change."""
        self._debounce_timer.start()

    @staticmethod
    def _format_legend_label(item_path: str) -> str:
        """Format an item_path into a readable legend label using full file path."""
        parts = item_path.split("/", 1)
        if len(parts) == 2:
            entry_id = parts[0].replace("historyfile_", "")
            return f"{entry_id}/{parts[1]}"
        return item_path

    @staticmethod
    def _make_scrollable_label(text: str, min_width: int = 300) -> QScrollArea:
        """Create a horizontally-scrollable label with minimum width that can grow."""
        lbl = QLabel(text)
        lbl.setStyleSheet("background: transparent;")
        scroll = QScrollArea()
        scroll.setWidget(lbl)
        scroll.setMinimumWidth(min_width)
        scroll.setFixedHeight(lbl.sizeHint().height() + 18)
        scroll.setWidgetResizable(False)
        scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; }")
        # Scroll to the right end so the most specific part is visible
        QTimer.singleShot(0, lambda: scroll.horizontalScrollBar().setValue(
            scroll.horizontalScrollBar().maximum()))
        return scroll

    def _emit_settings(self) -> None:
        self.settings_changed.emit()

    def _on_per_line_user_toggled(self, expanded: bool) -> None:
        self._user_collapsed_per_line = not expanded

    def _on_y_axis_changed(self, index) -> None:
        if index is None:
            return
        key = self._y_axis_keys[index]
        # Independent/Centered/Stacked require at least 2 data series
        if key in ("independent", "centered", "stacked") and len(self._legend_entries) < 2:
            QMessageBox.warning(
                self, "Insufficient Data",
                f"The \"{self._y_axis_options[index][1]}\" Y-axis mode requires "
                "at least 2 different quantities to be selected.",
            )
            self._y_axis_segment.blockSignals(True)
            self._y_axis_segment.setCurrentIndex(0)  # revert to Shared
            self._y_axis_segment.blockSignals(False)
            self._y_desc_label.setText(self._y_axis_tips[0])
            return
        self._y_desc_label.setText(self._y_axis_tips[index])
        is_stacked = key == "stacked"
        self._stacked_titles_container.setVisible(is_stacked)
        self._rebuild_y_labels()
        self._schedule_change()

    # Default placeholder labels per x-axis option
    _X_AXIS_DEFAULT_LABELS: dict[str, str] = {
        "queue_count": "Sequence Index",
        "combined_ticks": "Outer and Innerloop Iterations",
        "equispaced_major": "Outer and Innerloop Iterations",
        "cumulative_runtime": "Runtime in ms",
        "cumulative_evaluations": "Number of Evaluations",
    }

    # Default placeholder labels per y-axis option
    _Y_AXIS_DEFAULT_LABELS: dict[str, str] = {
        "shared": "Value",
        "independent": "(per-axis labels below)",
        "centered": "Value",
        "stacked": "(per-subplot labels below)",
    }

    def _on_x_axis_changed(self, index) -> None:
        if index is None:
            return
        self._x_desc_label.setText(self._x_axis_tips[index])
        key = self._x_axis_keys[index]
        self._x_label_edit.setPlaceholderText(
            self._X_AXIS_DEFAULT_LABELS.get(key, "Sequence Index")
        )
        self._schedule_change()

    def _on_legend_show_toggled(self, checked: bool) -> None:
        self._legend_collapsible._toggle_btn.setEnabled(checked)
        if checked:
            self._legend_collapsible.set_expanded(True)
        else:
            self._legend_collapsible.set_expanded(False)
        self._schedule_change()

    def _on_ref_lines_toggled(self, checked: bool) -> None:
        self._ref_lines_collapsible._toggle_btn.setEnabled(checked)
        if checked:
            self._ref_lines_collapsible.set_expanded(True)
        else:
            self._ref_lines_collapsible.set_expanded(False)
        self._schedule_change()

    def _replace_per_line_container(self, new_widget: QWidget) -> None:
        parent_layout = self._per_line_container
        while parent_layout.count():
            item = parent_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout_recursive(item.layout())
        parent_layout.addWidget(new_widget)

    @staticmethod
    def _clear_layout_recursive(layout) -> None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                PlotSettingsPanel._clear_layout_recursive(child.layout())

    # Reference lines

    def _add_reference_line(self) -> None:
        row = QHBoxLayout()
        row.setSpacing(4)
        name_lbl = QLabel("Name:")
        name_lbl.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        row.addWidget(name_lbl)
        name_edit = QLineEdit()
        name_edit.setMinimumWidth(self._INPUT_WIDTH)
        name_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        name_edit.setPlaceholderText(f"Ref {len(self._ref_line_widgets) + 1}")
        name_edit.textChanged.connect(self._schedule_change)
        name_edit.textChanged.connect(self._on_ref_name_changed)
        row.addWidget(name_edit)
        value_lbl = QLabel("Value:")
        value_lbl.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        row.addWidget(value_lbl)
        value_spin = QDoubleSpinBox()
        value_spin.setLocale(QLocale(QLocale.Language.C))
        value_spin.setRange(-1e9, 1e9)
        value_spin.setDecimals(4)
        value_spin.setFixedWidth(80)
        value_spin.valueChanged.connect(self._schedule_change)
        row.addWidget(value_spin)
        show_toggle = ToggleSwitch("")
        show_toggle.setChecked(True)
        show_toggle.toggled.connect(self._schedule_change)
        row.addWidget(show_toggle)
        clear_btn = QPushButton("Clear")
        clear_btn.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        clear_btn.setStyleSheet(
            "QPushButton { background-color: #cc4444; color: white; "
            "font-weight: bold; padding: 3px 8px; border-radius: 3px; }"
            "QPushButton:hover { background-color: #aa3333; }"
        )
        row.addWidget(clear_btn)
        # Use a QVBoxLayout wrapper so _remove_reference_line works unchanged
        container = QVBoxLayout()
        container.addLayout(row)
        widget_data: dict = {
            "enabled": show_toggle, "name": name_edit,
            "value": value_spin, "layout": container,
        }
        clear_btn.clicked.connect(lambda checked=False, wd=widget_data: self._remove_reference_line(wd))
        widget_data["remove"] = clear_btn
        self._ref_lines_container.addLayout(container)
        self._ref_line_widgets.append(widget_data)
        self._schedule_change()

    def _remove_reference_line(self, widget_data: dict) -> None:
        if widget_data in self._ref_line_widgets:
            self._ref_line_widgets.remove(widget_data)
            layout = widget_data["layout"]
            # Clear sub-layouts and widgets recursively
            self._clear_layout_recursive(layout)
            self._ref_lines_container.removeItem(layout)
            self._schedule_change()

    def _on_ref_name_changed(self, *_args) -> None:
        """Update per-line settings labels when a reference line name changes."""
        for i, w in enumerate(self._ref_line_widgets):
            ref_key = f"__ref_{i}"
            if ref_key in self._per_line_widgets:
                ref_name = w["name"].text() or w["name"].placeholderText()
                pw = self._per_line_widgets[ref_key]
                if "label" in pw:
                    pw["label"].setText(f"[Ref] {ref_name}")

    def _on_reset_customization(self) -> None:
        msg = QMessageBox(
            QMessageBox.Icon.Question,
            "Confirm Reset",
            "Reset all plot customizations to defaults?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            self,
        )
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        msg.setStyleSheet(
            "QPushButton { border: 1px solid #888; border-radius: 3px; "
            "padding: 4px 16px; min-width: 60px; }"
            "QPushButton:hover { background-color: #e0e0e0; }"
        )
        reply = msg.exec()
        if reply != QMessageBox.StandardButton.Yes:
            return
        self._reset_font_size(self._title_font_size)
        self._reset_font_size(self._x_font_size)
        self._reset_font_size(self._y_font_size)
        self._reset_font_size(self._legend_font_size)
        self._reset_font_size(self._x_tick_label_size)
        self._reset_font_size(self._y_tick_label_size)
        self._x_tick_marker_size.setValue(8)
        self._y_tick_marker_size.setValue(8)
        self._x_label_edit.clear()
        self._y_label_cache.clear()
        for edit in self._y_label_edits:
            edit.clear()
        self._title_edit.clear()
        for wd in list(self._ref_line_widgets):
            self._remove_reference_line(wd)
        self._per_line_widgets.clear()
        self._replace_per_line_container(QLabel("Plot data to configure per-line styles"))
        self.customization_reset.emit()
        self._schedule_change()

```
