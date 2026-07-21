---
title: ConvergenceIndicator_Outerloop_DeWit (Source)
---

← Back to [ConvergenceIndicator_Outerloop_DeWit documentation](ConvergenceIndicator_Outerloop_DeWit.md)

# ConvergenceIndicator_Outerloop_DeWit - Source Code

**File:** `Distributed_Design_Optimizer\coordination\convergence\DeWit\ConvergenceIndicator_Outerloop_DeWit.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""DeWit outer loop convergence indicator factory.

This module implements the DeWit convergence criterion factory for the outer loop,
which creates local and centralized convergence indicators that check if all
inconsistencies and coupling parameter changes are within tolerance.
"""

from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print, ddo_print_border
from Distributed_Design_Optimizer.coordination.convergence import ConvergenceIndicator_Outerloop_Interface
from Distributed_Design_Optimizer.coordination.convergence.DeWit.Local_ConvergenceIndicator_Outerloop_DeWit import Local_ConvergenceIndicator_Outerloop_DeWit
from Distributed_Design_Optimizer.coordination.convergence.DeWit.Centralized_ConvergenceIndicator_Outerloop_DeWit import Centralized_ConvergenceIndicator_Outerloop_DeWit


class ConvergenceIndicator_Outerloop_DeWit(ConvergenceIndicator_Outerloop_Interface):
    """DeWit outer loop convergence indicator factory.
    
    Creates local and centralized convergence indicators that check if all
    inconsistencies and coupling parameter changes are within tolerance.
    
    Attributes:
        _toleranceconsistency: Tolerance for consistency constraints and coupling changes.
    """
    
    def __init__(self, toleranceconsistency: float) -> None:
        """Initialize the DeWit outer loop convergence indicator.

        Args:
            toleranceconsistency: Tolerance for consistency constraints (typical value: 1E-4).
        """
        # Hyperparameter Validation Bounds
        self._toleranceconsistency_allowed_min: float = 0.0
        self._toleranceconsistency_allowed_max: float = float('inf')
        self._toleranceconsistency_rec_min: float = 1e-5
        self._toleranceconsistency_rec_max: float = 1e-2
        
        self._toleranceconsistency: float = toleranceconsistency
        
        self.validate_inputs()
        
    def validate_inputs(self) -> None:
        """Validate the inputs provided to the convergence indicator.
        
        Raises:
            ValueError: If any parameter is outside the allowed range.
        """
        if not (self._toleranceconsistency_allowed_min < self._toleranceconsistency < self._toleranceconsistency_allowed_max):
            raise ValueError(
                f"{DDO_Color}toleranceconsistency must be in ({self._toleranceconsistency_allowed_min}, {self._toleranceconsistency_allowed_max}), "
                f"but got {self._toleranceconsistency}.{Reset}"
            )
        elif not (self._toleranceconsistency_rec_min <= self._toleranceconsistency <= self._toleranceconsistency_rec_max):
            ddo_print_border()
            ddo_print(f"WARNING: toleranceconsistency={self._toleranceconsistency} is outside the recommended range "
                      f"[{self._toleranceconsistency_rec_min}, {self._toleranceconsistency_rec_max}].")
            ddo_print_border()
    
    def createLocalConvergenceIndicator(self) -> Local_ConvergenceIndicator_Outerloop_DeWit:
        """Create a local convergence indicator for subsystem-level evaluation.

        Returns:
            Local_ConvergenceIndicator_Outerloop_DeWit: A new local convergence indicator instance.
        """
        return Local_ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=self._toleranceconsistency)
    
    def createCentralizedConvergenceIndicator(self) -> Centralized_ConvergenceIndicator_Outerloop_DeWit:
        """Create a centralized convergence indicator for coordinator-level evaluation.

        Returns:
            Centralized_ConvergenceIndicator_Outerloop_DeWit: A new centralized convergence indicator instance.
        """
        return Centralized_ConvergenceIndicator_Outerloop_DeWit()
    
    def get_ToleranceConsistency(self) -> float:
        """Get the tolerance for consistency convergence.

        Returns:
            The consistency tolerance threshold value.
        """
        return self._toleranceconsistency
    
    def print_startup_summary(self) -> None:
        """Print the consistency tolerance used for outer loop convergence."""
        ddo_print(f"{type(self).__name__}:     toleranceconsistency:    {self._toleranceconsistency}", indent=1)

    def print_termination_summary(self) -> None:
        """Print the consistency tolerance used for outer loop convergence."""
        ddo_print(f"{type(self).__name__}:     toleranceconsistency:    {self._toleranceconsistency}", indent=1)

```
