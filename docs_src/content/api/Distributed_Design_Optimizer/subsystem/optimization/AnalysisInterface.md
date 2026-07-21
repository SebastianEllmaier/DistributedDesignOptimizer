---
title: AnalysisInterface
---

← Back to [optimization](index.md)

# AnalysisInterface

**Source:** [Distributed_Design_Optimizer\subsystem\optimization\AnalysisInterface.py](AnalysisInterface_source.md)

Analysis interface module.

This module defines the abstract interface for subsystem analysis components.

## Classes

### AnalysisInterface

> **Inherits from:** `ABC`

> Interface prescribing the methods which an analysis code object needs to implement.

#### Methods

??? abstract "evaluateLocalResponses(self, subsystem: [SubSystemInterface](../SubSystemInterface.md#subsysteminterface)) → None"
    Evaluate the responses of a subsystem.


    **Args:**
    > subsystem: The subsystem interface for which responses are  
    > evaluated.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: [SubSystemInterface](../SubSystemInterface.md#subsysteminterface)) → None"
    Map the physical responses and design variables onto the neighboring subsystems.


    **Args:**
    > subsystem: The subsystem interface for which responses and design  
    > variables are mapped.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters_Jacobians(self, subsystem: [SubSystemInterface](../SubSystemInterface.md#subsysteminterface)) → None"
    Map the Jacobians of the mapped responses.


    **Args:**
    > subsystem: The subsystem interface for which the Jacobians are  
    > mapped.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian(self, subsystem: [SubSystemInterface](../SubSystemInterface.md#subsysteminterface)) → List[List[List[List[float | None]]]] | None"
    Map the Hessians of the mapped responses, if known a priori.


    **Args:**
    > subsystem: The subsystem interface for which the Hessians are  
    > mapped.  


    **Returns:**
    > Nested list indexed by local-to-local coupling, then by mapped  
    > response component, then the 2D Hessian (n_design x n_design).  
    > None entries indicate values not provided (BFGS approximation used).  
    > Return None if no Hessians are provided at all.  

