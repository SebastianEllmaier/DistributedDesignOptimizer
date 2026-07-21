# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Analysis module for Subsystem 0 in the Supersonic Business Jet (SSBJ) problem.

This module defines the Analysis0 class which implements the physics-based
analysis computations and response mapping for Subsystem 0 in the distributed
design optimization framework.
"""

from typing import List
from Distributed_Design_Optimizer.subsystem.optimization import AnalysisInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis
from userfiles.SSBJ.constants import h, Mach
from userfiles.SSBJ.subsystem0.calculate_responses0 import calculate_range


class Analysis0(AnalysisInterface):
    """Analysis class for Subsystem 0 in the Supersonic Business Jet (SSBJ) problem.

    Attributes:
        None specific to this class; inherits from AnalysisInterface.
    """
    def __init__(self) -> None:
        """Initialize the Analysis0 instance."""
        pass
        
    def evaluateLocalResponses(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the physical responses of Subsystem 0.

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

        # unpack design variables
        specific_fuel_consumption = des_var[0]  # [1/hr]
        engine_weight = des_var[1]  # [lb]
        lift_to_drag_ratio = des_var[2]  # [-]
        structural_weight = des_var[3]  # [lb]
        fuel_weight = des_var[4]  # [lb]
        
        total_weight = engine_weight + structural_weight + fuel_weight  # [lb]
        
        range_value = calculate_range(specific_fuel_consumption=specific_fuel_consumption,          
                                      lift_to_drag_ratio=lift_to_drag_ratio,         
                                      total_weight=total_weight,        
                                      fuel_weight=fuel_weight,          
                                      h=h,                   
                                      Mach=Mach)
        
        responses = [range_value,   # [nmi]
                     total_weight]  # [lb]
        
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
        
        subsystem.set_CouplingVariables("1",
                                        couplingvariablein=[des_var[0],   # specific_fuel_consumption [1/hr]
                                                            des_var[1]],  # engine_weight [lb]
                                        couplingvariablein_unscaled=[des_var_unscaled[0],
                                                                     des_var_unscaled[1]])
        
        subsystem.set_CouplingVariables("2",
                                        couplingvariablein=[des_var[2]],  # lift_to_drag_ratio [-]
                                        couplingvariablein_unscaled=[des_var_unscaled[2]])
        
        subsystem.set_MappedResponseVariables(id="2",
                                              mappedresponsesin=[scalers[8].transform(responses[1])],  # total_weight [lb]
                                              mappedresponsesin_unscaled=[responses[1]])
        
        subsystem.set_CouplingVariables("3",
                                        couplingvariablein=[des_var[3],   # structural_weight [lb]
                                                            des_var[4]],  # fuel_weight [lb]
                                        couplingvariablein_unscaled=[des_var_unscaled[3],
                                                                     des_var_unscaled[4]])

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
        # id "2": 1 mapped response (total_weight)
        subsystem.set_MappedResponses_Jacobian(
            id="2",
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

