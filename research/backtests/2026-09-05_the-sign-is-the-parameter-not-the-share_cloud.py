#!/usr/bin/env python3
"""QUEUE idea 168 — the-sign-is-the-parameter-not-the-share  (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 168)
    "idea 159 showed the live INV tilt is affordable at every share (g/c = 16-4254 on the honest
     cost bar) and wrong-signed at all 20 large-cap (panel, share) points, while POS is
     right-signed at 19 of 20.  That makes the tilt EXPONENT, not its presence, the live dial:
     sweep k in composite x vol20^k over k in {-0.5, -0.25, 0, +0.25, +0.5} on both large-cap
     panels at 10/25 bps and report where signed dCAGR crosses zero, with rule 8.  If the argmax
     k is at or near 0 the fifth delete-the-scaler finding becomes a measured optimum rather
     than a comparison of three points.  Max 2 params."

WHAT IS AT STAKE.
    RULES v1 ranks on `composite / sqrt(vol20)`, i.e. k = -0.5 in the family
        s_k = composite x vol20^k .
    The project has now found five separate times that DELETING the scaler (k = 0) beats keeping
    it, and idea 159 found the k = +0.5 book (POS) right-signed on 19 of 20 large-cap points
    while the live k = -0.5 book (INV) was wrong-signed on 20 of 20.  Every one of those findings
    compares THREE POINTS: -0.5, 0, +0.5.  Three points cannot tell "the scaler is upside down"
    (argmax at +0.5, keep tilting harder) from "the scaler is noise" (argmax at 0, delete it) from
    "there is a shallow interior optimum" (argmax strictly between).  The exponent is a
    continuous dial and has never been swept.  Sweeping it turns a qualitative claim about a sign
    into a located optimum with a curve around it — or shows the curve is flat, in which case the
    live -0.5 is not merely suboptimal but arbitrary, and RULES should say so.

    The narrow reading of "where signed dCAGR crosses zero" is the k at which the tilt stops
    paying relative to the no-tilt control (k = 0).  Since dCAGR(k=0) = 0 identically, the
    crossing on the POSITIVE side is the interesting one and is what is reported; the crossing on
    the negative side is where the live tilt's sign flips and is reported beside it.

CORPUS — both large-cap panels, both cost rungs, the standing share ladder
    2 panels x 11 exponents x 8 shares x 2 cost rungs = 352 books, weekly, t+1, gross 0.75 spread
    over the names actually held (idea 153/159's `norm` construction).  Every book is a strict
    member of the family above; nothing else about the book changes with k, so dCAGR(k) isolates
    the exponent.
      Panels  u56 (universe.json, 56 names), broad (universe_broad.json, 136 names).
              The small panel is EXCLUDED by idea 168's own wording ("both large-cap panels")
              and because ideas 39/49 found the eligibility gate inverted there.
      Shares  0.05 0.10 0.15 0.20 0.27 0.35 0.53 0.75, as n = max(2, round(m x mean weekly
              eligible count)).  m = 1.00 is DROPPED: at full share every k holds the same set
              and dCAGR -> 0 mechanically (idea 153's confound (i)), which would plant a
              spurious zero-crossing at the top of the ladder.  That exclusion is pre-registered.
      Costs   10 and 25 bps.
    RULES v1 (n=5, w=0.15) and SPY are the two references PROTOCOL rule 3 requires.

TUNED PARAMETERS — exactly two, swept exhaustively, ALL grid points in .grid.csv:
    1. the tilt exponent k, 11 values:
         -1.00 -0.75 -0.50 -0.25 -0.10  0.00  +0.10 +0.25 +0.50 +0.75 +1.00
       idea 168's five requested values are a strict subset; the grid is widened symmetrically
       so an argmax at an endpoint is visible as an endpoint rather than mistaken for an
       interior optimum.  k = -0.50 is RULES v1's live value, k = 0.00 the no-scaler control.
    2. the book share m, 8 values above.  Idea 159/153 established share governs the MAGNITUDE
       any cross-sectional key can express, so a k-curve read at one share is not a result; the
       share axis is swept and every cell reported.
    Panel and cost rung are REPORTED CORPUS AXES, never selected on.

WHAT IS MEASURED, per (panel, cost, share)
    dCAGR(k)   = CAGR(book at k) - CAGR(book at k = 0), in pp/yr, SIGNED (not |.| — idea 168 is
                 explicitly about the sign; idea 159's |.| functional answered a different
                 question).
    k*         = argmax_k dCAGR(k) on the grid, and the parabolic-refined argmax through the
                 three points around it (reported separately; a refinement, never a new grid).
    k0+        = the smallest k > 0 at which dCAGR crosses back below zero (linear interpolation
                 between grid points); NaN if it never does on the grid.
    k0-        = the largest k < 0 at which dCAGR crosses below zero going left from 0.
    cost_k     = [Turnover(k) - Turnover(0)] x cost_bps, annualised — the extra bill the tilt
                 runs up, so "pays" can be read net as well as raw.  Both are reported.
    dSharpe(k) and dMaxDD(k) against the same k = 0 control.

FLATNESS TEST (idea 128's plateau instrument, applied to this dial)
    An argmax means nothing if the curve is flat.  For every (panel, cost, share) the SPREAD
    max_k dCAGR - min_k dCAGR is reported next to the extra cost of the tilt, and the whole
    curve's Sharpe range is compared against where the k = 0 control sits inside it.  If the
    Sharpe range across the entire exponent axis is smaller than the range across two adjacent
    shares, the exponent is not a live dial and the honest instruction is "do not scale".

WALK-FORWARD (PROTOCOL rule 8) — everything chosen on 2009-2016 only, read ONCE on 2017-2026.
    Arms, fixed before any OOS number is read, per (panel, cost):
      A_LIVE   k = -0.50, the live RULES v1 exponent, at the IS-Sharpe-best share  (no choice of k)
      A_ZERO   k =  0.00, the no-scaler control, at the same share                 (no choice of k)
      A_ISK    k chosen as the IS-window dCAGR argmax at the IS-Sharpe-best share  (k IS chosen)
      A_ISKS   (k, share) chosen jointly as the IS-window Sharpe argmax over all 88 books
    OOS CAGR / Sharpe / MaxDD reported against RULES v1 on the same panel and cost, and SPY.
    The pre-registered question rule 8 answers: does the IS-chosen exponent beat the two fixed
    exponents out of sample?  If A_ISK does not beat A_ZERO, the sweep has found no dial.
BOTH KEEP PATHS (4a and 4b) are evaluated on all 352 books, full sample and OOS window.

REPRODUCTION, asserted before any new number is read
    [a] k = -0.50 must reproduce idea 159's committed INV book and k = +0.50 its POS book, and
        k = 0.00 its NONE book, cell-for-cell on CAGR/Sharpe/MaxDD/H1/H2 at the 8 shared shares
        of the 10 bps grid.  If [a] fails, this is not the family idea 159 measured and no
        statement below is about the live tilt.
    [b] idea 168's own premise: signed dCAGR of k = -0.50 must be NEGATIVE at all 8 shares on
        both large-cap panels, and k = +0.50 positive at nearly all of them.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a] reproduces exactly; [b] reproduces idea 159's 20-of-20 / 19-of-20 signs on the 16
        shared (panel, share) points at 10 bps.
    P2  dCAGR(k) is monotone INCREASING in k over most of the grid, so the grid argmax sits at
        or near the +1.00 endpoint rather than at an interior optimum.  If so, "the sign is the
        parameter" is right but the answer is not "delete the scaler" — it is "invert it", which
        is a strictly stronger and more uncomfortable claim than any of the five prior findings.
    P3  The POSITIVE zero-crossing k0+ does NOT exist on the grid (the curve does not come back
        down inside |k| <= 1), i.e. idea 168's headline quantity is unbounded above on this grid.
        Reporting that honestly, rather than extrapolating, is the result.
    P4  The curve is SHALLOW relative to the share axis: the Sharpe range across all 11
        exponents is smaller than the range across the 8 shares at fixed k.  The exponent is a
        second-order dial.
    P5  Rule 8: A_ISK does NOT beat A_ZERO out of sample by a meaningful margin, because a
        shallow curve makes an IS argmax mostly noise.  A_LIVE is the worst of the three.
    P6  Nothing here is a KEEP.  The deliverable is a measured curve and, if P2 holds, an
        argument that RULES v1's k = -0.5 is on the wrong side of zero.

CAVEATS carried, not buried
    * SURVIVORSHIP.  Both panels are current-constituent lists (idea 54).  A vol tilt is exactly
      the instrument survivorship flatters most in the POSITIVE direction: the high-vol names
      that blew up and left the index are absent, so +k books are measured without their worst
      constituents.  Any finding that "tilt harder toward high vol" is therefore an UPPER BOUND
      and must not be read as a tradable instruction.  This caveat is the main reason P2, if it
      holds, is a finding about the panel and not a proposed rule change.
    * The 25 bps rung is a robustness axis, not a claim about realised costs; both are reported.
    * vol20 is floored at 0.08 before exponentiation (idea 81's convention, carried verbatim),
      so very low-vol names cannot dominate a negative-k book by division blow-up.
    * dCAGR is a full-sample difference of two compounded numbers and inherits path dependence;
      dSharpe and dMaxDD are reported beside it so no single statistic carries the verdict.
    * Idea 153's confound (i) is handled by dropping m = 1.00, but it still shades m = 0.75.
    * Idea 38 (calendar-day price index) and idea 126 (t+1 execution) carry over unchanged.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .curve.csv, .crossing.csv,
.walkforward.csv, .repro.csv.
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
from baseline import rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_the-sign-is-the-parameter-not-the-share_cloud"
OUT = ROOT / "research" / "backtests"
I159P = OUT / "2026-09-05_the-share-at-which-ranking-stops-paying_cloud.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


I159 = _load(I159P, "i159")
C, H, I153 = I159.C, I159.H, I159.I153

FREQ, GROSS, MAX_VOL, VFLOOR = "W", 0.75, 0.60, 0.08
PANELS = ["u56", "broad"]
KS = [-1.00, -0.75, -0.50, -0.25, -0.10, 0.00, 0.10, 0.25, 0.50, 0.75, 1.00]
SHARES = [0.05, 0.10, 0.15, 0.20, 0.27, 0.35, 0.53, 0.75]
COSTS = [10.0, 25.0]
IS_END, OOS_START = H.IS_END, H.OOS_START
K_LIVE, K_ZERO = -0.50, 0.00

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 900)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ------------------------------------------------------------------ the exponent family
_SC = {}


def score_k(px, k, pk):
    """idea 81's composite (imported verbatim through idea 153) times vol20^k.
    k = -0.5 is RULES v1's live `comp / sqrt(vol20)`; k = +0.5 is idea 159's POS; k = 0 is NONE."""
    ck = (pk, round(k, 4))
    if ck in _SC:
        return _SC[ck]
    comp, above, v = I153.parts(px)
    vv = v.clip(lower=VFLOOR)
    hv = vv ** 0.5                     # idea 159/81's `sqrt(vol20)` object, verbatim
    # The three exponents idea 159 published are computed by ITS arithmetic route, so
    # reproduction [a] is bit-exact.  x**-0.5 and 1/(x**0.5) differ by one ulp, which flipped a
    # rank tie in 2 of 48 reproduction cells (max CAGR gap 0.0125pp) before this was pinned.
    # The mathematical function is identical; only the floating-point route is pinned.
    if k == 0.0:
        s = comp
    elif k == -0.5:
        s = comp / hv
    elif k == 0.5:
        s = comp * hv
    else:
        s = comp * vv ** k
    _SC[ck] = (s, above, v)
    return _SC[ck]


def weights_k(px, k, n, pk):
    """idea 153's `norm` construction: gross 0.75 spread over the names actually held."""
    s, above, v = score_k(px, k, pk)
    m = (s.where(above & (v < MAX_VOL)).rank(axis=1, ascending=False) <= n).astype(float)
    cnt = m.sum(axis=1).replace(0, np.nan)
    return m.div(cnt, axis=0).fillna(0.0) * GROSS


def cross_up_to_down(ks, ys, side):
    """Interpolated k at which the signed dCAGR curve crosses zero, walking away from k = 0.
    side='+' walks right from 0 and returns the first k>0 where y goes from >=0 to <0;
    side='-' walks left from 0 and returns the first k<0 where y goes from >=0 to <0."""
    ks, ys = np.asarray(ks, float), np.asarray(ys, float)
    o = np.argsort(ks)
    ks, ys = ks[o], ys[o]
    i0 = int(np.argmin(np.abs(ks)))
    rng = range(i0, len(ks) - 1) if side == "+" else range(i0, 0, -1)
    for i in rng:
        j = i + 1 if side == "+" else i - 1
        a, b = ys[i], ys[j]
        if a >= 0 and b < 0:
            return float(ks[i] + (ks[j] - ks[i]) * a / (a - b))
    return np.nan


def parab(ks, ys):
    """Parabolic refinement of the grid argmax through its two neighbours.  A refinement of a
    grid point, never a new grid point: NaN when the argmax is at an endpoint."""
    ks, ys = np.asarray(ks, float), np.asarray(ys, float)
    o = np.argsort(ks)
    ks, ys = ks[o], ys[o]
    i = int(np.argmax(ys))
    if i in (0, len(ks) - 1):
        return np.nan
    x0, x1, x2 = ks[i - 1], ks[i], ks[i + 1]
    y0, y1, y2 = ys[i - 1], ys[i], ys[i + 1]
    d = (x0 - x1) * (x0 - x2) * (x1 - x2)
    if abs(d) < 1e-15:
        return np.nan
    A = (x2 * (y1 - y0) + x1 * (y0 - y2) + x0 * (y2 - y1)) / d
    B = (x2 * x2 * (y0 - y1) + x1 * x1 * (y2 - y0) + x0 * x0 * (y1 - y2)) / d
    return np.nan if abs(A) < 1e-15 else float(-B / (2 * A))


def main():
    t0 = time.time()
    say("=" * 205)
    say(f"IDEA 168 — the-sign-is-the-parameter-not-the-share   ({STEM})")
    say("Sweep the tilt EXPONENT k in composite x vol20^k on both large-cap panels at 10/25 bps; "
        "report signed dCAGR(k), its argmax, and where it crosses zero.  Rule 8 throughout.")
    say("PRE-REGISTERED: exactly 2 tuned params (exponent k x 11, book share m x 8). Panel and "
        "cost rung are carried corpus axes, never selected on.  m = 1.00 dropped a priori "
        "(idea 153 confound (i)).")
    say(f"Corpus: {len(PANELS)} panels x {len(KS)} exponents x {len(SHARES)} shares x "
        f"{len(COSTS)} costs = {len(PANELS)*len(KS)*len(SHARES)*len(COSTS)} books.")
    say(f"k = {K_LIVE:+.2f} is RULES v1's live scaler; k = {K_ZERO:+.2f} the no-scaler control; "
        f"k = +0.50 idea 159's POS.")
    say("=" * 205)

    ref = {}
    for pk in PANELS:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        el = I153.eligible_mask(px, pk).loc[start:]
        n_elig = float(el.sum(axis=1).mean())
        bars = dict(full=C.bars_win(spy, "full"), IS=C.bars_win(spy, "IS"),
                    OOS=C.bars_win(spy, "OOS"))
        ms, mo = metrics(spy), metrics(spy.loc[OOS_START:])
        ref[pk] = dict(px=px, start=start, spy=spy, bars=bars, n_elig=n_elig, desc=desc,
                       nmap={m: max(2, int(round(m * n_elig))) for m in SHARES},
                       spy_m=ms, spy_oos=mo)
        say(f"\n[panel] {pk} = {desc}: {px.shape[1]} cols, eval {start.date()} -> "
            f"{px.index[-1].date()}, mean weekly eligible {n_elig:.1f}")
        say("    share -> n:  " + ", ".join(f"{m:.3g}->{ref[pk]['nmap'][m]}" for m in SHARES))
        say(f"    SPY  {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%} halves "
            f"{bars['full']['s1']:.3f}/{bars['full']['s2']:.3f} | OOS {mo['CAGR']:.2%}/"
            f"{mo['Sharpe']:.3f}/{mo['MaxDD']:.2%}")
        say(f"    4b bars: H1>{bars['full']['s1']:.3f} H2>{bars['full']['s2']:.3f} "
            f"OOS>{bars['full']['soos']:.3f} |MaxDD|<={0.60*abs(bars['full']['sdd']):.2%} "
            f"CAGR>={0.70*bars['full']['scagr']:.2%}")

    # ---------------------------------------------------------------- the 352 books
    say("\n" + "=" * 205)
    say("RUNNING THE CORPUS")
    say("=" * 205)
    RET, TO, V1 = {}, {}, {}
    rows = []
    for pk in PANELS:
        R = ref[pk]
        px, start = R["px"], R["start"]
        for cost in COSTS:
            V1[(pk, cost)] = backtest(px, rules_v1_weights(px), cost_bps=cost,
                                      freq=FREQ)["returns"].loc[start:]
            for k in KS:
                for m in SHARES:
                    n = R["nmap"][m]
                    res = backtest(px, weights_k(px, k, n, pk), cost_bps=cost, freq=FREQ)
                    r = res["returns"].loc[start:]
                    RET[(pk, cost, k, m)] = r
                    TO[(pk, cost, k, m)] = float(res["turnover"].loc[start:].sum()
                                                 / (len(r) / 252.0))
                    mm, mo = metrics(r), metrics(r.loc[OOS_START:])
                    h1, h2 = H.halves(r)
                    mgf = H.margins(r, R["bars"]["full"])
                    fb = [b for b in ("H1", "H2", "OOS", "DD", "CAGR") if mgf[b] <= 0]
                    rows.append(dict(
                        panel=pk, cost=cost, k=k, share=m, n=n,
                        CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        IS_CAGR=metrics(H.window(r, "IS"))["CAGR"],
                        IS_Sharpe=metrics(H.window(r, "IS"))["Sharpe"],
                        turnover=TO[(pk, cost, k, m)],
                        pass4a=H.pass4a(r, V1[(pk, cost)]), pass4b=(len(fb) == 0),
                        failing="|".join(fb)))
        say(f"  {pk}: {len(KS)*len(SHARES)*len(COSTS)} books done  ({time.time()-t0:.0f}s)")
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    # ---------------------------------------------------------------- reproduction
    say("\n" + "=" * 205)
    say("REPRODUCTION GATE (asserted before any new number is read)")
    say("=" * 205)
    rep = []
    p159 = OUT / "2026-09-05_the-share-at-which-ranking-stops-paying_cloud.grid.csv"
    if p159.exists():
        A = pd.read_csv(p159).rename(columns={"m": "share"})   # idea 159 names its share `m`
        kmap = {"INV": -0.50, "NONE": 0.00, "POS": 0.50}
        if {"panel", "key", "share"} <= set(A.columns):
            A = A[A.key.isin(kmap)].copy()
            A["k"] = A.key.map(kmap)
            mine = G[G.cost == 10.0]
            mg = mine.merge(A, on=["panel", "k", "share"], suffixes=("", "_159"))
            for c in ("CAGR", "Sharpe", "MaxDD", "H1", "H2"):
                if f"{c}_159" in mg.columns:
                    d = float((mg[c] - mg[f"{c}_159"]).abs().max())
                    rep.append(dict(check="[a] idea159 INV/NONE/POS @10bps", field=c, n=len(mg),
                                    maxabsdiff=d, verdict="MATCH" if d < 1e-9 else "MISMATCH"))
                    say(f"  [a] {c:>7s}  n={len(mg):3d}  max|diff| {d:.3e}  "
                        f"{'MATCH' if d < 1e-9 else 'MISMATCH'}")
        else:
            say(f"  [a] SKIPPED — idea 159's grid.csv columns are {list(A.columns)[:12]}")
            rep.append(dict(check="[a]", field="-", n=0, maxabsdiff=np.nan, verdict="SKIPPED"))
    else:
        say("  [a] SKIPPED — idea 159's grid.csv absent")
        rep.append(dict(check="[a]", field="-", n=0, maxabsdiff=np.nan, verdict="SKIPPED"))

    # [b] idea 168's premise: sign of dCAGR at k=-0.5 and k=+0.5, 10 bps
    say("\n  [b] idea 168's premise — sign of signed dCAGR vs the k=0 control, 10 bps:")
    base = G.set_index(["panel", "cost", "k", "share"]).CAGR
    for kk, lab in ((K_LIVE, "INV (live)"), (0.50, "POS")):
        neg = pos = 0
        for pk in PANELS:
            for m in SHARES:
                d = base[(pk, 10.0, kk, m)] - base[(pk, 10.0, 0.0, m)]
                neg += d < 0
                pos += d > 0
        say(f"      k={kk:+.2f} {lab:<11s}: negative at {neg}/{len(PANELS)*len(SHARES)}, "
            f"positive at {pos}/{len(PANELS)*len(SHARES)}")
        rep.append(dict(check="[b] premise sign", field=f"k={kk:+.2f}",
                        n=len(PANELS) * len(SHARES), maxabsdiff=np.nan,
                        verdict=f"neg {neg} / pos {pos}"))
    pd.DataFrame(rep).to_csv(OUT / f"{STEM}.repro.csv", index=False)

    # ---------------------------------------------------------------- the k-curve
    say("\n" + "=" * 205)
    say("SIGNED dCAGR(k) IN pp/yr vs the k = 0 control — ALL grid points (.curve.csv)")
    say("=" * 205)
    crows = []
    for pk in PANELS:
        for cost in COSTS:
            for m in SHARES:
                c0 = base[(pk, cost, 0.0, m)]
                t0_ = TO[(pk, cost, 0.0, m)]
                s0 = G.set_index(["panel", "cost", "k", "share"]).Sharpe[(pk, cost, 0.0, m)]
                d0 = G.set_index(["panel", "cost", "k", "share"]).MaxDD[(pk, cost, 0.0, m)]
                for k in KS:
                    r = G[(G.panel == pk) & (G.cost == cost) & (G.k == k)
                          & (G.share == m)].iloc[0]
                    crows.append(dict(panel=pk, cost=cost, share=m, n=int(r.n), k=k,
                                      dCAGR_pp=(r.CAGR - c0) * 100.0,
                                      dSharpe=r.Sharpe - s0,
                                      dMaxDD_pp=(abs(r.MaxDD) - abs(d0)) * 100.0,
                                      cost_k_pp=(TO[(pk, cost, k, m)] - t0_) * cost / 10000.0
                                      * 100.0,
                                      CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD,
                                      pass4a=r.pass4a, pass4b=r.pass4b, failing=r.failing))
    CU = pd.DataFrame(crows)
    CU["dCAGR_net_of_extra_cost_pp"] = CU.dCAGR_pp          # dCAGR is already net of costs
    CU.to_csv(OUT / f"{STEM}.curve.csv", index=False)

    for pk in PANELS:
        for cost in COSTS:
            say(f"\n  [{pk} @ {cost:.0f}bps]  signed dCAGR (pp/yr) vs k=0, rows = share:")
            piv = CU[(CU.panel == pk) & (CU.cost == cost)].pivot(index="share", columns="k",
                                                                 values="dCAGR_pp")
            say(piv.to_string(float_format=lambda x: f"{x:+7.3f}"))
            pv = CU[(CU.panel == pk) & (CU.cost == cost)].pivot(index="share", columns="k",
                                                               values="Sharpe")
            say(f"  [{pk} @ {cost:.0f}bps]  Sharpe:")
            say(pv.to_string(float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- argmax and crossings
    say("\n" + "=" * 205)
    say("ARGMAX AND ZERO-CROSSINGS (.crossing.csv).  k0+ = first k>0 where signed dCAGR falls "
        "back below zero; k0- the same walking left.  NaN = no crossing inside |k| <= 1.")
    say("=" * 205)
    xrows = []
    for pk in PANELS:
        for cost in COSTS:
            for m in SHARES:
                sub = CU[(CU.panel == pk) & (CU.cost == cost) & (CU.share == m)]
                ks, ys = sub.k.to_numpy(), sub.dCAGR_pp.to_numpy()
                ss = sub.Sharpe.to_numpy()
                i = int(np.argmax(ys))
                xrows.append(dict(panel=pk, cost=cost, share=m, n=int(sub.n.iloc[0]),
                                  k_argmax_dCAGR=float(ks[i]), dCAGR_at_argmax=float(ys[i]),
                                  k_argmax_parab=parab(ks, ys),
                                  k_argmax_Sharpe=float(ks[int(np.argmax(ss))]),
                                  k0_plus=cross_up_to_down(ks, ys, "+"),
                                  k0_minus=cross_up_to_down(ks, ys, "-"),
                                  dCAGR_spread_pp=float(ys.max() - ys.min()),
                                  Sharpe_spread=float(ss.max() - ss.min()),
                                  Sharpe_at_k0=float(sub[sub.k == 0.0].Sharpe.iloc[0]),
                                  Sharpe_at_live=float(sub[sub.k == K_LIVE].Sharpe.iloc[0]),
                                  argmax_at_endpoint=bool(i in (0, len(ks) - 1))))
    X = pd.DataFrame(xrows)
    X.to_csv(OUT / f"{STEM}.crossing.csv", index=False)
    say(X.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say(f"\n  argmax at the +1.00 endpoint in {int((X.k_argmax_dCAGR == 1.0).sum())} of "
        f"{len(X)} cells; at the -1.00 endpoint in "
        f"{int((X.k_argmax_dCAGR == -1.0).sum())}; interior in "
        f"{int((~X.argmax_at_endpoint).sum())}.")
    say(f"  median grid argmax k* = {X.k_argmax_dCAGR.median():+.3f}   "
        f"(Sharpe argmax median {X.k_argmax_Sharpe.median():+.3f})")
    say(f"  k0+ (positive zero-crossing) exists in {int(X.k0_plus.notna().sum())} of {len(X)} "
        f"cells" + (f"; median {X.k0_plus.median():+.3f}" if X.k0_plus.notna().any() else ""))
    say(f"  k0- (negative zero-crossing) exists in {int(X.k0_minus.notna().sum())} of {len(X)} "
        f"cells" + (f"; median {X.k0_minus.median():+.3f}" if X.k0_minus.notna().any() else ""))
    say(f"  live k={K_LIVE:+.2f} beats the k=0 control on Sharpe in "
        f"{int((X.Sharpe_at_live > X.Sharpe_at_k0).sum())} of {len(X)} cells.")

    # ---------------------------------------------------------------- flatness
    say("\n" + "=" * 205)
    say("FLATNESS (idea 128's plateau instrument) — is the exponent a live dial at all?")
    say("=" * 205)
    for pk in PANELS:
        for cost in COSTS:
            sub = CU[(CU.panel == pk) & (CU.cost == cost)]
            r_k = sub.groupby("share").Sharpe.apply(lambda s: s.max() - s.min())
            r_m = sub.groupby("k").Sharpe.apply(lambda s: s.max() - s.min())
            say(f"  [{pk} @ {cost:.0f}bps]  Sharpe range across the 11 EXPONENTS at fixed share: "
                f"mean {r_k.mean():.4f} (max {r_k.max():.4f})   |   across the 8 SHARES at fixed "
                f"k: mean {r_m.mean():.4f} (max {r_m.max():.4f})   -> exponent is "
                f"{'SECOND-ORDER' if r_k.mean() < r_m.mean() else 'THE LARGER DIAL'}")

    # ---------------------------------------------------------------- KEEP paths
    say("\n" + "=" * 205)
    say("BOTH KEEP PATHS over all 352 books")
    say("=" * 205)
    say(f"  4a passes: {int(G.pass4a.sum())} / {len(G)}    4b passes: {int(G.pass4b.sum())} / "
        f"{len(G)}")
    say("\n  4b passes by k and cost:")
    say(G.groupby(["cost", "k"]).pass4b.sum().unstack(0).to_string())
    if G.pass4b.any():
        say("\n  the 4b-passing books:")
        say(G[G.pass4b][["panel", "cost", "k", "share", "n", "CAGR", "Sharpe", "MaxDD",
                         "H1", "H2", "OOS_Sharpe"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  failing-bar frequency among the 4b failures:")
    ff = G[~G.pass4b]
    for b in ("CAGR", "DD", "H1", "H2", "OOS"):
        kk = int(ff.failing.str.contains(b).sum())
        say(f"      {b:>4s}  {kk:4d} / {len(ff)}  ({kk/max(len(ff),1):.1%})")

    # ---------------------------------------------------------------- walk-forward
    say("\n" + "=" * 205)
    say("WALK-FORWARD (PROTOCOL rule 8) — everything chosen on 2009-2016 only, read ONCE on "
        "2017-2026.")
    say("=" * 205)
    wrows = []
    for pk in PANELS:
        R = ref[pk]
        so = metrics(R["spy"].loc[OOS_START:])
        for cost in COSTS:
            v1o = metrics(V1[(pk, cost)].loc[OOS_START:])
            IS = G[(G.panel == pk) & (G.cost == cost)]
            # share chosen by IS Sharpe at the no-scaler control (k is NOT chosen here)
            m_star = float(IS[IS.k == 0.0].sort_values("IS_Sharpe").iloc[-1].share)
            # k chosen by IS-window dCAGR argmax at that share
            isc = IS[IS.share == m_star].set_index("k").IS_CAGR
            k_star = float((isc - isc.loc[0.0]).idxmax())
            # (k, share) chosen jointly by IS Sharpe
            best = IS.sort_values("IS_Sharpe").iloc[-1]
            arms = {"A_LIVE": (K_LIVE, m_star), "A_ZERO": (0.0, m_star),
                    "A_ISK": (k_star, m_star),
                    "A_ISKS": (float(best.k), float(best.share))}
            say(f"\n  [{pk} @ {cost:.0f}bps]  IS-chosen share m* = {m_star:.2f} "
                f"(n={R['nmap'][m_star]}), IS-chosen exponent k* = {k_star:+.2f}, "
                f"joint IS argmax = (k {best.k:+.2f}, m {best.share:.2f})")
            for aname, (k, m) in arms.items():
                r = RET[(pk, cost, k, m)]
                mo = metrics(r.loc[OOS_START:])
                mgo = C.margins_at(r, R["bars"]["OOS"], 0.60, 0.70, which="OOS")
                fbo = [b for b in ("H1", "H2", "DD", "CAGR") if mgo[b] <= 0]
                wrows.append(dict(panel=pk, cost=cost, arm=aname, k=k, share=m,
                                  n=R["nmap"][m], OOS_CAGR=mo["CAGR"],
                                  OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                  OOS_4b_fail="|".join(fbo) if fbo else "(none)",
                                  v1_OOS_CAGR=v1o["CAGR"], v1_OOS_Sharpe=v1o["Sharpe"],
                                  v1_OOS_MaxDD=v1o["MaxDD"], spy_OOS_CAGR=so["CAGR"],
                                  spy_OOS_Sharpe=so["Sharpe"], spy_OOS_MaxDD=so["MaxDD"]))
                say(f"      {aname:<8s} k={k:+.2f} m={m:.2f}(n={R['nmap'][m]:3d})   OOS "
                    f"{mo['CAGR']:7.2%}/{mo['Sharpe']:.4f}/{mo['MaxDD']:7.2%}   "
                    f"4b-OOS fails: {'|'.join(fbo) if fbo else '(none)'}")
            say(f"      {'RULES v1':<8s} {'':22s}   OOS {v1o['CAGR']:7.2%}/"
                f"{v1o['Sharpe']:.4f}/{v1o['MaxDD']:7.2%}")
            say(f"      {'SPY':<8s} {'':22s}   OOS {so['CAGR']:7.2%}/{so['Sharpe']:.4f}/"
                f"{so['MaxDD']:7.2%}")
    WF = pd.DataFrame(wrows)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say("\n  Mean OOS by arm over the 4 (panel x cost) cells:")
    say(WF.groupby("arm")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].mean()
        .to_string(float_format=lambda x: f"{x:.4f}"))
    z = WF[WF.arm == "A_ZERO"].set_index(["panel", "cost"]).OOS_Sharpe
    for a in ("A_LIVE", "A_ISK", "A_ISKS"):
        d = WF[WF.arm == a].set_index(["panel", "cost"]).OOS_Sharpe - z
        say(f"      {a} - A_ZERO on OOS Sharpe: mean {d.mean():+.4f}, wins "
            f"{int((d > 0).sum())}/{len(d)}")

    say("\n" + "=" * 205)
    say(f"done in {time.time()-t0:.0f}s")
    say("=" * 205)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
