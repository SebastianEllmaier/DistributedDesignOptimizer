---
title: PlotHandler (Source)
---

← Back to [PlotHandler documentation](PlotHandler.md)

# PlotHandler - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\handlers\PlotHandler.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Plotting engine — orchestrates figure creation and customization.

Delegates actual plot building to _plot_builder and customization to _plot_customizer.
Stores last plot state so theme toggles and auto-updates can regenerate the current figure.
Emits interactive Plotly HTML via the plot_ready signal.
"""

import logging

import plotly.graph_objects as go

from PySide6.QtCore import QObject, Signal

from ..models.PlotConfig import PlotConfig
from . import _plot_builder as builder
from . import _plot_customizer as customizer

logger = logging.getLogger(__name__)

# Client-side script injected for aligned x-axis modes. It re-thins the outer
# iteration labels live whenever the user zooms/pans into a sub-range, using the
# same "nice number" spacing as the server so the visible detail adapts to what
# is currently shown. ``{plot_id}`` is substituted by Plotly; ``__DDO_ALIGN_DATA__``
# is substituted (as JSON) by us before rendering.
_ALIGN_ZOOM_JS = r"""
(function() {
  var gd = document.getElementById('{plot_id}');
  if (!gd || typeof Plotly === 'undefined') return;
  var DATA = __DDO_ALIGN_DATA__;
  var VALS = DATA.tickvals, LABELS = DATA.labels, VALUES = DATA.values;
  var MIN_PX = DATA.min_px, FONT = DATA.font_size;

  function niceStep(rough) {
    if (rough <= 0) return 1.0;
    var base = Math.pow(10, Math.floor(Math.log10(rough)));
    var frac = rough / base;
    var nice = frac <= 1 ? 1 : frac <= 2 ? 2 : frac <= 5 ? 5 : 10;
    return nice * base;
  }

  function thinForAxis(ax) {
    var out = VALS.map(function() { return ''; });
    if (!ax || !ax.range) return out;
    var lo = Math.min(ax.range[0], ax.range[1]);
    var hi = Math.max(ax.range[0], ax.range[1]);
    var vis = [];
    for (var i = 0; i < VALS.length; i++) {
      if (VALS[i] >= lo && VALS[i] <= hi) vis.push(i);
    }
    var n = vis.length;
    if (n === 0) return out;
    var size = gd._fullLayout && gd._fullLayout._size;
    var availPx = size ? size.w : Math.max(100, gd.clientWidth - 100);
    var minPx = MIN_PX * Math.max(1, FONT / 12);
    var visVals = vis.map(function(i) { return VALUES[i]; });
    var vmin = Math.min.apply(null, visVals);
    var vmax = Math.max.apply(null, visVals);
    var vrange = vmax - vmin;
    if (n <= 2 || vrange <= 0) {
      vis.forEach(function(i) { out[i] = LABELS[i]; });
      return out;
    }
    var targetCount = Math.max(2, Math.min(n, Math.floor(availPx / minPx)));
    var step = niceStep(vrange / targetCount);
    var keep = {};
    keep[vis[0]] = 1;
    keep[vis[n - 1]] = 1;
    var start = Math.ceil(vmin / step) * step;
    for (var t = start; t <= vmax + step * 1e-9; t += step) {
      var best = vis[0], bd = Infinity;
      for (var k = 0; k < n; k++) {
        var d = Math.abs(VALUES[vis[k]] - t);
        if (d < bd) { bd = d; best = vis[k]; }
      }
      keep[best] = 1;
    }
    for (var idx in keep) { out[idx] = LABELS[idx]; }
    return out;
  }

  function applyAll() {
    var fl = gd._fullLayout;
    if (!fl) return;
    var upd = {};
    Object.keys(fl).forEach(function(k) {
      if (/^xaxis\d*$/.test(k) && fl[k] && fl[k].range) {
        upd[k + '.ticktext'] = thinForAxis(fl[k]);
        upd[k + '.tickvals'] = VALS;
      }
    });
    if (Object.keys(upd).length) Plotly.relayout(gd, upd);
  }

  var timer = null;
  function schedule() {
    if (timer) clearTimeout(timer);
    timer = setTimeout(applyAll, 60);
  }

  gd.on('plotly_relayout', function(ev) {
    for (var key in ev) {
      if (/^xaxis\d*\.(range|autorange)/.test(key)) { schedule(); return; }
    }
  });

  // Correct the initial labels to the true rendered width.
  schedule();
})();
"""



class PlotHandler(QObject):
    """Plotting engine — creates Plotly figures and emits HTML strings."""

    plot_ready = Signal(str)       # HTML string
    plot_error = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        """Initialize the plot handler with default empty state.

        Args:
            parent: Optional parent QObject for Qt ownership.
        """
        super().__init__(parent)
        self._last_plottable_data: list[tuple[str, list[float]]] = []
        self._last_labels_map: dict[str, list[dict]] = {}
        self._last_customization: PlotConfig | None = None
        self._canvas_size: tuple[int, int] = (1000, 600)
        self._last_fig: go.Figure | None = None

    @property
    def last_plottable_data(self) -> list[tuple[str, list[float]]]:
        """Return the most recently plotted data series.

        Returns:
            List of (series_name, values) tuples from the last plot.
        """
        return self._last_plottable_data

    @property
    def last_labels_map(self) -> dict[str, list[dict]]:
        """Return the most recently used labels map.

        Returns:
            Mapping of series names to their label metadata dicts.
        """
        return self._last_labels_map

    @property
    def last_figure(self) -> go.Figure | None:
        """The most recent Plotly figure (for export).

        Returns:
            The last created Plotly figure, or None if no plot has been created.
        """
        return self._last_fig

    def clear(self) -> None:
        """Reset all stored plot state."""
        self._last_plottable_data = []
        self._last_labels_map = {}
        self._last_customization = None
        self._last_fig = None

    def set_canvas_size(self, width: int, height: int) -> None:
        """Set the canvas size used for figure creation.

        Args:
            width: Canvas width in pixels.
            height: Canvas height in pixels.
        """
        self._canvas_size = (width, height)

    def create_plot(self, plottable_data: list[tuple[str, list[float]]], config: PlotConfig,
                    labels_map: dict[str, list[dict]] | None = None) -> None:
        """Create a plot and emit plot_ready with the resulting HTML.

        Args:
            plottable_data: List of (series_name, values) tuples to plot.
            config: Plot configuration controlling type, style, and layout.
            labels_map: Optional mapping of series names to label metadata.
        """
        if not plottable_data:
            self.plot_error.emit("No data to plot.")
            return

        self._last_plottable_data = plottable_data
        self._last_labels_map = labels_map or {}
        try:
            fig = self._dispatch_plot(plottable_data, config)
            # Apply all customizations (fonts, labels, ref lines, per-line styles)
            customizer.apply_all(fig, config)
            self._last_fig = fig
            # For aligned x-axis modes, inject a client-side script so labels
            # re-thin live when the user zooms/pans into a sub-range.
            post_script = None
            align = getattr(fig, "_ddo_align", None)
            if align:
                import json
                post_script = _ALIGN_ZOOM_JS.replace(
                    "__DDO_ALIGN_DATA__", json.dumps(align),
                )
            # Inline plotly.js (no CDN) so charts render without an internet connection.
            raw_html = fig.to_html(include_plotlyjs=True, full_html=True,
                                   post_script=post_script,
                                   config={"responsive": True, "displaylogo": False,
                                           "displayModeBar": True,
                                           "toImageButtonOptions": {
                                               "format": "svg",
                                               "filename": "ddo_plot",
                                               "width": 1200,
                                               "height": 700,
                                               "scale": 1,
                                           }})
            # Inject CSS to make the plot fill the QWebEngineView (no scrollbars)
            responsive_css = (
                "<style>html,body{margin:0;padding:0;width:100%;height:100%;overflow:hidden;}"
                ".plotly-graph-div{width:100%!important;height:100%!important;}</style>"
            )
            html = raw_html.replace("</head>", responsive_css + "</head>", 1)
            self.plot_ready.emit(html)
        except Exception as e:
            logger.error(f"Plot creation failed: {e}", exc_info=True)
            self.plot_error.emit(str(e))

    def clear_customization(self) -> None:
        """Clear stored customization so it won't be re-applied on next plot."""
        self._last_customization = None

    def apply_customization(self, fig: go.Figure, config: PlotConfig) -> None:
        """Apply font, labels, reference lines, per-line styles to an existing Figure.

        Args:
            fig: The Plotly figure to customize.
            config: Plot configuration with customization settings.
        """
        if fig is None:
            return
        self._last_customization = config
        try:
            customizer.apply_all(fig, config)
        except Exception as e:
            logger.error(f"Customization failed: {e}", exc_info=True)

    # ------------------------------------------------------------------
    # Plot type dispatch
    # ------------------------------------------------------------------

    def _dispatch_plot(self, plottable_data: list[tuple[str, list[float]]], config: PlotConfig) -> go.Figure:
        from dataclasses import replace as _replace
        # Fall back to shared if fewer than 2 series for multi-axis modes
        if config.plot_type in ("independent", "centered", "stacked") and len(plottable_data) < 2:
            config = _replace(config, plot_type="shared")

        cs = self._canvas_size
        lm = self._last_labels_map
        pt = config.plot_type
        if pt == "independent":
            return builder.multi_axes_plot(plottable_data, config, cs, lm, centered=False)
        if pt == "centered":
            return builder.multi_axes_plot(plottable_data, config, cs, lm, centered=True)
        if pt == "stacked":
            return builder.stacked_plot(plottable_data, config, cs, lm)
        return builder.shared_axes_plot(plottable_data, config, cs, lm)

```
