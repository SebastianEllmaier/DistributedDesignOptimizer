# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Background worker for periodic file-modification checks."""

import logging

from PySide6.QtCore import QObject, QThread, Signal

from ..models.DataSource import DataSource

logger = logging.getLogger(__name__)


class AutoUpdateWorker(QThread):
    """Periodically checks the data source for file modifications."""

    updates_detected = Signal(list)   # [entry_ids that changed]
    check_complete = Signal()         # emitted each cycle (no changes)

    def __init__(self, source: DataSource, interval_ms: int = 30000, parent: QObject | None = None) -> None:
        """Initialize the auto-update worker.

        Args:
            source: The data source to monitor for changes.
            interval_ms: Polling interval in milliseconds.
            parent: Optional parent QObject.
        """
        super().__init__(parent)
        self._source = source
        self._interval_ms = interval_ms

    def run(self) -> None:
        """Poll the data source for updates at the configured interval."""
        while not self.isInterruptionRequested():
            try:
                changed = self._source.check_for_updates()
                updated_entries = [eid for eid, has_changed in changed.items() if has_changed]
                if updated_entries:
                    self.updates_detected.emit(updated_entries)
                else:
                    self.check_complete.emit()
            except Exception as e:
                logger.error(f"Auto-update check failed: {e}")
            self.msleep(self._interval_ms)

    def stop(self) -> None:
        """Request graceful stop."""
        self.requestInterruption()
