# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Middle-level coupling for Sensitivity Based Distributed Programming (SBDP).

This module provides middle-level coupling management for SBDP. In addition to
the base coupling quantities, it stores the Lagrange multipliers of the
coordination (hard) equality constraints so that they can be communicated to
the neighboring subsystem via the middle level.
"""

import copy
from typing import List
from Distributed_Design_Optimizer.middlelevel import SubSysMiddleLevelCouplingBasis
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive


class MiddleLevelCouplingSBDP(SubSysMiddleLevelCouplingBasis):
    """Middle-level coupling for SBDP.

    Handles coupling data between subsystems for Sensitivity Based Distributed
    Programming, including the Lagrange multipliers of the coordination
    equality constraints (mapped-response and shared-design-variable blocks).
    """

    def __init__(self, id: str) -> None:
        """Initialize middle-level coupling.

        Args:
            id: Identifier of the neighboring subsystem.
        """
        # call __init__() of MiddleLevelCouplingBasis
        super().__init__(id)

        # Lagrange multipliers of the coordination equality constraint blocks
        self._multipliers_mappedresponse_minus_copycouplingvariable: List[float] | None = None
        self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable: List[float] | None = None

    def set_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self, multipliersin: List[float]) -> None:
        """Set the multipliers of the mapped-response coordination equality block.

        Args:
            multipliersin: Lagrange multipliers of the mapped-response block.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_mappedresponse_minus_copycouplingvariable = copy.copy(multipliersin)

    def get_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self) -> List[float] | None:
        """Return the multipliers of the mapped-response coordination equality block.

        Returns:
            The Lagrange multipliers or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_mappedresponse_minus_copycouplingvariable)

    def set_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, multipliersin: List[float]) -> None:
        """Set the multipliers of the shared-design-variable coordination equality block.

        Args:
            multipliersin: Lagrange multipliers of the shared-design-variable block.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable = copy.copy(multipliersin)

    def get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self) -> List[float] | None:
        """Return the multipliers of the shared-design-variable coordination equality block.

        Returns:
            The Lagrange multipliers or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable)

    def update_state(self, other_middlelevelcoupling: 'MiddleLevelCouplingSBDP') -> None:
        """Update the state of this MiddleLevelCoupling from another instance.

        This method updates the numerical information stored in the class's attributes
        without changing the original memory address location. This is necessary for
        multiprocessing, where executed subsystems return from separate processes and
        their state must be transferred back to the original objects in the main process.

        Args:
            other_middlelevelcoupling: The source instance to copy state from.
        """
        # Call the base class update_state to handle common attributes
        super().update_state(other_middlelevelcoupling)

        self._multipliers_mappedresponse_minus_copycouplingvariable: List[float] | None = update_state_listprimitive(
            self._multipliers_mappedresponse_minus_copycouplingvariable, other_middlelevelcoupling.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable())

        self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable: List[float] | None = update_state_listprimitive(
            self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable, other_middlelevelcoupling.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
