---
title: InConsistencySize
---

← Back to [consensus_alc](index.md)

# InConsistencySize

**Source:** [Distributed_Design_Optimizer\middlelevel\consensus_alc\InConsistencySize.py](InConsistencySize_source.md)

Inconsistency size computation for consensus-based ALC.

This module provides functionality for computing inconsistency sizes
between coupled variables in consensus-based ALC.

## Classes

### InConsistencySize

> **Inherits from:** [InConsistencySizeBasis](../InConsistencySizeBasis.md#inconsistencysizebasis)

> Inconsistency size storage for consensus-based ALC.

> Stores and computes the size of inconsistencies between coupled
> variables in consensus-based ALC coordination.

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize inconsistency size.


    **Args:**
    > id: Identifier for this inconsistency measure.  

??? abstract "evaluate_Auxiliary_Minus_MappedResponse(self, auxiliary: List[float], mappedresponse: List[float]) → None"
    Set the inconsistency between the auxiliary variable and the mapped response for consensus constraints.


    **Args:**
    > auxiliary: Auxiliary variable values.  
    > mappedresponse: Mapped response values.  

??? abstract "get_Auxiliary_Minus_MappedResponse(self) → List[float] | None"
    Get the inconsistency between the auxiliary variable and the mapped response for consensus constraints.


    **Returns:**
    > List of inconsistency values or None if not set.  

??? abstract "get_Auxiliary_Minus_MappedResponse_InfyNorm(self) → float | None"
    Get the maximum auxiliary-minus-mapped-response inconsistency (infinity norm).


    **Returns:**
    > Maximum inconsistency value or None if not set.  

??? abstract "get_Auxiliary_Minus_MappedResponse_InfyNormID(self) → int | None"
    Get the index of the maximum auxiliary-minus-mapped-response inconsistency.


    **Returns:**
    > Index of maximum inconsistency or None if not set.  

??? abstract "evaluate_Auxiliary_Minus_CouplingVariable(self, auxiliary: List[float], couplingvariable: List[float]) → None"
    Set the inconsistency between the auxiliary variable and the coupling variable for consensus constraints.


    **Args:**
    > auxiliary: Auxiliary variable values.  
    > couplingvariable: Coupling variable values.  

??? abstract "get_Auxiliary_Minus_CouplingVariable(self) → List[float] | None"
    Get the inconsistency between the auxiliary variable and the coupling variable for consensus constraints.


    **Returns:**
    > List of inconsistency values or None if not set.  

??? abstract "get_Auxiliary_Minus_CouplingVariable_InfyNorm(self) → float | None"
    Get the maximum auxiliary-minus-coupling-variable inconsistency (infinity norm).


    **Returns:**
    > Maximum inconsistency value or None if not set.  

??? abstract "get_Auxiliary_Minus_CouplingVariable_InfyNormID(self) → int | None"
    Get the index of the maximum auxiliary-minus-coupling-variable inconsistency.


    **Returns:**
    > Index of maximum inconsistency or None if not set.  

??? abstract "evaluate_Auxiliary_Minus_SharedDesignVariable(self, auxiliary: List[float], shareddesignvariable: List[float]) → None"
    Set the inconsistency for shared design variables in consensus constraints.


    **Args:**
    > auxiliary: Auxiliary variable values.  
    > shareddesignvariable: Shared design variable values.  

??? abstract "get_Auxiliary_Minus_SharedDesignVariable(self) → List[float] | None"
    Get the inconsistency for shared design variables in consensus constraints.


    **Returns:**
    > List of inconsistency values or None if not set.  

??? abstract "get_Auxiliary_Minus_SharedDesignVariable_InfyNorm(self) → float | None"
    Get the maximum shared design variables auxiliary inconsistency (infinity norm).


    **Returns:**
    > Maximum inconsistency value or None if not set.  

??? abstract "get_Auxiliary_Minus_SharedDesignVariable_InfyNormID(self) → int | None"
    Get the index of the maximum shared design variables auxiliary inconsistency.


    **Returns:**
    > Index of maximum inconsistency or None if not set.  

??? abstract "evaluate_Auxiliary_Minus_TargetSharedDesignVariable(self, auxiliary: List[float], targetshareddesignvariable: List[float]) → None"
    Set the inconsistency for target shared design variables in consensus constraints.


    **Args:**
    > auxiliary: Auxiliary variable values.  
    > targetshareddesignvariable: Target shared design variable values.  

??? abstract "get_Auxiliary_Minus_TargetSharedDesignVariable(self) → List[float] | None"
    Get the inconsistency for target shared design variables in consensus constraints.


    **Returns:**
    > List of inconsistency values or None if not set.  

??? abstract "get_Auxiliary_Minus_TargetSharedDesignVariable_InfyNorm(self) → float | None"
    Get the maximum target shared design variables auxiliary inconsistency (infinity norm).


    **Returns:**
    > Maximum inconsistency value or None if not set.  

??? abstract "get_Auxiliary_Minus_TargetSharedDesignVariable_InfyNormID(self) → int | None"
    Get the index of the maximum target shared design variables auxiliary inconsistency.


    **Returns:**
    > Index of maximum inconsistency or None if not set.  

??? abstract "set_OscillationIndex_Auxiliary_Minus_MappedResponse(self, oscillationindex: List[float | None]) → None"
    Set oscillation index for auxiliary-minus-mapped-response inconsistency.


    **Args:**
    > oscillationindex: List of oscillation index values.  

??? abstract "get_OscillationIndex_Auxiliary_Minus_MappedResponse(self) → List[float | None] | None"
    Get oscillation index for auxiliary-minus-mapped-response inconsistency.


    **Returns:**
    > List of oscillation index values or None if not set.  

??? abstract "set_OscillationIndex_Auxiliary_Minus_CouplingVariable(self, oscillationindex: List[float | None]) → None"
    Set oscillation index for auxiliary-minus-coupling-variable inconsistency.


    **Args:**
    > oscillationindex: List of oscillation index values.  

??? abstract "get_OscillationIndex_Auxiliary_Minus_CouplingVariable(self) → List[float | None] | None"
    Get oscillation index for auxiliary-minus-coupling-variable inconsistency.


    **Returns:**
    > List of oscillation index values or None if not set.  

??? abstract "set_OscillationIndex_Auxiliary_Minus_SharedDesignVariable(self, oscillationindex: List[float | None]) → None"
    Set oscillation index for shared design variables auxiliary inconsistency.


    **Args:**
    > oscillationindex: List of oscillation index values.  

??? abstract "get_OscillationIndex_Auxiliary_Minus_SharedDesignVariable(self) → List[float | None] | None"
    Get oscillation index for shared design variables auxiliary inconsistency.


    **Returns:**
    > List of oscillation index values or None if not set.  

??? abstract "set_OscillationIndex_Auxiliary_Minus_TargetSharedDesignVariable(self, oscillationindex: List[float | None]) → None"
    Set oscillation index for target shared design variables auxiliary inconsistency.


    **Args:**
    > oscillationindex: List of oscillation index values.  

??? abstract "get_OscillationIndex_Auxiliary_Minus_TargetSharedDesignVariable(self) → List[float | None] | None"
    Get oscillation index for target shared design variables auxiliary inconsistency.


    **Returns:**
    > List of oscillation index values or None if not set.  

??? abstract "update_state(self, other_inconsistency: [InConsistencySize](../sbdp/InConsistencySize.md#inconsistencysize)) → None"
    Update the state of this InConsistencySize with the state of another InConsistencySize.

    This method updates the numerical information stored in the class's attributes
    without changing the original memory address location. This is necessary for
    multiprocessing, where executed subsystems return from separate processes and
    their state must be transferred back to the original objects in the main process.


    **Args:**
    > other_inconsistency: The source instance to copy state from.  

