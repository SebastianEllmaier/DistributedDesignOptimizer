---
title: Local_ConvergenceIndicator_Outerloop_DeWit
---

← Back to [DeWit](index.md)

# Local_ConvergenceIndicator_Outerloop_DeWit

**Source:** [Distributed_Design_Optimizer\coordination\convergence\DeWit\Local_ConvergenceIndicator_Outerloop_DeWit.py](Local_ConvergenceIndicator_Outerloop_DeWit_source.md)

DeWit local outer loop convergence indicator.

Evaluates outer loop convergence at the subsystem level by checking that
all inconsistencies and coupling parameter changes are within tolerance.

## Classes

### Local_ConvergenceIndicator_Outerloop_DeWit

> **Inherits from:** [Local_ConvergenceIndicator_Outerloop_Interface](../Local_ConvergenceIndicator_Outerloop_Interface.md#local_convergenceindicator_outerloop_interface)

> Local outer loop convergence indicator - DeWit.

> Evaluates outer loop convergence at the subsystem level by checking that
> all inconsistencies and coupling parameter changes are within tolerance.
> Each subsystem has its own instance of this class.


> **Attributes:**
> > _toleranceconsistency: Tolerance for consistency constraints and coupling changes.

#### Methods

??? abstract "__init__(self, toleranceconsistency: float) → None"
    Initialize the local DeWit outer loop convergence indicator.


    **Args:**
    > toleranceconsistency: Tolerance for consistency constraints.  

??? abstract "evaluate(self, subsystem: [LocalSubSystemBasis](../../../subsystem/LocalSubSystemBasis.md#localsubsystembasis)) → bool"
    Evaluate if local outer loop convergence criteria is met.

    Checks that all inconsistencies and coupling parameter changes
    are within the specified tolerance.


    **Args:**
    > subsystem: The subsystem to evaluate convergence for.  


    **Returns:**
    > bool: True if convergence condition is met, False otherwise.  

??? abstract "check_inconsistencies(self, inconsistencies: List[[InConsistencySizeInterface](../../../middlelevel/InConsistencySizeInterface.md#inconsistencysizeinterface)]) → bool"
    Check if all inconsistencies are within tolerance.


    **Args:**
    > inconsistencies: List of inconsistency size objects.  


    **Returns:**
    > bool: True if all inconsistencies are within tolerance.  

??? abstract "check_coupling_reduction(self, couplingNew: List[[SubSysCouplingParametersBasis](../../../subsystem/couplingparameters/SubSysCouplingParametersBasis.md#subsyscouplingparametersbasis)], couplingOld: List[[SubSysCouplingParametersBasis](../../../subsystem/couplingparameters/SubSysCouplingParametersBasis.md#subsyscouplingparametersbasis)]) → bool"
    Check if the coupling variable reduction is within tolerance.


    **Args:**
    > couplingNew: Current coupling parameters.  
    > couplingOld: Previous coupling parameters.  


    **Returns:**
    > bool: True if reduction is within tolerance.  

??? abstract "get_ToleranceConsistency(self) → float"
    Get the tolerance for consistency convergence.


    **Returns:**
    > The consistency tolerance threshold value.  

??? abstract "update_state(self, other: [Local_ConvergenceIndicator_Outerloop_DeWit](Local_ConvergenceIndicator_Outerloop_DeWit.md#local_convergenceindicator_outerloop_dewit)) → None"
    Update the state of this convergence indicator with the state of another.


    **Args:**
    > other: The convergence indicator to copy state from.  

