---
title: models
---

# models

## Class Diagram

*Click on class names to navigate to their documentation.*

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#e6f4f7', 'primaryBorderColor': '#035970', 'primaryTextColor': '#000000', 'lineColor': '#035970', 'secondaryColor': '#cce9ef', 'tertiaryColor': '#f5fafb', 'noteBkgColor': '#e6f4f7', 'noteBorderColor': '#035970', 'fontFamily': 'Arial, sans-serif'}}}%%
classDiagram
    direction TB

    class AnalysisConfig:::localStyle {
    }

    class DataSource:::abstractStyle {
        <<abstract>>
        +connect()
        +load_entry(path_or_id)
        +list_entries()
        +get_tree_structure(entry_id)
        +get_values(entry_id, item_path)
        ...
    }

    class DillDataSource:::localStyle {
        -_history_data
        -_file_paths
        -_file_mtimes
        -_lock
        +__init__()
        +connect()
        +load_entry(path)
        +list_entries()
        +get_tree_structure(entry_id)
        ...
    }

    class FontConfig:::localStyle {
    }

    class LineConfig:::localStyle {
    }

    class ReferenceLine:::localStyle {
    }

    class PlotConfig:::localStyle {
    }

    class PostgresDataSource:::localStyle {
        +connect()
        +load_entry(path_or_id)
        +list_entries()
        +get_tree_structure(entry_id)
        +get_values(entry_id, item_path)
        ...
    }

    DataSource <|-- DillDataSource
    DataSource <|-- PostgresDataSource

    %% Click handlers for navigation to documentation
    click AnalysisConfig href "AnalysisConfig/" "View AnalysisConfig documentation"
    click DataSource href "DataSource/" "View DataSource documentation"
    click DillDataSource href "DillDataSource/" "View DillDataSource documentation"
    click FontConfig href "PlotConfig/" "View FontConfig documentation"
    click LineConfig href "PlotConfig/" "View LineConfig documentation"
    click ReferenceLine href "PlotConfig/" "View ReferenceLine documentation"
    click PlotConfig href "PlotConfig/" "View PlotConfig documentation"
    click PostgresDataSource href "PostgresDataSource/" "View PostgresDataSource documentation"

    %% Style definitions
    classDef packageStyle fill:#e8e8e8,stroke:#999999,stroke-width:2px
    classDef externalStyle fill:#fff8e6,stroke:#FFCC80,stroke-width:2px
    classDef projectStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px
    classDef projectAbstractStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px,stroke-dasharray:5 5
    classDef localStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px
    classDef abstractStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px,stroke-dasharray:5 5
```

## Modules

- [AnalysisConfig](AnalysisConfig.md)
- [DataSource](DataSource.md)
- [DillDataSource](DillDataSource.md)
- [PlotConfig](PlotConfig.md)
- [PostgresDataSource](PostgresDataSource.md)

