---
title: ConvergenceIndicator_Outerloop_DeWit
---

← Back to [DeWit](index.md)

# ConvergenceIndicator_Outerloop_DeWit

**Source:** [Distributed_Design_Optimizer\coordination\convergence\DeWit\ConvergenceIndicator_Outerloop_DeWit.py](ConvergenceIndicator_Outerloop_DeWit_source.md)

DeWit outer loop convergence indicator factory.

This module implements the DeWit convergence criterion factory for the outer loop,
which creates local and centralized convergence indicators that check if all
inconsistencies and coupling parameter changes are within tolerance.

## Classes

### ConvergenceIndicator_Outerloop_DeWit

> **Inherits from:** [ConvergenceIndicator_Outerloop_Interface](../ConvergenceIndicator_Outerloop_Interface.md#convergenceindicator_outerloop_interface)

> DeWit outer loop convergence indicator factory.

> Creates local and centralized convergence indicators that check if all
> inconsistencies and coupling parameter changes are within tolerance.


> **Attributes:**
> > _toleranceconsistency: Tolerance for consistency constraints and coupling changes.

#### Methods

??? abstract "__init__(self, toleranceconsistency: float) → None"
    Initialize the DeWit outer loop convergence indicator.


    **Args:**
    > toleranceconsistency: Tolerance for consistency constraints (typical value: 1E-4).  

??? abstract "validate_inputs(self) → None"
    Validate the inputs provided to the convergence indicator.


    **Raises:**
    > ValueError: If any parameter is outside the allowed range.  

??? abstract "createLocalConvergenceIndicator(self) → [Local_ConvergenceIndicator_Outerloop_DeWit](Local_ConvergenceIndicator_Outerloop_DeWit.md#local_convergenceindicator_outerloop_dewit)"
    Create a local convergence indicator for subsystem-level evaluation.


    **Returns:**
    > Local_ConvergenceIndicator_Outerloop_DeWit: A new local convergence indicator instance.  

??? abstract "createCentralizedConvergenceIndicator(self) → [Centralized_ConvergenceIndicator_Outerloop_DeWit](Centralized_ConvergenceIndicator_Outerloop_DeWit.md#centralized_convergenceindicator_outerloop_dewit)"
    Create a centralized convergence indicator for coordinator-level evaluation.


    **Returns:**
    > Centralized_ConvergenceIndicator_Outerloop_DeWit: A new centralized convergence indicator instance.  

??? abstract "get_ToleranceConsistency(self) → float"
    Get the tolerance for consistency convergence.


    **Returns:**
    > The consistency tolerance threshold value.  

??? abstract "print_startup_summary(self) → None"
    Print the consistency tolerance used for outer loop convergence.

??? abstract "print_termination_summary(self) → None"
    Print the consistency tolerance used for outer loop convergence.

