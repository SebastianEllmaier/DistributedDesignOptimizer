---
title: Analysis3
---

← Back to [subsystem3](index.md)

# Analysis3

**Source:** [userfiles\SSBJ\subsystem3\Analysis3.py](Analysis3_source.md)

Analysis module for Subsystem 3 in the Supersonic Business Jet (SSBJ) problem.

This module defines the Analysis3 class which implements the physics-based
analysis computations and response mapping for Subsystem 3 in the distributed
design optimization framework.

## Classes

### Analysis3

> **Inherits from:** [AnalysisInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/AnalysisInterface.md#analysisinterface)

> Analysis class for Subsystem 3 in the Supersonic Business Jet (SSBJ) problem.


> **Attributes:**
> > None specific to this class; inherits from AnalysisInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the Analysis3 instance.

??? abstract "evaluateLocalResponses(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the physical responses of Subsystem 3.

    Computes the subsystem responses based on the current design variables.


    **Args:**
    > subsystem: The LocalSubSystemBasis instance containing design variables  
    > and where computed responses will be stored.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Map responses and design variables for inter-subsystem coupling.


    **Args:**
    > subsystem: The LocalSubSystemBasis instance containing responses  
    > and design variables to be mapped.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters_Jacobians(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Map the Jacobians of the mapped responses.


    **Args:**
    > subsystem: The subsystem for which the Jacobians are mapped.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Map the Hessians of the mapped responses, if known a priori.


    **Args:**
    > subsystem: The subsystem for which the Hessians are mapped.  

