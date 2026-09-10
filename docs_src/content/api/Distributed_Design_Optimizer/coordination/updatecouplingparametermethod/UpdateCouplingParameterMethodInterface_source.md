---
title: UpdateCouplingParameterMethodInterface (Source)
---

← Back to [UpdateCouplingParameterMethodInterface documentation](UpdateCouplingParameterMethodInterface.md)

# UpdateCouplingParameterMethodInterface - Source Code

**File:** `Distributed_Design_Optimizer\coordination\updatecouplingparametermethod\UpdateCouplingParameterMethodInterface.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Interface for coupling parameter update methods.

This module defines the abstract interface for updating coupling parameters
(Lagrange multipliers and penalty weights) in distributed optimization.
Different update strategies can be implemented by subclassing this interface.
"""

from abc import ABC, abstractmethod


class UpdateCouplingParameterMethodInterface(ABC):
    """Abstract interface for coupling parameter update strategies.

    This interface defines the contract for classes that implement
    update strategies for Lagrange multipliers and penalty weights
    used in augmented Lagrangian coordination methods.

    Subclasses must implement:
        - validate_inputs: Validate hyperparameter values
        - print_startup_summary: Print the configuration at startup
        - print_termination_summary: Print the configuration at the end
        - update_state: Update state from another instance (for multiprocessing)
    """

    @abstractmethod
    def validate_inputs(self) -> None:
        """Validate the hyperparameters of this update method.

        Raises:
            ValueError: If any parameter is outside the allowed range.
        """
    
    @abstractmethod
    def print_startup_summary(self) -> None:
        """Print the coupling parameter update method configuration at startup."""
    
    @abstractmethod
    def print_termination_summary(self) -> None:
        """Print the coupling parameter update method configuration at the end."""
    
    @abstractmethod
    def update_state(self, other: 'UpdateCouplingParameterMethodInterface') -> None:
        """Update the state of this instance with values from another instance.

        This method is necessary for multiprocessing. When subsystems are executed
        in parallel using multiprocessing.Pool, they are serialized and deserialized,
        creating new objects in separate memory spaces. After parallel execution
        completes, this method updates the original object's attribute values.

        Args:
            other: The source instance containing updated values from parallel execution.
        """

```
