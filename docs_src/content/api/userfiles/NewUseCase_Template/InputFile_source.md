---
title: InputFile (Source)
---

← Back to [InputFile documentation](InputFile.md)

# InputFile - Source Code

**File:** `userfiles\NewUseCase_Template\InputFile.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Input file configuration template for new use-cases.

This module defines the InputFile class which serves as a
template for configuring all parameters for a distributed optimization problem.
It demonstrates how to set up subsystem definitions, coordination methods,
iteration schemes, coupling parameters, and scaling variables.
"""
from typing import List
import copy
from Distributed_Design_Optimizer.coordination import InputFileBasis
from Distributed_Design_Optimizer.subsystem.tools import ScalerZeroOne, ScalerConstraint
from Distributed_Design_Optimizer.subsystem import LocalSubSystemBasis
from Distributed_Design_Optimizer.subsystem.optimization import AnalysisInterface, OptimizationInterface
from Distributed_Design_Optimizer.subsystem.optimization.designproblem import LocalObjectiveInterface, LocalConstraintsInterface

from Distributed_Design_Optimizer.coordination.coordinationmethod import (CoordinationMethodInterface,
                                                                        PC,
                                                                        LC,
                                                                        ALC,
                                                                        ALADIN,
                                                                        Consensus_ALC,
                                                                        SBDP
                                                                        )
from Distributed_Design_Optimizer.coordination.innerloop_iterationscheme import (IterationSchemeInterface,
                                                                                 Parallel,
                                                                                 SequentialForward,
                                                                                 SequentialBackward,
                                                                                 ParallelEvenThenOddLevels,
                                                                                 ParallelPerLevelIncreasing,
                                                                                 ParallelLocal_SequentialController
                                                                                 )
from Distributed_Design_Optimizer.coordination.updatecouplingparametermethod import (UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights,
                                                                                     UpdateCouplingParameterMethod_AugLagProximal_MultipliersFixedWeights,
                                                                                     UpdateCouplingParameterMethod_AdaptiveWeights,
                                                                                     UpdateCouplingParameterMethod_SubgradientMultipliers,
                                                                                     UpdateCouplingParameterMethod_AugLagMultipliersFixedWeights,
                                                                                     UpdateCouplingParameterMethod_OnlyInitialMultipliers
                                                                                     )
from Distributed_Design_Optimizer.coordination.convergence import (ConvergenceIndicator_Innerloop_DeWit,
                                                                   ConvergenceIndicator_Outerloop_DeWit,
                                                                   ConvergenceIndicator_Innerloop_AlwaysConverged
                                                                   )

from userfiles.NewUseCase_Template.subsystem0 import LocalConstraints0, LocalObjective0, Analysis0, Optimization0
from userfiles.NewUseCase_Template.subsystem1 import LocalConstraints1, LocalObjective1, Analysis1, Optimization1
from userfiles.NewUseCase_Template.subsystem2 import LocalConstraints2, LocalObjective2, Analysis2, Optimization2


class InputFile(InputFileBasis):
    """Template input file for distributed optimization.

    Configures a three-subsystem distributed optimization problem by defining
    the coordination method, subsystem hierarchy, design variable bounds,
    scaling variables, initial design variables, and coupling parameters.

    Attributes:
        _name: Identifier string for this use-case.
        _coordinationmethod: The coordination algorithm (e.g. ALC, PC, LC).
        _subsystems: List of LocalSubSystemBasis instances created by the
            coordination method.
    """

    def __init__(self) -> None:
        """Initialize the distributed optimization problem configuration.

        Sets up the full problem definition including:
            1. Coordination method and its hyperparameters.
            2. Subsystem IDs, hierarchy levels, and neighbor relationships.
            3. Analysis, objective, constraint, and optimization instances
               for each subsystem.
            4. Design variable bounds and scaling.
            5. Initial design variable values.
            6. Coupling and shared design variable initialization between
               neighboring subsystems.
        """
        
        # ── Step 1: Use-case name and coordination method ────────────────
        super().__init__()
        self._name = "NewUseCase_Template_Name"
        
        # Initialize the coordination method of choice.
        # Uncomment one of the alternatives below to switch algorithm.
        #self._coordinationmethod: CoordinationMethodInterface = PC(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1E-5),
        #                                                            convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-4),
        #                                                            updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AdaptiveWeights(
        #                                                                beta=3.5,
        #                                                                gamma=0.25,
        #                                                                initialweight=0.01),
        #                                                            iterationscheme=ParallelPerLevelIncreasing())
        # self._coordinationmethod: CoordinationMethodInterface = LC(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1E-5),
        #                                                             convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-4),
        #                                                             updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_SubgradientMultipliers(
        #                                                                 beta=3.5,
        #                                                                 initialmultiplier=0.0),
        #                                                             iterationscheme=ParallelPerLevelIncreasing())
        self._coordinationmethod: CoordinationMethodInterface = ALC(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1E-5),
                                                                    convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-4),
                                                                    updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights(
                                                                        beta=3.5,
                                                                        gamma=0.25,
                                                                        initialweight=0.5,
                                                                        initialmultiplier=0.0),
                                                                    iterationscheme=ParallelPerLevelIncreasing())
        # self._coordinationmethod: CoordinationMethodInterface = Consensus_ALC(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1E-5),
        #                                                                       convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-4),
        #                                                                       updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights(
        #                                                                           beta=3.5,
        #                                                                           gamma=0.25,
        #                                                                           initialweight=0.5,
        #                                                                           initialmultiplier=0.0),
        #                                                                       iterationscheme=Parallel())
        # self._coordinationmethod: CoordinationMethodInterface = ALADIN(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1000.0),
        #                                                                convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-4),
        #                                                                updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AugLagProximal_MultipliersFixedWeights(
        #                                                                    initialweight=0.01,
        #                                                                    initialmultiplier=0.0,
        #                                                                    initial_nu = 1e2,
        #                                                                    initial_sigma_i = 1.0),
        #                                                                iterationscheme=ParallelLocal_SequentialController())
        # self._coordinationmethod: CoordinationMethodInterface = SBDP(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_AlwaysConverged(),
        #                                                              convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-4),
        #                                                              updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_OnlyInitialMultipliers(initialmultiplier=0.0),
        #                                                              iterationscheme=Parallel())

        # ── Step 2: Define subsystem topology ─────────────────────────────
        # Each subsystem needs a unique ID, a hierarchy level, and a list of
        # neighbor IDs it is coupled with.
        id_list: List[str] = ["0",
                              "1",
                              "2"]
        
        level_list: List[int] = [0,   # subsystem 0 is at the top level
                                 1,   # subsystem 1 is one level below
                                 1]   # subsystem 2 is one level below
        
        neighborid_list: List[List[str]] = [["1", "2"],  # subsystem 0 is coupled to 1 and 2
                                            ["0", "2"],  # subsystem 1 is coupled to 0 and 2
                                            ["0", "1"]]  # subsystem 2 is coupled to 0 and 1
        
        # ── Step 3: Instantiate subsystem-specific components ──────────
        # One instance per subsystem for: analysis model, local objective,
        # local constraints, and optimization solver.
        analysis_list: List[AnalysisInterface] = [Analysis0(),
                                                  Analysis1(),
                                                  Analysis2()]
        
        localobjective_list: List[LocalObjectiveInterface] = [LocalObjective0(),
                                                              LocalObjective1(),
                                                              LocalObjective2()]
        
        localconstraints_list: List[LocalConstraintsInterface] = [LocalConstraints0(),
                                                                  LocalConstraints1(),
                                                                  LocalConstraints2()]
        
        optimization_list: List[OptimizationInterface] = [Optimization0(),
                                                          Optimization1(),
                                                          Optimization2()]
        
        # Create subsystems: the coordination method assembles LocalSubSystemBasis
        # instances from the topology and component lists defined above.
        self._subsystems: List[LocalSubSystemBasis] = self._coordinationmethod.createSubSystems(id_list=id_list,
                                                                                                level_list=level_list,
                                                                                                neighborid_list=neighborid_list,
                                                                                                analysis_list=analysis_list,
                                                                                                localobjective_list=localobjective_list,
                                                                                                localconstraints_list=localconstraints_list,
                                                                                                optimization_list=optimization_list)

        # ── Step 4: Design variable bounds ────────────────────────────
        # Set the unscaled (physical) lower and upper bounds for each
        # subsystem's design variables. The list length must match the
        # number of design variables in that subsystem.
        # Order: local design variables bounds,
        #        shared design variables bounds,
        #        additional design variables bounds (as a result of decomposition)
        self._subsystems[0].set_LowerBounds_Unscaled([... , ...])
        self._subsystems[1].set_LowerBounds_Unscaled([... , ...])
        self._subsystems[2].set_LowerBounds_Unscaled([... , ...])

        self._subsystems[0].set_UpperBounds_Unscaled([... , ...])
        self._subsystems[1].set_UpperBounds_Unscaled([... , ...])
        self._subsystems[2].set_UpperBounds_Unscaled([... , ...])
        
        # ── Step 5: Scaling variables ──────────────────────────────────
        # Define one scaler per variable. ScalerZeroOne maps to [0, 1],
        # ScalerConstraint normalizes constraint values.
        # Order: local design variables,
        #        shared design variables,
        #        additional design variables (as a result of decomposition),
        #        local objective, local equality constraints,
        #        local inequality constraints,
        #        mapped responses, copy of mapped responses (only if not already included earlier for additional desing variables).
        self._subsystems[0].set_Scalers([
            ScalerZeroOne(self._subsystems[0].get_LowerBounds_Unscaled()[0], self._subsystems[0].get_UpperBounds_Unscaled()[0]),
            ScalerZeroOne(self._subsystems[0].get_LowerBounds_Unscaled()[1], self._subsystems[0].get_UpperBounds_Unscaled()[1]),
            ScalerZeroOne(self._subsystems[0].get_LowerBounds_Unscaled()[2], self._subsystems[0].get_UpperBounds_Unscaled()[2]),
            ScalerZeroOne(..., ...),
            ScalerZeroOne(..., ...),
            ScalerZeroOne(..., ...),
            ScalerConstraint(..., ...),
            ScalerConstraint(..., ...),
            ScalerConstraint(..., ...),
        ])

        self._subsystems[1].set_Scalers([
            ScalerZeroOne(self._subsystems[1].get_LowerBounds_Unscaled()[0], self._subsystems[1].get_UpperBounds_Unscaled()[0]),
            ScalerZeroOne(self._subsystems[1].get_LowerBounds_Unscaled()[1], self._subsystems[1].get_UpperBounds_Unscaled()[1]),
            ScalerZeroOne(self._subsystems[1].get_LowerBounds_Unscaled()[2], self._subsystems[1].get_UpperBounds_Unscaled()[2]),
            ScalerZeroOne(self._subsystems[1].get_LowerBounds_Unscaled()[3], self._subsystems[1].get_UpperBounds_Unscaled()[3]),
            ScalerZeroOne(..., ...),
            ScalerConstraint(..., ...),
            ScalerConstraint(..., ...),
            ScalerConstraint(..., ...),
            copy.deepcopy(self._subsystems[0].get_Scalers()[...])  # reuse scaling variable from neighbor
        ])
        
        self._subsystems[2].set_Scalers([
            ScalerZeroOne(self._subsystems[2].get_LowerBounds_Unscaled()[0], self._subsystems[2].get_UpperBounds_Unscaled()[0]),
            ScalerZeroOne(self._subsystems[2].get_LowerBounds_Unscaled()[1], self._subsystems[2].get_UpperBounds_Unscaled()[1]),
            ScalerZeroOne(self._subsystems[2].get_LowerBounds_Unscaled()[2], self._subsystems[2].get_UpperBounds_Unscaled()[2]),
            copy.deepcopy(self._subsystems[1].get_Scalers()[...]),
            ScalerZeroOne(..., ...),
            ScalerConstraint(..., ...),
            ScalerConstraint(..., ...),
            ScalerConstraint(..., ...),
            copy.deepcopy(self._subsystems[0].get_Scalers()[...])  # reuse scaling variable from neighbor
        ])

        # ── Step 6: Design variable initialization & reference state ──────
        # Set granularity (step sizes), initial values, and (optionally)
        # reference values / coupling metadata for each subsystem's design
        # variables. Values are scaled via .transform().
        # Order: local design variables,
        #        shared design variables,
        #        additional design variables(as a result of decomposition)
        self._subsystems[0].set_DesignVariables_Granularity([... , ...])
        self._subsystems[0].set_DesignVariables([self._subsystems[0].get_Scalers()[0].transform(...),
                                                 self._subsystems[0].get_Scalers()[1].transform(...)
                                                 ])
        # self._subsystems[0].set_ReferenceDesignVariables([self._subsystems[1].get_Scalers()[0].transform(...),
        #                                                   self._subsystems[1].get_Scalers()[1].transform(...)
        #                                                   ])
        # self._subsystems[0].set_ReferenceLocalObjectiveValue(self._subsystems[1].get_Scalers()[...].transform(...))
        # self._subsystems[0].set_ReferenceLocalObjectiveValueUnscaled(...)
        # self._subsystems[0].set_DesignVariablesInfluenceAnyCouplingBool([False, False, False, True, True])
        # self._subsystems[0].set_NeighborID_for_additional_dv([None, None, None, ["1"], ["2"]])
        
        self._subsystems[1].set_DesignVariables_Granularity([... , ...])
        self._subsystems[1].set_DesignVariables([self._subsystems[1].get_Scalers()[0].transform(...),
                                                 self._subsystems[1].get_Scalers()[1].transform(...)
                                                 ])
        # self._subsystems[1].set_ReferenceDesignVariables([self._subsystems[1].get_Scalers()[0].transform(...),
        #                                                   self._subsystems[1].get_Scalers()[1].transform(...)
        #                                                  ])
        # self._subsystems[1].set_ReferenceLocalObjectiveValue(self._subsystems[1].get_Scalers()[...].transform(...))
        # self._subsystems[1].set_ReferenceLocalObjectiveValueUnscaled(...)
        # self._subsystems[1].set_DesignVariablesInfluenceAnyCouplingBool([True, True, True, True])
        # self._subsystems[1].set_NeighborID_for_additional_dv([None, None, None, None])
                
        self._subsystems[2].set_DesignVariables_Granularity([... , ...])
        self._subsystems[2].set_DesignVariables([self._subsystems[2].get_Scalers()[0].transform(...),
                                                 self._subsystems[2].get_Scalers()[1].transform(...)
                                                 ])
        # self._subsystems[2].set_ReferenceDesignVariables([self._subsystems[2].get_Scalers()[0].transform(...),
        #                                                   self._subsystems[2].get_Scalers()[1].transform(...)
        #                                                   ])
        # self._subsystems[2].set_ReferenceLocalObjectiveValue(self._subsystems[2].get_Scalers()[...].transform(...))
        # self._subsystems[2].set_ReferenceLocalObjectiveValueUnscaled(...)
        # self._subsystems[2].set_DesignVariablesInfluenceAnyCouplingBool([True, True, True, True])
        # self._subsystems[2].set_NeighborID_for_additional_dv([None, None, None, None])
        
        # ── Step 7: Coupling parameter initialization ─────────────────
        # For each pair of coupled subsystems, define the coupling and
        # shared design variables. Each "circle i - j" block sets the
        # variables that subsystem i owns w.r.t. neighbor j, and the
        # corresponding copies it holds of neighbor j's variables.
        #
        # Coupling variables:        ^{i}_{j}h
        # Mapped response variables: ^{i}_{j}H
        # Shared design variables:   ^{i}_{j}z
        # Target design variables:   ^{i}_{j}z_{t}

        # ── circle 0 - 1 ──
        self._subsystems[0].set_CouplingVariables("1", 
                                                  [self._subsystems[0].get_Scalers()[...].transform(...),
                                                   self._subsystems[0].get_Scalers()[...].transform(...)
                                                   ],
                                                  [... , ...])
        self._subsystems[0].set_Indices_CouplingVariables_in_DesignVariables("1", [..., ...])
        
        self._subsystems[0].set_Copy_MappedResponseVariables("1",
                                                            [self._subsystems[1].get_Scalers()[...].transform(...),
                                                             self._subsystems[1].get_Scalers()[...].transform(...)
                                                             ])
        
        # ── circle 1 - 0 (reciprocal of circle 0 - 1) ──
        self._subsystems[1].set_MappedResponseVariables("0",
                                                        [self._subsystems[1].get_Scalers()[...].transform(...),
                                                         self._subsystems[1].get_Scalers()[...].transform(...)
                                                         ],
                                                        [... , ...])
        
        self._subsystems[1].set_Copy_CouplingVariables("0",
                                                      [self._subsystems[0].get_Scalers()[...].transform(...),
                                                       self._subsystems[0].get_Scalers()[...].transform(...)
                                                       ])
        
        # ── circle 0 - 2 ──
        self._subsystems[0].set_CouplingVariables("2",
                                                  [self._subsystems[0].get_Scalers()[...].transform(...),
                                                   self._subsystems[0].get_Scalers()[...].transform(...)
                                                   ],
                                                  [... , ...])
        self._subsystems[0].set_Indices_CouplingVariables_in_DesignVariables("2", [... , ...])

        self._subsystems[0].set_Copy_MappedResponseVariables("2",
                                                            [self._subsystems[2].get_Scalers()[...].transform(...),
                                                             self._subsystems[2].get_Scalers()[...].transform(...)
                                                             ])
        
        # ── circle 2 - 0 (reciprocal of circle 0 - 2) ──
        self._subsystems[2].set_MappedResponseVariables("0",
                                                        [self._subsystems[2].get_Scalers()[...].transform(...),
                                                         self._subsystems[2].get_Scalers()[...].transform(...)
                                                         ],
                                                        [... , ...])
        
        self._subsystems[2].set_Copy_CouplingVariables("0",
                                                      [self._subsystems[0].get_Scalers()[...].transform(...),
                                                       self._subsystems[0].get_Scalers()[...].transform(...)
                                                       ])

        # ── circle 1 - 2 ──
        self._subsystems[1].set_SharedDesignVariables("2",
                                                      [self._subsystems[1].get_Scalers()[...].transform(...),
                                                       self._subsystems[1].get_Scalers()[...].transform(...)
                                                       ],
                                                      [... , ...])
        self._subsystems[1].set_Indices_SharedDesignVariables_in_DesignVariables("2", [... , ...])

        self._subsystems[1].set_Copy_TargetSharedDesignVariables("2",
                                                          [self._subsystems[2].get_Scalers()[...].transform(...),
                                                           self._subsystems[2].get_Scalers()[...].transform(...)
                                                           ])

        # ── circle 2 - 1 (reciprocal of circle 1 - 2) ──
        self._subsystems[2].set_TargetSharedDesignVariables("1",
                                                      [self._subsystems[2].get_Scalers()[...].transform(...),
                                                       self._subsystems[2].get_Scalers()[...].transform(...)
                                                       ],
                                                      [... , ...])
        self._subsystems[2].set_Indices_TargetSharedDesignVariables_in_DesignVariables("1", [... , ...])

        self._subsystems[2].set_Copy_SharedDesignVariables("1",
                                                          [self._subsystems[1].get_Scalers()[...].transform(...),
                                                           self._subsystems[1].get_Scalers()[...].transform(...)
                                                           ])

```
