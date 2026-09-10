# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Middle-level coupling basis module.

This module provides the base class for middle-level coupling parameters
between subsystems in distributed optimization.
"""

from Distributed_Design_Optimizer.middlelevel import MiddleLevelCouplingInterface


class MiddleLevelCouplingBasis(MiddleLevelCouplingInterface):
    
    """
    A MiddleLevelCoupling subclass object holds the coupling parameters between a subsystem and a single neighbor / controller. 
    It stores the identifier of the neighbor and stores the couplingvariables
    """
    
    def __init__(self, id: str) -> None:
        """Initialize the middle level coupling basis.

        Args:
            id: Identifier of the neighboring subsystem.
        """
        self._id: str = id

    def get_ID(self) -> str:
        """Get the identifier of the neighboring subsystem.

        Returns:
            The neighbor subsystem identifier.
        """
        # No copy.copy() needed - str is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding;
        # modifications there won't affect this class's attribute.
        return self._id
    
    def update_state(self, other_middlelevelcoupling: 'MiddleLevelCouplingBasis') -> None:
        """Update the state of this MiddleLevelCouplingBasis from another instance.

        This method is necessary for multiprocessing. When subsystems are executed
        in parallel processes via Parallel.py, the original objects need to
        be updated with results from the executed copies. This method preserves
        the memory address of the object's attributes while updating their values.

        Args:
            other_middlelevelcoupling: The source instance containing updated values to copy from.
        
        Note on copy operations:
            - _id (str): No copy.copy() needed - str is immutable in Python.
              Assigning creates a new binding; the original cannot be modified.
        """
        # Identifier - str is immutable, no copy.copy() needed
        self._id: str = other_middlelevelcoupling.get_ID()
