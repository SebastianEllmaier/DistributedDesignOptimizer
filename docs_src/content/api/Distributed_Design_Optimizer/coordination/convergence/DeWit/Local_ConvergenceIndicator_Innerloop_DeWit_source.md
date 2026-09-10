---
title: Local_ConvergenceIndicator_Innerloop_DeWit (Source)
---

← Back to [Local_ConvergenceIndicator_Innerloop_DeWit documentation](Local_ConvergenceIndicator_Innerloop_DeWit.md)

# Local_ConvergenceIndicator_Innerloop_DeWit - Source Code

**File:** `Distributed_Design_Optimizer\coordination\convergence\DeWit\Local_ConvergenceIndicator_Innerloop_DeWit.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""DeWit local inner loop convergence indicator.

Evaluates inner loop convergence at the subsystem level based on the relative
change of the total objective function between iterations.

Convergence criterion: |f_new - f_old| / (1 + |f_new|) <= tolerance
"""

from Distributed_Design_Optimizer.coordination.convergence import Local_ConvergenceIndicator_Innerloop_Interface
from Distributed_Design_Optimizer.subsystem import SubSystemInterface


class Local_ConvergenceIndicator_Innerloop_DeWit(Local_ConvergenceIndicator_Innerloop_Interface):
    """Local inner loop convergence indicator - DeWit.
    
    Evaluates convergence based on relative change of total objective.
    Each subsystem has one instance of this class.
    """
    
    def __init__(self, tolerancetotalobjective: float) -> None:
        """Initialize the local convergence indicator.
        
        Args:
            tolerancetotalobjective: Tolerance for relative change in total objective.
        """
        self._tolerancetotalobjective: float = tolerancetotalobjective
    
    def evaluate(self, subsystem: SubSystemInterface) -> bool:
        """Evaluate if local inner loop convergence criteria is met.
        
        Computes: error = |f_new - f_old| / (1 + |f_new|)
        Convergence if error <= tolerance.

        Args:
            subsystem: The subsystem to evaluate convergence for.

        Returns:
            bool: True if convergence condition is met, False otherwise.
        """
        totalobjectiveNew: float | None = subsystem.get_OptimData().get_TotalObjectiveValue()
        totalobjectiveOld: float | None = subsystem.copy_TotalObjective_Previous_outer_or_innerloop_itr()
        
        convergence = True
        
        # totalobjectiveNew is only None if the corresponding subsystem 
        # does not have any local or coordination objective, hence, it 
        # should indicate inner loop convergence
        if totalobjectiveNew is None:
            convergence = True
            
        elif totalobjectiveOld is None:
            convergence = False
        else:
            # compute inner error size
            error = abs(totalobjectiveNew - totalobjectiveOld) / (1 + abs(totalobjectiveNew))
            if error > self._tolerancetotalobjective:
                convergence = False
            
        return convergence
    
    def get_ToleranceTotalObjective(self) -> float:
        """Get the tolerance for the total objective convergence.

        Returns:
            The total objective tolerance threshold value.
        """
        return self._tolerancetotalobjective
    
    def update_state(self, other: 'Local_ConvergenceIndicator_Innerloop_DeWit') -> None:
        """Update the state of this convergence indicator with the state of another.

        Args:
            other: The convergence indicator to copy state from.
        """
        # tolerancetotalobjective is immutable and does not change during optimization
        pass

```
