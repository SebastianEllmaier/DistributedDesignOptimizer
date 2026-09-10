---
title: _static_graph_builder (Source)
---

← Back to [_static_graph_builder documentation](_static_graph_builder.md)

# _static_graph_builder - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\handlers\_static_graph_builder.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Static graph builders — produce graph_data dicts for GraphWidget rendering."""

import math
from collections import deque

import networkx as nx

from ..utils.graph_utils import (
    hierarchical_layout, green_yellow_red, build_edges, safe_edge_iter,
    NODE_TYPE_COLORS, NODE_TYPE_SHAPES, NODE_TYPE_SIZES,
    CLUSTER_PALETTE,
)


def build_static_graph(dill_data: deque, analysis: str, filename: str) -> dict:
    """Build a graph_data dict for QGraphicsView rendering.

    Args:
        dill_data: Deque of iteration-data dicts loaded from a dill history file.
        analysis: Analysis type key (e.g. "master_graph", "clustering").
        filename: Display name for the graph title.

    Returns:
        Dict with "nodes", "edges", and "title" keys for rendering.
    """
    if not dill_data:
        raise ValueError("No data available for analysis.")

    first = dill_data[0] if dill_data else {}
    last = dill_data[-1] if dill_data else {}
    master_graph = last.get("MasterGraph") or first.get("MasterGraph")
    subsystem_details = last.get("SubsystemDetails") or first.get("SubsystemDetails", {})

    if master_graph is None:
        raise ValueError("No MasterGraph found in data.")

    positions = hierarchical_layout(master_graph, subsystem_details)

    dispatch = {
        "master_graph": _graph_master,
        "clustering": _graph_cluster,
        "weighted_degree": _graph_centrality,
        "weighted_in_degree": _graph_centrality,
        "weighted_out_degree": _graph_centrality,
        "pagerank": _graph_centrality,
        "primal_residual": _graph_residual,
        "dual_residual": _graph_residual,
        "compromise": _graph_compromise,
    }
    builder = dispatch.get(analysis)
    if builder is None:
        raise ValueError(f"Unknown static analysis type: {analysis}")

    return builder(master_graph, positions, subsystem_details, last, analysis, filename)


def _graph_master(graph: nx.Graph, positions: dict[str, dict],
                  subsystem_details: dict, iteration_data: dict,
                  analysis: str, filename: str) -> dict:
    """Master graph: node types color-coded, edges by connection type."""
    nodes = []
    for node in graph.nodes():
        node_str = str(node)
        attrs = graph.nodes[node]
        ntype = attrs.get("type", "default")
        detail = subsystem_details.get(node_str, subsystem_details.get(node, {}))
        tooltip_lines = [f"Node: {node_str}"]
        if isinstance(detail, dict):
            for k, v in detail.items():
                tooltip_lines.append(f"  {k}: {v}")

        pos = positions.get(node_str, {"x": 0, "y": 0})
        nodes.append({
            "id": node_str,
            "x": pos["x"], "y": pos["y"],
            "color": NODE_TYPE_COLORS.get(ntype, "#E8684A"),
            "shape": NODE_TYPE_SHAPES.get(ntype, "dot"),
            "size": NODE_TYPE_SIZES.get(ntype, 12),
            "label": node_str,
            "tooltip": "\n".join(tooltip_lines),
        })

    edges = build_edges(graph, positions)
    return {"nodes": nodes, "edges": edges, "title": f"Master Graph — {filename}"}


def _graph_cluster(graph: nx.Graph, positions: dict[str, dict],
                   subsystem_details: dict, iteration_data: dict,
                   analysis: str, filename: str) -> dict:
    """Cluster visualization: nodes colored by cluster assignment."""
    cluster_data = iteration_data.get("ClusterAnalysis", {})
    cluster_nodes = cluster_data.get("nodes", {})

    cluster_map: dict[str, int] = {}
    for key, val in cluster_nodes.items():
        if isinstance(val, dict):
            nid = val.get("id", str(key))
            cluster_map[nid] = val.get("cluster", -1)

    nodes = []
    for node in graph.nodes():
        node_str = str(node)
        cluster_id = cluster_map.get(node_str, -1)
        color = CLUSTER_PALETTE[cluster_id % len(CLUSTER_PALETTE)] if cluster_id >= 0 else "#CCCCCC"
        pos = positions.get(node_str, {"x": 0, "y": 0})
        nodes.append({
            "id": node_str,
            "x": pos["x"], "y": pos["y"],
            "color": color,
            "shape": "dot", "size": 12,
            "label": node_str,
            "tooltip": f"Node: {node_str}\nCluster: {cluster_id}",
        })

    edges = build_edges(graph, positions, default_color="#CCCCCC")
    return {"nodes": nodes, "edges": edges, "title": f"Cluster Analysis — {filename}"}


def _graph_centrality(graph: nx.Graph, positions: dict[str, dict],
                      subsystem_details: dict, iteration_data: dict,
                      analysis: str, filename: str) -> dict:
    """Centrality visualization: node size/color by centrality score."""
    centrality_data = iteration_data.get("CentralityMeasures", {})
    centrality_nodes = centrality_data.get("nodes", {})

    metric_map = {
        "weighted_degree": ("WeightedDegree_centrality", "Weighted Degree Centrality"),
        "weighted_in_degree": ("WeightedInDegree_centrality", "Weighted In-Degree Centrality"),
        "weighted_out_degree": ("WeightedOutDegree_centrality", "Weighted Out-Degree Centrality"),
        "pagerank": ("PageRank_centrality", "PageRank"),
    }
    metric_key, metric_label = metric_map.get(analysis, ("WeightedDegree_centrality", "Weighted Degree Centrality"))

    scores = {}
    for key, val in centrality_nodes.items():
        if isinstance(val, dict):
            node_id = val.get("id", str(key))
            scores[node_id] = val.get(metric_key, 0.0)

    if scores:
        min_s = min(scores.values())
        max_s = max(scores.values())
    else:
        min_s = max_s = 0.0

    nodes = []
    for node in graph.nodes():
        node_str = str(node)
        score = scores.get(node_str, 0.0)
        norm = (score - min_s) / (max_s - min_s + 1e-9) if max_s > min_s else 0.5
        color = green_yellow_red(norm)
        size = 10 + 10 * norm

        pos = positions.get(node_str, {"x": 0, "y": 0})
        nodes.append({
            "id": node_str,
            "x": pos["x"], "y": pos["y"],
            "color": color,
            "shape": "dot", "size": size,
            "label": node_str,
            "tooltip": f"Node: {node_str}\n{metric_label}: {score:.8f}",
        })

    edges = build_edges(graph, positions, default_color="#CCCCCC")
    return {"nodes": nodes, "edges": edges, "title": f"{metric_label} — {filename}"}


def _graph_residual(graph: nx.Graph, positions: dict[str, dict],
                    subsystem_details: dict, iteration_data: dict,
                    analysis: str, filename: str) -> dict:
    """Residual visualization: edge color/width by residual magnitude."""
    residual_data = iteration_data.get("residuals", {})

    edge_norms: dict[str, float] = {}
    for edge_key, val in residual_data.items():
        if isinstance(val, dict):
            residuals = val.get("primal_residuals", val.get("dual_residuals", []))
            if residuals:
                norm = math.sqrt(sum(r ** 2 for r in residuals))
                edge_norms[edge_key] = norm

    if edge_norms:
        min_n = min(edge_norms.values())
        max_n = max(edge_norms.values())
    else:
        min_n = max_n = 0.0

    nodes = []
    for node in graph.nodes():
        node_str = str(node)
        pos = positions.get(node_str, {"x": 0, "y": 0})
        nodes.append({
            "id": node_str,
            "x": pos["x"], "y": pos["y"],
            "color": "#C0C0C0", "shape": "dot", "size": 10,
            "label": node_str,
            "tooltip": f"Node: {node_str}",
        })

    edges = []
    for u, v, *_ in safe_edge_iter(graph):
        edge_key = f"{u}-{v}"
        alt_key = f"{v}-{u}"
        norm = edge_norms.get(edge_key, edge_norms.get(alt_key, 0.0))
        normalized = (norm - min_n) / (max_n - min_n + 1e-9) if max_n > min_n else 0.0
        color = green_yellow_red(normalized)
        width = 1 + 4 * normalized

        u_str, v_str = str(u), str(v)
        pos_u = positions.get(u_str, {"x": 0, "y": 0})
        pos_v = positions.get(v_str, {"x": 0, "y": 0})
        edges.append({
            "source_x": pos_u["x"], "source_y": pos_u["y"],
            "target_x": pos_v["x"], "target_y": pos_v["y"],
            "color": color, "width": width,
            "tooltip": f"Edge: {u_str} → {v_str}\nL2 Norm: {norm:.6f}",
        })

    label = "Primal Residual" if analysis == "primal_residual" else "Dual Residual"
    return {"nodes": nodes, "edges": edges, "title": f"{label} (Static) — {filename}"}


def _graph_compromise(graph: nx.Graph, positions: dict[str, dict],
                      subsystem_details: dict, iteration_data: dict,
                      analysis: str, filename: str) -> dict:
    """Compromise visualization: edge color/width by compromise magnitude."""
    nodes = []
    for node in graph.nodes():
        node_str = str(node)
        pos = positions.get(node_str, {"x": 0, "y": 0})
        nodes.append({
            "id": node_str,
            "x": pos["x"], "y": pos["y"],
            "color": "#C0C0C0", "shape": "dot", "size": 10,
            "label": node_str,
            "tooltip": f"Node: {node_str}",
        })

    edge_compromises: dict[str, float] = {}
    for u, v, *rest in safe_edge_iter(graph):
        data = rest[-1] if rest else {}
        parent_comp = data.get("parent_mapped_compromise") or data.get("parent_shared_compromise")
        child_comp = data.get("child_mapped_compromise") or data.get("child_shared_compromise")
        if parent_comp is not None and child_comp is not None:
            all_vals = []
            if isinstance(parent_comp, list):
                all_vals.extend([abs(v) for v in parent_comp if v is not None])
            if isinstance(child_comp, list):
                all_vals.extend([abs(v) for v in child_comp if v is not None])
            if all_vals:
                edge_compromises[f"{u}-{v}"] = max(all_vals)

    if edge_compromises:
        min_c = min(edge_compromises.values())
        max_c = max(edge_compromises.values())
    else:
        min_c = max_c = 0.0

    edges = []
    for u, v, *_ in safe_edge_iter(graph):
        edge_key = f"{u}-{v}"
        comp = edge_compromises.get(edge_key, 0.0)
        normalized = (comp - min_c) / (max_c - min_c + 1e-9) if max_c > min_c else 0.0
        color = green_yellow_red(normalized)
        width = 1 + 4 * normalized

        u_str, v_str = str(u), str(v)
        pos_u = positions.get(u_str, {"x": 0, "y": 0})
        pos_v = positions.get(v_str, {"x": 0, "y": 0})
        edges.append({
            "source_x": pos_u["x"], "source_y": pos_u["y"],
            "target_x": pos_v["x"], "target_y": pos_v["y"],
            "color": color, "width": width,
            "tooltip": f"Edge: {u_str} → {v_str}\nCompromise: {comp:.6f}",
        })

    return {"nodes": nodes, "edges": edges, "title": f"Compromise Measure (Static) — {filename}"}

```
