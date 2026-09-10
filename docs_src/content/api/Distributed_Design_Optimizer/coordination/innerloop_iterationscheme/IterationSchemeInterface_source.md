---
title: IterationSchemeInterface (Source)
---

← Back to [IterationSchemeInterface documentation](IterationSchemeInterface.md)

# IterationSchemeInterface - Source Code

**File:** `Distributed_Design_Optimizer\coordination\innerloop_iterationscheme\IterationSchemeInterface.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Interface module for inner loop iteration schemes.

This module defines the abstract base class for iteration schemes that
control how subsystems are executed during inner loop iterations.
"""

from typing import List, Tuple
from abc import ABC, abstractmethod
from Distributed_Design_Optimizer.subsystem import SubSystemInterface


class IterationSchemeInterface(ABC):
    """Abstract base class for inner loop iteration schemes.

    Defines the interface for different strategies to execute hierarchic
    subsystems during inner loop iterations.
    """

    @abstractmethod
    def run_innerloop_jobs_multiprocessing(self, subsystemsIn: List[SubSystemInterface]) -> Tuple[List[SubSystemInterface], List[int]]:
        """Execute inner loop jobs using multiprocessing.

        Args:
            subsystemsIn: List of subsystems to execute.

        Returns:
            Tuple containing the list of executed subsystems and their indices.
        """
        
    @abstractmethod
    def print_startup_summary(self) -> None:
        """Print the iteration scheme configuration at startup."""
    
    @abstractmethod
    def print_termination_summary(self) -> None:
        """Print the iteration scheme configuration at the end."""
        
    @abstractmethod
    def print_beginning_of_run_innerloop_jobs_multiprocessing(self) -> None:
        """Print a banner before executing inner loop jobs via multiprocessing."""

```
