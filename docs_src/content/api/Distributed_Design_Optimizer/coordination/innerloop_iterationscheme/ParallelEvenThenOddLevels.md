---
title: ParallelEvenThenOddLevels
---

← Back to [innerloop_iterationscheme](index.md)

# ParallelEvenThenOddLevels

**Source:** [Distributed_Design_Optimizer\coordination\innerloop_iterationscheme\ParallelEvenThenOddLevels.py](ParallelEvenThenOddLevels_source.md)

Even-odd level iteration scheme module.

This module provides an iteration scheme where even levels are solved first
in parallel, followed by odd levels with updated values.

## Classes

### ParallelEvenThenOddLevels

> **Inherits from:** [IterationSchemeBasis](IterationSchemeBasis.md#iterationschemebasis)

> Iteration scheme that executes subsystems by level parity, even levels first.

> All subsystems at even levels are solved in parallel first, after which all
> subsystems at odd levels are solved, also in parallel, using the updated
> targets and responses determined at the even levels.
> For more reference, read Chapter 4 of Simon Tosseram's dissertation.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the ParallelEvenThenOddLevels iteration scheme.

??? abstract "run_innerloop_jobs_multiprocessing(self, subsystemsIn: List[[SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)]) → Tuple[List[[SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)], List[int]]"
    Run inner loop jobs using multiprocessing with even-odd level ordering.

    Executes all subsystems at even levels (0, 2, 4, ...) in parallel first,
    then all subsystems at odd levels (1, 3, 5, ...) in parallel.


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

