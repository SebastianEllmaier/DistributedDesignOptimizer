---
title: AutoUpdateWorker
---

← Back to [workers](index.md)

# AutoUpdateWorker

**Source:** [Distributed_Design_Optimizer\postprocess\workers\AutoUpdateWorker.py](AutoUpdateWorker_source.md)

Background worker for periodic file-modification checks.

## Classes

### AutoUpdateWorker

> **Inherits from:** `QThread`

> Periodically checks the data source for file modifications.

#### Methods

??? abstract "__init__(self, source: [DataSource](../models/DataSource.md#datasource), interval_ms: int, parent: QObject | None) → None"
    Initialize the auto-update worker.


    **Args:**
    > source: The data source to monitor for changes.  
    > interval_ms: Polling interval in milliseconds.  
    > parent: Optional parent QObject.  

??? abstract "run(self) → None"
    Poll the data source for updates at the configured interval.

??? abstract "stop(self) → None"
    Request graceful stop.

