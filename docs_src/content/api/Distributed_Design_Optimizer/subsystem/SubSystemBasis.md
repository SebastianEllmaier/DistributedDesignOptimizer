---
title: SubSystemBasis
---

← Back to [subsystem](index.md)

# SubSystemBasis

**Source:** [Distributed_Design_Optimizer\subsystem\SubSystemBasis.py](SubSystemBasis_source.md)

Subsystem basis module.

This module provides the base class for all subsystems in the
distributed design optimization framework.

## Classes

### SubSystemBasis

> **Inherits from:** [SubSystemInterface](SubSystemInterface.md#subsysteminterface)

> A SubSystemBasis object contains a general structure of methods to optimize the subsystem and to couple it to neighboring subsystems.

#### Methods

??? abstract "__init__(self, id: str, neighborid: List[str]) → None"
    Create a new instance of SubSystemBasis with neighbors/controller.


    **Args:**
    > id: Identifier for the subsystem.  
    > neighborid: Identifiers for the neighbors.  

??? abstract "get_SUBSYSTEMID(self) → str"
    Get the identifier of the subsystem.


    **Returns:**
    > The subsystem identifier.  

??? abstract "get_NeighborId(self) → List[str]"
    Get the neighbor IDs.


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

    For each MiddleLevelDataStorage, determines which neighbor it
    connects to, finds the matching local CouplingParameter, and
    writes it to shared storage (lock-safe via set_Coupling).

??? abstract "CopyFromMiddleLevel(self) → None"
    Copy coupling data from the shared middle-level data storage.

    For each MiddleLevelDataStorage, determines which neighbor it
    connects to, retrieves the stored coupling data, and applies it
    to the matching local CouplingParameter.

    NOTE ON ASYMMETRY WITH CopyToMiddleLevel:
    CopyToMiddleLevel passes the CouplingParameter directly to
    ml.set_Coupling(cp), which internally calls
    cp.CopyToMiddleLevelCoupling(slot) — the data flows from the
    caller's object INTO shared storage via argument.

    CopyFromMiddleLevel cannot mirror this pattern because of
    multiprocessing proxies: arguments sent through a BaseProxy
    are pickled to the manager process. Mutations of the argument
    inside the manager are applied to a deserialized copy and
    discarded — the caller's original is never modified. Only
    return values travel back across process boundaries.

    Therefore we use get_StoredCoupling(neighbor_id) which RETURNS
    the data, then apply it locally via
    cp.CopyFromMiddleLevelCoupling(storedcoupling).

??? abstract "run_innerloop_job(self) → None"
    Execute the inner loop job: copy from middle level, optimize, copy back.

??? abstract "run_updateCouplingParameters_innerLoop_job(self) → None"
    Update coupling parameters in the inner loop after optimization.

??? abstract "savesubsystemhistory(self) → None"
    Save the subsystem history to a dill file.

    The use-case name is read from the subsystem's own state (set via
    set_Name by the Coordinator). The target folder is the use-case's
    historyfiles folder (stored as self._historyfolderpath via
    set_HistoryFolderPath by the Coordinator).

??? abstract "set_LowerBounds_Unscaled(self, lowerbounds: List[float]) → None"
    Set the lower bounds for the design variables (unscaled values).


    **Args:**
    > lowerbounds: Lower bound values (unscaled).  

??? abstract "get_LowerBounds_Unscaled(self) → List[float] | None"
    Get the lower bounds of the design variables.


    **Returns:**
    > Lower bound values (unscaled).  

??? abstract "set_UpperBounds_Unscaled(self, upperbounds: List[float]) → None"
    Set the upper bounds of the design variables (unscaled values).


    **Args:**
    > upperbounds: Upper bound values (unscaled).  

??? abstract "get_UpperBounds_Unscaled(self) → List[float] | None"
    Get the upper bounds of the design variables.


    **Returns:**
    > Upper bound values (unscaled).  

??? abstract "updateSubsystemfromOptimdata(self, optimdata: [OptimDataBasis](optimization/optimizerdata/OptimDataBasis.md#optimdatabasis)) → None"
    Update subsystem state from optimization data.

    Updates the subsystem's design variables, objective values, and
    constraint values from the provided optimization data.


    **Args:**
    > optimdata: Optimization data containing updated values.  

??? abstract "updateOptimdatafromSubsystem(self) → None"
    Update self._optimdata from the current subsystem information.


    **Raises:**
    > ValueError: If design variables are incompatible with optimdata.  
    > ValueError: If design variables (unscaled) are incompatible with optimdata.  
    > ValueError: If total objective value is incompatible with optimdata.  
    > ValueError: If total equality constraint values are incompatible with optimdata.  
    > ValueError: If total inequality constraint values are incompatible with optimdata.  
    > ValueError: If coordination objective value is incompatible with optimdata.  
    > ValueError: If coordination equality constraint values are incompatible with optimdata.  
    > ValueError: If lower bounds are incompatible with optimdata.  
    > ValueError: If upper bounds are incompatible with optimdata.  

??? abstract "get_DesignVariables(self) → List[float] | None"
    Get the scaled design variables.


    **Returns:**
    > Scaled design variable values in [0, 1].  

??? abstract "get_DesignVariables_Unscaled(self) → List[float] | None"
    Get the unscaled design variables.


    **Returns:**
    > Unscaled design variable values.  

??? abstract "set_DesignVariables_Granularity(self, designvariables_granularity: List[float]) → None"
    Set the granularity of the design variables.


    **Args:**
    > designvariables_granularity: Granularity values where 0.0 means continuous.  

??? abstract "get_DesignVariables_Granularity(self) → List[float] | None"
    Get the granularity of the design variables.


    **Returns:**
    > Granularity values where 0.0 means continuous.  

??? abstract "set_TotalObjectiveValue(self, totalobjectivevalue: float | None) → None"
    Store the total objective value after the computation of the TotalObjective Class.


    **Args:**
    > totalobjectivevalue: The total objective value to store.  

??? abstract "get_TotalObjectiveValue(self) → float | None"
    Return the total objective value after the computation of the TotalObjective Class.


    **Returns:**
    > The total objective value, or None if not yet computed.  

??? abstract "set_CoordinationObjectiveValue(self, coordinationobjectivevalue: float | None) → None"
    Store the objective inconsistency results.


    **Args:**
    > coordinationobjectivevalue: The coordination objective value to store.  

??? abstract "get_CoordinationObjectiveValue(self) → float | None"
    Get the objective inconsistency function value.


    **Returns:**
    > The coordination objective value, or None if not yet computed.  

??? abstract "set_TotalConstraintEqValue(self, ceq: List[float] | None) → None"
    Store the equality constraint value after the computation of the TotalConstraint Class.


    **Args:**
    > ceq: The equality constraint values to store.  

??? abstract "get_TotalConstraintEqValue(self) → List[float] | None"
    Return the equality constraint value after the computation of the TotalConstraint Class.


    **Returns:**
    > The equality constraint values, or None if not yet computed.  

??? abstract "set_TotalConstraintIneqValue(self, cineq: List[float] | None) → None"
    Store the inequality constraint value after the computation of the TotalConstraint Class.


    **Args:**
    > cineq: The inequality constraint values to store.  

??? abstract "get_TotalConstraintIneqValue(self) → List[float] | None"
    Return the inequality constraint value after the computation of the TotalConstraint Class.


    **Returns:**
    > The inequality constraint values, or None if not yet computed.  

??? abstract "set_CoordinationEqualityConstraintValue(self, coordinationequalityconstraintvalue: List[float] | None) → None"
    Store the constraint inconsistency results.


    **Args:**
    > coordinationequalityconstraintvalue: The coordination equality constraint values.  

??? abstract "get_CoordinationEqualityConstraintValue(self) → List[float] | None"
    Get the constraint inconsistency function value.


    **Returns:**
    > The coordination equality constraint values, or None if not yet computed.  

??? abstract "set_CoordinationInequalityConstraintValue(self, coordinationinequalityconstraintvalue: List[float] | None) → None"
    Store the coordination inequality constraint results.


    **Args:**
    > coordinationinequalityconstraintvalue: The coordination inequality constraint values.  

??? abstract "get_CoordinationInequalityConstraintValue(self) → List[float] | None"
    Get the coordination inequality constraint function value.


    **Returns:**
    > The coordination inequality constraint values, or None if not yet computed.  

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
    > Unscaled design variables from the previous iteration, or None if not found.  

??? abstract "copy_DesignVariables_Previous_outerloop_itr(self) → List[float] | None"
    Copy the scaled design variables from the previous outer loop iteration.


    **Returns:**
    > Scaled design variables from the previous iteration, or None if not found.  

??? abstract "copy_DesignVariables_Previous_innerloop_itr(self) → List[float] | None"
    Copy the scaled design variables from the previous inner loop iteration.


    **Returns:**
    > Scaled design variables from the previous inner iteration, or None if not found.  

??? abstract "copy_DesignVariablesUnscaled_Previous_innerloop_itr(self) → List[float] | None"
    Copy the unscaled design variables from the previous inner loop iteration.


    **Returns:**
    > Unscaled design variables from the previous inner iteration, or None if not found.  

??? abstract "run_IterativeOptimization(self) → None"
    Execute the local optimization of the subsystem.

??? abstract "set_OptimData(self, optimdataIn: [OptimDataBasis](optimization/optimizerdata/OptimDataBasis.md#optimdatabasis)) → None"
    Store the information from the optimization run.


    **Args:**
    > optimdataIn: The optimization data to store.  

??? abstract "get_OptimData(self) → [OptimDataBasis](optimization/optimizerdata/OptimDataBasis.md#optimdatabasis)"
    Get information from the last optimization run.


    **Returns:**
    > The optimization data, or None if not set.  

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

    The local convergence indicator retrieves the data it needs from self.
    This allows different convergence criteria to access different data
    (e.g., total objective, primal/dual residuals, etc.).

??? abstract "get_ConvInnerLoop(self) → bool"
    Check if the subsystem is locally converged in the inner loop.


    **Returns:**
    > True if converged, False otherwise.  

??? abstract "evaluate_OuterLoopConvergenceIndicator(self) → None"
    Evaluate the outer loop convergence indicator.

    Same design rationale as evaluate_InnerLoopConvergenceIndicator:
    the local convergence indicator retrieves the data it needs from self.

??? abstract "get_ConvOuterLoop(self) → bool"
    Get the outer loop convergence indicator.


    **Returns:**
    > True if converged, False otherwise.  

??? abstract "CopyFromMiddleLevelCoupling(self, idIn: str, couplingIn: [MiddleLevelCouplingInterface](../middlelevel/MiddleLevelCouplingInterface.md#middlelevelcouplinginterface)) → None"
    Apply stored middle-level coupling data to the matching local CouplingParameter.


    **Args:**
    > idIn: Identifier of the neighbor subsystem.  
    > couplingIn: The MiddleLevelCouplingInterface data retrieved from storage.  

??? abstract "get_CouplingParameters(self) → List[[CouplingParametersInterface](couplingparameters/CouplingParametersInterface.md#couplingparametersinterface)]"
    Get the coupling parameters.


    **Returns:**
    > List of coupling parameters for all neighbors.  

??? abstract "get_CouplingParameter_with_ID(self, id: str) → [CouplingParametersInterface](couplingparameters/CouplingParametersInterface.md#couplingparametersinterface)"
    Return the coupling parameter from self._couplingparameters with the provided ID.


    **Args:**
    > id: Identifier of the neighbor subsystem.  


    **Raises:**
    > ValueError: If no coupling parameter with the given ID exists.  


    **Returns:**
    > The coupling parameter matching the provided ID.  

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

??? abstract "check_MultipliersNotSet(self) → bool"
    Return True if any existing constraint is missing its corresponding multiplier in optimdata.


    **Returns:**
    > True if at least one constraint has no corresponding multiplier set.  

??? abstract "update_state(self, other_subsystem: [SubSystemBasis](SubSystemBasis.md#subsystembasis)) → None"
    Update the state of this SubSystemBasis instance with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.

    The update preserves memory addresses by modifying attribute contents in-place where
    possible, rather than reassigning references. This is essential for maintaining object
    identity across the multiprocessing boundary.


    **Args:**
    > other_subsystem: The source SubSystemBasis containing updated values  
    > from parallel execution.  

