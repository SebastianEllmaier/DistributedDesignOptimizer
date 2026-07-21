---
title: _plot_customizer (Source)
---

← Back to [_plot_customizer documentation](_plot_customizer.md)

# _plot_customizer - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\handlers\_plot_customizer.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Plot customization helpers for PlotHandler — Plotly implementation."""

import logging

import plotly.graph_objects as go

from ..models.PlotConfig import PlotConfig
from ._plot_builder import MPL_TO_PLOTLY_DASH, tick_width_for

logger = logging.getLogger(__name__)


def apply_font(fig: go.Figure, config: PlotConfig) -> None:
    """Apply per-element font settings to all text elements.

    Args:
        fig: Plotly Figure to update in place.
        config: Plot configuration with font settings.
    """
    fig.update_layout(font=dict(
        family=config.title_font.family,
        size=config.title_font.size,
    ))
    # Apply tick label font sizes and tick marker lengths. The tick line width
    # scales with the tick length (via tick_width_for) so the marker's
    # length:width ratio stays constant as the tick size changes.
    fig.update_xaxes(
        tickfont=dict(size=config.x_tick_label_font.size),
        ticklen=config.x_tick_size,
        tickwidth=tick_width_for(config.x_tick_size),
    )
    fig.update_yaxes(
        tickfont=dict(size=config.y_tick_label_font.size),
        ticklen=config.y_tick_size,
        tickwidth=tick_width_for(config.y_tick_size),
    )


def apply_labels(fig: go.Figure, config: PlotConfig) -> None:
    """Apply custom axis labels and title.

    Args:
        fig: Plotly Figure to update in place.
        config: Plot configuration with custom label text.
    """
    updates: dict = {}
    if config.custom_x_label:
        updates["xaxis_title"] = dict(
            text=config.custom_x_label,
            font=dict(family=config.x_label_font.family, size=config.x_label_font.size),
        )
    if config.custom_y_label:
        updates["yaxis_title"] = dict(
            text=config.custom_y_label,
            font=dict(family=config.y_label_font.family, size=config.y_label_font.size),
        )
    if config.custom_title:
        updates["title"] = dict(
            text=config.custom_title,
            font=dict(family=config.title_font.family, size=config.title_font.size),
            x=0.5,
            xanchor="center",
        )
    if updates:
        fig.update_layout(**updates)


def apply_reference_lines(fig: go.Figure, config: PlotConfig) -> None:
    """Add / replace horizontal reference lines as traces (shown in legend).

    Args:
        fig: Plotly Figure to update in place.
        config: Plot configuration with reference line definitions.
    """
    # Remove previous reference line traces
    fig.data = tuple(t for t in fig.data
                     if not (hasattr(t, 'meta') and isinstance(t.meta, dict)
                             and t.meta.get('_ref_line')))
    # Remove previous reference line shapes
    if fig.layout.shapes:
        fig.layout.shapes = tuple(
            s for s in fig.layout.shapes
            if not (hasattr(s, 'name') and s.name and s.name.startswith('_ref_'))
        )
    for i, ref in enumerate(config.reference_lines):
        if ref.enabled:
            label = ref.name or f"ref {ref.value}"
            # Collect ALL unique x-values from existing data traces
            # so the ref line appears in hover at every x-tick
            all_x = set()
            for t in fig.data:
                if hasattr(t, 'x') and t.x is not None:
                    if hasattr(t, 'meta') and isinstance(t.meta, dict) and t.meta.get('_ref_line'):
                        continue
                    all_x.update(v for v in t.x if v is not None)
            x_vals = sorted(all_x) if all_x else [0, 1]
            # Add as a real scatter trace at every x position
            fig.add_trace(go.Scatter(
                x=x_vals,
                y=[ref.value] * len(x_vals),
                mode="lines+markers" if ref.markers else "lines",
                name=label,
                line=dict(dash=ref.style, color=ref.color, width=ref.width),
                marker=dict(size=4, color=ref.color),
                showlegend=True,
                meta={"_ref_line": True},
            ))


def apply_per_line_styles(fig: go.Figure, config: PlotConfig) -> None:
    """Update trace colors, dash styles, and widths from per-line config.

    Args:
        fig: Plotly Figure to update in place.
        config: Plot configuration with per-line style overrides.
    """
    for trace in fig.data:
        if not hasattr(trace, 'name') or trace.name is None:
            continue
        for path, lc in config.line_configs.items():
            if trace.name == lc.label:
                dash = MPL_TO_PLOTLY_DASH.get(lc.style, lc.style)
                trace.update(line=dict(dash=dash, width=lc.width))
                # Toggle point markers without discarding line styling
                if "markers" in (trace.mode or ""):
                    trace.update(mode="lines+markers" if lc.markers else "lines")
                elif lc.markers:
                    trace.update(mode="lines+markers")
                if lc.color:
                    trace.update(line_color=lc.color, marker_color=lc.color)
                break


def apply_legend(fig: go.Figure, config: PlotConfig) -> None:
    """Show / hide legend and apply themed positioning.

    Args:
        fig: Plotly Figure to update in place.
        config: Plot configuration with legend visibility and position.
    """
    if not config.show_legend:
        fig.update_layout(showlegend=False)
        return

    from ..styles.Theme import get_chart_colors
    colors = get_chart_colors()

    # Map legend position strings to Plotly x/y anchor
    _POS_MAP = {
        "upper right": dict(x=1, y=1, xanchor="right", yanchor="top"),
        "upper left": dict(x=0, y=1, xanchor="left", yanchor="top"),
        "lower right": dict(x=1, y=0, xanchor="right", yanchor="bottom"),
        "lower left": dict(x=0, y=0, xanchor="left", yanchor="bottom"),
        "upper center": dict(x=0.5, y=1, xanchor="center", yanchor="top"),
        "lower center": dict(x=0.5, y=0, xanchor="center", yanchor="bottom"),
        "center left": dict(x=0, y=0.5, xanchor="left", yanchor="middle"),
        "center right": dict(x=1, y=0.5, xanchor="right", yanchor="middle"),
    }
    pos = _POS_MAP.get(config.legend_position,
                       dict(x=1, y=1, xanchor="right", yanchor="top"))

    fig.update_layout(
        showlegend=True,
        legend=dict(
            bgcolor=colors["legend_face"],
            bordercolor=colors["legend_edge"],
            borderwidth=1,
            font=dict(
                color=colors["legend_text"],
                family=config.legend_font.family,
                size=config.legend_font.size,
            ),
            **pos,
        ),
    )


def apply_all(fig: go.Figure, config: PlotConfig) -> None:
    """Apply all customizations to a Plotly figure in order.

    Args:
        fig: Plotly Figure to update in place.
        config: Plot configuration with all customization settings.
    """
    apply_font(fig, config)
    apply_labels(fig, config)
    apply_reference_lines(fig, config)
    apply_per_line_styles(fig, config)
    apply_legend(fig, config)

```
