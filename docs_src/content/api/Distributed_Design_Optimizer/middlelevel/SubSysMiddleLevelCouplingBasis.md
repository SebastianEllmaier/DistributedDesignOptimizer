---
title: SubSysMiddleLevelCouplingBasis
---

← Back to [middlelevel](index.md)

# SubSysMiddleLevelCouplingBasis

**Source:** [Distributed_Design_Optimizer\middlelevel\SubSysMiddleLevelCouplingBasis.py](SubSysMiddleLevelCouplingBasis_source.md)

Local middle-level coupling basis module.

This module provides the base class for local-side middle-level coupling
parameters in distributed optimization.

## Classes

### SubSysMiddleLevelCouplingBasis

> **Inherits from:** [MiddleLevelCouplingBasis](MiddleLevelCouplingBasis.md#middlelevelcouplingbasis)

> A LocalMiddleLevelCoupling object holds the coupling parameters between a subsystem and a single neighbor.
> It stores the identifier of the neighbor and stores the couplingvariables

> The storage is defined as follows:
> Consider two coupled subsystems

> subsystem 0
> //                 /

> mapped response 0 -> 1         expected response 1 -> 0


> expected response 0 -> 1       mapped response 1 -> 0

> /                  //
> subsystem 1

> Consider that the reponses are stored locally for subsystem 0. Then:
> mapped response 0 -> 1   is called mappedresponses
> expected response 1 -> 0 is called couplingvariable
> and
> expected response 0 -> 1 is called couplingvariable
> mapped response 1 -> 0   is called mappedresponses

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize the local middle level coupling.


    **Args:**
    > id: Identifier of the neighboring subsystem.  

??? abstract "set_CouplingVariable(self, couplingvariable: List[float]) → None"
    Set the coupling variable values (scaled01).


    **Args:**
    > couplingvariable: Scaled [0,1] coupling variable values.  

??? abstract "get_CouplingVariable(self) → List[float] | None"
    Get the coupling variable values (scaled01).


    **Returns:**
    > Scaled [0,1] coupling variable values or None.  

??? abstract "set_MappedResponses(self, varin: List[float]) → None"
    Set the mapped response variable values (scaled01).


    **Args:**
    > varin: Scaled [0,1] mapped response values.  

??? abstract "get_MappedResponses(self) → List[float] | None"
    Get the mapped response variable values (scaled01).


    **Returns:**
    > Scaled [0,1] mapped response values or None.  

??? abstract "set_SharedDesignVariable(self, variablesin: List[float]) → None"
    Set the shared design variable values (scaled01).


    **Args:**
    > variablesin: Scaled [0,1] shared design variable values.  

??? abstract "get_SharedDesignVariable(self) → List[float] | None"
    Get the shared design variable values (scaled01).


    **Returns:**
    > Scaled [0,1] shared design variable values or None.  

??? abstract "set_TargetSharedDesignVariable(self, variablesin: List[float]) → None"
    Set the target shared design variable values (scaled01).


    **Args:**
    > variablesin: Scaled [0,1] target shared design variable values.  

??? abstract "get_TargetSharedDesignVariable(self) → List[float] | None"
    Get the target shared design variable values (scaled01).


    **Returns:**
    > Scaled [0,1] target shared design variable values or None.  

??? abstract "update_state(self, other_middlelevelcoupling: [SubSysMiddleLevelCouplingBasis](SubSysMiddleLevelCouplingBasis.md#subsysmiddlelevelcouplingbasis)) → None"
    Update the state of this SubSysMiddleLevelCouplingBasis from another instance.

    This method is necessary for multiprocessing. When subsystems are executed
    in parallel processes via Parallel.py, the original objects need to
    be updated with results from the executed copies. This method preserves
    the memory address of the object's attributes while updating their values.


    **Args:**
    > other_middlelevelcoupling: The source instance containing updated values to copy from.  

    Note on copy operations:
    - Base class attribute (_id): Handled by super().update_state()
    - List[float] attributes: Use update_state_listprimitive() which updates in-place
    to preserve memory address. The getter methods already return copy.copy()
    of the lists, providing the necessary isolation from the source.

