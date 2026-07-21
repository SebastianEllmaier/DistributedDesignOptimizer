---
title: InConsistencySize
---

← Back to [alc](index.md)

# InConsistencySize

**Source:** [Distributed_Design_Optimizer\middlelevel\alc\InConsistencySize.py](InConsistencySize_source.md)

Inconsistency size computation module for ALC.

This module provides functionality for computing inconsistency sizes
between coupled variables in standard ALC coordination.

## Classes

### InConsistencySize

> **Inherits from:** [InConsistencySizeBasis](../InConsistencySizeBasis.md#inconsistencysizebasis)

> Inconsistency size storage for augmented Lagrangian coordination.

> Stores coupling inconsistency measurements for the augmented Lagrangian
> coordination method.

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize the inconsistency size storage.


    **Args:**
    > id: Identifier of the neighboring subsystem.  

??? abstract "update_state(self, other_inconsistency: [InConsistencySize](../sbdp/InConsistencySize.md#inconsistencysize)) → None"
    Update the state from another inconsistency size instance.

    This method updates the numerical information stored in the class's attributes
    without changing the original memory address location. This is necessary for
    multiprocessing, where executed subsystems return from separate processes and
    their state must be transferred back to the original objects in the main process.


    **Args:**
    > other_inconsistency: Source instance to copy state from.  


    **Note:**
    > This class defines no additional attributes beyond the base class.  
    > All relevant attributes are updated via the base class update_state().  

