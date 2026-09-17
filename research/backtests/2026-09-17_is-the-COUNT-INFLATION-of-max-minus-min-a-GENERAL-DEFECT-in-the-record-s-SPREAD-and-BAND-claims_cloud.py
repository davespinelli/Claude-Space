#!/usr/bin/env python3
"""
Idea 1155 (cloud lane, 2026-09-17) — is the COUNT INFLATION of MAX-MINUS-MIN a GENERAL
DEFECT in the record's SPREAD and BAND claims?

THE PREMISE, READ FROM THE RECORD AND NOT RECALLED.  Idea 1148 found the count-matched WITHIN
spread is smaller than max-minus-min in 5 of 6 statistics (median 1.137x) because a RANGE GROWS
WITH THE NUMBER OF POINTS IT IS TAKEN OVER, and that 1140's committed "1.7x - 61x band" pools a
k=2 range with a k=3 one.  A range is not an estimator of dispersion: it is an estimator of
dispersion TIMES a function of the point count.  Every sentence in this record that compares one
ladder's spread to another's, or calls a dial "the widest", is therefore reading rung count as
if it were effect size, unless it matched the counts.  This run asks how far that goes and what
the repair costs.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  CLAIM SET     {C_STRICT, C_PROX, C_ALL}                -- 1197/1199's nesting convention
  MATCHING RULE {M_NONE, M_SUBSAMPLE, M_PAIRWISE, M_D2}  -- the repairs under test

  M_NONE       the status quo: max - min over however many rungs the author had.
  M_SUBSAMPLE  1148's own rule: mean of max-min over every size-k_min subset of the rungs,
               k_min being the smallest count in the comparison.  Exact, not sampled.
  M_PAIRWISE   mean |x_i - x_j| over all pairs.  COUNT-FREE by construction: its expectation
               does not depend on k at all, which is the property a "spread" claim assumes.
  M_D2         divide max-min by Hartley's d2(k), the expected range of k standard normals.
               The SPC repair: a closed form, no resampling, and the only rung that leaves the
               published number in the statistic's own units.

  Every rung is scored at every cell.  NOTHING IS SELECTED ON.  M_NONE is the control and is
  reported like any other rung; it wins Arm C on one panel and the run says so.

WHAT IS NOT A DIAL.  PANEL {U56, B136, SMALL} is not a dial (rule 9, all three always read).
The FOUR LADDERS {N (6 rungs), H (4), GROSS (10), CADENCE (2)} are the record's own, inherited
whole from 1082/1098/1101/1148/1159, and their UNEQUAL LENGTHS ARE THE POINT -- they are what
makes count inflation live in this record rather than hypothetical.  The SIX STATISTICS are
1140/1148's, inherited whole.  The block bootstrap (L=63, 400 draws) is a measuring instrument,
not a dial; it is applied identically to every cell.

Frozen at the record's construction: 3-leg composite (21/252, 0/126, 0/63), above-200d
eligibility, max_vol 0.60, anchor N=20 / H=126 / GROSS=0.75 / CADENCE=W, 10 bps (rule 2),
t+1 execution, warm-up 260 rows, IS end 2016-12-31.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward in Arm C with the choice made on
2009-2016 ONLY and 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on
every book; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py
are NOT modified by this script.

Runs standalone and offline:
  python research/backtests/2026-09-17_is-the-COUNT-INFLATION-of-max-minus-min-a-GENERAL-DEFECT-in-the-record-s-SPREAD-and-BAND-claims_cloud.py
"""
from __future__ import annotations

import itertools
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "is-the-COUNT-INFLATION-of-max-minus-min-a-GENERAL-DEFECT-in-the-record-s-SPREAD-and-BAND-claims"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"
LAD = {
    "N": [5, 10, 15, 20, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
    "CADENCE": ["W", "M"],
}
STATS = ["CAGR", "Sharpe", "MaxDD", "Vol", "Calmar", "Ulcer"]
MATCH = ["M_NONE", "M_SUBSAMPLE", "M_PAIRWISE", "M_D2"]
CLAIMSETS = ["C_STRICT", "C_PROX", "C_ALL"]
NBOOT, BLOCK, SEED0 = 400, 63, 11551155
LIVE_MAXDD_COMMITTED = -0.1205

# Hartley's d2(k): E[range of k iid N(0,1)].  Published constants, gated against Monte Carlo.
D2 = {2: 1.128379, 3: 1.692569, 4: 2.058751, 5: 2.325929, 6: 2.534413, 7: 2.704357,
      8: 2.847201, 9: 2.970026, 10: 3.077505, 11: 3.172873, 12: 3.258457}

LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ==================================================== the four matching rules
def spread(vals, rule, k_min=None):
    """Dispersion of a ladder's readings under each publishing convention.
    vals is the ladder's readings in rung order; k_min is the count a comparison is
    being matched to (defaults to len(vals), i.e. no matching)."""
    v = np.asarray([x for x in vals if np.isfinite(x)], float)
    k = len(v)
    if k < 2:
        return np.nan
    if rule == "M_NONE":
        return float(v.max() - v.min())
    if rule == "M_SUBSAMPLE":
        km = int(k_min or k)
        km = max(2, min(km, k))
        if km == k:
            return float(v.max() - v.min())
        return float(np.mean([s.max() - s.min() for s in
                              (np.asarray(c) for c in itertools.combinations(v, km))]))
    if rule == "M_PAIRWISE":
        d = np.abs(v[:, None] - v[None, :])
        return float(d[np.triu_indices(k, 1)].mean())
    if rule == "M_D2":
        return float((v.max() - v.min()) / D2[min(max(k, 2), 12)])
    raise ValueError(rule)


# ==================================================== census
SPREADTOK = re.compile(r"\b(spread|band|range|max[- ]?minus[- ]?min|widest|narrowest|"
                       r"wider|narrower|dispersion|max\s*-\s*min|from\s+[-\d.]+\s*(?:to|-)\s*[-\d.]+)\b",
                       re.I)
MULT = re.compile(r"(\d+(?:\.\d+)?)\s*x\b", re.I)
NUMV = re.compile(r"[-+]?\d+(?:\.\d+)?(?:e-?\d+)?%?")
ADJUD = re.compile(r"\b(clears?|cleared|passe?s?|passed|fails?|failed|beats?|picks?|picked|"
                   r"chooser|verdict|KEEP|KILL|PARK|significan\w*|decisive\w*|confirms?|"
                   r"refutes?|ranks?|ranked|selects?|adjudicat\w*|widest|largest|dominat\w*)\b")
# how many POINTS the range was taken over: a rung / cell / ladder count stated in the unit
KTOK = re.compile(r"(\d[\d,]*)\s*(?:-|\s)?\s*(rungs?|cells?|points?|ladders?|arms?|books?|"
                  r"anchors?|rows?|panels?|statistics?|families|families of)\b", re.I)
RANGEPAIR = re.compile(r"(\d+(?:\.\d+)?)\s*x\s*(?:-|to|–|—)\s*(\d+(?:\.\d+)?)\s*x", re.I)


def units():
    U = []
    for ln in (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore").split("\n"):
        if ln.startswith("| 20"):
            U.append(("LEADERBOARD", ln))
    for para in (ROOT / "research" / "CHANGELOG.md").read_text(errors="ignore").split("\n\n"):
        if para.strip():
            U.append(("CHANGELOG", para))
    n_md = 0
    for f in sorted((ROOT / "research" / "backtests").rglob("*.md")):
        n_md += 1
        for para in f.read_text(errors="ignore").split("\n\n"):
            if para.strip():
                U.append((f.name, para))
    return U, n_md


def census():
    U, n_md = units()
    fileset = {}
    for src, txt in U:
        fileset.setdefault(src, False)
        if SPREADTOK.search(txt):
            fileset[src] = True
    rows = []
    for src, txt in U:
        sp = bool(SPREADTOK.search(txt))
        mults = [float(m.group(1)) for m in MULT.finditer(txt)]
        ks = sorted({int(m.group(1).replace(",", "")) for m in KTOK.finditer(txt)})
        pairs = [(float(a), float(b)) for a, b in RANGEPAIR.findall(txt)]
        rows.append(dict(
            src=src, n_chars=len(txt),
            C_STRICT=sp and bool(mults) and bool(ADJUD.search(txt)),
            C_PROX=sp and bool(mults),
            C_ALL=fileset[src] and sp,
            N_MULT=len(mults), MAX_MULT=max(mults) if mults else np.nan,
            MIN_MULT=min(mults) if mults else np.nan,
            STATES_K=bool(ks), N_DISTINCT_K=len(ks),
            K_MIN=min(ks) if ks else 0, K_MAX=max(ks) if ks else 0,
            VARYING_K=len(ks) > 1,
            IS_BAND=bool(pairs), BAND_LO=pairs[0][0] if pairs else np.nan,
            BAND_HI=pairs[0][1] if pairs else np.nan,
            ADJUDICATED=bool(ADJUD.search(txt))))
    return pd.DataFrame(rows), len(U), n_md


# ==================================================== panels / runner (record's, inherited)
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.seg = {}
        for f in LAD["CADENCE"]:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            self.seg[f] = np.flatnonzero(m)
        self.i0 = WARMUP
        self.ioos = px.index.searchsorted(pd.Timestamp(OOS_START))
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)       # higher score -> lower key
        self.elig = above & (vol20 < MAXVOL)


def mech(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


def build(pan, N, H, gross, freq):
    """1098/1159's min-hold book: hold a name H days, refill to N from the eligible set."""
    reb = pan.seg[freq]
    T = pan.rets.shape[0]
    K = len(pan.iinv)
    W = np.zeros((T, pan.rets.shape[1]))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[t].copy()
            k[~(pan.elig[t] & pr[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = gross / len(sel)
    return W


def nrun(pan, Wt, freq):
    """weights are already t+1-applied (the mask is shifted); costs on turnover."""
    rets = pan.rets
    T, M = rets.shape
    reb = pan.seg[freq]
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1) - turn * COST / 1e4


def sharpe(r):
    v = r.std(ddof=0) * np.sqrt(252)
    return r.mean() * 252 / v if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + r)
    return float((e / np.maximum.accumulate(e) - 1).min())


def ulcer(r):
    e = np.cumprod(1 + r)
    dd = e / np.maximum.accumulate(e) - 1.0
    return float(np.sqrt(np.mean(dd ** 2)))


def cagr(r):
    e = np.cumprod(1 + r)
    return float(e[-1] ** (252 / len(r)) - 1)


def sixstats(r):
    c, d = cagr(r), mdd(r)
    return dict(CAGR=c, Sharpe=float(sharpe(r)), MaxDD=d,
                Vol=float(r.std(ddof=0) * np.sqrt(252)),
                Calmar=float(c / abs(d)) if d else np.nan, Ulcer=ulcer(r))


def build_panels():
    out = []
    u = load_universe()
    out.append(("U56", u, [c for c in u.columns if c != "SPY"]))
    b = load_universe(broad=True)
    out.append(("B136", b, [c for c in b.columns if c != "SPY"]))
    s = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    out.append(("SMALL", s, [c for c in s.columns if c != "SPY" and c not in bad]))
    return out


# ==================================================== main
def main():
    t0 = time.time()
    gates = []
    say("=" * 96)
    say("IDEA 1155 (cloud, 2026-09-17) — is the COUNT INFLATION of MAX-MINUS-MIN a GENERAL DEFECT?")
    say("  dial 1 = CLAIM SET     {C_STRICT, C_PROX, C_ALL}")
    say("  dial 2 = MATCHING RULE {M_NONE, M_SUBSAMPLE, M_PAIRWISE, M_D2}")
    say("=" * 96)

    # ---------------------------------------------------------------- ARM 0: DATA-FREE
    say("")
    say("(0) THE ARITHMETIC, PRINTED BEFORE ANY DATA IS TOUCHED")
    say("    A RANGE IS NOT AN ESTIMATOR OF DISPERSION. For k iid N(0,1) draws E[max-min] =")
    say("    d2(k), which RISES WITHOUT BOUND in k. Two ladders with the SAME underlying")
    say("    dispersion and DIFFERENT rung counts therefore publish different 'spreads'.")
    rng = np.random.default_rng(SEED0)
    mc = rng.standard_normal((400_000, 12))
    rows0 = []
    say(f"    {'k':>3}  {'d2(k) exact':>12}  {'d2(k) MC 4e5':>13}  {'vs k=2':>8}  {'vs k=4':>8}  ladder")
    for k in range(2, 13):
        e = D2[k]
        m = float((mc[:, :k].max(axis=1) - mc[:, :k].min(axis=1)).mean())
        lad = ",".join(n for n, v in LAD.items() if len(v) == k)
        say(f"    {k:>3}  {e:>12.6f}  {m:>13.6f}  {e / D2[2]:>8.4f}  {e / D2[4]:>8.4f}  {lad}")
        rows0.append(dict(k=k, d2_exact=e, d2_mc=m, vs_k2=e / D2[2], vs_k4=e / D2[4]))
    pd.DataFrame(rows0).to_csv(f"{OUT}.d2.csv", index=False)
    dmax = max(abs(D2[k] - float((mc[:, :k].max(axis=1) - mc[:, :k].min(axis=1)).mean()))
               for k in range(2, 13))
    gates.append(dict(gate="G0 Monte-Carlo d2(k) == published Hartley constants",
                      value=dmax, target=0.0, pass_=dmax < 5e-3))
    say("")
    say("    THE RECORD'S OWN LADDERS ARE 2, 4, 6 AND 10 RUNGS LONG. A GROSS ladder's max-min")
    say(f"    is {D2[10] / D2[2]:.4f}x a CADENCE ladder's ON PURE NOISE, and {D2[10] / D2[4]:.4f}x an H ladder's.")
    say("    1140's COMMITTED '1.7x - 61x band' pools a k=2 range with a k=3 one, and")
    say(f"    d2(3)/d2(2) = {D2[3] / D2[2]:.4f} — SO THE BOTTOM OF THAT COMMITTED BAND IS 1.13x THE")
    say("    COUNT DIFFERENCE ALONE, i.e. INDISTINGUISHABLE FROM ZERO EFFECT AT ITS LOWER END.")
    gates.append(dict(gate="G0b 1140's committed band floor 1.7x exceeds d2(3)/d2(2) but by <1.2x",
                      value=1.7 / (D2[3] / D2[2]), target=1.13,
                      pass_=bool(1.0 < 1.7 / (D2[3] / D2[2]) < 1.2)))

    # ---------------------------------------------------------------- ARM A: CENSUS
    say("")
    say("=" * 96)
    say("(A) CENSUS — the record's committed SPREAD / BAND / RANGE claims")
    say("=" * 96)
    cdf, nU, n_md = census()
    cdf.to_csv(f"{OUT}.census.csv", index=False)
    say(f"  corpus: {nU:,} committed text units "
        f"(LEADERBOARD rows {int((cdf.src == 'LEADERBOARD').sum()):,}, "
        f"CHANGELOG paragraphs {int((cdf.src == 'CHANGELOG').sum()):,}, {n_md} markdown artefacts)")
    crows = []
    for cs in CLAIMSETS:
        sub = cdf[cdf[cs]]
        n = len(sub)
        d = dict(CLAIM_SET=cs, N=n,
                 STATES_K=int(sub.STATES_K.sum()), NO_K=int((~sub.STATES_K).sum()),
                 VARYING_K=int(sub.VARYING_K.sum()), IS_BAND=int(sub.IS_BAND.sum()),
                 ADJUD=int(sub.ADJUDICATED.sum()),
                 ADJUD_NO_K=int((sub.ADJUDICATED & ~sub.STATES_K).sum()))
        for key in ["STATES_K", "VARYING_K", "ADJUD_NO_K"]:
            d[key + "_share"] = d[key] / n if n else np.nan
        crows.append(d)
        say(f"  {cs:9s} n={n:6d}  states a point count {d['STATES_K']:5d} ({d['STATES_K_share']:.4f})  "
            f"COMPARES DIFFERENT COUNTS {d['VARYING_K']:5d} ({d['VARYING_K_share']:.4f})  "
            f"quotes an x-to-x BAND {d['IS_BAND']:5d}  adjudicated {d['ADJUD']:5d}  "
            f"ADJUDICATED WITH NO COUNT {d['ADJUD_NO_K']:5d} ({d['ADJUD_NO_K_share']:.4f})")
    pd.DataFrame(crows).to_csv(f"{OUT}.claims.csv", index=False)
    gates.append(dict(gate="G6 claim sets nest C_STRICT<=C_PROX<=C_ALL",
                      value=float((cdf.C_STRICT & ~cdf.C_PROX).sum() + (cdf.C_PROX & ~cdf.C_ALL).sum()),
                      target=0.0,
                      pass_=bool(((cdf.C_STRICT & ~cdf.C_PROX).sum() + (cdf.C_PROX & ~cdf.C_ALL).sum()) == 0)))

    # ---- how many committed MULTIPLES are smaller than the count inflation they carry
    say("")
    say("  RE-EXPRESSING THE COMMITTED MULTIPLES. For each unit stating BOTH a multiple and")
    say("  two different point counts, the count difference alone buys d2(k_max)/d2(k_min).")
    say("  A multiple at or below that is NOT AN EFFECT — it is the two counts.")
    rr = []
    for cs in CLAIMSETS:
        sub = cdf[cdf[cs] & cdf.VARYING_K & cdf.N_MULT.gt(0)]
        for _, u in sub.iterrows():
            kmin, kmax = int(u.K_MIN), int(u.K_MAX)
            infl = D2[min(max(kmax, 2), 12)] / D2[min(max(kmin, 2), 12)]
            for col, nm in [("MIN_MULT", "smallest"), ("MAX_MULT", "largest")]:
                rr.append(dict(CLAIM_SET=cs, src=u.src, which=nm, mult=float(u[col]),
                               k_min=kmin, k_max=kmax, inflation=infl,
                               SURVIVES=bool(float(u[col]) > infl),
                               corrected=float(u[col]) / infl))
    rrdf = pd.DataFrame(rr)
    rrdf.to_csv(f"{OUT}.reread.csv", index=False)
    for cs in CLAIMSETS:
        s = rrdf[(rrdf.CLAIM_SET == cs) & (rrdf.which == "smallest")]
        b = rrdf[(rrdf.CLAIM_SET == cs) & (rrdf.which == "largest")]
        if len(s):
            say(f"    {cs:9s} checkable units {len(s):5d}   SMALLEST quoted multiple survives its own "
                f"count inflation at {int(s.SURVIVES.sum()):4d} ({s.SURVIVES.mean():.4f}); "
                f"LARGEST at {int(b.SURVIVES.sum()):4d} ({b.SURVIVES.mean():.4f}); "
                f"median inflation carried {s.inflation.median():.4f}")
        else:
            say(f"    {cs:9s} checkable units 0")

    # ---------------------------------------------------------------- ARM B: PRICE
    say("")
    say("=" * 96)
    say("(B) RE-WALKING THE RECORD'S FOUR LADDERS — 2, 4, 6 and 10 rungs, 3 panels, 6 statistics")
    say("=" * 96)
    panels = build_panels()
    books, ladrows, wf = [], [], []
    panel_names = [p[0] for p in panels]
    ctx = {}
    kmin_all = min(len(v) for v in LAD.values())

    for pname, px, invest in panels:
        pan = Panel(pname, px, invest)
        i0, ioos = pan.i0, pan.ioos
        spy = px["SPY"].pct_change().fillna(0.0).values
        s_full, s_oos = spy[i0:], spy[ioos:]
        base_r = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].fillna(0.0).values
        b_full, b_oos = base_r[i0:], base_r[ioos:]
        h = len(s_full) // 2
        spyT, baseT = sixstats(s_full), sixstats(b_full)
        spyH = (float(sharpe(s_full[:h])), float(sharpe(s_full[h:])))
        baseH = (float(sharpe(b_full[:h])), float(sharpe(b_full[h:])))
        ctx[pname] = dict(spyT=spyT, spyH=spyH, spy_oos=sixstats(s_oos),
                          baseT=baseT, baseH=baseH, base_oos=sixstats(b_oos))
        say(f"  {pname:6s} n_invest={len(invest):4d}  SPY {spyT['CAGR']:.2%} / {spyT['Sharpe']:.4f} / "
            f"{spyT['MaxDD']:.2%} (halves {spyH[0]:.4f}/{spyH[1]:.4f}), OOS {cagr(s_oos):.2%} / "
            f"{sharpe(s_oos):.4f} / {mdd(s_oos):.2%}")
        say(f"  {'':6s} {'':13s}  LIVE RULES v2 {baseT['CAGR']:.2%} / {baseT['Sharpe']:.4f} / "
            f"{baseT['MaxDD']:.2%}, OOS {cagr(b_oos):.2%} / {sharpe(b_oos):.4f}")
        if pname == "U56":
            gates.append(dict(gate="G3 live RULES v2 U56 MaxDD == record -12.05%",
                              value=baseT["MaxDD"], target=LIVE_MAXDD_COMMITTED,
                              pass_=abs(baseT["MaxDD"] - LIVE_MAXDD_COMMITTED) < 5e-4))

        # one-factor-at-a-time around the anchor; the anchor book is shared by all four ladders
        cache = {}

        def book(N, H, g, f):
            key = (N, H, g, f)
            if key not in cache:
                cache[key] = nrun(pan, build(pan, N, H, g, f), f)
            return cache[key]

        paths = {}
        for lname, rungs in LAD.items():
            for rung in rungs:
                N, H, g, f = A_N, A_H, A_G, A_C
                if lname == "N":
                    N = rung
                elif lname == "H":
                    H = rung
                elif lname == "GROSS":
                    g = rung
                else:
                    f = rung
                r = book(N, H, g, f)
                paths[(lname, rung)] = r
                rf, ros = r[i0:], r[ioos:]
                st = sixstats(rf)
                h1, h2 = float(sharpe(rf[:h])), float(sharpe(rf[h:]))
                so = sixstats(ros)
                books.append(dict(panel=pname, ladder=lname, rung=rung, N=N, H=H, gross=g,
                                  cadence=f, **st, H1=h1, H2=h2,
                                  IS_Sharpe=float(sharpe(r[i0:ioos])),
                                  OOS_CAGR=so["CAGR"], OOS_Sharpe=so["Sharpe"], OOS_MaxDD=so["MaxDD"],
                                  KEEP_4a=bool(h1 > baseH[0] and h2 > baseH[1]
                                               and st["MaxDD"] >= baseT["MaxDD"]),
                                  KEEP_4b=bool(h1 > spyH[0] and h2 > spyH[1]
                                               and so["Sharpe"] > ctx[pname]["spy_oos"]["Sharpe"]
                                               and st["MaxDD"] >= DD_CAP * spyT["MaxDD"]
                                               and st["CAGR"] >= CAGR_FLOOR * spyT["CAGR"]),
                                  KEEP_4b_OOS=bool(so["Sharpe"] > ctx[pname]["spy_oos"]["Sharpe"]
                                                   and so["MaxDD"] >= DD_CAP * ctx[pname]["spy_oos"]["MaxDD"]
                                                   and so["CAGR"] >= CAGR_FLOOR * ctx[pname]["spy_oos"]["CAGR"])))

        # G1: the anchor book reproduces engine.backtest.
        # THIS GATE FAILED ON THE FIRST CUT AT 1.977e-02 AND THE CAUSE IS PRINTED, NOT PATCHED
        # OVER: `build` writes its targets on the ALREADY-SHIFTED rebalance rows (t+1, the
        # APPLICATION row), because that is the row `nrun` starts each segment on.
        # `engine.backtest` shifts BOTH the weights frame and the mask by one row, so handing it
        # an application-time frame lags it a SECOND time. The comparand must therefore be the
        # DECISION-time frame Wdec[t] = W[t+1]. Nothing in the arithmetic of either runner
        # changed; the first cut compared two books one trading day apart.
        if pname == "U56":
            Wa = build(pan, A_N, A_H, A_G, A_C)
            Wdec = np.vstack([Wa[1:], np.zeros((1, Wa.shape[1]))])
            eng = backtest(px, pd.DataFrame(Wdec, index=px.index, columns=px.columns),
                           cost_bps=COST, freq=A_C)["returns"].values
            d = float(np.nanmax(np.abs(np.asarray(eng[i0:], float) - book(A_N, A_H, A_G, A_C)[i0:])))
            gates.append(dict(gate="G1 fast runner == engine.backtest on the anchor (post-warm-up)",
                              value=d, target=0.0, pass_=d < 1e-9))
            nn = np.flatnonzero(np.isnan(np.asarray(eng, float)))
            gates.append(dict(gate="G1b engine.backtest NaN rows all sit inside the warm-up",
                              value=float(len(nn)), target=float(len(nn)),
                              pass_=bool(np.all(nn < WARMUP))))

        # ---- the ladder spreads, on the tape and under a joint block bootstrap
        rboot = np.random.default_rng(SEED0 + 977 * panel_names.index(pname))
        Tn = len(s_full)
        nb = int(np.ceil(Tn / BLOCK))
        starts_boot = rboot.integers(0, Tn - BLOCK, size=(NBOOT, nb))
        idxs = np.concatenate([np.arange(BLOCK)[None, None, :] + starts_boot[:, :, None]], axis=0)
        idxs = idxs.reshape(NBOOT, -1)[:, :Tn]

        for lname, rungs in LAD.items():
            obs = {s: [] for s in STATS}
            mat = np.column_stack([paths[(lname, rg)][i0:] for rg in rungs])
            for j, rg in enumerate(rungs):
                st = sixstats(mat[:, j])
                for s in STATS:
                    obs[s].append(st[s])
            # bootstrap sampling SD of each spread statistic
            bs = {(s, m): [] for s in STATS for m in MATCH}
            for d_ in range(NBOOT):
                sub = mat[idxs[d_], :]
                vals = {s: [] for s in STATS}
                for j in range(len(rungs)):
                    st = sixstats(sub[:, j])
                    for s in STATS:
                        vals[s].append(st[s])
                for s in STATS:
                    for m in MATCH:
                        bs[(s, m)].append(spread(vals[s], m, kmin_all))
            for s in STATS:
                base_v = obs[s]
                row = dict(panel=pname, ladder=lname, k=len(rungs), stat=s)
                for m in MATCH:
                    v = spread(base_v, m, kmin_all)
                    arr = np.asarray(bs[(s, m)], float)
                    sd = float(np.nanstd(arr, ddof=1))
                    row[m] = v
                    row[m + "_bootSD"] = sd
                    row[m + "_t"] = v / sd if sd > 0 else np.nan
                row["INFLATION_vs_matched"] = (row["M_NONE"] / row["M_SUBSAMPLE"]
                                               if row["M_SUBSAMPLE"] else np.nan)
                row["INFLATION_vs_d2"] = (row["M_NONE"] / row["M_D2"]) if row["M_D2"] else np.nan
                ladrows.append(row)
        say(f"    {pname} done  t={time.time() - t0:.0f}s")

    bdf = pd.DataFrame(books)
    ldf = pd.DataFrame(ladrows)
    bdf.to_csv(f"{OUT}.books.csv", index=False)
    ldf.to_csv(f"{OUT}.ladders.csv", index=False)

    say("")
    say("  MAX-MIN vs COUNT-MATCHED, by ladder (mean over 6 statistics and 3 panels):")
    say(f"    {'ladder':8s} {'k':>3}  {'M_NONE/M_SUBSAMPLE':>19}  {'M_NONE/M_D2':>12}  "
        f"{'d2(k)/d2(2) predicted':>22}")
    for lname, rungs in LAD.items():
        s = ldf[ldf.ladder == lname]
        say(f"    {lname:8s} {len(rungs):>3}  {s.INFLATION_vs_matched.mean():>19.4f}  "
            f"{s.INFLATION_vs_d2.mean():>12.4f}  {D2[len(rungs)] / D2[2]:>22.4f}")
    say("")
    say("  1148's HEADLINE, RE-MEASURED ON 12 (panel, ladder) FAMILIES: in how many of the 6")
    say("  statistics is the COUNT-MATCHED spread SMALLER than max-min?")
    n_small = int((ldf.M_SUBSAMPLE < ldf.M_NONE).sum())
    say(f"    {n_small} of {len(ldf)} (panel, ladder, statistic) cells; median ratio "
        f"{ldf.INFLATION_vs_matched.median():.4f}  (1148 committed 5 of 6, median 1.137x)")
    bystat = ldf.groupby("stat").INFLATION_vs_matched.median()
    for s in STATS:
        sub = ldf[ldf.stat == s]
        say(f"      {s:8s} median inflation {bystat[s]:.4f}   smaller-at "
            f"{int((sub.M_SUBSAMPLE < sub.M_NONE).sum())} of {len(sub)}")
    gates.append(dict(gate="G4 M_SUBSAMPLE <= M_NONE at every cell (a subset range cannot exceed)",
                      value=float((ldf.M_SUBSAMPLE > ldf.M_NONE + 1e-12).sum()), target=0.0,
                      pass_=bool((ldf.M_SUBSAMPLE > ldf.M_NONE + 1e-12).sum() == 0)))
    gates.append(dict(gate="G5 M_PAIRWISE <= M_NONE at every cell (a mean gap cannot exceed the range)",
                      value=float((ldf.M_PAIRWISE > ldf.M_NONE + 1e-12).sum()), target=0.0,
                      pass_=bool((ldf.M_PAIRWISE > ldf.M_NONE + 1e-12).sum() == 0)))
    # G7: d2 is a CONSTANT divisor at a fixed k, so it cannot change a WITHIN-ladder t-stat.
    # Stated as a gate because it is the whole limit of the repair: M_D2 makes ACROSS-ladder
    # comparison legal and does nothing whatever for decisiveness.
    dt = float(np.nanmax(np.abs(ldf.M_D2_t.values - ldf.M_NONE_t.values)))
    gates.append(dict(gate="G7 M_D2 t-stat == M_NONE t-stat at every cell (constant divisor)",
                      value=dt, target=0.0, pass_=dt < 1e-9))

    say("")
    say("  DECISIVENESS: share of cells whose spread exceeds 2 block-bootstrap SEs of itself")
    say(f"    {'rule':12s} " + "  ".join(f"{s:>9s}" for s in STATS) + "      all")
    for m in MATCH:
        parts = []
        for s in STATS:
            sub = ldf[ldf.stat == s]
            parts.append(f"{float((sub[m + '_t'].abs() > 2).mean()):>9.4f}")
        allv = float((ldf[m + "_t"].abs() > 2).mean())
        say(f"    {m:12s} " + "  ".join(parts) + f"  {allv:>9.4f}")

    # ---------------------------------------------------------------- ARM C: RULE 8
    say("")
    say("=" * 96)
    say("(C) RULE 8 WALK-FORWARD — THE MATCHING RULE IS THE CHOOSER.")
    say("    The record's habit: pick the dial with the WIDEST spread and tune it. Here the")
    say("    chooser reads each ladder's IS-window (2009-2016 ONLY) Sharpe spread under one")
    say("    matching rule, takes the widest ladder, then takes that ladder's IS argmax.")
    say("    2017-2026 is read ONCE. C_ANCHOR (never move) is the do-nothing control.")
    say("=" * 96)
    for pname, px, invest in panels:
        pan = Panel(pname, px, invest)
        i0, ioos = pan.i0, pan.ioos
        sb = bdf[bdf.panel == pname]
        for m in MATCH + ["C_ANCHOR"]:
            if m == "C_ANCHOR":
                r = sb[(sb.ladder == "N") & (sb.rung == A_N)].iloc[0]
                widest, wspread = "(none)", 0.0
            else:
                sp = {}
                for lname, rungs in LAD.items():
                    vals = [sb[(sb.ladder == lname) & (sb.rung == rg)].iloc[0].IS_Sharpe for rg in rungs]
                    sp[lname] = spread(vals, m, kmin_all)
                widest = max(sp, key=lambda x: sp[x])
                wspread = sp[widest]
                cand = sb[sb.ladder == widest]
                r = cand.loc[cand.IS_Sharpe.idxmax()]
            c = ctx[pname]
            wf.append(dict(panel=pname, rule=m, widest_ladder=widest, widest_spread=wspread,
                           pick=f"N={int(r.N)}/H={int(r.H)}/g={r.gross:.2f}/{r.cadence}",
                           IS_Sharpe=r.IS_Sharpe, CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD,
                           OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                           SPY_OOS_Sharpe=c["spy_oos"]["Sharpe"], SPY_OOS_CAGR=c["spy_oos"]["CAGR"],
                           LIVE_OOS_Sharpe=c["base_oos"]["Sharpe"],
                           KEEP_4a=bool(r.KEEP_4a), KEEP_4b=bool(r.KEEP_4b),
                           KEEP_4b_OOS=bool(r.KEEP_4b_OOS)))
    wdf = pd.DataFrame(wf)
    wdf.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"    {'panel':6s} {'rule':12s} {'widest':8s} {'pick':28s} {'OOS CAGR':>9s} {'OOS Sh':>8s} "
        f"{'OOS DD':>8s}  4a 4b")
    for _, r in wdf.iterrows():
        say(f"    {r.panel:6s} {r['rule']:12s} {r.widest_ladder:8s} {r.pick:28s} "
            f"{r.OOS_CAGR:>9.2%} {r.OOS_Sharpe:>8.4f} {r.OOS_MaxDD:>8.2%}  "
            f"{'Y' if r.KEEP_4a else 'n'}  {'Y' if r.KEEP_4b else 'n'}")
    say("")
    say("  POOLED over 3 panels:")
    for m in MATCH + ["C_ANCHOR"]:
        s = wdf[wdf["rule"] == m]
        say(f"    {m:12s} mean OOS Sharpe {s.OOS_Sharpe.mean():.4f}  mean OOS CAGR "
            f"{s.OOS_CAGR.mean():.2%}  mean OOS MaxDD {s.OOS_MaxDD.mean():.2%}  "
            f"4b {int(s.KEEP_4b.sum())} of {len(s)}   widest ladder chosen: "
            f"{', '.join(sorted(set(s.widest_ladder)))}")

    say("")
    say(f"  BOTH KEEP PATHS over all {len(bdf)} books (PROTOCOL rule 4):")
    say(f"    4a {int(bdf.KEEP_4a.sum())} of {len(bdf)};  4b full {int(bdf.KEEP_4b.sum())};  "
        f"4b OOS {int(bdf.KEEP_4b_OOS.sum())};  BOTH {int((bdf.KEEP_4b & bdf.KEEP_4b_OOS).sum())}")
    for pname in panel_names:
        s = bdf[bdf.panel == pname]
        say(f"      {pname:6s} 4a {int(s.KEEP_4a.sum())}/{len(s)}   4b {int(s.KEEP_4b.sum())}/{len(s)}"
            f"   4b-OOS {int(s.KEEP_4b_OOS.sum())}/{len(s)}")

    # ---------------------------------------------------------------- GATES
    say("")
    say("=" * 96)
    say("GATES")
    say("=" * 96)
    gg = pd.DataFrame(gates)
    gg.to_csv(f"{OUT}.gates.csv", index=False)
    for _, g in gg.iterrows():
        say(f"  [{'PASS' if g.pass_ else 'FAIL'}] {g.gate:64s} value={g.value:.6g} target={g.target:.6g}")
    say(f"  {int(gg.pass_.sum())} of {len(gg)} gates pass")
    say(f"\n  total runtime {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG))
    return bdf, ldf, wdf, gg


if __name__ == "__main__":
    main()
