---
title: workers
---

# workers

## Class Diagram

*Click on class names to navigate to their documentation.*

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#e6f4f7', 'primaryBorderColor': '#035970', 'primaryTextColor': '#000000', 'lineColor': '#035970', 'secondaryColor': '#cce9ef', 'tertiaryColor': '#f5fafb', 'noteBkgColor': '#e6f4f7', 'noteBorderColor': '#035970', 'fontFamily': 'Arial, sans-serif'}}}%%
classDiagram
    direction TB

    %% External classes (not in this project)
    class QThread:::externalStyle {
        <<external>>
    }

    class AutoUpdateWorker:::localStyle {
        +updates_detected
        +check_complete
        -_source
        -_interval_ms
        +__init__(source, interval_ms, ...)
        +run()
        +stop()
    }

    class CallableWorker:::localStyle {
        +error
        -_fn
        -_args
        +__init__(fn, args, ...)
        +run()
    }

    class FileLoaderWorker:::localStyle {
        +file_loaded
        +progress
        +file_error
        -_source
        -_file_paths
        +__init__(source, file_paths, ...)
        +run()
    }

    class LLMWorker:::localStyle {
        +response_ready
        +__init__(call_fn, messages, ...)
    }

    class TopologyWorker:::localStyle {
        +graph_ready
        +chart_ready
        +html_ready
        -_label
        -_context_data
        -_output_type
        +__init__(build_fn, args, ...)
    }

    QThread <|-- AutoUpdateWorker
    QThread <|-- CallableWorker
    QThread <|-- FileLoaderWorker
    CallableWorker <|-- LLMWorker
    CallableWorker <|-- TopologyWorker

    %% Click handlers for navigation to documentation
    click AutoUpdateWorker href "AutoUpdateWorker/" "View AutoUpdateWorker documentation"
    click CallableWorker href "CallableWorker/" "View CallableWorker documentation"
    click FileLoaderWorker href "FileLoaderWorker/" "View FileLoaderWorker documentation"
    click LLMWorker href "LLMWorker/" "View LLMWorker documentation"
    click TopologyWorker href "TopologyWorker/" "View TopologyWorker documentation"

    %% Style definitions
    classDef packageStyle fill:#e8e8e8,stroke:#999999,stroke-width:2px
    classDef externalStyle fill:#fff8e6,stroke:#FFCC80,stroke-width:2px
    classDef projectStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px
    classDef projectAbstractStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px,stroke-dasharray:5 5
    classDef localStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px
    classDef abstractStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px,stroke-dasharray:5 5
```

## Modules

- [AutoUpdateWorker](AutoUpdateWorker.md)
- [CallableWorker](CallableWorker.md)
- [FileLoaderWorker](FileLoaderWorker.md)
- [LLMWorker](LLMWorker.md)
- [TopologyWorker](TopologyWorker.md)

