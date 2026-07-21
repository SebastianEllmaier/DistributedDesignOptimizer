---
title: ConvergenceIndicator_Innerloop_DeWit
---

← Back to [DeWit](index.md)

# ConvergenceIndicator_Innerloop_DeWit

**Source:** [Distributed_Design_Optimizer\coordination\convergence\DeWit\ConvergenceIndicator_Innerloop_DeWit.py](ConvergenceIndicator_Innerloop_DeWit_source.md)

DeWit inner loop convergence indicator factory.

This module provides the DeWit factory for inner loop convergence indicators
based on the relative change of the total objective function between iterations.

Convergence criterion: |f_new - f_old| / (1 + |f_new|) <= tolerance

## Classes

### ConvergenceIndicator_Innerloop_DeWit

> **Inherits from:** [ConvergenceIndicator_Innerloop_Interface](../ConvergenceIndicator_Innerloop_Interface.md#convergenceindicator_innerloop_interface)

> Inner loop convergence indicator factory - DeWit.

> This class creates local and centralized convergence indicators
> based on the relative change of the total objective function.

> Used in InputFile:
> ALC(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1e-5), ...)

#### Methods

??? abstract "__init__(self, tolerancetotalobjective: float) → None"
    Initialize the convergence indicator factory.


    **Args:**
    > tolerancetotalobjective: Tolerance for relative change in total objective.  

??? abstract "validate_inputs(self) → None"
    Validate the inputs/hyperparameters.


    **Raises:**
    > ValueError: If tolerancetotalobjective is not positive.  

??? abstract "createLocalConvergenceIndicator(self) → [Local_ConvergenceIndicator_Innerloop_DeWit](Local_ConvergenceIndicator_Innerloop_DeWit.md#local_convergenceindicator_innerloop_dewit)"
    Create a local convergence indicator for a subsystem.

    Called in ALC.createSubSystems() for each subsystem.


    **Returns:**
    > Local_ConvergenceIndicator_Innerloop_DeWit: A local convergence indicator instance.  

??? abstract "createCentralizedConvergenceIndicator(self) → [Centralized_ConvergenceIndicator_Innerloop_DeWit](Centralized_ConvergenceIndicator_Innerloop_DeWit.md#centralized_convergenceindicator_innerloop_dewit)"
    Create a centralized convergence indicator for the coordinator.

    Called in Coordinator.__init__().


    **Returns:**
    > Centralized_ConvergenceIndicator_Innerloop_DeWit: A centralized convergence indicator instance.  

??? abstract "get_ToleranceTotalObjective(self) → float"
    Get the tolerance for the total objective convergence.


    **Returns:**
    > The total objective tolerance threshold value.  

??? abstract "print_startup_summary(self) → None"
    Print the total objective tolerance used for inner loop convergence.

??? abstract "print_termination_summary(self) → None"
    Print the total objective tolerance used for inner loop convergence.

