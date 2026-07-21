---
title: Distributed_Design_Optimizer
---

# Distributed_Design_Optimizer

Core package for distributed multidisciplinary design optimization.

## Class Diagram

*Click on class names to navigate to their documentation.*

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#e6f4f7', 'primaryBorderColor': '#035970', 'primaryTextColor': '#000000', 'lineColor': '#035970', 'secondaryColor': '#cce9ef', 'tertiaryColor': '#f5fafb', 'noteBkgColor': '#e6f4f7', 'noteBorderColor': '#035970', 'fontFamily': 'Arial, sans-serif'}}}%%
classDiagram
    direction TB

    %% Sub-packages (click to navigate)
    class coordination["coordination/"]:::packageStyle
    class middlelevel["middlelevel/"]:::packageStyle
    class postprocess["postprocess/"]:::packageStyle
    class subsystem["subsystem/"]:::packageStyle


    %% Click handlers for navigation to documentation
    click coordination href "coordination/" "Browse coordination package"
    click middlelevel href "middlelevel/" "Browse middlelevel package"
    click postprocess href "postprocess/" "Browse postprocess package"
    click subsystem href "subsystem/" "Browse subsystem package"

    %% Style definitions
    classDef packageStyle fill:#e8e8e8,stroke:#999999,stroke-width:2px
    classDef externalStyle fill:#fff8e6,stroke:#FFCC80,stroke-width:2px
    classDef projectStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px
    classDef projectAbstractStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px,stroke-dasharray:5 5
    classDef localStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px
    classDef abstractStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px,stroke-dasharray:5 5
```

## Subpackages

- [coordination](coordination/index.md)
- [middlelevel](middlelevel/index.md)
- [postprocess](postprocess/index.md)
- [subsystem](subsystem/index.md)

## Modules

- [generate_inits](generate_inits.md)

