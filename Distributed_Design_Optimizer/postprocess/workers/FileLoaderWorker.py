# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Background worker for loading .dill history files."""

import logging

from PySide6.QtCore import QObject, QThread, Signal

from ..models.DataSource import DataSource

logger = logging.getLogger(__name__)


class FileLoaderWorker(QThread):
    """Background worker that loads .dill files without blocking the UI."""

    file_loaded = Signal(str, dict)    # (entry_id, tree_structure)
    progress = Signal(int, int)        # (current_index, total_count)
    file_error = Signal(str, str)      # (filename, error_message)

    def __init__(self, source: DataSource, file_paths: list[str], parent: QObject | None = None) -> None:
        """Initialize the file loader worker.

        Args:
            source: The data source that handles deserialization.
            file_paths: List of file paths to load.
            parent: Optional parent QObject.
        """
        super().__init__(parent)
        self._source = source
        self._file_paths = file_paths

    def run(self) -> None:
        """Load each file, emitting progress and results as signals."""
        total = len(self._file_paths)
        for i, path in enumerate(self._file_paths):
            if self.isInterruptionRequested():
                break
            try:
                entry_id = self._source.load_entry(path)
                tree_structure = self._source.get_tree_structure(entry_id)
                self.file_loaded.emit(entry_id, tree_structure)
            except Exception as e:
                logger.error(f"Failed to load {path}: {e}")
                self.file_error.emit(path, str(e))
            self.progress.emit(i + 1, total)
