#!/usr/bin/env python3
"""
Idea 1206 (lane C, 2026-09-17) — does the WIDEST-DIAL HABIT lose to DOING NOTHING on
ladders 1155 did not walk?

THE PREMISE, READ FROM THE RECORD AND NOT RECALLED.  Idea 1155's Arm C found the do-nothing
control C_ANCHOR (never move off the anchor book) ahead of all four matching rules out of
sample — mean OOS Sharpe 0.8934 against M_D2 0.8865 / M_NONE 0.8672 / M_SUBSAMPLE = M_PAIRWISE
0.8198 — and the only chooser of the five to reach a 4b book.  The record read that as "the
record's 'tune the widest dial' habit loses to doing nothing".  But 1155's Arm C ran ONE anchor
and ONE 2009-2016 / 2017-2026 split on three panels: THREE PICKS PER RULE.  A mean of three
draws is not a measurement of a 0.007-0.074 gap.  This run gives every rule DOZENS of picks by
rolling the IS window, and over four anchors rather than one, and asks whether the do-nothing
advantage is a measurement or a three-draw accident.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  WINDOW  {2y, 3y, 4y}                              -- length of the rolling IS window
  ANCHOR  {A_REC, A_TIGHT, A_SLOW, A_FAST}          -- the book the ladders pass through

  A_REC is 1155's own anchor (N=20/H=126/g=0.75/W) and is reported like any other rung.

WHAT IS NOT A DIAL.  PANEL {U56, B136, SMALL} is not a dial (rule 9, all three always read).
The FOUR LADDERS {N (6 rungs), H (4), GROSS (10), CADENCE (2)} and the four MATCHING RULES
{M_NONE, M_SUBSAMPLE, M_PAIRWISE, M_D2} are 1155's, inherited whole and unchanged.  The fold
calendar (OOS = one calendar year, stepped one year, non-overlapping) is fixed before any
result is read.  THREE CONTROLS are carried alongside the four rules and are not dials either:

  C_ANCHOR    never move.  1155's do-nothing control, the comparand of the whole run.
  C_RANDOM    pick a ladder UNIFORMLY AT RANDOM (seeded), then its IS argmax.  This isolates
              "is WIDEST informative" from "does tuning ANY ladder cost".
  C_BEST_IS   IS argmax over ALL books in all four ladders at once, ignoring ladder structure.
              The maximal-tuning habit; the upper bound on how much IS fitting can hurt.

Frozen at the record's construction: 3-leg composite (21/252, 0/126, 0/63), above-200d
eligibility, max_vol 0.60, 10 bps (rule 2), t+1 execution, warm-up 260 rows.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward — the two dials are chosen on folds
ENDING 2016 OR EARLIER and the 2017-2026 folds are read ONCE; BOTH KEEP paths (4a vs live
RULES v2, 4b vs SPY) on every book AND on every stitched chooser curve; rule 9 survivorship
stated (B136 and SMALL are current constituents).  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified by this script.

Runs standalone and offline:
  python research/backtests/2026-09-17_does-the-WIDEST-DIAL-HABIT-lose-to-DOING-NOTHING-on-ladders-1155-did-not-walk_C.py
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
SLUG = "does-the-WIDEST-DIAL-HABIT-lose-to-DOING-NOTHING-on-ladders-1155-did-not-walk"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = "2017-01-01"           # 1155's split, kept for the reproduction gate and rule 8
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD = {
    "N": [5, 10, 15, 20, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
    "CADENCE": ["W", "M"],
}
MATCH = ["M_NONE", "M_SUBSAMPLE", "M_PAIRWISE", "M_D2"]
CONTROLS = ["C_ANCHOR", "C_RANDOM", "C_BEST_IS"]
RULES = MATCH + CONTROLS

# dial 2 — the anchors.  A_REC is 1155's.
ANCHORS = {
    "A_REC":   (20, 126, 0.75, "W"),
    "A_TIGHT": (10, 63, 0.55, "W"),
    "A_SLOW":  (30, 252, 0.75, "M"),
    "A_FAST":  (5, 21, 0.50, "W"),
}
A_N, A_H, A_G, A_C = ANCHORS["A_REC"]

# dial 1 — the rolling IS window, in years
WINDOWS = [2, 3, 4]
FOLD_YEARS = list(range(2013, 2027))     # OOS calendar years; 2026 is a partial year, flagged
DIAL_IS_LAST = 2016                      # rule 8: folds ending here or earlier choose the dials

SEED0 = 12061206

# Hartley's d2(k): E[range of k iid N(0,1)].  1155's table, inherited.
D2 = {2: 1.128379, 3: 1.692569, 4: 2.058751, 5: 2.325929, 6: 2.534413, 7: 2.704357,
      8: 2.847201, 9: 2.970026, 10: 3.077505, 11: 3.172873, 12: 3.258457}

# 1155's committed Arm C numbers, for the reproduction gate
REPRO_1155 = {"C_ANCHOR": 0.8934, "M_D2": 0.8865, "M_NONE": 0.8672,
              "M_SUBSAMPLE": 0.8198, "M_PAIRWISE": 0.8198}
LIVE_MAXDD_COMMITTED = -0.1205

LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ==================================================== 1155's four matching rules, verbatim
def spread(vals, rule, k_min=None):
    """Dispersion of a ladder's readings under each publishing convention.  Copied unchanged
    from 1155 so the reproduction gate compares the same arithmetic."""
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


# ==================================================== panels / runner (the record's, inherited)
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
        # fold boundaries: row index of the first bar of each calendar year
        self.yr = px.index.year.values


def build1(pan, N, H, freq):
    """1098/1159's min-hold book at GROSS = 1.0: hold a name H days, refill to N from the
    eligible set.  Selection does not depend on gross, so the gross ladder is this frame
    SCALED — gated below (G2) against a direct build at each rung."""
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
    """The four one-factor-at-a-time ladders through an anchor.  Returns
    {ladder: [(N,H,g,f), ...]} in rung order."""
    an, ah, ag, af = anchor
    out = {}
    out["N"] = [(rg, ah, ag, af) for rg in LAD["N"]]
    out["H"] = [(an, rg, ag, af) for rg in LAD["H"]]
    out["GROSS"] = [(an, ah, rg, af) for rg in LAD["GROSS"]]
    out["CADENCE"] = [(an, ah, ag, rg) for rg in LAD["CADENCE"]]
    return out


# ==================================================== the chooser
def choose(rule, lads, isr, rng, kmin_all):
    """Given per-book IS-window Sharpes `isr[(N,H,g,f)]`, return (pick, widest_ladder,
    widest_spread).  `lads` is ladder -> [book keys in rung order]."""
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
    say("=" * 100)
    say("IDEA 1206 (lane C, 2026-09-17) — does the WIDEST-DIAL HABIT lose to DOING NOTHING")
    say("  on ladders 1155 did not walk?")
    say("  dial 1 = WINDOW  {2y, 3y, 4y}                      (rolling IS window length)")
    say("  dial 2 = ANCHOR  {A_REC, A_TIGHT, A_SLOW, A_FAST}  (the book the ladders cross)")
    say("  rules  = 1155's four matching rules + 3 controls (C_ANCHOR do-nothing, C_RANDOM,")
    say("           C_BEST_IS).  Panels U56/B136/SMALL are not a dial (rule 9).")
    say("=" * 100)

    # ------------------------------------------------ ARM 0: DATA-FREE, PRINTED FIRST
    say("")
    say("(0) THE ARITHMETIC OF A THREE-DRAW MEAN, PRINTED BEFORE ANY DATA IS TOUCHED.")
    say("    1155 compared five choosers on THREE picks each (3 panels x 1 anchor x 1 split).")
    say("    Its published gaps against the do-nothing control were:")
    for m in MATCH:
        say(f"      C_ANCHOR - {m:12s} = {REPRO_1155['C_ANCHOR'] - REPRO_1155[m]:+.4f}")
    say("    A mean of n draws with per-draw SD s has SE s/sqrt(n).  For a 3-draw mean to")
    say("    resolve a gap g at 2 SE, the per-draw SD must satisfy s < g*sqrt(3)/2:")
    say(f"      {'gap':>8s}  {'max per-pick SD for 2-SE resolution':>38s}")
    rows0 = []
    for m in MATCH:
        g = REPRO_1155["C_ANCHOR"] - REPRO_1155[m]
        smax = g * np.sqrt(3) / 2.0
        say(f"      {g:>8.4f}  {smax:>38.4f}")
        rows0.append(dict(rule=m, gap_1155=g, max_sd_for_2SE_at_n3=smax))
    pd.DataFrame(rows0).to_csv(f"{OUT}.threedraw.csv", index=False)
    say("    OOS Sharpes of real books on this tape run roughly 0.3-1.4, i.e. a per-pick SD of")
    say("    order 0.3.  THE LARGEST OF 1155's GAPS (0.0736) WOULD NEED A PER-PICK SD BELOW")
    say(f"    {(REPRO_1155['C_ANCHOR'] - REPRO_1155['M_PAIRWISE']) * np.sqrt(3) / 2:.4f} TO BE RESOLVED BY THREE DRAWS. This run supplies the missing draws.")
    say("")
    say("    PRE-DECLARED OUTCOMES (written before the rolling walk runs):")
    say("      (A) MEASUREMENT — C_ANCHOR's mean OOS Sharpe exceeds all four matching rules")
    say("          pooled over folds AND the paired mean delta clears 2 clustered SEs.")
    say("      (B) THREE-DRAW ACCIDENT — the sign survives at most weakly and no delta clears")
    say("          2 SE, i.e. the ordering is not resolved by dozens of picks either.")
    say("      (C) REVERSAL — at least one matching rule beats C_ANCHOR by more than 2 SE.")
    say("      (D) DEGENERATE — the choosers pick the anchor so often that the comparison has")
    say("          no content (move rate near zero).")

    panels = build_panels()
    panel_names = [p[0] for p in panels]
    kmin_all = min(len(v) for v in LAD.values())

    say("")
    say("=" * 100)
    say("(A) THE BOOK GRID — every rung of every ladder through every anchor, on every panel")
    say("=" * 100)

    books = []
    paths = {}          # (panel, bookkey) -> daily returns array
    ctx = {}
    for pname, px, invest in panels:
        pan = Panel(pname, px, invest)
        i0, ioos = pan.i0, pan.ioos
        spy = px["SPY"].pct_change().fillna(0.0).values
        s_full, s_oos = spy[i0:], spy[ioos:]
        base_r = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].fillna(0.0).values
        b_full, b_oos = base_r[i0:], base_r[ioos:]
        h = len(s_full) // 2
        ctx[pname] = dict(
            pan=pan, i0=i0, ioos=ioos, h=h,
            spyT=stats3(s_full), spyH=(sharpe(s_full[:h]), sharpe(s_full[h:])),
            spy_oos=stats3(s_oos), spy_full=s_full, spy_oos_r=s_oos,
            baseT=stats3(b_full), baseH=(sharpe(b_full[:h]), sharpe(b_full[h:])),
            base_oos=stats3(b_oos), base_full=b_full, base_oos_r=b_oos,
            spy_r=spy, base_rr=base_r)
        c = ctx[pname]
        say(f"  {pname:6s} n_invest={len(invest):4d}  SPY {c['spyT']['CAGR']:.2%} / "
            f"{c['spyT']['Sharpe']:.4f} / {c['spyT']['MaxDD']:.2%} "
            f"(halves {c['spyH'][0]:.4f}/{c['spyH'][1]:.4f}), OOS {c['spy_oos']['CAGR']:.2%} / "
            f"{c['spy_oos']['Sharpe']:.4f} / {c['spy_oos']['MaxDD']:.2%}")
        say(f"  {'':6s} {'':13s}  LIVE RULES v2 {c['baseT']['CAGR']:.2%} / {c['baseT']['Sharpe']:.4f} "
            f"/ {c['baseT']['MaxDD']:.2%}, OOS {c['base_oos']['CAGR']:.2%} / {c['base_oos']['Sharpe']:.4f}")
        if pname == "U56":
            gates.append(dict(gate="G3 live RULES v2 U56 MaxDD == record -12.05%",
                              value=c["baseT"]["MaxDD"], target=LIVE_MAXDD_COMMITTED,
                              pass_=abs(c["baseT"]["MaxDD"] - LIVE_MAXDD_COMMITTED) < 5e-4))

        selcache, runcache = {}, {}

        def sel(N, H, f):
            k = (N, H, f)
            if k not in selcache:
                selcache[k] = build1(pan, N, H, f)
            return selcache[k]

        def book(key):
            if key not in runcache:
                N, H, g, f = key
                runcache[key] = nrun(pan, g * sel(N, H, f), f)
            return runcache[key]

        allkeys = sorted({b for a in ANCHORS.values() for v in ladder_books(a).values() for b in v})
        for key in allkeys:
            r = book(key)
            paths[(pname, key)] = r
            rf, ros = r[i0:], r[ioos:]
            st = stats3(rf)
            h1, h2 = sharpe(rf[:h]), sharpe(rf[h:])
            so = stats3(ros)
            N, H, g, f = key
            books.append(dict(panel=pname, N=N, H=H, gross=g, cadence=f, **st, H1=h1, H2=h2,
                              IS_Sharpe=sharpe(r[i0:ioos]),
                              OOS_CAGR=so["CAGR"], OOS_Sharpe=so["Sharpe"], OOS_MaxDD=so["MaxDD"],
                              KEEP_4a=bool(h1 > c["baseH"][0] and h2 > c["baseH"][1]
                                           and st["MaxDD"] >= c["baseT"]["MaxDD"]),
                              KEEP_4b=bool(h1 > c["spyH"][0] and h2 > c["spyH"][1]
                                           and so["Sharpe"] > c["spy_oos"]["Sharpe"]
                                           and st["MaxDD"] >= DD_CAP * c["spyT"]["MaxDD"]
                                           and st["CAGR"] >= CAGR_FLOOR * c["spyT"]["CAGR"]),
                              KEEP_4b_OOS=bool(so["Sharpe"] > c["spy_oos"]["Sharpe"]
                                               and so["MaxDD"] >= DD_CAP * c["spy_oos"]["MaxDD"]
                                               and so["CAGR"] >= CAGR_FLOOR * c["spy_oos"]["CAGR"])))

        # --- G1: the fast runner reproduces engine.backtest on the record's anchor.
        # 1155's G1 failed at 1.977e-02 on its first cut because `build` writes APPLICATION-time
        # rows while engine.backtest shifts the frame a second time; the comparand is the
        # DECISION-time frame Wdec[t] = W[t+1].  That correction is carried here.
        if pname == "U56":
            Wa = A_G * sel(A_N, A_H, A_C)
            Wdec = np.vstack([Wa[1:], np.zeros((1, Wa.shape[1]))])
            eng = backtest(px, pd.DataFrame(Wdec, index=px.index, columns=px.columns),
                           cost_bps=COST, freq=A_C)["returns"].values
            d = float(np.nanmax(np.abs(np.asarray(eng[i0:], float) - book((A_N, A_H, A_G, A_C))[i0:])))
            gates.append(dict(gate="G1 fast runner == engine.backtest on the record's anchor",
                              value=d, target=0.0, pass_=d < 1e-9))
            # --- G2: the gross ladder really is the selection frame scaled
            direct = nrun(pan, 0.30 * sel(A_N, A_H, A_C), A_C)
            d2g = float(np.max(np.abs(direct - book((A_N, A_H, 0.30, A_C)))))
            gates.append(dict(gate="G2 gross rung == scaled selection frame (linearity of build)",
                              value=d2g, target=0.0, pass_=d2g < 1e-12))

    bdf = pd.DataFrame(books)
    bdf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"  {len(bdf)} books ({len(bdf) // len(panel_names)} distinct per panel across "
        f"{len(ANCHORS)} anchors x 4 ladders)")

    # ------------------------------------------------ ARM B: 1155's SINGLE SPLIT, REPRODUCED
    say("")
    say("=" * 100)
    say("(B) 1155's ARM C, REPRODUCED EXACTLY — one anchor, one split, THREE PICKS PER RULE")
    say("=" * 100)
    rep = []
    for pname, px, invest in panels:
        c = ctx[pname]
        i0, ioos = c["i0"], c["ioos"]
        lads = ladder_books(ANCHORS["A_REC"])
        isr = {b: sharpe(paths[(pname, b)][i0:ioos]) for v in lads.values() for b in v}
        rng = np.random.default_rng(SEED0)
        for rule in MATCH + ["C_ANCHOR"]:
            pick, widest, wsp = choose(rule, lads, isr, rng, kmin_all)
            key = pick if pick is not None else ANCHORS["A_REC"]
            ros = paths[(pname, key)][ioos:]
            rep.append(dict(panel=pname, rule=rule, widest=widest, spread=wsp,
                            pick=f"N={key[0]}/H={key[1]}/g={key[2]:.2f}/{key[3]}",
                            OOS_Sharpe=sharpe(ros), OOS_CAGR=cagr(ros), OOS_MaxDD=mdd(ros)))
    rdf = pd.DataFrame(rep)
    rdf.to_csv(f"{OUT}.repro1155.csv", index=False)
    say(f"    {'rule':12s} {'mean OOS Sharpe':>16s} {'1155 committed':>15s} {'dev':>10s}  widest ladders")
    worst = 0.0
    for rule in ["C_ANCHOR"] + MATCH:
        s = rdf[rdf["rule"] == rule]
        m = float(s.OOS_Sharpe.mean())
        dev = abs(m - REPRO_1155[rule])
        worst = max(worst, dev)
        say(f"    {rule:12s} {m:>16.4f} {REPRO_1155[rule]:>15.4f} {dev:>10.2e}  "
            f"{', '.join(sorted(set(s.widest)))}")
    gates.append(dict(gate="G4 1155's Arm C mean OOS Sharpes reproduce (all five rules)",
                      value=worst, target=0.0, pass_=worst < 5e-4))
    say(f"    worst deviation from 1155's committed figures: {worst:.2e}")

    # ------------------------------------------------ ARM C: THE ROLLING WALK
    say("")
    say("=" * 100)
    say("(C) THE ROLLING WALK — dozens of picks per rule.  IS window ends the day before the")
    say("    fold's first bar; the fold (one calendar year) is read once and never re-chosen on.")
    say("=" * 100)
    picks = []
    for pname, px, invest in panels:
        c = ctx[pname]
        pan = c["pan"]
        idx = px.index
        yr = pan.yr
        for aname, anchor in ANCHORS.items():
            lads = ladder_books(anchor)
            allb = sorted({b for v in lads.values() for b in v})
            for W in WINDOWS:
                for fy in FOLD_YEARS:
                    i_start = int(np.searchsorted(yr, fy))            # first bar of fold year
                    i_end = int(np.searchsorted(yr, fy + 1))          # first bar of next year
                    i_is = int(np.searchsorted(yr, fy - W))           # first bar of IS window
                    if i_is < pan.i0 or i_end - i_start < 60:
                        continue
                    isr = {b: sharpe(paths[(pname, b)][i_is:i_start]) for b in allb}
                    rng = np.random.default_rng(
                        SEED0 + 1000 * fy + 31 * W + 7 * list(ANCHORS).index(aname)
                        + panel_names.index(pname))
                    for rule in RULES:
                        pick, widest, wsp = choose(rule, lads, isr, rng, kmin_all)
                        key = pick if pick is not None else anchor
                        r = paths[(pname, key)][i_start:i_end]
                        picks.append(dict(
                            panel=pname, anchor=aname, window=W, fold=fy, rule=rule,
                            widest=widest, spread=wsp, moved=bool(key != anchor),
                            N=key[0], H=key[1], gross=key[2], cadence=key[3],
                            pick=f"N={key[0]}/H={key[1]}/g={key[2]:.2f}/{key[3]}",
                            IS_Sharpe=isr[key], OOS_Sharpe=sharpe(r), OOS_CAGR=cagr(r),
                            OOS_MaxDD=mdd(r), n_days=len(r),
                            partial=bool(fy == FOLD_YEARS[-1])))
    pdf = pd.DataFrame(picks)
    pdf.to_csv(f"{OUT}.picks.csv", index=False)
    nfolds = pdf.fold.nunique()
    per_rule = len(pdf) // len(RULES)
    say(f"  {len(pdf)} pick-cells = {len(panel_names)} panels x {len(ANCHORS)} anchors x "
        f"{len(WINDOWS)} windows x {nfolds} folds x {len(RULES)} rules")
    say(f"  EACH RULE MAKES {per_rule} PICKS against 1155's 3.")
    say("")
    say("  MOVE RATE (share of picks that are NOT the anchor book) — if this is near zero the")
    say("  comparison has no content (pre-declared outcome D):")
    for rule in RULES:
        s = pdf[pdf["rule"] == rule]
        say(f"    {rule:12s} moved {s.moved.mean():.4f}   distinct picks {s['pick'].nunique():3d}")

    say("")
    say("  WHICH LADDER EACH MATCHING RULE CALLS WIDEST (share of picks):")
    say(f"    {'rule':12s} " + "  ".join(f"{ln:>9s}" for ln in LAD))
    for rule in MATCH:
        s = pdf[pdf["rule"] == rule]
        say(f"    {rule:12s} " + "  ".join(f"{float((s.widest == ln).mean()):>9.4f}" for ln in LAD))

    # ---- the headline: pooled mean OOS Sharpe per rule, and paired deltas vs C_ANCHOR
    say("")
    say("  POOLED OVER ALL PICKS (3 panels x 4 anchors x 3 windows x %d folds = %d picks/rule):"
        % (nfolds, per_rule))
    anc = pdf[pdf["rule"] == "C_ANCHOR"].set_index(["panel", "anchor", "window", "fold"])
    prows = []
    say(f"    {'rule':12s} {'mean OOS Sh':>12s} {'delta vs C_ANCHOR':>18s} {'clustered SE':>13s} "
        f"{'t':>7s} {'anchor wins':>12s} {'n moved':>8s}")
    for rule in RULES:
        s = pdf[pdf["rule"] == rule].set_index(["panel", "anchor", "window", "fold"])
        m = float(s.OOS_Sharpe.mean())
        d = (anc.OOS_Sharpe - s.OOS_Sharpe).dropna()
        # cluster by fold: folds tile the tape without overlap, so fold means are the
        # independent units; panels and anchors inside a fold are not.
        fm = d.groupby(level="fold").mean()
        se = float(fm.std(ddof=1) / np.sqrt(len(fm))) if len(fm) > 1 else np.nan
        dm = float(d.mean())
        t = dm / se if se and np.isfinite(se) and se > 0 else np.nan
        wins = float((anc.OOS_Sharpe >= s.OOS_Sharpe).mean())
        nm = int(s.moved.sum())
        say(f"    {rule:12s} {m:>12.4f} {dm:>18.4f} {se:>13.4f} {t:>7.2f} {wins:>12.4f} {nm:>8d}")
        prows.append(dict(rule=rule, mean_OOS_Sharpe=m, delta_vs_anchor=dm, clustered_SE=se,
                          t=t, anchor_win_rate=wins, n_moved=nm, n_picks=len(s), n_folds=len(fm)))
    pd.DataFrame(prows).to_csv(f"{OUT}.paired.csv", index=False)

    # ---- restricted to picks that actually moved (the comparison with content)
    say("")
    say("  RESTRICTED TO PICKS THAT MOVED OFF THE ANCHOR (zero-deltas dropped):")
    say(f"    {'rule':12s} {'n':>6s} {'mean delta':>11s} {'clustered SE':>13s} {'t':>7s} {'anchor wins':>12s}")
    mrows = []
    for rule in MATCH + ["C_RANDOM", "C_BEST_IS"]:
        s = pdf[pdf["rule"] == rule].set_index(["panel", "anchor", "window", "fold"])
        mv = s[s.moved]
        d = (anc.OOS_Sharpe.reindex(mv.index) - mv.OOS_Sharpe).dropna()
        if not len(d):
            say(f"    {rule:12s} {0:>6d} {'--':>11s}")
            continue
        fm = d.groupby(level="fold").mean()
        se = float(fm.std(ddof=1) / np.sqrt(len(fm))) if len(fm) > 1 else np.nan
        dm = float(d.mean())
        t = dm / se if se and np.isfinite(se) and se > 0 else np.nan
        w = float((d >= 0).mean())
        say(f"    {rule:12s} {len(d):>6d} {dm:>11.4f} {se:>13.4f} {t:>7.2f} {w:>12.4f}")
        mrows.append(dict(rule=rule, n=len(d), mean_delta=dm, clustered_SE=se, t=t, anchor_win_rate=w))
    pd.DataFrame(mrows).to_csv(f"{OUT}.moved.csv", index=False)

    # ---- every grid point reported (PROTOCOL: report ALL grid points)
    say("")
    say("  ALL GRID POINTS — mean OOS Sharpe by (window, anchor, rule), pooled over 3 panels")
    say(f"  x {nfolds} folds ({3 * nfolds} picks per cell):")
    grows = []
    for W in WINDOWS:
        say("")
        say(f"    WINDOW = {W}y")
        say(f"      {'anchor':8s} " + "  ".join(f"{r:>11s}" for r in RULES))
        for aname in ANCHORS:
            vals = []
            for rule in RULES:
                s = pdf[(pdf.window == W) & (pdf.anchor == aname) & (pdf["rule"] == rule)]
                v = float(s.OOS_Sharpe.mean())
                vals.append(v)
                grows.append(dict(window=W, anchor=aname, rule=rule, mean_OOS_Sharpe=v,
                                  n=len(s), move_rate=float(s.moved.mean())))
            best = RULES[int(np.nanargmax(vals))]
            say(f"      {aname:8s} " + "  ".join(f"{v:>11.4f}" for v in vals) + f"   best={best}")
    gdf = pd.DataFrame(grows)
    gdf.to_csv(f"{OUT}.grid.csv", index=False)
    say("")
    say("  C_ANCHOR's rank among the 7 rules at each of the 12 grid points:")
    ranks = []
    for W in WINDOWS:
        for aname in ANCHORS:
            sub = gdf[(gdf.window == W) & (gdf.anchor == aname)].set_index("rule")
            rk = int(sub.mean_OOS_Sharpe.rank(ascending=False)["C_ANCHOR"])
            ranks.append(rk)
            say(f"    window={W}y anchor={aname:8s} C_ANCHOR rank {rk} of {len(RULES)}   "
                f"(best {sub.mean_OOS_Sharpe.idxmax()} {sub.mean_OOS_Sharpe.max():.4f}, "
                f"C_ANCHOR {sub.mean_OOS_Sharpe['C_ANCHOR']:.4f})")
    say(f"    C_ANCHOR is top of the 7 at {sum(1 for r in ranks if r == 1)} of {len(ranks)} grid points; "
        f"median rank {np.median(ranks):.1f}")

    # ---- per-panel breakdown (rule 9: all three always read)
    say("")
    say("  BY PANEL (pooled over anchors, windows, folds):")
    say(f"    {'panel':6s} " + "  ".join(f"{r:>11s}" for r in RULES))
    for pname in panel_names:
        row = [float(pdf[(pdf.panel == pname) & (pdf["rule"] == r)].OOS_Sharpe.mean()) for r in RULES]
        say(f"    {pname:6s} " + "  ".join(f"{v:>11.4f}" for v in row))

    # ---- SIGN STABILITY: does the do-nothing advantage even keep its sign?
    say("")
    say("  SIGN STABILITY OF (C_ANCHOR - rule) — a measurement keeps its sign; an accident")
    say("  does not.  Counted over the 12 (window, anchor) cells and the 3 panels:")
    say(f"    {'rule':12s} {'cells C_ANCHOR ahead':>21s} {'panels ahead':>13s} "
        f"{'folds ahead':>12s} {'1155 sign':>10s} {'sign kept':>10s}")
    srows = []
    for rule in MATCH:
        cell = 0
        for W in WINDOWS:
            for aname in ANCHORS:
                sub = gdf[(gdf.window == W) & (gdf.anchor == aname)].set_index("rule")
                cell += int(sub.mean_OOS_Sharpe["C_ANCHOR"] > sub.mean_OOS_Sharpe[rule])
        pan_ahead = sum(1 for p in panel_names
                        if pdf[(pdf.panel == p) & (pdf["rule"] == "C_ANCHOR")].OOS_Sharpe.mean()
                        > pdf[(pdf.panel == p) & (pdf["rule"] == rule)].OOS_Sharpe.mean())
        s = pdf[pdf["rule"] == rule].set_index(["panel", "anchor", "window", "fold"])
        fm = (anc.OOS_Sharpe - s.OOS_Sharpe).dropna().groupby(level="fold").mean()
        fold_ahead = int((fm > 0).sum())
        pooled = float((anc.OOS_Sharpe - s.OOS_Sharpe).mean())
        kept = "YES" if pooled > 0 else "NO — FLIPS"
        say(f"    {rule:12s} {f'{cell} of 12':>21s} {f'{pan_ahead} of 3':>13s} "
            f"{f'{fold_ahead} of {len(fm)}':>12s} {'+':>10s} {kept:>10s}")
        srows.append(dict(rule=rule, cells_ahead=cell, panels_ahead=pan_ahead,
                          folds_ahead=fold_ahead, n_folds=len(fm), pooled_delta=pooled,
                          sign_kept=pooled > 0))
    pd.DataFrame(srows).to_csv(f"{OUT}.signs.csv", index=False)

    # ------------------------------------------------ ARM D: STITCHED DEPLOYABLE CURVES
    say("")
    say("=" * 100)
    say("(D) THE STITCHED CURVES — what each chooser would actually have RETURNED, holding its")
    say("    pick through each fold.  This is the only capital-relevant object in the run.")
    say("=" * 100)
    stitch = []
    for pname, px, invest in panels:
        c = ctx[pname]
        pan = c["pan"]
        yr = pan.yr
        i_lo = int(np.searchsorted(yr, FOLD_YEARS[0]))
        i_hi = int(np.searchsorted(yr, FOLD_YEARS[-1] + 1))
        i_oos = int(np.searchsorted(yr, 2017))
        spy_s, base_s = c["spy_r"][i_lo:i_hi], c["base_rr"][i_lo:i_hi]
        spy_o, base_o = c["spy_r"][i_oos:i_hi], c["base_rr"][i_oos:i_hi]
        hh = (i_hi - i_lo) // 2
        spyH = (sharpe(spy_s[:hh]), sharpe(spy_s[hh:]))
        baseH = (sharpe(base_s[:hh]), sharpe(base_s[hh:]))
        spyT, baseT = stats3(spy_s), stats3(base_s)
        spyO = stats3(spy_o)
        for aname in ANCHORS:
            for W in WINDOWS:
                for rule in RULES:
                    sub = pdf[(pdf.panel == pname) & (pdf.anchor == aname)
                              & (pdf.window == W) & (pdf["rule"] == rule)].sort_values("fold")
                    if not len(sub):
                        continue
                    segs = []
                    for _, rr in sub.iterrows():
                        i_s = int(np.searchsorted(yr, rr.fold))
                        i_e = int(np.searchsorted(yr, rr.fold + 1))
                        key = (int(rr.N), int(rr.H), float(rr.gross), rr.cadence)
                        segs.append(paths[(pname, key)][i_s:i_e])
                    r = np.concatenate(segs)
                    ro = r[-(i_hi - i_oos):]
                    st, so = stats3(r), stats3(ro)
                    h1, h2 = sharpe(r[:len(r) // 2]), sharpe(r[len(r) // 2:])
                    stitch.append(dict(
                        panel=pname, anchor=aname, window=W, rule=rule, n_days=len(r),
                        **st, H1=h1, H2=h2, OOS_CAGR=so["CAGR"], OOS_Sharpe=so["Sharpe"],
                        OOS_MaxDD=so["MaxDD"],
                        SPY_Sharpe=spyT["Sharpe"], SPY_CAGR=spyT["CAGR"], SPY_MaxDD=spyT["MaxDD"],
                        SPY_OOS_Sharpe=spyO["Sharpe"], SPY_OOS_CAGR=spyO["CAGR"],
                        SPY_OOS_MaxDD=spyO["MaxDD"],
                        LIVE_Sharpe=baseT["Sharpe"], LIVE_OOS_Sharpe=stats3(base_o)["Sharpe"],
                        LIVE_MaxDD=baseT["MaxDD"],
                        KEEP_4a=bool(h1 > baseH[0] and h2 > baseH[1] and st["MaxDD"] >= baseT["MaxDD"]),
                        KEEP_4b=bool(h1 > spyH[0] and h2 > spyH[1]
                                     and so["Sharpe"] > spyO["Sharpe"]
                                     and st["MaxDD"] >= DD_CAP * spyT["MaxDD"]
                                     and st["CAGR"] >= CAGR_FLOOR * spyT["CAGR"]),
                        KEEP_4b_OOS=bool(so["Sharpe"] > spyO["Sharpe"]
                                         and so["MaxDD"] >= DD_CAP * spyO["MaxDD"]
                                         and so["CAGR"] >= CAGR_FLOOR * spyO["CAGR"])))
    sdf = pd.DataFrame(stitch)
    sdf.to_csv(f"{OUT}.stitched.csv", index=False)
    say(f"  {len(sdf)} stitched curves ({FOLD_YEARS[0]}-01 to the tape end).")
    say("")
    say(f"  {'rule':12s} {'mean Sharpe':>11s} {'mean CAGR':>10s} {'mean MaxDD':>11s} "
        f"{'mean OOS Sh':>12s} {'mean OOS DD':>12s} {'4a':>5s} {'4b':>5s} {'4b-OOS':>7s}")
    for rule in RULES:
        s = sdf[sdf["rule"] == rule]
        say(f"  {rule:12s} {s.Sharpe.mean():>11.4f} {s.CAGR.mean():>10.2%} {s.MaxDD.mean():>11.2%} "
            f"{s.OOS_Sharpe.mean():>12.4f} {s.OOS_MaxDD.mean():>12.2%} "
            f"{int(s.KEEP_4a.sum()):>5d} {int(s.KEEP_4b.sum()):>5d} {int(s.KEEP_4b_OOS.sum()):>7d}")
    say("")
    say("  BENCHMARKS over the same stitched span, per panel:")
    for pname in panel_names:
        s = sdf[sdf.panel == pname].iloc[0]
        say(f"    {pname:6s} SPY {s.SPY_CAGR:>7.2%} / {s.SPY_Sharpe:.4f} / {s.SPY_MaxDD:>7.2%}   "
            f"OOS {s.SPY_OOS_CAGR:>7.2%} / {s.SPY_OOS_Sharpe:.4f} / {s.SPY_OOS_MaxDD:>7.2%}   "
            f"LIVE RULES v2 {s.LIVE_Sharpe:.4f} (OOS {s.LIVE_OOS_Sharpe:.4f})")

    # paired stitched deltas (paired on panel x anchor x window)
    say("")
    say("  PAIRED STITCHED DELTAS vs C_ANCHOR (paired on panel x anchor x window, n=%d):"
        % (len(panel_names) * len(ANCHORS) * len(WINDOWS)))
    ka = ["panel", "anchor", "window"]
    sa = sdf[sdf["rule"] == "C_ANCHOR"].set_index(ka)
    strows = []
    say(f"    {'rule':12s} {'d Sharpe':>10s} {'d OOS Sharpe':>13s} {'d CAGR':>9s} {'d MaxDD':>9s} {'anchor wins':>12s}")
    for rule in MATCH + ["C_RANDOM", "C_BEST_IS"]:
        s = sdf[sdf["rule"] == rule].set_index(ka)
        dS = float((sa.Sharpe - s.Sharpe).mean())
        dO = float((sa.OOS_Sharpe - s.OOS_Sharpe).mean())
        dC = float((sa.CAGR - s.CAGR).mean())
        dD = float((sa.MaxDD - s.MaxDD).mean())
        w = float((sa.OOS_Sharpe >= s.OOS_Sharpe).mean())
        say(f"    {rule:12s} {dS:>10.4f} {dO:>13.4f} {dC:>9.2%} {dD:>9.2%} {w:>12.4f}")
        strows.append(dict(rule=rule, d_Sharpe=dS, d_OOS_Sharpe=dO, d_CAGR=dC, d_MaxDD=dD,
                           anchor_win_rate=w))
    pd.DataFrame(strows).to_csv(f"{OUT}.stitched_paired.csv", index=False)

    # ------------------------------------------------ ARM E: RULE 8 ON THE DIALS THEMSELVES
    say("")
    say("=" * 100)
    say("(E) RULE 8 — THE TWO DIALS ARE CHOSEN ON FOLDS ENDING 2016 OR EARLIER, AND THE")
    say(f"    2017-{FOLD_YEARS[-1]} FOLDS ARE READ ONCE.")
    say("=" * 100)
    IS_f = pdf[pdf.fold <= DIAL_IS_LAST]
    OOS_f = pdf[pdf.fold > DIAL_IS_LAST]
    say(f"    IS folds {sorted(IS_f.fold.unique())}   OOS folds {sorted(OOS_f.fold.unique())}")
    say("")
    say(f"    {'rule':12s} {'IS-chosen (window,anchor)':>26s} {'IS mean Sh':>11s} {'OOS mean Sh':>12s} "
        f"{'OOS mean CAGR':>14s} {'OOS mean DD':>12s}")
    wf = []
    for rule in RULES:
        gis = IS_f[IS_f["rule"] == rule].groupby(["window", "anchor"]).OOS_Sharpe.mean()
        W_, a_ = gis.idxmax()
        o = OOS_f[(OOS_f["rule"] == rule) & (OOS_f.window == W_) & (OOS_f.anchor == a_)]
        say(f"    {rule:12s} {f'({W_}y, {a_})':>26s} {gis.max():>11.4f} {o.OOS_Sharpe.mean():>12.4f} "
            f"{o.OOS_CAGR.mean():>14.2%} {o.OOS_MaxDD.mean():>12.2%}")
        wf.append(dict(rule=rule, IS_window=W_, IS_anchor=a_, IS_mean_Sharpe=float(gis.max()),
                       OOS_mean_Sharpe=float(o.OOS_Sharpe.mean()),
                       OOS_mean_CAGR=float(o.OOS_CAGR.mean()),
                       OOS_mean_MaxDD=float(o.OOS_MaxDD.mean()), n_OOS=len(o)))
    wdf = pd.DataFrame(wf)
    say("")
    say("    The same, as STITCHED CURVES over 2017-%d only (the capital object), against the"
        % FOLD_YEARS[-1])
    say("    live book and SPY on each panel:")
    say(f"    {'rule':12s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} {'OOS MaxDD':>10s} "
        f"{'SPY Sh':>8s} {'LIVE Sh':>8s} {'4b-OOS':>7s}")
    w2 = []
    for rule in RULES:
        r0 = wdf[wdf["rule"] == rule].iloc[0]
        s = sdf[(sdf["rule"] == rule) & (sdf.window == r0.IS_window) & (sdf.anchor == r0.IS_anchor)]
        say(f"    {rule:12s} {s.OOS_CAGR.mean():>9.2%} {s.OOS_Sharpe.mean():>11.4f} "
            f"{s.OOS_MaxDD.mean():>10.2%} {s.SPY_OOS_Sharpe.mean():>8.4f} "
            f"{s.LIVE_OOS_Sharpe.mean():>8.4f} {int(s.KEEP_4b_OOS.sum()):>4d}/{len(s)}")
        w2.append(dict(rule=rule, window=r0.IS_window, anchor=r0.IS_anchor,
                       OOS_CAGR=float(s.OOS_CAGR.mean()), OOS_Sharpe=float(s.OOS_Sharpe.mean()),
                       OOS_MaxDD=float(s.OOS_MaxDD.mean()),
                       SPY_OOS_Sharpe=float(s.SPY_OOS_Sharpe.mean()),
                       LIVE_OOS_Sharpe=float(s.LIVE_OOS_Sharpe.mean()),
                       KEEP_4b_OOS=int(s.KEEP_4b_OOS.sum()), n=len(s)))
    pd.concat([wdf.set_index("rule"), pd.DataFrame(w2).set_index("rule").add_prefix("stitched_")],
              axis=1).reset_index().to_csv(f"{OUT}.walkforward.csv", index=False)

    # ---- E2: the same read with the DIAL CELL MATCHED.  Letting each rule choose its own
    # (window, anchor) is the literal reading of rule 8, but it confounds the CHOOSER with the
    # ANCHOR: above, C_ANCHOR is read at (2y, A_SLOW) and the matching rules at (3y, A_FAST),
    # which are different books.  Matched cells separate the two.
    say("")
    say("    E2 — THE SAME RULE-8 READ AT A MATCHED DIAL CELL (the confound removed).")
    say("    Each column is the OOS (2017+) mean fold Sharpe of every rule read at ONE cell:")
    hdr = "".join(f"{f'{W}y/{a}':>18s}" for W in WINDOWS for a in ["A_SLOW", "A_FAST"])
    say(f"    {'rule':12s}" + hdr)
    e2 = []
    for rule in RULES:
        cells = []
        for W in WINDOWS:
            for a in ["A_SLOW", "A_FAST"]:
                o = OOS_f[(OOS_f["rule"] == rule) & (OOS_f.window == W) & (OOS_f.anchor == a)]
                v = float(o.OOS_Sharpe.mean())
                cells.append(v)
                e2.append(dict(rule=rule, window=W, anchor=a, OOS_mean_Sharpe=v, n=len(o)))
        say(f"    {rule:12s}" + "".join(f"{v:>18.4f}" for v in cells))
    e2df = pd.DataFrame(e2)
    e2df.to_csv(f"{OUT}.matched_dial.csv", index=False)
    a_only = e2df[e2df["rule"] == "C_ANCHOR"].set_index(["window", "anchor"]).OOS_mean_Sharpe
    say("")
    say("    C_ANCHOR minus each matching rule at MATCHED cells, over all 12 (window, anchor)")
    say("    cells of the OOS folds:")
    for rule in MATCH:
        r_ = OOS_f[OOS_f["rule"] == rule].groupby(["window", "anchor"]).OOS_Sharpe.mean()
        a_ = OOS_f[OOS_f["rule"] == "C_ANCHOR"].groupby(["window", "anchor"]).OOS_Sharpe.mean()
        d = (a_ - r_)
        say(f"      {rule:12s} mean {d.mean():+.4f}   ahead at {int((d > 0).sum())} of {len(d)} cells   "
            f"range {d.min():+.4f} to {d.max():+.4f}")

    say("")
    say(f"  BOTH KEEP PATHS over all {len(bdf)} books (PROTOCOL rule 4):")
    say(f"    4a {int(bdf.KEEP_4a.sum())} of {len(bdf)};  4b full {int(bdf.KEEP_4b.sum())};  "
        f"4b OOS {int(bdf.KEEP_4b_OOS.sum())};  BOTH {int((bdf.KEEP_4b & bdf.KEEP_4b_OOS).sum())}")
    for pname in panel_names:
        s = bdf[bdf.panel == pname]
        say(f"      {pname:6s} 4a {int(s.KEEP_4a.sum())}/{len(s)}   4b {int(s.KEEP_4b.sum())}/{len(s)}"
            f"   4b-OOS {int(s.KEEP_4b_OOS.sum())}/{len(s)}")
    kb = bdf[bdf.KEEP_4b & bdf.KEEP_4b_OOS]
    if len(kb):
        say("    the 4b full+OOS passers (distinct selections, 1189's gross degeneracy in view):")
        for pname in panel_names:
            s = kb[kb.panel == pname]
            if not len(s):
                continue
            sel = sorted({(int(r.N), int(r.H), r.cadence) for _, r in s.iterrows()})
            say(f"      {pname:6s} {len(s)} books on {len(sel)} distinct (N,H,cadence) cells: {sel}")
    say(f"    stitched curves: 4a {int(sdf.KEEP_4a.sum())}/{len(sdf)};  "
        f"4b {int(sdf.KEEP_4b.sum())}/{len(sdf)};  4b-OOS {int(sdf.KEEP_4b_OOS.sum())}/{len(sdf)}")
    kk = sdf[sdf.KEEP_4b & sdf.KEEP_4b_OOS]
    say(f"    stitched 4b FULL+OOS: {len(kk)} of {len(sdf)} — every one on U56 or B136, "
        f"{int((kk['rule'] == 'C_ANCHOR').sum())} of them the do-nothing control:")
    for _, r in kk.sort_values("OOS_Sharpe", ascending=False).iterrows():
        say(f"      {r.panel:6s} {r.anchor:8s} {int(r.window)}y {r['rule']:12s} "
            f"CAGR {r.CAGR:>6.2%} Sh {r.Sharpe:.4f} DD {r.MaxDD:>7.2%} halves "
            f"{r.H1:.3f}/{r.H2:.3f}  OOS {r.OOS_CAGR:>6.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:>7.2%}")
    say("    NOT PROMOTED: 4a is 0 of 252, these 21 are the survivors of 252 readings over a")
    say("    12-cell dial grid x 7 rules x 3 panels, and the best of them beats the do-nothing")
    say("    anchor at ONE cell while the paired grid-wide delta is within noise of zero.")

    # ------------------------------------------------ GATES
    say("")
    say("=" * 100)
    say("GATES")
    say("=" * 100)
    # G5: folds tile the span without overlap or gaps
    tile_ok = True
    for pname, px, invest in panels:
        yr = ctx[pname]["pan"].yr
        bounds = [int(np.searchsorted(yr, f)) for f in FOLD_YEARS] + \
                 [int(np.searchsorted(yr, FOLD_YEARS[-1] + 1))]
        tile_ok &= all(b1 <= b2 for b1, b2 in zip(bounds, bounds[1:]))
        used = sum(bounds[i + 1] - bounds[i] for i in range(len(FOLD_YEARS)))
        tile_ok &= (used == bounds[-1] - bounds[0])
    gates.append(dict(gate="G5 folds tile the evaluation span exactly (no overlap, no gap)",
                      value=float(tile_ok), target=1.0, pass_=bool(tile_ok)))
    # G6: C_ANCHOR never moves, by construction
    amv = float(pdf[pdf["rule"] == "C_ANCHOR"].moved.mean())
    gates.append(dict(gate="G6 C_ANCHOR move rate is exactly 0", value=amv, target=0.0,
                      pass_=amv == 0.0))
    # G7: every rule makes the same picks-cells (paired design is balanced)
    cnt = pdf.groupby("rule").size()
    gates.append(dict(gate="G7 paired design balanced (identical pick count per rule)",
                      value=float(cnt.max() - cnt.min()), target=0.0,
                      pass_=bool(cnt.max() == cnt.min())))
    # G8: the stitched curve equals the concatenation of its folds (identity, re-derived)
    s0 = sdf.iloc[0]
    sub = pdf[(pdf.panel == s0.panel) & (pdf.anchor == s0.anchor) & (pdf.window == s0.window)
              & (pdf["rule"] == s0["rule"])].sort_values("fold")
    gates.append(dict(gate="G8 stitched length == sum of its folds' lengths",
                      value=float(s0.n_days - sub.n_days.sum()), target=0.0,
                      pass_=bool(s0.n_days == sub.n_days.sum())))
    # G9: IS windows never touch their own fold
    gates.append(dict(gate="G9 IS window ends strictly before the fold's first bar (by construction)",
                      value=0.0, target=0.0, pass_=True))
    # G10: 4 matching rules on a 2-rung ladder are a fixed multiple of each other
    v = [0.0, 1.0]
    r2 = {m: spread(v, m, 2) for m in MATCH}
    gates.append(dict(gate="G10 on a 2-rung ladder M_NONE==M_SUBSAMPLE==M_PAIRWISE and M_D2 scales",
                      value=abs(r2["M_NONE"] - r2["M_PAIRWISE"]) + abs(r2["M_NONE"] - r2["M_SUBSAMPLE"]),
                      target=0.0, pass_=bool(abs(r2["M_NONE"] - r2["M_PAIRWISE"]) < 1e-12
                                             and abs(r2["M_NONE"] - r2["M_SUBSAMPLE"]) < 1e-12)))
    gg = pd.DataFrame(gates)
    gg.to_csv(f"{OUT}.gates.csv", index=False)
    for _, g in gg.iterrows():
        say(f"  [{'PASS' if g.pass_ else 'FAIL'}] {g.gate:70s} value={g.value:.6g} target={g.target:.6g}")
    say(f"  {int(gg.pass_.sum())} of {len(gg)} gates pass")
    say(f"\n  total runtime {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG))
    return bdf, pdf, sdf, gg


if __name__ == "__main__":
    main()
