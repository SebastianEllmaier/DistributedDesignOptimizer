---
title: InConsistencyOscillationComputer (Source)
---

← Back to [InConsistencyOscillationComputer documentation](InConsistencyOscillationComputer.md)

# InConsistencyOscillationComputer - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\InConsistencyOscillationComputer.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""InConsistency oscillation computation module.

This module provides functionality for computing and analyzing oscillations
in inconsistencies during distributed optimization.
"""

from typing import List,  Any, Dict, Optional
import numpy as np
import pywt
from Distributed_Design_Optimizer.postprocess import GraphInit
from Distributed_Design_Optimizer.subsystem import SubSystemInterface
from Distributed_Design_Optimizer.middlelevel import InConsistencySizeInterface



class InConsistencyOscillationComputer:
    """
    InConsistencyOscillationComputer computes the oscillation energy to understand the behaviour of Inconsistency Convergence.
    Oscillation Energy is computed through Wavelet Transformation which studies the Inconsistency through frequency domain.
    InConsistencyOscillation Metrics values are computed once the enough data (horizon) is attained.
    
    """
    
    def __init__(self, graph_init: GraphInit, subsystems: List[SubSystemInterface]):
        """Initialize the InConsistencyOscillationComputer.

        Args:
            graph_init: GraphInit object containing the master graph.
            subsystems: List of SubSystemInterface objects.
        """
        self._graph_init = graph_init
        self._mastergraph = graph_init.get_graph()
        self._horizon = 3  # Default value
        self._wavelet_type = 'haar' # used for limited data, simple wavelet
        self._wavelet_results = {}
        self._subsystems = subsystems
        
        # Create lookups for faster access
        self.create_subsystem_lookup()
        
    def create_subsystem_lookup(self) -> None:
        """Create a lookup dictionary for Subsystems objects.
        """
        self._subsystem_lookup: Dict[str, SubSystemInterface] = {}
        
        for subsystem in self._subsystems:
            id = subsystem.get_SUBSYSTEMID()
            self._subsystem_lookup[id] = subsystem
        
    def get_Horizon(self) -> int:
        """Get the horizon value for wavelet transform.

        Returns:
            The number of previous values to use.
        """
        return self._horizon
        
    def set_Horizon(self, horizon: int) -> None:
        """Set the number of previous values to use for wavelet transform.

        Args:
            horizon: The number of previous values to use.
        """
        self._horizon = horizon
        
    def compute_wavelet_transforms(self, all_history_entries: List[dict] | None) -> None:
        """Compute wavelet transforms for all edges in the master graph.

        Args:
            all_history_entries: List of history entries containing residual data, or None.
        """
        graph = self._mastergraph
        self._wavelet_results = {}
                
        # check if enough primal residual history data is available for the wavelet tranform computation
        if all_history_entries is None:
            for u, v, data in graph.edges(data= True):
                edge_type = data.get('type', 'unknown')
                
                # Get the appropriate residual data to determine length
                residual_data = None
                if edge_type == "decomposed_mappedresponse":
                    residual_data = data.get('primalmappedresidual')
                elif edge_type == "decomposed_shareddesignvariable":
                    residual_data = data.get('primalsharedresidual')
                
                # Skip if no residual data found
                if residual_data is None:
                    continue
                    
                none_values = [None] * len(residual_data)
                
                parent_inconsistencies: List[InConsistencySizeInterface] = self._subsystem_lookup.get(u).get_Inconsistencies()
                child_inconsistencies: List[InConsistencySizeInterface] = self._subsystem_lookup.get(v).get_Inconsistencies()                
                # set the oscillation index from parents prespective
                if edge_type == "decomposed_mappedresponse":
                    for inconsistency in parent_inconsistencies:
                        if inconsistency.get_ID() == v:
                            inconsistency.set_OscillationIndex_MappedResponse_Minus_CopyCouplingVariable(oscillationindex=none_values)
                elif edge_type == "decomposed_shareddesignvariable":
                    for inconsistency in parent_inconsistencies:
                        if inconsistency.get_ID() == v:
                            inconsistency.set_OscillationIndex_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(oscillationindex=none_values)
                            
                # set the oscillation index from child prespective
                if edge_type == "decomposed_mappedresponse":
                    for inconsistency in child_inconsistencies:
                        if inconsistency.get_ID() == u:
                            inconsistency.set_OscillationIndex_CopyMappedResponse_Minus_CouplingVariable(oscillationindex=none_values)
                elif edge_type == "decomposed_shareddesignvariable":
                    for inconsistency in child_inconsistencies:
                        if inconsistency.get_ID() == u:
                            inconsistency.set_OscillationIndex_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(oscillationindex=none_values)
                            
                reformatted_data = {f"{u}_{v}_{i}": None for i in range(len(residual_data))}
                self._graph_init.store_InConsistencyOscillationIndex(u, v, edge_type, reformatted_data)
            return

        for u, v, key, data in graph.edges(keys=True, data=True):
            edge_id = f"{u}-{v}"
            edge_type = data.get('type')
            
            edge_primalresidual_history = self.compute_EdgeResidualHistory(all_history_entries, 
                                                                        self._horizon, 
                                                                        edge_id, 
                                                                        edge_type)
                                                                    

            # Initialize wavelet_coeffs to None by default
            wavelet_coeffs = [None] 
            
            # Only compute wavelet transform if we have sufficient history data
            if edge_primalresidual_history is not None and len(edge_primalresidual_history) == self._horizon:            
                wavelet_coeffs = self._compute_edge_wavelet_transform(edge_primalresidual_history)
            
            # Store results
            self._wavelet_results[(u, v, edge_type)] = {
                'edge_id': edge_id,
                'edge_type': edge_type,
                'wavelet_coeffs': wavelet_coeffs
            }
            
            # Store in graph for visualization
            self._store_wavelet_in_graph(u, v, key, edge_type, wavelet_coeffs)
            
    def compute_EdgeResidualHistory(self, all_primalresidual_history: List[dict], k: int, edge_id: str, edge_type: str) -> List | None:
        """Return the edge primal residual history for a specific edge and type.

        Args:
            all_primalresidual_history: List of history entries containing residual data.
            k: Number of previous values required.
            edge_id: Edge identifier in format "idparent-idchild".
            edge_type: Type of edge.

        Returns:
            List of primal residual values for the specified edge, or None if not enough data.
        """
        edge_primalresidual_history: List = []
        
        for history_entry in all_primalresidual_history:
            # Extract residuals from history entry
            all_residuals = history_entry.get("residuals", {})
            
            if edge_id in all_residuals:
                edge_data = all_residuals[edge_id]
                
                if edge_type is not None and edge_data.get("type") != edge_type:
                    continue                
                
                # Get the primal residual values
                if "primal_residuals" in edge_data:
                    edge_primalresidual_history.append(edge_data["primal_residuals"])
        
        # Return None if we don't have enough data
        if len(edge_primalresidual_history) < k:
            return None
        
        # Return only the k most recent entries
        return edge_primalresidual_history[:k]
        
    
    def _compute_edge_wavelet_transform(self, residual_history: List[List[float]]):
        """
        Compute wavelet transform for a single edge's residual history.
        
        Args:
            residual_history: List of residual value lists
            
        Returns:
            dict: Dictionary of wavelet coefficients for each component
        """
        wavelet_results = {}
        
        # Handle potentially having different lengths of residuals for each iteration
        # by computing wavelet transform for each component
            
        num_components = len(residual_history[0])
        
        # Process each component separately
        for component_idx in range(num_components):
            # Extract the time series for this component
            try:
                component_series = [res[component_idx] for res in residual_history if component_idx < len(res)]
                
                if len(component_series) < self._horizon:
                    continue
                
                # Convert to numpy array and ensure it's 1D
                data = np.array(component_series).flatten()
                
                # Compute wavelet decomposition
                # Discreet wavelet used as continuous wavelet transforms demands more data points for computation
                # Level Decompositon of signals restricted to look into high, medium and smoothness information with limited data
                coeffs = pywt.wavedec(data, self._wavelet_type, level=min(2, pywt.dwt_max_level(len(data), self._wavelet_type)))
                
                # Calculate energy metrics
                # coeffs[0] is a low filter pass, computing low frequency
                approximation_energy = np.sum(np.square(coeffs[0]))
                
                # Detail coefficients represent high frequency components
                # coeffs[1], coeffs[2] are high filter passes, which get the high frequency values
                detail_energies = [np.sum(np.square(detail)) for detail in coeffs[1:]]
                high_frequency_energy = sum(detail_energies)
                
                # Total energy is the sum of approximation and all detail energies
                total_energy = approximation_energy + high_frequency_energy
                
                # Calculate oscillatory index: ratio of high frequency energy to total energy
                # High Values: Rapid Oscillations
                # Low Values: Slow and Smooth 
                oscillatory_index = high_frequency_energy / total_energy if total_energy > 0 else 0
                
                # Store the coefficients and energy metrics
                wavelet_results[component_idx] = float(oscillatory_index)
            except Exception as e:
                print(f"Error computing wavelet for component {component_idx}: {str(e)}")
                continue
                
        return wavelet_results
    
    def _store_wavelet_in_graph(self, u, v, key, edge_type, wavelet_coeffs):
        """
        Store wavelet transform results in the graph for a specific edge.
        
        Args:
            u: Source node ID
            v: Target node ID
            key: Edge key
            edge_type: Edge type
            wavelet_coeffs: Computed wavelet coefficients containing oscillatory indices
        """
        # Get the edge data to determine the length for None values when needed
        edge_data = self._mastergraph.get_edge_data(u, v, key)
        
        # Determine the residual data length based on edge type
        residual_length = 0
        if edge_data:
            if edge_type == "decomposed_mappedresponse" and 'primalmappedresidual' in edge_data:
                residual_length = len(edge_data['primalmappedresidual'])
            elif edge_type == "decomposed_shareddesignvariable" and 'primalsharedresidual' in edge_data:
                residual_length = len(edge_data['primalsharedresidual'])
        
        if key is not None and wavelet_coeffs is not None:
        # Restructure the data to match the expected format
        # Instead of component_0, component_1, etc. keys, use a more direct structure
            reformatted_data = {}
            
            for component_idx, oscillatory_index in wavelet_coeffs.items():
                reformatted_data[f"{u}_{v}_{component_idx}"] = oscillatory_index
            
            # Use the GraphInit method to store the oscillation index data
            self._graph_init.store_InConsistencyOscillationIndex(u, v, edge_type, reformatted_data)
            
            # InConsistencyOscillation is computed for every coupling link
            # store it in the Inconsistency size of the respective subsystem
            parent_inconsistencies: List[InConsistencySizeInterface] = self._subsystem_lookup.get(u).get_Inconsistencies()
            child_inconsistencies: List[InConsistencySizeInterface] = self._subsystem_lookup.get(v).get_Inconsistencies()
            
            oscillation_values = list(reformatted_data.values())
            
            # set the oscillation index from parents prespective
            if edge_type == "decomposed_mappedresponse":
                for inconsistency in parent_inconsistencies:
                    if inconsistency.get_ID() == v:
                        inconsistency.set_OscillationIndex_MappedResponse_Minus_CopyCouplingVariable(oscillationindex=oscillation_values)
            elif edge_type == "decomposed_shareddesignvariable":
                for inconsistency in parent_inconsistencies:
                    if inconsistency.get_ID() == v:
                        inconsistency.set_OscillationIndex_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(oscillationindex=oscillation_values)
                        
            # set the oscillation index from child prespective
            if edge_type == "decomposed_mappedresponse":
                for inconsistency in child_inconsistencies:
                    if inconsistency.get_ID() == u:
                        inconsistency.set_OscillationIndex_CopyMappedResponse_Minus_CouplingVariable(oscillationindex=oscillation_values)
            elif edge_type == "decomposed_shareddesignvariable":
                for inconsistency in child_inconsistencies:
                    if inconsistency.get_ID() == u:
                        inconsistency.set_OscillationIndex_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(oscillationindex=oscillation_values)
        else:
            # When wavelet_coeffs is None, we need to set [None] * len(residual_data) for all inconsistencies
            if residual_length > 0:
                none_values = [None] * residual_length
                
                parent_inconsistencies: List[InConsistencySizeInterface] = self._subsystem_lookup.get(u).get_Inconsistencies()
                child_inconsistencies: List[InConsistencySizeInterface] = self._subsystem_lookup.get(v).get_Inconsistencies()
                
                # set the oscillation index from parents prespective
                if edge_type == "decomposed_mappedresponse":
                    for inconsistency in parent_inconsistencies:
                        if inconsistency.get_ID() == v:
                            inconsistency.set_OscillationIndex_MappedResponse_Minus_CopyCouplingVariable(oscillationindex=none_values)
                elif edge_type == "decomposed_shareddesignvariable":
                    for inconsistency in parent_inconsistencies:
                        if inconsistency.get_ID() == v:
                            inconsistency.set_OscillationIndex_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(oscillationindex=none_values)
                            
                # set the oscillation index from child prespective
                if edge_type == "decomposed_mappedresponse":
                    for inconsistency in child_inconsistencies:
                        if inconsistency.get_ID() == u:
                            inconsistency.set_OscillationIndex_CopyMappedResponse_Minus_CouplingVariable(oscillationindex=none_values)
                elif edge_type == "decomposed_shareddesignvariable":
                    for inconsistency in child_inconsistencies:
                        if inconsistency.get_ID() == u:
                            inconsistency.set_OscillationIndex_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(oscillationindex=none_values)
            

                   
    
    def get_InConsistencyOscillationIndex_summary(self) -> Dict:
        """Get a simplified summary of computed oscillation indices.

        Returns:
            Summary of oscillation indices for all edges in a flat structure.
        """
        graph = self._mastergraph
        summary = {}
        
        for u, v, key, data in graph.edges(keys=True, data=True):
            edge_id = f"{u}-{v}"
            edge_type = data.get('type', 'unknown')
            
            # Skip non-decomposed edges
            if not edge_type.startswith('decomposed'):
                continue
                
            # Initialize this edge in the summary if not already present
            if edge_id not in summary:
                summary[edge_id] = {}
            
            # Find corresponding wavelet data in self._wavelet_results
            wavelet_key = (u, v, edge_type)
            if wavelet_key in self._wavelet_results:
                wavelet_data = self._wavelet_results[wavelet_key]
                
                # Extract oscillation metrics from wavelet data
                if 'wavelet_coeffs' in wavelet_data and wavelet_data['wavelet_coeffs']:
                    for component_idx, oscillatory_index in wavelet_data['wavelet_coeffs'].items():
                        component_id = f"{u}_{v}_{component_idx}"
                        summary[component_id] = oscillatory_index
        
        return summary
    
    
    def interpret_InConsistencyOscillationMetric(self) -> list:
        """Return formatted interpretation text for the InConsistency Oscillation Metric.

        Returns:
            List of tuples containing text, style tag, and phrases to bold.
        """
        interpretation_data = [
            ("InConsistency Oscillation Metric\n", "h3", ["Oscillatory Index"], []),
            
            ("This line chart tracks the Oscillatory Index over time, revealing the stability and nature of the convergence process.\n", "body", 
             [], ["stability", "nature"]),
            
            ("Interpretation\n", "h4", [], []),
            
            ("•  Horizontal Axis (X-axis): Represents the Iteration Number (time).\n", "bullet_item", 
             ["Horizontal Axis (X-axis)", "Iteration Number"], []),
             
            ("•  Vertical Axis (Y-axis): Represents the Oscillatory Index.\n", "bullet_item", 
             ["Vertical Axis (Y-axis)", "Oscillatory Index"], []),
             
            ("•  Oscillatory Index: This metric is calculated using a Wavelet Transform on the disagreement data. It measures the ratio of high-frequency energy (rapid, spiky changes) to the total energy (all changes).\n", "bullet_item", 
             ["Oscillatory Index", "Wavelet Transform", "high-frequency energy (rapid, spiky changes)", "total energy (all changes)"], []),

            ("    - A value of None may appear at the beginning of the plot, as the calculation requires a minimum history of data.\n", "sub_bullet_item", 
             ["None"], []),

            ("How to Interpret\n", "h4", [], []),
            
            ("This graph diagnoses how the system is converging, not just if it is converging. It provides organizational insight into the efficiency of the coordination.\n", "body", 
             [], ["how", "if"]),
            
            ("•  High Index Value (High \"Roughness\"): This indicates unstable, \"choppy,\" or rough convergence. The disagreement isn't decreasing smoothly; instead, it's oscillating rapidly.\n", "bullet_item", 
             ["High Index Value (High \"Roughness\")", "unstable, \"choppy,\" or rough convergence"], []),
             
            ("    - Organizational Insight: This suggests high coordination overhead or \"thrashing.\" The subsystems are likely making rapid, conflicting adjustments that may be creating new problems as they solve old ones. The process is inefficient and \"fighting itself\" to reach a solution.\n", "sub_bullet_item", 
             ["coordination overhead", "thrashing"], []),
             
            ("•  Low Index Value (High \"Smoothness\"): This indicates stable, smooth, and predictable convergence. The disagreement is being resolved steadily without erratic spikes.\n", "bullet_item", 
             ["Low Index Value (High \"Smoothness\")", "stable, smooth, and predictable convergence"], []),

            ("    - Organizational Insight: This is the ideal state. It shows the coordination algorithm and system decomposition are working in harmony. The \"conversation\" between subsystems is efficient, and progress is steady. 📈\n", "sub_bullet_item", 
             [], []),
             
            ("What to look for: An ideal process might start with a high index (as conflicts are first identified) but should quickly trend downwards to a low, stable value. A persistently high or spiky line signals a deeply inefficient or unstable coordination process that needs review.\n", "body", 
             [], [])
        ]
        return interpretation_data


















# from typing import List,  Any, Dict
# import numpy as np
# import pywt
# from Distributed_Design_Optimizer.postprocess.GraphInit import GraphInit
# from Distributed_Design_Optimizer.subsystem import SubSystemInterface
# from Distributed_Design_Optimizer.middlelevel.InConsistencySizeInterface import InConsistencySizeInterface



# class InConsistencyOscillationComputer:
#     """
#     InConsistencyOscillationComputer computes the oscillation energy to understand the behaviour of Inconsistency Convergence.
#     Oscillation Energy is computed through Wavelet Transformation which studies the Inconsistency through frequency domain.
#     InConsistencyOscillation Metrics values are computed once the enough data (horizon) is attained.
    
#     """
    
#     def __init__(self, graph_init: GraphInit, subsystems: List[SubSystemInterface]):
#         """
#         Initialize the wavelet computer.
        
#         Args:
#             graph_init: GraphInit object containing the master graph
#             coordinator: Coordinator object with access to history
#             horizon: Number of previous values to use for wavelet transform
#             wavelet_type: Wavelet type to use (default: 'morelet')
#         """
#         self._graph_init = graph_init
#         self._mastergraph = graph_init.get_graph()
#         self._horizon = 3  # Default value
#         self._wavelet_type = 'haar' # used for limited data, simple wavelet
#         self._wavelet_results = {}
#         self._subsystems = subsystems
        
#         # Create lookups for faster access
#         self.create_subsystem_lookup()
        
#     def create_subsystem_lookup(self) -> None:
#         """Create a lookup dictionary for Subsystems objects.
#         """
#         self._subsystem_lookup: Dict[str, SubSystemInterface] = {}
        
#         for subsystem in self._subsystems:
#             id = subsystem.get_SUBSYSTEMID()
#             self._subsystem_lookup[id] = subsystem
        
#     def get_Horizon(self) -> int:
#         """_summary_

#         Returns:
#             int: _description_
#         """
#         return self._horizon
        
#     def set_Horizon(self, horizon: int):
#         """Set the number of previous values to use for wavelet transform"""
#         self._horizon = horizon
        
#     def compute_wavelet_transforms(self, all_history_entries: List[dict] | None):
#         """
#         Compute wavelet transforms for all edges in the master graph.
        
#         Iterates through all edges, retrieves previous primal residual values,
#         and computes wavelet transforms for each edge.
#         """
#         graph = self._mastergraph
#         self._wavelet_results = {}
                
#         # check if enough primal residual history data is available for the wavelet tranform computation
#         if all_history_entries is None:
#             for u, v, data in graph.edges(data= True):
#                 edge_type = data.get('type', 'unknown')
#                 parent_inconsistencies: List[InConsistencySizeInterface] = self._subsystem_lookup.get(u).get_Inconsistencies()
#                 child_inconsistencies: List[InConsistencySizeInterface] = self._subsystem_lookup.get(v).get_Inconsistencies()                
#                 # set the oscillation index from parents prespective
#                 if edge_type == "decomposed_mappedresponse":
#                     for inconsistency in parent_inconsistencies:
#                         if inconsistency.get_ID() == v:
#                             inconsistency.set_OscillationIndex_MappedResponse_Minus_CopyCouplingVariable(oscillationindex=list([None] * len(data.get('primalmappedresidual'))))
#                 elif edge_type == "decomposed_shareddesignvariable":
#                     for inconsistency in parent_inconsistencies:
#                         if inconsistency.get_ID() == v:
#                             inconsistency.set_OscillationIndex_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(oscillationindex=list([None] * len(data.get('primalsharedresidual'))))
                            
#                 # set the oscillation index from child prespective
#                 if edge_type == "decomposed_mappedresponse":
#                     for inconsistency in child_inconsistencies:
#                         if inconsistency.get_ID() == u:
#                             inconsistency.set_OscillationIndex_CopyMappedResponse_Minus_CouplingVariable(oscillationindex=list([None] * len(data.get('primalmappedresidual'))))
#                 elif edge_type == "decomposed_shareddesignvariable":
#                     for inconsistency in child_inconsistencies:
#                         if inconsistency.get_ID() == u:
#                             inconsistency.set_OscillationIndex_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(oscillationindex=list([None] * len(data.get('primalsharedresidual'))))
                
#                 return
                        

                    

#         for u, v, key, data in graph.edges(keys=True, data=True):
#             edge_id = f"{u}-{v}"
#             edge_type = data.get('type')
            
#             edge_primalresidual_history = self.compute_EdgeResidualHistory(all_history_entries, 
#                                                                         self._horizon, 
#                                                                         edge_id, 
#                                                                         edge_type)
                                                                    

#             # Initialize wavelet_coeffs to None by default
#             wavelet_coeffs = None
            
#             # Only compute wavelet transform if we have sufficient history data
#             if edge_primalresidual_history is not None and len(edge_primalresidual_history) == self._horizon:            
#                 wavelet_coeffs = self._compute_edge_wavelet_transform(edge_primalresidual_history)
            
#             # Store results
#             self._wavelet_results[(u, v, edge_type)] = {
#                 'edge_id': edge_id,
#                 'edge_type': edge_type,
#                 'wavelet_coeffs': wavelet_coeffs
#             }
            
#             # Store in graph for visualization
#             self._store_wavelet_in_graph(u, v, key, edge_type, wavelet_coeffs)
            
#     def compute_EdgeResidualHistory(self, all_primalresidual_history, k: int, edge_id, edge_type) -> List | None:
        
#         """Return the edge primal residual history for a specific edge and type
    
#     Args:
#         all_primalresidual_history: List of history entries containing residual data
#         k: Number of previous values required
#         edge_id: Edge identifier in format "idparent-idchild"
#         edge_type: Type of edge
        
#     Returns:
#         List: List of primal residual values for the specified edge or None if not enough data
#     """
#         edge_primalresidual_history: List = []
        
#         for history_entry in all_primalresidual_history:
#             # Extract residuals from history entry
#             all_residuals = history_entry.get("residuals", {})
            
#             if edge_id in all_residuals:
#                 edge_data = all_residuals[edge_id]
                
#                 if edge_type is not None and edge_data.get("type") != edge_type:
#                     continue                
                
#                 # Get the primal residual values
#                 if "primal_residuals" in edge_data:
#                     edge_primalresidual_history.append(edge_data["primal_residuals"])
        
#         # Return None if we don't have enough data
#         if len(edge_primalresidual_history) < k:
#             return [None] * len(edge_primalresidual_history[0])
        
#         # Return only the k most recent entries
#         return edge_primalresidual_history[:k]
        
    
#     def _compute_edge_wavelet_transform(self, residual_history: List[List[float]]):
#         """
#         Compute wavelet transform for a single edge's residual history.
        
#         Args:
#             residual_history: List of residual value lists
            
#         Returns:
#             dict: Dictionary of wavelet coefficients for each component
#         """
#         wavelet_results = {}
        
#         # Handle potentially having different lengths of residuals for each iteration
#         # by computing wavelet transform for each component
            
#         num_components = len(residual_history[0])
        
#         # Process each component separately
#         for component_idx in range(num_components):
#             # Extract the time series for this component
#             try:
#                 component_series = [res[component_idx] for res in residual_history if component_idx < len(res)]
                
#                 if len(component_series) < self._horizon:
#                     continue
                
#                 # Convert to numpy array and ensure it's 1D
#                 data = np.array(component_series).flatten()
                
#                 # Compute wavelet decomposition
#                 # Discreet wavelet used as continuous wavelet transforms demands more data points for computation
#                 # Level Decompositon of signals restricted to look into high, medium and smoothness information with limited data
#                 coeffs = pywt.wavedec(data, self._wavelet_type, level=min(2, pywt.dwt_max_level(len(data), self._wavelet_type)))
                
#                 # Calculate energy metrics
#                 # coeffs[0] is a low filter pass, computing low frequency
#                 approximation_energy = np.sum(np.square(coeffs[0]))
                
#                 # Detail coefficients represent high frequency components
#                 # coeffs[1], coeffs[2] are high filter passes, which get the high frequency values
#                 detail_energies = [np.sum(np.square(detail)) for detail in coeffs[1:]]
#                 high_frequency_energy = sum(detail_energies)
                
#                 # Total energy is the sum of approximation and all detail energies
#                 total_energy = approximation_energy + high_frequency_energy
                
#                 # Calculate oscillatory index: ratio of high frequency energy to total energy
#                 # High Values: Rapid Oscillations
#                 # Low Values: Slow and Smooth 
#                 oscillatory_index = high_frequency_energy / total_energy if total_energy > 0 else 0
                
#                 # Store the coefficients and energy metrics
#                 wavelet_results[component_idx] = float(oscillatory_index)
#             except Exception as e:
#                 print(f"Error computing wavelet for component {component_idx}: {str(e)}")
#                 continue
                
#         return wavelet_results
    
#     def _store_wavelet_in_graph(self, u, v, key, edge_type, wavelet_coeffs):
#         """
#         Store wavelet transform results in the graph for a specific edge.
        
#         Args:
#             u: Source node ID
#             v: Target node ID
#             key: Edge key
#             edge_type: Edge type
#             wavelet_coeffs: Computed wavelet coefficients containing oscillatory indices
#         """
#         if key is not None and wavelet_coeffs is not None:
#         # Restructure the data to match the expected format
#         # Instead of component_0, component_1, etc. keys, use a more direct structure
#             reformatted_data = {}
            
#             for component_idx, oscillatory_index in wavelet_coeffs.items():
#                 reformatted_data[f"{u}_{v}_{component_idx}"] = oscillatory_index
            
#             # Use the GraphInit method to store the oscillation index data
#             self._graph_init.store_InConsistencyOscillationIndex(u, v, edge_type, reformatted_data)
            
#             # InConsistencyOscillation is computed for every coupling link
#             # store it in the Inconsistency size of the respective subsystem
#             parent_inconsistencies: List[InConsistencySizeInterface] = self._subsystem_lookup.get(u).get_Inconsistencies()
#             child_inconsistencies: List[InConsistencySizeInterface] = self._subsystem_lookup.get(v).get_Inconsistencies()
            
#             # set the oscillation index from parents prespective
#             if edge_type == "decomposed_mappedresponse":
#                 for inconsistency in parent_inconsistencies:
#                     if inconsistency.get_ID() == v:
#                         inconsistency.set_OscillationIndex_MappedResponse_Minus_CopyCouplingVariable(oscillationindex=list(reformatted_data.values()))
#             elif edge_type == "decomposed_shareddesignvariable":
#                 for inconsistency in parent_inconsistencies:
#                     if inconsistency.get_ID() == v:
#                         inconsistency.set_OscillationIndex_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(oscillationindex=list(reformatted_data.values()))
                        
#             # set the oscillation index from child prespective
#             if edge_type == "decomposed_mappedresponse":
#                 for inconsistency in child_inconsistencies:
#                     if inconsistency.get_ID() == u:
#                         inconsistency.set_OscillationIndex_CopyMappedResponse_Minus_CouplingVariable(oscillationindex=list(reformatted_data.values()))
#             elif edge_type == "decomposed_shareddesignvariable":
#                 for inconsistency in child_inconsistencies:
#                     if inconsistency.get_ID() == u:
#                         inconsistency.set_OscillationIndex_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(oscillationindex=list(reformatted_data.values()))
            

                   
    
#     def get_InConsistencyOscillationIndex_summary(self):
#         """
#         Get a simplified summary of computed oscillation indices.
        
#         Returns:
#             dict: Summary of oscillation indices for all edges in a flat structure:
#             {
#                 edge_id: {
#                     'component_id': oscillatory_index,
#                     ...
#                 },
#                 ...
#             }
#         """
#         graph = self._mastergraph
#         summary = {}
        
#         for u, v, key, data in graph.edges(keys=True, data=True):
#             edge_id = f"{u}-{v}"
#             edge_type = data.get('type', 'unknown')
            
#             # Skip non-decomposed edges
#             if not edge_type.startswith('decomposed'):
#                 continue
                
#             # Initialize this edge in the summary if not already present
#             if edge_id not in summary:
#                 summary[edge_id] = {}
            
#             # Find corresponding wavelet data in self._wavelet_results
#             wavelet_key = (u, v, edge_type)
#             if wavelet_key in self._wavelet_results:
#                 wavelet_data = self._wavelet_results[wavelet_key]
                
#                 # Extract oscillation metrics from wavelet data
#                 if 'wavelet_coeffs' in wavelet_data and wavelet_data['wavelet_coeffs']:
#                     for component_idx, oscillatory_index in wavelet_data['wavelet_coeffs'].items():
#                         component_id = f"{u}_{v}_{component_idx}"
#                         summary[component_id] = oscillatory_index
        
#         return summary
    
    
#     def interpret_InConsistencyOscillationMetric(self):
#         """
#         Returns the formatted interpretation text for the InConsistency Oscillation Metric.
        
#         The data is structured as a list of tuples, where each tuple contains:
#         (text_string, primary_style_tag, list_of_phrases_to_bold, list_of_phrases_to_italic)
#         """
#         interpretation_data = [
#             ("InConsistency Oscillation Metric\n", "h3", ["Oscillatory Index"], []),
            
#             ("This line chart tracks the Oscillatory Index over time, revealing the stability and nature of the convergence process.\n", "body", 
#              [], ["stability", "nature"]),
            
#             ("Interpretation\n", "h4", [], []),
            
#             ("•  Horizontal Axis (X-axis): Represents the Iteration Number (time).\n", "bullet_item", 
#              ["Horizontal Axis (X-axis)", "Iteration Number"], []),
             
#             ("•  Vertical Axis (Y-axis): Represents the Oscillatory Index.\n", "bullet_item", 
#              ["Vertical Axis (Y-axis)", "Oscillatory Index"], []),
             
#             ("•  Oscillatory Index: This metric is calculated using a Wavelet Transform on the disagreement data. It measures the ratio of high-frequency energy (rapid, spiky changes) to the total energy (all changes).\n", "bullet_item", 
#              ["Oscillatory Index", "Wavelet Transform", "high-frequency energy (rapid, spiky changes)", "total energy (all changes)"], []),

#             ("    - A value of None may appear at the beginning of the plot, as the calculation requires a minimum history of data.\n", "sub_bullet_item", 
#              ["None"], []),

#             ("How to Interpret\n", "h4", [], []),
            
#             ("This graph diagnoses how the system is converging, not just if it is converging. It provides organizational insight into the efficiency of the coordination.\n", "body", 
#              [], ["how", "if"]),
            
#             ("•  High Index Value (High \"Roughness\"): This indicates unstable, \"choppy,\" or rough convergence. The disagreement isn't decreasing smoothly; instead, it's oscillating rapidly.\n", "bullet_item", 
#              ["High Index Value (High \"Roughness\")", "unstable, \"choppy,\" or rough convergence"], []),
             
#             ("    - Organizational Insight: This suggests high coordination overhead or \"thrashing.\" The subsystems are likely making rapid, conflicting adjustments that may be creating new problems as they solve old ones. The process is inefficient and \"fighting itself\" to reach a solution.\n", "sub_bullet_item", 
#              ["coordination overhead", "thrashing"], []),
             
#             ("•  Low Index Value (High \"Smoothness\"): This indicates stable, smooth, and predictable convergence. The disagreement is being resolved steadily without erratic spikes.\n", "bullet_item", 
#              ["Low Index Value (High \"Smoothness\")", "stable, smooth, and predictable convergence"], []),

#             ("    - Organizational Insight: This is the ideal state. It shows the coordination algorithm and system decomposition are working in harmony. The \"conversation\" between subsystems is efficient, and progress is steady. 📈\n", "sub_bullet_item", 
#              [], []),
             
#             ("What to look for: An ideal process might start with a high index (as conflicts are first identified) but should quickly trend downwards to a low, stable value. A persistently high or spiky line signals a deeply inefficient or unstable coordination process that needs review.\n", "body", 
#              [], [])
#         ]
#         return interpretation_data
```
