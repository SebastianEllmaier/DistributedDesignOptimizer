# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Middle-level coupling for penalty coordination.

This module provides middle-level coupling management for
penalty-based coordination.
"""

from Distributed_Design_Optimizer.middlelevel import SubSysMiddleLevelCouplingBasis


class MiddleLevelCouplingPC(SubSysMiddleLevelCouplingBasis):
    """Middle level coupling for penalty coordination.

    Stores coupling data between subsystems using penalty
    coordination method.
    """

    def __init__(self, id: str) -> None:
        """Initialize the middle level coupling.

        Args:
            id: Identifier of the neighboring subsystem.
        """
        # call __init__() of MiddleLevelCouplingBasis
        super().__init__(id)
    
    def update_state(self, other_middlelevelcoupling: 'MiddleLevelCouplingPC') -> None:
        """Update the state from another middle level coupling instance.
        
        This method updates the numerical information stored in the class's attributes
        without changing the original memory address location. This is necessary for
        multiprocessing, where executed subsystems return from separate processes and
        their state must be transferred back to the original objects in the main process.

        Args:
            other_middlelevelcoupling: Source instance to copy state from.
        
        Note:
            This class defines no additional attributes beyond the base class.
            All relevant attributes are updated via the base class update_state().
        """
        # Call the base class update_state to handle all attributes
        super().update_state(other_middlelevelcoupling)
