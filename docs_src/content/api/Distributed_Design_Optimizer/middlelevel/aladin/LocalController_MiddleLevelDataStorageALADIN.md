---
title: LocalController_MiddleLevelDataStorageALADIN
---

← Back to [aladin](index.md)

# LocalController_MiddleLevelDataStorageALADIN

**Source:** [Distributed_Design_Optimizer\middlelevel\aladin\LocalController_MiddleLevelDataStorageALADIN.py](LocalController_MiddleLevelDataStorageALADIN_source.md)

Local-to-controller middle-level data storage module for ALADIN.

This module provides data storage for local-to-controller subsystem
coupling in ALADIN coordination.

## Classes

### LocalController_MiddleLevelDataStorageALADIN

> **Inherits from:** [MiddleLevelDataStorageBasis](../MiddleLevelDataStorageBasis.md#middleleveldatastoragebasis)

> Data storage for local-to-controller coupling in ALADIN.

> Stores coupling data between a local subsystem and the controller
> subsystem for ALADIN coordination.

#### Methods

??? abstract "__init__(self, idparent: str, idchild: str, local_neighbors_list: List[str], multiprocessing_lock: object) → None"
    Initialize local-to-controller middle-level data storage.


    **Args:**
    > idparent: Identifier of the parent subsystem.  
    > idchild: Identifier of the child subsystem.  
    > local_neighbors_list: List of local neighbor identifiers.  
    > multiprocessing_lock: Manager-created lock for multiprocessing.  

??? abstract "createManagedMiddleLevel(self, manager: Any, lock: Any) → Any"
    Create a managed proxy copy of this middle level for multiprocessing.

    Infers the neighbors of the associated local subsystem by iterating over
    the instantiated ControllerToLocal_MiddleLevelCoupling list.


    **Args:**
    > manager: Multiprocessing manager for creating shared objects.  
    > lock: Multiprocessing lock for synchronization.  


    **Returns:**
    > Managed proxy instance of this middle-level data storage.  

??? abstract "get_LocalToLocalForController_CouplingParameters(self) → List[[LocalToLocalForController_CouplingParameters](../../subsystem/couplingparameters/aladin/LocalToLocalForController_CouplingParameters.md#localtolocalforcontroller_couplingparameters)]"
    Return the local-local to controller coupling parameters.


    **Returns:**
    > List of local-local to controller coupling parameter objects.  

??? abstract "update_state(self, other_storage: Union[[LocalController_MiddleLevelDataStorageALADIN](LocalController_MiddleLevelDataStorageALADIN.md#localcontroller_middleleveldatastoragealadin), [MiddleLevelDataStorageProxy](../MiddleLevelDataStorageProxy.md#middleleveldatastorageproxy)]) → None"
    Update the state of this LocalController_MiddleLevelDataStorageALADIN with another instance.

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

