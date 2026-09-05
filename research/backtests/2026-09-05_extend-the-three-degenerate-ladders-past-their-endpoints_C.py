#!/usr/bin/env python3
"""QUEUE idea 218 — extend-the-three-degenerate-ladders-past-their-endpoints  (lane C, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 218)
    "idea 189 found the IS argmax sits on the LAST ladder point in 69-100% of books on GROSS
     (1.00), BAND (0.08) and SLEEVE (0.30), so those three dials answer nothing about fitting.
     Extend each ladder past its endpoint (gross to 1.5 with the leverage caveat stated, band to
     0.15, sleeve to 0.50) and report whether the argmax moves again; idea 187 asks the same
     question of cadence.  If it does, three of idea 171's five verdicts are truncation
     artefacts.  Max 2 params."

WHAT IS ACTUALLY BEING DECIDED.
    Idea 171 ran five dials and idea 189 read three of its five verdicts as "the fit is a
    constant wearing a selector's name": on GROSS/BAND/SLEEVE the IS argmax is the last point of
    the ladder in 94.3%/81.1%/100.0% of the 53 books (SEL-SHARPE), so MODE-LOO minus SEL-SHARPE
    is bounded by 0.0001 and nothing about fitting was measured there.  There are exactly two
    explanations and they have opposite consequences:
      (i)  THE DIAL IS MONOTONE.  IS Sharpe keeps rising past the endpoint.  Then the ladder was
           an arbitrary stopping point, "the argmax is the endpoint" is a fact about the GRID
           and not about the dial, and idea 171's three verdicts are truncation artefacts.  The
           selector is still not choosing anything; it is running to whatever wall we build.
      (ii) THE OPTIMUM IS AT THE ENDPOINT.  Extending the ladder leaves the argmax where it was.
           Then the endpoint concentration is a real property of the dial and idea 189's reading
           stands unqualified.
    This run distinguishes them by BUILDING THE WALL FURTHER OUT.  It is not a search for a
    better book: nothing on a ladder here is a new signal (idea 144).

THE EXTENSIONS — pre-registered, taken from the queue text, not chosen after looking.
    GROSS   0.20..1.00 (idea 171's 10 points)          + 1.10 1.20 1.30 1.40 1.50   -> 15 points
    BAND    0.00..0.08 (idea 171's 5 points)           + 0.10 0.12 0.15             ->  8 points
    SLEEVE  0.00..0.30 (idea 171's 7 points)           + 0.35 0.40 0.45 0.50        -> 11 points
    34 ladder points x 53 books = 1802 ladder rows, every one reported in .ladder.csv.

    ***  THE LEVERAGE CAVEAT, stated as the queue demands and not buried.  ***
    Gross > 1.00 is BORROWING.  products/backtester/engine holds the residual (1 - sum w) as
    cash at ZERO rate, so a gross-1.30 book is financed at 0% in both windows.  That is not a
    tradable assumption in either window and it is flattering in exactly the direction that
    would manufacture this run's headline.  So the GROSS ladder is priced at three financing
    rungs — 0% (the engine's own, i.e. idea 171's convention), 2%/yr and 5%/yr charged daily on
    (gross - 1) — and ALL THREE picks are reported.  The financing rungs are a CONTROL, not a
    tuned parameter: no rung is preferred and no result is read off one alone.

TUNED PARAMETERS — exactly two, per PROTOCOL rule 4.
    1. the SELECTOR, 2 values, both reported, neither preferred: SEL-SHARPE (IS Sharpe argmax)
       and SEL-4B (IS 4b relative min-margin argmax).  Idea 171's two, unchanged.
    2. the LADDER POINT, swept exhaustively (34 points), ALL reported.
    Derived, not tuned: the MODE arms (a count over the selector's own picks), the financing
    rungs (3 fixed values, all reported), CONST (the inherited incumbent), RANDOM (seeded),
    ORACLE (OOS argmax, not implementable, reported as the ceiling).

CORPUS — idea 171/189's 53 books EXACTLY, by importing idea 189's committed script and calling
    its build_corpus() rather than re-typing it: 5 fixed panels (U56, B136, BSTK100, ETF36,
    SMALL484) + 48 sub-panels of B136 (k in {20,40,80} x 16 draws, seed 171500+k).  Books inside
    a family are correlated draws, so the pooled t OVERSTATES significance; per-family tables are
    printed beside every pooled number and the FAMILY count, not the book count, is the honest
    sample size.

WALK-FORWARD (PROTOCOL rule 8).  The design IS the walk-forward: every selector, every mode and
    every financing rung reads the <= 2016-12-31 window only; 2017-01-01..2026 is read once, at
    the end.  .walkforward.csv reports per dial and arm the mean OOS CAGR/Sharpe/MaxDD over the
    53 books and the classic S1 pick, both against RULES v1 and SPY.

REPRODUCTION, asserted before any new number is read
    [a] fast_backtest reproduces products/backtester/engine.backtest to < 1e-12 on returns and
        turnover at all four cadences (idea 189's check_a, called directly).
    [b] at BAND=0 the CAND-n weights equal idea 78's weights_cand exactly (idea 189's check_b).
    [c] the 1166 rows at the 22 ORIGINAL ladder points reproduce idea 189's COMMITTED .ladder.csv
        to < 1e-10 on every numeric column with fail4a/fail4b strings identical, AND the
        truncated pick distributions reproduce its published ones (SEL-SHARPE: GROSS 1.00 in
        50/53, BAND 0.08 in 43/53, SLEEVE 0.30 in 53/53).  Without [c] this is a different
        experiment wearing idea 189's name.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  [a], [b] and [c] all hold.
    P2  SLEEVE: >= 90% of books move PAST 0.30 on the extended ladder.  Its published ladder is
        monotone in Sharpe over all seven points (1.177 -> 1.306 OOS) with turnover falling, so
        0.30 was a wall, not an optimum.
    P3  GROSS at 0% financing: >= 90% of books move past 1.00 (2009-2016 is a bull window and
        leverage is free in the engine).  At 5%/yr financing a MAJORITY of books pick <= 1.00.
    P4  BAND: the new-endpoint (0.15) share under SEL-SHARPE is < 80%, i.e. BELOW its old 81.1%
        at 0.08 — a wider band eventually holds losers, so this dial should show an interior
        optimum where the other two do not.
    P5  At least 2 of the 3 dials have a new-endpoint share > 50%: the degeneracy idea 189 found
        is a truncation artefact, not a resolved optimum.
    P6  The extension does NOT pay out of sample on all three dials: at least one dial has mean
        (SEL-EXT - SEL-TRUNC) OOS Sharpe <= 0.  Running further out on an IS ladder is the same
        act idea 175/189 priced as a loss.
    P7  No new fixed-panel 4b KEEP that is anything but a re-parameterisation of an existing book
        (idea 144).  Expect the SLEEVE extension to buy drawdown and lose the CAGR floor: at
        f=0.30 idea 189 already recorded fail4b=CAGR on U56.

CAVEATS carried, not buried
    * LEVERAGE: see above.  Any gross > 1.00 number at the 0% rung is not tradable.
    * Survivorship: B136, U56 and SMALL484 are current-constituent lists (idea 54).  All arms
      inherit it equally, so the paired comparison is unaffected; the LEVEL of every number is
      not.
    * Idea 144: a re-grossed / re-banded / re-sleeved book is the SAME book.
    * Idea 38 (calendar-day price index after 2014-09-17) and idea 126 (t+1 execution) carry over.
    * The extended endpoints are themselves walls.  If the argmax runs to 1.50 / 0.15 / 0.50 this
      run has moved the truncation, not removed it; that is stated as the finding, not hidden.
    * A sleeve at f=0.50 is half a bond/gold/dollar book.  Idea 190 already killed the static
      sleeve as an ASSET CHOICE (a cash carve-out at matched f reproduces 98.4% of its drawdown
      gain); nothing here revives it.

Deterministic, standalone.  Writes .console.txt, .ladder.csv, .picks.csv, .paired.csv,
.financing.csv, .walkforward.csv, .keep.csv.
"""
import importlib.util
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research" / "backtests"
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))

STEM = "2026-09-05_extend-the-three-degenerate-ladders-past-their-endpoints_C"
PARENT = "2026-09-05_does-any-fitted-dial-beat-its-own-modal-pick_B"

# ---- import idea 189's committed script as a module so the corpus and the book code are ITS code
_spec = importlib.util.spec_from_file_location("idea189", OUT / f"{PARENT}.py")
idea189 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(idea189)

from engine import metrics  # noqa: E402

COST_BPS = idea189.COST_BPS
IS_END = idea189.IS_END
OOS_START = idea189.OOS_START
EPS, PHI, DELTA = idea189.EPS, idea189.PHI, idea189.DELTA

# ---- the three dials: (extended ladder, incumbent, idea 171's old endpoint, old ladder)
ORIG = {
    "GROSS":  [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00],
    "BAND":   [0.00, 0.02, 0.03, 0.05, 0.08],
    "SLEEVE": [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30],
}
ADDED = {
    "GROSS":  [1.10, 1.20, 1.30, 1.40, 1.50],
    "BAND":   [0.10, 0.12, 0.15],
    "SLEEVE": [0.35, 0.40, 0.45, 0.50],
}
DIAL_ORDER = ["GROSS", "BAND", "SLEEVE"]
LADDER = {d: ORIG[d] + ADDED[d] for d in DIAL_ORDER}
INC = {"GROSS": 0.75, "BAND": 0.00, "SLEEVE": 0.00}
OLD_END = {d: ORIG[d][-1] for d in DIAL_ORDER}
NEW_END = {d: LADDER[d][-1] for d in DIAL_ORDER}

FIN_RUNGS = [0.00, 0.02, 0.05]          # annual financing rate charged on (gross - 1)
ARMS = ["CONST", "SEL-TRUNC", "SEL-EXT", "MODE-TRUNC-LOO", "MODE-EXT-LOO", "RANDOM-EXT", "ORACLE-EXT"]

# Book precomputes its eligibility masks over idea189.DIALS["BAND"][0]; widen that list BEFORE
# build_corpus() so the extended band points exist.  Nothing else about idea 189's code changes.
idea189.DIALS["BAND"] = (LADDER["BAND"], INC["BAND"])

fast_backtest = idea189.fast_backtest
halves = idea189.halves
rel_margin = idea189.rel_margin
keep_4a = idea189.keep_4a
keep_4b = idea189.keep_4b
tstat = idea189.tstat
sign_p = idea189.sign_p
modal = idea189.modal

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


idea189.P = P            # idea 189's check_a/check_b print through this run's console log


def fin_adjust(r, gross, rate):
    """Charge `rate`/yr, daily, on the borrowed part of a nominal-gross book.  Zero for gross<=1."""
    if rate == 0.0 or gross <= 1.0:
        return r
    return r - (gross - 1.0) * rate / 252.0


# ---------------------------------------------------------------- reproduction control [c]
def check_c(lad):
    ref = OUT / f"{PARENT}.ladder.csv"
    if not ref.exists():
        P(f"  [c] reference ladder {PARENT}.ladder.csv NOT FOUND -> cannot assert reproduction")
        return False
    a = pd.read_csv(ref)
    a = a[a.dial.isin(DIAL_ORDER)].copy()
    b = lad[lad.point.isin(sum(ORIG.values(), []))].copy()
    b = b[b.apply(lambda r: r["point"] in ORIG[r["dial"]], axis=1)]
    key = ["book", "dial", "point"]
    for f in (a, b):
        f["point"] = f["point"].astype(float).round(6).astype(str)
    a = a.sort_values(key).reset_index(drop=True)
    b = b.sort_values(key).reset_index(drop=True)
    same = len(a) == len(b) and (a[key].values == b[key].values).all()
    P(f"  [c] the {len(b)} ORIGINAL-point rows vs idea 189's committed {PARENT}.ladder.csv:"
      f"  rows {len(b)} vs {len(a)}, keys align={same}")
    if not same:
        return False
    worst, worstcol = 0.0, ""
    for c in ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "turnover", "IS_Sharpe", "IS_margin",
              "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "OOS_margin"]:
        d = float(np.nanmax(np.abs(a[c].values - b[c].values)))
        if d > worst:
            worst, worstcol = d, c
    s4a = float((a["fail4a"].fillna("-") == b["fail4a"].fillna("-")).mean())
    s4b = float((a["fail4b"].fillna("-") == b["fail4b"].fillna("-")).mean())
    P(f"      max|delta| over 12 numeric columns = {worst:.3e} (worst: {worstcol});  "
      f"fail4a identical in {s4a:.1%}, fail4b identical in {s4b:.1%}")
    ok = worst < 1e-10 and s4a == 1.0 and s4b == 1.0
    P(f"      -> {'PASS' if ok else 'FAIL'}")
    return ok


def check_c2(picks_trunc):
    """idea 189's PUBLISHED truncated pick distributions, re-derived here."""
    want = {"GROSS": (1.00, 50), "BAND": (0.08, 43), "SLEEVE": (0.30, 53)}
    ok = True
    P("  [c2] truncated SEL-SHARPE pick distributions vs idea 189's published counts:")
    for d in DIAL_ORDER:
        c = Counter(picks_trunc[(d, "SHARPE")].values())
        pt, n = want[d]
        got = c.get(pt, 0)
        ok &= got == n
        P(f"       {d:7s} endpoint {pt:>5}: {got:2d}/53 books  (idea 189 published {n}/53)  "
          f"{'ok' if got == n else 'MISMATCH'}")
    P(f"       -> {'PASS' if ok else 'FAIL'}")
    return ok


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"IDEA 218 - extend-the-three-degenerate-ladders-past-their-endpoints   (lane C, "
      f"{pd.Timestamp.today().date()})")
    P("=" * 122)
    P("Idea 189: the IS argmax is the LAST ladder point in 94.3%/81.1%/100.0% of books on")
    P("GROSS/BAND/SLEEVE.  Is that the dial, or is it the wall?  Build the wall further out.")
    P(f"Costs {COST_BPS} bps, t+1 execution, IS <= {IS_END}, OOS >= {OOS_START}.")
    P(f"Two tuned params: SELECTOR (2, both reported) x LADDER POINT "
      f"({sum(len(LADDER[d]) for d in DIAL_ORDER)}, all reported).")
    P("LEVERAGE CAVEAT: gross > 1.00 is borrowing and the engine finances it at 0%.  Three")
    P(f"financing rungs reported: {['%.0f%%' % (r*100) for r in FIN_RUNGS]} per year on (gross - 1).")
    P("")
    for d in DIAL_ORDER:
        P(f"  {d:7s} idea 171 ladder {ORIG[d]}  ->  EXTENDED with {ADDED[d]}"
          f"   (incumbent {INC[d]}, old endpoint {OLD_END[d]}, new endpoint {NEW_END[d]})")
    P("")

    books, panels = idea189.build_corpus()
    P(f"CORPUS: {len(books)} books, built by idea 189's own build_corpus() "
      f"({len([b for b in books if not b.name.startswith('B136k')])} fixed panels + "
      f"{len([b for b in books if b.name.startswith('B136k')])} sub-panels, seed {idea189.SEED}+k)")
    P("")

    P("REPRODUCTION CONTROLS [a] and [b] (idea 189's own checks, called directly)")
    okA = idea189.check_a(books[1])
    okB = all(idea189.check_b(b) for b in books[:3])
    if not (okA and okB):
        P("\n*** REPRODUCTION FAILED - this is not a Claude-Space backtest.  Stopping. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return
    P("")

    START, SPY, BASE = {}, {}, {}
    for b in books:
        if b.parent not in SPY:
            px = panels[b.parent]
            st = px.index[260]
            START[b.parent] = st
            SPY[b.parent] = px["SPY"].pct_change().fillna(0.0).loc[st:]
            BASE[b.parent] = fast_backtest(px, idea189.rules_v1_weights(px), COST_BPS, "W")["returns"].loc[st:]
    for k, v in SPY.items():
        m, mo = metrics(v), metrics(v.loc[OOS_START:])
        h1, h2 = halves(v)
        mb = metrics(BASE[k])
        P(f"  benchmark {k:6s} SPY  CAGR {m['CAGR']:6.2%} Sharpe {m['Sharpe']:.3f} MaxDD {m['MaxDD']:7.2%} "
          f"halves {h1:.3f}/{h2:.3f}  OOS Sharpe {mo['Sharpe']:.3f} | RULES v1 Sharpe {mb['Sharpe']:.3f}")
    P("")

    # ------------------------------------------------------------ the extended ladders
    P("RUNNING EXTENDED LADDERS ...")
    rows, fin_rows = [], []
    for bi, bk in enumerate(books):
        st = START[bk.parent]
        spy = SPY[bk.parent].reindex(bk.px.loc[st:].index).fillna(0.0)
        base = BASE[bk.parent].reindex(bk.px.loc[st:].index).fillna(0.0)
        spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
        for dial in DIAL_ORDER:
            for pt in LADDER[dial]:
                kw = dict(gross=INC["GROSS"], n=20, band=INC["BAND"], sleeve=INC["SLEEVE"])
                kw[{"GROSS": "gross", "BAND": "band", "SLEEVE": "sleeve"}[dial]] = pt
                res = fast_backtest(bk.px, bk.weights(**kw), COST_BPS, "W")
                r0 = res["returns"].loc[st:]
                turn = res["turnover"].loc[st:]
                for rate in (FIN_RUNGS if dial == "GROSS" else [0.0]):
                    r = fin_adjust(r0, kw["gross"], rate)
                    r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                    mf, mi, mo = metrics(r), metrics(r_is), metrics(r_oos)
                    mg_is, wb_is = rel_margin(r_is, spy_is)
                    mg_oos, wb_oos = rel_margin(r_oos, spy_oos)
                    h1, h2 = halves(r)
                    rec = dict(
                        book=bk.name, parent=bk.parent, dial=dial, point=pt, fin=rate,
                        is_incumbent=(pt == INC[dial]), is_added=(pt in ADDED[dial]),
                        CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                        turnover=turn.sum() / mf["Years"],
                        IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                        IS_margin=mg_is, IS_worstbar=wb_is,
                        OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                        OOS_margin=mg_oos, OOS_worstbar=wb_oos,
                        fail4a=keep_4a(r, base), fail4b=keep_4b(r, spy, r_oos, spy_oos))
                    if rate == 0.0:
                        rows.append(rec)
                    if dial == "GROSS":
                        fin_rows.append(rec)
        if (bi + 1) % 10 == 0:
            P(f"   ... {bi+1}/{len(books)} books  ({time.time()-t0:.0f}s)")
    lad = pd.DataFrame(rows)
    fin = pd.DataFrame(fin_rows)
    lad.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    fin.to_csv(OUT / f"{STEM}.financing.csv", index=False)
    P(f"   {len(lad)} ladder rows (0% financing) -> {STEM}.ladder.csv")
    P(f"   {len(fin)} GROSS rows across {len(FIN_RUNGS)} financing rungs -> {STEM}.financing.csv"
      f"   ({time.time()-t0:.0f}s)")
    P("")

    # ------------------------------------------------------------ picks
    def argmax_over(sub, col, points):
        s = sub.set_index("point").reindex(points)[col]
        return s.idxmax()

    picks_trunc, picks_ext = {}, {}
    for dial in DIAL_ORDER:
        for sel, col in [("SHARPE", "IS_Sharpe"), ("4B", "IS_margin")]:
            dt, de = {}, {}
            for bk in books:
                sub = lad[(lad.dial == dial) & (lad.book == bk.name)]
                dt[bk.name] = argmax_over(sub, col, ORIG[dial])
                de[bk.name] = argmax_over(sub, col, LADDER[dial])
            picks_trunc[(dial, sel)] = dt
            picks_ext[(dial, sel)] = de

    P("REPRODUCTION CONTROLS [c] and [c2]")
    okC = check_c(lad)
    okC2 = check_c2(picks_trunc)
    if not (okC and okC2):
        P("\n*** [c] FAILED: this is not idea 189's corpus/ladder.  Numbers are written out but no")
        P("*** verdict may be read from them.")
    P("")

    # ------------------------------------------------------------ THE HEADLINE: does the argmax move?
    P("=" * 122)
    P("HEADLINE - DOES THE ARGMAX MOVE WHEN THE WALL MOVES?   (53 books, IS <= 2016 only)")
    P("")
    P(f"  {'dial':7s} {'sel':6s} {'old end':>8s} {'share@old':>10s} {'new end':>8s} {'share@new':>10s} "
      f"{'moved past old':>15s} {'landed interior':>16s} {'ext modal':>10s} {'share':>7s}  verdict")
    census = []
    for dial in DIAL_ORDER:
        for sel in ["SHARPE", "4B"]:
            pt_, pe_ = picks_trunc[(dial, sel)], picks_ext[(dial, sel)]
            n = len(books)
            at_old_t = [b.name for b in books if pt_[b.name] == OLD_END[dial]]
            share_old = len(at_old_t) / n
            share_new = np.mean([pe_[b.name] == NEW_END[dial] for b in books])
            moved = np.mean([pe_[b.name] > OLD_END[dial] for b in books])
            # of the books that WERE at the old endpoint, how many moved past it
            moved_cond = (np.mean([pe_[b] > OLD_END[dial] for b in at_old_t]) if at_old_t else np.nan)
            interior = np.mean([(pe_[b.name] > OLD_END[dial]) and (pe_[b.name] < NEW_END[dial])
                                for b in books])
            mode_e = modal(list(pe_.values()), LADDER[dial])
            share_e = np.mean([v == mode_e for v in pe_.values()])
            verdict = ("TRUNCATION ARTEFACT (runs to the new wall)" if share_new >= 0.5 else
                       "INTERIOR OPTIMUM FOUND" if moved > 0.5 else
                       "endpoint held (old verdict stands)")
            P(f"  {dial:7s} {sel:6s} {OLD_END[dial]:8} {share_old:10.1%} {NEW_END[dial]:8} "
              f"{share_new:10.1%} {moved:15.1%} {interior:16.1%} {str(mode_e):>10s} {share_e:7.1%}  {verdict}")
            census.append(dict(dial=dial, selector=sel, old_end=OLD_END[dial], share_at_old=share_old,
                               new_end=NEW_END[dial], share_at_new=share_new, moved_past_old=moved,
                               moved_past_old_given_was_at_old=moved_cond, landed_interior=interior,
                               ext_mode=mode_e, ext_mode_share=share_e, n=n, verdict=verdict))
    pd.DataFrame(census).to_csv(OUT / f"{STEM}.picks.csv", index=False)
    P("")
    P("  full extended pick distributions:")
    for dial in DIAL_ORDER:
        for sel in ["SHARPE", "4B"]:
            vc = Counter(picks_ext[(dial, sel)].values())
            P(f"    {dial:7s} SEL-{sel:6s} " +
              " ".join(f"{p}:{vc.get(p,0)}" + ("*" if p in ADDED[dial] else "") for p in LADDER[dial]))
    P("   (* = a point that did not exist in idea 171's ladder)")
    P("")

    # ------------------------------------------------------------ ladder shape
    P("=" * 122)
    P("LADDER SHAPE - mean over the 53 books.  If IS keeps rising past the old endpoint the dial is")
    P("monotone and idea 171's ladder was an arbitrary stop; where IS turns over, the wall was real.")
    for dial in DIAL_ORDER:
        g = lad[lad.dial == dial].groupby("point", sort=False)[["IS_Sharpe", "OOS_Sharpe", "OOS_CAGR",
                                                                "OOS_MaxDD", "turnover"]].mean()
        for col, fmt in [("IS_Sharpe", "{:.3f}"), ("OOS_Sharpe", "{:.3f}"),
                         ("OOS_CAGR", "{:.1%}"), ("OOS_MaxDD", "{:.1%}")]:
            P(f"  {dial:7s} {col:10s} " + " ".join(
                f"{p}{'*' if p in ADDED[dial] else ''}:" + fmt.format(g.loc[p, col]) for p in LADDER[dial]))
        s = g["IS_Sharpe"]
        P(f"  {'':7s} IS argmax of the MEAN ladder = {s.idxmax()}"
          f"  (old endpoint {OLD_END[dial]}, new endpoint {NEW_END[dial]});"
          f"  OOS argmax = {g['OOS_Sharpe'].idxmax()}")
        P("")

    # ------------------------------------------------------------ arms and OOS consequence
    rng = np.random.default_rng(218_900)
    choices = []
    for dial in DIAL_ORDER:
        for bk in books:
            sub = lad[(lad.dial == dial) & (lad.book == bk.name)].set_index("point")
            loo_t, loo_e = {}, {}
            for sel, src, dst in [("SHARPE", picks_trunc, loo_t), ("SHARPE", picks_ext, loo_e)]:
                pk = src[(dial, sel)]
                others = [v for k, v in pk.items() if k != bk.name]
                dst["pt"] = modal(others, LADDER[dial])
            pick = {
                "CONST": INC[dial],
                "SEL-TRUNC": picks_trunc[(dial, "SHARPE")][bk.name],
                "SEL-EXT": picks_ext[(dial, "SHARPE")][bk.name],
                "MODE-TRUNC-LOO": loo_t["pt"],
                "MODE-EXT-LOO": loo_e["pt"],
                "RANDOM-EXT": LADDER[dial][int(rng.integers(len(LADDER[dial])))],
                "ORACLE-EXT": sub.reindex(LADDER[dial])["OOS_Sharpe"].idxmax(),
                "SEL-TRUNC-4B": picks_trunc[(dial, "4B")][bk.name],
                "SEL-EXT-4B": picks_ext[(dial, "4B")][bk.name],
            }
            for arm, pt in pick.items():
                r = sub.loc[pt]
                choices.append(dict(dial=dial, book=bk.name, parent=r.parent, arm=arm, point=pt,
                                    IS_Sharpe=r.IS_Sharpe, IS_margin=r.IS_margin,
                                    OOS_Sharpe=r.OOS_Sharpe, OOS_margin=r.OOS_margin,
                                    OOS_CAGR=r.OOS_CAGR, OOS_MaxDD=r.OOS_MaxDD,
                                    fail4a=r.fail4a, fail4b=r.fail4b))
    ch = pd.DataFrame(choices)

    P("=" * 122)
    P("WHAT THE EXTENSION COSTS OR BUYS OUT OF SAMPLE, paired over 53 books.")
    P("Positive = the arm on the left beats the arm on the right.")
    P("")
    paired = []
    for score in ["OOS_Sharpe", "OOS_margin"]:
        P(f"  --- OOS score = {score} " + "-" * 86)
        P(f"  {'dial':7s} {'contrast':34s} {'mean d':>9s} {'median':>9s} {'t':>7s} {'win':>4s} "
          f"{'loss':>5s} {'tie':>4s} {'sign p':>7s}  verdict")
        for dial in DIAL_ORDER:
            for a_arm, b_arm in [("SEL-EXT", "SEL-TRUNC"), ("SEL-EXT-4B", "SEL-TRUNC-4B"),
                                 ("SEL-EXT", "CONST"), ("MODE-EXT-LOO", "SEL-EXT"),
                                 ("MODE-EXT-LOO", "CONST"), ("ORACLE-EXT", "SEL-EXT")]:
                a = ch[(ch.dial == dial) & (ch.arm == a_arm)].set_index("book")[score]
                b = ch[(ch.dial == dial) & (ch.arm == b_arm)].set_index("book")[score]
                d = (a - b).reindex(b.index)
                p, w, l = sign_p(d.values)
                md = d.mean()
                verd = ("LEFT WINS" if (md > 0 and p < 0.05) else
                        "left ahead (n.s.)" if md > 0 else
                        "LEFT LOSES" if p < 0.05 else "left behind (n.s.)")
                if abs(md) < 1e-12:
                    verd = "identical (never differs)"
                P(f"  {dial:7s} {a_arm + ' - ' + b_arm:34s} {md:+9.4f} {d.median():+9.4f} "
                  f"{tstat(d.values):+7.2f} {w:4d} {l:5d} {len(d)-w-l:4d} {p:7.4f}  {verd}")
                paired.append(dict(score=score, dial=dial, arm=a_arm, ref=b_arm, mean_d=md,
                                   median_d=d.median(), t=tstat(d.values), win=w, loss=l,
                                   tie=len(d) - w - l, sign_p=p, n=len(d)))
        P("")
    pdf = pd.DataFrame(paired)
    pdf.to_csv(OUT / f"{STEM}.paired.csv", index=False)

    P("PER-FAMILY (sub-panels of B136 are correlated draws; the FAMILY count is the honest n).")
    P("SEL-EXT minus SEL-TRUNC, OOS Sharpe.")
    P(f"  {'dial':7s} " + " ".join(f"{p:>24s}" for p in ["U56", "B136", "SMALL"]))
    for dial in DIAL_ORDER:
        cells = []
        for par in ["U56", "B136", "SMALL"]:
            a = ch[(ch.dial == dial) & (ch.arm == "SEL-EXT") & (ch.parent == par)].set_index("book")
            b = ch[(ch.dial == dial) & (ch.arm == "SEL-TRUNC") & (ch.parent == par)].set_index("book")
            d = (a["OOS_Sharpe"] - b["OOS_Sharpe"]).reindex(b.index)
            cells.append(f"{d.mean():+.4f} (n{len(d)}, t{tstat(d.values):+.2f})" if len(d) else "n/a")
        P(f"  {dial:7s} " + " ".join(f"{c:>24s}" for c in cells))
    P("")

    # ------------------------------------------------------------ financing control
    P("=" * 122)
    P("THE LEVERAGE CONTROL.  GROSS only.  Does the extension survive paying for the borrowing?")
    P("Financing charged daily on (gross - 1) at a flat annual rate; nominal gross, so this is a")
    P("LOWER BOUND on the true charge (realised gross drifts above nominal between rebalances).")
    P("")
    P(f"  {'rate':>5s} {'IS argmax dist over the 15-point ladder (SEL-SHARPE)':60s} "
      f"{'share>1.00':>11s} {'share@1.50':>11s} {'mean OOS Sharpe of the pick':>28s}")
    fin_summary = []
    for rate in FIN_RUNGS:
        sub_all = fin[fin.fin == rate]
        pk = {}
        for bk in books:
            s = sub_all[sub_all.book == bk.name].set_index("point").reindex(LADDER["GROSS"])
            pk[bk.name] = s["IS_Sharpe"].idxmax()
        vc = Counter(pk.values())
        dist = " ".join(f"{p}:{vc.get(p,0)}" for p in LADDER["GROSS"] if vc.get(p, 0))
        lev = np.mean([v > 1.0 for v in pk.values()])
        top = np.mean([v == 1.50 for v in pk.values()])
        oos = np.mean([sub_all[(sub_all.book == b) & (sub_all.point == pk[b])]["OOS_Sharpe"].iloc[0]
                       for b in pk])
        P(f"  {rate:5.0%} {dist:60s} {lev:11.1%} {top:11.1%} {oos:28.4f}")
        fin_summary.append(dict(rate=rate, share_levered=lev, share_at_1_50=top,
                                mean_OOS_Sharpe_of_pick=oos,
                                mode=modal(list(pk.values()), LADDER["GROSS"])))
        for b, v in pk.items():
            fin_summary[-1].setdefault("picks", {})[b] = v
    P("")
    P("  mean ladder by financing rung (OOS Sharpe):")
    for rate in FIN_RUNGS:
        g = fin[fin.fin == rate].groupby("point", sort=False)["OOS_Sharpe"].mean()
        P(f"    {rate:5.0%}  " + " ".join(f"{p}:{g.loc[p]:.3f}" for p in LADDER["GROSS"]))
    P("  mean ladder by financing rung (OOS CAGR):")
    for rate in FIN_RUNGS:
        g = fin[fin.fin == rate].groupby("point", sort=False)["OOS_CAGR"].mean()
        P(f"    {rate:5.0%}  " + " ".join(f"{p}:{g.loc[p]:.1%}" for p in LADDER["GROSS"]))
    P("  mean ladder by financing rung (OOS MaxDD):")
    for rate in FIN_RUNGS:
        g = fin[fin.fin == rate].groupby("point", sort=False)["OOS_MaxDD"].mean()
        P(f"    {rate:5.0%}  " + " ".join(f"{p}:{g.loc[p]:.1%}" for p in LADDER["GROSS"]))
    P("")

    # ------------------------------------------------------------ rule 8 walk-forward
    P("=" * 122)
    P("PROTOCOL RULE 8 WALK-FORWARD.  Every arm chose on IS only; OOS is read once, here.")
    P("(i) mean OOS metrics across the 53 books, per dial and arm")
    P(f"  {'dial':7s} {'arm':16s} {'OOS CAGR':>9s} {'OOS Shrp':>9s} {'OOS MaxDD':>10s} "
      f"{'OOS margin':>11s} {'OOS-4b pass':>12s}")
    wf = []
    for dial in DIAL_ORDER:
        for arm in ARMS:
            a = ch[(ch.dial == dial) & (ch.arm == arm)]
            npass = int((a["OOS_margin"] > 0).sum())
            P(f"  {dial:7s} {arm:16s} {a.OOS_CAGR.mean():9.2%} {a.OOS_Sharpe.mean():9.3f} "
              f"{a.OOS_MaxDD.mean():10.2%} {a.OOS_margin.mean():+11.4f} {npass:6d}/{len(a)}")
            wf.append(dict(kind="mean_over_books", dial=dial, arm=arm, OOS_CAGR=a.OOS_CAGR.mean(),
                           OOS_Sharpe=a.OOS_Sharpe.mean(), OOS_MaxDD=a.OOS_MaxDD.mean(),
                           OOS_margin=a.OOS_margin.mean(), oos4b_pass=npass, n=len(a)))
    P("")
    P("  pooled over the three dials:")
    for arm in ARMS:
        a = ch[ch.arm == arm]
        P(f"    {arm:16s} OOS CAGR {a.OOS_CAGR.mean():7.2%}  OOS Sharpe {a.OOS_Sharpe.mean():.4f}  "
          f"OOS MaxDD {a.OOS_MaxDD.mean():7.2%}")
        wf.append(dict(kind="pooled", dial="ALL", arm=arm, OOS_CAGR=a.OOS_CAGR.mean(),
                       OOS_Sharpe=a.OOS_Sharpe.mean(), OOS_MaxDD=a.OOS_MaxDD.mean(),
                       OOS_margin=a.OOS_margin.mean(), oos4b_pass=int((a.OOS_margin > 0).sum()), n=len(a)))
    for k in SPY:
        so, bo = SPY[k].loc[OOS_START:], BASE[k].loc[OOS_START:]
        ms, mb = metrics(so), metrics(bo)
        P(f"    {'SPY/'+k:16s} OOS CAGR {ms['CAGR']:7.2%}  OOS Sharpe {ms['Sharpe']:.4f}  "
          f"OOS MaxDD {ms['MaxDD']:7.2%}")
        P(f"    {'RULESv1/'+k:16s} OOS CAGR {mb['CAGR']:7.2%}  OOS Sharpe {mb['Sharpe']:.4f}  "
          f"OOS MaxDD {mb['MaxDD']:7.2%}")
        wf.append(dict(kind="benchmark", dial="-", arm=f"SPY/{k}", OOS_CAGR=ms["CAGR"],
                       OOS_Sharpe=ms["Sharpe"], OOS_MaxDD=ms["MaxDD"]))
        wf.append(dict(kind="benchmark", dial="-", arm=f"RULESv1/{k}", OOS_CAGR=mb["CAGR"],
                       OOS_Sharpe=mb["Sharpe"], OOS_MaxDD=mb["MaxDD"]))
    P("")
    P("(ii) the classic S1 pick: within each dial+arm, the single book with the best IS Sharpe, read once OOS")
    P(f"  {'dial':7s} {'arm':16s} {'book':11s} {'point':>6s} {'OOS CAGR':>9s} {'OOS Shrp':>9s} "
      f"{'OOS MaxDD':>10s}  vs SPY / RULES v1")
    for dial in DIAL_ORDER:
        for arm in ARMS:
            a = ch[(ch.dial == dial) & (ch.arm == arm)]
            r = a.loc[a["IS_Sharpe"].idxmax()]
            ms, mb = metrics(SPY[r.parent].loc[OOS_START:]), metrics(BASE[r.parent].loc[OOS_START:])
            P(f"  {dial:7s} {arm:16s} {r.book:11s} {str(r.point):>6s} {r.OOS_CAGR:9.2%} "
              f"{r.OOS_Sharpe:9.3f} {r.OOS_MaxDD:10.2%}   SPY {ms['Sharpe']:.3f} / v1 {mb['Sharpe']:.3f}"
              f"   {'beats both' if r.OOS_Sharpe > max(ms['Sharpe'], mb['Sharpe']) else 'does not beat both'}")
            wf.append(dict(kind="S1_pick", dial=dial, arm=arm, book=r.book, point=r.point,
                           OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                           spy_OOS_Sharpe=ms["Sharpe"], v1_OOS_Sharpe=mb["Sharpe"]))
    pd.DataFrame(wf).to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P("")

    # ------------------------------------------------------------ both KEEP paths
    P("=" * 122)
    P(f"BOTH KEEP PATHS (PROTOCOL rule 4), evaluated on all {len(lad)} ladder rows (0% financing)")
    n4a = int((lad.fail4a == "-").sum())
    n4b = int((lad.fail4b == "-").sum())
    sub_mask = lad.book.str.startswith("B136k")
    P(f"  4a (beat the book):  {n4a}/{len(lad)} rows pass")
    P(f"  4b (capital-worthy): {n4b}/{len(lad)} rows pass "
      f"({int(((lad.fail4b=='-') & sub_mask).sum())} of them on sub-panels, a corpus device and NOT "
      f"tradable books)")
    added = lad[lad.is_added]
    P(f"  on the ADDED points only: 4a {int((added.fail4a=='-').sum())}/{len(added)}, "
      f"4b {int((added.fail4b=='-').sum())}/{len(added)}")
    bars = pd.Series([b for s in lad.fail4b for b in s.split(",") if b != "-"]).value_counts()
    P(f"  4b binding bars across all failing rows: {dict(bars)}")
    bars_a = pd.Series([b for s in added.fail4b for b in s.split(",") if b != "-"]).value_counts()
    P(f"  4b binding bars on the ADDED points:     {dict(bars_a)}")
    small = lad[lad.parent == "SMALL"]
    P(f"  SMALL484 rows passing 4b: {int((small.fail4b=='-').sum())}/{len(small)}  (idea 136)")
    kfixed = lad[(lad.fail4b == "-") & (~sub_mask)]
    if len(kfixed):
        P("  4b-passing rows on the FIXED (tradable) panels:")
        P("    " + kfixed[["book", "dial", "point", "is_added", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                           "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "turnover"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}").replace("\n", "\n    "))
        P("  NOTE (idea 144): every one is a re-parameterisation of an EXISTING book, not a new")
        P("  signal.  None is proposed.  This run is a methodology test.")
    else:
        P("  no fixed-panel row passes 4b.")
    P("")
    P("  arm-level 4b (fixed panels only):")
    for arm in ARMS:
        a = ch[(ch.arm == arm) & (~ch.book.str.startswith("B136k"))]
        P(f"    {arm:16s} {int((a.fail4b=='-').sum()):2d}/{len(a)} arm-cells pass 4b")
    lad[["book", "dial", "point", "is_added", "fail4a", "fail4b", "CAGR", "Sharpe", "MaxDD",
         "H1", "H2", "OOS_Sharpe"]].to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P("")

    # ------------------------------------------------------------ named-book view
    P("=" * 122)
    P("NAMED-BOOK VIEW.  U56 is the live book's panel.  Each extended ladder in full.")
    for bkname in ["U56"]:
        par = next(b.parent for b in books if b.name == bkname)
        ms = metrics(SPY[par])
        s1b, s2b = halves(SPY[par])
        mso = metrics(SPY[par].loc[OOS_START:])
        P(f"  SPY(full) CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} halves {s1b:.3f}/{s2b:.3f} "
          f"MaxDD {ms['MaxDD']:.2%} -> 4b bars: H1>{s1b:.3f} H2>{s2b:.3f} OOS>{mso['Sharpe']:.3f} "
          f"|DD|<={DELTA*abs(ms['MaxDD']):.2%} CAGR>={PHI*ms['CAGR']:.2%}")
        for dial in DIAL_ORDER:
            pk = ch[(ch.dial == dial) & (ch.book == bkname)].set_index("arm")["point"]
            P(f"    {dial}: incumbent {INC[dial]} | SEL-TRUNC {pk['SEL-TRUNC']} | "
              f"SEL-EXT {pk['SEL-EXT']} | MODE-EXT-LOO {pk['MODE-EXT-LOO']} | oracle {pk['ORACLE-EXT']}")
            d = lad[(lad.book == bkname) & (lad.dial == dial)]
            P("      " + d[["point", "is_added", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
                            "OOS_CAGR", "OOS_MaxDD", "turnover", "fail4a", "fail4b"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}").replace("\n", "\n      "))
        P("")

    # ------------------------------------------------------------ predictions scorecard
    P("=" * 122)
    P("PREDICTIONS SCORECARD (all written before any number above was read)")
    cen = pd.DataFrame(census).set_index(["dial", "selector"])
    p2 = cen.loc[("SLEEVE", "SHARPE"), "moved_past_old"] >= 0.90
    p3a = np.mean([v > 1.0 for v in fin_summary[0]["picks"].values()]) >= 0.90
    p3b = np.mean([v <= 1.0 for v in fin_summary[-1]["picks"].values()]) > 0.50
    p4 = cen.loc[("BAND", "SHARPE"), "share_at_new"] < 0.80
    p5 = int(sum(cen.loc[(d, "SHARPE"), "share_at_new"] > 0.50 for d in DIAL_ORDER)) >= 2
    ext_d = {d: pdf[(pdf.score == "OOS_Sharpe") & (pdf.dial == d) & (pdf.arm == "SEL-EXT")
                    & (pdf.ref == "SEL-TRUNC")].mean_d.iloc[0] for d in DIAL_ORDER}
    p6 = any(v <= 0 for v in ext_d.values())
    P(f"  P1 reproduction [a]+[b]+[c]+[c2]              : {'HIT' if (okA and okB and okC and okC2) else 'MISS'}")
    P(f"  P2 SLEEVE moves past 0.30 in >= 90% of books  : {'HIT' if p2 else 'MISS'}"
      f"  ({cen.loc[('SLEEVE','SHARPE'),'moved_past_old']:.1%})")
    P(f"  P3a GROSS@0% moves past 1.00 in >= 90%        : {'HIT' if p3a else 'MISS'}"
      f"  ({np.mean([v > 1.0 for v in fin_summary[0]['picks'].values()]):.1%})")
    P(f"  P3b GROSS@5% picks <= 1.00 in > 50%           : {'HIT' if p3b else 'MISS'}"
      f"  ({np.mean([v <= 1.0 for v in fin_summary[-1]['picks'].values()]):.1%})")
    P(f"  P4 BAND new-endpoint share < 80%              : {'HIT' if p4 else 'MISS'}"
      f"  ({cen.loc[('BAND','SHARPE'),'share_at_new']:.1%} at 0.15 vs 81.1% at 0.08)")
    P(f"  P5 >= 2 of 3 dials run to the NEW wall        : {'HIT' if p5 else 'MISS'}"
      f"  (shares@new: " + ", ".join(f"{d} {cen.loc[(d,'SHARPE'),'share_at_new']:.1%}" for d in DIAL_ORDER) + ")")
    P(f"  P6 extension fails to pay OOS on >= 1 dial    : {'HIT' if p6 else 'MISS'}"
      f"  (mean d: " + ", ".join(f"{d} {v:+.4f}" for d, v in ext_d.items()) + ")")
    P(f"  P7 no new fixed-panel 4b KEEP beyond re-params: "
      f"{'HIT (none)' if len(kfixed)==0 else 'see note'}  ({len(kfixed)} fixed-panel 4b rows, "
      f"{int(kfixed.is_added.sum()) if len(kfixed) else 0} of them on ADDED points)")
    P("")
    P(f"done in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
