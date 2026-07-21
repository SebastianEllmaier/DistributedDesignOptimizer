---
title: Local_ConvergenceIndicator_Outerloop_AlwaysConverged
---

← Back to [AlwaysConverged](index.md)

# Local_ConvergenceIndicator_Outerloop_AlwaysConverged

**Source:** [Distributed_Design_Optimizer\coordination\convergence\AlwaysConverged\Local_ConvergenceIndicator_Outerloop_AlwaysConverged.py](Local_ConvergenceIndicator_Outerloop_AlwaysConverged_source.md)

AlwaysConverged local outer loop convergence indicator for controller subsystems.

This module provides a local outer loop convergence indicator whose evaluate() method
always returns True. Used for controller subsystems (e.g., in ALADIN)
where convergence is determined entirely by the local subsystems.

## Classes

### Local_ConvergenceIndicator_Outerloop_AlwaysConverged

> **Inherits from:** [Local_ConvergenceIndicator_Outerloop_Interface](../Local_ConvergenceIndicator_Outerloop_Interface.md#local_convergenceindicator_outerloop_interface)

> Local outer loop convergence indicator that always returns True.

> Used for controller subsystems where outer loop convergence is not evaluated.

#### Methods

??? abstract "evaluate(self, subsystem: [SubSystemInterface](../../../subsystem/SubSystemInterface.md#subsysteminterface)) → bool"
    Always returns True.


    **Args:**
    > subsystem: The subsystem to evaluate convergence for (unused).  


    **Returns:**
    > bool: Always True.  

??? abstract "update_state(self, other: [Local_ConvergenceIndicator_Outerloop_AlwaysConverged](Local_ConvergenceIndicator_Outerloop_AlwaysConverged.md#local_convergenceindicator_outerloop_alwaysconverged)) → None"
    No state to update.


    **Args:**
    > other: The convergence indicator to copy state from (unused).  

