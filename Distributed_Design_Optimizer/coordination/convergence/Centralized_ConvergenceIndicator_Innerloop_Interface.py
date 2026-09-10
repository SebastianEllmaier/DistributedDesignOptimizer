# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Interface module for centralized inner loop convergence indicators.

This module defines the abstract interface for centralized inner loop convergence
indicators that aggregate convergence across all subsystems.
"""

from abc import ABC, abstractmethod
from typing import List
from Distributed_Design_Optimizer.subsystem import SubSystemInterface


class Centralized_ConvergenceIndicator_Innerloop_Interface(ABC):
    """Abstract interface for centralized inner loop convergence indicators.

    This interface defines the contract for evaluating inner loop convergence
    at the coordinator level by aggregating local convergence flags from all subsystems.
    """
    
    @abstractmethod
    def get_ConvInnerLoop(self) -> bool:
        """Return the current inner loop convergence flag.

        Returns:
            bool: True if inner loop has converged, False otherwise.
        """

    @abstractmethod
    def evaluate(self, subsystems: List[SubSystemInterface]) -> None:
        """Evaluate centralized inner loop convergence across all subsystems.

        This method first triggers local convergence evaluation in each subsystem,
        then aggregates the results to determine overall inner loop convergence.

        Args:
            subsystems: List of all subsystems to check for convergence.
        """

    @abstractmethod
    def print_beginning_of_centralized_convergenceindicator_innerloop_evaluation(self) -> None:
        """Print a banner before the centralized inner loop convergence evaluation."""
        
    @abstractmethod
    def print_end_of_centralized_convergenceindicator_innerloop_evaluation(self, subsystems: List[SubSystemInterface]) -> None:
        """Print per-subsystem and overall inner loop convergence results.

        Args:
            subsystems: List of all subsystems whose convergence flags are printed.
        """

    @abstractmethod
    def print_convergence_result(self) -> None:
        """Print the current innerloop convergence state."""

    @abstractmethod
    def update_state(self, other: 'Centralized_ConvergenceIndicator_Innerloop_Interface') -> None:
        """Update the state of this instance with values from another instance.

        Args:
            other: The source instance containing updated values.
        """