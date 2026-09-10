---
title: CouplingStrengthComputer (Source)
---

← Back to [CouplingStrengthComputer documentation](CouplingStrengthComputer.md)

# CouplingStrengthComputer - Source Code

**File:** `Distributed_Design_Optimizer\postprocess\CouplingStrengthComputer.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Coupling strength computation module.

This module provides functionality for computing coupling strength
metrics between subsystems in distributed optimization.
"""

from typing import List, Dict, Tuple
from Distributed_Design_Optimizer.postprocess import GraphInit
from Distributed_Design_Optimizer.subsystem import SubSystemInterface
from Distributed_Design_Optimizer.subsystem.couplingparameters import CouplingParametersInterface
from Distributed_Design_Optimizer.subsystem.optimization import OptimizationBasis



class CouplingStrengthComputer:
    
    """
    Compute coupling strength between subsystems.
    """
    
    def __init__(self, graph_init: GraphInit, subsystems: List[SubSystemInterface]):
        """Initialize the CouplingStrengthComputer with graph and subsystems.

        Args:
            graph_init: GraphInit instance containing the mastergraph.
            subsystems: List of SubSystemInterface objects.
        """
        self._graph_init: GraphInit = graph_init
        self._mastergraph = graph_init.get_graph()
        self._subsystems: List[SubSystemInterface] = subsystems
        self._partialcouplingstrength_ignoredcoupling: Dict[tuple, float] = {}
        self._couplingstrengths: Dict[Tuple[str, str], float] = {}
        
    
    def execute(self) -> None:
        """Execute the coupling strength computation.

        This method calculates coupling strengths by temporarily ignoring
        each coupling and measuring the impact on the objective function.
        """

        # --- First Pass: Calculate objective functions with ignored couplings ---
        for subsystem in self._subsystems:
            subsystem_id = subsystem.get_SUBSYSTEMID()
            original_optimdata = subsystem.get_OptimData()
            original_objective_value = original_optimdata.get_LocalObjectiveValue()
            couplingparams: List[CouplingParametersInterface] = subsystem.get_CouplingParameters()
            
            for coupling_param in couplingparams:
                neighbor_id = coupling_param.get_ID()
                
                # Temporarily ignore the coupling and re-run optimization
                subsystem.set_Ignore_CouplingID_for_CoordinationObjective(neighbor_id)
                subsystem.run_IterativeOptimization()
                
                # Store the objective value when this coupling is ignored
                optimdata_with_ignore = subsystem.get_OptimData()
                self._partialcouplingstrength_ignoredcoupling[(subsystem_id, neighbor_id)] = abs(original_objective_value - optimdata_with_ignore.get_LocalObjectiveValue())
                
                # Reset the ignored coupling for the next iteration
                subsystem.set_Ignore_CouplingID_for_CoordinationObjective(None)
                
                # update subsystem with original optim data
                # OptimizationBasis.updateSubsystemFromOptimdata(subsystem, original_optimdata)
                subsystem.updateSubsystemfromOptimdata(original_optimdata)
                
                
        for subsystem in self._subsystems:
            subsystem_id = subsystem.get_SUBSYSTEMID()
            couplingparams: List[CouplingParametersInterface] = subsystem.get_CouplingParameters()

            for j, coupling_param in enumerate(couplingparams):
                neighbor_id = coupling_param.get_ID()

                # Get objective value of current subsystem when ignoring the neighbor
                obj_A_ignoring_B = self._partialcouplingstrength_ignoredcoupling.get((subsystem_id, neighbor_id), None)
                
                # Get objective value of the neighbor subsystem when ignoring the current one
                obj_B_ignoring_A = self._partialcouplingstrength_ignoredcoupling.get((neighbor_id, subsystem_id), None)
                
                # aggregated objective value when couplings between A and B are ignored
                coupling_strength = (obj_A_ignoring_B + obj_B_ignoring_A) / 2.0
                
                couplingparams[j].set_CouplingStrength(coupling_strength)
                
                # store the coupling strength
                sorted_ids = tuple(sorted((subsystem_id, neighbor_id)))
                self._couplingstrengths[sorted_ids] = coupling_strength
                
                
    def get_couplingstrength(self) -> Dict[Tuple[str, str], float]:
        """
        Returns the calculated symmetric coupling strengths.

        Returns:
            A dictionary where keys are sorted tuples of subsystem IDs and
            values are the calculated coupling strengths.
        """
        return self._couplingstrengths
                
         
                
    

                

                
        
        
```
