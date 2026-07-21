---
title: LocalSubSystemBasis
---

← Back to [subsystem](index.md)

# LocalSubSystemBasis

**Source:** [Distributed_Design_Optimizer\subsystem\LocalSubSystemBasis.py](LocalSubSystemBasis_source.md)

Local subsystem basis module.

This module provides the abstract base class for local subsystems in
distributed optimization.

## Classes

### LocalSubSystemBasis

> **Inherits from:** [SubSystemBasis](SubSystemBasis.md#subsystembasis)

> A LocalSubSystemBasis object contains all necessary data for an individual subsystem.

> This includes methods to analyse its responses, to optimize the subsystem and to couple it
> to neighboring subsystems.

#### Methods

??? abstract "__init__(self, id: str, level: int, neighborid: List[str], analysis: [AnalysisInterface](optimization/AnalysisInterface.md#analysisinterface), localobjective: [LocalObjectiveInterface](optimization/designproblem/LocalObjectiveInterface.md#localobjectiveinterface), localconstraints: [LocalConstraintsInterface](optimization/designproblem/LocalConstraintsInterface.md#localconstraintsinterface), optimization: [OptimizationInterface](optimization/OptimizationInterface.md#optimizationinterface)) → None"
    Create a new instance of LocalSubSystemBasis with neighbors.


    **Args:**
    > id: Identifier for the subsystem.  
    > level: Level identifier for the subsystem.  
    > neighborid: Identifiers for the neighbors.  
    > analysis: Type of analysis class.  
    > localobjective: Type of local objective function class.  
    > localconstraints: Type of local constraint functions class.  
    > optimization: Type of optimization class.  

??? abstract "initialize_Initial_Optimdata_at_Beginning(self) → [LocalSubSystemOptimData](optimization/optimizerdata/LocalSubSystemOptimData.md#localsubsystemoptimdata)"
    Return a LocalSubSystemOptimData object based on the subsystem's current state.


    **Returns:**
    > A LocalSubSystemOptimData with all fields set to None.  

??? abstract "initialize_Optimdata(self) → [LocalSubSystemOptimData](optimization/optimizerdata/LocalSubSystemOptimData.md#localsubsystemoptimdata)"
    Return a LocalSubSystemOptimData object based on the subsystem's current state.


    **Returns:**
    > A LocalSubSystemOptimData initialized from the current subsystem state.  

??? abstract "get_Finite_Differences_Jacobian(self) → [FiniteDifferencesJacobian](tools/FiniteDifferencesJacobian.md#finitedifferencesjacobian)"
    Get the finite differences Jacobian approximation object.


    **Returns:**
    > The finite differences Jacobian approximation object.  

??? abstract "set_Scalers(self, scalers: List[[ScalerBasis](tools/ScalerBasis.md#scalerbasis)]) → None"
    Set the size of scaling for the design variables.


    **Args:**
    > scalers: List of scalers for the design variables.  

??? abstract "get_Scalers(self) → List[[ScalerBasis](tools/ScalerBasis.md#scalerbasis)]"
    Get the scalers for design variables and constraints.


    **Returns:**
    > List of scalers for variables and constraints.  

??? abstract "get_Inconsistencies(self) → List[[InConsistencySizeInterface](../middlelevel/InConsistencySizeInterface.md#inconsistencysizeinterface)]"
    Get the inconsistencies.


    **Returns:**
    > List of inconsistency objects for all neighbors.  

??? abstract "evaluate_MaxInconsistency(self) → None"
    Evaluate the maximum inconsistency across the subsystems and the ID of it.

??? abstract "get_maxInconsistencyValue(self) → float | None"
    Get the maximum inconsistency value across the subsystems.


    **Returns:**
    > The maximum inconsistency value across all neighbors, or None if not yet computed.  

??? abstract "get_MaxInconsistencyCoupledSubsystemID(self) → str | None"
    Get the coupled subsystem ID with the maximum inconsistency value.


    **Returns:**
    > The neighbor subsystem ID with the largest inconsistency, or None if not yet computed.  

??? abstract "return_initialized_Inconsistencies(self) → List[[InConsistencySizeInterface](../middlelevel/InConsistencySizeInterface.md#inconsistencysizeinterface)]"
    Return initialized inconsistencies.


    **Returns:**
    > List of initialized InConsistencySizeInterface objects.  

??? abstract "get_SubsystemLevel(self) → int"
    Get the level of the subsystem.


    **Returns:**
    > The level of the subsystem.  

??? abstract "append_Controller(self) → None"
    Update local subsystems by appending controller.


??? abstract "updateSubsystemfromOptimdata(self, optimdata: [OptimDataBasis](optimization/optimizerdata/OptimDataBasis.md#optimdatabasis)) → None"
    Update subsystem state from optimization data.

    Updates design variables, objective values, constraint values, and runs
    analysis based on the provided optimization data.


    **Args:**
    > optimdata: Optimization data containing updated values.  

??? abstract "updateOptimdatafromSubsystem(self) → None"
    Update the optimdata object with the information from the state of the subsystem.

    This should only be called if an optimdata object
    was created and should be modified afterwards
    (e.g. in initialization, where the optimdata object
    has None fields).

??? abstract "copy_LocalObjectiveUnscaled_Past_outerloop_itr(self, outerloop_itr_before: int) → float | None"
    Copy unscaled local objective from past outer loop iteration.


    **Args:**
    > outerloop_itr_before: The number of outer loop iterations to go back by.  


    **Returns:**
    > The unscaled local objective value from the past iteration, or None if not found.  

??? abstract "copy_LocalObjectiveUnscaled_Previous_outerloop_itr(self) → float | None"
    Copy the unscaled local objective from the previous outer loop iteration.


    **Returns:**
    > The unscaled local objective value from the previous iteration, or None if not found.  

??? abstract "copy_LocalObjective_Past_outerloop_itr(self, outerloop_itr_before: int) → float | None"
    Copy local objective from past outer loop iteration.


    **Args:**
    > outerloop_itr_before: The number of outer loop iterations to go back by.  


    **Returns:**
    > The scaled local objective value from the past iteration, or None if not found.  

??? abstract "copy_LocalObjective_Previous_outerloop_itr(self) → float | None"
    Copy the scaled local objective from the previous outer loop iteration.


    **Returns:**
    > The scaled local objective value from the previous iteration, or None if not found.  

??? abstract "copy_LocalObjective_Previous_innerloop_itr(self) → float | None"
    Copy the scaled local objective from the previous inner loop iteration.


    **Returns:**
    > The scaled local objective value from the previous inner iteration, or None if not found.  

??? abstract "copy_LocalObjectiveUnscaled_Previous_innerloop_itr(self) → float | None"
    Copy the unscaled local objective from the previous inner loop iteration.


    **Returns:**
    > The unscaled local objective value from the previous inner iteration, or None if not found.  

??? abstract "set_DesignVariables(self, designvariables: List[float]) → None"
    Set the scaled design variables.


    **Args:**
    > designvariables: Scaled design variable values in [0, 1].  

??? abstract "runAnalysis(self) → None"
    Execute the analysis code associated with this subsystem.

??? abstract "set_Responses_Unscaled(self, Responsesin: List[float]) → None"
    Store the physical responses (unscaled values).


    **Args:**
    > Responsesin: Physical response values (unscaled).  

??? abstract "get_Responses_Unscaled(self) → List[float]"
    Return the physical responses of a subsystem (unscaled values).


    **Returns:**
    > Physical response values (unscaled).  

??? abstract "mapToCouplingParameters(self) → None"
    Map the physical responses onto the neighboring domains.

??? abstract "evaluateTotalObjective(self) → None"
    Evaluate the total objective function (local + coordination).

??? abstract "evaluateLocalObjective(self) → None"
    Evaluate the local objective function.

??? abstract "evaluate_Responses_and_LocalObjective(self) → None"
    Run the analysis, update the coupling parameters, and compute the local objective.

??? abstract "set_LocalObjectiveValue(self, localobjectivevaluein: float | None) → None"
    Set the scaled local objective value.


    **Args:**
    > localobjectivevaluein: The scaled local objective value (in range [0.0, 1.0]).  

??? abstract "get_LocalObjectiveValue(self) → float | None"
    Get the scaled local objective value.


    **Returns:**
    > The scaled local objective value.  

??? abstract "get_LocalObjectiveValue_Unscaled(self) → float | None"
    Get the unscaled local objective value.


    **Returns:**
    > The unscaled local objective value.  

??? abstract "evaluateTotalConstraint(self) → None"
    Evaluate the total constraints (local + coordination).

??? abstract "evaluateTotalObjectiveAndTotalConstraint(self) → None"
    Evaluate both total objective and total constraint in a single call.

    This method combines evaluateTotalObjective() and evaluateTotalConstraint()
    to avoid redundant analysis and mapping operations when both values
    are needed (e.g., during optimization blackbox evaluations).

??? abstract "evaluateLocalConstraints(self) → None"
    Evaluate the local equality and inequality constraints.

??? abstract "set_EqualityLocalConstraintsValue(self, equalitylocalconstraintsin: List[float] | None) → None"
    Set the equality local constraints value (scaled01 value).


    **Args:**
    > equalitylocalconstraintsin: Equality constraint values (scaled to [-0.5, 0.5]).  

??? abstract "get_EqualityLocalConstraintsValue(self) → List[float] | None"
    Get the equality local constraints value (scaled01 value).


    **Returns:**
    > Equality constraint values (scaled to [-0.5, 0.5]).  

??? abstract "get_EqualityLocalConstraintsValue_Unscaled(self) → List[float] | None"
    Get the equality local constraints value (unscaled value).


    **Returns:**
    > Equality constraint values (unscaled).  

??? abstract "set_InequalityLocalConstraintsValue(self, inequalitylocalconstraintsvaluein: List[float] | None) → None"
    Set the inequality local constraints value (scaled01 value).


    **Args:**
    > inequalitylocalconstraintsvaluein: Inequality constraint values (scaled to [-0.5, 0.5]).  

??? abstract "get_InequalityLocalConstraintsValue(self) → List[float] | None"
    Get the inequality local constraints value (scaled01 value).


    **Returns:**
    > Inequality constraint values (scaled to [-0.5, 0.5]).  

??? abstract "get_InequalityLocalConstraintsValue_Unscaled(self) → List[float] | None"
    Get the inequality local constraints value (unscaled value).


    **Returns:**
    > Inequality constraint values (unscaled).  

??? abstract "evaluate_PerturbationDirectionsIndices_LocalObjectiveGradient(self, gradient_localobjective: List[float | None] | None, totalnumber_perturbationdirections: int) → List[int]"
    Return the perturbation direction indices for the local objective gradient.


    **Args:**
    > gradient_localobjective: The local objective gradient with None entries  
    > where approximation is needed.  
    > totalnumber_perturbationdirections: Total number of perturbation  
    > directions.  


    **Returns:**
    > List of indices where gradient approximation is needed.  

??? abstract "evaluate_PerturbationDirectionsIndices_CoordinationObjectiveGradient(self, gradient_coordinationobjective: List[float | None] | None, totalnumber_perturbationdirections: int) → List[int]"
    Return the perturbation direction indices for the coordination objective gradient.


    **Args:**
    > gradient_coordinationobjective: The coordination objective gradient with None entries  
    > where approximation is needed.  
    > totalnumber_perturbationdirections: Total number of perturbation  
    > directions.  


    **Returns:**
    > List of indices where gradient approximation is needed.  

??? abstract "evaluate_PerturbationDirectionsIndices_LocalEqualityConstraintsJacobian(self, jacobian_localequalityconstraints: List[List[float | None]] | None, totalnumber_perturbationdirections: int) → List[int]"
    Return the perturbation direction indices for the local equality constraints Jacobian.


    **Args:**
    > jacobian_localequalityconstraints: The local equality constraints Jacobian  
    > with None entries where approximation is needed.  
    > totalnumber_perturbationdirections: Total number of perturbation directions.  


    **Returns:**
    > List of indices where Jacobian approximation is needed.  

??? abstract "evaluate_PerturbationDirectionsIndices_CoordinationEqualityConstraintsJacobian(self, jacobian_coordinationequalityconstraints: List[List[float | None]] | None, totalnumber_perturbationdirections: int) → List[int]"
    Return the perturbation direction indices for the coordination equality constraints Jacobian.


    **Args:**
    > jacobian_coordinationequalityconstraints: The coordination equality constraints  
    > Jacobian with None entries where approximation is needed.  
    > totalnumber_perturbationdirections: Total number of perturbation directions.  


    **Returns:**
    > List of indices where Jacobian approximation is needed.  

??? abstract "evaluate_PerturbationDirectionsIndices_LocalInequalityConstraintsJacobian(self, jacobian_localinequalityconstraints: List[List[float | None]] | None, totalnumber_perturbationdirections: int) → List[int]"
    Return the perturbation direction indices for the active local inequality constraints Jacobian.


    **Args:**
    > jacobian_localinequalityconstraints: The local inequality constraints  
    > Jacobian with None entries where approximation is needed.  
    > totalnumber_perturbationdirections: Total number of perturbation  
    > directions.  


    **Returns:**
    > List of indices where Jacobian approximation is needed.  

??? abstract "evaluate_PerturbationDirectionsIndices_CoordinationInequalityConstraintsJacobian(self, jacobian_coordinationinequalityconstraints: List[List[float | None]] | None, totalnumber_perturbationdirections: int) → List[int]"
    Return the perturbation direction indices for the coordination inequality constraints Jacobian.


    **Args:**
    > jacobian_coordinationinequalityconstraints: The coordination inequality  
    > constraints Jacobian with None entries where approximation is needed.  
    > totalnumber_perturbationdirections: Total number of perturbation  
    > directions.  


    **Returns:**
    > List of indices where Jacobian approximation is needed.  

??? abstract "evaluate_PerturbationDirectionsIndices_MappedResponses(self, local_couplingparameters: List[[SubSysCouplingParametersBasis](couplingparameters/SubSysCouplingParametersBasis.md#subsyscouplingparametersbasis)], totalnumber_perturbationsdirections: int) → Dict[str, List[int]]"
    Return the dictionary of the mapping 'neighborID' to perturbation direction indices.

    Maps 'neighborID' -> indices of coordinate directions
    where the Jacobian of the mapped responses to the
    subsystem w.r.t. ID 'neighborID' needs
    to be approximated.


    **Args:**
    > local_couplingparameters: List of local coupling parameter objects.  
    > totalnumber_perturbationsdirections: Total number of perturbation directions.  


    **Returns:**
    > Dictionary mapping neighbor IDs to lists of perturbation direction indices.  

??? abstract "evaluate_PerturbationDirectionsIndices_MappedResponses_at_Neighbor(self, local_couplingparameter: [SubSysCouplingParametersBasis](couplingparameters/SubSysCouplingParametersBasis.md#subsyscouplingparametersbasis), totalnumber_perturbationsdirections: int) → List[int]"
    Return the indices of coordinate directions where the Jacobian of the mapped responses needs to be approximated.

    The Jacobian is for the mapped responses to the
    subsystem in the input 'local_couplingparameter'.
    Note that the Jacobian of mapped responses is stored in
    'local_couplingparameter' by Analysis_xxx.py.


    **Args:**
    > local_couplingparameter: The coupling parameter object for a specific neighbor.  
    > totalnumber_perturbationsdirections: Total number of perturbation directions.  


    **Returns:**
    > List of indices where Jacobian approximation is needed.  

??? abstract "evaluate_Gradient_LocalObjective(self) → None"
    Evaluate the gradient of the local objective and store it in self._optimdata.


??? abstract "evaluate_Gradient_TotalObjective(self) → None"
    Add get_Gradient_LocalObjective to get_Gradient_CoordinationObjective depending on subsystem type.

    The total objective gradient is stored in self._optimdata.

??? abstract "evaluate_Hessian_LocalObjective(self) → List[List[float | None]] | None"
    Evaluate the Hessian of the local objective.


    **Returns:**
    > The Hessian matrix of the local objective, or None if not provided.  

??? abstract "evaluate_Jacobian_LocalEqualityConstraints(self) → None"
    Evaluate the Jacobian of the local equality constraints and store it in self._optimdata.


??? abstract "evaluate_Jacobian_LocalInequalityConstraints(self) → None"
    Evaluate the Jacobian of the local inequality constraints and store it in self._optimdata.


??? abstract "evaluate_Hessian_EqualityLocalConstraints(self) → List[List[List[float | None]]] | None"
    Evaluate the Hessian of the local equality constraints.


    **Returns:**
    > The Hessian tensor of the local equality constraints, or None if not provided.  

??? abstract "evaluate_Hessian_InequalityLocalConstraints(self) → List[List[List[float | None]]] | None"
    Evaluate the Hessian of the local inequality constraints.


    **Returns:**
    > The Hessian tensor of the local inequality constraints, or None if not provided.  

??? abstract "evaluate_Jacobian_TotalEqualityConstraints(self) → None"
    Evaluate the Jacobian of the total equality constraints if it exists.

    Includes both local and coordination equality constraints.
    The Jacobian is stored in self._optimdata.

??? abstract "evaluate_Jacobian_TotalInEqualityConstraints(self) → None"
    Evaluate the Jacobian of the total inequality constraints if it exists.

    Includes both local and coordination inequality constraints.
    The Jacobian is stored in self._optimdata.

??? abstract "evaluate_Jacobian_MappedResponses(self) → None"
    Evaluate the Jacobians of the mapped responses and store them in the coupling parameters.

    This method calls the mapLocalResponsesDesignVariables_to_CouplingParameters_Jacobians function of self._analysis.
    The method in self._analysis directly calls set_MappedResponses_Jacobian of the
    local subsystem subclass which is abstractly defined, but this is defined in the
    userfiles for the specific design problems

??? abstract "evaluate_Hessians_MappedResponses(self) → List[List[List[List[float | None]]]] | None"
    Evaluate the Hessians of the mapped responses.

    This method calls the mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian function of self._analysis.


    **Returns:**
    > The Hessian tensor of the mapped responses, or None if not provided.  

??? abstract "evaluateAllJacobians(self) → None"
    Get the gradients, Jacobians, and Hessians needed for optimization.

    Calls evaluate_Gradient_xxx / evaluate_Jacobian_xxx /
    evaluate_Hessian_xxx of LocalSubSystemBasis.
    It fills in missing information (e.g. by using a jacobian approximator)
    and stores the results via setters into the LocalToControllerCouplingParamaters.

??? abstract "update_LocalObjective_Gradient(self, gradient_localobjective: List[float | None] | None, indices_gradient_localobjective: List[int]) → None"
    Update the missing entries of the gradient of the local objective using finite differences.


    **Args:**
    > gradient_localobjective: The local objective gradient with None entries  
    > where approximation is needed.  
    > indices_gradient_localobjective: Indices of coordinate directions to update.  

??? abstract "update_CoordinationObjective_Gradient(self, gradient_coordinationobjective: List[float | None] | None, indices_gradient_coordinationobjective: List[int]) → None"
    Update the missing entries of the gradient of the coordination objective using finite differences.


    **Args:**
    > gradient_coordinationobjective: The coordination objective gradient with None entries  
    > where approximation is needed.  
    > indices_gradient_coordinationobjective: Indices of coordinate directions to update.  

??? abstract "update_Jacobian_LocalEqualityConstraints(self, jacobian_localequalityconstraints: List[List[float | None]] | None, indices_jacobian_localequalityconstraints: List[int]) → None"
    Update the missing entries of the Jacobian of the local equality constraints using finite differences.


    **Args:**
    > jacobian_localequalityconstraints: The Jacobian with None entries  
    > where approximation is needed.  
    > indices_jacobian_localequalityconstraints: Indices of coordinate directions to update.  

??? abstract "update_Jacobian_CoordinationEqualityConstraints(self, jacobian_coordinationequalityconstraints: List[List[float | None]] | None, indices_jacobian_coordinationequalityconstraints: List[int]) → None"
    Update the missing entries of the Jacobian of the coordination equality constraints using finite differences.


    **Args:**
    > jacobian_coordinationequalityconstraints: The Jacobian with None entries  
    > where approximation is needed.  
    > indices_jacobian_coordinationequalityconstraints: Indices of coordinate directions to update.  

??? abstract "update_Jacobian_LocalInequalityConstraints(self, jacobian_localinequalityconstraints: List[List[float | None]] | None, indices_jacobian_localinequalityconstraints: List[int]) → None"
    Update the missing entries of the Jacobian of the local inequality constraints using finite differences.


    **Args:**
    > jacobian_localinequalityconstraints: The Jacobian with None entries  
    > where approximation is needed.  
    > indices_jacobian_localinequalityconstraints: Indices of coordinate directions to update.  

??? abstract "update_Jacobian_CoordinationInequalityConstraints(self, jacobian_coordinationinequalityconstraints: List[List[float | None]] | None, indices_jacobian_coordinationinequalityconstraints: List[int]) → None"
    Update the missing entries of the Jacobian of all coordination inequality constraints using finite differences.


    **Args:**
    > jacobian_coordinationinequalityconstraints: The Jacobian with None entries  
    > where approximation is needed.  
    > indices_jacobian_coordinationinequalityconstraints: Indices of coordinate directions to update.  

??? abstract "update_Jacobians_MappedResponses(self, local_couplingparameters: List[[SubSysCouplingParametersBasis](couplingparameters/SubSysCouplingParametersBasis.md#subsyscouplingparametersbasis)], dict_indices_jacobians_mappedresponses: Dict[str, List[int]]) → None"
    Update the missing entries of the Jacobians of the mapped responses using finite differences.


    **Args:**
    > local_couplingparameters: List of local coupling parameters to update.  
    > dict_indices_jacobians_mappedresponses: Dictionary mapping neighbor IDs to  
    > indices of coordinate directions to update.  

??? abstract "update_Jacobian_LowerBounds(self, totalnumber_perturbationdirections: int) → None"
    Compute and store the Jacobian of all lower bounds.

    The Jacobian of the lower bound constraints g_i(x) = -x_i + lb_i <= 0
    is a negative identity matrix: each row i has -1 on the diagonal and 0
    elsewhere. Computed for all bounds regardless of active set.


    **Args:**
    > totalnumber_perturbationdirections: Total number of perturbation directions.  

??? abstract "update_Jacobian_UpperBounds(self, totalnumber_perturbationdirections: int) → None"
    Compute and store the Jacobian of all upper bounds.

    The Jacobian of the upper bound constraints g_i(x) = x_i - ub_i <= 0
    is a positive identity matrix: each row i has +1 on the diagonal and 0
    elsewhere. Computed for all bounds regardless of active set.


    **Args:**
    > totalnumber_perturbationdirections: Total number of perturbation directions.  

??? abstract "get_MappedResponse_Jacobian(self, id: str) → List[List[float]]"
    Get from the LocalToLocalForController_CouplingParameters the mapped responses Jacobian.


    **Args:**
    > id: Identifier of the neighbor.  


    **Returns:**
    > The Jacobian matrix of the mapped responses for the given neighbor.  

??? abstract "set_MappedResponses_Jacobian(self, id: str, mappedresponses_jacobian_in: List[List[float | None]]) → None"
    Set the mapped responses Jacobian in the LocalToLocalForController_CouplingParameters.

    Only sets values if every entry is a float and the lengths are correct (which is not checked here,
    but typically in evaluateAllJacobians).


    **Args:**
    > id: Identifier of the neighbor subsystem.  
    > mappedresponses_jacobian_in: The Jacobian matrix to set.  

??? abstract "get_LocalObjective_Gradient(self) → List[float]"
    Return the local objective gradient from self._optimdata.


    **Returns:**
    > The gradient of the local objective function.  

??? abstract "set_LocalObjective_Gradient(self, localobjective_gradient_in: List[float]) → None"
    Set the local objective gradient in self._optimdata.


    **Args:**
    > localobjective_gradient_in: The local objective gradient to set.  

??? abstract "get_LocalEqualityConstraint_Jacobian(self) → List[List[float]]"
    Return the Jacobian of the local equality constraints from self._optimdata.


    **Returns:**
    > The Jacobian matrix of the local equality constraints.  

??? abstract "set_LocalEqualityConstraint_Jacobian(self, localequalityconstraints_gradient_in: List[List[float]]) → None"
    Set the Jacobian of the local equality constraints in self._optimdata.


    **Args:**
    > localequalityconstraints_gradient_in: The Jacobian to set.  

??? abstract "get_LocalActiveInequalityConstraint_Jacobian(self) → List[List[float]]"
    Return the Jacobian of the local inequality constraints from self._optimdata.


    **Returns:**
    > The Jacobian matrix of the local inequality constraints.  

??? abstract "set_LocalActiveInequalityConstraint_Jacobian(self, localactiveinequalityconstraints_gradient_in: List[List[float]]) → None"
    Set the Jacobian of the local inequality constraints in self._optimdata.


    **Args:**
    > localactiveinequalityconstraints_gradient_in: The Jacobian to set.  

??? abstract "set_ReferenceDesignVariables(self, refdesignvariables: List[float] | List[None]) → None"
    Set the reference design variables (scaled01 values).


    **Args:**
    > refdesignvariables: Reference design variable values.  
    > Can be a list of floats in [0.0, 1.0] or a list of None values.  

??? abstract "get_ReferenceDesignVariables(self) → List[float] | List[None] | None"
    Get the reference design variables.


    **Returns:**
    > The reference design variables (scaled), or None if not set.  

??? abstract "get_ReferenceDesignVariables_Unscaled(self) → List[float] | List[None] | None"
    Get the unscaled reference design variables.


    **Returns:**
    > The reference design variables (unscaled), or None if not set.  

??? abstract "set_ReferenceLocalObjectiveValue(self, referencelocalobjectivevalue: float | None) → None"
    Set the reference local objective value.


    **Args:**
    > referencelocalobjectivevalue: The reference local objective value to set.  

??? abstract "get_ReferenceLocalObjectiveValue(self) → float | None"
    Get the reference local objective value.


    **Returns:**
    > The reference local objective value, or None if not set.  

??? abstract "set_ReferenceLocalObjectiveValueUnscaled(self, referencelocalobjectivevalueunscaled: float | None) → None"
    Set the unscaled reference local objective value.


    **Args:**
    > referencelocalobjectivevalueunscaled: The unscaled reference local objective value to set.  

??? abstract "get_ReferenceLocalObjectiveValueUnscaled(self) → float | None"
    Get the unscaled reference local objective value.


    **Returns:**
    > The unscaled reference local objective value, or None if not set.  

??? abstract "set_MappedResponseVariables(self, id: str, mappedresponsesin: List[float], mappedresponsesin_unscaled: List[float]) → None"
    Store the mapped response variables for the neighboring subsystems.


    **Args:**
    > id: Identifier of the neighbor.  
    > mappedresponsesin: Mapped response values (scaled to [0, 1]).  
    > mappedresponsesin_unscaled: Mapped response values (unscaled).  

??? abstract "set_Copy_MappedResponseVariables(self, id: str, copymappedresponsesin: List[float]) → None"
    Copy the mapped variables from neighboring subsystems (scaled01 values).


    **Args:**
    > id: Identifier of the neighbor.  
    > copymappedresponsesin: Copy of mapped response values (scaled to [0, 1]).  

??? abstract "get_Copy_MappedResponseVariables(self, id: str) → List[float] | None"
    Get the copy of mapped variables from neighboring subsystems (scaled01 values).


    **Args:**
    > id: Identifier of the neighbor.  


    **Returns:**
    > Copy of mapped response values (scaled to [0, 1]).  

??? abstract "set_CouplingVariables(self, id: str, couplingvariablein: List[float], couplingvariablein_unscaled: List[float]) → None"
    Store the target coupling variables for each individual subsystem.


    **Args:**
    > id: Identifier of the neighboring subsystem.  
    > couplingvariablein: Target variable for the physical response of the neighboring subsystem (scaled to [0, 1]).  
    > couplingvariablein_unscaled: Target variable for the physical response of the neighboring subsystem (unscaled).  

??? abstract "set_Copy_CouplingVariables(self, id: str, copycouplingvariablesin: List[float]) → None"
    Store a copy of the coupling variables from neighboring subsystems (scaled01 values).


    **Args:**
    > id: Identifier of the subsystem from which the variables originate.  
    > copycouplingvariablesin: Copy of coupling variable values (scaled to [0, 1]).  

??? abstract "set_SharedDesignVariables(self, id: str, shareddesignvariablesin: List[float], shareddesignvariablesin_unscaled: List[float]) → None"
    Store the shared design variables for the neighboring subsystems (scaled01 values).


    **Args:**
    > id: Identifier of the neighbor.  
    > shareddesignvariablesin: Shared design variable values (scaled to [0, 1]).  
    > shareddesignvariablesin_unscaled: Shared design variable values (unscaled).  

??? abstract "set_Copy_SharedDesignVariables(self, id: str, copyshareddesignvariablesin: List[float]) → None"
    Store a copy of the shared design variables from neighboring subsystems (scaled01 values).


    **Args:**
    > id: Identifier of the subsystem from which the variables originate.  
    > copyshareddesignvariablesin: Copy of shared design variable values (scaled to [0, 1]).  

??? abstract "set_TargetSharedDesignVariables(self, id: str, targetdesignvariablesin: List[float], targetdesignvariablesin_unscaled: List[float]) → None"
    Store the target shared design variables for the neighboring subsystems (scaled01 values).


    **Args:**
    > id: Identifier of the neighbor.  
    > targetdesignvariablesin: Target design variable values (scaled to [0, 1]).  
    > targetdesignvariablesin_unscaled: Target design variable values (unscaled).  

??? abstract "set_Copy_TargetSharedDesignVariables(self, id: str, copytargetdesignvariablesin: List[float]) → None"
    Store a copy of the target design variables from neighboring subsystems (scaled01 values).


    **Args:**
    > id: Identifier of the subsystem from which the variables originate.  
    > copytargetdesignvariablesin: Copy of target design variable values (scaled to [0, 1]).  

??? abstract "set_Indices_CouplingVariables_in_DesignVariables(self, id: str, indices_couplingvariables_in_designvariables_in: List[int]) → None"
    Set the coupling variable indices within the design variables vector.


    **Args:**
    > id: Identifier of the neighbor subsystem.  
    > indices_couplingvariables_in_designvariables_in: The indices to set.  

??? abstract "set_Indices_SharedDesignVariables_in_DesignVariables(self, id: str, indices_shareddesignvariables_in_designvariables_in: List[int]) → None"
    Set the shared design variable indices within the design variables vector.


    **Args:**
    > id: Identifier of the neighbor subsystem.  
    > indices_shareddesignvariables_in_designvariables_in: The indices to set.  

??? abstract "set_Indices_TargetSharedDesignVariables_in_DesignVariables(self, id: str, indices_targetshareddesignvariables_in_designvariables_in: List[int]) → None"
    Set the target shared design variable indices within the design variables vector.


    **Args:**
    > id: Identifier of the neighbor subsystem.  
    > indices_targetshareddesignvariables_in_designvariables_in: The indices to set.  

??? abstract "run_updateCouplingParameters_outerLoop_job(self) → None"
    Update coupling parameters in the outer loop, including inconsistency evaluation.

??? abstract "run_prepare_updateCouplingParameters_job(self) → None"
    Prepare coupling parameters update after inner loop, including inconsistency evaluation.

??? abstract "evaluate_Inconsistencies(self) → None"
    Compute the difference between stored coupling and mapped variables compared to the latest available data.

    It returns a matrix containing fourvectors. The first row vector are the mapped-response side differences of
    the coupling circle. The second row vector returns differences of the coupling-variable side of the coupling circle.
    The third and fourth rows return the difference between the shared design variable vector.

    This method does not evaluate consensus inconsistencies;
    Current variant: This has to be specified in each LocalSubSystemBasis
    subclass, e.g. consensus ALC, after calling super().evaluate_Inconsistencies.

??? abstract "appendtohistory(self) → None"
    Append the current subsystem state to the history, including inconsistency data.

??? abstract "copy_Inconsistencies_at_Iteration(self, outerloop_itr: int, innerloop_itr: int) → List[[InConsistencySizeInterface](../middlelevel/InConsistencySizeInterface.md#inconsistencysizeinterface)]"
    Copy the inconsistencies of the specified iteration at number (outerloop_itr, innerloop_itr).


    **Args:**
    > outerloop_itr (int): outer loop iteration number  
    > innerloop_itr (int): inner loop iteration number  


    **Returns:**
    > The inconsistencies at the specified iteration, or initialized inconsistencies if not found.  

??? abstract "copy_Inconsistencies_Past_outerloop_itr(self, outerloop_itr_before: int) → List[[InConsistencySizeInterface](../middlelevel/InConsistencySizeInterface.md#inconsistencysizeinterface)]"
    Copy the inconsistencies from the self._outerloop_itr-th previous outer iteration.


    **Args:**
    > outerloop_itr_before: The number of outer loop iterations to go to the history  
    > self._outerloop_itr (int): The current outer loop iteration number  


    **Returns:**
    > The inconsistencies from the specified past iteration, or initialized inconsistencies if not found.  

??? abstract "copy_Inconsistencies_Previous_outerloop_itr(self) → List[[InConsistencySizeInterface](../middlelevel/InConsistencySizeInterface.md#inconsistencysizeinterface)]"
    Copy the inconsistencies from the previous outer loop iteration.


    **Returns:**
    > The inconsistencies from the previous outer loop iteration.  

??? abstract "copy_Inconsistencies_Previous_Previous_outerloop_itr(self) → List[[InConsistencySizeInterface](../middlelevel/InConsistencySizeInterface.md#inconsistencysizeinterface)]"
    Copy the inconsistencies from the previous previous outer loop iteration.


    **Returns:**
    > The inconsistencies from two outer loop iterations ago.  

??? abstract "get_Ignore_CouplingId_for_CoordinationObjective(self) → str | None"
    Get the coupling IDs to ignore for the coordination objective.


    **Returns:**
    > The coupling ID to ignore, or None if all couplings are considered.  

??? abstract "set_Ignore_CouplingId_for_CoordinationObjective(self, id: str | None) → None"
    Set the coupling ID to ignore for coordination objective calculation.


    **Args:**
    > id: Coupling ID to ignore, or None to consider all couplings.  

??? abstract "compute_KKT_system_matrix_and_bounds(self) → List[List[List[float]] | List[Tuple[float | None, float | None]]]"
    Return the total linear KKT system matrix.


    **Returns:**
    > A list containing the constraint matrix and bounds for the KKT system.  

??? abstract "decompose_KKT_multipliers(self, all_multipliers: List[float]) → None"
    Decompose the solution of the KKT system and store the parts into self._optimdata.

    Decomposes the multipliers stored in optimization_result into different
    parts (e.g. local inequality constraints) and stores them
    into self._optimdata.


    **Args:**
    > all_multipliers: Total accumulation of all multipliers (only for constraints, not for objective)  

??? abstract "compute_Jacobian_MappedResponse_Wrt_DesignVariables(self) → None"
    Compute the Jacobian of mapped responses with respect to design variables.

??? abstract "set_Jacobian_MappedResponse_Wrt_DesignVariables_Value(self, jacobinain: List[List[List[float]] | None]) → None"
    Set the Jacobian matrix of mapped response variables with respect to design variables.


    **Args:**
    > jacobinain: Jacobian matrix for each coupling.  

??? abstract "get_Jacobian_MappedResponse_Wrt_DesignVariables_Value(self) → List[List[List[float]] | None] | None"
    Return the Jacobian matrix of mapped response variables with respect to design variables.


    **Returns:**
    > Jacobian matrix for each coupling, or None if not computed.  

??? abstract "get_scaler_bound_violations(self) → List[Tuple[int, str]]"
    Collect scaler bound violations for this subsystem.


    **Returns:**
    > List of (scaler_index, warning_message) tuples.  

??? abstract "print_scaler_bound_violations(self) → None"
    Print any scaler bound violations for this subsystem.

??? abstract "print_scaler_bound_utilization_report(self) → None"
    Print a compact scaler bound utilization report for this subsystem.

??? abstract "print_startup_summary(self) → None"
    Print local subsystem info at startup.

??? abstract "print_end_of_innerloop_iteration(self) → None"
    Print local subsystem results at the end of an inner loop iteration.

??? abstract "print_termination_summary(self) → None"
    Print local subsystem results at the end of the optimization run.

??? abstract "update_state(self, other_subsystem: [LocalSubSystemBasis](LocalSubSystemBasis.md#localsubsystembasis)) → None"
    Update the state of this LocalSubSystemBasis instance with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.

    The update preserves memory addresses by modifying attribute contents in-place where
    possible, rather than reassigning references. This is essential for maintaining object
    identity across the multiprocessing boundary.


    **Args:**
    > other_subsystem: The source LocalSubSystemBasis containing updated values  
    > from parallel execution.  

