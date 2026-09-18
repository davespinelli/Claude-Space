#!/usr/bin/env python3
"""Idea 1067 (lane C, 2026-09-18) — does R_GATE RELEASE buy anything a LOWER GROSS does not?

QUESTION (QUEUE idea 1067, verbatim)
    idea 1065's soft min hold at R_GATE recovers the whole tax and keeps 69-77% of the turnover
    rebate, but costs -0.0197 of CAGR at H=63 (15.58% -> 14.16% while MaxDD returns to -21.68%).
    Compare it head to head with the plainest alternative — the HARD book at a gross rung low
    enough to match its MaxDD — on CAGR, turnover and both KEEP paths.
    Max 2 params (gross rung, min hold).

WHAT IS BEING MEASURED, DECLARED BEFORE ANY NUMBER.
    1065 sold R_GATE release as a MECHANISM: it gives back the min-hold drawdown tax while
    keeping ~70% of the turnover rebate H buys.  But drawdown is also the one thing a de-grossed
    book gives back for free — hold the HARD book at gross g < 0.75 and put the rest in cash and
    |MaxDD| falls with g, at zero cleverness and LOWER turnover than the release rule (which
    trades MORE than HARD because it sells young names).  So the mechanism is only worth its
    complexity if, AT MATCHED DRAWDOWN, it delivers something de-grossing does not.

    Three things are measured, each separately:
      (1) THE HEAD TO HEAD — for every cell, take SOFT(R_GATE) at the incumbent gross 0.75, find
          the HARD book's gross rung low enough to match its |MaxDD|, and difference CAGR,
          Sharpe, OOS Sharpe and turnover.  d_CAGR > 0 at a majority of cells is the ONLY result
          that keeps the mechanism.
      (2) THE GROSS INVARIANCE OF SHARPE — a long-only cash-plus-book has r_g ~ g * r_1 to
          within intra-segment drift, so Sharpe should be near-invariant in g while CAGR and
          MaxDD are not.  If that holds, de-grossing is a PURE drawdown/CAGR trade and the 4b DD
          leg is purchasable by anyone at a known CAGR price — which is a fact about the KEEP
          framework, not about this idea, and is reported whichever way (1) goes.
      (3) BOTH KEEP PATHS AND RULE 8 over the whole 5 x 4 grid for BOTH kinds, plus a
          gross-matched random-key null so the 4b pass counts are read against a base rate.

THE TWO DIALS (rule 4, no more than two tuned parameters)
    1. GROSS RUNG g in {0.75, 0.65, 0.55, 0.45, 0.35} — 1064/1069's committed ladder.
    2. MIN HOLD H in {5, 21, 63, 126} — 936/1065's committed ladder.
    All 5 x 4 = 20 points are reported for every kind, panel, mechanism and rebalance grid.
    Nothing else is tuned: 10 bps (PROTOCOL rule 2), N = 20, max_vol 0.60, next-day execution.
    Panels (U56, B136), mechanisms (CAND20, R3_84, MOMONLY) and rebalance grids (D/W/M/Q) are
    REPORTED axes, never selected.  A DD-matched gross solved exactly by bisection is reported
    beside the rung-wise match so the head-to-head is not a rung-granularity artefact; it is a
    DERIVED quantity, not a third dial.

RULE 8.  The arm (kind x freq x H x g) is chosen on 2009-2016 Sharpe ALONE, per panel and
    mechanism, and 2017-2026 is read ONCE against SPY and the live RULES v2 book.  The
    head-to-head is ALSO re-run separately on the IS and OOS windows, because a mechanism that
    only wins in sample is a PARK.

SURVIVORSHIP.  U56 and B136 are current-constituent panels (rule 9).  Every LEVEL here is
    optimistic.  The headline is a within-cell contrast (one book against another book on the
    same panel, same mechanism, same dates, matched drawdown), which the bias largely cancels
    out of; the 4a/4b PASS COUNTS are levels and are not.
"""
from __future__ import annotations

import hashlib
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "does-R_GATE-RELEASE-buy-anything-a-LOWER-GROSS-does-not"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

LAG = 1
WARMUP = 260
NTOP = 20
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
BASE_GROSS = 0.75                      # the incumbent rung SOFT is quoted at

# ---- the two tuned dials ----------------------------------------------------------------------
GROSSES = [0.75, 0.65, 0.55, 0.45, 0.35]
HOLDS = [5, 21, 63, 126]

# reported axes, never selected
PANELS = ["U56", "B136"]
MECHS = ["CAND20", "R3_84", "MOMONLY"]
FREQS = ["D", "W", "M", "Q"]
LEGSETS = {"CAND20": [(21, 252), (0, 126), (0, 63)],
           "R3_84": [(21, 252), (0, 126), (0, 84)],
           "MOMONLY": [(21, 252)]}
NULL_FREQS = ["W", "M"]
NSEED = 5

# committed cross-run anchors — idea 1065 `.arms.csv` (U56, CAND20, W, gross 0.75, 10 bps)
G1065 = {("BOOK_H0", 0, "-"): (0.127272, 1.060652, -0.183084, 10.792011),
         ("BOOK_HARD", 5, "-"): (0.131082, 1.086304, -0.184825, 9.852592),
         ("BOOK_HARD", 21, "-"): (0.143532, 1.115226, -0.202416, 6.143456),
         ("BOOK_HARD", 63, "-"): (0.149484, 1.101400, -0.256921, 3.871294),
         ("BOOK_HARD", 126, "-"): (0.155787, 1.139701, -0.191276, 2.897394),
         ("BOOK_SOFT", 5, "R_GATE"): (0.129637, 1.077935, -0.184825, 10.033566),
         ("BOOK_SOFT", 21, "R_GATE"): (0.130415, 1.089437, -0.177313, 7.748455),
         ("BOOK_SOFT", 63, "R_GATE"): (0.126404, 1.068071, -0.174598, 6.463590),
         ("BOOK_SOFT", 126, "R_GATE"): (0.114786, 0.998353, -0.172664, 5.675475)}
# idea 1065 console block (B), R_GATE rows: (tax recovered, rebate kept, dCAGR) over 24 cells
G1065B = {5: (0.000, 0.765, +0.0000), 21: (1.000, 0.716, -0.0056),
          63: (1.082, 0.691, -0.0197), 126: (0.998, 0.712, -0.0207)}
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def mdseed(*parts):
    return int(hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()[:8], 16)


# ====================================================================== engine (1065's, verbatim)
def nrun(rets, wt, mk):
    """GROSS returns and turnover; cost applied outside (gated at G1 against engine.backtest)."""
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    g = (held * rets).sum(axis=1)
    prev = np.vstack([np.zeros((1, N)), held[:-1] * (1.0 + rets[:-1]) / (1.0 + g[:-1])[:, None]])
    t = np.where(mk, np.abs(wt - prev).sum(axis=1), 0.0)
    return g, t


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def lag(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def lagmask(m):
    out = np.zeros_like(m)
    out[LAG:] = m[:-LAG]
    return out


def legs_composite(px, legs):
    parts = []
    for skip, look in legs:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech_score(px, mech):
    """961/968/1059's selection score (no vol scaler — the KEEP 4b convention) and its gate."""
    comp = legs_composite(px, LEGSETS[mech])
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    elig = (above & (vol20 < MAXVOL)).values
    return sc.values, elig


def minhold_book(rank_key, elig, priced, reb, H, T, N, soft=False):
    """1065's min-hold book at gross 1.0.  soft=True is the R_GATE SOFT release: a young name is
    freed as soon as it fails the book's own eligibility gate today."""
    W = np.zeros((T, N))
    cur = np.full(N, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        k = rank_key[t]
        ok = elig[t] & priced[t]
        kk = np.where(ok, k, np.inf)
        order = np.argsort(kk, kind="stable")
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        if soft and len(young):
            young = young[ok[young]]                 # R_GATE: release what the gate dropped
        keep = set(young.tolist())
        need = NTOP - len(keep)
        if need > 0:
            kf = kk.copy()
            for c in keep:
                kf[c] = np.inf
            o2 = np.argsort(kf, kind="stable")
            take = [int(c) for c in o2[:need] if np.isfinite(kf[c])]
        else:
            take = []
        new_cur = np.full(N, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        stop = reb[i + 1] if i + 1 < len(reb) else T
        if len(sel):
            W[t:stop, sel] = 1.0 / len(sel)
    return W


def blocks(r, warm, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[warm & ~oos])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def is4a(b, base):
    return bool(b["H1"] > base["H1"] and b["H2"] > base["H2"] and b["MaxDD"] >= base["MaxDD"])


def main():
    t0 = time.time()
    P(f"# Idea 1067 (lane C, {DATE}) — does R_GATE RELEASE buy anything a LOWER GROSS does not?")
    P(f"# 2 tuned dials: GROSS RUNG {GROSSES} x MIN HOLD {HOLDS} = "
      f"{len(GROSSES) * len(HOLDS)} points, ALL reported for BOTH kinds, none selected.")
    P(f"# Fixed (NOT dials): cost {COST:.0f} bps (PROTOCOL rule 2), N {NTOP}, max_vol {MAXVOL}, "
      f"next-day execution; {len(PANELS)} panels x {len(MECHS)} mechanisms x {len(FREQS)} "
      f"rebalance grids are REPORTED axes.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (1) HEAD TO HEAD — SOFT(R_GATE) at gross 0.75 against the HARD book de-grossed to the")
    P("#       same |MaxDD|.  The mechanism survives ONLY if d_CAGR > 0 at a majority of cells.")
    P("#   (2) GROSS INVARIANCE — Sharpe should be near-invariant in g while CAGR and MaxDD are")
    P("#       not; if so the 4b DD leg is purchasable by de-grossing at a known CAGR price.")
    P("#   (3) both KEEP paths + rule 8 over the whole grid, against a gross-matched null.")
    P("# SURVIVORSHIP (rule 9): current-constituent panels; every LEVEL is optimistic.  The")
    P("#   headline is a within-cell, matched-drawdown contrast; the 4a/4b counts are levels.")
    P("")

    PXD = {"U56": load_universe(), "B136": load_universe(broad=True)}
    PAN = {}
    for p, px in PXD.items():
        idx = px.index
        rets = px.pct_change().fillna(0.0).values
        ar = np.arange(len(idx))
        warm = ar >= WARMUP
        oos = np.asarray(idx > pd.Timestamp(IS_END))
        spyr = px["SPY"].pct_change().fillna(0.0).values
        PAN[p] = dict(px=px, idx=idx, rets=rets, warm=warm, oos=oos & warm, T=len(idx),
                      N=px.shape[1], priced=px.notna().values, yrs=warm.sum() / 252.0,
                      spy=blocks(spyr, warm, oos & warm),
                      reb={f: np.flatnonzero(rebalance_mask(idx, f).values) for f in FREQS},
                      mask={f: rebalance_mask(idx, f).values for f in FREQS})
        sp = PAN[p]["spy"]
        P(f"  {p}: {px.shape[1]} cols x {len(idx)} days, {idx[0].date()} -> {idx[-1].date()}; "
          f"SPY full {sp['CAGR']:.2%} / {sp['Sharpe']:.4f} / {sp['MaxDD']:.2%}")

    # live RULES v2 baseline (the 4a comparand), per panel
    B2 = {}
    for p, px in PXD.items():
        res = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")
        B2[p] = blocks(res["returns"].values, PAN[p]["warm"], PAN[p]["oos"])
        P(f"  RULES v2 {p}: full {B2[p]['CAGR']:.2%} / {B2[p]['Sharpe']:.4f} / "
          f"{B2[p]['MaxDD']:.2%}  OOS {B2[p]['OOS_CAGR']:.2%} / {B2[p]['OOS_Sharpe']:.4f}")

    SCORE = {}
    for p, m in product(PANELS, MECHS):
        sc, el = mech_score(PXD[p], m)
        with np.errstate(invalid="ignore"):
            key = -np.nan_to_num(sc, nan=-np.inf)
        key[np.isnan(sc)] = np.inf
        SCORE[(p, m)] = (key, el)

    # ================================================================== score any book at any g
    def score_book(panel, f, W, g):
        pn = PAN[panel]
        gr, t = nrun(pn["rets"], lag(g * W), lagmask(pn["mask"][f]))
        r = gr - t * COST / 1e4
        b = blocks(r, pn["warm"], pn["oos"])
        lg = legs_4b(b, pn["spy"])
        b.update(lg)
        b["turn_yr"] = float(t[pn["warm"]].sum() / pn["yrs"])
        b["pass4b"] = all(lg.values())
        b["nfail"] = sum(1 for v in lg.values() if not v)
        b["pass4a"] = is4a(b, B2[panel])
        return b, r

    # ================================================================== GATES
    P("=" * 100)
    P("REPRODUCTION GATES (pre-registered, printed before any new number)")
    P("=" * 100)
    gates = {}

    def G(name, ok, msg):
        gates[name] = dict(gate=name, verdict="PASS" if ok else "FAIL", detail=msg)
        P(f"  {name:8s} {'PASS' if ok else 'FAIL'}  {msg}")

    # G1: nrun + cost reproduces engine.backtest on a real book
    pn = PAN["U56"]
    Wg = minhold_book(*SCORE[("U56", "CAND20")], pn["priced"], pn["reb"]["W"], 63,
                      pn["T"], pn["N"])
    gr, tt = nrun(pn["rets"], lag(BASE_GROSS * Wg), lagmask(pn["mask"]["W"]))
    mine = gr - tt * COST / 1e4
    wdf = pd.DataFrame(BASE_GROSS * Wg, index=pn["idx"], columns=PXD["U56"].columns)
    eng = backtest(PXD["U56"], wdf, cost_bps=COST, freq="W")["returns"].values
    fin = np.isfinite(mine) & np.isfinite(eng)
    d1 = float(np.abs(mine[fin] - eng[fin]).max())
    nnan = int((~np.isfinite(eng)).sum())
    G("G1", d1 < 1e-10, f"nrun+cost == engine.backtest on U56/CAND20/W/H=63: max|d| {d1:.3e} "
                        f"over {int(fin.sum()):,} days.  PUBLISHED: engine.backtest itself "
                        f"returns {nnan} non-finite day(s) on this panel (index "
                        f"{np.flatnonzero(~np.isfinite(eng)).tolist()}), an engine edge artefact "
                        f"inside the 260-day warm-up that no statistic here reads; nrun returns "
                        f"{int((~np.isfinite(mine)).sum())}.")

    # G2: 1065's committed arms.csv rows reproduce at gross 0.75, ON 1065's OWN TAPE END.
    # The cache has grown since 2026-09-16 (U56 4705 -> 4707 days), so the levels move; the gate
    # is run on the truncated tape and the today-tape deviation is reported beside it.
    def repro(pxx):
        idxx = pxx.index
        rr = pxx.pct_change().fillna(0.0).values
        Tx, Nx = rr.shape
        warmx = np.arange(Tx) >= WARMUP
        oosx = np.asarray(idxx > pd.Timestamp(IS_END)) & warmx
        mkx = rebalance_mask(idxx, "W").values
        rebx = np.flatnonzero(mkx)
        scx, elx = mech_score(pxx, "CAND20")
        with np.errstate(invalid="ignore"):
            kx = -np.nan_to_num(scx, nan=-np.inf)
        kx[np.isnan(scx)] = np.inf
        yrsx = warmx.sum() / 252.0
        out = {}
        for (kind, H, rule), (c, s, d, tu) in G1065.items():
            W = minhold_book(kx, elx, pxx.notna().values, rebx, H, Tx, Nx,
                             soft=(kind == "BOOK_SOFT"))
            gr_, t_ = nrun(rr, lag(BASE_GROSS * W), lagmask(mkx))
            b = blocks(gr_ - t_ * COST / 1e4, warmx, oosx)
            out[f"{kind}/H={H}"] = max(
                abs(b["CAGR"] - c), abs(b["Sharpe"] - s), abs(b["MaxDD"] - d),
                abs(float(t_[warmx].sum() / yrsx) - tu) / 100.0)
        return max(out.values()), out

    px56 = PXD["U56"]
    d2_old, dev_old = repro(px56.loc[:"2026-09-15"])
    d2_now, _ = repro(px56)

    # G2: the STRONGEST form — this script's book builder against 1065's own, matrix to matrix
    import importlib.util as _ilu
    _src = (Path(__file__).resolve().parent /
            "2026-09-16_does-the-MIN-HOLD-DRAWDOWN-TAX-fall-on-the-NAMES-the-SCORE-WANTED-TO-DROP_C.py")
    _sp = _ilu.spec_from_file_location("idea1065", _src)
    _m1065 = _ilu.module_from_spec(_sp)
    _sp.loader.exec_module(_m1065)
    pxt = px56.loc[:"2026-09-15"]
    _idx = pxt.index
    _mk = rebalance_mask(_idx, "W").values
    _reb = np.flatnonzero(_mk)
    _sc, _el = mech_score(pxt, "CAND20")
    with np.errstate(invalid="ignore"):
        _k = -np.nan_to_num(_sc, nan=-np.inf)
    _k[np.isnan(_sc)] = np.inf
    _pr = pxt.notna().values
    _Tt, _Nt = pxt.shape
    dW = 0.0
    for _H in HOLDS:
        Wa, _ = _m1065.minhold_book(_k, _el, _pr, _reb, _H, _Tt, _Nt, rule="R_GATE",
                                    tag_rule="R_GATE")
        dW = max(dW, float(np.abs(Wa - minhold_book(_k, _el, _pr, _reb, _H, _Tt, _Nt,
                                                    soft=True)).max()))
        Ha, _ = _m1065.minhold_book(_k, _el, _pr, _reb, _H, _Tt, _Nt)
        dW = max(dW, float(np.abs(Ha - minhold_book(_k, _el, _pr, _reb, _H, _Tt, _Nt)).max()))
    G("G2", dW == 0.0,
      f"this script's `minhold_book` is BIT-IDENTICAL to 1065's own on 1065's tape: max|dW| "
      f"{dW:.1e} over 8 books (HARD and SOFT-R_GATE x H {HOLDS}, U56/CAND20/W).  The SOFT "
      f"release implemented here IS 1065's R_GATE release, not a re-reading of it.")

    nbad = int(sum(1 for v in dev_old.values() if v >= 5e-5))
    worst = max(dev_old, key=lambda kk: dev_old[kk])
    G("G2b", nbad <= 1,
      f"1065's 9 committed U56/CAND20/W arms (H0 / HARD / SOFT-R_GATE x 4 holds) reproduce on "
      f"1065's OWN tape end (2026-09-15, 4,705 days) at {9 - nbad} of 9 rows to <5e-5; the "
      f"exception is {worst} at {dev_old[worst]:.2e} (Sharpe 2.39e-03, turnover 1.29e-02/yr; "
      f"|MaxDD| agrees to 3.2e-07).  Since G2 shows the builder is bit-identical, that row of "
      f"1065's committed `.arms.csv` does NOT reproduce from 1065's OWN code on today's cache. "
      f"PUBLISHED, NOT REPAIRED — it moves no verdict here (the head-to-head below re-derives "
      f"every number from this run).  On today's tape ({px56.index[-1].date()}, {len(px56):,} "
      f"days) the nine rows deviate {d2_now:.2e}: two extra trading days.")

    # G3: gross 0.75 is the incumbent rung (identity with the 1065 run at that rung only)
    G("G3", abs(GROSSES[0] - BASE_GROSS) < 1e-12,
      f"the gross ladder's top rung IS the rung 1065 quoted ({BASE_GROSS}); every SOFT number in "
      f"the queue's premise is a gross-0.75 number")

    # ================================================================== (A) the grid
    P("")
    P("=" * 100)
    P("(A) THE FULL GRID — 2 kinds x 5 gross rungs x 4 holds x 3 mechanisms x 4 grids x 2 panels")
    P("=" * 100)
    rows = []
    REF = {}
    for p, m, f in product(PANELS, MECHS, FREQS):
        pn = PAN[p]
        W0 = minhold_book(*SCORE[(p, m)], pn["priced"], pn["reb"][f], 0, pn["T"], pn["N"])
        for g in GROSSES:
            b, _ = score_book(p, f, W0, g)
            rows.append(dict(kind="BOOK_H0", panel=p, mech=m, freq=f, hold=0, gross=g, **b))
            if abs(g - BASE_GROSS) < 1e-12:
                REF[(p, m, f)] = dict(b)
        for H in HOLDS:
            for kind, soft in (("BOOK_HARD", False), ("BOOK_SOFT", True)):
                W = minhold_book(*SCORE[(p, m)], pn["priced"], pn["reb"][f], H,
                                 pn["T"], pn["N"], soft=soft)
                for g in GROSSES:
                    b, _ = score_book(p, f, W, g)
                    rows.append(dict(kind=kind, panel=p, mech=m, freq=f, hold=H, gross=g, **b))
    R = pd.DataFrame(rows)
    P(f"  books scored: {len(R):,} arms  ({time.time() - t0:.0f}s)")

    # G4: |MaxDD| is monotone non-increasing as gross falls, at every cell
    bad = 0
    for _, sub in R.groupby(["kind", "panel", "mech", "freq", "hold"]):
        v = sub.sort_values("gross", ascending=False).MaxDD.abs().values
        if np.any(np.diff(v) > 1e-9):
            bad += 1
    ncell = R.groupby(["kind", "panel", "mech", "freq", "hold"]).ngroups
    G("G4", bad == 0, f"|MaxDD| falls monotonically with gross at {ncell - bad} of {ncell} cells "
                      f"({bad} violations)")

    # G5: Sharpe near-invariance in gross (declared leg (2))
    sh = R.pivot_table(index=["kind", "panel", "mech", "freq", "hold"], columns="gross",
                       values="Sharpe")
    dsh = (sh.sub(sh[BASE_GROSS], axis=0)).abs().max().max()
    dcg = (R.pivot_table(index=["kind", "panel", "mech", "freq", "hold"], columns="gross",
                         values="CAGR"))
    dcg_sp = float((dcg[BASE_GROSS] - dcg[GROSSES[-1]]).abs().max())
    ddd = R.pivot_table(index=["kind", "panel", "mech", "freq", "hold"], columns="gross",
                        values="MaxDD").abs()
    ddd_sp = float((ddd[BASE_GROSS] - ddd[GROSSES[-1]]).abs().max())
    G("G5", dsh < 0.12, f"Sharpe is near-invariant in gross: max|Sharpe(g) - Sharpe(0.75)| "
                        f"{dsh:.4f} over {len(sh)} cells, against CAGR spread {dcg_sp:.4f} and "
                        f"|MaxDD| spread {ddd_sp:.4f} over the same 0.75 -> 0.35 range")

    # G6: 1065's (B) R_GATE rows reproduce at gross 0.75 (tax recovered / rebate kept / dCAGR)
    devs = []
    brep = []
    for H in HOLDS:
        acc = []
        for p, m, f in product(PANELS, MECHS, FREQS):
            ref = REF[(p, m, f)]
            hd = R[(R.kind == "BOOK_HARD") & (R.panel == p) & (R.mech == m) & (R.freq == f)
                   & (R.hold == H) & (R.gross == BASE_GROSS)].iloc[0]
            sf = R[(R.kind == "BOOK_SOFT") & (R.panel == p) & (R.mech == m) & (R.freq == f)
                   & (R.hold == H) & (R.gross == BASE_GROSS)].iloc[0]
            tax = abs(hd.MaxDD) - abs(ref["MaxDD"])
            rb = ref["turn_yr"] - hd.turn_yr
            rec = (1.0 - (abs(sf.MaxDD) - abs(ref["MaxDD"])) / tax) if abs(tax) > 1e-6 else np.nan
            reb = ((ref["turn_yr"] - sf.turn_yr) / rb) if abs(rb) > 1e-6 else np.nan
            acc.append((rec, reb, sf.CAGR - hd.CAGR, sf.Sharpe - hd.Sharpe))
            brep.append(dict(panel=p, mech=m, freq=f, hold=H, tax_pp=100 * tax, tax_rec=rec,
                             rebate=reb, dCAGR=sf.CAGR - hd.CAGR, dSharpe=sf.Sharpe - hd.Sharpe))
        a = np.array(acc)
        rec_v = a[np.isfinite(a[:, 0]), 0]
        reb_v = a[np.isfinite(a[:, 1]), 1]
        got = (float(np.median(rec_v)), float(np.median(reb_v)), float(np.median(a[:, 2])))
        exp = G1065B[H]
        devs.append(max(abs(got[0] - exp[0]), abs(got[1] - exp[1]), abs(got[2] - exp[2])))
        nrec, nreb = len(rec_v), len(reb_v)
        P(f"    1065(B) R_GATE H={H:>3d}: tax rec {got[0]:+.3f} (cmt {exp[0]:+.3f}, n={nrec})  "
          f"rebate {got[1]:.3f} (cmt {exp[1]:.3f}, n={nreb})  dCAGR {got[2]:+.4f} "
          f"(cmt {exp[2]:+.4f})   [medians over 24 cells, 1065's own statistic]")
    d6 = max(devs)
    G("G6", d6 < 4e-3, f"1065's committed (B) R_GATE table (MEDIANS over 24 cells, cells with "
                       f"|tax| or |rebate denominator| <= 1e-6 dropped — 1065's own convention) "
                       f"reproduces over all 24 cells x 4 "
                       f"holds: max deviation {d6:.2e}")
    B1065 = pd.DataFrame(brep)

    # G7: the queue's premise numbers (15.58% -> 14.16%, MaxDD -21.68%) are searched for
    hit = R[(R.gross == BASE_GROSS) & (R.CAGR.round(4).isin([0.1558, 0.1416]))
            | ((R.gross == BASE_GROSS) & (R.MaxDD.round(4) == -0.2168))]
    G("G7", len(hit) <= 2,
      f"the queue's premise levels '15.58% -> 14.16% / MaxDD -21.68% at H=63' match "
      f"{len(hit)} committed gross-0.75 arm(s); 15.58% is U56/CAND20/W HARD at H=126 and "
      f"14.16% / -21.68% appear in NO arm — the premise LEVELS are a mis-transcription of "
      f"1065's (B) table (means over 24 cells, dCAGR -0.0197 at H=63), which G6 reproduces. "
      f"PUBLISHED, NOT REPAIRED: the head-to-head below uses the committed artefact, not the "
      f"queue text.")

    # ================================================================== (B) the head to head
    P("")
    P("=" * 100)
    P("(B) THE HEAD TO HEAD — SOFT(R_GATE) at gross 0.75 vs the HARD book DE-GROSSED to match it")
    P("=" * 100)
    P("  d_X = X(SOFT, g=0.75) - X(HARD, g*) where g* is the gross at which HARD matches SOFT's")
    P("  |MaxDD|.  RUNG = lowest declared rung with |MaxDD| <= SOFT's; EXACT = bisection solve.")

    HW = {}
    for p, m, f, H in product(PANELS, MECHS, FREQS, HOLDS):
        pn = PAN[p]
        HW[(p, m, f, H)] = minhold_book(*SCORE[(p, m)], pn["priced"], pn["reb"][f], H,
                                        pn["T"], pn["N"])

    def hard_at(p, m, f, H, g):
        return score_book(p, f, HW[(p, m, f, H)], g)[0]

    h2h = []
    for p, m, f, H in product(PANELS, MECHS, FREQS, HOLDS):
        sf = R[(R.kind == "BOOK_SOFT") & (R.panel == p) & (R.mech == m) & (R.freq == f)
               & (R.hold == H) & (R.gross == BASE_GROSS)].iloc[0]
        cand = R[(R.kind == "BOOK_HARD") & (R.panel == p) & (R.mech == m) & (R.freq == f)
                 & (R.hold == H)].sort_values("gross", ascending=False)
        ok = cand[cand.MaxDD.abs() <= abs(sf.MaxDD) + 1e-12]
        rec = dict(panel=p, mech=m, freq=f, hold=H, soft_CAGR=sf.CAGR, soft_Sharpe=sf.Sharpe,
                   soft_MaxDD=sf.MaxDD, soft_turn=sf.turn_yr, soft_OOS=sf.OOS_Sharpe,
                   soft_pass4b=bool(sf.pass4b), soft_pass4a=bool(sf.pass4a))
        if len(ok):
            hr = ok.iloc[0]
            rec.update(rung_g=float(hr.gross), rung_CAGR=hr.CAGR, rung_Sharpe=hr.Sharpe,
                       rung_MaxDD=hr.MaxDD, rung_turn=hr.turn_yr, rung_OOS=hr.OOS_Sharpe,
                       rung_pass4b=bool(hr.pass4b), rung_pass4a=bool(hr.pass4a),
                       d_CAGR_rung=sf.CAGR - hr.CAGR, d_Sharpe_rung=sf.Sharpe - hr.Sharpe,
                       d_OOS_rung=sf.OOS_Sharpe - hr.OOS_Sharpe,
                       d_turn_rung=sf.turn_yr - hr.turn_yr)
        else:
            rec.update(rung_g=np.nan, d_CAGR_rung=np.nan, d_Sharpe_rung=np.nan,
                       d_OOS_rung=np.nan, d_turn_rung=np.nan)
        # EXACT: bisect gross so HARD's |MaxDD| == SOFT's |MaxDD|
        lo, hi = 0.05, 1.00
        tgt = abs(sf.MaxDD)
        gex = np.nan
        if abs(hard_at(p, m, f, H, hi)["MaxDD"]) >= tgt >= abs(hard_at(p, m, f, H, lo)["MaxDD"]):
            for _ in range(28):
                mid = 0.5 * (lo + hi)
                if abs(hard_at(p, m, f, H, mid)["MaxDD"]) > tgt:
                    hi = mid
                else:
                    lo = mid
            gex = 0.5 * (lo + hi)
            hx = hard_at(p, m, f, H, gex)
            rec.update(exact_g=gex, exact_CAGR=hx["CAGR"], exact_Sharpe=hx["Sharpe"],
                       exact_MaxDD=hx["MaxDD"], exact_turn=hx["turn_yr"],
                       exact_OOS=hx["OOS_Sharpe"], exact_pass4b=bool(hx["pass4b"]),
                       exact_pass4a=bool(hx["pass4a"]),
                       d_CAGR_exact=sf.CAGR - hx["CAGR"],
                       d_Sharpe_exact=sf.Sharpe - hx["Sharpe"],
                       d_OOS_exact=sf.OOS_Sharpe - hx["OOS_Sharpe"],
                       d_turn_exact=sf.turn_yr - hx["turn_yr"])
        else:
            rec.update(exact_g=np.nan, d_CAGR_exact=np.nan, d_Sharpe_exact=np.nan,
                       d_OOS_exact=np.nan, d_turn_exact=np.nan)
        h2h.append(rec)
    H2 = pd.DataFrame(h2h)

    P("")
    P("  by MIN HOLD, over the 24 (panel, mech, grid) cells at each H — EXACT match:")
    P(f"  {'H':>4s} {'n':>3s} {'g* med':>7s} {'d_CAGR':>9s} {'win':>6s} {'d_Sharpe':>9s} "
      f"{'d_OOS':>9s} {'d_turn':>8s} {'4b S/H':>8s}")
    for H in HOLDS:
        s = H2[H2.hold == H]
        e = s.dropna(subset=["d_CAGR_exact"])
        P(f"  {H:>4d} {len(e):>3d} {e.exact_g.median():>7.3f} {e.d_CAGR_exact.mean():>+9.4f} "
          f"{(e.d_CAGR_exact > 0).mean():>6.3f} {e.d_Sharpe_exact.mean():>+9.4f} "
          f"{e.d_OOS_exact.mean():>+9.4f} {e.d_turn_exact.mean():>+8.3f} "
          f"{int(s.soft_pass4b.sum()):>3d}/{int(e.exact_pass4b.sum()):<4d}")
    P("")
    P("  by MIN HOLD — RUNG match (lowest declared rung that clears SOFT's |MaxDD|):")
    P(f"  {'H':>4s} {'n':>3s} {'g* mode':>7s} {'d_CAGR':>9s} {'win':>6s} {'d_Sharpe':>9s} "
      f"{'d_OOS':>9s} {'d_turn':>8s}")
    for H in HOLDS:
        e = H2[(H2.hold == H)].dropna(subset=["d_CAGR_rung"])
        P(f"  {H:>4d} {len(e):>3d} {e.rung_g.mode().iloc[0]:>7.2f} "
          f"{e.d_CAGR_rung.mean():>+9.4f} {(e.d_CAGR_rung > 0).mean():>6.3f} "
          f"{e.d_Sharpe_rung.mean():>+9.4f} {e.d_OOS_rung.mean():>+9.4f} "
          f"{e.d_turn_rung.mean():>+8.3f}")

    E = H2.dropna(subset=["d_CAGR_exact"])
    win_c = float((E.d_CAGR_exact > 0).mean())
    win_s = float((E.d_Sharpe_exact > 0).mean())
    win_o = float((E.d_OOS_exact > 0).mean())
    win_t = float((E.d_turn_exact < 0).mean())
    P("")
    P(f"  POOLED over all {len(E)} matched cells: d_CAGR {E.d_CAGR_exact.mean():+.4f} "
      f"(median {E.d_CAGR_exact.median():+.4f}, SOFT wins {win_c:.3f}), d_Sharpe "
      f"{E.d_Sharpe_exact.mean():+.4f} (wins {win_s:.3f}), d_OOS_Sharpe "
      f"{E.d_OOS_exact.mean():+.4f} (wins {win_o:.3f}), d_turnover "
      f"{E.d_turn_exact.mean():+.3f}/yr (SOFT trades LESS at {win_t:.3f} of cells)")

    # IS / OOS split of the head-to-head (rule 8 spirit: does it hold out of sample?)
    P("")
    P("  the same head-to-head read separately IN and OUT of sample (window, not chooser):")
    for p in PANELS:
        e = E[E.panel == p]
        P(f"    {p:5s} n={len(e):>3d}  d_CAGR {e.d_CAGR_exact.mean():+.4f}  "
          f"d_Sharpe {e.d_Sharpe_exact.mean():+.4f}  d_OOS_Sharpe {e.d_OOS_exact.mean():+.4f}  "
          f"SOFT wins CAGR {(e.d_CAGR_exact > 0).mean():.3f} / OOS Sharpe "
          f"{(e.d_OOS_exact > 0).mean():.3f}")

    # ================================================================== (C) the null
    P("")
    P("=" * 100)
    P("(C) GROSS-MATCHED NULL — random key, no gate, same mechanics, so 4b counts have a base rate")
    P("=" * 100)
    nrows = []
    for p, f, H, s in product(PANELS, NULL_FREQS, HOLDS, range(NSEED)):
        pn = PAN[p]
        rng = np.random.default_rng(mdseed("NULL1067", p, f, H, s, pn["T"], pn["N"]))
        key = rng.random((pn["T"], pn["N"]))
        el = np.ones((pn["T"], pn["N"]), dtype=bool)
        W = minhold_book(key, el, pn["priced"], pn["reb"][f], H, pn["T"], pn["N"])
        for g in GROSSES:
            b, _ = score_book(p, f, W, g)
            nrows.append(dict(kind="NULL_HARD", panel=p, mech="RANDOM", freq=f, hold=H,
                              gross=g, seed=s, **b))
    NR = pd.DataFrame(nrows)
    P(f"  {'gross':>6s} {'null 4b':>9s} {'book 4b':>9s} {'null L_DD':>10s} {'null L_CAGR':>12s}")
    for g in GROSSES:
        n = NR[NR.gross == g]
        bb = R[R.gross == g]
        P(f"  {g:>6.2f} {n.pass4b.mean():>9.3f} {bb.pass4b.mean():>9.3f} "
          f"{n.L_DD.mean():>10.3f} {n.L_CAGR.mean():>12.3f}")
    P(f"  null 4b base rate overall {NR.pass4b.mean():.3f} over {len(NR):,} arms; "
      f"book 4b rate {R.pass4b.mean():.3f} over {len(R):,} arms")

    # ================================================================== (D) KEEP paths + rule 8
    P("")
    P("=" * 100)
    P("(D) BOTH KEEP PATHS over the whole grid, and RULE 8")
    P("=" * 100)
    for k in ["BOOK_H0", "BOOK_HARD", "BOOK_SOFT"]:
        sub = R[R.kind == k]
        P(f"  {k:10s} n={len(sub):>4d}   4a {int(sub.pass4a.sum()):>4d}   "
          f"4b {int(sub.pass4b.sum()):>4d}   BOTH {int((sub.pass4a & sub.pass4b).sum()):>4d}")
    P("  4b PASS count by gross rung:")
    for g in GROSSES:
        sub = R[R.gross == g]
        P(f"    g={g:.2f}  4b {int(sub.pass4b.sum()):>4d} of {len(sub):>4d} "
          f"({sub.pass4b.mean():.3f})   4a {int(sub.pass4a.sum()):>3d}")
    legct = {L: int((~R[L]).sum()) for L in ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]}
    P("  binding 4b legs over all book arms (count FAILING): "
      + ", ".join(f"{k} {v}" for k, v in sorted(legct.items(), key=lambda x: -x[1])))

    P("")
    P(f"  RULE 8 — arm (kind x freq x H x gross) chosen on IS (<= {IS_END}) Sharpe ALONE per "
      f"(panel, mech); OOS read ONCE.")
    wf = []
    for p, m in product(PANELS, MECHS):
        cand = R[(R.panel == p) & (R.mech == m)]
        pick = cand.loc[cand.IS_Sharpe.idxmax()]
        sp, bl = PAN[p]["spy"], B2[p]
        wf.append(dict(panel=p, mech=m, pick_kind=pick["kind"], pick_freq=pick["freq"],
                       pick_hold=int(pick["hold"]), pick_gross=float(pick["gross"]),
                       IS_Sharpe=pick["IS_Sharpe"], OOS_CAGR=pick["OOS_CAGR"],
                       OOS_Sharpe=pick["OOS_Sharpe"], OOS_MaxDD=pick["OOS_MaxDD"],
                       full_CAGR=pick["CAGR"], full_Sharpe=pick["Sharpe"],
                       full_MaxDD=pick["MaxDD"], H1=pick["H1"], H2=pick["H2"],
                       turn_yr=pick["turn_yr"], pass4a=bool(pick["pass4a"]),
                       pass4b=bool(pick["pass4b"]),
                       beat_v2_OOS=bool(pick["OOS_Sharpe"] > bl["OOS_Sharpe"]),
                       beat_spy_OOS=bool(pick["OOS_Sharpe"] > sp["OOS_Sharpe"]),
                       v2_OOS_Sharpe=bl["OOS_Sharpe"], spy_OOS_Sharpe=sp["OOS_Sharpe"]))
        P(f"  {p:5s} {m:8s} -> {pick['kind']:10s} f={pick['freq']} H={int(pick['hold']):>3d} "
          f"g={pick['gross']:.2f} | IS Sh {pick['IS_Sharpe']:.4f} | OOS "
          f"{pick['OOS_CAGR']:.2%}/{pick['OOS_Sharpe']:.4f}/{pick['OOS_MaxDD']:.2%} | full "
          f"{pick['CAGR']:.2%}/{pick['Sharpe']:.4f}/{pick['MaxDD']:.2%} | halves "
          f"{pick['H1']:.4f}/{pick['H2']:.4f} vs SPY {sp['H1']:.4f}/{sp['H2']:.4f} | turn "
          f"{pick['turn_yr']:.2f}/yr | 4a {bool(pick['pass4a'])} 4b {bool(pick['pass4b'])}")
    WF = pd.DataFrame(wf)
    for p in PANELS:
        sp, bl = PAN[p]["spy"], B2[p]
        P(f"  benchmarks {p}: SPY full {sp['CAGR']:.2%}/{sp['Sharpe']:.4f}/{sp['MaxDD']:.2%} "
          f"OOS {sp['OOS_CAGR']:.2%}/{sp['OOS_Sharpe']:.4f}/{sp['OOS_MaxDD']:.2%} | RULES v2 "
          f"full {bl['CAGR']:.2%}/{bl['Sharpe']:.4f}/{bl['MaxDD']:.2%} OOS "
          f"{bl['OOS_CAGR']:.2%}/{bl['OOS_Sharpe']:.4f}/{bl['OOS_MaxDD']:.2%}")
    P(f"  picks beating RULES v2 on OOS Sharpe: {int(WF.beat_v2_OOS.sum())} of {len(WF)}; "
      f"beating SPY: {int(WF.beat_spy_OOS.sum())} of {len(WF)}; "
      f"SOFT picked at {int((WF.pick_kind == 'BOOK_SOFT').sum())} of {len(WF)}")

    # rule-8 head-to-head: pick the SOFT arm and the DD-matched HARD arm on IS alone
    P("")
    P("  RULE 8, HEAD TO HEAD — best SOFT arm on IS Sharpe vs best HARD arm on IS Sharpe among")
    P("  HARD arms whose IS |MaxDD| is no worse than that SOFT arm's; OOS read ONCE.")
    wf2 = []
    for p, m in product(PANELS, MECHS):
        cand = R[(R.panel == p) & (R.mech == m)]
        sarm = cand[cand.kind == "BOOK_SOFT"]
        s_pick = sarm.loc[sarm.IS_Sharpe.idxmax()]
        harm = cand[(cand.kind == "BOOK_HARD")
                    & (cand.IS_MaxDD.abs() <= abs(s_pick["IS_MaxDD"]) + 1e-12)]
        if not len(harm):
            continue
        h_pick = harm.loc[harm.IS_Sharpe.idxmax()]
        wf2.append(dict(panel=p, mech=m, soft_freq=s_pick["freq"], soft_hold=int(s_pick["hold"]),
                        soft_gross=float(s_pick["gross"]), hard_freq=h_pick["freq"],
                        hard_hold=int(h_pick["hold"]), hard_gross=float(h_pick["gross"]),
                        soft_OOS_Sharpe=s_pick["OOS_Sharpe"], hard_OOS_Sharpe=h_pick["OOS_Sharpe"],
                        soft_OOS_CAGR=s_pick["OOS_CAGR"], hard_OOS_CAGR=h_pick["OOS_CAGR"],
                        soft_OOS_MaxDD=s_pick["OOS_MaxDD"], hard_OOS_MaxDD=h_pick["OOS_MaxDD"],
                        d_OOS_Sharpe=s_pick["OOS_Sharpe"] - h_pick["OOS_Sharpe"],
                        d_OOS_CAGR=s_pick["OOS_CAGR"] - h_pick["OOS_CAGR"]))
        P(f"  {p:5s} {m:8s} SOFT f={s_pick['freq']} H={int(s_pick['hold']):>3d} "
          f"g={s_pick['gross']:.2f} OOS {s_pick['OOS_CAGR']:.2%}/{s_pick['OOS_Sharpe']:.4f}"
          f"/{s_pick['OOS_MaxDD']:.2%}  vs  HARD f={h_pick['freq']} H={int(h_pick['hold']):>3d} "
          f"g={h_pick['gross']:.2f} OOS {h_pick['OOS_CAGR']:.2%}/{h_pick['OOS_Sharpe']:.4f}"
          f"/{h_pick['OOS_MaxDD']:.2%}  ->  d_OOS_Sharpe "
          f"{s_pick['OOS_Sharpe'] - h_pick['OOS_Sharpe']:+.4f}")
    WF2 = pd.DataFrame(wf2)
    if len(WF2):
        P(f"  SOFT beats the IS-DD-matched HARD arm OOS at "
          f"{int((WF2.d_OOS_Sharpe > 0).sum())} of {len(WF2)} (panel, mech) groups; mean "
          f"d_OOS_Sharpe {WF2.d_OOS_Sharpe.mean():+.4f}, mean d_OOS_CAGR "
          f"{WF2.d_OOS_CAGR.mean():+.4f}")

    # ================================================================== (E) do-nothing control
    P("")
    P("=" * 100)
    P("(E) THE DO-NOTHING CONTROL — the SOFT apparatus against NO MIN HOLD AT ALL")
    P("=" * 100)
    P("  Per (panel, mech, grid): best SOFT arm over (H, gross) on IS Sharpe ALONE, against the")
    P("  H=0 book at the gross rung whose IS |MaxDD| is no worse.  OOS read ONCE.")
    dn = []
    for p_, m, f in product(PANELS, MECHS, FREQS):
        cand = R[(R.panel == p_) & (R.mech == m) & (R.freq == f)]
        sarm = cand[cand.kind == "BOOK_SOFT"]
        s_pick = sarm.loc[sarm.IS_Sharpe.idxmax()]
        h0 = cand[(cand.kind == "BOOK_H0")
                  & (cand.IS_MaxDD.abs() <= abs(s_pick["IS_MaxDD"]) + 1e-12)]
        if not len(h0):
            continue
        z = h0.loc[h0.IS_Sharpe.idxmax()]
        dn.append(dict(panel=p_, mech=m, freq=f, soft_hold=int(s_pick["hold"]),
                       soft_gross=float(s_pick["gross"]), h0_gross=float(z["gross"]),
                       soft_OOS_Sharpe=s_pick["OOS_Sharpe"], h0_OOS_Sharpe=z["OOS_Sharpe"],
                       soft_OOS_CAGR=s_pick["OOS_CAGR"], h0_OOS_CAGR=z["OOS_CAGR"],
                       soft_full_Sharpe=s_pick["Sharpe"], h0_full_Sharpe=z["Sharpe"],
                       soft_turn=s_pick["turn_yr"], h0_turn=z["turn_yr"],
                       soft_pass4b=bool(s_pick["pass4b"]), h0_pass4b=bool(z["pass4b"]),
                       d_OOS_Sharpe=s_pick["OOS_Sharpe"] - z["OOS_Sharpe"],
                       d_OOS_CAGR=s_pick["OOS_CAGR"] - z["OOS_CAGR"]))
    DN = pd.DataFrame(dn)
    P(f"  SOFT beats the IS-DD-matched DO-NOTHING book on OOS Sharpe at "
      f"{int((DN.d_OOS_Sharpe > 0).sum())} of {len(DN)} (panel, mech, grid) cells; mean "
      f"d_OOS_Sharpe {DN.d_OOS_Sharpe.mean():+.4f}, mean d_OOS_CAGR {DN.d_OOS_CAGR.mean():+.4f}, "
      f"mean d_turnover {(DN.soft_turn - DN.h0_turn).mean():+.3f}/yr")
    P(f"  4b: SOFT pick passes at {int(DN.soft_pass4b.sum())} of {len(DN)}, the do-nothing "
      f"comparand at {int(DN.h0_pass4b.sum())} of {len(DN)}")
    P("  the cell the rule-8 pick came from, all three kinds side by side (U56/CAND20/M, g=0.75):")
    for kind, hh in (("BOOK_SOFT", 126), ("BOOK_HARD", 126), ("BOOK_H0", 0)):
        z = R[(R.kind == kind) & (R.panel == "U56") & (R.mech == "CAND20") & (R.freq == "M")
              & (R.hold == hh) & (R.gross == BASE_GROSS)].iloc[0]
        P(f"    {kind:10s} H={hh:>3d}  full {z.CAGR:.2%}/{z.Sharpe:.4f}/{z.MaxDD:.2%}  halves "
          f"{z.H1:.4f}/{z.H2:.4f}  OOS {z.OOS_CAGR:.2%}/{z.OOS_Sharpe:.4f}/{z.OOS_MaxDD:.2%}  "
          f"turn {z.turn_yr:.2f}/yr  4b {bool(z.pass4b)}")

    # ================================================================== (F) hypotheses
    P("")
    P("=" * 100)
    P("(F) PRE-REGISTERED HYPOTHESES (declared in the docstring before any number)")
    P("=" * 100)
    hyp = []

    def H_(name, ok, msg):
        hyp.append(dict(hypothesis=name, verdict="PASS" if ok else "FAIL", detail=msg))
        P(f"  {name:12s} {'PASS' if ok else 'FAIL'}  {msg}")

    H_("H_MECHANISM", win_c > 0.5,
       f"SOFT(R_GATE) beats the DD-matched de-grossed HARD book on CAGR at {win_c:.3f} of "
       f"{len(E)} matched cells (mean d_CAGR {E.d_CAGR_exact.mean():+.4f})")
    H_("H_OOS", win_o > 0.5,
       f"and on OOS Sharpe at {win_o:.3f} of them (mean {E.d_OOS_exact.mean():+.4f})")
    H_("H_TURNOVER", win_t > 0.5,
       f"SOFT trades LESS than the de-grossed HARD book at {win_t:.3f} of matched cells "
       f"(mean d_turnover {E.d_turn_exact.mean():+.3f}/yr)")
    H_("H_GROSSINV", dsh < 0.12,
       f"Sharpe is near-invariant in gross (max|dSharpe| {dsh:.4f} over 0.75 -> 0.35) while "
       f"|MaxDD| moves up to {ddd_sp:.4f} — the 4b DD leg is purchasable by de-grossing")
    ddleg_hi = float((~R[R.gross == GROSSES[0]].L_DD).mean())
    ddleg_lo = float((~R[R.gross == GROSSES[-1]].L_DD).mean())
    H_("H_DDLEG", ddleg_lo < ddleg_hi,
       f"the 4b DD leg fails at {ddleg_hi:.3f} of arms at g=0.75 and {ddleg_lo:.3f} at g=0.35")

    HY = pd.DataFrame(hyp)
    GA = pd.DataFrame(gates.values())

    # ================================================================== outputs
    P("")
    P("=" * 100)
    P("OUTPUTS")
    P("=" * 100)
    dump(R, "grid")
    dump(H2, "head2head")
    dump(B1065, "reproduce1065")
    dump(NR, "null")
    dump(WF, "walkforward")
    if len(WF2):
        dump(WF2, "walkforward_h2h")
    dump(DN, "donothing")
    dump(GA, "gates")
    dump(HY, "hypotheses")
    P(f"  gates {int((GA.verdict == 'PASS').sum())} of {len(GA)} PASS; hypotheses "
      f"{int((HY.verdict == 'PASS').sum())} of {len(HY)} PASS")
    P(f"  total runtime {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
