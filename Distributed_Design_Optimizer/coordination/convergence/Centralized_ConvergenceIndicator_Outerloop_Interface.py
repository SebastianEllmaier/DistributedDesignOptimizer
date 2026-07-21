# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Interface module for centralized outer loop convergence indicators.

This module defines the abstract interface for centralized outer loop convergence
indicators that aggregate convergence across all subsystems.
"""

from abc import ABC, abstractmethod
from typing import List
from Distributed_Design_Optimizer.subsystem import SubSystemInterface


class Centralized_ConvergenceIndicator_Outerloop_Interface(ABC):
    """Abstract interface for centralized outer loop convergence indicators.

    This interface defines the contract for evaluating outer loop convergence
    at the coordinator level by aggregating local convergence flags from all subsystems.
    """
    
    @abstractmethod
    def get_ConvOuterLoop(self) -> bool:
        """Return the current outer loop convergence flag.

        Returns:
            bool: True if outer loop has converged, False otherwise.
        """

    @abstractmethod
    def evaluate(self, subsystems: List[SubSystemInterface]) -> None:
        """Evaluate centralized outer loop convergence across all subsystems.

        This method may trigger local convergence evaluation in each subsystem
        if needed, then aggregates the results to determine overall outer loop convergence.

        Args:
            subsystems: List of all subsystems to check for convergence.
        """
        
    @abstractmethod
    def print_beginning_of_centralized_convergenceindicator_outerloop_evaluation(self) -> None:
        """Print a banner before the centralized outer loop convergence evaluation."""
        
    @abstractmethod
    def print_end_of_centralized_convergenceindicator_outerloop_evaluation(self, subsystems: List[SubSystemInterface]) -> None:
        """Print per-subsystem and overall outer loop convergence results.

        Args:
            subsystems: List of all subsystems whose convergence flags are printed.
        """

    @abstractmethod
    def print_convergence_result(self) -> None:
        """Print the current outerloop convergence state."""

    @abstractmethod
    def update_state(self, other: 'Centralized_ConvergenceIndicator_Outerloop_Interface') -> None:
        """Update the state of this instance with values from another instance.

        Args:
            other: The source instance containing updated values.
        """