---
title: Centralized_ConvergenceIndicator_Outerloop_Basis
---

← Back to [convergence](index.md)

# Centralized_ConvergenceIndicator_Outerloop_Basis

**Source:** [Distributed_Design_Optimizer\coordination\convergence\Centralized_ConvergenceIndicator_Outerloop_Basis.py](Centralized_ConvergenceIndicator_Outerloop_Basis_source.md)

Base implementation for centralized outer loop convergence indicators.

## Classes

### Centralized_ConvergenceIndicator_Outerloop_Basis

> **Inherits from:** [Centralized_ConvergenceIndicator_Outerloop_Interface](Centralized_ConvergenceIndicator_Outerloop_Interface.md#centralized_convergenceindicator_outerloop_interface)

> Base class for centralized outer loop convergence indicators.

> Provides default storage and accessor for the outer loop convergence flag.

#### Methods

??? abstract "__init__(self) → None"
    Initialize with convergence flag set to False.

??? abstract "get_ConvOuterLoop(self) → bool"
    Return the current outer loop convergence flag.


    **Returns:**
    > bool: True if outer loop has converged, False otherwise.  

??? abstract "print_convergence_result(self) → None"
    Print the current outerloop convergence state.

??? abstract "update_state(self, other: [Centralized_ConvergenceIndicator_Outerloop_Basis](Centralized_ConvergenceIndicator_Outerloop_Basis.md#centralized_convergenceindicator_outerloop_basis)) → None"
    Update the state of this instance with values from another instance.


    **Args:**
    > other: The source instance containing updated values.  

