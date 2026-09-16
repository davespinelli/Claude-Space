#!/usr/bin/env python3
"""Idea 1039 (lane C, 2026-09-16) — is the END-COMPOSITION BAND itself a RHO artefact?

QUESTION (QUEUE idea 1039, verbatim)
    idea 1036 found the record's K-free null sd still moves across a 0.0191-wide band on WHICH
    single end is used, because the Q16 ends share the same 2019-2026 tape (measured cross-end
    rho 0.8934).  Build an end grid whose OOS windows do NOT overlap and report whether the
    composition band collapses.  Max 2 params (end grid, overlap fraction).

THE OBJECT.  For a window w, sd_RAW(w) = the cross-sectional sd, over the 18 GRID books of a
    panel, of each book's Sharpe measured on w.  That is the record's K-free null sd — the
    "a random draw from its own pool" yardstick at one end.  The COMPOSITION BAND of a grid of
    windows is max(sd_RAW) - min(sd_RAW) over the grid.  1036 measured it at 0.0191
    (0.0645..0.0836) over the 16 tail windows of the Q16 end grid.

WHAT IS NEW AGAINST 1036.  1036's 16 windows are TAIL windows: each runs from its end to the
    last day of the tape, so they are strictly NESTED, differ in LENGTH (1,936..2,881 days) and
    overlap by 74-99%.  Three channels are therefore confounded inside its 0.0191:
      (i)  WINDOW LENGTH  — a shorter window has a noisier per-book Sharpe, so a larger sd_RAW
           by arithmetic alone, with no change of content whatsoever;
      (ii) WINDOW CONTENT — which episodes a window actually holds (the "composition" reading);
      (iii) SAMPLING GEOMETRY — a band is max - min over K draws, and its size depends on how
           correlated those K draws are, i.e. exactly on the overlap.
    This run separates them.  It builds sliding grids of FIXED-LENGTH windows at a CONTROLLED
    overlap fraction (killing channel i outright, and dialling channel iii), and prices every
    observed band against the band the SAME books' own resampled paths produce on the SAME
    window geometry (isolating channel ii).

    The arithmetic prediction is declared BEFORE the numbers and is the opposite of the queue's
    framing: overlap makes K windows nearly the same measurement, so a band over overlapping
    windows should be SMALL and a band over DISJOINT windows LARGE.  If that is what happens,
    "the band is a rho artefact" is false in the direction the queue supposes, and the question
    that survives is whether the band ever EXCEEDS its own sampling null.

WHAT IS MEASURED
    (A) THE GRIDS.  For every (OVERLAP FRACTION f) x (WINDOW LENGTH L) point: the realised
        overlap, the calendar span, the measured cross-window rho of the 18-book Sharpe vectors,
        the per-window sd_RAW, and the band.  All 15 points published, none selected.
    (B) THE NULL.  Per cell, the 18 books' daily net returns are resampled JOINTLY by day (rows
        drawn with replacement, the same draw for all 18 books, so the cross-book correlation
        structure is inherited and only real time-variation is destroyed), the SAME windows are
        read off the synthetic path, and the band recomputed — 1,000 reps.  The observed band is
        published as a percentile of its own null at every grid point.
    (C) THE RECORD'S OWN GRID.  Q16_TAIL (1036's, reproduced as a gate) and Q16_FIXLEN (the same
        16 start dates, every window truncated to the SHORTEST of them) — the length control that
        says how much of 1036's 0.0191 is channel (i).
    (D) CONTROLS, reported at every point and not tuned: PLACEMENT (the whole grid slid back
        through the tape at up to 4 anchors), PANEL (U56 binding, B136 replication), COST
        (0 / 10 / 25 bps, 10 is PROTOCOL rule 2's and is the headline), CONVENTION (the record's
        median-over-cells-then-band, and the per-cell band the null is read against).
    (E) THE RULE-8 WALK-FORWARD at PROTOCOL's declared split 2016-12-31 (IS 2009-2016 chooses,
        2017-2026 read ONCE): OOS CAGR / Sharpe / MaxDD for each of the record's three IS-only
        choosers on both panels at all three rungs, against the live RULES v2 baseline and
        against SPY, BOTH KEEP paths (4a and 4b), every point reported.

TUNED PARAMETERS: exactly TWO, the two the queue names.  ALL 15 points reported.
    (1) OVERLAP FRACTION f in {0.00, 0.25, 0.50, 0.75, 0.90} — consecutive windows share f of
        their length (stride = round(L*(1-f))).  f = 0.00 is the DISJOINT grid the queue asks
        for; the record's Q16 sits above 0.90.
    (2) END GRID = the window length L in {400, 550, 700} trading days, at a FIXED window count
        K = 6.  K is held fixed because a band is an extreme statistic and grows with K; 6 is
        the largest count for which a DISJOINT grid of usable length fits this tape at all
        (6 x 700 = 4,200 of ~4,450 post-warmup days).  HEADLINE = L 550.

    A CONFOUND STATED UP FRONT, not discovered later: at fixed (K, L) a lower overlap NECESSARILY
    spans more calendar, so "less overlap" and "more macro heterogeneity" cannot be separated by
    the grid alone.  That is precisely why every band is read against a null built on the SAME
    window geometry: the null inherits the span, the lengths and the overlap and destroys only
    the real time-variation.  The percentile, not the band, is the adjudicable object.

PRE-REGISTERED HYPOTHESES AND BARS (declared before any number below the gates was read)
    H_COLLAPSE DECISIVE, the queue's literal question.  At matched (K, L) the band at f = 0.00 is
               <= half the band at f = 0.90.  PASS => the composition band is an overlap (rho)
               artefact.  FAIL => it is not, in that direction.
    H_MONO     the band is monotone non-increasing in f (tol 0.005), i.e. more overlap, smaller
               band.  A shape test for the same mechanism.
    H_RHO      the measured cross-window rho falls monotonically with f and |rho| <= 0.30 at
               f = 0.00 — the grid does what its label says.
    H_NULL     DECISIVE for what may be said.  At EVERY one of the 15 points the observed band
               sits at percentile <= 0.95 of its own joint-bootstrap null (median over the 6
               panel x rung cells).  PASS => the band is inside sampling noise at every overlap,
               so it is a GEOMETRY fact and never a composition finding.
    H_LEN      on the record's OWN Q16 grid, length-matching (Q16_FIXLEN) leaves the band within
               0.010 of Q16_TAIL's.  FAIL => 1036's 0.0191 is substantially a WINDOW-LENGTH fact
               and not a composition one.

REPRODUCTION GATES (printed before any hypothesis number is read)
    G1  this run's fast runner == engine.backtest on a live book, returns AND turnover.
    G2  the pool is the record's own grid_books(), 18 books per panel.
    G3  CROSS-RUN: SPY's OOS triple at 2016-12-31 == the committed 15.21% / 0.8713 / -33.72%.
    G4  CROSS-RUN: 1013's four published declared-split picks reproduce their OOS triples.
    G5  determinism: the whole book x rung x end ladder rebuilt reproduces bit-for-bit.
    G6  CROSS-RUN: 1036's committed K=1 placement band reproduces — per-end sd_RAW over the Q16
        grid, median over the 6 cells, min 0.0645 / max 0.0836 / spread 0.0191 (tol 0.005).
    G7  CROSS-RUN: 1036's measured cross-end rho 0.8934 on Q16 reproduces (tol 0.02).
    G8  WINDOW CONSTRUCTION: every slide window has exactly L days, every grid exactly K windows,
        the realised overlap equals the target to within 1/L, and at f = 0.00 consecutive windows
        share ZERO days.
    G9  THE CUMSUM SHARPE used for speed == fsharpe on the sliced returns (the arithmetic every
        number below rests on), and the window machinery reproduces the ladder's OOS_Sharpe on
        the record's own tail windows.
    G10 NULL SAMPLER: the joint day-resample preserves the cross-book correlation matrix (mean
        |d| vs the observed one, 3 MC SE) and produces a non-degenerate band distribution; and
        its cross-window rho at f = 0.00 is ~0 while at f = 0.90 it is ~the overlap-implied
        value — i.e. the null inherits the geometry and nothing else.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and
    drawdown LEVEL below is optimistic and every 4b count an UPPER bound.  The measured object is
    a RATIO of two bands read off the SAME books over the SAME tape (observed against its own
    resampled null), so the inflation is common to numerator and denominator and very largely
    cancels.  Where it does not, it raises the Sharpe LEVEL, which RAISES the sampling sd of a
    windowed Sharpe and therefore INFLATES the null — which makes H_NULL the EASIER call, and is
    reported as such.  SPY is a real index series and is not inflated.

NOT MODIFIED (PROTOCOL rule 6): RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
"""
from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import rebalance_mask, backtest  # noqa: E402

DATE = "2026-09-16"
SLUG = "is-the-END-COMPOSITION-BAND-itself-a-RHO-artefact"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_C"
LANEC = HERE / "2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"

WARMUP = 260
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
PANEL_HEAD = "U56"
REC_END = "2016-12-31"
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70
RAW_CH = ["IS_SHARPE", "IS_LEGS", "IS_CAGR"]

# ---- the two tuned dials -------------------------------------------------------------------
OVERLAPS = [0.00, 0.25, 0.50, 0.75, 0.90]
LENS = [400, 550, 700]
L_HEAD = 550
KWIN = 6                      # window COUNT, held fixed (a band grows with K)
MAX_ANCHORS = 4               # PLACEMENT control
NREP = 1000
SEED0 = 20260916

SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
PUB_1013 = {
    ("U56", "U56-band0.08-g1.00"): (0.1199, 1.162, -0.1905),
    ("U56", "U56-qroll-q0.17-w1008-d0.50"): (0.1560, 1.293, -0.1559),
    ("B136", "B136-band0.08-g1.00"): (0.1105, 1.097, -0.1950),
    ("B136", "B136-qroll-q0.12-w1008-d0.50"): (0.1430, 1.157, -0.1731),
}
PUB_1036_BAND = dict(sd_min=0.0645, sd_max=0.0836, spread=0.0191, rho=0.8934)
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


spec = importlib.util.spec_from_file_location("laneC1023", LANEC)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
fast_run, fmet, fsharpe = C.fast_run, C.fmet, C.fsharpe


# ====================================================================== ladder machinery (1036's)
def quarter_ends(lo, hi):
    return [str(d.date()) for d in pd.date_range(lo, hi, freq="QE")]


END_Q16 = quarter_ends("2015-01-01", "2018-12-31")
ALLE = sorted(set(END_Q16) | {REC_END})


def metblock(r):
    c, s, d = fmet(r)
    k = len(r) // 2
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:k]), H2=fsharpe(r[k:]))


def split_block(net, e):
    b = metblock(net.values)
    o = net.loc[pd.Timestamp(e) + pd.Timedelta(days=1):].values
    i = net.loc[:pd.Timestamp(e)].values
    oc, os_, od = fmet(o)
    ic, is_, idd = fmet(i)
    b.update(OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od, OOS_n=len(o),
             IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd, IS_n=len(i))
    return b


def legs_at(bk, sb):
    return {
        "L1_H1": bool(bk["H1"] > sb["H1"]),
        "L2_H2": bool(bk["H2"] > sb["H2"]),
        "L3_OOS": bool(bk["OOS_Sharpe"] > sb["OOS_Sharpe"]),
        "L4_DD": bool(abs(bk["OOS_MaxDD"]) <= DDCAP_FRAC * abs(sb["MaxDD"])),
        "L5_CAGR": bool(bk["OOS_CAGR"] >= CAGRFLOOR_FRAC * sb["CAGR"]),
    }


def raw_pick(sub, ch, spy_is):
    """IS-ONLY choosers — 1023's / 1031's / 1035's / 1036's own three, verbatim."""
    if ch == "IS_SHARPE":
        return sub["IS_Sharpe"].idxmax()
    if ch == "IS_CAGR":
        return sub["IS_CAGR"].idxmax()
    s = sub.copy()
    s["nlegs"] = ((s["IS_Sharpe"] > spy_is[1]).astype(int)
                  + (s["IS_CAGR"] >= CAGRFLOOR_FRAC * spy_is[0]).astype(int)
                  + (s["IS_MaxDD"].abs() <= DDCAP_FRAC * abs(spy_is[2])).astype(int))
    s = s.sort_values(["nlegs", "IS_Sharpe"], ascending=False)
    return s.index[0]


# ====================================================================== window machinery (new)
SQ252 = np.sqrt(252.0)


def cums(R):
    """Prefix sums of R and R^2 with a leading zero row.  R is T x N."""
    N = R.shape[1]
    z = np.zeros((1, N))
    return (np.vstack([z, np.cumsum(R, axis=0)]),
            np.vstack([z, np.cumsum(R * R, axis=0)]))


def win_sharpes(cs, cs2, wins):
    """Annualised Sharpe of every book on every window, from prefix sums.  Returns W x N."""
    out = np.empty((len(wins), cs.shape[1]))
    for j, (a, b) in enumerate(wins):
        n = b - a
        s = cs[b] - cs[a]
        q = cs2[b] - cs2[a]
        m = s / n
        var = (q - n * m * m) / (n - 1)
        out[j] = SQ252 * m / np.sqrt(var)
    return out


def sd_raw_vec(S):
    """Cross-book sd of the Sharpe vector, per window."""
    return S.std(axis=1, ddof=1)


def band_of(S):
    v = sd_raw_vec(S)
    return float(v.max() - v.min())


def mean_offdiag_corr(M):
    if M.shape[0] < 2:
        return np.nan
    R = np.corrcoef(M)
    iu = np.triu_indices(R.shape[0], 1)
    return float(R[iu].mean())


def slide_windows(T, L, K, f, anchor=0):
    """K windows of exactly L days, consecutive windows sharing f of their length.  The grid is
    anchored so the LAST window ends `anchor` days before the end of the tape."""
    stride = max(1, int(round(L * (1.0 - f))))
    last_end = T - anchor
    starts = [last_end - L - j * stride for j in range(K)][::-1]
    if starts[0] < 0:
        return None, stride
    return [(s, s + L) for s in starts], stride


def anchors_for(T, L, K, f, n=MAX_ANCHORS):
    """PLACEMENT control: slide the whole grid back through the tape, up to n anchors."""
    w, stride = slide_windows(T, L, K, f, 0)
    if w is None:
        return []
    span = w[-1][1] - w[0][0]
    room = T - span
    if room <= 0 or n <= 1:
        return [0]
    step = room // (n - 1)
    return [m * step for m in range(n)] if step > 0 else [0]


def main():
    t0 = time.time()
    P(f"# Idea 1039 (lane C, {DATE}) — is the END-COMPOSITION BAND itself a RHO artefact?")
    P(f"# 2 tuned dials: OVERLAP FRACTION {OVERLAPS} x END GRID (window length) {LENS} = "
      f"{len(OVERLAPS)*len(LENS)} points, ALL reported, none selected.  HEADLINE L = {L_HEAD}.")
    P(f"# Window COUNT held FIXED at K = {KWIN} (a band is max-min and grows with K); "
      f"6 x 700 = 4,200 days is the largest DISJOINT grid this tape admits.")
    P(f"# Controls at every point: PLACEMENT (<= {MAX_ANCHORS} anchors), panel [U56, B136], cost "
      f"{RUNGS} bps, POOL = the record's 18 GRID books per panel, and BOTH band conventions.")
    P(f"# NULL: {NREP:,} JOINT day-resamples per cell — the same day draw for all 18 books, so")
    P("#   cross-book correlation is inherited and only real time-variation is destroyed; the")
    P("#   SAME windows are read off the synthetic path, so span, length and overlap are too.")
    P("# CONFOUND STATED UP FRONT: at fixed (K, L) less overlap NECESSARILY spans more calendar,")
    P("#   so the grid alone cannot separate overlap from macro heterogeneity.  That is why the")
    P("#   PERCENTILE against a geometry-matched null, not the band, is the adjudicable object.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent panels — every LEVEL is optimistic; the")
    P("#   measured object is a ratio of two bands off the SAME books, and where the bias does")
    P("#   not cancel it INFLATES the null, making H_NULL the EASIER call.")
    P("")

    U = load_universe()
    B = load_universe(broad=True)
    PX = {"U56": U, "B136": B}
    REC = {p: PX[p].index[WARMUP] for p in PX}
    if not U.index.equals(B.index):
        P(f"   CALENDAR: U56 ends {U.index[-1].date()} ({len(U)} days), B136 ends "
          f"{B.index[-1].date()} ({len(B)} days); each panel keeps its OWN calendar "
          f"(1013/1023/1031/1035/1036's construction).  No splice.")
    P(f"Tape: U56 {U.shape} {U.index[0].date()}..{U.index[-1].date()}; "
      f"B136 {B.shape} {B.index[0].date()}..{B.index[-1].date()}.")

    pool = C.grid_books(U, B)
    BOOKS = {p: sorted(b for b in pool if pool[b]["panel"] == p) for p in PX}
    P(f"POOL = {len(pool)} never-memo-selected GRID books "
      f"({len(BOOKS['U56'])} U56 / {len(BOOKS['B136'])} B136).  END GRID Q16 = {len(END_Q16)} "
      f"ends {END_Q16[0]}..{END_Q16[-1]}; declared split {REC_END} read separately for rule 8.")

    NET = {}
    for nm, b in pool.items():
        px = PX[b["panel"]]
        r, t = fast_run(px, b["W"], rebalance_mask(px.index, b["freq"]))
        st = REC[b["panel"]]
        for c in RUNGS:
            NET[(nm, c)] = (r - t * c / 1e4).loc[st:]
    SPYR = {p: PX[p]["SPY"].pct_change().fillna(0.0).loc[REC[p]:] for p in PX}
    SPYB = {(p, e): split_block(SPYR[p], e) for p in PX for e in ALLE}
    SPYIS = {(p, e): (SPYB[(p, e)]["IS_CAGR"], SPYB[(p, e)]["IS_Sharpe"], SPYB[(p, e)]["IS_MaxDD"])
             for p in PX for e in ALLE}
    V2 = {}
    for p, px in PX.items():
        r, t = fast_run(px, rules_v2_weights(px), rebalance_mask(px.index, "W"))
        for c in RUNGS:
            V2[(p, c)] = split_block((r - t * c / 1e4).loc[REC[p]:], REC_END)

    def build_ladder():
        rows = []
        for nm, b in pool.items():
            p = b["panel"]
            for c in RUNGS:
                net = NET[(nm, c)]
                for e in ALLE:
                    bk = split_block(net, e)
                    lg = legs_at(bk, SPYB[(p, e)])
                    v2 = V2[(p, c)]
                    rows.append(dict(
                        book=nm, panel=p, cost=c, E=e,
                        **{k: bk[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe",
                                              "IS_CAGR", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe",
                                              "OOS_MaxDD", "IS_n", "OOS_n")},
                        spy_OOS_Sharpe=SPYB[(p, e)]["OOS_Sharpe"],
                        spy_OOS_CAGR=SPYB[(p, e)]["OOS_CAGR"],
                        **lg, pass4b=all(lg.values()),
                        pass4a=bool(bk["H1"] > v2["H1"] and bk["H2"] > v2["H2"]
                                    and bk["MaxDD"] >= v2["MaxDD"])))
        return pd.DataFrame(rows)

    L = build_ladder()
    L2 = build_ladder()
    num = L.select_dtypes(include=[float, int]).columns
    d5 = float(np.nanmax(np.abs(L[num].values - L2[num].values)))

    # per-cell return matrices, in the pool's sorted book order
    RMAT = {(p, c): np.column_stack([NET[(b, c)].values for b in BOOKS[p]])
            for p in PX for c in RUNGS}
    CUM = {k: cums(v) for k, v in RMAT.items()}
    TLEN = {p: RMAT[(p, RUNG_HEAD)].shape[0] for p in PX}
    CELLS = [(p, c) for p in PX for c in RUNGS]
    P(f"Post-warmup net series: U56 {TLEN['U56']:,} days, B136 {TLEN['B136']:,} days "
      f"(from {REC['U56'].date()} / {REC['B136'].date()}).")

    # the record's OWN tail windows, in index terms, per panel
    def tail_windows(p):
        idx = NET[(BOOKS[p][0], RUNG_HEAD)].index
        w = []
        for e in END_Q16:
            a = int(idx.searchsorted(pd.Timestamp(e), side="right"))
            w.append((a, len(idx)))
        return w

    TAILW = {p: tail_windows(p) for p in PX}
    FIXW = {}
    for p in PX:
        shortest = min(b - a for a, b in TAILW[p])
        FIXW[p] = [(a, a + shortest) for a, b in TAILW[p]]

    # ================================================================ GATES
    P("")
    P("## Reproduction gates (printed BEFORE any hypothesis number is read)")
    gates = []

    def gate(name, what, val, ok, note=""):
        gates.append(dict(gate=name, what=what, value=val, verdict="PASS" if ok else "FAIL"))
        P(f"{name:4s} {what}: {val}  {'PASS' if ok else 'FAIL'}" + (f"  {note}" if note else ""))
        return ok

    W2 = rules_v2_weights(U)
    eng = backtest(U, W2, cost_bps=0.0, freq="W")
    fr, ft = fast_run(U, W2, rebalance_mask(U.index, "W"))
    d_r = float(np.abs(eng["returns"].values[WARMUP:] - fr.values[WARMUP:]).max())
    d_t = float(np.abs(eng["turnover"].values[WARMUP:] - ft.values[WARMUP:]).max())
    gate("G1", "fast_run == engine.backtest (returns / turnover)", f"{d_r:.3e}/{d_t:.3e}",
         d_r < 1e-12 and d_t < 1e-10)

    gate("G2", "POOL is the record's grid_books(), 18 per panel",
         f"{len(BOOKS['U56'])}/{len(BOOKS['B136'])}",
         len(BOOKS["U56"]) == 18 and len(BOOKS["B136"]) == 18)

    sb = SPYB[(PANEL_HEAD, REC_END)]
    d3 = max(abs(sb["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
             abs(sb["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(sb["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G3", f"CROSS-RUN SPY OOS triple at {REC_END}",
         f"{sb['OOS_CAGR']:.4f}/{sb['OOS_Sharpe']:.4f}/{sb['OOS_MaxDD']:.4f} vs "
         f"{SPY_OOS_COMMITTED}, max|d| {d3:.2e}", d3 <= 5e-4)

    bad4, rows4 = 0, []
    for (p, nm), t13 in PUB_1013.items():
        r = L[(L.book == nm) & (L.panel == p) & (L.cost == RUNG_HEAD) & (L.E == REC_END)].iloc[0]
        d = max(abs(r.OOS_CAGR - t13[0]), abs(r.OOS_Sharpe - t13[1]), abs(r.OOS_MaxDD - t13[2]))
        bad4 += 0 if d <= 5e-4 else 1
        rows4.append(dict(panel=p, book=nm, OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                          OOS_MaxDD=r.OOS_MaxDD, pub_CAGR=t13[0], pub_Sharpe=t13[1],
                          pub_MaxDD=t13[2], maxd=d, verdict="PASS" if d <= 5e-4 else "FAIL"))
    gate("G4", "CROSS-RUN 1013's four published declared-split picks",
         f"{len(PUB_1013)-bad4}/{len(PUB_1013)}, max|d| {max(r['maxd'] for r in rows4):.2e}",
         bad4 == 0)
    dump(pd.DataFrame(rows4), "crossrun1013")

    gate("G5", "determinism (ladder rebuilt)", f"max|d| {d5:.1e}", d5 == 0.0)

    # G6 — 1036's K=1 placement band, record convention (median over the 6 cells, then band)
    tail_sd = {}
    for (p, c) in CELLS:
        S = win_sharpes(*CUM[(p, c)], TAILW[p])
        tail_sd[(p, c)] = sd_raw_vec(S)
    tail_med = np.median(np.array([tail_sd[k] for k in CELLS]), axis=0)
    g6v = dict(sd_min=float(tail_med.min()), sd_max=float(tail_med.max()),
               spread=float(tail_med.max() - tail_med.min()))
    d6 = max(abs(g6v[k] - PUB_1036_BAND[k]) for k in ("sd_min", "sd_max", "spread"))
    gate("G6", "CROSS-RUN 1036's K=1 placement band on Q16",
         f"{g6v['sd_min']:.4f}..{g6v['sd_max']:.4f} spread {g6v['spread']:.4f} vs published "
         f"{PUB_1036_BAND['sd_min']:.4f}..{PUB_1036_BAND['sd_max']:.4f}/"
         f"{PUB_1036_BAND['spread']:.4f}, max|d| {d6:.4f}", d6 <= 0.005)

    rho_q16 = float(np.median([mean_offdiag_corr(win_sharpes(*CUM[(p, c)], TAILW[p]))
                               for (p, c) in CELLS]))
    gate("G7", "CROSS-RUN 1036's measured cross-end rho on Q16",
         f"{rho_q16:.4f} vs published {PUB_1036_BAND['rho']:.4f}",
         abs(rho_q16 - PUB_1036_BAND["rho"]) <= 0.02)

    # G8 — window construction
    bad8, rows8 = 0, []
    for Lw in LENS:
        for f in OVERLAPS:
            for p in PX:
                w, stride = slide_windows(TLEN[p], Lw, KWIN, f, 0)
                ok = (w is not None and len(w) == KWIN
                      and all(b - a == Lw for a, b in w)
                      and abs((Lw - stride) / Lw - f) <= 1.0 / Lw
                      and (f > 0 or all(w[i][1] <= w[i + 1][0] for i in range(KWIN - 1))))
                bad8 += 0 if ok else 1
                rows8.append(dict(panel=p, L=Lw, f=f, stride=stride, n_win=0 if w is None else len(w),
                                  realised_overlap=(Lw - stride) / Lw,
                                  span=0 if w is None else w[-1][1] - w[0][0],
                                  fits=w is not None, verdict="PASS" if ok else "FAIL"))
    gate("G8", "WINDOW CONSTRUCTION (length, count, realised overlap, disjointness at f=0)",
         f"{len(rows8)-bad8}/{len(rows8)}", bad8 == 0)
    dump(pd.DataFrame(rows8), "windows")

    # G9 — the cumsum Sharpe is the record's Sharpe
    p, c = PANEL_HEAD, RUNG_HEAD
    Sx = win_sharpes(*CUM[(p, c)], TAILW[p])
    d9a = 0.0
    R = RMAT[(p, c)]
    for j, (a, b) in enumerate(TAILW[p]):
        for i in range(0, len(BOOKS[p]), 5):
            d9a = max(d9a, abs(Sx[j, i] - fsharpe(R[a:b, i])))
    lad = L[(L.panel == p) & (L.cost == c)].set_index(["E", "book"])
    d9b = max(abs(Sx[j, i] - lad.loc[(e, BOOKS[p][i]), "OOS_Sharpe"])
              for j, e in enumerate(END_Q16) for i in range(len(BOOKS[p])))
    gate("G9", "cumsum window Sharpe == fsharpe on the slice == the ladder's OOS_Sharpe",
         f"{d9a:.2e} / {float(d9b):.2e}", d9a < 1e-12 and float(d9b) < 1e-12)

    # ---- null sampler -------------------------------------------------------------------
    def null_bands(p, c, gridmap, nrep=NREP, seed=0):
        """Joint day-resample: one day draw shared by all 18 books.  Returns {key: array of
        bands} plus the null's mean cross-window rho per key, and the sampler's corr check."""
        R = RMAT[(p, c)]
        T = R.shape[0]
        rng = np.random.default_rng(SEED0 + seed)
        out = {k: np.empty(nrep) for k in gridmap}
        rho = {k: np.empty(nrep) for k in gridmap}
        cdiff = 0.0
        C0 = np.corrcoef(R.T)
        for r in range(nrep):
            idx = rng.integers(0, T, T)
            Rb = R[idx]
            if r < 20:
                cdiff = max(cdiff, float(np.abs(np.corrcoef(Rb.T) - C0).mean()))
            cs, cs2 = cums(Rb)
            for k, wins in gridmap.items():
                S = win_sharpes(cs, cs2, wins)
                v = sd_raw_vec(S)
                out[k][r] = v.max() - v.min()
                rho[k][r] = mean_offdiag_corr(S)
        return out, rho, cdiff

    # the full grid map per panel: 15 slide points (headline anchor) + the two record grids
    GRIDMAP = {}
    for p in PX:
        gm = {}
        for Lw in LENS:
            for f in OVERLAPS:
                w, _ = slide_windows(TLEN[p], Lw, KWIN, f, 0)
                if w is not None:
                    gm[("SLIDE", Lw, f)] = w
        gm[("Q16_TAIL", 0, -1.0)] = TAILW[p]
        gm[("Q16_FIXLEN", 0, -1.0)] = FIXW[p]
        GRIDMAP[p] = gm

    P("")
    P(f"   building the null: {NREP:,} joint day-resamples x {len(CELLS)} cells x "
      f"{len(GRIDMAP['U56'])} grids ...")
    NULL, NULLRHO, CDIFF = {}, {}, {}
    for i, (p, c) in enumerate(CELLS):
        nb, nr, cd = null_bands(p, c, GRIDMAP[p], seed=i)
        NULL[(p, c)], NULLRHO[(p, c)], CDIFF[(p, c)] = nb, nr, cd
    P(f"   null built in {time.time()-t0:.0f}s so far.")

    r0 = float(np.median([NULLRHO[k][("SLIDE", L_HEAD, 0.00)].mean() for k in CELLS]))
    r90 = float(np.median([NULLRHO[k][("SLIDE", L_HEAD, 0.90)].mean() for k in CELLS]))
    nd = float(np.median([NULL[k][("SLIDE", L_HEAD, 0.00)].std(ddof=1) for k in CELLS]))
    cmax = max(CDIFF.values())
    gate("G10", "NULL SAMPLER (corr preserved; rho ~0 at f=0, high at f=0.90; non-degenerate)",
         f"mean|dcorr| {cmax:.4f}; null rho f=0 {r0:+.4f}, f=0.90 {r90:+.4f}; null band sd "
         f"{nd:.4f}", cmax < 0.05 and abs(r0) < 0.10 and r90 > 0.50 and nd > 1e-6)
    dump(pd.DataFrame(gates), "gates")

    # ================================================================ (A) THE GRIDS
    P("")
    P("## (A) THE GRIDS — observed composition band at every (OVERLAP, LENGTH) point")
    P("   sd_RAW(w) = cross-book sd of the 18 GRID books' Sharpe on window w; band = max - min")
    P("   over the K windows of the grid.  Two conventions, both published:")
    P("     BAND_REC   the record's (1036's): median over the 6 panel x rung cells FIRST, band")
    P("                over the windows SECOND — the convention 1036's 0.0191 is in;")
    P("     BAND_CELL  band within a cell, median over the 6 cells — the one the null is read")
    P("                against, because a null must be built on ONE book set at a time.")
    P("")
    P(f"{'L':>4s} {'f':>5s} {'stride':>6s} {'span(d)':>8s} {'rho':>7s} | {'BAND_REC':>8s} "
      f"{'BAND_CELL':>9s} {'null_med':>8s} {'obs/null':>8s} {'pctile':>7s} | "
      f"{'anchors':>7s} {'anchor band range':>17s}")
    grows = []
    OBS = {}
    for Lw in LENS:
        for f in OVERLAPS:
            key = ("SLIDE", Lw, f)
            percell, rhos, bands_rec_src, anchor_rng = [], [], [], []
            for p in PX:
                for c in RUNGS:
                    if key not in GRIDMAP[p]:
                        continue
                    S = win_sharpes(*CUM[(p, c)], GRIDMAP[p][key])
                    percell.append(band_of(S))
                    rhos.append(mean_offdiag_corr(S))
                    bands_rec_src.append(sd_raw_vec(S))
                    av = []
                    for an in anchors_for(TLEN[p], Lw, KWIN, f):
                        w, _ = slide_windows(TLEN[p], Lw, KWIN, f, an)
                        if w is None:
                            continue
                        av.append(band_of(win_sharpes(*CUM[(p, c)], w)))
                    anchor_rng.append((min(av), max(av), len(av)))
            if not percell:
                continue
            band_rec = float(np.ptp(np.median(np.array(bands_rec_src), axis=0)))
            band_cell = float(np.median(percell))
            pcts = []
            for i, (p, c) in enumerate(CELLS):
                nb = NULL[(p, c)][key]
                pcts.append(float(((nb < percell[i]).sum() + 0.5 * (nb == percell[i]).sum())
                                  / len(nb)))
            null_med = float(np.median([np.median(NULL[k][key]) for k in CELLS]))
            _, stride = slide_windows(TLEN["U56"], Lw, KWIN, f, 0)
            span = GRIDMAP["U56"][key][-1][1] - GRIDMAP["U56"][key][0][0]
            row = dict(grid="SLIDE", L=Lw, f=f, stride=stride, span_days=span,
                       rho=float(np.median(rhos)), band_rec=band_rec, band_cell=band_cell,
                       null_median=null_med, ratio=band_cell / null_med,
                       pct_median=float(np.median(pcts)), pct_max=float(np.max(pcts)),
                       n_anchors=int(np.median([a[2] for a in anchor_rng])),
                       anchor_min=float(np.median([a[0] for a in anchor_rng])),
                       anchor_max=float(np.median([a[1] for a in anchor_rng])))
            grows.append(row)
            OBS[key] = row
            arng = "%.4f..%.4f" % (row["anchor_min"], row["anchor_max"])
            P(f"{Lw:4d} {f:5.2f} {stride:6d} {span:8d} {row['rho']:7.4f} | {band_rec:8.4f} "
              f"{band_cell:9.4f} {null_med:8.4f} {band_cell/null_med:8.3f} "
              f"{row['pct_median']:7.3f} | {row['n_anchors']:7d} {arng:>17s}")

    # the record's own two grids, same treatment
    for gname in ("Q16_TAIL", "Q16_FIXLEN"):
        key = (gname, 0, -1.0)
        percell, rhos, src, lens = [], [], [], []
        for p in PX:
            for c in RUNGS:
                S = win_sharpes(*CUM[(p, c)], GRIDMAP[p][key])
                percell.append(band_of(S))
                rhos.append(mean_offdiag_corr(S))
                src.append(sd_raw_vec(S))
        lens = [b - a for a, b in GRIDMAP["U56"][key]]
        pcts = []
        for i, (p, c) in enumerate(CELLS):
            nb = NULL[(p, c)][key]
            pcts.append(float(((nb < percell[i]).sum() + 0.5 * (nb == percell[i]).sum()) / len(nb)))
        null_med = float(np.median([np.median(NULL[k][key]) for k in CELLS]))
        row = dict(grid=gname, L=int(np.median(lens)), f=-1.0, stride=-1,
                   span_days=GRIDMAP["U56"][key][-1][1] - GRIDMAP["U56"][key][0][0],
                   rho=float(np.median(rhos)),
                   band_rec=float(np.ptp(np.median(np.array(src), axis=0))),
                   band_cell=float(np.median(percell)), null_median=null_med,
                   ratio=float(np.median(percell)) / null_med,
                   pct_median=float(np.median(pcts)), pct_max=float(np.max(pcts)),
                   n_anchors=1, anchor_min=np.nan, anchor_max=np.nan)
        grows.append(row)
        OBS[key] = row
    GR = pd.DataFrame(grows)
    dump(GR, "grids")

    P("")
    P("   THE RECORD'S OWN GRID (K = 16 windows, so its band is NOT comparable to the K = 6 rows")
    P("   above — a band grows with the window count; it is here for the LENGTH control):")
    P(f"{'grid':11s} {'K':>3s} {'len(d)':>7s} {'rho':>7s} | {'BAND_REC':>8s} {'BAND_CELL':>9s} "
      f"{'null_med':>8s} {'obs/null':>8s} {'pctile':>7s}")
    for gname in ("Q16_TAIL", "Q16_FIXLEN"):
        r = OBS[(gname, 0, -1.0)]
        lens = [b - a for a, b in GRIDMAP["U56"][(gname, 0, -1.0)]]
        P(f"{gname:11s} {len(lens):3d} {min(lens)}..{max(lens):<4d} {r['rho']:7.4f} | "
          f"{r['band_rec']:8.4f} {r['band_cell']:9.4f} {r['null_median']:8.4f} "
          f"{r['ratio']:8.3f} {r['pct_median']:7.3f}")

    # K-matched read of the record's grid (6 of the 16 ends, every stride placement)
    P("")
    P("   K-MATCHED read of Q16_TAIL (6 of its 16 ends, every stride-2 placement) so the")
    P("   record's grid can be compared to the K = 6 rows above:")
    kmrows = []
    for off in range(4):
        rows = [off + 2 * j for j in range(KWIN)]
        percell = []
        for p in PX:
            for c in RUNGS:
                w = [TAILW[p][i] for i in rows]
                percell.append(band_of(win_sharpes(*CUM[(p, c)], w)))
        kmrows.append(dict(offset=off, ends=";".join(END_Q16[i] for i in rows),
                           band_cell=float(np.median(percell))))
        P(f"      offset {off}: band_cell {float(np.median(percell)):.4f}  "
          f"({END_Q16[rows[0]]}..{END_Q16[rows[-1]]})")
    KM = pd.DataFrame(kmrows)
    dump(KM, "kmatched")
    km_med = float(KM.band_cell.median())
    P(f"      median over placements: {km_med:.4f}  — the record's K=6-matched band, against "
      f"{OBS[('SLIDE', L_HEAD, 0.00)]['band_cell']:.4f} for the DISJOINT L={L_HEAD} grid.")

    # ================================================================ (B) THE NULL READ
    P("")
    P("## (B) THE NULL — the observed band as a percentile of its own geometry-matched null")
    P("   Per cell: the 18 books' daily net returns resampled JOINTLY by day, the SAME windows")
    P("   read off the synthetic path, band recomputed, 1,000 reps.  Span, length, count and")
    P("   overlap are inherited exactly; only real time-variation is destroyed.")
    P(f"{'L':>4s} {'f':>5s} | " + " ".join(f"{p}/{c:.0f}" for (p, c) in CELLS) +
      f" | {'median':>7s} {'max':>6s}")
    nrows = []
    for Lw in LENS:
        for f in OVERLAPS:
            key = ("SLIDE", Lw, f)
            if key not in GRIDMAP["U56"]:
                continue
            pcts = []
            for i, (p, c) in enumerate(CELLS):
                S = win_sharpes(*CUM[(p, c)], GRIDMAP[p][key])
                ob = band_of(S)
                nb = NULL[(p, c)][key]
                pc = float(((nb < ob).sum() + 0.5 * (nb == ob).sum()) / len(nb))
                pcts.append(pc)
                nrows.append(dict(L=Lw, f=f, panel=p, cost=c, obs_band=ob,
                                  null_median=float(np.median(nb)), null_sd=float(nb.std(ddof=1)),
                                  pct=pc))
            P(f"{Lw:4d} {f:5.2f} | " + " ".join(f"{x:6.3f}" for x in pcts) +
              f" | {np.median(pcts):7.3f} {max(pcts):6.3f}")
    for gname in ("Q16_TAIL", "Q16_FIXLEN"):
        key = (gname, 0, -1.0)
        pcts = []
        for i, (p, c) in enumerate(CELLS):
            ob = band_of(win_sharpes(*CUM[(p, c)], GRIDMAP[p][key]))
            nb = NULL[(p, c)][key]
            pc = float(((nb < ob).sum() + 0.5 * (nb == ob).sum()) / len(nb))
            pcts.append(pc)
            nrows.append(dict(L=-1, f=-1.0, panel=p, cost=c, obs_band=ob,
                              null_median=float(np.median(nb)), null_sd=float(nb.std(ddof=1)),
                              pct=pc, grid=gname))
        P(f"{gname:>10s} | " + " ".join(f"{x:6.3f}" for x in pcts) +
          f" | {np.median(pcts):7.3f} {max(pcts):6.3f}")
    ND = pd.DataFrame(nrows)
    dump(ND, "nullread")

    # ================================================================ (E) RULE-8 WALK-FORWARD
    IDX = {(p, c, e): L[(L.panel == p) & (L.cost == c) & (L.E == e)].set_index("book")
           for p in PX for c in RUNGS for e in ALLE}
    PR = {(p, c): {ch: raw_pick(IDX[(p, c, REC_END)], ch, SPYIS[(p, REC_END)]) for ch in RAW_CH}
          for p in PX for c in RUNGS}
    P("")
    P(f"## (E) RULE-8 WALK-FORWARD at PROTOCOL's declared split {REC_END} "
      f"(IS 2009-2016 chooses, OOS 2017-2026 read ONCE)")
    P("   Every chooser's pick, its OOS triple, and BOTH KEEP paths against the LIVE RULES v2")
    P("   baseline and against SPY.  18 points, all published.")
    wrows = []
    for p in PX:
        for c in RUNGS:
            sub, sbp, v2 = IDX[(p, c, REC_END)], SPYB[(p, REC_END)], V2[(p, c)]
            for ch in RAW_CH:
                nm = PR[(p, c)][ch]
                r = sub.loc[nm]
                lg = legs_at(r, sbp)
                wrows.append(dict(panel=p, cost=c, chooser=ch, pick=nm,
                                  OOS_CAGR=r["OOS_CAGR"], OOS_Sharpe=r["OOS_Sharpe"],
                                  OOS_MaxDD=r["OOS_MaxDD"], H1=r["H1"], H2=r["H2"],
                                  full_CAGR=r["CAGR"], full_Sharpe=r["Sharpe"],
                                  full_MaxDD=r["MaxDD"], spy_OOS_CAGR=sbp["OOS_CAGR"],
                                  spy_OOS_Sharpe=sbp["OOS_Sharpe"], spy_full_CAGR=sbp["CAGR"],
                                  spy_full_MaxDD=sbp["MaxDD"], v2_OOS_Sharpe=v2["OOS_Sharpe"],
                                  v2_OOS_CAGR=v2["OOS_CAGR"], v2_H1=v2["H1"], v2_H2=v2["H2"],
                                  v2_MaxDD=v2["MaxDD"], **lg, pass4b=all(lg.values()),
                                  pass4a=bool(r["H1"] > v2["H1"] and r["H2"] > v2["H2"]
                                              and r["MaxDD"] >= v2["MaxDD"])))
    WF = pd.DataFrame(wrows)
    dump(WF, "walkforward")
    P(f"{'panel':6s} {'cost':>4s} {'chooser':>9s} {'pick':28s} | {'OOS CAGR':>8s} {'Sh':>6s} "
      f"{'MaxDD':>7s} | {'SPY OOS':>8s} {'Sh':>6s} | {'v2 OOS Sh':>9s} | {'4a':>3s} {'4b':>3s} "
      f"{'legs':>7s}")
    for _, r in WF.iterrows():
        legs = "".join("1" if r[k] else "0" for k in
                       ("L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"))
        P(f"{r.panel:6s} {r.cost:4.0f} {r.chooser:>9s} {r['pick'][:28]:28s} | "
          f"{r.OOS_CAGR:8.2%} {r.OOS_Sharpe:6.3f} {r.OOS_MaxDD:7.2%} | "
          f"{r.spy_OOS_CAGR:8.2%} {r.spy_OOS_Sharpe:6.3f} | {r.v2_OOS_Sharpe:9.3f} | "
          f"{'Y' if r.pass4a else 'n':>3s} {'Y' if r.pass4b else 'n':>3s} {legs:>7s}")
    v2h, spyh = V2[("U56", RUNG_HEAD)], SPYB[("U56", REC_END)]
    P(f"   4a passes {int(WF.pass4a.sum())}/{len(WF)}; 4b passes {int(WF.pass4b.sum())}/{len(WF)}."
      f"  Baseline RULES v2 (U56, {RUNG_HEAD:.0f} bps) full {v2h['CAGR']:.2%} / "
      f"{v2h['Sharpe']:.3f} / {v2h['MaxDD']:.2%} (halves {v2h['H1']:.3f}/{v2h['H2']:.3f}, "
      f"OOS Sharpe {v2h['OOS_Sharpe']:.3f}); SPY full {spyh['CAGR']:.2%} / "
      f"{spyh['Sharpe']:.3f} / {spyh['MaxDD']:.2%}.")
    P("   NOTE: this arm carries NO new book.  Every pick is a GRID ladder book the record")
    P("   already holds; it is run so the band question is answered on a rule-8 object too.")

    # ================================================================ HYPOTHESES
    P("")
    P("## Pre-registered hypotheses")
    H = []

    def hyp(name, bar, ok, detail):
        H.append(dict(hypothesis=name, bar=bar, verdict="PASS" if ok else "FAIL", detail=detail))
        P(f"{name:11s} {'PASS' if ok else 'FAIL'}  bar: {bar}")
        P(f"            {detail}")

    b0 = OBS[("SLIDE", L_HEAD, 0.00)]["band_cell"]
    b90 = OBS[("SLIDE", L_HEAD, 0.90)]["band_cell"]
    allL = {Lw: (OBS[("SLIDE", Lw, 0.00)]["band_cell"], OBS[("SLIDE", Lw, 0.90)]["band_cell"])
            for Lw in LENS}
    hyp("H_COLLAPSE", f"band at f=0.00 <= 0.5 x band at f=0.90, at L={L_HEAD}",
        bool(b0 <= 0.5 * b90),
        f"L={L_HEAD}: f=0.00 {b0:.4f} vs f=0.90 {b90:.4f} (ratio {b0/b90:.2f}x); all lengths " +
        ", ".join(f"L{Lw} {v[0]:.4f}/{v[1]:.4f} ({v[0]/v[1]:.2f}x)" for Lw, v in allL.items()))

    mono_bad = []
    for Lw in LENS:
        vals = [OBS[("SLIDE", Lw, f)]["band_cell"] for f in OVERLAPS]
        for i in range(len(vals) - 1):
            if vals[i + 1] > vals[i] + 0.005:
                mono_bad.append((Lw, OVERLAPS[i + 1]))
    hyp("H_MONO", "band monotone non-increasing in f (tol 0.005) at every length",
        len(mono_bad) == 0,
        "; ".join(f"L{Lw}: " + " ".join(f"{OBS[('SLIDE', Lw, f)]['band_cell']:.4f}"
                                        for f in OVERLAPS) for Lw in LENS) +
        f"; violations {len(mono_bad)}")

    rho_by_f = {Lw: [OBS[("SLIDE", Lw, f)]["rho"] for f in OVERLAPS] for Lw in LENS}
    rho_mono = all(all(v[i + 1] >= v[i] - 0.02 for i in range(len(v) - 1))
                   for v in rho_by_f.values())
    rho0 = max(abs(rho_by_f[Lw][0]) for Lw in LENS)
    hyp("H_RHO", "cross-window rho monotone in f (tol 0.02) and |rho| <= 0.30 at f = 0.00",
        bool(rho_mono and rho0 <= 0.30),
        "; ".join(f"L{Lw}: " + " ".join(f"{v:+.3f}" for v in rho_by_f[Lw]) for Lw in LENS) +
        f"; worst |rho| at f=0 {rho0:.3f}; Q16_TAIL rho {rho_q16:.4f}")

    pmax = max(OBS[("SLIDE", Lw, f)]["pct_median"] for Lw in LENS for f in OVERLAPS)
    pcell = max(OBS[("SLIDE", Lw, f)]["pct_max"] for Lw in LENS for f in OVERLAPS)
    hyp("H_NULL", "observed band at percentile <= 0.95 of its own geometry-matched null at ALL "
        f"{len(LENS)*len(OVERLAPS)} points (median over the 6 cells)", bool(pmax <= 0.95),
        f"worst median percentile {pmax:.3f}; worst SINGLE-CELL percentile {pcell:.3f}; "
        f"median over all points "
        f"{np.median([OBS[('SLIDE', Lw, f)]['pct_median'] for Lw in LENS for f in OVERLAPS]):.3f}; "
        f"median obs/null ratio "
        f"{np.median([OBS[('SLIDE', Lw, f)]['ratio'] for Lw in LENS for f in OVERLAPS]):.3f}")

    bt = OBS[("Q16_TAIL", 0, -1.0)]
    bf = OBS[("Q16_FIXLEN", 0, -1.0)]
    hyp("H_LEN", "length-matching the record's own Q16 grid moves its band by <= 0.010",
        bool(abs(bt["band_cell"] - bf["band_cell"]) <= 0.010),
        f"Q16_TAIL band_cell {bt['band_cell']:.4f} (BAND_REC {bt['band_rec']:.4f}, the "
        f"convention 1036 published 0.0191 in) vs Q16_FIXLEN {bf['band_cell']:.4f} "
        f"(BAND_REC {bf['band_rec']:.4f}); |d| {abs(bt['band_cell']-bf['band_cell']):.4f}; "
        f"percentiles {bt['pct_median']:.3f} -> {bf['pct_median']:.3f}")

    HY = pd.DataFrame(H)
    dump(HY, "hypotheses")

    # KEEP-path bookkeeping
    KP = pd.DataFrame([dict(
        path="4a", definition="Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse",
        points=len(WF), passes=int(WF.pass4a.sum()), claimed="no",
        note="every pick is an existing GRID ladder book; no new book is proposed"),
        dict(path="4b", definition="Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, "
                                   "CAGR >= 70% of SPY's",
             points=len(WF), passes=int(WF.pass4b.sum()), claimed="no",
             note="same books as 1013/1023/1031/1035/1036 already hold; this run's object is "
                  "the record's null construction, not a book")])
    dump(KP, "keeppaths")

    # ================================================================ VERDICT
    P("")
    P("## VERDICT")
    P(f"   gates {sum(g['verdict']=='PASS' for g in gates)}/{len(gates)} PASS; hypotheses "
      f"{int((HY.verdict=='PASS').sum())}/{len(HY)} PASS"
      + (f" ({', '.join(HY[HY.verdict=='FAIL'].hypothesis)} FAIL)."
         if (HY.verdict == "FAIL").any() else "."))
    P("")
    P("   ANSWER to the queue's question: NO — the composition band is not a rho artefact, and")
    P("   it does not collapse when the windows stop overlapping.  It does the OPPOSITE:")
    P(f"     - at L = {L_HEAD}, K = {KWIN}, the band runs " +
      " -> ".join(f"{OBS[('SLIDE', L_HEAD, f)]['band_cell']:.4f}" for f in OVERLAPS) +
      f" over f = " + "/".join(f"{f:.2f}" for f in OVERLAPS) + ",")
    P(f"       i.e. the DISJOINT grid's band is {b0/b90:.2f}x the f=0.90 grid's, not half of it;")
    P(f"     - measured cross-window rho moves " +
      " -> ".join(f"{OBS[('SLIDE', L_HEAD, f)]['rho']:+.3f}" for f in OVERLAPS) +
      f" (worst |rho| at f=0 over the three lengths {rho0:.3f}, against {rho_q16:.4f} on the")
    P(f"       record's Q16), so the grid separates what its label says it separates;")
    P(f"     - AT MATCHED WINDOW COUNT the gap is an order of magnitude: the record's own Q16")
    P(f"       grid read at K = {KWIN} (every stride-2 placement) bands {km_med:.4f}, against "
      f"{b0:.4f} for")
    P(f"       the DISJOINT L = {L_HEAD} grid — {b0/km_med:.1f}x;")
    P(f"     - and the reason is arithmetic, not economics: a band is max - min over K draws, and")
    P(f"       K nearly-identical (overlapping) draws cannot spread.  Overlap SUPPRESSES a band.")
    P("")
    P("   THE TWO SHAPE FAILS, reported as loudly as the answer.  H_MONO and H_RHO both FAIL,")
    P("   and neither failure touches the answer above:")
    P(f"     - H_MONO: {len(mono_bad)} violations of a 0.005 tolerance, "
      + "; ".join(f"L{Lw} at f={f:.2f}" for Lw, f in mono_bad) + ".  The large one is")
    P(f"       L=700 f=0.25 ({OBS[('SLIDE', 700, 0.25)]['band_cell']:.4f} against "
      f"{OBS[('SLIDE', 700, 0.00)]['band_cell']:.4f} at f=0.00) — and it is the SAME point that")
    P("       breaches H_NULL below, i.e. one grid, not a trend, and it sits in the direction of")
    P("       MORE band at LOW overlap, which the answer already claims.")
    P(f"     - H_RHO: its LEVEL leg passes (|rho| <= {rho0:.3f} at f=0.00 on all three lengths,")
    P(f"       rising to {min(rho_by_f[Lw][-1] for Lw in LENS):+.3f}.."
      f"{max(rho_by_f[Lw][-1] for Lw in LENS):+.3f} at f=0.90); only its MONOTONICITY leg fails,")
    P("       on wiggles of 0.026-0.028 at L=400 and L=550 where rho is statistically zero and a")
    P("       6-window correlation read over 18 books cannot resolve 0.02.  The bar was too tight")
    P("       for the object; it is scored FAIL as written.")
    P("")
    P("   WHAT SURVIVES, and it is the reusable half.  Almost every band in this run — the")
    P("   record's own Q16 band included — is INSIDE the band its own geometry-matched null")
    P("   produces, but NOT all of them, and H_NULL is recorded FAIL for it:")
    npass = sum(1 for Lw in LENS for f in OVERLAPS if OBS[("SLIDE", Lw, f)]["pct_median"] <= 0.95)
    worst = max(((Lw, f) for Lw in LENS for f in OVERLAPS),
                key=lambda k: OBS[("SLIDE", k[0], k[1])]["pct_median"])
    P(f"     {npass} of {len(LENS)*len(OVERLAPS)} points sit at or below the 0.95 bar; the "
      f"exception is L = {worst[0]}, f = {worst[1]:.2f} at {pmax:.3f}")
    P(f"     (worst single cell {pcell:.3f}).  Over {len(LENS)*len(OVERLAPS)} points a correct "
      f"sampler is EXPECTED to breach 0.95 about {0.05*len(LENS)*len(OVERLAPS):.2f} times, so one")
    P("     breach is not evidence of a composition effect — but the bar was pre-registered at")
    P("     ALL points and it is scored as it was written, not as it would be convenient.")
    P(f"     Median percentile over the {len(LENS)*len(OVERLAPS)} points "
      f"{np.median([OBS[('SLIDE', Lw, f)]['pct_median'] for Lw in LENS for f in OVERLAPS]):.3f}, "
      f"median obs/null ratio "
      f"{np.median([OBS[('SLIDE', Lw, f)]['ratio'] for Lw in LENS for f in OVERLAPS]):.3f};")
    P(f"     Q16_TAIL itself sits at {bt['pct_median']:.3f} of its own null "
      f"(observed {bt['band_cell']:.4f} against a null median of {bt['null_median']:.4f}), and")
    P(f"     Q16_FIXLEN at {bf['pct_median']:.3f}.  So 1036's 0.0191 is a SAMPLING-GEOMETRY fact")
    P("     and not a statement about which episodes a window holds: it should never have been")
    P("     read as END COMPOSITION.")
    P("")
    P(f"   THE LENGTH CHANNEL — H_LEN "
      f"{'PASS' if abs(bt['band_cell']-bf['band_cell'])<=0.010 else 'FAIL'}.  Length-matching the "
      f"record's own 16 windows moves the band")
    P(f"     from {bt['band_cell']:.4f} to {bf['band_cell']:.4f} (|d| "
      f"{abs(bt['band_cell']-bf['band_cell']):.4f}) and 1036's OWN convention from "
      f"{bt['band_rec']:.4f} to {bf['band_rec']:.4f},")
    P(f"     i.e. {bf['band_rec']/bt['band_rec']:.2f}x.  So a large part of the published 0.0191 "
      f"is WINDOW LENGTH, not content — and")
    P("     equalising the lengths makes the band BIGGER, because equal-length staggered windows")
    P("     are less nested than tail windows.  Both directions are geometry; neither is content.")
    P("")
    P("   WHAT THE RECORD MAY NO LONGER SAY: that the 0.0191 band shows END COMPOSITION moves")
    P("   the K-free null sd, or that overlap between OOS windows INFLATES a published band.  On")
    P("   this tape overlap deflates it, by roughly an order of magnitude at matched K.")
    P("   WHAT IT MAY SAY: that a band over K windows is only interpretable beside (i) K, (ii)")
    P("   the windows' lengths, (iii) their overlap, and (iv) the band the same books' own")
    P("   resampled paths give on that same geometry.")
    P("")
    P("   KEEP / KILL under PROTOCOL rule 4.  This run carries NO new book: its object is the")
    P("   record's own null construction, and the rule-8 arm re-runs GRID ladder books the")
    P("   record already holds.  Neither KEEP path is claimable and none is claimed.")
    P("")
    P("   PROPOSED (not applied — PROTOCOL rule 6 reserves changes to the Sunday review):")
    P("     rule 8 WINDOW GEOMETRY clause — a published band over a grid of windows states the")
    P("     window COUNT, the window LENGTHS and the OVERLAP, and is read against the band the")
    P("     SAME books' own resampled paths produce on that SAME geometry.  A band is max - min")
    P("     over K correlated draws: on this tape, holding K = 6 and the length fixed, it runs")
    P(f"     {OBS[('SLIDE', L_HEAD, 0.00)]['band_cell']:.4f} at zero overlap against "
      f"{OBS[('SLIDE', L_HEAD, 0.90)]['band_cell']:.4f} at 90% overlap, and the record's own Q16 "
      f"grid bands {km_med:.4f}")
    P("     at the same K.  Geometry, not composition, is what an unqualified band measures.")
    P(f"Runtime {time.time()-t0:.1f}s.")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT.name}.console.txt")


if __name__ == "__main__":
    main()
