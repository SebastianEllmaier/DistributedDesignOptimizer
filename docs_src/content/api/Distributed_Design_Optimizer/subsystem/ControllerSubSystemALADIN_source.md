---
title: ControllerSubSystemALADIN (Source)
---

← Back to [ControllerSubSystemALADIN documentation](ControllerSubSystemALADIN.md)

# ControllerSubSystemALADIN - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\ControllerSubSystemALADIN.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""ALADIN controller subsystem module.

This module provides the controller subsystem implementation for the
ALADIN coordination method.
"""

from typing import List, Tuple, Dict
import copy
import numpy as np
from scipy.linalg import block_diag
from Distributed_Design_Optimizer.subsystem import ControllerSubSystemBasis
from Distributed_Design_Optimizer.subsystem.optimization import OptimizationController
from Distributed_Design_Optimizer.subsystem.couplingparameters.aladin import (LocalToLocalForController_CouplingParameters,
                                                                              ControllerCouplingParametersALADIN
                                                                              )
from Distributed_Design_Optimizer.coordination.convergence import (Local_ConvergenceIndicator_Innerloop_AlwaysConverged,
                                                                   Local_ConvergenceIndicator_Outerloop_AlwaysConverged
                                                                   )
from Distributed_Design_Optimizer.coordination.updatecouplingparametermethod import UpdateCouplingParameterMethod_NoOp
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import ddo_print

class ControllerSubSystemALADIN(ControllerSubSystemBasis):
    """Controller subsystem implementation for the ALADIN coordination method.

    Implements the controller QP formulation for ALADIN distributed optimization,
    including assembly of the quadratic term, linear term, and constraint matrix,
    as well as mapping of design variables to coupling parameters.
    """
    
    def __init__(self,
                 neighborid: List[str],
                 neighbors_of_neighbors_ids: Dict[str, List[str]],
                 optimization: OptimizationController,
                 ) -> None:
        """Creates a new instance of ControllerSubSystemALADIN.

        Args:
            neighborid: List of identifiers for the neighboring local subsystems.
            neighbors_of_neighbors_ids: Mapping of local subsystem ID to its neighbor IDs.
            optimization: Optimization controller for solving the controller QP.
        """
        # Initialize coupling parameters and their nested structures before super().__init__(),
        # since ControllerSubSystemBasis.__init__() calls initialize_Initial_Optimdata_at_Beginning()
        # which may be extended in the future to reference couplingparameters (consistent with
        # the local subsystem initialization pattern in LocalSubSystemBasis).
        
        self._couplingparameters: List[ControllerCouplingParametersALADIN] = [ControllerCouplingParametersALADIN(id=neighbor_id) for neighbor_id in neighborid]
        
        # Instantiate self._couplingparameters.controllertolocal_couplingparameters
        # and self._couplingparameters.localtocontroller_couplingparameters
        for i in range(len(neighborid)):
            
            # Get ID of corresponding local subsystem
            local_id: str = neighborid[i]
            
            # Store couplingparameter object
            couplingparameter: ControllerCouplingParametersALADIN = self._couplingparameters[i]
            
            # Instantiate Copy LocalToLocalForController coupling parameters
            couplingparameter.set_Copy_LocalToLocalForController_CouplingParameters([LocalToLocalForController_CouplingParameters(id=neighbor_of_neighbor_id) 
                                                                             for neighbor_of_neighbor_id in neighbors_of_neighbors_ids[local_id]])

        # super() initialization is not called at the top,
        # since initialization of optimdata in ControllerSubSystemBasis may need couplingparameters
        super().__init__(neighborid)
        
        # Set solver for controller, i.e. here ALADIN's controller QP
        self._optimization: OptimizationController = optimization
        
        # Convergence indicators - always converged for controller
        self._local_convergenceindicator_innerloop = Local_ConvergenceIndicator_Innerloop_AlwaysConverged()
        self._local_convergenceindicator_outerloop = Local_ConvergenceIndicator_Outerloop_AlwaysConverged()
        
        # ALADIN manages coupling parameter updates internally, so use a no-op update method
        # to satisfy the SubSystemBasis.update_state() contract
        self._updatecouplingparametermethod_outerloop: UpdateCouplingParameterMethod_NoOp = UpdateCouplingParameterMethod_NoOp()
        
        
        # Provisionary indices_map: Possible future extension of ALADIN includes slack variables 
        # tau for numerical stability in the QP solver, for which provisionary code is implemented
        # Here, the slack variables, their getters and setters as well as update_state
        # have commented code
        
        # Disclaimer: The used mapping assumes self._designvariables are structured as follows
        #  [\:^{1}\delta, \:^{1}tauleft, \:^{1}taushared, \:^{2}\delta, \:^{2}tauleft, ...]
        # (so only tau for left (i's mapped response) and shared constraints)
        # Also see in prepare_Optimization to setup QP
        
        # Define the map which for each i <-> j coupling returns the positions of the corresponding blocks in self._designvariables
        # CURRENTLY WITHOUT SLACK VARIABLES TAU, HENCE indices_map has values = ((index_i,index_j))
        # Keys are the id pairs (i,j), values = ((index_i,index_j), (start_tau_left, end_tau_left), (start_tau_shared, end_tau_shared))
        self._indices_map: Dict[Tuple[str, str], List[List[int]]] = {}
        
        # Controller: There are no ALADIN-specific quantities which are not stored in self._couplingparameters
        # Hence, no further variables

    def validate_inputs(self) -> None:
        """Validate the components handed to this subsystem.

        The ALADIN controller does not receive convergence indicators, an update
        coupling parameter method, or an iteration scheme from the coordination
        method. Those components are fixed internally (always-converged indicators
        and a no-op update method). There is therefore nothing to validate.
        """

    def set_DesignVariables(self, designvariables: List[float]) -> None:
        """Set the design variable vector (scaled01 values).

        Args:
            designvariables: Design variable vector in scaled01 values.
        """
        self._designvariables = copy.copy(designvariables)  # scaled01 values
        self._designvariables_unscaled = copy.copy(designvariables)
        
    # Provision: Possible future extension of ALADIN includes slack variables 
    # tau for numerical stability in the QP solver, for which provisionary code is implemented
    # Here, the slack variables, their getters and setters as well as update_state
    # have commented code
    
    def get_Indices_Map(self) -> Dict[Tuple[str, str], List[List[int]]]:
        """Return the map of indices for each i <-> j coupling.

        For each i <-> j coupling, returns the positions of the corresponding
        blocks in self._designvariables. Keys are the id pairs (i,j),
        values = ((index_i,index_j), (start_tau_left, end_tau_left),
        (start_tau_shared, end_tau_shared)).

        Returns:
            Mapping from id pairs (i,j) to lists of index pairs in
            self._designvariables.
        """
        
        return self._indices_map
    
    def check_Decomposition(self, couplingparameters: List[ControllerCouplingParametersALADIN],
                            id_i: str, id_j: str) -> List[bool]:
        """Check whether the coupling i->j is decomposed, i.e. j->i also exists.

        Return a Boolean list, where the first entry indicates 
        the decomposition in the mapped responses constraints and
        the second entry the decomposition in the shared variables.
        
        Args:
            couplingparameters: List of controller coupling parameters.
            id_i: Identifier of subsystem i.
            id_j: Identifier of subsystem j.

        Returns:
            Boolean list [mapped_responses, shared_variables, coupling_variables, target_shared].
        """
        
        # Initialize to be returned list of booleans
        # Order of bools: 
        # Mapped responses, shared design variables, coupling variables, target shared design variables
        decomposed: List[bool] = [False, False, False, False]
        
        # Use indices_map[0], which gives the position of j,i coupling...
        indices_map: Dict[Tuple[str, str], List[List[int]]] = self.get_Indices_Map()
        
        # The index of subsystems id_i and id_j w.r.t to first 
        # getting the element with id id_i in self._couplingparameters
        # and then in ControllerCouplingParametersALADIN, the 
        # LocalToController_CouplingParameters object with id id_j
        
        index_i_from_i: int = indices_map[(id_i, id_j)][0][0]
        index_j_from_i: int = indices_map[(id_i, id_j)][0][1]
        
        # In ControllerCouplingParameter to subsystem i, get LocalToController 
        # Coupling parameter to subsystem j
        copy_localtolocalforcontroller_couplingparameters_from_i: List[LocalToLocalForController_CouplingParameters] = couplingparameters[index_i_from_i].get_Copy_LocalToLocalForController_CouplingParameters()
        copy_localtolocalforcontroller_couplingparameter_from_i: LocalToLocalForController_CouplingParameters = copy_localtolocalforcontroller_couplingparameters_from_i[index_j_from_i]
        
        # Check if mirrored id pair is contained in the keys of indices_map
        if (id_j, id_i) in indices_map.keys():
            
            # The index of subsystems id_j and id_i w.r.t to first 
            # getting the element with id id_j in self._couplingparameters
            # and then in ControllerCouplingParametersALADIN, the 
            # LocalToController_CouplingParameters object with id id_i
            
            index_j_from_j: int = indices_map[(id_j, id_i)][0][0]
            index_i_from_j: int = indices_map[(id_j, id_i)][0][1]
            
            # Get mirrored LocalToController coupling parameters object
            copy_localtolocalforcontroller_couplingparameters_from_j: List[LocalToLocalForController_CouplingParameters] = couplingparameters[index_j_from_j].get_Copy_LocalToLocalForController_CouplingParameters()
            copy_localtolocalforcontroller_couplingparameter_from_j: LocalToLocalForController_CouplingParameters = copy_localtolocalforcontroller_couplingparameters_from_j[index_i_from_j]            
            
            # Check if mapped response (subsystem i) <-> coupling variable (subsystem j) constraint exists
            if (copy_localtolocalforcontroller_couplingparameter_from_i.get_MappedResponses() is not None 
                and copy_localtolocalforcontroller_couplingparameter_from_j.get_CouplingVariables() is not None):
                
                # Update first entry in list 'decomposed' to True, since the constraint is decomposed
                decomposed[0] = True
                    
            # Check if shared variables (subsystem i) <-> target shared design variable (subsystem j) constraint exists
            if (copy_localtolocalforcontroller_couplingparameter_from_i.get_SharedDesignVariables() is not None 
                and copy_localtolocalforcontroller_couplingparameter_from_j.get_TargetSharedDesignVariables() is not None):
                
                # Update second entry in list 'decomposed' to True, since the constraint is decomposed
                decomposed[1] = True
            
            # For additional / coupling variables and target shared design variable couplings, suffices to check 
            # if those exist in subsystem i, no check of subsystem j needed
            # For completeness, the bidirectional check is still included
            
            # Check if additional / coupling variables h (subsystem i) <-> mapped response (subsystem j) constraint exists
            if (copy_localtolocalforcontroller_couplingparameter_from_i.get_CouplingVariables() is not None 
                and copy_localtolocalforcontroller_couplingparameter_from_j.get_MappedResponses() is not None):
                
                # Update third entry in list 'decomposed' to True, since the constraint is decomposed
                decomposed[2] = True
                
            # Check if target shared design variables (subsystem i) <-> shared design variables (subsystem j) constraint exists
            if (copy_localtolocalforcontroller_couplingparameter_from_i.get_TargetSharedDesignVariables() is not None 
                and copy_localtolocalforcontroller_couplingparameter_from_j.get_SharedDesignVariables() is not None):
                
                # Update fourth entry in list 'decomposed' to True, since the constraint is decomposed
                decomposed[3] = True
                    
        # Return the list 'decomposed'
        return decomposed

    def initialize_MapIndices(self) -> None:
        """Set self._indices_map by defining the index mapping for all couplings.

        For each i <-> j coupling, determines the positions of the corresponding
        blocks in self._designvariables. Keys are the id pairs (i,j),
        values = ((index_i, index_j), (start_tau_left, end_tau_left),
        (start_tau_shared, end_tau_shared)).
        """
        
        # The first loop is to have a mapping of id pairs to indices in the nested list structure, 
        # and the second to infer the sizes of the designvariable parts of tau
        
        # FIRST LOOP
        
        # index pointer in list of designvariables
        index: int = 0
        
        # length of each of the blocks of self._designvariables
        blocklength: int = 0
        
        # List of coupling parameters
        couplingparameters: List[ControllerCouplingParametersALADIN] | None = self.get_CouplingParameters()
        
        # Loop over subsystems i
        for i in range(len(couplingparameters)):

            # Get size of local (lower) bounds of subsystem i, which has the same size as \:^{i}d / \:^{i}\delta d
            blocklength = len(couplingparameters[i].get_Copy_Jacobian_LowerBound())
            
            # Update current index
            index += blocklength
            
            # Obtain LocalToLocalForController_CouplingParameters list
            copy_localtolocalforcontroller_couplingparameters: List[LocalToLocalForController_CouplingParameters] = couplingparameters[i].get_Copy_LocalToLocalForController_CouplingParameters()
            
            # Loop over neighbors j of i
            for j in range(len(copy_localtolocalforcontroller_couplingparameters)):
                
                # Get coupling associated to i <-> j coupling
                copy_localtolocalforcontroller_couplingparameter: LocalToLocalForController_CouplingParameters = copy_localtolocalforcontroller_couplingparameters[j]
                
                # Get ids of i and j
                ids: Tuple[str, str] = (couplingparameters[i].get_ID(), copy_localtolocalforcontroller_couplingparameter.get_ID())
                
                # Store index pairs of the subsystem i and j with the ids as key
                self._indices_map[ids] = []
                # Define 0-th position in list that is the dictionary's value as pair of index values
                # only to point to both subsystems in a subsystem coupling by their id values
                self._indices_map[ids].append([i,j])
                  
        
        # Provision: Possible future extension of ALADIN includes slack variables 
        # tau for numerical stability in the QP solver, for which provisionary code is implemented
        # Here, the slack variables, their getters and setters as well as update_state
        # have commented code
        
        # SECOND LOOP
        
        # # index pointer in list of designvariables
        # index: int = 0
        
        # # length of each of the blocks of self._designvariables
        # blocklength: int = 0
        
        # # List of coupling parameters
        # couplingparameters: List[ControllerCouplingParametersALADIN] | None = self.get_CouplingParameters()
        
        # # Loop over subsystems i
        # for i in range(len(couplingparameters)):

        #     # Get size of local (lower) bounds of subsystem i, which has the same size as \:^{i}d / \:^{i}\delta d
        #     blocklength = len(couplingparameters[i].get_Copy_Jacobian_LowerBound())
            
        #     # Update current index, which corresponds to skipping over the \:^{i}\delta_d blocks to define indices_map
        #     index += blocklength
            
        #     # Obtain LocalToLocalForController_CouplingParameters list
        #     copy_localtolocalforcontroller_couplingparameters: List[LocalToLocalForController_CouplingParameters] = couplingparameters[i].get_Copy_LocalToLocalForController_CouplingParameters()
            
        #     # Loop over neighbors j of i
        #     for j in range(len(copy_localtolocalforcontroller_couplingparameters)):
                
        #         # Get coupling associated to i <-> j coupling
        #         copy_localtolocalforcontroller_couplingparameter: LocalToLocalForController_CouplingParameters = copy_localtolocalforcontroller_couplingparameters[j]
                
        #         # Get ids of i and j
        #         ids: Tuple[str, str] = (couplingparameters[i].get_ID(), copy_localtolocalforcontroller_couplingparameter.get_ID())

        #         # Update indices map for subsystem i -> subsystem j, only if constraint decompositions exist
                
        #         # Check if for this i->j coupling, the j->i coupling parts decomposition exists
                
        #         coupling_decomposition_happened: List[bool] = self.check_Decomposition(couplingparameters=couplingparameters, id_i=ids[0], id_j=ids[1])
                    
                
        #         # For mapped responses (subsystem i) <-> coupling variables (subsystem j)
                
        #         # Infer part of tau of left / mapped response block, if it exists
        #         if coupling_decomposition_happened[0] is True:
                    
        #             # Get length of mapped responses to infer length of tau part
        #             blocklength = len(copy_localtolocalforcontroller_couplingparameter.get_MappedResponses())
                    
        #             # Update indices map by adding to the 1-st position of the list that is the dictionary's value the pair
        #             # of indices w.r.t self._designvariables of tau_left
        #             self._indices_map[ids].append([index, index + blocklength])
                     
        #             # Update index
        #             index += blocklength
                    
        #         else:
                    
        #             # Else empty list
        #             self._indices_map[ids].append([])
                
        #         # Infer part of tau of shared design variable block, if it exists
        #         if coupling_decomposition_happened[1] is True:
                    
        #             # Get length of shared design variables to infer length of tau part
        #             blocklength = len(copy_localtolocalforcontroller_couplingparameter.get_SharedDesignVariables())
                    
        #             # Update indices map by adding to the 2-nd position of the list that is the dictionary's value the pair
        #             # of indices w.r.t self._designvariables of tau_shared
        #             self._indices_map[ids].append([index, index + blocklength])
                     
        #             # Update index
        #             index += blocklength
                
        #         else:
                    
        #             # Else empty list
        #             self._indices_map[ids].append([])

    
########################################################################################################
#   Functions to handle coupling parameters
#######################################################################################################
    
    def mapToCouplingParameters(self) -> None:
        """Split design variables into delta_d and tau and set the corresponding LTCPs in CCP.
        """
        
        # Provision: Possible future extension of ALADIN includes slack variables 
        # tau for numerical stability in the QP solver, for which provisionary code is implemented
        # Here, the slack variables, their getters and setters as well as update_state
        # have commented code
        
        
        # # Disclaimer: This mapping assumes self._designvariables are structured as follows
        # #  [\:^{1}\delta, \:^{1}tauleft, \:^{1}taushared, \:^{2}\delta, \:^{2}tauleft, ...]
        # # (so only tau for left (i's mapped response) and shared constraints)
        # # Also see in prepare_Optimization to setup QP
        
        # # Get the map of indices to update the taus symmetrically
        # indices_map: Dict[Tuple[str, str], List[List[int]]] = self.get_Indices_Map()
        
        # List of designvariables
        designvariables: List[float] | None = self.get_DesignVariables()
        
        # index pointer in list of designvariables
        index: int = 0
        
        # List of coupling parameters
        couplingparameters: List[ControllerCouplingParametersALADIN] | None = self.get_CouplingParameters()
        
        # Mapping of delta_d and tau from self._designvariables into CCPs and nested lists of LTCPs
        # Note there are two loops, since the tau variables are symmetric, so e.g. \:^{i}_{j} \tau corresponds both
        # to subsystem i's LTCP's corresponding to j in \tau_left and at the same time to subsystem j's LTCP's 
        # corresponding to i in \tau_right
        
        # Loop over subsystems i
        for i in range(len(couplingparameters)):
            
            # Get id of the subsystem
            id_i: str = couplingparameters[i].get_ID()
            
            # Obtain \:^{i}delta_d
            
            # Get size of \:^{i}delta_d by using the Jacobian of the (lower) bounds
            blocklength = len(couplingparameters[i].get_Copy_Jacobian_LowerBound())
            
            # Extract the \:^{i}\delta_d part of self._designvariables
            couplingparameters[i].set_Delta_D(designvariables[index:index+blocklength])  # Get sublist starting from index with length blocklength for \:^{i}delta_d
            
            # Update current index
            index += blocklength
            
            # Provision: Possible future extension of ALADIN includes slack variables 
            # tau for numerical stability in the QP solver, for which provisionary code is implemented
            # Here, the slack variables, their getters and setters as well as update_state
            # have commented code
        
            # # Obtain ControllerToLocalCouplingParameters list
            # controllertolocal_couplingparameters_from_i: List[ControllerToLocalCouplingParameters] = couplingparameters[i].get_ControllerToLocal_CouplingParameters()
            
            # # Loop over neighbors j of i
            # for j in range(len(controllertolocal_couplingparameters_from_i)):
            #     # Obtain controller coupling parameter corresponding to i <-> j coupling
            #     controllertolocal_couplingparameter_from_i: ControllerToLocalCouplingParameters = controllertolocal_couplingparameters_from_i[j]
                
            #     # Get id of the corresponding subsystem
            #     id_j: str = controllertolocal_couplingparameter_from_i.get_ID()
                
            #     # Check if there is any coupling constraint decomposition between i and j
            #     # by checking if there are the keys first
            #     if (id_i, id_j) in indices_map and (id_j, id_i) in indices_map:
                    
            #         # Get indices in nested structure for mirrored j <-> i coupling
            #         indices_j_i: List[int] = indices_map[(id_j, id_i)][0]
                    
            #         # Obtain corresponding coupling parameter of mirrored coupling j <-> i
            #         controllertolocal_couplingparameters_from_j: List[ControllerToLocalCouplingParameters] = couplingparameters[indices_j_i[0]].get_ControllerToLocal_CouplingParameters()
            #         controllertolocal_couplingparameter_from_j: ControllerToLocalCouplingParameters = controllertolocal_couplingparameters_from_j[indices_j_i[1]]
                    
            #         # If there is a mapped response (subsystem i) <-> coupling variable (subsystem j) coupling constraint
            #         # By definition of initialize_Indices_Map, equaivalent to indices_map[id_i, id_j][1] is not []
            #         if len(indices_map[(id_i, id_j)][1]) != 0:
                        
            #             # Get the positions of the corresponding tau_mapped block in self._designvariables
            #             block_tau_mapped: List[int] = indices_map[(id_i, id_j)][1]
                        
            #             # Extract tau_left part of i <-> j coupling, using the definition of indices_map
            #             controllertolocal_couplingparameter_from_i.set_TauLeft(designvariables[block_tau_mapped[0]:block_tau_mapped[1]])
                        
            #             # Set tau_right part of i <-> j coupling 
            #             controllertolocal_couplingparameter_from_j.set_TauRight(controllertolocal_couplingparameter_from_i.get_TauLeft())
                        
            #             # Update index
            #             index = block_tau_mapped[1]
                        
            #         # If there is a shared design variable (subsystem i) <-> target shared design varuable (subsystem j) coupling constraint
            #         # By definition of initialize_Indices_Map, equaivalent to indices_map[id_i, id_j][2] is not []
            #         if len(indices_map[(id_i, id_j)][2]) != 0:
                        
            #             # Get the positions of the corresponding tau_shared block in self._designvariables
            #             block_tau_shared: List[int] = indices_map[(id_i, id_j)][2]
                        
            #             # Extract tau_shared of i <-> j coupling, using the definition of indices_map
            #             controllertolocal_couplingparameter_from_i.set_TauSharedDesignVariables(designvariables[block_tau_shared[0]:block_tau_shared[1]])
                        
            #             # Set tau_targetshared part of i <-> j coupling
            #             controllertolocal_couplingparameter_from_j.set_TauTargetSharedDesignVariables(controllertolocal_couplingparameter_from_i.get_TauSharedDesignVariables())
                        
            #             # Update index
            #             index = block_tau_shared[1]
                
    
    def initializeCouplingParameters_before_CopyToMiddleLevel(self) -> None:
        """Controller subsystem does not initialize coupling parameters, so we leave this function empty.
        """
        
        pass

    def initializeCouplingParameters_after_CopyFromMiddleLevel(self) -> None:
        """Controller subsystem does not initialize coupling parameters, so we leave this function empty.
        """
        
        # Provision: Possible future extension of ALADIN includes slack variables 
        # tau for numerical stability in the QP solver, for which provisionary code is implemented
        # CURRENTLY WITHOUT SLACK VARIABLES TAU, HENCE indices_map has values = ((index_i,index_j))
        # Here, the slack variables, their getters and setters as well as update_state
        # have commented code
    
        
        # Call initialize_Map_Indices here to create a hash table of id-pairs of couplings and 
        # there indices within the nested list-type structure, since self._couplingparameters
        # is a list of ControllerCouplingParametersALADIN and their attribute localtocontroller_
        # coupling parameters of LocalToController_CouplingParameters
        
        self.initialize_MapIndices()
        
        
        # Init of CCP's and LTCP's attributes, especially self._localcouplingparametera, happens by doing CopyFromMiddleLevel
        # Hence, no init needed except for QP problem solve
        
        # Prepare and solve controller QP to init the rest of the coupling parameters
        # Postprocessing stores the \:^{i}\delta d in the corresponding coupling parameters
        self.prepare_OptimizationProblem()
        self.run_IterativeOptimization()
        self.postprocess_Optimization()
    
    def initializeCouplingParameters_after_Second_CopyFromMiddleLevel(self) -> None:
        """Controller subsystem does not initialize coupling parameters, so we leave this function empty.
        """
        
        pass
    
    def updateCouplingParameters_innerLoop(self) -> None:
        """Update coupling parameters in the inner loop."""
        pass
    
    def prepare_updateCouplingParameters(self) -> None:
        """Prepare coupling parameters before update operations."""
        pass
        
    def updateCouplingParameters_outerLoop(self) -> None:
        """Update coupling parameters during outer loop iteration."""
        pass
    
    
###############################################################################################################
#   Functions to handle coupling parameters related to modelling a distributed optimization problem.
#   This only works on mappedresponses, couplingvariables, shareddesignvariables, targetshareddesignvariables
#   and their copy_-counterparts.
#   Nothing related to coupling parameters
###############################################################################################################
    
    def return_initialized_CouplingParameters(self) -> List[ControllerCouplingParametersALADIN]:
        """Return a fresh list of initialized ControllerCouplingParametersALADIN.

        Returns:
            List of initialized coupling parameters with matching IDs.
        """

        initialized_couplingparameters: List[ControllerCouplingParametersALADIN] = [ControllerCouplingParametersALADIN(self.get_CouplingParameters()[i].get_ID()) 
                                                                                    for i in range(len(self.get_CouplingParameters()))]
        
        return initialized_couplingparameters
    
##############################################################################################################
#   Functions to evaluate a subsystem's optimization objective and constraints for given responses
##############################################################################################################
 
    def evaluateCoordinationObjective(self) -> None:
        """Evaluate the coordination objective (the controller's QP objective in ALADIN).
        """
        
        # From the QP solver, obtain P and q and compute 0.5 * delta_d^{T}P*delta_t + q^{T}delta_d
        solver_qp = self._optimization.get_Optimizer()
        P: np.typing.ArrayLike = solver_qp.get_P()
        q: np.typing.ArrayLike = solver_qp.get_q()
        
        # Get the designvariables as np.array
        delta_d: np.typing.ArrayLike = np.array(self.get_DesignVariables())
        
        # Compute the QP objective 0.5 * d^{T}Pd + q^{T}d
        qp_objective: float = float(0.5 * delta_d.T @ P @ delta_d + q.T @ delta_d)
        
        # Set the coordination objective
        self.set_CoordinationObjectiveValue(qp_objective)
        
    
    def evaluate_Gradient_CoordinationObjective(self) -> None:
        """Evaluate the analytical gradient of the coordination objective.

        Assumes the QP data P and q were assembled already (see prepare_OptimizationProblem).
        """
        
        # From the QP solver, obtain P (symmetric by construction in controller) 
        # and q and compute \nabla(0.5 * delta_d^{T}P*delta_d + q^{T}*delta_d) = P*delta_d + q 
        solver_qp = self._optimization.get_Optimizer()
        P: np.typing.ArrayLike = solver_qp.get_P()
        q: np.typing.ArrayLike = solver_qp.get_q()
        
        # Get the designvariables as np.array
        delta_d: np.typing.ArrayLike = np.array(self.get_DesignVariables())
        
        # Compute the QP gradient P*delta_d + q
        qp_objective_gradient: List[float] = (P @ delta_d + q).tolist()
        
        # Set the coordination objective gradient
        self._optimdata.set_Gradient_CoordinationObjective(qp_objective_gradient)
    
      
    def evaluateCoordinationEqualityConstraint(self) -> None:
        """Evaluate the equality constraints of the controller's QP optimization problem."""
        
        # From the QP solver, obtain A and compute A*delta_d
        A: np.typing.ArrayLike = self._optimization.get_Optimizer().get_A()
        
        # Get the designvariables as np.array
        delta_d: np.typing.ArrayLike = np.array(self.get_DesignVariables())
        
        # Compute the QP equality constraint A*delta_d
        qp_equality_constraint: List[float] = (A @ delta_d).tolist()
        
        # Set the coordination objective
        self.set_CoordinationEqualityConstraintValue(qp_equality_constraint)
    
    def evaluateCoordinationInequalityConstraint(self) -> None:
        """Evaluate the inequality constraints of the controller's QP optimization problem.

        These stem from the local inequality and bound constraints assembled into the
        QP (G*delta_d - h <= 0); the result is an empty vector if none exist.
        """
        
        # From the QP solver, obtain G and h and compute G*delta_d - h
        solver_qp = self._optimization.get_Optimizer()
        G: np.typing.ArrayLike = solver_qp.get_G()
        h: np.typing.ArrayLike = solver_qp.get_h()
        
        # Get the designvariables of controller as np.array
        delta_d: np.typing.ArrayLike = np.array(self.get_DesignVariables())
        
        # Compute the QP inequality constraint G*delta_d - h (feasible when <= 0)
        # Since G and h are defined such that the constraints of the QP 
        # are formulated as G*delta_D <= h (<=> G*delta_D-h <= 0)
        # Where h = (- \:^{g}v(\:^{i}d))_i, i.e. the negated values of the 
        # inequality functions of all subsystems
        qp_inequality_constraint: List[float] = (G @ delta_d - h).tolist()
        
        # Set the coordination inequality constraint value
        self.set_CoordinationInequalityConstraintValue(qp_inequality_constraint)
    
    
    def evaluate_Jacobian_CoordinationEqualityConstraints(self) -> None:
        """Evaluate the Jacobian of the coordination equality constraints."""
        
        # The Jacobian of the linear equality constraint A*delta_d = 0 w.r.t. delta_d is A
        A: np.typing.ArrayLike = self._optimization.get_Optimizer().get_A()
        
        # Set the Jacobian of the coordination equality constraints
        if A is not None and np.asarray(A).size > 0:
            self._optimdata.set_Jacobian_CoordinationEqualityConstraints(np.asarray(A, dtype=float).tolist())
    
    def evaluate_Jacobian_CoordinationInEqualityConstraints(self) -> None:
        """Evaluate the Jacobian of the coordination inequality constraints."""
        
        # The Jacobian of the linear inequality constraint G*delta_d - h <= 0 w.r.t. delta_d is G
        G: np.typing.ArrayLike = self._optimization.get_Optimizer().get_G()
        
        # Set the Jacobian of the coordination inequality constraints
        if G is not None and np.asarray(G).size > 0:
            self._optimdata.set_Jacobian_CoordinationInequalityConstraints(np.asarray(G, dtype=float).tolist())
        
    
##############################################################################################################
#   Functions to preprocess / postprocess optimization
##############################################################################################################

    def prepare_OptimizationProblem(self) -> None:
        """Prepare the QP optimization problem by assembling P, q, and A."""
        
        # Note that the local quantities like e.g. Hessians, Jacobians, ..., can be accessed 
        # via copy_localcouplingparameters
        
        
        # Assemble the components of the standard QP form that are needed
        # Refer to the review paper on Distributed Design Optimization
        
        # The matrix of the quadratic term
        
        P: np.typing.ArrayLike = self.qp_quadratic_term() 
        
        # Check positive semi-definiteness of P
        eigenvalues = np.linalg.eigvalsh(P)
        eigenvalues_tol = 1e-12
        if np.any(eigenvalues < -eigenvalues_tol):
            min_eigenvalue = np.min(eigenvalues)
            num_negative = np.sum(eigenvalues < -eigenvalues_tol)
            ddo_print(f"WARNING: QP matrix P is NOT positive semi-definite. "
                     f"Min eigenvalue: {min_eigenvalue:.6e}, "
                     f"Number of negative eigenvalues: {num_negative}/{len(eigenvalues)}")
        
        # NOTE: In the following, possible modification strategies to restore positive semi-definiteness 
        # are described (currently NOT implemented) ---
        # If P is not positive semi-definite, one could consider the following approaches 
        # to transform P into a positive semi-definite matrix:
        #   - Method 1: Project eigenvalues < eigenvalues_tol to eigenvalues_tol
        #   - Method 2: Use P + mu * I, i.e. add a multiple of the identity matrix 
        #               such that the matrix is positive semi-definite
        #   - Method 3: Compute Cholesky-Decomposition (e.g. scipy.linalg.cho_factor); if this throws an error, 
        #               which happens iff the matrix is not positive semi-definite, then compute (minimal) perturbations
        #               needed to obtain a positive semi-definite matrix
        #   - Method 4: Use (damped) BFGS/SR1 matrices, which needs additional fields to store
        #   - Method 5: Diagonalize P = V.T @ D @ V, then use V.T @ abs(D) @ V 
        #               (from "Numerical Optimization" by Nocedal & Wright).
        #               Here, abs(D) denotes the elementwise absolute value of D.
        
        
        # The vector from the linear term
        q: np.typing.ArrayLike = self.qp_linear_term()
             
        # Constraints of the QP
        A: np.typing.ArrayLike = self.qp_constraint_equality_matrix()
        G: np.typing.ArrayLike = self.qp_constraint_inequality_matrix()
        h: np.typing.ArrayLike = self.qp_constraint_inequality_righthandside()
        
        # Store the newly computed quantities into the QP solver
        solver_qp = self._optimization.get_Optimizer()
        solver_qp.set_P(P)
        solver_qp.set_q(q)
        solver_qp.set_A(A)
        solver_qp.set_G(G)
        solver_qp.set_h(h)
    
    
    def qp_quadratic_term(self) -> np.typing.ArrayLike:
        """Compute the symmetrized quadratic term matrix P for the ALADIN QP.

        Returns:
            The symmetrized matrix P such that the QP objective is 0.5*d^T*P*d + q^T*d.
        """
        
        # Get local <-> controller coupling parameters
        couplingparameters: List[ControllerCouplingParametersALADIN] = self.get_CouplingParameters()
        
        # Build a list for each i <-> j and 
        # i <-> i term in the formula of P
        P: List[List[np.typing.ArrayLike]] = [[np.array([]) for j in range(len(couplingparameters))] 
                                              for i in range(len(couplingparameters))]
        
            
        # Get the indices map 
        indices_map: Dict[Tuple[str, str], List[List[int]]] = self.get_Indices_Map()
        
        # Loop over local subsystems i
        for i in range(len(couplingparameters)):
            
            # Get the coupling w.r.t local subsystem i
            coupling_i: ControllerCouplingParametersALADIN = couplingparameters[i]
            
            # Get the dimension of the designvariables of subsystem i
            primal_dimension: int = len(coupling_i.get_Copy_Jacobian_LowerBound())
            
            # Get the id of subsystem i
            id_i: str = coupling_i.get_ID()
            
            # Get the local <-> local coupling parameters of subsystem i
            couplingparameters_i: List[LocalToLocalForController_CouplingParameters] = coupling_i.get_Copy_LocalToLocalForController_CouplingParameters()
            
            # First term of formula is the Hessian of the local Lagrangian
            # It is a 2D-matrix, since subsystem copies zeros-matrix 
            # even if local objective, local equality and local inequality constraints 
            # do not exist
            P[i][i] = np.array(copy.deepcopy(coupling_i.get_Copy_Hessian_LocalConstraints_Lagrangian()))
            
            # Loop over all subsystems j that are neighbored to i
            for j in range(len(couplingparameters_i)):
                                    
                # Get the corresponding i -> j coupling parameter
                couplingparameter_i_j: LocalToLocalForController_CouplingParameters = couplingparameters_i[j]
                
                # Get the id of subsystem with index j in couplingparameters_i
                id_j: str = couplingparameter_i_j.get_ID()
                
                # Similarly, get the i <- j coupling parameter using the indices_map
                indices_j_i: Tuple[int, int] = tuple(indices_map[(id_j, id_i)][0])
                index_j: int = indices_j_i[0]
                index_i: int = indices_j_i[1]
                coupling_j: ControllerCouplingParametersALADIN = couplingparameters[index_j]
                couplingparameters_j: List[LocalToLocalForController_CouplingParameters] = coupling_j.get_Copy_LocalToLocalForController_CouplingParameters()
                couplingparameter_j_i: LocalToLocalForController_CouplingParameters = couplingparameters_j[index_i]
                
                # Initialize P[i][j] with zeros matrix
                # Infer from dimensions of Jacobian of lower bounds
                # the dimensions of \:^{i}d and \:^{j}d
                
                dimension_i: int = len(coupling_i.get_Copy_Jacobian_LowerBound())
                dimension_j: int = len(coupling_j.get_Copy_Jacobian_LowerBound())
                
                P[i][index_j] = np.zeros((dimension_i, dimension_j))
                
                # Add the terms from the coupling circle based on review paper appendix
                
                # Infer which parts of the coupling are decomposed
                decomposed_i_j: List[bool] = self.check_Decomposition(couplingparameters, id_i, id_j)
                
                # Mapped responses i -> j side
                
                # Check if there is a i -> j mapped response which is decomposed
                if decomposed_i_j[0] is True:
                
                    # Get the multipliers and weights w.r.t. the i -> j coupling for mapped responses
                    multipliers_mappedresponses_i_j: np.typing.ArrayLike = np.array(couplingparameter_i_j.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable())
                    weights_mappedresponses_i_j: np.typing.ArrayLike = np.array(couplingparameter_i_j.get_Weights_MappedResponse_Minus_CopyCouplingVariable())
                    
                    # Compute the inconsistencies of the constraints w.r.t. 
                    # the i -> j coupling for mapped responses
                    
                    mappedresponses_i: np.typing.ArrayLike = np.array(couplingparameter_i_j.get_MappedResponses())
                    additionalvariables_j: np.typing.ArrayLike = np.array(couplingparameter_j_i.get_CouplingVariables())
                    inconsistency_mappedresponses_i_j: np.typing.ArrayLike = mappedresponses_i - additionalvariables_j
                    
                    # Add the terms corresponding to this i <-> j coupling, where the mapped responses are by 
                    # subsystem i and the coupling is actually decomposed, to P[i][i] and P[i][j]
                    
                    # Update P[i][i] by formula of two parts
                    
                    # First part: Hessians of mapped responses
                    hessians_mappedresponses_i_j = np.array(couplingparameter_i_j.get_HessiansMappedResponses())
                    
                    # Loop over the dimension of the mapped response
                    for component in range(len(hessians_mappedresponses_i_j)):
                        
                        # Add to P[i][i] the summands as per formula
                        P[i][i] += ((multipliers_mappedresponses_i_j[component] + 2 * weights_mappedresponses_i_j[component] 
                                    * weights_mappedresponses_i_j[component] * inconsistency_mappedresponses_i_j[component]) 
                                    * hessians_mappedresponses_i_j[component]) 
                        
                    # The other part associated to the mapped responses
                    # ...[:, None] is needed for elementwise / rowwise vector matrix multiplication
                    jacobian_mappedresponses_i_j: np.typing.ArrayLike = np.array(couplingparameter_i_j.get_JacobianMappedResponses())
                    P[i][i] += (jacobian_mappedresponses_i_j.T @ np.diag(2 * weights_mappedresponses_i_j ** 2) @ jacobian_mappedresponses_i_j)
                    
                    
                    # Update P[i][j] by formula
                    
                    # Selector matrix of additional design variables of subsystem j
                    indices_additionalvariables_h_in_designvariables_j: List[int] = couplingparameter_j_i.get_Indices_CouplingVariables_In_DesignVariables()
                    selector_h_j: np.typing.ArrayLike = np.eye(dimension_j)[indices_additionalvariables_h_in_designvariables_j]
                    
                    # Update P[i][index_j]
                    # Factor 4 (not 2) because only one side of the off-diagonal is filled per constraint;
                    # symmetrization (P+P^T)/2 will halve it back to the correct factor of 2, but will also 
                    # correctly update P[j_index][i]
                    P[i][index_j] -= jacobian_mappedresponses_i_j.T @ np.diag(4 * weights_mappedresponses_i_j ** 2) @ selector_h_j
                    
                
                # Shared design variables i -> j (z) side
                
                # Check if there is a i -> j shared design variable which is decomposed
                if decomposed_i_j[1] is True:
                    
                    # Get the weights w.r.t. the i -> j coupling for shared design variables
                    weights_shareddesignvariables_i_j: np.typing.ArrayLike = np.array(couplingparameter_i_j.get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
                    
                    # Get the indices of the shared design variables of the i <-> j coupling
                    indices_shareddesignvariables_z_in_designvariables_i: List[int] = couplingparameter_i_j.get_Indices_SharedDesignVariables_In_DesignVariables()
                    
                    # Add the terms corresponding to this i <-> j coupling, where the shared design variables are by 
                    # subsystem i and the coupling is actually decomposed, to P[i][i] and P[i][j]
                    
                    # Selector matrix of shared design design variables of subsystem i
                    selector_z_i: np.typing.ArrayLike = np.eye(dimension_i)[indices_shareddesignvariables_z_in_designvariables_i]
                    
                    # Weights matrix
                    weights_matrix_shared_i_j = np.diag(weights_shareddesignvariables_i_j ** 2)
                    
                    # Update P[i][i]
                    P[i][i] += 2*(selector_z_i.T 
                                @ weights_matrix_shared_i_j
                                @ selector_z_i)
                    
                    # Update P[i][j] by formula
                    
                    # Selector matrix of target shared design variables t of subsystem j
                    indices_targetshareddesignvariables_t_in_designvariables_j: List[int] = couplingparameter_j_i.get_Indices_TargetSharedDesignVariables_In_DesignVariables()
                    selector_t_j: np.typing.ArrayLike = np.eye(dimension_j)[indices_targetshareddesignvariables_t_in_designvariables_j]
                    
                    # Update P[i][index_j]
                    # Factor 2 in weights_matrix is doubled here (multiply by 2) because only one side
                    # of the off-diagonal is filled per constraint; symmetrization (P+P^T)/2 halves it back, 
                    # but will also correctly update P[j_index][i]
                    # Another factor 2 comes from weights_matrix_shared_i_j
                    P[i][index_j] -= 4 * (selector_z_i.T 
                                          @ weights_matrix_shared_i_j 
                                          @ selector_t_j)
                    
                    
                # Coupling / additional variables h for i -> j coupling
                # which is the j -> i coupling for mapped responses
                
                # Check if there is a i -> j coupling variable which is decomposed
                if decomposed_i_j[2] is True:
                    
                    # Get the weights w.r.t. the j -> i coupling for mapped responses 
                    # (coupling / additional design variables of subsytem i)
                    
                    weights_mappedresponses_j_i: np.typing.ArrayLike = np.array(couplingparameter_j_i.get_Weights_MappedResponse_Minus_CopyCouplingVariable())
    
                    # Get the indices of the coupling variables of the i <-> j coupling
                    indices_couplingvariables_h_in_designvariables_i: List[int] = couplingparameter_i_j.get_Indices_CouplingVariables_In_DesignVariables()
                    
                    # Add the terms corresponding to this i <-> j coupling, where the shared design variables are by 
                    # subsystem i and the coupling is actually decomposed, to P[i][i] and P[i][j]
                    
                    # Selector matrix of additional design / coupling variables of subsystem i
                    selector_h_i: np.typing.ArrayLike = np.eye(dimension_i)[indices_couplingvariables_h_in_designvariables_i]
                    
                    # Weights matrix
                    weights_matrix_coupling_i_j = np.diag(2 * weights_mappedresponses_j_i ** 2)
                    
                    # Update P[i][i]
                    P[i][i] += selector_h_i.T @ weights_matrix_coupling_i_j @ selector_h_i
                    
                
                # Target shared variables for i -> j coupling
                # which is the j -> i coupling for shared design variables
                
                # Check if there is a i -> j target shared design variable which is decomposed
                if decomposed_i_j[3] is True:
                    
                    # Get the weights w.r.t. the j -> i coupling for shared design variables
                    # (target shared design variables of subsytem i)
                    
                    weights_shareddesignvariables_j_i: np.typing.ArrayLike = np.array(couplingparameter_j_i.get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
                    
                    # Get the indices of the target shared variables of the i <-> j coupling
                    indices_targetshareddesignvariables_t_in_designvariables_i: List[int] = couplingparameter_i_j.get_Indices_TargetSharedDesignVariables_In_DesignVariables()
                    
                    # Add the terms corresponding to this i <-> j coupling, where the shared design variables are by 
                    # subsystem i and the coupling is actually decomposed, to P[i][i] and P[i][j]
                    
                    # Selector matrix of target shared design variables of subsystem i
                    selector_t_i: np.typing.ArrayLike = np.eye(dimension_i)[indices_targetshareddesignvariables_t_in_designvariables_i]
                    
                    # Weights matrix
                    weights_matrix_targetshared_i_j = np.diag(2 * weights_shareddesignvariables_j_i ** 2)
                    
                    # Update P[i][i]
                    P[i][i] += selector_t_i.T @ weights_matrix_targetshared_i_j @ selector_t_i
                    
                
        # Build the big block matrix
        P_preliminary: np.typing.ArrayLike = np.block(P)
        
        # Symmetrizize P by (P + P^{T}) / 2, which originates 
        # the same quadratic form
        P_result: np.typing.ArrayLike = 0.5 * (P_preliminary + P_preliminary.T)
        
        # Return the total result
        return P_result
        

    def qp_linear_term(self) -> np.typing.ArrayLike:
        """Compute the linear term vector q for the ALADIN QP.

        Returns:
            The vector q such that the QP objective is 0.5*d^T*P*d + q^T*d.
        """
    
        
        # The vector of the linear term
        # Based on the pseudocode in review paper
        q: List[float] = []
        
        # Get local <-> controller coupling parameters
        couplingparameters: List[ControllerCouplingParametersALADIN] = self.get_CouplingParameters()
            
        # Get the indices map 
        indices_map: Dict[Tuple[str, str], List[List[int]]] = self.get_Indices_Map()
        
        # Loop over all subsystems to define q
        # those are in the local <-> controller couplings
        # and all coupling circles
        for coupling in couplingparameters:
            
            # Get id of subsystem with index i in list couplingparameters
            id_i: str = coupling.get_ID()
                        
            # Initialize new vector for components w.r.t. subsystem i
            primal_dimension: int = len(coupling.get_Copy_Jacobian_LowerBound())
            q_i: np.typing.ArrayLike = [0.0] * primal_dimension
            
            # By formula, first add gradient of local cost function of subsystem i,
            # if it exists
            if coupling.get_Copy_Gradient_LocalObjective() is not None:
                
                q_i += np.array(coupling.get_Copy_Gradient_LocalObjective()) 
                
            # Then add terms corresponding to the coupling circle of coupling i <-> j
            
            # Get the coupling parameters of subsystem i
            couplingparameters_i: List[LocalToLocalForController_CouplingParameters] = coupling.get_Copy_LocalToLocalForController_CouplingParameters()
            
            # Loop over i <-> j couplings
            for j in range(len(couplingparameters_i)):
                
                # Get the corresponding i -> j coupling parameter
                couplingparameter_i_j: LocalToLocalForController_CouplingParameters = couplingparameters_i[j]
                
                # Get the id of subsystem with index j in couplingparameters_i
                id_j: str = couplingparameter_i_j.get_ID()
                
                # Similarly, get the i <- j coupling parameter using the indices_map
                indices_j_i: Tuple[int, int] = tuple(indices_map[(id_j, id_i)][0])
                index_j: int = indices_j_i[0]
                index_i: int = indices_j_i[1]
                couplingparameters_j: List[LocalToLocalForController_CouplingParameters] = couplingparameters[index_j].get_Copy_LocalToLocalForController_CouplingParameters()
                couplingparameter_j_i: LocalToLocalForController_CouplingParameters = couplingparameters_j[index_i]
                
                # Add the terms from the coupling circle based on review paper appendix
                
                # Infer which parts of the coupling are decomposed
                decomposed_i_j: List[bool] = self.check_Decomposition(couplingparameters, id_i, id_j)
                
                # Mapped responses i -> j side
                
                # Check if there is a i -> j mapped response which is decomposed
                if decomposed_i_j[0] is True:
                
                    # Compute the term in the formula of q_i corresponding to the mapped responses
                    jacobian_mappedresponses_i_j: List[List[float]] = couplingparameter_i_j.get_JacobianMappedResponses()
                    
                    # Get the multipliers and weights w.r.t. the i -> j coupling for mapped responses
                    multipliers_mappedresponses_i_j: np.typing.ArrayLike = np.array(couplingparameter_i_j.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable())
                    weights_mappedresponses_i_j: np.typing.ArrayLike = np.array(couplingparameter_i_j.get_Weights_MappedResponse_Minus_CopyCouplingVariable())
                    
                    # Compute the inconsistencies of the constraints w.r.t. 
                    # the i -> j coupling for mapped responses
                    
                    mappedresponses_i: np.typing.ArrayLike = np.array(couplingparameter_i_j.get_MappedResponses())
                    additionalvariables_j: np.typing.ArrayLike = np.array(couplingparameter_j_i.get_CouplingVariables())
                    inconsistency_mappedresponses_i_j: np.typing.ArrayLike = mappedresponses_i - additionalvariables_j
                                        
                    # Compute the addand in the formula of q_i w.r.t. the i -> j coupling for mapped responses
                    mappedresponses_term: np.typing.ArrayLike = np.array(jacobian_mappedresponses_i_j).T @ (multipliers_mappedresponses_i_j 
                                                                                                            + 2 * weights_mappedresponses_i_j 
                                                                                                            * weights_mappedresponses_i_j 
                                                                                                            * inconsistency_mappedresponses_i_j)
                    
                    # Add the addand mappedresponses_term to q_i
                    q_i += mappedresponses_term


                # Shared design variables i -> j side
                
                # Check if there is a i -> j shared design variable which is decomposed
                if decomposed_i_j[1] is True:
                    
                    # Get the multipliers and weights w.r.t. the i -> j coupling for shared design variables
                    multipliers_shareddesignvariables_i_j: np.typing.ArrayLike = np.array(couplingparameter_i_j.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
                    weights_shareddesignvariables_i_j: np.typing.ArrayLike = np.array(couplingparameter_i_j.get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
                    
                    # Compute the inconsistencies of the constraints w.r.t. 
                    # the i -> j coupling for shared design variables
                    
                    shareddesignvariables_i: np.typing.ArrayLike = np.array(couplingparameter_i_j.get_SharedDesignVariables())
                    targetshareddesignvariables_j: np.typing.ArrayLike = np.array(couplingparameter_j_i.get_TargetSharedDesignVariables())
                    inconsistency_shareddesignvariables_i_j: np.typing.ArrayLike = shareddesignvariables_i - targetshareddesignvariables_j
                    
                    # Get the indices of the shared design variables of the i <-> j coupling
                    indices_shareddesignvariables_in_designvariables_i_j: List[int] = couplingparameter_i_j.get_Indices_SharedDesignVariables_In_DesignVariables() 
                    
                    # Compute the addand in the formula of q_i w.r.t. the i -> j coupling for shareddesignvariables
                    
                    # First, initialize a zeros-vector of correct dimension
                    shareddesignvariables_term: np.typing.ArrayLike = np.array([0.0] * primal_dimension)
                    
                    # Use the formula for the addand, explicitly the left-multiplication by the transposed 
                    # selector matrix of the shared design variables in the i <-> j coupling
                    # This is done by only setting certain components of the total vector
                    
                    shareddesignvariables_term[indices_shareddesignvariables_in_designvariables_i_j] = (multipliers_shareddesignvariables_i_j 
                                                                                                        + 2 * weights_shareddesignvariables_i_j 
                                                                                                        * weights_shareddesignvariables_i_j 
                                                                                                        * inconsistency_shareddesignvariables_i_j)
                    
                    # Add the addand shareddesignvariables_term to q_i
                    q_i += shareddesignvariables_term

                
                # Coupling / additional variables h for i -> j coupling
                # which is the j -> i coupling for mapped responses
                
                # Check if there is a i -> j coupling variable which is decomposed
                if decomposed_i_j[2] is True:
                    
                    # Get the multipliers and weights w.r.t. the j -> i coupling for mapped responses 
                    # (coupling / additional design variables of subsytem i)
                    
                    multipliers_mappedresponses_j_i: np.typing.ArrayLike = np.array(couplingparameter_j_i.get_Multipliers_MappedResponse_Minus_CopyCouplingVariable())
                    weights_mappedresponses_j_i: np.typing.ArrayLike = np.array(couplingparameter_j_i.get_Weights_MappedResponse_Minus_CopyCouplingVariable())
                    
                    # Compute the inconsistencies of the constraints w.r.t. 
                    # the i -> j coupling for coupling variables (i.e. mapped response variable coupling j -> i)
                    
                    couplingvariables_i: np.typing.ArrayLike = np.array(couplingparameter_i_j.get_CouplingVariables())
                    mappedresponses_j: np.typing.ArrayLike = np.array(couplingparameter_j_i.get_MappedResponses())
                    inconsistency_mappedresponses_j_i: np.typing.ArrayLike = mappedresponses_j - couplingvariables_i

                    # Get the indices of the coupling variables of the i <-> j coupling
                    indices_couplingvariables_in_designvariables_i_j: List[int] = couplingparameter_i_j.get_Indices_CouplingVariables_In_DesignVariables()
                    
                    # Compute the addand in the formula of q_i w.r.t. the i -> j coupling for coupling variables
                    
                    # First, initialize a zeros-vector of correct dimension
                    couplingvariables_term: np.typing.ArrayLike = np.array([0.0] * primal_dimension)
                    
                    # Use the formula for the addand, explicitly the left-multiplication by the transposed 
                    # selector matrix of the coupling variables in the i <-> j coupling
                    # This is done by only setting certain components of the total vector
                    
                    couplingvariables_term[indices_couplingvariables_in_designvariables_i_j] = (multipliers_mappedresponses_j_i 
                                                                                                + 2 * weights_mappedresponses_j_i 
                                                                                                * weights_mappedresponses_j_i 
                                                                                                * inconsistency_mappedresponses_j_i)
                    
                    # Add the addand couplingvariables_term to q_i
                    q_i -= couplingvariables_term
                    
                
                # Target shared variables for i -> j coupling
                # which is the j -> i coupling for shared design variables
                
                # Check if there is a i -> j target shared design variable which is decomposed
                if decomposed_i_j[3] is True:
                    
                    # Get the multipliers and weights w.r.t. the j -> i coupling for shared design variables
                    # (target shared design variables of subsytem i)
                    
                    multipliers_shareddesignvariables_j_i: np.typing.ArrayLike = np.array(couplingparameter_j_i.get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
                    weights_shareddesignvariables_j_i: np.typing.ArrayLike = np.array(couplingparameter_j_i.get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())
                    
                    # Compute the inconsistencies of the constraints w.r.t. 
                    # the i -> j coupling for shared design variables (i.e. target shared variables coupling j -> i)
                    
                    targetshareddesignvariables_i: np.typing.ArrayLike = np.array(couplingparameter_i_j.get_TargetSharedDesignVariables())
                    shareddesignvariables_j: np.typing.ArrayLike = np.array(couplingparameter_j_i.get_SharedDesignVariables())
                    inconsistency_shareddesignvariables_j_i: np.typing.ArrayLike = shareddesignvariables_j - targetshareddesignvariables_i
                                        
                    # Get the indices of the target shared variables of the i <-> j coupling
                    indices_targetshareddesignvariables_in_designvariables_i_j: List[int] = couplingparameter_i_j.get_Indices_TargetSharedDesignVariables_In_DesignVariables()
                    
                    # Compute the addand in the formula of q_i w.r.t. the i -> j coupling for target shared variables
                    
                    # First, initialize a zeros-vector of correct dimension
                    targetshareddesignvariables_term: np.typing.ArrayLike = np.array([0.0] * primal_dimension)
                    
                    # Use the formula for the addand, explicitly the left-multiplication by the transposed 
                    # selector matrix of the target shared design variables in the i <-> j coupling
                    # This is done by only setting certain components of the total vector
                    
                    targetshareddesignvariables_term[indices_targetshareddesignvariables_in_designvariables_i_j] = (
                        multipliers_shareddesignvariables_j_i 
                        + 2 * weights_shareddesignvariables_j_i * weights_shareddesignvariables_j_i * inconsistency_shareddesignvariables_j_i
                    )
                    
                    # Add the addand couplingvariables_term to q_i
                    q_i -= targetshareddesignvariables_term

            # Extend the total vector q by the component vector q_i w.r.t. subsystem i 
            q = np.append(q, q_i)
            
        return q
    
    
    def qp_constraint_equality_matrix(self) -> np.typing.ArrayLike:
        """Compute the constraint matrix A for the ALADIN QP.

        Returns:
            The block-structured matrix A defining the linear equality constraints A*d = 0.
        """
        
        # Build a list of per-subsystem equality constraint matrices
        A: List[np.typing.ArrayLike] = []
        
        # Get local <-> controller coupling parameters
        couplingparameters: List[ControllerCouplingParametersALADIN] = self.get_CouplingParameters()
        
        # Loop over local subsystems i
        for i in range(len(couplingparameters)):
            
            # Get the coupling w.r.t local subsystem i
            coupling_i: ControllerCouplingParametersALADIN = couplingparameters[i]
            
            # Get the dimension of the design variables of subsystem i
            dimension_i: int = len(coupling_i.get_Copy_Jacobian_LowerBound())
            
            # Collect rows for this subsystem
            rows: List[List[float]] = []
            
            # Get the Jacobian of the local equality constraints
            jacobian_alllocalequalityconstraints: List[List[float]] | None = coupling_i.get_Copy_Jacobian_LocalEqualityConstraints() 
            
            if jacobian_alllocalequalityconstraints is not None:
                
                rows += jacobian_alllocalequalityconstraints
        
            # Always append a block for this subsystem (even if 0 rows) to keep 
            # the block-diagonal width consistent with the total design variable dimension
            if len(rows) > 0:
                A.append(np.array(rows, dtype=float))
            else:
                A.append(np.zeros((0, dimension_i)))
        
        # Based on the list of Jacobian parts A, build a block-diagonal matrix
        if len(A) > 0:
            result: np.typing.ArrayLike = block_diag(*A)
        else:
            result = np.zeros((0, 0))
        
        # Return the result
        return result
    
    def qp_constraint_inequality_matrix(self) -> np.typing.ArrayLike:
        """
        Compute the constraint inequality matrix G for the ALADIN QP.

        Returns:
            The block-structured matrix G defining the linear inequality constraints G*d <= h.

        """
        
        # Build a list of per-subsystem constraint inequality / bound matrices
        G: List[np.typing.ArrayLike] = []
        
        # Get local <-> controller coupling parameters
        couplingparameters: List[ControllerCouplingParametersALADIN] = self.get_CouplingParameters()
        
        # Loop over local subsystems i
        for i in range(len(couplingparameters)):
            
            # Get the coupling w.r.t local subsystem i
            coupling_i: ControllerCouplingParametersALADIN = couplingparameters[i]
            
            # Get the dimension of the design variables of subsystem i
            dimension_i: int = len(coupling_i.get_Copy_Jacobian_LowerBound())
            
            # Collect rows for this subsystem
            rows: List[List[float]] = []
            
            # Get the jacobian of the local inequality constraints
            jacobian_alllocalinequalityconstraints: List[List[float]] | None = coupling_i.get_Copy_Jacobian_LocalInequalityConstraints()
            
            if jacobian_alllocalinequalityconstraints is not None:
                
                rows += jacobian_alllocalinequalityconstraints
            
            # Jacobians of bounds - these always exist, hence no check needed
            
            # Get the Jacobian of the active lower bounds
            jacobian_alllowerbounds: List[List[float]] = coupling_i.get_Copy_Jacobian_LowerBound()

            rows += jacobian_alllowerbounds
            
            # Get the Jacobian of the active upper bounds
            jacobian_allupperbounds: List[List[float]] = coupling_i.get_Copy_Jacobian_UpperBound()

            rows += jacobian_allupperbounds
            
            # Always append a block for this subsystem (even if 0 rows) to keep 
            # the block-diagonal width consistent with the total design variable dimension
            if len(rows) > 0:
                G.append(np.array(rows, dtype=float))
            else:
                G.append(np.zeros((0, dimension_i)))
        
        # Based on the list of Jacobian parts G, build a block-diagonal matrix
        if len(G) > 0:
            result: np.typing.ArrayLike = block_diag(*G)
        else:
            result = np.zeros((0, 0))
        
        # Return the result
        return result

    def qp_constraint_inequality_righthandside(self) -> np.typing.ArrayLike:
        """Compute the right-hand side vector h for the inequality constraints of the ALADIN QP.

        Returns:
            The vector h defining the right-hand side of the linear inequality constraints G*d <= h.
        """
        
        # Build a list of per-subsystem constraint inequality / bound matrices
        h: List[float] = []
        
        # Get local <-> controller coupling parameters
        couplingparameters: List[ControllerCouplingParametersALADIN] = self.get_CouplingParameters()
        
        # Loop over local subsystems i
        for i in range(len(couplingparameters)):
            
            # Get the coupling w.r.t local subsystem i
            coupling_i: ControllerCouplingParametersALADIN = couplingparameters[i]

            # Get the local inequality constraint values
            local_inequality_constraints_value: List[float] | None = coupling_i.get_Copy_LocalInequalityConstraintsValue()
            
            if local_inequality_constraints_value is not None:
                
                # Append
                h += local_inequality_constraints_value
            
            # Jacobians of bounds - these always exist, hence no check needed
            
            # Get the lower bound constraints values
            lower_boundconstraints_value = coupling_i.get_Copy_Lower_BoundConstraints_Value()
            
            if lower_boundconstraints_value is not None:
                
                # Append
                h += lower_boundconstraints_value
            
            # Get the Jacobian of the active upper bounds
            upper_boundconstraints_value = coupling_i.get_Copy_Upper_BoundConstraints_Value()
            
            if upper_boundconstraints_value is not None:
                
                # Append
                h += upper_boundconstraints_value
        
        # Assemble the right-hand side vector h as the negated concatenated constraint values
        if len(h) > 0:
            result: np.typing.ArrayLike = - np.array(h, dtype=float)
        else:
            result: np.typing.ArrayLike = np.zeros(0)
        
        # Return the result
        return result
    
    
    def postprocess_Optimization(self) -> None:
        """
        Postprocess optimization.
        """
        
        # NOTE: If solver did not return a feasible point / infeasibility
        # return delta_d = 0, since this is feasible by the QP-constraints
        
        if self.get_OptimData().get_DesignVariables() is not None:
            # Update coupling parameters
            self.mapToCouplingParameters()
    
########################################################################################################
#   Update State Function necessary for running multiprocessing
########################################################################################################
    def update_state(self, other_subsystem: 'ControllerSubSystemALADIN') -> None:
        """Update the state of this ControllerSubSystemALADIN instance with values from another instance.

        This method is necessary for multiprocessing. After parallel execution completes,
        this method updates the original object's attribute values while preserving their
        memory addresses.

        Args:
            other_subsystem: The source ControllerSubSystemALADIN containing updated values
                from parallel execution.
        """
        # Update all attributes inherited from ControllerSubSystemBasis (and SubSystemBasis)
        super().update_state(other_subsystem=other_subsystem)

        # _optimization: OptimizationController - strategy object, no update needed

        # _indices_map: Dict[Tuple[str, str], List[List[int]]] - mutable state
        # copy.deepcopy() used - contains nested mutable lists
        self._indices_map = copy.deepcopy(other_subsystem._indices_map)
```
