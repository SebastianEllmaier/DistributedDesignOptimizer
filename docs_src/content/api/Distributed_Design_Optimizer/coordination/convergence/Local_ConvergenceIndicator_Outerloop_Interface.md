---
title: Local_ConvergenceIndicator_Outerloop_Interface
---

← Back to [convergence](index.md)

# Local_ConvergenceIndicator_Outerloop_Interface

**Source:** [Distributed_Design_Optimizer\coordination\convergence\Local_ConvergenceIndicator_Outerloop_Interface.py](Local_ConvergenceIndicator_Outerloop_Interface_source.md)

Interface module for local outer loop convergence indicators.

This module defines the abstract interface for local outer loop convergence
indicators that are evaluated within each subsystem.

## Classes

### Local_ConvergenceIndicator_Outerloop_Interface

> **Inherits from:** `ABC`

> Abstract interface for local outer loop convergence indicators.

> This interface defines the contract for evaluating outer loop convergence
> at the subsystem level. Each subsystem has its own local convergence indicator
> that checks if the outer loop criteria (consistency, coupling parameter changes)
> are satisfied.

#### Methods

??? abstract "evaluate(self, subsystem: [SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)) → bool"
    Evaluate if local outer loop convergence criteria is met.

    The convergence indicator retrieves the data it needs from the subsystem.
    This allows different convergence criteria to access different data
    (e.g., inconsistencies, coupling parameters, etc.).


    **Args:**
    > subsystem: The subsystem to evaluate convergence for.  


    **Returns:**
    > bool: True if convergence condition is met, False otherwise.  

??? abstract "update_state(self, other: [Local_ConvergenceIndicator_Outerloop_Interface](Local_ConvergenceIndicator_Outerloop_Interface.md#local_convergenceindicator_outerloop_interface)) → None"
    Update the state of this convergence indicator with the state of another.

    This operation preserves the memory address of the object's attributes
    while updating their values. Required for multiprocessing synchronization.


    **Args:**
    > other: The convergence indicator to copy state from.  

