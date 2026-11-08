# CERT-17-16 — certificate skeleton at (p, r, λ) = (17, 16, 3)

Status: **passes FORMALIZATION.md conditions (i)–(iv) literally** (machine-checked,
`verify_cert.py`); **does not lift to the pinned Lean bridge** (three gaps below,
each confirmed by code). Data: `CERT_17_16.json`.

## The design

G = Z_17 ⋊_3 Z_16, (a,k)(b,l) = (a + 3^k·b, k+l). ord(3 mod 17) = 16.

- Z₀ = Z_17 × {1} ∪ Z_17 × {2}  (two full-kernel slices, 34 elements).
- Only one survivor block exists: (k_g,k_h) = (1,1), sum slice 2, twist μ = 3:
  survivors = { ((a,1), (b,1), (a+3b mod 17, 2)) : a,b ∈ Z_17 } — exactly **289 ≤ 511**
  rank-1 terms (the t^φ degeneration with φ = 1_{G∖Z₀} keeps exactly these).
- Clean condition: all three elements of every survivor lie in Z₀ ✓.
- Junk condition: every non-survivor pair of Z₀² has its product outside Z₀ ✓
  (here: c = (a+3b, 2) always lies in slice 2, so all 17² pairs survive — the
  block is a complete 17×17 grid).

## Coverage witness (condition (iv), literal 256-(i,j)-entry reading)

Label maps α, β, γ : Z₀ → {0..15} (stored element-wise in `CERT_17_16.json`)
give every surviving term a monomial (A_{α(g),γ(c)}, B_{γ(c),β(h)}, C_{α(g),β(h)}).

Checked: the 289 terms project onto **all 256 (i,j) pairs**; 288 distinct
(i,k,j) monomials (one monomial is hit twice ⇒ coefficient 2 — recorded).

## Map to `PolynomialApproximation` (pinned: `ComplexRectangularASI.lean:63`)

```lean
structure PolynomialApproximation (T : Tensor F X Y Z) (r d D : ℕ) where
  polynomial : Tensor (Polynomial F) X Y Z                              -- 1
  rank_bound : RankAtMost polynomial r                                  -- 2
  vanishes : ∀ x y z k, k < d → (polynomial x y z).coeff k = 0          -- 3
  leading : ∀ x y z, (polynomial x y z).coeff d = T x y z               -- 4
  degree_bound : ∀ x y z, (polynomial x y z).degree ≤ D                 -- 5
```

The intended instance, for T = `matrixCoefficients (Fin 16) (Fin 16) (Fin 16)`
(slots X = Y = Z = Fin 16 × Fin 16, 256 each):

- `polynomial` := Σ_{(g,h,c) ∈ survivors} e_g ⊗ e_h ⊗ e_c pulled back along
  slot maps built from α, β, γ — a **constant** polynomial tensor (no t).
- `rank_bound` ≤ 289 ≤ 511: the 289 indicator rank-1 terms.
- `vanishes`: d = 0 ⟹ vacuous. `degree_bound`: D = 0.
- `leading`: requires the pullback to **equal T exactly**. This is where the
  certificate fails, in three independently code-confirmed ways:

### Gap 1 — support accounting (design-independent, fatal for the whole lane)

The pinned target's support is `T x y z = 1 iff x.2 = y.1 ∧ y.2 = z.1 ∧ z.2 = x.1`
(`ComplexMatrixTensor.lean:17`): exactly **16³ = 4096** unit entries. FORMALIZATION.md's
"256-entry composition support" counts only the (i,j) C-slots — it undercounts by the
free k-index. Any certificate whose rank-1 terms each carry a single monomial (the
Frobenius/indicator class this lane constructs) needs ≥ 4096 terms > 511 budget.
This certificate's pullback carries 288 monomials ≠ 4096.

### Gap 2 — k-consistency / 17→16 pair-collision (the formalization's own criterion)

The survivor bipartite graph is K_{17,17} on the 17 slice-1 elements (18 components
with 17 isolated slice-2 c-slots). Any slot-wise labeling with κ_A(g) = κ_B(h) on
every surviving edge is constant on that component ⟹ ≤ 16 distinct (i,k) A-slot
variables < 256 required. This is the "17→16 index collapse forces γ constant"
death the formalization itself recorded — but it is **not encoded in conditions
(i)–(iv)**, which is why this design passes them literally.

### Gap 3 — general terms = the open problem

Evading Gaps 1–2 needs non-indicator rank-1 polynomial terms (each term spreading
over many monomials with general vectors). That is exactly the open statement
border-rank(⟨16,16,16⟩) ≤ 511 (flattening lower bound 256); the Frobenius lane
provides no mechanism for it.

## What remains to encode in Lean

Nothing for this certificate — it must not be encoded: `leading` is unsatisfiable
for it. The correct Lean-facing conclusions are: (a) fix FORMALIZATION.md's
support count (256 → 4096) and add the slot-wise κ-consistency condition to the
design criteria; (b) the lane's indicator-class constructions are then closed off
at every (p,r) in the r ≤ 16 window by Gap 1 alone; (c) any further attempt is
Gap 3, i.e. the classical open problem, not a group-design search.

## Verification

`python3 verify_cert.py` re-derives the survivor set, clean/junk conditions,
budget, coverage, monomial ledger and connectivity from (p, r, λ, Z₀, α, β, γ)
alone; exits non-zero on any failure. All checks pass.
