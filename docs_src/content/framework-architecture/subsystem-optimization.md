---
title: SubSystem Optimization
---

# SubSystem Optimization

The [Unified Algorithmic Structure](../distributed-optimization-for-multidisciplinary-design/unified-algorithmic-structure.md) defines the following general form for the optimization problem of each [`LocalSubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md), together with the Lagrange multiplier associated with each constraint:

\[\begin{aligned}
{}^{i}sym:d^{(sym:k,\,sym:l+1)} \leftarrow{} & \argmin_{{}^{i}sym:d\;\in\;{}^{i}sym:\mathcal{D}} \;\;
{}^{i}sym:v_f\!\left({}^{i}sym:r\right)
+ {}^{i}sym:P\!\left({}^{i}sym:d,\;
\left\{{}^{i}_{j}sym:u,\;{}^{j}_{i}sym:u\right\}_{j\in{}^{i}sym:N},\;
{}^{i}_{C}sym:u,\;{}^{C}_{i}sym:u\right) \\
& \text{s.t.} \;\; {}^{i}sym:v_g\!\left({}^{i}sym:r\right) \leq 0
\quad | \;\; {}^{i}sym:\kappa_g, \\
& \phantom{\text{s.t.}} \;\; {}^{i}sym:v_h\!\left({}^{i}sym:r\right) = 0
\quad | \;\; {}^{i}sym:\kappa_h, \\
& \phantom{\text{s.t.}} \;\; {}^{i}sym:v_{\mathcal{D}}\!\left({}^{i}sym:d\right) \leq 0
\quad | \;\; {}^{i}sym:\kappa_d, \\
& \phantom{\text{s.t.}} \;\; {}^{i}sym:Q^{\leq}\!\left({}^{i}sym:d,\;
\left\{{}^{i}_{j}sym:u,\;{}^{j}_{i}sym:u\right\}_{j\in{}^{i}sym:N},\;
{}^{i}_{C}sym:u,\;{}^{C}_{i}sym:u\right) \leq 0
\quad | \;\; \kappa_Q^{\leq}, \\
& \phantom{\text{s.t.}} \;\; {}^{i}sym:Q^{=}\!\left({}^{i}sym:d,\;
\left\{{}^{i}_{j}sym:u,\;{}^{j}_{i}sym:u\right\}_{j\in{}^{i}sym:N},\;
{}^{i}_{C}sym:u,\;{}^{C}_{i}sym:u\right) = 0
\quad | \;\; \kappa_Q^{=},
\end{aligned}\]

where sym:\kappa_g, sym:\kappa_h and sym:\kappa_d are the multipliers of the local inequality, local equality and design-variable-bound constraints, and $\kappa_Q^{\leq}$, $\kappa_Q^{=}$ are the multipliers of the coordination-specific inequality/equality constraints sym:Q^{\leq}, sym:Q^{=}. All multipliers are gathered at the optimal ${}^{i}$sym:d returned by the solver — see [Multiplier reconstruction when the solver does not provide them](#multiplier-reconstruction-when-the-solver-does-not-provide-them) below.

## Solving for optimal ${}^{i}$sym:d

The [Unified Algorithmic Structure Pseudocode-To-Code Traceability](core-components-and-unified-algorithmic-structure.md#unified-algorithmic-structure-pseudocode-to-code-traceability) indicates that [`SubSystemBasis.run_IterativeOptimization()`](../api/Distributed_Design_Optimizer/subsystem/SubSystemBasis.md) solves the above optimization problem. 
The following procedure details this further.

<!-- SUBSYSTEM-RUN-ITERATIVE-OPTIMIZATION-PSEUDOCODE-TRACEABILITY -->

The [Unified Algorithmic Structure](../distributed-optimization-for-multidisciplinary-design/unified-algorithmic-structure.md) defines the following general form for the optimization problem of each [`ControllerSubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/ControllerSubSystemBasis.md), which is structurally equivalent to the above optimization problem (neglecting ${}^{i}$sym:v_f, ${}^{i}$sym:v_g, ${}^{i}$sym:v_h and ${}^{i}$sym:D):

\[\begin{aligned}
sym:\Box \leftarrow{} & \argmin_{sym:\Box} \;\;
{}^{C}sym:P\!\left(sym:\Box,\;
\left\{{}^{C}_{i}sym:u,\;{}^{i}_{C}sym:u\right\}_{i\in sym:M}\right) \\
& \text{s.t.} \;\; {}^{C}sym:Q^{\leq}\!\left(sym:\Box,\;
\left\{{}^{C}_{i}sym:u,\;{}^{i}_{C}sym:u\right\}_{i\in sym:M}\right) \leq 0
\quad | \;\; \kappa_Q^{\leq}, \\
& \phantom{\text{s.t.}} \;\; {}^{C}sym:Q^{=}\!\left(sym:\Box,\;
\left\{{}^{C}_{i}sym:u,\;{}^{i}_{C}sym:u\right\}_{i\in sym:M}\right) = 0
\quad | \;\; \kappa_Q^{=}.
\end{aligned}\]

Thus the same [`SubSystemBasis.run_IterativeOptimization()`](../api/Distributed_Design_Optimizer/subsystem/SubSystemBasis.md) procedure is employed, albeit with coordination-specific definitions of ${}^{C}$sym:d, ${}^{C}$sym:P, ${}^{C}$sym:Q^{\leq}, ${}^{C}$sym:Q^{=}.

## Multiplier reconstruction when the solver does not provide them

The solving workflow described above — [`SubSystemBasis.run_IterativeOptimization()`](../api/Distributed_Design_Optimizer/subsystem/SubSystemBasis.md) — is identical for every coordination method and lives entirely in the shared parent classes [`SubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/SubSystemBasis.md), [`LocalSubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md) and [`ControllerSubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/ControllerSubSystemBasis.md). Determining the multipliers sym:\kappa_g, sym:\kappa_h, sym:\kappa_d, $\kappa_Q^{\leq}$, $\kappa_Q^{=}$ from the abbr:KKT conditions, however, is **not** part of that shared workflow: some coordination methods need these multipliers, while others don't. The abbr:KKT determination is therefore only *triggered* from within the coordination-specific `LocalSubSystem<Method>.postprocess_Optimization()` (or `ControllerSubSystem<Method>.postprocess_Optimization()`) — see [Where this is used in the workflow](#where-this-is-used-in-the-workflow) below.

Many solvers of the [`solver/`](../api/Distributed_Design_Optimizer/subsystem/optimization/solver/index.md) package do not return these multipliers directly. To make the coordination methods that need them independent of the chosen solver, the subsystem base classes reconstruct them from the first-order optimality (abbr:KKT) conditions at the returned primal solution.

The *reconstruction logic itself* is implemented once in the parent classes [`SubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/SubSystemBasis.md), [`LocalSubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md), and [`ControllerSubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/ControllerSubSystemBasis.md), so that every coordination-specific subsystem that does call it obtains it for free. It relies on the constraint gradients and Jacobians produced by the [Derivative Computation](derivative-computation.md), but does **not** trigger that computation itself: `compute_KKT_system_matrix_and_bounds()` only *reads* whatever gradients/Jacobians are already stored in `OptimData` (e.g. via `get_Jacobian_LocalEqualityConstraints()`). A coordination method's `postprocess_Optimization()` must therefore call `evaluateAllJacobians()` *before* `compute_KKT_multipliers()`, as [`LocalSubSystemALADIN`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemALADIN.md) and [`LocalSubSystemSBDP`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemSBDP.md) both do — see [Where this is used in the workflow](#where-this-is-used-in-the-workflow) below.

### Background: the stationarity condition

At a local optimum ${}^{i}$sym:d of the subsystem optimization problem stated above, the abbr:KKT stationarity condition states that the gradient of the Lagrangian vanishes:

\[
\nabla_{{}^{i}sym:d} f\left({}^{i}sym:d\right)
+ sym:\kappa_g^{T} \nabla_{{}^{i}sym:d} {}^{i}sym:v_g\!\left({}^{i}sym:r\right)
+ sym:\kappa_h^{T} \nabla_{{}^{i}sym:d} {}^{i}sym:v_h\!\left({}^{i}sym:r\right)
+ sym:\kappa_d^{T} \nabla_{{}^{i}sym:d} {}^{i}sym:v_{\mathcal{D}}\!\left({}^{i}sym:d\right)
+ \left(\kappa_Q^{\leq}\right)^{T} \nabla_{{}^{i}sym:d} {}^{i}sym:Q^{\leq}
+ \left(\kappa_Q^{=}\right)^{T} \nabla_{{}^{i}sym:d} {}^{i}sym:Q^{=}
= 0,
\]

where $f = {}^{i}$sym:v_f $+$ ${}^{i}$sym:P is the subsystem's total objective (local objective plus coordination term, exactly `TotalObjectiveValue` as assembled by `evaluateTotalObjective()`), and each gradient term is weighted by the multiplier introduced for that constraint in the optimization problem above. Only *active* inequality constraints and bounds (and all equality constraints) contribute: an inactive inequality/bound constraint's multiplier is fixed at `0` and drops out of the sum. Writing $\mathcal{A}$ for this set of active constraints and collecting their gradients row-wise into a Jacobian $J$ (one row per entry of sym:\kappa_g, sym:\kappa_h, sym:\kappa_d, $\kappa_Q^{\leq}$, $\kappa_Q^{=}$ that is active), the stationarity condition becomes the linear system

\[
J^{\top} \lambda = -\,\nabla_{{}^{i}sym:d} f,
\]

subject to $\lambda_a \geq 0$ for the multipliers of active inequality constraints and bounds, and $\lambda_a$ free (unrestricted sign) for the multipliers of equality constraints. The framework solves this system for $\lambda$ and then maps its entries back onto sym:\kappa_g, sym:\kappa_h, sym:\kappa_d, $\kappa_Q^{\leq}$, $\kappa_Q^{=}$ (or the controller's coordination-only counterparts).

### 1. Orchestration — `compute_KKT_multipliers()`

Defined in [`SubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/SubSystemBasis.md), this is the solver-agnostic driver that assembles and solves the linear system from the previous section, delegating the structure-dependent and fallback work to three helper methods detailed below: it requests the matrix and bounds from `compute_KKT_system_matrix_and_bounds()` (step 2), forms the right-hand side $b = -\nabla f$ from the stored gradient of the total objective, solves the system as a **linear feasibility problem** with a zero cost vector using `scipy.optimize.linprog` (`A_eq` $= J^{\top}$, `b_eq` $= b$), falling back to `compute_ApproximateKKT_multipliers()` (step 3) if that system is infeasible, and finally hands the solution to `decompose_KKT_multipliers()` (step 4):

<div class="algorithm" markdown="0">
<div class="algorithm-caption"><strong>Procedure</strong> SubSystemBasis.compute_KKT_multipliers()</div>
<div class="algo-body">
<div class="algo-line algo-indent-0"><span>result ← compute_KKT_system_matrix_and_bounds() <span class="algo-comment">▷ [constraint_matrix, bounds]</span></span></div>
<div class="algo-line algo-indent-0"><span>J ← transpose(constraint_matrix)</span></div>
<div class="algo-line algo-indent-0"><span>b ← −gradient_of_total_objective <span class="algo-comment">▷ zeros if no objective gradient</span></span></div>
<div class="algo-line algo-indent-0"><span>c ← 0 <span class="algo-comment">▷ pure feasibility, no cost</span></span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-0"><span>result ← linprog(c, A_eq = J, b_eq = b, bounds = bounds)</span></div>
<div class="algo-line algo-indent-0"><span><span class="algo-keyword">if</span> status = 0 (success) <span class="algo-keyword">then</span> all_multipliers ← result.x</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">else if</span> status = 1 (iteration limit) <span class="algo-keyword">then</span> raise error</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">else if</span> status = 2 (infeasible) <span class="algo-keyword">then</span> warn and</span></div>
<div class="algo-line algo-indent-2"><span>all_multipliers ← compute_ApproximateKKT_multipliers(J, b, bounds)</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">else</span> raise error <span class="algo-comment">▷ unbounded / unknown status</span></span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-0"><span>decompose_KKT_multipliers(all_multipliers)</span></div>
<div class="algo-line"><span><span class="algo-keyword">end procedure</span></span></div>
</div>
</div>

An infeasible system (status `2`) means either that the primal solution returned by the solver is not exactly optimal, or that the problem does not satisfy constraint qualifications so that no exact multipliers exist. Rather than terminating, the framework prints a warning and falls back to the approximate multipliers of step 3.

### 2. Assembling the system — `compute_KKT_system_matrix_and_bounds()`

`compute_KKT_system_matrix_and_bounds()` is declared abstract in [`SubSystemInterface`](../api/Distributed_Design_Optimizer/subsystem/SubSystemInterface.md) and implemented separately in [`LocalSubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md) and [`ControllerSubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/ControllerSubSystemBasis.md), because local subsystems and the controller carry different constraint sets. It assembles the $J$ and the per-multiplier bounds ($\lambda_a \geq 0$ vs. free-sign) of the linear system above: each row of the returned constraint matrix is one active-constraint gradient $\nabla_{{}^{i}d} c_a$, in the same order as the corresponding entry of sym:\kappa_g, sym:\kappa_h, sym:\kappa_d, $\kappa_Q^{\leq}$, $\kappa_Q^{=}$ — a fixed order that both `compute_KKT_multipliers()` and `decompose_KKT_multipliers()` rely on:

- [`LocalSubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md):
  `( local equality | coordination equality | local inequality | coordination inequality | lower bounds | upper bounds )`, i.e. `( `sym:\kappa_h` | `$\kappa_Q^{=}$` | `sym:\kappa_g` | `$\kappa_Q^{\leq}$` | `sym:\kappa_d` (lower) | `sym:\kappa_d` (upper) `
- [`ControllerSubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/ControllerSubSystemBasis.md):
  `( coordination equality | coordination inequality | lower bounds | upper bounds )`, i.e. `( `$\kappa_Q^{=}$` | `$\kappa_Q^{\leq}$` | `sym:\kappa_d` (lower) | `sym:\kappa_d` (upper) ` — the controller has no local objective or local constraints.

For each candidate constraint the method decides both the Jacobian row and the multiplier bound:

- Equality constraints contribute their Jacobian row and a free-sign bound `(None, None)`.
- Active inequality constraints and bounds contribute their Jacobian row and a non-negativity bound `(0.0, None)`.
- Inactive inequality constraints and bounds contribute a zero row and the bound `(None, None)`; their multiplier has no impact on the system and is later reported as `None`.

The activity flags and component Jacobians are read from the subsystem's `OptimData` (e.g. `get_Jacobian_LocalEqualityConstraints()`, `get_ActiveLowerBounds()`), which are populated by the [Derivative Computation](derivative-computation.md). The method returns `[constraint_matrix, bounds]` — `constraint_matrix` becomes $J$ (once transposed by [step 1](#1-orchestration-compute_kkt_multipliers) above) and `bounds` encodes, entry for entry, whether each $\lambda_a$ is free-sign (equality) or non-negative (active inequality/bound), exactly as required by the stationarity condition above.

### 3. Fallback — `compute_ApproximateKKT_multipliers()`

Also defined in [`SubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/SubSystemBasis.md), this method is called by [step 1](#1-orchestration-compute_kkt_multipliers) only when the exact system is infeasible. It computes the multipliers that **minimize the violation** of the abbr:KKT stationarity condition in the squared $\ell_2$-norm,

\[
\min_{\lambda} \; \left\lVert J^{\top}\lambda + \nabla f \right\rVert_2^2
\quad \text{s.t.} \quad \lambda_a \geq 0 \; \text{for active inequality and bound constraints},
\]

by casting it into standard quadratic-program form and solving it with the `clarabel` solver from the `qpsolvers` package. The non-negativity requirement of active-constraint multipliers is encoded through the lower bounds; free-sign (equality) multipliers receive a lower bound of $-\infty$.

### 4. Distributing the result — `decompose_KKT_multipliers()`

The solver returns one flat multiplier vector. `decompose_KKT_multipliers()`, implemented in [`LocalSubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md) and [`ControllerSubSystemBasis`](../api/Distributed_Design_Optimizer/subsystem/ControllerSubSystemBasis.md), walks the vector with an index pointer in exactly the same order used to assemble the matrix and stores each slice on the subsystem's `OptimData` — for example `set_Multipliers_Local_Equality_Constraints()` (sym:\kappa_h), `set_Multipliers_Coordination_Equality_Constraints()` ($\kappa_Q^{=}$), and `set_Multipliers_Local_Inequality_Constraints()` (sym:\kappa_g). For inequality and bound constraints, inactive entries are stored as `None` so that the multiplier list stays aligned with the full constraint list.

### Where this is used in the workflow

The computation is triggered lazily and only from within a coordination-specific subsystem class, not from the shared solving workflow: `SubSystemBasis.check_MultipliersNotSet()` returns `True` when at least one existing constraint (local bound, local inequality/equality, or coordination equality) is missing its multiplier in `OptimData`. Only the `LocalSubSystem<Method>` (or `ControllerSubSystem<Method>`) classes of coordination methods that actually need the multipliers call the computation from their own `postprocess_Optimization()`, guarded by this check. Note that `compute_KKT_multipliers()` itself does not call `evaluateAllJacobians()` — the caller must run it first so that the Jacobians read by `compute_KKT_system_matrix_and_bounds()` are up to date:

<div class="collapsible-code" markdown>

```python
# LocalSubSystemALADIN.postprocess_Optimization() / LocalSubSystemSBDP.postprocess_Optimization()
self.evaluateAllJacobians()  # populate OptimData's gradients/Jacobians first
self.updateSubsystemfromOptimdata(self.get_OptimData())

if self.check_MultipliersNotSet():
    # Not all multipliers are provided by the solver -> reconstruct them from the KKT conditions.
    self.compute_KKT_multipliers()
self.updateSubsystemfromOptimdata(self.get_OptimData())
```

</div>
