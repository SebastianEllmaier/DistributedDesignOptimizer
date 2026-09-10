---
title: main (Source)
---

← Back to [main documentation](main.md)

# main - Source Code

**File:** `userfiles\Sellar\main.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Entry point for running the Sellar Non-Hierarchic distributed optimization.

This module sets up and executes a distributed design optimization using a
non-hierarchic decomposition with Augmented Lagrangian Coordination for the
Sellar multidisciplinary problem. It initializes subsystems from an input
file and coordinates them.
"""
import sys  # noqa
import os  # noqa
# Add the parent directory of Distributed_Design_Optimizer to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)
import datetime
from typing import List
from Distributed_Design_Optimizer.coordination import InputFileInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.coordination import Coordinator
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print
import traceback

from userfiles.Sellar import InputFile


def main() -> None:
    """Run the distributed optimization for the Sellar problem.

    Initializes the input file configuration, creates subsystems, sets up
    the coordinator, and executes the distributed optimization algorithm.
    Prints the completion timestamp upon success or error details upon failure.

    Raises:
        Exception: Any exception that occurs during optimization is caught
            and printed with a traceback.
    """
    try:
        # Read input and create subsystems
        input_file: InputFileInterface = InputFile()
        subsystems: List[LocalSubSystemBasis] = input_file.get_Subsystems()
        
        # Create the coordinator
        coordinator: Coordinator = Coordinator(subsystems, input_file)
        # run distributed optimization
        coordinator.run()

        ddo_print("Program stopped at" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + " .")

    except Exception as e:
        ddo_print("Program failed, here is what I know:")
        ddo_print(str(e))
        
        traceback.print_exc()
        
if __name__ == "__main__":
    main()

```
