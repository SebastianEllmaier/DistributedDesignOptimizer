---
title: LocalController_MiddleLevelDataStorageALADIN (Source)
---

← Back to [LocalController_MiddleLevelDataStorageALADIN documentation](LocalController_MiddleLevelDataStorageALADIN.md)

# LocalController_MiddleLevelDataStorageALADIN - Source Code

**File:** `Distributed_Design_Optimizer\middlelevel\aladin\LocalController_MiddleLevelDataStorageALADIN.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Local-to-controller middle-level data storage module for ALADIN.

This module provides data storage for local-to-controller subsystem
coupling in ALADIN coordination.
"""

from typing import List, Union, Any
from Distributed_Design_Optimizer.middlelevel import MiddleLevelDataStorageBasis, MiddleLevelDataStorageProxy
from Distributed_Design_Optimizer.middlelevel.aladin import LocalToController_MiddleLevelCouplingALADIN
from Distributed_Design_Optimizer.middlelevel.aladin import ControllerToLocal_MiddleLevelCouplingALADIN
from Distributed_Design_Optimizer.subsystem.couplingparameters.aladin import LocalToLocalForController_CouplingParameters


class LocalController_MiddleLevelDataStorageALADIN(MiddleLevelDataStorageBasis):
    """Data storage for local-to-controller coupling in ALADIN.

    Stores coupling data between a local subsystem and the controller
    subsystem for ALADIN coordination.
    """

    def __init__(self, idparent: str, idchild: str, local_neighbors_list: List[str], multiprocessing_lock: object) -> None:
        """Initialize local-to-controller middle-level data storage.

        Args:
            idparent: Identifier of the parent subsystem.
            idchild: Identifier of the child subsystem.
            local_neighbors_list: List of local neighbor identifiers.
            multiprocessing_lock: Manager-created lock for multiprocessing.
        """
        # call __init__() of MiddleLevelDataStorageBasis
        super().__init__(idparent, idchild, multiprocessing_lock)
        
        self._couplingdata: List[ControllerToLocal_MiddleLevelCouplingALADIN | LocalToController_MiddleLevelCouplingALADIN] = [ControllerToLocal_MiddleLevelCouplingALADIN(local_neighbors_list), 
                                                                                                                               LocalToController_MiddleLevelCouplingALADIN(idchild, local_neighbors_list)]
    
    def createManagedMiddleLevel(self, manager: Any, lock: Any) -> Any:
        """Create a managed proxy copy of this middle level for multiprocessing.
        
        Infers the neighbors of the associated local subsystem by iterating over
        the instantiated ControllerToLocal_MiddleLevelCoupling list.

        Args:
            manager: Multiprocessing manager for creating shared objects.
            lock: Multiprocessing lock for synchronization.

        Returns:
            Managed proxy instance of this middle-level data storage.
        """
        # Obtain the LocalToLocalForController coupling parameters from the LocalMiddleLevelCoupling
        localtolocalforcontroller_middlelevelcouplings: List[LocalToLocalForController_CouplingParameters] = self.get_LocalToLocalForController_CouplingParameters()
        
        
        # Initialize neighbors list by iterating over localtolocalforcontroller_middlelevelcoupling
        local_neighbors_list: List[str] = [localtolocalforcontroller_middlelevelcouplings[j].get_ID() for j in range(len(localtolocalforcontroller_middlelevelcouplings))]

        managed = manager.LocalController_MiddleLevelDataStorageALADIN(
            idparent=self.get_ID()[0],
            idchild=self.get_ID()[1],
            local_neighbors_list=local_neighbors_list,
            multiprocessing_lock=lock
        )
        managed.update_state(self)
        return managed
    
    def get_LocalToLocalForController_CouplingParameters(self) -> List[LocalToLocalForController_CouplingParameters]:
        """Return the local-local to controller coupling parameters.

        Returns:
            List of local-local to controller coupling parameter objects.
        """
        
        self._DataLock.acquire()
        try:
            localtocontroller_middlelevelcoupling: LocalToController_MiddleLevelCouplingALADIN = self._couplingdata[1]
            
            # Since the second element of self._couplingdata is the LocalToController_MiddleLevelCouplingALADIN by init
            value = localtocontroller_middlelevelcoupling.get_LocalToLocalForController_CouplingParameters()
            return value
        finally:
            self._DataLock.release()
        
    def update_state(self, other_storage: Union['LocalController_MiddleLevelDataStorageALADIN', MiddleLevelDataStorageProxy]) -> None:
        """Update the state of this LocalController_MiddleLevelDataStorageALADIN with another instance.
        
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

```
