---
title: InConsistencySize
---

← Back to [aladin](index.md)

# InConsistencySize

**Source:** [Distributed_Design_Optimizer\middlelevel\aladin\InConsistencySize.py](InConsistencySize_source.md)

Inconsistency size computation module for ALADIN.

This module provides functionality for computing inconsistency sizes
between coupled variables in ALADIN coordination.

## Classes

### InConsistencySize

> **Inherits from:** [InConsistencySizeBasis](../InConsistencySizeBasis.md#inconsistencysizebasis)

> Computes inconsistency sizes for ALADIN coordination.

> Measures the inconsistency between coupled variables from different subsystems.

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize the ALADIN inconsistency size.


    **Args:**
    > id: Identifier for this inconsistency size instance.  

??? abstract "update_state(self, other_inconsistency: [InConsistencySize](../sbdp/InConsistencySize.md#inconsistencysize)) → None"
    Update the state of this InConsistencySize with the state of another InConsistencySize.

    This operation preserves the memory address of the object's attributes
    and only updates the value(s). This method is necessary for multiprocessing,
    where executed subsystems need to transfer their state back to the original objects.

    This subclass has no additional attributes beyond the base class,
    so it simply delegates to the base class update_state.


    **Args:**
    > other_inconsistency: The InConsistencySize to copy state from.  

