---
title: Analysis2
---

← Back to [subsystem2](index.md)

# Analysis2

**Source:** [userfiles\SSBJ\subsystem2\Analysis2.py](Analysis2_source.md)

Analysis module for Subsystem 2 in the Supersonic Business Jet (SSBJ) problem.

This module defines the Analysis2 class which implements the physics-based
analysis computations and response mapping for Subsystem 2 in the distributed
design optimization framework.

## Classes

### Analysis2

> **Inherits from:** [AnalysisInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/AnalysisInterface.md#analysisinterface)

> Analysis class for Subsystem 2 in the Supersonic Business Jet (SSBJ) problem.


> **Attributes:**
> > None specific to this class; inherits from AnalysisInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the Analysis2 instance.

??? abstract "evaluateLocalResponses(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the physical responses of Subsystem 2.

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

