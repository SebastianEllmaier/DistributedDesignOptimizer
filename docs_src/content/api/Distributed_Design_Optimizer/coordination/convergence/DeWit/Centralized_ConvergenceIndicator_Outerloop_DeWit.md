---
title: Centralized_ConvergenceIndicator_Outerloop_DeWit
---

← Back to [DeWit](index.md)

# Centralized_ConvergenceIndicator_Outerloop_DeWit

**Source:** [Distributed_Design_Optimizer\coordination\convergence\DeWit\Centralized_ConvergenceIndicator_Outerloop_DeWit.py](Centralized_ConvergenceIndicator_Outerloop_DeWit_source.md)

DeWit centralized outer loop convergence indicator.

Aggregates local outer loop convergence flags from all subsystems.
The coordinator has one instance of this class.

## Classes

### Centralized_ConvergenceIndicator_Outerloop_DeWit

> **Inherits from:** [Centralized_ConvergenceIndicator_Outerloop_Basis](../Centralized_ConvergenceIndicator_Outerloop_Basis.md#centralized_convergenceindicator_outerloop_basis)

> Centralized outer loop convergence indicator - DeWit.

> Aggregates local convergence flags from all subsystems.
> The coordinator has one instance of this class.

#### Methods

??? abstract "evaluate(self, subsystems: List[[SubSystemInterface](../../../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Evaluate centralized outer loop convergence across all subsystems.

    First triggers local convergence evaluation in each subsystem,
    then aggregates the results using logical AND.


    **Args:**
    > subsystems: List of all subsystems to check for convergence.  

??? abstract "print_beginning_of_centralized_convergenceindicator_outerloop_evaluation(self) → None"
    Print a banner before evaluating outer loop convergence via logical AND over all subsystems.

??? abstract "print_end_of_centralized_convergenceindicator_outerloop_evaluation(self, subsystems: List[[SubSystemInterface](../../../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Print per-subsystem outer loop convergence flags and the overall aggregated result.


    **Args:**
    > subsystems: List of all subsystems whose outer loop convergence flags are printed.  

??? abstract "update_state(self, other: [Centralized_ConvergenceIndicator_Outerloop_DeWit](Centralized_ConvergenceIndicator_Outerloop_DeWit.md#centralized_convergenceindicator_outerloop_dewit)) → None"
    Update the state of this instance with values from another instance.


    **Args:**
    > other: The source instance containing updated values.  

