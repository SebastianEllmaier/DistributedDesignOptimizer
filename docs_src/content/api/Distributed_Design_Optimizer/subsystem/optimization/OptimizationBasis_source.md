---
title: OptimizationBasis (Source)
---

← Back to [OptimizationBasis documentation](OptimizationBasis.md)

# OptimizationBasis - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\optimization\OptimizationBasis.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.

"""Optimization basis module.

This module provides the base class for optimization implementations.
"""


from Distributed_Design_Optimizer.subsystem import SubSystemInterface
from Distributed_Design_Optimizer.subsystem.optimization import OptimizationInterface
from Distributed_Design_Optimizer.subsystem.optimization.solver import SolverInterface
from Distributed_Design_Optimizer.subsystem.optimization.optimizerdata import OptimDataBasis


class OptimizationBasis(OptimizationInterface):
    """Base implementation of the optimization interface.

    Provides the foundational optimization functionality for subsystem optimization,
    delegating the actual optimization to a configured optimizer algorithm.
    """
    
    def __init__(self, optimizer: SolverInterface) -> None:
        """Initialize the optimization basis with the solver to delegate to.

        Args:
            optimizer: The solver algorithm used to optimize the subsystem.
        """
        self._optimizer = optimizer

    def callOptimizer(self, subsystemin: SubSystemInterface) -> OptimDataBasis:
        """Execute the optimizer on the given subsystem.

        Runs the configured optimizer algorithm on the subsystem and returns
        the optimization results.

        Args:
            subsystemin: The subsystem to be optimized.

        Returns:
            The optimization results produced by the configured solver.
        """
        # execute optimization and return the results to the caller
        return self._optimizer.execute(subsystem=subsystemin)

    def get_Optimizer(self) -> SolverInterface:
        """Return the solver algorithm configured for this optimization.

        Returns:
            The solver instance that this optimization delegates to.
        """
        return self._optimizer
```
