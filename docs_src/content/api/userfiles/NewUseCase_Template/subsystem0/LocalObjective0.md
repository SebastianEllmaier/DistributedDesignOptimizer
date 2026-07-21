---
title: LocalObjective0
---

← Back to [subsystem0](index.md)

# LocalObjective0

**Source:** [userfiles\NewUseCase_Template\subsystem0\LocalObjective0.py](LocalObjective0_source.md)

Local objective module for Subsystem 0 in the new use-case.

This module defines the LocalObjective0 class which implements the local
objective function computation for Subsystem 0 in the distributed design
optimization framework.

## Classes

### LocalObjective0

> **Inherits from:** [LocalObjectiveInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/designproblem/LocalObjectiveInterface.md#localobjectiveinterface)

> Local objective class for Subsystem 0.

> Implements the LocalObjectiveInterface to compute the local objective
> function contribution for Subsystem 0 in the new use-case.
> This subsystem has a non-zero local objective based on the computed responses.


> **Attributes:**
> > None specific to this class; inherits from LocalObjectiveInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the LocalObjective0 instance.

??? abstract "evaluateLocalObjective(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the local objective function for Subsystem 0.

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

