---
title: Optimization1
---

← Back to [subsystem1](index.md)

# Optimization1

**Source:** [userfiles\GeometricProgramming\subsystem1\Optimization1.py](Optimization1_source.md)

Optimization configuration for Subsystem 1 in the Geometric Programming problem.

This module defines the Optimization1 class which configures the local
optimization algorithm and its hyperparameters for Subsystem 1 in the
distributed design optimization framework.

## Classes

### Optimization1

> **Inherits from:** [OptimizationBasis](../../../Distributed_Design_Optimizer/subsystem/optimization/OptimizationBasis.md#optimizationbasis)

> Optimization configuration class for Subsystem 1.

> Configures the local optimization algorithm (PyNomadBBO by default) for
> solving the subproblem of Subsystem 1 in the Geometric Programming problem.


> **Attributes:**
> > _optimizer: The optimization algorithm instance configured with  
> > appropriate hyperparameters for this subsystem.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the Optimization1 instance with the selected optimizer.

