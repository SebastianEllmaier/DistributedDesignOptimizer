---
title: ControllerCouplingParametersBasis
---

← Back to [couplingparameters](index.md)

# ControllerCouplingParametersBasis

**Source:** [Distributed_Design_Optimizer\subsystem\couplingparameters\ControllerCouplingParametersBasis.py](ControllerCouplingParametersBasis_source.md)

Controller coupling parameters basis module.

This module provides the base class for controller-level coupling
parameters in hierarchical distributed optimization.

## Classes

### ControllerCouplingParametersBasis

> **Inherits from:** [CouplingParametersBasis](CouplingParametersBasis.md#couplingparametersbasis)

> Base class for controller-level coupling parameters in hierarchical coordination.

> Holds the coupling parameters between a controller subsystem and a single
> local subsystem. The controller exchanges auxiliary variables (controller
> to local) and local coupling information (local to controller). Subclasses
> add algorithm-specific attributes (e.g., ALADIN auxiliary variables and
> Jacobians).

> The storage is defined as follows::

> subsystem 0
> //                 /

> localcoupling 0 -> C         auxiliary C -> 0
> information

> /                  //
> Controller

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize controller coupling parameters.


    **Args:**
    > id: Identifier of the neighboring subsystem.  

??? abstract "update_state(self, other_coupling: [ControllerCouplingParametersBasis](ControllerCouplingParametersBasis.md#controllercouplingparametersbasis)) → None"
    Update the state of this ControllerCouplingParametersBasis with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.

    Note: This base class does not define any local attributes. Subclasses that add
    algorithm-specific attributes (e.g., auxiliary variables, jacobians) must override
    this method to update those attributes while calling super().update_state().


    **Args:**
    > other_coupling: The source ControllerCouplingParametersBasis containing updated values  
    > from parallel execution.  

