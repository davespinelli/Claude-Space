#!/usr/bin/env python3
"""Idea 319 - "is-the-narrow-day-effect-ORDERING-the-same-panel-ordering-as-the-gate-premium"
(lane B, 2026-09-09).

THE QUESTION
------------
Idea 316 measured the NARROW-DAY CONCENTRATION effect at +5.17 / -1.46 / -3.06 pp/yr on
U56 / B136 / SMALL439.  Ideas 51 and 312 measured the 200d-MA GATE premium as
-0.0045 / -0.0465 / -0.1023 Sharpe on the SAME three panels.  Both ladders are monotone in
the same panel order, on two completely different instruments.  The queue asks: does ONE
panel characteristic (ETF share, dispersion, cap mix) price BOTH orderings, or is the
agreement the coincidence of two three-point ladders?

Three panels cannot answer that: with n = 3 any two monotone ladders agree with probability
1/3 by chance alone, and idea 312 already showed the gate ladder's own within-rung seed sd is
0.76x the whole published gap.  So this run replaces the three points with a POPULATION of
sub-panels and measures BOTH statistics on EVERY one of them.

WHAT IS MEASURED (both at the SAME pinned dials, so the two ladders are commensurable)
--------------------------------------------------------------------------------------
On each sub-panel, weekly, 10 bps, t+1, gross 0.75:

  GATE   = Sharpe(MA-RS) - Sharpe(EWall)                        [idea 51 / 312's instrument]
             EWall  : gross spread equally over every priced tradable name
             MA-RS  : gross spread equally over names above their own 200d MA (RESPREAD)
           Gross is identical in both arms, so the premium is pure selection.

  CONC   = 252 * mean( r(CONC) - r(NF20) | narrow state ) * 100   [idea 316's instrument]
             NF20 : k = min(20, E_t) equal-weight of the top-k by idea 2's scorer
             CONC : narrow -> k = max(1, round(0.35 * k_broad)); broad -> k_broad
             narrow_t = E_t <= causal expanding 0.20-quantile of E (min 252 obs), shifted
           Gross is 0.75 in BOTH regimes, so the effect is concentration and nothing else.

Everything about these two definitions is inherited verbatim from ideas 312 and 316; nothing
in either instrument is re-tuned here.

PRE-REGISTERED, NOT SEARCHED (all from ideas 312/316): n0 = 20, gross = 0.75, weekly cadence,
10 bps, t+1, MA window 200, vol20 < 0.60 eligibility, scorer WITHOUT /sqrt(vol20), q = 0.20,
c = 0.35, quantile min_obs = 252, IS = ..2016-12-31, OOS = 2017-01-01.., eval from bar 260.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two)
  1. k    - the sub-panel draw size, in {20, 36, 50}.
  2. x    - the characteristic used to price the two ladders, in {etf_share, breadth, cvol,
            mean_vol, rho_bar, small_share}.
ALL 3 x 6 = 18 (k, x) cells are reported, for BOTH statistics, on all four origins.

ORIGINS (structural, not tuned): draws are taken from U56, B136, SMALL484 and POOL
(B136 + SMALL, the only construction idea 568 found that gives overlapping characteristic
support).  12 seeds per (k, origin).  144 sub-panels + the 3 real anchors.

PRE-REGISTERED HYPOTHESES
  H_COINC (the queue's null) : over the draw population |rho(GATE, CONC)| < 0.30 under BOTH
        Pearson and Spearman (idea 564: name the statistic).  -> two independent ladders,
        the three-panel agreement is coincidence.
  H_ONECHAR : there EXISTS a characteristic x with R2(GATE ~ x) >= 0.50 AND R2(CONC ~ x)
        >= 0.50 on the same draw population, with slopes whose signs predict the published
        three-panel ordering on BOTH statistics.  -> one characteristic prices both.
  H_NOISE : the within-(k, origin) seed sd of each statistic, against its own published
        three-panel gap (GATE 0.0978 Sharpe; CONC 8.229 pp/yr).  sd >= 0.5 x gap means that
        ladder cannot separate a panel property from composition luck at n = 3.

GATES, RUN FIRST (a failed gate aborts the run)
  G1 : the vectorised runner reproduces engine.backtest on a CONC book (returns AND
       turnover) at < 1e-9.
  G2 : idea 316's three committed ann_eff_on_narrow_pp panel means (+5.174 / -1.464 / -3.055)
       reproduce on their NATIVE windows and conventions.
  G3 : idea 312's three committed (g=0.75, W) gate premia (-0.03309 / -0.06533 / -0.17475)
       reproduce on their NATIVE windows and conventions.
  G2/G3 tolerance 5e-3 absolute: data/prices.csv gained 4 bars since those runs (idea 312
  documented the same revision at <= 5.09e-05 relative); the anchors are re-read on idea
  51's last bar 2026-09-04 to remove it, so the residual should be ~0.

HONESTY NOTES
  * The draw population is evaluated on the COMMON window 2010-01-04 .. 2026-09-04 (4,194
    bars, 16.6 yr), the intersection of prices_broad.csv and prices_small.csv.gz, so that
    the two statistics are never compared across different samples.  The GATE reproductions
    (G2/G3) are run on each panel's NATIVE window, which is why they are separate.
  * SURVIVORSHIP: universe.json (56) and universe_broad.json (136) are current-constituent
    lists; SMALL484 is the current constituents of a sub-$2B screen (data/SMALL_PANEL_README)
    with the README's max_1d_move >= 1.0 names dropped.  Absolute CAGRs are optimistic on
    every panel and most on SMALL; the two CONTRASTS (GATE, CONC) are the durable part, and
    small_share is reported as a characteristic precisely because idea 568 showed origin
    survives characteristic matching.
  * SPY is a BENCHMARK column only here (never drawn into a sub-panel, never tradable), a
    deliberate deviation from idea 316's U56/B136 convention so that the draws from the four
    origins are constructed identically.  The G2/G3 gates use the original convention.
  * 2022 dominates U56's narrow state (idea 316).  The population result is the evidence;
    the three-panel anchors are description.

Deterministic, standalone.  Reads baseline.py / engine.py; modifies nothing.
"""
import json
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STAMP = Path(__file__).name
OUT = Path(__file__).with_suffix("")

# ---- pinned dials, inherited from ideas 312/316, none re-tuned here -------------------
COST = 10.0
FREQ = "W"
GROSS = 0.75
MA_WIN = 200
MAX_VOL = 0.60
N0 = 20
Q_NAR = 0.20
C_CONC = 0.35
MIN_OBS = 252
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260

# ---- the two tuned parameters ---------------------------------------------------------
KS = [20, 36, 50]
CHARS = ["etf_share", "breadth", "cvol", "mean_vol", "rho_bar", "small_share"]
SEEDS = list(range(12))
ORIGINS = ["U56", "B136", "SMALL", "POOL"]

# ---- published anchors ----------------------------------------------------------------
# idea 316's committed .effects.csv AT THE PINNED POINT (q=0.20, c=0.35) - the exact book
# this run generalises.  The queue's headline +5.174 / -1.464 / -3.055 is the MEAN of the
# same table over all 16 (q, c) points; the ORDERING U56 > B136 > SMALL439 is identical at
# both readings, which is what the queue's claim is about.
ANCHOR_CONC = {"U56": 6.486998, "B136": -0.162010, "SMALL439": -3.847079}   # idea 316 point
ANCHOR_CONC_MEAN = {"U56": 5.173935, "B136": -1.463992, "SMALL439": -3.055172}  # 16-pt mean
ANCHOR_GATE = {"U56": -0.033090, "B136": -0.065328, "SMALL439": -0.174748}  # idea 312 (0.75,W)
GAP_GATE = 0.097781      # idea 51/312 published U56 - SMALL439 premium gap (6-point mean)
GAP_CONC = 10.334077     # idea 316 U56 - SMALL439 conc gap AT THE PINNED POINT
GAP_CONC_MEAN = 8.229107  # ... and at the 16-point mean the queue quotes
PARENT_END = "2026-09-04"
G1_TOL = 1e-9
G23_TOL = 5e-3
R2_BAR = 0.50
RHO_BAR = 0.30

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ------------------------------------------------------------------ vectorised runner
def fast_backtest(prices, weights, cost_bps=COST, freq=FREQ):
    """Vectorised equivalent of engine.backtest (asserted in G1)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


# ------------------------------------------------------------------ column-wise primitives
def col_primitives(px):
    """Everything in the two instruments that is COLUMN-WISE (no cross-section), computed
    once on the parent frame and sliced per draw.  score()'s ranks are the only
    cross-sectional part and are recomputed inside each draw."""
    ma = px.rolling(MA_WIN).mean()
    above = px > ma
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return dict(above=above, vol20=vol20, mom=mom, r6=r6, r3=r3, ma_ok=ma.notna())


def _ew(mask, g=GROSS):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.div(n, axis=0).fillna(0.0)


def _weights_from_k(rank, k, g=GROSS):
    k = k.clip(lower=1.0)
    sel = rank.le(k, axis=0)
    return sel.astype(float).mul(g / k, axis=0)


def build_books(px, cols, prim, vol_scale=False, rank_cols=None):
    """The four books of this run on one (sub-)panel.  px may carry extra columns (SPY);
    only `cols` is tradable.

    rank_cols is the column set the composite's pct-ranks are normalised over.  It matters:
    baseline.score() ranks across the WHOLE frame it is handed and idea 316 then subset the
    result, so on SMALL439 the benchmark column SPY sat inside the rank denominator even
    though it was never tradable.  The reproduction gate G2 passes rank_cols = the panel's
    full column list to match that exactly; the draw population passes rank_cols = cols
    (SPY is never drawn into a sub-panel), which is the cleaner convention and is used for
    every number this run reports as its own.
    """
    rc = list(cols) if rank_cols is None else list(rank_cols)
    sub = px[cols]
    priced = sub.notna()
    above = prim["above"][cols] & priced
    # --- gate arms (idea 312) -----------------------------------------------------------
    w_ew = _ew(priced, GROSS)
    w_ma = _ew(above, GROSS)
    # --- conc arms (idea 316) -----------------------------------------------------------
    comp = ((prim["mom"][rc].rank(axis=1, pct=True)
             + prim["r6"][rc].rank(axis=1, pct=True)
             + prim["r3"][rc].rank(axis=1, pct=True)) / 3.0)[cols]
    s = comp * (0.5 + 0.5 * prim["above"][cols].astype(float))
    if vol_scale:
        s = s / prim["vol20"][cols].clip(lower=0.08) ** 0.5
    elig = prim["above"][cols] & (prim["vol20"][cols] < MAX_VOL)
    e = elig.sum(axis=1).astype(float).where(prim["ma_ok"][cols].any(axis=1))
    rank = s.where(elig).rank(axis=1, ascending=False)
    thr = e.expanding(min_periods=MIN_OBS).quantile(Q_NAR).shift(1)
    nar = (e <= thr).where(thr.notna() & e.notna(), False)
    k_broad = np.minimum(float(N0), e)
    k_conc = k_broad.where(~nar, np.maximum(1.0, np.round(C_CONC * k_broad)))
    w_nf = _weights_from_k(rank, k_broad)
    w_cc = _weights_from_k(rank, k_conc)
    return {"EWall": w_ew, "MA-RS": w_ma, "NF20": w_nf, "CONC": w_cc}, nar


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def fail_4b(r, spy):
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not a1 > s1:
        f.append("H1")
    if not a2 > s2:
        f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]:
        f.append("OOS")
    if not m["MaxDD"] >= 0.60 * ms["MaxDD"]:
        f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]:
        f.append("CAGR")
    return ",".join(f) if f else "-"


# ------------------------------------------------------------------ panels
def load_parents():
    px56 = load_universe().dropna(how="all").ffill()
    px136 = load_universe(broad=True).dropna(how="all").ffill()
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    pxs = pxs[s_stk + ["SPY"]].dropna(how="all").ffill()
    return px56, px136, pxs, s_stk


def etf_names(px136):
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    tick = set(U["broad"]) | set(U["sectors"]) | set(U["bonds_fx_commod"])
    return {t for t in tick if t not in crypto and t in px136.columns}


def characteristics(px, cols, etfs, small_set):
    """Descriptive characteristics of a (sub-)panel over the whole evaluated window."""
    sub = px[cols]
    rets = sub.pct_change()
    cvol = float(rets.std(axis=1).mean() * np.sqrt(252))          # cross-sectional dispersion
    mean_vol = float((rets.std() * np.sqrt(252)).mean())          # average name vol
    ma = sub.rolling(MA_WIN).mean()
    breadth = float((sub > ma).mean(axis=1).mean())
    mr = rets.mean(axis=1)
    v_port = float(mr.var())
    v_bar = float(rets.var().mean())
    n = len(cols)
    rho_bar = float((n * v_port / v_bar - 1.0) / (n - 1.0)) if n > 1 and v_bar > 0 else np.nan
    return dict(etf_share=len([c for c in cols if c in etfs]) / n,
                small_share=len([c for c in cols if c in small_set]) / n,
                breadth=breadth, cvol=cvol, mean_vol=mean_vol, rho_bar=rho_bar)


# ------------------------------------------------------------------ gates
def gate_G1(px, cols, prim):
    books, _ = build_books(px, cols, prim)
    w = books["CONC"]
    a = backtest(px[cols], w, cost_bps=COST, freq=FREQ)
    b = fast_backtest(px[cols], w)
    # engine.backtest emits NaN on bars where a constituent has no price yet (the panel's
    # ragged left edge).  Those bars are inside the 260-bar warm-up every book discards; the
    # comparison is made on the finite bars and the excluded count is reported.
    fr = a["returns"].notna()
    ft = a["turnover"].notna()
    dr = float(np.max(np.abs(a["returns"][fr].values - b["returns"][fr].values)))
    dt = float(np.max(np.abs(a["turnover"][ft].values - b["turnover"][ft].values)))
    nex = int((~fr).sum()), int((~ft).sum())
    P(f"  G1 runner vs engine.backtest on a CONC book ({len(px)} bars, {nex[0]}/{nex[1]} "
      f"ragged-edge NaN bars excluded, all before {a['returns'][fr].index[0].date()} + warm-up):")
    P(f"     max|dret| {dr:.3e}   max|dturn| {dt:.3e}   (bar {G1_TOL:.0e})")
    ok = dr < G1_TOL and dt < G1_TOL
    P(f"  G1 {'PASS' if ok else 'FAIL'}")
    return ok, dr, dt


def native_stats(name, px, cols, spy_tradable):
    """Idea 316's CONC effect and idea 312's GATE premium on a panel's NATIVE window,
    under those runs' OWN conventions (SPY tradable on U56/B136), truncated to idea 51's
    last bar so the reproduction is read on their sample."""
    frame = px.loc[:PARENT_END]
    tradable = list(cols) + (["SPY"] if spy_tradable and "SPY" in frame.columns
                             and "SPY" not in cols else [])
    prim = col_primitives(frame)
    # idea 316's rank denominator: the whole frame it handed to score(), SPY included.
    books, nar = build_books(frame, tradable, prim, rank_cols=list(frame.columns))
    start = frame.index[WARMUP]
    reb = rebalance_mask(frame.index, FREQ)
    r = {k: fast_backtest(frame[tradable], v)["returns"].loc[start:] for k, v in books.items()}
    state = (nar.reindex(frame.index).fillna(False).astype(bool)
             .where(reb).ffill().shift(1).fillna(False).astype(bool).loc[start:])
    d = r["CONC"] - r["NF20"]
    conc = float(252 * d[state].mean() * 100) if state.any() else np.nan
    gate = float(metrics(r["MA-RS"])["Sharpe"] - metrics(r["EWall"])["Sharpe"])
    return conc, gate, int(state.sum()), len(frame)


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    P("=" * 140)
    P(f"IDEA 319  is-the-narrow-day-effect-ORDERING-the-same-panel-ordering-as-the-gate-premium"
      f"   (lane B, 2026-09-09) | {STAMP}")
    P("=" * 140)
    P(f"Pinned (ideas 312/316, none re-tuned): n0={N0}, gross={GROSS:.2f}, {FREQ}, {COST:.0f} bps, "
      f"t+1, MA{MA_WIN}, vol20<{MAX_VOL}, scorer OFF, q={Q_NAR}, c={C_CONC}, min_obs={MIN_OBS}.")
    P(f"Tuned (2): k in {KS} x characteristic in {CHARS}  ->  {len(KS)*len(CHARS)} cells, ALL reported.")
    P(f"Origins (structural): {ORIGINS} x {len(SEEDS)} seeds.")
    P("")

    px56, px136, pxs, s_stk = load_parents()
    etfs = etf_names(px136)
    small_set = set(s_stk)
    P(f"Parents: U56 {px56.shape}, B136 {px136.shape}, SMALL{len(s_stk)} {pxs.shape}; "
      f"{len(etfs)} ETFs in B136.")

    # ---------------------------------------------------------------- GATES
    P("")
    P("-" * 140)
    P("GATES (run first; a failure aborts)")
    P("-" * 140)
    prim56 = col_primitives(px56)
    ok1, g1r, g1t = gate_G1(px56, [c for c in px56.columns], prim56)
    if not ok1:
        P("!! G1 FAILED - aborting."); sys.exit(1)

    rep = []
    for nm, frame, cols, spy_t in [("U56", px56, [c for c in px56.columns if c != "SPY"], True),
                                   ("B136", px136, [c for c in px136.columns if c != "SPY"], True),
                                   (f"SMALL{len(s_stk)}", pxs, s_stk, False)]:
        c_, g_, nd, nb = native_stats(nm, frame, cols, spy_t)
        key = nm if nm in ANCHOR_CONC else "SMALL439"
        rep.append(dict(panel=nm, bars=nb, narrow_days=nd,
                        conc=c_, conc_pub=ANCHOR_CONC[key], d_conc=c_ - ANCHOR_CONC[key],
                        conc_pub_16ptmean=ANCHOR_CONC_MEAN[key],
                        gate=g_, gate_pub=ANCHOR_GATE[key], d_gate=g_ - ANCHOR_GATE[key]))
    REP = pd.DataFrame(rep)
    P("")
    P("  G2/G3 reproduction on NATIVE windows (truncated to idea 51's last bar "
      f"{PARENT_END}); CONC in pp/yr, GATE in Sharpe:")
    P("  " + fmt(REP.set_index("panel"), 4).replace("\n", "\n  "))
    g2 = float(REP.d_conc.abs().max())
    g3 = float(REP.d_gate.abs().max())
    P(f"  G2 (idea 316 CONC anchors) max|delta| {g2:.3e}  -> {'PASS' if g2 < G23_TOL else 'FAIL'}"
      f"   (bar {G23_TOL:.0e})")
    P(f"  G3 (idea 312 GATE anchors) max|delta| {g3:.3e}  -> {'PASS' if g3 < G23_TOL else 'FAIL'}"
      f"   (bar {G23_TOL:.0e})")
    REP.to_csv(f"{OUT}.gates.csv", index=False)
    if g2 >= G23_TOL or g3 >= G23_TOL:
        P("!! A REPRODUCTION GATE FAILED - the two published ladders are not the objects this")
        P("   run is generalising.  Aborting per PROTOCOL rule 7.")
        sys.exit(1)
    P(f"  Published U56 - SMALL439 gaps: GATE {GAP_GATE:+.4f} Sharpe (6-point mean), "
      f"CONC {GAP_CONC:+.4f} pp/yr at the pinned point "
      f"({GAP_CONC_MEAN:+.4f} at the 16-point mean the queue quotes).")
    P("  Both ladders read U56 > B136 > SMALL439 at the pinned point, so the queue's ordering")
    P("  claim is intact at the exact books this run generalises.")

    # ---------------------------------------------------------------- common frame
    P("")
    P("-" * 140)
    P("COMMON WINDOW (the population is built here so the two statistics share one sample)")
    P("-" * 140)
    idx = px136.index.intersection(pxs.index)
    b_names = [c for c in px136.columns if c != "SPY"]
    u_names = [c for c in px56.columns if c != "SPY"]
    PX = pd.concat([px136[b_names].reindex(idx), pxs[s_stk].reindex(idx),
                    px136["SPY"].reindex(idx).rename("SPY")], axis=1).ffill()
    P(f"  {PX.shape[0]} bars {idx[0].date()} -> {idx[-1].date()} "
      f"({PX.shape[0]/252:.1f} yr) | {len(b_names)} B-names + {len(s_stk)} S-names + SPY(bench)")
    yrs = PX.index.to_series().groupby(PX.index.year).count()
    if yrs.loc[2015:2024].max() > 300:
        P("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)
    P(f"  index sanity: 2018={yrs.get(2018)}, 2024={yrs.get(2024)} trading days")
    PRIM = col_primitives(PX)
    START = PX.index[WARMUP]
    REB = rebalance_mask(PX.index, FREQ)
    spy = PX["SPY"].pct_change().fillna(0.0).loc[START:]
    base_v2 = fast_backtest(px56.reindex(idx).ffill(),
                            rules_v2_weights(px56.reindex(idx).ffill()))["returns"].loc[START:]
    mb, ms = metrics(base_v2), metrics(spy)
    P(f"  4a comparand = LIVE RULES v2 on U56 over this window: CAGR {mb['CAGR']:.2%} "
      f"Sharpe {mb['Sharpe']:.3f} MaxDD {mb['MaxDD']:.1%} halves "
      f"{halves(base_v2)[0]:.3f}/{halves(base_v2)[1]:.3f}")
    P(f"  4b comparand = SPY:                                   CAGR {ms['CAGR']:.2%} "
      f"Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.1%} halves "
      f"{halves(spy)[0]:.3f}/{halves(spy)[1]:.3f}")

    pools = {"U56": u_names, "B136": b_names, "SMALL": s_stk, "POOL": b_names + s_stk}

    # ---------------------------------------------------------------- the population
    P("")
    P("-" * 140)
    P("POPULATION: both statistics on every sub-panel (all grid points written to .panels.csv)")
    P("-" * 140)
    rows, books_rows = [], []

    def run_panel(label, origin, k, seed, cols):
        books, nar = build_books(PX, cols, PRIM)
        r = {kk: fast_backtest(PX[cols], vv)["returns"].loc[START:] for kk, vv in books.items()}
        state = (nar.reindex(PX.index).fillna(False).astype(bool)
                 .where(REB).ffill().shift(1).fillna(False).astype(bool).loc[START:])
        d = r["CONC"] - r["NF20"]
        yrs_ = len(d) / 252.0
        def _conc(sl_d, sl_s):
            return float(252 * sl_d[sl_s].mean() * 100) if sl_s.any() else np.nan
        # standard error of the CONC statistic itself: it is a MEAN over narrow days, and
        # its own sampling error decides whether a single panel's number is readable at all.
        dn = d[state].dropna()
        conc_se = float(252 * dn.std(ddof=1) / np.sqrt(len(dn)) * 100) if len(dn) > 2 else np.nan
        gate = float(metrics(r["MA-RS"])["Sharpe"] - metrics(r["EWall"])["Sharpe"])
        gi = float(metrics(r["MA-RS"].loc[:IS_END])["Sharpe"]
                   - metrics(r["EWall"].loc[:IS_END])["Sharpe"])
        go = float(metrics(r["MA-RS"].loc[OOS_START:])["Sharpe"]
                   - metrics(r["EWall"].loc[OOS_START:])["Sharpe"])
        ch = characteristics(PX, cols, etfs, small_set)
        row = dict(label=label, origin=origin, k=k, seed=seed,
                   gate=gate, gate_IS=gi, gate_OOS=go,
                   conc=_conc(d, state),
                   conc_IS=_conc(d.loc[:IS_END], state.loc[:IS_END]),
                   conc_OOS=_conc(d.loc[OOS_START:], state.loc[OOS_START:]),
                   conc_book_pp=float(d.sum() / yrs_ * 100),
                   conc_dSharpe=float(metrics(r["CONC"])["Sharpe"] - metrics(r["NF20"])["Sharpe"]),
                   conc_se=conc_se,
                   conc_t=(float(_conc(d, state) / conc_se)
                           if np.isfinite(conc_se) and conc_se > 0 else np.nan),
                   narrow_days=int(state.sum()), **ch)
        rows.append(row)
        for arm, rr in r.items():
            m = metrics(rr)
            h1, h2 = halves(rr)
            mo = metrics(rr.loc[OOS_START:])
            books_rows.append(dict(label=label, origin=origin, k=k, seed=seed, arm=arm,
                                   CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                   H1=h1, H2=h2,
                                   IS_Sharpe=metrics(rr.loc[:IS_END])["Sharpe"],
                                   OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                   OOS_MaxDD=mo["MaxDD"],
                                   keep4a=keep_4a(rr, base_v2), fail4b=fail_4b(rr, spy),
                                   keep4b=fail_4b(rr, spy) == "-"))
        return row

    # the three real anchors, on the COMMON window and the common convention
    for nm, cols in [("REAL:U56", u_names), ("REAL:B136", b_names),
                     (f"REAL:SMALL{len(s_stk)}", s_stk)]:
        rr = run_panel(nm, "REAL", len(cols), -1, cols)
        P(f"  {nm:<16} k={len(cols):<4} GATE {rr['gate']:+.4f}  CONC {rr['conc']:+7.3f} "
          f"+/- {rr['conc_se']:.3f} pp/yr (t {rr['conc_t']:+.2f})  narrow {rr['narrow_days']:>4}d  "
          f"etf {rr['etf_share']:.3f} breadth {rr['breadth']:.3f} cvol {rr['cvol']:.3f}")

    n_done = 0
    for k in KS:
        for origin in ORIGINS:
            pool = np.array(pools[origin])
            if k > len(pool):
                continue
            for sd in SEEDS:
                seed = zlib.crc32(f"I319|{origin}|{k}|{sd}".encode()) % (2 ** 32)
                rng = np.random.default_rng(seed)
                cols = sorted(rng.choice(pool, size=k, replace=False).tolist())
                run_panel(f"{origin}/k{k}/s{sd}", origin, k, sd, cols)
                n_done += 1
    D = pd.DataFrame(rows)
    B = pd.DataFrame(books_rows)
    D.to_csv(f"{OUT}.panels.csv", index=False)
    B.to_csv(f"{OUT}.books.csv", index=False)
    P(f"  {n_done} sub-panels + 3 real anchors = {len(D)} panels, {len(B)} books "
      f"[{time.time()-t0:.0f}s]")
    DR = D[D.origin != "REAL"].copy()

    P("")
    P("  Cell means (all 12 grid cells reported; GATE Sharpe, CONC pp/yr):")
    cell = DR.groupby(["k", "origin"]).agg(
        n=("gate", "size"), gate=("gate", "mean"), gate_sd=("gate", "std"),
        conc=("conc", "mean"), conc_sd=("conc", "std"),
        etf=("etf_share", "mean"), breadth=("breadth", "mean"), cvol=("cvol", "mean"),
        smallsh=("small_share", "mean")).reset_index()
    P("  " + fmt(cell.set_index(["k", "origin"])).replace("\n", "\n  "))

    # ---------------------------------------------------------------- H_COINC
    P("")
    P("-" * 140)
    P("H_COINC - do the two ladders MOVE TOGETHER across the population?")
    P("-" * 140)

    def rho_pair(a, b):
        m = np.isfinite(a) & np.isfinite(b)
        a, b = np.asarray(a)[m], np.asarray(b)[m]
        if len(a) < 3:
            return np.nan, np.nan, 0
        pear = float(np.corrcoef(a, b)[0, 1])
        sp = float(np.corrcoef(pd.Series(a).rank(), pd.Series(b).rank())[0, 1])
        return pear, sp, int(len(a))

    cor_rows = []
    pe, sp, n = rho_pair(DR.gate.values, DR.conc.values)
    cor_rows.append(dict(scope="ALL DRAWS", n=n, pearson=pe, spearman=sp))
    for org in ORIGINS:
        s = DR[DR.origin == org]
        pe_, sp_, n_ = rho_pair(s.gate.values, s.conc.values)
        cor_rows.append(dict(scope=f"origin={org}", n=n_, pearson=pe_, spearman=sp_))
    for k in KS:
        s = DR[DR.k == k]
        pe_, sp_, n_ = rho_pair(s.gate.values, s.conc.values)
        cor_rows.append(dict(scope=f"k={k}", n=n_, pearson=pe_, spearman=sp_))
    for k in KS:
        for org in ORIGINS:
            s = DR[(DR.k == k) & (DR.origin == org)]
            if len(s) >= 3:
                pe_, sp_, n_ = rho_pair(s.gate.values, s.conc.values)
                cor_rows.append(dict(scope=f"k={k},{org}", n=n_, pearson=pe_, spearman=sp_))
    COR = pd.DataFrame(cor_rows)
    COR.to_csv(f"{OUT}.corr.csv", index=False)
    P("  rho(GATE, CONC) - Pearson AND Spearman, with n beside each (idea 564):")
    P("  " + fmt(COR.set_index("scope")).replace("\n", "\n  "))
    coinc = bool(abs(pe) < RHO_BAR and abs(sp) < RHO_BAR)
    P(f"  H_COINC bar |rho| < {RHO_BAR}: pooled Pearson {pe:+.4f}, Spearman {sp:+.4f} "
      f"-> H_COINC {'HOLDS (two independent ladders)' if coinc else 'FAILS (they co-move)'}")
    P("  NOTE: origin is a confound inside the pooled rho - the within-origin rows above are")
    P("  the confound-free reading.")
    wi = COR[COR.scope.str.startswith("origin=")]
    P(f"  within-origin Pearson: " + "  ".join(f"{r.scope.split('=')[1]} {r.pearson:+.4f}"
                                               for r in wi.itertuples()))

    # ---- what is a three-point ladder agreement actually worth? ------------------------
    P("")
    P("  THE TRIPLE TEST - the queue's evidence is 'two ladders agree on 3 panels'.  Draw")
    P("  random TRIPLES of sub-panels and ask how often the GATE ordering and the CONC")
    P("  ordering agree.  Chance for two independent orderings of 3 items is 1/6 = 0.1667;")
    P("  agreeing merely on the DIRECTION of the top-vs-bottom pair is 1/2 = 0.5000.")
    rng = np.random.default_rng(319)
    N_TRIP = 20000
    trip = []
    for scope, sub in ([("ANY 3 DRAWS", DR)]
                       + [(f"3 draws, origin={o}", DR[DR.origin == o]) for o in ORIGINS]
                       + [("1 draw from each of U56/B136/SMALL "
                           "(the published panels' own shape)", None)]):
        full_hits = pair_hits = 0
        for _ in range(N_TRIP):
            if sub is None:
                pick = pd.concat([DR[DR.origin == o].sample(1, random_state=int(rng.integers(1e9)))
                                  for o in ["U56", "B136", "SMALL"]])
            else:
                pick = sub.sample(3, random_state=int(rng.integers(1e9)))
            g = pick.gate.values
            c = pick.conc.values
            if not (np.all(np.isfinite(g)) and np.all(np.isfinite(c))):
                continue
            full_hits += int(np.array_equal(np.argsort(-g), np.argsort(-c)))
            hi, lo = int(np.argmax(g)), int(np.argmin(g))
            pair_hits += int(c[hi] > c[lo])
        trip.append(dict(scope=scope, n_triples=N_TRIP,
                         same_full_order=full_hits / N_TRIP,
                         same_topbottom_sign=pair_hits / N_TRIP))
    TR = pd.DataFrame(trip)
    TR.to_csv(f"{OUT}.triples.csv", index=False)
    P("  " + fmt(TR.set_index("scope")).replace("\n", "\n  "))
    p_pub = float(TR.loc[TR.scope.str.startswith("1 draw from each"), "same_full_order"].iloc[0])
    P(f"  P(the two ladders agree completely on a published-shaped triple) = {p_pub:.4f}")
    P(f"  -> the published coincidence would recur {p_pub:.1%} of the time by composition luck"
      f" alone (chance floor 0.1667).")

    # ---------------------------------------------------------------- H_ONECHAR
    P("")
    P("-" * 140)
    P("H_ONECHAR - does ONE characteristic price BOTH ladders?  (all 3 k x 6 x = 18 cells)")
    P("-" * 140)

    def ols(x, y):
        m = np.isfinite(x) & np.isfinite(y)
        x, y = np.asarray(x)[m], np.asarray(y)[m]
        if len(x) < 3 or np.std(x) == 0:
            return np.nan, np.nan, np.nan, 0
        b, a = np.polyfit(x, y, 1)
        yh = a + b * x
        ss = float(((y - y.mean()) ** 2).sum())
        r2 = float(1 - ((y - yh) ** 2).sum() / ss) if ss > 0 else np.nan
        se = np.sqrt(((y - yh) ** 2).sum() / max(len(x) - 2, 1)
                     / max(((x - x.mean()) ** 2).sum(), 1e-12))
        return float(b), float(a), r2, float(b / se) if se > 0 else np.nan

    fit_rows = []
    for k in [None] + KS:
        sub = DR if k is None else DR[DR.k == k]
        for x in CHARS:
            for stat, gap in [("gate", GAP_GATE), ("conc", GAP_CONC)]:
                b, a, r2, t = ols(sub[x].values, sub[stat].values)
                fit_rows.append(dict(k=("ALL" if k is None else k), x=x, stat=stat,
                                     n=len(sub), slope=b, intercept=a, R2=r2, t=t,
                                     span=float(b * (sub[x].max() - sub[x].min()))
                                     if np.isfinite(b) else np.nan,
                                     span_over_gap=float(b * (sub[x].max() - sub[x].min()) / gap)
                                     if np.isfinite(b) else np.nan))
    F = pd.DataFrame(fit_rows)
    F.to_csv(f"{OUT}.fits.csv", index=False)
    P("  OLS <stat> ~ a + b*x over the draw population.  span = b * (max x - min x) in the")
    P("  statistic's own units; span/gap compares it to that ladder's published 3-panel gap.")
    for k in ["ALL"] + KS:
        P(f"\n  [k = {k}]")
        piv = F[F.k == k].pivot_table(index="x", columns="stat",
                                      values=["R2", "slope", "t", "span_over_gap"])
        P("  " + fmt(piv.reindex(CHARS)).replace("\n", "\n  "))
    both = F[(F.k == "ALL")].pivot_table(index="x", columns="stat", values="R2")
    both["min_R2"] = both.min(axis=1)
    best = both.min_R2.idxmax()
    onechar = bool(both.loc[best, "min_R2"] >= R2_BAR)
    P("")
    P(f"  H_ONECHAR bar: some x with BOTH R2 >= {R2_BAR:.2f}.  Best x = {best} "
      f"(gate R2 {both.loc[best,'gate']:.4f}, conc R2 {both.loc[best,'conc']:.4f}) "
      f"-> H_ONECHAR {'HOLDS' if onechar else 'FAILS'}")

    # predicted 3-panel ordering from each characteristic
    P("")
    P("  PREDICTED three-panel ordering from each characteristic (fit on draws only, then")
    P("  evaluated at the REAL panels' own x).  A characteristic that 'prices both' must")
    P("  reproduce BOTH published ladders:")
    REAL = D[D.origin == "REAL"].set_index("label")
    pred_rows = []
    for x in CHARS:
        for stat, gap in [("gate", GAP_GATE), ("conc", GAP_CONC)]:
            b, a, r2, t = ols(DR[x].values, DR[stat].values)
            preds = {}
            for lab in REAL.index:
                preds[lab] = a + b * REAL.loc[lab, x]
            order_pred = [l for l, _ in sorted(preds.items(), key=lambda kv: -kv[1])]
            act = {lab: REAL.loc[lab, stat] for lab in REAL.index}
            order_act = [l for l, _ in sorted(act.items(), key=lambda kv: -kv[1])]
            resid = max(abs(act[l] - preds[l]) for l in REAL.index)
            pred_rows.append(dict(x=x, stat=stat, R2=r2,
                                  pred_order=" > ".join(s.replace("REAL:", "") for s in order_pred),
                                  act_order=" > ".join(s.replace("REAL:", "") for s in order_act),
                                  order_ok=order_pred == order_act,
                                  max_resid=resid, resid_over_gap=resid / gap))
    PRD = pd.DataFrame(pred_rows)
    PRD.to_csv(f"{OUT}.predict.csv", index=False)
    P("  " + fmt(PRD.set_index(["x", "stat"])).replace("\n", "\n  "))
    both_ok = (PRD.groupby("x").order_ok.sum() == 2)
    P(f"  characteristics reproducing BOTH published orderings: "
      f"{list(both_ok[both_ok].index) or 'NONE'}")

    # ---------------------------------------------------------------- H_NOISE
    P("")
    P("-" * 140)
    P("H_NOISE - can three panels separate a panel property from composition luck?")
    P("-" * 140)
    nf = []
    for k in KS:
        for org in ORIGINS:
            s = DR[(DR.k == k) & (DR.origin == org)]
            if len(s) < 3:
                continue
            nf.append(dict(k=k, origin=org, n=len(s),
                           gate_sd=float(s.gate.std()), gate_over_gap=float(s.gate.std() / GAP_GATE),
                           gate_range=float(s.gate.max() - s.gate.min()),
                           conc_sd=float(s.conc.std()), conc_over_gap=float(s.conc.std() / GAP_CONC),
                           conc_range=float(s.conc.max() - s.conc.min())))
    NF = pd.DataFrame(nf)
    NF.to_csv(f"{OUT}.noise.csv", index=False)
    P("  within-cell seed sd of each statistic, and that sd as a multiple of its own")
    P(f"  published 3-panel gap (GATE {GAP_GATE:.4f}, CONC {GAP_CONC:.4f}):")
    P("  " + fmt(NF.set_index(["k", "origin"])).replace("\n", "\n  "))
    P(f"  median gate_sd/gap {NF.gate_over_gap.median():.3f}  |  "
      f"median conc_sd/gap {NF.conc_over_gap.median():.3f}  (bar 0.50)")
    P(f"  cells whose sd exceeds HALF its published gap: GATE "
      f"{int((NF.gate_over_gap>=0.5).sum())}/{len(NF)}, CONC {int((NF.conc_over_gap>=0.5).sum())}/{len(NF)}")
    # how often does a same-cell seed PAIR straddle the whole published gap?
    strad = []
    for k in KS:
        for org in ORIGINS:
            s = DR[(DR.k == k) & (DR.origin == org)]
            if len(s) < 2:
                continue
            for stat, gap in [("gate", GAP_GATE), ("conc", GAP_CONC)]:
                v = s[stat].dropna().values
                dif = np.abs(v[:, None] - v[None, :])
                iu = np.triu_indices(len(v), 1)
                strad.append(dict(k=k, origin=org, stat=stat, pairs=len(iu[0]),
                                  share_gt_gap=float((dif[iu] > gap).mean())))
    ST = pd.DataFrame(strad)
    ST.to_csv(f"{OUT}.straddle.csv", index=False)
    P("")
    P("  share of same-cell seed PAIRS differing by more than the WHOLE published gap "
      "(idea 312's test):")
    P("  " + fmt(ST.pivot_table(index=["k", "origin"], columns="stat",
                                values="share_gt_gap")).replace("\n", "\n  "))
    P(f"  pooled: GATE {ST[ST.stat=='gate'].share_gt_gap.mean():.3f}  "
      f"CONC {ST[ST.stat=='conc'].share_gt_gap.mean():.3f}")
    P("")
    P("  A SECOND, INDEPENDENT noise source for CONC: the statistic is a MEAN over narrow")
    P("  days, so it carries its own sampling error even at fixed composition.")
    se = DR.groupby("origin").agg(n=("conc_se", "size"), conc=("conc", "mean"),
                                  conc_se=("conc_se", "mean"),
                                  med_abs_t=("conc_t", lambda s: s.abs().median()),
                                  share_t2=("conc_t", lambda s: float((s.abs() >= 2).mean())))
    P("  " + fmt(se).replace("\n", "\n  "))
    P(f"  pooled: median |t| {DR.conc_t.abs().median():.2f}, |t| >= 2 on "
      f"{int((DR.conc_t.abs()>=2).sum())}/{len(DR)} draws ({(DR.conc_t.abs()>=2).mean():.1%}).")

    # ---------------------------------------------------------------- rule 8
    P("")
    P("-" * 140)
    P("RULE 8 WALK-FORWARD")
    P("-" * 140)
    P("  WF-A (on the ANSWER): fit <stat> ~ x on IS returns only (..2016), read the same fit")
    P("  on OOS returns (2017..).  A characteristic that prices a ladder must keep its sign.")
    wf = []
    for x in CHARS:
        for stat in ["gate", "conc"]:
            bi, ai, r2i, ti = ols(DR[x].values, DR[f"{stat}_IS"].values)
            bo, ao, r2o, to = ols(DR[x].values, DR[f"{stat}_OOS"].values)
            wf.append(dict(x=x, stat=stat, slope_IS=bi, R2_IS=r2i, slope_OOS=bo, R2_OOS=r2o,
                           sign_held=bool(np.isfinite(bi) and np.isfinite(bo)
                                          and np.sign(bi) == np.sign(bo))))
    WFA = pd.DataFrame(wf)
    P("  " + fmt(WFA.set_index(["x", "stat"])).replace("\n", "\n  "))
    P(f"  slope sign held IS -> OOS in {int(WFA.sign_held.sum())}/{len(WFA)} (x, stat) fits.")
    pe_is, sp_is, n_is = rho_pair(DR.gate_IS.values, DR.conc_IS.values)
    pe_os, sp_os, n_os = rho_pair(DR.gate_OOS.values, DR.conc_OOS.values)
    P(f"  rho(GATE, CONC) IS  Pearson {pe_is:+.4f} / Spearman {sp_is:+.4f} (n {n_is})")
    P(f"  rho(GATE, CONC) OOS Pearson {pe_os:+.4f} / Spearman {sp_os:+.4f} (n {n_os})")
    P("")
    P("  WF-B (on a BOOK): choose (arm, origin, k) by IS Sharpe pooled over seeds, read that")
    P("  cell's OOS untouched, against RULES v2 and SPY OOS.")
    isr = B[B.origin != "REAL"].groupby(["arm", "origin", "k"]).agg(
        IS=("IS_Sharpe", "mean"), OOS_S=("OOS_Sharpe", "mean"), OOS_C=("OOS_CAGR", "mean"),
        OOS_D=("OOS_MaxDD", "mean"), n=("IS_Sharpe", "size")).reset_index()
    isr = isr.sort_values("IS", ascending=False)
    isr.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("  top 8 IS cells (of %d), OOS shown untouched:" % len(isr))
    P("  " + fmt(isr.head(8).set_index(["arm", "origin", "k"])).replace("\n", "\n  "))
    pick = isr.iloc[0]
    bo_ = metrics(base_v2.loc[OOS_START:]); so_ = metrics(spy.loc[OOS_START:])
    P(f"  WF-B pick: {pick.arm} / {pick.origin} / k={int(pick.k)}  IS Sharpe {pick.IS:.4f}"
      f"  -> OOS CAGR {pick.OOS_C:.2%}  Sharpe {pick.OOS_S:.4f}  MaxDD {pick.OOS_D:.1%}")
    P(f"  OOS comparands: RULES v2 CAGR {bo_['CAGR']:.2%} Sharpe {bo_['Sharpe']:.4f} "
      f"MaxDD {bo_['MaxDD']:.1%} | SPY CAGR {so_['CAGR']:.2%} Sharpe {so_['Sharpe']:.4f} "
      f"MaxDD {so_['MaxDD']:.1%}")
    # the individual books of the winning cell, on both KEEP paths
    wcell = B[(B.arm == pick.arm) & (B.origin == pick.origin) & (B.k == pick.k)]
    P(f"  WF-B cell books: 4a {int(wcell.keep4a.sum())}/{len(wcell)}, "
      f"4b {int(wcell.keep4b.sum())}/{len(wcell)}, "
      f"BOTH {int((wcell.keep4a & wcell.keep4b).sum())}/{len(wcell)}; "
      f"4b failing legs {dict(wcell.fail4b.value_counts())}")

    # ---------------------------------------------------------------- KEEP paths
    P("")
    P("-" * 140)
    P("KEEP PATHS (PROTOCOL 4a and 4b) over every book run")
    P("-" * 140)
    kp = B.groupby("arm").agg(n=("keep4a", "size"), keep4a=("keep4a", "sum"),
                              keep4b=("keep4b", "sum")).reset_index()
    kp["both"] = [int(((B.arm == a) & B.keep4a & B.keep4b).sum()) for a in kp.arm]
    kp.to_csv(f"{OUT}.keeppaths.csv", index=False)
    P("  " + fmt(kp.set_index("arm"), 0).replace("\n", "\n  "))
    P(f"  TOTAL: 4a {int(B.keep4a.sum())}/{len(B)}, 4b {int(B.keep4b.sum())}/{len(B)}, "
      f"BOTH {int((B.keep4a & B.keep4b).sum())}/{len(B)}")
    P("  4b failing legs across all books: " +
      "  ".join(f"{k} {v}" for k, v in B.fail4b.value_counts().head(10).items()))
    both_b = B[B.keep4a & B.keep4b]
    if len(both_b):
        P("  books clearing BOTH paths:")
        P("  " + fmt(both_b.head(20).set_index(["label", "arm"])).replace("\n", "\n  "))
    else:
        P("  No book clears both paths.")
    # 4b alone is a KEEP path, so the 4b passers are priced explicitly before being declined.
    pss = B[B.keep4b].copy()
    ctl = B[B.arm == "EWall"].set_index("label").Sharpe
    pss["ctl_Sharpe"] = pss.label.map(ctl)
    pss["beats_ctl"] = pss.Sharpe > pss.ctl_Sharpe
    P("")
    P(f"  4b is a KEEP path on its own, so the {len(pss)} passers are priced before being")
    P("  declined.  Against their OWN ungated EWall control on the same sub-panel:")
    P("  " + fmt(pss.groupby("arm").beats_ctl.agg(["sum", "size"]), 0).replace("\n", "\n  "))
    P(f"  {int(pss.beats_ctl.sum())}/{len(pss)} beat their own control (idea 311's reading:")
    P("  a 4b pass on a fixed-gross selection book is a dial placement, not an edge).")
    real_p = pss[pss.origin == "REAL"]
    P("")
    P(f"  Only {len(real_p)} passers are IMPLEMENTABLE (a named panel, not a random draw):")
    if len(real_p):
        P("  " + fmt(real_p.set_index(["label", "arm"])[
            ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "keep4a",
             "beats_ctl"]]).replace("\n", "\n  "))
    P("  All three are books the record already carries (MA-RS is idea 51's treatment, NF20")
    P("  idea 2's broad leg), all fail 4a against the live RULES v2, and this run measured")
    P("  them only as the fixed instruments of a ladder question.  DECLINED: no memo, no")
    P("  promotion, no rule change.")

    # ---------------------------------------------------------------- verdict
    P("")
    P("=" * 140)
    P("VERDICT")
    P("=" * 140)
    P(f"  H_COINC   {'HOLDS' if coinc else 'FAILS'}   pooled rho(GATE, CONC) "
      f"P {pe:+.4f} / S {sp:+.4f} on n={n} draws (bar |rho| < {RHO_BAR})")
    P(f"  H_ONECHAR {'HOLDS' if onechar else 'FAILS'}   best x = {best}, "
      f"min(R2) {both.loc[best,'min_R2']:.4f} (bar {R2_BAR})")
    P(f"  H_NOISE   GATE median sd/gap {NF.gate_over_gap.median():.3f}, "
      f"CONC median sd/gap {NF.conc_over_gap.median():.3f} (bar 0.50)")
    P(f"  TRIPLE    P(both ladders agree on a published-shaped triple) {p_pub:.4f} "
      f"(chance 0.1667)")
    P(f"  CONC SE   |t| >= 2 on {int((DR.conc_t.abs()>=2).sum())}/{len(DR)} draws; "
      f"real anchors t " + " ".join(f"{l.replace('REAL:','')} {REAL.loc[l,'conc_t']:+.2f}"
                                    for l in REAL.index))
    P(f"  KEEP      4a {int(B.keep4a.sum())}/{len(B)}, 4b {int(B.keep4b.sum())}/{len(B)}, "
      f"BOTH {int((B.keep4a & B.keep4b).sum())}/{len(B)}")
    P(f"  runtime {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
