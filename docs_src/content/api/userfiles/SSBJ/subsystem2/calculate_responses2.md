---
title: calculate_responses2
---

← Back to [subsystem2](index.md)

# calculate_responses2

**Source:** [userfiles\SSBJ\subsystem2\calculate_responses2.py](calculate_responses2_source.md)

Response calculation module for SSBJ Subsystem 2 (Aerodynamics).

This module provides aerodynamic calculations for the
Supersonic Business Jet (SSBJ) problem.

## Functions

??? abstract "poly_approx(S, S_new, flag, S_bound)"
    Second-order polynomial response-surface approximation (SSBJ surrogate).

    Fits a quadratic about the base point S and evaluates it at S_new,
    returning a dimensionless correction factor.
    NOTE: if S_new == S the normalized shift is zero and FF collapses to the
    constant term Ao (i.e. the factor becomes independent of the input).


    **Args:**
    > S: Base (reference) values.  
    > S_new: Evaluation-point values.  
    > flag: Per-variable slope/shape mode selector.  
    > S_bound: Per-variable bound used to fit the polynomial.  


    **Returns:**
    > FF: Dimensionless correction factor [-].  

??? abstract "calculate_drag_polar(tail_sweep_angle: float, wing_moment_arm: float, tail_moment_arm: float, thickness_to_chord_ratio: float, wing_sweep_angle: float, wing_aspect_ratio: float, wing_surface_area: float, tail_aspect_ratio: float, tail_surface_area: float, total_weight: float, engine_scale_factor: float, wing_twist: float, h: float, Mach: float)"
    Calculate the drag polar and related parameters.


    **Args:**
    > tail_sweep_angle: Horizontal tail sweep angle [deg].  
    > wing_moment_arm: Wing aerodynamic moment arm [ft].  
    > tail_moment_arm: Horizontal tail aerodynamic moment arm [ft].  
    > thickness_to_chord_ratio: Wing thickness-to-chord ratio [-].  
    > wing_sweep_angle: Wing sweep angle [deg].  
    > wing_aspect_ratio: Wing aspect ratio [-].  
    > wing_surface_area: Wing reference surface area [ft^2].  
    > tail_aspect_ratio: Horizontal tail aspect ratio [-].  
    > tail_surface_area: Horizontal tail reference surface area [ft^2].  
    > total_weight: Total aircraft weight [lb].  
    > engine_scale_factor: Engine scale factor, ESF [-].  
    > wing_twist: Wing twist / incidence angle [deg].  
    > h: Altitude [ft].  
    > Mach: Mach number [-].  


    **Returns:**
    > List containing [Lift [lb], Drag [lb], LDr [-], Pg [-],  
    > CLo_wing [-], CLo_tail [-]].  

