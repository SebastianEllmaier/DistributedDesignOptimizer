---
title: LocalConstraints0 (Source)
---

← Back to [LocalConstraints0 documentation](LocalConstraints0.md)

# LocalConstraints0 - Source Code

**File:** `userfiles\SSBJ\subsystem0\LocalConstraints0.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Local constraints module for Subsystem 0 in the Supersonic Business Jet (SSBJ) problem.

This module defines the LocalConstraints0 class which implements the local
equality and inequality constraints specific to Subsystem 0 in the distributed
design optimization framework.
"""
from typing import List
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalConstraintsInterface
from Distributed_Design_Optimizer.subsystem.tools import ScalerBasis, ScalerConstraint


class LocalConstraints0(LocalConstraintsInterface):
    """Local constraints class for Subsystem 0 in the Supersonic Business Jet (SSBJ) problem.

    Attributes:
        None specific to this class; inherits from LocalConstraintsInterface.
    """
    def __init__(self) -> None:
        """Initialize the LocalConstraints0 instance."""
        pass

    def evaluateEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate equality local constraints for Subsystem 0.

        Computes the equality constraint values from the subsystem responses,
        scales them using the appropriate ScalerConstraint, and stores the
        result in the subsystem.

        Args:
            subsystem: The local subsystem instance providing responses
                and scaling variables.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        
        equality_unscaled = []        
        # append any equality Local constraints to this list using the responses        
        ################################################################
        ###          USER CODE: Equality constraints                  ###
        ################################################################
        
        # no Equality Local constraints exist:
        equality = None
       
        # equality Local constraints needs to be a scaled01 quantity        
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        subsystem.set_EqualityLocalConstraintsValue(equality)

    def evaluate_Jacobian_EqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Jacobian of the local equality constraints.

        Args:
            subsystem: The local subsystem instance.
        """
        
        return None
    
    def evaluate_Hessians_EqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessians of the local equality constraints.

        Args:
            subsystem: The local subsystem instance.
        """
        
        return None
        
    def evaluateInEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate inequality local constraints for Subsystem 0.

        Computes the inequality constraint values from the subsystem responses,
        scales them using the appropriate ScalerConstraint, and stores the
        result in the subsystem.

        Args:
            subsystem: The local subsystem instance providing responses
                and scaling variables.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        
        inequality_unscaled = []
        # append any inequality Local constraints to this list using the responses
        ################################################################
        ###          USER CODE: Inequality constraints               ###
        ################################################################
        
        range_value = responses[0]  # [nmi]
         
        inequality_unscaled.append(-range_value / 2000.0 + 1.0)  # range constraint (range >= 2000 [nmi]) 
        
        # scale the inequality Local constraint evaluation
        scl: List[ScalerConstraint] = [scalers[7]]
        inequality: List[float] = [scl[i].transform(inequality_unscaled[i]) for i in range(len(inequality_unscaled))]
        
        # inequality Local constraints needs to be a scaled01 quantity        
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        subsystem.set_InequalityLocalConstraintsValue(inequality)

    def evaluate_Jacobian_InEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Jacobian of the local inequality constraints.

        Args:
            subsystem: The local subsystem instance.
        """
        
        return None
    
    def evaluate_Hessians_InEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessians of the local inequality constraints.

        Args:
            subsystem: The local subsystem instance.
        """
        
        return None
```
