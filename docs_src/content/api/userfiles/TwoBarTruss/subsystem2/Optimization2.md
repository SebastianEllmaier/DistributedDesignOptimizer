---
title: Optimization2
---

← Back to [subsystem2](index.md)

# Optimization2

**Source:** [userfiles\TwoBarTruss\subsystem2\Optimization2.py](Optimization2_source.md)

Optimization configuration module for Two-Bar Truss subsystem 2.

Configures the local optimization algorithm for bar 2 sizing in the
Two-Bar Truss distributed optimization problem.

## Classes

### Optimization2

> **Inherits from:** [OptimizationBasis](../../../Distributed_Design_Optimizer/subsystem/optimization/OptimizationBasis.md#optimizationbasis)

> Optimization configuration class for Two-Bar Truss subsystem 2.

> Configures the local optimizer (PyNomadBBO by default) and its
> hyperparameters for solving the bar 2 sizing subproblem.


> **Attributes:**
> > _optimizer: The configured optimizer instance.

#### Methods

??? abstract "__init__(self) → None"
    Initialize Optimization2 with selected optimizer settings.

