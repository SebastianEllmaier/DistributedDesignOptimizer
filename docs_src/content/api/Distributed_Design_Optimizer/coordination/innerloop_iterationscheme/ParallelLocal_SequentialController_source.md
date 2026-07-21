---
title: ParallelLocal_SequentialController (Source)
---

← Back to [ParallelLocal_SequentialController documentation](ParallelLocal_SequentialController.md)

# ParallelLocal_SequentialController - Source Code

**File:** `Distributed_Design_Optimizer\coordination\innerloop_iterationscheme\ParallelLocal_SequentialController.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Parallel local, sequential controller iteration scheme module.

This module provides an iteration scheme where local subsystems execute
in parallel while the controller subsystem executes sequentially.
"""

import multiprocessing
from typing import List, Tuple
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print, ddo_print_border
from Distributed_Design_Optimizer.subsystem import SubSystemInterface
from Distributed_Design_Optimizer.subsystem import ControllerSubSystemBasis
from Distributed_Design_Optimizer.coordination.innerloop_iterationscheme import IterationSchemeBasis


class ParallelLocal_SequentialController(IterationSchemeBasis):
    """Iteration scheme with parallel local subsystems and sequential controller.

    Executes local subsystems in parallel while running the controller
    subsystem sequentially to ensure proper coordination.
    """

    def __init__(self) -> None:
        """Initialize the iteration scheme."""
            
    def run_innerloop_jobs_multiprocessing(self, subsystemsIn: List[SubSystemInterface]) -> Tuple[List[SubSystemInterface], List[int]]:
        """Execute inner loop jobs using multiprocessing.

        Args:
            subsystemsIn: List of subsystems to execute.

        Returns:
            Tuple containing the list of executed subsystems and their original indices.
        """
        # Keep track of all executed subsystems and their indices
        all_executed_subsystems: List[SubSystemInterface] = []
        all_subsystem_indices: List[int] = []
        
        # Separate local subsystems from controller, tracking original indices
        local_subsystems: List[SubSystemInterface] = []
        local_subsystem_indices: List[int] = []
        controller_subsystem: SubSystemInterface | None = None
        controller_subsystem_index: int | None = None
        
        for i in range(len(subsystemsIn)):
            if isinstance(subsystemsIn[i], ControllerSubSystemBasis):
                controller_subsystem = subsystemsIn[i]
                controller_subsystem_index = i
            else:
                local_subsystems.append(subsystemsIn[i])
                local_subsystem_indices.append(i)
        
        # Execute all local subsystems in parallel using Pool
        if len(local_subsystems) > 0:
            if len(local_subsystems) > multiprocessing.cpu_count():
                raise ValueError(f"{DDO_Color}ERROR: To run subsystems in parallel, you need to have at least as many cpu cores as there are subsystems to be executed in parallel{Reset}")
            pool = multiprocessing.Pool(processes=min(len(local_subsystems), multiprocessing.cpu_count()),
                                        maxtasksperchild=1)
            executed_subsystems = pool.map(self.run_subsystem, local_subsystems)
            pool.close()
            pool.join()
            
            # Store executed subsystems and their original indices
            all_executed_subsystems.extend(executed_subsystems)
            all_subsystem_indices.extend(local_subsystem_indices)
        
        # If there is a controller, execute it sequentially after local subsystems
        if controller_subsystem is not None:
            controller_subsystem = self.run_subsystem(subsystem=controller_subsystem)
        
            # Store executed controller subsystem and its original index
            all_executed_subsystems.append(controller_subsystem)
            all_subsystem_indices.append(controller_subsystem_index)
        
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
        ddo_print(f"{pad} Phase 1: All local subsystems in parallel, Phase 2: Controller subsystem sequentially")
        ddo_print_border()
        print()
```
