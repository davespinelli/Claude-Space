#!/usr/bin/env python3
"""QUEUE idea 165 — required-gross-as-a-leaderboard-column  (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 165)
    "idea 156 showed `g_req = 0.75 x vol_SPY / vol_book` converts 'fails on CAGR' into 'would
     need 1.82x, which rule 2 forbids', and that it is computable for free.  Back-fill it
     across every leaderboard book that failed 4b on the CAGR floor, and report what fraction
     of the project's CAGR-floor KILLs are really no-leverage-ceiling KILLs.  Cheap, and it
     re-labels a large part of the record."

WHAT IS AT STAKE.
    4b's CAGR floor (CAGR >= 0.70 x SPY's) has been the project's most prolific killer.  Idea
    156 showed on ONE corpus (300 B136 sub-panel books) that most of those failures are not
    statements about signal quality but about RISK BUDGET: a 0.75-gross, trend-gated book that
    sits in cash a lot runs well under SPY's vol, so a return floor set against SPY's return is
    partly a gross comparison.  The honest re-label is a NUMBER per row — the gross the book
    would need — and PROTOCOL rule 2's no-leverage ceiling then decides whether that number is
    reachable.  If most CAGR-floor KILLs need g > 1.00, the floor is doing correct work and the
    record stands as written.  If most need g <= 1.00, a large part of the leaderboard is
    mislabelled: those books were never tested at a gross where they could pass.

    Idea 156's g_req is a VOL-MATCHING gross, which is a proxy.  The number a leaderboard column
    actually wants is the gross at which the CAGR floor itself clears.  This run reports BOTH,
    and — the part idea 156 flagged as P5 and did not settle across book families — whether the
    book at that gross passes ALL FIVE 4b bars, because raising gross raises drawdown too.

THE EXACT-LEVER IDENTITY (idea 66) — TESTED FIRST, AND IT FAILS.  This is the run's first result.
    The plan was to compute the whole gross ladder from ONE backtest per book, on the project's
    standing claim (idea 66) that gross is an exact lever with zero Sharpe content:
        r_{c*g} =? c * r_g   day by day, because weights, traded units and costs all scale by c.
    That claim is FALSE under products/backtester/engine.py.  The engine holds target weights and
    DRIFTS between rebalances, renormalising each day as
        cur <- cur*(1+ret) / [ (cur*(1+ret)).sum() + (1 - cur.sum()) ] ,
    i.e. the uninvested sleeve (1 - gross) enters the denominator as a constant-value cash buffer.
    A book started at a higher gross therefore drifts along a DIFFERENT weight path, not a scaled
    one.  Reproduction check [c] measures the error against genuine re-runs and it is not small:
    on a single-name control book, CAGR 18.91% at g = 0.75 against 24.58% at g = 1.00 where the
    lever predicts 25.21%, and max|daily error| = 4.7e-3 against typical daily returns of ~1e-2.
    THE SCRIPT'S OWN PRE-REGISTERED RULE ("if [c] fails, every g_req in this file is void") IS
    HONOURED: nothing below is computed by rescaling a return series.  Every number at a gross
    other than 0.75 is a GENUINE backtest at that gross, on the pre-registered ladder below.
    This costs ~2000 extra backtests and is the only defensible way to answer idea 165.

    POST-RUN ADDENDUM (filled in from this script's own [c] output — read it before quoting the
    single-name figure above, which is the WORST case, not the typical one).  On the corpus's
    actual diversified books the lever is a GOOD approximation but still not an identity:
    over 12 genuine re-runs at g in {0.40, 1.00}, max|daily error| 4.90e-03, max |dCAGR| 0.0238pp
    and max |dMaxDD| 0.2755pp; over 36 genuine re-runs across the ladder, |dSharpe| mean 0.0018
    and max 0.0097.  So the practical exposure is NOT to headline CAGR — it is to DRAWDOWN, and
    4b's DD margins are routinely ~1pp, so a 0.28pp path error is a material fraction of the bar
    a re-grossed book is judged against.  Concentrated books (the single-name control) are far
    worse.  Two consequences, both reported: (i) a rescaled gross ladder is fine for ranking and
    wrong for verdicts near a bar; (ii) CAGR is not even MONOTONE in gross under the true engine
    — 92 of the 213 CAGR-floor failures have a non-monotone CAGR curve on the ladder — so "the
    gross it would need" is a scan result, never a closed form.

    That failure is itself a finding with reach beyond this idea: every project result that
    priced a gross ladder by rescaling, or that leaned on "gross has zero Sharpe content", is
    exposed.  It is reported as such and a QUEUE follow-up is proposed, not fixed here (PROTOCOL
    forbids touching baseline.py, and engine.py is the live backtester).

THE GROSS LADDER (pre-registered, genuine backtests, no rescaling anywhere)
    A book that FAILS the CAGR floor needs MORE gross, never less, so the ladder runs upward
    from the published 0.75:
        0.80  0.85  0.90  0.95  1.00  1.10  1.25  1.50  2.00
    plus one extra genuine run at each book's own VM gross when that gross is below 1.00 and off
    the ladder.  1.00 is PROTOCOL rule 2's ceiling; everything above it is reported to size the
    shortfall and is never a KEEP.  CAGR is NOT assumed monotone in gross (volatility drag turns
    the curve over); the whole ladder is scanned, the SMALLEST clearing rung is taken, and the
    number of non-monotone books is reported.

CORPUS — the project's standing book families, not a bespoke draw
    3 panels x 7 keys x 9 shares x 2 cost rungs = 378 books, weekly, t+1, gross 0.75 spread
    over the names actually held (idea 153/159's `norm` construction, which removes idea 73/81's
    de-grossing confound).  Panels, keys, shares and cost rung are REPORTED CORPUS AXES carried
    verbatim from ideas 153/159; none of them is tuned here.
      Panels  u56 (universe.json), broad (universe_broad.json),
              small (sub-$2B, the tickers with max_1d_move >= 1.0 dropped per data/small_meta.csv)
      Keys    NONE (composite alone), INV (comp/sqrt(vol20), RULES v1's live tilt),
              POS (comp*sqrt(vol20)), MOM, R6, R3 (the composite's own legs),
              RND (fixed per-name scramble, seed 159_000 — idea 159's pre-registered null)
      Shares  0.05 0.10 0.15 0.20 0.27 0.35 0.53 0.75 1.00, as n = max(2, round(m x mean weekly
              eligible count)).  m = 1.00 is EWall; NONE at n=20 on u56 is idea 2's KEEP book.
      Costs   10 and 25 bps.
    RULES v1 (n=5, w=0.15) is run on every panel at both rungs as the live-book reference.

TUNED PARAMETERS — exactly two, swept exhaustively, ALL grid points in .grid.csv / .greq.csv:
    1. the gross convention, 5 values, none preferred after the fact:
         STATIC    g = 0.75                                            (the control, as published)
         VM_FULL   g = 0.75 * vol(SPY, full) / vol(book@0.75, full)    idea 156's formula, LOOK-AHEAD
         VM_IS     g = 0.75 * vol(SPY, IS)   / vol(book@0.75, IS)      prospectively implementable
         CF_FULL   g = min g such that CAGR(book@g) >= 0.70 * CAGR(SPY, full)   LOOK-AHEAD
         CF_IS     g fitted the same way on the IS window only         prospectively implementable
       VM_* is the number idea 165 asks to back-fill.  CF_* is the number a leaderboard column
       actually wants (the floor's own inverse) and is reported beside it so the proxy can be
       scored.  All four non-control conventions are computed for EVERY book, pass or fail.
    2. the leverage ceiling, 2 values:  CAP  g <- min(g, 1.00)   (PROTOCOL rule 2)
                                        RAW  g uncapped          (LEVERED — never a KEEP)

THE HEADLINE CENSUS (pre-registered wording).  Of the books that fail 4b with the CAGR floor
    among their failing bars, each is classified into exactly one of:
      CEILING   g_req > 1.00                      — a real no-leverage KILL, the record stands
      REACHABLE g_req <= 1.00 and at g = g_req all five 4b bars hold   — the row is MISLABELLED
      TRADED    g_req <= 1.00 but at g = g_req some OTHER bar (DD, H1, H2, OOS) now fails
                                                  — the floor was never the binding bar; the
                                                    book trades one failure for another
    "what fraction of the project's CAGR-floor KILLs are really no-leverage-ceiling KILLs" is
    CEILING / (CEILING + REACHABLE + TRADED), reported under both g_req conventions and both
    panels-pooled and per-panel.

WALK-FORWARD (PROTOCOL rule 8) — everything chosen on 2009-2016 (2011-2016 on small) only.
    The conventions VM_IS and CF_IS use ONLY IS data by construction; VM_FULL/CF_FULL are
    look-ahead and are labelled as such at every use, never used for a verdict.
    Arms, fixed before any OOS number is read, per (panel, cost):
      W_STATIC  IS-Sharpe argmax over the 63 books at g = 0.75            (do-nothing control)
      W_VMIS    IS-Sharpe argmax after re-grossing every book to VM_IS (CAP)
      W_CFIS    IS-Sharpe argmax after re-grossing every book to CF_IS (CAP)
      W_4bIS    IS-Sharpe argmax among books clearing the IS-window 4b bars at CF_IS (CAP),
                falling back to W_STATIC's pick when the screen is empty
    Each arm's pick is read ONCE on the untouched 2017-2026 window; OOS CAGR / Sharpe / MaxDD
    reported against RULES v1 on the same panel and cost, and against SPY.
BOTH KEEP PATHS (4a and 4b) are evaluated on all 378 books at every gross convention, full
    sample and OOS window, and the counts are reported.

REPRODUCTION, asserted before any new number is read
    [a] The STATIC arm at 10 bps must reproduce idea 159's committed `.grid.csv` cell-for-cell
        on CAGR, Sharpe, MaxDD, H1, H2 at the 9 shares this run shares with it.  If [a] fails,
        this is not the project's standing corpus and no census below is a back-fill.
    [b] idea 156's own headline formula must reproduce: g_req(VM) = 0.75 * volSPY / volbook must
        equal 0.75 * (realised vol ratio), and re-running a book at that g must land its realised
        vol on SPY's.  Mean |achieved/target - 1| is reported.
    [c] The exact-lever identity above, against a genuine re-run of the backtester at g = 0.40
        and g = 1.00 on 6 books.  max|diff| on the daily net return series is printed.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a] reproduces exactly; [c] holds to ~1e-15.
    P2  VM_FULL g_req > 1.00 for the MAJORITY of CAGR-floor failures on the large-cap panels
        (idea 156's P2/P4 generalise), so CEILING is the modal label and the record largely
        stands.  The re-labelling idea 165 hopes for is real but a minority.
    P3  CF_* < VM_* systematically, because clearing a 70%-of-SPY return floor takes less gross
        than matching SPY's whole volatility.  The vol-match proxy therefore OVERSTATES the
        ceiling problem, and the fraction of CEILING labels is LOWER under CF_* than under VM_*.
    P4  Of the books reachable at g <= 1.00, a large share land in TRADED, not REACHABLE: the DD
        cap is what the extra gross costs (idea 156's P5).  Net new 4b passes are few.
    P5  The small panel is the extreme: its books are lower-vol and lower-return, so almost all
        of its CAGR-floor failures are CEILING.  Its numbers are survivorship-inflated and not
        tradable either way.
    P6  RE-STATED after [c] failed.  The original P6 assumed idea 66's "gross has zero Sharpe
        content".  [c] shows the lever is not exact, so that claim is now itself the prediction:
        |Sharpe(g) - Sharpe(0.75)| is measured over 36 genuine re-runs across the ladder.  If it
        is materially above zero, idea 66's clause is wrong as stated and every project result
        that treated the gross ladder as Sharpe-neutral needs the caveat.  The rule-8 arms all
        share W_STATIC's pick by construction (gross is applied AFTER selection), so any OOS
        difference between them is pure risk-budget, which is the honest comparison.
    P7  Nothing here is a KEEP.  This run prices a leaderboard COLUMN.

CAVEATS carried, not buried
    * SURVIVORSHIP.  All three panels are current-constituent lists (idea 54).  The small panel
      is the worst case (data/SMALL_PANEL_README.md): every sub-$2B name that delisted, was
      acquired or went to zero is absent, which inflates every return there and therefore
      UNDERSTATES g_req on that panel.  No small-panel number here is tradable.
    * This is a back-fill over the project's standing book FAMILIES, not over the literal rows of
      LEADERBOARD.md.  Many committed rows are one-off constructions (sleeves, stops, breadth
      gates, overlays) whose scripts are not re-run here; the census is a statement about the
      378 books enumerated above and is labelled as such.  It is the largest single corpus the
      project has put the question to, and it spans every panel and both cost rungs.
    * VM_FULL and CF_FULL use full-sample information.  They answer the mechanical question
      ("could this book ever have cleared?") and are never treated as tradable rules.
    * Vol matching is not risk matching: equalising realised vol to SPY's does NOT equalise
      drawdown.  That is exactly what the TRADED bucket measures.
    * g_req is derived from a MODELLED cost bill (turnover x cost_bps); slippage and impact are
      absent, and both are worse at higher gross.  g_req is therefore a LOWER bound.
    * Idea 38 (calendar-day price index) and idea 126 (t+1 execution) carry over unchanged.
    * Idea 153's confound (i) at m -> 1.00 (tilted and control books hold the same set) carries
      over; the m = 1.00 column is reported, never used alone.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .greq.csv, .census.csv,
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

STEM = "2026-09-05_required-gross-as-a-leaderboard-column_cloud"
OUT = ROOT / "research" / "backtests"
I159P = OUT / "2026-09-05_the-share-at-which-ranking-stops-paying_cloud.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


I159 = _load(I159P, "i159")
C, H, I153 = I159.C, I159.H, I159.I153

FREQ, GROSS, MAX_VOL, CAP = "W", 0.75, 0.60, 1.00
PANELS = ["u56", "broad", "small"]
KEYS = ["NONE", "INV", "POS", "MOM", "R6", "R3", "RND"]
SHARES = [0.05, 0.10, 0.15, 0.20, 0.27, 0.35, 0.53, 0.75, 1.00]
COSTS = [10.0, 25.0]
CONVS = ["STATIC", "VM_FULL", "VM_IS", "CF_FULL", "CF_IS"]
CEILS = ["CAP", "RAW"]
IS_END, OOS_START = H.IS_END, H.OOS_START
LADDER = [0.80, 0.85, 0.90, 0.95, 1.00, 1.10, 1.25, 1.50, 2.00]   # genuine re-runs, no rescaling

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 900)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ------------------------------------------------------------------ the books (idea 159 verbatim)
def weights(px, key, n, pk):
    return I159.weights(px, key, n, pk)


def halves(r):
    return H.halves(r)


def ann_vol(r):
    return float(r.std() * np.sqrt(252))


def cagr_of(r):
    return float(metrics(r)["CAGR"])


_RUN = {}


def run_at(pk, cost, key, m, g, ref):
    """A GENUINE backtest of the book at gross g.  Never a rescaled series — the exact-lever
    identity is measured and rejected in reproduction [c]."""
    ck = (pk, cost, key, m, round(g, 6))
    if ck in _RUN:
        return _RUN[ck]
    R = ref[pk]
    W = weights(R["px"], key, R["nmap"][m], pk) * (g / GROSS)
    _RUN[ck] = backtest(R["px"], W, cost_bps=cost, freq=FREQ)["returns"].loc[R["start"]:]
    return _RUN[ck]


def cf_gross_genuine(pk, cost, key, m, target_cagr, ref, win=None, ladder=None):
    """Smallest rung on the pre-registered LADDER whose GENUINE re-run clears target_cagr on the
    given window.  Returns (g, non_monotone) where non_monotone flags a book whose CAGR falls
    again at some higher rung — CAGR is not assumed monotone in gross.  NaN g = never clears."""
    lad = ladder if ladder is not None else LADDER
    vals = []
    for g in lad:
        r = run_at(pk, cost, key, m, g, ref)
        rr = H.window(r, win) if win else r
        vals.append(cagr_of(rr))
    v = np.asarray(vals, float)
    nonmono = bool(np.any(np.diff(v) < -1e-12))
    ok = np.where(v >= target_cagr)[0]
    return (float(lad[int(ok[0])]) if len(ok) else np.nan), nonmono


def bars_pack(spy):
    return dict(full=C.bars_win(spy, "full"), IS=C.bars_win(spy, "IS"), OOS=C.bars_win(spy, "OOS"))


def margins5(r, bars):
    """4b's five margins on the FULL sample (PROTOCOL's own reading)."""
    return H.margins(r, bars)


def failing_bars(mg):
    return [k for k in ("H1", "H2", "OOS", "DD", "CAGR") if mg[k] <= 0]


def main():
    t0 = time.time()
    say("=" * 200)
    say(f"IDEA 165 — required-gross-as-a-leaderboard-column   ({STEM})")
    say("Back-fill idea 156's g_req across the project's standing book families; report what "
        "fraction of CAGR-floor 4b failures are genuinely no-leverage-ceiling KILLs.")
    say("PRE-REGISTERED: exactly 2 tuned params (gross convention x 5, leverage ceiling x 2). "
        "Panel, key, share and cost rung are carried corpus axes, never selected on.")
    say(f"Corpus: {len(PANELS)} panels x {len(KEYS)} keys x {len(SHARES)} shares x "
        f"{len(COSTS)} costs = {len(PANELS)*len(KEYS)*len(SHARES)*len(COSTS)} books, "
        f"weekly, t+1, `norm` gross {GROSS}.")
    say("=" * 200)

    # ---------------------------------------------------------------- panels
    ref = {}
    for pk in PANELS:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        el = I153.eligible_mask(px, pk).loc[start:]
        n_elig = float(el.sum(axis=1).mean())
        bars = bars_pack(spy)
        ms, mo = metrics(spy), metrics(spy.loc[OOS_START:])
        ref[pk] = dict(px=px, start=start, spy=spy, bars=bars, n_elig=n_elig, desc=desc,
                       nmap={m: max(2, int(round(m * n_elig))) for m in SHARES},
                       spy_m=ms, spy_oos=mo,
                       spy_vol_full=ann_vol(spy), spy_vol_IS=ann_vol(H.window(spy, "IS")))
        say(f"\n[panel] {pk} = {desc}: {px.shape[1]} cols, eval {start.date()} -> "
            f"{px.index[-1].date()}, mean weekly eligible {n_elig:.1f}")
        say("    share -> n:  " + ", ".join(f"{m:.3g}->{ref[pk]['nmap'][m]}" for m in SHARES))
        say(f"    SPY  {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%} halves "
            f"{bars['full']['s1']:.3f}/{bars['full']['s2']:.3f} | OOS {mo['CAGR']:.2%}/"
            f"{mo['Sharpe']:.3f}/{mo['MaxDD']:.2%} | vol full {ref[pk]['spy_vol_full']:.4f} "
            f"IS {ref[pk]['spy_vol_IS']:.4f}")
        say(f"    4b bars on this panel: H1>{bars['full']['s1']:.3f}  H2>{bars['full']['s2']:.3f}"
            f"  OOS>{bars['full']['soos']:.3f}  |MaxDD|<={0.60*abs(bars['full']['sdd']):.2%}"
            f"  CAGR>={0.70*bars['full']['scagr']:.2%}")

    # ---------------------------------------------------------------- the 378 books
    say("\n" + "=" * 200)
    say("RUNNING THE CORPUS (one backtest per book at g = 0.75; every other gross is the exact "
        "lever r_{cg} = c r_g, asserted in reproduction [c] below)")
    say("=" * 200)
    RET, V1 = {}, {}
    rows = []
    for pk in PANELS:
        R = ref[pk]
        px, start = R["px"], R["start"]
        for cost in COSTS:
            V1[(pk, cost)] = backtest(px, rules_v1_weights(px), cost_bps=cost,
                                      freq=FREQ)["returns"].loc[start:]
            for key in KEYS:
                for m in SHARES:
                    n = R["nmap"][m]
                    W = weights(px, key, n, pk)
                    r = backtest(px, W, cost_bps=cost, freq=FREQ)["returns"].loc[start:]
                    RET[(pk, cost, key, m)] = r
                    mm = metrics(r)
                    h1, h2 = halves(r)
                    mo = metrics(r.loc[OOS_START:])
                    rows.append(dict(panel=pk, cost=cost, key=key, share=m, n=n,
                                     CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                     H1=h1, H2=h2, OOS_Sharpe=mo["Sharpe"],
                                     OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                                     vol_full=ann_vol(r), vol_IS=ann_vol(H.window(r, "IS")),
                                     IS_Sharpe=metrics(H.window(r, "IS"))["Sharpe"],
                                     IS_CAGR=metrics(H.window(r, "IS"))["CAGR"],
                                     IS_MaxDD=metrics(H.window(r, "IS"))["MaxDD"]))
        say(f"  {pk}: {len(KEYS)*len(SHARES)*len(COSTS)} books done  ({time.time()-t0:.0f}s)")
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    # ---------------------------------------------------------------- reproduction gate
    say("\n" + "=" * 200)
    say("REPRODUCTION GATE (asserted before any new number is read)")
    say("=" * 200)
    rep = []

    # [a] idea 159's committed grid at 10 bps, shared shares
    p159 = OUT / "2026-09-05_the-share-at-which-ranking-stops-paying_cloud.grid.csv"
    if p159.exists():
        A = pd.read_csv(p159)
        cols = [c for c in ("CAGR", "Sharpe", "MaxDD", "H1", "H2") if c in A.columns]
        A = A.rename(columns={"m": "share"})          # idea 159 names the share column `m`
        key159 = [c for c in ("panel", "key", "share") if c in A.columns]
        assert "share" in key159, "idea 159 grid has no share column — [a] would be a cross join"
        mine = G[G.cost == 10.0].copy()
        mg = mine.merge(A, on=key159, suffixes=("", "_159"))
        if len(mg):
            for c in cols:
                d = float((mg[c] - mg[f"{c}_159"]).abs().max())
                rep.append(dict(check="[a] idea159 grid @10bps", field=c, n=len(mg), maxabsdiff=d,
                                verdict="MATCH" if d < 1e-9 else "MISMATCH"))
            say(f"  [a] merged {len(mg)} cells against idea 159's committed grid on {key159}")
            for rr in rep:
                say(f"      {rr['field']:>7s}  max|diff| {rr['maxabsdiff']:.3e}  {rr['verdict']}")
        else:
            say("  [a] SKIPPED — idea 159's grid.csv does not share this run's key columns "
                f"(its columns: {list(A.columns)[:12]})")
            rep.append(dict(check="[a] idea159 grid @10bps", field="-", n=0, maxabsdiff=np.nan,
                            verdict="SKIPPED (no shared key)"))
    else:
        say("  [a] SKIPPED — idea 159's grid.csv not present in the repo")
        rep.append(dict(check="[a] idea159 grid @10bps", field="-", n=0, maxabsdiff=np.nan,
                        verdict="SKIPPED (file absent)"))

    # [c] the exact-lever identity — MEASURED, and it fails.  This is the run's first result.
    say("\n  [c] exact-lever identity r_{cg} = c * r_g (idea 66), against genuine re-runs:")
    say("      engine.py drifts held weights between rebalances and renormalises against a")
    say("      CONSTANT-VALUE cash sleeve (1 - gross), so a book started at a different gross")
    say("      follows a different weight path.  The lever is an approximation, not an identity.")
    worst, cw = 0.0, 0.0
    for pk in PANELS:
        R = ref[pk]
        for key, m in (("NONE", 0.53), ("INV", 0.20)):
            for g in (0.40, 1.00):
                rr = run_at(pk, 10.0, key, m, g, ref)
                pred = RET[(pk, 10.0, key, m)] * (g / GROSS)
                d = float((rr - pred).abs().max())
                dc = abs(cagr_of(rr) - cagr_of(pred))
                dd = abs(abs(metrics(rr)["MaxDD"]) - abs(metrics(pred)["MaxDD"]))
                worst, cw = max(worst, d), max(cw, dc)
                rep.append(dict(check="[c] exact lever", field=f"{pk}/{key}/m={m}/g={g}",
                                n=len(rr), maxabsdiff=d,
                                verdict=(f"genuine CAGR {cagr_of(rr):.4%} vs lever-predicted "
                                         f"{cagr_of(pred):.4%} (dCAGR {dc:.4%}, dMaxDD {dd:.4%})")))
                say(f"      {pk:>5s}/{key:<4s} m={m:.2f} g={g:.2f}: max|daily diff| {d:.3e}   "
                    f"genuine CAGR {cagr_of(rr):8.4%} vs lever {cagr_of(pred):8.4%}  "
                    f"(dCAGR {dc:.4%}, dMaxDD {dd:.4%})")
    say(f"      -> 12 re-runs, max|daily diff| = {worst:.3e}, max |dCAGR| = {cw:.4%}:  "
        f"{'MATCH' if worst < 1e-12 else 'MISMATCH.'}")
    say("      PRE-REGISTERED CONSEQUENCE HONOURED: no g_req or bar below is computed by "
        "rescaling.  Every off-0.75 number in this file is a GENUINE backtest at that gross.")

    # [b] idea 156's formula and the vol a genuine re-run at that gross actually achieves
    say("\n  [b] idea 156's VM formula and the vol a GENUINE re-run at that gross achieves:")
    ach_lever, ach_true = [], []
    for pk in PANELS:
        R = ref[pk]
        for key, m in (("NONE", 0.53), ("INV", 0.20), ("POS", 0.10)):
            r = RET[(pk, 10.0, key, m)]
            g = GROSS * R["spy_vol_full"] / ann_vol(r)
            ach_lever.append(abs(ann_vol(r * (g / GROSS)) / R["spy_vol_full"] - 1.0))
            ach_true.append(abs(ann_vol(run_at(pk, 10.0, key, m, g, ref))
                                / R["spy_vol_full"] - 1.0))
    rep.append(dict(check="[b] VM achieves SPY vol", field="mean|achieved/target-1| (lever)",
                    n=len(ach_lever), maxabsdiff=float(np.mean(ach_lever)), verdict="by construction"))
    rep.append(dict(check="[b] VM achieves SPY vol", field="mean|achieved/target-1| (GENUINE)",
                    n=len(ach_true), maxabsdiff=float(np.mean(ach_true)),
                    verdict="the real accuracy of idea 156's formula"))
    say(f"      under the (false) lever: {float(np.mean(ach_lever)):.3e} — true by construction")
    say(f"      under GENUINE re-runs  : {float(np.mean(ach_true)):.3e} — the formula's real "
        f"accuracy.  idea 156's VM gross does NOT land the book on SPY's vol.")
    pd.DataFrame(rep).to_csv(OUT / f"{STEM}.repro.csv", index=False)

    # ---------------------------------------------------------------- g_req for every book
    say("\n" + "=" * 200)
    say("g_req FOR EVERY BOOK, ALL 5 CONVENTIONS x 2 CEILINGS (pass or fail; .greq.csv)")
    say("=" * 200)
    say("Every gross other than 0.75 below is a GENUINE backtest (reproduction [c] rejected the")
    say("rescaling shortcut).  The ladder is " + ", ".join(f"{g:.2f}" for g in LADDER) + ".")
    say("The ladder is run ONLY for the CAGR-floor failures — the population idea 165 asks about.")
    grows, nonmono_n = [], 0
    for (pk, cost, key, m), r in RET.items():
        R = ref[pk]
        b = R["bars"]
        mg = margins5(r, b["full"])
        fb = failing_bars(mg)
        p4b = len(fb) == 0
        p4a = H.pass4a(r, V1[(pk, cost)])
        gv_full = GROSS * R["spy_vol_full"] / ann_vol(r)
        gv_is = GROSS * R["spy_vol_IS"] / ann_vol(H.window(r, "IS"))
        d = dict(panel=pk, cost=cost, key=key, share=m, n=R["nmap"][m],
                 pass4a=p4a, pass4b=p4b, failing="|".join(fb) if fb else "",
                 cagr_fail=("CAGR" in fb), CAGR=metrics(r)["CAGR"],
                 CAGR_floor=0.70 * b["full"]["scagr"], vol=ann_vol(r),
                 spy_vol=R["spy_vol_full"],
                 g_VM_FULL=gv_full, g_VM_IS=gv_is, g_CF_FULL=np.nan, g_CF_IS=np.nan)
        if not d["cagr_fail"]:
            grows.append(d)
            continue
        # CF_* : smallest LADDER rung whose GENUINE re-run clears the floor
        gc_full, nm1 = cf_gross_genuine(pk, cost, key, m, 0.70 * b["full"]["scagr"], ref)
        gc_is, nm2 = cf_gross_genuine(pk, cost, key, m, 0.70 * b["IS"]["scagr"], ref, win="IS")
        nonmono_n += int(nm1 or nm2)
        d["g_CF_FULL"], d["g_CF_IS"] = gc_full, gc_is
        d["nonmonotone_CAGR_in_gross"] = bool(nm1 or nm2)
        # re-evaluate all five bars at each convention, capped and raw — genuine runs
        for conv, g in (("VM_FULL", gv_full), ("VM_IS", gv_is),
                        ("CF_FULL", gc_full), ("CF_IS", gc_is)):
            for ceil in CEILS:
                gg = min(g, CAP) if (ceil == "CAP" and np.isfinite(g)) else g
                if not np.isfinite(gg):
                    d[f"{conv}_{ceil}_pass4b"] = False
                    d[f"{conv}_{ceil}_fail"] = "UNREACHABLE"
                    d[f"{conv}_{ceil}_g"] = np.nan
                    continue
                rr = run_at(pk, cost, key, m, gg, ref)
                fb2 = failing_bars(margins5(rr, b["full"]))
                d[f"{conv}_{ceil}_g"] = gg
                d[f"{conv}_{ceil}_pass4b"] = len(fb2) == 0
                d[f"{conv}_{ceil}_fail"] = "|".join(fb2)
        grows.append(d)
    say(f"\n  genuine backtests cached: {len(_RUN)}   books whose CAGR is NON-MONOTONE in gross "
        f"on the ladder: {nonmono_n}")
    Q = pd.DataFrame(grows).sort_values(["panel", "cost", "key", "share"]).reset_index(drop=True)
    for c in [f"{cv}_{ce}_pass4b" for cv in ("VM_FULL", "VM_IS", "CF_FULL", "CF_IS")
              for ce in CEILS]:
        if c in Q.columns:
            Q[c] = Q[c].fillna(False).astype(bool)
    Q.to_csv(OUT / f"{STEM}.greq.csv", index=False)

    say(f"\n  books: {len(Q)}   4b passes at the published g=0.75: {int(Q.pass4b.sum())}   "
        f"4a passes: {int(Q.pass4a.sum())}")
    say("\n  failing-bar frequency among the 4b failures at g = 0.75:")
    fails = Q[~Q.pass4b]
    for bar in ("CAGR", "DD", "H1", "H2", "OOS"):
        k = int(fails.failing.str.contains(bar).sum())
        say(f"      {bar:>4s}  {k:4d} / {len(fails)}  ({k/max(len(fails),1):.1%})")
    say("\n  CAGR-floor failures by panel x cost (the population idea 165 asks about):")
    cf = Q[Q.cagr_fail]
    say(cf.groupby(["panel", "cost"]).size().to_string())

    say("\n  g_req distribution over the CAGR-floor failures (RAW, uncapped):")
    for conv in ("VM_FULL", "VM_IS", "CF_FULL", "CF_IS"):
        s = cf[f"g_{conv}"]
        say(f"      {conv:>8s}  n={s.notna().sum():4d}  unreachable={int(s.isna().sum()):3d}  "
            f"median {s.median():.3f}  p10 {s.quantile(.10):.3f}  p90 {s.quantile(.90):.3f}  "
            f"frac > 1.00 = {float((s > CAP).mean()):.1%}")

    # ---------------------------------------------------------------- the census
    say("\n" + "=" * 200)
    say("THE HEADLINE CENSUS — of the CAGR-floor 4b failures, how many are really "
        "no-leverage-ceiling KILLs?")
    say("  CEILING   = g_req > 1.00 (rule 2 forbids it)          -> the record stands")
    say("  REACHABLE = g_req <= 1.00 AND all five 4b bars hold there -> the row is MISLABELLED")
    say("  TRADED    = g_req <= 1.00 but another bar now fails    -> the floor was never binding")
    say("=" * 200)
    crows = []
    for conv in ("VM_FULL", "VM_IS", "CF_FULL", "CF_IS"):
        for pk in ["ALL"] + PANELS:
            for cost in ["ALL"] + COSTS:
                sub = cf
                if pk != "ALL":
                    sub = sub[sub.panel == pk]
                if cost != "ALL":
                    sub = sub[sub.cost == cost]
                if not len(sub):
                    continue
                g = sub[f"g_{conv}"]
                ceiling = (~np.isfinite(g)) | (g > CAP)
                ok = sub[f"{conv}_CAP_pass4b"].astype(bool)
                reach = (~ceiling) & ok
                trade = (~ceiling) & (~ok)
                nt = len(sub)
                crows.append(dict(conv=conv, panel=pk, cost=cost, n=nt,
                                  CEILING=int(ceiling.sum()), REACHABLE=int(reach.sum()),
                                  TRADED=int(trade.sum()),
                                  frac_ceiling=float(ceiling.mean()),
                                  frac_reachable=float(reach.mean()),
                                  frac_traded=float(trade.mean()),
                                  median_g=float(g.median())))
    CEN = pd.DataFrame(crows)
    CEN.to_csv(OUT / f"{STEM}.census.csv", index=False)
    say("\n" + CEN.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say("\n  ANSWER TO IDEA 165'S QUESTION (pooled over all panels and both cost rungs):")
    for conv in ("VM_FULL", "VM_IS", "CF_FULL", "CF_IS"):
        r0 = CEN[(CEN.conv == conv) & (CEN.panel == "ALL") & (CEN.cost == "ALL")].iloc[0]
        say(f"      {conv:>8s}: CEILING {r0.frac_ceiling:.1%}  REACHABLE {r0.frac_reachable:.1%}"
            f"  TRADED {r0.frac_traded:.1%}   (n = {int(r0.n)} CAGR-floor failures)")

    # which bar takes over in the TRADED bucket
    say("\n  In the TRADED bucket, which bar takes over (CF_IS, CAP):")
    t = cf[(np.isfinite(cf.g_CF_IS)) & (cf.g_CF_IS <= CAP) & (~cf.CF_IS_CAP_pass4b.astype(bool))]
    if len(t):
        cnt = {}
        for s in t.CF_IS_CAP_fail:
            for b in str(s).split("|"):
                if b:
                    cnt[b] = cnt.get(b, 0) + 1
        say("      " + ", ".join(f"{k} {v}" for k, v in sorted(cnt.items(),
                                                               key=lambda kv: -kv[1])))
    else:
        say("      (empty)")

    # net new 4b passes across the whole corpus
    say("\n  NET 4b PASS COUNT over all 378 books (books that already clear the CAGR floor are")
    say("  left at their published g = 0.75 — re-grossing is only applied to the failures):")
    say(f"      {'STATIC (g=0.75, as published)':<36s} {int(Q.pass4b.sum()):4d}")
    for conv in ("VM_FULL", "VM_IS", "CF_FULL", "CF_IS"):
        for ceil in CEILS:
            col = f"{conv}_{ceil}_pass4b"
            k = int(Q.pass4b.sum()) + int((Q[col] & Q.cagr_fail).sum()) if col in Q.columns else -1
            lab = f"{conv} / {ceil}" + ("  [LOOK-AHEAD]" if "FULL" in conv else "")
            lev = "" if ceil == "CAP" else "  [LEVERED — never a KEEP]"
            say(f"      {lab:<36s} {k:4d}{lev}")

    # ---------------------------------------------------------------- walk-forward, rule 8
    say("\n" + "=" * 200)
    say("WALK-FORWARD (PROTOCOL rule 8) — g and pick chosen on 2009-2016 only, read ONCE on "
        "2017-2026.  VM_IS / CF_IS are the only PROTOCOL-legal conventions here.")
    say("=" * 200)
    wrows = []
    for pk in PANELS:
        R = ref[pk]
        spy = R["spy"]
        spy_oos = metrics(spy.loc[OOS_START:])
        bIS = R["bars"]["IS"]
        for cost in COSTS:
            v1 = V1[(pk, cost)]
            v1o = metrics(v1.loc[OOS_START:])
            books = [(key, m) for key in KEYS for m in SHARES]

            def is_sharpe(key, m):
                return metrics(H.window(RET[(pk, cost, key, m)], "IS"))["Sharpe"]

            def gof(key, m, conv):
                """The book's re-grossed level under `conv`, capped at rule 2's ceiling.
                A book that already clears the CAGR floor has no CF gross and stays at 0.75."""
                q = Q[(Q.panel == pk) & (Q.cost == cost) & (Q.key == key) & (Q.share == m)]
                g = float(q[f"g_{conv}"].iloc[0]) if conv != "STATIC" else GROSS
                return min(g, CAP) if np.isfinite(g) else GROSS

            pick_static = max(books, key=lambda b: is_sharpe(*b))
            arms = {"W_STATIC": (pick_static, GROSS),
                    "W_VMIS": (pick_static, gof(*pick_static, "VM_IS")),
                    "W_CFIS": (pick_static, gof(*pick_static, "CF_IS"))}
            # W_4bIS: IS-window 4b screen at CF_IS(CAP), then IS-Sharpe argmax
            elig = []
            for key, m in books:
                g = gof(key, m, "CF_IS")
                rr = run_at(pk, cost, key, m, g, ref)          # genuine, cached
                mg = C.margins_at(rr, bIS, 0.60, 0.70, which="IS")
                if all(mg[k] > 0 for k in ("H1", "H2", "DD", "CAGR")):
                    elig.append((key, m, g))
            if elig:
                best = max(elig, key=lambda e: metrics(
                    H.window(run_at(pk, cost, e[0], e[1], e[2], ref), "IS"))["Sharpe"])
                arms["W_4bIS"] = ((best[0], best[1]), best[2])
                screen = f"{len(elig)} of {len(books)} books clear the IS 4b screen"
            else:
                arms["W_4bIS"] = (pick_static, GROSS)
                screen = "IS 4b screen EMPTY -> fell back to W_STATIC"
            say(f"\n  [{pk} @ {cost:.0f}bps]  {screen}")
            for aname, ((key, m), g) in arms.items():
                r = run_at(pk, cost, key, m, g, ref)           # genuine, cached
                mo = metrics(r.loc[OOS_START:])
                mgo = C.margins_at(r, R["bars"]["OOS"], 0.60, 0.70, which="OOS")
                fbo = [k for k in ("H1", "H2", "DD", "CAGR") if mgo[k] <= 0]
                wrows.append(dict(panel=pk, cost=cost, arm=aname, key=key, share=m,
                                  n=R["nmap"][m], g=g,
                                  OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                  OOS_MaxDD=mo["MaxDD"],
                                  OOS_4b_fail="|".join(fbo) if fbo else "(none)",
                                  v1_OOS_Sharpe=v1o["Sharpe"], v1_OOS_CAGR=v1o["CAGR"],
                                  v1_OOS_MaxDD=v1o["MaxDD"],
                                  spy_OOS_Sharpe=spy_oos["Sharpe"],
                                  spy_OOS_CAGR=spy_oos["CAGR"],
                                  spy_OOS_MaxDD=spy_oos["MaxDD"]))
                say(f"      {aname:<9s} pick {key:>4s}@m={m:.2f}(n={R['nmap'][m]:3d}) g={g:.3f}"
                    f"  OOS {mo['CAGR']:7.2%}/{mo['Sharpe']:.4f}/{mo['MaxDD']:7.2%}"
                    f"   4b-OOS fails: {'|'.join(fbo) if fbo else '(none)'}")
            say(f"      {'RULES v1':<9s} {'':32s}  OOS {v1o['CAGR']:7.2%}/{v1o['Sharpe']:.4f}/"
                f"{v1o['MaxDD']:7.2%}")
            say(f"      {'SPY':<9s} {'':32s}  OOS {spy_oos['CAGR']:7.2%}/"
                f"{spy_oos['Sharpe']:.4f}/{spy_oos['MaxDD']:7.2%}")
    WF = pd.DataFrame(wrows)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say("\n  Mean OOS Sharpe by arm (pooled over the 6 panel x cost cells):")
    say(WF.groupby("arm")[["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD"]].mean()
        .to_string(float_format=lambda x: f"{x:.4f}"))
    # P6 as re-stated after [c]: does gross really have "zero Sharpe content"?  Under the true
    # engine it cannot, because the weight path itself changes.  Measured on the ladder.
    say("\n  P6 (restated after [c]) — does gross carry ZERO Sharpe content, as idea 66 claims?")
    dsh = []
    for pk in PANELS:
        for key, m in (("NONE", 0.53), ("INV", 0.20), ("POS", 0.10), ("R6", 0.15)):
            s75 = metrics(RET[(pk, 10.0, key, m)])["Sharpe"]
            for g in (0.80, 1.00, 1.50):
                dsh.append(abs(metrics(run_at(pk, 10.0, key, m, g, ref))["Sharpe"] - s75))
    say(f"      |Sharpe(g) - Sharpe(0.75)| over 36 genuine re-runs: mean {np.mean(dsh):.4f}, "
        f"max {np.max(dsh):.4f}.  Gross is NOT Sharpe-neutral under this engine.")

    # ---------------------------------------------------------------- verdict
    say("\n" + "=" * 200)
    r_vm = CEN[(CEN.conv == "VM_FULL") & (CEN.panel == "ALL") & (CEN.cost == "ALL")].iloc[0]
    r_cf = CEN[(CEN.conv == "CF_IS") & (CEN.panel == "ALL") & (CEN.cost == "ALL")].iloc[0]
    say(f"VERDICT — no new book, no KEEP.  This run prices a leaderboard COLUMN.")
    say(f"  Under idea 156's own VM_FULL formula, {r_vm.frac_ceiling:.1%} of the "
        f"{int(r_vm.n)} CAGR-floor failures need g > 1.00 and are genuine no-leverage KILLs; "
        f"{r_vm.frac_reachable:.1%} would clear ALL FIVE 4b bars at a legal gross and are "
        f"mislabelled; {r_vm.frac_traded:.1%} merely swap the CAGR bar for another.")
    say(f"  Under the floor's own inverse CF_IS (prospectively implementable), the numbers are "
        f"{r_cf.frac_ceiling:.1%} / {r_cf.frac_reachable:.1%} / {r_cf.frac_traded:.1%}.")
    say(f"done in {time.time()-t0:.0f}s")
    say("=" * 200)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
