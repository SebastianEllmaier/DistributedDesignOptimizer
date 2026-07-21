---
title: Solver_QP
---

← Back to [solver](index.md)

# Solver_QP

**Source:** [Distributed_Design_Optimizer\subsystem\optimization\solver\Solver_QP.py](Solver_QP_source.md)

QP solver implementation for ALADIN controller optimization subproblems.

## Classes

### Solver_QP

> **Inherits from:** [SolverInterface](SolverInterface.md#solverinterface)

> This class implements the solution of a QP optimization subproblem.

#### Methods

??? abstract "__init__(self, maxevals: int | None, constraint_tol: float)"
    Initialize the QP solver.

    Initialize the quantities
    - P (QP matrix)
    - q (QP linear term)
    - A (QP linear equality constraints)

    The derived QP is solved via the python package.


    **Args:**
    > maxevals: Maximum number of function evaluations, or None for unlimited.  
    > constraint_tol: Tolerance for constraint validation.  

??? abstract "get_P(self) → np.typing.ArrayLike | None"
    Returns the QP matrix P.


    **Returns:**
    > np.typing.ArrayLike | None: The QP matrix P, or None if not set.  

??? abstract "set_P(self, P_in: np.typing.ArrayLike) → None"
    Sets the QP matrix P.


    **Args:**
    > P_in (np.typing.ArrayLike): The QP matrix P to set.  

??? abstract "get_q(self) → np.typing.ArrayLike | None"
    Returns the QP linear term q.


    **Returns:**
    > np.typing.ArrayLike | None: The QP linear term q, or None if not set.  

??? abstract "set_q(self, q_in: np.typing.ArrayLike) → None"
    Sets the QP linear term q.


    **Args:**
    > q_in (np.typing.ArrayLike): The QP linear term q to set.  

??? abstract "get_A(self) → np.typing.ArrayLike | None"
    Returns the QP linear equality constraints A.


    **Returns:**
    > np.typing.ArrayLike | None: The QP linear equality constraints A, or None if not set.  

??? abstract "set_A(self, A_in: np.typing.ArrayLike) → None"
    Sets the QP linear equality constraints A.


    **Args:**
    > A_in (np.typing.ArrayLike): The QP linear equality constraints A to set.  

??? abstract "get_G(self) → np.typing.ArrayLike | None"
    Returns the QP linear inequality constraints G.


    **Returns:**
    > np.typing.ArrayLike | None: The QP linear inequality constraints G, or None if not set.  

??? abstract "set_G(self, G_in: np.typing.ArrayLike) → None"
    Sets the QP linear inequality constraints G.


    **Args:**
    > G_in (np.typing.ArrayLike): The QP linear inequality constraint matrix G to set.  

??? abstract "get_h(self) → np.typing.ArrayLike | None"
    Returns the QP inequality constraint RHS vector h.


    **Returns:**
    > np.typing.ArrayLike | None: The RHS vector h for G x <= h, or None if not set.  

??? abstract "set_h(self, h_in: np.typing.ArrayLike) → None"
    Sets the QP inequality constraint RHS vector h.


    **Args:**
    > h_in (np.typing.ArrayLike): The RHS vector h for G x <= h to set.  

??? abstract "execute(self, subsystem: [SubSystemInterface](../../SubSystemInterface.md#subsysteminterface)) → [ControllerOptimData](../optimizerdata/ControllerOptimData.md#controlleroptimdata)"
    Execute the QP solver to solve the QP.


    **Args:**
    > subsystem (SubSystemInterface): The subsystem containing the optimization problem.  


    **Returns:**
    > The optimization results for the ALADIN controller.  

