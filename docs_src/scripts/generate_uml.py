#!/usr/bin/env python3
"""
Generate interactive Mermaid UML class diagrams from Python source code.

This script recursively processes:
- Distributed_Design_Optimizer/ - Core package modules
- userfiles/ - User example files and configurations

For each folder, it generates a Mermaid class diagram showing:
- Classes defined in Python files
- Inheritance relationships
- Key methods and attributes
- CLICKABLE LINKS to class documentation pages

The generated diagrams are embedded directly in markdown files for
client-side rendering with full interactivity.
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


# Configuration
SCRIPT_DIR = Path(__file__).parent
DOCS_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = DOCS_DIR.parent

# Output directory for Mermaid files (alongside API docs)
MERMAID_OUTPUT_BASE = DOCS_DIR / "content" / "api"

# Marker comment to indicate a file should not be overwritten
# Add this as the first line of a .mmd file to preserve manual edits
CUSTOM_MARKER = "%% @custom"


class ClassInfo:
    """Store information about a Python class."""
    
    def __init__(self, name: str, bases: List[str], methods: List[str], 
                 attributes: List[str], is_abstract: bool = False,
                 source_file: str = "", doc_path: str = ""):
        self.name = name
        self.bases = bases
        self.methods = methods
        self.attributes = attributes
        self.is_abstract = is_abstract
        self.source_file = source_file  # For generating doc links
        self.doc_path = doc_path  # Full documentation path relative to api/


# Global registry of all classes in the project
# Maps class name -> relative doc path from api/ folder
GLOBAL_CLASS_REGISTRY: Dict[str, str] = {}


class PythonClassExtractor(ast.NodeVisitor):
    """Extract class information from Python AST."""
    
    def __init__(self, source_file: str = ""):
        self.classes: List[ClassInfo] = []
        self.source_file = source_file
        
    def _extract_init_attributes(self, init_node: ast.FunctionDef) -> List[Tuple[str, bool]]:
        """Extract instance attributes from __init__ method (self.attr = ...).
        
        Returns:
            List of tuples (attr_name, is_private) where is_private indicates
            if the attribute starts with underscore.
        """
        attributes = []
        seen_names = set()
        for stmt in ast.walk(init_node):
            if isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    # Look for self.attribute = value patterns
                    if isinstance(target, ast.Attribute):
                        if isinstance(target.value, ast.Name) and target.value.id == 'self':
                            attr_name = target.attr
                            # Skip dunder attributes (e.g., __dict__)
                            if attr_name.startswith('__') and attr_name.endswith('__'):
                                continue
                            if attr_name not in seen_names:
                                seen_names.add(attr_name)
                                is_private = attr_name.startswith('_')
                                attributes.append((attr_name, is_private))
            # Handle AugAssign (self.attr += value, etc.)
            elif isinstance(stmt, ast.AugAssign):
                if isinstance(stmt.target, ast.Attribute):
                    if isinstance(stmt.target.value, ast.Name) and stmt.target.value.id == 'self':
                        attr_name = stmt.target.attr
                        if attr_name.startswith('__') and attr_name.endswith('__'):
                            continue
                        if attr_name not in seen_names:
                            seen_names.add(attr_name)
                            is_private = attr_name.startswith('_')
                            attributes.append((attr_name, is_private))
            # Handle AnnAssign (self.attr: type = value) - type-annotated assignments
            elif isinstance(stmt, ast.AnnAssign):
                if isinstance(stmt.target, ast.Attribute):
                    if isinstance(stmt.target.value, ast.Name) and stmt.target.value.id == 'self':
                        attr_name = stmt.target.attr
                        if attr_name.startswith('__') and attr_name.endswith('__'):
                            continue
                        if attr_name not in seen_names:
                            seen_names.add(attr_name)
                            is_private = attr_name.startswith('_')
                            attributes.append((attr_name, is_private))
        return attributes
        
    def visit_ClassDef(self, node: ast.ClassDef):
        # Get base classes
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(f"{self._get_attr_name(base)}")
        
        # Get methods (public ones, limit to key methods)
        methods = []
        attributes = []  # List of tuples: (attr_name, is_private)
        is_abstract = False
        init_node = None
        seen_attr_names = set()
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                # Check for abstract methods
                for decorator in item.decorator_list:
                    if isinstance(decorator, ast.Name) and decorator.id == 'abstractmethod':
                        is_abstract = True
                
                # Capture __init__ for attribute extraction
                if item.name == '__init__':
                    init_node = item
                
                # Only include public methods and __init__
                if not item.name.startswith('_') or item.name == '__init__':
                    # Simplify method signature for cleaner diagrams
                    args = [arg.arg for arg in item.args.args if arg.arg != 'self']
                    if len(args) > 2:
                        args = args[:2] + ['...']
                    # Escape special characters for Mermaid
                    method_sig = f"{item.name}({', '.join(args)})"
                    methods.append(method_sig)
                    
            elif isinstance(item, ast.Assign):
                # Class-level attributes (public only at class level)
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attr_name = target.id
                        # Skip dunder attributes
                        if attr_name.startswith('__') and attr_name.endswith('__'):
                            continue
                        if attr_name not in seen_attr_names:
                            seen_attr_names.add(attr_name)
                            is_private = attr_name.startswith('_')
                            attributes.append((attr_name, is_private))
        
        # Extract instance attributes from __init__ method
        if init_node:
            init_attributes = self._extract_init_attributes(init_node)
            # Add to attributes list, avoiding duplicates
            for attr_name, is_private in init_attributes:
                if attr_name not in seen_attr_names:
                    seen_attr_names.add(attr_name)
                    attributes.append((attr_name, is_private))
        
        # Limit methods to avoid cluttered diagrams
        if len(methods) > 6:
            methods = methods[:5] + ['...']
        if len(attributes) > 8:
            attributes = attributes[:7] + [('...', False)]
            
        self.classes.append(ClassInfo(
            name=node.name,
            bases=bases,
            methods=methods,
            attributes=attributes,
            is_abstract=is_abstract or 'ABC' in bases or 'Interface' in node.name,
            source_file=self.source_file
        ))
        
    def _get_attr_name(self, node: ast.Attribute) -> str:
        """Get full attribute name like 'module.Class'."""
        if isinstance(node.value, ast.Name):
            return f"{node.value.id}.{node.attr}"
        return node.attr


def extract_classes_from_file(file_path: Path) -> List[ClassInfo]:
    """Extract class information from a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            source = f.read()
        tree = ast.parse(source)
        extractor = PythonClassExtractor(source_file=file_path.stem)
        extractor.visit(tree)
        return extractor.classes
    except SyntaxError:
        return []
    except Exception as e:
        return []


def sanitize_mermaid_string(s: str) -> str:
    """Sanitize strings for use in Mermaid diagrams."""
    # Replace characters that might break Mermaid syntax
    s = s.replace('"', "'")
    s = s.replace('<', '~')
    s = s.replace('>', '~')
    s = s.replace('{', '(')
    s = s.replace('}', ')')
    return s


def build_global_class_registry(source_folder: Path, api_base_path: str = "") -> None:
    """
    Recursively scan source folder and build a global registry of all classes.
    
    This registry maps class names to their documentation paths, allowing
    proper cross-referencing between packages in UML diagrams.
    
    Args:
        source_folder: Root source folder to scan (e.g., Distributed_Design_Optimizer)
        api_base_path: Base path in the API docs (e.g., "Distributed_Design_Optimizer")
    """
    global GLOBAL_CLASS_REGISTRY
    
    skip_folders = {'__pycache__', '.git', '.venv', 'venv', 'build', 'dist', 
                    '.egg-info', 'node_modules', '.idea', '.vscode'}
    
    if source_folder.name in skip_folders or source_folder.name.startswith('.'):
        return
    
    # Current path in the API docs
    current_api_path = api_base_path
    
    # Scan Python files in this folder
    for py_file in source_folder.glob("*.py"):
        if py_file.name.startswith('__'):
            continue
        classes = extract_classes_from_file(py_file)
        for cls in classes:
            # Build the doc path: e.g., "Distributed_Design_Optimizer/coordination/convergence/ConvergenceIndicatorInterface"
            doc_path = f"{current_api_path}/{py_file.stem}" if current_api_path else py_file.stem
            GLOBAL_CLASS_REGISTRY[cls.name] = doc_path
    
    # Recursively scan subfolders
    for item in source_folder.iterdir():
        if item.is_dir() and item.name not in skip_folders and not item.name.startswith('.'):
            sub_api_path = f"{current_api_path}/{item.name}" if current_api_path else item.name
            build_global_class_registry(item, sub_api_path)


def generate_mermaid_diagram(folder_name: str, classes: List[ClassInfo], 
                             subfolders: List[str], current_doc_path: str = "") -> str:
    """
    Generate Mermaid class diagram content with clickable links.
    
    Args:
        folder_name: Name of the folder being documented
        classes: List of ClassInfo objects for classes in this folder
        subfolders: List of subfolder names (sub-packages)
        current_doc_path: Current folder's path in the API docs (for relative link calculation)
    
    Returns:
        Mermaid diagram syntax as a string
    """
    
    lines = []
    lines.append("```mermaid")
    # Theme matching previous PlantUML color scheme:
    # - primaryColor (#e6f4f7): Class background - light cyan
    # - primaryBorderColor (#035970): Class border - dark teal  
    # - primaryTextColor (#000000): Text color - black
    # - lineColor (#035970): Arrows and lines - dark teal
    # - secondaryColor (#cce9ef): Class header background - slightly darker cyan
    # - tertiaryColor (#f5fafb): Package/namespace background - very light
    # - noteBkgColor (#e6f4f7): Note background - same as class
    # - noteBorderColor (#035970): Note border - same as class border
    lines.append("%%{init: {'theme': 'base', 'themeVariables': { " +
                 "'primaryColor': '#e6f4f7', " +
                 "'primaryBorderColor': '#035970', " +
                 "'primaryTextColor': '#000000', " +
                 "'lineColor': '#035970', " +
                 "'secondaryColor': '#cce9ef', " +
                 "'tertiaryColor': '#f5fafb', " +
                 "'noteBkgColor': '#e6f4f7', " +
                 "'noteBorderColor': '#035970', " +
                 "'fontFamily': 'Arial, sans-serif'" +
                 "}}}%%")
    lines.append("classDiagram")
    lines.append("    direction TB")
    lines.append("")
    
    # Track which classes are defined locally vs external bases
    local_class_names = {c.name for c in classes}
    
    # Separate base classes into categories:
    # - project_bases: classes defined elsewhere in the project (in GLOBAL_CLASS_REGISTRY)
    # - external_bases: truly external classes (not in project)
    project_bases = {}  # Maps base name to its doc path
    external_bases = set()
    
    # Collect and categorize base classes
    for cls in classes:
        for base in cls.bases:
            base_name = base.split('.')[-1]  # Handle module.Class format
            if base_name in local_class_names or base_name in ['object', 'ABC']:
                continue
            # Check if this class exists elsewhere in the project
            if base_name in GLOBAL_CLASS_REGISTRY:
                project_bases[base_name] = GLOBAL_CLASS_REGISTRY[base_name]
            else:
                external_bases.add(base_name)
    
    # Add sub-packages as folder/package symbols (before classes)
    # Using :::styleName syntax for inline styling
    if subfolders:
        lines.append("    %% Sub-packages (click to navigate)")
        for subfolder in sorted(subfolders):
            # Use a sanitized ID for the class (replace hyphens, etc.)
            subfolder_id = subfolder.replace('-', '_').replace('.', '_')
            # Simple representation with inline style
            lines.append(f"    class {subfolder_id}[\"{subfolder}/\"]:::packageStyle")
        lines.append("")
    
    # Define truly external base classes with special styling
    if external_bases:
        lines.append("    %% External classes (not in this project)")
        for base in sorted(external_bases):
            lines.append(f"    class {base}:::externalStyle {{")
            lines.append(f"        <<external>>")
            lines.append(f"    }}")
            lines.append("")
    
    # Define project base classes (from elsewhere in the project) - clickable with links
    if project_bases:
        lines.append("    %% Classes from other packages (clickable)")
        for base_name in sorted(project_bases.keys()):
            # Check if it's an abstract class (has Interface in name or in registry as abstract)
            is_abstract = 'Interface' in base_name or 'Basis' in base_name or 'ABC' in base_name
            style_name = "projectAbstractStyle" if is_abstract else "projectStyle"
            annotation = "<<abstract>>" if is_abstract else "<<project>>"
            lines.append(f"    class {base_name}:::{style_name} {{")
            lines.append(f"        {annotation}")
            lines.append(f"    }}")
            lines.append("")
    
    # Define local classes with their members (using :::styleName syntax)
    for cls in classes:
        # Determine style based on class type
        style_name = "abstractStyle" if cls.is_abstract else "localStyle"
        
        # Class definition with annotation and inline style
        if cls.is_abstract:
            lines.append(f"    class {cls.name}:::{style_name} {{")
            lines.append(f"        <<abstract>>")
        else:
            lines.append(f"    class {cls.name}:::{style_name} {{")
        
        # Add attributes with visibility (+ for public, - for private)
        for attr in cls.attributes:
            if isinstance(attr, tuple):
                attr_name, is_private = attr
                if attr_name == '...':
                    lines.append(f"        ...")
                else:
                    visibility = '-' if is_private else '+'
                    lines.append(f"        {visibility}{sanitize_mermaid_string(attr_name)}")
            else:
                # Backward compatibility: string format (assume public)
                if attr == '...':
                    lines.append(f"        ...")
                else:
                    lines.append(f"        +{sanitize_mermaid_string(attr)}")
        
        # Add methods with visibility
        for method in cls.methods:
            if method == '...':
                lines.append(f"        ...")
            else:
                sanitized = sanitize_mermaid_string(method)
                lines.append(f"        +{sanitized}")
        
        lines.append(f"    }}")
        lines.append("")
    
    # Add inheritance relationships
    for cls in classes:
        for base in cls.bases:
            base_name = base.split('.')[-1]
            if base_name not in ['object', 'ABC']:
                lines.append(f"    {base_name} <|-- {cls.name}")
    
    # Add blank line before click handlers
    lines.append("")
    lines.append("    %% Click handlers for navigation to documentation")
    
    # Add click handlers for sub-packages (folders)
    if subfolders:
        for subfolder in sorted(subfolders):
            subfolder_id = subfolder.replace('-', '_').replace('.', '_')
            # Link to the subfolder's index page
            doc_link = f"{subfolder}/"
            tooltip = f"Browse {subfolder} package"
            lines.append(f'    click {subfolder_id} href "{doc_link}" "{tooltip}"')
    
    # Add click handlers for project classes (from other packages)
    # Calculate relative path from current location to the class's documentation
    if project_bases and current_doc_path:
        for base_name, base_doc_path in sorted(project_bases.items()):
            # Calculate relative path from current_doc_path to base_doc_path
            # Both paths are relative to the api/ folder
            current_parts = current_doc_path.strip('/').split('/')
            base_parts = base_doc_path.strip('/').split('/')
            
            # Find common prefix
            common_length = 0
            for i in range(min(len(current_parts), len(base_parts))):
                if current_parts[i] == base_parts[i]:
                    common_length = i + 1
                else:
                    break
            
            # Build relative path: go up from current, then down to base
            up_count = len(current_parts) - common_length
            remaining_path = '/'.join(base_parts[common_length:])
            
            if up_count > 0:
                relative_path = '../' * up_count + remaining_path
            else:
                relative_path = remaining_path
            
            doc_link = f"{relative_path}/" if relative_path else "./"
            tooltip = f"View {base_name} documentation"
            lines.append(f'    click {base_name} href "{doc_link}" "{tooltip}"')
    
    # Add click handlers for each local class (links to documentation)
    # Mermaid syntax: click ClassName href "url" "tooltip"
    # MkDocs serves .md files as directories (e.g., Class.md -> Class/)
    if classes:
        for cls in classes:
            # Link to the class's documentation page (without .md extension)
            doc_link = f"{cls.source_file}/"
            tooltip = f"View {cls.name} documentation"
            lines.append(f'    click {cls.name} href "{doc_link}" "{tooltip}"')
    
    # Add custom styling definitions (classDef needed for :::styleName to work)
    lines.append("")
    lines.append("    %% Style definitions")
    # Sub-packages: light grey for folders
    lines.append("    classDef packageStyle fill:#e8e8e8,stroke:#999999,stroke-width:2px")
    # External base classes: light orange (truly external - not in project)
    lines.append("    classDef externalStyle fill:#fff8e6,stroke:#FFCC80,stroke-width:2px")
    # Project classes from other packages: same cyan as local classes
    lines.append("    classDef projectStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px")
    # Project abstract classes from other packages: same cyan with dashed border
    lines.append("    classDef projectAbstractStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px,stroke-dasharray:5 5")
    # Local classes: light cyan
    lines.append("    classDef localStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px")
    # Abstract classes: light cyan with dashed border
    lines.append("    classDef abstractStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px,stroke-dasharray:5 5")
    
    # Note: Styles are applied inline using :::styleName syntax in class definitions above
    # This is more reliable than the cssClass statement
    
    # If no classes and no subfolders, show informative note
    if not classes and not subfolders:
        lines.append('    note "No classes found in this module"')
    
    lines.append("```")
    
    return '\n'.join(lines)


def is_custom_mermaid(mmd_file: Path) -> bool:
    """
    Check if a .mmd file has the @custom marker indicating manual edits.
    
    Files with '%% @custom' as the first line will be preserved during regeneration.
    """
    if not mmd_file.exists():
        return False
    
    try:
        with open(mmd_file, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            return first_line == CUSTOM_MARKER or first_line.startswith("%% @custom")
    except Exception:
        return False


def save_mermaid_file(mermaid_content: str, output_file: Path) -> bool:
    """
    Save Mermaid diagram content to .mmd file.
    
    If the file already exists and has the @custom marker, it will NOT be overwritten.
    To mark a file as custom, add this as the first line:
        %% @custom
    
    Returns:
        True if file was written, False if preserved due to @custom marker
    """
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Use .mmd extension for Mermaid files
    mmd_file = output_file.with_suffix('.mmd')
    
    # Check if file has @custom marker - if so, preserve it
    if is_custom_mermaid(mmd_file):
        print(f"  PRESERVED (has @custom marker): {mmd_file}")
        return False
    
    # Save .mmd file
    with open(mmd_file, 'w', encoding='utf-8') as f:
        f.write(mermaid_content)
    
    return True


def process_folder_for_mermaid(source_folder: Path, output_folder: Path, 
                                api_path: str = "", processed: Optional[Set[str]] = None) -> bool:
    """
    Process a folder and generate Mermaid diagram for its contents.
    
    Args:
        source_folder: Source Python folder to scan
        output_folder: Output folder for generated .mmd files
        api_path: Current path in the API docs (e.g., "Distributed_Design_Optimizer/coordination")
        processed: Set of already-processed folder paths (to avoid cycles)
    
    Returns True if a diagram was generated.
    """
    if processed is None:
        processed = set()
    
    folder_key = str(source_folder.resolve())
    if folder_key in processed:
        return False
    processed.add(folder_key)
    
    # Skip certain folders
    skip_folders = {'__pycache__', '.git', '.venv', 'venv', 'build', 'dist', 
                    '.egg-info', 'node_modules', '.idea', '.vscode'}
    
    if source_folder.name in skip_folders or source_folder.name.startswith('.'):
        return False
    
    # Collect classes from Python files in this folder
    all_classes: List[ClassInfo] = []
    has_python_files = False
    for py_file in sorted(source_folder.glob("*.py")):
        if py_file.name.startswith('__'):
            continue
        has_python_files = True
        classes = extract_classes_from_file(py_file)
        all_classes.extend(classes)
    
    # Collect subfolders
    subfolders = []
    for item in sorted(source_folder.iterdir()):
        if item.is_dir() and item.name not in skip_folders and not item.name.startswith('.'):
            # Only include subfolders that have Python files
            if any(item.rglob("*.py")):
                subfolders.append(item.name)
    
    # Generate Mermaid diagram for this folder if it has content
    if all_classes or subfolders or has_python_files:
        output_folder.mkdir(parents=True, exist_ok=True)
        
        mermaid_content = generate_mermaid_diagram(
            source_folder.name, 
            all_classes, 
            subfolders,
            current_doc_path=api_path
        )
        
        mmd_path = output_folder / "class_diagram.mmd"
        was_written = save_mermaid_file(mermaid_content, mmd_path)
    
    # Recursively process subfolders
    for subfolder_name in subfolders:
        subfolder_source = source_folder / subfolder_name
        subfolder_output = output_folder / subfolder_name
        subfolder_api_path = f"{api_path}/{subfolder_name}" if api_path else subfolder_name
        process_folder_for_mermaid(subfolder_source, subfolder_output, subfolder_api_path, processed)
    
    return True


def clean_old_plantuml_files(base_path: Path):
    """Remove old .puml files that are no longer needed."""
    removed_count = 0
    for puml_file in base_path.rglob("*.puml"):
        try:
            puml_file.unlink()
            removed_count += 1
        except Exception as e:
            print(f"  Warning: Could not remove {puml_file}: {e}")
    
    if removed_count > 0:
        print(f"  Cleaned up {removed_count} old .puml files")


def main():
    """Main function to generate all Mermaid UML diagrams."""
    
    # Clean up old PlantUML files
    clean_old_plantuml_files(MERMAID_OUTPUT_BASE)
    
    # Build global class registry for cross-package references
    ddo_source = PROJECT_ROOT / "Distributed_Design_Optimizer"
    if ddo_source.exists():
        build_global_class_registry(ddo_source, "Distributed_Design_Optimizer")
    
    # Process Distributed_Design_Optimizer
    ddo_output = MERMAID_OUTPUT_BASE / "Distributed_Design_Optimizer"
    
    if ddo_source.exists():
        process_folder_for_mermaid(ddo_source, ddo_output, "Distributed_Design_Optimizer")
    else:
        print(f"  WARNING: Source folder not found: {ddo_source}")
    
    # Note: userfiles is excluded from UML generation (API docs only)
    print(f"  Generated {len(GLOBAL_CLASS_REGISTRY)} Mermaid UML diagrams")


if __name__ == "__main__":
    main()
