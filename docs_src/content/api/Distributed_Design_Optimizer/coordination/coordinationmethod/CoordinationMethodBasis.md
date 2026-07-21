---
title: CoordinationMethodBasis
---

← Back to [coordinationmethod](index.md)

# CoordinationMethodBasis

**Source:** [Distributed_Design_Optimizer\coordination\coordinationmethod\CoordinationMethodBasis.py](CoordinationMethodBasis_source.md)

Basis class for coordination methods.

This module provides the base implementation for coordination methods,
containing common functionality shared across different coordination algorithms.

## Classes

### CoordinationMethodBasis

> **Inherits from:** [CoordinationMethodInterface](CoordinationMethodInterface.md#coordinationmethodinterface)

> Basis class for coordination methods providing common functionality.

> This class implements the common getter methods for iteration schemes
> that are shared across all coordination method implementations.
> Subclasses must set the iteration scheme attributes in their __init__.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the basis class.

    Note: Subclasses must set the following attributes:
    - _iterationscheme: IterationSchemeInterface
    - _allowediterationschemes: List[Type[IterationSchemeInterface]]
    - _unrecommendediterationschemes: List[Type[IterationSchemeInterface]]
    - _recommendediterationschemes: List[Type[IterationSchemeInterface]]

??? abstract "get_IterationScheme(self) → [IterationSchemeInterface](../innerloop_iterationscheme/IterationSchemeInterface.md#iterationschemeinterface)"
    Get the selected iteration scheme.


    **Returns:**
    > The iteration scheme instance.  

??? abstract "get_AllowedIterationSchemes(self) → List[Type[[IterationSchemeInterface](../innerloop_iterationscheme/IterationSchemeInterface.md#iterationschemeinterface)]]"
    Get the list of allowed iteration scheme types.


    **Returns:**
    > List of iteration scheme class types compatible with this coordination method.  

??? abstract "get_UnrecommendedIterationSchemes(self) → List[Type[[IterationSchemeInterface](../innerloop_iterationscheme/IterationSchemeInterface.md#iterationschemeinterface)]]"
    Get the list of unrecommended iteration scheme types.


    **Returns:**
    > List of iteration scheme class types that are unrecommended.  

??? abstract "get_RecommendedIterationSchemes(self) → List[Type[[IterationSchemeInterface](../innerloop_iterationscheme/IterationSchemeInterface.md#iterationschemeinterface)]]"
    Get the list of recommended iteration scheme types.


    **Returns:**
    > List of iteration scheme class types recommended for best convergence.  

??? abstract "get_Convergence_Indicator_Innerloop(self) → [ConvergenceIndicator_Innerloop_Interface](../convergence/ConvergenceIndicator_Innerloop_Interface.md#convergenceindicator_innerloop_interface)"
    Get the inner loop convergence indicator factory.


    **Returns:**
    > ConvergenceIndicator_Innerloop_Interface: The convergence indicator for inner loop.  

??? abstract "get_Convergence_Indicator_Outerloop(self) → [ConvergenceIndicator_Outerloop_Interface](../convergence/ConvergenceIndicator_Outerloop_Interface.md#convergenceindicator_outerloop_interface)"
    Get the outer loop convergence indicator factory.


    **Returns:**
    > ConvergenceIndicator_Outerloop_Interface: The convergence indicator for outer loop.  

??? abstract "print_startup_summary(self) → None"
    Print the convergence indicators, update method, and iteration scheme at startup.

??? abstract "print_termination_summary(self) → None"
    Print the convergence indicators, update method, and iteration scheme at the end.

