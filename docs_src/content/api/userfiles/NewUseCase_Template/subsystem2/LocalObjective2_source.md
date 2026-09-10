---
title: LocalObjective2 (Source)
---

← Back to [LocalObjective2 documentation](LocalObjective2.md)

# LocalObjective2 - Source Code

**File:** `userfiles\NewUseCase_Template\subsystem2\LocalObjective2.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Local objective module for Subsystem 2 in the new use-case.

This module defines the LocalObjective2 class which implements the local
objective function computation for Subsystem 2 in the distributed design
optimization framework.
"""
from typing import List
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalObjectiveInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis, ScalerZeroOne


class LocalObjective2(LocalObjectiveInterface):
    """Local objective class for Subsystem 2.

    Implements the LocalObjectiveInterface to compute the local objective
    function contribution for Subsystem 2 in the new use-case.
    This subsystem has no local objective (set to None).

    Attributes:
        None specific to this class; inherits from LocalObjectiveInterface.
    """
    def __init__(self) -> None:
        """Initialize the LocalObjective2 instance."""
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
            subsystem: The local subsystem instance.
        """
        # === Tutorial: scaled <-> unscaled gradients (chain rule) ==================
        # The optimizer works in SCALED [0,1] space, so this gradient must be
        # d(scaled objective) / d(scaled design variables). Every affine scaler has a
        # constant slope  scaler.get_scale() = d(scaled)/d(unscaled). If you derive the
        # objective derivatives in UNSCALED space (df/dx_j), convert them component-wise:
        #     df_s/ds_j = get_scale(obj) * df/dx_j / get_scale(x_j)
        # Return None instead to let the framework use finite-difference gradients.
        # ===========================================================================
        
        return None
    
    def evaluate_Hessian_LocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessian of the local objective function.

        Args:
            subsystem: The local subsystem instance.
        """
        # === Tutorial: scaled <-> unscaled Hessian (chain rule, 2nd order) =========
        # The optimizer works in SCALED [0,1] space, so this Hessian must be
        # d^2(scaled objective) / d(scaled design vars)^2. Each affine scaler has a
        # constant slope scaler.get_scale() = d(scaled)/d(unscaled). From the UNSCALED
        # second derivatives (d^2f/dx_j dx_k) convert element-wise:
        #     d2f_s/ds_j ds_k = get_scale(obj) * d2f/dx_j dx_k / (get_scale(x_j)*get_scale(x_k))
        # Return None instead to let the framework use finite-difference Hessians.
        # ===========================================================================
        
        return None
```
