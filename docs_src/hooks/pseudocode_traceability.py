# Copyright (C) The DistributedDesignOptimizer Contributors
# SPDX-License-Identifier: MIT
#
# MkDocs hook: Pseudocode-to-Code Traceability (Multi-Algorithm Support)
#
# Generates a side-by-side view mapping pseudocode steps to implementing
# classes/methods, and injects back-reference admonitions into API pages.
#
# Supported algorithms:
#   - Unified Algorithmic Structure
#   - Augmented Lagrangian Coordination (ALC)
#   - (Add new algorithms to _ALGORITHMS list)
#
# Configuration in mkdocs.yml:
#   hooks:
#     - hooks/pseudocode_traceability.py

import ast
import logging
import re
import sys
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Optional

try:
   import yaml
except ImportError:
    yaml = None

# Import symbols hook for processing sym: in copied pseudocode
# MkDocs runs hooks from the docs_src directory, so we need to add the hooks dir to path
_hooks_dir = Path(__file__).parent
if str(_hooks_dir) not in sys.path:
    sys.path.insert(0, str(_hooks_dir))

try:
   import symbols as symbols_hook
except ImportError:
    symbols_hook = None

log = logging.getLogger("mkdocs.hooks.unified_algorithmic_structure_pseudocode_traceability")


# ── Algorithm Configuration ──────────────────────────────────────────────────

@dataclass
class AlgorithmConfig:
    """Configuration for a pseudocode-to-code traceability algorithm."""
    id: str
    placeholder: str
    yaml_file: str
    pseudocode_source: str
    algorithm_number: int
    caption: str
    css_class: str
    traceability_url: str


# Define supported algorithms
_ALGORITHMS = [
    AlgorithmConfig(
        id="unified",
        placeholder="<!-- UNIFIED-ALGORITHMIC-STRUCTURE-PSEUDOCODE-TRACEABILITY -->",
        yaml_file="unified_algorithmic_structure_pseudocode_mapping.yaml",
        pseudocode_source="distributed-optimization-for-multidisciplinary-design/unified-algorithmic-structure.md",
        algorithm_number=1,
        caption="Unified Algorithmic Structure",
        css_class="unified-algorithmic-structure-pseudocode-traceability",
        traceability_url="framework-architecture/core-components-and-unified-algorithmic-structure.md",
    ),
    AlgorithmConfig(
        id="alc",
        placeholder="<!-- ALC-PSEUDOCODE-TRACEABILITY -->",
        yaml_file="alc_pseudocode_mapping.yaml",
        pseudocode_source="distributed-optimization-for-multidisciplinary-design/coordination-methods/augmented-lagrangian-coordination.md",
        algorithm_number=2,
        caption="Augmented Lagrangian Coordination (ALC)",
        css_class="alc-pseudocode-traceability",
        traceability_url="framework-architecture/pseudocode-traceability/augmented-lagrangian-coordination-pseudocode-traceability.md",
    ),
    AlgorithmConfig(
        id="consensus_alc",
        placeholder="<!-- CONSENSUS-ALC-PSEUDOCODE-TRACEABILITY -->",
        yaml_file="consensus_alc_pseudocode_mapping.yaml",
        pseudocode_source="distributed-optimization-for-multidisciplinary-design/coordination-methods/consensus-augmented-lagrangian-coordination.md",
        algorithm_number=3,
        caption="Consensus Augmented Lagrangian Coordination (Consensus ALC)",
        css_class="consensus-alc-pseudocode-traceability",
        traceability_url="framework-architecture/pseudocode-traceability/consensus-augmented-lagrangian-coordination-pseudocode-traceability.md",
    ),
    AlgorithmConfig(
        id="aladin",
        placeholder="<!-- ALADIN-PSEUDOCODE-TRACEABILITY -->",
        yaml_file="aladin_pseudocode_mapping.yaml",
        pseudocode_source="distributed-optimization-for-multidisciplinary-design/coordination-methods/aladin.md",
        algorithm_number=4,
        caption="Augmented Lagrangian Alternating Direction Inexact Newton (ALADIN)",
        css_class="aladin-pseudocode-traceability",
        traceability_url="framework-architecture/pseudocode-traceability/aladin-pseudocode-traceability.md",
    ),
    AlgorithmConfig(
        id="sbdp",
        placeholder="<!-- SBDP-PSEUDOCODE-TRACEABILITY -->",
        yaml_file="sbdp_pseudocode_mapping.yaml",
        pseudocode_source="distributed-optimization-for-multidisciplinary-design/coordination-methods/sensitivity-based-distributed-programming.md",
        algorithm_number=5,
        caption="Sensitivity Based Distributed Programming (SBDP)",
        css_class="sbdp-pseudocode-traceability",
        traceability_url="framework-architecture/pseudocode-traceability/sensitivity-based-distributed-programming-pseudocode-traceability.md",
    ),
    AlgorithmConfig(
        id="subsystem_copyfrom",
        placeholder="<!-- SUBSYSTEM-COPYFROM-PSEUDOCODE-TRACEABILITY -->",
        yaml_file="subsystem_copyfrom_pseudocode_mapping.yaml",
        pseudocode_source="framework-architecture/subsystem-copyfrom.md",
        algorithm_number=0,
        caption="SubSystemBasis.CopyFromMiddleLevel()",
        css_class="subsystem-copyfrom-pseudocode-traceability",
        traceability_url="framework-architecture/core-components-and-unified-algorithmic-structure.md",
    ),
    AlgorithmConfig(
        id="subsystem_copyto",
        placeholder="<!-- SUBSYSTEM-COPYTO-PSEUDOCODE-TRACEABILITY -->",
        yaml_file="subsystem_copyto_pseudocode_mapping.yaml",
        pseudocode_source="framework-architecture/subsystem-copyto.md",
        algorithm_number=0,
        caption="SubSystemBasis.CopyToMiddleLevel()",
        css_class="subsystem-copyto-pseudocode-traceability",
        traceability_url="framework-architecture/core-components-and-unified-algorithmic-structure.md",
    ),
    AlgorithmConfig(
        id="subsystem_run_iterative_optimization",
        placeholder="<!-- SUBSYSTEM-RUN-ITERATIVE-OPTIMIZATION-PSEUDOCODE-TRACEABILITY -->",
        yaml_file="subsystem_run_iterative_optimization_pseudocode_mapping.yaml",
        pseudocode_source="framework-architecture/subsystem-run-iterative-optimization.md",
        algorithm_number=0,
        caption="SubSystemBasis.run_IterativeOptimization()",
        css_class="subsystem-run-iterative-optimization-pseudocode-traceability",
        traceability_url="framework-architecture/core-components-and-unified-algorithmic-structure.md",
    ),
]


# ── Module-level state ───────────────────────────────────────────────────────
# Per-algorithm data: algorithm_id -> {mappings, math_symbol_mappings}
_algorithm_data: Dict[str, dict] = {}
_method_to_mappings = defaultdict(list)  # "Module.Class.method" -> list of (algo_id, entry) tuples
_validation_warnings = []
_api_base_path = "api"


# ─── MkDocs events ──────────────────────────────────────────────────────────

def on_config(config):
    """Load and validate all algorithm mapping YAML files."""
    global _algorithm_data, _method_to_mappings, _validation_warnings

    if yaml is None:
        log.error("Pseudocode traceability hook: PyYAML not installed")
        return config

    mkdocs_dir = Path(config["config_file_path"]).parent
    repo_root = mkdocs_dir.parent
    
    _algorithm_data.clear()
    _method_to_mappings.clear()
    _validation_warnings.clear()

    total_mappings = 0
    total_math_symbols = 0

    for algo in _ALGORITHMS:
        mapping_file = mkdocs_dir / "content" / "includes" / algo.yaml_file

        if not mapping_file.exists():
            log.warning(
                "Pseudocode traceability hook: mapping file not found for %s at %s",
                algo.id, mapping_file
            )
            continue

        # Load YAML
        with open(mapping_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        mappings = data.get("mappings", [])
        math_symbol_mappings = data.get("math_symbol_mappings", [])
        
        _algorithm_data[algo.id] = {
            "mappings": mappings,
            "math_symbol_mappings": math_symbol_mappings,
            "config": algo,
        }

        # Build reverse index: method key -> list of (algo_id, entry) tuples
        for entry in mappings:
            for impl in entry.get("implementations", []):
                key = f"{impl['module']}.{impl['class']}.{impl['method']}"
                _method_to_mappings[key].append((algo.id, entry))

        # Validate that referenced methods exist in source code
        _validate_mappings(repo_root, mappings, algo.id, algo.yaml_file)
        _validate_math_symbol_mappings(repo_root, math_symbol_mappings, algo.id, algo.yaml_file)

        total_mappings += len(mappings)
        total_math_symbols += len(math_symbol_mappings)
        
        log.info("Pseudocode traceability: loaded %s (%d mappings, %d math symbols)",
                 algo.id, len(mappings), len(math_symbol_mappings))

    if _validation_warnings and not getattr(on_config, '_warned', False):
        on_config._warned = True
        log.warning("=" * 70)
        log.warning("PSEUDOCODE TRACEABILITY: %d mapping(s) may need updating!", len(_validation_warnings))
        log.warning("=" * 70)
        for warn in _validation_warnings:
            log.warning("  ⚠ %s", warn)
        log.warning("-" * 70)
        log.warning("  Please review and update the relevant YAML mapping files in content/includes/")
        log.warning("=" * 70)

    log.info("Pseudocode traceability hook: %d total mappings + %d math symbols loaded from %d algorithms, %d warnings",
             total_mappings, total_math_symbols, len(_algorithm_data), len(_validation_warnings))
    return config


def on_page_markdown(markdown, page, config, files):
    """Inject traceability content into relevant pages."""
    if not _algorithm_data:
        return markdown

    page_url = page.url or ""

    # 1. Check each algorithm's placeholder and inject traceability HTML
    for algo in _ALGORITHMS:
        if algo.id not in _algorithm_data:
            continue
        if algo.placeholder in markdown and "framework-architecture" in page_url:
            html = _generate_traceability_html(algo, page_url, config)
            markdown = markdown.replace(algo.placeholder, html)

    # 2. On API pages: inject back-references into method documentation
    if page_url.startswith(_api_base_path + "/") or page_url.startswith("api/"):
        markdown = _inject_back_references(markdown, page_url)

    return markdown


# ─── Validation ──────────────────────────────────────────────────────────────

def _validate_mappings(repo_root: Path, mappings: List[dict], algo_id: str, yaml_file: str):
    """Validate that all referenced classes/methods exist in the source code."""
    global _validation_warnings

    # Cache parsed modules
    parsed_cache = {}

    for entry in mappings:
        for impl in entry.get("implementations", []):
            module_path = impl["module"]
            class_name = impl["class"]
            method_name = impl["method"]

            # Convert module path to file path
            file_path = repo_root / module_path.replace(".", "/") / "__init__.py"
            if not file_path.exists():
                # Try as a .py file (not a package)
                parts = module_path.rsplit(".", 1)
                if len(parts) == 2:
                    file_path = repo_root / parts[0].replace(".", "/") / (parts[1] + ".py")
                else:
                    file_path = repo_root / (module_path.replace(".", "/") + ".py")

            if not file_path.exists():
                _validation_warnings.append(
                    f"[{algo_id}:{entry['id']}] Module file not found: {module_path} "
                    f"(expected at {file_path}) - check {yaml_file}"
                )
                continue

            # Parse the file if not cached
            cache_key = str(file_path)
            if cache_key not in parsed_cache:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        tree = ast.parse(f.read(), filename=str(file_path))
                    parsed_cache[cache_key] = tree
                except (SyntaxError, UnicodeDecodeError) as e:
                    _validation_warnings.append(
                        f"[{algo_id}:{entry['id']}] Cannot parse {file_path}: {e}"
                    )
                    continue

            tree = parsed_cache[cache_key]

            # Find the class
            class_found = False
            method_found = False
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == class_name:
                    class_found = True
                    # Find the method
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef) and item.name == method_name:
                            method_found = True
                            break
                        elif isinstance(item, ast.AsyncFunctionDef) and item.name == method_name:
                            method_found = True
                            break
                    break

            if not class_found:
                _validation_warnings.append(
                    f"[{algo_id}:{entry['id']}] Class '{class_name}' not found in {module_path}"
                )
            elif not method_found:
                _validation_warnings.append(
                    f"[{algo_id}:{entry['id']}] Method '{class_name}.{method_name}()' not found in {module_path}"
                )


def _validate_math_symbol_mappings(repo_root: Path, math_symbol_mappings: List[dict], algo_id: str, yaml_file: str):
    """Validate that all methods referenced in math_symbol_mappings exist."""
    global _validation_warnings

    parsed_cache = {}

    for entry in math_symbol_mappings:
        for impl in entry.get("implementations", []):
            module_path = impl["module"]
            class_name = impl["class"]
            method_name = impl["method"]

            file_path = repo_root / module_path.replace(".", "/") / "__init__.py"
            if not file_path.exists():
                parts = module_path.rsplit(".", 1)
                if len(parts) == 2:
                    file_path = repo_root / parts[0].replace(".", "/") / (parts[1] + ".py")
                else:
                    file_path = repo_root / (module_path.replace(".", "/") + ".py")

            if not file_path.exists():
                _validation_warnings.append(
                    f"[{algo_id}:math:{entry['id']}] Module file not found: {module_path} - check {yaml_file}"
                )
                continue

            cache_key = str(file_path)
            if cache_key not in parsed_cache:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        tree = ast.parse(f.read(), filename=str(file_path))
                    parsed_cache[cache_key] = tree
                except (SyntaxError, UnicodeDecodeError) as e:
                    _validation_warnings.append(
                        f"[{algo_id}:math:{entry['id']}] Cannot parse {file_path}: {e}"
                    )
                    continue

            tree = parsed_cache[cache_key]

            class_found = False
            method_found = False
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == class_name:
                    class_found = True
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == method_name:
                            method_found = True
                            break
                    break

            if not class_found:
                _validation_warnings.append(
                    f"[{algo_id}:math:{entry['id']}] Class '{class_name}' not found in {module_path}"
                )
            elif not method_found:
                _validation_warnings.append(
                    f"[{algo_id}:math:{entry['id']}] Method '{class_name}.{method_name}()' not found in {module_path}"
                )


# ─── HTML Generation ─────────────────────────────────────────────────────────

def _resolve_api_url(module_path: str, class_name: str, method_name: str, from_page_url: str) -> str:
    """Resolve a module.class.method reference to a relative API docs URL."""
    parts = module_path.split(".")
    module_file = parts[-1]
    module_dir = "/".join(parts[:-1])

    # Calculate relative path from the current page
    from_depth = len([s for s in from_page_url.rstrip("/").split("/") if s])
    prefix = "../" * from_depth if from_depth else ""
    
    url = f"{prefix}{_api_base_path}/{module_dir}/{module_file}.md"
    
    # Add class anchor (MkDocs generates anchors from headings)
    anchor = class_name.lower()
    
    return f"{url}#{anchor}"


def _resolve_api_url_html(module_path: str, class_name: str, method_name: str, from_page_url: str) -> str:
    """Resolve to HTML URL (for rendered site navigation)."""
    parts = module_path.split(".")
    module_file = parts[-1]
    module_dir = "/".join(parts[:-1])
    
    from_depth = len([s for s in from_page_url.rstrip("/").split("/") if s])
    prefix = "../" * from_depth if from_depth else ""
    
    anchor = class_name.lower()
    return f"{prefix}{_api_base_path}/{module_dir}/{module_file}/#{anchor}"


def _generate_traceability_html(algo: AlgorithmConfig, page_url: str, config) -> str:
    """Generate the side-by-side traceability HTML for a specific algorithm."""
    
    algo_data = _algorithm_data.get(algo.id, {})
    mappings = algo_data.get("mappings", [])
    math_symbol_mappings = algo_data.get("math_symbol_mappings", [])
    
    # Build a lookup: algo_line -> list of mapping entries
    line_to_mappings = defaultdict(list)
    for entry in mappings:
        for line in entry.get("algo_lines", []):
            line_to_mappings[line].append(entry)

    # Full-width pseudocode with data attributes on linked lines
    algo_html = _generate_pseudocode_left(algo, line_to_mappings, math_symbol_mappings, config)
    
    # Hidden popup data (JSON-like) embedded as data attributes per mapping
    popup_data_html = _generate_popup_data(mappings, math_symbol_mappings, page_url)

    html = f'''
<div class="{algo.css_class}" markdown="0">
<div class="traceability-header">
<p>Highlighted lines are linked to the implementation. Hover or click to see the implementing classes/methods, then click through to the full API documentation.</p>
</div>
<div class="algorithm">
<div class="algorithm-caption"><strong>{"Procedure" if algo.algorithm_number == 0 else "Algorithm " + str(algo.algorithm_number)}</strong> {algo.caption}</div>
<div class="algo-body">
{algo_html}
</div>
</div>
<div class="impl-popup" id="impl-popup-{algo.id}" style="display:none;">
<div class="impl-popup-header">
<span class="impl-popup-label"></span>
<span class="impl-popup-close">&times;</span>
</div>
<div class="impl-popup-body"></div>
</div>
{popup_data_html}
</div>
'''
    return html


def _generate_pseudocode_left(algo: AlgorithmConfig, line_to_mappings: dict, math_symbol_mappings: list, config) -> str:
    """Parse the pseudocode HTML from the algorithm's source file and
    inject data attributes on lines that have traceability mappings.

    This avoids duplicating the pseudocode; changes to the source file
    are automatically reflected in the traceability view.
    """
    mkdocs_dir = Path(config["config_file_path"]).parent
    source_file = mkdocs_dir / "content" / algo.pseudocode_source

    if not source_file.exists():
        log.error("Pseudocode traceability: source file not found for %s at %s", algo.id, source_file)
        return f"<p><em>Error: pseudocode source not found at {algo.pseudocode_source}</em></p>"

    raw = source_file.read_text(encoding="utf-8")

    # Extract the <div class="algo-body">...</div> block
    body_start = raw.find('<div class="algo-body">')
    if body_start == -1:
        log.error("Pseudocode traceability: could not find algo-body in %s", source_file)
        return f"<p><em>Error: algo-body not found in {algo.pseudocode_source}</em></p>"

    # Find the matching closing </div> — the algo-body is followed by two closing </div>s
    # (one for algo-body, one for algorithm).  We grab everything between.
    body_content_start = raw.index(">", body_start) + 1
    # Walk forward counting nested divs to find the correct closing tag
    depth = 1
    pos = body_content_start
    while depth > 0 and pos < len(raw):
        next_open = raw.find("<div", pos)
        next_close = raw.find("</div>", pos)
        if next_close == -1:
            break
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            if depth == 0:
                body_content_end = next_close
            pos = next_close + 6

    body_html = raw[body_content_start:body_content_end].strip()

    # Process sym: syntax in the extracted pseudocode
    # (This is needed because the pseudocode is read from disk, bypassing
    # the normal hook processing order where symbols.py would process it)
    if symbols_hook is not None:
        body_html = symbols_hook.process_symbols_in_text(body_html, "framework-architecture/")

    # Now inject `algo-linked` class + `data-mapping-ids` attribute on mapped lines.
    # We process each <div class="algo-line ..."> and <div class="algo-math-block">
    # and assign line numbers using the same counter logic the CSS uses.
    line_counter = 0
    result_parts = []

    # Split on div boundaries.  Each element is either an algo-line or algo-math-block div.
    # We use a regex to find each top-level div element.
    div_pattern = re.compile(
        r'(<div\s+class="(algo-line[^"]*|algo-math-block[^"]*)")(>)',
        re.DOTALL,
    )

    last_end = 0
    # Collect all math symbol IDs for math-block lines
    math_symbol_ids = [entry["id"] for entry in math_symbol_mappings]

    for m in div_pattern.finditer(body_html):
        # Emit any text between matches (whitespace/newlines)
        result_parts.append(body_html[last_end:m.start()])

        classes_str = m.group(2)
        is_no_number = "no-number" in classes_str
        is_math_block = "algo-math-block" in classes_str

        if not is_no_number:
            line_counter += 1

        # Check if this line has a mapping
        mapping_ids = []
        if not is_no_number and line_counter in line_to_mappings:
            for entry in line_to_mappings[line_counter]:
                mapping_ids.append(entry["id"])

        if mapping_ids:
            # Add algo-linked class and data attribute
            new_classes = classes_str.rstrip() + " algo-linked"
            data_attr = f' data-mapping-ids="{",".join(mapping_ids)}"'
            # For math blocks, also attach math symbol IDs
            if is_math_block and math_symbol_ids:
                data_attr += f' data-math-symbol-ids="{",".join(math_symbol_ids)}"'
            result_parts.append(f'<div class="{new_classes}"{data_attr}>')
        else:
            result_parts.append(m.group(0))

        last_end = m.end()

    result_parts.append(body_html[last_end:])

    return "".join(result_parts)


def _generate_popup_data(mappings: List[dict], math_symbol_mappings: List[dict], page_url: str) -> str:
    """Generate hidden data elements that the JS popup reads from."""
    import html as html_mod
    
    items = []
    for entry in mappings:
        mapping_id = entry["id"]
        label = html_mod.escape(entry["label"])
        
        # Build implementation links as HTML
        impl_links = []
        for impl in entry.get("implementations", []):
            module_path = impl["module"]
            class_name = impl["class"]
            method_name = impl["method"]
            
            url = _resolve_api_url_html(module_path, class_name, method_name, page_url)
            display = f"{class_name}.{method_name}()"
            
            impl_links.append(
                f'<a href="{url}" class="impl-popup-link" '
                f'title="{html_mod.escape(module_path)}.{html_mod.escape(class_name)}.{html_mod.escape(method_name)}">'
                f'<code>{html_mod.escape(display)}</code>'
                f'</a>'
            )
        
        items.append(
            f'<div class="impl-data" data-mapping-id="{mapping_id}" '
            f'data-label="{label}" hidden>{"\n".join(impl_links)}</div>'
        )

    # Generate math symbol popup data
    for entry in math_symbol_mappings:
        symbol_id = entry["id"]
        label = html_mod.escape(entry["label"])
        symbol_latex = html_mod.escape(entry.get("symbol_latex", ""))

        impl_links = []
        for impl in entry.get("implementations", []):
            module_path = impl["module"]
            class_name = impl["class"]
            method_name = impl["method"]

            url = _resolve_api_url_html(module_path, class_name, method_name, page_url)
            display = f"{class_name}.{method_name}()"

            impl_links.append(
                f'<a href="{url}" class="impl-popup-link" '
                f'title="{html_mod.escape(module_path)}.{html_mod.escape(class_name)}.{html_mod.escape(method_name)}">'
                f'<code>{html_mod.escape(display)}</code>'
                f'</a>'
            )

        items.append(
            f'<div class="impl-data" data-mapping-id="{symbol_id}" '
            f'data-label="{label}" data-symbol-latex="{symbol_latex}" '
            f'hidden>{"\n".join(impl_links)}</div>'
        )
    
    return "\n".join(items)


# ─── Back-references ─────────────────────────────────────────────────────────

def _inject_back_references(markdown: str, page_url: str) -> str:
    """Inject pseudocode back-reference notes into API method documentation."""
    
    # Determine which module this page documents
    # API pages are at URL: api/Distributed_Design_Optimizer/coordination/Coordinator/
    # (MkDocs renders Coordinator.md as Coordinator/index.html)
    if not page_url.startswith("api/"):
        return markdown
    
    # Strip "api/" prefix and trailing slash
    rel_path = page_url[4:].rstrip("/")
    if rel_path.endswith("/index") or rel_path == "":
        return markdown  # Skip index pages
    
    # Skip source pages
    if "_source" in rel_path:
        return markdown

    # Inject a subtle inline back-reference INSIDE the method's collapsible content
    for method_key, algo_entries in _method_to_mappings.items():
        parts = method_key.rsplit(".", 2)
        if len(parts) != 3:
            continue
        module_path, _class_name, method_name = parts[0], parts[1], parts[2]
        
        # Convert module path to expected page path
        # e.g. Distributed_Design_Optimizer.coordination.Coordinator ->
        #      Distributed_Design_Optimizer/coordination/Coordinator
        expected_page = module_path.replace(".", "/")
        
        if rel_path != expected_page:
            continue
        
        # Find the method in the markdown (look for the admonition pattern)
        # Pattern: ??? abstract "method_name(...) → ..." followed by newline
        # The full line looks like: ??? abstract "run(self) → None"
        # Note: [^"]* matches everything inside the quotes (params, return type)
        pattern = re.compile(
            rf'(\?\?\? abstract "{re.escape(method_name)}\([^"]*")\n',
        )
        
        match = pattern.search(markdown)
        if match:
            # Build back-reference text, grouped by algorithm
            algo_refs = defaultdict(list)
            for algo_id, entry in algo_entries:
                algo_lines = entry.get("algo_lines", [])
                lines_str = ", ".join(str(ln) for ln in algo_lines)
                label = entry["label"]
                algo_refs[algo_id].append(f"*{label}* (Line{'s' if len(algo_lines) > 1 else ''} {lines_str})")
            
            # Calculate relative path from the .md file's directory to the target pages.
            url_segments = [s for s in page_url.rstrip("/").split("/") if s]
            dir_depth = len(url_segments) - 1
            prefix = "../" * dir_depth if dir_depth else ""
            
            # Build refs text with links to each algorithm's traceability page
            refs_parts = []
            for algo_id, refs in algo_refs.items():
                algo_config = _algorithm_data.get(algo_id, {}).get("config")
                if algo_config:
                    trace_url = f"{prefix}{algo_config.traceability_url}"
                    algo_name = algo_config.caption.split("(")[0].strip()  # Get short name
                    refs_text = ", ".join(refs)
                    refs_parts.append(f"{refs_text} → [{algo_name}]({trace_url})")
                else:
                    refs_parts.append(", ".join(refs))
            
            full_refs_text = "; ".join(refs_parts)
            
            # Insert a subtle reference line as first content INSIDE the method admonition
            # Must be indented with 4 spaces to be inside the ??? block
            back_ref_line = (
                f'    <small>📐 **Pseudocode:** {full_refs_text}</small>\n\n'
            )
            
            # Insert after the admonition header line
            insert_pos = match.end()
            markdown = markdown[:insert_pos] + back_ref_line + markdown[insert_pos:]
        else:
            log.warning("Pseudocode backref: method '%s' not found in page %s", method_name, page_url)
    
    return markdown
