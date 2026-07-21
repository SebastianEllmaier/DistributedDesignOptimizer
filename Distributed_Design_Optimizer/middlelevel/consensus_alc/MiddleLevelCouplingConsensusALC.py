# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Middle-level coupling for consensus-based ALC.

This module provides middle-level coupling management for
consensus-based Augmented Lagrangian Coordination.
"""

import copy
from typing import List
from Distributed_Design_Optimizer.middlelevel import SubSysMiddleLevelCouplingBasis
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive


class MiddleLevelCouplingConsensusALC(SubSysMiddleLevelCouplingBasis):
    """Middle-level coupling for consensus-based ALC.

    Handles coupling data between subsystems for consensus-based
    Augmented Lagrangian Coordination.
    """

    def __init__(self, id: str) -> None:
        """Initialize middle-level coupling.

        Args:
            id: Identifier of the neighboring subsystem.
        """
        # call __init__() of MiddleLevelCouplingBasis
        super().__init__(id)
        
        # Weights
        self._weights_auxiliary_minus_mappedresponse: List[float] | None = None
        self._weights_auxiliary_minus_couplingvariable: List[float] | None = None
        self._weights_auxiliary_minus_shareddesignvariable: List[float] | None = None
        self._weights_auxiliary_minus_targetshareddesignvariable: List[float] | None = None
        
        # Lagrange multipliers
        self._multipliers_auxiliary_minus_mappedresponse: List[float] | None = None
        self._multipliers_auxiliary_minus_couplingvariable: List[float] | None = None
        self._multipliers_auxiliary_minus_shareddesignvariable: List[float] | None = None
        self._multipliers_auxiliary_minus_targetshareddesignvariable: List[float] | None = None
        
    def set_Weights_Auxiliary_Minus_MappedResponse(self, weightsin: List[float]) -> None:
        """Set the weights for the auxiliary-minus-mapped-response part of the coupling circle.

        Args:
            weightsin: Weights to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._weights_auxiliary_minus_mappedresponse = copy.copy(weightsin)
        
    def get_Weights_Auxiliary_Minus_MappedResponse(self) -> List[float] | None:
        """Return the weights for the auxiliary-minus-mapped-response part of the coupling circle.

        Returns:
            The weights or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._weights_auxiliary_minus_mappedresponse)
    
    def set_Weights_Auxiliary_Minus_CouplingVariable(self, weightsin: List[float]) -> None:
        """Set the weights for the auxiliary-minus-coupling-variable part of the coupling circle.

        Args:
            weightsin: Weights to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._weights_auxiliary_minus_couplingvariable = copy.copy(weightsin)
        
    def get_Weights_Auxiliary_Minus_CouplingVariable(self) -> List[float] | None:
        """Return the weights for the auxiliary-minus-coupling-variable part of the coupling circle.

        Returns:
            The weights or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._weights_auxiliary_minus_couplingvariable)
    
    def set_Weights_Auxiliary_Minus_SharedDesignVariable(self, weightsin: List[float]) -> None:
        """Set the weights for the auxiliary-minus-shared-design-variable part of the coupling circle.

        Args:
            weightsin: Weights to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._weights_auxiliary_minus_shareddesignvariable = copy.copy(weightsin)
        
    def get_Weights_Auxiliary_Minus_SharedDesignVariable(self) -> List[float] | None:
        """Return the weights for the auxiliary-minus-shared-design-variable part of the coupling circle.

        Returns:
            The weights or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._weights_auxiliary_minus_shareddesignvariable)
    
    def set_Weights_Auxiliary_Minus_TargetSharedDesignVariable(self, weightsin: List[float]) -> None:
        """Set the weights for the auxiliary-minus-target-shared-design-variable part of the coupling circle.

        Args:
            weightsin: Weights to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._weights_auxiliary_minus_targetshareddesignvariable = copy.copy(weightsin)
        
    def get_Weights_Auxiliary_Minus_TargetSharedDesignVariable(self) -> List[float] | None:
        """Return the weights for the auxiliary-minus-target-shared-design-variable part of the coupling circle.

        Returns:
            The weights or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._weights_auxiliary_minus_targetshareddesignvariable)
    
    # Multipliers
    def set_Multipliers_Auxiliary_Minus_MappedResponse(self, multipliersin: List[float]) -> None:
        """Set the Lagrange multipliers for the auxiliary-minus-mapped-response part of the coupling circle.

        Args:
            multipliersin: Lagrange multipliers to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_auxiliary_minus_mappedresponse = copy.copy(multipliersin)
        
    def get_Multipliers_Auxiliary_Minus_MappedResponse(self) -> List[float] | None:
        """Return the Lagrange multipliers for the auxiliary-minus-mapped-response part of the coupling circle.

        Returns:
            The Lagrange multipliers or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_auxiliary_minus_mappedresponse)
    
    def set_Multipliers_Auxiliary_Minus_CouplingVariable(self, multipliersin: List[float]) -> None:
        """Set the Lagrange multipliers for the auxiliary-minus-coupling-variable part of the coupling circle.

        Args:
            multipliersin: Lagrange multipliers to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_auxiliary_minus_couplingvariable = copy.copy(multipliersin)
        
    def get_Multipliers_Auxiliary_Minus_CouplingVariable(self) -> List[float] | None:
        """Return the Lagrange multipliers for the auxiliary-minus-coupling-variable part of the coupling circle.

        Returns:
            The Lagrange multipliers or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_auxiliary_minus_couplingvariable)
    
    def set_Multipliers_Auxiliary_Minus_SharedDesignVariable(self, multipliersin: List[float]) -> None:
        """Set the Lagrange multipliers for the auxiliary-minus-shared-design-variable part of the coupling circle.

        Args:
            multipliersin: Lagrange multipliers to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_auxiliary_minus_shareddesignvariable = copy.copy(multipliersin)
        
    def get_Multipliers_Auxiliary_Minus_SharedDesignVariable(self) -> List[float] | None:
        """Return the Lagrange multipliers for the auxiliary-minus-shared-design-variable part of the coupling circle.

        Returns:
            The Lagrange multipliers or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_auxiliary_minus_shareddesignvariable)
    
    def set_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable(self, multipliersin: List[float]) -> None:
        """Set the Lagrange multipliers for the auxiliary-minus-target-shared-design-variable part of the coupling circle.

        Args:
            multipliersin: Lagrange multipliers to set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_auxiliary_minus_targetshareddesignvariable = copy.copy(multipliersin)
        
    def get_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable(self) -> List[float] | None:
        """Return the Lagrange multipliers for the auxiliary-minus-target-shared-design-variable part of the coupling circle.

        Returns:
            The Lagrange multipliers or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_auxiliary_minus_targetshareddesignvariable)
    
    def update_state(self, other_middlelevelcoupling: 'MiddleLevelCouplingConsensusALC') -> None:
        """Update the state of this MiddleLevelCoupling with another instance.
        
        This method updates the numerical information stored in the class's attributes
        without changing the original memory address location. This is necessary for
        multiprocessing, where executed subsystems return from separate processes and
        their state must be transferred back to the original objects in the main process.
        
        Args:
            other_middlelevelcoupling: The source instance to copy state from.
        """
        # Call the base class update_state to handle common attributes
        super().update_state(other_middlelevelcoupling)
        
        self._weights_auxiliary_minus_mappedresponse: List[float] | None = update_state_listprimitive(
            self._weights_auxiliary_minus_mappedresponse, other_middlelevelcoupling.get_Weights_Auxiliary_Minus_MappedResponse())
        
        self._weights_auxiliary_minus_couplingvariable: List[float] | None = update_state_listprimitive(
            self._weights_auxiliary_minus_couplingvariable, other_middlelevelcoupling.get_Weights_Auxiliary_Minus_CouplingVariable())
        
        self._weights_auxiliary_minus_shareddesignvariable: List[float] | None = update_state_listprimitive(
            self._weights_auxiliary_minus_shareddesignvariable, other_middlelevelcoupling.get_Weights_Auxiliary_Minus_SharedDesignVariable())
        
        self._weights_auxiliary_minus_targetshareddesignvariable: List[float] | None = update_state_listprimitive(
            self._weights_auxiliary_minus_targetshareddesignvariable, other_middlelevelcoupling.get_Weights_Auxiliary_Minus_TargetSharedDesignVariable())
        
        self._multipliers_auxiliary_minus_mappedresponse: List[float] | None = update_state_listprimitive(
            self._multipliers_auxiliary_minus_mappedresponse, other_middlelevelcoupling.get_Multipliers_Auxiliary_Minus_MappedResponse())
        
        self._multipliers_auxiliary_minus_couplingvariable: List[float] | None = update_state_listprimitive(
            self._multipliers_auxiliary_minus_couplingvariable, other_middlelevelcoupling.get_Multipliers_Auxiliary_Minus_CouplingVariable())
        
        self._multipliers_auxiliary_minus_shareddesignvariable: List[float] | None = update_state_listprimitive(
            self._multipliers_auxiliary_minus_shareddesignvariable, other_middlelevelcoupling.get_Multipliers_Auxiliary_Minus_SharedDesignVariable())
        
        self._multipliers_auxiliary_minus_targetshareddesignvariable: List[float] | None = update_state_listprimitive(
            self._multipliers_auxiliary_minus_targetshareddesignvariable, other_middlelevelcoupling.get_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable())
