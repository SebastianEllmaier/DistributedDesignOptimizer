#!/usr/bin/env python3
"""
Auto-generate API documentation from Python source code.
Extracts docstrings and creates Markdown files for MkDocs.

This script recursively processes:
- Distributed_Design_Optimizer/ - Core package modules
- userfiles/ - User example files and configurations

The generated documentation mirrors the source folder structure.
"""

import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set


# Global registry of class names to their documentation paths (for cross-references)
CLASS_REGISTRY: Dict[str, str] = {}

# Global tracking for validation report
SYNTAX_ERRORS: List[Dict] = []
LICENSE_ISSUES: List[Dict] = []
DOCSTRING_ISSUES: List[Dict] = []
FILES_CHECKED: int = 0
CLASSES_CHECKED: int = 0
FUNCTIONS_CHECKED: int = 0

# License header lines to check (loaded dynamically from file)
LICENSE_CHECK_LINES: List[str] = []
LICENSE_FULL_CONTENT: str = ""

# Docstring validation rules (loaded dynamically from file)
DOCSTRING_RULES: Dict[str, bool] = {}
DOCSTRING_STYLE_CONTENT: str = ""


def load_license_header(repo_root: Path) -> None:
    """Load the license header from the Short_License_Notice_Top_of_Every_Py_File.md.
    
    Args:
        repo_root: Path to the repository root
    """
    global LICENSE_CHECK_LINES, LICENSE_FULL_CONTENT
    
    license_file = repo_root / "docs_src" / "Short_License_Notice_Top_of_Every_Py_File.md"
    
    if not license_file.exists():
        print(f"  Warning: License file not found: {license_file}")
        LICENSE_CHECK_LINES = []
        LICENSE_FULL_CONTENT = ""
        return
    
    with open(license_file, 'r', encoding='utf-8') as f:
        LICENSE_FULL_CONTENT = f.read().strip()
    
    # Extract non-empty comment lines for checking
    # We'll check for the first two substantive lines (copyright and license type)
    LICENSE_CHECK_LINES = []
    for line in LICENSE_FULL_CONTENT.split('\n'):
        line = line.strip()
        if line.startswith('#') and len(line) > 2:
            # Get the content after the # (stripped)
            content = line[1:].strip()
            if content and not content.startswith('Additional') and not content.startswith('I kindly'):
                LICENSE_CHECK_LINES.append(content)
            if len(LICENSE_CHECK_LINES) >= 2:
                break


def load_docstring_style(repo_root: Path) -> None:
    """Load the docstring style rules from the Docstring_Style file.
    
    Args:
        repo_root: Path to the repository root
    """
    global DOCSTRING_RULES, DOCSTRING_STYLE_CONTENT
    
    style_file = repo_root / "docs_src" / "Docstring_Style.md"
    
    if not style_file.exists():
        print(f"  Warning: Docstring style file not found: {style_file}")
        DOCSTRING_RULES = {}
        DOCSTRING_STYLE_CONTENT = ""
        return
    
    with open(style_file, 'r', encoding='utf-8') as f:
        DOCSTRING_STYLE_CONTENT = f.read().strip()
    
    # Parse rules from the file - look for lines with [RULE] prefix
    DOCSTRING_RULES = {}
    for line in DOCSTRING_STYLE_CONTENT.split('\n'):
        line = line.strip()
        if '[RULE]' in line:
            # Extract rule name after [RULE]
            rule_part = line.split('[RULE]')[1].strip()
            # Remove leading # if present
            if rule_part.startswith('#'):
                rule_part = rule_part[1:].strip()
            rule_name = rule_part.split()[0] if rule_part else None
            if rule_name:
                DOCSTRING_RULES[rule_name] = True


def check_docstrings(module_data: Dict, file_path: str) -> List[Dict]:
    """Check docstrings against the loaded style rules.
    
    Args:
        module_data: Dictionary containing module documentation data
        file_path: Path to the file being checked
        
    Returns:
        List of docstring issues found
    """
    issues = []
    
    if not DOCSTRING_RULES:
        return issues
    
    # Check module docstring
    if DOCSTRING_RULES.get('MODULE_DOCSTRING_REQUIRED'):
        if not module_data.get('module_docstring'):
            issues.append({
                'file': file_path,
                'element': '(module)',
                'issue': 'Missing module-level docstring'
            })
    
    # Check class docstrings
    if DOCSTRING_RULES.get('CLASS_DOCSTRING_REQUIRED'):
        for cls in module_data.get('classes', []):
            if not cls.get('docstring_raw'):
                issues.append({
                    'file': file_path,
                    'element': f"class {cls['name']}",
                    'issue': 'Missing class docstring'
                })
            elif DOCSTRING_RULES.get('SUMMARY_LINE_REQUIRED'):
                issues.extend(_check_summary_line(
                    cls['docstring_raw'], file_path, f"class {cls['name']}"))
    
    # Check function/method docstrings
    check_functions = DOCSTRING_RULES.get('FUNCTION_DOCSTRING_REQUIRED', False)
    check_init = DOCSTRING_RULES.get('INIT_DOCSTRING_REQUIRED', False)
    
    # Check top-level functions
    if check_functions:
        for func in module_data.get('functions', []):
            if not func.get('is_private') and not func.get('docstring_raw'):
                issues.append({
                    'file': file_path,
                    'element': f"function {func['name']}",
                    'issue': 'Missing function docstring'
                })
            elif not func.get('is_private') and func.get('docstring_raw'):
                issues.extend(_check_function_docstring(
                    func, file_path, f"function {func['name']}"))
    
    # Check methods in classes
    for cls in module_data.get('classes', []):
        for method in cls.get('methods', []):
            element_name = f"{cls['name']}.{method['name']}"
            # Check __init__ if rule is enabled
            if method['name'] == '__init__' and check_init:
                if not method.get('docstring_raw'):
                    issues.append({
                        'file': file_path,
                        'element': element_name,
                        'issue': 'Missing __init__ docstring'
                    })
                else:
                    issues.extend(_check_function_docstring(
                        method, file_path, element_name))
            # Check public methods if rule is enabled
            elif check_functions and not method.get('is_private'):
                if not method.get('docstring_raw'):
                    issues.append({
                        'file': file_path,
                        'element': element_name,
                        'issue': 'Missing method docstring'
                    })
                else:
                    issues.extend(_check_function_docstring(
                        method, file_path, element_name))
    
    # Check type hints on all functions and methods (independent of docstrings)
    if DOCSTRING_RULES.get('NO_UNION_OPTIONAL') or DOCSTRING_RULES.get('NO_QUOTED_TYPE_HINTS'):
        for func in module_data.get('functions', []):
            issues.extend(_check_type_hints(
                func, file_path, f"function {func['name']}"))
        for cls in module_data.get('classes', []):
            for method in cls.get('methods', []):
                issues.extend(_check_type_hints(
                    method, file_path, f"{cls['name']}.{method['name']}"))
    
    return issues


def _check_summary_line(docstring: str, file_path: str, element: str) -> List[Dict]:
    """Check that a docstring starts with a proper one-line summary.
    
    Args:
        docstring: Raw docstring text
        file_path: Path to the file being checked
        element: Element identifier for reporting
        
    Returns:
        List of issues found
    """
    issues = []
    if not docstring:
        return issues
    
    lines = docstring.strip().split('\n')
    summary = lines[0].strip()
    
    if not summary:
        issues.append({
            'file': file_path,
            'element': element,
            'issue': 'Docstring summary line is empty'
        })
    elif not summary.endswith('.'):
        issues.append({
            'file': file_path,
            'element': element,
            'issue': f'Summary line does not end with a period: "{summary[:60]}..."'
                     if len(summary) > 60 else
                     f'Summary line does not end with a period: "{summary}"'
        })
    
    return issues


def _parse_docstring_sections(docstring: str) -> Dict[str, str]:
    """Parse a Google-style docstring into its sections.
    
    Args:
        docstring: Raw docstring text
        
    Returns:
        Dictionary mapping section names to their content.
    """
    sections = {}
    current_section = None
    current_content = []
    
    known_sections = {'Args', 'Returns', 'Raises', 'Yields', 'Attributes',
                      'Example', 'Examples', 'Note', 'Notes', 'References',
                      'Todo', 'Warnings'}
    
    for line in docstring.split('\n'):
        stripped = line.strip()
        # Check if this line is a section header (e.g., "Args:")
        if stripped.endswith(':') and stripped[:-1] in known_sections:
            # Save previous section
            if current_section is not None:
                sections[current_section] = '\n'.join(current_content)
            current_section = stripped[:-1]
            current_content = []
        elif current_section is not None:
            current_content.append(line)
    
    # Save the last section
    if current_section is not None:
        sections[current_section] = '\n'.join(current_content)
    
    return sections


def _parse_args_section(args_content: str) -> List[str]:
    """Parse the Args section to extract documented parameter names.
    
    Args:
        args_content: Content of the Args section (lines after "Args:")
        
    Returns:
        List of parameter names documented in the Args section.
    """
    params = []
    for line in args_content.split('\n'):
        stripped = line.strip()
        if not stripped:
            continue
        # A parameter line starts with "param_name:" or "param_name (type):"
        # It should be at the first indentation level (4 spaces from section header)
        match = re.match(r'^(\w+)\s*(?:\([^)]*\))?\s*:', stripped)
        if match:
            params.append(match.group(1))
    return params


def _check_function_docstring(func_info: Dict, file_path: str, element: str) -> List[Dict]:
    """Check a function/method docstring for Google-style compliance.
    
    Validates:
    - Summary line presence and period
    - Args section documents all parameters
    - No stale parameters in Args
    - Returns section present when return type is annotated
    
    Args:
        func_info: Dictionary with function/method data (docstring_raw, args, return_type)
        file_path: Path to the file being checked
        element: Element identifier for reporting
        
    Returns:
        List of issues found
    """
    issues = []
    docstring = func_info.get('docstring_raw')
    if not docstring:
        return issues
    
    # Check summary line
    if DOCSTRING_RULES.get('SUMMARY_LINE_REQUIRED'):
        issues.extend(_check_summary_line(docstring, file_path, element))
    
    # Parse docstring sections
    sections = _parse_docstring_sections(docstring)
    
    # Get actual parameters (exclude self and cls)
    actual_params = [
        arg['name'] for arg in func_info.get('args', [])
        if arg['name'] not in ('self', 'cls')
    ]
    
    # Check Args documentation
    if DOCSTRING_RULES.get('ARGS_DOCUMENTED') and actual_params:
        if 'Args' not in sections:
            issues.append({
                'file': file_path,
                'element': element,
                'issue': f'Missing Args: section (has parameters: {", ".join(actual_params)})'
            })
        else:
            documented_params = _parse_args_section(sections['Args'])
            
            # Check for undocumented parameters
            for param in actual_params:
                if param not in documented_params:
                    issues.append({
                        'file': file_path,
                        'element': element,
                        'issue': f'Parameter "{param}" not documented in Args section'
                    })
            
            # Check for stale/extra parameters in docstring
            if DOCSTRING_RULES.get('NO_UNDOCUMENTED_PARAMS'):
                for doc_param in documented_params:
                    if doc_param not in actual_params:
                        issues.append({
                            'file': file_path,
                            'element': element,
                            'issue': f'Args documents "{doc_param}" which is not in the signature'
                        })
    
    # Check Returns documentation
    if DOCSTRING_RULES.get('RETURNS_DOCUMENTED'):
        return_type = func_info.get('return_type')
        if return_type and return_type != 'None':
            if 'Returns' not in sections and 'Yields' not in sections:
                issues.append({
                    'file': file_path,
                    'element': element,
                    'issue': f'Missing Returns: section (return type annotated as {return_type})'
                })
    
    # Check Raises section format
    if DOCSTRING_RULES.get('RAISES_DOCUMENTED') and 'Raises' in sections:
        raises_content = sections['Raises']
        for line in raises_content.split('\n'):
            stripped = line.strip()
            if not stripped:
                continue
            # Each raises entry should match "ExceptionType: description"
            if not re.match(r'^[A-Z]\w*(?:Error|Exception|Warning)?\s*:', stripped):
                # Could be a continuation line (indented), skip those
                # Continuation lines are typically indented more than the exception line
                if not line.startswith('        ') and not line.startswith('\t\t'):
                    issues.append({
                        'file': file_path,
                        'element': element,
                        'issue': f'Raises entry not in "ExceptionType: description" format: "{stripped[:50]}"'
                    })
                    break  # Only report once per element
    
    return issues


def _check_type_hints(func_info: Dict, file_path: str, element: str) -> List[Dict]:
    """Check function/method type hints for PEP 604 style and forbidden quoting.

    Validates:
    - No typing.Union[...] usage (use "X | Y" instead)
    - No typing.Optional[...] usage (use "X | None" instead)
    - No quoted/forward-reference type hints (use direct type hints)

    The ``update_state`` methods are exempt from these checks: their parameter is
    inherently a forward reference to the enclosing class (and, for proxy-backed
    storages, a union with it). Because the class is not yet bound while its own
    method signatures are evaluated, a quoted/forward-reference hint is required
    there to avoid ``NameError`` and circular-import problems. This is a sanctioned
    pattern rather than a style violation, so it is skipped here.

    Args:
        func_info: Dictionary with function/method data (args, return_type_raw).
        file_path: Path to the file being checked.
        element: Element identifier for reporting.

    Returns:
        List of type-hint issues found.
    """
    issues = []

    # Skip state-merge methods: their hints are necessarily self-referential.
    if func_info.get('name') == 'update_state':
        return issues

    check_union = DOCSTRING_RULES.get('NO_UNION_OPTIONAL', False)
    check_quoted = DOCSTRING_RULES.get('NO_QUOTED_TYPE_HINTS', False)
    if not check_union and not check_quoted:
        return issues

    # Collect (label, raw annotation) pairs for all annotated args and the return type.
    annotations = []
    for arg in func_info.get('args', []):
        raw = arg.get('type_raw')
        if raw:
            annotations.append((f'parameter "{arg["name"]}"', raw))
    return_raw = func_info.get('return_type_raw')
    if return_raw:
        annotations.append(('return type', return_raw))

    for label, raw in annotations:
        if check_union:
            if re.search(r'\bUnion\[', raw):
                issues.append({
                    'file': file_path,
                    'element': element,
                    'issue': f'{label} uses Union[...] ("{raw}"); use "X | Y" syntax instead'
                })
            if re.search(r'\bOptional\[', raw):
                issues.append({
                    'file': file_path,
                    'element': element,
                    'issue': f'{label} uses Optional[...] ("{raw}"); use "X | None" syntax instead'
                })
        if check_quoted and 'Literal[' not in raw:
            # Quoted/forward-reference hints appear as string literals in the annotation.
            if '"' in raw or "'" in raw:
                issues.append({
                    'file': file_path,
                    'element': element,
                    'issue': f'{label} uses a quoted/forward-reference type hint ("{raw}"); use a direct type hint instead'
                })

    return issues


def sanitize_for_markdown(text: str, base_indent: str = "") -> str:
    """Sanitize text to be safe in Markdown while preserving docstring structure.
    
    Args:
        text: The docstring text to sanitize
        base_indent: Base indentation to apply to all lines (for nested content)
    """
    if not text:
        return f"{base_indent}No description available."
    
    # Replace problematic characters
    text = text.replace('"', "'")
    text = text.replace('\\', '/')
    text = text.replace('\t', '    ')
    
    # Remove control characters
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    
    # Process lines while preserving structure for Args/Returns/etc sections
    lines = text.split('\n')
    result_lines = []
    in_section = False
    
    for line in lines:
        stripped = line.strip()
        # Keep section headers (Args:, Returns:, etc.)
        if stripped.endswith(':') and stripped[:-1] in ('Args', 'Returns', 'Raises', 'Yields', 'Attributes', 'Example', 'Examples', 'Note', 'Notes'):
            result_lines.append('')  # Add blank line before section
            result_lines.append(f'{base_indent}**{stripped}**')  # Bold section header
            in_section = True
        elif line.startswith('    ') or line.startswith('\t'):
            # Indented content (argument descriptions)
            if in_section:
                result_lines.append(f'{base_indent}> {stripped}  ')  # Use blockquote for args
            else:
                result_lines.append(f'{base_indent}{stripped}')
        elif stripped == '':
            result_lines.append('')
            in_section = False
        else:
            result_lines.append(f'{base_indent}{stripped}')
            in_section = False
    
    return '\n'.join(result_lines).strip() or f"{base_indent}No description available."


class DocstringExtractor(ast.NodeVisitor):
    """Extract docstrings and signatures from Python AST."""
    
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.classes: List[Dict] = []
        self.functions: List[Dict] = []
        self.module_docstring: Optional[str] = None
        self.module_docstring_raw: Optional[str] = None
        
    def visit_Module(self, node: ast.Module):
        docstring = ast.get_docstring(node)
        self.module_docstring_raw = docstring
        self.module_docstring = sanitize_for_markdown(docstring) if docstring else None
        self.generic_visit(node)
        
    def visit_ClassDef(self, node: ast.ClassDef):
        docstring = ast.get_docstring(node)
        class_info = {
            'name': node.name,
            'docstring': sanitize_for_markdown(docstring),
            'docstring_raw': docstring,
            'bases': [self._get_name(base) for base in node.bases],
            'methods': [],
            'attributes': [],
            'lineno': node.lineno
        }
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = self._extract_function(item)
                class_info['methods'].append(method_info)
            elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                # Class attribute with type annotation (e.g., attr: Type = value)
                attr_info = {
                    'name': item.target.id,
                    'type': self._get_annotation(item.annotation) if item.annotation else None
                }
                class_info['attributes'].append(attr_info)
            elif isinstance(item, ast.Assign):
                # Class attribute without type annotation (e.g., attr = value)
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        class_info['attributes'].append({
                            'name': target.id,
                            'type': None
                        })
                
        self.classes.append(class_info)
        
    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Only top-level functions
        if isinstance(node, ast.FunctionDef):
            func_info = self._extract_function(node)
            self.functions.append(func_info)
            
    def _extract_function(self, node: ast.FunctionDef) -> Dict:
        args = []
        for arg in node.args.args:
            arg_info = {'name': arg.arg}
            if arg.annotation:
                arg_info['type'] = self._get_annotation(arg.annotation)
                arg_info['type_raw'] = self._get_raw_annotation(arg.annotation)
            args.append(arg_info)
            
        return_type = None
        return_type_raw = None
        if node.returns:
            return_type = self._get_annotation(node.returns)
            return_type_raw = self._get_raw_annotation(node.returns)
        
        docstring = ast.get_docstring(node)
        return {
            'name': node.name,
            'docstring': sanitize_for_markdown(docstring),
            'docstring_raw': docstring,
            'args': args,
            'return_type': return_type,
            'return_type_raw': return_type_raw,
            'lineno': node.lineno,
            'is_private': node.name.startswith('_')
        }
        
    def _get_name(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return str(node)
        
    def _get_annotation(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Subscript):
            return f"{self._get_name(node.value)}[{self._get_annotation(node.slice)}]"
        elif isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Tuple):
            return ", ".join(self._get_annotation(elt) for elt in node.elts)
        return ast.unparse(node) if hasattr(ast, 'unparse') else str(node)

    def _get_raw_annotation(self, node) -> str:
        """Return the raw source form of an annotation, preserving quotes and Union/Optional.

        Args:
            node: The AST annotation node.

        Returns:
            The unparsed annotation string, or an empty string if unavailable.
        """
        if not hasattr(ast, 'unparse'):
            return ""
        try:
            return ast.unparse(node)
        except Exception:
            return ""


def linkify_type(type_str: str, current_doc_path: str) -> str:
    """
    Convert type annotations to markdown links where possible.
    
    Args:
        type_str: The type annotation string (e.g., "List[SubSystemInterface]")
        current_doc_path: The path of the current documentation file (for relative links)
    
    Returns:
        Type string with class names converted to markdown links
    """
    if not type_str:
        return type_str
    
    # Avoid matching common built-in types
    builtin_types = {'Any', 'None', 'bool', 'int', 'float', 'str', 'bytes', 'list', 'dict', 
                     'set', 'tuple', 'List', 'Dict', 'Set', 'Tuple', 'Optional', 'Union',
                     'Callable', 'Type', 'Sequence', 'Iterable', 'Iterator', 'Generator'}
    
    def make_link(class_name: str) -> str:
        """Create a markdown link for a class name."""
        if class_name not in CLASS_REGISTRY:
            return class_name
            
        target_path = CLASS_REGISTRY[class_name]
        current_parts = current_doc_path.split('/')
        target_parts = target_path.split('/')
        
        # Find common prefix length
        common_len = 0
        for i in range(min(len(current_parts) - 1, len(target_parts) - 1)):
            if current_parts[i] == target_parts[i]:
                common_len = i + 1
            else:
                break
        
        # Build relative path
        ups = len(current_parts) - 1 - common_len
        rel_path = '../' * ups + '/'.join(target_parts[common_len:])
        
        return f"[{class_name}]({rel_path})"
    
    # Split by brackets and commas to process each potential type separately
    result = []
    current_word = ""
    for char in type_str:
        if char in '[](),: ':
            if current_word:
                if current_word not in builtin_types and current_word in CLASS_REGISTRY:
                    current_word = make_link(current_word)
                result.append(current_word)
                current_word = ""
            result.append(char)
        else:
            current_word += char
    if current_word:
        if current_word not in builtin_types and current_word in CLASS_REGISTRY:
            current_word = make_link(current_word)
        result.append(current_word)
    
    return ''.join(result)


def linkify_bases(bases: List[str], current_doc_path: str) -> str:
    """Convert base class names to markdown links."""
    linked = []
    for base in bases:
        if base in CLASS_REGISTRY:
            target_path = CLASS_REGISTRY[base]
            current_parts = current_doc_path.split('/')
            target_parts = target_path.split('/')
            common_len = 0
            for i in range(min(len(current_parts) - 1, len(target_parts) - 1)):
                if current_parts[i] == target_parts[i]:
                    common_len = i + 1
                else:
                    break
            ups = len(current_parts) - 1 - common_len
            rel_path = '../' * ups + '/'.join(target_parts[common_len:])
            linked.append(f"[{base}]({rel_path})")
        else:
            linked.append(f"`{base}`")
    return ', '.join(linked)


def generate_class_markdown(class_info: Dict, module_path: str, doc_path: str) -> str:
    """Generate Markdown documentation for a class."""
    md = f"### {class_info['name']}\n\n"
    
    if class_info['bases']:
        md += f"> **Inherits from:** {linkify_bases(class_info['bases'], doc_path)}\n\n"
    
    # Class docstring with indent
    docstring = sanitize_for_markdown(class_info.get('docstring_raw', class_info['docstring']), base_indent="> ")
    md += f"{docstring}\n\n"
    
    # Attributes (class-level typed attributes)
    attributes = class_info.get('attributes', [])
    # Filter to show only public attributes with type annotations
    typed_attributes = [a for a in attributes if a.get('type') and not a['name'].startswith('_')]
    
    if typed_attributes:
        md += "#### Attributes\n\n"
        for attr in typed_attributes:
            linked_type = linkify_type(attr['type'], doc_path)
            md += f"> `{attr['name']}`: {linked_type}  \n"
        md += "\n"
    
    # Methods
    public_methods = [m for m in class_info['methods'] if not m['is_private'] or m['name'] == '__init__']
    
    if public_methods:
        md += "#### Methods\n\n"
        for method in public_methods:
            md += generate_method_markdown(method, doc_path)
            
    return md


def generate_method_markdown(method: Dict, doc_path: str = "") -> str:
    """Generate Markdown for a method/function."""
    # Build signature with linkified types (without backticks so links work)
    args_parts = []
    for arg in method['args']:
        if 'type' in arg:
            linked_type = linkify_type(arg['type'], doc_path) if doc_path else arg['type']
            args_parts.append(f"{arg['name']}: {linked_type}")
        else:
            args_parts.append(arg['name'])
    args_str = ", ".join(args_parts)
    
    return_str = ""
    if method['return_type']:
        linked_return = linkify_type(method['return_type'], doc_path) if doc_path else method['return_type']
        return_str = f" → {linked_return}"
    
    # Method signature in a collapsible admonition box (??? = collapsed by default)
    md = f'??? abstract "{method["name"]}({args_str}){return_str}"\n'
    
    # Method docstring inside the collapsible box
    # Must be indented with 4 spaces and NO blank line after the header
    raw_docstring = method.get('docstring_raw') or method.get('docstring') or "No description available."
    
    # Process the docstring - indent every line with 4 spaces for the admonition
    docstring_lines = []
    in_section = False
    
    for line in raw_docstring.split('\n'):
        stripped = line.strip()
        if not stripped:
            docstring_lines.append("")
            in_section = False
        elif stripped.endswith(':') and stripped[:-1] in ('Args', 'Returns', 'Raises', 'Yields', 'Attributes', 'Example', 'Examples', 'Note', 'Notes'):
            docstring_lines.append("")
            docstring_lines.append(f"    **{stripped}**")
            in_section = True
        elif (line.startswith('    ') or line.startswith('\t')) and in_section:
            # Argument descriptions - use blockquote style
            docstring_lines.append(f"    > {stripped}  ")
        else:
            docstring_lines.append(f"    {stripped}")
    
    md += '\n'.join(docstring_lines)
    md += "\n\n"
        
    return md


def check_license_header(source: str) -> bool:
    """Check if the source code has the required license header.
    
    Args:
        source: The source code content
        
    Returns:
        True if license header is present, False otherwise
    """
    # If no license lines were loaded, skip the check
    if not LICENSE_CHECK_LINES:
        return True
    
    # Check that all required license lines are present in the source
    for check_line in LICENSE_CHECK_LINES:
        if check_line not in source:
            return False
    return True


def generate_validation_report(docs_src: Path) -> None:
    """Generate the syntax validation report.
    
    Args:
        docs_src: Path to the docs_src directory
    """
    report_path = docs_src / "syntax_report.txt"
    
    # Deduplicate docstring issues (files may be processed more than once)
    seen = set()
    unique_docstring_issues = []
    for issue in DOCSTRING_ISSUES:
        key = (issue['file'], issue['element'], issue['issue'])
        if key not in seen:
            seen.add(key)
            unique_docstring_issues.append(issue)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("SYNTAX VALIDATION REPORT\n")
        f.write("=" * 70 + "\n")
        f.write(f"Files checked: {FILES_CHECKED}\n")
        f.write(f"Classes checked: {CLASSES_CHECKED}\n")
        f.write(f"Functions/Methods checked: {FUNCTIONS_CHECKED}\n")
        f.write(f"Files with syntax errors: {len(SYNTAX_ERRORS)}\n")
        f.write(f"Files missing license header: {len(LICENSE_ISSUES)}\n")
        f.write(f"Docstring & type-hint issues found: {len(unique_docstring_issues)}\n")
        f.write("\n")
        
        # Syntax Errors Section
        if SYNTAX_ERRORS:
            f.write("=" * 70 + "\n")
            f.write("SYNTAX ERRORS (files could not be parsed)\n")
            f.write("=" * 70 + "\n\n")
            for error in SYNTAX_ERRORS:
                f.write(f"[FILE] {error['file']}\n")
                f.write(f"  Error: {error['error']}\n\n")
        
        # License Issues Section
        if LICENSE_ISSUES:
            f.write("=" * 70 + "\n")
            f.write("LICENSE HEADER MISSING\n")
            f.write("=" * 70 + "\n\n")
            for issue in LICENSE_ISSUES:
                f.write(f"[FILE] {issue['file']}\n")
                f.write(f"  Issue: {issue['issue']}\n\n")
        
        # Docstring Issues Section
        if unique_docstring_issues:
            f.write("=" * 70 + "\n")
            f.write("DOCSTRING & TYPE-HINT ISSUES\n")
            f.write("=" * 70 + "\n\n")
            # Group by file for better readability
            issues_by_file = {}
            for issue in unique_docstring_issues:
                file_key = issue['file']
                if file_key not in issues_by_file:
                    issues_by_file[file_key] = []
                issues_by_file[file_key].append(issue)
            
            for file_path, issues in sorted(issues_by_file.items()):
                f.write(f"[FILE] {file_path}\n")
                for issue in issues:
                    f.write(f"  - {issue['element']}: {issue['issue']}\n")
                f.write("\n")
        
        # Recommended Actions
        f.write("-" * 70 + "\n")
        f.write("RECOMMENDED ACTIONS\n")
        f.write("-" * 70 + "\n\n")
        
        if SYNTAX_ERRORS:
            f.write("SYNTAX ERRORS:\n")
            f.write("  Fix the Python syntax errors in the listed files.\n")
            f.write("  Common issues include:\n")
            f.write("    - Unexpected indentation\n")
            f.write("    - Missing colons after function/class definitions\n")
            f.write("    - Unclosed brackets or parentheses\n")
            f.write("    - Invalid f-string syntax\n\n")
        
        if LICENSE_ISSUES and LICENSE_FULL_CONTENT:
            f.write("LICENSE HEADER:\n")
            f.write("  Add the following license header at the TOP of each file:\n\n")
            for line in LICENSE_FULL_CONTENT.split('\n'):
                f.write(f"    {line}\n")
            f.write("\n")
        
        if unique_docstring_issues and DOCSTRING_STYLE_CONTENT:
            f.write("DOCSTRING STYLE:\n")
            f.write("  Add docstrings following the Google style guide.\n")
            f.write("  Required docstrings are determined by the rules in Docstring_Style file.\n")
            f.write("  Active rules:\n")
            for rule_name, enabled in DOCSTRING_RULES.items():
                if enabled:
                    f.write(f"    - {rule_name}\n")
            f.write("\n")
            f.write("  Example Google-style docstring:\n")
            f.write("    '''\n")
            f.write("    One-line summary of function.\n")
            f.write("\n")
            f.write("    Args:\n")
            f.write("        param1: Description of first parameter.\n")
            f.write("        param2: Description of second parameter.\n")
            f.write("\n")
            f.write("    Returns:\n")
            f.write("        Description of return value.\n")
            f.write("\n")
            f.write("    Raises:\n")
            f.write("        ValueError: Description of when this is raised.\n")
            f.write("    '''\n\n")
        
        if not SYNTAX_ERRORS and not LICENSE_ISSUES and not DOCSTRING_ISSUES:
            f.write("No issues found! All files have valid syntax, license headers, and docstrings.\n")


def process_module(file_path: Path, base_path: Path) -> Tuple[str, Dict]:
    """Process a Python module and extract documentation."""
    global FILES_CHECKED, CLASSES_CHECKED, FUNCTIONS_CHECKED, SYNTAX_ERRORS, LICENSE_ISSUES, DOCSTRING_ISSUES
    
    FILES_CHECKED += 1
    relative_path = file_path.relative_to(base_path)
    module_name = str(relative_path.with_suffix('')).replace(os.sep, '.')
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        source = f.read()
    
    # Check for license header
    if not check_license_header(source):
        LICENSE_ISSUES.append({
            'file': str(relative_path),
            'issue': 'Missing or incorrect license header'
        })
        
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        print(f"  Warning: Could not parse {file_path.name}: {e}")
        SYNTAX_ERRORS.append({
            'file': str(relative_path),
            'error': str(e)
        })
        return module_name, {}
        
    extractor = DocstringExtractor(module_name)
    extractor.visit(tree)
    
    # Track classes and functions
    CLASSES_CHECKED += len(extractor.classes)
    FUNCTIONS_CHECKED += len(extractor.functions)
    for cls in extractor.classes:
        FUNCTIONS_CHECKED += len(cls.get('methods', []))
    
    module_data = {
        'module_docstring': extractor.module_docstring,
        'classes': extractor.classes,
        'functions': extractor.functions,
        'path': str(relative_path),
        'source_code': source
    }
    
    # Check docstrings against style rules
    docstring_issues = check_docstrings(module_data, str(relative_path))
    DOCSTRING_ISSUES.extend(docstring_issues)
    
    return module_name, module_data


def generate_source_page(module_name: str, source_path: str, source_code: str) -> str:
    """Generate a Markdown page showing the source code of a module."""
    simple_name = module_name.split('.')[-1]
    
    md = f"---\ntitle: {simple_name} (Source)\n---\n\n"
    md += f"← Back to [{simple_name} documentation]({simple_name}.md)\n\n"
    md += f"# {simple_name} - Source Code\n\n"
    md += f"**File:** `{source_path}`\n\n"
    md += "```python\n"
    md += source_code
    md += "\n```\n"
    
    return md


def generate_module_page(module_name: str, module_data: Dict, doc_path: str, parent_package: str = "") -> str:
    """Generate a complete Markdown page for a module."""
    simple_name = module_name.split('.')[-1]
    
    # MkDocs front matter
    md = f"---\ntitle: {simple_name}\n---\n\n"
    
    # Navigation link back to parent package
    if parent_package:
        md += f"← Back to [{parent_package}](index.md)\n\n"
    
    md += f"# {simple_name}\n\n"
    md += f"**Source:** [{module_data['path']}]({simple_name}_source.md)\n\n"
    
    if module_data['module_docstring']:
        md += f"{module_data['module_docstring']}\n\n"
        
    # Classes
    if module_data['classes']:
        md += "## Classes\n\n"
        for class_info in module_data['classes']:
            md += generate_class_markdown(class_info, module_data['path'], doc_path)
            
    public_functions = [f for f in module_data['functions'] if not f['is_private']]
    if public_functions:
        md += "## Functions\n\n"
        for func in public_functions:
            md += generate_method_markdown(func, doc_path)
    
    return md


def generate_folder_index(folder_name: str, subfolders: List[str], modules: List[str], 
                          description: str = "", output_folder: Path = None) -> str:
    """Generate index page for a folder, including interactive Mermaid UML diagram if available."""
    md = f"---\ntitle: {folder_name}\n---\n\n"
    md += f"# {folder_name}\n\n"
    
    if description:
        md += f"{description}\n\n"
    
    # Check for interactive Mermaid class diagram (.mmd file) and embed it
    # Mermaid diagrams are rendered client-side with clickable links to documentation
    if output_folder:
        mmd_file = output_folder / "class_diagram.mmd"
        if mmd_file.exists():
            try:
                with open(mmd_file, 'r', encoding='utf-8') as f:
                    mermaid_content = f.read()
                md += "## Class Diagram\n\n"
                md += "*Click on class names to navigate to their documentation.*\n\n"
                # Mermaid content already includes ```mermaid and ``` delimiters
                md += mermaid_content
                md += "\n\n"
            except Exception:
                pass  # Skip if can't read the file
    
    if subfolders:
        md += "## Subpackages\n\n"
        for subfolder in sorted(subfolders):
            md += f"- [{subfolder}]({subfolder}/index.md)\n"
        md += "\n"
    
    if modules:
        md += "## Modules\n\n"
        for module in sorted(modules):
            md += f"- [{module}]({module}.md)\n"
        md += "\n"
    
    return md


def collect_classes_recursive(source_folder: Path, output_folder: Path, repo_root: Path,
                              processed_paths: Set[str] = None) -> List[Tuple[Path, str, Dict]]:
    """
    First pass: Collect all classes and build the CLASS_REGISTRY.
    
    Returns:
        List of (py_file, module_name, module_data) tuples for later processing.
    """
    global CLASS_REGISTRY
    
    if processed_paths is None:
        processed_paths = set()
    
    folder_key = str(source_folder.resolve())
    if folder_key in processed_paths:
        return []
    processed_paths.add(folder_key)
    
    collected = []
    
    # Process Python files in this folder
    for py_file in sorted(source_folder.glob("*.py")):
        if py_file.name.startswith('__'):
            continue
            
        module_name, module_data = process_module(py_file, repo_root)
        
        if module_data and (module_data['classes'] or module_data['functions']):
            collected.append((py_file, module_name, module_data, output_folder))
            
            # Register classes in the global registry
            # Calculate the doc path relative to api/ folder
            rel_output = output_folder.relative_to(output_folder.parents[len(output_folder.parts) - output_folder.parts.index('api') - 2])
            doc_path = str(rel_output / f"{py_file.stem}.md").replace('\\', '/')
            
            for class_info in module_data['classes']:
                # Store: class_name -> doc_path (with anchor to class heading)
                CLASS_REGISTRY[class_info['name']] = f"{doc_path}#{class_info['name'].lower()}"
    
    # Process subfolders recursively
    for subfolder in sorted(source_folder.iterdir()):
        if not subfolder.is_dir():
            continue
        if subfolder.name.startswith(('__', '.', 'build', 'dist', 'egg-info')):
            continue
        if subfolder.name in ('__pycache__', '.git', 'node_modules'):
            continue
            
        has_python = any(subfolder.rglob("*.py"))
        if not has_python:
            continue
            
        sub_output = output_folder / subfolder.name
        sub_output.mkdir(parents=True, exist_ok=True)
        
        collected.extend(collect_classes_recursive(subfolder, sub_output, repo_root, processed_paths))
    
    return collected


def process_folder_recursive(source_folder: Path, output_folder: Path, repo_root: Path,
                             processed_paths: Set[str] = None) -> Tuple[List[str], List[str]]:
    """
    Second pass: Generate documentation with cross-reference links.
    
    Returns:
        Tuple of (subfolder_names, module_names) for index generation.
    """
    if processed_paths is None:
        processed_paths = set()
    
    # Avoid processing the same path twice
    folder_key = str(source_folder.resolve())
    if folder_key in processed_paths:
        return [], []
    processed_paths.add(folder_key)
    
    output_folder.mkdir(parents=True, exist_ok=True)
    
    subfolders = []
    modules = []
    
    # Process Python files in this folder
    for py_file in sorted(source_folder.glob("*.py")):
        if py_file.name.startswith('__'):
            continue
            
        module_name, module_data = process_module(py_file, repo_root)
        
        if module_data and (module_data['classes'] or module_data['functions']):
            modules.append(py_file.stem)
            
            # Calculate doc_path for cross-references
            try:
                rel_output = output_folder.relative_to(output_folder.parents[len(output_folder.parts) - output_folder.parts.index('api') - 2])
                doc_path = str(rel_output / f"{py_file.stem}.md").replace('\\', '/')
            except (ValueError, IndexError):
                doc_path = f"{py_file.stem}.md"
            
            # Write module documentation with cross-reference links
            # Pass parent package name for navigation
            parent_package = source_folder.name
            module_md = generate_module_page(module_name, module_data, doc_path, parent_package)
            module_output = output_folder / f"{py_file.stem}.md"
            with open(module_output, 'w', encoding='utf-8') as f:
                f.write(module_md)
            
            # Write source code page
            source_md = generate_source_page(module_name, module_data['path'], module_data['source_code'])
            source_output = output_folder / f"{py_file.stem}_source.md"
            with open(source_output, 'w', encoding='utf-8') as f:
                f.write(source_md)
    
    # Process subfolders recursively
    for subfolder in sorted(source_folder.iterdir()):
        if not subfolder.is_dir():
            continue
        if subfolder.name.startswith(('__', '.', 'build', 'dist', 'egg-info')):
            continue
        if subfolder.name in ('__pycache__', '.git', 'node_modules'):
            continue
            
        # Check if folder contains any Python files (directly or in subfolders)
        has_python = any(subfolder.rglob("*.py"))
        if not has_python:
            continue
            
        subfolders.append(subfolder.name)
        sub_output = output_folder / subfolder.name
        
        # Recursively process subfolder
        sub_subfolders, sub_modules = process_folder_recursive(
            subfolder, sub_output, repo_root, processed_paths
        )
        
        # Generate index for subfolder
        index_md = generate_folder_index(subfolder.name, sub_subfolders, sub_modules, 
                                         output_folder=sub_output)
        with open(sub_output / "index.md", 'w', encoding='utf-8') as f:
            f.write(index_md)
    
    return subfolders, modules


def remove_stale_api_directories(output_path: Path, repo_root: Path):
    """Remove API output directories that no longer have corresponding source packages.

    This ensures that renamed or deleted packages don't leave stale documentation
    (including .mmd diagram files) in the output directory.
    """
    source_roots = {
        'Distributed_Design_Optimizer': repo_root / 'Distributed_Design_Optimizer',
        'userfiles': repo_root / 'userfiles',
    }

    for top_dir_name, source_root in source_roots.items():
        top_output = output_path / top_dir_name
        if top_output.exists() and source_root.exists():
            _remove_stale_dirs_recursive(top_output, source_root)


def _remove_stale_dirs_recursive(output_dir: Path, source_dir: Path):
    """Recursively remove output subdirectories whose corresponding source no longer exists."""
    import shutil
    for item in list(output_dir.iterdir()):
        if item.is_dir():
            corresponding_source = source_dir / item.name
            if not corresponding_source.exists() or not corresponding_source.is_dir():
                # Source package no longer exists - remove entirely (including .mmd files)
                shutil.rmtree(item, ignore_errors=True)
            else:
                # Source exists - recurse to check deeper levels
                _remove_stale_dirs_recursive(item, corresponding_source)


def clean_output_directory(output_path: Path):
    """Clean the output directory, preserving .mmd Mermaid diagram files."""
    if output_path.exists():
        for item in output_path.iterdir():
            if item.is_dir():
                # Recursively clean subdirectories
                clean_directory_preserve_mermaid(item)
            elif item.suffix != '.mmd':
                try:
                    item.unlink()
                except PermissionError:
                    pass  # Skip locked files, will be overwritten


def clean_directory_preserve_mermaid(dir_path: Path):
    """Recursively clean directory but preserve .mmd Mermaid diagram files."""
    for item in dir_path.iterdir():
        if item.is_dir():
            clean_directory_preserve_mermaid(item)
            # Remove empty directories
            try:
                if not any(item.iterdir()):
                    item.rmdir()
            except (PermissionError, OSError):
                pass
        elif item.suffix != '.mmd':
            try:
                item.unlink()
            except PermissionError:
                pass  # Skip locked files, will be overwritten


def main():
    global CLASS_REGISTRY, SYNTAX_ERRORS, LICENSE_ISSUES, DOCSTRING_ISSUES, FILES_CHECKED, CLASSES_CHECKED, FUNCTIONS_CHECKED
    
    # Paths
    script_dir = Path(__file__).parent
    docs_src = script_dir.parent
    repo_root = docs_src.parent
    output_path = docs_src / "content" / "api"
    
    # Load license header from file (must be done before processing modules)
    load_license_header(repo_root)
    
    # Load docstring style rules from file (must be done before processing modules)
    load_docstring_style(repo_root)
    
    # Remove stale directories for packages that no longer exist in source
    remove_stale_api_directories(output_path, repo_root)
    
    # Clean output directory (preserve .mmd Mermaid diagram files)
    clean_output_directory(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Reset class registry and validation tracking
    CLASS_REGISTRY.clear()
    SYNTAX_ERRORS.clear()
    LICENSE_ISSUES.clear()
    DOCSTRING_ISSUES.clear()
    FILES_CHECKED = 0
    CLASSES_CHECKED = 0
    FUNCTIONS_CHECKED = 0
    
    # === PASS 1: Collect all classes to build cross-reference registry ===
    ddo_source = repo_root / "Distributed_Design_Optimizer"
    userfiles_source = repo_root / "userfiles"
    
    if ddo_source.exists():
        ddo_output = output_path / "Distributed_Design_Optimizer"
        collect_classes_recursive(ddo_source, ddo_output, repo_root)
    
    if userfiles_source.exists():
        userfiles_output = output_path / "userfiles"
        collect_classes_recursive(userfiles_source, userfiles_output, repo_root)
    
    # === PASS 2: Generate documentation with cross-reference links ===
    sections = {}
    
    # Process Distributed_Design_Optimizer package
    if ddo_source.exists():
        ddo_output = output_path / "Distributed_Design_Optimizer"
        subfolders, modules = process_folder_recursive(ddo_source, ddo_output, repo_root)
        sections['Distributed_Design_Optimizer'] = (subfolders, modules)
        
        # Generate index for Distributed_Design_Optimizer
        index_md = generate_folder_index(
            "Distributed_Design_Optimizer", 
            subfolders, 
            modules,
            "Core package for distributed multidisciplinary design optimization.",
            output_folder=ddo_output
        )
        with open(ddo_output / "index.md", 'w', encoding='utf-8') as f:
            f.write(index_md)
    
    # Process userfiles
    if userfiles_source.exists():
        userfiles_output = output_path / "userfiles"
        subfolders, modules = process_folder_recursive(userfiles_source, userfiles_output, repo_root)
        sections['userfiles'] = (subfolders, modules)
        
        # Generate index for userfiles
        index_md = generate_folder_index(
            "userfiles", 
            subfolders, 
            modules,
            "Example configurations and user-defined subsystem implementations.",
            output_folder=userfiles_output
        )
        with open(userfiles_output / "index.md", 'w', encoding='utf-8') as f:
            f.write(index_md)
    
    # Generate main API index
    main_index = """---
title: API Reference
---

# API Reference

Complete API documentation auto-generated from source code.

## Packages

### Core Package

- [Distributed_Design_Optimizer](Distributed_Design_Optimizer/index.md) - Core package for distributed multidisciplinary design optimization

### Examples and User Files

- [userfiles](userfiles/index.md) - Example configurations and user-defined subsystem implementations
"""
    
    with open(output_path / "index.md", 'w', encoding='utf-8') as f:
        f.write(main_index)
    
    # Generate validation report
    generate_validation_report(docs_src)


if __name__ == "__main__":
    main()
