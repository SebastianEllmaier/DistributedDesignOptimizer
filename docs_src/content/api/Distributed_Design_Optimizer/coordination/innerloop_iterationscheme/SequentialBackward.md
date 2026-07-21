---
title: SequentialBackward
---

← Back to [innerloop_iterationscheme](index.md)

# SequentialBackward

**Source:** [Distributed_Design_Optimizer\coordination\innerloop_iterationscheme\SequentialBackward.py](SequentialBackward_source.md)

Bottom-up sequential iteration scheme module.

This module provides an iteration scheme where subsystems are executed
sequentially from lowest to highest hierarchical level.

## Classes

### SequentialBackward

> **Inherits from:** [IterationSchemeBasis](IterationSchemeBasis.md#iterationschemebasis)

> Iteration scheme that executes subsystems sequentially in bottom-up order.

> This scheme runs subsystems one at a time, starting from the
> lowest level and working up to the highest level (reverse order).

#### Methods

??? abstract "__init__(self) → None"
    Initialize the SequentialBackward iteration scheme.


??? abstract "run_innerloop_jobs_multiprocessing(self, subsystemsIn: List[[SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)]) → Tuple[List[[SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)], List[int]]"
    Execute inner loop jobs sequentially in bottom-up order using multiprocessing.

    Subsystems are processed one at a time in reverse order (bottom-up),
    using a process pool with blocking apply calls.


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

