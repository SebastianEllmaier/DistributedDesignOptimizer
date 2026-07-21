# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Basis class for coordination methods.

This module provides the base implementation for coordination methods,
containing common functionality shared across different coordination algorithms.
"""

from typing import List, Type
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print
from Distributed_Design_Optimizer.coordination.coordinationmethod import CoordinationMethodInterface
from Distributed_Design_Optimizer.coordination.innerloop_iterationscheme import IterationSchemeInterface
from Distributed_Design_Optimizer.coordination.updatecouplingparametermethod import UpdateCouplingParameterMethodInterface
from Distributed_Design_Optimizer.coordination.convergence import (ConvergenceIndicator_Innerloop_Interface,
                                                                   ConvergenceIndicator_Outerloop_Interface,
                                                                   )


class CoordinationMethodBasis(CoordinationMethodInterface):
    """Basis class for coordination methods providing common functionality.

    This class implements the common getter methods for iteration schemes
    that are shared across all coordination method implementations.
    Subclasses must set the iteration scheme attributes in their __init__.
    """

    _DDO_PRINT_LABEL_WIDTH: int = 20

    def __init__(self) -> None:
        """Initialize the basis class.
        
        Note: Subclasses must set the following attributes:
            - _iterationscheme: IterationSchemeInterface
            - _allowediterationschemes: List[Type[IterationSchemeInterface]]
            - _unrecommendediterationschemes: List[Type[IterationSchemeInterface]]
            - _recommendediterationschemes: List[Type[IterationSchemeInterface]]
        """
        
        # to be initialized in child-class of CoordinationMethodBasis
        self._iterationscheme: IterationSchemeInterface
        self._allowediterationschemes: List[Type[IterationSchemeInterface]] 
        self._unrecommendediterationschemes: List[Type[IterationSchemeInterface]]
        self._recommendediterationschemes: List[Type[IterationSchemeInterface]]
        
        # to be initialized in child-class of CoordinationMethodBasis
        self._convergence_indicator_innerloop: ConvergenceIndicator_Innerloop_Interface
        self._convergence_indicator_outerloop: ConvergenceIndicator_Outerloop_Interface
        self._updatecouplingparametermethod_outerloop: UpdateCouplingParameterMethodInterface
        self._iterationscheme: IterationSchemeInterface

    def get_IterationScheme(self) -> IterationSchemeInterface:
        """Get the selected iteration scheme.

        Returns:
            The iteration scheme instance.
        """
        return self._iterationscheme

    def get_AllowedIterationSchemes(self) -> List[Type[IterationSchemeInterface]]:
        """Get the list of allowed iteration scheme types.

        Returns:
            List of iteration scheme class types compatible with this coordination method.
        """
        return self._allowediterationschemes.copy()

    def get_UnrecommendedIterationSchemes(self) -> List[Type[IterationSchemeInterface]]:
        """Get the list of unrecommended iteration scheme types.

        Returns:
            List of iteration scheme class types that are unrecommended.
        """
        return self._unrecommendediterationschemes.copy()

    def get_RecommendedIterationSchemes(self) -> List[Type[IterationSchemeInterface]]:
        """Get the list of recommended iteration scheme types.

        Returns:
            List of iteration scheme class types recommended for best convergence.
        """
        return self._recommendediterationschemes.copy()
    
    def get_Convergence_Indicator_Innerloop(self) -> ConvergenceIndicator_Innerloop_Interface:
        """Get the inner loop convergence indicator factory.

        Returns:
            ConvergenceIndicator_Innerloop_Interface: The convergence indicator for inner loop.
        """
        return self._convergence_indicator_innerloop
    
    def get_Convergence_Indicator_Outerloop(self) -> ConvergenceIndicator_Outerloop_Interface:
        """Get the outer loop convergence indicator factory.

        Returns:
            ConvergenceIndicator_Outerloop_Interface: The convergence indicator for outer loop.
        """
        return self._convergence_indicator_outerloop
    
    def _print_coordination_config(self) -> None:
        """Print convergence indicators, update method, and iteration scheme."""
        ddo_print(f"{type(self).__name__}: ConvergenceIndicator_Innerloop:")
        self.get_Convergence_Indicator_Innerloop().print_startup_summary()
        ddo_print(f"{type(self).__name__}: ConvergenceIndicator_Outerloop:")
        self.get_Convergence_Indicator_Outerloop().print_startup_summary()
        ddo_print(f"{type(self).__name__}: UpdateCouplingParameterMethod_Outerloop:")
        self._updatecouplingparametermethod_outerloop.print_startup_summary()
        ddo_print(f"{type(self).__name__}: {'IterationScheme:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {type(self.get_IterationScheme()).__name__}")
        self.get_IterationScheme().print_startup_summary()

    def print_startup_summary(self) -> None:
        """Print the convergence indicators, update method, and iteration scheme at startup."""
        self._print_coordination_config()

    def print_termination_summary(self) -> None:
        """Print the convergence indicators, update method, and iteration scheme at the end."""
        self._print_coordination_config()
