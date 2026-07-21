---
title: LocalObjective0 (Source)
---

← Back to [LocalObjective0 documentation](LocalObjective0.md)

# LocalObjective0 - Source Code

**File:** `userfiles\TwoBarTruss\subsystem0\LocalObjective0.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Local objective module for Two-Bar Truss subsystem 0.

Defines the mass objective function for the system-level FEM subsystem.
"""
from typing import List
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalObjectiveInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis, ScalerZeroOne


class LocalObjective0(LocalObjectiveInterface):
    """Local objective class for Two-Bar Truss subsystem 0.

    Evaluates total truss mass normalized by the mass-normalization parameter.

    Attributes:
        None specific to this class; inherits from LocalObjectiveInterface.
    """

    def __init__(self) -> None:
        """Initialize LocalObjective0 instance."""
        pass

    def evaluateLocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the local objective function for subsystem 0.

        Computes the normalized mass objective M / M_max.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Local objective                      ###
        ################################################################
        # compute local objective, if no local objective simply set localobjective = 0.0
        
        localobjective_unscaled = responses[0] / 0.17
        
        # scale the local objective function evaluation
        localobjective = scalers[4].transform(localobjective_unscaled)
        
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
        # The TwoBarTruss responses are computed from a finite-element analysis
        # (complex physics), so no closed-form gradient is available. Return None
        # to let the framework fall back to its internal finite-difference
        # computation.
        return None

    def evaluate_Hessian_LocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessian of the local objective function.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        # No closed-form Hessian available (complex physics); return None to let
        # the framework fall back to its internal finite-difference computation.
        return None

```
