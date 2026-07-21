---
title: LocalObjective0
---

← Back to [subsystem0](index.md)

# LocalObjective0

**Source:** [userfiles\SSBJ\subsystem0\LocalObjective0.py](LocalObjective0_source.md)

Local objective module for Subsystem 0 in the Supersonic Business Jet (SSBJ) problem.

## Classes

### LocalObjective0

> **Inherits from:** [LocalObjectiveInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/designproblem/LocalObjectiveInterface.md#localobjectiveinterface)

> Local objective class for Subsystem 0: minimize total aircraft weight.


> **Attributes:**
> > None specific to this class; inherits from LocalObjectiveInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize LocalObjective0 instance.

??? abstract "evaluateLocalObjective(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the local objective function for Subsystem 0.


    **Args:**
    > subsystem: The local subsystem basis containing state information.  

??? abstract "evaluate_Gradient_LocalObjective(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the gradient of the local objective function.


    **Args:**
    > subsystem: Local subsystem instance.  

??? abstract "evaluate_Hessian_LocalObjective(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the Hessian of the local objective function.


    **Args:**
    > subsystem: Local subsystem instance.  

