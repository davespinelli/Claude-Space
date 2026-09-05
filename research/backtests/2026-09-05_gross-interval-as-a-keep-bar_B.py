#!/usr/bin/env python3
"""QUEUE idea 90 — gross-interval-as-a-pre-registered-KEEP-bar  (research sprint lane B, 2026-09-05)

QUESTION (pre-registered, from QUEUE.md idea 90)
    Idea 84 found that 4b's DD cap and CAGR floor both sit on the SAME dial (static gross g):
    Sharpe is g-invariant, CAGR rises with g, |MaxDD| rises with g.  So the CAGR floor is a
    LOWER bound on g and the DD cap an UPPER bound, and a 4b verdict is really the statement
    "the interval [g_min, g_max] is non-empty".  Idea 84 derived that interval for 4 standing
    candidates and proposed the clause; idea 90 asks whether the INTERVAL WIDTH is the
    robustness statistic PROTOCOL should quote in place of a single pass/fail.

    Pre-registered questions:

      Q1  Is the interval even an interval?  For every book x every (phi, delta) grid point,
          is the admissible m-set CONTIGUOUS?  If a material share of books admit a gapped
          set, "interval" is the wrong word and the proposed clause is mis-specified.
      Q2  Derive [g_min, g_max] and the width W = g_max - g_min for ALL 306 books (idea 84 did
          4).  Census: how many books have a non-empty interval, what is the width
          distribution, and how much of it is CENSORED by the grid rather than set by a bar
          (m = 0.10 floor, m = 1.30 no-leverage ceiling, idea 148's question).
      Q3  Which bar sets each end?  At the point just below g_min and just above g_max, which
          of 4b's five bars is the one that fails?  Idea 84's mechanism predicts CAGR below /
          DD above and NOTHING else; a Sharpe bar at either end falsifies the clause, because
          a g-invariant bar cannot bound a g-interval.
      Q4  The clause as worded: "non-empty on BOTH universes at 10 AND 25 bps".  Intersect the
          four intervals per (book, arm).  How many of the 51 (book, arm) pairs survive, what
          is the surviving JOINT width, and does the intersection ever collapse a set of
          individually-wide intervals to nothing (i.e. is the conjunction load-bearing)?
      Q5  Rule 8.  Compute the interval on 2009-2016 ONLY.  (a) Does IS width predict OOS
          outcome better than the incumbent binary IS pass/fail?  (b) As a live selector,
          does "widest IS interval" beat the incumbent IS-Sharpe screen, no screen, and SPY
          out of sample?  A width statistic that does not survive (a) is a reporting
          convention at best, and is reported as such.

    "The width predicts nothing" is a KILL of the idea's proposal and is reported as such.
    Rule 7: nothing is tuned until it works; every grid point is printed.

HARNESS  (nothing is re-implemented; the corpus the question was asked about is REBUILT)
    Idea 94's simulator (`2026-09-04_drawdown-insurance-price-list_B.py`) is imported and the
    306-book x 25-point gross family of idea 144
    (`2026-09-05_is-the-ladder-even-a-candidate_C.family.csv.gz`) is REBUILT from scratch here
    and asserted equal to the committed file, so this run owns its numbers rather than
    trusting a csv.  Checks run BEFORE any new number is read:
      (a) H.run with every instrument off vs engine.backtest, all 3 books x 3 panels — exact;
      (b) idea 94's published EWall + vol60-dg u56 @10bps row: 11.587% / 1.133 / -16.884%;
      (c) idea 144's committed family file: 7,650 rows, max|diff| over all 28 numeric columns;
      (d) idea 144/131's census off the m = 1.00 slice: 306 rows, 82 Pareto, 29 pass 4b,
          27 floor-only, 97 pass 4a.

CORPUS   3 panels (u56, broad, small) x 3 books (V1u, TOP20, EWall) x 17 arms x 2 cost rungs
    = 306 books; each book's gross family is m in {0.10, 0.15, ..., 1.30} (25 points, 75%
    target gross at m = 1.00, m = 1.30 = 97.5% = the no-leverage ceiling).  7,650 runs.
    Weekly, t+1, IS <= 2016-12-31, OOS >= 2017-01-01.  g is reported as REALISED MEAN GROSS,
    not as m, because that is the number a rule would have to quote.

TUNED PARAMETERS — exactly two, the two bar coefficients that define the interval
    phi    CAGR floor  in {0.00, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00}   (0.70 published)
    delta  MaxDD cap   in {0.40, 0.50, 0.60, 0.70, 0.80, 1.00}         (0.60 published)
    All 42 grid points reported (Q1, Q2 census).  m is the construction dial, swept
    exhaustively, and is not tuned.  The Q5 selectors take no parameter of their own
    (argmax, not threshold), by construction.

BOTH KEEP PATHS are evaluated: 4b as the interval object under study, and 4a (H.pass4a
    against live RULES v1 on the same panel and cost rung) given its own interval, which the
    mechanism predicts is one-sided.

CAVEATS carried, not buried
    - Survivorship (idea 54): all three panels are current-constituent lists.
    - Idea 128: the IS window's SPY MaxDD is shallower than the OOS window's, so every IS
      drawdown cap admits too much; this biases every Q5 selector the same way.
    - The m grid is 0.05 wide, so every width is quantised to ~0.03-0.04 of realised gross and
      an interval of one grid point is reported as width 0.000, not as "empty".
    - The two `ebud` arms scale an absolute turnover budget, so m is not a pure exposure
      rescale there (idea 144 Q1); their rows are kept and flagged, never silently dropped.
    - Idea 38 (u56/broad calendar-day index) and idea 126 (t+1 only) carry over.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_gross-interval-as-a-keep-bar_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I144_FAMILY = OUT / "2026-09-05_is-the-ladder-even-a-candidate_C.family.csv.gz"
I144_CORPUS = OUT / "2026-09-05_is-the-ladder-even-a-candidate_C.corpus.csv"
CKPT = OUT / "2026-09-05_gross-interval-as-a-keep-bar_B.family.csv.gz"
# The 7,650-run corpus is checkpointed to CKPT the moment it is built and reused on a re-run of
# this same script.  Deleting CKPT forces a full rebuild; the rebuild is deterministic and is
# asserted equal to idea 144's committed family file either way.

_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

FREQ, PCOST = H.FREQ, H.PCOST
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
BOOKS = H.BOOKS
PANELS = ["u56", "broad", "small"]
BIG = ["u56", "broad"]                       # "both universes" in idea 84's clause = the large-cap pair

MGRID = [round(x, 2) for x in np.arange(0.10, 1.3001, 0.05)]    # 25 construction points
M_FLOOR, M_CEIL = MGRID[0], MGRID[-1]
PHIS = [0.00, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
DELTAS = [0.40, 0.50, 0.60, 0.70, 0.80, 1.00]
PHI0, DELTA0 = 0.70, 0.60
BARS5 = ("H1", "H2", "OOS", "DD", "CAGR")
BARS_IS = ("H1", "H2", "DD", "CAGR")          # OOS bar is undefined inside the IS window
PURE_KINDS = ("ctl", "gate", "stop")          # scale-free arms: m is a pure exposure rescale there

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def rule(t=""):
    say("\n" + "=" * 118)
    if t:
        say(t)
        say("=" * 118)


# ------------------------------------------------------------------ panels (idea 144 verbatim)
def _panel(name):
    """(investable price frame, SPY return series, description).  SPY is a BENCHMARK on the
    small panel and is held out of the investable columns, exactly as in idea 144."""
    if name == "u56":
        px = load_universe()
        return px, px["SPY"].pct_change().fillna(0.0), "universe.json(56)"
    if name == "broad":
        px = load_universe(broad=True)
        return px, px["SPY"].pct_change().fillna(0.0), "universe_broad.json(136)"
    if name == "small":
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
        inv = [c for c in px.columns if c != "SPY" and c not in bad]
        return px[inv], px["SPY"].pct_change().fillna(0.0), f"prices_small({len(inv)}, SPY held out)"
    raise ValueError(name)


def stats_of(r, which):
    w = H.window(r, which) if which != "full" else r
    m = metrics(w)
    h1, h2 = H.halves(w)
    oos = metrics(H.window(r, "OOS"))["Sharpe"] if which == "full" else m["Sharpe"]
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2, OOS_Sharpe=oos)


def bars_win(spy, which):
    w = spy if which == "full" else H.window(spy, which)
    s1, s2 = H.halves(w)
    m = metrics(w)
    soos = metrics(H.window(spy, "OOS"))["Sharpe"] if which == "full" else m["Sharpe"]
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"], soos=soos)


# ================================================================== BUILD THE CORPUS
def build():
    frames, bars_by_panel, v1_oos = [], {}, {}
    cached = pd.read_csv(CKPT) if CKPT.exists() else None
    rule("CORPUS BUILD — 3 panels x 3 books x 17 arms x 2 costs x 25 gross points = 7,650 runs"
         + ("  [checkpoint found: arms reused, panels/bars/engine-equivalence re-derived]"
            if cached is not None else ""))
    for pname in PANELS:
        px, spy_full, desc = _panel(pname)
        start = px.index[260]
        spy = spy_full.loc[start:]
        bfull, bIS = bars_win(spy, "full"), bars_win(spy, "IS")
        bOOS = bars_win(spy, "OOS")
        bars_by_panel[pname] = (bfull, bIS, bOOS)

        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        v1_oos[pname] = {c: metrics(H.window(v1[c], "OOS")) for c in COSTS}

        worst = 0.0
        for b in BOOKS:
            W = H.targets(px, b)
            a = H.run(px, W, bps=PCOST)["r"].loc[start:]
            e = backtest(px, W, cost_bps=PCOST, freq=FREQ)["returns"].loc[start:]
            worst = max(worst, float((a - e).abs().max()))
        say(f"[{pname:5s}] {desc:32s} {px.shape[1]:4d} cols  eval {start.date()} -> {px.index[-1].date()}"
            f" | ENGINE-EQUIVALENCE max|diff| = {worst:.3e} "
            f"({'EXACT' if worst < 1e-12 else 'NOT EXACT — UNSAFE'})")
        say(f"        SPY full CAGR {bfull['scagr']:.2%} Sharpe {metrics(spy)['Sharpe']:.3f} MaxDD {bfull['sdd']:.2%}"
            f" halves {bfull['s1']:.3f}/{bfull['s2']:.3f} OOS {bfull['soos']:.3f}"
            f" | IS bars {bIS['s1']:.3f}/{bIS['s2']:.3f} DD {bIS['sdd']:.2%} CAGR {bIS['scagr']:.2%}"
            f" | OOS SPY CAGR {bOOS['scagr']:.2%} Sharpe {bOOS['soos']:.3f} MaxDD {bOOS['sdd']:.2%}")
        assert worst < 1e-12, "harness does not reproduce engine.backtest"

        if cached is not None:
            continue
        for book in BOOKS:
            for cost in COSTS:
                rows = []
                for arm, kind, kw, (gate, conv) in H.arm_specs():
                    W = H.targets(px, book, gate, conv)
                    for m_ in MGRID:
                        res = H.run(px, W, m=m_, bps=cost, **kw)
                        r = res["r"].loc[start:]
                        g = res["gross"].loc[start:]
                        sf, si = stats_of(r, "full"), stats_of(r, "IS")
                        so = metrics(H.window(r, "OOS"))
                        rows.append(dict(
                            panel=pname, book=book, cost=cost, arm=arm, kind=kind, m=m_,
                            CAGR=sf["CAGR"], Sharpe=sf["Sharpe"], MaxDD=sf["MaxDD"],
                            H1=sf["H1"], H2=sf["H2"], OOS_Sharpe_full=sf["OOS_Sharpe"],
                            IS_CAGR=si["CAGR"], IS_Sharpe=si["Sharpe"], IS_MaxDD=si["MaxDD"],
                            IS_H1=si["H1"], IS_H2=si["H2"],
                            OOS_CAGR=so["CAGR"], OOS_Sharpe=so["Sharpe"], OOS_MaxDD=so["MaxDD"],
                            gross=float(g.mean()),
                            gross_cv=float(g.std() / g.mean()) if g.mean() > 0 else np.nan,
                            pass4a=H.pass4a(r, v1[cost]),
                            TO=float(res["to"].loc[start:].sum() / (len(r) / 252)),
                        ))
                frames.append(pd.DataFrame(rows))
                say(f"        built {pname:5s} {book:5s} @{cost:4.0f}bps  {len(rows):4d} rows")
    if cached is not None:
        F = cached
        say(f"corpus reused from {CKPT.name} ({len(F)} rows)")
    else:
        F = pd.concat(frames, ignore_index=True)
        F["book_id"] = F.panel + "|" + F.book + "|" + F.cost.astype(str) + "|" + F.arm
        F.to_csv(CKPT, index=False, compression="gzip")   # checkpoint before any check reads it
        say(f"corpus checkpointed to {CKPT.name} ({len(F)} rows)")
    F["m"] = F.m.round(2)
    return F, bars_by_panel, v1_oos


def reproduce(F):
    """Every published control this run touches, checked before any new number is read."""
    rule("REPRODUCTION — published controls, checked before any new number is read")
    ok = True

    a = F[(F.panel == "u56") & (F.book == "EWall") & (F.cost == 10) & (F.arm == "vol60-dg") & (F.m == 1.0)]
    row = a.iloc[0]
    tgt = (0.11587148590018459, 1.1333131514162902, -0.16883950895070898)
    d = max(abs(row.CAGR - tgt[0]), abs(row.Sharpe - tgt[1]), abs(row.MaxDD - tgt[2]))
    say(f"(b) idea 94 EWall+vol60-dg u56@10bps  {row.CAGR:.5%} / {row.Sharpe:.4f} / {row.MaxDD:.5%}"
        f"   max|diff| vs published = {d:.3e}  {'OK' if d < 1e-9 else 'MISMATCH'}")
    ok &= d < 1e-9

    ref = pd.read_csv(I144_FAMILY)
    keys = ["panel", "book", "cost", "arm", "m"]
    # idea 144's file also carries pre-computed bar margins (m_*, IS_m_*, b_*) which this run
    # recomputes from the bars instead of storing; compare every column the two share.
    num = [c for c in ref.columns if c not in keys + ["kind", "book_id", "pass4a"]
           and c in F.columns and pd.api.types.is_numeric_dtype(ref[c])]
    L = ref.set_index(keys).sort_index()
    R = F.set_index(keys).sort_index()
    say(f"(c) idea 144 family file: committed {len(ref)} rows, rebuilt {len(F)} rows, "
        f"index identical = {L.index.equals(R.index)}")
    worst, wcol = 0.0, ""
    for c in num:
        dd = float((L[c] - R[c]).abs().max())
        if dd > worst:
            worst, wcol = dd, c
    pa = int((L["pass4a"].astype(bool) != R["pass4a"].astype(bool)).sum())
    # idea 144 wrote that file at 6 decimals, so 5e-7 is the tightest tolerance the file itself
    # can support; checks (b) and (d) below are against full-precision published values at 1e-9.
    say(f"    max|diff| over {len(num)} numeric columns = {worst:.3e} (worst column '{wcol}'); "
        f"pass4a disagreements = {pa}  "
        f"{'MATCH at the file precision (6dp)' if worst < 1e-6 and pa == 0 else 'MISMATCH'}")
    ok &= worst < 1e-6 and pa == 0

    C = pd.read_csv(I144_CORPUS)
    say(f"(d) idea 144/131 census (committed corpus.csv): rows {len(C)} (306), Pareto {int(C.pareto.sum())} (82), "
        f"pass 4b {int(C.pass4b.sum())} (29), floor-only {int(C.floor_only.sum())} (27), "
        f"pass 4a {int(C.pass4a.sum())} (97)")
    cen = (len(C), int(C.pareto.sum()), int(C.pass4b.sum()), int(C.floor_only.sum()), int(C.pass4a.sum()))
    ok &= cen == (306, 82, 29, 27, 97)
    m1 = F[F.m == 1.0].set_index(["panel", "book", "cost", "arm"]).sort_index()
    c1 = C.set_index(["panel", "book", "cost", "arm"]).sort_index()
    d2 = max(float((m1[c] - c1[c]).abs().max()) for c in ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"])
    say(f"    rebuilt m=1.00 slice vs committed corpus: max|diff| = {d2:.3e} "
        f"{'EXACT' if d2 < 1e-9 else 'MISMATCH'}")
    ok &= d2 < 1e-9
    say(f"\nALL REPRODUCTION CHECKS {'PASS' if ok else 'FAIL — every number below is unsafe'}")
    assert ok
    return ok


# ================================================================== interval machinery
def bar_frame(D, phi, delta, bars_by_panel, which):
    """Boolean frame, one column per 4b bar (idea 144's convention: strict > 0 margin)."""
    if which == "full":
        b1 = D.panel.map({p: bars_by_panel[p][0]["s1"] for p in bars_by_panel})
        b2 = D.panel.map({p: bars_by_panel[p][0]["s2"] for p in bars_by_panel})
        bo = D.panel.map({p: bars_by_panel[p][0]["soos"] for p in bars_by_panel})
        bd = D.panel.map({p: abs(bars_by_panel[p][0]["sdd"]) for p in bars_by_panel})
        bc = D.panel.map({p: bars_by_panel[p][0]["scagr"] for p in bars_by_panel})
        return pd.DataFrame(dict(H1=D.H1 - b1 > 0, H2=D.H2 - b2 > 0,
                                 OOS=D.OOS_Sharpe_full - bo > 0,
                                 DD=delta * bd - D.MaxDD.abs() > 0,
                                 CAGR=D.CAGR - phi * bc > 0), index=D.index)
    b1 = D.panel.map({p: bars_by_panel[p][1]["s1"] for p in bars_by_panel})
    b2 = D.panel.map({p: bars_by_panel[p][1]["s2"] for p in bars_by_panel})
    bd = D.panel.map({p: abs(bars_by_panel[p][1]["sdd"]) for p in bars_by_panel})
    bc = D.panel.map({p: bars_by_panel[p][1]["scagr"] for p in bars_by_panel})
    return pd.DataFrame(dict(H1=D.IS_H1 - b1 > 0, H2=D.IS_H2 - b2 > 0,
                             OOS=pd.Series(True, index=D.index),
                             DD=delta * bd - D.IS_MaxDD.abs() > 0,
                             CAGR=D.IS_CAGR - phi * bc > 0), index=D.index)


def intervals(F, phi, delta, bars_by_panel, which="full", keys=BARS5):
    """One row per book: the admissible m-set, its interval, its width in realised gross,
    contiguity, censoring, and the bar that fails at each shoulder."""
    B = bar_frame(F, phi, delta, bars_by_panel, which)
    D = F[["book_id", "panel", "book", "cost", "arm", "kind", "m", "gross"]].copy()
    D["ok"] = B[list(keys)].all(axis=1)
    for k in keys:
        D["f_" + k] = ~B[k]
    out = []
    for bid, G in D.groupby("book_id", sort=False):
        G = G.sort_values("m").reset_index(drop=True)
        okv = G.ok.values
        n_ok = int(okv.sum())
        r0 = G.iloc[0]
        rec = dict(book_id=bid, panel=r0.panel, book=r0.book, cost=r0.cost, arm=r0.arm,
                   kind=r0.kind, n_ok=n_ok, nonempty=n_ok > 0)
        if n_ok == 0:
            rec.update(m_lo=np.nan, m_hi=np.nan, g_lo=np.nan, g_hi=np.nan, width=np.nan,
                       contiguous=True, gaps=0, cens_lo=False, cens_hi=False,
                       lo_bar="", hi_bar="", g_mid=np.nan, m_mid=np.nan)
            out.append(rec)
            continue
        idx = np.flatnonzero(okv)
        lo, hi = int(idx[0]), int(idx[-1])
        gaps = int((~okv[lo:hi + 1]).sum())
        lo_bar = hi_bar = "grid"
        if lo > 0:
            fl = [k for k in keys if G.iloc[lo - 1]["f_" + k]]
            lo_bar = "+".join(fl)
        if hi < len(G) - 1:
            fh = [k for k in keys if G.iloc[hi + 1]["f_" + k]]
            hi_bar = "+".join(fh)
        mid = idx[len(idx) // 2]
        rec.update(m_lo=G.m[lo], m_hi=G.m[hi], g_lo=G.gross[lo], g_hi=G.gross[hi],
                   width=G.gross[hi] - G.gross[lo], contiguous=gaps == 0, gaps=gaps,
                   cens_lo=G.m[lo] == M_FLOOR, cens_hi=G.m[hi] == M_CEIL,
                   lo_bar=lo_bar, hi_bar=hi_bar, g_mid=G.gross[mid], m_mid=G.m[mid])
        out.append(rec)
    return pd.DataFrame(out)


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 4:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def auc(score, label):
    """Rank AUC of a continuous score against a binary label (ties handled by mid-rank)."""
    s, y = np.asarray(score, float), np.asarray(label, bool)
    ok = np.isfinite(s)
    s, y = s[ok], y[ok]
    if y.sum() == 0 or (~y).sum() == 0:
        return np.nan
    r = pd.Series(s).rank().values
    n1, n0 = int(y.sum()), int((~y).sum())
    return float((r[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def fmt(x, p=3):
    return "  n/a" if not np.isfinite(x) else f"{x:+.{p}f}"


# ================================================================== main
def main():
    F, bars_by_panel, v1_oos = build()
    reproduce(F)

    # ---------------------------------------------------------------- Q1 contiguity
    rule("Q1 — IS THE ADMISSIBLE GROSS SET AN INTERVAL?  (all 42 (phi, delta) grid points, full sample)")
    q1 = []
    IV = {}
    for phi in PHIS:
        for delta in DELTAS:
            iv = intervals(F, phi, delta, bars_by_panel, "full")
            IV[(phi, delta)] = iv
            ne = iv[iv.nonempty]
            q1.append(dict(phi=phi, delta=delta, nonempty=int(len(ne)), of=len(iv),
                           contiguous=int(ne.contiguous.sum()),
                           gapped=int((~ne.contiguous).sum()),
                           gap_pts=int(ne.gaps.sum()),
                           med_width=float(ne.width.median()) if len(ne) else np.nan,
                           cens_hi=int(ne.cens_hi.sum()), cens_lo=int(ne.cens_lo.sum())))
    Q1 = pd.DataFrame(q1)
    say(Q1.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    tot_ne, tot_gap = int(Q1.nonempty.sum()), int(Q1.gapped.sum())
    say(f"\nACROSS ALL 42 GRID POINTS: {tot_ne} non-empty book-verdicts, of which GAPPED = {tot_gap} "
        f"({tot_gap / max(tot_ne,1):.2%}).  'Interval' is {'well-defined' if tot_gap == 0 else 'NOT exact'}.")

    iv0 = IV[(PHI0, DELTA0)]
    ne0 = iv0[iv0.nonempty]

    # ---------------------------------------------------------------- Q2 census
    rule(f"Q2 — THE INTERVAL FOR ALL 306 BOOKS AT THE PUBLISHED BARS (phi={PHI0}, delta={DELTA0}), full sample")
    say(f"non-empty {len(ne0)} of {len(iv0)} books; empty {len(iv0) - len(ne0)}")
    if len(ne0):
        say("\nwidth (realised mean gross) distribution over the non-empty books:")
        q = ne0.width.quantile([0, .1, .25, .5, .75, .9, 1.0])
        say("   " + "  ".join(f"p{int(k*100):3d}={v:.4f}" for k, v in q.items()))
        say(f"   mean {ne0.width.mean():.4f}   one-grid-point (width 0.000) books = "
            f"{int((ne0.n_ok == 1).sum())}   median admissible points = {ne0.n_ok.median():.0f} of 25")
        say(f"\nCENSORING: right-censored at the no-leverage ceiling m=1.30: {int(ne0.cens_hi.sum())} "
            f"({ne0.cens_hi.mean():.1%});  left-censored at the grid floor m=0.10: {int(ne0.cens_lo.sum())} "
            f"({ne0.cens_lo.mean():.1%});  both ends censored (interval is the WHOLE grid): "
            f"{int((ne0.cens_hi & ne0.cens_lo).sum())}")
        say("\nby panel x book (non-empty count / median width / median g_lo / median g_hi):")
        agg = ne0.groupby(["panel", "book"]).agg(n=("width", "size"), med_w=("width", "median"),
                                                 med_lo=("g_lo", "median"), med_hi=("g_hi", "median"),
                                                 cens_hi=("cens_hi", "sum"))
        say(agg.to_string(float_format=lambda x: f"{x:.4f}"))
        say("\nby cost rung:")
        say(ne0.groupby("cost").agg(n=("width", "size"), med_w=("width", "median"),
                                    med_lo=("g_lo", "median"), med_hi=("g_hi", "median")
                                    ).to_string(float_format=lambda x: f"{x:.4f}"))
        say("\nwidest 15 books:")
        say(ne0.nlargest(15, "width")[["book_id", "n_ok", "m_lo", "m_hi", "g_lo", "g_hi", "width",
                                       "cens_lo", "cens_hi", "lo_bar", "hi_bar"]
                                      ].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- Q3 shoulders
    rule("Q3 — WHICH BAR SETS EACH END?  (idea 84's mechanism predicts CAGR below, DD above, nothing else)")
    if len(ne0):
        say("lower shoulder (bar that fails one grid point BELOW g_lo):")
        say(ne0.lo_bar.value_counts().to_string())
        say("\nupper shoulder (bar that fails one grid point ABOVE g_hi):")
        say(ne0.hi_bar.value_counts().to_string())
        sh_lo = ne0.lo_bar.str.contains("H1|H2|OOS", regex=True)
        sh_hi = ne0.hi_bar.str.contains("H1|H2|OOS", regex=True)
        say(f"\nA g-INVARIANT (Sharpe) bar at a shoulder falsifies the clause: lower {int(sh_lo.sum())}, "
            f"upper {int(sh_hi.sum())} of {len(ne0)}.")
        say("\nshoulders by arm kind (ctl/gate/stop rescale purely; dd and bud do NOT — idea 144 Q1):")
        say(pd.crosstab(ne0.kind, ne0.lo_bar).to_string())
        say(pd.crosstab(ne0.kind, ne0.hi_bar).to_string())
        pure = ne0[ne0.kind.isin(PURE_KINDS)]
        say(f"restricted to the {len(pure)} PURE-rescale books: Sharpe bar at a shoulder = "
            f"{int(pure.lo_bar.str.contains('H1|H2|OOS', regex=True).sum())} lower, "
            f"{int(pure.hi_bar.str.contains('H1|H2|OOS', regex=True).sum())} upper")
        say("\nSharpe spread along each book's own family (max-min over the 25 m points), by kind:")
        sp = F.groupby(["book_id", "kind"]).Sharpe.agg(lambda s: s.max() - s.min()).reset_index()
        say(sp.groupby("kind").Sharpe.describe()[["count", "mean", "50%", "max"]
                                                 ].to_string(float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- Q3b 4a's interval
    rule("Q3b — THE OTHER KEEP PATH.  4a's admissible gross set (Sharpe > live v1 in both halves, MaxDD no worse)")
    D4 = F[["book_id", "panel", "book", "cost", "arm", "m", "gross", "pass4a"]].copy()
    r4 = []
    for bid, G in D4.groupby("book_id", sort=False):
        G = G.sort_values("m").reset_index(drop=True)
        ok = G.pass4a.values.astype(bool)
        if not ok.any():
            r4.append(dict(book_id=bid, nonempty=False, n_ok=0, width=np.nan,
                           g_lo=np.nan, g_hi=np.nan, cens_lo=False, cens_hi=False, gaps=0))
            continue
        idx = np.flatnonzero(ok)
        lo, hi = int(idx[0]), int(idx[-1])
        r4.append(dict(book_id=bid, nonempty=True, n_ok=int(ok.sum()),
                       width=G.gross[hi] - G.gross[lo], g_lo=G.gross[lo], g_hi=G.gross[hi],
                       cens_lo=G.m[lo] == M_FLOOR, cens_hi=G.m[hi] == M_CEIL,
                       gaps=int((~ok[lo:hi + 1]).sum())))
    IV4 = pd.DataFrame(r4)
    n4 = IV4[IV4.nonempty]
    say(f"non-empty 4a sets: {len(n4)} of {len(IV4)} books; gapped {int((n4.gaps > 0).sum())}; "
        f"median width {n4.width.median():.4f}")
    say(f"LEFT-censored (admissible right down to the grid floor m=0.10) = {int(n4.cens_lo.sum())} "
        f"({n4.cens_lo.mean():.1%});  RIGHT-censored = {int(n4.cens_hi.sum())} ({n4.cens_hi.mean():.1%})")
    say("4a has no CAGR floor, so the mechanism predicts a ONE-SIDED set (a cap, open below): "
        f"{'CONFIRMED' if n4.cens_lo.mean() > 0.8 else 'NOT confirmed'}.")
    both = iv0.merge(IV4, on="book_id", suffixes=("_4b", "_4a"))
    say(f"books with a non-empty interval on BOTH paths: {int((both.nonempty_4b & both.nonempty_4a).sum())}; "
        f"4b only {int((both.nonempty_4b & ~both.nonempty_4a).sum())}; "
        f"4a only {int((~both.nonempty_4b & both.nonempty_4a).sum())}; "
        f"neither {int((~both.nonempty_4b & ~both.nonempty_4a).sum())}")

    # ---------------------------------------------------------------- Q4 the clause as worded
    rule("Q4 — THE CLAUSE AS WORDED: interval non-empty on BOTH large-cap universes at 10 AND 25 bps")
    piv = iv0[iv0.panel.isin(BIG)].copy()
    rows = []
    for (bk, arm), G in piv.groupby(["book", "arm"]):
        cells = {(r.panel, r.cost): r for r in G.itertuples()}
        have = len(cells) == 4
        ne = [c for c in cells.values() if c.nonempty]
        lo = max([c.g_lo for c in ne], default=np.nan) if len(ne) == 4 else np.nan
        hi = min([c.g_hi for c in ne], default=np.nan) if len(ne) == 4 else np.nan
        rows.append(dict(book=bk, arm=arm, cells=len(cells), n_nonempty=len(ne),
                         all4=len(ne) == 4 and have,
                         joint_lo=lo, joint_hi=hi,
                         joint_width=(hi - lo) if np.isfinite(lo) and np.isfinite(hi) and hi >= lo else np.nan,
                         joint_ok=bool(np.isfinite(lo) and np.isfinite(hi) and hi >= lo),
                         min_cell_width=min([c.width for c in ne], default=np.nan) if len(ne) == 4 else np.nan))
    J = pd.DataFrame(rows).sort_values(["joint_ok", "joint_width"], ascending=[False, False])
    say(f"(book, arm) pairs on the large-cap pair: {len(J)}")
    say(f"  all four cells non-empty : {int(J.all4.sum())}")
    say(f"  joint interval non-empty : {int(J.joint_ok.sum())}   <- the clause's actual pass set")
    coll = J[J.all4 & ~J.joint_ok]
    say(f"  collapsed by intersection (4/4 individually, empty jointly): {len(coll)}"
        f"  {'-> the conjunction IS load-bearing' if len(coll) else '-> the conjunction adds nothing beyond 4/4'}")
    say("\n" + J.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nQ4b — the two standing objects checked against their own joint interval, cell by cell.")
    say("    Idea 84's by-product proposed idea 57's ew-band3 at g = 0.85 (target gross), and the "
        "incumbent book is EWall + vol60-dg at the published g = 0.75.")
    for arm in ("band3-rw", "band3-dg", "vol60-dg"):
        sub = iv0[(iv0.book == "EWall") & (iv0.arm == arm) & iv0.panel.isin(BIG)]
        say(f"\n  EWall + {arm}:")
        say("    " + sub[["panel", "cost", "nonempty", "m_lo", "m_hi", "g_lo", "g_hi", "width",
                          "lo_bar", "hi_bar"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"
                                                         ).replace("\n", "\n    "))
        for gtest in (0.75, 0.85):
            verdicts = []
            for r in sub.itertuples():
                if not r.nonempty:
                    verdicts.append(f"{r.panel}@{r.cost:.0f}=EMPTY")
                else:
                    inside = r.g_lo - 1e-9 <= gtest <= r.g_hi + 1e-9
                    verdicts.append(f"{r.panel}@{r.cost:.0f}={'in' if inside else 'OUT'}")
            say(f"    realised g = {gtest:.2f} : " + "  ".join(verdicts))
    say("    NOTE: g here is REALISED mean gross on a 0.05-wide m grid; idea 84 swept a 312-point "
        "fine ladder and also read a 5 bps rung, so a disagreement at one grid step is a "
        "resolution difference, and a disagreement of three steps is not.")

    say("\nsame conjunction with the small panel added (3 panels x 2 costs = 6 cells):")
    rows6 = []
    for (bk, arm), G in iv0.groupby(["book", "arm"]):
        ne = [r for r in G.itertuples() if r.nonempty]
        lo = max([c.g_lo for c in ne], default=np.nan) if len(ne) == 6 else np.nan
        hi = min([c.g_hi for c in ne], default=np.nan) if len(ne) == 6 else np.nan
        rows6.append(dict(book=bk, arm=arm, n_nonempty=len(ne),
                          joint_ok=bool(len(ne) == 6 and np.isfinite(lo) and np.isfinite(hi) and hi >= lo),
                          joint_width=(hi - lo) if len(ne) == 6 and np.isfinite(lo) and np.isfinite(hi) and hi >= lo else np.nan))
    J6 = pd.DataFrame(rows6)
    say(f"  6/6 cells non-empty {int((J6.n_nonempty == 6).sum())}; joint interval non-empty "
        f"{int(J6.joint_ok.sum())}")
    if J6.joint_ok.any():
        say(J6[J6.joint_ok].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- Q5 rule 8
    rule("Q5 — RULE 8 WALK-FORWARD.  Interval read on 2009-2016 ONLY; 2017-2026 untouched")
    IS = intervals(F, PHI0, DELTA0, bars_by_panel, "IS", keys=BARS_IS)
    OO = []
    Bo = bar_frame(F, PHI0, DELTA0, bars_by_panel, "full")   # not used for OOS; built below explicitly
    for p in PANELS:
        b = bars_by_panel[p][2]
        sub = F[F.panel == p]
        OO.append(pd.DataFrame(dict(
            book_id=sub.book_id, m=sub.m,
            oos_ok=(sub.OOS_Sharpe > b["soos"]) & (DELTA0 * abs(b["sdd"]) - sub.OOS_MaxDD.abs() > 0)
                   & (sub.OOS_CAGR - PHI0 * b["scagr"] > 0),
            OOS_CAGR=sub.OOS_CAGR, OOS_Sharpe=sub.OOS_Sharpe, OOS_MaxDD=sub.OOS_MaxDD,
            IS_Sharpe=sub.IS_Sharpe)))
    OO = pd.concat(OO, ignore_index=True)
    del Bo

    # (a) does IS WIDTH predict OOS better than the binary IS pass?
    oos_book = OO.groupby("book_id").agg(oos_any=("oos_ok", "any"),
                                         oos_n=("oos_ok", "sum"),
                                         oos_S_at1=("OOS_Sharpe", "first"))
    oos_at_m1 = OO[np.isclose(OO.m, 1.0)].set_index("book_id")
    P = IS.merge(oos_book, on="book_id").merge(
        oos_at_m1[["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "oos_ok"]].rename(
            columns={"oos_ok": "oos_ok_m1"}), on="book_id")
    say(f"IS intervals: non-empty {int(P.nonempty.sum())} of {len(P)}; "
        f"gapped {int((P[P.nonempty].gaps > 0).sum())}; median IS width "
        f"{P[P.nonempty].width.median():.4f}")
    say(f"OOS truth: books with SOME m clearing OOS-4b = {int(P.oos_any.sum())} of {len(P)}; "
        f"at the published m=1.00 = {int(P.oos_ok_m1.sum())}")
    say("\nPREDICTORS of the OOS outcome, over all 306 books:")
    binp = P.nonempty.astype(float)
    wid = P.width.fillna(-1.0)
    isS = P.book_id.map(oos_at_m1.IS_Sharpe)
    for lbl, target in (("OOS-4b pass (family)", P.oos_any.values),
                        ("OOS-4b pass at m=1.00", P.oos_ok_m1.values.astype(bool))):
        say(f"  vs {lbl}:")
        say(f"     binary IS pass  AUC {fmt(auc(binp, target))}   "
            f"IS width      AUC {fmt(auc(wid, target))}   "
            f"IS Sharpe(m=1) AUC {fmt(auc(isS, target))}")
    say("  vs OOS Sharpe at m=1.00 (Spearman over all books):")
    say(f"     binary IS pass  {fmt(spearman(binp, P.OOS_Sharpe))}   "
        f"IS width      {fmt(spearman(wid, P.OOS_Sharpe))}   "
        f"IS Sharpe(m=1) {fmt(spearman(isS, P.OOS_Sharpe))}")
    ne_is = P[P.nonempty]
    say(f"  WITHIN the {len(ne_is)} books the binary screen already admits (the only place width can add "
        f"information the incumbent screen does not have):")
    say(f"     Spearman(IS width, OOS Sharpe@m=1) = {fmt(spearman(ne_is.width, ne_is.OOS_Sharpe))}   "
        f"Spearman(IS width, OOS CAGR) = {fmt(spearman(ne_is.width, ne_is.OOS_CAGR))}   "
        f"Spearman(IS width, |OOS MaxDD|) = {fmt(spearman(ne_is.width, ne_is.OOS_MaxDD.abs()))}")
    say(f"     AUC(IS width -> OOS-4b pass at m=1.00) = {fmt(auc(ne_is.width, ne_is.oos_ok_m1.values.astype(bool)))}")

    # (b) selectors, per (panel, book, cost) cell
    say("\nSELECTORS — one arm+m chosen per (panel, book, cost) cell on IS information only, "
        "then held untouched through 2017-2026.")
    IS_at = F.set_index(["book_id", "m"])
    sel_rows = []
    for (p, bk, c), G in IS.groupby(["panel", "book", "cost"]):
        ne = G[G.nonempty]
        cellF = F[(F.panel == p) & (F.book == bk) & (F.cost == c)]
        oo = OO.set_index(["book_id", "m"])

        def take(name, bid, m_):
            if bid is None or not np.isfinite(m_):
                sel_rows.append(dict(panel=p, book=bk, cost=c, sel=name, arm="(none)", m=np.nan,
                                     OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan, entered=False))
                return
            r = oo.loc[(bid, round(m_, 2))]
            sel_rows.append(dict(panel=p, book=bk, cost=c, sel=name, arm=bid.split("|")[-1], m=m_,
                                 OOS_CAGR=float(r.OOS_CAGR), OOS_Sharpe=float(r.OOS_Sharpe),
                                 OOS_MaxDD=float(r.OOS_MaxDD), entered=True))

        # S0 no screen: the published point of the control arm
        take("S0 control m=1.00", f"{p}|{bk}|{c}|control", 1.00)
        # S1 incumbent (idea 144): IS point-4b screen at m=1.00, then argmax IS Sharpe at m=1.00
        c1 = cellF[np.isclose(cellF.m, 1.0)].copy()
        adm = set(IS[(IS.panel == p) & (IS.book == bk) & (IS.cost == c) & IS.nonempty].book_id)
        # point screen = the m=1.00 row itself admissible
        bfIS = bar_frame(c1, PHI0, DELTA0, bars_by_panel, "IS")
        c1 = c1.assign(is_ok=bfIS[list(BARS_IS)].all(axis=1).values)
        pool = c1[c1.is_ok]
        take("S1 IS-point-4b + argmaxIS-Sharpe",
             pool.loc[pool.IS_Sharpe.idxmax(), "book_id"] if len(pool) else None,
             1.00 if len(pool) else np.nan)
        # S2 widest IS interval, m = interval midpoint  (no parameter of its own)
        take("S2 widest IS interval, m=mid",
             ne.loc[ne.width.idxmax(), "book_id"] if len(ne) else None,
             float(ne.loc[ne.width.idxmax(), "m_mid"]) if len(ne) else np.nan)
        # S3 widest IS interval, m pinned at 1.00 (idea 146's PIN result) — only if 1.00 admissible
        ne1 = ne[(ne.m_lo <= 1.0) & (ne.m_hi >= 1.0)]
        take("S3 widest IS interval, m=1.00 pinned",
             ne1.loc[ne1.width.idxmax(), "book_id"] if len(ne1) else None,
             1.00 if len(ne1) else np.nan)
        # S4 argmax IS Sharpe, no screen at all (m=1.00)
        take("S4 argmaxIS-Sharpe, no screen",
             c1.loc[c1.IS_Sharpe.idxmax(), "book_id"], 1.00)
    S = pd.DataFrame(sel_rows)

    say("\nper-cell picks:")
    say(S.pivot_table(index=["panel", "book", "cost"], columns="sel", values="arm",
                      aggfunc="first").to_string())
    say("\nOOS RESULT, equal-weighted across the 18 (panel, book, cost) cells "
        "(a cell a selector declines to enter is EXCLUDED from its mean and counted):")
    agg = S.groupby("sel").agg(cells=("entered", "sum"),
                               OOS_CAGR=("OOS_CAGR", "mean"),
                               OOS_Sharpe=("OOS_Sharpe", "mean"),
                               OOS_MaxDD=("OOS_MaxDD", "mean"))
    # reference rows
    ref = []
    for p in PANELS:
        b = bars_by_panel[p][2]
        ref.append(dict(sel=f"SPY [{p} window]", cells=1, OOS_CAGR=b["scagr"],
                        OOS_Sharpe=b["soos"], OOS_MaxDD=b["sdd"]))
        for c in COSTS:
            v = v1_oos[p][c]
            ref.append(dict(sel=f"RULES v1 baseline {p}@{c:.0f}bps", cells=1, OOS_CAGR=v["CAGR"],
                            OOS_Sharpe=v["Sharpe"], OOS_MaxDD=v["MaxDD"]))
    R = pd.DataFrame(ref).set_index("sel")
    say(pd.concat([agg, R]).to_string(float_format=lambda x: f"{x:.4f}"))

    say("\nPAIRED reading — only the cells EVERY selector enters (the only fair comparison):")
    ent = S.pivot_table(index=["panel", "book", "cost"], columns="sel", values="entered", aggfunc="first")
    common = ent.fillna(False).all(axis=1)
    say(f"cells entered by all {S.sel.nunique()} selectors: {int(common.sum())} of {len(ent)}")
    if common.sum():
        keep = set(common[common].index)
        Sc = S[S.set_index(["panel", "book", "cost"]).index.isin(keep)]
        say(Sc.groupby("sel").agg(cells=("entered", "sum"), OOS_CAGR=("OOS_CAGR", "mean"),
                                  OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_MaxDD=("OOS_MaxDD", "mean")
                                  ).to_string(float_format=lambda x: f"{x:.4f}"))
        say("\nmatched vs the SPY / baseline numbers of the SAME cells:")
        mrows = []
        for (p, bk, c) in keep:
            b = bars_by_panel[p][2]
            v = v1_oos[p][c]
            mrows.append(dict(who="SPY", CAGR=b["scagr"], Sharpe=b["soos"], MaxDD=b["sdd"]))
            mrows.append(dict(who="RULES v1", CAGR=v["CAGR"], Sharpe=v["Sharpe"], MaxDD=v["MaxDD"]))
        say(pd.DataFrame(mrows).groupby("who").mean().to_string(float_format=lambda x: f"{x:.4f}"))

    # full-sample and halves for the two headline selectors, for the leaderboard row
    say("\nFULL-SAMPLE and HALVES of each selector's picks (equal-weighted across entered cells) — "
        "reported for the leaderboard; the picks themselves are IS-chosen.")
    fs = F.set_index(["book_id", "m"])
    frows = []
    for sel, G in S[S.entered].groupby("sel"):
        vals = []
        for r in G.itertuples():
            bid = f"{r.panel}|{r.book}|{r.cost}|{r.arm}"
            row = fs.loc[(bid, round(r.m, 2))]
            vals.append(dict(CAGR=row.CAGR, Sharpe=row.Sharpe, MaxDD=row.MaxDD, H1=row.H1, H2=row.H2))
        d = pd.DataFrame(vals).mean()
        frows.append(dict(sel=sel, cells=len(G), **d.to_dict()))
    FS = pd.DataFrame(frows).set_index("sel")
    say(FS.to_string(float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- verdict
    rule("VERDICT")
    w_auc = auc(wid, P.oos_any.values)
    b_auc = auc(binp, P.oos_any.values)
    w_auc1 = auc(wid, P.oos_ok_m1.values.astype(bool))
    b_auc1 = auc(binp, P.oos_ok_m1.values.astype(bool))
    within = spearman(ne_is.width, ne_is.OOS_Sharpe)
    say(f"width vs binary, AUC on OOS-4b(family): {fmt(w_auc)} vs {fmt(b_auc)}  "
        f"(delta {fmt(w_auc - b_auc)})")
    say(f"width vs binary, AUC on OOS-4b(m=1.00): {fmt(w_auc1)} vs {fmt(b_auc1)}  "
        f"(delta {fmt(w_auc1 - b_auc1)})")
    say(f"within-admitted Spearman(width, OOS Sharpe): {fmt(within)}")
    say(f"gapped intervals across all 42 grid points: {tot_gap} of {tot_ne}")
    say(f"right-censored at the no-leverage ceiling (published bars): {int(ne0.cens_hi.sum())} of {len(ne0)}")

    # ---------------------------------------------------------------- artefacts
    iv0.to_csv(OUT / f"{STEM}.intervals.csv", index=False)
    Q1.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    J.to_csv(OUT / f"{STEM}.joint.csv", index=False)
    IV4.to_csv(OUT / f"{STEM}.intervals4a.csv", index=False)
    P.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    S.to_csv(OUT / f"{STEM}.selectors.csv", index=False)
    F.to_csv(OUT / f"{STEM}.family.csv.gz", index=False, compression="gzip")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nwrote {STEM}.[intervals|grid|joint|intervals4a|walkforward|selectors|family|console]")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
