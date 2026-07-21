---
title: Local_ConvergenceIndicator_Innerloop_Interface
---

← Back to [convergence](index.md)

# Local_ConvergenceIndicator_Innerloop_Interface

**Source:** [Distributed_Design_Optimizer\coordination\convergence\Local_ConvergenceIndicator_Innerloop_Interface.py](Local_ConvergenceIndicator_Innerloop_Interface_source.md)

Interface module for local inner loop convergence indicators.

This module defines the abstract interface for local inner loop convergence
indicators that are evaluated within each subsystem.

## Classes

### Local_ConvergenceIndicator_Innerloop_Interface

> **Inherits from:** `ABC`

> Abstract interface for local inner loop convergence indicators.

> This interface defines the contract for evaluating inner loop convergence
> at the subsystem level. Each subsystem has its own local convergence indicator
> that checks if the local optimization has stabilized.

#### Methods

??? abstract "evaluate(self, subsystem: [SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)) → bool"
    Evaluate if local inner loop convergence criteria is met.

    The convergence indicator retrieves the data it needs from the subsystem.
    This allows different convergence criteria to access different data
    (e.g., total objective, primal/dual residuals, etc.).


    **Args:**
    > subsystem: The subsystem to evaluate convergence for.  


    **Returns:**
    > bool: True if convergence condition is met, False otherwise.  

??? abstract "update_state(self, other: [Local_ConvergenceIndicator_Innerloop_Interface](Local_ConvergenceIndicator_Innerloop_Interface.md#local_convergenceindicator_innerloop_interface)) → None"
    Update the state of this convergence indicator with the state of another.

    This operation preserves the memory address of the object's attributes
    and only updates the value(s). This method is necessary for multiprocessing,
    where executed subsystems need to transfer their state back to the original objects.


    **Args:**
    > other: The convergence indicator to copy state from.  

