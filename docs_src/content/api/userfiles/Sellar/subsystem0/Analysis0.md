---
title: Analysis0
---

← Back to [subsystem0](index.md)

# Analysis0

**Source:** [userfiles\Sellar\subsystem0\Analysis0.py](Analysis0_source.md)

Analysis module for Sellar subsystem 0.

Implements the disciplinary analysis for the first subsystem in the Sellar
multidisciplinary design problem, computing response variables from design
variables and coupling variables.

## Classes

### Analysis0

> **Inherits from:** [AnalysisInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/AnalysisInterface.md#analysisinterface)

> Analysis class for Sellar subsystem 0.

> Computes the physical responses y1 and related quantities for the
> first discipline using the Sellar equations.


> **Attributes:**
> > None specific to this class; inherits from AnalysisInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize Analysis0 instance.

??? abstract "evaluateLocalResponses(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate subsystem responses using Sellar discipline 1 equations.

    Computes y1 and related physical responses from the design variables
    and coupling variables using the Sellar problem formulation.


    **Args:**
    > subsystem: The local subsystem containing design variables and scalers.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Map subsystem responses to neighboring subsystems.

    Transforms y1 to scaled values and distributes coupling variables
    y2 and shared design variables z1, z2 to subsystem 1.


    **Args:**
    > subsystem: The local subsystem containing responses and scalers.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters_Jacobians(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Map the Jacobians of the mapped responses.


    **Args:**
    > subsystem: The subsystem for which the Jacobians are mapped.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → List[List[List[List[float | None]]]] | None"
    Map the Hessians of the mapped responses, if known a priori.


    **Args:**
    > subsystem: The subsystem for which the Hessians are mapped.  


    **Returns:**
    > The mapped-response Hessian tensor  
    > [coupling][mapped_response][n_dv][n_dv], or None for finite differences.  

