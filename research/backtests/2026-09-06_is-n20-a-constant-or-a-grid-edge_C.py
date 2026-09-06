#!/usr/bin/env python3
"""Idea 240 - "is-n20-a-constant-or-a-grid-edge" (lane C, 2026-09-06).

The question
------------
Idea 77 reported that on idea 73's 7 panels the OOS argmax position count is **n=20 in
7 of 7 panels**, while each panel's own IS argmax matches its OOS argmax in only 2 of 7.
It read that as "the n dial is not predictable from its own in-sample Sharpe; it is
predictable from a constant -- take the widest n on offer."

But n=20 was the TOP of idea 73's grid {5, 10, 20}.  A 7-of-7 argmax at the edge of a
grid is exactly what a monotone-in-n curve produces, and it says nothing about whether
20 is special.  This run extends the grid to n in {20, 30, 40, 60} on all 7 panels and
asks the one question that separates the two readings:

    Does "take the widest n" survive leaving the edge?

Three outcomes, all pre-registered here before any OOS number was read:
    (A) OOS argmax stays at n=20 with 30/40/60 available  -> 20 is a real constant, the
        original finding was NOT an edge artefact.
    (B) OOS argmax moves to the new top (n=60) in most panels -> "widest n" survives, but
        the rule is still edge-bound and 20 was purely an artefact of idea 73's grid.
    (C) OOS argmax lands in the interior (30 or 40)       -> BOTH readings die: there is
        an interior optimum and neither 20 nor "widest" is the rule.

The de-grossing confound (stated before the design, not after)
--------------------------------------------------------------
Idea 73's book is `rank <= n` at a FIXED weight GROSS/n.  When a panel has fewer than n
eligible names the book holds GROSS * n_elig / n, i.e. widening n on a small panel is a
GROSS LADDER, not a wider book.  STK20 has 20 tradable names (13.4 mean eligible), ETF24
has 24, ETF36 has 36: on those panels n=30/40/60 are the SAME holdings at 2/3, 1/2 and
1/3 of the gross.  Reading an argmax across such cells would be reading idea 84/154's
gross dial with an n label on it.

So both conventions are run and BOTH are reported in full:
    FIXED  w = GROSS / n on the top-n names          (idea 73's, verbatim -- PRIMARY)
    NORM   w = GROSS / min(n, n_elig), i.e. always GROSS invested when anything is
           eligible (the width dial with the gross channel closed -- CONTROL)
Realised mean gross and mean held-name count are reported for every cell, and a cell is
flagged `saturated` when the panel cannot supply n names.  Under NORM a saturated cell is
byte-identical to the widest unsaturated one; those are marked and excluded from the
"did the argmax move" counts, because an argmax over duplicated books is not a choice.

Design
------
Panels, gate, cost, cadence, execution and the ranking key are idea 73/77's, imported
verbatim, and idea 77's harness rows and its n=20 IS/OOS column are reproduced as a gate
before anything new is read.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. panel (7)      2. n
The weighting convention is a stated CONTROL reported in full on every point, not a third
tuned dial: FIXED is pre-registered as primary because it is the incumbent construction.
Grid = 7 panels x n in {5,10,20,30,40,60} x 2 conventions = 84 points, plus 7 EWall and
7 v1 references = 98, ALL reported in `.grid.csv`.  n=5/10 are carried only for continuity
with idea 73's published curve; the idea-240 question is asked on {20,30,40,60}.

Walk-forward (PROTOCOL rule 8) -- rules fixed, with direction, before any OOS read
    WIDEST20   n=20, the widest point of idea 73's grid          (what idea 77 read)
    WIDEST60   n=60, the widest point of THIS grid               (the same rule, new edge)
    ISARGMAX   n = argmax IS Sharpe within the panel             (the dial reading itself)
    NOTHING    n=20 on U56, the project's incumbent book         (do-nothing control)
    RANDOM     mean OOS Sharpe over the 4 n values               (a coin flip on the dial)
    NARROWEST  n=20 is also the NARROWEST of {20,30,40,60}: reported as the sign check on
               WIDEST60, so the two edges of the new grid are both quoted.
    IS = 2009-2016, OOS = 2017-2026 read once, untouched.  Every rule is evaluated
    per-panel and pooled (equal-weight across the 7 panels), on both conventions.

Verdicts (both KEEP paths, every point)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: all three name lists are current constituents, one-directional.  It falls
hardest on STK20 / BSTK100 / SMALL484.  Widening n on a survivorship-selected list adds
names that are known ex post to have survived, so a finding that WIDER IS BETTER is
partly manufactured on this data -- restated in the memo.

Deterministic, standalone.  Reads baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import json
import numpy as np
import pandas as pd
from baseline import load_universe, score
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
W_FIXED = 0.15
NS_ALL = [5, 10, 20, 30, 40, 60]      # full curve reported
NS_Q = [20, 30, 40, 60]               # the idea-240 grid
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 400)


# ---------------------------------------------------------------- panels (idea 73/77, verbatim)
def build_panels():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    broad_g = [t for t in U["broad"] if t not in crypto]
    sect_g = [t for t in U["sectors"] if t not in crypto]
    bfc_g = [t for t in U["bonds_fx_commod"] if t not in crypto]
    stk_g = [t for t in U["megacap"] if t not in crypto]

    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)

    etf36 = broad_g + sect_g + bfc_g
    etf24 = broad_g + sect_g
    b_stk = [t for t in px136.columns if t not in set(etf36)]
    s_stk = [c for c in pxs.columns if c != "SPY"]

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        return p, set(tradable if tradable is not None else cols)

    return {
        "U56":      sub(px56, list(px56.columns)),
        "ETF36":    sub(px56, etf36),
        "ETF24":    sub(px56, etf24),
        "STK20":    sub(px56, stk_g, tradable=stk_g),
        "B136":     sub(px136, list(px136.columns)),
        "BSTK100":  sub(px136, b_stk, tradable=b_stk),
        "SMALL484": sub(pxs, s_stk, tradable=s_stk),
    }


# ---------------------------------------------------------------- books
def eligible_mask(px, tradable):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def weights(px, tradable, kind, n=None, conv="FIXED"):
    """kind in {v1, EWall, CAND}. conv only applies to CAND."""
    if kind == "v1":
        s = score(px, vol_scale=True)[0]
        rank = s.where(eligible_mask(px, tradable)).rank(axis=1, ascending=False)
        return (rank <= 5).astype(float) * W_FIXED
    elig = eligible_mask(px, tradable)
    if kind == "EWall":
        cnt = elig.sum(axis=1).replace(0, np.nan)
        return elig.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)
    s = score(px, vol_scale=False)[0]
    rank = s.where(elig).rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    if conv == "FIXED":                       # idea 73's: GROSS/n regardless of how many fill
        return sel * (GROSS / n)
    held = sel.sum(axis=1).replace(0, np.nan)  # NORM: always GROSS when anything is eligible
    return sel.div(held, axis=0).mul(GROSS).fillna(0.0)


def elig_count(px, tradable):
    """Mean eligible-name count on weekly rebalance dates."""
    elig = eligible_mask(px, tradable)
    mask = rebalance_mask(px.index, FREQ)
    return elig[mask.values].sum(axis=1)


# ---------------------------------------------------------------- stats helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def verdict_4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def fail_4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def fmt(df, p=3):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- main
def main():
    panels = build_panels()

    print("=" * 210)
    print(f"Idea 240 is-n20-a-constant-or-a-grid-edge (lane C) | {SCRIPT} | {COST_BPS} bps, weekly, next-day execution")
    print("=" * 210)

    px56 = panels["U56"][0]
    yrs = px56.index.to_series().groupby(px56.index.year).count()
    print(f"Index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)

    print("\nPanels:")
    ec = {}
    for k, (p, tr) in panels.items():
        ec[k] = elig_count(p, tr)
        print(f"  {k:<9} {len(tr):>3} tradable ({p.shape[1]} cols incl. benchmark)  "
              f"{p.index[0].date()} -> {p.index[-1].date()}   mean eligible {ec[k].mean():.1f}")

    # ---- run every book
    res, turn, wsum, hcnt = {}, {}, {}, {}
    jobs = [("EWall", None, "FIXED"), ("v1", None, "FIXED")]
    jobs += [("CAND", n, c) for c in ("FIXED", "NORM") for n in NS_ALL]
    for pk, (p, tr) in panels.items():
        for kind, n, conv in jobs:
            if kind != "CAND" and conv != "FIXED":
                continue
            w = weights(p, tr, kind, n, conv)
            r = backtest(p, w, cost_bps=COST_BPS, freq=FREQ)
            key = (pk, "EWall" if kind == "EWall" else ("v1" if kind == "v1" else f"CAND{n}"), conv)
            res[key] = r["returns"]
            turn[key] = r["turnover"]
            hw = r["weights"]
            wsum[key] = hw.sum(axis=1)
            hcnt[key] = (hw > 1e-12).sum(axis=1)
        print(f"  ran {pk}")

    start56 = px56.index[260]
    print("\n--- harness sanity (universe.json window, must match published rows) ---")
    for key, want in [(("U56", "CAND20", "FIXED"), "idea 2 KEEP: 12.7% / 1.093 / -18.3%, halves 1.088/1.103"),
                      (("U56", "v1", "FIXED"), "live v1: 6.5% / 0.666 / -13.8%")]:
        r = res[key].loc[start56:]
        m = metrics(r); h1, h2 = half_sharpes(r)
        print(f"  {key[0]}/{key[1]:<7} {m['CAGR']:.1%} / {m['Sharpe']:.3f} / {m['MaxDD']:.1%}  halves {h1:.3f}/{h2:.3f}   [{want}]")

    start = max(p.index[260] for p, _ in panels.values())
    end = min(p.index[-1] for p, _ in panels.values())
    spy = px56["SPY"].pct_change().fillna(0).loc[start:end]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    ms, ms_is, ms_oos = metrics(spy), metrics(spy_is), metrics(spy_oos)
    cut = lambda s: s.loc[start:end]
    print(f"\nCommon evaluation window (all panels, identical days): {start.date()} -> {end.date()} ({len(spy)} days)")
    print(f"SPY on it: {ms['CAGR']:.1%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.1%}  halves "
          f"{half_sharpes(spy)[0]:.3f}/{half_sharpes(spy)[1]:.3f}  IS {ms_is['Sharpe']:.3f}  OOS {ms_oos['Sharpe']:.3f}")
    print(f"4b bars (full): MaxDD <= {0.60 * abs(ms['MaxDD']):.1%}, CAGR >= {0.70 * ms['CAGR']:.2%}")
    print(f"4b OOS bar: Sharpe > {ms_oos['Sharpe']:.4f}")

    # ============================================================ 0. reproduction gate
    print("\n" + "=" * 210)
    print("0. REPRODUCTION GATE - idea 77's n=20 IS/OOS column, FIXED convention (its published table, section 1)")
    print("=" * 210)
    pub = {"STK20": (1.039, 1.446), "BSTK100": (1.052, 0.938), "B136": (1.025, 0.892),
           "U56": (0.956, 1.168), "SMALL484": (0.471, 0.510), "ETF24": (0.530, 0.889),
           "ETF36": (0.577, 0.942)}
    gate_ok = True
    for pk in pub:
        r = cut(res[(pk, "CAND20", "FIXED")])
        i, o = metrics(r.loc[:IS_END])["Sharpe"], metrics(r.loc[OOS_START:])["Sharpe"]
        d = max(abs(i - pub[pk][0]), abs(o - pub[pk][1]))
        gate_ok &= d < 0.002
        print(f"  {pk:<9} IS {i:.4f} [pub {pub[pk][0]:.3f}]   OOS {o:.4f} [pub {pub[pk][1]:.3f}]   maxdiff {d:.4f}")
    print(f"  REPRODUCTION: {'EXACT' if gate_ok else '*** MISMATCH - everything below is on a different harness ***'}")

    # ============================================================ 1. the full grid
    print("\n" + "=" * 210)
    print("1. THE FULL GRID - 7 panels x n in {5,10,20,30,40,60} x {FIXED, NORM}, all reported")
    print("=" * 210)
    rows = []
    for conv in ("FIXED", "NORM"):
        for pk in panels:
            n_tradable = len(panels[pk][1])
            eligc = ec[pk].loc[start:end]
            for n in NS_ALL:
                key = (pk, f"CAND{n}", conv)
                r = cut(res[key])
                ri, ro = r.loc[:IS_END], r.loc[OOS_START:]
                mf, mi, mo = metrics(r), metrics(ri), metrics(ro)
                h1, h2 = half_sharpes(r)
                base = cut(res[(pk, "v1", "FIXED")])
                sat = float((eligc < n).mean())          # share of rebalances that cannot fill n
                rows.append(dict(
                    conv=conv, panel=pk, n=n, n_tradable=n_tradable,
                    mean_elig=eligc.mean(), sat_share=sat,
                    mean_gross=cut(wsum[key]).mean(), mean_held=cut(hcnt[key]).mean(),
                    turnover=cut(turn[key]).sum() / mf["Years"],
                    CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                    IS_Sharpe=mi["Sharpe"], OOS_Sharpe=mo["Sharpe"],
                    OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                    pass_4a=verdict_4a(r, base),
                    fail_4b=fail_4b(r, spy, ro, spy_oos)))
    grid = pd.DataFrame(rows)
    grid["pass_4b"] = grid["fail_4b"] == "-"
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    for conv in ("FIXED", "NORM"):
        g = grid[grid.conv == conv]
        print(f"\n--- {conv} ---")
        print(fmt(g.set_index(["panel", "n"])[["mean_elig", "sat_share", "mean_gross", "mean_held", "turnover",
                                               "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                               "IS_Sharpe", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD"]]))
    print(f"\n  grid written to {STEM}.grid.csv ({len(grid)} points)")

    # duplicate detection under NORM (a saturated cell repeats the widest unsaturated book)
    print("\n--- NORM duplicate check: is n=60 a DISTINCT book from n=40/30/20 on this panel? ---")
    dup = []
    for pk in panels:
        base_r = cut(res[(pk, "CAND20", "NORM")])
        line = {"panel": pk}
        for n in NS_Q:
            r = cut(res[(pk, f"CAND{n}", "NORM")])
            line[f"n{n}_vs_n20_maxabs"] = float((r - base_r).abs().max())
        dup.append(line)
    dupdf = pd.DataFrame(dup).set_index("panel")
    print(dupdf.to_string(float_format=lambda x: f"{x:.2e}"))
    print("  0 => the wider n is the SAME book (panel cannot supply the extra names); an argmax over it is not a choice.")

    # ============================================================ 2. the argmax question
    print("\n" + "=" * 210)
    print("2. THE IDEA-240 QUESTION - where is the argmax on the WIDENED grid {20,30,40,60}?")
    print("=" * 210)
    arg_rows = []
    for conv in ("FIXED", "NORM"):
        for pk in panels:
            g = grid[(grid.conv == conv) & (grid.panel == pk) & (grid.n.isin(NS_Q))].set_index("n")
            g5 = grid[(grid.conv == conv) & (grid.panel == pk)].set_index("n")     # incl. 5/10
            distinct = int(sum(1 for n in NS_Q
                               if float((cut(res[(pk, f"CAND{n}", conv)]) -
                                         cut(res[(pk, "CAND20", conv)])).abs().max()) > 1e-12) + 1)
            arg_rows.append(dict(
                conv=conv, panel=pk, distinct_books=distinct,
                IS_argmax=int(g["IS_Sharpe"].idxmax()), OOS_argmax=int(g["OOS_Sharpe"].idxmax()),
                IS_argmax_old=int(g5.loc[[5, 10, 20]]["IS_Sharpe"].idxmax()),
                OOS_argmax_old=int(g5.loc[[5, 10, 20]]["OOS_Sharpe"].idxmax()),
                OOS_at20=g.loc[20, "OOS_Sharpe"], OOS_at60=g.loc[60, "OOS_Sharpe"],
                OOS_best=g["OOS_Sharpe"].max(),
                spread=g["OOS_Sharpe"].max() - g["OOS_Sharpe"].min(),
                monotone_rho=float(pd.Series(g["OOS_Sharpe"].values).rank()
                                   .corr(pd.Series(NS_Q).rank()))))
    argt = pd.DataFrame(arg_rows)
    argt.to_csv(OUT / f"{STEM}.argmax.csv", index=False)
    for conv in ("FIXED", "NORM"):
        a = argt[argt.conv == conv].set_index("panel")
        print(f"\n--- {conv} ---")
        print(fmt(a[["distinct_books", "IS_argmax_old", "OOS_argmax_old", "IS_argmax", "OOS_argmax",
                     "OOS_at20", "OOS_at60", "OOS_best", "spread", "monotone_rho"]]))
        n_at_20 = (a["OOS_argmax"] == 20).sum()
        n_at_60 = (a["OOS_argmax"] == 60).sum()
        n_int = ((a["OOS_argmax"] > 20) & (a["OOS_argmax"] < 60)).sum()
        d = a[a["distinct_books"] == 4]
        print(f"  OOS argmax on the WIDENED grid: n=20 in {n_at_20}/7, n=60 in {n_at_60}/7, interior (30/40) in {n_int}/7")
        print(f"  restricted to panels where all 4 books are DISTINCT ({len(d)}/7): "
              f"n=20 {int((d['OOS_argmax'] == 20).sum())}, n=60 {int((d['OOS_argmax'] == 60).sum())}, "
              f"interior {int(((d['OOS_argmax'] > 20) & (d['OOS_argmax'] < 60)).sum())}")
        print(f"  IS argmax == OOS argmax in {(a['IS_argmax'] == a['OOS_argmax']).sum()}/7 panels "
              f"[idea 77 on the old grid: 2/7]")

    # ---- 2b. if the argmax is not a constant, what is it a function of?
    print("\n--- 2b. the OOS argmax against the panel's own eligible count (descriptive, N=7) ---")
    for conv in ("FIXED", "NORM"):
        a = argt[argt.conv == conv].set_index("panel").copy()
        a["mean_elig"] = [ec[pk].loc[start:end].mean() for pk in a.index]
        a["n_tradable"] = [len(panels[pk][1]) for pk in a.index]
        a["sat20"] = [float((ec[pk].loc[start:end] < 20).mean()) for pk in a.index]
        a["argmax_over_elig"] = a["OOS_argmax"] / a["mean_elig"]
        a = a.sort_values("mean_elig")
        rho = float(pd.Series(a["mean_elig"].values).rank().corr(pd.Series(a["OOS_argmax"].values).rank()))
        print(f"\n  {conv}:  Spearman(mean eligible count, OOS argmax n) = {rho:+.3f}  (N=7)")
        print(fmt(a[["n_tradable", "mean_elig", "sat20", "OOS_argmax", "argmax_over_elig",
                     "OOS_at20", "OOS_at60", "spread"]]))

    # ============================================================ 3. rule 8 walk-forward
    print("\n" + "=" * 210)
    print("3. RULE 8 WALK-FORWARD - rules and directions fixed above; IS 2009-2016, OOS 2017-2026 read once")
    print("=" * 210)
    wf_rows = []
    for conv in ("FIXED", "NORM"):
        picks = {}
        for pk in panels:
            g = grid[(grid.conv == conv) & (grid.panel == pk) & (grid.n.isin(NS_Q))].set_index("n")
            picks[pk] = dict(WIDEST20=20, NARROWEST=20, WIDEST60=60,
                             ISARGMAX=int(g["IS_Sharpe"].idxmax()))
        for rule in ("WIDEST20", "WIDEST60", "ISARGMAX", "RANDOM", "NOTHING"):
            per = {}
            for pk in panels:
                if rule == "RANDOM":
                    g = grid[(grid.conv == conv) & (grid.panel == pk) & (grid.n.isin(NS_Q))]
                    per[pk] = dict(n=np.nan, OOS_Sharpe=g["OOS_Sharpe"].mean(),
                                   OOS_CAGR=g["OOS_CAGR"].mean(), OOS_MaxDD=g["OOS_MaxDD"].mean())
                    continue
                n = 20 if rule == "NOTHING" else picks[pk][rule]
                r = cut(res[(pk, f"CAND{n}", conv)]).loc[OOS_START:]
                m = metrics(r)
                per[pk] = dict(n=n, OOS_Sharpe=m["Sharpe"], OOS_CAGR=m["CAGR"], OOS_MaxDD=m["MaxDD"])
            if rule == "NOTHING":
                per = {"U56": per["U56"]}
            pooled = pd.DataFrame(per).T
            wf_rows.append(dict(conv=conv, rule=rule,
                                picks=";".join(f"{k}:{int(v['n'])}" for k, v in per.items()
                                               if not np.isnan(v["n"])) if rule != "RANDOM" else "mean over n",
                                OOS_Sharpe=pooled["OOS_Sharpe"].mean(),
                                OOS_CAGR=pooled["OOS_CAGR"].mean(),
                                OOS_MaxDD=pooled["OOS_MaxDD"].mean(),
                                **{f"S_{k}": v["OOS_Sharpe"] for k, v in per.items()}))
    wf = pd.DataFrame(wf_rows)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    for conv in ("FIXED", "NORM"):
        w = wf[wf.conv == conv].set_index("rule")
        print(f"\n--- {conv} (pooled = equal weight over the 7 panels; NOTHING is U56 alone) ---")
        cols = ["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD"] + [c for c in w.columns if c.startswith("S_")]
        print(fmt(w[cols], 3))
        print("  picks:")
        for rl, r in w.iterrows():
            print(f"    {rl:<10} {r['picks']}")
        base_oos = metrics(cut(res[("U56", "v1", "FIXED")]).loc[OOS_START:])
        print(f"  references OOS: SPY {ms_oos['CAGR']:.1%} / {ms_oos['Sharpe']:.3f} / {ms_oos['MaxDD']:.1%}   "
              f"RULES v1 (U56) {base_oos['CAGR']:.1%} / {base_oos['Sharpe']:.3f} / {base_oos['MaxDD']:.1%}")
        d = w.loc["WIDEST60", "OOS_Sharpe"] - w.loc["WIDEST20", "OOS_Sharpe"]
        print(f"  WIDEST60 - WIDEST20(=NARROWEST) pooled OOS Sharpe = {d:+.4f}")
        print(f"  ISARGMAX - WIDEST20 pooled = {w.loc['ISARGMAX', 'OOS_Sharpe'] - w.loc['WIDEST20', 'OOS_Sharpe']:+.4f}   "
              f"vs RANDOM {w.loc['RANDOM', 'OOS_Sharpe'] - w.loc['WIDEST20', 'OOS_Sharpe']:+.4f}")

    # per-panel paired sign test of WIDEST60 vs n=20
    print("\n--- paired: OOS Sharpe(n=60) - OOS Sharpe(n=20), per panel ---")
    pair = []
    for conv in ("FIXED", "NORM"):
        line = {"conv": conv}
        for pk in panels:
            g = grid[(grid.conv == conv) & (grid.panel == pk)].set_index("n")
            line[pk] = g.loc[60, "OOS_Sharpe"] - g.loc[20, "OOS_Sharpe"]
        line["mean"] = np.mean([line[pk] for pk in panels])
        line["wins"] = int(sum(line[pk] > 0 for pk in panels))
        pair.append(line)
    print(fmt(pd.DataFrame(pair).set_index("conv"), 4))

    # ============================================================ 4. KEEP paths
    print("\n" + "=" * 210)
    print("4. KEEP PATHS - both, every point")
    print("=" * 210)
    for conv in ("FIXED", "NORM"):
        g = grid[grid.conv == conv]
        print(f"\n--- {conv} ---   4a passes {int(g['pass_4a'].sum())}/{len(g)}   4b passes {int(g['pass_4b'].sum())}/{len(g)}")
        p4b = g[g.pass_4b]
        if len(p4b):
            print(fmt(p4b.set_index(["panel", "n"])[["mean_gross", "mean_held", "turnover", "CAGR", "Sharpe",
                                                     "MaxDD", "H1", "H2", "OOS_Sharpe", "pass_4a"]]))
        print("  4b failing bars, by count: " + ", ".join(
            f"{k}={v}" for k, v in g["fail_4b"].value_counts().items()))

    print("\n" + "=" * 210)
    print("DONE. Files: .grid.csv .argmax.csv .walkforward.csv")
    print("=" * 210)


if __name__ == "__main__":
    main()
