---
title: Categorization and Selection of Suitable Solution Approaches
---

# Categorization and Selection of Suitable Solution Approaches

## All-At-Once Problem Formulation and Decomposition

To categorize solution approaches, a common starting point is the All-At-Once (abbr:AAO) optimization problem. It aggregates the design variables, constraints, and objectives of all subsystems $i \in \{0,\dots,m\} =:$ sym:M into a single problem. Shared design variables ${}^{i}_{j}$sym:z and ${}^{j}_{i}$sym:z between coupled subsystems $i$ and $j$ are condensed into a single variable \(sym:z_{\{i,j\}}\), yielding:

\[\begin{aligned}
\left\{{}^{i}sym:x^{*}\right\}_{i\in sym:M},\;\left\{sym:z_{\{i,j\}}^{*}\right\}_{\substack{j\in{}^{i}sym:N \\ i\in sym:M}} := \; & \argmin_{\substack{{}^{i}sym:x \;\in\; {}^{i}\mathcal{X} \;\forall\; i\in sym:M \\ sym:z_{\{i,j\}} \;\in\; {}^{i}_{j}\mathcal{Z} \cap {}^{j}_{i}\mathcal{Z} \;\forall\; j\in{}^{i}sym:N,\; i\in sym:M}} \quad \sum_{i\in sym:M} {}^{i}sym:v_f\!\left({}^{i}sym:r\right) \\
& \text{s.t.} \quad {}^{i}sym:v_g\!\left({}^{i}sym:r\right) \leq 0 \quad \forall\; i\in sym:M, \\
& \phantom{\text{s.t.}} \quad {}^{i}sym:v_h\!\left({}^{i}sym:r\right) = 0 \quad \forall\; i\in sym:M, \\
& \text{where} \quad {}^{i}sym:r := {}^{i}sym:r\!\left({}^{i}sym:x,\;\left\{sym:z_{\{i,j\}},\;{}^{j}_{i}sym:h\right\}_{j\in{}^{i}sym:N}\right) \quad \forall\; i\in sym:M, \\
& \phantom{\text{where}} \quad {}^{j}_{i}sym:h := {}^{j}_{i}sym:H\!\left({}^{j}sym:r\right) \quad \forall\; j\in{}^{i}sym:N,\; i\in sym:M.
\end{aligned}\]

Here, ${}^{i}$sym:r depends on both ${}^{i}$sym:x and neighboring subsystems' design variables through the coupling mapping identity \({}^{j}_{i}sym:h := {}^{j}_{i}sym:H\!\left({}^{j}sym:r\right)\).

To address these inter-subsystem dependencies, many approaches apply a *decomposition* [@dewitUnifiedApproach2009a; @tosseramsDistributedOptimization2008]: ${}^{j}_{i}$sym:h and ${}^{i}_{j}$sym:z are treated as additional design variables of subsystem $i$, and pairwise *coupling constraints* are introduced:

\[{}^{i}_{j}sym:c :=
\begin{bmatrix}
{}^{i}_{j}sym:c_{h} \\
{}^{i}_{j}sym:c_{z}
\end{bmatrix}
:=
\begin{bmatrix}
{}^{i}_{j}sym:H\!\left({}^{i}sym:r\right) - {}^{i}_{j}sym:h \\
{}^{i}_{j}sym:z - {}^{j}_{i}sym:z
\end{bmatrix}
= 0 \quad \forall\; j\in{}^{i}sym:N,\; i\in sym:M.\]

Redundant shared-variable constraints are omitted (only one of \({}^{i}_{j}sym:c_{z}=0\) and \({}^{j}_{i}sym:c_{z}=0\) is imposed). Each component is only introduced if the corresponding quantities exist. This yields the decomposed abbr:AAO formulation [@dewitUnifiedApproach2009a; @tosseramsDistributedOptimization2008]:

\[\begin{aligned}
\left\{{}^{i}sym:x^{*}\right\}_{i\in sym:M},\;\left\{{}^{i}_{j}sym:z^{*},\;{}^{j}_{i}sym:h^{*}\right\}_{\substack{j\in{}^{i}sym:N \\ i\in sym:M}} := \; & \argmin_{\substack{{}^{i}sym:x \;\in\; {}^{i}\mathcal{X} \;\forall\; i\in sym:M \\ {}^{i}_{j}sym:z \;\in\; {}^{i}_{j}\mathcal{Z} \;\forall\; j\in{}^{i}sym:N,\; i\in sym:M \\ {}^{j}_{i}sym:h \;\in\; {}^{j}_{i}\mathcal{H} \;\forall\; j\in{}^{i}sym:N,\; i\in sym:M}} \quad \sum_{i\in sym:M} {}^{i}sym:v_f\!\left({}^{i}sym:r\right) \\
& \text{s.t.} \quad {}^{i}sym:v_g\!\left({}^{i}sym:r\right) \leq 0 \quad \forall\; i\in sym:M, \\
& \phantom{\text{s.t.}} \quad {}^{i}sym:v_h\!\left({}^{i}sym:r\right) = 0 \quad \forall\; i\in sym:M, \\
& \phantom{\text{s.t.}} \quad {}^{i}_{j}sym:c = 0 \quad \forall\; j\in{}^{i}sym:N,\; i\in sym:M, \\
& \text{where} \quad {}^{i}sym:r := {}^{i}sym:r\!\left({}^{i}sym:x,\;\left\{{}^{i}_{j}sym:z,\;{}^{j}_{i}sym:h\right\}_{j\in{}^{i}sym:N}\right) \quad \forall\; i\in sym:M.
\end{aligned}\]

The bound set ${}^{j}_{i}\mathcal{H}$ must be chosen to preserve equivalence with the original abbr:AAO problem (achievable by selecting an unbounded set). Unlike the original formulation, the decomposed version makes response ${}^{i}$sym:r depend solely on the design variables ${}^{i}$sym:x, ${}^{i}_{j}$sym:z, ${}^{j}_{i}$sym:h of subsystem $i$.

## Monolithic and Distributed Approaches

Solution approaches are first categorized by whether a *single* or *multiple* optimization routines determine design variables [@tosseramsDistributedOptimization2008]. Single-optimizer approaches are called *monolithic* [@mdobook; @martinsMultidisciplinaryDesign2013a]. Individual Discipline Feasible (abbr:IDF) operates on the decomposed formulation. A single optimizer determines ${}^{i}$sym:x, ${}^{i}_{j}$sym:z, ${}^{j}_{i}$sym:h $\;\forall\; j\in{}^{i}$sym:N, $i\in$sym:M and enforces all constraints (local and coupling) via its built-in constraint handling [@brevaultMultidisciplinarySystem2020a; @martinsMultidisciplinaryDesign2013a; @allisonOptimalPartitioning2009].
Multidisciplinary Feasible (abbr:MDF) operates on the original abbr:AAO problem directly. For each candidate set of design variables, a *convergence driver* (typically a Fixed-Point Iteration (abbr:FPI) scheme such as Gauss–Seidel or Jacobi) iterates the coupled response functions to mutual consistency before the optimizer proposes new variables [@mdobook; @brevaultMultidisciplinarySystem2020a; @martinsMultidisciplinaryDesign2013a]:

\[\begin{aligned}
{}^{0}sym:r &:= {}^{0}sym:r\!\left({}^{0}sym:x,\;\left\{sym:z_{\{0,j\}},\;{}^{j}_{0}sym:H\!\left({}^{j}sym:r\right)\right\}_{j\in{}^{0}sym:N}\right) \\
&\;\;\vdots \\
{}^{m}sym:r &:= {}^{m}sym:r\!\left({}^{m}sym:x,\;\left\{sym:z_{\{m,j\}},\;{}^{j}_{m}sym:H\!\left({}^{j}sym:r\right)\right\}_{j\in{}^{m}sym:N}\right)
\end{aligned}\]

Software frameworks such as [OpenMDAO](https://openmdao.org/) and [GEMSEO](https://gemseo.org/) support abbr:MDF/abbr:IDF approaches. Crucially, while monolithic methods allow distributed *evaluation* of local responses ${}^{i}$sym:r, the decision-making (i.e., determining optimal design variables) remains centralized [@wangNetworkTarget2012a; @allisonOptimalPartitioning2009; @tosseramsDistributedOptimization2008]. This framework provides *distributed* approaches instead.

*Distributed* solution approaches decompose the abbr:AAO problem into an equivalent set of coupled optimization subproblems, each solved by its own coordinated optimizer [@mdobook; @martinsMultidisciplinaryDesign2013a; @tosseramsDistributedOptimization2008]. Prominent methods include Collaborative Optimization (abbr:CO), Concurrent SubSpace Optimization (abbr:CSSO), abbr:BLISS, abbr:BLISS-2000, Analytical Target Cascading (abbr:ATC), and Augmented Lagrangian Coordination (abbr:ALC) [@mdobook; @brevaultMultidisciplinarySystem2020a; @tosseramsDistributedOptimization2008; @blouinIntrinsicAnalysis2004].

abbr:ALC belongs to the class of *primal-dual* approaches [@engelmannDistributedOptimization2022]. Pure *primal* methods also exist, but most cannot handle nonconvex local constraints [@engelmannDistributedOptimization2022]. A notable exception is Sensitivity-Based Distributed Programming (abbr:SBDP) [@voneschSensitivityBasedDistributed2025].

Our previous publication [insert link to review paper] identified relaxation-based primal-dual approaches (such as abbr:ALC) and abbr:SBDP — which grant subsystem autonomy over local and shared design variables and support bidirectional coupling — as the most suitable approaches for distributed design optimization.

The following sections apply these most promising approaches to the decomposed problem formulation above. First, representative distributed primal-dual methods based on Lagrangian relaxation of coupling constraints are derived: [abbr:ALC](coordination-methods/augmented-lagrangian-coordination.md) and [abbr:ALADIN](coordination-methods/aladin.md). Then, [abbr:SBDP](coordination-methods/sensitivity-based-distributed-programming.md) is considered for the same formulation. Alternatively, these approaches can also be applied to a [*consensus* reformulation](coordination-methods/consensus-augmented-lagrangian-coordination.md). Finally, a [unified algorithmic structure](unified-algorithmic-structure.md) is identified.

## Primal Problem (Compact Notation)

Before detailing algorithmic structures, the decomposed problem is rewritten in compact form. The local, shared, and coupling design variables of subsystem $i$ are stacked into a combined *design variable vector* ${}^{i}$sym:d:

\[{}^{i}sym:d :=
\begin{bmatrix}
{}^{i}sym:x \\
\left\{{}^{i}_{j}sym:z\right\}_{j\in{}^{i}sym:N} \\
\left\{{}^{j}_{i}sym:h\right\}_{j\in{}^{i}sym:N}
\end{bmatrix}
\in\;
{}^{i}sym:\mathcal{D}
:=
{}^{i}\mathcal{X}
\times
\prod_{j\in{}^{i}sym:N} {}^{i}_{j}\mathcal{Z}
\times
\prod_{j\in{}^{i}sym:N} {}^{j}_{i}\mathcal{H}.\]

The bound constraint \({}^{i}sym:d \in {}^{i}sym:\mathcal{D}\) can equivalently be expressed as an inequality:

\[{}^{i}sym:v_{\mathcal{D}}\!\left({}^{i}sym:d\right) :=
\begin{bmatrix}
{}^{i}sym:d_{1} - {}^{i}\bar{sym:d}_{1} \\
{}^{i}\underline{sym:d}_{1} - {}^{i}sym:d_{1} \\
\vdots \\
{}^{i}sym:d_{n_d} - {}^{i}\bar{sym:d}_{n_d} \\
{}^{i}\underline{sym:d}_{n_d} - {}^{i}sym:d_{n_d}
\end{bmatrix}
\leq 0.\]

Individual components of ${}^{i}$sym:d are retrieved via selector matrices:

\[{}^{i}_{j}sym:S_{z}\;{}^{i}sym:d = {}^{i}_{j}sym:z, \qquad {}^{j}_{i}sym:S_{h}\;{}^{i}sym:d = {}^{j}_{i}sym:h.\]

Coupling constraints now depend on ${}^{i}$sym:d and ${}^{j}$sym:d:

\[{}^{i}_{j}sym:c\!\left({}^{i}sym:d,\;{}^{j}sym:d\right) :=
\begin{bmatrix}
{}^{i}_{j}sym:H\!\left({}^{i}sym:r\right) - {}^{i}_{j}sym:h \\
{}^{i}_{j}sym:z - {}^{j}_{i}sym:z
\end{bmatrix}
= 0.\]

Using this notation, the decomposed problem is rewritten as the *primal problem*:

\[\begin{aligned}
\left\{{}^{i}sym:d^{*}\right\}_{i\in sym:M} := \; & \argmin_{{}^{i}sym:d \;\in\; {}^{i}sym:\mathcal{D} \;\forall\; i\in sym:M} \quad \sum_{i\in sym:M} {}^{i}sym:v_f\!\left({}^{i}sym:r\right) \\
& \text{s.t.} \quad {}^{i}sym:v_g\!\left({}^{i}sym:r\right) \leq 0 \quad \forall\; i\in sym:M, \\
& \phantom{\text{s.t.}} \quad {}^{i}sym:v_h\!\left({}^{i}sym:r\right) = 0 \quad \forall\; i\in sym:M, \\
& \phantom{\text{s.t.}} \quad {}^{i}_{j}sym:c\!\left({}^{i}sym:d,\;{}^{j}sym:d\right) = 0 \quad \forall\; j\in{}^{i}sym:N,\; i\in sym:M, \\
& \text{where} \quad {}^{i}sym:r := {}^{i}sym:r\!\left({}^{i}sym:d\right) \quad \forall\; i\in sym:M.
\end{aligned}\]

For readability, the response identity \({}^{i}sym:r := {}^{i}sym:r\!\left({}^{i}sym:d\right)\) is omitted in the remainder of this work.