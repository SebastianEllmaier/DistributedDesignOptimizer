
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
    from Distributed_Design_Optimizer.postprocess.widgets._auto_update_delegate import AutoUpdateDelegate as AutoUpdateDelegate
    from Distributed_Design_Optimizer.postprocess.widgets.ChatPanel import ChatPanel as ChatPanel
    from Distributed_Design_Optimizer.postprocess.widgets.CollapsibleSection import CollapsibleSection as CollapsibleSection
    from Distributed_Design_Optimizer.postprocess.widgets.DataSelectionPanel import DataSelectionPanel as DataSelectionPanel
    from Distributed_Design_Optimizer.postprocess.widgets.GraphWidget import EdgeItem as EdgeItem
    from Distributed_Design_Optimizer.postprocess.widgets.GraphWidget import GraphWidget as GraphWidget
    from Distributed_Design_Optimizer.postprocess.widgets.MainWindow import MainWindow as MainWindow
    from Distributed_Design_Optimizer.postprocess.widgets.GraphWidget import NodeItem as NodeItem
    from Distributed_Design_Optimizer.postprocess.widgets.PlotCanvas import PlotCanvas as PlotCanvas
    from Distributed_Design_Optimizer.postprocess.widgets.PlotSettingsPanel import PlotSettingsPanel as PlotSettingsPanel
    from Distributed_Design_Optimizer.postprocess.widgets.PlotlyPanel import PlotlyPanel as PlotlyPanel
    from Distributed_Design_Optimizer.postprocess.widgets.ToggleSwitch import ToggleSwitch as ToggleSwitch
    from Distributed_Design_Optimizer.postprocess.widgets.TopologyControlsWidget import TopologyControlsWidget as TopologyControlsWidget
    from Distributed_Design_Optimizer.postprocess.widgets._topology_delegate import TopologyDelegate as TopologyDelegate
    from Distributed_Design_Optimizer.postprocess.widgets.TopologyPanel import TopologyPanel as TopologyPanel
    from Distributed_Design_Optimizer.postprocess.widgets._welcome_card import WelcomeCard as WelcomeCard
    from Distributed_Design_Optimizer.postprocess.widgets.MainWindow import logger as logger

_LAZY_IMPORTS = {
    'AutoUpdateDelegate': 'Distributed_Design_Optimizer.postprocess.widgets._auto_update_delegate',
    'ChatPanel': 'Distributed_Design_Optimizer.postprocess.widgets.ChatPanel',
    'CollapsibleSection': 'Distributed_Design_Optimizer.postprocess.widgets.CollapsibleSection',
    'DataSelectionPanel': 'Distributed_Design_Optimizer.postprocess.widgets.DataSelectionPanel',
    'EdgeItem': 'Distributed_Design_Optimizer.postprocess.widgets.GraphWidget',
    'GraphWidget': 'Distributed_Design_Optimizer.postprocess.widgets.GraphWidget',
    'MainWindow': 'Distributed_Design_Optimizer.postprocess.widgets.MainWindow',
    'NodeItem': 'Distributed_Design_Optimizer.postprocess.widgets.GraphWidget',
    'PlotCanvas': 'Distributed_Design_Optimizer.postprocess.widgets.PlotCanvas',
    'PlotSettingsPanel': 'Distributed_Design_Optimizer.postprocess.widgets.PlotSettingsPanel',
    'PlotlyPanel': 'Distributed_Design_Optimizer.postprocess.widgets.PlotlyPanel',
    'ToggleSwitch': 'Distributed_Design_Optimizer.postprocess.widgets.ToggleSwitch',
    'TopologyControlsWidget': 'Distributed_Design_Optimizer.postprocess.widgets.TopologyControlsWidget',
    'TopologyDelegate': 'Distributed_Design_Optimizer.postprocess.widgets._topology_delegate',
    'TopologyPanel': 'Distributed_Design_Optimizer.postprocess.widgets.TopologyPanel',
    'WelcomeCard': 'Distributed_Design_Optimizer.postprocess.widgets._welcome_card',
    'logger': 'Distributed_Design_Optimizer.postprocess.widgets.MainWindow',
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

__all__ = ['AutoUpdateDelegate', 'ChatPanel', 'CollapsibleSection', 'DataSelectionPanel', 'EdgeItem', 'GraphWidget', 'MainWindow', 'NodeItem', 'PlotCanvas', 'PlotSettingsPanel', 'PlotlyPanel', 'ToggleSwitch', 'TopologyControlsWidget', 'TopologyDelegate', 'TopologyPanel', 'WelcomeCard', 'logger']
# </AUTOGEN_INIT>
