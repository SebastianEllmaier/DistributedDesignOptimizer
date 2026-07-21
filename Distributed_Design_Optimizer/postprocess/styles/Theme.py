# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Light theme for DDO Viewer — colors based on the DDO documentation palette.

Primary:   #035970
Secondary: #047a99
"""

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor

# DDO brand colors (from docs_src/content/stylesheets/custom.css)
PRIMARY = "#035970"
PRIMARY_LIGHT = "#047a99"
PRIMARY_DARK = "#024556"
SECONDARY = "#0596bd"
PRIMARY_LIGHTEST = "#e6f4f7"

# Derive RGB components for use in rgba() within QSS f-strings
_pc = QColor(PRIMARY)
_PRIMARY_RGB = f"{_pc.red()}, {_pc.green()}, {_pc.blue()}"


def get_accent_color() -> str:
    """Return the primary accent colour hex string.

    Returns:
        The primary brand color as a CSS hex string.
    """
    return PRIMARY


_LIGHT_QSS = f"""
QToolTip {{
    background-color: #f8f8f8;
    color: #333333;
    border: 1px solid #cccccc;
    padding: 4px;
    font-size: 9pt;
}}
QGroupBox {{
    font-weight: bold;
    font-size: 9pt;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    margin-top: 10px;
    padding-top: 14px;
    background: rgba(0, 0, 0, 0.02);
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: {PRIMARY};
}}
QTabWidget::pane {{
    border: 1px solid #e0e0e0;
    border-radius: 2px;
}}
QTabBar::tab {{
    padding: 6px 14px;
    margin-right: 2px;
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
}}
QTabBar::tab:selected {{
    border-bottom: 2px solid {PRIMARY};
}}
QPushButton {{
    padding: 5px 12px;
    border-radius: 3px;
}}
QStatusBar {{
    border-top: 1px solid #e0e0e0;
    font-size: 9pt;
}}
QSplitter::handle {{
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 transparent, stop:0.35 rgba(0,0,0,0.08),
        stop:0.5 rgba(0,0,0,0.18),
        stop:0.65 rgba(0,0,0,0.08), stop:1 transparent
    );
    min-width: 6px;
    min-height: 6px;
}}
QSplitter::handle:horizontal {{
    image: url(none);
    min-width: 6px;
    border-left: 1px solid rgba(0,0,0,0.10);
    border-right: 1px solid rgba(0,0,0,0.10);
}}
QSplitter::handle:vertical {{
    image: url(none);
    min-height: 6px;
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 transparent, stop:0.35 rgba(0,0,0,0.08),
        stop:0.5 rgba(0,0,0,0.18),
        stop:0.65 rgba(0,0,0,0.08), stop:1 transparent
    );
    border-top: 1px solid rgba(0,0,0,0.10);
    border-bottom: 1px solid rgba(0,0,0,0.10);
}}
QSplitter::handle:hover {{
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 transparent, stop:0.35 rgba({_PRIMARY_RGB}, 0.15),
        stop:0.5 rgba({_PRIMARY_RGB}, 0.35),
        stop:0.65 rgba({_PRIMARY_RGB}, 0.15), stop:1 transparent
    );
}}
QSplitter::handle:vertical:hover {{
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 transparent, stop:0.35 rgba({_PRIMARY_RGB}, 0.15),
        stop:0.5 rgba({_PRIMARY_RGB}, 0.35),
        stop:0.65 rgba({_PRIMARY_RGB}, 0.15), stop:1 transparent
    );
}}
QMainWindow::separator {{
    width: 6px;
    height: 6px;
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 transparent, stop:0.35 rgba(0,0,0,0.06),
        stop:0.5 rgba(0,0,0,0.14),
        stop:0.65 rgba(0,0,0,0.06), stop:1 transparent
    );
    border-left: 1px solid rgba(0,0,0,0.08);
    border-right: 1px solid rgba(0,0,0,0.08);
}}
QMainWindow::separator:hover {{
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 transparent, stop:0.35 rgba({_PRIMARY_RGB}, 0.15),
        stop:0.5 rgba({_PRIMARY_RGB}, 0.35),
        stop:0.65 rgba({_PRIMARY_RGB}, 0.15), stop:1 transparent
    );
}}
"""


def apply_light_theme(app: QApplication) -> None:
    """Apply the DDO-branded light theme using Fusion + standard palette.

    Args:
        app: The Qt application instance to theme.
    """
    app.setStyle("Fusion")
    palette = app.style().standardPalette()
    # Brand the highlight with primary color
    palette.setColor(QPalette.ColorRole.Highlight, QColor(PRIMARY))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Link, QColor(PRIMARY))
    app.setPalette(palette)
    app.setStyleSheet(_LIGHT_QSS)


def get_chart_colors() -> dict[str, str]:
    """Return chart-compatible color strings for the light theme.

    Keys: fig_face, ax_face, text, tick, grid, legend_face, legend_edge,
          legend_text, axis_line, minor_tick, minor_grid
    Used by Plotly plot builders and the GraphWidget.

    Returns:
        A dict mapping color role names to CSS hex color strings.
    """
    return {
        "fig_face": "#ffffff",
        "ax_face": "#ffffff",
        "text": "#333333",
        "tick": "#333333",
        "grid": "#cccccc",
        "minor_grid": "#dddddd",
        "legend_face": "#ffffff",
        "legend_edge": "#cccccc",
        "legend_text": "#333333",
        "axis_line": "black",
        "minor_tick": "red",
    }
