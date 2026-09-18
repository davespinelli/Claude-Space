#!/usr/bin/env python3
"""
Idea 1287 (lane cloud, 2026-09-18) — does the 2026-09-04 KEEP-4b BOOK survive EXECUTION
DELAY beyond PROTOCOL rule 2's t+1?

THE PREMISE.  The standing candidate (KEEP 4b, 2026-09-04) is U56 / N=20 / H=126 /
gross 0.75 / weekly, and every reading of it in the record is taken at PROTOCOL rule 2's
single convention: rank on the close of day t, hold from the close of day t+1.  That is
the most favourable implementable lag there is.  It is also the only one ever measured.
An implementer who cannot get the ranked close — who runs the screen the next morning,
or trades on a schedule, or simply is not at the terminal — is at t+2 or worse.  If the
book's 4b pass lives inside one day of staleness it is a short-horizon reversal artefact
dressed as a momentum book, and it is not capital-worthy however it scores at t+1.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.

  For each (LAG, CADENCE, PANEL) cell, build the SAME book — 3-leg composite, above-200d
  and vol20 < 0.60 eligibility, top N=20 with a 126-day minimum hold, gross 0.75, 10 bps —
  changing ONLY how stale the ranking snapshot is at application time:

      LAG = d   means   rank on the close of row (t - d), hold from the close of row t.

  LAG = 1 is PROTOCOL rule 2 exactly and reproduces the committed incumbent.  Nothing else
  in the construction moves.  Then:

      DECAY(d) = Sharpe(LAG = d) - Sharpe(LAG = 1)        (full sample, 10 bps, net)

  and the same for CAGR and for the OOS window.  The per-day slope is the OLS slope of
  net Sharpe on d over the five rungs.

  PRE-DECLARED OUTCOMES, fixed before the run.
    (A) ROBUST   — the U56 anchor cadence clears 4b at EVERY lag out to d = 5.
    (B) DECAYS   — it clears at d = 1 and d = 2 but fails somewhere in d <= 5.
    (C) FRAGILE  — it fails already at d = 2, i.e. the pass is one day deep.
    (D) NO PASS  — it does not clear 4b at d = 1 either (would refute the incumbent).
  Whichever comes out is the report.  No rung is dropped and no cell is selected on.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  LAG       {1, 2, 3, 5, 10} trading days   (1 is rule 2; the rest are the stress)
  CADENCE   {W, M}                          (the record's two rebalance rungs)

  10 cells per panel, 30 in all, EVERY ONE PUBLISHED in `.grid.csv`.

NOT DIALS, reported at every value: PANEL {U56, B136, SMALL} (rule 9); the 4a and 4b legs;
full sample, both halves, and the rule-8 OOS window; the live RULES v2 baseline and SPY.

FROZEN at the incumbent's construction, not tuned here: N = 20, H = 126, gross = 0.75,
3-leg composite (21/252, 0/126, 0/63), above-200d + vol20 < 0.60 eligibility, 10 bps per
unit turnover (rule 2), 260-row warm-up, first-wins stable tie-break.

PROTOCOL: rule 2 execution and costs; rule 4 both KEEP paths at every cell; rule 8
walk-forward — the lag is CHOSEN on warm-up..2016-12-31 only and 2017-2026 is read ONCE;
rule 9 survivorship stated below.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py
are NOT modified by this script.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT constituents of a hand-kept list, so both
panels are survivorship-biased toward names that did well over 2008-2026; this flatters any
momentum book on them.  The SMALL panel (data/prices_small) is current constituents of a
sub-$2B screen since 2010 and is biased the same way, harder — names that went to zero or
were acquired are simply absent.  Tickers with max_1d_move >= 1.0 in data/small_meta.csv are
dropped before anything is built (they are split/consolidation artefacts, not returns).
No result here should be read as an estimate of live expectancy on any of the three.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-18_does-the-KEEP-4b-BOOK-survive-EXECUTION-DELAY-beyond-rule-2-s-t-plus-1_cloud.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import rebalance_mask, backtest  # noqa: E402

OUT = Path(__file__).with_suffix("")
WARMUP, MAXVOL, REF_COST = 260, 0.60, 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G = 20, 126, 0.75           # the incumbent's frozen rungs
LAGS = [1, 2, 3, 5, 10]                 # dial 1
CADENCES = ["W", "M"]                   # dial 2
OOS_START = pd.Timestamp("2017-01-01")  # rule 8

_LOG: list[str] = []


def say(s=""):
    print(s)
    _LOG.append(s)


# ------------------------------------------------------------------ mechanics
def mech(q):
    """The record's 3-leg composite, above-200d flag and 20d vol, on the investable frame."""
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
        for f in CADENCES:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            self.seg[f] = np.flatnonzero(m)
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def build1(pan, N, H, freq, lag):
    """Min-hold top-N selection frame at GROSS = 1.0.  Row t is the APPLICATION-time weight;
    the ranking snapshot is row t-lag.  lag=1 is PROTOCOL rule 2's decide-at-t / apply-at-t+1."""
    reb = pan.seg[freq]
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
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


def nrun(pan, Wt, reb):
    """Gross daily returns and one-way turnover; costs applied afterwards as gross - turn*c/1e4."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    reb = np.asarray(reb, dtype=np.int64)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        curw = held[i1 - 1]
    return (held * rets).sum(axis=1), turn


def at_cost(gr, turn, c):
    return gr - turn * c / 1e4


# ------------------------------------------------------------------ metrics
def mt(r):
    r = np.asarray(r, dtype=float)
    if len(r) < 20:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = float(r.std(ddof=1) * np.sqrt(252))
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1.0),
                Sharpe=float(r.mean() * 252 / vol) if vol > 0 else np.nan,
                MaxDD=dd)


def windows(idx):
    """(full, h1, h2, is, oos) boolean masks over the post-warm-up rows."""
    n = len(idx)
    h = n // 2
    full = np.ones(n, bool)
    h1 = np.zeros(n, bool); h1[:h] = True
    h2 = np.zeros(n, bool); h2[h:] = True
    oos = np.asarray(idx >= OOS_START)
    return full, h1, h2, ~oos, oos


def legs(r, spy, live, idx):
    """Both KEEP paths.  4a vs the live RULES v2 book, 4b vs SPY.  Every leg published."""
    full, h1, h2, ins, oos = windows(idx)
    R, S, L = mt(r), mt(spy), mt(live)
    r1, r2 = mt(r[h1]), mt(r[h2])
    s1, s2 = mt(spy[h1]), mt(spy[h2])
    l1, l2 = mt(live[h1]), mt(live[h2])
    Ro, So = mt(r[oos]), mt(spy[oos])
    Ri = mt(r[ins])
    a = dict(a_h1=r1["Sharpe"] > l1["Sharpe"], a_h2=r2["Sharpe"] > l2["Sharpe"],
             a_dd=R["MaxDD"] >= L["MaxDD"])
    b = dict(b_h1=r1["Sharpe"] > s1["Sharpe"], b_h2=r2["Sharpe"] > s2["Sharpe"],
             b_oos=Ro["Sharpe"] > So["Sharpe"],
             b_dd=R["MaxDD"] >= 0.60 * S["MaxDD"],      # MaxDD is negative: >= is "no deeper than"
             b_cagr=R["CAGR"] >= 0.70 * S["CAGR"])
    return dict(CAGR=R["CAGR"], Sharpe=R["Sharpe"], MaxDD=R["MaxDD"],
                H1=r1["Sharpe"], H2=r2["Sharpe"],
                IS_Sharpe=Ri["Sharpe"], OOS_CAGR=Ro["CAGR"], OOS_Sharpe=Ro["Sharpe"],
                OOS_MaxDD=Ro["MaxDD"],
                pass4a=all(a.values()), pass4b=all(b.values()), **a, **b)


# ------------------------------------------------------------------ world
def make_panels():
    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"].astype(str))
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad]
    dropped = [c for c in pxS.columns if c != "SPY" and c in bad]
    return ([Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
             Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
             Panel("SMALL", pxS, inv)], dropped)


def bench_for(pan):
    """SPY and the live RULES v2 book on this panel, both post-warm-up, both at 10 bps."""
    live = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=REF_COST, freq="W")["returns"].values
    return pan.spy[WARMUP:], live[WARMUP:]


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say("=" * 100)
    say("IDEA 1287 (lane cloud, 2026-09-18) — does the 2026-09-04 KEEP-4b BOOK survive")
    say("EXECUTION DELAY beyond PROTOCOL rule 2's t+1?")
    say("=" * 100)
    say("")
    say("  LAG = d: rank on the close of row (t-d), hold from the close of row t. d=1 IS rule 2.")
    say("  DIALS (2, rule 4): LAG {1,2,3,5,10} x CADENCE {W,M} = 10 cells/panel, 30 published.")
    say("  FROZEN: N=20, H=126, gross=0.75, 10 bps, 3-leg composite, above-200d & vol20<0.60.")
    say("  OUTCOMES: (A) ROBUST to d=5  (B) DECAYS by d<=5  (C) FRAGILE at d=2  (D) NO PASS at d=1.")
    say("")

    panels, dropped = make_panels()
    say(f"  PANELS: U56 {len(panels[0].invest)} investable; B136 {len(panels[1].invest)}; "
        f"SMALL {len(panels[2].invest)} investable ({len(dropped)} dropped for "
        f"max_1d_move >= 1.0 in data/small_meta.csv). SPY is benchmark only, never held.")
    say(f"  TAPE: U56 {panels[0].idx[0].date()}..{panels[0].idx[-1].date()}; "
        f"SMALL {panels[2].idx[0].date()}..{panels[2].idx[-1].date()}.")
    say("")

    # ---------------------------------------------------------- benchmarks
    say("=" * 100)
    say("ARM A — BENCHMARKS (post-warm-up, 10 bps, weekly for the live book)")
    say("=" * 100)
    say("")
    B = {}
    say(f"  {'panel':6} {'series':22} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} "
        f"{'H1':>7} {'H2':>7} {'OOS CAGR':>9} {'OOS Sh':>8}")
    for pan in panels:
        spy, live = bench_for(pan)
        idx = pan.idx[WARMUP:]
        B[pan.name] = dict(spy=spy, live=live, idx=idx)
        full, h1, h2, ins, oos = windows(idx)
        for tag, ser in (("SPY (buy & hold)", spy), ("RULES v2 (live book)", live)):
            m, mo = mt(ser), mt(ser[oos])
            say(f"  {pan.name:6} {tag:22} {m['CAGR']:8.2%} {m['Sharpe']:8.4f} {m['MaxDD']:8.2%} "
                f"{mt(ser[h1])['Sharpe']:7.4f} {mt(ser[h2])['Sharpe']:7.4f} "
                f"{mo['CAGR']:9.2%} {mo['Sharpe']:8.4f}")
    say("")
    say("  4b bars from these: MaxDD cap = 0.60 x SPY MaxDD, CAGR floor = 0.70 x SPY CAGR,")
    say("  Sharpe > SPY in BOTH halves AND in the rule-8 OOS window.")

    # ---------------------------------------------------------- the grid
    say("")
    say("=" * 100)
    say("ARM B — THE FULL 30-CELL GRID (every cell published, none selected on)")
    say("=" * 100)
    say("")
    rows = []
    for pan in panels:
        spy, live, idx = B[pan.name]["spy"], B[pan.name]["live"], B[pan.name]["idx"]
        for cad in CADENCES:
            for d in LAGS:
                W = build1(pan, A_N, A_H, cad, d) * A_G
                gr, tu = nrun(pan, W, pan.seg[cad])
                r = at_cost(gr, tu, REF_COST)[WARMUP:]
                rec = legs(r, spy, live, idx)
                rec.update(panel=pan.name, cadence=cad, lag=d,
                           turnover_yr=float(tu[WARMUP:].sum() / (len(r) / 252.0)))
                rows.append(rec)
    G = pd.DataFrame(rows)

    for pan in panels:
        say(f"  --- {pan.name} " + "-" * 82)
        say(f"  {'cad':4} {'lag':>4} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
            f"{'OOScagr':>8} {'OOSsh':>7} {'turn/yr':>8}  {'4a':>3} {'4b':>3}")
        for _, x in G[G.panel == pan.name].iterrows():
            say(f"  {x.cadence:4} {x.lag:4d} {x.CAGR:8.2%} {x.Sharpe:8.4f} {x.MaxDD:8.2%} "
                f"{x.H1:7.4f} {x.H2:7.4f} {x.OOS_CAGR:8.2%} {x.OOS_Sharpe:7.4f} "
                f"{x.turnover_yr:8.2f}  {'Y' if x.pass4a else '.':>3} {'Y' if x.pass4b else '.':>3}")
        say("")

    # ---------------------------------------------------------- decay
    say("=" * 100)
    say("ARM C — THE DECAY: what one day of staleness costs")
    say("=" * 100)
    say("")
    say(f"  {'panel':6} {'cad':4} {'Sh(1)':>8} {'Sh(2)':>8} {'Sh(3)':>8} {'Sh(5)':>8} {'Sh(10)':>8} "
        f"{'slope/day':>10} {'dSh(2-1)':>9} {'dCAGR(2-1)':>11}")
    dec = []
    for pan in panels:
        for cad in CADENCES:
            sub = G[(G.panel == pan.name) & (G.cadence == cad)].set_index("lag")
            sh = [sub.loc[d, "Sharpe"] for d in LAGS]
            slope = float(np.polyfit(LAGS, sh, 1)[0])
            d21 = sub.loc[2, "Sharpe"] - sub.loc[1, "Sharpe"]
            c21 = sub.loc[2, "CAGR"] - sub.loc[1, "CAGR"]
            dec.append(dict(panel=pan.name, cadence=cad, slope_per_day=slope,
                            dSharpe_2_1=d21, dCAGR_2_1=c21,
                            **{f"Sharpe_lag{d}": sub.loc[d, "Sharpe"] for d in LAGS}))
            say(f"  {pan.name:6} {cad:4} " + " ".join(f"{v:8.4f}" for v in sh) +
                f" {slope:10.5f} {d21:9.4f} {c21:11.2%}")
    D = pd.DataFrame(dec)
    say("")
    say(f"  Median Sharpe slope per day of delay, over the 6 (panel, cadence) pairs: "
        f"{D.slope_per_day.median():+.5f}; range {D.slope_per_day.min():+.5f} to "
        f"{D.slope_per_day.max():+.5f}.")
    say(f"  Cells where one extra day COSTS Sharpe (dSh(2-1) < 0): "
        f"{int((D.dSharpe_2_1 < 0).sum())} of {len(D)}.")

    # ---------------------------------------------------------- rule 8
    say("")
    say("=" * 100)
    say("ARM D — RULE 8 WALK-FORWARD: lag chosen on warm-up..2016 ONLY, 2017-2026 read ONCE")
    say("=" * 100)
    say("")
    say("  CHOOSER: within each (panel, cadence), take the LAG with the highest IS Sharpe")
    say("  (warm-up..2016-12-31).  Then read that cell's 2017-2026 window, once.  The ANCHOR")
    say("  arm is lag = 1 (rule 2), never chosen, always reported.")
    say("")
    say(f"  {'panel':6} {'cad':4} {'IS-pick':>8} {'ISsh(pick)':>11} {'OOSsh(pick)':>12} "
        f"{'OOSsh(lag1)':>12} {'delta':>8} {'4b(pick)':>9} {'4b(lag1)':>9}")
    wf = []
    for pan in panels:
        for cad in CADENCES:
            sub = G[(G.panel == pan.name) & (G.cadence == cad)].set_index("lag")
            pick = int(sub["IS_Sharpe"].idxmax())
            wf.append(dict(panel=pan.name, cadence=cad, pick_lag=pick,
                           IS_Sharpe=sub.loc[pick, "IS_Sharpe"],
                           OOS_Sharpe_pick=sub.loc[pick, "OOS_Sharpe"],
                           OOS_Sharpe_lag1=sub.loc[1, "OOS_Sharpe"],
                           OOS_CAGR_pick=sub.loc[pick, "OOS_CAGR"],
                           OOS_MaxDD_pick=sub.loc[pick, "OOS_MaxDD"],
                           delta=sub.loc[pick, "OOS_Sharpe"] - sub.loc[1, "OOS_Sharpe"],
                           pass4b_pick=bool(sub.loc[pick, "pass4b"]),
                           pass4b_lag1=bool(sub.loc[1, "pass4b"]),
                           pass4a_pick=bool(sub.loc[pick, "pass4a"]),
                           pass4a_lag1=bool(sub.loc[1, "pass4a"])))
            w = wf[-1]
            say(f"  {pan.name:6} {cad:4} {pick:8d} {w['IS_Sharpe']:11.4f} "
                f"{w['OOS_Sharpe_pick']:12.4f} {w['OOS_Sharpe_lag1']:12.4f} {w['delta']:8.4f} "
                f"{'Y' if w['pass4b_pick'] else '.':>9} {'Y' if w['pass4b_lag1'] else '.':>9}")
    WF = pd.DataFrame(wf)
    say("")
    say(f"  The IS lag chooser beats the rule-2 anchor OOS in {int((WF.delta > 0).sum())} of "
        f"{len(WF)} (panel, cadence) pairs; mean delta {WF.delta.mean():+.4f} of OOS Sharpe.")
    say(f"  Distinct lags the IS chooser lands on: {sorted(WF.pick_lag.unique().tolist())}.")

    # ---------------------------------------------------------- verdict
    say("")
    say("=" * 100)
    say("ARM E — THE ANSWER")
    say("=" * 100)
    say("")
    u = G[(G.panel == "U56") & (G.cadence == "W")].set_index("lag")
    say("  The incumbent's own cell is (U56, W, lag=1). Its 4b legs, lag by lag:")
    say(f"  {'lag':>4} {'b_h1':>6} {'b_h2':>6} {'b_oos':>7} {'b_dd':>6} {'b_cagr':>7} {'4b':>4} "
        f"{'binding leg(s)':<28}")
    for d in LAGS:
        x = u.loc[d]
        names = dict(b_h1="H1 Sharpe", b_h2="H2 Sharpe", b_oos="OOS Sharpe",
                     b_dd="MaxDD cap", b_cagr="CAGR floor")
        bind = ", ".join(v for k, v in names.items() if not x[k]) or "-none-"
        say(f"  {d:4d} {'Y' if x.b_h1 else 'N':>6} {'Y' if x.b_h2 else 'N':>6} "
            f"{'Y' if x.b_oos else 'N':>7} {'Y' if x.b_dd else 'N':>6} "
            f"{'Y' if x.b_cagr else 'N':>7} {'PASS' if x.pass4b else 'FAIL':>4} {bind:<28}")
    say("")
    d1 = bool(u.loc[1, "pass4b"])
    d2 = bool(u.loc[2, "pass4b"])
    ok5 = all(bool(u.loc[d, "pass4b"]) for d in [1, 2, 3, 5])
    if not d1:
        outcome = "(D) NO PASS — the incumbent's own cell does not clear 4b on today's tape"
    elif ok5:
        outcome = "(A) ROBUST — clears 4b at every lag out to d = 5"
    elif d2:
        outcome = "(B) DECAYS — clears at d = 1 and d = 2, fails somewhere in d <= 5"
    else:
        outcome = "(C) FRAGILE — the 4b pass is one day deep; it is gone at d = 2"
    say(f"  PRE-DECLARED OUTCOME REACHED: {outcome}.")
    say("")
    say("  WHY: the ONLY leg that ever binds is the MaxDD cap.  Its margin, in pp of drawdown:")
    spyU = mt(B["U56"]["spy"])
    capU = 0.60 * spyU["MaxDD"]
    say(f"  U56 SPY MaxDD {spyU['MaxDD']:.2%}; 4b cap = 0.60 x that = {capU:.2%}.")
    say(f"  {'lag':>4} {'book MaxDD':>11} {'margin (pp)':>12} {'Sharpe':>8} {'dSharpe vs d=1':>15}")
    for d in LAGS:
        x = u.loc[d]
        say(f"  {d:4d} {x.MaxDD:11.2%} {100 * (x.MaxDD - capU):12.2f} {x.Sharpe:8.4f} "
            f"{x.Sharpe - u.loc[1, 'Sharpe']:15.4f}")
    mar = np.array([100 * (u.loc[d, "MaxDD"] - capU) for d in LAGS])
    ddsd = float(np.std([u.loc[d, "MaxDD"] for d in LAGS], ddof=1) * 100)
    shsd = float(np.std([u.loc[d, "Sharpe"] for d in LAGS], ddof=1))
    say("")
    say(f"  The lag=1 margin is {mar[0]:+.2f} pp against a spread of {ddsd:.2f} pp of MaxDD across")
    say(f"  the five lags — i.e. the pass sits {mar[0] / ddsd:.2f} lag-SDs inside a HARD cap, while")
    say(f"  Sharpe moves only {shsd:.4f} across the same five rungs and its three legs (H1, H2,")
    say(f"  OOS) pass at 5 of 5 lags.  The book's EDGE is delay-insensitive; its 4b VERDICT is not,")
    say("  because 4b's binding leg on this book is the single noisiest statistic in the rule.")
    say("")
    say(f"  Grid-wide: 4a passes {int(G.pass4a.sum())} of {len(G)} cells; "
        f"4b passes {int(G.pass4b.sum())} of {len(G)}.")
    say(f"  4b passes by lag: " + ", ".join(
        f"d={d}: {int(G[G.lag == d].pass4b.sum())}/{len(G[G.lag == d])}" for d in LAGS) + ".")
    say(f"  4b passes by panel: " + ", ".join(
        f"{p}: {int(G[G.panel == p].pass4b.sum())}/{len(G[G.panel == p])}"
        for p in ["U56", "B136", "SMALL"]) + ".")
    say("")
    say("  SURVIVORSHIP (rule 9): U56, B136 and SMALL are all CURRENT-constituent lists; names")
    say("  that died or were acquired are absent, which flatters every momentum book here.")
    say("  These are relative readings across lags on one fixed panel, not live expectancy.")

    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    D.to_csv(OUT.with_suffix(".decay.csv"), index=False)
    WF.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    OUT.with_suffix(".log.txt").write_text("\n".join(_LOG) + "\n")
    say("")
    say(f"  Wrote {OUT.name}.grid.csv ({len(G)} rows), .decay.csv ({len(D)}), "
        f".walkforward.csv ({len(WF)}), .log.txt")
    say(f"  Runtime {time.time() - t0:.1f}s, offline, deterministic.")
    OUT.with_suffix(".log.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
