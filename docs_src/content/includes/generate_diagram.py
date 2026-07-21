"""Auto-generate the abbreviations and symbols tables in index.md.

Keeps abbreviations.md and symbols.md as the single sources of truth.
The tables between the AUTO-GENERATED markers in index.md are rebuilt
on every run.

Similar to references.md, only abbreviations/symbols actually used in the
documentation are included in the generated tables.

Discovered and executed automatically by ``build_docs.run_content_diagram_generators()``.
"""

from __future__ import annotations

import re
from pathlib import Path

_ABBR_START = "<!-- AUTO-GENERATED-TABLE-START -->"
_ABBR_END = "<!-- AUTO-GENERATED-TABLE-END -->"
_SYM_START = "<!-- AUTO-GENERATED-SYMBOLS-START -->"
_SYM_END = "<!-- AUTO-GENERATED-SYMBOLS-END -->"
_ABBR_RE = re.compile(r"^\*\[(.+?)\]:\s+(.+)$")
_TABLE_ROW_RE = re.compile(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|$")


def _scan_docs_for_abbreviations(content_dir: Path, all_abbrs: list[tuple[str, str]]) -> set[str]:
    """Scan all markdown files for used abbreviations.
    
    Returns set of abbreviation strings that appear in the documentation.
    """
    used = set()
    abbr_strings = [abbr for abbr, _ in all_abbrs]
    
    for md_path in sorted(content_dir.rglob("*.md")):
        # Skip the nomenclature index itself and abbreviations.md
        if md_path.name in ("abbreviations.md", "symbols.md"):
            continue
        if "includes/index.md" in str(md_path):
            continue
            
        try:
            text = md_path.read_text(encoding="utf-8")
        except Exception:
            continue
        
        for abbr in abbr_strings:
            # Match as whole word (not inside another word)
            # Use word boundary for simple abbreviations
            pattern = r'\b' + re.escape(abbr) + r'\b'
            if re.search(pattern, text):
                used.add(abbr)
    
    return used


def _scan_docs_for_symbols(content_dir: Path, all_symbols: list[tuple[str, str, str]]) -> set[str]:
    """Scan all markdown files for used mathematical symbols.
    
    Returns set of symbol LaTeX strings that appear in the documentation.
    Symbols are matched by their LaTeX representation (e.g., \\mathcal{D}, v_f).
    """
    used = set()
    
    # Build patterns for each symbol
    # Extract the core LaTeX from $...$ wrapper
    symbol_patterns = []
    for sym, desc, _ in all_symbols:
        # Remove $ wrappers
        core = sym.strip().strip('$').strip()
        if core:
            symbol_patterns.append((sym, core))
    
    for md_path in sorted(content_dir.rglob("*.md")):
        # Skip the nomenclature index itself and symbols.md
        if md_path.name in ("abbreviations.md", "symbols.md"):
            continue
        if "includes/index.md" in str(md_path):
            continue
            
        try:
            text = md_path.read_text(encoding="utf-8")
        except Exception:
            continue
        
        for sym, core in symbol_patterns:
            # Escape for regex but handle LaTeX commands specially
            escaped = re.escape(core)
            if escaped in text or core in text:
                used.add(sym)
    
    return used


def _parse_abbreviations(abbr_path: Path) -> list[tuple[str, str]]:
    """Return list of (abbreviation, full_form) from abbreviations.md."""
    entries: list[tuple[str, str]] = []
    for line in abbr_path.read_text(encoding="utf-8").splitlines():
        m = _ABBR_RE.match(line.strip())
        if m:
            entries.append((m.group(1), m.group(2)))
    return entries


def _parse_symbols(sym_path: Path) -> list[tuple[str, str, str]]:
    """Return list of (symbol, description, value_range) from symbols.md."""
    entries: list[tuple[str, str, str]] = []
    for line in sym_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("<!--") or stripped.startswith("|---") or stripped == "":
            continue
        # Skip the header row
        m = _TABLE_ROW_RE.match(stripped)
        if m:
            sym, desc, vrange = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
            if sym.lower() == "symbol":
                continue
            entries.append((sym, desc, vrange))
    return entries


def _build_abbr_table(entries: list[tuple[str, str]]) -> str:
    """Build a `.doc-table` HTML table from abbreviation entries."""
    lines = [
        '<table class="doc-table">',
        "  <thead>",
        "    <tr>",
        "      <th>Abbreviation</th>",
        "      <th>Full Form</th>",
        "    </tr>",
        "  </thead>",
        "  <tbody>",
    ]
    for abbr, full in entries:
        lines.append("    <tr>")
        lines.append(f"      <td>{abbr}</td>")
        lines.append(f"      <td>{full}</td>")
        lines.append("    </tr>")
    lines.append("  </tbody>")
    lines.append("</table>")
    return "\n".join(lines)


def _build_sym_table(entries: list[tuple[str, str, str]]) -> str:
    """Build a `.doc-table` HTML table from symbol entries."""
    lines = [
        '<table class="doc-table">',
        "  <thead>",
        "    <tr>",
        "      <th>Symbol</th>",
        "      <th>Description</th>",
        "      <th>Value Range</th>",
        "    </tr>",
        "  </thead>",
        "  <tbody>",
    ]
    for sym, desc, vrange in entries:
        lines.append("    <tr>")
        lines.append(f"      <td>{sym}</td>")
        lines.append(f"      <td>{desc}</td>")
        lines.append(f"      <td>{vrange}</td>")
        lines.append("    </tr>")
    lines.append("  </tbody>")
    lines.append("</table>")
    return "\n".join(lines)


def _inject(content: str, start_marker: str, end_marker: str, table: str) -> str:
    """Replace content between markers with the given table."""
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    if start_idx == -1 or end_idx == -1:
        return content
    return (
        content[: start_idx + len(start_marker)]
        + "\n"
        + table
        + "\n"
        + content[end_idx:]
    )


def generate(docs_dir: Path) -> None:
    """Read data files and inject tables into index.md.
    
    Only includes abbreviations/symbols actually used in the documentation.
    """
    here = Path(__file__).resolve().parent
    content_dir = docs_dir / "content"
    index_path = here / "index.md"
    if not index_path.exists():
        return

    content = index_path.read_text(encoding="utf-8")
    new_content = content

    # --- Abbreviations ---
    abbr_path = here / "abbreviations.md"
    if abbr_path.exists():
        all_entries = _parse_abbreviations(abbr_path)
        if all_entries:
            # Filter to only used abbreviations
            used_abbrs = _scan_docs_for_abbreviations(content_dir, all_entries)
            entries = [(abbr, full) for abbr, full in all_entries if abbr in used_abbrs]
            print(f"  Abbreviations: {len(entries)} used of {len(all_entries)} defined")
            new_content = _inject(new_content, _ABBR_START, _ABBR_END,
                                  _build_abbr_table(entries))

    # --- Symbols ---
    sym_path = here / "symbols.md"
    if sym_path.exists():
        all_entries = _parse_symbols(sym_path)
        if all_entries:
            # Filter to only used symbols
            used_syms = _scan_docs_for_symbols(content_dir, all_entries)
            entries = [(sym, desc, vrange) for sym, desc, vrange in all_entries if sym in used_syms]
            print(f"  Symbols: {len(entries)} used of {len(all_entries)} defined")
            new_content = _inject(new_content, _SYM_START, _SYM_END,
                                  _build_sym_table(entries))

    if new_content != content:
        index_path.write_text(new_content, encoding="utf-8")
        print(f"  Updated {index_path.relative_to(docs_dir.parent)}")
    else:
        print(f"  {index_path.relative_to(docs_dir.parent)} is up to date")

    # --- Preprocess .bib file for pybtex compatibility ---
    _preprocess_bib(here, docs_dir)


# ---------------------------------------------------------------------------
#  BibTeX preprocessing: convert Biblatex extended name format to standard
#  BibTeX so pybtex (used by mkdocs-bibtex) can parse it.
#
#  Input :  Ellmaier_Group.bib        (original, never modified)
#  Output:  Ellmaier_Group_clean.bib  (auto-generated, used by mkdocs)
# ---------------------------------------------------------------------------

# Matches a single extended-name block:
#   family=Weck, given=Olivier, prefix=de, useprefix=true
_EXT_NAME_RE = re.compile(
    r"family\s*=\s*(?P<family>[^,]+)"
    r",\s*given\s*=\s*(?P<given>[^,]+)"
    r"(?:,\s*prefix\s*=\s*(?P<prefix>[^,]+))?"
    r"(?:,\s*useprefix\s*=\s*(?P<useprefix>[^,}\s]+))?"
)


def _convert_extended_name(match: re.Match) -> str:
    """Convert one Biblatex extended-name block to standard BibTeX."""
    family = match.group("family").strip()
    given = match.group("given").strip()
    prefix = (match.group("prefix") or "").strip()
    if prefix:
        # Standard BibTeX: 'prefix Family, Given' — the lowercase prefix
        # is automatically recognised as a von-part by BibTeX/pybtex.
        return f"{prefix} {family}, {given}"
    return f"{family}, {given}"


def _preprocess_bib(here: Path, docs_dir: Path) -> None:
    """Create a cleaned .bib file with standard BibTeX name format."""
    src = here / "Ellmaier_Group.bib"
    dst = here / "Ellmaier_Group_clean.bib"
    if not src.exists():
        return

    original = src.read_text(encoding="utf-8")
    cleaned = _EXT_NAME_RE.sub(_convert_extended_name, original)

    if dst.exists() and dst.read_text(encoding="utf-8") == cleaned:
        print(f"  {dst.relative_to(docs_dir.parent)} is up to date")
        return

    dst.write_text(cleaned, encoding="utf-8")
    print(f"  Updated {dst.relative_to(docs_dir.parent)}")
