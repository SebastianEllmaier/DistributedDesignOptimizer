# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Interface module for local inner loop convergence indicators.

This module defines the abstract interface for local inner loop convergence
indicators that are evaluated within each subsystem.
"""

from abc import ABC, abstractmethod
from Distributed_Design_Optimizer.subsystem import SubSystemInterface


class Local_ConvergenceIndicator_Innerloop_Interface(ABC):
    """Abstract interface for local inner loop convergence indicators.

    This interface defines the contract for evaluating inner loop convergence
    at the subsystem level. Each subsystem has its own local convergence indicator
    that checks if the local optimization has stabilized.
    """

    @abstractmethod
    def evaluate(self, subsystem: SubSystemInterface) -> bool:
        """Evaluate if local inner loop convergence criteria is met.

        The convergence indicator retrieves the data it needs from the subsystem.
        This allows different convergence criteria to access different data
        (e.g., total objective, primal/dual residuals, etc.).

        Args:
            subsystem: The subsystem to evaluate convergence for.

        Returns:
            bool: True if convergence condition is met, False otherwise.
        """

    @abstractmethod
    def update_state(self, other: 'Local_ConvergenceIndicator_Innerloop_Interface') -> None:
        """Update the state of this convergence indicator with the state of another.

        This operation preserves the memory address of the object's attributes
        and only updates the value(s). This method is necessary for multiprocessing,
        where executed subsystems need to transfer their state back to the original objects.

        Args:
            other: The convergence indicator to copy state from.
        """
