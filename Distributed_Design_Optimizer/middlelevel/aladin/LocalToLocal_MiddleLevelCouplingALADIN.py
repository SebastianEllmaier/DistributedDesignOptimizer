# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Local-to-local middle-level coupling module for ALADIN.

This module provides middle-level coupling management for local-to-local
subsystem communication in ALADIN coordination.
"""

import copy
from typing import List
from Distributed_Design_Optimizer.middlelevel import SubSysMiddleLevelCouplingBasis
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive


class LocalToLocal_MiddleLevelCouplingALADIN(SubSysMiddleLevelCouplingBasis):
    """Middle-level coupling for local-to-local communication in ALADIN.

    Handles coupling data between two local subsystems for the ALADIN
    coordination method.
    """

    def __init__(self, id: str) -> None:
        """Initialize local-to-local middle-level coupling.

        Args:
            id: Identifier of the neighboring subsystem.
        """
        # call __init__() of MiddleLevelCouplingBasis
        super().__init__(id)
        
        # d_hat quantities: coupling quantities evaluated at the controller-proposed d_hat
        self._mappedresponses_d_hat: List[float] | None = None
        self._couplingvariable_d_hat: List[float] | None = None
        self._shareddesignvariable_d_hat: List[float] | None = None
        self._targetshareddesignvariable_d_hat: List[float] | None = None
    
    def set_MappedResponses_D_Hat(self, varin: List[float]) -> None:
        """Set mapped response variables evaluated at d_hat.

        Args:
            varin: Mapped response values evaluated at d_hat.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._mappedresponses_d_hat = copy.copy(varin)

    def get_MappedResponses_D_Hat(self) -> List[float] | None:
        """Get mapped response variables evaluated at d_hat.

        Returns:
            Mapped response values evaluated at d_hat, or None.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._mappedresponses_d_hat)

    def set_CouplingVariable_D_Hat(self, couplingvariable_d_hat_in: List[float]) -> None:
        """Set coupling variable evaluated at d_hat.

        Args:
            couplingvariable_d_hat_in: Coupling variable values evaluated at d_hat.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._couplingvariable_d_hat = copy.copy(couplingvariable_d_hat_in)

    def get_CouplingVariable_D_Hat(self) -> List[float] | None:
        """Get coupling variable evaluated at d_hat.

        Returns:
            Coupling variable values evaluated at d_hat, or None.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._couplingvariable_d_hat)

    def set_SharedDesignVariable_D_Hat(self, variablesin: List[float]) -> None:
        """Set shared design variables evaluated at d_hat.

        Args:
            variablesin: Shared design variable values evaluated at d_hat.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._shareddesignvariable_d_hat = copy.copy(variablesin)

    def get_SharedDesignVariable_D_Hat(self) -> List[float] | None:
        """Get shared design variables evaluated at d_hat.

        Returns:
            Shared design variable values evaluated at d_hat, or None.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._shareddesignvariable_d_hat)

    def set_TargetSharedDesignVariable_D_Hat(self, variablesin: List[float]) -> None:
        """Set target shared design variables evaluated at d_hat.

        Args:
            variablesin: Target shared design variable values evaluated at d_hat.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._targetshareddesignvariable_d_hat = copy.copy(variablesin)

    def get_TargetSharedDesignVariable_D_Hat(self) -> List[float] | None:
        """Get target shared design variables evaluated at d_hat.

        Returns:
            Target shared design variable values evaluated at d_hat, or None.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._targetshareddesignvariable_d_hat)
    
    def update_state(self, other_middlelevelcoupling: 'LocalToLocal_MiddleLevelCouplingALADIN') -> None:
        """Update the state of this LocalToLocal_MiddleLevelCouplingALADIN with another instance.
        
        This method updates the numerical information stored in the class's attributes
        without changing the original memory address location. This is necessary for
        multiprocessing, where executed subsystems return from separate processes and
        their state must be transferred back to the original objects in the main process.
        
        Args:
            other_middlelevelcoupling: The source instance to copy state from.
        """
        # Call the base class update_state to handle all base attributes
        super().update_state(other_middlelevelcoupling)
        
        self._mappedresponses_d_hat = update_state_listprimitive(self._mappedresponses_d_hat, other_middlelevelcoupling.get_MappedResponses_D_Hat())
        self._couplingvariable_d_hat = update_state_listprimitive(self._couplingvariable_d_hat, other_middlelevelcoupling.get_CouplingVariable_D_Hat())
        self._shareddesignvariable_d_hat = update_state_listprimitive(self._shareddesignvariable_d_hat, other_middlelevelcoupling.get_SharedDesignVariable_D_Hat())
        self._targetshareddesignvariable_d_hat = update_state_listprimitive(self._targetshareddesignvariable_d_hat, other_middlelevelcoupling.get_TargetSharedDesignVariable_D_Hat())
