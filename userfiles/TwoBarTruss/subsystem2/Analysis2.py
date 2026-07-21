# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Analysis module for Two-Bar Truss subsystem 2 (bar 2 sizing).

Implements the analysis for bar 2 (compression member) in the Two-Bar Truss
structure, computing stress, Euler buckling stress, and cross-sectional area.
"""

import math
from typing import List
from Distributed_Design_Optimizer.subsystem.optimization import AnalysisInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis


class Analysis2(AnalysisInterface):
    """Analysis class for Two-Bar Truss subsystem 2 (bar 2).

    Computes compressive stress, Euler buckling critical stress, and
    cross-sectional area for bar 2 based on geometry and loading.

    Attributes:
        None specific to this class; inherits from AnalysisInterface.
    """

    def __init__(self) -> None:
        """Initialize Analysis2 instance."""
        pass
        
    def evaluateLocalResponses(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate stress responses for bar 2 (compression member).

        Computes compressive stress, Euler buckling critical stress, and
        cross-sectional area from tube geometry and internal force.

        Args:
            subsystem: The local subsystem basis containing design variables
                and scaling information.
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
        # sort input
        ri2   = des_var[0]  # radius 2
        t2    = des_var[1]  # thickness 2
        fint2 = des_var[2]  # nodalforce 2
        L2    = des_var[3]  # length 2

        E = 73 * 1E9

        # compute coupling parameter
        A2 = 2 * math.pi * ri2 * t2

        #  analysis function
        sigma2      = fint2 / A2  # stress
        sigma_Euler = (math.pi**2) * (ri2**2) * E / (2 * L2**2)  # Euler buckling stress (Eq 8.1)

        # structure output
        responses = [sigma2, sigma_Euler, A2]  # stress, Eulerstress, cross area 2
        # responses is a unscaled quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################      
         
        subsystem.set_Responses_Unscaled(responses)
    
    def mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: LocalSubSystemBasis) -> None:
        """Map computed responses to the parent subsystem.

        Maps cross-sectional area A2 and coupling variables (f2, L2)
        back to subsystem 0 for consistency.

        Args:
            subsystem: The local subsystem basis containing response data
                and mapping interfaces.
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
                                              mappedresponsesin=[scalers[7].transform(responses[2])],
                                              mappedresponsesin_unscaled=[responses[2]])  # cross area 2
        
        subsystem.set_CouplingVariables(id="0",
                                        couplingvariablein=des_var[2:4],
                                        couplingvariablein_unscaled=des_var_unscaled[2:4])  # nodal force 2, length 2

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
        # The mapped responses come from complex physics with no closed-form
        # Jacobian. For consistency with the other use-cases we still call the
        # setter, passing an all-None matrix of the correct shape
        # (number_of_mapped_responses, number_of_design_variables) so the
        # framework finite-differences every entry.
        n_dv: int = len(des_var)
        # id "0": 1 mapped response (cross area 2)
        subsystem.set_MappedResponses_Jacobian(
            id="0",
            mappedresponses_jacobian_in=[[None] * n_dv])
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################

    def mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian(self, subsystem: LocalSubSystemBasis) -> None:
        """Map the Hessians of the mapped responses, if known a priori.

        Args:
            subsystem: The subsystem for which the Hessians are mapped.
        """
        pass