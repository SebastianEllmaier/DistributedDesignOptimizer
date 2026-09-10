---
title: ConvergenceIndicator_Innerloop_DeWit (Source)
---

← Back to [ConvergenceIndicator_Innerloop_DeWit documentation](ConvergenceIndicator_Innerloop_DeWit.md)

# ConvergenceIndicator_Innerloop_DeWit - Source Code

**File:** `Distributed_Design_Optimizer\coordination\convergence\DeWit\ConvergenceIndicator_Innerloop_DeWit.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""DeWit inner loop convergence indicator factory.

This module provides the DeWit factory for inner loop convergence indicators
based on the relative change of the total objective function between iterations.

Convergence criterion: |f_new - f_old| / (1 + |f_new|) <= tolerance
"""

from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print
from Distributed_Design_Optimizer.coordination.convergence import ConvergenceIndicator_Innerloop_Interface
from Distributed_Design_Optimizer.coordination.convergence.DeWit.Local_ConvergenceIndicator_Innerloop_DeWit import Local_ConvergenceIndicator_Innerloop_DeWit
from Distributed_Design_Optimizer.coordination.convergence.DeWit.Centralized_ConvergenceIndicator_Innerloop_DeWit import Centralized_ConvergenceIndicator_Innerloop_DeWit


class ConvergenceIndicator_Innerloop_DeWit(ConvergenceIndicator_Innerloop_Interface):
    """Inner loop convergence indicator factory - DeWit.
    
    This class creates local and centralized convergence indicators
    based on the relative change of the total objective function.
    
    Used in InputFile:
        ALC(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1e-5), ...)
    """
    
    def __init__(self, tolerancetotalobjective: float) -> None:
        """Initialize the convergence indicator factory.
        
        Args:
            tolerancetotalobjective: Tolerance for relative change in total objective.
        """
        # Hyperparameter Validation Bounds:
        # tolerancetotalobjective: must be > 0
        self._tolerancetotalobjective_allowed_min: float = 0.0         # strict (>)
        self._tolerancetotalobjective_allowed_max: float = float('inf') # strict (<), inf bounds are always exclusive
        
        self._tolerancetotalobjective: float = tolerancetotalobjective
        self.validate_inputs()
        
    def validate_inputs(self) -> None:
        """Validate the inputs/hyperparameters.
        
        Raises:
            ValueError: If tolerancetotalobjective is not positive.
        """
        # ===== tolerancetotalobjective Validation =====
        # Allowed: > 0 (strict)
        if not (self._tolerancetotalobjective_allowed_min < self._tolerancetotalobjective < self._tolerancetotalobjective_allowed_max):
            raise ValueError(
                f"{DDO_Color}tolerancetotalobjective must be in ({self._tolerancetotalobjective_allowed_min}, {self._tolerancetotalobjective_allowed_max}), "
                f"but got {self._tolerancetotalobjective}.{Reset}"
            )
    
    def createLocalConvergenceIndicator(self) -> Local_ConvergenceIndicator_Innerloop_DeWit:
        """Create a local convergence indicator for a subsystem.
        
        Called in ALC.createSubSystems() for each subsystem.
        
        Returns:
            Local_ConvergenceIndicator_Innerloop_DeWit: A local convergence indicator instance.
        """
        return Local_ConvergenceIndicator_Innerloop_DeWit(
            tolerancetotalobjective=self._tolerancetotalobjective
        )
    
    def createCentralizedConvergenceIndicator(self) -> Centralized_ConvergenceIndicator_Innerloop_DeWit:
        """Create a centralized convergence indicator for the coordinator.
        
        Called in Coordinator.__init__().
        
        Returns:
            Centralized_ConvergenceIndicator_Innerloop_DeWit: A centralized convergence indicator instance.
        """
        return Centralized_ConvergenceIndicator_Innerloop_DeWit()
    
    def get_ToleranceTotalObjective(self) -> float:
        """Get the tolerance for the total objective convergence.

        Returns:
            The total objective tolerance threshold value.
        """
        return self._tolerancetotalobjective
    
    def print_startup_summary(self) -> None:
        """Print the total objective tolerance used for inner loop convergence."""
        ddo_print(f"{type(self).__name__}:     tolerancetotalobjective:     {self._tolerancetotalobjective}", indent=1)

    def print_termination_summary(self) -> None:
        """Print the total objective tolerance used for inner loop convergence."""
        ddo_print(f"{type(self).__name__}:     tolerancetotalobjective:     {self._tolerancetotalobjective}", indent=1)
```
