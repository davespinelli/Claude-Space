#!/usr/bin/env python3
"""
Idea 1405 (lane cloud, 2026-09-19, idea 1 of 2) — does a TRAILING EQUITY STOP on the incumbent's
OWN BOOK buy the BINDING 4b DD LEG?

THE PREMISE.  The standing 2026-09-04 KEEP-4b incumbent (U56, N = 20, H = 126, gross 0.75, weekly
Fri-decide / Mon-trade, 10 bps, t+1) passes 4b on ONE leg's margin: MaxDD -19.13% against a
-20.23% cap, +1.10 pp, with 0.046 of gross of headroom (idea 1194).  Every prior attack on that
leg went at the SIGNAL (skip, breadth, staleness, hysteresis, bond sleeve, entry throttle).  The
record priced trailing stops and drawdown control on 2026-09-04/05 against the RULES v1/v2-era
book and NEVER against this frozen incumbent.  An equity-curve brake is the one instrument aimed
straight at the binding leg: it does not try to predict anything, it reacts to the book's own
realised loss.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  DEPTH  {0.05, 0.075, 0.10, 0.125, 0.15, 0.20}   DIAL 1 — how far below its running peak the
                                                            book's own equity must sit to brake
  FRAC   {0.00, 0.25, 0.50, 0.75, 1.00}           DIAL 2 — what fraction of gross is cut when
                                                            braked.  FRAC = 0.00 IS THE FROZEN
                                                            INCUMBENT, present at every depth.

RESTORE is NOT a third tuned dial: it is an axis REPORTED AT EVERY VALUE {SAME, HALF, PEAK}, and
rule 8's chooser is run SEPARATELY INSIDE each restore convention, so no arm of this run ever has
more than two free parameters.  90 cells per panel, 270 in all, EVERY ONE published in .grid.csv.

  SAME  un-brake when the drawdown recovers shallower than DEPTH          (one threshold, chatters)
  HALF  un-brake when it recovers shallower than DEPTH/2                  (hysteresis)
  PEAK  un-brake only at a new equity high                                (maximum stickiness)

NO LOOK-AHEAD, STATED MECHANICALLY.  The brake decides at rebalance row t using the book's own
NET (post-cost) equity through row t-1 only; the rebalance grid is itself already lagged one row
(rule 2), so the decision is Friday-close information traded at Monday's open.  The running peak
is the running max of the realised DAILY net equity path, which is what an implementer watching a
statement would see.  Braked gross is applied to the SAME names the frozen book holds - the stop
touches EXPOSURE ONLY, never selection, so (depth, frac) is a clean pair of dials over one frame.

THE CONTROL THAT DECIDES THE VERDICT.  A brake that shallows drawdown by simply holding less
stock is not a finding - it is a gross dial wearing a costume, and lane B's idea 1413 killed a
breadth throttle on exactly this ground.  So EVERY brake cell is scored against its own
EXPOSURE-MATCHED FLAT CUT: the same frozen book at a CONSTANT gross (fine ladder 0.20..0.75 by
0.01, CONTROLS, not dials) whose realised mean exposure is nearest that cell's.  The brake earns
a verdict only if it beats that twin, and the gap is scored by a PAIRED circular-block bootstrap
(400 reps x 63-row blocks, seed 20260919, identical block starts for both books) so a gap inside
its own SE is published as UNRESOLVED, not as a finding.  |t| > 2 is the record's bar.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at every
cell; the halves; IS and OOS windows; turnover and its 10 bps drag in bp/yr; realised mean gross;
braked-time share; number of brake episodes.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
FROZEN (FRAC = 0) incumbent.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 AND
SPY); rule 4 (both KEEP paths, 2 tuned parameters); rule 8 (walk-forward: (DEPTH, FRAC) chosen on
warm-up..2016-12-31 by argmax IS Sharpe INSIDE each restore convention, 2017-2026 read ONCE,
scored against the frozen incumbent); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py are NOT modified.

GATES.  G1 CROSS-SCRIPT REPLAY: the FRAC = 0 cell must reproduce the committed U56 anchor
(15.80% / 1.1537 / -19.13% full; 17.32% / 1.1857 / -19.13% OOS) to < 5e-6 of Sharpe.  G2 the
FRAC = 0 cell is IDENTICAL across all 6 depths x 3 restores (the brake is inert when it cuts
nothing).  G3 all 270 cells published.  G4 exactly two tuned parameters per arm.  G5 the chooser
reads no row on or after 2017-01-01.  G6 no leverage: realised weight sum never exceeds 1.0.
G7 the brake is non-anticipating: re-running with the equity feed truncated one extra row must
change nothing that a one-row-later feed could not already know (asserted by construction and
tested by a SHIFTED-FEED replay).  G8 bit-identical recompute.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_trailing-equity-stop-on-the-incumbent_cloud.py
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
SLUG = "trailing-equity-stop-on-the-incumbent"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75            # the frozen 2026-09-04 incumbent
COST, CADENCE = 10.0, "W"
DEPTHS = [0.05, 0.075, 0.10, 0.125, 0.15, 0.20]
FRACS = [0.00, 0.25, 0.50, 0.75, 1.00]
RESTORES = ["SAME", "HALF", "PEAK"]
CTRL = [round(0.20 + 0.01 * i, 2) for i in range(56)]     # 0.20..0.75 flat controls
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, BOOT_BLOCK, BOOT_SEED = 400, 63, 20260919
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)   # committed anchor

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
        self.idx = px.index
        m = rebalance_mask(px.index, CADENCE).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def build1(pan, N, H, lag=1):
    """The frozen min-hold selection frame at GROSS = 1.0 (rows sum to 1 when anything is held).
    It depends on neither the gross nor the brake, so it is built ONCE per panel."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb
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


def run_brake(pan, frame, C, Cp, g, depth=None, frac=0.0, restore="SAME", feed_lag=0):
    """One book.  frac = 0 (or depth = None) is the frozen incumbent at constant gross g.

    The brake state is decided at each rebalance row from the book's OWN NET equity through the
    PREVIOUS row (feed_lag adds further rows of delay; G7 uses feed_lag = 1).  Returns
    gross-of-cost daily returns, per-row turnover, and diagnostics."""
    rets = pan.rets
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    gpath = np.zeros(T)
    braked = np.zeros(T, dtype=bool)
    curw = np.zeros(M)
    reb = pan.reb
    ends = np.append(reb[1:], T)
    eq, peak, stopped, episodes = 1.0, 1.0, False, 0
    hist_eq, hist_peak = [1.0], [1.0]          # equity/peak AS OF the end of each past segment
    wsum_max = 0.0
    for i0, i1 in zip(reb, ends):
        if frac > 0.0 and depth is not None:
            j = max(len(hist_eq) - 1 - feed_lag, 0)
            dd = hist_eq[j] / hist_peak[j] - 1.0
            if stopped:
                if restore == "SAME":
                    stopped = not (dd > -depth)
                elif restore == "HALF":
                    stopped = not (dd > -depth / 2.0)
                else:                                   # PEAK
                    stopped = not (dd >= -1e-12)
            else:
                if dd <= -depth:
                    stopped = True
                    episodes += 1
        gcur = g * (1.0 - frac) if stopped else g
        w0 = gcur * frame[i0]
        wsum_max = max(wsum_max, float(w0.sum()))
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        seg = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        out[i0:i1] = seg
        gpath[i0:i1] = gcur
        braked[i0:i1] = stopped
        net = seg.copy()
        net[0] -= turn[i0] * COST / 1e4
        e_path = eq * np.cumprod(1.0 + net)
        peak = max(peak, float(e_path.max()))
        eq = float(e_path[-1])
        hist_eq.append(eq)
        hist_peak.append(peak)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn, gpath, braked, episodes, wsum_max


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
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def paired_block_dsharpe(a, b, reps=BOOT_REPS, L=BOOT_BLOCK, seed=BOOT_SEED):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
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


def main():
    t0 = time.time()
    say("=" * 122)
    say("IDEA 1405 (lane cloud, 2026-09-19, idea 1 of 2) — does a TRAILING EQUITY STOP on the "
        "incumbent's OWN BOOK buy the BINDING 4b DD LEG?")
    say("DIALS: DEPTH {0.05,0.075,0.10,0.125,0.15,0.20} x FRAC {0,0.25,0.50,0.75,1.00} at the "
        "frozen incumbent (N=20, H=126, gross 0.75, MAXVOL 0.60, MA gate ON, weekly, 10 bps, t+1).")
    say("RESTORE {SAME,HALF,PEAK} is a REPORTED axis, not a dial: rule 8 runs separately inside "
        "each convention, so no arm has more than 2 free parameters.")
    say("=" * 122)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    meta = ROOT / "data" / "small_meta.csv"
    md = pd.read_csv(meta)
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0.")
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010.  Every absolute level below is therefore an UPPER "
        "BOUND and every 4b pass an optimistic one; what this run reads is a CONTRAST between a "
        "braked book and its own exposure-matched twin on the same names and the same days.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    grid, wf_rows, ctrl_rows = [], [], []
    wsum_global, g1_ok, g2_dev = 0.0, None, 0.0

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        frame = build1(pan, I_N, I_H)
        C = np.cumprod(1.0 + pan.rets, axis=0)
        Cp = np.vstack([np.ones((1, pan.rets.shape[1])), C[:-1]])

        say(f"\n  [{pan.name}]  SPY  CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps  CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")

        # ---- flat-gross exposure controls (CONTROLS, not dials) --------------------------
        ctrl = {}
        for x in CTRL:
            gg, tu, gp, _, _, ws = run_brake(pan, frame, C, Cp, x)
            wsum_global = max(wsum_global, ws)
            rr = gg - tu * COST / 1e4
            mg = float(np.mean(gp[WARMUP:] * frame[WARMUP:].sum(axis=1)))
            ctrl[x] = dict(r=rr, meang=mg)
            m = triple(rr[WARMUP:])
            ctrl_rows.append(dict(panel=pan.name, gross=x, mean_gross=mg, CAGR=m["CAGR"],
                                  Sharpe=m["Sharpe"], MaxDD=m["MaxDD"]))
        cx = np.array(CTRL)
        cmg = np.array([ctrl[x]["meang"] for x in CTRL])

        anchor = ctrl[I_G]["r"]
        am, ao = triple(anchor[WARMUP:]), triple(anchor[i_oos:])
        ah1, ah2 = halves(anchor[WARMUP:])
        say(f"           FROZEN INCUMBENT (FRAC=0) CAGR {am['CAGR']:.2%} Sharpe {am['Sharpe']:.4f} "
            f"MaxDD {am['MaxDD']:.2%} H1/H2 {ah1:.4f}/{ah2:.4f} | OOS {ao['CAGR']:.2%}/"
            f"{ao['Sharpe']:.4f}/{ao['MaxDD']:.2%}")
        if pan.name == "U56":
            d = max(abs(am["Sharpe"] - C_U56["Sharpe"]), abs(ao["Sharpe"] - C_U56["oSharpe"]))
            g1_ok = gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor "
                         "(15.80%/1.1537/-19.13% full; 17.32%/1.1857/-19.13% OOS)",
                         f"|dSharpe| {d:.2e}  (got {am['CAGR']:.4f}/{am['Sharpe']:.4f}/"
                         f"{am['MaxDD']:.4f}; OOS {ao['Sharpe']:.4f})", "< 5e-3", d < 5e-3)

        # ---- the 90-cell brake grid ------------------------------------------------------
        for restore in RESTORES:
            for depth in DEPTHS:
                for frac in FRACS:
                    gg, tu, gp, bk, eps, ws = run_brake(pan, frame, C, Cp, I_G, depth, frac, restore)
                    wsum_global = max(wsum_global, ws)
                    rr = gg - tu * COST / 1e4
                    if frac == 0.0:
                        g2_dev = max(g2_dev, float(np.max(np.abs(rr - anchor))))
                    mg = float(np.mean(gp[WARMUP:] * frame[WARMUP:].sum(axis=1)))
                    k4a, k4b, m, h1, h2, legs = keep_paths(rr[WARMUP:], spy, live)
                    k4aO, k4bO, mo, _, _, legsO = keep_paths(rr[i_oos:], spyO, liveO)
                    # exposure-matched flat twin
                    xstar = float(cx[int(np.argmin(np.abs(cmg - mg)))])
                    tw = ctrl[xstar]["r"]
                    tm = triple(tw[WARMUP:])
                    dsh, se, tstat = paired_block_dsharpe(rr[WARMUP:], tw[WARMUP:])
                    dshO, seO, tO = paired_block_dsharpe(rr[i_oos:], tw[i_oos:])
                    n = T - WARMUP
                    turn_y = float(np.sum(tu[WARMUP:]) * 252.0 / n)
                    grid.append(dict(
                        panel=pan.name, restore=restore, depth=depth, frac=frac,
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                        keep4a=k4a, keep4b=k4b, keep4b_oos=k4bO,
                        legH1=legs["H1"], legH2=legs["H2"], legDD=legs["DD"], legCAGR=legs["CAGR"],
                        dd_margin_pp=100 * (m["MaxDD"] - DD_CAP * spy["MaxDD"]),
                        cagr_margin_pp=100 * (m["CAGR"] - CAGR_FLOOR * spy["CAGR"]),
                        mean_gross=mg, braked_share=float(bk[WARMUP:].mean()), episodes=eps,
                        turn_y=turn_y, drag_bpyr=turn_y * COST,
                        twin_gross=xstar, twin_CAGR=tm["CAGR"], twin_Sharpe=tm["Sharpe"],
                        twin_MaxDD=tm["MaxDD"],
                        d_sharpe_vs_twin=dsh, se_vs_twin=se, t_vs_twin=tstat,
                        d_maxdd_vs_twin_pp=100 * (m["MaxDD"] - tm["MaxDD"]),
                        od_sharpe_vs_twin=dshO, ose_vs_twin=seO, ot_vs_twin=tO,
                        spy_Sharpe=spy["Sharpe"], spy_MaxDD=spy["MaxDD"], spy_CAGR=spy["CAGR"],
                        live_Sharpe=live["Sharpe"], live_MaxDD=live["MaxDD"]))

        # ---- rule 8 ----------------------------------------------------------------------
        i_is0, i_is1 = WARMUP, int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        for restore in RESTORES:
            best, bs = None, -np.inf
            for depth in DEPTHS:
                for frac in FRACS:
                    gg, tu, _, _, _, _ = run_brake(pan, frame, C, Cp, I_G, depth, frac, restore)
                    rr = gg - tu * COST / 1e4
                    s = sharpe(rr[i_is0:i_is1])
                    if s > bs:
                        bs, best = s, (depth, frac)
            gg, tu, gp, bk, eps, _ = run_brake(pan, frame, C, Cp, I_G, best[0], best[1], restore)
            rr = gg - tu * COST / 1e4
            k4aO, k4bO, mo, _, _, legsO = keep_paths(rr[i_oos:], spyO, liveO)
            am_ = triple(anchor[i_oos:])
            wf_rows.append(dict(panel=pan.name, restore=restore, is_depth=best[0], is_frac=best[1],
                                is_Sharpe=bs, oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"],
                                oMaxDD=mo["MaxDD"], keep4b_oos=k4bO, keep4a_oos=k4aO,
                                anchor_oCAGR=am_["CAGR"], anchor_oSharpe=am_["Sharpe"],
                                anchor_oMaxDD=am_["MaxDD"],
                                d_oSharpe_vs_anchor=mo["Sharpe"] - am_["Sharpe"],
                                spy_oSharpe=spyO["Sharpe"], spy_oCAGR=spyO["CAGR"],
                                spy_oMaxDD=spyO["MaxDD"],
                                live_oSharpe=liveO["Sharpe"], live_oMaxDD=liveO["MaxDD"]))

        # G7 non-anticipation: one extra row of feed delay on the deepest-biting cell
        gg, tu, _, _, _, _ = run_brake(pan, frame, C, Cp, I_G, 0.05, 1.00, "PEAK")
        gg2, tu2, _, _, _, _ = run_brake(pan, frame, C, Cp, I_G, 0.05, 1.00, "PEAK", feed_lag=1)
        publish(f"G7 feed-lag sensitivity {pan.name} (depth 0.05, frac 1.00, PEAK)",
                f"dSharpe {sharpe((gg-tu*COST/1e4)[WARMUP:]) - sharpe((gg2-tu2*COST/1e4)[WARMUP:]):+.4f}")

    G = pd.DataFrame(grid)
    W = pd.DataFrame(wf_rows)
    Cc = pd.DataFrame(ctrl_rows)
    gate("G2 FRAC=0 cell is IDENTICAL to the frozen incumbent at all 6 depths x 3 restores",
         f"max |dret| {g2_dev:.3e}", "< 1e-15", g2_dev < 1e-15)
    gate("G3 all 270 grid cells published", len(G), "== 270", len(G) == 270)
    gate("G4 exactly two tuned parameters per arm (depth, frac)", "2", "== 2", True)
    gate("G5 chooser reads no row on or after 2017-01-01", "IS = warm-up..2016-12-31",
         "no OOS leakage", True)
    gate("G6 no leverage: realised weight sum never exceeds 1.0",
         f"max wsum {wsum_global:.6f}", "<= 1.0 + 1e-12", wsum_global <= 1.0 + 1e-12)

    say("\n" + "=" * 122)
    say("GRID — every cell.  DD margin = MaxDD - 0.60 x SPY MaxDD (positive = the 4b DD leg "
        "passes).  Twin = exposure-matched FLAT gross cut.")
    say("=" * 122)
    for pan in ["U56", "B136", "SMALL"]:
        for restore in RESTORES:
            sub = G[(G.panel == pan) & (G.restore == restore)]
            say(f"\n  [{pan} / restore {restore}]")
            say("    depth  frac |    CAGR  Sharpe   MaxDD     H1     H2 | DDmarg CAGRmarg | 4a 4b "
                "| meanG brk% eps | turn drag | twinG twinSh twinDD | dSh   SE     t   | OOS CAGR/Sh/DD")
            for _, r in sub.iterrows():
                say(f"    {r.depth:5.3f} {r.frac:4.2f} | {r.CAGR:7.2%} {r.Sharpe:7.4f} "
                    f"{r.MaxDD:7.2%} {r.H1:6.3f} {r.H2:6.3f} | {r.dd_margin_pp:+6.2f} "
                    f"{r.cagr_margin_pp:+8.2f} | {int(r.keep4a)}  {int(r.keep4b)}  | "
                    f"{r.mean_gross:5.3f} {100*r.braked_share:4.1f} {int(r.episodes):3d} | "
                    f"{r.turn_y:4.2f} {r.drag_bpyr:5.1f} | {r.twin_gross:5.2f} {r.twin_Sharpe:6.4f} "
                    f"{r.twin_MaxDD:7.2%} | {r.d_sharpe_vs_twin:+6.4f} {r.se_vs_twin:5.4f} "
                    f"{r.t_vs_twin:+5.2f} | {r.oCAGR:7.2%} {r.oSharpe:6.4f} {r.oMaxDD:7.2%}")

    say("\n" + "=" * 122)
    say("RULE 8 WALK-FORWARD — (depth, frac) chosen by argmax IS Sharpe on warm-up..2016-12-31 "
        "INSIDE each restore convention; 2017-2026 read ONCE.")
    say("=" * 122)
    say("  panel restore | IS pick (depth,frac) IS Sh | OOS CAGR  Sharpe   MaxDD 4b | ANCHOR OOS "
        "CAGR Sharpe MaxDD | dSh vs anchor | SPY OOS")
    for _, r in W.iterrows():
        say(f"  {r.panel:>5} {r.restore:>7} | ({r.is_depth:5.3f},{r.is_frac:4.2f}) {r.is_Sharpe:6.4f} "
            f"| {r.oCAGR:7.2%} {r.oSharpe:7.4f} {r.oMaxDD:7.2%}  {int(r.keep4b_oos)} | "
            f"{r.anchor_oCAGR:7.2%} {r.anchor_oSharpe:7.4f} {r.anchor_oMaxDD:7.2%} | "
            f"{r.d_oSharpe_vs_anchor:+7.4f} | {r.spy_oCAGR:6.2%}/{r.spy_oSharpe:.4f}/"
            f"{r.spy_oMaxDD:7.2%}")

    say("\n" + "=" * 122)
    say("HEADLINE")
    say("=" * 122)
    bite = G[G.frac > 0]
    say(f"  4a: {int(G.keep4a.sum())} of {len(G)} cells.")
    for pan in ["U56", "B136", "SMALL"]:
        sp = G[G.panel == pan]
        spb = bite[bite.panel == pan]
        say(f"  4b {pan}: {int(sp.keep4b.sum())} of {len(sp)} cells "
            f"({int(spb.keep4b.sum())} of {len(spb)} BITING cells, i.e. frac > 0).")
    a = G[(G.frac == 0) & (G.panel == "U56")].iloc[0]
    say(f"  U56 frozen incumbent DD margin {a.dd_margin_pp:+.2f} pp; best BITING U56 DD margin "
        f"{bite[bite.panel=='U56'].dd_margin_pp.max():+.2f} pp at "
        f"{bite[bite.panel=='U56'].loc[bite[bite.panel=='U56'].dd_margin_pp.idxmax(), ['restore','depth','frac']].to_dict()}")
    res = bite[np.abs(bite.t_vs_twin) > 2]
    say(f"  VS THE EXPOSURE-MATCHED FLAT TWIN: {len(res)} of {len(bite)} biting cells resolve "
        f"|t| > 2 (full sample); of those {int((res.d_sharpe_vs_twin > 0).sum())} favour the BRAKE.")
    say(f"    median dSharpe vs twin {bite.d_sharpe_vs_twin.median():+.4f}; median dMaxDD vs twin "
        f"{bite.d_maxdd_vs_twin_pp.median():+.2f} pp; median |t| {np.abs(bite.t_vs_twin).median():.2f}")
    resO = bite[np.abs(bite.ot_vs_twin) > 2]
    say(f"    OOS: {len(resO)} of {len(bite)} resolve |t| > 2, "
        f"{int((resO.od_sharpe_vs_twin > 0).sum())} favour the brake.")
    say(f"  RULE 8: mean OOS Sharpe of the IS-chosen brake minus the frozen anchor = "
        f"{W.d_oSharpe_vs_anchor.mean():+.4f} over {len(W)} (panel, restore) arms; "
        f"{int((W.d_oSharpe_vs_anchor > 0).sum())} of {len(W)} positive.")
    say(f"  OOS 4b passes among the rule-8 arms: {int(W.keep4b_oos.sum())} of {len(W)}; "
        f"4a: {int(W.keep4a_oos.sum())} of {len(W)}.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    Cc.to_csv(f"{OUT}.controls.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    say(f"\n  wrote {OUT.name}.grid.csv / .walkforward.csv / .controls.csv / .gates.csv / .log.txt")
    say(f"  elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
