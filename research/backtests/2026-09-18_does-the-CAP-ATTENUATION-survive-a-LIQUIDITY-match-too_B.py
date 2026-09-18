#!/usr/bin/env python3
"""Idea 1078 (lane B, 2026-09-18) — does the CAP ATTENUATION survive a LIQUIDITY match too?

QUESTION (QUEUE idea 1078, verbatim)
    idea 1073 killed the volatility explanation for the 5.82x cap attenuation in
    rho(n/k, OOS S|k) (matching closes at most 50.5% of the gap, and at matched vol cap still
    moves rho 3.7x harder than vol).  Realised vol is only one proxy for 'small caps are
    noisier'.  Re-run the same three-tolerance ladder matched on median dollar volume instead
    (`load_volume(small=True)` x price), and report whether liquidity closes more of the gap
    than vol did.  Max 2 params (q, liquidity-match tolerance).

THE OBSTACLE, MEASURED NOT ASSUMED.  The ladder the queue asks to re-match spans TWO pools:
    q = 0.00 is pure BSTK (the ~100 large-cap stocks of `universe_broad.json`) and q = 1.00 is
    pure SMALL (the sub-$2B screen).  A dollar-volume window can only be imposed where BOTH
    pools carry a volume.  `load_volume` serves the small panel alone (it raises on
    small=False), and `data/` holds no volume cache for the broad panel.  PART 0 censuses this
    rather than asserting it, and the count it prints is the reason the queue's LITERAL run
    cannot be executed offline.  Two feasible routes are then run in full, and BOTH are
    reported; neither is allowed to stand in for the literal run.

    ROUTE A (real dollar volume, narrower cap axis).  Inside the small panel alone, cut the
        pool at its OWN median market cap into BIG (upper half of the sub-$2B screen) and TINY
        (lower half).  Every name there carries a real median IS dollar volume, so the queue's
        own variable can be used.  The SAME axis is ALSO run with a VOL match at the SAME
        tolerances, so "more of the gap than vol did" is answered LIKE FOR LIKE on one axis
        rather than against 1073's number on a different one.
    ROUTE B (1073's committed cap axis, proxy liquidity).  Keep SMALL vs BSTK exactly as 1073
        built it and match on the ROLL (1984) implied effective spread, 2*sqrt(-cov(r_t,r_t-1)),
        which is a liquidity measure computable FROM PRICES ALONE and therefore available on
        both pools.  It is a PROXY, so it is validated first: its rank correlation against the
        true median dollar volume is measured on the small names that carry both (H_VALID), and
        every claim taken from route B is scaled to that number.

THE TWO DIALS (rule 4 — no more than two tuned parameters)
    1. CAP MIX            q in {0.00, 0.50, 1.00} (fraction of the panel drawn from the SMALLER
                          -cap pool of whichever axis is in play).
    2. MATCH TOLERANCE    tau in {UNMATCHED, 0.45, 0.30, 0.20} — 1073's three tolerances,
                          inherited unchanged.
    All cells are reported at every k.  No cell is selected on.  The MATCH VARIABLE (dollar
    volume / realised vol / Roll spread) and the AXIS are ARMS, not dials: every arm is run at
    every (q, tau) and all of them are published.

THE WINDOW FORM IS NOT A THIRD DIAL.  It is fixed per variable by a rule declared here, before
    any book is run, that mentions no return and no verdict:
        if SD(log10 x) over the pooled eligible names < 1 decade -> MULTIPLICATIVE window
           x in X* x (1 +/- tau)                      (this is 1073's own form)
        else                                          -> DECADE window
           |log10 x - log10 X*| <= tau  decades
    A multiplicative +/-45% window is a 2.6x range; realised vol and the Roll spread span far
    less than a decade, so it binds on them.  Median dollar volume spans FOUR decades, where a
    2.6x window is empty by construction — the decade form is the same dial measured on the
    scale the variable actually lives on.  Which branch each variable took is printed with the
    SD that decided it (G8).

X* IS NOT A THIRD DIAL EITHER.  Exactly 1073's declared feasibility rule: over a grid, X*
    maximises min(n_lo_pool, n_hi_pool) inside the WIDEST window (tau = 0.45), ties to the lower
    X.  The whole grid each X* was chosen from is committed (.xstar.csv).

REPORTED, NOT TUNED
    - k in {20, 30, 40} (the control every rho is taken WITHIN), 8 seeded draws per cell.
      The tight tolerances do not admit every (q, k): infeasible cells are listed, not filled,
      and the HEADLINE block is k=20, the only width feasible at every tau on every arm.
    - the n/k ladder at {0.10, 0.20, 0.35, 0.50}.
    - the CROSSQ arm: each within-SMALL pool cut at its OWN median IS dollar volume, the
      liquidity analogue of 1073's decisive crossing cut.
    - the REPRO arm: 1073's four crossing cells rebuilt with its own pools, seed and draw order,
      to reproduce its committed +0.8759 / +0.7649 / +0.3586 / +0.1769 and its 0.4063 shift.
    Everything else inherited: RULES v1 eligibility, the v1 composite with the vol scaler OFF,
    GROSS 0.75, weekly, 10 bps, next-day execution, 260-day warm-up skip, IS ..2016, OOS 2017.. .

NO LOOK-AHEAD IN ANY DIAL.  Every dollar volume, every vol and every Roll spread used to build
    or match a panel is computed on 2010..2016-12-31 ONLY.  Gated (G3) by printing each IS
    measure against the full-sample measure it was not allowed to see.
    ONE EXCEPTION, DECLARED: the market cap that defines route A's axis is TODAY's cap from
    `research/deepvalue/universe_under2b.csv`.  It is a today-label of exactly the same kind as
    the SMALL / BSTK membership 1073's own axis is built from (both pools are current
    constituents), so route A inherits that label's status and no more.  It is never used to
    match, only to define the axis, and it is stated again under LIMITS.

WHAT IS DECLARED BEFORE ANY NUMBER
    H_REPRO    1073's four committed crossing rho reproduce here to |d| < 0.01.
    H_INFEAS   the queue's literal run is infeasible offline: 0 BSTK names carry a cached volume.
    H_VALID    the Roll spread is a usable liquidity proxy: |Spearman(Roll, -log10 DV)| >= 0.50
               on the small names carrying both.
    H_DVGAP    route A's axis really is a liquidity axis: median DV of BIG / TINY >= 2.0x.
    H_SPREAD   the attenuation is PRESENT to be matched away on route A's unmatched k=20 block:
               rho(q=0.00) - rho(q=1.00) >= 0.20.
    H_LIQ      LIQUIDITY matching closes it: at tau=0.20 the route-A gap is <= 50% of its
               UNMATCHED value on the same block.
    H_MORE     THE QUEUE'S QUESTION: on the SAME axis and the SAME block, liquidity closes MORE
               of the gap than vol does at EVERY tau.
    H_MONO     the liquidity closing is monotone in tau (0.45 -> 0.30 -> 0.20).
    H_ROLLSPR  the attenuation is present on route B's (1073's own) unmatched k=20 block.
    H_ROLL     on 1073's own axis a Roll-spread match closes >= 50% of that gap at tau=0.20.

RULE 8 (required).  n/k is chosen on 2009-2016 IS Sharpe ONLY inside each (arm, cell, tau, k,
    draw) choice set and the pick is read ONCE on 2017- against the do-nothing anchor (that
    choice set's mean OOS Sharpe), against SPY and against RULES v2 on the same panel.  Both
    KEEP paths are evaluated on EVERY book row with idea 286's committed `keep_paths`.

SURVIVORSHIP (rule 9).  SMALL and BSTK are CURRENT constituents of their screens
    (data/SMALL_PANEL_README.md).  Worse for THIS question than for most: a liquidity window is
    a window on names that were liquid enough to survive to be screened today, and route A's
    cap axis is cut on a cap measured today.  Every level is optimistic and every 4a/4b count an
    UPPER bound.  These are the record's committed CAND-n books on random sub-panels, so a 4b
    pass is a statement about the draw, not a capital candidate.  Nothing here is promoted.
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_volume, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


COST, FREQ, GROSS = 10, "W", 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARM = 260
MEAS_START = "2010-01-01"          # every IS measure starts here (1073's VOL_START)
QS = [0.00, 0.50, 1.00]            # DIAL 1
TAUS = [np.nan, 0.45, 0.30, 0.20]  # DIAL 2 (nan = UNMATCHED)
KS = [20, 30, 40]
HEADLINE_K = 20
RATIOS = [0.10, 0.20, 0.35, 0.50]
N_DRAWS = 8
COV_MIN = 0.90
SEED = 1078
pd.set_option("display.width", 260)
pd.set_option("display.max_rows", 900)

# committed anchors — idea 1073 lane C, `.crossing.csv`
RHO1073 = {"BSTK-LO": 0.8759082918622507, "BSTK-HI": 0.7649147351270061,
           "SMALL-LO": 0.3586072408278919, "SMALL-HI": 0.17691475003962565}
SHIFT1073 = 0.4063            # |rho(BSTK-HI) - rho(SMALL-LO)|, committed
VOLCLOSE1073 = {"0.45": 18.8, "0.30": 50.5, "0.20": 28.3}   # % of the GAP, committed


def _load(p, name):
    spec = importlib.util.spec_from_file_location(name, str(p))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


M276 = _load(BT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.py", "i276")
M286 = _load(BT / "2026-09-09_price-the-14-breadth-files-on-their-own-books_B.py", "i286")
M694 = _load(BT / "2026-09-11_is-the-WIDTH-to-OOS-slope-a-SELECTION-POOL-effect-or-a-SMALL-CAP-effect_cloud.py",
             "i694")
B1073 = BT / "2026-09-16_is-the-CAP-AXIS-a-STRENGTH-dial-rather-than-a-SIGN-dial_C.books.csv"

full_row, keep_paths = M286.full_row, M286.keep_paths
spearman, partial_spearman = M286.spearman, M286.partial_spearman
fast_bt, panel_cache, cand_w_fast, gross_stats = (M694.fast_bt, M694.panel_cache,
                                                  M694.cand_w_fast, M694.gross_stats)


# ------------------------------------------------------------------ the three IS measures
def name_vol(px, cols, end=IS_END):
    """1073's measure, unchanged: realised annualised daily vol, IS only, coverage-gated."""
    sub = px[cols].loc[MEAS_START:end]
    v = sub.pct_change().std() * np.sqrt(252)
    return v.where(sub.notna().mean() >= COV_MIN).dropna()


def dollar_vol(vol, px, cols, end=IS_END):
    """The queue's own variable: MEDIAN daily dollar volume = share volume x close, IS only."""
    cc = [c for c in cols if c in vol.columns and c in px.columns]
    if not cc:
        return pd.Series(dtype=float)
    v = vol[cc].loc[MEAS_START:end]
    d = (v * px[cc].loc[MEAS_START:end]).median()
    d = d.where(v.notna().mean() >= COV_MIN)
    return d[d > 0].dropna()


def roll_spread(px, cols, end=IS_END):
    """Roll (1984) implied effective spread 2*sqrt(-cov(r_t, r_t-1)) — PRICE-ONLY liquidity.
    Undefined (dropped) where the autocovariance is non-negative, which is the estimator's
    known failure mode and is counted, not filled."""
    sub = px[cols].loc[MEAS_START:end]
    r = sub.pct_change()
    cov_ok = sub.notna().mean()
    out, undef = {}, 0
    for c in cols:
        if c not in r.columns or cov_ok.get(c, 0) < COV_MIN:
            continue
        x = r[c].dropna().values
        if len(x) < 500:
            continue
        cv = float(np.cov(x[1:], x[:-1])[0, 1])
        if cv < 0:
            out[c] = 2.0 * np.sqrt(-cv)
        else:
            undef += 1
    return pd.Series(out, dtype=float).dropna(), undef


# ------------------------------------------------------------------ the declared window rule
def window_form(pooled):
    """DECLARED, outcome-free: multiplicative if the pooled cross-sectional SD of log10 x is
    under one decade, else decades."""
    sd = float(np.log10(pooled).std())
    return ("MULT" if sd < 1.0 else "DEC"), sd


def bounds(form, X, tau):
    if form == "MULT":
        return X * (1 - tau), X * (1 + tau)
    return 10 ** (np.log10(X) - tau), 10 ** (np.log10(X) + tau)


def pick_xstar(form, lo_ser, hi_ser, grid):
    """1073's feasibility rule: maximise min(n_lo, n_hi) inside the WIDEST window (tau=0.45),
    ties to the lower X.  Mentions no return, no Sharpe, no verdict."""
    rows = []
    for X in grid:
        lo, hi = bounds(form, X, 0.45)
        nl = int(((lo_ser >= lo) & (lo_ser <= hi)).sum())
        nh = int(((hi_ser >= lo) & (hi_ser <= hi)).sum())
        rows.append(dict(X=X, n_lo=nl, n_hi=nh, mn=min(nl, nh)))
    g = pd.DataFrame(rows)
    X = float(g.sort_values(["mn", "X"], ascending=[False, True]).iloc[0].X)
    return X, g


def main():
    t0all = time.time()
    P("=" * 110)
    P("IDEA 1078 — does-the-CAP-ATTENUATION-survive-a-LIQUIDITY-match-too (lane B, 2026-09-18)")
    P("=" * 110)
    P(f"TUNED (2): q (cap mix) in {QS}  x  tau (match tolerance) in "
      f"{['UNMATCHED' if t != t else t for t in TAUS]}.  Every cell reported.")
    P(f"ARMS (reported, never chosen among): DV / VOL on route A's within-SMALL cap axis, ROLL on")
    P(f"  1073's own SMALL-vs-BSTK axis, CROSSQ (each pool cut at its own median DV), REPRO.")
    P(f"REPORTED, NOT TUNED: k in {KS} (headline block k={HEADLINE_K}), {N_DRAWS} seeded draws, "
      f"n/k at {RATIOS}.")
    P("Costs 10 bps, weekly, next-day execution, GROSS 0.75, IS ..2016 / OOS 2017.. .")
    P("NO LOOK-AHEAD: every matching measure is computed on 2010..2016 ONLY (G3).")
    P("SURVIVORSHIP: both pools are current constituents; a liquidity window is a window on")
    P("  names liquid enough to survive to today.  Nothing here is a capital candidate.")

    src = M276.build_sources()
    pxs, pxb = src["pxs"], src["pxb"]
    idx = pxs.index.intersection(pxb.index)
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), pxb.reindex(idx).ffill()
    spy = pxb_c["SPY"]
    s_stk, b_stk = src["s_stk"], src["b_stk"]
    P(f"\ncommon calendar {idx[0].date()} .. {idx[-1].date()} ({len(idx)} days); "
      f"pools SMALL {len(s_stk)}, BSTK {len(b_stk)}")

    # ================================================================ PART 0 — the feasibility census
    P("\n" + "=" * 110)
    P("PART 0 — CAN THE QUEUE'S LITERAL RUN BE DONE OFFLINE?  (census, not assertion)")
    P("=" * 110)
    vol = load_volume(small=True)
    try:
        load_volume(small=False)
        broad_vol_serves = True
    except Exception as e:
        broad_vol_serves = False
        P(f"  baseline.load_volume(small=False) raises: {type(e).__name__}: {e}")
    cached = sorted(p.name for p in (ROOT / "data").glob("volume*"))
    n_b_vol = len([c for c in b_stk if c in vol.columns])
    n_s_vol = len([c for c in s_stk if c in vol.columns])
    P(f"  volume caches present in data/: {cached if cached else 'NONE'}")
    P(f"  BSTK names carrying a cached share volume: {n_b_vol} of {len(b_stk)}")
    P(f"  SMALL names carrying a cached share volume: {n_s_vol} of {len(s_stk)}")
    P(f"  => the q=0.00 end of 1073's ladder is PURE BSTK, so a dollar-volume window over the")
    P(f"     committed cap axis cannot be imposed offline.  Routes A and B below are run instead;")
    P(f"     neither is presented as the literal run.")

    # ================================================================ the measures
    vS, vB = name_vol(pxs_c, s_stk), name_vol(pxb_c, b_stk)
    dvS = dollar_vol(vol, pxs_c, s_stk)
    rS, undef_S = roll_spread(pxs_c, s_stk)
    rB, undef_B = roll_spread(pxb_c, b_stk)
    P(f"\nIS measures (2010..{IS_END}, coverage >= {COV_MIN}):")
    P(f"  realised vol      SMALL {len(vS):4d}  BSTK {len(vB):4d}")
    P(f"  median $ volume   SMALL {len(dvS):4d}  BSTK    0   (no cache)")
    P(f"  Roll spread       SMALL {len(rS):4d}  BSTK {len(rB):4d}   "
      f"(dropped for cov(r_t,r_t-1) >= 0: SMALL {undef_S}, BSTK {undef_B})")
    P(f"  SMALL $vol  q10/25/50/75/90 = "
      + " / ".join(f"{x:,.0f}" for x in dvS.quantile([.1, .25, .5, .75, .9])))
    P(f"  SMALL Roll  q10/50/90 = " + " / ".join(f"{x:.4f}" for x in rS.quantile([.1, .5, .9]))
      + f"   BSTK Roll q10/50/90 = " + " / ".join(f"{x:.4f}" for x in rB.quantile([.1, .5, .9])))

    # H_VALID — is the Roll spread a usable stand-in for the variable the queue named?
    both = [c for c in rS.index if c in dvS.index]
    rho_valid = spearman(rS.reindex(both), -np.log10(dvS.reindex(both)))
    P(f"\nROLL VALIDATION (H_VALID): Spearman(Roll spread, -log10 median $volume) over the "
      f"{len(both)} SMALL names carrying both = {rho_valid:+.4f}")

    # ---------------- route A axis: the within-SMALL cap cut (today-label, declared)
    uni = pd.read_csv(ROOT / "research" / "deepvalue" / "universe_under2b.csv")
    mc = uni.set_index("ticker")["mktcap"].dropna()
    mc = mc[~mc.index.duplicated()]
    ELIG = sorted(set(dvS.index) & set(vS.index) & set(mc.index))   # one name set for BOTH matches
    mcE = mc.reindex(ELIG)
    cap_med = float(mcE.median())
    TINY = sorted(mcE[mcE <= cap_med].index)
    BIG = sorted(mcE[mcE > cap_med].index)
    P(f"\nROUTE A axis (within-SMALL cap cut at the pool's OWN median cap "
      f"${cap_med/1e6:,.0f}M; TODAY-label, declared):")
    P(f"  eligible names carrying cap AND $volume AND vol: {len(ELIG)}  ->  "
      f"TINY {len(TINY)} (median ${mcE[TINY].median()/1e6:,.0f}M), "
      f"BIG {len(BIG)} (median ${mcE[BIG].median()/1e6:,.0f}M)")
    dv_ratio = float(dvS[BIG].median() / dvS[TINY].median())
    P(f"  median $volume  TINY {dvS[TINY].median():,.0f}  BIG {dvS[BIG].median():,.0f}  "
      f"= {dv_ratio:.2f}x   (H_DVGAP asks for >= 2.0x)")
    P(f"  mean IS vol     TINY {vS.reindex(TINY).mean():.4f}  BIG {vS.reindex(BIG).mean():.4f}  "
      f"= {vS.reindex(TINY).mean()/vS.reindex(BIG).mean():.3f}x")

    # ---------------- the window form, by the declared rule, per variable
    forms, sds = {}, {}
    forms["DV"], sds["DV"] = window_form(dvS.reindex(ELIG))
    forms["VOL"], sds["VOL"] = window_form(vS.reindex(ELIG))
    forms["ROLL"], sds["ROLL"] = window_form(pd.concat([rS, rB]))
    P("\nWINDOW FORM by the DECLARED rule (multiplicative if SD(log10 x) < 1 decade, else decades):")
    for v in ("DV", "VOL", "ROLL"):
        P(f"  {v:5s} SD(log10) {sds[v]:.3f}  ->  {'MULTIPLICATIVE  x in X*(1+/-tau)' if forms[v]=='MULT' else 'DECADES  |log10 x - log10 X*| <= tau'}")

    # ---------------- X* per arm, by 1073's feasibility rule
    XSTAR, GRIDS = {}, {}
    XSTAR["DV"], GRIDS["DV"] = pick_xstar(forms["DV"], dvS.reindex(TINY), dvS.reindex(BIG),
                                          np.round(10 ** np.arange(4.0, 7.51, 0.05), 2))
    XSTAR["VOL"], GRIDS["VOL"] = pick_xstar(forms["VOL"], vS.reindex(TINY), vS.reindex(BIG),
                                            np.round(np.arange(0.18, 0.801, 0.01), 2))
    XSTAR["ROLL"], GRIDS["ROLL"] = pick_xstar(forms["ROLL"], rS, rB,
                                              np.round(np.arange(0.002, 0.0601, 0.0005), 4))
    xs = pd.concat([g.assign(arm=a, form=forms[a]) for a, g in GRIDS.items()])
    xs.to_csv(f"{OUT}.xstar.csv", index=False)
    P("\nX* by 1073's declared feasibility rule (max min(n_lo, n_hi) at tau=0.45, ties low); "
      "full grids in .xstar.csv:")
    MEAS = {"DV": (dvS.reindex(TINY), dvS.reindex(BIG), "TINY", "BIG"),
            "VOL": (vS.reindex(TINY), vS.reindex(BIG), "TINY", "BIG"),
            "ROLL": (rS, rB, "SMALL", "BSTK")}
    for a in ("DV", "VOL", "ROLL"):
        lo_s, hi_s, ln, hn = MEAS[a]
        P(f"  {a:5s} X* = {XSTAR[a]:.4g}")
        for t in [x for x in TAUS if x == x]:
            lo, hi = bounds(forms[a], XSTAR[a], t)
            P(f"      tau={t:.2f}  window [{lo:.4g}, {hi:.4g}]  "
              f"{ln} {int(((lo_s>=lo)&(lo_s<=hi)).sum()):3d}  "
              f"{hn} {int(((hi_s>=lo)&(hi_s<=hi)).sum()):3d}")

    # ================================================================ panel construction
    panels, seen, infeasible = [], set(), []

    def add_matched(arm, lo_names, hi_names, lo_ser, hi_ser, form, X, rng):
        """q = fraction drawn from the LOW-cap (or LOW-liquidity-pool) side of the axis."""
        for t in TAUS:
            if t != t:
                wl, wh = sorted(lo_names), sorted(hi_names)
            else:
                lo, hi = bounds(form, X, t)
                wl = sorted(lo_ser[(lo_ser >= lo) & (lo_ser <= hi)].index)
                wh = sorted(hi_ser[(hi_ser >= lo) & (hi_ser <= hi)].index)
            for q in QS:
                for k in KS:
                    nl_ = int(round(q * k))
                    nh_ = k - nl_
                    if nl_ > len(wl) or nh_ > len(wh):
                        infeasible.append((arm, t, q, k, nl_, nh_, len(wl), len(wh)))
                        continue
                    for d in range(N_DRAWS):
                        lc = sorted(rng.choice(wl, size=nl_, replace=False)) if nl_ else []
                        hc = sorted(rng.choice(wh, size=nh_, replace=False)) if nh_ else []
                        key = (arm, tuple(lc), tuple(hc))
                        if key in seen:
                            P(f"  dedupe: {arm} tau={t} q={q:.2f} k={k} d{d} exact repeat — skipped")
                            continue
                        seen.add(key)
                        panels.append(dict(arm=arm, tau=t, q=q, k=k, draw=d,
                                           cols=list(lc) + list(hc),
                                           cell=f"q{q:.2f}/" + ("UNM" if t != t else f"t{t:.2f}")))

    add_matched("DV", TINY, BIG, dvS.reindex(TINY), dvS.reindex(BIG), forms["DV"], XSTAR["DV"],
                np.random.default_rng(SEED + 1))
    add_matched("VOL", TINY, BIG, vS.reindex(TINY), vS.reindex(BIG), forms["VOL"], XSTAR["VOL"],
                np.random.default_rng(SEED + 2))
    add_matched("ROLL", sorted(rS.index), sorted(rB.index), rS, rB, forms["ROLL"], XSTAR["ROLL"],
                np.random.default_rng(SEED + 3))
    P(f"\nMATCH arms built: DV {sum(1 for p in panels if p['arm']=='DV')}, "
      f"VOL {sum(1 for p in panels if p['arm']=='VOL')}, "
      f"ROLL {sum(1 for p in panels if p['arm']=='ROLL')} panels")
    if infeasible:
        P(f"  {len(infeasible)} INFEASIBLE cells (listed, never filled):")
        for a, t, q, k, nl_, nh_, wl, wh in infeasible:
            P(f"    {a:5s} tau={'UNM' if t!=t else f'{t:.2f}'} q={q:.2f} k={k}: needs "
              f"{nl_}lo/{nh_}hi, window holds {wl}lo/{wh}hi")

    # ---------------- CROSSQ arm: each within-SMALL pool cut at its OWN median IS $volume
    crossq = {}
    for nm, names in (("TINY", TINY), ("BIG", BIG)):
        d = dvS.reindex(names).dropna()
        med = float(d.median())
        crossq[f"{nm}-LOQ"] = (sorted(d[d <= med].index), float(d[d <= med].median()))
        crossq[f"{nm}-HIQ"] = (sorted(d[d > med].index), float(d[d > med].median()))
    P("\nCROSSQ arm pools (each cap pool cut at its OWN median IS $volume):")
    for nm, (names, mdv) in crossq.items():
        P(f"   {nm:10s} {len(names):3d} names, median $volume {mdv:,.0f}")
    rngq = np.random.default_rng(SEED + 4)
    for nm, (names, mdv) in crossq.items():
        for k in KS:
            if k > len(names):
                continue
            for d in range(N_DRAWS):
                cols = sorted(rngq.choice(names, size=k, replace=False))
                panels.append(dict(arm="CROSSQ", tau=np.nan,
                                   q=(1.0 if nm.startswith("TINY") else 0.0), k=k, draw=d,
                                   cols=list(cols), cell=nm))
    P(f"CROSSQ arm: {sum(1 for p in panels if p['arm']=='CROSSQ')} panels")

    # ---------------- REPRO arm: 1073's crossing cells, its pools, seed and draw order
    cross_pools_1073 = {}
    for nm, v in (("SMALL", vS), ("BSTK", vB)):
        med = float(v.median())
        cross_pools_1073[f"{nm}-LO"] = sorted(v[v <= med].index)
        cross_pools_1073[f"{nm}-HI"] = sorted(v[v > med].index)
    rngc = np.random.default_rng(1073 + 1)          # 1073's SEED + 1, its own value
    for nm, names in cross_pools_1073.items():
        for k in KS:
            if k > len(names):
                continue
            for d in range(N_DRAWS):
                cols = sorted(rngc.choice(names, size=k, replace=False))
                panels.append(dict(arm="REPRO", tau=np.nan,
                                   q=(1.0 if nm.startswith("SMALL") else 0.0), k=k, draw=d,
                                   cols=list(cols), cell=nm))
    P(f"REPRO arm: {sum(1 for p in panels if p['arm']=='REPRO')} panels "
      f"(1073's own pools, seed 1074 and draw order)")
    P(f"\nTOTAL {len(panels)} panels x {len(RATIOS)} books")

    # ================================================================ gates before results
    gates = {}
    S_SET, B_SET = set(s_stk), set(b_stk)

    def panel_px(cols):
        sc = [c for c in cols if c in S_SET]
        lc = [c for c in cols if c in B_SET and c not in S_SET]
        parts = ([pxs_c[sc]] if sc else []) + ([pxb_c[lc]] if lc else [])
        return pd.concat(parts + [spy.rename("SPY")], axis=1).dropna(how="all").ffill()[
            [c for c in cols] + ["SPY"]]

    ref = [p for p in panels if p["arm"] == "REPRO" and p["k"] == 40][0]
    px0 = panel_px(ref["cols"])
    c0 = panel_cache(px0, ref["cols"])
    w_ref = M286.cand_weights(20)(px0)
    dw = float(np.abs(w_ref.values - cand_w_fast(px0, c0, 20).values).max())
    eng = backtest(px0, w_ref, cost_bps=COST, freq=FREQ)
    r_f, t_f = fast_bt(px0, w_ref)
    dr = float(np.abs(eng["returns"] - r_f).max())
    dt = float(np.abs(eng["turnover"] - t_f).max())
    gates["G1"] = (dr < 1e-12 and dt < 1e-12 and dw == 0.0,
                   f"fast runner == engine.backtest on RETURNS ({dr:.2e}) and TURNOVER ({dt:.2e}); "
                   f"cached-rank CAND-20 == idea 286's committed cand_weights(20) (max|dw| {dw:.2e})")

    SER = {"DV": dvS, "VOL": vS, "ROLL": pd.concat([rS, rB])}
    bad = []
    for p in panels:
        k, q, t, cols, arm = p["k"], p["q"], p["tau"], p["cols"], p["arm"]
        if len(cols) != k or len(set(cols)) != len(cols):
            bad.append((arm, p["cell"], p["draw"], "width/dup"))
        if arm in ("DV", "VOL"):
            if sum(c in TINY for c in cols) != int(round(q * k)):
                bad.append((arm, p["cell"], p["draw"], "cap mix"))
        if arm == "ROLL":
            if sum(c in S_SET for c in cols) != int(round(q * k)):
                bad.append((arm, p["cell"], p["draw"], "cap mix"))
        if arm in ("DV", "VOL", "ROLL") and t == t:
            lo, hi = bounds(forms[arm], XSTAR[arm], t)
            ser = SER[arm]
            vv = [float(ser[c]) for c in cols if c in ser.index]
            if len(vv) != k or min(vv) < lo * (1 - 1e-9) or max(vv) > hi * (1 + 1e-9):
                bad.append((arm, p["cell"], p["draw"], "window"))
    gates["G2"] = (not bad, f"ENVELOPE over all {len(panels)} panels: exact width, no duplicate "
                            f"columns, exact cap mix on every matched arm, and EVERY name inside "
                            f"its declared window (not just the panel mean).  Violations: {len(bad)}"
                            + ("" if not bad else f" -> {bad[:5]}"))

    END = str(idx[-1].date())
    g3 = []
    for nm, is_s, full_s in (("realised vol", vS, name_vol(pxs_c, s_stk, end=END)),
                             ("median $volume", dvS, dollar_vol(vol, pxs_c, s_stk, end=END)),
                             ("Roll spread", rS, roll_spread(pxs_c, s_stk, end=END)[0])):
        com = [c for c in is_s.index if c in full_s.index]
        g3.append(f"{nm} {spearman(is_s.reindex(com), full_s.reindex(com)):+.4f} ({len(com)} names)")
    gates["G3"] = (True, "NO LOOK-AHEAD, reported not gated: each IS measure ranks against the "
                         "FULL-sample measure it was NOT allowed to see — " + "; ".join(g3)
                         + ".  High rank agreement is expected; what matters is that the OOS "
                           "window never entered any panel choice.")

    same = bool(np.array_equal(fast_bt(px0, w_ref)[0].values, r_f.values, equal_nan=True))
    gates["G4"] = (same, f"DETERMINISM: the reference book re-runs bit-identical ({same})")
    for g in ("G1", "G2", "G3", "G4"):
        P(f"  {g} {'PASS' if gates[g][0] else 'FAIL'}  {gates[g][1]}")

    # ================================================================ run the ladder
    P("\n" + "=" * 110)
    P("RUNNING THE LADDER")
    P("=" * 110)
    brows, prows = [], []
    for i, p in enumerate(panels):
        t0 = time.time()
        cols = p["cols"]
        px = panel_px(cols)
        st = px.index[WARM]
        cache = panel_cache(px, cols)
        n_elig = cache["gate"].sum(axis=1)
        reb = rebalance_mask(px.index, FREQ).values
        Ebar = float(n_elig[reb][px.index[reb] >= st].mean())
        pvol = float(np.mean([float(vS[c]) if c in vS.index else float(vB[c]) for c in cols
                              if (c in vS.index or c in vB.index)]))
        pdv = float(np.median([float(dvS[c]) for c in cols if c in dvS.index])) \
            if any(c in dvS.index for c in cols) else np.nan
        prl = float(np.mean([float(rS[c]) if c in rS.index else float(rB[c]) for c in cols
                             if (c in rS.index or c in rB.index)]))
        spy_r = full_row("SPY", px["SPY"].pct_change().fillna(0).loc[st:])
        wv2 = (rules_v2_weights(px).drop(columns=["SPY"], errors="ignore")
               .reindex(columns=px.columns).fillna(0.0))
        v2_r = full_row("v2", fast_bt(px, wv2)[0].loc[st:])
        for r in RATIOS:
            n = max(2, int(round(r * p["k"])))
            w = cand_w_fast(px, cache, n)
            ret, turn = fast_bt(px, w)
            row = full_row(f"CAND{n}", ret.loc[st:])
            a, b = keep_paths(row, spy_r, v2_r)
            g_nom, fill = gross_stats(px, w, st)
            brows.append(dict(arm=p["arm"], cell=p["cell"], tau=p["tau"], q=p["q"], k=p["k"],
                              draw=p["draw"], ratio=r, n=n, panel_vol=pvol, panel_dv=pdv,
                              panel_roll=prl, Ebar=Ebar, breadth=Ebar / p["k"], gross=g_nom,
                              fill=fill,
                              turnover=float(turn.loc[st:].sum() / (len(ret.loc[st:]) / 252)),
                              **{kk: vv for kk, vv in row.items() if kk != "tag"},
                              spy_S=spy_r["Sharpe"], spy_CAGR=spy_r["CAGR"], spy_DD=spy_r["MaxDD"],
                              spy_H1=spy_r["H1"], spy_H2=spy_r["H2"],
                              spy_OOS_S=spy_r["OOS_Sharpe"], spy_OOS_CAGR=spy_r["OOS_CAGR"],
                              spy_OOS_DD=spy_r["OOS_MaxDD"], v2_S=v2_r["Sharpe"],
                              v2_DD=v2_r["MaxDD"], v2_H1=v2_r["H1"], v2_H2=v2_r["H2"],
                              v2_OOS_S=v2_r["OOS_Sharpe"], v2_OOS_CAGR=v2_r["OOS_CAGR"],
                              v2_OOS_DD=v2_r["OOS_MaxDD"], pass4a=a, pass4b=b))
        prows.append(dict(arm=p["arm"], cell=p["cell"], tau=p["tau"], q=p["q"], k=p["k"],
                          draw=p["draw"], panel_vol=pvol, panel_dv=pdv, panel_roll=prl,
                          Ebar=Ebar, breadth=Ebar / p["k"]))
        if (i + 1) % 150 == 0 or i == 0:
            P(f"  [{i+1:4d}/{len(panels)}] {p['arm']}/{p['cell']} k={p['k']} d{p['draw']}  "
              f"{time.time()-t0:4.2f}s  (elapsed {time.time()-t0all:6.1f}s)")

    books = pd.DataFrame(brows)
    pans = pd.DataFrame(prows)
    books.to_csv(f"{OUT}.books.csv.gz", index=False, compression="gzip")
    pans.to_csv(f"{OUT}.panels.csv", index=False)
    P(f"\n{len(books):,} book rows over {len(pans):,} panels written.")

    # ---------------- G5 / G6: cross-run against idea 1073
    rep = books[books.arm == "REPRO"]
    RHO_REP = {c: partial_spearman(rep[rep.cell == c].OOS_Sharpe, rep[rep.cell == c].ratio,
                                   rep[rep.cell == c].k) for c in RHO1073}
    d5 = max(abs(RHO_REP[c] - RHO1073[c]) for c in RHO1073)
    shift_rep = abs(RHO_REP["BSTK-HI"] - RHO_REP["SMALL-LO"])
    gates["G5"] = (d5 < 0.01,
                   "CROSS-RUN idea 1073's committed crossing rho (its pools, seed and draw order): "
                   + "; ".join(f"{c} {RHO_REP[c]:+.4f} vs committed {RHO1073[c]:+.4f}"
                               for c in RHO1073)
                   + f"  max|d| {d5:.2e}; its 0.4063 shift reproduces at {shift_rep:.4f}")
    if B1073.exists():
        c1073 = pd.read_csv(B1073)
        c1073 = c1073[c1073.arm == "CROSS"][["cell", "k", "draw", "n", "OOS_Sharpe"]]
        m = rep.merge(c1073, on=["cell", "k", "draw", "n"], suffixes=("", "_1073"))
        dbk = float(np.abs(m.OOS_Sharpe - m.OOS_Sharpe_1073).max()) if len(m) else np.nan
        gates["G6"] = (len(m) > 0 and dbk < 1e-9,
                       f"CROSS-RUN at the BOOK level: {len(m)} of {len(rep)} REPRO rows join "
                       f"idea 1073's committed books.csv on (cell,k,draw,n); "
                       f"max|d OOS Sharpe| {dbk:.2e}")
    else:
        gates["G6"] = (False, "idea 1073's committed books.csv absent — book-level cross-run NOT run")

    # ---------------- G7: do the dials bind?
    g7bits, g7ok = [], True
    for arm, col in (("DV", "panel_dv"), ("VOL", "panel_vol"), ("ROLL", "panel_roll")):
        a = pans[pans.arm == arm]
        u = a[a.tau.isna()][col]
        t20 = a[np.isclose(a.tau.fillna(-1), 0.20)][col]
        if not len(t20):
            g7bits.append(f"{arm}: tau=0.20 EMPTY")
            g7ok = False
            continue
        su, s2 = float(np.log10(u).std()), float(np.log10(t20).std())
        g7ok = g7ok and s2 < su
        g7bits.append(f"{arm}: SD(log10 panel {col.split('_')[1]}) {su:.4f} (UNM) -> {s2:.4f} "
                      f"(tau=0.20)")
    gates["G7"] = (g7ok, "the tau dial BINDS on every matched arm — " + "; ".join(g7bits))
    gates["G8"] = (True, "X* GRIDS published in full (.xstar.csv, "
                         f"{len(xs)} points): " + "; ".join(
                             f"{a} form {forms[a]} X* {XSTAR[a]:.4g} min-count "
                             f"{int(GRIDS[a][np.isclose(GRIDS[a].X, XSTAR[a])].mn.iloc[0])}"
                             for a in ("DV", "VOL", "ROLL")))

    P("\n" + "=" * 110)
    P("GATES")
    P("=" * 110)
    for g in sorted(gates):
        P(f"  {g} {'PASS' if gates[g][0] else 'FAIL'}  {gates[g][1]}")
    npass = sum(1 for v in gates.values() if v[0])
    P(f"GATES: {npass} of {len(gates)} PASS.")
    pd.DataFrame([dict(gate=g, verdict="PASS" if v[0] else "FAIL", detail=v[1])
                  for g, v in sorted(gates.items())]).to_csv(f"{OUT}.gates.csv", index=False)

    # ================================================================ PART A — the ladders
    def ladder(arm, kblock):
        rows = []
        sub = books[(books.arm == arm)]
        if kblock is not None:
            sub = sub[sub.k == kblock]
        for t in TAUS:
            sel = sub[sub.tau.isna()] if t != t else sub[np.isclose(sub.tau.fillna(-1), t)]
            for q in QS:
                s = sel[sel.q == q]
                if len(s) < 8:
                    continue
                rows.append(dict(arm=arm, kblock=("ALL" if kblock is None else kblock),
                                 tau=("UNMATCHED" if t != t else f"{t:.2f}"), q=q, rows=len(s),
                                 panels=s.draw.nunique() * s.k.nunique(),
                                 panel_dv=s.panel_dv.mean(), panel_vol=s.panel_vol.mean(),
                                 panel_roll=s.panel_roll.mean(),
                                 rho=partial_spearman(s.OOS_Sharpe, s.ratio, s.k),
                                 OOS_S_mean=s.OOS_Sharpe.mean(), OOS_S_sd=s.OOS_Sharpe.std()))
        return pd.DataFrame(rows)

    LAD = pd.concat([ladder(a, kb) for a in ("DV", "VOL", "ROLL") for kb in (HEADLINE_K, None)],
                    ignore_index=True)
    LAD.to_csv(f"{OUT}.ladder.csv", index=False)
    P("\n" + "=" * 110)
    P(f"PART A — rho(n/k, OOS Sharpe | k) BY CAP MIX AND MATCH TOLERANCE (every cell, both blocks)")
    P("=" * 110)
    P(LAD.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    def gaps(arm, kblock):
        L = LAD[(LAD.arm == arm) & (LAD.kblock == ("ALL" if kblock is None else kblock))]
        piv = L.pivot(index="tau", columns="q", values="rho")
        out = {}
        for lbl in piv.index:
            if 0.0 in piv.columns and 1.0 in piv.columns:
                out[lbl] = (float(piv.loc[lbl, 0.0] - piv.loc[lbl, 1.0]),
                            float(piv.loc[lbl, 0.0]), float(piv.loc[lbl, 1.0]))
        return out

    P("\nTHE GAP rho(q=0.00) - rho(q=1.00) and the share of it each tolerance CLOSES")
    P(f"  (headline block k={HEADLINE_K} — the only width feasible at every tau on every arm):")
    closure = {}
    for arm in ("DV", "VOL", "ROLL"):
        G = gaps(arm, HEADLINE_K)
        if "UNMATCHED" not in G:
            P(f"   {arm}: UNMATCHED cell missing — no closure reportable")
            continue
        gU = G["UNMATCHED"][0]
        P(f"   {arm:5s} UNMATCHED gap {gU:+.4f}  (q=0.00 {G['UNMATCHED'][1]:+.4f}, "
          f"q=1.00 {G['UNMATCHED'][2]:+.4f})")
        closure[arm] = {}
        for lbl in ("0.45", "0.30", "0.20"):
            if lbl not in G:
                P(f"         tau={lbl} — cell absent (infeasible)")
                continue
            g = G[lbl][0]
            pct = 100 * (1 - g / gU) if abs(gU) > 1e-12 else np.nan
            closure[arm][lbl] = pct
            P(f"         tau={lbl}  gap {g:+.4f}  closes {pct:6.1f}% of UNMATCHED   "
              f"(q=0.00 {G[lbl][1]:+.4f}, q=1.00 {G[lbl][2]:+.4f})")
    P("\n  ALL-k block (reported beside it; its tight cells hold fewer q,k combinations):")
    for arm in ("DV", "VOL", "ROLL"):
        G = gaps(arm, None)
        if "UNMATCHED" not in G:
            continue
        gU = G["UNMATCHED"][0]
        P(f"   {arm:5s} UNMATCHED {gU:+.4f} -> "
          + ", ".join(f"tau={l} {G[l][0]:+.4f} ({100*(1-G[l][0]/gU):.1f}%)"
                      for l in ("0.45", "0.30", "0.20") if l in G))

    # ---------------- the queue's actual comparison
    P("\n" + "=" * 110)
    P("PART B — THE QUEUE'S QUESTION: does LIQUIDITY close MORE of the gap than VOL does?")
    P("=" * 110)
    P(f"  Route A, ONE axis (within-SMALL cap cut), ONE block (k={HEADLINE_K}), the SAME three")
    P("  tolerances, the two variables run side by side.  This is the like-for-like comparison;")
    P("  1073's committed vol closures sit on a DIFFERENT axis and are shown only for reference.")
    cmp_rows = []
    for lbl in ("0.45", "0.30", "0.20"):
        dvc = closure.get("DV", {}).get(lbl, np.nan)
        vlc = closure.get("VOL", {}).get(lbl, np.nan)
        cmp_rows.append(dict(tau=lbl, DV_closes_pct=dvc, VOL_closes_pct=vlc,
                             liquidity_more=bool(dvc > vlc) if (dvc == dvc and vlc == vlc) else None,
                             ROLL_closes_pct=closure.get("ROLL", {}).get(lbl, np.nan),
                             vol_1073_committed_pct=VOLCLOSE1073[lbl]))
    CMP = pd.DataFrame(cmp_rows)
    CMP.to_csv(f"{OUT}.comparison.csv", index=False)
    P(CMP.to_string(index=False, float_format=lambda x: f"{x:.1f}"))

    # ---------------- CROSSQ: the decisive cut on the liquidity axis
    P("\n" + "=" * 110)
    P("PART C — THE CROSSING CUT ON THE LIQUIDITY AXIS (cap fixed, $volume moved; and across)")
    P("=" * 110)
    cq = books[books.arm == "CROSSQ"]
    crows = []
    for cell in ("BIG-LOQ", "BIG-HIQ", "TINY-LOQ", "TINY-HIQ"):
        s = cq[cq.cell == cell]
        if not len(s):
            continue
        crows.append(dict(cell=cell, cap=("BIG" if cell.startswith("BIG") else "TINY"),
                          rows=len(s), panel_dv=s.panel_dv.mean(), panel_vol=s.panel_vol.mean(),
                          rho=partial_spearman(s.OOS_Sharpe, s.ratio, s.k),
                          OOS_S_mean=s.OOS_Sharpe.mean(), OOS_S_sd=s.OOS_Sharpe.std(),
                          breadth=s.breadth.mean()))
    C = pd.DataFrame(crows)
    C.to_csv(f"{OUT}.crossq.csv", index=False)
    P(C.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    cr = C.set_index("cell").rho.to_dict() if len(C) else {}
    d_liq_same_cap = d_cap_same_liq = np.nan
    if len(cr) == 4:
        d_liq_same_cap = abs(cr["BIG-HIQ"] - cr["BIG-LOQ"])
        d_cap_same_liq = abs(cr["BIG-LOQ"] - cr["TINY-HIQ"])
        P(f"\n   SAME CAP, different $volume : |rho(BIG-HIQ) - rho(BIG-LOQ)| = {d_liq_same_cap:.4f}")
        P(f"   NEAREST $volume, different cap: |rho(BIG-LOQ) - rho(TINY-HIQ)| = {d_cap_same_liq:.4f}"
          f"   ($volume {C.set_index('cell').panel_dv['BIG-LOQ']:,.0f} vs "
          f"{C.set_index('cell').panel_dv['TINY-HIQ']:,.0f})")
        P(f"   within TINY, $volume alone : rho(TINY-LOQ) {cr['TINY-LOQ']:+.4f} vs "
          f"rho(TINY-HIQ) {cr['TINY-HIQ']:+.4f}")

    # ================================================================ PART D — rule 8
    P("\n" + "=" * 110)
    P("PART D — RULE 8 WALK-FORWARD: n/k chosen on 2009-2016 IS Sharpe ONLY, 2017- read ONCE")
    P("=" * 110)
    SEL = {"IS-SHARPE-MAX": ("IS_Sharpe", True), "RATIO-MAX": ("ratio", True),
           "RATIO-MIN": ("ratio", False)}
    rng8 = np.random.default_rng(SEED + 8)
    wrows = []
    for (arm, cell, k, d), sub in books.groupby(["arm", "cell", "k", "draw"]):
        if len(sub) < 2:
            continue
        anchor = float(sub.OOS_Sharpe.mean())
        picks = {sel: (sub.loc[sub[col].idxmax()] if hi else sub.loc[sub[col].idxmin()])
                 for sel, (col, hi) in SEL.items()}
        picks["RANDOM"] = sub.iloc[int(rng8.integers(len(sub)))]
        for sel, pk in picks.items():
            wrows.append(dict(arm=arm, cell=cell, k=k, draw=d, selector=sel, ratio=pk.ratio,
                              n=pk.n, q=pk.q, tau=pk.tau, OOS_Sharpe=pk.OOS_Sharpe,
                              OOS_CAGR=pk.OOS_CAGR, OOS_MaxDD=pk.OOS_MaxDD, anchor=anchor,
                              edge=pk.OOS_Sharpe - anchor, spy_OOS_S=pk.spy_OOS_S,
                              spy_OOS_CAGR=pk.spy_OOS_CAGR, spy_OOS_DD=pk.spy_OOS_DD,
                              v2_OOS_S=pk.v2_OOS_S, v2_OOS_CAGR=pk.v2_OOS_CAGR,
                              v2_OOS_DD=pk.v2_OOS_DD, pass4a=pk.pass4a, pass4b=pk.pass4b))
    W = pd.DataFrame(wrows)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    W["beat_spy"] = W.OOS_Sharpe > W.spy_OOS_S
    W["beat_v2"] = W.OOS_Sharpe > W.v2_OOS_S
    wf = (W.groupby(["selector"]).agg(sets=("edge", "size"), OOS_S=("OOS_Sharpe", "mean"),
                                      OOS_CAGR=("OOS_CAGR", "mean"), OOS_DD=("OOS_MaxDD", "mean"),
                                      edge_vs_anchor=("edge", "mean"), beat_SPY=("beat_spy", "mean"),
                                      beat_v2=("beat_v2", "mean")).reset_index()
          .sort_values("OOS_S", ascending=False))
    P(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n   comparands on the SAME panels: SPY OOS Sharpe {W.spy_OOS_S.mean():.4f} / CAGR "
      f"{W.spy_OOS_CAGR.mean():.2%} / MaxDD {W.spy_OOS_DD.mean():.2%};   RULES v2 OOS Sharpe "
      f"{W.v2_OOS_S.mean():.4f} / CAGR {W.v2_OOS_CAGR.mean():.2%} / MaxDD {W.v2_OOS_DD.mean():.2%}")
    wfa = (W.groupby(["arm", "selector"]).agg(sets=("edge", "size"), OOS_S=("OOS_Sharpe", "mean"),
                                              OOS_CAGR=("OOS_CAGR", "mean"),
                                              OOS_DD=("OOS_MaxDD", "mean"),
                                              edge=("edge", "mean"),
                                              beat_SPY=("beat_spy", "mean"),
                                              beat_v2=("beat_v2", "mean")).reset_index())
    P("\n   by arm:")
    P(wfa.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    wfa.to_csv(f"{OUT}.wf_by_arm.csv", index=False)
    P("   the rule-8 arm changes NOTHING about the rho question; PROTOCOL rule 8 requires it of "
      "every run, and it is the capital leg of this one.")

    # ================================================================ KEEP paths
    P("\n" + "=" * 110)
    P("BOTH KEEP PATHS, EVERY BOOK ROW (idea 286's committed keep_paths; rule 4)")
    P("=" * 110)
    kp = (books.groupby(["arm", "q"]).agg(rows=("pass4a", "size"), p4a=("pass4a", "sum"),
                                          p4b=("pass4b", "sum")).reset_index())
    kp["rate4b"] = kp.p4b / kp.rows
    P(kp.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  TOTAL: 4a {int(books.pass4a.sum())} of {len(books):,}; "
      f"4b {int(books.pass4b.sum())} of {len(books):,}")
    P("  These are committed CAND-n books on RANDOM sub-panels of a survivor screen; a 4b pass "
      "here is a statement about the draw, not a capital candidate.  NOTHING IS PROMOTED.")
    kp.to_csv(f"{OUT}.keeppaths.csv", index=False)

    # ================================================================ limits, then hypotheses
    P("\n" + "=" * 110)
    P("LIMITS, STATED BEFORE THE VERDICT")
    P("=" * 110)
    P("  1. The queue's LITERAL run was not executed and is not claimed to have been: no volume "
      "cache covers the BSTK pool (PART 0).  Route A changes the AXIS to keep the VARIABLE; "
      "route B keeps the axis and changes the variable to a PROXY.  Neither substitutes for the "
      "other and neither substitutes for the literal run.")
    P(f"  2. Route A's cap axis is cut on TODAY's market cap and spans only the sub-$2B screen "
      f"(TINY median ${mcE[TINY].median()/1e6:,.0f}M vs BIG ${mcE[BIG].median()/1e6:,.0f}M) — a "
      f"far shorter cap lever than 1073's SMALL-vs-BSTK.  A weaker attenuation here is expected "
      f"on those grounds alone, so the DV-vs-VOL COMPARISON, not the level, is what route A "
      f"speaks to.")
    P(f"  3. The Roll spread is a proxy and ranks {rho_valid:+.4f} against true $volume on the "
      f"{len(both)} small names carrying both.  Route B's answer is only as good as that number.")
    P("  4. Matching can only be done where the two pools OVERLAP, so every matched cell speaks "
      "for neither pool's typical name, and the tight cells do not admit every (q, k) — the "
      "infeasible list above is part of the result.")
    P(f"  5. rho is measured on {N_DRAWS} draws x {len(RATIOS)} rungs per (cell, k).  No interval "
      f"is published for it, so two closures in this table are not shown to DIFFER; only "
      f"ORDERING and SIGN are claimed (idea 1044's rule).")
    P("  6. SURVIVORSHIP (rule 9): a realised IS $volume is measured on names that survived to be "
      "screened today, so every liquidity window is doubly a survivor window.  Levels are upper "
      "bounds; the quoted results are within-grid differences on identical dates.")

    P("\n" + "=" * 110)
    P("THE DECLARED HYPOTHESES")
    P("=" * 110)
    H = []
    H.append(("H_REPRO", d5 < 0.01,
               "1073's four committed crossing rho reproduce here to |d| < 0.01",
               "; ".join(f"{c} {RHO_REP[c]:+.4f} vs {RHO1073[c]:+.4f}" for c in RHO1073)
               + f"  max|d| {d5:.2e}; shift {shift_rep:.4f} vs committed {SHIFT1073}"))
    H.append(("H_INFEAS", n_b_vol == 0,
               "the queue's LITERAL run is infeasible offline: 0 BSTK names carry a cached volume",
               f"BSTK {n_b_vol} of {len(b_stk)} carry a volume; SMALL {n_s_vol} of {len(s_stk)}; "
               f"caches present: {cached}"))
    H.append(("H_VALID", abs(rho_valid) >= 0.50,
               "the Roll spread is a usable liquidity proxy: |Spearman(Roll, -log10 $vol)| >= 0.50",
               f"{rho_valid:+.4f} over {len(both)} SMALL names carrying both"))
    H.append(("H_DVGAP", dv_ratio >= 2.0,
               "route A's axis really IS a liquidity axis: median $volume BIG / TINY >= 2.0x",
               f"BIG {dvS[BIG].median():,.0f} / TINY {dvS[TINY].median():,.0f} = {dv_ratio:.2f}x"))
    GA = gaps("DV", HEADLINE_K)
    gA = GA.get("UNMATCHED", (np.nan,))[0]
    H.append(("H_SPREAD", gA >= 0.20,
               f"the attenuation is PRESENT to be matched away on route A's UNMATCHED k="
               f"{HEADLINE_K} block (gap >= 0.20)",
               f"gap {gA:+.4f} (q=0.00 {GA['UNMATCHED'][1]:+.4f}, q=1.00 {GA['UNMATCHED'][2]:+.4f})"))
    c20 = closure.get("DV", {}).get("0.20", np.nan)
    H.append(("H_LIQ", c20 >= 50.0,
               "LIQUIDITY matching CLOSES it: at tau=0.20 the route-A gap is <= 50% of UNMATCHED",
               f"tau=0.20 closes {c20:.1f}% of the UNMATCHED gap {gA:+.4f}"))
    more = [(l, closure.get("DV", {}).get(l, np.nan), closure.get("VOL", {}).get(l, np.nan))
            for l in ("0.45", "0.30", "0.20")]
    ok_more = all((d == d and v == v and d > v) for _, d, v in more)
    H.append(("H_MORE", ok_more,
               "THE QUEUE'S QUESTION: on the SAME axis and block, LIQUIDITY closes MORE of the "
               "gap than VOL at EVERY tau",
               "; ".join(f"tau={l} DV {d:.1f}% vs VOL {v:.1f}%" for l, d, v in more)))
    seqA = [GA[l][0] for l in ("UNMATCHED", "0.45", "0.30", "0.20") if l in GA]
    H.append(("H_MONO", all(seqA[i + 1] <= seqA[i] + 1e-9 for i in range(len(seqA) - 1)),
               "the liquidity closing is MONOTONE in tau (0.45 -> 0.30 -> 0.20)",
               " -> ".join(f"{x:+.4f}" for x in seqA)))
    GB = gaps("ROLL", HEADLINE_K)
    gB = GB.get("UNMATCHED", (np.nan,))[0]
    H.append(("H_ROLLSPR", gB >= 0.20,
               f"the attenuation is present on route B's (1073's own) UNMATCHED k={HEADLINE_K} "
               f"block (gap >= 0.20)",
               f"gap {gB:+.4f} (q=0.00 {GB['UNMATCHED'][1]:+.4f}, q=1.00 {GB['UNMATCHED'][2]:+.4f})"))
    cB = closure.get("ROLL", {}).get("0.20", np.nan)
    H.append(("H_ROLL", cB >= 50.0,
               "on 1073's OWN axis a Roll-spread match closes >= 50% of that gap at tau=0.20",
               f"tau=0.20 closes {cB:.1f}%; the committed VOL match on this axis closed "
               f"{VOLCLOSE1073['0.20']}% (its best rung {max(VOLCLOSE1073.values())}%)"))
    for nm, ok, claim, det in H:
        P(f"  {nm:<11s} {'PASS' if ok else 'FAIL'}  {claim}")
        P(f"              -> {det}")
    P(f"\nHYPOTHESES: {sum(1 for _, ok, _, _ in H if ok)} of {len(H)} PASS.")
    pd.DataFrame([dict(hypothesis=n, verdict="PASS" if o else "FAIL", claim=c, detail=d)
                  for n, o, c, d in H]).to_csv(f"{OUT}.hypotheses.csv", index=False)

    P(f"\ntotal elapsed {time.time()-t0all:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
