---
title: Centralized_ConvergenceIndicator_Outerloop_DeWit (Source)
---

← Back to [Centralized_ConvergenceIndicator_Outerloop_DeWit documentation](Centralized_ConvergenceIndicator_Outerloop_DeWit.md)

# Centralized_ConvergenceIndicator_Outerloop_DeWit - Source Code

**File:** `Distributed_Design_Optimizer\coordination\convergence\DeWit\Centralized_ConvergenceIndicator_Outerloop_DeWit.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""DeWit centralized outer loop convergence indicator.

Aggregates local outer loop convergence flags from all subsystems.
The coordinator has one instance of this class.
"""

from typing import List
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print, ddo_print_border
from Distributed_Design_Optimizer.coordination.convergence import Centralized_ConvergenceIndicator_Outerloop_Basis
from Distributed_Design_Optimizer.subsystem import SubSystemInterface


class Centralized_ConvergenceIndicator_Outerloop_DeWit(Centralized_ConvergenceIndicator_Outerloop_Basis):
    """Centralized outer loop convergence indicator - DeWit.
    
    Aggregates local convergence flags from all subsystems.
    The coordinator has one instance of this class.
    """
        
    def evaluate(self, subsystems: List[SubSystemInterface]) -> None:
        """Evaluate centralized outer loop convergence across all subsystems.

        First triggers local convergence evaluation in each subsystem,
        then aggregates the results using logical AND.

        Args:
            subsystems: List of all subsystems to check for convergence.
        """
        # Trigger local convergence evaluation in each subsystem
        for subsystem in subsystems:
            subsystem.evaluate_OuterLoopConvergenceIndicator()
        
        # Aggregate: all subsystems must be converged
        self._convouterloop = all(subsystem.get_ConvOuterLoop() for subsystem in subsystems)
    
    def print_beginning_of_centralized_convergenceindicator_outerloop_evaluation(self) -> None:
        """Print a banner before evaluating outer loop convergence via logical AND over all subsystems."""
        name = f"{type(self).__name__}:"
        pad = " " * len(name)
        ddo_print_border()
        ddo_print(f"{name} Starting Outerloop Convergence Evaluation ...")
        ddo_print(f"{pad} Evaluating inconsistencies and outer-loop convergence in each subsystem, then aggregating via logical AND")
        ddo_print_border()
        print()
        
    def print_end_of_centralized_convergenceindicator_outerloop_evaluation(self, subsystems: List[SubSystemInterface]) -> None:
        """Print per-subsystem outer loop convergence flags and the overall aggregated result.

        Args:
            subsystems: List of all subsystems whose outer loop convergence flags are printed.
        """
        name = f"{type(self).__name__}:"
        pad = " " * len(name)
        ddo_print_border()
        ddo_print(f"{name} Finished Outerloop Convergence Evaluation:")
        for subsystem in subsystems:
            ddo_print(f"{pad} SubSystem {subsystem.get_SUBSYSTEMID()} ConvOuterLoop is {subsystem.get_ConvOuterLoop()}")
        ddo_print(f"{pad} Overall ConvOuterLoop (Logical AND over all subsystems) is {self._convouterloop}")
        ddo_print_border()
        print()

    def update_state(self, other: 'Centralized_ConvergenceIndicator_Outerloop_DeWit') -> None:
        """Update the state of this instance with values from another instance.

        Args:
            other: The source instance containing updated values.
        """
        super().update_state(other)

```
