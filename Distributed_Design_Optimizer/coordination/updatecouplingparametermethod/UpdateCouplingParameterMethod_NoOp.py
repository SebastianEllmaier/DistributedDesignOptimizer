# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""No-op coupling parameter update method.

This module implements a no-op update strategy that performs no updates.
Used by subsystems that manage coupling parameters externally or do not
require parameter updates (e.g., controller subsystems).
"""

from typing import List
from Distributed_Design_Optimizer.coordination.updatecouplingparametermethod.UpdateCouplingParameterMethodInterface import UpdateCouplingParameterMethodInterface


class UpdateCouplingParameterMethod_NoOp(UpdateCouplingParameterMethodInterface):
    """No-op update method that performs no coupling parameter updates.

    Used as a placeholder for subsystems that do not update coupling
    parameters through the standard strategy interface.
    """

    def __init__(self) -> None:
        """Initialize the no-op update method."""
        pass

    def validate_inputs(self) -> None:
        """No-op: no parameters to validate."""
        pass

    def update_CoordinationMultipliers(self,
                                       multiplierin: List[float],
                                       weightsin: List[float],
                                       inconsistencyin: List[float]) -> None:
        """No-op: does not update multipliers.

        Args:
            multiplierin: Current multiplier values.
            weightsin: Current weight values.
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
        """No-op: this method does not provide an initial multiplier.

        Returns:
            ``None``; this no-op method does not provide an initial multiplier.
        """
        pass
    
    def print_startup_summary(self) -> None:
        """Nothing to print."""
        pass

    def print_termination_summary(self) -> None:
        """Nothing to print."""
        pass

    def update_state(self, other: 'UpdateCouplingParameterMethod_NoOp') -> None:
        """No-op: no state to update.

        Args:
            other: The source instance (ignored).
        """
        pass
