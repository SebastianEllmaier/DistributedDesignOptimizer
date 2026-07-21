---
title: JacobianComputer
---

← Back to [postprocess](index.md)

# JacobianComputer

**Source:** [Distributed_Design_Optimizer\postprocess\JacobianComputer.py](JacobianComputer_source.md)

Jacobian computation module.

This module provides functionality for computing Jacobian matrices
in distributed optimization problems.

## Classes

### JacobianComputer

> Computes Jacobian matrices for mapped response variables.

#### Methods

??? abstract "__init__(self)"
    Initialize the JacobianComputer.

??? abstract "execute(self, subsystemin: [SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)) → None"
    Execute Jacobian computation for a subsystem.


    **Args:**
    > subsystemin: The subsystem interface to compute Jacobian for.  

