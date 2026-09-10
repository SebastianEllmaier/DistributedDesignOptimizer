---
title: SolverInterface (Source)
---

← Back to [SolverInterface documentation](SolverInterface.md)

# SolverInterface - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\optimization\solver\SolverInterface.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Optimizer interface module.

This module defines the abstract interface for optimization algorithms.
"""

from abc import ABC, abstractmethod
from Distributed_Design_Optimizer.subsystem import SubSystemInterface
from Distributed_Design_Optimizer.subsystem.optimization.optimizerdata import OptimDataBasis


class SolverInterface(ABC):
    """Abstract interface for optimization algorithm implementations.

    Defines the contract that all optimizer algorithms must implement.
    Each optimizer executes an optimization routine on a subsystem and
    returns the optimization results.
    """
    
    @abstractmethod
    def execute(self, subsystem: SubSystemInterface) -> OptimDataBasis:
        """Execute the optimization solver.

        Args:
            subsystem: The subsystem to optimize.

        Returns:
            Optimization results containing design variables, objectives,
            constraints, and solver metadata.
        """

```
