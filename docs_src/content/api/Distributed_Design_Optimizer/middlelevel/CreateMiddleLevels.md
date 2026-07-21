---
title: CreateMiddleLevels
---

← Back to [middlelevel](index.md)

# CreateMiddleLevels

**Source:** [Distributed_Design_Optimizer\middlelevel\CreateMiddleLevels.py](CreateMiddleLevels_source.md)

Factory module for creating middle-level objects.

This module provides factory functions for creating middle-level data storage
and coupling objects for different coordination methods.

## Classes

### CreateMiddleLevels

> Factory class for creating middle level data storage objects.

> Provides static methods to create and manage middle level data storage
> instances for distributed optimization coordination.

#### Methods

??? abstract "createMiddleLevels(subsystemsIn: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)], manager: [CustomManager](../coordination/CustomManager.md#custommanager) | None, coordinationmethod: [CoordinationMethodInterface](../coordination/coordinationmethod/CoordinationMethodInterface.md#coordinationmethodinterface)) → List[[MiddleLevelDataStorageInterface](MiddleLevelDataStorageInterface.md#middleleveldatastorageinterface)]"
    Create middle level data storage objects for subsystem couplings.

    Creates appropriate middle level storage based on the coordination
    method and subsystem coupling relationships.


    **Args:**
    > subsystemsIn: List of subsystems to create middle levels for.  
    > manager: Optional CustomManager for multiprocessing support.  
    > coordinationmethod: Coordination method defining middle level types.  


    **Returns:**
    > List of middle level data storage objects for all couplings.  

??? abstract "createManagedMiddleLevels(middlelevelsIn: List[[MiddleLevelDataStorageInterface](MiddleLevelDataStorageInterface.md#middleleveldatastorageinterface)], managerIn: [CustomManager](../coordination/CustomManager.md#custommanager)) → List[Any]"
    Create managed middle levels for multiprocessing.

    Wraps middle level objects with multiprocessing manager proxies
    for shared access across processes.


    **Args:**
    > middlelevelsIn: List of middle level objects to wrap.  
    > managerIn: CustomManager for creating managed objects.  


    **Returns:**
    > List of managed middle level proxy objects.  

