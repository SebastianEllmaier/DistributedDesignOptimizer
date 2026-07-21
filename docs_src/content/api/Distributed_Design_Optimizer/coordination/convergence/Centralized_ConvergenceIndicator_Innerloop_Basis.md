---
title: Centralized_ConvergenceIndicator_Innerloop_Basis
---

← Back to [convergence](index.md)

# Centralized_ConvergenceIndicator_Innerloop_Basis

**Source:** [Distributed_Design_Optimizer\coordination\convergence\Centralized_ConvergenceIndicator_Innerloop_Basis.py](Centralized_ConvergenceIndicator_Innerloop_Basis_source.md)

Base implementation for centralized inner loop convergence indicators.

## Classes

### Centralized_ConvergenceIndicator_Innerloop_Basis

> **Inherits from:** [Centralized_ConvergenceIndicator_Innerloop_Interface](Centralized_ConvergenceIndicator_Innerloop_Interface.md#centralized_convergenceindicator_innerloop_interface)

> Base class for centralized inner loop convergence indicators.

> Provides default storage and accessor for the inner loop convergence flag.

#### Methods

??? abstract "__init__(self) → None"
    Initialize with convergence flag set to False.

??? abstract "get_ConvInnerLoop(self) → bool"
    Return the current inner loop convergence flag.


    **Returns:**
    > bool: True if inner loop has converged, False otherwise.  

??? abstract "print_convergence_result(self) → None"
    Print the current innerloop convergence state.

??? abstract "update_state(self, other: [Centralized_ConvergenceIndicator_Innerloop_Basis](Centralized_ConvergenceIndicator_Innerloop_Basis.md#centralized_convergenceindicator_innerloop_basis)) → None"
    Update the state of this instance with values from another instance.


    **Args:**
    > other: The source instance containing updated values.  

