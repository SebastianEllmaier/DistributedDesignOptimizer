---
title: MiddleLevelCouplingSBDP
---

← Back to [sbdp](index.md)

# MiddleLevelCouplingSBDP

**Source:** [Distributed_Design_Optimizer\middlelevel\sbdp\MiddleLevelCouplingSBDP.py](MiddleLevelCouplingSBDP_source.md)

Middle-level coupling for Sensitivity Based Distributed Programming (SBDP).

This module provides middle-level coupling management for SBDP. In addition to
the base coupling quantities, it stores the Lagrange multipliers of the
coordination (hard) equality constraints so that they can be communicated to
the neighboring subsystem via the middle level.

## Classes

### MiddleLevelCouplingSBDP

> **Inherits from:** [SubSysMiddleLevelCouplingBasis](../SubSysMiddleLevelCouplingBasis.md#subsysmiddlelevelcouplingbasis)

> Middle-level coupling for SBDP.

> Handles coupling data between subsystems for Sensitivity Based Distributed
> Programming, including the Lagrange multipliers of the coordination
> equality constraints (mapped-response and shared-design-variable blocks).

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize middle-level coupling.


    **Args:**
    > id: Identifier of the neighboring subsystem.  

??? abstract "set_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self, multipliersin: List[float]) → None"
    Set the multipliers of the mapped-response coordination equality block.


    **Args:**
    > multipliersin: Lagrange multipliers of the mapped-response block.  

??? abstract "get_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self) → List[float] | None"
    Return the multipliers of the mapped-response coordination equality block.


    **Returns:**
    > The Lagrange multipliers or None if not set.  

??? abstract "set_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, multipliersin: List[float]) → None"
    Set the multipliers of the shared-design-variable coordination equality block.


    **Args:**
    > multipliersin: Lagrange multipliers of the shared-design-variable block.  

??? abstract "get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self) → List[float] | None"
    Return the multipliers of the shared-design-variable coordination equality block.


    **Returns:**
    > The Lagrange multipliers or None if not set.  

??? abstract "update_state(self, other_middlelevelcoupling: [MiddleLevelCouplingSBDP](MiddleLevelCouplingSBDP.md#middlelevelcouplingsbdp)) → None"
    Update the state of this MiddleLevelCoupling from another instance.

    This method updates the numerical information stored in the class's attributes
    without changing the original memory address location. This is necessary for
    multiprocessing, where executed subsystems return from separate processes and
    their state must be transferred back to the original objects in the main process.


    **Args:**
    > other_middlelevelcoupling: The source instance to copy state from.  

