---
title: Centralized_ConvergenceIndicator_Innerloop_DeWit
---

← Back to [DeWit](index.md)

# Centralized_ConvergenceIndicator_Innerloop_DeWit

**Source:** [Distributed_Design_Optimizer\coordination\convergence\DeWit\Centralized_ConvergenceIndicator_Innerloop_DeWit.py](Centralized_ConvergenceIndicator_Innerloop_DeWit_source.md)

DeWit centralized inner loop convergence indicator.

Aggregates local inner loop convergence flags from all subsystems.
The coordinator has one instance of this class.

## Classes

### Centralized_ConvergenceIndicator_Innerloop_DeWit

> **Inherits from:** [Centralized_ConvergenceIndicator_Innerloop_Basis](../Centralized_ConvergenceIndicator_Innerloop_Basis.md#centralized_convergenceindicator_innerloop_basis)

> Centralized inner loop convergence indicator - DeWit.

> Aggregates local convergence flags from all subsystems.
> The coordinator has one instance of this class.

#### Methods

??? abstract "evaluate(self, subsystems: List[[SubSystemInterface](../../../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Evaluate centralized inner loop convergence across all subsystems.

    First triggers local convergence evaluation in each subsystem,
    then aggregates the results using logical AND.


    **Args:**
    > subsystems: List of all subsystems to check for convergence.  

??? abstract "print_beginning_of_centralized_convergenceindicator_innerloop_evaluation(self) → None"
    Print a banner before evaluating inner loop convergence via logical AND over all subsystems.

??? abstract "print_end_of_centralized_convergenceindicator_innerloop_evaluation(self, subsystems: List[[SubSystemInterface](../../../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Print per-subsystem inner loop convergence flags and the overall aggregated result.


    **Args:**
    > subsystems: List of all subsystems whose inner loop convergence flags are printed.  

??? abstract "update_state(self, other: [Centralized_ConvergenceIndicator_Innerloop_DeWit](Centralized_ConvergenceIndicator_Innerloop_DeWit.md#centralized_convergenceindicator_innerloop_dewit)) → None"
    Update the state of this instance with values from another instance.


    **Args:**
    > other: The source instance containing updated values.  

