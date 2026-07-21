---
title: Analysis1
---

← Back to [subsystem1](index.md)

# Analysis1

**Source:** [userfiles\GeometricProgramming\subsystem1\Analysis1.py](Analysis1_source.md)

Analysis module for Subsystem 1 in the Geometric Programming Top-Down Hierarchic problem.

This module defines the Analysis1 class which implements the physics-based
analysis computations and response mapping for Subsystem 1 in the distributed
design optimization framework.

## Classes

### Analysis1

> **Inherits from:** [AnalysisInterface](../../../Distributed_Design_Optimizer/subsystem/optimization/AnalysisInterface.md#analysisinterface)

> Analysis class for Subsystem 1.

> Implements the AnalysisInterface to compute physical responses and map
> coupling variables for Subsystem 1 in the Geometric Programming problem.
> This subsystem operates at level 1 in the hierarchical decomposition.


> **Attributes:**
> > None specific to this class; inherits from AnalysisInterface.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the Analysis1 instance.

??? abstract "evaluateLocalResponses(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Evaluate the physical responses of Subsystem 1.

    Computes the subsystem responses based on the current design variables.
    The responses include geometric programming formulas involving powers,
    inverse powers, and square root operations.


    **Args:**
    > subsystem: The LocalSubSystemBasis instance containing design variables  
    > and where computed responses will be stored.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Map responses and design variables for inter-subsystem coupling.

    Maps the mapped response to Subsystem 0 and the shared design variable
    to Subsystem 2 for coordination between subsystems.


    **Args:**
    > subsystem: The LocalSubSystemBasis instance containing responses  
    > and design variables to be mapped.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters_Jacobians(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Map the Jacobians of the mapped responses.


    **Args:**
    > subsystem: The subsystem for which the Jacobians are mapped.  

??? abstract "mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian(self, subsystem: [LocalSubSystemBasis](../../../Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → List[List[List[List[float | None]]]] | None"
    Map the Hessians of the mapped responses, if known a priori.


    **Args:**
    > subsystem: The subsystem for which the Hessians are mapped.  


    **Returns:**
    > Hessian tensor indexed by [local-to-local coupling][mapped response  
    > component][n_design][n_design], or None to fall back to a BFGS /  
    > finite-difference approximation.  

