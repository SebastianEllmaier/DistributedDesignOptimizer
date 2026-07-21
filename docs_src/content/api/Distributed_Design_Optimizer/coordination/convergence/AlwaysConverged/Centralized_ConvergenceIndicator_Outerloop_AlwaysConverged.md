---
title: Centralized_ConvergenceIndicator_Outerloop_AlwaysConverged
---

← Back to [AlwaysConverged](index.md)

# Centralized_ConvergenceIndicator_Outerloop_AlwaysConverged

**Source:** [Distributed_Design_Optimizer\coordination\convergence\AlwaysConverged\Centralized_ConvergenceIndicator_Outerloop_AlwaysConverged.py](Centralized_ConvergenceIndicator_Outerloop_AlwaysConverged_source.md)

AlwaysConverged centralized outer loop convergence indicator for controller subsystems.

This module provides a centralized outer loop convergence indicator whose evaluate()
method always sets convergence to True. Used for controller subsystems (e.g., in ALADIN)
where convergence is determined entirely by the local subsystems.

## Classes

### Centralized_ConvergenceIndicator_Outerloop_AlwaysConverged

> **Inherits from:** [Centralized_ConvergenceIndicator_Outerloop_Basis](../Centralized_ConvergenceIndicator_Outerloop_Basis.md#centralized_convergenceindicator_outerloop_basis)

> Centralized outer loop convergence indicator that always returns True.

> Used when the centralized convergence check should always pass.

#### Methods

??? abstract "evaluate(self, subsystems: List[[SubSystemInterface](../../../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Set outer loop convergence to True unconditionally.


    **Args:**
    > subsystems: List of subsystems (unused).  

??? abstract "print_beginning_of_centralized_convergenceindicator_outerloop_evaluation(self) → None"
    Print a banner indicating that outer loop convergence is always True.

??? abstract "print_end_of_centralized_convergenceindicator_outerloop_evaluation(self, subsystems: List[[SubSystemInterface](../../../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Print the overall outer loop convergence result (always True).


    **Args:**
    > subsystems: List of all subsystems (unused since convergence is always True).  

??? abstract "update_state(self, other: [Centralized_ConvergenceIndicator_Outerloop_AlwaysConverged](Centralized_ConvergenceIndicator_Outerloop_AlwaysConverged.md#centralized_convergenceindicator_outerloop_alwaysconverged)) → None"
    Update the state of this instance with values from another instance.


    **Args:**
    > other: The source instance containing updated values.  

