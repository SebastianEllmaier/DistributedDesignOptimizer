---
title: LocalObjective2
---

← Back to [subsystem2](index.md)

# LocalObjective2

**Source:** [userfiles\SpeedReducer\subsystem2\LocalObjective2.py](LocalObjective2_source.md)

Local objective module for Speed Reducer subsystem 2.

Defines the local objective function contribution from shaft 2
to the total weight objective.

## Classes

### LocalObjective2

> **Inherits from:** [LocalObjectiveInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/designproblem/LocalObjectiveInterface.md#localobjectiveinterface)

> Local objective class for Speed Reducer subsystem 2.

> Evaluates the shaft 2 weight contribution to the total reducer weight.


> **Attributes:**
> > None specific to this class; inherits from LocalObjectiveInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize LocalObjective2 instance.

??? abstract "evaluateLocalObjective(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the local objective function for subsystem 2.

    Computes the shaft 2 weight contribution to total reducer weight.


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

