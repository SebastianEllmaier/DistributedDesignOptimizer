---
title: SBDP Pseudocode-to-Code Traceability
---

# Sensitivity Based Distributed Programming (SBDP) Pseudocode-to-Code Traceability

This page maps each step of the [Sensitivity Based Distributed Programming (SBDP)](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/sensitivity-based-distributed-programming.md) pseudocode to the implementing classes and methods in the codebase.

<!-- SBDP-PSEUDOCODE-TRACEABILITY -->

## CouplingParameters and MiddleLevel

<iframe src="../../MiddleLevelDataStorage_Two_LocalSubSystemSBDP.drawio.html" width="100%" height="500" style="border:none;" allowfullscreen></iframe>

## Algorithm Options / Hyperparameters

The [abbr:SBDP](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/sensitivity-based-distributed-programming.md) coordination method is selected and configured in the use case `InputFile.py` by assigning an [`SBDP`](../../api/Distributed_Design_Optimizer/coordination/coordinationmethod/SBDP.md) instance to `self._coordinationmethod`. All algorithmic behaviour is wired through four constructor arguments:

```python
self._coordinationmethod: CoordinationMethodInterface = SBDP(
    convergence_indicator_innerloop=ConvergenceIndicator_Innerloop_AlwaysConverged(),
    convergence_indicator_outerloop=ConvergenceIndicator_Outerloop_DeWit(
        toleranceconsistency=1E-4),
    updatecouplingparametermethod_outerloop=UpdateCouplingParameterMethod_OnlyInitialMultipliers(
        initialmultiplier=0.0),
    iterationscheme=Parallel())
```

abbr:SBDP does *not* relax the coupling with an augmented-Lagrangian penalty. Instead it keeps the coordination equality as a **hard** constraint in each subsystem's local problem and couples subsystems through a first-order sensitivity correction \(\nabla_{{}^{i}sym:d}{}^{j}sym:L^{(sym:k)}\) (Algorithm 3 in [abbr:SBDP](../../distributed-optimization-for-multidisciplinary-design/coordination-methods/sensitivity-based-distributed-programming.md)). Consequently there are no penalty weights sym:s and no penalty-adaption hyperparameters sym:\beta, sym:\gamma; the coordination multipliers sym:\lambda_h and sym:\lambda_z are recovered directly from the abbr:KKT system of the local optimization rather than updated by a dual step.

### Convergence criteria

abbr:SBDP runs a single decentralized pass per outer iteration (there is no inner fixed-point loop), so the two indicators play asymmetric roles:

- **Inner loop** — `convergence_indicator_innerloop` must be [`ConvergenceIndicator_Innerloop_AlwaysConverged`](../../api/Distributed_Design_Optimizer/coordination/convergence/AlwaysConverged/ConvergenceIndicator_Innerloop_AlwaysConverged.md). Because abbr:SBDP performs exactly one primal solve per outer step, the inner loop is required to report convergence immediately after that single pass; [`LocalSubSystemSBDP`](../../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemSBDP.md) restricts the inner-loop indicator to this always-converged variant.

- **Outer loop** — `convergence_indicator_outerloop`, evaluated by [`SubSystemBasis.evaluate_OuterLoopConvergenceIndicator`](../../api/Distributed_Design_Optimizer/subsystem/SubSystemBasis.md). abbr:SBDP requires [`ConvergenceIndicator_Outerloop_DeWit`](../../api/Distributed_Design_Optimizer/coordination/convergence/DeWit/ConvergenceIndicator_Outerloop_DeWit.md), which terminates once all coupling inconsistencies \(sym:c = \left({}^{i}_{j}sym:H({}^{i}sym:r) - {}^{i}_{j}sym:h,\; {}^{i}_{j}sym:S_z\,{}^{i}sym:d - {}^{j}_{i}sym:z,\ldots\right)\) and their step-to-step changes fall within `toleranceconsistency`. This tolerance plays the role of the abbr:SBDP hyperparameter sym:\epsilon_k (see the *Hyperparameter ε_k* section below).

Both indicators are validated in [`LocalSubSystemSBDP`](../../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemSBDP.md), which restricts abbr:SBDP to the always-converged inner indicator and the DeWit outer indicator.

### Update method (multiplier recovery)

`updatecouplingparametermethod_outerloop` must be [`UpdateCouplingParameterMethod_OnlyInitialMultipliers`](../../api/Distributed_Design_Optimizer/coordination/updatecouplingparametermethod/UpdateCouplingParameterMethod_OnlyInitialMultipliers.md). abbr:SBDP does not perform a dual/penalty update: the coordination-equality multipliers sym:\lambda_h and sym:\lambda_z are recovered from the abbr:KKT system of each local solve (pseudocode line 9, `postprocess_Optimization` / `compute_KKT_multipliers` on [`LocalSubSystemSBDP`](../../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemSBDP.md)) and exchanged with neighbours through the interface storage. The update method therefore only seeds the multipliers before the first iteration:

- `initialmultiplier` — the initial coordination multipliers \({}^{i}_{j}sym:\lambda_h^{(0)}\), \({}^{i}_{j}sym:\lambda_z^{(0)}\) (recommended `0.0`). From the first outer iteration onward the values are overwritten by the recovered abbr:KKT multipliers, so this argument only sets the starting point of the sensitivity correction.

The recovered multipliers and the coupling data are stored per coupling in [`CouplingParametersSBDP`](../../api/Distributed_Design_Optimizer/subsystem/couplingparameters/sbdp/CouplingParametersSBDP.md).

### Iteration scheme

`iterationscheme` controls how the decentralized subsystem solves (pseudocode line 5) are scheduled by the [`IterationSchemeInterface`](../../api/Distributed_Design_Optimizer/coordination/innerloop_iterationscheme/IterationSchemeInterface.md). abbr:SBDP has no controller and each subsystem's local problem is independent within an outer step, so parallel execution is recommended:

- [`Parallel`](../../api/Distributed_Design_Optimizer/coordination/innerloop_iterationscheme/Parallel.md) — a **Jacobi** sweep: all subsystem problems are solved simultaneously from the previous iterate (recommended for abbr:SBDP).
- [`SequentialForward`](../../api/Distributed_Design_Optimizer/coordination/innerloop_iterationscheme/SequentialForward.md) / [`SequentialBackward`](../../api/Distributed_Design_Optimizer/coordination/innerloop_iterationscheme/SequentialBackward.md) — a **Gauss–Seidel** sweep: subsystems are solved one after another. These are allowed but not recommended, since the independent subproblems gain nothing from sequential execution.

### Hyperparameter ε_k

The pseudocode "Require" block (Algorithm 3, lines 1–2) lists the single hyperparameter sym:\epsilon_k alongside the initial multipliers \({}^{j}_{i}sym:\lambda_h\), \({}^{j}_{i}sym:\lambda_z\). In the implementation sym:\epsilon_k is realised as the outer-loop consistency tolerance `toleranceconsistency` of [`ConvergenceIndicator_Outerloop_DeWit`](../../api/Distributed_Design_Optimizer/coordination/convergence/DeWit/ConvergenceIndicator_Outerloop_DeWit.md):

- sym:\epsilon_k (`toleranceconsistency`) — the consensus tolerance on the coupling inconsistencies sym:c. A **smaller** sym:\epsilon_k (e.g. `1E-4`) enforces tighter agreement between coupled subsystems at the cost of more outer iterations; a **larger** value terminates the coordination earlier with looser consensus. Because abbr:SBDP has no penalty weights, sym:\epsilon_k is the primary control on the accuracy/effort trade-off.

