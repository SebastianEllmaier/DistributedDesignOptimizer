# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Performance metrics module.

This module provides functionality for computing performance metrics
in distributed optimization problems.
"""

from typing import List
import numpy as np
from Distributed_Design_Optimizer.subsystem import SubSystemInterface, LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.optimization.optimizerdata import OptimDataBasis
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print


class PerformanceMetrics:
    """Compute and store performance metrics for optimization convergence analysis."""

    _DDO_PRINT_LABEL_WIDTH: int = 42

    def __init__(self) -> None:
        """Initialize the PerformanceMetrics with default values."""
        self._referencevalues_initialized: bool = False
        
        self._globaldesignvariables: List[float] | None = None
        self._globaldesignvariablesunscaled: List[float] | None = None
        self._referenceglobaldesignvariables: List[float] | List[None] | None
        self._referenceglobaldesignvariablesunscaled: List[float] | List[None] | None
        self._globaldesignvariables_previousouterloop: List[float] | None = None
        self._globaldesignvariablesunscaled_previousouterloop: List[float] | None = None
        self._globaldesignvariables_previousinnerloop: List[float] | None = None
        self._globaldesignvariablesunscaled_previousinnerloop: List[float] | None = None
        
        self._globalobjectivefunctionvalue: float | None = None
        self._globalobjectivefunctionvalueunscaled: float | None = None
        self._referenceglobalobjectivevalue: float | None = None
        self._referenceglobalobjectivevalueunscaled: float | None = None
        self._globalobjectivefunctionvalue_previousouterloop: float | None = None
        self._globalobjectivefunctionvalueunscaled_previousouterloop: float | None = None
        self._globalobjectivefunctionvalue_previousinnerloop: float | None = None
        self._globalobjectivefunctionvalueunscaled_previousinnerloop: float | None = None        
        
        self._signedabsdistancefromreferenceglobalobjectivevalue: float | None = None
        self._signedabsdistancefromreferenceglobalobjectivevalueunscaled: float | None = None
        self._absdistancefromreferencedesignvariables: List[float] | None = None
        self._l2normfromreferencedesignvariables: float | None = None
        self._absdistancefromreferenceunscaleddesignvariables: List[float] | None = None 
        self._l2normfromreferencedesignvariablesunscaled: float | None = None
        self._relativerateofchangeglobaldesignvariables_outerloop: List[float] | None = None
        self._relativerateofchangeglobaldesignvariablesunscaled_outerloop: List[float] | None = None
        self._relativerateofchangeglobaldesignvariables_innerloop: List[float] | None = None
        self._relativerateofchangeglobaldesignvariablesunscaled_innerloop: List[float] | None = None
        self._rateofchangeglobalobjectiveunscaled_outerloop: float | None = None
        self._rateofchangeglobalobjective_outerloop: float | None = None
        self._lograteofchangeglobalobjectiveunscaled_outerloop: float | None = None
        self._lograteofchangeglobalobjective_outerloop: float | None = None
        self._rateofchangeconvergence_globalobjectivevalueunscaled: float | None = None
        self._rateofchangeconvergence_globalobjectivevalue: float | None = None
        self._rateofchangeglobalobjective_innerloop: float | None = None
        self._rateofchangeglobalobjectiveunscaled_innerloop: float | None = None
        self._lograteofchangeglobalobjective_innerloop: float | None = None
        self._lograteofchangeglobalobjectiveunscaled_innerloop: float | None = None
        self._rateofchangeconvergence_globalobjectivevalue_innerloop: float | None = None
        self._rateofchangeconvergence_globalobjectivevalueunscaled_innerloop: float | None = None
        self._relativerateofchangereferenceglobaldesignvariables_norm: float | None = None
        self._relativerateofchangereferenceglobaldesignvariablesunscaled_norm: float | None = None
        self._distancefromreferenceglobaloptimaunscaled: float | None = None
        self._distancefromreferencesubsystemoptimaunscaled: List[float] | None = None
    
    
    # def compute_NumberOfDesignVariableEvaluations(self, subsystems: List[SubSystemInterface]) -> None:
    #     """_summary_

    #     Args:
    #         subsystems (List[SubSystemInterface]): _description_
    #     """
    #     numberofdesignvariableevaluations = None
    #     for subsystem in subsystems:
    #         optimdata: OptimData = subsystem.get_OptimData()
    #         number: int = optimdata.get_NumberOfDesignVariableEvaluations()
    #         if numberofdesignvariableevaluations is None:
    #             numberofdesignvariableevaluations = number
    #         else:
    #             numberofdesignvariableevaluations += number
    #     self._numberofdesignvariableevaluations: int = numberofdesignvariableevaluations
        
    # def compute_RunTime(self, subsystems: List[SubSystemInterface]) -> None:
    #     """_summary_

    #     Args:
    #         subsystems (List[SubSystemInterface]): _description_
    #     """
    #     runtime = None
    #     for subsystem in subsystems:
    #         optimdata: OptimData = subsystem.get_OptimData()
    #         time: float = optimdata.get_Optimiation_RunTime()
    #         if runtime is None:
    #             runtime = time
    #         else:
    #             runtime += time
    #     self._runtime: float = runtime

    def compute_GlobalObjectiveValue(self, subsystems: List[SubSystemInterface]) -> None:
        """Compute the current scaled global objective function value of the entire problem.

        Args:
            subsystems: List of subsystems to compute the objective from.
        """

        global_obj = None

        for subsystem in subsystems:
            # Only LocalSubSystemBasis instances have local objective values;
            # ControllerSubSystem objects do not participate in the global objective.
            if isinstance(subsystem, LocalSubSystemBasis):
                optimdata: OptimDataBasis = subsystem.get_OptimData()
                obj_val: float | None = optimdata.get_LocalObjectiveValue()
                if obj_val is not None:
                    if global_obj is None:
                        global_obj = obj_val
                    else:
                        global_obj += obj_val
        self._globalobjectivefunctionvalue = global_obj
    
    def compute_GlobalObjectiveValueUnscaled(self, subsystems: List[SubSystemInterface]) -> None:
        """Compute the current unscaled global objective function value of the entire problem.

        Args:
            subsystems: List of subsystems to compute the objective from.
        """

        global_obj = None

        for subsystem in subsystems:
            # Only LocalSubSystemBasis instances have local objective values;
            # ControllerSubSystem objects do not participate in the global objective.
            if isinstance(subsystem, LocalSubSystemBasis):
                optimdata: OptimDataBasis = subsystem.get_OptimData()
                obj_val: float | None = optimdata.get_LocalObjectiveValue_Unscaled()
                if obj_val is not None:
                    if global_obj is None:
                        global_obj = obj_val
                    else:
                        global_obj += obj_val
        self._globalobjectivefunctionvalueunscaled = global_obj
        
    def compute_GlobalObjectiveValue_previousOuterLoop(self, subsystems: List[SubSystemInterface]) -> None:
        """Compute the scaled global objective value of the previous outer loop.

        Args:
            subsystems: List of subsystems to retrieve previous objective from.
        """
        
        globalobjectiveprevious = None
        for subsystem in subsystems:
            # Only LocalSubSystemBasis instances have local objective values;
            # ControllerSubSystem objects do not participate in the global objective.
            if isinstance(subsystem, LocalSubSystemBasis):
                previousvalue: float | None = subsystem.copy_LocalObjective_Previous_outerloop_itr()
                if previousvalue is not None:
                    if globalobjectiveprevious is None:
                        globalobjectiveprevious = previousvalue
                    else:
                        globalobjectiveprevious += previousvalue
        
        self._globalobjectivefunctionvalue_previousouterloop = globalobjectiveprevious
    
    def compute_GlobalObjectiveValueUnscaled_previousOuterLoop(self, subsystems: List[SubSystemInterface]) -> None:
        """Compute the unscaled global objective value of the previous outer loop.

        Args:
            subsystems: List of subsystems to retrieve previous objective from.
        """
        
        globalobjectiveprevious = None
        for subsystem in subsystems:
            # Only LocalSubSystemBasis instances have local objective values;
            # ControllerSubSystem objects do not participate in the global objective.
            if isinstance(subsystem, LocalSubSystemBasis):
                previousvalue: float | None = subsystem.copy_LocalObjectiveUnscaled_Previous_outerloop_itr()
                if previousvalue is not None:
                    if globalobjectiveprevious is None:
                        globalobjectiveprevious = previousvalue
                    else:
                        globalobjectiveprevious += previousvalue
        
        self._globalobjectivefunctionvalueunscaled_previousouterloop = globalobjectiveprevious
    
    def compute_GlobalObjectiveValue_previousInnerLoop(self, subsystems: List[SubSystemInterface]) -> None:
        """Compute the scaled global objective value of the previous inner loop.

        Args:
            subsystems: List of subsystems to retrieve previous objective from.
        """
        
        globalobjectiveprevious = None
        for subsystem in subsystems:
            # Only LocalSubSystemBasis instances have local objective values;
            # ControllerSubSystem objects do not participate in the global objective.
            if isinstance(subsystem, LocalSubSystemBasis):
                previousvalue: float | None = subsystem.copy_LocalObjective_Previous_innerloop_itr()
                if previousvalue is not None:
                    if globalobjectiveprevious is None:
                        globalobjectiveprevious = previousvalue
                    else:
                        globalobjectiveprevious += previousvalue
        
        self._globalobjectivefunctionvalue_previousinnerloop = globalobjectiveprevious
    
    def compute_GlobalObjectiveValueUnscaled_previousInnerLoop(self, subsystems: List[SubSystemInterface]) -> None:
        """Compute the unscaled global objective value of the previous inner loop.

        Args:
            subsystems: List of subsystems to retrieve previous objective from.
        """
        
        globalobjectiveprevious = None
        for subsystem in subsystems:
            # Only LocalSubSystemBasis instances have local objective values;
            # ControllerSubSystem objects do not participate in the global objective.
            if isinstance(subsystem, LocalSubSystemBasis):
                previousvalue: float | None = subsystem.copy_LocalObjectiveUnscaled_Previous_innerloop_itr()
                if previousvalue is not None:
                    if globalobjectiveprevious is None:
                        globalobjectiveprevious = previousvalue
                    else:
                        globalobjectiveprevious += previousvalue
        
        self._globalobjectivefunctionvalueunscaled_previousinnerloop = globalobjectiveprevious

    def store_GlobalDesignVariables(self, subsystems: List[SubSystemInterface]) -> None:
        """Store the vector of current scaled global design variable values for all subsystems.

        Args:
            subsystems: List of subsystems containing design variables.
        """
        globaldesignvariables_vals = []
        for subsystem in subsystems:
            # GlobalDesignVariables are defined only by LocalSubSystemBasis instances;
            # ControllerSubSystem design variables are not part of this global vector.
            if isinstance(subsystem, LocalSubSystemBasis):
                optimdata: OptimDataBasis = subsystem.get_OptimData()
                design_variables = optimdata.get_DesignVariables()
                if design_variables is not None:
                    globaldesignvariables_vals = globaldesignvariables_vals + design_variables

        self._globaldesignvariables = globaldesignvariables_vals if globaldesignvariables_vals else None
        
    def store_GlobalDesignVariablesUnscaled(self, subsystems: List[SubSystemInterface]) -> None:
        """Store the vector of current unscaled global design variable values for all subsystems.

        Args:
            subsystems: List of subsystems containing design variables.
        """
        globaldesignvariables_vals = []
        for subsystem in subsystems:
            # GlobalDesignVariables are defined only by LocalSubSystemBasis instances;
            # ControllerSubSystem design variables are not part of this global vector.
            if isinstance(subsystem, LocalSubSystemBasis):
                optimdata: OptimDataBasis = subsystem.get_OptimData()
                design_variables = optimdata.get_DesignVariables_Unscaled()
                if design_variables is not None:
                    globaldesignvariables_vals = globaldesignvariables_vals + design_variables

        self._globaldesignvariablesunscaled = globaldesignvariables_vals if globaldesignvariables_vals else None
    
    def store_GlobalDesignVariables_previousOuterLoop(self, subsystems: List[SubSystemInterface]) -> None:
        """Store the vector of previous outer loop scaled global design variable values.

        Args:
            subsystems: List of subsystems containing previous design variables.
        """
        globaldesignvariables_vals = []
        for subsystem in subsystems:
            # GlobalDesignVariables are defined only by LocalSubSystemBasis instances;
            # ControllerSubSystem design variables are not part of this global vector.
            if isinstance(subsystem, LocalSubSystemBasis):
                design_variables: List[float] | None = subsystem.copy_DesignVariables_Previous_outerloop_itr()
                if design_variables is not None:
                    globaldesignvariables_vals = globaldesignvariables_vals + design_variables
                
        self._globaldesignvariables_previousouterloop = globaldesignvariables_vals if globaldesignvariables_vals else None
        
    def store_GlobalDesignVariablesUnscaled_previousOuterLoop(self, subsystems: List[SubSystemInterface]) -> None:
        """Store the vector of previous outer loop unscaled global design variable values.

        Args:
            subsystems: List of subsystems containing previous design variables.
        """
        globaldesignvariables_vals = []
        for subsystem in subsystems:
            # GlobalDesignVariables are defined only by LocalSubSystemBasis instances;
            # ControllerSubSystem design variables are not part of this global vector.
            if isinstance(subsystem, LocalSubSystemBasis):
                design_variables: List[float] | None = subsystem.copy_DesignVariablesUnscaled_Previous_outerloop_itr()
                if design_variables is not None:
                    globaldesignvariables_vals = globaldesignvariables_vals + design_variables
                
        self._globaldesignvariablesunscaled_previousouterloop = globaldesignvariables_vals if globaldesignvariables_vals else None
        
    def store_GlobalDesignVariables_previousInnerLoop(self, subsystems: List[SubSystemInterface]) -> None:
        """Store the vector of previous inner loop scaled global design variable values.

        Args:
            subsystems: List of subsystems containing previous design variables.
        """
        globaldesignvariables_vals = []
        for subsystem in subsystems:
            # GlobalDesignVariables are defined only by LocalSubSystemBasis instances;
            # ControllerSubSystem design variables are not part of this global vector.
            if isinstance(subsystem, LocalSubSystemBasis):
                design_variables: List[float] | None = subsystem.copy_DesignVariables_Previous_innerloop_itr()
                if design_variables is not None:
                    globaldesignvariables_vals = globaldesignvariables_vals + design_variables
                
        self._globaldesignvariables_previousinnerloop = globaldesignvariables_vals if globaldesignvariables_vals else None
        
    def store_GlobalDesignVariablesUnscaled_previousInnerLoop(self, subsystems: List[SubSystemInterface]) -> None:
        """Store the vector of previous inner loop unscaled global design variable values.

        Args:
            subsystems: List of subsystems containing previous design variables.
        """
        globaldesignvariables_vals = []
        for subsystem in subsystems:
            # GlobalDesignVariables are defined only by LocalSubSystemBasis instances;
            # ControllerSubSystem design variables are not part of this global vector.
            if isinstance(subsystem, LocalSubSystemBasis):
                design_variables: List[float] | None = subsystem.copy_DesignVariablesUnscaled_Previous_innerloop_itr()
                if design_variables is not None:
                    globaldesignvariables_vals = globaldesignvariables_vals + design_variables
                
        self._globaldesignvariablesunscaled_previousinnerloop = globaldesignvariables_vals if globaldesignvariables_vals else None
        
    def store_RefGlobalDesignVariables(self, subsystems: List[SubSystemInterface]) -> None:
        """Stores the Scaled Reference GlobalDesignVariables values vector for all the subsystems.

        Args:
            subsystems: List of subsystems containing subsystems.
        """
        
        refglobaldesignvariables_vals = []        
        for subsystem in subsystems:
            # GlobalDesignVariables are defined only by LocalSubSystemBasis instances;
            # ControllerSubSystem design variables are not part of this global vector.
            if isinstance(subsystem, LocalSubSystemBasis):
                refdesign_variables = subsystem.get_ReferenceDesignVariables()
                if refdesign_variables is not None:
                    refglobaldesignvariables_vals = refglobaldesignvariables_vals + refdesign_variables
                
        self._referenceglobaldesignvariables = refglobaldesignvariables_vals if refglobaldesignvariables_vals else None
        
    def store_RefGlobalDesignVariablesUnscaled(self, subsystems: List[SubSystemInterface]) -> None:
        """Stores the Reference GlobalDesignVariables values vector for all the subsystems.

        Args:
            subsystems: List of subsystems containing subsystems.
        """
        
        refglobaldesignvariables_vals = []        
        for subsystem in subsystems:
            # GlobalDesignVariables are defined only by LocalSubSystemBasis instances;
            # ControllerSubSystem design variables are not part of this global vector.
            if isinstance(subsystem, LocalSubSystemBasis):
                refdesign_variables = subsystem.get_ReferenceDesignVariables_Unscaled()
                if refdesign_variables is not None:
                    refglobaldesignvariables_vals = refglobaldesignvariables_vals + refdesign_variables
                
        self._referenceglobaldesignvariablesunscaled = refglobaldesignvariables_vals if refglobaldesignvariables_vals else None
        
    def store_RefGlobalObjectiveValue(self, subsystems: List[SubSystemInterface]) -> None:
        """Stores the Scaled Reference Global Objective Function Value.

        Args:
            subsystems: List of subsystems containing subsystems.
        """
        global_obj = None
        for subsystem in subsystems:
            # Only LocalSubSystemBasis instances have reference objective values;
            # ControllerSubSystem objects do not participate in the global objective.
            if isinstance(subsystem, LocalSubSystemBasis):
                obj_val: float | None = subsystem.get_ReferenceLocalObjectiveValue()
                if obj_val is not None:
                    if global_obj is None:
                        global_obj = obj_val
                    else:
                        global_obj += obj_val
        
        self._referenceglobalobjectivevalue = global_obj
    
    def store_RefGlobalObjectiveValueUnscaled(self, subsystems: List[SubSystemInterface]) -> None:
        """Stores the Unscaled Reference Global Objective Function Value.

        Args:
            subsystems: List of subsystems containing subsystems.
        """
        global_obj = None
        for subsystem in subsystems:
            # Only LocalSubSystemBasis instances have reference objective values;
            # ControllerSubSystem objects do not participate in the global objective.
            if isinstance(subsystem, LocalSubSystemBasis):
                obj_val: float | None = subsystem.get_ReferenceLocalObjectiveValueUnscaled()
                if obj_val is not None:
                    if global_obj is None:
                        global_obj = obj_val
                    else:
                        global_obj += obj_val
        
        self._referenceglobalobjectivevalueunscaled = global_obj
        
    def compute_SignedAbsDistanceFromReferenceGlobalObjectiveValue(self) -> None:
        """Compute the signed distance from the scaled reference global objective value."""
        if self._referenceglobalobjectivevalue is not None and self._globalobjectivefunctionvalue is not None:
            self._signedabsdistancefromreferenceglobalobjectivevalue = self._referenceglobalobjectivevalue - self._globalobjectivefunctionvalue
        else:
            self._signedabsdistancefromreferenceglobalobjectivevalue = None
    
    def compute_SignedAbsDistanceFromReferenceGlobalObjectiveValueUnscaled(self) -> None:
        """Compute the signed distance from the unscaled reference global objective value."""
        if self._referenceglobalobjectivevalueunscaled is not None and self._globalobjectivefunctionvalueunscaled is not None:
            self._signedabsdistancefromreferenceglobalobjectivevalueunscaled = self._referenceglobalobjectivevalueunscaled - self._globalobjectivefunctionvalueunscaled
        else:
            self._signedabsdistancefromreferenceglobalobjectivevalueunscaled = None
        
    def compute_AbsDistanceFromReferenceDesignVariables(self) -> None:
        """Compute the absolute distance from scaled reference design variables."""
        if self._referenceglobaldesignvariables is not None and self._globaldesignvariables is not None:
            abs_dist = []
            for ref, desvar in zip(self._referenceglobaldesignvariables, self._globaldesignvariables):
                abs_dist.append(abs(ref-desvar))                
            self._absdistancefromreferencedesignvariables = abs_dist
        else:
            self._absdistancefromreferencedesignvariables = None
            
    def compute_AbsDistanceFromReferenceDesignVariables_Unscaled(self) -> None:
        """Compute the absolute distance from unscaled reference design variables."""
        if self._referenceglobaldesignvariablesunscaled is not None and self._globaldesignvariablesunscaled is not None:
            abs_dist = []
            for ref, desvar in zip(self._referenceglobaldesignvariablesunscaled, self._globaldesignvariablesunscaled):
                abs_dist.append(abs(ref-desvar))
            self._absdistancefromreferenceunscaleddesignvariables = abs_dist
        else:
            self._absdistancefromreferenceunscaleddesignvariables = None
    
    def compute_L2NormFromReferenceDesignVariables(self) -> None:
        """Compute the L2 norm from scaled reference design variables."""
        if self._referenceglobaldesignvariables is not None and self._globaldesignvariables is not None:            
            self._l2normfromreferencedesignvariables = float(np.linalg.norm(np.array(self._referenceglobaldesignvariables)-np.array(self._globaldesignvariables), 2))            
        else:
            self._l2normfromreferencedesignvariables = None   
    
    def compute_L2NormFromReferenceDesignVariables_Unscaled(self) -> None:
        """Compute the L2 norm from unscaled reference design variables."""
        if self._referenceglobaldesignvariablesunscaled is not None and self._globaldesignvariablesunscaled is not None:
            self._l2normfromreferencedesignvariablesunscaled = float(np.linalg.norm(np.array(self._referenceglobaldesignvariablesunscaled)-np.array(self._globaldesignvariablesunscaled), 2))         
        else:
            self._l2normfromreferencedesignvariablesunscaled =  None

    def compute_RateofChange_GlobalObjectiveValue_Outerloop(self, convinnerloop: bool) -> None:
        """Compute the rate of change of scaled global objective function value for outer loop.

        Args:
            convinnerloop: Whether the inner loop has converged.
        """
        
        if convinnerloop is True and self._globalobjectivefunctionvalue_previousouterloop is not None and self._globalobjectivefunctionvalue is not None:            
            self._rateofchangeglobalobjective_outerloop = self._globalobjectivefunctionvalue - self._globalobjectivefunctionvalue_previousouterloop
        else: 
            self._rateofchangeglobalobjective_outerloop = None
    
    def compute_RateofChange_GlobalObjectiveValueUnscaled_Outerloop(self, convinnerloop: bool) -> None:
        """Compute the rate of change of unscaled global objective function value for outer loop.

        Args:
            convinnerloop: Whether the inner loop has converged.
        """
        
        if convinnerloop is True and self._globalobjectivefunctionvalueunscaled_previousouterloop is not None and self._globalobjectivefunctionvalueunscaled is not None:            
            self._rateofchangeglobalobjectiveunscaled_outerloop = self._globalobjectivefunctionvalueunscaled - self._globalobjectivefunctionvalueunscaled_previousouterloop
        else:
            self._rateofchangeglobalobjectiveunscaled_outerloop = None
            
    def compute_RateofChange_GlobalObjectiveValue_Innerloop(self) -> None:
        """Compute the rate of change of scaled global objective function value for inner loop."""
        if self._globalobjectivefunctionvalue_previousinnerloop is not None and self._globalobjectivefunctionvalue is not None:            
            self._rateofchangeglobalobjective_innerloop = self._globalobjectivefunctionvalue - self._globalobjectivefunctionvalue_previousinnerloop
        else: 
            self._rateofchangeglobalobjective_innerloop = None
    
    def compute_RateofChange_GlobalObjectiveValueUnscaled_Innerloop(self) -> None:
        """Compute the rate of change of unscaled global objective function value for inner loop."""
        if self._globalobjectivefunctionvalueunscaled_previousinnerloop is not None and self._globalobjectivefunctionvalueunscaled is not None:            
            self._rateofchangeglobalobjectiveunscaled_innerloop = self._globalobjectivefunctionvalueunscaled - self._globalobjectivefunctionvalueunscaled_previousinnerloop
        else: 
            self._rateofchangeglobalobjectiveunscaled_innerloop = None
            
    def _safe_log_rate_of_change(self, current: float | None, previous: float | None) -> float | None:
        """Compute signed log rate of change, returning None if values are non-positive."""
        if current is None or previous is None or current <= 0 or previous <= 0:
            return None
        log_diff = np.log(current) - np.log(previous)
        sign = np.sign(current - previous)
        return float(log_diff * sign)

    def compute_LogRateofChange_GlobaObjectiveValue_Outerloop(self, convinnerloop: bool) -> None:
        """Compute the log rate of change of scaled global objective function value for outer loop.

        Args:
            convinnerloop: Whether the inner loop has converged.
        """ 
        if convinnerloop is True:
            self._lograteofchangeglobalobjective_outerloop = self._safe_log_rate_of_change(
                self._globalobjectivefunctionvalue, self._globalobjectivefunctionvalue_previousouterloop)
        else:
            self._lograteofchangeglobalobjective_outerloop = None

    def compute_LogRateofChange_GlobaObjectiveValueUnscaled_Outerloop(self, convinnerloop: bool) -> None:
        """Compute the log rate of change of unscaled global objective function value for outer loop.

        Args:
            convinnerloop: Whether the inner loop has converged.
        """
        if convinnerloop is True:
            self._lograteofchangeglobalobjectiveunscaled_outerloop = self._safe_log_rate_of_change(
                self._globalobjectivefunctionvalueunscaled, self._globalobjectivefunctionvalueunscaled_previousouterloop)
        else:
            self._lograteofchangeglobalobjectiveunscaled_outerloop = None
            
    def compute_LogRateofChange_GlobaObjectiveValue_Innerloop(self) -> None:
        """Compute the log rate of change of scaled global objective function value for inner loop.""" 
        self._lograteofchangeglobalobjective_innerloop = self._safe_log_rate_of_change(
            self._globalobjectivefunctionvalue, self._globalobjectivefunctionvalue_previousinnerloop)
            
    def compute_LogRateofChange_GlobaObjectiveValueUnscaled_Innerloop(self) -> None:
        """Compute the log rate of change of unscaled global objective function value for inner loop."""
        self._lograteofchangeglobalobjectiveunscaled_innerloop = self._safe_log_rate_of_change(
            self._globalobjectivefunctionvalueunscaled, self._globalobjectivefunctionvalueunscaled_previousinnerloop)
    
    def compute_RateofChangeConvergence_GlobalObjectiveValue_Outerloop(self, convinnerloop: bool) -> None:
        """Compute the rate of change convergence for scaled global objective value in outer loop.

        Args:
            convinnerloop: Whether the inner loop has converged.
        """
        if convinnerloop is True and self._globalobjectivefunctionvalue_previousouterloop is not None and self._globalobjectivefunctionvalue is not None:
            self._rateofchangeconvergence_globalobjectivevalue = abs(self._globalobjectivefunctionvalue - self._globalobjectivefunctionvalue_previousouterloop) / (1 + abs(self._globalobjectivefunctionvalue))
        else:
            self._rateofchangeconvergence_globalobjectivevalue = None
            
    def compute_RateofChangeConvergence_GlobalObjectiveValueUnscaled_Outerloop(self, convinnerloop: bool) -> None:
        """Compute the rate of change convergence for unscaled global objective value in outer loop.

        Args:
            convinnerloop: Whether the inner loop has converged.
        """

        if convinnerloop is True and self._globalobjectivefunctionvalueunscaled_previousouterloop is not None and self._globalobjectivefunctionvalueunscaled is not None:
            self._rateofchangeconvergence_globalobjectivevalueunscaled = abs(self._globalobjectivefunctionvalueunscaled - self._globalobjectivefunctionvalueunscaled_previousouterloop) / (1 + abs(self._globalobjectivefunctionvalueunscaled))
        else:
            self._rateofchangeconvergence_globalobjectivevalueunscaled = None
    
    def compute_RateofChangeConvergence_GlobalObjectiveValue_Innerloop(self) -> None:
        """Compute the rate of change convergence for scaled global objective value in inner loop."""
        if self._globalobjectivefunctionvalue_previousinnerloop is not None and self._globalobjectivefunctionvalue is not None:
            self._rateofchangeconvergence_globalobjectivevalue_innerloop = abs(self._globalobjectivefunctionvalue - self._globalobjectivefunctionvalue_previousinnerloop) / (1 + abs(self._globalobjectivefunctionvalue))
        else:
            self._rateofchangeconvergence_globalobjectivevalue_innerloop = None
            
    def compute_RateofChangeConvergence_GlobalObjectiveValueUnscaled_Innerloop(self) -> None:
        """Compute the rate of change convergence for unscaled global objective value in inner loop."""

        if self._globalobjectivefunctionvalueunscaled_previousinnerloop is not None and self._globalobjectivefunctionvalueunscaled is not None:
            self._rateofchangeconvergence_globalobjectivevalueunscaled_innerloop = abs(self._globalobjectivefunctionvalueunscaled - self._globalobjectivefunctionvalueunscaled_previousinnerloop) / (1 + abs(self._globalobjectivefunctionvalueunscaled))
        else:
            self._rateofchangeconvergence_globalobjectivevalueunscaled_innerloop = None
    
    def compute_RelativeRateofChange_GlobalDesignVariables_Outerloop(self) -> None:
        """Compute the relative rate of change of scaled global design variables for outer loop."""
        epsilon: float = 1e-12
        if self._globaldesignvariables_previousouterloop is not None and self._globaldesignvariables is not None:
            globaldesignvariables_change = []
            for curr, prev in zip(self._globaldesignvariables_previousouterloop, self._globaldesignvariables):  # curr is float, prev is float
                rel: float = abs(prev - curr) / (abs(prev) + epsilon)
                globaldesignvariables_change.append(rel)
            self._relativerateofchangeglobaldesignvariables_outerloop = globaldesignvariables_change
        else:
            self._relativerateofchangeglobaldesignvariables_outerloop = None
    
    def compute_RelativeRateofChange_GlobalDesignVariablesUnscaled_Outerloop(self) -> None:
        """Compute the relative rate of change of unscaled global design variables for outer loop."""
        epsilon: float = 1e-12
        if self._globaldesignvariablesunscaled_previousouterloop is not None and self._globaldesignvariablesunscaled is not None:
            globaldesignvariables_change = []
            for curr, prev in zip(self._globaldesignvariablesunscaled_previousouterloop, self._globaldesignvariablesunscaled):  # curr is float, prev is float
                rel: float = abs(prev - curr) / (abs(prev) + epsilon)
                globaldesignvariables_change.append(rel)
            self._relativerateofchangeglobaldesignvariablesunscaled_outerloop = globaldesignvariables_change
        else:
            self._relativerateofchangeglobaldesignvariablesunscaled_outerloop = None
    
    def compute_RelativeRateofChange_GlobalDesignVariables_Innerloop(self) -> None:
        """Compute the relative rate of change of scaled global design variables for inner loop."""
        epsilon: float = 1e-12
        if self._globaldesignvariables_previousinnerloop is not None and self._globaldesignvariables is not None:
            globaldesignvariables_change = []
            for curr, prev in zip(self._globaldesignvariables_previousinnerloop, self._globaldesignvariables):  # curr is float, prev is float
                rel = abs(prev - curr) / (abs(prev) + epsilon)
                globaldesignvariables_change.append(rel)
            self._relativerateofchangeglobaldesignvariables_innerloop = globaldesignvariables_change
        else:
            self._relativerateofchangeglobaldesignvariables_innerloop = None
    
    def compute_RelativeRateofChange_GlobalDesignVariablesUnscaled_Innerloop(self) -> None:
        """Compute the relative rate of change of unscaled global design variables for inner loop."""
        epsilon: float = 1e-12
        if self._globaldesignvariablesunscaled_previousinnerloop is not None and self._globaldesignvariablesunscaled is not None:
            globaldesignvariables_change = []
            for curr, prev in zip(self._globaldesignvariablesunscaled_previousinnerloop, self._globaldesignvariablesunscaled):  # curr is float, prev is float
                if curr is not None and prev is not None:
                    rel = abs(prev - curr) / (abs(prev) + epsilon)
                    globaldesignvariables_change.append(rel)
            self._relativerateofchangeglobaldesignvariablesunscaled_innerloop = globaldesignvariables_change
        else:
            self._relativerateofchangeglobaldesignvariablesunscaled_innerloop = None
            
    def compute_RelativeRateofChangeGlobalDesignVariables_Norm(self) -> None:
        """
        Compute the L2 Norm of the relative change of scaled GlobalDesignVariables with respect to scaled Reference variables.
        
        """
        if self._referenceglobaldesignvariables is not None and self._globaldesignvariables is not None:
            self._relativerateofchangereferenceglobaldesignvariables_norm = float(np.linalg.norm(np.array(self._referenceglobaldesignvariables) - np.array(self._globaldesignvariables), 2) / np.linalg.norm(np.array(self._globaldesignvariables), 2))
        else:
            self._relativerateofchangereferenceglobaldesignvariables_norm = None
    
    def compute_RelativeRateofChangeGlobalDesignVariablesUnscaled_Norm(self) -> None:
        """
        Compute the L2 Norm of the relative change of Unscaled GlobalDesignVariables with respect to Unscaled Reference variables.
        
        """
        if self._referenceglobaldesignvariablesunscaled is not None and self._globaldesignvariablesunscaled is not None:
            self._relativerateofchangereferenceglobaldesignvariablesunscaled_norm = float(np.linalg.norm(np.array(self._referenceglobaldesignvariablesunscaled) - np.array(self._globaldesignvariablesunscaled), 2) / np.linalg.norm(np.array(self._globaldesignvariablesunscaled), 2))
        else:
            self._relativerateofchangereferenceglobaldesignvariablesunscaled_norm = None
            
    def compute_DistanceFromReferenceGlobalOptimaUnscaled(self) -> None:
        """Compute distance from reference global optima using the already-stored unscaled global objective."""
        if self._referenceglobalobjectivevalueunscaled is not None and self._globalobjectivefunctionvalueunscaled is not None:
            self._distancefromreferenceglobaloptimaunscaled = self._referenceglobalobjectivevalueunscaled - self._globalobjectivefunctionvalueunscaled
        else:
            self._distancefromreferenceglobaloptimaunscaled = None
        
        
    def compute_DistanceFromReferenceSubsystemOptimaUnscaled(self, subsystems: List[SubSystemInterface]) -> None:
        """Compute distance from reference optima for each subsystem.

        Args:
            subsystems: List of subsystems containing objective values.
        """
        
        referencedistance: List[float] = []
        
        for subsystem in subsystems:
            # Only LocalSubSystemBasis instances have reference objective values;
            # ControllerSubSystem objects do not participate in the global objective.
            if isinstance(subsystem, LocalSubSystemBasis):
                objval = subsystem.get_OptimData().get_LocalObjectiveValue_Unscaled()
                refobj = subsystem.get_ReferenceLocalObjectiveValueUnscaled()
                
                if refobj is not None and objval is not None:
                    referencedistance.append(refobj-objval)
                else:
                    # If a value is missing, we cannot compute distances for any subsystem
                    referencedistance = None
                    break

        self._distancefromreferencesubsystemoptimaunscaled = referencedistance
    
    
 

    def initialize_ReferenceValues(self, subsystems: List[SubSystemInterface]) -> None:
        """Initializes and stores reference values.

        Args:
            subsystems: List of subsystems containing subsystems.
        """
        if not self._referencevalues_initialized:
            # Store reference GlobalDesignVariables values
            self.store_RefGlobalDesignVariables(subsystems)
            
            # Store reference Unscaled GlobalDesignVariables values
            self.store_RefGlobalDesignVariablesUnscaled(subsystems)

            # Store scaled reference global objective value
            self.store_RefGlobalObjectiveValue(subsystems)
            
            # Store reference global objective value
            self.store_RefGlobalObjectiveValueUnscaled(subsystems)
            
            # Mark reference values as initialized
            self._referencevalues_initialized = True 
    
    def update(self, convinnerloop: bool, subsystems: List[SubSystemInterface]) -> None:
        """Updates the metrics for the current iteration.

        Args:
            convinnerloop: Flag indicating inner loop convergence.
            subsystems: List of subsystems containing subsystems.
        """
        self.initialize_ReferenceValues(subsystems)

        # Global objective values (scaled and unscaled)
        self.compute_GlobalObjectiveValue(subsystems)
        self.compute_GlobalObjectiveValueUnscaled(subsystems)

        # Previous iteration objective values
        self.compute_GlobalObjectiveValue_previousOuterLoop(subsystems)
        self.compute_GlobalObjectiveValueUnscaled_previousOuterLoop(subsystems)
        self.compute_GlobalObjectiveValue_previousInnerLoop(subsystems)
        self.compute_GlobalObjectiveValueUnscaled_previousInnerLoop(subsystems)

        # Global design variables (current, previous outerloop, previous innerloop)
        self.store_GlobalDesignVariables(subsystems)
        self.store_GlobalDesignVariablesUnscaled(subsystems)
        self.store_GlobalDesignVariables_previousOuterLoop(subsystems)
        self.store_GlobalDesignVariablesUnscaled_previousOuterLoop(subsystems)
        self.store_GlobalDesignVariables_previousInnerLoop(subsystems)
        self.store_GlobalDesignVariablesUnscaled_previousInnerLoop(subsystems)

        # Distance from reference objective
        self.compute_SignedAbsDistanceFromReferenceGlobalObjectiveValue()
        self.compute_SignedAbsDistanceFromReferenceGlobalObjectiveValueUnscaled()

        # Distance from reference design variables
        self.compute_AbsDistanceFromReferenceDesignVariables()
        self.compute_AbsDistanceFromReferenceDesignVariables_Unscaled()
        self.compute_L2NormFromReferenceDesignVariables()
        self.compute_L2NormFromReferenceDesignVariables_Unscaled()

        # Rate of change of global objective (outerloop and innerloop)
        self.compute_RateofChange_GlobalObjectiveValue_Outerloop(convinnerloop)
        self.compute_RateofChange_GlobalObjectiveValueUnscaled_Outerloop(convinnerloop)
        self.compute_RateofChange_GlobalObjectiveValue_Innerloop()
        self.compute_RateofChange_GlobalObjectiveValueUnscaled_Innerloop()

        # Log rate of change of global objective
        self.compute_LogRateofChange_GlobaObjectiveValue_Outerloop(convinnerloop)
        self.compute_LogRateofChange_GlobaObjectiveValueUnscaled_Outerloop(convinnerloop)
        self.compute_LogRateofChange_GlobaObjectiveValue_Innerloop()
        self.compute_LogRateofChange_GlobaObjectiveValueUnscaled_Innerloop()

        # Rate of change convergence
        self.compute_RateofChangeConvergence_GlobalObjectiveValue_Outerloop(convinnerloop)
        self.compute_RateofChangeConvergence_GlobalObjectiveValueUnscaled_Outerloop(convinnerloop)
        self.compute_RateofChangeConvergence_GlobalObjectiveValue_Innerloop()
        self.compute_RateofChangeConvergence_GlobalObjectiveValueUnscaled_Innerloop()

        # Relative rate of change of design variables
        self.compute_RelativeRateofChange_GlobalDesignVariables_Outerloop()
        self.compute_RelativeRateofChange_GlobalDesignVariablesUnscaled_Outerloop()
        self.compute_RelativeRateofChange_GlobalDesignVariables_Innerloop()
        self.compute_RelativeRateofChange_GlobalDesignVariablesUnscaled_Innerloop()

        # Relative change norms
        self.compute_RelativeRateofChangeGlobalDesignVariables_Norm()
        self.compute_RelativeRateofChangeGlobalDesignVariablesUnscaled_Norm()

        # Distance from reference optima
        self.compute_DistanceFromReferenceGlobalOptimaUnscaled()
        self.compute_DistanceFromReferenceSubsystemOptimaUnscaled(subsystems)

    def get_GlobalObjectiveFunctionValue(self) -> float | None:
        """Return the global objective function value.

        Returns:
            The global objective function value, or None if not yet computed.
        """
        return self._globalobjectivefunctionvalue

    def get_GlobalObjectiveFunctionValueUnscaled(self) -> float | None:
        """Return the unscaled global objective function value.

        Returns:
            The unscaled global objective function value, or None if not yet computed.
        """
        return self._globalobjectivefunctionvalueunscaled

    def get_ReferenceGlobalObjectiveValue(self) -> float | None:
        """Return the reference global objective value.

        Returns:
            The reference global objective value, or None if not yet computed.
        """
        return self._referenceglobalobjectivevalue

    def get_ReferenceGlobalObjectiveValueUnscaled(self) -> float | None:
        """Return the unscaled reference global objective value.

        Returns:
            The unscaled reference global objective value, or None if not yet computed.
        """
        return self._referenceglobalobjectivevalueunscaled

    def get_SignedDistanceFromReferenceGlobalObjectiveValue(self) -> float | None:
        """Return the signed distance from the scaled reference global objective value.

        Returns:
            Signed distance from reference, or None if not computed.
        """
        return self._signedabsdistancefromreferenceglobalobjectivevalue

    def get_SignedDistanceFromReferenceGlobalObjectiveValueUnscaled(self) -> float | None:
        """Return the signed distance from the unscaled reference global objective value.

        Returns:
            Signed distance from unscaled reference, or None if not computed.
        """
        return self._signedabsdistancefromreferenceglobalobjectivevalueunscaled

    def get_L2NormFromReferenceDesignVariables(self) -> float | None:
        """Return the L2 norm distance from scaled reference design variables.

        Returns:
            L2 norm distance, or None if not computed.
        """
        return self._l2normfromreferencedesignvariables

    def get_L2NormFromReferenceDesignVariablesUnscaled(self) -> float | None:
        """Return the L2 norm distance from unscaled reference design variables.

        Returns:
            L2 norm distance from unscaled reference, or None if not computed.
        """
        return self._l2normfromreferencedesignvariablesunscaled

    def get_DistanceFromReferenceGlobalOptimaUnscaled(self) -> float | None:
        """Return the distance from unscaled reference global optima.

        Returns:
            Distance from unscaled reference global optima, or None if not computed.
        """
        return self._distancefromreferenceglobaloptimaunscaled

    def get_DistanceFromReferenceSubsystemOptimaUnscaled(self) -> List[float] | None:
        """Return the distance from reference optima for each subsystem.

        Returns:
            List of distances per subsystem, or None if not computed.
        """
        return self._distancefromreferencesubsystemoptimaunscaled

    def print_end_of_innerloop_iteration(self) -> None:
        """Print current global objective value at end of innerloop iteration."""
        ddo_print("Performance Metrics:")
        ddo_print(f"   {'Global Objective Function Value:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self.get_GlobalObjectiveFunctionValue()}")
        ddo_print(f"   {'Distance from Ref. Global Obj. (Unscaled):'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self.get_SignedDistanceFromReferenceGlobalObjectiveValueUnscaled()}")
        ddo_print(f"   {'L2 Norm from Ref. Design Vars (Unscaled):'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self.get_L2NormFromReferenceDesignVariablesUnscaled()}")

    def print_termination_summary(self) -> None:
        """Print performance metrics summary at the end of the optimization run."""
        ddo_print("Performance Metrics:")
        ddo_print(f"   {'Global Objective Function Value:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self.get_GlobalObjectiveFunctionValue()} (Reference: {self.get_ReferenceGlobalObjectiveValue()})")
        ddo_print(f"   {'Global Obj. Function Value Unscaled:'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self.get_GlobalObjectiveFunctionValueUnscaled()} (Reference: {self.get_ReferenceGlobalObjectiveValueUnscaled()})")
        ddo_print(f"   {'Distance from Ref. Global Obj. (Scaled):'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self.get_SignedDistanceFromReferenceGlobalObjectiveValue()}")
        ddo_print(f"   {'Distance from Ref. Global Obj. (Unscaled):'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self.get_SignedDistanceFromReferenceGlobalObjectiveValueUnscaled()}")
        ddo_print(f"   {'L2 Norm from Ref. Design Vars (Scaled):'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self.get_L2NormFromReferenceDesignVariables()}")
        ddo_print(f"   {'L2 Norm from Ref. Design Vars (Unscaled):'.ljust(self._DDO_PRINT_LABEL_WIDTH)} {self.get_L2NormFromReferenceDesignVariablesUnscaled()}")
        
