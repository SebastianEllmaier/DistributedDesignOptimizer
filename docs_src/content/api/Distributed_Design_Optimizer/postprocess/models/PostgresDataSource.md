---
title: PostgresDataSource
---

← Back to [models](index.md)

# PostgresDataSource

**Source:** [Distributed_Design_Optimizer\postprocess\models\PostgresDataSource.py](PostgresDataSource_source.md)

Stub PostgreSQL implementation of the DataSource interface.

## Classes

### PostgresDataSource

> **Inherits from:** [DataSource](DataSource.md#datasource)

> Future PostgreSQL data source — stub implementation.

> Intended SQL schema:
> runs(run_id, name, coordinator_type, created_at, updated_at)
> iterations(iteration_id, run_id, outer_loop_itr, data JSONB, created_at)
> time_series(run_id, variable_path, iteration, value)

#### Methods

??? abstract "connect(self) → None"
    Establish connection to the PostgreSQL database.

    Future: QSqlDatabase.addDatabase("QPSQL") or psycopg2.connect(
    host=kwargs['host'], port=kwargs['port'],
    dbname=kwargs['dbname'], user=kwargs['user'], password=kwargs['password']
    )

??? abstract "load_entry(self, path_or_id: str) → str"
    Load a run entry by its database identifier.


    **Args:**
    > path_or_id: Database run identifier.  


    **Returns:**
    > The entry identifier string.  

??? abstract "list_entries(self) → list[str]"
    Return all loaded entry IDs from the database.


    **Returns:**
    > List of entry identifier strings.  

??? abstract "get_tree_structure(self, entry_id: str) → dict"
    Return nested dict representing the variable hierarchy.


    **Args:**
    > entry_id: Identifier of the run entry.  


    **Returns:**
    > Nested dict for tree display.  

??? abstract "get_values(self, entry_id: str, item_path: str) → list[float]"
    Return time-series values for a given variable path.


    **Args:**
    > entry_id: Identifier of the run entry.  
    > item_path: Dot-separated path to the variable.  


    **Returns:**
    > List of float values across iterations.  

??? abstract "get_iteration_data(self, entry_id: str, iteration: int) → dict"
    Return full data dict for one iteration.


    **Args:**
    > entry_id: Identifier of the run entry.  
    > iteration: Zero-based iteration index.  


    **Returns:**
    > Dict containing all data for the requested iteration.  

??? abstract "get_all_iterations(self, entry_id: str) → deque"
    Return all iterations for an entry.


    **Args:**
    > entry_id: Identifier of the run entry.  


    **Returns:**
    > Deque of iteration data dicts.  

??? abstract "get_metadata(self, entry_id: str) → dict"
    Return metadata dict for the given run entry.


    **Args:**
    > entry_id: Identifier of the run entry.  


    **Returns:**
    > Dict with run metadata fields.  

??? abstract "check_for_updates(self) → dict[str, bool]"
    Check for updated runs in the database.


    **Returns:**
    > Dict mapping entry IDs to whether they have been updated.  

??? abstract "reload_entry(self, entry_id: str) → None"
    Re-query a specific run from the database.


    **Args:**
    > entry_id: Identifier of the entry to reload.  

??? abstract "get_iteration_labels(self, entry_id: str) → list[dict]"
    Return per-iteration metadata for x-axis labeling.


    **Args:**
    > entry_id: Identifier of the run entry.  


    **Returns:**
    > List of dicts with iteration metadata keys.  

??? abstract "remove_entry(self, entry_id: str) → None"
    Remove a run entry from the database.


    **Args:**
    > entry_id: Identifier of the entry to remove.  

??? abstract "close(self) → None"
    Close the database connection and release resources.

