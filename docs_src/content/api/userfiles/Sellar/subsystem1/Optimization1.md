---
title: Optimization1
---

← Back to [subsystem1](index.md)

# Optimization1

**Source:** [userfiles\Sellar\subsystem1\Optimization1.py](Optimization1_source.md)

Optimization configuration module for Sellar subsystem 1.

Configures the local optimization algorithm for subsystem 1 in the Sellar
distributed optimization problem.

## Classes

### Optimization1

> **Inherits from:** [OptimizationBasis](../../../Distributed_Design_Optimizer/subsystem/optimization/OptimizationBasis.md#optimizationbasis)

> Optimization configuration class for Sellar subsystem 1.

> Configures the local optimizer (PyNomadBBO by default) and its
> hyperparameters for solving the subsystem-level subproblem.


> **Attributes:**
> > _optimizer: The configured optimizer instance.

#### Methods

??? abstract "__init__(self) → None"
    Initialize Optimization1 with selected optimizer settings.

