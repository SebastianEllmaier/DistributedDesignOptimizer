---
title: MiddleLevelDataStorageALC
---

← Back to [alc](index.md)

# MiddleLevelDataStorageALC

**Source:** [Distributed_Design_Optimizer\middlelevel\alc\MiddleLevelDataStorageALC.py](MiddleLevelDataStorageALC_source.md)

Middle-level data storage module for standard ALC.

This module provides data storage for coupling parameters in standard
Augmented Lagrangian Coordination.

## Classes

### MiddleLevelDataStorageALC

> **Inherits from:** [MiddleLevelDataStorageBasis](../MiddleLevelDataStorageBasis.md#middleleveldatastoragebasis)

> Middle level data storage for augmented Lagrangian coordination.

> Stores coupling data between subsystems using augmented Lagrangian
> coordination method with thread-safe access.

#### Methods

??? abstract "__init__(self, idparent: str, idchild: str, multiprocessing_lock: object) → None"
    Initialize the middle level data storage.


    **Args:**
    > idparent: Identifier of the parent subsystem.  
    > idchild: Identifier of the child subsystem.  
    > multiprocessing_lock: Manager-created lock for multiprocessing.  

??? abstract "createManagedMiddleLevel(self, manager: Any, lock: Any) → Any"
    Create a managed proxy copy of this middle level for multiprocessing.


    **Args:**
    > manager: Multiprocessing manager for creating shared objects.  
    > lock: Multiprocessing lock for synchronization.  


    **Returns:**
    > Managed proxy instance of this middle-level data storage.  

??? abstract "update_state(self, other_storage: Union[[MiddleLevelDataStorageALC](MiddleLevelDataStorageALC.md#middleleveldatastoragealc), [MiddleLevelDataStorageProxy](../MiddleLevelDataStorageProxy.md#middleleveldatastorageproxy)]) → None"
    Update the state from another data storage instance.

    This method updates the numerical information stored in the class's attributes
    without changing the original memory address location. This is necessary for
    multiprocessing, where executed subsystems return from separate processes and
    their state must be transferred back to the original objects in the main process.


    **Args:**
    > other_storage: Source instance to copy state from.  


    **Note:**
    > This class defines no additional attributes beyond the base class.  
    > The _couplingdata attribute is updated via the base class update_state(),  
    > which iterates over each coupling object and calls its update_state() method.  

