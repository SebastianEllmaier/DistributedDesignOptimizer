# Distributed Design Optimizer - PySide6 Post-Processing GUI
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
    from Distributed_Design_Optimizer.postprocess.CentralityComputer import CentralityComputer as CentralityComputer
    from Distributed_Design_Optimizer.postprocess.ClusterComputer import ClusterComputer as ClusterComputer
    from Distributed_Design_Optimizer.postprocess.CompromiseComputer import CompromiseComputer as CompromiseComputer
    from Distributed_Design_Optimizer.postprocess.CouplingStrengthComputer import CouplingStrengthComputer as CouplingStrengthComputer
    from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_BORDER as DDO_BORDER
    from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_BORDER_WIDTH as DDO_BORDER_WIDTH
    from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color as DDO_Color
    from Distributed_Design_Optimizer.postprocess.GraphInit import GraphInit as GraphInit
    from Distributed_Design_Optimizer.postprocess.InConsistencyOscillationComputer import InConsistencyOscillationComputer as InConsistencyOscillationComputer
    from Distributed_Design_Optimizer.postprocess.JacobianComputer import JacobianComputer as JacobianComputer
    from Distributed_Design_Optimizer.postprocess.PerformanceMetrics import PerformanceMetrics as PerformanceMetrics
    from Distributed_Design_Optimizer.postprocess.terminal_print_tools import Reset as Reset
    from Distributed_Design_Optimizer.postprocess.ResidualComputer import ResidualComputer as ResidualComputer
    from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print as ddo_print
    from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print_border as ddo_print_border
    from Distributed_Design_Optimizer.postprocess.App import main as main

_LAZY_IMPORTS = {
    'CentralityComputer': 'Distributed_Design_Optimizer.postprocess.CentralityComputer',
    'ClusterComputer': 'Distributed_Design_Optimizer.postprocess.ClusterComputer',
    'CompromiseComputer': 'Distributed_Design_Optimizer.postprocess.CompromiseComputer',
    'CouplingStrengthComputer': 'Distributed_Design_Optimizer.postprocess.CouplingStrengthComputer',
    'DDO_BORDER': 'Distributed_Design_Optimizer.postprocess.terminal_print_tools',
    'DDO_BORDER_WIDTH': 'Distributed_Design_Optimizer.postprocess.terminal_print_tools',
    'DDO_Color': 'Distributed_Design_Optimizer.postprocess.terminal_print_tools',
    'GraphInit': 'Distributed_Design_Optimizer.postprocess.GraphInit',
    'InConsistencyOscillationComputer': 'Distributed_Design_Optimizer.postprocess.InConsistencyOscillationComputer',
    'JacobianComputer': 'Distributed_Design_Optimizer.postprocess.JacobianComputer',
    'PerformanceMetrics': 'Distributed_Design_Optimizer.postprocess.PerformanceMetrics',
    'Reset': 'Distributed_Design_Optimizer.postprocess.terminal_print_tools',
    'ResidualComputer': 'Distributed_Design_Optimizer.postprocess.ResidualComputer',
    'ddo_print': 'Distributed_Design_Optimizer.postprocess.terminal_print_tools',
    'ddo_print_border': 'Distributed_Design_Optimizer.postprocess.terminal_print_tools',
    'main': 'Distributed_Design_Optimizer.postprocess.App',
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

__all__ = ['CentralityComputer', 'ClusterComputer', 'CompromiseComputer', 'CouplingStrengthComputer', 'DDO_BORDER', 'DDO_BORDER_WIDTH', 'DDO_Color', 'GraphInit', 'InConsistencyOscillationComputer', 'JacobianComputer', 'PerformanceMetrics', 'Reset', 'ResidualComputer', 'ddo_print', 'ddo_print_border', 'main']
# </AUTOGEN_INIT>
