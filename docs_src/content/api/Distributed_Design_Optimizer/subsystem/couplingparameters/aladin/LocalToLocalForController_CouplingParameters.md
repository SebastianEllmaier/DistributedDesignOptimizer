---
title: LocalToLocalForController_CouplingParameters
---

← Back to [aladin](index.md)

# LocalToLocalForController_CouplingParameters

**Source:** [Distributed_Design_Optimizer\subsystem\couplingparameters\aladin\LocalToLocalForController_CouplingParameters.py](LocalToLocalForController_CouplingParameters_source.md)

Local to controller coupling parameters module.

This module provides parameters for coupling from local
subsystems to controller in ALADIN.

## Classes

### LocalToLocalForController_CouplingParameters

> This class is meant to be a part of the controller mapping.

> Maps between controller and local subsystem, since that part of
> the communicated data has an assignment to i <-> j pairs.

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize local to controller coupling parameters.


    **Args:**
    > id: Identifier for the coupled subsystem.  

??? abstract "get_ID(self) → str"
    Return the ID.


    **Returns:**
    > Identifier for the coupled subsystem.  

??? abstract "set_MappedResponses(self, mappedresponsesin: List[float]) → None"
    Set mapped responses.


    **Args:**
    > mappedresponsesin: Mapped responses to set.  

??? abstract "get_MappedResponses(self) → List[float] | None"
    Return mapped responses.


    **Returns:**
    > Mapped responses, or None if not set.  

??? abstract "set_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self, mappedresponse_minus_copycouplingvariable_in: List[float]) → None"
    Set multipliers corresponding to constraint with subsystem i's mapped responses.


    **Args:**
    > mappedresponse_minus_copycouplingvariable_in: Multipliers for the mapped response minus copied coupling variable inconsistency.  

??? abstract "get_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self) → List[float] | None"
    Return multipliers corresponding to constraint with subsystem i's mapped responses.


    **Returns:**
    > Left multipliers, or None if not set.  

??? abstract "set_Weights_MappedResponse_Minus_CopyCouplingVariable(self, mappedresponse_minus_copycouplingvariable_in: List[float]) → None"
    Set weights corresponding to constraint with subsystem i's mapped responses.


    **Args:**
    > mappedresponse_minus_copycouplingvariable_in: Weights for the mapped response minus copied coupling variable inconsistency.  

??? abstract "get_Weights_MappedResponse_Minus_CopyCouplingVariable(self) → List[float] | None"
    Return weights corresponding to constraint with subsystem i's mapped responses.


    **Returns:**
    > Left weights, or None if not set.  

??? abstract "set_JacobianMappedResponses(self, jacobianmappedresponsesin: List[List[float | None]]) → None"
    Set the Jacobians of subsystem i's mapped responses.


    **Args:**
    > jacobianmappedresponsesin: Jacobian of mapped responses to set.  

??? abstract "get_JacobianMappedResponses(self) → List[List[float | None]] | None"
    Return the Jacobians of subsystem i's mapped responses.

    If it is None, the user does not know the Jacobians.
    If it is a List[List[float | None]], the entries with None
    indicate the derivatives the user does not provide, i.e. need
    to be approximated ('intermediate storage').
    It needs to be ensured that if the Jacobian
    is used, it should have no 'None'-fields.


    **Returns:**
    > Jacobian of mapped responses, or None if not set.  

??? abstract "set_HessiansMappedResponses(self, hessiansmappedresponsesin: List[List[List[float]]]) → None"
    Set the Hessians of subsystem i's mapped responses.


    **Args:**
    > hessiansmappedresponsesin: Hessians of mapped responses to set.  

??? abstract "get_HessiansMappedResponses(self) → List[List[List[float]]] | None"
    Get the Hessians of subsystem i's mapped responses.


    **Returns:**
    > Hessians of mapped responses, or None if not set.  

??? abstract "set_Jacobian_MappedResponses_at_Position(self, i: int, j: int, value: float) → None"
    Update the Jacobian at position (i,j) with the input value.


    **Args:**
    > i: Row index.  
    > j: Column index.  
    > value: Value to set at position (i, j).  

??? abstract "set_CouplingVariables(self, couplingvariablesin: List[float]) → None"
    Set subsystem i's coupling variables.


    **Args:**
    > couplingvariablesin: Coupling variables to set.  

??? abstract "get_CouplingVariables(self) → List[float] | None"
    Return subsystem i's coupling variables.


    **Returns:**
    > Coupling variables, or None if not set.  

??? abstract "set_Multipliers_CopyMappedResponse_Minus_CouplingVariable(self, copymappedresponse_minus_couplingvariable_in: List[float]) → None"
    Set the multipliers corresponding to the constraints where subsystem i's coupling variables appear.


    **Args:**
    > copymappedresponse_minus_couplingvariable_in: Multipliers for the copied mapped response minus coupling variable inconsistency.  

??? abstract "get_Multipliers_CopyMappedResponse_Minus_CouplingVariable(self) → List[float] | None"
    Return the multipliers corresponding to the constraints where subsystem i's coupling variables appear.


    **Returns:**
    > Right multipliers, or None if not set.  

??? abstract "set_Weights_CopyMappedResponse_Minus_CouplingVariable(self, copymappedresponse_minus_couplingvariable_in: List[float]) → None"
    Set the weights corresponding to the constraints where subsystem i's coupling variables appear.


    **Args:**
    > copymappedresponse_minus_couplingvariable_in: Weights for the copied mapped response minus coupling variable inconsistency.  

??? abstract "get_Weights_CopyMappedResponse_Minus_CouplingVariable(self) → List[float] | None"
    Return the weights corresponding to the constraints where subsystem i's coupling variables appear.


    **Returns:**
    > Right weights, or None if not set.  

??? abstract "set_SharedDesignVariables(self, shareddesignvariablesin: List[float]) → None"
    Set the shared design variables of subsystem i.


    **Args:**
    > shareddesignvariablesin: Shared design variables to set.  

??? abstract "get_SharedDesignVariables(self) → List[float] | None"
    Return the shared design variables of subsystem i.


    **Returns:**
    > Shared design variables, or None if not set.  

??? abstract "set_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, shareddesignvariable_minus_copytargetshareddesignvariable_in: List[float]) → None"
    Set multipliers w.r.t constraints where subsystem i's shared design vars appear.


    **Args:**
    > shareddesignvariable_minus_copytargetshareddesignvariable_in: Multipliers for the shared design variable minus copied target shared design variable inconsistency.  

??? abstract "get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self) → List[float] | None"
    Return multipliers w.r.t constraints where subsystem i's shared design vars appear.


    **Returns:**
    > Multipliers for shared design variables, or None if not set.  

??? abstract "set_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, shareddesignvariable_minus_copytargetshareddesignvariable_in: List[float]) → None"
    Set weights w.r.t. constraints where subsystem i's shared design vars appear.


    **Args:**
    > shareddesignvariable_minus_copytargetshareddesignvariable_in: Weights for the shared design variable minus copied target shared design variable inconsistency.  

??? abstract "get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self) → List[float] | None"
    Return weights w.r.t. constraints where subsystem i's shared design vars appear.


    **Returns:**
    > Weights for shared design variables, or None if not set.  

??? abstract "set_TargetSharedDesignVariables(self, targetshareddesignvariablesin: List[float]) → None"
    Set the target shared design variables of subsystem i.


    **Args:**
    > targetshareddesignvariablesin: Target shared design variables to set.  

??? abstract "get_TargetSharedDesignVariables(self) → List[float] | None"
    Return the target shared design variables of subsystem i.


    **Returns:**
    > Target shared design variables, or None if not set.  

??? abstract "set_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self, copyshareddesignvariable_minus_targetshareddesignvariable_in: List[float]) → None"
    Set multipliers w.r.t constraints where subsystem i's target shared design vars appear.


    **Args:**
    > copyshareddesignvariable_minus_targetshareddesignvariable_in: Multipliers for the copied shared design variable minus target shared design variable inconsistency.  

??? abstract "get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self) → List[float] | None"
    Return multipliers w.r.t constraints where subsystem i's target shared design vars appear.


    **Returns:**
    > Multipliers for target shared design variables, or None if not set.  

??? abstract "set_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self, copyshareddesignvariable_minus_targetshareddesignvariable_in: List[float]) → None"
    Set weights w.r.t. constraints where subsystem i's target shared design vars appear.


    **Args:**
    > copyshareddesignvariable_minus_targetshareddesignvariable_in: Weights for the copied shared design variable minus target shared design variable inconsistency.  

??? abstract "get_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self) → List[float] | None"
    Return weights w.r.t. constraints where subsystem i's target shared design vars appear.


    **Returns:**
    > Weights for target shared design variables, or None if not set.  

??? abstract "set_Indices_CouplingVariables_In_DesignVariables(self, indices_couplingvariables_in_designvariables_in: List[int]) → None"
    Set the indices of the design variables of subsystem i that correspond to the coupling variables of the i <-> j coupling.


    **Args:**
    > indices_couplingvariables_in_designvariables_in: Indices of the coupling variables  
    > in the design variables of subsystem i.  

??? abstract "get_Indices_CouplingVariables_In_DesignVariables(self) → List[int] | None"
    Get the indices of the design variables of subsystem i that correspond to the coupling variables of the i <-> j coupling.


    **Returns:**
    > Indices of the coupling variables in the design variables of subsystem i,  
    > or None if not set.  

??? abstract "set_Indices_SharedDesignVariables_In_DesignVariables(self, indices_shareddesignvariables_in_designvariables_in: List[int]) → None"
    Set the indices of the design variables of subsystem i that correspond to the shared design variables of the i <-> j coupling.


    **Args:**
    > indices_shareddesignvariables_in_designvariables_in: Indices of the shared design  
    > variables in the design variables of subsystem i.  

??? abstract "get_Indices_SharedDesignVariables_In_DesignVariables(self) → List[int] | None"
    Get the indices of the design variables of subsystem i that correspond to the shared design variables of the i <-> j coupling.


    **Returns:**
    > Indices of the shared design variables in the design variables of subsystem i,  
    > or None if not set.  

??? abstract "set_Indices_TargetSharedDesignVariables_In_DesignVariables(self, indices_targetshareddesignvariables_in_designvariables_in: List[int]) → None"
    Set the indices of the design variables of subsystem i that correspond to the target shared design variables of the i <-> j coupling.


    **Args:**
    > indices_targetshareddesignvariables_in_designvariables_in: Indices of the target shared  
    > design variables in the design variables of subsystem i.  

??? abstract "get_Indices_TargetSharedDesignVariables_In_DesignVariables(self) → List[int] | None"
    Get the indices of the design variables of subsystem i that correspond to the target shared design variables of the i <-> j coupling.


    **Returns:**
    > Indices of the target shared design variables in the design variables  
    > of subsystem i, or None if not set.  

??? abstract "update_state(self, other_coupling: [LocalToLocalForController_CouplingParameters](LocalToLocalForController_CouplingParameters.md#localtolocalforcontroller_couplingparameters)) → None"
    Update the state of this object from another LocalToLocalForController_CouplingParameters.

    This method is necessary for multiprocessing: when subsystems are executed
    in parallel via Parallel.py using multiprocessing.Pool, each process
    receives a copy of the data. After execution, the original objects must be
    updated with results from the executed copies. This method updates the
    numerical information stored in the class's attributes without changing
    the original memory address location, preserving object identity.

    Attributes are updated in the same order as defined in __init__().


    **Args:**
    > other_coupling: The source LocalToLocalForController_CouplingParameters containing updated values  
    > from parallel execution.  

