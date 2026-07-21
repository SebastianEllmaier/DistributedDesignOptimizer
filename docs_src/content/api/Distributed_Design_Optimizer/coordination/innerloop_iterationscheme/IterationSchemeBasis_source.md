---
title: IterationSchemeBasis (Source)
---

← Back to [IterationSchemeBasis documentation](IterationSchemeBasis.md)

# IterationSchemeBasis - Source Code

**File:** `Distributed_Design_Optimizer\coordination\innerloop_iterationscheme\IterationSchemeBasis.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Base class module for inner loop iteration schemes.

This module provides the base class with common functionality for iteration
schemes, including the shared run_subsystem helper method.
"""

from Distributed_Design_Optimizer.subsystem import SubSystemInterface
from Distributed_Design_Optimizer.coordination.innerloop_iterationscheme import IterationSchemeInterface


class IterationSchemeBasis(IterationSchemeInterface):
    """Base class for inner loop iteration schemes.

    Provides common functionality shared by all iteration scheme implementations,
    including the run_subsystem helper method for multiprocessing execution.
    Concrete iteration schemes should inherit from this class.
    
    Note: The abstract method run_innerloop_jobs_multiprocessing() is inherited
    from IterationSchemeInterface and must be implemented by concrete subclasses.
    """

    @staticmethod  # implemented as staticmethod, because self is not needed as an input - only operates on the input subsystem
    def run_subsystem(subsystem: SubSystemInterface) -> SubSystemInterface:
        """Execute a single subsystem's inner loop job.
        
        Helper function used by multiprocessing to execute subsystems.
        Defined once here to avoid code duplication across all iteration schemes.

        Args:
            subsystem: The subsystem to execute.

        Returns:
            The executed subsystem with updated state.
        """
        subsystem.run_innerloop_job()
        return subsystem


```
