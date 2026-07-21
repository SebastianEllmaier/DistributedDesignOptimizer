---
title: Centralized_ConvergenceIndicator_Innerloop_Basis (Source)
---

← Back to [Centralized_ConvergenceIndicator_Innerloop_Basis documentation](Centralized_ConvergenceIndicator_Innerloop_Basis.md)

# Centralized_ConvergenceIndicator_Innerloop_Basis - Source Code

**File:** `Distributed_Design_Optimizer\coordination\convergence\Centralized_ConvergenceIndicator_Innerloop_Basis.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Base implementation for centralized inner loop convergence indicators."""

from Distributed_Design_Optimizer.coordination.convergence import Centralized_ConvergenceIndicator_Innerloop_Interface
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print

class Centralized_ConvergenceIndicator_Innerloop_Basis(Centralized_ConvergenceIndicator_Innerloop_Interface):
    """Base class for centralized inner loop convergence indicators.

    Provides default storage and accessor for the inner loop convergence flag.
    """

    def __init__(self) -> None:
        """Initialize with convergence flag set to False."""
        self._convinnerloop: bool = False
        
    def get_ConvInnerLoop(self) -> bool:
        """Return the current inner loop convergence flag.

        Returns:
            bool: True if inner loop has converged, False otherwise.
        """
        return self._convinnerloop

    def print_convergence_result(self) -> None:
        """Print the current innerloop convergence state."""
        ddo_print(f"{type(self).__name__}: Innerloop Convergence Indicator is {self.get_ConvInnerLoop()}")

    def update_state(self, other: 'Centralized_ConvergenceIndicator_Innerloop_Basis') -> None:
        """Update the state of this instance with values from another instance.

        Args:
            other: The source instance containing updated values.
        """
        # No copy.copy() needed - bool is a primitive/immutable type
        self._convinnerloop = other._convinnerloop

```
