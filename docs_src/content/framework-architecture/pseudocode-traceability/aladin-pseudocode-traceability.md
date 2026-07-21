---
title: ALADIN Pseudocode-to-Code Traceability
---

# Augmented Lagrangian Alternating Direction Inexact Newton (ALADIN) Pseudocode-to-Code Traceability

This page maps each step of the [abbr:ALADIN](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/aladin.md) pseudocode to the implementing classes and methods in the codebase.

<!-- ALADIN-PSEUDOCODE-TRACEABILITY -->

## CouplingParameters and MiddleLevel

<iframe src="../../MiddleLevelDataStorage_Two_LocalSubSystemALADIN.drawio.html" width="100%" height="500" style="border:none;" allowfullscreen></iframe>

<iframe src="../../MiddleLevelDataStorage_LocalSubSystemALADIN_ControllerSubSystemALADIN.drawio.html" width="100%" height="500" style="border:none;" allowfullscreen></iframe>

## Algorithm Options / Hyperparameters

The [abbr:ALADIN](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/aladin.md) coordination method is selected and configured in the use case `InputFile.py` by assigning an [`ALADIN`](../../api/Distributed_Design_Optimizer/coordination/coordinationmethod/ALADIN.md) instance to `self._coordinationmethod`. All algorithmic behaviour is wired through four constructor arguments:

```python
self._coordinationmethod: CoordinationMethodInterface = ALADIN(
    convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(
        tolerancetotalobjective=1000.0),
    convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(
        toleranceconsistency=1E-4),
    updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AugLagMultipliersFixedWeights(
        initialweight=0.01,
        initialmultiplier=0.0),
    iterationscheme=ParallelLocal_SequentialController())
```

### Convergence criteria

abbr:ALADIN uses a nested inner/outer loop (Algorithm 2 in [abbr:ALADIN](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/aladin.md)), so two convergence indicators are configured:

- **Inner loop** — `convergence_indicator_innerloop`, evaluated by [`SubSystemBasis.evaluate_InnerLoopConvergenceIndicator`](../../api/Distributed_Design_Optimizer/subsystem/SubSystemBasis.md). The recommended choice is [`ConvergenceIndicator_Innerloop_DeWit`](../../api/Distributed_Design_Optimizer/coordination/convergence/DeWit/ConvergenceIndicator_Innerloop_DeWit.md), which converges on the relative change of the total objective, \(\text{error} = |sym:v_f^{\text{new}} - sym:v_f^{\text{old}}| / (1 + |sym:v_f^{\text{new}}|) \le\) `tolerancetotalobjective`. A **smaller** `tolerancetotalobjective` forces more inner iterations (tighter local/controller abbr:QP resolution per outer step); a **larger** value (e.g. `1000.0`) lets the inner loop terminate quickly and shifts most of the work onto the outer dual updates.

- **Outer loop** — `convergence_indicator_outerloop`, evaluated by [`SubSystemBasis.evaluate_OuterLoopConvergenceIndicator`](../../api/Distributed_Design_Optimizer/subsystem/SubSystemBasis.md). The recommended choice is [`ConvergenceIndicator_Outerloop_DeWit`](../../api/Distributed_Design_Optimizer/coordination/convergence/DeWit/ConvergenceIndicator_Outerloop_DeWit.md), which terminates once all coupling inconsistencies \(\left({}^{i}_{j}sym:H({}^{i}sym:r) - {}^{i}_{j}sym:h,\; {}^{i}_{j}sym:z - {}^{j}_{i}sym:z,\ldots\right)\) and their step-to-step changes fall within `toleranceconsistency`. A **smaller** `toleranceconsistency` (e.g. `1E-4`) enforces tighter consensus between coupled subsystems at the cost of more outer iterations.

An [`AlwaysConverged`](../../api/Distributed_Design_Optimizer/coordination/convergence/AlwaysConverged/ConvergenceIndicator_Innerloop_AlwaysConverged.md) inner-loop indicator is also available when a single inner pass per outer iteration is desired.

### Update method (dual update)

`updatecouplingparametermethod_outerloop` implements the abbr:ALADIN dual update (pseudocode lines 25–27). abbr:ALADIN requires the fixed-weight augmented-Lagrangian multiplier update [`UpdateCouplingParameterMethod_AugLagMultipliersFixedWeights`](../../api/Distributed_Design_Optimizer/coordination/updatecouplingparametermethod/UpdateCouplingParameterMethod_AugLagMultipliersFixedWeights.md), which updates each multiplier as \(sym:\lambda \leftarrow sym:\lambda + 2\,sym:s^{2}\,sym:c(\cdot)\) using the coupling inconsistency \(sym:c(\cdot)\):

- `initialweight` — the penalty scaling weight sym:s (recommended \(0 < sym:s \le 0.1\), e.g. `0.01`). **Larger** `initialweight` produces larger multiplier steps and faster constraint enforcement, but risks oscillation/divergence; **smaller** values give gentler, more stable but slower consensus. Unlike abbr:ALC's adaptive-weight methods, this weight stays **fixed** across outer iterations — a defining property of abbr:ALADIN.
- `initialmultiplier` — the initial Lagrange multiplier \({}^{i}_{j}sym:\lambda^{(0)}\) (recommended `0.0`).

### Iteration scheme

`iterationscheme` controls how the inner-loop jobs are scheduled by the [`IterationSchemeInterface`](../../api/Distributed_Design_Optimizer/coordination/innerloop_iterationscheme/IterationSchemeInterface.md). Because abbr:ALADIN's controller abbr:QP couples all subsystems and must run after the local NLPs, the appropriate choice is [`ParallelLocal_SequentialController`](../../api/Distributed_Design_Optimizer/coordination/innerloop_iterationscheme/ParallelLocal_SequentialController.md): the local subsystem problems (pseudocode line 11) are solved in parallel, followed by the sequential controller abbr:QP (pseudocode line 18).

### Proximal hyperparameters ν, Σⁱ, s

The pseudocode "Require" block (Algorithm 2, lines 1–3) lists the penalty parameter sym:\nu, the positive-definite proximal scaling matrix ${}^{i}$sym:\Sigma, and the coupling scaling weights ${}^{i}_{j}$sym:s:

- sym:\nu and ${}^{i}$sym:\Sigma weight the proximal term \(\tfrac{sym:\nu}{2}\lVert {}^{i}sym:d - {}^{i}\hat{sym:d}\rVert_{{}^{i}sym:\Sigma}^{2}\) in the local subproblem (see [`LocalSubSystemALADIN.evaluateCoordinationObjective`](../../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemALADIN.md), accessed via `get_Nu`/`set_Nu` and `get_Sigma_i`/`set_Sigma_i`). A **larger** sym:\nu or larger diagonal entries of ${}^{i}$sym:\Sigma keep each local iterate closer to the controller prediction \({}^{i}\hat{sym:d}\) (stronger regularization, better consistency, slower local progress); **smaller** values give the local NLP more freedom. Currently ${}^{i}$sym:\Sigma is initialized to the identity matrix in `initializeCouplingParameters_before_CopyToMiddleLevel` and sym:\nu is set internally (not yet exposed through the `InputFile`).
- ${}^{i}_{j}$sym:s are the coupling scaling weights carried in the coordination abbr:QP and shared with the controller; they coincide with the `initialweight` sym:s of the dual update above.