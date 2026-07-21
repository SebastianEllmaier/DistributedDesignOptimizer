# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Interface module for input file configurations.

This module defines the abstract interface for input files that specify
optimization problem setup, including subsystems, coordination methods,
iteration schemes, and execution parameters.
"""

from abc import ABC, abstractmethod
from typing import List
from Distributed_Design_Optimizer.subsystem import SubSystemInterface
from Distributed_Design_Optimizer.coordination.innerloop_iterationscheme import IterationSchemeInterface
from Distributed_Design_Optimizer.coordination.coordinationmethod import CoordinationMethodInterface


class InputFileInterface(ABC):
    """Abstract interface for input file configurations.

    This interface defines the contract for input files that specify
    optimization problem setup, including subsystems, coordination methods,
    iteration schemes, and execution mode configuration.
    """

    @abstractmethod
    def get_Subsystems(self) -> List[SubSystemInterface]:
        """Get the list of subsystem subsystems for the optimization.

        Returns:
            List[SubSystemInterface]: The list of subsystem subsystems.
        """
    
    @abstractmethod
    def get_CoordinationMethod(self) -> CoordinationMethodInterface:
        """Get the coordination method for this optimization.

        Returns:
            CoordinationMethodInterface: _description_
        """
        
    @abstractmethod
    def get_IterationScheme(self) -> IterationSchemeInterface:
        """Get the iteration scheme for the optimization.

        Returns:
            IterationSchemeInterface: The iteration scheme instance.
        """
        
    @abstractmethod
    def get_Name(self) -> str:
        """Get the name identifier for this input file configuration.

        Returns:
            str: The name of the input file configuration.
        """

    @abstractmethod
    def get_HistoryFolderPath(self) -> str:
        """Get the folder path where history .dill files are saved.

        The path is derived from the location of the concrete InputFile
        subclass (i.e. the use-case folder under userfiles/<usecasename>/),
        so history files are stored alongside the use-case that produced them.

        Returns:
            str: The absolute path to the use-case's historyfiles folder.
        """

    @abstractmethod
    def print_startup_summary(self) -> None:
        """Print the input file configuration summary (use-case name and coordination method)."""
