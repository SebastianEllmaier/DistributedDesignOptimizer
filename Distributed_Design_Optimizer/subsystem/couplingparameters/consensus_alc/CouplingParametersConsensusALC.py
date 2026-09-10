# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Consensus ALC coupling parameters module.

This module provides coupling parameters for the
consensus-based Augmented Lagrangian Coordination method.
"""

import copy
from typing import List
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive
from Distributed_Design_Optimizer.subsystem.couplingparameters import SubSysCouplingParametersBasis
from Distributed_Design_Optimizer.middlelevel.consensus_alc import MiddleLevelCouplingConsensusALC


class CouplingParametersConsensusALC(SubSysCouplingParametersBasis):
    """Coupling parameters for consensus-based ALC.

    Stores auxiliary variables, weights, and Lagrange multipliers for
    consensus-based Augmented Lagrangian Coordination.
    """

    def __init__(self, id: str) -> None:
        """Initialize CouplingParametersConsensusALC.

        Args:
            id: Identifier for this coupling.
        """
        super().__init__(id)

        # Auxiliary variables from consensus constraints
        self._auxiliary_mappedresponse: List[float] | None = None
        self._auxiliary_couplingvariable: List[float] | None = None
        self._auxiliary_shareddesignvariable: List[float] | None = None
        self._auxiliary_targetshareddesignvariable: List[float] | None = None
        
        self._weights_auxiliary_minus_mappedresponse: List[float] | None = None
        self._weights_auxiliary_minus_couplingvariable: List[float] | None = None
        self._weights_auxiliary_minus_shareddesignvariable: List[float] | None = None
        self._weights_auxiliary_minus_targetshareddesignvariable: List[float] | None = None
        
        self._multipliers_auxiliary_minus_mappedresponse: List[float] | None = None
        self._multipliers_auxiliary_minus_couplingvariable: List[float] | None = None
        self._multipliers_auxiliary_minus_shareddesignvariable: List[float] | None = None
        self._multipliers_auxiliary_minus_targetshareddesignvariable: List[float] | None = None
        
        # The weights and Lagrange mulitpliers with respect to the consensus constraints of neighbors
        self._copy_weights_auxiliary_minus_mappedresponse: List[float] | None = None
        self._copy_weights_auxiliary_minus_couplingvariable: List[float] | None = None
        self._copy_weights_auxiliary_minus_shareddesignvariable: List[float] | None = None
        self._copy_weights_auxiliary_minus_targetshareddesignvariable: List[float] | None = None
        
        self._copy_multipliers_auxiliary_minus_mappedresponse: List[float] | None = None
        self._copy_multipliers_auxiliary_minus_couplingvariable: List[float] | None = None
        self._copy_multipliers_auxiliary_minus_shareddesignvariable: List[float] | None = None
        self._copy_multipliers_auxiliary_minus_targetshareddesignvariable: List[float] | None = None

    def set_Auxiliary_MappedResponse(self, auxiliary_mappedresponse_in: List[float]) -> None:
        """Set the auxiliary consensus variables for the mapped-response side of the coupling circle.

        Args:
            auxiliary_mappedresponse_in: Auxiliary consensus variable matched against the mapped response.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._auxiliary_mappedresponse = copy.copy(auxiliary_mappedresponse_in)
        
    def get_Auxiliary_MappedResponse(self) -> List[float] | None:
        """Return the auxiliary consensus variables for the mapped-response side of the coupling circle.

        Returns:
            Auxiliary consensus variables for the mapped-response side, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._auxiliary_mappedresponse)
    
    def set_Auxiliary_CouplingVariable(self, auxiliary_couplingvariable_in: List[float]) -> None:
        """Set the auxiliary consensus variables for the coupling-variable side of the coupling circle.

        Args:
            auxiliary_couplingvariable_in: Auxiliary consensus variable matched against the coupling variable.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._auxiliary_couplingvariable = copy.copy(auxiliary_couplingvariable_in)
        
    def get_Auxiliary_CouplingVariable(self) -> List[float] | None:
        """Return the auxiliary consensus variables for the coupling-variable side of the coupling circle.

        Returns:
            Auxiliary consensus variables for the coupling-variable side, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._auxiliary_couplingvariable)
    
    def set_Auxiliary_SharedDesignVariable(self, auxiliary_shareddesignvariable_in: List[float]) -> None:
        """Set the auxiliary consensus variables for the shared-design-variable side of the coupling circle.

        Args:
            auxiliary_shareddesignvariable_in: Auxiliary consensus variable matched against the shared design variable.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._auxiliary_shareddesignvariable = copy.copy(auxiliary_shareddesignvariable_in)
        
    def get_Auxiliary_SharedDesignVariable(self) -> List[float] | None:
        """Return the auxiliary consensus variables for the shared-design-variable side of the coupling circle.

        Returns:
            Auxiliary consensus variables for the shared-design-variable side, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._auxiliary_shareddesignvariable)
    
    def set_Auxiliary_TargetSharedDesignVariable(self, auxiliary_targetshareddesignvariable_in: List[float]) -> None:
        """Set the auxiliary consensus variables for the target-shared-design-variable side of the coupling circle.

        Args:
            auxiliary_targetshareddesignvariable_in: Auxiliary consensus variable matched against the target shared design variable.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._auxiliary_targetshareddesignvariable = copy.copy(auxiliary_targetshareddesignvariable_in)
        
    def get_Auxiliary_TargetSharedDesignVariable(self) -> List[float] | None:
        """Return the auxiliary consensus variables for the target-shared-design-variable side of the coupling circle.

        Returns:
            Auxiliary consensus variables for the target-shared-design-variable side, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._auxiliary_targetshareddesignvariable)
    
    # Weights
    
    def set_Weights_Auxiliary_Minus_MappedResponse(self, auxiliary_minus_mappedresponse_in: List[float]) -> None:
        """Set the penalty weights for the auxiliary-minus-mapped-response part of the coupling circle.

        Args:
            auxiliary_minus_mappedresponse_in: Penalty weights for the auxiliary minus mapped response inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._weights_auxiliary_minus_mappedresponse = copy.copy(auxiliary_minus_mappedresponse_in)
        
    def get_Weights_Auxiliary_Minus_MappedResponse(self) -> List[float] | None:
        """Get the penalty weights for the auxiliary-minus-mapped-response part of the coupling circle.

        Returns:
            Penalty weights for the auxiliary-minus-mapped-response part, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._weights_auxiliary_minus_mappedresponse)
    
    def set_Weights_Auxiliary_Minus_CouplingVariable(self, auxiliary_minus_couplingvariable_in: List[float]) -> None:
        """Set the penalty weights for the auxiliary-minus-coupling-variable part of the coupling circle.

        Args:
            auxiliary_minus_couplingvariable_in: Penalty weights for the auxiliary minus coupling variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._weights_auxiliary_minus_couplingvariable = copy.copy(auxiliary_minus_couplingvariable_in)
        
    def get_Weights_Auxiliary_Minus_CouplingVariable(self) -> List[float] | None:
        """Get the penalty weights for the auxiliary-minus-coupling-variable part of the coupling circle.

        Returns:
            Penalty weights for the auxiliary-minus-coupling-variable part, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._weights_auxiliary_minus_couplingvariable)
    
    def set_Weights_Auxiliary_Minus_SharedDesignVariable(self, auxiliary_minus_shareddesignvariable_in: List[float]) -> None:
        """Set the penalty weights for the auxiliary-minus-shared-design-variable part of the coupling circle.

        Args:
            auxiliary_minus_shareddesignvariable_in: Penalty weights for the auxiliary minus shared design variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._weights_auxiliary_minus_shareddesignvariable = copy.copy(auxiliary_minus_shareddesignvariable_in)
        
    def get_Weights_Auxiliary_Minus_SharedDesignVariable(self) -> List[float] | None:
        """Get the penalty weights for the auxiliary-minus-shared-design-variable part of the coupling circle.

        Returns:
            Penalty weights for the auxiliary-minus-shared-design-variable part, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._weights_auxiliary_minus_shareddesignvariable)
    
    def set_Weights_Auxiliary_Minus_TargetSharedDesignVariable(self, auxiliary_minus_targetshareddesignvariable_in: List[float]) -> None:
        """Set the penalty weights for the auxiliary-minus-target-shared-design-variable part of the coupling circle.

        Args:
            auxiliary_minus_targetshareddesignvariable_in: Penalty weights for the auxiliary minus target shared design variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._weights_auxiliary_minus_targetshareddesignvariable = copy.copy(auxiliary_minus_targetshareddesignvariable_in)
        
    def get_Weights_Auxiliary_Minus_TargetSharedDesignVariable(self) -> List[float] | None:
        """Get the penalty weights for the auxiliary-minus-target-shared-design-variable part of the coupling circle.

        Returns:
            Penalty weights for the auxiliary-minus-target-shared-design-variable part, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._weights_auxiliary_minus_targetshareddesignvariable)
    
    # Multipliers
    
    def set_Multipliers_Auxiliary_Minus_MappedResponse(self, auxiliary_minus_mappedresponse_in: List[float]) -> None:
        """Set the Lagrange multipliers for the auxiliary-minus-mapped-response part of the coupling circle.

        Args:
            auxiliary_minus_mappedresponse_in: Lagrange multipliers for the auxiliary minus mapped response inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_auxiliary_minus_mappedresponse = copy.copy(auxiliary_minus_mappedresponse_in)
        
    def get_Multipliers_Auxiliary_Minus_MappedResponse(self) -> List[float] | None:
        """Get the Lagrange multipliers for the auxiliary-minus-mapped-response part of the coupling circle.

        Returns:
            Lagrange multipliers for the auxiliary-minus-mapped-response part, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_auxiliary_minus_mappedresponse)
    
    def set_Multipliers_Auxiliary_Minus_CouplingVariable(self, auxiliary_minus_couplingvariable_in: List[float]) -> None:
        """Set the Lagrange multipliers for the auxiliary-minus-coupling-variable part of the coupling circle.

        Args:
            auxiliary_minus_couplingvariable_in: Lagrange multipliers for the auxiliary minus coupling variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_auxiliary_minus_couplingvariable = copy.copy(auxiliary_minus_couplingvariable_in)
        
    def get_Multipliers_Auxiliary_Minus_CouplingVariable(self) -> List[float] | None:
        """Get the Lagrange multipliers for the auxiliary-minus-coupling-variable part of the coupling circle.

        Returns:
            Lagrange multipliers for the auxiliary-minus-coupling-variable part, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_auxiliary_minus_couplingvariable)
    
    def set_Multipliers_Auxiliary_Minus_SharedDesignVariable(self, auxiliary_minus_shareddesignvariable_in: List[float]) -> None:
        """Set the Lagrange multipliers for the auxiliary-minus-shared-design-variable part of the coupling circle.

        Args:
            auxiliary_minus_shareddesignvariable_in: Lagrange multipliers for the auxiliary minus shared design variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_auxiliary_minus_shareddesignvariable = copy.copy(auxiliary_minus_shareddesignvariable_in)
        
    def get_Multipliers_Auxiliary_Minus_SharedDesignVariable(self) -> List[float] | None:
        """Get the Lagrange multipliers for the auxiliary-minus-shared-design-variable part of the coupling circle.

        Returns:
            Lagrange multipliers for the auxiliary-minus-shared-design-variable part, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_auxiliary_minus_shareddesignvariable)
    
    def set_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable(self, auxiliary_minus_targetshareddesignvariable_in: List[float]) -> None:
        """Set the Lagrange multipliers for the auxiliary-minus-target-shared-design-variable part of the coupling circle.

        Args:
            auxiliary_minus_targetshareddesignvariable_in: Lagrange multipliers for the auxiliary minus target shared design variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_auxiliary_minus_targetshareddesignvariable = copy.copy(auxiliary_minus_targetshareddesignvariable_in)
        
    def get_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable(self) -> List[float] | None:
        """Get the Lagrange multipliers for the auxiliary-minus-target-shared-design-variable part of the coupling circle.

        Returns:
            Lagrange multipliers for the auxiliary-minus-target-shared-design-variable part, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_auxiliary_minus_targetshareddesignvariable)
    
    # Weights with respect to consensus constraints of neighbors
    def set_Copy_Weights_Auxiliary_Minus_MappedResponse(self, copy_auxiliary_minus_mappedresponse_in: List[float]) -> None:
        """Set the weights for the neighbor consensus constraint w.r.t. the auxiliary-minus-mapped-response part of the coupling circle.

        Args:
            copy_auxiliary_minus_mappedresponse_in: Weights for the neighbor auxiliary minus mapped response inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_weights_auxiliary_minus_mappedresponse = copy.copy(copy_auxiliary_minus_mappedresponse_in)
        
    def get_Copy_Weights_Auxiliary_Minus_MappedResponse(self) -> List[float] | None:
        """Get the weights for the neighbor consensus constraint w.r.t. the auxiliary-minus-mapped-response part of the coupling circle.

        Returns:
            Weights for the neighbor consensus constraint, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_weights_auxiliary_minus_mappedresponse)
    
    def set_Copy_Weights_Auxiliary_Minus_CouplingVariable(self, copy_auxiliary_minus_couplingvariable_in: List[float]) -> None:
        """Set the weights for the neighbor consensus constraint w.r.t. the auxiliary-minus-coupling-variable part of the coupling circle.

        Args:
            copy_auxiliary_minus_couplingvariable_in: Weights for the neighbor auxiliary minus coupling variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_weights_auxiliary_minus_couplingvariable = copy.copy(copy_auxiliary_minus_couplingvariable_in)
        
    def get_Copy_Weights_Auxiliary_Minus_CouplingVariable(self) -> List[float] | None:
        """Get the weights for the neighbor consensus constraint w.r.t. the auxiliary-minus-coupling-variable part of the coupling circle.

        Returns:
            Weights for the neighbor consensus constraint, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_weights_auxiliary_minus_couplingvariable)
    
    def set_Copy_Weights_Auxiliary_Minus_SharedDesignVariable(self, copy_auxiliary_minus_shareddesignvariable_in: List[float]) -> None:
        """Set the weights for the neighbor consensus constraint w.r.t. the auxiliary-minus-shared-design-variable part of the coupling circle.

        Args:
            copy_auxiliary_minus_shareddesignvariable_in: Weights for the neighbor auxiliary minus shared design variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_weights_auxiliary_minus_shareddesignvariable = copy.copy(copy_auxiliary_minus_shareddesignvariable_in)
        
    def get_Copy_Weights_Auxiliary_Minus_SharedDesignVariable(self) -> List[float] | None:
        """Get the weights for the neighbor consensus constraint w.r.t. the auxiliary-minus-shared-design-variable part of the coupling circle.

        Returns:
            Weights for the neighbor consensus constraint, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_weights_auxiliary_minus_shareddesignvariable)
    
    def set_Copy_Weights_Auxiliary_Minus_TargetSharedDesignVariable(self, copy_auxiliary_minus_targetshareddesignvariable_in: List[float]) -> None:
        """Set the weights for the neighbor consensus constraint w.r.t. the auxiliary-minus-target-shared-design-variable part of the coupling circle.

        Args:
            copy_auxiliary_minus_targetshareddesignvariable_in: Weights for the neighbor auxiliary minus target shared design variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_weights_auxiliary_minus_targetshareddesignvariable = copy.copy(copy_auxiliary_minus_targetshareddesignvariable_in)
        
    def get_Copy_Weights_Auxiliary_Minus_TargetSharedDesignVariable(self) -> List[float] | None:
        """Get the weights for the neighbor consensus constraint w.r.t. the auxiliary-minus-target-shared-design-variable part of the coupling circle.

        Returns:
            Weights for the neighbor consensus constraint, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_weights_auxiliary_minus_targetshareddesignvariable) 
    
    # Lagrange multipliers with respect to consensus constraints of neighbors
    def set_Copy_Multipliers_Auxiliary_Minus_MappedResponse(self, copy_auxiliary_minus_mappedresponse_in: List[float]) -> None:
        """Set the Lagrange multipliers for the neighbor consensus constraint w.r.t. the auxiliary-minus-mapped-response part of the coupling circle.

        Args:
            copy_auxiliary_minus_mappedresponse_in: Lagrange multipliers for the neighbor auxiliary minus mapped response inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_multipliers_auxiliary_minus_mappedresponse = copy.copy(copy_auxiliary_minus_mappedresponse_in)
        
    def get_Copy_Multipliers_Auxiliary_Minus_MappedResponse(self) -> List[float] | None:
        """Get the Lagrange multipliers for the neighbor consensus constraint w.r.t. the auxiliary-minus-mapped-response part of the coupling circle.

        Returns:
            Lagrange multipliers for the neighbor consensus constraint, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_multipliers_auxiliary_minus_mappedresponse)
    
    def set_Copy_Multipliers_Auxiliary_Minus_CouplingVariable(self, copy_auxiliary_minus_couplingvariable_in: List[float]) -> None:
        """Set the Lagrange multipliers for the neighbor consensus constraint w.r.t. the auxiliary-minus-coupling-variable part of the coupling circle.

        Args:
            copy_auxiliary_minus_couplingvariable_in: Lagrange multipliers for the neighbor auxiliary minus coupling variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_multipliers_auxiliary_minus_couplingvariable = copy.copy(copy_auxiliary_minus_couplingvariable_in)
        
    def get_Copy_Multipliers_Auxiliary_Minus_CouplingVariable(self) -> List[float] | None:
        """Get the Lagrange multipliers for the neighbor consensus constraint w.r.t. the auxiliary-minus-coupling-variable part of the coupling circle.

        Returns:
            Lagrange multipliers for the neighbor consensus constraint, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_multipliers_auxiliary_minus_couplingvariable)
    
    def set_Copy_Multipliers_Auxiliary_Minus_SharedDesignVariable(self, copy_auxiliary_minus_shareddesignvariable_in: List[float]) -> None:
        """Set the Lagrange multipliers for the neighbor consensus constraint w.r.t. the auxiliary-minus-shared-design-variable part of the coupling circle.

        Args:
            copy_auxiliary_minus_shareddesignvariable_in: Lagrange multipliers for the neighbor auxiliary minus shared design variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_multipliers_auxiliary_minus_shareddesignvariable = copy.copy(copy_auxiliary_minus_shareddesignvariable_in)
        
    def get_Copy_Multipliers_Auxiliary_Minus_SharedDesignVariable(self) -> List[float] | None:
        """Get the Lagrange multipliers for the neighbor consensus constraint w.r.t. the auxiliary-minus-shared-design-variable part of the coupling circle.

        Returns:
            Lagrange multipliers for the neighbor consensus constraint, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_multipliers_auxiliary_minus_shareddesignvariable)
    
    def set_Copy_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable(self, copy_auxiliary_minus_targetshareddesignvariable_in: List[float]) -> None:
        """Set the Lagrange multipliers for the neighbor consensus constraint w.r.t. the auxiliary-minus-target-shared-design-variable part of the coupling circle.

        Args:
            copy_auxiliary_minus_targetshareddesignvariable_in: Lagrange multipliers for the neighbor auxiliary minus target shared design variable inconsistency.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_multipliers_auxiliary_minus_targetshareddesignvariable = copy.copy(copy_auxiliary_minus_targetshareddesignvariable_in)
        
    def get_Copy_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable(self) -> List[float] | None:
        """Get the Lagrange multipliers for the neighbor consensus constraint w.r.t. the auxiliary-minus-target-shared-design-variable part of the coupling circle.

        Returns:
            Lagrange multipliers for the neighbor consensus constraint, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_multipliers_auxiliary_minus_targetshareddesignvariable) 
    
    # General middle level function definition
    
    def CopyFromMiddleLevelCoupling(self, middlelevelcouplingIn: MiddleLevelCouplingConsensusALC) -> None:
        """Copy coupling parameters from the middle level.

        Args:
            middlelevelcouplingIn: Source middle level coupling.

        Raises:
            ValueError: If middlelevelcouplingIn is not a MiddleLevelCouplingConsensusALC instance.
        """
        if not isinstance(middlelevelcouplingIn, MiddleLevelCouplingConsensusALC):
            raise ValueError(f"{DDO_Color}Error in CouplingParametersConsensusALC.CopyFromMiddleLevelCoupling(): type of MiddleLevelCoupling is not matching.{Reset}")

        if middlelevelcouplingIn.get_MappedResponses() is not None:
            self.set_Copy_MappedResponses(middlelevelcouplingIn.get_MappedResponses())
            
        if middlelevelcouplingIn.get_CouplingVariable() is not None:
            self.set_Copy_CouplingVariable(middlelevelcouplingIn.get_CouplingVariable())
            
        if middlelevelcouplingIn.get_SharedDesignVariable() is not None:
            self.set_Copy_SharedDesignVariables(middlelevelcouplingIn.get_SharedDesignVariable())
            
        if middlelevelcouplingIn.get_TargetSharedDesignVariable() is not None:
            self.set_Copy_TargetSharedDesignVariables(middlelevelcouplingIn.get_TargetSharedDesignVariable())
        
        # Get weights of neighboring subsystem    
        
        if middlelevelcouplingIn.get_Weights_Auxiliary_Minus_MappedResponse() is not None:
            self.set_Copy_Weights_Auxiliary_Minus_MappedResponse(middlelevelcouplingIn.get_Weights_Auxiliary_Minus_MappedResponse())
            
        if middlelevelcouplingIn.get_Weights_Auxiliary_Minus_CouplingVariable() is not None:
            self.set_Copy_Weights_Auxiliary_Minus_CouplingVariable(middlelevelcouplingIn.get_Weights_Auxiliary_Minus_CouplingVariable())

        if middlelevelcouplingIn.get_Weights_Auxiliary_Minus_SharedDesignVariable() is not None:
            self.set_Copy_Weights_Auxiliary_Minus_SharedDesignVariable(middlelevelcouplingIn.get_Weights_Auxiliary_Minus_SharedDesignVariable())
            
        if middlelevelcouplingIn.get_Weights_Auxiliary_Minus_TargetSharedDesignVariable() is not None:
            self.set_Copy_Weights_Auxiliary_Minus_TargetSharedDesignVariable(middlelevelcouplingIn.get_Weights_Auxiliary_Minus_TargetSharedDesignVariable())
        
        # Get Lagrange multipliers of neighboring subsystem
        
        if middlelevelcouplingIn.get_Multipliers_Auxiliary_Minus_MappedResponse() is not None:
            self.set_Copy_Multipliers_Auxiliary_Minus_MappedResponse(middlelevelcouplingIn.get_Multipliers_Auxiliary_Minus_MappedResponse())
            
        if middlelevelcouplingIn.get_Multipliers_Auxiliary_Minus_CouplingVariable() is not None:
            self.set_Copy_Multipliers_Auxiliary_Minus_CouplingVariable(middlelevelcouplingIn.get_Multipliers_Auxiliary_Minus_CouplingVariable())
            
        if middlelevelcouplingIn.get_Multipliers_Auxiliary_Minus_SharedDesignVariable() is not None:
            self.set_Copy_Multipliers_Auxiliary_Minus_SharedDesignVariable(middlelevelcouplingIn.get_Multipliers_Auxiliary_Minus_SharedDesignVariable())
            
        if middlelevelcouplingIn.get_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable() is not None:
            self.set_Copy_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable(middlelevelcouplingIn.get_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable())
            
    def CopyToMiddleLevelCoupling(self, middlelevelcouplingIn: MiddleLevelCouplingConsensusALC) -> None:
        """Copy coupling parameters to the middle level.

        Args:
            middlelevelcouplingIn: Target middle level coupling.

        Raises:
            ValueError: If middlelevelcouplingIn is not a MiddleLevelCouplingConsensusALC instance.
        """
        if not isinstance(middlelevelcouplingIn, MiddleLevelCouplingConsensusALC):
            raise ValueError(f"{DDO_Color}Error in CouplingParametersConsensusALC.CopyToMiddleLevelCoupling(): type of MiddleLevelCoupling is not matching.{Reset}")
        
        # No copy.copy() wrapper needed - the getter methods already return defensive copies,
        # and the setter methods also create defensive copies of the input.
        if self.get_MappedResponses() is not None:
            middlelevelcouplingIn.set_MappedResponses(self.get_MappedResponses())
    
        if self.get_CouplingVariable() is not None:
            middlelevelcouplingIn.set_CouplingVariable(self.get_CouplingVariable())
        
        if self.get_SharedDesignVariables() is not None:
            middlelevelcouplingIn.set_SharedDesignVariable(self.get_SharedDesignVariables())
            
        if self.get_TargetSharedDesignVariables() is not None:
            middlelevelcouplingIn.set_TargetSharedDesignVariable(self.get_TargetSharedDesignVariables())
        
        # Update own weights in middlelevelcouplingIn
        if self.get_Weights_Auxiliary_Minus_MappedResponse() is not None:
            middlelevelcouplingIn.set_Weights_Auxiliary_Minus_MappedResponse(self.get_Weights_Auxiliary_Minus_MappedResponse())
            
        if self.get_Weights_Auxiliary_Minus_CouplingVariable() is not None:
            middlelevelcouplingIn.set_Weights_Auxiliary_Minus_CouplingVariable(self.get_Weights_Auxiliary_Minus_CouplingVariable())
            
        if self.get_Weights_Auxiliary_Minus_SharedDesignVariable() is not None:
            middlelevelcouplingIn.set_Weights_Auxiliary_Minus_SharedDesignVariable(self.get_Weights_Auxiliary_Minus_SharedDesignVariable())
        
        if self.get_Weights_Auxiliary_Minus_TargetSharedDesignVariable() is not None:
            middlelevelcouplingIn.set_Weights_Auxiliary_Minus_TargetSharedDesignVariable(self.get_Weights_Auxiliary_Minus_TargetSharedDesignVariable())
        
        # Update own multipliers in middlelevelcouplingIn
        
        if self.get_Multipliers_Auxiliary_Minus_MappedResponse() is not None:
            middlelevelcouplingIn.set_Multipliers_Auxiliary_Minus_MappedResponse(self.get_Multipliers_Auxiliary_Minus_MappedResponse())
        
        if self.get_Multipliers_Auxiliary_Minus_CouplingVariable() is not None:
            middlelevelcouplingIn.set_Multipliers_Auxiliary_Minus_CouplingVariable(self.get_Multipliers_Auxiliary_Minus_CouplingVariable())
            
        if self.get_Multipliers_Auxiliary_Minus_SharedDesignVariable() is not None:
            middlelevelcouplingIn.set_Multipliers_Auxiliary_Minus_SharedDesignVariable(self.get_Multipliers_Auxiliary_Minus_SharedDesignVariable())
            
        if self.get_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable() is not None:    
            middlelevelcouplingIn.set_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable(self.get_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable())
    
    def update_state(self, other_coupling: 'CouplingParametersConsensusALC') -> None:
        """Update the state of this CouplingParametersConsensusALC with values from another instance.

        This method is necessary for multiprocessing. When subsystems are executed in parallel
        using multiprocessing.Pool, they are serialized and deserialized, creating new objects
        in separate memory spaces. After parallel execution completes, this method updates
        the original object's attribute values while preserving their memory addresses.

        The update preserves memory addresses by modifying list contents in-place rather than
        reassigning references. This is essential for maintaining object identity across the
        multiprocessing boundary.

        Args:
            other_coupling: The source CouplingParametersConsensusALC containing updated values
                from parallel execution.
        """
        # Call the base class update_state to handle inherited attributes
        super().update_state(other_coupling=other_coupling)

        # Update all List[float] | None attributes using update_state_listprimitive
        
        # Auxiliary variables from consensus constraints
        self._auxiliary_mappedresponse: List[float] | None = update_state_listprimitive(self._auxiliary_mappedresponse, other_coupling.get_Auxiliary_MappedResponse())
        self._auxiliary_couplingvariable: List[float] | None = update_state_listprimitive(self._auxiliary_couplingvariable, other_coupling.get_Auxiliary_CouplingVariable())
        self._auxiliary_shareddesignvariable: List[float] | None = update_state_listprimitive(self._auxiliary_shareddesignvariable, other_coupling.get_Auxiliary_SharedDesignVariable())
        self._auxiliary_targetshareddesignvariable: List[float] | None = update_state_listprimitive(self._auxiliary_targetshareddesignvariable, other_coupling.get_Auxiliary_TargetSharedDesignVariable())

        # Weights for auxiliary consensus constraints (own subsystem)
        self._weights_auxiliary_minus_mappedresponse: List[float] | None = update_state_listprimitive(self._weights_auxiliary_minus_mappedresponse, other_coupling.get_Weights_Auxiliary_Minus_MappedResponse())
        self._weights_auxiliary_minus_couplingvariable: List[float] | None = update_state_listprimitive(self._weights_auxiliary_minus_couplingvariable, other_coupling.get_Weights_Auxiliary_Minus_CouplingVariable())
        self._weights_auxiliary_minus_shareddesignvariable: List[float] | None = update_state_listprimitive(self._weights_auxiliary_minus_shareddesignvariable, other_coupling.get_Weights_Auxiliary_Minus_SharedDesignVariable())
        self._weights_auxiliary_minus_targetshareddesignvariable: List[float] | None = update_state_listprimitive(self._weights_auxiliary_minus_targetshareddesignvariable, other_coupling.get_Weights_Auxiliary_Minus_TargetSharedDesignVariable())

        # Multipliers for auxiliary consensus constraints (own subsystem)
        self._multipliers_auxiliary_minus_mappedresponse: List[float] | None = update_state_listprimitive(self._multipliers_auxiliary_minus_mappedresponse, other_coupling.get_Multipliers_Auxiliary_Minus_MappedResponse())
        self._multipliers_auxiliary_minus_couplingvariable: List[float] | None = update_state_listprimitive(self._multipliers_auxiliary_minus_couplingvariable, other_coupling.get_Multipliers_Auxiliary_Minus_CouplingVariable())
        self._multipliers_auxiliary_minus_shareddesignvariable: List[float] | None = update_state_listprimitive(self._multipliers_auxiliary_minus_shareddesignvariable, other_coupling.get_Multipliers_Auxiliary_Minus_SharedDesignVariable())
        self._multipliers_auxiliary_minus_targetshareddesignvariable: List[float] | None = update_state_listprimitive(self._multipliers_auxiliary_minus_targetshareddesignvariable, other_coupling.get_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable())

        # Weights with respect to consensus constraints of neighbors
        self._copy_weights_auxiliary_minus_mappedresponse: List[float] | None = update_state_listprimitive(self._copy_weights_auxiliary_minus_mappedresponse, other_coupling.get_Copy_Weights_Auxiliary_Minus_MappedResponse())
        self._copy_weights_auxiliary_minus_couplingvariable: List[float] | None = update_state_listprimitive(self._copy_weights_auxiliary_minus_couplingvariable, other_coupling.get_Copy_Weights_Auxiliary_Minus_CouplingVariable())
        self._copy_weights_auxiliary_minus_shareddesignvariable: List[float] | None = update_state_listprimitive(self._copy_weights_auxiliary_minus_shareddesignvariable, other_coupling.get_Copy_Weights_Auxiliary_Minus_SharedDesignVariable())
        self._copy_weights_auxiliary_minus_targetshareddesignvariable: List[float] | None = update_state_listprimitive(self._copy_weights_auxiliary_minus_targetshareddesignvariable, other_coupling.get_Copy_Weights_Auxiliary_Minus_TargetSharedDesignVariable())

        # Multipliers with respect to consensus constraints of neighbors
        self._copy_multipliers_auxiliary_minus_mappedresponse: List[float] | None = update_state_listprimitive(self._copy_multipliers_auxiliary_minus_mappedresponse, other_coupling.get_Copy_Multipliers_Auxiliary_Minus_MappedResponse())
        self._copy_multipliers_auxiliary_minus_couplingvariable: List[float] | None = update_state_listprimitive(self._copy_multipliers_auxiliary_minus_couplingvariable, other_coupling.get_Copy_Multipliers_Auxiliary_Minus_CouplingVariable())
        self._copy_multipliers_auxiliary_minus_shareddesignvariable: List[float] | None = update_state_listprimitive(self._copy_multipliers_auxiliary_minus_shareddesignvariable, other_coupling.get_Copy_Multipliers_Auxiliary_Minus_SharedDesignVariable())
        self._copy_multipliers_auxiliary_minus_targetshareddesignvariable: List[float] | None = update_state_listprimitive(self._copy_multipliers_auxiliary_minus_targetshareddesignvariable, other_coupling.get_Copy_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable())
