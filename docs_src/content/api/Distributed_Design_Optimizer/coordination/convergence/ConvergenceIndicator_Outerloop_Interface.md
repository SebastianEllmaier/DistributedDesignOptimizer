---
title: ConvergenceIndicator_Outerloop_Interface
---

← Back to [convergence](index.md)

# ConvergenceIndicator_Outerloop_Interface

**Source:** [Distributed_Design_Optimizer\coordination\convergence\ConvergenceIndicator_Outerloop_Interface.py](ConvergenceIndicator_Outerloop_Interface_source.md)

Interface module for outer loop convergence indicator factories.

This module defines the abstract factory interface for creating outer loop
convergence indicators that are used in distributed optimization coordination.

## Classes

### ConvergenceIndicator_Outerloop_Interface

> **Inherits from:** `ABC`

> Abstract factory interface for outer loop convergence indicators.

> This interface defines the contract for creating local and centralized
> convergence indicators for the outer loop. Implementations provide
> specific convergence criteria (e.g., consistency-based, coupling parameter change).

#### Methods

??? abstract "createLocalConvergenceIndicator(self) → [Local_ConvergenceIndicator_Outerloop_Interface](Local_ConvergenceIndicator_Outerloop_Interface.md#local_convergenceindicator_outerloop_interface)"
    Create a local convergence indicator for subsystem-level evaluation.


    **Returns:**
    > Local_ConvergenceIndicator_Outerloop_Interface: A new local convergence indicator instance.  

??? abstract "createCentralizedConvergenceIndicator(self) → [Centralized_ConvergenceIndicator_Outerloop_Interface](Centralized_ConvergenceIndicator_Outerloop_Interface.md#centralized_convergenceindicator_outerloop_interface)"
    Create a centralized convergence indicator for coordinator-level evaluation.


    **Returns:**
    > Centralized_ConvergenceIndicator_Outerloop_Interface: A new centralized convergence indicator instance.  

??? abstract "validate_inputs(self) → None"
    Validate the inputs provided to the convergence indicator.


    **Raises:**
    > ValueError: If any parameter is outside the allowed range.  

??? abstract "print_startup_summary(self) → None"
    Print the outer loop convergence indicator configuration at startup.

??? abstract "print_termination_summary(self) → None"
    Print the outer loop convergence indicator configuration at the end.

