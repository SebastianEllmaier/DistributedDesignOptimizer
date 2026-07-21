# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
# <AUTOGEN_INIT>
from typing import TYPE_CHECKING

# Static type-checking imports for Pylance / mypy.
# The lazy __getattr__ pattern below defers actual imports to runtime for performance,
# but Pylance cannot statically resolve types from __getattr__-based exports. This
# causes type hints (e.g. inherited methods) to appear unresolved in the IDE.
# The TYPE_CHECKING guard provides the type information Pylance needs while being
# completely invisible at runtime -- it does not interfere with beartype or any other
# runtime type-checking, since TYPE_CHECKING is always False outside static analysis.
# Note: the `import X as X` form is required per PEP 484 to signal an explicit
# re-export; without it, Pylance treats the import as private to this module.
if TYPE_CHECKING:
    from Distributed_Design_Optimizer.subsystem.ControllerSubSystemALADIN import ControllerSubSystemALADIN as ControllerSubSystemALADIN
    from Distributed_Design_Optimizer.subsystem.ControllerSubSystemBasis import ControllerSubSystemBasis as ControllerSubSystemBasis
    from Distributed_Design_Optimizer.subsystem.LocalSubSystemALADIN import LocalSubSystemALADIN as LocalSubSystemALADIN
    from Distributed_Design_Optimizer.subsystem.LocalSubSystemALC import LocalSubSystemALC as LocalSubSystemALC
    from Distributed_Design_Optimizer.subsystem.LocalSubSystemBasis import LocalSubSystemBasis as LocalSubSystemBasis
    from Distributed_Design_Optimizer.subsystem.LocalSubSystemConsensusALC import LocalSubSystemConsensusALC as LocalSubSystemConsensusALC
    from Distributed_Design_Optimizer.subsystem.LocalSubSystemLC import LocalSubSystemLC as LocalSubSystemLC
    from Distributed_Design_Optimizer.subsystem.LocalSubSystemPC import LocalSubSystemPC as LocalSubSystemPC
    from Distributed_Design_Optimizer.subsystem.LocalSubSystemSBDP import LocalSubSystemSBDP as LocalSubSystemSBDP
    from Distributed_Design_Optimizer.subsystem.SubSystemBasis import SubSystemBasis as SubSystemBasis
    from Distributed_Design_Optimizer.subsystem.SubSystemInterface import SubSystemInterface as SubSystemInterface

_LAZY_IMPORTS = {
    'ControllerSubSystemALADIN': 'Distributed_Design_Optimizer.subsystem.ControllerSubSystemALADIN',
    'ControllerSubSystemBasis': 'Distributed_Design_Optimizer.subsystem.ControllerSubSystemBasis',
    'LocalSubSystemALADIN': 'Distributed_Design_Optimizer.subsystem.LocalSubSystemALADIN',
    'LocalSubSystemALC': 'Distributed_Design_Optimizer.subsystem.LocalSubSystemALC',
    'LocalSubSystemBasis': 'Distributed_Design_Optimizer.subsystem.LocalSubSystemBasis',
    'LocalSubSystemConsensusALC': 'Distributed_Design_Optimizer.subsystem.LocalSubSystemConsensusALC',
    'LocalSubSystemLC': 'Distributed_Design_Optimizer.subsystem.LocalSubSystemLC',
    'LocalSubSystemPC': 'Distributed_Design_Optimizer.subsystem.LocalSubSystemPC',
    'LocalSubSystemSBDP': 'Distributed_Design_Optimizer.subsystem.LocalSubSystemSBDP',
    'SubSystemBasis': 'Distributed_Design_Optimizer.subsystem.SubSystemBasis',
    'SubSystemInterface': 'Distributed_Design_Optimizer.subsystem.SubSystemInterface',
}


def __getattr__(name):
    if name in _LAZY_IMPORTS:
        import importlib
        module = importlib.import_module(_LAZY_IMPORTS[name])
        value = getattr(module, name)
        if isinstance(value, type):
            value.__module__ = __name__  # help dill locate the class via the package
        globals()[name] = value  # cache for subsequent access
        return value
    # Allow Python to resolve submodules (e.g. _plot_builder) not in _LAZY_IMPORTS
    if not name.startswith('__'):
        try:
            import importlib
            return importlib.import_module(f'{__name__}.{name}')
        except ImportError:
            pass
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')

# Patch co_filename so debugpy treats __getattr__ as non-user code and does
# not break on AttributeError for dunder probes like __wrapped__.
__getattr__.__code__ = __getattr__.__code__.replace(
    co_filename='<frozen importlib._bootstrap>')

import types as _types
import sys as _sys

class _LazyClassModule(_types.ModuleType):
    _ModuleType = _types.ModuleType  # bind before del
    def __setattr__(self, name, value):
        # When Python imports a submodule (e.g. ClassName.py), it calls
        # setattr(package, 'ClassName', <module>). If ClassName is in
        # _LAZY_IMPORTS, resolve the class from the module instead.
        if isinstance(value, _LazyClassModule._ModuleType):
            lazy = self.__dict__.get('_LAZY_IMPORTS', {})
            if name in lazy:
                try:
                    resolved = getattr(value, name)
                    if isinstance(resolved, type):
                        resolved.__module__ = self.__name__
                    super().__setattr__(name, resolved)
                    return
                except (AttributeError, RecursionError):
                    pass  # fall through to normal setattr
        super().__setattr__(name, value)

_sys.modules[__name__].__class__ = _LazyClassModule
del _types, _sys

__all__ = ['ControllerSubSystemALADIN', 'ControllerSubSystemBasis', 'LocalSubSystemALADIN', 'LocalSubSystemALC', 'LocalSubSystemBasis', 'LocalSubSystemConsensusALC', 'LocalSubSystemLC', 'LocalSubSystemPC', 'LocalSubSystemSBDP', 'SubSystemBasis', 'SubSystemInterface']
# </AUTOGEN_INIT>
