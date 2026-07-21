---
title: SubSystemHistoryEntry
---

← Back to [historyentry](index.md)

# SubSystemHistoryEntry

**Source:** [Distributed_Design_Optimizer\subsystem\historyentry\SubSystemHistoryEntry.py](SubSystemHistoryEntry_source.md)

Subsystem history entry module.

This module provides the base class for a single subsystem history log entry,
shared by local subsystems and the controller subsystem.

## Classes

### SubSystemHistoryEntry

> **Inherits from:** [HistoryEntry](HistoryEntry.md#historyentry)

> Base class for a single subsystem history log entry.

> Extends HistoryEntry with the state common to every subsystem snapshot
> (identifier, optimization data and convergence flags).

#### Methods

??? abstract "__init__(self, subsystem_id: str, outerloop_itr: int, innerloop_itr: int, innerloop_itr_runtime: float | None, innerloop_itr_numberofdesignvariableevaluations: int | None, optimdata: [OptimDataBasis](../optimization/optimizerdata/OptimDataBasis.md#optimdatabasis), convinnerloop: bool, convouterloop: bool) → None"
    Create a new SubSystemHistoryEntry.


    **Args:**
    > subsystem_id: Identifier of the subsystem this snapshot belongs to.  
    > outerloop_itr: Outer loop iteration number of this snapshot.  
    > innerloop_itr: Inner loop iteration number of this snapshot.  
    > innerloop_itr_runtime: Runtime of the inner loop iteration.  
    > innerloop_itr_numberofdesignvariableevaluations: Number of design  
    > variable evaluations of the inner loop iteration.  
    > optimdata: Snapshot of the subsystem's optimization data.  
    > convinnerloop: Inner loop convergence flag.  
    > convouterloop: Outer loop convergence flag.  

??? abstract "get_SUBSYSTEMID(self) → str"
    Return the identifier of the subsystem this snapshot belongs to.


    **Returns:**
    > The subsystem identifier.  

??? abstract "get_OptimData(self) → [OptimDataBasis](../optimization/optimizerdata/OptimDataBasis.md#optimdatabasis)"
    Return the snapshot of the subsystem's optimization data.


    **Returns:**
    > The optimization data of this snapshot.  

??? abstract "get_ConvInnerLoop(self) → bool"
    Return the inner loop convergence flag of this snapshot.


    **Returns:**
    > True if the subsystem was inner loop converged, False otherwise.  

??? abstract "get_ConvOuterLoop(self) → bool"
    Return the outer loop convergence flag of this snapshot.


    **Returns:**
    > True if the subsystem was outer loop converged, False otherwise.  

