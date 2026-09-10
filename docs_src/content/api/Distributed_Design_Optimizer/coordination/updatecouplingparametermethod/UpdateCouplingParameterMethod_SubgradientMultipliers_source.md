---
title: UpdateCouplingParameterMethod_SubgradientMultipliers (Source)
---

← Back to [UpdateCouplingParameterMethod_SubgradientMultipliers documentation](UpdateCouplingParameterMethod_SubgradientMultipliers.md)

# UpdateCouplingParameterMethod_SubgradientMultipliers - Source Code

**File:** `Distributed_Design_Optimizer\coordination\updatecouplingparametermethod\UpdateCouplingParameterMethod_SubgradientMultipliers.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Standard LC coupling parameter update method.

This module implements the standard Lagrangian Coordination
update strategy for Lagrange multipliers (without penalty weights).
"""

from typing import List
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print, ddo_print_border
from Distributed_Design_Optimizer.coordination.updatecouplingparametermethod.UpdateCouplingParameterMethodInterface import UpdateCouplingParameterMethodInterface


class UpdateCouplingParameterMethod_SubgradientMultipliers(UpdateCouplingParameterMethodInterface):
    """Standard LC update method for coupling parameters.

    Implements the Lagrangian coordination update rules (without penalty weights):
    - Multipliers: λ_new = λ_old + beta * inconsistency

    Note: gamma is not used in LC since there are no penalty weights to update.

    Attributes:
        _beta: Multiplier update step size (must be > 0).
        _initialmultiplier: Initial value for Lagrange multipliers.
    """

    def __init__(self,
                 beta: float,
                 initialmultiplier: float) -> None:
        """Initialize the standard LC update method.

        Args:
            beta: Multiplier update step size.
            initialmultiplier: Initial value for Lagrange multipliers.
        """
        # Hyperparameter Validation Bounds:
        
        # beta: must be > 0
        self._beta_allowed_min: float = 0.0                            # strict (>)
        self._beta_allowed_max: float = float('inf')                   # strict (<), inf bounds are always exclusive
        self._beta_rec_min: float = 0.0                                # strict (>), same as allowed_min
        self._beta_rec_max: float = float('inf')                       # strict (<), inf bounds are always exclusive
        
        # initialmultiplier: can be anything, should be 0
        self._initialmultiplier_allowed_min: float = float('-inf')     # strict (>), inf bounds are always exclusive
        self._initialmultiplier_allowed_max: float = float('inf')      # strict (<), inf bounds are always exclusive
        self._initialmultiplier_rec_min: float = 0.0                   # inclusive (>=)
        self._initialmultiplier_rec_max: float = 0.0                   # inclusive (<=)
        
        # Set inputs
        self._beta: float = beta
        self._initialmultiplier: float = initialmultiplier
        
        # Validate inputs
        self.validate_inputs()

    def validate_inputs(self) -> None:
        """Validate the hyperparameters of this update method.

        Raises:
            ValueError: If any parameter is outside the allowed range.
        """
        # ===== beta Validation =====
        # Allowed: > 0 (strict), Recommended: > 0 (strict)
        if not (self._beta_allowed_min < self._beta < self._beta_allowed_max):
            raise ValueError(
                f"{DDO_Color}beta must be in ({self._beta_allowed_min}, {self._beta_allowed_max}), but got {self._beta}.{Reset}"
            )
        elif not (self._beta_rec_min < self._beta < self._beta_rec_max):
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: beta={self._beta} is outside the recommended range "
                      f"({self._beta_rec_min}, {self._beta_rec_max}).")
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
                                       inconsistencyin: List[float]) -> None:
        """Update Lagrange multipliers using the standard LC subgradient rule.

        Update formula: λ_new = λ_old + beta * inconsistency
        Args:
            multiplierin: Current multiplier values to update in place.
            inconsistencyin: Current inconsistency values.
        """
        for i in range(len(multiplierin)):
            multiplierin[i] = multiplierin[i] + self._beta * inconsistencyin[i]

    def get_InitialMultiplier(self) -> float:
        """Get the initial Lagrange multiplier value.

        Returns:
            The initial Lagrange multiplier value.
        """
        return self._initialmultiplier
    
    def print_startup_summary(self) -> None:
        """Print the subgradient multiplier parameters beta and initial multiplier at startup."""
        name = f"{type(self).__name__}:"
        pad = " " * len(name)
        ddo_print(f"{name}     beta:                {self._beta}", indent=1)
        ddo_print(f"{pad}     initialmultiplier:   {self._initialmultiplier}", indent=1)
    
    def print_termination_summary(self) -> None:
        """Print the subgradient multiplier parameters beta and initial multiplier at the end."""
        name = f"{type(self).__name__}:"
        pad = " " * len(name)
        ddo_print(f"{name}     beta:                {self._beta}", indent=1)
        ddo_print(f"{pad}     initialmultiplier:   {self._initialmultiplier}", indent=1)
    
    def update_state(self, other: 'UpdateCouplingParameterMethod_SubgradientMultipliers') -> None:
        """Update the state of this instance with values from another instance.

        Args:
            other: The source instance containing updated values from parallel execution.
        """
        # No copy.copy() needed - float is a primitive/immutable type
        self._beta = other._beta
        self._initialmultiplier = other._initialmultiplier

```
