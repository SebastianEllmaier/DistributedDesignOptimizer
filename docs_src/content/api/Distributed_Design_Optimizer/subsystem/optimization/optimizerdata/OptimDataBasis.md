---
title: OptimDataBasis
---

← Back to [optimizerdata](index.md)

# OptimDataBasis

**Source:** [Distributed_Design_Optimizer\subsystem\optimization\optimizerdata\OptimDataBasis.py](OptimDataBasis_source.md)

Optimization data basis module.

This module provides the base class for optimization data structures.

## Classes

### OptimDataBasis

> Base data structure for optimization results.

> Holds design variables, objectives, constraints, gradients, Jacobians,
> multipliers, and solver metadata after a completed optimization.

#### Methods

??? abstract "__init__(self, optimizer_type: str | None, designvariables: List[float] | None, designvariables_unscaled: List[float] | None, lowerbounds: List[float] | None, lowerbounds_scaled: List[float] | None, upperbounds: List[float] | None, upperbounds_scaled: List[float] | None, totalobjectivevalue: float | None, coordinationobjectivevalue: float | None, totalconstrainteqvalue: List[float] | None, totalconstraintineqvalue: List[float] | None, coordinationequalityconstraintvalue: List[float] | None, coordinationinequalityconstraintvalue: List[float] | None, couplingparameters: List[[CouplingParametersBasis](../../couplingparameters/CouplingParametersBasis.md#couplingparametersbasis)] | None, gradient_coordinationobjective: List[float | None] | None, jacobian_coordinationequalityconstraints: List[List[float | None]] | None, jacobian_coordinationinequalityconstraints: List[List[float | None]] | None, gradient_totalobjective: List[float | None] | None, jacobian_totalequalityconstraints: List[List[float | None]] | None, jacobian_totalinequalityconstraints: List[List[float | None]] | None, jacobian_lowerbounds: List[List[float | None]] | None, jacobian_upperbounds: List[List[float | None]] | None, multipliers_lowerbounds: List[float | None] | None, multipliers_upperbounds: List[float | None] | None, multipliers_coordination_equality_constraints: List[float | None] | None, multipliers_coordination_inequality_constraints: List[float | None] | None, activecoordinationinequalityconstraints: List[bool] | None, activelowerbounds: List[bool] | None, activeupperbounds: List[bool] | None, exitflag: int | None, message: str | None, optimization_numberofdesignvariableevaluations: int | None, optimization_runtime: float | None, numberofactiveinequalityconstraints: int | None, numberofactivebounds: int | None) → None"
    Initialize OptimDataBasis.


    **Args:**
    > optimizer_type: The type of optimizer algorithm used.  
    > designvariables: List of scaled design variable values in [0.0, 1.0].  
    > designvariables_unscaled: List of unscaled design variable values.  
    > lowerbounds: List of unscaled lower bounds.  
    > lowerbounds_scaled: List of scaled lower bounds.  
    > upperbounds: List of unscaled upper bounds.  
    > upperbounds_scaled: List of scaled upper bounds.  
    > totalobjectivevalue: The total objective function value.  
    > coordinationobjectivevalue: The coordination objective value, or None  
    > if not available (e.g., when running Matlab Optimizer).  
    > totalconstrainteqvalue: List of total equality constraint values.  
    > totalconstraintineqvalue: List of total inequality constraint values.  
    > coordinationequalityconstraintvalue: List of coordination equality  
    > constraint values, or None if not available.  
    > coordinationinequalityconstraintvalue: List of coordination inequality  
    > constraint values, or None if not available.  
    > couplingparameters: List of coupling parameters objects.  
    > gradient_coordinationobjective: Gradient of the coordination objective.  
    > jacobian_coordinationequalityconstraints: Jacobian of the coordination  
    > equality constraints.  
    > jacobian_coordinationinequalityconstraints: Jacobian of the coordination  
    > inequality constraints.  
    > gradient_totalobjective: Gradient of the total objective.  
    > jacobian_totalequalityconstraints: Jacobian of the total equality  
    > constraints.  
    > jacobian_totalinequalityconstraints: Jacobian of the total inequality  
    > constraints.  
    > jacobian_lowerbounds: Jacobian of the lower bound constraints.  
    > jacobian_upperbounds: Jacobian of the upper bound constraints.  
    > multipliers_lowerbounds: Multipliers for the lower bounds.  
    > multipliers_upperbounds: Multipliers for the upper bounds.  
    > multipliers_coordination_equality_constraints: Multipliers for the  
    > coordination equality constraints.  
    > multipliers_coordination_inequality_constraints: Multipliers for the  
    > coordination inequality constraints.  
    > activecoordinationinequalityconstraints: List of bools indicating  
    > active coordination inequality constraints.  
    > activelowerbounds: List of bools indicating active lower bounds.  
    > activeupperbounds: List of bools indicating active upper bounds.  
    > exitflag: The exit flag indicating optimization convergence status.  
    > message: The optimization result message.  
    > optimization_numberofdesignvariableevaluations: Number of design  
    > variable evaluations during optimization.  
    > optimization_runtime: The runtime of the optimization in seconds.  
    > numberofactiveinequalityconstraints: Number of active inequality  
    > constraints, or None if not available.  
    > numberofactivebounds: Number of active bounds, or None if not available.  

??? abstract "set_Optimizer_Type(self, optimizer_type_in: str) → None"
    Set the type of optimization algorithm.


    **Args:**
    > optimizer_type_in: Optimizer algorithm identifier.  

??? abstract "get_Optimizer_Type(self) → str"
    Get the type of optimization algorithm.


    **Returns:**
    > The optimizer algorithm identifier.  

??? abstract "set_DesignVariables(self, designvariables_in: List[float]) → None"
    Set the design variables.


    **Args:**
    > designvariables_in: Design variables.  

??? abstract "get_DesignVariables(self) → List[float] | None"
    Get the design variables (scaled01 values).


    **Returns:**
    > The scaled design variable values.  

??? abstract "set_DesignVariables_Unscaled(self, designvariables_unscaled_in: List[float]) → None"
    Set the unscaled design variables.


    **Args:**
    > designvariables_unscaled_in: Unscaled design variables.  

??? abstract "get_DesignVariables_Unscaled(self) → List[float]"
    Get the unscaled design variables.


    **Returns:**
    > The unscaled design variable values.  

??? abstract "set_LowerBounds(self, lowerbounds_in: List[float]) → None"
    Set the lower bounds (unscaled).


    **Args:**
    > lowerbounds_in: Lower bounds.  

??? abstract "get_LowerBounds(self) → List[float] | None"
    Get the lower bounds (unscaled).


    **Returns:**
    > The lower bounds.  

??? abstract "set_LowerBounds_Scaled(self, lowerbounds_scaled_in: List[float]) → None"
    Set the scaled lower bounds.


    **Args:**
    > lowerbounds_scaled_in: Scaled lower bounds.  

??? abstract "get_LowerBounds_Scaled(self) → List[float] | None"
    Get the scaled lower bounds.


    **Returns:**
    > The scaled lower bounds.  

??? abstract "set_UpperBounds(self, upperbounds_in: List[float]) → None"
    Set the upper bounds (unscaled).


    **Args:**
    > upperbounds_in: Upper bounds.  

??? abstract "get_UpperBounds(self) → List[float] | None"
    Get the upper bounds (unscaled).


    **Returns:**
    > The upper bounds.  

??? abstract "set_UpperBounds_Scaled(self, upperbounds_scaled_in: List[float]) → None"
    Set the scaled upper bounds.


    **Args:**
    > upperbounds_scaled_in: Scaled upper bounds.  

??? abstract "get_UpperBounds_Scaled(self) → List[float] | None"
    Get the scaled upper bounds.


    **Returns:**
    > The scaled upper bounds.  

??? abstract "set_TotalObjectiveValue(self, totalobjectivevalue_in: float) → None"
    Set the local objective function value of the optimization problem.


    **Args:**
    > totalobjectivevalue_in: Total objective function value.  

??? abstract "get_TotalObjectiveValue(self) → float | None"
    Get the total objective function value of the optimization problem.


    **Returns:**
    > The total objective function value, or None if not set.  

??? abstract "set_CoordinationObjectiveValue(self, coordinationobjectivevalue_in: float) → None"
    Set the coordination objective value of the optimization problem.


    **Args:**
    > coordinationobjectivevalue_in: Coordination objective function value.  

??? abstract "get_CoordinationObjectiveValue(self) → float | None"
    Gets the coordination objective value.


    **Returns:**
    > The coordination objective value, or None if not available  
    > (e.g., when running Matlab Optimizer).  

??? abstract "set_CouplingParameters(self, couplingparameters_in: List[[CouplingParametersBasis](../../couplingparameters/CouplingParametersBasis.md#couplingparametersbasis)]) → None"
    Set coupling parameters to update current information.


    **Args:**
    > couplingparameters_in: The coupling parameters to set.  

??? abstract "get_CouplingParameters(self) → List[[CouplingParametersBasis](../../couplingparameters/CouplingParametersBasis.md#couplingparametersbasis)]"
    Get the coupling parameters.


    **Returns:**
    > The list of coupling parameters objects.  

??? abstract "set_Gradient_CoordinationObjective(self, gradient_coordinationobjective_in: List[float | None]) → None"
    Set the gradient of the coordination objective.


    **Args:**
    > gradient_coordinationobjective_in: Gradient of the coordination  
    > objective.  

??? abstract "get_Gradient_CoordinationObjective(self) → List[float | None] | None"
    Get the gradient of the coordination objective.


    **Returns:**
    > Gradient of the coordination objective, or None if not set.  

??? abstract "set_Jacobian_CoordinationEqualityConstraints(self, jacobian_coordinationequalityconstraints_in: List[List[float | None]]) → None"
    Set the Jacobian of the coordination equality constraints.


    **Args:**
    > jacobian_coordinationequalityconstraints_in: Jacobian of the  
    > coordination equality constraints.  

??? abstract "get_Jacobian_CoordinationEqualityConstraints(self) → List[List[float | None]] | None"
    Get the Jacobian of the coordination equality constraints.


    **Returns:**
    > Jacobian of the coordination equality constraints, or None if not  
    > set.  

??? abstract "set_Jacobian_CoordinationInequalityConstraints(self, jacobian_coordinationinequalityconstraints_in: List[List[float | None]]) → None"
    Set the Jacobian of the coordination inequality constraints.


    **Args:**
    > jacobian_coordinationinequalityconstraints_in: Jacobian of the  
    > coordination inequality constraints.  

??? abstract "get_Jacobian_CoordinationInequalityConstraints(self) → List[List[float | None]] | None"
    Get the Jacobian of the coordination inequality constraints.


    **Returns:**
    > Jacobian of the coordination inequality constraints, or None if  
    > not set.  

??? abstract "set_Gradient_TotalObjective(self, gradient_totalobjective_in: List[float | None]) → None"
    Set the gradient of the total objective.


    **Args:**
    > gradient_totalobjective_in: Gradient of the total objective.  

??? abstract "get_Gradient_TotalObjective(self) → List[float | None] | None"
    Get the gradient of the total objective.


    **Returns:**
    > Gradient of the total objective, or None if not set.  

??? abstract "set_Jacobian_TotalEqualityConstraints(self, jacobian_totalequalityconstraints_in: List[List[float | None]]) → None"
    Set the Jacobian of the total equality constraints.


    **Args:**
    > jacobian_totalequalityconstraints_in: Jacobian of the total equality  
    > constraints.  

??? abstract "get_Jacobian_TotalEqualityConstraints(self) → List[List[float | None]] | None"
    Get the Jacobian of the total equality constraints.


    **Returns:**
    > Jacobian of the total equality constraints, or None if not set.  

??? abstract "set_Jacobian_TotalInequalityConstraints(self, jacobian_totalinequalityconstraints_in: List[List[float | None]]) → None"
    Set the Jacobian of the total inequality constraints.


    **Args:**
    > jacobian_totalinequalityconstraints_in: Jacobian of the total  
    > inequality constraints.  

??? abstract "get_Jacobian_TotalInequalityConstraints(self) → List[List[float | None]] | None"
    Get the Jacobian of the total inequality constraints.


    **Returns:**
    > Jacobian of the total inequality constraints, or None if not set.  

??? abstract "set_Jacobian_LowerBounds(self, jacobian_lowerbounds_in: List[List[float | None]]) → None"
    Set the Jacobian of the lower bounds.


    **Args:**
    > jacobian_lowerbounds_in: Jacobian of the lower bounds.  

??? abstract "get_Jacobian_LowerBounds(self) → List[List[float | None]] | None"
    Get the Jacobian of the active lower bound constraints.


    **Returns:**
    > Jacobian of the active lower bounds, or None if not set.  

??? abstract "set_Jacobian_UpperBounds(self, jacobian_upperbounds_in: List[List[float | None]]) → None"
    Set the Jacobian of the upper bounds.


    **Args:**
    > jacobian_upperbounds_in: Jacobian of the upper bounds.  

??? abstract "get_Jacobian_UpperBounds(self) → List[List[float | None]] | None"
    Get the Jacobian of the active upper bound constraints.


    **Returns:**
    > Jacobian of the active upper bounds, or None if not set.  

??? abstract "set_Multipliers_LowerBounds(self, multipliers_lowerbounds_in: List[float | None]) → None"
    Set the multipliers w.r.t the lower bounds.


    **Args:**
    > multipliers_lowerbounds_in: Multipliers for the lower bounds.  

??? abstract "get_Multipliers_LowerBounds(self) → List[float | None] | None"
    Get the multipliers corresponding to the lower bounds.


    **Returns:**
    > Multipliers for the lower bounds, or None if not set.  

??? abstract "set_Multipliers_UpperBounds(self, multipliers_upperbounds_in: List[float | None]) → None"
    Set the multipliers w.r.t the upper bounds.


    **Args:**
    > multipliers_upperbounds_in: Multipliers for the upper bounds.  

??? abstract "get_Multipliers_UpperBounds(self) → List[float | None] | None"
    Get the multipliers corresponding to the upper bounds.


    **Returns:**
    > Multipliers for the upper bounds, or None if not set.  

??? abstract "set_Multipliers_Coordination_Equality_Constraints(self, multipliers_coordinationequalityconstraints_in: List[float | None]) → None"
    Set the multipliers w.r.t the coordination equality constraints.


    **Args:**
    > multipliers_coordinationequalityconstraints_in: Multipliers for the  
    > coordination equality constraints.  

??? abstract "get_Multipliers_Coordination_Equality_Constraints(self) → List[float | None] | None"
    Get the multipliers corresponding to the coordination equality constraints.


    **Returns:**
    > Multipliers for the coordination equality constraints, or None if  
    > not set.  

??? abstract "set_Multipliers_Coordination_Inequality_Constraints(self, multipliers_coordinationinequalityconstraints_in: List[float | None]) → None"
    Set the multipliers w.r.t the coordination inequality constraints.


    **Args:**
    > multipliers_coordinationinequalityconstraints_in: Multipliers for the  
    > coordination inequality constraints.  

??? abstract "get_Multipliers_Coordination_Inequality_Constraints(self) → List[float | None] | None"
    Get the multipliers corresponding to the coordination inequality constraints.


    **Returns:**
    > Multipliers for the coordination inequality constraints, or None  
    > if not set.  

??? abstract "set_TotalConstraintEqValue(self, totalconstrainteqvalue_in: List[float]) → None"
    Set the total equality constraint values.


    **Args:**
    > totalconstrainteqvalue_in: Total equality constraint values.  

??? abstract "get_TotalConstraintEqValue(self) → List[float] | None"
    Get the total equality constraint values.


    **Returns:**
    > The total equality constraint values, or None if not set.  

??? abstract "set_TotalConstraintIneqValue(self, totalconstraintineqvalue_in: List[float]) → None"
    Set the total inequality constraint values.


    **Args:**
    > totalconstraintineqvalue_in: Total inequality constraint values.  

??? abstract "get_TotalConstraintIneqValue(self) → List[float] | None"
    Get the total inequality constraint values.


    **Returns:**
    > The total inequality constraint values, or None if not set.  

??? abstract "set_CoordinationEqualityConstraintValue(self, coordinationequalityconstraintvalue_in: List[float]) → None"
    Set the coordination equality constraint values.


    **Args:**
    > coordinationequalityconstraintvalue_in: Coordination equality  
    > constraint values.  

??? abstract "get_CoordinationEqualityConstraintValue(self) → List[float] | None"
    Gets the coordination equality constraint values.


    **Returns:**
    > List of coordination equality constraint values, or None if not  
    > available (e.g., when running Matlab Optimizer).  

??? abstract "set_CoordinationInequalityConstraintValue(self, coordinationinequalityconstraintvalue_in: List[float]) → None"
    Set the coordination inequality constraint values.


    **Args:**
    > coordinationinequalityconstraintvalue_in: Coordination inequality  
    > constraint values.  

??? abstract "get_CoordinationInequalityConstraintValue(self) → List[float] | None"
    Get the coordination inequality constraint values.


    **Returns:**
    > The coordination inequality constraint values, or None if not set.  

??? abstract "get_ExitFlag(self) → int"
    Return the optimizer exit flag.


    **Returns:**
    > The optimizer exit flag.  

??? abstract "get_Message(self) → str"
    Get the optimization message.


    **Returns:**
    > The optimization result message.  

??? abstract "get_Optimization_NumberOfDesignVariableEvaluations(self) → int | None"
    Get the number of design variable evaluations.


    **Returns:**
    > The number of design variable evaluations.  

??? abstract "get_Optimization_RunTime(self) → float | None"
    Get the optimization runtime.


    **Returns:**
    > The optimization runtime in seconds.  

??? abstract "set_ActiveCoordinationInequalityConstraints(self, activecoordinationinequalityconstraints_in: List[bool]) → None"
    Set the list of bools indicating active coordination inequality constraints.


    **Args:**
    > activecoordinationinequalityconstraints_in: Active coordination  
    > inequality constraints.  

??? abstract "get_ActiveCoordinationInequalityConstraints(self) → List[bool] | None"
    Get the list of bools indicating active coordination inequality constraints.


    **Returns:**
    > Active coordination inequality constraints, or None if not set.  

??? abstract "set_ActiveLowerBounds(self, activelowerbounds_in: List[bool]) → None"
    Set the list of bools indicating active lower bounds.


    **Args:**
    > activelowerbounds_in: Active lower bounds.  

??? abstract "get_ActiveLowerBounds(self) → List[bool] | None"
    Get the list of bools indicating active lower bounds.


    **Returns:**
    > The active lower bounds.  

??? abstract "set_ActiveUpperBounds(self, activeupperbounds_in: List[bool]) → None"
    Set the list of bools indicating active upper bounds.


    **Args:**
    > activeupperbounds_in: Active upper bounds.  

??? abstract "get_ActiveUpperBounds(self) → List[bool] | None"
    Get the list of bools indicating active upper bounds.


    **Returns:**
    > The active upper bounds.  

??? abstract "set_NumberofActiveInequalityConstraints(self, numberofactiveinequalityconstraints_in: int) → None"
    Set the number of active inequality constraints.


    **Args:**
    > numberofactiveinequalityconstraints_in: Number of active inequality  
    > constraints.  

??? abstract "get_NumberofActiveInequalityConstraints(self) → int | None"
    Gets the number of active inequality constraints.


    **Returns:**
    > The number of active inequality constraints, or None if not available.  

??? abstract "set_NumberofActiveBounds(self, numberofactivebounds_in: int) → None"
    Set the number of active bounds.


    **Args:**
    > numberofactivebounds_in: Number of active bounds.  

??? abstract "get_NumberofActiveBounds(self) → int"
    Gets the number of active bounds.


    **Returns:**
    > The number of active bounds, or None if not available.  

??? abstract "get_RatioofActiveBoundsandConstraints(self) → float | None"
    Gets the ratio of active bounds and constraints to total.


    **Returns:**
    > The ratio of active constraints (input + output) to the total  
    > number of constraints and bounds, or None if not computable.  

??? abstract "print_results(self) → None"
    Print optimizer results.

