---
title: InputFile (Source)
---

← Back to [InputFile documentation](InputFile.md)

# InputFile - Source Code

**File:** `userfiles\SSBJ\InputFile.py`

```python
# Copyright (C) The DistributedDesignOptimizer Contributors
# Licensed under the GNU Lesser General Public License v3.0. See LICENSE file for details.
"""Input file configuration for Supersonic Business Jet (SSBJ) distributed optimization.

This module defines the InputFile class which configures all parameters for the
distributed optimization of the Supersonic Business Jet (SSBJ) multidisciplinary
problem, including subsystem definitions, coordination methods, iteration schemes,
coupling parameters, and scaling variables.
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

from userfiles.SSBJ.subsystem0 import LocalConstraints0, LocalObjective0, Analysis0, Optimization0
from userfiles.SSBJ.subsystem1 import LocalConstraints1, LocalObjective1, Analysis1, Optimization1
from userfiles.SSBJ.subsystem2 import LocalConstraints2, LocalObjective2, Analysis2, Optimization2
from userfiles.SSBJ.subsystem3 import LocalConstraints3, LocalObjective3, Analysis3, Optimization3


class InputFile(InputFileBasis):
    """Input file for Supersonic Business Jet (SSBJ) distributed optimization.

    Configures a four-subsystem distributed optimization problem by defining
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
        self._name = "SSBJ"
        
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
        self._coordinationmethod: CoordinationMethodInterface = ALC(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=5E-4),
                                                                    convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-5),
                                                                    updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights(
                                                                        beta=1.3,
                                                                        gamma=0.5,
                                                                        initialweight=0.01,
                                                                        initialmultiplier=0.0),
                                                                    iterationscheme=SequentialForward())
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
        id_list: List[str] = ["0",  # subsystem 0 (Aircraft)
                              "1",  # subsystem 1 (Propulsion)
                              "2",  # subsystem 2 (Aerodynamics)
                              "3"]  # subsystem 3 (Structure)
        
        level_list: List[int] = [0,
                                 1,
                                 1,
                                 1]
        
        neighborid_list: List[List[str]] = [["1", "2", "3"],  # subsystem 0 (Aircraft) is coupled to 1 (Propulsion), 2 (Aerodynamics) and 3 (Structure)
                                            ["0", "2"],       # subsystem 1 (Propulsion) is coupled to 0 (Aircraft) and 2 (Aerodynamics)
                                            ["0", "1", "3"],  # subsystem 2 (Aerodynamics) is coupled to 0 (Aircraft), 1 (Propulsion) and 3 (Structure)
                                            ["0", "2"]]       # subsystem 3 (Structure) is coupled to 0 (Aircraft) and 2 (Aerodynamics)
        
        # ── Step 3: Instantiate subsystem-specific components ──────────
        # One instance per subsystem for: analysis model, local objective,
        # local constraints, and optimization solver.
        analysis_list: List[AnalysisInterface] = [Analysis0(),
                                                  Analysis1(),
                                                  Analysis2(),
                                                  Analysis3()]
        
        localobjective_list: List[LocalObjectiveInterface] = [LocalObjective0(),
                                                              LocalObjective1(),
                                                              LocalObjective2(),
                                                              LocalObjective3()]
        
        localconstraints_list: List[LocalConstraintsInterface] = [LocalConstraints0(),
                                                                  LocalConstraints1(),
                                                                  LocalConstraints2(),
                                                                  LocalConstraints3()]
        
        optimization_list: List[OptimizationInterface] = [Optimization0(),
                                                          Optimization1(),
                                                          Optimization2(),
                                                          Optimization3()]
        
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
        self._subsystems[0].set_LowerBounds_Unscaled([1.0,        # 0d[0] specific_fuel_consumption [1/hr]
                                                      100.0,      # 0d[1] engine_weight [lb]
                                                      0.1,        # 0d[2] lift_to_drag_ratio [-]
                                                      5000.0,     # 0d[3] structural_weight [lb]
                                                      5000.0])    # 0d[4] fuel_weight [lb]
                                           
        self._subsystems[1].set_LowerBounds_Unscaled([0.1,        # 1d[0] throttle [-]
                                                      1000.0])    # 1d[1] drag [lb]
        
        self._subsystems[2].set_LowerBounds_Unscaled([40.0,       # 2d[0] tail_sweep_angle [deg]
                                                      0.01,       # 2d[1] wing_moment_arm [ft]
                                                      1.0,        # 2d[2] tail_moment_arm [ft]
                                                      0.01,       # 2d[3] thickness_to_chord_ratio [-]
                                                      40.0,       # 2d[4] wing_sweep_angle [deg]
                                                      2.5,        # 2d[5] wing_aspect_ratio [-]
                                                      200.0,      # 2d[6] wing_surface_area [ft^2]
                                                      2.5,        # 2d[7] tail_aspect_ratio [-]
                                                      50.0,       # 2d[8] tail_surface_area [ft^2]
                                                      5000.0,     # 2d[9] total_weight [lb]
                                                      0.5,        # 2d[10] engine_scale_factor [-]
                                                      0.2         # 2d[11] wing_twist [deg]
                                                      ])
        
        self._subsystems[3].set_LowerBounds_Unscaled([0.1,        # 3d[0] taper ratio [-]
                                                      1e-4,       # 3d[1] alpha1 station 0 (top sandwich depth fraction) [-]
                                                      1e-4,       # 3d[2] alpha1 station 1 [-]
                                                      1e-4,       # 3d[3] alpha1 station 2 [-]
                                                      1e-4,       # 3d[4] alpha3 station 0 (bottom sandwich depth fraction) [-]
                                                      1e-4,       # 3d[5] alpha3 station 1 [-]
                                                      1e-4,       # 3d[6] alpha3 station 2 [-]
                                                      0.1,        # 3d[7] ts2 station 0 (web sandwich thickness) [in]
                                                      0.1,        # 3d[8] ts2 station 1 [in]
                                                      0.1,        # 3d[9] ts2 station 2 [in]
                                                      1e-3,       # 3d[10] rho1 station 0 (top skin ratio t1/ts1) [-]
                                                      1e-3,       # 3d[11] rho1 station 1 [-]
                                                      1e-3,       # 3d[12] rho1 station 2 [-]
                                                      1e-3,       # 3d[13] rho2 station 0 (web skin ratio t2/ts2) [-]
                                                      1e-3,       # 3d[14] rho2 station 1 [-]
                                                      1e-3,       # 3d[15] rho2 station 2 [-]
                                                      1e-3,       # 3d[16] rho3 station 0 (bottom skin ratio t3/ts3) [-]
                                                      1e-3,       # 3d[17] rho3 station 1 [-]
                                                      1e-3,       # 3d[18] rho3 station 2 [-]
                                                      0.01,       # 3d[19] thickness_to_chord_ratio [-]
                                                      40.0,       # 3d[20] wing_sweep_angle [deg]
                                                      2.5,        # 3d[21] wing_aspect_ratio [-]
                                                      200.0,      # 3d[22] wing_surface_area [ft^2]
                                                      2.5,        # 3d[23] tail_aspect_ratio [-]
                                                      50.0,       # 3d[24] tail_surface_area [ft^2]
                                                      5000.0])    # 3d[25] lift [lb]
                                                                                      
        self._subsystems[0].set_UpperBounds_Unscaled([4.0,           # 0d[0] specific_fuel_consumption [1/hr]
                                                      30000.0,       # 0d[1] engine_weight [lb]
                                                      10.0,          # 0d[2] lift_to_drag_ratio [-]
                                                      1E5,           # 0d[3] structural_weight [lb]
                                                      1E5])          # 0d[4] fuel_weight [lb]
                                           
        self._subsystems[1].set_UpperBounds_Unscaled([1.0,           # 1d[0] throttle [-]
                                                      70000.0])      # 1d[1] drag [lb]
        
        self._subsystems[2].set_UpperBounds_Unscaled([70.0,          # 2d[0] tail_sweep_angle [deg]
                                                      0.2,           # 2d[1] wing_moment_arm [ft]
                                                      3.5,           # 2d[2] tail_moment_arm [ft]
                                                      0.1,           # 2d[3] thickness_to_chord_ratio [-]
                                                      70.0,          # 2d[4] wing_sweep_angle [deg]
                                                      8.0,           # 2d[5] wing_aspect_ratio [-]
                                                      800.0,         # 2d[6] wing_surface_area [ft^2]
                                                      8.5,           # 2d[7] tail_aspect_ratio [-]
                                                      148.9,         # 2d[8] tail_surface_area [ft^2]
                                                      1E5,           # 2d[9] total_weight [lb]
                                                      1.5,           # 2d[10] engine_scale_factor [-]
                                                      50.0           # 2d[11] wing_twist [deg]
                                                      ])
        
        self._subsystems[3].set_UpperBounds_Unscaled([0.4,          # 3d[0] taper ratio [-]
                                                      0.5,          # 3d[1] alpha1 station 0 (h_spar-margin edge: alpha1+alpha3<=0.5) [-]
                                                      0.5,          # 3d[2] alpha1 station 1 [-]
                                                      0.5,          # 3d[3] alpha1 station 2 [-]
                                                      0.5,          # 3d[4] alpha3 station 0 [-]
                                                      0.5,          # 3d[5] alpha3 station 1 [-]
                                                      0.5,          # 3d[6] alpha3 station 2 [-]
                                                      9.0,          # 3d[7] ts2 station 0 (web sandwich) [in]
                                                      9.0,          # 3d[8] ts2 station 1 [in]
                                                      9.0,          # 3d[9] ts2 station 2 [in]
                                                      1.0 / 1.1,    # 3d[10] rho1 station 0 (core-margin edge ts >= 1.1 t) [-]
                                                      1.0 / 1.1,    # 3d[11] rho1 station 1 [-]
                                                      1.0 / 1.1,    # 3d[12] rho1 station 2 [-]
                                                      1.0 / 1.1,    # 3d[13] rho2 station 0 [-]
                                                      1.0 / 1.1,    # 3d[14] rho2 station 1 [-]
                                                      1.0 / 1.1,    # 3d[15] rho2 station 2 [-]
                                                      1.0 / 1.1,    # 3d[16] rho3 station 0 [-]
                                                      1.0 / 1.1,    # 3d[17] rho3 station 1 [-]
                                                      1.0 / 1.1,    # 3d[18] rho3 station 2 [-]
                                                      0.1,          # 3d[19] thickness_to_chord_ratio [-]
                                                      70.0,         # 3d[20] wing_sweep_angle [deg]
                                                      8.0,          # 3d[21] wing_aspect_ratio [-]
                                                      800.0,        # 3d[22] wing_surface_area [ft^2]
                                                      8.5,          # 3d[23] tail_aspect_ratio [-]
                                                      148.9,        # 3d[24] tail_surface_area [ft^2]
                                                      100000.0])    # 3d[25] lift [lb]
        
        # ── Step 5: Scaling variables ──────────────────────────────────
        # Define one scaler per variable. ScalerZeroOne maps to [0, 1],
        # ScalerConstraint normalizes constraint values.
        # Order: local design variables, shared design variables,
        #        additional design variables (as a result of decomposition),
        #        local objective, local equality constraints,
        #        local inequality constraints,
        #        mapped responses, copy of mapped responses (only if not already included earlier for additional desing variables).
        
        self._subsystems[0].set_Scalers([
            ScalerZeroOne(0.9, self._subsystems[0].get_UpperBounds_Unscaled()[0]),                                                # [0] 0d[0] specific_fuel_consumption [1/hr]
            ScalerZeroOne(100.0, 206000.0),                                                                                       # [1] 0d[1] engine_weight [lb]
            ScalerZeroOne(-3.0, 15.0),                                                                                            # [2] 0d[2] lift_to_drag_ratio [-]
            ScalerZeroOne(self._subsystems[0].get_LowerBounds_Unscaled()[3], self._subsystems[0].get_UpperBounds_Unscaled()[3]),  # [3] 0d[3] structural_weight [lb]
            ScalerZeroOne(400.0, 1E5),                                                                                            # [4] 0d[4] fuel_weight [lb]
            ScalerZeroOne(9500.0, 230000.0),                                                                                      # [5] local objective scaler (total_weight [lb])
            ScalerConstraint(-1.0, 1.0),                                                                                          # [6] equality placeholder (None)
            ScalerConstraint(-20.0, 20.0),                                                                                        # [7] range constraint (range [nmi])
            ScalerZeroOne(5000.0, 250000.0),                                                                                      # [8] mapped response corresponding to 2d[9] total_weight [lb]
        ])
        
        self._subsystems[1].set_Scalers([
            ScalerZeroOne(self._subsystems[1].get_LowerBounds_Unscaled()[0], self._subsystems[1].get_UpperBounds_Unscaled()[0]),    # [0] 1d[0] throttle [-]
            ScalerZeroOne(800.0, 76500.0),                                                                                          # [1] 1d[1] drag [lb]
            ScalerZeroOne(0.0, 1.0),                                                                                                # [2] local objective placeholder (None)
            ScalerConstraint(-1.0, 1.0),                                                                                            # [3] equality placeholder (None)
            ScalerConstraint(-0.2, 0.2),                                                                                            # [4] engine temperature constraint (engine_temperature [-])
            ScalerConstraint(-4.2, 4.2),                                                                                            # [5] throttle setting constraint (dim_throttle/throttle_uA [-])
            copy.deepcopy(self._subsystems[0].get_Scalers()[0]),                                                                    # [6] mapped response corresponding to 0d[0] specific_fuel_consumption [1/hr]
            copy.deepcopy(self._subsystems[0].get_Scalers()[1]),                                                                    # [7] mapped response corresponding to 0d[1] engine_weight [lb]
            ScalerZeroOne(0.05, 20.0),                                                                                              # [8] mapped response corresponding to 2d[10] engine_scale_factor [-]
        ])

        self._subsystems[2].set_Scalers([
            ScalerZeroOne(self._subsystems[2].get_LowerBounds_Unscaled()[0], self._subsystems[2].get_UpperBounds_Unscaled()[0]),     # [0] 2d[0] tail_sweep_angle [deg]
            ScalerZeroOne(self._subsystems[2].get_LowerBounds_Unscaled()[1], self._subsystems[2].get_UpperBounds_Unscaled()[1]),     # [1] 2d[1] wing_moment_arm [ft]
            ScalerZeroOne(self._subsystems[2].get_LowerBounds_Unscaled()[2], self._subsystems[2].get_UpperBounds_Unscaled()[2]),     # [2] 2d[2] tail_moment_arm [ft]
            ScalerZeroOne(self._subsystems[2].get_LowerBounds_Unscaled()[3], self._subsystems[2].get_UpperBounds_Unscaled()[3]),     # [3] 2d[3] thickness_to_chord_ratio [-]
            ScalerZeroOne(self._subsystems[2].get_LowerBounds_Unscaled()[4], self._subsystems[2].get_UpperBounds_Unscaled()[4]),     # [4] 2d[4] wing_sweep_angle [deg]
            ScalerZeroOne(self._subsystems[2].get_LowerBounds_Unscaled()[5], self._subsystems[2].get_UpperBounds_Unscaled()[5]),     # [5] 2d[5] wing_aspect_ratio [-]
            ScalerZeroOne(self._subsystems[2].get_LowerBounds_Unscaled()[6], self._subsystems[2].get_UpperBounds_Unscaled()[6]),     # [6] 2d[6] wing_surface_area [ft^2]
            ScalerZeroOne(self._subsystems[2].get_LowerBounds_Unscaled()[7], self._subsystems[2].get_UpperBounds_Unscaled()[7]),     # [7] 2d[7] tail_aspect_ratio [-]
            ScalerZeroOne(self._subsystems[2].get_LowerBounds_Unscaled()[8], self._subsystems[2].get_UpperBounds_Unscaled()[8]),     # [8] 2d[8] tail_surface_area [ft^2]
            copy.deepcopy(self._subsystems[0].get_Scalers()[8]),                                                                     # [9] 2d[9] total_weight [lb]
            copy.deepcopy(self._subsystems[1].get_Scalers()[8]),                                                                     # [10] 2d[10] engine_scale_factor [-]
            ScalerZeroOne(-2400.0, 2100.0),                                                                                          # [11] 2d[11] wing_twist [deg]
            ScalerZeroOne(0.0, 1.0),                                                                                                 # [12] local objective placeholder (None)
            ScalerConstraint(-1.0, 1.0),                                                                                             # [13] equality placeholder (None)
            ScalerConstraint(-0.2, 0.2),                                                                                             # [14] pressure gradient constraint [-]
            ScalerConstraint(-3.8, 3.8),                                                                                             # [15] lift coefficient constraint 1 [-]
            ScalerConstraint(-1.8, 1.8),                                                                                             # [16] lift coefficient constraint 2 [-]
            copy.deepcopy(self._subsystems[0].get_Scalers()[2]),                                                                     # [17] mapped response corresponding to 0d[2] lift_to_drag_ratio [-]
            copy.deepcopy(self._subsystems[1].get_Scalers()[1]),                                                                     # [18] mapped response corresponding to 1d[1] drag [lb]
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[25], self._subsystems[3].get_UpperBounds_Unscaled()[25]),   # [19] mapped response corresponding to 3d[25] lift [lb]
        ])
        
        self._subsystems[3].set_Scalers([
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[0], self._subsystems[3].get_UpperBounds_Unscaled()[0]),       # [0] 3d[0] taper ratio [-]
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[1], self._subsystems[3].get_UpperBounds_Unscaled()[1]),       # [1] 3d[1] alpha1 station 0 [-]
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[2], self._subsystems[3].get_UpperBounds_Unscaled()[2]),       # [2] 3d[2] alpha1 station 1 [-]
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[3], self._subsystems[3].get_UpperBounds_Unscaled()[3]),       # [3] 3d[3] alpha1 station 2 [-]
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[4], self._subsystems[3].get_UpperBounds_Unscaled()[4]),       # [4] 3d[4] alpha3 station 0 [-]
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[5], self._subsystems[3].get_UpperBounds_Unscaled()[5]),       # [5] 3d[5] alpha3 station 1 [-]
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[6], self._subsystems[3].get_UpperBounds_Unscaled()[6]),       # [6] 3d[6] alpha3 station 2 [-]
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[7], self._subsystems[3].get_UpperBounds_Unscaled()[7]),       # [7] 3d[7] ts2 station 0 (web sandwich) [in]
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[8], self._subsystems[3].get_UpperBounds_Unscaled()[8]),       # [8] 3d[8] ts2 station 1 [in]
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[9], self._subsystems[3].get_UpperBounds_Unscaled()[9]),       # [9] 3d[9] ts2 station 2 [in]
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[10], self._subsystems[3].get_UpperBounds_Unscaled()[10]),     # [10] 3d[10] rho1 station 0 [-]
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[11], self._subsystems[3].get_UpperBounds_Unscaled()[11]),     # [11] 3d[11] rho1 station 1 [-]
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[12], self._subsystems[3].get_UpperBounds_Unscaled()[12]),     # [12] 3d[12] rho1 station 2 [-]
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[13], self._subsystems[3].get_UpperBounds_Unscaled()[13]),     # [13] 3d[13] rho2 station 0 [-]
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[14], self._subsystems[3].get_UpperBounds_Unscaled()[14]),     # [14] 3d[14] rho2 station 1 [-]
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[15], self._subsystems[3].get_UpperBounds_Unscaled()[15]),     # [15] 3d[15] rho2 station 2 [-]
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[16], self._subsystems[3].get_UpperBounds_Unscaled()[16]),     # [16] 3d[16] rho3 station 0 [-]
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[17], self._subsystems[3].get_UpperBounds_Unscaled()[17]),     # [17] 3d[17] rho3 station 1 [-]
            ScalerZeroOne(self._subsystems[3].get_LowerBounds_Unscaled()[18], self._subsystems[3].get_UpperBounds_Unscaled()[18]),     # [18] 3d[18] rho3 station 2 [-]
            copy.deepcopy(self._subsystems[2].get_Scalers()[3]),                                                                       # [19] 3d[19] thickness_to_chord_ratio [-]
            copy.deepcopy(self._subsystems[2].get_Scalers()[4]),                                                                       # [20] 3d[20] wing_sweep_angle [deg]
            copy.deepcopy(self._subsystems[2].get_Scalers()[5]),                                                                       # [21] 3d[21] wing_aspect_ratio [-]
            copy.deepcopy(self._subsystems[2].get_Scalers()[6]),                                                                       # [22] 3d[22] wing_surface_area [ft^2]
            copy.deepcopy(self._subsystems[2].get_Scalers()[7]),                                                                       # [23] 3d[23] tail_aspect_ratio [-]
            copy.deepcopy(self._subsystems[2].get_Scalers()[8]),                                                                       # [24] 3d[24] tail_surface_area [ft^2]
            copy.deepcopy(self._subsystems[2].get_Scalers()[19]),                                                                      # [25] 3d[25] lift [lb]
            ScalerZeroOne(0.0, 1.0),                                                                                                   # [26] local objective placeholder (None)
            ScalerConstraint(-1.0, 1.0),                                                                                               # [27] equality placeholder (None)
            ScalerConstraint(-10.0, 10.0),                                                                                             # [28] compressive stress point 1 station 0 (G1[0:3])
            ScalerConstraint(-50.0, 50.0),                                                                                             # [29] compressive stress point 1 station 1
            ScalerConstraint(-50.0, 50.0),                                                                                             # [30] compressive stress point 1 station 2
            ScalerConstraint(-1000.0, 1000.0),                                                                                         # [31] buckling point 1 compressive station 0 (G1[3:6])
            ScalerConstraint(-500.0, 500.0),                                                                                           # [32] buckling point 1 compressive station 1
            ScalerConstraint(-500.0, 500.0),                                                                                           # [33] buckling point 1 compressive station 2
            ScalerConstraint(-1000.0, 1000.0),                                                                                         # [34] buckling point 1 shear station 0 (G1[6:9])
            ScalerConstraint(-500.0, 500.0),                                                                                           # [35] buckling point 1 shear station 1
            ScalerConstraint(-500.0, 500.0),                                                                                           # [36] buckling point 1 shear station 2
            ScalerConstraint(-10.0, 10.0),                                                                                             # [37] compressive stress point 2 station 0 (G1[9:12])
            ScalerConstraint(-20.0, 20.0),                                                                                             # [38] compressive stress point 2 station 1
            ScalerConstraint(-10.0, 10.0),                                                                                             # [39] compressive stress point 2 station 2
            ScalerConstraint(-1000.0, 1000.0),                                                                                         # [40] buckling point 2 compressive station 0 (G1[12:15])
            ScalerConstraint(-1000.0, 1000.0),                                                                                         # [41] buckling point 2 compressive station 1
            ScalerConstraint(-1000.0, 1000.0),                                                                                         # [42] buckling point 2 compressive station 2
            ScalerConstraint(-1000.0, 1000.0),                                                                                         # [43] buckling point 2 shear station 0 (G1[15:18])
            ScalerConstraint(-1000.0, 1000.0),                                                                                         # [44] buckling point 2 shear station 1
            ScalerConstraint(-1000.0, 1000.0),                                                                                         # [45] buckling point 2 shear station 2
            ScalerConstraint(-10.0, 10.0),                                                                                             # [46] compressive stress point 3 station 0 (G1[18:21])
            ScalerConstraint(-50.0, 50.0),                                                                                             # [47] compressive stress point 3 station 1
            ScalerConstraint(-50.0, 50.0),                                                                                             # [48] compressive stress point 3 station 2
            ScalerConstraint(-1200.0, 1200.0),                                                                                         # [49] buckling point 3 compressive station 0 (G1[21:24])
            ScalerConstraint(-1000.0, 1000.0),                                                                                         # [50] buckling point 3 compressive station 1
            ScalerConstraint(-500.0, 500.0),                                                                                           # [51] buckling point 3 compressive station 2
            ScalerConstraint(-10000.0, 10000.0),                                                                                       # [52] buckling point 3 shear station 0 (G1[24:27])
            ScalerConstraint(-1000.0, 1000.0),                                                                                         # [53] buckling point 3 shear station 1
            ScalerConstraint(-500.0, 500.0),                                                                                           # [54] buckling point 3 shear station 2
            ScalerConstraint(-10.0, 10.0),                                                                                             # [55] tensile stress point 4 station 0 (G1[27:30])
            ScalerConstraint(-50.0, 50.0),                                                                                             # [56] tensile stress point 4 station 1
            ScalerConstraint(-50.0, 50.0),                                                                                             # [57] tensile stress point 4 station 2
            ScalerConstraint(-50.0, 50.0),                                                                                             # [58] tensile stress point 5 station 0 (G1[30:33])
            ScalerConstraint(-10.0, 10.0),                                                                                             # [59] tensile stress point 5 station 1
            ScalerConstraint(-10.0, 10.0),                                                                                             # [60] tensile stress point 5 station 2
            ScalerConstraint(-1500.0, 1500.0),                                                                                         # [61] buckling point 5 compressive station 0 (G1[33:36])
            ScalerConstraint(-1000.0, 1000.0),                                                                                         # [62] buckling point 5 compressive station 1
            ScalerConstraint(-1000.0, 1000.0),                                                                                         # [63] buckling point 5 compressive station 2
            ScalerConstraint(-1500.0, 1500.0),                                                                                         # [64] buckling point 5 shear station 0 (G1[36:39])
            ScalerConstraint(-1000.0, 1000.0),                                                                                         # [65] buckling point 5 shear station 1
            ScalerConstraint(-1000.0, 1000.0),                                                                                         # [66] buckling point 5 shear station 2
            ScalerConstraint(-10.0, 10.0),                                                                                             # [67] tensile stress point 6 station 0 (G1[39:42])
            ScalerConstraint(-50.0, 50.0),                                                                                             # [68] tensile stress point 6 station 1
            ScalerConstraint(-50.0, 50.0),                                                                                             # [69] tensile stress point 6 station 2
            ScalerConstraint(-10.0, 10.0),                                                                                             # [70] tensile stress point 1 sign-flip station 0 (G1[54:57])
            ScalerConstraint(-50.0, 50.0),                                                                                             # [71] tensile stress point 1 sign-flip station 1
            ScalerConstraint(-50.0, 50.0),                                                                                             # [72] tensile stress point 1 sign-flip station 2
            ScalerConstraint(-10.0, 10.0),                                                                                             # [73] tensile stress point 2 sign-flip station 0 (G1[57:60])
            ScalerConstraint(-20.0, 20.0),                                                                                             # [74] tensile stress point 2 sign-flip station 1
            ScalerConstraint(-10.0, 10.0),                                                                                             # [75] tensile stress point 2 sign-flip station 2
            ScalerConstraint(-10.0, 10.0),                                                                                             # [76] tensile stress point 3 sign-flip station 0 (G1[60:63])
            ScalerConstraint(-50.0, 50.0),                                                                                             # [77] tensile stress point 3 sign-flip station 1
            ScalerConstraint(-50.0, 50.0),                                                                                             # [78] tensile stress point 3 sign-flip station 2
            ScalerConstraint(-10.0, 10.0),                                                                                             # [79] compressive stress point 4 sign-flip station 0 (G1[63:66])
            ScalerConstraint(-50.0, 50.0),                                                                                             # [80] compressive stress point 4 sign-flip station 1
            ScalerConstraint(-50.0, 50.0),                                                                                             # [81] compressive stress point 4 sign-flip station 2
            ScalerConstraint(-50.0, 50.0),                                                                                             # [82] compressive stress point 5 sign-flip station 0 (G1[66:69])
            ScalerConstraint(-10.0, 10.0),                                                                                             # [83] compressive stress point 5 sign-flip station 1
            ScalerConstraint(-10.0, 10.0),                                                                                             # [84] compressive stress point 5 sign-flip station 2
            ScalerConstraint(-10.0, 10.0),                                                                                             # [85] compressive stress point 6 sign-flip station 0 (G1[69:72])
            ScalerConstraint(-50.0, 50.0),                                                                                             # [86] compressive stress point 6 sign-flip station 1
            ScalerConstraint(-50.0, 50.0),                                                                                             # [87] compressive stress point 6 sign-flip station 2
            ScalerConstraint(-1.0, 1.0),                                                                                               # [88]  h_spar margin station constraint 0 (alpha1+alpha3-0.5)
            ScalerConstraint(-1.0, 1.0),                                                                                               # [89]  h_spar margin station constraint 1
            ScalerConstraint(-1.0, 1.0),                                                                                               # [90]  h_spar margin station constraint 2
            ScalerConstraint(-5.0, 5.0),                                                                                               # [91]  ts1 lower gauge station constraint 0 (0.1/12 - ts1)
            ScalerConstraint(-2.0, 2.0),                                                                                               # [92]  ts1 lower gauge station constraint 1
            ScalerConstraint(-2.0, 2.0),                                                                                               # [93]  ts1 lower gauge station constraint 2
            ScalerConstraint(-2.0, 2.0),                                                                                               # [94]  ts1 upper gauge station constraint 0 (ts1 - 9/12)
            ScalerConstraint(-1.0, 1.0),                                                                                               # [95]  ts1 upper gauge station constraint 1
            ScalerConstraint(-0.75, 0.75),                                                                                             # [96]  ts1 upper gauge station constraint 2
            ScalerConstraint(-3.0, 3.00),                                                                                              # [97]  ts3 lower gauge station constraint 0 (0.1/12 - ts3)
            ScalerConstraint(-2.0, 2.0),                                                                                               # [98]  ts3 lower gauge station constraint 1
            ScalerConstraint(-2.0, 2.0),                                                                                               # [99]  ts3 lower gauge station constraint 2
            ScalerConstraint(-2.0, 2.0),                                                                                               # [100] ts3 upper gauge station constraint 0 (ts3 - 9/12)
            ScalerConstraint(-2.0, 2.0),                                                                                               # [101] ts3 upper gauge station constraint 1
            ScalerConstraint(-0.75, 0.75),                                                                                             # [102] ts3 upper gauge station constraint 2
            ScalerConstraint(-2.0, 2.0),                                                                                               # [103] t1 lower gauge station constraint 0 (0.1/12 - t1)
            ScalerConstraint(-2.0, 2.0),                                                                                               # [104] t1 lower gauge station constraint 1
            ScalerConstraint(-2.0, 2.0),                                                                                               # [105] t1 lower gauge station constraint 2
            ScalerConstraint(-2.0, 2.0),                                                                                               # [106] t1 upper gauge station constraint 0 (t1 - 4/12)
            ScalerConstraint(-2.0, 2.0),                                                                                               # [107] t1 upper gauge station constraint 1
            ScalerConstraint(-2.0, 2.0),                                                                                               # [108] t1 upper gauge station constraint 2
            ScalerConstraint(-1.0, 1.0),                                                                                               # [109] t2 lower gauge station constraint 0 (0.1/12 - t2)
            ScalerConstraint(-1.0, 1.0),                                                                                               # [110] t2 lower gauge station constraint 1
            ScalerConstraint(-1.0, 1.0),                                                                                               # [111] t2 lower gauge station constraint 2
            ScalerConstraint(-1.0, 1.0),                                                                                               # [112] t2 upper gauge station constraint 0 (t2 - 4/12)
            ScalerConstraint(-1.0, 1.0),                                                                                               # [113] t2 upper gauge station constraint 1
            ScalerConstraint(-1.0, 1.0),                                                                                               # [114] t2 upper gauge station constraint 2
            ScalerConstraint(-2.0, 2.0),                                                                                               # [115] t3 lower gauge station constraint 0 (0.1/12 - t3)
            ScalerConstraint(-2.0, 2.0),                                                                                               # [116] t3 lower gauge station constraint 1
            ScalerConstraint(-2.0, 2.0),                                                                                               # [117] t3 lower gauge station constraint 2
            ScalerConstraint(-2.0, 2.0),                                                                                               # [118] t3 upper gauge station constraint 0 (t3 - 4/12)
            ScalerConstraint(-1.0, 1.0),                                                                                               # [119] t3 upper gauge station constraint 1
            ScalerConstraint(-1.0, 1.0),                                                                                               # [120] t3 upper gauge station constraint 2
            copy.deepcopy(self._subsystems[0].get_Scalers()[3]),                                                                       # [121] mapped response corresponding to structural_weight [lb]
            copy.deepcopy(self._subsystems[0].get_Scalers()[4]),                                                                       # [122] mapped response corresponding to fuel_weight [lb]
            copy.deepcopy(self._subsystems[2].get_Scalers()[11])                                                                       # [123] mapped response corresponding to wing_twist (delta(L)/q effective area [ft^2])
        ])

        # ── Step 6: Design variable initialization & reference state ──────
        # Set granularity (step sizes), initial values, and (optionally)
        # reference values / coupling metadata for each subsystem's design
        # variables. Values are scaled via .transform().
        # Order: local design variables,
        #        shared design variables,
        #        additional design variables(as a result of decomposition)
        
        self._subsystems[0].set_DesignVariables_Granularity([0.0] * 5)
        self._subsystems[0].set_DesignVariables([self._subsystems[0].get_Scalers()[0].transform(2.0),                  # 0d[0] specific_fuel_consumption [1/hr]
                                                 self._subsystems[0].get_Scalers()[1].transform(15000.0),              # 0d[1] engine_weight [lb]
                                                 self._subsystems[0].get_Scalers()[2].transform(5.00),                 # 0d[2] lift_to_drag_ratio [-]
                                                 self._subsystems[0].get_Scalers()[3].transform(25000.0),              # 0d[3] structural_weight [lb]
                                                 self._subsystems[0].get_Scalers()[4].transform(25000.0)])             # 0d[4] fuel_weight [lb]
        
        # self._subsystems[0].set_ReferenceDesignVariables([self._subsystems[1].get_Scalers()[0].transform(...),
        #                                                   self._subsystems[1].get_Scalers()[1].transform(...)
        #                                                   ])
        self._subsystems[0].set_ReferenceLocalObjectiveValue(self._subsystems[0].get_Scalers()[5].transform(34300.0))
        self._subsystems[0].set_ReferenceLocalObjectiveValueUnscaled(34300.0)
        # self._subsystems[0].set_DesignVariablesInfluenceAnyCouplingBool([False, False, False, True, True])
        # self._subsystems[0].set_NeighborID_for_additional_dv([None, None, None, ["1"], ["2"]])
        
        self._subsystems[1].set_DesignVariables_Granularity([0.0] * 2)
        self._subsystems[1].set_DesignVariables([self._subsystems[1].get_Scalers()[0].transform(0.60),                   # 1d[0] throttle
                                                 self._subsystems[1].get_Scalers()[1].transform(40000.0)])               # 1d[1] drag
        
        self._subsystems[1].set_ReferenceLocalObjectiveValue(None)
        self._subsystems[1].set_ReferenceLocalObjectiveValueUnscaled(None)
                                                 
        # self._subsystems[1].set_ReferenceDesignVariables([self._subsystems[1].get_Scalers()[0].transform(...),
        #                                                   self._subsystems[1].get_Scalers()[1].transform(...)
        #                                                  ])
        # self._subsystems[1].set_ReferenceLocalObjectiveValue(self._subsystems[1].get_Scalers()[...].transform(...))
        # self._subsystems[1].set_ReferenceLocalObjectiveValueUnscaled(...)
        # self._subsystems[1].set_DesignVariablesInfluenceAnyCouplingBool([True, True, True, True])
        # self._subsystems[1].set_NeighborID_for_additional_dv([None, None, None, None])
                
        self._subsystems[2].set_DesignVariables_Granularity([0.0] * 12)
        self._subsystems[2].set_DesignVariables([self._subsystems[2].get_Scalers()[0].transform(45.0),                    # 2d[0] tail_sweep_angle [deg]
                                                 self._subsystems[2].get_Scalers()[1].transform(0.150),                   # 2d[1] wing_moment_arm [ft]
                                                 self._subsystems[2].get_Scalers()[2].transform(1.50),                    # 2d[2] tail_moment_arm [ft]
                                                 self._subsystems[2].get_Scalers()[3].transform(0.050),                   # 2d[3] thickness_to_chord_ratio [-]
                                                 self._subsystems[2].get_Scalers()[4].transform(60.0),                    # 2d[4] wing_sweep_angle [deg]
                                                 self._subsystems[2].get_Scalers()[5].transform(3.00),                    # 2d[5] wing_aspect_ratio [-]
                                                 self._subsystems[2].get_Scalers()[6].transform(500.0),                   # 2d[6] wing_surface_area [ft^2]
                                                 self._subsystems[2].get_Scalers()[7].transform(5.5),                     # 2d[7] tail_aspect_ratio [-]
                                                 self._subsystems[2].get_Scalers()[8].transform(100.0),                   # 2d[8] tail_surface_area [ft^2]
                                                 self._subsystems[2].get_Scalers()[9].transform(25000.0),                 # 2d[9] total_weight [lb]
                                                 self._subsystems[2].get_Scalers()[10].transform(1.0),                    # 2d[10] engine_scale_factor [-]
                                                 self._subsystems[2].get_Scalers()[11].transform(10.0)                    # 2d[11] wing_twist [deg]
                                                 ])
        
        self._subsystems[2].set_ReferenceLocalObjectiveValue(None)
        self._subsystems[2].set_ReferenceLocalObjectiveValueUnscaled(None)
        
        # self._subsystems[2].set_ReferenceDesignVariables([self._subsystems[2].get_Scalers()[0].transform(...),
        #                                                   self._subsystems[2].get_Scalers()[1].transform(...)
        #                                                   ])
        # self._subsystems[2].set_ReferenceLocalObjectiveValue(self._subsystems[2].get_Scalers()[...].transform(...))
        # self._subsystems[2].set_ReferenceLocalObjectiveValueUnscaled(...)
        # self._subsystems[2].set_DesignVariablesInfluenceAnyCouplingBool([True, True, True, True])
        # self._subsystems[2].set_NeighborID_for_additional_dv([None, None, None, None])
        
        self._subsystems[3].set_DesignVariables_Granularity([0.0] * 26)
        # Initial design (reformulation): the nominal skin ratio rho = t/ts = 3.0/6.0 = 0.5 and the
        # web sandwich ts2 = 6.0 in are carried over directly from the original nominal (t=3, ts=6 in).
        # The depth fractions are set to alpha1 = alpha3 = 0.2 (rather than the exact image of the old
        # ts=6 in nominal, which is planform-dependent and exceeds 0.5 at the small-chord tip station —
        # i.e. the old nominal was h_spar<0 infeasible there). alpha=0.2 gives h_spar = 0.6*D > 0 at
        # every station, so the starting point is strictly feasible w.r.t. the h_spar margin.
        self._subsystems[3].set_DesignVariables([self._subsystems[3].get_Scalers()[0].transform(0.30),       # 3d[0] taper ratio [-]
                                                 self._subsystems[3].get_Scalers()[1].transform(0.20),       # 3d[1] alpha1 station 0 [-]
                                                 self._subsystems[3].get_Scalers()[2].transform(0.20),       # 3d[2] alpha1 station 1 [-]
                                                 self._subsystems[3].get_Scalers()[3].transform(0.20),       # 3d[3] alpha1 station 2 [-]
                                                 self._subsystems[3].get_Scalers()[4].transform(0.20),       # 3d[4] alpha3 station 0 [-]
                                                 self._subsystems[3].get_Scalers()[5].transform(0.20),       # 3d[5] alpha3 station 1 [-]
                                                 self._subsystems[3].get_Scalers()[6].transform(0.20),       # 3d[6] alpha3 station 2 [-]
                                                 self._subsystems[3].get_Scalers()[7].transform(6.00),       # 3d[7] ts2 station 0 (web sandwich) [in]
                                                 self._subsystems[3].get_Scalers()[8].transform(6.00),       # 3d[8] ts2 station 1 [in]
                                                 self._subsystems[3].get_Scalers()[9].transform(6.00),       # 3d[9] ts2 station 2 [in]
                                                 self._subsystems[3].get_Scalers()[10].transform(0.50),      # 3d[10] rho1 station 0 [-]
                                                 self._subsystems[3].get_Scalers()[11].transform(0.50),      # 3d[11] rho1 station 1 [-]
                                                 self._subsystems[3].get_Scalers()[12].transform(0.50),      # 3d[12] rho1 station 2 [-]
                                                 self._subsystems[3].get_Scalers()[13].transform(0.50),      # 3d[13] rho2 station 0 [-]
                                                 self._subsystems[3].get_Scalers()[14].transform(0.50),      # 3d[14] rho2 station 1 [-]
                                                 self._subsystems[3].get_Scalers()[15].transform(0.50),      # 3d[15] rho2 station 2 [-]
                                                 self._subsystems[3].get_Scalers()[16].transform(0.50),      # 3d[16] rho3 station 0 [-]
                                                 self._subsystems[3].get_Scalers()[17].transform(0.50),      # 3d[17] rho3 station 1 [-]
                                                 self._subsystems[3].get_Scalers()[18].transform(0.50),      # 3d[18] rho3 station 2 [-]
                                                 self._subsystems[3].get_Scalers()[19].transform(0.050),     # 3d[19] thickness_to_chord_ratio [-]
                                                 self._subsystems[3].get_Scalers()[20].transform(60.0),      # 3d[20] wing_sweep_angle [deg]
                                                 self._subsystems[3].get_Scalers()[21].transform(3.00),      # 3d[21] wing_aspect_ratio [-]
                                                 self._subsystems[3].get_Scalers()[22].transform(500.0),     # 3d[22] wing_surface_area [ft^2]
                                                 self._subsystems[3].get_Scalers()[23].transform(5.5),       # 3d[23] tail_aspect_ratio [-]
                                                 self._subsystems[3].get_Scalers()[24].transform(100.0),     # 3d[24] tail_surface_area [ft^2]
                                                 self._subsystems[3].get_Scalers()[25].transform(25000.0)    # 3d[25] lift [lb]
                                                 ])
        
        self._subsystems[3].set_ReferenceLocalObjectiveValue(None)
        self._subsystems[3].set_ReferenceLocalObjectiveValueUnscaled(None)
        
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

        # ── circle 0 - 1 ─────────────────────────────────────────────────────────
        # [specific_fuel_consumption [1/hr], engine_weight [lb]]: owned by subsystem 0 (0d[0] => scaler[0], 0d[1] => scaler[1]), mapped by subsystem 1 (scaler[4], scaler[5])
        self._subsystems[0].set_CouplingVariables("1",
                                                  [self._subsystems[0].get_Scalers()[0].transform(2.0),  
                                                   self._subsystems[0].get_Scalers()[1].transform(15000.0)], 
                                                  [2.0,
                                                   15000.0])        
        self._subsystems[0].set_Indices_CouplingVariables_in_DesignVariables("1", [0, 1])        
        self._subsystems[0].set_Copy_MappedResponseVariables("1", [self._subsystems[1].get_Scalers()[6].transform(2.0),
                                                                  self._subsystems[1].get_Scalers()[7].transform(15000.0)])  
        
        
        # ── circle 1 - 0 (reciprocal of circle 0 - 1) ────────────────────────────
        # [specific_fuel_consumption [1/hr], engine_weight [lb]]: subsystem 1 maps them (scaler[4], scaler[5])
        self._subsystems[1].set_MappedResponseVariables("0",
                                                        [self._subsystems[1].get_Scalers()[6].transform(2.0), 
                                                         self._subsystems[1].get_Scalers()[7].transform(15000.0)], 
                                                        [2.0,
                                                         15000.0])        
        self._subsystems[1].set_Copy_CouplingVariables("0", [self._subsystems[0].get_Scalers()[0].transform(2.0),
                                                            self._subsystems[0].get_Scalers()[1].transform(15000.0)]) 
        

        # ── circle 0 - 2 ─────────────────────────────────────────────────────────
        # lift_to_drag_ratio [-]: owned by subsystem 0 (0d[2] => scaler[2]), mapped by subsystem 2 (scaler[15])
        self._subsystems[0].set_CouplingVariables("2", [self._subsystems[0].get_Scalers()[2].transform(5.00)], [5.00])  
        self._subsystems[0].set_Indices_CouplingVariables_in_DesignVariables("2", [2])
        self._subsystems[0].set_Copy_MappedResponseVariables("2", [self._subsystems[2].get_Scalers()[17].transform(5.00)])  

        # total_weight [lb]: owned by subsystem 2 (2d[9] => scaler[9]), mapped by subsystem 0 (scaler[8])
        self._subsystems[0].set_MappedResponseVariables("2", [self._subsystems[0].get_Scalers()[8].transform(25000.0)], [25000.0]) 
        self._subsystems[0].set_Copy_CouplingVariables("2", [self._subsystems[2].get_Scalers()[9].transform(25000.0)])  
        

        # ── circle 2 - 0 (reciprocal of circle 0 - 2) ────────────────────────────
        # lift_to_drag_ratio [-]: subsystem 2 maps it (scaler[15]), owned by subsystem 0 (0d[2] => scaler[2])
        self._subsystems[2].set_MappedResponseVariables("0", [self._subsystems[2].get_Scalers()[17].transform(5.00)], [5.00]) 
        self._subsystems[2].set_Copy_CouplingVariables("0", [self._subsystems[0].get_Scalers()[2].transform(5.00)])  

        # total_weight [lb]: owned by subsystem 2 (2d[9] => scaler[9]), mapped by subsystem 0 (scaler[8])
        self._subsystems[2].set_CouplingVariables("0", [self._subsystems[2].get_Scalers()[9].transform(25000.0)], [25000.0])  
        self._subsystems[2].set_Indices_CouplingVariables_in_DesignVariables("0", [9])
        self._subsystems[2].set_Copy_MappedResponseVariables("0", [self._subsystems[0].get_Scalers()[8].transform(25000.0)])
        
        
        # ── circle 0 - 3 ──────────────────────────────────────────────────────────
        # [structural_weight [lb], fuel_weight [lb]]: owned by subsystem 0 (0d[3] => scaler[3], 0d[4] => scaler[4]), mapped by subsystem 3 (scaler[100], scaler[101])
        self._subsystems[0].set_CouplingVariables("3",
                                                  [self._subsystems[0].get_Scalers()[3].transform(25000.0),
                                                   self._subsystems[0].get_Scalers()[4].transform(25000.0)],  
                                                  [25000.0,
                                                   25000.0])

        self._subsystems[0].set_Indices_CouplingVariables_in_DesignVariables("3", [3, 4])

        self._subsystems[0].set_Copy_MappedResponseVariables("3", [self._subsystems[3].get_Scalers()[121].transform(25000.0),
                                                                  self._subsystems[3].get_Scalers()[122].transform(25000.0)])
        

        # ── circle 3 - 0 (reciprocal of circle 0 - 3) ────────────────────────────
        # [structural_weight [lb], fuel_weight [lb]]: subsystem 3 maps them (scaler[100], scaler[101]), owned by subsystem 0 (0d[3] => scaler[3], 0d[4] => scaler[4])
        self._subsystems[3].set_MappedResponseVariables("0",
                                                        [self._subsystems[3].get_Scalers()[121].transform(25000.0),
                                                         self._subsystems[3].get_Scalers()[122].transform(25000.0)],
                                                        [25000.0,
                                                         25000.0])

        self._subsystems[3].set_Copy_CouplingVariables("0", [self._subsystems[0].get_Scalers()[3].transform(25000.0),
                                                            self._subsystems[0].get_Scalers()[4].transform(25000.0)])     
        
        # ── circle 1 - 2 ─────────────────────────────────────────────────────────
        # drag [lb]: owned by subsystem 1 (1d[1] => scaler[1]), mapped by subsystem 2 (scaler[16])
        self._subsystems[1].set_CouplingVariables("2", [self._subsystems[1].get_Scalers()[1].transform(40000.0)], [40000.0])
        self._subsystems[1].set_Indices_CouplingVariables_in_DesignVariables("2", [1])
        self._subsystems[1].set_Copy_MappedResponseVariables("2", [self._subsystems[2].get_Scalers()[18].transform(40000.0)])

        # engine_scale_factor [-]: owned by subsystem 2 (2d[10] => scaler[10]), mapped by subsystem 1 (scaler[8])
        self._subsystems[1].set_MappedResponseVariables("2", [self._subsystems[1].get_Scalers()[8].transform(1.0)], [1.0])
        self._subsystems[1].set_Copy_CouplingVariables("2", [self._subsystems[2].get_Scalers()[10].transform(1.0)])

        # ── circle 2 - 1 (reciprocal of circle 1 - 2) ────────────────────────────
        # engine_scale_factor [-]: owned by subsystem 2 (2d[10] => scaler[10]), mapped by subsystem 1 (scaler[8])
        self._subsystems[2].set_CouplingVariables("1", [self._subsystems[2].get_Scalers()[10].transform(1.0)], [1.0])  
        self._subsystems[2].set_Indices_CouplingVariables_in_DesignVariables("1", [10])
        self._subsystems[2].set_Copy_MappedResponseVariables("1", [self._subsystems[1].get_Scalers()[8].transform(1.0)])

        # drag [lb]: owned by subsystem 1 (1d[1] => scaler[1]), mapped by subsystem 2 (scaler[18])
        self._subsystems[2].set_MappedResponseVariables("1", [self._subsystems[2].get_Scalers()[18].transform(40000.0)], [40000.0])  
        self._subsystems[2].set_Copy_CouplingVariables("1", [self._subsystems[1].get_Scalers()[1].transform(40000.0)])

        # ── circle 2 - 3 ─────────────────────────────────────────────────────────
        # wing_twist: owned by subsystem 2 (2d[11] => scaler[11]), mapped by subsystem 3 (scaler[102])
        self._subsystems[2].set_CouplingVariables("3", [self._subsystems[2].get_Scalers()[11].transform(10.0)], [10.0])  
        self._subsystems[2].set_Indices_CouplingVariables_in_DesignVariables("3", [11])
        self._subsystems[2].set_Copy_MappedResponseVariables("3", [self._subsystems[3].get_Scalers()[123].transform(10.0)])

        # lift: owned by subsystem 3 (3d[25] => scaler[25]), mapped by subsystem 2 (scaler[19])
        self._subsystems[2].set_MappedResponseVariables("3", [self._subsystems[2].get_Scalers()[19].transform(25000.0)], [25000.0])  
        self._subsystems[2].set_Copy_CouplingVariables("3", [self._subsystems[3].get_Scalers()[25].transform(25000.0)])

        # [thickness_to_chord_ratio, wing_sweep_angle, wing_aspect_ratio, wing_surface_area, tail_aspect_ratio, tail_surface_area]:
        # owned by subsystem 2 (2d[3] => scaler[3], 2d[4] => scaler[4], 2d[5] => scaler[5], 2d[6] => scaler[6], 2d[7] => scaler[7], 2d[8] => scaler[8])
        # targets in subsystem 3 (3d[19] => scaler[19], 3d[20] => scaler[20], 3d[21] => scaler[21], 3d[22] => scaler[22], 3d[23] => scaler[23], 3d[24] => scaler[24])
        self._subsystems[2].set_SharedDesignVariables("3",
                                                      [self._subsystems[2].get_Scalers()[3].transform(0.050),
                                                       self._subsystems[2].get_Scalers()[4].transform(60.0),
                                                       self._subsystems[2].get_Scalers()[5].transform(3.00),
                                                       self._subsystems[2].get_Scalers()[6].transform(500.0),
                                                       self._subsystems[2].get_Scalers()[7].transform(5.5),
                                                       self._subsystems[2].get_Scalers()[8].transform(100.0)],
                                                      [0.050, 60.0, 3.00, 500.0, 5.5, 100.0])
        self._subsystems[2].set_Indices_SharedDesignVariables_in_DesignVariables("3", [3, 4, 5, 6, 7, 8])

        self._subsystems[2].set_Copy_TargetSharedDesignVariables("3",
                                                          [self._subsystems[3].get_Scalers()[19].transform(0.050),
                                                           self._subsystems[3].get_Scalers()[20].transform(60.0),
                                                           self._subsystems[3].get_Scalers()[21].transform(3.00),
                                                           self._subsystems[3].get_Scalers()[22].transform(500.0),
                                                           self._subsystems[3].get_Scalers()[23].transform(5.5),
                                                           self._subsystems[3].get_Scalers()[24].transform(100.0)])
        
        # ── circle 3 - 2 (reciprocal of circle 2 - 3) ────────────────────────────
        # lift: owned by subsystem 3 (3d[25] => scaler[25]), mapped by subsystem 2 (scaler[19])
        self._subsystems[3].set_CouplingVariables("2", [self._subsystems[3].get_Scalers()[25].transform(25000.0)], [25000.0])  
        self._subsystems[3].set_Indices_CouplingVariables_in_DesignVariables("2", [25])
        self._subsystems[3].set_Copy_MappedResponseVariables("2", [self._subsystems[2].get_Scalers()[19].transform(25000.0)])

        # wing_twist: owned by subsystem 2 (2d[11] => scaler[11]), mapped by subsystem 3 (scaler[102])
        self._subsystems[3].set_MappedResponseVariables("2", [self._subsystems[3].get_Scalers()[123].transform(10.0)], [10.0])  
        self._subsystems[3].set_Copy_CouplingVariables("2", [self._subsystems[2].get_Scalers()[11].transform(10.0)])

        # [thickness_to_chord_ratio, wing_sweep_angle, wing_aspect_ratio, wing_surface_area, tail_aspect_ratio, tail_surface_area]:
        self._subsystems[3].set_TargetSharedDesignVariables("2",
                                                            [self._subsystems[3].get_Scalers()[19].transform(0.050),
                                                             self._subsystems[3].get_Scalers()[20].transform(60.0),
                                                             self._subsystems[3].get_Scalers()[21].transform(3.00),
                                                             self._subsystems[3].get_Scalers()[22].transform(500.0),
                                                             self._subsystems[3].get_Scalers()[23].transform(5.5),
                                                             self._subsystems[3].get_Scalers()[24].transform(100.0)],
                                                            [0.050, 60.0, 3.00, 500.0, 5.5, 100.0])
        self._subsystems[3].set_Indices_TargetSharedDesignVariables_in_DesignVariables("2", [19, 20, 21, 22, 23, 24])

        self._subsystems[3].set_Copy_SharedDesignVariables("2",
                                                           [self._subsystems[2].get_Scalers()[3].transform(0.050),
                                                            self._subsystems[2].get_Scalers()[4].transform(60.0),
                                                            self._subsystems[2].get_Scalers()[5].transform(3.00),
                                                            self._subsystems[2].get_Scalers()[6].transform(500.0),
                                                            self._subsystems[2].get_Scalers()[7].transform(5.5),
                                                            self._subsystems[2].get_Scalers()[8].transform(100.0)])
        
```
