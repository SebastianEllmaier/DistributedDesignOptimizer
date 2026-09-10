# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Optimization controller module.

This module provides the QP-based optimization for the ALADIN
controller subsystem.
"""

from typing import cast
from Distributed_Design_Optimizer.subsystem.optimization import OptimizationBasis
from Distributed_Design_Optimizer.subsystem.optimization.solver import Solver_QP


class OptimizationController(OptimizationBasis):
    """QP-based optimization for the ALADIN controller subsystem.

    Configures OptimizationBasis with a quadratic programming solver and
    exposes it through get_Optimizer so the controller subsystem can populate
    the QP problem matrices (P, q, A, G, h).
    """

    def __init__(self) -> None:
        """Initialize OptimizationController with a QP solver."""
        # Choose your optimizer and its hyperparameters
        super().__init__(Solver_QP(maxevals=10000, constraint_tol=1E-8))

    def get_Optimizer(self) -> Solver_QP:
        """Return the QP solver configured for the controller.

        Returns:
            The quadratic programming solver instance.
        """
        return cast(Solver_QP, self._optimizer)