---
title: Local_ConvergenceIndicator_Innerloop_DeWit
---

← Back to [DeWit](index.md)

# Local_ConvergenceIndicator_Innerloop_DeWit

**Source:** [Distributed_Design_Optimizer\coordination\convergence\DeWit\Local_ConvergenceIndicator_Innerloop_DeWit.py](Local_ConvergenceIndicator_Innerloop_DeWit_source.md)

DeWit local inner loop convergence indicator.

Evaluates inner loop convergence at the subsystem level based on the relative
change of the total objective function between iterations.

Convergence criterion: |f_new - f_old| / (1 + |f_new|) <= tolerance

## Classes

### Local_ConvergenceIndicator_Innerloop_DeWit

> **Inherits from:** [Local_ConvergenceIndicator_Innerloop_Interface](../Local_ConvergenceIndicator_Innerloop_Interface.md#local_convergenceindicator_innerloop_interface)

> Local inner loop convergence indicator - DeWit.

> Evaluates convergence based on relative change of total objective.
> Each subsystem has one instance of this class.

#### Methods

??? abstract "__init__(self, tolerancetotalobjective: float) → None"
    Initialize the local convergence indicator.


    **Args:**
    > tolerancetotalobjective: Tolerance for relative change in total objective.  

??? abstract "evaluate(self, subsystem: [SubSystemInterface](../../../subsystem/SubSystemInterface.md#subsysteminterface)) → bool"
    Evaluate if local inner loop convergence criteria is met.

    Computes: error = |f_new - f_old| / (1 + |f_new|)
    Convergence if error <= tolerance.


    **Args:**
    > subsystem: The subsystem to evaluate convergence for.  


    **Returns:**
    > bool: True if convergence condition is met, False otherwise.  

??? abstract "get_ToleranceTotalObjective(self) → float"
    Get the tolerance for the total objective convergence.


    **Returns:**
    > The total objective tolerance threshold value.  

??? abstract "update_state(self, other: [Local_ConvergenceIndicator_Innerloop_DeWit](Local_ConvergenceIndicator_Innerloop_DeWit.md#local_convergenceindicator_innerloop_dewit)) → None"
    Update the state of this convergence indicator with the state of another.


    **Args:**
    > other: The convergence indicator to copy state from.  

