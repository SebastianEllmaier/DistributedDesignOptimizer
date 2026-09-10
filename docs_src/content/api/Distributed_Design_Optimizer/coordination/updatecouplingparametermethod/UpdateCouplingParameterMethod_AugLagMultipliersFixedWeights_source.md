---
title: UpdateCouplingParameterMethod_AugLagMultipliersFixedWeights (Source)
---

← Back to [UpdateCouplingParameterMethod_AugLagMultipliersFixedWeights documentation](UpdateCouplingParameterMethod_AugLagMultipliersFixedWeights.md)

# UpdateCouplingParameterMethod_AugLagMultipliersFixedWeights - Source Code

**File:** `Distributed_Design_Optimizer\coordination\updatecouplingparametermethod\UpdateCouplingParameterMethod_AugLagMultipliersFixedWeights.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""ALADIN coupling parameter update method.

This module implements the ALADIN update strategy for Lagrange multipliers.
ALADIN updates multipliers using the same augmented Lagrangian rule as ALC,
but does not update penalty weights.
"""

from typing import List
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print, ddo_print_border
from Distributed_Design_Optimizer.coordination.updatecouplingparametermethod.UpdateCouplingParameterMethodInterface import UpdateCouplingParameterMethodInterface


class UpdateCouplingParameterMethod_AugLagMultipliersFixedWeights(UpdateCouplingParameterMethodInterface):
    """ALADIN update method for coupling parameters.

    Implements the ALADIN multiplier update rule:
    - Multipliers: λ_new = λ_old + 2 * w² * c(x)
    - Weights: no update (ALADIN does not modify penalty weights)

    Attributes:
        _initialweight: Initial value for penalty weights (must be >= 0).
        _initialmultiplier: Initial value for Lagrange multipliers.
    """

    def __init__(self,
                 initialweight: float,
                 initialmultiplier: float) -> None:
        """Initialize the ALADIN update method.

        Args:
            initialweight: Initial value for penalty weights.
            initialmultiplier: Initial value for Lagrange multipliers.
        """
        # Hyperparameter Validation Bounds:

        # initialweight: must be >= 0, should be in (0, 0.1]
        self._initialweight_allowed_min: float = 0.0                   # inclusive (>=)
        self._initialweight_allowed_max: float = float('inf')          # strict (<), inf bounds are always exclusive
        self._initialweight_rec_min: float = 0.0                       # strict (>)
        self._initialweight_rec_max: float = 0.1                       # inclusive (<=)

        # initialmultiplier: can be anything, should be 0
        self._initialmultiplier_allowed_min: float = float('-inf')     # strict (>), inf bounds are always exclusive
        self._initialmultiplier_allowed_max: float = float('inf')      # strict (<), inf bounds are always exclusive
        self._initialmultiplier_rec_min: float = 0.0                   # inclusive (>=)
        self._initialmultiplier_rec_max: float = 0.0                   # inclusive (<=)

        # Set inputs
        self._initialweight: float = initialweight
        self._initialmultiplier: float = initialmultiplier

        # Validate inputs
        self.validate_inputs()

    def validate_inputs(self) -> None:
        """Validate the hyperparameters of this update method.

        Raises:
            ValueError: If any parameter is outside the allowed range.
        """
        # ===== initialweight Validation =====
        # Allowed: >= 0 (inclusive), Recommended: (0, 0.1] (strict left, inclusive right)
        if not (self._initialweight_allowed_min <= self._initialweight < self._initialweight_allowed_max):
            raise ValueError(
                f"{DDO_Color}initialweight must be in [{self._initialweight_allowed_min}, {self._initialweight_allowed_max}), but got {self._initialweight}.{Reset}"
            )
        elif not (self._initialweight_rec_min < self._initialweight <= self._initialweight_rec_max):
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: initialweight={self._initialweight} is outside the recommended range "
                      f"({self._initialweight_rec_min}, {self._initialweight_rec_max}].")
            ddo_print_border()

        # ===== initialmultiplier Validation =====
        # Allowed: all values, Recommended: 0
        if not (self._initialmultiplier_rec_min <= self._initialmultiplier <= self._initialmultiplier_rec_max):
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: initialmultiplier={self._initialmultiplier} is not the recommended value "
                      f"({self._initialmultiplier_rec_min}).")
            ddo_print_border()

    def update_CoordinationMultipliers(self,
                                       multiplierin: List[float],
                                       weightsin: List[float],
                                       inconsistencyin: List[float]) -> None:
        """Update Lagrange multipliers using the augmented Lagrangian rule.

        Update formula: λ_new = λ_old + 2 * w² * c(x)

        Args:
            multiplierin: Current multiplier values to update in place.
            weightsin: Current penalty weight values.
            inconsistencyin: Current inconsistency values.
        """
        for i in range(len(multiplierin)):
            multiplierin[i] = multiplierin[i] + 2 * weightsin[i] * weightsin[i] * inconsistencyin[i]

    def update_CoordinationWeights(self,
                                   weightin: List[float],
                                   inconsistencyIn: List[float],
                                   inconsistencyOldIn: List[float] | None) -> None:
        """No-op: ALADIN does not update penalty weights.

        Args:
            weightin: Current penalty weights.
            inconsistencyIn: Current inconsistency values.
            inconsistencyOldIn: Previous inconsistency values, or None.
        """
        # ALADIN does not update penalty weights
        pass

    def get_InitialWeight(self) -> float:
        """Get the initial penalty weight value.

        Returns:
            The initial penalty weight value.
        """
        return self._initialweight

    def get_InitialMultiplier(self) -> float:
        """Get the initial Lagrange multiplier value.

        Returns:
            The initial Lagrange multiplier value.
        """
        return self._initialmultiplier
    
    def print_startup_summary(self) -> None:
        """Print the fixed weight and initial multiplier values at startup."""
        name = f"{type(self).__name__}:"
        pad = " " * len(name)
        ddo_print(f"{name}     initialweight:       {self._initialweight}", indent=1)
        ddo_print(f"{pad}     initialmultiplier:   {self._initialmultiplier}", indent=1)

    def print_termination_summary(self) -> None:
        """Print the fixed weight and initial multiplier values at the end."""
        name = f"{type(self).__name__}:"
        pad = " " * len(name)
        ddo_print(f"{name}     initialweight:       {self._initialweight}", indent=1)
        ddo_print(f"{pad}     initialmultiplier:   {self._initialmultiplier}", indent=1)

    def update_state(self, other: 'UpdateCouplingParameterMethod_AugLagMultipliersFixedWeights') -> None:
        """Update the state of this instance with values from another instance.

        Args:
            other: The source instance containing updated values from parallel execution.
        """
        # No copy.copy() needed - float is a primitive/immutable type
        self._initialweight = other._initialweight
        self._initialmultiplier = other._initialmultiplier

```
