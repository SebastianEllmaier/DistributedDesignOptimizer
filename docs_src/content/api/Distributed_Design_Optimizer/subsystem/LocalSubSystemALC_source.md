---
title: LocalSubSystemALC (Source)
---

← Back to [LocalSubSystemALC documentation](LocalSubSystemALC.md)

# LocalSubSystemALC - Source Code

**File:** `Distributed_Design_Optimizer\subsystem\LocalSubSystemALC.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Augmented Lagrangian Coordination local subsystem module.

This module provides the local subsystem implementation for the
standard Augmented Lagrangian Coordination method.
"""

from typing import List, Type
import numpy as np
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.optimization import AnalysisInterface, OptimizationInterface
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalObjectiveInterface, LocalConstraintsInterface
from Distributed_Design_Optimizer.middlelevel.alc import InConsistencySize
from Distributed_Design_Optimizer.subsystem.couplingparameters.alc import CouplingParametersALC
from Distributed_Design_Optimizer.postprocess.terminal_print_tools import DDO_Color, Reset, ddo_print, ddo_print_border
from Distributed_Design_Optimizer.coordination.convergence import (Local_ConvergenceIndicator_Innerloop_Interface,
                                                                   Local_ConvergenceIndicator_Innerloop_DeWit,
                                                                   Local_ConvergenceIndicator_Outerloop_Interface,
                                                                   Local_ConvergenceIndicator_Outerloop_DeWit
                                                                   )
from Distributed_Design_Optimizer.coordination.updatecouplingparametermethod import (UpdateCouplingParameterMethodInterface,
                                                                                     UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights
                                                                                     )


class LocalSubSystemALC(LocalSubSystemBasis):
    """Local subsystem implementation using Augmented Lagrangian Coordination.

    Implements the Augmented Lagrangian Coordination (ALC) method for distributed
    optimization. Manages coupling parameters, coordination multipliers, weights,
    and convergence tracking for iterative decomposition-based optimization.
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
        """Create a new LocalSubSystemALC instance.

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
        # ALC coordination method. These are validated here (rather than in ALC)
        # because the corresponding objects are handed to this subsystem.

        # Allowed / recommended outerloop update coupling parameter methods for ALC
        self._allowedupdatemethods_outerloop: List[Type[UpdateCouplingParameterMethodInterface]] = [
            UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights
        ]
        self._recommendedupdatemethods_outerloop: List[Type[UpdateCouplingParameterMethodInterface]] = [
            UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights
        ]

        # Allowed / recommended local inner loop convergence indicators for ALC
        self._allowedconvergenceindicators_innerloop: List[Type[Local_ConvergenceIndicator_Innerloop_Interface]] = [
            Local_ConvergenceIndicator_Innerloop_DeWit
        ]
        self._recommendedconvergenceindicators_innerloop: List[Type[Local_ConvergenceIndicator_Innerloop_Interface]] = [
            Local_ConvergenceIndicator_Innerloop_DeWit
        ]

        # Allowed / recommended local outer loop convergence indicators for ALC
        self._allowedconvergenceindicators_outerloop: List[Type[Local_ConvergenceIndicator_Outerloop_Interface]] = [
            Local_ConvergenceIndicator_Outerloop_DeWit
        ]
        self._recommendedconvergenceindicators_outerloop: List[Type[Local_ConvergenceIndicator_Outerloop_Interface]] = [
            Local_ConvergenceIndicator_Outerloop_DeWit
        ]

        self._couplingparameters: List[CouplingParametersALC] = [CouplingParametersALC(neighbor_id) for neighbor_id in neighborid]
        
        # super() initialization is not called at the top,
        # since evaluateAllJacobians needs optimdata, and initialization of optimdata needs couplingparameters
        super().__init__(id, level, neighborid, analysis, localobjective, localconstraints, optimization)
        
        # Convergence indicators - passed from ALC
        self._local_convergenceindicator_innerloop: Local_ConvergenceIndicator_Innerloop_DeWit = local_convergenceindicator_innerloop
        self._local_convergenceindicator_outerloop: Local_ConvergenceIndicator_Outerloop_DeWit = local_convergenceindicator_outerloop
        
        self._inconsistencies: List[InConsistencySize] = [InConsistencySize(self.get_CouplingParameters()[i].get_ID())
                                                          for i in range(len(self.get_CouplingParameters()))]
        
        self._updatecouplingparametermethod_outerloop: UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights = updatecouplingparametermethod_outerloop

        # Validate the components handed to this subsystem
        self.validate_inputs()

    def validate_inputs(self) -> None:
        """Validate the components handed to this subsystem by the ALC coordination method.

        Validates that the outer-loop update coupling parameter method and the local
        inner/outer loop convergence indicators are compatible with ALC.

        Raises:
            ValueError: If a provided component is not compatible with ALC.
        """
        # ===== updatecouplingparametermethod_outerloop Validation =====
        if type(self._updatecouplingparametermethod_outerloop) not in self._allowedupdatemethods_outerloop:
            raise ValueError(
                f"{DDO_Color}Outerloop update method '{type(self._updatecouplingparametermethod_outerloop).__name__}' is not compatible with ALC. "
                f"Please choose one of the compatible methods: {[m.__name__ for m in self._allowedupdatemethods_outerloop]}{Reset}"
            )
        elif type(self._updatecouplingparametermethod_outerloop) not in self._recommendedupdatemethods_outerloop:
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: Outerloop update method '{type(self._updatecouplingparametermethod_outerloop).__name__}' is not recommended for ALC.")
            ddo_print(f"{type(self).__name__}: Recommended methods: {[m.__name__ for m in self._recommendedupdatemethods_outerloop]}")
            ddo_print_border()

        # ===== Convergence Indicator Inner Validation =====
        if type(self._local_convergenceindicator_innerloop) not in self._allowedconvergenceindicators_innerloop:
            raise ValueError(
                f"{DDO_Color}Inner loop convergence indicator '{type(self._local_convergenceindicator_innerloop).__name__}' is not compatible with ALC. "
                f"Please choose one of the compatible indicators: {[c.__name__ for c in self._allowedconvergenceindicators_innerloop]}{Reset}"
            )
        elif type(self._local_convergenceindicator_innerloop) not in self._recommendedconvergenceindicators_innerloop:
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: Inner loop convergence indicator '{type(self._local_convergenceindicator_innerloop).__name__}' is not recommended for ALC.")
            ddo_print(f"{type(self).__name__}: Recommended indicators: {[c.__name__ for c in self._recommendedconvergenceindicators_innerloop]}")
            ddo_print_border()

        # ===== Convergence Indicator Outer Validation =====
        if type(self._local_convergenceindicator_outerloop) not in self._allowedconvergenceindicators_outerloop:
            raise ValueError(
                f"{DDO_Color}Outer loop convergence indicator '{type(self._local_convergenceindicator_outerloop).__name__}' is not compatible with ALC. "
                f"Please choose one of the compatible indicators: {[c.__name__ for c in self._allowedconvergenceindicators_outerloop]}{Reset}"
            )
        elif type(self._local_convergenceindicator_outerloop) not in self._recommendedconvergenceindicators_outerloop:
            ddo_print_border()
            ddo_print(f"{type(self).__name__}: WARNING: Outer loop convergence indicator '{type(self._local_convergenceindicator_outerloop).__name__}' is not recommended for ALC.")
            ddo_print(f"{type(self).__name__}: Recommended indicators: {[c.__name__ for c in self._recommendedconvergenceindicators_outerloop]}")
            ddo_print_border()
    
################################################################################################################
#   Basics of the subsystem
################################################################################################################
    def append_Controller(self) -> None:
        """Update local subsystems by appending controller.
        """
        
        # ALC does not have a controller, hence, this function is empty
        pass 
    
##############################################################################################################
#   Functions to evaluate a subsystem's responses and map them onto coupling parameters
##############################################################################################################
    def mapToController(self) -> None:
        """Pass, since no controller in ALC.
        """
        
        pass
    
##############################################################################################################
#   Functions to evaluate a subsystem's optimization objective and constraints for given responses
############################################################################################################## 
    def evaluateCoordinationObjective(self) -> None:
        """Evaluate the coordination objective.
        """
        couplingin: List[CouplingParametersALC] = self.get_CouplingParameters()
        normcoupl = np.zeros(len(couplingin))
        inconsistency: List[InConsistencySize] = [InConsistencySize(couplingin[i].get_ID())
                                                  for i in range(len(couplingin))]
        
        for i in range(len(couplingin)):
            penalty_copymapres_minus_coupl = None
            penalty_mapres_minus_copycoupl = None
            penalty_shared_minus_copytgtshared = None
            penalty_copyshared_minus_tgtshared = None

            lagrangian_copymapres_minus_coupl = None
            lagrangian_mapres_minus_copycoupl = None
            lagrangian_shared_minus_copytgtshared = None
            lagrangian_copyshared_minus_tgtshared = None
            
            if ((couplingin[i].get_CouplingVariable() is not None) and
                    (couplingin[i].get_Copy_MappedResponses() is not None)):
                # Copied mapped response minus coupling variable inconsistency
                coupl: List[float] = couplingin[i].get_CouplingVariable()
                copymapres: List[float] = couplingin[i].get_Copy_MappedResponses()
                
                inconsistency[i].evaluate_CopyMappedResponse_Minus_CouplingVariable(couplingvariable=coupl, copymappedresponse=copymapres)
                
                penalty_copymapres_minus_coupl = np.array(couplingin[i].get_Weights_CopyMappedResponse_Minus_CouplingVariable()) * np.array(inconsistency[i].get_CopyMappedResponse_Minus_CouplingVariable())  # element-wise multiplication
                lagrangian_copymapres_minus_coupl = np.array(couplingin[i].get_Multipliers_CopyMappedResponse_Minus_CouplingVariable()) * np.array(inconsistency[i].get_CopyMappedResponse_Minus_CouplingVariable())  # element-wise multiplication
            else:
                penalty_copymapres_minus_coupl = np.array([0.0])
                lagrangian_copymapres_minus_coupl = np.array([0.0])

            if ((couplingin[i].get_Copy_CouplingVariable() is not None) and
                    (couplingin[i].get_MappedResponses() is not None)):
                # Mapped response minus copied coupling variable inconsistency
                copycoupl: List[float] = couplingin[i].get_Copy_CouplingVariable()
                mapres: List[float] = couplingin[i].get_MappedResponses()
                
                inconsistency[i].evaluate_MappedResponse_Minus_CopyCouplingVariable(copycouplingvariable=copycoupl, mappedresponse=mapres)
                
                penalty_mapres_minus_copycoupl = np.array(couplingin[i].get_Weights_MappedResponse_Minus_CopyCouplingVariable()) * np.array(inconsistency[i].get_MappedResponse_Minus_CopyCouplingVariable())  # element-wise multiplication
                lagrangian_mapres_minus_copycoupl = np.array(couplingin[i].get_Multipliers_MappedResponse_Minus_CopyCouplingVariable()) * np.array(inconsistency[i].get_MappedResponse_Minus_CopyCouplingVariable())  # element-wise multiplication
            else:
                penalty_mapres_minus_copycoupl = np.array([0.0])
                lagrangian_mapres_minus_copycoupl = np.array([0.0])

            if ((couplingin[i].get_Copy_TargetSharedDesignVariables() is not None) and
                    (couplingin[i].get_SharedDesignVariables() is not None)):
                # Shared design variable minus copied target shared design variable inconsistency
                copytgtshared: List[float] = couplingin[i].get_Copy_TargetSharedDesignVariables()
                shared: List[float] = couplingin[i].get_SharedDesignVariables()
                
                inconsistency[i].evaluate_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(copytargetshareddesignvariable=copytgtshared, shareddesignvariable=shared)
                                
                penalty_shared_minus_copytgtshared = np.array(couplingin[i].get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable()) * np.array(inconsistency[i].get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())  # element-wise multiplication
                lagrangian_shared_minus_copytgtshared = np.array(couplingin[i].get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable()) * np.array(inconsistency[i].get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable())  # element-wise multiplication
            else:
                penalty_shared_minus_copytgtshared = np.array([0.0])
                lagrangian_shared_minus_copytgtshared = np.array([0.0])

            if ((couplingin[i].get_Copy_SharedDesignVariables() is not None) and
                    (couplingin[i].get_TargetSharedDesignVariables() is not None)):
                # Copied shared design variable minus target shared design variable inconsistency
                copyshared: List[float] = couplingin[i].get_Copy_SharedDesignVariables()
                tgtshared: List[float] = couplingin[i].get_TargetSharedDesignVariables()
                
                inconsistency[i].evaluate_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(targetshareddesignvariable=tgtshared, copyshareddesignvariable=copyshared)

                penalty_copyshared_minus_tgtshared = np.array(couplingin[i].get_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable()) * np.array(inconsistency[i].get_CopySharedDesignVariable_Minus_TargetSharedDesignVariable())  # element-wise multiplication
                lagrangian_copyshared_minus_tgtshared = np.array(couplingin[i].get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable()) * np.array(inconsistency[i].get_CopySharedDesignVariable_Minus_TargetSharedDesignVariable())  # element-wise multiplication
            else:
                penalty_copyshared_minus_tgtshared = np.array([0.0])
                lagrangian_copyshared_minus_tgtshared = np.array([0.0])

            # Evaluate the objective inconsistency function
            normcoupl[i] = np.power(np.linalg.norm(np.concatenate((penalty_mapres_minus_copycoupl, penalty_copymapres_minus_coupl, penalty_shared_minus_copytgtshared, penalty_copyshared_minus_tgtshared))),2)
            normcoupl[i] = normcoupl[i] + np.sum(lagrangian_copymapres_minus_coupl) + np.sum(lagrangian_mapres_minus_copycoupl) + np.sum(lagrangian_shared_minus_copytgtshared) + np.sum(lagrangian_copyshared_minus_tgtshared)

        # Compute the sum of all the penalty function contributions
        phinorm = np.array(normcoupl)
        objective_inconsistency = float(np.sum(phinorm))
                
        # set the objective inconsistency value to subsystem object
        self.set_CoordinationObjectiveValue(objective_inconsistency)
        
    def evaluate_Gradient_CoordinationObjective(self) -> None:
        """Evaluate the analytical gradient of the coordination objective.

        Assumes the mapped responses Jacobian was evaluated already.
        """
        
        # TODO
        pass
        
        
    def evaluateCoordinationEqualityConstraint(self) -> None:
        """Evaluate the coordination equality constraint.
        """
        couplingin: List[CouplingParametersALC] = self.get_CouplingParameters()
        #########################################################################################################
        constraint_inconsistency = None
        #########################################################################################################
        self.set_CoordinationEqualityConstraintValue(constraint_inconsistency)

    def evaluateCoordinationInequalityConstraint(self) -> None:
        """Evaluate the coordination inequality constraint.
        """
        couplingin: List[CouplingParametersALC] = self.get_CouplingParameters()
        #########################################################################################################
        constraint_inconsistency = None
        #########################################################################################################
        self.set_CoordinationInequalityConstraintValue(constraint_inconsistency)

    def evaluate_Jacobian_CoordinationEqualityConstraints(self) -> None:
        """Evaluate the Jacobian of the coordination equality constraints.

        ALC does not have coordination equality constraints, hence no-op.
        """
        # No coordination equality constraints in ALC
        pass
    
    def evaluate_Jacobian_CoordinationInEqualityConstraints(self) -> None:
        """Evaluate the Jacobian of the coordination inequality constraints.

        ALC does not have coordination inequality constraints, hence no-op.
        """
        # No coordination inequality constraints in ALC
        pass
    
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
 
    def return_initialized_CouplingParameters(self) -> List[CouplingParametersALC]:
        """Return initialized coupling parameters.

        Returns:
            List of initialized CouplingParametersALC, one per neighbor.
        """
        
        initialized_couplingparameters: List[CouplingParametersALC] = [CouplingParametersALC(self.get_CouplingParameters()[i].get_ID())
                                                                     for i in range(len(self.get_CouplingParameters()))]
        return initialized_couplingparameters
    
########################################################################################################
#   Functions to handle coupling parameters
#######################################################################################################
    
    def initializeCouplingParameters_before_CopyToMiddleLevel(self) -> None:
        """Initialize coupling parameters before copying from neighboring subsystem.

        Create empty placeholders for coupling parameters, i.e. communicated quantities in the algorithms, 
        Lagrange multipliers, penalty weights, ...
        The sizes are read by already initialized quantities from the inner loop iteration.
        """
        
        pass
    
    def initializeCouplingParameters_after_CopyFromMiddleLevel(self) -> None:
        """Initialize coupling parameters after copying from neighboring subsystems.

        Create empty placeholders for coupling parameters, i.e. communicated quantities in the algorithms, 
        Lagrange multipliers, penalty weights, ...
        The sizes are read by already initialized quantities from the inner loop iteration.
        """
        coupling: List[CouplingParametersALC] = self.get_CouplingParameters()

        for i in range(len(coupling)):
            neighborid: str = coupling[i].get_ID()
            # initialize the coupling-variable coupling parameters
            if ((coupling[i].get_CouplingVariable() is not None) and
                    (coupling[i].get_Copy_MappedResponses() is not None)):
                initpenaltyr: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialWeight()] * len(coupling[i].get_CouplingVariable())
                initmultiplr: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialMultiplier()] * len(coupling[i].get_CouplingVariable())
                self.set_CoordinationWeights_CopyMappedResponse_Minus_CouplingVariable(neighborid, initpenaltyr)
                self.set_CoordinationMultipliers_CopyMappedResponse_Minus_CouplingVariable(neighborid, initmultiplr)
                
            if ((coupling[i].get_Copy_CouplingVariable() is not None) and
                    (coupling[i].get_MappedResponses() is not None)):
                # initialize the mapped-response coupling parameters
                initpenaltyl: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialWeight()] * len(coupling[i].get_MappedResponses())
                initmultipll: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialMultiplier()] * len(coupling[i].get_MappedResponses())
                self.set_CoordinationWeights_MappedResponse_Minus_CopyCouplingVariable(neighborid, initpenaltyl)
                self.set_CoordinationMultipliers_MappedResponse_Minus_CopyCouplingVariable(neighborid, initmultipll)
                
            if ((coupling[i].get_Copy_TargetSharedDesignVariables() is not None) and
                    (coupling[i].get_SharedDesignVariables() is not None)):
                # initialize the shared design variables coupling parameters
                initpenaltysd: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialWeight()] * len(coupling[i].get_SharedDesignVariables())
                initmultiplsd: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialMultiplier()] * len(coupling[i].get_SharedDesignVariables())
                self.set_CoordinationWeights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(neighborid, initpenaltysd)
                self.set_CoordinationMultipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(neighborid, initmultiplsd)
                
            if ((coupling[i].get_Copy_SharedDesignVariables() is not None) and
                    (coupling[i].get_TargetSharedDesignVariables() is not None)):
                # initialize the shared target variables coupling parameters
                initpenaltyst: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialWeight()] * len(coupling[i].get_TargetSharedDesignVariables())
                initmultiplst: List[float] = [self._updatecouplingparametermethod_outerloop.get_InitialMultiplier()] * len(coupling[i].get_TargetSharedDesignVariables())
                self.set_CoordinationWeights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(neighborid, initpenaltyst)
                self.set_CoordinationMultipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(neighborid, initmultiplst)
                
    def initializeCouplingParameters_after_Second_CopyFromMiddleLevel(self) -> None:
        """Initialize coupling parameters after two communication rounds between subsystems.
        """
        
        # ALC does not need such a second communication round, hence skip
        pass
    
    def prepare_updateCouplingParameters(self) -> None:
        """Prepare coupling parameters before update operations.
        """
        pass
        
    def updateCouplingParameters_innerLoop(self) -> None:
        """Update coupling parameters in the inner loop.
        """
        pass
    
    def updateCouplingParameters_outerLoop(self) -> None:
        """Update coupling parameters during outer loop iteration.
        """
        coupling: List[CouplingParametersALC] = self.get_CouplingParameters()
        
        inconsistencies_previous_outerloop_itr: List[InConsistencySize] = self.copy_Inconsistencies_Previous_outerloop_itr()
        
        # loop over all the coupling circles/neighbors
        for j in range(len(coupling)):
            # get the identifier of the neighboring subsystem
            neighborid: str = coupling[j].get_ID()
                
            # mapped-response part of the coupling circle
            if ((coupling[j].get_Multipliers_MappedResponse_Minus_CopyCouplingVariable() is not None) and (self._inconsistencies[j].get_MappedResponse_Minus_CopyCouplingVariable() is not None)):
                multipliersin: List[float] = coupling[j].get_Multipliers_MappedResponse_Minus_CopyCouplingVariable()
                penaltyweightsin: List[float] = coupling[j].get_Weights_MappedResponse_Minus_CopyCouplingVariable()
                inconsistency: List[float] = self._inconsistencies[j].get_MappedResponse_Minus_CopyCouplingVariable()
                inconsistency_previous_outerloop_itr: List[float] | None = inconsistencies_previous_outerloop_itr[j].get_MappedResponse_Minus_CopyCouplingVariable()
                        
                # update coordination multipliers
                self._updatecouplingparametermethod_outerloop.update_CoordinationMultipliers(multipliersin, penaltyweightsin, inconsistency)
                self.set_CoordinationMultipliers_MappedResponse_Minus_CopyCouplingVariable(neighborid, multipliersin)
                
                # update coordination weights    
                self._updatecouplingparametermethod_outerloop.update_CoordinationWeights(penaltyweightsin, inconsistency, inconsistency_previous_outerloop_itr)
                self.set_CoordinationWeights_MappedResponse_Minus_CopyCouplingVariable(neighborid, penaltyweightsin)

            # coupling-variable part of the coupling circle
            if ((coupling[j].get_Multipliers_CopyMappedResponse_Minus_CouplingVariable() is not None) and (self._inconsistencies[j].get_CopyMappedResponse_Minus_CouplingVariable() is not None)):
                multipliersin: List[float] = coupling[j].get_Multipliers_CopyMappedResponse_Minus_CouplingVariable()
                penaltyweightsin: List[float] = coupling[j].get_Weights_CopyMappedResponse_Minus_CouplingVariable()
                inconsistency: List[float] = self._inconsistencies[j].get_CopyMappedResponse_Minus_CouplingVariable()
                inconsistency_previous_outerloop_itr: List[float] | None = inconsistencies_previous_outerloop_itr[j].get_CopyMappedResponse_Minus_CouplingVariable()
                                    
                # update coordination multipliers
                self._updatecouplingparametermethod_outerloop.update_CoordinationMultipliers(multipliersin, penaltyweightsin, inconsistency)
                self.set_CoordinationMultipliers_CopyMappedResponse_Minus_CouplingVariable(neighborid, multipliersin)
                
                # update coordination weights    
                self._updatecouplingparametermethod_outerloop.update_CoordinationWeights(penaltyweightsin, inconsistency, inconsistency_previous_outerloop_itr)      
                self.set_CoordinationWeights_CopyMappedResponse_Minus_CouplingVariable(neighborid, penaltyweightsin)
            
            # shared-design-variable part of the coupling circle
            if ((coupling[j].get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable() is not None) and (self._inconsistencies[j].get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable() is not None)):
                multipliersin: List[float] = coupling[j].get_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable()
                penaltyweightsin: List[float] = coupling[j].get_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable()
                inconsistency: List[float] = self._inconsistencies[j].get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable()
                inconsistency_previous_outerloop_itr: List[float] | None = inconsistencies_previous_outerloop_itr[j].get_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable()
                                        
                # update coordination multipliers
                self._updatecouplingparametermethod_outerloop.update_CoordinationMultipliers(multipliersin, penaltyweightsin, inconsistency)
                self.set_CoordinationMultipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(neighborid, multipliersin)
                
                # update coordination weights    
                self._updatecouplingparametermethod_outerloop.update_CoordinationWeights(penaltyweightsin, inconsistency, inconsistency_previous_outerloop_itr)      
                self.set_CoordinationWeights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(neighborid, penaltyweightsin)
            
            # target part of the coupling circle
            if ((coupling[j].get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable() is not None) and (self._inconsistencies[j].get_CopySharedDesignVariable_Minus_TargetSharedDesignVariable() is not None)):
                multipliersin: List[float] = coupling[j].get_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable()
                penaltyweightsin: List[float] = coupling[j].get_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable()
                inconsistency: List[float] = self._inconsistencies[j].get_CopySharedDesignVariable_Minus_TargetSharedDesignVariable()
                inconsistency_previous_outerloop_itr: List[float] | None = inconsistencies_previous_outerloop_itr[j].get_CopySharedDesignVariable_Minus_TargetSharedDesignVariable()
                                        
                # update coordination multipliers
                self._updatecouplingparametermethod_outerloop.update_CoordinationMultipliers(multipliersin, penaltyweightsin, inconsistency)
                self.set_CoordinationMultipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(neighborid, multipliersin)
                
                # update coordination weights    
                self._updatecouplingparametermethod_outerloop.update_CoordinationWeights(penaltyweightsin, inconsistency, inconsistency_previous_outerloop_itr)      
                self.set_CoordinationWeights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(neighborid, penaltyweightsin)
                
    def evaluate_Inconsistencies(self) -> None:
        """Compute the difference between stored coupling and mapped variables.

        Compares to the latest available data from a subsystem.
        Delegates to the base class implementation which computes inconsistency vectors for the mapped-response side,
        coupling-variable side, shared design variables, and target shared design variables of each coupling circle.
        """
        super().evaluate_Inconsistencies()
        
    def return_initialized_Inconsistencies(self) -> List[InConsistencySize]:
        """Return initialized inconsistencies.

        Returns:
            List of initialized InConsistencySize, one per coupling parameter.
        """
        initialized_inconsistencies: List[InConsistencySize] = [InConsistencySize(self.get_CouplingParameters()[i].get_ID())
                                                                for i in range(len(self.get_CouplingParameters()))]
        return initialized_inconsistencies
    
    def set_CoordinationMultipliers_MappedResponse_Minus_CopyCouplingVariable(self, neighborid: str, multipliersin: List[float]) -> None:
        """Set coordination multipliers for the mapped response minus copied coupling variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            multipliersin: List of multiplier values to set.
        """
        # set coordination multipliers
        # No copy.copy() wrapper needed - setter creates its own defensive copy
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                couplingparameter.set_Multipliers_MappedResponse_Minus_CopyCouplingVariable(multipliersin)
                break

    def set_CoordinationMultipliers_CopyMappedResponse_Minus_CouplingVariable(self, neighborid: str, multipliersin: List[float]) -> None:
        """Set coordination multipliers for the copied mapped response minus coupling variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            multipliersin: List of multiplier values to set.
        """
        # set coordination multipliers
        # No copy.copy() wrapper needed - setter creates its own defensive copy
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                couplingparameter.set_Multipliers_CopyMappedResponse_Minus_CouplingVariable(multipliersin)
                break
                
    def set_CoordinationMultipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, neighborid: str, multipliersin: List[float]) -> None:
        """Set coordination multipliers for the shared design variable minus copied target shared design variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            multipliersin: List of multiplier values to set.
        """
        # set coordination multipliers
        # No copy.copy() wrapper needed - setter creates its own defensive copy
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                couplingparameter.set_Multipliers_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(multipliersin)
                break

    def set_CoordinationMultipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self, neighborid: str, multipliersin: List[float]) -> None:
        """Set coordination multipliers for the copied shared design variable minus target shared design variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            multipliersin: List of multiplier values to set.
        """
        # set coordination multipliers
        # No copy.copy() wrapper needed - setter creates its own defensive copy
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                couplingparameter.set_Multipliers_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(multipliersin)
                break
                
    def set_CoordinationWeights_MappedResponse_Minus_CopyCouplingVariable(self, neighborid: str, penaltyweightsin: List[float]) -> None:
        """Set coordination weights for the mapped response minus copied coupling variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            penaltyweightsin: List of penalty weight values to set.
        """
        # set coordination weights
        # No copy.copy() wrapper needed - setter creates its own defensive copy
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                couplingparameter.set_Weights_MappedResponse_Minus_CopyCouplingVariable(penaltyweightsin)
                break

    def set_CoordinationWeights_CopyMappedResponse_Minus_CouplingVariable(self, neighborid: str, penaltyweightsin: List[float]) -> None:
        """Set coordination weights for the copied mapped response minus coupling variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            penaltyweightsin: List of penalty weight values to set.
        """
        # set coordination weights
        # No copy.copy() wrapper needed - setter creates its own defensive copy
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                couplingparameter.set_Weights_CopyMappedResponse_Minus_CouplingVariable(penaltyweightsin)
                break
                
    def set_CoordinationWeights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(self, neighborid: str, penaltyweightsin: List[float]) -> None:
        """Set coordination weights for the shared design variable minus copied target shared design variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            penaltyweightsin: List of penalty weight values to set.
        """
        # set coordination weights
        # No copy.copy() wrapper needed - setter creates its own defensive copy
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                couplingparameter.set_Weights_SharedDesignVariable_Minus_CopyTargetSharedDesignVariable(penaltyweightsin)
                break

    def set_CoordinationWeights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(self, neighborid: str, penaltyweightsin: List[float]) -> None:
        """Set coordination weights for the copied shared design variable minus target shared design variable inconsistency of a neighbor.

        Args:
            neighborid: Identifier of the neighboring subsystem.
            penaltyweightsin: List of penalty weight values to set.
        """
        # set coordination weights
        # No copy.copy() wrapper needed - setter creates its own defensive copy
        for couplingparameter in self._couplingparameters:
            if couplingparameter.get_ID() == neighborid:
                couplingparameter.set_Weights_CopySharedDesignVariable_Minus_TargetSharedDesignVariable(penaltyweightsin)
                break
    
########################################################################################################
#   Update State Function necessary for running multiprocessing
########################################################################################################
    def update_state(self, other_subsystem: 'LocalSubSystemALC') -> None:
        """Update the state of this LocalSubSystemALC instance with values from another instance.

        This method is necessary for multiprocessing. When subsystems are executed in parallel
        using multiprocessing.Pool, they are serialized and deserialized, creating new objects
        in separate memory spaces. After parallel execution completes, this method updates
        the original object's attribute values while preserving their memory addresses.

        The update preserves memory addresses by modifying attribute contents in-place where
        possible, rather than reassigning references. This is essential for maintaining object
        identity across the multiprocessing boundary.

        Args:
            other_subsystem: The source LocalSubSystemALC containing
                updated values from parallel execution.
        """
        # Update attributes inherited from LocalSubSystemBasis (and transitively SubSystemBasis)
        # This includes: _local_convergenceindicator_innerloop, _local_convergenceindicator_outerloop, _updatecouplingparametermethod_outerloop
        super().update_state(other_subsystem)

```
