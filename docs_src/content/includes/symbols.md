<!-- Single source of truth for mathematical symbols used across the documentation.  -->
<!-- Parsed by generate_diagram.py to produce the table in index.md.                  -->
<!-- Format: standard Markdown table. Do NOT use literal | inside $...$ expressions.   -->

| Symbol | Description | Value Range |
|---|---|---|
| $\mathcal{A}_g$ | set of active local inequality constraints | $...$ |
| $\mathcal{A}_D$ | set of active bounds of design variable set $\mathcal{D}$ | $...$ |
| $\alpha_1$ | globalization step size | $\mathbb{R}_+$ |
| $\alpha_2$ | globalization step size | $\mathbb{R}_+$ |
| $\alpha_3$ | globalization step size | $\mathbb{R}_+$ |
| $\beta$ | hyperparameter for subgradient method | $[1;\infty[$ |
| $\Box$ | generalized controller optimization variable | $---$ |
| $c$ | coupling constraint function | $\mathbb{R}^{n_c}$ |
| $c_h$ | coupling constraint component (mapping) | $\mathbb{R}^{n_h}$ |
| $c_{h}$ | coupling constraint component (mapping) | $\mathbb{R}^{n_h}$ |
| $c_z$ | coupling constraint component (shared variables) | $\mathbb{R}^{n_z}$ |
| $c_{z}$ | coupling constraint component (shared variables) | $\mathbb{R}^{n_z}$ |
| $\hat{c}$ | dual residual | $\mathbb{R}$ |
| $c_c$ | consensus constraint function | $\mathbb{R}^{n_y}$ |
| $d$ | design variable | $\mathbb{R}^{n_d} \times \mathbb{C}^{n_d}$ |
| $d^{*}$ | optimal design variable | $\mathbb{R}^{n_d} \times \mathbb{C}^{n_d}$ |
| $d_{1}$ | first component of design variable | $\mathbb{R}$ |
| $d_{n_d}$ | last component of design variable | $\mathbb{R}$ |
| $D$ | design variable domain (non-calligraphic notation) | $---$ |
| $\mathcal{D}$ | set of design variable | $\mathbb{R}^{n_d} \times \mathbb{C}^{n_d}$ |
| $\epsilon_{outer}$ | tolerance for outerloop convergence criterion | $\mathbb{R}^{+}$ |
| $\epsilon_{inner}$ | tolerance for innerloop convergence criterion | $\mathbb{R}^{+}$ |
| $\epsilon_k$ | tolerance hyperparameter for SBDP outerloop convergence criterion | $\mathbb{R}^{+}$ |
| $\gamma$ | hyperparameter for subgradient method | $]0;1[$ |
| $h$ | coupling variable | $\mathbb{R}^{n_h} \times \mathbb{C}^{n_h}$ |
| $h^{*}$ | optimal coupling variable | $\mathbb{R}^{n_h} \times \mathbb{C}^{n_h}$ |
| $\mathcal{H}$ | set of additional coupling design variable | $\mathbb{R}^{n_h} \times \mathbb{C}^{n_h}$ |
| $H$ | mapping operator | $-$ |
| $i$ | subsystem index | $i \in M$ |
| $j$ | neighboring subsystem index | $j \in N$ |
| $k$ | outerloop iterator | $\mathbb{I}_0^{+}$ |
| $\kappa_d$ | Lagrange multiplier associated with active bounds of design variable set D | $\mathbb{R}^{...}$ |
| $\kappa_g$ | Lagrange multiplier associated with local inequality constraint v_g | $\mathbb{R}^{n_{v_g}}$ |
| $\kappa_h$ | Lagrange multiplier associated with local equality constraint v_h | $\mathbb{R}^{n_{v_h}}$ |
| $l$ | innerloop iterator | $\mathbb{I}_0^{+}$ |
| $L$ | (augmented) Lagrange function | $\mathbb{R}$ |
| $\lambda$ | Lagrange multiplier associated with $c$ or $c_c$ | $\mathbb{R}^{n_c}$ |
| $\lambda_h$ | coordination-equality multiplier (mapped-response block) | $\mathbb{R}^{n_h}$ |
| $\lambda_z$ | coordination-equality multiplier (shared-design-variable block) | $\mathbb{R}^{n_z}$ |
| $m$ | index of last subsystem | $M$ |
| $M$ | set of indices of subsystems | $\mathbb{I}_0^{+}$ |
| $N$ | set of indices of neighboring subsystems | $\mathbb{I}_0^{+}$ |
| $n_c$ | dimension of coupling constraint function | $\mathbb{I}^{+}$ |
| $n_d$ | dimension of design variable | $\mathbb{I}^{+}$ |
| $n_h$ | dimension of coupling variable | $\mathbb{I}^{+}$ |
| $n_x$ | dimension of local design variable | $\mathbb{I}^{+}$ |
| $n_y$ | dimension of auxiliary variable | $\mathbb{I}^{+}$ |
| $n_z$ | dimension of shared design variable | $\mathbb{I}^{+}$ |
| $n_{v_g}$ | dimension of local inequality constraint function | $\mathbb{I}^{+}$ |
| $n_{v_h}$ | dimension of local equality constraint function | $\mathbb{I}^{+}$ |
| $\nu$ | penalty parameter | $\mathbb{R}_+$ |
| $p$ | coordination parameters in unified notation | $...$ |
| $P$ | objective term for coordination | $...$ |
| $\pi$ | optimization function of a subsystem | $---$ |
| $Q$ | constraint term for coordination | $...$ |
| $Q^{\leq}$ | inequality constraint term for coordination | $...$ |
| $Q^{=}$ | equality constraint term for coordination | $...$ |
| $r$ | local response function | $\mathbb{R}$ |
| $\rho$ | step size parameter | $\mathbb{R}^{n_c}$ |
| $s$ | penalty parameter | $\mathbb{R}^{n_c}$ |
| $S$ | selector matrix to retrieve ${}^ix,\:{}^i_jz,\:{}^i_jh$ from ${}^id$ | $---$ |
| $S_z$ | selector matrix for shared design variables | $---$ |
| $S_{z}$ | selector matrix for shared design variables | $---$ |
| $S_h$ | selector matrix for coupling variables | $---$ |
| $S_{h}$ | selector matrix for coupling variables | $---$ |
| $\Sigma$ | positive definite scaling matrix | $\mathbb{R}^{n_d}$ |
| $\tau$ | slack variable | $\mathbb{R}^{n_c}$ |
| $u$ | coupling information in unified notation | $...$ |
| $v_f$ | local objective function | $\mathbb{R}$ |
| $v_g$ | local inequality constraint function | $\mathbb{R}^{n_g}$ |
| $v_{g,\text{active}}$ | active set of local inequality constraints | $---$ |
| $v_h$ | local equality constraint function | $\mathbb{R}^{n_h}$ |
| $v_D$ | local box constraint function on design variables | $---$ |
| $v_{D,\text{active}}$ | active set of local box constraints | $---$ |
| $v_{\mathcal{D}}$ | local box inequality constraint function | $---$ |
| $x$ | local design variable | $\mathbb{R}^{n_x} \times \mathbb{C}^{n_x}$ |
| $x^{*}$ | optimal local design variable | $\mathbb{R}^{n_x} \times \mathbb{C}^{n_x}$ |
| $\mathcal{X}$ | set of local design variable | $\mathbb{R}^{n_x} \times \mathbb{C}^{n_x}$ |
| $y$ | auxiliary variable | $\mathbb{R}^{n_y}$ |
| $z$ | shared design variable | $\mathbb{R}^{n_z} \times \mathbb{C}^{n_z}$ |
| $z^{*}$ | optimal shared design variable | $\mathbb{R}^{n_z} \times \mathbb{C}^{n_z}$ |
| $z_{\{i,j\}}$ | condensed shared design variable between subsystems $i$ and $j$ | $\mathbb{R}^{n_z} \times \mathbb{C}^{n_z}$ |
| $z_{\{i,j\}}^{*}$ | optimal condensed shared design variable | $\mathbb{R}^{n_z} \times \mathbb{C}^{n_z}$ |
| $z_{\{0,j\}}$ | condensed shared design variable between subsystem 0 and $j$ | $\mathbb{R}^{n_z} \times \mathbb{C}^{n_z}$ |
| $z_{\{m,j\}}$ | condensed shared design variable between subsystem $m$ and $j$ | $\mathbb{R}^{n_z} \times \mathbb{C}^{n_z}$ |
| $z_{t}$ | target shared design variable | $\mathbb{R}^{n_z} \times \mathbb{C}^{n_z}$ |
| $\mathcal{Z}$ | set of shared design variable | $\mathbb{R}^{n_z} \times \mathbb{C}^{n_z}$ |
