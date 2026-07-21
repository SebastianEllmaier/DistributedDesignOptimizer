---
title: Analysis1
---

← Back to [subsystem1](index.md)

# Analysis1

**Source:** [userfiles\TwoBarTruss\subsystem1\Analysis1.py](Analysis1_source.md)

Analysis module for Two-Bar Truss subsystem 1 (bar 1 sizing).

Implements the analysis for bar 1 in the Two-Bar Truss structure,
computing cross-sectional area and stress from radius and thickness.

## Classes

### Analysis1

> **Inherits from:** [AnalysisInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/AnalysisInterface.md#analysisinterface)

> Analysis class for Two-Bar Truss subsystem 1 (bar 1).

> Computes cross-sectional area and axial stress for bar 1
> based on tube radius, thickness, and internal force.


> **Attributes:**
> > None specific to this class; inherits from AnalysisInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize Analysis1 instance.

??? abstract "evaluateLocalResponses(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate cross-sectional area and stress for bar 1.

    Computes the cross-sectional area from tube radius and thickness,
    then calculates axial stress from internal force.


    **Args:**
    > subsystem: The local subsystem basis containing design variables  
    > and scaling information.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Map computed responses to the parent subsystem.

    Maps cross-sectional area A1 and internal force f1 coupling
    variable back to subsystem 0.


    **Args:**
    > subsystem: The local subsystem basis containing response data  
    > and mapping interfaces.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters_Jacobians(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Map the Jacobians of the mapped responses.


    **Args:**
    > subsystem: The subsystem for which the Jacobians are mapped.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Map the Hessians of the mapped responses, if known a priori.


    **Args:**
    > subsystem: The subsystem for which the Hessians are mapped.  

