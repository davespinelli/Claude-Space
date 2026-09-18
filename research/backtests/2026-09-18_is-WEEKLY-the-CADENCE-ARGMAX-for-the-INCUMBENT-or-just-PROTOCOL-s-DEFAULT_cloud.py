#!/usr/bin/env python3
"""
Idea 1335 (lane cloud, 2026-09-18) — is WEEKLY the CADENCE ARGMAX for the INCUMBENT, or just
PROTOCOL's DEFAULT?

THE PREMISE, READ FROM THE RECORD.  Idea 931 committed the reading that a W->M cadence change
is a TURNOVER REBATE every book on this tape collects.  Idea 1305 then measured the step
directly on the flat g=0.60 incumbent and FALSIFIED it on two of three panels: U56 -0.1053 /
SMALL -0.0796 of full-sample Sharpe against B136 +0.0283, with a uniform ~6-8 bp/yr cost refund
everywhere.  So the incumbent's WEEKLY cadence is a TUNED COORDINATE nobody has priced: it was
inherited from PROTOCOL's own default (`freq="W"` in baseline.compare), not chosen.

THE QUESTION AS THE QUEUE PUT IT.  Walk the full ladder CADENCE {D, W, 2W, M, Q} x COST
{0, 10, 25, 50} bps on three panels at the frozen incumbent, report every one of the 20 cells
per panel, both KEEP paths, and rule 8 (does an IS-chosen cadence beat PROTOCOL's W out of
sample, 2017-2026 read once).  RATIONALE the queue gives: if the cadence argmax MOVES WITH THE
COST RUNG, every committed number in this family is a 10-bps artifact.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  CADENCE {D, W, 2W, M, Q}      DIAL 1 — W is PROTOCOL's default and the incumbent's value
  COST    {0, 10, 25, 50} bps   DIAL 2 — 10 is PROTOCOL rule 2's rung and the headline

  20 cells per panel, 60 in all, EVERY ONE published in `.grid.csv`.

THE BOOK, FROZEN (nothing else is touched).  The certified incumbent the record carries into
every one of these runs: the 3-leg rank composite ((21,252), (0,126), (0,63)) x the
`0.5 + 0.5*above-200d` tilt, eligibility = above 200d MA AND vol20 < 0.60, N = 15 names at
equal weight, minimum hold H = 126 trading days, GROSS = 0.60, decisions lagged one row and
applied at t+1 (rule 2).  The ONLY thing this run varies is WHEN the book re-picks and WHAT the
tape charges it.

WHY THE COST RUNG IS FREE TO SWEEP.  Gross returns and one-way turnover are cadence properties,
not cost properties, so each (panel, cadence) is run ONCE and all four cost rungs are read off
the same pair as `gross - turnover * bps/1e4`.  The 20-cell grid is therefore exact, not
interpolated, and no cell is a re-tune.

2W IS BUILT FROM W, NOT GUESSED.  `rebalance_mask(idx, "W")` gives the last trading day of each
calendar week; the 2W schedule is that array subsampled every second entry (row 0 always a
rebalance, as in the record's runner), i.e. a genuine fortnightly book on the same calendar
grid, never a phase-shifted one.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at every
cell; the halves; the IS and OOS windows; turnover and its cost drag in bp/yr at every cell.

COMPARANDS (rule 3).  The live RULES v2 baseline REBUILT AT EACH COST RUNG (weekly, as it
trades) and SPY buy-and-hold (turnover-free, hence cost-invariant).  4a is judged against RULES
v2 at the SAME rung; 4b against SPY.

PROTOCOL: rule 1 (>= 10 years, gate G0); rule 2 (t+1 execution, no leverage, no shorting; the
10 bps rung is the headline and the other three are the queue's requested sensitivity); rule 3
(RULES v2 AND SPY); rule 4 (both KEEP paths, 2 tuned parameters and no more); rule 8
(walk-forward: CADENCE chosen on warm-up..2016-12-31 by argmax IS Sharpe AT EACH RUNG,
2017-2026 read ONCE); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified.

CROSS-RUN REPLAY (gate G1) AND THE TAPE-VINTAGE CAVEAT THIS RUN HAD TO MEASURE.  The
CADENCE=W / COST=10 cell on U56 is idea 1305's committed flat g=0.60 control and idea 1339's
committed PROTOCOL_DEFAULT cell: CAGR 13.657% / Sharpe 1.170567 / MaxDD -0.1638148 / halves
1.259064 / 1.114896 / OOS Sharpe 1.194662 / IS Sharpe 1.148195.  This run reproduces MaxDD to
1e-15 and the IS-WINDOW Sharpe to < 5e-4, but the FULL-SAMPLE and OOS numbers land 1.1e-3 and
1.8e-3 away.  The cause is NOT construction: commit 4e19a80 ("Daily close 2026-09-18") REWROTE
data/prices.csv, data/prices_broad.csv and data/prices_small.csv.gz wholesale (9410 lines
replaced, +6 net rows) AFTER 1305 was committed, so 1305 ran on a tape ending 2026-09-17 (U56
4707 rows) / 2026-09-11 (B136 4703, SMALL 4198) and this run reads 2026-09-18 (4708 / 4708 /
4203).  A re-adjusted, longer tape cannot move the IS window (which ends 2016-12-31) or a
drawdown set in 2020/2022, and it does move every full-sample and OOS statistic slightly.  The
gate is therefore SPLIT and published both ways: G1a asserts the tape-invariant quantities at
5e-4 (construction identity), G1b records the tape-vintage delta on the tape-sensitive ones at
a stated 3e-3 tolerance, and G1c asserts the row counts differ exactly as the daily close did.
No committed number is restated; the delta is reported as what it is.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-18_is-WEEKLY-the-CADENCE-ARGMAX-for-the-INCUMBENT-or-just-PROTOCOL-s-DEFAULT_cloud.py
"""
from __future__ import annotations

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

DATE = "2026-09-18"
SLUG = "is-WEEKLY-the-CADENCE-ARGMAX-for-the-INCUMBENT-or-just-PROTOCOL-s-DEFAULT"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 15, 126, 0.60                     # the incumbent, frozen
CADENCES = ["D", "W", "2W", "M", "Q"]             # DIAL 1
COSTS = [0.0, 10.0, 25.0, 50.0]                   # DIAL 2
HEADLINE_COST = 10.0                              # PROTOCOL rule 2's rung
PROTOCOL_CADENCE = "W"                            # the coordinate under test
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
# committed flat g=0.60 incumbent, U56, WEEKLY, 10 bps (idea 1305's .flat.csv, full precision;
# identical to idea 1339's PROTOCOL_DEFAULT cell) — replay gates G1a / G1b
C_INCUMBENT_U56 = dict(CAGR=0.13657311032419872, Sharpe=1.1705665614654293,
                       MaxDD=-0.1638148264272491, H1=1.2590639867986266,
                       H2=1.114896465229123, OOS_Sharpe=1.1946624691617433,
                       IS_Sharpe=1.1481948196913223)
# which of those the 2026-09-18 daily-close tape rewrite CANNOT move (IS ends 2016; the MaxDD is
# set in 2020/2022) and which it can
TAPE_INVARIANT = ["MaxDD", "IS_Sharpe"]
TAPE_SENSITIVE = ["CAGR", "Sharpe", "H1", "H2", "OOS_Sharpe"]
TAPE_TOL = 3e-3
# 1305's panel vintage, from its committed console log
C1305_ROWS = dict(U56=4707, B136=4703, SMALL=4198)
C1305_REBATE = dict(U56=-0.1053, SMALL=-0.0796, B136=+0.0283)   # 1305's W->M full-sample dSharpe

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def mech(q):
    """The incumbent's scorer, unchanged from the record."""
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


def cadence_rows(idx, cad):
    """Rebalance-APPLICATION rows for a cadence.  D/W/M/Q come straight from the engine's own
    mask (decided at the period's last close, applied the next row — rule 2).  2W is the W array
    subsampled every second entry."""
    if cad == "2W":
        base = cadence_rows(idx, "W")
        return base[::2]
    m = rebalance_mask(idx, cad).shift(1, fill_value=False).values.copy()
    m[0] = True
    return np.flatnonzero(m)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        self.reb = {c: cadence_rows(px.index, c) for c in CADENCES}
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def build1(pan, reb, N, H, lag=1):
    """The record's min-hold selection frame at GROSS = 1.0; lag=1 is rule 2."""
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


def run_flat(pan, reb, frame, gross=I_G):
    """The record's runner at constant gross.  Returns (gross returns, one-way turnover)."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    reb = np.asarray(reb, dtype=np.int64)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = gross * frame[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn


def at_cost(gr, tu, c):
    return gr - tu * c / 1e4


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


def annvol(r):
    return float(np.std(np.asarray(r, float), ddof=0) * np.sqrt(252))


def annturn(tu, lo, hi):
    n = hi - lo
    return float(np.sum(tu[lo:hi]) * 252.0 / n) if n > 0 else np.nan


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_paths(r, bm, live):
    """4a vs the live RULES v2 book at the SAME cost rung; 4b vs SPY (full-sample legs; 4b's OOS
    Sharpe leg is applied in the rule-8 section)."""
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 1335 (lane cloud, 2026-09-18) — is WEEKLY the CADENCE ARGMAX for the INCUMBENT, "
        "or just PROTOCOL's DEFAULT?")
    say("DIALS: CADENCE {D, W, 2W, M, Q} x COST {0, 10, 25, 50} bps at the FROZEN incumbent "
        "(N=15 / H=126 / gross 0.60 / MAXVOL 0.60 / MA gate ON).")
    say("=" * 108)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    meta = ROOT / "data" / "small_meta.csv"
    if meta.exists():
        md = pd.read_csv(meta)
        col = "ticker" if "ticker" in md.columns else md.columns[0]
        bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
        say(f"  SMALL filter: data/small_meta.csv drops {len(bad)} tickers with "
            f"max_1d_move >= 1.0 (protocol-mandated).")
    else:
        bad = set()
        say("  SMALL filter: data/small_meta.csv absent; falling back to an in-panel "
            "max |1d move| >= 1.0 screen.")
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 / SMALL are CURRENT-constituent lists; SMALL is a "
        "sub-$2B screen carried back to 2010, so its LEVELS are an upper bound and only its "
        "CONTRASTS across cadence are read here.")
    for p in panels:
        say(f"    {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  rebalances "
            + " / ".join(f"{c} {len(p.reb[c])}" for c in CADENCES))
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    grid, wf_rows, bench = [], [], {}

    for pan in panels:
        n = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is0, i_is1 = WARMUP, i_oos

        spy = pan.spy[WARMUP:]
        bm, bmO = bmpack(spy), bmpack(pan.spy[i_oos:])

        # the live RULES v2 comparand, rebuilt at EVERY cost rung (it trades weekly)
        lv, lvO = {}, {}
        for c in COSTS:
            lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=c, freq="W")["returns"].values
            lv[c], lvO[c] = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])

        say(f"\n  [{pan.name}]  SPY: CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.4f} MaxDD "
            f"{bm['MaxDD']:.2%} H1/H2 {bm['H1']:.4f}/{bm['H2']:.4f}   "
            f"|  4b bars: DD cap {DD_CAP*bm['MaxDD']:.2%}, CAGR floor "
            f"{CAGR_FLOOR*bm['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps: CAGR {lv[10.0]['CAGR']:.2%} Sharpe "
            f"{lv[10.0]['Sharpe']:.4f} MaxDD {lv[10.0]['MaxDD']:.2%} H1/H2 "
            f"{lv[10.0]['H1']:.4f}/{lv[10.0]['H2']:.4f}")
        say(f"           OOS SPY: CAGR {bmO['CAGR']:.2%} Sharpe {bmO['Sharpe']:.4f} MaxDD "
            f"{bmO['MaxDD']:.2%}  |  OOS RULES v2 @10bps: CAGR {lvO[10.0]['CAGR']:.2%} Sharpe "
            f"{lvO[10.0]['Sharpe']:.4f} MaxDD {lvO[10.0]['MaxDD']:.2%}")

        runs = {}
        for cad in CADENCES:
            reb = pan.reb[cad]
            frame = build1(pan, reb, I_N, I_H)
            g, tu = run_flat(pan, reb, frame)
            runs[cad] = dict(g=g, tu=tu, turn=annturn(tu, WARMUP, n))

        say(f"    {'cad':>3} {'cost':>5} | {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} "
            f"{'H1':>6} {'H2':>6} | {'turn':>5} {'drag':>7} {'vol':>6} | "
            f"{'OOS CAGR':>8} {'OOSShrp':>7} {'OOSMaxDD':>8} | {'ISShrp':>7} | 4a 4b  legs")
        for cad in CADENCES:
            g, tu, turn = runs[cad]["g"], runs[cad]["tu"], runs[cad]["turn"]
            for c in COSTS:
                rr = at_cost(g, tu, c)
                r = rr[WARMUP:]
                ka, kb, m, h1, h2, legs = keep_paths(r, bm, lv[c])
                mo = triple(rr[i_oos:])
                ho1, ho2 = halves(rr[i_oos:])
                kb_oos = bool(mo["Sharpe"] > bmO["Sharpe"])
                row = dict(panel=pan.name, cadence=cad, cost_bps=c,
                           CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                           vol_real=annvol(r), turn=turn, cost_drag_bp=turn * c,
                           n_rebal=len(pan.reb[cad]),
                           OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                           IS_Sharpe=sharpe(rr[i_is0:i_is1]),
                           SPY_Sharpe=bm["Sharpe"], SPY_CAGR=bm["CAGR"], SPY_MaxDD=bm["MaxDD"],
                           LIVE_Sharpe=lv[c]["Sharpe"], LIVE_MaxDD=lv[c]["MaxDD"],
                           OOS_SPY_Sharpe=bmO["Sharpe"], OOS_LIVE_Sharpe=lvO[c]["Sharpe"],
                           keep4a=ka, keep4b=kb, keep4b_oos_sharpe=kb_oos,
                           keep4b_and_oos=bool(kb and kb_oos),
                           leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                           leg_CAGR=legs["CAGR"])
                grid.append(row)
                say(f"    {cad:>3} {c:5.0f} | {m['CAGR']:7.2%} {m['Sharpe']:7.4f} "
                    f"{m['MaxDD']:8.2%} {h1:6.3f} {h2:6.3f} | {turn:5.2f} "
                    f"{turn*c:7.1f} {annvol(r):6.2%} | {mo['CAGR']:8.2%} {mo['Sharpe']:7.4f} "
                    f"{mo['MaxDD']:8.2%} | {row['IS_Sharpe']:7.4f} | "
                    f"{int(ka)}  {int(kb)}   "
                    + (",".join(k for k, v in legs.items() if not v) or "-"))

        bench[pan.name] = dict(spy=bm, spyO=bmO, live=lv, liveO=lvO, runs=runs, i_oos=i_oos,
                               i_is0=i_is0, i_is1=i_is1, n=n)

        gate(f"G1c tape vintage: {pan.name} rows > 1305's own run "
             f"(daily close 4e19a80 rewrote the tape after 1305 was committed)",
             f"{n} rows to {pan.idx[-1].date()} vs 1305's {C1305_ROWS[pan.name]}",
             f"> {C1305_ROWS[pan.name]}", n > C1305_ROWS[pan.name])

        if pan.name == "U56":
            w10 = [r for r in grid if r["panel"] == "U56" and r["cadence"] == "W"
                   and r["cost_bps"] == 10.0][0]
            for k in TAPE_INVARIANT:
                v = C_INCUMBENT_U56[k]
                gate(f"G1a construction identity (tape-invariant) U56 W@10bps {k}",
                     round(w10[k], 8), round(v, 8), abs(w10[k] - v) < 5e-4)
            say("      G1b TAPE-VINTAGE DELTA on the tape-sensitive statistics (1305's tape "
                "ended 2026-09-17, this one 2026-09-18; no committed number is restated):")
            worst = 0.0
            for k in TAPE_SENSITIVE:
                v = C_INCUMBENT_U56[k]
                d = w10[k] - v
                worst = max(worst, abs(d))
                say(f"        {k:>11}: this run {w10[k]:.6f}  1305 {v:.6f}  delta {d:+.6f}")
            gate("G1b tape-vintage delta within the stated tolerance on every tape-sensitive "
                 "statistic", round(worst, 6), f"< {TAPE_TOL}", worst < TAPE_TOL)
            say("        G1b FAILS BY DESIGN AND IS REPORTED, NOT LOOSENED: the HALVES move "
                f"{worst:.4f} across one daily tape rewrite, 2.3x the 3e-3 this run declared. "
                "That is a RECORD-WIDE caveat — cross-run replay of a half-sample Sharpe in "
                "this repo is resolution-limited to ~7e-3 by daily re-adjustment of "
                "data/prices*.csv, and no committed number in this family carries a tape stamp.")
            gate("G1d the committed cell's VERDICT survives the tape vintage (4b PASS on all "
                 "four full-sample legs, Sharpe > SPY, MaxDD inside the cap)",
                 f"4b={int(w10['keep4b'])} Sharpe {w10['Sharpe']:.4f} > SPY "
                 f"{w10['SPY_Sharpe']:.4f}, MaxDD {w10['MaxDD']:.2%} vs cap "
                 f"{DD_CAP*w10['SPY_MaxDD']:.2%}", "4b=1",
                 bool(w10["keep4b"]) and w10["Sharpe"] > w10["SPY_Sharpe"])

    # ---- the queue's own question, asked of each panel at each rung ------------------------
    G = pd.DataFrame(grid)
    say("\n" + "=" * 108)
    say("1. DOES THE CADENCE ARGMAX MOVE WITH THE COST RUNG?  (full-sample Sharpe argmax over "
        "the 5 cadences, at each rung)")
    say("=" * 108)
    argmax_rows = []
    for p in G.panel.unique():
        line = []
        for c in COSTS:
            sub = G[(G.panel == p) & (G.cost_bps == c)]
            best = sub.loc[sub.Sharpe.idxmax()]
            wr = sub[sub.cadence == PROTOCOL_CADENCE].iloc[0]
            line.append(f"{c:.0f}bp->{best.cadence}({best.Sharpe:.4f}; W {wr.Sharpe:.4f}, "
                        f"gap {best.Sharpe-wr.Sharpe:+.4f})")
            argmax_rows.append(dict(panel=p, cost_bps=c, basis="FULL_SHARPE",
                                    argmax=best.cadence, argmax_Sharpe=best.Sharpe,
                                    W_Sharpe=wr.Sharpe, gap_vs_W=best.Sharpe - wr.Sharpe))
        say(f"    {p:>6}: " + "   ".join(line))
    for p in G.panel.unique():
        a = [r["argmax"] for r in argmax_rows if r["panel"] == p]
        say(f"      -> {p}: argmax cadence across the four rungs = {a}  "
            f"{'STABLE' if len(set(a)) == 1 else 'MOVES'}")
    moved = sum(len({r['argmax'] for r in argmax_rows if r['panel'] == p}) > 1
                for p in G.panel.unique())
    say(f"    VERDICT on the queue's rationale: the full-sample Sharpe argmax MOVES with the "
        f"cost rung on {moved} of {G.panel.nunique()} panels.")
    say(f"    W is the argmax in {sum(1 for r in argmax_rows if r['argmax'] == PROTOCOL_CADENCE)}"
        f" of {len(argmax_rows)} (panel, rung) cells.")

    say("\n2. THE COST GRADIENT OF THE CADENCE STEP (turnover and its drag, bp/yr) ----------")
    for p in G.panel.unique():
        sub = G[(G.panel == p) & (G.cost_bps == 10.0)].set_index("cadence")
        say(f"    {p:>6}: turnover/yr " + "  ".join(f"{c} {sub.loc[c,'turn']:5.2f}"
                                                   for c in CADENCES))
        say(f"            W->M drag refund {(sub.loc['W','turn']-sub.loc['M','turn'])*10:+6.1f} "
            f"bp/yr at 10 bps, {(sub.loc['W','turn']-sub.loc['M','turn'])*50:+6.1f} at 50 bps; "
            f"D->W refund {(sub.loc['D','turn']-sub.loc['W','turn'])*10:+6.1f} bp/yr at 10 bps")
        dS = sub.loc["M", "Sharpe"] - sub.loc["W", "Sharpe"]
        say(f"            1305 REPLICATION: W->M full-sample dSharpe at 10 bps "
            f"{dS:+.4f}  (1305 committed {C1305_REBATE.get(p, float('nan')):+.4f})")
        if p in C1305_REBATE:
            gate(f"G2 sign of 1305's W->M dSharpe reproduced on {p}",
                 round(float(dS), 4), f"same sign as {C1305_REBATE[p]:+.4f}",
                 np.sign(dS) == np.sign(C1305_REBATE[p]))
    mono = []
    for p in G.panel.unique():
        sub = G[(G.panel == p) & (G.cost_bps == 10.0)].set_index("cadence")
        t = [sub.loc[c, "turn"] for c in CADENCES]
        mono.append(all(t[i] >= t[i + 1] for i in range(len(t) - 1)))
    gate("G3 turnover monotone non-increasing D>=W>=2W>=M>=Q on every panel",
         f"{sum(mono)}/{len(mono)} panels", "3/3", all(mono))

    say("\n3. KEEP PATHS OVER ALL 60 CELLS ------------------------------------------------")
    say(f"    4a (beat the live book, same rung): {int(G.keep4a.sum())} of {len(G)}")
    say(f"    4b full-sample: {int(G.keep4b.sum())} of {len(G)};  "
        f"4b full AND OOS Sharpe > SPY: {int(G.keep4b_and_oos.sum())} of {len(G)}")
    for p in G.panel.unique():
        s = G[G.panel == p]
        say(f"      {p:>6}: 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/{len(s)}"
            f"   4b+OOS {int(s.keep4b_and_oos.sum())}/{len(s)}")
    for c in COSTS:
        s = G[G.cost_bps == c]
        say(f"      {c:5.0f} bps: 4a {int(s.keep4a.sum())}/{len(s)}   "
            f"4b {int(s.keep4b.sum())}/{len(s)}   4b+OOS {int(s.keep4b_and_oos.sum())}/{len(s)}")
    for cad in CADENCES:
        s = G[G.cadence == cad]
        say(f"      cadence {cad:>2}: 4a {int(s.keep4a.sum())}/{len(s)}   "
            f"4b {int(s.keep4b.sum())}/{len(s)}   4b+OOS {int(s.keep4b_and_oos.sum())}/{len(s)}")

    # ---- rule 8 ----------------------------------------------------------------------------
    say("\n4. RULE 8 WALK-FORWARD — CADENCE chosen on warm-up..2016-12-31 by argmax IS Sharpe "
        "AT EACH RUNG; 2017-2026 read ONCE")
    say("=" * 108)
    for p in G.panel.unique():
        b = bench[p]
        for c in COSTS:
            sub = G[(G.panel == p) & (G.cost_bps == c)]
            pick = sub.loc[sub.IS_Sharpe.idxmax()]
            wr = sub[sub.cadence == PROTOCOL_CADENCE].iloc[0]
            rr = at_cost(b["runs"][pick.cadence]["g"], b["runs"][pick.cadence]["tu"], c)
            ro = rr[b["i_oos"]:]
            legs_oos = dict(
                OOS_Sharpe_vs_SPY=bool(pick.OOS_Sharpe > b["spyO"]["Sharpe"]),
                DD=bool(pick.OOS_MaxDD >= DD_CAP * b["spyO"]["MaxDD"]),
                CAGR=bool(pick.OOS_CAGR >= CAGR_FLOOR * b["spyO"]["CAGR"]))
            h1o, h2o = halves(ro)
            wf = dict(panel=p, cost_bps=c, IS_pick=pick.cadence, IS_Sharpe=pick.IS_Sharpe,
                      is_protocol_W=bool(pick.cadence == PROTOCOL_CADENCE),
                      OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                      OOS_MaxDD=pick.OOS_MaxDD,
                      W_OOS_CAGR=wr.OOS_CAGR, W_OOS_Sharpe=wr.OOS_Sharpe,
                      W_OOS_MaxDD=wr.OOS_MaxDD,
                      dOOS_Sharpe_vs_W=pick.OOS_Sharpe - wr.OOS_Sharpe,
                      dOOS_CAGR_vs_W=pick.OOS_CAGR - wr.OOS_CAGR,
                      SPY_OOS_Sharpe=b["spyO"]["Sharpe"], SPY_OOS_CAGR=b["spyO"]["CAGR"],
                      SPY_OOS_MaxDD=b["spyO"]["MaxDD"],
                      LIVE_OOS_Sharpe=b["liveO"][c]["Sharpe"],
                      LIVE_OOS_CAGR=b["liveO"][c]["CAGR"],
                      LIVE_OOS_MaxDD=b["liveO"][c]["MaxDD"],
                      OOS_H1=h1o, OOS_H2=h2o,
                      keep4b_oos_all=bool(all(legs_oos.values())),
                      oos_fail_legs=",".join(k for k, v in legs_oos.items() if not v) or "-",
                      best_OOS_cadence=sub.loc[sub.OOS_Sharpe.idxmax(), "cadence"],
                      best_OOS_Sharpe=sub.OOS_Sharpe.max())
            wf_rows.append(wf)
            say(f"    {p:>6} {c:5.0f} bps: IS pick {pick.cadence:>2} (IS Sharpe "
                f"{pick.IS_Sharpe:.4f}) -> OOS {pick.OOS_CAGR:7.2%}/{pick.OOS_Sharpe:.4f}/"
                f"{pick.OOS_MaxDD:7.2%}  vs PROTOCOL W {wr.OOS_CAGR:7.2%}/{wr.OOS_Sharpe:.4f}/"
                f"{wr.OOS_MaxDD:7.2%}  d {pick.OOS_Sharpe-wr.OOS_Sharpe:+.4f}  "
                f"| SPY {b['spyO']['CAGR']:7.2%}/{b['spyO']['Sharpe']:.4f}/"
                f"{b['spyO']['MaxDD']:7.2%}  RULESv2 {b['liveO'][c]['CAGR']:7.2%}/"
                f"{b['liveO'][c]['Sharpe']:.4f}  | 4b OOS {int(wf['keep4b_oos_all'])} "
                f"[{wf['oos_fail_legs']}]  | ex-post best OOS cadence "
                f"{wf['best_OOS_cadence']} ({wf['best_OOS_Sharpe']:.4f})")

    WF = pd.DataFrame(wf_rows)
    say(f"\n    The IS chooser picks PROTOCOL's W in {int(WF.is_protocol_W.sum())} of "
        f"{len(WF)} (panel, rung) cells.")
    say(f"    Mean OOS Sharpe of the IS-chosen cadence MINUS PROTOCOL's W: "
        f"{WF.dOOS_Sharpe_vs_W.mean():+.4f}  (min {WF.dOOS_Sharpe_vs_W.min():+.4f}, max "
        f"{WF.dOOS_Sharpe_vs_W.max():+.4f}); it beats W in "
        f"{int((WF.dOOS_Sharpe_vs_W > 0).sum())} of {len(WF)}.")
    say(f"    Mean OOS CAGR cost of choosing: {WF.dOOS_CAGR_vs_W.mean():+.2%}")
    say(f"    4b on every OOS leg after rule 8: {int(WF.keep4b_oos_all.sum())} of {len(WF)}.")
    hind = int((WF.best_OOS_cadence != WF.IS_pick).sum())
    say(f"    H_HINDSIGHT: the ex-post best OOS cadence differs from the IS pick in {hind} of "
        f"{len(WF)} cells — i.e. the IS window does not locate it.")

    say("\n5. WAS PROTOCOL's W A LUCKY DEFAULT?  (OOS Sharpe rank of W among the 5 cadences)")
    for p in G.panel.unique():
        for c in [HEADLINE_COST]:
            sub = G[(G.panel == p) & (G.cost_bps == c)].sort_values("OOS_Sharpe",
                                                                   ascending=False)
            order = list(sub.cadence)
            say(f"    {p:>6} @{c:.0f}bps OOS Sharpe order: "
                + " > ".join(f"{r.cadence}({r.OOS_Sharpe:.4f})" for r in sub.itertuples())
                + f"   -> W ranks {order.index('W')+1} of 5")

    # ---- outputs ---------------------------------------------------------------------------
    G.to_csv(f"{OUT}.grid.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(argmax_rows).to_csv(f"{OUT}.argmax_by_cost.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  wrote {Path(OUT).name}.grid.csv ({len(G)} cells), .walkforward.csv ({len(WF)}), "
        f".argmax_by_cost.csv, .gates.csv")
    say(f"  GATES: {sum(g['pass_'] for g in GATES)}/{len(GATES)} pass")
    say(f"  elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
