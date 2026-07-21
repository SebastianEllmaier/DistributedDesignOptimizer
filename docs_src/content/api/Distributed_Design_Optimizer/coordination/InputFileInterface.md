---
title: InputFileInterface
---

← Back to [coordination](index.md)

# InputFileInterface

**Source:** [Distributed_Design_Optimizer\coordination\InputFileInterface.py](InputFileInterface_source.md)

Interface module for input file configurations.

This module defines the abstract interface for input files that specify
optimization problem setup, including subsystems, coordination methods,
iteration schemes, and execution parameters.

## Classes

### InputFileInterface

> **Inherits from:** `ABC`

> Abstract interface for input file configurations.

> This interface defines the contract for input files that specify
> optimization problem setup, including subsystems, coordination methods,
> iteration schemes, and execution mode configuration.

#### Methods

??? abstract "get_Subsystems(self) → List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]"
    Get the list of subsystem subsystems for the optimization.


    **Returns:**
    > List[SubSystemInterface]: The list of subsystem subsystems.  

??? abstract "get_CoordinationMethod(self) → [CoordinationMethodInterface](coordinationmethod/CoordinationMethodInterface.md#coordinationmethodinterface)"
    Get the coordination method for this optimization.


    **Returns:**
    > CoordinationMethodInterface: _description_  

??? abstract "get_IterationScheme(self) → [IterationSchemeInterface](innerloop_iterationscheme/IterationSchemeInterface.md#iterationschemeinterface)"
    Get the iteration scheme for the optimization.


    **Returns:**
    > IterationSchemeInterface: The iteration scheme instance.  

??? abstract "get_Name(self) → str"
    Get the name identifier for this input file configuration.


    **Returns:**
    > str: The name of the input file configuration.  

??? abstract "get_HistoryFolderPath(self) → str"
    Get the folder path where history .dill files are saved.

    The path is derived from the location of the concrete InputFile
    subclass (i.e. the use-case folder under userfiles/<usecasename>/),
    so history files are stored alongside the use-case that produced them.


    **Returns:**
    > str: The absolute path to the use-case's historyfiles folder.  

??? abstract "print_startup_summary(self) → None"
    Print the input file configuration summary (use-case name and coordination method).

