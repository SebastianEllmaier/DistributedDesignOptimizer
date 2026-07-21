---
title: historyentry
---

# historyentry

## Class Diagram

*Click on class names to navigate to their documentation.*

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#e6f4f7', 'primaryBorderColor': '#035970', 'primaryTextColor': '#000000', 'lineColor': '#035970', 'secondaryColor': '#cce9ef', 'tertiaryColor': '#f5fafb', 'noteBkgColor': '#e6f4f7', 'noteBorderColor': '#035970', 'fontFamily': 'Arial, sans-serif'}}}%%
classDiagram
    direction TB

    class ControllerSubSystemHistoryEntry:::localStyle {
        +__init__(subsystem_id, outerloop_itr, ...)
        +get_OptimData()
    }

    class HistoryEntry:::localStyle {
        -_outerloop_itr
        -_innerloop_itr
        -_innerloop_itr_runtime
        -_innerloop_itr_numberofdesignvariableevaluations
        +__init__(outerloop_itr, innerloop_itr, ...)
        +get_OuterLoop_Itr()
        +get_InnerLoop_Itr()
        +get_InnerLoop_Itr_Runtime()
        +get_InnerLoop_Itr_NumberOfDesignVariableEvaluations()
    }

    class LocalSubSystemHistoryEntry:::localStyle {
        -_scalers
        -_inconsistencies
        -_maxinconsistencyvalue
        -_maxinconsistencysubsystemID
        +__init__(subsystem_id, outerloop_itr, ...)
        +get_OptimData()
        +get_Scalers()
        +get_Inconsistencies()
        +get_maxInconsistencyValue()
        +get_MaxInconsistencyCoupledSubsystemID()
    }

    class SubSystemHistoryEntry:::localStyle {
        -_subsystem_id
        -_optimdata
        -_convinnerloop
        -_convouterloop
        +__init__(subsystem_id, outerloop_itr, ...)
        +get_SUBSYSTEMID()
        +get_OptimData()
        +get_ConvInnerLoop()
        +get_ConvOuterLoop()
    }

    SubSystemHistoryEntry <|-- ControllerSubSystemHistoryEntry
    SubSystemHistoryEntry <|-- LocalSubSystemHistoryEntry
    HistoryEntry <|-- SubSystemHistoryEntry

    %% Click handlers for navigation to documentation
    click ControllerSubSystemHistoryEntry href "ControllerSubSystemHistoryEntry/" "View ControllerSubSystemHistoryEntry documentation"
    click HistoryEntry href "HistoryEntry/" "View HistoryEntry documentation"
    click LocalSubSystemHistoryEntry href "LocalSubSystemHistoryEntry/" "View LocalSubSystemHistoryEntry documentation"
    click SubSystemHistoryEntry href "SubSystemHistoryEntry/" "View SubSystemHistoryEntry documentation"

    %% Style definitions
    classDef packageStyle fill:#e8e8e8,stroke:#999999,stroke-width:2px
    classDef externalStyle fill:#fff8e6,stroke:#FFCC80,stroke-width:2px
    classDef projectStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px
    classDef projectAbstractStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px,stroke-dasharray:5 5
    classDef localStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px
    classDef abstractStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px,stroke-dasharray:5 5
```

## Modules

- [ControllerSubSystemHistoryEntry](ControllerSubSystemHistoryEntry.md)
- [HistoryEntry](HistoryEntry.md)
- [LocalSubSystemHistoryEntry](LocalSubSystemHistoryEntry.md)
- [SubSystemHistoryEntry](SubSystemHistoryEntry.md)

