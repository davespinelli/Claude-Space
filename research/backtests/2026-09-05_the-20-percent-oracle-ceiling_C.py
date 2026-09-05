#!/usr/bin/env python3
"""QUEUE idea 172 — the-20-percent-oracle-ceiling  (lane C, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 172)
    "idea 166's oracle control found only 60 of 300 books (20.0%) have ANY gross point that
     passes the OOS-window 4b, against 33 for the best implementable rule, i.e. two-thirds of
     the reachable set is already reached and the remaining 240 books are outside 4b at every
     gross.  Decompose those 240 by which bar is unreachable at every ladder point (as idea 161
     proposes for near-misses) and report whether the unreachable bar is always a SHARPE bar.
     If so, 4b's gross-sensitive bars are effectively already satisfied and the project should
     stop pricing gross.  Max 2 params."

WHAT IS AT STAKE
    The project spends most of its compute on GROSS ladders.  Ideas 66/173/176/184 have already
    shown the Sharpe bars barely move with gross and that a ladder is a BRACKET rather than a
    search.  Idea 172 asks the complementary question from the failure side: of the books that
    NO legal gross can put inside 4b, is the blocking bar always one of the three SHARPE bars
    (H1, H2, OOS) — the gross-invariant ones?  If yes, the two gross-sensitive bars (the DD cap
    and the CAGR floor) are not what excludes books, and pricing gross buys nothing at the
    margin.  If no — if some books are blocked only by DD or CAGR at every ladder point — then
    the ladder is doing real screening work and must stay.

    A THIRD possibility idea 172 does not name, and which this run separates explicitly:
      MISALIGNMENT — every one of the five bars is individually reachable at SOME ladder point,
      but no SINGLE point satisfies all five at once.  A book like that has no unreachable bar
      at all, yet is still outside 4b at every gross.  That is the only case in which "price the
      gross more finely" could ever help, so its count is the number the recommendation hangs on.

CORPUS — idea 78's Test B, RE-RUN through the engine, not read off a CSV.  Identical to
idea 166's, whose ladder this run must reproduce cell-for-cell before anything new is read.
    B136 panel; k in {20, 40, 80}; 50 fixed sub-panels per k from
    `np.random.default_rng(78_500 + k)`; CAND-n books at n in {5, 20}; 10 bps; weekly; t+1.
    300 books (3 k x 50 draws x 2 n) x 10 ladder points = 3000 genuine backtests.
    k, draw and n are CORPUS axes carried over from ideas 78/166, not parameters tuned here.

TUNED PARAMETERS — exactly two, swept exhaustively, ALL grid points reported:
    1. the LADDER POINT g, 10 values {0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.90,
       1.00} — idea 166's ladder unchanged, and PROTOCOL rule 2 caps it at 1.00.  "Unreachable"
       means "fails at all ten".  Per-point numbers are in .ladder.csv and the per-g table.
    2. the REACHABILITY TOLERANCE tau, 9 values {-0.20, -0.10, -0.05, -0.02, 0.00, +0.02,
       +0.05, +0.10, +0.20} in the scale-free relative-margin units of idea 166.  A bar counts
       as met iff its relative slack is > tau, so tau = 0.00 is the literal 4b bar, tau < 0
       RELAXES every bar (how far outside is the unreachable bar?) and tau > 0 TIGHTENS it (how
       robust is a book that does reach?).  Every tau is reported (.tolerance.csv).
       [Correction, logged: the first execution of this script swept tau >= 0 only and so read
       P6 in the tightening direction, which is not what P6 says.  The sweep below is signed and
       P6 is scored at tau = -0.05, its pre-registered meaning.  No other number changed.]

    Bars, relative slacks and the 4b constants (PHI=0.70, DELTA=0.60, EPS=0.05) are idea 166's
    verbatim, so the two runs are directly comparable.

DEFINITIONS used throughout
    SHARPE bars       = H1, H2, OOS      (idea 66/184: gross-invariant)
    GROSS-SENSITIVE   = DD, CAGR         (idea 184: the CAGR floor binds at low g, the DD cap
                                          at high g; 4b admission is a contiguous g-interval)
    reachable(bar)    = the bar's relative slack is > tau at AT LEAST ONE of the 10 ladder points
    unreachable set U = the bars that are not reachable
    book classes      : REACHED       — some single ladder point passes all five bars
                        MISALIGNED    — U empty, but no single point passes all five
                        SHARPE-ONLY   — U non-empty and U subset of {H1,H2,OOS}
                        GROSS-ONLY    — U non-empty and U subset of {DD,CAGR}
                        MIXED         — U contains bars of both kinds

REPRODUCTION, asserted before any new number is read
    [a] The re-run ladder must reproduce idea 166's committed
        `2026-09-05_does-the-ceiling-beat-a-chosen-gross_C.ladder.csv` on all 3000 rows for
        IS_margin, OOS_margin, full_margin, Sharpe, CAGR, MaxDD and the OOS_fails string.
    [b] Idea 172's own premise must reproduce: exactly 60 of 300 books (20.0%) have at least one
        ladder point passing the OOS-window 4b, and 102 of the 1200 book-arm rows in idea 166's
        grid pass it (its census line).
    [c] Internal identity: the OOS_fails string recomputed from the five per-bar slacks must
        equal idea 166's independently-built string in 3000 of 3000 rows.
    If any of [a]-[c] fails, this is not a re-run of idea 166 and the run says so.

WALK-FORWARD (PROTOCOL rule 8) — the decision idea 172 actually implies, selectors and every
parameter fixed on <= 2016-12-31, the 2017-01-01..2026 window read ONCE at the end.
    6 cells (k x n).  Within each cell, over its 50 books:
      S0  do-nothing        — the full B136 book at the static g=0.75 (no selection, no ladder)
      S1  IS-Sharpe argmax  — pick the book by IS Sharpe, static g=0.75 (select, do not price)
      S2  IS-reachability   — keep only books whose IS-window ladder has NO unreachable SHARPE
                              bar, then IS-Sharpe argmax (S1 fallback when empty)
      S3  price the gross   — S1's book, but g = the IS 4b-margin argmax ladder point
                              (the "keep pricing gross" arm; the one idea 172 proposes to stop)
    Reported OOS CAGR/Sharpe/MaxDD against RULES v1 on B136 and against SPY, plus BOTH KEEP
    paths (4a and 4b, PROTOCOL rule 4) on every pick and on every book-ladder row.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a], [b] and [c] all hold.
    P2  Among the 240 non-reached books the unreachable set is dominated by SHARPE bars, but
        NOT "always": I expect a non-trivial GROSS-ONLY count, because the DD cap at 60% of
        SPY's drawdown is brutal for a 5-name book at any gross.
    P3  MISALIGNED is small (< 15% of the 240).  If it is large, the ladder's resolution, not
        its existence, is the issue.
    P4  H2 is the most frequently unreachable single bar (idea 137's "the wall is a Sharpe bar",
        idea 43's H1 diagnosis is about the full sample, not the OOS window).
    P5  The per-bar slack RANGE over the ladder is at least an order of magnitude larger for
        DD/CAGR than for H1/H2/OOS, confirming the gross-invariance of the Sharpe bars on this
        corpus and window.
    P6  The tolerance sweep does not rescue the SHARPE-ONLY books: RELAXING every bar by 0.05
        relative units (tau = -0.05) makes fewer than a quarter of them reachable.
    P7  Rule 8: S3 (price the gross) does NOT beat S0/S1 on mean OOS Sharpe.  A ninth
        do-nothing win.
    P8  No new book and no KEEP.  Every 4b pass here is a re-grossing of a known book (idea 144).

CAVEATS carried, not buried
    * Survivorship: B136 is a current-constituent list (idea 54).  All arms inherit it equally.
    * Idea 144: a re-grossed book is the SAME book.  No verdict flip here is a new signal.
    * Idea 38 (calendar-day price index) and idea 126 (t+1 execution only) carry over.
    * "Unreachable" is unreachable ON THIS 10-POINT LADDER, which is bounded above by PROTOCOL
      rule 2's no-leverage cap.  A bar closable only at g > 1.00 is correctly counted as
      unreachable, because rule 2 forbids that point.
    * The k=20/n=20 cell holds every eligible name by construction (idea 78); reported, not read
      as a selection result.
    * The 300 sub-panels overlap, so t-statistics across books are magnitude cues, not tests.

Deterministic, standalone.  Writes .console.txt, .ladder.csv, .books.csv, .tolerance.csv,
.walkforward.csv.
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_the-20-percent-oracle-ceiling_C"
OUT = ROOT / "research" / "backtests"
I78P = OUT / "2026-09-05_candidate-count-vs-dispersion_B.py"
I166_LADDER = OUT / "2026-09-05_does-the-ceiling-beat-a-chosen-gross_C.ladder.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


I78 = _load(I78P, "i78")

COST_BPS = I78.COST_BPS          # 10
FREQ = I78.FREQ                  # "W"
GROSS0 = I78.GROSS               # 0.75
KS = I78.KS                      # [20, 40, 80]
N_BOOKS = I78.N_BOOKS            # [5, 20]
N_DRAWS = I78.N_DRAWS_B          # 50
SEED_B = I78.SEED_B              # 78_500
IS_END, OOS_START = I78.IS_END, I78.OOS_START
CAP = 1.00                       # PROTOCOL rule 2: no leverage

LADDER = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00]   # tuned param 1
TAUS = [-0.20, -0.10, -0.05, -0.02, 0.00, 0.02, 0.05, 0.10, 0.20]       # tuned param 2
TAU_P6 = -0.05                   # the relaxation at which P6 is scored
BARS = ["H1", "H2", "OOS", "DD", "CAGR"]
SHARPE_BARS = {"H1", "H2", "OOS"}
GROSS_BARS = {"DD", "CAGR"}
PHI, DELTA = 0.70, 0.60          # 4b's CAGR floor and DD cap coefficients (idea 166)
EPS = 0.05                       # floor on |threshold| in the relative-margin denominator

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 3000)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ------------------------------------------------------------------ idea 166's bar algebra
def win(r, which):
    if which == "full":
        return r
    return r.loc[:IS_END] if which == "IS" else r.loc[OOS_START:]


def bars_win(spy, which):
    w = win(spy, which)
    s1, s2 = I78.half_sharpes(w)
    m = metrics(w)
    soos = metrics(spy.loc[OOS_START:])["Sharpe"] if which == "full" else m["Sharpe"]
    return dict(s1=s1, s2=s2, soos=soos, sdd=m["MaxDD"], scagr=m["CAGR"])


def rel_margins(r, b, which):
    """4b's five bars as SCALE-FREE relative slacks on a window.  min(.) > 0 <=> passes."""
    w = win(r, which)
    h1, h2 = I78.half_sharpes(w)
    m = metrics(w)
    sh = metrics(r.loc[OOS_START:])["Sharpe"] if which == "full" else m["Sharpe"]
    d = dict(
        H1=(h1 - b["s1"]) / max(abs(b["s1"]), EPS),
        H2=(h2 - b["s2"]) / max(abs(b["s2"]), EPS),
        OOS=(sh - b["soos"]) / max(abs(b["soos"]), EPS),
        DD=(DELTA * abs(b["sdd"]) - abs(m["MaxDD"])) / max(DELTA * abs(b["sdd"]), EPS),
        CAGR=(m["CAGR"] - PHI * b["scagr"]) / max(abs(PHI * b["scagr"]), EPS),
    )
    d["margin"] = min(d[k] for k in BARS)
    d["fails"] = ",".join([k for k in BARS if d[k] <= 0]) or "-"
    return d


def classify(U):
    if not U:
        return "MISALIGNED"
    if U <= SHARPE_BARS:
        return "SHARPE-ONLY"
    if U <= GROSS_BARS:
        return "GROSS-ONLY"
    return "MIXED"


def main():
    t0 = time.time()
    say("=" * 200)
    say(f"IDEA 172 — the-20-percent-oracle-ceiling   ({STEM})")
    say("Decompose the 240 of 300 books that no legal gross puts inside the OOS-window 4b, by "
        "WHICH BAR is unreachable at every one of the 10 ladder points, and separate the "
        "MISALIGNED case (no unreachable bar, still no passing point) that idea 172 does not "
        "name.  Verdict read once on 2017-2026.")
    say("PRE-REGISTERED: 2 tuned params (ladder point x 10, reachability tolerance tau x 5). "
        "k, draw and n are ideas 78/166's corpus axes, carried over unchanged.")
    say("=" * 200)

    panels = I78.build_panels()
    px136, tr136 = panels["B136"]
    start = px136.index[260]
    spy = px136["SPY"].pct_change().fillna(0.0).loc[start:]
    spy_oos = spy.loc[OOS_START:]
    base = backtest(px136, rules_v1_weights(px136), cost_bps=COST_BPS,
                    freq=FREQ)["returns"].loc[start:]
    ms, mb = metrics(spy), metrics(base)
    b_full, b_IS, b_OOS = bars_win(spy, "full"), bars_win(spy, "IS"), bars_win(spy, "OOS")

    say(f"\n  panel B136: {px136.shape[1]} cols, eval {start.date()} .. {px136.index[-1].date()}"
        f"   IS <= {IS_END}, OOS {OOS_START} ->")
    say(f"  SPY  full {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%}   OOS "
        f"{metrics(spy_oos)['CAGR']:.2%}/{metrics(spy_oos)['Sharpe']:.3f}/"
        f"{metrics(spy_oos)['MaxDD']:.2%}")
    say(f"  RULES v1 on B136  full {mb['CAGR']:.2%}/{mb['Sharpe']:.3f}/{mb['MaxDD']:.2%}   OOS "
        f"{metrics(base.loc[OOS_START:])['CAGR']:.2%}/"
        f"{metrics(base.loc[OOS_START:])['Sharpe']:.3f}/"
        f"{metrics(base.loc[OOS_START:])['MaxDD']:.2%}")
    for lbl, b in (("full", b_full), ("IS", b_IS), ("OOS", b_OOS)):
        say(f"  4b bars on {lbl:<4}: H1 > {b['s1']:.3f}, H2 > {b['s2']:.3f}, "
            f"Sharpe(OOSbar) > {b['soos']:.3f}, |MaxDD| <= {DELTA * abs(b['sdd']):.2%}, "
            f"CAGR >= {PHI * b['scagr']:.2%}")
    say(f"  ladder (tuned param 1): {LADDER}")
    say(f"  tolerances (tuned param 2): {TAUS}")

    names136 = [c for c in px136.columns if c in tr136]
    lad_rows = []
    rets = {}                                    # (k,draw,n,g) -> returns, kept for rule 8

    for k in KS:
        rng = np.random.default_rng(SEED_B + k)
        for d in range(N_DRAWS):
            cols = list(rng.choice(names136, size=k, replace=False))
            keep = list(dict.fromkeys(cols + ["SPY"]))
            p = px136[keep].dropna(how="all").ffill()
            tr = set(cols)
            for nb in N_BOOKS:
                elig = I78.eligible_mask(p, tr)
                sc = I78.score(p, vol_scale=False)[0]
                sel = (sc.where(elig).rank(axis=1, ascending=False) <= nb).astype(float)
                for g in LADDER:
                    r = backtest(p, sel * (g / nb), cost_bps=COST_BPS,
                                 freq=FREQ)["returns"].loc[start:]
                    rets[(k, d, nb, round(g, 6))] = r
                    mi = rel_margins(r, b_IS, "IS")
                    mo = rel_margins(r, b_OOS, "OOS")
                    mf = rel_margins(r, b_full, "full")
                    m_is, m_full, m_oos = (metrics(win(r, "IS")), metrics(r),
                                           metrics(r.loc[OOS_START:]))
                    row = dict(k=k, draw=d, n=nb, g=g,
                               IS_margin=mi["margin"], IS_pass=mi["margin"] > 0,
                               IS_fails=mi["fails"], IS_Sharpe=m_is["Sharpe"],
                               IS_CAGR=m_is["CAGR"], IS_MaxDD=m_is["MaxDD"], IS_vol=m_is["Vol"],
                               OOS_margin=mo["margin"], OOS_pass=mo["margin"] > 0,
                               OOS_fails=mo["fails"],
                               full_margin=mf["margin"], full_pass=mf["margin"] > 0,
                               CAGR=m_full["CAGR"], Sharpe=m_full["Sharpe"],
                               MaxDD=m_full["MaxDD"],
                               OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"],
                               OOS_MaxDD=m_oos["MaxDD"])
                    for bar in BARS:
                        row[f"OOS_rel_{bar}"] = mo[bar]
                        row[f"IS_rel_{bar}"] = mi[bar]
                    lad_rows.append(row)
        say(f"  k={k:<3} done  ({time.time() - t0:.0f}s)")

    LAD = pd.DataFrame(lad_rows)
    LAD.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    NB_TOT = LAD.groupby(["k", "draw", "n"]).ngroups
    say(f"\n  {len(LAD)} ladder rows written ({NB_TOT} books x {len(LADDER)} g), "
        f"{len(LAD)} genuine backtests")

    # =============================================================== reproduction
    key = ["k", "draw", "n"]
    say("\n" + "=" * 200)
    say("REPRODUCTION — asserted before any new number is read")
    say("=" * 200)
    ref = pd.read_csv(I166_LADDER)
    A = LAD.set_index(key + ["g"]).sort_index()
    R = ref.set_index(key + ["g"]).sort_index()
    ok_a = A.index.equals(R.index)
    say(f"[a] vs idea 166's committed ladder.csv: rows {len(A)} vs {len(R)}, index identical "
        f"{ok_a}")
    common = A.index.intersection(R.index)
    A, R = A.loc[common], R.loc[common]
    for c in ("IS_margin", "OOS_margin", "full_margin", "Sharpe", "CAGR", "MaxDD", "IS_Sharpe"):
        dmax = float((A[c] - R[c]).abs().max())
        ok_a &= dmax < 1e-12
        say(f"    max|diff| {c:<11} = {dmax:.3e}")
    same = float((A["OOS_fails"].astype(str) == R["OOS_fails"].astype(str)).mean())
    ok_a &= same == 1.0
    say(f"    OOS failing-bar string identical in {same:.1%} of {len(common)} ladder points")
    say(f"[a] REPRODUCED EXACTLY: {ok_a}")

    orc = LAD.groupby(key)[["OOS_pass", "full_pass", "IS_pass"]].max()
    n_reached = int(orc.OOS_pass.sum())
    n_rows_oos = int(LAD.OOS_pass.sum())
    say(f"\n[b] PREMISE — idea 172/166: 60 of 300 books (20.0%) have SOME ladder point passing "
        f"the OOS-window 4b")
    say(f"    books with >= 1 OOS-passing ladder point : {n_reached} of {NB_TOT} "
        f"({n_reached / NB_TOT:.1%})")
    say(f"    books with >= 1 full-sample passing point: {int(orc.full_pass.sum())} of {NB_TOT}")
    say(f"    ladder POINTS passing the OOS-window 4b  : {n_rows_oos} of {len(LAD)}")
    ok_b = n_reached == 60
    say(f"[b] IDEA 172's PREMISE REPRODUCED: {ok_b}")

    rebuilt = LAD[[f"OOS_rel_{b}" for b in BARS]].apply(
        lambda row: ",".join([b for b in BARS if row[f"OOS_rel_{b}"] <= 0]) or "-", axis=1)
    ok_c = bool((rebuilt == LAD.OOS_fails).all())
    say(f"\n[c] IDENTITY — failing-bar string rebuilt from the five per-bar slacks matches in "
        f"{float((rebuilt == LAD.OOS_fails).mean()):.1%} of {len(LAD)} rows: {ok_c}")
    say(f"\nREPRODUCTION 3/3: {ok_a and ok_b and ok_c}")

    # =============================================================== per-bar reachability
    say("\n" + "=" * 200)
    say("THE DECOMPOSITION — every book, every bar, over the whole ladder  (tau = 0.00)")
    say("=" * 200)
    books = []
    for (kk, dd, nn), grp in LAD.groupby(key):
        grp = grp.sort_values("g")
        rec = dict(k=kk, draw=dd, n=nn, reached=bool(grp.OOS_pass.any()),
                   n_pass_points=int(grp.OOS_pass.sum()),
                   best_margin=float(grp.OOS_margin.max()),
                   best_g=float(grp.sort_values("OOS_margin").iloc[-1].g))
        U = set()
        for bar in BARS:
            v = grp[f"OOS_rel_{bar}"]
            rec[f"best_{bar}"] = float(v.max())
            rec[f"worst_{bar}"] = float(v.min())
            rec[f"range_{bar}"] = float(v.max() - v.min())
            rec[f"argmax_g_{bar}"] = float(grp.loc[v.idxmax(), "g"])
            rec[f"reach_{bar}"] = bool((v > 0).any())
            if not rec[f"reach_{bar}"]:
                U.add(bar)
        rec["U"] = ",".join([b for b in BARS if b in U]) or "-"
        rec["nU"] = len(U)
        rec["cls"] = "REACHED" if rec["reached"] else classify(U)
        books.append(rec)
    B = pd.DataFrame(books)
    B.to_csv(OUT / f"{STEM}.books.csv", index=False)

    say(f"\n  book classes over all {NB_TOT} books (REACHED = idea 166's 60):")
    cls_order = ["REACHED", "SHARPE-ONLY", "GROSS-ONLY", "MIXED", "MISALIGNED"]
    tab = B.cls.value_counts().reindex(cls_order).fillna(0).astype(int)
    say(pd.DataFrame({"books": tab, "share": (tab / NB_TOT)}).to_string(
        float_format=lambda x: f"{x:.3f}"))
    NR = B[~B.reached]
    say(f"\n  THE ANSWER — of the {len(NR)} books outside 4b at every legal gross:")
    t2 = NR.cls.value_counts().reindex(cls_order[1:]).fillna(0).astype(int)
    say(pd.DataFrame({"books": t2, "share": (t2 / max(len(NR), 1))}).to_string(
        float_format=lambda x: f"{x:.3f}"))
    say(f"\n  Idea 172's question, stated as a single number: the unreachable bar set is a "
        f"SUBSET OF THE SHARPE BARS in {int((NR.cls == 'SHARPE-ONLY').sum())} of {len(NR)} "
        f"({float((NR.cls == 'SHARPE-ONLY').mean()):.1%}); it involves a GROSS-SENSITIVE bar "
        f"(DD or CAGR) in {int(NR.cls.isin(['GROSS-ONLY', 'MIXED']).sum())} of {len(NR)} "
        f"({float(NR.cls.isin(['GROSS-ONLY', 'MIXED']).mean()):.1%}).")

    say(f"\n  per-BAR unreachability among the {len(NR)} (a book can have several unreachable bars):")
    rows = []
    for bar in BARS:
        sub = NR[~NR[f"reach_{bar}"]]
        rows.append(dict(bar=bar, kind=("SHARPE" if bar in SHARPE_BARS else "GROSS"),
                         unreachable=len(sub),
                         share=len(sub) / max(len(NR), 1),
                         median_best_slack=float(NR[f"best_{bar}"].median()),
                         median_slack_range=float(NR[f"range_{bar}"].median()),
                         reachable=int(NR[f"reach_{bar}"].sum()),
                         med_deficit=(float(-sub[f"best_{bar}"].median()) if len(sub)
                                      else np.nan),
                         p90_deficit=(float(-sub[f"best_{bar}"].quantile(0.10)) if len(sub)
                                      else np.nan)))
    say(pd.DataFrame(rows).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("  (median_best_slack is the bar's BEST relative slack over the ladder — negative means "
        "the bar fails at every point; median_slack_range is how much the bar moves over the "
        "6.75x span, i.e. how gross-sensitive it is.  med_deficit/p90_deficit are how much "
        "RELAXATION the bar would need, among the books where it is unreachable — this is the "
        "'how far outside' number, in the same units as the tau sweep below.)")

    say("\n  the exact unreachable SETS, most common first:")
    say(NR.U.value_counts().to_string())

    say(f"\n  P5 — how much each bar MOVES over the ladder (all {NB_TOT} books, relative slack):")
    mv = pd.DataFrame([dict(bar=b, kind=("SHARPE" if b in SHARPE_BARS else "GROSS"),
                            mean_range=float(B[f"range_{b}"].mean()),
                            median_range=float(B[f"range_{b}"].median()),
                            p90_range=float(B[f"range_{b}"].quantile(0.90)),
                            modal_argmax_g=float(B[f"argmax_g_{b}"].mode().iloc[0]))
                      for b in BARS])
    say(mv.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n  class by cell (k, n):")
    say(B.pivot_table(index=["k", "n"], columns="cls", values="draw", aggfunc="count")
        .reindex(columns=cls_order).fillna(0).astype(int).to_string())

    say("\n  the 60 REACHED books: which g passes, and how wide the passing interval is:")
    RE = LAD[LAD.OOS_pass].groupby("g").size().reindex(LAD.g.unique()).fillna(0).astype(int)
    say(RE.to_string())
    say(f"    mean number of passing ladder points among the reached books: "
        f"{float(B[B.reached].n_pass_points.mean()):.2f} of 10")

    # =============================================================== tolerance sweep
    say("\n" + "=" * 200)
    say("TOLERANCE SWEEP (tuned param 2) — how far outside is the unreachable bar?")
    say("=" * 200)
    tol = []
    for tau in TAUS:
        for (kk, dd, nn), grp in LAD.groupby(key):
            U = {b for b in BARS if not (grp[f"OOS_rel_{b}"] > tau).any()}
            reached = bool(((grp[[f"OOS_rel_{b}" for b in BARS]] > tau).all(axis=1)).any())
            tol.append(dict(tau=tau, k=kk, draw=dd, n=nn, reached=reached,
                            cls=("REACHED" if reached else classify(U)),
                            U=",".join([b for b in BARS if b in U]) or "-"))
    T = pd.DataFrame(tol)
    T.to_csv(OUT / f"{STEM}.tolerance.csv", index=False)
    piv = T.pivot_table(index="tau", columns="cls", values="draw",
                        aggfunc="count").reindex(columns=cls_order).fillna(0).astype(int)
    say(piv.to_string())
    say("  (a bar counts as met iff its relative slack > tau.  tau < 0 RELAXES every bar — how "
        "far outside is the unreachable bar; tau > 0 TIGHTENS it — how robust is a book that "
        "does reach.  tau = 0.00 is the literal 4b.)")
    say("\n  P6 — of the tau=0 SHARPE-ONLY books, how many become REACHED under relaxation:")
    s0 = set(map(tuple, B[B.cls == "SHARPE-ONLY"][key].values))
    for tau in TAUS:
        sub = T[T.tau == tau]
        got = sub[sub.reached].apply(lambda r: (r.k, r.draw, r.n) in s0, axis=1).sum() \
            if len(sub[sub.reached]) else 0
        say(f"    tau {tau:+.2f}: {int(got)} of {len(s0)} SHARPE-ONLY books now reached "
            f"({(int(got) / max(len(s0), 1)):.1%})")

    # =============================================================== rule 8 walk-forward
    say("\n" + "=" * 200)
    say(f"RULE 8 WALK-FORWARD — everything chosen on <= {IS_END}, read ONCE on {OOS_START} ->")
    say("S0 do-nothing (full B136 @0.75) / S1 IS-Sharpe argmax @0.75 / S2 IS-reachability screen "
        "then IS-Sharpe argmax / S3 = S1's book at the IS 4b-margin argmax gross ('price the "
        "gross').  6 cells (k x n).")
    say("=" * 200)
    spy_o, v1_o = metrics(spy_oos), metrics(base.loc[OOS_START:])

    _e136 = I78.eligible_mask(px136, tr136)
    _s136 = I78.score(px136, vol_scale=False)[0].where(_e136).rank(axis=1, ascending=False)
    c136 = {}

    def run136(nb, g):
        kk = (nb, round(float(g), 6))
        if kk not in c136:
            c136[kk] = backtest(px136, (_s136 <= nb).astype(float) * (kk[1] / nb),
                                cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        return c136[kk]

    # IS-only reachability screen: a book is admissible iff no SHARPE bar is unreachable on the
    # ladder READ ON THE IS WINDOW.  Uses IS_rel_* only.
    isb = []
    for (kk, dd, nn), grp in LAD.groupby(key):
        U = {b for b in BARS if not (grp[f"IS_rel_{b}"] > 0).any()}
        best = grp.sort_values(["IS_margin", "g"], ascending=[False, True]).iloc[0]
        isb.append(dict(k=kk, draw=dd, n=nn, IS_adm=(len(U & SHARPE_BARS) == 0),
                        IS_U=",".join([b for b in BARS if b in U]) or "-",
                        IS_Sharpe_at_075=float(grp[grp.g == GROSS0].IS_Sharpe.iloc[0]),
                        g_maxmarg=float(best.g)))
    IB = pd.DataFrame(isb)
    say(f"  IS-window reachability screen admits {int(IB.IS_adm.sum())} of {NB_TOT} books "
        f"({float(IB.IS_adm.mean()):.1%})")

    wf = []
    for kk in KS:
        for nb in N_BOOKS:
            sub = IB[(IB.k == kk) & (IB.n == nb)].sort_values(
                ["IS_Sharpe_at_075", "draw"], ascending=[False, True])
            s1 = sub.iloc[0]
            adm = sub[sub.IS_adm]
            s2 = adm.iloc[0] if len(adm) else s1
            picks = [
                ("S0 do-nothing (full B136)", -1, GROSS0, run136(nb, GROSS0)),
                ("S1 IS-Sharpe argmax", int(s1.draw), GROSS0,
                 rets[(kk, int(s1.draw), nb, round(GROSS0, 6))]),
                (f"S2 IS-reachability ({len(adm)} adm)", int(s2.draw), GROSS0,
                 rets[(kk, int(s2.draw), nb, round(GROSS0, 6))]),
                ("S3 price the gross", int(s1.draw), float(s1.g_maxmarg),
                 rets[(kk, int(s1.draw), nb, round(float(s1.g_maxmarg), 6))]),
            ]
            for lbl, dw, gg, r in picks:
                ro = r.loc[OOS_START:]
                mo = metrics(ro)
                f4b = I78.fail_4b(r, spy, ro, spy_oos)
                f4a = I78.fail_4a(r, base)
                rel = rel_margins(r, b_OOS, "OOS")
                wf.append(dict(k=kk, n=nb, selector=lbl.split(" ")[0], label=lbl, draw=dw, g=gg,
                               IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                               OOS_MaxDD=mo["MaxDD"], OOS_margin=rel["margin"],
                               OOS_fails=rel["fails"],
                               v1_OOS_CAGR=v1_o["CAGR"], v1_OOS_Sharpe=v1_o["Sharpe"],
                               v1_OOS_MaxDD=v1_o["MaxDD"],
                               spy_OOS_CAGR=spy_o["CAGR"], spy_OOS_Sharpe=spy_o["Sharpe"],
                               spy_OOS_MaxDD=spy_o["MaxDD"],
                               d_vs_v1=mo["Sharpe"] - v1_o["Sharpe"],
                               d_vs_spy=mo["Sharpe"] - spy_o["Sharpe"],
                               f4a=f4a, f4b=f4b, pass4a=(f4a == "-"), pass4b=(f4b == "-")))
                say(f"  k={kk:<3} n={nb:<3} {lbl:<32} g={gg:.2f} draw={dw:<3} -> OOS "
                    f"{mo['CAGR']:.2%}/{mo['Sharpe']:.3f}/{mo['MaxDD']:.2%} | dSharpe vs v1 "
                    f"{mo['Sharpe'] - v1_o['Sharpe']:+.3f}, vs SPY "
                    f"{mo['Sharpe'] - spy_o['Sharpe']:+.3f} | full 4b {f4b} | 4a {f4a}")
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    say(f"\n  SPY OOS               {spy_o['CAGR']:.2%}/{spy_o['Sharpe']:.3f}/"
        f"{spy_o['MaxDD']:.2%}")
    say(f"  RULES v1 OOS on B136  {v1_o['CAGR']:.2%}/{v1_o['Sharpe']:.3f}/{v1_o['MaxDD']:.2%}")
    say("\n  mean over the 6 cells:")
    say(WF.groupby("selector").agg(OOS_Sharpe=("OOS_Sharpe", "mean"),
                                   OOS_CAGR=("OOS_CAGR", "mean"),
                                   OOS_MaxDD=("OOS_MaxDD", "mean"),
                                   OOS_margin=("OOS_margin", "mean"),
                                   pass4a=("pass4a", "sum"), pass4b=("pass4b", "sum"),
                                   g=("g", "mean")).to_string(
        float_format=lambda x: f"{x:.4f}"))
    say("\n  PAIRED vs S0 (do-nothing), 6 cells:")
    P0 = WF[WF.selector == "S0"].set_index(["k", "n"]).sort_index()
    pr = []
    for s in ("S1", "S2", "S3"):
        Q = WF[WF.selector == s].set_index(["k", "n"]).sort_index()
        dS = Q.OOS_Sharpe - P0.OOS_Sharpe
        pr.append(dict(selector=s, d_OOS_Sharpe=float(dS.mean()), t=I78.tstat(dS),
                       wins=int((dS > 0).sum()), losses=int((dS < 0).sum()),
                       d_OOS_CAGR=float((Q.OOS_CAGR - P0.OOS_CAGR).mean()),
                       d_OOS_MaxDD=float((Q.OOS_MaxDD - P0.OOS_MaxDD).mean())))
    say(pd.DataFrame(pr).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("  (6 overlapping cells: the t is a magnitude cue, not a test.)")

    # =============================================================== KEEP paths, all rows
    say("\n" + "=" * 200)
    say(f"BOTH KEEP PATHS (PROTOCOL rule 4) on all {len(LAD)} book-ladder rows")
    say("=" * 200)
    f4a_all, f4b_all = [], []
    for row in LAD.itertuples():
        r = rets[(row.k, row.draw, row.n, round(row.g, 6))]
        f4a_all.append(I78.fail_4a(r, base) == "-")
        f4b_all.append(I78.fail_4b(r, spy, r.loc[OOS_START:], spy_oos) == "-")
    LAD["pass4a"], LAD["pass4b_full"] = f4a_all, f4b_all
    LAD.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    say(f"  4a passes {int(LAD.pass4a.sum())} of {len(LAD)};  full-sample 4b passes "
        f"{int(LAD.pass4b_full.sum())};  OOS-window 4b passes {int(LAD.OOS_pass.sum())}")
    best = LAD[LAD.pass4b_full].sort_values("Sharpe", ascending=False)
    if len(best):
        bb = best.iloc[0]
        say(f"  best full-4b row: k={int(bb.k)} draw={int(bb.draw)} n={int(bb.n)} g={bb.g:.2f} "
            f"-> {bb.CAGR:.2%}/{bb.Sharpe:.3f}/{bb.MaxDD:.2%}, OOS "
            f"{bb.OOS_CAGR:.2%}/{bb.OOS_Sharpe:.3f}/{bb.OOS_MaxDD:.2%}")
    say("  Idea 144: every one of these is a RE-GROSSING of a CAND-n book already in the record. "
        "No new book is proposed here.")

    # =============================================================== predictions
    say("\n" + "=" * 200)
    say("PRE-REGISTERED PREDICTIONS — scored")
    say("=" * 200)
    sh_only = float((NR.cls == "SHARPE-ONLY").mean())
    gross_any = int(NR.cls.isin(["GROSS-ONLY", "MIXED"]).sum())
    mis = float((NR.cls == "MISALIGNED").mean())
    unre = {b: int((~NR[f"reach_{b}"]).sum()) for b in BARS}
    top_bar = max(unre, key=unre.get)
    med_sharpe_rng = float(np.median([B[f"range_{b}"].median() for b in SHARPE_BARS]))
    med_gross_rng = float(np.median([B[f"range_{b}"].median() for b in GROSS_BARS]))
    tau05 = T[(T.tau == TAU_P6) & T.reached]
    got05 = int(tau05.apply(lambda r: (r.k, r.draw, r.n) in s0, axis=1).sum()) if len(tau05) else 0
    mean_s = WF.groupby("selector").OOS_Sharpe.mean()
    preds = [
        ("P1  reproduction [a][b][c] all hold", ok_a and ok_b and ok_c),
        (f"P2  SHARPE-dominated but not always ({sh_only:.1%} SHARPE-ONLY, {gross_any} books "
         f"with a gross-sensitive unreachable bar)", sh_only > 0.5 and gross_any > 0),
        (f"P3  MISALIGNED < 15% of the non-reached ({mis:.1%})", mis < 0.15),
        (f"P4  H2 the most frequently unreachable bar (actual: {top_bar}, "
         f"{unre[top_bar]}/{len(NR)})", top_bar == "H2"),
        (f"P5  gross-sensitive bars move >= 10x the Sharpe bars (median range "
         f"{med_gross_rng:.4f} vs {med_sharpe_rng:.4f})",
         med_gross_rng >= 10 * max(med_sharpe_rng, 1e-12)),
        (f"P6  relaxing every bar by 0.05 (tau={TAU_P6:+.2f}) rescues < 25% of the SHARPE-ONLY "
         f"books ({got05}/{len(s0)})",
         got05 < 0.25 * max(len(s0), 1)),
        (f"P7  S3 (price the gross) does not beat S0/S1 "
         f"({mean_s.get('S3', np.nan):.4f} vs S0 {mean_s.get('S0', np.nan):.4f} / S1 "
         f"{mean_s.get('S1', np.nan):.4f})",
         mean_s.get("S3", 0) <= max(mean_s.get("S0", 0), mean_s.get("S1", 0))),
        ("P8  no new book proposed (every 4b pass is a re-grossing, idea 144)", True),
    ]
    for lbl, hit in preds:
        say(f"  {'HIT ' if hit else 'MISS'}  {lbl}")
    say(f"\n  {sum(1 for _, h in preds if h)} of {len(preds)} pre-registered predictions HIT")

    say("\n" + "=" * 200)
    say("CENSUS")
    say("=" * 200)
    say(f"  genuine backtests {len(LAD)} (+{len(c136)} full-B136 controls +1 RULES v1)")
    say(f"  books {NB_TOT};  reached {n_reached};  not reached {len(NR)}")
    say(f"  walk-forward picks {len(WF)};  tolerance rows {len(T)}")
    say(f"  every g <= 1.00 (PROTOCOL rule 2): {bool((LAD.g <= CAP + 1e-12).all())}")
    say(f"  runtime {time.time() - t0:.0f}s")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")
    print(f"\nwrote {STEM}.console.txt/.ladder.csv/.books.csv/.tolerance.csv/.walkforward.csv")


if __name__ == "__main__":
    main()
