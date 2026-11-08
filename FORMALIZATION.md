# Formalization: Frobenius lane vs the M16 border certificate

## Target (fixed by the pinned Lean bridge)

One `PolynomialApproximation` of `[16,16,16]` with `rank_bound r ≤ 511`
(511⁴ < 16⁹ = 2³⁶), via `equalSquare_inequality_of_polynomialApproximation`
(Rectangular/ASI.lean, openai/math pinned commit). The polynomial field is a
`Tensor (Polynomial F) 16 16 16`; `rank_bound` counts rank-one *polynomial*
terms whose t→0 limit reproduces ⟨16,16,16⟩ (the 256-entry composition support
`{(A_ik, B_kj, C_ij)}` in 16×16×16 format).

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
    256-entry composition support of ⟨16,16,16⟩ exactly.

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

Z₀ = 16-subset of Z_17: survivors per slice = 240 (< 256 needed) — single
slice dead. Z₀ = full field: 289/slice, but 17→16 index collapse forces γ
constant (pair-collision argument) — dead. **Two slices: 480 survivors ≤ 511,
≥ 256 entries: the design question is open and exactly posed.** This is the
first construction step.
