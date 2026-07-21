# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Local constraints module for Sellar subsystem 0.

Defines the equality and inequality constraints local to subsystem 0
in the Sellar distributed optimization problem.
"""
from typing import List
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalConstraintsInterface
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis, ScalerConstraint


class LocalConstraints0(LocalConstraintsInterface):
    """Local constraints class for Sellar subsystem 0.

    Evaluates the local equality and inequality constraints for the
    first subsystem including the y1 constraint.

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
        ###          USER CODE: Equality constraints                  ###
        ################################################################
        # equality_unscaled.append(responses[...])
        # equality_unscaled.append(responses[...])  
        
        # scale equality Local constraint evaluation
        scl: List[ScalerConstraint] = [scalers[5]]
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

        Computes the local inequality constraint: 3.16 - y1 >= 0.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        
        inequality_unscaled = []
        # append any inequality Local constraints to this list using the responses
        ################################################################
        ###          USER CODE: Inequality constraints                ###
        ################################################################
        inequality_unscaled.append(3.16 - responses[2])
        
        # scale the inequality Local constraint evaluation
        scl: List[ScalerConstraint] = [scalers[6]]
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
        # scaler has a constant slope get_scale() = d(scaled)/d(unscaled). From the
        # UNSCALED partials dg/dx_u[j] convert component-wise:
        #     dg_s/ds_j = get_scale(constraint) * dg/dx_u[j] / get_scale(dv_scaler_j)
        # Return None instead to let the framework fall back to finite differences.
        # ===========================================================================

        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Jacobian of inequality constraints   ###
        ################################################################
        # Inequality constraint (unscaled), see evaluateInEqualityLocalConstraints:
        #   g1 = 3.16 - y1 = 3.16 - x - z1^2 - z2 + 0.2*y2   (scaled by scalers[6])
        # with design variables x = [x, z1, z2, y2] = des_var[0..3].
        z1 = des_var[1]

        # Rows of dg/dx_u (w.r.t. UNSCALED design variables).
        dgdx_unscaled: List[List[float]] = [
            [-1.0, -2.0 * z1, -1.0, 0.2],   # dg1/dx_u
        ]
        constraint_scalers: List[ScalerBasis] = [scalers[6]]

        # Chain rule into SCALED space, row by row:
        #   dg_s/ds_j = get_scale(constraint) * dg/dx_u[j] / get_scale(dv_scaler_j)
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
            subsystem: The local subsystem basis containing state information.
        """
        # === Tutorial: scaled <-> unscaled Hessians (chain rule, 2nd order) ========
        # The optimizer works in SCALED [0, 1] space, so each constraint Hessian must
        # be d^2(scaled constraint) / d(scaled design vars)^2. Each affine scaler has a
        # constant slope get_scale() = d(scaled)/d(unscaled), so from the UNSCALED
        # second derivatives d^2g/dx_j dx_k convert element-wise:
        #     d2g_s/ds_j ds_k = get_scale(constraint) * d2g/dx_j dx_k
        #                       / (get_scale(x_j) * get_scale(x_k))
        # Return None instead to let the framework fall back to finite differences.
        # ===========================================================================

        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Hessians of inequality constraints   ###
        ################################################################
        # g1 = 3.16 - x - z1^2 - z2 + 0.2*y2 is separable, so its Hessian is diagonal.
        # Only d^2g1/dz1^2 = -2 is nonzero. Design variables x = [x, z1, z2, y2].
        d2gdx2_unscaled: List[List[float]] = [
            [0.0, -2.0, 0.0, 0.0],   # diag of d^2g1/dx_u^2
        ]
        constraint_scalers: List[ScalerBasis] = [scalers[6]]

        # Chain rule into SCALED space (diagonal only):
        #   H_s[k][k] = get_scale(constraint) * d2g/dx_u^2[k] / get_scale(dv_k)^2
        n_dv: int = len(des_var)
        hessians: List[List[List[float]]] = []
        for row in range(len(d2gdx2_unscaled)):
            scale_c: float = constraint_scalers[row].get_scale()
            hessian: List[List[float]] = [[0.0 for _ in range(n_dv)] for _ in range(n_dv)]
            for k in range(n_dv):
                scale_dv_k: float = scalers[k].get_scale()
                hessian[k][k] = scale_c * d2gdx2_unscaled[row][k] / (scale_dv_k**2)
            hessians.append(hessian)

        # hessians must be scaled01 quantities (w.r.t. scaled01 design variables)
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        return hessians
