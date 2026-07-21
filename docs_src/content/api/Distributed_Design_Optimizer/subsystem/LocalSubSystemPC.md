---
title: LocalSubSystemPC
---

← Back to [subsystem](index.md)

# LocalSubSystemPC

**Source:** [Distributed_Design_Optimizer\subsystem\LocalSubSystemPC.py](LocalSubSystemPC_source.md)

Penalty Coordination local subsystem module.

This module provides the local subsystem implementation for the
Penalty Coordination method.

## Classes

### LocalSubSystemPC

> **Inherits from:** [LocalSubSystemBasis](LocalSubSystemBasis.md#localsubsystembasis)

> Local subsystem implementation using Penalty Coordination.

> Implements the Penalty Coordination (PC) method for distributed
> optimization. Manages coupling parameters, coordination weights,
> and convergence tracking for iterative decomposition-based optimization.

#### Methods

??? abstract "__init__(self, id: str, level: int, neighborid: List[str], analysis: [AnalysisInterface](optimization/AnalysisInterface.md#analysisinterface), localobjective: [LocalObjectiveInterface](optimization/designproblem/LocalObjectiveInterface.md#localobjectiveinterface), localconstraints: [LocalConstraintsInterface](optimization/designproblem/LocalConstraintsInterface.md#localconstraintsinterface), optimization: [OptimizationInterface](optimization/OptimizationInterface.md#optimizationinterface), local_convergenceindicator_innerloop: [Local_ConvergenceIndicator_Innerloop_Interface](../coordination/convergence/Local_ConvergenceIndicator_Innerloop_Interface.md#local_convergenceindicator_innerloop_interface), local_convergenceindicator_outerloop: [Local_ConvergenceIndicator_Outerloop_Interface](../coordination/convergence/Local_ConvergenceIndicator_Outerloop_Interface.md#local_convergenceindicator_outerloop_interface), updatecouplingparametermethod_outerloop: [UpdateCouplingParameterMethodInterface](../coordination/updatecouplingparametermethod/UpdateCouplingParameterMethodInterface.md#updatecouplingparametermethodinterface)) → None"
    Create a new LocalSubSystemPC instance.


    **Args:**
    > id: Identifier for the subsystem.  
    > level: Level identifier for the subsystem in the hierarchy.  
    > neighborid: List of identifiers for neighboring subsystems.  
    > analysis: Analysis interface for subsystem evaluation.  
    > localobjective: Local objective function class.  
    > localconstraints: Local constraint functions class.  
    > optimization: Optimization interface for solving local problems.  
    > local_convergenceindicator_innerloop: Local convergence indicator for inner loop.  
    > local_convergenceindicator_outerloop: Local convergence indicator for outer loop.  
    > updatecouplingparametermethod_outerloop: Method for updating coupling parameters in outer loop.  

??? abstract "validate_inputs(self) → None"
    Validate the components handed to this subsystem by the PC coordination method.

    Validates that the outer-loop update coupling parameter method and the local
    inner/outer loop convergence indicators are compatible with PC.


    **Raises:**
    > ValueError: If a provided component is not compatible with PC.  

??? abstract "append_Controller(self) → None"
    Update local subsystems by appending controller.


??? abstract "mapToController(self) → None"
    Pass, since no controller in PC.


??? abstract "evaluateCoordinationObjective(self) → None"
    Evaluate the coordination objective.


??? abstract "evaluate_Gradient_CoordinationObjective(self) → None"
    Evaluate the analytical gradient of the coordination objective.

    Assumes the mapped responses Jacobian was evaluated already.

??? abstract "evaluateCoordinationEqualityConstraint(self) → None"
    Evaluate the coordination equality constraint.


??? abstract "evaluateCoordinationInequalityConstraint(self) → None"
    Evaluate the coordination inequality constraint.


??? abstract "evaluate_Jacobian_CoordinationEqualityConstraints(self) → None"
    Evaluate the Jacobian of the coordination equality constraints.

    PC does not have coordination equality constraints, hence no-op.

??? abstract "evaluate_Jacobian_CoordinationInEqualityConstraints(self) → None"
    Evaluate the Jacobian of the coordination inequality constraints.

    PC does not have coordination inequality constraints, hence no-op.

??? abstract "prepare_OptimizationProblem(self) → None"
    Prepare the optimization problem.


??? abstract "postprocess_Optimization(self) → None"
    Postprocess the optimization.


??? abstract "return_initialized_CouplingParameters(self) → List[[CouplingParametersPC](couplingparameters/pc/CouplingParametersPC.md#couplingparameterspc)]"
    Return initialized coupling parameters.


    **Returns:**
    > List of initialized CouplingParametersPC, one per neighbor.  

??? abstract "initializeCouplingParameters_before_CopyToMiddleLevel(self) → None"
    Initialize coupling parameters before copying from neighboring subsystem.

    Create empty placeholders for coupling parameters, i.e. communicated quantities in the algorithms,
    penalty weights, ...
    The sizes are read by already initialized quantities from the inner loop iteration.

??? abstract "initializeCouplingParameters_after_CopyFromMiddleLevel(self) → None"
    Initialize coupling parameters after copying from neighboring subsystems.

    Create empty placeholders for coupling parameters, i.e. communicated quantities in the algorithms,
    penalty weights, ...
    The sizes are read by already initialized quantities from the inner loop iteration.

??? abstract "initializeCouplingParameters_after_Second_CopyFromMiddleLevel(self) → None"
    Initialize coupling parameters after two communication rounds between subsystems.


??? abstract "prepare_updateCouplingParameters(self) → None"
    Prepare coupling parameters before update operations.


??? abstract "updateCouplingParameters_innerLoop(self) → None"
    Update coupling parameters in the inner loop.


??? abstract "updateCouplingParameters_outerLoop(self) → None"
    Update coupling parameters during outer loop iteration.


??? abstract "evaluate_Inconsistencies(self) → None"
    Compute the difference between stored coupling and mapped variables.

    Compares to the latest available data from a subsystem.
    Delegates to the base class implementation which computes inconsistency vectors for the mapped-response side,
    coupling-variable side, shared design variables, and target shared design variables of each coupling circle.

??? abstract "return_initialized_Inconsistencies(self) → List[[InConsistencySize](../middlelevel/sbdp/InConsistencySize.md#inconsistencysize)]"
    Return initialized inconsistencies.


    **Returns:**
    > List of initialized InConsistencySize, one per coupling parameter.  

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

??? abstract "update_state(self, other_subsystem: [LocalSubSystemPC](LocalSubSystemPC.md#localsubsystempc)) → None"
    Update the state of this LocalSubSystemPC instance with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.

    The update preserves memory addresses by modifying attribute contents in-place where
    possible, rather than reassigning references. This is essential for maintaining object
    identity across the multiprocessing boundary.


    **Args:**
    > other_subsystem: The source LocalSubSystemPC containing  
    > updated values from parallel execution.  

