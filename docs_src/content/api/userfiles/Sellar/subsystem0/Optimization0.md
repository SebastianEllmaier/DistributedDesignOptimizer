---
title: Optimization0
---

← Back to [subsystem0](index.md)

# Optimization0

**Source:** [userfiles\Sellar\subsystem0\Optimization0.py](Optimization0_source.md)

Optimization configuration module for Sellar subsystem 0.

Configures the local optimization algorithm for subsystem 0 in the Sellar
distributed optimization problem.

## Classes

### Optimization0

> **Inherits from:** [OptimizationBasis](../../../Distributed_Design_Optimizer/subsystem/optimization/OptimizationBasis.md#optimizationbasis)

> Optimization configuration class for Sellar subsystem 0.

> Configures the local optimizer (PyNomadBBO by default) and its
> hyperparameters for solving the subsystem-level subproblem.


> **Attributes:**
> > _optimizer: The configured optimizer instance.

#### Methods

??? abstract "__init__(self) → None"
    Initialize Optimization0 with selected optimizer settings.

