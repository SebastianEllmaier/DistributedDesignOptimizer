---
title: CompromiseComputer (Source)
---

← Back to [CompromiseComputer documentation](CompromiseComputer.md)

# CompromiseComputer - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\CompromiseComputer.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Compromise computation module for optimization analysis.

This module provides functionality for computing compromise metrics
in distributed optimization problems.
"""

from typing import List, Dict, Tuple

import numpy as np
from decimal import Decimal, getcontext
from Distributed_Design_Optimizer.postprocess import GraphInit
from Distributed_Design_Optimizer.subsystem import SubSystemInterface
from Distributed_Design_Optimizer.middlelevel import MiddleLevelDataStorageInterface, MiddleLevelCouplingInterface


class CompromiseComputer:
    
    """
    CompromiseComputer computes the compromise metrics defined.
    Compromise metrics gives an idea how much the coupling variables moved from the intial points
    CompromiseComputer iterates through each edge of the Multi Di Graph and computes the compromise depending on the edge type
    Compromisee metrics are stored on the edges of the Master Graph
    """
    
    def __init__(self, graph_init: GraphInit, subsystems: List[SubSystemInterface], middlelevel_storages: List[MiddleLevelDataStorageInterface]):
        """Initialize the compromise computer.

        Args:
            graph_init: The graph initialization object.
            subsystems: List of all SubSystemInterface objects.
            middlelevel_storages: List of all MiddleLevelDataStorageInterface objects.
        """
        self._graph_init = graph_init
        self._mastergraph = graph_init.get_graph()
        self._subsystems: List[SubSystemInterface] = subsystems
        self._middlelevel_storages: List[MiddleLevelDataStorageInterface] = middlelevel_storages
        
        self._referenceflags: Dict[Tuple[str, str, str], bool] = {}
        # Store reference values per edge instead of globally
        self._referenceMappedResponseVariables: Dict[Tuple[str, str, str], List[float]] = {}
        self._referenceCouplingVariables: Dict[Tuple[str, str, str], List[float]] = {}
        self._referenceInconsistency: Dict[Tuple[str, str, str], List[float]] = {}
        self._referenceSharedVariables: Dict[Tuple[str, str, str], List[float]] = {}
        self._referenceTargetSharedVariables: Dict[Tuple[str, str, str], List[float]] = {}
        self._referenceSharedInconsistency: Dict[Tuple[str, str, str], List[float]] = {}
        
        
        # Create lookups for faster access
        self.create_subsystem_lookup()
        self.create_storage_lookup()
        
    def create_subsystem_lookup(self) -> None:
        """Create a lookup dictionary for Subsystems objects.
        """
        self._subsystem_lookup: Dict[str, SubSystemInterface] = {}
        
        for subsystem in self._subsystems:
            id = subsystem.get_SUBSYSTEMID()
            self._subsystem_lookup[id] = subsystem
            
    def create_storage_lookup(self) -> None:
        """Create a lookup dictionary for MiddleLevelDataStorageInterface objects."""
        self._storage_lookup: Dict[tuple, MiddleLevelDataStorageInterface] = {}
        
        for storage in self._middlelevel_storages:
            ids = storage.get_ID()
            # Store both directions for bidirectional lookup
            self._storage_lookup[(ids[0], ids[1])] = storage
            self._storage_lookup[(ids[1], ids[0])] = storage
            
    def compute_all_compromises(self) -> None:
        """Compute the compromises of each edge in the graph."""
        graph = self._mastergraph
        
        for u, v, key, data in graph.edges(keys=True, data=True):
            edge_type = data.get('type')
            self.compute_single_compromise(u, v, edge_type)
            
            
    def compute_single_compromise(self, idparent: str, idchild: str, edge_type: str) -> None:
        """Compute compromise metric for a single edge.

        Args:
            idparent: Parent node ID.
            idchild: Child node ID.
            edge_type: Type of edge.
        """
        # Get the corresponding MiddleLevelDataStorage
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
        
        parent_coupling: MiddleLevelCouplingInterface = None
        child_coupling: MiddleLevelCouplingInterface = None
        for idx, sid in enumerate(storage_ids):
            if sid.lower() == idparent.lower():
                parent_coupling = coupling_data[idx]
            elif sid.lower() == idchild.lower():
                child_coupling = coupling_data[idx]
        
        if parent_coupling is None or child_coupling is None:
            print(f"Warning: Missing coupling data for edge {idparent} -> {idchild}")
            return
        
        # Compute compromise based on edge type
        edge_data = self._mastergraph[idparent][idchild]
        edge_key = None
        
        # Find the correct edge key for this edge type
        for k, data in edge_data.items():
            if data.get('type') == edge_type:
                edge_key = k
                break
                
        if edge_key is None:
            print(f"Warning: Edge {idparent} -> {idchild} with type {edge_type} not found")
            return
            
        # Get the primal residual from the edge data
        primal_residual = None
        if edge_type == "decomposed_mappedresponse":
            primal_residual = edge_data[edge_key].get('primalmappedresidual')
        elif edge_type == "decomposed_shareddesignvariable":
            primal_residual = edge_data[edge_key].get('primalsharedresidual')
            
        if primal_residual is None:
            return            

        if edge_type == "decomposed_mappedresponse":
            self.compute_mapped_response_compromise(idparent, idchild, edge_type, edge_key, parent_coupling, child_coupling, primal_residual)
        elif edge_type == "decomposed_shareddesignvariable":
            self.compute_shared_design_compromise(idparent, idchild, edge_type, edge_key, parent_coupling, child_coupling, primal_residual)
            
    def compute_mapped_response_compromise(self, idparent: str, idchild: str, edge_type: str, edge_key: int,
                                          parent_coupling: MiddleLevelCouplingInterface, child_coupling: MiddleLevelCouplingInterface, primal_residual: List[float]) -> None:
        """Compute compromise metrics for mapped response variables.

        Args:
            idparent: Parent node ID.
            idchild: Child node ID.
            edge_type: Type of edge.
            edge_key: Edge key in the multigraph.
            parent_coupling: MiddleLevelCoupling object for parent.
            child_coupling: MiddleLevelCoupling object for child.
            primal_residual: List of primal residual values.
        """
        # Get current variable values
        parent_vars = parent_coupling.get_MappedResponses()
        child_vars = child_coupling.get_CouplingVariable()
        
        if parent_vars is None or child_vars is None:
            return
            
        parent_array = np.array(parent_vars)
        child_array = np.array(child_vars)
        parent_compromise = [None] * len(parent_array)
        child_compromise = [None] * len(child_array)
        
        edge_key_tuple = (idparent, idchild, edge_type)
        
        # If this is the first time we've seen a non-zero residual for this edge, store reference values
        if edge_key_tuple not in self._referenceflags:
            if np.all(primal_residual != 0):
                self._referenceflags[edge_key_tuple] = True
                self._referenceMappedResponseVariables[edge_key_tuple] = parent_vars.copy()            
                self._referenceCouplingVariables[edge_key_tuple] = child_vars.copy()
                self._referenceInconsistency[edge_key_tuple] = primal_residual
                # Added so that GUI can plot the lines
                self._mastergraph[idparent][idchild][edge_key]['parent_mapped_compromise'] = parent_compromise
                self._mastergraph[idparent][idchild][edge_key]['child_mapped_compromise'] = child_compromise
            return
        
        # Use high-precision Decimal for subtraction to capture small differences
        
        if edge_key_tuple in self._referenceMappedResponseVariables and edge_key_tuple in self._referenceCouplingVariables and self._referenceInconsistency[edge_key_tuple] is not None:

            parent_diff = np.array(self._referenceMappedResponseVariables[edge_key_tuple]) - parent_array
            child_diff =  child_array - np.array(self._referenceCouplingVariables[edge_key_tuple])
            
            parent_compromise = parent_diff / np.abs(self._referenceInconsistency[edge_key_tuple])
            child_compromise = child_diff / np.abs(self._referenceInconsistency[edge_key_tuple])
            # Store the compromise metrics in the graph
            self._mastergraph[idparent][idchild][edge_key]['parent_mapped_compromise'] = parent_compromise.tolist()
            self._mastergraph[idparent][idchild][edge_key]['child_mapped_compromise'] = child_compromise.tolist()
            
    def compute_shared_design_compromise(self, idparent: str, idchild: str, edge_type: str, edge_key: int,
                                        parent_coupling: MiddleLevelCouplingInterface, child_coupling: MiddleLevelCouplingInterface, primal_residual: List[float]) -> None:
        """Compute compromise metrics for shared design variables.

        Args:
            idparent: Parent node ID.
            idchild: Child node ID.
            edge_type: Type of edge.
            edge_key: Edge key in the multigraph.
            parent_coupling: MiddleLevelCoupling object for parent.
            child_coupling: MiddleLevelCoupling object for child.
            primal_residual: List of primal residual values.
        """
        # Get current variable values
        if self._subsystems[0].get_OuterLoop_Itr() > 5:
            print('STOP NOW')
        
        parent_vars = parent_coupling.get_SharedDesignVariables()
        child_vars = child_coupling.get_TargetSharedDesignVariables()
        
        
        
        if parent_vars is None or child_vars is None:
            raise ValueError("Expected Shared Design variables/TargetSharedDesign variables in CompromiseComputer.compute_shared_design_compromise()")
            
        parent_array = np.array(parent_vars)
        child_array = np.array(child_vars)
        
        parent_compromise = [None] * len(parent_array)
        child_compromise = [None] * len(child_array)
        
        edge_key_tuple = (idparent, idchild, edge_type)
        
        # If this is the first time we've seen a non-zero residual for this edge, store reference values
        if edge_key_tuple not in self._referenceflags:
            if not np.allclose(primal_residual, [0.0] * len(primal_residual)):
                self._referenceflags[edge_key_tuple] = True
                self._referenceSharedVariables[edge_key_tuple] = parent_vars.copy()
                self._referenceTargetSharedVariables[edge_key_tuple] = child_vars.copy()
                self._referenceSharedInconsistency[edge_key_tuple] = primal_residual
                # Added so that GUI can plot the lines
                self._mastergraph[idparent][idchild][edge_key]['parent_mapped_compromise'] = parent_compromise
                self._mastergraph[idparent][idchild][edge_key]['child_mapped_compromise'] = child_compromise
            return

        if edge_key_tuple in self._referenceSharedVariables and edge_key_tuple in self._referenceTargetSharedVariables and self._referenceSharedInconsistency[edge_key_tuple] is not None:
            
            # Where residual is non-zero, calculate compromise
            
            parent_diff = np.array(self._referenceSharedVariables[edge_key_tuple]) - parent_array
            child_diff = child_array - np.array(self._referenceTargetSharedVariables[edge_key_tuple])
            
            # Calculate compromise ratio (how much each side moved divided by initial inconsistency)
            parent_compromise = parent_diff / np.abs(self._referenceSharedInconsistency[edge_key_tuple])
            child_compromise = child_diff / np.abs(self._referenceSharedInconsistency[edge_key_tuple])
            
            # Store the compromise metrics in the graph
            self._mastergraph[idparent][idchild][edge_key]['parent_shared_compromise'] = parent_compromise.tolist()
            self._mastergraph[idparent][idchild][edge_key]['child_shared_compromise'] = child_compromise.tolist()
    
    def get_compromise_summary(self) -> Dict:
        """
        Get a comprehensive summary of computed compromise metrics.
        
        Returns:
            dict: Summary of compromise metrics for all edges
        """
        graph = self._mastergraph
        summary = {"edges": {}}
        
        for u, v, key, data in graph.edges(keys=True, data=True):
            edge_id = f"{u}-{v}"
            edge_type = data.get('type', 'unknown')
            
            if not edge_type.startswith('decomposed'):
                continue
                
            parent_compromise = None
            child_compromise = None
            
            if edge_type == "decomposed_mappedresponse":
                parent_compromise = data.get('parent_mapped_compromise')
                child_compromise = data.get('child_mapped_compromise')
            elif edge_type == "decomposed_shareddesignvariable":
                parent_compromise = data.get('parent_shared_compromise')
                child_compromise = data.get('child_shared_compromise')
            
            summary["edges"][edge_id] = {
                "id": edge_id,
                "type": edge_type,
                "parent_compromise": parent_compromise,
                "child_compromise": child_compromise
            }
            
        return summary
    
    def interpret_CompromiseRatio(self) -> list:
        """Return formatted interpretation text for the Compromise Ratio chart.

        Returns:
            List of tuples containing text, style tag, and phrases to bold.
        """
        interpretation_data = [
            ("Compromise Ratio\n", "h3", ["Compromise Ratio"]),
            
            ("This line chart tracks the Compromise Ratio for a coupled pair of subsystems, revealing which subsystem is making a greater effort to resolve their shared disagreement.\n", "body", []),
            
            ("Interpretation\n", "h4", []),
            
            ("•  Horizontal Axis (X-axis): Represents the Iteration Number (time).\n", "bullet_item", 
             ["Horizontal Axis (X-axis)", "Iteration Number"]),
             
            ("•  Vertical Axis (Y-axis): Represents the Compromise Ratio.\n", "bullet_item", 
             ["Vertical Axis (Y-axis)", "Compromise Ratio"]),
             
            ("•  Lines: This graph plots two lines for a single coupling:\n", "bullet_item", 
             ["Lines"]),
            
            # Sub-bullet items. We'll indent these further using a new tag or by modifying lmargin.
            # For simplicity, let's create a new 'sub_bullet_item' tag.
            # You'll need to add this tag to your GUI's setup.
            
            ("    - Parent Line: Shows the compromise from the parent subsystem.\n", "sub_bullet_item", 
             ["Parent Line"]),
             
            ("    - Child Line: Shows the compromise from the child subsystem.\n", "sub_bullet_item", 
             ["Child Line"]),

            ("•  Compromise Ratio: This metric is calculated once a disagreement (or \"inconsistency\") appears. It measures how much a subsystem has moved its variable from its initial position, as a fraction of the total initial disagreement. A value of 0.5 means that subsystem has \"given in\" or moved by an amount equal to 50% of the initial inconsistency.\n", "bullet_item", 
             ["Compromise Ratio", "moved its variable from its initial position", "total initial disagreement"]),

            ("How to Interpret\n", "h4", []),
            
            ("This graph exposes the \"negotiation\" and \"stubbornness\" in your system's coordination. By comparing the two lines, you can see which subsystem is more flexible.\n", "body", []),
            
            ("•  Symmetric Compromise (Both lines rise to ~0.5): This is an ideal, balanced negotiation. Both subsystems are \"meeting in the middle\" and contributing equally to resolve the conflict. 🤝\n", "bullet_item", 
             ["Symmetric Compromise (Both lines rise to ~0.5)", "balanced negotiation"]),
             
            ("•  Asymmetric Compromise (One line is high, one is low): This reveals a rigid or inflexible subsystem.\n", "bullet_item", 
             ["Asymmetric Compromise (One line is high, one is low)"]),
             
            ("    - If the Parent line is high and the Child line is low: The Parent is doing all the work to compromise. The Child's design or constraints are \"stubborn\" and are not adapting.\n", "sub_bullet_item", 
             ["Parent is doing all the work"]),
             
            ("    - If the Child line is high and the Parent line is low: The Child is making the sacrifice, while the Parent remains rigid.\n", "sub_bullet_item", 
             ["Child is making the sacrifice"]),

            ("•  No Compromise (Both lines stay low): This indicates a gridlock. Neither subsystem is moving to resolve the conflict, and the algorithm is stuck. This points to a fundamental incompatibility or flawed constraint in the decomposition. 🛑\n", "bullet_item", 
             ["No Compromise (Both lines stay low)", "gridlock"])
        ]
        return interpretation_data        




```
