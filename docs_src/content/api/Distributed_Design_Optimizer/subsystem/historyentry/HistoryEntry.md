---
title: HistoryEntry
---

← Back to [historyentry](index.md)

# HistoryEntry

**Source:** [Distributed_Design_Optimizer\subsystem\historyentry\HistoryEntry.py](HistoryEntry_source.md)

History entry base module.

This module provides the neutral base class for a single history log entry.
An entry is a snapshot of selected state captured at one inner loop iteration.
It is shared by the subsystem history entries and the coordinator history entry.

## Classes

### HistoryEntry

> Base class for a single history log entry.

> Holds the iteration bookkeeping fields that are common to every producer
> of a history (both subsystems and the coordinator).

#### Methods

??? abstract "__init__(self, outerloop_itr: int, innerloop_itr: int, innerloop_itr_runtime: float | None, innerloop_itr_numberofdesignvariableevaluations: int | None) → None"
    Create a new HistoryEntry.


    **Args:**
    > outerloop_itr: Outer loop iteration number of this snapshot.  
    > innerloop_itr: Inner loop iteration number of this snapshot.  
    > innerloop_itr_runtime: Runtime of the inner loop iteration.  
    > innerloop_itr_numberofdesignvariableevaluations: Number of design  
    > variable evaluations of the inner loop iteration.  

??? abstract "get_OuterLoop_Itr(self) → int"
    Return the outer loop iteration number of this snapshot.


    **Returns:**
    > The outer loop iteration number.  

??? abstract "get_InnerLoop_Itr(self) → int"
    Return the inner loop iteration number of this snapshot.


    **Returns:**
    > The inner loop iteration number.  

??? abstract "get_InnerLoop_Itr_Runtime(self) → float | None"
    Return the inner loop iteration runtime of this snapshot.


    **Returns:**
    > The inner loop iteration runtime.  

??? abstract "get_InnerLoop_Itr_NumberOfDesignVariableEvaluations(self) → int | None"
    Return the number of design variable evaluations of this snapshot.


    **Returns:**
    > The number of design variable evaluations.  

