# Copyright (C) The DistributedDesignOptimizer Contributors
# SPDX-License-Identifier: MIT
#
# MkDocs hook: LaTeX-style cross-page citations.
#
# Replaces [@key] with numbered superscript links pointing to the central
# references page. Generates the formatted bibliography on that page
# using pandoc + CSL (IEEE style).
#
# Configuration in mkdocs.yml:
#   hooks:
#     - hooks/citations.py
#   extra:
#     citations:
#       bib_file: "content/includes/Ellmaier_Group_clean.bib"
#       csl_file: "content/includes/ieee.csl"
#       references_url: "includes/references/"

import logging
import re
from collections import OrderedDict
from pathlib import Path

log = logging.getLogger("mkdocs.hooks.citations")

# ── Regex ────────────────────────────────────────────────────────────────────
# Match citation blocks: [@key] or [@key1; @key2; ...]
_CITE_BLOCK = re.compile(r"\[(@[\w.\-:]+(?:\s*;\s*@[\w.\-:]+)*)\]")
_CITE_KEY = re.compile(r"@([\w.\-:]+)")

# ── Module-level state (populated by on_config, used by on_page_markdown) ───
_bib_keys: set = set()
_cite_order: OrderedDict = OrderedDict()   # key → 1-based number
_cite_numbers: dict = {}                   # key → pandoc-assigned number
_bibliography_html: str = ""
_bib_file: str = ""
_csl_file: str = ""
_references_url: str = "includes/references/"
_BIB_CMD = "\\bibliography"


# ─── MkDocs events ──────────────────────────────────────────────────────────

def on_config(config):
    """Load bib file, scan docs for citations, render bibliography."""
    global _bib_keys, _bib_file, _csl_file, _references_url, _bibliography_html

    mkdocs_dir = Path(config["config_file_path"]).parent

    # Read configuration from extra.citations
    cit = config.get("extra", {}).get("citations", {})
    _bib_file = str(mkdocs_dir / cit.get(
        "bib_file", "content/includes/Ellmaier_Group_clean.bib"))
    _csl_file = str(mkdocs_dir / cit.get(
        "csl_file", "content/includes/ieee.csl"))
    _references_url = cit.get("references_url", "includes/references/")

    # 1. Parse bib file to get valid keys ─────────────────────────────────
    import pybtex.errors
    pybtex.errors.strict = False
    from pybtex.database import parse_file

    try:
        bib = parse_file(_bib_file, bib_format="bibtex")
        _bib_keys.clear()
        _bib_keys.update(bib.entries.keys())
    except Exception as exc:
        log.error("Citations hook – cannot parse bib file: %s", exc)
        return config

    log.info("Citations hook: %d bib entries loaded", len(_bib_keys))

    # 2. Scan all markdown for [@key] to build global citation order ──────
    docs_dir = Path(config["docs_dir"])
    _cite_order.clear()
    _cite_numbers.clear()
    n = 1
    for md_path in sorted(docs_dir.rglob("*.md")):
        try:
            text = md_path.read_text(encoding="utf-8")
        except Exception:
            continue
        for blk in _CITE_BLOCK.finditer(text):
            for km in _CITE_KEY.finditer(blk.group(1)):
                key = km.group(1)
                if key in _bib_keys and key not in _cite_order:
                    _cite_order[key] = n
                    n += 1

    if not _cite_order:
        log.info("Citations hook: no citations found")
        return config

    log.info("Citations hook: %d unique citations across docs", len(_cite_order))

    # 3. Render bibliography via pandoc + CSL ─────────────────────────────
    _bibliography_html = _render_bibliography()
    return config


def on_page_markdown(markdown, page, config, files):
    """Replace [@key] with cross-page links; inject bibliography."""
    if not _cite_order:
        return markdown

    # Relative path from this page to the references page
    page_url = page.url or ""
    depth = len([seg for seg in page_url.split("/") if seg])
    prefix = "../" * depth if depth else ""
    ref_base = prefix + _references_url

    def _replace_block(match):
        keys = [m.group(1) for m in _CITE_KEY.finditer(match.group(1))]
        valid = [k for k in keys if k in _cite_order]
        if not valid:
            return match.group(0)

        nums = _cite_numbers if _cite_numbers else _cite_order
        links = []
        for k in valid:
            n = nums.get(k, _cite_order.get(k, "?"))
            links.append(
                f'<a class="citation-ref" href="{ref_base}#ref-{k}">{n}</a>'
            )
        return "<sup>[" + ",\u2009".join(links) + "]</sup>"

    markdown = _CITE_BLOCK.sub(_replace_block, markdown)

    # On the references page, replace \bibliography with formatted entries
    if _BIB_CMD in markdown:
        markdown = markdown.replace(_BIB_CMD, _bibliography_html)

    return markdown


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _render_bibliography() -> str:
    """Run pandoc once to format all cited references as HTML."""
    try:
       import pypandoc
    except ImportError:
        log.warning("Citations hook: pypandoc not installed, using fallback")
        return _fallback_bibliography()

    keys = list(_cite_order.keys())

    # One citation per sentence keeps pandoc numbering in our order
    lines = [f"Ref{i} [@{k}].\n" for i, k in enumerate(keys, 1)]
    md_input = "\n".join(lines)

    try:
        html = pypandoc.convert_text(
            md_input, "html", format="markdown",
            extra_args=[
                f"--bibliography={_bib_file}",
                f"--csl={_csl_file}",
                "--citeproc",
            ],
        )
    except Exception as exc:
        log.error("Citations hook – pandoc failed: %s", exc)
        return _fallback_bibliography()

    # Extract pandoc-assigned numbers from inline citations
    for m in re.finditer(
        r'data-cites="([\w.\-:]+)"[^>]*>\[?(\d+)\]?', html
    ):
        _cite_numbers[m.group(1)] = int(m.group(2))

    # Extract the <div id="refs" ...> block (always at end of output)
    idx = html.find('<div id="refs"')
    if idx >= 0:
        return html[idx:].strip()

    log.warning("Citations hook: refs div not found in pandoc output")
    return _fallback_bibliography()


def _fallback_bibliography() -> str:
    """Plain-text fallback if pandoc is unavailable."""
    entries = []
    for key, num in _cite_order.items():
        entries.append(f'<p id="ref-{key}">[{num}] <em>{key}</em></p>')
    return "\n".join(entries)
