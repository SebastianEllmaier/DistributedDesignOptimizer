---
title: LocalObjective0
---

← Back to [subsystem0](index.md)

# LocalObjective0

**Source:** [userfiles\TwoBarTruss\subsystem0\LocalObjective0.py](LocalObjective0_source.md)

Local objective module for Two-Bar Truss subsystem 0.

Defines the mass objective function for the system-level FEM subsystem.

## Classes

### LocalObjective0

> **Inherits from:** [LocalObjectiveInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/designproblem/LocalObjectiveInterface.md#localobjectiveinterface)

> Local objective class for Two-Bar Truss subsystem 0.

> Evaluates total truss mass normalized by the mass-normalization parameter.


> **Attributes:**
> > None specific to this class; inherits from LocalObjectiveInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize LocalObjective0 instance.

??? abstract "evaluateLocalObjective(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the local objective function for subsystem 0.

    Computes the normalized mass objective M / M_max.


    **Args:**
    > subsystem: The local subsystem basis containing state information.  

??? abstract "evaluate_Gradient_LocalObjective(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the gradient of the local objective function.


    **Args:**
    > subsystem: The local subsystem basis containing state information.  

??? abstract "evaluate_Hessian_LocalObjective(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the Hessian of the local objective function.


    **Args:**
    > subsystem: The local subsystem basis containing state information.  

