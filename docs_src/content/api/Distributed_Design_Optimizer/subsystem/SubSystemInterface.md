---
title: SubSystemInterface
---

← Back to [subsystem](index.md)

# SubSystemInterface

**Source:** [Distributed_Design_Optimizer\subsystem\SubSystemInterface.py](SubSystemInterface_source.md)

Subsystem interface module.

This module defines the abstract interface for all subsystem classes
in the distributed optimization framework.

## Classes

### SubSystemInterface

> **Inherits from:** `ABC`

> Abstract interface for subsystems in the distributed optimization framework.

> Defines the contract for subsystem implementations including design variable
> management, objective/constraint evaluation, optimization, and coupling
> parameter handling.

#### Methods

??? abstract "validate_inputs(self) → None"
    Validate the components handed to this subsystem by its coordination method.


    **Raises:**
    > ValueError: If a provided component is not compatible with the subsystem.  

??? abstract "get_SUBSYSTEMID(self) → str"
    Get the identity of the subsystem within the hierarchy.


    **Returns:**
    > The subsystem identifier.  

??? abstract "get_NeighborId(self) → List[str]"
    Get the neighbor IDs for this subsystem.


    **Returns:**
    > List of neighbor identifiers.  

??? abstract "set_Name(self, name: str) → None"
    Set the use-case name used when saving the subsystem history.


    **Args:**
    > name: The use-case name identifier.  

??? abstract "get_Name(self) → str"
    Return the use-case name used when saving the subsystem history.


    **Returns:**
    > The use-case name identifier.  

??? abstract "set_HistoryFolderPath(self, history_folder_path: str) → None"
    Set the folder path used when saving the subsystem history.


    **Args:**
    > history_folder_path: The absolute path to the historyfiles folder.  

??? abstract "get_MiddleLevels(self) → List[[MiddleLevelDataStorageInterface](../middlelevel/MiddleLevelDataStorageInterface.md#middleleveldatastorageinterface)] | List[[MiddleLevelDataStorageProxy](../middlelevel/MiddleLevelDataStorageProxy.md#middleleveldatastorageproxy)]"
    Return the middle-level data storage interfaces.


    **Returns:**
    > List of middle-level data storage interfaces or proxies.  

??? abstract "set_MiddleLevels(self, middlelevels: List[[MiddleLevelDataStorageInterface](../middlelevel/MiddleLevelDataStorageInterface.md#middleleveldatastorageinterface)] | List[[MiddleLevelDataStorageProxy](../middlelevel/MiddleLevelDataStorageProxy.md#middleleveldatastorageproxy)]) → None"
    Set the middle-level data storage interfaces.


    **Args:**
    > middlelevels: List of middle-level data storage interfaces or proxies.  

??? abstract "get_OuterLoop_Itr(self) → int"
    Return the current outer loop iteration number.


    **Returns:**
    > The current outer loop iteration number.  

??? abstract "get_InnerLoop_Itr(self) → int"
    Return the current inner loop iteration number.


    **Returns:**
    > The current inner loop iteration number.  

??? abstract "get_InnerLoop_Itr_Runtime(self) → float | None"
    Return the inner loop iteration runtime.


    **Returns:**
    > The inner loop iteration runtime.  

??? abstract "get_InnerLoop_Itr_NumberOfDesignVariableEvaluations(self) → int | None"
    Return the number of design variable evaluations.


    **Returns:**
    > The number of design variable evaluations.  

??? abstract "set_OuterLoop_Itr(self, outerloop_itr_in: int) → None"
    Set the outer loop iteration number.


    **Args:**
    > outerloop_itr_in: The outer loop iteration number to set.  

??? abstract "set_InnerLoop_Itr(self, innerloop_itr_in: int) → None"
    Set the inner loop iteration number.


    **Args:**
    > innerloop_itr_in: The inner loop iteration number to set.  

??? abstract "set_InnerLoop_Itr_Runtime(self, innerloop_itr_runtime_in: float) → None"
    Set the inner loop iteration runtime.


    **Args:**
    > innerloop_itr_runtime_in: The inner loop iteration runtime to set.  

??? abstract "set_InnerLoop_Itr_NumberOfDesignVariableEvaluations(self, innerloop_itr_numberofdesignvariableevaluations_in: int) → None"
    Set the number of design variable evaluations.


    **Args:**
    > innerloop_itr_numberofdesignvariableevaluations_in: The number of design variable evaluations to set.  

??? abstract "get_SubsystemHistory(self) → Deque[[SubSystemHistoryEntry](historyentry/SubSystemHistoryEntry.md#subsystemhistoryentry)]"
    Return the subsystem history.


    **Returns:**
    > The subsystem history.  

??? abstract "CopyToMiddleLevel(self) → None"
    Copy coupling parameters to the shared middle-level data storage.

??? abstract "CopyFromMiddleLevel(self) → None"
    Copy coupling data from the shared middle-level data storage.

??? abstract "run_innerloop_job(self) → None"
    Execute the inner loop job.

??? abstract "run_updateCouplingParameters_innerLoop_job(self) → None"
    Update coupling parameters in the inner loop.

??? abstract "run_updateCouplingParameters_outerLoop_job(self) → None"
    Update coupling parameters in the outer loop.

??? abstract "run_prepare_updateCouplingParameters_job(self) → None"
    Prepare coupling parameters update after inner loop.

??? abstract "appendtohistory(self) → None"
    Append current state to the subsystem history.

??? abstract "savesubsystemhistory(self) → None"
    Save the subsystem history to a dill file.

    The use-case name is read from the subsystem's own state (set via
    set_Name), keeping a no-argument API consistent with the
    coordinator-side history save.

??? abstract "set_LowerBounds_Unscaled(self, lowerbounds: List[float]) → None"
    Set the lower bounds of the design variables (unscaled values).


    **Args:**
    > lowerbounds: Lower bound values (unscaled).  

??? abstract "get_LowerBounds_Unscaled(self) → List[float] | None"
    Get the lower bounds of the design variables (unscaled values).


    **Returns:**
    > Lower bound values (unscaled).  

??? abstract "set_UpperBounds_Unscaled(self, upperbounds: List[float]) → None"
    Set the upper bounds of the design variables (unscaled values).


    **Args:**
    > upperbounds: Upper bound values (unscaled).  

??? abstract "get_UpperBounds_Unscaled(self) → List[float] | None"
    Get the upper bounds of the design variables (unscaled values).


    **Returns:**
    > Upper bound values (unscaled).  

??? abstract "updateSubsystemfromOptimdata(self, optimdata: [OptimDataBasis](optimization/optimizerdata/OptimDataBasis.md#optimdatabasis)) → None"
    After optimization, update subsystem (including controller) based on result stored in OptimDataBasis object optimdata.


    **Args:**
    > optimdata: The optimization data containing updated values.  

??? abstract "updateOptimdatafromSubsystem(self) → None"
    Update the optimdata object with the information from the state of the subsystem.

    This should only be called if an optimdata object
    was created and should be modified afterwards
    (e.g. in initialization, where the optimdata object
    has None fields).

??? abstract "copy_Coupling_Past_outerloop_itr(self, outerloop_itr_before: int) → List[[CouplingParametersInterface](couplingparameters/CouplingParametersInterface.md#couplingparametersinterface)]"
    Copy the coupling from a past outer loop iteration.


    **Args:**
    > outerloop_itr_before: Number of iterations to go back.  


    **Returns:**
    > List of coupling parameters from the specified past iteration.  

??? abstract "copy_Coupling_Previous_outerloop_itr(self) → List[[CouplingParametersInterface](couplingparameters/CouplingParametersInterface.md#couplingparametersinterface)]"
    Copy the coupling from the previous outer loop iteration.


    **Returns:**
    > List of coupling parameters from the previous iteration.  

??? abstract "copy_TotalObjective_Previous_outer_or_innerloop_itr(self) → float | None"
    Copy the total objective from a previous iteration.


    **Returns:**
    > Total objective value from the previous iteration, or None if not found.  

??? abstract "copy_DesignVariablesUnscaled_Previous_outerloop_itr(self) → List[float] | None"
    Copy the unscaled design variables from the previous outer loop iteration.


    **Returns:**
    > Unscaled design variables, or None if not found.  

??? abstract "copy_DesignVariables_Previous_outerloop_itr(self) → List[float] | None"
    Copy the scaled design variables from the previous outer loop iteration.


    **Returns:**
    > Scaled design variables, or None if not found.  

??? abstract "copy_DesignVariables_Previous_innerloop_itr(self) → List[float] | None"
    Copy the scaled design variables from the previous inner loop iteration.


    **Returns:**
    > Scaled design variables, or None if not found.  

??? abstract "copy_DesignVariablesUnscaled_Previous_innerloop_itr(self) → List[float] | None"
    Copy the unscaled design variables from the previous inner loop iteration.


    **Returns:**
    > Unscaled design variables, or None if not found.  

??? abstract "set_DesignVariables(self, designvariables: List[float]) → None"
    Set the design variables of the subsystem (scaled01 values).


    **Args:**
    > designvariables: Design variable values (scaled to [0, 1]).  

??? abstract "get_DesignVariables(self) → List[float] | None"
    Get the design variables of the subsystem (scaled01 values).


    **Returns:**
    > Design variable values (scaled to [0, 1]).  

??? abstract "get_DesignVariables_Unscaled(self) → List[float] | None"
    Get the design variables of the subsystem (unscaled values).


    **Returns:**
    > Design variable values (unscaled).  

??? abstract "set_DesignVariables_Granularity(self, designvariables_granularity: List[float]) → None"
    Set the granularity of the design variables.


    **Args:**
    > designvariables_granularity: Granularity values where 0.0 means continuous.  

??? abstract "get_DesignVariables_Granularity(self) → List[float] | None"
    Get the granularity of the design variables.


    **Returns:**
    > Granularity values where 0.0 means continuous.  

??? abstract "mapToCouplingParameters(self) → None"
    Map the physical responses onto a neighbor.

??? abstract "mapToController(self) → None"
    Map necessary coupling information from neighbors to controller; None, if no controller.

??? abstract "evaluateTotalObjective(self) → None"
    Evaluate the total objective function value.

??? abstract "set_TotalObjectiveValue(self, totalobjectivevalue: float | None) → None"
    Store the total objective value after computation.

    Note: This value is updated after each solver iteration and may not be final.


    **Args:**
    > totalobjectivevalue: The total objective value.  

??? abstract "get_TotalObjectiveValue(self) → float | None"
    Get the total objective value.


    **Returns:**
    > The total objective value, or None if not yet computed.  

??? abstract "evaluateCoordinationObjective(self) → None"
    Evaluate objective inconsistency.

??? abstract "set_CoordinationObjectiveValue(self, coordinationobjectivevalue: float | None) → None"
    Store the coordination objective (inconsistency) results.


    **Args:**
    > coordinationobjectivevalue: The coordination objective value.  

??? abstract "get_CoordinationObjectiveValue(self) → float | None"
    Get the coordination objective value.


    **Returns:**
    > The coordination objective value, or None if not yet computed.  

??? abstract "evaluate_Gradient_CoordinationObjective(self) → None"
    Return analytical estimates from the user on the coordination objective.

??? abstract "evaluate_Gradient_TotalObjective(self) → None"
    Depending on if self is a local or controller subsystem, adds get_Gradient_LocalObjective (only for LocalSubSystemBasis) to get_Gradient_CoordinationObjective.

??? abstract "evaluateTotalConstraint(self) → None"
    Evaluate the local constraints.

??? abstract "evaluateTotalObjectiveAndTotalConstraint(self) → None"
    Evaluate both total objective and total constraint in a single call.

    This method combines evaluateTotalObjective() and evaluateTotalConstraint()
    to avoid redundant analysis and mapping operations when both values
    are needed (e.g., during optimization blackbox evaluations).

??? abstract "set_TotalConstraintEqValue(self, ceq: List[float] | None) → None"
    Store the equality constraint value after computation.

    Note: This value is updated after each solver iteration and may not be final.


    **Args:**
    > ceq: The equality constraint values.  

??? abstract "get_TotalConstraintEqValue(self) → List[float] | None"
    Get the total equality constraint value.


    **Returns:**
    > The equality constraint values, or None if not yet computed.  

??? abstract "set_TotalConstraintIneqValue(self, cineq: List[float] | None) → None"
    Store the inequality constraint value after computation.

    Note: This value is updated after each solver iteration and may not be final.


    **Args:**
    > cineq: The inequality constraint values.  

??? abstract "get_TotalConstraintIneqValue(self) → List[float] | None"
    Get the total inequality constraint value.


    **Returns:**
    > The inequality constraint values, or None if not yet computed.  

??? abstract "evaluateCoordinationEqualityConstraint(self) → None"
    Evaluate constraint inconsistency.

??? abstract "evaluateCoordinationInequalityConstraint(self) → None"
    Evaluate the coordination inequality constraint.

??? abstract "set_CoordinationEqualityConstraintValue(self, coordinationequalityconstraintvalue: List[float] | None) → None"
    Store the coordination equality constraint (inconsistency) results.


    **Args:**
    > coordinationequalityconstraintvalue: The coordination equality constraint values.  

??? abstract "get_CoordinationEqualityConstraintValue(self) → List[float] | None"
    Get the constraint inconsistency results.


    **Returns:**
    > The coordination equality constraint values, or None if not yet computed.  

??? abstract "set_CoordinationInequalityConstraintValue(self, coordinationinequalityconstraintvalue: List[float] | None) → None"
    Store the coordination inequality constraint results.


    **Args:**
    > coordinationinequalityconstraintvalue: The coordination inequality constraint values.  

??? abstract "get_CoordinationInequalityConstraintValue(self) → List[float] | None"
    Get the coordination inequality constraint results.


    **Returns:**
    > The coordination inequality constraint values, or None if not yet computed.  

??? abstract "evaluate_Jacobian_CoordinationEqualityConstraints(self) → None"
    Evaluate the Jacobian of the coordination equality constraints if it exists.

??? abstract "evaluate_Jacobian_CoordinationInEqualityConstraints(self) → None"
    Evaluate the Jacobian of the coordination inequality constraints if it exists.

??? abstract "evaluate_Jacobian_TotalEqualityConstraints(self) → None"
    Evaluate the Jacobian of the total equality constraints if it exists.

??? abstract "evaluate_Jacobian_TotalInEqualityConstraints(self) → None"
    Evaluate the Jacobian of the total inequality constraints if it exists.

??? abstract "prepare_OptimizationProblem(self) → None"
    Prepare the optimization problem.

??? abstract "run_IterativeOptimization(self) → None"
    Execute the local optimization of the subsystem.

??? abstract "set_OptimData(self, optimdataIn: [OptimDataBasis](optimization/optimizerdata/OptimDataBasis.md#optimdatabasis)) → None"
    Store the data associated with the optimization after finishing.


    **Args:**
    > optimdataIn: The optimization data to store.  

??? abstract "get_OptimData(self) → [OptimDataBasis](optimization/optimizerdata/OptimDataBasis.md#optimdatabasis)"
    Get the results of the last optimization.


    **Returns:**
    > The optimization data, or None if not set.  

??? abstract "postprocess_Optimization(self) → None"
    Postprocess the optimization.

??? abstract "check_MultipliersNotSet(self) → bool"
    Return True if any existing constraint is missing its corresponding multiplier in optimdata.


    **Returns:**
    > True if at least one constraint has no corresponding multiplier set.  

??? abstract "get_Local_ConvergenceIndicator_Innerloop(self) → [Local_ConvergenceIndicator_Innerloop_Interface](../coordination/convergence/Local_ConvergenceIndicator_Innerloop_Interface.md#local_convergenceindicator_innerloop_interface)"
    Get the local convergence indicator for the inner loop.


    **Returns:**
    > The local inner loop convergence indicator.  

??? abstract "get_Local_ConvergenceIndicator_Outerloop(self) → [Local_ConvergenceIndicator_Outerloop_Interface](../coordination/convergence/Local_ConvergenceIndicator_Outerloop_Interface.md#local_convergenceindicator_outerloop_interface)"
    Get the local convergence indicator for the outer loop.


    **Returns:**
    > The local outer loop convergence indicator.  

??? abstract "evaluate_InnerLoopConvergenceIndicator(self) → None"
    Evaluate the inner loop convergence indicator.

??? abstract "get_ConvInnerLoop(self) → bool"
    Check if the subsystem is locally converged in the inner loop.


    **Returns:**
    > True if converged, False otherwise.  

??? abstract "evaluate_OuterLoopConvergenceIndicator(self) → None"
    Evaluate the outer loop convergence indicator.

??? abstract "get_ConvOuterLoop(self) → bool"
    Get the outer loop convergence indicator.


    **Returns:**
    > True if converged, False otherwise.  

??? abstract "get_CouplingParameters(self) → List[[CouplingParametersInterface](couplingparameters/CouplingParametersInterface.md#couplingparametersinterface)]"
    Get the coupling parameters.


    **Returns:**
    > List of coupling parameters for all neighbors.  

??? abstract "get_CouplingParameter_with_ID(self, id: str) → [CouplingParametersInterface](couplingparameters/CouplingParametersInterface.md#couplingparametersinterface)"
    Return the coupling parameter from self._couplingparameters with the provided ID.


    **Args:**
    > id: Identifier of the neighbor subsystem.  


    **Returns:**
    > The coupling parameter matching the provided ID.  

??? abstract "return_initialized_CouplingParameters(self) → List[[CouplingParametersInterface](couplingparameters/CouplingParametersInterface.md#couplingparametersinterface)]"
    Initialize pairwise coupling parameters (local subsystems <-> local subsystems / controller).

    Implemented in specific subsystem class of subsystems for each distributed optimization algorithm.


    **Returns:**
    > List of initialized coupling parameters.  

??? abstract "initializeCouplingParameters_before_CopyToMiddleLevel(self) → None"
    Initialize coupling parameters before copying communicated information from neighboring subsystem.

??? abstract "initializeCouplingParameters_after_CopyFromMiddleLevel(self) → None"
    Initialize coupling parameters after copying communicated information from neighboring subsystems.

??? abstract "initializeCouplingParameters_after_Second_CopyFromMiddleLevel(self) → None"
    Initialize coupling parameters after already two communication rounds between subsystems (local subsystem and controller).

??? abstract "prepare_updateCouplingParameters(self) → None"
    Prepare for updating coupling parameters.

??? abstract "updateCouplingParameters_innerLoop(self) → None"
    Execute the update of coupling parameters in the inner loop.

    This is called after the update of the local and controller subsystem.

??? abstract "updateCouplingParameters_outerLoop(self) → None"
    Execute the update of the coupling parameters in each outer loop iteration after the inner loop.

??? abstract "compute_KKT_system_matrix_and_bounds(self) → List[List[List[float]] | List[Tuple[float | None, float | None]]]"
    Return the matrix of the linear KKT system and bounds on dual multipliers.


    **Returns:**
    > A list containing the KKT system matrix and bounds on dual multipliers.  

??? abstract "compute_KKT_multipliers(self) → None"
    If a coordination method needs multipliers of local constraints (incl. bound constraints), but the used solver does not provide such, then a globally defined procedure is called to set them in the OptimDataBasis object.

    The KKT multipliers are computed with respect to the current state
    of the subsystem, i.e. based on the Jacobians/gradients and design
    variable values currently stored in self._optimdata; updates of these
    quantities have to be done separately.
    Therefore, before calling this method, one should typically call
    evaluateAllJacobians() and updateSubsystemfromOptimdata()
    to ensure that the subsystem state and the stored Jacobians/gradients
    are consistent and up to date.

??? abstract "compute_ApproximateKKT_multipliers(self, matrix_KKT_system: np.typing.ArrayLike, negative_gradient_totalobjective: List[float], bounds: List[Tuple[float | None, float | None]]) → List[float]"
    Compute approximate KKT multipliers when the solver does not provide them.

    If a coordination method needs multipliers
    of local constraints (incl. bound constraints),
    but the used solver does not provide such, then
    a globally defined procedure is called to set them
    in the OptimDataBasis object.

    This function should only be called if the solver
    does not obtain a solution for the exact KKT-system;
    then, as a mitigation for algorithms that need multipliers
    to work, we compute the 'multipliers' that minimize the
    violation of the KKT system w.r.t. the squared l2-error.


    **Args:**
    > matrix_KKT_system: The KKT system matrix.  
    > negative_gradient_totalobjective: Negative gradient of the total objective.  
    > bounds: List of (lower, upper) bound tuples for each dual variable.  


    **Returns:**
    > The computed approximate KKT multipliers as a list.  

??? abstract "decompose_KKT_multipliers(self, all_multipliers: List[float]) → None"
    Decompose KKT multipliers into their constituent parts.

    After having computed the KKT multipliers in
    compute_KKT_multipliers, the total variable needs
    to be decomposed depending on which kind of constraint
    they map to (e.g. coordination objective gradient,
    lower/upper bounds, local and coordination in- and
    -equality constraints).


    **Args:**
    > all_multipliers: The combined KKT multiplier vector to decompose.  

??? abstract "print_startup_summary(self) → None"
    Print subsystem info at startup.

??? abstract "print_end_of_innerloop_iteration(self) → None"
    Print subsystem results at the end of an inner loop iteration.

??? abstract "print_termination_summary(self) → None"
    Print subsystem results at the end of the optimization run.

??? abstract "update_state(self, other_subsystem: [SubSystemInterface](SubSystemInterface.md#subsysteminterface)) → None"
    Update the state of this SubSystemInterface with the state of another SubSystemInterface.

    This operation preserves the memory address of all mutable attributes while updating
    their values. This is necessary for multiprocessing: when subsystems are executed in
    parallel via multiprocessing.Pool (see Parallel.py), they are serialized/deserialized
    into separate processes. After execution, the original objects must be updated with
    the computed results without changing their memory addresses, as other parts of the
    system may hold references to these objects.


    **Args:**
    > other_subsystem: The subsystem to copy state from.  


    **Note:**
    > Concrete implementations in subclasses must update all class attributes  
    > in the same order as defined in their __init__() method.  

