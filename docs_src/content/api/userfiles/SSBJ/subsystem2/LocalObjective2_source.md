---
title: LocalObjective2 (Source)
---

← Back to [LocalObjective2 documentation](LocalObjective2.md)

# LocalObjective2 - Source Code

**File:** `userfiles\SSBJ\subsystem2\LocalObjective2.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Local objective module for Subsystem 2 in the Supersonic Business Jet (SSBJ) problem."""
from typing import List
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalObjectiveInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis


class LocalObjective2(LocalObjectiveInterface):
    """Local objective class for Subsystem 2: no local objective.

    Attributes:
        None specific to this class; inherits from LocalObjectiveInterface.
    """

    def __init__(self) -> None:
        """Initialize LocalObjective2 instance."""
        pass

    def evaluateLocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the local objective function for Subsystem 2.

        Computes the local objective value from the subsystem responses,
        scales it using the appropriate scaler, and stores the result
        in the subsystem.

        Args:
            subsystem: The local subsystem instance providing responses
                and scaling variables.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Local objective                      ###
        ################################################################
        # compute local objective

        # localobjective_unscaled = responses[...]

        # scale the local objective function evaluation
        # localobjective = scalers[...].transform(localobjective_unscaled)

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
            subsystem: Local subsystem instance.
        """
        
        return None

    def evaluate_Hessian_LocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessian of the local objective function.

        Args:
            subsystem: Local subsystem instance.
        """
        
        return None

```
