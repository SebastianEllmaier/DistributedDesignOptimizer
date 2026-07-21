---
title: LocalObjective1
---

← Back to [subsystem1](index.md)

# LocalObjective1

**Source:** [userfiles\NewUseCase_Template\subsystem1\LocalObjective1.py](LocalObjective1_source.md)

Local objective module for Subsystem 1 in the new use-case.

This module defines the LocalObjective1 class which implements the local
objective function computation for Subsystem 1 in the distributed design
optimization framework.

## Classes

### LocalObjective1

> **Inherits from:** [LocalObjectiveInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/designproblem/LocalObjectiveInterface.md#localobjectiveinterface)

> Local objective class for Subsystem 1.

> Implements the LocalObjectiveInterface to compute the local objective
> function contribution for Subsystem 1 in the new use-case.
> This subsystem has no local objective (set to None).


> **Attributes:**
> > None specific to this class; inherits from LocalObjectiveInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the LocalObjective1 instance.

??? abstract "evaluateLocalObjective(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the local objective function for Subsystem 1.

    Computes the local objective value from the subsystem responses,
    scales it using the appropriate scaler, and stores the result
    in the subsystem.


    **Args:**
    > subsystem: The local subsystem instance providing responses  
    > and scaling variables.  

??? abstract "evaluate_Gradient_LocalObjective(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the gradient of the local objective function.


    **Args:**
    > subsystem: The local subsystem instance.  

??? abstract "evaluate_Hessian_LocalObjective(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the Hessian of the local objective function.


    **Args:**
    > subsystem: The local subsystem instance.  

