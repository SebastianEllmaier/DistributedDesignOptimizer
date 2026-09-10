# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Handler for loading, caching, and accessing optimization history data."""
import logging

from PySide6.QtCore import QObject, Signal

from ..models.DataSource import DataSource
from ..models.DillDataSource import DillDataSource
from ..workers.FileLoaderWorker import FileLoaderWorker

from collections import deque

logger = logging.getLogger(__name__)


class DataHandler(QObject):
    """Manages data loading, caching, and access through the DataSource abstraction."""

    entry_loaded = Signal(str, dict)       # (entry_id, tree_structure)
    loading_error = Signal(str, str)       # (filename, error_message)
    data_updated = Signal(list)            # [entry_ids that changed]
    loading_started = Signal(int)          # total file count
    loading_progress = Signal(int, int)    # (current, total)
    loading_finished = Signal()            # all files processed

    def __init__(self, parent: QObject | None = None) -> None:
        """Initialize the DataHandler with a default DillDataSource.

        Args:
            parent: Optional parent QObject for Qt ownership.
        """
        super().__init__(parent)
        self._source: DataSource = DillDataSource()
        self._loader_worker: FileLoaderWorker | None = None

    @property
    def source(self) -> DataSource:
        """Return the active data source.

        Returns:
            The currently active DataSource instance.
        """
        return self._source

    def set_source(self, source: DataSource) -> None:
        """Replace the active data source.

        Args:
            source: The new DataSource instance to use.
        """
        self._source.close()
        self._source = source

    def load_files(self, paths: list[str]) -> None:
        """Start background loading of .dill files.

        Args:
            paths: List of file paths to load.
        """
        if not paths:
            return
        self.loading_started.emit(len(paths))
        self._loader_worker = FileLoaderWorker(self._source, paths)
        self._loader_worker.file_loaded.connect(self._on_file_loaded)
        self._loader_worker.file_error.connect(self._on_load_error)
        self._loader_worker.progress.connect(self.loading_progress.emit)
        self._loader_worker.finished.connect(self._on_loading_finished)
        self._loader_worker.start()

    def get_plottable_data(self, item_paths: list[str]) -> list[tuple[str, list[float]]]:
        """Get plot-ready data for a list of item paths.

        item_paths format: "entry_id/dot.separated.path"
        Paths that resolve to all-NaN values (non-numeric data) are excluded.

        Args:
            item_paths: List of paths in "entry_id/dot.separated.path" format.

        Returns:
            List of (full_path, values) tuples for paths with numeric data.
        """
        import math
        result: list[tuple[str, list[float]]] = []
        for full_path in item_paths:
            entry_id, item_path = self._split_path(full_path)
            values = self._source.get_values(entry_id, item_path)
            if values and not all(math.isnan(v) for v in values):
                result.append((full_path, values))
        return result

    def is_path_plottable(self, entry_id: str, item_path: str) -> bool:
        """Check if a leaf path has at least one non-NaN numeric value.

        Args:
            entry_id: Identifier of the loaded data entry.
            item_path: Dot-separated path to a leaf data item.

        Returns:
            True if the path has at least one finite numeric value.
        """
        import math
        values = self._source.get_values(entry_id, item_path)
        return bool(values) and not all(math.isnan(v) for v in values)

    def get_iteration_data(self, entry_id: str, iteration: int) -> dict:
        """Return the raw data dictionary for a specific iteration.

        Args:
            entry_id: Identifier of the loaded data entry.
            iteration: Zero-based iteration index.

        Returns:
            Dictionary of data for the requested iteration.
        """
        return self._source.get_iteration_data(entry_id, iteration)

    def get_all_iterations(self, entry_id: str) -> deque:
        """Return all iteration records for the given entry.

        Args:
            entry_id: Identifier of the loaded data entry.

        Returns:
            Deque of iteration data dictionaries.
        """
        return self._source.get_all_iterations(entry_id)

    def get_metadata(self, entry_id: str) -> dict:
        """Return metadata for the given entry.

        Args:
            entry_id: Identifier of the loaded data entry.

        Returns:
            Dictionary of metadata for the entry.
        """
        return self._source.get_metadata(entry_id)

    def list_entries(self) -> list[str]:
        """Return a list of all loaded entry identifiers.

        Returns:
            List of entry ID strings.
        """
        return self._source.list_entries()

    def get_iteration_labels(self, entry_id: str) -> list[dict]:
        """Return per-iteration outerloop/innerloop metadata for x-axis labeling.

        Args:
            entry_id: Identifier of the loaded data entry.

        Returns:
            List of label dictionaries, one per iteration.
        """
        return self._source.get_iteration_labels(entry_id)

    def get_iteration_labels_map(self, item_paths: list[str]) -> dict[str, list[dict]]:
        """Return {entry_id: labels} for each unique entry referenced by item_paths.

        Args:
            item_paths: List of paths in "entry_id/dot.separated.path" format.

        Returns:
            Mapping of entry IDs to their iteration label lists.
        """
        result: dict[str, list[dict]] = {}
        for full_path in item_paths:
            entry_id = full_path.split("/", 1)[0]
            if entry_id not in result:
                result[entry_id] = self._source.get_iteration_labels(entry_id)
        return result

    def check_for_updates(self) -> dict[str, bool]:
        """Check which loaded entries have been modified on disk.

        Returns:
            Mapping of entry IDs to whether they have changed.
        """
        return self._source.check_for_updates()

    def reload_entries(self, entry_ids: list[str]) -> None:
        """Reload one or more entries from their backing files.

        Args:
            entry_ids: List of entry identifiers to reload.
        """
        for entry_id in entry_ids:
            self._source.reload_entry(entry_id)
            tree = self._source.get_tree_structure(entry_id)
            self.entry_loaded.emit(entry_id, tree)
        if entry_ids:
            self.data_updated.emit(entry_ids)

    def refresh_data(self, entry_ids: list[str]) -> None:
        """Reload data and re-emit tree structure (for auto-update).

        Args:
            entry_ids: List of entry identifiers to refresh.
        """
        for entry_id in entry_ids:
            self._source.reload_entry(entry_id)
            tree = self._source.get_tree_structure(entry_id)
            self.entry_loaded.emit(entry_id, tree)
        if entry_ids:
            self.data_updated.emit(entry_ids)

    def clear_all(self) -> None:
        """Clear all loaded data."""
        self._source.close()

    def remove_entry(self, entry_id: str) -> None:
        """Remove a single entry from loaded data.

        Args:
            entry_id: Identifier of the entry to remove.
        """
        self._source.remove_entry(entry_id)

    def find_coordinator_entry(self, validator) -> str | None:
        """Return the first entry_id whose metadata passes *validator*, or None.

        Args:
            validator: Callable that accepts a metadata dict and returns bool.

        Returns:
            The first matching entry ID, or None if no entry matches.
        """
        for entry_id in self._source.list_entries():
            metadata = self._source.get_metadata(entry_id)
            if validator(metadata):
                return entry_id
        return None

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _on_file_loaded(self, entry_id: str, tree_structure: dict) -> None:
        self.entry_loaded.emit(entry_id, tree_structure)

    def _on_load_error(self, filename: str, message: str) -> None:
        self.loading_error.emit(filename, message)

    def _on_loading_finished(self) -> None:
        self.loading_finished.emit()
        self._loader_worker = None

    @staticmethod
    def _split_path(full_path: str) -> tuple[str, str]:
        """Split 'entry_id/dot.path' into (entry_id, dot.path)."""
        parts = full_path.split("/", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        return parts[0], ""

    def cancel(self) -> None:
        """Stop any running background file loader."""
        if self._loader_worker and self._loader_worker.isRunning():
            self._loader_worker.requestInterruption()
            self._loader_worker.wait(2000)
            self._loader_worker = None
