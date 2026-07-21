---
title: ParallelLocal_SequentialController
---

← Back to [innerloop_iterationscheme](index.md)

# ParallelLocal_SequentialController

**Source:** [Distributed_Design_Optimizer\coordination\innerloop_iterationscheme\ParallelLocal_SequentialController.py](ParallelLocal_SequentialController_source.md)

Parallel local, sequential controller iteration scheme module.

This module provides an iteration scheme where local subsystems execute
in parallel while the controller subsystem executes sequentially.

## Classes

### ParallelLocal_SequentialController

> **Inherits from:** [IterationSchemeBasis](IterationSchemeBasis.md#iterationschemebasis)

> Iteration scheme with parallel local subsystems and sequential controller.

> Executes local subsystems in parallel while running the controller
> subsystem sequentially to ensure proper coordination.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the iteration scheme.

??? abstract "run_innerloop_jobs_multiprocessing(self, subsystemsIn: List[[SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)]) → Tuple[List[[SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)], List[int]]"
    Execute inner loop jobs using multiprocessing.


    **Args:**
    > subsystemsIn: List of subsystems to execute.  


    **Returns:**
    > Tuple containing the list of executed subsystems and their original indices.  

??? abstract "print_startup_summary(self) → None"
    Nothing to print.

??? abstract "print_termination_summary(self) → None"
    Nothing to print.

??? abstract "print_beginning_of_run_innerloop_jobs_multiprocessing(self) → None"
    Print a banner before executing inner loop jobs with multiprocessing.

