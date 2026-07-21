---
title: InputFile (Source)
---

← Back to [InputFile documentation](InputFile.md)

# InputFile - Source Code

**File:** `userfiles\TwoBarTruss\InputFile.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU General Public License v3.0. See LICENSE file for details.
"""Input file configuration for Two-Bar Truss problem with non-hierarchic decomposition.

This module defines the configuration for distributed optimization of the
Two-Bar Truss structural problem using Augmented Lagrangian Coordination (ALC)
with non-hierarchic decomposition into three subsystems.
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
from userfiles.TwoBarTruss.subsystem0 import Analysis0, LocalObjective0, LocalConstraints0, Optimization0
from userfiles.TwoBarTruss.subsystem1 import Analysis1, LocalObjective1, LocalConstraints1, Optimization1
from userfiles.TwoBarTruss.subsystem2 import Analysis2, LocalObjective2, LocalConstraints2, Optimization2


class InputFile(InputFileBasis):
    """Configuration class for Two-Bar Truss problem with non-hierarchic ALC.

    Defines the problem structure for the Two-Bar Truss structural optimization
    with three subsystems: system-level (FEM), bar 1, and bar 2.

    Attributes:
        _name: Problem identifier string.
        _coordinationmethod: Coordination algorithm (ALC variants).
        _subsystems: List of configured subsystem objects.
    """

    def __init__(self) -> None:
        """Initialize the Two-Bar Truss problem configuration.

        Sets up three subsystems: system-level FEM analysis, bar 1 sizing,
        and bar 2 sizing with their coupling relationships.
        """
        
        # ── Step 1: Use-case name and coordination method ────────────────
        super().__init__()
        self._name = "TwoBarTruss"
        
        # Initialize the coordination method of choice.
        # Uncomment one of the alternatives below to switch algorithm.
        # self._coordinationmethod: CoordinationMethodInterface = PC(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1E-5),
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
        self._coordinationmethod: CoordinationMethodInterface = ALC(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1E4),
                                                                    convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-5),
                                                                    updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights(
                                                                        beta=1.1,
                                                                        gamma=0.95,
                                                                        initialweight=0.01,
                                                                        initialmultiplier=0.0),
                                                                    iterationscheme=ParallelPerLevelIncreasing())
        # self._coordinationmethod: CoordinationMethodInterface = Consensus_ALC(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1000.0),
        #                                                                       convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-5),
        #                                                                       updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights(
        #                                                                           beta=1.1,
        #                                                                           gamma=0.95,
        #                                                                           initialweight=0.01,
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
        
        level_list: List[int] = [0,
                                 1,
                                 1]
        
        neighborid_list: List[List[str]] = [["1", "2"],
                                            ["0"],
                                            ["0"]]
        
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
        self._subsystems[0].set_LowerBounds_Unscaled([2.0 * 1E-1,            # local support 1
                                                      1.0 * 1E-1,            # local support 2
                                                      1.590 * 1E-4 * 1E-3,   # cross area 1
                                                      1.590 * 1E-4 * 1E-3])  # cross area 2
        
        self._subsystems[1].set_LowerBounds_Unscaled([1.0 * 1E-2 * 1E-1,     # radius 1
                                                      1.5900 * 1E-2 * 1E-2,  # thickness 1
                                                      -1.0 * 1E2 * 1E4])     # nodal force 1
        
        self._subsystems[2].set_LowerBounds_Unscaled([1.0 * 1E-2 * 1E-1,     # radius 2
                                                      1.5900 * 1E-2 * 1E-2,  # thickness 2
                                                      -1.0 * 1E2 * 1E4,      # nodal force 2
                                                      1.005])                # length 2

        self._subsystems[0].set_UpperBounds_Unscaled([1.0,          # local support 1
                                                      1.1,          # local support 2
                                                      1.0 * 1E-4,   # cross area 1
                                                      1.0 * 1E-4])  # cross area 2
        
        self._subsystems[1].set_UpperBounds_Unscaled([1.0 * 1E-1,        # radius 1
                                                      1.0 * 1E-2,        # thickness 1
                                                      1.0 * 1E2 * 1E4])  # nodal force 1
        
        self._subsystems[2].set_UpperBounds_Unscaled([1.0 * 1E-1,       # radius 2
                                                      1.0 * 1E-2,       # thickness 2
                                                      1.0 * 1E2 * 1E4,  # nodal force 2
                                                      1.487])           # length 2
        
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
            ScalerZeroOne(self._subsystems[0].get_LowerBounds_Unscaled()[0], self._subsystems[0].get_UpperBounds_Unscaled()[0]),  # [0] local support 1
            ScalerZeroOne(self._subsystems[0].get_LowerBounds_Unscaled()[1], self._subsystems[0].get_UpperBounds_Unscaled()[1]),  # [1] local support 2
            ScalerZeroOne(self._subsystems[0].get_LowerBounds_Unscaled()[2], 0.01),                                               # [2] cross area 1
            ScalerZeroOne(self._subsystems[0].get_LowerBounds_Unscaled()[3], 0.01),                                               # [3] cross area 2
            ScalerZeroOne(0.0, 5.0),                                                                                              # [4] local objective function
            ScalerConstraint(-0.01, 0.01),                                                                                        # [5] local equality function
            ScalerConstraint(-1E3, 1E3),                                                                                          # [6] local inequality function 
            ScalerZeroOne(self._subsystems[1].get_LowerBounds_Unscaled()[2], self._subsystems[1].get_UpperBounds_Unscaled()[2]),  # [7] nodal force 1
            ScalerZeroOne(self._subsystems[2].get_LowerBounds_Unscaled()[2], self._subsystems[2].get_UpperBounds_Unscaled()[2]),  # [8] nodal force 2
            ScalerZeroOne(1.0, self._subsystems[2].get_UpperBounds_Unscaled()[3]),                                                # [9] length 2
        ])
        
        self._subsystems[1].set_Scalers([
            ScalerZeroOne(self._subsystems[1].get_LowerBounds_Unscaled()[0], self._subsystems[1].get_UpperBounds_Unscaled()[0]),  # [0] radius 1
            ScalerZeroOne(self._subsystems[1].get_LowerBounds_Unscaled()[1], self._subsystems[1].get_UpperBounds_Unscaled()[1]),  # [1] thickness 1
            copy.deepcopy(self._subsystems[0].get_Scalers()[7]),                                                                  # [2] nodal force 1
            ScalerZeroOne(0.0, 0.01),                                                                                             # [3] local objective function
            ScalerConstraint(-0.01, 0.01),                                                                                        # [4] local equality function
            ScalerConstraint(-500.0, 500.0),                                                                                      # [5] local inequality function
            copy.deepcopy(self._subsystems[0].get_Scalers()[2])                                                                   # [6] cross area 1
        ])
        
        self._subsystems[2].set_Scalers([
            ScalerZeroOne(self._subsystems[2].get_LowerBounds_Unscaled()[0], self._subsystems[2].get_UpperBounds_Unscaled()[0]),  # [0] radius 2
            ScalerZeroOne(self._subsystems[2].get_LowerBounds_Unscaled()[1], self._subsystems[2].get_UpperBounds_Unscaled()[1]),  # [1] thickness 2
            copy.deepcopy(self._subsystems[0].get_Scalers()[8]),                                                                  # [2] nodal force 2
            copy.deepcopy(self._subsystems[0].get_Scalers()[9]),                                                                  # [3] length 2
            ScalerZeroOne(0.0, 0.01),                                                                                             # [4] local objective function
            ScalerConstraint(-0.01, 0.01),                                                                                        # [5] local equality function
            ScalerConstraint(-2E3, 2E3),                                                                                          # [6] local inequality function
            copy.deepcopy(self._subsystems[0].get_Scalers()[3]),                                                                  # [7] cross area 2
        ])
        
        # ── Step 6: Design variable initialization & reference state ──────
        # Set granularity (step sizes), initial values, and (optionally)
        # reference values / coupling metadata for each subsystem's design
        # variables. Values are scaled via .transform().
        # Order: local design variables,
        #        shared design variables,
        #        additional design variables(as a result of decomposition)
        self._subsystems[0].set_DesignVariables_Granularity([0.0, 0.0, 0.0, 0.0])
        self._subsystems[0].set_DesignVariables([self._subsystems[0].get_Scalers()[0].transform(5.6384 * 1E-1),         # local support 1
                                                 self._subsystems[0].get_Scalers()[1].transform(1.7000 * 1E-1),         # local support 2
                                                 self._subsystems[0].get_Scalers()[2].transform(2.0 * 1E-5),            # cross area 1
                                                 self._subsystems[0].get_Scalers()[3].transform(7.0955 * 1E-2 * 1E-3)   # cross area 2
                                                 ])
        self._subsystems[0].set_ReferenceDesignVariables([self._subsystems[0].get_Scalers()[0].transform(9.03 * 1E-1),  # local support 1
                                                          self._subsystems[0].get_Scalers()[1].transform(6.55 * 1E-1),  # local support 2
                                                          self._subsystems[0].get_Scalers()[2].transform(2.0 * 1E-5),   # cross area 1
                                                          self._subsystems[0].get_Scalers()[3].transform(3.12 * 1E-5)   # cross area 2
                                                          ])
        self._subsystems[0].set_ReferenceLocalObjectiveValue(self._subsystems[0].get_Scalers()[4].transform(1.06))
        self._subsystems[0].set_ReferenceLocalObjectiveValueUnscaled(1.06)
        # self._subsystems[0].set_DesignVariablesInfluenceAnyCouplingBool([None, None, None, None])
        # self._subsystems[0].set_NeighborID_for_additional_dv([None, None, ["1"], ["2"]])
        
        # local design variables
        # coupling variables as design variables
        self._subsystems[1].set_DesignVariables_Granularity([0.0, 0.0, 0.0])
        self._subsystems[1].set_DesignVariables([self._subsystems[1].get_Scalers()[0].transform(1.7028 * 1E-1 * 1E-1),    # radius 1
                                                 self._subsystems[1].get_Scalers()[1].transform(1.1834 * 1E-1 * 1E-2),    # thickness 1
                                                 self._subsystems[1].get_Scalers()[2].transform(1.528960935166501 * 1E4)  # nodal force 1
                                                 ])
        self._subsystems[1].set_ReferenceDesignVariables([self._subsystems[1].get_Scalers()[0].transform(6.22 * 1E-3),    # radius 1
                                                          self._subsystems[1].get_Scalers()[1].transform(5.12 * 1E-4),    # thickness 1
                                                          self._subsystems[1].get_Scalers()[2].transform(8.64 * 1E3)      # nodal force 1
                                                          ])
        self._subsystems[1].set_ReferenceLocalObjectiveValue(None)
        self._subsystems[1].set_ReferenceLocalObjectiveValueUnscaled(None)
        # self._subsystems[1].set_DesignVariablesInfluenceAnyCouplingBool([None, None, None])
        # self._subsystems[1].set_NeighborID_for_additional_dv([None, None, ["0"]])
        
        # local design variables
        # coupling variables as design variables
        self._subsystems[2].set_DesignVariables_Granularity([0.0, 0.0, 0.0, 0.0])
        self._subsystems[2].set_DesignVariables([self._subsystems[2].get_Scalers()[0].transform(1.5068 * 1E-1 * 1E-1),      # radius 2
                                                 self._subsystems[2].get_Scalers()[1].transform(7.4946 * 1E-2 * 1E-2),      # thickness 2
                                                 self._subsystems[2].get_Scalers()[2].transform(-1.354928162705639 * 1E4),  # nodal force 2
                                                 self._subsystems[2].get_Scalers()[3].transform(1.017334261685902)          # length 2
                                                 ])
        self._subsystems[2].set_ReferenceDesignVariables([self._subsystems[2].get_Scalers()[0].transform(3.12 * 1E-2),  # radius 2
                                                          self._subsystems[2].get_Scalers()[1].transform(1.59 * 1E-4),  # thickness 2
                                                          self._subsystems[2].get_Scalers()[2].transform(-7.67 * 1E3),  # nodal force 2
                                                          self._subsystems[2].get_Scalers()[3].transform(1.20)          # length 2
                                                          ])
        self._subsystems[2].set_ReferenceLocalObjectiveValue(None)
        self._subsystems[2].set_ReferenceLocalObjectiveValueUnscaled(None)
        # self._subsystems[2].set_DesignVariablesInfluenceAnyCouplingBool([None, None, None, None])
        # self._subsystems[2].set_NeighborID_for_additional_dv([None, None, ["0"], ["0"]])
        
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
        self._subsystems[0].set_CouplingVariables("1", [self._subsystems[0].get_Scalers()[2].transform(2.0 * 1E-5)], [2.0 * 1E-5])  # cross area 1        
        
        self._subsystems[0].set_Copy_MappedResponseVariables("1", [self._subsystems[1].get_Scalers()[6].transform(1.266179497797590 * 1E-1 * 1E-3)])  # cross area 1

        self._subsystems[0].set_MappedResponseVariables("1", [self._subsystems[0].get_Scalers()[7].transform(1.528960935166501 * 1E4)], [1.528960935166501 * 1E4])  # nodal force 1

        self._subsystems[0].set_Copy_CouplingVariables("1", [self._subsystems[1].get_Scalers()[2].transform(1.528960935166501 * 1E4)])  # nodal force 1
        
        # ── circle 0 - 2 ──
        self._subsystems[0].set_CouplingVariables("2", [self._subsystems[0].get_Scalers()[3].transform(7.095468173727783 * 1E-2 * 1E-3)], [7.095468173727783 * 1E-2 * 1E-3])  # cross area 2

        self._subsystems[0].set_Copy_MappedResponseVariables("2", [self._subsystems[2].get_Scalers()[7].transform(7.095468173727783 * 1E-2 * 1E-3)])  # cross area 2

        self._subsystems[0].set_MappedResponseVariables("2", [self._subsystems[0].get_Scalers()[8].transform(-1.354928162705639 * 1E4),  # nodal force 2
                                                              self._subsystems[0].get_Scalers()[9].transform(1.017334261685902)],        # length 2
                                                             [-1.354928162705639 * 1E4, 1.017334261685902]
                                                        )

        self._subsystems[0].set_Copy_CouplingVariables("2", [self._subsystems[2].get_Scalers()[2].transform(-1.354928162705639 * 1E4),  # nodal force 2
                                                             self._subsystems[2].get_Scalers()[3].transform(1.017334261685902)]       # length 2
                                                      )
        
        # ── circle 1 - 0 (reciprocal of circle 0 - 1) ──
        self._subsystems[1].set_MappedResponseVariables("0", [self._subsystems[1].get_Scalers()[6].transform(1.266179497797590 * 1E-1 * 1E-3)], [1.266179497797590 * 1E-1 * 1E-3])  # cross area 1

        self._subsystems[1].set_Copy_CouplingVariables("0", [self._subsystems[0].get_Scalers()[2].transform(1.266179497797590 * 1E-1 * 1E-3)])  # cross area 1

        self._subsystems[1].set_Copy_MappedResponseVariables("0", [self._subsystems[0].get_Scalers()[7].transform(1.528960935166501 * 1E4)])  # nodal force 1

        self._subsystems[1].set_CouplingVariables("0", [self._subsystems[1].get_Scalers()[2].transform(1.528960935166501 * 1E4)], [1.528960935166501 * 1E4])  # nodal force 1
           
        # ── circle 2 - 0 (reciprocal of circle 0 - 2) ──
        self._subsystems[2].set_MappedResponseVariables("0", [self._subsystems[2].get_Scalers()[7].transform(7.095468173727783 * 1E-2 * 1E-3)], [7.095468173727783 * 1E-2 * 1E-3])  # cross area 2

        self._subsystems[2].set_Copy_CouplingVariables("0", [self._subsystems[0].get_Scalers()[3].transform(7.095468173727783 * 1E-2 * 1E-3)])  # cross area 2

        self._subsystems[2].set_Copy_MappedResponseVariables("0", [self._subsystems[0].get_Scalers()[8].transform(-1.354928162705639 * 1E4),  # nodal force 2
                                                                   self._subsystems[0].get_Scalers()[9].transform(1.017334261685902)]         # length 2
                                                            )

        self._subsystems[2].set_CouplingVariables("0", [self._subsystems[2].get_Scalers()[2].transform(-1.354928162705639 * 1E4),  # nodal force 2
                                                        self._subsystems[2].get_Scalers()[3].transform(1.017334261685902)],        # length 2
                                                       [-1.354928162705639 * 1E4, 1.017334261685902]
                                                  )

```
