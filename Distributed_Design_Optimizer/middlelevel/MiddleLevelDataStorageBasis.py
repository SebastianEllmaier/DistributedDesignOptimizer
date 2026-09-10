# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Middle-level data storage basis module.

This module provides the base class for storing middle-level coupling
data in distributed optimization.
"""

from typing import List, Union
import copy
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset
from Distributed_Design_Optimizer.middlelevel import (MiddleLevelDataStorageInterface,
                                                      MiddleLevelDataStorageProxy,
                                                      MiddleLevelCouplingInterface
                                                      )
from Distributed_Design_Optimizer.subsystem.couplingparameters import CouplingParametersInterface
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive


class MiddleLevelDataStorageBasis(MiddleLevelDataStorageInterface):
    """Base class for middle level data storage.

    Provides thread-safe storage for coupling data exchanged between
    subsystems in distributed optimization.

    Attributes:
        _id: List of parent and child subsystem identifiers.
        _couplingdata: List of middle level coupling objects.
        _DataLock: Lock for thread-safe access.
    """
    
    def __init__(self, idparent: str, idchild: str, multiprocessing_lock: object) -> None:
        """Initialize the middle level data storage.

        Args:
            idparent: Identifier of the parent subsystem.
            idchild: Identifier of the child subsystem.
            multiprocessing_lock: Manager-created lock for multiprocessing.
        """
        self._id = [idparent, idchild]
        self._couplingdata: List[MiddleLevelCouplingInterface]  # to be defined in classes inheriting from MiddleLevelDataStorageBasis        
        self._DataLock = multiprocessing_lock
            
    def set_Coupling(self, coupling: CouplingParametersInterface) -> None:
        """Store coupling variables from a subsystem.

        Acquires the data lock, identifies which slot (parent or child)
        corresponds to the coupling parameter's neighbor ID, and copies
        the coupling data into the shared storage.

        Args:
            coupling: Coupling parameters to store.
        """
        self._DataLock.acquire()
        try:
            idin: str = coupling.get_ID()
            # NOTE: The slot indices here are intentionally inverted compared to
            # get_StoredCoupling(). coupling.get_ID() returns the NEIGHBOR's ID.
            # A subsystem writing its own data stores it in its OWN slot:
            #   - Parent (neighbor == child) writes to slot 0 (parent's slot)
            #   - Child  (neighbor == parent) writes to slot 1 (child's slot)
            if idin.lower() == self._id[1].lower():
                coupling.CopyToMiddleLevelCoupling(self._couplingdata[0])
                
            elif idin.lower() == self._id[0].lower():
                coupling.CopyToMiddleLevelCoupling(self._couplingdata[1])
                
            else:
                raise ValueError(
                    f"{DDO_Color}Unknown subsystem identity '{idin}' in set_Coupling. "
                    f"Expected one of {self._id}.{Reset}"
                )
        finally:
            self._DataLock.release()
    
    def get_StoredCoupling(self, id: str) -> MiddleLevelCouplingInterface | None:
        """Return the stored coupling data for a given subsystem ID (under lock).

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

        Args:
            id: Identifier of the neighbor subsystem whose data to retrieve.

        Returns:
            The stored MiddleLevelCouplingInterface for the given subsystem,
            or None if the coupling data for that slot is None.
        """
        self._DataLock.acquire()
        try:
            if id.lower() == self._id[0].lower():
                return self._couplingdata[0]
            elif id.lower() == self._id[1].lower():
                return self._couplingdata[1]
            else:
                raise ValueError(
                    f"{DDO_Color}Unknown subsystem identity '{id}' in get_StoredCoupling. "
                    f"Expected one of {self._id}.{Reset}"
                )
        finally:
            self._DataLock.release()
    
    def get_ID(self) -> List[str]:
        """Get the identifiers of the connected subsystems.

        Returns:
            List containing parent and child subsystem identifiers.
        """
        # copy.copy() used - List[str] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._id)
    
    def get_CouplingData(self) -> List[MiddleLevelCouplingInterface]:
        """Get all coupling data stored in this middle level.

        Returns:
            List of middle level coupling objects.
        """
        # No copy.copy() used - List[MiddleLevelCouplingInterface] is a list of class objects
        # returned by reference intentionally. This allows the caller to interact with the actual
        # objects. If isolation is needed, the caller should explicitly copy.
        return self._couplingdata
    
    def update_state(self, other_storage: Union['MiddleLevelDataStorageInterface', MiddleLevelDataStorageProxy]) -> None:
        """Update the state of this MiddleLevelDataStorageBasis from another instance.

        This method is necessary for multiprocessing. When subsystems are executed
        in parallel processes via Parallel.py, the original objects need to
        be updated with results from the executed copies. This method preserves
        the memory address of the object's attributes while updating their values.

        Args:
            other_storage: The source instance containing updated values to copy from.
        
        Note on copy operations:
            - _id (List[str]): Updated in-place via update_state_listprimitive()
              to preserve memory address. str elements are immutable,
              no copy.copy() needed for each element.
            - _couplingdata (List[MiddleLevelCouplingInterface]): Updated via nested
              update_state() calls to preserve memory addresses of contained objects.
            - _DataLock: NOT updated - shared lock resource must remain unchanged.
        """
        # Subsystem identifiers - List[str] updated in-place to preserve memory address
        self._id: List[str] = update_state_listprimitive(self._id, other_storage.get_ID())
        
        # Coupling data - class objects updated via nested update_state() calls
        # get_CouplingData() returns reference (no copy), which is intentional here
        for i in range(len(other_storage.get_CouplingData())):
            self._couplingdata[i].update_state(other_storage.get_CouplingData()[i])
        
        # _DataLock is NOT updated - it's a shared synchronization object
