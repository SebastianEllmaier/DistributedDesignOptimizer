# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Topology analysis handler — orchestrates analysis and emits results.

Static analyses delegate to _static_graph_builder.
Dynamic analyses delegate to _dynamic_builder.
"""

import logging
from collections import deque

import networkx as nx

from PySide6.QtCore import QObject, Signal

from ..models.AnalysisConfig import AnalysisConfig
from ..workers.TopologyWorker import TopologyWorker
from ._topology_dispatch import resolve as _resolve_topology

logger = logging.getLogger(__name__)


class TopologyHandler(QObject):
    """Runs topology analyses and produces native rendering data."""

    graph_ready = Signal(dict, str, dict)
    chart_ready = Signal(object, str, dict)
    html_ready = Signal(str, str, dict)
    analysis_error = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        """Initialize the topology handler.

        Args:
            parent: Optional parent QObject for Qt ownership.
        """
        super().__init__(parent)
        self._worker: TopologyWorker | None = None

    def run_analysis(self, dill_data: deque, config: AnalysisConfig, filename: str) -> None:
        """Run the specified topology analysis in a background thread.

        Args:
            dill_data: Deque of iteration data loaded from a dill history file.
            config: Analysis configuration specifying type and mode.
            filename: Name of the source dill file for labeling.
        """
        try:
            analysis = config.analysis_type
            mode = config.mode
            context_data = self._extract_context(analysis, mode, dill_data)
            context_data["filename"] = filename
            label = f"{analysis}_{mode}"

            build_fn, output_type = _resolve_topology(analysis, mode)
            args = (dill_data, analysis, filename)

            self.cancel()

            self._worker = TopologyWorker(build_fn, args, label, context_data, output_type)
            self._worker.graph_ready.connect(self.graph_ready.emit)
            self._worker.chart_ready.connect(self.chart_ready.emit)
            self._worker.html_ready.connect(self.html_ready.emit)
            self._worker.error.connect(self.analysis_error.emit)
            self._worker.start()
        except Exception as e:
            logger.error(f"Topology analysis setup failed: {e}", exc_info=True)
            self.analysis_error.emit(str(e))

    def cancel(self) -> None:
        """Cancel any running topology analysis worker."""
        if self._worker is not None and self._worker.isRunning():
            self._worker.requestInterruption()
            self._worker.wait(2000)
        self._worker = None

    def validate_coordinator_file(self, metadata: dict) -> bool:
        """Check if the entry is a coordinator-type dill file.

        Args:
            metadata: File metadata dictionary from the file registry.

        Returns:
            True if the file is a coordinator dill file, False otherwise.
        """
        return metadata.get("is_coordinator", False)

    def _extract_context(self, analysis_type: str, mode: str, dill_data: deque) -> dict:
        """Build a context summary dict for the ChatHandler."""
        context: dict = {
            "analysis_type": analysis_type,
            "mode": mode,
            "n_iterations": len(dill_data),
        }
        if dill_data:
            last = dill_data[-1] if isinstance(dill_data, (deque, list)) else dill_data
            if isinstance(last, dict):
                master = last.get("MasterGraph")
                if master is not None:
                    if isinstance(master, (nx.Graph, nx.DiGraph, nx.MultiDiGraph)):
                        context["n_nodes"] = master.number_of_nodes()
                        context["n_edges"] = master.number_of_edges()
                cluster = last.get("ClusterAnalysis")
                if cluster:
                    context["cluster_info"] = str(cluster)[:500]
                centrality = last.get("CentralityMeasures")
                if centrality:
                    context["centrality_info"] = str(centrality)[:500]
        return context
