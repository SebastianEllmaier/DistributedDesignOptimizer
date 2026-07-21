---
title: ControllerSubSystemHistoryEntry
---

← Back to [historyentry](index.md)

# ControllerSubSystemHistoryEntry

**Source:** [Distributed_Design_Optimizer\subsystem\historyentry\ControllerSubSystemHistoryEntry.py](ControllerSubSystemHistoryEntry_source.md)

Controller subsystem history entry module.

This module provides the history log entry for the controller subsystem. The
controller holds the shared subsystem state only (no scalers or inconsistencies).

## Classes

### ControllerSubSystemHistoryEntry

> **Inherits from:** [SubSystemHistoryEntry](SubSystemHistoryEntry.md#subsystemhistoryentry)

> History log entry for the controller subsystem.

> Carries the same fields as SubSystemHistoryEntry; the dedicated type keeps
> the controller optimization data type explicit and distinguishes controller
> snapshots from local subsystem snapshots.

#### Methods

??? abstract "__init__(self, subsystem_id: str, outerloop_itr: int, innerloop_itr: int, innerloop_itr_runtime: float | None, innerloop_itr_numberofdesignvariableevaluations: int | None, optimdata: [ControllerOptimData](../optimization/optimizerdata/ControllerOptimData.md#controlleroptimdata), convinnerloop: bool, convouterloop: bool) → None"
    Create a new ControllerSubSystemHistoryEntry.


    **Args:**
    > subsystem_id: Identifier of the controller subsystem.  
    > outerloop_itr: Outer loop iteration number of this snapshot.  
    > innerloop_itr: Inner loop iteration number of this snapshot.  
    > innerloop_itr_runtime: Runtime of the inner loop iteration.  
    > innerloop_itr_numberofdesignvariableevaluations: Number of design  
    > variable evaluations of the inner loop iteration.  
    > optimdata: Snapshot of the controller's optimization data.  
    > convinnerloop: Inner loop convergence flag.  
    > convouterloop: Outer loop convergence flag.  

??? abstract "get_OptimData(self) → [ControllerOptimData](../optimization/optimizerdata/ControllerOptimData.md#controlleroptimdata)"
    Return the snapshot of the controller's optimization data.


    **Returns:**
    > The controller optimization data of this snapshot.  

