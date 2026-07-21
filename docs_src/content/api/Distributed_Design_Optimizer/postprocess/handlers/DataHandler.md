---
title: DataHandler
---

← Back to [handlers](index.md)

# DataHandler

**Source:** [Distributed_Design_Optimizer\postprocess\handlers\DataHandler.py](DataHandler_source.md)

Handler for loading, caching, and accessing optimization history data.

## Classes

### DataHandler

> **Inherits from:** `QObject`

> Manages data loading, caching, and access through the DataSource abstraction.

#### Methods

??? abstract "__init__(self, parent: QObject | None) → None"
    Initialize the DataHandler with a default DillDataSource.


    **Args:**
    > parent: Optional parent QObject for Qt ownership.  

??? abstract "source(self) → [DataSource](../models/DataSource.md#datasource)"
    Return the active data source.


    **Returns:**
    > The currently active DataSource instance.  

??? abstract "set_source(self, source: [DataSource](../models/DataSource.md#datasource)) → None"
    Replace the active data source.


    **Args:**
    > source: The new DataSource instance to use.  

??? abstract "load_files(self, paths: list[str]) → None"
    Start background loading of .dill files.


    **Args:**
    > paths: List of file paths to load.  

??? abstract "get_plottable_data(self, item_paths: list[str]) → list[tuple[str, list[float]]]"
    Get plot-ready data for a list of item paths.

    item_paths format: "entry_id/dot.separated.path"
    Paths that resolve to all-NaN values (non-numeric data) are excluded.


    **Args:**
    > item_paths: List of paths in "entry_id/dot.separated.path" format.  


    **Returns:**
    > List of (full_path, values) tuples for paths with numeric data.  

??? abstract "is_path_plottable(self, entry_id: str, item_path: str) → bool"
    Check if a leaf path has at least one non-NaN numeric value.


    **Args:**
    > entry_id: Identifier of the loaded data entry.  
    > item_path: Dot-separated path to a leaf data item.  


    **Returns:**
    > True if the path has at least one finite numeric value.  

??? abstract "get_iteration_data(self, entry_id: str, iteration: int) → dict"
    Return the raw data dictionary for a specific iteration.


    **Args:**
    > entry_id: Identifier of the loaded data entry.  
    > iteration: Zero-based iteration index.  


    **Returns:**
    > Dictionary of data for the requested iteration.  

??? abstract "get_all_iterations(self, entry_id: str) → deque"
    Return all iteration records for the given entry.


    **Args:**
    > entry_id: Identifier of the loaded data entry.  


    **Returns:**
    > Deque of iteration data dictionaries.  

??? abstract "get_metadata(self, entry_id: str) → dict"
    Return metadata for the given entry.


    **Args:**
    > entry_id: Identifier of the loaded data entry.  


    **Returns:**
    > Dictionary of metadata for the entry.  

??? abstract "list_entries(self) → list[str]"
    Return a list of all loaded entry identifiers.


    **Returns:**
    > List of entry ID strings.  

??? abstract "get_iteration_labels(self, entry_id: str) → list[dict]"
    Return per-iteration outerloop/innerloop metadata for x-axis labeling.


    **Args:**
    > entry_id: Identifier of the loaded data entry.  


    **Returns:**
    > List of label dictionaries, one per iteration.  

??? abstract "get_iteration_labels_map(self, item_paths: list[str]) → dict[str, list[dict]]"
    Return {entry_id: labels} for each unique entry referenced by item_paths.


    **Args:**
    > item_paths: List of paths in "entry_id/dot.separated.path" format.  


    **Returns:**
    > Mapping of entry IDs to their iteration label lists.  

??? abstract "check_for_updates(self) → dict[str, bool]"
    Check which loaded entries have been modified on disk.


    **Returns:**
    > Mapping of entry IDs to whether they have changed.  

??? abstract "reload_entries(self, entry_ids: list[str]) → None"
    Reload one or more entries from their backing files.


    **Args:**
    > entry_ids: List of entry identifiers to reload.  

??? abstract "refresh_data(self, entry_ids: list[str]) → None"
    Reload data and re-emit tree structure (for auto-update).


    **Args:**
    > entry_ids: List of entry identifiers to refresh.  

??? abstract "clear_all(self) → None"
    Clear all loaded data.

??? abstract "remove_entry(self, entry_id: str) → None"
    Remove a single entry from loaded data.


    **Args:**
    > entry_id: Identifier of the entry to remove.  

??? abstract "find_coordinator_entry(self, validator) → str | None"
    Return the first entry_id whose metadata passes *validator*, or None.


    **Args:**
    > validator: Callable that accepts a metadata dict and returns bool.  


    **Returns:**
    > The first matching entry ID, or None if no entry matches.  

??? abstract "cancel(self) → None"
    Stop any running background file loader.

