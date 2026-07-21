# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Factory module for creating middle-level objects.

This module provides factory functions for creating middle-level data storage
and coupling objects for different coordination methods.
"""

from typing import List, Any, Dict, Tuple
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset
from Distributed_Design_Optimizer.coordination import CustomManager
from Distributed_Design_Optimizer.coordination.coordinationmethod import CoordinationMethodInterface
from Distributed_Design_Optimizer.middlelevel import MiddleLevelDataStorageInterface
from Distributed_Design_Optimizer.subsystem import SubSystemInterface
from Distributed_Design_Optimizer.subsystem.couplingparameters import CouplingParametersInterface


class CreateMiddleLevels:
    """Factory class for creating middle level data storage objects.

    Provides static methods to create and manage middle level data storage
    instances for distributed optimization coordination.
    """

    @staticmethod
    def createMiddleLevels(subsystemsIn: List[SubSystemInterface],
                           manager: CustomManager | None,
                           coordinationmethod: CoordinationMethodInterface) -> List[MiddleLevelDataStorageInterface]:
        """Create middle level data storage objects for subsystem couplings.

        Creates appropriate middle level storage based on the coordination
        method and subsystem coupling relationships.

        Args:
            subsystemsIn: List of subsystems to create middle levels for.
            manager: Optional CustomManager for multiprocessing support.
            coordinationmethod: Coordination method defining middle level types.

        Returns:
            List of middle level data storage objects for all couplings.
        """
        strlist = []
        
        # The key is the id of a local subsystem and 
        # the value is the list of neighbor ids
        neighbors_of_local_subsystems: Dict[Tuple[str], List[str]] = {}
            
        try:
            # create list of unique subsystem ID pairs that are coupled
            for i in range(len(subsystemsIn)):
                coupling: List[CouplingParametersInterface] = subsystemsIn[i].get_CouplingParameters()
                strid: str = subsystemsIn[i].get_SUBSYSTEMID()
                for j in range(len(coupling)):
                    ids: List[str] = [strid, coupling[j].get_ID()]
                    
                    # Check if this pair already exists (in either order)
                    addtolist = True
                    for k in range(len(strlist)):
                        dum = strlist[k]
                        if (((ids[0] == dum[0]) and (ids[1] == dum[1])) or
                                ((ids[0] == dum[1]) and (ids[1] == dum[0]))):
                            addtolist = False
                            break
                    if addtolist is True:
                        
                        # Keep track of the neighbors of local subsystems
                        
                        # If the coupling is between a local subsystem 
                        # and the controller
                        if subsystemsIn[i].get_SUBSYSTEMID() == "C" or coupling[j].get_ID() == "C":

                            # Add neighbors of the local subsystem to the dictionary
                            # 'neighbors_of_local_subsystems'
                            
                            neighbors_of_local_subsystems[tuple(ids)] = subsystemsIn[i].get_NeighborId()
                        
                        # If the subsystem is a local subsystem
                        # Check valid Id, i.e., if it is an integer
                        elif subsystemsIn[i].get_SUBSYSTEMID().isdigit() and coupling[j].get_ID().isdigit():
                            pass  # valid local-to-local pair
                        
                        else:
                            
                            # Non-valid subsystem IDs
                            raise ValueError(f"{DDO_Color}In CreateMiddleLevels.createMiddleLevels: The subsystem IDs (also in coupling parameters) can only be positive integers or 'C' for controller; current ID is neither{Reset}")
                        
                        strlist.append(ids)

            # Create the middle-levels with individual locks if manager is provided
            middlelevels = []
            
            # Create appropriate middlelevels based on the subsystem type
            for x in strlist:  # x is of type List[str] and holds IDs of two subsystems
                # Create an individual lock for each middlelevel if manager is provided
                multiprocessing_lock = manager.Lock() if manager is not None else None
                
                # Create appropriate MiddleLevel object based on the coordination method type
                # Both local and controller subsystems
                if "C" not in x:
                    local_middlelevel = coordinationmethod.createMiddleLevel(x[0], x[1], multiprocessing_lock=multiprocessing_lock)
                    if local_middlelevel is None:
                        # Throw error if coordinationmethod.createMiddleLevel returns None
                        raise ValueError(f"{DDO_Color}The local_middlelevel should be specified in createMiddleLevel of CoordinationMethodInterface{Reset}")
                    middlelevels.append(local_middlelevel)
                else:
                    # Intermediate storage of object
                    local_id: str | None = None
                    
                    if x[0] == "C":
                        # x[1] has the ID of the associated local subsystem
                        local_id = x[1]
                    elif x[1] == "C":
                        # x[0] has the ID of the associated local subsystem
                        local_id = x[0]
                    
                    # In local <-> controller middle level, idparent is "C" of controller and 
                    # id_child of local subsystem with ID local_id
                    controller_middlelevel = coordinationmethod.createControllerMiddleLevel("C",
                                                                                            local_id,
                                                                                            local_neighbors_list=neighbors_of_local_subsystems[tuple(x)], 
                                                                                            multiprocessing_lock=multiprocessing_lock)                        
                        
                    if controller_middlelevel is None:
                        # Throw error if coordinationmethod.createControllerMiddleLevel returns None
                        raise ValueError(f"{DDO_Color}The controller_middlelevel should be specified in createControllerMiddleLevel of CoordinationMethodInterface{Reset}")
                    middlelevels.append(controller_middlelevel)
            
        except IndexError as e:
            raise IndexError(f"{DDO_Color}Trying to access nonexisting subsystem in array{Reset}") from e

        return middlelevels


    @staticmethod
    def createManagedMiddleLevels(middlelevelsIn: List[MiddleLevelDataStorageInterface], managerIn: CustomManager) -> List[Any]:
        """Create managed middle levels for multiprocessing.

        Wraps middle level objects with multiprocessing manager proxies
        for shared access across processes.

        Args:
            middlelevelsIn: List of middle level objects to wrap.
            managerIn: CustomManager for creating managed objects.

        Returns:
            List of managed middle level proxy objects.
        """
        if managerIn is None:
            raise ValueError(f"{DDO_Color}Error: Manager not found for multiprocessing.{Reset}")
        
        # Create managed middlelevels by delegating to each MiddleLevel's createManagedMiddleLevel method
        managed_middlelevels = []
        for ml in middlelevelsIn:
            lock = managerIn.Lock()
            managed = ml.createManagedMiddleLevel(managerIn, lock)
            managed_middlelevels.append(managed)
            
        return managed_middlelevels
