# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Local objective module for Subsystem 0 in the Geometric Programming problem.

This module defines the LocalObjective0 class which implements the local
objective function computation for Subsystem 0 in the distributed design
optimization framework.
"""
from typing import List
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalObjectiveInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis, ScalerZeroOne


class LocalObjective0(LocalObjectiveInterface):
    """Local objective class for Subsystem 0.

    Implements the LocalObjectiveInterface to compute the local objective
    function contribution for Subsystem 0 in the Geometric Programming problem.
    This subsystem has a non-zero local objective based on the computed responses.

    Attributes:
        None specific to this class; inherits from LocalObjectiveInterface.
    """
    def __init__(self) -> None:
        """Initialize the LocalObjective0 instance."""
        pass
    
    def evaluateLocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the local objective function for Subsystem 0.

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
 
        localobjective_unscaled = responses[0]
            
        # scale the local objective function evaluation
        localobjective = scalers[5].transform(localobjective_unscaled)
        
        # or if no Local objective exist:
        # localobjective = None
        
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

        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Gradient of local objective          ###
        ################################################################
        # Local objective (unscaled): f = x3^2 + x4^2 + x0^-2 + 2*(x1/10)^2 + (x2/10)^2
        # (with x = [x0, x1, x2, x3=^{1}_{0}h, x4=^{2}_{0}h], see Analysis0.responses[0])
        x0, x1, x2, x3, x4 = des_var[0], des_var[1], des_var[2], des_var[3], des_var[4]

        # Partial derivatives w.r.t. the UNSCALED design variables: df/dx_u
        dfdx_unscaled: List[float] = [-2.0 * x0**-3,  # df/dx0
                                      x1 / 25.0,      # df/dx1  (d/dx1 of 2*(x1/10)^2 = x1/25)
                                      x2 / 50.0,      # df/dx2  (d/dx2 of (x2/10)^2 = x2/50)
                                      2.0 * x3,       # df/dx3
                                      2.0 * x4]       # df/dx4

        # Chain rule to SCALED space (scaled objective w.r.t. scaled design variables):
        # df_s/ds_j = scale(obj_scaler) * df/dx_u[j] / scale(dv_scaler_j)
        scale_obj: float = scalers[5].get_scale()
        gradient: List[float] = [scale_obj * dfdx_unscaled[j] / scalers[j].get_scale()
                                 for j in range(len(dfdx_unscaled))]

        # gradient must be a scaled01 quantity (w.r.t. scaled01 design variables)
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        return gradient

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

        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Hessian of local objective           ###
        ################################################################
        # The local objective is separable, so its Hessian is diagonal.
        x0, x1, x2, x3, x4 = des_var[0], des_var[1], des_var[2], des_var[3], des_var[4]

        # Second derivatives w.r.t. the UNSCALED design variables: d^2f/dx_u^2 (diagonal)
        d2fdx2_unscaled: List[float] = [6.0 * x0**-4,  # d^2f/dx0^2
                                        1.0 / 25.0,    # d^2f/dx1^2
                                        1.0 / 50.0,    # d^2f/dx2^2
                                        2.0,           # d^2f/dx3^2
                                        2.0]           # d^2f/dx4^2

        # Chain rule to SCALED space (diagonal): H_s[k][k] = scale(obj) * d2f/dx_u^2[k] / scale(dv_k)^2
        scale_obj: float = scalers[5].get_scale()
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