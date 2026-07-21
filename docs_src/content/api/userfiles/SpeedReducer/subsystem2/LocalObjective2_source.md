---
title: LocalObjective2 (Source)
---

← Back to [LocalObjective2 documentation](LocalObjective2.md)

# LocalObjective2 - Source Code

**File:** `userfiles\SpeedReducer\subsystem2\LocalObjective2.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Local objective module for Speed Reducer subsystem 2.

Defines the local objective function contribution from shaft 2
to the total weight objective.
"""
from typing import List
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalObjectiveInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis, ScalerZeroOne


class LocalObjective2(LocalObjectiveInterface):
    """Local objective class for Speed Reducer subsystem 2.

    Evaluates the shaft 2 weight contribution to the total reducer weight.

    Attributes:
        None specific to this class; inherits from LocalObjectiveInterface.
    """

    def __init__(self) -> None:
        """Initialize LocalObjective2 instance."""
        pass

    def evaluateLocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the local objective function for subsystem 2.

        Computes the shaft 2 weight contribution to total reducer weight.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Local objective                      ###
        ################################################################
        # compute local objective, if no local objective simply set localobjective = 0.0
        
        localobjective_unscaled = -1.5079 * responses[0] * (responses[4]**2) + 7.477 * (responses[4]**3) \
                                    + 0.7854 * responses[3] * (responses[4]**2)
            
        # scale the local objective function evaluation
        localobjective = scalers[5].transform(localobjective_unscaled)
        
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
        # === Tutorial: scaled <-> unscaled gradients (chain rule) ==================
        # The optimizer works in SCALED [0, 1] design-variable space, so this gradient
        # must be d(scaled objective) / d(scaled design variables). Every affine scaler
        # has a constant slope get_scale() = d(scaled)/d(unscaled). The objective is
        # written in RESPONSES r = [x1, x2, x3, x5, x7], but the design variables are
        # ordered [x5, x7, x1, x2, x3] (see Analysis2), so we differentiate w.r.t. the
        # responses, gather into design-variable order via dv_to_resp, then convert:
        #     df_s/ds_j = get_scale(obj) * df/dx_u[j] / get_scale(dv_scaler_j)
        # Return None instead to let the framework fall back to finite differences.
        # ===========================================================================

        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        ################################################################
        ###          USER CODE: Gradient of local objective          ###
        ################################################################
        # Local objective (unscaled): f = -1.5079*x1*x7^2 + 7.477*x7^3 + 0.7854*x5*x7^2
        # Responses r = [x1, x2, x3, x5, x7]; design variables [x5, x7, x1, x2, x3].
        dv_to_resp: List[int] = [3, 4, 0, 1, 2]
        r0, r3, r4 = responses[0], responses[3], responses[4]  # x1, x5, x7

        c1, c2, c3 = -1.5079, 7.477, 0.7854
        grad_resp: List[float] = [
            c1 * r4**2,                                     # df/dx1
            0.0,                                            # df/dx2
            0.0,                                            # df/dx3
            c3 * r4**2,                                     # df/dx5
            2.0 * c1 * r0 * r4 + 3.0 * c2 * r4**2 + 2.0 * c3 * r3 * r4,  # df/dx7
        ]

        # Gather into DESIGN-VARIABLE order, then chain-rule into SCALED space:
        scale_obj = scalers[5].get_scale()
        n_dv = len(des_var)
        gradient: List[float] = [scale_obj * grad_resp[dv_to_resp[j]] / scalers[j].get_scale()
                                 for j in range(n_dv)]

        # gradient must be a scaled01 quantity (w.r.t. scaled01 design variables)
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        return gradient

    def evaluate_Hessian_LocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessian of the local objective function.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        # === Tutorial: scaled <-> unscaled Hessian (chain rule, 2nd order) =========
        # The optimizer works in SCALED [0, 1] space, so this Hessian must be
        # d^2(scaled objective) / d(scaled design vars)^2. Each affine scaler has a
        # constant slope get_scale() = d(scaled)/d(unscaled). We build the Hessian in
        # RESPONSE space, gather into design-variable order, then convert element-wise:
        #     d2f_s/ds_a ds_b = get_scale(obj) * d2f/dx_a dx_b
        #                       / (get_scale(x_a) * get_scale(x_b))
        # Return None instead to let the framework fall back to finite differences.
        # ===========================================================================

        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        ################################################################
        ###          USER CODE: Hessian of local objective           ###
        ################################################################
        # f = -1.5079*x1*x7^2 + 7.477*x7^3 + 0.7854*x5*x7^2; r = [x1, x2, x3, x5, x7].
        dv_to_resp: List[int] = [3, 4, 0, 1, 2]
        r0, r3, r4 = responses[0], responses[3], responses[4]  # x1, x5, x7

        c1, c2, c3 = -1.5079, 7.477, 0.7854
        n_r = 5
        Hr: List[List[float]] = [[0.0 for _ in range(n_r)] for _ in range(n_r)]
        Hr[0][4] = Hr[4][0] = 2.0 * c1 * r4                       # d2f/dx1 dx7
        Hr[3][4] = Hr[4][3] = 2.0 * c3 * r4                       # d2f/dx5 dx7
        Hr[4][4] = 2.0 * c1 * r0 + 6.0 * c2 * r4 + 2.0 * c3 * r3  # d2f/dx7^2

        # Gather into DESIGN-VARIABLE order, then chain-rule into SCALED space:
        scale_obj = scalers[5].get_scale()
        n_dv = len(des_var)
        hessian: List[List[float]] = [
            [scale_obj * Hr[dv_to_resp[a]][dv_to_resp[b]] / (scalers[a].get_scale() * scalers[b].get_scale())
             for b in range(n_dv)]
            for a in range(n_dv)
        ]

        # hessian must be a scaled01 quantity (w.r.t. scaled01 design variables)
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        return hessian

```
