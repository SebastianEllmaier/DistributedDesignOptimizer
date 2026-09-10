# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Centrality computation module for graph analysis.

This module provides functionality for computing centrality metrics
in the coupling graph of distributed optimization problems.
"""

from typing import List, Dict

import networkx as nx
from Distributed_Design_Optimizer.postprocess import GraphInit
from Distributed_Design_Optimizer.subsystem import SubSystemInterface
from Distributed_Design_Optimizer.middlelevel import InConsistencySizeInterface
from pyvis.network import Network
import os
import colorsys

class CentralityComputer:
    """
    Computes the Centrality Measures for the master graph.

    The Degree Centrality and Page Rank measure is computed for the master graph with primal residuals as the edge weights
    Here the Master Graph (Multi Directed Graph) is preprocessed into a Directed Graph with aggregated Primal Residual Values
    From each edge, Max Inconsistency Value is considered and weights from two directed parallel edges are merged into a single with edge weights summed.
    The Centrality values and pagerank measures are stored in the Master graph Node
    """
    
    
    def __init__(self, graph_init: GraphInit, subsystems: List[SubSystemInterface]):
        """Compute the centrality measures of the graph.

        Args:
            graph_init: The initialized graph object.
            subsystems: List of subsystems in the system.
        """
        self._graph_init = graph_init
        self._mastergraph = graph_init.get_graph()
        self._subsystems: List[SubSystemInterface] = subsystems
        
        # Create a lookup function for the easier access of the parent and child Hierarchic Subsystem Objects
        self.create_subsystem_lookup()
        
    def create_subsystem_lookup(self) -> None:
        """Create a lookup dictionary for Subsystems objects.
        """
        self._subsystem_lookup: Dict[str, SubSystemInterface] = {}
        
        for subsystem in self._subsystems:
            id = subsystem.get_SUBSYSTEMID()
            self._subsystem_lookup[id] = subsystem
            
    def compute_EdgeWeights(self) -> None:
        """Centrality Measures are based on the inconsistencies. L infinity Norm is considered for the Centrality Measurement analysis.
        """
        graph = self._mastergraph
        
        for u, v, key, data in graph.edges(keys=True, data=True):
            # loop through each edge available and get its aggregated Max Inconsistency Value
            edge_type = data.get('type')
            self.compute_single_EdgeWeight(u, v, key, edge_type)
    
    def compute_single_EdgeWeight(self, idparent: str, idchild: str, key: object, edge_type: str) -> None:
        """Compute the edge weight for a single edge based on inconsistency values.

        Args:
            idparent: Identifier of the parent node.
            idchild: Identifier of the child node.
            key: The edge key in the multigraph.
            edge_type: The type of edge (decomposed_mappedresponse or decomposed_shareddesignvariable).
        """
        
            
        # Get the parent and child Hierarchic Subsystem Objects
        parent_inconsistencies: List[InConsistencySizeInterface] = self._subsystem_lookup.get(idparent).get_Inconsistencies()
        
        
        if edge_type == "decomposed_mappedresponse":
            for inconsistency in parent_inconsistencies:
                if inconsistency.get_ID() == idchild:
                    max_inconsistency = inconsistency.get_MappedResponse_Minus_CopyCouplingVariable_InfyNorm()
        elif edge_type == "decomposed_shareddesignvariable":
            for inconsistency in parent_inconsistencies:
                if inconsistency.get_ID() == idchild:
                    max_inconsistency = inconsistency.get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable_InfyNorm()
        else:
            max_inconsistency = 0.0
            
        # Store the weight in the edge data
        self._mastergraph[idparent][idchild][key]['weight'] = abs(max_inconsistency)
            
    def compute_CentralityMeasures(self) -> None:
        """
        Compute Centrality Measures for all nodes in the master graph.
        
        Computes Degree Centrality Measures and EigenVector 
        """
        # Degree Centrality needs to be computed only once, as it doesn't change
        degreecentralitycompute_flag = True
        # compute L Infinity Norms of Inconsistencies for each edge
        self.compute_EdgeWeights()
        
        # create a weighted graph for centrality calculations
        weighted_graph = nx.DiGraph()
        
        # add nodes to the weighted_graph from the mastergraph
        # here the Multi Di Graph is Converted to weighted directed graph
        for node in self._mastergraph:
            weighted_graph.add_node(node)
            
        # add weighted edges to the weighted_graph
        for u, v, key, data in self._mastergraph.edges(keys=True, data=True):
            weight = data.get('weight', 0.0)
            
            if weighted_graph.has_edge(u,v):
                weighted_graph[u][v]['weight'] += weight
            else:
                weighted_graph.add_edge(u, v, weight=weight)
        
        if degreecentralitycompute_flag:  
            indegree_centrality = nx.in_degree_centrality(weighted_graph)
            outdegree_centrality = nx.out_degree_centrality(weighted_graph)
            degreecentralitycompute_flag = False
        
        weighted_indegree = self._calculate_weightedInDegreeCentrality(weighted_graph)
        weighted_outdegree = self._calculate_weightedOutDegreeCentrality(weighted_graph)
        
        weighted_degree_centrality = {
            node: (weighted_indegree.get(node) or 0.0) + (weighted_outdegree.get(node) or 0.0)
            if weighted_indegree.get(node) is not None or weighted_outdegree.get(node) is not None else None
            for node in weighted_graph.nodes()
        }
        
        # Use PageRank directly - works for both connected and disconnected graphs
        # The alpha parameter (damping factor) can be tuned (default is 0.85)
        try:
            # Increased max_iter and added a tolerance parameter to aid convergence
            pagerank_centrality = nx.pagerank(weighted_graph, weight='weight', alpha=0.85, max_iter=5000, tol=1.0e-4)
        except nx.PowerIterationFailedConvergence:
            print("Warning: PageRank failed to converge. Setting PageRank values to 0.0 for all nodes.")
            # Fallback to a default value for all nodes if convergence still fails
            pagerank_centrality = {node: 0.0 for node in weighted_graph.nodes()}
        
        for node in self._mastergraph.nodes():
            self._graph_init.store_NodeCentrality(
                node,
                indegree_centrality.get(node, None),
                outdegree_centrality.get(node, None),
                weighted_indegree.get(node, None),
                weighted_outdegree.get(node, None),
                weighted_degree_centrality.get(node, None),
                pagerank_centrality.get(node, None)
            )
        
        #self.visualize_pagerank()
            
    def _calculate_weightedInDegreeCentrality(self, G) -> Dict:
        """Calculates the weighted in degree centrality
        
        -> Sum of the Incoming Weights and normalizes b (n-1)
        """
        
        weighted_indegree = {}
        n = len(G)
        
        for node in G:
            # sum of the incoming edge weights
            weighted_in_edges = sum(data.get('weight', 0.0) for _, _, data in G.in_edges(node, data=True))
            # Normalize by maximum possible number of nodes
            weighted_indegree[node] = weighted_in_edges / (n-1) if n > 1 else 0
            
        return weighted_indegree
    
    def _calculate_weightedOutDegreeCentrality(self, G):
        """
        Calculate weighted out degree centrality
        Sum the weights of outgoing edges and normalizes by (n-1)
        """
        
        weighted_outdegree = {}
        n = len(G)
        for node in G:
            # Sum weights of outgoing edges
            weighted_out_edges = sum(data.get('weight', 0.0) for _, _, data in G.out_edges(node, data=True))
            # Normalize by maximum possible number of nodes
            weighted_outdegree[node] = weighted_out_edges / (n-1) if n > 1 else 0
            
        return weighted_outdegree
    
    def get_centrality_summary(self) -> Dict:
        """
        Get a comprehensive summary of computed centrality measures.
        
        Returns:
            dict: Summary of centrality measures for all nodes and edges
        """
        summary = {
            "nodes": {},
            "edges": {}
        }
        
        # Node centrality summary
        for node in self._mastergraph.nodes():
            node_data = self._mastergraph.nodes[node]
            InDegree_value = node_data.get('InDegree_centrality', 0.0)
            OutDegree_value = node_data.get('OutDegree_centrality', 0.0)
            WeightedInDegree_value = node_data.get('WeightedInDegree_centrality', 0.0)
            WeightedOutDegree_value = node_data.get('WeightedOutDegree_centrality', 0.0)
            WeightedDegree_value = node_data.get('WeightedDegree_centrality', 0.0)
            pagerank_centrality = node_data.get('PageRank_centrality', 0.0)
            
            summary["nodes"][node] = {
                "id": node,
                'InDegree_centrality': InDegree_value,
                'OutDegree_centrality': OutDegree_value,
                'WeightedInDegree_centrality': WeightedInDegree_value,
                'WeightedOutDegree_centrality': WeightedOutDegree_value, 
                'WeightedDegree_centrality': WeightedDegree_value,                 
                "PageRank_centrality": pagerank_centrality
            }
        return summary
    
    def visualize_pagerank(self, filename: str = "pagerank_visualization.html", height: str = "750px", width: str = "100%") -> None:
        """Create an interactive visualization of the graph with nodes sized by PageRank.

        Args:
            filename: Name of the HTML file to save the visualization.
            height: Height of the visualization.
            width: Width of the visualization.
        """
        # Create a PyVis network
        net = Network(height=height, width=width, directed=True, notebook=False)
        
        # Get the graph and create a copy to work with
        graph = self._mastergraph
        
        # Find min and max PageRank values for scaling
        pagerank_values = [graph.nodes[node].get('PageRank_centrality', 0.0) for node in graph.nodes()]
        min_pagerank = min(pagerank_values) if pagerank_values else 0.0
        max_pagerank = max(pagerank_values) if pagerank_values else 1.0
        
        # Function to scale PageRank values to node sizes (between 10 and 50)
        def scale_pagerank_to_size(pagerank, min_val=min_pagerank, max_val=max_pagerank, min_size=10, max_size=50):
            if max_val == min_val:  # Avoid division by zero
                return (min_size + max_size) / 2
            return min_size + (pagerank - min_val) * (max_size - min_size) / (max_val - min_val)
        
        # Generate colors for nodes based on PageRank value (using a color gradient from blue to red)
        def get_color_for_value(value, min_val=min_pagerank, max_val=max_pagerank):
            if max_val == min_val:
                normalized = 0.5
            else:
                normalized = (value - min_val) / (max_val - min_val)
            
            # Convert to a color (using HSV where hue ranges from blue to red)
            hue = 0.6 - 0.6 * normalized  # 0.6 (blue) to 0.0 (red)
            rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.9)  # Saturation and Value are constants
            
            # Convert RGB (0-1) to hex color
            return f"#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}"
            
        # Add nodes to the visualization
        for node in graph.nodes():
            node_data = graph.nodes[node]
            pagerank = node_data.get('PageRank_centrality', 0.0)
            
            # Create a detailed title for hover tooltip
            title = f"Node: {node}<br>" \
                   f"PageRank: {pagerank:.4f}<br>" \
                   f"InDegree: {node_data.get('InDegree_centrality', 0.0):.4f}<br>" \
                   f"OutDegree: {node_data.get('OutDegree_centrality', 0.0):.4f}<br>" \
                   f"WeightedInDegree: {node_data.get('WeightedInDegree_centrality', 0.0):.4f}<br>" \
                   f"WeightedOutDegree: {node_data.get('WeightedOutDegree_centrality', 0.0):.4f}"
            
            node_size = scale_pagerank_to_size(pagerank)
            node_color = get_color_for_value(pagerank)
            
            net.add_node(node, 
                         title=title, 
                         size=node_size, 
                         color=node_color,
                         label=node)
        
        # Add edges to the visualization
        for u, v, key, data in graph.edges(keys=True, data=True):
            edge_type = data.get('type', 'unknown')
            weight = data.get('weight', None)
            
            # Create a tooltip for the edge
            title = f"Type: {edge_type}"
            if weight is not None:
                title += f"<br>Weight: {weight:.4f}"
            
            # Use different colors for different edge types
            if 'decomposed' in edge_type:
                color = "#007ACC"  # Blue for decomposed
            else:
                color = "#FFA500"  # Orange for non-decomposed
            
            # Add the edge to the network
            net.add_edge(u, v, title=title, color=color)
        
        # Configure physics for better layout
        net.barnes_hut(
            gravity=-80000,
            central_gravity=0.3,
            spring_length=200,
            spring_strength=0.05,
            damping=0.09
        )
        
        # Save the visualization
        output_path = filename
        net.show(output_path)
        print(f"Visualization saved to: {os.path.abspath(output_path)}")
        
    @staticmethod
    def interpret_static_WeightedInDegree_centrality() -> list:
        """Return formatted interpretation text for Static Weighted In-Degree Centrality.

        Returns:
            List of tuples containing text, style tag, and phrases to bold.
        """
        interpretation_data = [
            ("Static WeightedInDegree_centrality\n", "h3", ["Weighted In-Degree Centrality"]),
            
            ("This graph visualizes the Weighted In-Degree Centrality of each subsystem, highlighting which parts of the system are absorbing the most disagreement.\n", "body", []),

            ("Interpretation\n", "h4", []),

            ("•  Nodes: Each circle represents a subsystem.\n", "bullet_item", 
             ["Nodes", "subsystem"]),
             
            ("•  Edges: The directed arrows show the flow of dependency or decomposition between subsystems.\n", "bullet_item", 
             ["Edges"]),
             
            ("•  Centrality Score: The score is based on the total magnitude of incoming disagreement a subsystem receives from others.\n", "bullet_item", 
             ["Centrality Score", "incoming disagreement"]),
             
            ("•  Visual Cues: The size and color of a node both indicate its centrality score. A larger size and a color closer to red signify a higher score (more incoming disagreement).\n", "bullet_item", 
             ["Visual Cues", "size", "color"]),

            ("How to Interpret\n", "h4", []),
            
            ("The centrality score reveals the critical points of conflict within your system's architecture.\n", "body", []),

            ("•  High Centrality (Red / Large Nodes): These are the system's conflict hotspots or \"shock absorbers.\" A high score indicates the subsystem is dealing with significant disagreement from other parts of the system, likely involving influential design variables. The coordination algorithm should prioritize these nodes to resolve the most impactful conflicts. 🔥\n", "bullet_item", 
             ["High Centrality (Red / Large Nodes)", "conflict hotspots", "prioritize these nodes"]),
             
            ("•  Medium Centrality (Yellow / Medium Nodes): These subsystems are managing a moderate, healthy level of conflict and are actively participating in the resolution process.\n", "bullet_item", 
             ["Medium Centrality (Yellow / Medium Nodes)"]),
             
            ("•  Low Centrality (Green / Small Nodes): These are stable subsystems with minimal incoming disagreement. Their low conflict level suggests they have the capacity to handle additional tasks, making them good candidates for work redistribution. ✅\n", "bullet_item", 
             ["Low Centrality (Green / Small Nodes)", "additional tasks"])
        ]
        return interpretation_data
    
    @staticmethod
    def interpret_dynamic_WeightedInDegree_centrality() -> list:
        """Return formatted interpretation text for Dynamic Weighted In-Degree Centrality.

        Returns:
            List of tuples containing text, style tag, and phrases to bold.
        """
        interpretation_data = [
            ("Dynamic WeightedInDegree_centrality\n", "h3", []),
            
            ("This heatmap displays the evolution of Weighted In-Degree Centrality, showing how the incoming disagreement for each subsystem changes over time.\n", "body", []),
            
            ("Interpretation\n", "h4", []),
            
            ("•  Vertical Axis (Y-axis): Each row represents a unique subsystem, identified by its Node ID.\n", "bullet_item", 
             ["Vertical Axis (Y-axis)", "subsystem"]),
             
            ("•  Horizontal Axis (X-axis): Each column represents a single iteration of the algorithm, showing the progression over time.\n", "bullet_item", 
             ["Horizontal Axis (X-axis)", "iteration"]),
             
            ("•  Color: The color of each cell reveals the centrality score of a subsystem at a specific iteration. Brighter colors (like yellow) indicate a high level of incoming disagreement, while darker colors (like purple) indicate a low level.\n", "bullet_item", 
             ["Color", "Brighter colors", "darker colors"]),

            ("How to Interpret\n", "h4", []),
            
            ("By tracking the color changes for each subsystem from left to right, you can assess the algorithm's effectiveness at resolving conflicts.\n", "body", []),
            
            ("•  Healthy Convergence: Look for rows that transition from brighter colors to darker colors as the iterations increase. This is a positive sign, indicating that the algorithm is successfully resolving conflicts and the subsystem is becoming more stable. 👍\n", "bullet_item", 
             ["Healthy Convergence", "darker colors"]),
             
            ("•  Persistent Hotspots: Pay attention to any row that remains brightly colored across many iterations. This identifies a persistent \"shock absorber\" or conflict hotspot—a subsystem that is consistently struggling with high incoming disagreement that the algorithm cannot resolve. These subsystems may require an architectural review. 🧐\n", "bullet_item", 
             ["Persistent Hotspots", "remains brightly colored"]),
             
            ("•  Sudden Spikes: A sudden shift from a dark to a bright color can indicate that a new conflict has emerged for that subsystem late in the process.\n", "bullet_item", 
             ["Sudden Spikes"])
        ]
        return interpretation_data
    
    @staticmethod
    def interpret_static_WeightedOutDegree_centrality() -> list:
        """Return formatted interpretation text for Static Weighted Out-Degree Centrality.

        Returns:
            List of tuples containing text, style tag, and phrases to bold.
        """
        interpretation_data = [
            ("Static WeightedOutDegree_centrality\n", "h3", ["Weighted Out-Degree Centrality"]),
            
            ("This graph visualizes the Weighted Out-Degree Centrality of each subsystem, highlighting the primary sources of disagreement within the system.\n", "body", []),
            
            ("Interpretation\n", "h4", []),
            
            ("•  Nodes: Each circle represents a subsystem.\n", "bullet_item", 
             ["Nodes", "subsystem"]),
             
            ("•  Edges: The directed arrows show the flow of influence or dependency from one subsystem to another.\n", "bullet_item", 
             ["Edges"]),
             
            ("•  Centrality Score: The score is based on the total magnitude of outgoing disagreement a subsystem sends to other parts of the system.\n", "bullet_item", 
             ["Centrality Score", "outgoing disagreement"]),
             
            ("•  Visual Cues: The size and color of a node both indicate its centrality score. A larger size and a color closer to red signify a higher score (more outgoing disagreement).\n", "bullet_item", 
             ["Visual Cues", "size", "color"]),

            ("How to Interpret\n", "h4", []),
            
            ("This metric helps you pinpoint which subsystems are instigating the most conflict across the architecture.\n", "body", []),
            
            ("•  High Centrality (Red / Large Nodes): These subsystems are the primary sources of conflict, broadcasting a high level of disagreement that impacts many other subsystems. To effectively resolve system-wide issues, the design and variables within these specific nodes should be addressed first. They are the starting point of the \"drama.\" 😠\n", "bullet_item", 
             ["High Centrality (Red / Large Nodes)", "sources of conflict", "these specific nodes should be addressed first"]),
             
            ("•  Medium Centrality (Yellow / Medium Nodes): These subsystems contribute a moderate amount of disagreement to the system. They influence others but are not the most critical sources of conflict.\n", "bullet_item", 
             ["Medium Centrality (Yellow / Medium Nodes)"]),
             
            ("•  Low Centrality (Green / Small Nodes): These are stable subsystems that cause minimal disagreement for others. They have a low negative impact on the rest of the system's architecture.\n", "bullet_item", 
             ["Low Centrality (Green / Small Nodes)"])
        ]
        return interpretation_data
    
    @staticmethod
    def interpret_dynamic_WeightedOutDegree_centrality() -> list:
        """Return formatted interpretation text for Dynamic Weighted Out-Degree Centrality.

        Returns:
            List of tuples containing text, style tag, and phrases to bold.
        """
        interpretation_data = [
            ("Dynamic WeightedOut Degree Centrality\n", "h3", []),
            
            ("This heatmap displays the evolution of Weighted Out-Degree Centrality, showing how the outgoing disagreement from each subsystem changes over time.\n", "body", []),
            
            ("Interpretation\n", "h4", []),
            
            ("•  Vertical Axis (Y-axis): Each row represents a unique subsystem, identified by its Node ID.\n", "bullet_item", 
             ["Vertical Axis (Y-axis)", "subsystem"]),
             
            ("•  Horizontal Axis (X-axis): Each column represents a single iteration of the algorithm.\n", "bullet_item", 
             ["Horizontal Axis (X-axis)", "iteration"]),
             
            ("•  Color: The color of each cell reveals the centrality score of a subsystem at a specific iteration. Brighter colors (like yellow) identify a major source of outgoing disagreement, while darker colors (like purple) indicate the subsystem is causing little conflict.\n", "bullet_item", 
             ["Color", "Brighter colors", "darker colors"]),

            ("How to Interpret\n", "h4", []),
            
            ("By tracking the color changes for each subsystem, you can see if the algorithm is successfully neutralizing the sources of conflict.\n", "body", []),
            
            ("•  Successful Resolution: The ideal pattern is a row that transitions from a bright color to a darker color over the iterations. This shows the algorithm is effectively resolving the issues within a subsystem, stopping it from broadcasting disagreement. ✅\n", "bullet_item", 
             ["Successful Resolution", "darker color"]),
             
            ("•  Persistent Instigators: Pay close attention to any row that remains brightly colored. This signals a persistent source of conflict—a subsystem whose core issues are not being solved by the algorithm. These subsystems are critical targets for redesign or architectural review. 🎯\n", "bullet_item", 
             ["Persistent Instigators", "remains brightly colored", "source of conflict"]),
             
            ("•  Emerging Problems: If a row starts dark and later becomes bright, it indicates that a new source of disagreement has emerged within that subsystem during the coordination process.\n", "bullet_item", 
             ["Emerging Problems"])
        ]
        return interpretation_data
    
    @staticmethod
    def interpret_static_PageRank() -> list:
        """Return formatted interpretation text for Static PageRank Centrality.

        Returns:
            List of tuples containing text, style tag, and phrases to bold.
        """
        interpretation_data = [
            ("Static PageRank Measure\n", "h3", ["PageRank Centrality"]),
            
            ("This graph displays the PageRank Centrality of each subsystem, identifying not just which nodes are receiving disagreement, but which are influenced by *other important nodes*.\n", "body", []),
            
            ("Interpretation\n", "h4", []),
            
            ("•  Nodes: Each circle represents a subsystem.\n", "bullet_item", 
             ["Nodes", "subsystem"]),
             
            ("•  Edges: The directed arrows indicate the flow of influence or dependency.\n", "bullet_item", 
             ["Edges"]),
             
            ("•  PageRank Score: This score measures a subsystem's importance recursively. Unlike a simple in-degree count, which treats all incoming links equally, PageRank gives more weight to links coming from other high-importance subsystems.\n", "bullet_item", 
             ["PageRank Score"]),
             
            ("•  Visual Cues: The size and color of a node reflect its PageRank score. Larger, redder nodes are more influential; smaller, greener nodes are less so.\n", "bullet_item", 
             ["Visual Cues", "size", "color"]),
             
            ("What Extra Information Does PageRank Provide?\n", "h4", []),

            ("While Weighted In-Degree Centrality shows you which nodes are absorbing the most disagreement (the loudest hotspots), PageRank identifies the nodes that are at the receiving end of a critical chain of dependencies (the most strategic hotspots).\n", "body", 
             ["the loudest hotspots", "the most strategic hotspots"]),

            ("A subsystem can have a high PageRank even with few incoming links, provided those links come from other highly influential subsystems.\n", "body", []),

            ("How to Interpret\n", "h4", []),
            
            ("Use this view to identify the most strategically important points in your architecture.\n", "body", []),
            
            ("•  High PageRank (Red / Large Nodes): These are key strategic subsystems. A high score here means the node's behavior is dictated by other critical parts of the system. Resolving the disagreements flowing into this node is a high-leverage action, as its stability will likely have a positive, cascading effect on the other influential nodes that point to it. 🎯\n", "bullet_item", 
             ["High PageRank (Red / Large Nodes)", "key strategic subsystems"]),
             
            ("•  Low PageRank (Green / Small Nodes): These subsystems are less critical from a network influence perspective. They are either on the periphery or are influenced primarily by other non-critical nodes.\n", "bullet_item", 
             ["Low PageRank (Green / Small Nodes)"])
        ]
        return interpretation_data

    @staticmethod
    def interpret_dynamic_PageRank() -> list:
        """Return formatted interpretation text for Dynamic PageRank Centrality.

        Returns:
            List of tuples containing text, style tag, and phrases to bold.
        """
        interpretation_data = [
            ("Dynamic Pagerank Measure\n", "h3", []),
            
            ("This heatmap tracks the evolution of PageRank Centrality, showing how the strategic importance of each subsystem changes as the algorithm runs.\n", "body", []),
            
            ("Interpretation\n", "h4", []),
            
            ("•  Vertical Axis (Y-axis): Each row represents a unique subsystem (Node ID).\n", "bullet_item", 
             ["Vertical Axis (Y-axis)", "subsystem"]),
             
            ("•  Horizontal Axis (X-axis): Each column represents a single iteration of the algorithm.\n", "bullet_item", 
             ["Horizontal Axis (X-axis)", "iteration"]),
             
            ("•  Color: The color of a cell indicates the PageRank score at a specific iteration. Brighter colors (like yellow) signify high strategic importance, while darker colors (like purple) signify low importance.\n", "bullet_item", 
             ["Color", "Brighter colors", "darker colors"]),

            ("How to Interpret\n", "h4", []),
            
            ("By observing the color trends for each subsystem, you can understand the shifting dynamics of influence within your architecture.\n", "body", []),
            
            ("•  Increasing Importance (Dark to Bright): A row that trends towards brighter colors indicates a subsystem is becoming a more critical hub of influence as the algorithm progresses. This can happen as other issues are resolved, making this node a new focal point for remaining dependencies.\n", "bullet_item", 
             ["Increasing Importance (Dark to Bright)"]),
             
            ("•  Decreasing Importance (Bright to Dark): This is often a positive sign. A trend towards darker colors suggests that dependencies flowing into a key strategic node are being resolved, successfully reducing its role as a bottleneck. ✅\n", "bullet_item", 
             ["Decreasing Importance (Bright to Dark)"]),
             
            ("•  Stable Importance: A row that maintains its color shows a subsystem with a consistent role in the network. A persistently bright row is a constant strategic hub that remains central to the problem throughout the coordination process.\n", "bullet_item", 
             ["Stable Importance"])
        ]
        return interpretation_data
    