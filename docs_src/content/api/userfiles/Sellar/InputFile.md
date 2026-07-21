---
title: InputFile
---

← Back to [Sellar](index.md)

# InputFile

**Source:** [userfiles\Sellar\InputFile.py](InputFile_source.md)

Input file configuration for Sellar problem with non-hierarchic decomposition.

This module defines the configuration for distributed optimization of the Sellar
multidisciplinary design problem using Augmented Lagrangian Coordination (ALC)
with non-hierarchic (flat) decomposition structure.

## Classes

### InputFile

> **Inherits from:** [InputFileBasis](../../Distributed_Design_Optimizer/coordination/InputFileBasis.md#inputfilebasis)

> Configuration class for Sellar problem with non-hierarchic ALC coordination.

> Defines the problem structure, subsystem decomposition, and coordination
> parameters for the Sellar multidisciplinary design optimization benchmark.


> **Attributes:**
> > _name: Problem identifier string.  
> > _coordinationmethod: Coordination algorithm (ALC variants).  
> > _subsystems: List of configured subsystem objects.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the Sellar non-hierarchic problem configuration.

    Sets up the full problem definition including:
    1. Coordination method and its hyperparameters.
    2. Subsystem IDs, hierarchy levels, and neighbor relationships.
    3. Analysis, objective, constraint, and optimization instances
    for each subsystem.
    4. Design variable bounds and scaling.
    5. Initial design variable values.
    6. Coupling and shared design variable initialization between
    neighboring subsystems.

