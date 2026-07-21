---
title: Core Components and Unified Algorithmic Structure
---

# Core Components and Unified Algorithmic Structure

## DistributedDesignOptimizer (DDO) Repository

<!-- AUTO-GENERATED-DIAGRAM-START -->
```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#e6f4f7', 'primaryBorderColor': '#035970', 'primaryTextColor': '#000000', 'lineColor': '#035970', 'secondaryColor': '#cce9ef', 'tertiaryColor': '#f5fafb', 'noteBkgColor': '#e6f4f7', 'noteBorderColor': '#035970', 'fontFamily': 'Arial, sans-serif'}}}%%
classDiagram
    direction TB

    %% Top-level packages / folders
    class Distributed_Design_Optimizer["Distributed_Design_Optimizer/"]:::packageStyle
    class docs["docs/"]:::packageStyle
    class docs_src["docs_src/"]:::packageStyle
    class userfiles["userfiles/"]:::packageStyle

    %% Top-level files
    class LICENSE["LICENSE"]:::fileStyle
    class main_ddo_viewer_py["main_ddo_viewer.py"]:::fileStyle
    class README_md["README.md"]:::fileStyle
    class requirements_txt["requirements.txt"]:::fileStyle

    %% Style definitions
    classDef packageStyle fill:#e8e8e8,stroke:#999999,stroke-width:2px
    classDef fileStyle fill:#fff8e6,stroke:#FFCC80,stroke-width:2px
```
<!-- AUTO-GENERATED-DIAGRAM-END -->

The repository contains (among others):

- [`Distributed_Design_Optimizer`](../api/Distributed_Design_Optimizer/index.md) - core package for distributed design optimization

- `historyfiles` and `main_ddo_viewer.py` - storage and processing of logging data from executed optimizations. Executed optimizations store their logging data as `.dill` files in the respective use-case's `historyfiles/` folder under `userfiles/<usecasename>/`. Further details in [Tutorial > Processing](../tutorial/processing/index.md).

- [`userfiles`](../api/userfiles/index.md) - existing example use-cases and future use-cases to be solved with abbr:DDO. Further details in [Tutorial > Problem Definition and Algorithm Execution](../tutorial/problem-definition-and-algorithm-execution/index.md) and [Examples](../examples/GeometricProgramming/index.md).


## [`Distributed_Design_Optimizer`](../api/Distributed_Design_Optimizer/index.md) Package

The package consists of several packages, three of which are fundamental to the implementation of distributed design optimization:

- [`coordination/`](../api/Distributed_Design_Optimizer/coordination/index.md) holds 
    - [`Coordinator`](../api/Distributed_Design_Optimizer/coordination/Coordinator.md) - responsible for initializing and calling the main routines of the [Unified Algorithmic Structure](../distributed-optimization-for-multidisciplinary-design/unified-algorithmic-structure.md)
    - [`InputFileInterface`](../api/Distributed_Design_Optimizer/coordination/InputFileInterface.md) and [`InputFileBasis`](../api/Distributed_Design_Optimizer/coordination/InputFileBasis.md) - prescribing the template for any distributed optimization problem formulation
    - [`innerloop_iterationscheme`](../api/Distributed_Design_Optimizer/coordination/innerloop_iterationscheme/index.md) - executing subsystem (and controller) optimizations in series or parallel in the innerloop using `multiprocessing`
    - [`convergence`](../api/Distributed_Design_Optimizer/coordination/convergence/index.md) - providing various innerloop and outerloop convergence criteria
    - [`updatecouplingparametermethod`](../api/Distributed_Design_Optimizer/coordination/updatecouplingparametermethod/index.md) - providing various innerloop and outerloop coupling parameter update schemes
    - [`coordinationmethod`](../api/Distributed_Design_Optimizer/coordination/coordinationmethod/index.md) - providing coordination method specific functionalities to initialize the distributed design optimization

- [`subsystem/`](../api/Distributed_Design_Optimizer/subsystem/index.md) holds 
    - [`SubSystemInterface`](../api/Distributed_Design_Optimizer/subsystem/SubSystemInterface.md), [`SubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/SubSystemBasis.md) and coordination method specific subclasses - representing a distributed individual processing unit which collects all information and methods unique to a single subsystem in the distributed optimization algorithms
    - [`couplingparameters`](../api/Distributed_Design_Optimizer/subsystem/couplingparameters/index.md) > [`CouplingParametersInterface`](../api/Distributed_Design_Optimizer/subsystem/couplingparameters/CouplingParametersInterface.md), [`CouplingParametersBasis`](../api/Distributed_Design_Optimizer/subsystem/couplingparameters/CouplingParametersBasis.md) and coordination method specific subclasses - containing information relevant to the coupling between two subsystems. Each subsystem holds a list of these coupling parameters instances (one for each pairwise coupling with a neighboring subsystem).
    - [`optimization`](../api/Distributed_Design_Optimizer/subsystem/optimization/index.md) > [`AnalysisInterface`](../api/Distributed_Design_Optimizer/subsystem/optimization/AnalysisInterface.md), [`designproblem`](../api/Distributed_Design_Optimizer/subsystem/optimization/designproblem/index.md) and [`solver`](../api/Distributed_Design_Optimizer/subsystem/optimization/solver/index.md) packages - providing functionalities to formulate and solve each subsystem optimization problem. Further details in [SubSystem Optimization](subsystem-optimization.md).
    - [`tools`](../api/Distributed_Design_Optimizer/subsystem/tools/index.md) package - holding various classes and methods utilized by each subsystem instance, such as [`ScalerBasis`](../api/Distributed_Design_Optimizer/subsystem/tools/ScalerBasis.md), [`FiniteDifferencesJacobian`](../api/Distributed_Design_Optimizer/subsystem/tools/FiniteDifferencesJacobian.md) and [`HessianApproximationBFGS`](../api/Distributed_Design_Optimizer/subsystem/tools/HessianApproximationBFGS.md). Further details can be found under [Problem Definition and Algorithm Execution](../tutorial/problem-definition-and-algorithm-execution/index.md#3-defining-the-mainpy-and-inputfilepy) and [Derivative Computation](derivative-computation.md).     

- [`middlelevel/`](../api/Distributed_Design_Optimizer/middlelevel/index.md) holds
    - [`MiddleLevelCouplingInterface`](../api/Distributed_Design_Optimizer/middlelevel/MiddleLevelCouplingInterface.md), [`MiddleLevelCouplingBasis`](../api/Distributed_Design_Optimizer/middlelevel/MiddleLevelCouplingBasis.md) and coordination method specific subclasses - holding the information being exchanged between two neighboring [`SubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/SubSystemBasis.md) instances which can write and read the [`MiddleLevelDataStorageBasis`](../api/Distributed_Design_Optimizer/middlelevel/MiddleLevelDataStorageBasis.md).
    - [`MiddleLevelDataStorageInterface`](../api/Distributed_Design_Optimizer/middlelevel/MiddleLevelDataStorageInterface.md), [`MiddleLevelDataStorageBasis`](../api/Distributed_Design_Optimizer/middlelevel/MiddleLevelDataStorageBasis.md) and coordination method specific subclasses - representing the shared resource interface storage between [`SubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/SubSystemBasis.md) instances. Each instance is guarded by a `multiprocessing` lock and holds two instances of [`MiddleLevelCouplingInterface`](../api/Distributed_Design_Optimizer/middlelevel/MiddleLevelCouplingInterface.md) (or subclasses).

The intricate relationship between a subsystem's couplingparameter for a neighboring subsystem and the middlelevel data storage between them is further detailed in [Information Sharing via CouplingParameters and MiddleLevelDataStorage](information-sharing-via-couplingparameters-and-middleleveldatastorage.md).


## Unified Algorithmic Structure Pseudocode-to-Code Traceability

Given the definition of a distributed design optimization problem from [`userfiles`](../api/userfiles/index.md), 
the [`Distributed_Design_Optimizer`](../api/Distributed_Design_Optimizer/index.md) package implements the [Unified Algorithmic Structure](../distributed-optimization-for-multidisciplinary-design/unified-algorithmic-structure.md) as illustrated by the pseudocode-to-code traceability shown below.

<!-- UNIFIED-ALGORITHMIC-STRUCTURE-PSEUDOCODE-TRACEABILITY -->