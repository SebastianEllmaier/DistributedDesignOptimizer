---
title: _auto_update_delegate (Source)
---

← Back to [_auto_update_delegate documentation](_auto_update_delegate.md)

# _auto_update_delegate - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\widgets\_auto_update_delegate.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Delegate handling auto-update lifecycle for MainWindow."""

from PySide6.QtWidgets import QStatusBar
from PySide6.QtCore import QObject
from PySide6.QtGui import QAction

from ..handlers.DataHandler import DataHandler
from ..workers.AutoUpdateWorker import AutoUpdateWorker


class AutoUpdateDelegate(QObject):
    """Manages auto-update worker lifecycle."""

    def __init__(self, data_handler: DataHandler, auto_update_action: QAction,
                 status_bar: QStatusBar,
                 parent: QObject | None = None) -> None:
        """Initialize the auto-update delegate.

        Args:
            data_handler: Handler providing access to loaded data entries.
            auto_update_action: The toggle action controlling auto-update.
            status_bar: Status bar for displaying update messages.
            parent: Optional parent QObject.
        """
        super().__init__(parent)
        self._data_handler = data_handler
        self._auto_update_action = auto_update_action
        self._status_bar = status_bar
        self._worker: AutoUpdateWorker | None = None

    @property
    def worker(self) -> AutoUpdateWorker | None:
        """Return the active auto-update worker, or None if not running.

        Returns:
            The active worker instance, or None if auto-update is stopped.
        """
        return self._worker

    def on_toggled(self, enabled: bool) -> None:
        """Handle auto-update action toggled.

        Args:
            enabled: Whether auto-update is being enabled or disabled.
        """
        if enabled:
            if not self._data_handler.list_entries():
                self._auto_update_action.setChecked(False)
                self._status_bar.showMessage("Auto-update: load files first.")
                return
            self._worker = AutoUpdateWorker(self._data_handler.source)
            self._worker.updates_detected.connect(self._on_detected)
            self._worker.start()
            self._status_bar.showMessage("Auto-update: ON")
        else:
            if self._worker:
                self._worker.stop()
                self._worker.wait(2000)
                self._worker = None
            self._status_bar.showMessage("Auto-update: OFF")

    def _on_detected(self, entry_ids: list[str]) -> None:
        self._data_handler.refresh_data(entry_ids)

    def manual_update(self) -> None:
        """Check for file changes and reload if any."""
        changed = self._data_handler.check_for_updates()
        updated = [eid for eid, c in changed.items() if c]
        if updated:
            self._status_bar.showMessage(f"Updating {len(updated)} file(s)...")
            from PySide6.QtWidgets import QApplication
            QApplication.processEvents()  # show message before blocking reload
            self._data_handler.reload_entries(updated)
            self._status_bar.showMessage(f"Manual update: {len(updated)} file(s) reloaded.")
        else:
            self._status_bar.showMessage("Manual update: no changes detected.")

    def stop(self) -> None:
        """Stop worker if running (for cleanup on close)."""
        if self._worker:
            self._worker.stop()
            self._worker.wait(2000)

```
