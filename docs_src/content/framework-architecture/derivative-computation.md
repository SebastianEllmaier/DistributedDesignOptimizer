---
title: Derivative Computation
---

# Derivative Computation

Several coordination methods — for example [abbr:ALADIN](../distributed-optimization-for-multidisciplinary-design/coordination-methods/aladin.md) and [abbr:SBDP](../distributed-optimization-for-multidisciplinary-design/coordination-methods/sensitivity-based-distributed-programming.md) — need first- and sometimes second-order derivative information of each subsystem's objective sym:v_f, constraints sym:v_h & sym:v_g and mapped sym:H(r) responses.

The abbr:DDO framework lets the user supply **as much or as little** derivative information in `Analysis<id>`, `LocalObjective<id>` and `LocalConstraints<id>` (see [Tutorial > Problem Definition and Algorithm Execution](../tutorial/problem-definition-and-algorithm-execution/index.md)) as they know, and transparently fills every remaining gap: missing first-order entries are approximated by finite differences ([`FiniteDifferencesJacobian`](../api/Distributed_Design_Optimizer/subsystem/tools/FiniteDifferencesJacobian.md)), and missing second-order information is approximated by a BFGS update ([`HessianApproximationBFGS`](../api/Distributed_Design_Optimizer/subsystem/tools/HessianApproximationBFGS.md)).

## User-provided derivative interfaces

Users express whatever derivatives they know by implementing the (optional) derivative methods of three interfaces, listed below. Most of these methods **return** the derivative they compute — an objective gradient, a constraint Jacobian, or a (list of) Hessian(s) — as a nested list whose unknown entries are simply left as `None`. The single exception is `mapLocalResponsesDesignVariables_to_CouplingParameters_Jacobians()`, which does not return anything: it writes each neighbor's mapped-response Jacobian through the setter `set_MappedResponses_Jacobian(id=, mappedresponses_jacobian_in=)`. Whatever is left as `None` — a whole matrix or individual entries — is filled in transparently by the fallback machinery described below.

<table class="doc-table">
  <thead>
    <tr>
      <th>Interface</th>
      <th>Derivative methods</th>
      <th>Quantity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td markdown="span" rowspan="2">[`LocalObjectiveInterface`](../api/Distributed_Design_Optimizer/subsystem/optimization/designproblem/LocalObjectiveInterface.md)</td>
      <td markdown="span">`evaluate_Gradient_LocalObjective()`</td>
      <td markdown="span">Gradient of the local objective</td>
    </tr>
    <tr>
      <td markdown="span">`evaluate_Hessian_LocalObjective()`</td>
      <td markdown="span">Hessian of the local objective</td>
    </tr>
    <tr>
      <td markdown="span" rowspan="4">[`LocalConstraintsInterface`](../api/Distributed_Design_Optimizer/subsystem/optimization/designproblem/LocalConstraintsInterface.md)</td>
      <td markdown="span">`evaluate_Jacobian_EqualityLocalConstraints()`</td>
      <td markdown="span">Jacobian of local equality constraints</td>
    </tr>
    <tr>
      <td markdown="span">`evaluate_Jacobian_InEqualityLocalConstraints()`</td>
      <td markdown="span">Jacobian of local inequality constraints</td>
    </tr>
    <tr>
      <td markdown="span">`evaluate_Hessians_EqualityLocalConstraints()`</td>
      <td markdown="span">Hessians of local equality constraints</td>
    </tr>
    <tr>
      <td markdown="span">`evaluate_Hessians_InEqualityLocalConstraints()`</td>
      <td markdown="span">Hessians of local inequality constraints</td>
    </tr>
    <tr>
      <td markdown="span" rowspan="2">[`AnalysisInterface`](../api/Distributed_Design_Optimizer/subsystem/optimization/AnalysisInterface.md)</td>
      <td markdown="span">`mapLocalResponsesDesignVariables_to_CouplingParameters_Jacobians()`</td>
      <td markdown="span">Jacobians of the mapped coupling responses</td>
    </tr>
    <tr>
      <td markdown="span">`mapLocalResponsesDesignVariables_to_CouplingParameters_Hessian()`</td>
      <td markdown="span">Hessians of the mapped coupling responses</td>
    </tr>
  </tbody>
</table>

The coordination-objective gradient and the coordination-constraint Jacobians are not user-facing: they are derived internally from the formulation of each coordination method. [`SubSystemInterface`](../api/Distributed_Design_Optimizer/subsystem/SubSystemInterface.md) declares `evaluate_Gradient_CoordinationObjective()`, `evaluate_Jacobian_CoordinationEqualityConstraints()` and `evaluate_Jacobian_CoordinationInEqualityConstraints()`, and each coordination method's `LocalSubSystem<Method>` class (e.g. [`LocalSubSystemALC`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemALC.md), [`LocalSubSystemALADIN`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemALADIN.md), [`LocalSubSystemSBDP`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemSBDP.md)) overrides them with its own coordination formulation — filling in analytic entries where available and otherwise leaving them `None` for the finite-difference / BFGS fallback described below.

When adding a new use-case, implementing the derivative methods of the three interfaces above is entirely optional: they can be left empty to rely on finite differences and BFGS, or filled with whatever analytic entries are known to improve accuracy and reduce analysis calls. The [GeometricProgramming](../examples/GeometricProgramming/index.md) example demonstrates the fully analytic path — `LocalObjective0` returns an analytic gradient and Hessian and `LocalConstraints0` returns analytic constraint Jacobians and Hessians — whereas the [SSBJ](../examples/SSBJ/index.md) example keeps its mapped-response Jacobians as all-`None` matrices of the correct shape so the framework finite-differences them (its underlying physics has no closed form). See [Tutorial > Novel Distributed Optimization Method](../tutorial/novel-distributed-optimization-method/index.md#3-defining-the-coordination-specific-subsystem-classes) for where subsystem classes plug into this machinery.

### Scaled-space convention

The optimizer works entirely in the **scaled** $[0, 1]$ design domain, so every user-provided derivative is expected in that same scaled space. Because each scaler is affine with a constant slope $s = $ `scaler.get_scale()` $ = \mathrm{d}(\text{scaled})/\mathrm{d}(\text{unscaled})$, converting an analytic partial computed in physical (unscaled) units is a plain chain-rule rescaling:

\[
\frac{\partial(\text{scaled } y)}{\partial(\text{scaled } d_j)} = \frac{s_y}{s_{d_j}}\,\frac{\partial y}{\partial d_j},
\]

where $s_{d_j}$ is the slope of the $j$-th design-variable scaler and $s_y$ the slope of the scaler of the differentiated quantity $y$ (objective, constraint or mapped response; $s_y = 1$ for a quantity that is itself left unscaled). Second-order terms rescale analogously with an additional factor $1/s_{d_k}$ per extra derivative direction. The [Tutorial](../tutorial/problem-definition-and-algorithm-execution/index.md) examples carry `# === Tutorial: scaled <-> unscaled ... (chain rule) ===` comment blocks inside each derivative method showing this conversion in place.

## Coordination-objective and coordination-constraint derivatives

The *value* of the coordination-specific terms — sym:P (or, for methods with dedicated coordination constraints, sym:Q^{\leq} and sym:Q^{=}) — is evaluated every solver iteration: `LocalSubSystemBasis.evaluateTotalObjective()` calls `evaluateCoordinationObjective()`, and `evaluateTotalConstraint()` calls `evaluateCoordinationEqualityConstraint()` and `evaluateCoordinationInequalityConstraint()`, each overridden per coordination method to compute the value from that method's penalty / augmented-Lagrangian / consensus formulation (see [SubSystem Optimization](subsystem-optimization.md)). The corresponding *derivative* methods `evaluate_Gradient_CoordinationObjective()`, `evaluate_Jacobian_CoordinationEqualityConstraints()` and `evaluate_Jacobian_CoordinationInEqualityConstraints()` are a separate, independent set of overrides on the same `LocalSubSystem<Method>` class, only consulted by the Orchestration step below via `evaluateAllJacobians()`.

Inspecting the current coordination methods shows that none of them fill in the coordination-objective gradient analytically — [`LocalSubSystemALC`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemALC.md), [`LocalSubSystemConsensusALC`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemConsensusALC.md), [`LocalSubSystemLC`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemLC.md), [`LocalSubSystemPC`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemPC.md), [`LocalSubSystemALADIN`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemALADIN.md) and [`LocalSubSystemSBDP`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemSBDP.md) all leave `evaluate_Gradient_CoordinationObjective()` unimplemented (marked `# TODO`), relying entirely on finite differences whenever it is actually consulted. Coordination *constraints* only exist for [abbr:SBDP](../distributed-optimization-for-multidisciplinary-design/coordination-methods/sensitivity-based-distributed-programming.md), whose hard equality constraint sym:c_h, sym:c_z is computed analytically in `evaluateCoordinationEqualityConstraint()`; its Jacobian `evaluate_Jacobian_CoordinationEqualityConstraints()` is nonetheless still `# TODO` (again deferring to finite differences). All other methods (ALC and its variants, Consensus ALC, LC, PC, ALADIN) have no coordination constraints at all — their coupling is instead enforced through the coordination objective sym:P (a penalty / augmented-Lagrangian term for ALC-family methods and Consensus ALC, or the regularization term for ALADIN) — so their `evaluate_Jacobian_CoordinationEqualityConstraints()` / `evaluate_Jacobian_CoordinationInEqualityConstraints()` are simple no-ops.

As with the user-facing interfaces above, implementing these coordination-derivative overrides is entirely optional when adding a new coordination method: they can be left as no-ops (as every built-in method currently does) to rely on finite differences and BFGS, or filled with analytic entries to improve accuracy and reduce analysis calls. See [Tutorial > Novel Distributed Optimization Method](../tutorial/novel-distributed-optimization-method/index.md#3-defining-the-coordination-specific-subsystem-classes) for where subsystem classes plug into this machinery.

## First-order approximation — `FiniteDifferencesJacobian`

[`FiniteDifferencesJacobian`](../api/Distributed_Design_Optimizer/subsystem/tools/FiniteDifferencesJacobian.md) approximates, by perturbing the design variables, every first-order quantity listed above.

The routine operates on the design variables. The per-direction step size $\varepsilon_j$ is derived from each design variable's *granularity*.

For each perturbed direction $j$ the method chooses the difference scheme according to the box bounds, so that no perturbation ever leaves the feasible interval. Writing $e_j$ for the $j$-th unit vector, the three admissible schemes are

\[
\frac{\partial(\cdot)}{\partial d_j} \approx
\begin{cases}
\dfrac{(\cdot)(sym:d + \varepsilon_j e_j) - (\cdot)(sym:d - \varepsilon_j e_j)}{2\varepsilon_j}, & \text{central: both } sym:d + \varepsilon_j e_j,\; sym:d - \varepsilon_j e_j \text{ feasible},\\[2ex]
\dfrac{(\cdot)(sym:d + \varepsilon_j e_j) - (\cdot)(sym:d)}{\varepsilon_j}, & \text{forward: only } sym:d + \varepsilon_j e_j \text{ feasible},\\[2ex]
\dfrac{(\cdot)(sym:d) - (\cdot)(sym:d - \varepsilon_j e_j)}{\varepsilon_j}, & \text{backward: only } sym:d - \varepsilon_j e_j \text{ feasible}.
\end{cases}
\]

Each perturbation is applied through `updateSubsystem()`, which sets the perturbed design variables and re-runs the analysis, mapping, objective, and constraint evaluations so that every dependent quantity is refreshed before the difference is taken.

## Orchestration — `evaluateAllJacobians()`

The merge of user-provided and finite-difference derivatives happens in [`LocalSubSystemBasis.evaluateAllJacobians()`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md). It (1) collects whatever the user provides, (2) determines which directions are still missing, (3) runs finite differences **once** over the union of those directions, and (4) writes the approximations into the `None` slots only.

The design-variable **bound** Jacobians (active lower / upper bounds) are always assembled by the framework itself, and the **total** objective gradient and constraint Jacobians are finally composed from the local and coordination parts.

## Second-order information — `HessianApproximationBFGS`

Methods that need Hessians (notably [abbr:ALADIN](../distributed-optimization-for-multidisciplinary-design/coordination-methods/aladin.md)) obtain them through [`HessianApproximationBFGS`](../api/Distributed_Design_Optimizer/subsystem/tools/HessianApproximationBFGS.md), a subclass of `scipy.optimize.BFGS`. It maintains, across coordination iterations, a curvature-based approximation of the Hessian of a scalar function (the local objective, or an individual constraint / mapped-response component) from successive gradient evaluations.

Because the BFGS estimate depends on the whole gradient history, [`LocalSubSystemALADIN.evaluateAllHessians()`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemALADIN.md) advances the approximation **every** iteration. The merge with user-provided Hessians is, however, *all-or-nothing per matrix* rather than entry-wise: if the user's Hessian for a given function is `None` **or contains any `None` entry**, the complete BFGS matrix is used for that function; only a fully specified user Hessian is taken as-is. A separate BFGS object is kept for the local objective and for each local equality constraint, local inequality constraint, and mapped-response component.

## Where this is used in the workflow

[`evaluateAllJacobians()`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemBasis.md) is implemented once in `LocalSubSystemBasis`, but it is not called automatically after every local optimization — each coordination method's `LocalSubSystem<Method>.postprocess_Optimization()` decides whether its coordination scheme actually needs gradients / Jacobians and, if so, calls `evaluateAllJacobians()` itself. Currently [`LocalSubSystemALADIN`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemALADIN.md) and [`LocalSubSystemSBDP`](../api/Distributed_Design_Optimizer/subsystem/LocalSubSystemSBDP.md) call it, so that the gradients and Jacobians are evalauted at the optimal desing varibal point sym:d. Methods that also require curvature, such as [abbr:ALADIN](../distributed-optimization-for-multidisciplinary-design/coordination-methods/aladin.md), additionally call `evaluateAllHessians()` to assemble the Hessian of the Lagrangian exchanged with the controller. Methods whose coordination scheme needs neither derivative order (for example standard [abbr:ALC](../distributed-optimization-for-multidisciplinary-design/coordination-methods/augmented-lagrangian-coordination.md), which updates its multipliers and weights by a subgradient rule) leave `postprocess_Optimization()` empty and simply never trigger these routines.