---
title: solver
---

# solver

## Class Diagram

*Click on class names to navigate to their documentation.*

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#e6f4f7', 'primaryBorderColor': '#035970', 'primaryTextColor': '#000000', 'lineColor': '#035970', 'secondaryColor': '#cce9ef', 'tertiaryColor': '#f5fafb', 'noteBkgColor': '#e6f4f7', 'noteBorderColor': '#035970', 'fontFamily': 'Arial, sans-serif'}}}%%
classDiagram
    direction TB

    class Solver_PyNomadBBO:::localStyle {
        -_seed
        -_vns_mads_search
        -_quad_model_search
        -_maxevals
        -_constraint_handling_method
        -_eqcon_as_ineqcon_tol
        +__init__(maxevals, constraint_handling_method, ...)
        +execute(subsystem)
    }

    class Solver_QP:::localStyle {
        -_P
        -_q
        -_A
        -_G
        -_h
        -_maxevals
        -_constraint_tol
        +__init__(maxevals, constraint_tol)
        +get_P()
        +set_P(P_in)
        +get_q()
        +set_q(q_in)
        ...
    }

    class SolverInterface:::abstractStyle {
        <<abstract>>
        +execute(subsystem)
    }

    SolverInterface <|-- Solver_PyNomadBBO
    SolverInterface <|-- Solver_QP

    %% Click handlers for navigation to documentation
    click Solver_PyNomadBBO href "Solver_PyNomadBBO/" "View Solver_PyNomadBBO documentation"
    click Solver_QP href "Solver_QP/" "View Solver_QP documentation"
    click SolverInterface href "SolverInterface/" "View SolverInterface documentation"

    %% Style definitions
    classDef packageStyle fill:#e8e8e8,stroke:#999999,stroke-width:2px
    classDef externalStyle fill:#fff8e6,stroke:#FFCC80,stroke-width:2px
    classDef projectStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px
    classDef projectAbstractStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px,stroke-dasharray:5 5
    classDef localStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px
    classDef abstractStyle fill:#e6f4f7,stroke:#035970,stroke-width:2px,stroke-dasharray:5 5
```

## Modules

- [SolverInterface](SolverInterface.md)
- [Solver_PyNomadBBO](Solver_PyNomadBBO.md)
- [Solver_QP](Solver_QP.md)

