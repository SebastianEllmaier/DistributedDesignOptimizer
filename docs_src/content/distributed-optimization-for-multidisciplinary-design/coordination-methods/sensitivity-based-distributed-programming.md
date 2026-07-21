---
title: Sensitivity Based Distributed Programming (SBDP)
---


# Sensitivity Based Distributed Programming (SBDP)

abbr:SBDP [@voneschEnforcingConvergence2025; @voneschSensitivityBasedDistributed2025] augments each subsystem's objective with a first-order sensitivity correction that approximates how changes in ${}^{i}$sym:d affect the Lagrangians of neighboring subsystems. This section applies the framework to the [primal problem](../categorization-and-selection-of-suitable-solution-approaches.md#primal-problem-compact-notation).

Each coupling constraint is *assigned* to exactly one subsystem. Here ${}^{i}_{j}$sym:c belongs to subsystem $i$, simplifying the correction term. The constraint \({}^{i}_{j}sym:c\!\left({}^{i}sym:d,\;{}^{j}sym:d\right)\) is kept in subsystem $i$'s problem with \({}^{j}sym:d\) fixed at its previous iterate for decoupling [@voneschSensitivityBasedDistributed2025; @voneschEnforcingConvergence2025]. The full procedure is given in [Algorithm 3](#algorithm-3).

The total Lagrangian reads

\[\begin{aligned}
sym:L
:={} &
\sum_{i\in sym:M}
\Biggl(
{}^{i}sym:v_f\!\left({}^{i}sym:r\right)
+
{}^{i}sym:\kappa_g^{T}\,
{}^{i}sym:v_g\!\left({}^{i}sym:r\right)
+
{}^{i}sym:\kappa_h^{T}\,
{}^{i}sym:v_h\!\left({}^{i}sym:r\right)
+
{}^{i}sym:\kappa_d^{T}\,
{}^{i}sym:v_D\!\left({}^{i}sym:d\right)
\\
& \quad\quad\;\; +
\sum_{j\in{}^{i}sym:N}
{}^{i}_{j}sym:\lambda^{T}\,
{}^{i}_{j}sym:c\!\left({}^{i}sym:d,\;{}^{j}sym:d\right)
\Biggr),
\end{aligned}\]

which partitions into subsystem-local Lagrangians

\[sym:L
=
\sum_{i\in sym:M}
{}^{i}sym:L\!\left({}^{i}sym:d,\;\left\{{}^{j}sym:d\right\}_{j\in{}^{i}sym:N}\right),\]

with

\[\begin{aligned}
{}^{i}sym:L\!\left({}^{i}sym:d,\;\left\{{}^{j}sym:d\right\}_{j\in{}^{i}sym:N}\right)
:={} &
{}^{i}sym:v_f\!\left({}^{i}sym:r\right)
+
{}^{i}sym:\kappa_g^{T}\,
{}^{i}sym:v_g\!\left({}^{i}sym:r\right)
+
{}^{i}sym:\kappa_h^{T}\,
{}^{i}sym:v_h\!\left({}^{i}sym:r\right)
+
{}^{i}sym:\kappa_d^{T}\,
{}^{i}sym:v_D\!\left({}^{i}sym:d\right)
\\
&+
\sum_{j\in{}^{i}sym:N}
{}^{i}_{j}sym:\lambda^{T}\,
{}^{i}_{j}sym:c\!\left({}^{i}sym:d,\;{}^{j}sym:d\right).
\end{aligned}\]

The sensitivity correction for subsystem $i$ is the derivative of \({}^{j}sym:L\) with respect to \({}^{i}sym:d\) at iterate sym:k. Since \({}^{j}sym:v_f\), \({}^{j}sym:v_g\), \({}^{j}sym:v_h\), \({}^{j}sym:v_D\) depend only on \({}^{j}sym:d\), only the coupling term ${}^{j}_{i}$sym:c contributes to \(\nabla_{{}^{i}sym:d}{}^{j}sym:L^{(sym:k)}\):

\[\begin{aligned}
\nabla_{{}^{i}sym:d}{}^{j}sym:L^{(sym:k)}
={} &
\nabla_{{}^{i}sym:d}^{T}\,
{}^{j}_{i}sym:c\!\left({}^{j}sym:d,\;{}^{i}sym:d\right)\,
{}^{j}_{i}sym:\lambda^{(sym:k)}
\\
={} &
\begin{bmatrix}
-{}^{j}_{i}sym:S_{h} \\
-{}^{i}_{j}sym:S_{z}
\end{bmatrix}^{T}
\begin{bmatrix}
{}^{j}_{i}sym:\lambda_{h}^{(sym:k)} \\
{}^{j}_{i}sym:\lambda_{z}^{(sym:k)}
\end{bmatrix}
\end{aligned}\]

For convergence analysis and necessary assumptions, see [@voneschEnforcingConvergence2025; @voneschSensitivityBasedDistributed2025]. After the original abbr:SBDP publication [@voneschSensitivityBasedDistributed2025], modifications improving convergence were proposed, yielding abbr:SBDP+ [@voneschEnforcingConvergence2025].

All symbols are defined in the [Nomenclature](../../includes/index.md).

<div class="algorithm" id="algorithm-3" markdown="0">
<div class="algorithm-caption"><strong>Algorithm 3</strong> Sensitivity Based Distributed Programming (abbr:SBDP)</div>
<div class="algo-body">
<div class="algo-line"><span><span class="algo-keyword">Require:</span> hyperparameter \(sym:\epsilon_k\)</span></div>
<div class="algo-line"><span><span class="algo-keyword">Require:</span> initial \({}^{j}_{i}sym:\lambda,\; {}^{i}_{j}sym:h,\; {}^{j}_{i}sym:z\) in interface storage \(i \leftrightarrow j \;\; \forall\; j \in {}^{i}sym:N,\; i \in sym:M\)</span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line"><span>\(sym:k \leftarrow 0\) <span class="algo-comment">▷ initialize outerloop iterator</span></span></div>
<div class="algo-line"><span><span class="algo-keyword">repeat</span></span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">for every</span> \(i \in sym:M\) <span class="algo-keyword">in parallel do</span></span></div>
<div class="algo-line algo-indent-2"><span>Copy \({}^{j}_{i}sym:\lambda,\; {}^{j}_{i}sym:H\!\left({}^{j}sym:r\right),\; {}^{i}_{j}sym:h,\; {}^{j}_{i}sym:z\) from interface storage \(i \leftrightarrow j \;\; \forall\; j \in {}^{i}sym:N\)</span></div>
<div class="algo-line algo-indent-2"><span>Determine \(\nabla_{{}^{i}sym:d}{}^{j}sym:L^{(sym:k)} \;\; \forall\; j \in {}^{i}sym:N\)</span></div>
<div class="algo-math-block">
<span>

\[\begin{aligned}
{}^{i}sym:d^{(sym:k+1)} \leftarrow{} & \argmin_{{}^{i}sym:d \;\in\; {}^{i}sym:\mathcal{D}} \;\;
{}^{i}sym:v_f\!\left({}^{i}sym:r\right)
+ \sum_{j \in {}^{i}sym:N} \left(
\bigl(\nabla_{{}^{i}sym:d}{}^{j}sym:L^{(sym:k)}\bigr)^{T}
\left({}^{i}sym:d - {}^{i}sym:d^{(sym:k)}\right)
\right) \\
& \text{s.t.} \;\; {}^{i}sym:v_g\!\left({}^{i}sym:r\right) \leq 0, \\
& \phantom{\text{s.t.}} \;\; {}^{i}sym:v_h\!\left({}^{i}sym:r\right) = 0, \\
& \phantom{\text{s.t.}} \;\;
\begin{bmatrix}
{}^{i}_{j}sym:H\!\left({}^{i}sym:r\right) - {}^{i}_{j}sym:h \\
{}^{i}_{j}sym:S_{z}\,{}^{i}sym:d - {}^{j}_{i}sym:z
\end{bmatrix} = 0
\quad | \;
{}^{i}_{j}sym:\lambda
\quad \forall\; j \in {}^{i}sym:N.
\end{aligned}\]

</span>
</div>
<div class="algo-line algo-indent-2"><span>Determine \({}^{i}_{j}sym:\lambda \;\; \forall\; j \in {}^{i}sym:N\)</span></div>
<div class="algo-line algo-indent-2"><span>Copy \({}^{i}_{j}sym:\lambda,\; {}^{i}_{j}sym:H\!\left({}^{i}sym:r\right),\; {}^{j}_{i}sym:h,\; {}^{i}_{j}sym:z\) to interface storage \(i \leftrightarrow j \;\; \forall\; j \in {}^{i}sym:N\)</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">end for</span></span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-1"><span>Compute outerloop convergence criterion (e.g., [@dewitUnifiedApproach2009a; @tosseramsDistributedOptimization2008])</span></div>
<div class="algo-line algo-indent-1"><span>\(sym:k \leftarrow sym:k + 1\)</span></div>
<div class="algo-line"><span><span class="algo-keyword">until</span> outerloop convergence criterion is met</span></div>
<div class="algo-line"><span><span class="algo-keyword">return</span> \(\left\{{}^{i}sym:d^{(sym:k)}\right\}_{i \in sym:M}\)</span></div>
</div>
</div>


