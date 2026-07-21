# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""AlwaysConverged centralized outer loop convergence indicator for controller subsystems.

This module provides a centralized outer loop convergence indicator whose evaluate()
method always sets convergence to True. Used for controller subsystems (e.g., in ALADIN)
where convergence is determined entirely by the local subsystems.
"""

from typing import List
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print, ddo_print_border
from Distributed_Design_Optimizer.coordination.convergence import Centralized_ConvergenceIndicator_Outerloop_Basis
from Distributed_Design_Optimizer.subsystem import SubSystemInterface


class Centralized_ConvergenceIndicator_Outerloop_AlwaysConverged(Centralized_ConvergenceIndicator_Outerloop_Basis):
    """Centralized outer loop convergence indicator that always returns True.
    
    Used when the centralized convergence check should always pass.
    """
        
    def evaluate(self, subsystems: List[SubSystemInterface]) -> None:
        """Set outer loop convergence to True unconditionally.

        Args:
            subsystems: List of subsystems (unused).
        """
        self._convouterloop = True
    
    def print_beginning_of_centralized_convergenceindicator_outerloop_evaluation(self) -> None:
        """Print a banner indicating that outer loop convergence is always True."""
        name = f"{type(self).__name__}:"
        pad = " " * len(name)
        ddo_print_border()
        ddo_print(f"{name} Starting Outerloop Convergence Evaluation ...")
        ddo_print(f"{pad} Convergence is always True (no convergence check performed)")
        ddo_print_border()
        print()
        
    def print_end_of_centralized_convergenceindicator_outerloop_evaluation(self, subsystems: List[SubSystemInterface]) -> None:
        """Print the overall outer loop convergence result (always True).

        Args:
            subsystems: List of all subsystems (unused since convergence is always True).
        """
        name = f"{type(self).__name__}:"
        pad = " " * len(name)
        ddo_print_border()
        ddo_print(f"{name} Finished Outerloop Convergence Evaluation:")
        ddo_print(f"{pad} Overall ConvOuterLoop is {self._convouterloop}")
        ddo_print_border()
        print()

    def update_state(self, other: 'Centralized_ConvergenceIndicator_Outerloop_AlwaysConverged') -> None:
        """Update the state of this instance with values from another instance.

        Args:
            other: The source instance containing updated values.
        """
        super().update_state(other)
