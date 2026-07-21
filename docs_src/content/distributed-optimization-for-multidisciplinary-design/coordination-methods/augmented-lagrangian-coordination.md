---
title: Augmented Lagrangian Coordination (ALC)
---


# Augmented Lagrangian Coordination (ALC)

This derivation follows Sections 6.4 and 6.6 of [@tosseramsDistributedOptimization2008], Section 5 of [@dewitUnifiedApproach2009a], and Section 2 of [@stephanopoulosUseHestenes1975]. Augmented Lagrangian Duality (abbr:ALD) relaxes the coupling constraints \({}^{i}_{j}sym:c\!\left({}^{i}sym:d,\;{}^{j}sym:d\right)\) of the [primal problem](../categorization-and-selection-of-suitable-solution-approaches.md#primal-problem-compact-notation), yielding the *dual problem*

\[\max_{{}^{i}_{j}sym:\lambda\;\forall\; j\in{}^{i}sym:N,\; i\in sym:M}\left(
\begin{aligned}
& \min_{{}^{i}sym:d\;\in\;{}^{i}sym:\mathcal{D}\;\forall\; i\in sym:M} \quad sym:L\!\left(\left\{{}^{i}sym:d\right\}_{i\in sym:M},\;\left\{{}^{i}_{j}sym:\lambda,\;{}^{i}_{j}sym:s\right\}_{\substack{j\in{}^{i}sym:N \\ i\in sym:M}}\right) \\
& \text{s.t.} \quad {}^{i}sym:v_g\!\left({}^{i}sym:r\right) \leq 0 \quad \forall\; i\in sym:M, \\
& \phantom{\text{s.t.}} \quad {}^{i}sym:v_h\!\left({}^{i}sym:r\right) = 0 \quad \forall\; i\in sym:M
\end{aligned}
\right),\]

\[sym:L\!\left(\left\{{}^{i}sym:d\right\}_{i\in sym:M},\;\left\{{}^{i}_{j}sym:\lambda,\;{}^{i}_{j}sym:s\right\}_{\substack{j\in{}^{i}sym:N \\ i\in sym:M}}\right)
:= \sum_{i\in sym:M}
\left(
{}^{i}sym:v_f\!\left({}^{i}sym:r\right)
+
\sum_{j\in{}^{i}sym:N}
{}^{i}_{j}sym:\lambda^{T}\,{}^{i}_{j}sym:c\!\left({}^{i}sym:d,\;{}^{j}sym:d\right)
+
\bigl\|{}^{i}_{j}sym:s\circ{}^{i}_{j}sym:c\!\left({}^{i}sym:d,\;{}^{j}sym:d\right)\bigr\|_2^2
\right).\]

Relaxing coupling constraints simplifies optimizing primal variables ${}^{i}$sym:d but requires finding optimal dual variables ${}^{i}_{j}$sym:\lambda (*Lagrange multipliers*). A sufficiently large penalty parameter sym:s convexifies the augmented Lagrange function sym:L, improving numerical stability. The Method of Multipliers (abbr:MM) solves the dual problem by alternating between primal and dual variable updates in an *outer loop*.

The multiplier sym:\lambda update follows a subgradient scheme (where \(\circ\) denotes element-wise multiplication):

\[sym:\lambda^{(sym:k+1)} \leftarrow sym:\lambda^{(sym:k)} + 2 \cdot sym:s^{(sym:k)} \circ sym:s^{(sym:k)} \circ sym:c^{(sym:k+1)}\]

The penalty parameters are adapted based on inconsistency improvement:

\[sym:s^{(sym:k+1)} \leftarrow
\begin{cases}
sym:\beta \cdot sym:s^{(sym:k)} & \text{if } \left|sym:c^{(sym:k+1)}\right| > sym:\gamma \cdot \left|sym:c^{(sym:k)}\right| \\
sym:s^{(sym:k)} & \text{otherwise}
\end{cases}\]

The penalty parameter increases by factor sym:\beta only when inconsistency reduction is insufficient (less than factor sym:\gamma), avoiding unnecessarily large values while ensuring convergence.

These updates require centralized computation, making them unsuitable for distributed optimization. However, the primal update is separable into \(\left|sym:M\right|\) independent optimization problems — one per design variable ${}^{i}$sym:d — except for the quadratic penalty term \(\left\|{}^{i}_{j}sym:s\circ{}^{i}_{j}sym:c\right\|_{2}^{2}\) in sym:L.

abbr:ALC approximately solves the [primal problem](../categorization-and-selection-of-suitable-solution-approaches.md#primal-problem-compact-notation) via abbr:FPI schemes such as Gauss–Seidel (sequential, using the latest data) or Jacobi (parallel). This distributed primal update forms an *inner loop* with termination criteria as defined in [@dewitUnifiedApproach2009a; @tosseramsDistributedOptimization2008; @guoDistributedAugmented2025].

The resulting abbr:ALC algorithm is shown in [Algorithm 1](#algorithm-1) below. The dual update may also be distributed. The variant of [@dewitUnifiedApproach2009a; @tosseramsDistributedOptimization2008] uses the subgradient method above. In this implementation, each subsystem $i$ maintains multipliers and weights for both ${}^{i}_{j}$sym:c and ${}^{j}_{i}$sym:c. For convergence analysis, see [@dewitUnifiedApproach2009a; @tosseramsDistributedOptimization2008].

All symbols are defined in the [Nomenclature](../../includes/index.md).

<div class="algorithm" id="algorithm-1" markdown="0">
<div class="algorithm-caption"><strong>Algorithm 1</strong> Augmented Lagrangian Coordination (abbr:ALC)</div>
<div class="algo-body">
<div class="algo-line"><span><span class="algo-keyword">Require:</span> hyperparameters sym:\gamma, sym:\beta</span></div>
<div class="algo-line"><span><span class="algo-keyword">Require:</span> initial \({}^{j}_{i}sym:H\!\left({}^{j}sym:r\right),\; {}^{i}_{j}sym:h,\; {}^{j}_{i}sym:z\) in interface storage \(i \leftrightarrow j \;\; \forall\; j \in {}^{i}sym:N,\; i \in sym:M\)</span></div>
<div class="algo-line"><span><span class="algo-keyword">Require:</span> initial \({}^{i}_{j}sym:\lambda^{(0)},\; {}^{i}_{j}sym:s^{(0)} \;\; \forall\; j \in {}^{i}sym:N,\; i \in sym:M\)</span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line"><span>\(sym:k \leftarrow 0\) <span class="algo-comment">▷ initialize outerloop iterator</span></span></div>
<div class="algo-line"><span><span class="algo-keyword">repeat</span></span></div>
<div class="algo-line algo-indent-1"><span>\(sym:l \leftarrow 0\) <span class="algo-comment">▷ initialize innerloop iterator</span></span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">repeat</span> <span class="algo-comment">▷ decentralized Primal Update approximation</span></span></div>
<div class="algo-line algo-indent-2"><span><span class="algo-keyword">for every</span> \(i \in sym:M\) <span class="algo-keyword">in sequence or parallel do</span></span></div>
<div class="algo-line algo-indent-3"><span>Copy \({}^{j}_{i}sym:H\!\left({}^{j}sym:r\right),\; {}^{i}_{j}sym:h,\; {}^{j}_{i}sym:z\) from interface storage \(i \leftrightarrow j \;\; \forall\; j \in {}^{i}sym:N\)</span></div>
<div class="algo-math-block">
<span>

\[\begin{aligned}
{}^{i}sym:d^{(sym:k,\,sym:l+1)} \leftarrow{} & \argmin_{{}^{i}sym:d \;\in\; {}^{i}sym:\mathcal{D}} \;\; {}^{i}sym:v_f\!\left({}^{i}sym:r\right) \\
& + \sum_{j \in {}^{i}sym:N} \left(
\left({}^{i}_{j}sym:\lambda^{(sym:k)}\right)^{T}
\begin{bmatrix}
{}^{i}_{j}sym:H\!\left({}^{i}sym:r\right) - {}^{i}_{j}sym:h \\
{}^{i}_{j}sym:S_{z}\,{}^{i}sym:d - {}^{j}_{i}sym:z
\end{bmatrix}
+ \left\|{}^{i}_{j}sym:s^{(sym:k)} \circ
\begin{bmatrix}
{}^{i}_{j}sym:H\!\left({}^{i}sym:r\right) - {}^{i}_{j}sym:h \\
{}^{i}_{j}sym:S_{z}\,{}^{i}sym:d - {}^{j}_{i}sym:z
\end{bmatrix}
\right\|_{2}^{2} \right. \\
& \left. \quad\quad + \left({}^{j}_{i}sym:\lambda^{(sym:k)}\right)^{T}
\begin{bmatrix}
{}^{j}_{i}sym:H\!\left({}^{j}sym:r\right) - {}^{j}_{i}sym:S_{h}\,{}^{i}sym:d \\
{}^{j}_{i}sym:z - {}^{i}_{j}sym:S_{z}\,{}^{i}sym:d
\end{bmatrix}
+ \left\|{}^{j}_{i}sym:s^{(sym:k)} \circ
\begin{bmatrix}
{}^{j}_{i}sym:H\!\left({}^{j}sym:r\right) - {}^{j}_{i}sym:S_{h}\,{}^{i}sym:d \\
{}^{j}_{i}sym:z - {}^{i}_{j}sym:S_{z}\,{}^{i}sym:d
\end{bmatrix}
\right\|_{2}^{2}
\right) \\
& \text{s.t.} \;\; {}^{i}sym:v_g\!\left({}^{i}sym:r\right) \leq 0, \\
& \phantom{\text{s.t.}} \;\; {}^{i}sym:v_h\!\left({}^{i}sym:r\right) = 0.
\end{aligned}\]

</span>
</div>
<div class="algo-line algo-indent-3"><span>Copy \({}^{i}_{j}sym:H\!\left({}^{i}sym:r\right),\; {}^{j}_{i}sym:h,\; {}^{i}_{j}sym:z\) to interface storage \(i \leftrightarrow j \;\; \forall\; j \in {}^{i}sym:N\)</span></div>
<div class="algo-line algo-indent-2"><span><span class="algo-keyword">end for</span></span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-2"><span>Compute innerloop convergence criterion (e.g., [@dewitUnifiedApproach2009a; @tosseramsDistributedOptimization2008; @guoDistributedAugmented2025])</span></div>
<div class="algo-line algo-indent-2"><span>\(sym:l \leftarrow sym:l + 1\)</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">until</span> innerloop convergence criterion is met</span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-1"><span>\({}^{i}sym:d^{(sym:k+1)} \leftarrow {}^{i}sym:d^{(sym:k,\,sym:l)} \;\forall\; i \in sym:M\)</span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">for every</span> \(i \in sym:M\) <span class="algo-keyword">in parallel do</span> <span class="algo-comment">▷ decentralized Dual and Penalty Update</span></span></div>
<div class="algo-line algo-indent-2"><span>Copy \({}^{j}_{i}sym:H\!\left({}^{j}sym:r\right),\; {}^{i}_{j}sym:h,\; {}^{j}_{i}sym:z\) from interface storage \(i \leftrightarrow j \;\; \forall\; j \in {}^{i}sym:N\)</span></div>
<div class="algo-math-block">
<span>

\[\begin{aligned}
{}^{i}_{j}sym:c^{(sym:k+1)} &\leftarrow
\begin{bmatrix}
{}^{i}_{j}sym:H\!\left({}^{i}sym:r\right) - {}^{i}_{j}sym:h \\
{}^{i}_{j}sym:S_{z}\,{}^{i}sym:d^{(sym:k+1)} - {}^{j}_{i}sym:z
\end{bmatrix}, \\[0.5em]
{}^{j}_{i}sym:c^{(sym:k+1)} &\leftarrow
\begin{bmatrix}
{}^{j}_{i}sym:H\!\left({}^{j}sym:r\right) - {}^{j}_{i}sym:S_{h}\,{}^{i}sym:d^{(sym:k+1)} \\
{}^{j}_{i}sym:z - {}^{i}_{j}sym:S_{z}\,{}^{i}sym:d^{(sym:k+1)}
\end{bmatrix}
\end{aligned}\]

</span>
</div>
<div class="algo-math-block">
<span>

\[\begin{aligned}
{}^{i}_{j}sym:\lambda^{(sym:k+1)} &\leftarrow \operatorname{DualUpdate}\!\left(
{}^{i}_{j}sym:\lambda^{(sym:k)},\;
{}^{i}_{j}sym:s^{(sym:k)},\;
{}^{i}_{j}sym:c^{(sym:k+1)}
\right) \quad \forall\; j \in {}^{i}sym:N \\
{}^{j}_{i}sym:\lambda^{(sym:k+1)} &\leftarrow \operatorname{DualUpdate}\!\left(
{}^{j}_{i}sym:\lambda^{(sym:k)},\;
{}^{j}_{i}sym:s^{(sym:k)},\;
{}^{j}_{i}sym:c^{(sym:k+1)}
\right) \quad \forall\; j \in {}^{i}sym:N \\[0.5em]
{}^{i}_{j}sym:s^{(sym:k+1)} &\leftarrow \operatorname{PenaltyUpdate}\!\left(
sym:\beta,\; sym:\gamma,\;
{}^{i}_{j}sym:s^{(sym:k)},\;
{}^{i}_{j}sym:c^{(sym:k+1)},\;
{}^{i}_{j}sym:c^{(sym:k)}
\right) \quad \forall\; j \in {}^{i}sym:N \\
{}^{j}_{i}sym:s^{(sym:k+1)} &\leftarrow \operatorname{PenaltyUpdate}\!\left(
sym:\beta,\; sym:\gamma,\;
{}^{j}_{i}sym:s^{(sym:k)},\;
{}^{j}_{i}sym:c^{(sym:k+1)},\;
{}^{j}_{i}sym:c^{(sym:k)}
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
