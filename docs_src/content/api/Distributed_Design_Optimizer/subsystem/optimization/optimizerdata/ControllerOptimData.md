---
title: ControllerOptimData
---

← Back to [optimizerdata](index.md)

# ControllerOptimData

**Source:** [Distributed_Design_Optimizer\subsystem\optimization\optimizerdata\ControllerOptimData.py](ControllerOptimData_source.md)

Controller optimization data module.

This module provides data structures for controller optimization.

## Classes

### ControllerOptimData

> **Inherits from:** [OptimDataBasis](OptimDataBasis.md#optimdatabasis)

> Optimization data for the controller subsystem.

> Extends OptimDataBasis as a marker subclass for controller-specific
> optimization results. If a distributed optimization algorithm requires
> additional controller data, implement a new subclass of ControllerOptimData.

#### Methods

??? abstract "__init__(self, optimizer_type: str | None, designvariables: List[float] | None, designvariables_unscaled: List[float] | None, lowerbounds: List[float] | None, lowerbounds_scaled: List[float] | None, upperbounds: List[float] | None, upperbounds_scaled: List[float] | None, totalobjectivevalue: float | None, coordinationobjectivevalue: float | None, totalconstrainteqvalue: List[float] | None, totalconstraintineqvalue: List[float] | None, coordinationequalityconstraintvalue: List[float] | None, coordinationinequalityconstraintvalue: List[float] | None, gradient_coordinationobjective: List[float | None] | None, jacobian_coordinationequalityconstraints: List[List[float | None]] | None, jacobian_coordinationinequalityconstraints: List[List[float | None]] | None, gradient_totalobjective: List[float | None] | None, jacobian_totalequalityconstraints: List[List[float | None]] | None, jacobian_totalinequalityconstraints: List[List[float | None]] | None, jacobian_lowerbounds: List[List[float | None]] | None, jacobian_upperbounds: List[List[float | None]] | None, multipliers_lowerbounds: List[float] | None, multipliers_upperbounds: List[float] | None, multipliers_coordination_equality_constraints: List[float] | None, multipliers_coordination_inequality_constraints: List[float] | None, activecoordinationinequalityconstraints: List[bool] | None, activelowerbounds: List[bool] | None, activeupperbounds: List[bool] | None, exitflag: int | None, message: str | None, optimization_numberofdesignvariableevaluations: int | None, optimization_runtime: float | None, numberofactiveinequalityconstraints: int | None, numberofactivebounds: int | None) → None"
    Initialize ControllerOptimData.


    **Args:**
    > optimizer_type: The type of optimizer algorithm used.  
    > designvariables: List of scaled design variable values.  
    > designvariables_unscaled: List of unscaled design variable values.  
    > totalobjectivevalue: The total objective function value.  
    > coordinationobjectivevalue: The coordination objective value, or None  
    > if not available (e.g., when running Matlab Optimizer).  
    > totalconstrainteqvalue: List of total equality constraint values.  
    > totalconstraintineqvalue: List of total inequality constraint values.  
    > coordinationequalityconstraintvalue: List of coordination equality  
    > constraint values, or None if not available.  
    > lowerbounds: List of lower bound values for design variables.  
    > lowerbounds_scaled: List of scaled lower bound values.  
    > upperbounds: List of upper bound values for design variables.  
    > upperbounds_scaled: List of scaled upper bound values.  
    > coordinationinequalityconstraintvalue: List of coordination  
    > inequality constraint values, or None if not available.  
    > gradient_coordinationobjective: Gradient of the coordination  
    > objective function, or None if not available.  
    > jacobian_coordinationequalityconstraints: Jacobian of the  
    > coordination equality constraints, or None if not available.  
    > jacobian_coordinationinequalityconstraints: Jacobian of the  
    > coordination inequality constraints, or None if not available.  
    > gradient_totalobjective: Gradient of the total objective function,  
    > or None if not available.  
    > jacobian_totalequalityconstraints: Jacobian of the total equality  
    > constraints, or None if not available.  
    > jacobian_totalinequalityconstraints: Jacobian of the total  
    > inequality constraints, or None if not available.  
    > jacobian_lowerbounds: Jacobian of the lower bounds, or None if not  
    > available.  
    > jacobian_upperbounds: Jacobian of the upper bounds, or None if not  
    > available.  
    > multipliers_lowerbounds: Lagrange multipliers for the lower bounds,  
    > or None if not available.  
    > multipliers_upperbounds: Lagrange multipliers for the upper bounds,  
    > or None if not available.  
    > multipliers_coordination_equality_constraints: Lagrange multipliers  
    > for coordination equality constraints, or None if not available.  
    > multipliers_coordination_inequality_constraints: Lagrange  
    > multipliers for coordination inequality constraints, or None if  
    > not available.  
    > activecoordinationinequalityconstraints: Boolean list indicating  
    > active coordination inequality constraints, or None if not  
    > available.  
    > activelowerbounds: Boolean list indicating active lower bounds, or  
    > None if not available.  
    > activeupperbounds: Boolean list indicating active upper bounds, or  
    > None if not available.  
    > exitflag: The exit flag indicating optimization convergence status.  
    > message: The optimization result message.  
    > optimization_numberofdesignvariableevaluations: Number of design  
    > variable evaluations during optimization.  
    > optimization_runtime: The runtime of the optimization in seconds.  
    > numberofactiveinequalityconstraints: Number of active inequality  
    > constraints, or None if not available.  
    > numberofactivebounds: Number of active bounds, or None if not available.  

??? abstract "print_results(self) → None"
    Print controller optimizer results.

