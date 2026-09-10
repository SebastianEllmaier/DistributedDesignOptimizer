# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Unified dispatch registry for topology analyses.

Maps (analysis_type, mode) to (builder_function, output_type) so that
TopologyHandler doesn't need to branch on mode itself.
"""

from ._static_graph_builder import build_static_graph
from ._dynamic_builder import build_dynamic_html

# (analysis, mode) -> (build_fn, output_type)
# "master_graph" is always static regardless of mode.
_REGISTRY: dict[tuple[str, str], tuple] = {}

_ANALYSIS_TYPES = [
    "master_graph",
    "clustering",
    "weighted_degree",
    "weighted_in_degree",
    "weighted_out_degree",
    "pagerank",
    "primal_residual",
    "dual_residual",
    "compromise",
]

for _a in _ANALYSIS_TYPES:
    _REGISTRY[(_a, "static")] = (build_static_graph, "graph")
    if _a == "master_graph":
        # master_graph is always static, even when mode=dynamic
        _REGISTRY[(_a, "dynamic")] = (build_static_graph, "graph")
    else:
        _REGISTRY[(_a, "dynamic")] = (build_dynamic_html, "html")


def resolve(analysis: str, mode: str):
    """Return (build_fn, output_type) for the given analysis/mode pair.

    Args:
        analysis: Analysis type key (e.g. "master_graph", "clustering").
        mode: Either "static" or "dynamic".

    Raises:
        ValueError: If the combination is unknown.
    """
    key = (analysis, mode)
    entry = _REGISTRY.get(key)
    if entry is None:
        raise ValueError(f"Unknown topology analysis: {analysis!r} / {mode!r}")
    return entry
