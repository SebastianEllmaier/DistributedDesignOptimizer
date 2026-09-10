---
title: ALC (Source)
---

← Back to [ALC documentation](ALC.md)

# ALC - Source Code

**File:** `Distributed_Design_Optimizer\coordination\coordinationmethod\ALC.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Augmented Lagrangian Coordination (ALC) method module.

This module implements the standard Augmented Lagrangian Coordination
method for distributed multidisciplinary design optimization.
"""

import copy
from typing import List, Type
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print, ddo_print_border
from Distributed_Design_Optimizer.coordination.coordinationmethod import CoordinationMethodBasis
from Distributed_Design_Optimizer.coordination.innerloop_iterationscheme import (IterationSchemeInterface,
                                                                                 Parallel,
                                                                                 ParallelPerLevelIncreasing,
                                                                                 SequentialForward,
                                                                                 SequentialBackward,
                                                                                 ParallelEvenThenOddLevels,
                                                                                 ParallelOddThenEvenLevels
                                                                                 )
from Distributed_Design_Optimizer.coordination.updatecouplingparametermethod import UpdateCouplingParameterMethodInterface
from Distributed_Design_Optimizer.coordination.convergence import (ConvergenceIndicator_Innerloop_Interface,
                                                                   ConvergenceIndicator_Outerloop_Interface
                                                                   )
from Distributed_Design_Optimizer.subsystem.optimization import AnalysisInterface, OptimizationInterface
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalObjectiveInterface, LocalConstraintsInterface
from Distributed_Design_Optimizer.subsystem import SubSystemInterface, LocalSubSystemALC
from Distributed_Design_Optimizer.middlelevel.alc import MiddleLevelDataStorageALC


class ALC(CoordinationMethodBasis):
    """Augmented Lagrangian Coordination (ALC) method implementation.

    This coordination method uses augmented Lagrangian relaxation to coordinate
    subsystems in a distributed optimization problem. It manages penalty weights
    and Lagrangian multipliers to enforce consistency between coupled subsystems.
    """

    def __init__(self,
                 convergence_indicator_innerloop: ConvergenceIndicator_Innerloop_Interface,
                 convergence_indicator_outerloop: ConvergenceIndicator_Outerloop_Interface,
                 updatecouplingparametermethod_outerloop: UpdateCouplingParameterMethodInterface,
                 iterationscheme: IterationSchemeInterface) -> None:
        """Initialize the ALC coordination method.

        Args:
            convergence_indicator_innerloop: Convergence indicator for inner loop.
            convergence_indicator_outerloop: Convergence indicator for outer loop.
            updatecouplingparametermethod_outerloop: Method for updating coupling parameters in outer loop.
            iterationscheme: Iteration scheme for inner loop execution.
        """
        super().__init__()
        
        # Allowed iteration schemes for ALC (no controller required)
        self._allowediterationschemes: List[Type[IterationSchemeInterface]] = [
            Parallel, ParallelPerLevelIncreasing, SequentialForward,
            SequentialBackward, ParallelEvenThenOddLevels, ParallelOddThenEvenLevels
        ]
        
        # Unrecommended schemes that may cause oscillations near the optimum
        self._unrecommendediterationschemes: List[Type[IterationSchemeInterface]] = [
            Parallel, ParallelEvenThenOddLevels, ParallelOddThenEvenLevels
        ]
        
        # Recommended schemes for better convergence behavior
        self._recommendediterationschemes: List[Type[IterationSchemeInterface]] = [
            SequentialForward, SequentialBackward, ParallelPerLevelIncreasing
        ]
        
        # Set inputs
        self._convergence_indicator_innerloop: ConvergenceIndicator_Innerloop_Interface = convergence_indicator_innerloop
        self._convergence_indicator_outerloop: ConvergenceIndicator_Outerloop_Interface = convergence_indicator_outerloop
        self._updatecouplingparametermethod_outerloop: UpdateCouplingParameterMethodInterface = updatecouplingparametermethod_outerloop
        self._iterationscheme: IterationSchemeInterface = iterationscheme
        
        # Validate inputs
        self.validate_inputs()
    
    def validate_inputs(self) -> None:
        """Validate the inputs provided to the ALC coordination method.
        
        Validates that the iteration scheme is compatible with ALC. The
        outer-loop update coupling parameter method and the convergence
        indicators are validated by the subsystems they are handed to
        (see LocalSubSystemALC.validate_inputs).
        
        Raises:
            ValueError: If any parameter is outside the allowed range.
        """
        # ===== Iteration Scheme Validation =====
        if type(self._iterationscheme) not in self._allowediterationschemes:
            raise ValueError(
                f"{DDO_Color}Iteration scheme '{type(self._iterationscheme).__name__}' is not compatible with ALC. "
                f"ALC does not use a controller, so controller-based schemes are not supported. "
                f"Please choose one of the compatible schemes: {[s.__name__ for s in self._allowediterationschemes]}{Reset}"
            )
        elif type(self._iterationscheme) in self._unrecommendediterationschemes:
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: Iteration scheme '{type(self._iterationscheme).__name__}' is not recommended for ALC.")
            ddo_print(f"{type(self).__name__}: It may cause oscillations near the optimum due to outdated coupling information.")
            ddo_print(f"{type(self).__name__}: Recommended schemes for ALC: {[s.__name__ for s in self._recommendediterationschemes]}")
            ddo_print_border()
        
    def createSubSystems(self,
                         id_list: List[str],
                         level_list: List[int],
                         neighborid_list: List[List[str]],
                         analysis_list: List[AnalysisInterface],
                         localobjective_list: List[LocalObjectiveInterface],
                         localconstraints_list: List[LocalConstraintsInterface],
                         optimization_list: List[OptimizationInterface]) -> List[LocalSubSystemALC]:
        """Create subsystems for augmented Lagrangian coordination.

        Args:
            id_list: List of unique identifiers for each subsystem.
            level_list: List of hierarchy levels for each subsystem.
            neighborid_list: List of neighbor subsystem IDs for each subsystem.
            analysis_list: List of analysis objects for each subsystem.
            localobjective_list: List of local objective functions for each subsystem.
            localconstraints_list: List of local constraints for each subsystem.
            optimization_list: List of optimization objects for each subsystem.

        Returns:
            List of initialized LocalSubSystemALC objects.
        """
        if not (len(id_list) == len(level_list) == len(neighborid_list) == len(analysis_list) == len(localobjective_list) == len(localconstraints_list) == len(optimization_list)):
            raise ValueError(f"{DDO_Color}The length of the provided list does not match in ALC.createSubSystems{Reset}")
        
        subsystems = [LocalSubSystemALC(id=id_list[i],
                                        level=level_list[i],
                                        neighborid=neighborid_list[i],
                                        analysis=analysis_list[i],
                                        localobjective=localobjective_list[i],
                                        localconstraints=localconstraints_list[i],
                                        optimization=optimization_list[i],
                                        local_convergenceindicator_innerloop=self._convergence_indicator_innerloop.createLocalConvergenceIndicator(),
                                        local_convergenceindicator_outerloop=self._convergence_indicator_outerloop.createLocalConvergenceIndicator(),
                                        # deepcopy() to strengthen distributed character - only middlelevels are shared recourses between subsystems
                                        updatecouplingparametermethod_outerloop=copy.deepcopy(self._updatecouplingparametermethod_outerloop)
                                        )
                      for i in range(len(id_list))]
            
        return subsystems
    
    def createControllerSubSystem(self, subsystemsIn: List[LocalSubSystemALC]) -> SubSystemInterface | None:
        """Create a controller subsystem for coordinating local subsystems.

        Args:
            subsystemsIn: List of local subsystems to be coordinated.

        Returns:
            None, as ALC operates without a central controller.
        """
        # ALC works without a controller
        subsystemcontroller = None
        
        return subsystemcontroller
    
    def createMiddleLevel(self, idparent: str, idchild: str, multiprocessing_lock: object = None) -> MiddleLevelDataStorageALC:
        """Create a middle level data storage for coupling between subsystems.

        Args:
            idparent: Identifier of the parent subsystem.
            idchild: Identifier of the child subsystem.
            multiprocessing_lock: Optional lock for thread-safe access in multiprocessing.

        Returns:
            MiddleLevelDataStorage instance for managing coupling data.
        """
        return MiddleLevelDataStorageALC(idparent, idchild, multiprocessing_lock)
    
    def createControllerMiddleLevel(self, idparent: str, idchild: str, local_neighbors_list: List[str], multiprocessing_lock: object = None) -> MiddleLevelDataStorageALC | None:
        """Create middle level between controller and local subsystem.

        Args:
            idparent: Identifier of the parent (controller) subsystem.
            idchild: Identifier of the child subsystem.
            local_neighbors_list: List of neighbor IDs for the local subsystem (unused).
            multiprocessing_lock: Optional lock for thread-safe access in multiprocessing.

        Returns:
            None, as ALC operates without a central controller.
        """
        # No controller, hence return None
        return None

    def centralized_prepare_updateCouplingParameters(self, subsystemsIn: List[LocalSubSystemALC]) -> None:
        """Prepare centralized update of coupling parameters for all subsystems.

        For ALC, no centralized operation is required.

        Args:
            subsystemsIn: List of subsystems to prepare coupling parameters for.
        """
        pass

    def print_beginning_of_centralized_prepare_updateCouplingParameters(self) -> None:
        """Nothing to print."""
        # Nothing to print
        pass

```
