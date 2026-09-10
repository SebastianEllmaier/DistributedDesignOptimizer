---
title: ResidualComputer (Source)
---

← Back to [ResidualComputer documentation](ResidualComputer.md)

# ResidualComputer - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\ResidualComputer.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Residual computation module.

This module provides functionality for computing residuals
in distributed optimization problems.
"""

import copy
from typing import List, Dict

import numpy as np
from pyvis.network import Network
import webview
import os
from Distributed_Design_Optimizer.postprocess import GraphInit
from Distributed_Design_Optimizer.subsystem import SubSystemInterface
from Distributed_Design_Optimizer.coordination.innerloop_iterationscheme import (IterationSchemeInterface,
                                                                                 Parallel,
                                                                                 SequentialForward,
                                                                                 SequentialBackward,
                                                                                 ParallelEvenThenOddLevels,
                                                                                 ParallelPerLevelIncreasing
                                                                                 )
from Distributed_Design_Optimizer.middlelevel import MiddleLevelDataStorageInterface, MiddleLevelCouplingInterface
from Distributed_Design_Optimizer.subsystem.couplingparameters.alc import CouplingParametersALC
from Distributed_Design_Optimizer.subsystem.couplingparameters.lc import CouplingParametersLC
from Distributed_Design_Optimizer.subsystem.couplingparameters.pc import CouplingParametersPC


class ResidualComputer:
    """
    Computes residuals for edges in the master graph using coupling data from MiddleLevelDataStorageInterface objects.
    
    This class creates a bridge between the coupling data stored in MiddleLevelDataStorageInterface
    objects and the graph structure in GraphInit, computing and storing residuals
    as edge attributes in the master graph.
    """
    
    def __init__(self,
                 graph_init: GraphInit,
                 middlelevel_storages: List[MiddleLevelDataStorageInterface],
                 subsystems: List[SubSystemInterface],
                 iterationscheme: IterationSchemeInterface):
        """Initialize the residual computer.

        Args:
            graph_init: The graph initialization object containing the master graph.
            middlelevel_storages: List of all MiddleLevelDataStorageInterface objects.
            subsystems: List of subsystems in the system.
            iterationscheme: The iteration scheme used for coordination.
        """
        self._graphinit = graph_init
        self._mastergraph = graph_init.get_graph()
        self._subsystems: List[SubSystemInterface] = subsystems
        self._middlelevelstorages: List[MiddleLevelDataStorageInterface] = middlelevel_storages
        self._iterationscheme: IterationSchemeInterface = iterationscheme
        
        # Create a lookup map for faster access
        self.create_storage_lookup()
        self.create_subsystem_lookup()
    
    def create_storage_lookup(self) -> None:
        """Create a lookup dictionary for MiddleLevelDataStorageInterface objects."""
        self._storage_lookup: Dict[tuple, MiddleLevelDataStorageInterface] = {}
        
        for storage in self._middlelevelstorages:
            ids = storage.get_ID()
            # Store both directions for bidirectional lookup
            # This allows finding the same storage object for both (A,B) and (B,A)
            self._storage_lookup[(ids[0], ids[1])] = storage
            self._storage_lookup[(ids[1], ids[0])] = storage
    
    def create_subsystem_lookup(self) -> None:
        """Create a lookup dictionary for Subsystems objects."""
        self.subsystem_lookup: Dict[str, SubSystemInterface] = {}
        
        for subsystem in self._subsystems:
            id = subsystem.get_SUBSYSTEMID()
            self.subsystem_lookup[id] = subsystem
    
    def compute_all_primal_residuals(self) -> None:
        """Compute primal residuals for all edges in the master graph."""
        graph = self._mastergraph
        
        for u, v, key, data in graph.edges(keys=True, data=True):
            edge_type = data.get('type')
            self.compute_single_primal_residual(u, v, edge_type)
            
        #self.visualize_graph()
        

    def compute_single_primal_residual(self, idparent: str, idchild: str, edge_type: str) -> None:
        """Compute primal residual for a single edge.

        Args:
            idparent: Parent node ID.
            idchild: Child node ID.
            edge_type: Type of edge.
        """
        # Get the corresponding MiddleLevelDataStorageInterface
        storage = self._storage_lookup.get((idparent, idchild))
        if storage is None:
            print(f"Warning: No storage found for edge {idparent} -> {idchild}")
            return
        
        # Get coupling data for both parent and child.
        # get_CouplingData() returns [parent_data, child_data] matching
        # the order of get_ID() = [idparent, idchild].
        # Post-processing runs after optimization completes (no concurrent
        # writers), so accessing the raw references is safe here.
        coupling_data = storage.get_CouplingData()
        storage_ids = storage.get_ID()
        
        parent_coupling = None
        child_coupling = None
        for idx, sid in enumerate(storage_ids):
            if sid.lower() == idparent.lower():
                parent_coupling = coupling_data[idx]
            elif sid.lower() == idchild.lower():
                child_coupling = coupling_data[idx]
        
        if parent_coupling is None or child_coupling is None:
            print(f"Warning: Missing coupling data for edge {idparent} -> {idchild}")
            return
        
        # Compute residual based on edge type
        residual_values = self.calculate_primal_residual_by_type(parent_coupling, child_coupling, edge_type)
        
        if residual_values is not None:
            # Store the computed residual in the master graph
            self._graphinit.store_primalresidual(idparent, idchild, edge_type, residual_values)
            #print(f"Computed primal residual for edge {idparent} -> {idchild} ({edge_type}): {residual_values}")

    def calculate_primal_residual_by_type(self, parent_coupling: MiddleLevelCouplingInterface, child_coupling: MiddleLevelCouplingInterface, edge_type: str) -> List[float] | None:
        """Calculate primal residual values based on edge type.

        Args:
            parent_coupling: MiddleLevelCouplingInterface object for parent.
            child_coupling: MiddleLevelCouplingInterface object for child.
            edge_type: Type of edge.

        Returns:
            Computed residual values or None if computation fails.
        """
        try:
            # For decomposed mapped response edges: MappedResponseVariable[idparent] - CopyCouplingVariable[idchild]
            if edge_type == "decomposed_mappedresponse":
                parent_vars = parent_coupling.get_MappedResponses()
                child_vars = child_coupling.get_CouplingVariable()
                
                parent_array = np.array(parent_vars)
                child_array = np.array(child_vars)                
                
                residual = np.abs(parent_array - child_array)
                return residual.tolist()
            
            # For decomposed shared design variable edges: SharedDesignVariable[idparent] - CopyTargetVariable[idchild]
            elif edge_type == "decomposed_shareddesignvariable":
                parent_vars = parent_coupling.get_SharedDesignVariables()
                child_vars = child_coupling.get_TargetSharedDesignVariables()
                
                parent_array = np.array(parent_vars)
                child_array = np.array(child_vars)
                
                residual = np.abs(parent_array - child_array)
                return residual.tolist()
            
            # For non-decomposed edges: No residual computation
            elif edge_type.startswith("nondecomposed"):
                return None
            
            else:
                print(f"Warning: Unknown edge type '{edge_type}' for primal residual computation")
                return None
                
        except Exception as e:
            print(f"Error computing primal residual for edge type {edge_type}: {e}")
            return None

    
    def compute_all_dual_residuals(self, convinnerloop: bool) -> None:
        """Compute dual residuals for all edges in the master graph.

        Args:
            convinnerloop: Whether the inner loop has converged.
        """
        graph = self._mastergraph
        
        for u, v, key, data in graph.edges(keys=True, data=True):
            edge_type = data.get('type')
            self.compute_single_dual_residual(u, v, edge_type, convinnerloop)
            

    def compute_single_dual_residual(self, idparent: str, idchild: str, edge_type: str, convinnerloop: bool) -> None:
        """Compute dual residual for a single edge.

        Args:
            idparent: Parent node ID.
            idchild: Child node ID.
            edge_type: Type of edge.
            convinnerloop: Whether the inner loop has converged.
        """
        # Get the parent and child subsystems
        parent_subsystem = self.subsystem_lookup.get(idparent)
        child_subsystem = self.subsystem_lookup.get(idchild)
        
        if parent_subsystem is None:
            print(f"Warning: No Parent Hierarchic Subsystems found for ID {idparent}")
            
        if child_subsystem is None:
            print(f"Warning: No Child Hierarchic Subsystems found for ID {idparent}")
        
        # computes the dualresidual and relativedualresidual 
        dualresidual: List[float | None] | None = self.calculate_dual_residual_by_type(parent_subsystem, child_subsystem, idparent, idchild, edge_type, convinnerloop)
        
        if dualresidual is not None:
            # Store the computed dual residuals in the master graph
            self._graphinit.store_dualresidual(idparent, idchild, edge_type, dualresidual)
            
    def determine_DualResidualtype(self, parent_subsystem: SubSystemInterface, child_subsystem: SubSystemInterface) -> str:
        """Determine the type of ADMM residual computation based on level and execution.

        Args:
            parent_subsystem: The parent subsystem.
            child_subsystem: The child subsystem.

        Returns:
            The residual definition type string.
        """
        parentlevel = parent_subsystem.get_SubsystemLevel()
        childlevel = child_subsystem.get_SubsystemLevel()
        residualdefinintion = None
    
        if isinstance(self._iterationscheme, ParallelPerLevelIncreasing):
            if parentlevel == childlevel:
                residualdefinintion = "ParentChildParallel"
            else:                
                if parentlevel < childlevel:
                    residualdefinintion = "ParentFirst_ChildSecond"
                else:
                    residualdefinintion = "ChildFirst_ParentSecond"
                
        elif isinstance(self._iterationscheme, Parallel):
            residualdefinintion = "ParentChildParallel"
        
        elif isinstance(self._iterationscheme, ParallelEvenThenOddLevels):
            if parentlevel == childlevel:
                residualdefinintion = "ParentChildParallel"
            else:
                if parentlevel % 2 == 0:
                    residualdefinintion = "ParentFirst_ChildSecond"
                elif parentlevel % 2 == 1:
                    residualdefinintion = "ChildFirst_ParentSecond"
                
        elif isinstance(self._iterationscheme, SequentialForward):
            if parent_subsystem.get_SUBSYSTEMID() < child_subsystem.get_SUBSYSTEMID():
                residualdefinintion = "ParentFirst_ChildSecond"
            else:
                residualdefinintion = "ChildFirst_ParentSecond"
        
        elif isinstance(self._iterationscheme, SequentialBackward):
            if parent_subsystem.get_SUBSYSTEMID() < child_subsystem.get_SUBSYSTEMID():
                residualdefinintion = "ChildFirst_ParentSecond"
            else:
                residualdefinintion = "ParentFirst_ChildSecond"
                
        else: 
            raise NotImplementedError("Unknonw iterationscheme type in ResidualComputer.determine_DualResidualtype().")
                
        return residualdefinintion

    def calculate_dual_residual_by_type(self, parent_subsystem: SubSystemInterface, child_subsystem: SubSystemInterface, 
                                         idparent: str, idchild: str, edge_type: str, convinnerloop: bool) -> List[float | None] | None:
        """Calculate dual residual values based on edge type.

        Args:
            parent_subsystem: The parent subsystem.
            child_subsystem: The child subsystem.
            idparent: Parent node ID.
            idchild: Child node ID.
            edge_type: Type of edge.
            convinnerloop: Whether the inner loop has converged.

        Returns:
            Computed residual values or None.
        """
        
        ### Sequential Bottom Up requires Resiudal Def B, modify accordingly
        dualresidual = None
        try:
            if edge_type.startswith("nondecomposed"):
                return None
            
            residualtype = self.determine_DualResidualtype(parent_subsystem, child_subsystem)
            
            if edge_type == "decomposed_mappedresponse":
                if residualtype == "ParentFirst_ChildSecond":
                    dualresidual = self.compute_ParentFirstChildSecondMappedDualResidual(parent_subsystem, child_subsystem, idparent, idchild, convinnerloop)
                elif residualtype == "ChildFirst_ParentSecond":
                    dualresidual = self.compute_ChildFirstParentSecondMappedDualResidual(parent_subsystem, child_subsystem, idparent, idchild, convinnerloop)
                elif residualtype == "ParentChildParallel":
                    dualresidual = self.compute_ParentChildParallelMappedDualResidual(parent_subsystem, child_subsystem, idparent, idchild, convinnerloop)
                else:
                    print('Unknown Residual Computation Method')                
                    
            elif edge_type == "decomposed_shareddesignvariable":
                if residualtype == "ParentFirst_ChildSecond":
                    dualresidual = self.compute_ParentFirstChildSecondSharedDualResidual(parent_subsystem, child_subsystem, idparent, idchild, convinnerloop)
                elif residualtype == "ChildFirst_ParentSecond":
                    dualresidual = self.compute_ChildFirstParentSecondSharedDualResidual(parent_subsystem, child_subsystem, idparent, idchild, convinnerloop)
                elif residualtype == "ParentChildParallel":
                    residual = self.compute_ParentChildParallelSharedDualResidual(parent_subsystem, child_subsystem, idparent, idchild, convinnerloop)
                    dualresidual = [residual, residual]
                else:
                    print('Unknown Residual Computation Method')
            
            else:
                print(f"Warning: Unknown edge type '{edge_type}' for dual residual computation")
                return None

            return dualresidual
 
        except Exception as e:
            print(f"Error computing dual residual for edge type {edge_type}: {e}")
            return None
    
    def compute_ParentFirstChildSecondMappedDualResidual(self, parent_subsystem: SubSystemInterface, child_subsystem: SubSystemInterface,
                                                         idparent: str, idchild: str, convinnerloop: bool) -> List[float | None]:
        """Compute dual residual for parent-first child-second mapped response edge.

        Args:
            parent_subsystem: The parent subsystem.
            child_subsystem: The child subsystem.
            idparent: Parent node ID.
            idchild: Child node ID.
            convinnerloop: Whether the inner loop has converged.

        Returns:
            The computed dual residual values.
        """
        
        parentcoupling: List[CouplingParametersALC] | List[CouplingParametersLC] | List[CouplingParametersPC] = parent_subsystem.get_CouplingParameters()
        parent_subsystem.compute_Jacobian_MappedResponse_Wrt_DesignVariables()
        parentjacobians: List[List[List[float]] | None] | None = parent_subsystem.get_Jacobian_MappedResponse_Wrt_DesignVariables_Value()
        childcoupling_previous: List[CouplingParametersALC] | List[CouplingParametersLC] | List[CouplingParametersPC] = child_subsystem.copy_Coupling_Previous_outerloop_itr()
        
        for coupling in child_subsystem.get_CouplingParameters():
            if coupling.get_ID() == idparent:
                childcouplingvariable_current = coupling.get_CouplingVariable()
                break

        for coupling in childcoupling_previous:
            if coupling.get_ID() == idparent:
                childcouplingvariable_previous = coupling.get_CouplingVariable()
                break
        
        dualresidual = [None] * len(childcouplingvariable_current)
        
        if convinnerloop is True:
            for i in range(len(parentcoupling)):            
                if parentcoupling[i].get_ID() == idchild and parentjacobians is not None:                
                    jacobian = np.array(parentjacobians[i])
                    
                    for i in range(len(childcoupling_previous)):
                        if childcoupling_previous[i].get_ID() == idparent:    
                            if isinstance(childcoupling_previous[i], CouplingParametersALC) or isinstance(childcoupling_previous[i], CouplingParametersPC):
                                weights: List[float] | None = childcoupling_previous[i].get_Weights_CopyMappedResponse_Minus_CouplingVariable()
                                break
                            else:
                                return None
                    couplingvariables_change = None
                    if childcouplingvariable_current is not None and childcouplingvariable_previous is not None:
                        couplingvariables_change = np.array(childcouplingvariable_current) - np.array(childcouplingvariable_previous)
                    if jacobian is not None and weights is not None and couplingvariables_change is not None :
                        dualresidual: List[float] = (2 * (jacobian.T @ (np.array(weights)**2 * couplingvariables_change))).tolist()
                    
        return dualresidual

    def compute_ChildFirstParentSecondMappedDualResidual(self, parent_subsystem: SubSystemInterface, 
                                                         child_subsystem: SubSystemInterface, idparent: str, idchild: str, convinnerloop: bool) -> List[float | None]:
        """Compute dual residual for child-first parent-second mapped response edge.

        Args:
            parent_subsystem: The parent subsystem.
            child_subsystem: The child subsystem.
            idparent: Parent node ID.
            idchild: Child node ID.
            convinnerloop: Whether the inner loop has converged.

        Returns:
            The computed dual residual values.
        """
        
        
        parentxopt_original = copy.deepcopy(parent_subsystem.get_OptimData().get_DesignVariables())
        parentxopt_current = copy.deepcopy(parentxopt_original)
        parent_subsystem.set_DesignVariables(parentxopt_current)
        parent_subsystem.evaluateTotalObjective()
        parent_subsystem.evaluateTotalConstraint()
        parentcoupling_current: List[CouplingParametersALC] | List[CouplingParametersLC] | List[CouplingParametersPC] = parent_subsystem.get_CouplingParameters()
        
        for i in range(len(parentcoupling_current)):
            if parentcoupling_current[i].get_ID() == idchild:
                parentmapped_current = parentcoupling_current[i].get_MappedResponses()            
                
        
        parentcoupling_previous: List[CouplingParametersALC] | List[CouplingParametersLC] | List[CouplingParametersPC] = parent_subsystem.copy_Coupling_Previous_outerloop_itr()
        for coupling in parentcoupling_previous:
            if coupling.get_ID() == idchild:
                parentmapped_previous = coupling.get_MappedResponses()
                if isinstance(coupling, CouplingParametersALC) or isinstance(coupling, CouplingParametersPC):
                    weights: List[float] | None = coupling.get_Weights_MappedResponse_Minus_CopyCouplingVariable()
                    break
                else:
                    return None

        dualresidual = [None] * len(parentmapped_current)
        if convinnerloop is True:
            mappedvariables_change = None
            if parentmapped_previous is not None and parentmapped_current is not None:
                mappedvariables_change = np.array(parentmapped_previous) - np.array(parentmapped_current)
            
            if mappedvariables_change is not None and weights is not None:             
                dualresidual: List[float] = (-2 * (np.array(weights)**2 * mappedvariables_change)).tolist()

        return dualresidual
    
    def compute_ParentChildParallelMappedDualResidual(self, parent_subsystem: SubSystemInterface, 
                                                      child_subsystem: SubSystemInterface, idparent: str, idchild: str, convinnerloop: bool) -> List[float | None]:
        """Compute dual residual for parallel parent-child mapped response edge.

        Args:
            parent_subsystem: The parent subsystem.
            child_subsystem: The child subsystem.
            idparent: Parent node ID.
            idchild: Child node ID.
            convinnerloop: Whether the inner loop has converged.

        Returns:
            The computed dual residual values.
        """
        parentresiduals = self.compute_ParentFirstChildSecondMappedDualResidual(parent_subsystem, child_subsystem, idparent, idchild, convinnerloop)
        childresiduals = self.compute_ChildFirstParentSecondMappedDualResidual(parent_subsystem, child_subsystem, idparent, idchild, convinnerloop)
        dualresidual = [None] * (len(parentresiduals) + len(childresiduals))

        if convinnerloop is True:
            if parentresiduals is not None and childresiduals is not None:
                dualresidual: List[float | None] = parentresiduals + childresiduals
        
        return dualresidual
        
    def compute_ParentFirstChildSecondSharedDualResidual(self, parent_subsystem: SubSystemInterface, child_subsystem: SubSystemInterface,
                                                         idparent: str, idchild: str, convinnerloop: bool) -> List[float | None]:
        """Compute dual residual for parent-first child-second shared design variable edge.

        Args:
            parent_subsystem: The parent subsystem.
            child_subsystem: The child subsystem.
            idparent: Parent node ID.
            idchild: Child node ID.
            convinnerloop: Whether the inner loop has converged.

        Returns:
            The computed dual residual values.
        """
        
        childcoupling_current: List[CouplingParametersALC] | List[CouplingParametersLC] | List[CouplingParametersPC] = child_subsystem.get_CouplingParameters()
        childcoupling_previous: List[CouplingParametersALC] | List[CouplingParametersLC] | List[CouplingParametersPC] = child_subsystem.copy_Coupling_Previous_outerloop_itr()
        
        for coupling in childcoupling_previous:
            if coupling.get_ID() == idparent:
                childTargetSharedVariable_previous = coupling.get_TargetSharedDesignVariables()            
                if isinstance(coupling, CouplingParametersALC) or isinstance(coupling, CouplingParametersPC):
                   weights: List[float] | None = coupling.get_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable()
                   break
                else:
                    return None
            
        for coupling in childcoupling_current:
            if coupling.get_ID() == idparent:
                childTargetSharedVariable_current = coupling.get_TargetSharedDesignVariables()
                break     
        
        dualresidual = [None] * len(childTargetSharedVariable_current)    
        if convinnerloop is True:
            TargetSharedVariables_difference = None
            if childTargetSharedVariable_current is not None and childTargetSharedVariable_previous is not None:
                TargetSharedVariables_difference = np.array(childTargetSharedVariable_current)-np.array(childTargetSharedVariable_previous)
            if weights is not None and TargetSharedVariables_difference is not None:
                
                dualresidual: List[float] = (2 * (np.array(weights)**2 * TargetSharedVariables_difference)).tolist()
        
        return dualresidual
    
    def compute_ChildFirstParentSecondSharedDualResidual(self, parent_subsystem: SubSystemInterface, child_subsystem: SubSystemInterface, 
                                                         idparent: str, idchild: str, convinnerloop: bool) -> List[float | None]:
        """Compute dual residual for child-first parent-second shared design variable edge.

        Args:
            parent_subsystem: The parent subsystem.
            child_subsystem: The child subsystem.
            idparent: Parent node ID.
            idchild: Child node ID.
            convinnerloop: Whether the inner loop has converged.

        Returns:
            The computed dual residual values.
        """
        parentcoupling_current: List[CouplingParametersALC] | List[CouplingParametersLC] | List[CouplingParametersPC] = parent_subsystem.get_CouplingParameters()
        parentcoupling_previous: List[CouplingParametersALC] | List[CouplingParametersLC] | List[CouplingParametersPC] = parent_subsystem.copy_Coupling_Previous_outerloop_itr()
        
        for coupling in parentcoupling_previous:
            if coupling.get_ID() == idchild:
                SharedDesignVariable_previous = coupling.get_SharedDesignVariables()
                if isinstance(coupling, CouplingParametersALC) or isinstance(coupling, CouplingParametersPC):
                    weights: List[float] | None = coupling.get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable()
                    break
                else:
                    return None
        
        for coupling in parentcoupling_current:
            if coupling.get_ID() == idchild:
                SharedDesignVariable_current = coupling.get_SharedDesignVariables()
                break
        
        dualresidual = [None] * len(SharedDesignVariable_current)
        if convinnerloop is True:
            SharedDesignVariables_difference = None
            if SharedDesignVariable_previous is not None and SharedDesignVariable_current is not None:
                SharedDesignVariables_difference = np.array(SharedDesignVariable_previous) - np.array(SharedDesignVariable_current)
            if weights is not None and SharedDesignVariables_difference is not None:
                dualresidual: List[float] = (-2 * (np.array(weights)**2 * SharedDesignVariables_difference)).tolist()

        return dualresidual
    
    def compute_ParentChildParallelSharedDualResidual(self, parent_subsystem: SubSystemInterface, child_subsystem: SubSystemInterface, 
                                                      idparent: str, idchild: str, convinnerloop: bool) -> List[float | None]:
        """Compute dual residual for parallel parent-child shared design variable edge.

        Args:
            parent_subsystem: The parent subsystem.
            child_subsystem: The child subsystem.
            idparent: Parent node ID.
            idchild: Child node ID.
            convinnerloop: Whether the inner loop has converged.

        Returns:
            The computed dual residual values.
        """
        
        parentresidual = self.compute_ParentFirstChildSecondSharedDualResidual(parent_subsystem, child_subsystem, idparent, idchild, convinnerloop)
        childresidual = self.compute_ChildFirstParentSecondSharedDualResidual(parent_subsystem, child_subsystem, idparent, idchild, convinnerloop)
        dualresidual = [None] * (len(parentresidual) + len(childresidual))
        
        if convinnerloop is True:
            if parentresidual is not None and childresidual is not None:
                dualresidual: List[float | None] = parentresidual + childresidual
        
        return dualresidual

    def compute_residual_for_edge(self, idparent: str, idchild: str, edge_type: str, residual_type: str = "primal") -> None:
        """Compute residual for a specific edge on demand.

        Args:
            idparent: Parent node ID.
            idchild: Child node ID.
            edge_type: Type of edge.
            residual_type: Type of residual to compute ('primal' or 'dual').
        """
        if residual_type.lower() == "primal":
            self.compute_single_primal_residual(idparent, idchild, edge_type)
        elif residual_type.lower() == "dual":
            self.compute_single_dual_residual(idparent, idchild, edge_type)
        else:
            print(f"Warning: Unknown residual type '{residual_type}'. Use 'primal' or 'dual'.")
    
    def get_residual_summary(self) -> dict:
        """Get a comprehensive summary of computed residuals.

        Returns:
            Summary statistics including counts, max values, and formatted output.
        """
    
        graph = self._graphinit.get_graph()
        
        # Initialize the nested structure - fully indexable
        summary = {
            "edges": {}
        }
        
        # process each edge
        for u, v, data in graph.edges(data= True):
            # create an edge id
            edge_id = f"{u}-{v}"
            edge_type = data.get('type', 'unknown')
        
        # Extract the correct residual data based on edge type
            primal_residuals = None
            dual_residuals = None
            
            if edge_type in ["decomposed_mappedresponse", "nondecomposed_mappedresponse"]:
                primal_residuals: List[float] = data.get('primalmappedresidual')
                dual_residuals: List[float | None] | None = data.get('dualmappedresidual')
                
            elif edge_type in ["decomposed_shareddesignvariable", "nondecomposed_shareddesignvariable"]:
                primal_residuals: List[float] = data.get('primalsharedresidual')
                dual_residuals: List[float | None] | None = data.get('dualsharedresidual')
                
            
            # store the data in the data structure
            summary["edges"][edge_id] = {
                "id": edge_id,
                "type": edge_type,
                "primal_residuals": primal_residuals,
                "dualresiduals": dual_residuals,

            }
        return summary
    
    def visualize_graph(self) -> None:
        """Visualize the master graph using PyVis inside a GUI window."""
        graph = self._mastergraph
        
        # Create a PyVis network
        net = Network(height="100%", width="100%", bgcolor="#222222", font_color="white", notebook=True, directed=True)
        
        # Add nodes
        for node in graph.nodes():
            net.add_node(node, label=str(node))
            
        # Add edges with primal residual as weight
        for u, v, data in graph.edges(data=True):
            edge_type = data.get('type', 'unknown')
            
            primal_residuals = None
            if edge_type in ["decomposed_mappedresponse", "nondecomposed_mappedresponse"]:
                primal_residuals = data.get('primalmappedresidual')
            elif edge_type in ["decomposed_shareddesignvariable", "nondecomposed_shareddesignvariable"]:
                primal_residuals = data.get('primalsharedresidual')
            
            weight = 0.0
            if primal_residuals:
                # Use the L2 norm of the residual vector as the edge weight
                weight = np.linalg.norm(primal_residuals)
            
            # The 'title' attribute provides hover-over information
            title = f"Primal Residual Norm: {weight:.4f}<br>Decomposition Type: {edge_type}<br>Vector: {primal_residuals}"
            
            net.add_edge(u, v, value=weight, title=title)
            
        # Configure physics for better layout
        net.set_options("""
        var options = {
          "physics": {
            "forceAtlas2Based": {
              "gravitationalConstant": -50,
              "centralGravity": 0.01,
              "springLength": 100,
              "springConstant": 0.08
            },
            "minVelocity": 0.75,
            "solver": "forceAtlas2Based"
          }
        }
        """)
        
        # Save the graph to a temporary HTML file
        output_filename = "primal_residual_graph.html"
        net.save_graph(output_filename)
        
        # Get the full path to the HTML file
        html_file_path = os.path.abspath(output_filename)

        # --- GUI Display Logic ---
        try:
            # Create a pywebview window to display the local HTML file
            print("Opening graph in a GUI window...")
            webview.create_window(
                "Primal Residual Graph",
                f"file://{html_file_path}",
                width=1200,
                height=800,
                resizable=True
            )
            webview.start()
            print("GUI window closed.")

        except Exception as e:
            print(f"Could not create GUI window. Error: {e}")
        finally:
            # Clean up the temporary HTML file
            if os.path.exists(output_filename):
                os.remove(output_filename)
```
