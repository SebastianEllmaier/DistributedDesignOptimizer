---
title: SBDP
---

← Back to [coordinationmethod](index.md)

# SBDP

**Source:** [Distributed_Design_Optimizer\coordination\coordinationmethod\SBDP.py](SBDP_source.md)

Sensitivity Based Distributed Programming (SBDP) coordination method module.

This module implements the Sensitivity Based Distributed Programming (SBDP,
Algorithm 3) coordination method for distributed multidisciplinary design
optimization.

## Classes

### SBDP

> **Inherits from:** [CoordinationMethodBasis](CoordinationMethodBasis.md#coordinationmethodbasis)

> Sensitivity Based Distributed Programming coordination method.

> This coordination method implements SBDP (Algorithm 3). Each subsystem
> imposes its coupling as a hard coordination equality constraint and, once per
> outer iteration, solves a local NLP whose objective is augmented with a linear
> sensitivity term built from the neighbors' coordination-equality Lagrange
> multipliers. The subproblems are fully independent within an outer iteration
> and are therefore solved in parallel.

#### Methods

??? abstract "__init__(self, convergence_indicator_innerloop: [ConvergenceIndicator_Innerloop_Interface](../convergence/ConvergenceIndicator_Innerloop_Interface.md#convergenceindicator_innerloop_interface), convergence_indicator_outerloop: [ConvergenceIndicator_Outerloop_Interface](../convergence/ConvergenceIndicator_Outerloop_Interface.md#convergenceindicator_outerloop_interface), updatecouplingparametermethod_outerloop: [UpdateCouplingParameterMethodInterface](../updatecouplingparametermethod/UpdateCouplingParameterMethodInterface.md#updatecouplingparametermethodinterface), iterationscheme: [IterationSchemeInterface](../innerloop_iterationscheme/IterationSchemeInterface.md#iterationschemeinterface)) → None"
    Initialize the SBDP coordination method.


    **Args:**
    > convergence_indicator_innerloop: Convergence indicator for inner loop  
    > (SBDP performs a single inner pass per outer iteration, use  
    > ConvergenceIndicator_Innerloop_AlwaysConverged).  
    > convergence_indicator_outerloop: Convergence indicator for outer loop  
    > (e.g., ConvergenceIndicator_Outerloop_DeWit). Its tolerance plays  
    > the role of the SBDP hyperparameter epsilon_k.  
    > updatecouplingparametermethod_outerloop: Method for updating coupling  
    > parameters in the outer loop. SBDP recomputes the multipliers via  
    > the KKT system, so use UpdateCouplingParameterMethod_NoOp.  
    > iterationscheme: Iteration scheme for inner loop execution.  

??? abstract "validate_inputs(self) → None"
    Validate the inputs provided to the SBDP coordination method.

    Validates that the iteration scheme is compatible with SBDP. Validation of the
    update coupling parameter method and convergence indicators is delegated to
    LocalSubSystemSBDP.validate_inputs, since those components are handed to the
    subsystems.


    **Raises:**
    > ValueError: If any parameter is outside the allowed range.  

??? abstract "createSubSystems(self, id_list: List[str], level_list: List[int], neighborid_list: List[List[str]], analysis_list: List[[AnalysisInterface](../../subsystem/optimization/AnalysisInterface.md#analysisinterface)], localobjective_list: List[[LocalObjectiveInterface](../../subsystem/optimization/designproblem/LocalObjectiveInterface.md#localobjectiveinterface)], localconstraints_list: List[[LocalConstraintsInterface](../../subsystem/optimization/designproblem/LocalConstraintsInterface.md#localconstraintsinterface)], optimization_list: List[[OptimizationInterface](../../subsystem/optimization/OptimizationInterface.md#optimizationinterface)]) → List[[LocalSubSystemSBDP](../../subsystem/LocalSubSystemSBDP.md#localsubsystemsbdp)]"
    Create subsystems for Sensitivity Based Distributed Programming.


    **Args:**
    > id_list: List of unique identifiers for each subsystem.  
    > level_list: List of hierarchy levels for each subsystem.  
    > neighborid_list: List of neighbor subsystem IDs for each subsystem.  
    > analysis_list: List of analysis objects for each subsystem.  
    > localobjective_list: List of local objective functions for each subsystem.  
    > localconstraints_list: List of local constraints for each subsystem.  
    > optimization_list: List of optimization objects for each subsystem.  


    **Returns:**
    > List of initialized LocalSubSystemSBDP objects.  

??? abstract "createControllerSubSystem(self, subsystemsIn: List[[LocalSubSystemSBDP](../../subsystem/LocalSubSystemSBDP.md#localsubsystemsbdp)]) → [SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface) | None"
    Create a controller subsystem for coordinating local subsystems.


    **Args:**
    > subsystemsIn: List of local subsystems to be coordinated.  


    **Returns:**
    > None, as SBDP operates without a central controller.  

??? abstract "createMiddleLevel(self, idparent: str, idchild: str, multiprocessing_lock: object) → [MiddleLevelDataStorageSBDP](../../middlelevel/sbdp/MiddleLevelDataStorageSBDP.md#middleleveldatastoragesbdp)"
    Create a middle level data storage for coupling between subsystems.


    **Args:**
    > idparent: Identifier of the parent subsystem.  
    > idchild: Identifier of the child subsystem.  
    > multiprocessing_lock: Optional lock for thread-safe access in multiprocessing.  


    **Returns:**
    > MiddleLevelDataStorage instance for managing coupling data.  

??? abstract "createControllerMiddleLevel(self, idparent: str, idchild: str, local_neighbors_list: List[str], multiprocessing_lock: object) → [MiddleLevelDataStorageSBDP](../../middlelevel/sbdp/MiddleLevelDataStorageSBDP.md#middleleveldatastoragesbdp) | None"
    Create middle level between controller and local subsystem.


    **Args:**
    > idparent: Identifier of the parent (controller) subsystem.  
    > idchild: Identifier of the child subsystem.  
    > local_neighbors_list: List of neighbor IDs for the local subsystem (unused).  
    > multiprocessing_lock: Optional lock for thread-safe access in multiprocessing.  


    **Returns:**
    > None, as SBDP operates without a central controller.  

??? abstract "centralized_prepare_updateCouplingParameters(self, subsystemsIn: List[[LocalSubSystemSBDP](../../subsystem/LocalSubSystemSBDP.md#localsubsystemsbdp)]) → None"
    Prepare centralized update of coupling parameters for all subsystems.

    For SBDP, no centralized operation is required.


    **Args:**
    > subsystemsIn: List of subsystems to prepare coupling parameters for.  

??? abstract "print_beginning_of_centralized_prepare_updateCouplingParameters(self) → None"
    Nothing to print.

