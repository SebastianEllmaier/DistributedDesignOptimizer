---
title: LocalController_MiddleLevelCouplingBasis
---

← Back to [middlelevel](index.md)

# LocalController_MiddleLevelCouplingBasis

**Source:** [Distributed_Design_Optimizer\middlelevel\LocalController_MiddleLevelCouplingBasis.py](LocalController_MiddleLevelCouplingBasis_source.md)

Controller middle-level coupling basis module.

This module provides the base class for controller-side middle-level coupling
parameters in distributed optimization.

## Classes

### LocalController_MiddleLevelCouplingBasis

> **Inherits from:** [MiddleLevelCouplingBasis](MiddleLevelCouplingBasis.md#middlelevelcouplingbasis)

> Base class for controller-side middle-level coupling parameters.

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize the controller middle level coupling.


    **Args:**
    > id: Identifier of the neighboring subsystem.  

??? abstract "update_state(self, other_middlelevelcoupling: [LocalController_MiddleLevelCouplingBasis](LocalController_MiddleLevelCouplingBasis.md#localcontroller_middlelevelcouplingbasis)) → None"
    Update the state of this instance from another instance.

    This method is necessary for multiprocessing. When subsystems are executed
    in parallel processes via Parallel.py, the original objects need to
    be updated with results from the executed copies. This method preserves
    the memory address of the object's attributes while updating their values.

    This class delegates entirely to the base class update_state() which handles:
    - _id: Identifier of the neighboring subsystem (str)


    **Args:**
    > other_middlelevelcoupling: The source instance containing updated values to copy from.  

