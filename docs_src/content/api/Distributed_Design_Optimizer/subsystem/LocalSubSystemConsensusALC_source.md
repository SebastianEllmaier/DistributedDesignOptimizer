---
title: LocalSubSystemConsensusALC (Source)
---

← Back to [LocalSubSystemConsensusALC documentation](LocalSubSystemConsensusALC.md)

# LocalSubSystemConsensusALC - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\LocalSubSystemConsensusALC.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Consensus ALC local subsystem module.

This module provides the local subsystem implementation for the
consensus-based Augmented Lagrangian Coordination method.
"""

from typing import List, Type
import numpy as np
from numpy.typing import NDArray
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print, ddo_print_border
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.optimization import AnalysisInterface, OptimizationInterface
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalObjectiveInterface, LocalConstraintsInterface
from Distributed_Design_Optimizer.subsystem.couplingparameters.consensus_alc import CouplingParametersConsensusALC
from Distributed_Design_Optimizer.middlelevel.consensus_alc import InConsistencySize
from Distributed_Design_Optimizer.middlelevel import InConsistencySizeInterface
from Distributed_Design_Optimizer.coordination.convergence import (Local_ConvergenceIndicator_Innerloop_Interface,
                                                                   Local_ConvergenceIndicator_Innerloop_DeWit,
                                                                   Local_ConvergenceIndicator_Outerloop_Interface,
                                                                   Local_ConvergenceIndicator_Outerloop_DeWit
                                                                   )
from Distributed_Design_Optimizer.coordination.updatecouplingparametermethod import (UpdateCouplingParameterMethodInterface,
                                                                                     UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights
                                                                                     )


class LocalSubSystemConsensusALC(LocalSubSystemBasis):
    """Local subsystem for consensus-based ALC coordination.

    Implements the local subsystem functionality for consensus-based
    Augmented Lagrangian Coordination.
    """
        
    def __init__(self,
                 id: str,
                 level: int,
                 neighborid: List[str],
                 analysis: AnalysisInterface,
                 localobjective: LocalObjectiveInterface,
                 localconstraints: LocalConstraintsInterface,
                 optimization: OptimizationInterface,
                 local_convergenceindicator_innerloop: Local_ConvergenceIndicator_Innerloop_Interface,
                 local_convergenceindicator_outerloop: Local_ConvergenceIndicator_Outerloop_Interface,
                 updatecouplingparametermethod_outerloop: UpdateCouplingParameterMethodInterface
                 ) -> None:
        """Create a new LocalSubSystemConsensusALC instance.

        Args:
            id: Identifier for the subsystem.
            level: Level identifier for the subsystem in the hierarchy.
            neighborid: List of identifiers for neighboring subsystems.
            analysis: Analysis interface for subsystem evaluation.
            localobjective: Local objective function class.
            localconstraints: Local constraint functions class.
            optimization: Optimization interface for solving local problems.
            local_convergenceindicator_innerloop: Local convergence indicator for inner loop.
            local_convergenceindicator_outerloop: Local convergence indicator for outer loop.
            updatecouplingparametermethod_outerloop: Method for updating coupling parameters in outer loop.
        """
        # Compatibility settings for the components handed to this subsystem by the
        # Consensus_ALC coordination method. These are validated here (rather than in
        # Consensus_ALC) because the corresponding objects are handed to this subsystem.

        # Allowed / recommended outerloop update coupling parameter methods for Consensus_ALC
        self._allowedupdatemethods_outerloop: List[Type[UpdateCouplingParameterMethodInterface]] = [
            UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights
        ]
        self._recommendedupdatemethods_outerloop: List[Type[UpdateCouplingParameterMethodInterface]] = [
            UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights
        ]

        # Allowed / recommended local inner loop convergence indicators for Consensus_ALC
        self._allowedconvergenceindicators_innerloop: List[Type[Local_ConvergenceIndicator_Innerloop_Interface]] = [
            Local_ConvergenceIndicator_Innerloop_DeWit
        ]
        self._recommendedconvergenceindicators_innerloop: List[Type[Local_ConvergenceIndicator_Innerloop_Interface]] = [
            Local_ConvergenceIndicator_Innerloop_DeWit
        ]

        # Allowed / recommended local outer loop convergence indicators for Consensus_ALC
        self._allowedconvergenceindicators_outerloop: List[Type[Local_ConvergenceIndicator_Outerloop_Interface]] = [
            Local_ConvergenceIndicator_Outerloop_DeWit
        ]
        self._recommendedconvergenceindicators_outerloop: List[Type[Local_ConvergenceIndicator_Outerloop_Interface]] = [
            Local_ConvergenceIndicator_Outerloop_DeWit
        ]

        self._couplingparameters: List[CouplingParametersConsensusALC] = [CouplingParametersConsensusALC(neighbor_id) for neighbor_id in neighborid]
        
        # super() initialization is not called at the top,
        # since evaluateAllJacobians needs optimdata, and initialization of optimdata needs couplingparameters
        super().__init__(id, level, neighborid, analysis, localobjective, localconstraints, optimization)
        
        # Convergence indicators - passed from Consensus_ALC
        self._local_convergenceindicator_innerloop: Local_ConvergenceIndicator_Innerloop_DeWit = local_convergenceindicator_innerloop
        self._local_convergenceindicator_outerloop: Local_ConvergenceIndicator_Outerloop_DeWit = local_convergenceindicator_outerloop
        
        self._inconsistencies: List[InConsistencySize] = [InConsistencySize(self.get_CouplingParameters()[i].get_ID())
                                                          for i in range(len(self.get_CouplingParameters()))]
        
        self._updatecouplingparametermethod_outerloop: UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights = updatecouplingparametermethod_outerloop
        
        # Validate the components handed to this subsystem
        self.validate_inputs()

    def validate_inputs(self) -> None:
        """Validate the components handed to this subsystem by the Consensus_ALC coordination method.

        Validates that the outer-loop update coupling parameter method and the local
        inner/outer loop convergence indicators are compatible with Consensus_ALC.

        Raises:
            ValueError: If a provided component is not compatible with Consensus_ALC.
        """
        # ===== updatecouplingparametermethod_outerloop Validation =====
        if type(self._updatecouplingparametermethod_outerloop) not in self._allowedupdatemethods_outerloop:
            raise ValueError(
                f"{DDO_Color}Outerloop update method '{type(self._updatecouplingparametermethod_outerloop).__name__}' is not compatible with Consensus_ALC. "
                f"Please choose one of the compatible methods: {[m.__name__ for m in self._allowedupdatemethods_outerloop]}{Reset}"
            )
        elif type(self._updatecouplingparametermethod_outerloop) not in self._recommendedupdatemethods_outerloop:
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: Outerloop update method '{type(self._updatecouplingparametermethod_outerloop).__name__}' is not recommended for Consensus_ALC.")
            ddo_print(f"{type(self).__name__}: Recommended methods: {[m.__name__ for m in self._recommendedupdatemethods_outerloop]}")
            ddo_print_border()

        # ===== Convergence Indicator Inner Validation =====
        if type(self._local_convergenceindicator_innerloop) not in self._allowedconvergenceindicators_innerloop:
            raise ValueError(
                f"{DDO_Color}Inner loop convergence indicator '{type(self._local_convergenceindicator_innerloop).__name__}' is not compatible with Consensus_ALC. "
                f"Please choose one of the compatible indicators: {[c.__name__ for c in self._allowedconvergenceindicators_innerloop]}{Reset}"
            )
        elif type(self._local_convergenceindicator_innerloop) not in self._recommendedconvergenceindicators_innerloop:
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: Inner loop convergence indicator '{type(self._local_convergenceindicator_innerloop).__name__}' is not recommended for Consensus_ALC.")
            ddo_print(f"{type(self).__name__}: Recommended indicators: {[c.__name__ for c in self._recommendedconvergenceindicators_innerloop]}")
            ddo_print_border()

        # ===== Convergence Indicator Outer Validation =====
        if type(self._local_convergenceindicator_outerloop) not in self._allowedconvergenceindicators_outerloop:
            raise ValueError(
                f"{DDO_Color}Outer loop convergence indicator '{type(self._local_convergenceindicator_outerloop).__name__}' is not compatible with Consensus_ALC. "
                f"Please choose one of the compatible indicators: {[c.__name__ for c in self._allowedconvergenceindicators_outerloop]}{Reset}"
            )
        elif type(self._local_convergenceindicator_outerloop) not in self._recommendedconvergenceindicators_outerloop:
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: Outer loop convergence indicator '{type(self._local_convergenceindicator_outerloop).__name__}' is not recommended for Consensus_ALC.")
            ddo_print(f"{type(self).__name__}: Recommended indicators: {[c.__name__ for c in self._recommendedconvergenceindicators_outerloop]}")
            ddo_print_border()
    
################################################################################################################
#   Basics of the subsystem
################################################################################################################
    
    def append_Controller(self) -> None:
        """Update local subsystems by appending controller.
        """
        
        # Consensus ALC does not have a controller, hence, this function is empty
        pass 
    
##############################################################################################################
#   Functions to evaluate a subsystem's responses and map them onto coupling parameters
##############################################################################################################
    
    def mapToController(self) -> None:
        """Pass, since no controller in consensus ALC.
        """
        
        pass
    
    def evaluate_Gradient_CoordinationObjective(self) -> None:
        """Evaluate the analytical gradient of the coordination objective.

        Assumes the mapped responses Jacobian was evaluated already.
        """
        
        # TODO
        pass
    
    def evaluate_Jacobian_CoordinationEqualityConstraints(self) -> None:
        """Evaluate the Jacobian of the coordination equality constraints.

        Consensus ALC does not have coordination equality constraints, hence no-op.
        """
        # No coordination equality constraints in Consensus ALC
        pass
    
    def evaluate_Jacobian_CoordinationInEqualityConstraints(self) -> None:
        """Evaluate the Jacobian of the coordination inequality constraints.

        Consensus ALC does not have coordination inequality constraints, hence no-op.
        """
        # No coordination inequality constraints in Consensus ALC
        pass
    
##############################################################################################################
#   Functions to evaluate a subsystem's optimization objective and constraints for given responses
##############################################################################################################
 
    def evaluateCoordinationObjective(self) -> None:
        """Evaluate the coordination objective.
        """
        couplingin: List[CouplingParametersConsensusALC] = self.get_CouplingParameters()
        normcoupl = np.zeros(len(couplingin))
        inconsistency: List[InConsistencySize] = [InConsistencySize(couplingin[i].get_ID())
                                                  for i in range(len(couplingin))]
        
        for i in range(len(couplingin)):
            penalty_aux_minus_mapres = None
            penalty_aux_minus_coupl = None
            penalty_aux_minus_shared = None
            penalty_aux_minus_tgtshared = None

            lagrangian_aux_minus_mapres = None
            lagrangian_aux_minus_coupl = None
            lagrangian_aux_minus_shared = None
            lagrangian_aux_minus_tgtshared = None
            
            if ((couplingin[i].get_Copy_CouplingVariable() is not None) and
                    (couplingin[i].get_MappedResponses() is not None)):
                # Consensus constraint violation between the auxiliary variable and the mapped response
                auxmapres: List[float] = couplingin[i].get_Auxiliary_MappedResponse()
                mapres: List[float] = couplingin[i].get_MappedResponses()
                
                inconsistency[i].evaluate_Auxiliary_Minus_MappedResponse(auxiliary=auxmapres, mappedresponse=mapres)
                
                penalty_aux_minus_mapres = np.array(couplingin[i].get_Weights_Auxiliary_Minus_MappedResponse()) * np.array(inconsistency[i].get_Auxiliary_Minus_MappedResponse())  # element-wise multiplication
                lagrangian_aux_minus_mapres = np.array(couplingin[i].get_Multipliers_Auxiliary_Minus_MappedResponse()) * np.array(inconsistency[i].get_Auxiliary_Minus_MappedResponse())  # element-wise multiplication
            else:
                penalty_aux_minus_mapres = np.array([0.0])
                lagrangian_aux_minus_mapres = np.array([0.0])
            
            if ((couplingin[i].get_CouplingVariable() is not None) and
                    (couplingin[i].get_Copy_MappedResponses() is not None)):
                # Consensus constraint violation between the auxiliary variable and the coupling variable
                auxcoupl: List[float] = couplingin[i].get_Auxiliary_CouplingVariable()
                coupl: List[float] = couplingin[i].get_CouplingVariable()
                
                inconsistency[i].evaluate_Auxiliary_Minus_CouplingVariable(auxiliary=auxcoupl, couplingvariable=coupl)
                
                penalty_aux_minus_coupl = np.array(couplingin[i].get_Weights_Auxiliary_Minus_CouplingVariable()) * np.array(inconsistency[i].get_Auxiliary_Minus_CouplingVariable())  # element-wise multiplication
                lagrangian_aux_minus_coupl = np.array(couplingin[i].get_Multipliers_Auxiliary_Minus_CouplingVariable()) * np.array(inconsistency[i].get_Auxiliary_Minus_CouplingVariable())  # element-wise multiplication
            else:
                penalty_aux_minus_coupl = np.array([0.0])
                lagrangian_aux_minus_coupl = np.array([0.0])

            if ((couplingin[i].get_Copy_TargetSharedDesignVariables() is not None) and
                    (couplingin[i].get_SharedDesignVariables() is not None)):
                # Consensus constraint violation between the auxiliary variable and the shared design variables
                auxshared: List[float] = couplingin[i].get_Auxiliary_SharedDesignVariable()
                shared: List[float] = couplingin[i].get_SharedDesignVariables()
                
                inconsistency[i].evaluate_Auxiliary_Minus_SharedDesignVariable(auxiliary=auxshared, shareddesignvariable=shared)
                                
                penalty_aux_minus_shared = np.array(couplingin[i].get_Weights_Auxiliary_Minus_SharedDesignVariable()) * np.array(inconsistency[i].get_Auxiliary_Minus_SharedDesignVariable())  # element-wise multiplication
                lagrangian_aux_minus_shared = np.array(couplingin[i].get_Multipliers_Auxiliary_Minus_SharedDesignVariable()) * np.array(inconsistency[i].get_Auxiliary_Minus_SharedDesignVariable())  # element-wise multiplication
            else:
                penalty_aux_minus_shared = np.array([0.0])
                lagrangian_aux_minus_shared = np.array([0.0])

            if ((couplingin[i].get_Copy_SharedDesignVariables() is not None) and
                    (couplingin[i].get_TargetSharedDesignVariables() is not None)):
                # Consensus constraint violation between the auxiliary variable and the target shared design variables
                auxtgtshared: List[float] = couplingin[i].get_Auxiliary_TargetSharedDesignVariable()
                tgtshared: List[float] = couplingin[i].get_TargetSharedDesignVariables()
                
                inconsistency[i].evaluate_Auxiliary_Minus_TargetSharedDesignVariable(auxiliary=auxtgtshared, targetshareddesignvariable=tgtshared)

                penalty_aux_minus_tgtshared = np.array(couplingin[i].get_Weights_Auxiliary_Minus_TargetSharedDesignVariable()) * np.array(inconsistency[i].get_Auxiliary_Minus_TargetSharedDesignVariable())  # element-wise multiplication
                lagrangian_aux_minus_tgtshared = np.array(couplingin[i].get_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable()) * np.array(inconsistency[i].get_Auxiliary_Minus_TargetSharedDesignVariable())  # element-wise multiplication
            else:
                penalty_aux_minus_tgtshared = np.array([0.0])
                lagrangian_aux_minus_tgtshared = np.array([0.0])

            # Evaluate the objective inconsistency function
            normcoupl[i] = np.power(np.linalg.norm(np.concatenate((penalty_aux_minus_mapres, penalty_aux_minus_coupl, penalty_aux_minus_shared, penalty_aux_minus_tgtshared))),2)
            normcoupl[i] = normcoupl[i] + np.sum(lagrangian_aux_minus_coupl) + np.sum(lagrangian_aux_minus_mapres) + np.sum(lagrangian_aux_minus_shared) + np.sum(lagrangian_aux_minus_tgtshared)

        # Compute the sum of all the penalty function contributions
        phinorm = np.array(normcoupl)
        objective_inconsistency = float(np.sum(phinorm))
                
        # set the objective inconsistency value to subsystem object
        self.set_CoordinationObjectiveValue(objective_inconsistency)
        
    def evaluateCoordinationEqualityConstraint(self) -> None:
        """Evaluate the coordination equality constraint.
        """
        couplingin: List[CouplingParametersConsensusALC] = self.get_CouplingParameters()
        #########################################################################################################
        constraint_inconsistency = None
        #########################################################################################################
        self.set_CoordinationEqualityConstraintValue(constraint_inconsistency)

    def evaluateCoordinationInequalityConstraint(self) -> None:
        """Evaluate the coordination inequality constraint.
        """
        couplingin: List[CouplingParametersConsensusALC] = self.get_CouplingParameters()
        #########################################################################################################
        constraint_inconsistency = None
        #########################################################################################################
        self.set_CoordinationInequalityConstraintValue(constraint_inconsistency)

##############################################################################################################
#   Functions to prepare, solve and postprocess a subsystem's optimization problem
##############################################################################################################

    def prepare_OptimizationProblem(self) -> None:
        """Prepare the optimization problem.
        """
        pass  # this coordination method does not require any dedicated preparation step
    
    def postprocess_Optimization(self) -> None:
        """Postprocess the optimization.
        """
        pass  # this coordination method does not require any dedicated preparation step
    
#############################################################################################################
#   Functions to handle reference data provided by user used to perform algorithm analysis
#############################################################################################################
    
###############################################################################################################
#   Functions to handle coupling parameters related to modelling a distributed optimization problem.
#   This only works on mappedresponses, couplingvariables, shareddesignvariables, targetshareddesignvariables
#   and their copy_-counterparts.
#   Nothing related to coupling parameters
###############################################################################################################
 
    def return_initialized_CouplingParameters(self) -> List[CouplingParametersConsensusALC]:
        """Return initialized coupling parameters.

        Returns:
            Initialized coupling parameters for each neighbor.
        """
        
        initialized_couplingparameters: List[CouplingParametersConsensusALC] = [CouplingParametersConsensusALC(self.get_CouplingParameters()[i].get_ID())
                                                                                for i in range(len(self.get_CouplingParameters()))]
        return initialized_couplingparameters
    
########################################################################################################
#   Functions to handle coupling parameters
#######################################################################################################

    def update_AuxiliaryVariables(self, coupling: CouplingParametersConsensusALC) -> None:
        """Create initial and then update auxiliary variables using the update formula.

        Uses the initial values defined in the input file.

        Args:
            coupling: Coupling parameters for a consensus ALC neighbor.
        """
        
        # Get id of neighbouring subsystem
        neighborid: str = coupling.get_ID()
        
        # Initialize auxiliary-minus-mapped-response coupling parameters
        if ((coupling.get_Copy_CouplingVariable() is not None) and
                (coupling.get_MappedResponses() is not None)):
            
            mappedresponse: List[float] = coupling.get_MappedResponses()
            copycoupling: List[float] = coupling.get_Copy_CouplingVariable()
            
            multipliers_aux_minus_mappedresponse: List[float] = coupling.get_Multipliers_Auxiliary_Minus_MappedResponse()
            multipliers_copy_aux_minus_couplingvariable: List[float] = coupling.get_Copy_Multipliers_Auxiliary_Minus_CouplingVariable()
            
            weights_aux_minus_mappedresponse: List[float] = coupling.get_Weights_Auxiliary_Minus_MappedResponse()
            weights_copy_aux_minus_couplingvariable: List[float] = coupling.get_Copy_Weights_Auxiliary_Minus_CouplingVariable()
            
            # Update-formula (weighted-average closed form using squared weights)
            auxiliary_mappedresponse: NDArray = (- 0.5 * (np.array(multipliers_aux_minus_mappedresponse) + np.array(multipliers_copy_aux_minus_couplingvariable))
                                                 + (np.array(weights_aux_minus_mappedresponse)**2) * np.array(mappedresponse)
                                                 + (np.array(weights_copy_aux_minus_couplingvariable)**2) * np.array(copycoupling)
                                                 ) / ((np.array(weights_aux_minus_mappedresponse)**2) + (np.array(weights_copy_aux_minus_couplingvariable)**2))
            
            # Set auxiliary-minus-mapped-response variables as computed result
            self.set_AuxiliaryVariables_MappedResponse(neighborid, auxiliary_mappedresponse.tolist())
            
        # Initialize auxiliary-minus-coupling-variable coupling parameters
        if ((coupling.get_CouplingVariable() is not None) and 
                (coupling.get_Copy_MappedResponses() is not None)):
            
            couplingvariables: List[float] = coupling.get_CouplingVariable()
            copymappedresponses: List[float] = coupling.get_Copy_MappedResponses()
            
            multipliers_aux_minus_couplingvariable: List[float] = coupling.get_Multipliers_Auxiliary_Minus_CouplingVariable()
            multipliers_copy_aux_minus_mappedresponse: List[float] = coupling.get_Copy_Multipliers_Auxiliary_Minus_MappedResponse()
            
            weights_aux_minus_couplingvariable: List[float] = coupling.get_Weights_Auxiliary_Minus_CouplingVariable()
            weights_copy_aux_minus_mappedresponse: List[float] = coupling.get_Copy_Weights_Auxiliary_Minus_MappedResponse()
            
            # Update-formula (weighted-average closed form using squared weights)
            auxiliary_couplingvariable: NDArray = (- 0.5 * (np.array(multipliers_aux_minus_couplingvariable) + np.array(multipliers_copy_aux_minus_mappedresponse))
                                                   + (np.array(weights_aux_minus_couplingvariable)**2) * np.array(couplingvariables)
                                                   + (np.array(weights_copy_aux_minus_mappedresponse)**2) * np.array(copymappedresponses)
                                                   ) / ((np.array(weights_aux_minus_couplingvariable)**2) + (np.array(weights_copy_aux_minus_mappedresponse)**2))
            
            # Set auxiliary-minus-coupling-variable variables as computed result
            self.set_AuxiliaryVariables_CouplingVariable(neighborid, auxiliary_couplingvariable.tolist())
            
        # Initialize shared auxiliary coupling parameters
        if ((coupling.get_SharedDesignVariables() is not None) and 
                (coupling.get_Copy_TargetSharedDesignVariables() is not None)):
            
            shared: List[float] = coupling.get_SharedDesignVariables()
            copytargetshared: List[float] = coupling.get_Copy_TargetSharedDesignVariables()
            
            multipliers_aux_minus_shared: List[float] = coupling.get_Multipliers_Auxiliary_Minus_SharedDesignVariable()
            multipliers_copy_aux_minus_targetshared: List[float] = coupling.get_Copy_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable()
            
            weights_aux_minus_shared: List[float] = coupling.get_Weights_Auxiliary_Minus_SharedDesignVariable()
            weights_copy_aux_minus_targetshared: List[float] = coupling.get_Copy_Weights_Auxiliary_Minus_TargetSharedDesignVariable()
            
            # Update-formula (weighted-average closed form using squared weights)
            auxiliaryshared: NDArray = (- 0.5 * (np.array(multipliers_aux_minus_shared) + np.array(multipliers_copy_aux_minus_targetshared))
                                        + (np.array(weights_aux_minus_shared)**2) * np.array(shared)
                                        + (np.array(weights_copy_aux_minus_targetshared)**2) * np.array(copytargetshared)
                                        ) / ((np.array(weights_aux_minus_shared)**2) + (np.array(weights_copy_aux_minus_targetshared)**2))
            
            # Set shared auxiliary variables as computed result
            self.set_AuxiliaryVariables_SharedDesignVariable(neighborid, auxiliaryshared.tolist())
            
        # Initialize target shared coupling parameters
        if ((coupling.get_TargetSharedDesignVariables() is not None) and 
                (coupling.get_Copy_SharedDesignVariables() is not None)):
            
            targetshared: List[float] = coupling.get_TargetSharedDesignVariables()
            copyshared: List[float] = coupling.get_Copy_SharedDesignVariables()
            
            multipliers_aux_minus_targetshared: List[float] = coupling.get_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable()
            multipliers_copy_aux_minus_shared: List[float] = coupling.get_Copy_Multipliers_Auxiliary_Minus_SharedDesignVariable()
            
            weights_aux_minus_targetshared: List[float] = coupling.get_Weights_Auxiliary_Minus_TargetSharedDesignVariable()
            weights_copy_aux_minus_shared: List[float] = coupling.get_Copy_Weights_Auxiliary_Minus_SharedDesignVariable()
            
            # Update-formula (weighted-average closed form using squared weights)
            auxiliarytargetshared: NDArray = (- 0.5 * (np.array(multipliers_aux_minus_targetshared) + np.array(multipliers_copy_aux_minus_shared))
                                              + (np.array(weights_aux_minus_targetshared)**2) * np.array(targetshared)
                                              + (np.array(weights_copy_aux_minus_shared)**2) * np.array(copyshared)
                                              ) / ((np.array(weights_aux_minus_targetshared)**2) + (np.array(weights_copy_aux_minus_shared)**2))
            
            # Set target shared auxiliary variables as computed result
            self.set_AuxiliaryVariables_TargetSharedDesignVariable(neighborid, auxiliarytargetshared.tolist())            
    
    def initializeCouplingParameters_before_CopyToMiddleLevel(self) -> None:
        """Initialize coupling parameters before copying communicated information.

        Create empty placeholders for coupling parameters, i.e. communicated quantities in the algorithms, 
        Lagrange multipliers, penalty weights, ...
        The sizes are read by already initialized quantities from the inner loop iteration.
        """
        pass
    
    def initializeCouplingParameters_after_CopyFromMiddleLevel(self) -> None:
        """Initialize coupling parameters after copying communicated information.

        Create empty placeholders for coupling parameters, i.e. communicated quantities in the algorithms, 
        Lagrange multipliers, penalty weights, ...
        The sizes are read by already initialized quantities from the inner loop iteration.
        """
        
        coupling: List[CouplingParametersConsensusALC] = self.get_CouplingParameters()
        
        for i in range(len(coupling)):
            neighborid: str = coupling[i].get_ID()
            
            # Initialize auxiliary-minus-mapped-response coupling parameters
            if ((coupling[i].get_Copy_CouplingVariable() is not None) and
                    (coupling[i].get_MappedResponses() is not None)):
                
                initpenaltyl: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialWeight()] * len(coupling[i].get_MappedResponses())
                initmultipll: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialMultiplier()] * len(coupling[i].get_MappedResponses())
                
                self.set_CoordinationWeights_Auxiliary_Minus_MappedResponse(neighborid, initpenaltyl)
                self.set_CoordinationMultipliers_Auxiliary_Minus_MappedResponse(neighborid, initmultipll)
            
            # initialize the auxiliary-minus-coupling-variable coupling parameters
            if ((coupling[i].get_CouplingVariable() is not None) and
                    (coupling[i].get_Copy_MappedResponses() is not None)):
                initpenaltyr: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialWeight()] * len(coupling[i].get_CouplingVariable())
                initmultiplr: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialMultiplier()] * len(coupling[i].get_CouplingVariable())
                
                self.set_CoordinationWeights_Auxiliary_Minus_CouplingVariable(neighborid, initpenaltyr)
                self.set_CoordinationMultipliers_Auxiliary_Minus_CouplingVariable(neighborid, initmultiplr)
            
            # initialize the shared design variables coupling parameters
            if ((coupling[i].get_Copy_TargetSharedDesignVariables() is not None) and
                    (coupling[i].get_SharedDesignVariables() is not None)):
                initpenaltysd: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialWeight()] * len(coupling[i].get_SharedDesignVariables())
                initmultiplsd: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialMultiplier()] * len(coupling[i].get_SharedDesignVariables())
                
                self.set_CoordinationWeights_Auxiliary_Minus_SharedDesignVariable(neighborid, initpenaltysd)
                self.set_CoordinationMultipliers_Auxiliary_Minus_SharedDesignVariable(neighborid, initmultiplsd)
            
            # initialize the shared target variables coupling parameters
            if ((coupling[i].get_Copy_SharedDesignVariables() is not None) and
                    (coupling[i].get_TargetSharedDesignVariables() is not None)):
                initpenaltytsd: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialWeight()] * len(coupling[i].get_TargetSharedDesignVariables())
                initmultipltsd: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialMultiplier()] * len(coupling[i].get_TargetSharedDesignVariables())
                
                self.set_CoordinationWeights_Auxiliary_Minus_TargetSharedDesignVariable(neighborid, initpenaltytsd)
                self.set_CoordinationMultipliers_Auxiliary_Minus_TargetSharedDesignVariable(neighborid, initmultipltsd)
            
    def initializeCouplingParameters_after_Second_CopyFromMiddleLevel(self) -> None:
        """Initialize coupling parameters after two communication rounds between subsystems.
        """
        
        coupling: List[CouplingParametersConsensusALC] = self.get_CouplingParameters()
        
        for i in range(len(coupling)):            
            # Initialize auxiliary variables by calling update_AuxiliaryVariables
            self.update_AuxiliaryVariables(coupling[i])    
                
    def prepare_updateCouplingParameters(self) -> None:
        """Prepare coupling parameters before update operations.

        Consensus ALC does not have any outer loop preparations
        to update the coupling parameters.
        """
        pass
    
    def updateCouplingParameters_innerLoop(self) -> None:
        """Update auxiliary variables in inner loop directly after local subsystem updates -> See pseudocode.
        """
        
        couplings: List[CouplingParametersConsensusALC] = self.get_CouplingParameters()
        
        # Loop over all the coupling circles / neighbors
        for i in range(len(couplings)):
            # Get coupling i
            coupling: CouplingParametersConsensusALC = couplings[i]
            # update auxiliary variables
            self.update_AuxiliaryVariables(coupling)
    
    def updateCouplingParameters_outerLoop(self) -> None:
        """Update coupling parameters in the outer loop.
        """
        coupling: List[CouplingParametersConsensusALC] = self.get_CouplingParameters()
        
        inconsistencies_previous_outerloop_itr: List[InConsistencySize] = self.copy_Inconsistencies_Previous_outerloop_itr()
        
        # loop over all the consensus coupling circles/neighbors
        for j in range(len(coupling)):

            # get the identifier of the neighboring subsystem
            neighborid: str = coupling[j].get_ID()
                
            # auxiliary-minus-mapped-response part of the consensus coupling circle
            if ((coupling[j].get_Multipliers_Auxiliary_Minus_MappedResponse() is not None) and (self._inconsistencies[j].get_Auxiliary_Minus_MappedResponse() is not None)):
                # Getters return defensive copies - modifications below only affect local copies
                multipliersin: List[float] = coupling[j].get_Multipliers_Auxiliary_Minus_MappedResponse()
                penaltyweightsin: List[float] = coupling[j].get_Weights_Auxiliary_Minus_MappedResponse()
                inconsistency: List[float] = self._inconsistencies[j].get_Auxiliary_Minus_MappedResponse()
                inconsistency_previous_outerloop_itr: List[float] | None = inconsistencies_previous_outerloop_itr[j].get_Auxiliary_Minus_MappedResponse()
                        
                # update consensus coordination multipliers (modifies multipliersin in-place)
                self._updatecouplingparametermethod_outerloop.update_CoordinationMultipliers(multipliersin, penaltyweightsin, inconsistency)
                # Setter required to store modified copy back
                self.set_CoordinationMultipliers_Auxiliary_Minus_MappedResponse(neighborid, multipliersin)
                
                # update consensus coordination weights (modifies penaltyweightsin in-place)
                self._updatecouplingparametermethod_outerloop.update_CoordinationWeights(penaltyweightsin, inconsistency, inconsistency_previous_outerloop_itr)
                # Setter required to store modified copy back
                self.set_CoordinationWeights_Auxiliary_Minus_MappedResponse(neighborid, penaltyweightsin)

            # auxiliary-minus-coupling-variable part of the consensus coupling circle
            if ((coupling[j].get_Multipliers_Auxiliary_Minus_CouplingVariable() is not None) and (self._inconsistencies[j].get_Auxiliary_Minus_CouplingVariable() is not None)):
                # Getters return defensive copies - modifications below only affect local copies
                multipliersin: List[float] = coupling[j].get_Multipliers_Auxiliary_Minus_CouplingVariable()
                penaltyweightsin: List[float] = coupling[j].get_Weights_Auxiliary_Minus_CouplingVariable()
                inconsistency: List[float] = self._inconsistencies[j].get_Auxiliary_Minus_CouplingVariable()
                inconsistency_previous_outerloop_itr: List[float] | None = inconsistencies_previous_outerloop_itr[j].get_Auxiliary_Minus_CouplingVariable()
                                    
                # update consensus coordination multipliers (modifies multipliersin in-place)
                self._updatecouplingparametermethod_outerloop.update_CoordinationMultipliers(multipliersin, penaltyweightsin, inconsistency)
                # Setter required to store modified copy back
                self.set_CoordinationMultipliers_Auxiliary_Minus_CouplingVariable(neighborid, multipliersin)
                
                # update consensus coordination weights (modifies penaltyweightsin in-place)
                self._updatecouplingparametermethod_outerloop.update_CoordinationWeights(penaltyweightsin, inconsistency, inconsistency_previous_outerloop_itr)      
                # Setter required to store modified copy back
                self.set_CoordinationWeights_Auxiliary_Minus_CouplingVariable(neighborid, penaltyweightsin)
            
            # shared part of the consensus coupling circle
            if ((coupling[j].get_Multipliers_Auxiliary_Minus_SharedDesignVariable() is not None) and (self._inconsistencies[j].get_Auxiliary_Minus_SharedDesignVariable() is not None)):
                # Getters return defensive copies - modifications below only affect local copies
                multipliersin: List[float] = coupling[j].get_Multipliers_Auxiliary_Minus_SharedDesignVariable()
                penaltyweightsin: List[float] = coupling[j].get_Weights_Auxiliary_Minus_SharedDesignVariable()
                inconsistency: List[float] = self._inconsistencies[j].get_Auxiliary_Minus_SharedDesignVariable()
                inconsistency_previous_outerloop_itr: List[float] | None = inconsistencies_previous_outerloop_itr[j].get_Auxiliary_Minus_SharedDesignVariable()
                                        
                # update consensus coordination multipliers (modifies multipliersin in-place)
                self._updatecouplingparametermethod_outerloop.update_CoordinationMultipliers(multipliersin, penaltyweightsin, inconsistency)
                # Setter required to store modified copy back
                self.set_CoordinationMultipliers_Auxiliary_Minus_SharedDesignVariable(neighborid, multipliersin)
                
                # update consensus coordination weights (modifies penaltyweightsin in-place)
                self._updatecouplingparametermethod_outerloop.update_CoordinationWeights(penaltyweightsin, inconsistency, inconsistency_previous_outerloop_itr)      
                # Setter required to store modified copy back
                self.set_CoordinationWeights_Auxiliary_Minus_SharedDesignVariable(neighborid, penaltyweightsin)
            
            # target part of the consensus coupling circle
            if ((coupling[j].get_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable() is not None) and (self._inconsistencies[j].get_Auxiliary_Minus_TargetSharedDesignVariable() is not None)):
                # Getters return defensive copies - modifications below only affect local copies
                multipliersin: List[float] = coupling[j].get_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable()
                penaltyweightsin: List[float] = coupling[j].get_Weights_Auxiliary_Minus_TargetSharedDesignVariable()
                inconsistency: List[float] = self._inconsistencies[j].get_Auxiliary_Minus_TargetSharedDesignVariable()
                inconsistency_previous_outerloop_itr: List[float] | None = inconsistencies_previous_outerloop_itr[j].get_Auxiliary_Minus_TargetSharedDesignVariable()
                                        
                # update consensus coordination multipliers (modifies multipliersin in-place)
                self._updatecouplingparametermethod_outerloop.update_CoordinationMultipliers(multipliersin, penaltyweightsin, inconsistency)
                # Setter required to store modified copy back
                self.set_CoordinationMultipliers_Auxiliary_Minus_TargetSharedDesignVariable(neighborid, multipliersin)
                
                # update consensus coordination weights (modifies penaltyweightsin in-place)
                self._updatecouplingparametermethod_outerloop.update_CoordinationWeights(penaltyweightsin, inconsistency, inconsistency_previous_outerloop_itr)      
                # Setter required to store modified copy back
                self.set_CoordinationWeights_Auxiliary_Minus_TargetSharedDesignVariable(neighborid, penaltyweightsin)
                
            # Assert if weights are all positive, else throw exception: Auxiliary update formula has division by zero
            if coupling[j].get_Weights_Auxiliary_Minus_MappedResponse() is not None and 0.0 in coupling[j].get_Weights_Auxiliary_Minus_MappedResponse():
                raise ValueError(f"{DDO_Color}One component of the (auxiliary-minus-mapped-response) weights vector was assigned as zero, which is not allowed due to division by the weights.{Reset}")
            if coupling[j].get_Weights_Auxiliary_Minus_CouplingVariable() is not None and 0.0 in coupling[j].get_Weights_Auxiliary_Minus_CouplingVariable():
                raise ValueError(f"{DDO_Color}One component of the (auxiliary-minus-coupling-variable) weights vector was assigned as zero, which is not allowed due to division by the weights.{Reset}")
            if coupling[j].get_Weights_Auxiliary_Minus_SharedDesignVariable() is not None and 0.0 in coupling[j].get_Weights_Auxiliary_Minus_SharedDesignVariable():
                raise ValueError(f"{DDO_Color}One component of the (shared design variable) weights vector was assigned as zero, which is not allowed due to division by the weights.{Reset}")
            if coupling[j].get_Weights_Auxiliary_Minus_TargetSharedDesignVariable() is not None and 0.0 in coupling[j].get_Weights_Auxiliary_Minus_TargetSharedDesignVariable():
                raise ValueError(f"{DDO_Color}One component of the (target shared design variables) weights vector was assigned as zero, which is not allowed due to division by the weights.{Reset}")
                
    def evaluate_Inconsistencies(self) -> None:
        """Compute the difference between stored coupling and mapped variables.

        Compares to the latest available data from a subsystem, including consensus constraint violations.
        Computes four + four inconsistency vectors. The first vector is the auxiliary-minus-mapped-response differences of
        the coupling circle. The second vector is the auxiliary-minus-coupling-variable differences of the coupling circle.
        The third and fourth are the difference between the shared design variable vector.
        Similarly, there are four vectors for the consensus constraints.
        """    
        super().evaluate_Inconsistencies()
        couplingsubsystem: List[CouplingParametersConsensusALC] = self.get_CouplingParameters()
        
        for i in range(len(couplingsubsystem)):
            
            # Compute consensus inconsistencies
            
            # Auxiliary minus mapped response
            if (couplingsubsystem[i].get_MappedResponses() is not None) and \
                    (couplingsubsystem[i].get_Copy_CouplingVariable() is not None):
                # Update inconsistency
                auxiliary_mappedresponse: List[float] = couplingsubsystem[i].get_Auxiliary_MappedResponse()
                mappedresponse: List[float] = couplingsubsystem[i].get_MappedResponses()
                self._inconsistencies[i].evaluate_Auxiliary_Minus_MappedResponse(auxiliary=auxiliary_mappedresponse, mappedresponse=mappedresponse)
                
            # Auxiliary minus coupling variable
            if (couplingsubsystem[i].get_CouplingVariable() is not None) and \
                    (couplingsubsystem[i].get_Copy_MappedResponses() is not None):
                # Update inconsistency
                auxiliary_couplingvariable: List[float] = couplingsubsystem[i].get_Auxiliary_CouplingVariable()
                couplingvariable: List[float] = couplingsubsystem[i].get_CouplingVariable()
                self._inconsistencies[i].evaluate_Auxiliary_Minus_CouplingVariable(auxiliary=auxiliary_couplingvariable, couplingvariable=couplingvariable)
                
            # Shared auxiliary side
            if (couplingsubsystem[i].get_SharedDesignVariables() is not None) and \
                    (couplingsubsystem[i].get_Copy_TargetSharedDesignVariables() is not None):
                # Update inconsistency
                sharedauxiliary: List[float] = couplingsubsystem[i].get_Auxiliary_SharedDesignVariable()
                shareddesignvariable: List[float] = couplingsubsystem[i].get_SharedDesignVariables()
                self._inconsistencies[i].evaluate_Auxiliary_Minus_SharedDesignVariable(auxiliary=sharedauxiliary, shareddesignvariable=shareddesignvariable)
                
            # Shared auxiliary side
            if (couplingsubsystem[i].get_TargetSharedDesignVariables() is not None) and \
                    (couplingsubsystem[i].get_Copy_SharedDesignVariables() is not None):
                # Update inconsistency
                targetsharedauxiliary: List[float] = couplingsubsystem[i].get_Auxiliary_TargetSharedDesignVariable()
                targetshareddesignvariable: List[float] = couplingsubsystem[i].get_TargetSharedDesignVariables()
                self._inconsistencies[i].evaluate_Auxiliary_Minus_TargetSharedDesignVariable(auxiliary=targetsharedauxiliary, targetshareddesignvariable=targetshareddesignvariable)
        
    def return_initialized_Inconsistencies(self) -> List[InConsistencySize]:
        """Return initialized inconsistencies.

        Returns:
            List of initialized InConsistencySize, one per coupling parameter.
        """
        initialized_inconsistencies: List[InConsistencySize] = [InConsistencySize(self.get_CouplingParameters()[i].get_ID())
                                                                for i in range(len(self.get_CouplingParameters()))]
        return initialized_inconsistencies
    
    def set_AuxiliaryVariables_MappedResponse(self, neighborid: str, auxiliaryin: List[float]) -> None:
        """Set the auxiliary-minus-mapped-response auxiliary variables for a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            auxiliaryin: Auxiliary variable values to set.
        """
        # set auxiliary variables
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                # No copy.copy() needed here - set_Auxiliary_MappedResponse() already creates a defensive copy
                couplingparameter.set_Auxiliary_MappedResponse(auxiliaryin)
                break

    def set_AuxiliaryVariables_CouplingVariable(self, neighborid: str, auxiliaryin: List[float]) -> None:
        """Set the auxiliary-minus-coupling-variable auxiliary variables for a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            auxiliaryin: Auxiliary variable values to set.
        """
        # set auxiliary variables
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                # No copy.copy() needed here - set_Auxiliary_CouplingVariable() already creates a defensive copy
                couplingparameter.set_Auxiliary_CouplingVariable(auxiliaryin)
                break
                
    def set_AuxiliaryVariables_SharedDesignVariable(self, neighborid: str, auxiliaryin: List[float]) -> None:
        """Set the auxiliary-minus-shared-design-variable auxiliary variables for a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            auxiliaryin: Auxiliary variable values to set.
        """
        # set auxiliary variables
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                # No copy.copy() needed here - set_Auxiliary_SharedDesignVariable() already creates a defensive copy
                couplingparameter.set_Auxiliary_SharedDesignVariable(auxiliaryin)
                break

    def set_AuxiliaryVariables_TargetSharedDesignVariable(self, neighborid: str, auxiliaryin: List[float]) -> None:
        """Set the auxiliary-minus-target-shared-design-variable auxiliary variables for a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            auxiliaryin: Auxiliary variable values to set.
        """
        # set auxiliary variables
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                # No copy.copy() needed here - set_Auxiliary_TargetSharedDesignVariable() already creates a defensive copy
                couplingparameter.set_Auxiliary_TargetSharedDesignVariable(auxiliaryin)
                break
                
    def set_CoordinationMultipliers_Auxiliary_Minus_MappedResponse(self, neighborid: str, multipliersin: List[float]) -> None:
        """Set the coordination multipliers for the auxiliary minus mapped response inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            multipliersin: Auxiliary minus mapped response multiplier values to set.
        """
        # set coordination multipliers
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                # No copy.copy() needed here - set_Multipliers_Auxiliary_Minus_MappedResponse() already creates a defensive copy
                couplingparameter.set_Multipliers_Auxiliary_Minus_MappedResponse(multipliersin)
                break

    def set_CoordinationMultipliers_Auxiliary_Minus_CouplingVariable(self, neighborid: str, multipliersin: List[float]) -> None:
        """Set the coordination multipliers for the auxiliary minus coupling variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            multipliersin: Auxiliary minus coupling variable multiplier values to set.
        """
        # set coordination multipliers
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                # No copy.copy() needed here - set_Multipliers_Auxiliary_Minus_CouplingVariable() already creates a defensive copy
                couplingparameter.set_Multipliers_Auxiliary_Minus_CouplingVariable(multipliersin)
                break
                
    def set_CoordinationMultipliers_Auxiliary_Minus_SharedDesignVariable(self, neighborid: str, multipliersin: List[float]) -> None:
        """Set the coordination multipliers for the auxiliary minus shared design variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            multipliersin: Auxiliary minus shared design variable multiplier values to set.
        """
        # set coordination multipliers
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                # No copy.copy() needed here - set_Multipliers_Auxiliary_Minus_SharedDesignVariable() already creates a defensive copy
                couplingparameter.set_Multipliers_Auxiliary_Minus_SharedDesignVariable(multipliersin)
                break

    def set_CoordinationMultipliers_Auxiliary_Minus_TargetSharedDesignVariable(self, neighborid: str, multipliersin: List[float]) -> None:
        """Set the coordination multipliers for the auxiliary minus target shared design variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            multipliersin: Auxiliary minus target shared design variable multiplier values to set.
        """
        # set coordination multipliers
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                # No copy.copy() needed here - set_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable() already creates a defensive copy
                couplingparameter.set_Multipliers_Auxiliary_Minus_TargetSharedDesignVariable(multipliersin)
                break
                
    def set_CoordinationWeights_Auxiliary_Minus_MappedResponse(self, neighborid: str, penaltyweightsin: List[float]) -> None:
        """Set the coordination weights for the auxiliary minus mapped response inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            penaltyweightsin: Auxiliary minus mapped response penalty weight values to set.
        """
        # set coordination weights
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                # No copy.copy() needed here - set_Weights_Auxiliary_Minus_MappedResponse() already creates a defensive copy
                couplingparameter.set_Weights_Auxiliary_Minus_MappedResponse(penaltyweightsin)
                break

    def set_CoordinationWeights_Auxiliary_Minus_CouplingVariable(self, neighborid: str, penaltyweightsin: List[float]) -> None:
        """Set the coordination weights for the auxiliary minus coupling variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            penaltyweightsin: Auxiliary minus coupling variable penalty weight values to set.
        """
        # set coordination weights
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                # No copy.copy() needed here - set_Weights_Auxiliary_Minus_CouplingVariable() already creates a defensive copy
                couplingparameter.set_Weights_Auxiliary_Minus_CouplingVariable(penaltyweightsin)
                break
                
    def set_CoordinationWeights_Auxiliary_Minus_SharedDesignVariable(self, neighborid: str, penaltyweightsin: List[float]) -> None:
        """Set the coordination weights for the auxiliary minus shared design variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            penaltyweightsin: Auxiliary minus shared design variable penalty weight values to set.
        """
        # set coordination weights
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                # No copy.copy() needed here - set_Weights_Auxiliary_Minus_SharedDesignVariable() already creates a defensive copy
                couplingparameter.set_Weights_Auxiliary_Minus_SharedDesignVariable(penaltyweightsin)
                break

    def set_CoordinationWeights_Auxiliary_Minus_TargetSharedDesignVariable(self, neighborid: str, penaltyweightsin: List[float]) -> None:
        """Set the coordination weights for the auxiliary minus target shared design variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            penaltyweightsin: Auxiliary minus target shared design variable penalty weight values to set.
        """
        # set coordination weights
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                # No copy.copy() needed here - set_Weights_Auxiliary_Minus_TargetSharedDesignVariable() already creates a defensive copy
                couplingparameter.set_Weights_Auxiliary_Minus_TargetSharedDesignVariable(penaltyweightsin)
                break
    
########################################################################################################
#   Update State Function necessary for running multiprocessing
########################################################################################################
    def update_state(self, other_subsystem: 'LocalSubSystemConsensusALC') -> None:
        """Update the state of this LocalSubSystemConsensusALC instance with values from another instance.

        This method is necessary for multiprocessing. When subsystems are executed in parallel
        using multiprocessing.Pool, they are serialized and deserialized, creating new objects
        in separate memory spaces. After parallel execution completes, this method updates
        the original object's attribute values while preserving their memory addresses.

        The update preserves memory addresses by modifying attribute contents in-place where
        possible, rather than reassigning references. This is essential for maintaining object
        identity across the multiprocessing boundary.

        Args:
            other_subsystem: The source LocalSubSystemConsensusALC containing updated values
                from parallel execution.
        """
        # Update attributes inherited from LocalSubSystemBasis (and transitively SubSystemBasis)
        # This includes: _local_convergenceindicator_innerloop, _local_convergenceindicator_outerloop, _updatecouplingparametermethod_outerloop
        super().update_state(other_subsystem)

```
