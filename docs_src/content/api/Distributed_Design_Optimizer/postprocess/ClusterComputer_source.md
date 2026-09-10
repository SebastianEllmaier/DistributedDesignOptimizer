---
title: ClusterComputer (Source)
---

← Back to [ClusterComputer documentation](ClusterComputer.md)

# ClusterComputer - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\ClusterComputer.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Cluster computation module for graph analysis.

This module provides functionality for computing clusters in the
coupling graph of distributed optimization problems.
"""

import networkx as nx
import numpy as np
from typing import List, Dict, Tuple
from sklearn.cluster import SpectralClustering
from Distributed_Design_Optimizer.postprocess import GraphInit
from Distributed_Design_Optimizer.subsystem import SubSystemInterface
from Distributed_Design_Optimizer.middlelevel import InConsistencySizeInterface

class ClusterComputer:
    
    """

    Cluster Computer Performs Spectral Clustering Analysis on a Preprocessed Undirected Graph with aggregated Primal Residual as edge weight.

    Multi Di Graph is preprocessed into a undirected graph.

    Edges will have the max Inconsistency value as the edge weights.

    After analysis, the cluster id to which the node belongs to is stored in the Master Graph nodes

    """
    
    def __init__(self, graph_init: GraphInit, subsystems: List[SubSystemInterface]):
        """Initialize the cluster computer.

        Args:
            graph_init: The initialized graph object.
            subsystems: List of subsystems in the system.
        """
        self._graph_init = graph_init
        self._mastergraph = graph_init.get_graph()
        self._subsystems = subsystems
        self._subsystem_lookup = {}
        self._undirected_graph = None 
        self._cluster_labels = None 
        self._numberof_clusters = 2 
        
        # Build lookup immediately
        self.create_subsystem_lookup()
        
    def create_subsystem_lookup(self) -> None:
        """Create a lookup dictionary for Subsystems objects."""
        self._subsystem_lookup = {}
        for subsystem in self._subsystems:
            id = subsystem.get_SUBSYSTEMID()
            self._subsystem_lookup[id] = subsystem
            
    def preprocess_graph(self) -> None:
        """

        Preprocess the mastergraph into an undirected graph with appropriate weights.

        All different edges of the Master Graph is considered. Max Inconsistency Value of each edge is noted.

        If multiple edges (same or opposite directions) exists between two nodes, then it is aggregated into a single directed edge with max inconsistency value

       

        Returns:

            nx.Graph: Undirected graph with processed weights

        """
        undirected_graph = nx.Graph()
        
        # Ensure all nodes exist even if they have no edges
        undirected_graph.add_nodes_from(self._mastergraph.nodes())

        direction_max: Dict[Tuple[str, str], float] = {}

        # 1. Extract raw inconsistency values
        for idparent, idchild, key, data in self._mastergraph.edges(keys=True, data=True):
            parent_subsystem: SubSystemInterface = self._subsystem_lookup.get(idparent)
            if parent_subsystem is None: 
                continue
            
            # Defensive coding: handle None return
            inconsistencies = parent_subsystem.get_Inconsistencies()
            if not inconsistencies: 
                continue

            max_val = 0.0
            for inconsistency in inconsistencies:
                if inconsistency.get_ID() == idchild:
                    v = inconsistency.get_maxInconsistencyValue()
                    if v is not None:
                        max_val = max(max_val, abs(v))

            key_dir = (idparent, idchild)
            # Store max if multiple edges exist between same directed pair
            direction_max[key_dir] = max(direction_max.get(key_dir, 0.0), max_val)

        # 2. Symmetrize (Convert to Undirected)
        seen_pairs = set()
        for (u, v), val in direction_max.items():
            pair = tuple(sorted((u, v)))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            
            uv = direction_max.get((pair[0], pair[1]), 0.0)
            vu = direction_max.get((pair[1], pair[0]), 0.0)
            
            # Logic: We want high inconsistency to bind nodes together.
            final_weight = float(max(uv, vu))
            
            # OPTIONAL: Thresholding to remove noise (helps stability)
            if final_weight > 1e-6:
                undirected_graph.add_edge(pair[0], pair[1], weight=final_weight)

        self._undirected_graph = undirected_graph   

    def perform_spectral_clustering(self) -> None:
        """Perform spectral clustering on the preprocessed graph.

        This method preprocesses the graph, computes spectral clustering,
        and stores the cluster assignments in the graph nodes.
        """
        self.preprocess_graph()
        
        # Guard clause for empty graph or disconnected components
        if self._undirected_graph.number_of_nodes() == 0:
            return

        # Get adjacency matrix
        adjacency_matrix = nx.to_numpy_array(self._undirected_graph, weight='weight')
        
        # Dynamic Cluster Number (Optional Suggestion)
        # If the graph is huge, k=2 might not be enough. 
        # You might want to ensure k is not greater than number of nodes
        n_clusters = min(self._numberof_clusters, len(self._undirected_graph.nodes))
        
        if n_clusters < 2:
            # Trivial case: everything is one cluster
            self._cluster_labels = np.zeros(len(self._undirected_graph.nodes))
        else:
            clustering = SpectralClustering(
                n_clusters=n_clusters,
                affinity='precomputed',
                assign_labels='discretize',
                random_state=42
            )
            self._cluster_labels = clustering.fit_predict(adjacency_matrix)
        
        # Store results
        for i, node in enumerate(self._undirected_graph.nodes()):
            cluster_id = int(self._cluster_labels[i])
            # self._undirected_graph is local, so we must store in mastergraph/init
            self._graph_init.store_NodeCluster(node, cluster_id)
            if node in self._mastergraph.nodes:
                self._mastergraph.nodes[node]['cluster'] = cluster_id
                
                
    def get_cluster_summary(self) -> Dict:
        """
        Get a comprehensive summary of clustering results from the mastergraph.      

        Returns:

            dict: Summary of cluster assignments for all nodes

        """

        if self._cluster_labels is None:
            self.perform_spectral_clustering()

        summary = {
            "nodes": {},
            "clusters": {}
        }

       

        # Node cluster summary
        for node in self._mastergraph.nodes():
            cluster_id = self._mastergraph.nodes[node].get('cluster')         
            summary["nodes"][node] = {
                "id": node,
                "cluster": cluster_id
            }

            # Initialize or update cluster data
            if cluster_id not in summary["clusters"]:
                summary["clusters"][cluster_id] = {
                    "nodes": [],
                    "size": 0
                }

            # Add node to its cluster's node list
            summary["clusters"][cluster_id]["nodes"].append(node)
            summary["clusters"][cluster_id]["size"] += 1

        return summary

   

    @staticmethod
    def interpret_static_ClusterAnalysis() -> list:
        """Return formatted interpretation text for Static Cluster Analysis.

        Returns:
            List of tuples containing text, style tag, and phrases to bold.
        """

        interpretation_data = [
            ("Static Cluster Analysis\n", "h3", []),          

            ("This network graph shows how subsystems are clustered based on their level of disagreement, helping to identify potential architectural improvements.\n", "body", []),

            ("Interpretation\n", "h4", []),
            ("•  Nodes: Each circle represents a unique subsystem in the architecture.\n", "bullet_item",
             ["Nodes", "subsystem"]),
            ("•  Colors: The color of a node indicates which cluster it belongs to.\n", "bullet_item",
             ["Colors", "cluster"]),
            ("•  Clusters: The groups are calculated using Spectral Clustering on the disagreement data. This method partitions the graph by identifying subsystems with similar disagreement patterns. Subsystems within the same cluster (same color) have high disagreement with each other.\n", "bullet_item",

             ["Clusters", "Spectral Clustering"]),
            
            ("How to Interpret\n", "h4", []),
            ("Look for groups of nodes with the same color. A cluster of subsystems with high internal disagreement suggests they are tightly coupled and might be candidates for merging into a single system. This could simplify the architecture and reduce communication overhead between them.\n", "body",

             ["merging into a single system"])

        ]

        return interpretation_data

   

    @staticmethod
    def interpret_dynamic_ClusterAnalysis() -> list:
        """Return formatted interpretation text for Dynamic Cluster Analysis.

        Returns:
            List of tuples containing text, style tag, and phrases to bold.
        """

        interpretation_data = [

            ("Dynamic Cluster Analysis\n", "h3", []),           

            ("This Sankey diagram tracks the movement of subsystems between disagreement clusters over time, providing insight into the coordination algorithm's performance.\n", "body", []),

            ("Interpretation\n", "h4", []),          

            ("•  Vertical Columns: Each column represents a single iteration of the algorithm.\n", "bullet_item",
             ["Vertical Columns", "iteration"]),
            ("•  Colored Blocks: Each block within a column is a cluster at that iteration. Subsystems grouped in the same cluster have high disagreement with each other.\n", "bullet_item",

             ["Colored Blocks", "cluster"]),
            ("•  Flows: The connecting bands illustrate how subsystems move between clusters as the algorithm progresses from one iteration to the next.\n", "bullet_item",

             ["Flows", "move between clusters"]),
            ("How to Interpret\n", "h4", []),

            ("This visual helps you understand if the coordination algorithm is effectively solving the distributed problem.\n", "body", []),

            ("•  Healthy Convergence: When you see subsystems moving between different clusters over the iterations, it's a positive sign. This movement shows that the algorithm is actively resolving disagreements and working towards a consensus.\n", "bullet_item",

             ["Healthy Convergence", "resolving disagreements"]),
            ("•  Decomposition Issues: Look for flows that remain static, where a group of subsystems persists in the same cluster from start to finish. This indicates a persistent high level of disagreement that the algorithm cannot resolve. In this case, the underlying system decomposition should be reviewed, as these subsystems may be candidates for merging. 🧩\n", "bullet_item",

             ["Decomposition Issues", "system decomposition should be reviewed"])
        ]
        return interpretation_data
```
