
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
    from Distributed_Design_Optimizer.postprocess.handlers.llm_utils import API_BASE_PATH_V2 as API_BASE_PATH_V2
    from Distributed_Design_Optimizer.postprocess.handlers._axis_aligner import AlignedAxisData as AlignedAxisData
    from Distributed_Design_Optimizer.postprocess.handlers.ChatHandler import ChatHandler as ChatHandler
    from Distributed_Design_Optimizer.postprocess.handlers.DataHandler import DataHandler as DataHandler
    from Distributed_Design_Optimizer.postprocess.handlers.llm_utils import LlmApiModel as LlmApiModel
    from Distributed_Design_Optimizer.postprocess.handlers._plot_builder import MPL_TO_PLOTLY_DASH as MPL_TO_PLOTLY_DASH
    from Distributed_Design_Optimizer.postprocess.handlers.PlotHandler import PlotHandler as PlotHandler
    from Distributed_Design_Optimizer.postprocess.handlers.system_prompt import SYSTEM_PROMPT as SYSTEM_PROMPT
    from Distributed_Design_Optimizer.postprocess.handlers._plot_builder import TICK_LENGTH_TO_WIDTH_RATIO as TICK_LENGTH_TO_WIDTH_RATIO
    from Distributed_Design_Optimizer.postprocess.handlers.TopologyHandler import TopologyHandler as TopologyHandler
    from Distributed_Design_Optimizer.postprocess.handlers._plot_customizer import apply_all as apply_all
    from Distributed_Design_Optimizer.postprocess.handlers._plot_customizer import apply_font as apply_font
    from Distributed_Design_Optimizer.postprocess.handlers._plot_customizer import apply_labels as apply_labels
    from Distributed_Design_Optimizer.postprocess.handlers._plot_customizer import apply_legend as apply_legend
    from Distributed_Design_Optimizer.postprocess.handlers._plot_customizer import apply_per_line_styles as apply_per_line_styles
    from Distributed_Design_Optimizer.postprocess.handlers._plot_customizer import apply_reference_lines as apply_reference_lines
    from Distributed_Design_Optimizer.postprocess.handlers._axis_aligner import build_aligned_data as build_aligned_data
    from Distributed_Design_Optimizer.postprocess.handlers._dynamic_builder import build_dynamic_html as build_dynamic_html
    from Distributed_Design_Optimizer.postprocess.handlers._static_graph_builder import build_static_graph as build_static_graph
    from Distributed_Design_Optimizer.postprocess.handlers.llm_api import call_llm_api as call_llm_api
    from Distributed_Design_Optimizer.postprocess.handlers._axis_aligner import cumulative_from_labels as cumulative_from_labels
    from Distributed_Design_Optimizer.postprocess.handlers._plot_builder import generate_colors as generate_colors
    from Distributed_Design_Optimizer.postprocess.handlers._axis_aligner import generate_x_values as generate_x_values
    from Distributed_Design_Optimizer.postprocess.handlers.llm_utils import get_generate_chat_response as get_generate_chat_response
    from Distributed_Design_Optimizer.postprocess.handlers._plot_builder import get_legend_label as get_legend_label
    from Distributed_Design_Optimizer.postprocess.handlers._plot_builder import get_line_style as get_line_style
    from Distributed_Design_Optimizer.postprocess.handlers._axis_aligner import get_series_labels as get_series_labels
    from Distributed_Design_Optimizer.postprocess.handlers.llm_utils import get_access_token as get_access_token
    from Distributed_Design_Optimizer.postprocess.handlers._axis_aligner import get_x_label as get_x_label
    from Distributed_Design_Optimizer.postprocess.handlers.ChatHandler import logger as logger
    from Distributed_Design_Optimizer.postprocess.handlers._plot_builder import multi_axes_plot as multi_axes_plot
    from Distributed_Design_Optimizer.postprocess.handlers._topology_dispatch import resolve as resolve
    from Distributed_Design_Optimizer.postprocess.handlers._plot_builder import shared_axes_plot as shared_axes_plot
    from Distributed_Design_Optimizer.postprocess.handlers._plot_builder import stacked_plot as stacked_plot
    from Distributed_Design_Optimizer.postprocess.handlers._plot_builder import tick_width_for as tick_width_for

_LAZY_IMPORTS = {
    'API_BASE_PATH_V2': 'Distributed_Design_Optimizer.postprocess.handlers.llm_utils',
    'AlignedAxisData': 'Distributed_Design_Optimizer.postprocess.handlers._axis_aligner',
    'ChatHandler': 'Distributed_Design_Optimizer.postprocess.handlers.ChatHandler',
    'DataHandler': 'Distributed_Design_Optimizer.postprocess.handlers.DataHandler',
    'LlmApiModel': 'Distributed_Design_Optimizer.postprocess.handlers.llm_utils',
    'MPL_TO_PLOTLY_DASH': 'Distributed_Design_Optimizer.postprocess.handlers._plot_builder',
    'PlotHandler': 'Distributed_Design_Optimizer.postprocess.handlers.PlotHandler',
    'SYSTEM_PROMPT': 'Distributed_Design_Optimizer.postprocess.handlers.system_prompt',
    'TICK_LENGTH_TO_WIDTH_RATIO': 'Distributed_Design_Optimizer.postprocess.handlers._plot_builder',
    'TopologyHandler': 'Distributed_Design_Optimizer.postprocess.handlers.TopologyHandler',
    'apply_all': 'Distributed_Design_Optimizer.postprocess.handlers._plot_customizer',
    'apply_font': 'Distributed_Design_Optimizer.postprocess.handlers._plot_customizer',
    'apply_labels': 'Distributed_Design_Optimizer.postprocess.handlers._plot_customizer',
    'apply_legend': 'Distributed_Design_Optimizer.postprocess.handlers._plot_customizer',
    'apply_per_line_styles': 'Distributed_Design_Optimizer.postprocess.handlers._plot_customizer',
    'apply_reference_lines': 'Distributed_Design_Optimizer.postprocess.handlers._plot_customizer',
    'build_aligned_data': 'Distributed_Design_Optimizer.postprocess.handlers._axis_aligner',
    'build_dynamic_html': 'Distributed_Design_Optimizer.postprocess.handlers._dynamic_builder',
    'build_static_graph': 'Distributed_Design_Optimizer.postprocess.handlers._static_graph_builder',
    'call_llm_api': 'Distributed_Design_Optimizer.postprocess.handlers.llm_api',
    'cumulative_from_labels': 'Distributed_Design_Optimizer.postprocess.handlers._axis_aligner',
    'generate_colors': 'Distributed_Design_Optimizer.postprocess.handlers._plot_builder',
    'generate_x_values': 'Distributed_Design_Optimizer.postprocess.handlers._axis_aligner',
    'get_generate_chat_response': 'Distributed_Design_Optimizer.postprocess.handlers.llm_utils',
    'get_legend_label': 'Distributed_Design_Optimizer.postprocess.handlers._plot_builder',
    'get_line_style': 'Distributed_Design_Optimizer.postprocess.handlers._plot_builder',
    'get_series_labels': 'Distributed_Design_Optimizer.postprocess.handlers._axis_aligner',
    'get_access_token': 'Distributed_Design_Optimizer.postprocess.handlers.llm_utils',
    'get_x_label': 'Distributed_Design_Optimizer.postprocess.handlers._axis_aligner',
    'logger': 'Distributed_Design_Optimizer.postprocess.handlers.ChatHandler',
    'multi_axes_plot': 'Distributed_Design_Optimizer.postprocess.handlers._plot_builder',
    'resolve': 'Distributed_Design_Optimizer.postprocess.handlers._topology_dispatch',
    'shared_axes_plot': 'Distributed_Design_Optimizer.postprocess.handlers._plot_builder',
    'stacked_plot': 'Distributed_Design_Optimizer.postprocess.handlers._plot_builder',
    'tick_width_for': 'Distributed_Design_Optimizer.postprocess.handlers._plot_builder',
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

__all__ = ['API_BASE_PATH_V2', 'AlignedAxisData', 'ChatHandler', 'DataHandler', 'LlmApiModel', 'MPL_TO_PLOTLY_DASH', 'PlotHandler', 'SYSTEM_PROMPT', 'TICK_LENGTH_TO_WIDTH_RATIO', 'TopologyHandler', 'apply_all', 'apply_font', 'apply_labels', 'apply_legend', 'apply_per_line_styles', 'apply_reference_lines', 'build_aligned_data', 'build_dynamic_html', 'build_static_graph', 'call_llm_api', 'cumulative_from_labels', 'generate_colors', 'generate_x_values', 'get_generate_chat_response', 'get_legend_label', 'get_line_style', 'get_series_labels', 'get_access_token', 'get_x_label', 'logger', 'multi_axes_plot', 'resolve', 'shared_axes_plot', 'stacked_plot', 'tick_width_for']
# </AUTOGEN_INIT>
