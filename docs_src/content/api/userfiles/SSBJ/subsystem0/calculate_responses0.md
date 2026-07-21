---
title: calculate_responses0
---

← Back to [subsystem0](index.md)

# calculate_responses0

**Source:** [userfiles\SSBJ\subsystem0\calculate_responses0.py](calculate_responses0_source.md)

Response calculation module for SSBJ Subsystem 0 (Aircraft).

This module provides the range calculation for the aircraft subsystem
of the Supersonic Business Jet (SSBJ) problem.

## Functions

??? abstract "calculate_range(specific_fuel_consumption: float, lift_to_drag_ratio: float, total_weight: float, fuel_weight: float, h: float, Mach: float) → float"
    Calculate the aircraft range using the Breguet range equation.


    **Args:**
    > specific_fuel_consumption: Specific fuel consumption coefficient [1/hr].  
    > lift_to_drag_ratio: Lift-to-drag ratio [-].  
    > total_weight: Total aircraft weight [lb].  
    > fuel_weight: Fuel weight [lb].  
    > h: Altitude in feet [ft].  
    > Mach: Mach number [-].  


    **Returns:**
    > Range in nautical miles [nmi].  

