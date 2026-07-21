---
title: LocalSubSystemHistoryEntry
---

← Back to [historyentry](index.md)

# LocalSubSystemHistoryEntry

**Source:** [Distributed_Design_Optimizer\subsystem\historyentry\LocalSubSystemHistoryEntry.py](LocalSubSystemHistoryEntry_source.md)

Local subsystem history entry module.

This module provides the history log entry for a local subsystem, extending the
subsystem history entry with scaler and inconsistency snapshots.

## Classes

### LocalSubSystemHistoryEntry

> **Inherits from:** [SubSystemHistoryEntry](SubSystemHistoryEntry.md#subsystemhistoryentry)

> History log entry for a local subsystem.

> Extends SubSystemHistoryEntry with the scalers, inconsistencies and maximum
> inconsistency information that only exist for local subsystems.

#### Methods

??? abstract "__init__(self, subsystem_id: str, outerloop_itr: int, innerloop_itr: int, innerloop_itr_runtime: float | None, innerloop_itr_numberofdesignvariableevaluations: int | None, optimdata: [LocalSubSystemOptimData](../optimization/optimizerdata/LocalSubSystemOptimData.md#localsubsystemoptimdata), convinnerloop: bool, convouterloop: bool, scalers: List[[ScalerBasis](../tools/ScalerBasis.md#scalerbasis)], inconsistencies: List[[InConsistencySizeInterface](../../middlelevel/InConsistencySizeInterface.md#inconsistencysizeinterface)], maxinconsistencyvalue: float | None, maxinconsistencysubsystemID: str | None) → None"
    Create a new LocalSubSystemHistoryEntry.


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
    > scalers: Snapshot of the subsystem's scalers.  
    > inconsistencies: Snapshot of the subsystem's inconsistencies.  
    > maxinconsistencyvalue: Maximum inconsistency value of this snapshot.  
    > maxinconsistencysubsystemID: Identifier of the coupled subsystem with  
    > the maximum inconsistency.  

??? abstract "get_OptimData(self) → [LocalSubSystemOptimData](../optimization/optimizerdata/LocalSubSystemOptimData.md#localsubsystemoptimdata)"
    Return the snapshot of the subsystem's optimization data.


    **Returns:**
    > The local subsystem optimization data of this snapshot.  

??? abstract "get_Scalers(self) → List[[ScalerBasis](../tools/ScalerBasis.md#scalerbasis)]"
    Return the snapshot of the subsystem's scalers.


    **Returns:**
    > The list of scalers of this snapshot.  

??? abstract "get_Inconsistencies(self) → List[[InConsistencySizeInterface](../../middlelevel/InConsistencySizeInterface.md#inconsistencysizeinterface)]"
    Return the snapshot of the subsystem's inconsistencies.


    **Returns:**
    > The list of inconsistencies of this snapshot.  

??? abstract "get_maxInconsistencyValue(self) → float | None"
    Return the maximum inconsistency value of this snapshot.


    **Returns:**
    > The maximum inconsistency value, or None if not set.  

??? abstract "get_MaxInconsistencyCoupledSubsystemID(self) → str | None"
    Return the coupled subsystem identifier with the maximum inconsistency.


    **Returns:**
    > The coupled subsystem identifier, or None if not set.  

