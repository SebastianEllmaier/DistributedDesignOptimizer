---
title: graph_utils
---

← Back to [utils](index.md)

# graph_utils

**Source:** [Distributed_Design_Optimizer\postprocess\utils\graph_utils.py](graph_utils_source.md)

Graph layout and color utility functions for topology analysis.

## Functions

??? abstract "hierarchical_layout(graph: nx.Graph, subsystem_details: dict) → dict[str, dict]"
    Compute hierarchical positions from subsystem level data.


    **Args:**
    > graph: The NetworkX graph whose nodes will be positioned.  
    > subsystem_details: Mapping of node id to detail dicts containing a ``Level`` key.  


    **Returns:**
    > A dict mapping node id to ``{"x": float, "y": float}`` position dicts.  

??? abstract "green_yellow_red(normalized: float) → str"
    Map 0..1 to a green-yellow-red hex color.


    **Args:**
    > normalized: A value in [0, 1] where 0 is green and 1 is red.  


    **Returns:**
    > A CSS hex color string interpolated along the green-yellow-red gradient.  

??? abstract "safe_edge_iter(graph: nx.Graph) → list"
    Iterate edges safely for both multi and non-multi graphs.


    **Args:**
    > graph: A NetworkX graph (regular or multigraph).  


    **Returns:**
    > A list of edge tuples, each containing ``(u, v, key)`` or  
    > ``(u, v, key, data)`` depending on the *data* flag.  

??? abstract "build_edges(graph: nx.Graph, positions: dict[str, dict], default_color: str | None) → list[dict]"
    Build an edge list with source/target coordinates for GraphWidget.


    **Args:**
    > graph: The NetworkX graph to extract edges from.  
    > positions: Mapping of node id to ``{"x": float, "y": float}`` dicts.  
    > default_color: Optional fallback CSS color for edges without a type.  


    **Returns:**
    > A list of dicts, each containing source/target coordinates, color,  
    > width, and tooltip for one edge.  

