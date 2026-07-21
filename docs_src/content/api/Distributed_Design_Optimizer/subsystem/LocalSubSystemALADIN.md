---
title: LocalSubSystemALADIN
---

← Back to [subsystem](index.md)

# LocalSubSystemALADIN

**Source:** [Distributed_Design_Optimizer\subsystem\LocalSubSystemALADIN.py](LocalSubSystemALADIN_source.md)

ALADIN local subsystem module.

This module provides the local subsystem implementation for the
ALADIN coordination method.

## Classes

### LocalSubSystemALADIN

> **Inherits from:** [LocalSubSystemBasis](LocalSubSystemBasis.md#localsubsystembasis)

> Local subsystem for ALADIN coordination.

> Implements the local subsystem functionality for the ALADIN
> distributed optimization method.

#### Methods

??? abstract "__init__(self, id: str, level: int, neighborid: List[str], analysis: [AnalysisInterface](optimization/AnalysisInterface.md#analysisinterface), localobjective: [LocalObjectiveInterface](optimization/designproblem/LocalObjectiveInterface.md#localobjectiveinterface), localconstraints: [LocalConstraintsInterface](optimization/designproblem/LocalConstraintsInterface.md#localconstraintsinterface), optimization: [OptimizationInterface](optimization/OptimizationInterface.md#optimizationinterface), local_convergenceindicator_innerloop: [Local_ConvergenceIndicator_Innerloop_Interface](../coordination/convergence/Local_ConvergenceIndicator_Innerloop_Interface.md#local_convergenceindicator_innerloop_interface), local_convergenceindicator_outerloop: [Local_ConvergenceIndicator_Outerloop_Interface](../coordination/convergence/Local_ConvergenceIndicator_Outerloop_Interface.md#local_convergenceindicator_outerloop_interface), updatecouplingparametermethod_outerloop: [UpdateCouplingParameterMethodInterface](../coordination/updatecouplingparametermethod/UpdateCouplingParameterMethodInterface.md#updatecouplingparametermethodinterface)) → None"
    Create a new instance of LocalSubSystemALADIN.


    **Args:**
    > id: Identifier for the subsystem.  
    > level: Level identifier for the subsystem in the hierarchy.  
    > neighborid: List of identifiers for neighboring subsystems.  
    > analysis: Analysis interface for the subsystem.  
    > localobjective: Local objective function interface.  
    > localconstraints: Local constraints function interface.  
    > optimization: Optimization interface.  
    > local_convergenceindicator_innerloop: Local convergence indicator for inner loop.  
    > local_convergenceindicator_outerloop: Local convergence indicator for outer loop.  
    > updatecouplingparametermethod_outerloop: Strategy for updating coupling parameters in outer loop.  

??? abstract "validate_inputs(self) → None"
    Validate the components handed to this subsystem by the ALADIN coordination method.

    Validates that the outer-loop update coupling parameter method and the local
    inner/outer loop convergence indicators are compatible with ALADIN.


    **Raises:**
    > ValueError: If a provided component is not compatible with ALADIN.  

??? abstract "get_Nu(self) → float"
    Return the hyperparameter nu of the proximal term in the primal subproblem.


    **Returns:**
    > The hyperparameter nu value.  

??? abstract "set_Nu(self, nu_in: float) → None"
    Set the hyperparameter nu of the proximal term in the primal subproblem.


    **Args:**
    > nu_in: The hyperparameter nu value to set.  

??? abstract "get_Sigma_i(self) → List[List[float]]"
    Get the hyperparameter Sigma_i of the proximal term in the primal subproblem.


    **Returns:**
    > The proximal matrix Sigma_i (positive definite).  

??? abstract "set_Sigma_i(self, sigma_i_in: List[List[float]]) → None"
    Set the hyperparameter Sigma_i of the proximal term in the primal subproblem.


    **Args:**
    > sigma_i_in: The proximal matrix Sigma_i to set (positive definite).  

??? abstract "get_HessianApproximation_LocalObjective(self) → [HessianApproximationBFGS](tools/HessianApproximationBFGS.md#hessianapproximationbfgs) | None"
    Get the BFGS Hessian approximation of the local objective.


    **Returns:**
    > The BFGS approximation object, or None if not initialized.  

??? abstract "set_HessianApproximation_LocalObjective(self, hessianapproximation_localobjective_in: [HessianApproximationBFGS](tools/HessianApproximationBFGS.md#hessianapproximationbfgs)) → None"
    Set the BFGS Hessian approximation of the local objective.


    **Args:**
    > hessianapproximation_localobjective_in: The BFGS approximation object to set.  

??? abstract "get_HessianApproximation_LocalEqualityConstraints(self) → List[[HessianApproximationBFGS](tools/HessianApproximationBFGS.md#hessianapproximationbfgs)] | None"
    Get the list of BFGS Hessian approximations of the local equality constraints.


    **Returns:**
    > One BFGS object per equality constraint, or None if not initialized.  

??? abstract "set_HessianApproximation_LocalEqualityConstraints(self, hessianapproximation_localequalityconstraints_in: List[[HessianApproximationBFGS](tools/HessianApproximationBFGS.md#hessianapproximationbfgs)]) → None"
    Set the list of BFGS Hessian approximations of the local equality constraints.


    **Args:**
    > hessianapproximation_localequalityconstraints_in: One BFGS object per equality constraint.  

??? abstract "get_HessianApproximation_LocalInequalityConstraints(self) → List[[HessianApproximationBFGS](tools/HessianApproximationBFGS.md#hessianapproximationbfgs)] | None"
    Get the list of BFGS Hessian approximations of the local inequality constraints.


    **Returns:**
    > One BFGS object per inequality constraint, or None if not initialized.  

??? abstract "set_HessianApproximation_LocalInequalityConstraints(self, hessianapproximation_localinequalityconstraints_in: List[[HessianApproximationBFGS](tools/HessianApproximationBFGS.md#hessianapproximationbfgs)]) → None"
    Set the list of BFGS Hessian approximations of the local inequality constraints.


    **Args:**
    > hessianapproximation_localinequalityconstraints_in: One BFGS object per inequality constraint.  

??? abstract "get_HessianApproximation_MappedResponses(self) → List[List[[HessianApproximationBFGS](tools/HessianApproximationBFGS.md#hessianapproximationbfgs)] | None] | None"
    Get the list of BFGS Hessian approximations of the mapped responses.

    Each entry corresponds to one local-to-local coupling. Since a coupling
    may not include mapped responses, entries can be None.


    **Returns:**
    > Nested list of BFGS objects per coupling, or None.  

??? abstract "set_HessianApproximation_MappedResponses(self, hessianapproximations_mappedresponses_in: List[List[[HessianApproximationBFGS](tools/HessianApproximationBFGS.md#hessianapproximationbfgs)] | None]) → None"
    Set the list of BFGS Hessian approximations of the mapped responses.


    **Args:**
    > hessianapproximations_mappedresponses_in: Nested list of BFGS objects per coupling.  

??? abstract "append_Controller(self) → None"
    Update local subsystems by appending controller and adding necessary coupling parameters.


??? abstract "get_LocalToController_CouplingParameters(self) → [LocalToController_CouplingParametersALADIN](couplingparameters/aladin/LocalToController_CouplingParametersALADIN.md#localtocontroller_couplingparametersaladin)"
    Return the controller coupling parameters.


    **Returns:**
    > The controller coupling parameters object.  

??? abstract "synchronize_AllLocalGlobalCouplingParameters(self) → None"
    Synchronize all local-global coupling parameters to the controller.

    This method synchronizes every information that is needed by
    the controller and stored in the local couplings between i
    and j to the controller coupling parameters object's
    LocalToLocalForController_CouplingParameters objects.

??? abstract "synchronize_LocalGlobalCouplingParameter(self, localtolocal_couplingparameter: [LocalCouplingParametersALADIN](couplingparameters/aladin/LocalCouplingParametersALADIN.md#localcouplingparametersaladin), localtolocalforcontroller_couplingparameter: [LocalToLocalForController_CouplingParameters](couplingparameters/aladin/LocalToLocalForController_CouplingParameters.md#localtolocalforcontroller_couplingparameters)) → None"
    Synchronize a single local-global coupling parameter to the controller.

    This method synchronizes every information that is needed by
    the controller and stored in the local couplings between i
    and j to the controller coupling parameters object's
    LocalToLocalForController_CouplingParameters objects.


    **Args:**
    > localtolocal_couplingparameter: Local coupling parameters between subsystems i and j.  
    > localtolocalforcontroller_couplingparameter: Coupling parameters from local subsystem to controller.  

??? abstract "mapToController(self) → None"
    Synchronize necessary information with the controller.

    Only subsystem i's information like e.g. Jacobians,
    Hessians, local multipliers, ..., are computed and stored in
    couplingparameters in postprocess_Optimization.

??? abstract "evaluateCoordinationObjective(self) → None"
    Evaluate the coordination objective including inner product and proximal terms.


??? abstract "evaluate_Gradient_CoordinationObjective(self) → None"
    Evaluate the analytical gradient of the coordination objective.

    Assumes the mapped responses Jacobian was evaluated already.

??? abstract "evaluateCoordinationEqualityConstraint(self) → None"
    Evaluate the coordination equality constraint for ALADIN.


??? abstract "evaluateCoordinationInequalityConstraint(self) → None"
    Evaluate the coordination inequality constraint for ALADIN.


??? abstract "evaluate_Jacobian_CoordinationEqualityConstraints(self) → None"
    Evaluate the Jacobian of the coordination equality constraints.

    ALADIN does not have coordination equality constraints, hence no-op.

??? abstract "evaluate_Jacobian_CoordinationInEqualityConstraints(self) → None"
    Evaluate the Jacobian of the coordination inequality constraints.

    ALADIN does not have coordination inequality constraints, hence no-op.

??? abstract "prepare_OptimizationProblem(self) → None"
    Update d_hat.


??? abstract "postprocess_Optimization(self) → None"
    Perform ALADIN's postprocessing.


??? abstract "evaluate_Hessian_Lagrangian(self, local_hessians: Dict[str, List[List[float]] | List[List[List[float]] | None] | None]) → List[List[float]]"
    Compute the Hessian of the Lagrangian w.r.t. local and coordination constraints.

    Given the Hessians of each summand of the Lagrangian, this function computes
    the combined Hessian of the Lagrangian.


    **Args:**
    > local_hessians: Dictionary mapping constraint type names to their Hessian  
    > matrices. Keys include "Local Objective", "Local Equality Constraints",  
    > and "Local Inequality Constraints".  


    **Returns:**
    > The combined Hessian of the Lagrangian as a 2D list.  

??? abstract "check_MultipliersNotSet(self) → bool"
    Return True if any existing constraint is missing its corresponding multiplier in optimdata.


    **Returns:**
    > True if at least one constraint has no corresponding multiplier set.  

??? abstract "evaluateAllHessians(self) → Dict[str, List[List[float]] | List[List[List[float]] | List[List[List[List[float]]]] | None] | None]"
    Evaluate all Hessians of local objective, local equality constraints and local inequality constraints.

    If they exist and were provided by the user, those are used;
    else, BFGS approximations are used.


    **Returns:**
    > Dictionary with keys 'Local Objective', 'Local Equality Constraints',  
    > 'Local Inequality Constraints', and 'Mapped Responses'.  

??? abstract "evaluate_Complete_Hessian_LocalObjective(self) → List[List[float]]"
    Evaluate a complete Hessian of the local objective.

    - If the user-provided Hessian is complete, this will be used
    - Else, the BFGS-approximation of the Hessian of the local objective


    **Returns:**
    > Complete Hessian matrix of the local objective.  

??? abstract "evaluate_Complete_Hessian_LocalEqualityConstraints(self) → List[List[List[float]]]"
    Evaluate complete Hessians of all local equality constraints.

    - If the user-provided Hessian for a constraint is complete, this will be used
    - Else, the BFGS-approximation of the Hessian of that equality constraint


    **Returns:**
    > List of complete Hessian matrices, one per equality constraint.  

??? abstract "evaluate_Hessian_LocalInequalityConstraints(self) → List[List[List[float]] | None]"
    Evaluate the Hessians of all local inequality constraints.

    - If the user-provided Hessian for a constraint is complete, this will be used
    - Else, the BFGS-approximation of the Hessian of that inequality constraint


    **Returns:**
    > List of complete Hessian matrices, one per inequality constraint.  

??? abstract "evaluate_Complete_Hessian_MappedResponses(self) → List[List[List[List[float]]] | None]"
    Compute the Hessians of the mapped responses for each local-to-local coupling.


    **Returns:**
    > Hessian matrices per coupling, None if no mapped responses.  

??? abstract "return_initialized_CouplingParameters(self) → List[[LocalToController_CouplingParametersALADIN](couplingparameters/aladin/LocalToController_CouplingParametersALADIN.md#localtocontroller_couplingparametersaladin) | [LocalCouplingParametersALADIN](couplingparameters/aladin/LocalCouplingParametersALADIN.md#localcouplingparametersaladin)]"
    Return a fresh set of initialized coupling parameters for this subsystem.


    **Returns:**
    > Fresh coupling parameters, one per neighbor.  

??? abstract "initializeCouplingParameters_before_CopyToMiddleLevel(self) → None"
    Initialize coupling parameters before copying communicated information from neighboring subsystem.

    Create empty placeholders for coupling parameters, i.e. communicated quantities in the algorithms,
    Lagrange multipliers, penalty weights, ...
    The sizes are read by already initialized quantities from the inner loop iteration

??? abstract "initializeCouplingParameters_after_CopyFromMiddleLevel(self) → None"
    Initialize coupling parameters after copying communicated information from neighboring subsystems.

    Create empty placeholders for coupling parameters, i.e. communicated quantities in the algorithms,
    Lagrange multipliers, penalty weights, ...
    The sizes are read by already initialized quantities from the inner loop iteration

??? abstract "initializeCouplingParameters_after_Second_CopyFromMiddleLevel(self) → None"
    Initialize the rest of the coupling parameters by solving the controller QP in ALADIN.


??? abstract "prepare_updateCouplingParameters(self) → None"
    Synchronize all coupling parameters to controller.


??? abstract "updateCouplingParameters_innerLoop(self) → None"
    Update coupling parameters in the inner loop.

    In ALADIN, empty, but synchronize.

??? abstract "updateCouplingParameters_outerLoop(self) → None"
    Update coupling parameters during outer loop iteration.


??? abstract "updateSubsystem(self, perturbed_designvariables: List[float]) → None"
    Update the subsystem based on the inputted design variables.


    **Args:**
    > perturbed_designvariables: Design variables to evaluate the subsystem at.  

??? abstract "evaluate_Inconsistencies(self) → None"
    Compute the difference between stored coupling and mapped variables.

    Compared to the latest available data from a subsystem.
    It returns a matrix containing three vectors. The first row vector are the mapped-response side differences of
    the coupling circle. The second row vector returns differences of the coupling-variable side of the coupling circle.
    The third row returns the difference between the shared design variable vector.

??? abstract "return_initialized_Inconsistencies(self) → List[[InConsistencySize](../middlelevel/sbdp/InConsistencySize.md#inconsistencysize)]"
    Return a fresh set of initialized inconsistency objects.


    **Returns:**
    > One inconsistency object per coupling parameter.  

??? abstract "set_CoordinationMultipliers_MappedResponse_Minus_CopyCouplingVariable(self, neighborid: str, multipliersin: List[float]) → None"
    Set coordination multipliers for the mapped response minus copied coupling variable inconsistency of a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > multipliersin: List of multiplier values to set.  

??? abstract "set_CoordinationMultipliers_CopyMappedResponse_Minus_CouplingVariable(self, neighborid: str, multipliersin: List[float]) → None"
    Set coordination multipliers for the copied mapped response minus coupling variable inconsistency of a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > multipliersin: List of multiplier values to set.  

??? abstract "set_CoordinationMultipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, neighborid: str, multipliersin: List[float]) → None"
    Set coordination multipliers for the shared design variable minus copied target shared design variable inconsistency of a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > multipliersin: List of multiplier values to set.  

??? abstract "set_CoordinationMultipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self, neighborid: str, multipliersin: List[float]) → None"
    Set coordination multipliers for the copied shared design variable minus target shared design variable inconsistency of a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > multipliersin: List of multiplier values to set.  

??? abstract "set_CoordinationWeights_MappedResponse_Minus_CopyCouplingVariable(self, neighborid: str, penaltyweightsin: List[float]) → None"
    Set coordination weights for the mapped response minus copied coupling variable inconsistency of a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > penaltyweightsin: List of penalty weight values to set.  

??? abstract "set_CoordinationWeights_CopyMappedResponse_Minus_CouplingVariable(self, neighborid: str, penaltyweightsin: List[float]) → None"
    Set coordination weights for the copied mapped response minus coupling variable inconsistency of a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > penaltyweightsin: List of penalty weight values to set.  

??? abstract "set_CoordinationWeights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, neighborid: str, penaltyweightsin: List[float]) → None"
    Set coordination weights for the shared design variable minus copied target shared design variable inconsistency of a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > penaltyweightsin: List of penalty weight values to set.  

??? abstract "set_CoordinationWeights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self, neighborid: str, penaltyweightsin: List[float]) → None"
    Set coordination weights for the copied shared design variable minus target shared design variable inconsistency of a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > penaltyweightsin: List of penalty weight values to set.  

??? abstract "update_state(self, other_subsystem: [LocalSubSystemALADIN](LocalSubSystemALADIN.md#localsubsystemaladin)) → None"
    Update the state of this LocalSubSystemALADIN instance with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.

    The update preserves memory addresses by modifying attribute contents in-place where
    possible, rather than reassigning references. This is essential for maintaining object
    identity across the multiprocessing boundary.


    **Args:**
    > other_subsystem: The source LocalSubSystemALADIN containing updated values  
    > from parallel execution.  

