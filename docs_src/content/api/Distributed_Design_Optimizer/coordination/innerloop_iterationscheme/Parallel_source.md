---
title: Parallel (Source)
---

← Back to [Parallel documentation](Parallel.md)

# Parallel - Source Code

**File:** `Distributed_Design_Optimizer\coordination\innerloop_iterationscheme\Parallel.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Fully parallel iteration scheme module.

This module provides an iteration scheme where all subsystems
are executed simultaneously in parallel.
"""

import multiprocessing
from typing import List, Tuple
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print, ddo_print_border
from Distributed_Design_Optimizer.subsystem import SubSystemInterface
from Distributed_Design_Optimizer.coordination.innerloop_iterationscheme import IterationSchemeBasis


class Parallel(IterationSchemeBasis):
    """Iteration scheme that executes all subsystems in parallel.

    This scheme runs all subsystems simultaneously.
    """

    def __init__(self) -> None:
        """Initialize the Parallel iteration scheme.
        """
            
    def run_innerloop_jobs_multiprocessing(self, subsystemsIn: List[SubSystemInterface]) -> Tuple[List[SubSystemInterface], List[int]]:
        """Execute all inner loop jobs in parallel using multiprocessing.

        All subsystems are executed simultaneously using a process pool.

        Args:
            subsystemsIn: List of subsystems to execute.

        Returns:
            Tuple containing the list of executed subsystems and their indices.
        """
        # Keep track of all executed subsystems and their indices
        all_executed_subsystems = []
        all_subsystem_indices = []
        
        # Execute all subsystems in parallel using Pool
        if len(subsystemsIn) > multiprocessing.cpu_count():
            raise ValueError(f"{DDO_Color}ERROR: To run subsystems in parallel, you need to have at least as many cpu cores as there are subsystems to be executed in parallel{Reset}")
        pool = multiprocessing.Pool(processes=min(len(subsystemsIn), multiprocessing.cpu_count()),
                                    maxtasksperchild=1)
        executed_subsystems = pool.map(self.run_subsystem, subsystemsIn)
        pool.close()
        pool.join()
        
        # Store executed subsystems and their indices
        all_executed_subsystems.extend(executed_subsystems)
        all_subsystem_indices.extend(range(len(subsystemsIn)))
        
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
        ddo_print(f"{pad} All subsystems are executed simultaneously in a single parallel batch")
        ddo_print_border()
        print()
```
