---
title: ALADIN
---

← Back to [coordinationmethod](index.md)

# ALADIN

**Source:** [Distributed_Design_Optimizer\coordination\coordinationmethod\ALADIN.py](ALADIN_source.md)

ALADIN coordination method module.

This module implements the Augmented Lagrangian based Alternating Direction
Inexact Newton (ALADIN) coordination method for distributed optimization.

## Classes

### ALADIN

> **Inherits from:** [CoordinationMethodBasis](CoordinationMethodBasis.md#coordinationmethodbasis)

> ALADIN coordination method for distributed optimization.

> This coordination method implements the Augmented Lagrangian based
> Alternating Direction Inexact Newton (ALADIN) algorithm. It combines
> decentralized local subproblem solves with a centralized controller
> (quadratic programming) step that uses gradient and Hessian information
> to drive the coupled subsystems towards consensus.

#### Methods

??? abstract "__init__(self, convergence_indicator_innerloop: [ConvergenceIndicator_Innerloop_Interface](../convergence/ConvergenceIndicator_Innerloop_Interface.md#convergenceindicator_innerloop_interface), convergence_indicator_outerloop: [ConvergenceIndicator_Outerloop_Interface](../convergence/ConvergenceIndicator_Outerloop_Interface.md#convergenceindicator_outerloop_interface), updatecouplingparametermethod_outerloop: [UpdateCouplingParameterMethodInterface](../updatecouplingparametermethod/UpdateCouplingParameterMethodInterface.md#updatecouplingparametermethodinterface), iterationscheme: [IterationSchemeInterface](../innerloop_iterationscheme/IterationSchemeInterface.md#iterationschemeinterface)) → None"
    Initialize the ALADIN coordination method.


    **Args:**
    > convergence_indicator_innerloop: Convergence indicator for inner loop.  
    > convergence_indicator_outerloop: Convergence indicator for outer loop.  
    > updatecouplingparametermethod_outerloop: Method for updating coupling parameters in outer loop.  
    > iterationscheme: Iteration scheme for inner loop execution.  

??? abstract "validate_inputs(self) → None"
    Validate the inputs provided to the ALADIN coordination method.

    Validates that the iteration scheme is compatible with ALADIN. The
    outer-loop update coupling parameter method and the convergence
    indicators are validated by the subsystems they are handed to
    (see LocalSubSystemALADIN.validate_inputs).


    **Raises:**
    > ValueError: If any parameter is outside the allowed range.  

??? abstract "createSubSystems(self, id_list: List[str], level_list: List[int], neighborid_list: List[List[str]], analysis_list: List[[AnalysisInterface](../../subsystem/optimization/AnalysisInterface.md#analysisinterface)], localobjective_list: List[[LocalObjectiveInterface](../../subsystem/optimization/designproblem/LocalObjectiveInterface.md#localobjectiveinterface)], localconstraints_list: List[[LocalConstraintsInterface](../../subsystem/optimization/designproblem/LocalConstraintsInterface.md#localconstraintsinterface)], optimization_list: List[[OptimizationInterface](../../subsystem/optimization/OptimizationInterface.md#optimizationinterface)]) → List[[LocalSubSystemALADIN](../../subsystem/LocalSubSystemALADIN.md#localsubsystemaladin)]"
    Create local subsystems for ALADIN coordination.


    **Args:**
    > id_list: List of subsystem identifiers.  
    > level_list: List of subsystem hierarchy levels.  
    > neighborid_list: List of neighbor ID lists for each subsystem.  
    > analysis_list: List of analysis interfaces.  
    > localobjective_list: List of local objective interfaces.  
    > localconstraints_list: List of local constraints interfaces.  
    > optimization_list: List of optimization interfaces.  


    **Returns:**
    > List of created ALADIN local subsystems.  

??? abstract "createControllerSubSystem(self, subsystemsIn: List[[LocalSubSystemALADIN](../../subsystem/LocalSubSystemALADIN.md#localsubsystemaladin)]) → [SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface) | None"
    Create the ALADIN controller subsystem.


    **Args:**
    > subsystemsIn: List of local subsystems to coordinate.  


    **Returns:**
    > The created controller subsystem.  

??? abstract "createMiddleLevel(self, idparent: str, idchild: str, multiprocessing_lock: object) → [LocalToLocal_MiddleLevelDataStorageALADIN](../../middlelevel/aladin/LocalToLocal_MiddleLevelDataStorageALADIN.md#localtolocal_middleleveldatastoragealadin)"
    Create a local-to-local middle level data storage.


    **Args:**
    > idparent: Identifier of the parent subsystem.  
    > idchild: Identifier of the child subsystem.  
    > multiprocessing_lock: Optional lock for thread-safe access in multiprocessing.  


    **Returns:**
    > The created local-to-local middle level data storage.  

??? abstract "createControllerMiddleLevel(self, idparent: str, idchild: str, local_neighbors_list: List[str], multiprocessing_lock: object) → [LocalController_MiddleLevelDataStorageALADIN](../../middlelevel/aladin/LocalController_MiddleLevelDataStorageALADIN.md#localcontroller_middleleveldatastoragealadin) | None"
    Create middle level between controller and local subsystem.


    **Args:**
    > idparent: Identifier of the parent (controller) subsystem.  
    > idchild: Identifier of the child (local) subsystem.  
    > local_neighbors_list: List of neighbor IDs for the local subsystem.  
    > multiprocessing_lock: Optional lock for thread-safe access in multiprocessing.  


    **Returns:**
    > The created local-to-controller middle level data storage.  

??? abstract "centralized_prepare_updateCouplingParameters(self, subsystemsIn: List[[LocalSubSystemALADIN](../../subsystem/LocalSubSystemALADIN.md#localsubsystemaladin) | [ControllerSubSystemALADIN](../../subsystem/ControllerSubSystemALADIN.md#controllersubsystemaladin)]) → None"
    Prepare centralized update of coupling parameters for all subsystems.

    For ALADIN, no centralized operation is required.


    **Args:**
    > subsystemsIn: List of subsystems to prepare coupling parameters for.  

??? abstract "print_beginning_of_centralized_prepare_updateCouplingParameters(self) → None"
    Nothing to print.

