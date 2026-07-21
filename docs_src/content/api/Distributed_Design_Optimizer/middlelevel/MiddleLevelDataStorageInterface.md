---
title: MiddleLevelDataStorageInterface
---

← Back to [middlelevel](index.md)

# MiddleLevelDataStorageInterface

**Source:** [Distributed_Design_Optimizer\middlelevel\MiddleLevelDataStorageInterface.py](MiddleLevelDataStorageInterface_source.md)

Interface module for middle-level data storage.

This module defines the abstract interface for middle-level data storage
in distributed optimization.

## Classes

### MiddleLevelDataStorageInterface

> **Inherits from:** `ABC`

> Abstract interface for middle level data storage.

> Defines the contract for classes that store and manage coupling data
> between subsystems in distributed optimization.

#### Methods

??? abstract "set_Coupling(self, coupling: [CouplingParametersInterface](../subsystem/couplingparameters/CouplingParametersInterface.md#couplingparametersinterface)) → None"
    Store coupling variables from a subsystem.


    **Args:**
    > coupling: Coupling parameters to store.  

??? abstract "get_StoredCoupling(self, id: str) → [MiddleLevelCouplingInterface](MiddleLevelCouplingInterface.md#middlelevelcouplinginterface) | None"
    Return the stored coupling data for a given subsystem ID (under lock).

    NOTE ON ASYMMETRY WITH set_Coupling:
    set_Coupling(coupling) takes a CouplingParametersInterface and
    internally calls coupling.CopyToMiddleLevelCoupling(slot) to push
    data INTO the storage. The mirror operation — pulling data OUT —
    cannot use the same pattern (i.e. coupling.CopyFromMiddleLevelCoupling
    called inside this method) because of multiprocessing proxies:
    when called through a BaseProxy, arguments are pickled to the
    manager process. Any mutation of the argument happens on the
    deserialized copy in the manager and is discarded — the caller's
    original object is never modified. Only return values are sent
    back across process boundaries. Therefore this method RETURNS
    the stored data so the caller can apply it locally.


    **Args:**
    > id: Identifier of the neighbor subsystem whose data to retrieve.  


    **Returns:**
    > The stored MiddleLevelCouplingInterface for the given subsystem,  
    > or None if the coupling data for that slot is None.  

??? abstract "get_ID(self) → List[str]"
    Get the identifiers of the connected subsystems.


    **Returns:**
    > List containing parent and child subsystem identifiers.  

??? abstract "get_CouplingData(self) → List[[MiddleLevelCouplingInterface](MiddleLevelCouplingInterface.md#middlelevelcouplinginterface)]"
    Get all coupling data stored in this middle level.


    **Returns:**
    > List of middle level coupling objects.  

??? abstract "createManagedMiddleLevel(self, manager: Any, lock: Any) → Any"
    Create a managed proxy copy of this middle level for multiprocessing.

    This method creates a new managed instance of this middle level using the
    CustomManager, copies the current state to it, and returns it.
    For concrete implementation see e.g. MiddleLevelDataStorageALC, MiddleLevelDataStorageLC, ...


    **Args:**
    > manager: CustomManager instance for creating managed objects.  
    > lock: Multiprocessing lock for the managed object.  


    **Returns:**
    > Managed middle level proxy object with state copied from this instance.  

??? abstract "update_state(self, other_storage: Union[[MiddleLevelDataStorageInterface](MiddleLevelDataStorageInterface.md#middleleveldatastorageinterface), [MiddleLevelDataStorageProxy](MiddleLevelDataStorageProxy.md#middleleveldatastorageproxy)]) → None"
    Update the state of this data storage from another instance.

    This method is necessary for multiprocessing: when subsystems are executed
    in parallel via Parallel.py using multiprocessing.Pool, each process
    receives a copy of the data. After execution, the original objects must be
    updated with results from the executed copies. This method updates the
    numerical information stored in the class's attributes without changing
    the original memory address location, preserving object identity.


    **Args:**
    > other_storage: Source instance to copy state from. Can be either a  
    > MiddleLevelDataStorageInterface or MiddleLevelDataStorageProxy.  

