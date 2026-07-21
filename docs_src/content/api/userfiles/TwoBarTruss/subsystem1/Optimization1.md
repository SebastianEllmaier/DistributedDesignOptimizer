---
title: Optimization1
---

← Back to [subsystem1](index.md)

# Optimization1

**Source:** [userfiles\TwoBarTruss\subsystem1\Optimization1.py](Optimization1_source.md)

Optimization configuration module for Two-Bar Truss subsystem 1.

Configures the local optimization algorithm for bar 1 sizing in the
Two-Bar Truss distributed optimization problem.

## Classes

### Optimization1

> **Inherits from:** [OptimizationBasis](../../../Distributed_Design_Optimizer/subsystem/optimization/OptimizationBasis.md#optimizationbasis)

> Optimization configuration class for Two-Bar Truss subsystem 1.

> Configures the local optimizer (PyNomadBBO by default) and its
> hyperparameters for solving the bar 1 sizing subproblem.


> **Attributes:**
> > _optimizer: The configured optimizer instance.

#### Methods

??? abstract "__init__(self) → None"
    Initialize Optimization1 with selected optimizer settings.

