---
title: ChatHandler (Source)
---

← Back to [ChatHandler documentation](ChatHandler.md)

# ChatHandler - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\handlers\ChatHandler.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Handler for LLM-based chat interactions with optimization results."""

import logging
from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QObject, Signal

from ..workers.LLMWorker import LLMWorker

logger = logging.getLogger(__name__)


class ChatHandler(QObject):
    """Manages LLM interaction for analyzing optimization results."""

    response_ready = Signal(str)
    error = Signal(str)

    def __init__(self, config: dict[str, str], parent: QObject | None = None) -> None:
        """Initialize the chat handler.

        Args:
            config: Dictionary containing LLM client credentials.
            parent: Optional parent QObject.
        """
        super().__init__(parent)
        self._config = config
        self._analysis_type: str = ""
        self._context_data: str = ""
        self._history: list[dict] = []
        self._worker: LLMWorker | None = None
        self._last_question: str = ""
        self._call_fn: Callable[..., Any] | None = None

        # Import the LLM call function from existing codebase
        try:
            from Distributed_Design_Optimizer.postprocess.handlers.llm_api import call_llm_api
            from Distributed_Design_Optimizer.postprocess.handlers.system_prompt import SYSTEM_PROMPT
            self._call_fn = call_llm_api
            self._system_prompt = SYSTEM_PROMPT
        except ImportError:
            logger.warning("LLM API module not available. Chat will not function.")
            self._system_prompt = "You are an AI assistant analyzing optimization data."

    @property
    def is_available(self) -> bool:
        """Whether the LLM backend is usable.

        Returns:
            bool: True if the LLM call function is available.
        """
        return self._call_fn is not None

    def set_context(self, analysis_type: str, context_data: dict) -> None:
        """Update the current analysis context and reset conversation history.

        Args:
            analysis_type: The type of analysis being viewed.
            context_data: Dictionary of context information for the LLM.
        """
        self._analysis_type = analysis_type
        self._context_data = self._format_context(analysis_type, context_data)
        self._history.clear()

    def ask(self, question: str) -> None:
        """Send a question to the LLM in a background thread.

        Args:
            question: The user's question to send to the LLM.
        """
        if self._call_fn is None:
            self.error.emit("LLM API not available. Check that llm_api module is installed.")
            return

        # Prevent concurrent requests — cancel previous worker if still running
        if self._worker is not None and self._worker.isRunning():
            self._worker.response_ready.disconnect(self._on_response)
            self._worker.error.disconnect(self._on_error)
            self._worker.requestInterruption()
            self._worker.wait(1000)

        self._last_question = question
        messages = [
            {"role": "system", "content": self._system_prompt},
            {"role": "system", "content": f"The user is currently viewing the following data:\n{self._context_data}"},
        ]
        messages.extend(self._history)
        messages.append({"role": "user", "content": question})

        self._worker = LLMWorker(self._call_fn, messages, self._config)
        self._worker.response_ready.connect(self._on_response)
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self._history.clear()

    def cancel(self) -> None:
        """Stop any running LLM worker."""
        if self._worker is not None and self._worker.isRunning():
            self._worker.requestInterruption()
            self._worker.wait(1000)
        self._worker = None

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _on_response(self, response: str) -> None:
        # Store in history for multi-turn conversation
        if self._last_question:
            self._history.append({"role": "user", "content": self._last_question})
        self._history.append({"role": "assistant", "content": response})
        self.response_ready.emit(response)
        self._worker = None

    def _on_error(self, error_msg: str) -> None:
        self.error.emit(f"LLM Error: {error_msg}")
        self._worker = None

    @staticmethod
    def _format_context(analysis_type: str, data: dict) -> str:
        """Format context data into a readable string for the LLM."""
        lines = [f"Analysis Type: {analysis_type}"]
        context_fields = [
            ("mode", "Mode"),
            ("n_iterations", "Number of iterations"),
            ("n_nodes", "Graph nodes"),
            ("n_edges", "Graph edges"),
            ("cluster_info", "Cluster info"),
            ("centrality_info", "Centrality info"),
        ]
        for key, label in context_fields:
            if key in data:
                lines.append(f"{label}: {data[key]}")
        return "\n".join(lines)

```
