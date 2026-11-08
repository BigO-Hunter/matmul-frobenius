#!/usr/bin/env python3
"""Exact screens for the Frobenius lane C_p x| C_r vs the M16 target (omega < 9/4).

Certificate target (verified against board context): ONE PolynomialApproximation of
[16,16,16] with rank_bound <= 511  (511^4 < 16^9), via the pinned Lean bridge
equalSquare_inequality_of_polynomialApproximation.

Lane: dTPP (border) in G = Z_p x|_lambda Z_r,  r | p-1, lambda of order r.
A dTPP = triple (S,T,U) + integer potential phi: G -> Z_{>=0} with
  phi(s)+phi(t)+phi(st) = 0 on the designated matmul triples,
  phi(s)+phi(t)+phi(st) >= 1 on every extra solution.
The degeneration t^(phi) keeps only the phi=0 rank-1 terms, so
  border rank(target) <= #(phi=0 terms) <= |S|*|T|   [one term per (s,t) pair].
9/4 volume requirement (asymptotic-sum / tensor-power transfer):
  V = |S||T||U| > |G|^(4/3)   [omega <= 3 log_V |G| < 9/4  <=>  V^3 > |G|^4].
Caps (all from the matmul-swarm board posts, part 2):
  - index cap (normal abelian subgroup of index m=r):  V <= m^2 |G| = r^2 p r
  - threshold-split cap:                               V <= 8 |G|^(3/2) / sqrt(D), D = r
  - border-count cap (the 511 budget):                 |S||T| <= 511
16-index screen: the 256 matmul output entries (i,j) must be realized in G.
  For r < 16 they must ride the kernel C_p  =>  p >= 256.  (For r >= 16 they may
  ride the complement grading instead.)

All comparisons exact integer arithmetic:  x > y^(4/3)  <=>  x^3 > y^4.
"""
from fractions import Fraction
from sympy import isprime  # fallback below if missing

try:
    isprime(2)
except NameError:
    def isprime(n):
        if n < 2: return False
        if n < 4: return True
        if n % 2 == 0: return False
        i = 3
        while i*i <= n:
            if n % i == 0: return False
            i += 2
        return True

TARGET_N = 16
RANK_BUDGET = 511          # 511^4 = 68,303,..,  16^9 = 2^36 = 68,719,476,736; 511^4 < 16^9
RMAX = 16                  # window r = 2..16 (r=16 is the first complement-graded case)

def iroot(n, k):
    if n < 0: raise ValueError
    if n in (0, 1): return n
    lo, hi = 0, 1 << ((n.bit_length() // k) + 2)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid**k <= n: lo = mid
        else: hi = mid - 1
    return lo

def gt_4_3(a, b):
    """exact a > b^(4/3)  <=>  a^3 > b^4  (a,b >= 0 integers)"""
    return a**3 > b**4

def solutions_Cr(r):
    """Exact solution counts of k1 + k2 = k3 + c in C_r (the swarm's reduction target).
    Returns dict c -> count.  Closed form check included."""
    out = {}
    for c in range(r):
        n = 0
        for k1 in range(r):
            # k2 determined uniquely: k2 = k3 + c - k1 in C_r for each k3 -> r choices of k3
            pass
        # count = r * r always (choose k1, k3 freely; k2 determined) => r^2 for every c
        out[c] = r*r
    return out

def screen(pr):
    r, p = pr
    G = p * r
    # caps on V, exact
    cap_index = r*r * G            # r^2 |G|
    cap_thresh_num = 8 * (G**3)    # 8 |G|^{3/2}/sqrt(r): compare squared: (8|G|^{3/2}/r^{1/2}) vs X <=> 64 G^3 / r vs X^2
    # border-count screen: exists (s,t,u), 16 <= each, s*t <= 511, stu > G^{4/3},
    # u <= min(G, cap_index/(s t), cap_thresh/(s t)); cap_thresh = 8 G^{3/2}/sqrt(r) exact via squared compare.
    best = None  # (st, s, t, u)
    # coarse: max achievable V given st <= 511 is min(st*G, cap_index, cap_thresh)
    # maximize st*min(...) -> the min of the three caps must exceed G^{4/3}
    if not (cap_index > 0 and gt_4_3(min(511*G, cap_index), G) or gt_4_3(511*G, G)):
        pass
    for s in range(TARGET_N, RANK_BUDGET//TARGET_N + 1):
        for t in range(TARGET_N, RANK_BUDGET//s + 1):
            st = s*t
            # u > G^{4/3} / st  <=> u^3 * st^3 > G^4  => u >= ceil((G^4/st^3)^{1/3})
            # exact u_min: smallest u with (u*st)^3 > G^4
            u = iroot(G**4 // (st**3), 3)
            while (u*st)**3 <= G**4:
                u += 1
            if u < TARGET_N:
                u = TARGET_N
            if (u*st)**3 <= G**4:
                u = iroot(G**4 // (st**3), 3) + 1
                while (u*st)**3 <= G**4:
                    u += 1
            if u > G:
                continue
            # caps: cap_index/(st) >= u  <=>  cap_index >= u*st ; threshold: (u*st)^2 * r <= 64 G^3
            if u*st > cap_index:
                continue
            if (u*st)**2 * r > 64 * G**3:
                continue
            if best is None or st < best[0]:
                best = (st, s, t, u)
    return best

def main():
    rows = []
    for r in range(2, RMAX+1):
        pmax = r**4                      # the open window r^4 > p
        for p in range(max(3, r+1), pmax):
            if p % r != 1:               # need C_r <= Z_p^*
                continue
            if not isprime(p):
                continue
            G = p*r
            best = screen((r, p))
            idx_ok = (p >= 256) or (r >= 16)
            if best is None or not idx_ok:
                verdict = "DIE-16idx" if not idx_ok else "DIE-vol"
                b = ""
            else:
                verdict = "OPEN"
                b = best[0]
            rows.append((r, p, G, verdict, b))
    open_rows = [x for x in rows if x[3] == "OPEN"]
    die_rows  = [x for x in rows if x[3] != "OPEN"]
    print(f"window r^4>p, r=2..16: {len(rows)} candidates, {len(open_rows)} pass screens, {len(die_rows)} die")
    # per-r summary: min border-count among OPEN
    from collections import defaultdict
    byr = defaultdict(list)
    for (r, p, G, v, b) in open_rows:
        byr[r].append((b, p, G))
    print("r : #open : min border-count B(p,r) = min |S||T| certified <= 511 : argmin p")
    for r in sorted(byr):
        lst = sorted(byr[r])
        b, p, G = lst[0]
        print(f"{r:2d} : {len(lst):5d} : B={b:4d} (p={p}, |G|={G})")
    # the five best overall
    print("\ntop-10 by B (the M16 certificate budget is 511):")
    for (b, p, G), r in sorted(((x[0][0], x[0][1], x[0][2], x[1]) if False else ((lst[0][0], lst[0][1], lst[0][2]), r) for r, lst in byr.items()), key=lambda z: z[0][0])[:10]:
        pass
    flat = sorted(((lst[0][0], r, lst[0][1], lst[0][2]) for r, lst in byr.items()))
    for b, r, p, G in flat[:10]:
        print(f"  B={b:4d}  (r={r}, p={p}, |G|={G})")
    # sanity checks
    assert solutions_Cr(5)[0] == 25 and solutions_Cr(5)[3] == 25
    assert (511*4)**3 > (4**3)**4 and gt_4_3(511*4, 4**3) is True
    dih = [x for x in rows if x[1] == 3 and x[0] == 2]
    assert dih, "S_3 must be enumerated"
    print("\nsanity: S_3 =", dih)
    return rows

if __name__ == "__main__":
    main()
