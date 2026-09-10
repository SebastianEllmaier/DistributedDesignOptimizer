---
title: DataSelectionPanel (Source)
---

← Back to [DataSelectionPanel documentation](DataSelectionPanel.md)

# DataSelectionPanel - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\widgets\DataSelectionPanel.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Data selection panel for file loading, tree browsing, and item selection."""

import re

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTreeView, QListWidget, QLabel, QLineEdit, QFileDialog,
    QAbstractItemView, QListWidgetItem, QMenu, QApplication,
    QSplitter, QSplitterHandle, QFrame, QSizePolicy,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction, QPainter, QColor
from PySide6.QtCore import Signal, Qt, QModelIndex, QPoint, QSortFilterProxyModel

from ..styles.Theme import get_accent_color, PRIMARY, PRIMARY_LIGHT, SECONDARY, PRIMARY_DARK
from .ToggleSwitch import ToggleSwitch

_UNDO_STACK_LIMIT = 20


def _natural_sort_key(key: str) -> tuple:
    """Return a sort key that orders numeric strings numerically.

    Splits the key into numeric and non-numeric chunks so that, e.g.,
    "2" sorts before "11" instead of lexicographically after it. Each chunk
    is paired with a type-rank so numbers and text never compare against each
    other (which would raise a TypeError).
    """
    parts = re.split(r'(\d+)', str(key))
    return tuple(
        (0, int(part)) if part.isdigit() else (1, part.lower())
        for part in parts if part != ''
    )


class _GripSplitterHandle(QSplitterHandle):
    """Splitter handle that paints small grip dots and a directional arrow."""

    def paintEvent(self, event) -> None:
        """Paint grip dots and directional arrow on the handle.

        Args:
            event: The paint event triggered by Qt.
        """
        super().paintEvent(event)
        p = QPainter()
        if not p.begin(self):
            return
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        is_vertical = self.orientation() == Qt.Orientation.Vertical

        # Grip dots
        dot_c = QColor(0, 0, 0, 80)
        hover = self.underMouse()
        if hover:
            dot_c = QColor(3, 89, 112, 140)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(dot_c)
        r = 1.5
        if is_vertical:
            # Horizontal row of dots across center
            cy = h / 2
            n = 5
            spacing = 6
            x0 = w / 2 - (n - 1) * spacing / 2
            for i in range(n):
                p.drawEllipse(int(x0 + i * spacing - r), int(cy - r), int(2 * r), int(2 * r))
        else:
            # Vertical column of dots
            cx = w / 2
            n = 5
            spacing = 6
            y0 = h / 2 - (n - 1) * spacing / 2
            for i in range(n):
                p.drawEllipse(int(cx - r), int(y0 + i * spacing - r), int(2 * r), int(2 * r))
        p.end()


class _GripSplitter(QSplitter):
    """QSplitter that uses grip-dot handles."""

    def createHandle(self) -> QSplitterHandle:
        """Create a custom grip-dot splitter handle.

        Returns:
            A new grip-dot styled splitter handle.
        """
        return _GripSplitterHandle(self.orientation(), self)


class DataSelectionPanel(QWidget):
    """Left panel: file loading, tree browsing, item selection."""

    files_load_requested = Signal(list)   # [file_path, ...]
    selection_changed = Signal(list)       # [full_item_path, ...] currently in ListWidget

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the data selection panel.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.setMinimumWidth(250)
        self._undo_stack: list[list[str]] = []
        self._data_handler = None  # Set via set_data_handler()
        self._pending_trees: list[tuple[str, dict]] = []  # stored for re-filtering
        self._setup_ui()

    def set_data_handler(self, handler) -> None:
        """Set the DataHandler reference for plottability checks.

        Args:
            handler: The DataHandler instance used for plottability filtering.
        """
        self._data_handler = handler

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        # Load button row (primary action + Clear All Data)
        load_row = QHBoxLayout()
        load_row.setContentsMargins(0, 0, 0, 0)
        load_row.setSpacing(4)
        self._load_btn = QPushButton("Add More .dill History Files")
        self._load_btn.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self._load_btn.setStyleSheet(
            f"QPushButton {{ background-color: {PRIMARY}; color: white; "
            f"font-weight: bold; padding: 5px 12px; border-radius: 3px; }}"
            f"QPushButton:hover {{ background-color: {PRIMARY_DARK}; }}"
        )
        self._load_btn.clicked.connect(self.load_files)
        load_row.addWidget(self._load_btn)

        self._clear_all_btn = QPushButton("Clear All Data")
        self._clear_all_btn.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self._clear_all_btn.setStyleSheet(
            f"QPushButton {{ background-color: #cc4444; color: white; "
            f"font-weight: bold; padding: 5px 12px; border-radius: 3px; }}"
            f"QPushButton:hover {{ background-color: #aa3333; }}"
            f"QPushButton:disabled {{ background-color: #cccccc; color: #888888; }}"
        )
        self._clear_all_btn.setToolTip("Remove all loaded data and clear plots")
        self._clear_all_btn.setEnabled(False)
        load_row.addWidget(self._clear_all_btn)
        load_row.addStretch()
        layout.addLayout(load_row)

        # Second row: Auto-Update toggle + Refresh button
        action_row = QHBoxLayout()
        action_row.setContentsMargins(0, 0, 0, 0)
        action_row.setSpacing(4)

        self._auto_update_btn = ToggleSwitch("Auto-Update")
        self._auto_update_btn.setToolTip("Enable automatic file-change detection")
        self._auto_update_btn.setEnabled(False)
        action_row.addWidget(self._auto_update_btn)

        self._refresh_btn = QPushButton("Update Now")
        self._refresh_btn.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self._refresh_btn.setStyleSheet(
            f"QPushButton {{ background-color: {PRIMARY}; color: white; "
            f"font-weight: bold; padding: 5px 12px; border-radius: 3px; }}"
            f"QPushButton:hover {{ background-color: {PRIMARY_DARK}; }}"
            f"QPushButton:disabled {{ background-color: #cccccc; color: #888888; }}"
        )
        self._refresh_btn.setToolTip("Check for file changes and replot")
        self._refresh_btn.setEnabled(False)
        action_row.addWidget(self._refresh_btn)

        # Disable "Update Now" when auto-update is active
        self._auto_update_btn.toggled.connect(
            lambda on: self._refresh_btn.setEnabled(not on and self._refresh_btn_base_enabled)
        )
        self._refresh_btn_base_enabled = False
        action_row.addStretch()

        layout.addLayout(action_row)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: rgba(128, 128, 128, 0.3);")
        layout.addWidget(sep)

        # Filter field with clear button
        self._filter_input = QLineEdit()
        self._filter_input.setPlaceholderText("\U0001f50d Filter tree items...")
        self._filter_input.setClearButtonEnabled(True)
        self._filter_input.textChanged.connect(self._apply_filter)
        layout.addWidget(self._filter_input)

        # Hide non-plottable toggle
        self._hide_nonplottable_cb = ToggleSwitch("Hide non-plottable quantities")
        self._hide_nonplottable_cb.setChecked(True)
        self._hide_nonplottable_cb.setEnabled(False)
        self._hide_nonplottable_cb.setToolTip(
            "Exclude attributes that have no numeric data across all iterations"
        )
        self._hide_nonplottable_cb.toggled.connect(self._rebuild_tree)
        layout.addWidget(self._hide_nonplottable_cb)

        # Tree view
        tree_container = QWidget()
        tree_layout = QVBoxLayout(tree_container)
        tree_layout.setContentsMargins(0, 0, 0, 0)
        tree_layout.setSpacing(2)
        tree_label = QLabel("Data Structure")
        tree_label.setStyleSheet("font-weight: bold; font-size: 9pt;")
        tree_layout.addWidget(tree_label)

        self._tree_view = QTreeView()
        self._tree_model = QStandardItemModel()
        self._proxy_model = QSortFilterProxyModel()
        self._proxy_model.setSourceModel(self._tree_model)
        self._proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._proxy_model.setRecursiveFilteringEnabled(True)
        self._tree_view.setModel(self._proxy_model)
        self._tree_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self._tree_view.setHeaderHidden(True)
        self._tree_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._tree_view.setTextElideMode(Qt.TextElideMode.ElideNone)
        self._tree_view.expanded.connect(self._fit_tree_column)
        self._tree_view.collapsed.connect(self._fit_tree_column)
        self._tree_view.doubleClicked.connect(self._on_tree_double_click)
        tree_layout.addWidget(self._tree_view)

        # P6/P7: Add/Remove buttons between tree and list (vertical arrows)
        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(0, 2, 0, 2)
        self._add_btn = QPushButton("\u2193 Add")
        self._add_btn.setToolTip("Add selected tree items to the plot list")
        self._add_btn.setEnabled(False)
        self._add_btn.setStyleSheet(
            f"QPushButton {{ background-color: {PRIMARY}; color: white; "
            f"font-weight: bold; padding: 4px 10px; border-radius: 3px; }}"
            f"QPushButton:hover {{ background-color: {PRIMARY_DARK}; }}"
            f"QPushButton:disabled {{ background-color: #cccccc; color: #888888; }}"
        )
        self._add_btn.clicked.connect(self.move_selected_keys)
        self._remove_btn = QPushButton("\u2191 Remove")
        self._remove_btn.setToolTip("Remove selected items from the plot list")
        self._remove_btn.setEnabled(False)
        self._remove_btn.setStyleSheet(
            f"QPushButton {{ background-color: #cc4444; color: white; "
            f"font-weight: bold; padding: 4px 10px; border-radius: 3px; }}"
            f"QPushButton:hover {{ background-color: #aa3333; }}"
            f"QPushButton:disabled {{ background-color: #cccccc; color: #888888; }}"
        )
        self._remove_btn.clicked.connect(self.remove_selected_keys)
        btn_row.addWidget(self._add_btn)
        btn_row.addWidget(self._remove_btn)

        # Selected data label + list widget (B1: buttons placed here, between tree and list)
        list_container = QWidget()
        list_layout = QVBoxLayout(list_container)
        list_layout.setContentsMargins(0, 0, 0, 0)

        # B1: Add/Remove buttons at top of list container
        list_layout.addLayout(btn_row)

        # Header row with count (B2: bold header for visual weight)
        list_header = QHBoxLayout()
        selected_label = QLabel("Selected Data")
        selected_label.setStyleSheet("font-weight: bold; font-size: 9pt;")
        list_header.addWidget(selected_label)
        self._item_count_label = QLabel("0 items")
        self._item_count_label.setStyleSheet("color: gray; font-size: 8pt;")
        list_header.addStretch()
        list_header.addWidget(self._item_count_label)
        list_layout.addLayout(list_header)

        self._list_widget = QListWidget()
        self._list_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        # B5: Enable drag-drop reorder for controlling plot/legend order
        self._list_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self._list_widget.setDefaultDropAction(Qt.DropAction.MoveAction)
        list_layout.addWidget(self._list_widget)

        # QSplitter: tree → list (2 children only)
        self._splitter = _GripSplitter(Qt.Orientation.Vertical)
        self._splitter.addWidget(tree_container)
        self._splitter.addWidget(list_container)
        self._splitter.setStretchFactor(0, 3)
        self._splitter.setStretchFactor(1, 1)

        layout.addWidget(self._splitter, stretch=1)

        # Context menus
        self._tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._tree_view.customContextMenuRequested.connect(self._show_tree_context_menu)
        self._list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._list_widget.customContextMenuRequested.connect(self._show_list_context_menu)

        # C3: Enable/disable Add/Remove based on selection state
        self._tree_view.selectionModel().selectionChanged.connect(self._update_add_btn_state)
        self._list_widget.itemSelectionChanged.connect(self._update_remove_btn_state)

        # B5: Re-emit selection when items are reordered via drag-drop
        self._list_widget.model().rowsMoved.connect(lambda *_: self._emit_selection())

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def showEvent(self, event) -> None:  # noqa: N802
        """Handle the widget show event.

        Args:
            event: The show event triggered by Qt.
        """
        super().showEvent(event)

    def load_files(self) -> None:
        """Open a file dialog and emit paths."""
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Select .dill Files", "", "Dill Files (*.dill)"
        )
        if paths:
            self.files_load_requested.emit(paths)

    def populate_tree(self, entry_id: str, tree_structure: dict) -> None:
        """Add or update an entry's tree structure in the tree view.

        Args:
            entry_id: Unique identifier for the data entry.
            tree_structure: Nested dict representing the hierarchical data structure.
        """
        # Replace existing entry in pending list, or append new
        self._pending_trees = [
            (eid, ts) if eid != entry_id else (entry_id, tree_structure)
            for eid, ts in self._pending_trees
        ]
        if not any(eid == entry_id for eid, _ in self._pending_trees):
            self._pending_trees.append((entry_id, tree_structure))

        # Remove existing root item from the tree model if present,
        # preserving expanded state so the tree doesn't collapse on refresh.
        expanded_paths = self._collect_expanded_paths()
        root = self._tree_model.invisibleRootItem()
        for row in range(root.rowCount()):
            item = root.child(row)
            if item is not None and item.text() == entry_id:
                self._tree_model.removeRow(row)
                break

        self._add_entry_to_tree(entry_id, tree_structure, expand_default=False)
        self._restore_expanded_paths(expanded_paths)

    def _add_entry_to_tree(self, entry_id: str, tree_structure: dict,
                           expand_default: bool = True) -> None:
        """Build tree items for one entry, respecting the plottability filter."""
        root_item = QStandardItem(entry_id)
        root_item.setEditable(False)
        filter_active = self._hide_nonplottable_cb.isChecked()
        self._add_children(root_item, tree_structure, entry_id, "", filter_active)
        # Only add if the root has children (or filter is off)
        if root_item.rowCount() > 0 or not filter_active:
            self._tree_model.appendRow(root_item)
            if expand_default:
                self._tree_view.expandToDepth(0)
            self._fit_tree_column()

    def _rebuild_tree(self, *_args) -> None:
        """Rebuild the entire tree when the plottability filter is toggled."""
        # Save expanded paths before clearing
        expanded_paths = self._collect_expanded_paths()

        self._tree_model.clear()
        # Reconnect selection model (clearing the model resets it)
        self._tree_view.selectionModel().selectionChanged.connect(self._update_add_btn_state)
        for entry_id, tree_structure in self._pending_trees:
            self._add_entry_to_tree(entry_id, tree_structure, expand_default=False)

        # Restore expanded state
        self._restore_expanded_paths(expanded_paths)
        self._fit_tree_column()

    def _collect_expanded_paths(self) -> set[str]:
        """Collect UserRole paths of all currently expanded items."""
        expanded = set()
        self._walk_expanded(self._tree_model.invisibleRootItem(), expanded)
        return expanded

    def _walk_expanded(self, parent_item: QStandardItem, expanded: set[str]) -> None:
        """Recursively walk the tree model and record expanded item paths."""
        for row in range(parent_item.rowCount()):
            child = parent_item.child(row)
            if child is None:
                continue
            proxy_idx = self._proxy_model.mapFromSource(child.index())
            if proxy_idx.isValid() and self._tree_view.isExpanded(proxy_idx):
                path = child.data(Qt.ItemDataRole.UserRole) or f"__root__{child.text()}"
                expanded.add(path)
                self._walk_expanded(child, expanded)

    def _restore_expanded_paths(self, expanded_paths: set[str]) -> None:
        """Re-expand items whose UserRole path is in the given set."""
        if not expanded_paths:
            return
        self._walk_and_expand(self._tree_model.invisibleRootItem(), expanded_paths)

    def _walk_and_expand(self, parent_item: QStandardItem, expanded_paths: set[str]) -> None:
        """Recursively walk and expand matching items."""
        for row in range(parent_item.rowCount()):
            child = parent_item.child(row)
            if child is None:
                continue
            path = child.data(Qt.ItemDataRole.UserRole) or f"__root__{child.text()}"
            if path in expanded_paths:
                proxy_idx = self._proxy_model.mapFromSource(child.index())
                if proxy_idx.isValid():
                    self._tree_view.setExpanded(proxy_idx, True)
            self._walk_and_expand(child, expanded_paths)

    def clear_tree(self) -> None:
        """Remove all entries from the tree and selection list."""
        self._tree_model.clear()
        self._tree_view.selectionModel().selectionChanged.connect(self._update_add_btn_state)
        self._list_widget.clear()
        self._undo_stack.clear()
        self._pending_trees.clear()

    def move_selected_keys(self) -> None:
        """Move selected tree items to the list widget."""
        indexes = self._tree_view.selectedIndexes()
        if not indexes:
            return
        self._save_undo_state()
        for index in indexes:
            source_index = self._proxy_model.mapToSource(index)
            item = self._tree_model.itemFromIndex(source_index)
            if item is None or item.hasChildren():
                continue  # skip branch nodes
            full_path = self._build_item_path(item)
            # Avoid duplicates
            existing = [self._list_widget.item(i).text() for i in range(self._list_widget.count())]
            if full_path not in existing:
                item = QListWidgetItem(full_path)
                item.setToolTip(full_path)
                self._list_widget.addItem(item)
        self._emit_selection()

    def remove_selected_keys(self) -> None:
        """Remove selected items from the list widget."""
        if not self._list_widget.selectedItems():
            return
        self._save_undo_state()
        for item in reversed(self._list_widget.selectedItems()):
            row = self._list_widget.row(item)
            self._list_widget.takeItem(row)
        self._emit_selection()

    def get_selected_item_paths(self) -> list[str]:
        """Return currently highlighted items in the list widget.

        Returns:
            List of full paths for items currently selected in the list.
        """
        return [item.text() for item in self._list_widget.selectedItems()]

    def get_all_item_paths(self) -> list[str]:
        """Return all items in the list widget.

        Returns:
            List of full paths for all items in the list.
        """
        return [self._list_widget.item(i).text() for i in range(self._list_widget.count())]

    def undo(self) -> None:
        """Restore the list widget to its previous state."""
        if not self._undo_stack:
            return
        state = self._undo_stack.pop()
        self._list_widget.clear()
        for path in state:
            item = QListWidgetItem(path)
            item.setToolTip(path)
            self._list_widget.addItem(item)
        self._emit_selection()

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _add_children(self, parent_item: QStandardItem, structure: dict,
                       entry_id: str, prefix: str, filter_active: bool = False) -> None:
        """Recursively populate tree model from nested dict.

        When *filter_active* is True, leaf nodes that are non-plottable
        (all-NaN values) are excluded, and branches with no remaining
        children are also excluded.
        """
        if not isinstance(structure, dict):
            return
        for key, subtree in sorted(structure.items(), key=lambda kv: _natural_sort_key(kv[0])):
            current_path = f"{prefix}.{key}" if prefix else key
            full_path = f"{entry_id}/{current_path}"

            if isinstance(subtree, dict) and subtree:
                # Branch node — recurse first, then decide whether to keep
                child = QStandardItem(key)
                child.setEditable(False)
                child.setData(full_path, Qt.ItemDataRole.UserRole)
                self._add_children(child, subtree, entry_id, current_path, filter_active)
                if filter_active and child.rowCount() == 0:
                    continue  # skip empty branches
                parent_item.appendRow(child)
            else:
                # Leaf node — check plottability if filter is active
                if filter_active and self._data_handler is not None:
                    if not self._data_handler.is_path_plottable(entry_id, current_path):
                        continue
                child = QStandardItem(key)
                child.setEditable(False)
                child.setData(full_path, Qt.ItemDataRole.UserRole)
                parent_item.appendRow(child)

    def _build_item_path(self, item: QStandardItem) -> str:
        """Build the full path from a tree item's stored data."""
        data = item.data(Qt.ItemDataRole.UserRole)
        if data:
            return data
        # Fallback: walk parents
        parts = []
        current = item
        while current:
            parts.insert(0, current.text())
            current = current.parent()
        return "/".join(parts[:1]) + "/" + ".".join(parts[1:]) if len(parts) > 1 else parts[0]

    def _on_tree_double_click(self, index: QModelIndex) -> None:
        """Double-click: leaf adds itself, branch adds all leaves (C5a)."""
        source_index = self._proxy_model.mapToSource(index)
        item = self._tree_model.itemFromIndex(source_index)
        if item is None:
            return
        existing = {self._list_widget.item(i).text() for i in range(self._list_widget.count())}
        if item.rowCount() == 0:
            full_path = self._build_item_path(item)
            if full_path not in existing:
                list_item = QListWidgetItem(full_path)
                list_item.setToolTip(full_path)
                self._list_widget.addItem(list_item)
        else:
            self._save_undo_state()
            self._collect_leaves(item, existing)
        self._emit_selection()

    def _show_tree_context_menu(self, pos: QPoint) -> None:
        """Right-click context menu for the tree view."""
        menu = QMenu(self)
        add_action = QAction("Add to Selection", self)
        add_action.triggered.connect(self.move_selected_keys)
        menu.addAction(add_action)

        add_children_action = QAction("Add All Children", self)
        add_children_action.triggered.connect(self._add_all_children)
        menu.addAction(add_children_action)

        expand_action = QAction("Expand All", self)
        expand_action.triggered.connect(self._tree_view.expandAll)
        menu.addAction(expand_action)

        collapse_action = QAction("Collapse All", self)
        collapse_action.triggered.connect(self._tree_view.collapseAll)
        menu.addAction(collapse_action)

        menu.exec(self._tree_view.viewport().mapToGlobal(pos))

    def _fit_tree_column(self, *_args) -> None:
        """Ensure tree column is at least as wide as the viewport."""
        self._tree_view.resizeColumnToContents(0)
        vw = self._tree_view.viewport().width()
        if self._tree_view.header().sectionSize(0) < vw:
            self._tree_view.header().resizeSection(0, vw)

    def _show_list_context_menu(self, pos: QPoint) -> None:
        """Right-click context menu for the list widget."""
        menu = QMenu(self)
        remove_action = QAction("Remove Selected", self)
        remove_action.triggered.connect(self.remove_selected_keys)
        menu.addAction(remove_action)

        remove_all_action = QAction("Remove All", self)
        remove_all_action.triggered.connect(self._remove_all)
        menu.addAction(remove_all_action)

        if self._list_widget.currentItem():
            copy_action = QAction("Copy Path", self)
            copy_action.triggered.connect(self._copy_selected_path)
            menu.addAction(copy_action)

        menu.exec(self._list_widget.viewport().mapToGlobal(pos))

    def _remove_all(self) -> None:
        """Remove all items from the list widget."""
        self._save_undo_state()
        self._list_widget.clear()
        self._emit_selection()

    def _add_all_children(self) -> None:
        """Recursively add all leaf children of selected tree items to the list."""
        self._save_undo_state()  # B5: allow undo
        indexes = self._tree_view.selectedIndexes()
        existing = {self._list_widget.item(i).text() for i in range(self._list_widget.count())}
        for index in indexes:
            source_index = self._proxy_model.mapToSource(index)
            item = self._tree_model.itemFromIndex(source_index)
            if item:
                self._collect_leaves(item, existing)
        self._emit_selection()

    def _collect_leaves(self, item: QStandardItem, existing: set[str]) -> None:
        """Recursively collect leaf nodes from a tree item."""
        if item.rowCount() == 0:
            full_path = self._build_item_path(item)
            if full_path not in existing:
                item = QListWidgetItem(full_path)
                item.setToolTip(full_path)
                self._list_widget.addItem(item)
                existing.add(full_path)
        else:
            for row in range(item.rowCount()):
                self._collect_leaves(item.child(row), existing)

    def _copy_selected_path(self) -> None:
        """Copy the current item's path to clipboard."""
        item = self._list_widget.currentItem()
        if item:
            QApplication.clipboard().setText(item.text())

    def _apply_filter(self, text: str) -> None:
        """Filter tree items via proxy model."""
        self._proxy_model.setFilterFixedString(text)
        if text:
            self._tree_view.expandAll()
        else:
            self._tree_view.collapseAll()
            self._tree_view.expandToDepth(0)

    def _emit_selection(self) -> None:
        """Emit the current full list of items and update count label."""
        paths = self.get_all_item_paths()
        count = len(paths)
        self._item_count_label.setText(f"{count} item{'s' if count != 1 else ''}")
        self.selection_changed.emit(paths)

    def _update_add_btn_state(self, *_args) -> None:
        """Enable Add only when at least one selected item is a leaf node."""
        for index in self._tree_view.selectedIndexes():
            source_index = self._proxy_model.mapToSource(index)
            item = self._tree_model.itemFromIndex(source_index)
            if item is not None and not item.hasChildren():
                self._add_btn.setEnabled(True)
                return
        self._add_btn.setEnabled(False)

    def _update_remove_btn_state(self) -> None:
        self._remove_btn.setEnabled(bool(self._list_widget.selectedItems()))

    def _save_undo_state(self) -> None:
        """Snapshot current list state onto the undo stack."""
        state = [self._list_widget.item(i).text() for i in range(self._list_widget.count())]
        self._undo_stack.append(state)
        if len(self._undo_stack) > _UNDO_STACK_LIMIT:
            self._undo_stack.pop(0)

```
