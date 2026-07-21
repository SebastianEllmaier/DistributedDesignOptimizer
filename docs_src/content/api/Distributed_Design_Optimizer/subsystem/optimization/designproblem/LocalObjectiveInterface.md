---
title: LocalObjectiveInterface
---

← Back to [designproblem](index.md)

# LocalObjectiveInterface

**Source:** [Distributed_Design_Optimizer\subsystem\optimization\designproblem\LocalObjectiveInterface.py](LocalObjectiveInterface_source.md)

Local objective interface module.

This module defines the abstract interface for local subsystem objectives.

## Classes

### LocalObjectiveInterface

> **Inherits from:** `ABC`

> Interface for the class that defines the local objective function value.

#### Methods

??? abstract "evaluateLocalObjective(self, subsystem: [SubSystemInterface](../../SubSystemInterface.md#subsysteminterface)) → None"
    Evaluate the objective function of a subsystem.


    **Args:**
    > subsystem: The subsystem interface for which the local objective  
    > function is evaluated.  

??? abstract "evaluate_Gradient_LocalObjective(self, subsystem: [SubSystemInterface](../../SubSystemInterface.md#subsysteminterface)) → None"
    Evaluate the gradient of the objective function for the components that are known.


    **Args:**
    > subsystem: The subsystem interface for which the gradient is  
    > evaluated.  

??? abstract "evaluate_Hessian_LocalObjective(self, subsystem: [SubSystemInterface](../../SubSystemInterface.md#subsysteminterface)) → None"
    Evaluate the Hessian of the objective function for the components that are known.


    **Args:**
    > subsystem: The subsystem interface for which the Hessian is  
    > evaluated.  

