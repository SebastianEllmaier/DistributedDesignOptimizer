---
title: LocalConstraints0 (Source)
---

← Back to [LocalConstraints0 documentation](LocalConstraints0.md)

# LocalConstraints0 - Source Code

**File:** `userfiles\SpeedReducer\subsystem0\LocalConstraints0.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Local constraints module for Speed Reducer subsystem 0.

Defines the bending stress, surface stress, and geometric constraints
for the gear subsystem in the Speed Reducer problem.
"""
from typing import List
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalConstraintsInterface
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis, ScalerConstraint


class LocalConstraints0(LocalConstraintsInterface):
    """Local constraints class for Speed Reducer subsystem 0.

    Evaluates gear-related constraints including bending stress, contact
    stress, and geometric ratio constraints.

    Attributes:
        None specific to this class; inherits from LocalConstraintsInterface.
    """

    def __init__(self) -> None:
        """Initialize LocalConstraints0 instance."""
        pass

    def evaluateEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate equality constraints for subsystem 0.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        
        equality_unscaled = []
        # append any equality Local constraints to this list using the responses
        ################################################################
        ###          USER CODE: Equality constraints                 ###
        ################################################################
        # equality_unscaled.append(responses[...])
        # equality_unscaled.append(responses[...])        
        
        # scale equality Local constraint evaluation
        scl: List[ScalerConstraint] = [scalers[4]]
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
            subsystem: The local subsystem basis containing state information.
        """
        
        return None

    def evaluate_Hessians_EqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessians of the local equality constraints.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        
        return None
        
    def evaluateInEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate inequality constraints for subsystem 0.

        Computes 5 gear-related constraints on stress and geometry.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        
        inequality_unscaled = []
        # append any inequality Local constraints to this list using the responses
        ################################################################
        ###          USER CODE: Inequality constraints               ###
        ################################################################
        inequality_unscaled.append((27 / (responses[0] * (responses[1]**2) * responses[2])) - 1.0)
        inequality_unscaled.append((397.5 / (responses[0] * (responses[1]**2) * (responses[2]**2))) - 1.0)
        inequality_unscaled.append(((responses[1] * responses[2]) / 40) - 1.0)
        inequality_unscaled.append(((5 * responses[1]) / responses[0]) - 1.0)
        inequality_unscaled.append((responses[0] / (12 * responses[1])) - 1.0)
        
        # scale the inequality Local constraint evaluation
        scl: List[ScalerConstraint] = scalers[5:10]
        inequality: List[float] = [scl[i].transform(inequality_unscaled[i]) for i in range(len(inequality_unscaled))]
        # inequality Local constraints needs to be a scaled01 quantity        
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################ 
        subsystem.set_InequalityLocalConstraintsValue(inequality)

    def evaluate_Jacobian_InEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Jacobian of the local inequality constraints.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        # === Tutorial: scaled <-> unscaled Jacobian (chain rule) ===================
        # The optimizer works in SCALED [0, 1] design-variable space, so each Jacobian
        # row must be d(scaled constraint) / d(scaled design variables). Every affine
        # scaler has a constant slope get_scale() = d(scaled)/d(unscaled). Each of the
        # five constraints is a single monomial (minus 1) in the RESPONSES r = [x1, x2,
        # x3] (which map 1:1 onto the design variables). For a monomial
        # M = coeff * prod_k r_k^p_k we have dM/dr_k = (p_k / r_k) * M. After gathering
        # into design-variable order, convert component-wise:
        #     dg_s/ds_j = get_scale(constraint) * dg/dx_u[j] / get_scale(dv_scaler_j)
        # Return None instead to let the framework fall back to finite differences.
        # ===========================================================================

        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        ################################################################
        ###          USER CODE: Jacobian of inequality constraints   ###
        ################################################################
        # Inequality constraints (unscaled), see evaluateInEqualityLocalConstraints,
        # written as (coefficient, [exponents over r=[x1,x2,x3]]) for g = M - 1:
        #   g0 = 27/(x1 x2^2 x3) - 1
        #   g1 = 397.5/(x1 x2^2 x3^2) - 1
        #   g2 = x2 x3 / 40 - 1
        #   g3 = 5 x2 / x1 - 1
        #   g4 = x1 / (12 x2) - 1
        dv_to_resp: List[int] = [0, 1, 2]
        r: List[float] = [responses[0], responses[1], responses[2]]
        n_r: int = len(r)

        monomials = [
            (27.0, [-1, -2, -1]),
            (397.5, [-1, -2, -2]),
            (1.0 / 40.0, [0, 1, 1]),
            (5.0, [-1, 1, 0]),
            (1.0 / 12.0, [1, -1, 0]),
        ]
        constraint_scalers: List[ScalerBasis] = scalers[5:10]

        n_dv: int = len(des_var)
        jacobian: List[List[float]] = []
        for row, (coeff, p) in enumerate(monomials):
            M = coeff
            for k in range(n_r):
                M *= r[k]**p[k]
            grad_resp = [p[k] / r[k] * M for k in range(n_r)]  # dM/dr_k
            scale_c = constraint_scalers[row].get_scale()
            jacobian.append([scale_c * grad_resp[dv_to_resp[j]] / scalers[j].get_scale()
                             for j in range(n_dv)])

        # jacobian must be a scaled01 quantity (w.r.t. scaled01 design variables)
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        return jacobian

    def evaluate_Hessians_InEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessians of the local inequality constraints.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        # === Tutorial: scaled <-> unscaled Hessians (chain rule, 2nd order) ========
        # The optimizer works in SCALED [0, 1] space, so each constraint Hessian must
        # be d^2(scaled constraint) / d(scaled design vars)^2. Each affine scaler has a
        # constant slope get_scale() = d(scaled)/d(unscaled). For a monomial
        # M = coeff * prod_k r_k^p_k the second derivatives are
        #   d2M/dr_a dr_b = (p_a p_b)/(r_a r_b) * M        (a != b)
        #   d2M/dr_a^2   = p_a (p_a - 1)/r_a^2 * M         (a == b)
        # After gathering into design-variable order, convert element-wise:
        #     d2g_s/ds_a ds_b = get_scale(constraint) * d2g/dx_a dx_b
        #                       / (get_scale(x_a) * get_scale(x_b))
        # Return None instead to let the framework fall back to finite differences.
        # ===========================================================================

        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        ################################################################
        ###          USER CODE: Hessians of inequality constraints   ###
        ################################################################
        dv_to_resp: List[int] = [0, 1, 2]
        r: List[float] = [responses[0], responses[1], responses[2]]
        n_r: int = len(r)

        monomials = [
            (27.0, [-1, -2, -1]),
            (397.5, [-1, -2, -2]),
            (1.0 / 40.0, [0, 1, 1]),
            (5.0, [-1, 1, 0]),
            (1.0 / 12.0, [1, -1, 0]),
        ]
        constraint_scalers: List[ScalerBasis] = scalers[5:10]

        n_dv: int = len(des_var)
        hessians: List[List[List[float]]] = []
        for row, (coeff, p) in enumerate(monomials):
            M = coeff
            for k in range(n_r):
                M *= r[k]**p[k]
            Hr = [[0.0 for _ in range(n_r)] for _ in range(n_r)]
            for a in range(n_r):
                for b in range(n_r):
                    if a == b:
                        Hr[a][b] = p[a] * (p[a] - 1) / r[a]**2 * M
                    else:
                        Hr[a][b] = p[a] * p[b] / (r[a] * r[b]) * M
            scale_c = constraint_scalers[row].get_scale()
            hessians.append([
                [scale_c * Hr[dv_to_resp[a]][dv_to_resp[b]] / (scalers[a].get_scale() * scalers[b].get_scale())
                 for b in range(n_dv)]
                for a in range(n_dv)
            ])

        # hessians must be scaled01 quantities (w.r.t. scaled01 design variables)
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        return hessians

```
