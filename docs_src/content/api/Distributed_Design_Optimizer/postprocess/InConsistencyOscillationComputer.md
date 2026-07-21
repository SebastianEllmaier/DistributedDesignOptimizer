---
title: InConsistencyOscillationComputer
---

← Back to [postprocess](index.md)

# InConsistencyOscillationComputer

**Source:** [Distributed_Design_Optimizer\postprocess\InConsistencyOscillationComputer.py](InConsistencyOscillationComputer_source.md)

InConsistency oscillation computation module.

This module provides functionality for computing and analyzing oscillations
in inconsistencies during distributed optimization.

## Classes

### InConsistencyOscillationComputer

> InConsistencyOscillationComputer computes the oscillation energy to understand the behaviour of Inconsistency Convergence.
> Oscillation Energy is computed through Wavelet Transformation which studies the Inconsistency through frequency domain.
> InConsistencyOscillation Metrics values are computed once the enough data (horizon) is attained.

#### Methods

??? abstract "__init__(self, graph_init: [GraphInit](GraphInit.md#graphinit), subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)])"
    Initialize the InConsistencyOscillationComputer.


    **Args:**
    > graph_init: GraphInit object containing the master graph.  
    > subsystems: List of SubSystemInterface objects.  

??? abstract "create_subsystem_lookup(self) → None"
    Create a lookup dictionary for Subsystems objects.


??? abstract "get_Horizon(self) → int"
    Get the horizon value for wavelet transform.


    **Returns:**
    > The number of previous values to use.  

??? abstract "set_Horizon(self, horizon: int) → None"
    Set the number of previous values to use for wavelet transform.


    **Args:**
    > horizon: The number of previous values to use.  

??? abstract "compute_wavelet_transforms(self, all_history_entries: List[dict] | None) → None"
    Compute wavelet transforms for all edges in the master graph.


    **Args:**
    > all_history_entries: List of history entries containing residual data, or None.  

??? abstract "compute_EdgeResidualHistory(self, all_primalresidual_history: List[dict], k: int, edge_id: str, edge_type: str) → List | None"
    Return the edge primal residual history for a specific edge and type.


    **Args:**
    > all_primalresidual_history: List of history entries containing residual data.  
    > k: Number of previous values required.  
    > edge_id: Edge identifier in format "idparent-idchild".  
    > edge_type: Type of edge.  


    **Returns:**
    > List of primal residual values for the specified edge, or None if not enough data.  

??? abstract "get_InConsistencyOscillationIndex_summary(self) → Dict"
    Get a simplified summary of computed oscillation indices.


    **Returns:**
    > Summary of oscillation indices for all edges in a flat structure.  

??? abstract "interpret_InConsistencyOscillationMetric(self) → list"
    Return formatted interpretation text for the InConsistency Oscillation Metric.


    **Returns:**
    > List of tuples containing text, style tag, and phrases to bold.  

