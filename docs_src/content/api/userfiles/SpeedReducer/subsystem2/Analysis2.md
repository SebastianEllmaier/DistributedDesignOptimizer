---
title: Analysis2
---

← Back to [subsystem2](index.md)

# Analysis2

**Source:** [userfiles\SpeedReducer\subsystem2\Analysis2.py](Analysis2_source.md)

Analysis module for Speed Reducer subsystem 2.

Implements the disciplinary analysis for shaft 2 in the Speed Reducer problem,
computing shaft dimensions and strength-related responses.

## Classes

### Analysis2

> **Inherits from:** [AnalysisInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/AnalysisInterface.md#analysisinterface)

> Analysis class for Speed Reducer subsystem 2 (shaft 2).

> Computes physical responses for shaft 2 including diameter, length,
> and coupling with the gear subsystem.


> **Attributes:**
> > None specific to this class; inherits from AnalysisInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize Analysis2 instance.

??? abstract "evaluateLocalResponses(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate subsystem responses for shaft 2.

    Computes physical responses for shaft 2 including diameter, length,
    and shared design variables from the gear subsystem.


    **Args:**
    > subsystem: The local subsystem containing design variables and scalers.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Map subsystem responses to neighboring subsystems.

    Distributes target design variables z1, z2, z3 to both subsystem 0
    (gear) and subsystem 1 (shaft 1).


    **Args:**
    > subsystem: The local subsystem containing responses and scalers.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters_Jacobians(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Map the Jacobians of the mapped responses.


    **Args:**
    > subsystem: The subsystem for which the Jacobians are mapped.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Map the Hessians of the mapped responses, if known a priori.


    **Args:**
    > subsystem: The subsystem for which the Hessians are mapped.  

