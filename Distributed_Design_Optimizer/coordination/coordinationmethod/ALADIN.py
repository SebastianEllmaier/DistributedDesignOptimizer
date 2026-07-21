# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""ALADIN coordination method module.

This module implements the Augmented Lagrangian based Alternating Direction
Inexact Newton (ALADIN) coordination method for distributed optimization.
"""

import copy
from typing import List, Dict, Type
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print, ddo_print_border
from Distributed_Design_Optimizer.coordination.coordinationmethod import CoordinationMethodBasis
from Distributed_Design_Optimizer.coordination.innerloop_iterationscheme import (IterationSchemeInterface,
                                                                                 ParallelLocal_SequentialController
                                                                                 )
from Distributed_Design_Optimizer.coordination.updatecouplingparametermethod import UpdateCouplingParameterMethodInterface

from Distributed_Design_Optimizer.coordination.convergence import (ConvergenceIndicator_Innerloop_Interface,
                                                                   ConvergenceIndicator_Outerloop_Interface
                                                                   )
from Distributed_Design_Optimizer.subsystem.optimization import AnalysisInterface, OptimizationInterface, OptimizationController
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalObjectiveInterface, LocalConstraintsInterface
from Distributed_Design_Optimizer.subsystem import SubSystemInterface, LocalSubSystemALADIN, ControllerSubSystemALADIN
from Distributed_Design_Optimizer.middlelevel.aladin import (LocalController_MiddleLevelDataStorageALADIN,
                                                             LocalToLocal_MiddleLevelDataStorageALADIN
                                                             )


class ALADIN(CoordinationMethodBasis):
    """ALADIN coordination method for distributed optimization.

    This coordination method implements the Augmented Lagrangian based
    Alternating Direction Inexact Newton (ALADIN) algorithm. It combines
    decentralized local subproblem solves with a centralized controller
    (quadratic programming) step that uses gradient and Hessian information
    to drive the coupled subsystems towards consensus.
    """

    def __init__(self,
                 convergence_indicator_innerloop: ConvergenceIndicator_Innerloop_Interface,
                 convergence_indicator_outerloop: ConvergenceIndicator_Outerloop_Interface,
                 updatecouplingparametermethod_outerloop: UpdateCouplingParameterMethodInterface,
                 iterationscheme: IterationSchemeInterface) -> None:
        """Initialize the ALADIN coordination method.

        Args:
            convergence_indicator_innerloop: Convergence indicator for inner loop.
            convergence_indicator_outerloop: Convergence indicator for outer loop.
            updatecouplingparametermethod_outerloop: Method for updating coupling parameters in outer loop.
            iterationscheme: Iteration scheme for inner loop execution.
        """
        super().__init__()

        # Only ParallelLocal_SequentialController is compatible with ALADIN
        self._allowediterationschemes: List[Type[IterationSchemeInterface]] = [
            ParallelLocal_SequentialController
        ]
        
        # Empty because only one scheme is allowed - there are no "allowed but not
        # recommended" schemes for ALADIN. All other schemes are incompatible.
        self._unrecommendediterationschemes: List[Type[IterationSchemeInterface]] = []
        
        # The only allowed scheme is also the recommended one
        self._recommendediterationschemes: List[Type[IterationSchemeInterface]] = [
            ParallelLocal_SequentialController
        ]
        
        # Set inputs
        self._convergence_indicator_innerloop: ConvergenceIndicator_Innerloop_Interface = convergence_indicator_innerloop
        self._convergence_indicator_outerloop: ConvergenceIndicator_Outerloop_Interface = convergence_indicator_outerloop
        self._updatecouplingparametermethod_outerloop: UpdateCouplingParameterMethodInterface = updatecouplingparametermethod_outerloop
        self._iterationscheme: IterationSchemeInterface = iterationscheme

        # Validate inputs
        self.validate_inputs()
    
    def validate_inputs(self) -> None:
        """Validate the inputs provided to the ALADIN coordination method.
        
        Validates that the iteration scheme is compatible with ALADIN. The
        outer-loop update coupling parameter method and the convergence
        indicators are validated by the subsystems they are handed to
        (see LocalSubSystemALADIN.validate_inputs).
        
        Raises:
            ValueError: If any parameter is outside the allowed range.
        """
        # ===== Iteration Scheme Validation =====
        if type(self._iterationscheme) not in self._allowediterationschemes:
            raise ValueError(
                f"{DDO_Color}Iteration scheme '{type(self._iterationscheme).__name__}' is not allowed for ALADIN. "
                f"ALADIN requires a controller-based scheme. "
                f"Allowed schemes: {[s.__name__ for s in self._allowediterationschemes]}{Reset}"
            )
        elif type(self._iterationscheme) in self._unrecommendediterationschemes:
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: Iteration scheme '{type(self._iterationscheme).__name__}' is not recommended for ALADIN.")
            ddo_print(f"{type(self).__name__}: Recommended schemes for ALADIN: {[s.__name__ for s in self._recommendediterationschemes]}")
            ddo_print_border()
        
    def createSubSystems(self,
                         id_list: List[str],
                         level_list: List[int],
                         neighborid_list: List[List[str]],
                         analysis_list: List[AnalysisInterface],
                         localobjective_list: List[LocalObjectiveInterface],
                         localconstraints_list: List[LocalConstraintsInterface],
                         optimization_list: List[OptimizationInterface]) -> List[LocalSubSystemALADIN]:
        """Create local subsystems for ALADIN coordination.

        Args:
            id_list: List of subsystem identifiers.
            level_list: List of subsystem hierarchy levels.
            neighborid_list: List of neighbor ID lists for each subsystem.
            analysis_list: List of analysis interfaces.
            localobjective_list: List of local objective interfaces.
            localconstraints_list: List of local constraints interfaces.
            optimization_list: List of optimization interfaces.

        Returns:
            List of created ALADIN local subsystems.
        """
        if not (len(id_list) == len(level_list) == len(neighborid_list) == len(analysis_list) == len(localobjective_list) == len(localconstraints_list) == len(optimization_list)):
            raise ValueError(f"{DDO_Color}The length of the provided list does not match in ALADIN.createSubSystems{Reset}")
        
        subsystems = [LocalSubSystemALADIN(id=id_list[i],
                                           level=level_list[i],
                                           neighborid=neighborid_list[i],
                                           analysis=analysis_list[i],
                                           localobjective=localobjective_list[i],
                                           localconstraints=localconstraints_list[i],
                                           optimization=optimization_list[i],
                                           local_convergenceindicator_innerloop=self._convergence_indicator_innerloop.createLocalConvergenceIndicator(),
                                           local_convergenceindicator_outerloop=self._convergence_indicator_outerloop.createLocalConvergenceIndicator(),
                                           # deepcopy() to strengthen distributed character - only middlelevels are shared recourses between subsystems
                                           updatecouplingparametermethod_outerloop=copy.deepcopy(self._updatecouplingparametermethod_outerloop))
                      for i in range(len(id_list))]
            
        return subsystems
    
    def createControllerSubSystem(self, subsystemsIn: List[LocalSubSystemALADIN]) -> SubSystemInterface | None:
        """Create the ALADIN controller subsystem.

        Args:
            subsystemsIn: List of local subsystems to coordinate.

        Returns:
            The created controller subsystem.
        """
        # Get IDs of all local subsystems
        local_subsystem_ids: List[str] = [subsystem.get_SUBSYSTEMID() for subsystem in subsystemsIn]
        
        # Get neighbors of neighbors list
        neighbors_of_neighbors_id: Dict[str, List[str]] = {}
        
        # Loop over local neighbor id to have the mapping of local subsystem id and its neighbors' ids list
        for subsystem in subsystemsIn:
            # Assign local id -> List of neighbor ids in dictionary neighbors_of_neighbors_id
            neighbors_of_neighbors_id[subsystem.get_SUBSYSTEMID()] = subsystem.get_NeighborId()  
        
        subsystemcontroller: ControllerSubSystemALADIN = ControllerSubSystemALADIN(neighborid=local_subsystem_ids,
                                                                                   neighbors_of_neighbors_ids=neighbors_of_neighbors_id,
                                                                                   optimization=OptimizationController())
        
        return subsystemcontroller
    
    def createMiddleLevel(self, idparent: str, idchild: str, multiprocessing_lock: object = None) -> LocalToLocal_MiddleLevelDataStorageALADIN:
        """Create a local-to-local middle level data storage.

        Args:
            idparent: Identifier of the parent subsystem.
            idchild: Identifier of the child subsystem.
            multiprocessing_lock: Optional lock for thread-safe access in multiprocessing.

        Returns:
            The created local-to-local middle level data storage.
        """
        return LocalToLocal_MiddleLevelDataStorageALADIN(idparent=idparent, idchild=idchild, multiprocessing_lock=multiprocessing_lock)
    
    def createControllerMiddleLevel(self, idparent: str, idchild: str, local_neighbors_list: List[str], multiprocessing_lock: object = None) -> LocalController_MiddleLevelDataStorageALADIN | None:
        """Create middle level between controller and local subsystem.

        Args:
            idparent: Identifier of the parent (controller) subsystem.
            idchild: Identifier of the child (local) subsystem.
            local_neighbors_list: List of neighbor IDs for the local subsystem.
            multiprocessing_lock: Optional lock for thread-safe access in multiprocessing.

        Returns:
            The created local-to-controller middle level data storage.
        """
        return LocalController_MiddleLevelDataStorageALADIN(idparent=idparent, idchild=idchild,
                                                            local_neighbors_list=local_neighbors_list, multiprocessing_lock=multiprocessing_lock)

    def centralized_prepare_updateCouplingParameters(self, subsystemsIn: List[LocalSubSystemALADIN | ControllerSubSystemALADIN]) -> None:
        """Prepare centralized update of coupling parameters for all subsystems.

        For ALADIN, no centralized operation is required.

        Args:
            subsystemsIn: List of subsystems to prepare coupling parameters for.
        """
        pass
    
    def print_beginning_of_centralized_prepare_updateCouplingParameters(self) -> None:
        """Nothing to print."""
        # Nothing to print
        pass
