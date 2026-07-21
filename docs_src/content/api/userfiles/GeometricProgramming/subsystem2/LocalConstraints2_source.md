---
title: LocalConstraints2 (Source)
---

← Back to [LocalConstraints2 documentation](LocalConstraints2.md)

# LocalConstraints2 - Source Code

**File:** `userfiles\GeometricProgramming\subsystem2\LocalConstraints2.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Local constraints module for Subsystem 2 in the Geometric Programming problem.

This module defines the LocalConstraints2 class which implements the local
equality and inequality constraints specific to Subsystem 2 in the distributed
design optimization framework.
"""
from typing import List
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalConstraintsInterface
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis, ScalerConstraint


class LocalConstraints2(LocalConstraintsInterface):
    """Local constraints class for Subsystem 2.

    Implements the LocalConstraintsInterface to define equality and inequality
    constraints for Subsystem 2 in the Geometric Programming problem.

    Attributes:
        None specific to this class; inherits from LocalConstraintsInterface.
    """
    def __init__(self) -> None:
        """Initialize the LocalConstraints2 instance."""
        pass

    def evaluateEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate equality local constraints for Subsystem 2.

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
        # scl: List[ScalerConstraint] = [scalers[...]]
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
        
        return None
    
    def evaluate_Hessians_EqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessians of the local equality constraints.

        Args:
            subsystem: The local subsystem instance.
        """
        
        return None
        
    def evaluateInEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate inequality local constraints for Subsystem 2.

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
        inequality_unscaled.append(responses[0])
        inequality_unscaled.append(responses[1])

        # scale the inequality Local constraint evaluation
        scl: List[ScalerConstraint] = scalers[6:8]
        inequality: List[float] = [scl[i].transform(inequality_unscaled[i]) for i in range(len(inequality_unscaled))]
        
        # or if no InEquality Local constraints exist:
        # inequality = None
        
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

        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Jacobian of inequality constraints   ###
        ################################################################
        # Inequality constraints (unscaled), see Analysis2.responses[0:2]:
        #   g1 = (x0/100)^-2 - (x1/10)^2 + (x3/10)^2 = 1e4*x0^-2 - x1^2/100 + x3^2/100  (scalers[6])
        #   g2 = (x0/100)^2 - x2^2 + (x3/10)^2       = x0^2/1e4 - x2^2 + x3^2/100       (scalers[7])
        # with x = [x0, x1, x2, x3=^{2}_{1}z].
        x0, x1, x2, x3 = des_var[0], des_var[1], des_var[2], des_var[3]

        # Rows of dg/dx_u (w.r.t. UNSCALED design variables) and their constraint scalers.
        dgdx_unscaled: List[List[float]] = [
            [-20000.0 * x0**-3, -x1 / 50.0, 0.0, x3 / 50.0],  # dg1/dx_u
            [x0 / 5000.0, 0.0, -2.0 * x2, x3 / 50.0],         # dg2/dx_u
        ]
        constraint_scalers: List[ScalerBasis] = [scalers[6], scalers[7]]

        # Chain rule to SCALED space:
        # dg_s/ds_j = scale(constraint_scaler) * dg/dx_u[j] / scale(dv_scaler_j)
        n_dv: int = len(des_var)
        jacobian: List[List[float]] = []
        for row in range(len(dgdx_unscaled)):
            scale_c: float = constraint_scalers[row].get_scale()
            jacobian.append([scale_c * dgdx_unscaled[row][j] / scalers[j].get_scale()
                             for j in range(n_dv)])

        # jacobian must be a scaled01 quantity (w.r.t. scaled01 design variables)
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        return jacobian

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

        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Hessians of inequality constraints   ###
        ################################################################
        # Both inequality constraints are separable, so each Hessian is diagonal.
        x0, x1, x2, x3 = des_var[0], des_var[1], des_var[2], des_var[3]

        # Diagonal second derivatives w.r.t. UNSCALED design variables.
        d2gdx2_unscaled: List[List[float]] = [
            [60000.0 * x0**-4, -1.0 / 50.0, 0.0, 1.0 / 50.0],  # d^2g1/dx_u^2
            [1.0 / 5000.0, 0.0, -2.0, 1.0 / 50.0],             # d^2g2/dx_u^2
        ]
        constraint_scalers: List[ScalerBasis] = [scalers[6], scalers[7]]

        # Chain rule to SCALED space (diagonal):
        # H_s[k][k] = scale(constraint_scaler) * d^2g/dx_u^2[k] / scale(dv_k)^2
        n_dv: int = len(des_var)
        hessians: List[List[List[float]]] = []
        for row in range(len(d2gdx2_unscaled)):
            scale_c: float = constraint_scalers[row].get_scale()
            hessian: List[List[float]] = [[0.0 for _ in range(n_dv)] for _ in range(n_dv)]
            for k in range(n_dv):
                scale_dv_k: float = scalers[k].get_scale()
                hessian[k][k] = scale_c * d2gdx2_unscaled[row][k] / (scale_dv_k**2)
            hessians.append(hessian)

        # hessians must be a scaled01 quantity (w.r.t. scaled01 design variables)
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        return hessians

```
