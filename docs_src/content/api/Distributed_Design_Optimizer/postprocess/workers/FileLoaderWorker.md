---
title: FileLoaderWorker
---

← Back to [workers](index.md)

# FileLoaderWorker

**Source:** [Distributed_Design_Optimizer\postprocess\workers\FileLoaderWorker.py](FileLoaderWorker_source.md)

Background worker for loading .dill history files.

## Classes

### FileLoaderWorker

> **Inherits from:** `QThread`

> Background worker that loads .dill files without blocking the UI.

#### Methods

??? abstract "__init__(self, source: [DataSource](../models/DataSource.md#datasource), file_paths: list[str], parent: QObject | None) → None"
    Initialize the file loader worker.


    **Args:**
    > source: The data source that handles deserialization.  
    > file_paths: List of file paths to load.  
    > parent: Optional parent QObject.  

??? abstract "run(self) → None"
    Load each file, emitting progress and results as signals.

