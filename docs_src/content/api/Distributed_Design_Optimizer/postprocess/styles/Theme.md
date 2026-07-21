---
title: Theme
---

← Back to [styles](index.md)

# Theme

**Source:** [Distributed_Design_Optimizer\postprocess\styles\Theme.py](Theme_source.md)

Light theme for DDO Viewer — colors based on the DDO documentation palette.

Primary:   #035970
Secondary: #047a99

## Functions

??? abstract "get_accent_color() → str"
    Return the primary accent colour hex string.


    **Returns:**
    > The primary brand color as a CSS hex string.  

??? abstract "apply_light_theme(app: QApplication) → None"
    Apply the DDO-branded light theme using Fusion + standard palette.


    **Args:**
    > app: The Qt application instance to theme.  

??? abstract "get_chart_colors() → dict[str, str]"
    Return chart-compatible color strings for the light theme.

    Keys: fig_face, ax_face, text, tick, grid, legend_face, legend_edge,
    legend_text, axis_line, minor_tick, minor_grid
    Used by Plotly plot builders and the GraphWidget.


    **Returns:**
    > A dict mapping color role names to CSS hex color strings.  

