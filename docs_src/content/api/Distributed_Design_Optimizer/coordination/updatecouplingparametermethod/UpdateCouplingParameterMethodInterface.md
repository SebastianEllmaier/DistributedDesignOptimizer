---
title: UpdateCouplingParameterMethodInterface
---

← Back to [updatecouplingparametermethod](index.md)

# UpdateCouplingParameterMethodInterface

**Source:** [Distributed_Design_Optimizer\coordination\updatecouplingparametermethod\UpdateCouplingParameterMethodInterface.py](UpdateCouplingParameterMethodInterface_source.md)

Interface for coupling parameter update methods.

This module defines the abstract interface for updating coupling parameters
(Lagrange multipliers and penalty weights) in distributed optimization.
Different update strategies can be implemented by subclassing this interface.

## Classes

### UpdateCouplingParameterMethodInterface

> **Inherits from:** `ABC`

> Abstract interface for coupling parameter update strategies.

> This interface defines the contract for classes that implement
> update strategies for Lagrange multipliers and penalty weights
> used in augmented Lagrangian coordination methods.

> Subclasses must implement:
> - validate_inputs: Validate hyperparameter values
> - print_startup_summary: Print the configuration at startup
> - print_termination_summary: Print the configuration at the end
> - update_state: Update state from another instance (for multiprocessing)

#### Methods

??? abstract "validate_inputs(self) → None"
    Validate the hyperparameters of this update method.


    **Raises:**
    > ValueError: If any parameter is outside the allowed range.  

??? abstract "print_startup_summary(self) → None"
    Print the coupling parameter update method configuration at startup.

??? abstract "print_termination_summary(self) → None"
    Print the coupling parameter update method configuration at the end.

??? abstract "update_state(self, other: [UpdateCouplingParameterMethodInterface](UpdateCouplingParameterMethodInterface.md#updatecouplingparametermethodinterface)) → None"
    Update the state of this instance with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed
    in parallel using multiprocessing.Pool, they are serialized and deserialized,
    creating new objects in separate memory spaces. After parallel execution
    completes, this method updates the original object's attribute values.


    **Args:**
    > other: The source instance containing updated values from parallel execution.  

