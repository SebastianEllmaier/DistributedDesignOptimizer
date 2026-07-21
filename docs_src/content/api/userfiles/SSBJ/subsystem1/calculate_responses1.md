---
title: calculate_responses1
---

← Back to [subsystem1](index.md)

# calculate_responses1

**Source:** [userfiles\SSBJ\subsystem1\calculate_responses1.py](calculate_responses1_source.md)

Response calculation module for SSBJ Subsystem 1 (Propulsion).

This module provides propulsion-related calculations for the
Supersonic Business Jet (SSBJ) problem.

## Functions

??? abstract "poly_approx(S, S_new, flag, S_bound)"
    Calculate polynomial approximation for propulsion parameters.


    **Args:**
    > S: Base values for normalization.  
    > S_new: New values to be normalized against base values.  
    > flag: Flags controlling the polynomial coefficient calculation mode.  
    > S_bound: Boundary values for the polynomial approximation.  


    **Returns:**
    > Scaled performance factor.  

??? abstract "calculate_specific_fuel_consumption(dim_throttle: float, h: float, Mach: float)"
    Calculate Specific Fuel Consumption (SFC).


    **Args:**
    > dim_throttle: Dimensional throttle setting [lb].  
    > h: Altitude in feet [ft].  
    > Mach: Mach number [-].  


    **Returns:**
    > Specific fuel consumption value [1/hr].  

??? abstract "calculate_engine_scale_factor(drag: float, dim_throttle: float)"
    Calculate Engine Specific Force (ESF).


    **Args:**
    > drag: Total drag force [lb].  
    > dim_throttle: Dimensional throttle setting [lb].  


    **Returns:**
    > Engine scale factor [-].  

??? abstract "calculate_engine_weight(engine_scale_factor: float)"
    Calculate engine weight based on ESF.


    **Args:**
    > engine_scale_factor: Engine scale factor [-].  


    **Returns:**
    > Engine weight [lb].  

??? abstract "calculate_engine_temperature(drag: float, throttle: float, h: float, Mach: float)"
    Calculate engine temperature and throttle adjustment.

    Reproduces the original DMDO SSBJ propulsion logic, which normalizes the
    (non-dimensional) throttle design variable against the drag reference in
    the polynomial approximation.


    **Args:**
    > drag: Total drag force [lb].  
    > throttle: Throttle setting (non-dimensional design variable) [-].  
    > h: Altitude in feet [ft].  
    > Mach: Mach number [-].  


    **Returns:**
    > Engine temperature scaling factor [-].  

??? abstract "calculate_throttle_uA(h: float, Mach: float)"
    Calculate upper-bound throttle value.


    **Args:**
    > h: Altitude in feet [ft].  
    > Mach: Mach number [-].  


    **Returns:**
    > Upper-bound throttle value [lb].  

