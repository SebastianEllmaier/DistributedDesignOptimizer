# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Local constraints module for Two-Bar Truss subsystem 1.

Defines the stress constraint for bar 1 in the Two-Bar Truss problem.
"""
from typing import List
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalConstraintsInterface
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis, ScalerConstraint


class LocalConstraints1(LocalConstraintsInterface):
    """Local constraints class for Two-Bar Truss subsystem 1.

    Evaluates the tensile stress constraint for bar 1.

    Attributes:
        None specific to this class; inherits from LocalConstraintsInterface.
    """

    def __init__(self) -> None:
        """Initialize LocalConstraints1 instance."""
        pass

    def evaluateEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate equality constraints for subsystem 1.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        
        equality_unscaled = []
        # append any equality Local constraints to this list using the responses
        ################################################################
        ###          USER CODE: Equality constraints                 ###
        ################################################################
        # equality_unscaled.append(responses[...])
        
        # scale equality Local constraint evaluation
        scl: List[ScalerConstraint] = [scalers[4]]
        # equality: List[float] = [scl[i].transform(equality_unscaled[i]) for i in range(len(equality_unscaled))]
        
        # or if no Equality Local constraints exist:
        equality = None
        # equality Local constraints needs to be a scaled01 quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################  
        subsystem.set_EqualityLocalConstraintsValue(equality)

    def evaluate_Jacobian_EqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Jacobian of the local equality constraints.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        
        return None

    def evaluate_Hessians_EqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessians of the local equality constraints.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        
        return None

    def evaluateInEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate inequality constraints for subsystem 1.

        Computes the stress constraint: sigma1 / (0.9 * sigma_max) - 1 <= 0.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        
        inequality_unscaled = []
        # append any inequality Local constraints to this list using the responses
        ################################################################
        ###          USER CODE: Inequality constraints               ###
        ################################################################
        inequality_unscaled.append((responses[0] / (0.9 * 480 * 1E6)) - 1.0)
        
        # scale the inequality Local constraint evaluation
        scl: List[ScalerConstraint] = [scalers[5]]
        inequality: List[float] = [scl[i].transform(inequality_unscaled[i]) for i in range(len(inequality_unscaled))]
        # inequality Local constraints needs to be a scaled01 quantity        
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################ 
        subsystem.set_InequalityLocalConstraintsValue(inequality)

    def evaluate_Jacobian_InEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Jacobian of the local inequality constraints.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        # No closed-form Jacobian available (complex physics); return None to let
        # the framework fall back to its internal finite-difference computation.
        return None

    def evaluate_Hessians_InEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessians of the local inequality constraints.

        Args:
            subsystem: The local subsystem basis containing state information.
        """
        # No closed-form Hessian available (complex physics); return None to let
        # the framework fall back to its internal finite-difference computation.
        return None
