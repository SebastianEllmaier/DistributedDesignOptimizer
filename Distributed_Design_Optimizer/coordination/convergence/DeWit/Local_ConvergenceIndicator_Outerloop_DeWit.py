# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""DeWit local outer loop convergence indicator.

Evaluates outer loop convergence at the subsystem level by checking that
all inconsistencies and coupling parameter changes are within tolerance.
"""

import numpy as np
from typing import List
from Distributed_Design_Optimizer.coordination.convergence import Local_ConvergenceIndicator_Outerloop_Interface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.couplingparameters import SubSysCouplingParametersBasis
from Distributed_Design_Optimizer.middlelevel import InConsistencySizeInterface


class Local_ConvergenceIndicator_Outerloop_DeWit(Local_ConvergenceIndicator_Outerloop_Interface):
    """Local outer loop convergence indicator - DeWit.
    
    Evaluates outer loop convergence at the subsystem level by checking that
    all inconsistencies and coupling parameter changes are within tolerance.
    Each subsystem has its own instance of this class.
    
    Attributes:
        _toleranceconsistency: Tolerance for consistency constraints and coupling changes.
    """
    
    def __init__(self, toleranceconsistency: float) -> None:
        """Initialize the local DeWit outer loop convergence indicator.

        Args:
            toleranceconsistency: Tolerance for consistency constraints.
        """
        self._toleranceconsistency: float = toleranceconsistency
    
    def evaluate(self, subsystem: LocalSubSystemBasis) -> bool:
        """Evaluate if local outer loop convergence criteria is met.

        Checks that all inconsistencies and coupling parameter changes
        are within the specified tolerance.

        Args:
            subsystem: The subsystem to evaluate convergence for.

        Returns:
            bool: True if convergence condition is met, False otherwise.
        """
        subsystem.evaluate_Inconsistencies()
        inconsistencies = subsystem.get_Inconsistencies()
        coupling = subsystem.get_CouplingParameters()
        coupling_previous_outerloop_itr = subsystem.copy_Coupling_Previous_outerloop_itr()
        
        # Filter to local coupling parameters only (excluding controller coupling parameters,
        # which do not carry coupling variables, mapped responses, or shared design variables)
        local_coupling = [c for c in coupling if isinstance(c, SubSysCouplingParametersBasis)]
        local_coupling_previous = [c for c in coupling_previous_outerloop_itr if isinstance(c, SubSysCouplingParametersBasis)]
        
        # Check all inconsistencies are within tolerance
        convequal = self.check_inconsistencies(inconsistencies)
        
        # Check coupling parameter changes are within tolerance
        convrate = self.check_coupling_reduction(local_coupling, local_coupling_previous)
        
        # Both conditions must be met
        return convequal and convrate
    
    def check_inconsistencies(self, inconsistencies: List[InConsistencySizeInterface]) -> bool:
        """Check if all inconsistencies are within tolerance.

        Args:
            inconsistencies: List of inconsistency size objects.

        Returns:
            bool: True if all inconsistencies are within tolerance.
        """
        # Per-inconsistency-type convergence flags across all inconsistencies
        conv_incon_mapres_minus_copycoupl: List[bool] = []   # mapped-response side inconsistencies
        conv_incon_copymapres_minus_coupl: List[bool] = []  # coupling-variable side inconsistencies
        conv_incon_shared_minus_copytgtshared: List[bool] = [] # shared design variable inconsistencies
        conv_incon_copyshared_minus_tgtshared: List[bool] = [] # target shared design variable inconsistencies
        
        for i in range(len(inconsistencies)):
            
            # Mapped-response side: mapped response minus copied coupling variable, i.e. |mapped_response - copy_coupling_variable|
            incon_mapres_minus_copycoupl = inconsistencies[i].get_MappedResponse_Minus_CopyCouplingVariable()
            if incon_mapres_minus_copycoupl is not None:
                conv_incon_mapres_minus_copycoupl.append(all(abs(incon_mapres_minus_copycoupl[j]) <= self._toleranceconsistency for j in range(len(incon_mapres_minus_copycoupl))))
            
            # Coupling-variable side: copied mapped response minus coupling variable, i.e. |copy_mapped_response - coupling_variable|
            incon_copymapres_minus_coupl = inconsistencies[i].get_CopyMappedResponse_Minus_CouplingVariable()
            if incon_copymapres_minus_coupl is not None:
                conv_incon_copymapres_minus_coupl.append(all(abs(incon_copymapres_minus_coupl[j]) <= self._toleranceconsistency for j in range(len(incon_copymapres_minus_coupl))))
            
            # Shared-design-variable side: shared design variable minus copied target shared design variable, i.e. |shared_design_variable - copy_target_shared_design_variable|
            incon_shared_minus_copytgtshared = inconsistencies[i].get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable()
            if incon_shared_minus_copytgtshared is not None:
                conv_incon_shared_minus_copytgtshared.append(all(abs(incon_shared_minus_copytgtshared[j]) <= self._toleranceconsistency for j in range(len(incon_shared_minus_copytgtshared))))
            
            # Target-shared-design-variable side: copied shared design variable minus target shared design variable, i.e. |copy_shared_design_variable - target_shared_design_variable|
            incon_copyshared_minus_tgtshared = inconsistencies[i].get_CopySharedDesignVariable_Minus_TargetSharedDesignVariable()
            if incon_copyshared_minus_tgtshared is not None:
                conv_incon_copyshared_minus_tgtshared.append(all(abs(incon_copyshared_minus_tgtshared[j]) <= self._toleranceconsistency for j in range(len(incon_copyshared_minus_tgtshared))))
        
        # All inconsistency types across all inconsistencies must be within tolerance
        converged = all(conv_incon_mapres_minus_copycoupl) and all(conv_incon_copymapres_minus_coupl) and all(conv_incon_shared_minus_copytgtshared) and all(conv_incon_copyshared_minus_tgtshared)
        return converged
    
    def check_coupling_reduction(self, couplingNew: List[SubSysCouplingParametersBasis], couplingOld: List[SubSysCouplingParametersBasis]) -> bool:
        """Check if the coupling variable reduction is within tolerance.

        Args:
            couplingNew: Current coupling parameters.
            couplingOld: Previous coupling parameters.

        Returns:
            bool: True if reduction is within tolerance.
        """
        decrement: List[float] = []
        
        for i in range(len(couplingNew)):
            if ((couplingOld[i].get_CouplingVariable() is not None) and
                    (couplingNew[i].get_CouplingVariable() is not None)):
                coupling_old: List[float] = couplingOld[i].get_CouplingVariable()
                coupling_new: List[float] = couplingNew[i].get_CouplingVariable()
                for j in range(len(coupling_old)):
                    decrement.append(coupling_new[j] - coupling_old[j])

            if ((couplingOld[i].get_MappedResponses() is not None) and
                    (couplingNew[i].get_MappedResponses() is not None)):
                map_new: List[float] = couplingNew[i].get_MappedResponses()
                map_old: List[float] = couplingOld[i].get_MappedResponses()
                for j in range(len(map_old)):
                    decrement.append(map_new[j] - map_old[j])

            if ((couplingOld[i].get_SharedDesignVariables() is not None) and
                    (couplingNew[i].get_SharedDesignVariables() is not None)):
                shared_new: List[float] = couplingNew[i].get_SharedDesignVariables()
                shared_old: List[float] = couplingOld[i].get_SharedDesignVariables()
                for j in range(len(shared_old)):
                    decrement.append(shared_new[j] - shared_old[j])

            if ((couplingOld[i].get_TargetSharedDesignVariables() is not None) and
                    (couplingNew[i].get_TargetSharedDesignVariables() is not None)):
                target_new: List[float] = couplingNew[i].get_TargetSharedDesignVariables()
                target_old: List[float] = couplingOld[i].get_TargetSharedDesignVariables()
                for j in range(len(target_old)):
                    decrement.append(target_new[j] - target_old[j])

        if decrement:
            infnorm = np.linalg.norm(np.array(decrement), ord=np.inf)
            if infnorm > self._toleranceconsistency:
                return False
            return True
        else:
            return True
    
    def get_ToleranceConsistency(self) -> float:
        """Get the tolerance for consistency convergence.

        Returns:
            The consistency tolerance threshold value.
        """
        return self._toleranceconsistency
    
    def update_state(self, other: 'Local_ConvergenceIndicator_Outerloop_DeWit') -> None:
        """Update the state of this convergence indicator with the state of another.

        Args:
            other: The convergence indicator to copy state from.
        """
        # toleranceconsistency is immutable and does not change during optimization
        pass
