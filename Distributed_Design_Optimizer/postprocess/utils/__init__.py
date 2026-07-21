
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
    from Distributed_Design_Optimizer.postprocess.utils.graph_utils import CLUSTER_PALETTE as CLUSTER_PALETTE
    from Distributed_Design_Optimizer.postprocess.utils.graph_utils import EDGE_TYPE_COLORS as EDGE_TYPE_COLORS
    from Distributed_Design_Optimizer.postprocess.utils.FlexibleUnpickler import FlexibleUnpickler as FlexibleUnpickler
    from Distributed_Design_Optimizer.postprocess.utils.graph_utils import NODE_TYPE_COLORS as NODE_TYPE_COLORS
    from Distributed_Design_Optimizer.postprocess.utils.graph_utils import NODE_TYPE_SHAPES as NODE_TYPE_SHAPES
    from Distributed_Design_Optimizer.postprocess.utils.graph_utils import NODE_TYPE_SIZES as NODE_TYPE_SIZES
    from Distributed_Design_Optimizer.postprocess.utils.graph_utils import build_edges as build_edges
    from Distributed_Design_Optimizer.postprocess.utils.graph_utils import green_yellow_red as green_yellow_red
    from Distributed_Design_Optimizer.postprocess.utils.graph_utils import hierarchical_layout as hierarchical_layout
    from Distributed_Design_Optimizer.postprocess.utils.FlexibleUnpickler import logger as logger
    from Distributed_Design_Optimizer.postprocess.utils.graph_utils import safe_edge_iter as safe_edge_iter

_LAZY_IMPORTS = {
    'CLUSTER_PALETTE': 'Distributed_Design_Optimizer.postprocess.utils.graph_utils',
    'EDGE_TYPE_COLORS': 'Distributed_Design_Optimizer.postprocess.utils.graph_utils',
    'FlexibleUnpickler': 'Distributed_Design_Optimizer.postprocess.utils.FlexibleUnpickler',
    'NODE_TYPE_COLORS': 'Distributed_Design_Optimizer.postprocess.utils.graph_utils',
    'NODE_TYPE_SHAPES': 'Distributed_Design_Optimizer.postprocess.utils.graph_utils',
    'NODE_TYPE_SIZES': 'Distributed_Design_Optimizer.postprocess.utils.graph_utils',
    'build_edges': 'Distributed_Design_Optimizer.postprocess.utils.graph_utils',
    'green_yellow_red': 'Distributed_Design_Optimizer.postprocess.utils.graph_utils',
    'hierarchical_layout': 'Distributed_Design_Optimizer.postprocess.utils.graph_utils',
    'logger': 'Distributed_Design_Optimizer.postprocess.utils.FlexibleUnpickler',
    'safe_edge_iter': 'Distributed_Design_Optimizer.postprocess.utils.graph_utils',
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

__all__ = ['CLUSTER_PALETTE', 'EDGE_TYPE_COLORS', 'FlexibleUnpickler', 'NODE_TYPE_COLORS', 'NODE_TYPE_SHAPES', 'NODE_TYPE_SIZES', 'build_edges', 'green_yellow_red', 'hierarchical_layout', 'logger', 'safe_edge_iter']
# </AUTOGEN_INIT>
