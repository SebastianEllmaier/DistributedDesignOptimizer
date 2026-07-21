---
title: handlers
---

# handlers

## Class Diagram

*Click on class names to navigate to their documentation.*

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#e6f4f7', 'primaryBorderColor': '#035970', 'primaryTextColor': '#000000', 'lineColor': '#035970', 'secondaryColor': '#cce9ef', 'tertiaryColor': '#f5fafb', 'noteBkgColor': '#e6f4f7', 'noteBorderColor': '#035970', 'fontFamily': 'Arial, sans-serif'}}}%%
classDiagram
    direction TB

    %% External classes (not in this project)
    class Enum:::externalStyle {
        <<external>>
    }

    class QObject:::externalStyle {
        <<external>>
    }

    class str:::externalStyle {
        <<external>>
    }

    class AlignedAxisData:::localStyle {
    }

    class ChatHandler:::localStyle {
        +response_ready
        +error
        -_config
        -_analysis_type
        -_context_data
        -_history
        -_worker
        ...
        +__init__(config, parent)
        +is_available()
        +set_context(analysis_type, context_data)
        +ask(question)
        +clear_history()
        +cancel()
    }

    class DataHandler:::localStyle {
        +entry_loaded
        +loading_error
        +data_updated
        +loading_started
        +loading_progress
        +loading_finished
        -_source
        -_loader_worker
        +__init__(parent)
        +source()
        +set_source(source)
        +load_files(paths)
        +get_plottable_data(item_paths)
        ...
    }

    class LlmApiModel:::localStyle {
        +TITAN
        +OPENAI
        +SONNET
        +GPT_4o
        +COHERE
    }

    class PlotHandler:::localStyle {
        +plot_ready
        +plot_error
        -_last_plottable_data
        -_last_labels_map
        -_last_customization
        -_canvas_size
        -_last_fig
        +__init__(parent)
        +last_plottable_data()
        +last_labels_map()
        +last_figure()
        +clear()
        ...
    }

    class TopologyHandler:::localStyle {
        +graph_ready
        +chart_ready
        +html_ready
        +analysis_error
        -_worker
        +__init__(parent)
        +run_analysis(dill_data, config, ...)
        +cancel()
        +validate_coordinator_file(metadata)
    }

    QObject <|-- ChatHandler
    QObject <|-- DataHandler
    str <|-- LlmApiModel
    Enum <|-- LlmApiModel
    QObject <|-- PlotHandler
    QObject <|-- TopologyHandler

    %% Click handlers for navigation to documentation
    click AlignedAxisData href "_axis_aligner/" "View AlignedAxisData documentation"
    click ChatHandler href "ChatHandler/" "View ChatHandler documentation"
    click DataHandler href "DataHandler/" "View DataHandler documentation"
    click LlmApiModel href "llm_utils/" "View LlmApiModel documentation"
    click PlotHandler href "PlotHandler/" "View PlotHandler documentation"
    click TopologyHandler href "TopologyHandler/" "View TopologyHandler documentation"

    %% Style definitions
    classDef packageStyle fill:#e8e8e8,stroke:#999999,stroke-width:2px
    classDef externalStyle fill:#fff8e6,stroke:#FFCC80,stroke-width:2px
    classDef projectStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px
    classDef projectAbstractStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px,stroke-dasharray:5 5
    classDef localStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px
    classDef abstractStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px,stroke-dasharray:5 5
```

## Modules

- [ChatHandler](ChatHandler.md)
- [DataHandler](DataHandler.md)
- [PlotHandler](PlotHandler.md)
- [TopologyHandler](TopologyHandler.md)
- [_axis_aligner](_axis_aligner.md)
- [_dynamic_builder](_dynamic_builder.md)
- [_plot_builder](_plot_builder.md)
- [_plot_customizer](_plot_customizer.md)
- [_static_graph_builder](_static_graph_builder.md)
- [_topology_dispatch](_topology_dispatch.md)
- [llm_api](llm_api.md)
- [llm_utils](llm_utils.md)

