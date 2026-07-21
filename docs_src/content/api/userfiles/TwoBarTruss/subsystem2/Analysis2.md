---
title: Analysis2
---

← Back to [subsystem2](index.md)

# Analysis2

**Source:** [userfiles\TwoBarTruss\subsystem2\Analysis2.py](Analysis2_source.md)

Analysis module for Two-Bar Truss subsystem 2 (bar 2 sizing).

Implements the analysis for bar 2 (compression member) in the Two-Bar Truss
structure, computing stress, Euler buckling stress, and cross-sectional area.

## Classes

### Analysis2

> **Inherits from:** [AnalysisInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/AnalysisInterface.md#analysisinterface)

> Analysis class for Two-Bar Truss subsystem 2 (bar 2).

> Computes compressive stress, Euler buckling critical stress, and
> cross-sectional area for bar 2 based on geometry and loading.


> **Attributes:**
> > None specific to this class; inherits from AnalysisInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize Analysis2 instance.

??? abstract "evaluateLocalResponses(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate stress responses for bar 2 (compression member).

    Computes compressive stress, Euler buckling critical stress, and
    cross-sectional area from tube geometry and internal force.


    **Args:**
    > subsystem: The local subsystem basis containing design variables  
    > and scaling information.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Map computed responses to the parent subsystem.

    Maps cross-sectional area A2 and coupling variables (f2, L2)
    back to subsystem 0 for consistency.


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

