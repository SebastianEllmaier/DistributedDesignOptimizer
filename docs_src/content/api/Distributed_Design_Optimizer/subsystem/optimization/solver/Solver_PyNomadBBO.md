---
title: Solver_PyNomadBBO
---

← Back to [solver](index.md)

# Solver_PyNomadBBO

**Source:** [Distributed_Design_Optimizer\subsystem\optimization\solver\Solver_PyNomadBBO.py](Solver_PyNomadBBO_source.md)

PyNomad BBO optimizer module.

This module provides optimization using PyNomad for
black-box optimization.

## Classes

### Solver_PyNomadBBO

> **Inherits from:** [SolverInterface](SolverInterface.md#solverinterface)

> NOMAD Blackbox Optimization solver via PyNomad.

> Implements the MADS (Mesh Adaptive Direct Search) algorithm for derivative-free
> optimization. Supports both continuous and discrete (granular) design variables.
> Handles constraints using Progressive Barrier (PB) or Extreme Barrier (EB) methods.

#### Methods

??? abstract "__init__(self, maxevals: int | None, constraint_handling_method: str, seed: int, vns_mads_search: bool, quad_model_search: bool, eqcon_as_ineqcon_tol: float) → None"
    Initialize the PyNomad optimizer.


    **Args:**
    > maxevals: Maximum number of blackbox evaluations. None for unlimited.  
    > constraint_handling_method: Method for handling constraints.  
    > 'PB' for Progressive Barrier or 'EB' for Extreme Barrier.  
    > seed: Random seed for reproducibility.  
    > vns_mads_search: Whether to enable Variable Neighborhood Search.  
    > Useful for escaping local minima but computationally expensive.  
    > quad_model_search: Whether to enable quadratic model search in the  
    > MADS search phase for proposing new candidate points.  
    > eqcon_as_ineqcon_tol: Tolerance for converting equality constraints  
    > to inequality constraints.  

??? abstract "execute(self, subsystem: [SubSystemInterface](../../SubSystemInterface.md#subsysteminterface)) → [OptimDataBasis](../optimizerdata/OptimDataBasis.md#optimdatabasis)"
    Execute the NOMAD MADS optimization algorithm.


    **Args:**
    > subsystem: The subsystem to optimize containing design variables,  
    > bounds, objectives, and constraints.  


    **Returns:**
    > Optimization results containing optimal design variables and  
    > objective/constraint values.  

