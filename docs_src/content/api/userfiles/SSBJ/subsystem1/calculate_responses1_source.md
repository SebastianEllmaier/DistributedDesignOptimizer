---
title: calculate_responses1 (Source)
---

← Back to [calculate_responses1 documentation](calculate_responses1.md)

# calculate_responses1 - Source Code

**File:** `userfiles\SSBJ\subsystem1\calculate_responses1.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Response calculation module for SSBJ Subsystem 1 (Propulsion).

This module provides propulsion-related calculations for the
Supersonic Business Jet (SSBJ) problem.

Attribution:
    This file contains code derived from the DMDO framework by Ahmed Bayoumy,
    originally published under the GNU Lesser General Public License v3.0.
    Ahmed H. Bayoumy, the copyright holder of the original code, has granted
    permission to distribute this derived file under the GNU Lesser General
    Public License v3.0.
    Source: https://github.com/Ahmed-Bayoumy/DMDO/blob/DEV/tests/SBJ/SSBJ_Propulsion.py
    Relevant original functions: calculate_tempe_throttleua(), SBJ_propulsion_analysis(),
    calculate_sfc(), calculate_esf(), calculate_engine_weight(), poly_approx()

    Modifications from the original:
        - Refactored from class SSBJPropulsion to standalone functions; removed
          auxiliary methods (SBJ_propulsion_opt(), print_results(), __init__()).
        - Constants, coefficients, and state variables are passed as function
          arguments instead of class attributes.
        - poly_approx() decoupled from instance state (self.R, self.h, etc.).
        - Added type hints to function signatures.
        - Added Google-style docstrings.
"""

import copy
import numpy as np


def poly_approx(S, S_new, flag, S_bound):
    """Calculate polynomial approximation for propulsion parameters.

    Args:
        S: Base values for normalization.
        S_new: New values to be normalized against base values.
        flag: Flags controlling the polynomial coefficient calculation mode.
        S_bound: Boundary values for the polynomial approximation.

    Returns:
        Scaled performance factor.
    """
    S_norm = []
    S_shifted = []
    Ai = []
    Aij = np.zeros((len(S), len(S)))
    
    R = np.array([
        [0.2736, 0.3970, 0.8152, 0.9230, 0.1108],
        [0.4252, 0.4415, 0.6357, 0.7435, 0.1138],
        [0.0329, 0.8856, 0.8390, 0.3657, 0.0019],
        [0.0878, 0.7248, 0.1978, 0.0200, 0.0169],
        [0.8955, 0.4568, 0.8075, 0.9239, 0.2525]
    ])
    
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
            Aij[i,i] = A[2]
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
            Aij[i,i] = A[2]
        
    # Calculate cross terms
    for i in range(len(S)):
        for j in range(i+1, len(S)):
            Aij[i, j] = Aij[i,i] * R[i,j]
            Aij[j, i] = Aij[i, j]
    
    S_shifted = np.array(S_shifted)
    
    # Calculate FF (Performance Factor)
    FF = Ao + np.dot(Ai, (np.transpose(S_shifted))) + \
            (1/2) * np.dot(np.dot(S_shifted, Aij), np.transpose(S_shifted))
    
    return FF
    
def calculate_specific_fuel_consumption(dim_throttle: float, h: float, Mach: float):
    """Calculate Specific Fuel Consumption (SFC).

    Args:
        dim_throttle: Dimensional throttle setting [lb].
        h: Altitude in feet [ft].
        Mach: Mach number [-].

    Returns:
        Specific fuel consumption value [1/hr].
    """
    
    s = [1.13238425638512, 1.53436586044561, -0.00003295564466, 
                 -0.00016378694115, -0.31623315541888, 0.00000410691343, 
                 -0.00005248000590, -0.00000000008574, 0.00000000190214, 
                 0.00000001059951]
    
    
    return (s[0] + s[1]*Mach + s[2]*h + s[3]*dim_throttle + \
            s[4]*Mach**2 + 2*h*Mach*s[5] + 2*dim_throttle*Mach*s[6] + \
            s[7]*h**2 + 2*dim_throttle*h*s[8] + s[9]*dim_throttle**2)
    
def calculate_engine_scale_factor(drag: float, dim_throttle: float):
    """Calculate Engine Specific Force (ESF).

    Args:
        drag: Total drag force [lb].
        dim_throttle: Dimensional throttle setting [lb].

    Returns:
        Engine scale factor [-].
    """
    
    return (drag / 2) / dim_throttle
    
def calculate_engine_weight(engine_scale_factor: float):
    """Calculate engine weight based on ESF.

    Args:
        engine_scale_factor: Engine scale factor [-].

    Returns:
        Engine weight [lb].
    """
    
    return 4360.0 * (engine_scale_factor**1.05) * 2
    
def calculate_engine_temperature(drag:float, throttle: float, h: float, Mach: float):
    """Calculate engine temperature and throttle adjustment.

    Reproduces the original DMDO SSBJ propulsion logic, which normalizes the
    (non-dimensional) throttle design variable against the drag reference in
    the polynomial approximation.

    Args:
        drag: Total drag force [lb].
        throttle: Throttle setting (non-dimensional design variable) [-].
        h: Altitude in feet [ft].
        Mach: Mach number [-].

    Returns:
        Engine temperature scaling factor [-].
    """
    
    engine_temperature = poly_approx([Mach, h, drag], [Mach, h, throttle], [2, 4, 2],\
                                   [.25, .25, .25])
    return engine_temperature
    
def calculate_throttle_uA(h: float, Mach: float):
    """Calculate upper-bound throttle value.

    Args:
        h: Altitude in feet [ft].
        Mach: Mach number [-].

    Returns:
        Upper-bound throttle value [lb].
    """
    
    p = [11483.7822254806, 10856.2163466548, -0.5080237941, 
                 3200.157926969, -0.1466251679, 0.0000068572]
        
    throttle_uA = p[0] + p[1]*Mach + p[2]*h + p[3]*Mach**2 + \
                  2*p[4]*Mach*h + p[5]*h**2
                  
    return throttle_uA
```
