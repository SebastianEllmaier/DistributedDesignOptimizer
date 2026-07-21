---
title: PerformanceMetrics
---

← Back to [postprocess](index.md)

# PerformanceMetrics

**Source:** [Distributed_Design_Optimizer\postprocess\PerformanceMetrics.py](PerformanceMetrics_source.md)

Performance metrics module.

This module provides functionality for computing performance metrics
in distributed optimization problems.

## Classes

### PerformanceMetrics

> Compute and store performance metrics for optimization convergence analysis.

#### Methods

??? abstract "__init__(self) → None"
    Initialize the PerformanceMetrics with default values.

??? abstract "compute_GlobalObjectiveValue(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Compute the current scaled global objective function value of the entire problem.


    **Args:**
    > subsystems: List of subsystems to compute the objective from.  

??? abstract "compute_GlobalObjectiveValueUnscaled(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Compute the current unscaled global objective function value of the entire problem.


    **Args:**
    > subsystems: List of subsystems to compute the objective from.  

??? abstract "compute_GlobalObjectiveValue_previousOuterLoop(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Compute the scaled global objective value of the previous outer loop.


    **Args:**
    > subsystems: List of subsystems to retrieve previous objective from.  

??? abstract "compute_GlobalObjectiveValueUnscaled_previousOuterLoop(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Compute the unscaled global objective value of the previous outer loop.


    **Args:**
    > subsystems: List of subsystems to retrieve previous objective from.  

??? abstract "compute_GlobalObjectiveValue_previousInnerLoop(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Compute the scaled global objective value of the previous inner loop.


    **Args:**
    > subsystems: List of subsystems to retrieve previous objective from.  

??? abstract "compute_GlobalObjectiveValueUnscaled_previousInnerLoop(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Compute the unscaled global objective value of the previous inner loop.


    **Args:**
    > subsystems: List of subsystems to retrieve previous objective from.  

??? abstract "store_GlobalDesignVariables(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Store the vector of current scaled global design variable values for all subsystems.


    **Args:**
    > subsystems: List of subsystems containing design variables.  

??? abstract "store_GlobalDesignVariablesUnscaled(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Store the vector of current unscaled global design variable values for all subsystems.


    **Args:**
    > subsystems: List of subsystems containing design variables.  

??? abstract "store_GlobalDesignVariables_previousOuterLoop(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Store the vector of previous outer loop scaled global design variable values.


    **Args:**
    > subsystems: List of subsystems containing previous design variables.  

??? abstract "store_GlobalDesignVariablesUnscaled_previousOuterLoop(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Store the vector of previous outer loop unscaled global design variable values.


    **Args:**
    > subsystems: List of subsystems containing previous design variables.  

??? abstract "store_GlobalDesignVariables_previousInnerLoop(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Store the vector of previous inner loop scaled global design variable values.


    **Args:**
    > subsystems: List of subsystems containing previous design variables.  

??? abstract "store_GlobalDesignVariablesUnscaled_previousInnerLoop(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Store the vector of previous inner loop unscaled global design variable values.


    **Args:**
    > subsystems: List of subsystems containing previous design variables.  

??? abstract "store_RefGlobalDesignVariables(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Stores the Scaled Reference GlobalDesignVariables values vector for all the subsystems.


    **Args:**
    > subsystems: List of subsystems containing subsystems.  

??? abstract "store_RefGlobalDesignVariablesUnscaled(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Stores the Reference GlobalDesignVariables values vector for all the subsystems.


    **Args:**
    > subsystems: List of subsystems containing subsystems.  

??? abstract "store_RefGlobalObjectiveValue(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Stores the Scaled Reference Global Objective Function Value.


    **Args:**
    > subsystems: List of subsystems containing subsystems.  

??? abstract "store_RefGlobalObjectiveValueUnscaled(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Stores the Unscaled Reference Global Objective Function Value.


    **Args:**
    > subsystems: List of subsystems containing subsystems.  

??? abstract "compute_SignedAbsDistanceFromReferenceGlobalObjectiveValue(self) → None"
    Compute the signed distance from the scaled reference global objective value.

??? abstract "compute_SignedAbsDistanceFromReferenceGlobalObjectiveValueUnscaled(self) → None"
    Compute the signed distance from the unscaled reference global objective value.

??? abstract "compute_AbsDistanceFromReferenceDesignVariables(self) → None"
    Compute the absolute distance from scaled reference design variables.

??? abstract "compute_AbsDistanceFromReferenceDesignVariables_Unscaled(self) → None"
    Compute the absolute distance from unscaled reference design variables.

??? abstract "compute_L2NormFromReferenceDesignVariables(self) → None"
    Compute the L2 norm from scaled reference design variables.

??? abstract "compute_L2NormFromReferenceDesignVariables_Unscaled(self) → None"
    Compute the L2 norm from unscaled reference design variables.

??? abstract "compute_RateofChange_GlobalObjectiveValue_Outerloop(self, convinnerloop: bool) → None"
    Compute the rate of change of scaled global objective function value for outer loop.


    **Args:**
    > convinnerloop: Whether the inner loop has converged.  

??? abstract "compute_RateofChange_GlobalObjectiveValueUnscaled_Outerloop(self, convinnerloop: bool) → None"
    Compute the rate of change of unscaled global objective function value for outer loop.


    **Args:**
    > convinnerloop: Whether the inner loop has converged.  

??? abstract "compute_RateofChange_GlobalObjectiveValue_Innerloop(self) → None"
    Compute the rate of change of scaled global objective function value for inner loop.

??? abstract "compute_RateofChange_GlobalObjectiveValueUnscaled_Innerloop(self) → None"
    Compute the rate of change of unscaled global objective function value for inner loop.

??? abstract "compute_LogRateofChange_GlobaObjectiveValue_Outerloop(self, convinnerloop: bool) → None"
    Compute the log rate of change of scaled global objective function value for outer loop.


    **Args:**
    > convinnerloop: Whether the inner loop has converged.  

??? abstract "compute_LogRateofChange_GlobaObjectiveValueUnscaled_Outerloop(self, convinnerloop: bool) → None"
    Compute the log rate of change of unscaled global objective function value for outer loop.


    **Args:**
    > convinnerloop: Whether the inner loop has converged.  

??? abstract "compute_LogRateofChange_GlobaObjectiveValue_Innerloop(self) → None"
    Compute the log rate of change of scaled global objective function value for inner loop.

??? abstract "compute_LogRateofChange_GlobaObjectiveValueUnscaled_Innerloop(self) → None"
    Compute the log rate of change of unscaled global objective function value for inner loop.

??? abstract "compute_RateofChangeConvergence_GlobalObjectiveValue_Outerloop(self, convinnerloop: bool) → None"
    Compute the rate of change convergence for scaled global objective value in outer loop.


    **Args:**
    > convinnerloop: Whether the inner loop has converged.  

??? abstract "compute_RateofChangeConvergence_GlobalObjectiveValueUnscaled_Outerloop(self, convinnerloop: bool) → None"
    Compute the rate of change convergence for unscaled global objective value in outer loop.


    **Args:**
    > convinnerloop: Whether the inner loop has converged.  

??? abstract "compute_RateofChangeConvergence_GlobalObjectiveValue_Innerloop(self) → None"
    Compute the rate of change convergence for scaled global objective value in inner loop.

??? abstract "compute_RateofChangeConvergence_GlobalObjectiveValueUnscaled_Innerloop(self) → None"
    Compute the rate of change convergence for unscaled global objective value in inner loop.

??? abstract "compute_RelativeRateofChange_GlobalDesignVariables_Outerloop(self) → None"
    Compute the relative rate of change of scaled global design variables for outer loop.

??? abstract "compute_RelativeRateofChange_GlobalDesignVariablesUnscaled_Outerloop(self) → None"
    Compute the relative rate of change of unscaled global design variables for outer loop.

??? abstract "compute_RelativeRateofChange_GlobalDesignVariables_Innerloop(self) → None"
    Compute the relative rate of change of scaled global design variables for inner loop.

??? abstract "compute_RelativeRateofChange_GlobalDesignVariablesUnscaled_Innerloop(self) → None"
    Compute the relative rate of change of unscaled global design variables for inner loop.

??? abstract "compute_RelativeRateofChangeGlobalDesignVariables_Norm(self) → None"
    Compute the L2 Norm of the relative change of scaled GlobalDesignVariables with respect to scaled Reference variables.

??? abstract "compute_RelativeRateofChangeGlobalDesignVariablesUnscaled_Norm(self) → None"
    Compute the L2 Norm of the relative change of Unscaled GlobalDesignVariables with respect to Unscaled Reference variables.

??? abstract "compute_DistanceFromReferenceGlobalOptimaUnscaled(self) → None"
    Compute distance from reference global optima using the already-stored unscaled global objective.

??? abstract "compute_DistanceFromReferenceSubsystemOptimaUnscaled(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Compute distance from reference optima for each subsystem.


    **Args:**
    > subsystems: List of subsystems containing objective values.  

??? abstract "initialize_ReferenceValues(self, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Initializes and stores reference values.


    **Args:**
    > subsystems: List of subsystems containing subsystems.  

??? abstract "update(self, convinnerloop: bool, subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)]) → None"
    Updates the metrics for the current iteration.


    **Args:**
    > convinnerloop: Flag indicating inner loop convergence.  
    > subsystems: List of subsystems containing subsystems.  

??? abstract "get_GlobalObjectiveFunctionValue(self) → float | None"
    Return the global objective function value.


    **Returns:**
    > The global objective function value, or None if not yet computed.  

??? abstract "get_GlobalObjectiveFunctionValueUnscaled(self) → float | None"
    Return the unscaled global objective function value.


    **Returns:**
    > The unscaled global objective function value, or None if not yet computed.  

??? abstract "get_ReferenceGlobalObjectiveValue(self) → float | None"
    Return the reference global objective value.


    **Returns:**
    > The reference global objective value, or None if not yet computed.  

??? abstract "get_ReferenceGlobalObjectiveValueUnscaled(self) → float | None"
    Return the unscaled reference global objective value.


    **Returns:**
    > The unscaled reference global objective value, or None if not yet computed.  

??? abstract "get_SignedDistanceFromReferenceGlobalObjectiveValue(self) → float | None"
    Return the signed distance from the scaled reference global objective value.


    **Returns:**
    > Signed distance from reference, or None if not computed.  

??? abstract "get_SignedDistanceFromReferenceGlobalObjectiveValueUnscaled(self) → float | None"
    Return the signed distance from the unscaled reference global objective value.


    **Returns:**
    > Signed distance from unscaled reference, or None if not computed.  

??? abstract "get_L2NormFromReferenceDesignVariables(self) → float | None"
    Return the L2 norm distance from scaled reference design variables.


    **Returns:**
    > L2 norm distance, or None if not computed.  

??? abstract "get_L2NormFromReferenceDesignVariablesUnscaled(self) → float | None"
    Return the L2 norm distance from unscaled reference design variables.


    **Returns:**
    > L2 norm distance from unscaled reference, or None if not computed.  

??? abstract "get_DistanceFromReferenceGlobalOptimaUnscaled(self) → float | None"
    Return the distance from unscaled reference global optima.


    **Returns:**
    > Distance from unscaled reference global optima, or None if not computed.  

??? abstract "get_DistanceFromReferenceSubsystemOptimaUnscaled(self) → List[float] | None"
    Return the distance from reference optima for each subsystem.


    **Returns:**
    > List of distances per subsystem, or None if not computed.  

??? abstract "print_end_of_innerloop_iteration(self) → None"
    Print current global objective value at end of innerloop iteration.

??? abstract "print_termination_summary(self) → None"
    Print performance metrics summary at the end of the optimization run.

