---
title: UpdateCouplingParameterMethod_AugLagProximal_MultipliersFixedWeights
---

← Back to [updatecouplingparametermethod](index.md)

# UpdateCouplingParameterMethod_AugLagProximal_MultipliersFixedWeights

**Source:** [Distributed_Design_Optimizer\coordination\updatecouplingparametermethod\UpdateCouplingParameterMethod_AugLagProximal_MultipliersFixedWeights.py](UpdateCouplingParameterMethod_AugLagProximal_MultipliersFixedWeights_source.md)

ALADIN coupling parameter update method.

This module implements the user-specified initialization strategy for all
ALADIN coupling parameters:

- Augmented Lagrangian multipliers and penalty weights (``initialweight``,
``initialmultiplier``): multipliers are updated via the augmented Lagrangian
rule λ_new = λ_old + 2·w²·c(x); weights are held fixed.
- Proximal term parameters ν and Σ^i (``initial_nu``, ``initial_sigma_i``):
the proximal matrix is initialized as ``initial_sigma_i * I`` and the
penalty parameter as ``initial_nu``; both are held fixed across iterations.

## Classes

### UpdateCouplingParameterMethod_AugLagProximal_MultipliersFixedWeights

> **Inherits from:** [UpdateCouplingParameterMethodInterface](UpdateCouplingParameterMethodInterface.md#updatecouplingparametermethodinterface)

> User-specified coupling parameter initialization for ALADIN.

> Combines the augmented Lagrangian multiplier/weight update rule with the
> user-specified initialization of the ALADIN proximal term parameters.

> Multiplier update rule: λ_new = λ_old + 2·w²·c(x)
> Weights: no update (ALADIN does not modify penalty weights)
> Proximal matrix: Σ^i = initial_sigma_i · I (fixed across iterations)
> Proximal penalty: ν = initial_nu (fixed across iterations)


> **Attributes:**
> > _initialweight: Initial value for penalty weights (must be >= 0).  
> > _initialmultiplier: Initial value for Lagrange multipliers.  
> > _initial_nu: Initial value of the proximal penalty parameter ν  
> > (must be > 0).  
> > _initial_sigma_i: Diagonal entry for the initial proximal matrix Σ^i  
> > (must be > 0).  The full matrix is ``initial_sigma_i * I``.

#### Methods

??? abstract "__init__(self, initialweight: float, initialmultiplier: float, initial_nu: float, initial_sigma_i: float) → None"
    Initialize the ALADIN coupling parameter method.


    **Args:**
    > initialweight: Initial value for penalty weights.  
    > Must be >= 0.  
    > initialmultiplier: Initial value for Lagrange multipliers.  
    > initial_nu: Initial value of the proximal penalty parameter ν.  
    > Must be strictly positive.  
    > initial_sigma_i: Diagonal entry of the initial proximal matrix  
    > Σ^i = initial_sigma_i · I.  Must be strictly positive so  
    > that Σ^i is positive definite.  

??? abstract "validate_inputs(self) → None"
    Validate the hyperparameters of this update method.


    **Raises:**
    > ValueError: If any parameter is outside the allowed range.  

??? abstract "get_InitialWeight(self) → float"
    Get the initial penalty weight value.


    **Returns:**
    > The initial penalty weight value.  

??? abstract "get_InitialMultiplier(self) → float"
    Get the initial Lagrange multiplier value.


    **Returns:**
    > The initial Lagrange multiplier value.  

??? abstract "get_Initial_Nu(self) → float"
    Get the initial value of the proximal penalty parameter ν.


    **Returns:**
    > The initial ν value.  

??? abstract "get_Initial_Sigma_i(self) → float"
    Get the diagonal entry of the initial proximal matrix Σ^i.

    The full matrix used during initialization is ``initial_sigma_i * I``.


    **Returns:**
    > The scalar diagonal entry of the initial proximal matrix.  

??? abstract "initialize_ProximalParameters(self, subsystem: Distributed_Design_Optimizer.subsystem.LocalSubSystemALADIN.LocalSubSystemALADIN) → None"
    Push the initial ν and Σ^i onto the subsystem.

    Called once inside
    ``LocalSubSystemALADIN.initializeCouplingParameters_before_CopyToMiddleLevel``
    to replace the hardcoded identity default with the user-specified values.


    **Args:**
    > subsystem: The ALADIN local subsystem to initialize.  

??? abstract "update_CoordinationMultipliers(self, multiplierin: List[float], weightsin: List[float], inconsistencyin: List[float]) → None"
    Update Lagrange multipliers using the augmented Lagrangian rule.

    Update formula: λ_new = λ_old + 2 · w² · c(x)


    **Args:**
    > multiplierin: Current multiplier values to update in place.  
    > weightsin: Current penalty weight values.  
    > inconsistencyin: Current inconsistency values.  

??? abstract "update_CoordinationWeights(self, weightin: List[float]) → None"
    ALADIN does not update penalty weights.


    **Args:**
    > weightin: Current penalty weights.  

??? abstract "update_Proximal_nu(self) → None"
    Proximal penalty parameter ν is held fixed across iterations.

??? abstract "update_Proximal_Sigma_i(self) → None"
    Proximal matrix Σ^i is held fixed across iterations.

??? abstract "print_startup_summary(self) → None"
    Print the coupling parameter configuration at startup.

??? abstract "print_termination_summary(self) → None"
    Print the coupling parameter configuration at the end.

??? abstract "update_state(self, other: [UpdateCouplingParameterMethod_AugLagProximal_MultipliersFixedWeights](UpdateCouplingParameterMethod_AugLagProximal_MultipliersFixedWeights.md#updatecouplingparametermethod_auglagproximal_multipliersfixedweights)) → None"
    Update the state of this instance with values from another instance.

    This method is necessary for multiprocessing.  When subsystems are
    executed in parallel using ``multiprocessing.Pool``, they are
    serialized and deserialized, creating new objects in separate memory
    spaces.  After parallel execution completes, this method updates the
    original object's attribute values.


    **Args:**
    > other: The source instance containing updated values from  
    > parallel execution.  

