---
title: LocalToLocal_MiddleLevelDataStorageALADIN
---

← Back to [aladin](index.md)

# LocalToLocal_MiddleLevelDataStorageALADIN

**Source:** [Distributed_Design_Optimizer\middlelevel\aladin\LocalToLocal_MiddleLevelDataStorageALADIN.py](LocalToLocal_MiddleLevelDataStorageALADIN_source.md)

Local-to-local middle-level data storage module for ALADIN.

This module provides data storage for local-to-local subsystem
coupling in ALADIN coordination.

## Classes

### LocalToLocal_MiddleLevelDataStorageALADIN

> **Inherits from:** [MiddleLevelDataStorageBasis](../MiddleLevelDataStorageBasis.md#middleleveldatastoragebasis)

> Data storage for local-to-local coupling in ALADIN.

> Stores coupling data between two local subsystems for ALADIN
> coordination.

#### Methods

??? abstract "__init__(self, idparent: str, idchild: str, multiprocessing_lock: object) → None"
    Initialize local-to-local middle-level data storage.


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

??? abstract "update_state(self, other_storage: Union[[LocalToLocal_MiddleLevelDataStorageALADIN](LocalToLocal_MiddleLevelDataStorageALADIN.md#localtolocal_middleleveldatastoragealadin), [MiddleLevelDataStorageProxy](../MiddleLevelDataStorageProxy.md#middleleveldatastorageproxy)]) → None"
    Update the state of this LocalToLocal_MiddleLevelDataStorageALADIN with another instance.

    This method updates the numerical information stored in the class's attributes
    without changing the original memory address location. This is necessary for
    multiprocessing, where executed subsystems return from separate processes and
    their state must be transferred back to the original objects in the main process.


    **Args:**
    > other_storage: The source instance to copy state from.  


    **Note:**
    > This class defines no additional attributes beyond the base class.  
    > The _couplingdata attribute is updated via the base class update_state(),  
    > which iterates over each coupling object and calls its update_state() method.  

