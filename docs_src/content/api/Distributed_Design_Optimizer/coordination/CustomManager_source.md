---
title: CustomManager (Source)
---

← Back to [CustomManager documentation](CustomManager.md)

# CustomManager - Source Code

**File:** `Distributed_Design_Optimizer\coordination\CustomManager.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Custom multiprocessing manager for distributed optimization.

This module provides CustomManager, a custom BaseManager subclass for managing
shared middle-level data storage objects across multiple processes during
parallel distributed optimization.
"""

import importlib
import multiprocessing
import pkgutil
from multiprocessing.managers import BaseManager, AutoProxy

from Distributed_Design_Optimizer import middlelevel
from Distributed_Design_Optimizer.middlelevel import (
    MiddleLevelDataStorageBasis,
    MiddleLevelDataStorageProxy,
)


class CustomManager(BaseManager):
    """Custom manager for handling shared objects between processes."""

    @classmethod
    def register_all_data_storages(cls) -> None:
        """Auto-discover and register all MiddleLevelDataStorageBasis subclasses.

        Recursively imports all subpackages under the middlelevel package,
        then registers every subclass of MiddleLevelDataStorageBasis with
        this manager using MiddleLevelDataStorageProxy as the proxy type.
        """
        # Recursively import all submodules so subclasses are defined
        for importer, modname, ispkg in pkgutil.walk_packages(
            middlelevel.__path__,
            prefix='Distributed_Design_Optimizer.middlelevel.'
        ):
            try:
                importlib.import_module(modname)
            except ImportError:
                pass  # Skip modules that fail to import

        # Recursively collect all subclasses (including nested inheritance)
        def get_all_subclasses(base_cls):
            subclasses = set()
            for subclass in base_cls.__subclasses__():
                subclasses.add(subclass)
                subclasses.update(get_all_subclasses(subclass))
            return subclasses

        # Register each discovered subclass
        for subclass in get_all_subclasses(MiddleLevelDataStorageBasis):
            cls.register(subclass.__name__, subclass, MiddleLevelDataStorageProxy)


# Register Lock explicitly
CustomManager.register('Lock', multiprocessing.Lock, proxytype=AutoProxy)

# Note: Call CustomManager.register_all_data_storages() before using the manager
# (e.g., in Coordinator) to avoid circular imports

```
