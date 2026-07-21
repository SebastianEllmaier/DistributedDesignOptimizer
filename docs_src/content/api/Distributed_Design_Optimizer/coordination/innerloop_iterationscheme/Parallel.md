---
title: Parallel
---

← Back to [innerloop_iterationscheme](index.md)

# Parallel

**Source:** [Distributed_Design_Optimizer\coordination\innerloop_iterationscheme\Parallel.py](Parallel_source.md)

Fully parallel iteration scheme module.

This module provides an iteration scheme where all subsystems
are executed simultaneously in parallel.

## Classes

### Parallel

> **Inherits from:** [IterationSchemeBasis](IterationSchemeBasis.md#iterationschemebasis)

> Iteration scheme that executes all subsystems in parallel.

> This scheme runs all subsystems simultaneously.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the Parallel iteration scheme.


??? abstract "run_innerloop_jobs_multiprocessing(self, subsystemsIn: List[[SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)]) → Tuple[List[[SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)], List[int]]"
    Execute all inner loop jobs in parallel using multiprocessing.

    All subsystems are executed simultaneously using a process pool.


    **Args:**
    > subsystemsIn: List of subsystems to execute.  


    **Returns:**
    > Tuple containing the list of executed subsystems and their indices.  

??? abstract "print_startup_summary(self) → None"
    Nothing to print.

??? abstract "print_termination_summary(self) → None"
    Nothing to print.

??? abstract "print_beginning_of_run_innerloop_jobs_multiprocessing(self) → None"
    Print a banner before executing inner loop jobs with multiprocessing.

