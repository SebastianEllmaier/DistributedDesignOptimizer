---
title: DillDataSource
---

← Back to [models](index.md)

# DillDataSource

**Source:** [Distributed_Design_Optimizer\postprocess\models\DillDataSource.py](DillDataSource_source.md)

Dill-file-backed implementation of the DataSource interface.

## Classes

### DillDataSource

> **Inherits from:** [DataSource](DataSource.md#datasource)

> Data source backed by .dill files on disk.

#### Methods

??? abstract "__init__(self) → None"
    Initialize empty storage dicts and a reentrant lock.

??? abstract "connect(self) → None"
    No-op for file-based source.

??? abstract "load_entry(self, path: str) → str"
    Load a .dill file and return its entry_id (filename).


    **Args:**
    > path: Filesystem path to the .dill file.  


    **Returns:**
    > The entry identifier string (derived from the filename).  

??? abstract "list_entries(self) → list[str]"
    Return all loaded entry IDs.


    **Returns:**
    > List of entry identifier strings.  

??? abstract "get_tree_structure(self, entry_id: str) → dict"
    Walk the loaded deque/dict and return a nested dict for tree display.

    Leaf nodes have value ``None``; branch nodes are nested dicts.


    **Args:**
    > entry_id: Identifier of the loaded entry.  


    **Returns:**
    > Nested dict representing the data hierarchy.  

??? abstract "get_values(self, entry_id: str, item_path: str) → list[float]"
    Collect the scalar value at *item_path* across all iterations.

    Handles two data shapes:
    - Multi-queue: deque of dicts, each containing scalars -> one value per element.
    - Single-queue: deque with one element containing arrays -> values from that array.


    **Args:**
    > entry_id: Identifier of the loaded entry.  
    > item_path: Dot-separated path to the data variable.  


    **Returns:**
    > List of floats, one per data point. Non-numeric values produce NaN.  

??? abstract "get_iteration_data(self, entry_id: str, iteration: int) → dict"
    Return full data dict for a single iteration.


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
    Return metadata dict for the given entry.


    **Args:**
    > entry_id: Identifier of the loaded entry.  


    **Returns:**
    > Dict with keys: filename, path, n_iterations, is_coordinator.  

??? abstract "check_for_updates(self) → dict[str, bool]"
    Check file modification times and return which entries have changed.


    **Returns:**
    > Dict mapping entry IDs to whether the file has been modified.  

??? abstract "reload_entry(self, entry_id: str) → None"
    Re-load a previously loaded entry from its stored file path.


    **Args:**
    > entry_id: Identifier of the entry to reload.  

??? abstract "remove_entry(self, entry_id: str) → None"
    Remove a single entry from loaded data.


    **Args:**
    > entry_id: Identifier of the entry to remove.  

??? abstract "get_iteration_labels(self, entry_id: str) → list[dict]"
    Extract per-iteration metadata for x-axis labeling.

    Returns dicts with keys: outerloop_itr, innerloop_itr,
    innerloop_itr_runtime, innerloop_itr_numberofdesignvariableevaluations.


    **Args:**
    > entry_id: Identifier of the loaded entry.  


    **Returns:**
    > List of dicts with iteration metadata keys.  

??? abstract "close(self) → None"
    Release resources and clear all loaded data.

