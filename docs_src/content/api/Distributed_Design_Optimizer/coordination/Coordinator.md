---
title: Coordinator
---

← Back to [coordination](index.md)

# Coordinator

**Source:** [Distributed_Design_Optimizer\coordination\Coordinator.py](Coordinator_source.md)

Coordinator module for distributed design optimization.

This module provides the main Coordinator class that orchestrates multi-level
distributed design optimization. It manages the coordination between subsystems,
handles inner and outer loop iterations, convergence checks, and history tracking.


**Example:**
> >>> from Distributed_Design_Optimizer.coordination import Coordinator  
> >>> coordinator = Coordinator(subsystems, inputfile)  
> >>> coordinator.run()

## Classes

### Coordinator

> Coordinator for multi-level distributed design optimization.

> This class orchestrates the coordination between subsystems in a hierarchical
> optimization problem. It manages the inner and outer loop iterations, convergence
> checks, and history tracking.


> **Attributes:**
> > _inputfile: The input file configuration interface.  
> > _convouterloop: Flag indicating outer loop convergence.  
> > _outerloop_itr: Current outer loop iteration counter.  
> > _innerloop_itr: Current inner loop iteration counter.  
> > _subsystems: List of subsystem interfaces representing the optimization structure.  
> > _middlelevels: List of middle level data storage interfaces.

#### Methods

??? abstract "__init__(self, subsystemsIn: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)], inputfile: [InputFileInterface](InputFileInterface.md#inputfileinterface)) → None"
    Initialize the Coordinator.


    **Args:**
    > subsystemsIn: List of subsystem interfaces to be coordinated.  
    > inputfile: Input file interface containing coordination configuration.  

??? abstract "run(self) → None"
    Run the distributed optimization coordination.

??? abstract "initialize(self) → None"
    Initialize all subsystems by evaluating responses, constraints, and coupling parameters.

    Performs three rounds of middle-level data exchange to ensure all coupling
    parameters are fully initialized across the subsystem hierarchy.

??? abstract "outerloop_iteration(self) → None"
    Run the inner and outer loop during the coordination.

??? abstract "innerloop_iteration(self) → None"
    Execute a single inner loop iteration of the optimization process.

??? abstract "run_innerloop_jobs(self) → None"
    Run the subsystem optimization jobs for one innerloop iteration via multiprocessing.

    Sets the current iterators on all subsystems, swaps in managed middlelevels for
    the multiprocessing run, restores the originals afterwards, updates each original
    subsystem with its executed state, and stores the iteration accounting in
    ``self._innerloop_itr_runtime`` and
    ``self._innerloop_itr_numberofdesignvariableevaluations``.

??? abstract "appendtohistory(self) → None"
    Append current iteration state to the coordinator history.


??? abstract "savecoordinatorhistory(self) → None"
    Save the coordinator history to a dill file.

    The use-case name is read from the input file (via get_Name). The
    target folder is the use-case's historyfiles folder (stored as
    self._historyfolderpath during initialization).

??? abstract "get_CoordinatorHistory(self) → Deque[[CoordinatorHistoryEntry](CoordinatorHistoryEntry.md#coordinatorhistoryentry)]"
    Return the coordinator history.


    **Returns:**
    > The deque containing the history of coordinator states.  

??? abstract "evaluate_MaxInconsistency(self) → None"
    Evaluate the max inconsistency value of all the subsystems.

??? abstract "get_MaxInconsistencyValue(self) → float"
    Return the maximum inconsistency value.


    **Returns:**
    > The maximum inconsistency value across all subsystems.  

??? abstract "get_MaxInconsistencyValueSubsystemID(self) → str"
    Return the subsystem ID with maximum inconsistency.


    **Returns:**
    > The subsystem ID with maximum inconsistency, or None if not set.  

??? abstract "evaluate_MaxRatioOfActiveConstraints(self) → None"
    Compute the max ratio of active constraints of the entire system.

??? abstract "compute_InConsistencyOscillations(self) → None"
    Compute the oscillation behaviour of the inconsistencies using wavelet transforms.

??? abstract "get_MaxRatioOfActiveConstraints(self) → float"
    Return the maximum ratio of active constraints.


    **Returns:**
    > The maximum ratio of active constraints across all subsystems.  

??? abstract "get_MaxRatioOfActiveConstraintsSubsystemID(self) → str"
    Return the subsystem ID with the maximum ratio of active constraints.


    **Returns:**
    > The subsystem ID with the maximum ratio of active constraints.  

??? abstract "copy_PrimalResiduals_Previous_outer_or_innerloop_itr(self, k: int) → List[[CoordinatorHistoryEntry](CoordinatorHistoryEntry.md#coordinatorhistoryentry)] | None"
    Retrieve previous k entries from the coordinator history.


    **Args:**
    > k: Number of previous entries to retrieve  


    **Returns:**
    > List or None: List of previous history entries (most recent first)  
    > or None if not enough history entries available  

??? abstract "print_banner(self, message: str) → None"
    Print a bordered banner with a single message line.


    **Args:**
    > message: The text to display inside the banner.  

??? abstract "print_all_scaler_bound_violations(self) → None"
    Collect and print scaler bound violations across all subsystems.

??? abstract "print_all_scaler_bound_utilization_report(self) → None"
    Print a full scaler bound utilization report for all subsystems.

??? abstract "print_startup_summary(self) → None"
    Print a startup summary banner to the console.

    Displays information about the optimization run including use-case name,
    coordination method, and iteration scheme.

??? abstract "print_beginning_of_initialization(self) → None"
    Print a banner indicating the start of initialization.

??? abstract "print_end_of_initialization(self) → None"
    Print a banner indicating the end of initialization.

??? abstract "print_beginning_of_run_prepare_updateCouplingParameters_job(self) → None"
    Print a banner before preparing the coupling parameter update step.

??? abstract "print_beginning_of_run_updateCouplingParameters_outerloop_job(self) → None"
    Print a banner before updating coupling parameters in the outer loop.

??? abstract "print_beginning_of_outerloop_iteration(self) → None"
    Print a banner indicating the start of an outer loop iteration.

??? abstract "print_beginning_of_innerloop_iteration(self) → None"
    Print a banner indicating the start of an inner loop iteration.

??? abstract "print_beginning_of_run_updateCouplingParameters_innerloop_job(self) → None"
    Print a banner before updating coupling parameters in the inner loop.

??? abstract "print_finished_run_prepare_updateCouplingParameters_job(self) → None"
    Print a banner after preparing the coupling parameter update step.

??? abstract "print_finished_run_updateCouplingParameters_outerloop_job(self) → None"
    Print a banner after updating coupling parameters in the outer loop.

??? abstract "print_finished_run_updateCouplingParameters_innerloop_job(self) → None"
    Print a banner after updating coupling parameters in the inner loop.

??? abstract "print_beginning_of_appendto_and_saving_subsystem_history(self) → None"
    Print a banner before appending to and saving each subsystem history.

??? abstract "print_beginning_of_appendto_and_saving_coordinator_history(self) → None"
    Print a banner before appending to and saving the coordinator history.

??? abstract "print_finished_appendto_and_saving_subsystem_history(self) → None"
    Print a banner after appending to and saving each subsystem history.

??? abstract "print_finished_appendto_and_saving_coordinator_history(self) → None"
    Print a banner after appending to and saving the coordinator history.

??? abstract "print_end_of_innerloop_iteration(self) → None"
    Print a summary at the end of an inner loop iteration.

    Displays detailed results for each subsystem including solver information,
    design variables, physical responses, objective values, and inconsistencies.

??? abstract "print_end_of_outerloop_iteration(self) → None"
    Print a summary at the end of an outer loop iteration.

    Displays the outer loop iteration number and convergence status.

??? abstract "print_termination_summary(self) → None"
    Print a termination summary banner to the console.

    Displays final results of the optimization run including iteration counts,
    maximum inconsistency values, and performance metrics.

