---
title: LocalToController_CouplingParametersBasis (Source)
---

← Back to [LocalToController_CouplingParametersBasis documentation](LocalToController_CouplingParametersBasis.md)

# LocalToController_CouplingParametersBasis - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\couplingparameters\LocalToController_CouplingParametersBasis.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Local to controller coupling parameters basis module.

This module provides the base class for local subsystem-level coupling
parameters, which are determined for the controller, in hierarchical 
distributed optimization.
"""

from Distributed_Design_Optimizer.subsystem.couplingparameters import CouplingParametersBasis


class LocalToController_CouplingParametersBasis(CouplingParametersBasis):
    """Base class for local subsystem-level coupling parameters determined for the controller.

    Holds the coupling parameters between a single local subsystem and a
    controller. The local subsystem exchanges local coupling information
    (local to controller). Subclasses add algorithm-specific attributes
    (e.g., ALADIN auxiliary variables and Jacobians).
    """

    def __init__(self) -> None:
        """Initialize local-to-controller coupling parameters.

        Since this coupling parameter is stored in the local subsystem and
        with respect to the controller, the ID of this coupling parameter is "C".
        """
        super().__init__(id="C")
        
    def update_state(self, other_coupling: 'LocalToController_CouplingParametersBasis') -> None:
        """Update the state of this LocalToController_CouplingParametersBasis with values from another instance.

        This method is necessary for multiprocessing. When subsystems are executed in parallel
        using multiprocessing.Pool, they are serialized and deserialized, creating new objects
        in separate memory spaces. After parallel execution completes, this method updates
        the original object's attribute values while preserving their memory addresses.

        Note: This base class does not define any local attributes. Subclasses that add
        algorithm-specific attributes (e.g., auxiliary variables, jacobians) must override
        this method to update those attributes while calling super().update_state().

        Args:
            other_coupling: The source LocalToController_CouplingParametersBasis containing updated values
                from parallel execution.
        """
        # Call the base class update_state to handle inherited attributes (_id from CouplingParametersBasis)
        super().update_state(other_coupling=other_coupling)
```
