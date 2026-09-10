# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Abstract interface for all scaler implementations."""
from abc import ABC, abstractmethod
from typing import List


class ScalerInterface(ABC):
    """Abstract interface for all scaler implementations."""

    @abstractmethod
    def __init__(self, lower_scaler_bound_unscaled: float, upper_scaler_bound_unscaled: float) -> None:
        """Initialize the scaler with the unscaled data range.

        Args:
            lower_scaler_bound_unscaled: The lower bound of the unscaled data range.
            upper_scaler_bound_unscaled: The upper bound of the unscaled data range.
        """

    @abstractmethod
    def transform(self, value_unscaled: float) -> float:
        """Scale value_unscaled according to feature_range.

        Args:
            value_unscaled: The value to transform.

        Returns:
            The scaled value.
        """

    @abstractmethod
    def inverse_transform(self, value_scaled: float) -> float:
        """Undo the scaling of value_scaled according to feature_range.

        Args:
            value_scaled: The scaled value to inverse transform.

        Returns:
            The original unscaled value.
        """

    @abstractmethod
    def get_bound_violation_warnings(self) -> List[str]:
        """Get warning messages for observed values outside the fitted range.

        Returns:
            List of warning message strings. Empty list if no violations.
        """

    @abstractmethod
    def get_bound_utilization_report(self) -> tuple[str, bool, bool]:
        """Get a compact one-line bound utilization summary for this scaler.

        Returns:
            A tuple of (summary_line, has_violation, has_conservative).
        """
