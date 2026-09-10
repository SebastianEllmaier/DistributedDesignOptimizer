# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Bottom-up sequential iteration scheme module.

This module provides an iteration scheme where subsystems are executed
sequentially from lowest to highest hierarchical level.
"""

import multiprocessing
from typing import List, Tuple
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print, ddo_print_border
from Distributed_Design_Optimizer.coordination.innerloop_iterationscheme import IterationSchemeBasis
from Distributed_Design_Optimizer.subsystem import SubSystemInterface


class SequentialBackward(IterationSchemeBasis):
    """Iteration scheme that executes subsystems sequentially in bottom-up order.

    This scheme runs subsystems one at a time, starting from the
    lowest level and working up to the highest level (reverse order).
    """

    def __init__(self) -> None:
        """Initialize the SequentialBackward iteration scheme.
        """
    
    def run_innerloop_jobs_multiprocessing(self, subsystemsIn: List[SubSystemInterface]) -> Tuple[List[SubSystemInterface], List[int]]:
        """Execute inner loop jobs sequentially in bottom-up order using multiprocessing.

        Subsystems are processed one at a time in reverse order (bottom-up),
        using a process pool with blocking apply calls.

        Args:
            subsystemsIn: List of subsystems to execute.

        Returns:
            Tuple containing the list of executed subsystems and their indices.
        """
        # Keep track of all executed subsystems and their indices
        all_executed_subsystems = []
        all_subsystem_indices = []
        
        # Execute all subsystems in sequential using Pool but in reverse order
        pool = multiprocessing.Pool(processes=min(len(subsystemsIn), multiprocessing.cpu_count()),
                                    maxtasksperchild=1)
        # Run each task sequentially through apply(), which blocks until completion
        # Process in bottom-up order (reverse order)
        for i in range(len(subsystemsIn) - 1, -1, -1):
            executed_subsystem = pool.apply(self.run_subsystem, (subsystemsIn[i],))
            all_executed_subsystems.append(executed_subsystem)
            all_subsystem_indices.append(i)
        pool.close()
        pool.join()
        
        return all_executed_subsystems, all_subsystem_indices

    def print_startup_summary(self) -> None:
        """Nothing to print."""
        pass

    def print_termination_summary(self) -> None:
        """Nothing to print."""
        pass
    
    def print_beginning_of_run_innerloop_jobs_multiprocessing(self) -> None:
        """Print a banner before executing inner loop jobs with multiprocessing."""
        name = f"{type(self).__name__}:"
        pad = " " * len(name)
        ddo_print_border()
        ddo_print(f"{name} Starting InnerLoop Jobs Execution using Multiprocessing ...")
        ddo_print(f"{pad} Subsystems are executed one-at-a-time in reverse index order")
        ddo_print_border()
        print()