---
title: ParallelOddThenEvenLevels
---

← Back to [innerloop_iterationscheme](index.md)

# ParallelOddThenEvenLevels

**Source:** [Distributed_Design_Optimizer\coordination\innerloop_iterationscheme\ParallelOddThenEvenLevels.py](ParallelOddThenEvenLevels_source.md)

Odd-even level iteration scheme module.

This module provides an iteration scheme where odd levels are solved first
in parallel, followed by even levels with updated values.

## Classes

### ParallelOddThenEvenLevels

> **Inherits from:** [IterationSchemeBasis](IterationSchemeBasis.md#iterationschemebasis)

> Iteration scheme that executes subsystems by level parity, odd levels first.

> All subsystems at odd levels are solved in parallel first, after which all
> subsystems at even levels are solved, also in parallel, using the updated
> targets and responses determined at the odd levels.
> For more reference, read Chapter 4 of Simon Tosseram's dissertation.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the ParallelOddThenEvenLevels iteration scheme.

??? abstract "run_innerloop_jobs_multiprocessing(self, subsystemsIn: List[[SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)]) → Tuple[List[[SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)], List[int]]"
    Run inner loop jobs using multiprocessing with odd-even level ordering.

    Executes all subsystems at odd levels (1, 3, 5, ...) in parallel first,
    then all subsystems at even levels (0, 2, 4, ...) in parallel.


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

