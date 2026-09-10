---
title: MainWindow (Source)
---

← Back to [MainWindow documentation](MainWindow.md)

# MainWindow - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\widgets\MainWindow.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Main application window for the DDO Viewer."""
import logging

from PySide6.QtWidgets import (
    QMainWindow, QDockWidget, QTabWidget, QTabBar,
    QStatusBar, QMessageBox, QWidget, QSizePolicy, QApplication,
    QLabel, QProgressBar, QStyle, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QFrame, QComboBox,
)
from PySide6.QtCore import Qt, QSettings, QTimer
from PySide6.QtGui import QAction, QCloseEvent

from ..styles.Theme import get_accent_color, PRIMARY, PRIMARY_LIGHT, SECONDARY, PRIMARY_DARK
from ..handlers.DataHandler import DataHandler
from ..handlers.PlotHandler import PlotHandler
from ..handlers.TopologyHandler import TopologyHandler
from ..handlers.ChatHandler import ChatHandler
from .DataSelectionPanel import DataSelectionPanel
from .PlotCanvas import PlotCanvas
from .TopologyPanel import TopologyPanel
from .PlotSettingsPanel import PlotSettingsPanel
from .ChatPanel import ChatPanel
from .TopologyControlsWidget import TopologyControlsWidget
from ._auto_update_delegate import AutoUpdateDelegate
from ._topology_delegate import TopologyDelegate

logger = logging.getLogger(__name__)

# Workflow stage indices
_TAB_DATA = 0
_TAB_VIS = 1
_TAB_SETTINGS = 2
_TAB_CHAT = 3

_STEP_COUNT = 4

# Activity-bar button stylesheet templates
_ACTIVITY_BTN_STYLE = (
    "QPushButton {{"
    "  background: transparent; border: none; color: #666;"
    "  font-size: 9pt; padding: 10px 4px;"
    "  border-left: 3px solid transparent;"
    "}}"
    "QPushButton:checked {{"
    "  background-color: #f0f0f0; color: {primary};"
    "  font-weight: bold; border-left: 3px solid {primary};"
    "}}"
    "QPushButton:disabled {{"
    "  color: #c0c0c0;"
    "}}"
    "QPushButton:hover:!disabled:!checked {{"
    "  background-color: #e8e8e8;"
    "}}"
).format(primary=PRIMARY)


class MainWindow(QMainWindow):
    """Top-level application window.

    Layout:
        Left dock  — action bar + QTabWidget with Data / Settings / AI Chat tabs
        Central    — QTabWidget with Plot / Topology (with embedded controls)
    """

    def __init__(self, llm_config: dict | None = None) -> None:
        """Initialize the main window and all child widgets.

        Args:
            llm_config: Optional LLM configuration dict for the AI chat handler.
        """
        super().__init__()
        self.setWindowTitle("DDO Viewer — Distributed Optimization Processing")
        self.setMinimumSize(1000, 700)
        self.resize(1400, 900)

        self._settings = QSettings("DDO", "DDOViewer")

        # --- Create handlers ---
        self._data_handler = DataHandler(self)
        self._plot_handler = PlotHandler(self)
        self._topology_handler = TopologyHandler(self)
        self._chat_handler = ChatHandler(llm_config or {}, self)

        # --- Delegates (initialized after layout setup) ---
        self._auto_update_delegate: AutoUpdateDelegate | None = None
        self._topology_delegate: TopologyDelegate | None = None

        # --- Create widgets ---
        self._data_panel = DataSelectionPanel()
        self._data_panel.set_data_handler(self._data_handler)
        self._plot_canvas = PlotCanvas()
        self._topology_panel = TopologyPanel()
        self._settings_panel = PlotSettingsPanel()
        self._chat_panel = ChatPanel()

        # Track workflow state
        self._vis_type: str | None = None  # "lineplot" or "topology"
        self._has_visualization = False     # True once a plot/topology is generated

        # --- Settings stack: placeholder / plot settings / topology controls ---
        self._settings_placeholder = QWidget()
        ph_layout = QVBoxLayout(self._settings_placeholder)
        ph_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ph_icon = QLabel()
        ph_icon.setPixmap(
            self.style()
            .standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)
            .pixmap(48, 48)
        )
        ph_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ph_layout.addWidget(ph_icon)
        ph_title = QLabel("Settings")
        ph_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ph_title.setStyleSheet("font-size: 13pt; font-weight: bold;")
        ph_layout.addWidget(ph_title)
        ph_sub = QLabel(
            "Select a visualization type first,\n"
            "then configure its settings here."
        )
        ph_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ph_sub.setStyleSheet("color: gray; font-size: 10pt;")
        ph_layout.addWidget(ph_sub)

        self._settings_stack = QStackedWidget()
        self._settings_stack.addWidget(self._settings_placeholder)  # page 0: placeholder
        self._settings_stack.addWidget(self._settings_panel)         # page 1: plot settings
        self._topology_controls = TopologyControlsWidget()
        self._topology_controls.launch_requested.connect(
            self._topology_panel.topology_launch_requested.emit
        )
        self._settings_stack.addWidget(self._topology_controls)      # page 2: topology controls
        self._settings_stack.setCurrentIndex(0)

        # --- Visualization chooser widget ---
        self._vis_chooser = self._create_vis_chooser()

        # --- Assemble layout ---
        self._setup_central_widget()
        self._setup_left_dock()
        self._setup_status_bar()

        # --- Wire signals ---
        self._connect_signals()

        # --- Restore layout state ---
        self._restore_state()

    # ==================================================================
    # Layout Setup
    # ==================================================================

    def _create_vis_chooser(self) -> QWidget:
        """Build the Visualization chooser panel with LinePlot / Topology segmented control."""
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        title = QLabel("Choose Visualization Type")
        title.setStyleSheet("font-size: 13pt; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        desc = QLabel("Select how you want to visualize the loaded data.")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("color: gray; font-size: 10pt;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        layout.addSpacing(8)

        # Dropdown: Line Plot / Topology
        self._vis_segment = QComboBox()
        self._vis_segment.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self._vis_segment.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self._vis_segment.addItems(["Line Plot", "Topology"])
        self._vis_segment.activated.connect(self._on_vis_segment_changed)
        layout.addWidget(self._vis_segment)

        layout.addSpacing(16)

        self._clear_graph_btn = QPushButton("Clear Graph")
        self._clear_graph_btn.setMinimumHeight(36)
        self._clear_graph_btn.setStyleSheet(
            f"QPushButton {{ background-color: #cc4444; color: white; "
            f"font-weight: bold; padding: 5px 12px; border-radius: 3px; }}"
            f"QPushButton:hover {{ background-color: #aa3333; }}"
            f"QPushButton:disabled {{ background-color: #cccccc; color: #888888; }}"
        )
        self._clear_graph_btn.setToolTip("Clear the current visualization")
        self._clear_graph_btn.setEnabled(False)
        layout.addWidget(self._clear_graph_btn)

        layout.addStretch()
        return w

    def _on_vis_segment_changed(self, index: int | None) -> None:
        """Handle segmented control selection."""
        if index is None:
            return
        if index == 0:
            self._on_vis_chosen("lineplot")
        elif index == 1:
            self._on_vis_chosen("topology")

    def _setup_central_widget(self) -> None:
        """Central area: stacked widget with Line Plot and Topology views."""
        self._central_stack = QStackedWidget()
        self._central_stack.addWidget(self._plot_canvas)     # page 0: line plot
        self._central_stack.addWidget(self._topology_panel)  # page 1: topology
        self._central_stack.setCurrentIndex(0)
        self.setCentralWidget(self._central_stack)

    def _setup_left_dock(self) -> None:
        """Left dock with VS Code-style vertical activity bar + stacked panels."""
        # Create actions (used by auto-update delegate)
        self._auto_update_action = QAction("Auto-Update", self)
        self._auto_update_action.setCheckable(True)
        self._auto_update_action.setToolTip("Enable automatic file-change detection")

        self._refresh_action = QAction("Refresh", self)
        self._refresh_action.setToolTip("Check for file changes and replot")

        # Dock content: horizontal layout = activity bar | panel stack
        dock_content = QWidget()
        dock_h_layout = QHBoxLayout(dock_content)
        dock_h_layout.setContentsMargins(0, 0, 0, 0)
        dock_h_layout.setSpacing(0)

        # --- Activity bar (narrow vertical column) ---
        activity_bar = QWidget()
        activity_bar.setStyleSheet(
            "background-color: #f5f5f5; border-right: 1px solid #ddd;"
        )
        ab_layout = QVBoxLayout(activity_bar)
        ab_layout.setContentsMargins(0, 4, 0, 4)
        ab_layout.setSpacing(0)

        # Build activity buttons: emoji + text in a single QPushButton
        self._activity_btns: list[QPushButton] = []
        btn_defs = [
            ("\U0001F4C2\nData", "Load and manage .dill history files"),
            ("\U0001F4CA\nVisualization", "Choose visualization type"),
            ("\U0001F527\nSettings", "Configure plot settings"),
            ("\U0001F916\nAI Chat", "Ask questions about the visualization"),
        ]
        for i, (text, tooltip) in enumerate(btn_defs):
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setToolTip(tooltip)
            btn.setStyleSheet(
                "QPushButton {"
                "  background: transparent; border: none;"
                "  border-left: 3px solid transparent;"
                "  padding: 10px 6px; color: #555;"
                "}"
                "QPushButton:checked {"
                f"  background-color: white; border-left: 3px solid {PRIMARY};"
                f"  color: {PRIMARY}; font-weight: bold;"
                "}"
                "QPushButton:hover:!disabled:!checked {"
                "  background-color: #e8e8e8;"
                "}"
                "QPushButton:disabled {"
                "  color: #ccc;"
                "}"
            )
            btn.clicked.connect(lambda checked, idx=i: self._on_activity_btn_clicked(idx))
            ab_layout.addWidget(btn)
            self._activity_btns.append(btn)

        # Down-arrow connectors between buttons
        for i in range(len(self._activity_btns) - 1):
            arrow = QLabel("▾")
            arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
            arrow.setStyleSheet(f"color: {PRIMARY_LIGHT}; font-size: 16pt;")
            # Insert arrow after button i — layout index = button_index + arrows_before + 1
            ab_layout.insertWidget(ab_layout.indexOf(self._activity_btns[i]) + 1, arrow)

        ab_layout.addStretch()

        # Compute fixed width: measure widest label in bold + padding
        from PySide6.QtGui import QFontMetrics, QFont as _QFont
        bold_font = self.font()
        bold_font.setBold(True)
        fm_bold = QFontMetrics(bold_font)
        max_text_w = 0
        for text, _tooltip in btn_defs:
            for line in text.split("\n"):
                max_text_w = max(max_text_w, fm_bold.horizontalAdvance(line))
        activity_bar.setFixedWidth(max_text_w + 30)  # padding + border

        dock_h_layout.addWidget(activity_bar)

        # --- Panel stack (content area) ---
        self._panel_stack = QStackedWidget()
        self._panel_stack.addWidget(self._data_panel)      # page 0
        self._panel_stack.addWidget(self._vis_chooser)     # page 1
        self._panel_stack.addWidget(self._settings_stack)  # page 2
        self._panel_stack.addWidget(self._chat_panel)      # page 3
        self._panel_stack.setCurrentIndex(0)

        dock_h_layout.addWidget(self._panel_stack, stretch=1)

        # Select first button
        self._activity_btns[0].setChecked(True)

        # Initially disable panels 1-3
        self._set_tab_enabled(_TAB_VIS, False)
        self._set_tab_enabled(_TAB_SETTINGS, False)
        self._set_tab_enabled(_TAB_CHAT, False)

        # A1: Dock with hidden title bar
        self._left_dock = QDockWidget(self)
        self._left_dock.setObjectName("SidePanel")
        self._left_dock.setWindowTitle("Side Panel")
        self._left_dock.setTitleBarWidget(QWidget())
        self._left_dock.setWidget(dock_content)
        self._left_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )
        self._left_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._left_dock)

    def _setup_menus(self) -> None:
        """No menu bar — all actions are accessible via buttons."""
        # Menu bar intentionally removed per user request.
        pass

    def _setup_status_bar(self) -> None:
        """Status bar: left-aligned info widgets, right-aligned progress bar."""
        self._status_bar = QStatusBar()
        self.setStatusBar(self._status_bar)

        # F2: Left-aligned file count and plot mode (addWidget, not addPermanentWidget)
        self._file_count_label = QLabel("0 files")
        self._file_count_label.setToolTip("Number of loaded history files")
        self._status_bar.addWidget(self._file_count_label)

        self._plot_mode_label = QLabel("")
        self._plot_mode_label.setToolTip("Current Y-axis and X-axis modes")
        self._status_bar.addWidget(self._plot_mode_label)

        # F3: DPI-scaled progress bar (right-aligned)
        fm = self.fontMetrics()
        self._progress_bar = QProgressBar()
        self._progress_bar.setFixedWidth(fm.averageCharWidth() * 20)
        self._progress_bar.setMaximumHeight(fm.height() + 2)
        self._progress_bar.setVisible(False)
        self._status_bar.addPermanentWidget(self._progress_bar)

        self._status_bar.showMessage("Ready")

    # ==================================================================
    # Signal Wiring
    # ==================================================================

    def _connect_signals(self) -> None:
        """Wire all cross-component signals."""
        # Data panel → DataHandler
        self._data_panel.files_load_requested.connect(self._data_handler.load_files)
        # P19: auto-plot when selection changes
        self._data_panel.selection_changed.connect(self._on_selection_changed)
        # Clear All Data button in data panel
        self._data_panel._clear_all_btn.clicked.connect(self._clear_data)

        # DataHandler → Data panel
        self._data_handler.entry_loaded.connect(self._data_panel.populate_tree)
        self._data_handler.loading_error.connect(self._on_loading_error)
        self._data_handler.loading_started.connect(self._on_loading_started)
        self._data_handler.loading_progress.connect(self._on_loading_progress)
        self._data_handler.loading_finished.connect(self._on_loading_finished)
        self._data_handler.data_updated.connect(self._on_data_updated)

        # PlotHandler → PlotCanvas
        self._plot_handler.plot_ready.connect(self._on_plot_ready)
        self._plot_handler.plot_error.connect(self._on_plot_error)

        # Image-save feedback → status bar
        self._plot_canvas.image_saved.connect(
            lambda msg: self._status_bar.showMessage(msg, 5000)
        )
        # Debounced re-plot on canvas resize so aligned-mode x-axis tick labels
        # re-thin to the actual rendered width (not a static estimate).
        self._last_plot_width = 0
        self._resize_replot_timer = QTimer(self)
        self._resize_replot_timer.setSingleShot(True)
        self._resize_replot_timer.setInterval(250)
        self._resize_replot_timer.timeout.connect(self._replot_for_resize)
        self._plot_canvas.resized.connect(
            lambda w, h: self._resize_replot_timer.start()
        )
        self._topology_panel.image_saved.connect(
            lambda msg: self._status_bar.showMessage(msg, 5000)
        )

        # Settings panel — auto-apply (P13)
        self._settings_panel.settings_changed.connect(self._on_settings_changed)
        self._settings_panel.customization_reset.connect(self._plot_handler.clear_customization)

        # Topology — delegate handles launch + result dispatch
        self._topology_delegate = TopologyDelegate(
            self._data_handler, self._topology_handler, self._chat_handler,
            self._topology_panel, self._chat_panel, self._central_stack,
            self._status_bar, self,
        )
        self._topology_delegate.analysis_complete.connect(self._on_topology_complete)
        self._topology_panel.topology_launch_requested.connect(self._topology_delegate.on_launch)
        self._topology_handler.graph_ready.connect(self._topology_delegate.on_graph_ready)
        self._topology_handler.chart_ready.connect(self._topology_delegate.on_chart_ready)
        self._topology_handler.html_ready.connect(self._topology_delegate.on_html_ready)
        self._topology_handler.analysis_error.connect(self._topology_delegate.on_error)

        # Chat
        self._chat_panel.message_sent.connect(self._chat_handler.ask)
        self._chat_handler.response_ready.connect(self._chat_panel.show_response)
        self._chat_handler.error.connect(lambda msg: self._chat_panel.show_response(f"Error: {msg}"))
        self._chat_panel.set_llm_available(self._chat_handler.is_available)

        # Wire data-panel action buttons
        self._clear_graph_btn.clicked.connect(self._clear_graph)
        self._data_panel._auto_update_btn.toggled.connect(self._auto_update_action.setChecked)
        self._auto_update_action.toggled.connect(self._data_panel._auto_update_btn.setChecked)
        self._data_panel._refresh_btn.clicked.connect(self._refresh_action.trigger)

        # Auto-update delegate
        self._auto_update_delegate = AutoUpdateDelegate(
            self._data_handler, self._auto_update_action,
            self._status_bar, parent=self,
        )
        self._auto_update_action.toggled.connect(self._auto_update_delegate.on_toggled)
        self._refresh_action.triggered.connect(self._auto_update_delegate.manual_update)

    # ==================================================================
    # Slot Implementations
    # ==================================================================

    def _set_tab_enabled(self, index: int, enabled: bool) -> None:
        """Enable or disable an activity-bar button."""
        btn = self._activity_btns[index]
        btn.setEnabled(enabled)
        if not enabled and btn.isChecked():
            # Fall back to Data panel
            self._on_activity_btn_clicked(_TAB_DATA)

    def _on_activity_btn_clicked(self, index: int) -> None:
        """Switch the panel stack to the clicked activity button."""
        if not self._activity_btns[index].isEnabled():
            return
        if index == _TAB_CHAT:
            QMessageBox.information(
                self, "AI Chat",
                "The AI Chat feature is currently not implemented.\n"
                "This functionality will be available in a future release."
            )
            return
        for i, btn in enumerate(self._activity_btns):
            btn.setChecked(i == index)
        self._panel_stack.setCurrentIndex(index)

    def _switch_to_panel(self, index: int) -> None:
        """Programmatically switch to a panel by index."""
        self._on_activity_btn_clicked(index)

    def _on_vis_chosen(self, vis_type: str) -> None:
        """Handle visualization type selection from the chooser panel."""
        if vis_type == "topology":
            QMessageBox.information(
                self, "Topology Visualization",
                "The Topology visualization feature is currently not available.\n"
                "Please select Line Plot instead."
            )
            # Reset segmented control back to Line Plot
            self._vis_segment.blockSignals(True)
            self._vis_segment.setCurrentIndex(0)
            self._vis_segment.blockSignals(False)
            return

        # Line Plot chosen
        self._vis_type = vis_type
        self._central_stack.setCurrentIndex(0)  # show plot canvas
        self._settings_stack.setCurrentIndex(1)  # show plot settings
        self._set_tab_enabled(_TAB_SETTINGS, True)

        # Check if user already has plottable data selected
        selected = self._data_panel.get_all_item_paths()
        if selected:
            # Trigger plot immediately with existing selection
            self._on_selection_changed(selected)
        else:
            # No data selected yet — guide user to Data panel
            self._switch_to_panel(_TAB_DATA)
            QMessageBox.information(
                self, "Line Plot Selected",
                "Please select plottable quantities from the data tree\n"
                "and add them to the selection list to generate a plot."
            )

    def _on_selection_changed(self, item_paths: list[str]) -> None:
        """P19: Auto-plot when selection changes. Update status bar."""
        n = len(item_paths)
        self._status_bar.showMessage(f"{n} item{'s' if n != 1 else ''} in selection list.")

        # Only auto-plot if a visualization type has been chosen
        if not self._vis_type:
            return

        if not item_paths:
            # All items removed — clear the plot
            if self._has_visualization:
                self._clear_graph()
            return

        # Auto-plot
        config = self._settings_panel.get_plot_config()
        plottable_data = self._data_handler.get_plottable_data(item_paths)
        if not plottable_data:
            return
        labels_map = self._data_handler.get_iteration_labels_map(item_paths)
        self._sync_canvas_size()
        self._plot_handler.create_plot(plottable_data, config, labels_map)

    def _on_plot_ready(self, html: str) -> None:
        """Display the new plot HTML and refresh line entry controls."""
        # Switch central stack first so the web view surface is visible
        # before the deferred HTML injection
        self._central_stack.setCurrentWidget(self._plot_canvas)
        QApplication.processEvents()  # Let compositor initialize the surface
        self._plot_canvas.set_html(html, self._plot_handler.last_figure)
        # Rebuild per-line/legend widgets when data items or ref lines change
        new_keys = [p for p, _ in (self._plot_handler.last_plottable_data or [])]
        old_keys = list(self._settings_panel._legend_entries.keys())
        has_ref_lines = any(
            w["enabled"].isChecked()
            for w in self._settings_panel._ref_line_widgets
        )
        # Always rebuild when ref lines are active to keep labels in sync
        if new_keys != old_keys or has_ref_lines:
            self._settings_panel.refresh_line_entries(self._plot_handler.last_plottable_data)
        # Update permanent status bar label
        config = self._settings_panel.get_plot_config()
        self._plot_mode_label.setText(f"Y: {config.plot_type}  |  X: {config.x_axis_type}")
        self._status_bar.showMessage("Plot updated.")
        # Unlock AI Chat once a visualization is generated
        if not self._has_visualization:
            self._has_visualization = True
            self._set_tab_enabled(_TAB_CHAT, True)
            self._clear_graph_btn.setEnabled(True)

    def _sync_canvas_size(self) -> None:
        size = self._plot_canvas.size()
        width = max(400, size.width())
        self._plot_handler.set_canvas_size(width, max(300, size.height()))
        self._last_plot_width = width

    def _replot_for_resize(self) -> None:
        """Re-plot after a resize so aligned-mode tick labels re-thin to width.

        Only aligned x-axis modes compute tick-label density server-side, so
        other modes (handled by Plotly's responsive rescaling) are skipped.
        A minimum width delta avoids redundant re-plots during small drags.
        """
        if not self._plot_handler.last_plottable_data:
            return
        config = self._settings_panel.get_plot_config()
        if config.x_axis_type not in ("combined_ticks", "equispaced_major"):
            return
        new_width = max(400, self._plot_canvas.size().width())
        if abs(new_width - self._last_plot_width) < 40:
            return
        labels_map = self._plot_handler.last_labels_map
        item_paths = self._data_panel.get_all_item_paths()
        if item_paths:
            labels_map = self._data_handler.get_iteration_labels_map(item_paths)
        self._sync_canvas_size()
        self._plot_handler.create_plot(
            self._plot_handler.last_plottable_data, config, labels_map,
        )

    def _on_plot_error(self, message: str) -> None:
        self._status_bar.showMessage(f"Plot error: {message}")
        QMessageBox.warning(self, "Plot Error", message)

    def _on_topology_complete(self, analysis_type: str) -> None:
        """Handle topology delegate signalling analysis is done."""
        self._has_visualization = True
        self._set_tab_enabled(_TAB_CHAT, True)
        self._switch_to_panel(_TAB_CHAT)

    def _on_settings_changed(self) -> None:
        """Auto-apply: re-plot when ANY setting changes (P13)."""
        if self._plot_handler.last_plottable_data:
            config = self._settings_panel.get_plot_config()
            labels_map = self._plot_handler.last_labels_map
            if config.x_axis_type in ("cumulative_runtime", "cumulative_evaluations",
                                       "combined_ticks", "equispaced_major"):
                item_paths = self._data_panel.get_all_item_paths()
                if item_paths:
                    labels_map = self._data_handler.get_iteration_labels_map(item_paths)
            self._sync_canvas_size()
            self._plot_handler.create_plot(
                self._plot_handler.last_plottable_data, config, labels_map,
            )



    def _on_loading_error(self, filename: str, message: str) -> None:
        self._status_bar.showMessage(f"Error loading {filename}: {message}")

    def _on_loading_started(self, total: int) -> None:
        self._progress_bar.setRange(0, total)
        self._progress_bar.setValue(0)
        self._progress_bar.setVisible(True)
        self._status_bar.showMessage(f"Loading {total} file(s)...")

    def _on_loading_progress(self, current: int, total: int) -> None:
        self._progress_bar.setValue(current)
        self._status_bar.showMessage(f"Loading file {current}/{total}...")

    def _on_loading_finished(self) -> None:
        self._progress_bar.setVisible(False)
        n_entries = len(self._data_handler.list_entries())
        self._file_count_label.setText(f"{n_entries} file{'s' if n_entries != 1 else ''}")
        # Unlock Visualization tab after data is loaded
        if n_entries > 0:
            self._set_tab_enabled(_TAB_VIS, True)
            self._data_panel._clear_all_btn.setEnabled(True)
            self._data_panel._auto_update_btn.setEnabled(True)
            self._data_panel._refresh_btn_base_enabled = True
            self._data_panel._refresh_btn.setEnabled(
                not self._data_panel._auto_update_btn.isChecked()
            )
            self._data_panel._hide_nonplottable_cb.setEnabled(True)
        self._status_bar.showMessage("All files loaded.")

    def _on_data_updated(self, entry_ids: list[str]) -> None:
        """Auto-update detected changes — replot if selections exist."""
        item_paths = self._data_panel.get_all_item_paths()
        if item_paths and self._plot_handler.last_plottable_data:
            config = self._settings_panel.get_plot_config()
            plottable_data = self._data_handler.get_plottable_data(item_paths)
            labels_map = self._data_handler.get_iteration_labels_map(item_paths)
            self._sync_canvas_size()
            self._plot_handler.create_plot(plottable_data, config, labels_map)
            self._status_bar.showMessage(f"Auto-update: {len(entry_ids)} file(s) changed, replotted.")
        else:
            self._status_bar.showMessage(f"Auto-update: {len(entry_ids)} file(s) changed.")



    # ------------------------------------------------------------------
    # Utility actions
    # ------------------------------------------------------------------

    def _clear_graph(self) -> None:
        """Clear the current visualization without removing loaded data."""
        self._plot_canvas.clear()
        self._plot_handler.clear()
        self._plot_mode_label.setText("")
        self._has_visualization = False
        self._clear_graph_btn.setEnabled(False)
        self._set_tab_enabled(_TAB_CHAT, False)
        self._status_bar.showMessage("Graph cleared.")

    def _clear_data(self) -> None:
        self._data_handler.clear_all()
        self._data_panel.clear_tree()
        self._plot_canvas.clear()
        self._topology_panel.clear()
        self._plot_handler.clear()
        self._file_count_label.setText("0 files")
        self._plot_mode_label.setText("")
        # Reset workflow state
        self._vis_type = None
        self._has_visualization = False
        self._set_tab_enabled(_TAB_VIS, False)
        self._set_tab_enabled(_TAB_SETTINGS, False)
        self._set_tab_enabled(_TAB_CHAT, False)
        self._settings_stack.setCurrentIndex(0)
        self._switch_to_panel(_TAB_DATA)
        # Reset button states
        self._data_panel._clear_all_btn.setEnabled(False)
        self._data_panel._auto_update_btn.setEnabled(False)
        self._data_panel._refresh_btn_base_enabled = False
        self._data_panel._refresh_btn.setEnabled(False)
        self._data_panel._hide_nonplottable_cb.setEnabled(False)
        self._clear_graph_btn.setEnabled(False)
        # Reset vis segment (no signal)
        self._vis_segment.blockSignals(True)
        self._vis_segment.setCurrentIndex(0)
        self._vis_segment.blockSignals(False)
        self._status_bar.showMessage("All data cleared.")

    def _show_about(self) -> None:
        QMessageBox.about(
            self, "About DDO Viewer",
            "DDO Viewer — Distributed Optimization Processing\n\n"
            "PySide6-based visualization tool for distributed design optimization results.\n"
            "Supports .dill files with future PostgreSQL backend."
        )

    # ------------------------------------------------------------------
    # State persistence
    # ------------------------------------------------------------------

    def closeEvent(self, event: QCloseEvent) -> None:
        """Persist window state and cancel background tasks before closing.

        Args:
            event: The close event.
        """
        if self._auto_update_delegate:
            self._auto_update_delegate.stop()
        self._topology_handler.cancel()
        self._chat_handler.cancel()
        self._data_handler.cancel()
        self._settings.setValue("chat_history", self._chat_panel.get_history_html())
        self._settings.setValue("geometry", self.saveGeometry())
        self._settings.setValue("windowState", self.saveState())
        super().closeEvent(event)

    def _restore_state(self) -> None:
        geometry = self._settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        state = self._settings.value("windowState")
        if state:
            self.restoreState(state)
        chat_html = self._settings.value("chat_history", "")
        if chat_html:
            self._chat_panel.restore_history(chat_html)

```
