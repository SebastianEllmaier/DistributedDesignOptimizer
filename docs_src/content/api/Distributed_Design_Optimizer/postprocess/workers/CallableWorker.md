---
title: CallableWorker
---

← Back to [workers](index.md)

# CallableWorker

**Source:** [Distributed_Design_Optimizer\postprocess\workers\CallableWorker.py](CallableWorker_source.md)

Base class for simple background workers that run a callable and emit results.

## Classes

### CallableWorker

> **Inherits from:** `QThread`

> Generic background worker that invokes a callable and emits the result.

> Subclasses override `_handle_result` to route the return value
> to their typed signals.

#### Methods

??? abstract "__init__(self, fn, args: tuple, parent: QObject | None) → None"
    Initialize the callable worker.


    **Args:**
    > fn: The callable to execute in the background thread.  
    > args: Positional arguments to pass to the callable.  
    > parent: Optional parent QObject.  

??? abstract "run(self) → None"
    Execute the callable and route the result or emit an error.

