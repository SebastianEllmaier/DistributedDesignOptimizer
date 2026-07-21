---
title: LocalObjective0 (Source)
---

← Back to [LocalObjective0 documentation](LocalObjective0.md)

# LocalObjective0 - Source Code

**File:** `userfiles\SSBJ\subsystem0\LocalObjective0.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Local objective module for Subsystem 0 in the Supersonic Business Jet (SSBJ) problem."""
from typing import List
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalObjectiveInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis


class LocalObjective0(LocalObjectiveInterface):
    """Local objective class for Subsystem 0: minimize total aircraft weight.

    Attributes:
        None specific to this class; inherits from LocalObjectiveInterface.
    """

    def __init__(self) -> None:
        """Initialize LocalObjective0 instance."""
        pass

    def evaluateLocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the local objective function for Subsystem 0.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Local objective                      ###
        ################################################################
        # Minimize total_weight = responses[1] [lb]
        localobjective_unscaled = responses[1]

        # scale using the total_weight scaler (scalers[5] = local objective scaler)
        localobjective = scalers[5].transform(localobjective_unscaled)

        # localobjective needs to be a scaled01 quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        subsystem.set_LocalObjectiveValue(localobjective)

    def evaluate_Gradient_LocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the gradient of the local objective function.

        Args:
            subsystem: Local subsystem instance.
        """
        # The SSBJ responses are computed from complex physics (BLISS discipline
        # analyses), so no closed-form gradient is available. Return None to let
        # the framework fall back to its internal finite-difference computation.
        return None

    def evaluate_Hessian_LocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessian of the local objective function.

        Args:
            subsystem: Local subsystem instance.
        """
        # No closed-form Hessian available (complex physics); return None to let
        # the framework fall back to its internal finite-difference computation.
        return None

```
