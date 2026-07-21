---
title: LocalToController_MiddleLevelCouplingALADIN
---

← Back to [aladin](index.md)

# LocalToController_MiddleLevelCouplingALADIN

**Source:** [Distributed_Design_Optimizer\middlelevel\aladin\LocalToController_MiddleLevelCouplingALADIN.py](LocalToController_MiddleLevelCouplingALADIN_source.md)

Local-to-controller middle-level coupling module for ALADIN.

This module provides middle-level coupling management for local-to-controller
subsystem communication in ALADIN coordination.

## Classes

### LocalToController_MiddleLevelCouplingALADIN

> **Inherits from:** [LocalToController_MiddleLevelCouplingBasis](../LocalToController_MiddleLevelCouplingBasis.md#localtocontroller_middlelevelcouplingbasis)

> Middle level coupling updated by the local subsystem.

> Handles the coupling between local subsystems and the controller
> (middlelevel between local subsystem and controller).

#### Methods

??? abstract "__init__(self, id: str, local_neighbors_list: List[str]) → None"
    Initialize local-to-controller middle-level coupling.


    **Args:**
    > id: Identifier for this coupling.  
    > local_neighbors_list: List of local neighbor identifiers.  

??? abstract "get_Hessian_LocalConstraints_Lagrangian(self) → List[List[float]] | None"
    Return the Hessian of the Lagrangian w.r.t. local constraints.

    Needed for the controller QP problem.


    **Returns:**
    > List[List[float]] | None: The Hessian matrix or None if not set.  

??? abstract "set_Hessian_LocalConstraints_Lagrangian(self, hessian_localconstraintslagrangian_in: List[List[float]]) → None"
    Set the Hessian of the Lagrangian w.r.t. local constraints.

    Needed for the controller QP problem.


    **Args:**
    > hessian_localconstraintslagrangian_in (List[List[float]]): The Hessian matrix to set.  

??? abstract "get_Gradient_LocalObjective(self) → List[float] | None"
    Return the gradient of the local objective function.


    **Returns:**
    > List[float] | None: The gradient vector or None if not set.  

??? abstract "set_Gradient_LocalObjective(self, gradient_localobjective_in: List[float]) → None"
    Set the gradient of the local objective function.


    **Args:**
    > gradient_localobjective_in (List[float]): The gradient vector to set.  

??? abstract "get_LocalInequalityConstraintsValue(self) → List[float] | None"
    Return the local inequality constraint values.


    **Returns:**
    > List[float] | None: The local inequality constraint values or None if not set.  

??? abstract "set_LocalInequalityConstraintsValue(self, localinequalityconstraintvalues_in: List[float]) → None"
    Set the local inequality constraint values.


    **Args:**
    > localinequalityconstraintvalues_in (List[float]): The local inequality constraint values to set.  

??? abstract "get_Jacobian_LocalInequalityConstraints(self) → List[List[float]] | None"
    Return the Jacobian of the local inequality constraints.


    **Returns:**
    > List[List[float]] | None: The Jacobian matrix or None if not set.  

??? abstract "set_Jacobian_LocalInequalityConstraints(self, jacobian_localinequalityconstraints_in: List[List[float]]) → None"
    Set the Jacobian of the local inequality constraints.


    **Args:**
    > jacobian_localinequalityconstraints_in (List[List[float]]): The Jacobian matrix to set.  

??? abstract "get_Lower_BoundConstraints_Value(self) → List[float] | None"
    Return the lower bound constraint values.


    **Returns:**
    > List[float] | None: The lower bound constraint values or None if not set.  

??? abstract "set_Lower_BoundConstraints_Value(self, lower_boundconstraints_value_in: List[float]) → None"
    Set the lower bound constraint values.


    **Args:**
    > lower_boundconstraints_value_in (List[float]): The lower bound constraint values to set.  

??? abstract "get_Jacobian_LowerBound(self) → List[List[float]] | None"
    Return the Jacobian of the lower bounds.


    **Returns:**
    > List[List[float]] | None: The Jacobian matrix or None if not set.  

??? abstract "set_Jacobian_LowerBound(self, jacobian_lowerbound_in: List[List[float]]) → None"
    Set the Jacobian of the lower bounds.


    **Args:**
    > jacobian_lowerbound_in (List[List[float]]): The Jacobian matrix to set.  

??? abstract "get_Upper_BoundConstraints_Value(self) → List[float] | None"
    Return the upper bound constraint values.


    **Returns:**
    > List[float] | None: The upper bound constraint values or None if not set.  

??? abstract "set_Upper_BoundConstraints_Value(self, upper_boundconstraints_value_in: List[float]) → None"
    Set the upper bound constraint values.


    **Args:**
    > upper_boundconstraints_value_in (List[float]): The upper bound constraint values to set.  

??? abstract "get_Jacobian_UpperBound(self) → List[List[float]] | None"
    Return the Jacobian of the upper bounds.


    **Returns:**
    > List[List[float]] | None: The Jacobian matrix or None if not set.  

??? abstract "set_Jacobian_UpperBound(self, jacobian_upperbound_in: List[List[float]]) → None"
    Set the Jacobian of the upper bounds.


    **Args:**
    > jacobian_upperbound_in (List[List[float]]): The Jacobian matrix to set.  

??? abstract "get_Jacobian_LocalEqualityConstraints(self) → List[List[float]] | None"
    Return the Jacobian of the equality constraints.


    **Returns:**
    > List[List[float]] | None: The Jacobian matrix or None if not set.  

??? abstract "set_Jacobian_LocalEqualityConstraints(self, jacobian_equalityconstraints_in: List[List[float]]) → None"
    Set the Jacobian of the equality constraints.


    **Args:**
    > jacobian_equalityconstraints_in (List[List[float]]): The Jacobian matrix to set.  

??? abstract "get_LocalToLocalForController_CouplingParameters(self) → List[[LocalToLocalForController_CouplingParameters](../../subsystem/couplingparameters/aladin/LocalToLocalForController_CouplingParameters.md#localtolocalforcontroller_couplingparameters)]"
    Return the list of LocalToLocalForController_CouplingParameters.

    Returns all coupling parameters for each i <-> j coupling.


    **Returns:**
    > List[LocalToLocalForController_CouplingParameters]: The coupling parameters list.  

??? abstract "set_LocalToLocalForController_CouplingParameters(self, localtolocalforcontroller_couplingparametersin: List[[LocalToLocalForController_CouplingParameters](../../subsystem/couplingparameters/aladin/LocalToLocalForController_CouplingParameters.md#localtolocalforcontroller_couplingparameters)]) → None"
    Set the list of LocalToLocalForController_CouplingParameters.

    Sets all coupling parameters for each i <-> j coupling.


    **Args:**
    > localtolocalforcontroller_couplingparametersin (List[LocalToLocalForController_CouplingParameters]): The coupling parameters list to set.  

??? abstract "update_state(self, other_middlelevelcoupling: [LocalToController_MiddleLevelCouplingALADIN](LocalToController_MiddleLevelCouplingALADIN.md#localtocontroller_middlelevelcouplingaladin)) → None"
    Update the state of this LocalToController_MiddleLevelCouplingALADIN with another instance.

    This method updates the numerical information stored in the class's attributes
    without changing the original memory address location. This is necessary for
    multiprocessing, where executed subsystems return from separate processes and
    their state must be transferred back to the original objects in the main process.


    **Args:**
    > other_middlelevelcoupling: The source instance to copy state from.  

