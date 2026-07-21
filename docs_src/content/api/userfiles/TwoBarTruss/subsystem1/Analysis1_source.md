---
title: Analysis1 (Source)
---

← Back to [Analysis1 documentation](Analysis1.md)

# Analysis1 - Source Code

**File:** `userfiles\TwoBarTruss\subsystem1\Analysis1.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Analysis module for Two-Bar Truss subsystem 1 (bar 1 sizing).

Implements the analysis for bar 1 in the Two-Bar Truss structure,
computing cross-sectional area and stress from radius and thickness.
"""

import math
from typing import List
from Distributed_Design_Optimizer.subsystem.optimization import AnalysisInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis


class Analysis1(AnalysisInterface):
    """Analysis class for Two-Bar Truss subsystem 1 (bar 1).

    Computes cross-sectional area and axial stress for bar 1
    based on tube radius, thickness, and internal force.

    Attributes:
        None specific to this class; inherits from AnalysisInterface.
    """

    def __init__(self) -> None:
        """Initialize Analysis1 instance."""
        pass

    def evaluateLocalResponses(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate cross-sectional area and stress for bar 1.

        Computes the cross-sectional area from tube radius and thickness,
        then calculates axial stress from internal force.

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
        # reorder input
        ri1   = des_var[0]  # radius 1
        t1    = des_var[1]  # thickness 1
        fint1 = des_var[2]  # nodal force 1

        # compute coupling variables
        A1 = 2 * math.pi * ri1 * t1

        # compute local response
        sigma1 = fint1 / A1

        #  structure output
        responses = [sigma1, A1]  # stress, cross area 1
        # responses is a unscaled quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
         
        subsystem.set_Responses_Unscaled(responses)

    def mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: LocalSubSystemBasis) -> None:
        """Map computed responses to the parent subsystem.

        Maps cross-sectional area A1 and internal force f1 coupling
        variable back to subsystem 0.

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
                                              mappedresponsesin=[scalers[6].transform(responses[1])],
                                              mappedresponsesin_unscaled=[responses[1]])  # cross area 1
        
        subsystem.set_CouplingVariables(id="0",
                                        couplingvariablein=[des_var[2]],
                                        couplingvariablein_unscaled=[des_var_unscaled[2]])  # nodal force 1

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
        # id "0": 1 mapped response (cross area 1)
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

```
