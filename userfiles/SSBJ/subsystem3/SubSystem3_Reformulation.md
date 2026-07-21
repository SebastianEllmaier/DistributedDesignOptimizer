# Subsystem 3 (Structures) — Reformulation plan

## 0. Summary

This document specifies a single reformulation of the subsystem-3 design variables that fixes
**all** the current numerical/physical issues *by construction*, while remaining **equivalent**
to the original *constrained* optimization problem.

The idea is a two-level fractional parametrization of the panel thicknesses:

1. **Sandwich** thickness expressed relative to the available structural depth
   `D = beta * (t/c) * chord` (for the two panels that set the spar height), and
2. **Skin** thickness expressed as a fraction of its own sandwich.

With this choice the two structural relations that the original enforces through
ill-conditioned *division* constraints become a **box bound** and one **linear** constraint, and
the negative-core and negative/near-zero `h_spar` failure modes disappear from the analysis
entirely — the `max(ts - t, 0)` core clamp is permanently unnecessary. The `1E-5` `h_spar`
floor is **retained**, but only as a cheap guard for the one infeasible box corner the solver
still evaluates (it never activates in the feasible region). The original absolute
minimum/maximum thickness gauges are re-imposed as explicit **lower and upper** inequalities. The
design-variable **box bounds are deliberately defined on the safe (superset) side** — each lower
bound at or below an *analytic* worst-case feasible minimum, each upper bound at or above the
feasible maximum — so that the reformulated feasible set is a **superset of, and in fact equal to,**
the original: no original-feasible design can ever be clipped by a bound (proved in §8).

---

## 1. The issues in the current formulation

| # | issue | current cause |
|---|---|---|
| I1 | negative core mass | `core = ts - t` can be `< 0`; `t`, `ts` are independent box vars |
| I2 | negative / near-zero `h_spar` | `h_spar = D - 0.5(ts1+ts3)` unbounded below
| I3 | stress / twist blow-up | terms `~ 1/h_spar^2` (and `1/(c_box h_spar)^2`) explode as `h_spar -> 0` |
| I4 | constraint conditioning | `G1[42:45]` divides by `h_spar`; `G1[45:54]` divides by `ts - 0.1 t` (sign-flips when `<= 0`) |

Geometry recap (per spanwise station `i = 0,1,2`, panels: 1 = top, 2 = web, 3 = bottom):

```
D_i      = beta * (t/c) * chord_i          # available box depth  (beta = 0.9)
h_spar_i = D_i - 0.5 (ts1_i + ts3_i)       # spar (web) height; only ts1, ts3 enter
core_p   = ts_p - t_p                       # core thickness per panel
```

`t/c` and the planform (hence `chord_i`, hence `D_i`) are **shared** variables; `taper` is local.
The thickness variables `t`, `ts` are **purely local** to subsystem 3.

---

## 2. New design variables

Replace the 18 absolute thickness variables (`t1..t3`, `ts1..ts3`, 9 + 9) by 18 fractional /
mixed variables, **3 per spanwise station**:

| symbol | count | meaning | replaces |
|---|---|---|---|
| `alpha1_i` | 3 | top-sandwich depth fraction, `ts1 = 2*alpha1*D` | `ts1` |
| `alpha3_i` | 3 | bottom-sandwich depth fraction, `ts3 = 2*alpha3*D` | `ts3` |
| `ts2_i`    | 3 | web sandwich, **absolute** (in) — web does not set `h_spar` | `ts2` |
| `rho1_i`   | 3 | top skin ratio, `t1 = rho1 * ts1` | `t1` |
| `rho2_i`   | 3 | web skin ratio, `t2 = rho2 * ts2` | `t2` |
| `rho3_i`   | 3 | bottom skin ratio, `t3 = rho3 * ts3` | `t3` |

DOF preserved: `3*6 = 18` (original `9 t + 9 ts = 18`).

### Reconstruction map (computed inside the analysis, after `Wing_Mod`)
```
D_i  = beta * (t/c) * chord_i
ts1  = 2 * alpha1 * D ;   ts3 = 2 * alpha3 * D ;   ts2 = ts2  (absolute)
t1   = rho1 * ts1     ;   t2  = rho2 * ts2     ;   t3  = rho3 * ts3
core_p   = ts_p * (1 - rho_p)
h_spar   = D * (1 - alpha1 - alpha3)
```
`D` uses only quantities available locally in subsystem 3 (its own copies of the shared
geometry plus local `taper`), so the new variables are genuinely **local**.

The map is a **bijection** to the physical `(t, ts)` at fixed `D`, so every response is the
exact original function of the reconstructed `(t, ts)`.

---

## 3. Bounds and their derivation

These bounds, **together with the absolute-gauge inequalities of §4**, are chosen so that the
**reformulated feasible set coincides with the original feasible set**: every design feasible in
the original has an admissible `(alpha, rho, ts2)` image, and no design infeasible in the original
is admitted. The `alpha`/`rho` upper bounds sit exactly on an original *feasibility edge*
(the `h_spar` margin and the core margin); the absolute thickness gauges `t in [0.1,4]`,
`ts in [0.1,9]` are reproduced as explicit **lower and upper** inequalities (§4) rather than as box
bounds; and the `alpha_min`/`rho_min` lower box bounds sit strictly below the feasible minimum
(§3.3) so they only serve as positivity safeguards and cut nothing.

| variable | lower | upper | derivation |
|---|---|---|---|
| `alpha1_i`, `alpha3_i` | `1e-4` (`alpha_min`, §3.3) | `0.5` | see §3.1 |
| `ts2_i` (web, in) | `0.1` | `9.0` | unchanged absolute gauge (identical to original) |
| `rho1_i`, `rho2_i`, `rho3_i` | `1e-3` (`rho_min`, §3.3) | `1/1.1 = 0.90909...` | see §3.2 |

Structural depth is `D_i = beta * (t/c) * chord_i`. The lower-bound derivations below need only the
**global worst-case (maximum) depth**, which is obtained **analytically** from `Wing_Mod` (not from
sampling): chord is maximized at the in-bounds corner `Sw = 800, ARw = 2.5, taper = 0.1`, giving the
root chord `c[0] = 2*sqrt(800) / (1.1*sqrt(2.5)) = 32.5 ft`, so with `t/c = 0.1`, `beta = 0.9`:

```
D_max^global = 0.9 * 0.1 * 32.5 ft = 2.93 ft = 35.1 in     # root station; c[1], c[2] < c[0]
```

`D` is bounded **below** by a small but strictly positive value (~0.5 in, reached at the smallest
in-bounds wing with `t/c = 0.01` and a small tip chord); this lower bound is used only for the
conditioning discussion (§5), never for feasibility.

> **Correction vs. earlier drafts.** A previous version derived these bounds from a 200k-sample
> `Wing_Mod` sweep whose tabulated `D_max(root) = 21.33 in` *understated* the true in-bounds maximum
> (`35.1 in` above). That made `alpha_min = 0.002` larger than the true smallest feasible `alpha`,
> which would have **clipped feasible thin-sandwich designs at the high-depth root** and silently
> broken equivalence. The analytic worst case removes the dependence on sampling.

### 3.1 Upper `alpha = 0.5` is the `h_spar` feasibility edge (not restrictive)
`h_spar_i = D_i (1 - alpha1_i - alpha3_i)`. The original `h_spar` margin constraint `G1[42:45]`
is algebraically `alpha1 + alpha3 <= 0.5` (§5), so **every feasible original design already has**
`alpha1 + alpha3 <= 0.5` — hence `alpha_k <= 0.5` per panel excludes **no feasible design**.
A literal superset of the original *box* would instead allow `alpha` up to `9/(2 D_min)` (well
above 1 for the smallest in-bounds depths), but that region is exactly where `alpha1 + alpha3 > 1`
drives `h_spar < 0` and the `1e13/1e19`
blow-ups — infeasible in the original, and re-admitting it would defeat the reformulation. So
`0.5` is the correct feasibility-preserving upper bound. The linear constraint
`alpha1 + alpha3 <= 0.5` (§4) still enforces the *joint* margin; the per-panel box only caps each
fraction.

### 3.2 Upper `rho = 1/1.1` is the core-margin feasibility edge (not restrictive)
`core_p = ts_p (1 - rho_p)`. The original 10 %-of-skin core margin `ts >= 1.1 t` is exactly
`rho = t/ts <= 1/1.1`. So `rho <= 1/1.1` reproduces the original ratio constraint `G1[45:54]`
**as a box bound** and excludes no feasible design (a literal box-superset would allow `rho` up to
`4/0.11 ~ 36`, i.e. the core-margin-violating points the original already rejected).

### 3.3 Lower bounds `alpha_min = 1e-4`, `rho_min = 1e-3` (positivity safeguards only)
These lower box bounds do **not** encode the `0.1`-inch minimum gauge — that is re-imposed as an
explicit inequality in §4. They serve two purposes: (a) they must sit *strictly below* the
smallest value any feasible design can take **at the worst-case depth**, so they cut nothing; and
(b) they keep the reconstructed `t`, `ts` **strictly positive** at the infeasible trial points
where the §4 gauge inequalities are violated (so the stress terms `q/t`, `c_box/t` never divide by
exactly zero).

The smallest *feasible* sandwich is `ts = 1.1 * t_lo = 0.11 in` (skin floor plus core margin), and
the smallest feasible depth fraction `alpha = ts/(2 D)` is reached at the **largest** depth. Using
the analytic global worst case `D_max^global = 35.1 in` (§3 — **not** a sampled estimate):

```
alpha_lo^feas = 0.11 / (2 * 35.1) = 0.00157     # global minimum over all stations and designs
```

and the smallest feasible skin ratio is `t_lo/ts_hi = 0.1/9 = 0.011` (independent of `D`). The
lower box bounds are set an order of magnitude below these feasible minima, so they provably cut
nothing **even under the worst-case depth**:
- `alpha_min = 1e-4  << 0.00157 = 0.11/(2 * D_max^global)`   (~15x margin)
- `rho_min   = 1e-3  << 0.011   = 0.1/9`                     (~11x margin)

**Important:** `alpha_min`/`rho_min` alone allow the reconstructed `ts = 2 alpha D` and
`t = rho ts` to fall **well below** the `0.1`-inch floor at small-`D` stations (e.g.
`ts ~ 1e-4 in`, `t ~ 1e-7 in` at the tip). That is intentional — the box only guarantees
positivity; the `0.1`-inch minimum gauge itself is enforced by the §4 lower-gauge inequalities.
Without those inequalities the feasible set would be enlarged on the thin side (breaking
equivalence whenever the minimum gauge is active, which is typical at the lightly loaded tip) and
the `1/t` stress terms would be orders of magnitude larger than the original ever permitted — see
§4 and §5.

---

## 4. Constraints: removed / replaced / added / kept

Reference: `LocalConstraints3.py`, `evaluateInEqualityLocalConstraints`.

### Removed (both are division-based, ill-conditioned — issue I4)
- **`G1[45:54]`** (9 ratio constraints `t/(ts - 0.1 t) - 1 <= 0`): now the **box bound**
  `rho <= 1/1.1`. Eliminated, and the `ts - 0.1 t` denominator sign-flip vanishes.
- **`G1[42:45]`** (3 constraints `0.5(ts1+ts3)/h_spar - 1 <= 0`): replaced below.

### Replaced (now linear, division-free)
- **`h_spar` margin** — one per station:
  ```
  g_hspar,i = alpha1_i + alpha3_i - 0.5 <= 0
  ```
  This is *algebraically identical* to the original `G1[42:45]` (see §5), but contains no
  division by `h_spar`.

### Added (re-impose the absolute gauges, now that `ts1, ts3, t1..t3` are depth-relative)
Because a constant fraction maps to a *depth-dependent* physical thickness, the absolute gauges
that were box bounds in the original must be re-imposed as inequalities (well-conditioned, linear
in the reconstructed `t`, `ts`). **Both** the upper *and* the lower gauges are re-imposed: a
constant `alpha`/`rho` can push the reconstructed thickness above `9`/`4` at large `D` *and* below
`0.1` at small `D`, so dropping the lower gauge would both enlarge the feasible set on the thin
side (breaking equivalence when the minimum gauge is active) and reintroduce a `1/t` blow-up
*worse* than the original:
```
sandwich top/bottom :   0.1 <= ts1_i <= 9.0 ,   0.1 <= ts3_i <= 9.0
skin (all panels)   :   0.1 <= t_p,i  <= 4.0
```
The web sandwich `ts2` keeps its hard box bound `[0.1, 9.0]` (it is still an absolute variable),
so among the web quantities only its skin `t2 = rho2 ts2` needs the `0.1 <= t2 <= 4.0` pair. The
`alpha_min`/`rho_min` box bounds (§3.3) sit below the feasible minimum and only guarantee strict
positivity at infeasible trial points; they do **not** substitute for these gauge inequalities.

Count: `ts1, ts3` each contribute a lower + upper pair over 3 stations (`2*2*3 = 12`); `t1, t2, t3`
each contribute a lower + upper pair over 3 stations (`2*3*3 = 18`); total **30** gauge
inequalities.

### Kept (unchanged in role; they consume the reconstructed `t`, `ts`)
- All stress / buckling constraints `G1[0:42]` and `G1[54:72]`.

### Net conditioning change
12 division-based constraints (`G1[42:54]`) are removed; `3` linear `h_spar`-margin constraints
and `30` linear absolute-gauge inequalities are added (net `+21`: the inequality count grows from
`72` to `93`). The replacements are all **division-free**, and every added constraint is linear in
the design variables or in the reconstructed `t`, `ts`.

---

## 5. How each issue is solved, and why it stays equivalent

### Issue-by-issue
- **I1 (negative core):** `core_p = ts_p (1 - rho_p)` with `rho_p <= 1` is `>= 0` **by box bound**,
  for *every* panel. The reverted `max(ts - t, 0)` clamp is permanently unnecessary.
- **I2 (negative/near-zero `h_spar`):** `h_spar = D (1 - alpha1 - alpha3) >= 0` by the `alpha`
  box, and `>= 0.5 D` in the feasible region by `alpha1 + alpha3 <= 0.5`, so it never goes
  negative (no sign-flipped stresses). The one residual case is the box corner
  `alpha1 = alpha3 = 0.5`, where `h_spar = 0` exactly: this point is infeasible (it violates the
  `alpha`-sum margin) but the solver still *evaluates* it, so the cheap
  `h_spar = max(h_spar, 1E-5)` floor is **kept** purely as a guard against an exact
  divide-by-zero there. The floor never activates in the feasible region, so it does not affect
  equivalence.
- **I3 (stress/twist blow-up):** in the feasible region two facts bound *both* blow-up families:
  `h_spar >= 0.5 D` bounds `1/h_spar^2 <= 4/D^2` (and the twist `Phi ~ 1/(c_box h_spar)^2`), and
  the re-imposed lower gauges `t >= 0.1`, `ts >= 0.1` (§4) bound the skin-thickness terms `q/t`,
  `c_box/t`. This removes the pathological `1e13`/`1e19` excursions of the original (which arose
  from `h_spar -> 0` while the chord stayed moderate — now impossible, since `h_spar >= 0.5 D` and
  `D` is proportional to chord). **It does not make the terms uniformly small:** at the thin-wing /
  small-chord corner the torsion term `1/(c_box h_spar)^2 ~ 1/(chord^4 (t/c)^2)` can still reach
  `~1e4-1e6` with `t/c = 0.01`. That residual magnitude is **physically genuine** (slender, thin
  wings really do twist far more) and **finite**, not a numerical artifact — the reformulation
  makes the problem *physically conditioned* rather than perfectly scaled. The lower gauges are
  essential to this bound: with only `alpha_min`/`rho_min`, the reconstructed `t` could fall to
  `~1e-7 in` and the `1/t` terms would dwarf anything the original min-gauge permitted.
- **I4 (constraint conditioning):** the two division families become a box bound (`rho`) and one
  linear constraint (`alpha1 + alpha3 <= 0.5`). No division by `h_spar` or by `ts - 0.1 t`.

### Equivalence argument
1. **Physics is exact.** At the `D` of the current iterate, `(alpha, rho, ts2) -> (t, ts)` is a
   bijection; all responses are the unchanged functions of `(t, ts)`.
2. **The three structural relations are reproduced exactly:**

   | original | reformulated | type |
   |---|---|---|
   | `core >= 0` (implicit) | `rho <= 1` | box |
   | `ts >= 1.1 t`  (`G1[45:54]`) | `rho <= 1/1.1` | box |
   | `ts1 + ts3 <= D`  (`G1[42:45]`) | `alpha1 + alpha3 <= 0.5` | linear |

   The last identity: `alpha1 + alpha3 <= 0.5  <=>  2 D (alpha1+alpha3) <= D  <=>  ts1 + ts3 <= D`,
   which is precisely `0.5(ts1+ts3) <= h_spar` since `h_spar = D - 0.5(ts1+ts3)`.
3. **The absolute gauges (`0.1 <= ts <= 9`, `0.1 <= t <= 4`) are reproduced exactly** by the §4
   lower- *and* upper-gauge inequalities. The `alpha_min`/`rho_min` box only adds strict
   positivity below the feasible minimum (§3.3) and so cuts nothing.

Because the original box bounds on `t`, `ts` are reproduced as inequalities and the three
structural relations are reproduced as a box/linear set, the reformulated **feasible set coincides
with** the original's physically meaningful region — not merely a superset — and the **constrained
optima coincide**, *including* when the minimum gauge is active at the optimum (e.g. at the tip).
The only region the reformulation removes from the *box* is the non-physical part the original
constraints already rejected (negative core, `h_spar <= 0`).

---

## 6. Required code changes

### 6.1 `calculate_responses3.py`
- **Signature:** accept the fractional variables instead of `t`, `ts`:
  `calculate_structural_responses(taper_ratio, alpha1, alpha3, ts2, rho1, rho2, rho3,
  thickness_to_chord_ratio, wing_sweep_angle, wing_aspect_ratio, wing_surface_area,
  tail_aspect_ratio, tail_surface_area, lift, h)` (each `alpha*/rho*` a length-3 array, `ts2` in
  inches).
- **Reorder:** call `Wing_Mod(...)` **first** (it is already called before `h_spar`), then build
  the depth and reconstruct, replacing the current inches->feet block and the `h_spar` block:
  ```python
  c, c_box, Sweep_40, D_mx, b, a = Wing_Mod(...)            # unchanged call
  D   = beta * float(thickness_to_chord_ratio) * np.array(c[0:3])   # available depth (ft)

  ts1 = 2.0 * np.asarray(alpha1) * D
  ts3 = 2.0 * np.asarray(alpha3) * D
  ts2 = np.asarray(ts2) / 12.0                              # web absolute, in -> ft
  t1  = np.asarray(rho1) * ts1
  t2  = np.asarray(rho2) * ts2
  t3  = np.asarray(rho3) * ts3

  h_spar = D * (1.0 - np.asarray(alpha1) - np.asarray(alpha3))   # >= 0 in the feasible region
  h_spar = np.maximum(h_spar, 1E-5)   # KEEP: guards the exact box corner alpha1 = alpha3 = 0.5

  hspar_margin = np.asarray(alpha1) + np.asarray(alpha3) - 0.5   # <= 0 is the h_spar margin (§4); returned for responses[93:96]
  ```
- **Keep** the line `h_spar = np.maximum(h_spar, 1E-5)` and its header note: it never activates in
  the feasible region (`h_spar >= 0.5 D`), but it prevents an exact divide-by-zero at the
  infeasible box corner `alpha1 = alpha3 = 0.5` (where `h_spar = 0`), which the solver may still
  evaluate.
- **Delete** (already reverted) any `max(ts - t, 0)` core clamp; `ts_p - t_p = ts_p(1 - rho_p) >= 0`
  is guaranteed by the `rho <= 1/1.1` box, so the clamp is permanently unnecessary.
- **Units:** `c[0:3]` (hence `D`) are in **feet**, so `ts1 = 2 alpha D`, `ts3`, and the
  reconstructed `t1, t3` come out in feet; `ts2` is converted in->ft above. `alpha`, `rho` are
  dimensionless, so the §3 bounds (derived from the analytic worst-case depth in inches) apply
  unchanged. The §4
  gauge inequalities must compare against the gauges in the **same units** as the reconstructed
  `t`, `ts` the constraint module reads from `responses[75:93]` (feet) — i.e. `0.1 in = 0.1/12 ft`,
  `9 in = 9/12 ft`, `4 in = 4/12 ft`.
- Everything downstream (`A_top`, `Izz`, `loads`, weights, stresses) is **unchanged** — it
  consumes the reconstructed `t1..t3`, `ts1..ts3`. The function still returns the reconstructed
  `t_ft`/`ts_ft` for the constraint module and **additionally returns the 3 `hspar_margin`
  values**, which `Analysis3` places at `responses[93:96]` (§6.2).

### 6.2 `Analysis3.py`
- Remap `des_var` slices to the new layout (keeping the shared block `[19:26]` untouched so the
  coupling to subsystems 0/2 is unaffected):
  ```
  [0]      taper
  [1:4]    alpha1      [4:7]   alpha3     [7:10]  ts2 (in)
  [10:13]  rho1        [13:16] rho2       [16:19] rho3
  [19] t/c ... [25] lift     (unchanged shared variables)
  ```
- Pass these to `calculate_structural_responses`. Assemble `responses` in this **exact order** so
  that `Ws, Wf, theta` remain the **last three** entries (the coupling map in
  `mapLocalResponsesDesignVariables_to_CouplingParameters` reads them by *negative* index
  `responses[-3]`, `responses[-2]`, `responses[-1]`):
  ```
  responses = C_structure_flat   # [0:75]   (includes h_spar at [72:75])
            + t_ft               # [75:84]  reconstructed skin, ft
            + ts_ft              # [84:93]  reconstructed sandwich, ft
            + hspar_margin       # [93:96]  alpha1 + alpha3 - 0.5  (3 values)  <-- NEW, BEFORE Ws/Wf/theta
            + [Ws, Wf, theta]    # [96:99]  -> still responses[-3], [-2], [-1]
  ```
  **Critical:** the 3 `h_spar`-margin values must be inserted **before** `[Ws, Wf, theta]`, not
  appended at the end. Appending at the end would make `responses[-1]` the third margin and
  silently corrupt the `wing_twist` / `structural_weight` / `fuel_weight` coupling to subsystems 0
  and 2. `LocalConstraints3` reads the margins at the fixed positive indices `responses[93:96]`.
- **Scaler indices:** the mapped-response scalers referenced here move from `scalers[100/101/102]`
  to `scalers[121/122/123]` because the inequality block grows by `+21` (§6.3). Update the
  `set_MappedResponseVariables` calls accordingly. (The negative-index reads of `responses` are
  unaffected by this scaler shift, since `Ws/Wf/theta` stay last by construction above.)

### 6.3 `InputFile.py`
- Update subsystem-3 lower/upper bounds for indices `[1:19]` to the new ranges (§3). The new
  layout per station is `alpha1, alpha3 in [1e-4, 0.5]`, `ts2 in [0.1, 9.0]`,
  `rho1, rho2, rho3 in [1e-3, 0.90909]` (see §6.2 for the index assignment).
- Update the corresponding 18 `ScalerZeroOne` entries to match those ranges.
- **Inequality scalers:** remove the 12 entries `scalers[70:82]` (the old `G1[42:54]`) and append
  one `ScalerConstraint` per newly added inequality (3 `h_spar`-margin + 30 absolute-gauge = 33),
  giving `72 - 12 + 33 = 93` inequality scalers, i.e. block `[28:121]` (§6.4 lists the recommended
  magnitudes).
- **Index shift (important):** because the inequality block grows by `+21` (72 -> 93), every
  hardcoded scaler index *after* it shifts by `+21`. The mapped-response copies move from
  `[100],[101],[102]` to `[121],[122],[123]`; update them here, in `Analysis3.py` (§6.2), and the
  slice `scalers[28:100] -> scalers[28:121]` in `LocalConstraints3.py` (§6.4). The shared scalers
  `[19:25]` and the lift scaler `[25]` are unchanged.
- **Pre-existing caveat (verify while here):** the existing `scalers[28:100]` comment labels in
  `InputFile.py` ("geometric / stress / lower-bound constraint") are already out of order relative
  to the actual constraint sequence built in `LocalConstraints3.py`, and several magnitudes look
  tuned for a raw-stress (not dimensionless `value/limit-1`) formulation. Re-derive/verify the
  kept stress-constraint scaler magnitudes against the current constraint expressions when editing
  this block. **See §9 for the recommended sequencing — fix this stale/misaligned scaler block
  independently and lock a regression baseline _before_ reparametrizing.**

### 6.4 `LocalConstraints3.py`
- **Remove** `G1[42:45]` and `G1[45:54]` (12 entries) and their scalers `scalers[28+42 : 28+54]`
  ( = `scalers[70:82]`).
- **Add**, *appended at the end of the inequality list* (so the positional `scalers[28:...]`
  mapping of the kept stress/buckling constraints is not disturbed):
  - the 3 linear `h_spar`-margin constraints `alpha1_i + alpha3_i - 0.5 <= 0`. These need the
    design variables, not just `responses`. Compute `alpha1 + alpha3 - 0.5` inside
    `calculate_structural_responses` and place it in `responses` at indices `[93:96]` — i.e.
    **after** `ts_ft` but **before** `[Ws, Wf, theta]` (§6.2), so the coupling map's negative-index
    reads of `Ws/Wf/theta` stay valid. `LocalConstraints3` then reads these constraints from
    `responses[93:96]`; otherwise read them via `subsystem.get_DesignVariables_Unscaled()`.
  - the **30** absolute-gauge inequalities of §4 — **lower and upper**:
    `0.1 - ts1 <= 0`, `ts1 - 9 <= 0` (and the same for `ts3`); `0.1 - t_p <= 0`, `t_p - 4 <= 0`
    (for `t1, t2, t3`). Compare in the **same units** as `responses[75:93]` (feet): use
    `0.1/12`, `9/12`, `4/12` (§6.1).
- Keep stress/buckling `G1[0:42]`, `G1[54:72]` and their scalers; the kept slice becomes
  `scalers[28:121]` (§6.3).
- **Scalers:** every newly added inequality needs a matching `ScalerConstraint` entry in
  `InputFile.py` (§6.3). Scale the `h_spar`-margin gauges by `O(1)` (`ScalerConstraint(-1.0, 1.0)`
  — the value is the `alpha`-sum minus `0.5`). Scale each absolute-gauge inequality by its gauge
  magnitude in **feet**: about `0.75` for the `9 in = 9/12 ft` sandwich gauges and about `0.33`
  for the `4 in = 4/12 ft` skin gauges (apply the same magnitude to the matching lower gauge).

---

## 7. Caveat: hard bounds become soft constraints

The original absolute gauges `t in [0.1,4]`, `ts1/ts3 in [0.1,9]` are **box bounds**, which the
solver (NOMAD) never violates — so the original analysis never receives a degenerate thickness.
After the reparametrization these gauges become **inequality constraints** (§4, lower *and*
upper), which the solver *can* violate at infeasible trial points. Two safeguards preserve the
robustness the original got for free from its box:

1. **Strict positivity of `t`, `ts`.** The `alpha_min`/`rho_min` box (§3.3) together with
   `D >= D_min > 0` keeps the reconstructed `t`, `ts` strictly positive even where the gauge
   inequalities are violated, so `q/t` and `c_box/t` never divide by exactly zero. (They can still
   grow large in the deep-infeasible region, but they remain finite and the lower-gauge
   inequalities push the optimizer back toward `t, ts >= 0.1`.)
2. **Strict positivity of `h_spar`.** `h_spar = D(1 - alpha1 - alpha3)` is `>= 0.5 D` in the
   feasible region; the only place it hits exactly zero is the infeasible box corner
   `alpha1 = alpha3 = 0.5`. The retained `h_spar = max(h_spar, 1E-5)` floor (§6.1) guards that one
   point and never activates in the feasible region, so it does not affect equivalence.

This soft-gauge behaviour is the single genuine cost of the reformulation — the price of
converting the local-shared `h_spar` coupling into a structural guarantee. Everything else is an
improvement: negative core and negative/near-zero `h_spar` are impossible in the feasible region,
the two ill-conditioned division constraint families are gone, the minimum/maximum gauges are
preserved (so the optima coincide), and the stress/twist terms are bounded (though **not** made
uniformly small — see I3 in §5) by physical depth and physical thickness in the feasible region.

---

## 8. Design-bound definition and the feasible-set guarantee (`F_new` ⊇ `F_orig`, in fact `=`)

This section fixes the design bounds **exactly as the implementation must set them** and proves that,
together with the constraints of §4, they make the reformulated feasible set a **superset of — and
in fact equal to — the original feasible set**. The bounds are chosen on the *safe (superset) side*:
every lower bound sits at or below an **analytic** worst-case feasible minimum and every upper bound
at or above the feasible maximum, so **no original-feasible design can be excluded by a box bound**,
regardless of any sampling precision. This is the decisive replacement for the earlier
"equivalence holds only if `alpha_min` is tuned below the feasible minimum" reasoning: here the
bounds are *over-wide by construction*, and feasibility is carried entirely by the explicit
constraints of §4.

### 8.1 The design bounds (final, normative)

Per spanwise station `i = 0, 1, 2` (18 local thickness variables):

| variable | lower | upper | role |
|---|---|---|---|
| `alpha1_i`, `alpha3_i` | `1e-4` | `0.5` | search box; lower is superset-safe, upper is the `h_spar`-margin edge |
| `ts2_i` (web, in) | `0.1` | `9.0` | identical to the original box |
| `rho1_i`, `rho2_i`, `rho3_i` | `1e-3` | `1/1.1 = 0.90909...` | search box; lower is superset-safe, upper is the core-margin edge |

The shared block `[19:25]` and `lift [25]` keep their original bounds (§6.3); only the 18 local
thickness variables are rebounded.

### 8.2 Superset: `F_new` ⊇ `F_orig` (no feasible design is ever clipped)

Let `F_orig` be the original feasible set in `(t, ts)` and `F_new` the image of the reformulated
feasible set under the reconstruction map. Superset means **every** original-feasible design has a
preimage inside the reformulated box. At the iterate's depth `D`, that preimage is
`alpha_k = ts_k/(2D)`, `rho_p = t_p/ts_p`, `ts2` absolute. Each coordinate provably lies inside its
box:

- **`alpha` lower.** The smallest feasible `alpha = ts/(2D)` is attained by the smallest sandwich
  over the largest depth: `alpha >= 0.1/(2 * D_max^global) = 0.1/(2 * 35.1) = 0.001425` (or `0.00157`
  if the core margin `ts >= 0.11` is used). `alpha_min = 1e-4` lies **below** both — it contains
  every feasible `alpha`.
- **`alpha` upper.** Every feasible design obeys `ts1 + ts3 <= D`, so `alpha1, alpha3 = ts/(2D) < 0.5`.
  The bound `0.5` lies **at/above** every feasible `alpha`.
- **`rho` lower.** `rho = t/ts >= t_min/ts_max = 0.1/9 = 0.0111`. `rho_min = 1e-3` lies below it.
- **`rho` upper.** The core margin `ts >= 1.1 t` gives `rho = t/ts <= 1/1.1`. The bound `1/1.1`
  contains this closed edge.
- **`ts2`.** Box identical to the original → contains every feasible `ts2`.

Since the box contains the preimage of every original-feasible point, and since each retained
constraint of §4 is an **exact restatement** of an original constraint (§5, *Equivalence argument* —
it removes none and adds none), no original-feasible design is excluded: **`F_new` ⊇ `F_orig`**.

**Why this is decisive (margin, not a knife-edge).** The superset guarantee needs only
`alpha_min <= 0.1/(2 * D_max)` and `rho_min <= 0.1/9`. The chosen values clear these by `~14x` and
`~11x`. Equivalently, the `alpha`-side guarantee holds for **any** true depth
`D_max <= 0.1/(2 * alpha_min) = 500 in`, against an actual `D_max = 35.1 in` — so the result cannot
be broken by an imprecise depth estimate. (If extra safety is ever wanted, lower `alpha_min`/`rho_min`
further; smaller values only enlarge the search box and never affect feasibility, which the §4
gauges enforce.)

### 8.3 Equality: `F_new` `=` `F_orig`

Conversely, every reformulated-feasible point satisfies the reconstructed absolute gauges
(`0.1 <= t <= 4`, `0.1 <= ts <= 9`, in), the ratio box (`rho <= 1/1.1  <=>  ts >= 1.1 t`), the
linear margin (`alpha1 + alpha3 <= 0.5  <=>  ts1 + ts3 <= D`), and the unchanged stress/buckling
constraints — i.e. its `(t, ts)` image satisfies **every** original constraint and is therefore
original-feasible: `F_new` ⊆ `F_orig`. With §8.2 this gives **`F_new` = `F_orig`**.

The reformulation is thus a **bijective change of local search coordinates** that leaves the
feasible set unchanged and — because the coupling block (§6.2) is byte-for-byte identical — leaves
the distributed problem's optimum and consistency constraints identical to the original. Only the
coordinates in which subsystem 3 searches change.

---

## 9. Implementation sequencing and hazards

1. **Fix the scaler block independently first.** The existing `scalers[28:100]` block in
   `InputFile.py` already has (a) comment labels ("geometric / stress / lower-bound") that do **not**
   match the actual constraint order built in `LocalConstraints3.py` (stress/buckling `[0:42]`, then
   ratio/geometry `[42:54]`, then sign-flips `[54:72]`), and (b) magnitudes (e.g. `±20893`,
   `±841091337`) that look tuned for a **raw-stress** formulation, whereas the current constraints
   are dimensionless `value/limit - 1 ~ O(1)`. Performing this reformulation's `+21` index shift and
   12-remove / 33-add surgery *on top of* a misaligned base compounds two hard-to-debug problems.
   Re-align the labels, re-derive/verify the kept stress-constraint scaler magnitudes, and lock in a
   regression baseline **before** reparametrizing.
2. **Unit hazard for the new gauges.** The original ratio/geometry constraints were dimensionless,
   so units cancelled. The new absolute-gauge inequalities are **not** dimensionless and are
   compared against `responses[75:93]`, which are in **feet**. Use `0.1/12`, `9/12`, `4/12` (ft),
   *not* `0.1`, `9`, `4`. A units slip here yields a silently wrong feasible set.
3. **Constraint/scaler surgery in lock-step.** Remove `G1[42:54]` and the matching `scalers[70:82]`
   from *both* lists together (so the kept sign-flip block and its scalers shift consistently), and
   append the 33 new constraints and their 33 scalers in the *same order* in `LocalConstraints3.py`
   and `InputFile.py`. Add a one-off assertion that the inequality count equals the scaler-slice
   length (`93`, i.e. `scalers[28:121]`).
