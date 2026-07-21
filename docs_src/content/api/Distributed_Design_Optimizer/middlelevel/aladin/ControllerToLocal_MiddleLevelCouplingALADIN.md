---
title: ControllerToLocal_MiddleLevelCouplingALADIN
---

← Back to [aladin](index.md)

# ControllerToLocal_MiddleLevelCouplingALADIN

**Source:** [Distributed_Design_Optimizer\middlelevel\aladin\ControllerToLocal_MiddleLevelCouplingALADIN.py](ControllerToLocal_MiddleLevelCouplingALADIN_source.md)

Controller-to-local middle-level coupling module for ALADIN.

This module provides middle-level coupling management for controller-to-local
subsystem communication in ALADIN coordination.

## Classes

### ControllerToLocal_MiddleLevelCouplingALADIN

> **Inherits from:** [ControllerToLocal_MiddleLevelCouplingBasis](../ControllerToLocal_MiddleLevelCouplingBasis.md#controllertolocal_middlelevelcouplingbasis)

> Middle level coupling updated by the controller.

> Handles the coupling from the controller to a local subsystem
> (middlelevel between controller and local subsystem).

#### Methods

??? abstract "__init__(self, local_neighbors_list: List[str]) → None"
    Initialize controller-to-local middle-level coupling.


    **Args:**
    > local_neighbors_list: List of local neighbor identifiers.  

??? abstract "get_Delta_D(self) → List[float] | None"
    Return the list delta_d from controller.


    **Returns:**
    > List[float] | None: The delta_d list from the controller.  

??? abstract "set_Delta_D(self, delta_d_in: List[float]) → None"
    Set the list delta_d from controller.


    **Args:**
    > delta_d_in (List[float]): The delta_d list to set.  

??? abstract "update_state(self, other_middlelevelcoupling: [ControllerToLocal_MiddleLevelCouplingALADIN](ControllerToLocal_MiddleLevelCouplingALADIN.md#controllertolocal_middlelevelcouplingaladin)) → None"
    Update the state of this ControllerToLocal_MiddleLevelCouplingALADIN with another instance.

    This operation preserves the memory address of the object's attributes
    and only updates the value(s). This method is necessary for multiprocessing,
    where executed subsystems need to transfer their state back to the original objects.


    **Args:**
    > other_middlelevelcoupling: The ControllerToLocal_MiddleLevelCouplingALADIN to copy state from.  

