# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Analysis module for Subsystem 2 in the Supersonic Business Jet (SSBJ) problem.

This module defines the Analysis2 class which implements the physics-based
analysis computations and response mapping for Subsystem 2 in the distributed
design optimization framework.
"""

from typing import List
from Distributed_Design_Optimizer.subsystem.optimization import AnalysisInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis
from userfiles.SSBJ.constants import h, Mach
from userfiles.SSBJ.subsystem2.calculate_responses2 import calculate_drag_polar


class Analysis2(AnalysisInterface):
    """Analysis class for Subsystem 2 in the Supersonic Business Jet (SSBJ) problem.

    Attributes:
        None specific to this class; inherits from AnalysisInterface.
    """
    def __init__(self) -> None:
        """Initialize the Analysis2 instance."""
        pass
        
    def evaluateLocalResponses(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the physical responses of Subsystem 2.

        Computes the subsystem responses based on the current design variables.

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
                  
        [lift, drag, lift_to_drag_ratio, pressure_gradient, wing_lift_coefficient, tail_lift_coefficient] = calculate_drag_polar(tail_sweep_angle=des_var[0],  # [deg]                 
                                                                                                                                 wing_moment_arm=des_var[1],  # [ft]                        
                                                                                                                                 tail_moment_arm=des_var[2],  # [ft]                        
                                                                                                                                 thickness_to_chord_ratio=des_var[3],  # [-]                
                                                                                                                                 wing_sweep_angle=des_var[4],  # [deg]                        
                                                                                                                                 wing_aspect_ratio=des_var[5],  # [-]                      
                                                                                                                                 wing_surface_area=des_var[6],  # [ft^2]                       
                                                                                                                                 tail_aspect_ratio=des_var[7],  # [-]                        
                                                                                                                                 tail_surface_area=des_var[8],  # [ft^2]                        
                                                                                                                                 total_weight=des_var[9],  # [lb]                        
                                                                                                                                 engine_scale_factor=des_var[10],  # [-]                      
                                                                                                                                 wing_twist=des_var[11],  # [deg]                      
                                                                                                                                 h=h,                           
                                                                                                                                 Mach=Mach)                                    
                                                                                                                                 
        responses = [pressure_gradient,      # [0] adverse pressure gradient factor [-]
                     wing_lift_coefficient,  # [1] wing lift coefficient [-]
                     tail_lift_coefficient,  # [2] tail lift coefficient [-]
                     lift,                   # [3] lift [lb]
                     drag,                   # [4] drag [lb]
                     lift_to_drag_ratio]     # [5] lift-to-drag ratio [-]        
        
        # responses is a unscaled quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
         
        subsystem.set_Responses_Unscaled(responses)

    def mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: LocalSubSystemBasis) -> None:
        """Map responses and design variables for inter-subsystem coupling.

        Args:
            subsystem: The LocalSubSystemBasis instance containing responses
                and design variables to be mapped.
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
                                              mappedresponsesin=[scalers[17].transform(responses[5])],  # lift_to_drag_ratio [-]
                                              mappedresponsesin_unscaled=[responses[5]])
        
        subsystem.set_CouplingVariables("0",
                                        couplingvariablein=[des_var[9]],  # total_weight [lb]
                                        couplingvariablein_unscaled=[des_var_unscaled[9]])
        
        subsystem.set_CouplingVariables("1",
                                        couplingvariablein=[des_var[10]],  # engine_scale_factor [-]
                                        couplingvariablein_unscaled=[des_var_unscaled[10]]) 
        
        subsystem.set_MappedResponseVariables(id="1",
                                              mappedresponsesin=[scalers[18].transform(responses[4])],  # drag [lb]
                                              mappedresponsesin_unscaled=[responses[4]])
        
        subsystem.set_CouplingVariables("3",
                                        couplingvariablein=[des_var[11]],  # wing_twist [deg]
                                        couplingvariablein_unscaled=[des_var_unscaled[11]])
        
        subsystem.set_MappedResponseVariables(id="3",
                                              mappedresponsesin=[scalers[19].transform(responses[3])],  # lift [lb]
                                              mappedresponsesin_unscaled=[responses[3]])
        
        subsystem.set_SharedDesignVariables(id="3",
                                            shareddesignvariablesin=des_var[3:9],  # [thickness_to_chord_ratio [-], wing_sweep_angle [deg], wing_aspect_ratio [-], wing_surface_area [ft^2], tail_aspect_ratio [-], tail_surface_area [ft^2]]
                                            shareddesignvariablesin_unscaled=des_var_unscaled[3:9])
        
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################

        return
    
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
        # id "0": 1 mapped response (lift_to_drag_ratio)
        subsystem.set_MappedResponses_Jacobian(
            id="0",
            mappedresponses_jacobian_in=[[None] * n_dv])
        # id "1": 1 mapped response (drag)
        subsystem.set_MappedResponses_Jacobian(
            id="1",
            mappedresponses_jacobian_in=[[None] * n_dv])
        # id "3": 1 mapped response (lift)
        subsystem.set_MappedResponses_Jacobian(
            id="3",
            mappedresponses_jacobian_in=[[None] * n_dv])
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################

    def mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian(self, subsystem: LocalSubSystemBasis) -> None:
        """Map the Hessians of the mapped responses, if known a priori.

        Args:
            subsystem: The subsystem for which the Hessians are mapped.
        """
        
        ################################################################
        ###          USER CODE: Compute Hessians                     ###
        ################################################################
        # No closed-form Hessian available (complex physics); return None to let
        # the framework fall back to its internal finite-difference computation.
        return None
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
