# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Level-by-level iteration scheme module.

This module provides an iteration scheme where subsystems at each level
are executed in parallel before moving to the next level.
"""

import multiprocessing
from typing import List, Tuple
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print, ddo_print_border
from Distributed_Design_Optimizer.subsystem import SubSystemInterface
from Distributed_Design_Optimizer.coordination.innerloop_iterationscheme import IterationSchemeBasis


class ParallelPerLevelIncreasing(IterationSchemeBasis):
    """Iteration scheme that executes subsystems level by level.

    This scheme processes subsystems by their level, executing all
    subsystems at the same level in parallel before moving to the next level.
    """

    def __init__(self) -> None:
        """Initialize the ParallelPerLevelIncreasing iteration scheme.
        """
    
    def run_innerloop_jobs_multiprocessing(self, subsystemsIn: List[SubSystemInterface]) -> Tuple[List[SubSystemInterface], List[int]]:
        """Execute inner loop jobs level by level using multiprocessing.

        Subsystems are grouped by their subsystem level and executed in parallel
        within each level. Processing proceeds from level 0 upward.

        Args:
            subsystemsIn: List of subsystems to execute.

        Returns:
            Tuple containing the list of executed subsystems and their indices.
        """
        # Keep track of all executed subsystems and their indices
        all_executed_subsystems = []
        all_subsystem_indices = []
        
        # Process level by level
        lvl = 0  # level counter
        subsystems_processed = 0
        
        while subsystems_processed < len(subsystemsIn):
            # Find subsystems at the current level
            level_subsystems = []
            level_subsystem_indices = []
            
            for i in range(len(subsystemsIn)):
                if subsystemsIn[i].get_SubsystemLevel() == lvl:
                    level_subsystems.append(subsystemsIn[i])
                    level_subsystem_indices.append(i)
            
            if not level_subsystems:  # No subsystems at this level
                lvl += 1
                continue
                
            # Execute all subsystems at this level in parallel
            if len(level_subsystems) > multiprocessing.cpu_count():
                raise ValueError(f"{DDO_Color}ERROR: To run subsystems in parallel, you need to have at least as many cpu cores as there are subsystems to be executed in parallel{Reset}")
            pool = multiprocessing.Pool(processes=min(len(level_subsystems), multiprocessing.cpu_count()),
                                        maxtasksperchild=1)
            executed_subsystems = pool.map(self.run_subsystem, level_subsystems)                    
            pool.close()
            pool.join()
            
            # Store executed subsystems and their indices for later processing
            all_executed_subsystems.extend(executed_subsystems)
            all_subsystem_indices.extend(level_subsystem_indices)
            
            subsystems_processed += len(level_subsystems)
            lvl += 1
        
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
        ddo_print(f"{pad} Subsystems at the same level run in parallel, levels processed in increasing order")
        ddo_print_border()
        print()