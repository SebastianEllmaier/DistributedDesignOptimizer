---
title: ConvergenceIndicator_Innerloop_Interface (Source)
---

← Back to [ConvergenceIndicator_Innerloop_Interface documentation](ConvergenceIndicator_Innerloop_Interface.md)

# ConvergenceIndicator_Innerloop_Interface - Source Code

**File:** `Distributed_Design_Optimizer\coordination\convergence\ConvergenceIndicator_Innerloop_Interface.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Interface module for inner loop convergence indicators.

This module defines the abstract interface for inner loop convergence indicators
used in distributed optimization coordination.
"""

from abc import ABC, abstractmethod
from Distributed_Design_Optimizer.coordination.convergence import (Local_ConvergenceIndicator_Innerloop_Interface,
                                                                   Centralized_ConvergenceIndicator_Innerloop_Interface)


class ConvergenceIndicator_Innerloop_Interface(ABC):
    """Abstract interface for inner loop convergence indicators.

    This interface defines the contract for creating local and centralized
    convergence indicators for the inner loop of distributed optimization.
    
    The inner loop convergence typically checks if the total objective function
    has stabilized (small relative change between iterations).
    """

    @abstractmethod
    def createLocalConvergenceIndicator(self) -> Local_ConvergenceIndicator_Innerloop_Interface:
        """Create a local convergence indicator for a subsystem.

        Returns:
            Local_ConvergenceIndicator_Innerloop_Interface: A local convergence indicator instance.
        """

    @abstractmethod
    def createCentralizedConvergenceIndicator(self) -> Centralized_ConvergenceIndicator_Innerloop_Interface:
        """Create a centralized convergence indicator for the coordinator.

        Returns:
            Centralized_ConvergenceIndicator_Innerloop_Interface: A centralized convergence indicator instance.
        """

    @abstractmethod
    def validate_inputs(self) -> None:
        """Validate the inputs/hyperparameters of this convergence indicator.
        
        Raises:
            ValueError: If any parameter is outside the allowed range.
        """
        
    @abstractmethod
    def print_startup_summary(self) -> None:
        """Print the inner loop convergence indicator configuration at startup."""
    
    @abstractmethod
    def print_termination_summary(self) -> None:
        """Print the inner loop convergence indicator configuration at the end."""

```
