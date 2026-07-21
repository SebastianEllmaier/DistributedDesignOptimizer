---
title: CouplingStrengthComputer
---

← Back to [postprocess](index.md)

# CouplingStrengthComputer

**Source:** [Distributed_Design_Optimizer\postprocess\CouplingStrengthComputer.py](CouplingStrengthComputer_source.md)

Coupling strength computation module.

This module provides functionality for computing coupling strength
metrics between subsystems in distributed optimization.

## Classes

### CouplingStrengthComputer

> Compute coupling strength between subsystems.

#### Methods

??? abstract "__init__(self, graph_init: [GraphInit](GraphInit.md#graphinit), subsystems: List[[SubSystemInterface](../subsystem/SubSystemInterface.md#subsysteminterface)])"
    Initialize the CouplingStrengthComputer with graph and subsystems.


    **Args:**
    > graph_init: GraphInit instance containing the mastergraph.  
    > subsystems: List of SubSystemInterface objects.  

??? abstract "execute(self) → None"
    Execute the coupling strength computation.

    This method calculates coupling strengths by temporarily ignoring
    each coupling and measuring the impact on the objective function.

??? abstract "get_couplingstrength(self) → Dict[Tuple[str, str], float]"
    Returns the calculated symmetric coupling strengths.


    **Returns:**
    > A dictionary where keys are sorted tuples of subsystem IDs and  
    > values are the calculated coupling strengths.  

