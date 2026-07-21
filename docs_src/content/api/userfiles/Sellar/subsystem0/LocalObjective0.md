---
title: LocalObjective0
---

← Back to [subsystem0](index.md)

# LocalObjective0

**Source:** [userfiles\Sellar\subsystem0\LocalObjective0.py](LocalObjective0_source.md)

Local objective module for Sellar subsystem 0.

Defines the local objective function contribution from subsystem 0
in the Sellar distributed optimization problem.

## Classes

### LocalObjective0

> **Inherits from:** [LocalObjectiveInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/designproblem/LocalObjectiveInterface.md#localobjectiveinterface)

> Local objective class for Sellar subsystem 0.

> Evaluates the local objective contribution: x1^2 + z2 + y1 + exp(-y2).


> **Attributes:**
> > None specific to this class; inherits from LocalObjectiveInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize LocalObjective0 instance.

??? abstract "evaluateLocalObjective(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the local objective function for subsystem 0.


    **Args:**
    > subsystem: The local subsystem basis containing state information.  

??? abstract "evaluate_Gradient_LocalObjective(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Compute the gradient of the local objective function.


    **Args:**
    > subsystem: The local subsystem basis containing state information.  

??? abstract "evaluate_Hessian_LocalObjective(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Compute the Hessian of the local objective function.


    **Args:**
    > subsystem: The local subsystem basis containing state information.  

