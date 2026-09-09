#!/usr/bin/env python3
"""Idea 588 — HOW MANY PUBLISHED DIAL STEPS IN THE RECORD ARE NO-OPS?   (cloud, 2026-09-09)

PRE-REGISTERED QUESTION (from QUEUE.md, written before any number here was read)
    Idea 320 found U56's n0=60 and n0=E_t books are BIT-IDENTICAL (max|dW| exactly 0.000e+00)
    because the panel saturates at 37.5 eligible names, so 1 of 4 published ABS dial steps on
    that panel moved nothing.  Re-derive every committed grid whose dial is an absolute count
    and report, per panel, how many adjacent grid points are the same book to machine
    precision; any "the dial is flat here" claim resting on a no-op step needs re-reading.
    Max 2 params.

TWO INDEPENDENT PARTS, both pre-registered.

PART A — THE RECORD-WIDE CENSUS (published numbers only, no re-derivation).
    Every committed CSV under research/backtests/ that carries BOTH an integer count-dial
    column (n, n0, k, N, K, width) and at least one performance column (CAGR, Sharpe, MaxDD,
    OOS_*, H1, H2, ann_ret, ann_vol, turn, IS_Sharpe) is a candidate grid.  Rows are grouped
    by every non-float column other than the dial (the file's own reporting axes), duplicate
    dial values inside a group are dropped, the group is sorted on the dial, and each strictly
    increasing ADJACENT PAIR is one published step.  A step is counted a NO-OP CANDIDATE when
    every shared performance column is EXACTLY equal (float equality on the committed value,
    NaN==NaN).  This is necessary, not sufficient: it proves the published numbers are the
    same, and Part B proves the BOOKS are.  A NEAR pair (all |d| < 1e-9 but not all exactly
    equal) is counted separately.  Counts are broken out per dial column because `k` and `K`
    are sometimes a draw size, not a book dial — that caveat is reported, not hidden.

PART B — RE-DERIVATION TO MACHINE PRECISION (three live panels).
    Idea 320's ABS width book, unchanged: rank the eligible names by research/scan.py's
    composite, hold the top k at gross/k each, k = min(n0, E_t), gross 0.75 every day, weekly,
    10 bps, weights at close t applied at t+1.  For every adjacent pair of dial points the FULL
    target weight matrices are differenced: max|dW|, sum|dW|, the share of DAYS whose weight
    rows are identical, and max|dr| on the realised return series.

    THE CLOSED FORM, pre-registered before the grid was run: with k = min(n0, E_t) the step
    n0_a -> n0_b (a < b) is an exact no-op if and only if E_t <= n0_a on EVERY day, i.e. iff
    n0_a >= max_t E_t.  So each (panel, gate) has one CEILING and every published grid point
    at or above it is redundant by construction.  The grid tests this identity rather than
    assuming it.

TUNED PARAMETERS: exactly TWO.
    (1) the dial n0 in {5, 10, 20, 30, 40, 60, 80, 100, E_t} — ALL 9 points reported;
    (2) the eligibility gate in {NONE, MA, MA+VOL} — ALL 3 reported.
    The gate is the second parameter on purpose: it is what sets E_t, so it is the direct test
    of whether the no-op rate is a property of the panel or of the gate bolted on top of it.
    PANEL is a reporting axis, never selected on.  Nothing else is swept.

    Because points above a panel's ceiling are no-ops by construction, the no-op RATE is
    reported twice: over this script's full 9-point grid (which deliberately contains
    out-of-range points, as the record's own grids do) and over IDEA 320's OWN published
    5-point grid {20, 30, 40, 60, E_t}, which is the number that speaks to the record.

RULE 8 (PROTOCOL 8), run on every (panel, gate): n0 chosen on IS <= 2016-12-31 by IS Sharpe,
    2017-2026 read ONCE.  Reported with the thing this idea is about: the TIE-SET SIZE of the
    pick — how many other grid points are the same book to machine precision — because an
    argmax over a grid containing no-ops is decided by the sort order, not by the data.
    OOS CAGR/Sharpe/MaxDD are printed against the live RULES v2 baseline, RULES v1 and SPY,
    and BOTH KEEP paths (4a and 4b) are evaluated at all 81 grid points.

REPRODUCTION GATES, asserted before any new number is read
  G1  the numpy replica reproduces engine.backtest (returns and turnover) below 1e-12.
  G2  idea 320's committed grid.csv: CAGR/Sharpe/MaxDD/H1/H2/OOS_Sharpe at ABS n0 in
      {20,30,40,60,E_t} on all three panels, under the MA+VOL gate (its gate).
  G3  idea 320's committed saturation.csv: the four adjacent-step max|dW| values per panel,
      including the U56 n0=60 -> E_t zero.
  G4  idea 320's headline "the panel saturates at 37.5 eligible names": U56 k_mean at n0=E_t.

SURVIVORSHIP (PROTOCOL 9 / idea 54): B136 and SMALL439 are CURRENT-constituent lists, so the
names that died are absent and every panel's realised E_t is a survivor's count.  The ceiling
this script publishes is therefore an UNDERSTATEMENT of the eligible-name count a real
historical panel would have offered, which means the true no-op rate on a survivorship-free
panel would be LOWER than the one reported here.  That direction is stated because it cuts
against the finding, not for it.  SMALL439: the 483-name sub-$2B panel with the 44 tickers
whose max_1d_move >= 1.0 dropped per data/SMALL_PANEL_README.md.

NOTE ON A CONVENTION, found while building G4: idea 320 reports every E_t / k statistic on the
POST-WARM-UP window (px.index[260:]), not on the full index.  U56's eligible-name mean is 37.50
on that window and 37.05 on the full one.  Both are correct; only the first reproduces the
record.  Every E_t number in this script is on idea 320's window, and the ceiling too.

Deterministic, no network.  Writes .census.csv .ceiling.csv .steps.csv .steps_i320grid.csv
.grid.csv .walkforward.csv .console.txt
"""
import glob
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

BT = REPO / "research" / "backtests"
STAMP = "2026-09-09_how-many-published-dial-STEPS-in-the-record-are-NO-OPS_cloud"
OUT = BT / STAMP

I320 = BT / "2026-09-09_is-the-UNCONDITIONAL-width-dial-a-B136-fact-or-a-panel-ordering_B"

COST_BPS = 10.0
FREQ = "W"
GROSS = 0.75
MAX_VOL = 0.60
VOL_SCALE = False
COMMON_END = "2026-09-04"
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

DIAL_GRID = [5, 10, 20, 30, 40, 60, 80, 100, "E"]
I320_GRID = ["ABS n0=20", "ABS n0=30", "ABS n0=40", "ABS n0=60", "ABS n0=E_t"]
GATES = ["NONE", "MA", "MA+VOL"]

DIAL_COLS = ["n", "n0", "k", "N", "K", "width"]
MET_COLS = ["cagr", "sharpe", "maxdd", "oos_cagr", "oos_sharpe", "oos_maxdd",
            "h1", "h2", "ann_ret", "ann_vol", "turn", "is_sharpe"]

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ engine replica
def fast_backtest(prices, weights, cost_bps=COST_BPS, freq=FREQ):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(index=idx, columns=prices.columns).fillna(0.0).shift(1).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values
    n = len(idx)
    cur = np.zeros(prices.shape[1])
    held = np.empty_like(rets)
    turn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = np.nansum(held * rets, axis=1) - turn * cost_bps / 1e4
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx),
            pd.DataFrame(held, index=idx, columns=prices.columns))


# ------------------------------------------------------------------ book primitives
def gate_mask(px, cols, gate):
    """Eligibility under one of the record's three gate conventions."""
    _, above, vol20 = score(px)
    priced = px[cols].notna() & px[cols].rolling(200).mean().notna()
    if gate == "NONE":
        return priced
    if gate == "MA":
        return priced & above[cols]
    return priced & above[cols] & (vol20[cols] < MAX_VOL)


def elig_count(px, cols, gate):
    e = gate_mask(px, cols, gate).sum(axis=1).astype(float)
    ma_ok = px[cols].rolling(200).mean().notna().any(axis=1)
    return e.where(ma_ok)


def ranked(px, cols, gate):
    s = score(px, vol_scale=VOL_SCALE)[0][cols].where(gate_mask(px, cols, gate))
    return s.rank(axis=1, ascending=False)


def k_series(dial, e):
    if dial == "E":
        return e.clip(lower=1.0)
    return np.minimum(float(dial), e).clip(lower=1.0)


def weights_from_k(rank, k):
    k = k.clip(lower=1.0)
    return rank.le(k, axis=0).astype(float).mul(GROSS / k, axis=0)


def dial_label(d):
    return "ABS n0=E_t" if d == "E" else f"ABS n0={d:d}"


# ------------------------------------------------------------------ metric helpers
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def keep_4a(r, base):
    a1, a2 = halves(r)
    b1, b2 = halves(base)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def tests_4b(r, spy):
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    return {"H1": a1 > s1, "H2": a2 > s2,
            "OOS": metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"],
            "DD": abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]),
            "CAGR": m["CAGR"] >= 0.70 * ms["CAGR"]}


def fail_4b(r, spy):
    f = [k for k, v in tests_4b(r, spy).items() if not v]
    return ",".join(f) if f else "-"


# ------------------------------------------------------------------ PART A
def census():
    files = sorted(glob.glob(str(BT / "*.csv"))) + sorted(glob.glob(str(BT / "*.csv.gz")))
    rows = []
    tot = dict(files=0, groups=0, steps=0, noop=0, near=0)
    for f in files:
        try:
            df = pd.read_csv(f, low_memory=False)
        except Exception:
            continue
        lc = {c.lower(): c for c in df.columns}
        mets = [lc[m] for m in MET_COLS if m in lc]
        mets = [c for c in mets if pd.api.types.is_numeric_dtype(df[c])]
        if not mets:
            continue
        dials = [c for c in df.columns if c in DIAL_COLS]
        if not dials:
            continue
        for d in dials:
            col = pd.to_numeric(df[d], errors="coerce")
            v = col.dropna()
            if len(v) == 0 or not np.allclose(v % 1, 0) or v.nunique() < 2:
                continue
            others = [c for c in df.columns
                      if c != d and c not in mets and not pd.api.types.is_float_dtype(df[c])]
            sub = df.assign(_d=col).dropna(subset=["_d"])
            fs = dict(steps=0, noop=0, near=0, groups=0)
            for _, g in (sub.groupby(others, dropna=False) if others else [(None, sub)]):
                g = g.drop_duplicates(subset=["_d"]).sort_values("_d")
                if len(g) < 2:
                    continue
                fs["groups"] += 1
                M = g[mets].to_numpy(dtype=float)
                for i in range(len(g) - 1):
                    fs["steps"] += 1
                    a, b = M[i], M[i + 1]
                    both_nan = np.isnan(a) & np.isnan(b)
                    if np.all((a == b) | both_nan):
                        fs["noop"] += 1
                    elif np.all((np.abs(a - b) < 1e-9) | both_nan):
                        fs["near"] += 1
            if fs["steps"] == 0:
                continue
            tot["files"] += 1
            for kk in ("groups", "steps", "noop", "near"):
                tot[kk] += fs[kk]
            rows.append(dict(file=Path(f).name, dial_col=d, n_metrics=len(mets), **fs))
    return pd.DataFrame(rows), tot


# ------------------------------------------------------------------ panels
def build_panels():
    px56 = load_universe().dropna(how="all").ffill().loc[:COMMON_END]
    px136 = load_universe(broad=True).dropna(how="all").ffill().loc[:COMMON_END]
    pxs = load_universe(small=True).loc[:COMMON_END]
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_all = [c for c in pxs.columns if c != "SPY"]
    s_stk = [c for c in s_all if c not in bad]
    P(f"  SMALL: {len(s_all)} names in panel, dropped {len(s_all) - len(s_stk)} with "
      f"max_1d_move >= 1.0 -> {len(s_stk)} tradable")
    return [("U56", px56, list(px56.columns)),
            ("B136", px136, list(px136.columns)),
            (f"SMALL{len(s_stk)}", pxs[s_stk + ["SPY"]].dropna(how="all").ffill(), s_stk)]


# ------------------------------------------------------------------ main
def main():
    P(f"# Idea 588 — how many published dial STEPS in the record are NO-OPS?   ({STAMP})")
    P(f"Costs {COST_BPS:.0f} bps, {FREQ} cadence, gross {GROSS}, t+1 execution (PROTOCOL 2/3).")
    P(f"Tuned: dial n0 in {DIAL_GRID} x gate in {GATES}; ALL 27 points per panel reported. "
      "Panel is a reporting axis.")
    P("")

    # ---------------- PART A
    P("=" * 100)
    P("PART A — RECORD-WIDE CENSUS OF PUBLISHED ADJACENT COUNT-DIAL STEPS")
    P("=" * 100)
    cen, tot = census()
    cen.to_csv(f"{OUT}.census.csv", index=False)
    P(f"Scanned {len(sorted(glob.glob(str(BT / '*.csv'))) + sorted(glob.glob(str(BT / '*.csv.gz'))))} "
      f"committed CSVs; {tot['files']} (file, dial-column) pairs carry an integer count dial "
      f"AND a performance column.")
    P(f"  reporting groups {tot['groups']:,}   adjacent published steps {tot['steps']:,}")
    P(f"  BIT-IDENTICAL on every shared performance column: {tot['noop']:,} "
      f"({tot['noop'] / max(tot['steps'], 1):.3%})")
    P(f"  NEAR-identical (all |d| < 1e-9, not exact):        {tot['near']:,} "
      f"({tot['near'] / max(tot['steps'], 1):.3%})")
    by = cen.groupby("dial_col")[["steps", "noop", "near"]].sum()
    by["rate"] = by.noop / by.steps
    P("\nBy dial column (CAVEAT: `k`/`K` is sometimes a draw size or a fold count, not a book "
      "dial; those rows are reported, not claimed):")
    P(by.to_string(float_format=lambda x: f"{x:.4f}"))
    bk = cen[cen.dial_col.isin(["n", "n0", "width"])]
    P(f"\nDEFENSIBLE SUBSET — dial columns that are unambiguously a BOOK WIDTH (n, n0, width): "
      f"{int(bk.noop.sum()):,}/{int(bk.steps.sum()):,} = {bk.noop.sum() / bk.steps.sum():.3%} of "
      "published adjacent steps re-publish the previous point's numbers unchanged.")
    top = cen[cen.noop > 0].sort_values("noop", ascending=False)
    P(f"\n{len(top)} (file, dial) pairs contain at least one identical step. Top 12:")
    for _, r in top.head(12).iterrows():
        P(f"  {r.noop:5d}/{r.steps:6d}  [{r.dial_col}]  {r.file[:74]}")
    P("")

    # ---------------- PART B
    P("=" * 100)
    P("PART B — RE-DERIVATION OF THE BOOKS TO MACHINE PRECISION")
    P("=" * 100)
    panels = build_panels()

    # G1
    pname, px, cols = panels[0]
    r0 = ranked(px, cols, "MA+VOL")
    e0 = elig_count(px, cols, "MA+VOL")
    w0 = weights_from_k(r0, k_series(20, e0))
    fr, ft, _ = fast_backtest(px, w0, cost_bps=0.0)
    ref = backtest(px, w0, cost_bps=0.0, freq=FREQ)
    d1 = float(np.abs(fr - ref["returns"]).max())
    d1t = float(np.abs(ft - ref["turnover"]).max())
    P(f"G1  replica vs engine.backtest: max|dret| {d1:.3e}  max|dturn| {d1t:.3e}   "
      f"{'PASS' if d1 < 1e-12 and d1t < 1e-12 else 'FAIL'}")
    assert d1 < 1e-12 and d1t < 1e-12

    grid, steps, steps320, ceil_rows, wf = [], [], [], [], []
    i320g = pd.read_csv(f"{I320}.grid.csv")
    i320s = pd.read_csv(f"{I320}.saturation.csv")
    g2worst = {}
    g3worst = 0.0
    g3n = 0
    g4 = None

    for pname, px, cols in panels:
        start = px.index[260]              # idea 320's warm-up cut; every E_t/k/dW stat below
        spy = px["SPY"].pct_change().fillna(0).iloc[260:]   # is measured on THIS window, as it is
        b_v2 = fast_backtest(px, rules_v2_weights(px))[0].iloc[260:]
        b_v1 = fast_backtest(px, rules_v1_weights(px))[0].iloc[260:]
        for bn, bs in (("RULES v2 (live)", b_v2), ("RULES v1", b_v1), ("SPY", spy)):
            mm = metrics(bs)
            h1, h2 = halves(bs)
            mo = metrics(bs.loc[OOS_START:])
            grid.append(dict(panel=pname, gate="BENCH", dial=bn, CAGR=mm["CAGR"],
                             Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                             IS_Sharpe=metrics(bs.loc[:IS_END])["Sharpe"],
                             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                             k_mean=np.nan, sat=np.nan, E_max=np.nan, p4a=False, p4b=False,
                             fail4b="-"))
        for gate in GATES:
            rank = ranked(px, cols, gate)
            e_full = elig_count(px, cols, gate)
            e = e_full.loc[start:]
            ev = e.dropna()
            ceiling = float(ev.max())
            ceil_rows.append(dict(panel=pname, gate=gate, n_names=len(cols),
                                  E_mean=float(ev.mean()), E_med=float(ev.median()),
                                  E_p95=float(ev.quantile(0.95)), E_max=ceiling,
                                  ceiling_frac=ceiling / len(cols)))
            books = {}
            wcache = {}
            prevW = prevL = prevr = None
            for d in DIAL_GRID:
                lab = dial_label(d)
                k_all = k_series(d, e_full)
                W_all = weights_from_k(rank, k_all).fillna(0.0)
                r, to, held = fast_backtest(px, W_all)
                r = r.iloc[260:]
                k = k_all.loc[start:]
                W = W_all.loc[start:]
                mm = metrics(r)
                h1, h2 = halves(r)
                mo = metrics(r.loc[OOS_START:])
                t4 = tests_4b(r, spy)
                sat = float((ev <= k.reindex(ev.index)).mean())
                grid.append(dict(panel=pname, gate=gate, dial=lab, CAGR=mm["CAGR"],
                                 Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                                 IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                 OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                 OOS_MaxDD=mo["MaxDD"], k_mean=float(k.mean()), sat=sat,
                                 E_max=ceiling, p4a=keep_4a(r, b_v2), p4b=all(t4.values()),
                                 fail4b=fail_4b(r, spy)))
                books[lab] = r
                if lab in I320_GRID:
                    wcache[lab] = (W, r)
                if prevW is not None:
                    dW = (W - prevW).abs()
                    mx = float(dW.max().max())
                    sm = float(dW.sum().sum())
                    same_day = float((dW.max(axis=1) == 0).mean())
                    dr = float(np.abs(r - prevr).max())
                    prev_n0 = np.inf if prevL.endswith("E_t") else float(prevL.split("=")[1])
                    steps.append(dict(panel=pname, gate=gate, step=f"{prevL} -> {lab}",
                                      from_dial=prevL, to_dial=lab, max_abs_dW=mx,
                                      sum_abs_dW=sm, days_identical=same_day, max_abs_dr=dr,
                                      identical=bool(mx == 0.0), E_max=ceiling,
                                      predicted_noop=bool(prev_n0 >= ceiling)))
                prevW, prevL, prevr = W, lab, r

            # idea 320's OWN published grid {20,30,40,60,E_t}: its adjacency, not this
            # script's, so its 60 -> E_t step (the one it found flat) is actually formed.
            for a, b in zip(I320_GRID[:-1], I320_GRID[1:]):
                Wa, ra = wcache[a]
                Wb, rb = wcache[b]
                dW = (Wb - Wa).abs()
                mx = float(dW.max().max())
                prev_n0 = np.inf if a.endswith("E_t") else float(a.split("=")[1])
                steps320.append(dict(panel=pname, gate=gate, step=f"{a} -> {b}",
                                     from_dial=a, to_dial=b, max_abs_dW=mx,
                                     sum_abs_dW=float(dW.sum().sum()),
                                     days_identical=float((dW.max(axis=1) == 0).mean()),
                                     max_abs_dr=float(np.abs(rb - ra).max()),
                                     identical=bool(mx == 0.0), E_max=ceiling,
                                     predicted_noop=bool(prev_n0 >= ceiling)))
            wcache.clear()

            # rule 8 on this (panel, gate)
            sub = [g for g in grid if g["panel"] == pname and g["gate"] == gate]
            pick = max(sub, key=lambda x: x["IS_Sharpe"])
            tie = [g["dial"] for g in sub
                   if abs(g["IS_Sharpe"] - pick["IS_Sharpe"]) == 0.0]
            wf.append(dict(panel=pname, gate=gate, pick=pick["dial"], tie_set=len(tie),
                           tie_members="|".join(tie), IS_Sharpe=pick["IS_Sharpe"],
                           OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                           OOS_MaxDD=pick["OOS_MaxDD"],
                           v2_OOS_Sharpe=metrics(b_v2.loc[OOS_START:])["Sharpe"],
                           v2_OOS_CAGR=metrics(b_v2.loc[OOS_START:])["CAGR"],
                           v2_OOS_MaxDD=metrics(b_v2.loc[OOS_START:])["MaxDD"],
                           spy_OOS_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"],
                           spy_OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                           spy_OOS_MaxDD=metrics(spy.loc[OOS_START:])["MaxDD"],
                           oos_best=max(sub, key=lambda x: x["OOS_Sharpe"])["dial"],
                           p4a=pick["p4a"], p4b=pick["p4b"], fail4b=pick["fail4b"]))

            if gate == "MA+VOL":
                ref320 = i320g[(i320g.panel == pname) & (i320g.unit == "ABS")]
                if len(ref320):
                    w = 0.0
                    for _, rr in ref320.iterrows():
                        mine = [g for g in grid if g["panel"] == pname and g["gate"] == gate
                                and g["dial"] == rr.dial]
                        if not mine:
                            continue
                        mine = mine[0]
                        for c in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"):
                            w = max(w, abs(mine[c] - rr[c]))
                    g2worst[pname] = w
                ref_s = i320s[i320s.panel == pname]
                for _, rr in ref_s.iterrows():
                    mine = [s for s in steps320 if s["panel"] == pname and s["gate"] == gate
                            and s["step"] == rr.step]
                    assert mine, (pname, rr.step)
                    g3n += 1
                    g3worst = max(g3worst, abs(mine[0]["max_abs_dW"] - rr.max_abs_dW))
                if pname == "U56":
                    g4 = [g for g in grid if g["panel"] == pname and g["gate"] == gate
                          and g["dial"] == "ABS n0=E_t"][0]["k_mean"]

    G = pd.DataFrame(grid)
    S = pd.DataFrame(steps)
    S320 = pd.DataFrame(steps320)
    C = pd.DataFrame(ceil_rows)
    W = pd.DataFrame(wf)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    S.to_csv(f"{OUT}.steps.csv", index=False)
    S320.to_csv(f"{OUT}.steps_i320grid.csv", index=False)
    C.to_csv(f"{OUT}.ceiling.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)

    P(f"G2  idea 320 grid.csv reproduction (MA+VOL gate, 5 ABS points, 6 columns): worst |d| "
      + "  ".join(f"{k} {v:.2e}" for k, v in g2worst.items())
      + f"   {'PASS' if max(g2worst.values()) < 5e-3 else 'FAIL'}")
    P(f"G3  idea 320 saturation.csv max|dW| reproduction: worst |d| over {g3n} steps {g3worst:.3e}   "
      f"{'PASS' if g3worst < 1e-12 else 'FAIL'}")
    P(f"G4  idea 320 'the panel saturates at 37.5 eligible names': U56 k_mean at n0=E_t = "
      f"{g4:.4f}   {'PASS' if abs(g4 - 37.4999) < 0.01 else 'FAIL'}")
    assert max(g2worst.values()) < 5e-3 and g3worst < 1e-12 and abs(g4 - 37.4999) < 0.01
    P("")

    P("THE CEILING (max_t E_t): every published dial point at or above it is a no-op by "
      "construction.")
    P(C.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    P("")

    P("THE CLOSED FORM. A step is an exact no-op iff its LOWER dial point >= the panel-gate "
      "ceiling.")
    ALL = pd.concat([S, S320], ignore_index=True)
    agree = int((ALL.identical == ALL.predicted_noop).sum())
    P(f"  predicted vs realised over all {len(ALL)} re-derived steps "
      f"({len(S)} on this script's grid + {len(S320)} on idea 320's): {agree}/{len(ALL)} agree "
      f"({agree / len(ALL):.1%}); "
      f"{'IDENTITY HOLDS' if agree == len(ALL) else 'IDENTITY FAILS — see steps.csv'}")
    P(f"  max|dr| over every step flagged identical: "
      f"{ALL.loc[ALL.identical, 'max_abs_dr'].max() if ALL.identical.any() else float('nan'):.3e} "
      "(zero weight difference => zero return difference, as it must be)")
    P("")

    P("RE-DERIVED NO-OP RATE, by panel x gate")
    for sub, lab in ((S, "this script's 9-point grid (8 steps per panel-gate)"),
                     (S320, "idea 320's OWN published 5-point grid (4 steps per panel-gate)")):
        t = sub.groupby(["panel", "gate"]).agg(steps=("identical", "size"),
                                               noop=("identical", "sum"),
                                               mean_days_same=("days_identical", "mean"))
        t["rate"] = t.noop / t.steps
        P(f"\n  over {lab}:")
        P("  " + t.to_string(float_format=lambda x: f"{x:.3f}").replace("\n", "\n  "))
        P(f"  TOTAL {int(sub.identical.sum())}/{len(sub)} = {sub.identical.mean():.1%} of steps "
          "move nothing.")
    P("")

    P("PARTIAL no-ops: the share of DAYS on which an adjacent step changes no weight at all")
    pv = S.pivot_table(index=["panel", "gate"], columns="step", values="days_identical")
    P(pv.to_string(float_format=lambda x: f"{x:.3f}"))
    P("")

    P("THE FULL GRID (81 books + 9 benchmark rows, ALL points reported)")
    show = ["panel", "gate", "dial", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "k_mean", "sat", "p4a", "p4b", "fail4b"]
    P(G[show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    P("KEEP PATHS at all 81 grid points (PROTOCOL 4a and 4b, both evaluated)")
    gg = G[G.gate != "BENCH"]
    P(f"  4a passes: {int(gg.p4a.sum())}/{len(gg)}   4b passes: {int(gg.p4b.sum())}/{len(gg)}   "
      f"BOTH: {int((gg.p4a & gg.p4b).sum())}/{len(gg)}")
    fl = pd.Series([x for s in gg.fail4b for x in s.split(",") if x != "-"]).value_counts()
    P("  binding 4b legs across the failures: " + ", ".join(f"{k} {v}" for k, v in fl.items()))
    if gg.p4b.any():
        P("  4b passers:")
        P("  " + gg[gg.p4b][show].to_string(index=False, float_format=lambda x: f"{x:.4f}")
          .replace("\n", "\n  "))
        dupes = []
        for _, r in gg[gg.p4b].iterrows():
            st = S[(S.panel == r.panel) & (S.gate == r.gate) & (S.identical) &
                   ((S.from_dial == r.dial) | (S.to_dial == r.dial))]
            if len(st):
                dupes.append(f"{r.panel}/{r.gate}/{r.dial}")
        P(f"  of which sit on a NO-OP step (i.e. are a re-publication of the neighbouring "
          f"point, not an independent pass): {len(dupes)} — {', '.join(dupes) if dupes else 'none'}")
    P("")

    P("RULE 8 (PROTOCOL 8): n0 chosen on IS <= 2016-12-31 by IS Sharpe, 2017- read once.")
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  picks whose IS-argmax is NOT unique (decided by sort order, not by data): "
      f"{int((W.tie_set > 1).sum())}/{len(W)}")
    P("")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
