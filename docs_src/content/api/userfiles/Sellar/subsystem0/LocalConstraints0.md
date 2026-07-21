---
title: LocalConstraints0
---

← Back to [subsystem0](index.md)

# LocalConstraints0

**Source:** [userfiles\Sellar\subsystem0\LocalConstraints0.py](LocalConstraints0_source.md)

Local constraints module for Sellar subsystem 0.

Defines the equality and inequality constraints local to subsystem 0
in the Sellar distributed optimization problem.

## Classes

### LocalConstraints0

> **Inherits from:** [LocalConstraintsInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/designproblem/LocalConstraintsInterface.md#localconstraintsinterface)

> Local constraints class for Sellar subsystem 0.

> Evaluates the local equality and inequality constraints for the
> first subsystem including the y1 constraint.


> **Attributes:**
> > None specific to this class; inherits from LocalConstraintsInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize LocalConstraints0 instance.

??? abstract "evaluateEqualityLocalConstraints(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate equality constraints for subsystem 0.


    **Args:**
    > subsystem: The local subsystem basis containing state information.  

??? abstract "evaluate_Jacobian_EqualityLocalConstraints(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the Jacobian of the local equality constraints.


    **Args:**
    > subsystem: The local subsystem basis containing state information.  

??? abstract "evaluate_Hessians_EqualityLocalConstraints(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the Hessians of the local equality constraints.


    **Args:**
    > subsystem: The local subsystem basis containing state information.  

??? abstract "evaluateInEqualityLocalConstraints(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate inequality constraints for subsystem 0.

    Computes the local inequality constraint: 3.16 - y1 >= 0.


    **Args:**
    > subsystem: The local subsystem basis containing state information.  

??? abstract "evaluate_Jacobian_InEqualityLocalConstraints(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the Jacobian of the local inequality constraints.


    **Args:**
    > subsystem: The local subsystem basis containing state information.  

??? abstract "evaluate_Hessians_InEqualityLocalConstraints(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the Hessians of the local inequality constraints.


    **Args:**
    > subsystem: The local subsystem basis containing state information.  

