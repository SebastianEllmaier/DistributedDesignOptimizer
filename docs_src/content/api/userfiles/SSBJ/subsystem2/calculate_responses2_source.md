---
title: calculate_responses2 (Source)
---

← Back to [calculate_responses2 documentation](calculate_responses2.md)

# calculate_responses2 - Source Code

**File:** `userfiles\SSBJ\subsystem2\calculate_responses2.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Response calculation module for SSBJ Subsystem 2 (Aerodynamics).

This module provides aerodynamic calculations for the
Supersonic Business Jet (SSBJ) problem.

Attribution:
    This file contains code derived from the DMDO framework by Ahmed Bayoumy,
    originally published under the GNU Lesser General Public License v3.0.
    Ahmed H. Bayoumy, the copyright holder of the original code, has granted
    permission to distribute this derived file under the GNU Lesser General
    Public License v3.0.
    Source: https://github.com/Ahmed-Bayoumy/DMDO/blob/DEV/tests/SBJ/SSBJ_Aerodynamics.py
    Relevant original functions: calculate_drag_polar(), poly_approx()

    Modifications from the original:
        - Refactored from class SSBJAerodynamics to standalone functions; removed
          auxiliary methods (SBJ_aerodynamics_opt(), print_results(), __init__()).
        - Constants, coefficients, and state variables are passed as function
          arguments instead of class attributes.
        - poly_approx() decoupled from instance state (self.Z, self.ESFp, etc.).
        - Removed the if CLo[0] > 0 branch in calculate_constraints() (only the
          CLo[0] > 0 case is retained).
        - Adverse pressure gradient (calculate_drag_polar()): the base argument of
          poly_approx() is set to the fixed baseline thickness-to-chord ratio
          (tc = 0.05) to match NoHiMDO (SBJ_constraint_dragpolar.m). The DMDO port
          reused the local thickness_to_chord_ratio for both the base and the
          evaluation point (base == new), which collapses the response surface to a
          constant and makes the constraint inert. Using the fixed baseline as the
          base restores a live constraint that responds to the local t/c design
          variable. (DDO's aerodynamics subsystem only has access to its own local
          t/c, not the shared/target copy NoHiMDO passes as tc, so the baseline
          design value about which the response surface is fitted is used instead.)
        - Engine-scale-factor drag factor Fo1 (calculate_drag_polar()): the base
          argument of poly_approx() is set to the fixed nominal ESF baseline
          (engine_scale_factor = 1.0, i.e. the initial local design value) instead
          of reusing the current engine_scale_factor for both base and evaluation
          point. The DMDO port used base == new, which collapsed Fo1 to the constant
          Ao and made the ESF term in CDmin inert. Using base != new restores an Fo1
          (and hence a minimum-drag coefficient) that responds to the local
          engine_scale_factor design variable, mirroring the adverse-pressure-gradient
          (tc = 0.05) fix above.
        - Added type hints to function signatures.
        - Added Google-style docstrings.
        - Added explanatory inline comments and physical units (e.g. [ft], [lb],
          [deg], [-]) throughout to document the design variables, responses, and
          intermediate quantities.
"""

import numpy as np 
import copy

def poly_approx(S, S_new, flag, S_bound):
    """
    Second-order polynomial response-surface approximation (SSBJ surrogate).

    Fits a quadratic about the base point S and evaluates it at S_new,
    returning a dimensionless correction factor.
    NOTE: if S_new == S the normalized shift is zero and FF collapses to the
    constant term Ao (i.e. the factor becomes independent of the input).

    Args:
        S: Base (reference) values.
        S_new: Evaluation-point values.
        flag: Per-variable slope/shape mode selector.
        S_bound: Per-variable bound used to fit the polynomial.

    Returns:
        FF: Dimensionless correction factor [-].
    """
    S_norm = []
    S_shifted = []
    Ai = []
    Aij = np.zeros((len(S), len(S)))

    for i in range(len(S)):
        S_norm.append(S_new[i] / S[i])
        if S_norm[i] > 1.25:
            S_norm[i] = 1.25
        elif S_norm[i] < 0.75:
            S_norm[i] = 0.75
        S_shifted.append(S_norm[i] - 1)
        a = 0.1
        b = a

        if flag[i] == 5:
            # CALCULATE POLYNOMIAL COEFFICIENTS (S-ABOUT ORIGIN)
            So = 0
            Sl = So - S_bound[i]
            Su = So + S_bound[i]
            Mtx_shifted = np.array([[1, Sl, Sl**2], [1, So, So**2], [1, Su, Su**2]])

            F_bound = np.array([1 + (.5*a)**2, 1, 1 + (.5*b)**2])
            A = np.linalg.solve(Mtx_shifted, F_bound)
            Ao = A[0]
            Ai.append(A[1])
            Aij[i, i] = A[2]

        # CALCULATE POLYNOMIAL COEFFICIENTS
        else:
            if flag[i] == 0:
                S_shifted.append(0)
            elif flag[i] == 3:
                a *= -1
                b = copy.deepcopy(a)
            elif flag[i] == 2:
                b = 2 * a
            elif flag[i] == 4:
                a *= -1
                b = 2*a
            # DETERMINE BOUNDS ON FF DEPENDING ON SLOPE-SHAPE
            # CALCULATE POLYNOMIAL COEFFICIENTS (S-ABOUT ORIGIN)
            So = 0
            Sl = So - S_bound[i]
            Su = So + S_bound[i]
            Mtx_shifted = np.array([[1, Sl, Sl**2], [1, So, So**2], [1, Su, Su**2]])
            F_bound = np.array([1 - .5*a, 1, 1 + .5*b])
            A = np.linalg.solve(Mtx_shifted, F_bound)
            Ao = A[0]
            Ai.append(A[1])
            Aij[i, i] = A[2]

            # CALCULATE POLYNOMIAL COEFFICIENTS

    # Correlation matrix
    R = np.array([[0.2736, 0.3970, 0.8152, 0.9230, 0.1108],
                    [0.4252, 0.4415, 0.6357, 0.7435, 0.1138],
                    [0.0329, 0.8856, 0.8390, 0.3657, 0.0019],
                    [0.0878, 0.7248, 0.1978, 0.0200, 0.0169],
                    [0.8955, 0.4568, 0.8075, 0.9239, 0.2525]])

    for i in range(len(S)):
        for j in range(i+1, len(S)):
            Aij[i, j] = Aij[i, i] * R[i, j]
            Aij[j, i] = Aij[i, j]

    S_shifted = np.array(S_shifted)
    FF = Ao + np.dot(Ai, np.transpose(S_shifted)) + (1/2) * np.dot(np.dot(S_shifted, Aij), np.transpose(S_shifted))
    return FF

def calculate_drag_polar(tail_sweep_angle: float, wing_moment_arm: float, tail_moment_arm: float, thickness_to_chord_ratio: float, wing_sweep_angle: float, wing_aspect_ratio: float, wing_surface_area: float, tail_aspect_ratio: float, tail_surface_area: float, total_weight: float, engine_scale_factor: float, wing_twist: float, h: float, Mach: float):
    """
    Calculate the drag polar and related parameters.

    Args:
        tail_sweep_angle: Horizontal tail sweep angle [deg].
        wing_moment_arm: Wing aerodynamic moment arm [ft].
        tail_moment_arm: Horizontal tail aerodynamic moment arm [ft].
        thickness_to_chord_ratio: Wing thickness-to-chord ratio [-].
        wing_sweep_angle: Wing sweep angle [deg].
        wing_aspect_ratio: Wing aspect ratio [-].
        wing_surface_area: Wing reference surface area [ft^2].
        tail_aspect_ratio: Horizontal tail aspect ratio [-].
        tail_surface_area: Horizontal tail reference surface area [ft^2].
        total_weight: Total aircraft weight [lb].
        engine_scale_factor: Engine scale factor, ESF [-].
        wing_twist: Wing twist / incidence angle [deg].
        h: Altitude [ft].
        Mach: Mach number [-].

    Returns:
        List containing [Lift [lb], Drag [lb], LDr [-], Pg [-],
        CLo_wing [-], CLo_tail [-]].
    """
    Nh = 1.0  # horizontal-tail effectiveness factor [-]
        
    # Calculate velocity [ft/s] and density [slug/ft^3] (US Standard Atmosphere)
    if h < 36089:  # 36089 ft = tropopause altitude
        V = Mach * (1116.39 * np.sqrt(1 - (6.875e-06 * h)))  # velocity [ft/s]; 1116.39 ft/s = sea-level speed of sound
        rho = (2.377e-03) * (1 - (6.875e-06 * h))**4.2561    # density [slug/ft^3]; 2.377e-3 = sea-level density
    else:
        V = Mach * 968.1                                     # velocity [ft/s]; 968.1 ft/s = stratospheric speed of sound
        rho = (2.377e-03) * (.2971) * np.exp(-(h - 36089) / 20806.7)  # density [slug/ft^3]

    q = 0.5 * rho * (V**2)  # dynamic pressure [lb/ft^2]

    # Scale coefficients for proper conditioning of matrix A
    # Row 1 = lift balance, row 2 = pitching-moment balance about the CG.
    a = q * wing_surface_area / 1e5                                     # wing lift term [lb] / 1e5
    b = Nh * q * tail_surface_area / 1e5                                # tail lift term [lb] / 1e5
    c = wing_moment_arm                                                 # wing moment arm [ft]
    d = tail_moment_arm * Nh * (tail_surface_area / wing_surface_area)  # effective tail moment arm [ft]

    A = np.array([[a, b], [c, d]])

    # Scale coefficient Wt (total_weight) for proper conditioning of matrix A
    B = np.array([total_weight / 1e5, 0])  # total_weight [lb] / 1e5

    # Solve for CLo (trim lift coefficients [-]: CLo[0] wing, CLo[1] tail)
    try:
        CLo = np.linalg.solve(A, B)
    except:  # noqa: E722
        CLo = np.array([-np.inf, np.inf])

    # Calculate delta_L: empirical lift increment [lb] due to wing twist.
    # NOTE: delta_L = wing_twist[deg] * q[lb/ft^2] does not formally balance
    # dimensionally; this is a simplification inherited from the SSBJ surrogate.
    delta_L = wing_twist * q                        # lift increment [lb]
    Lw1 = CLo[0] * q * wing_surface_area - delta_L  # wing lift [lb]
    CLw1 = Lw1 / (q * wing_surface_area)            # wing lift coefficient [-]
    CLht1 = -CLw1 * c / d                           # tail lift coefficient [-]

    # Scale first coefficient of D for proper conditioning of matrix A
    D = np.array([(total_weight - CLw1 * a - CLht1 * b) / 1e5, -CLw1 * c - CLht1 * d])

    # Solve for DCL (lift-coefficient increments [-])
    try:
        DCL = np.linalg.solve(A, D)
    except:  # noqa: E722
        DCL = np.array([np.nan, np.nan])

    # Calculate induced-drag (drag-due-to-lift) factors kw, kht [-]
    if Mach >= 1:  # supersonic branch
        kw = wing_aspect_ratio * (Mach**2 - 1) * np.cos(wing_sweep_angle * np.pi / 180) / \
        (4 * wing_aspect_ratio * np.sqrt(Mach**2 - 1) - 2)  # wing induced-drag factor [-]
        kht = tail_aspect_ratio * (Mach**2 - 1) * np.cos(tail_sweep_angle * np.pi / 180) / \
        (4 * tail_aspect_ratio * np.sqrt(Mach**2 - 1) - 2)  # tail induced-drag factor [-]
    else:  # subsonic branch (0.8 = Oswald span efficiency)
        kw = 1 / (np.pi * 0.8 * wing_aspect_ratio)   # wing induced-drag factor [-]
        kht = 1 / (np.pi * 0.8 * tail_aspect_ratio)  # tail induced-drag factor [-]

    # Calculate Fo1: engine-scale-factor (ESF) drag-correction factor [-].
    # By definition ESF = 1.0 at the nominal engine, which is also the initial
    # design value of the local engine_scale_factor (2d[10]). We therefore fit the
    # response surface about that fixed baseline (base = 1.0) and evaluate it at the
    # current engine_scale_factor. Using base != new keeps Fo1 (and hence the ESF
    # term in CDmin below) live and responsive to the local ESF. This mirrors the
    # base != new fix applied to the adverse-pressure-gradient term Pg further down;
    # the original DMDO used base == new, which collapsed Fo1 to the constant Ao.
    ENGINE_SCALE_FACTOR_REFERENCE = 1.0  # nominal ESF [-] (initial value of 2d[10])
    S_initial1 = [ENGINE_SCALE_FACTOR_REFERENCE]
    S1 = [engine_scale_factor]
    flag1 = 1
    bound1 = 0.25
    Fo1 = poly_approx(S_initial1 if isinstance(S_initial1, list) else [S_initial1],
                        S1 if isinstance(S1, list) else [S1],
                        flag1 if isinstance(flag1, list) else [flag1],
                        bound1 if isinstance(bound1, list) else [bound1])

    # Calculate minimum drag coefficient CDmin [-] (0.01375 = skin-friction/CDmin constant)
    CDmin = 0.01375 * Fo1 + 3.05 * (thickness_to_chord_ratio**(5/3)) * ((np.cos(wing_sweep_angle * np.pi / 180))**(3/2))

    # Calculate total drag coefficients [-]
    CDw = CDmin + kw * (CLo[0]**2) + kw * (DCL[0]**2)  # wing drag coefficient [-]
    CDht = kht * (CLo[1]**2) + kht * (DCL[1]**2)       # tail drag coefficient [-]
    CDp = CDw + CDht                                    # total drag coefficient [-]
    CLp = CLo[0] + CLo[1]                               # total lift coefficient [-]

    # Calculate lift and drag
    Lift = total_weight                                               # lift [lb] (equals weight in trimmed cruise)
    Drag = q * CDw * wing_surface_area + q * CDht * tail_surface_area  # drag [lb]
    LDr = CLp / CDp                                                   # lift-to-drag ratio [-]

    # Calculate adverse pressure gradient (G2)
    # NoHiMDO (SBJ_constraint_dragpolar.m) evaluates PolyApprox(tc, Z(1)), where
    # the base "tc" is the system/shared copy of the thickness-to-chord ratio and
    # Z(1) is the aerodynamics-local copy. Because these are two distinct copies in
    # the non-hierarchical ALC scheme, the constraint is live. This subsystem only
    # has access to its own local thickness_to_chord_ratio, so we reproduce that
    # behaviour with the fixed baseline value (tc = 0.05, the reference design
    # point about which the response surface is fitted) as the base and the current
    # local thickness_to_chord_ratio as the evaluation point. Using base != new
    # keeps the constraint live (the DMDO port used base == new, which made it
    # collapse to a constant).
    THICKNESS_TO_CHORD_RATIO_REFERENCE = 0.05  # NoHiMDO baseline tc [-] (S_initial2)
    S_initial2 = [THICKNESS_TO_CHORD_RATIO_REFERENCE]
    S2 = [thickness_to_chord_ratio]
    flag1 = [1]
    bound1 = [0.25]

    Pg = poly_approx(S_initial2, S2, flag1, bound1)  # adverse pressure gradient factor [-]

    # Return [Lift [lb], Drag [lb], LDr [-], Pg [-], CLo_wing [-], CLo_tail [-]]
    return [Lift, Drag, LDr, Pg, CLo[0], CLo[1]]
```
