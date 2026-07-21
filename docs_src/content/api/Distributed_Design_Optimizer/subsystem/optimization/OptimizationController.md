---
title: OptimizationController
---

← Back to [optimization](index.md)

# OptimizationController

**Source:** [Distributed_Design_Optimizer\subsystem\optimization\OptimizationController.py](OptimizationController_source.md)

Optimization controller module.

This module provides the QP-based optimization for the ALADIN
controller subsystem.

## Classes

### OptimizationController

> **Inherits from:** [OptimizationBasis](OptimizationBasis.md#optimizationbasis)

> QP-based optimization for the ALADIN controller subsystem.

> Configures OptimizationBasis with a quadratic programming solver and
> exposes it through get_Optimizer so the controller subsystem can populate
> the QP problem matrices (P, q, A, G, h).

#### Methods

??? abstract "__init__(self) → None"
    Initialize OptimizationController with a QP solver.

??? abstract "get_Optimizer(self) → [Solver_QP](solver/Solver_QP.md#solver_qp)"
    Return the QP solver configured for the controller.


    **Returns:**
    > The quadratic programming solver instance.  

