---
title: CouplingParametersInterface
---

← Back to [couplingparameters](index.md)

# CouplingParametersInterface

**Source:** [Distributed_Design_Optimizer\subsystem\couplingparameters\CouplingParametersInterface.py](CouplingParametersInterface_source.md)

Coupling parameters interface module.

This module defines the abstract interface for coupling parameters
in multilevel coordination.

## Classes

### CouplingParametersInterface

> **Inherits from:** `ABC`

> Interface for coupling parameters between subsystems.

> A CouplingParameters object holds the coupling parameters between
> a subsystem and a single neighbor. It stores the identifier of the neighbor
> and stores the couplingvariables.

#### Methods

??? abstract "get_ID(self) → str"
    Return the identifier of the neighboring subsystem.


    **Returns:**
    > The neighbor identifier.  

??? abstract "CopyFromMiddleLevelCoupling(self, middlelevelcouplingIn: [MiddleLevelCouplingInterface](../../middlelevel/MiddleLevelCouplingInterface.md#middlelevelcouplinginterface)) → None"
    Copy coupling parameters from the middle level.


    **Args:**
    > middlelevelcouplingIn: The middle level coupling to copy from.  

??? abstract "CopyToMiddleLevelCoupling(self, middlelevelcouplingIn: [MiddleLevelCouplingInterface](../../middlelevel/MiddleLevelCouplingInterface.md#middlelevelcouplinginterface)) → None"
    Copy coupling parameters to the middle level.


    **Args:**
    > middlelevelcouplingIn: The middle level coupling to copy to.  

??? abstract "update_state(self, other_coupling: [CouplingParametersInterface](CouplingParametersInterface.md#couplingparametersinterface)) → None"
    Update the state of this object with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.

    Implementation Guidelines for Subclasses:
    - Call super().update_state(other_coupling=other_coupling) first to handle inherited attributes
    - For primitives (str, float, int, bool, None): Use direct assignment
    - For List[float]: Use update_state_listprimitive() for in-place updates
    - For List[List[float]]: Iterate and use update_state_listprimitive() per inner list
    - For nested class objects: Call their update_state() methods
    - Maintain the same attribute order as defined in __init__()


    **Args:**
    > other_coupling: The source CouplingParametersInterface containing updated values  
    > from parallel execution.  

