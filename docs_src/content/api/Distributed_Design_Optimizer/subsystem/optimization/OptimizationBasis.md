---
title: OptimizationBasis
---

← Back to [optimization](index.md)

# OptimizationBasis

**Source:** [Distributed_Design_Optimizer\subsystem\optimization\OptimizationBasis.py](OptimizationBasis_source.md)

Optimization basis module.

This module provides the base class for optimization implementations.

## Classes

### OptimizationBasis

> **Inherits from:** [OptimizationInterface](OptimizationInterface.md#optimizationinterface)

> Base implementation of the optimization interface.

> Provides the foundational optimization functionality for subsystem optimization,
> delegating the actual optimization to a configured optimizer algorithm.

#### Methods

??? abstract "__init__(self, optimizer: [SolverInterface](solver/SolverInterface.md#solverinterface)) → None"
    Initialize the optimization basis with the solver to delegate to.


    **Args:**
    > optimizer: The solver algorithm used to optimize the subsystem.  

??? abstract "callOptimizer(self, subsystemin: [SubSystemInterface](../SubSystemInterface.md#subsysteminterface)) → [OptimDataBasis](optimizerdata/OptimDataBasis.md#optimdatabasis)"
    Execute the optimizer on the given subsystem.

    Runs the configured optimizer algorithm on the subsystem and returns
    the optimization results.


    **Args:**
    > subsystemin: The subsystem to be optimized.  


    **Returns:**
    > The optimization results produced by the configured solver.  

??? abstract "get_Optimizer(self) → [SolverInterface](solver/SolverInterface.md#solverinterface)"
    Return the solver algorithm configured for this optimization.


    **Returns:**
    > The solver instance that this optimization delegates to.  

