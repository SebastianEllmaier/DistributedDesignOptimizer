---
title: GraphInit
---

← Back to [postprocess](index.md)

# GraphInit

**Source:** [Distributed_Design_Optimizer\postprocess\GraphInit.py](GraphInit_source.md)

Graph initialization module.

This module provides functionality for initializing and managing
graph data structures for distributed optimization analysis.

## Classes

### GraphInit

> Main class for creating and managing a distributed design optimizer graph.

> This class provides methods to build, manipulate, and visualize graphs representing
> coupling relationships between subsystems in distributed design optimization problems.

#### Methods

??? abstract "__init__(self)"
    Initialize the GraphInit with an empty MultiDiGraph.

??? abstract "set_MasterGraph(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)], visualize: bool) → nx.MultiDiGraph"
    Build the complete graph from SubSystemInterface list.


    **Args:**
    > subsystems: List of SubSystemInterface objects containing subsystem information.  
    > visualize: Whether to display the graph visualization.  


    **Returns:**
    > The constructed graph.  

??? abstract "add_edge_with_attributes(self, idparent: str, idchild: str, edge_type: str) → None"
    Add an edge with all the attributes from the original Edges class.


    **Args:**
    > idparent: Parent node ID.  
    > idchild: Child node ID.  
    > edge_type: Type of edge (must be unique between any pair of nodes).  


    **Raises:**
    > ValueError: If an edge with the same type already exists between the nodes.  

??? abstract "set_vertices(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Add vertices (nodes) to the graph.


    **Args:**
    > subsystems: List of SubSystemInterface objects containing subsystem information.  

??? abstract "set_edges(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Set edges based on coupling relationships.


    **Args:**
    > subsystems: List of SubSystemInterface objects containing coupling information.  

??? abstract "store_primalresidual(self, idparent: str, idchild: str, edge_type: str, residual_values: List[float] | None) → None"
    Store primal residual for a specific edge identified by type.


    **Args:**
    > idparent: Parent node ID.  
    > idchild: Child node ID.  
    > edge_type: Type of edge to find.  
    > residual_values: List of residual values to store.  

??? abstract "store_dualresidual(self, idparent: str, idchild: str, edge_type: str, residual_values: List[float | None] | None) → None"
    Store the aggregated dual residual for a specific edge identified by type.


    **Args:**
    > idparent: Parent node ID.  
    > idchild: Child node ID.  
    > edge_type: Type of edge to find.  
    > residual_values: List of residual values to store.  

??? abstract "store_NodeCentrality(self, node_id: str, in_degree_value: float, out_degree_value: float, weightedInDegree_value: float, weightedOutDegree_value: float, weighteddegree_centrality: float | None, pagerank_centrality: float | None) → None"
    Store the Centrality Values for a specific Node.


    **Args:**
    > node_id: Node identifier.  
    > in_degree_value: In-degree centrality value.  
    > out_degree_value: Out-degree centrality value.  
    > weightedInDegree_value: Weighted in-degree centrality value.  
    > weightedOutDegree_value: Weighted out-degree centrality value.  
    > weighteddegree_centrality: Weighted degree centrality value.  
    > pagerank_centrality: PageRank centrality value.  

??? abstract "store_NodeCluster(self, node_id: str, cluster_id: int) → None"
    Store the cluster assignment for a specific node.


    **Args:**
    > node_id: Node identifier.  
    > cluster_id: Assigned cluster ID.  

??? abstract "store_InConsistencyOscillationIndex(self, idparent: str, idchild: str, edge_type: str, oscillation_data: Dict) → None"
    Store the inconsistency oscillation index data for a specific edge identified by type.


    **Args:**
    > idparent: Parent node ID.  
    > idchild: Child node ID.  
    > edge_type: Type of edge to find.  
    > oscillation_data: Dictionary containing oscillation index values.  

??? abstract "compute_couplingstrength(self, idparent: str, idchild: str, edge_type: str) → None"
    Compute coupling strength for a specific edge identified by type.


    **Args:**
    > idparent: Parent node ID.  
    > idchild: Child node ID.  
    > edge_type: Type of edge to find.  

??? abstract "get_edge_attributes(self, idparent: str, idchild: str, edge_type: str) → Dict | None"
    Get all attributes for a specific edge identified by type.


    **Args:**
    > idparent: Parent node ID.  
    > idchild: Child node ID.  
    > edge_type: Type of edge to find.  


    **Returns:**
    > Edge attributes dictionary or None if edge not found.  

??? abstract "get_graph(self) → nx.MultiDiGraph"
    Return the NetworkX graph.


    **Returns:**
    > The internal graph object.  

??? abstract "visualize_graph(self, title: str, figsize: tuple, save_path: str, interactive: bool) → None"
    Visualize the directed multigraph using the GraphVisualizer class.


    **Args:**
    > title: Title for the plot.  
    > figsize: Figure size (width, height). If None, auto-calculated based on node count.  
    > save_path: Optional path to save the figure.  
    > interactive: Whether to enable interactive hover tooltips.  

??? abstract "print_edge_verification(self) → None"
    Print edge list for verification purposes - shows idparent, idchild, and type.

??? abstract "main(subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → nx.MultiDiGraph"
    Main method to create and return a graph.


    **Args:**
    > subsystems: List of SubSystemInterface objects.  


    **Returns:**
    > The constructed graph.  

