---
title: LocalConstraints1 (Source)
---

← Back to [LocalConstraints1 documentation](LocalConstraints1.md)

# LocalConstraints1 - Source Code

**File:** `userfiles\NewUseCase_Template\subsystem1\LocalConstraints1.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Local constraints module for Subsystem 1 in the new use-case.

This module defines the LocalConstraints1 class which implements the local
equality and inequality constraints specific to Subsystem 1 in the distributed
design optimization framework.
"""
from typing import List
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalConstraintsInterface
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis, ScalerConstraint


class LocalConstraints1(LocalConstraintsInterface):
    """Local constraints class for Subsystem 1 in the new use-case."""
    def __init__(self) -> None:
        """Initialize the LocalConstraints1 instance."""
        pass

    def evaluateEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate equality local constraints for Subsystem 1.

        Computes the equality constraint values from the subsystem responses,
        scales them using the appropriate ScalerConstraint, and stores the
        result in the subsystem.

        Args:
            subsystem: The local subsystem instance providing responses
                and scaling variables.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        
        equality_unscaled = []        
        # append any equality Local constraints to this list using the responses        
        ################################################################
        ###          USER CODE: Equality constraints                  ###
        ################################################################
        # equality_unscaled.append(responses[...])
        # equality_unscaled.append(responses[...])  
        
        # scale equality Local constraint evaluation
        scl: List[ScalerConstraint] = [scalers[...]]
        # equality: List[float] = [scl[i].transform(equality_unscaled[i]) for i in range(len(equality_unscaled))]
        
        # or if no Equality Local constraints exist:
        equality = None
       
        # equality Local constraints needs to be a scaled01 quantity        
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################        
        subsystem.set_EqualityLocalConstraintsValue(equality)

    def evaluate_Jacobian_EqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Jacobian of the local equality constraints.

        Args:
            subsystem: The local subsystem instance.
        """
        # === Tutorial: scaled <-> unscaled Jacobian (chain rule) ===================
        # Constraints are handled in SCALED [0,1] space, so this Jacobian must be
        # d(scaled constraint) / d(scaled design variables). Every affine scaler has a
        # constant slope scaler.get_scale() = d(scaled)/d(unscaled). From the UNSCALED
        # derivatives (dg/dx_j) convert each entry:
        #     dg_s/ds_j = get_scale(constraint) * dg/dx_j / get_scale(x_j)
        # Return None instead to let the framework use finite-difference Jacobians.
        # ===========================================================================
        
        return None
    
    def evaluate_Hessians_EqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessians of the local equality constraints.

        Args:
            subsystem: The local subsystem instance.
        """
        # === Tutorial: scaled <-> unscaled Hessians (chain rule, 2nd order) ========
        # Constraints are handled in SCALED [0,1] space, so each Hessian must be
        # d^2(scaled constraint) / d(scaled design vars)^2. Each affine scaler has a
        # constant slope scaler.get_scale() = d(scaled)/d(unscaled). From the UNSCALED
        # second derivatives (d^2g/dx_j dx_k) convert element-wise:
        #     d2g_s/ds_j ds_k = get_scale(constraint) * d2g/dx_j dx_k / (get_scale(x_j)*get_scale(x_k))
        # Return None instead to let the framework use finite-difference Hessians.
        # ===========================================================================
        
        return None
        
    def evaluateInEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate inequality local constraints for Subsystem 1.

        Computes the inequality constraint values from the subsystem responses,
        scales them using the appropriate ScalerConstraint, and stores the
        result in the subsystem.

        Args:
            subsystem: The local subsystem instance providing responses
                and scaling variables.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        
        inequality_unscaled = []
        # append any inequality Local constraints to this list using the responses
        ################################################################
        ###          USER CODE: Inequality constraints                ###
        ################################################################
        # inequality_unscaled.append(responses[...])
        # inequality_unscaled.append(responses[...])
        
        # scale the inequality Local constraint evaluation
        scl: List[ScalerConstraint] = scalers[...]
        # inequality: List[float] = [scl[i].transform(inequality_unscaled[i]) for i in range(len(inequality_unscaled))]
        
        # or if no InEquality Local constraints exist:
        inequality = None
        
        # inequality Local constraints needs to be a scaled01 quantity        
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        subsystem.set_InequalityLocalConstraintsValue(inequality)

    def evaluate_Jacobian_InEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Jacobian of the local inequality constraints.

        Args:
            subsystem: The local subsystem instance.
        """
        # === Tutorial: scaled <-> unscaled Jacobian (chain rule) ===================
        # Constraints are handled in SCALED [0,1] space, so this Jacobian must be
        # d(scaled constraint) / d(scaled design variables). Every affine scaler has a
        # constant slope scaler.get_scale() = d(scaled)/d(unscaled). From the UNSCALED
        # derivatives (dg/dx_j) convert each entry:
        #     dg_s/ds_j = get_scale(constraint) * dg/dx_j / get_scale(x_j)
        # Return None instead to let the framework use finite-difference Jacobians.
        # ===========================================================================
        
        return None
    
    def evaluate_Hessians_InEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessians of the local inequality constraints.

        Args:
            subsystem: The local subsystem instance.
        """
        # === Tutorial: scaled <-> unscaled Hessians (chain rule, 2nd order) ========
        # Constraints are handled in SCALED [0,1] space, so each Hessian must be
        # d^2(scaled constraint) / d(scaled design vars)^2. Each affine scaler has a
        # constant slope scaler.get_scale() = d(scaled)/d(unscaled). From the UNSCALED
        # second derivatives (d^2g/dx_j dx_k) convert element-wise:
        #     d2g_s/ds_j ds_k = get_scale(constraint) * d2g/dx_j dx_k / (get_scale(x_j)*get_scale(x_k))
        # Return None instead to let the framework use finite-difference Hessians.
        # ===========================================================================
        
        return None
```
