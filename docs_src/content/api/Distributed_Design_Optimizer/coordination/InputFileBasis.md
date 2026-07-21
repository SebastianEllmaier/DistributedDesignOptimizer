---
title: InputFileBasis
---

← Back to [coordination](index.md)

# InputFileBasis

**Source:** [Distributed_Design_Optimizer\coordination\InputFileBasis.py](InputFileBasis_source.md)

Basis implementation of the InputFile interface for coordination setup.

## Classes

### InputFileBasis

> **Inherits from:** [InputFileInterface](InputFileInterface.md#inputfileinterface)

> Base class providing the standard InputFile configuration for coordination.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the input file basis with default None values.

??? abstract "get_Subsystems(self) → List[[LocalSubSystemBasis](../subsystem/LocalSubSystemBasis.md#localsubsystembasis)]"
    Return the list of local subsystems.


    **Returns:**
    > The list of local subsystem basis instances.  

??? abstract "get_CoordinationMethod(self) → [CoordinationMethodInterface](coordinationmethod/CoordinationMethodInterface.md#coordinationmethodinterface)"
    Return the coordination method.


    **Returns:**
    > The coordination method interface instance.  

??? abstract "get_IterationScheme(self) → [IterationSchemeInterface](innerloop_iterationscheme/IterationSchemeInterface.md#iterationschemeinterface)"
    Return the iteration scheme.


    **Returns:**
    > The iteration scheme interface instance.  

??? abstract "get_Name(self) → str"
    Return the name of the input file configuration.


    **Returns:**
    > The name identifier string.  

??? abstract "get_HistoryFolderPath(self) → str"
    Return the folder path where history .dill files are saved.

    The path is derived from the source-file location of the concrete
    InputFile subclass (``type(self)``), which resides in the use-case
    folder under userfiles/<usecasename>/. This anchors the historyfiles
    folder to the use-case rather than the current working directory,
    independent of where the use-case's main.py is launched from.


    **Returns:**
    > The absolute path to the use-case's historyfiles folder.  

??? abstract "print_startup_summary(self) → None"
    Print the input file configuration summary.

