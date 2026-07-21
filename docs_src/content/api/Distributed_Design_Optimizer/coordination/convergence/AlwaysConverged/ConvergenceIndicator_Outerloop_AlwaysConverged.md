---
title: ConvergenceIndicator_Outerloop_AlwaysConverged
---

← Back to [AlwaysConverged](index.md)

# ConvergenceIndicator_Outerloop_AlwaysConverged

**Source:** [Distributed_Design_Optimizer\coordination\convergence\AlwaysConverged\ConvergenceIndicator_Outerloop_AlwaysConverged.py](ConvergenceIndicator_Outerloop_AlwaysConverged_source.md)

AlwaysConverged outer loop convergence indicator factory for controller subsystems.

This module provides the factory for outer loop convergence indicators whose
evaluate() method always returns True. Used for controller subsystems (e.g., in ALADIN)
where convergence is determined entirely by the local subsystems.

## Classes

### ConvergenceIndicator_Outerloop_AlwaysConverged

> **Inherits from:** [ConvergenceIndicator_Outerloop_Interface](../ConvergenceIndicator_Outerloop_Interface.md#convergenceindicator_outerloop_interface)

> Outer loop convergence indicator factory that always reports convergence.

> Used for controller subsystems where the controller does not participate
> in outer loop convergence decisions.

#### Methods

??? abstract "createLocalConvergenceIndicator(self) → [Local_ConvergenceIndicator_Outerloop_AlwaysConverged](Local_ConvergenceIndicator_Outerloop_AlwaysConverged.md#local_convergenceindicator_outerloop_alwaysconverged)"
    Create a local convergence indicator that always returns True.


    **Returns:**
    > Local_ConvergenceIndicator_Outerloop_AlwaysConverged: A local convergence indicator instance.  

??? abstract "createCentralizedConvergenceIndicator(self) → [Centralized_ConvergenceIndicator_Outerloop_AlwaysConverged](Centralized_ConvergenceIndicator_Outerloop_AlwaysConverged.md#centralized_convergenceindicator_outerloop_alwaysconverged)"
    Create a centralized convergence indicator that always returns True.


    **Returns:**
    > Centralized_ConvergenceIndicator_Outerloop_AlwaysConverged: A centralized convergence indicator instance.  

??? abstract "validate_inputs(self) → None"
    No inputs to validate.

??? abstract "print_startup_summary(self) → None"
    Nothing to print.

??? abstract "print_termination_summary(self) → None"
    Nothing to print.

