---
title: IterationSchemeBasis
---

← Back to [innerloop_iterationscheme](index.md)

# IterationSchemeBasis

**Source:** [Distributed_Design_Optimizer\coordination\innerloop_iterationscheme\IterationSchemeBasis.py](IterationSchemeBasis_source.md)

Base class module for inner loop iteration schemes.

This module provides the base class with common functionality for iteration
schemes, including the shared run_subsystem helper method.

## Classes

### IterationSchemeBasis

> **Inherits from:** [IterationSchemeInterface](IterationSchemeInterface.md#iterationschemeinterface)

> Base class for inner loop iteration schemes.

> Provides common functionality shared by all iteration scheme implementations,
> including the run_subsystem helper method for multiprocessing execution.
> Concrete iteration schemes should inherit from this class.

> Note: The abstract method run_innerloop_jobs_multiprocessing() is inherited
> from IterationSchemeInterface and must be implemented by concrete subclasses.

#### Methods

??? abstract "run_subsystem(subsystem: [SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)) → [SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)"
    Execute a single subsystem's inner loop job.

    Helper function used by multiprocessing to execute subsystems.
    Defined once here to avoid code duplication across all iteration schemes.


    **Args:**
    > subsystem: The subsystem to execute.  


    **Returns:**
    > The executed subsystem with updated state.  

