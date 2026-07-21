# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Controller middle-level coupling basis module.

This module provides the base class for controller-side middle-level coupling
parameters in distributed optimization.
"""


from Distributed_Design_Optimizer.middlelevel import MiddleLevelCouplingBasis


class LocalController_MiddleLevelCouplingBasis(MiddleLevelCouplingBasis):
    """Base class for controller-side middle-level coupling parameters."""
    
    def __init__(self, id: str) -> None:
        """Initialize the controller middle level coupling.

        Args:
            id: Identifier of the neighboring subsystem.
        """
        
        super().__init__(id=id)
    
    def update_state(self, other_middlelevelcoupling: 'LocalController_MiddleLevelCouplingBasis') -> None:
        """Update the state of this instance from another instance.

        This method is necessary for multiprocessing. When subsystems are executed
        in parallel processes via Parallel.py, the original objects need to
        be updated with results from the executed copies. This method preserves
        the memory address of the object's attributes while updating their values.
        
        This class delegates entirely to the base class update_state() which handles:
        - _id: Identifier of the neighboring subsystem (str)

        Args:
            other_middlelevelcoupling: The source instance containing updated values to copy from.
        """
        super().update_state(other_middlelevelcoupling=other_middlelevelcoupling)
        