---
title: HessianApproximationBFGS (Source)
---

← Back to [HessianApproximationBFGS documentation](HessianApproximationBFGS.md)

# HessianApproximationBFGS - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\tools\HessianApproximationBFGS.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""BFGS Hessian approximation module.

This module provides BFGS-based Hessian approximation for
optimization algorithms.
"""

import copy
import numpy as np
from scipy.optimize import BFGS
from typing import List
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset
from Distributed_Design_Optimizer.subsystem.tools import update_state_listprimitive


class HessianApproximationBFGS(BFGS):
    """
    A HessianApproximationBFGS object extends the scipy BFGS Hessian update strategy.

    It tracks previous design variables and gradients, enabling incremental
    Hessian approximation updates from absolute (current) values rather than deltas.

    Args:
        exception_strategy (str): Strategy when curvature condition is violated
            ('skip_update' or 'damp_update').
        min_curvature (float | None): Minimum curvature threshold.
        init_scale (float | str): Initialization scale for the Hessian matrix.
    """
    
    def __init__(self,
                 exception_strategy: str = 'skip_update',
                 min_curvature: float | None = None,
                 init_scale: float | str = 'auto'
                 ) -> None:
        """
        Creates a new instance of HessianApproximationBFGS.

        Args:
            exception_strategy (str): Strategy when curvature condition is violated
                ('skip_update' or 'damp_update').
            min_curvature (float | None): Minimum curvature threshold.
            init_scale (float | str): Initialization scale for the Hessian matrix.
        """
        
        super().__init__(exception_strategy=exception_strategy,
                         min_curvature=min_curvature,
                         init_scale=init_scale)
        
        # The previous design variable vector
        self._previous_x: List[float] | None = None
        
        # The previous gradient vector
        self._previous_g: List[float] | None = None


################################################################################################################
#   Getters and setters
################################################################################################################

    def get_Previous_X(self) -> List[float] | None:
        """
        Returns the previous design variable vector.

        Returns:
            List[float] | None: the previous design variable vector
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._previous_x)
    
    def set_Previous_X(self, previous_x_in: List[float]) -> None:
        """
        Sets the previous design variable vector.

        Args:
            previous_x_in (List[float]): the previous design variable vector
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._previous_x = copy.copy(previous_x_in)
    
    def get_Previous_G(self) -> List[float] | None:
        """
        Returns the previous gradient vector.

        Returns:
            List[float] | None: the previous gradient vector
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        return copy.copy(self._previous_g)
    
    def set_Previous_G(self, previous_g_in: List[float]) -> None:
        """
        Sets the previous gradient vector.

        Args:
            previous_g_in (List[float]): the previous gradient vector
        """
        # copy.copy() used - List[float] is mutable. This prevents modifications
        # in the caller from being reflected back to the class attribute.
        self._previous_g = copy.copy(previous_g_in)


################################################################################################################
#   Update Hessian approximation
################################################################################################################

    def check_CurvatureConditionViolation(self, delta_x: List[float], delta_g: List[float]) -> bool:
        """
        Check if the curvature condition of BFGS is triggered.

        This also happens in the function update of scipy.optimize.BFGS.
        The logic is based on the check in _update_implementation in
        scipy.optimize.BFGS.
        Source: https://github.com/scipy/scipy/blob/v1.17.0/scipy/optimize/_hessian_update_strategy.py, L379-L422

        Args:
            delta_x (List[float]): Change in design variables.
            delta_g (List[float]): Change in gradient.

        Returns:
            bool: True if the curvature condition is violated, False otherwise.
        """
        
        # Direct Hessian approximation via BFGS
        w = np.array(delta_x)
        z = np.array(delta_g)
        
        # Compute wMw, where M is the current Hessian
        w_z = np.dot(w, z)
        M_w = self @ w
        w_M_w = -M_w.dot(w)  
        
        # Comment from scipy.optimize.BFGS code:
        # Source: https://github.com/scipy/scipy/blob/v1.17.0/scipy/optimize/_hessian_update_strategy.py L391-L393
        
        # Guarantee that w_M_w > 0 by reinitializing matrix.
        # While this is always true in exact arithmetic,
        # indefinite matrix may appear due to roundoff errors.
        if w_M_w <= 0:
            scale = self._auto_scale(w, z)
            # Reinitialize matrix-vector-products
            # since the Hessian approximation is reset to scale * np.eye(self.n, dtype=float)
            M_w = scale * w
            w_M_w = M_w.dot(w)
            
        # Compute boolean if curvature condition is violated
        curvature_condition_violated: bool = bool(w_z <= self.min_curvature * w_M_w)
        
        # Return the indicator if the curvature condition is violated
        return curvature_condition_violated
         
    
    def updateHessianApproximation(self, current_x: List[float], current_g: List[float]) -> None:
        """
        Update the internal BFGS Hessian approximation using the current design variables and gradient.

        Computes the deltas from the stored previous values and delegates
        to the parent BFGS update method.

        After the update, the previous design variables and gradient are
        overwritten with the current values.

        Args:
            current_x (List[float]): the current design variable vector
            current_g (List[float]): the current gradient vector
        """
        
        # Check if the previous designvariables and previous gradients are set
        if self._previous_x is not None and self._previous_g is not None:
            
            # Only if the previous values exist, the update formula is applicable
            
            # Compute the change in design variables
            delta_x: List[float] = [current_x[i] - self._previous_x[i] for i in range(len(current_x))]
            
            # Compute the change in gradient
            delta_g: List[float] = [current_g[i] - self._previous_g[i] for i in range(len(current_g))]
            
            # Check BFGS curvature condition for the well-definedness of the BFGS update formula
            if self.check_CurvatureConditionViolation(delta_x, delta_g) is True:
                
                # raise Warning that the curvature condition is violated 
                # and it is reverted to the exception strategy
                print(f"{DDO_Color}WARNING: ", 
                      f"The curvature condition for the well-definedness of the BFGS update formula is violated, and hence the update is reverted to the exception strategy: {self.exception_strategy}. ",
                      f"The curvature condition is based on the condition <delta_x, delta_g> <= {self.min_curvature} * (delta_x * M * delta_x), where M is the current BFGS iterate matrix. ", 
                      f"The need for this check comes from the fact that the BFGS demands positiveness of <delta_x, delta_g>, and due to numerical instabilities, satisfying even a minimum curvature.{Reset}")
            
            # Delegate to the parent BFGS update
            super().update(np.array(delta_x), np.array(delta_g))
        
        # Store current values as previous for next iteration
        self._previous_x = copy.copy(current_x)
        self._previous_g = copy.copy(current_g)
        
    def update_state(self, other_hessian_approximator: 'HessianApproximationBFGS') -> None:
        """
        Updates the self object with the data from other_hessian_approximator.

        Args:
            other_hessian_approximator (HessianApproximationBFGS): The source object to copy state from.
        """
        
        self._previous_x = update_state_listprimitive(self._previous_x, other_hessian_approximator.get_Previous_X())
        self._previous_g = update_state_listprimitive(self._previous_g, other_hessian_approximator.get_Previous_G())
        
        
```
