# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""
Graph layout and color utility functions for topology analysis.
"""

import networkx as nx

# Color palettes matching the original LoadGraph visuals
NODE_TYPE_COLORS = {
    "discipline": "#5B8FF9",
    "optimizer": "#61DDAA",
    "data": "#F6BD16",
}
NODE_TYPE_SHAPES = {
    "discipline": "dot",
    "optimizer": "triangle",
    "data": "square",
}
NODE_TYPE_SIZES = {
    "discipline": 14,
    "optimizer": 14,
    "data": 11,
}
EDGE_TYPE_COLORS = {
    "discipline_connection": "#9467bd",
    "optimizer_connection": "#8c564b",
}
CLUSTER_PALETTE = [
    "#5B8FF9", "#61DDAA", "#F6BD16", "#E8684A", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
]


def hierarchical_layout(graph: nx.Graph, subsystem_details: dict) -> dict[str, dict]:
    """Compute hierarchical positions from subsystem level data.

    Args:
        graph: The NetworkX graph whose nodes will be positioned.
        subsystem_details: Mapping of node id to detail dicts containing a ``Level`` key.

    Returns:
        A dict mapping node id to ``{"x": float, "y": float}`` position dicts.
    """
    levels: dict[int, list] = {}
    for node in graph.nodes():
        node_str = str(node)
        detail = subsystem_details.get(node_str, subsystem_details.get(node, {}))
        level = detail.get("Level", 0) if isinstance(detail, dict) else 0
        levels.setdefault(level, []).append(node_str)

    positions: dict[str, dict] = {}
    for level_idx, level_key in enumerate(sorted(levels.keys())):
        nodes_in_level = sorted(levels[level_key])
        n = len(nodes_in_level)
        start_x = -(n - 1) * 200
        for j, node_id in enumerate(nodes_in_level):
            positions[node_id] = {"x": start_x + j * 400, "y": level_idx * 300}
    return positions


def green_yellow_red(normalized: float) -> str:
    """Map 0..1 to a green-yellow-red hex color.

    Args:
        normalized: A value in [0, 1] where 0 is green and 1 is red.

    Returns:
        A CSS hex color string interpolated along the green-yellow-red gradient.
    """
    normalized = max(0.0, min(1.0, normalized))
    if normalized <= 0.5:
        r = int(255 * (normalized / 0.5))
        g = 255
    else:
        r = 255
        g = int(255 * (1.0 - (normalized - 0.5) / 0.5))
    return f"#{r:02x}{g:02x}{0:02x}"


def safe_edge_iter(graph: nx.Graph, *, data: bool = False) -> list:
    """Iterate edges safely for both multi and non-multi graphs.

    Args:
        graph: A NetworkX graph (regular or multigraph).

    Returns:
        A list of edge tuples, each containing ``(u, v, key)`` or
        ``(u, v, key, data)`` depending on the *data* flag.
    """
    if data:
        try:
            return list(graph.edges(keys=True, data=True))
        except TypeError:
            return [(u, v, 0, d) for u, v, d in graph.edges(data=True)]
    else:
        try:
            return list(graph.edges(keys=True))
        except TypeError:
            return [(u, v, 0) for u, v in graph.edges()]


def build_edges(graph: nx.Graph, positions: dict[str, dict],
                default_color: str | None = None) -> list[dict]:
    """Build an edge list with source/target coordinates for GraphWidget.

    Args:
        graph: The NetworkX graph to extract edges from.
        positions: Mapping of node id to ``{"x": float, "y": float}`` dicts.
        default_color: Optional fallback CSS color for edges without a type.

    Returns:
        A list of dicts, each containing source/target coordinates, color,
        width, and tooltip for one edge.
    """
    edges: list[dict] = []
    for u, v, key, data in safe_edge_iter(graph, data=True):
        u_str, v_str = str(u), str(v)
        pos_u = positions.get(u_str, {"x": 0, "y": 0})
        pos_v = positions.get(v_str, {"x": 0, "y": 0})
        etype = data.get("type", "")
        color = default_color or EDGE_TYPE_COLORS.get(etype, "#CCCCCC")
        width = 2 if etype in EDGE_TYPE_COLORS else 1

        tooltip_lines = [f"Edge: {u_str} → {v_str}"]
        if etype:
            tooltip_lines.append(f"Type: {etype}")
        for attr_key in ("primalmappedresidual", "primalsharedresidual", "Dimensionality"):
            if attr_key in data:
                tooltip_lines.append(f"{attr_key}: {data[attr_key]}")

        edges.append({
            "source_x": pos_u["x"], "source_y": pos_u["y"],
            "target_x": pos_v["x"], "target_y": pos_v["y"],
            "color": color, "width": width,
            "tooltip": "\n".join(tooltip_lines),
        })
    return edges
