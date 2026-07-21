---
title: CouplingParametersConsensusALC
---

← Back to [consensus_alc](index.md)

# CouplingParametersConsensusALC

**Source:** [Distributed_Design_Optimizer\subsystem\couplingparameters\consensus_alc\CouplingParametersConsensusALC.py](CouplingParametersConsensusALC_source.md)

Consensus ALC coupling parameters module.

This module provides coupling parameters for the
consensus-based Augmented Lagrangian Coordination method.

## Classes

### CouplingParametersConsensusALC

> **Inherits from:** [SubSysCouplingParametersBasis](../SubSysCouplingParametersBasis.md#subsyscouplingparametersbasis)

> Coupling parameters for consensus-based ALC.

> Stores auxiliary variables, weights, and Lagrange multipliers for
> consensus-based Augmented Lagrangian Coordination.

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize CouplingParametersConsensusALC.


    **Args:**
    > id: Identifier for this coupling.  

??? abstract "set_Auxiliary_MappedResponse(self, auxiliary_mappedresponse_in: List[float]) → None"
    Set the auxiliary consensus variables for the mapped-response side of the coupling circle.


    **Args:**
    > auxiliary_mappedresponse_in: Auxiliary consensus variable matched against the mapped response.  

??? abstract "get_Auxiliary_MappedResponse(self) → List[float] | None"
    Return the auxiliary consensus variables for the mapped-response side of the coupling circle.


    **Returns:**
    > Auxiliary consensus variables for the mapped-response side, or None if not set.  

??? abstract "set_Auxiliary_CouplingVariable(self, auxiliary_couplingvariable_in: List[float]) → None"
    Set the auxiliary consensus variables for the coupling-variable side of the coupling circle.


    **Args:**
    > auxiliary_couplingvariable_in: Auxiliary consensus variable matched against the coupling variable.  

??? abstract "get_Auxiliary_CouplingVariable(self) → List[float] | None"
    Return the auxiliary consensus variables for the coupling-variable side of the coupling circle.


    **Returns:**
    > Auxiliary consensus variables for the coupling-variable side, or None if not set.  

??? abstract "set_Auxiliary_SharedDesignVariable(self, auxiliary_shareddesignvariable_in: List[float]) → None"
    Set the auxiliary consensus variables for the shared-design-variable side of the coupling circle.


    **Args:**
    > auxiliary_shareddesignvariable_in: Auxiliary consensus variable matched against the shared design variable.  

??? abstract "get_Auxiliary_SharedDesignVariable(self) → List[float] | None"
    Return the auxiliary consensus variables for the shared-design-variable side of the coupling circle.


    **Returns:**
    > Auxiliary consensus variables for the shared-design-variable side, or None if not set.  

??? abstract "set_Auxiliary_TargetSharedDesignVariable(self, auxiliary_targetshareddesignvariable_in: List[float]) → None"
    Set the auxiliary consensus variables for the target-shared-design-variable side of the coupling circle.


    **Args:**
    > auxiliary_targetshareddesignvariable_in: Auxiliary consensus variable matched against the target shared design variable.  

??? abstract "get_Auxiliary_TargetSharedDesignVariable(self) → List[float] | None"
    Return the auxiliary consensus variables for the target-shared-design-variable side of the coupling circle.


    **Returns:**
    > Auxiliary consensus variables for the target-shared-design-variable side, or None if not set.  

??? abstract "set_Weights_Auxiliary_Minus_MappedResponse(self, auxiliary_minus_mappedresponse_in: List[float]) → None"
    Set the penalty weights for the auxiliary-minus-mapped-response part of the coupling circle.


    **Args:**
    > auxiliary_minus_mappedresponse_in: Penalty weights for the auxiliary minus mapped response inconsistency.  

??? abstract "get_Weights_Auxiliary_Minus_MappedResponse(self) → List[float] | None"
    Get the penalty weights for the auxiliary-minus-mapped-response part of the coupling circle.


    **Returns:**
    > Penalty weights for the auxiliary-minus-mapped-response part, or None if not set.  

??? abstract "set_Weights_Auxiliary_Minus_CouplingVariable(self, auxiliary_minus_couplingvariable_in: List[float]) → None"
    Set the penalty weights for the auxiliary-minus-coupling-variable part of the coupling circle.


    **Args:**
    > auxiliary_minus_couplingvariable_in: Penalty weights for the auxiliary minus coupling variable inconsistency.  

??? abstract "get_Weights_Auxiliary_Minus_CouplingVariable(self) → List[float] | None"
    Get the penalty weights for the auxiliary-minus-coupling-variable part of the coupling circle.


    **Returns:**
    > Penalty weights for the auxiliary-minus-coupling-variable part, or None if not set.  

??? abstract "set_Weights_Auxiliary_Minus_SharedDesignVariable(self, auxiliary_minus_shareddesignvariable_in: List[float]) → None"
    Set the penalty weights for the auxiliary-minus-shared-design-variable part of the coupling circle.


    **Args:**
    > auxiliary_minus_shareddesignvariable_in: Penalty weights for the auxiliary minus shared design variable inconsistency.  

??? abstract "get_Weights_Auxiliary_Minus_SharedDesignVariable(self) → List[float] | None"
    Get the penalty weights for the auxiliary-minus-shared-design-variable part of the coupling circle.


    **Returns:**
    > Penalty weights for the auxiliary-minus-shared-design-variable part, or None if not set.  

??? abstract "set_Weights_Auxiliary_Minus_TargetSharedDesignVariable(self, auxiliary_minus_targetshareddesignvariable_in: List[float]) → None"
    Set the penalty weights for the auxiliary-minus-target-shared-design-variable part of the coupling circle.


    **Args:**
    > auxiliary_minus_targetshareddesignvariable_in: Penalty weights for the auxiliary minus target shared design variable inconsistency.  

??? abstract "get_Weights_Auxiliary_Minus_TargetSharedDesignVariable(self) → List[float] | None"
    Get the penalty weights for the auxiliary-minus-target-shared-design-variable part of the coupling circle.


    **Returns:**
    > Penalty weights for the auxiliary-minus-target-shared-design-variable part, or None if not set.  

??? abstract "set_Multipliers_Auxiliary_Minus_MappedResponse(self, auxiliary_minus_mappedresponse_in: List[float]) → None"
    Set the Lagrange multipliers for the auxiliary-minus-mapped-response part of the coupling circle.


    **Args:**
    > auxiliary_minus_mappedresponse_in: Lagrange multipliers for the auxiliary minus mapped response inconsistency.  

??? abstract "get_Multipliers_Auxiliary_Minus_MappedResponse(self) → List[float] | None"
    Get the Lagrange multipliers for the auxiliary-minus-mapped-response part of the coupling circle.


    **Returns:**
    > Lagrange multipliers for the auxiliary-minus-mapped-response part, or None if not set.  

??? abstract "set_Multipliers_Auxiliary_Minus_CouplingVariable(self, auxiliary_minus_couplingvariable_in: List[float]) → None"
    Set the Lagrange multipliers for the auxiliary-minus-coupling-variable part of the coupling circle.


    **Args:**
    > auxiliary_minus_couplingvariable_in: Lagrange multipliers for the auxiliary minus coupling variable inconsistency.  

??? abstract "get_Multipliers_Auxiliary_Minus_CouplingVariable(self) → List[float] | None"
    Get the Lagrange multipliers for the auxiliary-minus-coupling-variable part of the coupling circle.


    **Returns:**
    > Lagrange multipliers for the auxiliary-minus-coupling-variable part, or None if not set.  

??? abstract "set_Multipliers_Auxiliary_Minus_SharedDesignVariable(self, auxiliary_minus_shareddesignvariable_in: List[float]) → None"
    Set the Lagrange multipliers for the auxiliary-minus-shared-design-variable part of the coupling circle.


    **Args:**
    > auxiliary_minus_shareddesignvariable_in: Lagrange multipliers for the auxiliary minus shared design variable inconsistency.  

??? abstract "get_Multipliers_Auxiliary_Minus_SharedDesignVariable(self) → List[float] | None"
    Get the Lagrange multipliers for the auxiliary-minus-shared-design-variable part of the coupling circle.


    **Returns:**
    > Lagrange multipliers for the auxiliary-minus-shared-design-variable part, or None if not set.  

??? abstract "set_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable(self, auxiliary_minus_targetshareddesignvariable_in: List[float]) → None"
    Set the Lagrange multipliers for the auxiliary-minus-target-shared-design-variable part of the coupling circle.


    **Args:**
    > auxiliary_minus_targetshareddesignvariable_in: Lagrange multipliers for the auxiliary minus target shared design variable inconsistency.  

??? abstract "get_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable(self) → List[float] | None"
    Get the Lagrange multipliers for the auxiliary-minus-target-shared-design-variable part of the coupling circle.


    **Returns:**
    > Lagrange multipliers for the auxiliary-minus-target-shared-design-variable part, or None if not set.  

??? abstract "set_Copy_Weights_Auxiliary_Minus_MappedResponse(self, copy_auxiliary_minus_mappedresponse_in: List[float]) → None"
    Set the weights for the neighbor consensus constraint w.r.t. the auxiliary-minus-mapped-response part of the coupling circle.


    **Args:**
    > copy_auxiliary_minus_mappedresponse_in: Weights for the neighbor auxiliary minus mapped response inconsistency.  

??? abstract "get_Copy_Weights_Auxiliary_Minus_MappedResponse(self) → List[float] | None"
    Get the weights for the neighbor consensus constraint w.r.t. the auxiliary-minus-mapped-response part of the coupling circle.


    **Returns:**
    > Weights for the neighbor consensus constraint, or None if not set.  

??? abstract "set_Copy_Weights_Auxiliary_Minus_CouplingVariable(self, copy_auxiliary_minus_couplingvariable_in: List[float]) → None"
    Set the weights for the neighbor consensus constraint w.r.t. the auxiliary-minus-coupling-variable part of the coupling circle.


    **Args:**
    > copy_auxiliary_minus_couplingvariable_in: Weights for the neighbor auxiliary minus coupling variable inconsistency.  

??? abstract "get_Copy_Weights_Auxiliary_Minus_CouplingVariable(self) → List[float] | None"
    Get the weights for the neighbor consensus constraint w.r.t. the auxiliary-minus-coupling-variable part of the coupling circle.


    **Returns:**
    > Weights for the neighbor consensus constraint, or None if not set.  

??? abstract "set_Copy_Weights_Auxiliary_Minus_SharedDesignVariable(self, copy_auxiliary_minus_shareddesignvariable_in: List[float]) → None"
    Set the weights for the neighbor consensus constraint w.r.t. the auxiliary-minus-shared-design-variable part of the coupling circle.


    **Args:**
    > copy_auxiliary_minus_shareddesignvariable_in: Weights for the neighbor auxiliary minus shared design variable inconsistency.  

??? abstract "get_Copy_Weights_Auxiliary_Minus_SharedDesignVariable(self) → List[float] | None"
    Get the weights for the neighbor consensus constraint w.r.t. the auxiliary-minus-shared-design-variable part of the coupling circle.


    **Returns:**
    > Weights for the neighbor consensus constraint, or None if not set.  

??? abstract "set_Copy_Weights_Auxiliary_Minus_TargetSharedDesignVariable(self, copy_auxiliary_minus_targetshareddesignvariable_in: List[float]) → None"
    Set the weights for the neighbor consensus constraint w.r.t. the auxiliary-minus-target-shared-design-variable part of the coupling circle.


    **Args:**
    > copy_auxiliary_minus_targetshareddesignvariable_in: Weights for the neighbor auxiliary minus target shared design variable inconsistency.  

??? abstract "get_Copy_Weights_Auxiliary_Minus_TargetSharedDesignVariable(self) → List[float] | None"
    Get the weights for the neighbor consensus constraint w.r.t. the auxiliary-minus-target-shared-design-variable part of the coupling circle.


    **Returns:**
    > Weights for the neighbor consensus constraint, or None if not set.  

??? abstract "set_Copy_Multipliers_Auxiliary_Minus_MappedResponse(self, copy_auxiliary_minus_mappedresponse_in: List[float]) → None"
    Set the Lagrange multipliers for the neighbor consensus constraint w.r.t. the auxiliary-minus-mapped-response part of the coupling circle.


    **Args:**
    > copy_auxiliary_minus_mappedresponse_in: Lagrange multipliers for the neighbor auxiliary minus mapped response inconsistency.  

??? abstract "get_Copy_Multipliers_Auxiliary_Minus_MappedResponse(self) → List[float] | None"
    Get the Lagrange multipliers for the neighbor consensus constraint w.r.t. the auxiliary-minus-mapped-response part of the coupling circle.


    **Returns:**
    > Lagrange multipliers for the neighbor consensus constraint, or None if not set.  

??? abstract "set_Copy_Multipliers_Auxiliary_Minus_CouplingVariable(self, copy_auxiliary_minus_couplingvariable_in: List[float]) → None"
    Set the Lagrange multipliers for the neighbor consensus constraint w.r.t. the auxiliary-minus-coupling-variable part of the coupling circle.


    **Args:**
    > copy_auxiliary_minus_couplingvariable_in: Lagrange multipliers for the neighbor auxiliary minus coupling variable inconsistency.  

??? abstract "get_Copy_Multipliers_Auxiliary_Minus_CouplingVariable(self) → List[float] | None"
    Get the Lagrange multipliers for the neighbor consensus constraint w.r.t. the auxiliary-minus-coupling-variable part of the coupling circle.


    **Returns:**
    > Lagrange multipliers for the neighbor consensus constraint, or None if not set.  

??? abstract "set_Copy_Multipliers_Auxiliary_Minus_SharedDesignVariable(self, copy_auxiliary_minus_shareddesignvariable_in: List[float]) → None"
    Set the Lagrange multipliers for the neighbor consensus constraint w.r.t. the auxiliary-minus-shared-design-variable part of the coupling circle.


    **Args:**
    > copy_auxiliary_minus_shareddesignvariable_in: Lagrange multipliers for the neighbor auxiliary minus shared design variable inconsistency.  

??? abstract "get_Copy_Multipliers_Auxiliary_Minus_SharedDesignVariable(self) → List[float] | None"
    Get the Lagrange multipliers for the neighbor consensus constraint w.r.t. the auxiliary-minus-shared-design-variable part of the coupling circle.


    **Returns:**
    > Lagrange multipliers for the neighbor consensus constraint, or None if not set.  

??? abstract "set_Copy_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable(self, copy_auxiliary_minus_targetshareddesignvariable_in: List[float]) → None"
    Set the Lagrange multipliers for the neighbor consensus constraint w.r.t. the auxiliary-minus-target-shared-design-variable part of the coupling circle.


    **Args:**
    > copy_auxiliary_minus_targetshareddesignvariable_in: Lagrange multipliers for the neighbor auxiliary minus target shared design variable inconsistency.  

??? abstract "get_Copy_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable(self) → List[float] | None"
    Get the Lagrange multipliers for the neighbor consensus constraint w.r.t. the auxiliary-minus-target-shared-design-variable part of the coupling circle.


    **Returns:**
    > Lagrange multipliers for the neighbor consensus constraint, or None if not set.  

??? abstract "CopyFromMiddleLevelCoupling(self, middlelevelcouplingIn: [MiddleLevelCouplingConsensusALC](../../../middlelevel/consensus_alc/MiddleLevelCouplingConsensusALC.md#middlelevelcouplingconsensusalc)) → None"
    Copy coupling parameters from the middle level.


    **Args:**
    > middlelevelcouplingIn: Source middle level coupling.  


    **Raises:**
    > ValueError: If middlelevelcouplingIn is not a MiddleLevelCouplingConsensusALC instance.  

??? abstract "CopyToMiddleLevelCoupling(self, middlelevelcouplingIn: [MiddleLevelCouplingConsensusALC](../../../middlelevel/consensus_alc/MiddleLevelCouplingConsensusALC.md#middlelevelcouplingconsensusalc)) → None"
    Copy coupling parameters to the middle level.


    **Args:**
    > middlelevelcouplingIn: Target middle level coupling.  


    **Raises:**
    > ValueError: If middlelevelcouplingIn is not a MiddleLevelCouplingConsensusALC instance.  

??? abstract "update_state(self, other_coupling: [CouplingParametersConsensusALC](CouplingParametersConsensusALC.md#couplingparametersconsensusalc)) → None"
    Update the state of this CouplingParametersConsensusALC with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.

    The update preserves memory addresses by modifying list contents in-place rather than
    reassigning references. This is essential for maintaining object identity across the
    multiprocessing boundary.


    **Args:**
    > other_coupling: The source CouplingParametersConsensusALC containing updated values  
    > from parallel execution.  

