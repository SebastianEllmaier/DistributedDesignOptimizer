
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
    from Distributed_Design_Optimizer.coordination.convergence.Centralized_ConvergenceIndicator_Innerloop_Basis import Centralized_ConvergenceIndicator_Innerloop_Basis as Centralized_ConvergenceIndicator_Innerloop_Basis
    from Distributed_Design_Optimizer.coordination.convergence.Centralized_ConvergenceIndicator_Innerloop_Interface import Centralized_ConvergenceIndicator_Innerloop_Interface as Centralized_ConvergenceIndicator_Innerloop_Interface
    from Distributed_Design_Optimizer.coordination.convergence.Centralized_ConvergenceIndicator_Outerloop_Basis import Centralized_ConvergenceIndicator_Outerloop_Basis as Centralized_ConvergenceIndicator_Outerloop_Basis
    from Distributed_Design_Optimizer.coordination.convergence.Centralized_ConvergenceIndicator_Outerloop_Interface import Centralized_ConvergenceIndicator_Outerloop_Interface as Centralized_ConvergenceIndicator_Outerloop_Interface
    from Distributed_Design_Optimizer.coordination.convergence.ConvergenceIndicator_Innerloop_Interface import ConvergenceIndicator_Innerloop_Interface as ConvergenceIndicator_Innerloop_Interface
    from Distributed_Design_Optimizer.coordination.convergence.ConvergenceIndicator_Outerloop_Interface import ConvergenceIndicator_Outerloop_Interface as ConvergenceIndicator_Outerloop_Interface
    from Distributed_Design_Optimizer.coordination.convergence.Local_ConvergenceIndicator_Innerloop_Interface import Local_ConvergenceIndicator_Innerloop_Interface as Local_ConvergenceIndicator_Innerloop_Interface
    from Distributed_Design_Optimizer.coordination.convergence.Local_ConvergenceIndicator_Outerloop_Interface import Local_ConvergenceIndicator_Outerloop_Interface as Local_ConvergenceIndicator_Outerloop_Interface

_LAZY_IMPORTS = {
    'Centralized_ConvergenceIndicator_Innerloop_Basis': 'Distributed_Design_Optimizer.coordination.convergence.Centralized_ConvergenceIndicator_Innerloop_Basis',
    'Centralized_ConvergenceIndicator_Innerloop_Interface': 'Distributed_Design_Optimizer.coordination.convergence.Centralized_ConvergenceIndicator_Innerloop_Interface',
    'Centralized_ConvergenceIndicator_Outerloop_Basis': 'Distributed_Design_Optimizer.coordination.convergence.Centralized_ConvergenceIndicator_Outerloop_Basis',
    'Centralized_ConvergenceIndicator_Outerloop_Interface': 'Distributed_Design_Optimizer.coordination.convergence.Centralized_ConvergenceIndicator_Outerloop_Interface',
    'ConvergenceIndicator_Innerloop_Interface': 'Distributed_Design_Optimizer.coordination.convergence.ConvergenceIndicator_Innerloop_Interface',
    'ConvergenceIndicator_Outerloop_Interface': 'Distributed_Design_Optimizer.coordination.convergence.ConvergenceIndicator_Outerloop_Interface',
    'Local_ConvergenceIndicator_Innerloop_Interface': 'Distributed_Design_Optimizer.coordination.convergence.Local_ConvergenceIndicator_Innerloop_Interface',
    'Local_ConvergenceIndicator_Outerloop_Interface': 'Distributed_Design_Optimizer.coordination.convergence.Local_ConvergenceIndicator_Outerloop_Interface',
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

__all__ = ['Centralized_ConvergenceIndicator_Innerloop_Basis', 'Centralized_ConvergenceIndicator_Innerloop_Interface', 'Centralized_ConvergenceIndicator_Outerloop_Basis', 'Centralized_ConvergenceIndicator_Outerloop_Interface', 'ConvergenceIndicator_Innerloop_Interface', 'ConvergenceIndicator_Outerloop_Interface', 'Local_ConvergenceIndicator_Innerloop_Interface', 'Local_ConvergenceIndicator_Outerloop_Interface']
# </AUTOGEN_INIT>

# ---- Re-exports from DeWit/ and AlwaysConverged/ subpackages ----
# These classes were moved into subpackages for organization but must remain
# importable from the parent convergence package for backward compatibility.
if TYPE_CHECKING:
    from Distributed_Design_Optimizer.coordination.convergence.DeWit.ConvergenceIndicator_Innerloop_DeWit import ConvergenceIndicator_Innerloop_DeWit as ConvergenceIndicator_Innerloop_DeWit
    from Distributed_Design_Optimizer.coordination.convergence.DeWit.ConvergenceIndicator_Outerloop_DeWit import ConvergenceIndicator_Outerloop_DeWit as ConvergenceIndicator_Outerloop_DeWit
    from Distributed_Design_Optimizer.coordination.convergence.DeWit.Local_ConvergenceIndicator_Innerloop_DeWit import Local_ConvergenceIndicator_Innerloop_DeWit as Local_ConvergenceIndicator_Innerloop_DeWit
    from Distributed_Design_Optimizer.coordination.convergence.DeWit.Local_ConvergenceIndicator_Outerloop_DeWit import Local_ConvergenceIndicator_Outerloop_DeWit as Local_ConvergenceIndicator_Outerloop_DeWit
    from Distributed_Design_Optimizer.coordination.convergence.DeWit.Centralized_ConvergenceIndicator_Innerloop_DeWit import Centralized_ConvergenceIndicator_Innerloop_DeWit as Centralized_ConvergenceIndicator_Innerloop_DeWit
    from Distributed_Design_Optimizer.coordination.convergence.DeWit.Centralized_ConvergenceIndicator_Outerloop_DeWit import Centralized_ConvergenceIndicator_Outerloop_DeWit as Centralized_ConvergenceIndicator_Outerloop_DeWit
    from Distributed_Design_Optimizer.coordination.convergence.AlwaysConverged.ConvergenceIndicator_Innerloop_AlwaysConverged import ConvergenceIndicator_Innerloop_AlwaysConverged as ConvergenceIndicator_Innerloop_AlwaysConverged
    from Distributed_Design_Optimizer.coordination.convergence.AlwaysConverged.ConvergenceIndicator_Outerloop_AlwaysConverged import ConvergenceIndicator_Outerloop_AlwaysConverged as ConvergenceIndicator_Outerloop_AlwaysConverged
    from Distributed_Design_Optimizer.coordination.convergence.AlwaysConverged.Local_ConvergenceIndicator_Innerloop_AlwaysConverged import Local_ConvergenceIndicator_Innerloop_AlwaysConverged as Local_ConvergenceIndicator_Innerloop_AlwaysConverged
    from Distributed_Design_Optimizer.coordination.convergence.AlwaysConverged.Local_ConvergenceIndicator_Outerloop_AlwaysConverged import Local_ConvergenceIndicator_Outerloop_AlwaysConverged as Local_ConvergenceIndicator_Outerloop_AlwaysConverged
    from Distributed_Design_Optimizer.coordination.convergence.AlwaysConverged.Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged import Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged as Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged
    from Distributed_Design_Optimizer.coordination.convergence.AlwaysConverged.Centralized_ConvergenceIndicator_Outerloop_AlwaysConverged import Centralized_ConvergenceIndicator_Outerloop_AlwaysConverged as Centralized_ConvergenceIndicator_Outerloop_AlwaysConverged

_LAZY_IMPORTS.update({
    'ConvergenceIndicator_Innerloop_DeWit': 'Distributed_Design_Optimizer.coordination.convergence.DeWit.ConvergenceIndicator_Innerloop_DeWit',
    'ConvergenceIndicator_Outerloop_DeWit': 'Distributed_Design_Optimizer.coordination.convergence.DeWit.ConvergenceIndicator_Outerloop_DeWit',
    'Local_ConvergenceIndicator_Innerloop_DeWit': 'Distributed_Design_Optimizer.coordination.convergence.DeWit.Local_ConvergenceIndicator_Innerloop_DeWit',
    'Local_ConvergenceIndicator_Outerloop_DeWit': 'Distributed_Design_Optimizer.coordination.convergence.DeWit.Local_ConvergenceIndicator_Outerloop_DeWit',
    'Centralized_ConvergenceIndicator_Innerloop_DeWit': 'Distributed_Design_Optimizer.coordination.convergence.DeWit.Centralized_ConvergenceIndicator_Innerloop_DeWit',
    'Centralized_ConvergenceIndicator_Outerloop_DeWit': 'Distributed_Design_Optimizer.coordination.convergence.DeWit.Centralized_ConvergenceIndicator_Outerloop_DeWit',
    'ConvergenceIndicator_Innerloop_AlwaysConverged': 'Distributed_Design_Optimizer.coordination.convergence.AlwaysConverged.ConvergenceIndicator_Innerloop_AlwaysConverged',
    'ConvergenceIndicator_Outerloop_AlwaysConverged': 'Distributed_Design_Optimizer.coordination.convergence.AlwaysConverged.ConvergenceIndicator_Outerloop_AlwaysConverged',
    'Local_ConvergenceIndicator_Innerloop_AlwaysConverged': 'Distributed_Design_Optimizer.coordination.convergence.AlwaysConverged.Local_ConvergenceIndicator_Innerloop_AlwaysConverged',
    'Local_ConvergenceIndicator_Outerloop_AlwaysConverged': 'Distributed_Design_Optimizer.coordination.convergence.AlwaysConverged.Local_ConvergenceIndicator_Outerloop_AlwaysConverged',
    'Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged': 'Distributed_Design_Optimizer.coordination.convergence.AlwaysConverged.Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged',
    'Centralized_ConvergenceIndicator_Outerloop_AlwaysConverged': 'Distributed_Design_Optimizer.coordination.convergence.AlwaysConverged.Centralized_ConvergenceIndicator_Outerloop_AlwaysConverged',
})

__all__ += [
    'ConvergenceIndicator_Innerloop_DeWit', 'ConvergenceIndicator_Outerloop_DeWit',
    'Local_ConvergenceIndicator_Innerloop_DeWit', 'Local_ConvergenceIndicator_Outerloop_DeWit',
    'Centralized_ConvergenceIndicator_Innerloop_DeWit', 'Centralized_ConvergenceIndicator_Outerloop_DeWit',
    'ConvergenceIndicator_Innerloop_AlwaysConverged', 'ConvergenceIndicator_Outerloop_AlwaysConverged',
    'Local_ConvergenceIndicator_Innerloop_AlwaysConverged', 'Local_ConvergenceIndicator_Outerloop_AlwaysConverged',
    'Centralized_ConvergenceIndicator_Innerloop_AlwaysConverged', 'Centralized_ConvergenceIndicator_Outerloop_AlwaysConverged',
]
