---
title: Optimization0
---

← Back to [subsystem0](index.md)

# Optimization0

**Source:** [userfiles\TwoBarTruss\subsystem0\Optimization0.py](Optimization0_source.md)

Optimization configuration module for Two-Bar Truss subsystem 0.

Configures the local optimization algorithm for the system-level FEM
subsystem in the Two-Bar Truss distributed optimization problem.

## Classes

### Optimization0

> **Inherits from:** [OptimizationBasis](../../../Distributed_Design_Optimizer/subsystem/optimization/OptimizationBasis.md#optimizationbasis)

> Optimization configuration class for Two-Bar Truss subsystem 0.

> Configures the local optimizer (PyNomadBBO by default) and its
> hyperparameters for solving the system-level subproblem.


> **Attributes:**
> > _optimizer: The configured optimizer instance.

#### Methods

??? abstract "__init__(self) → None"
    Initialize Optimization0 with selected optimizer settings.

