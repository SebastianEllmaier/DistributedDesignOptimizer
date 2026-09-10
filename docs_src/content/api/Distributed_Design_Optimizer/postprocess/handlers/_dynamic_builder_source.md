---
title: _dynamic_builder (Source)
---

← Back to [_dynamic_builder documentation](_dynamic_builder.md)

# _dynamic_builder - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\handlers\_dynamic_builder.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Dynamic HTML builders for topology analysis."""

import math
from collections import deque

import numpy as np

from ._plot_builder import _get_plotly_template

_PLOTLY_CONFIG: dict = {
    "responsive": True,
    "displaylogo": False,
    "displayModeBar": True,
    "toImageButtonOptions": {
        "format": "svg",
        "filename": "ddo_plot",
        "width": 1200,
        "height": 700,
        "scale": 1,
    },
}


# ==================================================================
# Interactive HTML builders (Plotly)
# ==================================================================

def build_dynamic_html(dill_data: deque, analysis: str, filename: str) -> str:
    """Build interactive Plotly HTML for dynamic analyses.

    Args:
        dill_data: Deque of per-iteration dicts loaded from a dill history file.
        analysis: Analysis type key (e.g. "clustering", "pagerank").
        filename: Original filename used in the plot title.

    Returns:
        Full HTML string containing the interactive Plotly visualisation.
    """
    dispatch = {
        "clustering": _html_cluster_flow,
        "weighted_degree": lambda d, f: _html_centrality_heatmap(d, "WeightedDegree_centrality", "Weighted Degree", f),
        "weighted_in_degree": lambda d, f: _html_centrality_heatmap(d, "WeightedInDegree_centrality", "Weighted In-Degree", f),
        "weighted_out_degree": lambda d, f: _html_centrality_heatmap(d, "WeightedOutDegree_centrality", "Weighted Out-Degree", f),
        "pagerank": lambda d, f: _html_centrality_heatmap(d, "PageRank_centrality", "PageRank", f),
        "primal_residual": lambda d, f: _html_residual_evolution(d, "primal", f),
        "dual_residual": lambda d, f: _html_residual_evolution(d, "dual", f),
        "compromise": _html_compromise_evolution,
    }
    builder = dispatch.get(analysis)
    if builder is None:
        raise ValueError(f"Unknown dynamic analysis type: {analysis}")
    return builder(dill_data, filename)


# ==================================================================
# HTML implementations
# ==================================================================

def _html_centrality_heatmap(dill_data: deque, metric_key: str,
                             metric_label: str, filename: str) -> str:
    import plotly.graph_objects as go

    all_nodes = set()
    iterations = []
    for iteration in dill_data:
        centrality = iteration.get("CentralityMeasures", {})
        nodes_data = centrality.get("nodes", {})
        for key, val in nodes_data.items():
            if isinstance(val, dict):
                all_nodes.add(val.get("id", str(key)))
        iterations.append(nodes_data)

    node_list = sorted(all_nodes)
    if not node_list or not iterations:
        raise ValueError("No centrality data available.")

    node_index = {nid: idx for idx, nid in enumerate(node_list)}
    z = np.zeros((len(node_list), len(iterations)))
    for j, nodes_data in enumerate(iterations):
        for key, val in nodes_data.items():
            if isinstance(val, dict):
                node_id = val.get("id", str(key))
                idx = node_index.get(node_id)
                if idx is not None:
                    z[idx, j] = val.get(metric_key, 0.0)

    fig = go.Figure(data=go.Heatmap(
        z=z, x=list(range(len(iterations))), y=node_list,
        colorscale="Viridis", colorbar=dict(title=metric_label),
        hovertemplate="Iteration: %{x}<br>Node: %{y}<br>Value: %{z:.6f}<extra></extra>",
    ))
    fig.update_layout(
        title=f"{metric_label} Centrality Evolution — {filename}",
        xaxis_title="Iteration", yaxis_title="Node ID",
        template=_get_plotly_template(), height=max(500, len(node_list) * 30),
    )
    # Inline plotly.js (no CDN) so the chart renders without an internet connection.
    return fig.to_html(include_plotlyjs=True, full_html=True,
                       config=_PLOTLY_CONFIG)


def _html_residual_evolution(dill_data: deque, residual_type: str, filename: str) -> str:
    import plotly.graph_objects as go

    edge_histories: dict[str, list[float]] = {}
    for iteration in dill_data:
        residuals = iteration.get("residuals", {})
        for edge_key, val in residuals.items():
            if isinstance(val, dict):
                key_name = "primal_residuals" if residual_type == "primal" else "dual_residuals"
                residual_vec = val.get(key_name, [])
                norm = math.sqrt(sum(r ** 2 for r in residual_vec)) if residual_vec else 0.0
                edge_histories.setdefault(edge_key, []).append(norm)

    if not edge_histories:
        raise ValueError(f"No {residual_type} residual data available.")

    label = "Primal Residual" if residual_type == "primal" else "Dual Residual"
    fig = go.Figure()
    for edge_key, norms in sorted(edge_histories.items()):
        fig.add_trace(go.Scatter(
            x=list(range(len(norms))), y=norms, mode="lines+markers",
            name=edge_key, marker=dict(size=3),
        ))
    fig.update_layout(
        title=f"{label} Evolution — {filename}",
        xaxis_title="Iteration", yaxis_title=f"{label} L2 Norm",
        yaxis_type="log", template=_get_plotly_template(),
        hovermode="x unified", height=600,
    )
    # Inline plotly.js (no CDN) so the chart renders without an internet connection.
    return fig.to_html(include_plotlyjs=True, full_html=True,
                       config=_PLOTLY_CONFIG)


def _html_cluster_flow(dill_data: deque, filename: str) -> str:
    import plotly.graph_objects as go

    all_nodes = set()
    cluster_history: list[dict] = []
    for iteration in dill_data:
        cluster_data = iteration.get("ClusterAnalysis", {})
        nodes_data = cluster_data.get("nodes", {})
        assignments = {}
        for key, val in nodes_data.items():
            if isinstance(val, dict):
                node_id = val.get("id", str(key))
                assignments[node_id] = val.get("cluster", -1)
                all_nodes.add(node_id)
        cluster_history.append(assignments)

    if not cluster_history or not all_nodes:
        raise ValueError("No cluster data available.")

    node_list = sorted(all_nodes)
    z = np.zeros((len(node_list), len(cluster_history)))
    for j, assignments in enumerate(cluster_history):
        for i, node_id in enumerate(node_list):
            z[i, j] = assignments.get(node_id, -1)

    fig = go.Figure(data=go.Heatmap(
        z=z, x=list(range(len(cluster_history))), y=node_list,
        colorscale="tab10", colorbar=dict(title="Cluster ID"),
        hovertemplate="Iteration: %{x}<br>Node: %{y}<br>Cluster: %{z}<extra></extra>",
    ))
    fig.update_layout(
        title=f"Cluster Assignment Evolution — {filename}",
        xaxis_title="Iteration", yaxis_title="Node ID",
        template=_get_plotly_template(), height=max(500, len(node_list) * 30),
    )
    # Inline plotly.js (no CDN) so the chart renders without an internet connection.
    return fig.to_html(include_plotlyjs=True, full_html=True,
                       config=_PLOTLY_CONFIG)


def _html_compromise_evolution(dill_data: deque, filename: str) -> str:
    import plotly.graph_objects as go

    edge_histories: dict[str, list[float]] = {}
    for iteration in dill_data:
        master_graph = iteration.get("MasterGraph")
        if master_graph is None:
            continue
        for u, v, key, data in master_graph.edges(keys=True, data=True):
            edge_id = f"{u}-{v}"
            parent_comp = data.get("parent_mapped_compromise") or data.get("parent_shared_compromise")
            child_comp = data.get("child_mapped_compromise") or data.get("child_shared_compromise")

            if parent_comp is not None:
                p_key = f"{edge_id} (parent)"
                vals = [x for x in (parent_comp if isinstance(parent_comp, list) else [parent_comp]) if x is not None]
                if vals:
                    edge_histories.setdefault(p_key, []).append(float(np.mean(np.abs(vals))))
            if child_comp is not None:
                c_key = f"{edge_id} (child)"
                vals = [x for x in (child_comp if isinstance(child_comp, list) else [child_comp]) if x is not None]
                if vals:
                    edge_histories.setdefault(c_key, []).append(float(np.mean(np.abs(vals))))

    if not edge_histories:
        raise ValueError("No compromise data available.")

    fig = go.Figure()
    for edge_key, ratios in sorted(edge_histories.items()):
        fig.add_trace(go.Scatter(
            x=list(range(len(ratios))), y=ratios, mode="lines+markers",
            name=edge_key, marker=dict(size=3),
        ))
    fig.add_hline(y=0.5, line_dash="dash", line_color="gray", opacity=0.6)
    fig.update_layout(
        title=f"Compromise Ratio Evolution — {filename}",
        xaxis_title="Iteration", yaxis_title="Mean |Compromise Ratio|",
        template=_get_plotly_template(), hovermode="x unified", height=600,
    )
    # Inline plotly.js (no CDN) so the chart renders without an internet connection.
    return fig.to_html(include_plotlyjs=True, full_html=True,
                       config=_PLOTLY_CONFIG)


```
