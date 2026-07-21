---
title: Centralized_ConvergenceIndicator_Outerloop_Interface
---

← Back to [convergence](index.md)

# Centralized_ConvergenceIndicator_Outerloop_Interface

**Source:** [Distributed_Design_Optimizer\coordination\convergence\Centralized_ConvergenceIndicator_Outerloop_Interface.py](Centralized_ConvergenceIndicator_Outerloop_Interface_source.md)

Interface module for centralized outer loop convergence indicators.

This module defines the abstract interface for centralized outer loop convergence
indicators that aggregate convergence across all subsystems.

## Classes

### Centralized_ConvergenceIndicator_Outerloop_Interface

> **Inherits from:** `ABC`

> Abstract interface for centralized outer loop convergence indicators.

> This interface defines the contract for evaluating outer loop convergence
> at the coordinator level by aggregating local convergence flags from all subsystems.

#### Methods

??? abstract "get_ConvOuterLoop(self) → bool"
    Return the current outer loop convergence flag.


    **Returns:**
    > bool: True if outer loop has converged, False otherwise.  

??? abstract "evaluate(self, subsystems: List[[SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Evaluate centralized outer loop convergence across all subsystems.

    This method may trigger local convergence evaluation in each subsystem
    if needed, then aggregates the results to determine overall outer loop convergence.


    **Args:**
    > subsystems: List of all subsystems to check for convergence.  

??? abstract "print_beginning_of_centralized_convergenceindicator_outerloop_evaluation(self) → None"
    Print a banner before the centralized outer loop convergence evaluation.

??? abstract "print_end_of_centralized_convergenceindicator_outerloop_evaluation(self, subsystems: List[[SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Print per-subsystem and overall outer loop convergence results.


    **Args:**
    > subsystems: List of all subsystems whose convergence flags are printed.  

??? abstract "print_convergence_result(self) → None"
    Print the current outerloop convergence state.

??? abstract "update_state(self, other: [Centralized_ConvergenceIndicator_Outerloop_Interface](Centralized_ConvergenceIndicator_Outerloop_Interface.md#centralized_convergenceindicator_outerloop_interface)) → None"
    Update the state of this instance with values from another instance.


    **Args:**
    > other: The source instance containing updated values.  

