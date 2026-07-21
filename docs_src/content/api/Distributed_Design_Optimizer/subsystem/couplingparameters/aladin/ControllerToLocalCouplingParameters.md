---
title: ControllerToLocalCouplingParameters
---

← Back to [aladin](index.md)

# ControllerToLocalCouplingParameters

**Source:** [Distributed_Design_Optimizer\subsystem\couplingparameters\aladin\ControllerToLocalCouplingParameters.py](ControllerToLocalCouplingParameters_source.md)

Controller to local coupling parameters module.

This module provides parameters for coupling from controller
to local subsystems in ALADIN.

## Classes

### ControllerToLocalCouplingParameters

> This class is a part of the controller mapping between controller and local subsystem.

> It handles the communicated data that has an assignment to i <-> j pairs.

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize controller to local coupling parameters.


    **Args:**
    > id: Identifier of the local subsystem j to which subsystem i is coupled.  

??? abstract "get_ID(self) → str"
    Return the ID.


    **Returns:**
    > The identifier of the coupled local subsystem.  

??? abstract "update_state(self, other_coupling: [ControllerToLocalCouplingParameters](ControllerToLocalCouplingParameters.md#controllertolocalcouplingparameters)) → None"
    Update the state of this object from another ControllerToLocalCouplingParameters.

    This method is necessary for multiprocessing: when subsystems are executed
    in parallel via Parallel.py using multiprocessing.Pool, each process
    receives a copy of the data. After execution, the original objects must be
    updated with results from the executed copies. This method updates the
    numerical information stored in the class's attributes without changing
    the original memory address location, preserving object identity.

    Attributes are updated in the same order as defined in __init__().


    **Args:**
    > other_coupling: Source instance to copy state from.  

