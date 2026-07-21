---
title: _axis_aligner (Source)
---

← Back to [_axis_aligner documentation](_axis_aligner.md)

# _axis_aligner - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\handlers\_axis_aligner.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""X-axis generation and multi-file alignment logic for PlotHandler.

All functions are pure data transformations — no plotting library dependencies.
"""

import logging
from dataclasses import dataclass

import numpy as np

from ..models.PlotConfig import PlotConfig

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AlignedAxisData:
    """Result of :func:`build_aligned_data` — all data needed to render aligned plots."""

    x_positions: list[float]
    aligned_y: list[list[float]]
    major_positions: list[int]
    major_labels: list[str]
    minor_positions: list[float]
    hover_labels: list[str]


def generate_x_values(values: list[float], config: PlotConfig,
                      series_labels: list[dict] | None = None) -> list[float]:
    """Generate X-axis values based on the configured x_axis_type.

    Args:
        values: Y-values whose length determines the number of x-positions.
        config: Plot configuration containing the x_axis_type setting.
        series_labels: Optional per-iteration metadata dicts for cumulative modes.

    Returns:
        List of float x-coordinates, one per value.
    """
    n = len(values)
    labels = series_labels or []
    if config.x_axis_type == "cumulative_runtime":
        return cumulative_from_labels(n, "innerloop_itr_runtime", labels)
    if config.x_axis_type == "cumulative_evaluations":
        return cumulative_from_labels(n, "innerloop_itr_numberofdesignvariableevaluations", labels)
    # "queue_count", "combined_ticks", "equispaced_major" — sequential
    return [float(i) for i in range(n)]


def cumulative_from_labels(n: int, key: str, labels: list[dict]) -> list[float]:
    """Build cumulative x-values from iteration label metadata.

    Args:
        n: Number of data points to produce.
        key: Metadata key to accumulate (e.g. runtime or evaluation count).
        labels: Per-iteration metadata dicts containing the accumulation key.

    Returns:
        List of cumulative float values with length *n*.
    """
    cumulative = 0.0
    has_data = False
    result: list[float] = []
    for i in range(n):
        if labels and i < len(labels):
            val = labels[i].get(key)
            if val is not None:
                try:
                    cumulative += float(val)
                    has_data = True
                except (TypeError, ValueError):
                    pass
        result.append(cumulative)
    if not has_data:
        logger.warning(f"No '{key}' data available in iteration labels — x-axis will be flat.")
    return result


def get_x_label(config: PlotConfig) -> str:
    """Return appropriate X-axis label based on x_axis_type.

    Args:
        config: Plot configuration containing x_axis_type and custom_x_label.

    Returns:
        Human-readable axis label string.
    """
    if config.custom_x_label:
        return config.custom_x_label
    # Tick legend embedded inline in the label: a thin tick glyph is placed
    # directly after each word — after "Outer" in the major-tick colour and
    # after "Innerloop" in the minor-tick colour. Colours are sourced from the
    # same theme used by _add_aligned_ticks (single source of truth) so the
    # legend always matches the rendered ticks. The inner glyph is rendered at
    # 50% height to mirror the real minor ticks (which are 50% of the majors).
    # Rendered via Plotly's HTML subset.
    from ..styles.Theme import get_chart_colors
    chart_colors = get_chart_colors()
    major_color = chart_colors["axis_line"]
    minor_color = chart_colors["minor_tick"]
    iter_label = (
        f'Outer <span style="color:{major_color}">&#9615;</span> and '
        f'Innerloop <span style="color:{minor_color};font-size:0.5em">&#9615;</span> '
        'Iterations'
    )
    labels = {
        "queue_count": "Sequence Index",
        "combined_ticks": iter_label,
        "equispaced_major": iter_label,
        "cumulative_runtime": "Runtime in ms",
        "cumulative_evaluations": "Number of Evaluations",
    }
    return labels.get(config.x_axis_type, "Sequence Index")


def build_aligned_data(plottable_data: list[tuple[str, list[float]]],
                       config: PlotConfig,
                       labels_map: dict[str, list[dict]]) -> AlignedAxisData:
    """Build a unified x-axis across all series using outerloop/innerloop alignment.

    Args:
        plottable_data: List of (item_path, y_values) tuples for each series.
        config: Plot configuration controlling axis type and spacing.
        labels_map: Mapping from entry ID to per-iteration metadata dicts.

    Returns:
        An :class:`AlignedAxisData` containing unified x-positions,
        NaN-padded y-arrays, and major/minor tick information.
    """
    series_ticks_and_values: list[tuple[list, list[list], list[float], dict]] = []

    for item_path, values in plottable_data:
        labels = get_series_labels(item_path, labels_map)
        outer_itrs: list = []
        for i in range(len(values)):
            if i < len(labels):
                outer = labels[i].get("outerloop_itr")
                outer_itrs.append(outer if outer is not None else i)
            else:
                outer_itrs.append(i)

        major_ticks: list = []
        minor_ticks_per_major: list[list] = []
        prev_outer = None
        current_minors: list = []
        for outer in outer_itrs:
            if outer != prev_outer:
                if prev_outer is not None:
                    minor_ticks_per_major.append(current_minors)
                major_ticks.append(outer)
                current_minors = []
                prev_outer = outer
            else:
                current_minors.append(len(current_minors))
        if prev_outer is not None:
            minor_ticks_per_major.append(current_minors)

        # First-occurrence index per major value (mirrors list.index() / `in`)
        # so downstream lookups are O(1) instead of O(n) list scans.
        major_index: dict = {}
        for idx, m in enumerate(major_ticks):
            if m not in major_index:
                major_index[m] = idx

        series_ticks_and_values.append((major_ticks, minor_ticks_per_major, values, major_index))

    # Union all major tick values
    all_major: list = []
    seen_major: set = set()
    for major_ticks, _, _, _ in series_ticks_and_values:
        for m in major_ticks:
            if m not in seen_major:
                all_major.append(m)
                seen_major.add(m)
    all_major.sort()

    # Max minors after each major tick across all series
    max_minors_after: list[int] = []
    for i, major in enumerate(all_major):
        max_count = 0
        for major_ticks, minor_ticks_per_major, _, major_index in series_ticks_and_values:
            idx = major_index.get(major)
            if idx is not None:
                count = len(minor_ticks_per_major[idx]) if idx < len(minor_ticks_per_major) else 0
                max_count = max(max_count, count)
        max_minors_after.append(max_count)

    # In "combined_ticks" mode every tick is an equispaced integer slot, so the
    # final outer iteration's inner ticks can also be placed. In "equispaced_major"
    # mode minors are fractional subdivisions between consecutive majors, so the
    # last outer's minors have no enclosing interval and are dropped.
    include_last_minors = (config.x_axis_type == "combined_ticks")

    # Build unified_x (minors between majors; last-outer minors only when included)
    unified_x: list[tuple] = []
    for i, major in enumerate(all_major):
        unified_x.append((major, None))
        if include_last_minors or i < len(all_major) - 1:
            for m in range(max_minors_after[i]):
                unified_x.append((major, m))

    # Align each series' values onto the unified grid
    aligned_y_list: list[list[float]] = []
    for major_ticks, minor_ticks_per_major, values, major_index in series_ticks_and_values:
        y_aligned: list[float] = []
        val_idx = 0
        for i, major in enumerate(all_major):
            major_idx = major_index.get(major)
            if major_idx is not None:
                if val_idx < len(values):
                    y_aligned.append(values[val_idx])
                    val_idx += 1
                else:
                    y_aligned.append(float('nan'))
                # Place minors between majors; last-outer minors only when included
                if include_last_minors or i < len(all_major) - 1:
                    minors = minor_ticks_per_major[major_idx] if major_idx < len(minor_ticks_per_major) else []
                    for m in range(max_minors_after[i]):
                        if m < len(minors) and val_idx < len(values):
                            y_aligned.append(values[val_idx])
                            val_idx += 1
                        else:
                            y_aligned.append(float('nan'))
            else:
                y_aligned.append(float('nan'))
                if include_last_minors or i < len(all_major) - 1:
                    for m in range(max_minors_after[i]):
                        y_aligned.append(float('nan'))
        aligned_y_list.append(y_aligned)

    # Compute x positions and tick info
    equispaced = (config.x_axis_type == "equispaced_major")

    # Build hover labels for each position (Outer N or Outer N, Inner M)
    hover_labels: list[str] = []

    if equispaced:
        x_positions: list[float] = []
        major_positions: list[int] = []
        minor_positions: list[float] = []
        major_labels_out: list[str] = []
        for i, major in enumerate(all_major):
            major_positions.append(i)
            major_labels_out.append(str(major))
            x_positions.append(float(i))
            hover_labels.append(f"Outer {major}")
            if include_last_minors or i < len(all_major) - 1:
                n_minors = max_minors_after[i]
                for m in range(n_minors):
                    pos = i + (m + 1) / (n_minors + 1)
                    x_positions.append(pos)
                    minor_positions.append(pos)
                    hover_labels.append(f"Outer {major}, Inner {m + 1}")
    else:
        x_positions = [float(i) for i in range(len(unified_x))]
        major_positions: list[int] = []
        minor_positions: list[float] = []
        major_labels_out: list[str] = []
        for idx, ux in enumerate(unified_x):
            if ux[1] is None:
                major_positions.append(idx)
                major_labels_out.append(str(ux[0]))
                hover_labels.append(f"Outer {ux[0]}")
            else:
                minor_positions.append(float(idx))
                hover_labels.append(f"Outer {ux[0]}, Inner {ux[1] + 1}")

    return AlignedAxisData(
        x_positions=x_positions,
        aligned_y=aligned_y_list,
        major_positions=major_positions,
        major_labels=major_labels_out,
        minor_positions=minor_positions,
        hover_labels=hover_labels,
    )


def get_series_labels(item_path: str, labels_map: dict[str, list[dict]]) -> list[dict]:
    """Get iteration labels for the entry that owns this series.

    Args:
        item_path: Slash-delimited path whose first segment is the entry ID.
        labels_map: Mapping from entry ID to per-iteration metadata dicts.

    Returns:
        List of label dicts for the matching entry, or an empty list.
    """
    entry_id = item_path.split("/", 1)[0]
    return labels_map.get(entry_id, [])

```
