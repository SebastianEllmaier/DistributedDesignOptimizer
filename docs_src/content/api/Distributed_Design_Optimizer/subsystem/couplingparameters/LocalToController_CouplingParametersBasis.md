---
title: LocalToController_CouplingParametersBasis
---

← Back to [couplingparameters](index.md)

# LocalToController_CouplingParametersBasis

**Source:** [Distributed_Design_Optimizer\subsystem\couplingparameters\LocalToController_CouplingParametersBasis.py](LocalToController_CouplingParametersBasis_source.md)

Local to controller coupling parameters basis module.

This module provides the base class for local subsystem-level coupling
parameters, which are determined for the controller, in hierarchical
distributed optimization.

## Classes

### LocalToController_CouplingParametersBasis

> **Inherits from:** [CouplingParametersBasis](CouplingParametersBasis.md#couplingparametersbasis)

> Base class for local subsystem-level coupling parameters determined for the controller.

> Holds the coupling parameters between a single local subsystem and a
> controller. The local subsystem exchanges local coupling information
> (local to controller). Subclasses add algorithm-specific attributes
> (e.g., ALADIN auxiliary variables and Jacobians).

#### Methods

??? abstract "__init__(self) → None"
    Initialize local-to-controller coupling parameters.

    Since this coupling parameter is stored in the local subsystem and
    with respect to the controller, the ID of this coupling parameter is "C".

??? abstract "update_state(self, other_coupling: [LocalToController_CouplingParametersBasis](LocalToController_CouplingParametersBasis.md#localtocontroller_couplingparametersbasis)) → None"
    Update the state of this LocalToController_CouplingParametersBasis with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.

    Note: This base class does not define any local attributes. Subclasses that add
    algorithm-specific attributes (e.g., auxiliary variables, jacobians) must override
    this method to update those attributes while calling super().update_state().


    **Args:**
    > other_coupling: The source LocalToController_CouplingParametersBasis containing updated values  
    > from parallel execution.  

