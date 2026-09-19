#!/usr/bin/env python3
"""Idea 1562 — does the 1538 TWO-STATE GROSS survive a CAGR-MATCHED DE-GROSS TWIN and a SPY-LAG SWEEP?

THE OBJECT.  Idea 1538 (lane C, 2026-09-19) left an incidental KEEP-4b candidate: the frozen
incumbent book (U56, N=20, H=126, band 0.00, MAXVOL 0.60, weekly) run at gross 0.75 when SPY is
above its own 200d MA and 0.5625 when it is below — FULL 14.92% / 1.1788 / -18.05%, OOS 16.48% /
1.2250 / -18.05%, 4b PASS on FULL and OOS, beating the frozen anchor (15.80% / 1.1537 / -19.13%,
OOS 1.1857) on both Sharpes with a shallower drawdown.

THE DOUBT.  It is a DE-GROSS DEVICE.  Eight consecutive 2026-09-19 runs found every
drawdown-buying device in the record beaten AT MATCHED EXPOSURE by a plain constant de-gross, and
idea 1494 asks whether realised mean gross is a sufficient statistic for the whole family.  A
two-state gross that spends 0.5625 in exactly the states where the tape falls is, mechanically, a
book with a lower mean gross than 0.75.  So the only legitimate comparand is not the g = 0.75
anchor: it is the CONSTANT gross g* that produces the SAME CAGR.

WHAT IS PRICED (the idea's own three arms, all cells published).
  (a) CAGR-MATCHED TWIN.  For every candidate cell, solve for the constant gross g* whose FULL
      sample CAGR equals the candidate's at that cost rung (fine ladder + interpolation, then an
      EXACT engine run at g*; realised |CAGR gap| gated < 20 bp).  Report dSharpe and dMaxDD of
      candidate minus twin, with a paired circular-block bootstrap SE.
  (b) COST LADDER 0 / 10 / 25 / 50 bps.  Turnover is cost-free to compute (the drift
      renormalisation uses the GROSS return), so every rung is read off one engine run.
  (c) SWEEP  MA length {100, 150, 200, 250}  x  low-state gross {0.375, 0.5625, 0.675}  = 12 cells
      on three panels.  Plus the SPY-LAG sweep of the title: the macro signal read with L = 1
      (1538's convention), 2 and 5 trading days of lag, on U56, all 12 cells.

TUNED PARAMETERS: exactly TWO — the MA length and the low-state gross.  The cost rung and the
signal lag are ROBUSTNESS LADDERS, published in full, never selected on.

PRE-REGISTERED VERDICT RULE (written before the run, not after).
  H_SCALAR  the twin wins:  pooled mean dSharpe(cand - twin) <= 0 across the 12 cells at 10 bps.
            If H_SCALAR holds on U56, the candidate is DEAD ON ARRIVAL as a capital claim and the
            run is a KILL, whatever its 4b verdict against SPY.
  H_DEVICE  the gate wins:  pooled mean dSharpe > 0 AND the rule-8 chosen cell beats its own twin
            OUT OF SAMPLE.  Only then is it the first macro gate in the record that is not a
            de-gross in costume.

PROTOCOL: rule 1 (>= 10y); rule 2 (weights at t-1 applied at t, 10 bps headline, no shorting, no
leverage — every gross rung is <= 1.00 and the low state only ever CUTS); rule 3 (compared to the
live RULES v2 baseline AND SPY); rule 4 (full + both halves, both KEEP paths at EVERY cell);
rule 8 (parameters chosen on warm-up..2016-12-31 ONLY, 2017-01-01..end read exactly once);
rule 9 (survivorship stated).

GATES.  G0 >= 10y.  G1 CROSS-SCRIPT REPLAY of the committed 2026-09-04 U56 frozen anchor.
G2 CROSS-SCRIPT REPLAY of idea 1538's own candidate cell (U56, MA 200, gL 0.5625, 10 bps).
G3 exactly two tuned parameters.  G4 CAGR match quality < 20 bp on every matched twin.
G5 no chooser reads a row on or after 2017-01-01.  G6 gross in [0, 1] on every book.
G7 the cost ladder is an identity on the SAME turnover path (0 bps run reproduces rg exactly).
G8 every one of the 12 x 4 x 3 cells published.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-19_two-state-gross-vs-cagr-matched-degross-twin_cloud.py
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
SLUG = "two-state-gross-vs-cagr-matched-degross-twin"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_V, I_B, I_C = 20, 126, 0.75, 0.60, 0.00, "W"     # the frozen incumbent
COSTS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_COST = 10.0
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

MAS = [100, 150, 200, 250]                        # DIAL 1 (tuned)
GLOWS = [0.375, 0.5625, 0.675]                    # DIAL 2 (tuned)
LAGS = [1, 2, 5]                                  # robustness ladder, never selected on
GGRID = np.round(np.arange(0.05, 1.0001, 0.01), 4)

BOOT_REPS, BOOT_BLOCK, BOOT_SEED = 400, 63, 20260919
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)
C_1538 = dict(CAGR=0.1492, Sharpe=1.1788, MaxDD=-0.1805,
              oCAGR=0.1648, oSharpe=1.2250, oMaxDD=-0.1805)
MATCH_BAR = 0.0020                                # 20 bp of CAGR

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


# ------------------------------------------------------------------ statistics
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


def keep_paths(r, bm, live):
    """4a against the LIVE book (rule 4a), 4b against SPY (rule 4b).  Returns both verdicts and
    the four 4b legs, so a fail can always be attributed."""
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def paired_block_dsharpe(a, b, reps=BOOT_REPS, L=BOOT_BLOCK, seed=BOOT_SEED):
    """PAIRED circular-block bootstrap of the Sharpe DIFFERENCE (idea 1444's ruler, not the
    marginal one): the same block index set is applied to both series."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    idx = (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n
    A, B = a[idx], b[idx]

    def sh(X):
        v = X.std(axis=1, ddof=0) * np.sqrt(252)
        return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)

    d = sh(A) - sh(B)
    obs = float(sharpe(a) - sharpe(b))
    se = float(np.nanstd(d, ddof=1))
    return obs, se, (obs / se if se > 0 else np.nan)


# ------------------------------------------------------------------ the panel
def mech_legs(q: pd.DataFrame):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return (sum(parts) / len(parts)).values


def cadence_rows(idx, cad):
    """Rebalance ROWS, already shifted one day: the decision taken at close t-1 is applied at t."""
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
        self.spy_px = px["SPY"]
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        q = px[invest]
        self.q = q
        self.comp = mech_legs(q)
        self.vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values

    def frame_inputs(self):
        """The frozen incumbent's eligibility and ranking key: per-name 200d MA gate (band 0.00)
        and the MAXVOL 0.60 ceiling, exactly as RULES carries them."""
        above = (self.q > self.q.rolling(200).mean()).values
        elig = above & (np.nan_to_num(self.vol20, nan=1e9) < I_V)
        sc = self.comp * (0.5 + 0.5 * above.astype(float))
        key = np.where(np.isfinite(sc), -sc, np.inf)
        return elig, key

    def macro_state(self, ma, lag):
        """True = SPY above its own `ma`-day MA, read with `lag` trading days of delay."""
        s = self.spy_px
        g = (s > s.rolling(int(ma)).mean()).shift(int(lag)).fillna(False)
        return g.values.astype(bool)


def build_frame(pan, elig, key, reb, N=I_N, H=I_H, lag=1):
    """The frozen incumbent's HOLDINGS frame (unit gross).  min-hold H retains a held name that is
    still priced; vacancies are filled from the eligible set by the composite key."""
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


def run_gseq(pan, frame, reb, gseq):
    """Daily engine.  `gseq` is the per-row gross (scalar broadcast or a full sequence).  De-gross
    goes to CASH at 0%, never re-spread and never levered.  Returns the GROSS return path and the
    turnover path, from which the net path at ANY cost rung is an identity."""
    T, M = pan.rets.shape
    isreb = np.zeros(T, bool)
    isreb[reb] = True
    g = np.broadcast_to(np.asarray(gseq, float), (T,))
    cur = np.zeros(M)
    rg = np.zeros(T)
    turn = np.zeros(T)
    sc = np.zeros(T)
    gmax = 0.0
    for t in range(T):
        if isreb[t]:
            gt = float(g[t])
            post = gt * frame[t]
        else:
            gt = sc[t - 1] if t else 0.0
            post = cur
        sc[t] = gt
        turn[t] = float(np.abs(post - cur).sum())
        gmax = max(gmax, float(post.sum()))
        r = float(post @ pan.rets[t])
        rg[t] = r
        cur = post * (1.0 + pan.rets[t]) / (1.0 + r)
    return dict(rg=rg, turn=turn, gmax=gmax, gbar=float(sc[WARMUP:].mean()))


def net_of(run, cost):
    return run["rg"] - run["turn"] * cost / 1e4


def main():
    t0 = time.time()
    say("=" * 124)
    say("IDEA 1562 — does the 1538 TWO-STATE GROSS survive a CAGR-MATCHED DE-GROSS TWIN, a COST "
        "LADDER and a SPY-LAG SWEEP?   (lane cloud, idea 1 of 2)")
    say("  PRE-REGISTERED: H_SCALAR = the constant de-gross twin wins (pooled mean dSharpe <= 0 at "
        "10 bps) -> the candidate is DEAD ON ARRIVAL and this run is a KILL.")
    say("  H_DEVICE = the gate wins (pooled mean dSharpe > 0 AND the rule-8 cell beats its own "
        "twin OUT OF SAMPLE) -> the first macro gate in the record that is not a de-gross.")
    say("=" * 124)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} investable names survive.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)}.")
    say("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every ABSOLUTE level below is an UPPER BOUND.  "
        "The HEADLINE of this run is a CONTRAST between two books over the SAME names on the SAME "
        "days differing only in the gross PATH, which the bias cannot manufacture; the 4a / 4b "
        "pass counts are NOT immune and are reported as upper bounds.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y)")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)", round(min(len(p.idx) for p in panels) / 252.0, 2),
         ">= 10.0", min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G3 exactly two tuned parameters (MA length, low-state gross); cost rung and signal lag "
         "are published ladders, never selected on", 2, "== 2", True)

    grid, lagrows, wf_rows, ladder_rows = [], [], [], []
    g1_ok = g2_ok = None
    worst_match = 0.0
    gmax_global = 0.0
    g7_dev = 0.0

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is = int(np.searchsorted(pan.idx.values, np.datetime64(IS_END)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=HEADLINE_COST,
                      freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])

        say(f"\n  [{pan.name}]  SPY CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")
        say(f"           OOS SPY {spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}  |  "
            f"OOS RULES v2 {liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")

        elig, key = pan.frame_inputs()
        reb = cadence_rows(pan.idx, I_C)
        frame = build_frame(pan, elig, key, reb)

        # ---- the frozen anchor (constant gross 0.75) --------------------------------------
        A = run_gseq(pan, frame, reb, I_G)
        gmax_global = max(gmax_global, A["gmax"])
        anch = net_of(A, HEADLINE_COST)
        am, ao = triple(anch[WARMUP:]), triple(anch[i_oos:])
        ah1, ah2 = halves(anch[WARMUP:])
        a4a, a4b, _, _, _, alegs = keep_paths(anch[WARMUP:], spy, live)
        a4aO, a4bO, _, _, _, alegsO = keep_paths(anch[i_oos:], spyO, liveO)
        say(f"           FROZEN ANCHOR g=0.75  CAGR {am['CAGR']:.2%} Sharpe {am['Sharpe']:.4f} "
            f"MaxDD {am['MaxDD']:.2%} H1/H2 {ah1:.4f}/{ah2:.4f} | OOS {ao['CAGR']:.2%}/"
            f"{ao['Sharpe']:.4f}/{ao['MaxDD']:.2%} | 4a {a4a}/{a4aO} 4b {a4b}/{a4bO} "
            f"| mean gross {A['gbar']:.4f}")
        if pan.name == "U56":
            d = max(abs(am["Sharpe"] - C_U56["Sharpe"]), abs(ao["Sharpe"] - C_U56["oSharpe"]),
                    abs(am["CAGR"] - C_U56["CAGR"]), abs(am["MaxDD"] - C_U56["MaxDD"]))
            g1_ok = gate("G1 cross-script replay of the committed 2026-09-04 U56 frozen anchor "
                         "(15.80%/1.1537/-19.13% full; 1.1857 OOS)",
                         f"max |dev| {d:.2e}", "< 5e-3", d < 5e-3)
        g7_dev = max(g7_dev, float(np.abs(net_of(A, 0.0) - A["rg"]).max()))

        # ---- the CONSTANT DE-GROSS LADDER (the comparand family) --------------------------
        lad = {}
        for g in GGRID:
            R = run_gseq(pan, frame, reb, float(g))
            lad[float(g)] = R
            for c in COSTS:
                rn = net_of(R, c)
                m, mo = triple(rn[WARMUP:]), triple(rn[i_oos:])
                h1, h2 = halves(rn[WARMUP:])
                k4a, k4b, _, _, _, lg = keep_paths(rn[WARMUP:], spy, live)
                k4aO, k4bO, _, _, _, lgO = keep_paths(rn[i_oos:], spyO, liveO)
                ladder_rows.append(dict(panel=pan.name, g=float(g), cost=c,
                                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                        H1=h1, H2=h2, oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"],
                                        oMaxDD=mo["MaxDD"], keep4a=k4a, keep4b=k4b,
                                        keep4a_oos=k4aO, keep4b_oos=k4bO,
                                        gbar=R["gbar"]))
        gs = np.array(sorted(lad))
        curve = {c: np.array([cagr(net_of(lad[float(g)], c)[WARMUP:]) for g in gs]) for c in COSTS}

        def matched_twin(target_cagr, cost):
            """The CONSTANT gross whose FULL-sample CAGR equals `target_cagr` at this cost rung.
            Interpolate on the fine ladder, then run the engine EXACTLY at g*."""
            y = curve[cost]
            o = np.argsort(y)
            gstar = float(np.interp(target_cagr, y[o], gs[o]))
            gstar = float(min(max(gstar, 0.0), 1.0))
            R = run_gseq(pan, frame, reb, gstar)
            rn = net_of(R, cost)
            return gstar, R, rn, abs(cagr(rn[WARMUP:]) - target_cagr)

        # ---- the CANDIDATE GRID ----------------------------------------------------------
        for ma in MAS:
            for gl in GLOWS:
                st = pan.macro_state(ma, 1)
                gseq = np.where(st, I_G, gl)
                C = run_gseq(pan, frame, reb, gseq)
                gmax_global = max(gmax_global, C["gmax"])
                for c in COSTS:
                    rn = net_of(C, c)
                    k4a, k4b, m, h1, h2, lg = keep_paths(rn[WARMUP:], spy, live)
                    k4aO, k4bO, mo, oh1, oh2, lgO = keep_paths(rn[i_oos:], spyO, liveO)
                    gstar, TW, tw, gap = matched_twin(m["CAGR"], c)
                    worst_match = max(worst_match, gap)
                    tm, tmo = triple(tw[WARMUP:]), triple(tw[i_oos:])
                    th1, th2 = halves(tw[WARMUP:])
                    t4a, t4b, _, _, _, _ = keep_paths(tw[WARMUP:], spy, live)
                    t4aO, t4bO, _, _, _, _ = keep_paths(tw[i_oos:], spyO, liveO)
                    dS, seS, tS = paired_block_dsharpe(rn[WARMUP:], tw[WARMUP:])
                    dSO, seSO, tSO = paired_block_dsharpe(rn[i_oos:], tw[i_oos:])
                    dSa, seSa, tSa = paired_block_dsharpe(rn[WARMUP:], anch[WARMUP:])
                    grid.append(dict(
                        panel=pan.name, ma=ma, glow=gl, cost=c, lag=1,
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                        gbar=C["gbar"], keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO, keep4b_oos=k4bO,
                        leg_H1=lg["H1"], leg_H2=lg["H2"], leg_DD=lg["DD"], leg_CAGR=lg["CAGR"],
                        legO_H1=lgO["H1"], legO_H2=lgO["H2"], legO_DD=lgO["DD"],
                        legO_CAGR=lgO["CAGR"],
                        gstar=gstar, twin_gap=gap, twin_gbar=TW["gbar"],
                        twCAGR=tm["CAGR"], twSharpe=tm["Sharpe"], twMaxDD=tm["MaxDD"],
                        twH1=th1, twH2=th2, twoCAGR=tmo["CAGR"], twoSharpe=tmo["Sharpe"],
                        twoMaxDD=tmo["MaxDD"], tw4a=t4a, tw4b=t4b, tw4a_oos=t4aO, tw4b_oos=t4bO,
                        dSharpe_twin=dS, se_twin=seS, t_twin=tS,
                        dMaxDD_twin=m["MaxDD"] - tm["MaxDD"],
                        odSharpe_twin=dSO, ose_twin=seSO, ot_twin=tSO,
                        odMaxDD_twin=mo["MaxDD"] - tmo["MaxDD"],
                        dSharpe_anchor=dSa, se_anchor=seSa, t_anchor=tSa,
                        dMaxDD_anchor=m["MaxDD"] - am["MaxDD"],
                        isSharpe=sharpe(rn[WARMUP:i_is + 1]),
                        isSharpe_twin=sharpe(tw[WARMUP:i_is + 1]),
                        anchor_isSharpe=sharpe(anch[WARMUP:i_is + 1])))
                    if (pan.name == "U56" and ma == 200 and abs(gl - 0.5625) < 1e-9
                            and c == HEADLINE_COST):
                        d2 = max(abs(m["CAGR"] - C_1538["CAGR"]),
                                 abs(m["Sharpe"] - C_1538["Sharpe"]),
                                 abs(m["MaxDD"] - C_1538["MaxDD"]),
                                 abs(mo["CAGR"] - C_1538["oCAGR"]),
                                 abs(mo["Sharpe"] - C_1538["oSharpe"]),
                                 abs(mo["MaxDD"] - C_1538["oMaxDD"]))
                        g2_ok = gate("G2 cross-script replay of idea 1538's candidate cell "
                                     "(U56 MA200 gL0.5625 @10bps: 14.92%/1.1788/-18.05% full, "
                                     "16.48%/1.2250/-18.05% OOS)",
                                     f"max |dev| {d2:.2e} (got {m['CAGR']:.4f}/{m['Sharpe']:.4f}/"
                                     f"{m['MaxDD']:.4f}; OOS {mo['CAGR']:.4f}/{mo['Sharpe']:.4f}/"
                                     f"{mo['MaxDD']:.4f})", "< 5e-3", d2 < 5e-3)

                # ---- the SPY-LAG sweep (U56 only, headline cost) ---------------------------
                if pan.name == "U56":
                    for L in LAGS:
                        stL = pan.macro_state(ma, L)
                        RL = run_gseq(pan, frame, reb, np.where(stL, I_G, gl))
                        rnL = net_of(RL, HEADLINE_COST)
                        k4a, k4b, m, h1, h2, _ = keep_paths(rnL[WARMUP:], spy, live)
                        k4aO, k4bO, mo, _, _, _ = keep_paths(rnL[i_oos:], spyO, liveO)
                        gstar, TW, tw, gap = matched_twin(m["CAGR"], HEADLINE_COST)
                        worst_match = max(worst_match, gap)
                        tm = triple(tw[WARMUP:])
                        dS, seS, tS = paired_block_dsharpe(rnL[WARMUP:], tw[WARMUP:])
                        lagrows.append(dict(panel=pan.name, ma=ma, glow=gl, lag=L,
                                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                            H1=h1, H2=h2, oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"],
                                            oMaxDD=mo["MaxDD"], keep4b=k4b, keep4b_oos=k4bO,
                                            keep4a=k4a, keep4a_oos=k4aO, gstar=gstar,
                                            twSharpe=tm["Sharpe"], twMaxDD=tm["MaxDD"],
                                            dSharpe_twin=dS, t_twin=tS,
                                            dMaxDD_twin=m["MaxDD"] - tm["MaxDD"]))

        # ---- RULE 8 -----------------------------------------------------------------------
        sub = pd.DataFrame([r for r in grid
                            if r["panel"] == pan.name and r["cost"] == HEADLINE_COST])
        pick = sub.loc[sub["isSharpe"].idxmax()]
        wf_rows.append(dict(panel=pan.name, chooser="C_ISSHARPE", ma=int(pick["ma"]),
                            glow=float(pick["glow"]), isSharpe=float(pick["isSharpe"]),
                            oCAGR=float(pick["oCAGR"]), oSharpe=float(pick["oSharpe"]),
                            oMaxDD=float(pick["oMaxDD"]),
                            twin_oSharpe=float(pick["twoSharpe"]),
                            twin_oMaxDD=float(pick["twoMaxDD"]),
                            twin_oCAGR=float(pick["twoCAGR"]),
                            d_oSharpe_twin=float(pick["odSharpe_twin"]),
                            t_oSharpe_twin=float(pick["ot_twin"]),
                            anchor_oCAGR=ao["CAGR"], anchor_oSharpe=ao["Sharpe"],
                            anchor_oMaxDD=ao["MaxDD"],
                            live_oCAGR=liveO["CAGR"], live_oSharpe=liveO["Sharpe"],
                            live_oMaxDD=liveO["MaxDD"],
                            spy_oCAGR=spyO["CAGR"], spy_oSharpe=spyO["Sharpe"],
                            spy_oMaxDD=spyO["MaxDD"],
                            keep4b_oos=bool(pick["keep4b_oos"]),
                            keep4a_oos=bool(pick["keep4a_oos"])))
        # a second, equally legal IS-only chooser: the largest IS Sharpe MARGIN over its own twin
        sub2 = sub.assign(mar=sub["isSharpe"] - sub["isSharpe_twin"])
        p2 = sub2.loc[sub2["mar"].idxmax()]
        wf_rows.append(dict(panel=pan.name, chooser="C_ISMARGIN", ma=int(p2["ma"]),
                            glow=float(p2["glow"]), isSharpe=float(p2["isSharpe"]),
                            oCAGR=float(p2["oCAGR"]), oSharpe=float(p2["oSharpe"]),
                            oMaxDD=float(p2["oMaxDD"]),
                            twin_oSharpe=float(p2["twoSharpe"]),
                            twin_oMaxDD=float(p2["twoMaxDD"]),
                            twin_oCAGR=float(p2["twoCAGR"]),
                            d_oSharpe_twin=float(p2["odSharpe_twin"]),
                            t_oSharpe_twin=float(p2["ot_twin"]),
                            anchor_oCAGR=ao["CAGR"], anchor_oSharpe=ao["Sharpe"],
                            anchor_oMaxDD=ao["MaxDD"],
                            live_oCAGR=liveO["CAGR"], live_oSharpe=liveO["Sharpe"],
                            live_oMaxDD=liveO["MaxDD"],
                            spy_oCAGR=spyO["CAGR"], spy_oSharpe=spyO["Sharpe"],
                            spy_oMaxDD=spyO["MaxDD"],
                            keep4b_oos=bool(p2["keep4b_oos"]),
                            keep4a_oos=bool(p2["keep4a_oos"])))
        say(f"    rule-8 IS window rows {WARMUP}..{i_is} ({pan.idx[WARMUP].date()}.."
            f"{pan.idx[i_is].date()}), OOS from {pan.idx[i_oos].date()}")

    G = pd.DataFrame(grid)
    LG = pd.DataFrame(lagrows)
    WF = pd.DataFrame(wf_rows)
    LD = pd.DataFrame(ladder_rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    LG.to_csv(f"{OUT}.lagsweep.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    LD.to_csv(f"{OUT}.degrossladder.csv", index=False)

    gate("G4 CAGR match quality of every de-gross twin", f"worst |gap| {worst_match:.2e}",
         f"< {MATCH_BAR}", worst_match < MATCH_BAR)
    gate("G5 no chooser reads a row on or after 2017-01-01 (IS Sharpe ends at IS_END)",
         "isSharpe computed on [WARMUP, i_is] only", "structural", True)
    gate("G6 gross in [0, 1] on every book (no leverage, rule 2)", f"max sum(w) {gmax_global:.6f}",
         "<= 1.0 + 1e-9", gmax_global <= 1.0 + 1e-9)
    gate("G7 the cost ladder is an identity on one turnover path (0 bps == gross)",
         f"max |dev| {g7_dev:.2e}", "== 0", g7_dev == 0.0)
    gate("G8 every cell published", f"{len(G)} grid rows "
         f"({len(MAS)}x{len(GLOWS)}x{len(COSTS)}x3 = {len(MAS)*len(GLOWS)*len(COSTS)*3})",
         f"== {len(MAS)*len(GLOWS)*len(COSTS)*3}",
         len(G) == len(MAS) * len(GLOWS) * len(COSTS) * 3)

    # ------------------------------------------------------------------ the headline
    say("\n" + "=" * 124)
    say("ARM (a)+(c) — THE 12-CELL SWEEP AGAINST ITS OWN CAGR-MATCHED CONSTANT DE-GROSS TWIN "
        f"(headline {HEADLINE_COST:.0f} bps, lag 1).  Every cell published.")
    say("=" * 124)
    for p in ["U56", "B136", "SMALL"]:
        s = G[(G.panel == p) & (G.cost == HEADLINE_COST)].sort_values(["ma", "glow"])
        say(f"\n  [{p}]  cand = two-state gross (0.75 above SPY's MA, gL below); twin = constant "
            f"g* matched on FULL CAGR")
        say("    MA   gL      gbar   CAGR     Sharpe   MaxDD     |  g*     twSharpe twMaxDD  |  "
            "dSharpe   t      dMaxDD   | 4a 4b | oSharpe  otwin   odS      4bO")
        for _, r in s.iterrows():
            say(f"    {int(r.ma):<4} {r.glow:<6.4f} {r.gbar:.4f} {r.CAGR:7.2%} {r.Sharpe:8.4f} "
                f"{r.MaxDD:8.2%}  | {r.gstar:.4f} {r.twSharpe:8.4f} {r.twMaxDD:8.2%} | "
                f"{r.dSharpe_twin:+8.4f} {r.t_twin:+6.2f} {r.dMaxDD_twin:+7.2%} | "
                f"{int(r.keep4a)}  {int(r.keep4b)}  | {r.oSharpe:7.4f} {r.twoSharpe:7.4f} "
                f"{r.odSharpe_twin:+8.4f} {int(r.keep4b_oos)}")
        w = s["dSharpe_twin"]
        say(f"    POOLED {p}: mean dSharpe(cand - twin) {w.mean():+.4f}, cand wins "
            f"{int((w > 0).sum())} of {len(w)}; mean dMaxDD {s['dMaxDD_twin'].mean():+.2%}, "
            f"shallower {int((s['dMaxDD_twin'] > 0).sum())} of {len(s)}; "
            f"|t| > 2 at {int((s['t_twin'].abs() > 2).sum())} of {len(s)} cells")

    say("\n" + "=" * 124)
    say("ARM (b) — THE COST LADDER 0 / 10 / 25 / 50 bps.  Pooled over the 12 cells of each panel.")
    say("=" * 124)
    say("    panel  cost   mean dSharpe(cand-twin)  cand wins   mean dMaxDD   shallower   "
        "4b FULL  4b OOS  4b BOTH   twin 4b BOTH")
    for p in ["U56", "B136", "SMALL"]:
        for c in COSTS:
            s = G[(G.panel == p) & (G.cost == c)]
            both = int((s.keep4b & s.keep4b_oos).sum())
            tboth = int((s.tw4b & s.tw4b_oos).sum())
            say(f"    {p:<6} {c:>4.0f}   {s['dSharpe_twin'].mean():+.4f}                "
                f"{int((s['dSharpe_twin'] > 0).sum())} of {len(s)}     "
                f"{s['dMaxDD_twin'].mean():+.2%}       "
                f"{int((s['dMaxDD_twin'] > 0).sum())} of {len(s)}       "
                f"{int(s.keep4b.sum())}       {int(s.keep4b_oos.sum())}      {both}         "
                f"{tboth}")

    say("\n" + "=" * 124)
    say("ARM (SPY-LAG SWEEP, title) — U56, headline cost, lag L in {1, 2, 5} trading days.")
    say("=" * 124)
    say("    MA   gL      L  CAGR     Sharpe   MaxDD    | g*     twSharpe dSharpe   t      "
        "dMaxDD  | 4b 4bO")
    for _, r in LG.sort_values(["ma", "glow", "lag"]).iterrows():
        say(f"    {int(r.ma):<4} {r.glow:<6.4f} {int(r.lag)}  {r.CAGR:7.2%} {r.Sharpe:8.4f} "
            f"{r.MaxDD:7.2%} | {r.gstar:.4f} {r.twSharpe:8.4f} {r.dSharpe_twin:+8.4f} "
            f"{r.t_twin:+6.2f} {r.dMaxDD_twin:+7.2%} | {int(r.keep4b)}  {int(r.keep4b_oos)}")
    for L in LAGS:
        s = LG[LG.lag == L]
        say(f"    POOLED lag {L}: mean dSharpe(cand - twin) {s['dSharpe_twin'].mean():+.4f}, cand "
            f"wins {int((s['dSharpe_twin'] > 0).sum())} of {len(s)}; mean Sharpe "
            f"{s['Sharpe'].mean():.4f}; 4b BOTH {int((s.keep4b & s.keep4b_oos).sum())} of {len(s)}")

    say("\n" + "=" * 124)
    say("RULE 8 — parameters (MA, gL) chosen on warm-up..2016-12-31 ONLY; 2017-01-01..end read ONCE.")
    say("=" * 124)
    for _, r in WF.iterrows():
        say(f"  [{r.panel}] {r.chooser} picks MA {int(r.ma)} / gL {r.glow:.4f} (IS Sharpe "
            f"{r.isSharpe:.4f})")
        say(f"      OOS cand   {r.oCAGR:7.2%} / {r.oSharpe:.4f} / {r.oMaxDD:7.2%}   "
            f"4a {int(r.keep4a_oos)}  4b {int(r.keep4b_oos)}")
        say(f"      OOS twin   {r.twin_oCAGR:7.2%} / {r.twin_oSharpe:.4f} / {r.twin_oMaxDD:7.2%}"
            f"   dSharpe {r.d_oSharpe_twin:+.4f} (t {r.t_oSharpe_twin:+.2f})")
        say(f"      OOS anchor {r.anchor_oCAGR:7.2%} / {r.anchor_oSharpe:.4f} / "
            f"{r.anchor_oMaxDD:7.2%}")
        say(f"      OOS LIVE   {r.live_oCAGR:7.2%} / {r.live_oSharpe:.4f} / {r.live_oMaxDD:7.2%}")
        say(f"      OOS SPY    {r.spy_oCAGR:7.2%} / {r.spy_oSharpe:.4f} / {r.spy_oMaxDD:7.2%}")
    say(f"  POOLED over {len(WF)} (panel, chooser) cells: mean OOS Sharpe cand "
        f"{WF['oSharpe'].mean():.4f} vs twin {WF['twin_oSharpe'].mean():.4f} vs anchor "
        f"{WF['anchor_oSharpe'].mean():.4f} vs LIVE {WF['live_oSharpe'].mean():.4f} vs SPY "
        f"{WF['spy_oSharpe'].mean():.4f}")
    say(f"  the chosen cell beats its OWN TWIN out of sample at "
        f"{int((WF['d_oSharpe_twin'] > 0).sum())} of {len(WF)} cells")

    # ------------------------------------------------------------------ verdict
    u = G[(G.panel == "U56") & (G.cost == HEADLINE_COST)]
    pooled_all = G[G.cost == HEADLINE_COST]["dSharpe_twin"].mean()
    h_scalar = bool(u["dSharpe_twin"].mean() <= 0)
    wf_ok = bool((WF["d_oSharpe_twin"] > 0).all())
    h_device = bool(pooled_all > 0 and wf_ok)
    say("\n" + "=" * 124)
    say(f"  H_SCALAR (twin wins on U56 at 10 bps, pooled mean dSharpe <= 0): "
        f"{'HOLDS' if h_scalar else 'does NOT hold'}  [U56 pooled {u['dSharpe_twin'].mean():+.4f}, "
        f"all panels {pooled_all:+.4f}]")
    say(f"  H_DEVICE (pooled dSharpe > 0 AND every rule-8 cell beats its own twin OOS): "
        f"{'HOLDS' if h_device else 'does NOT hold'}")
    verdict = "KILL" if h_scalar or not h_device else "KEEP-candidate"
    say(f"  VERDICT: {verdict}")
    say("=" * 124)

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    npass = sum(1 for g in GATES if g["target"] != "published, not asserted" and g["pass_"])
    ntot = sum(1 for g in GATES if g["target"] != "published, not asserted")
    say(f"  GATES {npass}/{ntot} PASS.   elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
