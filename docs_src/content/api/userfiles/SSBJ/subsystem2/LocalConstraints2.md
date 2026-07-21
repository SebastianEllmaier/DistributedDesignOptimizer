---
title: LocalConstraints2
---

← Back to [subsystem2](index.md)

# LocalConstraints2

**Source:** [userfiles\SSBJ\subsystem2\LocalConstraints2.py](LocalConstraints2_source.md)

Local constraints module for Subsystem 2 in the Supersonic Business Jet (SSBJ) problem.

This module defines the LocalConstraints2 class which implements the local
equality and inequality constraints specific to Subsystem 2 in the distributed
design optimization framework.

## Classes

### LocalConstraints2

> **Inherits from:** [LocalConstraintsInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/designproblem/LocalConstraintsInterface.md#localconstraintsinterface)

> Local constraints class for Subsystem 2 in the Supersonic Business Jet (SSBJ) problem.


> **Attributes:**
> > None specific to this class; inherits from LocalConstraintsInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the LocalConstraints2 instance.

??? abstract "evaluateEqualityLocalConstraints(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate equality local constraints for Subsystem 2.

    Computes the equality constraint values from the subsystem responses,
    scales them using the appropriate ScalerConstraint, and stores the
    result in the subsystem.


    **Args:**
    > subsystem: The local subsystem instance providing responses  
    > and scaling variables.  

??? abstract "evaluate_Jacobian_EqualityLocalConstraints(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the Jacobian of the local equality constraints.


    **Args:**
    > subsystem: The local subsystem instance.  

??? abstract "evaluate_Hessians_EqualityLocalConstraints(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the Hessians of the local equality constraints.


    **Args:**
    > subsystem: The local subsystem instance.  

??? abstract "evaluateInEqualityLocalConstraints(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate inequality local constraints for Subsystem 2.

    Computes the inequality constraint values from the subsystem responses,
    scales them using the appropriate ScalerConstraint, and stores the
    result in the subsystem.


    **Args:**
    > subsystem: The local subsystem instance providing responses  
    > and scaling variables.  

??? abstract "evaluate_Jacobian_InEqualityLocalConstraints(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the Jacobian of the local inequality constraints.


    **Args:**
    > subsystem: The local subsystem instance.  

??? abstract "evaluate_Hessians_InEqualityLocalConstraints(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the Hessians of the local inequality constraints.


    **Args:**
    > subsystem: The local subsystem instance.  

