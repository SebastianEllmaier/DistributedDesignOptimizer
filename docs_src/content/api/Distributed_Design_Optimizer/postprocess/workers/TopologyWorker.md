---
title: TopologyWorker
---

← Back to [workers](index.md)

# TopologyWorker

**Source:** [Distributed_Design_Optimizer\postprocess\workers\TopologyWorker.py](TopologyWorker_source.md)

Background worker for topology analysis computations.

## Classes

### TopologyWorker

> **Inherits from:** [CallableWorker](CallableWorker.md#callableworker)

> Background worker for topology analysis computation.

#### Methods

??? abstract "__init__(self, build_fn, args: tuple, label: str, context_data: dict, output_type: str, parent) → None"
    Initialize the topology worker.


    **Args:**
    > build_fn: Callable that produces the topology result.  
    > args: Positional arguments for the build function.  
    > label: Display label for the result.  
    > context_data: Additional context passed through to signals.  
    > output_type: Result kind - ``"graph"``, ``"chart"``, or ``"html"``.  
    > parent: Optional parent QObject.  

