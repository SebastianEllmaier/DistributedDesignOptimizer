---
title: CouplingParametersLC
---

← Back to [lc](index.md)

# CouplingParametersLC

**Source:** [Distributed_Design_Optimizer\subsystem\couplingparameters\lc\CouplingParametersLC.py](CouplingParametersLC_source.md)

Coupling Lagrange multipliers module.

This module provides Lagrange multiplier parameters for the
Lagrangian Coordination method.

## Classes

### CouplingParametersLC

> **Inherits from:** [SubSysCouplingParametersBasis](../SubSysCouplingParametersBasis.md#subsyscouplingparametersbasis)

> Coupling multipliers for Lagrangian coordination.

> Extends SubSysCouplingParametersBasis with Lagrange multiplier vectors for
> mapped-response/coupling-variable sides of the coupling circle and shared/target design variables.

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize CouplingParametersLC.


    **Args:**
    > id: Unique identifier for this coupling.  

??? abstract "set_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self, mappedresponse_minus_copycouplingvariable_in: List[float]) → None"
    Set the Lagrange multipliers for the mapped-response side of the coupling circle.


    **Args:**
    > mappedresponse_minus_copycouplingvariable_in: Vector of Lagrange multipliers for mapped-response side.  

??? abstract "get_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self) → List[float] | None"
    Obtain the Lagrange multipliers from the mapped-response side of the coupling circle.


    **Returns:**
    > Vector of Lagrange multipliers for mapped-response side, or None if not set.  

??? abstract "set_Multipliers_CopyMappedResponse_Minus_CouplingVariable(self, copymappedresponse_minus_couplingvariable_in: List[float]) → None"
    Set the Lagrange multipliers for the coupling-variable side of the coupling circle.


    **Args:**
    > copymappedresponse_minus_couplingvariable_in: Vector of Lagrange multipliers for coupling-variable side.  

??? abstract "get_Multipliers_CopyMappedResponse_Minus_CouplingVariable(self) → List[float] | None"
    Obtain the Lagrange multipliers from the coupling-variable side of the coupling circle.


    **Returns:**
    > Vector of Lagrange multipliers for coupling-variable side, or None if not set.  

??? abstract "set_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, shareddesignvariable_minus_copytargetshareddesignvariable_in: List[float]) → None"
    Set the Lagrange multipliers for the shared design variables.


    **Args:**
    > shareddesignvariable_minus_copytargetshareddesignvariable_in: Vector of multipliers for shared design variables.  

??? abstract "get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self) → List[float] | None"
    Obtain the Lagrange multipliers from the shared design variables.


    **Returns:**
    > Vector of multipliers for shared design variables, or None if not set.  

??? abstract "set_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self, copyshareddesignvariable_minus_targetshareddesignvariable_in: List[float]) → None"
    Set the Lagrange multipliers for the target design variables.


    **Args:**
    > copyshareddesignvariable_minus_targetshareddesignvariable_in: Vector of multipliers for target design variables.  

??? abstract "get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self) → List[float] | None"
    Obtain the Lagrange multipliers from the target design variables.


    **Returns:**
    > Vector of multipliers for target design variables, or None if not set.  

??? abstract "CopyFromMiddleLevelCoupling(self, middlelevelcouplingIn: [MiddleLevelCouplingLC](../../../middlelevel/lc/MiddleLevelCouplingLC.md#middlelevelcouplinglc)) → None"
    Copy coupling data from a MiddleLevelCoupling object.


    **Args:**
    > middlelevelcouplingIn: The MiddleLevelCoupling object to copy data from.  


    **Raises:**
    > ValueError: If middlelevelcouplingIn is not a MiddleLevelCoupling instance.  

??? abstract "CopyToMiddleLevelCoupling(self, middlelevelcouplingIn: [MiddleLevelCouplingLC](../../../middlelevel/lc/MiddleLevelCouplingLC.md#middlelevelcouplinglc)) → None"
    Copy coupling data to a MiddleLevelCoupling object.


    **Args:**
    > middlelevelcouplingIn: The MiddleLevelCoupling object to copy data to.  


    **Raises:**
    > ValueError: If middlelevelcouplingIn is not a MiddleLevelCoupling instance.  

??? abstract "update_state(self, other_coupling: [CouplingParametersLC](CouplingParametersLC.md#couplingparameterslc)) → None"
    Update the state of this CouplingParametersLC with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.

    The update preserves memory addresses by modifying list contents in-place rather than
    reassigning references. This is essential for maintaining object identity across the
    multiprocessing boundary.


    **Args:**
    > other_coupling: The source CouplingParametersLC containing updated values  
    > from parallel execution.  

