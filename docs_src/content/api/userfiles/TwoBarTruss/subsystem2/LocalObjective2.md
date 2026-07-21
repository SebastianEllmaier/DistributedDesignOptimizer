---
title: LocalObjective2
---

← Back to [subsystem2](index.md)

# LocalObjective2

**Source:** [userfiles\TwoBarTruss\subsystem2\LocalObjective2.py](LocalObjective2_source.md)

Local objective module for Two-Bar Truss subsystem 2.

Defines the local objective function contribution from bar 2
(no local objective contribution in this decomposition).

## Classes

### LocalObjective2

> **Inherits from:** [LocalObjectiveInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/designproblem/LocalObjectiveInterface.md#localobjectiveinterface)

> Local objective class for Two-Bar Truss subsystem 2.

> Bar 2 has no local objective contribution (set to 0.0).


> **Attributes:**
> > None specific to this class; inherits from LocalObjectiveInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize LocalObjective2 instance.

??? abstract "evaluateLocalObjective(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the local objective function for subsystem 2.


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

