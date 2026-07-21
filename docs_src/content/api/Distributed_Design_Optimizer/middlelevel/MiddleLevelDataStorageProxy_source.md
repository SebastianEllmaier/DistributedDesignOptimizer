---
title: MiddleLevelDataStorageProxy (Source)
---

← Back to [MiddleLevelDataStorageProxy documentation](MiddleLevelDataStorageProxy.md)

# MiddleLevelDataStorageProxy - Source Code

**File:** `Distributed_Design_Optimizer\middlelevel\MiddleLevelDataStorageProxy.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Proxy module for middle-level data storage.

This module provides proxy objects for multiprocessing access to
middle-level data storage in distributed optimization.
"""

from multiprocessing.managers import BaseProxy
from typing import List, Any


class MiddleLevelDataStorageProxy(BaseProxy):
    """Proxy class for MiddleLevelDataStorage for use with multiprocessing.

    Provides remote method invocation for MiddleLevelDataStorage objects
    across process boundaries.
    """
    
    _exposed_ = ['set_Coupling', 'get_StoredCoupling', 'get_ID', 'get_CouplingData', 'update_state']
    
    def set_Coupling(self, coupling: Any) -> None:
        """Store coupling variables from a subsystem.

        Args:
            coupling: Coupling parameters to store.
        """
        return self._callmethod('set_Coupling', (coupling,))
    
    def get_StoredCoupling(self, id: Any) -> Any:
        """Return the stored coupling data for a given subsystem ID (under lock).

        Args:
            id: Identifier of the neighbor subsystem whose data to retrieve.

        Returns:
            The stored MiddleLevelCouplingInterface for the given subsystem.
        """
        return self._callmethod('get_StoredCoupling', (id,))
    
    def get_ID(self) -> List[str]:
        """Get the identifiers of the connected subsystems.

        Returns:
            List containing parent and child subsystem identifiers.
        """
        return self._callmethod('get_ID', ())
    
    def get_CouplingData(self) -> List[Any]:
        """Get all coupling data stored in this middle level.

        Returns:
            List of middle level coupling objects.
        """
        return self._callmethod('get_CouplingData', ())
    
    def update_state(self, other_storage: Any) -> None:
        """Forward state update call to the remote MiddleLevelDataStorage object.

        This proxy method is necessary for multiprocessing: it enables the caller
        to invoke update_state() on the actual MiddleLevelDataStorage object that
        resides in the manager process. The proxy itself has no local state to
        update - it simply forwards the call across process boundaries via
        _callmethod().

        The actual state update (preserving memory addresses while updating
        numerical values) happens in the remote MiddleLevelDataStorage object,
        not in this proxy.

        Note:
            This is a proxy method - no local attributes are updated here.
            The state lives in the actual MiddleLevelDataStorage object being proxied.

        Args:
            other_storage: Source instance to copy state from. Passed to the
                remote object's update_state() method.
        """
        return self._callmethod('update_state', (other_storage,))

```
