---
title: ConvergenceIndicator_Innerloop_AlwaysConverged (Source)
---

← Back to [ConvergenceIndicator_Innerloop_AlwaysConverged documentation](ConvergenceIndicator_Innerloop_AlwaysConverged.md)

# ConvergenceIndicator_Innerloop_AlwaysConverged - Source Code

**File:** `Distributed_Design_Optimizer\coordination\convergence\AlwaysConverged\ConvergenceIndicator_Innerloop_AlwaysConverged.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""AlwaysConverged inner loop convergence indicator factory for controller subsystems.

This module provides the factory for inner loop convergence indicators whose 
evaluate() method always returns True. Used for controller subsystems (e.g., in ALADIN)
where convergence is determined entirely by the local subsystems.
"""

from Distributed_Design_Optimizer.coordination.convergence import ConvergenceIndicator_Innerloop_Interface
from Distributed_Design_Optimizer.coordination.convergence.AlwaysConverged.Local_ConvergenceIndicator_Innerloop_AlwaysConverged import Local_ConvergenceIndicator_Innerloop_AlwaysConverged
from Distributed_Design_Optimizer.coordination.convergence.AlwaysConverged.Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged import Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged


class ConvergenceIndicator_Innerloop_AlwaysConverged(ConvergenceIndicator_Innerloop_Interface):
    """Inner loop convergence indicator factory that always reports convergence.
    
    Used for controller subsystems where the controller does not participate
    in inner loop convergence decisions.
    """
    
    def createLocalConvergenceIndicator(self) -> Local_ConvergenceIndicator_Innerloop_AlwaysConverged:
        """Create a local convergence indicator that always returns True.
        
        Returns:
            Local_ConvergenceIndicator_Innerloop_AlwaysConverged: A local convergence indicator instance.
        """
        return Local_ConvergenceIndicator_Innerloop_AlwaysConverged()
    
    def createCentralizedConvergenceIndicator(self) -> Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged:
        """Create a centralized convergence indicator that always returns True.
        
        Returns:
            Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged: A centralized convergence indicator instance.
        """
        return Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged()
    
    def validate_inputs(self) -> None:
        """No inputs to validate."""
        pass
    
    def print_startup_summary(self) -> None:
        """Nothing to print."""
        pass

    def print_termination_summary(self) -> None:
        """Nothing to print."""
        pass
```
