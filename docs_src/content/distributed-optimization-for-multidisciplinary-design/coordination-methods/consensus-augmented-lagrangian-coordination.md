---
title: Consensus Augmented Lagrangian Coordination (Consensus ALC)
---

# Consensus Augmented Lagrangian Coordination (Consensus ALC)

The preceding solution approaches coordinate subsystems on the [primal problem](../categorization-and-selection-of-suitable-solution-approaches.md#primal-problem-compact-notation) directly. An alternative is to rewrite the problem in *consensus* form [@jeongReviewDecentralized2023; @houskaAugmentedLagrangian2016; @wangNetworkTarget2012a] (also called *two-block* [@engelmannDistributedOptimization2022; @yangSurveyADMM2022; @subramanyamGloballyConvergent2021] or *centralized coordination* [@xuAccuracyEfficiency2015a; @tosseramsDistributedOptimization2008]) by introducing consensus variables ${}^{i}_{j}$sym:y for every ${}^{i}_{j}$sym:c. The coupling constraints become consensus constraints ${}^{i}_{j}$sym:c_c:

\[
{}^{i}_{j}sym:c_c\!\left({}^{i}sym:d,\;{}^{j}sym:d,\;{}^{i}_{j}sym:y\right)
:=
\begin{bmatrix}
{}^{i}_{j}sym:c_c^{i}\!\left({}^{i}sym:d,\;{}^{i}_{j}sym:y\right) \\
{}^{i}_{j}sym:c_c^{j}\!\left({}^{j}sym:d,\;{}^{i}_{j}sym:y\right)
\end{bmatrix}
:=
\begin{bmatrix}
{}^{i}_{j}sym:y -
\begin{bmatrix}
{}^{i}_{j}sym:H\!\left({}^{i}sym:r\right) \\
{}^{i}_{j}sym:z
\end{bmatrix} \\
{}^{i}_{j}sym:y -
\begin{bmatrix}
{}^{i}_{j}sym:h \\
{}^{j}_{i}sym:z
\end{bmatrix}
\end{bmatrix}
= 0,
\]

yielding the *consensus reformulation*:

\[\begin{aligned}
\left\{{}^{i}sym:d^{*}\right\}_{i\in sym:M},\;
\left\{{}^{i}_{j}sym:y^{*}\right\}_{\substack{j\in{}^{i}sym:N \\ i\in sym:M}}
:={} & \argmin_{\substack{{}^{i}sym:d\;\in\;{}^{i}sym:\mathcal{D}\;\forall\; i\in sym:M,\\
{}^{i}_{j}sym:y\;\forall\; j\in{}^{i}sym:N,\; i\in sym:M}}
\quad \sum_{i\in sym:M} {}^{i}sym:v_f\!\left({}^{i}sym:r\right) \\
& \text{s.t.} \quad {}^{i}sym:v_g\!\left({}^{i}sym:r\right) \leq 0 \quad \forall\; i\in sym:M, \\
& \phantom{\text{s.t.}} \quad {}^{i}sym:v_h\!\left({}^{i}sym:r\right) = 0 \quad \forall\; i\in sym:M, \\
& \phantom{\text{s.t.}} \quad {}^{i}_{j}sym:c_c\!\left({}^{i}sym:d,\;{}^{j}sym:d,\;{}^{i}_{j}sym:y\right) = 0 \quad \forall\; j\in{}^{i}sym:N,\; i\in sym:M.
\end{aligned}\]

Treating ${}^{i}_{j}$sym:y as local design variables of an additional *controller* (with no objective or constraints) recovers the [primal problem](../categorization-and-selection-of-suitable-solution-approaches.md#primal-problem-compact-notation) structure. Subsystems couple only to the controller, not to each other, so all previous approaches apply. Whether the original or consensus form is preferable is problem-dependent. Primal-dual methods such as abbr:ALC are commonly used with the consensus form; [abbr:ALADIN](aladin.md) and [abbr:SBDP](sensitivity-based-distributed-programming.md) were applied to the original form by their developers and their consensus variants are omitted here.

Consensus abbr:ALC follows Sections 5 and 6.3 of [@tosseramsDistributedOptimization2008] and Section 5.4 of [@wangNetworkTarget2012a]. Where [abbr:ALC](augmented-lagrangian-coordination.md) relaxes ${}^{i}_{j}$sym:c, Consensus abbr:ALC relaxes ${}^{i}_{j}$sym:c_c instead. The augmented Lagrange function sym:L becomes

\[sym:L\!\left(\left\{{}^{i}sym:d\right\}_{i\in sym:M},\;
\left\{{}^{i}_{j}sym:y,\;{}^{i}_{j}sym:\lambda,\;{}^{i}_{j}sym:s\right\}_{\substack{j\in{}^{i}sym:N \\ i\in sym:M}}\right)
:= \sum_{i\in sym:M}
\left(
{}^{i}sym:v_f\!\left({}^{i}sym:r\right)
+
\sum_{j\in{}^{i}sym:N}
{}^{i}_{j}sym:\lambda^{T}\,{}^{i}_{j}sym:c_c\!\left({}^{i}sym:d,\;{}^{j}sym:d,\;{}^{i}_{j}sym:y\right)
+
\bigl\|{}^{i}_{j}sym:s\circ{}^{i}_{j}sym:c_c\!\left({}^{i}sym:d,\;{}^{j}sym:d,\;{}^{i}_{j}sym:y\right)\bigr\|_2^2
\right).\]

As in [abbr:ALC](augmented-lagrangian-coordination.md), abbr:ALD and abbr:MM are applied. The primal update separates into \({}^{i}sym:d\;\forall\; i\in sym:M\) and \({}^{i}_{j}sym:y\;\forall\; j\in{}^{i}sym:N,\; i\in sym:M\) except for the quadratic penalty; an abbr:FPI alternates between both (the ${}^{i}$sym:d step is fully parallel). Dual and penalty updates use the same subgradient method as [abbr:ALC](augmented-lagrangian-coordination.md), applied to ${}^{i}_{j}$sym:c_c rather than ${}^{i}_{j}$sym:c.

The ${}^{i}_{j}$sym:y optimization is an unconstrained convex abbr:QP (for \({}^{i}_{j}sym:s^{(sym:k)} \neq 0\)) admitting a closed-form solution [@wangNetworkTarget2012a]. Each subsystem $i$ can compute ${}^{i}_{j}$sym:y and ${}^{j}_{i}$sym:y locally, eliminating a dedicated controller at the cost of duplicated work but reduced communication — mirroring the dual and penalty updates. The full procedure is given in [Algorithm 4](#algorithm-4). For convergence analysis, see [@wangNetworkTarget2012a; @tosseramsDistributedOptimization2008].

All symbols are defined in the [Nomenclature](../../includes/index.md).

<div class="algorithm" id="algorithm-4" markdown="0">
<div class="algorithm-caption"><strong>Algorithm 4</strong> Consensus Augmented Lagrangian Coordination (Consensus abbr:ALC)</div>
<div class="algo-body">
<div class="algo-line"><span><span class="algo-keyword">Require:</span> hyperparameters sym:\gamma, sym:\beta</span></div>
<div class="algo-line"><span><span class="algo-keyword">Require:</span> initial \({}^{j}_{i}sym:y^{(0)},\; {}^{i}_{j}sym:y^{(0)} \;\; \forall\; j \in {}^{i}sym:N,\; {}^{i}sym:\lambda^{(0)},\; {}^{i}sym:s^{(0)} \;\; \forall\; i \in sym:M\)</span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line"><span>\(sym:k \leftarrow 0\) <span class="algo-comment">▷ initialize outerloop iterator</span></span></div>
<div class="algo-line"><span><span class="algo-keyword">repeat</span></span></div>
<div class="algo-line algo-indent-1"><span>\(sym:l \leftarrow 0\) <span class="algo-comment">▷ initialize innerloop iterator</span></span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">repeat</span> <span class="algo-comment">▷ decentralized Primal Update approximation</span></span></div>
<div class="algo-line algo-indent-2"><span><span class="algo-keyword">for every</span> \(i \in sym:M\) <span class="algo-keyword">in parallel do</span></span></div>
<div class="algo-math-block">
<span>

\[\begin{aligned}
{}^{i}sym:d^{(sym:k,\,sym:l+1)} \leftarrow{} & \argmin_{{}^{i}sym:d \;\in\; {}^{i}sym:\mathcal{D}} \;\; {}^{i}sym:v_f\!\left({}^{i}sym:r\right) \\
& + \sum_{j \in {}^{i}sym:N} \left(
\left({}^{i}_{j}sym:\lambda^{i}\right)^{(sym:k)\,T}
{}^{i}_{j}sym:c_c^{i}\!\left({}^{i}sym:d,\; {}^{i}_{j}sym:y\right)
+ \left\|\left({}^{i}_{j}sym:s^{i}\right)^{(sym:k)} \circ {}^{i}_{j}sym:c_c^{i}\!\left({}^{i}sym:d,\; {}^{i}_{j}sym:y\right)\right\|_{2}^{2}
\right. \\
& \left. \quad\quad +
\left({}^{j}_{i}sym:\lambda^{i}\right)^{(sym:k)\,T}
{}^{j}_{i}sym:c_c^{i}\!\left({}^{i}sym:d,\; {}^{j}_{i}sym:y\right)
+ \left\|\left({}^{j}_{i}sym:s^{i}\right)^{(sym:k)} \circ {}^{j}_{i}sym:c_c^{i}\!\left({}^{i}sym:d,\; {}^{j}_{i}sym:y\right)\right\|_{2}^{2}
\right) \\
& \text{s.t.} \;\; {}^{i}sym:v_g\!\left({}^{i}sym:r\right) \leq 0, \\
& \phantom{\text{s.t.}} \;\; {}^{i}sym:v_h\!\left({}^{i}sym:r\right) = 0.
\end{aligned}\]

</span>
</div>
<div class="algo-line algo-indent-3"><span>Copy \({}^{i}_{j}sym:H\!\left({}^{i}sym:r\right),\; {}^{j}_{i}sym:h,\; {}^{i}_{j}sym:z,\; {}^{j}_{i}sym:\lambda^{i},\; {}^{i}_{j}sym:\lambda^{i},\; {}^{j}_{i}sym:s^{i},\; {}^{i}_{j}sym:s^{i}\) to interface storage \(i \leftrightarrow j \;\; \forall\; j \in {}^{i}sym:N\)</span></div>
<div class="algo-line algo-indent-2"><span><span class="algo-keyword">end for</span></span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-2"><span><span class="algo-keyword">for every</span> \(i \in sym:M\) <span class="algo-keyword">in parallel do</span></span></div>
<div class="algo-line algo-indent-3"><span>Copy \({}^{j}_{i}sym:H\!\left({}^{j}sym:r\right),\; {}^{i}_{j}sym:h,\; {}^{j}_{i}sym:z,\; {}^{i}_{j}sym:\lambda^{j},\; {}^{j}_{i}sym:\lambda^{j},\; {}^{i}_{j}sym:s^{j},\; {}^{j}_{i}sym:s^{j}\) from interface storage \(i \leftrightarrow j \;\; \forall\; j \in {}^{i}sym:N\)</span></div>
<div class="algo-math-block">
<span>

\[\begin{aligned}
{}^{i}_{j}sym:y^{(sym:k,\,sym:l+1)} \leftarrow \Biggl(
& - \frac{1}{2}\left(\left({}^{i}_{j}sym:\lambda^{i}\right)^{(sym:k)} + \left({}^{i}_{j}sym:\lambda^{j}\right)^{(sym:k)}\right)
+ \left(\left({}^{i}_{j}sym:s^{i}\right)^{(sym:k)} \circ \left({}^{i}_{j}sym:s^{i}\right)^{(sym:k)}\right) \circ
\begin{bmatrix}
{}^{i}_{j}sym:H\!\left({}^{i}sym:r\right) \\
{}^{i}_{j}sym:z
\end{bmatrix} \\
& + \left(\left({}^{i}_{j}sym:s^{j}\right)^{(sym:k)} \circ \left({}^{i}_{j}sym:s^{j}\right)^{(sym:k)}\right) \circ
\begin{bmatrix}
{}^{i}_{j}sym:h \\
{}^{j}_{i}sym:z
\end{bmatrix}
\Biggr) \\
& \oslash \left(\left({}^{i}_{j}sym:s^{i}\right)^{(sym:k)} \circ \left({}^{i}_{j}sym:s^{i}\right)^{(sym:k)} + \left({}^{i}_{j}sym:s^{j}\right)^{(sym:k)} \circ \left({}^{i}_{j}sym:s^{j}\right)^{(sym:k)}\right) \;\;\; \forall\; j \in {}^{i}sym:N
\end{aligned}\]

</span>
</div>
<div class="algo-math-block">
<span>

\[\begin{aligned}
{}^{j}_{i}sym:y^{(sym:k,\,sym:l+1)} \leftarrow \Biggl(
& - \frac{1}{2}\left(\left({}^{j}_{i}sym:\lambda^{j}\right)^{(sym:k)} + \left({}^{j}_{i}sym:\lambda^{i}\right)^{(sym:k)}\right)
+ \left(\left({}^{j}_{i}sym:s^{j}\right)^{(sym:k)} \circ \left({}^{j}_{i}sym:s^{j}\right)^{(sym:k)}\right) \circ
\begin{bmatrix}
{}^{j}_{i}sym:H\!\left({}^{j}sym:r\right) \\
{}^{j}_{i}sym:z
\end{bmatrix} \\
& + \left(\left({}^{j}_{i}sym:s^{i}\right)^{(sym:k)} \circ \left({}^{j}_{i}sym:s^{i}\right)^{(sym:k)}\right) \circ
\begin{bmatrix}
{}^{j}_{i}sym:h \\
{}^{i}_{j}sym:z
\end{bmatrix}
\Biggr) \\
& \oslash \left(\left({}^{j}_{i}sym:s^{j}\right)^{(sym:k)} \circ \left({}^{j}_{i}sym:s^{j}\right)^{(sym:k)} + \left({}^{j}_{i}sym:s^{i}\right)^{(sym:k)} \circ \left({}^{j}_{i}sym:s^{i}\right)^{(sym:k)}\right) \;\;\; \forall\; j \in {}^{i}sym:N
\end{aligned}\]

</span>
</div>
<div class="algo-line algo-indent-2"><span><span class="algo-keyword">end for</span></span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-2"><span>Compute innerloop convergence criterion (e.g., [@dewitUnifiedApproach2009a; @tosseramsDistributedOptimization2008; @guoDistributedAugmented2025])</span></div>
<div class="algo-line algo-indent-2"><span>\(sym:l \leftarrow sym:l + 1\)</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">until</span> innerloop convergence criterion is met</span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-1"><span>\({}^{i}sym:d^{(sym:k+1)},\; {}^{i}_{j}sym:y^{(sym:k+1)} \leftarrow {}^{i}sym:d^{(sym:k,\,sym:l)},\; {}^{i}_{j}sym:y^{(sym:k,\,sym:l)} \;\; \forall\; j \in {}^{i}sym:N,\; i \in sym:M\)</span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">for every</span> \(i \in sym:M\) <span class="algo-keyword">do</span> <span class="algo-comment">▷ decentralized Dual and Penalty Update</span></span></div>
<div class="algo-math-block">
<span>

\[\begin{aligned}
\left({}^{i}_{j}sym:c_c^{i}\right)^{(sym:k+1)} &\leftarrow
{}^{i}_{j}sym:y^{(sym:k+1)} -
\begin{bmatrix}
{}^{i}_{j}sym:H\!\left({}^{i}sym:r\right) \\
{}^{i}_{j}sym:S_{z}\,{}^{i}sym:d^{(sym:k+1)}
\end{bmatrix}, \\[0.5em]
\left({}^{j}_{i}sym:c_c^{i}\right)^{(sym:k+1)} &\leftarrow
{}^{j}_{i}sym:y^{(sym:k+1)} -
\begin{bmatrix}
{}^{j}_{i}sym:S_{h}\,{}^{i}sym:d^{(sym:k+1)} \\
{}^{i}_{j}sym:S_{z}\,{}^{i}sym:d^{(sym:k+1)}
\end{bmatrix}
\end{aligned}\]

</span>
</div>
<div class="algo-math-block">
<span>

\[\begin{aligned}
\left({}^{i}_{j}sym:\lambda^{i}\right)^{(sym:k+1)} &\leftarrow \operatorname{DualUpdate}\!\left(
\left({}^{i}_{j}sym:\lambda^{i}\right)^{(sym:k)},\;
\left({}^{i}_{j}sym:s^{i}\right)^{(sym:k)},\;
\left({}^{i}_{j}sym:c_c^{i}\right)^{(sym:k+1)}
\right) \quad \forall\; j \in {}^{i}sym:N \\
\left({}^{j}_{i}sym:\lambda^{i}\right)^{(sym:k+1)} &\leftarrow \operatorname{DualUpdate}\!\left(
\left({}^{j}_{i}sym:\lambda^{i}\right)^{(sym:k)},\;
\left({}^{j}_{i}sym:s^{i}\right)^{(sym:k)},\;
\left({}^{j}_{i}sym:c_c^{i}\right)^{(sym:k+1)}
\right) \quad \forall\; j \in {}^{i}sym:N \\[0.5em]
\left({}^{i}_{j}sym:s^{i}\right)^{(sym:k+1)} &\leftarrow \operatorname{PenaltyUpdate}\!\left(
sym:\beta,\; sym:\gamma,\;
\left({}^{i}_{j}sym:s^{i}\right)^{(sym:k)},\;
\left({}^{i}_{j}sym:c_c^{i}\right)^{(sym:k+1)},\;
\left({}^{i}_{j}sym:c_c^{i}\right)^{(sym:k)}
\right) \quad \forall\; j \in {}^{i}sym:N \\
\left({}^{j}_{i}sym:s^{i}\right)^{(sym:k+1)} &\leftarrow \operatorname{PenaltyUpdate}\!\left(
sym:\beta,\; sym:\gamma,\;
\left({}^{j}_{i}sym:s^{i}\right)^{(sym:k)},\;
\left({}^{j}_{i}sym:c_c^{i}\right)^{(sym:k+1)},\;
\left({}^{j}_{i}sym:c_c^{i}\right)^{(sym:k)}
\right) \quad \forall\; j \in {}^{i}sym:N
\end{aligned}\]

</span>
</div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">end for</span></span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-1"><span>Compute outerloop convergence criterion (e.g., [@dewitUnifiedApproach2009a; @tosseramsDistributedOptimization2008])</span></div>
<div class="algo-line algo-indent-1"><span>\(sym:k \leftarrow sym:k + 1\)</span></div>
<div class="algo-line"><span><span class="algo-keyword">until</span> outerloop convergence criterion is met</span></div>
<div class="algo-line"><span><span class="algo-keyword">return</span> \(\left\{{}^{i}sym:d^{(sym:k)}\right\}_{i \in sym:M}\)</span></div>
</div>
</div>
