---
title: CouplingParametersSBDP (Source)
---

← Back to [CouplingParametersSBDP documentation](CouplingParametersSBDP.md)

# CouplingParametersSBDP - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\couplingparameters\sbdp\CouplingParametersSBDP.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""SBDP coupling parameters module.

This module provides coupling parameters for the Sensitivity Based Distributed
Programming (SBDP) method.

In SBDP each subsystem imposes a hard coordination equality constraint made of
two blocks:

    [ H(r) - h ; S_z d - z ] = 0   | lambda

where the first (mapped-response) block carries the multiplier ``lambda_h`` and
the second (shared-design-variable) block carries the multiplier ``lambda_z``.
These multipliers are computed locally (KKT) and communicated to the neighboring
subsystem via the middle level, where they are stored as the neighbor's
``copy_multipliers``. The neighbor then uses them to build the sensitivity term
of its own subproblem objective.
"""

import copy
from typing import List
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive
from Distributed_Design_Optimizer.subsystem.couplingparameters import SubSysCouplingParametersBasis
from Distributed_Design_Optimizer.middlelevel.sbdp import MiddleLevelCouplingSBDP


class CouplingParametersSBDP(SubSysCouplingParametersBasis):
    """Coupling parameters for Sensitivity Based Distributed Programming.

    Extends SubSysCouplingParametersBasis with the Lagrange multipliers of the
    coordination equality constraint blocks (own multipliers) and the copies of
    the neighbor's multipliers pulled from the middle level.
    """

    def __init__(self, id: str) -> None:
        """Initialize CouplingParametersSBDP.

        Args:
            id: Identifier of the neighboring subsystem.
        """
        super().__init__(id)

        # Own multipliers of the coordination equality constraint blocks:
        #   lambda_h -> mapped-response block ( H(r) - h )
        #   lambda_z -> shared-design-variable block ( S_z d - z )
        self._multipliers_mappedresponse_minus_copycouplingvariable: List[float] | None = None
        self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable: List[float] | None = None

        # Copies of the neighbor's multipliers, communicated via the middle level.
        # These are used to construct the sensitivity term of the local objective.
        self._copy_multipliers_mappedresponse_minus_copycouplingvariable: List[float] | None = None
        self._copy_multipliers_shareddesignvariable_minus_copytargetshareddesignvariable: List[float] | None = None

        # This neighbor's contribution grad_d^j L^(k) to the coordination objective's linear
        # sensitivity term, scattered into the subsystem's design-variable space. Computed once
        # per outer iteration in LocalSubSystemSBDP.prepare_OptimizationProblem() and summed
        # over neighbors to form the full sensitivity gradient sum_j grad_d^j L^(k).
        self._sensitivity_gradient: List[float] | None = None

    # ------------------------------------------------------------------ #
    # Own multipliers
    # ------------------------------------------------------------------ #

    def set_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self, multipliersin: List[float]) -> None:
        """Set the own multipliers of the mapped-response coordination equality block.

        Args:
            multipliersin: Lagrange multipliers of the mapped-response block.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_mappedresponse_minus_copycouplingvariable = copy.copy(multipliersin)

    def get_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self) -> List[float] | None:
        """Return the own multipliers of the mapped-response coordination equality block.

        Returns:
            Lagrange multipliers of the mapped-response block, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_mappedresponse_minus_copycouplingvariable)

    def set_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, multipliersin: List[float]) -> None:
        """Set the own multipliers of the shared-design-variable coordination equality block.

        Args:
            multipliersin: Lagrange multipliers of the shared-design-variable block.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable = copy.copy(multipliersin)

    def get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self) -> List[float] | None:
        """Return the own multipliers of the shared-design-variable coordination equality block.

        Returns:
            Lagrange multipliers of the shared-design-variable block, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable)

    # ------------------------------------------------------------------ #
    # Copies of the neighbor's multipliers (from the middle level)
    # ------------------------------------------------------------------ #

    def set_Copy_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self, multipliersin: List[float]) -> None:
        """Set the copy of the neighbor's mapped-response block multipliers.

        Args:
            multipliersin: Neighbor's Lagrange multipliers of the mapped-response block.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_multipliers_mappedresponse_minus_copycouplingvariable = copy.copy(multipliersin)

    def get_Copy_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self) -> List[float] | None:
        """Return the copy of the neighbor's mapped-response block multipliers.

        Returns:
            Neighbor's mapped-response block multipliers, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_multipliers_mappedresponse_minus_copycouplingvariable)

    def set_Copy_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, multipliersin: List[float]) -> None:
        """Set the copy of the neighbor's shared-design-variable block multipliers.

        Args:
            multipliersin: Neighbor's Lagrange multipliers of the shared-design-variable block.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._copy_multipliers_shareddesignvariable_minus_copytargetshareddesignvariable = copy.copy(multipliersin)

    def get_Copy_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self) -> List[float] | None:
        """Return the copy of the neighbor's shared-design-variable block multipliers.

        Returns:
            Neighbor's shared-design-variable block multipliers, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._copy_multipliers_shareddesignvariable_minus_copytargetshareddesignvariable)

    # ------------------------------------------------------------------ #
    # Sensitivity gradient contribution of this neighbor
    # ------------------------------------------------------------------ #

    def set_Sensitivity_Gradient(self, sensitivity_gradient_in: List[float]) -> None:
        """Set this neighbor's contribution to the coordination-objective sensitivity gradient.

        Args:
            sensitivity_gradient_in: Sensitivity gradient grad_d^j L^(k) scattered into the
                subsystem's design-variable space.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._sensitivity_gradient = copy.copy(sensitivity_gradient_in)

    def get_Sensitivity_Gradient(self) -> List[float] | None:
        """Return this neighbor's contribution to the coordination-objective sensitivity gradient.

        Returns:
            Sensitivity gradient grad_d^j L^(k) scattered into the subsystem's
            design-variable space, or None if not set.
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._sensitivity_gradient)

    # ------------------------------------------------------------------ #
    # Middle-level exchange
    # ------------------------------------------------------------------ #

    def CopyFromMiddleLevelCoupling(self, middlelevelcouplingIn: MiddleLevelCouplingSBDP) -> None:
        """Copy coupling data from a MiddleLevelCoupling object.

        Args:
            middlelevelcouplingIn: The MiddleLevelCoupling object to copy data from.

        Raises:
            ValueError: If middlelevelcouplingIn is not a MiddleLevelCouplingSBDP instance.
        """
        if not isinstance(middlelevelcouplingIn, MiddleLevelCouplingSBDP):
            raise ValueError(f"{DDO_Color}Error in CouplingParametersSBDP.CopyFromMiddleLevelCoupling(): type of MiddleLevelCoupling is not matching.{Reset}")

        if middlelevelcouplingIn.get_MappedResponses() is not None:
            self.set_Copy_MappedResponses(middlelevelcouplingIn.get_MappedResponses())

        if middlelevelcouplingIn.get_CouplingVariable() is not None:
            self.set_Copy_CouplingVariable(middlelevelcouplingIn.get_CouplingVariable())

        if middlelevelcouplingIn.get_SharedDesignVariable() is not None:
            self.set_Copy_SharedDesignVariables(middlelevelcouplingIn.get_SharedDesignVariable())

        if middlelevelcouplingIn.get_TargetSharedDesignVariable() is not None:
            self.set_Copy_TargetSharedDesignVariables(middlelevelcouplingIn.get_TargetSharedDesignVariable())

        # Pull the neighbor's coordination equality multipliers into the copy fields
        if middlelevelcouplingIn.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable() is not None:
            self.set_Copy_Multipliers_MappedResponse_Minus_CopyCouplingVariable(middlelevelcouplingIn.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable())

        if middlelevelcouplingIn.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable() is not None:
            self.set_Copy_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(middlelevelcouplingIn.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())

    def CopyToMiddleLevelCoupling(self, middlelevelcouplingIn: MiddleLevelCouplingSBDP) -> None:
        """Copy coupling data to a MiddleLevelCoupling object.

        Args:
            middlelevelcouplingIn: The MiddleLevelCoupling object to copy data to.

        Raises:
            ValueError: If middlelevelcouplingIn is not a MiddleLevelCouplingSBDP instance.
        """
        if not isinstance(middlelevelcouplingIn, MiddleLevelCouplingSBDP):
            raise ValueError(f"{DDO_Color}Error in CouplingParametersSBDP.CopyToMiddleLevelCoupling(): type of MiddleLevelCoupling is not matching.{Reset}")

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

        # Publish the own coordination equality multipliers to the middle level
        if self.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable() is not None:
            middlelevelcouplingIn.set_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable())

        if self.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable() is not None:
            middlelevelcouplingIn.set_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())

    def update_state(self, other_coupling: 'CouplingParametersSBDP') -> None:
        """Update the state of this CouplingParametersSBDP with values from another instance.

        This method is necessary for multiprocessing. When subsystems are executed in parallel
        using multiprocessing.Pool, they are serialized and deserialized, creating new objects
        in separate memory spaces. After parallel execution completes, this method updates
        the original object's attribute values while preserving their memory addresses.

        The update preserves memory addresses by modifying list contents in-place rather than
        reassigning references. This is essential for maintaining object identity across the
        multiprocessing boundary.

        Args:
            other_coupling: The source CouplingParametersSBDP containing updated values
                from parallel execution.
        """
        # Call the base class update_state to handle inherited attributes
        super().update_state(other_coupling=other_coupling)

        # Update all List[float] | None attributes using update_state_listprimitive
        self._multipliers_mappedresponse_minus_copycouplingvariable: List[float] | None = update_state_listprimitive(
            self._multipliers_mappedresponse_minus_copycouplingvariable, other_coupling.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable())
        self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable: List[float] | None = update_state_listprimitive(
            self._multipliers_shareddesignvariable_minus_copytargetshareddesignvariable, other_coupling.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
        self._copy_multipliers_mappedresponse_minus_copycouplingvariable: List[float] | None = update_state_listprimitive(
            self._copy_multipliers_mappedresponse_minus_copycouplingvariable, other_coupling.get_Copy_Multipliers_MappedResponse_Minus_CopyCouplingVariable())
        self._copy_multipliers_shareddesignvariable_minus_copytargetshareddesignvariable: List[float] | None = update_state_listprimitive(
            self._copy_multipliers_shareddesignvariable_minus_copytargetshareddesignvariable, other_coupling.get_Copy_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
        self._sensitivity_gradient: List[float] | None = update_state_listprimitive(
            self._sensitivity_gradient, other_coupling.get_Sensitivity_Gradient())

```
