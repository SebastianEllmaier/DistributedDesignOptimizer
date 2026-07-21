---
title: ALC Pseudocode-to-Code Traceability
---

# Augmented Lagrangian Coordination (ALC) Pseudocode-to-Code Traceability

This page maps each step of the [Augmented Lagrangian Coordination (ALC)](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/augmented-lagrangian-coordination.md) pseudocode to the implementing classes and methods in the codebase.

<!-- ALC-PSEUDOCODE-TRACEABILITY -->

## CouplingParameters and MiddleLevel

<iframe src="../../MiddleLevelDataStorage_Two_LocalSubSystemALC.drawio.html" width="100%" height="500" style="border:none;" allowfullscreen></iframe>

## Algorithm Options / Hyperparameters

The [abbr:ALC](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/augmented-lagrangian-coordination.md) coordination method is selected and configured in the use case `InputFile.py` by assigning an [`ALC`](../../api/Distributed_Design_Optimizer/coordination/coordinationmethod/ALC.md) instance to `self._coordinationmethod`. All algorithmic behaviour is wired through four constructor arguments:

```python
self._coordinationmethod: CoordinationMethodInterface = ALC(
    convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(
        tolerancetotalobjective=1E-5),
    convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(
        toleranceconsistency=1E-4),
    updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights(
        beta=1.3,
        gamma=0.25,
        initialweight=0.01,
        initialmultiplier=0.0),
    iterationscheme=Parallel())
```

### Convergence criteria

abbr:ALC uses a nested inner/outer loop (Algorithm 1 in [abbr:ALC](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/augmented-lagrangian-coordination.md)), so two convergence indicators are configured:

- **Inner loop** — `convergence_indicator_innerloop`, evaluated by [`SubSystemBasis.evaluate_InnerLoopConvergenceIndicator`](../../api/Distributed_Design_Optimizer/subsystem/SubSystemBasis.md). abbr:ALC requires [`ConvergenceIndicator_Innerloop_DeWit`](../../api/Distributed_Design_Optimizer/coordination/convergence/DeWit/ConvergenceIndicator_Innerloop_DeWit.md), which converges on the relative change of the total objective, \(\text{error} = |sym:v_f^{\text{new}} - sym:v_f^{\text{old}}| / (1 + |sym:v_f^{\text{new}}|) \le\) `tolerancetotalobjective`. A **smaller** `tolerancetotalobjective` (e.g. `1E-5`) forces more inner abbr:FPI sweeps per outer step (tighter primal-update fixed point); a **larger** value terminates the inner loop earlier and shifts most of the work onto the outer dual and penalty updates.

- **Outer loop** — `convergence_indicator_outerloop`, evaluated by [`SubSystemBasis.evaluate_OuterLoopConvergenceIndicator`](../../api/Distributed_Design_Optimizer/subsystem/SubSystemBasis.md). abbr:ALC requires [`ConvergenceIndicator_Outerloop_DeWit`](../../api/Distributed_Design_Optimizer/coordination/convergence/DeWit/ConvergenceIndicator_Outerloop_DeWit.md), which terminates once all coupling inconsistencies \(sym:c = \left({}^{i}_{j}sym:H({}^{i}sym:r) - {}^{i}_{j}sym:h,\; {}^{i}_{j}sym:z - {}^{j}_{i}sym:z,\ldots\right)\) and their step-to-step changes fall within `toleranceconsistency`. A **smaller** `toleranceconsistency` (e.g. `1E-4`) enforces tighter consensus between coupled subsystems at the cost of more outer iterations.

Both indicators are validated in [`LocalSubSystemALC`](../../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemALC.md) (`validate_inputs`), which restricts abbr:ALC to the DeWit inner/outer indicators.

### Update method (dual and penalty update)

`updatecouplingparametermethod_outerloop` implements the abbr:ALC dual and penalty update (pseudocode lines 19–20), applied by [`LocalSubSystemALC.updateCouplingParameters_outerLoop`](../../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemALC.md). abbr:ALC requires the adaptive-weight augmented-Lagrangian method [`UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights`](../../api/Distributed_Design_Optimizer/coordination/updatecouplingparametermethod/UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights.md), which advances the multipliers by the subgradient step \(sym:\lambda \leftarrow sym:\lambda + 2\,sym:s \circ sym:s \circ sym:c\) (`update_CoordinationMultipliers`) and adapts the penalty weights sym:s (`update_CoordinationWeights`):

- `initialweight` — the initial penalty weight sym:s (recommended \(0 < sym:s \le 0.1\), e.g. `0.01`). **Larger** `initialweight` produces larger multiplier steps and faster constraint enforcement, but risks oscillation/ill-conditioning; **smaller** values give gentler, more stable but slower consensus.
- `initialmultiplier` — the initial Lagrange multiplier \({}^{i}_{j}sym:\lambda^{(0)}\) (recommended `0.0`).

### Iteration scheme

`iterationscheme` controls how the inner-loop primal updates are scheduled by the [`IterationSchemeInterface`](../../api/Distributed_Design_Optimizer/coordination/innerloop_iterationscheme/IterationSchemeInterface.md). abbr:ALC has no controller — the [primal problem](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/augmented-lagrangian-coordination.md) is solved distributedly by an abbr:FPI scheme, so the choice selects the fixed-point sweep:

- [`Parallel`](../../api/Distributed_Design_Optimizer/coordination/innerloop_iterationscheme/Parallel.md) — a **Jacobi** sweep: all subsystem problems (pseudocode line 10) are solved simultaneously from the previous iterate.
- [`SequentialForward`](../../api/Distributed_Design_Optimizer/coordination/innerloop_iterationscheme/SequentialForward.md) / [`SequentialBackward`](../../api/Distributed_Design_Optimizer/coordination/innerloop_iterationscheme/SequentialBackward.md) — a **Gauss–Seidel** sweep: subsystems are solved one after another, each using the latest neighbour data (often faster convergence, no parallelism).

### Penalty hyperparameters β, γ, s

The pseudocode "Require" block (Algorithm 1, lines 1–3) lists the penalty-adaption hyperparameters sym:\beta and sym:\gamma, alongside the initial penalty weights sym:s and multipliers sym:\lambda. sym:\beta and sym:\gamma are passed to the update method above and govern the penalty update \(sym:s^{(sym:k+1)} \leftarrow sym:\beta\,sym:s^{(sym:k)}\) applied only when \(|sym:c^{(sym:k+1)}| > sym:\gamma\,|sym:c^{(sym:k)}|\):

- sym:\beta — the penalty-weight increase factor (must satisfy \(sym:\beta > 1\), recommended \(sym:\beta \le 3\), e.g. `1.3`). A **larger** sym:\beta grows the weights more aggressively when consensus stalls (stronger constraint enforcement, but risk of ill-conditioning and oscillation); a value **closer to 1** grows them gently (more stable, slower consensus).
- sym:\gamma — the inconsistency-reduction threshold (must satisfy \(0 < sym:\gamma < 1\), e.g. `0.25`). The weights are only increased when the inconsistency fails to shrink below a factor sym:\gamma of the previous step. A **smaller** sym:\gamma demands a larger per-iteration reduction before the weights are held constant, so penalties grow more often; a value **closer to 1** tolerates slow reduction and increases penalties rarely.

The corresponding weights sym:s and multipliers sym:\lambda are stored per coupling in [`CouplingParametersALC`](../../api/Distributed_Design_Optimizer/subsystem/couplingparameters/alc/CouplingParametersALC.md), while sym:\beta and sym:\gamma are held on the [`ALC`](../../api/Distributed_Design_Optimizer/coordination/coordinationmethod/ALC.md) coordination method.