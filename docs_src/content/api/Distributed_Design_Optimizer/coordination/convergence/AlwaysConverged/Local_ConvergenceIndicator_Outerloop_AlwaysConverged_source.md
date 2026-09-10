---
title: Local_ConvergenceIndicator_Outerloop_AlwaysConverged (Source)
---

← Back to [Local_ConvergenceIndicator_Outerloop_AlwaysConverged documentation](Local_ConvergenceIndicator_Outerloop_AlwaysConverged.md)

# Local_ConvergenceIndicator_Outerloop_AlwaysConverged - Source Code

**File:** `Distributed_Design_Optimizer\coordination\convergence\AlwaysConverged\Local_ConvergenceIndicator_Outerloop_AlwaysConverged.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""AlwaysConverged local outer loop convergence indicator for controller subsystems.

This module provides a local outer loop convergence indicator whose evaluate() method
always returns True. Used for controller subsystems (e.g., in ALADIN)
where convergence is determined entirely by the local subsystems.
"""

from Distributed_Design_Optimizer.coordination.convergence import Local_ConvergenceIndicator_Outerloop_Interface
from Distributed_Design_Optimizer.subsystem import SubSystemInterface


class Local_ConvergenceIndicator_Outerloop_AlwaysConverged(Local_ConvergenceIndicator_Outerloop_Interface):
    """Local outer loop convergence indicator that always returns True.
    
    Used for controller subsystems where outer loop convergence is not evaluated.
    """
    
    def evaluate(self, subsystem: SubSystemInterface) -> bool:
        """Always returns True.

        Args:
            subsystem: The subsystem to evaluate convergence for (unused).

        Returns:
            bool: Always True.
        """
        return True
    
    def update_state(self, other: 'Local_ConvergenceIndicator_Outerloop_AlwaysConverged') -> None:
        """No state to update.

        Args:
            other: The convergence indicator to copy state from (unused).
        """
        pass

```
