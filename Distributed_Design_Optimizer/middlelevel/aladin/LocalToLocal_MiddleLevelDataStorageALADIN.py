# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Local-to-local middle-level data storage module for ALADIN.

This module provides data storage for local-to-local subsystem
coupling in ALADIN coordination.
"""


from typing import List, Union, Any
from Distributed_Design_Optimizer.middlelevel import MiddleLevelDataStorageBasis, MiddleLevelDataStorageProxy
from Distributed_Design_Optimizer.middlelevel.aladin import LocalToLocal_MiddleLevelCouplingALADIN


class LocalToLocal_MiddleLevelDataStorageALADIN(MiddleLevelDataStorageBasis):
    """Data storage for local-to-local coupling in ALADIN.

    Stores coupling data between two local subsystems for ALADIN
    coordination.
    """

    def __init__(self, idparent: str, idchild: str, multiprocessing_lock: object) -> None:
        """Initialize local-to-local middle-level data storage.

        Args:
            idparent: Identifier of the parent subsystem.
            idchild: Identifier of the child subsystem.
            multiprocessing_lock: Manager-created lock for multiprocessing.
        """
        # call __init__() of MiddleLevelDataStorageBasis
        super().__init__(idparent, idchild, multiprocessing_lock)
        
        self._couplingdata: List[LocalToLocal_MiddleLevelCouplingALADIN] = [LocalToLocal_MiddleLevelCouplingALADIN(idparent), LocalToLocal_MiddleLevelCouplingALADIN(idchild)]
    
    def createManagedMiddleLevel(self, manager: Any, lock: Any) -> Any:
        """Create a managed proxy copy of this middle level for multiprocessing.

        Args:
            manager: Multiprocessing manager for creating shared objects.
            lock: Multiprocessing lock for synchronization.

        Returns:
            Managed proxy instance of this middle-level data storage.
        """
        managed = manager.LocalToLocal_MiddleLevelDataStorageALADIN(
            idparent=self.get_ID()[0],
            idchild=self.get_ID()[1],
            multiprocessing_lock=lock
        )
        managed.update_state(self)
        return managed
    
    def update_state(self, other_storage: Union['LocalToLocal_MiddleLevelDataStorageALADIN', MiddleLevelDataStorageProxy]) -> None:
        """Update the state of this LocalToLocal_MiddleLevelDataStorageALADIN with another instance.
        
        This method updates the numerical information stored in the class's attributes
        without changing the original memory address location. This is necessary for
        multiprocessing, where executed subsystems return from separate processes and
        their state must be transferred back to the original objects in the main process.
        
        Args:
            other_storage: The source instance to copy state from.
        
        Note:
            This class defines no additional attributes beyond the base class.
            The _couplingdata attribute is updated via the base class update_state(),
            which iterates over each coupling object and calls its update_state() method.
        """
        # Call the base class update_state to handle all attributes including _couplingdata
        super().update_state(other_storage)
