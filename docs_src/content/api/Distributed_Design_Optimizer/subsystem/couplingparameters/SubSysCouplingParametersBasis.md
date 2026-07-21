---
title: SubSysCouplingParametersBasis
---

← Back to [couplingparameters](index.md)

# SubSysCouplingParametersBasis

**Source:** [Distributed_Design_Optimizer\subsystem\couplingparameters\SubSysCouplingParametersBasis.py](SubSysCouplingParametersBasis_source.md)

Subsystem coupling parameters basis module.

This module provides the base class for subsystem-level coupling
parameters in distributed optimization.

## Classes

### SubSysCouplingParametersBasis

> **Inherits from:** [CouplingParametersBasis](CouplingParametersBasis.md#couplingparametersbasis)

> Base class for subsystem-level coupling parameters between local subsystems.

> Stores the coupling variables, mapped responses, shared design variables,
> their copies from the neighboring subsystem, associated Jacobians, and
> index mappings into the subsystem's design variable vector. All scaled
> quantities use [0, 1] scaling.

> The storage is defined as follows::

> subsystem 0
> //                 /

> mapped response 0 -> 1         coupling variable 1 -> 0


> coupling variable 0 -> 1         mapped response 1 -> 0

> /                  //
> subsystem 1

> Consider that the responses are stored locally for subsystem 0. Then:
> - mapping responses from  0 -> 1 is called mappedresponses
> - coupling variables from 1 -> 0 is called couplingvariable
> - coupling responses from 0 -> 1 is called copy_couplingvariable
> - mapping responses from  1 -> 0 is called copy_mappedresponses

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize coupling parameters for a subsystem.


    **Args:**
    > id: Identifier of the neighboring subsystem.  

??? abstract "get_CouplingVariable(self) → List[float] | None"
    Returns the coupling variables prescribed by the subsystem for a single neighboring subsystem.


    **Returns:**
    > Vector of coupling variables as scaled01 values.  

??? abstract "set_CouplingVariable(self, couplingvariable: List[float]) → None"
    Stores a new value of the coupling variables.


    **Args:**
    > couplingvariable: Coupling variables as scaled01 values.  

??? abstract "get_MappedResponses(self) → List[float] | None"
    Returns the physically mapped responses from the subsystem onto the neighboring subsystem.


    **Returns:**
    > Mapped responses as scaled01 values.  

??? abstract "set_MappedResponses(self, varin: List[float]) → None"
    Stores the mapped responses from the subsystem onto the neighboring subsystem.


    **Args:**
    > varin: Mapped responses as scaled01 values.  

??? abstract "set_CouplingVariable_Unscaled(self, couplingvariable: List[float]) → None"
    Stores the unscaled coupling variables.

    Note: No getter method is provided for unscaled values to prevent coordination
    methods from using unscaled values for coordination. Coordination should always
    use scaled [0,1] values to ensure numerical stability and consistency.


    **Args:**
    > couplingvariable: Coupling variables as unscaled values.  

??? abstract "set_MappedResponses_Unscaled(self, varin: List[float]) → None"
    Stores the unscaled mapped responses.

    Note: No getter method is provided for unscaled values to prevent coordination
    methods from using unscaled values for coordination. Coordination should always
    use scaled [0,1] values to ensure numerical stability and consistency.


    **Args:**
    > varin: Mapped responses as unscaled values.  

??? abstract "get_Copy_CouplingVariable(self) → List[float] | None"
    Gets the stored copy of the coupling variable of a neighboring subsystem.


    **Returns:**
    > Copy of the coupling variable as scaled01 values.  

??? abstract "set_Copy_CouplingVariable(self, varin: List[float]) → None"
    Stores a copy of the coupling variable representing the physical coupling required by a neighboring subsystem.


    **Args:**
    > varin: Copy of coupling variable as scaled01 values.  

??? abstract "get_Copy_MappedResponses(self) → List[float] | None"
    Gets the stored copy of the physical responses mapped onto this subsystem.


    **Returns:**
    > Copy of mapped responses as scaled01 values.  

??? abstract "set_Copy_MappedResponses(self, varin: List[float]) → None"
    Stores a copy of the mapped physical responses of a neighboring subsystem onto this subsystem.


    **Args:**
    > varin: Copy of mapped responses as scaled01 values.  

??? abstract "get_Jacobian_MappedResponse(self) → List[List[float | None]] | None"
    Returns the stored Jacobian of the mapped responses, possibly with missing values.


    **Returns:**
    > The Jacobian matrix, or None if not set.  

??? abstract "set_Jacobian_MappedResponse(self, jacobian_mappedresponse_in: List[List[float] | None]) → None"
    Sets the Jacobian of the mapped response from this subsystem's coupling.

    The Jacobian should have no missing values
    (or does not exist, if there are no mapped responses).


    **Args:**
    > jacobian_mappedresponse_in: The Jacobian matrix to set.  

??? abstract "set_Jacobian_MappedResponse_at_Position(self, i: int, j: int, jacobian_mappedresponse_point: float) → None"
    Sets value 'jacobian_mappedresponse_point' to the Jacobian at index (i,j).


    **Args:**
    > i: Row index of the Jacobian matrix.  
    > j: Column index of the Jacobian matrix.  
    > jacobian_mappedresponse_point: The value to set at position (i,j).  

??? abstract "get_Copy_Jacobian_MappedResponse(self) → List[List[float]] | None"
    Returns the Jacobian of the mapped response from the other subsystem's coupling.

    The Jacobian should have no missing values
    (or does not exist, if there are no mapped responses).


    **Returns:**
    > The copy Jacobian matrix, or None if not set.  

??? abstract "set_Copy_Jacobian_MappedResponse(self, copy_jacobian_mappedresponse_in: List[List[float] | None]) → None"
    Sets the Jacobian of the mapped response from the neighboring subsystem's coupling.

    The Jacobian should have no missing values
    (or does not exist, if there are no mapped responses).


    **Args:**
    > copy_jacobian_mappedresponse_in: The copy Jacobian matrix to set.  

??? abstract "set_SharedDesignVariables(self, variablesin: List[float]) → None"
    Sets the shared design variables which are shared with the neighboring subsystem.


    **Args:**
    > variablesin: Shared design variables as scaled01 values.  

??? abstract "get_SharedDesignVariables(self) → List[float] | None"
    Gets the shared design variables.


    **Returns:**
    > Shared design variables as scaled01 values.  

??? abstract "set_SharedDesignVariables_Unscaled(self, variablesin: List[float]) → None"
    Stores the unscaled shared design variables.

    Note: No getter method is provided for unscaled values to prevent coordination
    methods from using unscaled values for coordination. Coordination should always
    use scaled [0,1] values to ensure numerical stability and consistency.


    **Args:**
    > variablesin: Shared design variables as unscaled values.  

??? abstract "set_Copy_SharedDesignVariables(self, copy_ofvariablesin: List[float]) → None"
    Sets a copy of the shared design variable value of the neighboring subsystem.


    **Args:**
    > copy_ofvariablesin: Copy of shared design variables as scaled01 values.  

??? abstract "get_Copy_SharedDesignVariables(self) → List[float] | None"
    Gets the copy of the shared design variable of the neighboring subsystem.


    **Returns:**
    > Copy of shared design variables as scaled01 values.  

??? abstract "set_TargetSharedDesignVariables(self, variablesin: List[float]) → None"
    Sets the target shared design variables which are shared with the neighboring subsystem.


    **Args:**
    > variablesin: Target shared design variables as scaled01 values.  

??? abstract "get_TargetSharedDesignVariables(self) → List[float] | None"
    Gets the target shared design variables.


    **Returns:**
    > Target shared design variables as scaled01 values.  

??? abstract "set_TargetSharedDesignVariables_Unscaled(self, variablesin: List[float]) → None"
    Stores the unscaled target shared design variables.

    Note: No getter method is provided for unscaled values to prevent coordination
    methods from using unscaled values for coordination. Coordination should always
    use scaled [0,1] values to ensure numerical stability and consistency.


    **Args:**
    > variablesin: Target shared design variables as unscaled values.  

??? abstract "set_Copy_TargetSharedDesignVariables(self, copy_ofvariablesin: List[float]) → None"
    Sets a copy of the shared design variable value of the neighboring subsystem.


    **Args:**
    > copy_ofvariablesin: Copy of target shared design variables as scaled01 values.  

??? abstract "get_Copy_TargetSharedDesignVariables(self) → List[float] | None"
    Gets the copy of the shared design variable of the neighboring subsystem.


    **Returns:**
    > Copy of target shared design variables as scaled01 values.  

??? abstract "set_CouplingStrength(self, couplingstrengthIn: float) → None"
    Sets the coupling strength value.


    **Args:**
    > couplingstrengthIn: The coupling strength value to set.  

??? abstract "get_CouplingStrength(self) → float | None"
    Gets the coupling strength value.


    **Returns:**
    > The coupling strength value, or None if not set.  

??? abstract "set_Indices_CouplingVariables_In_DesignVariables(self, indices_couplingvariables_in_designvariables_in: List[int]) → None"
    Sets the indices of coupling variables within the design variables vector.


    **Args:**
    > indices_couplingvariables_in_designvariables_in: Indices of the coupling variables  
    > in the designvariables of subsystem i.  

??? abstract "get_Indices_CouplingVariables_In_DesignVariables(self) → List[int] | None"
    Gets the indices of coupling variables within the design variables vector.


    **Returns:**
    > Indices of the coupling variables in the designvariables of subsystem i,  
    > or None if not set.  

??? abstract "set_Indices_SharedDesignVariables_In_DesignVariables(self, indices_shareddesignvariables_in_designvariables_in: List[int]) → None"
    Sets the indices of shared design variables within the design variables vector.


    **Args:**
    > indices_shareddesignvariables_in_designvariables_in: Indices of the shared design  
    > variables in the designvariables of subsystem i.  

??? abstract "get_Indices_SharedDesignVariables_In_DesignVariables(self) → List[int] | None"
    Gets the indices of shared design variables within the design variables vector.


    **Returns:**
    > Indices of the shared design variables in the designvariables of subsystem i,  
    > or None if not set.  

??? abstract "set_Indices_TargetSharedDesignVariables_In_DesignVariables(self, indices_targetshareddesignvariables_in_designvariables_in: List[int]) → None"
    Sets the indices of target shared design variables within the design variables vector.


    **Args:**
    > indices_targetshareddesignvariables_in_designvariables_in: Indices of the target shared  
    > design variables in the designvariables of subsystem i.  

??? abstract "get_Indices_TargetSharedDesignVariables_In_DesignVariables(self) → List[int] | None"
    Gets the indices of target shared design variables within the design variables vector.


    **Returns:**
    > Indices of the target shared design variables in the designvariables  
    > of subsystem i, or None if not set.  

??? abstract "update_state(self, other_coupling: [SubSysCouplingParametersBasis](SubSysCouplingParametersBasis.md#subsyscouplingparametersbasis)) → None"
    Update the state of this SubSysCouplingParametersBasis with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.

    The update preserves memory addresses by modifying list contents in-place rather than
    reassigning references. This is essential for maintaining object identity across the
    multiprocessing boundary.


    **Args:**
    > other_coupling: The source SubSysCouplingParametersBasis containing updated values  
    > from parallel execution.  

