---
title: ClusterComputer
---

← Back to [postprocess](index.md)

# ClusterComputer

**Source:** [Distributed_Design_Optimizer\postprocess\ClusterComputer.py](ClusterComputer_source.md)

Cluster computation module for graph analysis.

This module provides functionality for computing clusters in the
coupling graph of distributed optimization problems.

## Classes

### ClusterComputer

> Cluster Computer Performs Spectral Clustering Analysis on a Preprocessed Undirected Graph with aggregated Primal Residual as edge weight.

> Multi Di Graph is preprocessed into a undirected graph.

> Edges will have the max Inconsistency value as the edge weights.

> After analysis, the cluster id to which the node belongs to is stored in the Master Graph nodes

#### Methods

??? abstract "__init__(self, graph_init: [GraphInit](GraphInit.md#graphinit), subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)])"
    Initialize the cluster computer.


    **Args:**
    > graph_init: The initialized graph object.  
    > subsystems: List of subsystems in the system.  

??? abstract "create_subsystem_lookup(self) → None"
    Create a lookup dictionary for Subsystems objects.

??? abstract "preprocess_graph(self) → None"
    Preprocess the mastergraph into an undirected graph with appropriate weights.

    All different edges of the Master Graph is considered. Max Inconsistency Value of each edge is noted.

    If multiple edges (same or opposite directions) exists between two nodes, then it is aggregated into a single directed edge with max inconsistency value




    **Returns:**

    nx.Graph: Undirected graph with processed weights

??? abstract "perform_spectral_clustering(self) → None"
    Perform spectral clustering on the preprocessed graph.

    This method preprocesses the graph, computes spectral clustering,
    and stores the cluster assignments in the graph nodes.

??? abstract "get_cluster_summary(self) → Dict"
    Get a comprehensive summary of clustering results from the mastergraph.


    **Returns:**

    dict: Summary of cluster assignments for all nodes

??? abstract "interpret_static_ClusterAnalysis() → list"
    Return formatted interpretation text for Static Cluster Analysis.


    **Returns:**
    > List of tuples containing text, style tag, and phrases to bold.  

??? abstract "interpret_dynamic_ClusterAnalysis() → list"
    Return formatted interpretation text for Dynamic Cluster Analysis.


    **Returns:**
    > List of tuples containing text, style tag, and phrases to bold.  

