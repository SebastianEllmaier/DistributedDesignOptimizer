---
title: Optimization0
---

← Back to [subsystem0](index.md)

# Optimization0

**Source:** [userfiles\GeometricProgramming\subsystem0\Optimization0.py](Optimization0_source.md)

Optimization configuration for Subsystem 0 in the Geometric Programming problem.

This module defines the Optimization0 class which configures the local
optimization algorithm and its hyperparameters for Subsystem 0 in the
distributed design optimization framework.

## Classes

### Optimization0

> **Inherits from:** [OptimizationBasis](../../../Distributed_Design_Optimizer/subsystem/optimization/OptimizationBasis.md#optimizationbasis)

> Optimization configuration class for Subsystem 0.

> Configures the local optimization algorithm (PyNomadBBO by default) for
> solving the subproblem of Subsystem 0 in the Geometric Programming problem.


> **Attributes:**
> > _optimizer: The optimization algorithm instance configured with  
> > appropriate hyperparameters for this subsystem.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the Optimization0 instance with the selected optimizer.

