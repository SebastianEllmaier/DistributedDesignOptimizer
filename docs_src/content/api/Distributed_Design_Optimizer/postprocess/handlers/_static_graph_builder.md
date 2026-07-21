---
title: _static_graph_builder
---

← Back to [handlers](index.md)

# _static_graph_builder

**Source:** [Distributed_Design_Optimizer\postprocess\handlers\_static_graph_builder.py](_static_graph_builder_source.md)

Static graph builders — produce graph_data dicts for GraphWidget rendering.

## Functions

??? abstract "build_static_graph(dill_data: deque, analysis: str, filename: str) → dict"
    Build a graph_data dict for QGraphicsView rendering.


    **Args:**
    > dill_data: Deque of iteration-data dicts loaded from a dill history file.  
    > analysis: Analysis type key (e.g. "master_graph", "clustering").  
    > filename: Display name for the graph title.  


    **Returns:**
    > Dict with "nodes", "edges", and "title" keys for rendering.  

