# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Base implementation for centralized outer loop convergence indicators."""

from Distributed_Design_Optimizer.coordination.convergence import Centralized_ConvergenceIndicator_Outerloop_Interface
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print

class Centralized_ConvergenceIndicator_Outerloop_Basis(Centralized_ConvergenceIndicator_Outerloop_Interface):
    """Base class for centralized outer loop convergence indicators.

    Provides default storage and accessor for the outer loop convergence flag.
    """
    
    def __init__(self) -> None:
        """Initialize with convergence flag set to False."""
        self._convouterloop: bool = False
        
    def get_ConvOuterLoop(self) -> bool:
        """Return the current outer loop convergence flag.

        Returns:
            bool: True if outer loop has converged, False otherwise.
        """
        return self._convouterloop

    def print_convergence_result(self) -> None:
        """Print the current outerloop convergence state."""
        ddo_print(f"{type(self).__name__}: Outerloop Convergence Indicator is {self.get_ConvOuterLoop()}")

    def update_state(self, other: 'Centralized_ConvergenceIndicator_Outerloop_Basis') -> None:
        """Update the state of this instance with values from another instance.

        Args:
            other: The source instance containing updated values.
        """
        # No copy.copy() needed - bool is a primitive/immutable type
        self._convouterloop = other._convouterloop