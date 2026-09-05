#!/usr/bin/env python3
"""QUEUE idea 166 — does-the-ceiling-beat-a-chosen-gross  (lane C, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 166)
    "idea 156 found `g = min(g_req, 1.00)` is the only setting that puts the small-pool cell
     inside 4b (0.00 -> 0.12 -> 0.00), which is suspicious: the ceiling is an arbitrary constant
     that happens to sit where the two bars cross.  Test it against a gross chosen on the IS
     window to maximise the 4b margin, and against idea 152's static-ladder interval midpoint,
     on the same 300 books.  If the ceiling wins, it is load-bearing; if a chosen gross wins,
     idea 148's clause is a coincidence of units.  Max 2 params."

WHAT IS AT STAKE.
    Idea 148 proposed, and idea 156 strengthened, a RULES/PROTOCOL clause of the form "run the
    book at `g = min(g_required, 1.00)`".  The 1.00 in that expression is not a fitted number:
    it is PROTOCOL rule 2's no-leverage constraint, i.e. a unit of account.  Idea 156's headline
    observation is that the small-pool cell (k=20, n=20) passes 4b at 0.12 under that ceiling
    and at 0.00 both below it (static 0.75) and above it (uncapped vol match).  A single
    non-monotone cell at exactly the legal boundary is the signature of BOTH of the following:

      (i)  the ceiling is load-bearing — the CAGR floor pushes gross up, the DD cap pushes it
           down, and 1.00 happens to be inside the resulting interval for these books; or
      (ii) the ceiling is a coincidence of units — ANY sensibly chosen gross would land in that
           same interval, and the constant 1.00 is doing no work that a gross chosen on the
           in-sample window would not do better.

    (i) and (ii) are separated by a direct horse race between gross-choice RULES, all of them
    prospective (IS-only) and all of them capped at 1.00 by PROTOCOL rule 2, evaluated on the
    untouched OOS window.  That is this run.

CORPUS — idea 78's Test B, re-run, not approximated.  IDENTICAL to idea 156's.
    The B136 panel; k in {20, 40, 80}; 50 fixed sub-panels per k from
    `np.random.default_rng(78_500 + k)`; CAND-n books at n in {5, 20}; 10 bps; weekly; t+1.
    300 books (3 k x 50 draws x 2 n).  k, draw and n are CORPUS axes carried over from idea 78,
    not parameters tuned here.

TUNED PARAMETERS — exactly two, swept exhaustively, ALL grid points in .grid.csv / .ladder.csv:
    1. the GROSS-CHOICE RULE, 4 values (every one IS-only and capped at 1.00):
         STATIC    g = 0.75                                       (idea 78's own; the control)
         CEILING   g = min(0.75 * vol(SPY,IS) / vol(book@0.75,IS), 1.00)     (idea 148/156)
         MAXMARG   g = ladder argmax of the IS 4b relative min-margin (ties -> smaller g)
         MIDPOINT  midpoint of the contiguous IS-4b-PASSING ladder interval containing the
                   MAXMARG point; empty interval -> falls back to MAXMARG (counted, reported)
    2. the LADDER POINT g, 10 values {0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.90,
       1.00}.  This is the search space MAXMARG and MIDPOINT choose from, and it is itself
       reported book-by-book so the choice rules can be audited against every point.

    The "4b relative min-margin" scalarises 4b's five bars into one scale-free number:
        rel(H1)=(h1-s1)/|s1|, rel(H2)=(h2-s2)/|s2|, rel(OOSbar)=(sh-soos)/|soos|,
        rel(DD)=(0.60|sdd|-|dd|)/(0.60|sdd|), rel(CAGR)=(cagr-0.70*scagr)/(0.70*scagr),
        margin = min of the five.  margin > 0 <=> the book passes 4b on that window.
    Read on the IS window it is a legal prospective screen; read on OOS it is the score.

REPRODUCTION, asserted before any new number is read
    [a] The STATIC arm (g=0.75) must reproduce idea 78's committed
        `2026-09-05_candidate-count-vs-dispersion_B.gridB.csv` cell-for-cell on CAGR, Sharpe,
        MaxDD, H1, H2, Sharpe_OOS and the 4b failing-bar string, for all 300 books.
    [b] Idea 156's own headline must reproduce: 55.0% of the 300 books need g > 1.00; the
        k=20/n=20 cell 4b pass rate is 0.00 at STATIC and 0.12 at CEILING.
    If [a] or [b] fails, this is not a re-run of ideas 78/156 and is reported as such.

WALK-FORWARD (PROTOCOL rule 8) — selectors fixed BEFORE any OOS number is read:
    Within each gross arm and separately at each n: S1 = IS Sharpe argmax over the 150 books;
    S2 = 4b-aware IS screen (IS halves, IS DD cap, IS CAGR floor) then IS Sharpe argmax, with an
    S1 fallback when the screen is empty; S0 = the do-nothing full-B136 control at the same
    gross rule.  Everything (including each arm's g) chosen on <= 2016-12-31 only and read ONCE
    on 2017-01-01..2026.  OOS CAGR/Sharpe/MaxDD reported against RULES v1 on B136 and SPY.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a] and [b] both hold.
    P2  CEILING sits at exactly 1.00 for a majority of books (idea 156's 55%), so it is not
        really a "chosen" gross at all — it is "as much gross as rule 2 allows".
    P3  MAXMARG picks a gross well BELOW 1.00 for most books, because the DD cap is the bar
        that binds once CAGR is bought with gross (idea 156's central finding).
    P4  On the IS window MAXMARG beats CEILING by construction (it is the argmax).  The test is
        OOS: I expect MAXMARG >= CEILING on OOS 4b pass count, i.e. the ceiling is NOT uniquely
        load-bearing and idea 148's clause is at least partly a coincidence of units.
    P5  MIDPOINT >= MAXMARG on OOS, because the interval midpoint is the more robust point
        estimate of the same interval (idea 152's reading) and MAXMARG sits on a boundary.
    P6  No arm produces a 4b KEEP that PROTOCOL would accept.  Nothing here is a new book.

CAVEATS carried, not buried
    * Survivorship: B136 is a current-constituent list (idea 54).  All arms inherit it equally.
    * Idea 144: a re-grossed book is the SAME book.  No verdict flip here is a new signal.
    * Idea 66's "gross is an exact lever" is checked here, not assumed (the ladder is re-run
      through the engine at every point rather than scaled analytically).
    * Idea 38 (calendar-day price index) and idea 126 (t+1 execution only) carry over.
    * The k=20/n=20 cell holds every eligible name by construction, so its "selection" is a
      weighting artefact (idea 78 flagged this); reported, not read as a selection result.
    * A gross-choice rule fitted on IS is one more thing fitted on IS.  The OOS window is read
      exactly once, at the end, and is the only basis for the verdict.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .ladder.csv, .choices.csv,
.walkforward.csv, .cells.csv.
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

STEM = "2026-09-05_does-the-ceiling-beat-a-chosen-gross_C"
OUT = ROOT / "research" / "backtests"
I78P = OUT / "2026-09-05_candidate-count-vs-dispersion_B.py"


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

LADDER = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00]
ARMS = ["STATIC", "CEILING", "MAXMARG", "MIDPOINT"]
PHI, DELTA = 0.70, 0.60          # 4b's CAGR floor and DD cap coefficients
EPS = 0.05                       # floor on |threshold| in the relative-margin denominator

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 3000)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ------------------------------------------------------------------ window helpers
def win(r, which):
    if which == "full":
        return r
    return r.loc[:IS_END] if which == "IS" else r.loc[OOS_START:]


def bars_win(spy, which):
    """SPY's 4b reference numbers on a window (same convention as idea 153's bars_win)."""
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
    d["margin"] = min(d[k] for k in ("H1", "H2", "OOS", "DD", "CAGR"))
    d["fails"] = ",".join([k for k in ("H1", "H2", "OOS", "DD", "CAGR") if d[k] <= 0]) or "-"
    return d


def midpoint_interval(gs, passes, gstar):
    """Midpoint of the contiguous run of passing ladder points containing gstar.

    Returns (g_mid, lo, hi) or (nan, nan, nan) when gstar itself does not pass."""
    i = gs.index(gstar)
    if not passes[i]:
        return np.nan, np.nan, np.nan
    lo = i
    while lo - 1 >= 0 and passes[lo - 1]:
        lo -= 1
    hi = i
    while hi + 1 < len(gs) and passes[hi + 1]:
        hi += 1
    return 0.5 * (gs[lo] + gs[hi]), gs[lo], gs[hi]


def main():
    t0 = time.time()
    say("=" * 200)
    say(f"IDEA 166 — does-the-ceiling-beat-a-chosen-gross   ({STEM})")
    say("Horse race between four IS-only, rule-2-legal gross-choice rules on idea 78's SAME 300 "
        "books: STATIC 0.75, idea 148/156's CEILING min(g_req,1.00), the IS 4b-margin argmax "
        "MAXMARG, and idea 152's interval MIDPOINT.  Verdict read once on 2017-2026.")
    say("PRE-REGISTERED: 2 tuned params (gross-choice rule x 4, ladder point x 10). k, draw and "
        "n are idea 78's corpus axes, carried over unchanged.")
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
    vol_spy_is = metrics(spy.loc[:IS_END])["Vol"]

    say(f"\n  panel B136: {px136.shape[1]} cols, eval {start.date()} .. {px136.index[-1].date()}"
        f"   IS <= {IS_END}, OOS {OOS_START} ->")
    say(f"  SPY  full {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%}  vol "
        f"{ms['Vol']:.2%}   OOS {metrics(spy_oos)['CAGR']:.2%}/"
        f"{metrics(spy_oos)['Sharpe']:.3f}/{metrics(spy_oos)['MaxDD']:.2%}")
    say(f"  RULES v1 on B136  full {mb['CAGR']:.2%}/{mb['Sharpe']:.3f}/{mb['MaxDD']:.2%}   "
        f"OOS {metrics(base.loc[OOS_START:])['CAGR']:.2%}/"
        f"{metrics(base.loc[OOS_START:])['Sharpe']:.3f}/"
        f"{metrics(base.loc[OOS_START:])['MaxDD']:.2%}")
    for lbl, b in (("full", b_full), ("IS", b_IS), ("OOS", b_OOS)):
        say(f"  4b bars on {lbl:<4}: H1 > {b['s1']:.3f}, H2 > {b['s2']:.3f}, "
            f"Sharpe(OOSbar) > {b['soos']:.3f}, |MaxDD| <= {DELTA * abs(b['sdd']):.2%}, "
            f"CAGR >= {PHI * b['scagr']:.2%}")
    say(f"  SPY IS realised vol {vol_spy_is:.2%} — the CEILING arm's vol-match target")
    say(f"  ladder: {LADDER}")

    names136 = [c for c in px136.columns if c in tr136]

    lad_rows, choice_rows, grid_rows = [], [], []
    rets = {}                                     # (k,draw,n,arm) -> returns of the chosen g

    for k in KS:
        rng = np.random.default_rng(SEED_B + k)
        for d in range(N_DRAWS):
            cols = list(rng.choice(names136, size=k, replace=False))
            keep = list(dict.fromkeys(cols + ["SPY"]))
            p = px136[keep].dropna(how="all").ffill()
            tr = set(cols)
            for nb in N_BOOKS:
                # the selection mask once; the weight is mask * (g / n), i.e. BIT-FOR-BIT
                # idea 78's `weights_cand(..., gross=g)`.  Only the ranking is reused.
                elig = I78.eligible_mask(p, tr)
                sc = I78.score(p, vol_scale=False)[0]
                sel = (sc.where(elig).rank(axis=1, ascending=False) <= nb).astype(float)
                cache = {}

                def run(g, _sel=sel, _p=p, _nb=nb, _c=cache):
                    key = round(float(g), 6)
                    if key not in _c:
                        _c[key] = backtest(_p, _sel * (key / _nb), cost_bps=COST_BPS,
                                           freq=FREQ)["returns"].loc[start:]
                    return _c[key]

                # ---- the ladder (tuned param 2), every point recorded
                lad = []
                for g in LADDER:
                    r = run(g)
                    mi, mo, mf = (rel_margins(r, b_IS, "IS"), rel_margins(r, b_OOS, "OOS"),
                                  rel_margins(r, b_full, "full"))
                    m_is, m_full = metrics(win(r, "IS")), metrics(r)
                    lad.append(dict(k=k, draw=d, n=nb, g=g,
                                    IS_margin=mi["margin"], IS_pass=mi["margin"] > 0,
                                    IS_fails=mi["fails"], IS_Sharpe=m_is["Sharpe"],
                                    IS_CAGR=m_is["CAGR"], IS_MaxDD=m_is["MaxDD"],
                                    IS_vol=m_is["Vol"],
                                    OOS_margin=mo["margin"], OOS_pass=mo["margin"] > 0,
                                    OOS_fails=mo["fails"],
                                    full_margin=mf["margin"], full_pass=mf["margin"] > 0,
                                    CAGR=m_full["CAGR"], Sharpe=m_full["Sharpe"],
                                    MaxDD=m_full["MaxDD"]))
                lad_rows.extend(lad)
                L = pd.DataFrame(lad)

                # ---- the four gross-choice rules (tuned param 1), all IS-only, all <= 1.00
                v_is = metrics(run(GROSS0).loc[:IS_END])["Vol"]
                g_req = GROSS0 * vol_spy_is / v_is if v_is > 0 else np.nan
                g_ceil = min(g_req, CAP)
                order = L.sort_values(["IS_margin", "g"], ascending=[False, True])
                g_star = float(order.iloc[0].g)
                g_mid, iv_lo, iv_hi = midpoint_interval(
                    LADDER, list(L.IS_pass.values), g_star)
                mid_fb = not np.isfinite(g_mid)
                if mid_fb:
                    g_mid = g_star
                chosen = dict(STATIC=GROSS0, CEILING=g_ceil, MAXMARG=g_star, MIDPOINT=g_mid)

                for arm in ARMS:
                    g = float(min(chosen[arm], CAP))
                    r = run(g)
                    rets[(k, d, nb, arm)] = r
                    mi = rel_margins(r, b_IS, "IS")
                    mo = rel_margins(r, b_OOS, "OOS")
                    mf = rel_margins(r, b_full, "full")
                    m_full, m_oos, m_is = metrics(r), metrics(r.loc[OOS_START:]), \
                        metrics(r.loc[:IS_END])
                    h1, h2 = I78.half_sharpes(r)
                    f4b = I78.fail_4b(r, spy, r.loc[OOS_START:], spy_oos)
                    f4a = I78.fail_4a(r, base)
                    grid_rows.append(dict(
                        k=k, draw=d, n=nb, arm=arm, g=g, g_req=g_req,
                        at_cap=(abs(g - CAP) < 1e-9), mid_fallback=(arm == "MIDPOINT" and mid_fb),
                        iv_lo=iv_lo, iv_hi=iv_hi,
                        CAGR=m_full["CAGR"], Sharpe=m_full["Sharpe"], MaxDD=m_full["MaxDD"],
                        H1=h1, H2=h2, vol=m_full["Vol"],
                        Sharpe_IS=m_is["Sharpe"], CAGR_IS=m_is["CAGR"], MaxDD_IS=m_is["MaxDD"],
                        CAGR_OOS=m_oos["CAGR"], Sharpe_OOS=m_oos["Sharpe"],
                        MaxDD_OOS=m_oos["MaxDD"],
                        IS_margin=mi["margin"], IS_pass=mi["margin"] > 0, IS_fails=mi["fails"],
                        OOS_margin=mo["margin"], OOS_pass=mo["margin"] > 0,
                        OOS_fails=mo["fails"],
                        full_margin=mf["margin"], full_pass4b=(f4b == "-"), f4b=f4b,
                        pass4a=(f4a == "-"), f4a=f4a))
                choice_rows.append(dict(k=k, draw=d, n=nb, g_req=g_req, g_ceiling=g_ceil,
                                        g_maxmarg=g_star, g_midpoint=float(min(g_mid, CAP)),
                                        iv_lo=iv_lo, iv_hi=iv_hi, mid_fallback=mid_fb,
                                        IS_interval_empty=(not bool(L.IS_pass.any())),
                                        n_IS_passing=int(L.IS_pass.sum()),
                                        vol_IS_at_075=v_is))
        say(f"  k={k:<3} done  ({time.time() - t0:.0f}s)")

    G = pd.DataFrame(grid_rows)
    LAD = pd.DataFrame(lad_rows)
    CH = pd.DataFrame(choice_rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    LAD.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    CH.to_csv(OUT / f"{STEM}.choices.csv", index=False)
    say(f"\n  {len(LAD)} ladder rows (300 books x {len(LADDER)} g) and {len(G)} book-arm rows "
        f"written")

    # =============================================================== [a] reproduction, idea 78
    say("\n" + "=" * 200)
    say("[a] REPRODUCTION — the STATIC arm (g=0.75) vs idea 78's committed gridB.csv, 300 books")
    say("=" * 200)
    ref = pd.read_csv(OUT / "2026-09-05_candidate-count-vs-dispersion_B.gridB.csv")
    S = G[G.arm == "STATIC"].set_index(["k", "n", "draw"]).sort_index()
    R = ref.set_index(["k", "n", "draw"]).sort_index()
    ok_a = S.index.equals(R.index)
    say(f"    rows: this run {len(S)}, idea 78 {len(R)}; index identical: {ok_a}")
    common = S.index.intersection(R.index)
    S, R = S.loc[common], R.loc[common]
    for c in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "Sharpe_OOS"):
        dmax = float((S[c] - R[c]).abs().max())
        ok_a &= dmax < 1e-9
        say(f"    max|diff| {c:<11} = {dmax:.3e}")
    same = float((S["f4b"].astype(str) == R["f4b"].astype(str)).mean())
    ok_a &= same == 1.0
    say(f"    4b failing-bar string identical in {same:.1%} of the 300 books")
    say(f"[a] REPRODUCED EXACTLY: {ok_a}")

    # =============================================================== [b] idea 156's headline
    say("\n[b] PREMISE — idea 156: 55.0% of books need g > 1.00; k=20/n=20 4b pass 0.00 STATIC "
        "-> 0.12 CEILING")
    frac = float((CH.g_req > CAP).mean())
    p_static = float(G[(G.arm == "STATIC") & (G.k == 20) & (G.n == 20)].full_pass4b.mean())
    p_ceil = float(G[(G.arm == "CEILING") & (G.k == 20) & (G.n == 20)].full_pass4b.mean())
    say(f"    fraction of the 300 books with g_req > 1.00 : {frac:.1%}   (idea 156: 55.0%)")
    say(f"    k=20/n=20 full-sample 4b pass: STATIC {p_static:.2f}, CEILING {p_ceil:.2f}   "
        f"(idea 156: 0.00 -> 0.12)")
    ok_b = abs(frac - 0.550) < 0.005 and p_static == 0.0 and abs(p_ceil - 0.12) < 0.005
    say(f"[b] IDEA 156's HEADLINE REPRODUCED: {ok_b}")

    # =============================================================== what each rule chooses
    say("\n" + "=" * 200)
    say("WHAT EACH RULE CHOOSES — the gross itself, before any performance number")
    say("=" * 200)
    ch = G.groupby("arm").agg(g_mean=("g", "mean"), g_med=("g", "median"),
                              g_min=("g", "min"), g_max=("g", "max"),
                              at_cap=("at_cap", "mean")).reindex(ARMS)
    say(ch.to_string(float_format=lambda x: f"{x:.4f}"))
    say(f"    MIDPOINT fell back to MAXMARG (empty IS interval at the argmax) in "
        f"{float(CH.mid_fallback.mean()):.1%} of books; books with NO passing IS ladder point: "
        f"{float(CH.IS_interval_empty.mean()):.1%}")
    say(f"    Spearman(g_chosen, g_req): MAXMARG "
        f"{I78.spearman(CH.g_maxmarg, CH.g_req):+.3f}, MIDPOINT "
        f"{I78.spearman(CH.g_midpoint, CH.g_req):+.3f}, CEILING "
        f"{I78.spearman(CH.g_ceiling, CH.g_req):+.3f}")
    say("    per-cell mean chosen gross:")
    say(G.pivot_table(index=["k", "n"], columns="arm", values="g",
                      aggfunc="mean").reindex(columns=ARMS)
        .to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n    MAXMARG's chosen ladder point, distribution over the 300 books:")
    say(CH.g_maxmarg.value_counts().sort_index().to_string())

    # =============================================================== the horse race
    say("\n" + "=" * 200)
    say("THE HORSE RACE — 300 books, four gross-choice rules, PAIRED")
    say("=" * 200)
    race = G.groupby("arm").agg(
        n=("g", "size"),
        IS_pass=("IS_pass", "sum"), IS_margin=("IS_margin", "mean"),
        OOS_pass=("OOS_pass", "sum"), OOS_margin=("OOS_margin", "mean"),
        full_pass4b=("full_pass4b", "sum"), full_margin=("full_margin", "mean"),
        pass4a=("pass4a", "sum"),
        CAGR=("CAGR", "mean"), Sharpe=("Sharpe", "mean"), MaxDD=("MaxDD", "mean"),
        OOS_CAGR=("CAGR_OOS", "mean"), OOS_Sharpe=("Sharpe_OOS", "mean"),
        OOS_MaxDD=("MaxDD_OOS", "mean")).reindex(ARMS)
    say(race.to_string(float_format=lambda x: f"{x:.4f}"))
    say("  (IS_pass/OOS_pass/full_pass4b are COUNTS out of 300; the margins are the scale-free "
        "min-slack means.  IS is the window the rules were fitted on; OOS is the verdict.)")

    key = ["k", "n", "draw"]
    P = {a: G[G.arm == a].set_index(key).sort_index() for a in ARMS}
    say("\n  PAIRED differences vs CEILING (idea 148/156's clause) — the question as posed:")
    pr = []
    for a in ARMS:
        if a == "CEILING":
            continue
        j = P[a].join(P["CEILING"], rsuffix="_c")
        dm = j.OOS_margin - j.OOS_margin_c
        ds = j.Sharpe_OOS - j.Sharpe_OOS_c
        pr.append(dict(arm=a,
                       OOSpass_arm=int(j.OOS_pass.sum()), OOSpass_CEILING=int(j.OOS_pass_c.sum()),
                       win=int((j.OOS_pass & ~j.OOS_pass_c).sum()),
                       lose=int((~j.OOS_pass & j.OOS_pass_c).sum()),
                       d_OOS_margin=float(dm.mean()), t_margin=I78.tstat(dm),
                       d_OOS_Sharpe=float(ds.mean()), t_Sharpe=I78.tstat(ds),
                       d_OOS_CAGR=float((j.CAGR_OOS - j.CAGR_OOS_c).mean()),
                       d_OOS_MaxDD=float((j.MaxDD_OOS - j.MaxDD_OOS_c).mean()),
                       full4b_arm=int(j.full_pass4b.sum()),
                       full4b_CEILING=int(j.full_pass4b_c.sum())))
    PR = pd.DataFrame(pr)
    say(PR.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("  win/lose = books where the arm passes the OOS-window 4b and CEILING does not, and "
        "vice versa.  t is a paired daily-free t over the 300 books (independence across draws "
        "is NOT claimed — the sub-panels overlap; the t is a magnitude cue only).")

    say("\n  per-cell OOS-window 4b pass rate (the verdict window):")
    say(G.pivot_table(index=["k", "n"], columns="arm", values="OOS_pass",
                      aggfunc="mean").reindex(columns=ARMS)
        .to_string(float_format=lambda x: f"{x:.2f}"))
    say("\n  per-cell FULL-sample 4b pass rate (PROTOCOL's own reading, idea 156's table):")
    cells = G.pivot_table(index=["k", "n"], columns="arm", values="full_pass4b",
                          aggfunc="mean").reindex(columns=ARMS)
    say(cells.to_string(float_format=lambda x: f"{x:.2f}"))
    cells.to_csv(OUT / f"{STEM}.cells.csv")
    say("\n  per-cell mean OOS margin:")
    say(G.pivot_table(index=["k", "n"], columns="arm", values="OOS_margin",
                      aggfunc="mean").reindex(columns=ARMS)
        .to_string(float_format=lambda x: f"{x:.3f}"))

    say("\n  4b failing-bar census on the OOS window (a book can fail several bars):")
    cen = []
    for a in ARMS:
        A = G[G.arm == a]
        row = dict(arm=a, n=len(A), OOS_pass=int(A.OOS_pass.sum()))
        for bar in ("H1", "H2", "OOS", "DD", "CAGR"):
            row[bar] = int(A.OOS_fails.astype(str).str.split(",").apply(
                lambda v: bar in v).sum())
        cen.append(row)
    say(pd.DataFrame(cen).to_string(index=False))

    # =============================================================== ladder oracle control
    say("\n" + "=" * 200)
    say("ORACLE CONTROL — the best ladder point chosen ON THE OOS WINDOW (not implementable)")
    say("=" * 200)
    orc = LAD.groupby(key)[["OOS_pass"]].max()
    say(f"  books with at least ONE ladder point passing the OOS-window 4b: "
        f"{int(orc.OOS_pass.sum())} of 300 ({float(orc.OOS_pass.mean()):.1%})")
    say(f"  books with at least one ladder point passing the FULL-sample 4b: "
        f"{int(LAD.groupby(key)['full_pass'].max().sum())} of 300")
    say("  Reading: the oracle is the ceiling on what ANY gross-choice rule can reach.  If every "
        "implementable rule sits far below it, the choice of g is not the binding problem.")
    say("\n  ladder-point 4b pass rates (all 10 points, both windows, all 300 books):")
    say(LAD.groupby("g").agg(IS_pass=("IS_pass", "mean"), OOS_pass=("OOS_pass", "mean"),
                             full_pass=("full_pass", "mean"),
                             OOS_margin=("OOS_margin", "mean"),
                             Sharpe=("Sharpe", "mean"), MaxDD=("MaxDD", "mean"),
                             CAGR=("CAGR", "mean")).to_string(
        float_format=lambda x: f"{x:.4f}"))
    say("\n  the small-pool cell k=20/n=20 alone, ladder point by ladder point:")
    say(LAD[(LAD.k == 20) & (LAD.n == 20)].groupby("g").agg(
        IS_pass=("IS_pass", "mean"), OOS_pass=("OOS_pass", "mean"),
        full_pass=("full_pass", "mean"), full_margin=("full_margin", "mean"),
        CAGR=("CAGR", "mean"), MaxDD=("MaxDD", "mean")).to_string(
        float_format=lambda x: f"{x:.4f}"))

    # =============================================================== rule 8 walk-forward
    say("\n" + "=" * 200)
    say(f"RULE 8 WALK-FORWARD — everything chosen on <= {IS_END}, read ONCE on {OOS_START} ->")
    say("S1 = IS-Sharpe argmax over the 150 books.  S2 = 4b-aware IS screen then IS-Sharpe "
        "argmax (S1 fallback).  S0 = do-nothing full-B136 control at the same gross rule.")
    say("=" * 200)
    spy_o, v1_o = metrics(spy_oos), metrics(base.loc[OOS_START:])
    bIS = dict(s1=b_IS["s1"], s2=b_IS["s2"], dd=b_IS["sdd"], cagr=b_IS["scagr"])

    def is_adm(row):
        h1, h2 = I78.half_sharpes(rets[(row.k, row.draw, row.n, row.arm)].loc[:IS_END])
        return (h1 > bIS["s1"] and h2 > bIS["s2"]
                and abs(row.MaxDD_IS) <= DELTA * abs(bIS["dd"])
                and row.CAGR_IS >= PHI * bIS["cagr"])

    # the S0 control needs the full-B136 book at each arm's own gross
    _e136 = I78.eligible_mask(px136, tr136)
    _s136 = I78.score(px136, vol_scale=False)[0].where(_e136).rank(axis=1, ascending=False)
    SEL136 = {nb: (_s136 <= nb).astype(float) for nb in N_BOOKS}
    c136 = {}

    def run136(nb, g):
        key = (nb, round(float(g), 6))
        if key not in c136:
            c136[key] = backtest(px136, SEL136[nb] * (key[1] / nb), cost_bps=COST_BPS,
                                 freq=FREQ)["returns"].loc[start:]
        return c136[key]

    wf = []
    for arm in ARMS:
        A = G[G.arm == arm].copy()
        A["IS_adm"] = A.apply(is_adm, axis=1)
        for nb in N_BOOKS:
            sub = A[A.n == nb]
            # S0: the same gross RULE applied to the full B136 book, IS-only
            r075 = run136(nb, GROSS0)
            if arm == "STATIC":
                g0 = GROSS0
            elif arm == "CEILING":
                g0 = min(GROSS0 * vol_spy_is / metrics(r075.loc[:IS_END])["Vol"], CAP)
            else:
                lad0 = [(g, rel_margins(run136(nb, g), b_IS, "IS")["margin"]) for g in LADDER]
                gs0 = max(lad0, key=lambda z: (z[1], -z[0]))[0]
                if arm == "MAXMARG":
                    g0 = gs0
                else:
                    gm, _, _ = midpoint_interval(LADDER, [m > 0 for _, m in lad0], gs0)
                    g0 = gs0 if not np.isfinite(gm) else min(gm, CAP)
            picks = [("S0 do-nothing (full B136)", None, run136(nb, g0), g0)]
            s1 = sub.sort_values(["Sharpe_IS", "k"], ascending=[False, True]).iloc[0]
            picks.append(("S1 IS-Sharpe argmax", s1, rets[(s1.k, s1.draw, nb, arm)], s1.g))
            adm = sub[sub.IS_adm]
            s2 = (adm.sort_values(["Sharpe_IS", "k"], ascending=[False, True]).iloc[0]
                  if len(adm) else s1)
            picks.append((f"S2 4b-aware IS screen ({len(adm)} adm)", s2,
                          rets[(s2.k, s2.draw, nb, arm)], s2.g))
            for lbl, row, r, gg in picks:
                ro = r.loc[OOS_START:]
                mo = metrics(ro)
                f4b = I78.fail_4b(r, spy, ro, spy_oos)
                f4a = I78.fail_4a(r, base)
                mo_rel = rel_margins(r, b_OOS, "OOS")
                wf.append(dict(arm=arm, n=nb, selector=lbl, g=float(gg),
                               k=(int(row.k) if row is not None else -1),
                               draw=(int(row.draw) if row is not None else -1),
                               IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                               OOS_MaxDD=mo["MaxDD"], OOS_margin=mo_rel["margin"],
                               OOS_fails=mo_rel["fails"],
                               v1_OOS_CAGR=v1_o["CAGR"], v1_OOS_Sharpe=v1_o["Sharpe"],
                               v1_OOS_MaxDD=v1_o["MaxDD"],
                               spy_OOS_CAGR=spy_o["CAGR"], spy_OOS_Sharpe=spy_o["Sharpe"],
                               spy_OOS_MaxDD=spy_o["MaxDD"],
                               d_vs_v1=mo["Sharpe"] - v1_o["Sharpe"],
                               d_vs_spy=mo["Sharpe"] - spy_o["Sharpe"],
                               f4a=f4a, f4b=f4b, pass4b=(f4b == "-"), pass4a=(f4a == "-")))
                say(f"  {arm:<9} n={nb:<3} {lbl:<34} g={gg:.3f} k={wf[-1]['k']:<3} -> OOS "
                    f"{mo['CAGR']:.2%}/{mo['Sharpe']:.3f}/{mo['MaxDD']:.2%} | dSharpe vs v1 "
                    f"{mo['Sharpe'] - v1_o['Sharpe']:+.3f}, vs SPY "
                    f"{mo['Sharpe'] - spy_o['Sharpe']:+.3f} | full 4b {f4b}")
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(f"\n  SPY OOS               {spy_o['CAGR']:.2%}/{spy_o['Sharpe']:.3f}/"
        f"{spy_o['MaxDD']:.2%}")
    say(f"  RULES v1 OOS on B136  {v1_o['CAGR']:.2%}/{v1_o['Sharpe']:.3f}/{v1_o['MaxDD']:.2%}")
    say("\n  mean OOS Sharpe by gross rule across the 6 (selector x n) walk-forward picks:")
    say(WF.groupby("arm").agg(OOS_Sharpe=("OOS_Sharpe", "mean"),
                              OOS_CAGR=("OOS_CAGR", "mean"),
                              OOS_MaxDD=("OOS_MaxDD", "mean"),
                              pass4b=("pass4b", "sum"), pass4a=("pass4a", "sum"),
                              g=("g", "mean")).reindex(ARMS)
        .to_string(float_format=lambda x: f"{x:.4f}"))

    # =============================================================== census
    say("\n" + "=" * 200)
    say("CENSUS")
    say("=" * 200)
    say(f"  ladder rows {len(LAD)};  book-arm rows {len(G)};  walk-forward picks {len(WF)}")
    say(f"  book-arm 4a passes {int(G.pass4a.sum())};  full-sample 4b passes "
        f"{int(G.full_pass4b.sum())};  OOS-window 4b passes {int(G.OOS_pass.sum())}")
    say(f"  every g used is <= 1.00 (PROTOCOL rule 2): {bool((G.g <= CAP + 1e-12).all())}")
    say(f"  runtime {time.time() - t0:.0f}s")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")
    print(f"\nwrote {STEM}.console.txt/.grid.csv/.ladder.csv/.choices.csv/.walkforward.csv/"
          f".cells.csv")


if __name__ == "__main__":
    main()
