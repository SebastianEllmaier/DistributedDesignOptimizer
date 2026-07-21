---
title: InputFile
---

← Back to [GeometricProgramming](index.md)

# InputFile

**Source:** [userfiles\GeometricProgramming\InputFile.py](InputFile_source.md)

Input file configuration for Geometric Programming Top-Down Hierarchic continuous optimization.

This module defines the InputFileAugmentedLagrangian class which configures
all parameters for the distributed optimization including subsystem definitions,
coordination methods, iteration schemes, and hyperparameters for the ALC method.

## Classes

### InputFile

> **Inherits from:** [InputFileBasis](../../Distributed_Design_Optimizer/coordination/InputFileBasis.md#inputfilebasis)

> Input file for Geometric Programming distributed optimization.

> Configures a three-subsystem distributed optimization problem by defining
> the coordination method, subsystem hierarchy, design variable bounds,
> scaling variables, initial design variables, and coupling parameters.


> **Attributes:**
> > _name: Identifier string for this use-case.  
> > _coordinationmethod: The coordination algorithm (e.g. ALC, PC, LC).  
> > _subsystems: List of LocalSubSystemBasis instances created by the  
> > coordination method.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the distributed optimization problem configuration.

    Sets up the full problem definition including:
    1. Coordination method and its hyperparameters.
    2. Subsystem IDs, hierarchy levels, and neighbor relationships.
    3. Analysis, objective, constraint, and optimization instances
    for each subsystem.
    4. Design variable bounds and scaling.
    5. Initial design variable values.
    6. Coupling and shared design variable initialization between
    neighboring subsystems.

