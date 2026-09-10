# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""DeWit centralized inner loop convergence indicator.

Aggregates local inner loop convergence flags from all subsystems.
The coordinator has one instance of this class.
"""

from typing import List
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print, ddo_print_border
from Distributed_Design_Optimizer.coordination.convergence import Centralized_ConvergenceIndicator_Innerloop_Basis
from Distributed_Design_Optimizer.subsystem import SubSystemInterface


class Centralized_ConvergenceIndicator_Innerloop_DeWit(Centralized_ConvergenceIndicator_Innerloop_Basis):
    """Centralized inner loop convergence indicator - DeWit.
    
    Aggregates local convergence flags from all subsystems.
    The coordinator has one instance of this class.
    """
    
    def evaluate(self, subsystems: List[SubSystemInterface]) -> None:
        """Evaluate centralized inner loop convergence across all subsystems.

        First triggers local convergence evaluation in each subsystem,
        then aggregates the results using logical AND.

        Args:
            subsystems: List of all subsystems to check for convergence.
        """
        # Trigger local convergence evaluation in each subsystem
        for subsystem in subsystems:
            subsystem.evaluate_InnerLoopConvergenceIndicator()
        
        # Aggregate: all subsystems must be converged
        self._convinnerloop = all(subsystem.get_ConvInnerLoop() for subsystem in subsystems)

    def print_beginning_of_centralized_convergenceindicator_innerloop_evaluation(self) -> None:
        """Print a banner before evaluating inner loop convergence via logical AND over all subsystems."""
        name = f"{type(self).__name__}:"
        pad = " " * len(name)
        ddo_print_border()
        ddo_print(f"{name} Starting Innerloop Convergence Evaluation ...")
        ddo_print(f"{pad} Evaluating local convergence in each subsystem, then aggregating via logical AND")
        ddo_print_border()
        print()
        
    def print_end_of_centralized_convergenceindicator_innerloop_evaluation(self, subsystems: List[SubSystemInterface]) -> None:
        """Print per-subsystem inner loop convergence flags and the overall aggregated result.

        Args:
            subsystems: List of all subsystems whose inner loop convergence flags are printed.
        """
        name = f"{type(self).__name__}:"
        pad = " " * len(name)
        ddo_print_border()
        ddo_print(f"{name} Finished Innerloop Convergence Evaluation:")
        for subsystem in subsystems:
            ddo_print(f"{pad} SubSystem {subsystem.get_SUBSYSTEMID()} ConvInnerLoop is {subsystem.get_ConvInnerLoop()}")
        ddo_print(f"{pad} Overall ConvInnerLoop (Logical AND over all subsystems) is {self._convinnerloop}")
        ddo_print_border()
        print()

    def update_state(self, other: 'Centralized_ConvergenceIndicator_Innerloop_DeWit') -> None:
        """Update the state of this instance with values from another instance.

        Args:
            other: The source instance containing updated values.
        """
        super().update_state(other)
