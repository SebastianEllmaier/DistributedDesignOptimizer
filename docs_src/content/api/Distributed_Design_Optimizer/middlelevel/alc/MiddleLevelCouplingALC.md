---
title: MiddleLevelCouplingALC
---

← Back to [alc](index.md)

# MiddleLevelCouplingALC

**Source:** [Distributed_Design_Optimizer\middlelevel\alc\MiddleLevelCouplingALC.py](MiddleLevelCouplingALC_source.md)

Middle-level coupling module for standard ALC.

This module provides middle-level coupling management for standard
Augmented Lagrangian Coordination.

## Classes

### MiddleLevelCouplingALC

> **Inherits from:** [SubSysMiddleLevelCouplingBasis](../SubSysMiddleLevelCouplingBasis.md#subsysmiddlelevelcouplingbasis)

> Middle level coupling for augmented Lagrangian coordination.

> Stores coupling data between subsystems using augmented Lagrangian
> coordination method.

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize the middle level coupling.


    **Args:**
    > id: Identifier of the neighboring subsystem.  

??? abstract "update_state(self, other_middlelevelcoupling: [MiddleLevelCouplingALC](MiddleLevelCouplingALC.md#middlelevelcouplingalc)) → None"
    Update the state from another middle level coupling instance.

    This method updates the numerical information stored in the class's attributes
    without changing the original memory address location. This is necessary for
    multiprocessing, where executed subsystems return from separate processes and
    their state must be transferred back to the original objects in the main process.


    **Args:**
    > other_middlelevelcoupling: Source instance to copy state from.  


    **Note:**
    > This class defines no additional attributes beyond the base class.  
    > All relevant attributes are updated via the base class update_state().  

