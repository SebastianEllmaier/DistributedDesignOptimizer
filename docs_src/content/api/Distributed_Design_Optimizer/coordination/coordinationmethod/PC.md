---
title: PC
---

← Back to [coordinationmethod](index.md)

# PC

**Source:** [Distributed_Design_Optimizer\coordination\coordinationmethod\PC.py](PC_source.md)

Penalty Coordination (PC) method module.

This module implements the Penalty Coordination method for distributed
multidisciplinary design optimization.

## Classes

### PC

> **Inherits from:** [CoordinationMethodBasis](CoordinationMethodBasis.md#coordinationmethodbasis)

> Penalty Coordination (PC) method implementation.

> This coordination method uses penalty relaxation to coordinate
> subsystems in a distributed optimization problem. It manages penalty weights
> to enforce consistency between coupled subsystems.

#### Methods

??? abstract "__init__(self, convergence_indicator_innerloop: [ConvergenceIndicator_Innerloop_Interface](../convergence/ConvergenceIndicator_Innerloop_Interface.md#convergenceindicator_innerloop_interface), convergence_indicator_outerloop: [ConvergenceIndicator_Outerloop_Interface](../convergence/ConvergenceIndicator_Outerloop_Interface.md#convergenceindicator_outerloop_interface), updatecouplingparametermethod_outerloop: [UpdateCouplingParameterMethodInterface](../updatecouplingparametermethod/UpdateCouplingParameterMethodInterface.md#updatecouplingparametermethodinterface), iterationscheme: [IterationSchemeInterface](../innerloop_iterationscheme/IterationSchemeInterface.md#iterationschemeinterface)) → None"
    Initialize the PC coordination method.


    **Args:**
    > convergence_indicator_innerloop: Convergence indicator for inner loop (e.g., ConvergenceIndicator_Innerloop_DeWit).  
    > convergence_indicator_outerloop: Convergence indicator for outer loop (e.g., ConvergenceIndicator_Outerloop_DeWit).  
    > updatecouplingparametermethod_outerloop: Method for updating coupling parameters in outer loop.  
    > iterationscheme: Iteration scheme for inner loop execution.  

??? abstract "validate_inputs(self) → None"
    Validate the inputs provided to the PC coordination method.

    Validates that the iteration scheme is compatible with PC. Validation of the
    update coupling parameter method and convergence indicators is delegated to
    LocalSubSystemPC.validate_inputs, since those components are handed to the
    subsystems.


    **Raises:**
    > ValueError: If any parameter is outside the allowed range.  

??? abstract "createSubSystems(self, id_list: List[str], level_list: List[int], neighborid_list: List[List[str]], analysis_list: List[[AnalysisInterface](../../subsystem/optimization/AnalysisInterface.md#analysisinterface)], localobjective_list: List[[LocalObjectiveInterface](../../subsystem/optimization/designproblem/LocalObjectiveInterface.md#localobjectiveinterface)], localconstraints_list: List[[LocalConstraintsInterface](../../subsystem/optimization/designproblem/LocalConstraintsInterface.md#localconstraintsinterface)], optimization_list: List[[OptimizationInterface](../../subsystem/optimization/OptimizationInterface.md#optimizationinterface)]) → List[[LocalSubSystemPC](../../subsystem/LocalSubSystemPC.md#localsubsystempc)]"
    Create subsystems for penalty coordination.


    **Args:**
    > id_list: List of unique identifiers for each subsystem.  
    > level_list: List of hierarchy levels for each subsystem.  
    > neighborid_list: List of neighbor subsystem IDs for each subsystem.  
    > analysis_list: List of analysis objects for each subsystem.  
    > localobjective_list: List of local objective functions for each subsystem.  
    > localconstraints_list: List of local constraints for each subsystem.  
    > optimization_list: List of optimization objects for each subsystem.  


    **Returns:**
    > List of initialized LocalSubSystemPC objects.  

??? abstract "createControllerSubSystem(self, subsystemsIn: List[[LocalSubSystemPC](../../subsystem/LocalSubSystemPC.md#localsubsystempc)]) → [SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface) | None"
    Create a controller subsystem for coordinating local subsystems.


    **Args:**
    > subsystemsIn: List of local subsystems to be coordinated.  


    **Returns:**
    > None, as PC operates without a central controller.  

??? abstract "createMiddleLevel(self, idparent: str, idchild: str, multiprocessing_lock: object) → [MiddleLevelDataStoragePC](../../middlelevel/pc/MiddleLevelDataStoragePC.md#middleleveldatastoragepc)"
    Create a middle level data storage for coupling between subsystems.


    **Args:**
    > idparent: Identifier of the parent subsystem.  
    > idchild: Identifier of the child subsystem.  
    > multiprocessing_lock: Optional lock for thread-safe access in multiprocessing.  


    **Returns:**
    > MiddleLevelDataStorage instance for managing coupling data.  

??? abstract "createControllerMiddleLevel(self, idparent: str, idchild: str, local_neighbors_list: List[str], multiprocessing_lock: object) → [MiddleLevelDataStoragePC](../../middlelevel/pc/MiddleLevelDataStoragePC.md#middleleveldatastoragepc) | None"
    Create middle level between controller and local subsystem.


    **Args:**
    > idparent: Identifier of the parent (controller) subsystem.  
    > idchild: Identifier of the child subsystem.  
    > local_neighbors_list: List of neighbor IDs for the local subsystem (unused).  
    > multiprocessing_lock: Optional lock for thread-safe access in multiprocessing.  


    **Returns:**
    > None, as PC operates without a central controller.  

??? abstract "centralized_prepare_updateCouplingParameters(self, subsystemsIn: List[[LocalSubSystemPC](../../subsystem/LocalSubSystemPC.md#localsubsystempc)]) → None"
    Prepare centralized update of coupling parameters for all subsystems.

    For PC, no centralized operation is required.


    **Args:**
    > subsystemsIn: List of subsystems to prepare coupling parameters for.  

??? abstract "print_beginning_of_centralized_prepare_updateCouplingParameters(self) → None"
    Nothing to print.

