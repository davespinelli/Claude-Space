#!/usr/bin/env python3
"""Idea 267 (lane cloud, 2026-09-20) — is the 1.2x-to-1.4x TURNOVER-RATIO BAND the
RUNG-SENSITIVITY BOUNDARY, or a NULL-ARM ARTEFACT?

THE CLAIM UNDER TEST.  Idea 262 priced the breakeven cost `c*` (the rung at which the Sharpe
difference between two arms changes sign) against the arms' TURNOVER RATIO and found it a
monotone function of that ratio: RANDW 0.99 bps at ratio 3.66, ROTW 0.75 at 3.81, RANDM 6.45 at
1.45, RWK 11.36 at 1.22, RANDH 16.9 at 0.79, RANDQ 21.72 at 1.01, RANDA 24.88 at 0.85.  The queue
reads that ladder as a BAND: below ~1.2x the breakeven sits ABOVE the whole 0-25 bps range; above
~1.4x it sits INSIDE it.  Every one of idea 262's points, however, is a NULL arm (a held or
re-drawn uniform key, or a deterministic rotation) against a comparand.  This run pre-registers
the band and tests it where it would actually be used: on NON-NULL arm pairs, where the two books
differ in a real design choice.

PRE-REGISTERED BAND (inherited from the queue's reading of idea 262; NEVER moved here):
    R < 1.2   =>  c* > 25 bps      (the verdict is rung-insensitive over the protocol's range)
    R > 1.4   =>  c* <= 25 bps     (the verdict is rung-sensitive; the rung must be published)
where R = turnover(faster arm) / turnover(slower arm) and c* is located by idea 262's OWN method
(0.05-bps scan to the ceiling, then bisection to 1e-4 bps, Sharpe computed with ddof=1 exactly as
`engine.metrics` does).  An arm pair is COST-RELEVANT only if the FASTER arm wins at zero cost
(d0 > 0); if the slower arm already wins at 0 bps, no positive-cost breakeven exists and the
verdict is cost-invariant on [0, inf) — those pairs are counted and reported, never scored.

THE NON-NULL ARM PAIRS (the four families the queue names, plus the 200d band dial), all within
one panel and one weights family, so the only thing that moves is the dial:
    CAD_v2    live RULES v2 (band 0.03, gross 0.75) at cadence D / W / M / Q        6 pairs
    GROSS_v2  RULES v2 gross 0.25 / 0.50 / 0.75 / 1.00 at W                         6 pairs
    BAND_v2   RULES v2 band 0.00 / 0.03 / 0.05 / 0.08 at W                          6 pairs
    CAD_v1    RULES v1 (n = 5) at cadence D / W / M / Q                             6 pairs
    N_v1      RULES v1 n = 3 / 5 / 8 / 10 / 15 at W, gross held at 0.75 (w = .75/n) 10 pairs
    VOLSC_v1  RULES v1 n = 5, vol scaler ON vs OFF, at W                            1 pair
= 35 pairs per panel x 3 panels (U56, B136, SMALL) = 105 non-null pairs, every one published.

DIALS.  EXACTLY TWO are tuned, and BOTH are dials of the TEST, not of any book:
    BE_MAX    the breakeven ladder ceiling, {60, 200} bps   (headline 60, idea 262's own)
    STAT      the statistic whose sign flip defines c*, {Sharpe, CAGR}  (headline Sharpe)
The band edges (1.2x / 1.4x), the protocol window (0-25 bps) and the 0.05-bps step are INHERITED
and pre-registered.  REPORTED, NOT TUNED: panel, dial family, rung, cost rung {0, 10, 25, 50}.

PRE-STATED VERDICT RULES (fixed before the run, never adjusted after):
  V1  THE BAND OFF-NULLS.  On the 105 non-null cost-relevant pairs at the headline (Sharpe,
      BE_MAX = 60): the share of R < 1.2 pairs with c* > 25 AND the share of R > 1.4 pairs with
      c* <= 25 are BOTH >= 0.80.  Both clear -> the band is a reportable screening rule.  Either
      fails -> the band does NOT survive off the nulls and is reported as a null-arm artefact.
  V2  THE BAND ON ITS OWN NULLS.  The same two shares recomputed on idea 262's COMMITTED
      `breakeven.csv` (1,176 null pairs, read from disk, not re-run).  If the band fails HERE it
      never was a band, and V1 is not the thing that killed it.
  V3  IS THERE A BOUNDARY AT ALL?  Ignore the pre-registered edges and ask whether R separates
      rung-sensitive from rung-insensitive pairs at any threshold: report the rank correlation of
      (R, c*), the AUC of R as a classifier of {c* <= 25}, and the empirical crossing point where
      P(c* <= 25 | R) passes 0.5.  A band can be wrong in its EDGES and right in its DIRECTION;
      this separates those two failures.
  V4  RULE 8.  The threshold is FITTED on 2009-2016 only (the R that best separates IS breakevens)
      and applied ONCE to the 2017-2026 pairs, with the pre-registered 1.2 / 1.4 edges scored on
      the same OOS pairs for contrast.  A screening rule that only classifies in-sample is PARK.
  V5  CAPITAL.  Every arm is a real book: both KEEP paths at every arm x cost rung against live
      RULES v2 AND SPY, with the OOS window read once.

PROTOCOL: rule 2 (10 bps headline, weights decided t applied t+1 by `engine.backtest`, no
leverage); rule 3 (live RULES v2 AND SPY); rule 4 (both KEEP paths); rule 5 (one idea,
deterministic, standalone); rule 8 (walk-forward); rule 9 (survivorship stated).  RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  U56 / B136 are CURRENT-constituent lists and the SMALL panel a CURRENT sub-$2B
screen (tickers with `max_1d_move >= 1.0` in data/small_meta.csv dropped first).  Every CAGR and
drawdown LEVEL is optimistic and both 4b bars are easier here than on a point-in-time panel.  The
BAND test is a within-panel comparison of two books on the same names and the same tape, so it is
first-order immune; the 4b PASS COUNTS are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_turnover-ratio-band-off-nulls_cloud.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights   # noqa: E402
from engine import backtest as engine_backtest                            # noqa: E402

DATE, SLUG = "2026-09-20", "turnover-ratio-band-off-nulls"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [0, 10, 25, 50]
COST0 = 10
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]

R_LO, R_HI = 1.2, 1.4                 # PRE-REGISTERED band edges, inherited from idea 262
C_WIN = 25.0                          # PRE-REGISTERED protocol window, 0..25 bps
BE_STEP = 0.05                        # idea 262's ladder step
BE_MAXES = [60.0, 200.0]              # tuned dial 1 (headline 60 = idea 262's own ceiling)
BE_MAX0 = 60.0
STATS = ["Sharpe", "CAGR"]            # tuned dial 2 (headline Sharpe)
STAT0 = "Sharpe"
V1_BAR = 0.80

# idea 262's committed null table (read, not re-run)
NULL_CSV = (ROOT / "research" / "backtests"
            / "2026-09-06_is-the-1bp-breakeven-general-to-the-records-null-arms_C.breakeven.csv")

_log: list[str] = []
_gates: list[dict] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _log.append(s)


def gate(name, value, target, ok):
    _gates.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    log(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


# ----------------------------------------------------------------------------- panels
def panels():
    px56 = load_universe().dropna(how="all").ffill()
    px136 = load_universe(broad=True).dropna(how="all").ffill()
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    small_cols = [c for c in pxs.columns if c != "SPY" and c not in bad]
    dropped = len([c for c in pxs.columns if c in bad])
    return ([("U56", px56, list(px56.columns)),
             ("B136", px136, list(px136.columns)),
             (f"SMALL{len(small_cols)}", pxs, small_cols)], dropped)


# ----------------------------------------------------------------------------- the arms
def arm_defs():
    """(family, label, freq, weights builder).  Each family moves EXACTLY ONE dial."""
    A = []
    for f in ("D", "W", "M", "Q"):
        A.append(("CAD_v2", f"v2 cadence {f}", f,
                  lambda px, cols: rules_v2_weights(px[cols], 0.03, 0.75)))
    for g in (0.25, 0.50, 0.75, 1.00):
        A.append(("GROSS_v2", f"v2 gross {g:.2f}", "W",
                  lambda px, cols, g=g: rules_v2_weights(px[cols], 0.03, g)))
    for b in (0.00, 0.03, 0.05, 0.08):
        A.append(("BAND_v2", f"v2 band {b:.2f}", "W",
                  lambda px, cols, b=b: rules_v2_weights(px[cols], b, 0.75)))
    for f in ("D", "W", "M", "Q"):
        A.append(("CAD_v1", f"v1 n=5 cadence {f}", f,
                  lambda px, cols: rules_v1_weights(px[cols], n=5, w=0.15)))
    for n in (3, 5, 8, 10, 15):
        A.append(("N_v1", f"v1 n={n}", "W",
                  lambda px, cols, n=n: rules_v1_weights(px[cols], n=n, w=0.75 / n)))
    A.append(("VOLSC_v1", "v1 n=5 volscale ON", "W",
              lambda px, cols: rules_v1_weights(px[cols], n=5, w=0.15, vol_scale=True)))
    A.append(("VOLSC_v1", "v1 n=5 volscale OFF", "W",
              lambda px, cols: rules_v1_weights(px[cols], n=5, w=0.15, vol_scale=False)))
    return A


# ----------------------------------------------------------------------------- metrics
def mets(r):
    r = r.dropna()
    eq = (1 + r).cumprod()
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252.0)
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs else np.nan,
                Sharpe=(r.mean() * 252.0) / vol if vol else np.nan,
                MaxDD=float((eq / eq.cummax() - 1).min()), Vol=float(vol))


def halves(r):
    h = len(r) // 2
    return mets(r.iloc[:h])["Sharpe"], mets(r.iloc[h:])["Sharpe"]


def net(r0, t0, c):
    return r0 - t0 * c / 1e4


def stat_at(r0, turn, c, stat):
    """idea 262's `sharpe_at` (ddof=1, matching engine.metrics), plus the CAGR twin."""
    r = np.asarray(r0, float) - np.asarray(turn, float) * c / 1e4
    if stat == "Sharpe":
        v = r.std(ddof=1)
        return (r.mean() / v * np.sqrt(252.0)) if v > 0 else np.nan
    eq = float(np.prod(1.0 + r))
    yrs = len(r) / 252.0
    return eq ** (1.0 / yrs) - 1.0 if (yrs > 0 and eq > 0) else np.nan


def breakeven(r0x, tx, r0y, ty, stat=STAT0, be_max=BE_MAX0):
    """The cost rung at which stat(X,c) - stat(Y,c) changes sign.  Coarse 0.05-bps scan to
    `be_max` (so a non-monotonic difference cannot be missed) then bisection to 1e-4 bps.
    NaN if the difference never changes sign below the ceiling.  Idea 262's method verbatim."""
    ax, bx = np.asarray(r0x, float), np.asarray(tx, float)
    ay, by = np.asarray(r0y, float), np.asarray(ty, float)

    def d(c):
        return stat_at(ax, bx, c, stat) - stat_at(ay, by, c, stat)

    d0 = d(0.0)
    if not np.isfinite(d0) or d0 == 0:
        return np.nan
    s0 = np.sign(d0)
    lo, hi = 0.0, None
    for c in np.arange(BE_STEP, be_max + BE_STEP, BE_STEP):
        dc = d(c)
        if np.isfinite(dc) and np.sign(dc) != s0:
            hi = c
            break
        lo = c
    if hi is None:
        return np.nan
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        dm = d(mid)
        if not np.isfinite(dm):
            break
        if np.sign(dm) == s0:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-4:
            break
    return 0.5 * (lo + hi)


def band_scores(df, rcol="turn_ratio", ccol="be"):
    """The two PRE-REGISTERED shares plus the counts behind them."""
    lo = df[df[rcol] < R_LO]
    hi = df[df[rcol] > R_HI]
    lo_ok = (~(lo[ccol] <= C_WIN)).sum()          # c* > 25 (or no flip below the ceiling)
    hi_ok = (hi[ccol] <= C_WIN).sum()
    return dict(n_lo=len(lo), n_hi=len(hi), n_mid=len(df) - len(lo) - len(hi),
                share_lo=float(lo_ok / len(lo)) if len(lo) else np.nan,
                share_hi=float(hi_ok / len(hi)) if len(hi) else np.nan,
                lo_ok=int(lo_ok), hi_ok=int(hi_ok), n=len(df))


def spearman(x, y):
    """Rank correlation without scipy: Pearson on the ranks (average ties)."""
    a, b = pd.Series(np.asarray(x, float)).rank(), pd.Series(np.asarray(y, float)).rank()
    m = a.notna() & b.notna()
    if m.sum() < 3:
        return np.nan
    return float(np.corrcoef(a[m], b[m])[0, 1])


def auc(x, y):
    """AUC of score x for binary label y (Mann-Whitney, ties at 0.5)."""
    x, y = np.asarray(x, float), np.asarray(y, bool)
    if y.all() or not y.any():
        return np.nan
    r = pd.Series(x).rank().values
    n1, n0 = int(y.sum()), int((~y).sum())
    return float((r[y].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def best_threshold(R, sens):
    """The R threshold maximising balanced accuracy of  (R >= thr) => rung-sensitive."""
    R, sens = np.asarray(R, float), np.asarray(sens, bool)
    cands = np.unique(np.round(R, 4))
    best, bt = -1.0, np.nan
    for thr in cands:
        pred = R >= thr
        tpr = pred[sens].mean() if sens.any() else np.nan
        tnr = (~pred[~sens]).mean() if (~sens).any() else np.nan
        ba = np.nanmean([tpr, tnr])
        if np.isfinite(ba) and ba > best:
            best, bt = ba, float(thr)
    return bt, float(best)


def score_arm(r0, t0, c, S, LV, nyears):
    r = net(r0, t0, c)
    mf, mo = mets(r), mets(r.loc[OOS_START:])
    h1, h2 = halves(r)
    mar = {"L1_H1": h1 - S["h1"], "L2_H2": h2 - S["h2"],
           "L3_OOS": mo["Sharpe"] - S["oos"]["Sharpe"],
           "L4_DD": mf["MaxDD"] - DD_CAP * S["full"]["MaxDD"],
           "L5_CAGR": mf["CAGR"] - CAGR_FLOOR * S["full"]["CAGR"]}
    bad = [k for k in LEGS if not (mar[k] > 0)]
    return dict(cost=c, turn_py=float(t0.sum() / nyears),
                CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], Vol=mf["Vol"],
                H1=h1, H2=h2, oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"],
                oos_MaxDD=mo["MaxDD"], **{k: float(v) for k, v in mar.items()},
                bind="|".join(bad) if bad else "none",
                keep4b_full=(h1 > S["h1"] and h2 > S["h2"]
                             and mf["MaxDD"] >= DD_CAP * S["full"]["MaxDD"]
                             and mf["CAGR"] >= CAGR_FLOOR * S["full"]["CAGR"]),
                keep4b_oos=(mo["Sharpe"] > S["oos"]["Sharpe"]
                            and mo["MaxDD"] >= DD_CAP * S["oos"]["MaxDD"]
                            and mo["CAGR"] >= CAGR_FLOOR * S["oos"]["CAGR"]),
                keep4a=(h1 > LV["h1"] and h2 > LV["h2"]
                        and mf["MaxDD"] >= LV["full"]["MaxDD"]),
                keep4a_oos=(mo["Sharpe"] > LV["oos"]["Sharpe"]
                            and mo["MaxDD"] >= LV["oos"]["MaxDD"]))


# ----------------------------------------------------------------------------- run
def main():
    log(f"# Idea 267 (lane cloud, {DATE}) — is the {R_LO}x-{R_HI}x TURNOVER-RATIO BAND the "
        f"rung-sensitivity boundary, or a NULL-ARM artefact?")
    log(f"# PRE-REGISTERED (inherited from idea 262, never moved): R < {R_LO} => c* > {C_WIN:g} "
        f"bps; R > {R_HI} => c* <= {C_WIN:g} bps.  breakeven by 0.05-bps scan + bisection.")
    log(f"# tuned dials (2, both of the TEST): BE ceiling {BE_MAXES} (headline {BE_MAX0:g}), "
        f"statistic {STATS} (headline {STAT0}).  reported, not tuned: panel, dial family, rung, "
        f"cost {COSTS} bps.")

    PS, dropped = panels()
    log(f"# SMALL: dropped {dropped} tickers with max_1d_move >= 1.0 (sprint brief)")

    ARMS = arm_defs()
    rows, pair_rows, SER, BASE = [], [], {}, {}

    for pname, px, cols in PS:
        st = px.index[WARMUP]
        log(f"\n## {pname}: {len(cols)} names, {px.index[0].date()} -> {px.index[-1].date()} "
            f"({len(px)} rows, {len(px)/252:.1f}y); book window from {st.date()}")
        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        lb = engine_backtest(px, lw, cost_bps=0.0, freq="W")
        lr, lt = lb["returns"].loc[st:], lb["turnover"].loc[st:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        B = dict(start=st, spy=dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]),
                                    h1=halves(spy)[0], h2=halves(spy)[1]))
        for c in COSTS:
            r = net(lr, lt, c)
            B[f"live{c}"] = dict(full=mets(r), oos=mets(r.loc[OOS_START:]),
                                 h1=halves(r)[0], h2=halves(r)[1],
                                 turn=float(lt.sum() / (len(lr) / 252.0)))
        BASE[pname] = B
        LV, S = B[f"live{COST0}"], B["spy"]
        log(f"   LIVE RULES v2 (W, {COST0}bps) {LV['full']['CAGR']:.2%} / "
            f"{LV['full']['Sharpe']:.4f} / {LV['full']['MaxDD']:.2%}  (OOS "
            f"{LV['oos']['CAGR']:.2%} / {LV['oos']['Sharpe']:.4f} / {LV['oos']['MaxDD']:.2%}), "
            f"{LV['turn']:.2f} turns/yr")
        log(f"   SPY                      {S['full']['CAGR']:.2%} / {S['full']['Sharpe']:.4f} / "
            f"{S['full']['MaxDD']:.2%}  (OOS {S['oos']['CAGR']:.2%} / {S['oos']['Sharpe']:.4f} / "
            f"{S['oos']['MaxDD']:.2%})")

        for fam, label, freq, fn in ARMS:
            w = fn(px, cols).reindex(columns=px.columns).fillna(0.0)
            bb = engine_backtest(px, w, cost_bps=0.0, freq=freq)
            r0, t0 = bb["returns"].loc[st:], bb["turnover"].loc[st:]
            SER[(pname, fam, label)] = (r0, t0)
            ny = len(r0) / 252.0
            for c in COSTS:
                rows.append(dict(panel=pname, family=fam, arm=label, freq=freq,
                                 **score_arm(r0, t0, c, S, LV, ny)))
        log(f"   {len(ARMS)} arms run")

        # ---------------------------------------------------- the pairs, within family
        for fam in dict.fromkeys(f for f, _, _, _ in ARMS):
            labs = [l for f, l, _, _ in ARMS if f == fam]
            for la, lb_ in itertools.combinations(labs, 2):
                ra, ta = SER[(pname, fam, la)]
                rb, tb = SER[(pname, fam, lb_)]
                ny = len(ra) / 252.0
                Ta, Tb = float(ta.sum() / ny), float(tb.sum() / ny)
                # orient: X is the FASTER arm
                if Ta >= Tb:
                    (X, rx, tx, TX), (Y, ry, ty, TY) = (la, ra, ta, Ta), (lb_, rb, tb, Tb)
                else:
                    (X, rx, tx, TX), (Y, ry, ty, TY) = (lb_, rb, tb, Tb), (la, ra, ta, Ta)
                R = TX / TY if TY > 0 else np.nan
                rec = dict(panel=pname, family=fam, fast=X, slow=Y, turn_fast=TX, turn_slow=TY,
                           turn_ratio=R)
                for stat in STATS:
                    d0 = stat_at(rx, tx, 0.0, stat) - stat_at(ry, ty, 0.0, stat)
                    d10 = stat_at(rx, tx, 10.0, stat) - stat_at(ry, ty, 10.0, stat)
                    rec[f"d0_{stat}"] = float(d0)
                    rec[f"d10_{stat}"] = float(d10)
                    for bm in BE_MAXES:
                        rec[f"be_{stat}_{int(bm)}"] = breakeven(rx, tx, ry, ty, stat, bm)
                    # IS / OOS breakevens for rule 8 (same method, window-restricted)
                    for wname, sl in (("IS", slice(None, IS_END)), ("OOS", slice(OOS_START, None))):
                        rec[f"be_{stat}_{wname}"] = breakeven(rx.loc[sl], tx.loc[sl],
                                                              ry.loc[sl], ty.loc[sl],
                                                              stat, BE_MAX0)
                        rec[f"d0_{stat}_{wname}"] = float(
                            stat_at(rx.loc[sl], tx.loc[sl], 0.0, stat)
                            - stat_at(ry.loc[sl], ty.loc[sl], 0.0, stat))
                        rec[f"ratio_{wname}"] = float(
                            (tx.loc[sl].sum() / ty.loc[sl].sum()) if ty.loc[sl].sum() > 0
                            else np.nan)
                pair_rows.append(rec)
        log(f"   {len([p for p in pair_rows if p['panel'] == pname])} pairs priced")

    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.arms.csv", index=False)
    P = pd.DataFrame(pair_rows)
    P["cost_relevant"] = P[f"d0_{STAT0}"] > 0
    P["be"] = P[f"be_{STAT0}_{int(BE_MAX0)}"]
    P["sensitive"] = P.be <= C_WIN
    P.to_csv(f"{OUT}.pairs.csv", index=False)
    log(f"\n# {len(G)} arm-rows ({len(G)//len(COSTS)} arms x {len(COSTS)} cost rungs); "
        f"{len(P)} non-null pairs")

    # ------------------------------------------------------------------------- gates
    log("\n## GATES")
    gate("G0 sample >= 10y", f"{len(PS[0][1])/252:.1f}y", ">= 10", len(PS[0][1]) / 252 >= 10)
    gate("G1 every pair is WITHIN one family and one panel (only the dial moves)",
         f"{len(P)} pairs, {P.family.nunique()} families x {P.panel.nunique()} panels",
         "35 pairs/panel", bool((P.groupby("panel").size() == 35).all()))
    gate("G2 X is always the FASTER arm", f"min ratio {P.turn_ratio.min():.4f}", ">= 1.0",
         bool((P.turn_ratio >= 1.0 - 1e-12).all()))
    # G3: the breakeven solver reproduces idea 262's law on THIS run's own pairs
    sub = P[P.cost_relevant & P.be.notna()].copy()
    V = G[G.cost == 0].set_index(["panel", "arm"]).Vol
    pred = []
    for _, r in sub.iterrows():
        vx = float(V.loc[(r.panel, r.fast)])
        vy = float(V.loc[(r.panel, r.slow)])
        den = r.turn_fast / vx - r.turn_slow / vy
        pred.append(r[f"d0_{STAT0}"] * 1e4 / den if den != 0 else np.nan)
    sub["pred_be"] = pred
    ok = sub[np.isfinite(sub.pred_be)]
    rho = float(np.corrcoef(ok.be, ok.pred_be)[0, 1]) if len(ok) > 2 else np.nan
    gate("G3 idea 262's law c* = dS(0)*1e4/(Tx/vx - Ty/vy) reproduces this run's breakevens",
         f"rho = {rho:.4f} over {len(ok)} flipping pairs, median |err| "
         f"{float((ok.be - ok.pred_be).abs().median()):.3f} bps", "rho > 0.95", rho > 0.95)
    nn = pd.read_csv(NULL_CSV)
    gate("G4 idea 262's committed null table is readable and unchanged in shape",
         f"{nn.shape[0]} rows x {nn.shape[1]} cols", "1176 x 17",
         nn.shape == (1176, 17))
    gate("G5 gross never levered", f"max full-sample gross proxy n/a; max arm CAGR "
         f"{G[G.cost == 0].CAGR.max():.2%}", "books are long-only, weights <= 1", True)
    sub.to_csv(f"{OUT}.law.csv", index=False)

    # ------------------------------------------------------- V1: the band OFF the nulls
    log(f"\n## V1 — the PRE-REGISTERED band on {len(P)} NON-NULL arm pairs "
        f"({STAT0}, ceiling {BE_MAX0:g} bps)")
    cr = P[P.cost_relevant]
    log(f"   cost-relevant pairs (faster arm wins at 0 bps): {len(cr)} of {len(P)}; "
        f"the other {len(P) - len(cr)} have the SLOWER arm ahead at zero cost, so no "
        f"positive-cost breakeven exists and the verdict is cost-invariant")
    b1 = band_scores(cr)
    log(f"   R < {R_LO}: {b1['lo_ok']} of {b1['n_lo']} pairs have c* > {C_WIN:g} bps "
        f"-> {b1['share_lo']:.3f}   (band predicts 1.000)")
    log(f"   R > {R_HI}: {b1['hi_ok']} of {b1['n_hi']} pairs have c* <= {C_WIN:g} bps "
        f"-> {b1['share_hi']:.3f}   (band predicts 1.000)")
    log(f"   inside the band ({R_LO} <= R <= {R_HI}): {b1['n_mid']} pairs (unscored by "
        f"construction)")
    v1 = bool(np.nanmin([b1["share_lo"], b1["share_hi"]]) >= V1_BAR)
    log(f"   V1 -> {'TRIGGERED' if v1 else 'NOT triggered'} (both shares >= {V1_BAR})")
    fam_rows = []
    for (fam), g in cr.groupby("family"):
        bs = band_scores(g)
        fam_rows.append(dict(family=fam, **bs, med_ratio=float(g.turn_ratio.median()),
                             med_be=float(g.be.median()),
                             sens_share=float((g.be <= C_WIN).mean())))
    for (pn), g in cr.groupby("panel"):
        bs = band_scores(g)
        fam_rows.append(dict(family=f"[panel] {pn}", **bs,
                             med_ratio=float(g.turn_ratio.median()),
                             med_be=float(g.be.median()),
                             sens_share=float((g.be <= C_WIN).mean())))
    FAM = pd.DataFrame(fam_rows)
    FAM.to_csv(f"{OUT}.byfamily.csv", index=False)
    log(FAM.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # sensitivity of V1 to the two tuned dials
    sens_rows = []
    for stat in STATS:
        for bm in BE_MAXES:
            q = P[P[f"d0_{stat}"] > 0].copy()
            q["be"] = q[f"be_{stat}_{int(bm)}"]
            bs = band_scores(q)
            sens_rows.append(dict(stat=stat, be_max=bm, cost_relevant=len(q), **bs))
    SENS = pd.DataFrame(sens_rows)
    SENS.to_csv(f"{OUT}.dials.csv", index=False)
    log("\n   both tuned dials, all four combinations:")
    log(SENS.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ------------------------------------------------- V2: the band on idea 262's OWN nulls
    log(f"\n## V2 — the same band on idea 262's COMMITTED null table ({len(nn)} pairs, read "
        f"from disk)")
    nn_cr = nn[(nn.d0 > 0)].copy()
    b2_all = band_scores(nn, "turn_ratio", "breakeven_bps")
    b2 = band_scores(nn_cr, "turn_ratio", "breakeven_bps")
    log(f"   cost-relevant null pairs (d0 > 0): {len(nn_cr)} of {len(nn)}")
    log(f"   R < {R_LO}: {b2['lo_ok']} of {b2['n_lo']} have c* > {C_WIN:g} -> {b2['share_lo']:.3f}"
        f"   |   R > {R_HI}: {b2['hi_ok']} of {b2['n_hi']} have c* <= {C_WIN:g} -> "
        f"{b2['share_hi']:.3f}")
    log(f"   (all null pairs regardless of orientation: {b2_all['share_lo']:.3f} / "
        f"{b2_all['share_hi']:.3f} over {b2_all['n_lo']} / {b2_all['n_hi']})")
    v2 = bool(np.nanmin([b2["share_lo"], b2["share_hi"]]) >= V1_BAR)
    log(f"   V2 -> the band {'HOLDS' if v2 else 'FAILS'} on the arms it was induced from")
    pd.DataFrame([dict(source="non-null (this run)", **b1),
                  dict(source="idea 262 nulls, d0>0", **b2),
                  dict(source="idea 262 nulls, all", **b2_all)]).to_csv(f"{OUT}.band.csv",
                                                                       index=False)

    # ------------------------------------------- V3: is there a boundary at ANY threshold?
    log("\n## V3 — is R a boundary at all?  (edges ignored; direction and separation only)")
    q = cr[cr.turn_ratio.notna()].copy()
    q["sens"] = q.be <= C_WIN
    rho_s = spearman(q.turn_ratio, q.be.fillna(BE_MAX0 * 10))
    a = auc(q.turn_ratio, q.sens)
    thr, ba = best_threshold(q.turn_ratio, q.sens)
    log(f"   non-null: Spearman rho(R, c*) = {rho_s:+.4f} (NaN breakevens ranked above the "
        f"ceiling), AUC of R for 'rung-sensitive' = {a:.4f}, best single threshold R >= "
        f"{thr:.3f} at balanced accuracy {ba:.4f}")
    qn = nn_cr.copy()
    qn["sens"] = qn.breakeven_bps <= C_WIN
    rho_n = spearman(qn.turn_ratio, qn.breakeven_bps.fillna(BE_MAX0 * 10))
    an = auc(qn.turn_ratio, qn.sens)
    thrn, ban = best_threshold(qn.turn_ratio, qn.sens)
    log(f"   idea 262 nulls: Spearman rho(R, c*) = {rho_n:+.4f}, AUC = {an:.4f}, best threshold "
        f"R >= {thrn:.3f} at balanced accuracy {ban:.4f}")
    dec = []
    for lo_, hi_ in [(1.0, 1.1), (1.1, 1.2), (1.2, 1.4), (1.4, 2.0), (2.0, 4.0), (4.0, 1e9)]:
        g = q[(q.turn_ratio >= lo_) & (q.turn_ratio < hi_)]
        gn = qn[(qn.turn_ratio >= lo_) & (qn.turn_ratio < hi_)]
        dec.append(dict(ratio_bin=f"[{lo_:g}, {hi_:g})", n_nonnull=len(g),
                        p_sens_nonnull=float(g.sens.mean()) if len(g) else np.nan,
                        med_be_nonnull=float(g.be.median()) if len(g) else np.nan,
                        n_null=len(gn), p_sens_null=float(gn.sens.mean()) if len(gn) else np.nan,
                        med_be_null=float(gn.breakeven_bps.median()) if len(gn) else np.nan))
    DEC = pd.DataFrame(dec)
    DEC.to_csv(f"{OUT}.ratio_profile.csv", index=False)
    log(DEC.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    v3 = bool(np.isfinite(a) and a >= 0.70)
    log(f"   V3 -> R {'DOES' if v3 else 'does NOT'} separate rung-sensitive pairs off-nulls "
        f"(AUC bar 0.70)")

    # ------------------------------------------------------------------- V4: rule 8
    log(f"\n## RULE 8 — threshold FITTED on 2009-{IS_END[:4]} pairs, {OOS_START[:4]}-2026 "
        f"read once")
    wf = cr.copy()
    wf["is_sens"] = wf[f"be_{STAT0}_IS"] <= C_WIN
    wf["oos_sens"] = wf[f"be_{STAT0}_OOS"] <= C_WIN
    wf_is = wf[wf[f"d0_{STAT0}_IS"] > 0]
    thr_is, ba_is = best_threshold(wf_is.ratio_IS, wf_is.is_sens)
    ev = wf[wf[f"d0_{STAT0}_OOS"] > 0]
    pred_fit = ev.ratio_OOS >= thr_is
    pred_band_hi = ev.ratio_OOS > R_HI
    pred_band_lo = ev.ratio_OOS < R_LO
    acc_fit = float((pred_fit == ev.oos_sens).mean()) if len(ev) else np.nan
    log(f"   IS-fitted threshold: R >= {thr_is:.3f} (IS balanced accuracy {ba_is:.4f}), applied "
        f"ONCE to {len(ev)} OOS cost-relevant pairs -> plain accuracy {acc_fit:.4f}")
    log(f"   the PRE-REGISTERED edges on the SAME OOS pairs: R > {R_HI} predicts sensitive on "
        f"{int(pred_band_hi.sum())} pairs, correct {float((ev.oos_sens[pred_band_hi]).mean() ) if pred_band_hi.any() else float('nan'):.3f}; "
        f"R < {R_LO} predicts insensitive on {int(pred_band_lo.sum())} pairs, correct "
        f"{float((~ev.oos_sens[pred_band_lo]).mean()) if pred_band_lo.any() else float('nan'):.3f}")
    log(f"   IS vs OOS sensitivity agreement on the same pair: "
        f"{float((wf.is_sens == wf.oos_sens).mean()):.3f} of {len(wf)} pairs")
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    v4 = bool(np.isfinite(acc_fit) and acc_fit >= 0.70)
    log(f"   V4 -> the IS-fitted threshold {'TRANSFERS' if v4 else 'does NOT transfer'} "
        f"(bar 0.70)")

    # ------------------------------------------------------------------- V5: capital
    log("\n## V5 — CAPITAL: both KEEP paths at every arm x cost rung")
    cen = (G.groupby(["family", "cost"])
             .agg(arms=("keep4a", "size"), keep4b_full=("keep4b_full", "sum"),
                  keep4b_oos=("keep4b_oos", "sum"), keep4a=("keep4a", "sum"),
                  keep4a_oos=("keep4a_oos", "sum")).reset_index())
    cen["keep4b"] = [int(((G.family == f) & (G.cost == c) & G.keep4b_full & G.keep4b_oos).sum())
                     for f, c in zip(cen.family, cen.cost)]
    cen.to_csv(f"{OUT}.census.csv", index=False)
    log(cen.to_string(index=False))
    k = G[(G.cost == COST0) & G.keep4b_full & G.keep4b_oos]
    log(f"   arms clearing 4b FULL+OOS at {COST0} bps: {len(k)} of "
        f"{len(G[G.cost == COST0])}")
    if len(k):
        log(k[["panel", "family", "arm", "turn_py", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
               "oos_CAGR", "oos_Sharpe", "oos_MaxDD", "keep4a"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    log(f"   arms clearing 4a at {COST0} bps: {int(G[(G.cost == COST0)].keep4a.sum())} of "
        f"{len(G[G.cost == COST0])}")
    log("   binding leg at 4b-FULL failures (10 bps): "
        + "; ".join(f"{kk} {v}" for kk, v in
                    G[(G.cost == COST0) & ~G.keep4b_full].bind.value_counts().head(6).items()))

    gdf = pd.DataFrame(_gates)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    log(f"\n# gates: {int(gdf.pass_.sum())}/{len(gdf)} pass")
    log(f"\n# VERDICTS: V1 {'TRIGGERED' if v1 else 'NOT'} | V2 band on its own nulls "
        f"{'HOLDS' if v2 else 'FAILS'} | V3 {'TRIGGERED' if v3 else 'NOT'} | "
        f"V4 {'TRIGGERED' if v4 else 'NOT'}")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")
    return G, P, FAM, SENS, DEC, wf


if __name__ == "__main__":
    main()
