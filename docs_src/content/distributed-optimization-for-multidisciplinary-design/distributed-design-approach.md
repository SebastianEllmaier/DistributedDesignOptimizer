---
title: Distributed Design Approach
---

# Distributed Design Approach

Competitive engineering systems require tight integration of multiple disciplines (mechanics, electrics, software) [@kruegerFunktionaleSynthese2024; @isermannDesignsSpecification2023; @guerineauDESIGNMETHODSELECTION2018], which increases development complexity. A coherent early-phase conceptual design is therefore crucial to shorten timelines and avoid costly later corrections [@tanRelativeImpact2017; @SEH25; @christopheConceptualDesign2014].
Multidisciplinary Design Optimization (abbr:MDO) uses algorithms to find feasible and optimal multi-component designs [@brevaultMultidisciplinarySystem2020a; @martinsMultidisciplinaryDesign2013a; @tosseramsDistributedOptimization2008].

Complex design tasks are typically *partitioned* into subtasks solved by specialized subteams [@engelmannDistributedOptimization2022; @safaviCollaborativeMultidisciplinary2016a; @tosseramsDistributedOptimization2008]. This is both necessary and advantageous [@wangNetworkTarget2012a; @xieDynamicContributionbased2009]:

- *Divide-and-conquer* yields manageable subtasks.
- Subtasks can be executed in parallel, shortening development time.
- No single engineer can master all required fields (electronics, mechanics, etc.).
- Dedicated tools (e.g., abbr:FEM, abbr:CFD) are inherently partitioned by vendor or infrastructure.

Partitioning demands frequent communication between subteams to maintain design coherence [@papageorgiouRoleMultidisciplinary2017a; @martinsMultidisciplinaryDesign2013a]. As an example, the Supersonic Business Jet (abbr:SSBJ) design (adapted from [@BenchmarkProblems; @dewitUnifiedApproach2009a; @sobieszczanski-sobieskiBiLevelIntegrated1998]) is partitioned into the subtasks shown below:

<iframe src="../FIGURE_SSBJ_distributed_design_appraoch.drawio.html" width="100%" height="500" style="border:none;" allowfullscreen></iframe>

Once partitioned into coupled subsystems, optimization algorithms can efficiently explore the large design spaces characteristic of early conceptual phases [@brevaultMultidisciplinarySystem2020a; @safaviCollaborativeMultidisciplinary2016a; @tosseramsDistributedOptimization2008]. However, engineers must formulate each subtask as a mathematical optimization problem [@bilMultidisciplinaryDesign2015a; @allisonOptimalPartitioning2009].

Adopting the notation from [@dewitUnifiedApproach2009a] (similar to [@stephanopoulosUseHestenes1975]), the optimization problem of subsystem $i$ reads:

\[\begin{aligned}
{}^{i}sym:x^{*},\;\left\{{}^{i}_{j}sym:z^{*}\right\}_{j\in{}^{i}sym:N} := \; & \argmin_{\substack{{}^{i}sym:x \;\in\; {}^{i}\mathcal{X} \\ {}^{i}_{j}sym:z \;\in\; {}^{i}_{j}\mathcal{Z} \;\forall\; j\in{}^{i}sym:N}} \quad {}^{i}sym:v_f\!\left({}^{i}sym:r\right) \\
& \text{s.t.} \quad {}^{i}sym:v_g\!\left({}^{i}sym:r\right) \leq 0, \\
& \phantom{\text{s.t.}} \quad {}^{i}sym:v_h\!\left({}^{i}sym:r\right) = 0, \\
& \text{where} \quad {}^{i}sym:r := {}^{i}sym:r\!\left({}^{i}sym:x,\;\left\{{}^{i}_{j}sym:z,\;{}^{j}_{i}sym:h\right\}_{j\in{}^{i}sym:N}\right).
\end{aligned}\]

The notation is summarized as follows:

<table class="doc-table">
  <thead>
    <tr>
      <th>Symbol</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>${}^{i}$sym:x</td>
      <td><em>Local design variables</em> of subsystem $i$ within bounds ${}^{i}\mathcal{X}$</td>
    </tr>
    <tr>
      <td>${}^{i}_{j}$sym:z</td>
      <td><em>Shared design variables</em> with neighbor $j$ within bounds ${}^{i}_{j}\mathcal{Z}$</td>
    </tr>
    <tr>
      <td>${}^{i}$sym:N</td>
      <td>Index set of all neighbors $j$ coupled to subsystem $i$</td>
    </tr>
    <tr>
      <td>${}^{i}$sym:v_f</td>
      <td><em>Objective function</em></td>
    </tr>
    <tr>
      <td>${}^{i}$sym:v_g, ${}^{i}$sym:v_h</td>
      <td><em>Inequality</em> and <em>equality constraints</em></td>
    </tr>
    <tr>
      <td>${}^{i}$sym:r</td>
      <td><em>Response function</em></td>
    </tr>
    <tr>
      <td>${}^{j}_{i}$sym:h</td>
      <td><em>Coupling variable</em> provided by neighbor $j$</td>
    </tr>
    <tr>
      <td>${}^{j}_{i}$sym:H</td>
      <td><em>Coupling function</em> (mapping) from subsystem $j$ to $i$</td>
    </tr>
  </tbody>
</table>

The coupling variable is defined as:

\[{}^{j}_{i}sym:h := {}^{j}_{i}sym:H\!\left({}^{j}sym:r\right),\]

where the expression \({}^{j}_{i}sym:H\!\left({}^{j}sym:r\right)\) is called the *mapped response* of subsystem $j$ to $i$.

The figure below translates the abbr:SSBJ partitioning into the mathematical notation above.

<iframe src="../FIGURE_SSBJ_distributed_optimization_problem_modelling.drawio.html" width="100%" height="500" style="border:none;" allowfullscreen></iframe>

The abbr:SSBJ example is also used as an illustration in [Tutorial > Problem Defintion and Algorithm Execution](../tutorial/problem-definition-and-algorithm-execution/index.md) and [Tutorial > Processing](../tutorial/processing/index.md). 
Further infromation on the abbr:SSBJ can be found in the [SSBJ example](../examples/SSBJ/index.md).
