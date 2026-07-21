---
title: PlotConfig (Source)
---

← Back to [PlotConfig documentation](PlotConfig.md)

# PlotConfig - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\models\PlotConfig.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Dataclass models for plot configuration, fonts, lines, and reference lines."""
from dataclasses import dataclass, field


@dataclass
class FontConfig:
    """Font configuration for a single text element."""
    family: str = "Segoe UI"
    size: int = 12
    weight: str = "normal"  # "normal" | "bold"


@dataclass
class LineConfig:
    """Configuration for a single plot line."""
    item_path: str
    label: str
    style: str = "-"          # "-", "--", "-.", ":"
    width: float = 2.0
    color: str | None = None  # None → auto-assign from palette
    markers: bool = True      # show point markers along the line


@dataclass
class ReferenceLine:
    """A horizontal reference line on the plot."""
    name: str = ""
    value: float = 0.0
    color: str = "red"
    style: str = "-"
    width: float = 1.5
    enabled: bool = True
    markers: bool = False     # show point markers along the reference line


@dataclass
class PlotConfig:
    """Complete plot configuration state."""

    # Y-axis arrangement
    plot_type: str = "shared"  # "shared" | "independent" | "centered" | "stacked"
    log_scale: bool = False

    # X-axis type
    x_axis_type: str = "queue_count"  # "queue_count" | "combined_ticks" | "equispaced_major" | "cumulative_runtime" | "cumulative_evaluations"

    # Display options
    show_legend: bool = True
    show_grid: bool = False
    legend_position: str = "upper right"

    # Custom labels
    custom_x_label: str = ""
    custom_y_label: str = ""
    custom_title: str = ""
    stacked_titles: list[str] = field(default_factory=list)
    stacked_y_labels: list[str] = field(default_factory=list)
    independent_y_labels: list[str] = field(default_factory=list)

    # Font (per-element)
    title_font: FontConfig = field(default_factory=FontConfig)
    x_label_font: FontConfig = field(default_factory=FontConfig)
    y_label_font: FontConfig = field(default_factory=FontConfig)
    legend_font: FontConfig = field(default_factory=FontConfig)
    x_tick_label_font: FontConfig = field(default_factory=FontConfig)
    y_tick_label_font: FontConfig = field(default_factory=FontConfig)
    x_tick_size: int = 8      # tick marker length in px
    y_tick_size: int = 8      # tick marker length in px

    # Per-line overrides (keyed by item_path)
    line_configs: dict[str, LineConfig] = field(default_factory=dict)

    # Reference lines
    reference_lines: list[ReferenceLine] = field(default_factory=list)

```
