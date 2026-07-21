---
title: CustomManager
---

← Back to [coordination](index.md)

# CustomManager

**Source:** [Distributed_Design_Optimizer\coordination\CustomManager.py](CustomManager_source.md)

Custom multiprocessing manager for distributed optimization.

This module provides CustomManager, a custom BaseManager subclass for managing
shared middle-level data storage objects across multiple processes during
parallel distributed optimization.

## Classes

### CustomManager

> **Inherits from:** `BaseManager`

> Custom manager for handling shared objects between processes.

#### Methods

??? abstract "register_all_data_storages(cls) → None"
    Auto-discover and register all MiddleLevelDataStorageBasis subclasses.

    Recursively imports all subpackages under the middlelevel package,
    then registers every subclass of MiddleLevelDataStorageBasis with
    this manager using MiddleLevelDataStorageProxy as the proxy type.

