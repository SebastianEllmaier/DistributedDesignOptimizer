---
title: LocalToController_MiddleLevelCouplingBasis
---

← Back to [middlelevel](index.md)

# LocalToController_MiddleLevelCouplingBasis

**Source:** [Distributed_Design_Optimizer\middlelevel\LocalToController_MiddleLevelCouplingBasis.py](LocalToController_MiddleLevelCouplingBasis_source.md)

Local -> Controller Middle-level coupling basis module.

This module provides the base class for middle-level coupling parameters
from local subsystem to controller in distributed optimization.

## Classes

### LocalToController_MiddleLevelCouplingBasis

> **Inherits from:** [LocalController_MiddleLevelCouplingBasis](LocalController_MiddleLevelCouplingBasis.md#localcontroller_middlelevelcouplingbasis)

> Holds the coupling parameters from a local subsystem to the controller.

> It stores the identifier of the neighbor and stores the coupling variables.

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize the local -> controller middle level coupling basis.


    **Args:**
    > id: Identifier of the neighboring subsystem.  

??? abstract "update_state(self, other_middlelevelcoupling: [LocalToController_MiddleLevelCouplingBasis](LocalToController_MiddleLevelCouplingBasis.md#localtocontroller_middlelevelcouplingbasis)) → None"
    Update the state of this LocalToController_MiddleLevelCouplingBasis from another instance.

    This method is necessary for multiprocessing. When subsystems are executed
    in parallel processes via Parallel.py, the original objects need to
    be updated with results from the executed copies. This method preserves
    the memory address of the object's attributes while updating their values.


    **Args:**
    > other_middlelevelcoupling: The source instance containing updated values to copy from.  

    Note on copy operations:
    - _id (str): No copy.copy() needed - str is immutable in Python.
    Assigning creates a new binding; the original cannot be modified.

