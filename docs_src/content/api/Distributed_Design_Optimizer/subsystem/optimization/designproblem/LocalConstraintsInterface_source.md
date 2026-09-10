---
title: LocalConstraintsInterface (Source)
---

← Back to [LocalConstraintsInterface documentation](LocalConstraintsInterface.md)

# LocalConstraintsInterface - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\optimization\designproblem\LocalConstraintsInterface.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Local constraints interface module.

This module defines the abstract interface for local subsystem constraints.
"""

from abc import ABC, abstractmethod
from Distributed_Design_Optimizer.subsystem import SubSystemInterface


class LocalConstraintsInterface(ABC):
    """Interface that should be implemented by any local constraint class formulation."""

    @abstractmethod
    def evaluateEqualityLocalConstraints(self, subsystem: SubSystemInterface) -> None:
        """Evaluate the equality local constraints.

        Args:
            subsystem: The subsystem interface for which equality constraints
                are evaluated.
        """

    @abstractmethod
    def evaluateInEqualityLocalConstraints(self, subsystem: SubSystemInterface) -> None:
        """Evaluate the inequality local constraints.

        Args:
            subsystem: The subsystem interface for which inequality constraints
                are evaluated.
        """

    @abstractmethod
    def evaluate_Jacobian_EqualityLocalConstraints(self, subsystem: SubSystemInterface) -> None:
        """Evaluate the Jacobian of the local equality constraints that are known to be computed.

        Args:
            subsystem: The subsystem interface for which the Jacobian is
                evaluated.
        """

    @abstractmethod
    def evaluate_Jacobian_InEqualityLocalConstraints(self, subsystem: SubSystemInterface) -> None:
        """Evaluate the Jacobian of the local inequality constraints that are known to be computed.

        Args:
            subsystem: The subsystem interface for which the Jacobian is
                evaluated.
        """

    @abstractmethod
    def evaluate_Hessians_EqualityLocalConstraints(self, subsystem: SubSystemInterface) -> None:
        """Evaluate the Hessians of the local equality constraints that are known to be computed.

        Args:
            subsystem: The subsystem interface for which the Hessians are
                evaluated.
        """

    @abstractmethod
    def evaluate_Hessians_InEqualityLocalConstraints(self, subsystem: SubSystemInterface) -> None:
        """Evaluate the Hessians of the local inequality constraints that are known to be computed.

        Args:
            subsystem: The subsystem interface for which the Hessians are
                evaluated.
        """


```
