---
title: SolverInterface
---

← Back to [solver](index.md)

# SolverInterface

**Source:** [Distributed_Design_Optimizer\subsystem\optimization\solver\SolverInterface.py](SolverInterface_source.md)

Optimizer interface module.

This module defines the abstract interface for optimization algorithms.

## Classes

### SolverInterface

> **Inherits from:** `ABC`

> Abstract interface for optimization algorithm implementations.

> Defines the contract that all optimizer algorithms must implement.
> Each optimizer executes an optimization routine on a subsystem and
> returns the optimization results.

#### Methods

??? abstract "execute(self, subsystem: [SubSystemInterface](../../SubSystemInterface.md#subsysteminterface)) → [OptimDataBasis](../optimizerdata/OptimDataBasis.md#optimdatabasis)"
    Execute the optimization solver.


    **Args:**
    > subsystem: The subsystem to optimize.  


    **Returns:**
    > Optimization results containing design variables, objectives,  
    > constraints, and solver metadata.  

