# Formalization: Frobenius lane vs the M16 border certificate

## Target (fixed by the pinned Lean bridge)

One `PolynomialApproximation` of `[16,16,16]` with `rank_bound r ≤ 511`
(511⁴ < 16⁹ = 2³⁶), via `equalSquare_inequality_of_polynomialApproximation`
(Rectangular/ASI.lean, openai/math pinned commit). The polynomial field is a
`Tensor (Polynomial F) 16 16 16`; `rank_bound` counts rank-one *polynomial*
terms whose t→0 limit reproduces ⟨16,16,16⟩ (the **4096-entry** composition
support `{(A_ik, B_kj, C_ij) : i,k,j ∈ [16]}` in 16×16×16 format).

**Support correction (2026-11-07, commit c4f666b).** The pinned target is
`matrixCoefficients (Fin 16) (Fin 16) (Fin 16)`, slots `Fin 16 × Fin 16`,
`T x y z = 1 iff x.2 = y.1 ∧ y.2 = z.1 ∧ z.2 = x.1`
(`Tensor/ComplexMatrixTensor.lean:17`) — exactly **16³ = 4096 unit entries**,
one per (i,k,j). Earlier text said "256 entries"; that figure counted only the
(i,j) C-slots and undercounts by the free k-index by a factor 16.

## Lane object

`G = Z_p ⋊_λ C_r`, p prime, r | p−1, λ of order r (fixed-point-free action ⟹
Frobenius). Kernel C_p, complement C_r, |G| = pr, smallest nonlinear degree
D = r. Group tensor T_G = Σ_{g,h} e_g⊗e_h⊗e_{gh} (|G|² rank-1 terms).

A **dTPP** (swarm part 2 definition) = support choice + integer potential
φ: G → Z≥0 with φ(s)+φ(t)+φ(st) = 0 on designated matmul triples and ≥ 1 on
every extra solution. The t^φ degeneration keeps exactly the φ=0 terms, so

    border rank(target) ≤ #{φ=0 terms}.

## Lemma 1 (0/1-collapse — exact, trivial proof)

If w ∈ Z≥0^G is feasible, so is w' = min(w,1): clean sums are 0 termwise; a
junk sum ≥ 1 has some term ≥ 1 which survives truncation; surviving sets are
identical. **Wlog φ = 1_{G∖Z₀}** for a zero-set Z₀ ⊆ G, and the exact
potential LP collapses to a set-design problem:

  - clean (a,b,k): a, b, a+λᵏb ∈ Z₀ (all three),
  - junk in support: at least one of the three outside Z₀,
  - certified border count = #{surviving triples} ≤ 511, projecting onto the
    4096-entry composition support of ⟨16,16,16⟩ exactly,
  - **(slot-wise lift criterion — Gap 2).** The projection must be realizable
    by slot-wise label maps α,β,γ: Z₀ → {0..15} with a consistent k-label:
    κ_A(g) = κ_B(h) on every surviving pair (g,h); equivalently the k-label is
    constant on each connected component of the survivor bipartite graph.
    Conditions (i)–(iv) as written (free per-term labels, 256 (i,j)-pairs) do
    **not** encode this: a design can pass (i)–(iv) literally and still fail
    the Lean lift.

The "exact potential LP" is therefore the feasibility system over Z₀; its LP
value per (p,r) is the certified border-count floor B(p,r) computed by
`screens.py` (volume / index / threshold-split / border-count screens, all in
exact integer arithmetic via x > y^{4/3} ⟺ x³ > y⁴).

## Lemma 2 (translation-orbit accounting)

Translation by the kernel (a,k) ↦ (a+x,k) acts on T_G's terms. If a potential
is kernel-translation-invariant (as any class-function ansatz is), surviving
terms come in full p² translation orbits ⟹ certified count ≥ p². For p ≥ 257
this is ≥ 66049 ≫ 511: **no class-function potential can reach 511.** The
potential must be genuinely non-invariant, i.e. Z₀ is a genuine design inside
the kernel — this is the precise content of the swarm's "reduces to solution
counts in C_r": the junk a slice must kill is governed by how Z₀²-pairs fold
back into Z₀ under each twist a+λᵏb.

## Screens applied per (p,r) (exact arithmetic)

1. window: r | p−1, p < r⁴ (the open window), nonabelian.
2. 16-index screen: r < 16 ⟹ matmul entries must ride the kernel ⟹ p ≥ 256.
3. volume: ∃ s,t,u ≥ 16 with s·t ≤ 511 and (s·t·u)³ > (pr)⁴  (V > |G|^{4/3}).
4. index cap: V ≤ r²·|G| (normal abelian subgroup of index r).
5. threshold-split cap: (u·s·t)²·r ≤ 64·|G|³ (V ≤ 8|G|^{3/2}/√D, D=r).
6. border-count floor: B(p,r) = min s·t over (3)–(5).

## Minimal-candidate probe (r=16, p=17, λ=3 primitive root mod 17)

Z₀ = 16-subset of Z_17: 240 survivors per slice — dead on both ledgers
(< 256 (i,j)-pairs and < 4096 support entries). Z₀ = full field: 289/slice;
it passes (i)–(iv) literally (coverage 256/256, witness maps in
`CERT_17_16.json`), but the survivor bipartite graph is K₁₇,₁₇ on the 17
slice-1 elements (18 components), so the slot-wise criterion above forces
κ constant ⟹ ≤ 16 A-variables < 256 — the 17→16 pair-collision death.

**"Two slices: 480" was a hand-count error (ignored the mod-17 wrap
a+b ∈ [17,28] ≡ [0,11]).** Exact enumeration (`enum_17_16.py`) gives 960 for
two 16-subsets at K={0,8} and 792 for the 15-AP design; the budget window
[256,511] contains **6,474,090** two-slice designs at sizes 14–17 (max 489 at
(14,14) for K={0,k}). Details: `RESULTS_enum_17_16.json`, `POTENTIALS.md`.

## Verdict — lane closure (2026-11-07, commit c4f666b)

The exact enumeration and certificate skeleton close the Frobenius lane for
the M16 target:

1. **Gap 1 (design-independent, fatal).** The pinned target support has 4096
   entries; any certificate whose rank-1 terms each carry one monomial (the
   indicator / Frobenius-lane class) needs ≥ 4096 terms > the 511 budget.
   This kills the lane at every (p,r) in the r ≤ 16 window, not just (17,16).
2. **Gap 2 (literal passage, not liftable).** One design does pass conditions
   (i)–(iv) literally: K={k,2k} full kernels at (17,16), Z₀ = Z₁₇×{1} ∪
   Z₁₇×{2}, 289 survivors, coverage 256/256 (explicit α,β,γ). But its
   survivor graph's K₁₇,₁₇ component forces the slot-wise k-label constant —
   ≤ 16 A-variables < 256 (machine-checked, `verify_cert.py`).
3. **Residue = Gap 3.** Evading both requires general (non-indicator) rank-1
   polynomial terms, i.e. exactly the classical open problem
   ∂R(⟨16,16,16⟩) ≤ 511 (flattening lower bound 256, budget 511) — not a
   group-design search. Evidence: commit c4f666b, `CERT_17_16.json`,
   `CERT.md`, `RESULTS_enum_17_16.json`.
