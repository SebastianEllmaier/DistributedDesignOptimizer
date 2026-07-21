#!/usr/bin/env python3
"""
Auto-generate mermaid diagrams for the Architecture Overview page.

Called by build_docs.py during the documentation build.
Convention: every content subfolder may contain a ``generate_diagram.py`` with a
``generate(docs_dir: Path) -> None`` entry-point that build_docs will discover
and execute automatically.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Shared helpers (same logic used by generate_api_docs / generate_uml)
# ---------------------------------------------------------------------------

START_MARKER = "<!-- AUTO-GENERATED-DIAGRAM-START -->"
END_MARKER = "<!-- AUTO-GENERATED-DIAGRAM-END -->"


def _embed_mmd_in_index(mmd_path: Path, md_path: Path,
                        start_marker: str = START_MARKER,
                        end_marker: str = END_MARKER) -> None:
    """Read a .mmd file and embed its content into an index.md between markers.

    The mermaid content (including ````` ``mermaid`` fences) is placed between
    the given start and end markers.
    Everything outside the markers is preserved.
    """
    with open(mmd_path, 'r', encoding='utf-8') as f:
        mermaid_content = f.read()

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if start_marker in content and end_marker in content:
        before = content[:content.index(start_marker) + len(start_marker)]
        after = content[content.index(end_marker):]
        new_content = f"{before}\n{mermaid_content.strip()}\n{after}"
    else:
        print(f"  WARNING: Markers not found in {md_path}. Skipping diagram embedding.")
        return

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)


# ---------------------------------------------------------------------------
# Entry-point called by build_docs.py
# ---------------------------------------------------------------------------

def generate(docs_dir: Path) -> None:
    """Generate the top-level workspace structure mermaid diagram.

    Follows the same pattern as the API reference UML diagrams:
    1. Scans the repository root for top-level folders/files.
    2. Writes a ``.mmd`` file (``workspace_structure.mmd``).
    3. Reads the ``.mmd`` file and embeds it into ``index.md`` between markers.

    The ``.mmd`` file can be marked with ``%% @custom`` on the first line to
    prevent overwriting, consistent with ``generate_uml.py``.
    """
    repo_root = docs_dir.parent
    arch_dir = docs_dir / "content" / "framework-architecture"
    mmd_path = arch_dir / "workspace_structure.mmd"
    md_path = arch_dir / "core-components-and-unified-algorithmic-structure.md"

    if not md_path.exists():
        print("  WARNING: framework-architecture/core-components-and-unified-algorithmic-structure.md not found. Skipping.")
        return

    # Respect @custom marker (same convention as generate_uml.py)
    if mmd_path.exists():
        try:
            with open(mmd_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
            if first_line.startswith("%% @custom"):
                print(f"  PRESERVED (has @custom marker): {mmd_path}")
                _embed_mmd_in_index(mmd_path, md_path)
                return
        except Exception:
            pass

    # Determine top-level items (skip hidden / venv / cache dirs)
    skip = {'.git', '.venv', '.mypy_cache', '__pycache__', '.vscode',
            'node_modules', '.egg-info'}
    folders = []
    files = []
    for item in sorted(repo_root.iterdir()):
        if item.name.startswith('.') or item.name in skip:
            continue
        if item.is_dir():
            folders.append(item.name)
        elif item.is_file():
            files.append(item.name)

    # Build mermaid diagram (same style / theme as API class diagrams)
    lines = []
    lines.append("```mermaid")
    lines.append("%%{init: {'theme': 'base', 'themeVariables': { "
                 "'primaryColor': '#e6f4f7', "
                 "'primaryBorderColor': '#035970', "
                 "'primaryTextColor': '#000000', "
                 "'lineColor': '#035970', "
                 "'secondaryColor': '#cce9ef', "
                 "'tertiaryColor': '#f5fafb', "
                 "'noteBkgColor': '#e6f4f7', "
                 "'noteBorderColor': '#035970', "
                 "'fontFamily': 'Arial, sans-serif'"
                 "}}}%%")
    lines.append("classDiagram")
    lines.append("    direction TB")
    lines.append("")
    lines.append("    %% Top-level packages / folders")
    for folder in folders:
        folder_id = folder.replace('-', '_').replace('.', '_')
        lines.append(f'    class {folder_id}["{folder}/"]:::packageStyle')
    lines.append("")
    lines.append("    %% Top-level files")
    for f in files:
        file_id = f.replace('-', '_').replace('.', '_').replace(' ', '_')
        lines.append(f'    class {file_id}["{f}"]:::fileStyle')
    lines.append("")
    lines.append("    %% Style definitions")
    lines.append("    classDef packageStyle fill:#e8e8e8,stroke:#999999,stroke-width:2px")
    lines.append("    classDef fileStyle fill:#fff8e6,stroke:#FFCC80,stroke-width:2px")
    lines.append("```")

    mermaid_content = "\n".join(lines)

    # Write .mmd file
    arch_dir.mkdir(parents=True, exist_ok=True)
    with open(mmd_path, 'w', encoding='utf-8') as f:
        f.write(mermaid_content)

    # Embed into index.md
    _embed_mmd_in_index(mmd_path, md_path)

    print(f"  Generated architecture overview diagram "
          f"({len(folders)} folders, {len(files)} files)")
