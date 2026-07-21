---
title: LocalObjective1 (Source)
---

← Back to [LocalObjective1 documentation](LocalObjective1.md)

# LocalObjective1 - Source Code

**File:** `userfiles\Sellar\subsystem1\LocalObjective1.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Local objective module for Sellar subsystem 1.

Defines the local objective function contribution from subsystem 1
in the Sellar distributed optimization problem.
"""

from typing import List
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalObjectiveInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis, ScalerZeroOne


class LocalObjective1(LocalObjectiveInterface):
    """Local objective class for Sellar subsystem 1.

    Subsystem 1 has no local objective contribution (set to None).

    Attributes:
        None specific to this class; inherits from LocalObjectiveInterface.
    """

    def __init__(self) -> None:
        """Initialize LocalObjective1 instance."""
        pass

    def evaluateLocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the local objective function for subsystem 1.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Local objective                      ###
        ################################################################
        # compute local objective
        
        # localobjective_unscaled = responses[...]
            
        # scale the local objective function evaluation
        scaler: ScalerZeroOne = scalers[3]
        # localobjective = scaler.transform(localobjective_unscaled)
        
        # or if no Local objective exist:
        localobjective = None
        
        # localobjective needs to be a scaled01 quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################        
        subsystem.set_LocalObjectiveValue(localobjective)

    def evaluate_Gradient_LocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the gradient of the local objective function.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        
        return None

    def evaluate_Hessian_LocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessian of the local objective function.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        
        return None

```
