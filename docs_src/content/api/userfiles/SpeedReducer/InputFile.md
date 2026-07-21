---
title: InputFile
---

← Back to [SpeedReducer](index.md)

# InputFile

**Source:** [userfiles\SpeedReducer\InputFile.py](InputFile_source.md)

Input file configuration for Speed Reducer problem with non-hierarchic decomposition.

This module defines the configuration for distributed optimization of the Speed
Reducer design problem using Augmented Lagrangian Coordination (ALC) with
non-hierarchic decomposition into three subsystems.

## Classes

### InputFile

> **Inherits from:** [InputFileBasis](../../Distributed_Design_Optimizer/coordination/InputFileBasis.md#inputfilebasis)

> Configuration class for Speed Reducer problem with non-hierarchic ALC coordination.

> Defines the problem structure, subsystem decomposition, and coordination
> parameters for the Speed Reducer gearbox design optimization problem.


> **Attributes:**
> > _name: Problem identifier string.  
> > _coordinationmethod: Coordination algorithm (ALC variants).  
> > _subsystems: List of configured subsystem objects.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the Speed Reducer problem configuration.

    Sets up three subsystems representing the gear design, shaft 1,
    and shaft 2 disciplines with shared design variables.

