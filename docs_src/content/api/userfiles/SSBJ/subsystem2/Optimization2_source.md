---
title: Optimization2 (Source)
---

← Back to [Optimization2 documentation](Optimization2.md)

# Optimization2 - Source Code

**File:** `userfiles\SSBJ\subsystem2\Optimization2.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Optimization configuration for Subsystem 2 in the SSBJ problem."""
from Distributed_Design_Optimizer.subsystem.optimization import OptimizationBasis
from Distributed_Design_Optimizer.subsystem.optimization.solver import (
                                                                        # Solver_SCBO,
                                                                        # Solver_Scipy,
                                                                        # Solver_CMA,
                                                                        # Solver_IPOPT,
                                                                        Solver_PyNomadBBO,
                                                                        # Solver_Pyomo,
                                                                        # Solver_Fmincon
                                                                        )


class Optimization2(OptimizationBasis):
    """Optimization configuration class for Subsystem 2.

    Attributes:
        _optimizer: The configured optimizer instance.
    """
    def __init__(self) -> None:
        """Initialize the Optimization2 instance with the selected optimizer."""

        super().__init__(Solver_PyNomadBBO(maxevals=20000,
                                           constraint_handling_method="PB",
                                           seed=1,
                                           vns_mads_search=False,
                                           quad_model_search=False,
                                           eqcon_as_ineqcon_tol=1E-8))

        # super().__init__(Solver_SCBO(option_1=None))

        # super().__init__(Solver_Scipy(method="trust-constr",
        #                               constraint_jac="2-point",
        #                               constraint_keep_feasible=False,
        #                               maxiter=None))

        # super().__init__(Solver_IPOPT(maxiter=1000,
        #                               acceptable_tol=1e-8,
        #                               constraint_jac="2-point",
        #                               constraint_keep_feasible=False))

        # super().__init__(Solver_Pyomo(option_1=None,
        #                               option_2=None))

        # super().__init__(Solver_Fmincon(method="active_set",
        #                                 maxiter=1000,
        #                                 maxfunevals=10000,
        #                                 tolfun=1e-8,
        #                                 tolcon=1e-8))

```
