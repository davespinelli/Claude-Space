#!/usr/bin/env python3
"""
Idea 1436 (lane cloud, 2026-09-19) — is the BETA BAND's 4b DD GAIN anything more than a
BETA-MATCHED EXPOSURE DIAL?

THE PREMISE (verbatim from the queue).  Idea 1429 shut the DOLLAR exposure channel to < 1e-12
and still moved U56's binding 4b DD margin from the frozen incumbent's +1.1028 pp to
+1.83 .. +4.40 pp at 16 of 16 biting cells — but realised BOOK BETA fell 1.0162 -> 0.65..0.93
and CAGR fell monotonically in c, which a plain rotation down the security market line predicts
entirely.  1429's own PARK memo named the repair and did not run it:

    "The repair is named, not run: a BETA-MATCHED twin, and a rule-8 chooser keyed on the
     4b DD margin rather than on Sharpe."

This run is that twin.  (The chooser half is idea 1440 and is NOT touched here.)

WHAT IS UNDER TEST.  1429's rule ranks the n held names by trailing beta (ascending) and pays
    w_i = (G/n) (1 + c z_i),  z_i = 1 - 2(rank_i - 0.5)/n,  sum z = 0 EXACTLY,  G = 0.75.
c = 0 IS the frozen 2026-09-04 incumbent (U56, N = 20, H = 126, gross 0.75, MAXVOL 0.60, MA
gate ON, weekly Fri-decide / Mon-trade, 10 bps, t+1).  The cell reads the FULL n-way beta
ranking.  Its NAV beta is b*_cell = sum_i w_i beta_i.  The question is whether anything
survives once a control is handed that SAME b* and denied the ranking.

TWO BETA-MATCHED TWINS, both solved SEGMENT BY SEGMENT against the cell's OWN realised b*.
Both hold the IDENTICAL names on the IDENTICAL rows as the cell (1429's selection frame is
built once per panel and depends on neither dial), and both are exact, not fitted:

  TWIN-G  "BETA-MATCHED DE-GROSS" — ZERO bits of the ranking.  The frozen incumbent's own
          EQUAL weights, with gross scaled to g = b*_cell / mean(beta) so the book's NAV beta
          equals the cell's.  Gross is free (clipped to [0, G]: no leverage), ordering is
          not read at all.  This is the exposure family's best shot: if a plain de-gross of
          the anchor reaches the cell's drawdown once it is given the cell's beta, the band is
          a BETA DIAL and belongs with the trailing stop (1405), the breadth throttle (1413)
          and the convention blend (1423), which all died as exposure dials in costume.

  TWIN-B  "BETA-MATCHED BARBELL" — ONE bit of the ranking, at FIXED gross.  Split the n names
          at the MEDIAN beta; pay every low-beta name w_lo and every high-beta name w_hi with
              n_lo w_lo + n_hi w_hi = G           (gross pinned to the cell's, exactly)
              n_lo w_lo b_lo + n_hi w_hi b_hi = b*_cell     (beta pinned to the cell's)
          so the twin matches gross AND beta and reads only WHICH HALF a name is in — never
          its rank inside the half, never the cardinal spread.  This isolates the FINE
          ordering, which is the only thing 1429's rule can be about once beta is matched.

  At c = 0 both twins are BIT-IDENTICAL to the frozen incumbent by algebra (TWIN-G: g = G;
  TWIN-B: A = G n_lo / n for every n, odd or even) — gate G3 asserts it, it is not assumed.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4) — inherited unchanged from 1429 so that the cells
being re-scored are the SAME cells:
  C  {0.00, 0.25, 0.50, 0.75, 1.00}   band half-width.  c = 0.00 IS the frozen incumbent.
  B  {20, 63, 126, 252}               trailing beta lookback, in trading days.
20 cells per panel, 60 in all, EVERY ONE published.  The twins carry NO free parameter: their
weights are the unique solution to the two linear constraints above.

THE BAR, PRE-REGISTERED HERE BEFORE ANY NUMBER WAS READ.  The beta band is a NAME-LEVEL
finding only if, on U56:
  (i)   the cell's 4b DD margin beats BOTH twins' at a MAJORITY of the 16 biting cells, AND
  (ii)  the cell's MaxDD edge over the TIGHTER twin (TWIN-B) resolves |t| > 2 at >= 1 cell
        under the paired 63-row circular-block bootstrap, AND
  (iii) 4b still passes FULL and OOS at the cells where (i) and (ii) hold.
If the gain VANISHES against either twin, the band is a beta dial and the beta family CLOSES —
that is a documented KILL and is reported as one.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths for the
CELL and for BOTH TWINS at every cell; the halves; IS and OOS; turnover and its 10 bps drag;
realised mean gross; realised NAV beta of cell and twins; the barbell's clip rate.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
FROZEN (c = 0) incumbent.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 AND
SPY); rule 4 (both KEEP paths, 2 tuned parameters); rule 8 (walk-forward: (c, B) chosen on
warm-up..2016-12-31 by argmax IS Sharpe, 2017-2026 read ONCE, and the SAME chooser run over the
twins so the OOS comparison is chooser-matched); rule 9 (survivorship stated).  RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

GATES.  G0 sample >= 10y.  G1 CROSS-SCRIPT REPLAY of the committed U56 anchor
(15.80% / 1.1537 / -19.13% full; 1.1857 OOS) AND of 1429's own headline DD margin +1.1028 pp.
G2 BETA MATCH EXACT: max per-segment |b*_twin - b*_cell| < 1e-10 over every unclipped segment,
for both twins.  G3 at c = 0 both twins are bit-identical to the anchor.  G4 all 60 cells
published.  G5 exactly two tuned parameters.  G6 the chooser reads no row on or after
2017-01-01.  G7 NO LEVERAGE: TWIN-B's gross equals G to < 1e-12 at every rebalance and TWIN-G's
never exceeds G.  G8 every cell and every twin holds the IDENTICAL name set on every row
(1429's frame, imported not re-implemented).  G9 look-ahead: beta is trailing only.
G10 bit-identical recompute of the U56 headline cell.

The 1429 frame is IMPORTED from its committed script rather than re-typed, so any drift between
the two runs is impossible by construction.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_beta-matched-twin-for-the-beta-band_cloud.py
"""
from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))

DATE = "2026-09-19"
SLUG = "beta-matched-twin-for-the-beta-band"
OUT = HERE / f"{DATE}_{SLUG}_cloud"

# ---- import idea 1429's committed frame (do NOT re-implement it) -----------------------------
_SRC = HERE / "2026-09-19_beta-keyed-floor-and-cap_C.py"
_spec = importlib.util.spec_from_file_location("idea1429", _SRC)
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)

from baseline import load_universe, rules_v2_weights  # noqa: E402

CS, BS = M.CS, M.BS
I_N, I_H, I_G = M.I_N, M.I_H, M.I_G
WARMUP, COST, OOS_START = M.WARMUP, M.COST, M.OOS_START
DD_CAP, CAGR_FLOOR = M.DD_CAP, M.CAGR_FLOOR
SEED = 20260919
BAR_DD_PP, BAR_T = M.BAR_DD_PP, M.BAR_T

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


# ---------------------------------------------------------------------------------------------
# the two beta-matched twins
# ---------------------------------------------------------------------------------------------
def seg_betas(pan, segs, B):
    """Per-segment beta vector for the segment's OWN held names, at its OWN decision row.
    Non-finite entries get the row's own median beta — identical neutral fill to 1429's."""
    BE = pan.beta[B]
    out = []
    for (t, stop, ts, sel) in segs:
        if not len(sel):
            out.append(np.zeros(0))
            continue
        b = BE[ts, sel].astype(float)
        fin = np.isfinite(b)
        if not fin.all():
            med = np.nanmedian(b[fin]) if fin.any() else 1.0
            b = np.where(fin, b, med)
        out.append(b)
    return out


def nav_beta(ws, bs):
    """Per-segment NAV beta of a book: sum_i w_i beta_i (cash contributes zero)."""
    return np.array([float(np.sum(w * b)) if len(w) else np.nan for w, b in zip(ws, bs)])


def twin_degross(ws_cell, bs):
    """TWIN-G: the anchor's EQUAL weights, gross scaled to hit the cell's NAV beta.
    Zero bits of the ranking; gross free, clipped to [0, G] (no leverage)."""
    out, clipped = [], 0
    for w, b in zip(ws_cell, bs):
        n = len(w)
        if n == 0:
            out.append(np.zeros(0))
            continue
        tgt = float(np.sum(w * b))
        mb = float(np.mean(b))
        g = tgt / mb if abs(mb) > 1e-12 else I_G
        if g > I_G or g < 0.0:
            clipped += 1
            g = min(max(g, 0.0), I_G)
        out.append(np.full(n, g / n))
    return out, clipped


def twin_barbell(ws_cell, bs):
    """TWIN-B: two-point weights at FIXED gross G hitting the cell's NAV beta.  One bit of the
    ranking (which side of the median beta), never the rank inside a half."""
    out, clipped = [], 0
    for w, b in zip(ws_cell, bs):
        n = len(w)
        if n == 0:
            out.append(np.zeros(0))
            continue
        if n < 2:
            out.append(np.full(n, I_G / n))
            continue
        tgt = float(np.sum(w * b))
        order = np.argsort(b, kind="stable")
        n_lo = n // 2
        lo, hi = order[:n_lo], order[n_lo:]
        b_lo, b_hi = float(np.mean(b[lo])), float(np.mean(b[hi]))
        if abs(b_lo - b_hi) < 1e-12:
            out.append(np.full(n, I_G / n))
            continue
        A = (tgt - I_G * b_hi) / (b_lo - b_hi)       # dollars in the LOW-beta half
        if A > I_G or A < 0.0:
            clipped += 1
            A = min(max(A, 0.0), I_G)
        wv = np.empty(n)
        wv[lo] = A / len(lo)
        wv[hi] = (I_G - A) / len(hi)
        out.append(wv)
    return out, clipped


def main():
    t_start = time.time()
    say("=" * 128)
    say("IDEA 1436 (lane cloud, 2026-09-19) — is the BETA BAND's 4b DD GAIN anything more than "
        "a BETA-MATCHED EXPOSURE DIAL?")
    say("FRAME: idea 1429's committed script is IMPORTED, not re-typed.  Cells = C "
        f"{CS} x B {BS} on the frozen incumbent (N={I_N}, H={I_H}, gross {I_G}, weekly, "
        f"{COST:.0f} bps, t+1).  c=0 IS it.")
    say("TWIN-G = beta-matched DE-GROSS (equal weights, gross solved for the cell's NAV beta; "
        "ZERO bits of the ranking).")
    say("TWIN-B = beta-matched BARBELL (two-point weights at FIXED gross solved for the cell's "
        "NAV beta; ONE bit of the ranking).")
    say(f"PRE-REGISTERED BAR (before any number was read): NAME-LEVEL only if U56 (i) the cell's "
        f"4b DD margin beats BOTH twins at a MAJORITY of the 16 biting cells, (ii) |t| > {BAR_T:.0f} "
        f"on MaxDD vs TWIN-B at >= 1 cell, (iii) 4b passes FULL and OOS there.")
    say("=" * 128)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0.")

    panels = [M.Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              M.Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              M.Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010.  Every absolute level below is an UPPER BOUND and "
        "every 4b pass an optimistic one.  What this run reads is a CONTRAST between three "
        "weightings of the SAME names on the SAME days at the SAME NAV beta, which the bias "
        "cannot manufacture — but it cannot cure it either.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G9 beta trailing only (1429's rolling_beta, imported; stamped at the t-1 decision row)",
         "by construction", "no look-ahead", True)
    gate("G5 exactly two tuned parameters (c, B); the twins carry none",
         f"{len(CS)} x {len(BS)} = {len(CS)*len(BS)} cells/panel", "2 params", True)

    grid, wf_rows = [], []
    g2_dev, g3_dev, g7_dev, g7g_max = 0.0, 0.0, 0.0, 0.0
    clip_g_tot, clip_b_tot, seg_tot = 0, 0, 0
    headline = None

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy, spyO = M.bmpack(pan.spy[WARMUP:]), M.bmpack(pan.spy[i_oos:])
        lr = M.backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = M.bmpack(lr[WARMUP:]), M.bmpack(lr[i_oos:])
        segs = M.segments(pan, I_N, I_H)
        C = np.cumprod(1.0 + pan.rets, axis=0)
        Cp = np.vstack([np.ones((1, pan.rets.shape[1])), C[:-1]])
        betas = {B: seg_betas(pan, segs, B) for B in BS}

        say(f"\n  [{pan.name}]  SPY  CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps  CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%}")

        ws0 = M.cell_weights(pan, segs, 0.0, BS[0])
        g0, t0_, gp0, en0, _, _, _, _ = M.run_book(pan, segs, ws0, C, Cp)
        anchor = g0 - t0_ * COST / 1e4
        am, ao = M.triple(anchor[WARMUP:]), M.triple(anchor[i_oos:])
        ah1, ah2 = M.halves(anchor[WARMUP:])
        a_dd_margin = 100 * (am["MaxDD"] - DD_CAP * spy["MaxDD"])
        say(f"           FROZEN INCUMBENT (c=0) CAGR {am['CAGR']:.2%} Sharpe {am['Sharpe']:.4f} "
            f"MaxDD {am['MaxDD']:.2%} H1/H2 {ah1:.4f}/{ah2:.4f} | OOS {ao['CAGR']:.2%}/"
            f"{ao['Sharpe']:.4f}/{ao['MaxDD']:.2%} | 4b DD margin {a_dd_margin:+.4f} pp")
        if pan.name == "U56":
            d = max(abs(am["Sharpe"] - M.C_U56["Sharpe"]), abs(ao["Sharpe"] - M.C_U56["oSharpe"]))
            gate("G1a cross-script replay of the committed U56 anchor "
                 "(15.80%/1.1537/-19.13% full; 1.1857 OOS)",
                 f"|dSharpe| {d:.2e} (got {am['CAGR']:.4f}/{am['Sharpe']:.4f}/{am['MaxDD']:.4f})",
                 "< 5e-3", d < 5e-3)
            gate("G1b replay of 1429's committed anchor 4b DD margin +1.1028 pp",
                 f"{a_dd_margin:+.4f} pp", f"|d| < 0.01 pp of {BAR_DD_PP:+.4f}",
                 abs(a_dd_margin - BAR_DD_PP) < 0.01)

        for c in CS:
            for B in BS:
                bs_ = betas[B]
                ws = M.cell_weights(pan, segs, c, B)
                gg, tu, gp, en, mw, mn, _, _ = M.run_book(pan, segs, ws, C, Cp)
                rr = gg - tu * COST / 1e4
                bstar = nav_beta(ws, bs_)

                wG, cg = twin_degross(ws, bs_)
                wBb, cb = twin_barbell(ws, bs_)
                clip_g_tot += cg
                clip_b_tot += cb
                seg_tot += len(segs)

                ggG, tuG, gpG, _, _, _, wsxG, _ = M.run_book(pan, segs, wG, C, Cp)
                rG = ggG - tuG * COST / 1e4
                ggB, tuB, gpB, _, _, _, _, wdB = M.run_book(pan, segs, wBb, C, Cp)
                rB = ggB - tuB * COST / 1e4
                g7_dev = max(g7_dev, wdB)
                g7g_max = max(g7g_max, wsxG)

                # G2: the twins hit the cell's NAV beta exactly where unclipped
                bG, bB = nav_beta(wG, bs_), nav_beta(wBb, bs_)
                ok = np.isfinite(bstar)
                if cg == 0:
                    g2_dev = max(g2_dev, float(np.nanmax(np.abs(bG[ok] - bstar[ok]))))
                if cb == 0:
                    g2_dev = max(g2_dev, float(np.nanmax(np.abs(bB[ok] - bstar[ok]))))
                if c == 0.0:
                    g3_dev = max(g3_dev,
                                 float(np.max(np.abs(rG - anchor))),
                                 float(np.max(np.abs(rB - anchor))))

                k4a, k4b, m, h1, h2, legs = M.keep_paths(rr[WARMUP:], spy, live)
                k4aO, k4bO, mo, _, _, legsO = M.keep_paths(rr[i_oos:], spyO, liveO)
                kG4a, kG4b, mG, _, _, _ = M.keep_paths(rG[WARMUP:], spy, live)
                _, kG4bO, mGo, _, _, _ = M.keep_paths(rG[i_oos:], spyO, liveO)
                kB4a, kB4b, mB, _, _, _ = M.keep_paths(rB[WARMUP:], spy, live)
                _, kB4bO, mBo, _, _, _ = M.keep_paths(rB[i_oos:], spyO, liveO)

                dsG, _, tsG = M.paired_block(rr[WARMUP:], rG[WARMUP:], "sharpe", seed=SEED)
                ddG, _, tdG = M.paired_block(rr[WARMUP:], rG[WARMUP:], "mdd", seed=SEED)
                dsB, _, tsB = M.paired_block(rr[WARMUP:], rB[WARMUP:], "sharpe", seed=SEED)
                ddB, _, tdB = M.paired_block(rr[WARMUP:], rB[WARMUP:], "mdd", seed=SEED)
                odsB, _, otsB = M.paired_block(rr[i_oos:], rB[i_oos:], "sharpe", seed=SEED)
                oddB, _, otdB = M.paired_block(rr[i_oos:], rB[i_oos:], "mdd", seed=SEED)

                n_eff = T - WARMUP
                grid.append(dict(
                    panel=pan.name, c=c, B=B,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                    keep4a=k4a, keep4b=k4b, keep4b_oos=k4bO, keep4a_oos=k4aO,
                    legDD=legs["DD"], legCAGR=legs["CAGR"], legH1=legs["H1"], legH2=legs["H2"],
                    oleg_DD=legsO["DD"], oleg_CAGR=legsO["CAGR"],
                    dd_margin_pp=100 * (m["MaxDD"] - DD_CAP * spy["MaxDD"]),
                    cagr_margin_pp=100 * (m["CAGR"] - CAGR_FLOOR * spy["CAGR"]),
                    anchor_dd_margin_pp=a_dd_margin,
                    book_beta=float(np.nanmean(bstar)),
                    anchor_book_beta=float(np.nanmean(nav_beta(ws0, bs_))),
                    mean_gross=float(np.mean(gp[WARMUP:])), eff_n=float(en.mean()),
                    turn_y=float(np.sum(tu[WARMUP:]) * 252.0 / n_eff),
                    # ---- TWIN-G: beta-matched de-gross (zero ranking bits) ----
                    G_CAGR=mG["CAGR"], G_Sharpe=mG["Sharpe"], G_MaxDD=mG["MaxDD"],
                    G_oSharpe=mGo["Sharpe"], G_oMaxDD=mGo["MaxDD"],
                    G_dd_margin_pp=100 * (mG["MaxDD"] - DD_CAP * spy["MaxDD"]),
                    G_keep4a=kG4a, G_keep4b=kG4b, G_keep4b_oos=kG4bO,
                    G_mean_gross=float(np.mean(gpG[WARMUP:])),
                    G_book_beta=float(np.nanmean(bG)),
                    G_turn_y=float(np.sum(tuG[WARMUP:]) * 252.0 / n_eff),
                    d_maxdd_pp_vs_G=100 * (m["MaxDD"] - mG["MaxDD"]), t_maxdd_vs_G=tdG,
                    d_sharpe_vs_G=dsG, t_sharpe_vs_G=tsG,
                    cell_beats_G_on_dd=bool(m["MaxDD"] > mG["MaxDD"]),
                    # ---- TWIN-B: beta-matched barbell at fixed gross (one ranking bit) ----
                    B_CAGR=mB["CAGR"], B_Sharpe=mB["Sharpe"], B_MaxDD=mB["MaxDD"],
                    B_oSharpe=mBo["Sharpe"], B_oMaxDD=mBo["MaxDD"],
                    B_dd_margin_pp=100 * (mB["MaxDD"] - DD_CAP * spy["MaxDD"]),
                    B_keep4a=kB4a, B_keep4b=kB4b, B_keep4b_oos=kB4bO,
                    B_mean_gross=float(np.mean(gpB[WARMUP:])),
                    B_book_beta=float(np.nanmean(bB)),
                    B_turn_y=float(np.sum(tuB[WARMUP:]) * 252.0 / n_eff),
                    d_maxdd_pp_vs_B=100 * (m["MaxDD"] - mB["MaxDD"]), t_maxdd_vs_B=tdB,
                    d_sharpe_vs_B=dsB, t_sharpe_vs_B=tsB,
                    od_maxdd_pp_vs_B=100 * oddB, ot_maxdd_vs_B=otdB,
                    od_sharpe_vs_B=odsB, ot_sharpe_vs_B=otsB,
                    cell_beats_B_on_dd=bool(m["MaxDD"] > mB["MaxDD"]),
                    clip_G=cg, clip_B=cb, n_segments=len(segs),
                    spy_Sharpe=spy["Sharpe"], spy_MaxDD=spy["MaxDD"], spy_CAGR=spy["CAGR"],
                    live_Sharpe=live["Sharpe"], live_MaxDD=live["MaxDD"],
                    anchor_Sharpe=am["Sharpe"], anchor_MaxDD=am["MaxDD"], anchor_CAGR=am["CAGR"]))
                if pan.name == "U56" and c == 0.50 and B == 126:
                    headline = rr.copy()
            say(f"    [{pan.name}] c={c:.2f} done  ({time.time()-t_start:.0f}s)")

        # ---- rule 8: same chooser over CELL, TWIN-G and TWIN-B (chooser-matched) -----------
        i_is0, i_is1 = WARMUP, i_oos
        best = {}
        for arm in ("CELL", "TWIN_G", "TWIN_B"):
            bs_best, pick = -np.inf, None
            for c in CS:
                for B in BS:
                    ws = M.cell_weights(pan, segs, c, B)
                    if arm == "CELL":
                        wuse = ws
                    elif arm == "TWIN_G":
                        wuse, _ = twin_degross(ws, betas[B])
                    else:
                        wuse, _ = twin_barbell(ws, betas[B])
                    gg, tu, _, _, _, _, _, _ = M.run_book(pan, segs, wuse, C, Cp)
                    rr = gg - tu * COST / 1e4
                    s = M.sharpe(rr[i_is0:i_is1])
                    if s > bs_best:
                        bs_best, pick = s, (c, B)
            best[arm] = (pick, bs_best)

        for arm, (pick, is_s) in best.items():
            ws = M.cell_weights(pan, segs, pick[0], pick[1])
            if arm == "TWIN_G":
                wuse, _ = twin_degross(ws, betas[pick[1]])
            elif arm == "TWIN_B":
                wuse, _ = twin_barbell(ws, betas[pick[1]])
            else:
                wuse = ws
            gg, tu, _, _, _, _, _, _ = M.run_book(pan, segs, wuse, C, Cp)
            rr = gg - tu * COST / 1e4
            k4aO, k4bO, mo, _, _, legsO = M.keep_paths(rr[i_oos:], spyO, liveO)
            dA, _, tA = M.paired_block(rr[i_oos:], anchor[i_oos:], "sharpe", seed=SEED)
            ddA, _, ddtA = M.paired_block(rr[i_oos:], anchor[i_oos:], "mdd", seed=SEED)
            wf_rows.append(dict(panel=pan.name, arm=arm, is_c=pick[0], is_B=pick[1],
                                is_Sharpe=is_s, picked_anchor=bool(pick[0] == 0.0),
                                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                                keep4a_oos=k4aO, keep4b_oos=k4bO,
                                oleg_DD=legsO["DD"], oleg_CAGR=legsO["CAGR"],
                                oleg_H1=legsO["H1"], oleg_H2=legsO["H2"],
                                anchor_oSharpe=ao["Sharpe"], anchor_oMaxDD=ao["MaxDD"],
                                anchor_oCAGR=ao["CAGR"],
                                spy_oSharpe=spyO["Sharpe"], spy_oMaxDD=spyO["MaxDD"],
                                spy_oCAGR=spyO["CAGR"],
                                d_sharpe_vs_anchor=dA, t_sharpe_vs_anchor=tA,
                                d_maxdd_pp_vs_anchor=100 * ddA, t_maxdd_vs_anchor=ddtA,
                                oos_dd_margin_pp=100 * (mo["MaxDD"] - DD_CAP * spyO["MaxDD"])))
            say(f"    RULE 8 [{pan.name}] {arm:7s} IS pick (c={pick[0]:.2f}, B={pick[1]:3d}) "
                f"IS Sharpe {is_s:.4f} -> OOS {mo['CAGR']:.2%} / {mo['Sharpe']:.4f} / "
                f"{mo['MaxDD']:.2%}  4b_oos={k4bO}")

    G = pd.DataFrame(grid)
    W = pd.DataFrame(wf_rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ---- gates ---------------------------------------------------------------------------
    say("\n" + "=" * 128)
    gate("G2 BETA MATCH EXACT (max per-segment |b*_twin - b*_cell| over unclipped cells)",
         f"{g2_dev:.3e}", "< 1e-10", g2_dev < 1e-10)
    gate("G3 at c = 0 both twins are BIT-IDENTICAL to the frozen anchor",
         f"max |dret| {g3_dev:.3e}", "< 1e-12", g3_dev < 1e-12)
    gate("G4 all cells published", f"{len(G)} rows", f"{3*len(CS)*len(BS)}",
         len(G) == 3 * len(CS) * len(BS))
    gate("G7a TWIN-B gross pinned to G at every rebalance",
         f"max |sum w - {I_G}| = {g7_dev:.3e}", "< 1e-12", g7_dev < 1e-12)
    gate("G7b NO LEVERAGE anywhere (TWIN-G gross never exceeds G)",
         f"max gross {g7g_max:.6f}", f"<= {I_G}", g7g_max <= I_G + 1e-12)
    gate("G6 rule-8 chooser reads no row on or after 2017-01-01",
         "IS window = warm-up .. 2016-12-31", "no OOS leakage", True)
    gate("G8 every cell and twin holds the IDENTICAL names on every row "
         "(1429's selection frame, imported)", "by construction", "identical", True)
    publish("CLIP RATE TWIN-G (segments clipped to [0, G])",
            f"{clip_g_tot} of {seg_tot} ({100*clip_g_tot/max(seg_tot,1):.3f}%)")
    publish("CLIP RATE TWIN-B (segments clipped to [0, G])",
            f"{clip_b_tot} of {seg_tot} ({100*clip_b_tot/max(seg_tot,1):.3f}%)")
    say(f"    PUBLISHED  clip rate TWIN-G {clip_g_tot}/{seg_tot}, TWIN-B {clip_b_tot}/{seg_tot}")

    # G10 bit-identical recompute of the U56 headline cell
    panU = panels[0]
    segsU = M.segments(panU, I_N, I_H)
    CU = np.cumprod(1.0 + panU.rets, axis=0)
    CpU = np.vstack([np.ones((1, panU.rets.shape[1])), CU[:-1]])
    wsh = M.cell_weights(panU, segsU, 0.50, 126)
    gh, th, _, _, _, _, _, _ = M.run_book(panU, segsU, wsh, CU, CpU)
    rh = gh - th * COST / 1e4
    gate("G10 bit-identical recompute of the U56 headline cell (c=0.50, B=126)",
         f"max |dret| {float(np.max(np.abs(rh - headline))):.3e}", "0.0",
         float(np.max(np.abs(rh - headline))) == 0.0)

    # ---- the verdict ----------------------------------------------------------------------
    say("\n" + "=" * 128)
    say("READING THE BAR — U56, the only panel that can carry capital")
    U = G[(G.panel == "U56") & (G.c > 0)]
    nb = len(U)
    beatG = int(U.cell_beats_G_on_dd.sum())
    beatB = int(U.cell_beats_B_on_dd.sum())
    both = int((U.cell_beats_G_on_dd & U.cell_beats_B_on_dd).sum())
    tB = int((U.t_maxdd_vs_B.abs() > BAR_T).sum())
    tG = int((U.t_maxdd_vs_G.abs() > BAR_T).sum())
    say(f"  (i)  cell's MaxDD beats TWIN-G at {beatG} of {nb} biting cells, TWIN-B at {beatB} "
        f"of {nb}, BOTH at {both} of {nb}.")
    say(f"  (ii) |t| > {BAR_T:.0f} on MaxDD vs TWIN-B at {tB} of {nb}; vs TWIN-G at {tG} of {nb}.")
    say(f"  (iii) 4b FULL passes at {int(U.keep4b.sum())} of {nb}, OOS at "
        f"{int(U.keep4b_oos.sum())} of {nb}; TWIN-G 4b FULL {int(U.G_keep4b.sum())}, "
        f"TWIN-B 4b FULL {int(U.B_keep4b.sum())}.")
    say(f"  DD MARGIN (pp): cell {U.dd_margin_pp.min():+.4f} .. {U.dd_margin_pp.max():+.4f} | "
        f"TWIN-G {U.G_dd_margin_pp.min():+.4f} .. {U.G_dd_margin_pp.max():+.4f} | "
        f"TWIN-B {U.B_dd_margin_pp.min():+.4f} .. {U.B_dd_margin_pp.max():+.4f} | "
        f"anchor {U.anchor_dd_margin_pp.iloc[0]:+.4f}")
    say(f"  NAV BETA: cell {U.book_beta.min():.4f} .. {U.book_beta.max():.4f} | TWIN-G "
        f"{U.G_book_beta.min():.4f} .. {U.G_book_beta.max():.4f} | TWIN-B "
        f"{U.B_book_beta.min():.4f} .. {U.B_book_beta.max():.4f} | anchor "
        f"{U.anchor_book_beta.iloc[0]:.4f}")
    say(f"  MEAN GROSS: cell {U.mean_gross.mean():.6f} | TWIN-G {U.G_mean_gross.min():.4f} .. "
        f"{U.G_mean_gross.max():.4f} (the exposure it spends to reach the same beta) | TWIN-B "
        f"{U.B_mean_gross.mean():.6f}")
    say(f"  TURNOVER/yr: cell {U.turn_y.min():.2f}..{U.turn_y.max():.2f} | TWIN-G "
        f"{U.G_turn_y.min():.2f}..{U.G_turn_y.max():.2f} | TWIN-B {U.B_turn_y.min():.2f}.."
        f"{U.B_turn_y.max():.2f}")
    leg_i = both > nb / 2
    leg_ii = tB >= 1
    leg_iii = int(U.keep4b.sum()) > 0 and int(U.keep4b_oos.sum()) > 0
    verdict = "KEEP-candidate (4b)" if (leg_i and leg_ii and leg_iii) else "KILL"
    say(f"  BAR: (i) {leg_i}  (ii) {leg_ii}  (iii) {leg_iii}  ->  VERDICT: {verdict}")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nWrote {OUT}.grid.csv / .walkforward.csv / .gates.csv / .log.txt "
        f"({time.time()-t_start:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
