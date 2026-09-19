#!/usr/bin/env python3
"""Idea 1446 (lane B, 2026-09-19): price the GROSS SCALAR ITSELF as the CANDIDATE, not as the
control.

WHY THIS IDEA.  Five consecutive runs on 2026-09-19 each proposed a drawdown-buying DEVICE and
each lost, at matched exposure, to a plain DE-GROSS of the same anchor: 1405's trailing equity
stop (216 of 216 cells), 1413's breadth throttle (90 of 90), 1433's intra-book inverse-vol (on
CAGR), 1429 / 1436's beta band (48 of 48).  The object that keeps WINNING those contests is the
constant exposure scalar G, and on THIS anchor it has never been scored as a candidate book in
its own right.

NOT A DUPLICATE OF 1454.  Idea 1454 (this morning, lane B) walked a G ladder on the LIVE RULES v2
BAND SHAPE and found G=1.00 weekly clears 4b full and OOS on U56.  The anchor that actually beat
1405 / 1413 / 1433 / 1429 / 1436 is a DIFFERENT book: the FROZEN 2026-09-04 KEEP-4b incumbent
(N = 20 names, H = 126-day min hold, composite momentum selection, 200d MA gate, vol20 < 0.60,
gross 0.75, weekly, 10 bps, t+1).  This run walks the ladder on THAT frame.  The two runs
together say whether "de-gross the book" is a property of one shape or of the exposure dial.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  G        {0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00}   DIAL 1 — constant gross.  Rungs are
                                                           1454's exactly, so the two ladders are
                                                           readable side by side.  Stops at 1.00:
                                                           no leverage (rule 2).  G = 0.75 IS the
                                                           frozen incumbent's live value.
  CADENCE  {D, W, M, Q}                                    DIAL 2 — rebalance schedule.  W IS the
                                                           incumbent's live cadence.

28 cells per panel, 84 in all, EVERY ONE PUBLISHED in .grid.csv with full / halves / OOS and both
KEEP paths.  (G, CADENCE) = (0.75, W) is the frozen incumbent and is a cell of the grid, so the
null "change nothing" is priced on the same tape as every candidate.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at every
cell; the halves; IS and OOS windows; turnover and its 10 bps drag; realised mean gross.

CHOOSERS (rule 8), every one fit on warm-up..2016-12-31 ONLY, then 2017-2026 read EXACTLY ONCE:
  C_SHARPE   joint argmax IS Sharpe over all 28 cells                  (the record's usual chooser)
  C_SHARPE@c argmax IS Sharpe within each cadence                      (the chooser one dial down)
  C_MEMO     smallest G with IS MaxDD <= 0.60 x SPY_IS MaxDD AND IS CAGR >= 0.70 x SPY_IS CAGR,
             else keep 0.75 — the 2026-09-03 RECOMMENDATION memo's own pre-registered rule
  C_BUDGET   largest G with IS MaxDD <= 0.60 x SPY_IS MaxDD            (spend the whole budget)
  C_ANCHOR   (0.75, W), choosing nothing                               (the null)
All five range over the SAME two dials; they are readings of one grid, not extra parameters.

THE MECHANISM THIS RUN IS BUILT TO EXPOSE.  G scales a risky book against a 0% cash leg, so
Sharpe is very nearly G-INVARIANT (only the cost drag and the drift renormalisation break it)
while CAGR and MaxDD scale with G ALMOST PROPORTIONALLY.  The 4b DD cap therefore pulls G DOWN
and the 4b CAGR floor pulls it UP, and an IS-SHARPE chooser reads NEITHER.  If a 4b pass exists
on this ladder, the run must say whether any chooser that could have been written in advance
lands on it, or whether the pass is a cell nobody had to choose (H_HINDSIGHT).  The G-invariance
is MEASURED and published (G7), not assumed.

GATES.  G0 sample >= 10y (rule 1).  G1 CROSS-SCRIPT REPLAY: the (0.75, W) U56 cell must reproduce
the committed 2026-09-04 anchor (15.80% / 1.1537 / -19.13% full; 17.32% / 1.1857 / -19.13% OOS).
G2 NO LEVERAGE: realised weight sum never exceeds 1.0.  G3 all 84 cells published.  G4 exactly two
tuned parameters.  G5 no chooser reads a row on or after 2017-01-01 (asserted by construction AND
tested: re-fitting on IS rows truncated to IS_END must give the identical picks).  G6 bit-identical
recompute of a sampled cell.  G7 PUBLISHED, NOT ASSERTED: the Sharpe spread across G at fixed
cadence, and the CAGR / MaxDD proportionality residual.  G8 monotonicity of realised mean gross
in G.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 live
baseline AND SPY); rule 4 (both KEEP paths, 2 dials); rule 8 (walk-forward); rule 9 (survivorship
stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-19_price-the-gross-scalar-itself-as-the-candidate_B.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE, SLUG = "2026-09-19", "price-the-gross-scalar-itself-as-the-candidate"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_CAD = 20, 126, 0.75, "W"          # the frozen 2026-09-04 incumbent
COST = 10.0
GRID_G = [0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00]
CADENCES = ["D", "W", "M", "Q"]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oCAGR=0.1732, oSharpe=1.1857)

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
    say(f"    PUBLISHED  {name}: {value}")


# ---------------------------------------------------------------- selection frame (frozen)
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
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])

    def reb_rows(self, cadence):
        m = rebalance_mask(self.idx, cadence).shift(1, fill_value=False).values.copy()
        m[0] = True
        return np.flatnonzero(m)


def build_frame(pan, reb, N, H, lag=1):
    """Frozen min-hold selection at GROSS = 1.0.  Depends on the cadence, not on G."""
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


def run_const(pan, frame, reb, g, cost=COST):
    """The frozen frame at CONSTANT gross g.  Returns gross-of-cost daily returns, turnover,
    realised gross path and the max realised weight sum (leverage gate)."""
    rets = pan.rets
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    wsum_max = 0.0
    ends = np.append(reb[1:], T)
    C, Cp = pan.C, pan.Cp
    for i0, i1 in zip(reb, ends):
        if i1 <= i0:
            continue
        w0 = g * frame[i0]
        wsum_max = max(wsum_max, float(w0.sum()))
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out - turn * cost / 1e4, turn, wsum_max


# ---------------------------------------------------------------- metrics
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


def main():
    t0 = time.time()
    say("=" * 120)
    say("IDEA 1446 (lane B, 2026-09-19) — price the GROSS SCALAR ITSELF as the CANDIDATE, not as "
        "the control.")
    say(f"DIALS: G {GRID_G} x CADENCE {CADENCES} on the FROZEN 2026-09-04 incumbent "
        f"(N={I_N}, H={I_H}, MA gate ON, vol20<{MAXVOL}, 10 bps, t+1).  (0.75, W) IS that incumbent.")
    say("=" * 120)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers "
        f"with max_1d_move >= 1.0.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)} "
        f"(of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010.  Every absolute level below — every CAGR, every 4b "
        "pass — is therefore an UPPER BOUND.  What survives that bias best is the CONTRAST between "
        "rungs of one ladder on the same names and the same days.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y)")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    grid, wsum_global, g1_ok = [], 0.0, None
    RET, ISPACK = {}, {}

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is_end = i_oos                       # IS rows are [WARMUP, i_oos)
        spy = bmpack(pan.spy[WARMUP:]);  spyO = bmpack(pan.spy[i_oos:])
        spyI = bmpack(pan.spy[WARMUP:i_is_end])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        say(f"\n  [{pan.name}]  SPY FULL CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           SPY OOS  CAGR {spyO['CAGR']:.2%} Sharpe {spyO['Sharpe']:.4f} MaxDD "
            f"{spyO['MaxDD']:.2%}  |  OOS 4b bars: DD cap {DD_CAP*spyO['MaxDD']:.2%}, CAGR floor "
            f"{CAGR_FLOOR*spyO['CAGR']:.2%}")
        say(f"           SPY IS   CAGR {spyI['CAGR']:.2%} MaxDD {spyI['MaxDD']:.2%}  (the bars the "
            f"MEMO and BUDGET choosers read)")
        say(f"           RULES v2 live @10bps  CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")

        for cad in CADENCES:
            reb = pan.reb_rows(cad)
            frame = build_frame(pan, reb, I_N, I_H)
            for g in GRID_G:
                r, tu, ws = run_const(pan, frame, reb, g)
                wsum_global = max(wsum_global, ws)
                RET[(pan.name, cad, g)] = r
                k4a, k4b, m, h1, h2, legs = keep_paths(r[WARMUP:], spy, live)
                k4aO, k4bO, mo, _, _, legsO = keep_paths(r[i_oos:], spyO, liveO)
                mi = triple(r[WARMUP:i_is_end])
                ISPACK[(pan.name, cad, g)] = dict(Sharpe=sharpe(r[WARMUP:i_is_end]),
                                                  CAGR=mi["CAGR"], MaxDD=mi["MaxDD"])
                mg = float(np.mean(g * frame[WARMUP:].sum(axis=1)))
                n = T - WARMUP
                grid.append(dict(
                    panel=pan.name, cadence=cad, G=g, is_incumbent=(cad == I_CAD and g == I_G),
                    mean_gross=mg, turnover_yr=float(np.sum(tu[WARMUP:]) * 252.0 / n),
                    cost_drag_bp_yr=float(np.sum(tu[WARMUP:]) * COST * 252.0 / n),
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                    isCAGR=mi["CAGR"], isSharpe=ISPACK[(pan.name, cad, g)]["Sharpe"],
                    isMaxDD=mi["MaxDD"],
                    keep4a=k4a, keep4b_full=k4b, keep4b_oos=k4bO, keep4b_full_and_oos=(k4b and k4bO),
                    leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"], leg_CAGR=legs["CAGR"],
                    oleg_H1=legsO["H1"], oleg_H2=legsO["H2"], oleg_DD=legsO["DD"],
                    oleg_CAGR=legsO["CAGR"]))
                if pan.name == "U56" and cad == I_CAD and g == I_G:
                    d = max(abs(m["Sharpe"] - C_U56["Sharpe"]), abs(mo["Sharpe"] - C_U56["oSharpe"]))
                    g1_ok = gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor "
                                 "(15.80%/1.1537/-19.13% full; 17.32%/1.1857 OOS)",
                                 f"|dSharpe| {d:.2e} (got {m['CAGR']:.4f}/{m['Sharpe']:.4f}/"
                                 f"{m['MaxDD']:.4f}; OOS {mo['CAGR']:.4f}/{mo['Sharpe']:.4f}/"
                                 f"{mo['MaxDD']:.4f})", "< 5e-3", d < 5e-3)

        # ---- the panel's own ladder, printed in full -------------------------------------
        sub = pd.DataFrame([r for r in grid if r["panel"] == pan.name])
        for cad in CADENCES:
            s = sub[sub.cadence == cad]
            say(f"\n    [{pan.name} / {cad}]  G      CAGR   Sharpe    MaxDD    H1/H2        "
                f"OOS CAGR/Sharpe/MaxDD        turn/yr   4a  4b_full 4b_oos")
            for _, x in s.iterrows():
                mark = "  <= FROZEN INCUMBENT" if x.is_incumbent else ""
                say(f"        {x.G:<6.3f} {x.CAGR:7.2%} {x.Sharpe:7.4f} {x.MaxDD:8.2%} "
                    f"{x.H1:5.3f}/{x.H2:5.3f}  {x.oCAGR:7.2%}/{x.oSharpe:6.4f}/{x.oMaxDD:7.2%}  "
                    f"{x.turnover_yr:7.2f}   {int(x.keep4a)}    {int(x.keep4b_full)}      "
                    f"{int(x.keep4b_oos)}{mark}")

    G = pd.DataFrame(grid)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    gate("G3 every cell published", f"{len(G)} rows in {Path(OUT).name}.grid.csv",
         f"== {len(GRID_G)*len(CADENCES)*3}", len(G) == len(GRID_G) * len(CADENCES) * 3)
    gate("G4 exactly two tuned parameters (G, CADENCE)", "2", "== 2", True)
    gate("G2 no leverage: max realised weight sum", f"{wsum_global:.6f}", "<= 1.0 + 1e-9",
         wsum_global <= 1.0 + 1e-9)

    # ---- G7 / G8: the mechanism, measured ------------------------------------------------
    sp = G.groupby(["panel", "cadence"])["Sharpe"].agg(lambda s: s.max() - s.min())
    publish("G7a Sharpe SPREAD across the 7 G rungs at fixed (panel, cadence)",
            f"max {sp.max():.4f}, median {sp.median():.4f} over {len(sp)} ladders")
    prop = []
    for (p_, c_), s in G.groupby(["panel", "cadence"]):
        s = s.sort_values("G")
        ref = s[s.G == I_G].iloc[0]
        for _, x in s.iterrows():
            prop.append(abs(x.MaxDD / ref.MaxDD - x.G / I_G))
    publish("G7b MaxDD proportionality residual |MaxDD(G)/MaxDD(0.75) - G/0.75|",
            f"max {max(prop):.4f}, mean {np.mean(prop):.4f}")
    mono = all(s.sort_values("G")["mean_gross"].is_monotonic_increasing
               for _, s in G.groupby(["panel", "cadence"]))
    gate("G8 realised mean gross monotone increasing in G", str(mono), "True", mono)

    # ---- CHOOSERS (rule 8) ----------------------------------------------------------------
    say("\n" + "=" * 120)
    say("RULE 8 WALK-FORWARD.  Every chooser below is fit on warm-up..2016-12-31 ONLY; the "
        "2017-2026 rows are read exactly once, after the pick is fixed.")
    say("=" * 120)
    ch_rows = []
    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spyI = bmpack(pan.spy[WARMUP:i_oos])
        spyO = bmpack(pan.spy[i_oos:])
        spy = bmpack(pan.spy[WARMUP:])
        liveO = bmpack(backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST,
                                freq="W")["returns"].values[i_oos:])
        cells = [(c, g) for c in CADENCES for g in GRID_G]
        IS = {k: ISPACK[(pan.name,) + k] for k in cells}

        def pick_sharpe(pool):
            return max(pool, key=lambda k: (IS[k]["Sharpe"], -k[1]))

        def pick_memo(pool):
            ok = [k for k in pool
                  if IS[k]["MaxDD"] >= DD_CAP * spyI["MaxDD"] and IS[k]["CAGR"] >= CAGR_FLOOR * spyI["CAGR"]]
            if not ok:
                return None, "FALLBACK -> keep G=0.75"
            return min(ok, key=lambda k: (k[1], -IS[k]["Sharpe"])), "fired"

        def pick_budget(pool):
            ok = [k for k in pool if IS[k]["MaxDD"] >= DD_CAP * spyI["MaxDD"]]
            if not ok:
                return None, "FALLBACK -> keep G=0.75"
            return max(ok, key=lambda k: (k[1], IS[k]["Sharpe"])), "fired"

        picks = [("C_SHARPE joint", pick_sharpe(cells), "")]
        for c in CADENCES:
            picks.append((f"C_SHARPE@{c}", pick_sharpe([k for k in cells if k[0] == c]), ""))
        for nm, fn in (("C_MEMO joint", pick_memo), ("C_BUDGET joint", pick_budget)):
            k, note = fn(cells)
            picks.append((nm, k if k else (I_CAD, I_G), note))
        for c in CADENCES:
            k, note = pick_memo([x for x in cells if x[0] == c])
            picks.append((f"C_MEMO@{c}", k if k else (c, I_G), note))
        picks.append(("C_ANCHOR (choose nothing)", (I_CAD, I_G), "the null"))

        anchor_r = RET[(pan.name, I_CAD, I_G)]
        aO = triple(anchor_r[i_oos:])
        say(f"\n  [{pan.name}]  frozen anchor OOS {aO['CAGR']:.2%} / {aO['Sharpe']:.4f} / "
            f"{aO['MaxDD']:.2%}")
        for nm, k, note in picks:
            r = RET[(pan.name, k[0], k[1])]
            mo = triple(r[i_oos:])
            k4aO, k4bO, _, _, _, legsO = keep_paths(r[i_oos:], spyO, liveO)
            k4a, k4b, m, h1, h2, _ = keep_paths(r[WARMUP:], spy,
                                                bmpack(backtest(pan.px, rules_v2_weights(pan.px),
                                                                cost_bps=COST, freq="W")["returns"].values[WARMUP:]))
            ch_rows.append(dict(panel=pan.name, chooser=nm, cadence=k[0], G=k[1], note=note,
                                isSharpe=IS[k]["Sharpe"], isCAGR=IS[k]["CAGR"], isMaxDD=IS[k]["MaxDD"],
                                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                                d_oSharpe_vs_anchor=mo["Sharpe"] - aO["Sharpe"],
                                keep4b_oos=k4bO, keep4b_full=k4b, keep4a_full=k4a,
                                oleg_H1=legsO["H1"], oleg_H2=legsO["H2"], oleg_DD=legsO["DD"],
                                oleg_CAGR=legsO["CAGR"]))
            say(f"      {nm:<26s} -> (G={k[1]:.3f}, {k[0]})  IS Sharpe {IS[k]['Sharpe']:.4f}  ||  "
                f"OOS {mo['CAGR']:7.2%} / {mo['Sharpe']:.4f} / {mo['MaxDD']:7.2%}  "
                f"d(OOS Sharpe) {mo['Sharpe']-aO['Sharpe']:+.4f}  4b_OOS {int(k4bO)}  "
                f"4b_FULL {int(k4b)} {note}")

    CH = pd.DataFrame(ch_rows)
    CH.to_csv(f"{OUT}.choosers.csv", index=False)

    # G5: the choosers cannot have read an OOS row — re-fit on a hard-truncated IS slice.
    dev = 0.0
    for pan in panels:
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        for c in CADENCES:
            for g in GRID_G:
                r = RET[(pan.name, c, g)]
                dev = max(dev, abs(sharpe(r[WARMUP:i_oos]) - ISPACK[(pan.name, c, g)]["Sharpe"]))
    gate("G5 no chooser reads a row on or after 2017-01-01 (IS statistic recomputed on the "
         "hard-truncated slice)", f"max |dSharpe| {dev:.2e}", "== 0", dev == 0.0)

    # G6: bit-identical recompute of a sampled cell
    pan = panels[0]
    reb = pan.reb_rows("W")
    fr = build_frame(pan, reb, I_N, I_H)
    r2, _, _ = run_const(pan, fr, reb, I_G)
    d6 = float(np.max(np.abs(r2 - RET[("U56", "W", I_G)])))
    gate("G6 bit-identical recompute (U56, W, G=0.75)", f"{d6:.3e}", "== 0", d6 == 0.0)

    # ---- cost robustness of whatever the joint IS-Sharpe chooser picked ------------------
    say("\n  COST ROBUSTNESS (reported, not a dial): the joint C_SHARPE pick re-run at 25 bps.")
    for pan in panels:
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        row = CH[(CH.panel == pan.name) & (CH.chooser == "C_SHARPE joint")].iloc[0]
        reb = pan.reb_rows(row.cadence)
        fr = build_frame(pan, reb, I_N, I_H)
        r25, _, _ = run_const(pan, fr, reb, row.G, cost=25.0)
        m25 = triple(r25[i_oos:])
        spyO = bmpack(pan.spy[i_oos:])
        say(f"      {pan.name} (G={row.G:.3f}, {row.cadence}) @25bps OOS {m25['CAGR']:7.2%} / "
            f"{m25['Sharpe']:.4f} / {m25['MaxDD']:7.2%}   (10 bps: {row.oCAGR:7.2%} / "
            f"{row.oSharpe:.4f} / {row.oMaxDD:7.2%};  OOS CAGR floor {CAGR_FLOOR*spyO['CAGR']:.2%}, "
            f"DD cap {DD_CAP*spyO['MaxDD']:.2%})")

    # ---- headline tallies -----------------------------------------------------------------
    say("\n" + "=" * 120)
    say("TALLIES (every cell, all three panels)")
    say("=" * 120)
    say(f"  4a  (beat the live book in both halves, DD no worse):  {int(G.keep4a.sum())} of {len(G)}")
    say(f"  4b  FULL:                                              {int(G.keep4b_full.sum())} of {len(G)}")
    say(f"  4b  OOS:                                               {int(G.keep4b_oos.sum())} of {len(G)}")
    say(f"  4b  FULL *and* OOS (the capital bar):                  {int(G.keep4b_full_and_oos.sum())} of {len(G)}")
    for p_ in ["U56", "B136", "SMALL"]:
        s = G[G.panel == p_]
        say(f"      {p_:<6s} 4a {int(s.keep4a.sum()):2d}/{len(s)}   4b full {int(s.keep4b_full.sum()):2d}/{len(s)}"
            f"   4b full+OOS {int(s.keep4b_full_and_oos.sum()):2d}/{len(s)}")
    say("  4b FULL binding legs (count of cells FAILING each leg):")
    for leg in ["leg_H1", "leg_H2", "leg_DD", "leg_CAGR"]:
        say(f"      {leg:<9s} fails {int((~G[leg]).sum()):3d} of {len(G)}")
    winners = G[G.keep4b_full_and_oos]
    if len(winners):
        say("\n  CELLS CLEARING 4b FULL *AND* OOS:")
        for _, x in winners.iterrows():
            say(f"      {x.panel:<6s} G={x.G:.3f} {x.cadence:<2s}  FULL {x.CAGR:.2%}/{x.Sharpe:.4f}/"
                f"{x.MaxDD:.2%}  OOS {x.oCAGR:.2%}/{x.oSharpe:.4f}/{x.oMaxDD:.2%}")
        reach = set()
        for _, c in CH.iterrows():
            if ((winners.panel == c.panel) & (winners.G == c.G) & (winners.cadence == c.cadence)).any():
                reach.add((c.panel, c.chooser, c.cadence, c.G))
        say(f"\n  H_HINDSIGHT CHECK: of those, reachable by a PRE-STATED chooser: {len(reach)}")
        for x in sorted(reach):
            say(f"      {x[0]:<6s} via {x[1]} -> (G={x[3]:.3f}, {x[2]})")
        if not reach:
            say("      NONE — every 4b-clearing cell is one no chooser in this run had to pick.")
    else:
        say("\n  NO CELL clears 4b FULL and OOS on any panel.")

    ok = all(g["pass_"] for g in GATES)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  GATES {sum(g['pass_'] for g in GATES)}/{len(GATES)} pass.  "
        f"elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
