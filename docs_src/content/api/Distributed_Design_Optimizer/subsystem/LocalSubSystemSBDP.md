---
title: LocalSubSystemSBDP
---

← Back to [subsystem](index.md)

# LocalSubSystemSBDP

**Source:** [Distributed_Design_Optimizer\subsystem\LocalSubSystemSBDP.py](LocalSubSystemSBDP_source.md)

Sensitivity Based Distributed Programming (SBDP) local subsystem module.

This module provides the local subsystem implementation for the Sensitivity
Based Distributed Programming (SBDP) method (Algorithm 3).

Each outer iteration every subsystem solves, in parallel, the local NLP

min   v_f(r) + sum_j ( grad_d^j L^(k) )^T ( d - d^(k) )
s.t.  local inequality constraints  g(r) <= 0
local equality constraints    h(r)  = 0
coordination equality constraint (hard):
[ H(r) - h ; S_z d - z ] = 0   | lambda

The linear sensitivity term uses the neighbor's coordination-equality Lagrange
multipliers (communicated via the middle level and stored as copies). After the
solve, the subsystem's own coordination-equality multipliers ``lambda`` are
recovered from the KKT system and published to the neighbors.

## Classes

### LocalSubSystemSBDP

> **Inherits from:** [LocalSubSystemBasis](LocalSubSystemBasis.md#localsubsystembasis)

> Local subsystem implementation using Sensitivity Based Distributed Programming.

> Implements the SBDP method (Algorithm 3) for distributed optimization. The
> coordination coupling is imposed as a hard equality constraint, whose Lagrange
> multipliers are recovered from the local KKT system and communicated to the
> neighbors, where they enter the linear sensitivity term of the local objective.

#### Methods

??? abstract "__init__(self, id: str, level: int, neighborid: List[str], analysis: [AnalysisInterface](optimization/AnalysisInterface.md#analysisinterface), localobjective: [LocalObjectiveInterface](optimization/designproblem/LocalObjectiveInterface.md#localobjectiveinterface), localconstraints: [LocalConstraintsInterface](optimization/designproblem/LocalConstraintsInterface.md#localconstraintsinterface), optimization: [OptimizationInterface](optimization/OptimizationInterface.md#optimizationinterface), local_convergenceindicator_innerloop: [Local_ConvergenceIndicator_Innerloop_Interface](../coordination/convergence/Local_ConvergenceIndicator_Innerloop_Interface.md#local_convergenceindicator_innerloop_interface), local_convergenceindicator_outerloop: [Local_ConvergenceIndicator_Outerloop_Interface](../coordination/convergence/Local_ConvergenceIndicator_Outerloop_Interface.md#local_convergenceindicator_outerloop_interface), updatecouplingparametermethod_outerloop: [UpdateCouplingParameterMethodInterface](../coordination/updatecouplingparametermethod/UpdateCouplingParameterMethodInterface.md#updatecouplingparametermethodinterface)) → None"
    Create a new LocalSubSystemSBDP instance.


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
    Validate the components handed to this subsystem by the SBDP coordination method.

    Validates that the outer-loop update coupling parameter method and the local
    inner/outer loop convergence indicators are compatible with SBDP.


    **Raises:**
    > ValueError: If a provided component is not compatible with SBDP.  

??? abstract "append_Controller(self) → None"
    Update local subsystems by appending controller.


??? abstract "mapToController(self) → None"
    Pass, since no controller in SBDP.


??? abstract "evaluateCoordinationObjective(self) → None"
    Evaluate the coordination objective (linear sensitivity term).

    Computes ``grad^T (d - d^(k))`` where ``grad`` is the sensitivity gradient
    and ``d^(k)`` is the design of the previous outer loop iteration.

??? abstract "evaluate_Gradient_CoordinationObjective(self) → None"
    Evaluate the analytical gradient of the coordination objective.

    The gradient of the linear sensitivity term is the constant sensitivity
    gradient, independent of the design variables. It is stored exactly, so no
    finite-difference approximation is required.

??? abstract "evaluateCoordinationEqualityConstraint(self) → None"
    Evaluate the coordination equality constraint.

    Builds, per neighbor, the vertical stack ``[ H(r) - h ; S_z d - z ]``.

    Each block is obtained from an InConsistencySize object (as in
    LocalSubSystemPC.evaluateCoordinationObjective). The mapped-response block
    ``H(r) - h`` is the negated ``copy_couplingvariable - mappedresponse``
    inconsistency, and the shared-design-variable block ``S_z d - z`` is the
    negated ``copy_targetshareddesignvariable - shareddesignvariable``
    inconsistency, so that the stored values equal ``H(r) - h`` and ``S_z d - z``
    respectively.

    NOTE: The per-neighbor block-presence conditionals used here must stay
    identical to those in evaluate_Jacobian_CoordinationEqualityConstraints() and
    the multiplier distribution in postprocess_Optimization(), so that the
    constraint value, its Jacobian and the multiplier decomposition remain
    consistently ordered.

??? abstract "evaluateCoordinationInequalityConstraint(self) → None"
    Evaluate the coordination inequality constraint.

    SBDP does not use coordination inequality constraints.

??? abstract "evaluate_Jacobian_CoordinationEqualityConstraints(self) → None"
    Evaluate the Jacobian of the coordination equality constraints.

    The rows are ordered exactly as in evaluateCoordinationEqualityConstraint().
    The mapped-response block rows ``d(H(r) - h)/dd = dH/dd`` are returned with
    ``None`` entries so that they are filled by finite differences. The
    shared-design-variable block rows ``d(S_z d - z)/dd`` are the exact selection
    rows (a single 1.0 at the shared-design position).

??? abstract "evaluate_Jacobian_CoordinationInEqualityConstraints(self) → None"
    Evaluate the Jacobian of the coordination inequality constraints.

    SBDP does not have coordination inequality constraints, hence no-op.

??? abstract "prepare_OptimizationProblem(self) → None"
    Prepare the optimization problem.

    Captures the design of the previous outer loop iteration, d^(k), used as the
    fixed linearization point of the sensitivity term, and computes the constant
    per-neighbor sensitivity gradients of the coordination objective once for the
    whole inner solve, storing each on its coupling parameter.

    Each neighbor's sensitivity gradient ``grad_d^j L^(k)`` is obtained by scattering
    the negated neighbor coordination-equality multipliers into the design-variable
    space using the coupling / shared-design index maps. They depend only on the
    neighbor multipliers communicated at the start of the outer iteration and are
    therefore constant throughout the inner solve, so computing them once here avoids
    recomputing them on every black-box optimizer (e.g. PyNomad) evaluation.

??? abstract "postprocess_Optimization(self) → None"
    Postprocess the optimization.

    Recovers the coordination-equality Lagrange multipliers from the local KKT
    system and distributes them into the coupling parameters, so that they are
    subsequently published to the neighbors via the middle level.

??? abstract "return_initialized_CouplingParameters(self) → List[[CouplingParametersSBDP](couplingparameters/sbdp/CouplingParametersSBDP.md#couplingparameterssbdp)]"
    Return initialized coupling parameters.


    **Returns:**
    > List of initialized CouplingParametersSBDP, one per neighbor.  

??? abstract "initializeCouplingParameters_before_CopyToMiddleLevel(self) → None"
    Initialize coupling parameters before copying from neighboring subsystem.


??? abstract "initializeCouplingParameters_after_CopyFromMiddleLevel(self) → None"
    Initialize coupling parameters after copying from neighboring subsystems.

    Seeds the subsystem's own coordination-equality multipliers, sized to match
    the corresponding coordination-equality blocks, so that they are communicated
    to the neighbors from the first iteration onwards.

??? abstract "initializeCouplingParameters_after_Second_CopyFromMiddleLevel(self) → None"
    Initialize coupling parameters after two communication rounds between subsystems.


??? abstract "prepare_updateCouplingParameters(self) → None"
    Prepare coupling parameters before update operations.


??? abstract "updateCouplingParameters_innerLoop(self) → None"
    Update coupling parameters in the inner loop.


??? abstract "updateCouplingParameters_outerLoop(self) → None"
    Update coupling parameters during outer loop iteration.

    In SBDP the coordination multipliers are recomputed from the KKT system in
    each subsystem solve (see postprocess_Optimization) rather than by a dual
    ascent update, hence no outer-loop multiplier update is performed here.

??? abstract "evaluate_Inconsistencies(self) → None"
    Compute the difference between stored coupling and mapped variables.

    Delegates to the base class implementation which computes inconsistency
    vectors for the mapped-response side, coupling-variable side, shared design
    variables, and target shared design variables of each coupling circle.

??? abstract "return_initialized_Inconsistencies(self) → List[[InConsistencySize](../middlelevel/sbdp/InConsistencySize.md#inconsistencysize)]"
    Return initialized inconsistencies.


    **Returns:**
    > List of initialized InConsistencySize, one per coupling parameter.  

??? abstract "set_Multipliers_MappedResponse_Minus_CopyCouplingVariable(self, neighborid: str, multipliersin: List[float]) → None"
    Set the mapped-response coordination multipliers of a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > multipliersin: List of multiplier values to set.  

??? abstract "set_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, neighborid: str, multipliersin: List[float]) → None"
    Set the shared-design-variable coordination multipliers of a neighbor.


    **Args:**
    > neighborid: Identifier of the neighboring subsystem.  
    > multipliersin: List of multiplier values to set.  

??? abstract "update_state(self, other_subsystem: [LocalSubSystemSBDP](LocalSubSystemSBDP.md#localsubsystemsbdp)) → None"
    Update the state of this LocalSubSystemSBDP instance with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.


    **Args:**
    > other_subsystem: The source LocalSubSystemSBDP containing updated values  
    > from parallel execution.  

