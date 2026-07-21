---
title: Optimization0
---

← Back to [subsystem0](index.md)

# Optimization0

**Source:** [userfiles\SpeedReducer\subsystem0\Optimization0.py](Optimization0_source.md)

Optimization configuration module for Speed Reducer subsystem 0.

Configures the local optimization algorithm for the gear subsystem in the
Speed Reducer distributed optimization problem.

## Classes

### Optimization0

> **Inherits from:** [OptimizationBasis](../../../Distributed_Design_Optimizer/subsystem/optimization/OptimizationBasis.md#optimizationbasis)

> Optimization configuration class for Speed Reducer subsystem 0.

> Configures the local optimizer (PyNomadBBO by default) and its
> hyperparameters for solving the gear subsystem subproblem.


> **Attributes:**
> > _optimizer: The configured optimizer instance.

#### Methods

??? abstract "__init__(self) → None"
    Initialize Optimization0 with selected optimizer settings.

