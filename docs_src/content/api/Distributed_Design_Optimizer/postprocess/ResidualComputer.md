---
title: ResidualComputer
---

← Back to [postprocess](index.md)

# ResidualComputer

**Source:** [Distributed_Design_Optimizer\postprocess\ResidualComputer.py](ResidualComputer_source.md)

Residual computation module.

This module provides functionality for computing residuals
in distributed optimization problems.

## Classes

### ResidualComputer

> Computes residuals for edges in the master graph using coupling data from MiddleLevelDataStorageInterface objects.

> This class creates a bridge between the coupling data stored in MiddleLevelDataStorageInterface
> objects and the graph structure in GraphInit, computing and storing residuals
> as edge attributes in the master graph.

#### Methods

??? abstract "__init__(self, graph_init: [GraphInit](GraphInit.md#graphinit), middlelevel_storages: List[[MiddleLevelDataStorageInterface](../middlelevel/MiddleLevelDataStorageInterface.md#middleleveldatastorageinterface)], subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)], iterationscheme: [IterationSchemeInterface](../coordination/innerloop_iterationscheme/IterationSchemeInterface.md#iterationschemeinterface))"
    Initialize the residual computer.


    **Args:**
    > graph_init: The graph initialization object containing the master graph.  
    > middlelevel_storages: List of all MiddleLevelDataStorageInterface objects.  
    > subsystems: List of subsystems in the system.  
    > iterationscheme: The iteration scheme used for coordination.  

??? abstract "create_storage_lookup(self) → None"
    Create a lookup dictionary for MiddleLevelDataStorageInterface objects.

??? abstract "create_subsystem_lookup(self) → None"
    Create a lookup dictionary for Subsystems objects.

??? abstract "compute_all_primal_residuals(self) → None"
    Compute primal residuals for all edges in the master graph.

??? abstract "compute_single_primal_residual(self, idparent: str, idchild: str, edge_type: str) → None"
    Compute primal residual for a single edge.


    **Args:**
    > idparent: Parent node ID.  
    > idchild: Child node ID.  
    > edge_type: Type of edge.  

??? abstract "calculate_primal_residual_by_type(self, parent_coupling: [MiddleLevelCouplingInterface](../middlelevel/MiddleLevelCouplingInterface.md#middlelevelcouplinginterface), child_coupling: [MiddleLevelCouplingInterface](../middlelevel/MiddleLevelCouplingInterface.md#middlelevelcouplinginterface), edge_type: str) → List[float] | None"
    Calculate primal residual values based on edge type.


    **Args:**
    > parent_coupling: MiddleLevelCouplingInterface object for parent.  
    > child_coupling: MiddleLevelCouplingInterface object for child.  
    > edge_type: Type of edge.  


    **Returns:**
    > Computed residual values or None if computation fails.  

??? abstract "compute_all_dual_residuals(self, convinnerloop: bool) → None"
    Compute dual residuals for all edges in the master graph.


    **Args:**
    > convinnerloop: Whether the inner loop has converged.  

??? abstract "compute_single_dual_residual(self, idparent: str, idchild: str, edge_type: str, convinnerloop: bool) → None"
    Compute dual residual for a single edge.


    **Args:**
    > idparent: Parent node ID.  
    > idchild: Child node ID.  
    > edge_type: Type of edge.  
    > convinnerloop: Whether the inner loop has converged.  

??? abstract "determine_DualResidualtype(self, parent_subsystem: [SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface), child_subsystem: [SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)) → str"
    Determine the type of ADMM residual computation based on level and execution.


    **Args:**
    > parent_subsystem: The parent subsystem.  
    > child_subsystem: The child subsystem.  


    **Returns:**
    > The residual definition type string.  

??? abstract "calculate_dual_residual_by_type(self, parent_subsystem: [SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface), child_subsystem: [SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface), idparent: str, idchild: str, edge_type: str, convinnerloop: bool) → List[float | None] | None"
    Calculate dual residual values based on edge type.


    **Args:**
    > parent_subsystem: The parent subsystem.  
    > child_subsystem: The child subsystem.  
    > idparent: Parent node ID.  
    > idchild: Child node ID.  
    > edge_type: Type of edge.  
    > convinnerloop: Whether the inner loop has converged.  


    **Returns:**
    > Computed residual values or None.  

??? abstract "compute_ParentFirstChildSecondMappedDualResidual(self, parent_subsystem: [SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface), child_subsystem: [SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface), idparent: str, idchild: str, convinnerloop: bool) → List[float | None]"
    Compute dual residual for parent-first child-second mapped response edge.


    **Args:**
    > parent_subsystem: The parent subsystem.  
    > child_subsystem: The child subsystem.  
    > idparent: Parent node ID.  
    > idchild: Child node ID.  
    > convinnerloop: Whether the inner loop has converged.  


    **Returns:**
    > The computed dual residual values.  

??? abstract "compute_ChildFirstParentSecondMappedDualResidual(self, parent_subsystem: [SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface), child_subsystem: [SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface), idparent: str, idchild: str, convinnerloop: bool) → List[float | None]"
    Compute dual residual for child-first parent-second mapped response edge.


    **Args:**
    > parent_subsystem: The parent subsystem.  
    > child_subsystem: The child subsystem.  
    > idparent: Parent node ID.  
    > idchild: Child node ID.  
    > convinnerloop: Whether the inner loop has converged.  


    **Returns:**
    > The computed dual residual values.  

??? abstract "compute_ParentChildParallelMappedDualResidual(self, parent_subsystem: [SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface), child_subsystem: [SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface), idparent: str, idchild: str, convinnerloop: bool) → List[float | None]"
    Compute dual residual for parallel parent-child mapped response edge.


    **Args:**
    > parent_subsystem: The parent subsystem.  
    > child_subsystem: The child subsystem.  
    > idparent: Parent node ID.  
    > idchild: Child node ID.  
    > convinnerloop: Whether the inner loop has converged.  


    **Returns:**
    > The computed dual residual values.  

??? abstract "compute_ParentFirstChildSecondSharedDualResidual(self, parent_subsystem: [SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface), child_subsystem: [SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface), idparent: str, idchild: str, convinnerloop: bool) → List[float | None]"
    Compute dual residual for parent-first child-second shared design variable edge.


    **Args:**
    > parent_subsystem: The parent subsystem.  
    > child_subsystem: The child subsystem.  
    > idparent: Parent node ID.  
    > idchild: Child node ID.  
    > convinnerloop: Whether the inner loop has converged.  


    **Returns:**
    > The computed dual residual values.  

??? abstract "compute_ChildFirstParentSecondSharedDualResidual(self, parent_subsystem: [SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface), child_subsystem: [SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface), idparent: str, idchild: str, convinnerloop: bool) → List[float | None]"
    Compute dual residual for child-first parent-second shared design variable edge.


    **Args:**
    > parent_subsystem: The parent subsystem.  
    > child_subsystem: The child subsystem.  
    > idparent: Parent node ID.  
    > idchild: Child node ID.  
    > convinnerloop: Whether the inner loop has converged.  


    **Returns:**
    > The computed dual residual values.  

??? abstract "compute_ParentChildParallelSharedDualResidual(self, parent_subsystem: [SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface), child_subsystem: [SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface), idparent: str, idchild: str, convinnerloop: bool) → List[float | None]"
    Compute dual residual for parallel parent-child shared design variable edge.


    **Args:**
    > parent_subsystem: The parent subsystem.  
    > child_subsystem: The child subsystem.  
    > idparent: Parent node ID.  
    > idchild: Child node ID.  
    > convinnerloop: Whether the inner loop has converged.  


    **Returns:**
    > The computed dual residual values.  

??? abstract "compute_residual_for_edge(self, idparent: str, idchild: str, edge_type: str, residual_type: str) → None"
    Compute residual for a specific edge on demand.


    **Args:**
    > idparent: Parent node ID.  
    > idchild: Child node ID.  
    > edge_type: Type of edge.  
    > residual_type: Type of residual to compute ('primal' or 'dual').  

??? abstract "get_residual_summary(self) → dict"
    Get a comprehensive summary of computed residuals.


    **Returns:**
    > Summary statistics including counts, max values, and formatted output.  

??? abstract "visualize_graph(self) → None"
    Visualize the master graph using PyVis inside a GUI window.

