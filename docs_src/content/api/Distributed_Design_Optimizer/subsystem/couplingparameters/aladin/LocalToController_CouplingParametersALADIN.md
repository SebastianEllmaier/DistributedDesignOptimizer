---
title: LocalToController_CouplingParametersALADIN
---

← Back to [aladin](index.md)

# LocalToController_CouplingParametersALADIN

**Source:** [Distributed_Design_Optimizer\subsystem\couplingparameters\aladin\LocalToController_CouplingParametersALADIN.py](LocalToController_CouplingParametersALADIN_source.md)

Local -> Controller coupling parameters module.

This module provides coupling parameters for the local subsystems
regarding data communicated to ALADIN controller subsystem.

## Classes

### LocalToController_CouplingParametersALADIN

> **Inherits from:** [LocalToController_CouplingParametersBasis](../LocalToController_CouplingParametersBasis.md#localtocontroller_couplingparametersbasis)

> Coupling parameters for the ALADIN controller subsystem.

> Extends LocalToController_CouplingParametersBasis with delta_d, d_hat, Hessians,
> gradients, Jacobians of active constraints/bounds, equality constraints,
> and per-coupling local-to-controller / controller-to-local sub-parameters.

#### Methods

??? abstract "__init__(self) → None"
    Initialize LocalToController_CouplingParametersALADIN.

??? abstract "set_Copy_Delta_D(self, copy_delta_d_in: List[float]) → None"
    Set the copy of the delta_d variables.


    **Args:**
    > copy_delta_d_in: The copy of the delta_d variables to set.  

??? abstract "get_Copy_Delta_D(self) → List[float] | None"
    Get the copy of the delta_d variables.


    **Returns:**
    > The copy of the delta_d variables, or None if not set.  

??? abstract "set_D_hat(self, d_hat_in: List[float]) → None"
    Set the d_hat variables.


    **Args:**
    > d_hat_in: The d_hat variables to set.  

??? abstract "get_D_hat(self) → List[float] | None"
    Get the d_hat variables.


    **Returns:**
    > The d_hat variables, or None if not set.  

??? abstract "set_Hessian_LocalConstraints_Lagrangian(self, hessian_localconstraints_lagrangian_in: List[List[float]]) → None"
    Set the Hessian of the Lagrangian w.r.t. local constraints needed for the controller QP problem.


    **Args:**
    > hessian_localconstraints_lagrangian_in: The Hessian to set.  

??? abstract "get_Hessian_LocalConstraints_Lagrangian(self) → List[List[float]] | None"
    Get the Hessian of the Lagrangian w.r.t. local constraints needed for the controller QP problem.


    **Returns:**
    > The Hessian of the Lagrangian w.r.t. local constraints, or None if not set.  

??? abstract "set_Gradient_LocalObjective(self, gradient_localobjective_in: List[float]) → None"
    Set the gradient of the local objective function.


    **Args:**
    > gradient_localobjective_in: The gradient of the local objective function to set.  

??? abstract "get_Gradient_LocalObjective(self) → List[float] | None"
    Get the gradient of the local objective function.


    **Returns:**
    > The gradient of the local objective function, or None if not set.  

??? abstract "set_LocalInequalityConstraintsValue(self, localinequalityconstraintsvalue_in: List[float]) → None"
    Set the local inequality constraint values.


    **Args:**
    > localinequalityconstraintsvalue_in: The local inequality constraint values to set.  

??? abstract "get_LocalInequalityConstraintsValue(self) → List[float] | None"
    Get the local inequality constraint values.


    **Returns:**
    > The local inequality constraint values, or None if not set.  

??? abstract "set_Lower_BoundConstraints_Value(self, lower_boundconstraints_value_in: List[float]) → None"
    Set the lower bound constraint values.


    **Args:**
    > lower_boundconstraints_value_in: The lower bound constraint values to set.  

??? abstract "get_Lower_BoundConstraints_Value(self) → List[float] | None"
    Get the lower bound constraint values.


    **Returns:**
    > The lower bound constraint values, or None if not set.  

??? abstract "set_Upper_BoundConstraints_Value(self, upper_boundconstraints_value_in: List[float]) → None"
    Set the upper bound constraint values.


    **Args:**
    > upper_boundconstraints_value_in: The upper bound constraint values to set.  

??? abstract "get_Upper_BoundConstraints_Value(self) → List[float] | None"
    Get the upper bound constraint values.


    **Returns:**
    > The upper bound constraint values, or None if not set.  

??? abstract "set_Jacobian_LocalInequalityConstraints(self, jacobian_localinequalityconstraints_in: List[List[float]]) → None"
    Set the Jacobian of the local inequality constraints.


    **Args:**
    > jacobian_localinequalityconstraints_in: The Jacobian to set.  

??? abstract "get_Jacobian_LocalInequalityConstraints(self) → List[List[float]] | None"
    Get the Jacobian of the local inequality constraints.


    **Returns:**
    > The Jacobian of the local inequality constraints, or None if not set.  

??? abstract "set_Jacobian_LowerBound(self, jacobian_lowerbound_in: List[List[float]]) → None"
    Set the Jacobian of the lower bounds of the subsystem's design variables.


    **Args:**
    > jacobian_lowerbound_in: The Jacobian of the lower bounds to set.  

??? abstract "get_Jacobian_LowerBound(self) → List[List[float]] | None"
    Get the Jacobian of the lower bounds of the subsystem's design variables.


    **Returns:**
    > The Jacobian of the lower bounds, or None if not set.  

??? abstract "set_Jacobian_UpperBound(self, jacobian_upperbound_in: List[List[float]]) → None"
    Set the Jacobian of the upper bounds of the subsystem's design variables.


    **Args:**
    > jacobian_upperbound_in: The Jacobian of the upper bounds to set.  

??? abstract "get_Jacobian_UpperBound(self) → List[List[float]] | None"
    Get the Jacobian of the upper bounds of the subsystem's design variables.


    **Returns:**
    > The Jacobian of the upper bounds, or None if not set.  

??? abstract "set_Jacobian_LocalEqualityConstraints(self, jacobian_equalityconstraints_in: List[List[float]]) → None"
    Set the Jacobian of the equality constraints.


    **Args:**
    > jacobian_equalityconstraints_in: The Jacobian of the equality constraints to set.  

??? abstract "get_Jacobian_LocalEqualityConstraints(self) → List[List[float]] | None"
    Get the Jacobian of the equality constraints.


    **Returns:**
    > The Jacobian of the equality constraints, or None if not set.  

??? abstract "set_LocalToLocalForController_CouplingParameters(self, localtocontroller_couplingparametersin: List[[LocalToLocalForController_CouplingParameters](LocalToLocalForController_CouplingParameters.md#localtolocalforcontroller_couplingparameters)]) → None"
    Set the local-to-controller coupling parameters for each i <-> j coupling.


    **Args:**
    > localtocontroller_couplingparametersin: The list of local-to-controller coupling parameters to set.  

??? abstract "get_LocalToLocalForController_CouplingParameters(self) → List[[LocalToLocalForController_CouplingParameters](LocalToLocalForController_CouplingParameters.md#localtolocalforcontroller_couplingparameters)] | None"
    Get the local-to-controller coupling parameters for each i <-> j coupling.


    **Returns:**
    > The local-to-controller coupling parameters, or None if not set.  

??? abstract "CopyToMiddleLevel_LocalToLocalForController_CouplingParameters(self, localtocontroller_couplingparameter: [LocalToLocalForController_CouplingParameters](LocalToLocalForController_CouplingParameters.md#localtolocalforcontroller_couplingparameters), middlelevel_localtocontroller_couplingparameter: [LocalToLocalForController_CouplingParameters](LocalToLocalForController_CouplingParameters.md#localtolocalforcontroller_couplingparameters)) → None"
    Update a local-to-controller coupling parameter in the middlelevel coupling.


    **Args:**
    > localtocontroller_couplingparameter: The source local-to-controller coupling parameter.  
    > middlelevel_localtocontroller_couplingparameter: The middle level coupling parameter to update.  

??? abstract "CopyFromMiddleLevelCoupling(self, middlelevelcouplingIn: [ControllerToLocal_MiddleLevelCouplingALADIN](../../../middlelevel/aladin/ControllerToLocal_MiddleLevelCouplingALADIN.md#controllertolocal_middlelevelcouplingaladin)) → None"
    Copy coupling parameters from the middle level.


    **Args:**
    > middlelevelcouplingIn: The middle level coupling to copy from.  


    **Raises:**
    > ValueError: If middlelevelcouplingIn is not a ControllerToLocal or LocalToController MiddleLevelCouplingALADIN instance.  

??? abstract "CopyToMiddleLevelCoupling(self, middlelevelcouplingIn: [LocalToController_MiddleLevelCouplingALADIN](../../../middlelevel/aladin/LocalToController_MiddleLevelCouplingALADIN.md#localtocontroller_middlelevelcouplingaladin)) → None"
    Copy coupling parameters to the middle level.


    **Args:**
    > middlelevelcouplingIn: The middle level coupling to copy to.  


    **Raises:**
    > ValueError: If middlelevelcouplingIn is not a LocalToController or ControllerToLocal MiddleLevelCouplingALADIN instance.  

??? abstract "update_state(self, other_coupling: [LocalToController_CouplingParametersALADIN](LocalToController_CouplingParametersALADIN.md#localtocontroller_couplingparametersaladin)) → None"
    Update the state of this LocalToController_CouplingParametersALADIN with values from another instance.

    This method is necessary for multiprocessing. When subsystems are executed in parallel
    using multiprocessing.Pool, they are serialized and deserialized, creating new objects
    in separate memory spaces. After parallel execution completes, this method updates
    the original object's attribute values while preserving their memory addresses.

    The update preserves memory addresses by modifying list contents in-place rather than
    reassigning references. This is essential for maintaining object identity across the
    multiprocessing boundary.


    **Args:**
    > other_coupling: The source LocalToController_CouplingParametersALADIN containing updated values  
    > from parallel execution.  

