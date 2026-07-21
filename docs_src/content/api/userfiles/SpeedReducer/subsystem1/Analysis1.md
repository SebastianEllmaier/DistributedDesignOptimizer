---
title: Analysis1
---

← Back to [subsystem1](index.md)

# Analysis1

**Source:** [userfiles\SpeedReducer\subsystem1\Analysis1.py](Analysis1_source.md)

Analysis module for Speed Reducer subsystem 1.

Implements the disciplinary analysis for shaft 1 in the Speed Reducer problem,
computing shaft dimensions and strength-related responses.

## Classes

### Analysis1

> **Inherits from:** [AnalysisInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/AnalysisInterface.md#analysisinterface)

> Analysis class for Speed Reducer subsystem 1 (shaft 1).

> Computes physical responses for shaft 1 including diameter, length,
> and coupling with the gear subsystem.


> **Attributes:**
> > None specific to this class; inherits from AnalysisInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize Analysis1 instance.

??? abstract "evaluateLocalResponses(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate subsystem responses for shaft 1.

    Computes physical responses for shaft 1 including diameter, length,
    and shared design variables from the gear subsystem.


    **Args:**
    > subsystem: The local subsystem containing design variables and scalers.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Map subsystem responses to neighboring subsystems.

    Distributes target design variables z1, z2, z3 to subsystem 0 and
    shared design variables to subsystem 2.


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

