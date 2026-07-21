---
title: MiddleLevelDataStorageBasis
---

← Back to [middlelevel](index.md)

# MiddleLevelDataStorageBasis

**Source:** [Distributed_Design_Optimizer\middlelevel\MiddleLevelDataStorageBasis.py](MiddleLevelDataStorageBasis_source.md)

Middle-level data storage basis module.

This module provides the base class for storing middle-level coupling
data in distributed optimization.

## Classes

### MiddleLevelDataStorageBasis

> **Inherits from:** [MiddleLevelDataStorageInterface](MiddleLevelDataStorageInterface.md#middleleveldatastorageinterface)

> Base class for middle level data storage.

> Provides thread-safe storage for coupling data exchanged between
> subsystems in distributed optimization.


> **Attributes:**
> > _id: List of parent and child subsystem identifiers.  
> > _couplingdata: List of middle level coupling objects.  
> > _DataLock: Lock for thread-safe access.

#### Methods

??? abstract "__init__(self, idparent: str, idchild: str, multiprocessing_lock: object) → None"
    Initialize the middle level data storage.


    **Args:**
    > idparent: Identifier of the parent subsystem.  
    > idchild: Identifier of the child subsystem.  
    > multiprocessing_lock: Manager-created lock for multiprocessing.  

??? abstract "set_Coupling(self, coupling: [CouplingParametersInterface](../subsystem/couplingparameters/CouplingParametersInterface.md#couplingparametersinterface)) → None"
    Store coupling variables from a subsystem.

    Acquires the data lock, identifies which slot (parent or child)
    corresponds to the coupling parameter's neighbor ID, and copies
    the coupling data into the shared storage.


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

??? abstract "update_state(self, other_storage: Union[[MiddleLevelDataStorageInterface](MiddleLevelDataStorageInterface.md#middleleveldatastorageinterface), [MiddleLevelDataStorageProxy](MiddleLevelDataStorageProxy.md#middleleveldatastorageproxy)]) → None"
    Update the state of this MiddleLevelDataStorageBasis from another instance.

    This method is necessary for multiprocessing. When subsystems are executed
    in parallel processes via Parallel.py, the original objects need to
    be updated with results from the executed copies. This method preserves
    the memory address of the object's attributes while updating their values.


    **Args:**
    > other_storage: The source instance containing updated values to copy from.  

    Note on copy operations:
    - _id (List[str]): Updated in-place via update_state_listprimitive()
    to preserve memory address. str elements are immutable,
    no copy.copy() needed for each element.
    - _couplingdata (List[MiddleLevelCouplingInterface]): Updated via nested
    update_state() calls to preserve memory addresses of contained objects.
    - _DataLock: NOT updated - shared lock resource must remain unchanged.

