---
title: LocalCouplingParametersALADIN
---

← Back to [aladin](index.md)

# LocalCouplingParametersALADIN

**Source:** [Distributed_Design_Optimizer\subsystem\couplingparameters\aladin\LocalCouplingParametersALADIN.py](LocalCouplingParametersALADIN_source.md)

ALADIN local coupling parameters module.

This module provides coupling parameters for local subsystems
in the ALADIN coordination method.

## Classes

### LocalCouplingParametersALADIN

> **Inherits from:** [SubSysCouplingParametersBasis](../SubSysCouplingParametersBasis.md#subsyscouplingparametersbasis)

> Coupling parameters for ALADIN local subsystems.

> Extends SubSysCouplingParametersBasis with penalty weight vectors,
> Lagrange multiplier vectors, and d_hat quantities (coupling values
> evaluated at the controller-proposed design point) for left/right
> sides of the coupling circle and shared/target design variables.

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize LocalCouplingParametersALADIN.


    **Args:**
    > id: Identifier for this coupling.  

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
    Set the weights for coordination of the consistency constraint between shared design variables.


    **Args:**
    > shareddesignvariable_minus_copytargetshareddesignvariable_in: Vector of weights for shared design variables.  

??? abstract "get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self) → List[float] | None"
    Get the weights for coordination of the consistency constraints for shared design variables.


    **Returns:**
    > Vector of weights for shared design variables, or None if not set.  

??? abstract "set_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self, copyshareddesignvariable_minus_targetshareddesignvariable_in: List[float]) → None"
    Set the weights for coordination of the consistency constraint between target shared design variables.


    **Args:**
    > copyshareddesignvariable_minus_targetshareddesignvariable_in: Vector of weights for target design variables.  

??? abstract "get_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self) → List[float] | None"
    Get the weights for coordination of the consistency constraints for target shared design variables.


    **Returns:**
    > Vector of weights for target design variables, or None if not set.  

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
    Set the Lagrange multipliers for the target shared design variables.


    **Args:**
    > copyshareddesignvariable_minus_targetshareddesignvariable_in: Vector of multipliers for target design variables.  

??? abstract "get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self) → List[float] | None"
    Obtain the Lagrange multipliers from the target shared design variables.


    **Returns:**
    > Vector of multipliers for target design variables, or None if not set.  

??? abstract "set_MappedResponses_D_Hat(self, mappedresponses_d_hat_in: List[float]) → None"
    Set mapped response variables evaluated at the controller-proposed d_hat.


    **Args:**
    > mappedresponses_d_hat_in: Mapped response variables at d_hat.  

??? abstract "get_MappedResponses_D_Hat(self) → List[float] | None"
    Get mapped response variables evaluated at the controller-proposed d_hat.


    **Returns:**
    > Mapped response variables at d_hat, or None if not set.  

??? abstract "set_CouplingVariable_D_Hat(self, couplingvariable_d_hat_in: List[float]) → None"
    Set coupling variable evaluated at the controller-proposed d_hat.


    **Args:**
    > couplingvariable_d_hat_in: Coupling variable at d_hat.  

??? abstract "get_CouplingVariable_D_Hat(self) → List[float] | None"
    Get coupling variable evaluated at the controller-proposed d_hat.


    **Returns:**
    > Coupling variable at d_hat, or None if not set.  

??? abstract "set_SharedDesignVariables_D_Hat(self, shareddesignvariables_d_hat_in: List[float]) → None"
    Set shared design variables evaluated at the controller-proposed d_hat.


    **Args:**
    > shareddesignvariables_d_hat_in: Shared design variables at d_hat.  

??? abstract "get_SharedDesignVariables_D_Hat(self) → List[float] | None"
    Get shared design variables evaluated at the controller-proposed d_hat.


    **Returns:**
    > Shared design variables at d_hat, or None if not set.  

??? abstract "set_TargetSharedDesignVariables_D_Hat(self, targetshareddesignvariables_d_hat_in: List[float]) → None"
    Set target shared design variables evaluated at the controller-proposed d_hat.


    **Args:**
    > targetshareddesignvariables_d_hat_in: Target shared design variables at d_hat.  

??? abstract "get_TargetSharedDesignVariables_D_Hat(self) → List[float] | None"
    Get target shared design variables evaluated at the controller-proposed d_hat.


    **Returns:**
    > Target shared design variables at d_hat, or None if not set.  

??? abstract "set_Copy_MappedResponses_D_Hat(self, copy_mappedresponses_d_hat_in: List[float]) → None"
    Set copy of neighbor's mapped response variables evaluated at neighbor's d_hat.


    **Args:**
    > copy_mappedresponses_d_hat_in: Neighbor's mapped response variables at d_hat.  

??? abstract "get_Copy_MappedResponses_D_Hat(self) → List[float] | None"
    Get copy of neighbor's mapped response variables evaluated at neighbor's d_hat.


    **Returns:**
    > Neighbor's mapped response variables at d_hat, or None if not set.  

??? abstract "set_Copy_CouplingVariable_D_Hat(self, copy_couplingvariable_d_hat_in: List[float]) → None"
    Set copy of neighbor's coupling variable evaluated at neighbor's d_hat.


    **Args:**
    > copy_couplingvariable_d_hat_in: Neighbor's coupling variable at d_hat.  

??? abstract "get_Copy_CouplingVariable_D_Hat(self) → List[float] | None"
    Get copy of neighbor's coupling variable evaluated at neighbor's d_hat.


    **Returns:**
    > Neighbor's coupling variable at d_hat, or None if not set.  

??? abstract "set_Copy_SharedDesignVariables_D_Hat(self, copy_shareddesignvariables_d_hat_in: List[float]) → None"
    Set copy of neighbor's shared design variables evaluated at neighbor's d_hat.


    **Args:**
    > copy_shareddesignvariables_d_hat_in: Neighbor's shared design variables at d_hat.  

??? abstract "get_Copy_SharedDesignVariables_D_Hat(self) → List[float] | None"
    Get copy of neighbor's shared design variables evaluated at neighbor's d_hat.


    **Returns:**
    > Neighbor's shared design variables at d_hat, or None if not set.  

??? abstract "set_Copy_TargetSharedDesignVariables_D_Hat(self, copy_targetshareddesignvariables_d_hat_in: List[float]) → None"
    Set copy of neighbor's target shared design variables evaluated at neighbor's d_hat.


    **Args:**
    > copy_targetshareddesignvariables_d_hat_in: Neighbor's target shared design variables at d_hat.  

??? abstract "get_Copy_TargetSharedDesignVariables_D_Hat(self) → List[float] | None"
    Get copy of neighbor's target shared design variables evaluated at neighbor's d_hat.


    **Returns:**
    > Neighbor's target shared design variables at d_hat, or None if not set.  

??? abstract "CopyFromMiddleLevelCoupling(self, middlelevelcouplingIn: [LocalToLocal_MiddleLevelCouplingALADIN](../../../middlelevel/aladin/LocalToLocal_MiddleLevelCouplingALADIN.md#localtolocal_middlelevelcouplingaladin)) → None"
    Copy coupling parameters from the middle level.


    **Args:**
    > middlelevelcouplingIn: Middle level coupling to copy from.  


    **Raises:**
    > ValueError: If middlelevelcouplingIn is not a LocalToLocal_MiddleLevelCouplingALADIN instance.  

??? abstract "CopyToMiddleLevelCoupling(self, middlelevelcouplingIn: [LocalToLocal_MiddleLevelCouplingALADIN](../../../middlelevel/aladin/LocalToLocal_MiddleLevelCouplingALADIN.md#localtolocal_middlelevelcouplingaladin)) → None"
    Copy coupling parameters to the middle level.


    **Args:**
    > middlelevelcouplingIn: Middle level coupling to copy to.  


    **Raises:**
    > ValueError: If middlelevelcouplingIn is not a LocalToLocal_MiddleLevelCouplingALADIN instance.  

??? abstract "update_state(self, other_coupling: [LocalCouplingParametersALADIN](LocalCouplingParametersALADIN.md#localcouplingparametersaladin)) → None"
    Update the state of this LocalCouplingParametersALADIN with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.

    The update preserves memory addresses by modifying list contents in-place rather than
    reassigning references. This is essential for maintaining object identity across the
    multiprocessing boundary.


    **Args:**
    > other_coupling: The source LocalCouplingParametersALADIN containing updated values  
    > from parallel execution.  

