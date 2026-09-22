#!/usr/bin/env python3
"""Idea 1480 (lane cloud, 2026-09-22): does the 1468 H_HINDSIGHT STOP survive a
DE-GROSS TWIN, a COST LADDER and ANY LEGAL IS-ONLY CHOOSER?

THE CELL UNDER TEST.  Idea 1468's one book clearing 4b on the FULL sample AND out of
sample while beating the frozen 2026-09-04 incumbent on both Sharpes is U56, trailing
equity stop at FRAC = 0.50, depth = 0.075 (published full 13.71% / 1.1713 / -14.54%,
OOS 15.52% / 1.2689 / -14.54%, against the anchor's 15.80% / 1.1537 / -19.13% and
1.1857).  NO rule-8 chooser in that run reached it -- the IS-argmax picked depth 0 on
every panel.  This run prices the cell the way the record prices every DD-buying device.

CONSTRUCTION (frozen from idea 1468 so the numbers are commensurable; the selection
frame, the stop mechanics and the metric conventions are PORTED from
`research/backtests/2026-09-19_dd-per-cagr-slope-measurability_cloud.py`)
  ANCHOR: the frozen 2026-09-04 incumbent -- top N = 20 by the 3-leg composite
    (21/252, 0/126, 0/63 rank-averaged, halved when below the 200d MA), eligible =
    above the 200d MA and vol20 < 0.60, MIN HOLD H = 126 trading days, equal weight at
    gross 0.75, weekly (last trading day of the ISO week), decided at close t and
    applied at t+1.
  DEVICE STOP(d): at each rebalance the book reads its OWN NET equity drawdown through
    the PREVIOUS segment (known at the decision close).  On dd <= -d it scales the whole
    target book by (1 - FRAC), FRAC = 0.50 FROZEN at 1468's non-absorbing headline arm;
    it restores (RESTORE = "SAME") the first rebalance at which dd > -d.  d = 0 is the
    un-braked anchor and is BIT-IDENTICAL to it (gate G2).
  TWIN: the SAME anchor scaled by a CONSTANT k chosen so its CAGR EQUALS the stop book's
    CAGR at that same cost rung (secant iterations; achieved match is gate G4).  A device
    that buys drawdown only by holding less is dominated by this scalar.

  TUNED PARAMETERS: exactly two, STOP DEPTH d and COST RUNG c.  PANEL {U56, B136, SMALL},
  FRAC (0.50) and cadence (W) are REPORTED, never selected on, and every grid point is
  published.

  COSTS 0 / 10 / 25 / 50 bps.  The stop reads its own NET equity, so cost FEEDS BACK into
  the positions and no zero-cost reconstruction is legal here: every cell is a FRESH run
  at its own rung.  10 bps is PROTOCOL rule 2's binding rung and carries the headline.

  RULE 8: the depth is chosen on the FIRST HALF ONLY (IS = warm-up .. 2016-12-31) by FOUR
  LEGAL IS-ONLY CHOOSERS -- argmax IS Sharpe, argmax IS 4b-leg count, IS PERCENTILE (the
  rung at the 75th percentile of the IS-Sharpe ordering, a shrunk argmax), and STEEPEST IS
  SLOPE (argmax of dMaxDD/dCAGR against the IS anchor) -- and 2017-2026 is read ONCE at the
  end.  The queue's question is whether ANY of them reaches d = 0.075.

SURVIVORSHIP CAVEAT: U56 and B136 are CURRENT constituents (PROTOCOL rule 9).  The SMALL
panel is current constituents of a sub-$2B screen (data/SMALL_PANEL_README.md), biased
upward; tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped first.  SMALL
is used only as a THIRD panel for the DIRECTION of the effect, never as a capital book.

Run: python3 research/backtests/2026-09-22_hindsight-stop-degross-cost-chooser_cloud.py
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights          # noqa: E402
from engine import backtest, rebalance_mask                   # noqa: E402

DATE, SLUG = "2026-09-22", "hindsight-stop-degross-cost-chooser"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75              # the frozen 2026-09-04 incumbent
CADENCE = "W"
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
DEPTHS = [0.0, 0.05, 0.075, 0.10, 0.125, 0.15, 0.20]   # 1405's published ladder, + the anchor
FRAC = 0.50                                            # FROZEN (1468's non-absorbing arm)
RESTORE = "SAME"                                       # FROZEN
COSTS = [0.0, 10.0, 25.0, 50.0]
HEADLINE = 10.0
TARGET_DEPTH = 0.075                                   # the hindsight cell
PCTL = 0.75                                            # the IS-PERCENTILE chooser's level
# idea 1468's committed U56 anchor and headline cell, for the cross-script replay gates
C1468_ANCHOR = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857, oCAGR=0.1732)
C1468_CELL = dict(CAGR=0.1371, Sharpe=1.1713, MaxDD=-0.1454, oCAGR=0.1552, oSharpe=1.2689, oMaxDD=-0.1454)

LOG, GATES = [], []
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)
def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)
def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    say(f"    PUBLISHED  {name}: {value}")

# ------------------------------------------------------------------ mechanics (ported)
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
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])

def segments(pan, N=I_N, H=I_H, lag=1):
    """The frozen min-hold selection frame.  Built ONCE per panel; every depth and every
    cost rung holds the IDENTICAL names (gate G3)."""
    T = pan.rets.shape[0]; K = len(pan.iinv)
    cur = np.full(K, -1, dtype=np.int64); pr = pan.priced[:, pan.iinv]; reb = pan.reb
    segs = []
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young): young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep); take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep: k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep: new[c] = cur[c]
        for c in take: new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        stop = reb[i + 1] if i + 1 < len(reb) else T
        segs.append((int(t), int(stop), int(ts), sel.copy()))
    return segs

def w_equal(segs, gross):
    return [np.full(len(sel), gross / len(sel)) if len(sel) else np.zeros(0)
            for (_t, _s, _ts, sel) in segs]

def run_book(pan, segs, ws, cost, depth=None, frac=0.0, restore=RESTORE):
    """One book at ONE cost rung.  The brake decides at each rebalance row from the book's
    OWN NET equity through the PREVIOUS segment only (causal: known at the decision close)."""
    rets, C, Cp = pan.rets, pan.C, pan.Cp
    T, M = rets.shape
    turn = np.zeros(T); out = np.zeros(T); gpath = np.zeros(T); curw = np.zeros(M)
    eq, peak, stopped, episodes, braked = 1.0, 1.0, False, 0, 0
    for (i0, i1, _ts, sel), wv in zip(segs, ws):
        if frac > 0.0 and depth is not None and depth > 0:
            dd = eq / peak - 1.0
            if stopped:
                stopped = not (dd > -depth) if restore == "SAME" else not (dd > -depth / 2.0)
            elif dd <= -depth:
                stopped = True; episodes += 1
        scale = (1.0 - frac) if stopped else 1.0
        w0 = np.zeros(M)
        if len(sel): w0[pan.iinv[sel]] = wv * scale
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        seg = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        out[i0:i1] = seg; gpath[i0:i1] = w0.sum()
        if stopped: braked += (i1 - i0)
        nt = seg.copy(); nt[0] -= turn[i0] * cost / 1e4
        e_path = eq * np.cumprod(1.0 + nt)
        peak = max(peak, float(e_path.max())); eq = float(e_path[-1])
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    net = out - turn * cost / 1e4
    return dict(net=net, turn=turn, gross=gpath, episodes=episodes, braked_rows=braked)

# ------------------------------------------------------------------ statistics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5: return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan
def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan
def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5: return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)
def triple(r): return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))
def halves(r):
    h = len(r) // 2; return sharpe(r[:h]), sharpe(r[h:])
def pack(r, om):
    h1, h2 = halves(r); m = triple(r); o = triple(r[om])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"])
def keep_paths(m, spy, live):
    k4a = bool(m["H1"] > live["H1"] and m["H2"] > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(m["H1"] > spy["H1"]), H2=bool(m["H2"] > spy["H2"]),
                OOS=bool(m["OOS_Sharpe"] > spy["OOS_Sharpe"]),
                DD=bool(m["MaxDD"] >= DD_CAP * spy["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * spy["CAGR"]))
    return k4a, bool(all(legs.values())), legs
def legs_count_is(r_is, spy_is):
    """IS-only 4b leg count: the legs that CAN be read on IS rows alone."""
    m = triple(r_is); h1, h2 = halves(r_is)
    return int(h1 > spy_is["H1"]) + int(h2 > spy_is["H2"]) + \
           int(m["MaxDD"] >= DD_CAP * spy_is["MaxDD"]) + int(m["CAGR"] >= CAGR_FLOOR * spy_is["CAGR"])

def matched_twin(pan, segs, gross, cost, target_cagr, k0=1.0):
    """Anchor scaled by a CONSTANT k so its CAGR equals target_cagr at this cost rung."""
    f = lambda k: cagr(run_book(pan, segs, w_equal(segs, gross * k), cost)["net"][WARMUP:]) - target_cagr
    a, b = max(0.02, k0 * 0.6), min(2.5, max(0.05, k0 * 1.4))
    fa, fb = f(a), f(b)
    tries = 0
    while fa * fb > 0 and tries < 6:
        a = max(0.01, a * 0.6); b = min(3.0, b * 1.4); fa, fb = f(a), f(b); tries += 1
    if fa * fb > 0:
        k = k0; return k, f(k) + target_cagr, abs(f(k))
    best_k, best_f = 0.5 * (a + b), np.inf
    for _ in range(60):
        mid = 0.5 * (a + b); fm = f(mid)
        if abs(fm) < abs(best_f): best_k, best_f = mid, fm
        if fa * fm <= 0: b, fb = mid, fm
        else: a, fa = mid, fm
        if abs(fm) < 1e-9: break
    return best_k, best_f + target_cagr, abs(best_f)

# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"IDEA 1480 (lane cloud) -- {DATE}.  FRAC {FRAC} FROZEN, RESTORE {RESTORE}.")
    say(f"  TUNED: depth d {DEPTHS} x cost rung {COSTS} bps.  REPORTED: panel, FRAC, cadence {CADENCE}.")
    pxU = load_universe(); pxB = load_universe(broad=True); pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(md.loc[md["max_1d_move"] >= 1.0, "ticker"])
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad]
    say(f"  SMALL filter (protocol-mandated): drops {len(bad)} tickers with max_1d_move >= 1.0; "
        f"{len(inv)} investable names remain.  SURVIVORSHIP: current constituents only.")
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]

    grid, wf, series = [], [], {}
    for pan in panels:
        segs = segments(pan)
        om = pan.idx[WARMUP:] >= OOS_START
        ism = pan.idx[WARMUP:] <= IS_END
        spy = pan.spy[WARMUP:]
        say(f"\n[{pan.name}] rows={len(spy)} {pan.idx[WARMUP].date()}..{pan.idx[-1].date()} "
            f" segs={len(segs)}  IS rows={int(ism.sum())}  OOS rows={int(om.sum())}  ({time.time()-t0:.0f}s)")
        # names held are depth- and cost-independent (gate G3)
        publish(f"G3_selection_frame_{pan.name}", f"{len(segs)} segments, mean n held "
                f"{np.mean([len(s[3]) for s in segs]):.2f}")
        spy_pack = pack(spy, om)
        for c in COSTS:
            v2 = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=c, freq=CADENCE)["returns"].values[WARMUP:]
            live = pack(v2, om)
            anc = run_book(pan, segs, w_equal(segs, I_G), c)
            anc_r = anc["net"][WARMUP:]; anc_m = pack(anc_r, om)
            for d in DEPTHS:
                bk = run_book(pan, segs, w_equal(segs, I_G), c, depth=d, frac=(FRAC if d > 0 else 0.0))
                r = bk["net"][WARMUP:]; m = pack(r, om)
                k, tw_cagr, err = matched_twin(pan, segs, I_G, c, m["CAGR"],
                                               k0=(m["CAGR"] / anc_m["CAGR"] if anc_m["CAGR"] > 0 else 1.0))
                tw = run_book(pan, segs, w_equal(segs, I_G * k), c)
                tw_r = tw["net"][WARMUP:]; tw_m = pack(tw_r, om)
                a4, b4, legs = keep_paths(m, spy_pack, live)
                ta4, tb4, tlegs = keep_paths(tw_m, spy_pack, live)
                row = dict(panel=pan.name, depth=d, cost_bps=c, frac=(FRAC if d > 0 else 0.0),
                           episodes=bk["episodes"], braked_rows=bk["braked_rows"],
                           mean_gross=float(bk["gross"][WARMUP:].mean()),
                           turnover_yr=float(bk["turn"][WARMUP:].sum() / (len(r) / 252)),
                           twin_k=k, twin_cagr_err=err,
                           twin_mean_gross=float(tw["gross"][WARMUP:].mean()),
                           twin_turnover_yr=float(tw["turn"][WARMUP:].sum() / (len(tw_r) / 252)))
                for pre, mm in (("stop", m), ("twin", tw_m), ("anch", anc_m), ("v2", live), ("spy", spy_pack)):
                    for kk, vv in mm.items(): row[f"{pre}_{kk}"] = vv
                row.update(stop_4a=a4, stop_4b=b4, twin_4a=ta4, twin_4b=tb4,
                           dMaxDD=m["MaxDD"] - tw_m["MaxDD"], dSharpe=m["Sharpe"] - tw_m["Sharpe"],
                           dCAGR=m["CAGR"] - tw_m["CAGR"],
                           dOOS_MaxDD=m["OOS_MaxDD"] - tw_m["OOS_MaxDD"],
                           dOOS_Sharpe=m["OOS_Sharpe"] - tw_m["OOS_Sharpe"],
                           beats_twin_dd=bool(m["MaxDD"] > tw_m["MaxDD"]),
                           beats_twin_sharpe=bool(m["Sharpe"] > tw_m["Sharpe"]),
                           **{f"leg_{k2}": v2_ for k2, v2_ in legs.items()})
                grid.append(row)
                series[(pan.name, c, d)] = dict(r=r, is_=r[ism], m=m, anc=anc_m, spy=spy_pack, live=live,
                                                twin=tw_m, twin_k=k)
                gate(f"G4_twin_cagr_match_{pan.name}_d{d}_c{int(c)}", f"{err:.2e}", "< 1e-6", err < 1e-6)
            say(f"  cost {int(c):>2} bps done ({time.time()-t0:.0f}s)")

        # ---- rule 8: four LEGAL IS-only choosers, 2017-2026 read ONCE
        for c in COSTS:
            spy_is = dict(zip(("H1", "H2"), halves(spy[ism])))
            spy_is.update(triple(spy[ism]))
            picks = {}
            cand = [d for d in DEPTHS]
            iss = {d: series[(pan.name, c, d)]["is_"] for d in cand}
            sh = {d: sharpe(iss[d]) for d in cand}
            picks["IS_SHARPE"] = max(cand, key=lambda d: sh[d])
            lg = {d: legs_count_is(iss[d], spy_is) for d in cand}
            picks["IS_LEGS"] = max(cand, key=lambda d: (lg[d], sh[d]))
            order = sorted(cand, key=lambda d: sh[d])
            picks["IS_PCTL"] = order[min(len(order) - 1, int(np.floor(PCTL * (len(order) - 1))))]
            anc_is = iss[0.0]
            slope = {}
            for d in cand:
                dC = (cagr(iss[d]) - cagr(anc_is)) * 100.0
                dD = (mdd(iss[d]) - mdd(anc_is)) * 100.0
                slope[d] = (dD / dC) if abs(dC) >= 1e-9 else -np.inf
            picks["IS_SLOPE"] = max(cand, key=lambda d: slope[d])
            for nm, d in picks.items():
                s = series[(pan.name, c, d)]
                a4, b4, legs = keep_paths(s["m"], s["spy"], s["live"])
                wf.append(dict(panel=pan.name, cost_bps=c, chooser=nm, picked_depth=d,
                               reaches_target=bool(abs(d - TARGET_DEPTH) < 1e-12),
                               IS_Sharpe=sh[d], IS_legs=lg[d], IS_slope=slope[d],
                               FULL_CAGR=s["m"]["CAGR"], FULL_Sharpe=s["m"]["Sharpe"], FULL_MaxDD=s["m"]["MaxDD"],
                               H1=s["m"]["H1"], H2=s["m"]["H2"],
                               OOS_CAGR=s["m"]["OOS_CAGR"], OOS_Sharpe=s["m"]["OOS_Sharpe"], OOS_MaxDD=s["m"]["OOS_MaxDD"],
                               anch_OOS_CAGR=s["anc"]["OOS_CAGR"], anch_OOS_Sharpe=s["anc"]["OOS_Sharpe"],
                               anch_OOS_MaxDD=s["anc"]["OOS_MaxDD"],
                               twin_OOS_CAGR=s["twin"]["OOS_CAGR"], twin_OOS_Sharpe=s["twin"]["OOS_Sharpe"],
                               twin_OOS_MaxDD=s["twin"]["OOS_MaxDD"],
                               v2_OOS_CAGR=s["live"]["OOS_CAGR"], v2_OOS_Sharpe=s["live"]["OOS_Sharpe"],
                               v2_OOS_MaxDD=s["live"]["OOS_MaxDD"],
                               spy_OOS_CAGR=s["spy"]["OOS_CAGR"], spy_OOS_Sharpe=s["spy"]["OOS_Sharpe"],
                               spy_OOS_MaxDD=s["spy"]["OOS_MaxDD"],
                               pick_4a=a4, pick_4b=b4))

    G = pd.DataFrame(grid); G.to_csv(f"{OUT}.grid.csv", index=False)
    W = pd.DataFrame(wf);  W.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ---------------- gates
    u10 = G[(G.panel == "U56") & (G.cost_bps == HEADLINE)]
    a0 = u10[u10.depth == 0.0].iloc[0]
    dev = max(abs(a0["stop_CAGR"] - C1468_ANCHOR["CAGR"]), abs(a0["stop_Sharpe"] - C1468_ANCHOR["Sharpe"]),
              abs(a0["stop_MaxDD"] - C1468_ANCHOR["MaxDD"]), abs(a0["stop_OOS_Sharpe"] - C1468_ANCHOR["oSharpe"]))
    gate("G1_replay_1468_U56_anchor", f"max |dev| {dev:.2e} "
         f"({a0['stop_CAGR']:.4f}/{a0['stop_Sharpe']:.4f}/{a0['stop_MaxDD']:.4f}/{a0['stop_OOS_Sharpe']:.4f})",
         "< 5e-4 vs 0.1580/1.1537/-0.1913/1.1857", dev < 5e-4)
    cell = u10[np.isclose(u10.depth, TARGET_DEPTH)].iloc[0]
    dev2 = max(abs(cell["stop_CAGR"] - C1468_CELL["CAGR"]), abs(cell["stop_Sharpe"] - C1468_CELL["Sharpe"]),
               abs(cell["stop_MaxDD"] - C1468_CELL["MaxDD"]), abs(cell["stop_OOS_CAGR"] - C1468_CELL["oCAGR"]),
               abs(cell["stop_OOS_Sharpe"] - C1468_CELL["oSharpe"]), abs(cell["stop_OOS_MaxDD"] - C1468_CELL["oMaxDD"]))
    gate("G2_replay_1468_U56_headline_cell_d0.075", f"max |dev| {dev2:.2e} "
         f"({cell['stop_CAGR']:.4f}/{cell['stop_Sharpe']:.4f}/{cell['stop_MaxDD']:.4f} | OOS "
         f"{cell['stop_OOS_CAGR']:.4f}/{cell['stop_OOS_Sharpe']:.4f}/{cell['stop_OOS_MaxDD']:.4f})",
         "< 5e-4 vs 0.1371/1.1713/-0.1454 | 0.1552/1.2689/-0.1454", dev2 < 5e-4)
    # G5: d = 0 is the anchor exactly, on every panel and rung
    e5 = float(np.abs(G[G.depth == 0.0]["stop_Sharpe"].values - G[G.depth == 0.0]["anch_Sharpe"].values).max())
    gate("G5_depth0_is_the_anchor", f"max |dev| {e5:.3e}", "== 0", e5 == 0.0)
    # G6: an unreachable depth never brakes
    p0 = panels[0]; s0 = segments(p0)
    nb = run_book(p0, s0, w_equal(s0, I_G), HEADLINE, depth=0.99, frac=FRAC)
    e6 = float(np.abs(nb["net"] - run_book(p0, s0, w_equal(s0, I_G), HEADLINE)["net"]).max())
    gate("G6_unreachable_depth_is_base", f"max |dev| {e6:.3e}, episodes {nb['episodes']}", "< 1e-15", e6 < 1e-15)
    # G7: the twin is a pure exposure scalar (no name or timing change)
    gate("G7_twin_is_pure_scalar", f"turnover ratio range "
         f"{(G.twin_turnover_yr / G.twin_k / G[G.depth==0.0].turnover_yr.mean()).min():.3f}..."
         f"{(G.twin_turnover_yr / G.twin_k / G[G.depth==0.0].turnover_yr.mean()).max():.3f}",
         "published", True)
    Gt = pd.DataFrame(GATES); Gt.to_csv(f"{OUT}.gates.csv", index=False)

    # ---------------- summary
    say(f"\n=== GRID: {len(G)} published cells ({len(DEPTHS)} depths x {len(COSTS)} rungs x 3 panels) ===")
    say("\n-- STOP minus its own CAGR-MATCHED DE-GROSS TWIN: dMaxDD (pp), by panel x cost, braking depths only --")
    br = G[G.depth > 0]
    say((br.pivot_table(index="panel", columns="cost_bps", values="dMaxDD") * 100).round(3).to_string())
    say("\n-- dSharpe (stop minus twin), by panel x cost --")
    say(br.pivot_table(index="panel", columns="cost_bps", values="dSharpe").round(4).to_string())
    say("\n-- how often the stop BEATS its twin (of {} braking cells) --".format(len(br)))
    say(br.groupby(["panel", "cost_bps"])[["beats_twin_dd", "beats_twin_sharpe"]].sum().to_string())
    say("\n-- KEEP counts (all cells) --")
    say(G.groupby(["panel", "cost_bps"])[["stop_4a", "stop_4b", "twin_4a", "twin_4b"]].sum().to_string())
    say(f"\n-- 4a total {int(G.stop_4a.sum())} of {len(G)};  4b total {int(G.stop_4b.sum())} of {len(G)};"
        f"  twin 4b {int(G.twin_4b.sum())} of {len(G)} --")
    say("\n-- THE HINDSIGHT CELL (U56, d = 0.075) across the cost ladder --")
    cols = ["cost_bps", "stop_CAGR", "stop_Sharpe", "stop_MaxDD", "stop_OOS_CAGR", "stop_OOS_Sharpe",
            "stop_OOS_MaxDD", "twin_k", "twin_MaxDD", "twin_OOS_Sharpe", "dMaxDD", "dSharpe",
            "stop_4a", "stop_4b", "episodes"]
    say(G[(G.panel == "U56") & (np.isclose(G.depth, TARGET_DEPTH))][cols].to_string(index=False,
        float_format=lambda x: f"{x:.4f}"))
    say("\n-- FULL GRID at the headline 10 bps rung --")
    say(G[G.cost_bps == HEADLINE][["panel", "depth", "stop_CAGR", "stop_Sharpe", "stop_MaxDD", "H1" if False else "stop_H1",
                                   "stop_H2", "stop_OOS_CAGR", "stop_OOS_Sharpe", "stop_OOS_MaxDD",
                                   "twin_k", "twin_MaxDD", "twin_Sharpe", "dMaxDD", "dSharpe",
                                   "stop_4a", "stop_4b", "twin_4b", "episodes", "mean_gross"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n-- RULE 8: four LEGAL IS-only choosers, depth chosen on IS rows alone; 2017-2026 read ONCE --")
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    n_reach = int(W.reaches_target.sum())
    say(f"\nTHE QUEUE'S QUESTION -- choosers reaching d = {TARGET_DEPTH}: {n_reach} of {len(W)} "
        f"({len(W.chooser.unique())} choosers x {len(COSTS)} rungs x 3 panels).")
    if n_reach: say(W[W.reaches_target].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n-- chooser picks by (panel, cost) --")
    say(W.pivot_table(index=["panel", "cost_bps"], columns="chooser", values="picked_depth").to_string())
    say(f"\n-- chooser picks that clear 4b: {int(W.pick_4b.sum())} of {len(W)};  4a: {int(W.pick_4a.sum())} of {len(W)} --")
    say(f"\nGATES: {sum(1 for g in GATES if g['pass_'])} of {len(GATES)} pass.")
    say(f"done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.out.txt").write_text("\n".join(LOG) + "\n")

if __name__ == "__main__":
    main()
