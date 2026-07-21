---
title: LocalObjective1
---

← Back to [subsystem1](index.md)

# LocalObjective1

**Source:** [userfiles\Sellar\subsystem1\LocalObjective1.py](LocalObjective1_source.md)

Local objective module for Sellar subsystem 1.

Defines the local objective function contribution from subsystem 1
in the Sellar distributed optimization problem.

## Classes

### LocalObjective1

> **Inherits from:** [LocalObjectiveInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/designproblem/LocalObjectiveInterface.md#localobjectiveinterface)

> Local objective class for Sellar subsystem 1.

> Subsystem 1 has no local objective contribution (set to None).


> **Attributes:**
> > None specific to this class; inherits from LocalObjectiveInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize LocalObjective1 instance.

??? abstract "evaluateLocalObjective(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the local objective function for subsystem 1.


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

