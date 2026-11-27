# matmul-frobenius

Frobenius group-algebra lane toward M16 border certificates (ω < 9/4) on the BigO Speedrun matmul board: screens, potentials, the (17,16) enumeration, and certificate forensics.
Construction: ours. AI-assisted (darkhipo swarm), disclosed.
Status: research shelf — screens and enumeration; forensics tooling for third-party certificates. The (17,16) indicator-class lane has a recorded **closure verdict** (see below).

---

## Why this repo is up

Private research shelf: the screens, potentials and (17,16) enumeration toward M16 border certificates, plus forensics tooling for third-party certificates — working material for the matmul board.

[BigO-Hunter](https://github.com/BigO-Hunter) is the darkhipo swarm's tracking & packaging org for contributions toward [Big O Speedrun](https://bigospeedrun.com) — a companion, never the project. Org story: [profile](https://github.com/BigO-Hunter/.github) · [bigo-hunter.github.io](https://bigo-hunter.github.io).

## What's in it

| Path | Content |
|---|---|
| `screens.py` | exact screens for the Frobenius lane C_p ⋊ C_r vs the M16 target (ω < 9/4; rank ≤ 511 for ⟨16,16,16⟩) |
| `POTENTIALS.md` | potential-function analysis |
| `enum_17_16.py` + `RESULTS_enum_17_16.json` | decisive exact (17,16) Z₀-design enumeration (6.47M-design window; K={k,2k} full-kernel designs pass literal conditions (i)–(iv); 289 survivors; 256/256 coverage) |
| `build_cert.py` + `CERT_17_16.json` + `CERT.md` | certificate skeleton for the passing design + the gap analysis |
| `verify_cert.py` | clean-room verifier: re-derives every stored claim from (p, r, λ, Z₀, α, β, γ) alone |
| `FORMALIZATION.md` | the Lean-facing design criteria and their corrections |

## Lane closure verdict (CERT.md)

The (17,16) design **passes FORMALIZATION.md conditions (i)–(iv) literally** (machine-checked) but **does not lift to the pinned Lean bridge** — three confirmed gaps: (1) pullback ≠ target (support count corrected 256→4096); (2) k-consistency: the K₁₇,₁₇ survivor component forces slot-wise κ constant ⇒ ≤16 A-variables < 256; (3) evading both needs general (non-indicator) rank-1 terms — exactly the open border-rank(⟨16,16,16⟩) ≤ 511 problem. Conclusion: the lane's indicator-class constructions are closed off at every (p,r) in the r ≤ 16 window; further progress is the classical open problem, not a group-design search.

## Reproduction

```sh
python3 verify_cert.py     # clean-room re-derivation of CERT_17_16.json — ALL CHECKS PASS
python3 enum_17_16.py      # full (17,16) enumeration (exact integers; regenerates RESULTS_enum_17_16.json)
python3 build_cert.py      # rebuild CERT_17_16.json from the enumeration results
```

`verify_cert.py` reads the certificate relative to its own file (portable from any clone; fixed 2026-11-26, was a machine-local absolute path).

## Branch map

Single branch: `main` (renamed from `enum-17-16`, 2026-11-26, E5 normalization — same commits; the enumeration lane's name is preserved in `RESULTS_enum_17_16.json` / `CERT_17_16.json`).

## What work can be done here

Open work: M16 border certificate construction from the (17,16) enumeration; an ω < 9/4 landing; certificate forensics for third-party submissions continues.

## License

Licensed under the Copy-Free/Stays-Free (CFSF) License — see [LICENSE](LICENSE). CFSF: copy-free (use for any purpose) and stays-free (nobody may fence this work). The name is unclaimed in software licensing (checked 2026-11-09) and is deliberately not "Copyfree" — the Copyfree Initiative's certification mark — since CFSF's anti-enclosure condition is excluded by their standard. 
