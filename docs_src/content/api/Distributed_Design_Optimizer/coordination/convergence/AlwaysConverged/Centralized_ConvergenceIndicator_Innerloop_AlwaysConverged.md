---
title: Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged
---

← Back to [AlwaysConverged](index.md)

# Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged

**Source:** [Distributed_Design_Optimizer\coordination\convergence\AlwaysConverged\Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged.py](Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged_source.md)

AlwaysConverged centralized inner loop convergence indicator for controller subsystems.

This module provides a centralized inner loop convergence indicator whose evaluate()
method always sets convergence to True. Used for controller subsystems (e.g., in ALADIN)
where convergence is determined entirely by the local subsystems.

## Classes

### Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged

> **Inherits from:** [Centralized_ConvergenceIndicator_Innerloop_Basis](../Centralized_ConvergenceIndicator_Innerloop_Basis.md#centralized_convergenceindicator_innerloop_basis)

> Centralized inner loop convergence indicator that always returns True.

> Used when the centralized convergence check should always pass.

#### Methods

??? abstract "evaluate(self, subsystems: List[[SubSystemInterface](../../../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Set inner loop convergence to True unconditionally.


    **Args:**
    > subsystems: List of subsystems (unused).  

??? abstract "print_beginning_of_centralized_convergenceindicator_innerloop_evaluation(self) → None"
    Print a banner indicating that inner loop convergence is always True.

??? abstract "print_end_of_centralized_convergenceindicator_innerloop_evaluation(self, subsystems: List[[SubSystemInterface](../../../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Print the overall inner loop convergence result (always True).


    **Args:**
    > subsystems: List of all subsystems (unused since convergence is always True).  

??? abstract "update_state(self, other: [Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged](Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged.md#centralized_convergenceindicator_innerloop_alwaysconverged)) → None"
    Update the state of this instance with values from another instance.


    **Args:**
    > other: The source instance containing updated values.  

