---
title: Analysis0
---

← Back to [subsystem0](index.md)

# Analysis0

**Source:** [userfiles\TwoBarTruss\subsystem0\Analysis0.py](Analysis0_source.md)

Analysis module for Two-Bar Truss subsystem 0 (system-level FEM).

Implements the finite element analysis for the Two-Bar Truss structure,
computing mass, displacement, and internal forces from support locations
and cross-sectional areas.

## Classes

### Analysis0

> **Inherits from:** [AnalysisInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/AnalysisInterface.md#analysisinterface)

> Analysis class for Two-Bar Truss subsystem 0 (system-level).

> Performs FEM analysis to compute total mass, tip displacement,
> internal forces in both bars, and bar lengths.


> **Attributes:**
> > None specific to this class; inherits from AnalysisInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize Analysis0 instance.

??? abstract "evaluateLocalResponses(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the FEM analysis for the Two-Bar Truss system.

    Computes total mass, tip displacement, internal forces in both bars,
    and bar length L2 from support locations and cross-sectional areas.


    **Args:**
    > subsystem: The local subsystem basis containing design variables  
    > and scaling information.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Map computed responses to neighboring subsystems.

    Maps internal force f1 to subsystem 1 and internal force f2 with
    bar length L2 to subsystem 2 for coupling consistency.


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

