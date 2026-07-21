---
title: HessianApproximationBFGS
---

← Back to [tools](index.md)

# HessianApproximationBFGS

**Source:** [Distributed_Design_Optimizer\subsystem\tools\HessianApproximationBFGS.py](HessianApproximationBFGS_source.md)

BFGS Hessian approximation module.

This module provides BFGS-based Hessian approximation for
optimization algorithms.

## Classes

### HessianApproximationBFGS

> **Inherits from:** `BFGS`

> A HessianApproximationBFGS object extends the scipy BFGS Hessian update strategy.

> It tracks previous design variables and gradients, enabling incremental
> Hessian approximation updates from absolute (current) values rather than deltas.


> **Args:**
> > exception_strategy (str): Strategy when curvature condition is violated  
> > ('skip_update' or 'damp_update').  
> > min_curvature (float | None): Minimum curvature threshold.  
> > init_scale (float | str): Initialization scale for the Hessian matrix.

#### Methods

??? abstract "__init__(self, exception_strategy: str, min_curvature: float | None, init_scale: float | str) → None"
    Creates a new instance of HessianApproximationBFGS.


    **Args:**
    > exception_strategy (str): Strategy when curvature condition is violated  
    > ('skip_update' or 'damp_update').  
    > min_curvature (float | None): Minimum curvature threshold.  
    > init_scale (float | str): Initialization scale for the Hessian matrix.  

??? abstract "get_Previous_X(self) → List[float] | None"
    Returns the previous design variable vector.


    **Returns:**
    > List[float] | None: the previous design variable vector  

??? abstract "set_Previous_X(self, previous_x_in: List[float]) → None"
    Sets the previous design variable vector.


    **Args:**
    > previous_x_in (List[float]): the previous design variable vector  

??? abstract "get_Previous_G(self) → List[float] | None"
    Returns the previous gradient vector.


    **Returns:**
    > List[float] | None: the previous gradient vector  

??? abstract "set_Previous_G(self, previous_g_in: List[float]) → None"
    Sets the previous gradient vector.


    **Args:**
    > previous_g_in (List[float]): the previous gradient vector  

??? abstract "check_CurvatureConditionViolation(self, delta_x: List[float], delta_g: List[float]) → bool"
    Check if the curvature condition of BFGS is triggered.

    This also happens in the function update of scipy.optimize.BFGS.
    The logic is based on the check in _update_implementation in
    scipy.optimize.BFGS.
    Source: https://github.com/scipy/scipy/blob/v1.17.0/scipy/optimize/_hessian_update_strategy.py, L379-L422


    **Args:**
    > delta_x (List[float]): Change in design variables.  
    > delta_g (List[float]): Change in gradient.  


    **Returns:**
    > bool: True if the curvature condition is violated, False otherwise.  

??? abstract "updateHessianApproximation(self, current_x: List[float], current_g: List[float]) → None"
    Update the internal BFGS Hessian approximation using the current design variables and gradient.

    Computes the deltas from the stored previous values and delegates
    to the parent BFGS update method.

    After the update, the previous design variables and gradient are
    overwritten with the current values.


    **Args:**
    > current_x (List[float]): the current design variable vector  
    > current_g (List[float]): the current gradient vector  

??? abstract "update_state(self, other_hessian_approximator: [HessianApproximationBFGS](HessianApproximationBFGS.md#hessianapproximationbfgs)) → None"
    Updates the self object with the data from other_hessian_approximator.


    **Args:**
    > other_hessian_approximator (HessianApproximationBFGS): The source object to copy state from.  

