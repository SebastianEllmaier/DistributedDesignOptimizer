---
title: LocalConstraints2
---

← Back to [subsystem2](index.md)

# LocalConstraints2

**Source:** [userfiles\TwoBarTruss\subsystem2\LocalConstraints2.py](LocalConstraints2_source.md)

Local constraints module for Two-Bar Truss subsystem 2.

Defines the buckling stability constraint for bar 2 (compression member)
in the Two-Bar Truss problem.

## Classes

### LocalConstraints2

> **Inherits from:** [LocalConstraintsInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/designproblem/LocalConstraintsInterface.md#localconstraintsinterface)

> Local constraints class for Two-Bar Truss subsystem 2.

> Evaluates the Euler buckling stability constraint for bar 2.


> **Attributes:**
> > None specific to this class; inherits from LocalConstraintsInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize LocalConstraints2 instance.

??? abstract "evaluateEqualityLocalConstraints(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate equality constraints for subsystem 2.


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
    Evaluate inequality constraints for subsystem 2.

    Computes the buckling constraint (sigma2 / sigma_Euler)**2 - 1 <= 0,
    magnitude-compressed via a sign/zero-crossing preserving power map so
    the feasible set is unchanged (see power_ratio below).


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

