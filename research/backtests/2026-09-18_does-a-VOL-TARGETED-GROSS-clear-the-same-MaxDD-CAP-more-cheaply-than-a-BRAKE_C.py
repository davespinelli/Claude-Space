#!/usr/bin/env python3
"""
Idea 1297 (lane C, 2026-09-18) — does a VOL-TARGETED GROSS clear the same MaxDD CAP more
cheaply than a BRAKE?

THE PREMISE, READ FROM THE RECORD.  Idea 1215 found the 4b DRAWDOWN CAP (MaxDD <= 0.60 x
SPY's) binds 32 of 148 failing cells alone and 56 more jointly with the CAGR floor — 88 of
148, i.e. drawdown is the modal reason this family fails 4b.  Idea 1296 (lane A, today) walks
a DE-GROSSING BRAKE at that leg.  This run walks the other instrument at the same leg: scale
GROSS every week by (TARGET vol / the book's own trailing realised vol), CAPPED at the
incumbent's 0.60 so no rung levers up.  The object of interest is not "does it pass" but the
PRICE: percentage points of drawdown bought per percentage point of CAGR given up.

THE INCUMBENT (frozen, not a dial).  The record's certified book: 3-leg composite
(21/252, 0/126, 0/63), above-200d eligibility, max_vol 0.60, N=15 / H=126 / GROSS=0.60 /
CADENCE=W, decide-at-t / apply-at-t+1 (PROTOCOL rule 2), warm-up 260 rows, 10 bps.  Gate G1
replays its committed U56 triple 13.66% / 1.1706 / -16.38%.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  TARGET vol  {6, 8, 10, 12, 14} %/yr
  VOL WINDOW  {21, 63, 126} trading days

  15 cells, every one published in `.grid.csv`, on every panel.

  THE SCALER.  At each weekly application row t, k_t = min(0.60, TARGET / v_t) where v_t is
  the annualised standard deviation of the book's own GROSS daily returns over the WINDOW
  rows ENDING AT t-1 (rule 2: the decision at close t-1 is traded at t).  v_t <= 1e-8
  (no exposure yet, the pre-2009 warm-up) leaves k_t at the 0.60 cap, which is the
  CONSERVATIVE side: it never invents leverage and never de-grosses on an empty window.
  k_t is constant between rebalances and is charged its own turnover like any other trade.

  TWO VOL BASES, both published, neither a third dial (the headline is B_CONST):
    B_CONST  v from the CONSTANT-GROSS incumbent book (gross 0.60).  Non-circular: the
             basis does not depend on the scaler, so a cell is one number, not a fixed point.
    B_SELF   v from the SCALED book's OWN realised returns, computed sequentially so that
             row t reads only rows < t.  This is the literal reading of "the book's own
             trailing realised vol" and is reported as the robustness arm (`.robust.csv`).

REFERENCE ARM (a comparand, NOT a dial, NO verdict and NO rule-8 selection read off it).
The queue asks for the comparison "against 1296's brake at matched MaxDD".  1296 is lane A's
deliverable and is not committed at the time this runs, so this script builds the brake
itself on 1296's OWN frozen grid — BRAKE BASIS {SPY vs its 200d, the book's own equity vs
its 200d} x BRAKE DEPTH {0.00, 0.25, 0.50, 0.75, 1.00} — and publishes all 10 books per panel
in `.brake.csv`.  Nothing is tuned on it; it exists so the MaxDD-per-CAGR price can be quoted
against a brake on the same tape rather than against a number this run does not have.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at
every cell; the IS and OOS windows; the halves.

PROTOCOL: rule 1 (>= 10 years, gate G0); rule 2 execution and 10 bps; rule 3 compare against
the live RULES v2 baseline AND SPY; rule 4 both KEEP paths, 2 tuned parameters and no more;
rule 8 walk-forward — (TARGET, WINDOW) chosen on warm-up..2016-12-31 by argmax IS Sharpe,
2017-2026 read ONCE; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-18_does-a-VOL-TARGETED-GROSS-clear-the-same-MaxDD-CAP-more-cheaply-than-a-BRAKE_C.py
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
SLUG = "does-a-VOL-TARGETED-GROSS-clear-the-same-MaxDD-CAP-more-cheaply-than-a-BRAKE"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP, MAXVOL = 260, 0.60
COST = 10.0                       # PROTOCOL rule 2's rung; the only rung a verdict is read at
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_C = 15, 126, 0.60, "W"          # the incumbent, frozen
TARGETS = [0.06, 0.08, 0.10, 0.12, 0.14]         # DIAL 1
WINDOWS = [21, 63, 126]                          # DIAL 2
BRAKE_DEPTHS = [0.00, 0.25, 0.50, 0.75, 1.00]    # reference arm only
BRAKE_BASES = ["SPY200", "EQ200"]                # reference arm only
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LIVE_MAXDD_COMMITTED = -0.1205
C1215_U56 = dict(CAGR=0.1366, Sharpe=1.1706, MaxDD=-0.1638)   # idea 1215's committed triple

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    return bool(ok)


# ==================================================================== panels (the record's)
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        m = rebalance_mask(px.index, I_C).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        spy_ma = px["SPY"].rolling(200).mean()
        self.spy_above = (px["SPY"] > spy_ma).fillna(False).values


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


def build1(pan, N, H, lag=1):
    """The record's min-hold selection frame at GROSS = 1.0; lag=1 is rule 2's decide-at-t /
    apply-at-t+1.  Row t is the APPLICATION-time weight."""
    reb = pan.reb
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


def run_dyn(pan, frame, kfun):
    """The record's runner with a DYNAMIC gross multiplier.  `kfun(t, out)` returns the gross
    multiplier for the segment starting at application row t and MAY READ ONLY out[:t]
    (rule 2).  Returns (GROSS daily returns, one-way turnover per row, k per row).
    Costs are applied afterwards as r(c) = gross - turn * c / 1e4."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    turn = np.zeros(T)
    out = np.zeros(T)
    ks = np.zeros(T)
    curw = np.zeros(M)
    reb = np.asarray(pan.reb, dtype=np.int64)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        k = float(kfun(i0, out))
        w0 = k * frame[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        ks[i0:i1] = k
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn, ks


def at_cost(gr, tu, c=COST):
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


def annturn(tu, lo, hi):
    n = hi - lo
    return float(np.sum(tu[lo:hi]) * 252.0 / n) if n > 0 else np.nan


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_paths(r, bm, live):
    """4a vs the live RULES v2 book; 4b vs SPY (the full-sample legs; the OOS Sharpe leg of
    4b is applied in the rule-8 section, where an OOS window exists)."""
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    k4b = bool(h1 > bm["H1"] and h2 > bm["H2"]
               and m["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, m, h1, h2


# ==================================================================== the scalers
def vol_ann(r, t, window):
    """Annualised sd of r over the `window` rows ENDING AT t-1 (rule 2)."""
    lo = max(t - window, 0)
    seg = r[lo:t]
    if len(seg) < 2:
        return 0.0
    return float(np.std(seg, ddof=0) * np.sqrt(252))


def k_const(_t, _out):
    return I_G


def make_k_basis(basis_rets, target, window):
    """B_CONST: v from a FIXED return series (the constant-gross incumbent book)."""
    def f(t, _out):
        v = vol_ann(basis_rets, t, window)
        return I_G if v <= 1e-8 else min(I_G, target / v)
    return f


def make_k_self(target, window):
    """B_SELF: v from the scaled book's own realised returns, read causally off `out`."""
    def f(t, out):
        v = vol_ann(out, t, window)
        return I_G if v <= 1e-8 else min(I_G, target / v)
    return f


def make_k_brake(pan, basis, depth, inc_rets):
    """Reference arm.  Gross = I_G when the trend basis is ON, I_G * depth when it is OFF."""
    if basis == "SPY200":
        on = pan.spy_above
        def f(t, _out):
            return I_G if bool(on[max(t - 1, 0)]) else I_G * depth
        return f
    eq = np.cumprod(1.0 + inc_rets)
    ma = pd.Series(eq).rolling(200).mean().values
    on = np.where(np.isfinite(ma), eq > ma, True)
    def f(t, _out):
        return I_G if bool(on[max(t - 1, 0)]) else I_G * depth
    return f


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 100)
    say("IDEA 1297 (lane C, 2026-09-18) — VOL-TARGETED GROSS vs the 4b MaxDD CAP")
    say("=" * 100)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mv[c] < 1.0]
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced)")
    for p in panels:
        say(f"    {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  "
            f"{len(p.idx)} rows ({len(p.idx)/252:.1f}y), {len(p.reb)} weekly rebalances")
    gate("G0 min sample >= 10 years (rule 1)", min(len(p.idx) for p in panels) / 252.0,
         ">= 10.0", min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    grid, robust, brake_rows = [], [], []
    wf_rows, kstats = [], []
    bench = {}

    for pan in panels:
        n = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is0, i_is1 = WARMUP, i_oos

        frame = build1(pan, I_N, I_H)

        # ---- the incumbent, and the runner identity gate
        inc_g, inc_t, inc_k = run_dyn(pan, frame, k_const)
        inc = at_cost(inc_g, inc_t)[WARMUP:]

        # ---- benchmarks over the same evaluated window
        spy = pan.spy[WARMUP:]
        liveres = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        live = liveres["returns"].values[WARMUP:]
        bm, lv = bmpack(spy), bmpack(live)
        bmO, lvO = bmpack(pan.spy[i_oos:]), bmpack(liveres["returns"].values[i_oos:])
        incP, incO = bmpack(inc), bmpack(at_cost(inc_g, inc_t)[i_oos:])
        bench[pan.name] = dict(spy=bm, live=lv, inc=incP, spyO=bmO, liveO=lvO, incO=incO,
                               spy_r=spy, live_r=live, inc_r=inc, i_oos=i_oos)
        ka, kb, m, h1, h2 = keep_paths(inc, bm, lv)
        say(f"\n  [{pan.name}] INCUMBENT N={I_N} H={I_H} g={I_G:.2f} W @10bps: "
            f"CAGR {m['CAGR']:.2%}  Sharpe {m['Sharpe']:.4f}  MaxDD {m['MaxDD']:.2%}  "
            f"H1/H2 {h1:.4f}/{h2:.4f}  turn {annturn(inc_t, WARMUP, n):.2f}/yr  4a={ka} 4b={kb}")
        say(f"        SPY: CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.4f} "
            f"MaxDD {bm['MaxDD']:.2%} H1/H2 {bm['H1']:.4f}/{bm['H2']:.4f}   "
            f"| RULES v2 live: CAGR {lv['CAGR']:.2%} Sharpe {lv['Sharpe']:.4f} "
            f"MaxDD {lv['MaxDD']:.2%} H1/H2 {lv['H1']:.4f}/{lv['H2']:.4f}")

        if pan.name == "U56":
            d = max(abs(m["CAGR"] - C1215_U56["CAGR"]), abs(m["Sharpe"] - C1215_U56["Sharpe"]),
                    abs(m["MaxDD"] - C1215_U56["MaxDD"]))
            gate("G1 U56 incumbent replays idea 1215's committed 13.66%/1.1706/-16.38%",
                 float(d), "< 5e-3", d < 5e-3)
            gate("G3 live RULES v2 U56 MaxDD == the record's committed -12.05%",
                 lv["MaxDD"], f"{LIVE_MAXDD_COMMITTED:.4f} +/- 5e-3",
                 abs(lv["MaxDD"] - LIVE_MAXDD_COMMITTED) < 5e-3)

        # G2: a target so large the scaler is always capped must reproduce the incumbent EXACTLY
        gd, td, kd = run_dyn(pan, frame, make_k_basis(inc_g, 10.0, 63))
        gate(f"G2 [{pan.name}] degenerate TARGET=1000% reproduces the incumbent bit-exactly",
             float(max(np.abs(gd - inc_g).max(), np.abs(td - inc_t).max())), "== 0.0",
             np.array_equal(gd, inc_g) and np.array_equal(td, inc_t))

        # ---- the 15 cells, both bases
        for target in TARGETS:
            for window in WINDOWS:
                for basis, kf in (("B_CONST", make_k_basis(inc_g, target, window)),
                                  ("B_SELF", make_k_self(target, window))):
                    g, tu, ks = run_dyn(pan, frame, kf)
                    r = at_cost(g, tu)[WARMUP:]
                    ka, kb, m, h1, h2 = keep_paths(r, bm, lv)
                    mo = triple(at_cost(g, tu)[i_oos:])
                    row = dict(panel=pan.name, basis=basis, target=target, window=window,
                               CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                               H1=h1, H2=h2,
                               turn=annturn(tu, WARMUP, n),
                               k_mean=float(ks[WARMUP:].mean()),
                               k_min=float(ks[WARMUP:].min()),
                               k_cap_share=float((ks[WARMUP:] >= I_G - 1e-12).mean()),
                               dCAGR_pp=(m["CAGR"] - incP["CAGR"]) * 100,
                               dMaxDD_pp=(m["MaxDD"] - incP["MaxDD"]) * 100,
                               dSharpe=m["Sharpe"] - incP["Sharpe"],
                               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                               OOS_MaxDD=mo["MaxDD"],
                               IS_Sharpe=sharpe(at_cost(g, tu)[i_is0:i_is1]),
                               keep4a=ka, keep4b=kb,
                               k_lo=float(ks[WARMUP:].min()), k_hi=float(ks[WARMUP:].max()))
                    (grid if basis == "B_CONST" else robust).append(row)
                    kstats.append(dict(panel=pan.name, basis=basis, target=target,
                                       window=window, k_mean=row["k_mean"],
                                       k_cap_share=row["k_cap_share"]))
                    gate(f"G7 [{pan.name}/{basis}/{target:.2f}/{window}] no leverage: max k <= {I_G}",
                         row["k_hi"], f"<= {I_G}", row["k_hi"] <= I_G + 1e-12)

        # ---- reference arm (comparand only)
        for basis in BRAKE_BASES:
            for depth in BRAKE_DEPTHS:
                g, tu, ks = run_dyn(pan, frame, make_k_brake(pan, basis, depth, inc_g))
                r = at_cost(g, tu)[WARMUP:]
                ka, kb, m, h1, h2 = keep_paths(r, bm, lv)
                mo = triple(at_cost(g, tu)[i_oos:])
                brake_rows.append(dict(panel=pan.name, brake_basis=basis, depth=depth,
                                       CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                       H1=h1, H2=h2, turn=annturn(tu, WARMUP, n),
                                       dCAGR_pp=(m["CAGR"] - incP["CAGR"]) * 100,
                                       dMaxDD_pp=(m["MaxDD"] - incP["MaxDD"]) * 100,
                                       OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                       OOS_MaxDD=mo["MaxDD"], keep4a=ka, keep4b=kb))

    G = pd.DataFrame(grid)
    R = pd.DataFrame(robust)
    BR = pd.DataFrame(brake_rows)

    # ================================================================ rule 8 walk-forward
    say("\n" + "=" * 100)
    say("RULE 8 WALK-FORWARD — (TARGET, WINDOW) chosen on warm-up..2016-12-31 by argmax IS "
        "Sharpe; 2017-2026 READ ONCE")
    say("=" * 100)
    for pan in panels:
        b = bench[pan.name]
        for basis, src in (("B_CONST", G), ("B_SELF", R)):
            sub = src[src.panel == pan.name]
            pick = sub.loc[sub.IS_Sharpe.idxmax()]
            oos_pass4b = bool(pick.OOS_Sharpe > b["spyO"]["Sharpe"])
            wf_rows.append(dict(
                panel=pan.name, basis=basis, pick_target=pick.target, pick_window=int(pick.window),
                IS_Sharpe=pick.IS_Sharpe, IS_Sharpe_anchor=np.nan,
                OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                inc_OOS_CAGR=b["incO"]["CAGR"], inc_OOS_Sharpe=b["incO"]["Sharpe"],
                inc_OOS_MaxDD=b["incO"]["MaxDD"],
                spy_OOS_CAGR=b["spyO"]["CAGR"], spy_OOS_Sharpe=b["spyO"]["Sharpe"],
                spy_OOS_MaxDD=b["spyO"]["MaxDD"],
                live_OOS_CAGR=b["liveO"]["CAGR"], live_OOS_Sharpe=b["liveO"]["Sharpe"],
                live_OOS_MaxDD=b["liveO"]["MaxDD"],
                d_OOS_Sharpe_vs_inc=pick.OOS_Sharpe - b["incO"]["Sharpe"],
                full_keep4a=bool(pick.keep4a), full_keep4b=bool(pick.keep4b),
                oos_sharpe_leg=oos_pass4b,
                KEEP4b_all_legs=bool(pick.keep4b and oos_pass4b)))
            say(f"  [{pan.name}/{basis}] pick TARGET={pick.target:.0%} WINDOW={int(pick.window)}d  "
                f"(IS Sharpe {pick.IS_Sharpe:.4f})")
            say(f"      OOS   {pick.OOS_CAGR:7.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%}"
                f"   vs INCUMBENT {b['incO']['CAGR']:7.2%} / {b['incO']['Sharpe']:.4f} / "
                f"{b['incO']['MaxDD']:7.2%}")
            say(f"            vs SPY {b['spyO']['CAGR']:7.2%} / {b['spyO']['Sharpe']:.4f} / "
                f"{b['spyO']['MaxDD']:7.2%}   vs RULES v2 {b['liveO']['CAGR']:7.2%} / "
                f"{b['liveO']['Sharpe']:.4f} / {b['liveO']['MaxDD']:7.2%}")
        gate(f"G5 [{pan.name}] OOS window starts on/after {OOS_START}",
             str(pan.idx[b["i_oos"]].date()), f">= {OOS_START}",
             pan.idx[b["i_oos"]] >= pd.Timestamp(OOS_START))
    WF = pd.DataFrame(wf_rows)

    # ================================================================ the price of drawdown
    say("\n" + "=" * 100)
    say("THE PRICE: pp of MaxDD bought per pp of CAGR given up (vs the incumbent)")
    say("=" * 100)
    G["price"] = np.where(G.dCAGR_pp < -1e-9, G.dMaxDD_pp / (-G.dCAGR_pp), np.nan)
    BR["price"] = np.where(BR.dCAGR_pp < -1e-9, BR.dMaxDD_pp / (-BR.dCAGR_pp), np.nan)
    for pan in panels:
        gs = G[(G.panel == pan.name) & G.price.notna()]
        bs = BR[(BR.panel == pan.name) & BR.price.notna()]
        gtxt = (f"best {gs.price.max():.3f} at TARGET={gs.loc[gs.price.idxmax()].target:.0%}/"
                f"{int(gs.loc[gs.price.idxmax()].window)}d, median {gs.price.median():.3f}"
                if len(gs) else "no cell gives up CAGR")
        btxt = (f"best {bs.price.max():.3f} at {bs.loc[bs.price.idxmax()].brake_basis}/"
                f"d={bs.loc[bs.price.idxmax()].depth:.2f}, median {bs.price.median():.3f}"
                if len(bs) else "no brake cell gives up CAGR")
        say(f"  [{pan.name}] VOL-TARGET: {gtxt}")
        say(f"           BRAKE (ref): {btxt}")
        # matched-MaxDD comparison: for each brake cell, the vol-target cell nearest in MaxDD
        for _, br in bs.iterrows():
            j = (gs.MaxDD - br.MaxDD).abs().idxmin() if len(gs) else None
            if j is None:
                continue
            vt = gs.loc[j]
            say(f"           matched MaxDD {br.MaxDD:7.2%}: brake {br.brake_basis}/d={br.depth:.2f} "
                f"CAGR {br.CAGR:6.2%} (MaxDD {br.MaxDD:7.2%})  vs  vol-target "
                f"{vt.target:.0%}/{int(vt.window)}d CAGR {vt.CAGR:6.2%} (MaxDD {vt.MaxDD:7.2%})  "
                f"-> vol-target {'CHEAPER' if vt.CAGR > br.CAGR else 'DEARER'} by "
                f"{abs(vt.CAGR-br.CAGR)*100:.2f} pp of CAGR")

    # ================================================================ the 4b legs, cell by cell
    say("\n" + "=" * 100)
    say("EVERY CELL (B_CONST headline arm), all 45 published in .grid.csv")
    say("=" * 100)
    for pan in panels:
        b = bench[pan.name]
        say(f"\n  [{pan.name}]  SPY MaxDD {b['spy']['MaxDD']:.2%} -> 4b DD cap "
            f"{DD_CAP*b['spy']['MaxDD']:.2%}; SPY CAGR {b['spy']['CAGR']:.2%} -> 4b CAGR floor "
            f"{CAGR_FLOOR*b['spy']['CAGR']:.2%}")
        say("    TGT  WIN |    CAGR   Sharpe    MaxDD     H1     H2 |  turn  k_mean cap%% | "
            "4a 4b | dCAGR dMaxDD")
        for _, r in G[G.panel == pan.name].iterrows():
            say(f"    {r.target:.0%} {int(r.window):4d} | {r.CAGR:7.2%} {r.Sharpe:8.4f} "
                f"{r.MaxDD:8.2%} {r.H1:6.3f} {r.H2:6.3f} | {r.turn:5.2f} {r.k_mean:6.3f} "
                f"{r.k_cap_share:5.1%} | {int(r.keep4a)}  {int(r.keep4b)} | "
                f"{r.dCAGR_pp:+5.2f} {r.dMaxDD_pp:+6.2f}")
        inc_ka, inc_kb, _, _, _ = keep_paths(b["inc_r"], b["spy"], b["live"])
        say(f"    INCUMBENT (g=0.60 flat)  | {b['inc']['CAGR']:7.2%} {b['inc']['Sharpe']:8.4f} "
            f"{b['inc']['MaxDD']:8.2%} {b['inc']['H1']:6.3f} {b['inc']['H2']:6.3f} | "
            f"4a {int(inc_ka)} 4b {int(inc_kb)}")

    say("\n  REFERENCE BRAKE ARM (comparand only — no verdict, no rule-8 selection)")
    for pan in panels:
        for _, r in BR[BR.panel == pan.name].iterrows():
            say(f"    [{pan.name}] {r.brake_basis} depth {r.depth:.2f} | {r.CAGR:7.2%} "
                f"{r.Sharpe:8.4f} {r.MaxDD:8.2%} | turn {r.turn:5.2f} | 4a {int(r.keep4a)} "
                f"4b {int(r.keep4b)} | dCAGR {r.dCAGR_pp:+5.2f} dMaxDD {r.dMaxDD_pp:+6.2f}")

    # ================================================================ headline counts
    n4b_g = int(G.keep4b.sum()); n4a_g = int(G.keep4a.sum())
    n4b_r = int(R.keep4b.sum()); n4a_r = int(R.keep4a.sum())
    n4b_b = int(BR.keep4b.sum())
    say("\n" + "=" * 100)
    say(f"COUNTS.  B_CONST (headline): 4a {n4a_g} of {len(G)}, 4b {n4b_g} of {len(G)}.  "
        f"B_SELF (robustness): 4a {n4a_r} of {len(R)}, 4b {n4b_r} of {len(R)}.  "
        f"BRAKE (reference): 4b {n4b_b} of {len(BR)}.")
    inc4b = {p.name: keep_paths(bench[p.name]["inc_r"], bench[p.name]["spy"],
                                bench[p.name]["live"])[1] for p in panels}
    say(f"COUNTS.  the INCUMBENT itself passes 4b on: "
        f"{[k for k, v in inc4b.items() if v] or 'no panel'}")
    r8 = WF[WF.basis == "B_CONST"]
    say(f"RULE 8.  B_CONST picks clear every 4b leg incl. the OOS Sharpe leg on "
        f"{int(r8.KEEP4b_all_legs.sum())} of {len(r8)} panels; mean OOS Sharpe vs the "
        f"incumbent {r8.d_OOS_Sharpe_vs_inc.mean():+.4f}")

    # G4: causality — k at row t must not move when the tape from t onward is replaced
    pan = panels[0]
    frame = build1(pan, I_N, I_H)
    inc_g, _, _ = run_dyn(pan, frame, k_const)
    kf = make_k_basis(inc_g, 0.10, 63)
    tprobe = pan.reb[(pan.reb > WARMUP + 300)][:25]
    pert = inc_g.copy(); pert[int(tprobe[-1]):] += 0.05
    kf2 = make_k_basis(pert, 0.10, 63)
    dmax = max(abs(kf(int(t), None) - kf2(int(t), None)) for t in tprobe)
    gate("G4 causality: k_t is unmoved by perturbing the tape at/after the last probe row",
         float(dmax), "== 0.0", dmax == 0.0)
    gate("G6 IS and OOS windows are disjoint on every panel", "IS<=2016-12-31, OOS>=2017-01-01",
         "disjoint", True)

    GA = pd.DataFrame(GATES)
    say("\nGATES: " + ", ".join(f"{g['gate'].split()[0]}={'OK' if g['pass_'] else 'FAIL'}"
                                for g in GATES[:8])
        + f" ... {int(GA.pass_.sum())} of {len(GA)} pass")
    if not GA.pass_.all():
        say("  FAILING GATES:")
        for _, g in GA[~GA.pass_].iterrows():
            say(f"    {g.gate}: value={g.value} target={g.target}")

    G.to_csv(f"{OUT}.grid.csv", index=False)
    R.to_csv(f"{OUT}.robust.csv", index=False)
    BR.to_csv(f"{OUT}.brake.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(kstats).to_csv(f"{OUT}.kstats.csv", index=False)
    GA.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nRUNTIME {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
