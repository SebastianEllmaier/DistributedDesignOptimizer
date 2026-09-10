# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Analysis module for Sellar subsystem 1.

Implements the disciplinary analysis for the second subsystem in the Sellar
multidisciplinary design problem, computing the y2 response variable.
"""

import math
from typing import List
from Distributed_Design_Optimizer.subsystem.optimization import AnalysisInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis


class Analysis1(AnalysisInterface):
    """Analysis class for Sellar subsystem 1.

    Computes the physical response y2 for the second discipline using
    the Sellar equations: y2 = sqrt(y1) + z1 + z2.

    Attributes:
        None specific to this class; inherits from AnalysisInterface.
    """

    def __init__(self) -> None:
        """Initialize Analysis1 instance."""
        pass
        
    def evaluateLocalResponses(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate subsystem responses using Sellar discipline 2 equations.

        Computes y2 from the design variables z1, z2 and coupling variable y1
        using the formula: y2 = sqrt(y1) + z1 + z2.

        Args:
            subsystem: The local subsystem containing design variables and scalers.
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
                
        responses = [math.sqrt(des_var[2]) + des_var[0] + des_var[1]]
        
        # responses is a unscaled quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
         
        subsystem.set_Responses_Unscaled(responses)
    
    def mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: LocalSubSystemBasis) -> None:
        """Map subsystem responses to neighboring subsystems.

        Transforms y2 to scaled values and distributes coupling variable y1
        and target design variables z1, z2 to subsystem 0.

        Args:
            subsystem: The local subsystem containing responses and scalers.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var: List[float] = subsystem.get_DesignVariables()  # scaled01 values
        des_var_unscaled: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
                 
        # map responses and shared/target design variables
        ################################################################
        ###          USER CODE: Map to coupling parameters           ###
        ################################################################
        # only map scaled01 quantities!
        
        subsystem.set_MappedResponseVariables(id="0",
                                              mappedresponsesin=[scalers[6].transform(responses[0])],
                                              mappedresponsesin_unscaled=[responses[0]])  # y2
        
        subsystem.set_CouplingVariables(id="0",
                                        couplingvariablein=[des_var[2]],
                                        couplingvariablein_unscaled=[des_var_unscaled[2]])  # y1
        
        subsystem.set_TargetSharedDesignVariables(id="0",
                                                  targetdesignvariablesin=[des_var[0], des_var[1]],
                                                  targetdesignvariablesin_unscaled=[des_var_unscaled[0], des_var_unscaled[1]])  # z1 z2
        
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
        # === Tutorial: scaled <-> unscaled mapped-response Jacobian (chain rule) ====
        # The mapped response y2 is passed to the neighbor in SCALED [0, 1] space, and
        # the design variables are scaled too, so the Jacobian row stored here must be
        # d(scaled y2) / d(scaled design variables). Every affine scaler has a constant
        # slope get_scale() = d(scaled)/d(unscaled). From the UNSCALED partials
        # dy2/dx_u[j] convert component-wise:
        #     dH_s/ds_j = get_scale(mapped) * dy2/dx_u[j] / get_scale(dv_scaler_j)
        # This method uses a SETTER (set_MappedResponses_Jacobian) and returns None.
        # ===========================================================================

        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var_unscaled: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values

        ################################################################
        ###          USER CODE: Compute Jacobians                    ###
        ################################################################
        # Mapped response (unscaled), see mapLocalResponsesDesignVariables_to_...:
        #   y2 = sqrt(y1) + z1 + z2   (mapped to neighbor "0", scaled by scalers[6])
        # with design variables x = [z1, z2, y1] = des_var[0..2].
        y1 = des_var_unscaled[2]

        # Partials dy2/dx_u w.r.t. the UNSCALED design variables.
        dY2dx_unscaled: List[float] = [1.0, 1.0, 0.5 * y1**-0.5]

        # Chain rule into SCALED space:
        #   dH_s/ds_j = get_scale(mapped) * dy2/dx_u[j] / get_scale(dv_scaler_j)
        scale_h: float = scalers[6].get_scale()
        n_dv: int = len(des_var_unscaled)
        jacobian_row: List[float] = [scale_h * dY2dx_unscaled[j] / scalers[j].get_scale()
                                     for j in range(n_dv)]

        # Store the (n_mapped_responses x n_dv) Jacobian for the coupling to "0".
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
            The mapped-response Hessian tensor
            [coupling][mapped_response][n_dv][n_dv], or None for finite differences.
        """
        # === Tutorial: scaled <-> unscaled mapped-response Hessian (2nd order) ======
        # The mapped response y2 is exchanged in SCALED [0, 1] space, so its Hessian
        # must be d^2(scaled y2) / d(scaled design vars)^2. Each affine scaler has a
        # constant slope get_scale() = d(scaled)/d(unscaled); from the UNSCALED second
        # derivatives d^2y2/dx_j dx_k convert element-wise:
        #     d2H_s/ds_j ds_k = get_scale(mapped) * d2y2/dx_j dx_k
        #                       / (get_scale(x_j) * get_scale(x_k))
        # This method RETURNS the tensor [coupling][response][n_dv][n_dv].
        # ===========================================================================

        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var_unscaled: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values

        ################################################################
        ###          USER CODE: Compute Hessians                     ###
        ################################################################
        # y2 = sqrt(y1) + z1 + z2 is separable, so its Hessian is diagonal.
        # Only d^2y2/dy1^2 = -0.25*y1^(-3/2) is nonzero. Design variables x = [z1, z2, y1].
        y1 = des_var_unscaled[2]
        d2Y2dx2_diag: List[float] = [0.0, 0.0, -0.25 * y1**-1.5]

        # Chain rule into SCALED space (diagonal only):
        #   H_s[k][k] = get_scale(mapped) * d2y2/dx_u^2[k] / get_scale(dv_k)^2
        scale_h: float = scalers[6].get_scale()
        n_dv: int = len(des_var_unscaled)
        hessian_mapped: List[List[float]] = [[0.0 for _ in range(n_dv)] for _ in range(n_dv)]
        for k in range(n_dv):
            scale_dv_k: float = scalers[k].get_scale()
            hessian_mapped[k][k] = scale_h * d2Y2dx2_diag[k] / (scale_dv_k**2)

        # One coupling ("0"), one mapped response (y2): wrap as [coupling][response].
        return [[hessian_mapped]]
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
