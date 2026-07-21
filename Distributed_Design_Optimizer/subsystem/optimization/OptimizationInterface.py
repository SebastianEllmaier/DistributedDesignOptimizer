# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Optimization interface module.

This module defines the abstract interface for optimization components.
"""

from abc import abstractmethod, ABC
from Distributed_Design_Optimizer.subsystem import SubSystemInterface
from Distributed_Design_Optimizer.subsystem.optimization.optimizerdata import OptimDataBasis


class OptimizationInterface(ABC):
    """Abstract interface for optimization execution.

    Defines the contract for classes that execute optimization algorithms
    on subsystems within the distributed design optimization framework.
    """
   
    @abstractmethod
    def callOptimizer(self, subsystemin: SubSystemInterface) -> OptimDataBasis:
        """Execute an optimization algorithm on the given subsystem.

        Args:
            subsystemin: The subsystem to be optimized.

        Returns:
            The optimization results produced by the configured solver.
        """
