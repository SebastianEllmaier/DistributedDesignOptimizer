---
title: TopologyHandler
---

← Back to [handlers](index.md)

# TopologyHandler

**Source:** [Distributed_Design_Optimizer\postprocess\handlers\TopologyHandler.py](TopologyHandler_source.md)

Topology analysis handler — orchestrates analysis and emits results.

Static analyses delegate to _static_graph_builder.
Dynamic analyses delegate to _dynamic_builder.

## Classes

### TopologyHandler

> **Inherits from:** `QObject`

> Runs topology analyses and produces native rendering data.

#### Methods

??? abstract "__init__(self, parent: QObject | None) → None"
    Initialize the topology handler.


    **Args:**
    > parent: Optional parent QObject for Qt ownership.  

??? abstract "run_analysis(self, dill_data: deque, config: [AnalysisConfig](../models/AnalysisConfig.md#analysisconfig), filename: str) → None"
    Run the specified topology analysis in a background thread.


    **Args:**
    > dill_data: Deque of iteration data loaded from a dill history file.  
    > config: Analysis configuration specifying type and mode.  
    > filename: Name of the source dill file for labeling.  

??? abstract "cancel(self) → None"
    Cancel any running topology analysis worker.

??? abstract "validate_coordinator_file(self, metadata: dict) → bool"
    Check if the entry is a coordinator-type dill file.


    **Args:**
    > metadata: File metadata dictionary from the file registry.  


    **Returns:**
    > True if the file is a coordinator dill file, False otherwise.  

