# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Plot type builders for PlotHandler — Plotly implementation.

Produces plotly.graph_objects.Figure objects for shared, independent, centered,
and stacked plot types.
"""

import logging
import math

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ..models.PlotConfig import PlotConfig, FontConfig
from ._axis_aligner import (
    generate_x_values, get_x_label, build_aligned_data,
    AlignedAxisData, get_series_labels,
)

logger = logging.getLogger(__name__)

# Mapping from legacy matplotlib line-style strings to Plotly dash values
MPL_TO_PLOTLY_DASH = {"-": "solid", "--": "dash", "-.": "dashdot", ":": "dot"}

# Fixed tick marker length-to-width ratio. The default tick length is 8px with
# a 1px line width, so a length:width ratio of 8:1. Tick line width is derived
# from the tick length via this ratio so the marker's shape stays identical as
# its size changes (thicker when longer, thinner when shorter).
TICK_LENGTH_TO_WIDTH_RATIO = 8.0


def tick_width_for(tick_length: int | float) -> float:
    """Return the tick line width that preserves the fixed length:width ratio.

    Args:
        tick_length: The tick marker length in px.

    Returns:
        The proportional tick line width in px so the length:width ratio stays
        constant regardless of the configured tick size.
    """
    return tick_length / TICK_LENGTH_TO_WIDTH_RATIO


def _font_dict(fc: FontConfig, **overrides) -> dict:
    """Convert a FontConfig to a Plotly font dict."""
    d = dict(family=fc.family, size=fc.size)
    d.update(overrides)
    return d


# ------------------------------------------------------------------
# Utility helpers
# ------------------------------------------------------------------

def generate_colors(n: int) -> list[str]:
    """Generate n distinct colours using Plotly's qualitative palette.

    Args:
        n: Number of distinct colours to generate.

    Returns:
        List of CSS colour strings from the Dark24 palette.
    """
    import plotly.express as px
    palette = px.colors.qualitative.Dark24
    return [palette[i % len(palette)] for i in range(n)]


def get_line_style(item_path: str, config: PlotConfig) -> tuple[str, float]:
    """Get Plotly dash style and width from config.

    Args:
        item_path: Data series identifier key.
        config: Plot configuration containing per-line style overrides.

    Returns:
        Tuple of (dash style string, line width).
    """
    lc = config.line_configs.get(item_path)
    if lc:
        return MPL_TO_PLOTLY_DASH.get(lc.style, "solid"), lc.width
    return "solid", 2.0


def get_legend_label(item_path: str, config: PlotConfig) -> str:
    """Get display label for a data series.

    Args:
        item_path: Data series identifier key.
        config: Plot configuration containing per-line label overrides.

    Returns:
        Human-readable legend label string.
    """
    if item_path in config.line_configs:
        return config.line_configs[item_path].label
    parts = item_path.split("/", 1)
    if len(parts) == 2:
        entry_id = parts[0]
        path_part = parts[1]
        segments = path_part.split(".")
        if len(segments) >= 2:
            tail = ".".join(segments[-2:])
        else:
            tail = segments[-1]
        if tail == "0" or tail.isdigit():
            tail = ".".join(segments[-3:]) if len(segments) >= 3 else path_part
        short_entry = (entry_id.replace("historyfile_", "")
                       .replace("_coordinator.dill", "[C]")
                       .replace("_subsystem_", "[S:")
                       .replace(".dill", "]"))
        return f"{short_entry}: {tail}"
    return item_path.split(".")[-1]


def _get_plotly_template() -> str:
    """Return 'plotly_white' for the light theme."""
    return "plotly_white"


def _base_layout(config: PlotConfig, canvas_size: tuple[int, int]) -> dict:
    """Return common layout kwargs."""
    from ..styles.Theme import get_chart_colors
    colors = get_chart_colors()
    return dict(
        template=_get_plotly_template(),
        autosize=True,
        paper_bgcolor=colors["fig_face"],
        plot_bgcolor=colors["ax_face"],
        font=dict(
            family=config.title_font.family,
            size=config.title_font.size,
            color=colors["text"],
        ),
        margin=dict(l=60, r=40, t=50, b=60),
        hovermode="x unified",
    )


def _apply_common_axis(fig: go.Figure, config: PlotConfig, *,
                       x_grid_managed: bool = False,
                       skip_yaxis: bool = False) -> None:
    """Apply common axis settings: grid, log scale, labels.

    Args:
        x_grid_managed: If True, skip x-axis grid/tick settings (managed by
                        _add_aligned_ticks).
        skip_yaxis: If True, skip y-axis updates (e.g. multi_axes_plot
                    configures y-axes individually).
    """
    from ..styles.Theme import get_chart_colors
    colors = get_chart_colors()
    x_update = dict(
        title=dict(text=get_x_label(config), font=_font_dict(config.x_label_font)),
        showline=True,
        linecolor=colors["axis_line"],
        mirror=True,
        zeroline=False,
        exponentformat="power",
        showexponent="all",
    )
    if not x_grid_managed:
        x_update["gridcolor"] = colors["grid"]
        x_update["griddash"] = "dash"
        x_update["showgrid"] = config.show_grid
        x_update["ticks"] = "outside"
    if config.x_axis_type == "cumulative_evaluations":
        x_update["exponentformat"] = "power"
    layout_updates = dict(xaxis=x_update)
    if not skip_yaxis:
        y_update = dict(
            title=dict(text=config.custom_y_label or "Value", font=_font_dict(config.y_label_font)),
            gridcolor=colors["grid"],
            griddash="dash",
            showgrid=config.show_grid,
            ticks="outside",
            showline=True,
            linecolor=colors["axis_line"],
            mirror=True,
            zeroline=False,
            hoverformat=".6~r",
            exponentformat="power",
            showexponent="all",
        )
        if config.log_scale:
            y_update["type"] = "log"
            y_update["exponentformat"] = "power"
            y_update["dtick"] = 1  # only powers of 10
            # Minor ticks are 50% of the major length, with width scaled by the
            # same ratio so their length:width shape matches the major ticks.
            y_update["minor"] = dict(ticks="outside", showgrid=config.show_grid,
                                     gridcolor=colors["grid"], griddash="dot",
                                     ticklen=0.5 * config.y_tick_size,
                                     tickwidth=tick_width_for(0.5 * config.y_tick_size))
        layout_updates["yaxis"] = y_update
    fig.update_layout(**layout_updates)


def _nice_step(rough: float) -> float:
    """Round a rough step up to the nearest 1/2/5 x 10^n (Plotly-style).

    Args:
        rough: A positive rough step size.

    Returns:
        The smallest "nice" step >= ``rough`` from the {1, 2, 5} x 10^n family.
    """
    if rough <= 0:
        return 1.0
    base = 10.0 ** math.floor(math.log10(rough))
    frac = rough / base
    if frac <= 1:
        nice = 1.0
    elif frac <= 2:
        nice = 2.0
    elif frac <= 5:
        nice = 5.0
    else:
        nice = 10.0
    return nice * base


def _thin_major_labels(major_labels: list[str], canvas_width: int,
                       tick_font_size: int) -> list[str]:
    """Blank out overlapping outer-iteration labels using Plotly-style spacing.

    Every major tick MARK is preserved (this only affects which labels are
    drawn). The number of visible labels adapts to the available pixel width
    and the tick font size, so wider plots / smaller fonts show more labels.

    Args:
        major_labels: Outer-iteration labels in axis order (numeric strings).
        canvas_width: Current rendered figure width in pixels.
        tick_font_size: X tick label font size in points.

    Returns:
        A list the same length as ``major_labels`` with dropped entries set
        to the empty string.
    """
    n = len(major_labels)
    if n <= 2:
        return list(major_labels)

    # Interpret labels as numeric outer-iteration values; fall back to index
    # positions if any label is non-numeric.
    values: list[float] = []
    try:
        values = [float(lbl) for lbl in major_labels]
    except (TypeError, ValueError):
        values = [float(i) for i in range(n)]

    vmin, vmax = min(values), max(values)
    vrange = vmax - vmin
    if vrange <= 0:
        return list(major_labels)

    # Available horizontal space for the axis (figure width minus L/R margins).
    avail = max(100.0, float(canvas_width) - 100.0)
    # Minimum pixels between labels, scaled by font size (default 12pt) so
    # larger fonts yield fewer labels.
    min_px = 70.0 * max(1.0, float(tick_font_size) / 12.0)
    target_count = max(2, min(n, int(avail / min_px)))

    step = _nice_step(vrange / target_count)
    start = math.ceil(vmin / step) * step

    # Target gridline values (multiples of step spanning the range); snap each
    # to the nearest present major so sparse / non-contiguous outers still show.
    keep: set[int] = {0, n - 1}
    t = start
    while t <= vmax + step * 1e-9:
        best_i = min(range(n), key=lambda i: abs(values[i] - t))
        keep.add(best_i)
        t += step

    return [major_labels[i] if i in keep else "" for i in range(n)]


def _add_aligned_ticks(fig: go.Figure, major_pos: list, major_labels: list[str],
                       minor_pos: list, *, xaxis_key: str = "xaxis",
                       show_grid: bool = False,
                       canvas_width: int = 1000, tick_font_size: int = 12,
                       major_tick_size: int = 8,
                       subplot_domains: list[tuple[float, float]] | None = None) -> None:
    """Apply major and minor tick marks for outer/inner iteration alignment.

    Major ticks (outer iterations): black tick marks with labels.
    Minor ticks (inner iterations): red tick marks, drawn as shapes below the axis.
    Grid lines are drawn as shapes at all positions when show_grid is True.

    Args:
        canvas_width: Current rendered figure width in pixels; drives how many
                      outer-iteration labels can be shown without overlap.
        tick_font_size: X tick label font size; larger fonts need more spacing,
                        so fewer labels are shown.
        major_tick_size: Outer (major) tick marker length in px (config.x_tick_size).
                         The inner (minor) ticks are always drawn at 50% of this,
                         so the two scale together as the user changes tick size.
        subplot_domains: For stacked plots, list of (y_bottom, y_top) paper
                         coordinates for each subplot. Grid and ticks are drawn
                         per-subplot to avoid crossing subplot boundaries.
                         Also applies tick config to all x-axes (xaxis, xaxis2, ...).
    """
    from ..styles.Theme import get_chart_colors
    chart_colors = get_chart_colors()

    all_pos = sorted(set(major_pos) | set(minor_pos))
    major_set = set(major_pos)

    # Keep every major tick MARK (tickvals) but thin the visible LABELS so
    # they never overlap at the current width / font size (Plotly-style
    # "nice number" spacing).
    ticktext = _thin_major_labels(major_labels, canvas_width, tick_font_size)

    # Stash the full (unthinned) major data on the figure so the browser can
    # re-thin labels live when the user zooms/pans into a sub-range.
    try:
        _vals = [float(lbl) for lbl in major_labels]
    except (TypeError, ValueError):
        _vals = [float(i) for i in range(len(major_labels))]
    try:
        object.__setattr__(fig, "_ddo_align", dict(
            tickvals=[float(v) for v in major_pos],
            labels=[str(lbl) for lbl in major_labels],
            values=_vals,
            min_px=70.0,
            font_size=float(tick_font_size),
        ))
    except Exception:  # pragma: no cover - defensive; zoom-thinning is optional
        pass

    minor_only = [pos for pos in minor_pos if pos not in major_set]
    minor_tick_color = chart_colors["minor_tick"]

    tick_config = dict(
        tickmode="array",
        tickvals=major_pos,
        ticktext=ticktext,
        tickfont=dict(size=9),
        ticks="outside",
        ticklen=major_tick_size,
        # Width scales with length so the tick shape (length:width ratio) is
        # preserved as the user changes the tick size.
        tickwidth=tick_width_for(major_tick_size),
        tickcolor=chart_colors["axis_line"],
        showgrid=False,  # we draw grid manually as shapes
        # Inner (red) ticks are rendered as native axis minor ticks whose
        # ticklen is in px — exactly like the major (outer) ticks — so they are
        # always 50% of the outer tick length regardless of the rendered figure
        # size. major_tick_size is config.x_tick_size (the GUI tick-size value).
        # The width is scaled by the same ratio so minors keep the same shape.
        minor=dict(
            tickmode="array",
            tickvals=minor_only,
            ticks="outside",
            ticklen=0.5 * major_tick_size,
            tickwidth=tick_width_for(0.5 * major_tick_size),
            tickcolor=minor_tick_color,
            showgrid=False,
        ),
    )

    if subplot_domains is not None:
        # Apply tick config to ALL x-axes in stacked subplots
        n = len(subplot_domains)
        for i in range(n):
            key = "xaxis" if i == 0 else f"xaxis{i + 1}"
            fig.update_layout(**{key: tick_config})
    else:
        fig.update_layout(**{xaxis_key: tick_config})

    ax_ref = xaxis_key.replace("axis", "")  # "xaxis" -> "x"

    if subplot_domains is None:
        # Single plot: ticks below axis at y=0, grid from 0 to 1
        domains = [(0.0, 1.0)]
    else:
        domains = subplot_domains

    # Accumulate shapes in a plain list and assign once. Each fig.add_shape()
    # appends to the layout.shapes tuple (O(n) copy per call -> O(n^2) overall),
    # which dominates runtime for large tick counts; a single batched assignment
    # produces identical shapes in O(n).
    new_shapes: list[dict] = []

    # Draw grid lines within each subplot domain when grid is enabled
    if show_grid:
        grid_color = chart_colors["grid"]
        for y_bot, y_top in domains:
            for pos in all_pos:
                new_shapes.append(dict(
                    type="line",
                    x0=pos, x1=pos,
                    y0=y_bot, y1=y_top,
                    yref="paper",
                    xref=ax_ref,
                    line=dict(color=grid_color, width=0.5, dash="dash"),
                    layer="below",
                ))

    if new_shapes:
        existing = list(fig.layout.shapes) if fig.layout.shapes else []
        fig.update_layout(shapes=existing + new_shapes)


# ------------------------------------------------------------------
# Public plot builders — each returns a go.Figure
# ------------------------------------------------------------------

def shared_axes_plot(plottable_data: list[tuple[str, list[float]]], config: PlotConfig,
                     canvas_size: tuple[int, int], labels_map: dict[str, list[dict]]) -> go.Figure:
    """Single shared Y-axis for all data series.

    Args:
        plottable_data: List of (item_path, y_values) tuples to plot.
        config: Plot configuration controlling axes, styles, and layout.
        canvas_size: Width and height in pixels for the figure.
        labels_map: Mapping of item paths to per-point label metadata.

    Returns:
        Configured Plotly Figure with all series on a shared Y-axis.
    """
    fig = go.Figure()
    colors = generate_colors(len(plottable_data))

    if config.x_axis_type in ("combined_ticks", "equispaced_major"):
        ad = build_aligned_data(plottable_data, config, labels_map)
        for idx, (item_path, _) in enumerate(plottable_data):
            label = get_legend_label(item_path, config)
            dash, width = get_line_style(item_path, config)
            lc = config.line_configs.get(item_path)
            color = lc.color if lc and lc.color else colors[idx]
            fig.add_trace(go.Scatter(
                x=ad.x_positions, y=ad.aligned_y[idx], name=label,
                mode="lines+markers", marker=dict(size=4, color=color),
                line=dict(color=color, dash=dash, width=width),
                text=ad.hover_labels,
                hovertemplate="%{text}<br>y: %{y}<extra>%{fullData.name}</extra>",
            ))
        _add_aligned_ticks(fig, ad.major_positions, ad.major_labels, ad.minor_positions,
                           show_grid=config.show_grid,
                           canvas_width=canvas_size[0],
                           tick_font_size=config.x_tick_label_font.size,
                           major_tick_size=config.x_tick_size)
    elif config.x_axis_type in ("cumulative_runtime", "cumulative_evaluations"):
        for idx, (item_path, values) in enumerate(plottable_data):
            series_labels = get_series_labels(item_path, labels_map)
            x_vals = generate_x_values(values, config, series_labels)
            label = get_legend_label(item_path, config)
            dash, width = get_line_style(item_path, config)
            lc = config.line_configs.get(item_path)
            color = lc.color if lc and lc.color else colors[idx]
            fig.add_trace(go.Scatter(
                x=x_vals, y=values, name=label,
                mode="lines+markers", marker=dict(size=4, color=color),
                line=dict(color=color, dash=dash, width=width),
            ))
    else:
        for idx, (item_path, values) in enumerate(plottable_data):
            series_labels = get_series_labels(item_path, labels_map)
            x_vals = generate_x_values(values, config, series_labels)
            label = get_legend_label(item_path, config)
            dash, width = get_line_style(item_path, config)
            lc = config.line_configs.get(item_path)
            color = lc.color if lc and lc.color else colors[idx]
            fig.add_trace(go.Scatter(
                x=x_vals, y=values, name=label,
                mode="lines+markers", marker=dict(size=4, color=color),
                line=dict(color=color, dash=dash, width=width),
            ))

    fig.update_layout(**_base_layout(config, canvas_size))
    uses_aligned = config.x_axis_type in ("combined_ticks", "equispaced_major")
    _apply_common_axis(fig, config, x_grid_managed=uses_aligned)

    return fig


def multi_axes_plot(plottable_data: list[tuple[str, list[float]]], config: PlotConfig,
                    canvas_size: tuple[int, int], labels_map: dict[str, list[dict]],
                    *, centered: bool = False) -> go.Figure:
    """Multiple independent or centered Y-axes (overlaid).

    Args:
        plottable_data: List of (item_path, y_values) tuples to plot.
        config: Plot configuration controlling axes, styles, and layout.
        canvas_size: Width and height in pixels for the figure.
        labels_map: Mapping of item paths to per-point label metadata.

    Returns:
        Configured Plotly Figure with independent Y-axes per series.
    """
    n = len(plottable_data)
    fig = go.Figure()
    colors = generate_colors(n)

    ad: AlignedAxisData | None = None
    if config.x_axis_type in ("combined_ticks", "equispaced_major"):
        ad = build_aligned_data(plottable_data, config, labels_map)

    for idx, (item_path, values) in enumerate(plottable_data):
        label = get_legend_label(item_path, config)
        dash, width = get_line_style(item_path, config)
        lc = config.line_configs.get(item_path)
        color = lc.color if lc and lc.color else colors[idx]
        yaxis_name = "y" if idx == 0 else f"y{idx + 1}"

        if ad is not None:
            x_vals = ad.x_positions
            y_vals = ad.aligned_y[idx]
        else:
            series_labels = get_series_labels(item_path, labels_map)
            x_vals = generate_x_values(values, config, series_labels)
            y_vals = values

        hover_kwargs = {}
        if ad is not None:
            hover_kwargs["text"] = ad.hover_labels
            hover_kwargs["hovertemplate"] = "%{text}<br>y: %{y}<extra>%{fullData.name}</extra>"

        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals, name=label,
            mode="lines+markers", marker=dict(size=4, color=color),
            line=dict(color=color, dash=dash, width=width),
            yaxis=yaxis_name, **hover_kwargs,
        ))

    # Configure Y-axes
    layout_kwargs = _base_layout(config, canvas_size)
    from ..styles.Theme import get_chart_colors
    chart_colors = get_chart_colors()

    y_type = "log" if config.log_scale else None

    for idx, (item_path, _) in enumerate(plottable_data):
        label = get_legend_label(item_path, config)
        # Use custom per-axis y-label if provided
        if config.independent_y_labels and idx < len(config.independent_y_labels) and config.independent_y_labels[idx]:
            label = config.independent_y_labels[idx]
        color = colors[idx]
        lc = config.line_configs.get(item_path)
        if lc and lc.color:
            color = lc.color
        axis_key = "yaxis" if idx == 0 else f"yaxis{idx + 1}"
        axis_def = dict(
            title=dict(text=label, font=dict(color=color)),
            tickfont=dict(color=color),
            gridcolor=chart_colors["grid"],
            griddash="dash",
            showgrid=(idx == 0 and config.show_grid),
            showline=True,
            linecolor=chart_colors["axis_line"],
            mirror=True,
            zeroline=False,
            ticks="outside",
            hoverformat=".6~r",
            exponentformat="power",
            showexponent="all",
        )
        if y_type:
            axis_def["type"] = y_type
            axis_def["exponentformat"] = "power"
            axis_def["showexponent"] = "all"
            axis_def["dtick"] = 1
            # Minor ticks: 50% of the major length, same length:width ratio.
            minor_len = 0.5 * config.y_tick_size
            if idx == 0:
                axis_def["minor"] = dict(ticks="outside", showgrid=config.show_grid,
                                         gridcolor=chart_colors["grid"], griddash="dot",
                                         ticklen=minor_len, tickwidth=tick_width_for(minor_len))
            else:
                axis_def["minor"] = dict(ticks="outside", showgrid=False,
                                         ticklen=minor_len, tickwidth=tick_width_for(minor_len))
        # Apply centering: symmetric y-range around zero
        if centered and not config.log_scale:
            if ad is not None:
                y_data = [v for v in ad.aligned_y[idx] if v is not None and not (isinstance(v, float) and v != v)]
            else:
                y_data = [v for v in plottable_data[idx][1] if v is not None and not (isinstance(v, float) and v != v)]
            if y_data:
                data_min, data_max = min(y_data), max(y_data)
                padding = (data_max - data_min) * 0.05 if data_max != data_min else 1.0
                ymin, ymax = data_min - padding, data_max + padding
                if ymin > 0:
                    ymin = 0
                elif ymax < 0:
                    ymax = 0
                max_abs = max(abs(ymin), abs(ymax))
                axis_def["range"] = [-max_abs, max_abs]
            else:
                axis_def["range"] = [-1, 1]
        if idx > 0:
            axis_def["overlaying"] = "y"
            axis_def["side"] = "right"
            axis_def["mirror"] = False
            axis_def["showticklabels"] = True
            axis_def["showexponent"] = "all"
            if idx > 1:
                axis_def["anchor"] = "free"
                axis_def["position"] = 1.0 - 0.05 * (idx - 1)
        layout_kwargs[axis_key] = axis_def

    if n > 1:
        layout_kwargs["margin"]["r"] = max(60, 40 + 50 * (n - 1))

    fig.update_layout(**layout_kwargs)

    uses_aligned = ad is not None
    _apply_common_axis(fig, config, x_grid_managed=uses_aligned, skip_yaxis=True)

    if ad is not None:
        _add_aligned_ticks(fig, ad.major_positions, ad.major_labels, ad.minor_positions,
                           show_grid=config.show_grid,
                           canvas_width=canvas_size[0],
                           tick_font_size=config.x_tick_label_font.size,
                           major_tick_size=config.x_tick_size)

    return fig


def stacked_plot(plottable_data: list[tuple[str, list[float]]], config: PlotConfig,
                 canvas_size: tuple[int, int], labels_map: dict[str, list[dict]]) -> go.Figure:
    """Stacked subplots (one per data series).

    Args:
        plottable_data: List of (item_path, y_values) tuples to plot.
        config: Plot configuration controlling axes, styles, and layout.
        canvas_size: Width and height in pixels for the figure.
        labels_map: Mapping of item paths to per-point label metadata.

    Returns:
        Configured Plotly Figure with vertically stacked subplots.
    """
    n = len(plottable_data)
    # Use custom stacked titles if provided, otherwise default to legend labels
    subplot_titles = []
    for idx, (p, _) in enumerate(plottable_data):
        default_label = get_legend_label(p, config)
        if config.stacked_titles and idx < len(config.stacked_titles) and config.stacked_titles[idx]:
            subplot_titles.append(config.stacked_titles[idx])
        else:
            subplot_titles.append(default_label)
    fig = make_subplots(rows=n, cols=1, shared_xaxes=True, subplot_titles=subplot_titles,
                        vertical_spacing=max(0.02, 0.08 / n))
    colors = generate_colors(n)
    from ..styles.Theme import get_chart_colors
    chart_colors = get_chart_colors()

    ad: AlignedAxisData | None = None
    if config.x_axis_type in ("combined_ticks", "equispaced_major"):
        ad = build_aligned_data(plottable_data, config, labels_map)

    for idx, (item_path, values) in enumerate(plottable_data):
        label = get_legend_label(item_path, config)
        dash, width = get_line_style(item_path, config)
        lc = config.line_configs.get(item_path)
        color = lc.color if lc and lc.color else colors[idx]
        row = idx + 1

        if ad is not None:
            x_vals = ad.x_positions
            y_vals = ad.aligned_y[idx]
        else:
            series_labels = get_series_labels(item_path, labels_map)
            x_vals = generate_x_values(values, config, series_labels)
            y_vals = values

        hover_kwargs = {}
        if ad is not None:
            hover_kwargs["text"] = ad.hover_labels
            hover_kwargs["hovertemplate"] = "%{text}<br>y: %{y}<extra>%{fullData.name}</extra>"

        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals, name=label,
            mode="lines+markers", marker=dict(size=4, color=color),
            line=dict(color=color, dash=dash, width=width), **hover_kwargs,
            showlegend=config.show_legend,
        ), row=row, col=1)

        if config.log_scale:
            fig.update_yaxes(type="log", exponentformat="power", dtick=1,
                             minor=dict(ticks="outside", showgrid=config.show_grid,
                                        gridcolor=chart_colors["minor_grid"], griddash="dot",
                                        ticklen=0.5 * config.y_tick_size,
                                        tickwidth=tick_width_for(0.5 * config.y_tick_size)),
                             row=row, col=1)
        fig.update_yaxes(showgrid=config.show_grid, griddash="dash",
                         showline=True, linecolor=chart_colors["axis_line"], mirror=True,
                         zeroline=False, ticks="outside",
                         exponentformat="power", showexponent="all", row=row, col=1)
        uses_aligned = config.x_axis_type in ("combined_ticks", "equispaced_major")
        x_grid = False if uses_aligned else config.show_grid
        fig.update_xaxes(showline=True, linecolor=chart_colors["axis_line"], mirror=True,
                         zeroline=False, ticks="outside",
                         showgrid=x_grid, gridcolor=chart_colors["minor_grid"], griddash="dash",
                         exponentformat="power", showexponent="all",
                         row=row, col=1)

        # Apply custom per-subplot y-label
        if config.stacked_y_labels and idx < len(config.stacked_y_labels) and config.stacked_y_labels[idx]:
            fig.update_yaxes(title_text=config.stacked_y_labels[idx], row=row, col=1)
        elif config.custom_y_label:
            fig.update_yaxes(title_text=config.custom_y_label, row=row, col=1)

    w, h = canvas_size
    stacked_h = max(400, 250 * n)
    layout_kwargs = _base_layout(config, (w, stacked_h))
    layout_kwargs["height"] = stacked_h
    fig.update_layout(**layout_kwargs)

    fig.update_xaxes(title_text=get_x_label(config), row=n, col=1)

    if ad is not None:
        # Extract per-subplot y-domains from the figure layout
        subplot_domains = []
        for row_idx in range(n):
            yaxis_key = "yaxis" if row_idx == 0 else f"yaxis{row_idx + 1}"
            domain = fig.layout[yaxis_key].domain
            if domain:
                subplot_domains.append((domain[0], domain[1]))
            else:
                subplot_domains.append((0.0, 1.0))
        _add_aligned_ticks(fig, ad.major_positions, ad.major_labels, ad.minor_positions,
                           show_grid=config.show_grid,
                           canvas_width=canvas_size[0],
                           tick_font_size=config.x_tick_label_font.size,
                           major_tick_size=config.x_tick_size,
                           subplot_domains=subplot_domains)

    return fig
