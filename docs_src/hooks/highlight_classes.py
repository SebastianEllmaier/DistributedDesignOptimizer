# Copyright (C) The DistributedDesignOptimizer Contributors
# SPDX-License-Identifier: MIT
#
# MkDocs hook: VS Code Dark Modern syntax highlighting adjustments.
#
# Post-processes rendered HTML to re-tag Pygments tokens so that code blocks
# match the VS Code "Dark Modern" color scheme:
#
# 1. Known project class names: <span class="n"> → <span class="nc"> (teal)
# 2. Typing module types (List, Dict, …): <span class="n"> → <span class="nc"> (teal)
# 3. Method calls after dot: <span class="n"> → <span class="nf"> (yellow)
# 4. Bracket pair colorization: <span class="p"> → depth-aware color classes
#
# Reads CLASS_REGISTRY directly from the generate_api_docs module (shared
# memory when build_docs.py runs everything in a single process).
# Falls back to class_registry.json if the module hasn't been imported.
#
# Configuration in mkdocs.yml:
#   hooks:
#     - hooks/highlight_classes.py

import json
import logging
import re
from pathlib import Path

log = logging.getLogger("mkdocs.hooks.highlight_classes")

# ── Module-level state ───────────────────────────────────────────────────────
_class_names: set = set()

# Standard typing module types that should be colored as classes (teal)
_TYPING_TYPES: set = {
    'List', 'Dict', 'Tuple', 'Set', 'FrozenSet', 'Optional', 'Union',
    'Any', 'Callable', 'Iterator', 'Generator', 'Sequence', 'Mapping',
    'MutableMapping', 'MutableSequence', 'MutableSet', 'Type',
    'ClassVar', 'Final', 'Literal', 'TypeVar', 'Generic', 'Iterable',
}

# Regex to match <span class="n">ClassName</span> inside code blocks
# We only target spans with exactly class="n" (generic Name token)
_NAME_SPAN = re.compile(r'<span class="n">([^<]+)</span>')

# Regex to detect method calls: .method_name(
# Reclassifies the method name from "n" (Name) to "nf" (Name.Function → yellow)
_METHOD_CALL = re.compile(
    r'(<span class="o">\.</span>)'         # dot operator
    r'<span class="n">([^<]+)</span>'      # method name (to reclassify)
    r'(?=<span class="p">\()'             # lookahead: opening paren in punctuation
)

# Regex for punctuation spans (used by bracket pair colorization)
_PUNCT_SPAN = re.compile(r'<span class="p">([^<]+)</span>')

# Bracket pair colors cycle (VS Code Dark Modern defaults)
_BRACKET_CLASSES = ['bp1', 'bp2', 'bp3']
_OPEN_BRACKETS = '([{'
_CLOSE_BRACKETS = ')]}'


def on_config(config):
    """Load the class registry from the in-memory module or fallback JSON."""
    global _class_names

    # Primary: read directly from the already-imported module (single-process build)
    try:
        from scripts.generate_api_docs import CLASS_REGISTRY
        if CLASS_REGISTRY:
            _class_names = set(CLASS_REGISTRY.keys())
            log.info("highlight_classes hook: loaded %d class names from memory", len(_class_names))
            return config
    except ImportError:
        pass

    # Fallback: read from JSON file (standalone mkdocs build without build_docs.py)
    mkdocs_dir = Path(config["config_file_path"]).parent
    registry_file = mkdocs_dir / "class_registry.json"

    if not registry_file.exists():
        log.warning(
            "highlight_classes hook: no class registry available. "
            "Run build_docs.py or generate_api_docs.py first."
        )
        return config

    with open(registry_file, "r", encoding="utf-8") as f:
        _class_names = set(json.load(f))

    log.info("highlight_classes hook: loaded %d class names from JSON", len(_class_names))
    return config


def _replace_class_span(match: re.Match) -> str:
    """Replace <span class="n"> with <span class="nc"> if text is a known class or typing type."""
    name = match.group(1)
    if name in _class_names or name in _TYPING_TYPES:
        return f'<span class="nc">{name}</span>'
    return match.group(0)


def _replace_method_call(match: re.Match) -> str:
    """Reclassify method name after dot from "n" to "nf" (yellow)."""
    dot_span = match.group(1)
    method_name = match.group(2)
    return f'{dot_span}<span class="nf">{method_name}</span>'


def _colorize_brackets(html: str) -> str:
    """Add bracket pair colorization to punctuation spans.

    Tracks bracket nesting depth across the page and assigns color classes
    bp1 (gold), bp2 (orchid), bp3 (blue) cycling with depth, matching
    VS Code Dark Modern bracket pair colorization.
    """
    depth = 0

    def _replace_punct(match: re.Match) -> str:
        nonlocal depth
        content = match.group(1)

        # Fast path: no brackets in this span, leave unchanged
        if not any(c in content for c in _OPEN_BRACKETS + _CLOSE_BRACKETS):
            return match.group(0)

        parts = []
        for ch in content:
            if ch in _OPEN_BRACKETS:
                cls = _BRACKET_CLASSES[depth % 3]
                parts.append(f'<span class="{cls}">{ch}</span>')
                depth += 1
            elif ch in _CLOSE_BRACKETS:
                depth = max(0, depth - 1)
                cls = _BRACKET_CLASSES[depth % 3]
                parts.append(f'<span class="{cls}">{ch}</span>')
            else:
                parts.append(f'<span class="p">{ch}</span>')
        return ''.join(parts)

    return _PUNCT_SPAN.sub(_replace_punct, html)


def on_page_content(html: str, page, config, files) -> str:
    """Post-process rendered HTML to match VS Code Dark Modern highlighting."""
    # Only process pages that contain code blocks (performance optimization)
    if '<code class="language-python' not in html and "<code" not in html:
        return html

    # 1. Reclassify known class names and typing types: .n → .nc (teal)
    if _class_names or _TYPING_TYPES:
        html = _NAME_SPAN.sub(_replace_class_span, html)

    # 2. Reclassify method calls after dot: .n → .nf (yellow)
    html = _METHOD_CALL.sub(_replace_method_call, html)

    # 3. Bracket pair colorization: .p brackets → depth-aware color classes
    html = _colorize_brackets(html)

    return html
