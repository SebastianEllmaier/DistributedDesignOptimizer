---
title: Consensus ALC Pseudocode-to-Code Traceability
---

# Consensus Augmented Lagrangian Coordination (Consensus ALC) Pseudocode-to-Code Traceability

This page maps each step of the [Consensus Augmented Lagrangian Coordination](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/consensus-augmented-lagrangian-coordination.md) pseudocode to the implementing classes and methods in the codebase.

<!-- CONSENSUS-ALC-PSEUDOCODE-TRACEABILITY -->

## CouplingParameters and MiddleLevel

<iframe src="../../MiddleLevelDataStorage_Two_LocalSubSystemConsensusALC.drawio.html" width="100%" height="500" style="border:none;" allowfullscreen></iframe>

## Algorithm Options / Hyperparameters

The [Consensus abbr:ALC](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/consensus-augmented-lagrangian-coordination.md) coordination method is selected and configured in the use case `InputFile.py` by assigning a [`Consensus_ALC`](../../api/Distributed_Design_Optimizer/coordination/coordinationmethod/Consensus_ALC.md) instance to `self._coordinationmethod`. All algorithmic behaviour is wired through four constructor arguments:

```python
self._coordinationmethod: CoordinationMethodInterface = Consensus_ALC(
    convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_DeWit(
        tolerancetotalobjective=1000.0),
    convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(
        toleranceconsistency=1E-4),
    updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights(
        beta=1.3,
        gamma=0.25,
        initialweight=0.01,
        initialmultiplier=0.0),
    iterationscheme=Parallel())
```

Like [abbr:ALC](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/augmented-lagrangian-coordination.md), Consensus abbr:ALC relaxes constraints with a subgradient dual/penalty scheme, but it relaxes the *consensus constraints* sym:c_c (introduced by the auxiliary variables sym:y) instead of the coupling constraints sym:c. The four constructor arguments are therefore identical in role to abbr:ALC; the differences are internal to the primal inner loop (see the [auxiliary-variable update](#auxiliary-consensus-variable-update) below).

### Convergence criteria

Consensus abbr:ALC uses a nested inner/outer loop (Algorithm 4 in [Consensus abbr:ALC](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/consensus-augmented-lagrangian-coordination.md)), so two convergence indicators are configured:

- **Inner loop** — `convergence_indicator_innerloop`, evaluated by [`SubSystemBasis.evaluate_InnerLoopConvergenceIndicator`](../../api/Distributed_Design_Optimizer/subsystem/SubSystemBasis.md). Consensus abbr:ALC requires [`ConvergenceIndicator_Innerloop_DeWit`](../../api/Distributed_Design_Optimizer/coordination/convergence/DeWit/ConvergenceIndicator_Innerloop_DeWit.md), which converges on the relative change of the total objective, \(\text{error} = |sym:v_f^{\text{new}} - sym:v_f^{\text{old}}| / (1 + |sym:v_f^{\text{new}}|) \le\) `tolerancetotalobjective`. A **smaller** `tolerancetotalobjective` forces more inner abbr:FPI sweeps (each alternating the sym:d and sym:y updates) per outer step; a **larger** value (e.g. `1000.0`) terminates the inner loop earlier and shifts most of the work onto the outer dual and penalty updates.

- **Outer loop** — `convergence_indicator_outerloop`, evaluated by [`SubSystemBasis.evaluate_OuterLoopConvergenceIndicator`](../../api/Distributed_Design_Optimizer/subsystem/SubSystemBasis.md). Consensus abbr:ALC requires [`ConvergenceIndicator_Outerloop_DeWit`](../../api/Distributed_Design_Optimizer/coordination/convergence/DeWit/ConvergenceIndicator_Outerloop_DeWit.md), which terminates once all consensus inconsistencies \(sym:c_c = \left(sym:y - [{}^{i}_{j}sym:H({}^{i}sym:r);\, {}^{i}_{j}sym:z],\ldots\right)\) and their step-to-step changes fall within `toleranceconsistency`. A **smaller** `toleranceconsistency` (e.g. `1E-4`) enforces tighter consensus between coupled subsystems at the cost of more outer iterations.

Both indicators are validated in [`LocalSubSystemConsensusALC`](../../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemConsensusALC.md), which restricts Consensus abbr:ALC to the DeWit inner/outer indicators.

### Update method (dual and penalty update)

`updatecouplingparametermethod_outerloop` implements the Consensus abbr:ALC dual and penalty update, applied by [`LocalSubSystemConsensusALC.updateCouplingParameters_outerLoop`](../../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemConsensusALC.md). Consensus abbr:ALC requires the adaptive-weight augmented-Lagrangian method [`UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights`](../../api/Distributed_Design_Optimizer/coordination/updatecouplingparametermethod/UpdateCouplingParameterMethod_AugLagMultipliersAdaptiveWeights.md), which advances the multipliers by the subgradient step \(sym:\lambda \leftarrow sym:\lambda + 2\,sym:s \circ sym:s \circ sym:c_c\) (`update_CoordinationMultipliers`) and adapts the penalty weights sym:s (`update_CoordinationWeights`) — the same rule as abbr:ALC but evaluated on the consensus residual sym:c_c:

- `initialweight` — the initial penalty weight sym:s (recommended \(0 < sym:s \le 0.1\), e.g. `0.01`). **Larger** `initialweight` produces larger multiplier steps and faster constraint enforcement, but risks oscillation/ill-conditioning; **smaller** values give gentler, more stable but slower consensus.
- `initialmultiplier` — the initial Lagrange multiplier \({}^{i}_{j}sym:\lambda^{(0)}\) (recommended `0.0`).

### Auxiliary (consensus) variable update

The consensus reformulation adds the auxiliary variables sym:y, which are optimized *inside* the inner loop alongside the sym:d step. Because the sym:y subproblem is an unconstrained convex abbr:QP (for \(sym:s^{(sym:k)} \neq 0\)), it has a closed-form solution that each subsystem evaluates locally in [`LocalSubSystemConsensusALC.update_AuxiliaryVariables`](../../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemConsensusALC.md) (invoked via `updateCouplingParameters_innerLoop`), eliminating a dedicated controller at the cost of duplicated work but reduced communication. The resulting sym:y values are stored per coupling in [`CouplingParametersConsensusALC`](../../api/Distributed_Design_Optimizer/subsystem/couplingparameters/consensus_alc/CouplingParametersConsensusALC.md). This step is not user-configurable; it is governed only by the current weights sym:s and multipliers sym:\lambda.

### Iteration scheme

`iterationscheme` controls how the inner-loop primal updates are scheduled by the [`IterationSchemeInterface`](../../api/Distributed_Design_Optimizer/coordination/innerloop_iterationscheme/IterationSchemeInterface.md). Consensus abbr:ALC has no dedicated controller — the sym:d step is fully parallel and alternates with the local sym:y update in an abbr:FPI, so the choice selects the fixed-point sweep:

- [`Parallel`](../../api/Distributed_Design_Optimizer/coordination/innerloop_iterationscheme/Parallel.md) — a **Jacobi** sweep: all subsystem problems are solved simultaneously from the previous iterate.
- [`SequentialForward`](../../api/Distributed_Design_Optimizer/coordination/innerloop_iterationscheme/SequentialForward.md) / [`SequentialBackward`](../../api/Distributed_Design_Optimizer/coordination/innerloop_iterationscheme/SequentialBackward.md) — a **Gauss–Seidel** sweep: subsystems are solved one after another, each using the latest neighbour data (often faster convergence, no parallelism).

### Penalty hyperparameters β, γ, s

The pseudocode "Require" block (Algorithm 4, lines 1–2) lists the penalty-adaption hyperparameters sym:\beta and sym:\gamma, alongside the initial auxiliary variables sym:y, penalty weights sym:s and multipliers sym:\lambda. sym:\beta and sym:\gamma are passed to the update method above and govern the penalty update \(sym:s^{(sym:k+1)} \leftarrow sym:\beta\,sym:s^{(sym:k)}\) applied only when \(|sym:c_c^{(sym:k+1)}| > sym:\gamma\,|sym:c_c^{(sym:k)}|\):

- sym:\beta — the penalty-weight increase factor (must satisfy \(sym:\beta > 1\), recommended \(sym:\beta \le 3\), e.g. `1.3`). A **larger** sym:\beta grows the weights more aggressively when consensus stalls (stronger constraint enforcement, but risk of ill-conditioning and oscillation); a value **closer to 1** grows them gently (more stable, slower consensus).
- sym:\gamma — the inconsistency-reduction threshold (must satisfy \(0 < sym:\gamma < 1\), e.g. `0.25`). The weights are only increased when the inconsistency fails to shrink below a factor sym:\gamma of the previous step. A **smaller** sym:\gamma demands a larger per-iteration reduction before the weights are held constant, so penalties grow more often; a value **closer to 1** tolerates slow reduction and increases penalties rarely.

The corresponding weights sym:s, multipliers sym:\lambda and auxiliary variables sym:y are stored per coupling in [`CouplingParametersConsensusALC`](../../api/Distributed_Design_Optimizer/subsystem/couplingparameters/consensus_alc/CouplingParametersConsensusALC.md), while sym:\beta and sym:\gamma are held on the [`Consensus_ALC`](../../api/Distributed_Design_Optimizer/coordination/coordinationmethod/Consensus_ALC.md) coordination method.