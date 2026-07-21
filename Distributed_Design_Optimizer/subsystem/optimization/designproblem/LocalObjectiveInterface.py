# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Local objective interface module.

This module defines the abstract interface for local subsystem objectives.
"""

from abc import ABC, abstractmethod
from Distributed_Design_Optimizer.subsystem import SubSystemInterface


class LocalObjectiveInterface(ABC):
    """Interface for the class that defines the local objective function value."""

    @abstractmethod
    def evaluateLocalObjective(self, subsystem: SubSystemInterface) -> None:
        """Evaluate the objective function of a subsystem.

        Args:
            subsystem: The subsystem interface for which the local objective
                function is evaluated.
        """

    @abstractmethod
    def evaluate_Gradient_LocalObjective(self, subsystem: SubSystemInterface) -> None:
        """Evaluate the gradient of the objective function for the components that are known.

        Args:
            subsystem: The subsystem interface for which the gradient is
                evaluated.
        """

    @abstractmethod
    def evaluate_Hessian_LocalObjective(self, subsystem: SubSystemInterface) -> None:
        """Evaluate the Hessian of the objective function for the components that are known.

        Args:
            subsystem: The subsystem interface for which the Hessian is
                evaluated.
        """

