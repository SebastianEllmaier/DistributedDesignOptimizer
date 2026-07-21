---
title: OptimizationInterface
---

← Back to [optimization](index.md)

# OptimizationInterface

**Source:** [Distributed_Design_Optimizer\subsystem\optimization\OptimizationInterface.py](OptimizationInterface_source.md)

Optimization interface module.

This module defines the abstract interface for optimization components.

## Classes

### OptimizationInterface

> **Inherits from:** `ABC`

> Abstract interface for optimization execution.

> Defines the contract for classes that execute optimization algorithms
> on subsystems within the distributed design optimization framework.

#### Methods

??? abstract "callOptimizer(self, subsystemin: [SubSystemInterface](../SubSystemInterface.md#subsysteminterface)) → [OptimDataBasis](optimizerdata/OptimDataBasis.md#optimdatabasis)"
    Execute an optimization algorithm on the given subsystem.


    **Args:**
    > subsystemin: The subsystem to be optimized.  


    **Returns:**
    > The optimization results produced by the configured solver.  

