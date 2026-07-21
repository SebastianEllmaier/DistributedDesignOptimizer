---
title: Optimization1
---

← Back to [subsystem1](index.md)

# Optimization1

**Source:** [userfiles\SpeedReducer\subsystem1\Optimization1.py](Optimization1_source.md)

Optimization configuration module for Speed Reducer subsystem 1.

Configures the local optimization algorithm for shaft 1 in the Speed
Reducer distributed optimization problem.

## Classes

### Optimization1

> **Inherits from:** [OptimizationBasis](../../../Distributed_Design_Optimizer/subsystem/optimization/OptimizationBasis.md#optimizationbasis)

> Optimization configuration class for Speed Reducer subsystem 1.

> Configures the local optimizer (PyNomadBBO by default) and its
> hyperparameters for solving the shaft 1 subproblem.


> **Attributes:**
> > _optimizer: The configured optimizer instance.

#### Methods

??? abstract "__init__(self) → None"
    Initialize Optimization1 with selected optimizer settings.

