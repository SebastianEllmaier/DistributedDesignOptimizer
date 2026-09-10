# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Optimization configuration module for Two-Bar Truss subsystem 2.

Configures the local optimization algorithm for bar 2 sizing in the
Two-Bar Truss distributed optimization problem.
"""
from Distributed_Design_Optimizer.subsystem.optimization import OptimizationBasis
from Distributed_Design_Optimizer.subsystem.optimization.solver import (
                                                                        # Solver_SCBO,
                                                                        # Solver_Scipy,
                                                                        # Solver_CMA,
                                                                        # Solver_IPOPT,
                                                                        Solver_PyNomadBBO,
                                                                        # Solver_Pyomo,
                                                                        # Solver_Fmincon
                                                                        )

class Optimization2(OptimizationBasis):
    """Optimization configuration class for Two-Bar Truss subsystem 2.

    Configures the local optimizer (PyNomadBBO by default) and its
    hyperparameters for solving the bar 2 sizing subproblem.

    Attributes:
        _optimizer: The configured optimizer instance.
    """

    def __init__(self) -> None:
        """Initialize Optimization2 with selected optimizer settings."""
        
        # Choose you optimizer and its hyperparameters
        
        # super().__init__(Solver_SCBO(option_1=None))
        
        # super().__init__(Solver_Scipy(method="trust-constr",
        #                               constraint_jac="2-point",
        #                               constraint_keep_feasible=False,
        #                               maxiter=500))
        
        # super().__init__(Solver_CMA(maxevals=10000,
        #                             maxiter=1000,
        #                             tolfun=1e-9,
        #                             tolx=1e-9,
        #                             seed=2,
        #                             adaptsigma=True,
        #                             elitism=False,
        #                             eqcon_as_ineqcon_tol=1E-8))
        
        super().__init__(Solver_PyNomadBBO(maxevals=10000,
                                           constraint_handling_method="PB",
                                           seed=1,
                                           vns_mads_search=False,
                                           quad_model_search=False,
                                           eqcon_as_ineqcon_tol=1E-8))
        
        # super().__init__(Solver_IPOPT(maxiter=1000,
        #                               acceptable_tol=1e-8,
        #                               constraint_jac="2-point",
        #                               constraint_keep_feasible=False))
        
        # super().__init__(Solver_Pyomo(option_1=None,
        #                               option_2=None))
        
        # super().__init__(Solver_Fmincon(method="active_set",
        #                                 maxiter=1000,
        #                                 maxfunevals=10000,
        #                                 tolfun=1e-9,
        #                                 tolcon=1e-8))
