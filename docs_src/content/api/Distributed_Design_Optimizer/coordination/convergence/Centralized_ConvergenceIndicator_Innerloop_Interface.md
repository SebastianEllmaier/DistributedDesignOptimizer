---
title: Centralized_ConvergenceIndicator_Innerloop_Interface
---

← Back to [convergence](index.md)

# Centralized_ConvergenceIndicator_Innerloop_Interface

**Source:** [Distributed_Design_Optimizer\coordination\convergence\Centralized_ConvergenceIndicator_Innerloop_Interface.py](Centralized_ConvergenceIndicator_Innerloop_Interface_source.md)

Interface module for centralized inner loop convergence indicators.

This module defines the abstract interface for centralized inner loop convergence
indicators that aggregate convergence across all subsystems.

## Classes

### Centralized_ConvergenceIndicator_Innerloop_Interface

> **Inherits from:** `ABC`

> Abstract interface for centralized inner loop convergence indicators.

> This interface defines the contract for evaluating inner loop convergence
> at the coordinator level by aggregating local convergence flags from all subsystems.

#### Methods

??? abstract "get_ConvInnerLoop(self) → bool"
    Return the current inner loop convergence flag.


    **Returns:**
    > bool: True if inner loop has converged, False otherwise.  

??? abstract "evaluate(self, subsystems: List[[SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Evaluate centralized inner loop convergence across all subsystems.

    This method first triggers local convergence evaluation in each subsystem,
    then aggregates the results to determine overall inner loop convergence.


    **Args:**
    > subsystems: List of all subsystems to check for convergence.  

??? abstract "print_beginning_of_centralized_convergenceindicator_innerloop_evaluation(self) → None"
    Print a banner before the centralized inner loop convergence evaluation.

??? abstract "print_end_of_centralized_convergenceindicator_innerloop_evaluation(self, subsystems: List[[SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Print per-subsystem and overall inner loop convergence results.


    **Args:**
    > subsystems: List of all subsystems whose convergence flags are printed.  

??? abstract "print_convergence_result(self) → None"
    Print the current innerloop convergence state.

??? abstract "update_state(self, other: [Centralized_ConvergenceIndicator_Innerloop_Interface](Centralized_ConvergenceIndicator_Innerloop_Interface.md#centralized_convergenceindicator_innerloop_interface)) → None"
    Update the state of this instance with values from another instance.


    **Args:**
    > other: The source instance containing updated values.  

