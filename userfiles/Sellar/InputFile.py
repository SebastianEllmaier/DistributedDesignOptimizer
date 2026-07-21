# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Input file configuration for Sellar problem with non-hierarchic decomposition.

This module defines the configuration for distributed optimization of the Sellar
multidisciplinary design problem using Augmented Lagrangian Coordination (ALC)
with non-hierarchic (flat) decomposition structure.
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
from userfiles.Sellar.subsystem0 import LocalConstraints0, LocalObjective0, Analysis0, Optimization0
from userfiles.Sellar.subsystem1 import LocalConstraints1, LocalObjective1, Analysis1, Optimization1


class InputFile(InputFileBasis):
    """Configuration class for Sellar problem with non-hierarchic ALC coordination.

    Defines the problem structure, subsystem decomposition, and coordination
    parameters for the Sellar multidisciplinary design optimization benchmark.

    Attributes:
        _name: Problem identifier string.
        _coordinationmethod: Coordination algorithm (ALC variants).
        _subsystems: List of configured subsystem objects.
    """

    def __init__(self) -> None:
        """Initialize the Sellar non-hierarchic problem configuration.

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
        self._name = "Sellar"
        
        # Initialize the coordination method of choice.
        # Uncomment one of the alternatives below to switch algorithm.
        # self._coordinationmethod: CoordinationMethodInterface = PC(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1E-4),
        #                                                            convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-5),
        #                                                            updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AdaptiveWeights(
        #                                                                beta=1.3,
        #                                                                gamma=0.25,
        #                                                                initialweight=0.01),
        #                                                            iterationscheme=SequentialForward())
        # self._coordinationmethod: CoordinationMethodInterface = LC(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1E-4),
        #                                                            convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-5),
        #                                                            updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_SubgradientMultipliers(
        #                                                                beta=1.3,
        #                                                                initialmultiplier=0.0),
        #                                                            iterationscheme=SequentialForward())
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
        #                                                                           gamma=0.25,
        #                                                                           initialweight=0.01,
        #                                                                           initialmultiplier=0.0),
        #                                                                       iterationscheme=Parallel())
        # self._coordinationmethod: CoordinationMethodInterface = ALCSigma(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1E-4),
        #                                                                  convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-5),
        #                                                                  updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AugLagSigma(
        #                                                                      beta=1.3,
        #                                                                      gamma=0.25,
        #                                                                      initialweight=0.01,
        #                                                                      initialmultiplier=0.0,
        #                                                                      sigma_active="1",
        #                                                                      initialsigma=1.0),
        #                                                                  iterationscheme=SequentialForward())
        # self._coordinationmethod: CoordinationMethodInterface = ALCTransformation(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1E-4),
        #                                                                           convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-5),
        #                                                                           updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights(
        #                                                                               beta=1.3,
        #                                                                               gamma=0.25,
        #                                                                               initialweight=0.01,
        #                                                                               initialmultiplier=0.0),
        #                                                                           iterationscheme=SequentialForward(),
        #                                                                           transformationfunction="pow",
        #                                                                           ppower=3)
        # self._coordinationmethod: CoordinationMethodInterface = ALCNeighborhoodSearch(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1E-4),
        #                                                                               convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-5),
        #                                                                               updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AugLagNeighborhoodSearch(
        #                                                                                   beta=1.3,
        #                                                                                   gamma=0.25,
        #                                                                                   initialweight=0.01,
        #                                                                                   initialmultiplier=0.0),
        #                                                                               iterationscheme=SequentialForward())
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
        id_list: List[str] = ["0",
                              "1"]
        
        level_list: List[int] = [0,
                                 1]
        
        neighborid_list: List[List[str]] = [["1"],
                                            ["0"]]
        
        # ── Step 3: Instantiate subsystem-specific components ──────────
        # One instance per subsystem for: analysis model, local objective,
        # local constraints, and optimization solver.
        analysis_list: List[AnalysisInterface] = [Analysis0(),
                                                  Analysis1()]
        
        localobjective_list: List[LocalObjectiveInterface] = [LocalObjective0(),
                                                              LocalObjective1()]
        
        localconstraints_list: List[LocalConstraintsInterface] = [LocalConstraints0(),
                                                                  LocalConstraints1()]
        
        optimization_list: List[OptimizationInterface] = [Optimization0(),
                                                          Optimization1()]
        
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
        self._subsystems[0].set_LowerBounds_Unscaled([0.0, -10.0, 0.0, 1.77763888346])  # x, z1, z2, y2
        self._subsystems[1].set_LowerBounds_Unscaled([-10.0, 0.0, 3.16])  # z1, z2, y1
        self._subsystems[0].set_UpperBounds_Unscaled([10.0, 10.0, 10.0, 24.0])  # x, z1, z2, y2
        self._subsystems[1].set_UpperBounds_Unscaled([10.0, 10.0, 115.2])  # z1, z2, y1
        
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
            ScalerZeroOne(self._subsystems[0].get_LowerBounds_Unscaled()[0], self._subsystems[0].get_UpperBounds_Unscaled()[0]),    # x
            ScalerZeroOne(self._subsystems[0].get_LowerBounds_Unscaled()[1], self._subsystems[0].get_UpperBounds_Unscaled()[1]),    # z1
            ScalerZeroOne(self._subsystems[0].get_LowerBounds_Unscaled()[2], self._subsystems[0].get_UpperBounds_Unscaled()[2]),    # z2
            ScalerZeroOne(-1.0, 30.0),    # y2
            ScalerZeroOne(-5.0, 200.0),    # local objective function
            ScalerConstraint(-0.01, 0.01),    # local equality function
            ScalerConstraint(-120.0, 120.0),    # local inequality function 1
            ScalerZeroOne(-5.0, 120.0)    # y1
        ])

        self._subsystems[1].set_Scalers([
            copy.deepcopy(self._subsystems[0].get_Scalers()[1]),    # z1
            copy.deepcopy(self._subsystems[0].get_Scalers()[2]),    # z2
            copy.deepcopy(self._subsystems[0].get_Scalers()[7]),    # y1
            ScalerZeroOne(0.0, 0.01),    # local objective function
            ScalerConstraint(-0.01, 0.01),    # local equality function
            ScalerConstraint(-50.0, 50.0),    # local inequality function 1
            copy.deepcopy(self._subsystems[0].get_Scalers()[3])    # y2
        ])
        
        # ── Step 6: Design variable initialization & reference state ──────
        # Set granularity (step sizes), initial values, and (optionally)
        # reference values / coupling metadata for each subsystem's design
        # variables. Values are scaled via .transform().
        # Order: local design variables,
        #        shared design variables,
        #        additional design variables(as a result of decomposition)
        self._subsystems[0].set_DesignVariables_Granularity([0.0, 0.0, 0.0, 0.0])  # x, z1, z2, y2
        self._subsystems[0].set_DesignVariables([self._subsystems[0].get_Scalers()[0].transform(0.0),   # x
                                                 self._subsystems[0].get_Scalers()[1].transform(5.0),   # z1
                                                 self._subsystems[0].get_Scalers()[2].transform(5.0),   # z2
                                                 self._subsystems[0].get_Scalers()[3].transform(7.848)  # y2
                                                 ])
        self._subsystems[0].set_ReferenceDesignVariables([self._subsystems[0].get_Scalers()[0].transform(0.0),        # x
                                                          self._subsystems[0].get_Scalers()[1].transform(1.9776),     # z1
                                                          self._subsystems[0].get_Scalers()[2].transform(0.0),        # z2
                                                          self._subsystems[0].get_Scalers()[3].transform(3.13227167)  # y2
                                                          ])
        self._subsystems[0].set_ReferenceLocalObjectiveValue(self._subsystems[0].get_Scalers()[4].transform(3.18339))
        self._subsystems[0].set_ReferenceLocalObjectiveValueUnscaled(3.18339)
        # self._subsystems[0].set_DesignVariablesInfluenceAnyCouplingBool([False, True, True, True])
        # self._subsystems[0].set_NeighborID_for_additional_dv([None, None, None, ["1"]])
        
        self._subsystems[1].set_DesignVariables_Granularity([0.0, 0.0, 0.0])  # z1, z2, y1
        self._subsystems[1].set_DesignVariables([self._subsystems[1].get_Scalers()[0].transform(5.0),  # z1
                                                 self._subsystems[1].get_Scalers()[1].transform(5.0),  # z2
                                                 self._subsystems[1].get_Scalers()[2].transform(8.43)  # y1
                                                 ])
        self._subsystems[1].set_ReferenceDesignVariables([self._subsystems[1].get_Scalers()[0].transform(1.9776),      # z1
                                                          self._subsystems[1].get_Scalers()[1].transform(0.0),         # z2
                                                          self._subsystems[1].get_Scalers()[2].transform(1.333266665)  # y1
                                                          ])
        self._subsystems[1].set_ReferenceLocalObjectiveValue(None)
        self._subsystems[1].set_ReferenceLocalObjectiveValueUnscaled(None)
        # self._subsystems[1].set_DesignVariablesInfluenceAnyCouplingBool([True, True, True])
        # self._subsystems[1].set_NeighborID_for_additional_dv([None, None, ["0"]])
        
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
        self._subsystems[0].set_CouplingVariables("1", [self._subsystems[0].get_Scalers()[3].transform(7.848)], [7.848])  # y2
        self._subsystems[0].set_Indices_CouplingVariables_in_DesignVariables("1", [3])
        
        self._subsystems[0].set_MappedResponseVariables("1", [self._subsystems[0].get_Scalers()[7].transform(8.43)], [8.43])  # y1
        
        self._subsystems[0].set_SharedDesignVariables("1", [self._subsystems[0].get_Scalers()[1].transform(5.0),
                                                            self._subsystems[0].get_Scalers()[2].transform(5.0)],
                                                           [5.0, 5.0])  # z1 z2
        self._subsystems[0].set_Indices_SharedDesignVariables_in_DesignVariables("1", [1, 2])

        self._subsystems[0].set_Copy_MappedResponseVariables("1", [self._subsystems[1].get_Scalers()[6].transform(7.848)])  # y2

        self._subsystems[0].set_Copy_CouplingVariables("1", [self._subsystems[1].get_Scalers()[2].transform(8.43)])  # y1
        
        self._subsystems[0].set_Copy_TargetSharedDesignVariables("1", [self._subsystems[1].get_Scalers()[0].transform(5.0),
                                                                       self._subsystems[1].get_Scalers()[1].transform(5.0)])  # z1 z2

        # ── circle 1 - 0 (reciprocal of circle 0 - 1) ──
        self._subsystems[1].set_Copy_CouplingVariables("0", [self._subsystems[0].get_Scalers()[3].transform(7.848)])  # y2
        
        self._subsystems[1].set_Copy_MappedResponseVariables("0", [self._subsystems[0].get_Scalers()[7].transform(8.43)])  # y1
        
        self._subsystems[1].set_Copy_SharedDesignVariables("0", [self._subsystems[0].get_Scalers()[1].transform(5.0),
                                                                 self._subsystems[0].get_Scalers()[2].transform(5.0)])  # z1 z2

        self._subsystems[1].set_MappedResponseVariables("0", [self._subsystems[1].get_Scalers()[6].transform(7.848)], [7.848])  # y2

        self._subsystems[1].set_CouplingVariables("0", [self._subsystems[1].get_Scalers()[2].transform(8.43)], [8.43])  # y1
        self._subsystems[1].set_Indices_CouplingVariables_in_DesignVariables("0", [2])
        
        self._subsystems[1].set_TargetSharedDesignVariables("0", [self._subsystems[1].get_Scalers()[0].transform(5.0),
                                                                  self._subsystems[1].get_Scalers()[1].transform(5.0)],
                                                                 [5.0, 5.0])  # z1 z2
        self._subsystems[1].set_Indices_TargetSharedDesignVariables_in_DesignVariables("0", [0, 1])
