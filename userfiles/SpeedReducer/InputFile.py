# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Input file configuration for Speed Reducer problem with non-hierarchic decomposition.

This module defines the configuration for distributed optimization of the Speed
Reducer design problem using Augmented Lagrangian Coordination (ALC) with
non-hierarchic decomposition into three subsystems.
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
from userfiles.SpeedReducer.subsystem0 import LocalConstraints0, LocalObjective0, Analysis0, Optimization0
from userfiles.SpeedReducer.subsystem1 import LocalConstraints1, LocalObjective1, Analysis1, Optimization1
from userfiles.SpeedReducer.subsystem2 import LocalConstraints2, LocalObjective2, Analysis2, Optimization2


class InputFile(InputFileBasis):
    """Configuration class for Speed Reducer problem with non-hierarchic ALC coordination.

    Defines the problem structure, subsystem decomposition, and coordination
    parameters for the Speed Reducer gearbox design optimization problem.

    Attributes:
        _name: Problem identifier string.
        _coordinationmethod: Coordination algorithm (ALC variants).
        _subsystems: List of configured subsystem objects.
    """

    def __init__(self) -> None:
        """Initialize the Speed Reducer problem configuration.

        Sets up three subsystems representing the gear design, shaft 1,
        and shaft 2 disciplines with shared design variables.
        """
        
        # ── Step 1: Use-case name and coordination method ────────────────
        super().__init__()
        self._name = "SpeedReducer"
        
        # Initialize the coordination method of choice.
        # Uncomment one of the alternatives below to switch algorithm.
        # self._coordinationmethod: CoordinationMethodInterface = PC(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1E-4),
        #                                                            convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-5),
        #                                                            updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AdaptiveWeights(
        #                                                                beta=1.3,
        #                                                                gamma=0.5,
        #                                                                initialweight=0.01),
        #                                                            iterationscheme=SequentialForward())
        # self._coordinationmethod: CoordinationMethodInterface = LC(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1E-4),
        #                                                             convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-5),
        #                                                             updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_SubgradientMultipliers(
        #                                                                 beta=1.3,
        #                                                                 initialmultiplier=0.0),
        #                                                             iterationscheme=SequentialForward())
        self._coordinationmethod: CoordinationMethodInterface = ALC(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1E-4),
                                                                    convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-5),
                                                                    updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights(
                                                                        beta=1.3,
                                                                        gamma=0.5,
                                                                        initialweight=0.01,
                                                                        initialmultiplier=0.0),
                                                                    iterationscheme=SequentialForward())
        # self._coordinationmethod: CoordinationMethodInterface = Consensus_ALC(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1E-4),
        #                                                                       convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-5),
        #                                                                       updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights(
        #                                                                           beta=1.3,
        #                                                                           gamma=0.5,
        #                                                                           initialweight=0.01,
        #                                                                           initialmultiplier=0.0),
        #                                                                       iterationscheme=Parallel())
        # self._coordinationmethod: CoordinationMethodInterface = ALADIN(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1000.0),
        #                                                                convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-5),
        #                                                                updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AugLagProximal_MultipliersFixedWeights(
        #                                                                    initialweight=0.01,
        #                                                                    initialmultiplier=0.0,
        #                                                                    initial_nu = 1e2,
        #                                                                    initial_sigma_i = 1.0),
        #                                                                iterationscheme=ParallelLocal_SequentialController())
        # self._coordinationmethod: CoordinationMethodInterface = SBDP(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_AlwaysConverged(),
        #                                                              convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-5),
        #                                                              updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_OnlyInitialMultipliers(initialmultiplier=0.0),
        #                                                              iterationscheme=Parallel())
        
        # ── Step 2: Define subsystem topology ─────────────────────────────
        # Each subsystem needs a unique ID, a hierarchy level, and a list of
        # neighbor IDs it is coupled with.
        id_list: List[str] = ["0",  # Gear
                              "1",  # Shaft 1
                              "2"]  # Shaft 2
        
        level_list: List[int] = [0,
                                 1,
                                 1]
        
        neighborid_list: List[List[str]] = [["1", "2"],
                                            ["0", "2"],
                                            ["0", "1"]]
        
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
        self._subsystems[0].set_LowerBounds_Unscaled([2.6,   # x1 gear tooth width
                                                      0.7,   # x2 teeth module
                                                      17.0])  # x3 number of teeth of pinion
        self._subsystems[1].set_LowerBounds_Unscaled([7.3,    # x4 length shaft 1
                                                      2.9,    # x6 diameter shaft 1
                                                      2.6,   # x1 gear tooth width
                                                      0.7,   # x2 teeth module
                                                      17.0])  # x3 number of teeth of pinion
        self._subsystems[2].set_LowerBounds_Unscaled([7.3,    # x5 length shaft 2
                                                      5.0,    # x7 diameter shaft 2
                                                      2.6,   # x1 gear tooth width
                                                      0.7,   # x2 teeth module
                                                      17.0])  # x3 number of teeth of pinion
       
        self._subsystems[0].set_UpperBounds_Unscaled([3.6, 0.8, 28.0])  # x1 gear tooth width, x2 teeth module, x3 number of teeth of pinion
        self._subsystems[1].set_UpperBounds_Unscaled([8.3, 3.9, 3.6, 0.8, 28.0])  # x4 length shaft 1, x6 diameter shaft 1, x1 gear tooth width, x2 teeth module, x3 number of teeth of pinion
        self._subsystems[2].set_UpperBounds_Unscaled([8.3, 5.5, 3.6, 0.8, 28.0])  # x5 length shaft 2, x7 diameter shaft 2, x1 gear tooth width, x2 teeth module, x3 number of teeth of pinion
        
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
            ScalerZeroOne(self._subsystems[0].get_LowerBounds_Unscaled()[0], self._subsystems[0].get_UpperBounds_Unscaled()[0]),  # x1 gear tooth width
            ScalerZeroOne(self._subsystems[0].get_LowerBounds_Unscaled()[1], self._subsystems[0].get_UpperBounds_Unscaled()[1]),  # x2 teeth module
            ScalerZeroOne(self._subsystems[0].get_LowerBounds_Unscaled()[2], self._subsystems[0].get_UpperBounds_Unscaled()[2]),  # x3 number of teeth of pinion
            ScalerZeroOne(1200.0, 7000.0),  # local objective function
            ScalerConstraint(-0.01, 0.01),  # local equality function
            ScalerConstraint(-1.0, 1.0),  # local inequality function 0 gear tooth bending stress
            ScalerConstraint(-1.0, 1.0),  # local inequality function 1 gear tooth contact stress
            ScalerConstraint(-1.0, 1.0),  # local inequality function 2 shaft 1 deformation and stress
            ScalerConstraint(-1.0, 1.0),  # local inequality function 3 shaft 2 deformation and stress
            ScalerConstraint(-1.0, 1.0)   # local inequality function 4 geometric constraint
        ])
        
        self._subsystems[1].set_Scalers([
            ScalerZeroOne(self._subsystems[1].get_LowerBounds_Unscaled()[0], self._subsystems[1].get_UpperBounds_Unscaled()[0]),  # x4 length shaft 1
            ScalerZeroOne(self._subsystems[1].get_LowerBounds_Unscaled()[1], self._subsystems[1].get_UpperBounds_Unscaled()[1]),  # x6 diameter shaft 1
            copy.deepcopy(self._subsystems[0].get_Scalers()[0]),  # x1 gear tooth width
            copy.deepcopy(self._subsystems[0].get_Scalers()[1]),  # x2 teeth module
            copy.deepcopy(self._subsystems[0].get_Scalers()[2]),  # x3 number of teeth of pinion
            ScalerZeroOne(100.0, 600.0),  # local objective function
            ScalerConstraint(-0.01, 0.01),  # local equality function
            ScalerConstraint(-1.0, 1.0),  # local inequality function 0 shaft 1 deformation and stress
            ScalerConstraint(-1.0, 1.0),  # local inequality function 1 shaft 1 deformation and stress
            ScalerConstraint(-1.0, 1.0)   # local inequality function 2 geometric constraint
        ])
        
        self._subsystems[2].set_Scalers([
            ScalerZeroOne(self._subsystems[2].get_LowerBounds_Unscaled()[0], self._subsystems[2].get_UpperBounds_Unscaled()[0]),  # x5 length shaft 2
            ScalerZeroOne(self._subsystems[2].get_LowerBounds_Unscaled()[1], self._subsystems[2].get_UpperBounds_Unscaled()[1]),  # x7 diameter shaft 2
            copy.deepcopy(self._subsystems[0].get_Scalers()[0]),  # x1 gear tooth width
            copy.deepcopy(self._subsystems[0].get_Scalers()[1]),  # x2 teeth module
            copy.deepcopy(self._subsystems[0].get_Scalers()[2]),  # x3 number of teeth of pinion
            ScalerZeroOne(100.0, 1500.0),  # local objective function
            ScalerConstraint(-0.01, 0.01),  # local equality function
            ScalerConstraint(-1.0, 1.0),  # local inequality function 0 shaft 2 deformation and stress
            ScalerConstraint(-1.0, 1.0),  # local inequality function 1 shaft 2 deformation and stress
            ScalerConstraint(-1.0, 1.0)   # local inequality function 2 geometric constraint
        ])
       
        # ── Step 6: Design variable initialization & reference state ──────
        # Set granularity (step sizes), initial values, and (optionally)
        # reference values / coupling metadata for each subsystem's design
        # variables. Values are scaled via .transform().
        # Order: local design variables,
        #        shared design variables,
        #        additional design variables(as a result of decomposition)
        self._subsystems[0].set_DesignVariables_Granularity([0.0, 0.0, 0.0])  # x1 gear tooth width, x2 teeth module, x3 number of teeth of pinion
        self._subsystems[0].set_DesignVariables([self._subsystems[0].get_Scalers()[0].transform(3.1),  # x1 gear tooth width
                                                 self._subsystems[0].get_Scalers()[1].transform(0.75),  # x2 teeth module
                                                 self._subsystems[0].get_Scalers()[2].transform(22.5)   # x3 number of teeth of pinion
                                                 ])
        self._subsystems[0].set_ReferenceDesignVariables([self._subsystems[0].get_Scalers()[0].transform(3.5),  # x1 gear tooth width
                                                          self._subsystems[0].get_Scalers()[1].transform(0.7),  # x2 teeth module
                                                          self._subsystems[0].get_Scalers()[2].transform(17.0)   # x3 number of teeth of pinion
                                                          ])
        self._subsystems[0].set_ReferenceLocalObjectiveValue(self._subsystems[0].get_Scalers()[3].transform(2343.0))
        self._subsystems[0].set_ReferenceLocalObjectiveValueUnscaled(2343.0)
        # self._subsystems[0].set_DesignVariablesInfluenceAnyCouplingBool([False, False, False])
        # self._subsystems[0].set_NeighborID_for_additional_dv([None, None, None])
        self._subsystems[1].set_DesignVariables_Granularity([0.0, 0.0, 0.0, 0.0, 0.0])  # x4 length shaft 1, x6 diameter shaft 1, x1 gear tooth width, x2 teeth module, x3 number of teeth of pinion
        self._subsystems[1].set_DesignVariables([self._subsystems[1].get_Scalers()[0].transform(7.8),   # x4 length shaft 1
                                                 self._subsystems[1].get_Scalers()[1].transform(3.4),   # x6 diameter shaft 1
                                                 self._subsystems[1].get_Scalers()[2].transform(3.1),   # x1 gear tooth width
                                                 self._subsystems[1].get_Scalers()[3].transform(0.75),  # x2 teeth module
                                                 self._subsystems[1].get_Scalers()[4].transform(22.5)   # x3 number of teeth of pinion
                                                 ])
        self._subsystems[1].set_ReferenceDesignVariables([self._subsystems[1].get_Scalers()[0].transform(7.3),   # x4 length shaft 1
                                                          self._subsystems[1].get_Scalers()[1].transform(3.5),   # x6 diameter shaft 1
                                                          self._subsystems[1].get_Scalers()[2].transform(3.5),   # x1 gear tooth width
                                                          self._subsystems[1].get_Scalers()[3].transform(0.7),   # x2 teeth module
                                                          self._subsystems[1].get_Scalers()[4].transform(17.0)   # x3 number of teeth of pinion
                                                          ])
        self._subsystems[1].set_ReferenceLocalObjectiveValue(self._subsystems[1].get_Scalers()[5].transform(161.0))
        self._subsystems[1].set_ReferenceLocalObjectiveValueUnscaled(161.0)
        # self._subsystems[1].set_DesignVariablesInfluenceAnyCouplingBool([False, False, False, False, False])
        # self._subsystems[1].set_NeighborID_for_additional_dv([None, None, None, None, None])
        
        self._subsystems[2].set_DesignVariables_Granularity([0.0, 0.0, 0.0, 0.0, 0.0])  # x5 length shaft 2, x7 diameter shaft 2, x1 gear tooth width, x2 teeth module, x3 number of teeth of pinion
        self._subsystems[2].set_DesignVariables([self._subsystems[2].get_Scalers()[0].transform(7.8),   # x5 length shaft 2
                                                 self._subsystems[2].get_Scalers()[1].transform(5.25),  # x7 diameter shaft 2
                                                 self._subsystems[2].get_Scalers()[2].transform(3.1),   # x1 gear tooth width
                                                 self._subsystems[2].get_Scalers()[3].transform(0.75),  # x2 teeth module
                                                 self._subsystems[2].get_Scalers()[4].transform(22.5)   # x3 number of teeth of pinion
                                                 ])
        self._subsystems[2].set_ReferenceDesignVariables([self._subsystems[2].get_Scalers()[0].transform(8.1),   # x5 length shaft 2
                                                          self._subsystems[2].get_Scalers()[1].transform(5.3),   # x7 diameter shaft 2
                                                          self._subsystems[2].get_Scalers()[2].transform(3.5),   # x1 gear tooth width
                                                          self._subsystems[2].get_Scalers()[3].transform(0.7),   # x2 teeth module
                                                          self._subsystems[2].get_Scalers()[4].transform(17.0)   # x3 number of teeth of pinion
                                                          ])
        self._subsystems[2].set_ReferenceLocalObjectiveValue(self._subsystems[2].get_Scalers()[5].transform(213.5))
        self._subsystems[2].set_ReferenceLocalObjectiveValueUnscaled(213.5)
        # self._subsystems[2].set_DesignVariablesInfluenceAnyCouplingBool([False, False, False, False, False])
        # self._subsystems[2].set_NeighborID_for_additional_dv([None, None, None, None, None])
             
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
        #  x1 gear tooth width, x2 teeth module, x3 number of teeth of pinion
        self._subsystems[0].set_SharedDesignVariables("1", [self._subsystems[0].get_Scalers()[0].transform(3.1),
                                                            self._subsystems[0].get_Scalers()[1].transform(0.75),
                                                            self._subsystems[0].get_Scalers()[2].transform(22.5)
                                                            ], [3.1, 0.75, 22.5]
                                                      )
        self._subsystems[0].set_Indices_SharedDesignVariables_in_DesignVariables("1", [0, 1, 2])
        #  x1 gear tooth width, x2 teeth module, x3 number of teeth of pinion
        self._subsystems[0].set_Copy_TargetSharedDesignVariables("1", [self._subsystems[1].get_Scalers()[2].transform(3.1),
                                                                self._subsystems[1].get_Scalers()[3].transform(0.75),
                                                                self._subsystems[1].get_Scalers()[4].transform(22.5)
                                                                ]
                                                          )
       
        # ── circle 0 - 2 ──
        #  x1 gear tooth width, x2 teeth module, x3 number of teeth of pinion
        self._subsystems[0].set_SharedDesignVariables("2", [self._subsystems[0].get_Scalers()[0].transform(3.1),
                                                            self._subsystems[0].get_Scalers()[1].transform(0.75),
                                                            self._subsystems[0].get_Scalers()[2].transform(22.5)
                                                            ], [3.1, 0.75, 22.5]
                                                      )
        self._subsystems[0].set_Indices_SharedDesignVariables_in_DesignVariables("2", [0, 1, 2])
        #  x1 gear tooth width, x2 teeth module, x3 number of teeth of pinion
        self._subsystems[0].set_Copy_TargetSharedDesignVariables("2", [self._subsystems[2].get_Scalers()[2].transform(3.1),
                                                                self._subsystems[2].get_Scalers()[3].transform(0.75),
                                                                self._subsystems[2].get_Scalers()[4].transform(22.5)
                                                                ]
                                                          )
       
        # ── circle 1 - 0 (reciprocal of circle 0 - 1) ──
        #  x1 gear tooth width, x2 teeth module, x3 number of teeth of pinion
        self._subsystems[1].set_TargetSharedDesignVariables("0", [self._subsystems[1].get_Scalers()[2].transform(3.1),
                                                            self._subsystems[1].get_Scalers()[3].transform(0.75),
                                                            self._subsystems[1].get_Scalers()[4].transform(22.5)
                                                            ], [3.1, 0.75, 22.5]
                                                      )
        self._subsystems[1].set_Indices_TargetSharedDesignVariables_in_DesignVariables("0", [2, 3, 4])
        #  x1 gear tooth width, x2 teeth module, x3 number of teeth of pinion
        self._subsystems[1].set_Copy_SharedDesignVariables("0", [self._subsystems[0].get_Scalers()[0].transform(3.1),
                                                                self._subsystems[0].get_Scalers()[1].transform(0.75),
                                                                self._subsystems[0].get_Scalers()[2].transform(22.5)
                                                                ]
                                                          )
       
        # ── circle 1 - 2 ──
        #  x1 gear tooth width, x2 teeth module, x3 number of teeth of pinion
        self._subsystems[1].set_SharedDesignVariables("2", [self._subsystems[1].get_Scalers()[2].transform(3.1),
                                                            self._subsystems[1].get_Scalers()[3].transform(0.75),
                                                            self._subsystems[1].get_Scalers()[4].transform(22.5)
                                                            ], [3.1, 0.75, 22.5]
                                                      )
        self._subsystems[1].set_Indices_SharedDesignVariables_in_DesignVariables("2", [2, 3, 4])
        #  x1 gear tooth width, x2 teeth module, x3 number of teeth of pinion
        self._subsystems[1].set_Copy_TargetSharedDesignVariables("2", [self._subsystems[2].get_Scalers()[2].transform(3.1),
                                                                self._subsystems[2].get_Scalers()[3].transform(0.75),
                                                                self._subsystems[2].get_Scalers()[4].transform(22.5)
                                                                ]
                                                          )
        # ── circle 2 - 0 (reciprocal of circle 0 - 2) ──
        #  x1 gear tooth width, x2 teeth module, x3 number of teeth of pinion
        self._subsystems[2].set_TargetSharedDesignVariables("0", [self._subsystems[2].get_Scalers()[2].transform(3.1),
                                                            self._subsystems[2].get_Scalers()[3].transform(0.75),
                                                            self._subsystems[2].get_Scalers()[4].transform(22.5)
                                                            ], [3.1, 0.75, 22.5]
                                                      )
        self._subsystems[2].set_Indices_TargetSharedDesignVariables_in_DesignVariables("0", [2, 3, 4])
        #  x1 gear tooth width, x2 teeth module, x3 number of teeth of pinion
        self._subsystems[2].set_Copy_SharedDesignVariables("0", [self._subsystems[0].get_Scalers()[0].transform(3.1),
                                                                self._subsystems[0].get_Scalers()[1].transform(0.75),
                                                                self._subsystems[0].get_Scalers()[2].transform(22.5)
                                                                ]
                                                          )
       
        # ── circle 2 - 1 (reciprocal of circle 1 - 2) ──
        #  x1 gear tooth width, x2 teeth module, x3 number of teeth of pinion
        self._subsystems[2].set_TargetSharedDesignVariables("1", [self._subsystems[2].get_Scalers()[2].transform(3.1),
                                                            self._subsystems[2].get_Scalers()[3].transform(0.75),
                                                            self._subsystems[2].get_Scalers()[4].transform(22.5)
                                                            ], [3.1, 0.75, 22.5]
                                                      )
        self._subsystems[2].set_Indices_TargetSharedDesignVariables_in_DesignVariables("1", [2, 3, 4])
        #  x1 gear tooth width, x2 teeth module, x3 number of teeth of pinion
        self._subsystems[2].set_Copy_SharedDesignVariables("1", [self._subsystems[1].get_Scalers()[2].transform(3.1),
                                                                self._subsystems[1].get_Scalers()[3].transform(0.75),
                                                                self._subsystems[1].get_Scalers()[4].transform(22.5)
                                                                ]
                                                          )
