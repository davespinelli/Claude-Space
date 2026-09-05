#!/usr/bin/env python3
"""QUEUE idea 177 — publish-the-failing-bar-not-the-required-gross  (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 177)
    "idea 165 found g_req re-labels at most 2.3% of CAGR-floor KILLs while 62% of them are
     drawdown failures wearing a CAGR label, knowable for free at g=0.75.  Idea 161 asks the
     same question from the other end.  Propose the failing-bar string as a LEADERBOARD schema
     column, back-fill it across the 378-book corpus, and measure how often the first-named bar
     predicts which instrument would fix the book.  Cheap; max 2 params."

WHAT IS AT STAKE
    Idea 165 proposed `g_req` as the leaderboard's re-label column and its own run killed it:
    the number costs ~2000 genuine backtests to produce, is not monotone in gross for 92 of 213
    books, and re-labels at most 2.3% of the CAGR-floor KILLs.  Idea 177's counter-proposal is
    the CHEAPEST possible column — the list of 4b bars the book actually failed, which every
    backtest already computes and throws away.  A column earns its place in a schema only if it
    CARRIES DECISION CONTENT.  For a failing-bar string the decision it should inform is "what
    would you change to fix this book?", so the test is exactly that: does the first-named bar
    predict which instrument repairs the book, better than the base rate and better than chance?

    Two rival readings, both testable on one corpus:
      (A) DIAGNOSTIC — different bars fail for different mechanical reasons (a CAGR failure is a
          risk-budget shortfall, a DD failure is a concentration/exposure problem, a half-Sharpe
          failure is a regime problem), so the named bar points at its own repair.  Then the
          bar -> instrument map is much better than the base rate.
      (B) BOOKKEEPING — the bars are five readings of one underlying quantity (how good the book
          is), the failures come in near-identical bundles, and whichever instrument helps most
          helps most books regardless of which bar was named.  Then the map is no better than
          "always apply the single best instrument", and the column is a label, not a diagnosis.
    (B) is the project's standing prior: ideas 110/132/151/166/171/174/175/186/192 have now put
    an in-sample selector behind a do-nothing or a pre-registered constant eight times running.

CORPUS — carried verbatim from ideas 153/159/165, not a bespoke draw
    3 panels x 7 keys x 9 shares = 189 weight paths, weekly, t+1, gross 0.75 spread over the
    names actually held (idea 153/159's `norm` construction), x 2 cost rungs = 378 books.
      Panels  u56 (universe.json), broad (universe_broad.json),
              small (sub-$2B, the max_1d_move >= 1.0 tickers dropped per data/small_meta.csv)
      Keys    NONE INV POS MOM R6 R3 RND (RND = idea 159's fixed per-name scramble, seed 159000)
      Shares  0.05 0.10 0.15 0.20 0.27 0.35 0.53 0.75 1.00, n = max(2, round(m x mean weekly
              eligible count)).  Costs 10 and 25 bps.
    Panels, keys, shares and cost rungs are REPORTED CORPUS AXES; none of them is tuned here.

    COST IS DERIVED, NOT RE-RUN.  engine.backtest computes port = (held*rets).sum(1) -
    turnover*bps/1e4, so the second cost rung is an EXACT linear deduction from one 0 bps run.
    Reproduction check [a] measures that identity against genuine re-runs and the run says so
    loudly if it is not ~1e-16.  This is what makes 1701 genuine backtests affordable.

THE PROPOSED COLUMN
    `failing`  the 4b bars the book failed, in the canonical order H1|H2|OOS|DD|CAGR
               (idea 165's own string, already emitted by its .greq.csv but never tested)
    `bar1`     the FIRST-NAMED bar — the thing idea 177 wants to hang a decision on.

TUNED PARAMETERS — exactly two, swept exhaustively, ALL grid points reported
    1. the NAMING RULE, 3 values (there is no canonical "first" bar; the choice is the parameter)
         CANON   first in the fixed order H1|H2|OOS|DD|CAGR  (idea 165's string order)
         TIGHT   the most negative RAW margin
         TIGHTZ  the most negative margin divided by that bar's corpus-wide SD of margins
                 (the bars are in incomparable units — Sharpe, pp of drawdown, pp of CAGR —
                 so a raw argmin is partly a units artefact; TIGHTZ removes that)
    2. the DIAL STRENGTH of every repair instrument, 2 values: MILD / STRONG (table below).
    3 naming rules x 2 dials = 6 grid points, every one printed and written to .naming.csv.

REPAIR INSTRUMENTS — a reported axis of 4, price-only, each a single change to the book
    GUP   raise gross          MILD g=0.90   STRONG g=1.00 (PROTOCOL rule 2's ceiling)
    GDN   cut gross            MILD g=0.60   STRONG g=0.45
    WIDE  hold more names      MILD n->max(n+1, round(1.5n))  STRONG n->max(n+2, round(2.5n)),
                               both capped at the panel width
    SLOW  rebalance slower     MILD freq=M   STRONG freq=Q   (the book is weekly as published)
    Every treated book is a GENUINE backtest.  Idea 165 established that gross is NOT an exact
    lever under engine.py (the uninvested sleeve enters the drift denominator), so no series in
    this file is produced by rescaling another.  189 base + 8 treatment grids x 189 = 1701 runs.

WALK-FORWARD (PROTOCOL rule 8) — the map is FITTED IN-SAMPLE AND READ ONCE OUT-OF-SAMPLE
    Bars are read on the IS window (<= 2016-12-31) and the repair outcome is scored on the IS
    window, so the bar1 -> instrument map is built from IS information only.  It is then applied
    once to 2017-01-01..2026 for every book that fails the IS-window 4b.  Four arms:
      S0  DO-NOTHING          hold the book as published (the control the project keeps winning with)
      S1  MAP                 apply the IS-fitted bar1 -> instrument map
      S2  CONSTANT            always apply the single instrument with the best mean IS score
                              (a pre-registered constant, per ideas 175/189)
      S3  RANDOM              a random instrument per book, seed 177000 (the chance null)
    Reported per arm: mean OOS Sharpe, paired difference vs S0 with a t-stat and a win/loss
    count, mean OOS CAGR and MaxDD, and both KEEP paths (4a against RULES v1, 4b against SPY)
    on the OOS window, beside RULES v1's and SPY's own OOS numbers on every panel.

PRE-REGISTERED PREDICTIONS (written before any number from the main grid was read)
    P1  Reproduction: this run's 378 books match idea 165's published .grid.csv on n, CAGR,
        Sharpe, MaxDD, H1, H2 and OOS_Sharpe to < 1e-9, and the derived cost rung matches a
        genuine re-run to ~1e-16.  If [a] or [b] fails nothing below is trustworthy.
    P2  The column is not degenerate: a MAJORITY of failing books fail on >= 2 bars, so
        "first-named" is a real choice and the naming rule matters.
    P3  Reading (B) wins: the bar1 -> instrument map beats the base-rate control by less than
        10 percentage points of accuracy under every naming rule, and its permutation p > 0.05
        under at least one.  If (A) wins instead — a map that beats base rate by >= 10pp with
        p < 0.05 under all three naming rules — that is a genuinely useful column and a rare
        positive result for the project.
    P4  DD is the most common first-named bar under TIGHTZ, and GDN (cut gross) is the
        corpus-modal fixing instrument — i.e. the map collapses toward one cell.
    P5  Rule 8: S0 do-nothing is not beaten by S1 at t > 2 (the ninth consecutive do-nothing
        result).  S2 the constant beats S1 the fitted map, per idea 189's generalisation.
    P6  No new book: fewer than 40 of the 378 untreated books pass 4b on the full sample and no
        treated book is promoted by this run.

CAVEATS carried, not buried
    * SURVIVORSHIP.  All three panels are current constituents (idea 54).  The small panel is
      the sub-$2B screen with the 44 max_1d_move >= 1.0 tickers dropped, and its SPY is a joined
      benchmark that is never selectable.  Absent delistings inflate every CAGR here, so every
      4b CAGR-floor margin in this file is optimistic and no level is an achievable return.
    * Idea 128: the IS window's SPY drawdown is shallower than the OOS window's, so an IS-read
      DD bar is measured on a window that cannot express a deep drawdown.  That biases the
      IS-fitted map toward under-naming DD, which works AGAINST P4 in the walk-forward.
    * Idea 165: CAGR is not monotone in gross under engine.py, so GUP/GDN are scans, not levers,
      and "the instrument that fixes it" is always relative to the two dial values tested.
    * Every row is quoted at t+1 execution only (idea 126).
    * This run classifies EXISTING books.  It cannot promote one and does not try to; its output
      is a statement about the LEADERBOARD schema, not a candidate.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .repro.csv, .naming.csv,
.repair.csv and .walkforward.csv.  Exposes build_panels()/build_base() for downstream reuse.
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402,F401
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_publish-the-failing-bar-not-the-required-gross_cloud"
OUT = ROOT / "research" / "backtests"
I159P = OUT / "2026-09-05_the-share-at-which-ranking-stops-paying_cloud.py"
I165_GRID = OUT / "2026-09-05_required-gross-as-a-leaderboard-column_cloud.grid.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


I159 = _load(I159P, "i159")
C, H, I153 = I159.C, I159.H, I159.I153

FREQ, GROSS, MAX_VOL = "W", 0.75, 0.60
PANELS = ["u56", "broad", "small"]
KEYS = ["NONE", "INV", "POS", "MOM", "R6", "R3", "RND"]
SHARES = [0.05, 0.10, 0.15, 0.20, 0.27, 0.35, 0.53, 0.75, 1.00]
COSTS = [10.0, 25.0]
BARS = ("H1", "H2", "OOS", "DD", "CAGR")
NAMINGS = ["CANON", "TIGHT", "TIGHTZ"]
DIALS = ["MILD", "STRONG"]
INSTR = ["GUP", "GDN", "WIDE", "SLOW"]
IS_END, OOS_START = H.IS_END, H.OOS_START
PHI, DELTA = 0.70, 0.60
SEED = 177_000

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 800)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# --------------------------------------------------------------- instrument definitions
def spec(instr, dial, n, ncap):
    """(gross, n, freq) for a treated book.  The untreated book is (0.75, n, 'W')."""
    if instr == "GUP":
        return (0.90 if dial == "MILD" else 1.00), n, FREQ
    if instr == "GDN":
        return (0.60 if dial == "MILD" else 0.45), n, FREQ
    if instr == "WIDE":
        nn = max(n + 1, int(round(1.5 * n))) if dial == "MILD" else max(n + 2, int(round(2.5 * n)))
        return GROSS, min(nn, ncap), FREQ
    if instr == "SLOW":
        return GROSS, n, ("M" if dial == "MILD" else "Q")
    raise ValueError(instr)


# --------------------------------------------------------------- one run -> both cost rungs
def run_paths(px, key, n, pk, g, freq, start):
    """One GENUINE 0 bps backtest; both cost rungs derived exactly (check [a] validates this)."""
    W = I159.weights(px, key, n, pk) * (g / GROSS)
    res = backtest(px, W, cost_bps=0.0, freq=freq)
    r0, tv = res["returns"], res["turnover"]
    return {c: (r0 - tv * c / 1e4).loc[start:] for c in COSTS}, float(tv.sum() / (len(r0) / 252))


def margins(r, bars, which):
    """4b's five margins on a window.  which='full' is PROTOCOL's own reading."""
    w = H.window(r, which)
    h1, h2 = H.halves(w)
    m = metrics(w)
    soos = metrics(r.loc[OOS_START:])["Sharpe"] if which == "full" else m["Sharpe"]
    return dict(H1=h1 - bars["s1"], H2=h2 - bars["s2"], OOS=soos - bars["soos"],
                DD=DELTA * abs(bars["sdd"]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - PHI * bars["scagr"])


def fails(mg):
    return [k for k in BARS if mg[k] <= 0]


def name_bar(mg, rule, sd):
    f = fails(mg)
    if not f:
        return ""
    if rule == "CANON":
        return f[0]
    if rule == "TIGHT":
        return min(f, key=lambda k: mg[k])
    return min(f, key=lambda k: mg[k] / sd[k])


def tstat(d):
    d = np.asarray([x for x in d if np.isfinite(x)], float)
    if len(d) < 3 or d.std(ddof=1) == 0:
        return np.nan
    return float(d.mean() / (d.std(ddof=1) / np.sqrt(len(d))))


def modal(vals):
    v, c = np.unique(np.asarray(vals), return_counts=True)
    return str(v[int(np.argmax(c))])


# --------------------------------------------------------------- reusable corpus builders
def build_panels(verbose=True):
    ref, nmap = {}, {}
    for pk in PANELS:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        b = {w: C.bars_win(spy, w) for w in ("full", "IS", "OOS")}
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        n_elig = float(I153.eligible_mask(px, pk).loc[start:].sum(axis=1).mean())
        ref[pk] = dict(px=px, start=start, spy=spy, bars=b, v1=v1, n_elig=n_elig, desc=desc,
                       ncap=px.shape[1])
        nmap[pk] = {m: max(2, int(round(m * n_elig))) for m in SHARES}
        if verbose:
            ms, mo = metrics(spy), metrics(spy.loc[OOS_START:])
            say(f"\n[panel] {pk} = {desc}: {px.shape[1]} cols, eval from {start.date()}, mean "
                f"weekly eligible {n_elig:.1f}")
            say("    share -> n:  " + ", ".join(f"{m:.3g}->{nmap[pk][m]}" for m in SHARES))
            say(f"    SPY  {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%}  halves "
                f"{b['full']['s1']:.3f}/{b['full']['s2']:.3f} | OOS {mo['CAGR']:.2%}/"
                f"{mo['Sharpe']:.3f}/{mo['MaxDD']:.2%}")
            for c in COSTS:
                m1, mo1 = metrics(v1[c]), metrics(v1[c].loc[OOS_START:])
                say(f"    RULES v1 @{c:.0f}bps {m1['CAGR']:.2%}/{m1['Sharpe']:.3f}/"
                    f"{m1['MaxDD']:.2%} | OOS {mo1['CAGR']:.2%}/{mo1['Sharpe']:.3f}/"
                    f"{mo1['MaxDD']:.2%}")
    return ref, nmap


def build_base(ref, nmap):
    """The 378 untreated books (189 genuine runs, both cost rungs derived)."""
    base_r, turn = {}, {}
    for pk in PANELS:
        R = ref[pk]
        for key in KEYS:
            for m in SHARES:
                paths, tv = run_paths(R["px"], key, nmap[pk][m], pk, GROSS, FREQ, R["start"])
                for c in COSTS:
                    base_r[(pk, c, key, m)] = paths[c]
                    turn[(pk, c, key, m)] = tv
    return base_r, turn


def main():
    t0 = time.time()
    say("=" * 200)
    say(f"IDEA 177 — publish-the-failing-bar-not-the-required-gross   ({STEM})")
    say("Back-fill the 4b FAILING-BAR string across idea 165's 378-book corpus and measure "
        "whether the first-named bar predicts which instrument repairs the book.")
    say("PRE-REGISTERED: exactly 2 tuned params (naming rule x 3, dial strength x 2). Panels, "
        "keys, shares, cost rungs and the 4 instruments are carried/reported axes, never tuned.")
    say("PREDICTIONS P1-P6 are in the docstring, written before the grid was read.")
    say("=" * 200)

    ref, nmap = build_panels()

    # ---------------------------------------------------------- [a] the cost identity
    say("\n" + "=" * 200)
    say("REPRODUCTION [a] — the derived cost rung against genuine re-runs at cost_bps=25")
    errs = []
    for pk in PANELS:
        R = ref[pk]
        for key, m in (("NONE", SHARES[2]), ("R6", SHARES[-3]), ("RND", SHARES[-1])):
            n = nmap[pk][m]
            gen = backtest(R["px"], I159.weights(R["px"], key, n, pk),
                           cost_bps=25.0, freq=FREQ)["returns"].loc[R["start"]:]
            der = run_paths(R["px"], key, n, pk, GROSS, FREQ, R["start"])[0][25.0]
            errs.append(float(np.abs(gen - der).max()))
    cost_ok = max(errs) < 1e-12
    say(f"    max |genuine - derived| over {len(errs)} books: {max(errs):.3e}  -> "
        f"{'IDENTITY HOLDS' if cost_ok else 'IDENTITY FAILS — every cost rung below is void'}")

    # ---------------------------------------------------------- the base corpus
    say("\n" + "=" * 200)
    say("BASE CORPUS — 3 panels x 7 keys x 9 shares = 189 genuine runs -> 378 books")
    base_r, turn = build_base(ref, nmap)
    rows = []
    for bk, r in base_r.items():
        pk, c, key, m = bk
        mf, mo, mi = metrics(r), metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
        h1, h2 = H.halves(r)
        rows.append(dict(panel=pk, cost=c, key=key, share=m, n=nmap[pk][m], turnover=turn[bk],
                         CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                         OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                         IS_Sharpe=mi["Sharpe"]))
    grid = pd.DataFrame(rows)
    say(f"    {len(grid)} books built in {time.time()-t0:.0f}s")

    # ---------------------------------------------------------- [b] against idea 165's grid
    say("\nREPRODUCTION [b] — this run's 378 books against idea 165's published .grid.csv")
    rep = []
    if I165_GRID.exists():
        pub = pd.read_csv(I165_GRID)
        k = ["panel", "cost", "key", "share"]
        j = grid.merge(pub, on=k, suffixes=("", "_p"))
        say(f"    matched {len(j)} of {len(grid)} rows on (panel, cost, key, share)")
        for f in ("n", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"):
            d = float(np.abs(j[f].astype(float) - j[f + "_p"].astype(float)).max())
            rep.append(dict(check="[b] idea165 grid", field=f, n=len(j), maxabsdiff=d,
                            verdict="MATCH" if d < 1e-9 else "MISMATCH"))
            say(f"    {f:<12} max|diff| {d:.3e}   {'MATCH' if d < 1e-9 else 'MISMATCH'}")
        repro_ok = all(x["verdict"] == "MATCH" for x in rep) and len(j) == len(grid)
    else:
        repro_ok = False
        say("    idea 165 grid not found — reproduction UNAVAILABLE")
    rep.append(dict(check="[a] cost identity", field="returns", n=len(errs), maxabsdiff=max(errs),
                    verdict="MATCH" if cost_ok else "MISMATCH"))
    pd.DataFrame(rep).to_csv(OUT / f"{STEM}.repro.csv", index=False)
    say(f"    P1 REPRODUCTION: {'PASS (2/2)' if (repro_ok and cost_ok) else 'FAIL — read the numbers above before quoting anything below'}")

    # ---------------------------------------------------------- margins of the untreated books
    mg = {w: {bk: margins(r, ref[bk[0]]["bars"][w], w) for bk, r in base_r.items()}
          for w in ("full", "IS", "OOS")}
    sd = {w: {k: float(np.std([mg[w][b][k] for b in base_r], ddof=1)) for k in BARS}
          for w in ("full", "IS", "OOS")}
    say("\n    corpus SD of each margin (the TIGHTZ scaler, full sample): " +
        ", ".join(f"{k} {sd['full'][k]:.4f}" for k in BARS))
    grid["failing"] = ["|".join(fails(mg["full"][b])) for b in base_r]
    for rule in NAMINGS:
        grid[f"bar1_{rule}"] = [name_bar(mg["full"][b], rule, sd["full"]) for b in base_r]
    grid["pass4b"] = [len(fails(mg["full"][b])) == 0 for b in base_r]
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"    grid with the proposed columns -> {STEM}.grid.csv")

    # ---------------------------------------------------------- the repair grid
    say("\n" + "=" * 200)
    say("REPAIR GRID — 4 instruments x 2 dials x 189 paths = 1512 genuine runs")
    treat, tmg = {}, {}
    for instr in INSTR:
        for dial in DIALS:
            for pk in PANELS:
                R = ref[pk]
                for key in KEYS:
                    for m in SHARES:
                        g, n2, fq = spec(instr, dial, nmap[pk][m], R["ncap"])
                        paths, _ = run_paths(R["px"], key, n2, pk, g, fq, R["start"])
                        for c in COSTS:
                            tk = (pk, c, key, m, instr, dial)
                            treat[tk] = paths[c]
                            tmg[tk] = {w: margins(paths[c], R["bars"][w], w)
                                       for w in ("full", "IS", "OOS")}
            say(f"    {instr}/{dial}: {time.time()-t0:.0f}s")

    # ---------------------------------------------------------- the column itself
    say("\n" + "=" * 200)
    say("THE PROPOSED COLUMN — 4b failing string and first-named bar, all 378 books")
    nfail = {b: len(fails(mg["full"][b])) for b in base_r}
    n_pass = sum(1 for v in nfail.values() if v == 0)
    say(f"    4b passes (full sample): {n_pass} of {len(base_r)};  failing: {len(base_r)-n_pass}")
    dist = pd.Series([v for v in nfail.values() if v > 0]).value_counts().sort_index()
    say("    P2 — bars failed per failing book:  " +
        ", ".join(f"{k}: {v}" for k, v in dist.items()))
    multi = float(sum(v for k, v in dist.items() if k >= 2) / max(1, dist.sum()))
    say(f"    fraction failing >= 2 bars: {multi:.3f}  ->  P2 {'HIT' if multi > 0.5 else 'MISS'}")
    say("    failing-string frequency (canonical order), top 12 of "
        f"{grid.failing.nunique()} distinct strings:")
    for s, v in grid.failing.value_counts().head(12).items():
        say(f"        {(s or '(passes 4b)'):<26} {v}")
    say("    first-named bar frequency by naming rule (failing books only):")
    say(pd.DataFrame({r: grid.loc[grid.failing != "", f"bar1_{r}"].value_counts()
                      for r in NAMINGS}).fillna(0).astype(int).to_string())

    # ---------------------------------------------------------- repair outcomes
    rep_rows = []
    for bk in base_r:
        pk, c, key, m = bk
        for instr in INSTR:
            for dial in DIALS:
                mt = tmg[(pk, c, key, m, instr, dial)]["full"]
                ft = fails(mt)
                rep_rows.append(dict(panel=pk, cost=c, key=key, share=m, instr=instr, dial=dial,
                                     base_nfail=nfail[bk], treat_nfail=len(ft),
                                     fixed=(nfail[bk] > 0 and len(ft) == 0),
                                     zmin=min(mt[k] / sd["full"][k] for k in BARS),
                                     **{f"m_{k}": mt[k] for k in BARS},
                                     **{f"cleared_{k}": bool(mt[k] > 0) for k in BARS}))
    repair = pd.DataFrame(rep_rows)
    repair.to_csv(OUT / f"{STEM}.repair.csv", index=False)
    say(f"\n    repair grid -> {STEM}.repair.csv ({len(repair)} rows)")
    say(f"    books FIXED to a full-sample 4b pass, by instrument x dial "
        f"(of {len(base_r)-n_pass} failing books):")
    say(repair[repair.base_nfail > 0].pivot_table(index="instr", columns="dial", values="fixed",
                                                  aggfunc="sum").reindex(INSTR).to_string())
    say("    ...and mean post-repair z-margin (higher = closer to passing every bar):")
    say(repair[repair.base_nfail > 0].pivot_table(index="instr", columns="dial", values="zmin",
                                                  aggfunc="mean").reindex(INSTR).to_string(
        float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------- does bar1 predict the repair?
    say("\n" + "=" * 200)
    say("THE QUESTION — does the FIRST-NAMED bar predict which instrument fixes the book?")
    say("    acc = accuracy of the corpus-modal bar1 -> instrument map; base-rate = always the "
        "corpus-modal instrument; p = 2000-draw permutation null on the bar1 labels.")
    rng = np.random.default_rng(SEED)
    nam_rows = []
    for dial in DIALS:
        fixed_by = {b: [i for i in INSTR if
                        len(fails(tmg[(b[0], b[1], b[2], b[3], i, dial)]["full"])) == 0]
                    for b in base_r if nfail[b] > 0}
        best = {b: max(INSTR, key=lambda i: (i in fixed_by[b],
                                             min(tmg[(b[0], b[1], b[2], b[3], i, dial)]["full"][k]
                                                 / sd["full"][k] for k in BARS)))
                for b in fixed_by}
        for rule in NAMINGS:
            lab = {b: name_bar(mg["full"][b], rule, sd["full"]) for b in fixed_by}
            for scope, ks in (("FIXABLE", [b for b in fixed_by if fixed_by[b]]),
                              ("ALL_FAILING", list(fixed_by))):
                if len(ks) < 10:
                    continue
                y = np.array([best[b] for b in ks])
                x = np.array([lab[b] for b in ks])
                mp = {bar: modal(y[x == bar]) for bar in sorted(set(x))}
                acc = float(np.mean([mp[a] == b for a, b in zip(x, y)]))
                base_rate = float(np.unique(y, return_counts=True)[1].max() / len(y))
                null = np.empty(2000)
                for t in range(2000):
                    xs = rng.permutation(x)
                    m2 = {bar: modal(y[xs == bar]) for bar in sorted(set(xs))}
                    null[t] = np.mean([m2[a] == b for a, b in zip(xs, y)])
                p = float((null >= acc).mean())
                nam_rows.append(dict(rule=rule, dial=dial, scope=scope, n=len(ks), acc=acc,
                                     base_rate=base_rate, lift_pp=100 * (acc - base_rate),
                                     null_mean=float(null.mean()), p_perm=p,
                                     map=";".join(f"{k}->{v}" for k, v in mp.items())))
                say(f"    {rule:<7} {dial:<7} {scope:<12} n={len(ks):<4} acc {acc:.3f}  "
                    f"base {base_rate:.3f}  lift {100*(acc-base_rate):+5.1f}pp  null "
                    f"{null.mean():.3f}  p={p:.4f}   " +
                    ";".join(f"{k}->{v}" for k, v in mp.items()))
    naming = pd.DataFrame(nam_rows)
    naming.to_csv(OUT / f"{STEM}.naming.csv", index=False)
    fx = naming[naming.scope == "FIXABLE"]
    if len(fx):
        p3 = bool((fx.lift_pp < 10).all() or (fx.p_perm > 0.05).any())
        say(f"\n    P3 (reading B — bookkeeping): max lift {fx.lift_pp.max():+.1f}pp, min p "
            f"{fx.p_perm.min():.4f}  ->  {'HIT' if p3 else 'MISS — reading (A) survives'}")

    # ---------------------------------------------------------- weaker target: does the bar move?
    say("\n    WEAKER TARGET — P(instrument clears bar B | the untreated book fails bar B)")
    for dial in DIALS:
        tab = {}
        for bar in BARS:
            ks = [b for b in base_r if nfail[b] > 0 and mg["full"][b][bar] <= 0]
            tab[bar] = {"n": len(ks), **{i: (float(np.mean(
                [tmg[(b[0], b[1], b[2], b[3], i, dial)]["full"][bar] > 0 for b in ks]))
                if ks else np.nan) for i in INSTR}}
        say(f"      dial={dial}")
        say(pd.DataFrame(tab).T.to_string(float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------- rule 8 walk-forward
    say("\n" + "=" * 200)
    say("RULE 8 WALK-FORWARD — bar1 and the map fitted on IS (<= 2016-12-31); 2017-2026 read ONCE")
    wf_rows = []
    for dial in DIALS:
        cells = [b for b in base_r if len(fails(mg["IS"][b])) > 0]
        isz = {(b, i): min(tmg[(b[0], b[1], b[2], b[3], i, dial)]["IS"][k] / sd["IS"][k]
                           for k in BARS) for b in cells for i in INSTR}
        is_best = {b: max(INSTR, key=lambda i: isz[(b, i)]) for b in cells}
        const = max(INSTR, key=lambda i: float(np.mean([isz[(b, i)] for b in cells])))
        for rule in NAMINGS:
            lab = {b: name_bar(mg["IS"][b], rule, sd["IS"]) for b in cells}
            mp = {bar: modal([is_best[b] for b in cells if lab[b] == bar])
                  for bar in sorted(set(lab.values()))}
            rr = np.random.default_rng(SEED + 1)
            pick = {"S0": {b: None for b in cells}, "S1": {b: mp[lab[b]] for b in cells},
                    "S2": {b: const for b in cells},
                    "S3": {b: INSTR[int(rr.integers(0, len(INSTR)))] for b in cells}}
            per = {}
            for arm in ("S0", "S1", "S2", "S3"):
                out = []
                for b in cells:
                    pk, c, key, m = b
                    r = base_r[b] if pick[arm][b] is None else treat[(pk, c, key, m, pick[arm][b], dial)]
                    mo = metrics(r.loc[OOS_START:])
                    mgo = (mg["OOS"][b] if pick[arm][b] is None
                           else tmg[(pk, c, key, m, pick[arm][b], dial)]["OOS"])
                    v1o = ref[pk]["v1"][c].loc[OOS_START:]
                    h1, h2 = H.halves(r.loc[OOS_START:])
                    b1, b2 = H.halves(v1o)
                    out.append(dict(S=mo["Sharpe"], CAGR=mo["CAGR"], DD=mo["MaxDD"],
                                    p4b=all(mgo[k] > 0 for k in BARS),
                                    p4a=bool(h1 > b1 and h2 > b2 and
                                             mo["MaxDD"] >= metrics(v1o)["MaxDD"])))
                per[arm] = out
            for arm in ("S0", "S1", "S2", "S3"):
                o = per[arm]
                d = [x["S"] - y["S"] for x, y in zip(o, per["S0"])]
                t = tstat(d)
                wf_rows.append(dict(rule=rule, dial=dial, arm=arm, n=len(o), const=const,
                                    map=";".join(f"{k}->{v}" for k, v in mp.items()),
                                    mean_OOS_Sharpe=float(np.mean([x["S"] for x in o])),
                                    mean_OOS_CAGR=float(np.mean([x["CAGR"] for x in o])),
                                    mean_OOS_MaxDD=float(np.mean([x["DD"] for x in o])),
                                    d_vs_S0=float(np.mean(d)), t_vs_S0=t,
                                    wins=int(sum(1 for x in d if x > 0)),
                                    losses=int(sum(1 for x in d if x < 0)),
                                    pass4a=int(sum(x["p4a"] for x in o)),
                                    pass4b=int(sum(x["p4b"] for x in o))))
                say(f"    {rule:<7} {dial:<7} {arm}  n={len(o):<4} OOS Sharpe "
                    f"{np.mean([x['S'] for x in o]):.4f}  CAGR "
                    f"{np.mean([x['CAGR'] for x in o]):.2%}  MaxDD "
                    f"{np.mean([x['DD'] for x in o]):.2%}  d_vs_S0 {np.mean(d):+.4f} "
                    f"(t {t:+.2f}, {sum(1 for x in d if x>0)}W/{sum(1 for x in d if x<0)}L)  "
                    f"OOS 4a {sum(x['p4a'] for x in o)}  4b {sum(x['p4b'] for x in o)}"
                    + (f"   map={mp}" if arm == "S1" else "")
                    + (f"   const={const}" if arm == "S2" else ""))
    wf = pd.DataFrame(wf_rows)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    say("\n    BENCHMARKS over the same OOS window (2017-01-01..end), per panel and cost rung:")
    for pk in PANELS:
        mo = metrics(ref[pk]["spy"].loc[OOS_START:])
        s = "  ".join(
            f"RULES v1 @{c:.0f}bps {metrics(ref[pk]['v1'][c].loc[OOS_START:])['CAGR']:.2%}/"
            f"{metrics(ref[pk]['v1'][c].loc[OOS_START:])['Sharpe']:.4f}/"
            f"{metrics(ref[pk]['v1'][c].loc[OOS_START:])['MaxDD']:.2%}" for c in COSTS)
        say(f"      {pk:<6} SPY OOS {mo['CAGR']:.2%}/{mo['Sharpe']:.4f}/{mo['MaxDD']:.2%}   {s}")

    s0 = float(wf[wf.arm == "S0"].mean_OOS_Sharpe.mean())
    s1, s2, s3 = (wf[wf.arm == a] for a in ("S1", "S2", "S3"))
    say(f"\n    P5 — S0 do-nothing {s0:.4f} | S1 map {s1.mean_OOS_Sharpe.mean():.4f} "
        f"(max t {s1.t_vs_S0.max():+.2f}) | S2 constant {s2.mean_OOS_Sharpe.mean():.4f} "
        f"(max t {s2.t_vs_S0.max():+.2f}) | S3 random {s3.mean_OOS_Sharpe.mean():.4f}")
    say(f"    P5 do-nothing clause {'HIT' if s1.t_vs_S0.max() <= 2 else 'MISS'}; "
        f"constant beats map: "
        f"{'YES' if s2.mean_OOS_Sharpe.mean() > s1.mean_OOS_Sharpe.mean() else 'NO'}")
    say(f"    P6 — untreated books passing full-sample 4b: {n_pass} of {len(base_r)}  ->  "
        f"{'HIT' if n_pass < 40 else 'MISS'}.  No book is promoted by this run.")
    say(f"\nTOTAL {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
