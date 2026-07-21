---
title: InputFileBasis (Source)
---

← Back to [InputFileBasis documentation](InputFileBasis.md)

# InputFileBasis - Source Code

**File:** `Distributed_Design_Optimizer\coordination\InputFileBasis.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Basis implementation of the InputFile interface for coordination setup."""

import os
import inspect
from typing import List
from Distributed_Design_Optimizer.coordination import InputFileInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.coordination.coordinationmethod import CoordinationMethodInterface
from Distributed_Design_Optimizer.coordination.innerloop_iterationscheme import IterationSchemeInterface
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print


class InputFileBasis(InputFileInterface):
    """Base class providing the standard InputFile configuration for coordination."""

    _DDO_PRINT_LABEL_WIDTH: int = 24

    def __init__(self) -> None:
        """Initialize the input file basis with default None values."""
        self._subsystems: List[LocalSubSystemBasis] | None = None
        self._coordinationmethod: CoordinationMethodInterface | None = None
        self._iterationscheme: IterationSchemeInterface | None = None
        self._name: str | None = None
                
    def get_Subsystems(self) -> List[LocalSubSystemBasis]:
        """Return the list of local subsystems.

        Returns:
            The list of local subsystem basis instances.
        """
        return self._subsystems

    def get_CoordinationMethod(self) -> CoordinationMethodInterface:
        """Return the coordination method.

        Returns:
            The coordination method interface instance.
        """
        return self._coordinationmethod

    def get_IterationScheme(self) -> IterationSchemeInterface:
        """Return the iteration scheme.

        Returns:
            The iteration scheme interface instance.
        """
        return self._iterationscheme
    
    def get_Name(self) -> str:
        """Return the name of the input file configuration.

        Returns:
            The name identifier string.
        """
        return self._name

    def get_HistoryFolderPath(self) -> str:
        """Return the folder path where history .dill files are saved.

        The path is derived from the source-file location of the concrete
        InputFile subclass (``type(self)``), which resides in the use-case
        folder under userfiles/<usecasename>/. This anchors the historyfiles
        folder to the use-case rather than the current working directory,
        independent of where the use-case's main.py is launched from.

        Returns:
            The absolute path to the use-case's historyfiles folder.
        """
        usecase_dir: str = os.path.dirname(os.path.abspath(inspect.getfile(type(self))))
        return os.path.join(usecase_dir, "historyfiles")

    def print_startup_summary(self) -> None:
        """Print the input file configuration summary."""
        ddo_print(f"{'Use-case name:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self.get_Name()}")
        ddo_print(f"{'Coordination Method:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {type(self.get_CoordinationMethod()).__name__}")

```
