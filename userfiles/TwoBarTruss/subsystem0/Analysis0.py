# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Analysis module for Two-Bar Truss subsystem 0 (system-level FEM).

Implements the finite element analysis for the Two-Bar Truss structure,
computing mass, displacement, and internal forces from support locations
and cross-sectional areas.
"""

import numpy as np
from typing import List
from Distributed_Design_Optimizer.subsystem.optimization import AnalysisInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis, ScalerZeroOne


class Analysis0(AnalysisInterface):
    """Analysis class for Two-Bar Truss subsystem 0 (system-level).

    Performs FEM analysis to compute total mass, tip displacement,
    internal forces in both bars, and bar lengths.

    Attributes:
        None specific to this class; inherits from AnalysisInterface.
    """

    def __init__(self) -> None:
        """Initialize Analysis0 instance."""
        pass
        
    def evaluateLocalResponses(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the FEM analysis for the Two-Bar Truss system.

        Computes total mass, tip displacement, internal forces in both bars,
        and bar length L2 from support locations and cross-sectional areas.

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
        # Evaluate the FEM Calculations
        Z1 = des_var[0]      # location support 1
        Z2 = des_var[1]      # location support 2

        A1 = des_var[2]      # cross area 1
        A2 = des_var[3]      # cross area 2
        
        E   = 73 * 1E9
        F   = 1.0 * 1E4
        rho = 2800
        L   = 1.0            # fixed truss height

        # compute length
        L1 = np.sqrt(Z1**2 + L**2)  # length of bar 1
        L2 = np.sqrt(Z2**2 + L**2)  # length of bar 2

        # compute internal forces (statically determinate node equilibrium)
        fint1 =  F * L1 / (Z1 + Z2)  # normal force element 1 (tension)
        fint2 = -F * L2 / (Z1 + Z2)  # normal force element 2 (compression)

        # assemble the apex-node stiffness matrix K (Eq 8.10) from the bar
        # direction cosines (node DOFs: horizontal r2, vertical r3)
        c1 =  Z1 / L1  # bar 1 horizontal direction cosine (cos alpha)
        s1 =  L  / L1  # bar 1 vertical direction cosine (sin alpha)
        c2 = -Z2 / L2  # bar 2 horizontal direction cosine (cos beta)
        s2 =  L  / L2  # bar 2 vertical direction cosine (sin beta)

        k11 = E * ((A1 / L1) * c1**2   + (A2 / L2) * c2**2)
        k12 = E * ((A1 / L1) * c1 * s1 + (A2 / L2) * c2 * s2)
        k22 = E * ((A1 / L1) * s1**2   + (A2 / L2) * s2**2)

        # solve K u = P with P = [F, 0] via the Schur complement (Eq 8.11)
        u = F / (k11 - k12**2 / k22)  # horizontal displacement

        # compute total mass
        M = rho * (A1 * L1 + A2 * L2)

        # structure responses
        h = [fint1, fint2, L2]
        r = [M, u]
        responses = np.concatenate([r, h])  # responses = [M, u, fint1, fint2, L2] = [mass, displacement, nodal force 1, nodal force 2, length 2]        
        responses = responses.tolist()
        # responses is a unscaled quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
         
        subsystem.set_Responses_Unscaled(responses)

    def mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: LocalSubSystemBasis) -> None:
        """Map computed responses to neighboring subsystems.

        Maps internal force f1 to subsystem 1 and internal force f2 with
        bar length L2 to subsystem 2 for coupling consistency.

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
        
        subsystem.set_MappedResponseVariables(id="1",
                                              mappedresponsesin=[scalers[7].transform(responses[2])],
                                              mappedresponsesin_unscaled=[responses[2]])  # nodal force 1
        
        rsp: List[float] = responses[3:5]
        scl: List[ScalerZeroOne] = scalers[8:10]
        subsystem.set_MappedResponseVariables(id="2",
                                              mappedresponsesin=[scl[i].transform(rsp[i]) for i in range(len(rsp))],
                                              mappedresponsesin_unscaled=rsp)  # nodal force 2, length 2
        
        subsystem.set_CouplingVariables(id="1",
                                        couplingvariablein=[des_var[2]],
                                        couplingvariablein_unscaled=[des_var_unscaled[2]])  # cross area 1

        subsystem.set_CouplingVariables(id="2",
                                        couplingvariablein=[des_var[3]],
                                        couplingvariablein_unscaled=[des_var_unscaled[3]])  # cross area 2

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
        # id "1": 1 mapped response (nodal force 1)
        subsystem.set_MappedResponses_Jacobian(
            id="1",
            mappedresponses_jacobian_in=[[None] * n_dv])
        # id "2": 2 mapped responses (nodal force 2, length 2)
        subsystem.set_MappedResponses_Jacobian(
            id="2",
            mappedresponses_jacobian_in=[[None] * n_dv for _ in range(2)])
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################

    def mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian(self, subsystem: LocalSubSystemBasis) -> None:
        """Map the Hessians of the mapped responses, if known a priori.

        Args:
            subsystem: The subsystem for which the Hessians are mapped.
        """
        pass

