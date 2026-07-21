---
title: _topology_dispatch
---

← Back to [handlers](index.md)

# _topology_dispatch

**Source:** [Distributed_Design_Optimizer\postprocess\handlers\_topology_dispatch.py](_topology_dispatch_source.md)

Unified dispatch registry for topology analyses.

Maps (analysis_type, mode) to (builder_function, output_type) so that
TopologyHandler doesn't need to branch on mode itself.

## Functions

??? abstract "resolve(analysis: str, mode: str)"
    Return (build_fn, output_type) for the given analysis/mode pair.


    **Args:**
    > analysis: Analysis type key (e.g. "master_graph", "clustering").  
    > mode: Either "static" or "dynamic".  


    **Raises:**
    > ValueError: If the combination is unknown.  

