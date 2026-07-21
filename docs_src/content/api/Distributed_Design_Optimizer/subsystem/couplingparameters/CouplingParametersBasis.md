---
title: CouplingParametersBasis
---

← Back to [couplingparameters](index.md)

# CouplingParametersBasis

**Source:** [Distributed_Design_Optimizer\subsystem\couplingparameters\CouplingParametersBasis.py](CouplingParametersBasis_source.md)

Coupling parameters basis module.

This module provides the base class for coupling parameters in
multilevel distributed optimization.

## Classes

### CouplingParametersBasis

> **Inherits from:** [CouplingParametersInterface](CouplingParametersInterface.md#couplingparametersinterface)

> Base implementation of coupling parameters storing the neighbor identifier.

> Provides the common ``_id`` attribute and its getter, shared by both
> subsystem-level and controller-level coupling parameter subclasses.

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize coupling parameters.


    **Args:**
    > id: Identifier of the neighboring subsystem.  

??? abstract "get_ID(self) → str"
    Return the identifier of the neighboring subsystem.


    **Returns:**
    > The neighbor identifier.  

??? abstract "update_state(self, other_coupling: [CouplingParametersBasis](CouplingParametersBasis.md#couplingparametersbasis)) → None"
    Update the state of this CouplingParametersBasis with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.

    For primitive/immutable types like str, direct assignment is safe since Python
    creates a new binding rather than modifying the original value.


    **Args:**
    > other_coupling: The source CouplingParametersBasis containing updated values  
    > from parallel execution.  

