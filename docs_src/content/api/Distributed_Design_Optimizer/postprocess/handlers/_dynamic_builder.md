---
title: _dynamic_builder
---

← Back to [handlers](index.md)

# _dynamic_builder

**Source:** [Distributed_Design_Optimizer\postprocess\handlers\_dynamic_builder.py](_dynamic_builder_source.md)

Dynamic HTML builders for topology analysis.

## Functions

??? abstract "build_dynamic_html(dill_data: deque, analysis: str, filename: str) → str"
    Build interactive Plotly HTML for dynamic analyses.


    **Args:**
    > dill_data: Deque of per-iteration dicts loaded from a dill history file.  
    > analysis: Analysis type key (e.g. "clustering", "pagerank").  
    > filename: Original filename used in the plot title.  


    **Returns:**
    > Full HTML string containing the interactive Plotly visualisation.  

