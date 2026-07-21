---
title: Analysis1
---

← Back to [subsystem1](index.md)

# Analysis1

**Source:** [userfiles\Sellar\subsystem1\Analysis1.py](Analysis1_source.md)

Analysis module for Sellar subsystem 1.

Implements the disciplinary analysis for the second subsystem in the Sellar
multidisciplinary design problem, computing the y2 response variable.

## Classes

### Analysis1

> **Inherits from:** [AnalysisInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/AnalysisInterface.md#analysisinterface)

> Analysis class for Sellar subsystem 1.

> Computes the physical response y2 for the second discipline using
> the Sellar equations: y2 = sqrt(y1) + z1 + z2.


> **Attributes:**
> > None specific to this class; inherits from AnalysisInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize Analysis1 instance.

??? abstract "evaluateLocalResponses(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate subsystem responses using Sellar discipline 2 equations.

    Computes y2 from the design variables z1, z2 and coupling variable y1
    using the formula: y2 = sqrt(y1) + z1 + z2.


    **Args:**
    > subsystem: The local subsystem containing design variables and scalers.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Map subsystem responses to neighboring subsystems.

    Transforms y2 to scaled values and distributes coupling variable y1
    and target design variables z1, z2 to subsystem 0.


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

