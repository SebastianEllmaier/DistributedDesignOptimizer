---
title: CallableWorker (Source)
---

← Back to [CallableWorker documentation](CallableWorker.md)

# CallableWorker - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\workers\CallableWorker.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Base class for simple background workers that run a callable and emit results."""

import logging

from PySide6.QtCore import QObject, QThread, Signal

logger = logging.getLogger(__name__)


class CallableWorker(QThread):
    """Generic background worker that invokes a callable and emits the result.

    Subclasses override `_handle_result` to route the return value
    to their typed signals.
    """

    error = Signal(str)

    def __init__(self, fn, args: tuple = (), parent: QObject | None = None) -> None:
        """Initialize the callable worker.

        Args:
            fn: The callable to execute in the background thread.
            args: Positional arguments to pass to the callable.
            parent: Optional parent QObject.
        """
        super().__init__(parent)
        self._fn = fn
        self._args = args

    def run(self) -> None:
        """Execute the callable and route the result or emit an error."""
        try:
            result = self._fn(*self._args)
            self._handle_result(result)
        except Exception as e:
            logger.error(f"{type(self).__name__} failed: {e}", exc_info=True)
            self.error.emit(str(e))

    def _handle_result(self, result) -> None:
        """Route the result to the appropriate signal. Override in subclasses."""
        raise NotImplementedError

```
