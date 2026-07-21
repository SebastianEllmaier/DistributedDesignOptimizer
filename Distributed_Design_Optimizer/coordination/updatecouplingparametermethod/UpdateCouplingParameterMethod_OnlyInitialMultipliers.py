# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Initial-multiplier-only coupling parameter update method.

This module implements an update strategy that performs no multiplier or
weight updates and only provides the initial Lagrange multiplier value.
Used by subsystems (e.g. SBDP) that recover the coordination multipliers
themselves (e.g. from the KKT system) but still need a seed value for the
initial multipliers.
"""

from typing import List
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print, ddo_print_border
from Distributed_Design_Optimizer.coordination.updatecouplingparametermethod.UpdateCouplingParameterMethodInterface import UpdateCouplingParameterMethodInterface


class UpdateCouplingParameterMethod_OnlyInitialMultipliers(UpdateCouplingParameterMethodInterface):
    """Update method that only provides the initial Lagrange multiplier value.

    All update and weight operations are no-ops; only get_InitialMultiplier
    returns a meaningful value. Intended for coordination methods that manage
    the coordination multipliers externally but require a seed value.

    Attributes:
        _initialmultiplier: Initial value for Lagrange multipliers.
    """

    def __init__(self,
                 initialmultiplier: float) -> None:
        """Initialize the initial-multiplier-only update method.

        Args:
            initialmultiplier: Initial value for Lagrange multipliers.
        """
        # Hyperparameter Validation Bounds:

        # initialmultiplier: can be anything, should be 0
        self._initialmultiplier_allowed_min: float = float('-inf')     # strict (>), inf bounds are always exclusive
        self._initialmultiplier_allowed_max: float = float('inf')      # strict (<), inf bounds are always exclusive
        self._initialmultiplier_rec_min: float = 0.0                   # inclusive (>=)
        self._initialmultiplier_rec_max: float = 0.0                   # inclusive (<=)

        # Set inputs
        self._initialmultiplier: float = initialmultiplier

        # Validate inputs
        self.validate_inputs()

    def validate_inputs(self) -> None:
        """Validate the hyperparameters of this update method.

        Raises:
            ValueError: If any parameter is outside the allowed range.
        """
        # ===== initialmultiplier Validation =====
        # Allowed: all values, Recommended: 0
        if not (self._initialmultiplier_rec_min <= self._initialmultiplier <= self._initialmultiplier_rec_max):
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: initialmultiplier={self._initialmultiplier} is not the recommended value "
                      f"({self._initialmultiplier_rec_min}).")
            ddo_print_border()

    def update_CoordinationMultipliers(self,
                                       multiplierin: List[float],
                                       inconsistencyin: List[float]) -> None:
        """No-op: does not update multipliers.

        Args:
            multiplierin: Current multiplier values.
            inconsistencyin: Current inconsistency values.
        """
        pass

    def update_CoordinationWeights(self,
                                   weightin: List[float],
                                   inconsistencyIn: List[float],
                                   inconsistencyOldIn: List[float] | None) -> None:
        """No-op: does not update weights.

        Args:
            weightin: Current penalty weights.
            inconsistencyIn: Current inconsistency values.
            inconsistencyOldIn: Previous inconsistency values, or None.
        """
        pass

    def get_InitialWeight(self) -> float:
        """No-op: this method does not provide an initial weight.

        Returns:
            ``None``; this no-op method does not provide an initial weight.
        """
        pass

    def get_InitialMultiplier(self) -> float:
        """Get the initial Lagrange multiplier value.

        Returns:
            The initial Lagrange multiplier value.
        """
        return self._initialmultiplier

    def print_startup_summary(self) -> None:
        """Print the initial multiplier value at startup."""
        name = f"{type(self).__name__}:"
        ddo_print(f"{name}     initialmultiplier:   {self._initialmultiplier}", indent=1)

    def print_termination_summary(self) -> None:
        """Print the initial multiplier value at the end."""
        name = f"{type(self).__name__}:"
        ddo_print(f"{name}     initialmultiplier:   {self._initialmultiplier}", indent=1)

    def update_state(self, other: 'UpdateCouplingParameterMethod_OnlyInitialMultipliers') -> None:
        """Update the state of this instance with values from another instance.

        Args:
            other: The source instance containing updated values from parallel execution.
        """
        # No copy.copy() needed - float is a primitive/immutable type
        self._initialmultiplier = other._initialmultiplier
