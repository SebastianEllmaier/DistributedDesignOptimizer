# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Interface module for outer loop convergence indicator factories.

This module defines the abstract factory interface for creating outer loop 
convergence indicators that are used in distributed optimization coordination.
"""

from abc import ABC, abstractmethod
from Distributed_Design_Optimizer.coordination.convergence import (Local_ConvergenceIndicator_Outerloop_Interface,
                                                                   Centralized_ConvergenceIndicator_Outerloop_Interface)


class ConvergenceIndicator_Outerloop_Interface(ABC):
    """Abstract factory interface for outer loop convergence indicators.

    This interface defines the contract for creating local and centralized
    convergence indicators for the outer loop. Implementations provide
    specific convergence criteria (e.g., consistency-based, coupling parameter change).
    """

    @abstractmethod
    def createLocalConvergenceIndicator(self) -> Local_ConvergenceIndicator_Outerloop_Interface:
        """Create a local convergence indicator for subsystem-level evaluation.

        Returns:
            Local_ConvergenceIndicator_Outerloop_Interface: A new local convergence indicator instance.
        """

    @abstractmethod
    def createCentralizedConvergenceIndicator(self) -> Centralized_ConvergenceIndicator_Outerloop_Interface:
        """Create a centralized convergence indicator for coordinator-level evaluation.

        Returns:
            Centralized_ConvergenceIndicator_Outerloop_Interface: A new centralized convergence indicator instance.
        """

    @abstractmethod
    def validate_inputs(self) -> None:
        """Validate the inputs provided to the convergence indicator.
        
        Raises:
            ValueError: If any parameter is outside the allowed range.
        """

    @abstractmethod
    def print_startup_summary(self) -> None:
        """Print the outer loop convergence indicator configuration at startup."""
    
    @abstractmethod
    def print_termination_summary(self) -> None:
        """Print the outer loop convergence indicator configuration at the end."""
