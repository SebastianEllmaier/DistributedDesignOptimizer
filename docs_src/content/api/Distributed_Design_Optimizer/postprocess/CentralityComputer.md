---
title: CentralityComputer
---

← Back to [postprocess](index.md)

# CentralityComputer

**Source:** [Distributed_Design_Optimizer\postprocess\CentralityComputer.py](CentralityComputer_source.md)

Centrality computation module for graph analysis.

This module provides functionality for computing centrality metrics
in the coupling graph of distributed optimization problems.

## Classes

### CentralityComputer

> Computes the Centrality Measures for the master graph.

> The Degree Centrality and Page Rank measure is computed for the master graph with primal residuals as the edge weights
> Here the Master Graph (Multi Directed Graph) is preprocessed into a Directed Graph with aggregated Primal Residual Values
> From each edge, Max Inconsistency Value is considered and weights from two directed parallel edges are merged into a single with edge weights summed.
> The Centrality values and pagerank measures are stored in the Master graph Node

#### Methods

??? abstract "__init__(self, graph_init: [GraphInit](GraphInit.md#graphinit), subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)])"
    Compute the centrality measures of the graph.


    **Args:**
    > graph_init: The initialized graph object.  
    > subsystems: List of subsystems in the system.  

??? abstract "create_subsystem_lookup(self) → None"
    Create a lookup dictionary for Subsystems objects.


??? abstract "compute_EdgeWeights(self) → None"
    Centrality Measures are based on the inconsistencies. L infinity Norm is considered for the Centrality Measurement analysis.


??? abstract "compute_single_EdgeWeight(self, idparent: str, idchild: str, key: object, edge_type: str) → None"
    Compute the edge weight for a single edge based on inconsistency values.


    **Args:**
    > idparent: Identifier of the parent node.  
    > idchild: Identifier of the child node.  
    > key: The edge key in the multigraph.  
    > edge_type: The type of edge (decomposed_mappedresponse or decomposed_shareddesignvariable).  

??? abstract "compute_CentralityMeasures(self) → None"
    Compute Centrality Measures for all nodes in the master graph.

    Computes Degree Centrality Measures and EigenVector

??? abstract "get_centrality_summary(self) → Dict"
    Get a comprehensive summary of computed centrality measures.


    **Returns:**
    > dict: Summary of centrality measures for all nodes and edges  

??? abstract "visualize_pagerank(self, filename: str, height: str, width: str) → None"
    Create an interactive visualization of the graph with nodes sized by PageRank.


    **Args:**
    > filename: Name of the HTML file to save the visualization.  
    > height: Height of the visualization.  
    > width: Width of the visualization.  

??? abstract "interpret_static_WeightedInDegree_centrality() → list"
    Return formatted interpretation text for Static Weighted In-Degree Centrality.


    **Returns:**
    > List of tuples containing text, style tag, and phrases to bold.  

??? abstract "interpret_dynamic_WeightedInDegree_centrality() → list"
    Return formatted interpretation text for Dynamic Weighted In-Degree Centrality.


    **Returns:**
    > List of tuples containing text, style tag, and phrases to bold.  

??? abstract "interpret_static_WeightedOutDegree_centrality() → list"
    Return formatted interpretation text for Static Weighted Out-Degree Centrality.


    **Returns:**
    > List of tuples containing text, style tag, and phrases to bold.  

??? abstract "interpret_dynamic_WeightedOutDegree_centrality() → list"
    Return formatted interpretation text for Dynamic Weighted Out-Degree Centrality.


    **Returns:**
    > List of tuples containing text, style tag, and phrases to bold.  

??? abstract "interpret_static_PageRank() → list"
    Return formatted interpretation text for Static PageRank Centrality.


    **Returns:**
    > List of tuples containing text, style tag, and phrases to bold.  

??? abstract "interpret_dynamic_PageRank() → list"
    Return formatted interpretation text for Dynamic PageRank Centrality.


    **Returns:**
    > List of tuples containing text, style tag, and phrases to bold.  

