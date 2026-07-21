# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""Flexible unpickler that handles lazy-import module/class shadowing."""

import sys
import types
import typing
import importlib
import logging

import dill

logger = logging.getLogger(__name__)


class FlexibleUnpickler(dill.Unpickler):
    """Custom unpickler that handles lazy-import module/class shadowing.

    When DDO subsystem classes are serialized, the unpickler may encounter
    module-level names that have been replaced by lazy-import proxies.
    This class repairs those before resolving.
    """

    def find_class(self, module: str, name: str) -> typing.Any:
        """Find a class/callable, repairing lazy-import shadowing first.

        Args:
            module: Fully-qualified module path of the pickled object.
            name: Class or callable name to resolve within the module.

        Returns:
            The resolved class or callable object.
        """
        self._fix_lazy_import_shadowing(module)
        try:
            return super().find_class(module, name)
        except Exception:
            return self._search_for_class(module, name)

    _fixed_modules: set = set()

    @staticmethod
    def _fix_lazy_import_shadowing(module_path: str) -> None:
        """Replace module objects that shadow lazy class exports."""
        if module_path in FlexibleUnpickler._fixed_modules:
            return
        for pkg_path, pkg in list(sys.modules.items()):
            if not pkg_path.startswith("Distributed_Design_Optimizer"):
                continue
            lazy = getattr(pkg, "_LAZY_IMPORTS", None)
            if not lazy:
                continue
            for cls_name in lazy:
                attr = pkg.__dict__.get(cls_name)
                if isinstance(attr, types.ModuleType):
                    real_cls = getattr(attr, cls_name, None)
                    if real_cls is not None and not isinstance(real_cls, types.ModuleType):
                        setattr(pkg, cls_name, real_cls)
        FlexibleUnpickler._fixed_modules.add(module_path)

    @staticmethod
    def _search_for_class(original_module: str, name: str) -> typing.Any:
        """Search for *name* after the normal import failed."""
        parts = original_module.split(".")
        FlexibleUnpickler._fix_lazy_import_shadowing(original_module)

        # Strategy 1: Check sys.modules
        mod = sys.modules.get(original_module)
        if mod is not None:
            cls = getattr(mod, name, None)
            if cls is not None and not isinstance(cls, types.ModuleType):
                return cls

        # Strategy 2: Walk parent packages
        for i in range(len(parts), 0, -1):
            candidate = ".".join(parts[:i])
            try:
                mod = sys.modules.get(candidate)
                if mod is None:
                    mod = importlib.import_module(candidate)
                attr = getattr(mod, name, None)
                if attr is None:
                    continue
                if isinstance(attr, types.ModuleType):
                    real = getattr(attr, name, None)
                    if real is not None and not isinstance(real, types.ModuleType):
                        return real
                else:
                    return attr
            except Exception:
                continue

        raise ImportError(
            f"Cannot find class '{name}' (originally from '{original_module}')"
        )
