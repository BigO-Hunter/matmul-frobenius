#!/usr/bin/env python3
"""Decisive finite enumeration of Z0-designs at (p,r,lam)=(17,16,3) for the M16
border certificate (FORMALIZATION.md conditions (i)-(iv)). Exact integers.

G = Z_17 x|_3 Z_16, (a,k)(b,l) = (a + 3^k b, k+l).
Design: Z0 = (S1 x {k1}) U (S2 x {k2}). Survivor block (kg,kh) iff kg,kh,(kg+kh)%16 in K;
block count N(A,B,C; mu) = #{(a,b) in A x B : a + lam^kg * b in C}  (all mod 17).
"""
import itertools, json, random
import numpy as np

P, LAM, R, BUDGET, TARGET_SUPPORT = 17, 3, 16, 511, 16 ** 3
assert pow(LAM, 8, P) == P - 1 and pow(LAM, 16, P) == 1
assert all(pow(LAM, d, P) != 1 for d in range(1, 16)), "ord(3) mod 17 = 16 required"
LAMPOW = [pow(LAM, k, P) for k in range(R)]
OUT = "/Volumes/Substrate-1/bigo/matmul-frobenius/RESULTS_enum_17_16.json"

# ---------- structural theorem over the C(16,2)=120 K-pairs (checked) ----------
KPAIRS = list(itertools.combinations(range(R), 2))
contributing, zero_pairs = {}, []
for K in KPAIRS:
    bl = [(kg, kh, (kg + kh) % R) for kg in K for kh in K if (kg + kh) % R in K]
    (contributing.__setitem__(K, bl) if bl else zero_pairs.append(K))
expect_zero = [K for K in KPAIRS
               if not (0 in K or (2 * K[0]) % R == K[1] or (2 * K[1]) % R == K[0])]
assert set(zero_pairs) == set(expect_zero), "K-pair zero-block theorem violated"
print(f"K-pairs: {len(KPAIRS)} total | {len(contributing)} can contribute | {len(zero_pairs)} provably zero", flush=True)

# ---------- subset universe: exhaustive sizes 14..17 ----------
SUBS = [frozenset(c) for m in (14, 15, 16, 17) for c in itertools.combinations(range(P), m)]
NS = len(SUBS)
B = np.zeros((NS, P), dtype=np.int64)
for i, s in enumerate(SUBS):
    for a in s:
        B[i, a] = 1
sizes = B.sum(1)

TP = np.zeros((R, NS, P), dtype=np.int64)   # TP[mu][j][a] = #{(b,u) in S_j^2 : u-mu*b=a}
for mu in range(R):
    m = LAMPOW[mu]
    for j, s in enumerate(SUBS):
        row = np.zeros(P, dtype=np.int64)
        for b in s:
            for u in s:
                row[(u - m * b) % P] += 1
        TP[mu, j] = row
X = np.stack([B @ TP[mu].T for mu in range(R)])                                   # N(S_A,S_B,S_B)
Y = np.stack([TP[0][:, (LAMPOW[mu] * np.arange(P)) % P] @ B.T for mu in range(R)])  # N(S_A,S_B,S_A)
Z = X.transpose(0, 2, 1)  # placeholder; real Z built below via pair histograms
H = np.zeros((R, NS, P), dtype=np.int64)    # H[mu][j][v] = #{(a,b) in S_j^2 : a+mu*b=v}
for mu in range(R):
    m = LAMPOW[mu]
    for j, s in enumerate(SUBS):
        row = np.zeros(P, dtype=np.int64)
        for a in s:
            for b in s:
                row[(a + m * b) % P] += 1
        H[mu, j] = row
Z = np.stack([H[mu] @ B.T for mu in range(R)])                                    # N(S_A,S_A,S_B)
DIAG = np.stack([np.diagonal(X[mu]).copy() for mu in range(R)])
print(f"universe: {NS} subsets (sizes 14..17); count tables built", flush=True)

def totals(K):
    k1, k2 = K
    s = lambda k: 0 if k == k1 else 1
    tot = np.zeros((NS, NS), dtype=np.int64)
    for (kg, kh, ks) in contributing[K]:
        f, si, t = s(kg), s(kh), s(ks)
        if f == 0 and si == 0 and t == 0:   tot += DIAG[kg][:, None]
        elif f == 1 and si == 1 and t == 1: tot += DIAG[kg][None, :]
        elif f == 0 and si == 1 and t == 1: tot += X[kg]
        elif f == 1 and si == 0 and t == 0: tot += X[kg].T
        elif f == 0 and si == 0 and t == 1: tot += Z[kg]
        elif f == 1 and si == 1 and t == 0: tot += Z[kg].T
        elif f == 0 and si == 1 and t == 0: tot += Y[kg]
        elif f == 1 and si == 0 and t == 1: tot += Y[kg].T
    return tot

def brute_triples(S1, S2, K):
    out = []
    for (kg, kh, ks) in contributing[K]:
        A = S1 if kg == K[0] else S2
        Bb = S1 if kh == K[0] else S2
        C = S1 if ks == K[0] else S2
        m = LAMPOW[kg]
        for a in A:
            for b in Bb:
                if (a + m * b) % P in C:
                    out.append(((a, kg), (b, kh), ((a + m * b) % P, ks)))
    return out

# ---------- window enumeration ----------
window_hist = {}          # K -> {count: n_pairs}
per_k_max, samples = {}, {}
rng = random.Random(7)
checkfail = 0
for K in contributing:
    T = totals(K)
    for _ in range(6):    # spot-check vs brute
        i, j = rng.randrange(NS), rng.randrange(NS)
        bt = len(brute_triples(SUBS[i], SUBS[j], K))
        if bt != int(T[i, j]): checkfail += 1
    per_k_max[K] = int(T.max())
    vals, cnts = np.unique(T[(T >= 256) & (T <= BUDGET)], return_counts=True)
    window_hist[K] = {int(v): int(c) for v, c in zip(vals, cnts)}
    # diverse in-window sample: argmax per size combo + randoms
    ii, jj = np.where((T >= 256) & (T <= BUDGET))
    if len(ii):
        ss = {int(sizes[i]) * 100 + int(sizes[j]): (int(T[i, j]), int(i), int(j))
              for i, j in zip(ii.tolist(), jj.tolist())}
        best_per_combo = {}
        for (i, j) in zip(ii.tolist(), jj.tolist()):
            key = (int(sizes[i]), int(sizes[j]))
            v = int(T[i, j])
            if key not in best_per_combo or v > best_per_combo[key][0]:
                best_per_combo[key] = (v, i, j)
        rnd = rng.sample(range(len(ii)), min(5, len(ii)))
        cand = list(best_per_combo.values()) + [(int(T[ii[p], jj[p]]), int(ii[p]), int(jj[p])) for p in rnd]
        samples[K] = sorted(cand, key=lambda x: -x[0])
assert checkfail == 0, "vectorized/brute mismatch"
total_window = sum(sum(h.values()) for h in window_hist.values())
allmax = max(per_k_max.values())
print(f"window designs in [256,511]: {total_window}; global max count {allmax}", flush=True)
print("per-K max:", {str(K): v for K, v in sorted(per_k_max.items(), key=lambda x: -x[1])[:8]}, flush=True)

# ---------- coverage search on the best sampled designs ----------
Z0el = lambda i, j, K: [(a, K[0]) for a in SUBS[i]] + [(a, K[1]) for a in SUBS[j]]
def coverage_search(K, i, j, restarts=25, sweeps=40, seed=1):
    triples = brute_triples(SUBS[i], SUBS[j], K)
    els = Z0el(i, j, K)
    idx = {e: t for t, e in enumerate(els)}
    E = [(idx[g], idx[h]) for (g, h, c) in triples]
    tE_a = [[] for _ in els]   # alpha-side incidence: edges (t, v)
    tE_b = [[] for _ in els]   # beta-side incidence: edges (u, t)
    for (u, v) in E:
        tE_a[u].append((u, v)); tE_b[v].append((u, v))
    rng = random.Random(seed)
    best_cov, best_map = 0, None
    for r in range(restarts):
        al = [rng.randrange(16) for _ in els]
        be = [rng.randrange(16) for _ in els]
        C = np.zeros((16, 16), dtype=np.int32)
        for (u, v) in E:
            C[al[u], be[v]] += 1
        cov = int((C > 0).sum())
        def shift(tE, arr, t, val):
            """flip arr[t] cur->val incrementally; return coverage delta"""
            cur = arr[t]
            delta = 0
            for (u, v) in tE:
                cell = (cur, be[v]) if arr is al else (al[u], cur)
                if C[cell] == 1: delta -= 1
                C[cell] -= 1
            arr[t] = val
            for (u, v) in tE:
                cell = (val, be[v]) if arr is al else (al[u], val)
                if C[cell] == 0: delta += 1
                C[cell] += 1
            return delta
        for _ in range(sweeps):
            if cov == 256: break
            improved = False
            for t in range(len(els)):
                for tE, arr in ((tE_a[t], al), (tE_b[t], be)):
                    cur = arr[t]
                    for val in range(16):
                        if val == cur: continue
                        d = shift(tE, arr, t, val)
                        if d > 0:
                            cov += d; cur = val; improved = True
                        else:   # rollback
                            d2 = shift(tE, arr, t, cur)
                            assert d + d2 == 0
            if not improved: break
        if cov > best_cov:
            best_cov, best_map = cov, (list(al), list(be))
        if best_cov == 256: break
    # uncovered cells of the best map
    unco = None
    if best_map:
        al, be = best_map
        Cb = np.zeros((16, 16), dtype=np.int32)
        for (u, v) in E:
            Cb[al[u], be[v]] += 1
        unco = [[int(x), int(y)] for x, y in zip(*np.where(Cb == 0))]
    return best_cov, best_map, len(E), unco

def components(K, i, j):   # bipartite survivor-graph connectivity (k-consistency obstruction)
    triples = brute_triples(SUBS[i], SUBS[j], K)
    els = Z0el(i, j, K)
    idx = {e: t for t, e in enumerate(els)}
    parent = list(range(len(els)))
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    ncomp = len(els)
    for (g, h, c) in triples:
        u, v = idx[g], idx[h]
        ru, rv = find(u), find(v)
        if ru != rv: parent[ru] = rv; ncomp -= 1
    return ncomp

results_cov = []
uncovered_best = None
tried = 0
KSEARCH = [K for K in ((0, 1), (0, 4), (0, 8), (0, 13), (1, 2)) if K in samples]
for K in KSEARCH:
    for (t, i, j) in samples[K]:
        cov, mp, ne, unco = coverage_search(K, i, j)
        nc = components(K, i, j)
        results_cov.append({"K": list(K), "count": t, "sizes": [int(sizes[i]), int(sizes[j])],
                            "coverage": cov, "survivors": ne, "components": nc,
                            "uncovered": unco,
                            "alpha": mp[0] if mp else None, "beta": mp[1] if mp else None})
        tried += 1
        print(f"  cov-search K={K} count={t} sizes=({sizes[i]},{sizes[j]}): "
              f"coverage={cov}/256 comps={nc} uncovered={unco}", flush=True)
        if cov == 256: break
    if any(r["coverage"] == 256 for r in results_cov): break
best = max(results_cov, key=lambda r: r["coverage"])

# ---------- probe re-checks ----------
def one_slice(S, k=0):
    m = LAMPOW[k]
    return sum(1 for a in S for b in S if (a + m * b) % P in S)
probe = {"single_slice_Z17_minus_0": one_slice(frozenset(range(1, P))),
         "single_slice_full_kernel": one_slice(frozenset(range(P))),
         "two_16subsets_K08": len(brute_triples(frozenset(range(1, P)), frozenset(range(1, P)), (0, 8))),
         "two_15AP_K08": len(brute_triples(frozenset(range(15)), frozenset(range(15)), (0, 8)))}

# ---------- small slices + (257) ----------
small_t = {m: max(one_slice(frozenset(c)) for c in itertools.combinations(range(P), m))
           for m in range(1, 14)}
p2 = 257
ord3 = next(d for d in range(1, 257) if pow(3, d, p2) == 1)
lam8 = pow(3, 32, p2)
ordl8 = next(d for d in range(1, 9) if pow(lam8, d, p2) == 1)
ap_tab = {}
for s in (16, 20, 23, 26, 30):
    A = range(s)
    single = sum(1 for a in A for b in A if (a + b) % p2 < s)
    K01 = (sum(1 for a in A for b in A if (a + b) % p2 < s)
           + sum(1 for a in A for b in A if (a + b) % p2 < s)
           + sum(1 for a in A for b in A if (a + 3 * b) % p2 < s))
    ap_tab[s] = {"single_mu1": single, "K01_r16_lam3": K01}

out = {
    "lambda_checks": {"ord_3_mod_17": 16, "ord_3_mod_257": ord3, "lam_for_r8": int(lam8), "ord_lam_r8": ordl8},
    "kpair_theorem": {"total": len(KPAIRS), "contributing": len(contributing), "zero_pairs": len(zero_pairs),
                      "blocks": {str(list(K)): bl for K, bl in contributing.items()}},
    "universe": {"sizes": [14, 15, 16, 17], "n_subsets": NS, "pair_checks": NS * NS * len(contributing)},
    "per_k_max": {str(list(K)): v for K, v in per_k_max.items()},
    "window_total": total_window, "window_global_max": allmax,
    "window_hist_top": {str(list(K)): dict(sorted(h.items(), key=lambda x: -x[0])[:8])
                        for K, h in sorted(window_hist.items(),
                                           key=lambda x: -(max(x[1]) if x[1] else 0))[:10]
                        if h},
    "probe_recheck": probe,
    "coverage_search": results_cov,
    "best_design": best,
    "small_slice_self_triple_max": small_t,
    "ap_257": {str(s): v for s, v in ap_tab.items()},
}
with open(OUT, "w") as f:
    json.dump(out, f, indent=1)
print("\nprobe re-check:", probe)
print("small-slice self-triple maxima:", small_t)
print(f"(257): ord(3)={ord3}; lam(r=8)=3^32={lam8} ord={ordl8}")
print("AP-slice counts on Z_257:", ap_tab)
print(f"BEST coverage: {best['coverage']}/256 on K={best['K']} count={best['count']}")
print("DONE")
