---
title: UpdateCouplingParameterMethod_AdaptiveWeights (Source)
---

← Back to [UpdateCouplingParameterMethod_AdaptiveWeights documentation](UpdateCouplingParameterMethod_AdaptiveWeights.md)

# UpdateCouplingParameterMethod_AdaptiveWeights - Source Code

**File:** `Distributed_Design_Optimizer\coordination\updatecouplingparametermethod\UpdateCouplingParameterMethod_AdaptiveWeights.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Standard PC coupling parameter update method.

This module implements the standard Penalty Coordination
update strategy for penalty weights (without Lagrange multipliers).
"""

from typing import List
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print, ddo_print_border
from Distributed_Design_Optimizer.coordination.updatecouplingparametermethod.UpdateCouplingParameterMethodInterface import UpdateCouplingParameterMethodInterface


class UpdateCouplingParameterMethod_AdaptiveWeights(UpdateCouplingParameterMethodInterface):
    """Standard PC update method for coupling parameters.

    Implements the penalty coordination update rules (without multipliers):
    - Weights: w_new = β * w_old if |c_new| > γ * |c_old|, else w_old

    Attributes:
        _beta: Penalty weight update factor for increasing weights (must be > 1).
        _gamma: Inconsistency reduction threshold factor (must be in (0, 1)).
        _initialweight: Initial value for penalty weights (must be >= 0).
    """

    def __init__(self,
                 beta: float,
                 gamma: float,
                 initialweight: float) -> None:
        """Initialize the standard PC update method.

        Args:
            beta: Penalty weight update factor for increasing weights.
            gamma: Inconsistency reduction threshold factor.
            initialweight: Initial value for penalty weights.
        """
        # Hyperparameter Validation Bounds:
        
        # beta: must be > 1, should be <= 3
        self._beta_allowed_min: float = 1.0                            # strict (>)
        self._beta_allowed_max: float = float('inf')                   # strict (<), inf bounds are always exclusive
        self._beta_rec_min: float = 1.0                                # strict (>), same as allowed_min
        self._beta_rec_max: float = 3.0                                # inclusive (<=)
        
        # gamma: must be in (0, 1)
        self._gamma_allowed_min: float = 0.0                           # strict (>)
        self._gamma_allowed_max: float = 1.0                           # strict (<)
        
        # initialweight: must be >= 0, should be in (0, 0.1]
        self._initialweight_allowed_min: float = 0.0                   # inclusive (>=)
        self._initialweight_allowed_max: float = float('inf')          # strict (<), inf bounds are always exclusive
        self._initialweight_rec_min: float = 0.0                       # strict (>)
        self._initialweight_rec_max: float = 0.1                       # inclusive (<=)
        
        # Set inputs
        self._beta: float = beta
        self._gamma: float = gamma
        self._initialweight: float = initialweight
        
        # Validate inputs
        self.validate_inputs()

    def validate_inputs(self) -> None:
        """Validate the hyperparameters of this update method.

        Raises:
            ValueError: If any parameter is outside the allowed range.
        """
        # ===== beta Validation =====
        # Allowed: > 1 (strict), Recommended: <= 3 (inclusive)
        if not (self._beta_allowed_min < self._beta < self._beta_allowed_max):
            raise ValueError(
                f"{DDO_Color}beta must be in ({self._beta_allowed_min}, {self._beta_allowed_max}), but got {self._beta}. See e.g. Meng Xu, "
                f"'Accuracy, Efficiency, and Parallelism in Network Target Coordination Optimization'{Reset}"
            )
        elif not (self._beta_rec_min < self._beta <= self._beta_rec_max):
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: beta={self._beta} is outside the recommended range (beta <= {self._beta_rec_max}), "
                      "see e.g. Meng Xu: Accuracy, Efficiency, and Parallelism in Network Target Coordination Optimization'")
            ddo_print_border()
        
        # ===== gamma Validation =====
        # Allowed: (0, 1) (strict on both sides)
        if not (self._gamma_allowed_min < self._gamma < self._gamma_allowed_max):
            raise ValueError(
                f"{DDO_Color}gamma must be in ({self._gamma_allowed_min}, {self._gamma_allowed_max}), but got {self._gamma}. "
                f"See e.g. Meng Xu, 'Accuracy, Efficiency, and Parallelism in Network Target Coordination Optimization'{Reset}"
            )
        
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

    def update_CoordinationWeights(self,
                                   weightin: List[float],
                                   inconsistencyIn: List[float],
                                   inconsistencyOldIn: List[float] | None) -> None:
        """Update penalty weights based on inconsistency progress.

        If the inconsistency has not decreased sufficiently (by factor gamma),
        the weight is increased by factor beta.

        Args:
            weightin: Current weight values to update in place.
            inconsistencyIn: Current inconsistency values.
            inconsistencyOldIn: Previous iteration inconsistency values, or None.
        """
        if inconsistencyOldIn is not None:
            for i in range(len(inconsistencyIn)):
                # If decrement in inconsistencies is not enough, increase the penalties
                if abs(inconsistencyIn[i]) > self._gamma * abs(inconsistencyOldIn[i]):
                    weightin[i] = self._beta * weightin[i]
                # else: keep the weight unchanged

    def get_InitialWeight(self) -> float:
        """Get the initial penalty weight value.

        Returns:
            The initial penalty weight value.
        """
        return self._initialweight
    
    def print_startup_summary(self) -> None:
        """Print the adaptive weight parameters beta and gamma at startup."""
        name = f"{type(self).__name__}:"
        pad = " " * len(name)
        ddo_print(f"{name}     beta:            {self._beta}", indent=1)
        ddo_print(f"{pad}     gamma:           {self._gamma}", indent=1)
        ddo_print(f"{pad}     initialweight:   {self._initialweight}", indent=1)

    def print_termination_summary(self) -> None:
        """Print the adaptive weight parameters beta and gamma at the end."""
        name = f"{type(self).__name__}:"
        pad = " " * len(name)
        ddo_print(f"{name}     beta:            {self._beta}", indent=1)
        ddo_print(f"{pad}     gamma:           {self._gamma}", indent=1)
        ddo_print(f"{pad}     initialweight:   {self._initialweight}", indent=1)
    
    def update_state(self, other: 'UpdateCouplingParameterMethod_AdaptiveWeights') -> None:
        """Update the state of this instance with values from another instance.

        Args:
            other: The source instance containing updated values from parallel execution.
        """
        # No copy.copy() needed - float is a primitive/immutable type
        self._beta = other._beta
        self._gamma = other._gamma
        self._initialweight = other._initialweight

```
