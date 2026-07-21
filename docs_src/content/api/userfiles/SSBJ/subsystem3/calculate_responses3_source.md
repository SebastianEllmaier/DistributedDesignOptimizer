---
title: calculate_responses3 (Source)
---

← Back to [calculate_responses3 documentation](calculate_responses3.md)

# calculate_responses3 - Source Code

**File:** `userfiles\SSBJ\subsystem3\calculate_responses3.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# This file contains code derived from the DMDO framework by Ahmed Bayoumy,
# originally published under the GNU General Public License v3.0.
# Source: https://github.com/Ahmed-Bayoumy/DMDO/blob/DEV/tests/SBJ/SSBJ_Structures.py
# Relevant original functions: Wing_Mod(), loads(), polyApprox(),
#   calculate_structural_response(), calculate_constraints()
#
# Modifications from the original:
#   - Refactored from class WingDesignAnalyzer to standalone functions; removed
#       auxiliary methods (SBJ_structure_opt(), print_results(), __init__()).
#   - Constants, coefficients, and state variables are passed as function
#       arguments instead of class attributes.
#   - polyApprox() decoupled from instance state; renamed to poly_approx().
#   - Stress calculations use h_spar (spar height) consistently instead of
#       altitude self.h, correcting a variable-shadowing bug in the original.
#   - Added type hints to function signatures.
#   - Added Google-style docstrings.
#   - Fixed integer truncation of wing twist: `twist` is now allocated with
#       np.zeros(aa) instead of np.array([0] * aa), which previously created an
#       integer array that truncated the float twist values.
#         Original line: twist = np.array([0] * aa)
#         Modified line: twist = np.zeros(aa)
#   - Documented that the altitude `h` parameter is intentionally unused: the
#       original WingDesignAnalyzer never uses altitude in the structural-response
#       physics (Ws, Wf, theta); it only appeared in the constraints via the
#       variable-shadowing bug noted above. The parameter is retained for
#       interface symmetry with the other subsystems.
#   - Added a lower-bound guard on the spar height: h_spar = max(h_spar, 1E-5).
#       The original imposes no floor, so h_spar can reach zero or go negative for
#       some in-bounds designs, yielding non-physical sign-flipped stresses. The
#       clamp keeps the section height strictly positive.
#   - REPARAMETRIZED the panel thicknesses (see subsystem3/SubSystem3_Reformulation.md).
#       The 18 absolute thickness inputs (t1..t3, ts1..ts3, in inches) are replaced by a
#       two-level fractional parametrization, 3 values per spanwise station:
#         * alpha1, alpha3 : top/bottom sandwich depth fractions, ts1 = 2*alpha1*D,
#                            ts3 = 2*alpha3*D, where D = beta*(t/c)*chord is the available
#                            structural box depth (reconstructed locally after Wing_Mod);
#         * ts2            : web sandwich thickness, kept ABSOLUTE in inches (the web does
#                            not set the spar height, so it has no depth to be relative to);
#         * rho1, rho2, rho3 : skin-to-sandwich ratios, t_p = rho_p * ts_p.
#       Consequences (all exact restatements of the original physics at the current depth D):
#         * the spar-height margin 0.5(ts1+ts3) <= h_spar becomes the linear, division-free
#           h_spar = D*(1 - alpha1 - alpha3) with the constraint alpha1 + alpha3 <= 0.5;
#         * the core thickness ts_p - t_p = ts_p*(1 - rho_p) is >= 0 by construction (rho_p <= 1),
#           so the reverted max(ts - t, 0) core clamp is permanently unnecessary;
#         * h_spar >= 0 structurally (alpha-sum <= 1) and >= 0.5*D in the feasible region, so the
#           negative/near-zero h_spar blow-up cannot occur for a feasible design.
#       The Wing_Mod call is moved AHEAD of the thickness construction because the reconstruction
#       needs the chords c[0:3]; everything downstream is unchanged and consumes the reconstructed
#       t1..t3, ts1..ts3 exactly as before.
#   - Signature and return value changed accordingly: the function now accepts
#       (alpha1, alpha3, ts2, rho1, rho2, rho3) instead of (t, ts) and additionally returns the
#       reconstructed t_ft/ts_ft (feet) and the 3 h_spar-margin values (alpha1+alpha3-0.5) so the
#       caller can assemble the response vector and the constraint module can read them.
#   - Clamped the torsional twist contribution to +-180 degrees: Phi is the Bredt-Batho
#       closed-section twist (radians, converted via *180/pi) and scales like 1/h_spar**2, so a
#       near-degenerate (infeasible) section depth drives it far past +-180 deg. Such magnitudes are
#       non-physical for this linear small-angle model and can overflow `theta` downstream. Phi is
#       now clipped to +-pi rad (np.clip(Phi, -np.pi, np.pi)), capping the converted contribution at
#       +-180 deg. Feasible designs (where |Phi| stays small) are unaffected; the clamp only bounds
#       infeasible probes the optimizer may still evaluate.
#   - Floored the section moment of inertia I in loads() to a small positive value
#       (I = max(I, 1E-5), analogous to the h_spar floor). I is used only as a divisor when forming
#       the bending twist (A, B, Slope_A, Slope_B), so as Izz -> 0 for a near-degenerate thin-skin
#       section the bending twist bend_twist ~ 1/I diverges. bend_twist is the dominant, otherwise-
#       unbounded contributor to wing_twist (theta) -- the Phi clamp above does not cover it -- so
#       this floor caps it and prevents the theta blow-up that triggered the scaler-range warnings.
#   - Introduced a single module-level floor constant EPS (= 1E-5) and routed the existing h_spar
#       and moment-of-inertia floors through it, then applied the same guard to the remaining
#       divide-by-near-zero weaknesses that share the thin-section failure mode:
#         * np.mean(Izz), the bending-stress divisor in sig_1..sig_6: floored to EPS (Izz_mean), so
#           the bending stresses stay finite as Izz -> 0 (the loads() I floor does not cover this
#           raw mean);
#         * the panel-thickness divisors in the shear terms (tau* and tau*_T): floored copies
#           t1_div/t2_div/t3_div = max(t_p, EPS) are used ONLY as divisors, since t_p = rho_p*ts_p
#           can reach ~1e-7 for in-bounds-but-degenerate designs; the unfloored t1/t2/t3 still feed
#           the weights and core thickness, leaving that physics unchanged;
#         * the neutral-axis denominator of Y_bar: floored to EPS to prevent a 0/0 -> NaN when all
#           panels vanish together (a NaN would silently poison Izz, the stresses, and the weights).
#       All guards activate only for near-degenerate (effectively infeasible) sections; feasible
#       designs are unaffected.
#   - Clamped the per-station total elastic twist to a physical/mechanical ceiling
#       (twist = clip(twist, -THETA_TWIST_MAX_DEG, +THETA_TWIST_MAX_DEG), THETA_TWIST_MAX_DEG = 30).
#       The coupling response theta = deltaL_divby_q = sum(twist_deg * 0.1 * Spanel * 2) is the
#       twist-induced lift increment delta(L)/q (an effective area, not an angle), whose only
#       physically variable driver is the twist angle. The linear small-angle structural model is
#       valid only for modest twist; real wash-in/out is a few degrees and the hard aeroelastic
#       ceiling (torsional divergence / control reversal / material yield) sits at order ~10-15 deg.
#       The 30 deg cap is a deliberately generous bound that leaves feasible designs untouched while
#       excluding the non-physical model-breakdown values (e.g. ~8000) that thin near-degenerate
#       sections produced even after the Phi clamp and the I floor. With this cap
#       |theta| <= 0.1 * 30 * S_ref(<=800) ~ 2400, which is the basis for the widened wing_twist
#       scaler range in InputFile.py.
#   - Added explanatory inline comments and physical units (e.g. [ft], [lb], [lb/ft^2], [deg], [-])
#       to the design variables, reconstructed quantities, loads, stresses, weights, and twist
#       throughout, and completed the Google-style docstrings with per-argument/return units.
"""Response calculation module for SSBJ Subsystem 3 (Structures).

This module provides structural analysis calculations for the
Supersonic Business Jet (SSBJ) problem.
"""

import numpy as np 
from typing import List

# Common small positive floor used throughout this module to guard divisions and reciprocals
# against near-degenerate (effectively infeasible) sections, where a vanishing section depth,
# inertia, or panel thickness would otherwise drive a divisor to zero and blow up (or NaN-poison)
# the responses. Shared by the h_spar floor, the moment-of-inertia floor in loads(), the mean(Izz)
# bending-stress divisor, the panel-thickness shear divisors, and the Y_bar denominator guard.
EPS = 1E-5

# Physical/mechanical ceiling on the per-station elastic wing twist (degrees), used to bound the
# aeroelastic lift increment theta = deltaL_divby_q = sum(twist * Spanel * 0.1 * 2). The linear
# small-angle Bredt-Batho + beam-bending model is only valid for modest twist; real wash-in/out is
# a few degrees and the hard aeroelastic ceiling (torsional divergence / control reversal / yield)
# sits at order ~10-15 deg, so 30 deg is a deliberately generous cap that excludes only the
# non-physical model-breakdown blow-ups produced for near-degenerate thin sections. With this cap
# |theta| <= 0.1 * 30 * S_ref(<=800) ~ 2400, which sets the wing_twist scaler range in InputFile.py.
THETA_TWIST_MAX_DEG = 30.0


def Wing_Mod(taper_ratio: float, thickness_to_chord_ratio: float, wing_sweep_angle: float, wing_aspect_ratio: float, wing_surface_area: float, tail_aspect_ratio: float, tail_surface_area: float):
    """Calculate wing geometry parameters.

    Args:
        taper_ratio: Wing taper ratio [-].
        thickness_to_chord_ratio: Wing thickness-to-chord ratio [-].
        wing_sweep_angle: Wing sweep angle [deg].
        wing_aspect_ratio: Wing aspect ratio [-].
        wing_surface_area: Wing reference surface area [ft^2].
        tail_aspect_ratio: Horizontal tail aspect ratio [-].
        tail_surface_area: Horizontal tail reference surface area [ft^2].

    Returns:
        Tuple of (c, c_box, Sweep_40, D_mx, b, l): c section chords [ft],
        c_box structural box chord [ft], Sweep_40 sweep at 40% chord [deg],
        D_mx load-line-to-shear-center offset [ft], b wing span [ft],
        l torsion moment arm [ft].
    """
    c = [0, 0, 0, 0]
    x = [0] * 8
    y = [0] * 8
    
    b = max(2, np.real(np.sqrt(wing_aspect_ratio * wing_surface_area)))  # wing span [ft]
    c[0] = 2 * wing_surface_area / ((1 + taper_ratio) * b)  # root chord [ft]
    c[3] = taper_ratio * c[0]  # tip chord [ft]
    x[0] = 0
    y[0] = 0
    x[1] = c[0]
    y[1] = 0
    x[6] = (b / 2) * np.tan(wing_sweep_angle * np.pi / 180)
    y[6] = b / 2
    x[7] = x[6] + c[3]
    y[7] = b / 2
    y[2] = b / 6
    x[2] = (x[6] / y[6]) * y[2]
    y[4] = b / 3
    x[4] = (x[6] / y[6]) * y[4]
    x[5] = x[7] + ((x[1] - x[7]) / y[7]) * (y[7] - y[4])
    y[5] = y[4]
    x[3] = x[7] + ((x[1] - x[7]) / y[7]) * (y[7] - y[2])
    y[3] = y[2]
    c[1] = x[3] - x[2]  # chord at station 1 (b/6) [ft]
    c[2] = x[5] - x[4]  # chord at station 2 (b/3) [ft]
    TE_sweep = (np.arctan((x[7] - x[1]) / y[7])) * 180 / np.pi  # trailing-edge sweep [deg]
    Sweep_40 = (np.arctan(((x[7] - 0.6 * (x[7] - x[6])) - 0.4 * x[1]) / y[7])) * 180 / np.pi  # sweep at 40% chord [deg]

    l = np.multiply([c[i] for i in range(3)], 0.4 * np.cos(wing_sweep_angle * np.pi / 180))  # noqa: E741  # torsion moment arm per station [ft]
    k = np.multiply([c[i] for i in range(3)], 0.6 * np.sin((90 - TE_sweep) * np.pi / 180) / 
                    np.sin((90 + TE_sweep - wing_sweep_angle) * np.pi / 180))  # aft box-chord contribution per station [ft]
    c_box = np.add(l, k)  # structural box chord per station [ft]
    D_mx = np.subtract(l, np.multiply(0.407, c_box))  # load-line-to-shear-center offset per station [ft]

    return c, c_box, Sweep_40, D_mx, b, l
    
def loads(b, c, Sweep_40, D_mx, L, Izz, E):
    """Calculate load distribution and structural response.

    Args:
        b: Wing span [ft].
        c: Section chord lengths [ft].
        Sweep_40: Sweep angle at 40% chord [deg].
        D_mx: Load-line-to-shear-center offset [ft].
        L: Total lift force [lb].
        Izz: Section second moment of area distribution [ft^4].
        E: Young's modulus [lb/ft^2].

    Returns:
        Tuple of (P, Mz, Mx, bend_twist, Spanel): P shear force [lb],
        Mz bending moment [lb-ft], Mx torsion moment [lb-ft],
        bend_twist bending twist [deg], Spanel panel area [ft^2].
    """
    NP = 9
    n = 90
    rn = n // NP 
    
    h = (b / 2) / n  # spanwise integration step [ft]
    x = np.linspace(0, b / 2 - h, n)
    x1 = np.linspace(h, b / 2, n)

    # Calculate wing loading
    l = np.linspace(0, (b / 2) - (b / 2) / NP, NP)  # noqa: E741
    c1mc4 = c[0] - c[3]
    f_all = np.multiply((3 * b / 10), np.sqrt(np.subtract(1, np.power(x, 2) / 
                        np.power(np.divide(b, 2), 2))))
    f1_all = np.multiply((3 * b / 10), np.sqrt(np.subtract(1, np.power(x1, 2) / 
                            np.power(np.divide(b, 2), 2))))
    C = c[3] + 2 * ((b / 2 - x) / b) * c1mc4
    C1 = c[3] + 2 * ((b / 2 - x1) / b) * c1mc4
    A_Tot = np.multiply((h / 4) * (C + C1), (np.add(f_all, f1_all)))
    Area = np.sum(A_Tot.reshape((NP, rn)), axis=1)
    Spanel = np.multiply((h * rn / 2), (np.add([C[int(i)] for i in np.linspace(0, n - 10, 9)], 
                                [C[int(i)] for i in np.linspace(9, n - 1, 9)])))

    # Calculate sweep angles
    cosSweep = np.cos(Sweep_40 * np.pi / 180)
    cosInvSweep = 1 / cosSweep
    tanCos2Sweep = np.tan(Sweep_40 * np.pi / 180) * cosSweep * cosSweep
    
    # Calculate distributed loads
    p = np.divide(L * Area, sum(Area))  # distributed lift per panel [lb]
    
    # Calculate shear force and bending moment
    Tcsp = np.cumsum(p)
    Tsp = Tcsp[-1]
    temp = [0] + [Tcsp[i] for i in range(len(Tcsp) - 1)]
    T = np.subtract(Tsp, temp)
    pl = np.multiply(p, l)
    Tcspl = np.cumsum(pl)
    Tspl = Tcspl[-1]
    Mb = np.multiply(np.subtract(np.subtract(Tspl, Tcspl), 
                                    np.multiply(l, np.subtract(Tsp, Tcsp))), cosInvSweep)

    # Extract loads at specific points
    P = [T[int(i)] for i in np.arange(0, NP - 1, int(NP / 3))]  # shear force [lb]
    Mx = np.multiply(P, D_mx)  # torsion moment [lb-ft]
    Mz = [Mb[int(i)] for i in np.arange(0, NP - 1, int(NP / 3))]  # bending moment [lb-ft]

    # Calculate wing twist due to bending
    I = np.zeros((NP))  # noqa: E741
    chord = c[3] + (np.divide(2 * (b / 2 - l), b)) * c1mc4
    y = np.zeros((2, 9))
    y[0, :] = (l - 0.4 * chord * tanCos2Sweep) * cosInvSweep
    y[1, :] = (l + 0.6 * chord * tanCos2Sweep) * cosInvSweep
    y[1, 0] = 0
    
    I[0:int(NP / 3)] = np.sqrt((Izz[0]**2 + Izz[1]**2) / 2)
    I[int(NP / 3):int(2 * NP / 3)] = np.sqrt((Izz[1]**2 + Izz[2]**2) / 2)
    I[int(2 * NP / 3):int(NP)] = np.sqrt((Izz[2]**2) / 2)

    # MODIFIED: floor the section moment of inertia to the common EPS (analogous to the
    # h_spar = max(h_spar, EPS) guard in calculate_structural_responses). I appears only as a
    # divisor in A, B, Slope_A, Slope_B below, so as Izz -> 0 for a near-degenerate (thin-skin)
    # section the bending twist bend_twist ~ 1/I diverges. Unlike the torsion term Phi, bend_twist
    # is not otherwise bounded, so this floor caps it and prevents the wing_twist (theta) blow-up.
    I = np.maximum(I, EPS)  # noqa: E741

    La = y[0, 1:NP] - y[0, 0:NP - 1]
    La = np.append(0, La)
    Lb = y[1, 1:NP] - y[1, 0:NP - 1]
    Lb = np.append(0, Lb)
    
    A = T * La**3 / (3 * E * I) + Mb * La**2 / (2 * E * I)
    B = T * Lb**3 / (3 * E * I) + Mb * Lb**2 / (2 * E * I)
    Slope_A = T * La**2 / (2 * E * I) + Mb * La / (E * I)
    Slope_B = T * Lb**2 / (2 * E * I) + Mb * Lb / (E * I)

    for i in range(NP - 1):
        Slope_A[i + 1] = Slope_A[i] + Slope_A[i + 1]
        Slope_B[i + 1] = Slope_B[i] + Slope_B[i + 1]
        A[i + 1] = A[i] + Slope_A[i] * La[i + 1] + A[i + 1]
        B[i + 1] = B[i] + Slope_B[i] * Lb[i + 1] + B[i + 1]

    bend_twist = ((B - A) / chord) * 180 / np.pi  # bending-induced twist [deg]
    
    # Ensure twist is non-decreasing
    for i in range(1, len(bend_twist)):
        if bend_twist[i] < bend_twist[i - 1]:
            bend_twist[i] = bend_twist[i - 1]
    
    return P, Mz, Mx, bend_twist, Spanel


def calculate_structural_responses(taper_ratio: float, alpha1: List[float], alpha3: List[float], ts2: List[float], rho1: List[float], rho2: List[float], rho3: List[float], thickness_to_chord_ratio: float, wing_sweep_angle: float, wing_aspect_ratio: float, wing_surface_area: float, tail_aspect_ratio: float, tail_surface_area: float, lift: float, h: float):
    """Calculate structural weights, twist, and constraint intermediate values in one pass.

    The skin/sandwich thicknesses arrive in the *depth-relative* parametrization
    (see ``SubSystem3_Reformulation.md``) and are reconstructed internally:

      * ``ts1 = 2*alpha1*D`` and ``ts3 = 2*alpha3*D`` (top/bottom sandwich), where the available
        structural depth ``D = beta*(t/c)*chord`` is rebuilt locally, so the spar-height margin
        becomes the linear, division-free relation ``h_spar = D*(1 - alpha1 - alpha3)``;
      * ``ts2`` is the web sandwich thickness, kept absolute (inches), because the web does not set
        ``h_spar``;
      * ``t_p = rho_p*ts_p`` (skin as a fraction of its own sandwich), so the core thickness
        ``ts_p - t_p = ts_p*(1 - rho_p)`` is non-negative whenever ``rho_p <= 1``.

    Args:
        taper_ratio: Wing taper ratio [-].
        alpha1: Length-3 top-sandwich depth fractions [-] (per spanwise station); ``ts1 = 2*alpha1*D``.
        alpha3: Length-3 bottom-sandwich depth fractions [-]; ``ts3 = 2*alpha3*D``.
        ts2: Length-3 web sandwich thicknesses [in] (absolute).
        rho1: Length-3 top skin ratios [-]; ``t1 = rho1*ts1``.
        rho2: Length-3 web skin ratios [-]; ``t2 = rho2*ts2``.
        rho3: Length-3 bottom skin ratios [-]; ``t3 = rho3*ts3``.
        thickness_to_chord_ratio: Wing thickness-to-chord ratio [-].
        wing_sweep_angle: Wing sweep angle [deg].
        wing_aspect_ratio: Wing aspect ratio [-].
        wing_surface_area: Wing reference surface area [ft^2].
        tail_aspect_ratio: Horizontal tail aspect ratio [-].
        tail_surface_area: Horizontal tail reference surface area [ft^2].
        lift: Total lift force [lb].
        h: Altitude [ft] (unused; see note below).

    Returns:
        Tuple of (C_structure_flat, t_ft, ts_ft, hspar_margin, Ws, Wf, theta), where ``t_ft`` and
        ``ts_ft`` are the reconstructed skin/sandwich thicknesses in feet [ft] (9 values each, ordered
        panel 1/2/3), ``hspar_margin = alpha1 + alpha3 - 0.5`` [-] (3 values, one per station) is the
        linear h_spar-margin constraint quantity, ``Ws`` is the structural weight [lb], ``Wf`` the
        fuel weight [lb], and ``theta`` the twist-induced lift increment delta(L)/q [ft^2] (an
        effective area, NOT an angle).
    """

    C = [500.0, 16000.0, 4.0, 4360.0, 0.01375, 1.0]  # model constants: C[0] base fuel weight [lb], C[1] base structural weight [lb], C[2] ultimate load factor [-]
    beta = 0.9                     # structural box depth fraction of (t/c)*chord [-]
    E = 10600000.0 * 144.0         # Young's modulus [lb/ft^2] (10.6e6 psi * 144 in^2/ft^2)
    G = 4000000 * 144              # shear modulus [lb/ft^2] (4.0e6 psi * 144 in^2/ft^2)
    nu = 0.3                       # Poisson's ratio [-]
    rho_alum = 0.1 * 144           # skin (aluminum) material density [lb/ft^3]
    rho_core = 0.1 * 144 / 10      # sandwich core material density [lb/ft^3]
    rho_fuel = 6.5 * 7.4805        # fuel density [lb/ft^3] (6.5 lb/gal * 7.4805 gal/ft^3)
    Fw_at_t = 5.0                  # fuselage width at the tail [ft]

    # MODIFIED: the altitude `h` parameter is intentionally unused. In the original DMDO
    # WingDesignAnalyzer, altitude (self.h / Z[1]) is never used in the structural-response
    # physics (Ws, Wf, theta); it only appeared in calculate_constraints() via a variable-
    # shadowing bug where the local spar-height variable was also named `h`. That bug was
    # corrected in this port (h_spar is used consistently), so altitude has no remaining
    # use here. The parameter is kept for interface symmetry with the other subsystems.

    # Convert thickness from inches to feet (matching reference implementation)
    # MODIFIED (reformulation): the skin/sandwich thicknesses are no longer passed as absolute
    # inches. They arrive in the depth-relative parametrization (alpha1, alpha3, ts2, rho1, rho2,
    # rho3) and are reconstructed below, AFTER the wing geometry, because the reconstruction needs
    # the chord-derived structural depth D.

    # Wing geometry (once) -- moved AHEAD of the thickness construction: the reconstruction of the
    # depth-relative sandwich thicknesses needs the chords c[0:3].
    c, c_box, Sweep_40, D_mx, b, a = Wing_Mod(taper_ratio, thickness_to_chord_ratio, wing_sweep_angle, wing_aspect_ratio, wing_surface_area, tail_aspect_ratio, tail_surface_area)

    # Available structural box depth per spanwise station (feet); beta = 0.9 (defined above).
    D = beta * float(thickness_to_chord_ratio) * np.array([c[i] for i in range(3)])

    # Reconstruct the physical thicknesses (all in FEET, matching the original post-conversion units):
    #   ts1 = 2*alpha1*D, ts3 = 2*alpha3*D : top/bottom sandwich scale with the box depth, so the
    #                                        spar-height margin becomes linear (see h_spar below);
    #   ts2 (web)                          : absolute, converted inches -> feet like the original;
    #   t_p = rho_p*ts_p                   : skin as a fraction of its own sandwich, so the core
    #                                        ts_p - t_p = ts_p*(1 - rho_p) >= 0 whenever rho_p <= 1.
    alpha1 = np.asarray(alpha1, dtype=float)
    alpha3 = np.asarray(alpha3, dtype=float)
    rho1   = np.asarray(rho1, dtype=float)
    rho2   = np.asarray(rho2, dtype=float)
    rho3   = np.asarray(rho3, dtype=float)

    ts1 = 2.0 * alpha1 * D                       # top sandwich thickness [ft]
    ts3 = 2.0 * alpha3 * D                       # bottom sandwich thickness [ft]
    ts2 = np.asarray(ts2, dtype=float) / 12.0   # web sandwich thickness [ft] (inches -> feet)
    t1  = rho1 * ts1                             # top skin thickness [ft]
    t2  = rho2 * ts2                             # web skin thickness [ft]
    t3  = rho3 * ts3                             # bottom skin thickness [ft]

    # Spar (web) height -- now an exact, division-free function of the depth fractions:
    #   h_spar = D - 0.5(ts1 + ts3) = D*(1 - alpha1 - alpha3).
    # In the feasible region (alpha1 + alpha3 <= 0.5) this is >= 0.5*D > 0, so the negative /
    # near-zero h_spar failure mode of the original formulation cannot occur there.
    h_spar = D * (1.0 - alpha1 - alpha3)

    # MODIFIED (retained from the pre-reformulation port): floor the spar height to a small positive
    # value. With the depth-relative parametrization h_spar >= 0 structurally (alpha-sum <= 1) and
    # >= 0.5*D in the feasible region, so this floor NEVER activates for a feasible design. It is
    # kept purely to guard the single infeasible box corner alpha1 = alpha3 = 0.5 (where h_spar = 0
    # exactly), which the optimizer may still evaluate, preventing an exact divide-by-zero downstream.
    h_spar = np.maximum(h_spar, EPS)

    # Linear h_spar-margin constraint quantity (replaces the original division-based G1[42:45]):
    #   alpha1 + alpha3 - 0.5 <= 0  <=>  ts1 + ts3 <= D  <=>  0.5(ts1 + ts3) <= h_spar.
    # Returned to Analysis3, which places it at responses[93:96] for LocalConstraints3 to read.
    hspar_margin = alpha1 + alpha3 - 0.5

    A_top    = (np.multiply(t1, 0.5 * c_box)) + (np.multiply(t2, h_spar / 6))  # top cap effective area [ft^2]
    A_bottom = (np.multiply(t3, 0.5 * c_box)) + (np.multiply(t2, h_spar / 6))  # bottom cap effective area [ft^2]
    # MODIFIED: guard the neutral-axis denominator. If all panels go thin together A_top and
    # A_bottom both -> 0, so 2*A_top + 2*A_bottom -> 0 and Y_bar becomes 0/0 = NaN, which would
    # poison Izz, every sig_*, and the weights. Flooring the denominator to EPS keeps Y_bar finite.
    Y_bar    = np.multiply(h_spar, np.divide((2 * A_top), np.maximum(2 * A_top + 2 * A_bottom, EPS)))  # neutral-axis height [ft]
    Izz      = (np.multiply(2, np.multiply(A_top,    np.power((h_spar - Y_bar), 2))) +
                np.multiply(2, np.multiply(A_bottom, np.power((-Y_bar), 2))))  # section second moment of area [ft^4]

    # Loads (once)
    P, Mz, Mx, bend_twist, Spanel = loads(b, c, Sweep_40, D_mx, lift, Izz, E)
    Mz = np.array(Mz)
    P  = np.array(P)
    Mx = np.array(Mx)

    # Structural weights and twist
    Phi = (Mx / (4 * G * (c_box * h_spar)**2)) * (c_box / t1 + 2 * h_spar / t2 + c_box / t3)  # torsional twist [rad] (Bredt-Batho; strictly a per-unit-span rate used here as an angle)
    # MODIFIED: clamp the torsional twist contribution to +-180 deg. Phi (radians) scales like
    # 1/h_spar**2, so a near-degenerate (infeasible) section depth drives the converted
    # contribution Phi*180/pi far past +-180 deg, which is non-physical for this linear small-angle
    # model and can overflow `theta` downstream. Clipping Phi to +-pi rad caps the contribution at
    # +-180 deg without affecting feasible designs (where |Phi| stays small).
    Phi = np.clip(Phi, -np.pi, np.pi)
    aa = len(bend_twist)
    twist = np.zeros(aa)  # MODIFIED: was `twist = np.array([0] * aa)`, which created an integer array that truncated the float twist values assigned below
    twist[0:int(aa/3)]           = bend_twist[0:int(aa/3)]           + Phi[0] * 180 / np.pi
    twist[int(aa/3):int(aa*2/3)] = bend_twist[int(aa/3):int(aa*2/3)] + Phi[1] * 180 / np.pi
    twist[int(aa*2/3):aa]        = bend_twist[int(aa*2/3):aa]        + Phi[2] * 180 / np.pi
    # MODIFIED: clamp the per-station total elastic twist (bend_twist + torsion contribution) to a
    # physical/mechanical ceiling before integrating it into theta = deltaL_divby_q. theta is the
    # twist-induced lift increment delta(L)/q = sum(twist_deg * 0.1 * Spanel * 2) (an effective
    # area, not an angle); its only physically variable driver is the twist angle. The linear
    # small-angle model breaks down past ~10-15 deg (torsional divergence / control reversal /
    # yield), so capping twist at +-THETA_TWIST_MAX_DEG keeps theta within the physically realizable
    # range and excludes the model-breakdown blow-ups from near-degenerate thin sections. Feasible
    # designs (modest twist) are unaffected.
    twist = np.clip(twist, -THETA_TWIST_MAX_DEG, THETA_TWIST_MAX_DEG)  # per-station elastic twist [deg]
    deltaL_divby_q = np.sum(twist * Spanel * 0.1 * 2)  # twist-induced lift increment delta(L)/q [ft^2] (effective area, not an angle)

    Wtop_alum    = (b / 4) * (c[0] + c[3]) * np.mean(t1) * rho_alum          # top skin weight [lb]
    Wbottom_alum = (b / 4) * (c[0] + c[3]) * np.mean(t3) * rho_alum          # bottom skin weight [lb]
    Wside_alum   = (b / 2) * np.mean(h_spar) * np.mean(t2) * rho_alum        # web skin weight [lb]
    Wtop_core    = (b / 4) * (c[0] + c[3]) * np.mean(ts1 - t1) * rho_core    # top core weight [lb]
    Wbottom_core = (b / 4) * (c[0] + c[3]) * np.mean(ts3 - t3) * rho_core    # bottom core weight [lb]
    Wside_core   = (b / 2) * np.mean(h_spar) * np.mean(ts2 - t2) * rho_core  # web core weight [lb]
    W_wingstruct = Wtop_alum + Wbottom_alum + Wside_alum + Wtop_core + Wbottom_core + Wside_core  # per-side wing structural weight [lb]
    W_fuel_wing  = np.mean(h_spar * 0.6 * c_box) * (b / 3) * 2 * rho_fuel    # wing-tank fuel weight [lb]

    Bh   = np.sqrt(tail_aspect_ratio * tail_surface_area)  # horizontal tail span [ft]
    W_ht = 3.316 * ((1 + (Fw_at_t / Bh))**-2.0) * ((lift * C[2] / 1000)**0.260) * (tail_surface_area**0.806)  # horizontal tail weight [lb]

    Wf    = C[0] + W_fuel_wing         # total fuel weight [lb]
    Ws    = C[1] + W_ht + 2 * W_wingstruct  # total structural weight [lb]
    theta = deltaL_divby_q             # coupling to aero: lift increment delta(L)/q [ft^2]

    # Constraint intermediate values
    teq1 = ((t1**3)/4 + (3*t1)*(ts1 - t1/2)**2)**(1/3)  # equivalent smeared thickness, top panel [ft]
    teq2 = ((t2**3)/4 + (3*t2)*(ts2 - t2/2)**2)**(1/3)  # equivalent smeared thickness, web panel [ft]
    teq3 = ((t3**3)/4 + (3*t3)*(ts3 - t3/2)**2)**(1/3)  # equivalent smeared thickness, bottom panel [ft]

    # MODIFIED: guard the mean section inertia used as the bending-stress divisor. As the skins get
    # thin Izz -> 0 (see the I floor in loads()), so np.mean(Izz) collapses and every sig_* below
    # diverges. Flooring it to EPS (Izz_mean) bounds the bending stresses for near-degenerate
    # sections; the raw Izz is left untouched everywhere else.
    Izz_mean = max(float(np.mean(Izz)), EPS)  # mean section inertia used as bending-stress divisor [ft^4]
    sig_1 = Mz * (0.95 * h_spar - h_spar * np.mean(t1)) / Izz_mean  # bending stress, point 1 [lb/ft^2]
    sig_2 = Mz * (h_spar     - h_spar * np.mean(t1)) / Izz_mean  # bending stress, point 2 [lb/ft^2]
    sig_3 = sig_1  # bending stress, point 3 [lb/ft^2]
    sig_4 = Mz * (0.05 * h_spar - h_spar * np.mean(t1)) / Izz_mean  # bending stress, point 4 [lb/ft^2]
    sig_5 = Mz * (-h_spar * np.mean(t1))                 / Izz_mean  # bending stress, point 5 [lb/ft^2]
    sig_6 = sig_4  # bending stress, point 6 [lb/ft^2]
    q     = Mx / (2 * c_box * h_spar)  # torsional shear flow [lb/ft]

    # Critical buckling stresses: sig_cr* normal, tau_cr* shear [lb/ft^2]
    sig_cr1 = (np.pi**2 * E * 4   / (12 * (1 - nu**2))) * (teq2 / (0.95 * h_spar))**2
    tau_cr1 = (np.pi**2 * E * 5.5 / (12 * (1 - nu**2))) * (teq2 / (0.95 * h_spar))**2
    sig_cr2 = (np.pi**2 * E * 4   / (12 * (1 - nu**2))) * (teq1 / c_box)**2
    tau_cr2 = (np.pi**2 * E * 5.5 / (12 * (1 - nu**2))) * (teq1 / c_box)**2
    sig_cr3 = sig_cr1;  tau_cr3 = tau_cr1
    sig_cr5 = (np.pi**2 * E * 4   / (12 * (1 - nu**2))) * (teq3 / c_box)**2
    tau_cr5 = (np.pi**2 * E * 5.5 / (12 * (1 - nu**2))) * (teq3 / c_box)**2

    # MODIFIED: floor the panel thicknesses used as divisors below (skin t1/t3, web t2). Under the
    # depth-relative parametrization t_p = rho_p*ts_p can reach ~1e-7 for in-bounds-but-degenerate
    # designs, so the shear terms q/t and T/(h_spar*t) blow up. These floored copies are used ONLY
    # as divisors here; the unfloored t1/t2/t3 still feed the weights and core thickness above, so
    # that physics is unchanged.
    t1_div = np.maximum(t1, EPS)
    t2_div = np.maximum(t2, EPS)
    t3_div = np.maximum(t3, EPS)

    T1      = P * (a / c_box)  # torsion-induced shear force, point 1 [lb]
    tau1_T  = T1 / (h_spar * t2_div)  # torsion shear stress contribution [lb/ft^2]
    tau1    = q / t2_div + tau1_T  # total shear stress, point 1 [lb/ft^2]
    sig_eq1 = np.sqrt(sig_1**2 + 3 * tau1**2)  # von Mises equivalent stress, point 1 [lb/ft^2]

    tau2    = q / t1_div  # total shear stress, point 2 [lb/ft^2]
    sig_eq2 = np.sqrt(sig_2**2 + 3 * tau2**2)  # von Mises equivalent stress, point 2 [lb/ft^2]

    T2      = P * (a / c_box)  # torsion-induced shear force, point 3 [lb]
    tau3_T  = -T2 / (h_spar * t2_div)  # torsion shear stress contribution [lb/ft^2]
    tau3    = q / t2_div + tau3_T  # total shear stress, point 3 [lb/ft^2]
    sig_eq3 = np.sqrt(sig_3**2 + 3 * tau3**2)  # von Mises equivalent stress, point 3 [lb/ft^2]

    tau4    = -q / t2_div + tau1_T  # total shear stress, point 4 [lb/ft^2]
    sig_eq4 = np.sqrt(sig_4**2 + 3 * tau4**2)  # von Mises equivalent stress, point 4 [lb/ft^2]

    tau5    = q / t3_div  # total shear stress, point 5 [lb/ft^2]
    sig_eq5 = np.sqrt(sig_5**2 + 3 * tau5**2)  # von Mises equivalent stress, point 5 [lb/ft^2]

    tau6    = -q / t2_div + tau3_T  # total shear stress, point 6 [lb/ft^2]
    sig_eq6 = np.sqrt(sig_6**2 + 3 * tau6**2)  # von Mises equivalent stress, point 6 [lb/ft^2]

    C_structure_flat = (sig_1.tolist() + sig_2.tolist() + sig_3.tolist() +
                        sig_4.tolist() + sig_5.tolist() + sig_6.tolist() +
                        sig_cr1.tolist() + tau_cr1.tolist() +
                        sig_cr2.tolist() + tau_cr2.tolist() +
                        sig_cr3.tolist() + tau_cr3.tolist() +
                        sig_cr5.tolist() + tau_cr5.tolist() +
                        tau1.tolist() + sig_eq1.tolist() +
                        tau2.tolist() + sig_eq2.tolist() +
                        tau3.tolist() + sig_eq3.tolist() +
                        sig_eq4.tolist() +
                        tau5.tolist() + sig_eq5.tolist() +
                        sig_eq6.tolist() +
                        h_spar.tolist())

    # Reconstructed thicknesses in feet, in the response layout consumed by LocalConstraints3
    # (responses[75:84] = t1,t2,t3 ; responses[84:93] = ts1,ts2,ts3).
    t_ft  = t1.tolist() + t2.tolist() + t3.tolist()
    ts_ft = ts1.tolist() + ts2.tolist() + ts3.tolist()

    return C_structure_flat, t_ft, ts_ft, hspar_margin.tolist(), Ws, Wf, theta

```
