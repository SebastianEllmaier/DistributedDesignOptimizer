---
title: ScalerConstraint (Source)
---

← Back to [ScalerConstraint documentation](ScalerConstraint.md)

# ScalerConstraint - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\tools\ScalerConstraint.py`

```python

# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Scaler for normalizing constraint values to [-0.5, 0.5]."""
import numpy as np

from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis


class ScalerConstraint(ScalerBasis):
    """A scaler that normalizes constraint values to the range [-0.5, 0.5].

    Provides validation and scalar value support for optimization constraints.
    Requires symmetric data range about 0.
    """

    def __init__(self, lower_scaler_bound_unscaled: float, upper_scaler_bound_unscaled: float) -> None:
        """Initialize the ScalerConstraint with feature range [-0.5, 0.5].

        Ensures that the data range is symmetric about 0, meaning -1*min = max.

        Args:
            lower_scaler_bound_unscaled: The lower bound of the unscaled data range.
            upper_scaler_bound_unscaled: The upper bound of the unscaled data range.

        Raises:
            ValueError: If the data range is not symmetric about 0 or is zero.
        """
        super().__init__(
            lower_scaler_bound_unscaled=lower_scaler_bound_unscaled,
            upper_scaler_bound_unscaled=upper_scaler_bound_unscaled,
            lower_scaler_bound_scaled=-0.5,
            upper_scaler_bound_scaled=0.5,
        )

        # Check if data range is symmetric about 0
        if not np.isclose(-1 * self._lower_scaler_bound_unscaled, self._upper_scaler_bound_unscaled, rtol=1e-8):
            raise ValueError(f"{DDO_Color}Fitted data range must be symmetric about 0. Got min={self._lower_scaler_bound_unscaled} and max={self._upper_scaler_bound_unscaled}. "
                             f"Please ensure that -1*min = max when calling ScalerConstraint() in input file{Reset}")

```
