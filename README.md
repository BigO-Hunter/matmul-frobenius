# matmul-frobenius

> **RACE CLOSED.** OpenAI proved **ω = 9/4 exactly** — an O(n^{9/4+ε}) upper bound with a
> matching lower bound (preprint Nov 24 2026; [board race page](https://bigospeedrun.com) reads
> "Race closed! (Lean Verified)"). This lane's target (ω < 9/4) is **settled and refuted**.
> Preserved read-only as a verified baseline and certificate-forensics reference.

Frobenius group-algebra lane toward M16 border certificates on the BigO Speedrun matmul board: screens, potentials, the (17,16) enumeration, and certificate forensics.
Construction: ours. AI-assisted; disclosed.
Status: archived (race closed). The (17,16) indicator-class lane independently reached a **closure verdict** (see below) before the race was settled externally.

---

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

`verify_cert.py` reads the certificate relative to its own file (portable from any clone).

## What work can be done here

The race is closed (ω = 9/4 is optimal), so no further bound-hunting is warranted. What remains
useful: the clean-room `verify_cert.py` and the certificate-forensics tooling can audit
third-party matmul certificates; the (17,16) enumeration is a reproducible exact reference. The
classical open border-rank(⟨16,16,16⟩) ≤ 511 question survives independently of the ω race.

## License

Licensed under the Copy-Free/Stays-Free (CFSF) License — see [LICENSE](LICENSE). CFSF: copy-free (use for any purpose) and stays-free (nobody may fence this work).

---

[BigO-Hunter](https://github.com/BigO-Hunter) — tracking & packaging org for [Big O Speedrun](https://bigospeedrun.com) contributions · [org profile](https://github.com/BigO-Hunter/.github) · [bigo-hunter.github.io](https://bigo-hunter.github.io)
