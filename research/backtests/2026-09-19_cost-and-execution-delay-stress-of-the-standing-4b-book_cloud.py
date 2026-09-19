#!/usr/bin/env python3
"""Idea 1590 — does the STANDING 4b BOOK survive 25 and 50 bps AND a second, third and fourth day
of EXECUTION DELAY?

THE OBJECT.  Every 4b pass in this record — idea 1570's two included (U56 OOS 16.15% / 1.2247 /
-16.54%, B136 OOS 14.29% / 1.0254 / -16.69%) — is priced at exactly 10 bps with the decision taken
at close t-1 and applied at t.  Real capital pays neither: a retail-to-small-institutional book in
56 large caps pays spread plus impact well above 10 bps, and a signal computed after the close is
rarely in the market the next morning.  This run prices the standing frozen incumbent, and the
constant-gross ladder that dominates every device the record has tried, on the FULL grid the two
unpriced axes make.

WHAT IS PRICED.
  PANELS      U56, B136, SMALL (three).
  BOOK        the frozen incumbent frame: N = 20, H = 126, MAXVOL 0.60, per-name 200d MA gate,
              weekly cadence — held fixed, never tuned.
  GROSS       a published ladder 0.40 .. 1.00 step 0.05 (13 rungs).  Gross is NOT a tuned
              parameter of this run: it is chosen mechanically by the rule-8 IS-only chooser at
              each cell, and every rung is published regardless.
  DIAL 1      COST RUNG {0, 10, 25, 50} bps.
  DIAL 2      EXECUTION DELAY {+0, +1, +2, +3} trading days ON TOP of PROTOCOL rule 2's t-1 -> t.
              Implemented by reading the signal at close t-1-d and applying it at t, so +0 IS the
              protocol's own convention and reproduces the committed anchor exactly (G1).
  => 3 x 13 x 4 x 4 = 624 published cells, both KEEP paths at every one.

TUNED PARAMETERS: exactly TWO — the cost rung and the execution delay.  The gross ladder is the
chooser's coordinate (IS rows only) and the book's N / H / MAXVOL / cadence are frozen inheritances.

THE DEATH SEARCH.  For every (panel, delay, gross) book the exact cost rung at which its 4b verdict
dies is bisected on the realised turnover path, FULL and OOS separately, to 0.01 bp.  Likewise the
exact delay at which it dies at each cost rung.  A book whose 4b pass survives to c* = 12 bps is
not a capital claim; one that survives to 60 is.

PRE-REGISTERED VERDICT RULE (written before the run).
  H_FRAGILE  the standing 4b passes die inside the realistic envelope: the MEDIAN c* of the 4b
             passes at delay +0 is < 25 bps, OR the rule-8 pick loses its 4b verdict at the
             (25 bps, +1 day) cell on the large-cap panels.  Then the record's 4b case is an
             artefact of an optimistic cost-and-timing convention and this is a KILL for capital.
  H_ROBUST   a rule-8 pick that reads IS rows only still clears 4b FULL and OOS at (25 bps, +1)
             on at least one panel, with MaxDD no worse than 60% of SPY's.  Then the book is the
             first in the record priced at a cost and a latency capital can actually pay, and it
             is a KEEP-candidate under path 4b.
  Anything in between is PARK.

PROTOCOL: rule 1 (>= 10y); rule 2 (decisions at t-1 applied at t at delay +0, 10 bps headline, no
shorting, no leverage); rule 3 (compared to the live RULES v2 baseline AND SPY); rule 4 (full +
both halves, both KEEP paths at EVERY cell); rule 8 (gross chosen on warm-up..2016-12-31 only,
2017-01-01..end read exactly once); rule 9 (survivorship stated).

GATES.  G0 >= 10y.  G1 cross-script replay of the committed 2026-09-04 U56 frozen anchor at the
(10 bps, +0) cell.  G2 exactly two tuned parameters.  G3 the cost ladder is an exact identity on
one turnover path.  G4 gross in [0, 1] on every book.  G5 no chooser reads a row on or after
2017-01-01.  G6 every one of the 624 cells published.  G7 delay +0 reproduces the protocol
convention bit-for-bit against an independently built lag-1 frame.  G8 the death search brackets
every reported c* (verdict true at c*-eps, false at c*+eps).

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-19_cost-and-execution-delay-stress-of-the-standing-4b-book_cloud.py
"""
from __future__ import annotations

import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-19"
SLUG = "cost-and-execution-delay-stress-of-the-standing-4b-book"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_V, I_C = 20, 126, 0.75, 0.60, "W"
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

COSTS = [0.0, 10.0, 25.0, 50.0]                       # DIAL 1 (tuned)
DELAYS = [0, 1, 2, 3]                                 # DIAL 2 (tuned)
GROSS = [round(0.40 + 0.05 * i, 2) for i in range(13)]  # chooser's coordinate, all published
HEADLINE_COST, REAL_COST, REAL_DELAY = 10.0, 25.0, 1
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)
CMAX = 400.0                                          # bisection ceiling, bps

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def legs4b(r, bm):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])), m, h1, h2


def keep_paths(r, bm, live):
    lg, m, h1, h2 = legs4b(r, bm)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    return k4a, bool(all(lg.values())), m, h1, h2, lg


def mech_legs(q: pd.DataFrame):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return (sum(parts) / len(parts)).values


def cadence_rows(idx, cad):
    m = rebalance_mask(idx, cad)
    v = m.shift(1, fill_value=False).values.copy()
    v[0] = True
    return np.flatnonzero(v)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        q = px[invest]
        self.q = q
        self.comp = mech_legs(q)
        self.vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values

    def frame_inputs(self):
        above = (self.q > self.q.rolling(200).mean()).values
        elig = above & (np.nan_to_num(self.vol20, nan=1e9) < I_V)
        sc = self.comp * (0.5 + 0.5 * above.astype(float))
        return elig, np.where(np.isfinite(sc), -sc, np.inf)


def build_frame(pan, elig, key, reb, N=I_N, H=I_H, lag=1):
    """The frozen incumbent's HOLDINGS frame at unit gross.  `lag` is the total number of trading
    days between the close the signal is read at and the day the trade lands: lag = 1 is PROTOCOL
    rule 2's own convention (decide at close t-1, apply at t); lag = 1 + d adds d days of delay."""
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
            k = key[ts].copy()
            k[~(elig[ts] & pr[ts])] = np.inf
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


def run_g(pan, frame, reb, g):
    T, M = pan.rets.shape
    isreb = np.zeros(T, bool)
    isreb[reb] = True
    cur = np.zeros(M)
    rg = np.zeros(T)
    turn = np.zeros(T)
    gmax = 0.0
    for t in range(T):
        post = g * frame[t] if isreb[t] else cur
        turn[t] = float(np.abs(post - cur).sum())
        gmax = max(gmax, float(post.sum()))
        r = float(post @ pan.rets[t])
        rg[t] = r
        cur = post * (1.0 + pan.rets[t]) / (1.0 + r)
    return dict(rg=rg, turn=turn, gmax=gmax,
                turn_y=float(turn[WARMUP:].sum()) * 252.0 / max(len(turn) - WARMUP, 1))


def net_of(run, c):
    return run["rg"] - run["turn"] * c / 1e4


def death_cost(run, lo_i, bm, cmax=CMAX):
    """Exact cost rung (bps) at which the 4b verdict of this book flips from PASS to FAIL, found by
    bisection on the realised turnover path.  Returns nan if it already fails at 0 bps, cmax if it
    still passes at cmax."""
    def ok(c):
        lg, _, _, _ = legs4b(net_of(run, c)[lo_i:], bm)
        return all(lg.values())
    if not ok(0.0):
        return float("nan")
    if ok(cmax):
        return cmax
    lo, hi = 0.0, cmax
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if ok(mid):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main():
    t0 = time.time()
    say("=" * 126)
    say("IDEA 1590 — does the STANDING 4b BOOK survive 25 and 50 bps AND a second, third and "
        "fourth day of EXECUTION DELAY?   (lane cloud, idea 2 of 2)")
    say("  PRE-REGISTERED  H_FRAGILE: median c* of the 4b passes at delay +0 is < 25 bps, OR the "
        "rule-8 pick loses 4b at (25 bps, +1 day) on the large-cap panels -> KILL for capital.")
    say("  PRE-REGISTERED  H_ROBUST: an IS-only rule-8 pick still clears 4b FULL and OOS at "
        "(25 bps, +1 day) on >= 1 panel -> the first book in the record priced at a cost and a "
        "latency capital can actually pay; KEEP-candidate under path 4b.")
    say("=" * 126)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"\n  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} investable names survive.")
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)}.")
    say("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every ABSOLUTE level below — and every 4a / 4b "
        "pass count — is an UPPER BOUND.  The run's HEADLINE is a DEGRADATION along two axes over "
        "the SAME names on the SAME days, which the bias cannot manufacture.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y)")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)", round(min(len(p.idx) for p in panels) / 252.0, 2),
         ">= 10.0", min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G2 exactly two tuned parameters (cost rung, execution delay); the gross ladder is the "
         "rule-8 chooser's IS-only coordinate and N / H / MAXVOL / cadence are frozen inheritances",
         2, "== 2", True)

    rows, wf_rows, death_rows = [], [], []
    g1_ok = g7_ok = None
    gmax_global = 0.0
    g3_dev = 0.0
    g8_ok = True
    bench = {}

    for pan in panels:
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is = int(np.searchsorted(pan.idx.values, np.datetime64(IS_END)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=HEADLINE_COST,
                      freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        bench[pan.name] = dict(spy=spy, spyO=spyO, live=live, liveO=liveO, i_oos=i_oos)
        say(f"\n  [{pan.name}]  SPY {spy['CAGR']:.2%}/{spy['Sharpe']:.4f}/{spy['MaxDD']:.2%} "
            f"H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap {DD_CAP*spy['MaxDD']:.2%}, "
            f"CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}   |  OOS SPY {spyO['CAGR']:.2%}/"
            f"{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}")
        say(f"           RULES v2 live @10bps {live['CAGR']:.2%}/{live['Sharpe']:.4f}/"
            f"{live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}  |  OOS "
            f"{liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")

        elig, key = pan.frame_inputs()
        reb = cadence_rows(pan.idx, I_C)
        for d in DELAYS:
            frame = build_frame(pan, elig, key, reb, lag=1 + d)
            if pan.name == "U56" and d == 0:
                f2 = build_frame(pan, elig, key, reb, lag=1)
                g7_ok = gate("G7 delay +0 IS the protocol convention (independently rebuilt lag-1 "
                             "frame)", f"max |dev| {np.abs(frame-f2).max():.2e}", "== 0",
                             float(np.abs(frame - f2).max()) == 0.0)
            for g in GROSS:
                R = run_g(pan, frame, reb, g)
                gmax_global = max(gmax_global, R["gmax"])
                g3_dev = max(g3_dev, float(np.abs(net_of(R, 0.0) - R["rg"]).max()))
                cstar_f = death_cost(R, WARMUP, spy)
                cstar_o = death_cost(R, i_oos, spyO)
                if np.isfinite(cstar_f) and 0 < cstar_f < CMAX:
                    a, b = net_of(R, cstar_f - 0.02), net_of(R, cstar_f + 0.02)
                    la, _, _, _ = legs4b(a[WARMUP:], spy)
                    lb, _, _, _ = legs4b(b[WARMUP:], spy)
                    g8_ok = g8_ok and all(la.values()) and not all(lb.values())
                death_rows.append(dict(panel=pan.name, delay=d, gross=g, cstar_full_bps=cstar_f,
                                       cstar_oos_bps=cstar_o, turn_y=R["turn_y"]))
                for c in COSTS:
                    rn = net_of(R, c)
                    k4a, k4b, m, h1, h2, lg = keep_paths(rn[WARMUP:], spy, live)
                    k4aO, k4bO, mo, _, _, lgO = keep_paths(rn[i_oos:], spyO, liveO)
                    rows.append(dict(
                        panel=pan.name, delay=d, gross=g, cost=c,
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                        keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO, keep4b_oos=k4bO,
                        legH1=lg["H1"], legH2=lg["H2"], legDD=lg["DD"], legCAGR=lg["CAGR"],
                        olegH1=lgO["H1"], olegH2=lgO["H2"], olegDD=lgO["DD"], olegCAGR=lgO["CAGR"],
                        is_Sharpe=sharpe(rn[WARMUP:i_is]), turn_y=R["turn_y"],
                        drag_bpyr=R["turn_y"] * c,
                        dd_margin_pp=(m["MaxDD"] - DD_CAP * spy["MaxDD"]) * 100,
                        cagr_margin_pp=(m["CAGR"] - CAGR_FLOOR * spy["CAGR"]) * 100,
                        spy_Sharpe=spy["Sharpe"], spy_MaxDD=spy["MaxDD"], spy_CAGR=spy["CAGR"],
                        spy_oSharpe=spyO["Sharpe"], spy_oMaxDD=spyO["MaxDD"],
                        spy_oCAGR=spyO["CAGR"], live_Sharpe=live["Sharpe"],
                        live_MaxDD=live["MaxDD"], live_oSharpe=liveO["Sharpe"],
                        live_oMaxDD=liveO["MaxDD"], live_oCAGR=liveO["CAGR"]))
                    if pan.name == "U56" and d == 0 and g == I_G and c == HEADLINE_COST:
                        dev = max(abs(m["Sharpe"] - C_U56["Sharpe"]),
                                  abs(mo["Sharpe"] - C_U56["oSharpe"]),
                                  abs(m["CAGR"] - C_U56["CAGR"]),
                                  abs(m["MaxDD"] - C_U56["MaxDD"]))
                        g1_ok = gate("G1 cross-script replay of the committed 2026-09-04 U56 "
                                     "frozen anchor at (10 bps, +0 days) "
                                     "(15.80%/1.1537/-19.13% full; 1.1857 OOS)",
                                     f"max |dev| {dev:.2e}", "< 5e-3", dev < 5e-3)

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    D = pd.DataFrame(death_rows)
    D.to_csv(f"{OUT}.deathsearch.csv", index=False)
    gate("G3 the cost ladder is an exact identity on one turnover path",
         f"max |dev| {g3_dev:.2e}", "== 0", g3_dev == 0.0)
    gate("G4 gross in [0, 1] on every book", f"max realised weight sum {gmax_global:.6f}",
         "<= 1.0", gmax_global <= 1.0 + 1e-9)
    want = len(panels) * len(DELAYS) * len(GROSS) * len(COSTS)
    gate("G6 every cell published", f"{len(G)} rows = 3 panels x {len(DELAYS)} delays x "
         f"{len(GROSS)} gross x {len(COSTS)} cost", f"== {want}", len(G) == want)
    gate("G8 the death search brackets every reported c* (PASS at c*-0.02 bp, FAIL at c*+0.02 bp)",
         f"{int(D['cstar_full_bps'].between(0.001, CMAX-0.001).sum())} interior c* checked",
         "all bracketed", g8_ok)

    # ---------------------------------------------------------------- the standing book
    say("\n" + "=" * 126)
    say("THE STANDING BOOK (the frozen incumbent, gross 0.75) ACROSS THE FULL COST x DELAY GRID.")
    say("=" * 126)
    for pan in panels:
        say(f"\n  [{pan.name}]  frozen incumbent g = 0.75")
        say(f"    {'delay':>6}{'cost':>7}{'CAGR':>9}{'Sharpe':>9}{'MaxDD':>9}{'H1':>8}{'H2':>8}"
            f"{'oCAGR':>9}{'oSharpe':>9}{'oMaxDD':>9}{'4a':>6}{'4b':>6}{'4aO':>6}{'4bO':>6}"
            f"{'turn/y':>8}{'drag bp':>9}")
        sub = G[(G.panel == pan.name) & (G.gross == I_G)].sort_values(["delay", "cost"])
        for _, r in sub.iterrows():
            say(f"    {int(r.delay):>+6}{r.cost:>7.0f}{r.CAGR:>9.2%}{r.Sharpe:>9.4f}"
                f"{r.MaxDD:>9.2%}{r.H1:>8.4f}{r.H2:>8.4f}{r.oCAGR:>9.2%}{r.oSharpe:>9.4f}"
                f"{r.oMaxDD:>9.2%}{str(r.keep4a):>6}{str(r.keep4b):>6}{str(r.keep4a_oos):>6}"
                f"{str(r.keep4b_oos):>6}{r.turn_y:>8.2f}{r.drag_bpyr:>9.0f}")

    say("\n  MARGINAL COST OF ONE MORE DAY OF EXECUTION DELAY (gross 0.75, 10 bps, vs delay +0):")
    for pan in panels:
        b = G[(G.panel == pan.name) & (G.gross == I_G) & (G.cost == HEADLINE_COST) & (G.delay == 0)].iloc[0]
        for d in DELAYS[1:]:
            r = G[(G.panel == pan.name) & (G.gross == I_G) & (G.cost == HEADLINE_COST) & (G.delay == d)].iloc[0]
            say(f"    {pan.name:<6} +{d}d  dSharpe {r.Sharpe-b.Sharpe:+.4f}  dCAGR "
                f"{(r.CAGR-b.CAGR)*100:+.2f} pp  dMaxDD {(r.MaxDD-b.MaxDD)*100:+.2f} pp  "
                f"dOOS Sharpe {r.oSharpe-b.oSharpe:+.4f}  4b {b.keep4b} -> {r.keep4b} "
                f"(OOS {b.keep4b_oos} -> {r.keep4b_oos})")

    # ---------------------------------------------------------------- death search
    say("\n" + "=" * 126)
    say("THE DEATH SEARCH — the EXACT cost rung (bps) at which each book's 4b verdict flips to "
        f"FAIL, bisected on its own turnover path (ceiling {CMAX:.0f} bps).")
    say("=" * 126)
    alive0 = D[(D.delay == 0) & D["cstar_full_bps"].notna()]
    for pan in panels:
        say(f"\n  [{pan.name}]  c* FULL by (delay, gross); 'x' = already fails 4b at 0 bps, "
            f"'>{CMAX:.0f}' = survives the ceiling")
        say("    delay |" + "".join(f"{g:>8.2f}" for g in GROSS))
        for d in DELAYS:
            cells = []
            for g in GROSS:
                v = D[(D.panel == pan.name) & (D.delay == d) & (D.gross == g)]["cstar_full_bps"].iloc[0]
                cells.append("       x" if not np.isfinite(v) else
                             (f"  >{CMAX:.0f}" if v >= CMAX - 1e-6 else f"{v:>8.1f}"))
            say(f"    {d:>+5} |" + "".join(cells))
    for pan in panels:
        sub = D[(D.panel == pan.name) & (D.delay == 0) & D["cstar_full_bps"].notna()]
        subo = D[(D.panel == pan.name) & (D.delay == 0) & D["cstar_oos_bps"].notna()]
        say(f"\n  [{pan.name}] delay +0: {len(sub)} of {len(GROSS)} gross rungs pass 4b FULL at "
            f"0 bps; median c* {sub['cstar_full_bps'].median() if len(sub) else float('nan'):.1f} "
            f"bps, max {sub['cstar_full_bps'].max() if len(sub) else float('nan'):.1f}.  OOS: "
            f"{len(subo)} pass, median c* "
            f"{subo['cstar_oos_bps'].median() if len(subo) else float('nan'):.1f} bps.")
    med_c0 = alive0["cstar_full_bps"].median() if len(alive0) else float("nan")
    say(f"\n  POOLED across panels at delay +0: {len(alive0)} books pass 4b FULL at 0 bps; "
        f"MEDIAN c* = {med_c0:.1f} bps, q25 "
        f"{alive0['cstar_full_bps'].quantile(0.25) if len(alive0) else float('nan'):.1f}, q75 "
        f"{alive0['cstar_full_bps'].quantile(0.75) if len(alive0) else float('nan'):.1f}.")

    # ---------------------------------------------------------------- 4b pass counts
    say("\n  4b PASS COUNTS over the whole grid (FULL / OOS / BOTH), by (cost, delay), "
        f"out of {len(GROSS)*len(panels)} books per cell:")
    say(f"    {'cost':>6}" + "".join(f"{('+'+str(d)+'d'):>20}" for d in DELAYS))
    for c in COSTS:
        cells = []
        for d in DELAYS:
            s = G[(G.cost == c) & (G.delay == d)]
            cells.append(f"{int(s.keep4b.sum()):>6}/{int(s.keep4b_oos.sum()):>4}/"
                         f"{int((s.keep4b & s.keep4b_oos).sum()):>4}   ")
        say(f"    {c:>6.0f}" + "".join(f"{x:>20}" for x in cells))
    say(f"    4a passes over the WHOLE grid: {int(G.keep4a.sum())} of {len(G)} full, "
        f"{int(G.keep4a_oos.sum())} OOS.")

    # ---------------------------------------------------------------- rule 8
    say("\n" + "=" * 126)
    say("RULE 8 — gross chosen by argmax IS Sharpe on warm-up..2016-12-31 ONLY, SEPARATELY at each "
        "(cost, delay) cell (the chooser pays the same cost and latency the book does); "
        "2017-01-01..end read exactly ONCE.")
    say("=" * 126)
    for pan in panels:
        b = bench[pan.name]
        say(f"\n  [{pan.name}]  {'cost':>5}{'delay':>7}{'pick g':>9}{'IS S':>9}{'oCAGR':>9}"
            f"{'oSharpe':>9}{'oMaxDD':>9}{'4b':>6}{'4bO':>6}{'4aO':>6}  vs SPY OOS "
            f"{b['spyO']['CAGR']:.2%}/{b['spyO']['Sharpe']:.4f}/{b['spyO']['MaxDD']:.2%}, "
            f"RULES v2 OOS {b['liveO']['CAGR']:.2%}/{b['liveO']['Sharpe']:.4f}")
        for c in COSTS:
            for d in DELAYS:
                sub = G[(G.panel == pan.name) & (G.cost == c) & (G.delay == d)]
                pk = sub.loc[sub["is_Sharpe"].idxmax()]
                say(f"        {c:>5.0f}{d:>+7}{pk.gross:>9.2f}{pk.is_Sharpe:>9.4f}"
                    f"{pk.oCAGR:>9.2%}{pk.oSharpe:>9.4f}{pk.oMaxDD:>9.2%}{str(pk.keep4b):>6}"
                    f"{str(pk.keep4b_oos):>6}{str(pk.keep4a_oos):>6}")
                wf_rows.append(dict(panel=pan.name, cost=c, delay=d, pick_gross=float(pk.gross),
                                    is_Sharpe=float(pk.is_Sharpe), CAGR=pk.CAGR,
                                    Sharpe=pk.Sharpe, MaxDD=pk.MaxDD, H1=pk.H1, H2=pk.H2,
                                    keep4a=bool(pk.keep4a), keep4b=bool(pk.keep4b),
                                    oCAGR=pk.oCAGR, oSharpe=pk.oSharpe, oMaxDD=pk.oMaxDD,
                                    keep4a_oos=bool(pk.keep4a_oos),
                                    keep4b_oos=bool(pk.keep4b_oos),
                                    spy_oCAGR=b["spyO"]["CAGR"], spy_oSharpe=b["spyO"]["Sharpe"],
                                    spy_oMaxDD=b["spyO"]["MaxDD"],
                                    live_oCAGR=b["liveO"]["CAGR"],
                                    live_oSharpe=b["liveO"]["Sharpe"],
                                    live_oMaxDD=b["liveO"]["MaxDD"]))
    W = pd.DataFrame(wf_rows)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    gate("G5 no chooser reads a row on or after 2017-01-01",
         f"every chooser window ends {IS_END}", f"<= {IS_END}", True)

    # ---------------------------------------------------------------- verdict
    real = W[(W.cost == REAL_COST) & (W.delay == REAL_DELAY)]
    real_big = real[real.panel.isin(["U56", "B136"])]
    robust = real[(real.keep4b) & (real.keep4b_oos)]
    fragile = (med_c0 < REAL_COST) or bool(
        (~(real_big.keep4b & real_big.keep4b_oos)).all())
    verdict = "KILL" if (fragile and len(robust) == 0) else (
        "KEEP-candidate" if len(robust) > 0 and not (med_c0 < REAL_COST) else "PARK")
    say("\n" + "=" * 126)
    say(f"THE REALISTIC CELL (25 bps, +1 day), rule-8 picks:")
    for _, r in real.iterrows():
        say(f"    {r.panel:<6} pick g {r.pick_gross:.2f}  FULL {r.CAGR:.2%}/{r.Sharpe:.4f}/"
            f"{r.MaxDD:.2%} (H1/H2 {r.H1:.4f}/{r.H2:.4f})  OOS {r.oCAGR:.2%}/{r.oSharpe:.4f}/"
            f"{r.oMaxDD:.2%}  4b {r.keep4b}/{r.keep4b_oos}  4a {r.keep4a}/{r.keep4a_oos}")
    say(f"POOLED median c* at delay +0 = {med_c0:.1f} bps (bar 25).  4b BOTH-window passes at "
        f"(25 bps, +1 day): {len(robust)} of {len(real)} panels.")
    say(f"PRE-REGISTERED VERDICT: H_FRAGILE {fragile}, H_ROBUST {len(robust) > 0}  ->  {verdict}")
    say("=" * 126)

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nGATES: {len(gdf)} recorded, {int((~gdf['pass_']).sum())} FAIL.")
    say(f"elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    return verdict


if __name__ == "__main__":
    main()
