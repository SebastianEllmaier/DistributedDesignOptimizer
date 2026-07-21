---
title: InputFile
---

← Back to [TwoBarTruss](index.md)

# InputFile

**Source:** [userfiles\TwoBarTruss\InputFile.py](InputFile_source.md)

Input file configuration for Two-Bar Truss problem with non-hierarchic decomposition.

This module defines the configuration for distributed optimization of the
Two-Bar Truss structural problem using Augmented Lagrangian Coordination (ALC)
with non-hierarchic decomposition into three subsystems.

## Classes

### InputFile

> **Inherits from:** [InputFileBasis](../../Distributed_Design_Optimizer/coordination/InputFileBasis.md#inputfilebasis)

> Configuration class for Two-Bar Truss problem with non-hierarchic ALC.

> Defines the problem structure for the Two-Bar Truss structural optimization
> with three subsystems: system-level (FEM), bar 1, and bar 2.


> **Attributes:**
> > _name: Problem identifier string.  
> > _coordinationmethod: Coordination algorithm (ALC variants).  
> > _subsystems: List of configured subsystem objects.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the Two-Bar Truss problem configuration.

    Sets up three subsystems: system-level FEM analysis, bar 1 sizing,
    and bar 2 sizing with their coupling relationships.

