---
title: AnalysisInterface (Source)
---

← Back to [AnalysisInterface documentation](AnalysisInterface.md)

# AnalysisInterface - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\optimization\AnalysisInterface.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Analysis interface module.

This module defines the abstract interface for subsystem analysis components.
"""

from abc import ABC, abstractmethod
from typing import List
from Distributed_Design_Optimizer.subsystem import SubSystemInterface


class AnalysisInterface(ABC):
    """Interface prescribing the methods which an analysis code object needs to implement."""

    @abstractmethod
    def evaluateLocalResponses(self, subsystem: SubSystemInterface) -> None:
        """Evaluate the responses of a subsystem.

        Args:
            subsystem: The subsystem interface for which responses are
                evaluated.
        """

    @abstractmethod
    def mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: SubSystemInterface) -> None:
        """Map the physical responses and design variables onto the neighboring subsystems.

        Args:
            subsystem: The subsystem interface for which responses and design
                variables are mapped.
        """

    @abstractmethod
    def mapLocalResponsesDesignVariables_to_CouplingParameters_Jacobians(self, subsystem: SubSystemInterface) -> None:
        """Map the Jacobians of the mapped responses.

        Args:
            subsystem: The subsystem interface for which the Jacobians are
                mapped.
        """

    @abstractmethod
    def mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian(self, subsystem: SubSystemInterface) -> List[List[List[List[float | None]]]] | None:
        """Map the Hessians of the mapped responses, if known a priori.

        Args:
            subsystem: The subsystem interface for which the Hessians are
                mapped.

        Returns:
            Nested list indexed by local-to-local coupling, then by mapped
            response component, then the 2D Hessian (n_design x n_design).
            None entries indicate values not provided (BFGS approximation used).
            Return None if no Hessians are provided at all.
        """

```
