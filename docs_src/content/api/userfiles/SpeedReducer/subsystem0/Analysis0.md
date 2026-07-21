---
title: Analysis0
---

← Back to [subsystem0](index.md)

# Analysis0

**Source:** [userfiles\SpeedReducer\subsystem0\Analysis0.py](Analysis0_source.md)

Analysis module for Speed Reducer subsystem 0.

Implements the disciplinary analysis for the gear subsystem in the Speed
Reducer problem, handling the shared design variables z1, z2, z3.

## Classes

### Analysis0

> **Inherits from:** [AnalysisInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/AnalysisInterface.md#analysisinterface)

> Analysis class for Speed Reducer subsystem 0 (gear subsystem).

> Computes the physical responses related to gear face width, tooth module,
> and number of teeth from the shared design variables.


> **Attributes:**
> > None specific to this class; inherits from AnalysisInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize Analysis0 instance.

??? abstract "evaluateLocalResponses(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate subsystem responses for the gear subsystem.

    Computes physical responses related to gear face width, tooth module,
    and number of teeth from the shared design variables z1, z2, z3.


    **Args:**
    > subsystem: The local subsystem containing design variables and scalers.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Map subsystem responses to neighboring subsystems.

    Distributes shared design variables z1, z2, z3 to both shaft
    subsystems (subsystem 1 and subsystem 2).


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

