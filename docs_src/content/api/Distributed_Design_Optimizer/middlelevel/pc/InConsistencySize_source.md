---
title: InConsistencySize (Source)
---

← Back to [InConsistencySize documentation](InConsistencySize.md)

# InConsistencySize - Source Code

**File:** `Distributed_Design_Optimizer\middlelevel\pc\InConsistencySize.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Inconsistency size computation for penalty coordination.

This module provides functionality for computing inconsistency sizes
between coupled variables in penalty coordination.
"""

from Distributed_Design_Optimizer.middlelevel import InConsistencySizeBasis


class InConsistencySize(InConsistencySizeBasis):
    """Inconsistency size storage for penalty coordination.

    Stores coupling inconsistency measurements for the penalty
    coordination method.
    """

    def __init__(self,
                 id: str) -> None:
        """Initialize the inconsistency size storage.

        Args:
            id: Identifier of the neighboring subsystem.
        """
        # call __init__() of InConsistencySizeBasis
        super().__init__(id)
        
    def update_state(self, other_inconsistency: 'InConsistencySize') -> None:
        """Update the state from another inconsistency size instance.
        
        This method updates the numerical information stored in the class's attributes
        without changing the original memory address location. This is necessary for
        multiprocessing, where executed subsystems return from separate processes and
        their state must be transferred back to the original objects in the main process.

        Args:
            other_inconsistency: Source instance to copy state from.
        
        Note:
            This class defines no additional attributes beyond the base class.
            All relevant attributes are updated via the base class update_state().
        """
        # Call the base class update_state to handle all attributes
        super().update_state(other_inconsistency)

```
