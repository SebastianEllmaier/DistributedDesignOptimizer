---
title: LocalConstraintsInterface
---

← Back to [designproblem](index.md)

# LocalConstraintsInterface

**Source:** [Distributed_Design_Optimizer\subsystem\optimization\designproblem\LocalConstraintsInterface.py](LocalConstraintsInterface_source.md)

Local constraints interface module.

This module defines the abstract interface for local subsystem constraints.

## Classes

### LocalConstraintsInterface

> **Inherits from:** `ABC`

> Interface that should be implemented by any local constraint class formulation.

#### Methods

??? abstract "evaluateEqualityLocalConstraints(self, subsystem: [SubSystemInterface](../../SubSystemInterface.md#subsysteminterface)) → None"
    Evaluate the equality local constraints.


    **Args:**
    > subsystem: The subsystem interface for which equality constraints  
    > are evaluated.  

??? abstract "evaluateInEqualityLocalConstraints(self, subsystem: [SubSystemInterface](../../SubSystemInterface.md#subsysteminterface)) → None"
    Evaluate the inequality local constraints.


    **Args:**
    > subsystem: The subsystem interface for which inequality constraints  
    > are evaluated.  

??? abstract "evaluate_Jacobian_EqualityLocalConstraints(self, subsystem: [SubSystemInterface](../../SubSystemInterface.md#subsysteminterface)) → None"
    Evaluate the Jacobian of the local equality constraints that are known to be computed.


    **Args:**
    > subsystem: The subsystem interface for which the Jacobian is  
    > evaluated.  

??? abstract "evaluate_Jacobian_InEqualityLocalConstraints(self, subsystem: [SubSystemInterface](../../SubSystemInterface.md#subsysteminterface)) → None"
    Evaluate the Jacobian of the local inequality constraints that are known to be computed.


    **Args:**
    > subsystem: The subsystem interface for which the Jacobian is  
    > evaluated.  

??? abstract "evaluate_Hessians_EqualityLocalConstraints(self, subsystem: [SubSystemInterface](../../SubSystemInterface.md#subsysteminterface)) → None"
    Evaluate the Hessians of the local equality constraints that are known to be computed.


    **Args:**
    > subsystem: The subsystem interface for which the Hessians are  
    > evaluated.  

??? abstract "evaluate_Hessians_InEqualityLocalConstraints(self, subsystem: [SubSystemInterface](../../SubSystemInterface.md#subsysteminterface)) → None"
    Evaluate the Hessians of the local inequality constraints that are known to be computed.


    **Args:**
    > subsystem: The subsystem interface for which the Hessians are  
    > evaluated.  

