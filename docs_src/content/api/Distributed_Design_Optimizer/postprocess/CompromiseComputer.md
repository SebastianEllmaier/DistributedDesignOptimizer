---
title: CompromiseComputer
---

← Back to [postprocess](index.md)

# CompromiseComputer

**Source:** [Distributed_Design_Optimizer\postprocess\CompromiseComputer.py](CompromiseComputer_source.md)

Compromise computation module for optimization analysis.

This module provides functionality for computing compromise metrics
in distributed optimization problems.

## Classes

### CompromiseComputer

> CompromiseComputer computes the compromise metrics defined.
> Compromise metrics gives an idea how much the coupling variables moved from the intial points
> CompromiseComputer iterates through each edge of the Multi Di Graph and computes the compromise depending on the edge type
> Compromisee metrics are stored on the edges of the Master Graph

#### Methods

??? abstract "__init__(self, graph_init: [GraphInit](GraphInit.md#graphinit), subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)], middlelevel_storages: List[[MiddleLevelDataStorageInterface](../middlelevel/MiddleLevelDataStorageInterface.md#middleleveldatastorageinterface)])"
    Initialize the compromise computer.


    **Args:**
    > graph_init: The graph initialization object.  
    > subsystems: List of all SubSystemInterface objects.  
    > middlelevel_storages: List of all MiddleLevelDataStorageInterface objects.  

??? abstract "create_subsystem_lookup(self) → None"
    Create a lookup dictionary for Subsystems objects.


??? abstract "create_storage_lookup(self) → None"
    Create a lookup dictionary for MiddleLevelDataStorageInterface objects.

??? abstract "compute_all_compromises(self) → None"
    Compute the compromises of each edge in the graph.

??? abstract "compute_single_compromise(self, idparent: str, idchild: str, edge_type: str) → None"
    Compute compromise metric for a single edge.


    **Args:**
    > idparent: Parent node ID.  
    > idchild: Child node ID.  
    > edge_type: Type of edge.  

??? abstract "compute_mapped_response_compromise(self, idparent: str, idchild: str, edge_type: str, edge_key: int, parent_coupling: [MiddleLevelCouplingInterface](../middlelevel/MiddleLevelCouplingInterface.md#middlelevelcouplinginterface), child_coupling: [MiddleLevelCouplingInterface](../middlelevel/MiddleLevelCouplingInterface.md#middlelevelcouplinginterface), primal_residual: List[float]) → None"
    Compute compromise metrics for mapped response variables.


    **Args:**
    > idparent: Parent node ID.  
    > idchild: Child node ID.  
    > edge_type: Type of edge.  
    > edge_key: Edge key in the multigraph.  
    > parent_coupling: MiddleLevelCoupling object for parent.  
    > child_coupling: MiddleLevelCoupling object for child.  
    > primal_residual: List of primal residual values.  

??? abstract "compute_shared_design_compromise(self, idparent: str, idchild: str, edge_type: str, edge_key: int, parent_coupling: [MiddleLevelCouplingInterface](../middlelevel/MiddleLevelCouplingInterface.md#middlelevelcouplinginterface), child_coupling: [MiddleLevelCouplingInterface](../middlelevel/MiddleLevelCouplingInterface.md#middlelevelcouplinginterface), primal_residual: List[float]) → None"
    Compute compromise metrics for shared design variables.


    **Args:**
    > idparent: Parent node ID.  
    > idchild: Child node ID.  
    > edge_type: Type of edge.  
    > edge_key: Edge key in the multigraph.  
    > parent_coupling: MiddleLevelCoupling object for parent.  
    > child_coupling: MiddleLevelCoupling object for child.  
    > primal_residual: List of primal residual values.  

??? abstract "get_compromise_summary(self) → Dict"
    Get a comprehensive summary of computed compromise metrics.


    **Returns:**
    > dict: Summary of compromise metrics for all edges  

??? abstract "interpret_CompromiseRatio(self) → list"
    Return formatted interpretation text for the Compromise Ratio chart.


    **Returns:**
    > List of tuples containing text, style tag, and phrases to bold.  

