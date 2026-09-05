#!/usr/bin/env python3
"""QUEUE idea 168 — the-sign-is-the-parameter-not-the-share  (lane B, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 168)
    "idea 159 showed the live INV tilt is affordable at every share (g/c = 16-4254 on the
     honest cost bar) and wrong-signed at all 20 large-cap (panel, share) points, while POS
     is right-signed at 19 of 20.  That makes the tilt EXPONENT, not its presence, the live
     dial: sweep k in composite x vol20^k over k in {-0.5, -0.25, 0, +0.25, +0.5} on both
     large-cap panels at 10/25 bps and report where signed dCAGR crosses zero, with rule 8.
     If the argmax k is at or near 0 the fifth delete-the-scaler finding becomes a measured
     optimum rather than a comparison of three points.  Max 2 params."

WHAT IS AT STAKE.  RULES v1 trades `composite / sqrt(vol20)`, i.e. k = -0.5.  Ideas 72, 82,
    141, 160 and 159 have five times concluded some version of "delete the scaler", each time
    by comparing THREE points (INV / NONE / POS).  Three points cannot tell "k = 0 is the
    optimum" from "k = 0 happened to win a three-horse race".  A ladder in k can.  If the
    argmax of the k-curve sits at or near 0 with the curve falling away on both sides, the
    delete-the-scaler finding stops being a comparison and becomes a measured optimum.  If the
    argmax sits at +0.5 or beyond, the project has been reading a monotone curve's endpoint as
    an optimum for five ideas running and the live dial should be moved the other way, not to
    zero.  Either answer is worth the run; a KILL of "k=0 is the argmax" is as useful as a KEEP.

THE MEASUREMENT, fixed before any number was read
    The book is idea 81/153/159's verbatim, with the tilt exponent generalised:
        score_k = composite * (0.5 + 0.5 * above200) * clip(vol20, 0.08) ** k
    so k = -0.5 IS RULES v1's live score exactly, k = 0 is the unscaled composite (idea 159's
    NONE control), k = +0.5 is its POS arm.  Eligibility (above 200d AND vol20 < 0.60) and
    GROSS = 0.75 stay at RULES v1's values; only the exponent moves.

    Every (panel, constr, share, k) book is run ONCE at 0 bps and every cost rung is derived
    exactly from the same path as   r_c = r_0 - turnover * c / 1e4   (engine.backtest is linear
    in cost), so a level and its cost-differential are the SAME book, not two runs.  The
    identity is asserted against a fresh 10 bps engine run before any result is read.

    LEVEL curve      CAGR(k), Sharpe(k), MaxDD(k) at each cost rung.
    SIGNED difference   dCAGR(k) = CAGR(k) - CAGR(k = 0)   at matched (panel, constr, share,
                     cost).  k = 0 is the control, so dCAGR(0) = 0 identically -- that root is
                     an artefact of the definition and is NOT the crossing the idea asks for.
    THE CROSSING the idea asks for is the boundary of the BENEFICIAL BAND: the maximal
                     contiguous run of grid points containing the argmax on which dCAGR >= 0,
                     with its two endpoints located by linear interpolation between the last
                     inside point and the first outside point.  A band whose endpoint is the
                     grid edge is reported as "open at that edge", never as a crossing.
    ARGMAX           argmax_k CAGR and argmax_k Sharpe, per cell, full sample / IS / OOS.

TUNED PARAMETERS -- exactly two, both swept exhaustively, ALL grid points reported:
    1. the TILT EXPONENT k in {-1.00, -0.75, -0.50, -0.25, 0.00, +0.25, +0.50, +0.75, +1.00}
       (the idea's five points, extended symmetrically by two rungs each side so the argmax
       can be shown to be INTERIOR rather than merely the best of five; the extension is a
       finer/wider reading of the same one parameter, not a second one).
    2. target BOOK SHARE m in {0.20, 0.53, 0.85}, realised as n = max(2, round(m x mean weekly
       eligible count)) -- idea 153/159's own map, so m = 0.53 lands on u56 n = 20.  Share is
       here as idea 159's axis: if the argmax k moves with share, "the sign is the parameter"
       is false and the two dials interact.
    Panels (u56/broad/small), cost rungs (0/10/25 bps), the two gross constructions, the halves,
    the IS/OOS windows and every diagnostic are REPORTED axes, never selected on.

CONFOUNDS, declared before the result
    (i) vol20 is clipped at 0.08 before exponentiation, so |k| > 1 would mostly re-rank the
        clip floor rather than the vol; the grid stops at |k| = 1 for that reason.
    (ii) The eligibility gate already removes vol20 >= 0.60, so the k-ladder operates on a
        vol range that is truncated from above -- the measured slope in k is the slope INSIDE
        the gate, not the slope of a vol factor at large.
    (iii) idea 73/81/153's de-grossing: the literal GROSS/n book invests less than 0.75 when
        fewer than n names are eligible.  The whole grid is re-run gross-normalised ("norm")
        as a reported control, because a k that changes the eligible-set overlap also changes
        how often the literal book is under-invested.
    (iv) At m = 0.85 all k hold most of the eligible set, so dCAGR -> 0 mechanically; a band
        that is wide only at m = 0.85 is arithmetic, not evidence.

REPRODUCTION, asserted before any new number is read (idea 153/159's committed numbers)
    [a] mean weekly eligible counts: u56 37.5, broad 91.5, small 141.2 (tol 0.15).
    [b] share -> n map: u56 m=0.53 -> n=20, m=0.20 -> n=7; broad m=0.53 -> n=48.
    [c] idea 153/159's dCAGR(POS - NONE) at m = 0.20, lit, 10 bps: u56 +2.83%/yr,
        broad +2.75%/yr (tol 0.10 pp) -- this is exactly dCAGR(k=+0.5) in this script.
    [d] idea 159's signed dCAGR(INV - NONE) at m = 0.53, lit, 0 bps, u56 = -0.0268 (tol 0.002)
        -- this is exactly dCAGR(k=-0.5) here, and it is the live book's own tilt.
    [e] the cost-derivation identity r_0 - turnover*10/1e4 == fresh 10 bps engine run to 1e-12.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  Reproduction [a]-[e] holds.
    P2  Over the negative half of the ladder (k <= 0) signed dCAGR is monotone increasing in k
        on both large-cap panels at the incumbent share: Spearman(k, dCAGR) >= +0.6 for k <= 0.
        (Idea 159 says INV is wrong-signed; if so, moving k up toward 0 must help.)
    P3  The full-sample Sharpe argmax k is >= 0 on both large-cap panels at m = 0.53 -- the
        live k = -0.5 is not the optimum.
    P4  The argmax k is NOT sharply identified: across the (panel, share, constr, cost) cells
        of the two large-cap panels the argmax k spans at least 0.50 of the grid.
    P5  Rule 8: an IS-fitted chooser of k (S_IS) does NOT beat the do-nothing constant k = 0
        (S_ZERO) on mean OOS Sharpe.  Ideas 110/151/132/166 killed four such selectors; this
        is the fifth and the prior is that it dies too.
    P6  No book at any k passes 4b (full sample AND OOS window) on either large-cap panel.

WALK-FORWARD (PROTOCOL rule 8), selection rules fixed BEFORE any OOS number is read
    k is chosen on 2009-2016 ONLY (2011-2016 on the small panel), each selector reads its pick
    ONCE on 2017-01-01..2026:
      S_IS     argmax IS Sharpe over the 9-point k ladder at that (panel, constr, share, cost)
      S_ZERO   k = 0 at the same share                                     (do-nothing control)
      S_INV    k = -0.50 at the same share                        (the incumbent's own tilt)
      S_POS    k = +0.50 at the same share                    (idea 159's right-signed arm)
      S_LIVE   RULES v1 on that panel (n = 5, w = 0.15)                          (the book)
    Reported as OOS CAGR/Sharpe/MaxDD against RULES v1 (same panel, same cost) and SPY.
    Both KEEP paths (4a and 4b) are evaluated at EVERY book, full sample and OOS window alone.

CAVEATS carried, not buried
    * Survivorship: all three panels are current-constituent lists (idea 54).
    * Idea 49/39: the eligibility gate is INVERTED on the small panel, so its numbers are about
      a gate that does not work there; reported, not traded.
    * Idea 38 (calendar-day price index) and idea 126 (t+1 execution only) carry over.
    * Idea 128: the IS window's SPY drawdown is shallower than the OOS window's.
    * A ladder in one exponent on one realised path is not a factor study; it prices THIS
      book's dial, nothing else.

HARNESS
    `baseline` (the live rules), idea 129's panel/4b-bar machinery and idea 94's window/halves
    machinery are IMPORTED, so the panels, the control arm and the bars are the committed ones.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .curve.csv, .band.csv,
.argmax.csv, .walkforward.csv.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_the-sign-is-the-parameter-not-the-share_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
C = _load(I129, "i129")

FREQ = "W"
COSTS = [0.0, 10.0, 25.0]
PANELS = ["u56", "broad", "small"]
LARGE = ["u56", "broad"]
OOS_START, IS_END = H.OOS_START, H.IS_END
PHI0, DELTA0 = 0.70, 0.60
GROSS, MAX_VOL = 0.75, 0.60

KGRID = [-1.00, -0.75, -0.50, -0.25, 0.00, 0.25, 0.50, 0.75, 1.00]   # tuned parameter 1
SHARES = [0.20, 0.53, 0.85]                                          # tuned parameter 2
CONSTR = ["lit", "norm"]                                             # reported axis
K_LIVE, K_ZERO, K_POS = -0.50, 0.00, 0.50

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 900)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ------------------------------------------------------------------ the book (idea 81/153/159 verbatim, k generalised)
def parts(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True)
            + r3.rank(axis=1, pct=True)) / 3
    above = px > px.rolling(200).mean()
    v = px.pct_change().rolling(20).std() * np.sqrt(252)
    return comp * (0.5 + 0.5 * above.astype(float)), above, v


_PARTS = {}


def base_parts(px, pk):
    if pk not in _PARTS:
        _PARTS[pk] = parts(px)
    return _PARTS[pk]


_SC = {}


def score_of(px, k, pk):
    """score_k = composite * clip(vol20, 0.08) ** k.  k = -0.5 is RULES v1 exactly."""
    key = (pk, round(k, 4))
    if key not in _SC:
        s, above, v = base_parts(px, pk)
        _SC[key] = s * (v.clip(lower=0.08) ** k)
    return _SC[key]


def held_mask(px, k, n, pk):
    s = score_of(px, k, pk)
    _, above, v = base_parts(px, pk)
    rank = s.where(above & (v < MAX_VOL)).rank(axis=1, ascending=False)
    return rank <= n


def weights(px, k, n, pk, constr="lit"):
    m = held_mask(px, k, n, pk).astype(float)
    if constr == "lit":
        return m * (GROSS / n)
    kk = m.sum(axis=1).replace(0, np.nan)
    return m.div(kk, axis=0).fillna(0.0) * GROSS


def eligible_mask(px, pk):
    _, above, v = base_parts(px, pk)
    return above & (v < MAX_VOL)


def net(r0, to, c):
    return r0 - to * c / 1e4


def win(r, which):
    return H.window(r, which)


def mtr(r):
    if len(r) < 60:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    return metrics(r)


def spearman(a, b):
    return H.spearman(a, b)


# ------------------------------------------------------------------ beneficial band
def band_of(ks, d):
    """Maximal contiguous run of grid points containing the argmax on which d >= 0.
    Endpoints located by linear interpolation to the first outside point; a band that runs
    to the grid edge is reported open at that edge (NaN endpoint, flag)."""
    ks, d = np.asarray(ks, float), np.asarray(d, float)
    ok = np.isfinite(d)
    if ok.sum() < 3:
        return dict(lo=np.nan, hi=np.nan, open_lo=True, open_hi=True, kmax=np.nan, dmax=np.nan)
    i0 = int(np.nanargmax(np.where(ok, d, -np.inf)))
    if d[i0] < 0:
        return dict(lo=np.nan, hi=np.nan, open_lo=False, open_hi=False, kmax=ks[i0], dmax=d[i0])
    lo_i = i0
    while lo_i - 1 >= 0 and np.isfinite(d[lo_i - 1]) and d[lo_i - 1] >= 0:
        lo_i -= 1
    hi_i = i0
    while hi_i + 1 < len(d) and np.isfinite(d[hi_i + 1]) and d[hi_i + 1] >= 0:
        hi_i += 1
    if lo_i == 0:
        lo, open_lo = np.nan, True
    else:
        x0, x1, y0, y1 = ks[lo_i - 1], ks[lo_i], d[lo_i - 1], d[lo_i]
        lo, open_lo = float(x0 + (x1 - x0) * (0 - y0) / (y1 - y0)), False
    if hi_i == len(d) - 1:
        hi, open_hi = np.nan, True
    else:
        x0, x1, y0, y1 = ks[hi_i], ks[hi_i + 1], d[hi_i], d[hi_i + 1]
        hi, open_hi = float(x0 + (x1 - x0) * (0 - y0) / (y1 - y0)), False
    return dict(lo=lo, hi=hi, open_lo=open_lo, open_hi=open_hi, kmax=ks[i0], dmax=d[i0])


def main():
    say("=" * 195)
    say(f"IDEA 168 — the-sign-is-the-parameter-not-the-share   ({STEM})")
    say("Is the live tilt exponent k = -0.5 a choice on a curve with an interior optimum, or "
        "the wrong end of a monotone one?  Ladder k, report the argmax and the beneficial band.")
    say("=" * 195)

    ref, grid_rows, curve_rows, band_rows, amax_rows, wf_rows = {}, [], [], [], [], []
    RET = {}   # (pk, constr, m, k) -> (r0, turnover)

    # ---------------------------------------------------------------- panels + reproduction
    say("\n" + "-" * 195)
    say("REPRODUCTION GATE (asserted before any new number is read)")
    say("-" * 195)
    ELIG_REF = {"u56": 37.5, "broad": 91.5, "small": 141.2}
    NMAP_REF = {("u56", 0.53): 20, ("u56", 0.20): 7, ("broad", 0.53): 48}
    gate = []

    for pk in PANELS:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bfull, bIS, bOOS = (C.bars_win(spy, w) for w in ("full", "IS", "OOS"))
        v1res = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=FREQ)
        v1r0, v1to = v1res["returns"].loc[start:], v1res["turnover"].loc[start:]
        v1 = {c: net(v1r0, v1to, c) for c in COSTS}
        el = eligible_mask(px, pk).loc[start:]
        n_elig = float(el.sum(axis=1).mean())
        nmap = {m: max(2, int(round(m * n_elig))) for m in SHARES}
        ref[pk] = dict(px=px, start=start, spy=spy, bfull=bfull, bIS=bIS, bOOS=bOOS,
                       v1=v1, n_elig=n_elig, desc=desc, nmap=nmap,
                       ms=metrics(spy), mso=metrics(spy.loc[OOS_START:]),
                       msi=metrics(win(spy, "IS")))
        ms, mso = ref[pk]["ms"], ref[pk]["mso"]
        say(f"\n[panel] {pk} = {desc}: {px.shape[1]} cols, eval from {start.date()}, "
            f"mean weekly eligible names {n_elig:.1f} (idea 153 ref {ELIG_REF[pk]})")
        say("    share -> n:  " + ", ".join(f"m={m:.2f}->n={nmap[m]}" for m in SHARES))
        say(f"    SPY full {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%} halves "
            f"{bfull['s1']:.3f}/{bfull['s2']:.3f} | OOS {mso['CAGR']:.2%}/{mso['Sharpe']:.3f}"
            f"/{mso['MaxDD']:.2%}")
        gate.append(("[a] mean eligible " + pk, n_elig, ELIG_REF[pk], 0.15))
        for (p2, m2), nref in NMAP_REF.items():
            if p2 == pk:
                gate.append((f"[b] n at m={m2:.2f} {pk}", nmap[m2], nref, 0.001))

    # cost identity [e] on one book
    pk = "u56"
    px, start = ref[pk]["px"], ref[pk]["start"]
    W = weights(px, K_LIVE, ref[pk]["nmap"][0.53], pk, "lit")
    a0 = backtest(px, W, cost_bps=0.0, freq=FREQ)
    a10 = backtest(px, W, cost_bps=10.0, freq=FREQ)
    ident = float((net(a0["returns"], a0["turnover"], 10.0) - a10["returns"]).abs().max())
    gate.append(("[e] cost identity max|diff|", ident, 0.0, 1e-12))

    # ---------------------------------------------------------------- the grid
    say("\n" + "-" * 195)
    say("GRID — one 0 bps run per (panel, constr, share, k); 10/25 bps derived exactly")
    say("-" * 195)
    for pk in PANELS:
        px, start = ref[pk]["px"], ref[pk]["start"]
        for constr in CONSTR:
            for m in SHARES:
                n = ref[pk]["nmap"][m]
                for k in KGRID:
                    W = weights(px, k, n, pk, constr)
                    res = backtest(px, W, cost_bps=0.0, freq=FREQ)
                    r0, to = res["returns"].loc[start:], res["turnover"].loc[start:]
                    RET[(pk, constr, m, k)] = (r0, to)
                say(f"  ran {pk}/{constr}/m={m:.2f} (n={n}) x {len(KGRID)} k-points")

    # ---------------------------------------------------------------- levels, 4a/4b, curves
    for pk in PANELS:
        R = ref[pk]
        for constr in CONSTR:
            for m in SHARES:
                n = R["nmap"][m]
                for c in COSTS:
                    base_c = None
                    lvl = {}
                    for k in KGRID:
                        r0, to = RET[(pk, constr, m, k)]
                        r = net(r0, to, c)
                        mf, mi, mo = mtr(r), mtr(win(r, "IS")), mtr(win(r, "OOS"))
                        h1, h2 = H.halves(r)
                        mgf = C.margins_at(r, R["bfull"], PHI0, DELTA0, "full")
                        mgo = C.margins_at(r, R["bOOS"], PHI0, DELTA0, "OOS")
                        p4a = H.pass4a(r, R["v1"][c])
                        p4b_full = not C.fails(mgf)
                        p4b_oos = not C.fails(mgo)
                        lvl[k] = dict(CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"],
                                      IS_S=mi["Sharpe"], OOS_S=mo["Sharpe"],
                                      OOS_C=mo["CAGR"], OOS_D=mo["MaxDD"],
                                      turnover=float(to.sum() / (len(to) / 252)))
                        grid_rows.append(dict(
                            panel=pk, constr=constr, m=m, n=n, k=k, cost=c,
                            CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"],
                            H1=h1, H2=h2, IS_Sharpe=mi["Sharpe"], OOS_CAGR=mo["CAGR"],
                            OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            ann_turnover=lvl[k]["turnover"],
                            pass4a=p4a, pass4b_full=p4b_full, pass4b_oos=p4b_oos,
                            fails4b_full=";".join(C.fails(mgf)) or "-",
                            fails4b_oos=";".join(C.fails(mgo)) or "-"))
                    base_c = lvl[K_ZERO]
                    for k in KGRID:
                        curve_rows.append(dict(
                            panel=pk, constr=constr, m=m, n=n, cost=c, k=k,
                            CAGR=lvl[k]["CAGR"], Sharpe=lvl[k]["Sharpe"],
                            dCAGR=lvl[k]["CAGR"] - base_c["CAGR"],
                            dSharpe=lvl[k]["Sharpe"] - base_c["Sharpe"],
                            dCAGR_OOS=lvl[k]["OOS_C"] - base_c["OOS_C"],
                            dSharpe_OOS=lvl[k]["OOS_S"] - base_c["OOS_S"]))
                    ks = KGRID
                    dC = [lvl[k]["CAGR"] - base_c["CAGR"] for k in ks]
                    dS = [lvl[k]["Sharpe"] - base_c["Sharpe"] for k in ks]
                    bC, bS = band_of(ks, dC), band_of(ks, dS)
                    band_rows.append(dict(panel=pk, constr=constr, m=m, n=n, cost=c,
                                          metric="CAGR", **bC))
                    band_rows.append(dict(panel=pk, constr=constr, m=m, n=n, cost=c,
                                          metric="Sharpe", **bS))
                    neg = [k for k in ks if k <= 0]
                    amax_rows.append(dict(
                        panel=pk, constr=constr, m=m, n=n, cost=c,
                        argmax_CAGR=ks[int(np.nanargmax([lvl[k]["CAGR"] for k in ks]))],
                        argmax_Sharpe=ks[int(np.nanargmax([lvl[k]["Sharpe"] for k in ks]))],
                        argmax_IS_Sharpe=ks[int(np.nanargmax([lvl[k]["IS_S"] for k in ks]))],
                        argmax_OOS_Sharpe=ks[int(np.nanargmax([lvl[k]["OOS_S"] for k in ks]))],
                        sp_k_dCAGR=spearman(ks, dC),
                        sp_k_dSharpe=spearman(ks, dS),
                        sp_negk_dCAGR=spearman(neg, [lvl[k]["CAGR"] - base_c["CAGR"] for k in neg]),
                        sp_negk_dSharpe=spearman(neg, [lvl[k]["Sharpe"] - base_c["Sharpe"] for k in neg]),
                        live_minus_zero_CAGR=lvl[K_LIVE]["CAGR"] - base_c["CAGR"],
                        live_minus_zero_Sharpe=lvl[K_LIVE]["Sharpe"] - base_c["Sharpe"],
                        pos_minus_zero_CAGR=lvl[K_POS]["CAGR"] - base_c["CAGR"]))

    G = pd.DataFrame(grid_rows)
    CU = pd.DataFrame(curve_rows)
    BD = pd.DataFrame(band_rows)
    AX = pd.DataFrame(amax_rows)

    # reproduction [c]/[d] read off the curve
    for pk, refv in (("u56", 0.0283), ("broad", 0.0275)):
        q = CU[(CU.panel == pk) & (CU.constr == "lit") & (CU.m == 0.20)
               & (CU.cost == 10.0) & (CU.k == K_POS)]
        gate.append((f"[c] dCAGR(k=+0.5) m=0.20 10bps {pk}", float(q["dCAGR"].iloc[0]), refv, 0.0010))
    q = CU[(CU.panel == "u56") & (CU.constr == "lit") & (CU.m == 0.53)
           & (CU.cost == 0.0) & (CU.k == K_LIVE)]
    gate.append(("[d] dCAGR(k=-0.5) m=0.53 0bps u56", float(q["dCAGR"].iloc[0]), -0.0268, 0.0020))

    say("")
    n_ok = 0
    for nm, got, want, tol in gate:
        ok = abs(got - want) <= tol
        n_ok += ok
        say(f"  {'PASS' if ok else 'FAIL'}  {nm:<44s} got {got:+.6f}  ref {want:+.6f}  tol {tol:g}")
    say(f"\n  reproduction: {n_ok} of {len(gate)} anchors reproduced.")

    # ---------------------------------------------------------------- P2/P3/P4 read-out
    say("\n" + "-" * 195)
    say("THE k-CURVE — signed dCAGR vs the k = 0 control, at 10 bps, literal construction")
    say("-" * 195)
    for pk in PANELS:
        for m in SHARES:
            q = CU[(CU.panel == pk) & (CU.constr == "lit") & (CU.m == m) & (CU.cost == 10.0)]
            q = q.set_index("k").reindex(KGRID)
            say(f"\n  {pk}  m={m:.2f}  n={int(q['n'].iloc[0])}")
            say("    k        " + "".join(f"{k:>9.2f}" for k in KGRID))
            say("    CAGR     " + "".join(f"{v:>8.2%} " for v in q["CAGR"]))
            say("    dCAGR    " + "".join(f"{v:>+8.2%} " for v in q["dCAGR"]))
            say("    Sharpe   " + "".join(f"{v:>9.3f}" for v in q["Sharpe"]))
            say("    dSharpe  " + "".join(f"{v:>+9.3f}" for v in q["dSharpe"]))

    say("\n" + "-" * 195)
    say("ARGMAX AND MONOTONICITY (all cells, all costs, both constructions)")
    say("-" * 195)
    say(AX.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say("\n" + "-" * 195)
    say("BENEFICIAL BAND — endpoints of the maximal dCAGR >= 0 run containing the argmax")
    say("-" * 195)
    say(BD.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    lc = AX[AX.panel.isin(LARGE)]
    inc = lc[lc.m == 0.53]
    P2 = bool((inc["sp_negk_dCAGR"] >= 0.6).all())
    P3 = bool((inc["argmax_Sharpe"] >= 0).all())
    span = float(lc["argmax_Sharpe"].max() - lc["argmax_Sharpe"].min())
    P4 = bool(span >= 0.50)
    say(f"\n  P2 Spearman(k<=0, dCAGR) >= +0.6 at m=0.53 on both large-cap panels: "
        f"{P2}  values {[round(v,3) for v in inc['sp_negk_dCAGR']]}")
    say(f"  P3 full-sample Sharpe argmax k >= 0 at m=0.53 on both large-cap panels: "
        f"{P3}  values {sorted(set(inc['argmax_Sharpe']))}")
    say(f"  P4 argmax_Sharpe span across large-cap cells = {span:.2f} (>= 0.50 -> {P4})")

    # ---------------------------------------------------------------- 4a / 4b census
    say("\n" + "-" * 195)
    say("KEEP-PATH CENSUS — every book, both paths, full sample and OOS window")
    say("-" * 195)
    cen = (G.groupby(["panel", "cost"])[["pass4a", "pass4b_full", "pass4b_oos"]]
             .sum().astype(int))
    cen["books"] = G.groupby(["panel", "cost"]).size()
    say(cen.to_string())
    G["pass4b_both"] = G["pass4b_full"] & G["pass4b_oos"]
    P6 = not bool(G[(G.panel.isin(LARGE)) & (G.cost >= 10.0) & G["pass4b_both"]].shape[0])
    say(f"\n  P6 no large-cap book at any k passes 4b full AND OOS at 10/25 bps: {P6}")
    if not P6:
        say(G[(G.panel.isin(LARGE)) & (G.cost >= 10.0) & G["pass4b_both"]].to_string(index=False))
    win4a = G[(G.cost >= 10.0) & G["pass4a"]]
    say(f"  4a passers at 10/25 bps: {len(win4a)} of {len(G[G.cost >= 10.0])}")
    if len(win4a):
        say(win4a.sort_values("Sharpe", ascending=False).head(12).to_string(index=False))

    # ---------------------------------------------------------------- rule 8 walk-forward
    say("\n" + "-" * 195)
    say("WALK-FORWARD (PROTOCOL rule 8) — k chosen on IS 2009-2016 only, read once on OOS 2017-2026")
    say("-" * 195)
    for pk in PANELS:
        R = ref[pk]
        for constr in CONSTR:
            for m in SHARES:
                n = R["nmap"][m]
                for c in (10.0, 25.0):
                    isS = {k: mtr(win(net(*RET[(pk, constr, m, k)], c), "IS"))["Sharpe"]
                           for k in KGRID}
                    k_is = KGRID[int(np.nanargmax([isS[k] for k in KGRID]))]
                    picks = dict(S_IS=k_is, S_ZERO=K_ZERO, S_INV=K_LIVE, S_POS=K_POS)
                    v1o = win(R["v1"][c], "OOS")
                    mv1, msp = mtr(v1o), R["mso"]
                    for sel, k in picks.items():
                        r = net(*RET[(pk, constr, m, k)], c)
                        ro, ri = win(r, "OOS"), win(r, "IS")
                        mo = mtr(ro)
                        mgo = C.margins_at(r, R["bOOS"], PHI0, DELTA0, "OOS")
                        wf_rows.append(dict(
                            panel=pk, constr=constr, m=m, n=n, cost=c, selector=sel, k=k,
                            IS_Sharpe=mtr(ri)["Sharpe"],
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            v1_OOS_CAGR=mv1["CAGR"], v1_OOS_Sharpe=mv1["Sharpe"],
                            v1_OOS_MaxDD=mv1["MaxDD"],
                            spy_OOS_CAGR=msp["CAGR"], spy_OOS_Sharpe=msp["Sharpe"],
                            spy_OOS_MaxDD=msp["MaxDD"],
                            beats_v1_OOS=bool(mo["Sharpe"] > mv1["Sharpe"]),
                            beats_spy_OOS=bool(mo["Sharpe"] > msp["Sharpe"]),
                            pass4a_OOS=H.pass4a(ro, v1o),
                            pass4b_OOS=not C.fails(mgo),
                            fails4b_OOS=";".join(C.fails(mgo)) or "-"))
    WF = pd.DataFrame(wf_rows)
    say(WF.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say("\n  mean OOS Sharpe by selector (all cells / large-cap cells only):")
    a = WF.groupby("selector")["OOS_Sharpe"].mean()
    b = WF[WF.panel.isin(LARGE)].groupby("selector")["OOS_Sharpe"].mean()
    cc = WF[WF.panel.isin(LARGE)].groupby("selector")["OOS_CAGR"].mean()
    say(pd.DataFrame({"OOS_Sharpe_all": a, "OOS_Sharpe_large": b,
                      "OOS_CAGR_large": cc}).to_string(float_format=lambda x: f"{x:.4f}"))

    piv = WF.pivot_table(index=["panel", "constr", "m", "cost"], columns="selector",
                         values="OOS_Sharpe")
    wins = int((piv["S_IS"] > piv["S_ZERO"]).sum())
    ties = int((piv["S_IS"] == piv["S_ZERO"]).sum())
    P5 = not bool(b["S_IS"] > b["S_ZERO"])
    say(f"\n  paired S_IS vs S_ZERO on OOS Sharpe: S_IS wins {wins} of {len(piv)} cells "
        f"({ties} ties, i.e. IS chose k=0)")
    say(f"  mean OOS Sharpe S_IS {b['S_IS']:.4f} vs S_ZERO {b['S_ZERO']:.4f} "
        f"(large-cap) -> P5 (fitting does NOT beat the constant) = {P5}")
    say("  paired table:")
    say(piv.to_string(float_format=lambda x: f"{x:.3f}"))

    hit = float((AX[AX.panel.isin(LARGE)]["argmax_IS_Sharpe"]
                 == AX[AX.panel.isin(LARGE)]["argmax_OOS_Sharpe"]).mean())
    say(f"\n  IS argmax k == OOS argmax k in {hit:.1%} of large-cap cells "
        f"(9-point grid, chance 11.1%)")
    say(f"  Spearman(IS argmax k, OOS argmax k) over large-cap cells = "
        f"{spearman(AX[AX.panel.isin(LARGE)]['argmax_IS_Sharpe'], AX[AX.panel.isin(LARGE)]['argmax_OOS_Sharpe']):.3f}")

    # ---------------------------------------------------------------- verdict
    say("\n" + "=" * 195)
    say("PREDICTION SCORECARD")
    say("=" * 195)
    for nm, got in (("P1 reproduction", n_ok == len(gate)), ("P2 monotone on k<=0", P2),
                    ("P3 argmax >= 0", P3), ("P4 argmax not sharply identified", P4),
                    ("P5 IS chooser does not beat k=0", P5), ("P6 no 4b passer", P6)):
        say(f"  {nm:<40s} {'CONFIRMED' if got else 'FALSIFIED'}")

    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    CU.to_csv(OUT / f"{STEM}.curve.csv", index=False)
    BD.to_csv(OUT / f"{STEM}.band.csv", index=False)
    AX.to_csv(OUT / f"{STEM}.argmax.csv", index=False)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")
    say(f"\nwrote {STEM}.grid.csv/.curve.csv/.band.csv/.argmax.csv/.walkforward.csv/.console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
