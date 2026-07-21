---
title: ParallelPerLevelIncreasing
---

← Back to [innerloop_iterationscheme](index.md)

# ParallelPerLevelIncreasing

**Source:** [Distributed_Design_Optimizer\coordination\innerloop_iterationscheme\ParallelPerLevelIncreasing.py](ParallelPerLevelIncreasing_source.md)

Level-by-level iteration scheme module.

This module provides an iteration scheme where subsystems at each level
are executed in parallel before moving to the next level.

## Classes

### ParallelPerLevelIncreasing

> **Inherits from:** [IterationSchemeBasis](IterationSchemeBasis.md#iterationschemebasis)

> Iteration scheme that executes subsystems level by level.

> This scheme processes subsystems by their level, executing all
> subsystems at the same level in parallel before moving to the next level.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the ParallelPerLevelIncreasing iteration scheme.


??? abstract "run_innerloop_jobs_multiprocessing(self, subsystemsIn: List[[SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)]) → Tuple[List[[SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)], List[int]]"
    Execute inner loop jobs level by level using multiprocessing.

    Subsystems are grouped by their subsystem level and executed in parallel
    within each level. Processing proceeds from level 0 upward.


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

