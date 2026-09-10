---
title: Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged (Source)
---

← Back to [Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged documentation](Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged.md)

# Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged - Source Code

**File:** `Distributed_Design_Optimizer\coordination\convergence\AlwaysConverged\Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""AlwaysConverged centralized inner loop convergence indicator for controller subsystems.

This module provides a centralized inner loop convergence indicator whose evaluate()
method always sets convergence to True. Used for controller subsystems (e.g., in ALADIN)
where convergence is determined entirely by the local subsystems.
"""

from typing import List
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print, ddo_print_border
from Distributed_Design_Optimizer.coordination.convergence import Centralized_ConvergenceIndicator_Innerloop_Basis
from Distributed_Design_Optimizer.subsystem import SubSystemInterface


class Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged(Centralized_ConvergenceIndicator_Innerloop_Basis):
    """Centralized inner loop convergence indicator that always returns True.
    
    Used when the centralized convergence check should always pass.
    """
    
    def evaluate(self, subsystems: List[SubSystemInterface]) -> None:
        """Set inner loop convergence to True unconditionally.

        Args:
            subsystems: List of subsystems (unused).
        """
        self._convinnerloop = True

    def print_beginning_of_centralized_convergenceindicator_innerloop_evaluation(self) -> None:
        """Print a banner indicating that inner loop convergence is always True."""
        name = f"{type(self).__name__}:"
        pad = " " * len(name)
        ddo_print_border()
        ddo_print(f"{name} Starting Innerloop Convergence Evaluation ...")
        ddo_print(f"{pad} Convergence is always True (no convergence check performed)")
        ddo_print_border()
        print()
        
    def print_end_of_centralized_convergenceindicator_innerloop_evaluation(self, subsystems: List[SubSystemInterface]) -> None:
        """Print the overall inner loop convergence result (always True).

        Args:
            subsystems: List of all subsystems (unused since convergence is always True).
        """
        name = f"{type(self).__name__}:"
        pad = " " * len(name)
        ddo_print_border()
        ddo_print(f"{name} Finished Innerloop Convergence Evaluation:")
        ddo_print(f"{pad} Overall ConvInnerLoop is {self._convinnerloop}")
        ddo_print_border()
        print()

    def update_state(self, other: 'Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged') -> None:
        """Update the state of this instance with values from another instance.

        Args:
            other: The source instance containing updated values.
        """
        super().update_state(other)

```
