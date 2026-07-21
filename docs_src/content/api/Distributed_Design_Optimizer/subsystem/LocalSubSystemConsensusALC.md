---
title: LocalSubSystemConsensusALC
---

← Back to [subsystem](index.md)

# LocalSubSystemConsensusALC

**Source:** [Distributed_Design_Optimizer\subsystem\LocalSubSystemConsensusALC.py](LocalSubSystemConsensusALC_source.md)

Consensus ALC local subsystem module.

This module provides the local subsystem implementation for the
consensus-based Augmented Lagrangian Coordination method.

## Classes

### LocalSubSystemConsensusALC

> **Inherits from:** [LocalSubSystemBasis](LocalSubSystemBasis.md#localsubsystembasis)

> Local subsystem for consensus-based ALC coordination.

> Implements the local subsystem functionality for consensus-based
> Augmented Lagrangian Coordination.

#### Methods

??? abstract "__init__(self, id: str, level: int, neighborid: List[str], analysis: [AnalysisInterface](optimization/AnalysisInterface.md#analysisinterface), localobjective: [LocalObjectiveInterface](optimization/designproblem/LocalObjectiveInterface.md#localobjectiveinterface), localconstraints: [LocalConstraintsInterface](optimization/designproblem/LocalConstraintsInterface.md#localconstraintsinterface), optimization: [OptimizationInterface](optimization/OptimizationInterface.md#optimizationinterface), local_convergenceindicator_innerloop: [Local_ConvergenceIndicator_Innerloop_Interface](../coordination/convergence/Local_ConvergenceIndicator_Innerloop_Interface.md#local_convergenceindicator_innerloop_interface), local_convergenceindicator_outerloop: [Local_ConvergenceIndicator_Outerloop_Interface](../coordination/convergence/Local_ConvergenceIndicator_Outerloop_Interface.md#local_convergenceindicator_outerloop_interface), updatecouplingparametermethod_outerloop: [UpdateCouplingParameterMethodInterface](../coordination/updatecouplingparametermethod/UpdateCouplingParameterMethodInterface.md#updatecouplingparametermethodinterface)) → None"
    Create a new LocalSubSystemConsensusALC instance.


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
    Validate the components handed to this subsystem by the Consensus_ALC coordination method.

    Validates that the outer-loop update coupling parameter method and the local
    inner/outer loop convergence indicators are compatible with Consensus_ALC.


    **Raises:**
    > ValueError: If a provided component is not compatible with Consensus_ALC.  

??? abstract "append_Controller(self) → None"
    Update local subsystems by appending controller.


??? abstract "mapToController(self) → None"
    Pass, since no controller in consensus ALC.


??? abstract "evaluate_Gradient_CoordinationObjective(self) → None"
    Evaluate the analytical gradient of the coordination objective.

    Assumes the mapped responses Jacobian was evaluated already.

??? abstract "evaluate_Jacobian_CoordinationEqualityConstraints(self) → None"
    Evaluate the Jacobian of the coordination equality constraints.

    Consensus ALC does not have coordination equality constraints, hence no-op.

??? abstract "evaluate_Jacobian_CoordinationInEqualityConstraints(self) → None"
    Evaluate the Jacobian of the coordination inequality constraints.

    Consensus ALC does not have coordination inequality constraints, hence no-op.

??? abstract "evaluateCoordinationObjective(self) → None"
    Evaluate the coordination objective.


??? abstract "evaluateCoordinationEqualityConstraint(self) → None"
    Evaluate the coordination equality constraint.


??? abstract "evaluateCoordinationInequalityConstraint(self) → None"
    Evaluate the coordination inequality constraint.


??? abstract "prepare_OptimizationProblem(self) → None"
    Prepare the optimization problem.


??? abstract "postprocess_Optimization(self) → None"
    Postprocess the optimization.


??? abstract "return_initialized_CouplingParameters(self) → List[[CouplingParametersConsensusALC](couplingparameters/consensus_alc/CouplingParametersConsensusALC.md#couplingparametersconsensusalc)]"
    Return initialized coupling parameters.


    **Returns:**
    > Initialized coupling parameters for each neighbor.  

??? abstract "update_AuxiliaryVariables(self, coupling: [CouplingParametersConsensusALC](couplingparameters/consensus_alc/CouplingParametersConsensusALC.md#couplingparametersconsensusalc)) → None"
    Create initial and then update auxiliary variables using the update formula.

    Uses the initial values defined in the input file.


    **Args:**
    > coupling: Coupling parameters for a consensus ALC neighbor.  

??? abstract "initializeCouplingParameters_before_CopyToMiddleLevel(self) → None"
    Initialize coupling parameters before copying communicated information.

    Create empty placeholders for coupling parameters, i.e. communicated quantities in the algorithms,
    Lagrange multipliers, penalty weights, ...
    The sizes are read by already initialized quantities from the inner loop iteration.

??? abstract "initializeCouplingParameters_after_CopyFromMiddleLevel(self) → None"
    Initialize coupling parameters after copying communicated information.

    Create empty placeholders for coupling parameters, i.e. communicated quantities in the algorithms,
    Lagrange multipliers, penalty weights, ...
    The sizes are read by already initialized quantities from the inner loop iteration.

??? abstract "initializeCouplingParameters_after_Second_CopyFromMiddleLevel(self) → None"
    Initialize coupling parameters after two communication rounds between subsystems.


??? abstract "prepare_updateCouplingParameters(self) → None"
    Prepare coupling parameters before update operations.

    Consensus ALC does not have any outer loop preparations
    to update the coupling parameters.

??? abstract "updateCouplingParameters_innerLoop(self) → None"
    Update auxiliary variables in inner loop directly after local subsystem updates -> See pseudocode.


??? abstract "updateCouplingParameters_outerLoop(self) → None"
    Update coupling parameters in the outer loop.


??? abstract "evaluate_Inconsistencies(self) → None"
    Compute the difference between stored coupling and mapped variables.

    Compares to the latest available data from a subsystem, including consensus constraint violations.
    Computes four + four inconsistency vectors. The first vector is the auxiliary-minus-mapped-response differences of
    the coupling circle. The second vector is the auxiliary-minus-coupling-variable differences of the coupling circle.
    The third and fourth are the difference between the shared design variable vector.
    Similarly, there are four vectors for the consensus constraints.

??? abstract "return_initialized_Inconsistencies(self) → List[[InConsistencySize](../middlelevel/sbdp/InConsistencySize.md#inconsistencysize)]"
    Return initialized inconsistencies.


    **Returns:**
    > List of initialized InConsistencySize, one per coupling parameter.  

??? abstract "set_AuxiliaryVariables_MappedResponse(self, neighborid: str, auxiliaryin: List[float]) → None"
    Set the auxiliary-minus-mapped-response auxiliary variables for a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > auxiliaryin: Auxiliary variable values to set.  

??? abstract "set_AuxiliaryVariables_CouplingVariable(self, neighborid: str, auxiliaryin: List[float]) → None"
    Set the auxiliary-minus-coupling-variable auxiliary variables for a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > auxiliaryin: Auxiliary variable values to set.  

??? abstract "set_AuxiliaryVariables_SharedDesignVariable(self, neighborid: str, auxiliaryin: List[float]) → None"
    Set the auxiliary-minus-shared-design-variable auxiliary variables for a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > auxiliaryin: Auxiliary variable values to set.  

??? abstract "set_AuxiliaryVariables_TargetSharedDesignVariable(self, neighborid: str, auxiliaryin: List[float]) → None"
    Set the auxiliary-minus-target-shared-design-variable auxiliary variables for a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > auxiliaryin: Auxiliary variable values to set.  

??? abstract "set_CoordinationMultipliers_Auxiliary_Minus_MappedResponse(self, neighborid: str, multipliersin: List[float]) → None"
    Set the coordination multipliers for the auxiliary minus mapped response inconsistency of a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > multipliersin: Auxiliary minus mapped response multiplier values to set.  

??? abstract "set_CoordinationMultipliers_Auxiliary_Minus_CouplingVariable(self, neighborid: str, multipliersin: List[float]) → None"
    Set the coordination multipliers for the auxiliary minus coupling variable inconsistency of a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > multipliersin: Auxiliary minus coupling variable multiplier values to set.  

??? abstract "set_CoordinationMultipliers_Auxiliary_Minus_SharedDesignVariable(self, neighborid: str, multipliersin: List[float]) → None"
    Set the coordination multipliers for the auxiliary minus shared design variable inconsistency of a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > multipliersin: Auxiliary minus shared design variable multiplier values to set.  

??? abstract "set_CoordinationMultipliers_Auxiliary_Minus_TargetSharedDesignVariable(self, neighborid: str, multipliersin: List[float]) → None"
    Set the coordination multipliers for the auxiliary minus target shared design variable inconsistency of a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > multipliersin: Auxiliary minus target shared design variable multiplier values to set.  

??? abstract "set_CoordinationWeights_Auxiliary_Minus_MappedResponse(self, neighborid: str, penaltyweightsin: List[float]) → None"
    Set the coordination weights for the auxiliary minus mapped response inconsistency of a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > penaltyweightsin: Auxiliary minus mapped response penalty weight values to set.  

??? abstract "set_CoordinationWeights_Auxiliary_Minus_CouplingVariable(self, neighborid: str, penaltyweightsin: List[float]) → None"
    Set the coordination weights for the auxiliary minus coupling variable inconsistency of a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > penaltyweightsin: Auxiliary minus coupling variable penalty weight values to set.  

??? abstract "set_CoordinationWeights_Auxiliary_Minus_SharedDesignVariable(self, neighborid: str, penaltyweightsin: List[float]) → None"
    Set the coordination weights for the auxiliary minus shared design variable inconsistency of a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > penaltyweightsin: Auxiliary minus shared design variable penalty weight values to set.  

??? abstract "set_CoordinationWeights_Auxiliary_Minus_TargetSharedDesignVariable(self, neighborid: str, penaltyweightsin: List[float]) → None"
    Set the coordination weights for the auxiliary minus target shared design variable inconsistency of a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > penaltyweightsin: Auxiliary minus target shared design variable penalty weight values to set.  

??? abstract "update_state(self, other_subsystem: [LocalSubSystemConsensusALC](LocalSubSystemConsensusALC.md#localsubsystemconsensusalc)) → None"
    Update the state of this LocalSubSystemConsensusALC instance with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.

    The update preserves memory addresses by modifying attribute contents in-place where
    possible, rather than reassigning references. This is essential for maintaining object
    identity across the multiprocessing boundary.


    **Args:**
    > other_subsystem: The source LocalSubSystemConsensusALC containing updated values  
    > from parallel execution.  

