---
title: MiddleLevelDataStorageProxy
---

← Back to [middlelevel](index.md)

# MiddleLevelDataStorageProxy

**Source:** [Distributed_Design_Optimizer\middlelevel\MiddleLevelDataStorageProxy.py](MiddleLevelDataStorageProxy_source.md)

Proxy module for middle-level data storage.

This module provides proxy objects for multiprocessing access to
middle-level data storage in distributed optimization.

## Classes

### MiddleLevelDataStorageProxy

> **Inherits from:** `BaseProxy`

> Proxy class for MiddleLevelDataStorage for use with multiprocessing.

> Provides remote method invocation for MiddleLevelDataStorage objects
> across process boundaries.

#### Methods

??? abstract "set_Coupling(self, coupling: Any) → None"
    Store coupling variables from a subsystem.


    **Args:**
    > coupling: Coupling parameters to store.  

??? abstract "get_StoredCoupling(self, id: Any) → Any"
    Return the stored coupling data for a given subsystem ID (under lock).


    **Args:**
    > id: Identifier of the neighbor subsystem whose data to retrieve.  


    **Returns:**
    > The stored MiddleLevelCouplingInterface for the given subsystem.  

??? abstract "get_ID(self) → List[str]"
    Get the identifiers of the connected subsystems.


    **Returns:**
    > List containing parent and child subsystem identifiers.  

??? abstract "get_CouplingData(self) → List[Any]"
    Get all coupling data stored in this middle level.


    **Returns:**
    > List of middle level coupling objects.  

??? abstract "update_state(self, other_storage: Any) → None"
    Forward state update call to the remote MiddleLevelDataStorage object.

    This proxy method is necessary for multiprocessing: it enables the caller
    to invoke update_state() on the actual MiddleLevelDataStorage object that
    resides in the manager process. The proxy itself has no local state to
    update - it simply forwards the call across process boundaries via
    _callmethod().

    The actual state update (preserving memory addresses while updating
    numerical values) happens in the remote MiddleLevelDataStorage object,
    not in this proxy.


    **Note:**
    > This is a proxy method - no local attributes are updated here.  
    > The state lives in the actual MiddleLevelDataStorage object being proxied.  


    **Args:**
    > other_storage: Source instance to copy state from. Passed to the  
    > remote object's update_state() method.  

