---
title: Local_ConvergenceIndicator_Outerloop_Interface (Source)
---

← Back to [Local_ConvergenceIndicator_Outerloop_Interface documentation](Local_ConvergenceIndicator_Outerloop_Interface.md)

# Local_ConvergenceIndicator_Outerloop_Interface - Source Code

**File:** `Distributed_Design_Optimizer\coordination\convergence\Local_ConvergenceIndicator_Outerloop_Interface.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Interface module for local outer loop convergence indicators.

This module defines the abstract interface for local outer loop convergence
indicators that are evaluated within each subsystem.
"""

from abc import ABC, abstractmethod
from Distributed_Design_Optimizer.subsystem import SubSystemInterface


class Local_ConvergenceIndicator_Outerloop_Interface(ABC):
    """Abstract interface for local outer loop convergence indicators.

    This interface defines the contract for evaluating outer loop convergence
    at the subsystem level. Each subsystem has its own local convergence indicator
    that checks if the outer loop criteria (consistency, coupling parameter changes)
    are satisfied.
    """

    @abstractmethod
    def evaluate(self, subsystem: SubSystemInterface) -> bool:
        """Evaluate if local outer loop convergence criteria is met.

        The convergence indicator retrieves the data it needs from the subsystem.
        This allows different convergence criteria to access different data
        (e.g., inconsistencies, coupling parameters, etc.).

        Args:
            subsystem: The subsystem to evaluate convergence for.

        Returns:
            bool: True if convergence condition is met, False otherwise.
        """

    @abstractmethod
    def update_state(self, other: 'Local_ConvergenceIndicator_Outerloop_Interface') -> None:
        """Update the state of this convergence indicator with the state of another.

        This operation preserves the memory address of the object's attributes
        while updating their values. Required for multiprocessing synchronization.

        Args:
            other: The convergence indicator to copy state from.
        """

```
