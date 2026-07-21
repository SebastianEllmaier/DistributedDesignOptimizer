---
title: ConvergenceIndicator_Innerloop_AlwaysConverged
---

← Back to [AlwaysConverged](index.md)

# ConvergenceIndicator_Innerloop_AlwaysConverged

**Source:** [Distributed_Design_Optimizer\coordination\convergence\AlwaysConverged\ConvergenceIndicator_Innerloop_AlwaysConverged.py](ConvergenceIndicator_Innerloop_AlwaysConverged_source.md)

AlwaysConverged inner loop convergence indicator factory for controller subsystems.

This module provides the factory for inner loop convergence indicators whose
evaluate() method always returns True. Used for controller subsystems (e.g., in ALADIN)
where convergence is determined entirely by the local subsystems.

## Classes

### ConvergenceIndicator_Innerloop_AlwaysConverged

> **Inherits from:** [ConvergenceIndicator_Innerloop_Interface](../ConvergenceIndicator_Innerloop_Interface.md#convergenceindicator_innerloop_interface)

> Inner loop convergence indicator factory that always reports convergence.

> Used for controller subsystems where the controller does not participate
> in inner loop convergence decisions.

#### Methods

??? abstract "createLocalConvergenceIndicator(self) → [Local_ConvergenceIndicator_Innerloop_AlwaysConverged](Local_ConvergenceIndicator_Innerloop_AlwaysConverged.md#local_convergenceindicator_innerloop_alwaysconverged)"
    Create a local convergence indicator that always returns True.


    **Returns:**
    > Local_ConvergenceIndicator_Innerloop_AlwaysConverged: A local convergence indicator instance.  

??? abstract "createCentralizedConvergenceIndicator(self) → [Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged](Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged.md#centralized_convergenceindicator_innerloop_alwaysconverged)"
    Create a centralized convergence indicator that always returns True.


    **Returns:**
    > Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged: A centralized convergence indicator instance.  

??? abstract "validate_inputs(self) → None"
    No inputs to validate.

??? abstract "print_startup_summary(self) → None"
    Nothing to print.

??? abstract "print_termination_summary(self) → None"
    Nothing to print.

