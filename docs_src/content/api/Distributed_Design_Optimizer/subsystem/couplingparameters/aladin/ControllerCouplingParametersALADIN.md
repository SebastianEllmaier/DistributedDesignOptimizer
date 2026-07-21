---
title: ControllerCouplingParametersALADIN
---

← Back to [aladin](index.md)

# ControllerCouplingParametersALADIN

**Source:** [Distributed_Design_Optimizer\subsystem\couplingparameters\aladin\ControllerCouplingParametersALADIN.py](ControllerCouplingParametersALADIN_source.md)

ALADIN controller coupling parameters module.

This module provides coupling parameters for the ALADIN
controller subsystem.

## Classes

### ControllerCouplingParametersALADIN

> **Inherits from:** [ControllerCouplingParametersBasis](../ControllerCouplingParametersBasis.md#controllercouplingparametersbasis)

> Coupling parameters for the ALADIN controller subsystem.

> Extends ControllerCouplingParametersBasis with delta_d, d_hat, Hessians,
> gradients, Jacobians of active constraints/bounds, equality constraints,
> and per-coupling local-to-controller / controller-to-local sub-parameters.

#### Methods

??? abstract "__init__(self, id: str) → None"
    Initialize ControllerCouplingParametersALADIN.


    **Args:**
    > id: Identifier of the neighboring subsystem.  

??? abstract "set_Delta_D(self, delta_d_in: List[float]) → None"
    Set the delta_d variables.


    **Args:**
    > delta_d_in: The delta_d variables to set.  

??? abstract "get_Delta_D(self) → List[float] | None"
    Get the delta_d variables.


    **Returns:**
    > The delta_d variables, or None if not set.  

??? abstract "set_Copy_Hessian_LocalConstraints_Lagrangian(self, copy_hessian_localconstraints_lagrangian_in: List[List[float]]) → None"
    Set the copy of the Hessian of the Lagrangian w.r.t. local constraints.


    **Args:**
    > copy_hessian_localconstraints_lagrangian_in: The copy of the Hessian to set.  

??? abstract "get_Copy_Hessian_LocalConstraints_Lagrangian(self) → List[List[float]] | None"
    Get the copy of the Hessian of the Lagrangian w.r.t. local constraints.


    **Returns:**
    > The copy of the Hessian of the Lagrangian, or None if not set.  

??? abstract "set_Copy_Gradient_LocalObjective(self, copy_gradient_localobjective_in: List[float]) → None"
    Set the copy of the gradient of the local objective function.


    **Args:**
    > copy_gradient_localobjective_in: The copy of the gradient to set.  

??? abstract "get_Copy_Gradient_LocalObjective(self) → List[float] | None"
    Get the copy of the gradient of the local objective function.


    **Returns:**
    > The copy of the gradient of the local objective function, or None if not set.  

??? abstract "set_Copy_LocalInequalityConstraintsValue(self, copy_localinequalityconstraintsvalue_in: List[float]) → None"
    Set the copy of the local inequality constraint values.


    **Args:**
    > copy_localinequalityconstraintsvalue_in: The copy of the local inequality constraint values to set.  

??? abstract "get_Copy_LocalInequalityConstraintsValue(self) → List[float] | None"
    Get the copy of the local inequality constraint values.


    **Returns:**
    > The copy of the local inequality constraint values, or None if not set.  

??? abstract "set_Copy_Jacobian_LocalInequalityConstraints(self, copy_jacobian_localinequalityconstraints_in: List[List[float]]) → None"
    Set the copy of the Jacobian of the local inequality constraints.


    **Args:**
    > copy_jacobian_localinequalityconstraints_in: The copy of the Jacobian to set.  

??? abstract "get_Copy_Jacobian_LocalInequalityConstraints(self) → List[List[float]] | None"
    Get the copy of the Jacobian of the local inequality constraints.


    **Returns:**
    > The copy of the Jacobian of the local inequality constraints, or None if not set.  

??? abstract "set_Copy_Lower_BoundConstraints_Value(self, copy_lower_boundconstraints_value_in: List[float]) → None"
    Set the copy of the lower bound constraint values.


    **Args:**
    > copy_lower_boundconstraints_value_in: The copy of the lower bound constraint values to set.  

??? abstract "get_Copy_Lower_BoundConstraints_Value(self) → List[float] | None"
    Get the copy of the lower bound constraint values.


    **Returns:**
    > The copy of the lower bound constraint values, or None if not set.  

??? abstract "set_Copy_Jacobian_LowerBound(self, copy_jacobian_lowerbound_in: List[List[float]]) → None"
    Set the copy of the Jacobian of the lower bounds of the subsystem's design variables.


    **Args:**
    > copy_jacobian_lowerbound_in: The copy of the Jacobian to set.  

??? abstract "get_Copy_Jacobian_LowerBound(self) → List[List[float]] | None"
    Get the copy of the Jacobian of the lower bounds of the subsystem's design variables.


    **Returns:**
    > The copy of the Jacobian of the lower bounds, or None if not set.  

??? abstract "set_Copy_Upper_BoundConstraints_Value(self, copy_upper_boundconstraints_value_in: List[float]) → None"
    Set the copy of the upper bound constraint values.


    **Args:**
    > copy_upper_boundconstraints_value_in: The copy of the upper bound constraint values to set.  

??? abstract "get_Copy_Upper_BoundConstraints_Value(self) → List[float] | None"
    Get the copy of the upper bound constraint values.


    **Returns:**
    > The copy of the upper bound constraint values, or None if not set.  

??? abstract "set_Copy_Jacobian_UpperBound(self, copy_jacobian_upperbound_in: List[List[float]]) → None"
    Set the copy of the Jacobian of the upper bounds of the subsystem's design variables.


    **Args:**
    > copy_jacobian_upperbound_in: The copy of the Jacobian to set.  

??? abstract "get_Copy_Jacobian_UpperBound(self) → List[List[float]] | None"
    Get the copy of the Jacobian of the upper bounds of the subsystem's design variables.


    **Returns:**
    > The copy of the Jacobian of the upper bounds, or None if not set.  

??? abstract "set_Copy_Jacobian_LocalEqualityConstraints(self, copy_jacobian_equalityconstraints_in: List[List[float]]) → None"
    Set the copy of the Jacobian of the equality constraints.


    **Args:**
    > copy_jacobian_equalityconstraints_in: The copy of the Jacobian to set.  

??? abstract "get_Copy_Jacobian_LocalEqualityConstraints(self) → List[List[float]] | None"
    Get the copy of the Jacobian of the equality constraints.


    **Returns:**
    > The copy of the Jacobian of the equality constraints, or None if not set.  

??? abstract "set_Copy_LocalToLocalForController_CouplingParameters(self, copy_localtolocalforcontroller_couplingparametersin: List[[LocalToLocalForController_CouplingParameters](LocalToLocalForController_CouplingParameters.md#localtolocalforcontroller_couplingparameters)]) → None"
    Set the copy of the local-to-local-for-controller coupling parameters for each i <-> j coupling.


    **Args:**
    > copy_localtolocalforcontroller_couplingparametersin: The copy of the local-to-local-for-controller coupling parameters to set.  

??? abstract "get_Copy_LocalToLocalForController_CouplingParameters(self) → List[[LocalToLocalForController_CouplingParameters](LocalToLocalForController_CouplingParameters.md#localtolocalforcontroller_couplingparameters)] | None"
    Get the copy of the local-to-local-for-controller coupling parameters for each i <-> j coupling.


    **Returns:**
    > The copy of the local-to-local-for-controller coupling parameters, or None if not set.  

??? abstract "CopyFromMiddleLevel_LocalToLocalForController_CouplingParameters(self, copy_localtolocalforcontroller_couplingparameter: [LocalToLocalForController_CouplingParameters](LocalToLocalForController_CouplingParameters.md#localtolocalforcontroller_couplingparameters), middlelevel_localtolocalforcontroller_couplingparameter: [LocalToLocalForController_CouplingParameters](LocalToLocalForController_CouplingParameters.md#localtolocalforcontroller_couplingparameters)) → None"
    Update a local-to-local-for-controller coupling parameter from the middlelevel coupling.


    **Args:**
    > copy_localtolocalforcontroller_couplingparameter: The local copy to update.  
    > middlelevel_localtolocalforcontroller_couplingparameter: The middle level coupling parameter source.  

??? abstract "CopyFromMiddleLevelCoupling(self, middlelevelcouplingIn: [LocalToController_MiddleLevelCouplingALADIN](../../../middlelevel/aladin/LocalToController_MiddleLevelCouplingALADIN.md#localtocontroller_middlelevelcouplingaladin)) → None"
    Copy coupling parameters from the middle level.


    **Args:**
    > middlelevelcouplingIn: The middle level coupling to copy from.  


    **Raises:**
    > ValueError: If middlelevelcouplingIn is not a LocalToController_MiddleLevelCouplingALADIN instance.  

??? abstract "CopyToMiddleLevelCoupling(self, middlelevelcouplingIn: [ControllerToLocal_MiddleLevelCouplingALADIN](../../../middlelevel/aladin/ControllerToLocal_MiddleLevelCouplingALADIN.md#controllertolocal_middlelevelcouplingaladin)) → None"
    Copy coupling parameters to the middle level.


    **Args:**
    > middlelevelcouplingIn: The middle level coupling to copy to.  


    **Raises:**
    > ValueError: If middlelevelcouplingIn is not a ControllerToLocal_MiddleLevelCouplingALADIN instance.  

??? abstract "update_state(self, other_coupling: [ControllerCouplingParametersALADIN](ControllerCouplingParametersALADIN.md#controllercouplingparametersaladin)) → None"
    Update the state of this ControllerCouplingParametersALADIN with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.

    The update preserves memory addresses by modifying list contents in-place rather than
    reassigning references. This is essential for maintaining object identity across the
    multiprocessing boundary.


    **Args:**
    > other_coupling: The source ControllerCouplingParametersALADIN containing updated values  
    > from parallel execution.  

