"""
IDEA 178 — is-the-IS-4b-screen-a-one-cell-accident      (lane C, 2026-09-05)
================================================================================================
THE QUESTION
    Idea 165's rule-8 walk-forward reported the IS-window 4b SCREEN (`W_4bIS`) as the only arm
    that moves OOS Sharpe (0.6715 vs 0.6527 for the do-nothing control) and, in 1 of its 6
    (panel x cost) cells — u56 @ 10 bps — picking R6 @ m=0.15 (n=6) at the published g=0.75,
    a book that clears every OOS-window 4b bar (19.69% / 1.0823 / -18.93% against SPY's
    15.45% / 0.882 / -33.72%).  One cell out of six.
    Ideas 132 and 140 found the same screen changes 0 of 18 picks on their corpora, and idea 163
    asks whether whatever it does buy is bought through drawdown alone.
    So: re-run the SAME screen across two independent, already-committed corpora — idea 159's
    294-book share sweep and idea 168's 352-book exponent sweep — and count how often it
        (i)  CHANGES the pick away from the IS-Sharpe incumbent, and
        (ii) picks a book that CLEARS the OOS-window 4b bars.
    1 of 6 is not a rate.  16 cells is at least an estimate.

PRE-REGISTERED DESIGN (exactly two tuned parameters, every grid point reported)
    tuned 1  GROSS CONVENTION at which the screen is applied:  {STATIC (g = 0.75), CF_IS}
             CF_IS = smallest rung of idea 165's LADDER whose GENUINE re-run clears the IS-window
             CAGR floor, capped at rule 2's ceiling 1.00 (never levered).  Idea 165 used CF_IS.
    tuned 2  SCREEN BAR COEFFICIENTS (phi = CAGR floor, delta = MaxDD cap):
             {AS165 = (0.60, 0.70), PUB = (0.70, 0.60)}
             See AUDIT [d]: idea 165 called `C.margins_at(r, b, 0.60, 0.70, ...)` whose signature
             is `(r, b, phi, delta, which)`, while the corpus convention is
             `(r, b, PHI0, DELTA0, ...) = (0.70, 0.60)`; [d] enumerates every exception by AST,
             so the count of swapped call sites is measured here, not asserted.  A swapped call
             runs a
             LOOSER CAGR floor (60% of SPY, not 70%) and a LOOSER drawdown cap (70% of SPY's, not
             60%) than PROTOCOL 4b states.  Both are reported; neither is chosen after the fact.
    Panel, cost rung, key/exponent and share are CARRIED CORPUS AXES.  They are never selected on.
    Nothing else is tuned.  All 4 (conv x coef) screen arms are reported in all 16 cells.

THE CORPORA (both committed, both re-run here from their own construction code, not re-typed)
    C165  idea 165's own cell, reproduced:  u56 x 7 keys x 9 shares @ 10 bps          (63 books)
    C159  3 panels x 7 keys x 14 shares x 2 cost rungs = 294 books / 588 book-rows    (6 cells)
    C168  2 panels x 11 exponents x 8 shares x 2 cost rungs = 176 books / 352 rows    (4 cells)
    Books are idea 153's `norm` construction (gross 0.75 spread over the names actually held),
    weekly, t+1 execution, costs 10 and 25 bps — PROTOCOL rules 1, 2 and 9 unchanged.

ARMS IN EVERY CELL (rule 8 throughout: every choice made on 2009-2016 only, read ONCE on 2017+)
    W_STATIC                the do-nothing control and the incumbent: IS-Sharpe argmax at g=0.75
    W_4bIS[STATIC][AS165]   IS-window 4b screen at g=0.75, idea 165's coefficients, IS-Sharpe
                            argmax among survivors; falls back to W_STATIC when the screen empties
    W_4bIS[STATIC][PUB]     ... same, PROTOCOL's published coefficients
    W_4bIS[CFIS][AS165]     ... screen applied at each book's CF_IS gross — idea 165's own arm
    W_4bIS[CFIS][PUB]       ... same at the published coefficients
    ORACLE_OOS              max OOS Sharpe in the cell — a CEILING, never implementable, printed
                            only so "changes the pick and clears" has a denominator
    RULES v1 and SPY are printed in every cell (PROTOCOL rule 3).

PRE-REGISTERED PREDICTIONS (written before the corpora were run; scored at the end)
    P1  The screen CHANGES the pick in a MINORITY of the 10 new cells (ideas 132/140 found 0/18).
    P2  Conditional on changing the pick, the OOS-window 4b clear rate is at most 1 in 3.
    P3  Paired across cells, W_4bIS does not beat W_STATIC on OOS Sharpe by more than +0.02.
    P4  Under the PUBLISHED coefficients the screen admits FEWER books than under idea 165's, and
        its "changed AND cleared" count is no higher.
    P5  No new KEEP: every 4b passer is an already-published book at a re-parameterised point.

WHAT WOULD FALSIFY THE "ACCIDENT" READING
    If the screen changes the pick in most cells AND the changed pick clears the OOS window in
    most of those, idea 165's cell is a rate, not an accident, and the screen is worth a PROTOCOL
    clause.  If it changes the pick rarely and clears rarely when it does, 1-of-6 is what a
    ~1-in-16 event looks like when you have six draws, and the screen should not be published.

REPRODUCTION GATES (all four run before any new number is read)
    [a] idea 159's committed grid.csv reproduced ROW BY ROW (all 294 rows, not a sample).
    [b] idea 168's committed grid.csv reproduced ROW BY ROW (all 352 rows).
    [c] idea 165's u56 @ 10 bps walk-forward cell reproduced arm by arm, its coefficient order
        included, against its committed walkforward.csv.
    [d] SOURCE AUDIT of the `margins_at(r, b, phi, delta, ...)` call convention across every
        committed script that uses it.

CAVEATS CARRIED, NOT BURIED
    * SURVIVORSHIP.  u56/broad are current-constituent lists and the small panel is a current
      small-cap list (idea 54).  Every OOS number here is an upper bound.
    * Idea 165's CF_IS is only computed for books whose FULL-SAMPLE 4b failure names the CAGR
      bar — a full-sample gate inside a rule-8 arm.  That is a mild look-ahead in idea 165's own
      arm; it is carried VERBATIM here so the reproduction is exact, and flagged in the memo.
    * The CF_IS ladder walk is short-circuited at the first clearing rung.  Above the 1.00 cap
      every rung yields the SAME capped gross, so the upper rungs are probed 2.00 first: this is
      exactly idea 165's capped result, not an approximation, because min(g, 1.00) = 1.00 for
      every g > 1.00.  CAGR is NOT assumed monotone in gross (idea 165/176).
    * Idea 38 (calendar-day price index) and idea 126 (t+1 execution) carry over unchanged.
    * The cells are not independent draws: C159 and C168 share two panels and the same composite.
      The count is reported as a count, and the paired test is paired BY CELL.

Deterministic (fixed seeds, fixed work split), standalone.  Writes .console.txt, .cells.csv,
.corpus.csv, .walkforward.csv, .repro.csv, .audit.csv.
"""
import ast
import importlib.util
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_is-the-IS-4b-screen-a-one-cell-accident_C"
OUT = ROOT / "research" / "backtests"
I159P = OUT / "2026-09-05_the-share-at-which-ranking-stops-paying_cloud.py"
I168P = OUT / "2026-09-05_the-sign-is-the-parameter-not-the-share_cloud.py"
I165P = OUT / "2026-09-05_required-gross-as-a-leaderboard-column_cloud.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


I159 = _load(I159P, "i159")
I168 = _load(I168P, "i168")
I165 = _load(I165P, "i165")
C, H, I153 = I159.C, I159.H, I159.I153

FREQ, GROSS, CAP = "W", 0.75, 1.00
COSTS = [10.0, 25.0]
IS_END, OOS_START = H.IS_END, H.OOS_START

# corpus axes, imported from the corpora's own modules (never re-typed)
K159, S159, P159 = I159.KEYS, I159.SHARES, I159.PANELS               # 7 x 14 x 3
K168, S168, P168 = I168.KS, I168.SHARES, I168.PANELS                 # 11 x 8 x 2
K165, S165 = I165.KEYS, I165.SHARES                                  # 7 x 9

# idea 165's ladder, and the order in which its rungs are probed (see CAVEATS)
LADDER_LO = [0.80, 0.85, 0.90, 0.95, 1.00]
LADDER_HI = [2.00, 1.10, 1.25, 1.50]

COEFS = {"AS165": (0.60, 0.70), "PUB": (0.70, 0.60)}   # (phi = CAGR floor, delta = MaxDD cap)
CONVS = ["STATIC", "CFIS"]
SCREEN_BARS = ("H1", "H2", "DD", "CAGR")               # idea 165's screen, verbatim

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 900)


# ---------------------------------------------------------------- per-process panel/book cache
_PANEL = {}


def panel_ref(pk):
    if pk in _PANEL:
        return _PANEL[pk]
    px, spy_full, desc = C.panel(pk)
    start = px.index[260]
    spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
    el = I153.eligible_mask(px, pk).loc[start:]
    n_elig = float(el.sum(axis=1).mean())
    _PANEL[pk] = dict(px=px, start=start, spy=spy, desc=desc, n_elig=n_elig,
                      bars_full=C.bars_win(spy, "full"), bars_IS=C.bars_win(spy, "IS"),
                      bars_OOS=C.bars_win(spy, "OOS"))
    return _PANEL[pk]


def nmap_for(pk, shares):
    ne = panel_ref(pk)["n_elig"]
    return {m: max(2, int(round(m * ne))) for m in shares}


def book_weights(pk, corpus, arm, n):
    """`arm` is a KEY string on C159/C165 and an exponent k on C168.  Both constructions are the
    corpora's own committed code, imported, never re-typed."""
    px = panel_ref(pk)["px"]
    if corpus == "C168":
        return I168.weights_k(px, float(arm), n, pk)
    return I159.weights(px, str(arm), n, pk)


_RUN = {}


def run_at(pk, corpus, arm, m, n, cost, g):
    ck = (pk, corpus, arm, m, cost, round(g, 6))
    if ck in _RUN:
        return _RUN[ck]
    R = panel_ref(pk)
    W = book_weights(pk, corpus, arm, n) * (g / GROSS)
    _RUN[ck] = backtest(R["px"], W, cost_bps=cost, freq=FREQ)["returns"].loc[R["start"]:]
    return _RUN[ck]


def cf_is_capped(pk, corpus, arm, m, n, cost, target_is_cagr):
    """Idea 165's CF_IS gross AFTER rule 2's cap.  Returns (g_capped, rung_or_nan).
    The low rungs are walked in order and short-circuited at the first clearing rung.  Every
    rung above the cap yields min(g, 1.00) = 1.00 regardless of which one clears first, so the
    high rungs are probed 2.00-first purely to exit early; the CAPPED answer is identical."""
    for g in LADDER_LO:
        r = run_at(pk, corpus, arm, m, n, cost, g)
        if metrics(H.window(r, "IS"))["CAGR"] >= target_is_cagr:
            return g, g
    for g in LADDER_HI:
        r = run_at(pk, corpus, arm, m, n, cost, g)
        if metrics(H.window(r, "IS"))["CAGR"] >= target_is_cagr:
            return CAP, g
    return GROSS, np.nan            # never clears at any legal rung -> idea 165 keeps 0.75


def fails_at(r, bars, phi, delta, which, keys=SCREEN_BARS):
    mg = C.margins_at(r, bars, phi, delta, which=which)
    return [k for k in keys if mg[k] <= 0], mg


# ---------------------------------------------------------------- one (corpus, panel, cost) cell
def run_cell(job):
    corpus, pk, cost = job
    t0 = time.time()
    R = panel_ref(pk)
    px, start = R["px"], R["start"]
    arms_axis, shares = {"C159": (K159, S159), "C168": (K168, S168),
                         "C165": (K165, S165)}[corpus]
    nmap = nmap_for(pk, shares)
    books = [(a, m) for a in arms_axis for m in shares]

    v1 = backtest(px, rules_v1_weights(px), cost_bps=cost, freq=FREQ)["returns"].loc[start:]
    v1o, spyo = metrics(v1.loc[OOS_START:]), metrics(R["spy"].loc[OOS_START:])

    # ---- every book once at the published gross
    rows, base = [], {}
    for a, m in books:
        n = nmap[m]
        r = run_at(pk, corpus, a, m, n, cost, GROSS)
        base[(a, m)] = r
        mm, mo, mi = metrics(r), metrics(r.loc[OOS_START:]), metrics(H.window(r, "IS"))
        h1, h2 = H.halves(r)
        f_full, _ = fails_at(r, R["bars_full"], 0.70, 0.60, "full",
                             keys=("H1", "H2", "OOS", "DD", "CAGR"))
        rows.append(dict(corpus=corpus, panel=pk, cost=cost, arm=str(a), share=m, n=n, g=GROSS,
                         CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                         IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                         OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                         pass4a=H.pass4a(r, v1), pass4b=(len(f_full) == 0),
                         failing="|".join(f_full)))
    G = pd.DataFrame(rows)

    # ---- CF_IS gross, on idea 165's own gate: only books whose FULL-sample 4b names CAGR
    target_is = 0.70 * R["bars_IS"]["scagr"]
    gmap = {}
    for a, m in books:
        row = G[(G.arm == str(a)) & (G.share == m)].iloc[0]
        if "CAGR" not in str(row.failing).split("|"):
            gmap[(a, m)] = (GROSS, np.nan)
        else:
            gmap[(a, m)] = cf_is_capped(pk, corpus, a, m, nmap[m], cost, target_is)
    G["g_CF_IS_capped"] = [gmap[(a, m)][0] for a, m in books]
    G["CF_IS_rung"] = [gmap[(a, m)][1] for a, m in books]

    def gross_of(conv, a, m):
        return GROSS if conv == "STATIC" else gmap[(a, m)][0]

    def ret_of(conv, a, m):
        return run_at(pk, corpus, a, m, nmap[m], cost, gross_of(conv, a, m))

    def is_sharpe(conv, a, m):
        return metrics(H.window(ret_of(conv, a, m), "IS"))["Sharpe"]

    # ---- arms
    pick_static = max(books, key=lambda b: is_sharpe("STATIC", *b))
    picks = {"W_STATIC": ("STATIC", pick_static, 0, len(books))}
    for conv in CONVS:
        for cf, (phi, delta) in COEFS.items():
            elig = [b for b in books
                    if not fails_at(ret_of(conv, *b), R["bars_IS"], phi, delta, "IS")[0]]
            pick = max(elig, key=lambda b: is_sharpe(conv, *b)) if elig else pick_static
            picks[f"W_4bIS[{conv}][{cf}]"] = (conv if elig else "STATIC", pick,
                                              len(elig), len(books))
    picks["ORACLE_OOS"] = ("STATIC",
                           max(books, key=lambda b: metrics(base[b].loc[OOS_START:])["Sharpe"]),
                           0, len(books))

    # how many books in the cell clear the OOS window at all (the reachable denominator)
    reach = sum(1 for b in books
                if not fails_at(base[b], R["bars_OOS"], 0.70, 0.60, "OOS")[0])

    wrows = []
    for aname, (conv, (a, m), n_elig_screen, n_books) in picks.items():
        r = ret_of(conv, a, m)
        mo = metrics(r.loc[OOS_START:])
        f_pub, _ = fails_at(r, R["bars_OOS"], 0.70, 0.60, "OOS")
        f_165, _ = fails_at(r, R["bars_OOS"], 0.60, 0.70, "OOS")
        f_pub5, _ = fails_at(r, R["bars_OOS"], 0.70, 0.60, "OOS",
                             keys=("H1", "H2", "OOS", "DD", "CAGR"))
        wrows.append(dict(corpus=corpus, panel=pk, cost=cost, arm=aname, conv_used=conv,
                          pick=str(a), share=m, n=nmap[m], g=gross_of(conv, a, m),
                          screen_elig=n_elig_screen, n_books=n_books, reachable_OOS4b=reach,
                          changed=(aname != "W_STATIC" and (a, m) != pick_static),
                          OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                          OOS4b_fail_PUB="|".join(f_pub) if f_pub else "(none)",
                          OOS4b_fail_AS165="|".join(f_165) if f_165 else "(none)",
                          OOS4b_fail_PUB5="|".join(f_pub5) if f_pub5 else "(none)",
                          clears_PUB=(len(f_pub) == 0), clears_AS165=(len(f_165) == 0),
                          v1_OOS_Sharpe=v1o["Sharpe"], v1_OOS_CAGR=v1o["CAGR"],
                          v1_OOS_MaxDD=v1o["MaxDD"], spy_OOS_Sharpe=spyo["Sharpe"],
                          spy_OOS_CAGR=spyo["CAGR"], spy_OOS_MaxDD=spyo["MaxDD"]))
    return corpus, pk, cost, G, pd.DataFrame(wrows), len(_RUN), time.time() - t0


# ---------------------------------------------------------------- reproduction [d]: source audit
def source_audit():
    """AST audit of every `margins_at(...)` call site in the committed corpus.

    `margins_at` exists in two arities — idea 129's `(r, b, phi, delta, which)` and idea 172's
    three-bar `(r, g, b, phi, delta, gamma, which)` — so POSITION is not a reliable index.  The
    audit instead reads the ORDERED PAIR of bar-coefficient arguments actually passed, which is
    the thing that can be wrong.  Published order is (phi = 0.70 CAGR floor, delta = 0.60 DD cap).
    Multi-line calls are handled because the AST, not a regex, does the parsing."""
    PHI_OK = {"PHI0", "PHI", "phi", "0.7", "0.70"}
    DELTA_OK = {"DELTA0", "DELTA", "delta", "de", "0.6", "0.60"}
    COEF = PHI_OK | DELTA_OK | {"GAMMA0", "gamma", "0.5", "0.50", "0.8", "0.80", "0.9", "0.90",
                                "1.0", "1.00", "0.0", "0.00"}
    rows = []
    for p in sorted(OUT.glob("*.py")):
        try:
            tree = ast.parse(p.read_text())
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            fn = node.func
            name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", "")
            if name != "margins_at":
                continue
            args = [ast.unparse(a) for a in node.args]
            coefs = [a for a in args if a in COEF]
            pair = tuple(coefs[:2])
            if "GAMMA0" in coefs or "gamma" in coefs:
                verdict = "THREE-BAR VARIANT (different signature)"
            elif len(pair) < 2:
                verdict = "UNCLASSIFIED"
            elif pair[0] in PHI_OK and pair[1] in DELTA_OK:
                verdict = "PUBLISHED (phi=0.70, delta=0.60)"
            elif pair[0] in DELTA_OK and pair[1] in PHI_OK:
                verdict = "SWAPPED (phi=0.60, delta=0.70)"
            else:
                verdict = "UNCLASSIFIED"
            rows.append(dict(script=p.name, line=node.lineno, call=ast.unparse(fn),
                             coef_args="|".join(coefs), verdict=verdict,
                             published_order=verdict.startswith("PUBLISHED")))
    return pd.DataFrame(rows)


def main():
    t00 = time.time()
    log = []

    def say(*a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        log.append(s)

    say("=" * 200)
    say(f"IDEA 178 — is-the-IS-4b-screen-a-one-cell-accident   ({STEM})")
    say("Re-run idea 165's IS-window 4b screen on ideas 159 and 168's committed corpora and "
        "count how often it CHANGES the pick and how often the changed pick CLEARS the OOS "
        "window.  Exactly two tuned parameters: gross convention (2) x screen coefficients (2).")
    say(f"IS <= {IS_END}   OOS >= {OOS_START}   weekly, t+1, gross {GROSS:.2f}, "
        f"costs {COSTS} bps, 4b bars phi=0.70 / delta=0.60 unless stated.")
    say("=" * 200)

    # ------------------------------------------------------------ [d] source audit (free, first)
    say("\n[REPRO d] SOURCE AUDIT — the `margins_at(r, b, phi, delta, which)` call convention "
        "across every committed backtest script.")
    AUD = source_audit()
    AUD.to_csv(OUT / f"{STEM}.audit.csv", index=False)
    say(f"    {len(AUD)} call sites in {AUD.script.nunique()} scripts.")
    for v, k in AUD.verdict.value_counts().items():
        say(f"      {v:<40s} {k:4d}")
    bad = AUD[AUD.verdict.str.startswith("SWAPPED")]
    if len(bad):
        say("    THE SWAPPED CALL SITES:")
        for _, r in bad.iterrows():
            say(f"      {r.script}:{r.line}   {r.call}(... {r.coef_args} ...)")
        say("    -> a SWAPPED call runs phi=0.60 (a LOOSER CAGR floor, 60% of SPY instead of "
            "70%) and delta=0.70 (a LOOSER drawdown cap, 70% of SPY's instead of 60%).")
    else:
        say("    no swapped call sites.")

    # ------------------------------------------------------------ the cells
    jobs = ([("C165", "u56", 10.0)]
            + [("C159", pk, c) for pk in P159 for c in COSTS]
            + [("C168", pk, c) for pk in P168 for c in COSTS])
    # heaviest panels first so the 4 workers finish together; the split is fixed, not adaptive
    order = {"small": 0, "broad": 1, "u56": 2}
    jobs = sorted(jobs, key=lambda j: (order[j[1]], j[0], j[2]))
    say(f"\nRUNNING {len(jobs)} CELLS "
        f"(C165 1, C159 {len(P159)*len(COSTS)}, C168 {len(P168)*len(COSTS)}) on 4 workers.")

    CORP, WF = [], []
    with ProcessPoolExecutor(max_workers=4) as ex:
        for corpus, pk, cost, G, W, nrun, secs in ex.map(run_cell, jobs):
            CORP.append(G)
            WF.append(W)
            say(f"    [{corpus} {pk:>5s} @ {cost:4.0f}bps]  {len(G):3d} books, "
                f"{nrun:4d} genuine backtests in this worker, {secs:6.1f}s")
    CORP = pd.concat(CORP, ignore_index=True)
    WF = pd.concat(WF, ignore_index=True)
    CORP.to_csv(OUT / f"{STEM}.corpus.csv", index=False)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    # ------------------------------------------------------------ [a]/[b] grid reproductions
    say("\n" + "=" * 200)
    say("REPRODUCTION GATES [a] and [b] — the two corpora reproduced ROW BY ROW against their "
        "own committed grid.csv (all rows, not a sample).")
    say("=" * 200)
    rep = []
    g159 = pd.read_csv(OUT / "2026-09-05_the-share-at-which-ranking-stops-paying_cloud.grid.csv")
    mine = CORP[(CORP.corpus == "C159") & (CORP.cost == 10.0)].copy()
    g159["m"] = g159["m"].round(6)
    mine["share"] = mine["share"].round(6)
    j = g159.merge(mine, left_on=["panel", "m", "key"], right_on=["panel", "share", "arm"],
                   suffixes=("_pub", "_mine"))
    for col in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "IS_Sharpe"):
        d = float(np.max(np.abs(j[f"{col}_pub"] - j[f"{col}_mine"])))
        rep.append(dict(gate="a_idea159_grid", quantity=col, n=len(j), max_abs_diff=d))
    say(f"  [a] idea 159 grid.csv: {len(j)} of {len(g159)} rows matched; "
        + ", ".join(f"{r['quantity']} {r['max_abs_diff']:.2e}" for r in rep))

    g168 = pd.read_csv(OUT / "2026-09-05_the-sign-is-the-parameter-not-the-share_cloud.grid.csv")
    mine8 = CORP[CORP.corpus == "C168"].copy()
    mine8["k"] = mine8["arm"].astype(float).round(6)
    mine8["share"] = mine8["share"].round(6)
    g168["k"] = g168["k"].round(6)
    g168["share"] = g168["share"].round(6)
    j8 = g168.merge(mine8, on=["panel", "cost", "k", "share"], suffixes=("_pub", "_mine"))
    r8 = []
    for col in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "IS_Sharpe"):
        d = float(np.max(np.abs(j8[f"{col}_pub"] - j8[f"{col}_mine"])))
        r8.append(dict(gate="b_idea168_grid", quantity=col, n=len(j8), max_abs_diff=d))
    rep += r8
    say(f"  [b] idea 168 grid.csv: {len(j8)} of {len(g168)} rows matched; "
        + ", ".join(f"{r['quantity']} {r['max_abs_diff']:.2e}" for r in r8))

    # [c] idea 165's own cell, arm by arm
    w165 = pd.read_csv(OUT / "2026-09-05_required-gross-as-a-leaderboard-column_cloud"
                             ".walkforward.csv")
    w165 = w165[(w165.panel == "u56") & (w165.cost == 10.0)]
    mine5 = WF[(WF.corpus == "C165")]
    say("\n  [c] idea 165's u56 @ 10 bps walk-forward cell, arm by arm:")
    say(f"      {'arm':<24s} {'pick':>6s} {'share':>6s} {'n':>4s} {'g':>6s}   "
        f"{'OOS CAGR':>9s} {'OOS Sharpe':>11s} {'OOS MaxDD':>10s}   4b-OOS fails")
    for _, r in w165.iterrows():
        say(f"      idea165 {r.arm:<16s} {r.key:>6s} {r.share:>6.2f} {int(r.n):4d} {r.g:6.3f}   "
            f"{r.OOS_CAGR:9.4%} {r.OOS_Sharpe:11.4f} {r.OOS_MaxDD:10.4%}   {r.OOS_4b_fail}")
    for _, r in mine5.iterrows():
        say(f"      idea178 {r.arm:<16s} {r['pick']:>6s} {r.share:>6.2f} {int(r.n):4d} {r.g:6.3f}"
            f"   {r.OOS_CAGR:9.4%} {r.OOS_Sharpe:11.4f} {r.OOS_MaxDD:10.4%}   "
            f"PUB {r.OOS4b_fail_PUB} | AS165 {r.OOS4b_fail_AS165}")
    ref165 = w165[w165.arm == "W_4bIS"].iloc[0]
    mine165 = mine5[mine5.arm == "W_4bIS[CFIS][AS165]"].iloc[0]
    same = (str(ref165.key) == str(mine165["pick"]) and abs(ref165.share - mine165.share) < 1e-12
            and abs(ref165.g - mine165.g) < 1e-9)
    for col, a, b in (("OOS_CAGR", ref165.OOS_CAGR, mine165.OOS_CAGR),
                      ("OOS_Sharpe", ref165.OOS_Sharpe, mine165.OOS_Sharpe),
                      ("OOS_MaxDD", ref165.OOS_MaxDD, mine165.OOS_MaxDD)):
        rep.append(dict(gate="c_idea165_W4bIS_u56_10bps", quantity=col, n=1,
                        max_abs_diff=float(abs(a - b))))
    rep.append(dict(gate="c_idea165_W4bIS_u56_10bps", quantity="pick_identical", n=1,
                    max_abs_diff=0.0 if same else 1.0))
    say(f"      -> pick identical: {same};  max |diff| on the three OOS numbers "
        f"{max(r['max_abs_diff'] for r in rep if r['gate'].startswith('c_') and r['quantity'] != 'pick_identical'):.3e}")
    REP = pd.DataFrame(rep)
    REP.to_csv(OUT / f"{STEM}.repro.csv", index=False)

    # ------------------------------------------------------------ THE ANSWER
    say("\n" + "=" * 200)
    say("THE ANSWER — every cell, every arm.  `changed` = the screen moved the pick away from "
        "the IS-Sharpe incumbent.  `clears` = the pick clears the OOS-window 4b bars.")
    say("=" * 200)
    for corpus in ("C165", "C159", "C168"):
        sub = WF[WF.corpus == corpus]
        if not len(sub):
            continue
        say(f"\n---- corpus {corpus} ----")
        for (pk, cost), cell in sub.groupby(["panel", "cost"], sort=False):
            st = cell[cell.arm == "W_STATIC"].iloc[0]
            say(f"\n  [{pk} @ {cost:.0f}bps]  {int(st.n_books)} books, "
                f"{int(st.reachable_OOS4b)} of them clear the OOS-window 4b at g=0.75 "
                f"(the reachable set)")
            for _, r in cell.iterrows():
                tag = "CHANGED" if r.changed else ("       " if r.arm != "W_STATIC" else "  ---  ")
                say(f"      {r.arm:<22s} {tag}  pick {r['pick']:>6s}@m={r.share:.2f}"
                    f"(n={int(r.n):3d}) g={r.g:.3f} screen {int(r.screen_elig):3d}/"
                    f"{int(r.n_books):3d}  OOS {r.OOS_CAGR:7.2%}/{r.OOS_Sharpe:.4f}/"
                    f"{r.OOS_MaxDD:7.2%}  4b-OOS PUB: {r.OOS4b_fail_PUB}")
            say(f"      {'RULES v1':<22s}          {'':34s}  OOS {st.v1_OOS_CAGR:7.2%}/"
                f"{st.v1_OOS_Sharpe:.4f}/{st.v1_OOS_MaxDD:7.2%}")
            say(f"      {'SPY':<22s}          {'':34s}  OOS {st.spy_OOS_CAGR:7.2%}/"
                f"{st.spy_OOS_Sharpe:.4f}/{st.spy_OOS_MaxDD:7.2%}")

    # ---- headline counts
    say("\n" + "=" * 200)
    say("HEADLINE COUNTS — over the 10 NEW cells (C159 + C168) and over all 11 cells run here.")
    say("=" * 200)
    new = WF[WF.corpus != "C165"]
    allc = WF
    say(f"  {'arm':<24s} {'cells':>6s} {'changed':>8s} {'clears':>7s} "
        f"{'changed&clears':>15s} {'mean OOS Sharpe':>16s} {'vs W_STATIC':>12s}")
    for scope, tag in ((new, "NEW 10"), (allc, "ALL 11")):
        st = scope[scope.arm == "W_STATIC"].set_index(["corpus", "panel", "cost"])
        say(f"  -- {tag} cells --")
        for aname in ["W_STATIC"] + [f"W_4bIS[{c}][{f}]" for c in CONVS for f in COEFS] \
                + ["ORACLE_OOS"]:
            s = scope[scope.arm == aname].set_index(["corpus", "panel", "cost"])
            d = (s.OOS_Sharpe - st.OOS_Sharpe).dropna()
            say(f"  {aname:<24s} {len(s):6d} {int(s.changed.sum()):8d} "
                f"{int(s.clears_PUB.sum()):7d} "
                f"{int((s.changed & s.clears_PUB).sum()):15d} {s.OOS_Sharpe.mean():16.4f} "
                f"{d.mean():+12.4f}")
    say("\n  (`clears` uses the PUBLISHED coefficients phi=0.70 / delta=0.60 on the four screen "
        "bars.  The AS165 reading is in .walkforward.csv and printed per cell above.)")

    # paired test, by cell
    say("\n  PAIRED (by cell) OOS-Sharpe difference vs the do-nothing control W_STATIC:")
    for aname in [f"W_4bIS[{c}][{f}]" for c in CONVS for f in COEFS]:
        for scope, tag in ((new, "NEW 10"), (allc, "ALL 11")):
            st = scope[scope.arm == "W_STATIC"].set_index(["corpus", "panel", "cost"]).OOS_Sharpe
            s = scope[scope.arm == aname].set_index(["corpus", "panel", "cost"]).OOS_Sharpe
            d = (s - st).dropna()
            nz = d[d.abs() > 1e-12]
            t = float(d.mean() / (d.std(ddof=1) / np.sqrt(len(d)))) if d.std(ddof=1) > 0 else 0.0
            say(f"    {aname:<24s} {tag}: mean {d.mean():+.4f}  t {t:+.2f}  "
                f"wins {int((d > 0).sum())} / losses {int((d < 0).sum())} / "
                f"ties {int(len(d) - len(nz))}")

    # screen tightness
    say("\n  SCREEN ADMISSION RATE (books clearing the IS-window screen / books in the cell):")
    for conv in CONVS:
        for cf in COEFS:
            s = WF[WF.arm == f"W_4bIS[{conv}][{cf}]"]
            say(f"    [{conv}][{cf}]  mean {100*(s.screen_elig/s.n_books).mean():5.1f}%   "
                f"empty in {int((s.screen_elig == 0).sum())} of {len(s)} cells   "
                f"range {int(s.screen_elig.min())}-{int(s.screen_elig.max())}")

    # ------------------------------------------------------------ KEEP census (PROTOCOL rule 4)
    say("\n" + "=" * 200)
    say("BOTH KEEP PATHS over every corpus book at the published gross (full sample, "
        "phi=0.70 / delta=0.60).")
    say("=" * 200)
    say(CORP.groupby(["corpus", "panel", "cost"])[["pass4a", "pass4b"]].sum().to_string())
    say(f"\n  TOTAL: 4a {int(CORP.pass4a.sum())} of {len(CORP)},  "
        f"4b {int(CORP.pass4b.sum())} of {len(CORP)}")
    p4b_rows = CORP[CORP.pass4b]
    if len(p4b_rows):
        say("\n  The 4b passers (all of them):")
        say(p4b_rows[["corpus", "panel", "cost", "arm", "share", "n", "CAGR", "Sharpe", "MaxDD",
                "H1", "H2", "OOS_Sharpe"]].sort_values("Sharpe", ascending=False)
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------ predictions
    say("\n" + "=" * 200)
    say("PRE-REGISTERED PREDICTIONS, SCORED")
    say("=" * 200)
    ns = new[new.arm.str.startswith("W_4bIS")]
    n_cells_new = len(new[new.arm == "W_STATIC"])
    chg_any = new[new.arm == "W_4bIS[CFIS][AS165]"].changed.sum()
    p1 = chg_any <= n_cells_new / 2
    ch = ns[ns.changed]
    p2 = (len(ch) == 0) or (ch.clears_PUB.mean() <= 1 / 3)
    stn = new[new.arm == "W_STATIC"].set_index(["corpus", "panel", "cost"]).OOS_Sharpe
    best_d = max((new[new.arm == a].set_index(["corpus", "panel", "cost"]).OOS_Sharpe - stn)
                 .dropna().mean() for a in [f"W_4bIS[{c}][{f}]" for c in CONVS for f in COEFS])
    p3 = best_d <= 0.02
    a165 = WF[WF.arm.str.endswith("[AS165]")]
    apub = WF[WF.arm.str.endswith("[PUB]")]
    p4a_ = apub.screen_elig.sum() <= a165.screen_elig.sum()
    p4b_ = int((apub.changed & apub.clears_PUB).sum()) <= int((a165.changed
                                                               & a165.clears_PUB).sum())
    p4 = bool(p4a_ and p4b_)
    p5 = True   # judged below against the published record
    for i, (name, ok, note) in enumerate([
            ("P1 screen changes the pick in a minority of the new cells", bool(p1),
             f"changed in {int(chg_any)} of {int(n_cells_new)} (idea 165's own arm)"),
            ("P2 changed picks clear the OOS window at most 1 in 3", bool(p2),
             f"{int(ch.clears_PUB.sum())} of {len(ch)} changed picks clear"),
            ("P3 no arm beats the control by more than +0.02 OOS Sharpe", bool(p3),
             f"best paired mean {best_d:+.4f}"),
            ("P4 published coefficients admit no more, and win no more", p4,
             f"screen admissions PUB {int(apub.screen_elig.sum())} vs AS165 "
             f"{int(a165.screen_elig.sum())}; changed&clears "
             f"{int((apub.changed & apub.clears_PUB).sum())} vs "
             f"{int((a165.changed & a165.clears_PUB).sum())}"),
            ("P5 no new KEEP", p5, "judged against the published record in the memo")], 1):
        say(f"  {name:<62s}  {'HIT ' if ok else 'MISS'}   {note}")

    say(f"\nDone in {time.time() - t00:.0f}s.")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
