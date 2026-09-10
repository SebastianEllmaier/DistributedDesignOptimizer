---
title: Analysis3 (Source)
---

← Back to [Analysis3 documentation](Analysis3.md)

# Analysis3 - Source Code

**File:** `userfiles\SSBJ\subsystem3\Analysis3.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Analysis module for Subsystem 3 in the Supersonic Business Jet (SSBJ) problem.

This module defines the Analysis3 class which implements the physics-based
analysis computations and response mapping for Subsystem 3 in the distributed
design optimization framework.
"""

from typing import List
from Distributed_Design_Optimizer.subsystem.optimization import AnalysisInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis
from userfiles.SSBJ.constants import h
from userfiles.SSBJ.subsystem3.calculate_responses3 import calculate_structural_responses


class Analysis3(AnalysisInterface):
    """Analysis class for Subsystem 3 in the Supersonic Business Jet (SSBJ) problem.

    Attributes:
        None specific to this class; inherits from AnalysisInterface.
    """
    def __init__(self) -> None:
        """Initialize the Analysis3 instance."""
        pass
        
    def evaluateLocalResponses(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the physical responses of Subsystem 3.

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
        
        C_structure, t_ft, ts_ft, hspar_margin, structural_weight, fuel_weight, wing_twist = calculate_structural_responses(
                                                                                   taper_ratio=des_var[0],  # [-]
                                                                                   alpha1=[des_var[i] for i in range(1, 4)],  # top-sandwich depth fractions [-]
                                                                                   alpha3=[des_var[i] for i in range(4, 7)],  # bottom-sandwich depth fractions [-]
                                                                                   ts2=[des_var[i] for i in range(7, 10)],  # web sandwich thicknesses [in]
                                                                                   rho1=[des_var[i] for i in range(10, 13)],  # top skin ratios [-]
                                                                                   rho2=[des_var[i] for i in range(13, 16)],  # web skin ratios [-]
                                                                                   rho3=[des_var[i] for i in range(16, 19)],  # bottom skin ratios [-]
                                                                                   thickness_to_chord_ratio=des_var[19],  # [-]
                                                                                   wing_sweep_angle=des_var[20],  # [deg]
                                                                                   wing_aspect_ratio=des_var[21],  # [-]
                                                                                   wing_surface_area=des_var[22],  # [ft^2]
                                                                                   tail_aspect_ratio=des_var[23],  # [-]
                                                                                   tail_surface_area=des_var[24],  # [ft^2]
                                                                                   lift=des_var[25],  # [lb]
                                                                                   h=h)  # altitude [ft] (unused in structural physics)

        # responses layout: C_structure (stresses/buckling/h_spar, all [lb/ft^2] except h_spar [ft]),
        # t_ft/ts_ft reconstructed thicknesses [ft], hspar_margin [-], structural_weight [lb],
        # fuel_weight [lb], wing_twist = delta(L)/q effective area [ft^2]
        responses = C_structure + t_ft + ts_ft + hspar_margin + [structural_weight, fuel_weight, wing_twist]
        
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
                                              mappedresponsesin=[scalers[121].transform(responses[-3]),   # structural_weight [lb]
                                                                 scalers[122].transform(responses[-2])],  # fuel_weight [lb]
                                              mappedresponsesin_unscaled=[responses[-3],
                                                                          responses[-2]])
        
        subsystem.set_CouplingVariables("2",
                                        couplingvariablein=[des_var[25]],  # lift [lb]
                                        couplingvariablein_unscaled=[des_var_unscaled[25]])
        
        subsystem.set_MappedResponseVariables(id="2",
                                              mappedresponsesin=[scalers[123].transform(responses[-1])],  # wing_twist = delta(L)/q [ft^2]
                                              mappedresponsesin_unscaled=[responses[-1]])
        
        subsystem.set_TargetSharedDesignVariables(id="2",
                                                  targetdesignvariablesin=des_var[19:25],  # [thickness_to_chord_ratio [-], wing_sweep_angle [deg], wing_aspect_ratio [-], wing_surface_area [ft^2], tail_aspect_ratio [-], tail_surface_area [ft^2]]
                                                  targetdesignvariablesin_unscaled=des_var_unscaled[19:25])
        
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
        # id "0": 2 mapped responses (structural_weight, fuel_weight)
        subsystem.set_MappedResponses_Jacobian(
            id="0",
            mappedresponses_jacobian_in=[[None] * n_dv for _ in range(2)])
        # id "2": 1 mapped response (wing_twist)
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

```
