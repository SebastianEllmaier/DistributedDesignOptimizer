# Copyright (C) The DistributedDesignOptimizer Contributors
# SPDX-License-Identifier: MIT
#
# MkDocs hook: LaTeX-style abbreviation references.
#
# Replaces abbr:KEY with <abbr title="Full Form">KEY</abbr> elements.
# Similar to \acrshort{} in LaTeX.
#
# Usage in markdown:
#   The abbr:ADMM framework is used for...
#   → renders as: The <abbr title="Alternating Directions Method of Multipliers">ADMM</abbr> framework is used for...
#
# Configuration in mkdocs.yml:
#   hooks:
#     - hooks/abbreviations.py

import logging
import re
from pathlib import Path

log = logging.getLogger("mkdocs.hooks.abbreviations")

# ── Regex ────────────────────────────────────────────────────────────────────
# Match abbr:KEY pattern where KEY is uppercase abbreviation
# Allows hyphens only when followed by uppercase/digits (e.g., BLISS-2000)
# Examples: abbr:ADMM, abbr:MDO, abbr:ALC, abbr:BLISS-2000
# Does NOT match: abbr:ATC-style (stops at ATC)
_ABBR_REF = re.compile(r"abbr:([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*)")
_ABBR_DEF_RE = re.compile(r"^\*\[(.+?)\]:\s+(.+)$")

# ── Module-level state ───────────────────────────────────────────────────────
_abbreviations: dict[str, str] = {}  # KEY -> Full Form
_used_abbreviations: set[str] = set()


def on_config(config):
    """Load abbreviations from abbreviations.md."""
    global _abbreviations
    
    mkdocs_dir = Path(config["config_file_path"]).parent
    abbr_file = mkdocs_dir / "content" / "includes" / "abbreviations.md"
    
    if not abbr_file.exists():
        log.warning("Abbreviations hook: abbreviations.md not found at %s", abbr_file)
        return config
    
    _abbreviations.clear()
    _used_abbreviations.clear()
    
    for line in abbr_file.read_text(encoding="utf-8").splitlines():
        m = _ABBR_DEF_RE.match(line.strip())
        if m:
            key = m.group(1)
            full_form = m.group(2)
            _abbreviations[key] = full_form
            # Also store lowercase version for case-insensitive matching
            _abbreviations[key.lower()] = full_form
    
    log.info("Abbreviations hook: %d abbreviations loaded", len(_abbreviations) // 2)
    return config


def on_page_markdown(markdown, page, config, files):
    """Replace abbr:KEY with <abbr> elements."""
    if not _abbreviations:
        return markdown
    
    def _replace_abbr(match):
        key = match.group(1).strip()
        # Try exact match first, then case-insensitive
        full_form = _abbreviations.get(key) or _abbreviations.get(key.lower())
        
        if not full_form:
            log.warning("Abbreviations hook: unknown abbreviation '%s' on page %s", 
                       key, page.url)
            return key  # Return just the key without abbr tag
        
        _used_abbreviations.add(key)
        # Return HTML abbr element
        return f'<abbr title="{full_form}">{key}</abbr>'
    
    return _ABBR_REF.sub(_replace_abbr, markdown)


def get_used_abbreviations() -> set[str]:
    """Return the set of abbreviations used across all pages.
    
    Can be called by generate_diagram.py to filter the nomenclature list.
    """
    return _used_abbreviations.copy()
