# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Delegate handling topology result dispatch for MainWindow."""

from PySide6.QtWidgets import QStackedWidget, QStatusBar, QMessageBox, QWidget
from PySide6.QtCore import QObject, Signal

from ..models.AnalysisConfig import AnalysisConfig
from ..handlers.DataHandler import DataHandler
from ..handlers.TopologyHandler import TopologyHandler
from ..handlers.ChatHandler import ChatHandler
from .TopologyPanel import TopologyPanel
from .ChatPanel import ChatPanel


class TopologyDelegate(QObject):
    """Handles topology launch, result dispatch, and error display."""

    analysis_complete = Signal(str)  # emitted with analysis_type after finalization

    def __init__(self, data_handler: DataHandler, topology_handler: TopologyHandler,
                 chat_handler: ChatHandler, topology_panel: TopologyPanel,
                 chat_panel: ChatPanel, central_stack: QStackedWidget,
                 status_bar: QStatusBar,
                 parent: QObject | None = None) -> None:
        """Initialize the topology delegate.

        Args:
            data_handler: Handler for accessing loaded data entries.
            topology_handler: Handler that runs topology analyses.
            chat_handler: Handler for setting AI chat context.
            topology_panel: Panel displaying topology visualizations.
            chat_panel: Panel displaying the AI chat interface.
            central_stack: Stacked widget controlling the main view.
            status_bar: Status bar for displaying messages.
            parent: Optional parent QObject.
        """
        super().__init__(parent)
        self._data_handler = data_handler
        self._topology_handler = topology_handler
        self._chat_handler = chat_handler
        self._topology_panel = topology_panel
        self._chat_panel = chat_panel
        self._central_stack = central_stack
        self._status_bar = status_bar

    def on_launch(self, config: AnalysisConfig) -> None:
        """Launch topology analysis.

        Args:
            config: Configuration specifying the analysis type and mode.
        """
        coordinator_entry = self._data_handler.find_coordinator_entry(
            self._topology_handler.validate_coordinator_file
        )
        if coordinator_entry is None:
            QMessageBox.warning(
                self.parent(), "No Coordinator File",
                "No coordinator .dill file found. Load a coordinator file first."
            )
            return
        config.entry_id = coordinator_entry
        dill_data = self._data_handler.get_all_iterations(coordinator_entry)
        metadata = self._data_handler.get_metadata(coordinator_entry)
        self._topology_handler.run_analysis(dill_data, config, metadata["filename"])

    def on_graph_ready(self, graph_data: dict, analysis_type: str, context_data: dict) -> None:
        """Handle completed graph analysis by displaying results.

        Args:
            graph_data: Dictionary containing the graph structure data.
            analysis_type: The type of topology analysis performed.
            context_data: Additional context metadata for the analysis.
        """
        self._topology_panel.display_graph(graph_data)
        self._finalize(analysis_type, context_data, "graph")

    def on_chart_ready(self, fig_or_html, analysis_type: str, context_data: dict) -> None:
        """Handle completed chart analysis by displaying results.

        Args:
            fig_or_html: A Plotly figure or HTML string to display.
            analysis_type: The type of topology analysis performed.
            context_data: Additional context metadata for the analysis.
        """
        self._topology_panel.display_chart(fig_or_html)
        self._finalize(analysis_type, context_data, "chart")

    def on_html_ready(self, html_content: str, analysis_type: str, context_data: dict) -> None:
        """Handle completed HTML analysis by displaying results.

        Args:
            html_content: The HTML string to render in the panel.
            analysis_type: The type of topology analysis performed.
            context_data: Additional context metadata for the analysis.
        """
        self._topology_panel.display_html(html_content)
        self._finalize(analysis_type, context_data, "interactive")

    def on_error(self, message: str) -> None:
        """Display a critical error dialog for a failed topology analysis.

        Args:
            message: The error message to display.
        """
        QMessageBox.critical(self.parent(), "Topology Error", message)

    def _finalize(self, analysis_type: str, context_data: dict, kind: str) -> None:
        self._central_stack.setCurrentWidget(self._topology_panel)
        self._chat_handler.set_context(analysis_type, context_data)
        filename = context_data.get("filename", "unknown")
        self._chat_panel.set_context(analysis_type, filename)
        self._status_bar.showMessage(f"Topology {kind}: {analysis_type}")
        self.analysis_complete.emit(analysis_type)
        main_window._switch_to_panel(_TAB_CHAT)
