---
title: ControllerSubSystemALADIN
---

← Back to [subsystem](index.md)

# ControllerSubSystemALADIN

**Source:** [Distributed_Design_Optimizer\subsystem\ControllerSubSystemALADIN.py](ControllerSubSystemALADIN_source.md)

ALADIN controller subsystem module.

This module provides the controller subsystem implementation for the
ALADIN coordination method.

## Classes

### ControllerSubSystemALADIN

> **Inherits from:** [ControllerSubSystemBasis](ControllerSubSystemBasis.md#controllersubsystembasis)

> Controller subsystem implementation for the ALADIN coordination method.

> Implements the controller QP formulation for ALADIN distributed optimization,
> including assembly of the quadratic term, linear term, and constraint matrix,
> as well as mapping of design variables to coupling parameters.

#### Methods

??? abstract "__init__(self, neighborid: List[str], neighbors_of_neighbors_ids: Dict[str, List[str]], optimization: [OptimizationController](optimization/OptimizationController.md#optimizationcontroller)) → None"
    Creates a new instance of ControllerSubSystemALADIN.


    **Args:**
    > neighborid: List of identifiers for the neighboring local subsystems.  
    > neighbors_of_neighbors_ids: Mapping of local subsystem ID to its neighbor IDs.  
    > optimization: Optimization controller for solving the controller QP.  

??? abstract "validate_inputs(self) → None"
    Validate the components handed to this subsystem.

    The ALADIN controller does not receive convergence indicators, an update
    coupling parameter method, or an iteration scheme from the coordination
    method. Those components are fixed internally (always-converged indicators
    and a no-op update method). There is therefore nothing to validate.

??? abstract "set_DesignVariables(self, designvariables: List[float]) → None"
    Set the design variable vector (scaled01 values).


    **Args:**
    > designvariables: Design variable vector in scaled01 values.  

??? abstract "get_Indices_Map(self) → Dict[Tuple[str, str], List[List[int]]]"
    Return the map of indices for each i <-> j coupling.

    For each i <-> j coupling, returns the positions of the corresponding
    blocks in self._designvariables. Keys are the id pairs (i,j),
    values = ((index_i,index_j), (start_tau_left, end_tau_left),
    (start_tau_shared, end_tau_shared)).


    **Returns:**
    > Mapping from id pairs (i,j) to lists of index pairs in  
    > self._designvariables.  

??? abstract "check_Decomposition(self, couplingparameters: List[[ControllerCouplingParametersALADIN](couplingparameters/aladin/ControllerCouplingParametersALADIN.md#controllercouplingparametersaladin)], id_i: str, id_j: str) → List[bool]"
    Check whether the coupling i->j is decomposed, i.e. j->i also exists.

    Return a Boolean list, where the first entry indicates
    the decomposition in the mapped responses constraints and
    the second entry the decomposition in the shared variables.


    **Args:**
    > couplingparameters: List of controller coupling parameters.  
    > id_i: Identifier of subsystem i.  
    > id_j: Identifier of subsystem j.  


    **Returns:**
    > Boolean list [mapped_responses, shared_variables, coupling_variables, target_shared].  

??? abstract "initialize_MapIndices(self) → None"
    Set self._indices_map by defining the index mapping for all couplings.

    For each i <-> j coupling, determines the positions of the corresponding
    blocks in self._designvariables. Keys are the id pairs (i,j),
    values = ((index_i, index_j), (start_tau_left, end_tau_left),
    (start_tau_shared, end_tau_shared)).

??? abstract "mapToCouplingParameters(self) → None"
    Split design variables into delta_d and tau and set the corresponding LTCPs in CCP.


??? abstract "initializeCouplingParameters_before_CopyToMiddleLevel(self) → None"
    Controller subsystem does not initialize coupling parameters, so we leave this function empty.


??? abstract "initializeCouplingParameters_after_CopyFromMiddleLevel(self) → None"
    Controller subsystem does not initialize coupling parameters, so we leave this function empty.


??? abstract "initializeCouplingParameters_after_Second_CopyFromMiddleLevel(self) → None"
    Controller subsystem does not initialize coupling parameters, so we leave this function empty.


??? abstract "updateCouplingParameters_innerLoop(self) → None"
    Update coupling parameters in the inner loop.

??? abstract "prepare_updateCouplingParameters(self) → None"
    Prepare coupling parameters before update operations.

??? abstract "updateCouplingParameters_outerLoop(self) → None"
    Update coupling parameters during outer loop iteration.

??? abstract "return_initialized_CouplingParameters(self) → List[[ControllerCouplingParametersALADIN](couplingparameters/aladin/ControllerCouplingParametersALADIN.md#controllercouplingparametersaladin)]"
    Return a fresh list of initialized ControllerCouplingParametersALADIN.


    **Returns:**
    > List of initialized coupling parameters with matching IDs.  

??? abstract "evaluateCoordinationObjective(self) → None"
    Evaluate the coordination objective (the controller's QP objective in ALADIN).


??? abstract "evaluate_Gradient_CoordinationObjective(self) → None"
    Evaluate the analytical gradient of the coordination objective.

    Assumes the QP data P and q were assembled already (see prepare_OptimizationProblem).

??? abstract "evaluateCoordinationEqualityConstraint(self) → None"
    Evaluate the equality constraints of the controller's QP optimization problem.

??? abstract "evaluateCoordinationInequalityConstraint(self) → None"
    Evaluate the inequality constraints of the controller's QP optimization problem.

    These stem from the local inequality and bound constraints assembled into the
    QP (G*delta_d - h <= 0); the result is an empty vector if none exist.

??? abstract "evaluate_Jacobian_CoordinationEqualityConstraints(self) → None"
    Evaluate the Jacobian of the coordination equality constraints.

??? abstract "evaluate_Jacobian_CoordinationInEqualityConstraints(self) → None"
    Evaluate the Jacobian of the coordination inequality constraints.

??? abstract "prepare_OptimizationProblem(self) → None"
    Prepare the QP optimization problem by assembling P, q, and A.

??? abstract "qp_quadratic_term(self) → np.typing.ArrayLike"
    Compute the symmetrized quadratic term matrix P for the ALADIN QP.


    **Returns:**
    > The symmetrized matrix P such that the QP objective is 0.5*d^T*P*d + q^T*d.  

??? abstract "qp_linear_term(self) → np.typing.ArrayLike"
    Compute the linear term vector q for the ALADIN QP.


    **Returns:**
    > The vector q such that the QP objective is 0.5*d^T*P*d + q^T*d.  

??? abstract "qp_constraint_equality_matrix(self) → np.typing.ArrayLike"
    Compute the constraint matrix A for the ALADIN QP.


    **Returns:**
    > The block-structured matrix A defining the linear equality constraints A*d = 0.  

??? abstract "qp_constraint_inequality_matrix(self) → np.typing.ArrayLike"
    Compute the constraint inequality matrix G for the ALADIN QP.


    **Returns:**
    > The block-structured matrix G defining the linear inequality constraints G*d <= h.  

??? abstract "qp_constraint_inequality_righthandside(self) → np.typing.ArrayLike"
    Compute the right-hand side vector h for the inequality constraints of the ALADIN QP.


    **Returns:**
    > The vector h defining the right-hand side of the linear inequality constraints G*d <= h.  

??? abstract "postprocess_Optimization(self) → None"
    Postprocess optimization.

??? abstract "update_state(self, other_subsystem: [ControllerSubSystemALADIN](ControllerSubSystemALADIN.md#controllersubsystemaladin)) → None"
    Update the state of this ControllerSubSystemALADIN instance with values from another instance.

    This method is necessary for multiprocessing. After parallel execution completes,
    this method updates the original object's attribute values while preserving their
    memory addresses.


    **Args:**
    > other_subsystem: The source ControllerSubSystemALADIN containing updated values  
    > from parallel execution.  

