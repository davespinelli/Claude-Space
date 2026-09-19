#!/usr/bin/env python3
"""
Idea 1296 (lane cloud, 2026-09-19) — does a DE-GROSSING DRAWDOWN BRAKE buy back the 4b MaxDD LEG
the record says is the BINDER?

THE PREMISE.  Idea 1215 found the 4b DD cap alone binds 32 of 148 failing cells and jointly with
the CAGR floor 56 more (88 of 148): drawdown is the MODAL reason this family fails 4b.  Idea 1253
sharpened it — the committed U56 pass clears the DD cap by only 1.10 pp, and one weekday of
execution slippage spends all of it.  A brake that cuts GROSS when a causal book-level trend
signal is off targets that leg directly and adds NO cross-sectional signal: it cannot pick names,
it can only be out of the way.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  BRAKE BASIS {NONE, SPY200, OWN200}      DIAL 1 — NONE is the frozen incumbent
  BRAKE DEPTH {0.00, 0.25, 0.50, 0.75, 1.00}   DIAL 2 — gross MULTIPLIER while braked; 1.00 = off

  15 cells per panel, 45 in all, EVERY ONE published in `.grid.csv` (including the rungs that are
  degenerate BY CONSTRUCTION: basis NONE is one book repeated at all five depths, and depth 1.00
  is that same book under every basis.  Those degeneracies are not hidden, they are the run's own
  internal replay gates G2 and G3.)

  BASIS DEFINITIONS, both read ONE ROW BEFORE the rebalance row (rule 2, no look-ahead):
    NONE    never braked; gross is the incumbent's 0.60 at every rebalance.
    SPY200  braked when SPY's close is NOT above its own 200d simple moving average.
    OWN200  braked when THE BOOK'S OWN equity curve is NOT above its own 200d moving average.
            This is path-dependent and is therefore computed INSIDE the rebalance loop from
            realised, already-published rows only — the brake at t reads equity through t-1 and
            nothing later.  Before 200 equity rows exist the state is OFF (braked), the same
            convention `px > px.rolling(200).mean()` uses in baseline.py.

THE BOOK, OTHERWISE FROZEN.  The record's certified 2026-09-04 incumbent: 3-leg rank composite
((21,252), (0,126), (0,63)) x the `0.5 + 0.5*above-200d` tilt, eligibility = above 200d MA AND
vol20 < 0.60, N = 15 names at equal weight, minimum hold H = 126 trading days, base gross 0.60,
weekly cadence, decisions lagged one row and applied at t+1 (rule 2), 10 bps per unit turnover.

WHAT IS BEING ASKED, PRECISELY.  Not "does the brake raise Sharpe" — the question is whether it
buys back the DD LEG, so every cell publishes the DD MARGIN (MaxDD minus the 4b cap 0.60 x SPY's
MaxDD) and the CAGR MARGIN (CAGR minus 0.70 x SPY's) side by side, because a brake that fixes the
DD leg by breaking the CAGR leg has bought nothing.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at every
cell; the halves; IS and OOS windows; turnover and its 10 bps drag in bp/yr; the number of days
the brake is actually engaged.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
FROZEN (BASIS = NONE) incumbent — the book that had nothing to choose.

PROTOCOL: rule 1 (>= 10 years); rule 2 (t+1, 10 bps, no leverage, no shorting — the brake only
ever REDUCES gross); rule 3 (RULES v2 AND SPY); rule 4 (both KEEP paths, 2 tuned parameters);
rule 8 (walk-forward: the (BASIS, DEPTH) PAIR chosen on warm-up..2016-12-31 by argmax IS Sharpe,
2017-2026 read ONCE, scored against the frozen NONE book); rule 9 (survivorship stated).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

TAPE STAMP: every panel's row count and date range are printed and written to `.gates.csv`.
The committed idea-1335 U56 (N=15, W) anchor is replayed and its deviation PUBLISHED rather than
asserted, because commit 4e19a80 and the 2026-09-19 daily close have both moved the tape since
that number was written (idea 1350 measured exactly this channel).

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_does-a-DE-GROSSING-DRAWDOWN-BRAKE-buy-back-the-4b-MaxDD-LEG_cloud.py
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

DATE = "2026-09-19"
SLUG = "does-a-DE-GROSSING-DRAWDOWN-BRAKE-buy-back-the-4b-MaxDD-LEG"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_CAD = 15, 126, 0.60, "W"         # the frozen incumbent
COST = 10.0                                        # PROTOCOL rule 2
BASES = ["NONE", "SPY200", "OWN200"]               # DIAL 1
DEPTHS = [0.00, 0.25, 0.50, 0.75, 1.00]            # DIAL 2
MA = 200
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
# idea 1335's committed .grid.csv, U56 / N=15 / W / 10 bps — replayed, deviation PUBLISHED
C1335_U56_W = dict(CAGR=0.1367020011892825, Sharpe=1.17166235540161, MaxDD=-0.163814812515476,
                   H1=1.2526855979053693, H2=1.121880836109541, turn=2.463043347965852)

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


def publish(name, value):
    GATES.append(dict(gate=name, value=value, target="published, not asserted", pass_=True))


def mech(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(MA).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


def cadence_rows(idx, cad):
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
        self.reb = cadence_rows(px.index, I_CAD)
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        s = px["SPY"]
        self.spy_on = (s > s.rolling(MA).mean()).fillna(False).values   # NaN -> braked


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


def run_braked(pan, reb, frame, basis, depth, gross=I_G):
    """Segment-by-segment book with a book-level GROSS multiplier decided one row BEFORE each
    rebalance row.  OWN200 reads the equity this very loop has already produced, so the brake is
    causal by construction and no future row can reach it."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    turn = np.zeros(T)
    out = np.zeros(T)
    eq = np.ones(T + 1)          # eq[k] = equity at the END of row k-1; eq[0] = 1.0 (pre-history)
    braked = np.zeros(T, dtype=bool)
    curw = np.zeros(M)
    reb = np.asarray(reb, dtype=np.int64)
    ends = np.append(reb[1:], T)
    filled = 0                   # rows of `out` (hence of eq) already realised
    for i0, i1 in zip(reb, ends):
        d = max(i0 - 1, 0)       # the row the decision reads (rule 2)
        if basis == "NONE":
            on = True
        elif basis == "SPY200":
            on = bool(pan.spy_on[d])
        else:                    # OWN200 — the book's own equity vs its own 200d MA
            if filled >= MA:
                e = eq[1:filled + 1]
                on = bool(e[-1] > e[-MA:].mean())
            else:
                on = False       # insufficient history -> braked (baseline.py's convention)
        g = gross if on else gross * depth
        braked[i0:i1] = not on
        w0 = g * frame[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        seg = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        out[i0:i1] = seg
        # realise the segment net of its own entry cost so OWN200 sees the book it will trade
        net = seg.copy()
        net[0] -= turn[i0] * COST / 1e4
        eq[i0 + 1:i1 + 1] = eq[i0] * np.cumprod(1.0 + net)
        filled = i1
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn, braked


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
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1296 (lane cloud, 2026-09-19) — does a DE-GROSSING DRAWDOWN BRAKE buy back the 4b "
        "MaxDD LEG the record says is the BINDER?")
    say("DIALS: BRAKE BASIS {NONE, SPY200, OWN200} x BRAKE DEPTH {0.00,0.25,0.50,0.75,1.00} at the "
        "frozen incumbent (N=15, H=126, gross 0.60, weekly, 10 bps, t+1).")
    say("=" * 118)

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
        say("  SMALL filter: data/small_meta.csv absent; in-panel max |1d move| >= 1.0 screen.")
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 / SMALL are CURRENT-constituent lists; SMALL is a "
        "sub-$2B screen carried back to 2010, so its LEVELS are an upper bound and only its "
        "CONTRASTS across basis and depth are read here.")
    say("  TAPE STAMP:")
    for p in panels:
        say(f"    {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}",
                f"{len(p.idx)} rows, {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    grid, wf_rows, bench = [], [], {}

    for pan in panels:
        n = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        frame = build1(pan, pan.reb, I_N, I_H)

        say(f"\n  [{pan.name}]  SPY: CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.4f}/{spy['H2']:.4f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps: CAGR {live['CAGR']:.2%} Sharpe "
            f"{live['Sharpe']:.4f} MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.4f}/"
            f"{live['H2']:.4f}")
        say(f"           OOS SPY {spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}  |  "
            f"OOS RULES v2 {liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")
        say(f"    {'basis':>6} {'depth':>5} | {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} {'H1':>6} "
            f"{'H2':>6} | {'DDmargin':>8} {'CGmargin':>8} | {'brk%':>5} {'turn':>5} {'drag':>6} | "
            f"{'OOSCAGR':>8} {'OOSShrp':>7} {'OOSMaxDD':>8} | {'ISShrp':>7} | 4a 4b  fail-legs")
        runs = {}
        for basis in BASES:
            for depth in DEPTHS:
                g, tu, brk = run_braked(pan, pan.reb, frame, basis, depth)
                rr = g - tu * COST / 1e4
                r = rr[WARMUP:]
                turn = annturn(tu, WARMUP, n)
                ka, kb, m, h1, h2, legs = keep_paths(r, spy, live)
                mo = triple(rr[i_oos:])
                kb_oos = bool(mo["Sharpe"] > spyO["Sharpe"])
                runs[(basis, depth)] = rr
                ddm = m["MaxDD"] - DD_CAP * spy["MaxDD"]
                cgm = m["CAGR"] - CAGR_FLOOR * spy["CAGR"]
                row = dict(panel=pan.name, basis=basis, depth=depth,
                           CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                           DD_margin_pp=ddm, CAGR_margin_pp=cgm,
                           brake_days_pct=float(brk[WARMUP:].mean()),
                           vol_real=annvol(r), turn=turn, cost_drag_bp=turn * COST,
                           n_rebal=len(pan.reb),
                           OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                           IS_Sharpe=sharpe(rr[WARMUP:i_oos]),
                           SPY_Sharpe=spy["Sharpe"], SPY_CAGR=spy["CAGR"],
                           SPY_MaxDD=spy["MaxDD"], LIVE_Sharpe=live["Sharpe"],
                           LIVE_MaxDD=live["MaxDD"], OOS_SPY_Sharpe=spyO["Sharpe"],
                           OOS_SPY_CAGR=spyO["CAGR"], OOS_SPY_MaxDD=spyO["MaxDD"],
                           OOS_LIVE_Sharpe=liveO["Sharpe"],
                           keep4a=ka, keep4b=kb, keep4b_oos_sharpe=kb_oos,
                           keep4b_and_oos=bool(kb and kb_oos),
                           leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                           leg_CAGR=legs["CAGR"])
                grid.append(row)
                say(f"    {basis:>6} {depth:5.2f} | {m['CAGR']:7.2%} {m['Sharpe']:7.4f} "
                    f"{m['MaxDD']:8.2%} {h1:6.3f} {h2:6.3f} | {ddm:+8.2%} {cgm:+8.2%} | "
                    f"{brk[WARMUP:].mean():5.1%} {turn:5.2f} {turn*COST:6.1f} | "
                    f"{mo['CAGR']:8.2%} {mo['Sharpe']:7.4f} {mo['MaxDD']:8.2%} | "
                    f"{row['IS_Sharpe']:7.4f} | {int(ka)}  {int(kb)}   "
                    + (",".join(k for k, v in legs.items() if not v) or "-"))
        bench[pan.name] = dict(spy=spy, spyO=spyO, live=live, liveO=liveO, runs=runs,
                               i_oos=i_oos, n=n)

        # ---- internal replay gates ---------------------------------------------------------
        base_none = runs[("NONE", DEPTHS[0])]
        d2 = max(float(np.abs(runs[("NONE", d)] - base_none).max()) for d in DEPTHS)
        gate(f"G2 {pan.name}: BASIS=NONE is one book at all five depths (degeneracy is real)",
             d2, "< 1e-15", d2 < 1e-15)
        d3 = max(float(np.abs(runs[(b, 1.00)] - base_none).max()) for b in BASES)
        gate(f"G3 {pan.name}: DEPTH=1.00 reproduces the unbraked book under every basis",
             d3, "< 1e-15", d3 < 1e-15)
        d4 = min(float(np.abs(runs[(b, 0.00)] - base_none).max()) for b in BASES if b != "NONE")
        gate(f"G4 {pan.name}: DEPTH=0.00 actually MOVES the book (the dial is not inert)",
             round(d4, 8), "> 1e-6", d4 > 1e-6)

        if pan.name == "U56":
            a = [r for r in grid if r["panel"] == "U56" and r["basis"] == "NONE"
                 and r["depth"] == 1.00][0]
            say("    REPLAY of idea 1335's committed U56 (N=15, W) @10bps — PUBLISHED, NOT "
                "ASSERTED (the tape has moved: 4e19a80 + the 2026-09-19 daily close):")
            for k, v in C1335_U56_W.items():
                say(f"      {k:>7}: this run {a[k]:.10f}  committed {v:.10f}  dev "
                    f"{a[k]-v:+.3e}")
                publish(f"REPLAY vs 1335 U56 (N=15,W) {k}",
                        f"{a[k]:.10f} vs {v:.10f} (dev {a[k]-v:+.3e})")

    G = pd.DataFrame(grid)

    # ---- 1. the question ------------------------------------------------------------------
    say("\n" + "=" * 118)
    say("1. DOES THE BRAKE BUY BACK THE DD LEG?  (DD margin = MaxDD - 0.60 x SPY MaxDD; >= 0 "
        "passes.  CAGR margin = CAGR - 0.70 x SPY CAGR.)")
    say("=" * 118)
    for p in G.panel.unique():
        anc = G[(G.panel == p) & (G.basis == "NONE") & (G.depth == 1.00)].iloc[0]
        say(f"    {p:>6}  anchor (NONE): DD margin {anc.DD_margin_pp:+.2%}  CAGR margin "
            f"{anc.CAGR_margin_pp:+.2%}  -> DD leg {'PASS' if anc.leg_DD else 'FAIL'}, "
            f"CAGR leg {'PASS' if anc.leg_CAGR else 'FAIL'}")
        for basis in ["SPY200", "OWN200"]:
            sub = G[(G.panel == p) & (G.basis == basis)].sort_values("depth")
            say(f"      {basis:>6}: " + "  ".join(
                f"d{r.depth:.2f}[DD {r.DD_margin_pp:+.2%} / CG {r.CAGR_margin_pp:+.2%} / "
                f"S {r.Sharpe:.3f}]" for r in sub.itertuples()))
    say("\n    Cells where the brake TURNS THE DD LEG FROM FAIL TO PASS (the idea's own target):")
    flips = []
    for p in G.panel.unique():
        anc = G[(G.panel == p) & (G.basis == "NONE") & (G.depth == 1.00)].iloc[0]
        if anc.leg_DD:
            say(f"      {p}: the anchor already PASSES the DD leg ({anc.DD_margin_pp:+.2%}) — "
                f"nothing to buy back; the brake can only be asked not to break it.")
            continue
        d = G[(G.panel == p) & (G.leg_DD) & (G.basis != "NONE")]
        if len(d) == 0:
            say(f"      {p}: NONE of the 10 braked cells recovers the DD leg.")
        for r in d.itertuples():
            flips.append(dict(panel=p, basis=r.basis, depth=r.depth))
            say(f"      {p} {r.basis} d{r.depth:.2f}: DD {r.MaxDD:.2%} (margin "
                f"{r.DD_margin_pp:+.2%}) BUT CAGR margin {r.CAGR_margin_pp:+.2%} -> 4b "
                f"{'PASS' if r.keep4b else 'FAIL'} [{'' if r.keep4b else 'fails: ' + ','.join(k for k, v in dict(H1=r.leg_H1, H2=r.leg_H2, DD=r.leg_DD, CAGR=r.leg_CAGR).items() if not v)}]")
    say(f"    DD-leg recoveries across all panels: {len(flips)}")

    say("\n2. WHAT THE BRAKE COSTS AND BUYS, AT EVERY RUNG (vs that panel's own NONE anchor)")
    for p in G.panel.unique():
        anc = G[(G.panel == p) & (G.basis == "NONE") & (G.depth == 1.00)].iloc[0]
        for basis in ["SPY200", "OWN200"]:
            sub = G[(G.panel == p) & (G.basis == basis)].sort_values("depth")
            say(f"    {p:>6} {basis:>6}: " + "  ".join(
                f"d{r.depth:.2f}[dS {r.Sharpe-anc.Sharpe:+.4f} dDD {r.MaxDD-anc.MaxDD:+.2%} "
                f"dCAGR {r.CAGR-anc.CAGR:+.2%} dturn {r.turn-anc.turn:+.2f}]"
                for r in sub.itertuples()))
        b = G[(G.panel == p) & (G.basis != "NONE")]
        nun = b.groupby("basis").brake_days_pct.nunique().to_dict()
        sp = G[(G.panel == p) & (G.basis == "SPY200")].brake_days_pct
        ow = G[(G.panel == p) & (G.basis == "OWN200")].sort_values("depth")
        say(f"      brake ENGAGED share of days: SPY200 {sp.iloc[0]:.1%} at EVERY depth "
            f"({nun['SPY200']} distinct value) — an EXOGENOUS basis cannot see the book it brakes;"
            f"  OWN200 " + " / ".join(f"d{r.depth:.2f} {r.brake_days_pct:.1%}"
                                      for r in ow.itertuples())
            + f" ({nun['OWN200']} distinct values) — a SELF-REFERENTIAL basis reads the equity it "
              "is braking, so the share is PATH-DEPENDENT.")
        say("        NOTE (a mechanical defect of the self-referential basis, not a result): at "
            "OWN200 d0.00 the book goes fully to cash, its equity is then FLAT, a flat curve is "
            "never ABOVE its own 200d mean, and the brake NEVER RELEASES — 100.0% engaged, zero "
            "return, Sharpe undefined.  An absorbing state; reported, not tuned away.")

    say("\n3. KEEP PATHS OVER ALL 45 CELLS ----------------------------------------------")
    say(f"    4a (beat the live book): {int(G.keep4a.sum())} of {len(G)}")
    say(f"    4b full-sample: {int(G.keep4b.sum())} of {len(G)};  4b full AND OOS Sharpe > SPY: "
        f"{int(G.keep4b_and_oos.sum())} of {len(G)}")
    for p in G.panel.unique():
        s = G[G.panel == p]
        say(f"      {p:>6}: 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/{len(s)}"
            f"   4b+OOS {int(s.keep4b_and_oos.sum())}/{len(s)}")
    for basis in BASES:
        s = G[G.basis == basis]
        say(f"      {basis:>6}: 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/"
            f"{len(s)}   4b+OOS {int(s.keep4b_and_oos.sum())}/{len(s)}")
    for d in DEPTHS:
        s = G[G.depth == d]
        say(f"      d{d:.2f}: 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/"
            f"{len(s)}   4b+OOS {int(s.keep4b_and_oos.sum())}/{len(s)}")
    fails = dict(H1=int((~G.leg_H1).sum()), H2=int((~G.leg_H2).sum()),
                 DD=int((~G.leg_DD).sum()), CAGR=int((~G.leg_CAGR).sum()))
    say(f"    4b binding legs across all {len(G)} cells: " + ", ".join(
        f"{k} fails {v}" for k, v in sorted(fails.items(), key=lambda kv: -kv[1])))
    say("    Cells that BEAT the frozen NONE anchor on full-sample Sharpe AND pass 4b full+OOS:")
    any_dom = False
    for p in G.panel.unique():
        anc = G[(G.panel == p) & (G.basis == "NONE") & (G.depth == 1.00)].iloc[0]
        d = G[(G.panel == p) & (G.Sharpe > anc.Sharpe) & G.keep4b_and_oos & (G.basis != "NONE")]
        for r in d.itertuples():
            any_dom = True
            say(f"      {p} {r.basis} d{r.depth:.2f}: {r.Sharpe:.4f} vs anchor {anc.Sharpe:.4f} "
                f"(+{r.Sharpe-anc.Sharpe:.4f}), OOS {r.OOS_Sharpe:.4f} vs {anc.OOS_Sharpe:.4f}, "
                f"MaxDD {r.MaxDD:.2%} vs {anc.MaxDD:.2%}")
    if not any_dom:
        say("      NONE on any panel.")

    # ---- rule 8 ---------------------------------------------------------------------------
    say("\n4. RULE 8 WALK-FORWARD — the (BASIS, DEPTH) PAIR chosen on warm-up..2016-12-31 by "
        "argmax IS Sharpe; 2017-2026 read ONCE")
    say("=" * 118)
    for p in G.panel.unique():
        b = bench[p]
        sub = G[G.panel == p]
        pick = sub.loc[sub.IS_Sharpe.idxmax()]
        anc = sub[(sub.basis == "NONE") & (sub.depth == 1.00)].iloc[0]
        ro = b["runs"][(pick.basis, float(pick.depth))][b["i_oos"]:]
        h1o, h2o = halves(ro)
        legs_oos = dict(OOS_Sharpe_vs_SPY=bool(pick.OOS_Sharpe > b["spyO"]["Sharpe"]),
                        DD=bool(pick.OOS_MaxDD >= DD_CAP * b["spyO"]["MaxDD"]),
                        CAGR=bool(pick.OOS_CAGR >= CAGR_FLOOR * b["spyO"]["CAGR"]))
        anc_legs_oos = dict(OOS_Sharpe_vs_SPY=bool(anc.OOS_Sharpe > b["spyO"]["Sharpe"]),
                            DD=bool(anc.OOS_MaxDD >= DD_CAP * b["spyO"]["MaxDD"]),
                            CAGR=bool(anc.OOS_CAGR >= CAGR_FLOOR * b["spyO"]["CAGR"]))
        best_oos = sub.loc[sub.OOS_Sharpe.idxmax()]
        wf = dict(panel=p, IS_pick_basis=pick.basis, IS_pick_depth=float(pick.depth),
                  IS_Sharpe=pick.IS_Sharpe,
                  IS_margin_over_anchor=pick.IS_Sharpe - anc.IS_Sharpe,
                  is_the_anchor=bool(pick.basis == "NONE" or pick.depth == 1.00),
                  OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                  OOS_H1=h1o, OOS_H2=h2o,
                  ANCHOR_OOS_CAGR=anc.OOS_CAGR, ANCHOR_OOS_Sharpe=anc.OOS_Sharpe,
                  ANCHOR_OOS_MaxDD=anc.OOS_MaxDD,
                  dOOS_Sharpe_vs_anchor=pick.OOS_Sharpe - anc.OOS_Sharpe,
                  dOOS_CAGR_vs_anchor=pick.OOS_CAGR - anc.OOS_CAGR,
                  dOOS_MaxDD_vs_anchor=pick.OOS_MaxDD - anc.OOS_MaxDD,
                  SPY_OOS_CAGR=b["spyO"]["CAGR"], SPY_OOS_Sharpe=b["spyO"]["Sharpe"],
                  SPY_OOS_MaxDD=b["spyO"]["MaxDD"],
                  LIVE_OOS_CAGR=b["liveO"]["CAGR"], LIVE_OOS_Sharpe=b["liveO"]["Sharpe"],
                  LIVE_OOS_MaxDD=b["liveO"]["MaxDD"],
                  keep4b_oos_all=bool(all(legs_oos.values())),
                  anchor_keep4b_oos_all=bool(all(anc_legs_oos.values())),
                  oos_fail_legs=",".join(k for k, v in legs_oos.items() if not v) or "-",
                  best_OOS_basis=best_oos.basis, best_OOS_depth=float(best_oos.depth),
                  best_OOS_Sharpe=best_oos.OOS_Sharpe)
        wf_rows.append(wf)
        say(f"    {p:>6}: IS pick ({pick.basis}, d{pick.depth:.2f}) IS Sharpe {pick.IS_Sharpe:.4f} "
            f"(anchor {anc.IS_Sharpe:.4f}, margin {pick.IS_Sharpe-anc.IS_Sharpe:+.5f}) -> OOS "
            f"{pick.OOS_CAGR:7.2%}/{pick.OOS_Sharpe:.4f}/{pick.OOS_MaxDD:7.2%}")
        say(f"            vs FROZEN NONE      {anc.OOS_CAGR:7.2%}/{anc.OOS_Sharpe:.4f}/"
            f"{anc.OOS_MaxDD:7.2%}   d Sharpe {pick.OOS_Sharpe-anc.OOS_Sharpe:+.4f}, d CAGR "
            f"{pick.OOS_CAGR-anc.OOS_CAGR:+.2%}, d MaxDD {pick.OOS_MaxDD-anc.OOS_MaxDD:+.2%}")
        say(f"            vs SPY {b['spyO']['CAGR']:7.2%}/{b['spyO']['Sharpe']:.4f}/"
            f"{b['spyO']['MaxDD']:7.2%}   vs RULES v2 {b['liveO']['CAGR']:7.2%}/"
            f"{b['liveO']['Sharpe']:.4f}/{b['liveO']['MaxDD']:7.2%}")
        say(f"            4b on every OOS leg: pick {int(wf['keep4b_oos_all'])} "
            f"[{wf['oos_fail_legs']}]  anchor {int(wf['anchor_keep4b_oos_all'])}   | ex-post best "
            f"OOS cell ({wf['best_OOS_basis']}, d{wf['best_OOS_depth']:.2f}) "
            f"{wf['best_OOS_Sharpe']:.4f}")

    WF = pd.DataFrame(wf_rows)
    say(f"\n    The IS chooser lands on a book identical to the frozen anchor in "
        f"{int(WF.is_the_anchor.sum())} of {len(WF)} panels.")
    say(f"    Mean OOS Sharpe of the IS-chosen PAIR minus the frozen anchor: "
        f"{WF.dOOS_Sharpe_vs_anchor.mean():+.4f} (min {WF.dOOS_Sharpe_vs_anchor.min():+.4f}, "
        f"max {WF.dOOS_Sharpe_vs_anchor.max():+.4f}); it beats the anchor in "
        f"{int((WF.dOOS_Sharpe_vs_anchor > 0).sum())} of {len(WF)}.")
    say(f"    Mean OOS CAGR difference: {WF.dOOS_CAGR_vs_anchor.mean():+.2%};  mean OOS MaxDD "
        f"difference: {WF.dOOS_MaxDD_vs_anchor.mean():+.2%} (positive = SHALLOWER).")
    say(f"    4b on every OOS leg after rule 8: pick {int(WF.keep4b_oos_all.sum())} of {len(WF)}, "
        f"anchor {int(WF.anchor_keep4b_oos_all.sum())} of {len(WF)}.")
    hind = int(((WF.best_OOS_basis != WF.IS_pick_basis)
                | (WF.best_OOS_depth != WF.IS_pick_depth)).sum())
    say(f"    H_HINDSIGHT: the ex-post best OOS cell differs from the IS pick on {hind} of "
        f"{len(WF)} panels.")

    say("\n5. THE DEPTH LADDER, OOS (2017-2026), for the reader who wants the raw shape")
    for p in G.panel.unique():
        for basis in BASES:
            sub = G[(G.panel == p) & (G.basis == basis)].sort_values("depth")
            say(f"    {p:>6} {basis:>6}: " + "  ".join(
                f"d{r.depth:.2f}({r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:.2%})" for r in sub.itertuples()))

    G.to_csv(f"{OUT}.grid.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  wrote {Path(OUT).name}.grid.csv ({len(G)} cells), .walkforward.csv ({len(WF)}), "
        f".gates.csv")
    asserted = [g for g in GATES if g["target"] != "published, not asserted"]
    say(f"  GATES: {sum(g['pass_'] for g in asserted)}/{len(asserted)} asserted pass "
        f"(plus {len(GATES)-len(asserted)} published stamps)")
    say(f"  elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
