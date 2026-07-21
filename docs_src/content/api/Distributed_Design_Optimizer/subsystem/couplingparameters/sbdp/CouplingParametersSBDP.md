---
title: CouplingParametersSBDP
---

← Back to [sbdp](index.md)

# CouplingParametersSBDP

**Source:** [Distributed_Design_Optimizer\subsystem\couplingparameters\sbdp\CouplingParametersSBDP.py](CouplingParametersSBDP_source.md)

SBDP coupling parameters module.

This module provides coupling parameters for the Sensitivity Based Distributed
Programming (SBDP) method.

In SBDP each subsystem imposes a hard coordination equality constraint made of
two blocks:

[ H(r) - h ; S_z d - z ] = 0   | lambda

where the first (mapped-response) block carries the multiplier ``lambda_h`` and
the second (shared-design-variable) block carries the multiplier ``lambda_z``.
These multipliers are computed locally (KKT) and communicated to the neighboring
subsystem via the middle level, where they are stored as the neighbor's
``copy_multipliers``. The neighbor then uses them to build the sensitivity term
of its own subproblem objective.

## Classes

### CouplingParametersSBDP

> **Inherits from:** [SubSysCouplingParametersBasis](../SubSysCouplingParametersBasis.md#subsyscouplingparametersbasis)

> Coupling parameters for Sensitivity Based Distributed Programming.

> Extends SubSysCouplingParametersBasis with the Lagrange multipliers of the
> coordination equality constraint blocks (own multipliers) and the copies of
> the neighbor's multipliers pulled from the middle level.

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize CouplingParametersSBDP.


    **Args:**
    > id: Identifier of the neighboring subsystem.  

??? abstract "set_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self, multipliersin: List[float]) → None"
    Set the own multipliers of the mapped-response coordination equality block.


    **Args:**
    > multipliersin: Lagrange multipliers of the mapped-response block.  

??? abstract "get_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self) → List[float] | None"
    Return the own multipliers of the mapped-response coordination equality block.


    **Returns:**
    > Lagrange multipliers of the mapped-response block, or None if not set.  

??? abstract "set_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, multipliersin: List[float]) → None"
    Set the own multipliers of the shared-design-variable coordination equality block.


    **Args:**
    > multipliersin: Lagrange multipliers of the shared-design-variable block.  

??? abstract "get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self) → List[float] | None"
    Return the own multipliers of the shared-design-variable coordination equality block.


    **Returns:**
    > Lagrange multipliers of the shared-design-variable block, or None if not set.  

??? abstract "set_Copy_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self, multipliersin: List[float]) → None"
    Set the copy of the neighbor's mapped-response block multipliers.


    **Args:**
    > multipliersin: Neighbor's Lagrange multipliers of the mapped-response block.  

??? abstract "get_Copy_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self) → List[float] | None"
    Return the copy of the neighbor's mapped-response block multipliers.


    **Returns:**
    > Neighbor's mapped-response block multipliers, or None if not set.  

??? abstract "set_Copy_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, multipliersin: List[float]) → None"
    Set the copy of the neighbor's shared-design-variable block multipliers.


    **Args:**
    > multipliersin: Neighbor's Lagrange multipliers of the shared-design-variable block.  

??? abstract "get_Copy_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self) → List[float] | None"
    Return the copy of the neighbor's shared-design-variable block multipliers.


    **Returns:**
    > Neighbor's shared-design-variable block multipliers, or None if not set.  

??? abstract "set_Sensitivity_Gradient(self, sensitivity_gradient_in: List[float]) → None"
    Set this neighbor's contribution to the coordination-objective sensitivity gradient.


    **Args:**
    > sensitivity_gradient_in: Sensitivity gradient grad_d^j L^(k) scattered into the  
    > subsystem's design-variable space.  

??? abstract "get_Sensitivity_Gradient(self) → List[float] | None"
    Return this neighbor's contribution to the coordination-objective sensitivity gradient.


    **Returns:**
    > Sensitivity gradient grad_d^j L^(k) scattered into the subsystem's  
    > design-variable space, or None if not set.  

??? abstract "CopyFromMiddleLevelCoupling(self, middlelevelcouplingIn: [MiddleLevelCouplingSBDP](../../../middlelevel/sbdp/MiddleLevelCouplingSBDP.md#middlelevelcouplingsbdp)) → None"
    Copy coupling data from a MiddleLevelCoupling object.


    **Args:**
    > middlelevelcouplingIn: The MiddleLevelCoupling object to copy data from.  


    **Raises:**
    > ValueError: If middlelevelcouplingIn is not a MiddleLevelCouplingSBDP instance.  

??? abstract "CopyToMiddleLevelCoupling(self, middlelevelcouplingIn: [MiddleLevelCouplingSBDP](../../../middlelevel/sbdp/MiddleLevelCouplingSBDP.md#middlelevelcouplingsbdp)) → None"
    Copy coupling data to a MiddleLevelCoupling object.


    **Args:**
    > middlelevelcouplingIn: The MiddleLevelCoupling object to copy data to.  


    **Raises:**
    > ValueError: If middlelevelcouplingIn is not a MiddleLevelCouplingSBDP instance.  

??? abstract "update_state(self, other_coupling: [CouplingParametersSBDP](CouplingParametersSBDP.md#couplingparameterssbdp)) → None"
    Update the state of this CouplingParametersSBDP with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.

    The update preserves memory addresses by modifying list contents in-place rather than
    reassigning references. This is essential for maintaining object identity across the
    multiprocessing boundary.


    **Args:**
    > other_coupling: The source CouplingParametersSBDP containing updated values  
    > from parallel execution.  

