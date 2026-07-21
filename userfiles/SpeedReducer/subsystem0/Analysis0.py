# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Analysis module for Speed Reducer subsystem 0.

Implements the disciplinary analysis for the gear subsystem in the Speed
Reducer problem, handling the shared design variables z1, z2, z3.
"""

from typing import List
from Distributed_Design_Optimizer.subsystem.optimization import AnalysisInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis


class Analysis0(AnalysisInterface):
    """Analysis class for Speed Reducer subsystem 0 (gear subsystem).

    Computes the physical responses related to gear face width, tooth module,
    and number of teeth from the shared design variables.

    Attributes:
        None specific to this class; inherits from AnalysisInterface.
    """

    def __init__(self) -> None:
        """Initialize Analysis0 instance."""
        pass
        
    def evaluateLocalResponses(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate subsystem responses for the gear subsystem.

        Computes physical responses related to gear face width, tooth module,
        and number of teeth from the shared design variables z1, z2, z3.

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
        # responses are the shared design variables z1, z2, z3  
        
        responses = [des_var[0], des_var[1], des_var[2]]
        
        # responses is a unscaled quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
         
        subsystem.set_Responses_Unscaled(responses)
        
    def mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: LocalSubSystemBasis) -> None:
        """Map subsystem responses to neighboring subsystems.

        Distributes shared design variables z1, z2, z3 to both shaft
        subsystems (subsystem 1 and subsystem 2).

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
        
        subsystem.set_SharedDesignVariables(id="1",
                                            shareddesignvariablesin=[des_var[0], des_var[1], des_var[2]],
                                            shareddesignvariablesin_unscaled=[des_var_unscaled[0], des_var_unscaled[1], des_var_unscaled[2]])  # z1, z2, z3 with subsystem 1
        subsystem.set_SharedDesignVariables(id="2",
                                            shareddesignvariablesin=[des_var[0], des_var[1], des_var[2]],
                                            shareddesignvariablesin_unscaled=[des_var_unscaled[0], des_var_unscaled[1], des_var_unscaled[2]])  # z1, z2, z3 with subsystem 2
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################

    def mapLocalResponsesDesignVariables_to_CouplingParameters_Jacobians(self, subsystem: LocalSubSystemBasis) -> None:
        """Map the Jacobians of the mapped responses.

        Args:
            subsystem: The subsystem for which the Jacobians are mapped.
        """
        
        ################################################################
        ###          USER CODE: Compute Jacobians                    ###
        ################################################################
        # This subsystem exchanges only shared design variables (no mapped
        # responses), so there is no mapped-response Jacobian to provide.
        pass
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################

    def mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian(self, subsystem: LocalSubSystemBasis) -> None:
        """Map the Hessians of the mapped responses, if known a priori.

        Args:
            subsystem: The subsystem for which the Hessians are mapped.
        """
        pass
