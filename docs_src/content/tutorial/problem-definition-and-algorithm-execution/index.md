---
title: Problem Definition and Algorithm Execution
---

# Problem Definition and Algorithm Execution

This section covers how to define and solve distributed design optimization problems with the abbr:DDO framework.
A step-by-step guide is illustrated for the [SSBJ](../../examples/SSBJ/index.md) Example below.

## 1. Formulation of the distributed design optimization problem

The [Distributed Design Approach](../../distributed-optimization-for-multidisciplinary-design/distributed-design-approach.md) leads to a specific distributed design optimization problem formulation. Therein, each subsystem optimization problem is defined with the following notation: local design variables ${}^{i}$sym:x, shared design variables ${}^{i}_{j}$sym:z, coupling variables ${}^{j}_{i}$sym:h, local response function ${}^{i}$sym:r, local inequality constraints ${}^{i}$sym:v_g, local equality constraints ${}^{i}$sym:v_h, and local objective function ${}^{i}$sym:v_f. Furthermore, two neighboring subsystems may be coupled through shared design variables ${}^{i}_{j}$sym:z and/or coupling variables ${}^{j}_{i}$sym:h, where ${}^{j}_{i}h := {}^{j}_{i}H\left({}^{j}r\right)$.

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, the distributed design optimization problem formulation is shown below:

<iframe src="../../examples/SSBJ/SSBJ_model.drawio.html" width="100%" height="500" style="border:none;" allowfullscreen></iframe>

## 2. Creation of folder holding all use-case specific files

With the [`userfiles/NewUseCase_Template/`](../../api/userfiles/NewUseCase_Template/index.md) as reference, a new folder named after the use-case is created under [`userfiles/`](../../api/userfiles/index.md).
It has the following structure:

<div class="file-tree" style="white-space: pre; line-height: 1.8;" markdown>
<span style="font-family: monospace;">:material-folder:</span> [`userfiles/NewUseCase_Template/`](../../api/userfiles/NewUseCase_Template/index.md)
<span style="font-family: monospace;">├──</span> <span style="font-family: monospace;">:material-folder:</span> [`subsystem0/`](../../api/userfiles/NewUseCase_Template/subsystem0/index.md)
<span style="font-family: monospace;">│   ├──</span> <span style="font-family: monospace;">:material-language-python:</span> `__init__.py`
<span style="font-family: monospace;">│   ├──</span> <span style="font-family: monospace;">:material-language-python:</span> [`Analysis0.py`](../../api/userfiles/NewUseCase_Template/subsystem0/Analysis0.md) > implements ${}^{0}$sym:r$({}^{0}$sym:d$)$
<span style="font-family: monospace;">│   ├──</span> <span style="font-family: monospace;">:material-language-python:</span> [`LocalConstraints0.py`](../../api/userfiles/NewUseCase_Template/subsystem0/LocalConstraints0.md) > implements ${}^{0}$sym:v_g and ${}^{0}$sym:v_h
<span style="font-family: monospace;">│   ├──</span> <span style="font-family: monospace;">:material-language-python:</span> [`LocalObjective0.py`](../../api/userfiles/NewUseCase_Template/subsystem0/LocalObjective0.md) > implements ${}^{0}$sym:v_f
<span style="font-family: monospace;">│   └──</span> <span style="font-family: monospace;">:material-language-python:</span> [`Optimization0.py`](../../api/userfiles/NewUseCase_Template/subsystem0/Optimization0.md) > selects optimization algorithm (with hyperparameters)
<span style="font-family: monospace;">├──</span> <span style="font-family: monospace;">:material-folder:</span> [`subsystem1/`](../../api/userfiles/NewUseCase_Template/subsystem1/index.md)
<span style="font-family: monospace;">│   ├──</span> <span style="font-family: monospace;">:material-language-python:</span> `__init__.py`
<span style="font-family: monospace;">│   ├──</span> <span style="font-family: monospace;">:material-language-python:</span> [`Analysis1.py`](../../api/userfiles/NewUseCase_Template/subsystem1/Analysis1.md) > implements ${}^{1}$sym:r$({}^{1}$sym:d$)$
<span style="font-family: monospace;">│   ├──</span> <span style="font-family: monospace;">:material-language-python:</span> [`LocalConstraints1.py`](../../api/userfiles/NewUseCase_Template/subsystem1/LocalConstraints1.md) > implements ${}^{1}$sym:v_g and ${}^{1}$sym:v_h
<span style="font-family: monospace;">│   ├──</span> <span style="font-family: monospace;">:material-language-python:</span> [`LocalObjective1.py`](../../api/userfiles/NewUseCase_Template/subsystem1/LocalObjective1.md) > implements ${}^{1}$sym:v_f
<span style="font-family: monospace;">│   └──</span> <span style="font-family: monospace;">:material-language-python:</span> [`Optimization1.py`](../../api/userfiles/NewUseCase_Template/subsystem1/Optimization1.md) > selects optimization algorithm (with hyperparameters)
<span style="font-family: monospace;">├──</span> <span style="font-family: monospace;">:material-folder:</span> [`subsystem2/`](../../api/userfiles/NewUseCase_Template/subsystem2/index.md)
<span style="font-family: monospace;">├──</span> <span style="font-family: monospace;">:material-language-python:</span> [`InputFile.py`](../../api/userfiles/NewUseCase_Template/InputFile.md) > selects coordination algorithm, defines subsystem coupling topology,
<span style="font-family: monospace;">│</span>                                       scaling variables, and design space
<span style="font-family: monospace;">├──</span> <span style="font-family: monospace;">:material-language-python:</span> [`main.py`](../../api/userfiles/NewUseCase_Template/main.md) > run the framework for defined `InputFile.py`
<span style="font-family: monospace;">└──</span> <span style="font-family: monospace;">:material-file-document:</span> `SOURCE.txt` > holds relevant use-case specific information
</div>

The content of each of these files is detailed in the following steps. The `__init__.py` files do not need to be defined by the user as they are generated automatically when executing the coordination method in [Step 8.](../problem-definition-and-algorithm-execution/index.md#8-executing-the-coordination-method). Constants used throughout the use-case may be implemented in a dedicated `constants.py` file within the `userfiles/NewUseCase_Template/` folder and imported from there.

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, the folder holding all use-case specific files is under [`userfiles/SSBJ/`](../../api/userfiles/SSBJ/index.md).

## 3. Defining the main.py and InputFile.py

The newly created `main.py` needs to import and instantiate class `InputFile` defined in `InputFile.py`. This is the only use-case specific modification for `main.py`.
The implementation of `InputFile.__init__()` collects all information necessary to set-up and solve a distributed design optimization problem using the DistributedDesignOptimizer framework. 

First, the attribute `_name` of `InputFile` is set. This name may describe the use-case along with some coordination method specific hyperparameter or other information deemed important by the user. The framework logs data under this name in the use-case's `historyfiles/` folder (i.e. `userfiles/<usecasename>/historyfiles/`) for subsequent post-processing. Further details in [Data Logging](../../framework-architecture/data-logging.md) and [Tutorial > Processing](../processing/index.md).
Next, the attribute `_coordinationmethod` of `InputFile` is set by initializing a coordination method of choice. Further details on available coordination methods and their associated options and hyperparameters in [ALC Pseudocode-to-Code Traceability](../../framework-architecture/pseudocode-traceability/augmented-lagrangian-coordination-pseudocode-traceability.md), [ALADIN Pseudocode-to-Code Traceability](../../framework-architecture/pseudocode-traceability/aladin-pseudocode-traceability.md), [Consensus ALC Pseudocode-to-Code Traceability](../../framework-architecture/pseudocode-traceability/consensus-augmented-lagrangian-coordination-pseudocode-traceability.md).

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, this reads as follows:

<div class="collapsible-code" markdown>

```python
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
        
        # ── Step 1: Use-case name and coordination method ───────────────
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
        #                                                            iterationscheme=SequentialForward())
        #self._coordinationmethod: CoordinationMethodInterface = LC(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1E-5),
        #                                                            convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-4),
        #                                                            updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_SubgradientMultipliers(
        #                                                                beta=3.5,
        #                                                                initialmultiplier=0.0),
        #                                                            iterationscheme=SequentialForward())        
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
        # self._coordinationmethod: CoordinationMethodInterface = ALCSigma(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1E-5),
        #                                                                  convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-4),
        #                                                                  updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AugLagSigma(
        #                                                                      beta=1.3,
        #                                                                      gamma=0.5,
        #                                                                      initialweight=0.01,
        #                                                                      initialmultiplier=0.0,
        #                                                                      sigma_active="1",
        #                                                                      initialsigma=1.0),
        #                                                                  iterationscheme=SequentialForward())
        # self._coordinationmethod: CoordinationMethodInterface = ALCTransformation(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1E-5),
        #                                                                           convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-4),
        #                                                                           updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights(
        #                                                                               beta=1.3,
        #                                                                               gamma=0.5,
        #                                                                               initialweight=0.01,
        #                                                                               initialmultiplier=0.0),
        #                                                                           iterationscheme=SequentialForward(),
        #                                                                           transformationfunction="pow",
        #                                                                           ppower=3)
        # self._coordinationmethod: CoordinationMethodInterface = ALCNeighborhoodSearch(convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(tolerancetotalobjective=1E-5),
        #                                                                               convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(toleranceconsistency=1E-4),
        #                                                                               updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AugLagNeighborhoodSearch(
        #                                                                                   beta=1.3,
        #                                                                                   gamma=0.5,
        #                                                                                   initialweight=0.01,
        #                                                                                   initialmultiplier=0.0),
        #                                                                               iterationscheme=SequentialForward())
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
```

</div>

Next, the subsystem topology is defined and each subsystem's `Analysis<id>`, `LocalObjective<id>`, `LocalConstraints<id>` and `Optimization<id>` is instantiated. The specific implementation of these classes is detailed later in this tutorial.

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, this reads as follows:

<div class="collapsible-code" markdown>

```python
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
```

</div>

The upper and lower bounds for each subsystem design variable sym:d constitute the design space sym:\mathcal{D} and are set next. Hereby, the design variables consist of local, shared and additional design variables following the decomposition procedure introduced in [Unified Algorithmic Structure](../../distributed-optimization-for-multidisciplinary-design/unified-algorithmic-structure.md).

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, this reads as follows:

<div class="collapsible-code" markdown>

```python
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
```

</div>

In order to render the distributed design optimization algorithms of this framework insensitive towards different orders of magnitudes among quantities, 
a comprehensive scaling approach is used. This ensures that 

- design variables $^{i}$sym:d $\quad\forall{}i\in$sym:M
- local objective $^{i}$sym:v_f values $\quad\forall{}i\in$sym:M
- mapped responses $^{i}_{j}$sym:H $\quad\forall{}j\in{}^{i}$sym:N$,i\in$sym:M
- coupling variables $^{i}_{j}$sym:h $\quad\forall{}j\in{}^{i}$sym:N$,i\in$sym:M
- shared design variables $^{i}_{j}$sym:z $\quad\forall{}j\in{}^{i}$sym:N$,i\in$sym:M
- target shared design variables $^{i}_{j}$sym:z_{t} $\quad\forall{}j\in{}^{i}$sym:N$,i\in$sym:M

are scaled to within [0; 1], and all

- local equality constraint $^{i}$sym:v_h values $\quad\forall{}i\in$sym:M
- local inequality constraint $^{i}$sym:v_g values $\quad\forall{}i\in$sym:M

are scaled to [-0.5; 0.5] symmetrically around 0.0.

Each of the above scalar quantities is assigned either a [`ScalerZeroOne`](../../api/Distributed_Design_Optimizer/subsystem/tools/ScalerZeroOne.md) or [`ScalerConstraint`](../../api/Distributed_Design_Optimizer/subsystem/tools/ScalerConstraint.md) object which transforms between its scaled and unscaled domain. However, to use these scaler objects, they need to be defined and assigned to each subsystem first. Even if a subsystem does not have a local equality constraint or local inequality constraint or local objective (as indicated by `None` later in [Step 5.](index.md#5-defining-the-localconstraintspy) and [Step 6.](index.md#6-defining-the-localobjectivepy)), a single corresponding scaler object (serving as a placeholder) needs to be assigned.

Each scaler object is initialized with upper and lower bounds (which are scaled to 0 & 1 in case of a [`ScalerZeroOne`](../../api/Distributed_Design_Optimizer/subsystem/tools/ScalerZeroOne.md) or -0.5 & 0.5 in case of a [`ScalerConstraint`](../../api/Distributed_Design_Optimizer/subsystem/tools/ScalerConstraint.md)). These bounds should describe the realizable value range of the associated quantity in the unscaled domain for the given design space sym:\mathcal{D} (which was defined above) as tight as possible. The realizable value range of some quantity may be determined

- using the previously defined design space sym:\mathcal{D}, or
- using domain knowledge of the use-case at hand, or
- following an iterative trial-and-error approach by comparing each scaler object's attributes
    - `_smallest_observed_value_unscaled`
    - `_largest_observed_value_unscaled`
  with their currently defined
    - `_lower_scaler_bound_unscaled`
    - `_upper_scaler_bound_unscaled`
  using the [DDO Viewer](../processing/ddo-viewer.md), and adapting the scaler bounds if the `*_observed_*` values violate them.

Not only quantities local to a single subsystem are scaled, but also quantities involved in the coupling of two neighboring subsystems. It is paramount, that

- mapped responses $^{i}_{j}$sym:H and coupling variables $^{i}_{j}$sym:h are scaled with the same [`ScalerZeroOne`](../../api/Distributed_Design_Optimizer/subsystem/tools/ScalerZeroOne.md) object, and
- shared design variables $^{i}_{j}$sym:z and target shared design variables $^{i}_{j}$sym:z_{t} are scaled with the same [`ScalerZeroOne`](../../api/Distributed_Design_Optimizer/subsystem/tools/ScalerZeroOne.md) object

as they represent the same quantity. `copy.deepcopy()` operations are used for this purpose as shown below. 

It is important to stress, that the scaling bounds should not be excessively large, but instead as tight as possible.

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, this reads as follows:

<div class="collapsible-code" markdown>

```python
        # ── Step 5: Scaling variables ──────────────────────────────────
        # Define one scaler per variable. ScalerZeroOne maps to [0; 1],
        # ScalerConstraint normalizes constraint values.
        # Order: local design variables, shared design variables,
        #        additional design variables (as a result of decomposition),
        #        local objective, local equality constraints,
        #        local inequality constraints,
        #        mapped responses, copy of mapped responses (only if not already included earlier for additional design variables).
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
            ScalerConstraint(-10.0, 10.0),      # [28] compressive stress point 1 station 0 (G1[0:3])
            ScalerConstraint(-50.0, 50.0),      # [29] compressive stress point 1 station 1
            ScalerConstraint(-50.0, 50.0),      # [30] compressive stress point 1 station 2
            ScalerConstraint(-1000.0, 1000.0),  # [31] buckling point 1 compressive station 0 (G1[3:6])
            ScalerConstraint(-500.0, 500.0),    # [32] buckling point 1 compressive station 1
            ScalerConstraint(-500.0, 500.0),    # [33] buckling point 1 compressive station 2
            ScalerConstraint(-1000.0, 1000.0),  # [34] buckling point 1 shear station 0 (G1[6:9])
            ScalerConstraint(-500.0, 500.0),    # [35] buckling point 1 shear station 1
            ScalerConstraint(-500.0, 500.0),    # [36] buckling point 1 shear station 2
            ScalerConstraint(-10.0, 10.0),      # [37] compressive stress point 2 station 0 (G1[9:12])
            ScalerConstraint(-20.0, 20.0),      # [38] compressive stress point 2 station 1
            ScalerConstraint(-10.0, 10.0),      # [39] compressive stress point 2 station 2
            ScalerConstraint(-1000.0, 1000.0),  # [40] buckling point 2 compressive station 0 (G1[12:15])
            ScalerConstraint(-1000.0, 1000.0),  # [41] buckling point 2 compressive station 1
            ScalerConstraint(-1000.0, 1000.0),  # [42] buckling point 2 compressive station 2
            ScalerConstraint(-1000.0, 1000.0),  # [43] buckling point 2 shear station 0 (G1[15:18])
            ScalerConstraint(-1000.0, 1000.0),  # [44] buckling point 2 shear station 1
            ScalerConstraint(-1000.0, 1000.0),  # [45] buckling point 2 shear station 2
            ScalerConstraint(-10.0, 10.0),      # [46] compressive stress point 3 station 0 (G1[18:21])
            ScalerConstraint(-50.0, 50.0),      # [47] compressive stress point 3 station 1
            ScalerConstraint(-50.0, 50.0),      # [48] compressive stress point 3 station 2
            ScalerConstraint(-1200.0, 1200.0),  # [49] buckling point 3 compressive station 0 (G1[21:24])
            ScalerConstraint(-1000.0, 1000.0),  # [50] buckling point 3 compressive station 1
            ScalerConstraint(-500.0, 500.0),    # [51] buckling point 3 compressive station 2
            ScalerConstraint(-10000.0, 10000.0),# [52] buckling point 3 shear station 0 (G1[24:27])
            ScalerConstraint(-1000.0, 1000.0),  # [53] buckling point 3 shear station 1
            ScalerConstraint(-500.0, 500.0),    # [54] buckling point 3 shear station 2
            ScalerConstraint(-10.0, 10.0),      # [55] tensile stress point 4 station 0 (G1[27:30])
            ScalerConstraint(-50.0, 50.0),      # [56] tensile stress point 4 station 1
            ScalerConstraint(-50.0, 50.0),      # [57] tensile stress point 4 station 2
            ScalerConstraint(-50.0, 50.0),      # [58] tensile stress point 5 station 0 (G1[30:33])
            ScalerConstraint(-10.0, 10.0),      # [59] tensile stress point 5 station 1
            ScalerConstraint(-10.0, 10.0),      # [60] tensile stress point 5 station 2
            ScalerConstraint(-1000.0, 1000.0),  # [61] buckling point 5 compressive station 0 (G1[33:36])
            ScalerConstraint(-1000.0, 1000.0),  # [62] buckling point 5 compressive station 1
            ScalerConstraint(-1000.0, 1000.0),  # [63] buckling point 5 compressive station 2
            ScalerConstraint(-1000.0, 1000.0),  # [64] buckling point 5 shear station 0 (G1[36:39])
            ScalerConstraint(-1000.0, 1000.0),  # [65] buckling point 5 shear station 1
            ScalerConstraint(-1000.0, 1000.0),  # [66] buckling point 5 shear station 2
            ScalerConstraint(-10.0, 10.0),      # [67] tensile stress point 6 station 0 (G1[39:42])
            ScalerConstraint(-50.0, 50.0),      # [68] tensile stress point 6 station 1
            ScalerConstraint(-50.0, 50.0),      # [69] tensile stress point 6 station 2
            ScalerConstraint(-10.0, 10.0),      # [70] tensile stress point 1 sign-flip station 0 (G1[54:57])
            ScalerConstraint(-50.0, 50.0),      # [71] tensile stress point 1 sign-flip station 1
            ScalerConstraint(-50.0, 50.0),      # [72] tensile stress point 1 sign-flip station 2
            ScalerConstraint(-10.0, 10.0),      # [73] tensile stress point 2 sign-flip station 0 (G1[57:60])
            ScalerConstraint(-20.0, 20.0),      # [74] tensile stress point 2 sign-flip station 1
            ScalerConstraint(-10.0, 10.0),      # [75] tensile stress point 2 sign-flip station 2
            ScalerConstraint(-10.0, 10.0),      # [76] tensile stress point 3 sign-flip station 0 (G1[60:63])
            ScalerConstraint(-50.0, 50.0),      # [77] tensile stress point 3 sign-flip station 1
            ScalerConstraint(-50.0, 50.0),      # [78] tensile stress point 3 sign-flip station 2
            ScalerConstraint(-10.0, 10.0),      # [79] compressive stress point 4 sign-flip station 0 (G1[63:66])
            ScalerConstraint(-50.0, 50.0),      # [80] compressive stress point 4 sign-flip station 1
            ScalerConstraint(-50.0, 50.0),      # [81] compressive stress point 4 sign-flip station 2
            ScalerConstraint(-50.0, 50.0),      # [82] compressive stress point 5 sign-flip station 0 (G1[66:69])
            ScalerConstraint(-10.0, 10.0),      # [83] compressive stress point 5 sign-flip station 1
            ScalerConstraint(-10.0, 10.0),      # [84] compressive stress point 5 sign-flip station 2
            ScalerConstraint(-10.0, 10.0),      # [85] compressive stress point 6 sign-flip station 0 (G1[69:72])
            ScalerConstraint(-50.0, 50.0),      # [86] compressive stress point 6 sign-flip station 1
            ScalerConstraint(-50.0, 50.0),      # [87] compressive stress point 6 sign-flip station 2
            ScalerConstraint(-1.0, 1.0),        # [88] h_spar margin station constraint 0 (alpha1+alpha3-0.5)
            ScalerConstraint(-1.0, 1.0),        # [89] h_spar margin station constraint 1
            ScalerConstraint(-1.0, 1.0),        # [90] h_spar margin station constraint 2
            ScalerConstraint(-5.0, 5.0),        # [91] ts1 lower gauge station constraint 0 (0.1/12 - ts1)
            ScalerConstraint(-2.0, 2.0),        # [92] ts1 lower gauge station constraint 1
            ScalerConstraint(-2.0, 2.0),        # [93] ts1 lower gauge station constraint 2
            ScalerConstraint(-2.0, 2.0),        # [94] ts1 upper gauge station constraint 0 (ts1 - 9/12)
            ScalerConstraint(-1.0, 1.0),        # [95] ts1 upper gauge station constraint 1
            ScalerConstraint(-0.75, 0.75),      # [96] ts1 upper gauge station constraint 2
            ScalerConstraint(-3.0, 3.00),       # [97] ts3 lower gauge station constraint 0 (0.1/12 - ts3)
            ScalerConstraint(-2.0, 2.0),        # [98] ts3 lower gauge station constraint 1
            ScalerConstraint(-2.0, 2.0),        # [99] ts3 lower gauge station constraint 2
            ScalerConstraint(-2.0, 2.0),        # [100] ts3 upper gauge station constraint 0 (ts3 - 9/12)
            ScalerConstraint(-2.0, 2.0),        # [101] ts3 upper gauge station constraint 1
            ScalerConstraint(-0.75, 0.75),      # [102] ts3 upper gauge station constraint 2
            ScalerConstraint(-2.0, 2.0),        # [103] t1 lower gauge station constraint 0 (0.1/12 - t1)
            ScalerConstraint(-2.0, 2.0),        # [104] t1 lower gauge station constraint 1
            ScalerConstraint(-2.0, 2.0),        # [105] t1 lower gauge station constraint 2
            ScalerConstraint(-2.0, 2.0),        # [106] t1 upper gauge station constraint 0 (t1 - 4/12)
            ScalerConstraint(-2.0, 2.0),        # [107] t1 upper gauge station constraint 1
            ScalerConstraint(-2.0, 2.0),        # [108] t1 upper gauge station constraint 2
            ScalerConstraint(-1.0, 1.0),        # [109] t2 lower gauge station constraint 0 (0.1/12 - t2)
            ScalerConstraint(-1.0, 1.0),        # [110] t2 lower gauge station constraint 1
            ScalerConstraint(-1.0, 1.0),        # [111] t2 lower gauge station constraint 2
            ScalerConstraint(-1.0, 1.0),        # [112] t2 upper gauge station constraint 0 (t2 - 4/12)
            ScalerConstraint(-1.0, 1.0),        # [113] t2 upper gauge station constraint 1
            ScalerConstraint(-1.0, 1.0),        # [114] t2 upper gauge station constraint 2
            ScalerConstraint(-2.0, 2.0),        # [115] t3 lower gauge station constraint 0 (0.1/12 - t3)
            ScalerConstraint(-2.0, 2.0),        # [116] t3 lower gauge station constraint 1
            ScalerConstraint(-2.0, 2.0),        # [117] t3 lower gauge station constraint 2
            ScalerConstraint(-2.0, 2.0),        # [118] t3 upper gauge station constraint 0 (t3 - 4/12)
            ScalerConstraint(-1.0, 1.0),        # [119] t3 upper gauge station constraint 1
            ScalerConstraint(-1.0, 1.0),        # [120] t3 upper gauge station constraint 2
            copy.deepcopy(self._subsystems[0].get_Scalers()[3]),                                                                       # [121] mapped response corresponding to structural_weight [lb]
            copy.deepcopy(self._subsystems[0].get_Scalers()[4]),                                                                       # [122] mapped response corresponding to fuel_weight [lb]
            copy.deepcopy(self._subsystems[2].get_Scalers()[11])                                                                       # [123] mapped response corresponding to wing_twist (delta(L)/q effective area [ft^2])
        ])
```

</div>

Having defined the upper and lower bounds for each design variable as well as all necessary scaling variables, further information needs to be provided for each subsystem:

- design variable granularities
- initial design variables
- reference design variables (optional; needed for some processing functionalities)
- reference local objective values scaled and unscaled (optional; needed for some processing functionalities)

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, this reads as follows:

<div class="collapsible-code" markdown>

```python
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
        self._subsystems[0].set_ReferenceLocalObjectiveValue(self._subsystems[0].get_Scalers()[5].transform(34300.0))
        self._subsystems[0].set_ReferenceLocalObjectiveValueUnscaled(34300.0)
        
        self._subsystems[1].set_DesignVariables_Granularity([0.0] * 2)
        self._subsystems[1].set_DesignVariables([self._subsystems[1].get_Scalers()[0].transform(0.60),                   # 1d[0] throttle
                                                 self._subsystems[1].get_Scalers()[1].transform(40000.0)])               # 1d[1] drag
        self._subsystems[1].set_ReferenceLocalObjectiveValue(None)
        self._subsystems[1].set_ReferenceLocalObjectiveValueUnscaled(None)
                
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

        self._subsystems[3].set_DesignVariables_Granularity([0.0] * 26)
        # Initial design (reformulation): the nominal skin ratio rho = t/ts = 3.0/6.0 = 0.5 and the
        # web sandwich ts2 = 6.0 in are carried over from the original nominal (t=3, ts=6 in). The
        # depth fractions are set to alpha1 = alpha3 = 0.2 so that h_spar = 0.6*D > 0 at every
        # station, giving a strictly feasible starting point w.r.t. the h_spar margin.
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
```

</div>

The beginning of the `InputFile` already defines the general subsystem topology through the use of neighbor IDs for each subsystem.
As stated in the beginning of this tutorial, two neighboring subsystems may be coupled through shared design variables ${}^{i}_{j}$sym:z and/or coupling variables ${}^{j}_{i}$sym:h, where ${}^{j}_{i}h := {}^{j}_{i}H\left({}^{j}r\right)$.
This specific pairwise coupling structure between two neighboring subsystems is defined next.

The distributed design optimization problem formulation of [Step 1.](index.md#1-formulation-of-the-distributed-design-optimization-problem) modelled a shared design variable between subsystems $i$ and $j$ as $^{i}_{j}$sym:z$={}^{j}_{i}$sym:z. Within the abbr:DDO framework, this is defined through either one (but not both simultaneously) of the following couplings:

- `_shareddesignvariable` $^{i}_{j}$sym:z $:= {}^{i}_{j}$sym:z_{t} `_targetshareddesignvariable` <br>, where  $^{i}_{j}$sym:z is a design variable of subsystem $i$ and $^{i}_{j}$sym:z_{t} is a design variable of subsystem $j$ .
- `_targetshareddesignvariable` $^{j}_{i}$sym:z_{t} $:= {}^{j}_{i}$sym:z `_shareddesignvariable` <br>, where $^{j}_{i}$sym:z_{t} is a design variables of subsystem $i$ and $^{j}_{i}$sym:z is a design variable of subsystem $j$ .

Whichever of the above is chosen does not influence the behavior of the abbr:DDO framework.

The following illustrates the coupling structure naming between two neighboring subsystems.

<iframe src="../../framework-architecture/CouplingCircle_Terminology_diagram.drawio.html" width="100%" height="500" style="border:none;" allowfullscreen></iframe>

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, this reads as follows:

<div class="collapsible-code" markdown>

```python
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
        # [specific_fuel_consumption [1/hr], engine_weight [lb]]: owned by subsystem 0 (0d[0] => scaler[0], 0d[1] => scaler[1]), mapped by subsystem 1 (scaler[6], scaler[7])
        self._subsystems[0].set_CouplingVariables("1",
                                                  [self._subsystems[0].get_Scalers()[0].transform(2.0),
                                                   self._subsystems[0].get_Scalers()[1].transform(15000.0)],
                                                  [2.0,
                                                   15000.0])
        self._subsystems[0].set_Indices_CouplingVariables_in_DesignVariables("1", [0, 1])
        self._subsystems[0].set_Copy_MappedResponseVariables("1", [self._subsystems[1].get_Scalers()[6].transform(2.0),
                                                                  self._subsystems[1].get_Scalers()[7].transform(15000.0)])

        # ── circle 1 - 0 (reciprocal of circle 0 - 1) ────────────────────────────
        self._subsystems[1].set_MappedResponseVariables("0",
                                                        [self._subsystems[1].get_Scalers()[6].transform(2.0),
                                                         self._subsystems[1].get_Scalers()[7].transform(15000.0)],
                                                        [2.0,
                                                         15000.0])
        self._subsystems[1].set_Copy_CouplingVariables("0", [self._subsystems[0].get_Scalers()[0].transform(2.0),
                                                            self._subsystems[0].get_Scalers()[1].transform(15000.0)])

        # ── circle 0 - 2 ─────────────────────────────────────────────────────────
        # lift_to_drag_ratio [-]: owned by subsystem 0 (0d[2] => scaler[2]), mapped by subsystem 2 (scaler[17])
        self._subsystems[0].set_CouplingVariables("2", [self._subsystems[0].get_Scalers()[2].transform(5.00)], [5.00])
        self._subsystems[0].set_Indices_CouplingVariables_in_DesignVariables("2", [2])
        self._subsystems[0].set_Copy_MappedResponseVariables("2", [self._subsystems[2].get_Scalers()[17].transform(5.00)])
        # total_weight [lb]: owned by subsystem 2 (2d[9] => scaler[9]), mapped by subsystem 0 (scaler[8])
        self._subsystems[0].set_MappedResponseVariables("2", [self._subsystems[0].get_Scalers()[8].transform(25000.0)], [25000.0])
        self._subsystems[0].set_Copy_CouplingVariables("2", [self._subsystems[2].get_Scalers()[9].transform(25000.0)])

        # ── circle 2 - 0 (reciprocal of circle 0 - 2) ────────────────────────────
        self._subsystems[2].set_MappedResponseVariables("0", [self._subsystems[2].get_Scalers()[17].transform(5.00)], [5.00])
        self._subsystems[2].set_Copy_CouplingVariables("0", [self._subsystems[0].get_Scalers()[2].transform(5.00)])
        self._subsystems[2].set_CouplingVariables("0", [self._subsystems[2].get_Scalers()[9].transform(25000.0)], [25000.0])
        self._subsystems[2].set_Indices_CouplingVariables_in_DesignVariables("0", [9])
        self._subsystems[2].set_Copy_MappedResponseVariables("0", [self._subsystems[0].get_Scalers()[8].transform(25000.0)])

        # ── circle 0 - 3 ─────────────────────────────────────────────────────────
        # [structural_weight [lb], fuel_weight [lb]]: owned by subsystem 0 (0d[3] => scaler[3], 0d[4] => scaler[4]), mapped by subsystem 3 (scaler[121], scaler[122])
        self._subsystems[0].set_CouplingVariables("3",
                                                  [self._subsystems[0].get_Scalers()[3].transform(25000.0),
                                                   self._subsystems[0].get_Scalers()[4].transform(25000.0)],
                                                  [25000.0,
                                                   25000.0])
        self._subsystems[0].set_Indices_CouplingVariables_in_DesignVariables("3", [3, 4])
        self._subsystems[0].set_Copy_MappedResponseVariables("3", [self._subsystems[3].get_Scalers()[121].transform(25000.0),
                                                                  self._subsystems[3].get_Scalers()[122].transform(25000.0)])

        # ── circle 3 - 0 (reciprocal of circle 0 - 3) ────────────────────────────
        self._subsystems[3].set_MappedResponseVariables("0",
                                                        [self._subsystems[3].get_Scalers()[121].transform(25000.0),
                                                         self._subsystems[3].get_Scalers()[122].transform(25000.0)],
                                                        [25000.0,
                                                         25000.0])
        self._subsystems[3].set_Copy_CouplingVariables("0", [self._subsystems[0].get_Scalers()[3].transform(25000.0),
                                                            self._subsystems[0].get_Scalers()[4].transform(25000.0)])

        # ── circle 1 - 2 ─────────────────────────────────────────────────────────
        # drag [lb]: owned by subsystem 1 (1d[1] => scaler[1]), mapped by subsystem 2 (scaler[18])
        self._subsystems[1].set_CouplingVariables("2", [self._subsystems[1].get_Scalers()[1].transform(40000.0)], [40000.0])
        self._subsystems[1].set_Indices_CouplingVariables_in_DesignVariables("2", [1])
        self._subsystems[1].set_Copy_MappedResponseVariables("2", [self._subsystems[2].get_Scalers()[18].transform(40000.0)])
        # engine_scale_factor [-]: owned by subsystem 2 (2d[10] => scaler[10]), mapped by subsystem 1 (scaler[8])
        self._subsystems[1].set_MappedResponseVariables("2", [self._subsystems[1].get_Scalers()[8].transform(1.0)], [1.0])
        self._subsystems[1].set_Copy_CouplingVariables("2", [self._subsystems[2].get_Scalers()[10].transform(1.0)])

        # ── circle 2 - 1 (reciprocal of circle 1 - 2) ────────────────────────────
        self._subsystems[2].set_CouplingVariables("1", [self._subsystems[2].get_Scalers()[10].transform(1.0)], [1.0])
        self._subsystems[2].set_Indices_CouplingVariables_in_DesignVariables("1", [10])
        self._subsystems[2].set_Copy_MappedResponseVariables("1", [self._subsystems[1].get_Scalers()[8].transform(1.0)])
        self._subsystems[2].set_MappedResponseVariables("1", [self._subsystems[2].get_Scalers()[18].transform(40000.0)], [40000.0])
        self._subsystems[2].set_Copy_CouplingVariables("1", [self._subsystems[1].get_Scalers()[1].transform(40000.0)])

        # ── circle 2 - 3 ─────────────────────────────────────────────────────────
        # wing_twist: owned by subsystem 2 (2d[11] => scaler[11]), mapped by subsystem 3 (scaler[123])
        self._subsystems[2].set_CouplingVariables("3", [self._subsystems[2].get_Scalers()[11].transform(10.0)], [10.0])
        self._subsystems[2].set_Indices_CouplingVariables_in_DesignVariables("3", [11])
        self._subsystems[2].set_Copy_MappedResponseVariables("3", [self._subsystems[3].get_Scalers()[123].transform(10.0)])
        # lift: owned by subsystem 3 (3d[25] => scaler[25]), mapped by subsystem 2 (scaler[19])
        self._subsystems[2].set_MappedResponseVariables("3", [self._subsystems[2].get_Scalers()[19].transform(25000.0)], [25000.0])
        self._subsystems[2].set_Copy_CouplingVariables("3", [self._subsystems[3].get_Scalers()[25].transform(25000.0)])
        # shared design variables [thickness_to_chord_ratio, wing_sweep_angle, wing_aspect_ratio, wing_surface_area, tail_aspect_ratio, tail_surface_area]:
        # owned by subsystem 2 (2d[3:9]), target in subsystem 3 (3d[19:25])
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
        self._subsystems[3].set_CouplingVariables("2", [self._subsystems[3].get_Scalers()[25].transform(25000.0)], [25000.0])
        self._subsystems[3].set_Indices_CouplingVariables_in_DesignVariables("2", [25])
        self._subsystems[3].set_Copy_MappedResponseVariables("2", [self._subsystems[2].get_Scalers()[19].transform(25000.0)])
        self._subsystems[3].set_MappedResponseVariables("2", [self._subsystems[3].get_Scalers()[123].transform(10.0)], [10.0])
        self._subsystems[3].set_Copy_CouplingVariables("2", [self._subsystems[2].get_Scalers()[11].transform(10.0)])
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

</div>


## 4. Defining the Analysis<id>.py

[Step 2.](index.md#2-creation-of-folder-holding-all-use-case-specific-files) previously created `Analysis<id>.py` files and classes for each subsystem.
The following class methods of each `Analysis<id>` need to be detailed:

- `def evaluateLocalResponses()` > implements ${}^{i}$sym:r$({}^{i}$sym:d$)$
- `def mapLocalResponsesDesignVariables_to_CouplingParameters()` > sets `_mappedresponses` $^{i}_{j}$sym:H, `_shareddesignvariables` $^{i}_{j}$sym:z, `_couplingvariables` $^{j}_{i}$sym:h, `_targetshareddesignvariables` $^{j}_{i}$sym:z_{t} for some given ${}^{i}$sym:r$({}^{i}$sym:d$)$ and ${}^{i}$sym:d. This implementation needs to match with the coupling circle definition of the `InputFile` (excluding `set_Copy_*()` calls).
- `def mapLocalResponsesDesignVariables_to_CouplingParameters_Jacobians()` > some coordination methods (e.g. [abbr:ALADIN](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/aladin.md) and [abbr:SBDP](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/sensitivity-based-distributed-programming.md)) require the first-order derivatives (Jacobians) of the mapped responses $^{i}_{j}$sym:H with respect to the design variables ${}^{i}$sym:d. Because the optimizer operates in the scaled $[0, 1]$ domain, the Jacobian is stored in scaled space, i.e. $\partial(\text{scaled } {}^{i}_{j}H)\,/\,\partial(\text{scaled } {}^{i}d)$; unscaled analytic partials are converted with the constant scaler slopes `scaler.get_scale()` (see [Derivative Computation](../../framework-architecture/derivative-computation.md)). Each neighbor's Jacobian is passed through the setter `set_MappedResponses_Jacobian(id=, mappedresponses_jacobian_in=)`; any unknown entry (or an all-`None` matrix of shape `(number_of_mapped_responses, number_of_design_variables)`) is left as `None`, prompting an internal finite-difference approximation.
- `def mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian()` > analogously, methods that additionally need curvature (e.g. [abbr:ALADIN](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/aladin.md)) require the second-order derivatives (Hessians) of the mapped responses with respect to ${}^{i}$sym:d. This method **returns** the scaled-space Hessian tensor `[neighbor][response][number_of_design_variables][number_of_design_variables]`, or `None` (fully or per entry) to prompt the framework's internal BFGS / finite-difference approximation ([Derivative Computation](../../framework-architecture/derivative-computation.md)).

In case, the above implementations become too complex in `Analysis<id>.py`, separate helper folders or files may be added within the `subsystem<id>/` folder and be imported into `Analysis<id>.py`.

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, this reads as follows:

<div class="collapsible-code" markdown>

```python
class Analysis0(AnalysisInterface):
    """Analysis class for Subsystem 0 (Aircraft) in the Supersonic Business Jet (SSBJ) problem.

    Implements the AnalysisInterface to compute the aircraft range and total
    weight for Subsystem 0 (Aircraft) and to map its coupling variables to the
    neighboring subsystems. This subsystem acts as the top level in the
    hierarchical decomposition.

    Attributes:
        None specific to this class; inherits from AnalysisInterface.
    """
    def __init__(self) -> None:
        """Initialize the Analysis0 instance."""
        pass
        
    def evaluateLocalResponses(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the physical responses of Subsystem 0.

        Computes the subsystem responses based on the current design variables.
        The aircraft range is evaluated with the Breguet range helper and the
        total weight is the sum of engine, structural, and fuel weight.

        Args:
            subsystem: The LocalSubSystemBasis instance containing design variables
                and where computed responses will be stored.
        """
        
        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        
        # load copymappedresponsevariables from other neighboring subsystems which may be necessary for this analysis
        # scalers: List[ScalerBasis] = subsystem.get_Scalers() 
        # copymappedresponsevariables_neighbor_id_scaled01: List[float] | None = subsystem.get_Copy_MappedResponseVariables(id=neighbor_id)  # scaled01 values
        # # to unscale, run
        # copymappedresponsevariables_neighbor_id = scalers[corresponding_index].inverse_transform(copymappedresponsevariables_neighbor_id_scaled01)  # unscaled value        

        # Compute responses using des_var and copymappedresponsevariables
        ################################################################
        ###          USER CODE: Compute responses                    ###
        ################################################################
        
        # unpack design variables
        specific_fuel_consumption = des_var[0]  # [1/hr]
        engine_weight = des_var[1]  # [lb]
        lift_to_drag_ratio = des_var[2]  # [-]
        structural_weight = des_var[3]  # [lb]
        fuel_weight = des_var[4]  # [lb]

        total_weight = engine_weight + structural_weight + fuel_weight  # [lb]

        range_value = calculate_range(specific_fuel_consumption=specific_fuel_consumption,
                                      lift_to_drag_ratio=lift_to_drag_ratio,
                                      total_weight=total_weight,
                                      fuel_weight=fuel_weight,
                                      h=h,
                                      Mach=Mach)

        responses = [range_value,   # [nmi]
                     total_weight]  # [lb]
        
        # responses is a unscaled quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        subsystem.set_Responses_Unscaled(responses)

    def mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: LocalSubSystemBasis) -> None:
        """Map responses and design variables for inter-subsystem coupling.

        Maps computed responses and shared/target design variables to neighboring
        subsystems.

        Args:
            subsystem: The LocalSubSystemBasis instance containing responses
                and design variables to be mapped.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var: List[float] = subsystem.get_DesignVariables()  # scaled01 values
        des_var_unscaled: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
                 
        # map responses and shared/target design variables
        ################################################################
        ###          USER CODE: Map to coupling parameters           ###
        ################################################################
        # only map scaled01 quantities!
        
        # subsystem.set_MappedResponseVariables(id=,
        #                                       mappedresponsesin=,
        #                                       mappedresponsesin_unscaled=)
        # subsystem.set_MappedResponseVariables(id=,
        #                                       mappedresponsesin=,
        #                                       mappedresponsesin_unscaled=)
        
        subsystem.set_CouplingVariables("1",
                                        couplingvariablein=[des_var[0],   # specific_fuel_consumption [1/hr]
                                                            des_var[1]],  # engine_weight [lb]
                                        couplingvariablein_unscaled=[des_var_unscaled[0],
                                                                     des_var_unscaled[1]])
        
        subsystem.set_CouplingVariables("2",
                                        couplingvariablein=[des_var[2]],  # lift_to_drag_ratio [-]
                                        couplingvariablein_unscaled=[des_var_unscaled[2]])

        subsystem.set_MappedResponseVariables(id="2",
                                              mappedresponsesin=[scalers[8].transform(responses[1])],  # total_weight [lb]
                                              mappedresponsesin_unscaled=[responses[1]])

        subsystem.set_CouplingVariables("3",
                                        couplingvariablein=[des_var[3],   # structural_weight [lb]
                                                            des_var[4]],  # fuel_weight [lb]
                                        couplingvariablein_unscaled=[des_var_unscaled[3],
                                                                     des_var_unscaled[4]])
        
        # subsystem.set_TargetSharedDesignVariables(id=,
        #                                     targetdesignvariablesin=,
        #                                     targetdesignvariables_unscaled=)
        # subsystem.set_TargetSharedDesignVariables(id=,
        #                                     targetdesignvariablesin=,
        #                                     targetdesignvariables_unscaled=)
        
        # subsystem.set_SharedDesignVariables(id=,
        #                                     shareddesignvariablesin=,
        #                                     shareddesignvariablesin_unscaled=)
        # subsystem.set_SharedDesignVariables(id=,
        #                                     shareddesignvariablesin=,
        #                                     shareddesignvariablesin_unscaled=)

        ################################################################
        ###          END USER CODE                                   ###
        ################################################################

    def mapLocalResponsesDesignVariables_to_CouplingParameters_Jacobians(self, subsystem: LocalSubSystemBasis) -> None:
        """Map the Jacobians of the mapped responses.

        Args:
            subsystem: The subsystem for which the Jacobians are mapped.
        """
        
        responses: List[float] = subsystem.get_Responses_Unscaled()  
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var: List[float] = subsystem.get_DesignVariables()        
        
        ################################################################
        ###          USER CODE: Compute Jacobians                    ###
        ################################################################
        # The mapped responses come from complex physics with no closed-form
        # Jacobian. For consistency with the other use-cases we still call the
        # setter, passing an all-None matrix of the correct shape
        # (number_of_mapped_responses, number_of_design_variables) so the
        # framework finite-differences every entry.
        n_dv: int = len(des_var)
        # id "2": 1 mapped response (total_weight)
        subsystem.set_MappedResponses_Jacobian(
            id="2",
            mappedresponses_jacobian_in=[[None] * n_dv])
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################

    def mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian(self, subsystem: LocalSubSystemBasis) -> None:
        """Map the Hessians of the mapped responses, if known a priori.

        Args:
            subsystem: The subsystem for which the Hessians are mapped.
        """
        ################################################################
        ###          USER CODE: Compute Hessians                     ###
        ################################################################
        # No closed-form Hessian available (complex physics); return None to let
        # the framework fall back to its internal finite-difference computation.
        return None
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
```

</div>
<br/>

<div class="collapsible-code" markdown>

```python
class Analysis1(AnalysisInterface):
    """Analysis class for Subsystem 1 (Propulsion) in the Supersonic Business Jet (SSBJ) problem.

    Implements the AnalysisInterface to compute the propulsion responses (engine
    temperature, throttle limits, specific fuel consumption, engine scale factor
    and engine weight) for Subsystem 1 (Propulsion) and to map its coupling
    variables. This subsystem operates at level 1 in the hierarchical decomposition.

    Attributes:
        None specific to this class; inherits from AnalysisInterface.
    """
    def __init__(self) -> None:
        """Initialize the Analysis1 instance."""
        pass
        
    def evaluateLocalResponses(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the physical responses of Subsystem 1.

        Computes the subsystem responses based on the current design variables
        using the propulsion (engine deck) helper functions.

        Args:
            subsystem: The LocalSubSystemBasis instance containing design variables
                and where computed responses will be stored.
        """
                  
        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        
        # load copymappedresponsevariables from other neighboring subsystems which may be necessary for this analysis
        # scalers: List[ScalerBasis] = subsystem.get_Scalers() 
        # copymappedresponsevariables_neighbor_id_scaled01: List[float] | None = subsystem.get_Copy_MappedResponseVariables(id=neighbor_id)  # scaled01 values
        # # to unscale, run
        # copymappedresponsevariables_neighbor_id = scalers[corresponding_index].inverse_transform(copymappedresponsevariables_neighbor_id_scaled01)  # unscaled value        

        # Compute responses using des_var and copymappedresponsevariables
        ################################################################
        ###          USER CODE: Compute responses                    ###
        ################################################################
        dim_throttle = 16168 * des_var[0]  # dim_throttle [lb] (= 16168 * throttle)

        engine_temperature = calculate_engine_temperature(drag=des_var[1],
                                                          throttle=des_var[0],
                                                          h=h,
                                                          Mach=Mach)

        throttle_uA = calculate_throttle_uA(h=h,
                                            Mach=Mach)

        specific_fuel_consumption = calculate_specific_fuel_consumption(dim_throttle=dim_throttle,
                                                                        h=h,
                                                                        Mach=Mach)

        engine_scale_factor = calculate_engine_scale_factor(drag=des_var[1],
                                                            dim_throttle=dim_throttle)

        engine_weight = calculate_engine_weight(engine_scale_factor=engine_scale_factor)

        responses = [engine_temperature,   # [-]
                     dim_throttle,
                     throttle_uA,   # [lb]
                     specific_fuel_consumption,   # [1/hr]
                     engine_scale_factor,   # [-]
                     engine_weight]   # [lb]
        
        # responses is a unscaled quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        subsystem.set_Responses_Unscaled(responses)        

    def mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: LocalSubSystemBasis) -> None:
        """Map responses and design variables for inter-subsystem coupling.

        Maps the mapped response to Subsystem 0 and the shared design variable
        to Subsystem 2 for coordination between subsystems.

        Args:
            subsystem: The LocalSubSystemBasis instance containing responses
                and design variables to be mapped.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var: List[float] = subsystem.get_DesignVariables()  # scaled01 values
        des_var_unscaled: List[float] = subsystem.get_DesignVariables_Unscaled() # unscaled
                         
        # map responses and shared/target design variables
        ################################################################
        ###          USER CODE: Map to coupling parameters           ###
        ################################################################
        # only map scaled01 quantities!
        
        subsystem.set_MappedResponseVariables(id="0",
                                              mappedresponsesin=[scalers[6].transform(responses[3]),   # specific_fuel_consumption [1/hr]
                                                                 scalers[7].transform(responses[5])],  # engine_weight [lb]
                                              mappedresponsesin_unscaled=[responses[3],
                                                                          responses[5]])
        
        # subsystem.set_CouplingVariables(id=,
        #                                 couplingvariablein=,
        #                                 couplingvariablein_unscaled=)
        # subsystem.set_CouplingVariables(id=,
        #                                 couplingvariablein=,
        #                                 couplingvariablein_unscaled=)
        
        # subsystem.set_TargetDesignVariables(id=,
        #                                     targetdesignvariablesin=,
        #                                     targetdesignvariables_unscaled=)
        # subsystem.set_TargetDesignVariables(id=,
        #                                     targetdesignvariablesin=,
        #                                     targetdesignvariables_unscaled=)
        
        subsystem.set_CouplingVariables("2",
                                        couplingvariablein=[des_var[1]],  # drag [lb]
                                        couplingvariablein_unscaled=[des_var_unscaled[1]])

        subsystem.set_MappedResponseVariables(id="2",
                                              mappedresponsesin=[scalers[8].transform(responses[4])],  # engine_scale_factor [-]
                                              mappedresponsesin_unscaled=[responses[4]])

        ################################################################
        ###          END USER CODE                                   ###
        ################################################################

    def mapLocalResponsesDesignVariables_to_CouplingParameters_Jacobians(self, subsystem: LocalSubSystemBasis) -> None:
        """Map the Jacobians of the mapped responses.

        Args:
            subsystem: The subsystem for which the Jacobians are mapped.
        """
        
        responses: List[float] = subsystem.get_Responses_Unscaled()  
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var: List[float] = subsystem.get_DesignVariables()        
        
        ################################################################
        ###          USER CODE: Compute Jacobians                    ###
        ################################################################
        # The mapped responses come from complex physics with no closed-form
        # Jacobian. For consistency with the other use-cases we still call the
        # setter, passing an all-None matrix of the correct shape
        # (number_of_mapped_responses, number_of_design_variables) so the
        # framework finite-differences every entry.
        n_dv: int = len(des_var)
        # id "0": 2 mapped responses (specific_fuel_consumption, engine_weight)
        subsystem.set_MappedResponses_Jacobian(
            id="0",
            mappedresponses_jacobian_in=[[None] * n_dv for _ in range(2)])
        # id "2": 1 mapped response (engine_scale_factor)
        subsystem.set_MappedResponses_Jacobian(
            id="2",
            mappedresponses_jacobian_in=[[None] * n_dv])
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################

    def mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian(self, subsystem: LocalSubSystemBasis) -> None:
        """Map the Hessians of the mapped responses, if known a priori.

        Args:
            subsystem: The subsystem for which the Hessians are mapped.
        """
        ################################################################
        ###          USER CODE: Compute Hessians                     ###
        ################################################################
        # No closed-form Hessian available (complex physics); return None to let
        # the framework fall back to its internal finite-difference computation.
        return None
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
```

</div>
<br/>

<div class="collapsible-code" markdown>

```python
class Analysis2(AnalysisInterface):
    """Analysis class for Subsystem 2 (Aerodynamics) in the Supersonic Business Jet (SSBJ) problem.

    Implements the AnalysisInterface to compute the aerodynamic responses (lift,
    drag, lift-to-drag ratio, pressure gradient and lift coefficients) for
    Subsystem 2 (Aerodynamics) and to map its coupling and shared design
    variables. This subsystem operates at level 1 in the hierarchical decomposition.

    Attributes:
        None specific to this class; inherits from AnalysisInterface.
    """
    def __init__(self) -> None:
        """Initialize the Analysis2 instance."""
        pass
        
    def evaluateLocalResponses(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the physical responses of Subsystem 2.

        Computes the subsystem responses based on the current design variables
        using the aerodynamic drag-polar helper function.

        Args:
            subsystem: The LocalSubSystemBasis instance containing design variables
                and where computed responses will be stored.
        """
                  
        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values
        
        # load copymappedresponsevariables from other neighboring subsystems which may be necessary for this analysis
        # scalers: List[ScalerBasis] = subsystem.get_Scalers() 
        # copymappedresponsevariables_neighbor_id_scaled01: List[float] | None = subsystem.get_Copy_MappedResponseVariables(id=neighbor_id)  # scaled01 values
        # # to unscale, run
        # copymappedresponsevariables_neighbor_id = scalers[corresponding_index].inverse_transform(copymappedresponsevariables_neighbor_id_scaled01)  # unscaled value        

        # Compute responses using des_var and copymappedresponsevariables
        ################################################################
        ###          USER CODE: Compute responses                    ###
        ################################################################
        
        [lift, drag, lift_to_drag_ratio, pressure_gradient, wing_lift_coefficient, tail_lift_coefficient] = calculate_drag_polar(
            tail_sweep_angle=des_var[0],           # [deg]
            wing_moment_arm=des_var[1],            # [ft]
            tail_moment_arm=des_var[2],            # [ft]
            thickness_to_chord_ratio=des_var[3],   # [-]
            wing_sweep_angle=des_var[4],           # [deg]
            wing_aspect_ratio=des_var[5],          # [-]
            wing_surface_area=des_var[6],          # [ft^2]
            tail_aspect_ratio=des_var[7],          # [-]
            tail_surface_area=des_var[8],          # [ft^2]
            total_weight=des_var[9],               # [lb]
            engine_scale_factor=des_var[10],       # [-]
            wing_twist=des_var[11],                # [deg]
            h=h,
            Mach=Mach)

        responses = [pressure_gradient,      # [0] adverse pressure gradient factor [-]
                     wing_lift_coefficient,  # [1] wing lift coefficient [-]
                     tail_lift_coefficient,  # [2] tail lift coefficient [-]
                     lift,                   # [3] lift [lb]
                     drag,                   # [4] drag [lb]
                     lift_to_drag_ratio]     # [5] lift-to-drag ratio [-]
        
        # responses is a unscaled quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        subsystem.set_Responses_Unscaled(responses)

    def mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: LocalSubSystemBasis) -> None:
        """Map responses and design variables for inter-subsystem coupling.

        Maps the mapped response to Subsystem 0 and the target shared design
        variable to Subsystem 1 for coordination between subsystems.

        Args:
            subsystem: The LocalSubSystemBasis instance containing responses
                and design variables to be mapped.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var: List[float] = subsystem.get_DesignVariables()  # scaled01 values
        des_var_unscaled: List[float] = subsystem.get_DesignVariables_Unscaled() # unscaled
                 
        # map responses and shared/target design variables
        ################################################################
        ###          USER CODE: Map to coupling parameters           ###
        ################################################################
        # only map scaled01 quantities!
        
        subsystem.set_MappedResponseVariables(id="0",
                                              mappedresponsesin=[scalers[17].transform(responses[5])],  # lift_to_drag_ratio [-]
                                              mappedresponsesin_unscaled=[responses[5]])

        subsystem.set_CouplingVariables("0",
                                        couplingvariablein=[des_var[9]],  # total_weight [lb]
                                        couplingvariablein_unscaled=[des_var_unscaled[9]])
        
        # subsystem.set_CouplingVariables(id=,
        #                                 couplingvariablein=,
        #                                 couplingvariablein_unscaled=)
        # subsystem.set_CouplingVariables(id=,
        #                                 couplingvariablein=,
        #                                 couplingvariablein_unscaled=)
        
        subsystem.set_CouplingVariables("1",
                                        couplingvariablein=[des_var[10]],  # engine_scale_factor [-]
                                        couplingvariablein_unscaled=[des_var_unscaled[10]])

        subsystem.set_MappedResponseVariables(id="1",
                                              mappedresponsesin=[scalers[18].transform(responses[4])],  # drag [lb]
                                              mappedresponsesin_unscaled=[responses[4]])

        subsystem.set_CouplingVariables("3",
                                        couplingvariablein=[des_var[11]],  # wing_twist [deg]
                                        couplingvariablein_unscaled=[des_var_unscaled[11]])

        subsystem.set_MappedResponseVariables(id="3",
                                              mappedresponsesin=[scalers[19].transform(responses[3])],  # lift [lb]
                                              mappedresponsesin_unscaled=[responses[3]])

        subsystem.set_SharedDesignVariables(id="3",
                                            shareddesignvariablesin=des_var[3:9],  # [thickness_to_chord_ratio, wing_sweep_angle, wing_aspect_ratio, wing_surface_area, tail_aspect_ratio, tail_surface_area]
                                            shareddesignvariablesin_unscaled=des_var_unscaled[3:9])

        # subsystem.set_SharedDesignVariables(id=,
        #                                     shareddesignvariablesin=,
        #                                     shareddesignvariablesin_unscaled=)
        # subsystem.set_SharedDesignVariables(id=,
        #                                     shareddesignvariablesin=,
        #                                     shareddesignvariablesin_unscaled=)

        ################################################################
        ###          END USER CODE                                   ###
        ################################################################

    def mapLocalResponsesDesignVariables_to_CouplingParameters_Jacobians(self, subsystem: LocalSubSystemBasis) -> None:
        """Map the Jacobians of the mapped responses.

        Args:
            subsystem: The subsystem for which the Jacobians are mapped.
        """
        
        responses: List[float] = subsystem.get_Responses_Unscaled()  
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var: List[float] = subsystem.get_DesignVariables()        
        
        ################################################################
        ###          USER CODE: Compute Jacobians                    ###
        ################################################################
        # The mapped responses come from complex physics with no closed-form
        # Jacobian. For consistency with the other use-cases we still call the
        # setter, passing an all-None matrix of the correct shape
        # (number_of_mapped_responses, number_of_design_variables) so the
        # framework finite-differences every entry.
        n_dv: int = len(des_var)
        # id "0": 1 mapped response (lift_to_drag_ratio)
        subsystem.set_MappedResponses_Jacobian(
            id="0",
            mappedresponses_jacobian_in=[[None] * n_dv])
        # id "1": 1 mapped response (drag)
        subsystem.set_MappedResponses_Jacobian(
            id="1",
            mappedresponses_jacobian_in=[[None] * n_dv])
        # id "3": 1 mapped response (lift)
        subsystem.set_MappedResponses_Jacobian(
            id="3",
            mappedresponses_jacobian_in=[[None] * n_dv])
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################

    def mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian(self, subsystem: LocalSubSystemBasis) -> None:
        """Map the Hessians of the mapped responses, if known a priori.

        Args:
            subsystem: The subsystem for which the Hessians are mapped.
        """
        ################################################################
        ###          USER CODE: Compute Hessians                     ###
        ################################################################
        # No closed-form Hessian available (complex physics); return None to let
        # the framework fall back to its internal finite-difference computation.
        return None
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
```

</div>
<br/>

<div class="collapsible-code" markdown>

```python
class Analysis3(AnalysisInterface):
    """Analysis class for Subsystem 3 (Structure) in the Supersonic Business Jet (SSBJ) problem.

    Implements the AnalysisInterface to compute the structural responses
    (stresses, buckling, h_spar margin, reconstructed thicknesses, structural
    and fuel weight and the effective wing-twist area) for Subsystem 3
    (Structure) and to map its coupling and shared design variables. This
    subsystem operates at level 1 in the hierarchical decomposition.

    Attributes:
        None specific to this class; inherits from AnalysisInterface.
    """
    def __init__(self) -> None:
        """Initialize the Analysis3 instance."""
        pass

    def evaluateLocalResponses(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the physical responses of Subsystem 3.

        Computes the subsystem responses based on the current design variables
        using the structural (wing box) helper function.

        Args:
            subsystem: The LocalSubSystemBasis instance containing design variables
                and where computed responses will be stored.
        """

        des_var: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values

        # load copymappedresponsevariables from other neighboring subsystems which may be necessary for this analysis
        # scalers: List[ScalerBasis] = subsystem.get_Scalers()
        # copymappedresponsevariables_neighbor_id_scaled01: List[float] | None = subsystem.get_Copy_MappedResponseVariables(id=neighbor_id)  # scaled01 values
        # # to unscale, run
        # copymappedresponsevariables_neighbor_id = scalers[corresponding_index].inverse_transform(copymappedresponsevariables_neighbor_id_scaled01)  # unscaled value

        # Compute responses using des_var and copymappedresponsevariables
        ################################################################
        ###          USER CODE: Compute responses                    ###
        ################################################################

        C_structure, t_ft, ts_ft, hspar_margin, structural_weight, fuel_weight, wing_twist = calculate_structural_responses(
            taper_ratio=des_var[0],                             # [-]
            alpha1=[des_var[i] for i in range(1, 4)],           # top-sandwich depth fractions [-]
            alpha3=[des_var[i] for i in range(4, 7)],           # bottom-sandwich depth fractions [-]
            ts2=[des_var[i] for i in range(7, 10)],             # web sandwich thicknesses [in]
            rho1=[des_var[i] for i in range(10, 13)],           # top skin ratios [-]
            rho2=[des_var[i] for i in range(13, 16)],           # web skin ratios [-]
            rho3=[des_var[i] for i in range(16, 19)],           # bottom skin ratios [-]
            thickness_to_chord_ratio=des_var[19],               # [-]
            wing_sweep_angle=des_var[20],                       # [deg]
            wing_aspect_ratio=des_var[21],                      # [-]
            wing_surface_area=des_var[22],                      # [ft^2]
            tail_aspect_ratio=des_var[23],                      # [-]
            tail_surface_area=des_var[24],                      # [ft^2]
            lift=des_var[25],                                   # [lb]
            h=h)                                                # altitude [ft]

        # responses layout: C_structure (stresses/buckling/h_spar), t_ft/ts_ft reconstructed
        # thicknesses [ft], hspar_margin [-], structural_weight [lb], fuel_weight [lb],
        # wing_twist = delta(L)/q effective area [ft^2]
        responses = C_structure + t_ft + ts_ft + hspar_margin + [structural_weight, fuel_weight, wing_twist]

        # responses is a unscaled quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        subsystem.set_Responses_Unscaled(responses)

    def mapLocalResponsesDesignVariables_to_CouplingParameters(self, subsystem: LocalSubSystemBasis) -> None:
        """Map responses and design variables for inter-subsystem coupling.

        Args:
            subsystem: The LocalSubSystemBasis instance containing responses
                and design variables to be mapped.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var: List[float] = subsystem.get_DesignVariables()  # scaled01 values
        des_var_unscaled: List[float] = subsystem.get_DesignVariables_Unscaled()  # unscaled values

        # map responses and shared/target design variables
        ################################################################
        ###          USER CODE: Map to coupling parameters           ###
        ################################################################
        # only map scaled01 quantities!

        subsystem.set_MappedResponseVariables(id="0",
                                              mappedresponsesin=[scalers[121].transform(responses[-3]),   # structural_weight [lb]
                                                                 scalers[122].transform(responses[-2])],  # fuel_weight [lb]
                                              mappedresponsesin_unscaled=[responses[-3],
                                                                          responses[-2]])

        subsystem.set_CouplingVariables("2",
                                        couplingvariablein=[des_var[25]],  # lift [lb]
                                        couplingvariablein_unscaled=[des_var_unscaled[25]])

        subsystem.set_MappedResponseVariables(id="2",
                                              mappedresponsesin=[scalers[123].transform(responses[-1])],  # wing_twist = delta(L)/q [ft^2]
                                              mappedresponsesin_unscaled=[responses[-1]])

        subsystem.set_TargetSharedDesignVariables(id="2",
                                                  targetdesignvariablesin=des_var[19:25],  # [thickness_to_chord_ratio, wing_sweep_angle, wing_aspect_ratio, wing_surface_area, tail_aspect_ratio, tail_surface_area]
                                                  targetdesignvariablesin_unscaled=des_var_unscaled[19:25])

        ################################################################
        ###          END USER CODE                                   ###
        ################################################################

    def mapLocalResponsesDesignVariables_to_CouplingParameters_Jacobians(self, subsystem: LocalSubSystemBasis) -> None:
        """Map the Jacobians of the mapped responses.

        Args:
            subsystem: The subsystem for which the Jacobians are mapped.
        """

        responses: List[float] = subsystem.get_Responses_Unscaled()
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        des_var: List[float] = subsystem.get_DesignVariables()

        ################################################################
        ###          USER CODE: Compute Jacobians                    ###
        ################################################################
        # The mapped responses come from complex physics with no closed-form
        # Jacobian. For consistency with the other use-cases we still call the
        # setter, passing an all-None matrix of the correct shape
        # (number_of_mapped_responses, number_of_design_variables) so the
        # framework finite-differences every entry.
        n_dv: int = len(des_var)
        # id "0": 2 mapped responses (structural_weight, fuel_weight)
        subsystem.set_MappedResponses_Jacobian(
            id="0",
            mappedresponses_jacobian_in=[[None] * n_dv for _ in range(2)])
        # id "2": 1 mapped response (wing_twist)
        subsystem.set_MappedResponses_Jacobian(
            id="2",
            mappedresponses_jacobian_in=[[None] * n_dv])
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################

    def mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian(self, subsystem: LocalSubSystemBasis) -> None:
        """Map the Hessians of the mapped responses, if known a priori.

        Args:
            subsystem: The subsystem for which the Hessians are mapped.
        """
        ################################################################
        ###          USER CODE: Compute Hessians                     ###
        ################################################################
        # No closed-form Hessian available (complex physics); return None to let
        # the framework fall back to its internal finite-difference computation.
        return None
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
```

</div>

## 5. Defining the LocalConstraints<id>.py

[Step 2.](index.md#2-creation-of-folder-holding-all-use-case-specific-files) previously created `LocalConstraints<id>.py` files and classes for each subsystem. 
The following class methods of each `LocalConstraints<id>` need to be detailed:

- `def evaluateEqualityLocalConstraints()` > implements ${}^{i}$sym:v_h
- `def evaluate_Jacobian_EqualityLocalConstraints()` > some coordination methods (e.g. [abbr:ALADIN](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/aladin.md) and [abbr:SBDP](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/sensitivity-based-distributed-programming.md)) require the first-order derivatives (Jacobian) of the local equality constraints ${}^{i}$sym:v_h with respect to the design variables ${}^{i}$sym:d. Because the optimizer operates in the scaled domain (design variables in $[0, 1]$, constraints in $[-0.5, 0.5]$), the Jacobian is expressed in scaled space; unscaled analytic partials are converted with the constant scaler slopes `scaler.get_scale()` (see [Derivative Computation](../../framework-architecture/derivative-computation.md)). The method **returns** the Jacobian as `List[List[float | None]]`; any entry (or the whole return value) left as `None` prompts an internal finite-difference approximation.
- `def evaluate_Hessians_EqualityLocalConstraints()` > analogously, methods that additionally need curvature (e.g. [abbr:ALADIN](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/aladin.md)) require the second-order derivatives (Hessians) of ${}^{i}$sym:v_h with respect to ${}^{i}$sym:d. This method **returns** one scaled-space Hessian per equality constraint as `List[List[List[float | None]]]`, or `None` (fully or per entry) to prompt the framework's internal BFGS / finite-difference approximation ([Derivative Computation](../../framework-architecture/derivative-computation.md)).
- `def evaluateInEqualityLocalConstraints()` > implements ${}^{i}$sym:v_g
- `def evaluate_Jacobian_InEqualityLocalConstraints()` > analogously to the equality case, this returns the scaled-space Jacobian of the local inequality constraints ${}^{i}$sym:v_g with respect to ${}^{i}$sym:d as `List[List[float | None]]`; any entry (or the whole return value) left as `None` prompts an internal finite-difference approximation ([Derivative Computation](../../framework-architecture/derivative-computation.md)).
- `def evaluate_Hessians_InEqualityLocalConstraints()` > **returns** one scaled-space Hessian per inequality constraint as `List[List[List[float | None]]]`, or `None` (fully or per entry) to prompt the framework's internal BFGS / finite-difference approximation ([Derivative Computation](../../framework-architecture/derivative-computation.md)).

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, this reads as follows:

<div class="collapsible-code" markdown>

```python
class LocalConstraints0(LocalConstraintsInterface):
    """Local constraints class for Subsystem 0 (Aircraft) in the Supersonic Business Jet (SSBJ) problem.

    Implements the LocalConstraintsInterface to define the range inequality
    constraint of Subsystem 0 (Aircraft).

    Attributes:
        None specific to this class; inherits from LocalConstraintsInterface.
    """
    def __init__(self) -> None:
        """Initialize the LocalConstraints0 instance."""
        pass

    def evaluateEqualityLocalConstraints(self, subsystemin: LocalSubSystemBasis) -> None:
        """Evaluate equality local constraints for Subsystem 0.

        Computes the equality constraint values from the subsystem responses,
        scales them using the appropriate ScalerConstraint, and stores the
        result in the subsystem.

        Args:
            subsystemin: The local subsystem instance providing responses
                and scaling variables.
        """
        responses: List[float] = subsystemin.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystemin.get_Scalers()
        
        equality_unscaled = []        
        # append any equality local constraints to this list using the responses        
        ################################################################
        ###          USER CODE: Equality constraints                  ###
        ################################################################
        # equality_unscaled.append(responses[...])
        # equality_unscaled.append(responses[...])  
        
        # scale equality local constraint evaluation
        # scl: List[ScalerConstraint] = [scalers[...]]
        # equality: List[float] = [scl[i].transform(equality_unscaled[i]) for i in range(len(equality_unscaled))]
        
        # or if no equality local constraints exist:
        equality = None
       
        # equality local constraints needs to be a scaled01 quantity        
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################       
        subsystemin.set_EqualityLocalConstraintsValue(equality)
        
    def evaluate_Jacobian_EqualityLocalConstraints(self, subsystemin: LocalSubSystemBasis) -> List[List[float | None]] | None :
        """Evaluate the Jacobian of equality local constraints.

        Args:
            subsystemin: The local subsystem instance.

        Returns:
            Jacobian matrix of equality constraints with respect to design
            variables, or None if not provided (finite differences used).
        """
        
        return None
    
    def evaluate_Hessians_EqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> List[List[List[float | None]]] | None:
        """Evaluate the Hessians of equality local constraints.

        Args:
            subsystem: The local subsystem instance.

        Returns:
            List of Hessian matrices (one per constraint) with respect to
            design variables, or None if not provided.
        """
        
        return None    
        
    def evaluateInEqualityLocalConstraints(self, subsystemin: LocalSubSystemBasis) -> None:
        """Evaluate inequality local constraints for Subsystem 0.

        Computes the inequality constraint values from the subsystem responses,
        scales them using the appropriate ScalerConstraint, and stores the
        result in the subsystem.

        Args:
            subsystemin: The local subsystem instance providing responses
                and scaling variables.
        """
        responses: List[float] = subsystemin.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystemin.get_Scalers()
        
        inequality_unscaled = []
        # append any inequality local constraints to this list using the responses
        ################################################################
        ###          USER CODE: Inequality constraints               ###
        ################################################################
        range_value = responses[0]  # [nmi]

        inequality_unscaled.append(-range_value / 2000.0 + 1.0)  # range constraint (range >= 2000 [nmi])

        # scale the inequality local constraint evaluation
        scl: List[ScalerConstraint] = [scalers[7]]
        inequality: List[float] = [scl[i].transform(inequality_unscaled[i]) for i in range(len(inequality_unscaled))]
        
        # or if no inequality local constraints exist:
        # inequality = None
        
        # inequality local constraints needs to be a scaled01 quantity        
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        subsystemin.set_InEqualityLocalConstraintsValue(inequality)

    def evaluate_Jacobian_InEqualityLocalConstraints(self, subsystemin: LocalSubSystemBasis) -> List[List[float | None]] | None :
        """Evaluate the Jacobian of inequality local constraints.

        Args:
            subsystemin: The local subsystem instance.

        Returns:
            Jacobian matrix of inequality constraints with respect to design
            variables, or None if not provided (finite differences used).
        """
        
        return None
    
    def evaluate_Hessians_InEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> List[List[List[float | None]]] | None:
        """Evaluate the Hessians of inequality local constraints.

        Args:
            subsystem: The local subsystem instance.

        Returns:
            List of Hessian matrices (one per constraint) with respect to
            design variables, or None if not provided.
        """
        
        return None
```

</div>
<br/>

<div class="collapsible-code" markdown>

```python
class LocalConstraints1(LocalConstraintsInterface):
    """Local constraints class for Subsystem 1 (Propulsion) in the Supersonic Business Jet (SSBJ) problem.

    Implements the LocalConstraintsInterface to define the engine-temperature
    and throttle-setting inequality constraints of Subsystem 1 (Propulsion).

    Attributes:
        None specific to this class; inherits from LocalConstraintsInterface.
    """
    def __init__(self) -> None:
        """Initialize the LocalConstraints1 instance."""
        pass

    def evaluateEqualityLocalConstraints(self, subsystemin: LocalSubSystemBasis) -> None:
        """Evaluate equality local constraints for Subsystem 1.

        Computes the equality constraint values from the subsystem responses,
        scales them using the appropriate ScalerConstraint, and stores the
        result in the subsystem.

        Args:
            subsystemin: The local subsystem instance providing responses
                and scaling variables.
        """
        responses: List[float] = subsystemin.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystemin.get_Scalers()
        
        equality_unscaled = []        
        # append any equality local constraints to this list using the responses        
        ################################################################
        ###          USER CODE: Equality constraints                  ###
        ################################################################
        # equality_unscaled.append(responses[...])
        # equality_unscaled.append(responses[...])  
        
        # scale equality local constraint evaluation
        # scl: List[ScalerConstraint] = [scalers[...]]
        # equality: List[float] = [scl[i].transform(equality_unscaled[i]) for i in range(len(equality_unscaled))]
        
        # or if no equality local constraints exist:
        equality = None
       
        # equality local constraints needs to be a scaled01 quantity        
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################       
        subsystemin.set_EqualityLocalConstraintsValue(equality)

    def evaluate_Jacobian_EqualityLocalConstraints(self, subsystemin: LocalSubSystemBasis) -> List[List[float | None]] | None :
        """Evaluate the Jacobian of equality local constraints.

        Args:
            subsystemin: The local subsystem instance.

        Returns:
            Jacobian matrix of equality constraints with respect to design
            variables, or None if not provided (finite differences used).
        """
        
        return None
    
    def evaluate_Hessians_EqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> List[List[List[float | None]]] | None:
        """Evaluate the Hessians of equality local constraints.

        Args:
            subsystem: The local subsystem instance.

        Returns:
            List of Hessian matrices (one per constraint) with respect to
            design variables, or None if not provided.
        """
        
        return None

    def evaluateInEqualityLocalConstraints(self, subsystemin: LocalSubSystemBasis) -> None:
        """Evaluate inequality local constraints for Subsystem 1.

        Computes the inequality constraint values from the subsystem responses,
        scales them using the appropriate ScalerConstraint, and stores the
        result in the subsystem.

        Args:
            subsystemin: The local subsystem instance providing responses
                and scaling variables.
        """
        responses: List[float] = subsystemin.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystemin.get_Scalers()
        
        inequality_unscaled = []
        # append any inequality local constraints to this list using the responses
        ################################################################
        ###          USER CODE: Inequality constraints                ###
        ################################################################
        engine_temperature = responses[0]  # [-]
        dim_throttle = responses[1]        # [lb]
        throttle_uA = responses[2]         # [lb]

        inequality_unscaled.append(engine_temperature/1.02 - 1.0)   # engine temperature constraint (engine_temperature [-])
        inequality_unscaled.append(dim_throttle/throttle_uA - 1.0)  # throttle setting constraint (dim_throttle/throttle_uA [-])
        
        # scale the inequality local constraint evaluation
        scl: List[ScalerConstraint] = scalers[4:6]
        inequality: List[float] = [scl[i].transform(inequality_unscaled[i]) for i in range(len(inequality_unscaled))]
        
        # or if no inequality local constraints exist:
        # inequality = None
        
        # inequality local constraints needs to be a scaled01 quantity        
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        subsystemin.set_InEqualityLocalConstraintsValue(inequality)

    def evaluate_Jacobian_InEqualityLocalConstraints(self, subsystemin: LocalSubSystemBasis) -> List[List[float | None]] | None :
        """Evaluate the Jacobian of inequality local constraints.

        Args:
            subsystemin: The local subsystem instance.

        Returns:
            Jacobian matrix of inequality constraints with respect to design
            variables, or None if not provided (finite differences used).
        """
        
        return None
    
    def evaluate_Hessians_InEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> List[List[List[float | None]]] | None:
        """Evaluate the Hessians of inequality local constraints.

        Args:
            subsystem: The local subsystem instance.

        Returns:
            List of Hessian matrices (one per constraint) with respect to
            design variables, or None if not provided.
        """
        
        return None
```

</div>
<br/>

<div class="collapsible-code" markdown>

```python
class LocalConstraints2(LocalConstraintsInterface):
    """Local constraints class for Subsystem 2 (Aerodynamics) in the Supersonic Business Jet (SSBJ) problem.

    Implements the LocalConstraintsInterface to define the pressure-gradient and
    lift-coefficient inequality constraints of Subsystem 2 (Aerodynamics).

    Attributes:
        None specific to this class; inherits from LocalConstraintsInterface.
    """
    def __init__(self) -> None:
        """Initialize the LocalConstraints2 instance."""
        pass

    def evaluateEqualityLocalConstraints(self, subsystemin: LocalSubSystemBasis) -> None:
        """Evaluate equality local constraints for Subsystem 2.

        Computes the equality constraint values from the subsystem responses,
        scales them using the appropriate ScalerConstraint, and stores the
        result in the subsystem.

        Args:
            subsystemin: The local subsystem instance providing responses
                and scaling variables.
        """
        responses: List[float] = subsystemin.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystemin.get_Scalers()
        
        equality_unscaled = []        
        # append any equality local constraints to this list using the responses        
        ################################################################
        ###          USER CODE: Equality constraints                  ###
        ################################################################
        # equality_unscaled.append(responses[...])
        # equality_unscaled.append(responses[...])  
        
        # scale equality local constraint evaluation
        # scl: List[ScalerConstraint] = [scalers[...]]
        # equality: List[float] = [scl[i].transform(equality_unscaled[i]) for i in range(len(equality_unscaled))]
        
        # or if no equality local constraints exist:
        equality = None
       
        # equality local constraints needs to be a scaled01 quantity        
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################       
        subsystemin.set_EqualityLocalConstraintsValue(equality)
        
    def evaluate_Jacobian_EqualityLocalConstraints(self, subsystemin: LocalSubSystemBasis) -> List[List[float | None]] | None :
        """Evaluate the Jacobian of equality local constraints.

        Args:
            subsystemin: The local subsystem instance.

        Returns:
            Jacobian matrix of equality constraints with respect to design
            variables, or None if not provided (finite differences used).
        """
        
        return None
    
    def evaluate_Hessians_EqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> List[List[List[float | None]]] | None:
        """Evaluate the Hessians of equality local constraints.

        Args:
            subsystem: The local subsystem instance.

        Returns:
            List of Hessian matrices (one per constraint) with respect to
            design variables, or None if not provided.
        """
        
        return None
        
    def evaluateInEqualityLocalConstraints(self, subsystemin: LocalSubSystemBasis) -> None:
        """Evaluate inequality local constraints for Subsystem 2.

        Computes the inequality constraint values from the subsystem responses,
        scales them using the appropriate ScalerConstraint, and stores the
        result in the subsystem.

        Args:
            subsystemin: The local subsystem instance providing responses
                and scaling variables.
        """
        responses: List[float] = subsystemin.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystemin.get_Scalers()
        
        inequality_unscaled = []
        # append any inequality local constraints to this list using the responses
        ################################################################
        ###          USER CODE: Inequality constraints                ###
        ################################################################
        pressure_gradient = responses[0]       # adverse pressure gradient factor [-]
        wing_lift_coefficient = responses[1]   # wing lift coefficient [-]
        tail_lift_coefficient = responses[2]   # tail lift coefficient [-]

        inequality_unscaled.append(pressure_gradient/1.1 - 1.0)  # g0 pressure gradient constraint [-] (Pg <= 1.1)
        inequality_unscaled.append((2 * tail_lift_coefficient) - wing_lift_coefficient)  # g1 lift coefficient constraint 1 [-]
        inequality_unscaled.append((2 * (-tail_lift_coefficient)) - wing_lift_coefficient)  # g2 lift coefficient constraint 2 [-]

        # scale the inequality local constraint evaluation
        scl: List[ScalerConstraint] = scalers[14:17]
        inequality: List[float] = [scl[i].transform(inequality_unscaled[i]) for i in range(len(inequality_unscaled))]
        
        # or if no inequality local constraints exist:
        # inequality = None
        
        # inequality local constraints needs to be a scaled01 quantity        
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        subsystemin.set_InEqualityLocalConstraintsValue(inequality)

    def evaluate_Jacobian_InEqualityLocalConstraints(self, subsystemin: LocalSubSystemBasis) -> List[List[float | None]] | None :
        """Evaluate the Jacobian of inequality local constraints.

        Args:
            subsystemin: The local subsystem instance.

        Returns:
            Jacobian matrix of inequality constraints with respect to design
            variables, or None if not provided (finite differences used).
        """
        
        return None
    
    def evaluate_Hessians_InEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> List[List[List[float | None]]] | None:
        """Evaluate the Hessians of inequality local constraints.

        Args:
            subsystem: The local subsystem instance.

        Returns:
            List of Hessian matrices (one per constraint) with respect to
            design variables, or None if not provided.
        """
        
        return None
```

</div>
<br/>

<div class="collapsible-code" markdown>

```python
class LocalConstraints3(LocalConstraintsInterface):
    """Local constraints class for Subsystem 3 (Structure) in the Supersonic Business Jet (SSBJ) problem.

    Implements the LocalConstraintsInterface to define the structural inequality
    constraints (stress, buckling, h_spar margin and absolute gauge bounds) of
    Subsystem 3 (Structure). Requires `import numpy as np`.

    Attributes:
        None specific to this class; inherits from LocalConstraintsInterface.
    """
    def __init__(self) -> None:
        """Initialize the LocalConstraints3 instance."""
        pass

    def evaluateEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate equality local constraints for Subsystem 3."""
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()

        equality_unscaled = []
        ################################################################
        ###          USER CODE: Equality constraints                 ###
        ################################################################

        # no equality local constraints exist:
        equality = None

        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        subsystem.set_EqualityLocalConstraintsValue(equality)

    def evaluate_Jacobian_EqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Jacobian of the local equality constraints."""
        return None

    def evaluate_Hessians_EqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessians of the local equality constraints."""
        return None

    def evaluateInEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate inequality local constraints for Subsystem 3.

        Computes the structural inequality constraint values from the subsystem
        responses, scales them using the appropriate ScalerConstraint, and stores
        the result in the subsystem.

        Args:
            subsystem: The local subsystem instance providing responses
                and scaling variables.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()

        inequality_unscaled = []
        ################################################################
        ###          USER CODE: Inequality constraints               ###
        ################################################################

        # Unpack flattened response arrays (each variable covers 3 panels)
        # sig_1..sig_6: bending stresses, indices 0:18 [lb/ft^2]
        sig_1   = np.array(responses[0:3])
        sig_2   = np.array(responses[3:6])
        sig_3   = np.array(responses[6:9])
        sig_4   = np.array(responses[9:12])
        sig_5   = np.array(responses[12:15])
        sig_6   = np.array(responses[15:18])
        # sig_cr/tau_cr: critical buckling normal/shear stresses, indices 18:42 [lb/ft^2]
        sig_cr1 = np.array(responses[18:21])
        tau_cr1 = np.array(responses[21:24])
        sig_cr2 = np.array(responses[24:27])
        tau_cr2 = np.array(responses[27:30])
        sig_cr3 = np.array(responses[30:33])
        tau_cr3 = np.array(responses[33:36])
        sig_cr5 = np.array(responses[36:39])
        tau_cr5 = np.array(responses[39:42])
        # tau/sig_eq: shear stresses & von Mises equivalent stresses, indices 42:72 [lb/ft^2]
        tau1    = np.array(responses[42:45])
        sig_eq1 = np.array(responses[45:48])
        tau2    = np.array(responses[48:51])
        sig_eq2 = np.array(responses[51:54])
        tau3    = np.array(responses[54:57])
        sig_eq3 = np.array(responses[57:60])
        sig_eq4 = np.array(responses[60:63])
        tau5    = np.array(responses[63:66])
        sig_eq5 = np.array(responses[66:69])
        sig_eq6 = np.array(responses[69:72])
        # h_spar at index 72:75 [ft], thickness arrays: indices 75:93 [ft]
        h_spar = np.array(responses[72:75])
        t1  = np.array(responses[75:78])
        t2  = np.array(responses[78:81])
        t3  = np.array(responses[81:84])
        ts1 = np.array(responses[84:87])
        ts2 = np.array(responses[87:90])
        ts3 = np.array(responses[90:93])
        # allowable compressive / tensile stresses [lb/ft^2] (65000 psi * 144)
        Sig_C = 65000.0 * 144.0
        Sig_T = 65000.0 * 144.0

        k = 6.09375

        # Magnitude-compressed ratio constraints of the form EXPR - 1 <= 0, where the raw ratio
        # EXPR is replaced by its power image sign(EXPR)*|EXPR|**exponent. This strictly-increasing
        # map preserves the zero-crossing (|EXPR| = 1 -> 0) and sign, so the feasible set is
        # unchanged while extreme magnitudes at infeasible designs are compressed.
        def power_ratio(expr: np.ndarray, exponent: float) -> np.ndarray:
            """Return sign(expr)*|expr|**exponent: magnitude-compressed, sign/zero-crossing preserving."""
            expr = np.asarray(expr, dtype=float)
            return np.sign(expr) * np.abs(expr)**exponent

        # G1[0:3]   – compressive stress point 1
        inequality_unscaled.extend((power_ratio((k * sig_eq1) / Sig_C, 1.0 / 4.0) - 1).tolist())
        # G1[3:6]   – buckling point 1 (compressive)
        inequality_unscaled.extend((power_ratio(k * (sig_1 / sig_cr1 + (tau1 / tau_cr1)**2), 1.0 / 4.0) - 1).tolist())
        # G1[6:9]   – buckling point 1 (shear)
        inequality_unscaled.extend((power_ratio(k * (-sig_1 / sig_cr1 + (tau1 / tau_cr1)**2), 1.0 / 4.0) - 1).tolist())
        # G1[9:12]  – compressive stress point 2
        inequality_unscaled.extend((power_ratio((k * sig_eq2) / Sig_C, 1.0 / 4.0) - 1).tolist())
        # G1[12:15] – buckling point 2 (compressive)
        inequality_unscaled.extend((power_ratio(k * (sig_2 / sig_cr2 + (tau2 / tau_cr2)**2), 1.0 / 8.0) - 1).tolist())
        # G1[15:18] – buckling point 2 (shear)
        inequality_unscaled.extend((power_ratio(k * (-sig_2 / sig_cr2 + (tau2 / tau_cr2)**2), 1.0 / 8.0) - 1).tolist())
        # G1[18:21] – compressive stress point 3
        inequality_unscaled.extend((power_ratio((k * sig_eq3) / Sig_C, 1.0 / 4.0) - 1).tolist())
        # G1[21:24] – buckling point 3 (compressive)
        inequality_unscaled.extend((power_ratio(k * (sig_3 / sig_cr3 + (tau3 / tau_cr3)**2), 1.0 / 4.0) - 1).tolist())
        # G1[24:27] – buckling point 3 (shear)
        inequality_unscaled.extend((power_ratio(k * (-sig_3 / sig_cr3 + (tau3 / tau_cr3)**2), 1.0 / 4.0) - 1).tolist())
        # G1[27:30] – tensile stress point 4
        inequality_unscaled.extend((power_ratio((k * sig_eq4) / Sig_T, 1.0 / 4.0) - 1).tolist())
        # G1[30:33] – tensile stress point 5
        inequality_unscaled.extend((power_ratio((k * sig_eq5) / Sig_T, 1.0 / 4.0) - 1).tolist())
        # G1[33:36] – buckling point 5 (compressive)
        inequality_unscaled.extend((power_ratio(k * (sig_5 / sig_cr5 + (tau5 / tau_cr5)**2), 1.0 / 8.0) - 1).tolist())
        # G1[36:39] – buckling point 5 (shear)
        inequality_unscaled.extend((power_ratio(k * (-sig_5 / sig_cr5 + (tau5 / tau_cr5)**2), 1.0 / 8.0) - 1).tolist())
        # G1[39:42] – tensile stress point 6
        inequality_unscaled.extend((power_ratio((k * sig_eq6) / Sig_T, 1.0 / 4.0) - 1).tolist())
        # Sign-flip stress families share the same EXPR - 1 <= 0 structure and power map.
        # G1[54:57] – tensile stress point 1 (sign flip)
        inequality_unscaled.extend((power_ratio(-(k * sig_eq1) / Sig_C, 1.0 / 4.0) - 1).tolist())
        # G1[57:60] – tensile stress point 2 (sign flip)
        inequality_unscaled.extend((power_ratio(-(k * sig_eq2) / Sig_C, 1.0 / 4.0) - 1).tolist())
        # G1[60:63] – tensile stress point 3 (sign flip)
        inequality_unscaled.extend((power_ratio(-(k * sig_eq3) / Sig_C, 1.0 / 4.0) - 1).tolist())
        # G1[63:66] – compressive stress point 4 (sign flip)
        inequality_unscaled.extend((power_ratio(-(k * sig_eq4) / Sig_T, 1.0 / 4.0) - 1).tolist())
        # G1[66:69] – compressive stress point 5 (sign flip)
        inequality_unscaled.extend((power_ratio(-(k * sig_eq5) / Sig_T, 1.0 / 4.0) - 1).tolist())
        # G1[69:72] – compressive stress point 6 (sign flip)
        inequality_unscaled.extend((power_ratio(-(k * sig_eq6) / Sig_T, 1.0 / 4.0) - 1).tolist())

        # h_spar margin (one per spanwise station): alpha1_i + alpha3_i - 0.5 <= 0
        hspar_margin = np.array(responses[93:96])
        inequality_unscaled.extend(hspar_margin.tolist())

        # Absolute-gauge inequalities (lower and upper) in feet: 0.1 in = 0.1/12 ft, 9 in = 9/12 ft,
        # 4 in = 4/12 ft. ts2 keeps its hard box bound, so only its skin t2 needs a gauge pair.
        ts_lo = 0.1 / 12.0   # 0.1 in in feet
        ts_hi = 9.0 / 12.0   # 9.0 in in feet
        t_lo  = 0.1 / 12.0   # 0.1 in in feet
        t_hi  = 4.0 / 12.0   # 4.0 in in feet
        # top sandwich ts1: lower then upper
        inequality_unscaled.extend((ts_lo - ts1).tolist())
        inequality_unscaled.extend((ts1 - ts_hi).tolist())
        # bottom sandwich ts3: lower then upper
        inequality_unscaled.extend((ts_lo - ts3).tolist())
        inequality_unscaled.extend((ts3 - ts_hi).tolist())
        # skin t1: lower then upper
        inequality_unscaled.extend((t_lo - t1).tolist())
        inequality_unscaled.extend((t1 - t_hi).tolist())
        # skin t2: lower then upper
        inequality_unscaled.extend((t_lo - t2).tolist())
        inequality_unscaled.extend((t2 - t_hi).tolist())
        # skin t3: lower then upper
        inequality_unscaled.extend((t_lo - t3).tolist())
        inequality_unscaled.extend((t3 - t_hi).tolist())

        # scale the inequality local constraint evaluation
        # 93 inequality constraints (72 - 12 removed + 33 added) -> scalers[28:121]
        scl: List[ScalerConstraint] = scalers[28:121]
        inequality: List[float] = [scl[i].transform(inequality_unscaled[i]) for i in range(len(inequality_unscaled))]

        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        subsystem.set_InequalityLocalConstraintsValue(inequality)

    def evaluate_Jacobian_InEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Jacobian of the local inequality constraints."""
        return None

    def evaluate_Hessians_InEqualityLocalConstraints(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessians of the local inequality constraints."""
        return None
```

</div>


## 6. Defining the LocalObjective<id>.py

[Step 2.](index.md#2-creation-of-folder-holding-all-use-case-specific-files) previously created `LocalObjective<id>.py` files and classes for each subsystem. 
The following class methods of each `LocalObjective<id>` need to be detailed:

- `def evaluateLocalObjective()` > implements ${}^{i}$sym:v_f
- `def evaluate_Gradient_LocalObjective()` > some coordination methods (e.g. [abbr:ALADIN](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/aladin.md) and [abbr:SBDP](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/sensitivity-based-distributed-programming.md)) require the first-order derivative (gradient) of the local objective ${}^{i}$sym:v_f with respect to the design variables ${}^{i}$sym:d. Because the optimizer operates in the scaled $[0, 1]$ domain, the gradient is expressed in scaled space; unscaled analytic partials are converted with the constant scaler slopes `scaler.get_scale()` (see [Derivative Computation](../../framework-architecture/derivative-computation.md)). The method **returns** the gradient as `List[float | None]`; any entry (or the whole return value) left as `None` prompts an internal finite-difference approximation.
- `def evaluate_Hessian_LocalObjective()` > analogously, methods that additionally need curvature (e.g. [abbr:ALADIN](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/aladin.md)) require the second-order derivative (Hessian) of ${}^{i}$sym:v_f with respect to ${}^{i}$sym:d. This method **returns** the scaled-space Hessian as `List[List[float | None]]`, or `None` (fully or per entry) to prompt the framework's internal BFGS / finite-difference approximation ([Derivative Computation](../../framework-architecture/derivative-computation.md)).

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, this reads as follows:

<div class="collapsible-code" markdown>

```python
class LocalObjective0(LocalObjectiveInterface):
    """Local objective class for Subsystem 0 (Aircraft) in the Supersonic Business Jet (SSBJ) problem.

    Implements the LocalObjectiveInterface to compute the local objective of
    Subsystem 0 (Aircraft): the total aircraft weight to be minimized.

    Attributes:
        None specific to this class; inherits from LocalObjectiveInterface.
    """
    def __init__(self) -> None:
        """Initialize the LocalObjective0 instance."""
        pass
    
    def evaluateLocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the local objective function for Subsystem 0.

        Computes the local objective value from the subsystem responses,
        scales it using the appropriate scaler, and stores the result
        in the subsystem.

        Args:
            subsystem: The local subsystem instance providing responses
                and scaling variables.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Local objective                      ###
        ################################################################
        # compute local objective
 
        localobjective_unscaled = responses[1]  # total_weight [lb]
            
        # scale the local objective function evaluation
        localobjective = scalers[5].transform(localobjective_unscaled)
        
        # or if no Local objective exist:
        # localobjective = None
        
        # localobjective needs to be a scaled01 quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################     
        subsystem.set_LocalObjectiveValue(localobjective)

    def evaluate_Gradient_LocalObjective(self, subsystem) -> List[float | None] | None:
        """Evaluate the gradient of the local objective function.

        Args:
            subsystem: The local subsystem instance.

        Returns:
            Gradient vector of the local objective with respect to design
            variables, or None if not provided (finite differences used).
        """
        
        return None
    
    def evaluate_Hessian_LocalObjective(self, subsystem) -> List[List[float | None]] | None:
        """Evaluate the Hessian of the local objective function.

        Args:
            subsystem: The local subsystem instance.

        Returns:
            Hessian matrix of the local objective with respect to design
            variables, or None if not provided.
        """
        
        return None
```

</div>
<br/>

<div class="collapsible-code" markdown>

```python
class LocalObjective1(LocalObjectiveInterface):
    """Local objective class for Subsystem 1 (Propulsion) in the Supersonic Business Jet (SSBJ) problem.

    Implements the LocalObjectiveInterface for Subsystem 1 (Propulsion).
    This subsystem has no local objective (set to None).

    Attributes:
        None specific to this class; inherits from LocalObjectiveInterface.
    """
    def __init__(self) -> None:
        """Initialize the LocalObjective1 instance."""
        pass

    def evaluateLocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the local objective function for Subsystem 1.

        Computes the local objective value from the subsystem responses,
        scales it using the appropriate scaler, and stores the result
        in the subsystem.

        Args:
            subsystem: The local subsystem instance providing responses
                and scaling variables.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Local objective                      ###
        ################################################################
        # compute local objective
 
        # localobjective_unscaled = responses[...]
            
        # scale the local objective function evaluation
        # localobjective = scalers[...].transform(localobjective_unscaled)
        
        # or if no Local objective exist:
        localobjective = None
        
        # localobjective needs to be a scaled01 quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################        
        subsystem.set_LocalObjectiveValue(localobjective)

    def evaluate_Gradient_LocalObjective(self, subsystem) -> List[float | None] | None:
        """Evaluate the gradient of the local objective function.

        Args:
            subsystem: The local subsystem instance.

        Returns:
            Gradient vector of the local objective with respect to design
            variables, or None if not provided (finite differences used).
        """
        
        return None
    
    def evaluate_Hessian_LocalObjective(self, subsystem) -> List[List[float | None]] | None:
        """Evaluate the Hessian of the local objective function.

        Args:
            subsystem: The local subsystem instance.

        Returns:
            Hessian matrix of the local objective with respect to design
            variables, or None if not provided.
        """
        
        return None
```

</div>
<br/>

<div class="collapsible-code" markdown>

```python
class LocalObjective2(LocalObjectiveInterface):
    """Local objective class for Subsystem 2 (Aerodynamics) in the Supersonic Business Jet (SSBJ) problem.

    Implements the LocalObjectiveInterface for Subsystem 2 (Aerodynamics).
    This subsystem has no local objective (set to None).

    Attributes:
        None specific to this class; inherits from LocalObjectiveInterface.
    """
    def __init__(self) -> None:
        """Initialize the LocalObjective2 instance."""
        pass

    def evaluateLocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the local objective function for Subsystem 2.

        Computes the local objective value from the subsystem responses,
        scales it using the appropriate scaler, and stores the result
        in the subsystem.

        Args:
            subsystem: The local subsystem instance providing responses
                and scaling variables.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Local objective                      ###
        ################################################################
        # compute local objective
 
        # localobjective_unscaled = responses[...]
            
        # scale the local objective function evaluation
        # localobjective = scalers[...].transform(localobjective_unscaled)
        
        # or if no Local objective exist:
        localobjective = None
        
        # localobjective needs to be a scaled01 quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        subsystem.set_LocalObjectiveValue(localobjective)

    def evaluate_Gradient_LocalObjective(self, subsystem) -> List[float | None] | None:
        """Evaluate the gradient of the local objective function.

        Args:
            subsystem: The local subsystem instance.

        Returns:
            Gradient vector of the local objective with respect to design
            variables, or None if not provided (finite differences used).
        """
        
        return None
    
    def evaluate_Hessian_LocalObjective(self, subsystem) -> List[List[float | None]] | None:
        """Evaluate the Hessian of the local objective function.

        Args:
            subsystem: The local subsystem instance.

        Returns:
            Hessian matrix of the local objective with respect to design
            variables, or None if not provided.
        """
        
        return None
```

</div>
<br/>

<div class="collapsible-code" markdown>

```python
class LocalObjective3(LocalObjectiveInterface):
    """Local objective class for Subsystem 3 (Structure) in the Supersonic Business Jet (SSBJ) problem.

    Implements the LocalObjectiveInterface for Subsystem 3 (Structure).
    This subsystem has no local objective (set to None).

    Attributes:
        None specific to this class; inherits from LocalObjectiveInterface.
    """

    def __init__(self) -> None:
        """Initialize LocalObjective3 instance."""
        pass

    def evaluateLocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the local objective function for Subsystem 3.

        Args:
            subsystem: The local subsystem instance providing responses
                and scaling variables.
        """
        responses: List[float] = subsystem.get_Responses_Unscaled()  # unscaled values
        scalers: List[ScalerBasis] = subsystem.get_Scalers()
        ################################################################
        ###          USER CODE: Local objective                      ###
        ################################################################
        # no local objective exists:
        localobjective = None

        # localobjective needs to be a scaled01 quantity
        ################################################################
        ###          END USER CODE                                   ###
        ################################################################
        subsystem.set_LocalObjectiveValue(localobjective)

    def evaluate_Gradient_LocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the gradient of the local objective function.

        Args:
            subsystem: Local subsystem instance.
        """
        return None

    def evaluate_Hessian_LocalObjective(self, subsystem: LocalSubSystemBasis) -> None:
        """Evaluate the Hessian of the local objective function.

        Args:
            subsystem: Local subsystem instance.
        """
        return None
```

</div>

## 7. Defining the Optimization<id>.py

[Step 2.](index.md#2-creation-of-folder-holding-all-use-case-specific-files) previously created `Optimization<id>.py` files and classes for each subsystem. 
A suitable solver (including its hyperparameters) must be chosen for solving the optimization problem of each subsystem.

In case of the [SSBJ](../../examples/SSBJ/index.md) Example, this reads as follows:

<div class="collapsible-code" markdown>

```python
class Optimization0(OptimizationBasis):
    """Optimization configuration class for Subsystem 0.

    Configures the local optimization algorithm (PyNomadBBO by default) for
    solving the subproblem of Subsystem 0 (Aircraft) in the Supersonic Business Jet (SSBJ) problem.

    Attributes:
        _optimizer: The optimization algorithm instance configured with
            appropriate hyperparameters for this subsystem.
    """
    def __init__(self) -> None:
        """Initialize the Optimization0 instance with the selected optimizer."""

        # Choose your optimizer and its hyperparameters

        # super().__init__(Solver_SCBO(option_1=None))

        # super().__init__(Solver_Scipy(method="trust-constr",
        #                               constraint_jac="2-point",
        #                               constraint_keep_feasible=False,
        #                               maxiter=None))

        super().__init__(Solver_PyNomadBBO(maxevals=10000,
                                           constraint_handling_method="PB",
                                           seed=1,
                                           vns_mads_search=False,
                                           quad_model_search=False,
                                           eqcon_as_ineqcon_tol=1E-8))

        # super().__init__(Solver_IPOPT(maxiter=1000,
        #                               acceptable_tol=1e-8,
        #                               constraint_jac="2-point",
        #                               constraint_keep_feasible=False))

        # super().__init__(Solver_Pyomo(option_1=None,
        #                               option_2=None))

        # super().__init__(Solver_Fmincon(method="active_set",
        #                                 maxiter=1000,
        #                                 maxfunevals=10000,
        #                                 tolfun=1e-8,
        #                                 tolcon=1e-8))
```

</div>
<br/>

<div class="collapsible-code" markdown>

```python
class Optimization1(OptimizationBasis):
    """Optimization configuration class for Subsystem 1.

    Configures the local optimization algorithm (PyNomadBBO by default) for
    solving the subproblem of Subsystem 1 (Propulsion) in the Supersonic Business Jet (SSBJ) problem.

    Attributes:
        _optimizer: The optimization algorithm instance configured with
            appropriate hyperparameters for this subsystem.
    """
    def __init__(self) -> None:
        """Initialize the Optimization1 instance with the selected optimizer."""

        # Choose your optimizer and its hyperparameters

        # super().__init__(Solver_SCBO(option_1=None))

        # super().__init__(Solver_Scipy(method="trust-constr",
        #                               constraint_jac="2-point",
        #                               constraint_keep_feasible=False,
        #                               maxiter=None))

        super().__init__(Solver_PyNomadBBO(maxevals=10000,
                                           constraint_handling_method="PB",
                                           seed=1,
                                           vns_mads_search=False,
                                           quad_model_search=False,
                                           eqcon_as_ineqcon_tol=1E-8))

        # super().__init__(Solver_IPOPT(maxiter=1000,
        #                               acceptable_tol=1e-8,
        #                               constraint_jac="2-point",
        #                               constraint_keep_feasible=False))

        # super().__init__(Solver_Pyomo(option_1=None,
        #                               option_2=None))

        # super().__init__(Solver_Fmincon(method="active_set",
        #                                 maxiter=1000,
        #                                 maxfunevals=10000,
        #                                 tolfun=1e-8,
        #                                 tolcon=1e-8))
```

</div>
<br/>

<div class="collapsible-code" markdown>

```python
class Optimization2(OptimizationBasis):
    """Optimization configuration class for Subsystem 2.

    Configures the local optimization algorithm (PyNomadBBO by default) for
    solving the subproblem of Subsystem 2 (Aerodynamics) in the Supersonic Business Jet (SSBJ) problem.

    Attributes:
        _optimizer: The optimization algorithm instance configured with
            appropriate hyperparameters for this subsystem.
    """
    def __init__(self) -> None:
        """Initialize the Optimization2 instance with the selected optimizer."""

        # Choose your optimizer and its hyperparameters

        # super().__init__(Solver_SCBO(option_1=None))

        # super().__init__(Solver_Scipy(method="trust-constr",
        #                               constraint_jac="2-point",
        #                               constraint_keep_feasible=False,
        #                               maxiter=None))

        super().__init__(Solver_PyNomadBBO(maxevals=20000,
                                           constraint_handling_method="PB",
                                           seed=1,
                                           vns_mads_search=False,
                                           quad_model_search=False,
                                           eqcon_as_ineqcon_tol=1E-8))

        # super().__init__(Solver_IPOPT(maxiter=1000,
        #                               acceptable_tol=1e-8,
        #                               constraint_jac="2-point",
        #                               constraint_keep_feasible=False))

        # super().__init__(Solver_Pyomo(option_1=None,
        #                               option_2=None))

        # super().__init__(Solver_Fmincon(method="active_set",
        #                                 maxiter=1000,
        #                                 maxfunevals=10000,
        #                                 tolfun=1e-8,
        #                                 tolcon=1e-8))
```

</div>
<br/>

<div class="collapsible-code" markdown>

```python
class Optimization3(OptimizationBasis):
    """Optimization configuration class for Subsystem 3.

    Configures the local optimization algorithm (PyNomadBBO by default) for
    solving the subproblem of Subsystem 3 (Structure) in the Supersonic Business Jet (SSBJ) problem.

    Attributes:
        _optimizer: The optimization algorithm instance configured with
            appropriate hyperparameters for this subsystem.
    """
    def __init__(self) -> None:
        """Initialize the Optimization3 instance with the selected optimizer."""

        # Choose your optimizer and its hyperparameters

        # super().__init__(Solver_SCBO(option_1=None))

        # super().__init__(Solver_Scipy(method="trust-constr",
        #                               constraint_jac="2-point",
        #                               constraint_keep_feasible=False,
        #                               maxiter=None))

        super().__init__(Solver_PyNomadBBO(maxevals=30000,
                                           constraint_handling_method="PB",
                                           seed=1,
                                           vns_mads_search=False,
                                           quad_model_search=False,
                                           eqcon_as_ineqcon_tol=1E-8))

        # super().__init__(Solver_IPOPT(maxiter=1000,
        #                               acceptable_tol=1e-8,
        #                               constraint_jac="2-point",
        #                               constraint_keep_feasible=False))

        # super().__init__(Solver_Pyomo(option_1=None,
        #                               option_2=None))

        # super().__init__(Solver_Fmincon(method="active_set",
        #                                 maxiter=1000,
        #                                 maxfunevals=10000,
        #                                 tolfun=1e-8,
        #                                 tolcon=1e-8))
```

</div>

## 8. Executing the Coordination Method

With completed `main.py`, `InputFile.py` as well as subsystem specific `Analysis<id>.py`, `LocalConstraints<id>.py`, `LocalObjective<id>.py` and `Optimization<id>.py` files, the abbr:DDO framework executes the coordination method of choice by calling the `main()` function of `main.py` in the terminal. 

During the execution, various information from the abbr:DDO framework or third party optimization algorithms of `Optimization<id>.py` is printed to the terminal. Furthermore, the framework logs data in the use-case's `historyfiles/` folder as `userfiles/<usecasename>/historyfiles/historyfile_name_*_.dill` for subsequent post-processing. Further details in [Data Logging](../../framework-architecture/data-logging.md) and [Tutorial > Processing](../processing/index.md).
