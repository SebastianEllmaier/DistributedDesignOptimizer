# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Graph initialization module.

This module provides functionality for initializing and managing
graph data structures for distributed optimization analysis.
"""

import networkx as nx
from typing import List, Dict
from Distributed_Design_Optimizer.subsystem import SubSystemInterface, LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.couplingparameters import SubSysCouplingParametersBasis

class GraphInit:
    """
    Main class for creating and managing a distributed design optimizer graph.
    
    This class provides methods to build, manipulate, and visualize graphs representing
    coupling relationships between subsystems in distributed design optimization problems.
    """
    
    def __init__(self):
        """Initialize the GraphInit with an empty MultiDiGraph."""
        self._graph: nx.MultiDiGraph = nx.MultiDiGraph()



    def set_MasterGraph(self, subsystems: List[SubSystemInterface], visualize: bool = True) -> nx.MultiDiGraph:
        """Build the complete graph from SubSystemInterface list.

        Args:
            subsystems: List of SubSystemInterface objects containing subsystem information.
            visualize: Whether to display the graph visualization.

        Returns:
            The constructed graph.
        """
        self.set_vertices(subsystems)
        self.set_edges(subsystems)
        
        # # Print edge details before visualization
        # self._print_edge_details()
        
        # if visualize:
        #     self.visualize_graph("Distributed Design Optimizer Graph", interactive=True)
        
        return self._graph

    def add_edge_with_attributes(self, idparent: str, idchild: str, edge_type: str) -> None:
        """Add an edge with all the attributes from the original Edges class.

        Args:
            idparent: Parent node ID.
            idchild: Child node ID.
            edge_type: Type of edge (must be unique between any pair of nodes).

        Raises:
            ValueError: If an edge with the same type already exists between the nodes.
        """
        # Check that edge type is unique between this pair of nodes
        if not self._check_edge_type_uniqueness(idparent, idchild, edge_type):
            raise ValueError(f"Edge with type '{edge_type}' already exists between nodes '{idparent}' and '{idchild}'")
        
        self._graph.add_edge(
            idparent,
            idchild,
            type=edge_type,
            primalmappedresidual=None,
            primalsharedresidual=None,
            dualmappedresidual=None,
            dualsharedresidual=None,
        )

    def set_vertices(self, subsystems: List[SubSystemInterface]) -> None:
        """Add vertices (nodes) to the graph.

        Args:
            subsystems: List of SubSystemInterface objects containing subsystem information.
        """
        for subsystem in subsystems:
            subsystem_id = subsystem.get_SUBSYSTEMID()
            self._graph.add_node(subsystem_id)

    def set_edges(self, subsystems: List[SubSystemInterface]) -> None:
        """Set edges based on coupling relationships.

        Args:
            subsystems: List of SubSystemInterface objects containing coupling information.
        """
        for subsystem in subsystems:
            
            if isinstance(subsystem, LocalSubSystemBasis):
            
                subsystem_id = subsystem.get_SUBSYSTEMID()
                couplingparameters = subsystem.get_CouplingParameters()
                for coupling in couplingparameters:
                    
                    if isinstance(coupling, SubSysCouplingParametersBasis):
                        # For each coupling, only outgoing edges are added.
                        # Incoming edges will be added from the other subsystem.
                        if coupling.get_MappedResponses() is not None:
                            if coupling.get_Copy_CouplingVariable() is not None:
                                self.add_edge_with_attributes(subsystem_id, coupling.get_ID(), "decomposed_mappedresponse")
                            else:
                                self.add_edge_with_attributes(subsystem_id, coupling.get_ID(), "nondecomposed_mappedresponse")
                        
                        if coupling.get_SharedDesignVariables() is not None:
                            if coupling.get_Copy_TargetSharedDesignVariables() is not None:
                                self.add_edge_with_attributes(
                                    subsystem_id, coupling.get_ID(), "decomposed_shareddesignvariable"
                                )
                            else:
                                self.add_edge_with_attributes(
                                    subsystem_id, coupling.get_ID(), "nondecomposed_shareddesignvariable"
                                )

    def store_primalresidual(self, idparent: str, idchild: str, edge_type: str, residual_values: List[float] | None) -> None:
        """Store primal residual for a specific edge identified by type.

        Args:
            idparent: Parent node ID.
            idchild: Child node ID.
            edge_type: Type of edge to find.
            residual_values: List of residual values to store.
        """
        edge_key = self._find_edge_key_by_type(idparent, idchild, edge_type)
        if edge_key is not None:
            edge_data = self._graph[idparent][idchild][edge_key]
            if edge_type == "decomposed_mappedresponse" or edge_type == "nondecomposed_mappedresponse":
                edge_data['primalmappedresidual'] = residual_values
            elif edge_type == "decomposed_shareddesignvariable" or edge_type == "nondecomposed_shareddesignvariable":
                edge_data['primalsharedresidual'] = residual_values

    def store_dualresidual(self, idparent: str, idchild: str, edge_type: str,  residual_values: List[float | None] | None) -> None:
        """Store the aggregated dual residual for a specific edge identified by type.

        Args:
            idparent: Parent node ID.
            idchild: Child node ID.
            edge_type: Type of edge to find.
            residual_values: List of residual values to store.
        """
        edge_key = self._find_edge_key_by_type(idparent, idchild, edge_type)
        if edge_key is not None:
            edge_data = self._graph[idparent][idchild][edge_key]
            if edge_type == "decomposed_mappedresponse" or edge_type == "nondecomposed_mappedresponse":
                edge_data['dualmappedresidual'] = residual_values
            elif edge_type == "decomposed_shareddesignvariable" or edge_type == "nondecomposed_shareddesignvariable":
                edge_data['dualsharedresidual'] = residual_values
                
                
    def store_NodeCentrality(self, node_id: str, in_degree_value: float, out_degree_value: float, 
                             weightedInDegree_value: float, weightedOutDegree_value: float, 
                             weighteddegree_centrality: float | None, pagerank_centrality: float | None,) -> None:
        """Store the Centrality Values for a specific Node.

        Args:
            node_id: Node identifier.
            in_degree_value: In-degree centrality value.
            out_degree_value: Out-degree centrality value.
            weightedInDegree_value: Weighted in-degree centrality value.
            weightedOutDegree_value: Weighted out-degree centrality value.
            weighteddegree_centrality: Weighted degree centrality value.
            pagerank_centrality: PageRank centrality value.
        """
        
        if self._graph.has_node(node_id):            
            self._graph.nodes[node_id]['InDegree_centrality'] = in_degree_value
            self._graph.nodes[node_id]['OutDegree_centrality'] = out_degree_value
            self._graph.nodes[node_id]['WeightedInDegree_centrality'] = weightedInDegree_value
            self._graph.nodes[node_id]['WeightedOutDegree_centrality'] = weightedOutDegree_value
            self._graph.nodes[node_id]['WeightedDegree_centrality'] = weighteddegree_centrality
            self._graph.nodes[node_id]['PageRank_centrality'] = pagerank_centrality
        else:
            print(f"Warning: Node {node_id} not found in the graph")
            
    def store_NodeCluster(self, node_id: str, cluster_id: int) -> None:
        """Store the cluster assignment for a specific node.

        Args:
            node_id: Node identifier.
            cluster_id: Assigned cluster ID.
        """        
        if self._graph.has_node(node_id):
            self._graph.nodes[node_id]['cluster'] = cluster_id
        else:
            print(f"Warning: Node {node_id} not found in the graph")
                
                
    def store_InConsistencyOscillationIndex(self, idparent: str, idchild: str, edge_type: str, oscillation_data: Dict) -> None:
        """Store the inconsistency oscillation index data for a specific edge identified by type.

        Args:
            idparent: Parent node ID.
            idchild: Child node ID.
            edge_type: Type of edge to find.
            oscillation_data: Dictionary containing oscillation index values.
        """
        edge_key = self._find_edge_key_by_type(idparent, idchild, edge_type)
        if edge_key is not None:
            edge_data = self._graph[idparent][idchild][edge_key]
            edge_data['oscillatory_index'] = oscillation_data
        else:
            print(f"Warning: Edge from {idparent} to {idchild} with type {edge_type} not found")

    def compute_couplingstrength(self, idparent: str, idchild: str, edge_type: str) -> None:
        """Compute coupling strength for a specific edge identified by type.

        Args:
            idparent: Parent node ID.
            idchild: Child node ID.
            edge_type: Type of edge to find.
        """
        edge_key = self._find_edge_key_by_type(idparent, idchild, edge_type)
        if edge_key is not None:
            edge_data = self._graph[idparent][idchild][edge_key]
            #TODO: Add coupling strength computation logic here
            edge_data['coupling_strength'] = 0.0  # placeholder

    def get_edge_attributes(self, idparent: str, idchild: str, edge_type: str) -> Dict | None:
        """Get all attributes for a specific edge identified by type.

        Args:
            idparent: Parent node ID.
            idchild: Child node ID.
            edge_type: Type of edge to find.

        Returns:
            Edge attributes dictionary or None if edge not found.
        """
        edge_key = self._find_edge_key_by_type(idparent, idchild, edge_type)
        if edge_key is not None:
            return self._graph[idparent][idchild][edge_key]
        return None

    def get_graph(self) -> nx.MultiDiGraph:
        """Return the NetworkX graph.

        Returns:
            The internal graph object.
        """
        return self._graph

    def visualize_graph(self, title: str = "Graph Visualization",
                        figsize: tuple = None, save_path: str = None, interactive: bool = True) -> None:
        """Visualize the directed multigraph using the GraphVisualizer class.

        Args:
            title: Title for the plot.
            figsize: Figure size (width, height). If None, auto-calculated based on node count.
            save_path: Optional path to save the figure.
            interactive: Whether to enable interactive hover tooltips.
        """
        visualizer = GraphVisualizer()
        visualizer.visualize(self._graph, title, figsize, save_path, interactive)

    def print_edge_verification(self) -> None:
        """Print edge list for verification purposes - shows idparent, idchild, and type."""
        self._print_edge_details()

    @staticmethod
    def main(subsystems: List[SubSystemInterface]) -> nx.MultiDiGraph:
        """Main method to create and return a graph.

        Args:
            subsystems: List of SubSystemInterface objects.

        Returns:
            The constructed graph.
        """
        graph_init = GraphInit()
        return graph_init.set_MasterGraph(subsystems)



    def _check_edge_type_uniqueness(self, idparent: str, idchild: str, edge_type: str):
        """Check if an edge with the same type already exists between the nodes.
        
        Args:
            idparent: Parent node ID
            idchild: Child node ID
            edge_type: Type of edge to check
            
        Returns:
            bool: True if edge type is unique, False otherwise
        """
        if self._graph.has_edge(idparent, idchild):
            edge_data = self._graph[idparent][idchild]
            existing_types = [edge_data[key]['type'] for key in edge_data]
            return edge_type not in existing_types
        return True
    
    def _find_edge_key_by_type(self, idparent: str, idchild: str, edge_type: str):
        """Find the key of an edge with specific type between two nodes.
        
        Args:
            idparent: Parent node ID
            idchild: Child node ID
            edge_type: Type of edge to find
            
        Returns:
            int or None: NetworkX edge key if found, None otherwise
        """
        if self._graph.has_edge(idparent, idchild):
            edge_data = self._graph[idparent][idchild]
            for key in edge_data:
                if edge_data[key]['type'] == edge_type:
                    return key
        return None

    def _print_edge_details(self):
        """Print detailed information about all edges."""
        print("\n" + "="*80)
        print("EDGE LIST FOR VERIFICATION (idparent, idchild, type)")
        print("="*80)
        
        edge_count = 0
        for u, v, key, data in self._graph.edges(keys=True, data=True):
            edge_count += 1
            edge_type = data.get('type', 'Unknown')
            print(f"Edge {edge_count}: idparent='{u}' → idchild='{v}' | type='{edge_type}' | NetworkX_key={key}")
        
        if edge_count == 0:
            print("No edges found in the graph.")
        else:
            print(f"\nTotal edges: {edge_count}")
        
        print("="*80)