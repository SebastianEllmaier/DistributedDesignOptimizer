# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Local objective module for Sellar subsystem 0.

Defines the local objective function contribution from subsystem 0
in the Sellar distributed optimization problem.
"""
import math
from typing import List
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalObjectiveInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis, ScalerZeroOne


class LocalObjective0(LocalObjectiveInterface):
    """Local objective class for Sellar subsystem 0.

    Evaluates the local objective contribution: x1^2 + z2 + y1 + exp(-y2).

    Attributes:
        None specific to this class; inherits from LocalObjectiveInterface.
    """

    def __init__(self) -> None:
        """Initialize LocalObjective0 instance."""
        pass
    
    def evaluateLocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the local objective function for subsystem 0.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Local objective                      ###
        ################################################################
        # compute local objective, if no local objective simply set localobjective = 0.0
 
        localobjective_unscaled = responses[0] + responses[1] + responses[2] + responses[3]
            
        # scale the local objective function evaluation
        localobjective = scalers[4].transform(localobjective_unscaled)
        
        # localobjective needs to be a scaled01 quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        subsystem.set_LocalObjectiveValue(localobjective)

    def evaluate_Gradient_LocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Compute the gradient of the local objective function.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        # === Tutorial: scaled <-> unscaled gradients (chain rule) ==================
        # The optimizer works in SCALED [0, 1] design-variable space, so this gradient
        # must be d(scaled objective) / d(scaled design variables). Every affine scaler
        # has a constant slope  scaler.get_scale() = d(scaled)/d(unscaled). If you
        # differentiate the objective in UNSCALED (physical) space, df/dx_u[j], convert
        # component-wise to scaled space with:
        #     df_s/ds_j = get_scale(obj) * df/dx_u[j] / get_scale(dv_scaler_j)
        # Return None instead to let the framework fall back to finite differences.
        # ===========================================================================

        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Gradient of local objective          ###
        ################################################################
        # Local objective (unscaled): f = x^2 + z2 + y1 + exp(-y2), with
        #   y1 = x + z1^2 + z2 - 0.2*y2   (see Analysis0.evaluateLocalResponses)
        #   => f = x^2 + x + z1^2 + 2*z2 - 0.2*y2 + exp(-y2)
        # and design variables x = [x, z1, z2, y2] = des_var[0..3].
        x, z1, y2 = des_var[0], des_var[1], des_var[3]

        # Partial derivatives w.r.t. the UNSCALED design variables: df/dx_u
        dfdx_unscaled: List[float] = [
            2.0 * x + 1.0,          # df/dx
            2.0 * z1,               # df/dz1
            2.0,                    # df/dz2
            -0.2 - math.exp(-y2),   # df/dy2
        ]

        # Chain rule into SCALED space:
        #   df_s/ds_j = get_scale(obj) * df/dx_u[j] / get_scale(dv_scaler_j)
        scale_obj: float = scalers[4].get_scale()
        gradient: List[float] = [scale_obj * dfdx_unscaled[j] / scalers[j].get_scale()
                                 for j in range(len(dfdx_unscaled))]

        # gradient must be a scaled01 quantity (w.r.t. scaled01 design variables)
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        return gradient
    
    def evaluate_Hessian_LocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Compute the Hessian of the local objective function.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        # === Tutorial: scaled <-> unscaled Hessian (chain rule, 2nd order) =========
        # The optimizer works in SCALED [0, 1] space, so this Hessian must be
        # d^2(scaled objective) / d(scaled design vars)^2. Each affine scaler has a
        # constant slope get_scale() = d(scaled)/d(unscaled), so from the UNSCALED
        # second derivatives d^2f/dx_j dx_k convert element-wise:
        #     d2f_s/ds_j ds_k = get_scale(obj) * d2f/dx_j dx_k
        #                       / (get_scale(x_j) * get_scale(x_k))
        # Return None instead to let the framework fall back to finite differences.
        # ===========================================================================

        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Hessian of local objective           ###
        ################################################################
        # The local objective is separable, so its Hessian is diagonal.
        # with design variables x = [x, z1, z2, y2] = des_var[0..3].
        y2 = des_var[3]

        # Diagonal second derivatives w.r.t. UNSCALED design variables: d^2f/dx_u^2
        d2fdx2_unscaled: List[float] = [
            2.0,                # d^2f/dx^2
            2.0,                # d^2f/dz1^2
            0.0,                # d^2f/dz2^2
            math.exp(-y2),      # d^2f/dy2^2
        ]

        # Chain rule into SCALED space (diagonal only):
        #   H_s[k][k] = get_scale(obj) * d2f/dx_u^2[k] / get_scale(dv_k)^2
        scale_obj: float = scalers[4].get_scale()
        n: int = len(d2fdx2_unscaled)
        hessian: List[List[float]] = [[0.0 for _ in range(n)] for _ in range(n)]
        for k in range(n):
            scale_dv_k: float = scalers[k].get_scale()
            hessian[k][k] = scale_obj * d2fdx2_unscaled[k] / (scale_dv_k**2)

        # hessian must be a scaled01 quantity (w.r.t. scaled01 design variables)
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        return hessian

