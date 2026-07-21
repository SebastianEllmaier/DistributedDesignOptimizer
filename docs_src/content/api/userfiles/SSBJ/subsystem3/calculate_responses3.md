---
title: calculate_responses3
---

← Back to [subsystem3](index.md)

# calculate_responses3

**Source:** [userfiles\SSBJ\subsystem3\calculate_responses3.py](calculate_responses3_source.md)

Response calculation module for SSBJ Subsystem 3 (Structures).

This module provides structural analysis calculations for the
Supersonic Business Jet (SSBJ) problem.

## Functions

??? abstract "Wing_Mod(taper_ratio: float, thickness_to_chord_ratio: float, wing_sweep_angle: float, wing_aspect_ratio: float, wing_surface_area: float, tail_aspect_ratio: float, tail_surface_area: float)"
    Calculate wing geometry parameters.


    **Args:**
    > taper_ratio: Wing taper ratio [-].  
    > thickness_to_chord_ratio: Wing thickness-to-chord ratio [-].  
    > wing_sweep_angle: Wing sweep angle [deg].  
    > wing_aspect_ratio: Wing aspect ratio [-].  
    > wing_surface_area: Wing reference surface area [ft^2].  
    > tail_aspect_ratio: Horizontal tail aspect ratio [-].  
    > tail_surface_area: Horizontal tail reference surface area [ft^2].  


    **Returns:**
    > Tuple of (c, c_box, Sweep_40, D_mx, b, l): c section chords [ft],  
    > c_box structural box chord [ft], Sweep_40 sweep at 40% chord [deg],  
    > D_mx load-line-to-shear-center offset [ft], b wing span [ft],  
    > l torsion moment arm [ft].  

??? abstract "loads(b, c, Sweep_40, D_mx, L, Izz, E)"
    Calculate load distribution and structural response.


    **Args:**
    > b: Wing span [ft].  
    > c: Section chord lengths [ft].  
    > Sweep_40: Sweep angle at 40% chord [deg].  
    > D_mx: Load-line-to-shear-center offset [ft].  
    > L: Total lift force [lb].  
    > Izz: Section second moment of area distribution [ft^4].  
    > E: Young's modulus [lb/ft^2].  


    **Returns:**
    > Tuple of (P, Mz, Mx, bend_twist, Spanel): P shear force [lb],  
    > Mz bending moment [lb-ft], Mx torsion moment [lb-ft],  
    > bend_twist bending twist [deg], Spanel panel area [ft^2].  

??? abstract "calculate_structural_responses(taper_ratio: float, alpha1: List[float], alpha3: List[float], ts2: List[float], rho1: List[float], rho2: List[float], rho3: List[float], thickness_to_chord_ratio: float, wing_sweep_angle: float, wing_aspect_ratio: float, wing_surface_area: float, tail_aspect_ratio: float, tail_surface_area: float, lift: float, h: float)"
    Calculate structural weights, twist, and constraint intermediate values in one pass.

    The skin/sandwich thicknesses arrive in the *depth-relative* parametrization
    (see ``SubSystem3_Reformulation.md``) and are reconstructed internally:

    * ``ts1 = 2*alpha1*D`` and ``ts3 = 2*alpha3*D`` (top/bottom sandwich), where the available
    structural depth ``D = beta*(t/c)*chord`` is rebuilt locally, so the spar-height margin
    becomes the linear, division-free relation ``h_spar = D*(1 - alpha1 - alpha3)``;
    * ``ts2`` is the web sandwich thickness, kept absolute (inches), because the web does not set
    ``h_spar``;
    * ``t_p = rho_p*ts_p`` (skin as a fraction of its own sandwich), so the core thickness
    ``ts_p - t_p = ts_p*(1 - rho_p)`` is non-negative whenever ``rho_p <= 1``.


    **Args:**
    > taper_ratio: Wing taper ratio [-].  
    > alpha1: Length-3 top-sandwich depth fractions [-] (per spanwise station); ``ts1 = 2*alpha1*D``.  
    > alpha3: Length-3 bottom-sandwich depth fractions [-]; ``ts3 = 2*alpha3*D``.  
    > ts2: Length-3 web sandwich thicknesses [in] (absolute).  
    > rho1: Length-3 top skin ratios [-]; ``t1 = rho1*ts1``.  
    > rho2: Length-3 web skin ratios [-]; ``t2 = rho2*ts2``.  
    > rho3: Length-3 bottom skin ratios [-]; ``t3 = rho3*ts3``.  
    > thickness_to_chord_ratio: Wing thickness-to-chord ratio [-].  
    > wing_sweep_angle: Wing sweep angle [deg].  
    > wing_aspect_ratio: Wing aspect ratio [-].  
    > wing_surface_area: Wing reference surface area [ft^2].  
    > tail_aspect_ratio: Horizontal tail aspect ratio [-].  
    > tail_surface_area: Horizontal tail reference surface area [ft^2].  
    > lift: Total lift force [lb].  
    > h: Altitude [ft] (unused; see note below).  


    **Returns:**
    > Tuple of (C_structure_flat, t_ft, ts_ft, hspar_margin, Ws, Wf, theta), where ``t_ft`` and  
    > ``ts_ft`` are the reconstructed skin/sandwich thicknesses in feet [ft] (9 values each, ordered  
    > panel 1/2/3), ``hspar_margin = alpha1 + alpha3 - 0.5`` [-] (3 values, one per station) is the  
    > linear h_spar-margin constraint quantity, ``Ws`` is the structural weight [lb], ``Wf`` the  
    > fuel weight [lb], and ``theta`` the twist-induced lift increment delta(L)/q [ft^2] (an  
    > effective area, NOT an angle).  

