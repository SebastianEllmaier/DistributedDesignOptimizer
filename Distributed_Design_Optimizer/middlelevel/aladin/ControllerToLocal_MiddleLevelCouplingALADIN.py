# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Controller-to-local middle-level coupling module for ALADIN.

This module provides middle-level coupling management for controller-to-local
subsystem communication in ALADIN coordination.
"""

import copy
from typing import List
from Distributed_Design_Optimizer.middlelevel import ControllerToLocal_MiddleLevelCouplingBasis
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive


class ControllerToLocal_MiddleLevelCouplingALADIN(ControllerToLocal_MiddleLevelCouplingBasis):
    """Middle level coupling updated by the controller.

    Handles the coupling from the controller to a local subsystem
    (middlelevel between controller and local subsystem).
    """
    
    def __init__(self, local_neighbors_list: List[str]) -> None:
        """Initialize controller-to-local middle-level coupling.

        Args:
            local_neighbors_list: List of local neighbor identifiers.
        """
        # Call init of ControllerToLocal_MiddleLevelCouplingBasis
        super().__init__()

        self._delta_d: List[float] | None = None

    # Getter and setter for delta_d
    def get_Delta_D(self) -> List[float] | None:
        """Return the list delta_d from controller.

        Returns:
            List[float] | None: The delta_d list from the controller.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._delta_d)
    
    def set_Delta_D(self, delta_d_in: List[float]) -> None:
        """Set the list delta_d from controller.

        Args:
            delta_d_in (List[float]): The delta_d list to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._delta_d = copy.copy(delta_d_in)
        
    def update_state(self, other_middlelevelcoupling: 'ControllerToLocal_MiddleLevelCouplingALADIN') -> None:
        """Update the state of this ControllerToLocal_MiddleLevelCouplingALADIN with another instance.

        This operation preserves the memory address of the object's attributes
        and only updates the value(s). This method is necessary for multiprocessing,
        where executed subsystems need to transfer their state back to the original objects.

        Args:
            other_middlelevelcoupling: The ControllerToLocal_MiddleLevelCouplingALADIN to copy state from.
        """
        # Call the base class update_state to handle common attributes
        super().update_state(other_middlelevelcoupling)
        
        # Update delta_d using update_state_listprimitive to preserve memory address
        self._delta_d: List[float] | None = update_state_listprimitive(self._delta_d, other_middlelevelcoupling.get_Delta_D())
