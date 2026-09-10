# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Coordinator module for distributed design optimization.

This module provides the main Coordinator class that orchestrates multi-level
distributed design optimization. It manages the coordination between subsystems,
handles inner and outer loop iterations, convergence checks, and history tracking.

Example:
    >>> from Distributed_Design_Optimizer.coordination import Coordinator
    >>> coordinator = Coordinator(subsystems, inputfile)
    >>> coordinator.run()
"""

import gc
import traceback
from collections import deque
from typing import List, Deque
import os
import copy
import time
import dill
from Distributed_Design_Optimizer.coordination import InputFileInterface, CustomManager
# Register all MiddleLevelDataStorage subclasses with the CustomManager
CustomManager.register_all_data_storages()
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print, ddo_print_border
from Distributed_Design_Optimizer.middlelevel import MiddleLevelDataStorageInterface, CreateMiddleLevels
from Distributed_Design_Optimizer.coordination.innerloop_iterationscheme import IterationSchemeInterface
from Distributed_Design_Optimizer.coordination.convergence import Centralized_ConvergenceIndicator_Innerloop_Interface, Centralized_ConvergenceIndicator_Outerloop_Interface
from Distributed_Design_Optimizer.subsystem import SubSystemInterface, LocalSubSystemBasis
from Distributed_Design_Optimizer.coordination.CoordinatorHistoryEntry import CoordinatorHistoryEntry
from Distributed_Design_Optimizer.postprocess import (GraphInit,
                                                      ResidualComputer,
                                                      CentralityComputer,
                                                      PerformanceMetrics,
                                                      CompromiseComputer,
                                                      InConsistencyOscillationComputer,
                                                      ClusterComputer,
                                                      CouplingStrengthComputer
                                                      )

class Coordinator:
    """Coordinator for multi-level distributed design optimization.
    
    This class orchestrates the coordination between subsystems in a hierarchical
    optimization problem. It manages the inner and outer loop iterations, convergence
    checks, and history tracking.
    
    Attributes:
        _inputfile: The input file configuration interface.
        _convouterloop: Flag indicating outer loop convergence.
        _outerloop_itr: Current outer loop iteration counter.
        _innerloop_itr: Current inner loop iteration counter.
        _subsystems: List of subsystem interfaces representing the optimization structure.
        _middlelevels: List of middle level data storage interfaces.
    """

    _DDO_PRINT_LABEL_WIDTH: int = 36

    def __init__(self,
                 subsystemsIn: List[SubSystemInterface],
                 inputfile: InputFileInterface) -> None:
        """Initialize the Coordinator.
        
        Args:
            subsystemsIn: List of subsystem interfaces to be coordinated.
            inputfile: Input file interface containing coordination configuration.
        """
        
        controllersubsystem: SubSystemInterface | None = inputfile.get_CoordinationMethod().createControllerSubSystem(subsystemsIn)  # if required by coordintion approach
        
        # beartype enforces the return type (ControllerSubSystemBasis | None) at runtime,
        # so only the None vs. not-None distinction needs to be handled here.
        if controllersubsystem is None:
            subsystems: List[SubSystemInterface] = subsystemsIn
        else:
            subsystems: List[SubSystemInterface] = subsystemsIn + [controllersubsystem]
            
            # Update subsystems according to controller
            for subsystem in subsystems:
                # Controller is added to the local subsystems
                if isinstance(subsystem, LocalSubSystemBasis):
                    # Add controller to the local subsystems and update local subsystems
                    subsystem.append_Controller()
        
        self._subsystems: List[SubSystemInterface] = subsystems
            
        self._inputfile: InputFileInterface = inputfile
        
        self._outerloop_itr: int = 0
        self._innerloop_itr: int = 0
        self._innerloop_itr_runtime: float | None = None
        self._innerloop_itr_numberofdesignvariableevaluations: int | None = None
        
        self._manager: CustomManager = CustomManager()
        self._manager.start()
        
        self._middlelevels: List[MiddleLevelDataStorageInterface] = CreateMiddleLevels.createMiddleLevels(self._subsystems, self._manager, self._inputfile.get_CoordinationMethod())
        
        self._historyfolderpath: str = self._inputfile.get_HistoryFolderPath()
        
        for subsystem in self._subsystems:
            subsystem.set_MiddleLevels(self._middlelevels)
            subsystem.set_Name(self._inputfile.get_Name())
            subsystem.set_HistoryFolderPath(self._historyfolderpath)
        
        self._iterationscheme: IterationSchemeInterface = self._inputfile.get_CoordinationMethod().get_IterationScheme()                
        self._centralized_convergenceindicator_innerloop: Centralized_ConvergenceIndicator_Innerloop_Interface = \
            self._inputfile.get_CoordinationMethod().get_Convergence_Indicator_Innerloop().createCentralizedConvergenceIndicator()
        self._centralized_convergenceindicator_outerloop: Centralized_ConvergenceIndicator_Outerloop_Interface = \
            self._inputfile.get_CoordinationMethod().get_Convergence_Indicator_Outerloop().createCentralizedConvergenceIndicator()
        self._coordinatorhistory: Deque[CoordinatorHistoryEntry] = deque()
        
        self._graphinit = GraphInit()
        self._graphinit.set_MasterGraph(self._subsystems)
        self._mastergraph = self._graphinit.get_graph()
        
        self._residualscomputer: ResidualComputer = ResidualComputer(self._graphinit, self._middlelevels, self._subsystems, self._iterationscheme)
        self._centralitycomputer: CentralityComputer = CentralityComputer(self._graphinit, self._subsystems)
        self._compromisecomputer: CompromiseComputer = CompromiseComputer(self._graphinit, self._subsystems, self._middlelevels)
        self._inconsistencyoscillationcomputer: InConsistencyOscillationComputer = InConsistencyOscillationComputer(self._graphinit, self._subsystems)
        self._clustercomputer: ClusterComputer = ClusterComputer(self._graphinit, self._subsystems)
        self._couplingstrengthcomputer: CouplingStrengthComputer = CouplingStrengthComputer(self._graphinit, self._subsystems)
        self._performancemetric: PerformanceMetrics = PerformanceMetrics()
        
        self._maxinconsistencyvalue: float | None = None
        self._maxinconsistencyvaluesubsystemID: str | None = None
        self._maxratioofactiveconstraints: float | None = None
        self._maxratioofactiveconstraintssubsystemID: str | None = None   
        
    def run(self) -> None:
        """Run the distributed optimization coordination."""

        # print startup summary info to terminal
        self.print_startup_summary()

        try:
            self.initialize()

            # initialize outerloop iterator
            self._outerloop_itr = 0

            # this is intended for do-while loop
            self.outerloop_iteration()
            while self._centralized_convergenceindicator_outerloop.get_ConvOuterLoop() is False:
                self.outerloop_iteration()

            # TODO: Extend coupling strength computer to controller
            # after coordiantion outer loop is finished, compute coupling strength
            # self._couplingstrengthcomputer.execute()
            # self._coordinatorhistory[-1]["CouplingStrength"]= copy.deepcopy(self._couplingstrengthcomputer.get_couplingstrength())
            # Update coordinator history and save
            # self.savecoordinatorhistory()
        finally:
            # Always shut down the manager process, even if an exception propagates,
            # to avoid leaking the multiprocessing manager.
            self._manager.shutdown()

        # print termination summary
        self.print_termination_summary()     

    def initialize(self) -> None:
        """Initialize all subsystems by evaluating responses, constraints, and coupling parameters.

        Performs three rounds of middle-level data exchange to ensure all coupling
        parameters are fully initialized across the subsystem hierarchy.
        """
        self.print_beginning_of_initialization()
        
        # Evaluate total constraints and objective to initialize the subsystem
        for subsystem in self._subsystems:
            if isinstance(subsystem, LocalSubSystemBasis):
                subsystem.evaluate_Responses_and_LocalObjective()
                subsystem.evaluateTotalConstraint()
                
        # Update optimdata objects according to initialization
        for subsystem in self._subsystems:
            subsystem.updateOptimdatafromSubsystem()

        # Initialized independent coupling parameters and fill the middlelevels
        for subsystem in self._subsystems:
            subsystem.initializeCouplingParameters_before_CopyToMiddleLevel()
            subsystem.postprocess_Optimization()
            subsystem.CopyToMiddleLevel()
        
        # Copy from middlelevels and initialize further coupling parameters of the subsystems
        for subsystem in self._subsystems:
            subsystem.CopyFromMiddleLevel()
            subsystem.initializeCouplingParameters_after_CopyFromMiddleLevel()
            subsystem.CopyToMiddleLevel()
            
        # TODO: Change to new method for third round, change names (add to SubSystemInterface)
        # Copy from middlelevels and initialize further coupling parameters of the subsystems
        for subsystem in self._subsystems:
            subsystem.CopyFromMiddleLevel()
            subsystem.initializeCouplingParameters_after_Second_CopyFromMiddleLevel()
            subsystem.CopyToMiddleLevel()
        
        self.print_end_of_initialization()
            
    def outerloop_iteration(self) -> None:
        """Run the inner and outer loop during the coordination."""

        # print information beginning of outerloop iteration
        self.print_beginning_of_outerloop_iteration()
        
        self._innerloop_itr: int = 0
        self._innerloop_itr_runtime: float | None = None
        self._innerloop_itr_numberofdesignvariableevaluations: int | None = None
        
        # this is intended for do-while loop
        self.innerloop_iteration()
        while self._centralized_convergenceindicator_innerloop.get_ConvInnerLoop() is False:
            self.innerloop_iteration()
                
        # Decentralized preparation operation necessary for updating coupling parameters, including controller
        self.print_beginning_of_run_prepare_updateCouplingParameters_job()
        for subsystem in self._subsystems:
            subsystem.run_prepare_updateCouplingParameters_job()
        self.print_finished_run_prepare_updateCouplingParameters_job()
            
        # Centralized operation necessary for updating coupling parameters, including controller
        self._inputfile.get_CoordinationMethod().print_beginning_of_centralized_prepare_updateCouplingParameters()
        self._inputfile.get_CoordinationMethod().centralized_prepare_updateCouplingParameters(self._subsystems)
        
        # Decentralized operation necessary for updating coupling parameters, including controller
        self.print_beginning_of_run_updateCouplingParameters_outerloop_job()
        for subsystem in self._subsystems:
            subsystem.run_updateCouplingParameters_outerLoop_job()
        self.print_finished_run_updateCouplingParameters_outerloop_job()

        # Determine outerloop convergence
        self._centralized_convergenceindicator_outerloop.print_beginning_of_centralized_convergenceindicator_outerloop_evaluation()
        self._centralized_convergenceindicator_outerloop.evaluate(self._subsystems)
        self._centralized_convergenceindicator_outerloop.print_end_of_centralized_convergenceindicator_outerloop_evaluation(self._subsystems)
               
        # print information end of outerloop iteration
        self.print_end_of_outerloop_iteration()
        
        self._outerloop_itr = self._outerloop_itr + 1        

        # try to free some unused resources.
        gc.collect()
            
    def innerloop_iteration(self) -> None:
        """Execute a single inner loop iteration of the optimization process."""
        # print information beginning of innerloop iteration
        self.print_beginning_of_innerloop_iteration()
        
        # run the subsystem optimization jobs via multiprocessing
        self.run_innerloop_jobs()
        
        # Decentralized operation step necessary for updating coupling parameters,
        # including the controller subsystem
        self.print_beginning_of_run_updateCouplingParameters_innerloop_job()
        for subsystem in self._subsystems:
            subsystem.run_updateCouplingParameters_innerLoop_job()
        self.print_finished_run_updateCouplingParameters_innerloop_job()
        
        # Determine innerloop convergence
        # Centralized operation to determine innerloop convergence
        self._centralized_convergenceindicator_innerloop.print_beginning_of_centralized_convergenceindicator_innerloop_evaluation()
        self._centralized_convergenceindicator_innerloop.evaluate(self._subsystems)
        self._centralized_convergenceindicator_innerloop.print_end_of_centralized_convergenceindicator_innerloop_evaluation(self._subsystems)

        # update subsystems info
        for subsystem in self._subsystems:
            subsystem.set_OuterLoop_Itr(self._outerloop_itr)
            subsystem.set_InnerLoop_Itr(self._innerloop_itr)
            subsystem.set_InnerLoop_Itr_Runtime(self._innerloop_itr_runtime)
            subsystem.set_InnerLoop_Itr_NumberOfDesignVariableEvaluations(self._innerloop_itr_numberofdesignvariableevaluations)
            if isinstance(subsystem, LocalSubSystemBasis):
                subsystem.evaluate_Inconsistencies()      
        
        # compute the primal and dual residuals
        # self._residualscomputer.compute_all_primal_residuals()
        # self._residualscomputer.compute_all_dual_residuals(self._centralized_convergenceindicator_innerloop.get_ConvInnerLoop())
        # compute the centrality measures
        # self._centralitycomputer.compute_CentralityMeasures()
        # compute the Compromise Measures for the subsystems
        # self._compromisecomputer.compute_all_compromises()
        # preprocess the graph and perform clustering
        # self._clustercomputer.perform_spectral_clustering()        
        # update coordinator metrics
        self._performancemetric.update(self._centralized_convergenceindicator_innerloop.get_ConvInnerLoop(), self._subsystems)
        # compute the inconsistency oscillations
        # self.compute_InConsistencyOscillations()        
        # get the max inconsistency of the systems
        self.evaluate_MaxInconsistency()
        # get max ratio of active constraints
        self.evaluate_MaxRatioOfActiveConstraints()
        
        # update and save subsystems history
        self.print_beginning_of_appendto_and_saving_subsystem_history()
        for subsystem in self._subsystems:
            subsystem.appendtohistory()
            subsystem.savesubsystemhistory()
        self.print_finished_appendto_and_saving_subsystem_history()
        
        # Update coordinator history and save
        self.print_beginning_of_appendto_and_saving_coordinator_history()
        self.appendtohistory()
        self.savecoordinatorhistory()
        self.print_finished_appendto_and_saving_coordinator_history()
        
        # print information end of innerloop iteration
        self.print_end_of_innerloop_iteration()
        
        # increase the innerloop iterator
        self._innerloop_itr = self._innerloop_itr + 1
                    
    def run_innerloop_jobs(self) -> None:
        """Run the subsystem optimization jobs for one innerloop iteration via multiprocessing.

        Sets the current iterators on all subsystems, swaps in managed middlelevels for
        the multiprocessing run, restores the originals afterwards, updates each original
        subsystem with its executed state, and stores the iteration accounting in
        ``self._innerloop_itr_runtime`` and
        ``self._innerloop_itr_numberofdesignvariableevaluations``.
        """
        try:
            innerloop_startime = time.time()
            
            # update the subsystem's inner and outerloop iterators to the current ones
            # Only needed for accounting of iteration numbers
            for subsystem in self._subsystems:
                subsystem.set_OuterLoop_Itr(self._outerloop_itr)
                subsystem.set_InnerLoop_Itr(self._innerloop_itr)
                
            managed_middlelevels = CreateMiddleLevels.createManagedMiddleLevels(self._middlelevels,
                                                                                self._manager)
            # Save original middlelevels for later restoration
            original_middlelevels = self._middlelevels
            
            # Assign to each subsystem the managed_middlelevels
            for subsystem in self._subsystems:
                subsystem.set_MiddleLevels(managed_middlelevels)
                
            # Execute the subsystems with specified iterationscheme order
            self._iterationscheme.print_beginning_of_run_innerloop_jobs_multiprocessing()
            all_executed_subsystems, all_subsystem_indices = self._iterationscheme.run_innerloop_jobs_multiprocessing(self._subsystems)
            
            # After all levels are processed:
            # Restore original middlelevels memory addresses
            for idx in all_subsystem_indices:
                self._subsystems[idx].set_MiddleLevels(original_middlelevels)
                
            # Update original subsystems with data from executed subsystems
            for executed_subsystem, idx in zip(all_executed_subsystems, all_subsystem_indices):
                self._subsystems[idx].update_state(executed_subsystem)
            
            innerloop_finishtime = time.time()
            self._innerloop_itr_runtime = innerloop_finishtime - innerloop_startime
            self._innerloop_itr_numberofdesignvariableevaluations = 0
            for subsystem in self._subsystems:
                numberofdesignvariableevaluations = subsystem.get_OptimData().get_Optimization_NumberOfDesignVariableEvaluations()
                if numberofdesignvariableevaluations is not None:
                    self._innerloop_itr_numberofdesignvariableevaluations += numberofdesignvariableevaluations
            
        except Exception as e:
            ddo_print("Exception while running innerloop jobs via multiprocessing: ")
            ddo_print(str(e))
            traceback.print_exc()
            # Propagate the exception so the caller (run) can react and the manager
            # is shut down via the try/finally there, instead of killing the interpreter.
            raise
                    
    def appendtohistory(self) -> None:
        """Append current iteration state to the coordinator history.
        """
        # subsystem_details = {}
        # # MOVE BOOLEAN BEFORE FUNCTION IS CALLED
        # subsystem_details_append = True
        # if subsystem_details_append:
        #     for i in range(len(self._subsystems)):
        #         subsystem: SubSystemInterface = self._subsystems[i]
        #         # Check if subsystem is local subsystem -> TODO: Should the controller subsystem, if existing, be included in coordinatorhistory?
        #         if isinstance(subsystem, LocalSubSystemBasis):   
                    
        #             # Since nonexisting local constraints are none, 
        #             # assign correct dimensions
        #             dimension_localequalityconstraints: int = 0
        #             if subsystem.get_EqualityLocalConstraintsValue() is not None:
        #                 dimension_localequalityconstraints = len(subsystem.get_EqualityLocalConstraintsValue())
                        
        #             dimension_localinequalityconstraints: int = 0         
        #             if subsystem.get_InequalityLocalConstraintsValue() is not None:
        #                 dimension_localinequalityconstraints = len(subsystem.get_InequalityLocalConstraintsValue())
                        
        #             subsystem_details[subsystem.get_SUBSYSTEMID()] = {'Level' : subsystem.get_SubsystemLevel(),
        #                                                               'Design Variables Dimension' : len(subsystem.get_DesignVariables()),
        #                                                               'Inequality Constraint Dimensions' : dimension_localinequalityconstraints,
        #                                                               'Equality Constraint Dimension' : dimension_localequalityconstraints
        #                                                               }
        #         subsystem_details_append = False
                
        self._coordinatorhistory.append(CoordinatorHistoryEntry(outerloop_itr=self._outerloop_itr,
                                                                innerloop_itr=self._innerloop_itr,
                                                                innerloop_itr_runtime=self._innerloop_itr_runtime,
                                                                innerloop_itr_numberofdesignvariableevaluations=self._innerloop_itr_numberofdesignvariableevaluations,
                                                                maxinconsistencyvalue=self.get_MaxInconsistencyValue(),
                                                                maxinconsistencyID=self.get_MaxInconsistencyValueSubsystemID(),
                                                                maxratioofactiveconstraints=self.get_MaxRatioOfActiveConstraints(),
                                                                maxratioofactiveconstraintsID=self.get_MaxRatioOfActiveConstraintsSubsystemID(),
                                                                performancemetrics=copy.deepcopy(self._performancemetric),
                                                                centralitymeasures=copy.deepcopy(self._centralitycomputer.get_centrality_summary()),
                                                                compromisemeasures=copy.deepcopy(self._compromisecomputer.get_compromise_summary()),
                                                                inconsistencyoscillationindex=copy.deepcopy(self._inconsistencyoscillationcomputer.get_InConsistencyOscillationIndex_summary()),
                                                                clusteranalysis=copy.deepcopy(self._clustercomputer.get_cluster_summary()),
                                                                couplingstrength=copy.deepcopy(self._couplingstrengthcomputer.get_couplingstrength()),
                                                                mastergraph=copy.deepcopy(self._mastergraph),
                                                                ))
        
    def savecoordinatorhistory(self) -> None:
        """Save the coordinator history to a dill file.

        The use-case name is read from the input file (via get_Name). The
        target folder is the use-case's historyfiles folder (stored as
        self._historyfolderpath during initialization).
        """
        filename: str = f"historyfile_{self._inputfile.get_Name()}_coordinator.dill"

        # Create the folder if it doesn't exist
        os.makedirs(self._historyfolderpath, exist_ok=True)
        history_file_path: str = os.path.join(self._historyfolderpath, filename)

        # Serialize the object to a binary format
        with open(history_file_path, 'wb') as file:
            dill.dump(self._coordinatorhistory, file)
    
    def get_CoordinatorHistory(self) -> Deque[CoordinatorHistoryEntry]:
        """Return the coordinator history.
        
        Returns:
            The deque containing the history of coordinator states.
        """
        # No copy.copy() used - Deque is a class object returned by reference intentionally.
        # This allows the caller to interact with the actual object. If isolation is needed,
        # the caller should explicitly copy.
        return self._coordinatorhistory
    
    def evaluate_MaxInconsistency(self) -> None:        
        """Evaluate the max inconsistency value of all the subsystems."""       
        maxinconsistencyValue = 0.0
        maxinconsistencysubsystemID = None
        
        for subsystem in self._subsystems:
            if isinstance(subsystem, LocalSubSystemBasis):  # inconsistencies are only defined between pairs of LocalSubSystem objects, not ControllerSubSystemBasis objects
                if subsystem.get_maxInconsistencyValue() is not None:
                    if subsystem.get_maxInconsistencyValue() > maxinconsistencyValue:
                        maxinconsistencyValue = subsystem.get_maxInconsistencyValue()
                        maxinconsistencysubsystemID = subsystem.get_MaxInconsistencyCoupledSubsystemID()
        
        self._maxinconsistencyvalue = maxinconsistencyValue
        self._maxinconsistencyvaluesubsystemID = maxinconsistencysubsystemID
        
    def get_MaxInconsistencyValue(self) -> float:
        """Return the maximum inconsistency value.
        
        Returns:
            The maximum inconsistency value across all subsystems.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding,
        # so modifications to that variable cannot affect this class's attribute.
        return self._maxinconsistencyvalue
    
    def get_MaxInconsistencyValueSubsystemID(self) -> str:
        """Return the subsystem ID with maximum inconsistency.
        
        Returns:
            The subsystem ID with maximum inconsistency, or None if not set.
        """
        # No copy.copy() needed - str is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding,
        # so modifications to that variable cannot affect this class's attribute.
        return self._maxinconsistencyvaluesubsystemID
    
    def evaluate_MaxRatioOfActiveConstraints(self) -> None:
        """Compute the max ratio of active constraints of the entire system."""
        max_ratioofconstraintvalues = 0.0
        max_ratioofconstraintvaluessubsystemID = None
        for subsystem in self._subsystems:
            if isinstance(subsystem, LocalSubSystemBasis):  # ratio of active constraints is only defined for LocalSubSystem objects, not ControllerSubSystemBasis objects
                subsystem_ratioofactiveconstraint = subsystem.get_OptimData().get_RatioofActiveBoundsandConstraints()
                if subsystem_ratioofactiveconstraint is not None:
                    if subsystem_ratioofactiveconstraint > max_ratioofconstraintvalues:
                        max_ratioofconstraintvalues = subsystem_ratioofactiveconstraint
                        max_ratioofconstraintvaluessubsystemID = subsystem.get_SUBSYSTEMID()
        
        self._maxratioofactiveconstraints = max_ratioofconstraintvalues
        self._maxratioofactiveconstraintssubsystemID = max_ratioofconstraintvaluessubsystemID
        
    def compute_InConsistencyOscillations(self) -> None:
        """Compute the oscillation behaviour of the inconsistencies using wavelet transforms."""
        primal_history = self.copy_PrimalResiduals_Previous_outer_or_innerloop_itr(k=self._inconsistencyoscillationcomputer.get_Horizon())
        self._inconsistencyoscillationcomputer.compute_wavelet_transforms(primal_history)        
        
    def get_MaxRatioOfActiveConstraints(self) -> float:
        """Return the maximum ratio of active constraints.

        Returns:
            The maximum ratio of active constraints across all subsystems.
        """
        # No copy.copy() needed - float is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding,
        # so modifications to that variable cannot affect this class's attribute.
        return self._maxratioofactiveconstraints
    
    def get_MaxRatioOfActiveConstraintsSubsystemID(self) -> str:
        """Return the subsystem ID with the maximum ratio of active constraints.

        Returns:
            The subsystem ID with the maximum ratio of active constraints.
        """
        # No copy.copy() needed - str is a primitive/immutable type.
        # Assigning this return value to a variable in the caller creates a new binding,
        # so modifications to that variable cannot affect this class's attribute.
        return self._maxratioofactiveconstraintssubsystemID
            
    def copy_PrimalResiduals_Previous_outer_or_innerloop_itr(self, k: int) -> List[CoordinatorHistoryEntry] | None:
        """
        Retrieve previous k entries from the coordinator history.
    
        Args:
            k: Number of previous entries to retrieve
            
        Returns:
            List or None: List of previous history entries (most recent first)
                        or None if not enough history entries available
        """
        recent_entries = None
        if len(self._coordinatorhistory) >= k:           
    
            # Get the k most recent entries from the history
            recent_entries = []
            for i in range(len(self._coordinatorhistory) - 1, len(self._coordinatorhistory) - k - 1, -1):
                recent_entries.append(self._coordinatorhistory[i])
            
        return recent_entries
    
    def print_banner(self, message: str) -> None:
        """Print a bordered banner with a single message line.

        Args:
            message: The text to display inside the banner.
        """
        ddo_print_border()
        ddo_print(f"{type(self).__name__}: {message}")
        ddo_print_border()
        ddo_print("")

    def print_all_scaler_bound_violations(self) -> None:
        """Collect and print scaler bound violations across all subsystems."""
        # Collect violations once to avoid iterating subsystems twice
        subsystems_with_violations: list = []
        for subsystem in self._subsystems:
            if isinstance(subsystem, LocalSubSystemBasis):
                if subsystem.get_scaler_bound_violations():
                    subsystems_with_violations.append(subsystem)
        if subsystems_with_violations:
            ddo_print("Scaler Bound Violations:")
            for subsystem in subsystems_with_violations:
                if isinstance(subsystem, LocalSubSystemBasis):
                    subsystem.print_scaler_bound_violations()

    def print_all_scaler_bound_utilization_report(self) -> None:
        """Print a full scaler bound utilization report for all subsystems."""
        ddo_print("Scaler Bound Utilization Report:")
        for subsystem in self._subsystems:
            if isinstance(subsystem, LocalSubSystemBasis):
                subsystem.print_scaler_bound_utilization_report()

    def print_startup_summary(self) -> None:
        """Print a startup summary banner to the console.

        Displays information about the optimization run including use-case name,
        coordination method, and iteration scheme.
        """
        ddo_print_border()
        ddo_print("")
        ddo_print("                  Running DistributedDesignOptimizer               ")
        ddo_print("")
        self._inputfile.print_startup_summary()
        self._inputfile.get_CoordinationMethod().print_startup_summary()
        ddo_print("")
        ddo_print("Subsystems:")
        for subsystem in self._subsystems:
            subsystem.print_startup_summary()
        ddo_print_border()
        ddo_print("")

    def print_beginning_of_initialization(self) -> None:
        """Print a banner indicating the start of initialization."""
        self.print_banner("Starting Initialization ...")

    def print_end_of_initialization(self) -> None:
        """Print a banner indicating the end of initialization."""
        self.print_banner("Finished Initialization")

    def print_beginning_of_run_prepare_updateCouplingParameters_job(self) -> None:
        """Print a banner before preparing the coupling parameter update step."""
        self.print_banner("Starting Prepare Update of CouplingParameters ...")

    def print_beginning_of_run_updateCouplingParameters_outerloop_job(self) -> None:
        """Print a banner before updating coupling parameters in the outer loop."""
        self.print_banner("Starting Update of CouplingParameters in Outerloop ...")

    def print_beginning_of_outerloop_iteration(self) -> None:
        """Print a banner indicating the start of an outer loop iteration."""
        self.print_banner(f"Starting Outerloop Iteration Nr. {self._outerloop_itr} ...")

    def print_beginning_of_innerloop_iteration(self) -> None:
        """Print a banner indicating the start of an inner loop iteration."""
        self.print_banner(f"Starting Innerloop Iteration Nr. {self._innerloop_itr} (Outerloop Nr. {self._outerloop_itr}) ...")

    def print_beginning_of_run_updateCouplingParameters_innerloop_job(self) -> None:
        """Print a banner before updating coupling parameters in the inner loop."""
        self.print_banner("Starting Update of CouplingParameters in InnerLoop ...")

    def print_finished_run_prepare_updateCouplingParameters_job(self) -> None:
        """Print a banner after preparing the coupling parameter update step."""
        self.print_banner("Finished Prepare Update of CouplingParameters")

    def print_finished_run_updateCouplingParameters_outerloop_job(self) -> None:
        """Print a banner after updating coupling parameters in the outer loop."""
        self.print_banner("Finished Update of CouplingParameters in Outerloop")

    def print_finished_run_updateCouplingParameters_innerloop_job(self) -> None:
        """Print a banner after updating coupling parameters in the inner loop."""
        self.print_banner("Finished Update of CouplingParameters in InnerLoop")

    def print_beginning_of_appendto_and_saving_subsystem_history(self) -> None:
        """Print a banner before appending to and saving each subsystem history."""
        self.print_banner("Appending important information to each subsystem history and saving into historyfiles/*.dill ...")

    def print_beginning_of_appendto_and_saving_coordinator_history(self) -> None:
        """Print a banner before appending to and saving the coordinator history."""
        self.print_banner("Appending important information to coordinator history and saving into historyfiles/*.dill ...")

    def print_finished_appendto_and_saving_subsystem_history(self) -> None:
        """Print a banner after appending to and saving each subsystem history."""
        self.print_banner("Finished appending and saving each subsystem history")

    def print_finished_appendto_and_saving_coordinator_history(self) -> None:
        """Print a banner after appending to and saving the coordinator history."""
        self.print_banner("Finished appending and saving coordinator history")

    def print_end_of_innerloop_iteration(self) -> None:
        """Print a summary at the end of an inner loop iteration.

        Displays detailed results for each subsystem including solver information,
        design variables, physical responses, objective values, and inconsistencies.
        """
        ddo_print_border()
        ddo_print(f"{type(self).__name__}: Finished Innerloop Iteration Nr. {self._innerloop_itr} (Outerloop Nr. {self._outerloop_itr}) after {self._innerloop_itr_runtime:.0f} sec. and {self._innerloop_itr_numberofdesignvariableevaluations} design variables evaluations")
        ddo_print("")

        for subsystem in self._subsystems:
            subsystem.print_end_of_innerloop_iteration()

        self._performancemetric.print_end_of_innerloop_iteration()
        ddo_print("")
        ddo_print(f"{type(self).__name__}:")
        ddo_print(f"   {'Max Inconsistency Value:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self._maxinconsistencyvalue} (SubSystem {self._maxinconsistencyvaluesubsystemID})")
        ddo_print(f"   {'Max Ratio Active Constraints:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self._maxratioofactiveconstraints} (SubSystem {self._maxratioofactiveconstraintssubsystemID})")
        self.print_all_scaler_bound_violations()
        self._centralized_convergenceindicator_innerloop.print_convergence_result()
        ddo_print_border()
        ddo_print("")

    def print_end_of_outerloop_iteration(self) -> None:
        """Print a summary at the end of an outer loop iteration.

        Displays the outer loop iteration number and convergence status.
        """
        cumulative_runtime = sum(
            entry.get_InnerLoop_Itr_Runtime() for entry in self._coordinatorhistory
            if entry.get_OuterLoop_Itr() == self._outerloop_itr
        )
        cumulative_dv_evals = sum(
            entry.get_InnerLoop_Itr_NumberOfDesignVariableEvaluations() for entry in self._coordinatorhistory
            if entry.get_OuterLoop_Itr() == self._outerloop_itr
        )
        ddo_print_border()
        ddo_print(f"{type(self).__name__}: Finished Outerloop Iteration Nr. {self._outerloop_itr} after {self._innerloop_itr} innerloop iterations")
        ddo_print(f"   {'Cumulative Runtime:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {cumulative_runtime:.0f} sec.")
        ddo_print(f"   {'Cumulative DV Evaluations:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {cumulative_dv_evals}")
        ddo_print(f"   {'Max Inconsistency Value:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self._maxinconsistencyvalue} (SubSystem {self._maxinconsistencyvaluesubsystemID})")
        self.print_all_scaler_bound_violations()
        self._centralized_convergenceindicator_outerloop.print_convergence_result()
        ddo_print_border()
        ddo_print("")

    def print_termination_summary(self) -> None:
        """Print a termination summary banner to the console.

        Displays final results of the optimization run including iteration counts,
        maximum inconsistency values, and performance metrics.
        """
        ddo_print_border()
        ddo_print("")
        ddo_print("                   Finished Running DistributedDesignOptimizer             ")
        ddo_print("")
        self._inputfile.print_startup_summary()
        ddo_print(f"{'Total outerloop iterations:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self._outerloop_itr}")
        ddo_print(f"{'Total inner and outerloop iterations:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {len(self._coordinatorhistory)}")
        ddo_print("")
        self._performancemetric.print_termination_summary()
        ddo_print("")

        for subsystem in self._subsystems:
            subsystem.print_termination_summary()

        ddo_print(f"   {'Max Inconsistency Value:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self._maxinconsistencyvalue} (SubSystem {self._maxinconsistencyvaluesubsystemID})")
        self.print_all_scaler_bound_utilization_report()
        self._inputfile.get_CoordinationMethod().print_termination_summary()
        ddo_print_border()
        ddo_print("")

