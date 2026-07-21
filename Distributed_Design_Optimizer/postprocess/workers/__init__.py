
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
    from Distributed_Design_Optimizer.postprocess.workers.AutoUpdateWorker import AutoUpdateWorker as AutoUpdateWorker
    from Distributed_Design_Optimizer.postprocess.workers.CallableWorker import CallableWorker as CallableWorker
    from Distributed_Design_Optimizer.postprocess.workers.FileLoaderWorker import FileLoaderWorker as FileLoaderWorker
    from Distributed_Design_Optimizer.postprocess.workers.LLMWorker import LLMWorker as LLMWorker
    from Distributed_Design_Optimizer.postprocess.workers.TopologyWorker import TopologyWorker as TopologyWorker
    from Distributed_Design_Optimizer.postprocess.workers.AutoUpdateWorker import logger as logger

_LAZY_IMPORTS = {
    'AutoUpdateWorker': 'Distributed_Design_Optimizer.postprocess.workers.AutoUpdateWorker',
    'CallableWorker': 'Distributed_Design_Optimizer.postprocess.workers.CallableWorker',
    'FileLoaderWorker': 'Distributed_Design_Optimizer.postprocess.workers.FileLoaderWorker',
    'LLMWorker': 'Distributed_Design_Optimizer.postprocess.workers.LLMWorker',
    'TopologyWorker': 'Distributed_Design_Optimizer.postprocess.workers.TopologyWorker',
    'logger': 'Distributed_Design_Optimizer.postprocess.workers.AutoUpdateWorker',
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

__all__ = ['AutoUpdateWorker', 'CallableWorker', 'FileLoaderWorker', 'LLMWorker', 'TopologyWorker', 'logger']
# </AUTOGEN_INIT>
