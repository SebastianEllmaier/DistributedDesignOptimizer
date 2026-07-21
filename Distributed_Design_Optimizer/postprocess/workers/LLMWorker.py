# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Background worker for asynchronous LLM API calls."""

import logging
from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QObject, Signal

from .CallableWorker import CallableWorker

logger = logging.getLogger(__name__)


class LLMWorker(CallableWorker):
    """Background worker for LLM API calls."""

    response_ready = Signal(str)

    def __init__(self, call_fn: Callable[..., Any], messages: list[dict], config: dict, parent: QObject | None = None) -> None:
        """Initialize the LLM worker.

        Args:
            call_fn: Callable that performs the LLM API request.
            messages: Chat message history to send.
            config: LLM configuration parameters.
            parent: Optional parent QObject.
        """
        super().__init__(call_fn, (messages, config), parent)

    def _handle_result(self, response_data) -> None:
        choices = response_data.get("choices", [])
        if not choices:
            self.error.emit("LLM returned empty response (no choices).")
            return
        ai_response = choices[0].get("message", {}).get("content", "")
        if not ai_response:
            self.error.emit("LLM response contained no content.")
            return
        self.response_ready.emit(ai_response)
