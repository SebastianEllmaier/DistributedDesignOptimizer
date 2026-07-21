---
title: ConvergenceIndicator_Innerloop_Interface
---

← Back to [convergence](index.md)

# ConvergenceIndicator_Innerloop_Interface

**Source:** [Distributed_Design_Optimizer\coordination\convergence\ConvergenceIndicator_Innerloop_Interface.py](ConvergenceIndicator_Innerloop_Interface_source.md)

Interface module for inner loop convergence indicators.

This module defines the abstract interface for inner loop convergence indicators
used in distributed optimization coordination.

## Classes

### ConvergenceIndicator_Innerloop_Interface

> **Inherits from:** `ABC`

> Abstract interface for inner loop convergence indicators.

> This interface defines the contract for creating local and centralized
> convergence indicators for the inner loop of distributed optimization.

> The inner loop convergence typically checks if the total objective function
> has stabilized (small relative change between iterations).

#### Methods

??? abstract "createLocalConvergenceIndicator(self) → [Local_ConvergenceIndicator_Innerloop_Interface](Local_ConvergenceIndicator_Innerloop_Interface.md#local_convergenceindicator_innerloop_interface)"
    Create a local convergence indicator for a subsystem.


    **Returns:**
    > Local_ConvergenceIndicator_Innerloop_Interface: A local convergence indicator instance.  

??? abstract "createCentralizedConvergenceIndicator(self) → [Centralized_ConvergenceIndicator_Innerloop_Interface](Centralized_ConvergenceIndicator_Innerloop_Interface.md#centralized_convergenceindicator_innerloop_interface)"
    Create a centralized convergence indicator for the coordinator.


    **Returns:**
    > Centralized_ConvergenceIndicator_Innerloop_Interface: A centralized convergence indicator instance.  

??? abstract "validate_inputs(self) → None"
    Validate the inputs/hyperparameters of this convergence indicator.


    **Raises:**
    > ValueError: If any parameter is outside the allowed range.  

??? abstract "print_startup_summary(self) → None"
    Print the inner loop convergence indicator configuration at startup.

??? abstract "print_termination_summary(self) → None"
    Print the inner loop convergence indicator configuration at the end.

