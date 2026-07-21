
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Scaler for normalizing values to the range [0, 1]."""
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis


class ScalerZeroOne(ScalerBasis):
    """A scaler that normalizes values to the range [0, 1].

    Provides validation and scalar value support for optimization design variables.
    """

    def __init__(self, lower_scaler_bound_unscaled: float, upper_scaler_bound_unscaled: float) -> None:
        """Initialize the ScalerZeroOne with feature range [0, 1].

        Args:
            lower_scaler_bound_unscaled: The lower bound of the unscaled data range.
            upper_scaler_bound_unscaled: The upper bound of the unscaled data range.

        Raises:
            ValueError: If lower_scaler_bound_unscaled is not strictly less than upper_scaler_bound_unscaled.
        """
        super().__init__(
            lower_scaler_bound_unscaled=lower_scaler_bound_unscaled,
            upper_scaler_bound_unscaled=upper_scaler_bound_unscaled,
            lower_scaler_bound_scaled=0.0,
            upper_scaler_bound_scaled=1.0,
        )
