# Copyright (C) The DistributedDesignOptimizer Contributors
# SPDX-License-Identifier: MIT
#
# MkDocs hook: LaTeX-style symbol references.
#
# Replaces sym:KEY with a math symbol wrapped in a tooltip span.
# Similar to \gls{} in LaTeX glossary.
#
# Usage in markdown (prose):
#   The design variable sym:d is optimized...
#   → renders as: The design variable <span class="sym-ref" title="design variable">$d$</span> is optimized...
#
# Usage inside math delimiters \(...\) or \[...\]:
#   \(sym:k \leftarrow 0\)
#   → renders as: \(k \leftarrow 0\)  (just the raw LaTeX, no span)
#
# Configuration in mkdocs.yml:
#   hooks:
#     - hooks/symbols.py

import logging
import re
from pathlib import Path

log = logging.getLogger("mkdocs.hooks.symbols")

# ── Regex ────────────────────────────────────────────────────────────────────
# Match sym:KEY pattern where KEY is LaTeX content
# Examples: sym:d, sym:k, sym:v_f, sym:v_{g,\text{active}}, sym:\mathcal{D}, sym:\lambda, sym:Q^{\leq}
# Pattern structure:
#   1. Base: single letter OR LaTeX command with optional arg (\mathcal{D})
#   2. Optional subscript: either simple (_f) or complex with braces (_{g,\text{active}})
#   3. Optional superscript: either simple (^2) or complex (^{\leq}), but NOT iteration indices (^{(k)})
# The complex brace patterns use (?:[^{}]|\{[^}]*\})* to handle one level of nested braces
_SYM_REF = re.compile(
    r"sym:("
    r"(?:[A-Za-z]|\\[A-Za-z]+(?:\{[^}]*\})?)"  # Base: letter OR \cmd{arg}?
    r"(?:_(?:[A-Za-z0-9]|\{(?!\()(?:[^{}]|\{[^}]*\})*\}))?"  # Optional subscript
    r"(?:\^(?:[A-Za-z0-9]|\{(?!\()(?:[^{}]|\{[^}]*\})*\}))?"  # Optional superscript
    r")"
)

# Parse symbol table rows: | $symbol$ | Description | Value Range |
_SYM_TABLE_RE = re.compile(r"^\|\s*\$(.+?)\$\s*\|\s*(.+?)\s*\|.*$")

# Match math regions: \(...\) inline and \[...\] display math
# Use DOTALL so . matches newlines inside display math
_MATH_INLINE = re.compile(r"\\\(.*?\\\)", re.DOTALL)
_MATH_DISPLAY = re.compile(r"\\\[.*?\\\]", re.DOTALL)

# ── Module-level state ───────────────────────────────────────────────────────
_symbols: dict[str, str] = {}  # LaTeX key -> Description
_used_symbols: set[str] = set()


def _load_symbols_from_file(sym_file: Path) -> None:
    """Load symbols from a symbols.md file.
    
    This is the core loading logic, separated out so it can be called
    from on_config() or directly from other hooks.
    """
    global _symbols
    
    if not sym_file.exists():
        log.warning("Symbols hook: symbols.md not found at %s", sym_file)
        return
    
    _symbols.clear()
    
    for line in sym_file.read_text(encoding="utf-8").splitlines():
        m = _SYM_TABLE_RE.match(line.strip())
        if m:
            latex_key = m.group(1).strip()
            description = m.group(2).strip()
            _symbols[latex_key] = description
    
    log.info("Symbols hook: %d symbols loaded", len(_symbols))


def ensure_symbols_loaded(docs_src_dir: Path = None) -> None:
    """Ensure symbols are loaded, loading from file if needed.
    
    This function can be called by other hooks (e.g., unified_algorithmic_structure_pseudocode_traceability.py)
    to ensure the symbols dictionary is populated before calling process_symbols_in_text().
    
    Args:
        docs_src_dir: Path to the docs_src directory. If None, attempts to find it
                      relative to this file's location.
    """
    global _symbols
    
    if _symbols:
        return  # Already loaded
    
    if docs_src_dir is None:
        # Assume hooks/ is inside docs_src/
        docs_src_dir = Path(__file__).parent.parent
    
    sym_file = docs_src_dir / "content" / "includes" / "symbols.md"
    _load_symbols_from_file(sym_file)


def on_config(config):
    """Load symbols from symbols.md table."""
    global _used_symbols
    
    mkdocs_dir = Path(config["config_file_path"]).parent
    sym_file = mkdocs_dir / "content" / "includes" / "symbols.md"
    
    _used_symbols.clear()
    _load_symbols_from_file(sym_file)
    
    return config


def _replace_sym_in_math(match):
    """Replace sym:KEY inside math with just the raw LaTeX symbol."""
    key = match.group(1).strip()
    
    # Track usage even inside math
    if key in _symbols:
        _used_symbols.add(key)
    
    # Return just the raw LaTeX (no $ wrapper since we're already in math)
    return key


def _replace_sym_in_prose(match, page_url):
    """Replace sym:KEY in prose with tooltip-wrapped math."""
    key = match.group(1).strip()
    
    # Look up the description
    description = _symbols.get(key)
    
    if not description:
        log.warning("Symbols hook: unknown symbol '%s' on page %s", key, page_url)
        return f"${key}$"  # Return just the math without tooltip
    
    _used_symbols.add(key)
    # Escape quotes in description for HTML attribute
    desc_escaped = description.replace('"', '&quot;')
    # Return span with tooltip wrapping the math
    return f'<span class="sym-ref" title="{desc_escaped}">${key}$</span>'


def on_page_markdown(markdown, page, config, files):
    """Replace sym:KEY with appropriate output based on context."""
    if not _symbols:
        return markdown
    
    # Step 1: Process sym: inside math regions (just output raw LaTeX)
    def process_math_region(math_match):
        math_content = math_match.group(0)
        # Replace sym:KEY with just KEY inside the math
        return _SYM_REF.sub(_replace_sym_in_math, math_content)
    
    # Process inline math \(...\)
    markdown = _MATH_INLINE.sub(process_math_region, markdown)
    # Process display math \[...\]
    markdown = _MATH_DISPLAY.sub(process_math_region, markdown)
    
    # Step 2: Process remaining sym: in prose (output tooltip span)
    def replace_prose(match):
        return _replace_sym_in_prose(match, page.url)
    
    markdown = _SYM_REF.sub(replace_prose, markdown)
    
    return markdown


def get_used_symbols() -> set[str]:
    """Return the set of symbols used across all pages.
    
    Can be called by generate_diagram.py to filter the nomenclature list.
    """
    return _used_symbols.copy()


def process_symbols_in_text(text: str, page_url: str = "<external>") -> str:
    """Process sym:KEY syntax in raw text.
    
    This is a public function that can be called by other hooks
    (e.g., unified_algorithmic_structure_pseudocode_traceability.py) to process sym: syntax in
    text that was read directly from files (bypassing the normal
    hook processing order).
    
    Args:
        text: The raw text containing sym:KEY syntax
        page_url: Page URL for logging warnings about unknown symbols
        
    Returns:
        Text with sym: replaced appropriately (math context vs prose)
    """
    # Ensure symbols are loaded (needed when called from other hooks
    # that may have imported this module before MkDocs called on_config)
    ensure_symbols_loaded()
    
    if not _symbols:
        log.warning("Symbols hook: no symbols loaded, cannot process sym: syntax")
        return text
    
    # Step 1: Process sym: inside math regions (just output raw LaTeX)
    def process_math_region(math_match):
        math_content = math_match.group(0)
        return _SYM_REF.sub(_replace_sym_in_math, math_content)
    
    # Process inline math \(...)\)
    text = _MATH_INLINE.sub(process_math_region, text)
    # Process display math \[...]\]
    text = _MATH_DISPLAY.sub(process_math_region, text)
    
    # Step 2: Process remaining sym: in prose (output tooltip span)
    def replace_prose(match):
        return _replace_sym_in_prose(match, page_url)
    
    text = _SYM_REF.sub(replace_prose, text)
    
    return text
