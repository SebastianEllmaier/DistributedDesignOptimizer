---
title: LocalSubSystemOptimData
---

← Back to [optimizerdata](index.md)

# LocalSubSystemOptimData

**Source:** [Distributed_Design_Optimizer\subsystem\optimization\optimizerdata\LocalSubSystemOptimData.py](LocalSubSystemOptimData_source.md)

Local subsystem optimization data module.

This module provides data structures for local subsystem optimization.

## Classes

### LocalSubSystemOptimData

> **Inherits from:** [OptimDataBasis](OptimDataBasis.md#optimdatabasis)

> Optimization data for local subsystems.

> Extends OptimDataBasis with local-specific data including local objectives,
> local constraints, coupling parameters, and local multipliers.

#### Methods

??? abstract "__init__(self, optimizer_type: str | None, designvariables: List[float] | None, designvariables_unscaled: List[float] | None, lowerbounds: List[float] | None, lowerbounds_scaled: List[float] | None, upperbounds: List[float] | None, upperbounds_scaled: List[float] | None, Responses_unscaled: List[float] | None, localobjectivevalue: float | None, localobjectivevalue_unscaled: float | None, totalobjectivevalue: float | None, coordinationobjectivevalue: float | None, equalitylocalconstraintsvalue: List[float] | None, equalitylocalconstraintsvalue_unscaled: List[float] | None, inequalitylocalconstraintsvalue: List[float] | None, inequalitylocalconstraintsvalue_unscaled: List[float] | None, totalconstrainteqvalue: List[float] | None, totalconstraintineqvalue: List[float] | None, coordinationequalityconstraintvalue: List[float] | None, coordinationinequalityconstraintvalue: List[float] | None, couplingparameters: List[[CouplingParametersBasis](../../couplingparameters/CouplingParametersBasis.md#couplingparametersbasis)] | None, gradient_localobjective: List[float | None] | None, gradient_coordinationobjective: List[float | None] | None, gradient_totalobjective: List[float | None] | None, jacobian_localequalityconstraints: List[List[float | None]] | None, jacobian_coordinationequalityconstraints: List[List[float | None]] | None, jacobian_totalequalityconstraints: List[List[float | None]] | None, jacobian_localinequalityconstraints: List[List[float | None]] | None, jacobian_coordinationinequalityconstraints: List[List[float | None]] | None, jacobian_totalinequalityconstraints: List[List[float | None]] | None, jacobian_lowerbounds: List[List[float | None]] | None, jacobian_upperbounds: List[List[float | None]] | None, multipliers_lowerbounds: List[float] | None, multipliers_upperbounds: List[float] | None, multipliers_local_inequality_constraints: List[float] | None, multipliers_local_equality_constraints: List[float] | None, multipliers_coordination_equality_constraints: List[float] | None, multipliers_coordination_inequality_constraints: List[float] | None, activelocalinequalityconstraints: List[bool] | None, activecoordinationinequalityconstraints: List[bool] | None, activelowerbounds: List[bool] | None, activeupperbounds: List[bool] | None, exitflag: int | None, message: str | None, optimization_numberofdesignvariableevaluations: int | None, optimization_runtime: float | None, numberofactiveinequalityconstraints: int | None, numberofactivebounds: int | None) → None"
    Initialize LocalSubSystemOptimData.


    **Args:**
    > optimizer_type: The type of optimizer algorithm used.  
    > designvariables: List of scaled design variable values in [0.0, 1.0].  
    > designvariables_unscaled: List of unscaled design variable values.  
    > Responses_unscaled: List of unscaled physical response values.  
    > localobjectivevalue: The scaled local objective value in [0.0, 1.0].  
    > localobjectivevalue_unscaled: The unscaled local objective value.  
    > totalobjectivevalue: The total objective function value.  
    > coordinationobjectivevalue: The coordination objective value, or None  
    > if not available (e.g., when running Matlab Optimizer).  
    > equalitylocalconstraintsvalue: List of scaled equality local constraint  
    > values in [-0.5, 0.5], or None if not available.  
    > equalitylocalconstraintsvalue_unscaled: List of unscaled equality local  
    > constraint values.  
    > inequalitylocalconstraintsvalue: List of scaled inequality local  
    > constraint values in [-0.5, 0.5], or None if not available.  
    > inequalitylocalconstraintsvalue_unscaled: List of unscaled inequality  
    > local constraint values, or None.  
    > totalconstrainteqvalue: List of total equality constraint values.  
    > totalconstraintineqvalue: List of total inequality constraint values.  
    > coordinationequalityconstraintvalue: List of coordination equality  
    > constraint values, or None if not available.  
    > exitflag: The exit flag indicating optimization convergence status.  
    > message: The optimization result message.  
    > optimization_numberofdesignvariableevaluations: Number of design  
    > variable evaluations during optimization.  
    > optimization_runtime: The runtime of the optimization in seconds.  
    > numberofactiveinequalityconstraints: Number of active inequality  
    > constraints, or None if not available.  
    > numberofactivebounds: Number of active bounds, or None if not available.  
    > lowerbounds: List of lower bound values for the design variables.  
    > lowerbounds_scaled: List of scaled lower bound values.  
    > upperbounds: List of upper bound values for the design variables.  
    > upperbounds_scaled: List of scaled upper bound values.  
    > coordinationinequalityconstraintvalue: List of coordination inequality  
    > constraint values, or None if not available.  
    > couplingparameters: List of coupling parameters objects.  
    > gradient_localobjective: Gradient of the local objective function.  
    > gradient_coordinationobjective: Gradient of the coordination objective.  
    > gradient_totalobjective: Gradient of the total objective function.  
    > jacobian_localequalityconstraints: Jacobian of local equality constraints.  
    > jacobian_coordinationequalityconstraints: Jacobian of coordination  
    > equality constraints.  
    > jacobian_totalequalityconstraints: Jacobian of total equality constraints.  
    > jacobian_localinequalityconstraints: Jacobian of local inequality  
    > constraints.  
    > jacobian_coordinationinequalityconstraints: Jacobian of coordination  
    > inequality constraints.  
    > jacobian_totalinequalityconstraints: Jacobian of total inequality  
    > constraints.  
    > jacobian_lowerbounds: Jacobian of the lower bounds.  
    > jacobian_upperbounds: Jacobian of the upper bounds.  
    > multipliers_lowerbounds: Multipliers for the lower bounds.  
    > multipliers_upperbounds: Multipliers for the upper bounds.  
    > multipliers_local_inequality_constraints: Multipliers for local  
    > inequality constraints.  
    > multipliers_local_equality_constraints: Multipliers for local  
    > equality constraints.  
    > multipliers_coordination_equality_constraints: Multipliers for  
    > coordination equality constraints.  
    > multipliers_coordination_inequality_constraints: Multipliers for  
    > coordination inequality constraints.  
    > activelocalinequalityconstraints: List of bools indicating active  
    > local inequality constraints.  
    > activecoordinationinequalityconstraints: List of bools indicating  
    > active coordination inequality constraints.  
    > activelowerbounds: List of bools indicating active lower bounds.  
    > activeupperbounds: List of bools indicating active upper bounds.  

??? abstract "set_Responses_Unscaled(self, Responses_unscaled_in: List[float]) → None"
    Set the unscaled physical responses.


    **Args:**
    > Responses_unscaled_in: Unscaled physical responses.  

??? abstract "get_Responses_Unscaled(self) → List[float]"
    Get the unscaled response values.


    **Returns:**
    > The unscaled physical response values.  

??? abstract "set_LocalObjectiveValue(self, localobjectivevalue_in: float) → None"
    Set the local objective function value.


    **Args:**
    > localobjectivevalue_in: Local objective function value.  

??? abstract "get_LocalObjectiveValue(self) → float | None"
    Gets the scaled local objective function value.


    **Returns:**
    > The local objective value scaled to [0.0, 1.0], or None if not  
    > available (e.g., when running Matlab Optimizer).  

??? abstract "set_LocalObjectiveValue_Unscaled(self, localobjectivevalue_unscaled_in: float) → None"
    Set the unscaled local objective function value.


    **Args:**
    > localobjectivevalue_unscaled_in: Unscaled local objective function value.  

??? abstract "get_LocalObjectiveValue_Unscaled(self) → float | None"
    Gets the unscaled local objective function value.


    **Returns:**
    > The unscaled local objective value, or None if not available  
    > (e.g., when running Matlab Optimizer).  

??? abstract "set_EqualityLocalConstraintsValue(self, equalitylocalconstraintsvalue_in: List[float]) → None"
    Set the equality local constraint values.


    **Args:**
    > equalitylocalconstraintsvalue_in: Equality local constraint values.  

??? abstract "get_EqualityLocalConstraintsValue(self) → List[float] | None"
    Gets the scaled equality local constraint values.


    **Returns:**
    > List of equality constraint values scaled to [-0.5, 0.5], or None  
    > if not available (e.g., when running Matlab Optimizer).  

??? abstract "set_EqualityLocalConstraintsValue_Unscaled(self, equalitylocalconstraintsvalue_unscaled_in: List[float]) → None"
    Set the unscaled equality local constraint values.


    **Args:**
    > equalitylocalconstraintsvalue_unscaled_in: Unscaled equality local  
    > constraint values.  

??? abstract "set_InequalityLocalConstraintsValue(self, inequalitylocalconstraintsvalue_in: List[float]) → None"
    Set the inequality local constraint values.


    **Args:**
    > inequalitylocalconstraintsvalue_in: Inequality local constraint values.  

??? abstract "get_InequalityLocalConstraintsValue(self) → List[float] | None"
    Gets the scaled inequality local constraint values.


    **Returns:**
    > List of inequality constraint values scaled to [-0.5, 0.5], or None  
    > if not available (e.g., when running Matlab Optimizer).  

??? abstract "set_InequalityLocalConstraintsValue_Unscaled(self, inequalitylocalconstraintsvalue_unscaled_in: List[float]) → None"
    Set the unscaled inequality local constraint values.


    **Args:**
    > inequalitylocalconstraintsvalue_unscaled_in: Unscaled inequality  
    > local constraint values.  

??? abstract "set_Gradient_LocalObjective(self, gradient_localobjective_in: List[float | None]) → None"
    Set the gradient of the local objective.


    **Args:**
    > gradient_localobjective_in: Gradient of the local objective function.  

??? abstract "get_Gradient_LocalObjective(self) → List[float | None] | None"
    Get the gradient of the local objective.


    **Returns:**
    > The gradient of the local objective, or None if not available.  

??? abstract "set_Jacobian_LocalEqualityConstraints(self, jacobian_localequalityconstraints_in: List[List[float | None]]) → None"
    Set the Jacobian of the local equality constraints.


    **Args:**
    > jacobian_localequalityconstraints_in: Jacobian of the local  
    > equality constraints.  

??? abstract "get_Jacobian_LocalEqualityConstraints(self) → List[List[float | None]] | None"
    Get the Jacobian of the local equality constraints.


    **Returns:**
    > The Jacobian of the local equality constraints, or None if not available.  

??? abstract "set_Jacobian_LocalInequalityConstraints(self, jacobian_localinequalityconstraints_in: List[List[float | None]]) → None"
    Set the Jacobian of the local inequality constraints.


    **Args:**
    > jacobian_localinequalityconstraints_in: Jacobian of the local  
    > inequality constraints.  

??? abstract "get_Jacobian_LocalInequalityConstraints(self) → List[List[float | None]] | None"
    Get the Jacobian of the local inequality constraints.


    **Returns:**
    > The Jacobian of the local inequality constraints, or None if not available.  

??? abstract "get_LocalCouplingParameters(self) → List[[SubSysCouplingParametersBasis](../../couplingparameters/SubSysCouplingParametersBasis.md#subsyscouplingparametersbasis)] | None"
    Get the local <-> local coupling parameters (excluding controller couplings).


    **Returns:**
    > List of local coupling parameters, or None if no local <-> local  
    > couplings exist.  

??? abstract "get_CouplingParameter(self, id: str) → [SubSysCouplingParametersBasis](../../couplingparameters/SubSysCouplingParametersBasis.md#subsyscouplingparametersbasis) | None"
    Get the coupling parameter associated with id, if it is a local <-> local coupling.


    **Args:**
    > id: The coupling parameter ID to search for.  


    **Returns:**
    > The coupling parameter matching the ID.  

??? abstract "get_Jacobian_MappedResponse(self, id: str) → List[List[float | None]] | None"
    Get the Jacobian of the mapped responses for the coupling with given ID.


    **Args:**
    > id: The coupling parameter ID.  


    **Returns:**
    > The Jacobian of the mapped responses, or None if not available.  

??? abstract "set_Jacobian_MappedResponses(self, id: str, jacobian_mappedresponses_in: List[List[float | None]]) → None"
    Set the Jacobian of the mapped responses associated with id.


    **Args:**
    > id: The coupling parameter ID.  
    > jacobian_mappedresponses_in: Jacobian of the mapped responses.  

??? abstract "set_Multipliers_Local_Inequality_Constraints(self, multipliers_localinequalityconstraints_in: List[float | None]) → None"
    Set the multipliers for the local inequality constraints.


    **Args:**
    > multipliers_localinequalityconstraints_in: Multipliers for local  
    > inequality constraints.  

??? abstract "get_Multipliers_Local_Inequality_Constraints(self) → List[float | None] | None"
    Get the multipliers for the local inequality constraints.


    **Returns:**
    > Multipliers for local inequality constraints, or None if not set.  

??? abstract "set_Multipliers_Local_Equality_Constraints(self, multipliers_localequalityconstraints_in: List[float | None]) → None"
    Set the multipliers for the local equality constraints.


    **Args:**
    > multipliers_localequalityconstraints_in: Multipliers for local  
    > equality constraints.  

??? abstract "get_Multipliers_Local_Equality_Constraints(self) → List[float | None] | None"
    Get the multipliers for the local equality constraints.


    **Returns:**
    > Multipliers for local equality constraints, or None if not set.  

??? abstract "set_ActiveLocalInequalityConstraints(self, activelocalinequalityconstraints_in: List[bool]) → None"
    Set the list of bools indicating active local inequality constraints.


    **Args:**
    > activelocalinequalityconstraints_in: Active local inequality  
    > constraints.  

??? abstract "get_ActiveLocalInequalityConstraints(self) → List[bool] | None"
    Get the list of bools indicating active local inequality constraints.


    **Returns:**
    > Active local inequality constraints, or None if not available.  

??? abstract "print_results(self) → None"
    Print local subsystem optimizer results.

