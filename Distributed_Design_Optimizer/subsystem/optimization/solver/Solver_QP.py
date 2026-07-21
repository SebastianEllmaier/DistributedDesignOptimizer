# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
#
# Additional Request:
# We kindly request that any modifications or changes to the source code be
# shared with us by submitting them as pull requests to our GitHub repository.
# This request is not legally binding but is made in the spirit of
# collaboration and open-source development.
"""QP solver implementation for ALADIN controller optimization subproblems."""
import numpy as np
from scipy.sparse import csc_matrix
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print, ddo_print_border
from qpsolvers import solve_problem
from qpsolvers.problem import Problem
from qpsolvers.solution import Solution
import time

from Distributed_Design_Optimizer.subsystem.SubSystemInterface import SubSystemInterface

from Distributed_Design_Optimizer.subsystem.optimization.optimizerdata.ControllerOptimData import ControllerOptimData

from Distributed_Design_Optimizer.subsystem.optimization.solver import SolverInterface

class Solver_QP(SolverInterface):
    """
    This class implements the solution of a QP optimization subproblem.
    """
    
    def __init__(self, 
                 maxevals: int | None,
                 constraint_tol: float  # 1E-8 as default
                 ):
        """
        Initialize the QP solver.

        Initialize the quantities
        - P (QP matrix)
        - q (QP linear term)
        - A (QP linear equality constraints)

        The derived QP is solved via the python package.

        Args:
            maxevals: Maximum number of function evaluations, or None for unlimited.
            constraint_tol: Tolerance for constraint validation.
        """
        
        self._P: np.typing.ArrayLike | None = None
        self._q: np.typing.ArrayLike | None = None
        self._A: np.typing.ArrayLike | None = None
        self._G: np.typing.ArrayLike | None = None
        self._h: np.typing.ArrayLike | None = None
        
        # Solver specific information
        if isinstance(maxevals, int) and (maxevals > 0):
            self._maxevals = maxevals
        elif maxevals is None:
            self._maxevals = maxevals
        else:
            raise NotImplementedError(f"{DDO_Color}Unknown maxevals for Solver_QP{Reset}")
        
        if isinstance(constraint_tol, float) and (constraint_tol > 0):
            self._constraint_tol = constraint_tol
        else:
            raise NotImplementedError(f"{DDO_Color}Unknown constraint_tol for Solver_QP{Reset}")

    ###########################################################################
    # Quadratic matrix P of the QP
    ###########################################################################

    def get_P(self) -> np.typing.ArrayLike | None:
        """
        Returns the QP matrix P.

        Returns:
            np.typing.ArrayLike | None: The QP matrix P, or None if not set.
        """

        return self._P

    def set_P(self, P_in: np.typing.ArrayLike) -> None:
        """
        Sets the QP matrix P.

        Args:
            P_in (np.typing.ArrayLike): The QP matrix P to set.
        """

        self._P = P_in

    ###########################################################################
    # Linear vector q of the QP
    ###########################################################################

    def get_q(self) -> np.typing.ArrayLike | None:
        """
        Returns the QP linear term q.

        Returns:
            np.typing.ArrayLike | None: The QP linear term q, or None if not set.
        """

        return self._q

    def set_q(self, q_in: np.typing.ArrayLike) -> None:
        """
        Sets the QP linear term q.

        Args:
            q_in (np.typing.ArrayLike): The QP linear term q to set.
        """

        self._q = q_in

    ###########################################################################
    # Linear equality constraints A of the QP
    ###########################################################################

    def get_A(self) -> np.typing.ArrayLike | None:
        """
        Returns the QP linear equality constraints A.

        Returns:
            np.typing.ArrayLike | None: The QP linear equality constraints A, or None if not set.
        """

        return self._A

    def set_A(self, A_in: np.typing.ArrayLike) -> None:
        """
        Sets the QP linear equality constraints A.

        Args:
            A_in (np.typing.ArrayLike): The QP linear equality constraints A to set.
        """

        self._A = A_in
        
    def get_G(self) -> np.typing.ArrayLike | None:
        """
        Returns the QP linear inequality constraints G.

        Returns:
            np.typing.ArrayLike | None: The QP linear inequality constraints G, or None if not set.
        """

        return self._G

    def set_G(self, G_in: np.typing.ArrayLike) -> None:
        """
        Sets the QP linear inequality constraints G.

        Args:
            G_in (np.typing.ArrayLike): The QP linear inequality constraint matrix G to set.
        """

        self._G = G_in

    def get_h(self) -> np.typing.ArrayLike | None:
        """
        Returns the QP inequality constraint RHS vector h.

        Returns:
            np.typing.ArrayLike | None: The RHS vector h for G x <= h, or None if not set.
        """

        return self._h

    def set_h(self, h_in: np.typing.ArrayLike) -> None:
        """
        Sets the QP inequality constraint RHS vector h.

        Args:
            h_in (np.typing.ArrayLike): The RHS vector h for G x <= h to set.
        """

        self._h = h_in
        
    def execute(self, subsystem: SubSystemInterface) -> ControllerOptimData:
        """
        Execute the QP solver to solve the QP.

        Args:
            subsystem (SubSystemInterface): The subsystem containing the optimization problem.

        Returns:
            The optimization results for the ALADIN controller.
        """
        
        # Check if the subsystem is a controller or not
        from Distributed_Design_Optimizer.subsystem.ControllerSubSystemALADIN import ControllerSubSystemALADIN
        if not isinstance(subsystem, ControllerSubSystemALADIN):
            
            # Raise error
            raise NotImplementedError("Only ALADIN controller can access the QP solver.")
        
        # Get the quantities
        P: np.typing.ArrayLike = np.atleast_2d(np.asarray(self.get_P(), dtype=float))
        q: np.typing.ArrayLike = np.atleast_1d(np.asarray(self.get_q(), dtype=float))
        A: np.typing.ArrayLike = self.get_A()
        G: np.typing.ArrayLike = self.get_G()
        h: np.typing.ArrayLike = self.get_h()
        
        # Build the QP problem in qpsolvers notation:
        #   min  (1/2) x^T P x + q^T x
        #   s.t. A x  = b   (linear equality constraints)
        #        G x <= h   (linear inequality constraints)
        # Initialize all constraint matrices/vectors to None;
        # they are only populated if the corresponding constraint is active.
        A_val = None  # equality constraint matrix (n_eq x n_vars)
        b_val = None  # equality constraint RHS vector (n_eq,) — zero vector (Ax = 0)
        G_val = None  # inequality constraint matrix (n_ineq x n_vars)
        h_val = None  # inequality constraint RHS vector (n_ineq,) — zero vector (Gx <= 0)

        # Populate A and b if equality constraints are present
        if A is not None and np.asarray(A).size > 0 and np.asarray(A).shape[0] > 0:
            A_val = np.atleast_2d(np.asarray(A, dtype=float))
            b_val: np.typing.ArrayLike = np.zeros(A_val.shape[0])  # RHS is zero: A x = 0

        # Populate G and h if inequality constraints are present
        if G is not None and np.asarray(G).size > 0 and np.asarray(G).shape[0] > 0:
            G_val = np.atleast_2d(np.asarray(G, dtype=float))
            # Use provided h if available, otherwise default to zero vector (G x <= 0)
            if h is not None and np.asarray(h).size == G_val.shape[0]:
                h_val: np.typing.ArrayLike = np.atleast_1d(np.asarray(h, dtype=float))
            else:
                h_val: np.typing.ArrayLike = np.zeros(G_val.shape[0])

        # Construct the Problem object; None entries are ignored by qpsolvers
        
        # Convert P, G, A into csc-sparse-matrices for QPALM performance
        P_csc = csc_matrix(P)
        G_csc = csc_matrix(G_val) if G_val is not None else None
        A_csc = csc_matrix(A_val) if A_val is not None else None
        problem: Problem = Problem(P_csc, q, A=A_csc, b=b_val, G=G_csc, h=h_val)
        
        # Solve the QP problem, with solver QPALM
        # Tighten QPALM tolerances to match constraint_tol so solutions satisfy constraints
        starttime = time.time()
        solution: Solution = solve_problem(problem=problem, solver="qpalm", verbose=True,
                                           eps_abs=self._constraint_tol, 
                                           eps_rel=0.0)
        delta_d: np.typing.ArrayLike = solution.x
        finishtime = time.time()
        
        subsystem.set_DesignVariables(delta_d.tolist())
        subsystem.evaluateTotalObjective()
        subsystem.evaluateTotalConstraint()
        
        # Map QPALM solver status to exitflag (1 = good, 0 = bad) and extract solver message.
        # QPALM status codes:
        #   solved                      – Solution found
        #   dual terminated             – Dual terminated
        #   maximum iterations reached  – Iteration limit reached
        #   primal infeasible           – Problem is primal infeasible
        #   dual infeasible             – Problem is dual infeasible
        #   time limit reached          – Time limit reached
        #   unsolved                    – Not solved
        #   error                       – Numerical/internal error
        _qpalm_info = solution.extras.get('info', None)
        if _qpalm_info is not None:
            solver_status = str(_qpalm_info.status)
        else:
            # Fallback: derive status from solution.found
            solver_status = "solved" if solution.found else "unsolved"
        status_msg = f"QPALM status: {solver_status}"
        
        # Statuses that indicate numerical difficulties
        _NUMERICAL_WARNING_STATUSES = {"error"}
        # Statuses that indicate acceptable but suboptimal termination
        _ALMOST_STATUSES = {"dual terminated"}
        # Statuses that indicate hard failures
        _FAILURE_STATUSES = {"primal infeasible", "dual infeasible", "maximum iterations reached", "time limit reached", "unsolved"}
        
        if solver_status in _NUMERICAL_WARNING_STATUSES:
            ddo_print_border()
            ddo_print(f"WARNING: QP solver (QPALM) returned status '{solver_status}' for Subsystem {subsystem.get_SUBSYSTEMID()}. "
                      f"This may indicate ill-conditioning of the QP subproblem. "
                      f"One possible remedy is the introduction of slack variables (see Houska et al., 'An Augmented Lagrangian Based Algorithm for Distributed Nonconvex Optimization').")
            ddo_print_border()
        elif solver_status in _ALMOST_STATUSES:
            ddo_print_border()
            ddo_print(f"WARNING: QP solver (QPALM) returned status '{solver_status}' for Subsystem {subsystem.get_SUBSYSTEMID()}. "
                      f"The solution may be inaccurate. Consider tightening solver tolerances or checking problem scaling.")
            ddo_print_border()
        elif solver_status in _FAILURE_STATUSES:
            ddo_print_border()
            ddo_print(f"WARNING: QP solver (QPALM) failed with status '{solver_status}' for Subsystem {subsystem.get_SUBSYSTEMID()}. "
                      f"The QP subproblem could not be solved successfully.")
            ddo_print_border()
        
        exitflag = 1
        # Check equality constraints with numpy.isclose
        if subsystem.get_TotalConstraintEqValue() is not None and np.all(np.isclose(np.array(subsystem.get_TotalConstraintEqValue()), 0.0, atol=self._constraint_tol)):
            eq_msg = "Equality TotalConstraints of Subsystem "+subsystem.get_SUBSYSTEMID()+" are VALIDATED!"
        else:
            eq_msg = "Equality TotalConstraints of Subsystem "+subsystem.get_SUBSYSTEMID()+" are NOT VALIDATED!" 
            exitflag = 0 
                      
        # Check inequality constraints with tolerance
        if subsystem.get_TotalConstraintIneqValue() is None:
            ineq_msg = " "
        elif (subsystem.get_TotalConstraintIneqValue() is not None
                and np.all(np.logical_or(np.array(subsystem.get_TotalConstraintIneqValue()) <= 0.0, 
                                         np.isclose(np.array(subsystem.get_TotalConstraintIneqValue()), 0, atol=self._constraint_tol)))):
            ineq_msg = " Inequality TotalConstraints of Subsystem "+subsystem.get_SUBSYSTEMID()+" are VALIDATED!"
        else:
            ineq_msg = "Inequality TotalConstraints of Subsystem "+subsystem.get_SUBSYSTEMID()+" are NOT VALIDATED!"
            exitflag = 0
            raise ValueError(f'{DDO_Color}TOTALCONSTRAINTS VIOLATIONS DETECTED!{Reset}')
        
        # Override exitflag to 0 if solver reported a hard failure or numerical error
        if solver_status in _FAILURE_STATUSES or solver_status in _NUMERICAL_WARNING_STATUSES:
            exitflag = 0
        
        # Extract number of solver iterations from QPALM extras
        if _qpalm_info is not None:
            numberofdesignvariableevaluations: int | None = getattr(_qpalm_info, 'iter', None)
        else:
            numberofdesignvariableevaluations: int | None = None
            
        message = solver_status + " " + eq_msg + " " + ineq_msg + " " + status_msg
        
        # Create an optimdata object
        optimdata: ControllerOptimData = ControllerOptimData(optimizer_type="QP-Solver QPALM", 
                                                             designvariables=subsystem.get_DesignVariables(),
                                                             designvariables_unscaled=None,
                                                             lowerbounds=None,
                                                             lowerbounds_scaled=None,
                                                             upperbounds=None,
                                                             upperbounds_scaled=None, 
                                                             totalobjectivevalue=subsystem.get_TotalObjectiveValue(), 
                                                             coordinationobjectivevalue=subsystem.get_CoordinationObjectiveValue(), 
                                                             totalconstrainteqvalue=subsystem.get_TotalConstraintEqValue(),
                                                             totalconstraintineqvalue=subsystem.get_TotalConstraintIneqValue(), 
                                                             coordinationequalityconstraintvalue=subsystem.get_CoordinationEqualityConstraintValue(),
                                                             coordinationinequalityconstraintvalue=subsystem.get_CoordinationInequalityConstraintValue(),
                                                             gradient_coordinationobjective=(P_csc @ delta_d + q).tolist() if P_csc is not None and q is not None else None,
                                                             jacobian_coordinationequalityconstraints=A.tolist() if A is not None else None, 
                                                             jacobian_coordinationinequalityconstraints=G.tolist() if G is not None else None, 
                                                             gradient_totalobjective=(P_csc @ delta_d + q).tolist() if P_csc is not None and q is not None else None,
                                                             jacobian_totalequalityconstraints=A.tolist() if A is not None else None,
                                                             jacobian_totalinequalityconstraints=G.tolist() if G is not None else None,
                                                             jacobian_lowerbounds=None,
                                                             jacobian_upperbounds=None,
                                                             multipliers_lowerbounds=None,
                                                             multipliers_upperbounds=None,
                                                             multipliers_coordination_equality_constraints=solution.y.tolist() if solution.y is not None else None,  # For QPALM, solution.y are the multipliers for equality constraints
                                                             multipliers_coordination_inequality_constraints=solution.z.tolist() if solution.z is not None else None,  # For QPALM, solution.z are the multipliers for inequality constraints
                                                             activecoordinationinequalityconstraints=np.isclose(np.array(subsystem.get_CoordinationInequalityConstraintValue()), 0.0, atol=self._constraint_tol).tolist() if subsystem.get_CoordinationInequalityConstraintValue() is not None else None,
                                                             activelowerbounds=None,
                                                             activeupperbounds=None,
                                                             exitflag=exitflag,
                                                             message=message,
                                                             optimization_numberofdesignvariableevaluations=numberofdesignvariableevaluations,
                                                             optimization_runtime=finishtime - starttime,
                                                             numberofactiveinequalityconstraints=None, 
                                                             numberofactivebounds=None
                                                             )
        
        # Return the optimdata
        return optimdata
        
        
        
        
        
