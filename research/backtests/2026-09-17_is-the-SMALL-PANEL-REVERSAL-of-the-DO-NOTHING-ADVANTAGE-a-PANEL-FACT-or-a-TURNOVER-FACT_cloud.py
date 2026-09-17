#!/usr/bin/env python3
"""
Idea 1208 (cloud lane, 2026-09-17) — is the SMALL-PANEL REVERSAL of the DO-NOTHING ADVANTAGE
a PANEL FACT or a TURNOVER FACT?

THE PREMISE, READ FROM THE RECORD AND NOT RECALLED.  Idea 1206 walked 1155's five choosers over
472 picks each and found the headline (do-nothing beats the widest-dial habit) to be a three-draw
accident: no pooled delta cleared 2 clustered SE.  But its BY PANEL table carried the one large
effect in the whole run, and the record committed it:

    panel       M_NONE  M_SUBSAMPLE   M_PAIRWISE         M_D2     C_ANCHOR     C_RANDOM    C_BEST_IS
    U56         1.1823       1.1689       1.1689       1.1767       1.2165       1.2110       1.1354
    B136        1.1475       1.1270       1.1270       1.1271       1.1708       1.1447       1.1460
    SMALL       0.5899       0.6783       0.6783       0.6718       0.5298       0.5025       0.6148

C_ANCHOR (never move) is TOP on U56 and B136 and THIRD FROM BOTTOM on SMALL, where the three
count-matched rules beat it by +0.1420 to +0.1485 of mean OOS Sharpe — twenty times the pooled
gap 1206 could not resolve.  1206 named the reversal and did not explain it.

THE HYPOTHESIS THE QUEUE NAMES.  1206 also found the count-matched rules move the WIDEST DIAL
from N to CADENCE (0.3072-0.3136 of picks against M_NONE's 0.0551).  The CADENCE ladder is
{W, M}; its far rung is a TURNOVER CUT.  So the SMALL reversal may be nothing about the
small-cap tape and everything about a cost rebate the count-matched rules collect because the
anchor book turns over more on that panel.  This run separates the two.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  COST   {0, 10, 25, 50} bps per unit turnover     -- the cost rung
  MATCH  {T_NONE, T_BAND, T_CHARGE}                -- the turnover match

  T_NONE    1206's run, unchanged.  Every book pays its own turnover.
  T_BAND    the chooser may only pick rungs whose IS-window turnover, MEASURED AT THE ANCHOR'S
            GROSS, is within +/-25% of the anchor's (band pre-declared, sensitivity reported,
            never adjudicated on).  The anchor is in its own band by construction, so every
            ladder keeps at least one candidate.  Every GROSS rung maps to the anchor itself
            under that measurement, so the GROSS ladder is untouched and the band bites
            precisely on N, H and CADENCE, where the story lives.
  T_CHARGE  every book pays the turnover of the ANCHOR'S SELECTION FRAME READ AT THE BOOK'S OWN
            GROSS RUNG, i.e. turn of (N_anchor, H_anchor, g_book, cadence_anchor) — a book that
            is always built, never a scaled estimate.  Selection-driven turnover differences are
            removed and the gross rung's own turnover is kept.  The counterfactual "what if
            moving were turnover-neutral?".  It is the identity on the anchor and on the whole
            GROSS ladder (G2), which is exactly the intent.

A DEFECT THIS RUN'S GATES CAUGHT AND THE RECORD SHOULD CARRY.  The first cut of both matches
assumed turnover is LINEAR IN GROSS (turn(g) = g*turn(1)), which is the natural reading of
W = g * selection_frame.  It is FALSE, and G2 rejected it at 0.0173 of one-way turnover on the
record's own anchor: the drifted weights are renormalised by a portfolio value that includes a
cash sleeve of size 1-g, so the weight a position drifts to — and hence the trade needed to
restore it — depends on the gross rung.  Every construction below therefore uses BUILT turnover
paths and never a scaled one.  The measured non-linearity is reported in (A).

COST is an accounting assumption and not a strategy parameter, so it is REPORTED at all four
rungs and never chosen on performance; only MATCH (with window/anchor) is walked forward.
Note T_NONE and T_CHARGE coincide exactly at 0 bps (G5) — the grid is 12 points, 11 distinct.

WHAT IS NOT A DIAL.  PANEL {U56, B136, SMALL} is not a dial (rule 9, all three always read) —
it is the object of the question.  The four ladders {N (6), H (4), GROSS (10), CADENCE (2)},
the four matching rules {M_NONE, M_SUBSAMPLE, M_PAIRWISE, M_D2}, the three controls
{C_ANCHOR, C_RANDOM, C_BEST_IS}, the four anchors, the three IS windows and the fold calendar
are 1206's, inherited whole and unchanged.

SURVIVORSHIP (rule 9).  B136 and SMALL are CURRENT constituents of their screens; the SMALL
panel is the sub-$2B screen of data/SMALL_PANEL_README.md with every ticker whose max 1-day
move reaches 100% dropped before use.  Any statement about SMALL below is a statement about
names that survived to the screen date, and the reversal under test is itself on that panel.

PROTOCOL: rule 2 costs (10 bps is the rung the verdict is read at) and t+1 execution; rule 8
walk-forward — MATCH/window/anchor chosen on folds ENDING 2016 OR EARLIER, the 2017-2026 folds
read ONCE, and the reversal statistic itself reported IS vs OOS; BOTH KEEP paths (4a vs live
RULES v2, 4b vs SPY) on every book and every stitched chooser curve.  RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network):
  python research/backtests/2026-09-17_is-the-SMALL-PANEL-REVERSAL-of-the-DO-NOTHING-ADVANTAGE-a-PANEL-FACT-or-a-TURNOVER-FACT_cloud.py
"""
from __future__ import annotations

import itertools
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
SLUG = "is-the-SMALL-PANEL-REVERSAL-of-the-DO-NOTHING-ADVANTAGE-a-PANEL-FACT-or-a-TURNOVER-FACT"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]

# ---- dial 1: the cost rung.  10 bps is PROTOCOL rule 2 and the rung the verdict is read at.
COSTS = [0.0, 10.0, 25.0, 50.0]
COST_REF = 10.0
# ---- dial 2: the turnover match.  BAND pre-declared at 0.25 before any result is read.
MODES = ["T_NONE", "T_BAND", "T_CHARGE"]
BAND = 0.25
BAND_SENS = [0.10, 0.25, 0.50]      # reported as a diagnostic; never adjudicated on

LAD = {
    "N": [5, 10, 15, 20, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
    "CADENCE": ["W", "M"],
}
MATCH = ["M_NONE", "M_SUBSAMPLE", "M_PAIRWISE", "M_D2"]
CONTROLS = ["C_ANCHOR", "C_RANDOM", "C_BEST_IS"]
RULES = MATCH + CONTROLS

ANCHORS = {
    "A_REC":   (20, 126, 0.75, "W"),
    "A_TIGHT": (10, 63, 0.55, "W"),
    "A_SLOW":  (30, 252, 0.75, "M"),
    "A_FAST":  (5, 21, 0.50, "W"),
}
A_N, A_H, A_G, A_C = ANCHORS["A_REC"]

WINDOWS = [2, 3, 4]
FOLD_YEARS = list(range(2013, 2027))
DIAL_IS_LAST = 2016
SEED0 = 12061206

D2 = {2: 1.128379, 3: 1.692569, 4: 2.058751, 5: 2.325929, 6: 2.534413, 7: 2.704357,
      8: 2.847201, 9: 2.970026, 10: 3.077505, 11: 3.172873, 12: 3.258457}

# 1206's committed BY PANEL means at 10 bps, T_NONE — the reproduction gate
REPRO_1206 = {
    ("U56", "M_NONE"): 1.1823, ("U56", "M_SUBSAMPLE"): 1.1689, ("U56", "M_PAIRWISE"): 1.1689,
    ("U56", "M_D2"): 1.1767, ("U56", "C_ANCHOR"): 1.2165, ("U56", "C_RANDOM"): 1.2110,
    ("U56", "C_BEST_IS"): 1.1354,
    ("B136", "M_NONE"): 1.1475, ("B136", "M_SUBSAMPLE"): 1.1270, ("B136", "M_PAIRWISE"): 1.1270,
    ("B136", "M_D2"): 1.1271, ("B136", "C_ANCHOR"): 1.1708, ("B136", "C_RANDOM"): 1.1447,
    ("B136", "C_BEST_IS"): 1.1460,
    ("SMALL", "M_NONE"): 0.5899, ("SMALL", "M_SUBSAMPLE"): 0.6783, ("SMALL", "M_PAIRWISE"): 0.6783,
    ("SMALL", "M_D2"): 0.6718, ("SMALL", "C_ANCHOR"): 0.5298, ("SMALL", "C_RANDOM"): 0.5025,
    ("SMALL", "C_BEST_IS"): 0.6148,
}
LIVE_MAXDD_COMMITTED = -0.1205

LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ==================================================== 1155/1206's four matching rules, verbatim
def spread(vals, rule, k_min=None):
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
        return float(np.mean([abs(a - b) for a, b in itertools.combinations(v, 2)]))
    if rule == "M_D2":
        return float((v.max() - v.min()) / D2[min(max(k, 2), 12)])
    raise ValueError(rule)


# ==================================================== panels / runner (1206's, inherited)
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
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.yr = px.index.year.values


def build1(pan, N, H, freq):
    """1206's min-hold selection frame at GROSS = 1.0."""
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
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def nrun(pan, Wt, freq):
    """1206's runner, SPLIT: returns (gross daily return, daily turnover).  Cost never feeds
    back into the weight path, so net at any rung c is exactly gross - turn*c/1e4 (G9)."""
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
    return (held * rets).sum(axis=1), turn


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min())


def cagr(r):
    r = np.asarray(r, float)
    e = np.cumprod(1 + r)
    return float(e[-1] ** (252 / len(r)) - 1)


def stats3(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


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


def ladder_books(anchor):
    an, ah, ag, af = anchor
    return {
        "N": [(rg, ah, ag, af) for rg in LAD["N"]],
        "H": [(an, rg, ag, af) for rg in LAD["H"]],
        "GROSS": [(an, ah, rg, af) for rg in LAD["GROSS"]],
        "CADENCE": [(an, ah, ag, rg) for rg in LAD["CADENCE"]],
    }


def choose(rule, lads, isr, rng, kmin_all):
    """1206's chooser, unchanged.  `lads` may carry a RESTRICTED candidate list per ladder
    under T_BAND; the rules themselves are untouched."""
    if rule == "C_ANCHOR":
        return None, "(none)", 0.0
    if rule == "C_BEST_IS":
        allb = sorted({b for v in lads.values() for b in v})
        pick = max(allb, key=lambda b: (isr[b] if np.isfinite(isr[b]) else -np.inf))
        return pick, "(all)", 0.0
    if rule == "C_RANDOM":
        names = sorted(lads)
        lname = names[int(rng.integers(0, len(names)))]
        cand = lads[lname]
        pick = max(cand, key=lambda b: (isr[b] if np.isfinite(isr[b]) else -np.inf))
        return pick, lname, 0.0
    sp = {ln: spread([isr[b] for b in bks], rule, kmin_all) for ln, bks in lads.items()}
    widest = max(sp, key=lambda x: (sp[x] if np.isfinite(sp[x]) else -np.inf))
    cand = lads[widest]
    pick = max(cand, key=lambda b: (isr[b] if np.isfinite(isr[b]) else -np.inf))
    return pick, widest, float(sp[widest])


# ==================================================== main
def main():
    t0 = time.time()
    gates = []
    say("=" * 104)
    say("IDEA 1208 (cloud lane, 2026-09-17) — is the SMALL-PANEL REVERSAL of the DO-NOTHING")
    say("  ADVANTAGE a PANEL FACT or a TURNOVER FACT?")
    say("  dial 1 = COST   {0, 10, 25, 50} bps            (accounting rung; never chosen on)")
    say("  dial 2 = MATCH  {T_NONE, T_BAND, T_CHARGE}     (the turnover match; band 0.25)")
    say("  Panels U56/B136/SMALL are NOT a dial (rule 9) — the panel split IS the question.")
    say("=" * 104)

    # ------------------------------------------------ ARM 0: DATA-FREE, PRINTED FIRST
    say("")
    say("(0) THE QUESTION, STATED AS ARITHMETIC BEFORE ANY DATA IS TOUCHED.")
    say("    1206's committed BY PANEL means at 10 bps.  C_ANCHOR minus each matching rule:")
    say(f"      {'rule':12s} {'U56':>10s} {'B136':>10s} {'SMALL':>10s}   sign pattern")
    rows0 = []
    for m in MATCH:
        d = [REPRO_1206[(p, "C_ANCHOR")] - REPRO_1206[(p, m)] for p in ("U56", "B136", "SMALL")]
        pat = "".join("+" if x > 0 else "-" for x in d)
        say(f"      {m:12s} {d[0]:>+10.4f} {d[1]:>+10.4f} {d[2]:>+10.4f}   {pat}")
        rows0.append(dict(rule=m, d_U56=d[0], d_B136=d[1], d_SMALL=d[2], pattern=pat))
    pd.DataFrame(rows0).to_csv(f"{OUT}.premise.csv", index=False)
    rev = np.mean([REPRO_1206[("SMALL", m)] for m in ["M_SUBSAMPLE", "M_PAIRWISE", "M_D2"]]) \
        - REPRO_1206[("SMALL", "C_ANCHOR")]
    say(f"    THE REVERSAL UNDER TEST: on SMALL the three count-matched rules average "
        f"{rev:+.4f}")
    say("    of OOS Sharpe ABOVE the do-nothing control, against a pooled gap 1206 measured at")
    say("    +0.0017 with clustered SE 0.0526.  The reversal is ~20x the unresolvable headline.")
    say("")
    say("    WHY TURNOVER IS THE SUSPECT: 1206 found the count-matched rules call CADENCE widest")
    say("    at 0.307-0.314 of picks against M_NONE's 0.0551, and the CADENCE ladder's far rung")
    say("    (monthly) is a TURNOVER CUT.  If the reversal is a cost rebate it must SHRINK to")
    say("    zero as the cost rung goes to 0 bps and must VANISH once turnover is matched.")
    say("")
    say("    PRE-DECLARED OUTCOMES (written before the walk runs):")
    say("      (A) TURNOVER FACT — the SMALL reversal is <= 0.02 at 0 bps AND under T_CHARGE and")
    say("          T_BAND at 10 bps, and grows monotonically with the cost rung.")
    say("      (B) PANEL FACT — the reversal survives at 0 bps AND under both matches at 10 bps")
    say("          (each >= half its T_NONE/10bps size).")
    say("      (C) MIXED — the cost rung and the matches disagree, or the reversal is roughly")
    say("          halved but not removed.")
    say("      (D) DEGENERATE — the matches collapse the move rate to ~0 so there is nothing to")
    say("          compare on SMALL.")
    say("")
    say("    SURVIVORSHIP (rule 9): B136 and SMALL are CURRENT constituents; SMALL is the")
    say("    sub-$2B screen with max_1d_move >= 1.0 tickers dropped.  The reversal under test")
    say("    is a statement about names that survived to the screen date.")

    panels = build_panels()
    panel_names = [p[0] for p in panels]
    kmin_all = min(len(v) for v in LAD.values())

    say("")
    say("=" * 104)
    say("(A) THE BOOK GRID — gross return and turnover stored separately, so any cost rung is")
    say("    an exact linear re-read of one run (G9).")
    say("=" * 104)

    gross_r, turn_r, turn1 = {}, {}, {}      # (panel,key)->array ; (panel,(N,H,f))->array
    ctx = {}
    for pname, px, invest in panels:
        pan = Panel(pname, px, invest)
        i0, ioos = pan.i0, pan.ioos
        spy = px["SPY"].pct_change().fillna(0.0).values
        base_by_cost = {c: backtest(px, rules_v2_weights(px), cost_bps=c,
                                    freq="W")["returns"].fillna(0.0).values for c in COSTS}
        h = len(spy[i0:]) // 2
        ctx[pname] = dict(pan=pan, i0=i0, ioos=ioos, h=h, spy_r=spy, base_by_cost=base_by_cost)
        c_ = ctx[pname]
        s_full = spy[i0:]
        c_["spyT"] = stats3(s_full)
        c_["spyH"] = (sharpe(s_full[:h]), sharpe(s_full[h:]))
        c_["spy_oos"] = stats3(spy[ioos:])
        c_["baseT"] = {c: stats3(base_by_cost[c][i0:]) for c in COSTS}
        c_["baseH"] = {c: (sharpe(base_by_cost[c][i0:][:h]), sharpe(base_by_cost[c][i0:][h:]))
                       for c in COSTS}
        c_["base_oos"] = {c: stats3(base_by_cost[c][ioos:]) for c in COSTS}

        say(f"  {pname:6s} n_invest={len(invest):4d}  SPY {c_['spyT']['CAGR']:.2%} / "
            f"{c_['spyT']['Sharpe']:.4f} / {c_['spyT']['MaxDD']:.2%} "
            f"(halves {c_['spyH'][0]:.4f}/{c_['spyH'][1]:.4f}), OOS {c_['spy_oos']['CAGR']:.2%} / "
            f"{c_['spy_oos']['Sharpe']:.4f} / {c_['spy_oos']['MaxDD']:.2%}")
        say(f"  {'':6s} {'':13s}  LIVE RULES v2 by cost rung: " + "  ".join(
            f"{int(c)}bps {c_['baseT'][c]['Sharpe']:.4f}" for c in COSTS))
        if pname == "U56":
            gates.append(dict(gate="G3 live RULES v2 U56 MaxDD @10bps == record -12.05%",
                              value=c_["baseT"][COST_REF]["MaxDD"], target=LIVE_MAXDD_COMMITTED,
                              pass_=abs(c_["baseT"][COST_REF]["MaxDD"] - LIVE_MAXDD_COMMITTED) < 5e-4))

        selcache = {}

        def sel(N, H, f):
            k = (N, H, f)
            if k not in selcache:
                selcache[k] = build1(pan, N, H, f)
            return selcache[k]

        allkeys = sorted({b for a in ANCHORS.values() for v in ladder_books(a).values() for b in v})
        for key in allkeys:
            N, H, g, f = key
            gr, tu = nrun(pan, g * sel(N, H, f), f)
            gross_r[(pname, key)] = gr
            turn_r[(pname, key)] = tu
        # unit-gross turnover per selection frame (for T_BAND / T_CHARGE)
        for (N, H, f) in sorted({(k[0], k[1], k[3]) for k in allkeys}):
            _, tu1 = nrun(pan, 1.0 * sel(N, H, f), f)
            turn1[(pname, (N, H, f))] = tu1

        if pname == "U56":
            # G1: fast runner net@10 == engine.backtest on the record's anchor
            Wa = A_G * sel(A_N, A_H, A_C)
            Wdec = np.vstack([Wa[1:], np.zeros((1, Wa.shape[1]))])
            eng = backtest(px, pd.DataFrame(Wdec, index=px.index, columns=px.columns),
                           cost_bps=COST_REF, freq=A_C)["returns"].values
            mine = gross_r[(pname, ANCHORS["A_REC"])] - turn_r[(pname, ANCHORS["A_REC"])] * COST_REF / 1e4
            d = float(np.nanmax(np.abs(np.asarray(eng[i0:], float) - mine[i0:])))
            gates.append(dict(gate="G1 fast runner net@10bps == engine.backtest on the anchor",
                              value=d, target=0.0, pass_=d < 1e-9))
            # --- the rejected shortcut, measured and reported (see the docstring)
            NONLIN = 0.0
            for g in LAD["GROSS"]:
                k = (A_N, A_H, g, A_C)
                NONLIN = max(NONLIN, float(np.max(np.abs(
                    turn_r[(pname, k)] - g * turn1[(pname, (A_N, A_H, A_C))]))))
            ctx[pname]["nonlin"] = NONLIN
            # G2: T_CHARGE is the identity on the anchor and on its whole GROSS ladder
            w2 = 0.0
            for g in LAD["GROSS"]:
                k = (A_N, A_H, g, A_C)
                w2 = max(w2, float(np.max(np.abs(
                    turn_r[(pname, k)] - turn_r[(pname, (A_N, A_H, k[2], A_C))]))))
            gates.append(dict(gate="G2 T_CHARGE is the identity on the anchor and its GROSS ladder",
                              value=w2, target=0.0, pass_=w2 == 0.0))
            # G9: net(c) identity vs a direct run charged at c
            gr, tu = nrun(pan, 0.55 * sel(A_N, A_H, A_C), A_C)
            d9 = float(np.max(np.abs((gr - tu * 25.0 / 1e4)
                                     - (gross_r[(pname, (A_N, A_H, 0.55, A_C))]
                                        - turn_r[(pname, (A_N, A_H, 0.55, A_C))] * 25.0 / 1e4))))
            gates.append(dict(gate="G9 net(c) == gross - turn*c/1e4 (re-derived at 25 bps)",
                              value=d9, target=0.0, pass_=d9 < 1e-15))

    say(f"  {len(gross_r)} (panel, book) paths built; "
        f"{len(turn1)} distinct unit-gross selection frames.")

    # ---- the turnover levels themselves: is the SMALL anchor a high-turnover book?
    say("")
    say("  TURNOVER LEVELS (annualised sum of daily turnover over the evaluated span), by panel")
    say("  and anchor, at gross 1.0 — the premise the queue's hypothesis rests on:")
    say(f"    {'panel':6s} " + "  ".join(f"{a:>10s}" for a in ANCHORS) + f" {'CADENCE=M of A_REC':>20s}")
    trows = []
    for pname in panel_names:
        c_ = ctx[pname]
        i0 = c_["i0"]
        vals = []
        for aname, a in ANCHORS.items():
            u = turn1[(pname, (a[0], a[1], a[3]))][i0:]
            v = float(u.sum() * 252 / len(u))
            vals.append(v)
            trows.append(dict(panel=pname, anchor=aname, ann_turnover_unit_gross=v))
        am = (A_N, A_H, "M")
        um = turn1[(pname, am)][i0:]
        vm = float(um.sum() * 252 / len(um))
        trows.append(dict(panel=pname, anchor="A_REC@CADENCE=M", ann_turnover_unit_gross=vm))
        say(f"    {pname:6s} " + "  ".join(f"{v:>10.2f}" for v in vals) + f" {vm:>20.2f}")
    pd.DataFrame(trows).to_csv(f"{OUT}.turnover_levels.csv", index=False)
    say("    (x/yr, one-way units of NAV.  A_REC is weekly; its monthly twin is the CADENCE rung")
    say("     the count-matched rules reach for.)")
    say("")
    say("  THE REJECTED SHORTCUT, MEASURED (see the docstring; G2 rejected it before any result")
    say("  was read).  turn(g) - g*turn(1) on the record's anchor, worst day over the GROSS")
    say(f"  ladder: {ctx['U56']['nonlin']:.6f} of one-way turnover.  Turnover is NOT linear in gross:")
    say("  the drifted weights are renormalised by a portfolio value carrying a 1-g cash sleeve,")
    say("  so the trade needed to restore a position depends on the rung.  Both matches below")
    say("  therefore use BUILT turnover paths only.")

    # ------------------------------------------------ helper: net path under a grid point
    def charge_key(key, anchor):
        """The anchor's SELECTION FRAME read at the book's own gross rung.  Always a built
        book: for the N/H/CADENCE ladders key[2] is the anchor's gross, and for the GROSS
        ladder this is the rung itself (so T_CHARGE is the identity there, G2)."""
        return (anchor[0], anchor[1], key[2], anchor[3])

    def gross_ref_key(key, anchor):
        """The book's SELECTION FRAME read at the anchor's gross rung — the turnover
        measurement T_BAND compares, so the GROSS ladder is not banded out by construction."""
        return (key[0], key[1], anchor[2], key[3])

    def net(pname, key, cost, mode, anchor):
        tu = turn_r[(pname, charge_key(key, anchor) if mode == "T_CHARGE" else key)]
        return gross_r[(pname, key)] - tu * cost / 1e4

    def band_lads(pname, anchor, i_is, i_start, band):
        """Candidate lists restricted to rungs whose IS-window turnover, measured at the
        ANCHOR'S GROSS, is within +/-band of the anchor's.  The anchor is always in its own
        band (ratio exactly 1)."""
        lads = ladder_books(anchor)
        ua = turn_r[(pname, anchor)][i_is:i_start].mean()
        out = {}
        for ln, bks in lads.items():
            keep = []
            for b in bks:
                ub = turn_r[(pname, gross_ref_key(b, anchor))][i_is:i_start].mean()
                rat = (ub / ua) if ua > 0 else 1.0
                if (1.0 / (1.0 + band)) <= rat <= (1.0 + band):
                    keep.append(b)
            if anchor in bks and anchor not in keep:
                keep.append(anchor)
            out[ln] = keep if keep else [anchor]
        return out

    # ------------------------------------------------ ARM B: THE WALK AT EVERY GRID POINT
    say("")
    say("=" * 104)
    say("(B) THE ROLLING WALK, RE-RUN AT EVERY GRID POINT.  Folds are calendar years, IS window")
    say("    ends the day before the fold's first bar, each fold read once.")
    say("=" * 104)
    picks = []
    for pname, px, invest in panels:
        c_ = ctx[pname]
        pan = c_["pan"]
        yr = pan.yr
        for aname, anchor in ANCHORS.items():
            base_lads = ladder_books(anchor)
            allb = sorted({b for v in base_lads.values() for b in v})
            for W in WINDOWS:
                for fy in FOLD_YEARS:
                    i_start = int(np.searchsorted(yr, fy))
                    i_end = int(np.searchsorted(yr, fy + 1))
                    i_is = int(np.searchsorted(yr, fy - W))
                    if i_is < pan.i0 or i_end - i_start < 60:
                        continue
                    for cost in COSTS:
                        npath = {b: net(pname, b, cost, "T_NONE", anchor) for b in allb}
                        cpath = {b: net(pname, b, cost, "T_CHARGE", anchor) for b in allb}
                        for mode in MODES:
                            pth = cpath if mode == "T_CHARGE" else npath
                            lads = (band_lads(pname, anchor, i_is, i_start, BAND)
                                    if mode == "T_BAND" else base_lads)
                            cand = sorted({b for v in lads.values() for b in v})
                            isr = {b: sharpe(pth[b][i_is:i_start]) for b in cand}
                            rng = np.random.default_rng(
                                SEED0 + 1000 * fy + 31 * W + 7 * list(ANCHORS).index(aname)
                                + panel_names.index(pname))
                            for rule in RULES:
                                pick, widest, wsp = choose(rule, lads, isr, rng, kmin_all)
                                key = pick if pick is not None else anchor
                                r = pth[key][i_start:i_end]
                                ut = turn_r[(pname, key)][i_start:i_end]
                                picks.append(dict(
                                    panel=pname, anchor=aname, window=W, fold=fy, cost=cost,
                                    mode=mode, rule=rule, widest=widest, spread=wsp,
                                    moved=bool(key != anchor),
                                    N=key[0], H=key[1], gross=key[2], cadence=key[3],
                                    n_cand=len(cand),
                                    OOS_Sharpe=sharpe(r), OOS_CAGR=cagr(r), OOS_MaxDD=mdd(r),
                                    ann_vol=float(np.std(r, ddof=0) * np.sqrt(252)),
                                    ann_turn=float(ut.sum() * 252 / max(len(ut), 1)),
                                    n_days=len(r), partial=bool(fy == FOLD_YEARS[-1])))
    pdf = pd.DataFrame(picks)
    pdf.to_csv(f"{OUT}.picks.csv", index=False)
    nfolds = pdf.fold.nunique()
    say(f"  {len(pdf)} pick-cells = {len(panel_names)} panels x {len(ANCHORS)} anchors x "
        f"{len(WINDOWS)} windows x {nfolds} folds x {len(COSTS)} costs x {len(MODES)} modes x "
        f"{len(RULES)} rules")
    say(f"  {len(pdf) // (len(COSTS) * len(MODES) * len(RULES))} picks per rule per grid point.")

    # ---- G4: reproduce 1206 exactly at (10 bps, T_NONE)
    ref = pdf[(pdf.cost == COST_REF) & (pdf["mode"] == "T_NONE")]
    worst, rrows = 0.0, []
    for pname in panel_names:
        for rule in RULES:
            v = float(ref[(ref.panel == pname) & (ref["rule"] == rule)].OOS_Sharpe.mean())
            dv = abs(v - REPRO_1206[(pname, rule)])
            worst = max(worst, dv)
            rrows.append(dict(panel=pname, rule=rule, mine=v, committed_1206=REPRO_1206[(pname, rule)],
                              dev=dv))
    pd.DataFrame(rrows).to_csv(f"{OUT}.repro1206.csv", index=False)
    gates.append(dict(gate="G4 1206's BY PANEL means reproduce at (10bps, T_NONE), all 21 cells",
                      value=worst, target=0.0, pass_=worst < 5e-4))
    say(f"  reproduction of 1206's 21 BY PANEL cells at (10 bps, T_NONE): worst dev {worst:.2e}")

    # ---- G5: T_NONE == T_CHARGE at 0 bps
    a = pdf[(pdf.cost == 0.0) & (pdf["mode"] == "T_NONE")].set_index(
        ["panel", "anchor", "window", "fold", "rule"]).OOS_Sharpe.sort_index()
    b = pdf[(pdf.cost == 0.0) & (pdf["mode"] == "T_CHARGE")].set_index(
        ["panel", "anchor", "window", "fold", "rule"]).OOS_Sharpe.sort_index()
    d5 = float(np.nanmax(np.abs(a.values - b.values)))
    gates.append(dict(gate="G5 T_NONE and T_CHARGE coincide exactly at 0 bps", value=d5,
                      target=0.0, pass_=d5 == 0.0))

    # ------------------------------------------------ ARM C: THE REVERSAL AT EVERY GRID POINT
    say("")
    say("=" * 104)
    say("(C) THE HEADLINE — the SMALL reversal at all 12 grid points, with U56 and B136 beside")
    say("    it.  REVERSAL := mean OOS Sharpe of the three count-matched rules (M_SUBSAMPLE,")
    say("    M_PAIRWISE, M_D2) MINUS C_ANCHOR.  Positive = the do-nothing control LOSES.")
    say("=" * 104)
    CM = ["M_SUBSAMPLE", "M_PAIRWISE", "M_D2"]

    KEYS = ["anchor", "window", "fold"]

    def reversal(sub, pname):
        """Mean OOS Sharpe of the three count-matched rules minus C_ANCHOR, with a PAIRED
        delta clustered by fold.  Folds are non-overlapping calendar years and so are the
        independent units; anchors and windows inside a fold are not."""
        s = sub[sub.panel == pname]
        anc = float(s[s["rule"] == "C_ANCHOR"].OOS_Sharpe.mean())
        cm = float(s[s["rule"].isin(CM)].OOS_Sharpe.mean())
        a = s[s["rule"] == "C_ANCHOR"].set_index(KEYS).OOS_Sharpe
        m = s[s["rule"].isin(CM)].groupby(KEYS).OOS_Sharpe.mean()
        d = (m - a.reindex(m.index)).dropna()
        fm = d.groupby(level="fold").mean()
        se = float(fm.std(ddof=1) / np.sqrt(len(fm))) if len(fm) > 1 else np.nan
        t = float(d.mean() / se) if se and np.isfinite(se) and se > 0 else np.nan
        return cm - anc, anc, cm, se, t

    say("    Each delta is PAIRED on (anchor, window, fold) and its SE is clustered by fold")
    say("    (14 non-overlapping calendar years).  1206's unresolvable headline had SE 0.0526.")
    hrows = []
    say("")
    say(f"    {'mode':9s} {'cost':>5s} " + "  ".join(f"{p:>30s}" for p in panel_names)
        + f"  {'SMALL mv':>9s}")
    say(f"    {'':9s} {'':>5s} "
        + "  ".join(f"{'anchor matched   delta    SE     t':>30s}" for _ in panel_names))
    for mode in MODES:
        for cost in COSTS:
            sub = pdf[(pdf.cost == cost) & (pdf["mode"] == mode)]
            cells = []
            for pname in panel_names:
                d, anc, cm, se, t = reversal(sub, pname)
                cells.append(f"{anc:6.4f} {cm:7.4f} {d:+7.4f} {se:6.4f} {t:+5.2f}")
                hrows.append(dict(mode=mode, cost=cost, panel=pname, anchor_mean=anc,
                                  matched_mean=cm, reversal=d, clustered_SE=se, t=t,
                                  resolved_2SE=bool(abs(t) >= 2.0)))
            mr = float(sub[(sub.panel == "SMALL") & (sub["rule"].isin(CM))].moved.mean())
            say(f"    {mode:9s} {int(cost):>5d} " + "  ".join(cells) + f"  {mr:>9.4f}")
    hdf = pd.DataFrame(hrows)
    hdf.to_csv(f"{OUT}.reversal_grid.csv", index=False)
    say("")
    say(f"  RESOLVED AT 2 CLUSTERED SE: SMALL {int(hdf[(hdf.panel == 'SMALL')].resolved_2SE.sum())}"
        f" of 12 grid points;  U56 {int(hdf[(hdf.panel == 'U56')].resolved_2SE.sum())} of 12;  "
        f"B136 {int(hdf[(hdf.panel == 'B136')].resolved_2SE.sum())} of 12.")
    ref_row = hdf[(hdf["mode"] == "T_NONE") & (hdf.cost == COST_REF) & (hdf.panel == "SMALL")].iloc[0]
    need = (2.0 * ref_row.clustered_SE / abs(ref_row.reversal)) ** 2 * nfolds
    say(f"  THE REVERSAL 1206 COMMITTED IS ITSELF UNRESOLVED.  At the reference cell it reads")
    say(f"  {ref_row.reversal:+.4f} with clustered SE {ref_row.clustered_SE:.4f}, t {ref_row.t:+.2f}.  SE falls as")
    say(f"  1/sqrt(folds), so resolving it at 2 SE needs {need:.0f} non-overlapping calendar folds against")
    say(f"  the {nfolds} this tape supplies — about {need - nfolds:.0f} more years of small-cap history.  1206")
    say("  called it 'the largest real effect in the run'; it is the largest UNRESOLVED effect.")

    say("")
    say("  THE SAME, READ AS THE THREE PRE-DECLARED TESTS:")
    r_ref = float(hdf[(hdf["mode"] == "T_NONE") & (hdf.cost == COST_REF)
                      & (hdf.panel == "SMALL")].reversal.iloc[0])
    r_zero = float(hdf[(hdf["mode"] == "T_NONE") & (hdf.cost == 0.0)
                       & (hdf.panel == "SMALL")].reversal.iloc[0])
    r_band = float(hdf[(hdf["mode"] == "T_BAND") & (hdf.cost == COST_REF)
                       & (hdf.panel == "SMALL")].reversal.iloc[0])
    r_chg = float(hdf[(hdf["mode"] == "T_CHARGE") & (hdf.cost == COST_REF)
                      & (hdf.panel == "SMALL")].reversal.iloc[0])
    say(f"    SMALL reversal at the reference cell (10 bps, T_NONE)   {r_ref:+.4f}")
    say(f"    ... at 0 bps (cost channel removed)                     {r_zero:+.4f}  "
        f"({r_zero / r_ref if r_ref else np.nan:.2f}x of reference)")
    say(f"    ... under T_BAND at 10 bps (turnover-matched candidates) {r_band:+.4f}  "
        f"({r_band / r_ref if r_ref else np.nan:.2f}x)")
    say(f"    ... under T_CHARGE at 10 bps (anchor's turnover charged) {r_chg:+.4f}  "
        f"({r_chg / r_ref if r_ref else np.nan:.2f}x)")
    cost_series = [float(hdf[(hdf["mode"] == "T_NONE") & (hdf.cost == c)
                             & (hdf.panel == "SMALL")].reversal.iloc[0]) for c in COSTS]
    mono = all(x <= y + 1e-12 for x, y in zip(cost_series, cost_series[1:]))
    say(f"    SMALL reversal across the cost rungs {COSTS}: "
        + "  ".join(f"{v:+.4f}" for v in cost_series) + f"   monotone in cost: {mono}")
    for pname in ("U56", "B136"):
        cs = [float(hdf[(hdf["mode"] == "T_NONE") & (hdf.cost == c)
                        & (hdf.panel == pname)].reversal.iloc[0]) for c in COSTS]
        say(f"    {pname:5s} reversal across the same rungs:        "
            + "  ".join(f"{v:+.4f}" for v in cs))

    # ---- verdict logic, applied to the pre-declared thresholds
    A_ok = (abs(r_zero) <= 0.02) and (abs(r_band) <= 0.02) and (abs(r_chg) <= 0.02) and mono
    B_ok = (r_zero >= 0.5 * r_ref) and (r_band >= 0.5 * r_ref) and (r_chg >= 0.5 * r_ref)
    mr_all = float(pdf[(pdf["mode"] == "T_BAND") & (pdf.panel == "SMALL")
                       & (pdf["rule"].isin(CM))].moved.mean())
    D_ok = mr_all < 0.02
    answer = "(D) DEGENERATE" if D_ok else ("(A) TURNOVER FACT" if A_ok else
                                            ("(B) PANEL FACT" if B_ok else "(C) MIXED"))
    say("")
    say(f"  PRE-DECLARED OUTCOME SELECTED: {answer}")
    say(f"    (A) test: |0bps|<=0.02 {abs(r_zero) <= 0.02}, |T_BAND|<=0.02 {abs(r_band) <= 0.02}, "
        f"|T_CHARGE|<=0.02 {abs(r_chg) <= 0.02}, monotone {mono}")
    say(f"    (B) test: 0bps>=half {r_zero >= 0.5 * r_ref}, T_BAND>=half {r_band >= 0.5 * r_ref}, "
        f"T_CHARGE>=half {r_chg >= 0.5 * r_ref}")
    say(f"    (D) test: T_BAND SMALL move rate {mr_all:.4f} < 0.02 -> {D_ok}")

    # ---- the mechanism: where do the picks actually go on SMALL?
    say("")
    say("  MECHANISM — share of SMALL picks landing on CADENCE=M, and the realised annualised")
    say("  turnover of the picked book, by rule and grid point:")
    say(f"    {'mode':9s} {'cost':>5s} {'rule':12s} {'share M':>8s} {'ann turn':>9s} "
        f"{'widest=CADENCE':>15s} {'mean OOS Sh':>12s}")
    mrows = []
    for mode in MODES:
        for cost in COSTS:
            for rule in ["C_ANCHOR"] + CM + ["M_NONE"]:
                s = pdf[(pdf.cost == cost) & (pdf["mode"] == mode) & (pdf.panel == "SMALL")
                        & (pdf["rule"] == rule)]
                shm = float((s.cadence == "M").mean())
                at = float(s.ann_turn.mean())
                wc = float((s.widest == "CADENCE").mean())
                ms = float(s.OOS_Sharpe.mean())
                say(f"    {mode:9s} {int(cost):>5d} {rule:12s} {shm:>8.4f} {at:>9.2f} "
                    f"{wc:>15.4f} {ms:>12.4f}")
                mrows.append(dict(mode=mode, cost=cost, rule=rule, share_cadence_M=shm,
                                  ann_turnover=at, widest_is_cadence=wc, mean_OOS_Sharpe=ms))
    pd.DataFrame(mrows).to_csv(f"{OUT}.mechanism.csv", index=False)

    # ---- the exact linear cost attribution (no Sharpe non-linearity involved)
    say("")
    say("  EXACT COST ATTRIBUTION on SMALL at 10 bps, T_NONE: the count-matched rules' picks")
    say("  turn over LESS/MORE than the anchor by this much per year, worth this much of")
    say("  annual mean return at each rung (turnover deltas are exact; Sharpe is not linear):")
    s10 = pdf[(pdf.cost == COST_REF) & (pdf["mode"] == "T_NONE") & (pdf.panel == "SMALL")]
    ta = float(s10[s10["rule"] == "C_ANCHOR"].ann_turn.mean())
    tc = float(s10[s10["rule"].isin(CM)].ann_turn.mean())
    say(f"    anchor {ta:.2f}/yr   count-matched picks {tc:.2f}/yr   delta {tc - ta:+.2f}/yr")
    arows = []
    for c in COSTS:
        drag = (tc - ta) * c / 1e4
        say(f"      at {int(c):>3d} bps the turnover delta is worth {-drag:+.4%} of annual return "
            f"to the count-matched rules")
        arows.append(dict(cost=c, anchor_turn=ta, matched_turn=tc, delta_turn=tc - ta,
                          annual_return_advantage=-drag))
    vol = float(s10[s10["rule"].isin(CM)].ann_vol.mean())
    say(f"    realised annualised vol of the count-matched picks on SMALL: {vol:.2%}")
    say("    A Sharpe gap of X costs X*vol of annual return, so the cost rebate can explain at")
    say("    most this share of the observed reversal:")
    for c in COSTS:
        drag = (tc - ta) * c / 1e4
        say(f"      at {int(c):>3d} bps: rebate {-drag:+.4%} of return = {-drag / vol:+.4f} of Sharpe "
            f"= {abs(drag / vol) / abs(r_ref) if r_ref else np.nan:.2%} of the {r_ref:+.4f} reversal")
        arows[COSTS.index(c)]["sharpe_units"] = -drag / vol
        arows[COSTS.index(c)]["share_of_reversal"] = abs(drag / vol) / abs(r_ref) if r_ref else np.nan
    pd.DataFrame(arows).to_csv(f"{OUT}.attribution.csv", index=False)

    # ---- the two channels, separated
    say("")
    say("  CHANNEL DECOMPOSITION on SMALL — each channel measured AT ZERO COST and at 10 bps.")
    say("  A channel that is a COST effect must be ~0 at 0 bps by construction:")
    say(f"    {'channel':34s} {'at 0 bps':>10s} {'at 10 bps':>10s} {'at 50 bps':>10s}")

    def rv(mode, cost, pname="SMALL"):
        return float(hdf[(hdf["mode"] == mode) & (hdf.cost == cost) & (hdf.panel == pname)]
                     .reversal.iloc[0])
    crows = []
    for label, f_ in [
        ("LEVEL   REV(T_NONE)", lambda c: rv("T_NONE", c)),
        ("CHARGE  REV(T_CHARGE)-REV(T_NONE)", lambda c: rv("T_CHARGE", c) - rv("T_NONE", c)),
        ("REACH   REV(T_BAND)-REV(T_NONE)", lambda c: rv("T_BAND", c) - rv("T_NONE", c)),
    ]:
        vals = [f_(c) for c in (0.0, 10.0, 50.0)]
        say(f"    {label:34s} {vals[0]:>+10.4f} {vals[1]:>+10.4f} {vals[2]:>+10.4f}")
        crows.append(dict(channel=label, at_0=vals[0], at_10=vals[1], at_50=vals[2]))
    pd.DataFrame(crows).to_csv(f"{OUT}.channels.csv", index=False)
    say("    The REACH channel is the candidate set the chooser may reach, not a price: if it")
    say("    reads the same at 0 bps as at 10 bps it carries NO cost content whatsoever.")

    # ---- band sensitivity, reported and never adjudicated on
    say("")
    say("  T_BAND SENSITIVITY (the band is pre-declared at 0.25; these are reported, not used):")
    say(f"    {'band':>6s} {'SMALL reversal':>15s} {'SMALL move rate':>16s} {'mean n_cand':>12s}")
    brows = []
    for band in BAND_SENS:
        if band == BAND:
            s = pdf[(pdf.cost == COST_REF) & (pdf["mode"] == "T_BAND") & (pdf.panel == "SMALL")]
            d = float(s[s["rule"].isin(CM)].OOS_Sharpe.mean()
                      - s[s["rule"] == "C_ANCHOR"].OOS_Sharpe.mean())
            mv = float(s[s["rule"].isin(CM)].moved.mean())
            nc = float(s.n_cand.mean())
        else:
            vals, mvs, ncs = [], [], []
            for pname, px, invest in panels:
                if pname != "SMALL":
                    continue
                pan = ctx[pname]["pan"]
                yr = pan.yr
                for aname, anchor in ANCHORS.items():
                    allb = sorted({b for v in ladder_books(anchor).values() for b in v})
                    for W in WINDOWS:
                        for fy in FOLD_YEARS:
                            i_start = int(np.searchsorted(yr, fy))
                            i_end = int(np.searchsorted(yr, fy + 1))
                            i_is = int(np.searchsorted(yr, fy - W))
                            if i_is < pan.i0 or i_end - i_start < 60:
                                continue
                            pth = {b: net(pname, b, COST_REF, "T_NONE", anchor) for b in allb}
                            lads = band_lads(pname, anchor, i_is, i_start, band)
                            cand = sorted({b for v in lads.values() for b in v})
                            ncs.append(len(cand))
                            isr = {b: sharpe(pth[b][i_is:i_start]) for b in cand}
                            rng = np.random.default_rng(0)
                            a_r = sharpe(pth[anchor][i_start:i_end])
                            for rule in CM:
                                k, _, _ = choose(rule, lads, isr, rng, kmin_all)
                                vals.append(sharpe(pth[k][i_start:i_end]) - a_r)
                                mvs.append(k != anchor)
            d, mv, nc = float(np.mean(vals)), float(np.mean(mvs)), float(np.mean(ncs))
        say(f"    {band:>6.2f} {d:>15.4f} {mv:>16.4f} {nc:>12.2f}")
        brows.append(dict(band=band, SMALL_reversal=d, move_rate=mv, mean_n_cand=nc))
    pd.DataFrame(brows).to_csv(f"{OUT}.band_sens.csv", index=False)

    # ------------------------------------------------ ARM D: RULE 8
    say("")
    say("=" * 104)
    say("(D) RULE 8 — MATCH (with window and anchor) CHOSEN ON FOLDS ENDING 2016 OR EARLIER;")
    say(f"    the 2017-{FOLD_YEARS[-1]} folds read ONCE.  The cost rung is an accounting")
    say("    assumption and is reported at all four rungs, never chosen on.")
    say("=" * 104)
    IS_f = pdf[pdf.fold <= DIAL_IS_LAST]
    OOS_f = pdf[pdf.fold > DIAL_IS_LAST]
    say(f"    IS folds {sorted(IS_f.fold.unique())}   OOS folds {sorted(OOS_f.fold.unique())}")

    say("")
    say("    D1 — THE ANSWER ITSELF, WALKED FORWARD.  The SMALL reversal computed separately on")
    say("    the IS folds and on the OOS folds, at every grid point.  A turnover fact must read")
    say("    the same way in both windows:")
    say(f"      {'mode':9s} {'cost':>5s} {'SMALL IS':>10s} {'SMALL OOS':>10s} {'U56 IS':>9s} "
        f"{'U56 OOS':>9s} {'B136 IS':>9s} {'B136 OOS':>9s}")
    wrows = []
    for mode in MODES:
        for cost in COSTS:
            cells = []
            for pname in ("SMALL", "U56", "B136"):
                for f_ in (IS_f, OOS_f):
                    sub = f_[(f_.cost == cost) & (f_["mode"] == mode) & (f_.panel == pname)]
                    d = float(sub[sub["rule"].isin(CM)].OOS_Sharpe.mean()
                              - sub[sub["rule"] == "C_ANCHOR"].OOS_Sharpe.mean())
                    cells.append(d)
            say(f"      {mode:9s} {int(cost):>5d} {cells[0]:>+10.4f} {cells[1]:>+10.4f} "
                f"{cells[2]:>+9.4f} {cells[3]:>+9.4f} {cells[4]:>+9.4f} {cells[5]:>+9.4f}")
            wrows.append(dict(mode=mode, cost=cost, SMALL_IS=cells[0], SMALL_OOS=cells[1],
                              U56_IS=cells[2], U56_OOS=cells[3], B136_IS=cells[4],
                              B136_OOS=cells[5]))
    pd.DataFrame(wrows).to_csv(f"{OUT}.rule8_reversal.csv", index=False)

    say("")
    say("    D2 — THE LITERAL CHOOSER WALK.  Within each cost rung, each rule's (mode, window,")
    say("    anchor) is the IS-fold argmax of mean fold Sharpe; the OOS folds are then read once:")
    say(f"      {'cost':>5s} {'rule':12s} {'IS-chosen cell':>28s} {'IS mean Sh':>11s} "
        f"{'OOS mean Sh':>12s} {'OOS mean CAGR':>14s} {'OOS mean DD':>12s}")
    w2 = []
    for cost in COSTS:
        for rule in RULES:
            gis = IS_f[(IS_f["rule"] == rule) & (IS_f.cost == cost)].groupby(
                ["mode", "window", "anchor"]).OOS_Sharpe.mean()
            m_, W_, a_ = gis.idxmax()
            o = OOS_f[(OOS_f["rule"] == rule) & (OOS_f.cost == cost) & (OOS_f["mode"] == m_)
                      & (OOS_f.window == W_) & (OOS_f.anchor == a_)]
            say(f"      {int(cost):>5d} {rule:12s} {f'({m_}, {W_}y, {a_})':>28s} "
                f"{gis.max():>11.4f} {o.OOS_Sharpe.mean():>12.4f} {o.OOS_CAGR.mean():>14.2%} "
                f"{o.OOS_MaxDD.mean():>12.2%}")
            w2.append(dict(cost=cost, rule=rule, IS_mode=m_, IS_window=W_, IS_anchor=a_,
                           IS_mean_Sharpe=float(gis.max()),
                           OOS_mean_Sharpe=float(o.OOS_Sharpe.mean()),
                           OOS_mean_CAGR=float(o.OOS_CAGR.mean()),
                           OOS_mean_MaxDD=float(o.OOS_MaxDD.mean()), n_OOS=len(o)))
    pd.DataFrame(w2).to_csv(f"{OUT}.walkforward.csv", index=False)
    say("    Letting each rule choose its own cell confounds the CHOOSER with the ANCHOR, so the")
    say("    matched-cell read is the honest one:")
    say("")
    say("    D3 — MATCHED-CELL OOS read at 10 bps: mean OOS (2017+) fold Sharpe of every rule at")
    say("    ONE (mode, window, anchor) cell, pooled over panels and folds:")
    hdr = "".join(f"{m:>14s}" for m in MODES)
    say(f"      {'rule':12s}" + hdr + "   (window 3y, anchor A_REC)")
    e3 = []
    for rule in RULES:
        vals = []
        for mode in MODES:
            o = OOS_f[(OOS_f["rule"] == rule) & (OOS_f.cost == COST_REF) & (OOS_f["mode"] == mode)
                      & (OOS_f.window == 3) & (OOS_f.anchor == "A_REC")]
            v = float(o.OOS_Sharpe.mean())
            vals.append(v)
            e3.append(dict(rule=rule, mode=mode, cost=COST_REF, window=3, anchor="A_REC",
                           OOS_mean_Sharpe=v, n=len(o)))
        say(f"      {rule:12s}" + "".join(f"{v:>14.4f}" for v in vals))
    pd.DataFrame(e3).to_csv(f"{OUT}.matched_cell.csv", index=False)

    # ------------------------------------------------ ARM E: BOTH KEEP PATHS
    say("")
    say("=" * 104)
    say("(E) BOTH KEEP PATHS (PROTOCOL rule 4) — on every book at every cost rung, and on every")
    say("    stitched chooser curve at every grid point.")
    say("=" * 104)
    books = []
    for pname, px, invest in panels:
        c_ = ctx[pname]
        i0, ioos, h = c_["i0"], c_["ioos"], c_["h"]
        allkeys = sorted({b for a in ANCHORS.values() for v in ladder_books(a).values() for b in v})
        for cost in COSTS:
            bT, bH, bO = c_["baseT"][cost], c_["baseH"][cost], c_["base_oos"][cost]
            for key in allkeys:
                r = gross_r[(pname, key)] - turn_r[(pname, key)] * cost / 1e4
                rf, ros = r[i0:], r[ioos:]
                st, so = stats3(rf), stats3(ros)
                h1, h2 = sharpe(rf[:h]), sharpe(rf[h:])
                books.append(dict(
                    panel=pname, cost=cost, N=key[0], H=key[1], gross=key[2], cadence=key[3],
                    **st, H1=h1, H2=h2, OOS_CAGR=so["CAGR"], OOS_Sharpe=so["Sharpe"],
                    OOS_MaxDD=so["MaxDD"],
                    KEEP_4a=bool(h1 > bH[0] and h2 > bH[1] and st["MaxDD"] >= bT["MaxDD"]),
                    KEEP_4b=bool(h1 > c_["spyH"][0] and h2 > c_["spyH"][1]
                                 and so["Sharpe"] > c_["spy_oos"]["Sharpe"]
                                 and st["MaxDD"] >= DD_CAP * c_["spyT"]["MaxDD"]
                                 and st["CAGR"] >= CAGR_FLOOR * c_["spyT"]["CAGR"]),
                    KEEP_4b_OOS=bool(so["Sharpe"] > c_["spy_oos"]["Sharpe"]
                                     and so["MaxDD"] >= DD_CAP * c_["spy_oos"]["MaxDD"]
                                     and so["CAGR"] >= CAGR_FLOOR * c_["spy_oos"]["CAGR"])))
    bdf = pd.DataFrame(books)
    bdf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"  {len(bdf)} book-readings ({len(bdf) // len(COSTS)} books x {len(COSTS)} cost rungs)")
    say(f"    {'cost':>5s} {'4a':>8s} {'4b full':>9s} {'4b OOS':>8s} {'both':>8s}")
    for cost in COSTS:
        s = bdf[bdf.cost == cost]
        say(f"    {int(cost):>5d} {int(s.KEEP_4a.sum()):>4d}/{len(s):<3d} "
            f"{int(s.KEEP_4b.sum()):>5d}/{len(s):<3d} {int(s.KEEP_4b_OOS.sum()):>4d}/{len(s):<3d} "
            f"{int((s.KEEP_4b & s.KEEP_4b_OOS).sum()):>4d}/{len(s):<3d}")

    stitch = []
    GRP = {k: v.sort_values("fold") for k, v in
           pdf.groupby(["panel", "cost", "mode", "anchor", "window", "rule"], sort=False)}
    for pname, px, invest in panels:
        c_ = ctx[pname]
        yr = c_["pan"].yr
        i_lo = int(np.searchsorted(yr, FOLD_YEARS[0]))
        i_hi = int(np.searchsorted(yr, FOLD_YEARS[-1] + 1))
        i_oos = int(np.searchsorted(yr, 2017))
        spy_s, spy_o = c_["spy_r"][i_lo:i_hi], c_["spy_r"][i_oos:i_hi]
        hh = (i_hi - i_lo) // 2
        spyH = (sharpe(spy_s[:hh]), sharpe(spy_s[hh:]))
        spyT, spyO = stats3(spy_s), stats3(spy_o)
        for cost in COSTS:
            base_s = c_["base_by_cost"][cost][i_lo:i_hi]
            base_o = c_["base_by_cost"][cost][i_oos:i_hi]
            baseH = (sharpe(base_s[:hh]), sharpe(base_s[hh:]))
            baseT, baseO = stats3(base_s), stats3(base_o)
            for mode in MODES:
                for aname, anchor in ANCHORS.items():
                    for W in WINDOWS:
                        for rule in RULES:
                            sub = GRP.get((pname, cost, mode, aname, W, rule))
                            if sub is None or not len(sub):
                                continue
                            segs = []
                            for _, rr in sub.iterrows():
                                i_s = int(np.searchsorted(yr, rr.fold))
                                i_e = int(np.searchsorted(yr, rr.fold + 1))
                                key = (int(rr.N), int(rr.H), float(rr.gross), rr.cadence)
                                segs.append(net(pname, key, cost, mode, anchor)[i_s:i_e])
                            r = np.concatenate(segs)
                            ro = r[-(i_hi - i_oos):]
                            st, so = stats3(r), stats3(ro)
                            h1, h2 = sharpe(r[:len(r) // 2]), sharpe(r[len(r) // 2:])
                            stitch.append(dict(
                                panel=pname, cost=cost, mode=mode, anchor=aname, window=W,
                                rule=rule, n_days=len(r), **st, H1=h1, H2=h2,
                                OOS_CAGR=so["CAGR"], OOS_Sharpe=so["Sharpe"], OOS_MaxDD=so["MaxDD"],
                                SPY_CAGR=spyT["CAGR"], SPY_Sharpe=spyT["Sharpe"],
                                SPY_MaxDD=spyT["MaxDD"], SPY_OOS_CAGR=spyO["CAGR"],
                                SPY_OOS_Sharpe=spyO["Sharpe"], SPY_OOS_MaxDD=spyO["MaxDD"],
                                LIVE_Sharpe=baseT["Sharpe"], LIVE_MaxDD=baseT["MaxDD"],
                                LIVE_OOS_Sharpe=baseO["Sharpe"],
                                KEEP_4a=bool(h1 > baseH[0] and h2 > baseH[1]
                                             and st["MaxDD"] >= baseT["MaxDD"]),
                                KEEP_4b=bool(h1 > spyH[0] and h2 > spyH[1]
                                             and so["Sharpe"] > spyO["Sharpe"]
                                             and st["MaxDD"] >= DD_CAP * spyT["MaxDD"]
                                             and st["CAGR"] >= CAGR_FLOOR * spyT["CAGR"]),
                                KEEP_4b_OOS=bool(so["Sharpe"] > spyO["Sharpe"]
                                                 and so["MaxDD"] >= DD_CAP * spyO["MaxDD"]
                                                 and so["CAGR"] >= CAGR_FLOOR * spyO["CAGR"])))
    sdf = pd.DataFrame(stitch)
    sdf.to_csv(f"{OUT}.stitched.csv", index=False)
    say("")
    say(f"  {len(sdf)} stitched chooser curves ({FOLD_YEARS[0]}-01 to the tape end).")
    say(f"    {'mode':9s} {'cost':>5s} {'mean Sh':>8s} {'mean CAGR':>10s} {'mean DD':>9s} "
        f"{'mean OOS Sh':>12s} {'4a':>8s} {'4b':>8s} {'4b-OOS':>8s}")
    for mode in MODES:
        for cost in COSTS:
            s = sdf[(sdf["mode"] == mode) & (sdf.cost == cost)]
            say(f"    {mode:9s} {int(cost):>5d} {s.Sharpe.mean():>8.4f} {s.CAGR.mean():>10.2%} "
                f"{s.MaxDD.mean():>9.2%} {s.OOS_Sharpe.mean():>12.4f} "
                f"{int(s.KEEP_4a.sum()):>4d}/{len(s):<3d} {int(s.KEEP_4b.sum()):>4d}/{len(s):<3d} "
                f"{int(s.KEEP_4b_OOS.sum()):>4d}/{len(s):<3d}")
    say("")
    say("  BENCHMARKS over the stitched span, per panel (SPY is buy-and-hold and pays no cost):")
    for pname in panel_names:
        s = sdf[(sdf.panel == pname) & (sdf.cost == COST_REF)].iloc[0]
        say(f"    {pname:6s} SPY {s.SPY_CAGR:>7.2%} / {s.SPY_Sharpe:.4f} / {s.SPY_MaxDD:>7.2%}   "
            f"OOS {s.SPY_OOS_CAGR:>7.2%} / {s.SPY_OOS_Sharpe:.4f} / {s.SPY_OOS_MaxDD:>7.2%}   "
            f"LIVE RULES v2 @10bps {s.LIVE_Sharpe:.4f} (OOS {s.LIVE_OOS_Sharpe:.4f})")
    kk = sdf[sdf.KEEP_4b & sdf.KEEP_4b_OOS]
    say("")
    say(f"  stitched curves clearing 4b FULL and 4b OOS: {len(kk)} of {len(sdf)}")
    if len(kk):
        say(f"    by panel: " + "  ".join(f"{p} {int((kk.panel == p).sum())}" for p in panel_names))
        say(f"    by rule:  " + "  ".join(f"{r} {int((kk['rule'] == r).sum())}" for r in RULES))
        say(f"    by cost:  " + "  ".join(f"{int(c)}bps {int((kk.cost == c).sum())}" for c in COSTS))
        say("    best ten by OOS Sharpe:")
        for _, r in kk.sort_values("OOS_Sharpe", ascending=False).head(10).iterrows():
            say(f"      {r.panel:6s} {int(r.cost):>2d}bps {r['mode']:9s} {r.anchor:8s} "
                f"{int(r.window)}y {r['rule']:12s} CAGR {r.CAGR:>6.2%} Sh {r.Sharpe:.4f} "
                f"DD {r.MaxDD:>7.2%} halves {r.H1:.3f}/{r.H2:.3f}  "
                f"OOS {r.OOS_CAGR:>6.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:>7.2%}")
    say("    NOT PROMOTED unless 4a also clears: these are survivors of a 12-cell dial grid x 7")
    say("    rules x 4 anchors x 3 windows x 3 panels, and this run is a DIAGNOSTIC of 1206's")
    say("    panel split, not a search for a book.")

    # ------------------------------------------------ GATES
    say("")
    say("=" * 104)
    say("GATES")
    say("=" * 104)
    tile_ok = True
    for pname, px, invest in panels:
        yr = ctx[pname]["pan"].yr
        bounds = [int(np.searchsorted(yr, f)) for f in FOLD_YEARS] + \
                 [int(np.searchsorted(yr, FOLD_YEARS[-1] + 1))]
        tile_ok &= all(b1 <= b2 for b1, b2 in zip(bounds, bounds[1:]))
        used = sum(bounds[i + 1] - bounds[i] for i in range(len(FOLD_YEARS)))
        tile_ok &= (used == bounds[-1] - bounds[0])
    gates.append(dict(gate="G6 folds tile the evaluation span exactly (no overlap, no gap)",
                      value=float(tile_ok), target=1.0, pass_=bool(tile_ok)))
    amv = float(pdf[pdf["rule"] == "C_ANCHOR"].moved.mean())
    gates.append(dict(gate="G7 C_ANCHOR move rate is exactly 0 at every grid point",
                      value=amv, target=0.0, pass_=amv == 0.0))
    cnt = pdf.groupby(["rule", "cost", "mode"]).size()
    gates.append(dict(gate="G8 paired design balanced (identical pick count per rule x grid point)",
                      value=float(cnt.max() - cnt.min()), target=0.0,
                      pass_=bool(cnt.max() == cnt.min())))
    # G10: under T_BAND the anchor is always a candidate
    ok10 = True
    pan_s = ctx["SMALL"]["pan"]
    for aname, anchor in ANCHORS.items():
        for W in WINDOWS:
            for fy in FOLD_YEARS:
                i_start = int(np.searchsorted(pan_s.yr, fy))
                i_is = int(np.searchsorted(pan_s.yr, fy - W))
                if i_is < pan_s.i0:
                    continue
                lads = band_lads("SMALL", anchor, i_is, i_start, BAND)
                ok10 &= all(anchor in v for k, v in lads.items() if anchor in ladder_books(anchor)[k])
    gates.append(dict(gate="G10 T_BAND always keeps the anchor in every ladder it belongs to",
                      value=float(ok10), target=1.0, pass_=bool(ok10)))
    # G11: 4 matching rules on a 2-rung ladder are a fixed multiple of each other
    v = [0.0, 1.0]
    r2 = {m: spread(v, m, 2) for m in MATCH}
    gates.append(dict(gate="G11 on a 2-rung ladder M_NONE==M_SUBSAMPLE==M_PAIRWISE",
                      value=abs(r2["M_NONE"] - r2["M_PAIRWISE"]) + abs(r2["M_NONE"] - r2["M_SUBSAMPLE"]),
                      target=0.0, pass_=bool(abs(r2["M_NONE"] - r2["M_PAIRWISE"]) < 1e-12
                                             and abs(r2["M_NONE"] - r2["M_SUBSAMPLE"]) < 1e-12)))
    gg = pd.DataFrame(gates)
    gg.to_csv(f"{OUT}.gates.csv", index=False)
    for _, g in gg.iterrows():
        say(f"  [{'PASS' if g.pass_ else 'FAIL'}] {g.gate:72s} value={g.value:.6g} target={g.target:.6g}")
    say(f"  {int(gg.pass_.sum())} of {len(gg)} gates pass")
    say(f"\n  total runtime {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG))
    return bdf, pdf, sdf, hdf, gg


if __name__ == "__main__":
    main()
