---
title: ControllerSubSystemBasis
---

← Back to [subsystem](index.md)

# ControllerSubSystemBasis

**Source:** [Distributed_Design_Optimizer\subsystem\ControllerSubSystemBasis.py](ControllerSubSystemBasis_source.md)

Controller subsystem basis module.

This module provides the base class for controller subsystems in
hierarchical distributed optimization.

## Classes

### ControllerSubSystemBasis

> **Inherits from:** [SubSystemBasis](SubSystemBasis.md#subsystembasis)

> A ControllerSubSystemBasis object with id = 'C' contains all necessary data for a controller.

> It includes methods to optimize the subsystem and to couple it to
> neighboring subsystems.

#### Methods

??? abstract "__init__(self, neighborid: List[str]) → None"
    Create a new instance of ControllerSubSystemBasis.


    **Args:**
    > neighborid: List of identifiers for neighboring subsystems.  

??? abstract "initialize_Initial_Optimdata_at_Beginning(self) → [ControllerOptimData](optimization/optimizerdata/ControllerOptimData.md#controlleroptimdata)"
    Return a ControllerOptimData object based on the subsystem's current state.


    **Returns:**
    > A ControllerOptimData with all fields set to None.  

??? abstract "mapToController(self) → None"
    Controller does not map to itself.

??? abstract "run_updateCouplingParameters_outerLoop_job(self) → None"
    Update coupling parameters in the outer loop after the inner loop.

??? abstract "run_prepare_updateCouplingParameters_job(self) → None"
    Prepare coupling parameters update after inner loop is finished.

??? abstract "appendtohistory(self) → None"
    Append the current controller state to the history.

??? abstract "evaluateTotalObjective(self) → None"
    Evaluate the total objective function (coordination only, no local objective).

??? abstract "evaluateTotalConstraint(self) → None"
    Evaluate the total constraints (coordination only, no local constraints).

??? abstract "evaluateTotalObjectiveAndTotalConstraint(self) → None"
    Evaluate both total objective and total constraint in a single call.

    This method combines evaluateTotalObjective() and evaluateTotalConstraint()
    to avoid redundant mapping operations when both values are needed.

??? abstract "compute_KKT_system_matrix_and_bounds(self) → List[List[List[float]] | List[Tuple[float | None, float | None]]]"
    Return the total linear KKT system matrix.


    **Returns:**
    > A list containing the constraint matrix and bounds for the KKT system.  

??? abstract "decompose_KKT_multipliers(self, all_multipliers: List[float]) → None"
    Decompose the KKT system solution into individual multiplier groups.

    The solution stored in optimization_result is separated into different
    parts (e.g. local inequality constraints) and stored in self._optimdata.


    **Args:**
    > all_multipliers: Total accumulation of all multipliers (only for constraints, not for objective)  

??? abstract "evaluate_Gradient_TotalObjective(self) → None"
    Evaluate the gradient of the total objective (coordination only, if it exists).


    **Returns:**
    > None. The total objective gradient is stored in self._optimdata.  

??? abstract "evaluate_Jacobian_TotalEqualityConstraints(self) → None"
    Evaluate the Jacobian of the total equality constraints if it exists.


    **Returns:**
    > None. The Jacobian is stored in self._optimdata.  

??? abstract "evaluate_Jacobian_TotalInEqualityConstraints(self) → None"
    Evaluate the Jacobian of the total inequality constraints if it exists.


    **Returns:**
    > None. The Jacobian is stored in self._optimdata.  

??? abstract "print_startup_summary(self) → None"
    Print controller subsystem info at startup.

??? abstract "print_end_of_innerloop_iteration(self) → None"
    Print controller subsystem results at the end of an inner loop iteration.

??? abstract "print_termination_summary(self) → None"
    Print controller subsystem results at the end of the optimization run.

??? abstract "update_state(self, other_subsystem: [ControllerSubSystemBasis](ControllerSubSystemBasis.md#controllersubsystembasis)) → None"
    Update the state of this ControllerSubSystemBasis instance with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.

    The update preserves memory addresses by modifying attribute contents in-place where
    possible, rather than reassigning references. This is essential for maintaining object
    identity across the multiprocessing boundary.


    **Args:**
    > other_subsystem: The source ControllerSubSystemBasis containing updated values  
    > from parallel execution.  

