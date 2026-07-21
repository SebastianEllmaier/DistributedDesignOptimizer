---
title: CouplingParametersPC
---

← Back to [pc](index.md)

# CouplingParametersPC

**Source:** [Distributed_Design_Optimizer\subsystem\couplingparameters\pc\CouplingParametersPC.py](CouplingParametersPC_source.md)

Coupling weights module.

This module provides coupling weight parameters for the
Penalty Coordination method.

## Classes

### CouplingParametersPC

> **Inherits from:** [SubSysCouplingParametersBasis](../SubSysCouplingParametersBasis.md#subsyscouplingparametersbasis)

> Coupling weights for penalty coordination.

> Extends SubSysCouplingParametersBasis with penalty weight vectors for
> mapped-response/coupling-variable sides of the coupling circle and shared/target design variables.

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize CouplingParametersPC.


    **Args:**
    > id: Unique identifier for this coupling.  

??? abstract "set_Weights_MappedResponse_Minus_CopyCouplingVariable(self, mappedresponse_minus_copycouplingvariable_in: List[float]) → None"
    Set the penalty weights for the mapped-response part of the coupling circle.


    **Args:**
    > mappedresponse_minus_copycouplingvariable_in: Vector of penalty weights for mapped-response side.  

??? abstract "get_Weights_MappedResponse_Minus_CopyCouplingVariable(self) → List[float] | None"
    Get the penalty weights for the mapped-response part of the coupling circle.


    **Returns:**
    > Vector of penalty weights for mapped-response side, or None if not set.  

??? abstract "set_Weights_CopyMappedResponse_Minus_CouplingVariable(self, copymappedresponse_minus_couplingvariable_in: List[float]) → None"
    Set the penalty weights for the coupling-variable part of the coupling circle.


    **Args:**
    > copymappedresponse_minus_couplingvariable_in: Vector of penalty weights for coupling-variable side.  

??? abstract "get_Weights_CopyMappedResponse_Minus_CouplingVariable(self) → List[float] | None"
    Get the penalty weights for the coupling-variable part of the coupling circle.


    **Returns:**
    > Vector of penalty weights for coupling-variable side, or None if not set.  

??? abstract "set_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, shareddesignvariable_minus_copytargetshareddesignvariable_in: List[float]) → None"
    Set the weights for coordination of consistency constraint between shared design variables.


    **Args:**
    > shareddesignvariable_minus_copytargetshareddesignvariable_in: Vector of weights for shared design variables.  

??? abstract "get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self) → List[float] | None"
    Get the weights for coordination of consistency constraints for shared design variables.


    **Returns:**
    > Vector of weights for shared design variables, or None if not set.  

??? abstract "set_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self, copyshareddesignvariable_minus_targetshareddesignvariable_in: List[float]) → None"
    Set the weights for coordination of consistency constraint between target design variables.


    **Args:**
    > copyshareddesignvariable_minus_targetshareddesignvariable_in: Vector of weights for target design variables.  

??? abstract "get_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self) → List[float] | None"
    Get the weights for coordination of consistency constraints for target design variables.


    **Returns:**
    > Vector of weights for target design variables, or None if not set.  

??? abstract "CopyFromMiddleLevelCoupling(self, middlelevelcouplingIn: [MiddleLevelCouplingPC](../../../middlelevel/pc/MiddleLevelCouplingPC.md#middlelevelcouplingpc)) → None"
    Copy coupling data from a MiddleLevelCoupling object.


    **Args:**
    > middlelevelcouplingIn: The MiddleLevelCoupling object to copy data from.  


    **Raises:**
    > ValueError: If middlelevelcouplingIn is not a MiddleLevelCoupling instance.  

??? abstract "CopyToMiddleLevelCoupling(self, middlelevelcouplingIn: [MiddleLevelCouplingPC](../../../middlelevel/pc/MiddleLevelCouplingPC.md#middlelevelcouplingpc)) → None"
    Copy coupling data to a MiddleLevelCoupling object.


    **Args:**
    > middlelevelcouplingIn: The MiddleLevelCoupling object to copy data to.  


    **Raises:**
    > ValueError: If middlelevelcouplingIn is not a MiddleLevelCoupling instance.  

??? abstract "update_state(self, other_coupling: [CouplingParametersPC](CouplingParametersPC.md#couplingparameterspc)) → None"
    Update the state of this CouplingParametersPC with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.

    The update preserves memory addresses by modifying list contents in-place rather than
    reassigning references. This is essential for maintaining object identity across the
    multiprocessing boundary.


    **Args:**
    > other_coupling: The source CouplingParametersPC containing updated values  
    > from parallel execution.  

