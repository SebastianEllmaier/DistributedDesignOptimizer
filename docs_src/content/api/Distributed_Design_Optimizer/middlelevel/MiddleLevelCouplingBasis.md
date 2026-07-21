---
title: MiddleLevelCouplingBasis
---

← Back to [middlelevel](index.md)

# MiddleLevelCouplingBasis

**Source:** [Distributed_Design_Optimizer\middlelevel\MiddleLevelCouplingBasis.py](MiddleLevelCouplingBasis_source.md)

Middle-level coupling basis module.

This module provides the base class for middle-level coupling parameters
between subsystems in distributed optimization.

## Classes

### MiddleLevelCouplingBasis

> **Inherits from:** [MiddleLevelCouplingInterface](MiddleLevelCouplingInterface.md#middlelevelcouplinginterface)

> A MiddleLevelCoupling subclass object holds the coupling parameters between a subsystem and a single neighbor / controller.
> It stores the identifier of the neighbor and stores the couplingvariables

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize the middle level coupling basis.


    **Args:**
    > id: Identifier of the neighboring subsystem.  

??? abstract "get_ID(self) → str"
    Get the identifier of the neighboring subsystem.


    **Returns:**
    > The neighbor subsystem identifier.  

??? abstract "update_state(self, other_middlelevelcoupling: [MiddleLevelCouplingBasis](MiddleLevelCouplingBasis.md#middlelevelcouplingbasis)) → None"
    Update the state of this MiddleLevelCouplingBasis from another instance.

    This method is necessary for multiprocessing. When subsystems are executed
    in parallel processes via Parallel.py, the original objects need to
    be updated with results from the executed copies. This method preserves
    the memory address of the object's attributes while updating their values.


    **Args:**
    > other_middlelevelcoupling: The source instance containing updated values to copy from.  

    Note on copy operations:
    - _id (str): No copy.copy() needed - str is immutable in Python.
    Assigning creates a new binding; the original cannot be modified.

