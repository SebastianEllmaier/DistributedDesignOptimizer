---
title: MiddleLevelCouplingInterface (Source)
---

← Back to [MiddleLevelCouplingInterface documentation](MiddleLevelCouplingInterface.md)

# MiddleLevelCouplingInterface - Source Code

**File:** `Distributed_Design_Optimizer\middlelevel\MiddleLevelCouplingInterface.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Interface module for middle-level coupling.

This module defines the abstract interface for middle-level coupling
between subsystems in distributed optimization.
"""

from abc import ABC, abstractmethod


class MiddleLevelCouplingInterface(ABC):
    """Abstract interface for middle-level coupling.
    
    A MiddleLevelCoupling object holds the coupling parameters between a subsystem and a single neighbor. 
    It stores the identifier of the neighbor and stores the couplingvariables

    The storage is defined as follows:
    Consider two coupled subsystems

                             subsystem 0
                        //                 \\

         mapped response 0 -> 1         expected response 1 -> 0


         expected response 0 -> 1       mapped response 1 -> 0

                        \\                  //
                             subsystem 1

    Consider that the reponses are stored locally for subsystem 0. Then:
    mapped response 0 -> 1   is called mappedresponses
    expected response 1 -> 0 is called couplingvariable
    and
    expected response 0 -> 1 is called couplingvariable
    mapped response 1 -> 0   is called mappedresponses
    """
    
    @abstractmethod
    def get_ID(self) -> str:
        """Get the identifier of the neighboring subsystem.

        Returns:
            The neighbor subsystem identifier.
        """

    @abstractmethod
    def update_state(self, other_middlelevelcoupling: 'MiddleLevelCouplingInterface') -> None:
        """Update the state of this MiddleLevelCouplingInterface from another instance.

        This method is necessary for multiprocessing. When subsystems are executed
        in parallel processes via Parallel.py, the original objects need to
        be updated with results from the executed copies. Implementations must
        preserve the memory address of the object's attributes while updating
        their values.

        Args:
            other_middlelevelcoupling: The source instance containing updated values to copy from.
        
        Note:
            Implementations should follow these copy operation guidelines:
            - Primitives (str, float, int, None): No copy.copy() needed (immutable types)
            - List[float]: Use update_state_listprimitive() for in-place updates
            - Class objects: Call nested update_state() methods
        """

```
