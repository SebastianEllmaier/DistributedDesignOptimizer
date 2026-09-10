---
title: generate_inits (Source)
---

← Back to [generate_inits documentation](generate_inits.md)

# generate_inits - Source Code

**File:** `Distributed_Design_Optimizer\generate_inits.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Script to auto-generate __init__.py files for the Distributed_Design_Optimizer package.

Uses AST parsing to discover public classes/functions from each package's direct .py
submodules ONLY (not from subpackages), then generates lazy imports via __getattr__
with a custom module __class__ to handle submodule name collisions.

Problem: When ClassName.py defines class ClassName, `from package import ClassName`
resolves the submodule file rather than calling __getattr__, so beartype sees a module
object instead of the class. The fix: a custom module subclass overrides
__getattribute__ to detect when a submodule would be returned for a name in
_LAZY_IMPORTS, and lazily resolves the class instead.

This means you can do:
    from Distributed_Design_Optimizer.coordination.multilevelmethod import ALC, PC, LC
but NOT:
    from Distributed_Design_Optimizer.coordination import ALC

Each level only re-exports what is defined in its own .py files.

Usage:
    python -m Distributed_Design_Optimizer.generate_inits          # generate all __init__.py files
    python -m Distributed_Design_Optimizer.generate_inits --dry    # preview without writing

Notes:
    - Preserves everything outside the <AUTOGEN_INIT> tags (e.g. beartype_this_package())
    - Creates missing __init__.py files with proper headers
    - Safe to re-run at any time after adding/removing modules
    - Uses lazy imports with module __class__ override to avoid both circular imports
      and submodule name collisions with beartype
"""
import os
import sys
import re
import ast
import argparse
import warnings

# __file__ is inside Distributed_Design_Optimizer/, so go up one level for repo root
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

PACKAGE_ROOT = os.path.join(REPO_ROOT, "Distributed_Design_Optimizer")
USERFILES_ROOT = os.path.join(REPO_ROOT, "userfiles")

HEADER = """\
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""

AUTOGEN_OPEN = "# <AUTOGEN_INIT>"
AUTOGEN_CLOSE = "# </AUTOGEN_INIT>"


def find_all_packages(root):
    """Find all directories under root that are (or should be) Python packages.

    Args:
        root: Root directory path to search for packages.
    """
    packages = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip __pycache__, build, and hidden directories
        dirnames[:] = [d for d in dirnames if not d.startswith(('.', '__')) and d != 'build']
        # A directory is a package if it has .py files or subdirectories with .py files
        has_py = any(f.endswith('.py') and f != '__init__.py' for f in filenames)
        has_subpackages = any(
            os.path.isfile(os.path.join(dirpath, d, '__init__.py'))
            for d in dirnames
        )
        if has_py or has_subpackages:
            packages.append(dirpath)
    return packages


def ensure_init_with_tags(package_dir):
    """Ensure __init__.py exists and contains AUTOGEN_INIT tags.

    Args:
        package_dir: Path to the package directory.
    """
    init_path = os.path.join(package_dir, "__init__.py")

    if not os.path.exists(init_path):
        # Create new __init__.py with header and tags
        content = f"{HEADER}{AUTOGEN_OPEN}\n{AUTOGEN_CLOSE}\n"
        with open(init_path, 'w') as f:
            f.write(content)
        warnings.warn(f"generate_inits: Created {os.path.relpath(init_path, REPO_ROOT)}")
        return

    # Read existing content
    with open(init_path, 'r') as f:
        content = f.read()

    # If tags already present, nothing to do
    if AUTOGEN_OPEN in content:
        return

    # Add tags at the end, preserving existing content
    if not content.endswith('\n'):
        content += '\n'
    content += f"{AUTOGEN_OPEN}\n{AUTOGEN_CLOSE}\n"
    with open(init_path, 'w') as f:
        f.write(content)
    warnings.warn(f"generate_inits: Added AUTOGEN tags to {os.path.relpath(init_path, REPO_ROOT)}")


def get_package_dotpath(package_dir):
    """Convert a filesystem path to a Python dotted module path.

    Args:
        package_dir: Filesystem path to the package directory.
    """
    relpath = os.path.relpath(package_dir, REPO_ROOT)
    return relpath.replace(os.sep, '.')


def get_module_names(package_dir):
    """Get names of direct .py submodules (without .py extension).

    Args:
        package_dir: Path to the package directory.
    """
    modules = set()
    for name in os.listdir(package_dir):
        if name.endswith('.py') and name != '__init__.py' and name != 'generate_inits.py':
            modules.add(name[:-3])
    return modules


def get_public_names_from_module(module_path):
    """Extract public class/function/variable names from a .py file using AST.

    Returns a list of public names defined at module level.

    Args:
        module_path: Filesystem path to the .py file.
    """
    try:
        with open(module_path, 'r', encoding='utf-8') as f:
            source = f.read()
    except (OSError, UnicodeDecodeError):
        return []

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    # Check for explicit __all__
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == '__all__':
                    if isinstance(node.value, (ast.List, ast.Tuple)):
                        names = []
                        for elt in node.value.elts:
                            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                names.append(elt.value)
                        if names:
                            return names

    # No __all__, collect public top-level definitions
    names = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith('_'):
                names.append(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and not target.id.startswith('_'):
                    names.append(target.id)

    return names


def generate_lazy_init_content(package_dir):
    """Generate lazy import __init__.py content for a package.

    Uses __getattr__ for lazy resolution (avoids circular imports) combined
    with a custom module __class__ override (__getattribute__) that intercepts
    submodule objects being returned for names in _LAZY_IMPORTS, resolving the
    class instead. This handles the Python quirk where `from package import X`
    returns the submodule when X.py exists, bypassing __getattr__.
    Includes TYPE_CHECKING imports for Pylance/mypy static analysis.

    Args:
        package_dir: Path to the package directory.
    """
    pkg_dotpath = get_package_dotpath(package_dir)
    module_names = sorted(get_module_names(package_dir))

    # Build mapping: public_name -> module_name
    name_to_module = {}
    all_names = []

    for mod_name in module_names:
        mod_path = os.path.join(package_dir, mod_name + '.py')
        public_names = get_public_names_from_module(mod_path)
        for name in public_names:
            if name not in name_to_module:
                name_to_module[name] = mod_name
                all_names.append(name)

    if not name_to_module:
        return None

    # Generate the lazy import code
    lines = []

    # Generate TYPE_CHECKING block for static analysis (Pylance / mypy).
    # The lazy __getattr__ pattern defers imports to runtime for performance,
    # but Pylance cannot statically resolve types from __getattr__-based exports.
    # The TYPE_CHECKING guard provides type information to static analyzers while
    # being completely invisible at runtime — it does not interfere with beartype
    # or any other runtime type-checking, since TYPE_CHECKING is always False
    # outside static analysis.
    lines.append("from typing import TYPE_CHECKING")
    lines.append("")
    lines.append("# Static type-checking imports for Pylance / mypy.")
    lines.append("# The lazy __getattr__ pattern below defers actual imports to runtime for performance,")
    lines.append("# but Pylance cannot statically resolve types from __getattr__-based exports. This")
    lines.append("# causes type hints (e.g. inherited methods) to appear unresolved in the IDE.")
    lines.append("# The TYPE_CHECKING guard provides the type information Pylance needs while being")
    lines.append("# completely invisible at runtime -- it does not interfere with beartype or any other")
    lines.append("# runtime type-checking, since TYPE_CHECKING is always False outside static analysis.")
    lines.append("# Note: the `import X as X` form is required per PEP 484 to signal an explicit")
    lines.append("# re-export; without it, Pylance treats the import as private to this module.")
    lines.append("if TYPE_CHECKING:")
    # Use `import X as X` form to signal explicit re-export per PEP 484.
    # Without the `as X`, Pylance treats the import as private to this module
    # and won't re-export it to consumers (e.g. `from package import MyClass`).
    for name in sorted(name_to_module.keys()):
        mod = name_to_module[name]
        lines.append(f"    from {pkg_dotpath}.{mod} import {name} as {name}")
    lines.append("")

    # Build the _LAZY_IMPORTS mapping
    lines.append("_LAZY_IMPORTS = {")
    for name in sorted(name_to_module.keys()):
        mod = name_to_module[name]
        lines.append(f"    '{name}': '{pkg_dotpath}.{mod}',")
    lines.append("}")
    lines.append("")

    # Generate __getattr__ for lazy resolution (avoids circular imports)
    #
    # After defining __getattr__, we patch its co_filename to a frozen-module
    # path so that debugpy classifies it as non-user code.  This prevents
    # the debugger's "Raised Exceptions" breakpoint from firing when Python
    # probes dunder attributes like __wrapped__ (beartype) that don't exist.
    lines.append("")
    lines.append("def __getattr__(name):")
    lines.append("    if name in _LAZY_IMPORTS:")
    lines.append("        import importlib")
    lines.append("        module = importlib.import_module(_LAZY_IMPORTS[name])")
    lines.append("        value = getattr(module, name)")
    lines.append("        if isinstance(value, type):")
    lines.append("            value.__module__ = __name__  # help dill locate the class via the package")
    lines.append("        globals()[name] = value  # cache for subsequent access")
    lines.append("        return value")
    lines.append("    # Allow Python to resolve submodules (e.g. _plot_builder) not in _LAZY_IMPORTS")
    lines.append("    if not name.startswith('__'):")
    lines.append("        try:")
    lines.append("            import importlib")
    lines.append("            return importlib.import_module(f'{__name__}.{name}')")
    lines.append("        except ImportError:")
    lines.append("            pass")
    lines.append("    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')")
    lines.append("")
    lines.append("# Patch co_filename so debugpy treats __getattr__ as non-user code and does")
    lines.append("# not break on AttributeError for dunder probes like __wrapped__.")
    lines.append("__getattr__.__code__ = __getattr__.__code__.replace(")
    lines.append("    co_filename='<frozen importlib._bootstrap>')")
    lines.append("")

    # Generate module __class__ override using __setattr__ to handle submodule
    # name collisions WITHOUT __getattribute__.
    #
    # Problem: When ClassName.py defines class ClassName, `from package import ClassName`
    # causes Python to import the .py file as a submodule, then call
    # setattr(package, 'ClassName', <module>). After that, __getattr__ is never
    # called because the attribute already exists as a module.
    #
    # Fix: Override __setattr__ to intercept when Python sets a submodule on
    # the package for a name in _LAZY_IMPORTS. Instead of storing the module,
    # resolve the class from it immediately.
    #
    # This avoids __getattribute__ entirely, which means no user-code frame
    # is on the stack for dunder probes like __wrapped__, so the debugger's
    # "Raised Exceptions" breakpoint is never triggered by those.
    lines.append("import types as _types")
    lines.append("import sys as _sys")
    lines.append("")
    lines.append("class _LazyClassModule(_types.ModuleType):")
    lines.append("    _ModuleType = _types.ModuleType  # bind before del")
    lines.append("    def __setattr__(self, name, value):")
    lines.append("        # When Python imports a submodule (e.g. ClassName.py), it calls")
    lines.append("        # setattr(package, 'ClassName', <module>). If ClassName is in")
    lines.append("        # _LAZY_IMPORTS, resolve the class from the module instead.")
    lines.append("        if isinstance(value, _LazyClassModule._ModuleType):")
    lines.append("            lazy = self.__dict__.get('_LAZY_IMPORTS', {})")
    lines.append("            if name in lazy:")
    lines.append("                try:")
    lines.append("                    resolved = getattr(value, name)")
    lines.append("                    if isinstance(resolved, type):")
    lines.append("                        resolved.__module__ = self.__name__")
    lines.append("                    super().__setattr__(name, resolved)")
    lines.append("                    return")
    lines.append("                except (AttributeError, RecursionError):")
    lines.append("                    pass  # fall through to normal setattr")
    lines.append("        super().__setattr__(name, value)")
    lines.append("")
    lines.append("_sys.modules[__name__].__class__ = _LazyClassModule")
    lines.append("del _types, _sys")
    lines.append("")

    # Generate __all__
    all_str = ', '.join(f"'{n}'" for n in sorted(all_names))
    lines.append(f"__all__ = [{all_str}]")

    return '\n'.join(lines)


def update_init_file(init_path, autogen_content):
    """Replace the AUTOGEN section in an __init__.py file.

    Args:
        init_path: Path to the __init__.py file.
        autogen_content: The new autogenerated content to insert.
    """
    with open(init_path, 'r') as f:
        content = f.read()

    new_section = f"{AUTOGEN_OPEN}\n{autogen_content}\n{AUTOGEN_CLOSE}"
    content = re.sub(
        rf"{re.escape(AUTOGEN_OPEN)}.*?{re.escape(AUTOGEN_CLOSE)}",
        new_section,
        content,
        flags=re.DOTALL,
    )
    with open(init_path, 'w') as f:
        f.write(content)


def main(dry=False):
    """Generate lazy-import __init__.py files for all packages.

    Args:
        dry: If True, perform a dry run without writing files.
    """
    packages = find_all_packages(PACKAGE_ROOT)
    # Also include the root package itself
    if PACKAGE_ROOT not in packages:
        packages.insert(0, PACKAGE_ROOT)

    for pkg_dir in packages:
        ensure_init_with_tags(pkg_dir)

    for pkg_dir in packages:
        init_path = os.path.join(pkg_dir, "__init__.py")

        # Skip the top-level package (handled separately)
        if pkg_dir == PACKAGE_ROOT:
            continue

        autogen_content = generate_lazy_init_content(pkg_dir)
        if autogen_content is None:
            continue

        if not dry:
            update_init_file(init_path, autogen_content)

    # The top-level package only re-exports its direct subpackages
    top_init_path = os.path.join(PACKAGE_ROOT, "__init__.py")
    direct_subpackages = [
        d for d in os.listdir(PACKAGE_ROOT)
        if os.path.isdir(os.path.join(PACKAGE_ROOT, d))
        and not d.startswith(('.', '__'))
        and d != 'build'
        and os.path.isfile(os.path.join(PACKAGE_ROOT, d, '__init__.py'))
    ]
    shallow_imports = "\n".join(
        f"from Distributed_Design_Optimizer import {subpkg}"
        for subpkg in sorted(direct_subpackages)
    )

    with open(top_init_path, 'r') as f:
        content = f.read()

    new_section = f"{AUTOGEN_OPEN}\n{shallow_imports}\n{AUTOGEN_CLOSE}\n"
    content = re.sub(
        rf"{re.escape(AUTOGEN_OPEN)}.*?{re.escape(AUTOGEN_CLOSE)}\n?",
        new_section,
        content,
        flags=re.DOTALL,
    )
    if not dry:
        with open(top_init_path, 'w') as f:
            f.write(content)

    userfiles_packages = find_all_packages(USERFILES_ROOT)

    for pkg_dir in userfiles_packages:
        init_path = os.path.join(pkg_dir, "__init__.py")

        autogen_content = generate_lazy_init_content(pkg_dir)
        if autogen_content is None:
            continue

        # Write clean file: header + AUTOGEN-wrapped content
        full_content = f"{HEADER}{AUTOGEN_OPEN}\n{autogen_content}\n{AUTOGEN_CLOSE}\n"

        if not dry:
            with open(init_path, 'w') as f:
                f.write(full_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto-generate __init__.py files")
    parser.add_argument('--dry', action='store_true', help="Preview without writing")
    args = parser.parse_args()
    main(dry=args.dry)

```
