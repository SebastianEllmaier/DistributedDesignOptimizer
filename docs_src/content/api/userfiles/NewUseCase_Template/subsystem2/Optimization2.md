---
title: Optimization2
---

← Back to [subsystem2](index.md)

# Optimization2

**Source:** [userfiles\NewUseCase_Template\subsystem2\Optimization2.py](Optimization2_source.md)

Optimization configuration for Subsystem 2 in the new use-case.

This module defines the Optimization2 class which configures the local
optimization algorithm and its hyperparameters for Subsystem 2 in the
distributed design optimization framework.

## Classes

### Optimization2

> **Inherits from:** [OptimizationBasis](../../../Distributed_Design_Optimizer/subsystem/optimization/OptimizationBasis.md#optimizationbasis)

> Optimization configuration class for Subsystem 2.

> Configures the local optimization algorithm (PyNomadBBO by default) for
> solving the subproblem of Subsystem 2 in the new use-case.


> **Attributes:**
> > _optimizer: The optimization algorithm instance configured with  
> > appropriate hyperparameters for this subsystem.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the Optimization2 instance with the selected optimizer.

