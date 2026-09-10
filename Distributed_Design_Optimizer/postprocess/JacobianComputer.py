# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Jacobian computation module.

This module provides functionality for computing Jacobian matrices
in distributed optimization problems.
"""

import copy
from typing import List

import numpy as np
from Distributed_Design_Optimizer.subsystem.optimization.optimizerdata import OptimDataBasis
from Distributed_Design_Optimizer.subsystem.couplingparameters import CouplingParametersInterface
from Distributed_Design_Optimizer.subsystem import SubSystemInterface



class JacobianComputer:
    """Computes Jacobian matrices for mapped response variables."""

    def __init__(self):
        """Initialize the JacobianComputer."""
        pass

    def execute(self, subsystemin: SubSystemInterface) -> None:
        """Execute Jacobian computation for a subsystem.

        Args:
            subsystemin: The subsystem interface to compute Jacobian for.
        """
        
        couplings_optimdata: List[CouplingParametersInterface] = subsystemin.get_CouplingParameters()
        if subsystemin.get_OptimData() is None:
            # Create a properly structured 3D jacobian with None values
            jacobian = []
            
            # For each coupling, create a list of mapped responses
            for coupling in couplings_optimdata:
                coupling_jacobian = None               
                jacobian.append(coupling_jacobian)            
            subsystemin.set_Jacobian_MappedResponse_Wrt_DesignVariables(jacobian)
            
        else:
            
            # compute jacobian of mapped responses at xopt_scaled
            xopt_scaled: List[float] = copy.copy(subsystemin.get_OptimData().get_DesignVariables())  # scaled01 value
            len_xopt_scaled = len(xopt_scaled)            
            lowerbounds = subsystemin.get_LowerBounds_Unscaled()  # unscaled values
            lowerbounds_scaled: List[float] = [subsystemin.get_Scalers()[i].transform(lowerbounds[i]) for i in range(len(lowerbounds))]
            upperbounds = subsystemin.get_UpperBounds_Unscaled()  # unscaled values
            upperbounds_scaled: List[float] = [subsystemin.get_Scalers()[i].transform(upperbounds[i]) for i in range(len(upperbounds))]
            
            epsilon_scaled = [None] * len(subsystemin.get_DesignVariables_Granularity())
            for i in range(len(epsilon_scaled)):
                granularity = subsystemin.get_DesignVariables_Granularity()[i]
                if granularity == 0.0:  # continuous
                    epsilon_scaled[i] = 1E-6  # continuous epsilon
                elif granularity > 0.0:  # discrete
                    epsilon_scaled[i] = granularity  # take the designvariable's granularity as epsilon
                else:
                    raise ValueError(f"Invalid granularity at index {i}: {granularity}. Must be >= 0.0")
            
            # get a copy of the total mapped response for a subsystem 
            total_original_mapped_responses = []
            # track the coupling indices which have mapped response 
            coupling_idx_with_mapped_responses = []
            for idx, coupling in enumerate(couplings_optimdata):
                if coupling.get_MappedResponses() is not None:
                    total_original_mapped_responses.append(copy.copy(coupling.get_MappedResponses()))
                    coupling_idx_with_mapped_responses.append(idx)
            
            # initalize the jacobian of a subsystem. a 3D list
            # first dimension: coupling
            # second dimension: mapped response
            # third dimension: design variable
            jacobian = [None] * len(couplings_optimdata)
            
            # for each coupling parameter
            for response_idx, coupling_idx in enumerate(coupling_idx_with_mapped_responses):
                # get the mapped response for the coupling parameter
                couplingparameter: CouplingParametersInterface = couplings_optimdata[coupling_idx]
                mappedresponse = total_original_mapped_responses[response_idx]
                len_mappedresponse = len(mappedresponse)
                
                # mappedresponse.designvariable jacobian per coupling
                jacobian_per_coupling = np.zeros((len_mappedresponse, len(xopt_scaled)))
                
                # for each mapped response in the mapped response vector
                for mappedresponse_idx in range(len_mappedresponse):
                    # for each design variable in the design variable vector
                    for j in range(len_xopt_scaled):
                        # create a perturbed design vector
                        x_perturbed_scaled = copy.copy(xopt_scaled)  # scaled01 value
                        
                        # based on the bounds determine appropriate differenciation method
                        if upperbounds_scaled[j] is not None and xopt_scaled[j] + epsilon_scaled[j] > upperbounds_scaled[j]:
                            # near the upper bound -> Backward differentiation
                            x_perturbed_scaled[j] -= epsilon_scaled[j]
                            subsystemin.set_DesignVariables(x_perturbed_scaled)
                            subsystemin.evaluateTotalObjective()
                            subsystemin.evaluateTotalConstraint()
                            perturbed_mapped_response = couplingparameter.get_MappedResponses()
                            derivative = (total_original_mapped_responses[response_idx][mappedresponse_idx] - perturbed_mapped_response[mappedresponse_idx]) / epsilon_scaled[j]
                            
                        elif lowerbounds_scaled[j] is not None and xopt_scaled[j] - epsilon_scaled[j] < lowerbounds_scaled[j]:
                            # near the lower bound -> Forward differentiation
                            x_perturbed_scaled[j] += epsilon_scaled[j]
                            subsystemin.set_DesignVariables(x_perturbed_scaled)
                            subsystemin.evaluateTotalObjective()
                            subsystemin.evaluateTotalConstraint()
                            perturbed_mapped_response = couplingparameter.get_MappedResponses()
                            derivative = (perturbed_mapped_response[mappedresponse_idx] - total_original_mapped_responses[response_idx][mappedresponse_idx]) / epsilon_scaled[j]
                            
                        else:
                            # Not near the bounds - use central differentiation
                            # ensure forward/backward response does not fall out of the bounds
                            x_forward_scaled = copy.copy(xopt_scaled)
                            x_forward_scaled[j] += epsilon_scaled[j]
                            x_backward_scaled = copy.copy(xopt_scaled)
                            x_backward_scaled[j] -= epsilon_scaled[j]
                            # check bounds
                            if upperbounds_scaled[j] is not None and x_forward_scaled[j] > upperbounds_scaled[j]:
                                x_forward_scaled[j] = xopt_scaled[j]
                            if lowerbounds_scaled[j] is not None and x_backward_scaled[j] < lowerbounds_scaled[j]:
                                x_backward_scaled[j] = xopt_scaled[j]
                            subsystemin.set_DesignVariables(x_forward_scaled)
                            subsystemin.evaluateTotalObjective()
                            subsystemin.evaluateTotalConstraint()
                            forward_perturbed_mapped_response = couplingparameter.get_MappedResponses()
                            subsystemin.set_DesignVariables(x_backward_scaled)
                            subsystemin.evaluateTotalObjective()
                            subsystemin.evaluateTotalConstraint()
                            backward_perturbed_mapped_response = couplingparameter.get_MappedResponses()
                            derivative = (forward_perturbed_mapped_response[mappedresponse_idx] - backward_perturbed_mapped_response[mappedresponse_idx]) / (2*epsilon_scaled[j])
                            
                        # reset the original values
                        subsystemin.set_DesignVariables(xopt_scaled)
                        subsystemin.evaluateTotalObjective()
                        subsystemin.evaluateTotalConstraint()
                        jacobian_per_coupling[mappedresponse_idx, j] = derivative
                                    
                jacobian[coupling_idx] = jacobian_per_coupling.tolist()
                        
            # jacobina is of type List[List[List[float]]], where the first index corresponds to the index of subsystemin.get_CouplingParameters()      
            subsystemin.set_Jacobian_MappedResponse_Wrt_DesignVariables(jacobian)
            
 