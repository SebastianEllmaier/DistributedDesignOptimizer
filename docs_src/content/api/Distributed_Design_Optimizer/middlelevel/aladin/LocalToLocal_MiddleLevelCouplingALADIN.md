---
title: LocalToLocal_MiddleLevelCouplingALADIN
---

← Back to [aladin](index.md)

# LocalToLocal_MiddleLevelCouplingALADIN

**Source:** [Distributed_Design_Optimizer\middlelevel\aladin\LocalToLocal_MiddleLevelCouplingALADIN.py](LocalToLocal_MiddleLevelCouplingALADIN_source.md)

Local-to-local middle-level coupling module for ALADIN.

This module provides middle-level coupling management for local-to-local
subsystem communication in ALADIN coordination.

## Classes

### LocalToLocal_MiddleLevelCouplingALADIN

> **Inherits from:** [SubSysMiddleLevelCouplingBasis](../SubSysMiddleLevelCouplingBasis.md#subsysmiddlelevelcouplingbasis)

> Middle-level coupling for local-to-local communication in ALADIN.

> Handles coupling data between two local subsystems for the ALADIN
> coordination method.

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize local-to-local middle-level coupling.


    **Args:**
    > id: Identifier of the neighboring subsystem.  

??? abstract "set_MappedResponses_D_Hat(self, varin: List[float]) → None"
    Set mapped response variables evaluated at d_hat.


    **Args:**
    > varin: Mapped response values evaluated at d_hat.  

??? abstract "get_MappedResponses_D_Hat(self) → List[float] | None"
    Get mapped response variables evaluated at d_hat.


    **Returns:**
    > Mapped response values evaluated at d_hat, or None.  

??? abstract "set_CouplingVariable_D_Hat(self, couplingvariable_d_hat_in: List[float]) → None"
    Set coupling variable evaluated at d_hat.


    **Args:**
    > couplingvariable_d_hat_in: Coupling variable values evaluated at d_hat.  

??? abstract "get_CouplingVariable_D_Hat(self) → List[float] | None"
    Get coupling variable evaluated at d_hat.


    **Returns:**
    > Coupling variable values evaluated at d_hat, or None.  

??? abstract "set_SharedDesignVariable_D_Hat(self, variablesin: List[float]) → None"
    Set shared design variables evaluated at d_hat.


    **Args:**
    > variablesin: Shared design variable values evaluated at d_hat.  

??? abstract "get_SharedDesignVariable_D_Hat(self) → List[float] | None"
    Get shared design variables evaluated at d_hat.


    **Returns:**
    > Shared design variable values evaluated at d_hat, or None.  

??? abstract "set_TargetSharedDesignVariable_D_Hat(self, variablesin: List[float]) → None"
    Set target shared design variables evaluated at d_hat.


    **Args:**
    > variablesin: Target shared design variable values evaluated at d_hat.  

??? abstract "get_TargetSharedDesignVariable_D_Hat(self) → List[float] | None"
    Get target shared design variables evaluated at d_hat.


    **Returns:**
    > Target shared design variable values evaluated at d_hat, or None.  

??? abstract "update_state(self, other_middlelevelcoupling: [LocalToLocal_MiddleLevelCouplingALADIN](LocalToLocal_MiddleLevelCouplingALADIN.md#localtolocal_middlelevelcouplingaladin)) → None"
    Update the state of this LocalToLocal_MiddleLevelCouplingALADIN with another instance.

    This method updates the numerical information stored in the class's attributes
    without changing the original memory address location. This is necessary for
    multiprocessing, where executed subsystems return from separate processes and
    their state must be transferred back to the original objects in the main process.


    **Args:**
    > other_middlelevelcoupling: The source instance to copy state from.  

