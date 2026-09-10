---
title: ParallelOddThenEvenLevels (Source)
---

← Back to [ParallelOddThenEvenLevels documentation](ParallelOddThenEvenLevels.md)

# ParallelOddThenEvenLevels - Source Code

**File:** `Distributed_Design_Optimizer\coordination\innerloop_iterationscheme\ParallelOddThenEvenLevels.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Odd-even level iteration scheme module.

This module provides an iteration scheme where odd levels are solved first
in parallel, followed by even levels with updated values.
"""

import multiprocessing
from typing import List, Tuple
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print, ddo_print_border
from Distributed_Design_Optimizer.subsystem import SubSystemInterface
from Distributed_Design_Optimizer.coordination.innerloop_iterationscheme import IterationSchemeBasis


class ParallelOddThenEvenLevels(IterationSchemeBasis):
    """Iteration scheme that executes subsystems by level parity, odd levels first.

    All subsystems at odd levels are solved in parallel first, after which all
    subsystems at even levels are solved, also in parallel, using the updated
    targets and responses determined at the odd levels.
    For more reference, read Chapter 4 of Simon Tosseram's dissertation.
    """

    def __init__(self) -> None:
        """Initialize the ParallelOddThenEvenLevels iteration scheme."""
            
    def run_innerloop_jobs_multiprocessing(self, subsystemsIn: List[SubSystemInterface]) -> Tuple[List[SubSystemInterface], List[int]]:
        """Run inner loop jobs using multiprocessing with odd-even level ordering.

        Executes all subsystems at odd levels (1, 3, 5, ...) in parallel first,
        then all subsystems at even levels (0, 2, 4, ...) in parallel.

        Args:
            subsystemsIn: List of subsystems to execute.

        Returns:
            Tuple containing the list of executed subsystems and their original indices.
        """
        # Keep track of all executed subsystems and their indices
        all_executed_subsystems = []
        all_subsystem_indices = []
        
        # Process odd levels first (1, 3, 5, ...)
        odd_subsystems = []
        odd_subsystem_indices = []
        
        for i in range(len(subsystemsIn)):
            if subsystemsIn[i].get_SubsystemLevel() % 2 == 1:
                odd_subsystems.append(subsystemsIn[i])
                odd_subsystem_indices.append(i)
        
        if odd_subsystems:
            # Execute all odd level subsystems in parallel
            if len(odd_subsystems) > multiprocessing.cpu_count():
                raise ValueError(f"{DDO_Color}ERROR: To run subsystems in parallel, you need to have at least as many cpu cores as there are subsystems to be executed in parallel{Reset}")
            pool = multiprocessing.Pool(processes=min(len(odd_subsystems), multiprocessing.cpu_count()),
                                        maxtasksperchild=1)
            executed_odd_subsystems = pool.map(self.run_subsystem, odd_subsystems)
            pool.close()
            pool.join()
            
            # Store executed subsystems and their indices for later processing
            all_executed_subsystems.extend(executed_odd_subsystems)
            all_subsystem_indices.extend(odd_subsystem_indices)
        
        # Process even levels next (0, 2, 4, ...)
        even_subsystems = []
        even_subsystem_indices = []
        
        for i in range(len(subsystemsIn)):
            if subsystemsIn[i].get_SubsystemLevel() % 2 == 0:
                even_subsystems.append(subsystemsIn[i])
                even_subsystem_indices.append(i)
        
        if even_subsystems:
            # Execute all even level subsystems in parallel
            if len(even_subsystems) > multiprocessing.cpu_count():
                raise ValueError(f"{DDO_Color}ERROR: To run subsystems in parallel, you need to have at least as many cpu cores as there are subsystems to be executed in parallel{Reset}")
            pool = multiprocessing.Pool(processes=min(len(even_subsystems), multiprocessing.cpu_count()),
                                        maxtasksperchild=1)
            executed_even_subsystems = pool.map(self.run_subsystem, even_subsystems)
            pool.close()
            pool.join()
            
            # Store executed subsystems and their indices for later processing
            all_executed_subsystems.extend(executed_even_subsystems)
            all_subsystem_indices.extend(even_subsystem_indices)
        
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
        ddo_print(f"{pad} Phase 1: All odd-level subsystems in parallel, Phase 2: All even-level subsystems in parallel")
        ddo_print_border()
        print()
```
