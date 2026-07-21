# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Analysis module for Subsystem 2 in the Geometric Programming Top-Down Hierarchic problem.

This module defines the Analysis2 class which implements the physics-based
analysis computations and response mapping for Subsystem 2 in the distributed
design optimization framework.
"""

import math
from typing import List
from Distributed_Design_Optimizer.subsystem.optimization import AnalysisInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis


class Analysis2(AnalysisInterface):
    """Analysis class for Subsystem 2.

    Implements the AnalysisInterface to compute physical responses and map
    coupling variables for Subsystem 2 in the Geometric Programming problem.
    This subsystem operates at level 1 in the hierarchical decomposition.

    Attributes:
        None specific to this class; inherits from AnalysisInterface.
    """
    def __init__(self) -> None:
        """Initialize the Analysis2 instance."""
        pass
        
    def evaluateLocalResponses(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the physical responses of Subsystem 2.

        Computes the subsystem responses based on the current design variables.
        The responses include geometric programming formulas involving powers,
        inverse powers, and square root operations.

        Args:
            subsystem: The LocalSubSystemBasis instance containing design variables
                and where computed responses will be stored.
        """
                  
        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        
        # load copymappedresponsevariables from other neighborhing subsystmes which may be necessary for this analysis
        # scalers: List[ScalerBasis] = subsystem.get_Scalers() 
        # copymappedresponsevariables_neighbor_id_scaled01: List[float] | None = subsystem.get_Copy_MappedResponseVariables(id=neighbor_id)  # scaled01 values
        # # to unscale, run
        # copymappedresponsevariables_neighbor_id = scalers[corresponding_index].inverse_transform(copymappedresponsevariables_neighbor_id_scaled01)  # unscaled value        

        # Compute responses using des_var and copymappedresponsevariables
        ################################################################
        ###          USER CODE: Compute responses                    ###
        ################################################################
        
        responses = [((des_var[0] / 100)**-2) - ((des_var[1] / 10)**2) + ((des_var[3] / 10)**2),
                     ((des_var[0] / 100)**2) - (des_var[2]**2) + ((des_var[3] / 10)**2),
                     math.sqrt(((des_var[0] / 100)**2) + ((des_var[1] / 10)**2) + (des_var[2]**2) + ((des_var[3] / 10)**2))]
        
        # responses is a unscaled quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        subsystem.set_Responses_Unscaled(responses)

    def mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: LocalSubSystemBasis) -> None:
        """Map responses and design variables for inter-subsystem coupling.

        Maps the mapped response to Subsystem 0 and the target shared design
        variable to Subsystem 1 for coordination between subsystems.

        Args:
            subsystem: The LocalSubSystemBasis instance containing responses
                and design variables to be mapped.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var: List[float] = subsystem.get_DesignVariables()  # scaled01 values
        des_var_unscaled: List[float] = subsystem.get_DesignVariables_Unscaled() # unscaled
                 
        # map responses and shared/target design variables
        ################################################################
        ###          USER CODE: Map to coupling parameters           ###
        ################################################################
        # only map scaled01 quantities!
        
        subsystem.set_MappedResponseVariables(id="0",
                                              mappedresponsesin=[scalers[8].transform(responses[2])],
                                              mappedresponsesin_unscaled=[responses[2]])  # ^{2}_{0}H
        
        # subsystem.set_CouplingVariables(id=,
        #                                 couplingvariablein=,
        #                                 couplingvariablein_unscaled=)
        # subsystem.set_CouplingVariables(id=,
        #                                 couplingvariablein=,
        #                                 couplingvariablein_unscaled=)
        
        subsystem.set_TargetSharedDesignVariables(id="1",
                                                  targetdesignvariablesin=[des_var[3]],
                                                  targetdesignvariablesin_unscaled=[des_var_unscaled[3]])  # ^{2}_{1}z

        # subsystem.set_SharedDesignVariables(id=,
        #                                     shareddesignvariablesin=,
        #                                     shareddesignvariablesin_unscaled=)
        # subsystem.set_SharedDesignVariables(id=,
        #                                     shareddesignvariablesin=,
        #                                     shareddesignvariablesin_unscaled=)

        ################################################################
        ###          END USER CODE                                   ###
        ################################################################

    def mapLocalResponsesDesignVariables_to_CouplingParameters_Jacobians(self, subsystem: LocalSubSystemBasis) -> None:
        """Map the Jacobians of the mapped responses.

        Args:
            subsystem: The subsystem for which the Jacobians are mapped.
        """
        
        responses: List[float] = subsystem.get_Responses_Unscaled()  
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var: List[float] = subsystem.get_DesignVariables()        
        
        ################################################################
        ###          USER CODE: Compute Jacobians                    ###
        ################################################################
        # === Tutorial: scaled <-> unscaled Jacobian (chain rule) ===================
        # Mapped responses (coupling parameters) live in SCALED [0,1] space, so this
        # Jacobian must be d(scaled response) / d(scaled design variables). Every affine
        # scaler has a constant slope scaler.get_scale() = d(scaled)/d(unscaled). From the
        # UNSCALED derivatives (dH/dx_j) convert each entry:
        #     dH_s/ds_j = get_scale(response) * dH/dx_j / get_scale(x_j)
        # Return None instead to let the framework use finite-difference Jacobians.
        # ===========================================================================
        # Mapped response (unscaled), see Analysis2.responses[2]:
        #   H = sqrt(S),  S = (x0/100)^2 + (x1/10)^2 + x2^2 + (x3/10)^2
        #     = x0^2/1e4 + x1^2/100 + x2^2 + x3^2/100
        # with x = [x0, x1, x2, x3=^{2}_{1}z]. This is mapped to neighbor "0"
        # and scaled by scalers[8] (see mapLocalResponsesDesignVariables_to_CouplingParameters).
        des_var_unscaled: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        x0, x1, x2, x3 = des_var_unscaled[0], des_var_unscaled[1], des_var_unscaled[2], des_var_unscaled[3]

        # H = sqrt(S); reuse the already-evaluated unscaled response value for sqrt(S).
        response_h: float = responses[2]

        # dS/dx_u, then dH/dx_u = (dS/dx_u) / (2*H)
        dS_dx_unscaled: List[float] = [x0 / 5000.0, x1 / 50.0, 2.0 * x2, x3 / 50.0]
        dHdx_unscaled: List[float] = [dS_dx_unscaled[j] / (2.0 * response_h) for j in range(4)]

        # Chain rule to SCALED space:
        # dH_s/ds_j = scale(mapped_response_scaler) * dH/dx_u[j] / scale(dv_scaler_j)
        scale_h: float = scalers[8].get_scale()
        n_dv: int = len(des_var_unscaled)
        jacobian_row: List[float] = [scale_h * dHdx_unscaled[j] / scalers[j].get_scale()
                                     for j in range(n_dv)]

        # Store the Jacobian of the mapped response w.r.t. neighbor "0".
        # Shape must be (number_of_mapped_responses, number_of_design_variables) = (1, 4).
        subsystem.set_MappedResponses_Jacobian(id="0",
                                               mappedresponses_jacobian_in=[jacobian_row])
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################

    def mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian(self, subsystem: LocalSubSystemBasis) -> List[List[List[List[float | None]]]] | None:
        """Map the Hessians of the mapped responses, if known a priori.

        Args:
            subsystem: The subsystem for which the Hessians are mapped.

        Returns:
            Hessian tensor indexed by [local-to-local coupling][mapped response
            component][n_design][n_design], or None to fall back to a BFGS /
            finite-difference approximation.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Compute Hessians                     ###
        ################################################################
        # === Tutorial: scaled <-> unscaled Hessian (chain rule, 2nd order) =========
        # Mapped responses (coupling parameters) live in SCALED [0,1] space, so this
        # Hessian must be d^2(scaled response) / d(scaled design vars)^2. Each affine
        # scaler has a constant slope scaler.get_scale() = d(scaled)/d(unscaled). From the
        # UNSCALED second derivatives (d^2H/dx_j dx_k) convert element-wise:
        #     d2H_s/ds_j ds_k = get_scale(response) * d2H/dx_j dx_k / (get_scale(x_j)*get_scale(x_k))
        # Return None instead to let the framework use a BFGS/finite-difference Hessian.
        # ===========================================================================
        # Mapped response (unscaled), see Analysis2.responses[2]:
        #   H = sqrt(S),  S = x0^2/1e4 + x1^2/100 + x2^2 + x3^2/100
        # with x = [x0, x1, x2, x3=^{2}_{1}z], mapped to neighbor "0" (scaled by scalers[8]).
        des_var_unscaled: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        x0, x1, x2, x3 = des_var_unscaled[0], des_var_unscaled[1], des_var_unscaled[2], des_var_unscaled[3]
        n_dv: int = len(des_var_unscaled)

        # Reuse the already-evaluated unscaled response value for H = sqrt(S).
        response_h: float = responses[2]

        # First derivatives dS/dx_u and diagonal second derivatives d^2S/dx_u^2 (S is separable).
        dS_dx_unscaled: List[float] = [x0 / 5000.0, x1 / 50.0, 2.0 * x2, x3 / 50.0]
        d2S_dx2_diag: List[float] = [1.0 / 5000.0, 1.0 / 50.0, 2.0, 1.0 / 50.0]

        # Unscaled Hessian of H = sqrt(S):
        #   d^2H/dx_j dx_k = (d^2S/dx_j dx_k)/(2H) - (dS/dx_j * dS/dx_k)/(4 H^3)
        # The first term is diagonal (S separable); the second is a full rank-1 term.
        d2Hdx2_unscaled: List[List[float]] = [
            [
                (d2S_dx2_diag[j] if j == k else 0.0) / (2.0 * response_h) - dS_dx_unscaled[j] * dS_dx_unscaled[k] / (4.0 * response_h**3)
                for k in range(n_dv)
            ]
            for j in range(n_dv)
        ]

        # Chain rule to SCALED space.
        scale_h: float = scalers[8].get_scale()
        hessian_mapped: List[List[float]] = [
            [
                scale_h * d2Hdx2_unscaled[j][k] / (scalers[j].get_scale() * scalers[k].get_scale())
                for k in range(n_dv)
            ]
            for j in range(n_dv)
        ]

        # Shape: [local-to-local coupling][mapped response component][n_dv][n_dv] = (1, 1, 4, 4).
        # A single coupling (neighbor "0") with one mapped response H.
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        return [[hessian_mapped]]
