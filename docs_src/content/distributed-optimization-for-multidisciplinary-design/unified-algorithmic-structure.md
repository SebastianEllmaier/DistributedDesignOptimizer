---
title: Unified Algorithmic Structure
---

# Unified Algorithmic Structure

Although the previously introduced methods — [abbr:ALC](coordination-methods/augmented-lagrangian-coordination.md), [abbr:ALADIN](coordination-methods/aladin.md), [abbr:SBDP](coordination-methods/sensitivity-based-distributed-programming.md), and [Consensus abbr:ALC](coordination-methods/consensus-augmented-lagrangian-coordination.md) — differ in methodology, they share a unified structure. Each subsystem solves

\[\begin{aligned}
{}^{i}sym:d^{(sym:k,\,sym:l+1)} \leftarrow{} & \argmin_{{}^{i}sym:d\;\in\;{}^{i}sym:\mathcal{D}} \;\;
{}^{i}sym:v_f\!\left({}^{i}sym:r\right)
+ {}^{i}sym:P\!\left({}^{i}sym:d,\;
\left\{{}^{i}_{j}sym:u,\;{}^{j}_{i}sym:u\right\}_{j\in{}^{i}sym:N},\;
{}^{i}_{C}sym:u,\;{}^{C}_{i}sym:u\right) \\
& \text{s.t.} \;\; {}^{i}sym:v_g\!\left({}^{i}sym:r\right) \leq 0, \\
& \phantom{\text{s.t.}} \;\; {}^{i}sym:v_h\!\left({}^{i}sym:r\right) = 0, \\
& \phantom{\text{s.t.}} \;\; {}^{i}sym:Q^{\leq}\!\left({}^{i}sym:d,\;
\left\{{}^{i}_{j}sym:u,\;{}^{j}_{i}sym:u\right\}_{j\in{}^{i}sym:N},\;
{}^{i}_{C}sym:u,\;{}^{C}_{i}sym:u\right) \leq 0, \\
& \phantom{\text{s.t.}} \;\; {}^{i}sym:Q^{=}\!\left({}^{i}sym:d,\;
\left\{{}^{i}_{j}sym:u,\;{}^{j}_{i}sym:u\right\}_{j\in{}^{i}sym:N},\;
{}^{i}_{C}sym:u,\;{}^{C}_{i}sym:u\right) = 0,
\end{aligned}\]

where ${}^{i}$sym:v_f, ${}^{i}$sym:v_g, and ${}^{i}$sym:v_h are private to subsystem $i$. The coordination approach may introduce an objective term ${}^{i}$sym:P or constraint term ${}^{i}$sym:Q that depend on coupling information sym:u exchanged with neighbors and, optionally, a controller. The controller solves

\[\begin{aligned}
sym:\Box \leftarrow{} & \argmin_{sym:\Box} \;\;
{}^{C}sym:P\!\left(sym:\Box,\;
\left\{{}^{C}_{i}sym:u,\;{}^{i}_{C}sym:u\right\}_{i\in sym:M}\right) \\
& \text{s.t.} \;\; {}^{C}sym:Q^{\leq}\!\left(sym:\Box,\;
\left\{{}^{C}_{i}sym:u,\;{}^{i}_{C}sym:u\right\}_{i\in sym:M}\right) \leq 0, \\
& \phantom{\text{s.t.}} \;\; {}^{C}sym:Q^{=}\!\left(sym:\Box,\;
\left\{{}^{C}_{i}sym:u,\;{}^{i}_{C}sym:u\right\}_{i\in sym:M}\right) = 0.
\end{aligned}\]

The unified algorithm alternates between inner and outer loops—solving subsystem and/or controller problems, updating coupling parameters (e.g. multipliers or penalty parameters), and exchanging sym:u through storage interfaces. Not every method uses all parts:

- the controller problem may be absent,
- the inner loop may collapse to a single iteration or be omitted entirely,
- coupling parameters may be updated in the inner loop, the outer loop, or both.

[Algorithm 5](#algorithm-5) therefore represents a generalized superset of the previously derived methods.

All symbols are defined in the [Nomenclature](../includes/index.md).

<div class="algorithm" id="algorithm-5" markdown="0">
<div class="algorithm-caption"><strong>Algorithm 5</strong> Unified Algorithmic Structure</div>
<div class="algo-body">
<div class="algo-line"><span><span class="algo-keyword">Require:</span> hyperparameters for inner and outerloop convergence criteria</span></div>
<div class="algo-line"><span><span class="algo-keyword">Require:</span> hyperparameters for update of relevant coupling parameters</span></div>
<div class="algo-line"><span><span class="algo-keyword">Require:</span> initial relevant coupling parameters in interface storage</span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line"><span>\(sym:k \leftarrow 0\) <span class="algo-comment">▷ initialize outerloop iterator</span></span></div>
<div class="algo-line"><span><span class="algo-keyword">repeat</span></span></div>
<div class="algo-line algo-indent-1"><span>\(sym:l \leftarrow 0\) <span class="algo-comment">▷ initialize innerloop iterator</span></span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">repeat</span> <span class="algo-comment">▷ following some iteration scheme</span></span></div>
<div class="algo-line algo-indent-2"><span><span class="algo-keyword">for every</span> \(sym:i \in sym:M\) <span class="algo-keyword">do</span></span></div>
<div class="algo-line algo-indent-3"><span>Copy relevant coupling parameters of \({}^{sym:i}_{sym:j}sym:u,\; {}^{sym:j}_{sym:i}sym:u \;\forall\; sym:j \in {}^{sym:i}sym:N\) and \({}^{sym:i}_{C}sym:u,\; {}^{C}_{sym:i}sym:u\) from interface storage</span></div>
<div class="algo-line algo-indent-3"><span>Prepare optimization problem formulation</span></div>
<div class="algo-math-block">
<span>

\[\begin{aligned} {}^{sym:i}sym:d^{(sym:k,\,sym:l+1)} \leftarrow{} & \argmin_{{}^{sym:i}sym:d \;\in\; {}^{sym:i}sym:\mathcal{D}} \;\; {}^{sym:i}sym:v_f\!\left({}^{sym:i}sym:r\right) + {}^{sym:i}sym:P\!\left({}^{sym:i}sym:d,\; \left\{{}^{sym:i}_{sym:j}sym:u,\; {}^{sym:j}_{sym:i}sym:u\right\}_{sym:j \in {}^{sym:i}sym:N},\; {}^{sym:i}_{C}sym:u,\; {}^{C}_{sym:i}sym:u\right) \\ & \text{s.t.} \;\; {}^{sym:i}sym:v_g\!\left({}^{sym:i}sym:r\right) \leq 0, \\ & \phantom{\text{s.t.}} \;\; {}^{sym:i}sym:v_h\!\left({}^{sym:i}sym:r\right) = 0, \\ & \phantom{\text{s.t.}} \;\; {}^{sym:i}sym:Q^{\leq}\!\left({}^{sym:i}sym:d,\; \left\{{}^{sym:i}_{sym:j}sym:u,\; {}^{sym:j}_{sym:i}sym:u\right\}_{sym:j \in {}^{sym:i}sym:N},\; {}^{sym:i}_{C}sym:u,\; {}^{C}_{sym:i}sym:u\right) \leq 0, \\ & \phantom{\text{s.t.}} \;\; {}^{sym:i}sym:Q^{=}\!\left({}^{sym:i}sym:d,\; \left\{{}^{sym:i}_{sym:j}sym:u,\; {}^{sym:j}_{sym:i}sym:u\right\}_{sym:j \in {}^{sym:i}sym:N},\; {}^{sym:i}_{C}sym:u,\; {}^{C}_{sym:i}sym:u\right) = 0. \end{aligned}\]

</span>
</div>
<div class="algo-line algo-indent-3"><span>Post-process the optimization</span></div>
<div class="algo-line algo-indent-3"><span>Copy relevant coupling parameters of \({}^{sym:i}_{sym:j}sym:u,\; {}^{sym:j}_{sym:i}sym:u \;\forall\; sym:j \in {}^{sym:i}sym:N\) and \({}^{sym:i}_{C}sym:u,\; {}^{C}_{sym:i}sym:u\) to interface storage</span></div>
<div class="algo-line algo-indent-2"><span><span class="algo-keyword">end for</span></span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-2"><span><span class="algo-keyword">for</span> <strong>Controller</strong> <span class="algo-keyword">do</span></span></div>
<div class="algo-line algo-indent-3"><span>Copy relevant coupling parameters of \({}^{C}_{sym:i}sym:u,\; {}^{sym:i}_{C}sym:u \;\forall\; sym:i \in sym:M\) from interface storage</span></div>
<div class="algo-line algo-indent-3"><span>Prepare optimization problem formulation</span></div>
<div class="algo-math-block">
<span>

\[\begin{aligned} sym:\Box \leftarrow{} & \argmin_{sym:\Box} \;\; {}^{C}sym:P\!\left(sym:\Box,\; \left\{{}^{C}_{sym:i}sym:u,\; {}^{sym:i}_{C}sym:u\right\}_{sym:i \in sym:M}\right) \\ & \text{s.t.} \;\; {}^{C}sym:Q^{\leq}\!\left(sym:\Box,\; \left\{{}^{C}_{sym:i}sym:u,\; {}^{sym:i}_{C}sym:u\right\}_{sym:i \in sym:M}\right) \leq 0, \\ & \phantom{\text{s.t.}} \;\; {}^{C}sym:Q^{=}\!\left(sym:\Box,\; \left\{{}^{C}_{sym:i}sym:u,\; {}^{sym:i}_{C}sym:u\right\}_{sym:i \in sym:M}\right) = 0. \end{aligned}\]

</span>
</div>
<div class="algo-line algo-indent-3"><span>Post-process the optimization</span></div>
<div class="algo-line algo-indent-3"><span>Copy relevant coupling parameters of \({}^{C}_{sym:i}sym:u,\; {}^{sym:i}_{C}sym:u \;\forall\; sym:i \in sym:M\) to interface storage</span></div>
<div class="algo-line algo-indent-2"><span><span class="algo-keyword">end for</span></span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-2"><span><span class="algo-keyword">for every</span> \(sym:i \in sym:M\) <span class="algo-keyword">and Controller in parallel do</span></span></div>
<div class="algo-line algo-indent-3"><span>Copy relevant coupling parameters of \({}^{sym:i}_{sym:j}sym:u,\; {}^{sym:j}_{sym:i}sym:u \;\forall\; sym:j \in {}^{sym:i}sym:N\) and \({}^{sym:i}_{C}sym:u,\; {}^{C}_{sym:i}sym:u\) from interface storage</span></div>
<div class="algo-line algo-indent-3"><span>Update relevant coupling parameters \({}^{sym:i}_{sym:j}sym:u,\; {}^{sym:j}_{sym:i}sym:u \;\forall\; sym:j \in {}^{sym:i}sym:N\) and \({}^{sym:i}_{C}sym:u,\; {}^{C}_{sym:i}sym:u\)</span></div>
<div class="algo-line algo-indent-3"><span>Copy relevant coupling parameters of \({}^{sym:i}_{sym:j}sym:u,\; {}^{sym:j}_{sym:i}sym:u \;\forall\; sym:j \in {}^{sym:i}sym:N\) and \({}^{sym:i}_{C}sym:u,\; {}^{C}_{sym:i}sym:u\) to interface storage</span></div>
<div class="algo-line algo-indent-2"><span><span class="algo-keyword">end for</span></span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-2"><span>Compute innerloop convergence criterion</span></div>
<div class="algo-line algo-indent-2"><span>\(sym:l \leftarrow sym:l + 1\)</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">until</span> innerloop convergence criterion is met</span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-1"><span>\({}^{sym:i}sym:d^{(sym:k+1)} \leftarrow {}^{sym:i}sym:d^{(sym:k,\,sym:l)} \;\forall\; sym:i \in sym:M\)</span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">for every</span> \(sym:i \in sym:M\) <span class="algo-keyword">and Controller in parallel do</span></span></div>
<div class="algo-line algo-indent-2"><span>Copy relevant coupling parameters of \({}^{sym:i}_{sym:j}sym:u,\; {}^{sym:j}_{sym:i}sym:u \;\forall\; sym:j \in {}^{sym:i}sym:N\) and \({}^{sym:i}_{C}sym:u,\; {}^{C}_{sym:i}sym:u\) from interface storage</span></div>
<div class="algo-line algo-indent-2"><span>Prepare update of relevant coupling parameters \({}^{sym:i}_{sym:j}sym:u,\; {}^{sym:j}_{sym:i}sym:u \;\forall\; sym:j \in {}^{sym:i}sym:N\) and \({}^{sym:i}_{C}sym:u,\; {}^{C}_{sym:i}sym:u\)</span></div>
<div class="algo-line algo-indent-2"><span>Copy relevant coupling parameters of \({}^{sym:i}_{sym:j}sym:u,\; {}^{sym:j}_{sym:i}sym:u \;\forall\; sym:j \in {}^{sym:i}sym:N\) and \({}^{sym:i}_{C}sym:u,\; {}^{C}_{sym:i}sym:u\) to interface storage</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">end for</span></span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">for every</span> \(sym:i \in sym:M\) <span class="algo-keyword">and Controller in parallel do</span></span></div>
<div class="algo-line algo-indent-2"><span>Copy relevant coupling parameters of \({}^{sym:i}_{sym:j}sym:u,\; {}^{sym:j}_{sym:i}sym:u \;\forall\; sym:j \in {}^{sym:i}sym:N\) and \({}^{sym:i}_{C}sym:u,\; {}^{C}_{sym:i}sym:u\) from interface storage</span></div>
<div class="algo-line algo-indent-2"><span>Update relevant coupling parameters \({}^{sym:i}_{sym:j}sym:u,\; {}^{sym:j}_{sym:i}sym:u \;\forall\; sym:j \in {}^{sym:i}sym:N\) and \({}^{sym:i}_{C}sym:u,\; {}^{C}_{sym:i}sym:u\)</span></div>
<div class="algo-line algo-indent-2"><span>Copy relevant coupling parameters of \({}^{sym:i}_{sym:j}sym:u,\; {}^{sym:j}_{sym:i}sym:u \;\forall\; sym:j \in {}^{sym:i}sym:N\) and \({}^{sym:i}_{C}sym:u,\; {}^{C}_{sym:i}sym:u\) to interface storage</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">end for</span></span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-1"><span>Compute outerloop convergence criterion</span></div>
<div class="algo-line algo-indent-1"><span>\(sym:k \leftarrow sym:k + 1\)</span></div>
<div class="algo-line"><span><span class="algo-keyword">until</span> outerloop convergence criterion is met</span></div>
<div class="algo-line"><span><span class="algo-keyword">return</span> \(\left\{{}^{sym:i}sym:d^{(sym:k)}\right\}_{sym:i \in sym:M}\)</span></div>
</div>
</div>