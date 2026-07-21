---
title: LocalConstraints1 (Source)
---

← Back to [LocalConstraints1 documentation](LocalConstraints1.md)

# LocalConstraints1 - Source Code

**File:** `userfiles\SpeedReducer\subsystem1\LocalConstraints1.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Local constraints module for Speed Reducer subsystem 1.

Defines the stress, deflection, and geometric constraints for shaft 1
in the Speed Reducer problem.
"""
import math
from typing import List
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalConstraintsInterface
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis, ScalerConstraint


class LocalConstraints1(LocalConstraintsInterface):
    """Local constraints class for Speed Reducer subsystem 1.

    Evaluates shaft 1 stress, deflection, and mounting constraints.

    Attributes:
        None specific to this class; inherits from LocalConstraintsInterface.
    """

    def __init__(self) -> None:
        """Initialize LocalConstraints1 instance."""
        pass

    def evaluateEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate equality constraints for subsystem 1.

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
        scl: List[ScalerConstraint] = [scalers[6]]
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
        """Evaluate inequality constraints for subsystem 1.

        Computes 3 shaft-related constraints on stress and geometry.

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
        inequality_unscaled.append(((1.93 * (responses[3]**3)) / (responses[1] * responses[2] * (responses[4]**4))) - 1.0)
        inequality_unscaled.append((math.sqrt(((745 * responses[3]) / (responses[1] * responses[2]))**2 + 16.9E+6)
                                        / (110.0 * (responses[4]**3))) - 1.0)
        inequality_unscaled.append(((1.5 * responses[4] + 1.9) / responses[3]) - 1.0)

        # scale the inequality Local constraint evaluation
        scl: List[ScalerConstraint] = scalers[7:10]
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
        # scaler has a constant slope get_scale() = d(scaled)/d(unscaled). The three
        # constraints are written in RESPONSES r = [x1, x2, x3, x4, x6]; the design
        # variables are ordered [x4, x6, x1, x2, x3], so we differentiate w.r.t. the
        # responses, gather into design-variable order, then convert component-wise:
        #     dg_s/ds_j = get_scale(constraint) * dg/dx_u[j] / get_scale(dv_scaler_j)
        # Return None instead to let the framework fall back to finite differences.
        # ===========================================================================

        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        ################################################################
        ###          USER CODE: Jacobian of inequality constraints   ###
        ################################################################
        # Constraints (unscaled), responses r = [x1, x2, x3, x4, x6]:
        #   g0 = 1.93*x4^3 / (x2 x3 x6^4) - 1                      (monomial)
        #   g1 = sqrt((745 x4/(x2 x3))^2 + 16.9e6) / (110 x6^3) - 1 (sqrt composite)
        #   g2 = (1.5 x6 + 1.9)/x4 - 1                              (sum of monomials)
        dv_to_resp: List[int] = [3, 4, 0, 1, 2]
        r: List[float] = list(responses)
        n_r: int = len(r)

        def mono_grad(coeff: float, p: List[int]) -> List[float]:
            M = coeff
            for k in range(n_r):
                M *= r[k]**p[k]
            return [p[k] / r[k] * M for k in range(n_r)]

        # g0: monomial in r=[x1,x2,x3,x4,x6]
        grad0 = mono_grad(1.93, [0, -1, -1, 3, -4])

        # g1 = T * w - 1, with u = 745 x4/(x2 x3), T = sqrt(u^2 + 16.9e6),
        #      w = (1/110) x6^-3. u = 745 r1^-1 r2^-1 r3^1 (r1=x2, r2=x3, r3=x4).
        u = 745.0 * r[3] / (r[1] * r[2])
        T = math.sqrt(u**2 + 16.9E+6)
        w = (1.0 / 110.0) * r[4]**-3
        grad1 = [0.0] * n_r
        grad1[1] = w * (u / T) * (-u / r[1])   # dg1/dx2
        grad1[2] = w * (u / T) * (-u / r[2])   # dg1/dx3
        grad1[3] = w * (u / T) * (u / r[3])    # dg1/dx4
        grad1[4] = T * (-3.0 / 110.0) * r[4]**-4  # dg1/dx6

        # g2 = 1.5*x6/x4 + 1.9/x4 - 1  (two monomials)
        grad2a = mono_grad(1.5, [0, 0, 0, -1, 1])
        grad2b = mono_grad(1.9, [0, 0, 0, -1, 0])
        grad2 = [grad2a[k] + grad2b[k] for k in range(n_r)]

        grads = [grad0, grad1, grad2]
        constraint_scalers: List[ScalerBasis] = scalers[7:10]
        n_dv: int = len(des_var)
        jacobian: List[List[float]] = []
        for row in range(3):
            scale_c = constraint_scalers[row].get_scale()
            jacobian.append([scale_c * grads[row][dv_to_resp[j]] / scalers[j].get_scale()
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
        # constant slope get_scale() = d(scaled)/d(unscaled). For the sqrt composite
        # g1 = T*w with T = sqrt(u^2 + K), the second derivatives of T follow
        #   d2T/dx dy = (u_x u_y + u u_xy)/T - u^2 u_x u_y / T^3.
        # We build each Hessian in RESPONSE space, gather into design-variable order,
        # then convert element-wise:
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
        dv_to_resp: List[int] = [3, 4, 0, 1, 2]
        r: List[float] = list(responses)
        n_r: int = len(r)

        def mono_hess(coeff: float, p: List[int]) -> List[List[float]]:
            M = coeff
            for k in range(n_r):
                M *= r[k]**p[k]
            H = [[0.0 for _ in range(n_r)] for _ in range(n_r)]
            for a in range(n_r):
                for b in range(n_r):
                    if a == b:
                        H[a][b] = p[a] * (p[a] - 1) / r[a]**2 * M
                    else:
                        H[a][b] = p[a] * p[b] / (r[a] * r[b]) * M
            return H

        # g0: monomial
        H0 = mono_hess(1.93, [0, -1, -1, 3, -4])

        # g1 = T * w, T = sqrt(u^2 + K), u = 745 r1^-1 r2^-1 r3^1 (r1=x2,r2=x3,r3=x4),
        #      w = (1/110) r4^-3 (r4=x6).
        K = 16.9E+6
        D = 110.0
        u = 745.0 * r[3] / (r[1] * r[2])
        T = math.sqrt(u**2 + K)
        uvars = [1, 2, 3]     # response indices appearing in u
        pexp = [-1, -1, 1]    # corresponding exponents of u
        u_x = {vi: pexp[i] / r[vi] * u for i, vi in enumerate(uvars)}
        u_xy = {}
        for i, vi in enumerate(uvars):
            for j, vj in enumerate(uvars):
                if vi == vj:
                    u_xy[(vi, vj)] = pexp[i] * (pexp[i] - 1) / r[vi]**2 * u
                else:
                    u_xy[(vi, vj)] = pexp[i] * pexp[j] / (r[vi] * r[vj]) * u
        w = (1.0 / D) * r[4]**-3
        wp = (-3.0 / D) * r[4]**-4    # dw/dx6
        wpp = (12.0 / D) * r[4]**-5   # d2w/dx6^2
        H1 = [[0.0 for _ in range(n_r)] for _ in range(n_r)]
        for vi in uvars:
            for vj in uvars:
                Txy = (u_x[vi] * u_x[vj] + u * u_xy[(vi, vj)]) / T - u**2 * u_x[vi] * u_x[vj] / T**3
                H1[vi][vj] = w * Txy
        for vi in uvars:
            T_i = (u / T) * u_x[vi]
            H1[vi][4] = T_i * wp
            H1[4][vi] = T_i * wp
        H1[4][4] = T * wpp

        # g2: sum of two monomials
        H2a = mono_hess(1.5, [0, 0, 0, -1, 1])
        H2b = mono_hess(1.9, [0, 0, 0, -1, 0])
        H2 = [[H2a[a][b] + H2b[a][b] for b in range(n_r)] for a in range(n_r)]

        Hs = [H0, H1, H2]
        constraint_scalers: List[ScalerBasis] = scalers[7:10]
        n_dv: int = len(des_var)
        hessians: List[List[List[float]]] = []
        for row in range(3):
            scale_c = constraint_scalers[row].get_scale()
            hessians.append([
                [scale_c * Hs[row][dv_to_resp[a]][dv_to_resp[b]] / (scalers[a].get_scale() * scalers[b].get_scale())
                 for b in range(n_dv)]
                for a in range(n_dv)
            ])

        # hessians must be scaled01 quantities (w.r.t. scaled01 design variables)
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        return hessians

```
