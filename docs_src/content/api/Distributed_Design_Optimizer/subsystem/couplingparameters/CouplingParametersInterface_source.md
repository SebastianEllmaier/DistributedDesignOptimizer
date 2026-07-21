---
title: CouplingParametersInterface (Source)
---

← Back to [CouplingParametersInterface documentation](CouplingParametersInterface.md)

# CouplingParametersInterface - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\couplingparameters\CouplingParametersInterface.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Coupling parameters interface module.

This module defines the abstract interface for coupling parameters
in multilevel coordination.
"""

from abc import ABC, abstractmethod
from Distributed_Design_Optimizer.middlelevel import MiddleLevelCouplingInterface


class CouplingParametersInterface(ABC):
    """Interface for coupling parameters between subsystems.

    A CouplingParameters object holds the coupling parameters between
    a subsystem and a single neighbor. It stores the identifier of the neighbor
    and stores the couplingvariables.
    """

    @abstractmethod
    def get_ID(self) -> str:
        """Return the identifier of the neighboring subsystem.

        Returns:
            The neighbor identifier.
        """
        
    @abstractmethod
    def CopyFromMiddleLevelCoupling(self, middlelevelcouplingIn: MiddleLevelCouplingInterface) -> None:
        """Copy coupling parameters from the middle level.

        Args:
            middlelevelcouplingIn: The middle level coupling to copy from.
        """
    
    @abstractmethod    
    def CopyToMiddleLevelCoupling(self, middlelevelcouplingIn: MiddleLevelCouplingInterface) -> None:
        """Copy coupling parameters to the middle level.

        Args:
            middlelevelcouplingIn: The middle level coupling to copy to.
        """

    @abstractmethod
    def update_state(self, other_coupling: 'CouplingParametersInterface') -> None:
        """Update the state of this object with values from another instance.

        This method is necessary for multiprocessing. When subsystems are executed in parallel
        using multiprocessing.Pool, they are serialized and deserialized, creating new objects
        in separate memory spaces. After parallel execution completes, this method updates
        the original object's attribute values while preserving their memory addresses.

        Implementation Guidelines for Subclasses:
            - Call super().update_state(other_coupling=other_coupling) first to handle inherited attributes
            - For primitives (str, float, int, bool, None): Use direct assignment
            - For List[float]: Use update_state_listprimitive() for in-place updates
            - For List[List[float]]: Iterate and use update_state_listprimitive() per inner list
            - For nested class objects: Call their update_state() methods
            - Maintain the same attribute order as defined in __init__()

        Args:
            other_coupling: The source CouplingParametersInterface containing updated values
                from parallel execution.
        """

```
