# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Local constraints module for Two-Bar Truss subsystem 2.

Defines the buckling stability constraint for bar 2 (compression member)
in the Two-Bar Truss problem.
"""
from typing import List
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalConstraintsInterface
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis, ScalerConstraint


class LocalConstraints2(LocalConstraintsInterface):
    """Local constraints class for Two-Bar Truss subsystem 2.

    Evaluates the Euler buckling stability constraint for bar 2.

    Attributes:
        None specific to this class; inherits from LocalConstraintsInterface.
    """

    def __init__(self) -> None:
        """Initialize LocalConstraints2 instance."""
        pass

    def evaluateEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate equality constraints for subsystem 2.

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
        scl: List[ScalerConstraint] = [scalers[5]]
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
        """Evaluate inequality constraints for subsystem 2.

        Computes the buckling constraint (sigma2 / sigma_Euler)**2 - 1 <= 0,
        magnitude-compressed via a sign/zero-crossing preserving power map so
        the feasible set is unchanged (see power_ratio below).

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
         
        # Buckling constraint  (sigma2 / sigma_Euler)**2 - 1 <= 0.  At infeasible
        # designs (thin bar + large nodal force) the squared stress ratio reaches
        # O(1e10+), pushing the scaled value outside ScalerConstraint(-500, 500).
        # Compress the magnitude with a sign/zero-crossing preserving power map
        #     EXPR -> sign(EXPR) * |EXPR|**exponent   (strictly increasing, EXPR=1 -> 1)
        # so  power_ratio(EXPR, p) - 1 <= 0  has the SAME feasible set as EXPR - 1 <= 0.
        def power_ratio(expr: float, exponent: float) -> float:
            """Return sign(expr)*|expr|**exponent: magnitude-compressed, sign/zero-crossing preserving."""
            return (1.0 if expr >= 0.0 else -1.0) * abs(expr)**exponent

        inequality_unscaled.append(power_ratio((responses[0] / responses[1])**2, 1.0 / 4.0) - 1.0)
        
        # scale the inequality Local constraint evaluation
        scl: List[ScalerConstraint] = [scalers[6]]
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
