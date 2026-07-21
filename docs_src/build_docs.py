#!/usr/bin/env python3
"""
Build and preview MkDocs documentation locally.

Usage:
    python build_docs.py
"""

import os
import sys
import subprocess
import shutil
import time
import threading
import re
from pathlib import Path

try:
   import yaml
except ImportError:
    yaml = None  # yaml not required for nav update functionality


def print_header(text):
    print("========================================")
    print(text)
    print("========================================")
    print()

def print_step(step, text):
    print(f"[{step}] {text}")

def print_warning(text):
    print(f"  WARNING: {text}")

def print_success(text):
    print(text)

def print_error(text):
    print(text)


def generate_section_index(folder_path: Path, folder_name: str, parent_name: str = None) -> str:
    """
    Generate an index.md content for a documentation section.
    Lists all subdirectories as links.
    
    Args:
        folder_path: Path to the folder
        folder_name: Display name for the section
        parent_name: Name of the parent folder (for back link)
    
    Returns:
        Markdown content for the index page
    """
    # Collect subdirectories that contain .md files
    subfolders = []
    for item in sorted(folder_path.iterdir()):
        if item.is_dir() and not item.name.startswith(('.', '_')):
            # Check if subfolder has any .md files
            if any(item.rglob("*.md")):
                subfolders.append(item.name)
    
    # Build markdown content
    # Convert folder name to title (replace - and _ with spaces, title case)
    title = folder_name.replace('-', ' ').replace('_', ' ').title()
    
    md = f"---\ntitle: {title}\n---\n\n"
    
    # Add back link for middle-level directories
    if parent_name:
        parent_title = parent_name.replace('-', ' ').replace('_', ' ').title()
        md += f"← Back to [{parent_title}](../index.md)\n\n"
    
    md += f"# {title}\n\n"
    
    if subfolders:
        md += "## Contents\n\n"
        for subfolder in subfolders:
            # Convert subfolder name to display name
            display_name = subfolder.replace('-', ' ').replace('_', ' ').title()
            md += f"- [{display_name}]({subfolder}/index.md)\n"
    
    return md


def update_section_indices(folder_path: Path, exclude_sections: list = None, parent_name: str = None):
    """
    Recursively update index.md files for documentation sections that have subdirectories.
    Only generates index files for folders with subdirectories.
    Works at any nesting level.
    
    Args:
        folder_path: Path to the folder to process
        exclude_sections: List of section names to exclude (e.g., ['api'])
        parent_name: Name of the parent folder (for back links in middle-level dirs)
    """
    if exclude_sections is None:
        exclude_sections = ['api', 'stylesheets']
    
    for item in folder_path.iterdir():
        if not item.is_dir():
            continue
        if item.name.startswith(('.', '_')):
            continue
        if item.name in exclude_sections:
            continue
        
        # Check if this folder has subdirectories with .md files
        subdirs_with_content = []
        for subitem in item.iterdir():
            if subitem.is_dir() and not subitem.name.startswith(('.', '_')):
                if any(subitem.rglob("*.md")):
                    subdirs_with_content.append(subitem)
        
        # Only generate index if there are subdirectories with content
        if subdirs_with_content:
            index_content = generate_section_index(item, item.name, parent_name)
            index_path = item / "index.md"
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)
            
            # Recursively process subdirectories (pass current folder name as parent)
            update_section_indices(item, exclude_sections=[], parent_name=item.name)


def clean_generated_indices(folder_path: Path, exclude_sections: list = None):
    """
    Remove index.md files from directories that have subdirectories (will be regenerated).
    Preserves index.md in directories without subdirectories (manually written).
    
    Args:
        folder_path: Path to the folder to process
        exclude_sections: List of section names to exclude (e.g., ['api'])
    """
    if exclude_sections is None:
        exclude_sections = ['api', 'stylesheets']
    
    for item in folder_path.iterdir():
        if not item.is_dir():
            continue
        if item.name.startswith(('.', '_')):
            continue
        if item.name in exclude_sections:
            continue
        
        # Check if this folder has subdirectories with .md files
        has_subdirs_with_content = False
        for subitem in item.iterdir():
            if subitem.is_dir() and not subitem.name.startswith(('.', '_')):
                if any(subitem.rglob("*.md")):
                    has_subdirs_with_content = True
                    break
        
        # Only remove index.md if there are subdirectories (will be regenerated)
        if has_subdirs_with_content:
            index_path = item / "index.md"
            if index_path.exists():
                index_path.unlink()
            
            # Recursively clean subdirectories
            clean_generated_indices(item, exclude_sections=[])


def generate_api_nav_recursive(folder_path: Path, base_path: Path, prefix: str = "") -> list:
    """
    Recursively generate navigation structure for API documentation.
    
    Args:
        folder_path: Current folder to process
        base_path: Base path for relative path calculation (content/ folder)
        prefix: Path prefix for nav entries (e.g., "api/")
    
    Returns:
        List of nav entries for this folder and its subfolders
    """
    nav_items = []
    
    # Calculate relative path from content/ folder
    try:
        rel_path = folder_path.relative_to(base_path)
        current_prefix = str(rel_path).replace('\\', '/') + '/'
    except ValueError:
        current_prefix = prefix
    
    # Check for index.md in this folder
    index_file = folder_path / "index.md"
    has_index = index_file.exists()
    
    # Collect subfolders and .md files
    subfolders = []
    md_files = []
    
    for item in sorted(folder_path.iterdir()):
        if item.is_dir() and not item.name.startswith(('.', '_')):
            # Check if subfolder has any .md files
            if any(item.rglob("*.md")):
                subfolders.append(item)
        elif item.is_file() and item.suffix == '.md' and item.name != 'index.md':
            md_files.append(item)
    
    # If this folder has content (index, subfolders, or md files), build the nav structure
    if has_index or subfolders or md_files:
        # Add index.md first if it exists
        if has_index:
            nav_items.append(f"{current_prefix}index.md")
        
        # Add subfolders recursively
        for subfolder in subfolders:
            subfolder_nav = generate_api_nav_recursive(subfolder, base_path, current_prefix)
            if subfolder_nav:
                # Create a nested structure with folder name as key
                nav_items.append({subfolder.name: subfolder_nav})
        
        # Add individual .md files
        for md_file in md_files:
            file_path = f"{current_prefix}{md_file.name}"
            # Use filename without extension as display name
            display_name = md_file.stem
            nav_items.append({display_name: file_path})
    
    return nav_items


def update_mkdocs_nav(docs_dir: Path):
    """
    Update mkdocs.yml with dynamically generated API Reference navigation.
    
    This function scans the actual content/api/ directory and updates the
    nav section to only include entries for documentation files that exist.
    It removes entries for deleted packages and adds entries for new ones.
    
    Uses string manipulation to preserve special YAML tags like !!python/name:
    that standard YAML libraries cannot handle.
    """
    mkdocs_path = docs_dir / "mkdocs.yml"
    content_path = docs_dir / "content"
    api_path = content_path / "api"
    
    if not mkdocs_path.exists():
        print_warning("mkdocs.yml not found")
        return
    
    if not api_path.exists():
        print_warning("content/api/ directory not found")
        return
    
    # Read existing mkdocs.yml as text (preserves !!python/name: tags)
    with open(mkdocs_path, 'r', encoding='utf-8') as f:
        mkdocs_content = f.read()
    
    # Generate nav entries for Distributed_Design_Optimizer
    ddo_path = api_path / "Distributed_Design_Optimizer"
    ddo_nav = []
    if ddo_path.exists():
        ddo_nav = generate_api_nav_recursive(ddo_path, content_path)
    
    # Generate nav entries for userfiles
    userfiles_path = api_path / "userfiles"
    userfiles_nav = []
    if userfiles_path.exists():
        userfiles_nav = generate_api_nav_recursive(userfiles_path, content_path)
    
    # Build the complete API Reference nav section as YAML text
    api_nav_lines = ["- API Reference:"]
    
    # Add api/index.md if it exists
    if (api_path / "index.md").exists():
        api_nav_lines.append("  - api/index.md")
    
    # Add Distributed_Design_Optimizer section
    if ddo_nav:
        api_nav_lines.append("  - Distributed_Design_Optimizer:")
        api_nav_lines.extend(_nav_to_yaml_lines(ddo_nav, indent=4))
    
    # Add userfiles section
    if userfiles_nav:
        api_nav_lines.append("  - userfiles:")
        api_nav_lines.extend(_nav_to_yaml_lines(userfiles_nav, indent=4))
    
    new_api_section = "\n".join(api_nav_lines)
    
    # Find and replace the API Reference section in mkdocs.yml
    # Pattern: "- API Reference:" followed by all indented content until next top-level nav item
    
    # Match "- API Reference:" and everything until the next "- " at the same indentation level
    # or end of nav section (next top-level key like "extra_css:")
    pattern = r'(- API Reference:\n(?:[ ]{2,}.*\n)*)'
    
    match = re.search(pattern, mkdocs_content)
    if match:
        # Replace the matched section
        mkdocs_content = mkdocs_content[:match.start()] + new_api_section + "\n" + mkdocs_content[match.end():]
        
        # Write updated content
        with open(mkdocs_path, 'w', encoding='utf-8') as f:
            f.write(mkdocs_content)
        
        print(f"  Updated API Reference nav ({_count_nav_entries(ddo_nav)} DDO entries, {_count_nav_entries(userfiles_nav)} userfiles entries)")
    else:
        print_warning("Could not find 'API Reference' section in mkdocs.yml nav")


def _nav_to_yaml_lines(nav_items: list, indent: int = 0) -> list:
    """
    Convert a nav structure to YAML lines with proper indentation.
    
    Args:
        nav_items: List of nav entries (strings or dicts)
        indent: Current indentation level in spaces
    
    Returns:
        List of YAML lines
    """
    lines = []
    indent_str = " " * indent
    
    for item in nav_items:
        if isinstance(item, str):
            # Simple path entry
            lines.append(f"{indent_str}- {item}")
        elif isinstance(item, dict):
            # Entry with display name or nested section
            for key, value in item.items():
                if isinstance(value, str):
                    # Display name: path
                    lines.append(f"{indent_str}- {key}: {value}")
                elif isinstance(value, list):
                    # Nested section
                    lines.append(f"{indent_str}- {key}:")
                    lines.extend(_nav_to_yaml_lines(value, indent + 2))
    
    return lines


def _count_nav_entries(nav_items: list) -> int:
    """Count total number of file entries in a nav structure."""
    count = 0
    for item in nav_items:
        if isinstance(item, str):
            count += 1
        elif isinstance(item, dict):
            for value in item.values():
                if isinstance(value, str):
                    count += 1
                elif isinstance(value, list):
                    count += _count_nav_entries(value)
    return count


def run_content_diagram_generators(docs_dir: Path) -> None:
    """Discover and run generate_diagram.py scripts in content subfolders.

    Convention: any content subfolder may contain a ``generate_diagram.py``
    that exposes a ``generate(docs_dir: Path) -> None`` function.  This
    allows each documentation section to own its diagram-generation logic
    while build_docs.py handles orchestration.
    """
    import importlib.util

    content_dir = docs_dir / "content"
    for script in sorted(content_dir.rglob("generate_diagram.py")):
        module_name = script.stem
        try:
            spec = importlib.util.spec_from_file_location(module_name, script)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "generate"):
                mod.generate(docs_dir)
            else:
                print_warning(f"{script} has no generate() function. Skipping.")
        except Exception as e:
            print_warning(f"Failed to run {script}: {e}")


def validate_bib_file(docs_dir: Path) -> list[str]:
    """Validate the cleaned .bib file with pybtex and return a list of issues.

    Uses pybtex in non-strict mode so that all problems are collected
    rather than aborting on the first one.  Results are written to
    ``bib_syntax_report.txt``.
    """
    import io
    import contextlib
    import warnings

    bib_path = docs_dir / "content" / "includes" / "Ellmaier_Group_clean.bib"
    if not bib_path.exists():
        return ["Ellmaier_Group_clean.bib not found. Run diagram generators first."]

    try:
        import pybtex.errors
        from pybtex.database.input.bibtex import Parser
    except ImportError:
        return ["pybtex not installed. Cannot validate .bib file."]

    issues: list[str] = []
    original_report = pybtex.errors.report_error

    def _collect(exception):
        issues.append(str(exception))

    # pybtex.database imports report_error at module level, so we must
    # patch it there too, not just in pybtex.errors.
    import pybtex.database
    original_db_report = getattr(pybtex.database, "report_error", None)

    try:
        pybtex.errors.set_strict_mode(False)
        pybtex.errors.report_error = _collect
        pybtex.database.report_error = _collect
        parser = Parser()
        # Suppress pybtex's own stderr warnings and Python warnings
        with contextlib.redirect_stderr(io.StringIO()), warnings.catch_warnings():
            warnings.simplefilter("ignore")
            parser.parse_file(str(bib_path))
    except Exception as exc:
        issues.append(f"Fatal parse error: {exc}")
    finally:
        pybtex.errors.report_error = original_report
        if original_db_report is not None:
            pybtex.database.report_error = original_db_report

    # Write report file
    report_path = docs_dir / "bib_syntax_report.txt"
    with open(report_path, "w", encoding="utf-8") as fh:
        fh.write(f"BibTeX Syntax Report  ({bib_path.name})\n")
        fh.write("=" * 60 + "\n\n")
        fh.write(f"Source file : {bib_path.relative_to(docs_dir)}\n")
        fh.write(f"Total issues: {len(issues)}\n\n")
        if issues:
            for i, issue in enumerate(issues, 1):
                fh.write(f"  {i}. {issue}\n")
        else:
            fh.write("No issues found.\n")

    return issues


class ProgressIndicator:
    """Simple spinning progress indicator."""
    
    def __init__(self, message=""):
        self.message = message
        self.running = False
        self.thread = None
        
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.start()
        
    def _spin(self):
        # Use ASCII characters for Windows compatibility
        spinner = ['|', '/', '-', '\\']
        idx = 0
        while self.running:
            print(f"\r  {spinner[idx]} {self.message}", end='', flush=True)
            idx = (idx + 1) % len(spinner)
            time.sleep(0.2)
            
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        # Clear the spinner line completely
        print(f"\r{' ' * (len(self.message) + 10)}\r", end='', flush=True)


def main(serve=True):
    # Change to docs directory
    docs_dir = Path(__file__).parent.resolve()
    os.chdir(docs_dir)
    
    # Add docs_src to sys.path so scripts can be imported directly
    if str(docs_dir) not in sys.path:
        sys.path.insert(0, str(docs_dir))
    
    print_header("MkDocs Documentation Build & Preview")
    
    # === STEP 1: Create directories ===
    print_step("1/9", "Creating directories...")
    
    directories = [
        "content/api",
        "content/stylesheets",
        "content/javascripts",
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    # Note: custom.css lives directly in content/stylesheets/ (no copy needed)
    # Note: MkDocs Material has native Mermaid support, no custom JS needed
    
    # === STEP 1b: Ensure pandoc is available ===
    try:
        import pypandoc
        pypandoc.get_pandoc_version()
    except (ImportError, OSError):
        print("  pandoc not found, downloading...")
        try:
            import pypandoc
            pypandoc.download_pandoc()
            print("  pandoc downloaded successfully.")
        except Exception as e:
            print_warning(f"Could not download pandoc: {e}")
            print_warning("Citations hook will not work. Install pandoc manually or pip install pypandoc_binary.")
    
    # === STEP 2: Clean and generate section index pages ===
    print_step("2/9", "Generating section index pages...")
    
    content_path = docs_dir / "content"
    try:
        # First, clean old generated index.md files (only in dirs with subdirs)
        clean_generated_indices(content_path, exclude_sections=['api', 'stylesheets', 'framework-architecture', 'includes', 'tutorial', 'examples', 'distributed-optimization-for-multidisciplinary-design'])
        # Then generate fresh index.md files
        update_section_indices(content_path, exclude_sections=['api', 'stylesheets', 'framework-architecture', 'includes', 'tutorial', 'examples', 'distributed-optimization-for-multidisciplinary-design'])
    except Exception as e:
        print_warning(f"Failed to generate section indices: {e}")

    # Run per-section diagram generators (e.g. framework-architecture/generate_diagram.py)
    try:
        run_content_diagram_generators(docs_dir)
    except Exception as e:
        print_warning(f"Failed running content diagram generators: {e}")
    
    # === STEP 3: Validate .bib file ===
    print_step("3/9", "Validating BibTeX file...")
    
    bib_clean = docs_dir / "content" / "includes" / "Ellmaier_Group_clean.bib"
    if bib_clean.exists():
        bib_issues = validate_bib_file(docs_dir)
        report_path = docs_dir / "bib_syntax_report.txt"
        if bib_issues:
            print_warning(f"{len(bib_issues)} issue(s) found in .bib file.")
            print(f"  Report: {report_path}")
            print(f"  Please fix these in content/includes/Ellmaier_Group.bib and rebuild.")
        else:
            print("  .bib file is valid.")
    else:
        print_warning("Ellmaier_Group_clean.bib not found. Skipping validation.")
    
    # === STEP 4: Generate interactive Mermaid UML diagrams ===
    print_step("4/9", "Generating interactive Mermaid UML diagrams...")
    
    try:
        from scripts.generate_uml import main as generate_uml
        generate_uml()
    except ImportError:
        print_warning("generate_uml.py not found. Skipping.")
    except Exception as e:
        print_warning(f"Failed to generate Mermaid diagrams: {e}")
    
    # === STEP 5: Generate API docs (embeds Mermaid diagrams with clickable links) ===
    print_step("5/9", "Generating API documentation...")
    
    try:
        from scripts.generate_api_docs import main as generate_api_docs, CLASS_REGISTRY
        generate_api_docs()
        # Point user to the syntax report
        report_path = docs_dir / "syntax_report.txt"
        if report_path.exists():
            print(f"  Syntax report: {report_path}")
    except ImportError:
        print_warning("generate_api_docs.py not found. Skipping.")
    except Exception as e:
        print_warning(f"Failed to generate API docs: {e}")
    
    # === STEP 6: Update navigation for API Reference ===
    print_step("6/9", "Updating API Reference navigation...")
    
    try:
        update_mkdocs_nav(docs_dir)
    except Exception as e:
        print_warning(f"Failed to update navigation: {e}")
    
    # === STEP 7: Check mkdocs ===
    print_step("7/9", "Checking MkDocs installation...")
    
    # Check if mkdocs is available
    try:
        from mkdocs.config import load_config
        from mkdocs.commands.build import build as mkdocs_build
    except ImportError:
        print()
        print_error("ERROR: MkDocs not found in current Python environment.")
        print()
        print("Please install:")
        print("  pip install mkdocs mkdocs-material")
        print()
        print(f"Current Python: {sys.executable}")
        sys.exit(1)
    
    # === STEP 7b: Copy each example's drawio HTML next to its docs page ===
    # Single source of truth stays in /userfiles. At build time the diagrams
    # are copied into the matching content/examples/<UseCase>/ folder (a
    # git-ignored build artifact) so MkDocs can serve them for the example
    # pages' iframes. Only use cases that have an examples page are copied.
    userfiles_src = docs_dir.parent / "userfiles"
    examples_dir = docs_dir / "content" / "examples"
    if userfiles_src.is_dir() and examples_dir.is_dir():
        copied = 0
        for example_folder in sorted(examples_dir.iterdir()):
            if not example_folder.is_dir():
                continue
            src_folder = userfiles_src / example_folder.name
            if not src_folder.is_dir():
                continue
            for f in src_folder.glob("*.drawio.html"):
                shutil.copy2(f, example_folder / f.name)
                copied += 1
        if copied:
            print(f"  Copied {copied} drawio HTML file(s) from userfiles/ into content/examples/")

    # === STEP 8: Build static site ===
    print_step("8/9", "Building static site...")
    print("  (This may take a minute for large documentation sites...)")
    
    try:
        cfg = load_config(str(docs_dir / "mkdocs.yml"))
        mkdocs_build(cfg)
        print("  Build completed successfully!")
        # Create .nojekyll file for GitHub Pages (disables Jekyll processing)
        nojekyll_path = docs_dir.parent / "docs" / ".nojekyll"
        nojekyll_path.touch()
    except Exception as e:
        print_warning(f"Build failed: {e}")

    # === STEP 9: Serve locally ===
    if not serve:
        print_success("Build-only mode: skipping local server.")
        return

    print_step("9/9", "Starting local server...")
    print("Press Ctrl+C to stop")
    print()
    
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "mkdocs", "serve"],
            stderr=subprocess.STDOUT,
        )
        process.wait()
        
    except KeyboardInterrupt:
        print()
        print_success("Server stopped.")
    except Exception as e:
        print_error(f"MkDocs serve failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build and preview MkDocs documentation.")
    parser.add_argument("--no-serve", action="store_true", help="Build the site but do not start the local server (for CI).")
    args = parser.parse_args()
    main(serve=not args.no_serve)
