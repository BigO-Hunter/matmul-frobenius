# POTENTIALS.md — Frobenius C_p ⋊ C_r window, exact screens vs M16 target

Method: `screens.py` (exact integer arithmetic; x > y^{4/3} ⟺ x³ > y⁴).
Window: r = 2..16, p prime ≡ 1 mod r, p < r⁴ (the open window r⁴ > p).
Verdict key: OPEN = passes all screens (lane not excluded); DIE-16idx =
16-index structure impossible; DIE-vol = volume/index/threshold caps exclude
any |S||T| ≤ 511 certificate.

## Headline

3919 candidates enumerated; 3770 OPEN, 149 DIE-16idx, 0 DIE-vol.
**Every OPEN candidate has B(p,r) = 256 — the trivial 16×16 floor.**
The size-level screens are slack across the entire window: no (p,r) in
r⁴ > p is excluded by volume, index, threshold-split, or the 511 border
budget. The lane is decided entirely by the Z₀-design (Lemma 1/2 in
FORMALIZATION.md), not by counting.

## Per-r table (r, #candidates, #OPEN, #die, min B, argmin p)

| r  | cands | OPEN | die | min B | argmin p | \|G\| at argmin | C_r junk-solution count (exact, every c) |
|----|-------|------|-----|-------|----------|------|-------|
| 2  | 5     | 0    | 5   | —     | —        | —    | 4     |
| 3  | 10    | 0    | 10  | —     | —        | —    | 9     |
| 4  | 24    | 0    | 24  | —     | —        | —    | 16    |
| 5  | 26    | 13   | 13  | 256   | 271      | 1355 | 25    |
| 6  | 101   | 76   | 25  | 256   | 271      | 1626 | 36    |
| 7  | 56    | 48   | 8   | 256   | 281      | 1967 | 49    |
| 8  | 133   | 123  | 10  | 256   | 257      | 2056 | 64    |
| 9  | 138   | 130  | 8   | 256   | 271      | 2439 | 81    |
| 10 | 306   | 293  | 13  | 256   | 271      | 2710 | 100   |
| 11 | 168   | 164  | 4   | 256   | 331      | 3641 | 121   |
| 12 | 572   | 561  | 11  | 256   | 277      | 3324 | 144   |
| 13 | 260   | 256  | 4   | 256   | 313      | 4069 | 169   |
| 14 | 667   | 659  | 8   | 256   | 281      | 3934 | 196   |
| 15 | 639   | 633  | 6   | 256   | 271      | 4065 | 225   |
| 16 | 834   | 814  | 20  | 256   | 17       | 272  | 256   |

C_r junk-solution count: #{(k₁,k₂,k₃) ∈ C_r³ : k₁+k₂ ≡ k₃+c} = r² exactly,
for every c (choose k₁,k₃ freely; k₂ determined). Lower bound r² > p^{1/2} in
the whole window; the swarm's r⁴ > p window is exactly where r³ > p^{3/4}.

## Representative OPEN candidates (p, r, exact B, verdict)

(17,16,B=256,OPEN) (257,8,B=256,OPEN) (257,16,B=256,OPEN) (271,5..10,B=256,OPEN)
(277,12,B=256,OPEN) (281,7,14,15,B=256,OPEN) (313,13,B=256,OPEN) (331,11,B=256,OPEN)
… all 3770 rows reproducible via `python3 screens.py` (full list on stdout).

Minimal candidate: **(p,r) = (17,16), |G| = 272, λ = 3 (ord 16 mod 17)** —
probed in FORMALIZATION.md §probe: single slice 240 < 256 (dead), two slices
480 ≤ 511 with the Z₀/cell-consistency design open.

## Negative map (what the screens do NOT decide)

- The screens certify only necessary conditions on SIZES. The binding object
  is the Z₀ zero-set design with per-slice fold-back counts (Lemma 1); after
  Lemma 2 no kernel-translation-invariant potential can reach 511 for p ≥ 257,
  so the search space is genuine 0/1 designs on Z_p (p ≥ 257) or mixed-slot
  designs at r = 16.
- Not decided here: (a) existence of any Z₀ realizing the composition support
  at ≤ 511 survivors for any candidate; (b) the r = 16 two-slice design at
  p = 17; (c) whether the swarm's historical CKSU §7.1 sets admit potentials
  our screens don't see (they are a subset of the Z₀ designs).

## Next construction step (single)

Solve the (17,16) two-slice design exactly: choose Z₀ (17- or 16-subset),
two slices k₁ ≠ k₂, projections α,β,γ (16 labels each), and verify in exact
arithmetic that the ≤ 480 surviving triples project onto exactly the 256-entry
composition support {(A_ik,B_kj,C_ij)}. Enumeration is finite and small:
2·17 subsets × C(16,2) slice pairs × label maps — a first SAT/ILP target
smaller than any SL2(5) instance. If it fails, the same enumerator scales to
(257,8) and (257,16).

## Exact enumeration at (17,16) — RESULTS (enum_17_16.py, 2026-11-07)

All numbers below are machine-checked (`RESULTS_enum_17_16.json`,
`verify_cert.py`; vectorized totals cross-checked against brute force on
random designs).

**Search space.** K-pairs: C(16,2) = 120; a code-checked structural theorem
shows 91 of them have NO possible survivor block (kg,kh,kg+kh ∈ K unsolvable
for |K|=2); the 29 contributing pairs are {0,k} (3–4 blocks) and {k,2k} (1
block). Slice contents: exhaustive over all 834 subsets of Z_17 of sizes
14–17 per slice ⇒ 834² × 29 = 20.2M two-slice designs counted exactly; sizes
≤ 13 covered by exact self-triple maxima (max 133 at |S|=13) plus 150k random
cross-pair samples.

**Probe re-check (exact).** single 16-subset slice Z∖{0}: 240 survivors ✓
(probe right, < 256 dead). Full-kernel single slice: 289 ✓. "Two 16-subsets,
K={0,8} = 480" ✗ — exact count is **960** (the probe undercounted; the 15-AP
K={0,8} design gives 792, not 480 — both hand counts ignored the mod-17 wrap
a+b ∈ [17,28] ≡ [0,11]).

**The budget window [256,511] is huge, not marginal: 6,474,090 in-window
designs** at sizes 14–17 (e.g. max 489 for (14,14) at K={0,k}). Global max
count 1156 (K={0,8}, full kernels).

**Condition (iv) is the whole game.** Coverage search over α,β label maps
(incremental hill-climb, 25 restarts): (a) (14,14)×K={0,k} designs stall at a
universal **252/256** ceiling — the 4 uncovered cells always form a 2×2
submatrix (two rows × two columns), stable across all 21 designs, all k, all
counts — an apparent ceiling, not yet a proof; (b) the **K={k,2k} full-kernel
design PASSES**: Z₀ = Z_17×{1} ∪ Z_17×{2}, 289 survivors, coverage **256/256**
with explicit witness maps (CERT_17_16.json / CERT.md / verify_cert.py).

**Verdict vs the pinned Lean bridge — the lane is closed.** The pinned target
`matrixCoefficients (Fin 16)³` (ComplexMatrixTensor.lean:17) has support
**16³ = 4096**, not 256: FORMALIZATION.md's "256-entry composition support"
undercounts by the free k-index. Any single-monomial-per-term (indicator)
certificate — everything this lane constructs — needs ≥ 4096 terms > 511.
Independently, the passing design's survivor graph is K_{17,17}, forcing
slot-wise k-labels constant ⇒ ≤ 16 A-variables: the formalization's own
17→16 pair-collision death, which its conditions (i)–(iv) fail to encode.
Both gaps are machine-confirmed; the certificate is not liftable. Beating
them requires general rank-1 polynomial terms = the open problem
border-rank(⟨16,16,16⟩) ≤ 511 (flattening ≥ 256), not a group-design search.

**(257,8) / (257,16).** λ checked: ord(3 mod 257) = 256 (primitive root);
3^32 = 64 has order 8 exactly. The passing (17,16) shape does not scale:
full-kernel blocks give 257² = 66049 ≫ 511. AP-slice scan: K={0,1} with two
16-element APs gives 323 ∈ [256,511] (in-window at (257,16)), s=20 gives 497;
but Gap 1 (4096 > 511) already closes the lane at every (p,r), so these are
not pursued. Small-slice self-triple maxima on Z_17: 1,3,7,12,19,27,37,48,
61,75,91,109,133 for |S| = 1..13.

Files: enum_17_16.py (enumerator), RESULTS_enum_17_16.json (raw results),
build_cert.py / CERT_17_16.json / verify_cert.py / CERT.md (certificate + gaps).
