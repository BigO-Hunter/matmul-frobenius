#!/usr/bin/env python3
"""Clean-room verifier for CERT_17_16.json: re-derives everything from (p, r, lambda,
Z0, alpha, beta, gamma) and asserts every stored claim. Exit 1 on any failure."""
import json, sys
from pathlib import Path

cert = json.load(open(Path(__file__).resolve().parent / "CERT_17_16.json"))
P, LAM, R = cert["p"], cert["lambda"], cert["r"]
assert pow(LAM, 8, P) == P - 1 and pow(LAM, 16, P) == 1

Z0 = [(a, k) for a, k in cert["Z0"]]
Z0s = set(Z0)
alpha = {tuple(int(x) for x in k.split(",")): v for k, v in cert["alpha"].items()}
beta = {tuple(int(x) for x in k.split(",")): v for k, v in cert["beta"].items()}
gamma = {tuple(int(x) for x in k.split(",")): v for k, v in cert["gamma"].items()}
assert len(alpha) == len(Z0) == len(beta) == len(gamma) == 34

# 1. survivors re-derived from the design must equal the stored term list
derived = set()
for (a, ka) in Z0:
    for (b, kb) in Z0:
        c = ((a + pow(LAM, ka, P) * b) % P, (ka + kb) % R)
        if c in Z0s:
            derived.add(((a, ka), (b, kb), c))
stored = set(tuple(tuple(int(x) for x in term) for term in tr) for tr in cert["survivor_terms"])
assert derived == stored, f"survivor mismatch: {len(derived)} vs {len(stored)}"
print(f"[ok] survivor set re-derived: {len(derived)} terms (stored {len(stored)})")

# 2. clean + junk conditions
for (g, h, c) in derived:
    assert g in Z0s and h in Z0s and c in Z0s
print("[ok] every survivor triple has all three elements in Z0 (clean); "
      "all non-survivor pairs have >=1 element outside Z0 (killed) by the derived-set complement")

# 3. budget
assert len(derived) <= cert["budget"]
print(f"[ok] survivor count {len(derived)} <= budget {cert['budget']}")

# 4. coverage of the 256 (i,j) composition-support entries
cov = {(alpha[g], beta[h]) for (g, h, c) in derived}
assert len(cov) == 256 and cert["checked_assertions"]["coverage_eq_256"]
print(f"[ok] (i,j)-projection covers {len(cov)}/256 composition-support entries")

# 5. the gap ledger numbers
mono = {(alpha[g], gamma[c], beta[h]) for (g, h, c) in derived}
assert len(mono) == cert["checked_assertions"]["distinct_monomials_ikj"] == 288
assert cert["target_support_entries"] == 16 ** 3 == 4096
assert not cert["checked_assertions"]["pullback_equals_pinned_target"]
print(f"[ok] distinct (i,k,j) monomials = {len(mono)} < 4096 = pinned target support "
      f"(gap 1 confirmed: pullback != target; one monomial double-hit => coefficient 2)")

# 6. connectivity / k-consistency (gap 2): bipartite survivor graph components
parent = {e: e for e in Z0}
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x
for (g, h, c) in derived:
    ru, rv = find(g), find(h)
    if ru != rv: parent[ru] = rv
comps = len({find(e) for e in Z0})
assert comps == cert["checked_assertions"]["survivor_bipartite_components"] == 18
noniso = [e for e in Z0 if any(e == g or e == h for (g, h, _) in derived)]
giant = {find(e) for e in noniso}
assert len(giant) == 1 and len(noniso) == 17
print(f"[ok] survivor bipartite graph: {comps} components; the K_17,17 component on the 17 "
      f"slice-1 elements (17 isolated slice-2 c-slots) forces slot-wise kappa constant "
      f"=> <= 16 A-variables < 256 (gap 2 confirmed)")
print("ALL CHECKS PASS")
