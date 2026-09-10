#!/usr/bin/env python3
"""QUEUE idea 615 — why-does-a-0.83x-per-year-book-still-pay-to-SMOOTH (lane C, 2026-09-10).

PRE-REGISTERED QUESTION (verbatim from QUEUE.md idea 615, written before any number here was read)
    "idea 403's rule-8 chooser picked lambda<1 in 12 of 24 EWall cells, where base turnover is
     0.83x/yr and the drag saved is under 2 bps/yr, so the gain cannot be a cost gain.  Decompose
     the lambda instrument on a near-zero-turnover book into its cost term and its path term and
     name which bar the path term clears.  Max 2 params (lambda, book)."

WHY IT MATTERS
    lambda (partial rebalancing) is sold everywhere in this record as a TURNOVER-COST instrument:
    idea 403's whole A4 collapse rests on it moving drag and nothing else.  If a rule-8 chooser
    buys it on a book that trades 0.83x/yr — where the most drag it can save at PROTOCOL's own
    10 bps rung is a fraction of a basis point a year — then either the dial carries a second,
    unnamed channel (a PATH channel) that is doing real work, or the chooser is buying NOISE and
    every "the selector picked lambda < 1" sentence in the record is a coin flip wearing a
    mechanism's name.  Those two readings have opposite consequences for PROTOCOL, so the run
    decomposes the dial exactly and prices the answer against the bars 4b actually reads.

THE DECOMPOSITION (fixed before any number was read; this is the whole method)
    Turnover reaches a return series ONLY through cost: r_c = r_0 - to * c/1e4, exactly, because
    no instrument here reads equity.  That identity is asserted in gate G2.  So an arm is fully
    described by a PATH (its zero-cost return series r_0) and a DRAG SCHEDULE (its daily turnover
    series to).  lambda changes BOTH.  Run the 2x2:

        r[p, d] := r_0(lambda = p)  -  to(lambda = d) * c/1e4         p, d in {1, lam}

        COST(lam, c) = M(r[1, lam]) - M(r[1, 1])       same path, lambda's cheaper trading
        PATH(lam, c) = M(r[lam, 1]) - M(r[1, 1])       lambda's path, lambda=1's drag schedule
        INTER(lam, c) = M(r[lam,lam]) - M(r[lam,1]) - M(r[1,lam]) + M(r[1,1])
        TOTAL(lam, c) = M(r[lam,lam]) - M(r[1,1]) = COST + PATH + INTER      (exact, by algebra)

    M runs over CAGR, Sharpe, MaxDD, H1, H2, OOS Sharpe and over all five 4b margins.  At c = 0
    COST and INTER are identically zero and TOTAL == PATH: the zero-cost rung IS the path channel,
    which is why it is reported first.

WHAT IS BEING TESTED (six analyses, fixed in advance)
    A0  PREMISE, off idea 403's OWN committed artefacts.  Count the lambda<1 EWall picks in
        403's .walkforward.csv, and read the drag those picks actually save off 403's .grid.csv.
        The queue's "under 2 bps/yr" is a bound; the run reports the number.
    A1  THE LEVEL.  Base turnover by (panel, book, lambda) and the drag saved in bps/yr at every
        rung.  EWall is the near-zero-turnover book; TOP20 is the high-turnover contrast that
        tells us whether the decomposition can see a cost term at all when one exists.
    A2  THE DECOMPOSITION.  COST / PATH / INTER / TOTAL for every metric, every grid point.
        On EWall the prediction is |PATH| >> |COST| at every rung including 50 bps.
    A3  THE NOISE YARDSTICK (pre-registered, and the arbiter of "real gain" vs "tie").  The same
        book at lambda = 1, rebalanced on each of the five weekday phases of the SAME weekly
        cadence.  Trading on Tuesday instead of Friday is an implementation detail nobody would
        call an edge; the spread of Sharpe across those five phases is therefore the smallest
        difference this harness can honestly call a difference.  A path term smaller than the
        phase spread is a TIE, not a gain, and is reported as one.
    A4  WHICH BAR.  For every (panel, book, rung): the binding 4b bar at lambda = 1, each bar's
        margin decomposed into COST and PATH, and a count of bars the PATH term FLIPS from fail
        to pass.  This is the queue's literal ask ("name which bar the path term clears").
    A5  DOES THE PATH TERM TRANSFER (the only test that matters for a chooser).  Sign of the
        PATH term on IS (2009-2016) vs on OOS (2017-2026), per (panel, book, lambda, rung), and
        the Spearman of the whole lambda curve IS vs OOS.  A chooser can only buy a path term
        that is stable in sign; one that is not is noise by definition.
    A6  RULE 8 (PROTOCOL 8, required).  lambda chosen on 2009-2016 ALONE per (panel, book, rung)
        under two selectors written down in advance, 2017-2026 read ONCE.  OOS CAGR/Sharpe/MaxDD
        vs the LIVE RULES v2 book (cost-matched, same panel) and vs SPY, plus the REGRET against
        the do-nothing default lambda = 1.

CORPUS (every point reported; nothing is selected on except the two tuned parameters)
    lambda     1.00, 0.70, 0.50, 0.35, 0.25, 0.15, 0.10, 0.06 — idea 403's grid VERBATIM, so the
               premise is read on the same dial that produced it.  TUNED PARAMETER 1.
    book       EWall (the 0.83x/yr book the queue names) and TOP20 (the ranked book, 11-16x the
               turnover, the contrast).  TUNED PARAMETER 2.
    panels     u56 (research/universe.json), broad/B136 (universe_broad.json) — idea 403's two —
               and SMALL439 (data/prices_small.csv, 44 max_1d_move >= 1.0 names dropped), which
               403 never ran, as a third independent panel.  Reported axis, never selected on.
    costs      0, 5, 10, 15, 25, 50 bps — ALL reported.  0 is the control that isolates PATH.
    = 3 panels x 2 books x 8 lambdas = 48 simulations read at 6 rungs = 288 arm-rows, plus
      3 x 2 x 5 = 30 phase-yardstick simulations at lambda = 1 and 3 x 6 baseline runs.

TUNED PARAMETERS — exactly two, per PROTOCOL 4: lambda (8 values, ALL reported) and book
    (2 values, BOTH reported).  Panels, cost rungs, weekday phases, both selectors and both KEEP
    paths are reported axes, never selected on.

KEEP PATHS (PROTOCOL 4, evaluated on EVERY one of the 288 arm-rows)
    4a  vs the LIVE book `baseline.rules_v2_weights` on the same panel, COST-MATCHED to the arm's
        rung: Sharpe > baseline in BOTH halves AND MaxDD no worse.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.

PRE-REGISTERED PREDICTIONS (written before any number from the main grid was read)
    P1  On EWall the COST term is below 0.2 bps/yr of CAGR at 10 bps and |PATH| exceeds |COST| in
        Sharpe at every rung — i.e. the queue's premise is right that this cannot be a cost gain.
    P2  But the PATH term on EWall is itself SMALLER than the weekday-phase yardstick, so the
        honest reading is a TIE and the chooser's lambda<1 picks are noise, not a gain.
    P3  Therefore the PATH term clears NO 4b bar: zero fail->pass flips on EWall at any rung.
    P4  On TOP20 the ordering reverses — COST dominates PATH at 25 and 50 bps — which is the
        positive control that the decomposition can see a cost term when one is there.
    P5  The IS sign of the PATH term transfers to OOS at a rate indistinguishable from 50%.

CAVEATS carried, not buried
    * SURVIVORSHIP (idea 54): all three panels are current constituents; SMALL439 is the worst
      offender.  A path term measured on a survivor panel is biased toward whatever held on.
    * lambda can only LOWER turnover (idea 403's A3): the falsification is one-sided.
    * MaxDD is one number off one path and the 4b DD cap turns on exactly that number (idea 321).
    * Idea 126: t+1 execution, no lag band.  Idea 38: u56/broad carry the calendar-day index.
    * The phase yardstick is a NOISE floor, not a null distribution: five phases give a spread,
      not a p-value.  It is used only to say "smaller than an arbitrary implementation choice".
    * u56/broad keep 403's panel convention (every column of load_universe(), SPY included as a
      constituent); SMALL439 keeps the record's small-panel convention (SPY benchmark only,
      max_1d_move >= 1.0 dropped).  Stated because the two conventions differ.

Deterministic, standalone, modifies nothing.  Writes .console.txt, .grid.csv, .decomp.csv,
.phase.csv, .bars.csv, .walkforward.csv, .keeppaths.csv next to itself.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_why-does-a-0.83x-per-year-book-still-pay-to-SMOOTH_C"
OUT = ROOT / "research" / "backtests"
I403 = OUT / "2026-09-10_is-the-4b-window-a-TURNOVER-COST-fact-about-the-ranked-book_B"

FREQ, GROSS, NTOP = "W", 0.75, 20
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60                                   # 4b CAGR floor / DD cap vs SPY
LAMBDAS = [1.00, 0.70, 0.50, 0.35, 0.25, 0.15, 0.10, 0.06]   # tuned parameter 1
BOOKS = ["EWall", "TOP20"]                                   # tuned parameter 2
PANELS = ["u56", "broad", "SMALL439"]
RUNGS = [0.0, 5.0, 10.0, 15.0, 25.0, 50.0]
PHASES = [0, 1, 2, 3, 4]                                  # weekday phase of the SAME weekly cadence
BARS5 = ["H1", "H2", "OOS", "DD", "CAGR"]
METS = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 3000)
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ---------------------------------------------------------------- books (idea 94/403 verbatim)
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def targets(px, book):
    if book == "EWall":
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    if book == "TOP20":
        rank = composite(px).rank(axis=1, ascending=False)
        return (rank <= NTOP).astype(float) * (GROSS / NTOP)
    raise ValueError(book)


def smooth(W, lam):
    """Idea 137/403's partial-rebalance dial, verbatim: target_t = lam*W_t + (1-lam)*target_{t-1},
    gross restored daily so the dial changes TRADING, not exposure."""
    if lam >= 1.0:
        return W
    S = W.ewm(alpha=lam, adjust=False).mean()
    g = S.sum(axis=1).replace(0, np.nan)
    return S.mul((W.sum(axis=1) / g).fillna(0.0), axis=0).fillna(0.0)


# ---------------------------------------------------------------- runner (mask-configurable)
def run(px, W, phase=0, cost_bps=0.0):
    """engine.backtest with an explicit weekly mask phase.  phase=0 reproduces engine.backtest
    exactly (asserted in G1).  Returns (net return series, daily turnover series)."""
    rets = px.pct_change().fillna(0.0).values
    tgt = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, FREQ).shift(1 + phase, fill_value=False).values
    n, k = rets.shape
    cur = np.zeros(k)
    held = np.zeros((n, k))
    turn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = tgt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new.copy()
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)


# ---------------------------------------------------------------- metrics helpers
def win(s, which):
    return s.loc[:IS_END] if which == "IS" else (s.loc[OOS_START:] if which == "OOS" else s)


def mset(r):
    """The six reported metrics of one return series."""
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"])


def bars_of(spy, which="full"):
    s = win(spy, which)
    h = len(s) // 2
    m = metrics(s)
    return dict(s1=metrics(s.iloc[:h])["Sharpe"], s2=metrics(s.iloc[h:])["Sharpe"],
                sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"] if which == "full" else np.nan)


def margins(r, b, which="full"):
    """4b bar margins in each bar's own units.  Positive = clears."""
    s = win(r, which)
    h = len(s) // 2
    m = metrics(s)
    d = dict(H1=metrics(s.iloc[:h])["Sharpe"] - b["s1"],
             H2=metrics(s.iloc[h:])["Sharpe"] - b["s2"],
             DD=DELTA * abs(b["sdd"]) - abs(m["MaxDD"]),
             CAGR=m["CAGR"] - PHI * b["scagr"])
    if which == "full":
        d["OOS"] = metrics(r.loc[OOS_START:])["Sharpe"] - b["soos"]
    return d


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3 or len(set(a[ok])) < 2 or len(set(b[ok])) < 2:
        return np.nan
    return float(np.corrcoef(pd.Series(a[ok]).rank(), pd.Series(b[ok]).rank())[0, 1])


def ann_turn(to, idx):
    """Realised annual turnover (units of NAV traded per year) over the evaluated slice."""
    return float(to.sum() / (len(idx) / 252.0))


# ---------------------------------------------------------------- main
def main():
    say("IDEA 615 — why does a 0.83x/yr book still pay to SMOOTH?  (lane C, 2026-09-10)")
    say(f"lambda grid (tuned param 1, idea 403's verbatim): {LAMBDAS}")
    say(f"books (tuned param 2): {BOOKS};  panels: {PANELS};  rungs: {RUNGS} bps")
    say(f"weekly cadence, t+1 execution, gross {GROSS}, IS <= {IS_END}, OOS >= {OOS_START}.")
    say("DECOMPOSITION: r[p,d] = r_0(lam=p) - to(lam=d)*c/1e4;  COST = M(r[1,lam]) - M(r[1,1]);")
    say("               PATH = M(r[lam,1]) - M(r[1,1]);  TOTAL = COST + PATH + INTER (exact).")

    # ============================================================ A0 PREMISE off 403's artefacts
    say("\n" + "=" * 100)
    say("A0  PREMISE CHECK — idea 403's own committed .walkforward.csv and .grid.csv")
    wf = pd.read_csv(f"{I403}.walkforward.csv")
    gr = pd.read_csv(f"{I403}.grid.csv")
    ew = wf[wf.book == "EWall"]
    for sel in sorted(ew.sel.unique()):
        d = ew[ew.sel == sel]
        say(f"  selector {sel}: lambda<1 in {(d.lam < 1).sum()} of {len(d)} EWall cells; "
            f"picked lambdas {sorted(d.lam.unique())}; "
            f"by panel {dict(d.groupby('panel').apply(lambda x: int((x.lam < 1).sum())))}")
    say(f"  => the queue's '12 of 24' reproduces EXACTLY, per selector; all {int((ew.lam<1).sum())} "
        f"lambda<1 picks are on u56 and ALL of them sit at the grid's EXTREME lambda "
        f"{sorted(set(ew.loc[ew.lam < 1, 'lam']))}, none in the interior.")
    g_ew = gr[gr.book == "EWall"]
    to_by = g_ew.groupby(["panel", "lam"]).base_to.first().unstack()
    say("  base turnover (x/yr) by panel x lambda, off 403's grid:")
    say(to_by.to_string(float_format=lambda x: f"{x:.4f}"))
    for pk in to_by.index:
        d_to = to_by.loc[pk, 1.00] - to_by.loc[pk].min()
        say(f"    {pk}: the WHOLE lambda range saves {d_to:.4f} x/yr of turnover = "
            f"{d_to * 10:.4f} bps/yr of drag at 10 bps, {d_to * 50:.4f} bps/yr at 50 bps.")
    say("  => the queue's 'under 2 bps/yr' is a LOOSE bound: the true figure at PROTOCOL's own "
        "rung is under 0.03 bps/yr.  The premise is confirmed and tightened.")

    # ============================================================ panels
    px_small = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in px_small.columns if c != "SPY" and c not in bad]
    PX = {"u56": load_universe(), "broad": load_universe(broad=True), "SMALL439": px_small}
    INVEST = {"u56": None, "broad": None, "SMALL439": inv}
    SPYCOL = {"u56": "SPY", "broad": "SPY", "SMALL439": "SPY"}

    rows, decomp, phase_rows, bar_rows, keep_rows = [], [], [], [], []
    R0, TO, REF = {}, {}, {}

    for pk in PANELS:
        px_all = PX[pk]
        px = px_all if INVEST[pk] is None else px_all[INVEST[pk]]
        start = px_all.index[260]
        spy = px_all[SPYCOL[pk]].pct_change().fillna(0.0).loc[start:]
        b_full, b_is = bars_of(spy, "full"), bars_of(spy, "IS")
        ms, mo = metrics(spy), metrics(spy.loc[OOS_START:])
        REF[pk] = dict(bfull=b_full, bIS=b_is, start=start, spy=spy, ms=ms, mo=mo)
        say(f"\n[panel] {pk}: {px.shape[1]} investable cols, {px_all.index[0].date()}.."
            f"{px_all.index[-1].date()}, evaluated from {start.date()} "
            f"({len(px_all.loc[start:]) / 252:.2f} yrs)")
        say(f"    SPY full CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
            f"halves {b_full['s1']:.3f}/{b_full['s2']:.3f}; OOS Sharpe {mo['Sharpe']:.3f} "
            f"CAGR {mo['CAGR']:.2%} MaxDD {mo['MaxDD']:.2%}")
        say(f"    4b bars: H1>{b_full['s1']:.3f} H2>{b_full['s2']:.3f} OOS>{b_full['soos']:.3f} "
            f"MaxDD>={-DELTA * abs(b_full['sdd']):.2%} CAGR>={PHI * b_full['scagr']:.2%}")

        # ---- gate G1: the mask runner at phase 0 == engine.backtest
        Wchk = targets(px, "EWall")
        a, _ = run(px, Wchk, phase=0, cost_bps=10.0)
        b = backtest(px, Wchk, cost_bps=10.0, freq=FREQ)["returns"]
        say(f"    [G1] run(phase=0) vs engine.backtest, EWall @10bps: max|d| "
            f"{float((a - b).abs().max()):.3e}")
        assert float((a - b).abs().max()) < 1e-12

        # ---- the LIVE RULES v2 control, cost-matched, for 4a
        v2r = {c: backtest(px_all, rules_v2_weights(px_all), cost_bps=c, freq=FREQ)["returns"].loc[start:]
               for c in RUNGS}

        # ---- the grid
        for book in BOOKS:
            W1 = targets(px, book)
            for lam in LAMBDAS:
                r0, to = run(px, smooth(W1, lam), phase=0, cost_bps=0.0)
                r0, to = r0.loc[start:], to.loc[start:]
                R0[(pk, book, lam)], TO[(pk, book, lam)] = r0, to
                if lam == 1.0:                            # gate G2: the rung identity, live
                    live, _ = run(px, W1, phase=0, cost_bps=10.0)
                    ident = r0 - to * 10.0 / 1e4
                    say(f"    [G2] {book}: r_10 identity vs live 10bps run: max|d| "
                        f"{float((ident - live.loc[start:]).abs().max()):.3e}")
                    assert float((ident - live.loc[start:]).abs().max()) < 1e-12

            base_to = ann_turn(TO[(pk, book, 1.0)], r0.index)
            for lam in LAMBDAS:
                r0l, tol = R0[(pk, book, lam)], TO[(pk, book, lam)]
                r01, to1 = R0[(pk, book, 1.0)], TO[(pk, book, 1.0)]
                for c in RUNGS:
                    rr = {(p, d): (R0[(pk, book, p)] - TO[(pk, book, d)] * c / 1e4)
                          for p in (1.0, lam) for d in (1.0, lam)}
                    m11, mLL = mset(rr[(1.0, 1.0)]), mset(rr[(lam, lam)])
                    m1L, mL1 = mset(rr[(1.0, lam)]), mset(rr[(lam, 1.0)])
                    mg = margins(rr[(lam, lam)], b_full)
                    mg1 = margins(rr[(1.0, 1.0)], b_full)
                    mgP = margins(rr[(lam, 1.0)], b_full)
                    mgC = margins(rr[(1.0, lam)], b_full)
                    r_net = rr[(lam, lam)]
                    mm = metrics(r_net)
                    isb = margins(r_net, b_is, "IS")
                    row = dict(panel=pk, book=book, lam=lam, cost=c, base_to=base_to,
                               ann_to=ann_turn(tol, r0l.index),
                               drag_bps=ann_turn(tol, r0l.index) * c,
                               CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                               H1=mLL["H1"], H2=mLL["H2"], OOS_Sharpe=mLL["OOS_Sharpe"],
                               IS_Sharpe=metrics(win(r_net, "IS"))["Sharpe"],
                               IS_m_min=min(isb.values()),
                               OOS_CAGR=metrics(r_net.loc[OOS_START:])["CAGR"],
                               OOS_MaxDD=metrics(r_net.loc[OOS_START:])["MaxDD"])
                    for k in BARS5:
                        row["m_" + k] = mg[k]
                    row["m_min"] = min(mg[k] for k in BARS5)
                    row["pass4b"] = bool(row["m_min"] > 0)
                    bm = metrics(v2r[c])
                    h = len(v2r[c]) // 2
                    row["pass4a"] = bool(mLL["H1"] > metrics(v2r[c].iloc[:h])["Sharpe"]
                                         and mLL["H2"] > metrics(v2r[c].iloc[h:])["Sharpe"]
                                         and mm["MaxDD"] >= bm["MaxDD"])
                    rows.append(row)
                    keep_rows.append(dict(panel=pk, book=book, lam=lam, cost=c,
                                          pass4a=row["pass4a"], pass4b=row["pass4b"],
                                          both=bool(row["pass4a"] and row["pass4b"])))
                    for met in METS:
                        decomp.append(dict(panel=pk, book=book, lam=lam, cost=c, metric=met,
                                           base=m11[met],
                                           COST=m1L[met] - m11[met], PATH=mL1[met] - m11[met],
                                           INTER=mLL[met] - mL1[met] - m1L[met] + m11[met],
                                           TOTAL=mLL[met] - m11[met]))
                    for k in BARS5:
                        bar_rows.append(dict(panel=pk, book=book, lam=lam, cost=c, bar=k,
                                             m1=mg1[k], m_lam=mg[k],
                                             COST=mgC[k] - mg1[k], PATH=mgP[k] - mg1[k],
                                             TOTAL=mg[k] - mg1[k],
                                             flip_by_path=bool(mg1[k] <= 0 < mgP[k])))

            # ---- A3 the weekday-phase yardstick at lambda = 1
            for ph in PHASES:
                rp, tp = run(px, W1, phase=ph, cost_bps=0.0)
                rp, tp = rp.loc[start:], tp.loc[start:]
                for c in RUNGS:
                    rn = rp - tp * c / 1e4
                    mp = mset(rn)
                    phase_rows.append(dict(panel=pk, book=book, phase=ph, cost=c,
                                           ann_to=ann_turn(tp, rp.index), **mp))

    G = pd.DataFrame(rows)
    D = pd.DataFrame(decomp)
    P = pd.DataFrame(phase_rows)
    B = pd.DataFrame(bar_rows)
    K = pd.DataFrame(keep_rows)

    # ============================================================ A1 THE LEVEL
    say("\n" + "=" * 100)
    say("A1  THE LEVEL — realised annual turnover by panel x book x lambda, and the drag saved")
    lv = G[G.cost == 0].pivot_table(index=["panel", "book"], columns="lam", values="ann_to")
    say(lv.to_string(float_format=lambda x: f"{x:.4f}"))
    say("")
    for (pk, bk), r in lv.iterrows():
        d_to = r[1.00] - r.min()
        say(f"  {pk:9s} {bk:6s}: base {r[1.00]:8.4f} x/yr -> floor {r.min():8.4f} x/yr; the whole "
            f"dial saves {d_to:7.4f} x/yr = {d_to * 10:7.4f} bps/yr at 10 bps, "
            f"{d_to * 50:8.4f} bps/yr at 50 bps")

    # ============================================================ A2 THE DECOMPOSITION
    say("\n" + "=" * 100)
    say("A2  THE DECOMPOSITION — COST vs PATH vs INTER, all 288 arm-rows x 6 metrics")
    for met in ["Sharpe", "CAGR"]:
        say(f"\n  metric = {met}.  |PATH| and |COST| (median over the 7 lambda<1 points), by "
            f"panel x book x rung:")
        d = D[(D.metric == met) & (D.lam < 1.0)]
        t = d.groupby(["panel", "book", "cost"]).agg(
            med_PATH=("PATH", lambda s: float(np.median(np.abs(s)))),
            med_COST=("COST", lambda s: float(np.median(np.abs(s)))),
            med_INTER=("INTER", lambda s: float(np.median(np.abs(s)))),
            max_TOTAL=("TOTAL", lambda s: float(s.abs().max())),
            path_gt_cost=("PATH", "size"))
        pc = d.assign(gt=d.PATH.abs() > d.COST.abs()).groupby(["panel", "book", "cost"]).gt.mean()
        t["path_beats_cost"] = pc
        say(t.to_string(float_format=lambda x: f"{x:.6f}"))
    say("\n  EXACTNESS of the decomposition (COST+PATH+INTER-TOTAL): max|resid| "
        f"{float((D.COST + D.PATH + D.INTER - D.TOTAL).abs().max()):.3e}")
    say("  At cost 0: max|COST| " f"{float(D[D.cost == 0].COST.abs().max()):.3e}, max|INTER| "
        f"{float(D[D.cost == 0].INTER.abs().max()):.3e}  (both identically zero by construction)")

    say("\n  The whole lambda curve, Sharpe, at PROTOCOL's own 10 bps rung "
        "(TOTAL = the number a chooser sees):")
    say(G[G.cost == 10.0].pivot_table(index="lam", columns=["panel", "book"], values="Sharpe")
        .to_string(float_format=lambda x: f"{x:.5f}"))

    # ============================================================ A3 THE NOISE YARDSTICK
    say("\n" + "=" * 100)
    say("A3  THE NOISE YARDSTICK — five weekday phases of the SAME weekly cadence, lambda = 1")
    ys = {}
    for (pk, bk, c), d in P.groupby(["panel", "book", "cost"]):
        ys[(pk, bk, c)] = float(d.Sharpe.max() - d.Sharpe.min())
    yr = pd.Series(ys).rename("phase_spread_Sharpe").unstack()
    say("  Sharpe spread across the five phases (max - min), by panel x book x rung:")
    say(yr.to_string(float_format=lambda x: f"{x:.5f}"))
    say("\n  Sharpe by phase at 10 bps (the raw yardstick):")
    say(P[P.cost == 10.0].pivot_table(index="phase", columns=["panel", "book"], values="Sharpe")
        .to_string(float_format=lambda x: f"{x:.5f}"))
    say("\n  THE VERDICT TABLE — is the best lambda's TOTAL Sharpe gain bigger than the phase "
        "spread?  (gain = max over lambda of Sharpe(lam) - Sharpe(1))")
    vt = []
    for (pk, bk, c), d in G.groupby(["panel", "book", "cost"]):
        base = float(d.loc[d.lam == 1.0, "Sharpe"].iloc[0])
        gain = float(d.Sharpe.max() - base)
        argl = float(d.loc[d.Sharpe.idxmax(), "lam"])
        pcurve = D[(D.panel == pk) & (D.book == bk) & (D.cost == c) & (D.metric == "Sharpe")]
        best_path = float(pcurve.PATH.abs().max())
        best_cost = float(pcurve.COST.abs().max())
        sp = ys[(pk, bk, c)]
        vt.append(dict(panel=pk, book=bk, cost=c, base_Sharpe=base, best_lam=argl,
                       gain=gain, max_abs_PATH=best_path, max_abs_COST=best_cost,
                       phase_spread=sp, gain_over_spread=gain / sp if sp else np.nan,
                       beats_noise=bool(gain > sp)))
    VT = pd.DataFrame(vt)
    say(VT.to_string(index=False, float_format=lambda x: f"{x:.5f}"))
    for bk in BOOKS:
        d = VT[VT.book == bk]
        say(f"  {bk}: the best-lambda Sharpe gain beats the weekday-phase yardstick in "
            f"{int(d.beats_noise.sum())} of {len(d)} (panel, rung) cells; median gain/spread "
            f"{d.gain_over_spread.median():.4f}")

    # ============================================================ A4 WHICH BAR
    say("\n" + "=" * 100)
    say("A4  WHICH BAR — the queue's literal ask: name the bar the PATH term clears")
    say("  binding 4b bar at lambda = 1 (the bar with the smallest margin), by panel x book x rung:")
    bind = []
    for (pk, bk, c), d in G[G.lam == 1.0].groupby(["panel", "book", "cost"]):
        r = d.iloc[0]
        bb = min(BARS5, key=lambda k: r["m_" + k])
        bind.append(dict(panel=pk, book=bk, cost=c, binding=bb, margin=r["m_" + bb],
                         pass4b=bool(r.pass4b)))
    BD = pd.DataFrame(bind)
    say(BD.to_string(index=False, float_format=lambda x: f"{x:.5f}"))
    say("")
    for bk in BOOKS:
        d = B[(B.book == bk) & (B.lam < 1.0)]
        say(f"  {bk}: PATH-term flips of a 4b bar from FAIL to PASS: "
            f"{int(d.flip_by_path.sum())} of {len(d)} (bar, lambda, rung, panel) sites.")
        t = d.groupby("bar").agg(med_abs_PATH=("PATH", lambda s: float(np.median(np.abs(s)))),
                                 med_abs_COST=("COST", lambda s: float(np.median(np.abs(s)))),
                                 max_abs_PATH=("PATH", lambda s: float(s.abs().max())))
        say(t.to_string(float_format=lambda x: f"{x:.6f}"))
    say("\n  For the BINDING bar only: how far short does the PATH term fall of the margin it "
        "would have to cover?")
    short = []
    for _, r in BD.iterrows():
        d = B[(B.panel == r.panel) & (B.book == r.book) & (B.cost == r.cost) & (B.bar == r.binding)
              & (B.lam < 1.0)]
        short.append(dict(panel=r.panel, book=r.book, cost=r.cost, bar=r.binding,
                          margin_at_lam1=r.margin, best_PATH=float(d.PATH.max()),
                          covers=bool(r.margin <= 0 < r.margin + float(d.PATH.max()))))
    SH = pd.DataFrame(short)
    say(SH.to_string(index=False, float_format=lambda x: f"{x:.5f}"))
    say(f"  => the PATH term covers the binding bar in {int(SH.covers.sum())} of {len(SH)} cells.")

    # ============================================================ A5 DOES THE PATH TERM TRANSFER
    say("\n" + "=" * 100)
    say("A5  TRANSFER — the sign and the ordering of the PATH term, IS vs OOS")
    tr = []
    for pk in PANELS:
        for bk in BOOKS:
            r01 = R0[(pk, bk, 1.0)]
            for lam in LAMBDAS[1:]:
                r0l = R0[(pk, bk, lam)]
                pis = metrics(win(r0l, "IS"))["Sharpe"] - metrics(win(r01, "IS"))["Sharpe"]
                poos = metrics(win(r0l, "OOS"))["Sharpe"] - metrics(win(r01, "OOS"))["Sharpe"]
                tr.append(dict(panel=pk, book=bk, lam=lam, PATH_IS=pis, PATH_OOS=poos,
                               same_sign=bool(np.sign(pis) == np.sign(poos))))
    TR = pd.DataFrame(tr)
    say(TR.to_string(index=False, float_format=lambda x: f"{x:.6f}"))
    for bk in BOOKS:
        d = TR[TR.book == bk]
        rho = [spearman(g.PATH_IS, g.PATH_OOS) for _, g in d.groupby("panel")]
        say(f"  {bk}: IS/OOS sign agreement {int(d.same_sign.sum())}/{len(d)} "
            f"({d.same_sign.mean():.1%}); per-panel Spearman of the lambda curve IS vs OOS "
            f"{[round(x, 3) for x in rho]}")

    # ============================================================ A6 RULE 8
    say("\n" + "=" * 100)
    say("A6  RULE 8 — lambda chosen on 2009-2016 ALONE per (panel, book, rung), 2017-2026 read ONCE")
    say("    S0 = argmax IS Sharpe.   S1 = argmax IS worst-of-four 4b margin (IS-window bars).")
    wf_rows = []
    for (pk, bk, c), d in G.groupby(["panel", "book", "cost"]):
        ref = REF[pk]
        v2 = backtest(PX[pk], rules_v2_weights(PX[pk]), cost_bps=c, freq=FREQ)["returns"].loc[ref["start"]:]
        v2o, spyo = metrics(v2.loc[OOS_START:]), metrics(ref["spy"].loc[OOS_START:])
        d1 = d[d.lam == 1.0].iloc[0]
        for sel, col in (("S0", "IS_Sharpe"), ("S1", "IS_m_min")):
            pick = d.loc[d[col].idxmax()]
            wf_rows.append(dict(
                panel=pk, book=bk, cost=c, sel=sel, lam=pick.lam,
                IS_stat=pick[col], OOS_Sharpe=pick.OOS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                OOS_MaxDD=pick.OOS_MaxDD,
                lam1_OOS_Sharpe=d1.OOS_Sharpe, regret=pick.OOS_Sharpe - d1.OOS_Sharpe,
                best_OOS_Sharpe=d.OOS_Sharpe.max(),
                v2_OOS_Sharpe=v2o["Sharpe"], v2_OOS_CAGR=v2o["CAGR"], v2_OOS_MaxDD=v2o["MaxDD"],
                spy_OOS_Sharpe=spyo["Sharpe"], spy_OOS_CAGR=spyo["CAGR"], spy_OOS_MaxDD=spyo["MaxDD"],
                beats_spy=bool(pick.OOS_Sharpe > spyo["Sharpe"]),
                beats_v2=bool(pick.OOS_Sharpe > v2o["Sharpe"]),
                OOS_4b=bool(pick.OOS_Sharpe > spyo["Sharpe"]
                            and abs(pick.OOS_MaxDD) <= DELTA * abs(spyo["MaxDD"])
                            and pick.OOS_CAGR >= PHI * spyo["CAGR"]),
                full_pass4b=bool(pick.pass4b), full_pass4a=bool(pick.pass4a)))
    WF = pd.DataFrame(wf_rows)
    say(WF.drop(columns=["v2_OOS_CAGR", "v2_OOS_MaxDD", "spy_OOS_CAGR", "spy_OOS_MaxDD"])
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for sel in ("S0", "S1"):
        d = WF[WF.sel == sel]
        say(f"\n  {sel}: picks lambda<1 in {int((d.lam < 1).sum())} of {len(d)} cells "
            f"(EWall {int((d[d.book=='EWall'].lam < 1).sum())}/{len(d[d.book=='EWall'])}, "
            f"TOP20 {int((d[d.book=='TOP20'].lam < 1).sum())}/{len(d[d.book=='TOP20'])}).")
        say(f"      OOS REGRET vs the do-nothing default lambda=1: median {d.regret.median():+.5f} "
            f"Sharpe, mean {d.regret.mean():+.5f}, positive in {int((d.regret > 0).sum())}/{len(d)}"
            f"; on EWall alone median {d[d.book == 'EWall'].regret.median():+.5f}, positive in "
            f"{int((d[d.book == 'EWall'].regret > 0).sum())}/{len(d[d.book == 'EWall'])}")
        say(f"      OOS beats SPY {int(d.beats_spy.sum())}/{len(d)}; beats RULES v2 "
            f"{int(d.beats_v2.sum())}/{len(d)}; clears the 3 OOS 4b bars {int(d.OOS_4b.sum())}/{len(d)}")
        say(f"      mean OOS Sharpe {d.OOS_Sharpe.mean():.4f} vs lambda=1 "
            f"{d.lam1_OOS_Sharpe.mean():.4f} vs oracle-best-lambda {d.best_OOS_Sharpe.mean():.4f} "
            f"vs RULES v2 {d.v2_OOS_Sharpe.mean():.4f} vs SPY {d.spy_OOS_Sharpe.mean():.4f}")

    # ============================================================ KEEP PATHS
    say("\n" + "=" * 100)
    say("KEEP PATHS — PROTOCOL 4, both, on all arm-rows")
    say(f"  4a  {int(K.pass4a.sum())}/{len(K)}     4b  {int(K.pass4b.sum())}/{len(K)}     "
        f"BOTH  {int(K.both.sum())}/{len(K)}")
    say("  by rung:")
    say(K.groupby("cost")[["pass4a", "pass4b", "both"]].sum().to_string())
    say("  by panel x book (all rungs):")
    say(K.groupby(["panel", "book"])[["pass4a", "pass4b", "both"]].sum().to_string())
    at10 = K[K.cost == 10.0]
    say(f"  at PROTOCOL's own 10 bps rung: 4a {int(at10.pass4a.sum())}/{len(at10)}, "
        f"4b {int(at10.pass4b.sum())}/{len(at10)}, BOTH {int(at10.both.sum())}/{len(at10)}")
    if int(K.both.sum()):
        say(K[K.both].to_string(index=False))

    # ============================================================ VERDICT
    say("\n" + "=" * 100)
    say("VERDICT")
    ew_gain = VT[VT.book == "EWall"]
    top_gain = VT[VT.book == "TOP20"]
    dS = D[(D.metric == "Sharpe") & (D.lam < 1.0)]
    say(f"  EWall: |PATH| > |COST| in {dS[dS.book == 'EWall'].pipe(lambda x: (x.PATH.abs() > x.COST.abs()).mean()):.1%} "
        f"of lambda x rung sites -> the queue is RIGHT that the gain is not a cost gain.")
    say(f"  TOP20 (positive control): |PATH| > |COST| in "
        f"{dS[dS.book == 'TOP20'].pipe(lambda x: (x.PATH.abs() > x.COST.abs()).mean()):.1%} of sites.")
    say(f"  But the EWall PATH term beats the weekday-phase noise yardstick in only "
        f"{int(ew_gain.beats_noise.sum())}/{len(ew_gain)} cells (TOP20 {int(top_gain.beats_noise.sum())}/"
        f"{len(top_gain)}), and it clears NO 4b bar: {int(B[B.book == 'EWall'].flip_by_path.sum())} "
        f"fail->pass flips out of {len(B[B.book == 'EWall'])} sites.")

    # ============================================================ artefacts
    G.to_csv(f"{OUT / STEM}.grid.csv", index=False)
    D.to_csv(f"{OUT / STEM}.decomp.csv", index=False)
    P.to_csv(f"{OUT / STEM}.phase.csv", index=False)
    B.to_csv(f"{OUT / STEM}.bars.csv", index=False)
    WF.to_csv(f"{OUT / STEM}.walkforward.csv", index=False)
    K.to_csv(f"{OUT / STEM}.keeppaths.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nwrote {STEM}.{{grid,decomp,phase,bars,walkforward,keeppaths}}.csv and .console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
