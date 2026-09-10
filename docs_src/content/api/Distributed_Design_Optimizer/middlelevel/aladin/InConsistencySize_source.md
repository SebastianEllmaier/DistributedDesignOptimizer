---
title: InConsistencySize (Source)
---

← Back to [InConsistencySize documentation](InConsistencySize.md)

# InConsistencySize - Source Code

**File:** `Distributed_Design_Optimizer\middlelevel\aladin\InConsistencySize.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Inconsistency size computation module for ALADIN.

This module provides functionality for computing inconsistency sizes
between coupled variables in ALADIN coordination.
"""

from Distributed_Design_Optimizer.middlelevel import InConsistencySizeBasis


class InConsistencySize(InConsistencySizeBasis):
    """Computes inconsistency sizes for ALADIN coordination.

    Measures the inconsistency between coupled variables from different subsystems.
    """

    def __init__(self,
                 id: str) -> None:
        """Initialize the ALADIN inconsistency size.

        Args:
            id: Identifier for this inconsistency size instance.
        """
        # call __init__() of InConsistencySizeBasis
        super().__init__(id)
        
    def update_state(self, other_inconsistency: 'InConsistencySize') -> None:
        """Update the state of this InConsistencySize with the state of another InConsistencySize.

        This operation preserves the memory address of the object's attributes
        and only updates the value(s). This method is necessary for multiprocessing,
        where executed subsystems need to transfer their state back to the original objects.

        This subclass has no additional attributes beyond the base class,
        so it simply delegates to the base class update_state.

        Args:
            other_inconsistency: The InConsistencySize to copy state from.
        """
        # Call base class update_state to handle all attributes defined in InConsistencySizeBasis
        super().update_state(other_inconsistency)

```
