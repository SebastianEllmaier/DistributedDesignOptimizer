# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""
Reusable widget for embedding interactive Plotly charts via QWebEngineView.

Provides the common set_html / clear / export pattern used by both
PlotCanvas and TopologyPanel's chart page.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QFileDialog
from PySide6.QtCore import Qt, QUrl, QObject, Signal, Slot, QTimer
import base64
import logging
import os
import tempfile
import uuid
from urllib.parse import unquote

logger = logging.getLogger(__name__)

# JavaScript snippet injected into every Plotly HTML to replace the default
# camera button with a single "Save As…" dropdown offering SVG/PNG/JPEG/WebP.
# Uses Plotly.toImage() → base64 → sends to Qt via QWebChannel for a native
# file-save dialog.
_EXTRA_DOWNLOAD_JS = """<script src="qrc:///qtwebchannel/qwebchannel.js"></script>
<script>
(function addExportDropdown() {
    var gd = document.querySelector('.plotly-graph-div');
    if (!gd || !window.Plotly) { setTimeout(addExportDropdown, 100); return; }

    var opts = {width: 1200, height: 700, scale: 2};
    var formats = [
        {fmt: 'svg',  label: 'SVG (vector)',  ext: '.svg'},
        {fmt: 'png',  label: 'PNG',           ext: '.png'},
        {fmt: 'jpeg', label: 'JPEG',          ext: '.jpg'},
        {fmt: 'webp', label: 'WebP',          ext: '.webp'},
    ];

    /* Remove the default camera / download button */
    var btns = gd.querySelectorAll('.modebar-btn');
    btns.forEach(function(b) {
        var t = (b.getAttribute('data-title') || '').toLowerCase();
        if (t.indexOf('download') !== -1 || t.indexOf('png') !== -1) {
            b.remove();
        }
    });

    var bar = gd.querySelector('.modebar-group:last-child');
    if (!bar) return;

    var wrap = document.createElement('div');
    wrap.style.cssText = 'position:relative;display:inline-flex;align-items:center;';

    var btn = document.createElement('a');
    btn.className = 'modebar-btn';
    btn.setAttribute('data-title', 'Save image as\u2026');
    btn.innerHTML = '<svg viewBox="0 0 24 24" width="1.3em" height="1.3em" stroke="currentColor" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        + '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
        + '<polyline points="7 10 12 15 17 10"/>'
        + '<line x1="12" y1="15" x2="12" y2="3"/>'
        + '</svg>'
        + '<span style="font-size:10px;margin-left:1px;">\u25BE</span>';
    btn.style.cssText = 'cursor:pointer;display:flex;align-items:center;';

    var menu = document.createElement('div');
    menu.style.cssText = 'display:none;position:absolute;top:100%;right:0;'
        + 'background:#fff;border:1px solid #ccc;border-radius:4px;'
        + 'box-shadow:0 2px 8px rgba(0,0,0,.18);z-index:9999;min-width:130px;padding:4px 0;';

    formats.forEach(function(f) {
        var item = document.createElement('div');
        item.textContent = f.label;
        item.style.cssText = 'padding:5px 14px;cursor:pointer;font-size:13px;white-space:nowrap;color:#333;';
        item.addEventListener('mouseenter', function() { item.style.background = '#e6f4f7'; });
        item.addEventListener('mouseleave', function() { item.style.background = 'none'; });
        item.addEventListener('click', function(e) {
            e.stopPropagation();
            menu.style.display = 'none';
            Plotly.toImage(gd, Object.assign({}, opts, {format: f.fmt})).then(function(dataUrl) {
                if (window._qtBridge) {
                    window._qtBridge.saveImage(f.fmt, f.ext, dataUrl);
                }
            });
        });
        menu.appendChild(item);
    });

    btn.addEventListener('click', function(e) {
        e.stopPropagation();
        menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
    });

    document.addEventListener('click', function() { menu.style.display = 'none'; });

    wrap.appendChild(btn);
    wrap.appendChild(menu);
    bar.appendChild(wrap);

    /* Set up QWebChannel bridge */
    if (typeof QWebChannel !== 'undefined') {
        new QWebChannel(qt.webChannelTransport, function(channel) {
            window._qtBridge = channel.objects.bridge;
        });
    }
})();
</script>"""

# Lazy import — avoids pulling in WebEngine until actually needed
_QWebEngineView = None


def _get_web_engine_class():
    global _QWebEngineView
    if _QWebEngineView is None:
        from PySide6.QtWebEngineWidgets import QWebEngineView
        _QWebEngineView = QWebEngineView
    return _QWebEngineView


class _ImageSaveBridge(QObject):
    """QWebChannel bridge for saving Plotly chart images via native file dialog."""

    image_saved = Signal(str)  # emitted with status message after successful save

    _FILTER_MAP = {
        'svg':  'SVG Files (*.svg)',
        'png':  'PNG Files (*.png)',
        'jpeg': 'JPEG Files (*.jpg *.jpeg)',
        'webp': 'WebP Files (*.webp)',
    }

    @Slot(str, str, str)
    def saveImage(self, fmt: str, ext: str, data_url: str) -> None:
        """Handle an image-save request forwarded from JavaScript.

        Args:
            fmt: Image format identifier (e.g. ``'png'``, ``'svg'``).
            ext: File extension including dot (e.g. ``'.png'``).
            data_url: Base64-encoded data URL of the image.
        """
        path, _ = QFileDialog.getSaveFileName(
            None, 'Save Plot Image', f'ddo_plot{ext}',
            self._FILTER_MAP.get(fmt, 'All Files (*)'),
        )
        if not path:
            return
        try:
            header, payload = data_url.split(',', 1)
            if 'base64' in header:
                raw = base64.b64decode(payload)
            else:
                # SVG comes as data:image/svg+xml,<url-encoded content>
                raw = unquote(payload).encode('utf-8')
            if fmt == 'svg':
                # SVG is XML text — try UTF-8, fall back to latin-1
                try:
                    text = raw.decode('utf-8')
                except UnicodeDecodeError:
                    text = raw.decode('latin-1')
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(text)
            else:
                with open(path, 'wb') as f:
                    f.write(raw)
            filename = os.path.basename(path)
            self.image_saved.emit(f"Plot image saved to {filename}")
        except Exception as exc:
            logger.error('Failed to save image: %s', exc, exc_info=True)


class PlotlyPanel(QWidget):
    """Embeds a Plotly chart rendered as HTML inside a QWebEngineView."""

    image_saved = Signal(str)  # forwarded from bridge

    def __init__(self, placeholder_text: str = "", parent: QWidget | None = None) -> None:
        """Initialize the Plotly panel.

        Args:
            placeholder_text: Text shown when no chart is loaded.
            parent: Optional parent widget.
        """
        super().__init__(parent)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._bridge = _ImageSaveBridge(self)
        self._bridge.image_saved.connect(self.image_saved)

        # Optional placeholder label
        self._placeholder: QLabel | None = None
        if placeholder_text:
            self._placeholder = QLabel(placeholder_text)
            self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._placeholder.setStyleSheet("color: gray; font-size: 12pt;")
            self._layout.addWidget(self._placeholder)

        self._web_view = None
        self._html: str | None = None
        self._plotly_fig = None  # cache for export
        # Charts are loaded from a local temp file rather than via setHtml(),
        # because inlined plotly.js (used for offline rendering) is several MB —
        # well past Qt's documented ~2MB content limit for QWebEnginePage.setHtml().
        self._temp_dir = tempfile.mkdtemp(prefix="ddo_plot_")
        self._temp_html_path: str | None = None

    @property
    def html(self) -> str | None:
        """Return the current HTML string, or ``None`` if empty.

        Returns:
            The current HTML content, or None if no content is set.
        """
        return self._html

    @property
    def figure(self):
        """Return the cached Plotly figure (if any) for export."""
        return self._plotly_fig

    def set_html(self, html: str, fig=None) -> None:
        """Display Plotly HTML content, replacing any existing view.

        Args:
            html: Raw HTML string containing a Plotly chart.
            fig: Optional Plotly figure cached for later image export.
        """
        self._ensure_web_view()
        if self._placeholder:
            self._placeholder.hide()

        self._html = html
        self._plotly_fig = fig
        # Inject white body background to prevent black flash during compositing
        styled_html = html.replace(
            "<head>",
            "<head><style>body{background:#fff !important;}</style>",
            1,
        )
        # Inject extra download-format buttons into the modebar
        styled_html = styled_html.replace("</body>", _EXTRA_DOWNLOAD_JS + "</body>", 1)
        # Write to a fresh local temp file and load it (instead of setHtml()) so
        # the several-MB inlined plotly.js payload isn't subject to Qt's setHtml()
        # size limit. A new filename is used each time to avoid any browser-side
        # caching of a previously-loaded local file at the same path.
        old_path = self._temp_html_path
        new_path = os.path.join(self._temp_dir, f"plot_{uuid.uuid4().hex}.html")
        with open(new_path, "w", encoding="utf-8") as f:
            f.write(styled_html)
        self._temp_html_path = new_path
        self._web_view.load(QUrl.fromLocalFile(new_path))
        self._web_view.show()
        if old_path and old_path != new_path:
            try:
                os.remove(old_path)
            except OSError:
                pass  # best-effort cleanup; harmless if still locked/in use

    def set_figure(self, fig) -> None:
        """Accept a Plotly go.Figure, convert to HTML, and display.

        Args:
            fig: A Plotly ``go.Figure`` to render.
        """
        # Inline plotly.js (no CDN) so charts render without an internet connection.
        html = fig.to_html(include_plotlyjs=True, full_html=True,
                           config={"responsive": True, "displaylogo": False,
                                   "displayModeBar": True,
                                   "toImageButtonOptions": {
                                       "format": "svg",
                                       "filename": "ddo_plot",
                                       "width": 1200,
                                       "height": 700,
                                       "scale": 1,
                                   }})
        self.set_html(html, fig)

    def refresh(self) -> None:
        """Re-render the current HTML."""
        if self._html and self._web_view and self._temp_html_path:
            self._web_view.load(QUrl.fromLocalFile(self._temp_html_path))

    def clear(self) -> None:
        """Remove the chart and show placeholder."""
        self._html = None
        self._plotly_fig = None
        if self._web_view:
            self._web_view.setHtml("")
        if self._placeholder:
            self._placeholder.show()
        if self._temp_html_path:
            try:
                os.remove(self._temp_html_path)
            except OSError:
                pass
            self._temp_html_path = None

    def __del__(self) -> None:
        """Best-effort cleanup of the temp directory used for local chart HTML."""
        try:
            import shutil
            shutil.rmtree(self._temp_dir, ignore_errors=True)
        except Exception:
            pass

    def export_image(self, path: str, dpi: int = 150, width: int = 1200, height: int = 700) -> None:
        """Save the current figure to a static image file (PNG/SVG/PDF via kaleido).

        Args:
            path: Destination file path.
            dpi: Resolution in dots per inch.
            width: Image width in pixels.
            height: Image height in pixels.
        """
        if self._plotly_fig is not None:
            scale = dpi / 100.0
            self._plotly_fig.write_image(path, width=width, height=height, scale=scale)
        elif self._html:
            # Fallback: grab the web view as a pixmap
            if self._web_view:
                pixmap = self._web_view.grab()
                pixmap.save(path)

    def copy_to_clipboard(self) -> None:
        """Copy the current web view content to the system clipboard as an image."""
        if self._web_view:
            pixmap = self._web_view.grab()
            QApplication.clipboard().setPixmap(pixmap)

    def init_web_view(self) -> None:
        """Eagerly create the QWebEngineView (call during startup to avoid flash)."""
        self._ensure_web_view()

    def _ensure_web_view(self) -> None:
        """Lazily create the QWebEngineView on first use."""
        if self._web_view is None:
            from PySide6.QtWebEngineCore import QWebEngineSettings
            from PySide6.QtWebChannel import QWebChannel
            WebView = _get_web_engine_class()
            self._web_view = WebView(self)
            # White background to avoid black flash during compositor init
            self._web_view.page().setBackgroundColor(Qt.GlobalColor.white)
            self._web_view.setStyleSheet("background: white;")
            self._web_view.setHtml(
                "<html><body style='background:#fff;'></body></html>",
                QUrl("about:blank"),
            )
            # Register JS ↔ Qt bridge for the image-save dialog
            channel = QWebChannel(self._web_view.page())
            channel.registerObject('bridge', self._bridge)
            self._web_view.page().setWebChannel(channel)
            # Trigger Plotly resize after page finishes loading
            self._web_view.loadFinished.connect(self._on_load_finished)
            self._layout.addWidget(self._web_view)

    def _on_load_finished(self, ok: bool) -> None:
        """Trigger Plotly relayout after load so autosize charts render."""
        if self._web_view and self._html:
            # Poll until Plotly is loaded, then resize; force white bg
            resize_js = """
            (function waitForPlotly() {
                document.body.style.background = '#fff';
                var gd = document.querySelector('.plotly-graph-div');
                if (gd && window.Plotly) {
                    Plotly.Plots.resize(gd);
                } else {
                    setTimeout(waitForPlotly, 50);
                }
            })();
            """
            self._web_view.page().runJavaScript(resize_js)
            # QtWebEngine/Chromium (on some Windows GPU/D3D11 configurations)
            # doesn't actually present the first composited frame after a full
            # page load() until an input or resize event nudges it — the chart
            # appears black/blank until the user hovers over it. Force a
            # imperceptible 1px window resize to trigger a real repaint.
            self._nudge_repaint()

    def _nudge_repaint(self) -> None:
        """Force a compositor repaint by nudging the top-level window size.

        Works around a QtWebEngine quirk where the first frame after
        navigating to a new page isn't presented until an input/resize event
        occurs. The 1px resize-and-restore is visually imperceptible.
        """
        win = self._web_view.window() if self._web_view else None
        if win is None:
            return
        size = win.size()
        win.resize(size.width() + 1, size.height())
        QTimer.singleShot(0, lambda: win.resize(size) if win else None)

    def _deferred_resize(self) -> None:
        if self._web_view and self._html:
            self._web_view.page().runJavaScript(
                "var gd = document.querySelector('.plotly-graph-div');"
                "if (gd && window.Plotly) { Plotly.Plots.resize(gd); }"
            )
