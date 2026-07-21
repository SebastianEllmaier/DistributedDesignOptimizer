---
title: DataSource
---

← Back to [models](index.md)

# DataSource

**Source:** [Distributed_Design_Optimizer\postprocess\models\DataSource.py](DataSource_source.md)

Abstract base class defining the data source interface for postprocessing backends.

## Classes

### DataSource

> **Inherits from:** `ABC`

> Abstract interface for all data backends (dill files, PostgreSQL, etc.).

#### Methods

??? abstract "connect(self) → None"
    Establish connection to the data source.

??? abstract "load_entry(self, path_or_id: str) → str"
    Load one entry and return its entry_id.


    **Args:**
    > path_or_id: File path or database identifier of the entry to load.  


    **Returns:**
    > The unique entry identifier string.  

??? abstract "list_entries(self) → list[str]"
    Return all loaded entry IDs.


    **Returns:**
    > List of entry identifier strings.  

??? abstract "get_tree_structure(self, entry_id: str) → dict"
    Return nested dict representing the data hierarchy for tree population.


    **Args:**
    > entry_id: Identifier of the loaded entry.  


    **Returns:**
    > Nested dict where leaves are ``None`` and branches are sub-dicts.  

??? abstract "get_values(self, entry_id: str, item_path: str) → list[float]"
    Return time-series values for a given dot-separated path.


    **Args:**
    > entry_id: Identifier of the loaded entry.  
    > item_path: Dot-separated path to the data variable.  


    **Returns:**
    > List of float values across iterations.  

??? abstract "get_iteration_data(self, entry_id: str, iteration: int) → dict"
    Return full data dict for one iteration.


    **Args:**
    > entry_id: Identifier of the loaded entry.  
    > iteration: Zero-based iteration index.  


    **Returns:**
    > Dict containing all data for the requested iteration.  

??? abstract "get_all_iterations(self, entry_id: str) → deque"
    Return all iterations for an entry.


    **Args:**
    > entry_id: Identifier of the loaded entry.  


    **Returns:**
    > Deque of iteration data dicts.  

??? abstract "get_metadata(self, entry_id: str) → dict"
    Return metadata dict (filename, path, n_iterations, is_coordinator, etc.).


    **Args:**
    > entry_id: Identifier of the loaded entry.  


    **Returns:**
    > Dict with keys such as filename, path, n_iterations, and is_coordinator.  

??? abstract "check_for_updates(self) → dict[str, bool]"
    Return {entry_id: has_changed} for auto-update.


    **Returns:**
    > Dict mapping entry IDs to whether they have changed since last load.  

??? abstract "reload_entry(self, entry_id: str) → None"
    Re-load an entry from its stored source (file path, DB id, etc.).


    **Args:**
    > entry_id: Identifier of the entry to reload.  

??? abstract "get_iteration_labels(self, entry_id: str) → list[dict]"
    Return per-iteration metadata for x-axis labeling.

    Each dict contains:
    outerloop_itr: int
    innerloop_itr: int
    innerloop_itr_runtime: float
    innerloop_itr_numberofdesignvariableevaluations: int
    Returns empty list if iteration metadata is unavailable.


    **Args:**
    > entry_id: Identifier of the loaded entry.  


    **Returns:**
    > List of dicts with iteration metadata keys.  

??? abstract "remove_entry(self, entry_id: str) → None"
    Remove a single entry from the loaded data.


    **Args:**
    > entry_id: Identifier of the entry to remove.  

??? abstract "close(self) → None"
    Release resources and clear loaded data.

