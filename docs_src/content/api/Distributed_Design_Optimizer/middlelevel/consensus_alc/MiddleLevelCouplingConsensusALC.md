---
title: MiddleLevelCouplingConsensusALC
---

← Back to [consensus_alc](index.md)

# MiddleLevelCouplingConsensusALC

**Source:** [Distributed_Design_Optimizer\middlelevel\consensus_alc\MiddleLevelCouplingConsensusALC.py](MiddleLevelCouplingConsensusALC_source.md)

Middle-level coupling for consensus-based ALC.

This module provides middle-level coupling management for
consensus-based Augmented Lagrangian Coordination.

## Classes

### MiddleLevelCouplingConsensusALC

> **Inherits from:** [SubSysMiddleLevelCouplingBasis](../SubSysMiddleLevelCouplingBasis.md#subsysmiddlelevelcouplingbasis)

> Middle-level coupling for consensus-based ALC.

> Handles coupling data between subsystems for consensus-based
> Augmented Lagrangian Coordination.

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize middle-level coupling.


    **Args:**
    > id: Identifier of the neighboring subsystem.  

??? abstract "set_Weights_Auxiliary_Minus_MappedResponse(self, weightsin: List[float]) → None"
    Set the weights for the auxiliary-minus-mapped-response part of the coupling circle.


    **Args:**
    > weightsin: Weights to set.  

??? abstract "get_Weights_Auxiliary_Minus_MappedResponse(self) → List[float] | None"
    Return the weights for the auxiliary-minus-mapped-response part of the coupling circle.


    **Returns:**
    > The weights or None if not set.  

??? abstract "set_Weights_Auxiliary_Minus_CouplingVariable(self, weightsin: List[float]) → None"
    Set the weights for the auxiliary-minus-coupling-variable part of the coupling circle.


    **Args:**
    > weightsin: Weights to set.  

??? abstract "get_Weights_Auxiliary_Minus_CouplingVariable(self) → List[float] | None"
    Return the weights for the auxiliary-minus-coupling-variable part of the coupling circle.


    **Returns:**
    > The weights or None if not set.  

??? abstract "set_Weights_Auxiliary_Minus_SharedDesignVariable(self, weightsin: List[float]) → None"
    Set the weights for the auxiliary-minus-shared-design-variable part of the coupling circle.


    **Args:**
    > weightsin: Weights to set.  

??? abstract "get_Weights_Auxiliary_Minus_SharedDesignVariable(self) → List[float] | None"
    Return the weights for the auxiliary-minus-shared-design-variable part of the coupling circle.


    **Returns:**
    > The weights or None if not set.  

??? abstract "set_Weights_Auxiliary_Minus_TargetSharedDesignVariable(self, weightsin: List[float]) → None"
    Set the weights for the auxiliary-minus-target-shared-design-variable part of the coupling circle.


    **Args:**
    > weightsin: Weights to set.  

??? abstract "get_Weights_Auxiliary_Minus_TargetSharedDesignVariable(self) → List[float] | None"
    Return the weights for the auxiliary-minus-target-shared-design-variable part of the coupling circle.


    **Returns:**
    > The weights or None if not set.  

??? abstract "set_Multipliers_Auxiliary_Minus_MappedResponse(self, multipliersin: List[float]) → None"
    Set the Lagrange multipliers for the auxiliary-minus-mapped-response part of the coupling circle.


    **Args:**
    > multipliersin: Lagrange multipliers to set.  

??? abstract "get_Multipliers_Auxiliary_Minus_MappedResponse(self) → List[float] | None"
    Return the Lagrange multipliers for the auxiliary-minus-mapped-response part of the coupling circle.


    **Returns:**
    > The Lagrange multipliers or None if not set.  

??? abstract "set_Multipliers_Auxiliary_Minus_CouplingVariable(self, multipliersin: List[float]) → None"
    Set the Lagrange multipliers for the auxiliary-minus-coupling-variable part of the coupling circle.


    **Args:**
    > multipliersin: Lagrange multipliers to set.  

??? abstract "get_Multipliers_Auxiliary_Minus_CouplingVariable(self) → List[float] | None"
    Return the Lagrange multipliers for the auxiliary-minus-coupling-variable part of the coupling circle.


    **Returns:**
    > The Lagrange multipliers or None if not set.  

??? abstract "set_Multipliers_Auxiliary_Minus_SharedDesignVariable(self, multipliersin: List[float]) → None"
    Set the Lagrange multipliers for the auxiliary-minus-shared-design-variable part of the coupling circle.


    **Args:**
    > multipliersin: Lagrange multipliers to set.  

??? abstract "get_Multipliers_Auxiliary_Minus_SharedDesignVariable(self) → List[float] | None"
    Return the Lagrange multipliers for the auxiliary-minus-shared-design-variable part of the coupling circle.


    **Returns:**
    > The Lagrange multipliers or None if not set.  

??? abstract "set_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable(self, multipliersin: List[float]) → None"
    Set the Lagrange multipliers for the auxiliary-minus-target-shared-design-variable part of the coupling circle.


    **Args:**
    > multipliersin: Lagrange multipliers to set.  

??? abstract "get_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable(self) → List[float] | None"
    Return the Lagrange multipliers for the auxiliary-minus-target-shared-design-variable part of the coupling circle.


    **Returns:**
    > The Lagrange multipliers or None if not set.  

??? abstract "update_state(self, other_middlelevelcoupling: [MiddleLevelCouplingConsensusALC](MiddleLevelCouplingConsensusALC.md#middlelevelcouplingconsensusalc)) → None"
    Update the state of this MiddleLevelCoupling with another instance.

    This method updates the numerical information stored in the class's attributes
    without changing the original memory address location. This is necessary for
    multiprocessing, where executed subsystems return from separate processes and
    their state must be transferred back to the original objects in the main process.


    **Args:**
    > other_middlelevelcoupling: The source instance to copy state from.  

