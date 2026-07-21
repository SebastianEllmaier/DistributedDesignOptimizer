# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Dill-file-backed implementation of the DataSource interface."""
import os
import time
import threading
import types
import logging
from collections import deque
from pathlib import Path

import numpy as np

try:
    import networkx as _nx
    _NX_GRAPH_TYPES: tuple = (_nx.Graph, _nx.DiGraph, _nx.MultiGraph, _nx.MultiDiGraph)
except ImportError:
    _NX_GRAPH_TYPES = ()

from .DataSource import DataSource
from ..utils.FlexibleUnpickler import FlexibleUnpickler

logger = logging.getLogger(__name__)

_LOAD_RETRIES = 3
_LOAD_RETRY_DELAY = 0.5  # seconds


class DillDataSource(DataSource):
    """Data source backed by .dill files on disk."""

    def __init__(self) -> None:
        """Initialize empty storage dicts and a reentrant lock."""
        self._history_data: dict[str, deque] = {}
        self._file_paths: dict[str, str] = {}
        self._file_mtimes: dict[str, float] = {}
        self._lock = threading.RLock()

    # ------------------------------------------------------------------
    # DataSource interface
    # ------------------------------------------------------------------

    def connect(self, **kwargs) -> None:
        """No-op for file-based source."""

    def load_entry(self, path: str) -> str:
        """Load a .dill file and return its entry_id (filename).

        Args:
            path: Filesystem path to the .dill file.

        Returns:
            The entry identifier string (derived from the filename).
        """
        filepath = Path(path)
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {path}")

        # Retry loading in case the file is mid-write (e.g. during auto-update)
        last_error: Exception | None = None
        for attempt in range(_LOAD_RETRIES):
            try:
                with open(filepath, "rb") as f:
                    data = FlexibleUnpickler(f).load()
                break
            except (EOFError, OSError, Exception) as e:
                last_error = e
                if attempt < _LOAD_RETRIES - 1:
                    logger.debug(f"Load attempt {attempt + 1} failed for {path}: {e}, retrying...")
                    time.sleep(_LOAD_RETRY_DELAY)
        else:
            raise IOError(f"Failed to load {path} after {_LOAD_RETRIES} attempts: {last_error}") from last_error

        resolved = str(filepath.resolve())
        entry_id = filepath.name

        with self._lock:
            # Check if this exact file path is already loaded under an existing entry_id
            for eid, fpath in self._file_paths.items():
                if fpath == resolved:
                    # Update in-place
                    self._history_data[eid] = data
                    self._file_mtimes[eid] = os.path.getmtime(filepath)
                    return eid

            # New file — ensure uniqueness for same-name files from different directories
            if entry_id in self._history_data:
                counter = 2
                base = entry_id
                while entry_id in self._history_data:
                    entry_id = f"{base}_{counter}"
                    counter += 1

            self._history_data[entry_id] = data
            self._file_paths[entry_id] = resolved
            self._file_mtimes[entry_id] = os.path.getmtime(filepath)
        return entry_id

    def list_entries(self) -> list[str]:
        """Return all loaded entry IDs.

        Returns:
            List of entry identifier strings.
        """
        return list(self._history_data.keys())

    def get_tree_structure(self, entry_id: str) -> dict:
        """Walk the loaded deque/dict and return a nested dict for tree display.

        Leaf nodes have value ``None``; branch nodes are nested dicts.

        Args:
            entry_id: Identifier of the loaded entry.

        Returns:
            Nested dict representing the data hierarchy.
        """
        data = self._history_data.get(entry_id)
        if data is None:
            return {}
        return self._build_tree(data)

    def get_values(self, entry_id: str, item_path: str) -> list[float]:
        """Collect the scalar value at *item_path* across all iterations.

        Handles two data shapes:
        - Multi-queue: deque of dicts, each containing scalars -> one value per element.
        - Single-queue: deque with one element containing arrays -> values from that array.

        Args:
            entry_id: Identifier of the loaded entry.
            item_path: Dot-separated path to the data variable.

        Returns:
            List of floats, one per data point. Non-numeric values produce NaN.
        """
        data = self._history_data.get(entry_id)
        if data is None:
            return []

        iterable = data if isinstance(data, (deque, list)) else [data]

        # Single-queue detection: if there's exactly one element and the target
        # value is an array/list, extract values from it directly
        if len(iterable) == 1:
            val = self._get_nested_value(iterable[0], item_path)
            if val is not None and isinstance(val, (list, tuple, np.ndarray)):
                result: list[float] = []
                for v in val:
                    try:
                        result.append(float(v))
                    except (TypeError, ValueError):
                        result.append(float('nan'))
                return result

        # Multi-queue: one scalar per iteration
        values: list[float] = []
        for item in iterable:
            val = self._get_nested_value(item, item_path)
            if val is None:
                values.append(float('nan'))
            else:
                try:
                    values.append(float(val))
                except (TypeError, ValueError):
                    values.append(float('nan'))
        return values

    def get_iteration_data(self, entry_id: str, iteration: int) -> dict:
        """Return full data dict for a single iteration.

        Args:
            entry_id: Identifier of the loaded entry.
            iteration: Zero-based iteration index.

        Returns:
            Dict containing all data for the requested iteration.
        """
        data = self._history_data.get(entry_id)
        if data is None:
            return {}
        iterable = data if isinstance(data, (deque, list)) else [data]
        if 0 <= iteration < len(iterable):
            return iterable[iteration]
        return {}

    def get_all_iterations(self, entry_id: str) -> deque:
        """Return all iterations for an entry.

        Args:
            entry_id: Identifier of the loaded entry.

        Returns:
            Deque of iteration data dicts.
        """
        return self._history_data.get(entry_id, deque())

    def get_metadata(self, entry_id: str) -> dict:
        """Return metadata dict for the given entry.

        Args:
            entry_id: Identifier of the loaded entry.

        Returns:
            Dict with keys: filename, path, n_iterations, is_coordinator.
        """
        data = self._history_data.get(entry_id)
        n_iterations = len(data) if isinstance(data, (deque, list)) else 1
        filepath = self._file_paths.get(entry_id, "")
        is_coordinator = "coordinator" in entry_id.lower()
        return {
            "filename": entry_id,
            "path": filepath,
            "n_iterations": n_iterations,
            "is_coordinator": is_coordinator,
        }

    def check_for_updates(self) -> dict[str, bool]:
        """Check file modification times and return which entries have changed.

        Returns:
            Dict mapping entry IDs to whether the file has been modified.
        """
        with self._lock:
            changed: dict[str, bool] = {}
            for entry_id, filepath in self._file_paths.items():
                try:
                    current_mtime = os.path.getmtime(filepath)
                    changed[entry_id] = current_mtime > self._file_mtimes.get(entry_id, 0)
                except OSError:
                    changed[entry_id] = False
            return changed

    def reload_entry(self, entry_id: str) -> None:
        """Re-load a previously loaded entry from its stored file path.

        Args:
            entry_id: Identifier of the entry to reload.
        """
        with self._lock:
            path = self._file_paths.get(entry_id)
        if path:
            self.load_entry(path)

    def remove_entry(self, entry_id: str) -> None:
        """Remove a single entry from loaded data.

        Args:
            entry_id: Identifier of the entry to remove.
        """
        with self._lock:
            self._history_data.pop(entry_id, None)
            self._file_paths.pop(entry_id, None)
            self._file_mtimes.pop(entry_id, None)

    def get_iteration_labels(self, entry_id: str) -> list[dict]:
        """Extract per-iteration metadata for x-axis labeling.

        Returns dicts with keys: outerloop_itr, innerloop_itr,
        innerloop_itr_runtime, innerloop_itr_numberofdesignvariableevaluations.

        Args:
            entry_id: Identifier of the loaded entry.

        Returns:
            List of dicts with iteration metadata keys.
        """
        data = self._history_data.get(entry_id)
        if data is None:
            return []
        iterable = data if isinstance(data, (deque, list)) else [data]
        labels: list[dict] = []
        for item in iterable:
            labels.append({
                "outerloop_itr": getattr(item, "_outerloop_itr", None),
                "innerloop_itr": getattr(item, "_innerloop_itr", None),
                "innerloop_itr_runtime": getattr(item, "_innerloop_itr_runtime", None),
                "innerloop_itr_numberofdesignvariableevaluations": getattr(item, "_innerloop_itr_numberofdesignvariableevaluations", None),
            })
        return labels

    def close(self) -> None:
        """Release resources and clear all loaded data."""
        with self._lock:
            self._history_data.clear()
            self._file_paths.clear()
            self._file_mtimes.clear()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_tree(self, data, max_depth: int = 8) -> dict:
        """Recursively build a nested dict of keys/attributes."""
        if isinstance(data, (deque, list)):
            if len(data) == 0:
                return {}
            # Use first element as the representative structure
            representative = None
            for item in data:
                if item is not None:
                    representative = item
                    break
            if representative is None:
                return {}
            return self._build_tree(representative, max_depth)

        if max_depth <= 0:
            return {}

        tree: dict = {}
        if isinstance(data, dict):
            for key in sorted(data.keys()):
                child = data[key]
                subtree = self._inspect_child(child, max_depth - 1)
                tree[str(key)] = subtree
        elif hasattr(data, "__dict__"):
            for key in sorted(vars(data).keys()):
                child = getattr(data, key)
                subtree = self._inspect_child(child, max_depth - 1)
                # Strip leading underscores for display but keep attribute accessible
                display_key = key.lstrip("_") if key.startswith("_") else key
                tree[display_key] = subtree
        return tree

    def _inspect_child(self, child, max_depth: int) -> dict | None:
        """Return sub-tree dict for a child, or None for leaf nodes."""
        if child is None:
            return None
        if isinstance(child, (int, float, str, bool, np.floating, np.integer)):
            return None
        # NetworkX graphs: treat as leaf to avoid massive internal tree expansion
        if _NX_GRAPH_TYPES and isinstance(child, _NX_GRAPH_TYPES):
            return None
        if isinstance(child, np.ndarray):
            if child.ndim == 0:
                return None
            if child.ndim == 1 and len(child) > 0:
                # 1-D array of scalars: expose individual elements by index
                if np.issubdtype(child.dtype, np.number) or np.issubdtype(child.dtype, np.bool_):
                    return {str(i): None for i in range(len(child))}
            return None
        if isinstance(child, (list, tuple)):
            if len(child) == 0:
                return None
            # Check if list of scalars (plottable) vs list of complex objects
            if isinstance(child[0], (int, float, str, bool, np.floating, np.integer)):
                # Expose individual elements by index for per-element plotting
                return {str(i): None for i in range(len(child))}
            # List of complex objects: expose by index, then recurse into structure
            subtree: dict = {}
            for i, item in enumerate(child):
                item_tree = self._build_tree(item, max_depth)
                if item_tree:
                    subtree[str(i)] = item_tree
                else:
                    subtree[str(i)] = None
            return subtree if subtree else None
        if isinstance(child, dict):
            return self._build_tree(child, max_depth)
        if hasattr(child, "__dict__") and not isinstance(child, types.ModuleType):
            return self._build_tree(child, max_depth)
        return None

    @staticmethod
    def _get_nested_value(obj, path: str):
        """Traverse a nested object using a dot-separated path.

        Handles dict keys, list/array indices, and object attributes.
        For object attributes, also tries the underscore-prefixed variant
        (e.g., 'globalobjectivefunctionvalue' → '_globalobjectivefunctionvalue')
        to match the tree display convention of stripping leading underscores.
        """
        attrs = path.split(".")
        for attr in attrs:
            if isinstance(obj, dict) and attr in obj:
                obj = obj[attr]
            elif isinstance(obj, (list, tuple, np.ndarray)) and attr.isdigit():
                index = int(attr)
                if 0 <= index < len(obj):
                    obj = obj[index]
                else:
                    return None
            elif hasattr(obj, attr):
                obj = getattr(obj, attr)
            elif hasattr(obj, f"_{attr}"):
                obj = getattr(obj, f"_{attr}")
            else:
                return None
        return obj
