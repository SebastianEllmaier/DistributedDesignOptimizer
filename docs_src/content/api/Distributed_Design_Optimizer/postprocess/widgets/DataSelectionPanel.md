---
title: DataSelectionPanel
---

← Back to [widgets](index.md)

# DataSelectionPanel

**Source:** [Distributed_Design_Optimizer\postprocess\widgets\DataSelectionPanel.py](DataSelectionPanel_source.md)

Data selection panel for file loading, tree browsing, and item selection.

## Classes

### _GripSplitterHandle

> **Inherits from:** `QSplitterHandle`

> Splitter handle that paints small grip dots and a directional arrow.

#### Methods

??? abstract "paintEvent(self, event) → None"
    Paint grip dots and directional arrow on the handle.


    **Args:**
    > event: The paint event triggered by Qt.  

### _GripSplitter

> **Inherits from:** `QSplitter`

> QSplitter that uses grip-dot handles.

#### Methods

??? abstract "createHandle(self) → QSplitterHandle"
    Create a custom grip-dot splitter handle.


    **Returns:**
    > A new grip-dot styled splitter handle.  

### DataSelectionPanel

> **Inherits from:** `QWidget`

> Left panel: file loading, tree browsing, item selection.

#### Methods

??? abstract "__init__(self, parent: QWidget | None) → None"
    Initialize the data selection panel.


    **Args:**
    > parent: Optional parent widget.  

??? abstract "set_data_handler(self, handler) → None"
    Set the DataHandler reference for plottability checks.


    **Args:**
    > handler: The DataHandler instance used for plottability filtering.  

??? abstract "showEvent(self, event) → None"
    Handle the widget show event.


    **Args:**
    > event: The show event triggered by Qt.  

??? abstract "load_files(self) → None"
    Open a file dialog and emit paths.

??? abstract "populate_tree(self, entry_id: str, tree_structure: dict) → None"
    Add or update an entry's tree structure in the tree view.


    **Args:**
    > entry_id: Unique identifier for the data entry.  
    > tree_structure: Nested dict representing the hierarchical data structure.  

??? abstract "clear_tree(self) → None"
    Remove all entries from the tree and selection list.

??? abstract "move_selected_keys(self) → None"
    Move selected tree items to the list widget.

??? abstract "remove_selected_keys(self) → None"
    Remove selected items from the list widget.

??? abstract "get_selected_item_paths(self) → list[str]"
    Return currently highlighted items in the list widget.


    **Returns:**
    > List of full paths for items currently selected in the list.  

??? abstract "get_all_item_paths(self) → list[str]"
    Return all items in the list widget.


    **Returns:**
    > List of full paths for all items in the list.  

??? abstract "undo(self) → None"
    Restore the list widget to its previous state.

