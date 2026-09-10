# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Background worker for topology analysis computations."""

import logging

from PySide6.QtCore import Signal

from .CallableWorker import CallableWorker

logger = logging.getLogger(__name__)


class TopologyWorker(CallableWorker):
    """Background worker for topology analysis computation."""

    graph_ready = Signal(dict, str, dict)      # (graph_data, label, context_data)
    chart_ready = Signal(object, str, dict)    # (Figure, label, context_data)
    html_ready = Signal(str, str, dict)        # (html_string, label, context_data)

    def __init__(self, build_fn, args: tuple, label: str,
                 context_data: dict, output_type: str = "graph", parent=None) -> None:
        """Initialize the topology worker.

        Args:
            build_fn: Callable that produces the topology result.
            args: Positional arguments for the build function.
            label: Display label for the result.
            context_data: Additional context passed through to signals.
            output_type: Result kind - ``"graph"``, ``"chart"``, or ``"html"``.
            parent: Optional parent QObject.
        """
        super().__init__(build_fn, args, parent)
        self._label = label
        self._context_data = context_data
        self._output_type = output_type  # "graph" | "chart" | "html"

    def _handle_result(self, result) -> None:
        if self._output_type == "html":
            self.html_ready.emit(result, self._label, self._context_data)
        elif self._output_type == "chart":
            self.chart_ready.emit(result, self._label, self._context_data)
        else:
            self.graph_ready.emit(result, self._label, self._context_data)
