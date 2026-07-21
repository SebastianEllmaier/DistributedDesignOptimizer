
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Base scaler implementation for normalizing values to a scaled range."""
from typing import List

import numpy as np

from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset
from Distributed_Design_Optimizer.subsystem.tools import ScalerInterface


class ScalerBasis(ScalerInterface):
    """Base implementation for scalers that normalize values to a scaled range.

    Provides common initialization, transform, inverse_transform, and
    bound-violation warning logic. Subclasses set the scaled bounds and
    display name, and may add extra validation.
    """

    def __init__(
        self,
        lower_scaler_bound_unscaled: float,
        upper_scaler_bound_unscaled: float,
        lower_scaler_bound_scaled: float,
        upper_scaler_bound_scaled: float,
    ) -> None:
        """Initialize the scaler.

        Args:
            lower_scaler_bound_unscaled: The lower bound of the unscaled data range.
            upper_scaler_bound_unscaled: The upper bound of the unscaled data range.
            lower_scaler_bound_scaled: The lower bound of the scaled feature range.
            upper_scaler_bound_scaled: The upper bound of the scaled feature range.

        Raises:
            ValueError: If lower_scaler_bound_unscaled is not strictly less than upper_scaler_bound_unscaled.
        """
        if not lower_scaler_bound_unscaled < upper_scaler_bound_unscaled:
            raise ValueError(
                f"{DDO_Color}lower_scaler_bound_unscaled ({lower_scaler_bound_unscaled}) must be strictly less than "
                f"upper_scaler_bound_unscaled ({upper_scaler_bound_unscaled}){Reset}")

        self._lower_scaler_bound_warning_raised: bool = False
        self._upper_scaler_bound_warning_raised: bool = False
        self._smallest_observed_value_unscaled: float | None = None
        self._largest_observed_value_unscaled: float | None = None
        self._upper_scaler_bound_scaled: float = upper_scaler_bound_scaled
        self._lower_scaler_bound_scaled: float = lower_scaler_bound_scaled
        self._lower_scaler_bound_unscaled: float = lower_scaler_bound_unscaled
        self._upper_scaler_bound_unscaled: float = upper_scaler_bound_unscaled

        # Compute scale and min factors
        # scale = (feature_max - feature_min) / (data_max - data_min)
        # min = feature_min - data_min * scale
        self._scale: float = (self._upper_scaler_bound_scaled - self._lower_scaler_bound_scaled) / (self._upper_scaler_bound_unscaled - self._lower_scaler_bound_unscaled)
        self._min: float = self._lower_scaler_bound_scaled - self._lower_scaler_bound_unscaled * self._scale

    def transform(self, value_unscaled: float) -> float:
        """Scale value_unscaled according to feature_range.

        Args:
            value_unscaled: The value to transform.

        Returns:
            The scaled value.

        Warns:
            UserWarning: If the input value is outside the fitted range (once per bound).
        """
        # Update observed value tracking
        if self._smallest_observed_value_unscaled is None or value_unscaled < self._smallest_observed_value_unscaled:
            self._smallest_observed_value_unscaled = value_unscaled
        if self._largest_observed_value_unscaled is None or value_unscaled > self._largest_observed_value_unscaled:
            self._largest_observed_value_unscaled = value_unscaled

        # Direct float comparison
        if value_unscaled < self._lower_scaler_bound_unscaled and not self._lower_scaler_bound_warning_raised:
            self._lower_scaler_bound_warning_raised = True
            print(f"{DDO_Color}WARNING: Input value {value_unscaled} is below the fitted range [{self._lower_scaler_bound_unscaled} , {self._upper_scaler_bound_unscaled}]. "
                  f"Adapt your bounds of {type(self).__name__}() in input file. "
                  f"Thus results of distributed optimization execution are not representative.{Reset}")
        if value_unscaled > self._upper_scaler_bound_unscaled and not self._upper_scaler_bound_warning_raised:
            self._upper_scaler_bound_warning_raised = True
            print(f"{DDO_Color}WARNING: Input value {value_unscaled} is above the fitted range [{self._lower_scaler_bound_unscaled} , {self._upper_scaler_bound_unscaled}]. "
                  f"Adapt your bounds of {type(self).__name__}() in input file. "
                  f"Thus results of distributed optimization execution are not representative.{Reset}")
        # Direct arithmetic: x * scale + min
        return float(value_unscaled * self._scale + self._min)

    def inverse_transform(self, value_scaled: float) -> float:
        """Undo the scaling of value_scaled according to feature_range.

        Args:
            value_scaled: The scaled value to inverse transform.

        Returns:
            The original unscaled value.

        Warns:
            UserWarning: If the input value is outside the feature_range (once per bound).
        """
        # Tolerance-based comparison to allow values at boundaries
        if value_scaled < self._lower_scaler_bound_scaled and not np.isclose(value_scaled, self._lower_scaler_bound_scaled, atol=1e-8, rtol=0):
            if not self._lower_scaler_bound_warning_raised:
                self._lower_scaler_bound_warning_raised = True
                print(f"{DDO_Color}WARNING: Input value {value_scaled} is below the feature_range [{self._lower_scaler_bound_scaled}, {self._upper_scaler_bound_scaled}]. "
                      f"Thus results of distributed optimization execution are not representative.{Reset}")
        if value_scaled > self._upper_scaler_bound_scaled and not np.isclose(value_scaled, self._upper_scaler_bound_scaled, atol=1e-8, rtol=0):
            if not self._upper_scaler_bound_warning_raised:
                self._upper_scaler_bound_warning_raised = True
                print(f"{DDO_Color}WARNING: Input value {value_scaled} is above the feature_range [{self._lower_scaler_bound_scaled}, {self._upper_scaler_bound_scaled}]. "
                      f"Thus results of distributed optimization execution are not representative.{Reset}")
        # Direct arithmetic inverse: (x - min) / scale
        return float((value_scaled - self._min) / self._scale)

    def get_scale(self) -> float:
        """Return the constant affine scale factor d(scaled)/d(unscaled) of this scaler.

        Since the transform is affine (scaled = unscaled * scale + offset), this
        factor is a constant equal to ``self._scale``. Use it to map a derivative
        taken w.r.t. an unscaled quantity into scaled space, e.g. to convert
        d(response_unscaled) into d(response_scaled). The inverse mapping (into
        scaled design-variable space) is obtained at the call-site as ``1.0 / get_scale()``.

        Returns:
            The derivative d(scaled)/d(unscaled).
        """
        return self._scale

    def get_bound_violation_warnings(self) -> List[str]:
        """Get warning messages for observed values outside the fitted range.

        Returns:
            List of warning message strings. Empty list if no violations.
        """
        warnings_list: List[str] = []

        smallest = self._smallest_observed_value_unscaled
        largest = self._largest_observed_value_unscaled

        if smallest is None and largest is None:
            return warnings_list

        # Check lower bound violation
        if smallest is not None and smallest < self._lower_scaler_bound_unscaled:
            warnings_list.append(
                f"WARNING: Input value {smallest} is below the fitted range [{self._lower_scaler_bound_unscaled} , {self._upper_scaler_bound_unscaled}]. "
                f"Adapt your bounds of {type(self).__name__}() in input file. "
                f"Thus results of distributed optimization execution are not representative."
            )

        # Check upper bound violation
        if largest is not None and largest > self._upper_scaler_bound_unscaled:
            warnings_list.append(
                f"WARNING: Input value {largest} is above the fitted range [{self._lower_scaler_bound_unscaled} , {self._upper_scaler_bound_unscaled}]. "
                f"Adapt your bounds of {type(self).__name__}() in input file. "
                f"Thus results of distributed optimization execution are not representative."
            )

        return warnings_list

    def get_bound_utilization_report(self) -> tuple[str, bool, bool]:
        """Get a compact one-line bound utilization summary for this scaler.

        Returns:
            A tuple of (summary_line, has_violation, has_conservative).
            summary_line is a compact string. has_violation / has_conservative
            indicate whether advisory footnotes should be printed.
            Returns ('No values observed.', False, False) if nothing was seen.
        """
        smallest = self._smallest_observed_value_unscaled
        largest = self._largest_observed_value_unscaled

        if smallest is None and largest is None:
            return ('No values observed.', False, False)

        lb = self._lower_scaler_bound_unscaled
        ub = self._upper_scaler_bound_unscaled
        has_violation = False
        has_conservative = False
        parts: List[str] = []

        # Lower bound status
        if smallest is not None:
            if smallest < lb:
                parts.append(f"LB {lb}: min={smallest:.6g} VIOLATED(by {lb - smallest:.6g}) !")
                has_violation = True
            elif smallest == lb:
                parts.append(f"LB {lb}: min={smallest:.6g} EXACT")
            else:
                margin = smallest - lb
                parts.append(f"LB {lb}: min={smallest:.6g} OK(margin {margin:.6g}) *")
                has_conservative = True

        # Upper bound status
        if largest is not None:
            if largest > ub:
                parts.append(f"UB {ub}: max={largest:.6g} VIOLATED(by {largest - ub:.6g}) !")
                has_violation = True
            elif largest == ub:
                parts.append(f"UB {ub}: max={largest:.6g} EXACT")
            else:
                margin = ub - largest
                parts.append(f"UB {ub}: max={largest:.6g} OK(margin {margin:.6g}) *")
                has_conservative = True

        return (' | '.join(parts), has_violation, has_conservative)