---
title: MiddleLevelDataStorageALC (Source)
---

← Back to [MiddleLevelDataStorageALC documentation](MiddleLevelDataStorageALC.md)

# MiddleLevelDataStorageALC - Source Code

**File:** `Distributed_Design_Optimizer\middlelevel\alc\MiddleLevelDataStorageALC.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Middle-level data storage module for standard ALC.

This module provides data storage for coupling parameters in standard
Augmented Lagrangian Coordination.
"""

from typing import List, Union, Any
from Distributed_Design_Optimizer.middlelevel import MiddleLevelDataStorageBasis, MiddleLevelDataStorageProxy
from Distributed_Design_Optimizer.middlelevel.alc import MiddleLevelCouplingALC


class MiddleLevelDataStorageALC(MiddleLevelDataStorageBasis):
    """Middle level data storage for augmented Lagrangian coordination.

    Stores coupling data between subsystems using augmented Lagrangian
    coordination method with thread-safe access.
    """

    def __init__(self, idparent: str, idchild: str, multiprocessing_lock: object) -> None:
        """Initialize the middle level data storage.

        Args:
            idparent: Identifier of the parent subsystem.
            idchild: Identifier of the child subsystem.
            multiprocessing_lock: Manager-created lock for multiprocessing.
        """
        # call __init__() of MiddleLevelDataStorageBasis
        super().__init__(idparent, idchild, multiprocessing_lock)
        
        self._couplingdata: List[MiddleLevelCouplingALC] = [MiddleLevelCouplingALC(idparent), MiddleLevelCouplingALC(idchild)]
    
    def createManagedMiddleLevel(self, manager: Any, lock: Any) -> Any:
        """Create a managed proxy copy of this middle level for multiprocessing.

        Args:
            manager: Multiprocessing manager for creating shared objects.
            lock: Multiprocessing lock for synchronization.

        Returns:
            Managed proxy instance of this middle-level data storage.
        """
        managed = manager.MiddleLevelDataStorageALC(
            idparent=self.get_ID()[0],
            idchild=self.get_ID()[1],
            multiprocessing_lock=lock
        )
        managed.update_state(self)
        return managed
    
    def update_state(self, other_storage: Union['MiddleLevelDataStorageALC', MiddleLevelDataStorageProxy]) -> None:
        """Update the state from another data storage instance.
        
        This method updates the numerical information stored in the class's attributes
        without changing the original memory address location. This is necessary for
        multiprocessing, where executed subsystems return from separate processes and
        their state must be transferred back to the original objects in the main process.

        Args:
            other_storage: Source instance to copy state from.
        
        Note:
            This class defines no additional attributes beyond the base class.
            The _couplingdata attribute is updated via the base class update_state(),
            which iterates over each coupling object and calls its update_state() method.
        """
        # Call the base class update_state to handle all attributes including _couplingdata
        super().update_state(other_storage)

```
