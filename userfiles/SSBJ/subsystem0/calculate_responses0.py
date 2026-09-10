# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Response calculation module for SSBJ Subsystem 0 (Aircraft).

This module provides the range calculation for the aircraft subsystem
of the Supersonic Business Jet (SSBJ) problem.

Attribution:
    This file contains code derived from the DMDO framework by Ahmed Bayoumy,
    originally published under the GNU Lesser General Public License v3.0.
    Ahmed H. Bayoumy, the copyright holder of the original code, has granted
    permission to distribute this derived file under the GNU Lesser General
    Public License v3.0.
    Source: https://github.com/Ahmed-Bayoumy/DMDO/blob/DEV/tests/SBJ/SSBJ_Aircraft.py
    Relevant original function: _calculate_range()

    Modifications from the original:
        - Refactored from a class-based structure (SSBJ_Aircraft) to a standalone function.
        - Inlined the _calculate_theta_r() helper logic directly into calculate_range().
        - Parameters are passed as function arguments instead of class attributes.
        - Removed auxiliary methods: SBJ_aircraft_analysis(), SBJ_aircraft_opt(),
          get_results(), __str__(), __repr__().
        - Added type hints to function signatures.
        - Added Google-style docstrings.
        - CORRECTED the Breguet range equation. The original DMDO code computes
          np.sqrt(theta_r / SFC), which places the specific fuel consumption (SFC)
          under the square root and makes range scale as SFC^(-0.5). The standard
          Breguet range equation for jet aircraft (Anderson, Raymer, MIT 16.Unified)
          is R = (a*M / (g*c_T)) * (L/D) * ln(W1/W2), where the thrust-specific fuel
          consumption c_T enters linearly (R proportional to 1/SFC). The square root
          applies only to the temperature ratio theta_r, because it originates from
          the speed of sound a = a_0 * sqrt(theta_r) (a_0 = 661 kn at sea level).
          We therefore use np.sqrt(theta_r) / SFC instead of np.sqrt(theta_r / SFC).
          This also matches the NoHiMDO reference implementations
          (bastientalgorn/NoHiMDO and khbalhandawi/NoHiMDO). Note: this is a
          physics-fidelity change and alters the computed range (~1.4x at the
          nominal point), which affects the range >= 2000 nmi constraint.
"""

import numpy as np
import math


def calculate_range(specific_fuel_consumption: float, lift_to_drag_ratio: float, total_weight: float, fuel_weight: float, h: float, Mach: float) -> float:
        """Calculate the aircraft range using the Breguet range equation.

        Args:
            specific_fuel_consumption: Specific fuel consumption coefficient [1/hr].
            lift_to_drag_ratio: Lift-to-drag ratio [-].
            total_weight: Total aircraft weight [lb].
            fuel_weight: Fuel weight [lb].
            h: Altitude in feet [ft].
            Mach: Mach number [-].

        Returns:
            Range in nautical miles [nmi].
        """
        if h < 36089:
            theta_r = 1 - 0.000006875 * h  # temperature ratio [-]
        else:
            theta_r = 0.7519  # temperature ratio [-]

        # Breguet range: V = a*M with a = a_0 * sqrt(theta_r) (a_0 = 661 kn), and the
        # specific fuel consumption divides linearly (R ~ 1/SFC). The sqrt wraps only
        # theta_r. This corrects the original DMDO form np.sqrt(theta_r / SFC); see
        # the module header for the full rationale.
        return (Mach * lift_to_drag_ratio * 661.0 *
                np.sqrt(theta_r) / specific_fuel_consumption *
                math.log((total_weight) / (total_weight - fuel_weight)))