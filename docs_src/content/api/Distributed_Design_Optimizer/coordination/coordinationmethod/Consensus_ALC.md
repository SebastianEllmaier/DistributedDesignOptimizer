---
title: Consensus_ALC
---

← Back to [coordinationmethod](index.md)

# Consensus_ALC

**Source:** [Distributed_Design_Optimizer\coordination\coordinationmethod\Consensus_ALC.py](Consensus_ALC_source.md)

Consensus-based ALC coordination method module.

This module implements consensus-based Augmented Lagrangian Coordination
for distributed multidisciplinary design optimization.

## Classes

### Consensus_ALC

> **Inherits from:** [CoordinationMethodBasis](CoordinationMethodBasis.md#coordinationmethodbasis)

> Consensus ALC coordination method for distributed optimization.

> This coordination method implements consensus-based Augmented Lagrangian
> Coordination. Each subsystem maintains its own copy of the shared coupling
> variables and drives them towards a common consensus value, allowing the
> independent subproblems to be solved fully in parallel.

#### Methods

??? abstract "__init__(self, convergence_indicator_innerloop: [ConvergenceIndicator_Innerloop_Interface](../convergence/ConvergenceIndicator_Innerloop_Interface.md#convergenceindicator_innerloop_interface), convergence_indicator_outerloop: [ConvergenceIndicator_Outerloop_Interface](../convergence/ConvergenceIndicator_Outerloop_Interface.md#convergenceindicator_outerloop_interface), updatecouplingparametermethod_outerloop: [UpdateCouplingParameterMethodInterface](../updatecouplingparametermethod/UpdateCouplingParameterMethodInterface.md#updatecouplingparametermethodinterface), iterationscheme: [IterationSchemeInterface](../innerloop_iterationscheme/IterationSchemeInterface.md#iterationschemeinterface)) → None"
    Initialize the Consensus_ALC coordination method.


    **Args:**
    > convergence_indicator_innerloop: Convergence indicator for inner loop (e.g., ConvergenceIndicator_Innerloop_DeWit).  
    > convergence_indicator_outerloop: Convergence indicator for outer loop (e.g., ConvergenceIndicator_Outerloop_DeWit).  
    > updatecouplingparametermethod_outerloop: Method for updating coupling parameters in outer loop.  
    > iterationscheme: Iteration scheme for inner loop execution.  

??? abstract "validate_inputs(self) → None"
    Validate the inputs provided to the Consensus_ALC coordination method.

    Validates that the iteration scheme is compatible with Consensus_ALC. Validation of
    the update coupling parameter method and convergence indicators is delegated to
    LocalSubSystemConsensusALC.validate_inputs, since those components are handed to the
    subsystems.


    **Raises:**
    > ValueError: If any parameter is outside the allowed range.  

??? abstract "createSubSystems(self, id_list: List[str], level_list: List[int], neighborid_list: List[List[str]], analysis_list: List[[AnalysisInterface](../../subsystem/optimization/AnalysisInterface.md#analysisinterface)], localobjective_list: List[[LocalObjectiveInterface](../../subsystem/optimization/designproblem/LocalObjectiveInterface.md#localobjectiveinterface)], localconstraints_list: List[[LocalConstraintsInterface](../../subsystem/optimization/designproblem/LocalConstraintsInterface.md#localconstraintsinterface)], optimization_list: List[[OptimizationInterface](../../subsystem/optimization/OptimizationInterface.md#optimizationinterface)]) → List[[LocalSubSystemConsensusALC](../../subsystem/LocalSubSystemConsensusALC.md#localsubsystemconsensusalc)]"
    Create subsystems for consensus-based augmented Lagrangian coordination.


    **Args:**
    > id_list: List of unique identifiers for each subsystem.  
    > level_list: List of hierarchy levels for each subsystem.  
    > neighborid_list: List of neighbor subsystem IDs for each subsystem.  
    > analysis_list: List of analysis objects for each subsystem.  
    > localobjective_list: List of local objective functions for each subsystem.  
    > localconstraints_list: List of local constraints for each subsystem.  
    > optimization_list: List of optimization objects for each subsystem.  


    **Returns:**
    > List of initialized LocalSubSystemConsensusALC objects.  

??? abstract "createControllerSubSystem(self, subsystemsIn: List[[LocalSubSystemConsensusALC](../../subsystem/LocalSubSystemConsensusALC.md#localsubsystemconsensusalc)]) → [SubSystemInterface](../../subsystem/SubSystemInterface.md#subsysteminterface) | None"
    Create a controller subsystem for coordinating local subsystems.


    **Args:**
    > subsystemsIn: List of local subsystems to be coordinated.  


    **Returns:**
    > None, as Consensus ALC operates without a central controller.  

??? abstract "createMiddleLevel(self, idparent: str, idchild: str, multiprocessing_lock: object) → [MiddleLevelDataStorageConsensusALC](../../middlelevel/consensus_alc/MiddleLevelDataStorageConsensusALC.md#middleleveldatastorageconsensusalc)"
    Create a middle level data storage for coupling between subsystems.


    **Args:**
    > idparent: Identifier of the parent subsystem.  
    > idchild: Identifier of the child subsystem.  
    > multiprocessing_lock: Optional lock for thread-safe access in multiprocessing.  


    **Returns:**
    > MiddleLevelDataStorage instance for managing coupling data.  

??? abstract "createControllerMiddleLevel(self, idparent: str, idchild: str, local_neighbors_list: List[str], multiprocessing_lock: object) → [MiddleLevelDataStorageConsensusALC](../../middlelevel/consensus_alc/MiddleLevelDataStorageConsensusALC.md#middleleveldatastorageconsensusalc) | None"
    Create middle level between controller and local subsystem.


    **Args:**
    > idparent: Identifier of the parent (controller) subsystem.  
    > idchild: Identifier of the child subsystem.  
    > local_neighbors_list: List of neighbor IDs for the local subsystem (unused).  
    > multiprocessing_lock: Optional lock for thread-safe access in multiprocessing.  


    **Returns:**
    > None, as Consensus ALC operates without a central controller.  

??? abstract "centralized_prepare_updateCouplingParameters(self, subsystemsIn: List[[LocalSubSystemConsensusALC](../../subsystem/LocalSubSystemConsensusALC.md#localsubsystemconsensusalc)]) → None"
    Prepare centralized update of coupling parameters for all subsystems.

    For Consensus ALC, no centralized operation is required.


    **Args:**
    > subsystemsIn: List of subsystems to prepare coupling parameters for.  

??? abstract "print_beginning_of_centralized_prepare_updateCouplingParameters(self) → None"
    Nothing to print.

