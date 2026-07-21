# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Local objective module for Speed Reducer subsystem 0.

Defines the local objective function contribution from the gear subsystem
to the total weight objective.
"""
from typing import List
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalObjectiveInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis, ScalerZeroOne


class LocalObjective0(LocalObjectiveInterface):
    """Local objective class for Speed Reducer subsystem 0.

    Evaluates the gear weight contribution to the total speed reducer weight.

    Attributes:
        None specific to this class; inherits from LocalObjectiveInterface.
    """

    def __init__(self) -> None:
        """Initialize LocalObjective0 instance."""
        pass
    
    def evaluateLocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the local objective function for subsystem 0.

        Computes the gear weight contribution to total reducer weight.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Local objective                      ###
        ################################################################
        # compute local objective, if no local objective simply set localobjective = 0.0
 
        localobjective_unscaled = 0.7854 * responses[0] * (responses[1]**2) * \
                                    (3.3333 * (responses[2]**2) + 14.9334 * responses[2] - 43.0934)
            
        # scale the local objective function evaluation
        localobjective = scalers[3].transform(localobjective_unscaled)
        
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
        # has a constant slope  scaler.get_scale() = d(scaled)/d(unscaled). Here the
        # objective is written in terms of the RESPONSES r (= x1, x2, x3); those map
        # 1:1 onto the design variables (see Analysis0). So we differentiate w.r.t. the
        # responses, gather into design-variable order, then convert component-wise:
        #     df_s/ds_j = get_scale(obj) * df/dx_u[j] / get_scale(dv_scaler_j)
        # Return None instead to let the framework fall back to finite differences.
        # ===========================================================================

        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        ################################################################
        ###          USER CODE: Gradient of local objective          ###
        ################################################################
        # Local objective (unscaled): f = 0.7854 * x1 * x2^2 * A(x3),
        #   A(x3) = 3.3333*x3^2 + 14.9334*x3 - 43.0934.
        # Responses r = [x1, x2, x3] map to design variables via
        #   responses = [des_var[0], des_var[1], des_var[2]]  =>  dv_to_resp[j].
        dv_to_resp: List[int] = [0, 1, 2]
        r0, r1, r2 = responses[0], responses[1], responses[2]

        c = 0.7854
        A = 3.3333 * r2**2 + 14.9334 * r2 - 43.0934
        Ap = 6.6666 * r2 + 14.9334  # dA/dx3

        # Gradient in RESPONSE space df/dr:
        grad_resp: List[float] = [
            c * r1**2 * A,          # df/dx1
            2.0 * c * r0 * r1 * A,  # df/dx2
            c * r0 * r1**2 * Ap,    # df/dx3
        ]

        # Gather into DESIGN-VARIABLE order, then chain-rule into SCALED space:
        #   df_s/ds_j = get_scale(obj) * df/dx_u[j] / get_scale(dv_scaler_j)
        scale_obj = scalers[3].get_scale()
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
        # constant slope get_scale() = d(scaled)/d(unscaled). This objective is NOT
        # separable, so the Hessian has cross terms. From the UNSCALED second
        # derivatives d^2f/dx_j dx_k convert element-wise:
        #     d2f_s/ds_j ds_k = get_scale(obj) * d2f/dx_j dx_k
        #                       / (get_scale(x_j) * get_scale(x_k))
        # Return None instead to let the framework fall back to finite differences.
        # ===========================================================================

        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        ################################################################
        ###          USER CODE: Hessian of local objective           ###
        ################################################################
        # f = 0.7854 * x1 * x2^2 * A(x3); responses r = [x1, x2, x3].
        dv_to_resp: List[int] = [0, 1, 2]
        r0, r1, r2 = responses[0], responses[1], responses[2]

        c = 0.7854
        A = 3.3333 * r2**2 + 14.9334 * r2 - 43.0934
        Ap = 6.6666 * r2 + 14.9334  # dA/dx3
        App = 6.6666                # d^2A/dx3^2

        # Symmetric Hessian in RESPONSE space d^2f/dr dr:
        n_r = 3
        Hr: List[List[float]] = [[0.0 for _ in range(n_r)] for _ in range(n_r)]
        Hr[0][1] = Hr[1][0] = 2.0 * c * r1 * A
        Hr[0][2] = Hr[2][0] = c * r1**2 * Ap
        Hr[1][1] = 2.0 * c * r0 * A
        Hr[1][2] = Hr[2][1] = 2.0 * c * r0 * r1 * Ap
        Hr[2][2] = c * r0 * r1**2 * App

        # Gather into DESIGN-VARIABLE order, then chain-rule into SCALED space:
        #   H_s[a][b] = get_scale(obj) * d2f/dx_u^2[a][b]
        #              / (get_scale(x_a) * get_scale(x_b))
        scale_obj = scalers[3].get_scale()
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
