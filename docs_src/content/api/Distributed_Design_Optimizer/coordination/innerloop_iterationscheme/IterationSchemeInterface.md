---
title: IterationSchemeInterface
---

← Back to [innerloop_iterationscheme](index.md)

# IterationSchemeInterface

**Source:** [Distributed_Design_Optimizer\coordination\innerloop_iterationscheme\IterationSchemeInterface.py](IterationSchemeInterface_source.md)

Interface module for inner loop iteration schemes.

This module defines the abstract base class for iteration schemes that
control how subsystems are executed during inner loop iterations.

## Classes

### IterationSchemeInterface

> **Inherits from:** `ABC`

> Abstract base class for inner loop iteration schemes.

> Defines the interface for different strategies to execute hierarchic
> subsystems during inner loop iterations.

#### Methods

??? abstract "run_innerloop_jobs_multiprocessing(self, subsystemsIn: List[[SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)]) → Tuple[List[[SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)], List[int]]"
    Execute inner loop jobs using multiprocessing.


    **Args:**
    > subsystemsIn: List of subsystems to execute.  


    **Returns:**
    > Tuple containing the list of executed subsystems and their indices.  

??? abstract "print_startup_summary(self) → None"
    Print the iteration scheme configuration at startup.

??? abstract "print_termination_summary(self) → None"
    Print the iteration scheme configuration at the end.

??? abstract "print_beginning_of_run_innerloop_jobs_multiprocessing(self) → None"
    Print a banner before executing inner loop jobs via multiprocessing.

