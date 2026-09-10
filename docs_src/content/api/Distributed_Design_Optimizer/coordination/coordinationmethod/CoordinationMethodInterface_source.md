---
title: CoordinationMethodInterface (Source)
---

← Back to [CoordinationMethodInterface documentation](CoordinationMethodInterface.md)

# CoordinationMethodInterface - Source Code

**File:** `Distributed_Design_Optimizer\coordination\coordinationmethod\CoordinationMethodInterface.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Interface module for coordination methods.

This module defines the abstract interface for coordination methods used
in distributed multidisciplinary design optimization.
"""

from typing import List, Type
from abc import abstractmethod, ABC
from Distributed_Design_Optimizer.coordination.innerloop_iterationscheme import IterationSchemeInterface
from Distributed_Design_Optimizer.subsystem.optimization import AnalysisInterface, OptimizationInterface
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalObjectiveInterface, LocalConstraintsInterface
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis, ControllerSubSystemBasis, SubSystemInterface
from Distributed_Design_Optimizer.middlelevel import MiddleLevelDataStorageInterface
from Distributed_Design_Optimizer.coordination.convergence import (ConvergenceIndicator_Innerloop_Interface,
                                                                   ConvergenceIndicator_Outerloop_Interface)


class CoordinationMethodInterface(ABC):
    """Abstract interface for coordination methods in distributed optimization.

    Defines the contract for creating subsystems and middle levels used in
    multi-level coordination strategies. Implementations provide specific
    coordination algorithms like Augmented Lagrangian Coordination (ALC).
    """

    @abstractmethod
    def validate_inputs(self) -> None:
        """Validate the inputs provided to the coordination method.
        
        This method must be implemented by all coordination methods to validate
        their inputs, particularly the iteration scheme. It should raise a
        ValueError if the inputs are invalid and print a warning if the inputs
        are valid but not recommended.
        
        Raises:
            ValueError: If any input is invalid or incompatible with this
                coordination method.
        """
    
    @abstractmethod
    def get_Convergence_Indicator_Innerloop(self) -> ConvergenceIndicator_Innerloop_Interface:
        """Get the inner loop convergence indicator factory.

        Returns:
            ConvergenceIndicator_Innerloop_Interface: The convergence indicator for inner loop.
        """
    
    @abstractmethod
    def get_Convergence_Indicator_Outerloop(self) -> ConvergenceIndicator_Outerloop_Interface:
        """Get the outer loop convergence indicator factory.

        Returns:
            ConvergenceIndicator_Outerloop_Interface: The convergence indicator for outer loop.
        """
    
    @abstractmethod
    def createSubSystems(self,
                         id_list: List[str],
                         level_list: List[int],
                         neighborid_list: List[List[str]],
                         analysis_list: List[AnalysisInterface],
                         localobjective_list: List[LocalObjectiveInterface],
                         localconstraints_list: List[LocalConstraintsInterface],
                         optimization_list: List[OptimizationInterface]) -> List[LocalSubSystemBasis]:
        """Create subsystems for this coordination method.

        Args:
            id_list: List of unique identifiers for each subsystem.
            level_list: List of hierarchy levels for each subsystem.
            neighborid_list: List of neighbor ID lists for each subsystem.
            analysis_list: List of analysis interfaces for each subsystem.
            localobjective_list: List of local objective interfaces for each subsystem.
            localconstraints_list: List of local constraints interfaces for each subsystem.
            optimization_list: List of optimization interfaces for each subsystem.

        Returns:
            List of created subsystem interfaces.
        """
    
    @abstractmethod
    def createControllerSubSystem(self, subsystemsIn: List[LocalSubSystemBasis]) -> ControllerSubSystemBasis | None:
        """Create the controller subsystem for this coordination method.

        Args:
            subsystemsIn: List of local subsystems to coordinate.

        Returns:
            The controller subsystem interface, or None if no controller is needed.
        """
    
    @abstractmethod
    def createMiddleLevel(self, idparent: str, idchild: str, multiprocessing_lock: object = None) -> MiddleLevelDataStorageInterface:
        """Create a middle level data storage between parent and child subsystems.

        Args:
            idparent: Identifier of the parent subsystem.
            idchild: Identifier of the child subsystem.
            multiprocessing_lock: Lock object for thread-safe operations.

        Returns:
            The middle level data storage interface.
        """
    
    @abstractmethod
    def createControllerMiddleLevel(self, idparent: str, idchild: str, local_neighbors_list: List[str], multiprocessing_lock: object = None) -> MiddleLevelDataStorageInterface | None:
        """Create middle level between controller "C" and local subsystem, if controller exists.

        Args:
            idparent: Identifier of the parent (controller) subsystem.
            idchild: Identifier of the child (local) subsystem.
            local_neighbors_list: List of neighbor subsystem IDs for the local subsystem.
            multiprocessing_lock: Lock object for thread-safe operations.

        Returns:
            The controller middle level data storage interface, or None if no controller is needed.
        """
    
    @abstractmethod
    def get_IterationScheme(self) -> IterationSchemeInterface:
        """Get the iteration scheme.

        Returns:
            The iteration scheme instance.
        """
    
    @abstractmethod
    def get_AllowedIterationSchemes(self) -> List[Type[IterationSchemeInterface]]:
        """Get the list of iteration scheme types allowed for this coordination method.

        Returns:
            List of iteration scheme class types that are compatible with this
            coordination method.
        """
    
    @abstractmethod
    def get_UnrecommendedIterationSchemes(self) -> List[Type[IterationSchemeInterface]]:
        """Get the list of unrecommended iteration scheme types for this coordination method.
        
        These schemes are allowed but may cause issues like oscillations near the optimum
        due to outdated coupling information.

        Returns:
            List of iteration scheme class types that are unrecommended.
        """
    
    @abstractmethod
    def get_RecommendedIterationSchemes(self) -> List[Type[IterationSchemeInterface]]:
        """Get the list of recommended iteration scheme types for this coordination method.

        Returns:
            List of iteration scheme class types that are recommended for best convergence.
        """

    @abstractmethod
    def centralized_prepare_updateCouplingParameters(self, subsystemsIn: List[SubSystemInterface]) -> None:
        """Prepare centralized update of coupling parameters for all subsystems.

        Performs type-specific centralized operations on coupling parameters.
        This is called after inner loop completion and before decentralized
        coupling parameter updates.

        Args:
            subsystemsIn: List of subsystems to prepare coupling parameters for.
        """
        
    @abstractmethod
    def print_startup_summary(self) -> None:
        """Print the coordination method configuration at startup."""
    
    @abstractmethod
    def print_termination_summary(self) -> None:
        """Print the coordination method configuration at the end."""
        
    @abstractmethod
    def print_beginning_of_centralized_prepare_updateCouplingParameters(self) -> None:
        """Print a banner before the centralized coupling parameter preparation step."""
        

```
