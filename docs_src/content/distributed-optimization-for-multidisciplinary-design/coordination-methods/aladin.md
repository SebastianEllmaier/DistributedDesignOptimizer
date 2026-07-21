---
title: Augmented Lagrangian Alternating Direction Inexact Newton (ALADIN)
---

# Augmented Lagrangian Alternating Direction Inexact Newton (ALADIN)

Where [abbr:ALC](augmented-lagrangian-coordination.md) solves the [primal problem](../categorization-and-selection-of-suitable-solution-approaches.md#primal-problem-compact-notation) via abbr:FPI, Augmented Lagrangian based Alternating Direction Inexact Newton (abbr:ALADIN) computes search directions \(\Delta{}^{i}sym:d\) by Newton/abbr:SQP iterations on the abbr:KKT system [@houskaAugmentedLagrangian2016; @engelmannDistributedOptimization2022; @jiangDistributedOptimization2020]. While [@houskaAugmentedLagrangian2016] treats affine coupling constraints sym:c, this section extends the principle to nonlinear pairwise couplings, yielding a novel distributed Newton/abbr:SQP method.

The abbr:SQP objective is the second-order Taylor approximation of the total Lagrangian sym:L, with abbr:KKT feasibility as linearized constraints. Unlike the active-set Newton interpretation of [@houskaAugmentedLagrangian2016; @engelmannDistributedOptimization2022; @jiangDistributedOptimization2020], the abbr:QP does not prescribe an active set for inequality constraints:

\[\begin{aligned}
\left\{\Delta{}^{i}sym:d\right\}_{i\in sym:M}
\leftarrow
& \argmin_{\Delta{}^{i}sym:d\;\forall\; i\in sym:M}
\quad
\sum_{i\in sym:M}
\Biggl(
{}^{i}sym:v_f
+
\nabla_{{}^{i}sym:d}^{T}{}^{i}sym:v_f\,\Delta{}^{i}sym:d
+
\frac{1}{2}
\Delta{}^{i}sym:d^{T}
\nabla^{2}_{{}^{i}sym:d\,{}^{i}sym:d}{}^{i}sym:v_f
\,\Delta{}^{i}sym:d
\\
& \phantom{\argmin_{\Delta{}^{i}sym:d\;\forall\; i\in sym:M}} \quad\quad\quad\;\; +
{}^{i}sym:\kappa_g^{T}\,{}^{i}sym:v_g
+
{}^{i}sym:\kappa_g^{T}
\nabla_{{}^{i}sym:d}{}^{i}sym:v_g\,\Delta{}^{i}sym:d
+
\frac{1}{2}
\Delta{}^{i}sym:d^{T}
\left(
\sum_{q=1}^{{}^{i}n_{v_g}}
({}^{i}sym:\kappa_g)_{q}
\nabla^{2}_{{}^{i}sym:d\,{}^{i}sym:d}
\bigl(({}^{i}sym:v_g)_{q}\bigr)
\right)
\Delta{}^{i}sym:d
\\
& \phantom{\argmin_{\Delta{}^{i}sym:d\;\forall\; i\in sym:M}} \quad\quad\quad\;\; +
{}^{i}sym:\kappa_h^{T}\,{}^{i}sym:v_h
+
{}^{i}sym:\kappa_h^{T}
\nabla_{{}^{i}sym:d}{}^{i}sym:v_h\,\Delta{}^{i}sym:d
+
\frac{1}{2}
\Delta{}^{i}sym:d^{T}
\left(
\sum_{q=1}^{{}^{i}n_{v_h}}
({}^{i}sym:\kappa_h)_{q}
\nabla^{2}_{{}^{i}sym:d\,{}^{i}sym:d}
\bigl(({}^{i}sym:v_h)_{q}\bigr)
\right)
\Delta{}^{i}sym:d
\\
& \phantom{\argmin_{\Delta{}^{i}sym:d\;\forall\; i\in sym:M}} \quad\quad\quad\;\; +
{}^{i}sym:\kappa_d^{T}\,{}^{i}sym:v_D
+
{}^{i}sym:\kappa_d^{T}\nabla_{{}^{i}sym:d}{}^{i}sym:v_D\,\Delta{}^{i}sym:d
\Biggr)
\\
& \phantom{\argmin_{\Delta{}^{i}sym:d\;\forall\; i\in sym:M}} \quad +
\sum_{i\in sym:M}\sum_{j\in{}^{i}sym:N}
\Biggl(
{}^{i}_{j}sym:\lambda^{T}
\begin{bmatrix}
{}^{i}_{j}sym:H\!\left({}^{i}sym:r\right) - {}^{i}_{j}sym:h \\
{}^{i}_{j}sym:z - {}^{j}_{i}sym:z
\end{bmatrix}
+
{}^{i}_{j}sym:\lambda^{T}
\begin{bmatrix}
\nabla_{{}^{i}sym:d}{}^{i}_{j}sym:H\,\Delta{}^{i}sym:d
- {}^{i}_{j}sym:S_{h}\,\Delta{}^{j}sym:d \\
{}^{i}_{j}sym:S_{z}\,\Delta{}^{i}sym:d
- {}^{j}_{i}sym:S_{z}\,\Delta{}^{j}sym:d
\end{bmatrix}
\\
& \phantom{\argmin_{\Delta{}^{i}sym:d\;\forall\; i\in sym:M}} \quad\quad\quad\quad\quad\quad\; +
\frac{1}{2}
\Delta{}^{i}sym:d^{T}
\left(
\sum_{q=1}^{{}^{i}_{j}n_h}
({}^{i}_{j}sym:\lambda_{h})_{q}
\nabla^{2}_{{}^{i}sym:d\,{}^{i}sym:d}
\bigl({}^{i}_{j}sym:H\bigr)_{q}
\right)
\Delta{}^{i}sym:d
\Biggr)
\\
& \phantom{\argmin_{\Delta{}^{i}sym:d\;\forall\; i\in sym:M}} \quad +
\sum_{i\in sym:M}\sum_{j\in{}^{i}sym:N}
\Biggl(
\left\|
{}^{i}_{j}sym:s\circ
\begin{bmatrix}
{}^{i}_{j}sym:H\!\left({}^{i}sym:r\right) - {}^{i}_{j}sym:h \\
{}^{i}_{j}sym:z - {}^{j}_{i}sym:z
\end{bmatrix}
\right\|_{2}^{2}
+
2\left({}^{i}_{j}sym:s^{2}\circ
\begin{bmatrix}
{}^{i}_{j}sym:H\!\left({}^{i}sym:r\right) - {}^{i}_{j}sym:h \\
{}^{i}_{j}sym:z - {}^{j}_{i}sym:z
\end{bmatrix}
\right)^{T}
\begin{bmatrix}
\nabla_{{}^{i}sym:d}{}^{i}_{j}sym:H\,\Delta{}^{i}sym:d
- {}^{i}_{j}sym:S_{h}\,\Delta{}^{j}sym:d \\
{}^{i}_{j}sym:S_{z}\,\Delta{}^{i}sym:d
- {}^{j}_{i}sym:S_{z}\,\Delta{}^{j}sym:d
\end{bmatrix}
\\
& \phantom{\argmin_{\Delta{}^{i}sym:d\;\forall\; i\in sym:M}} \quad\quad\quad\quad\quad\quad\; +
\begin{bmatrix}
\nabla_{{}^{i}sym:d}{}^{i}_{j}sym:H\,\Delta{}^{i}sym:d
- {}^{i}_{j}sym:S_{h}\,\Delta{}^{j}sym:d \\
{}^{i}_{j}sym:S_{z}\,\Delta{}^{i}sym:d
- {}^{j}_{i}sym:S_{z}\,\Delta{}^{j}sym:d
\end{bmatrix}^{T}
\operatorname{diag}\!\left({}^{i}_{j}sym:s\right)^{2}
\begin{bmatrix}
\nabla_{{}^{i}sym:d}{}^{i}_{j}sym:H\,\Delta{}^{i}sym:d
- {}^{i}_{j}sym:S_{h}\,\Delta{}^{j}sym:d \\
{}^{i}_{j}sym:S_{z}\,\Delta{}^{i}sym:d
- {}^{j}_{i}sym:S_{z}\,\Delta{}^{j}sym:d
\end{bmatrix}
\\
& \phantom{\argmin_{\Delta{}^{i}sym:d\;\forall\; i\in sym:M}} \quad\quad\quad\quad\quad\quad\; +
\sum_{q=1}^{{}^{i}_{j}n_h}
\left({}^{i}_{j}sym:s_{h}^{2}\circ
\left({}^{i}_{j}sym:H\!\left({}^{i}sym:r\right) - {}^{i}_{j}sym:h\right)
\right)_{q}
\Delta{}^{i}sym:d^{T}
\nabla^{2}_{{}^{i}sym:d\,{}^{i}sym:d}
\bigl(({}^{i}_{j}sym:H)_{q}\bigr)
\Delta{}^{i}sym:d
\Biggr)
\\
&\text{s.t.} \quad
{}^{i}sym:v_g
+
\nabla_{{}^{i}sym:d}{}^{i}sym:v_g\,
\Delta{}^{i}sym:d
\leq
0
\quad \forall\; i\in sym:M,
\\
&\phantom{\text{s.t.}} \quad
{}^{i}sym:v_h
+
\nabla_{{}^{i}sym:d}{}^{i}sym:v_h\,
\Delta{}^{i}sym:d
=
0
\quad \forall\; i\in sym:M,
\\
&\phantom{\text{s.t.}} \quad
{}^{i}sym:v_D
+
\nabla_{{}^{i}sym:d}{}^{i}sym:v_D\,
\Delta{}^{i}sym:d
\leq
0
\quad \forall\; i\in sym:M.
\end{aligned}\]

The bound constraint \({}^{i}sym:d \in {}^{i}sym:\mathcal{D}\) is expressed as an inequality whose Hessian vanishes. All quantities are evaluated at \({}^{i}sym:d^{(sym:k,\,sym:l)}\), and \({}^{i}sym:\kappa_g,\; {}^{i}sym:\kappa_h,\; {}^{i}sym:\kappa_d\) and \({}^{i}_{j}sym:\lambda\) are Lagrange multipliers for \({}^{i}sym:v_g,\; {}^{i}sym:v_h,\; {}^{i}sym:v_D\), and ${}^{i}_{j}$sym:c, respectively.

Since the abbr:QP couples \(\Delta{}^{i}sym:d\) and \(\Delta{}^{j}sym:d\) pairwise, a *controller* entity assembles and solves it. abbr:ALADIN separates locally feasible subsystem iterates from the coupled abbr:SQP correction. Subsystems provide gradients, Hessians, multipliers, and active sets to the controller.

The controller prediction is

\[{}^{i}\hat{sym:d}^{(sym:k,\,sym:l+1)}
:=
{}^{i}sym:d^{(sym:k,\,sym:l)}
+
\Delta{}^{i}sym:d
\quad \forall\; i\in sym:M.\]

A proximalized auxiliary problem is introduced around this prediction:

\[\begin{aligned}
\left\{{}^{i}sym:d^{(sym:k,\,sym:l+1)}\right\}_{i\in sym:M}
\leftarrow
& \argmin_{{}^{i}sym:d\;\forall\; i\in sym:M}
\quad
\sum_{i\in sym:M}
\left(
{}^{i}sym:v_f\!\left({}^{i}sym:r\right)
+
\sum_{j\in{}^{i}sym:N}
{}^{i}_{j}sym:\lambda^{T}
\,{}^{i}_{j}sym:c\!\left({}^{i}sym:d,\;{}^{j}sym:d\right)
+
\frac{sym:\nu}{2}
\left\|
{}^{i}sym:d
-
{}^{i}\hat{sym:d}^{(sym:k,\,sym:l+1)}
\right\|_{{}^{i}sym:\Sigma}^{2}
\right)
\\
&\text{s.t.} \quad
{}^{i}sym:v_g\!\left({}^{i}sym:r\right)\leq 0
\quad |\; {}^{i}sym:\kappa_g
\quad \forall\; i\in sym:M,
\\
&\phantom{\text{s.t.}} \quad
{}^{i}sym:v_h\!\left({}^{i}sym:r\right)=0
\quad |\; {}^{i}sym:\kappa_h
\quad \forall\; i\in sym:M,
\\
&\phantom{\text{s.t.}} \quad
{}^{i}sym:v_D\!\left({}^{i}sym:d\right)\leq 0
\quad |\; {}^{i}sym:\kappa_d
\quad \forall\; i\in sym:M.
\end{aligned}\]

The proximal term regularizes around the controller prediction. Since this is separable, each subsystem $i$ solves:

\[\begin{aligned}
{}^{i}sym:d^{(sym:k,\,sym:l+1)}
\leftarrow
& \argmin_{{}^{i}sym:d} \quad
{}^{i}sym:v_f\!\left({}^{i}sym:r\right)
+
\sum_{j\in{}^{i}sym:N}
\Biggl(
{}^{i}_{j}sym:\lambda^{T}
\begin{bmatrix}
{}^{i}_{j}sym:H\!\left({}^{i}sym:r\right) \\
{}^{i}_{j}sym:S_{z}\,{}^{i}sym:d
\end{bmatrix}
+
{}^{j}_{i}sym:\lambda^{T}
\begin{bmatrix}
- {}^{j}_{i}sym:S_{h}\,{}^{i}sym:d \\
- {}^{i}_{j}sym:S_{z}\,{}^{i}sym:d
\end{bmatrix}
\Biggr)
\\
& \quad\quad\quad\quad\; +
\frac{sym:\nu}{2}
\left\|
{}^{i}sym:d
-
{}^{i}\hat{sym:d}^{(sym:k,\,sym:l+1)}
\right\|_{{}^{i}sym:\Sigma}^{2}
\\
& \text{s.t.} \quad
{}^{i}sym:v_g\!\left({}^{i}sym:r\right)\leq 0 \quad
|\; {}^{i}sym:\kappa_g,
\\
& \phantom{\text{s.t.}} \quad
{}^{i}sym:v_h\!\left({}^{i}sym:r\right)=0 \quad
|\; {}^{i}sym:\kappa_h,
\\
& \phantom{\text{s.t.}} \quad
{}^{i}sym:v_D\!\left({}^{i}sym:d\right)\leq 0 \quad
|\; {}^{i}sym:\kappa_d.
\end{aligned}\]

The iterates \({}^{i}sym:d^{(sym:k,\,sym:l+1)}\) satisfy local feasibility exactly, so constraint linearizations in the abbr:QP objective vanish and constant terms are omitted. The local Hessian ${}^{i}B$ collects:

\[{}^{i}B
:=
\nabla^{2}_{{}^{i}sym:d\,{}^{i}sym:d}{}^{i}sym:v_f
+
\sum_{q=1}^{{}^{i}n_{v_g}}
({}^{i}sym:\kappa_g)_{q}
\nabla^{2}_{{}^{i}sym:d\,{}^{i}sym:d}
\bigl(({}^{i}sym:v_g)_{q}\bigr)
+
\sum_{q=1}^{{}^{i}n_{v_h}}
({}^{i}sym:\kappa_h)_{q}
\nabla^{2}_{{}^{i}sym:d\,{}^{i}sym:d}
\bigl(({}^{i}sym:v_h)_{q}\bigr).\]

For convergence analysis and necessary assumptions of the original abbr:ALADIN with affine coupling constraints sym:c, see [@engelmannDistributedOptimization2022; @jiangDistributedOptimization2020; @houskaAugmentedLagrangian2016].
A detailed convergence analysis of the generalized abbr:ALADIN algorithm presented here is reserved for future work.


All symbols are defined in the [Nomenclature](../../includes/index.md). The full procedure is stated in [Algorithm 2](#algorithm-2).

<div class="algorithm" id="algorithm-2" markdown="0">
<div class="algorithm-caption"><strong>Algorithm 2</strong> Augmented Lagrangian Alternating Direction Inexact Newton (abbr:ALADIN)</div>
<div class="algo-body">
<div class="algo-line"><span><span class="algo-keyword">Require:</span> hyperparameters sym:\nu, \({}^{i}sym:\Sigma\), \({}^{i}_{j}sym:s \;\; \forall\; j \in {}^{i}sym:N,\; i \in sym:M\)</span></div>
<div class="algo-line"><span><span class="algo-keyword">Require:</span> initial \(\Delta{}^{i}sym:d\) in interface storage \(i \leftrightarrow \text{Controller} \;\; \forall\; i \in sym:M\)</span></div>
<div class="algo-line"><span><span class="algo-keyword">Require:</span> initial \({}^{i}sym:\lambda^{(0)} \;\; \forall\; i \in sym:M\)</span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line"><span>\(sym:k \leftarrow 0\) <span class="algo-comment">▷ initialize outerloop iterator</span></span></div>
<div class="algo-line"><span><span class="algo-keyword">repeat</span></span></div>
<div class="algo-line algo-indent-1"><span>\(sym:l \leftarrow 0\) <span class="algo-comment">▷ initialize innerloop iterator</span></span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">repeat</span></span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-2"><span><span class="algo-keyword">for every</span> \(i \in sym:M\) <span class="algo-keyword">in parallel do</span></span></div>
<div class="algo-line algo-indent-3"><span>Copy \(\Delta{}^{i}sym:d\) from interface storage \(i \leftrightarrow \text{Controller}\)</span></div>
<div class="algo-line algo-indent-3 algo-gray"><span>Copy \({}^{i}_{j}sym:h,\; {}^{j}_{i}sym:z\) from interface storage \(i \leftrightarrow j \;\; \forall\; j \in {}^{i}sym:N\)</span></div>
<div class="algo-math-block">
<span>

\[
{}^{i}\hat{sym:d}^{(sym:k,\,sym:l+1)} \leftarrow {}^{i}sym:d^{(sym:k,\,sym:l)} + \Delta{}^{i}sym:d
\]

</span>
</div>
<div class="algo-math-block">
<span>

\[\begin{aligned}
{}^{i}sym:d^{(sym:k,\,sym:l+1)} \leftarrow{} & \argmin_{{}^{i}sym:d} \;\; {}^{i}sym:v_f\!\left({}^{i}sym:r\right)
+ \sum_{j \in {}^{i}sym:N} \left(
\left({}^{i}_{j}sym:\lambda\right)^{T}
\begin{bmatrix}
{}^{i}_{j}sym:H\!\left({}^{i}sym:r\right) \\
{}^{i}_{j}sym:S_{z}\,{}^{i}sym:d
\end{bmatrix}
+ \left({}^{j}_{i}sym:\lambda\right)^{T}
\begin{bmatrix}
- {}^{j}_{i}sym:S_{h}\,{}^{i}sym:d \\
- {}^{i}_{j}sym:S_{z}\,{}^{i}sym:d
\end{bmatrix}
\right) \\
& + \frac{sym:\nu}{2} \left\| {}^{i}sym:d - {}^{i}\hat{sym:d}^{(sym:k,\,sym:l+1)} \right\|_{{}^{i}sym:\Sigma}^{2} \\
& \text{s.t.} \;\; {}^{i}sym:v_g\!\left({}^{i}sym:r\right) \leq 0 \quad | \; {}^{i}sym:\kappa_g \\
& \phantom{\text{s.t.}} \;\; {}^{i}sym:v_h\!\left({}^{i}sym:r\right) = 0 \quad | \; {}^{i}sym:\kappa_h \\
& \phantom{\text{s.t.}} \;\; {}^{i}sym:v_D\!\left({}^{i}sym:d\right) \leq 0 \quad | \; {}^{i}sym:\kappa_d
\end{aligned}\]

</span>
</div>
<div class="algo-line algo-indent-3"><span>Copy \({}^{i}B,\; \nabla_{{}^{i}sym:d}{}^{i}sym:v_f,\; {}^{i}sym:v_g,\; \nabla_{{}^{i}sym:d}{}^{i}sym:v_g,\; \nabla_{{}^{i}sym:d}{}^{i}sym:v_h,\; {}^{i}sym:v_D,\; \nabla_{{}^{i}sym:d}{}^{i}sym:v_D,\; \nabla^{2}_{{}^{i}sym:d\,{}^{i}sym:d}{}^{i}_{j}sym:H,\; \nabla_{{}^{i}sym:d}{}^{i}_{j}sym:H,\; {}^{i}_{j}sym:H\),</span></div>
<div class="algo-line algo-indent-3"><span>\({}^{j}_{i}sym:h,\; {}^{i}_{j}sym:z,\; {}^{j}_{i}sym:S_{h},\; {}^{i}_{j}sym:S_{z},\; {}^{i}_{j}sym:\lambda,\; {}^{i}_{j}sym:s \;\; \forall\; j \in {}^{i}sym:N\) to interface storage \(i \leftrightarrow \text{Controller}\)</span></div>
<div class="algo-line algo-indent-3 algo-gray"><span>Copy \({}^{i}_{j}sym:H,\; {}^{j}_{i}sym:h,\; {}^{i}_{j}sym:z\) to interface storage \(i \leftrightarrow j \;\; \forall\; j \in {}^{i}sym:N\)</span></div>
<div class="algo-line algo-indent-2"><span><span class="algo-keyword">end for</span></span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-2"><span><span class="algo-keyword">for Controller do</span></span></div>
<div class="algo-line algo-indent-3"><span>Copy \({}^{i}B,\; \nabla_{{}^{i}sym:d}{}^{i}sym:v_f,\; {}^{i}sym:v_g,\; \nabla_{{}^{i}sym:d}{}^{i}sym:v_g,\; \nabla_{{}^{i}sym:d}{}^{i}sym:v_h,\; {}^{i}sym:v_D,\; \nabla_{{}^{i}sym:d}{}^{i}sym:v_D,\; \nabla^{2}_{{}^{i}sym:d\,{}^{i}sym:d}{}^{i}_{j}sym:H,\; \nabla_{{}^{i}sym:d}{}^{i}_{j}sym:H,\; {}^{i}_{j}sym:H\),</span></div>
<div class="algo-line algo-indent-3"><span>\({}^{j}_{i}sym:h,\; {}^{i}_{j}sym:z,\; {}^{j}_{i}sym:S_{h},\; {}^{i}_{j}sym:S_{z},\; {}^{i}_{j}sym:\lambda,\; {}^{i}_{j}sym:s \;\; \forall\; j \in {}^{i}sym:N\) from interface storage \(i \leftrightarrow \text{Controller} \;\; \forall\; i \in sym:M\)</span></div>
<div class="algo-math-block">
<span>

\[\begin{aligned}
\left\{\Delta{}^{i}sym:d\right\}_{i \in sym:M} \leftarrow{} & \argmin_{\Delta{}^{i}sym:d \;\forall\; i \in sym:M} \;\;
\sum_{i \in sym:M} \left(
\nabla_{{}^{i}sym:d}^{T}{}^{i}sym:v_f\,\Delta{}^{i}sym:d
+ \frac{1}{2} \Delta{}^{i}sym:d^{T}\,{}^{i}B\,\Delta{}^{i}sym:d
\right) \\
& + \sum_{i \in sym:M} \sum_{j \in {}^{i}sym:N} \left(
\left({}^{i}_{j}sym:\lambda\right)^{T}
\begin{bmatrix}
\nabla_{{}^{i}sym:d}{}^{i}_{j}sym:H\,\Delta{}^{i}sym:d - {}^{i}_{j}sym:S_{h}\,\Delta{}^{j}sym:d \\
{}^{i}_{j}sym:S_{z}\,\Delta{}^{i}sym:d - {}^{j}_{i}sym:S_{z}\,\Delta{}^{j}sym:d
\end{bmatrix}
+ \frac{1}{2} \Delta{}^{i}sym:d^{T} \left(
\sum_{q=1}^{{}^{i}_{j}n_h} \left({}^{i}_{j}sym:\lambda_{h}\right)_{q} \nabla^{2}_{{}^{i}sym:d\,{}^{i}sym:d} \left({}^{i}_{j}sym:H\right)_{q}
\right) \Delta{}^{i}sym:d
\right) \\
& + \sum_{i \in sym:M} \sum_{j \in {}^{i}sym:N} \left(
2 \left( {}^{i}_{j}sym:s^{2} \circ
\begin{bmatrix}
{}^{i}_{j}sym:H\!\left({}^{i}sym:r\right) - {}^{i}_{j}sym:h \\
{}^{i}_{j}sym:z - {}^{j}_{i}sym:z
\end{bmatrix}
\right)^{T}
\begin{bmatrix}
\nabla_{{}^{i}sym:d}{}^{i}_{j}sym:H\,\Delta{}^{i}sym:d - {}^{i}_{j}sym:S_{h}\,\Delta{}^{j}sym:d \\
{}^{i}_{j}sym:S_{z}\,\Delta{}^{i}sym:d - {}^{j}_{i}sym:S_{z}\,\Delta{}^{j}sym:d
\end{bmatrix}
\right. \\
& \quad\quad\quad\quad\quad\;\; +
\begin{bmatrix}
\nabla_{{}^{i}sym:d}{}^{i}_{j}sym:H\,\Delta{}^{i}sym:d - {}^{i}_{j}sym:S_{h}\,\Delta{}^{j}sym:d \\
{}^{i}_{j}sym:S_{z}\,\Delta{}^{i}sym:d - {}^{j}_{i}sym:S_{z}\,\Delta{}^{j}sym:d
\end{bmatrix}^{T}
\operatorname{diag}\!\left({}^{i}_{j}sym:s\right)^{2}
\begin{bmatrix}
\nabla_{{}^{i}sym:d}{}^{i}_{j}sym:H\,\Delta{}^{i}sym:d - {}^{i}_{j}sym:S_{h}\,\Delta{}^{j}sym:d \\
{}^{i}_{j}sym:S_{z}\,\Delta{}^{i}sym:d - {}^{j}_{i}sym:S_{z}\,\Delta{}^{j}sym:d
\end{bmatrix} \\
& \left. \quad\quad\quad\quad\quad\;\; +
\sum_{q=1}^{{}^{i}_{j}n_h} \left( {}^{i}_{j}sym:s_{h}^{2} \circ \left( {}^{i}_{j}sym:H\!\left({}^{i}sym:r\right) - {}^{i}_{j}sym:h \right) \right)_{q}
\Delta{}^{i}sym:d^{T} \nabla^{2}_{{}^{i}sym:d\,{}^{i}sym:d} \left( \left({}^{i}_{j}sym:H\right)_{q} \right) \Delta{}^{i}sym:d
\right) \\
& \text{s.t.} \;\; {}^{i}sym:v_g + \nabla_{{}^{i}sym:d}{}^{i}sym:v_g\,\Delta{}^{i}sym:d \leq 0 \quad \forall\; i \in sym:M \\
& \phantom{\text{s.t.}} \;\; \nabla_{{}^{i}sym:d}{}^{i}sym:v_h\,\Delta{}^{i}sym:d = 0 \quad \forall\; i \in sym:M \\
& \phantom{\text{s.t.}} \;\; {}^{i}sym:v_D + \nabla_{{}^{i}sym:d}{}^{i}sym:v_D\,\Delta{}^{i}sym:d \leq 0 \quad \forall\; i \in sym:M
\end{aligned}\]

</span>
</div>
<div class="algo-line algo-indent-3"><span>Copy \(\Delta{}^{i}sym:d\) to interface storage \(i \leftrightarrow \text{Controller} \;\; \forall\; i \in sym:M\)</span></div>
<div class="algo-line algo-indent-2"><span><span class="algo-keyword">end for</span></span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-2"><span>Compute innerloop convergence criterion (e.g., [@dewitUnifiedApproach2009a; @tosseramsDistributedOptimization2008; @guoDistributedAugmented2025])</span></div>
<div class="algo-line algo-indent-2"><span>\(sym:l \leftarrow sym:l + 1\)</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">until</span> innerloop convergence criterion is met</span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-1"><span>\({}^{i}sym:d^{(sym:k+1)} \leftarrow {}^{i}sym:d^{(sym:k,\,sym:l)} \;\; \forall\; i \in sym:M\)</span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">for every</span> \(i \in sym:M\) <span class="algo-keyword">do</span></span></div>
<div class="algo-line algo-indent-2"><span>Copy \(\Delta{}^{i}sym:d\) from interface storage \(i \leftrightarrow \text{Controller}\)</span></div>
<div class="algo-line algo-indent-2 algo-gray"><span>Copy \({}^{j}_{i}sym:H\!\left({}^{j}sym:r\right),\; {}^{i}_{j}sym:h,\; {}^{j}_{i}sym:z\) from interface storage \(i \leftrightarrow j \;\; \forall\; j \in {}^{i}sym:N\)</span></div>
<div class="algo-math-block">
<span>

\[
{}^{i}\hat{sym:d}^{(sym:k+1)} \leftarrow {}^{i}sym:d^{(sym:k+1)} + \Delta{}^{i}sym:d
\]

</span>
</div>
<div class="algo-line algo-indent-2 algo-gray"><span>Copy \({}^{i}_{j}sym:H,\; {}^{j}_{i}sym:h,\; {}^{i}_{j}sym:z\) to interface storage \(i \leftrightarrow j \;\; \forall\; j \in {}^{i}sym:N\)</span></div>
<div class="algo-line algo-indent-2"><span>Copy \({}^{i}_{j}\hat{sym:H},\; {}^{j}_{i}\hat{sym:h},\; {}^{i}_{j}\hat{sym:z}\) to interface storage \(i \leftrightarrow j \;\; \forall\; j \in {}^{i}sym:N\)</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">end for</span></span></div>
<div class="algo-line no-number"><span>&nbsp;</span></div>
<div class="algo-line algo-indent-1"><span><span class="algo-keyword">for every</span> \(i \in sym:M\) <span class="algo-keyword">do</span> <span class="algo-comment">▷ decentralized Dual Update</span></span></div>
<div class="algo-line algo-indent-2"><span>Copy \({}^{j}_{i}\hat{sym:H}\!\left({}^{j}sym:r\right),\; {}^{i}_{j}\hat{sym:h},\; {}^{j}_{i}\hat{sym:z}\) from interface storage \(i \leftrightarrow j \;\; \forall\; j \in {}^{i}sym:N\)</span></div>
<div class="algo-line algo-indent-2 algo-gray"><span>Copy \({}^{j}_{i}sym:H\!\left({}^{j}sym:r\right),\; {}^{i}_{j}sym:h,\; {}^{j}_{i}sym:z\) from interface storage \(i \leftrightarrow j \;\; \forall\; j \in {}^{i}sym:N\)</span></div>
<div class="algo-math-block">
<span>

\[\begin{aligned}
{}^{i}_{j}\hat{sym:c}^{(sym:k+1)} &\leftarrow
\begin{bmatrix}
{}^{i}_{j}\hat{sym:H}\!\left({}^{i}sym:r\right) - {}^{i}_{j}\hat{sym:h} \\
{}^{i}_{j}sym:S_{z}\,{}^{i}\hat{sym:d}^{(sym:k+1)} - {}^{j}_{i}\hat{sym:z}
\end{bmatrix},
\quad
{}^{j}_{i}\hat{sym:c}^{(sym:k+1)} \leftarrow
\begin{bmatrix}
{}^{j}_{i}\hat{sym:H}\!\left({}^{j}sym:r\right) - {}^{j}_{i}sym:S_{h}\,{}^{i}\hat{sym:d}^{(sym:k+1)} \\
{}^{j}_{i}\hat{sym:z} - {}^{i}_{j}sym:S_{z}\,{}^{i}\hat{sym:d}^{(sym:k+1)}
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
{}^{i}_{j}\hat{sym:c}^{(sym:k+1)}
\right) \quad \forall\; j \in {}^{i}sym:N \\
{}^{j}_{i}sym:\lambda^{(sym:k+1)} &\leftarrow \operatorname{DualUpdate}\!\left(
{}^{j}_{i}sym:\lambda^{(sym:k)},\;
{}^{j}_{i}sym:s^{(sym:k)},\;
{}^{j}_{i}\hat{sym:c}^{(sym:k+1)}
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