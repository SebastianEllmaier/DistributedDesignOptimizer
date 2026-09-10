---
title: Analysis0 (Source)
---

← Back to [Analysis0 documentation](Analysis0.md)

# Analysis0 - Source Code

**File:** `userfiles\GeometricProgramming\subsystem0\Analysis0.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Analysis module for Subsystem 0 in the Geometric Programming Top-Down Hierarchic problem.

This module defines the Analysis0 class which implements the physics-based
analysis computations and response mapping for Subsystem 0 in the distributed
design optimization framework.
"""

from typing import List
from Distributed_Design_Optimizer.subsystem.optimization import AnalysisInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis


class Analysis0(AnalysisInterface):
    """Analysis class for Subsystem 0.

    Implements the AnalysisInterface to compute physical responses and map
    coupling variables for Subsystem 0 in the Geometric Programming problem.
    This subsystem acts as the root level in the hierarchical decomposition.

    Attributes:
        None specific to this class; inherits from AnalysisInterface.
    """
    def __init__(self) -> None:
        """Initialize the Analysis0 instance."""
        pass
        
    def evaluateLocalResponses(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the physical responses of Subsystem 0.

        Computes the subsystem responses based on the current design variables.
        The responses are calculated using geometric programming formulas involving
        powers and inverse powers of design variables.

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
        
        responses = [(des_var[3]**2) + (des_var[4]**2) + (des_var[0]**-2) + 2 * ((des_var[1] / 10)**2) + ((des_var[2] / 10)**2), 
                     (des_var[3]**-2) + (des_var[0]**2) - ((des_var[1] / 10)**2), 
                     (des_var[4]**-2) + ((des_var[1] / 10)**2) - ((des_var[2] / 10)**2)]
        
        # responses is a unscaled quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        subsystem.set_Responses_Unscaled(responses)

    def mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: LocalSubSystemBasis) -> None:
        """Map responses and design variables for inter-subsystem coupling.

        Maps computed responses and shared/target design variables to neighboring
        subsystems.

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
        
        # subsystem.set_MappedResponseVariables(id=,
        #                                       mappedresponsesin=,
        #                                       mappedresponsesin_unscaled=)
        # subsystem.set_MappedResponseVariables(id=,
        #                                       mappedresponsesin=,
        #                                       mappedresponsesin_unscaled=)
        
        subsystem.set_CouplingVariables(id="1",
                                        couplingvariablein=[des_var[3]],
                                        couplingvariablein_unscaled=[des_var_unscaled[3]])  # ^{1}_{0}h
        
        subsystem.set_CouplingVariables(id="2",
                                        couplingvariablein=[des_var[4]],
                                        couplingvariablein_unscaled=[des_var_unscaled[4]])  # ^{2}_{0}h
        
        # subsystem.set_TargetSharedDesignVariables(id=,
        #                                     targetdesignvariablesin=,
        #                                     targetdesignvariablesin_unscaled=)
        # subsystem.set_TargetSharedDesignVariables(id=,
        #                                     targetdesignvariablesin=,
        #                                     targetdesignvariablesin_unscaled=)
        
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
        
        # No mapped responses, hence, pass
        pass    
    
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
        
        # No mapped responses, hence, pass
        pass    
    
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################

```
