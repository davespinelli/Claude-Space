#!/usr/bin/env python3
"""Idea 586 - does the IS-side EPISODE MISMATCH move any published rule-8 pick?  (cloud, 2026-09-09)

PRE-REGISTERED QUESTION (QUEUE.md 586, written before any number below was read)
    Idea 321 found the in-sample 4b DD gate compares a book's 2011/2012 episode against
    SPY's 2009 crash (modal book worst-episode year 2011/2011/2012 vs SPY 2009/2009/2011),
    a mismatch that vanishes out of sample where 2020 sets both sides.  Re-base the IS DD
    bar onto a common-episode window and re-read every committed rule-8 pick that used an
    IS DD gate: does any pick change?  Max 2 params.

WHY THE MISMATCH EXISTS -- THE PRE-REGISTERED MECHANISM, AND ITS REFUTATION BY THIS RUN
    PRE-REGISTERED (written before measuring, and REPORTED HERE BECAUSE IT TURNED OUT WRONG):
        every book in the record is a 200d-MA-gated or momentum-ranked book on a panel that
        starts 2008-01; it needs 200 closes to have a signal at all and the gate holds it
        flat through the 2008-09 crash, so the book's IS equity curve DOES NOT CONTAIN the
        episode that sets SPY's IS MaxDD.  4b's DD leg would then be priced off an episode
        the book never traded -- a LOOSE bar handing every book ~33 pp of allowance against
        a 5-8 pp risk history.
    WHAT THIS RUN ACTUALLY FOUND: that reading is FALSE, on two counts measured in Part 1.
        (i) PROTOCOL's own 260-day warm-up skip already truncates the 2008 leg: SPY's IS
            MaxDD measured from 2009-01-13 is -22.1%, not -55%, so the bar is 13.24 pp, not
            ~33 pp.  (ii) De-grossing is PARTIAL -- bonds and gold were above their 200d MA
            in early 2009 -- so every book is live from the FIRST post-warm-up day and 0 of
            the 4 IS episodes are excluded by any live-start filter.
        The two arms therefore already read the SAME episode set, and the common-episode
        re-basing the queue asked for is an exact NO-OP (CE == RAW at every theta).
    WHAT SURVIVES: the mismatch is real but it is a MAXIMISATION mismatch, not an exposure
        one -- each arm takes its maximum over the shared episode set on a DIFFERENT episode
        (book 2011/2011/2012 vs SPY 2009/2009/2011).  Removing that freedom is what EM does
        below, and that is where the effect lives.

THE TWO CONVENTIONS.  Both are computed on the SAME books, SAME window, SAME costs.  The
convention is a REPORTING AXIS: it is printed at every value and never selected on.
  RAW  (the incumbent, what every committed rule-8 pick used)
       bar_IS  = 0.60 * |MaxDD of SPY over the whole IS window|
       book_IS = |MaxDD of the book over the whole IS window|
  CE(theta)  (the candidate re-basing: COMMON EPISODE)
       SPY drawdown episodes are maximal underwater runs of SPY whose trough reaches
       -theta.  An episode is COMMON if its peak date is on or after the book's own
       live-start (first day the book carries non-zero gross) and its trough date is
       inside IS.  Both arms are then read ONLY inside those common episode spans, each
       span's peak reset at the span's start:
       bar_IS  = 0.60 * max over common episodes of |SPY DD within the span|
       book_IS = max over common episodes of |book DD within the span|
       If a book has NO common IS episode at theta the cell is reported as UNDEFINED and
       carries no verdict (it is never silently passed).
  EM(theta)  (the STRICT re-basing: EPISODE-MATCHED, added after CE's first run)
       CE turned out to be a NO-OP -- identical to RAW at every theta on every panel -- for a
       reason worth stating rather than hiding: PROTOCOL's own 260-day warm-up skip already
       removes the 2008 leg of SPY's crash, so SPY's IS MaxDD is -22.1% measured from
       2009-01, not -55%; and de-grossing is PARTIAL, so every band book carries some
       exposure (bonds and gold were above their 200d MA in early 2009) from the first
       post-warm-up day.  The common-episode filter therefore excludes NOTHING, and the two
       arms already read the same episode set.  That kills the "the book never traded the
       episode" reading of the defect -- but NOT the defect itself, because each arm is
       still free to take its MAXIMUM over that set on a DIFFERENT episode.  EM removes
       exactly that freedom: it requires, for EVERY common IS episode e,
            |book DD within e|  <=  0.60 * |SPY DD within e|
       so the 2011 book episode is priced against SPY's 2011, not against SPY's 2009.  This
       is the form of the re-basing with teeth, and it is the one H_VERDICT/H_PICK are read
       on.  RAW, CE and EM are all reported at every grid point.

TUNED PARAMETERS: exactly TWO, the band b and the gross g, i.e. idea 321's own pair, so the
rule-8 chooser here is the same object the record's picks came from.  Panel, cost rung,
cadence, theta and convention are REPORTING axes, printed at every value, never selected on.
Every grid point is written to .grid.csv; nothing is filtered before reporting.

RULE 8 (PROTOCOL 8).  For each panel x cost rung x convention: the chooser sees IS
(<= 2016-12-31) ONLY.  It keeps the (b, g) points that pass the IS-side 4b legs
(IS Sharpe > SPY IS Sharpe, the IS DD bar under THAT convention, IS CAGR >= 0.70 * SPY IS
CAGR) and takes the survivor with the highest IS Sharpe.  2017-01-01..2026 is then read
ONCE for the picked point: OOS CAGR / Sharpe / MaxDD against the live RULES v2 baseline and
against SPY, with BOTH KEEP paths (4a and 4b) evaluated on the full sample.

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read)
  H_MISMATCH  idea 321's finding reproduces: on IS, the book's worst-episode year differs
              from SPY's on >= 80% of grid points in every panel.
  H_BAR       CE materially tightens the IS bar: the median IS DD bar falls by >= 5 pp.
  H_VERDICT   >= 10% of IS DD-gate verdicts flip between RAW and the re-based bar at
              theta = 0.10.  Read on EM (the strict form); CE is reported beside it.
  H_PICK      (THE HEADLINE) at least one rule-8 pick changes under the re-based bar.  If no pick moves,
              the mismatch is real but INERT for the record's picks and the honest answer
              is a KILL of the remedy, not of the defect.

CENSUS OF THE RECORD.  "Every committed rule-8 pick" is bounded here by what the record
actually publishes: all research/backtests/*.walkforward.csv are read and each is classified
by whether it carries the columns needed to re-read its own IS DD gate WITHOUT re-running
its script.  The count of re-readable files is reported honestly; files that publish only
the pick and its OOS metrics cannot be re-read from disk and are named as such.

REPRODUCTION GATES, asserted and printed before any new number is read
  G1  fast_backtest reproduces engine.backtest to < 1e-12 on 4 real books (idea 321's gate).
  G2  band_book(px, 0.03, 0.75) reproduces baseline.rules_v2_weights EXACTLY (0.0).
  G3  episode decomposition identity: max over disjoint underwater episodes == MaxDD
      exactly (0.0) on SPY and on every book.
  G4  the structural relation between the conventions, asserted rather than assumed.
      G4a the SPY arm NESTS exactly: at theta -> 0 with the live-start forced to the window
          start, CE's bar == RAW's bar to 0.0, because SPY's episode-local depths ARE its
          own drawdown decomposition (this is G3's identity applied to SPY).
      G4b the BOOK arm does NOT nest and must not be claimed to: reading the book inside
          SPY's episode spans with the peak reset at each span's start is a reading over
          SUBWINDOWS, so book_CE <= book_RAW for every theta and every book, with equality
          only when the book's own worst drawdown happens to sit inside one SPY span.
      The first run of this script FAILED a naive "CE nests RAW on both arms" gate at
      3.494e-02; that failure is the property above, not an error, and the gate is stated
      here in the form that is actually true.  The consequence matters for reading Part 2:
      CE TIGHTENS BOTH SIDES of the inequality, so which way a verdict moves is not
      determined by construction and has to be measured.

SURVIVORSHIP (PROTOCOL 9).  B136 and SMALL439 are CURRENT-constituent lists: the names that
died are absent, so both panels' crashes are shallower than the real world's and every DD
number on them is optimistic.  SMALL439 is the 483-name sub-$2B panel with the 44 tickers
whose max_1d_move >= 1.0 in data/small_meta.csv dropped first (data errors, not returns).
The IS-side bar is priced off SPY, which is survivorship-free, so the MISMATCH statistic is
not biased by this; the book-side DD is.

Costs 10 and 25 bps on turnover, weights decided at close t applied at t+1, no shorting, no
leverage (PROTOCOL 2).  Deterministic, no network.
Writes .grid.csv, .episodes.csv, .flips.csv, .walkforward.csv, .census.csv, .console.txt
"""
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402

sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask  # noqa: E402

OUT = Path(__file__).with_suffix("")
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
DD_CAP = 0.60          # PROTOCOL 4b
CAGR_FLOOR = 0.70      # PROTOCOL 4b
COSTS = [10.0, 25.0]
PROTO_COST = 10.0
THETAS = [0.08, 0.10, 0.15, 0.20]
POINT_THETA = 0.10
BANDS = [0.00, 0.03, 0.05, 0.08, 0.10, 0.15, 0.20]     # tuned param 1
GROSS = [0.25, 0.50, 0.75, 1.00]                       # tuned param 2
FREQS = ["W", "M"]                                     # reporting axis
WARM = 260

_LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _LOG.append(s)


# ------------------------------------------------------------------ engine
def fast_backtest(prices, weights, freq="W"):
    """Numpy replica of engine.backtest.  Returns (gross_return_series, turnover_series)
    so both cost rungs are priced from one pass: net = gross - turnover * bps / 1e4."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values
    n = len(idx)
    cur = np.zeros(prices.shape[1])
    held = np.empty_like(rets)
    turn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    g = np.nansum(held * rets, axis=1)
    return (pd.Series(g, index=idx), pd.Series(turn, index=idx),
            pd.Series(held.sum(axis=1), index=idx))


def net(gross_r, turn, bps):
    return gross_r - turn * bps / 1e4


# ------------------------------------------------------------------ dd machinery
def dd_path(r):
    eq = (1.0 + r.fillna(0.0)).cumprod().values
    peak = np.maximum.accumulate(eq)
    return pd.Series(eq / peak - 1.0, index=r.index)


def dd_episodes(r):
    """Disjoint underwater episodes, deepest first: (depth<=0, (peak, trough, end)).
    The span STARTS at the peak day (the last day with dd == 0), so re-peaking inside
    the span reproduces the episode depth exactly -- this is what G4a asserts."""
    dd = dd_path(r).values
    under = dd < 0
    out, i, n = [], 0, len(dd)
    while i < n:
        if not under[i]:
            i += 1
            continue
        j = i
        while j < n and under[j]:
            j += 1
        seg = dd[i:j]
        t = int(np.argmin(seg))
        out.append((float(seg[t]), (max(i - 1, 0), i + t, j - 1)))
        i = j
    out.sort(key=lambda x: x[0])
    return out


def maxdd(r):
    d = dd_path(r)
    return float(d.min()) if len(d) else 0.0


def dd_in_span(r, lo, hi):
    """|MaxDD| of r restricted to [lo, hi] with the peak RESET at lo (episode-local)."""
    seg = r.iloc[lo:hi + 1]
    if len(seg) < 2:
        return 0.0
    return abs(float(dd_path(seg).min()))


def perf(r):
    r = r.dropna()
    if len(r) < 20:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan, N=len(r))
    eq = (1 + r).cumprod()
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252)
    return dict(CAGR=float(eq.iloc[-1] ** (1 / yrs) - 1),
                Sharpe=float((r.mean() * 252) / vol) if vol > 0 else np.nan,
                MaxDD=maxdd(r), N=len(r))


def worst_year(r):
    ep = dd_episodes(r)
    return int(r.index[ep[0][1][1]].year) if ep else -1


# ------------------------------------------------------------------ books
def band_book(px, band, gross):
    """The live RULES v2 family: equal weight inside the 200d +/- band, de-gross to cash."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0)


# ------------------------------------------------------------------ CE re-basing
def spy_ep_table(spy_r, theta):
    """SPY episodes reaching -theta, as (peak_pos, trough_pos, end_pos, depth)."""
    return [(s, t, e, d) for d, (s, t, e) in dd_episodes(spy_r) if abs(d) >= theta]


def ce_bar(spy_r, book_r, eps, live_start_pos, is_end_pos):
    """Common-episode IS bar and book reading.  Returns (bar, book, n_ep) or (nan, nan, 0)."""
    common = [(s, t, e) for (s, t, e, _d) in eps
              if s >= live_start_pos and t <= is_end_pos]
    if not common:
        return np.nan, np.nan, 0
    spy_d = max(dd_in_span(spy_r, s, min(e, is_end_pos)) for s, t, e in common)
    bk_d = max(dd_in_span(book_r, s, min(e, is_end_pos)) for s, t, e in common)
    return DD_CAP * spy_d, bk_d, len(common)


def em_check(spy_r, book_r, eps, live_start_pos, is_end_pos):
    """EPISODE-MATCHED: the 4b DD inequality imposed inside EVERY common IS episode.
    Returns (pass, worst_ratio, binding_year, n_common, binding_SPY_depth).  worst_ratio is
    max_e |book DD in e| / (0.60 * |SPY DD in e|); <= 1 is a pass."""
    common = [(s_, t, e) for (s_, t, e, _d) in eps
              if s_ >= live_start_pos and t <= is_end_pos]
    if not common:
        return None, np.nan, -1, 0, np.nan
    worst, wy, wd = -np.inf, -1, np.nan
    for s_, t, e in common:
        hi = min(e, is_end_pos)
        sd = dd_in_span(spy_r, s_, hi)
        bd = dd_in_span(book_r, s_, hi)
        if sd <= 0:
            continue
        ratio = bd / (DD_CAP * sd)
        if ratio > worst:
            worst, wy, wd = ratio, int(spy_r.index[t].year), sd
    if worst == -np.inf:
        return None, np.nan, -1, 0, np.nan
    return bool(worst <= 1.0), float(worst), wy, len(common), wd


def live_start(gross_path, idx):
    """First position at which the book actually carries exposure."""
    nz = np.flatnonzero(gross_path.values > 1e-12)
    return int(nz[0]) if len(nz) else len(idx) - 1


# ------------------------------------------------------------------ 4b legs
def keep_paths(r, spy, base, start):
    """Full-sample 4a and 4b on the common window, per PROTOCOL 4."""
    r, spy, base = r.loc[start:], spy.loc[start:], base.loc[start:]
    h = len(r) // 2
    pr, pb, ps = perf(r), perf(base), perf(spy)
    r1, r2 = perf(r.iloc[:h]), perf(r.iloc[h:])
    s1, s2 = perf(spy.iloc[:h]), perf(spy.iloc[h:])
    b1, b2 = perf(base.iloc[:h]), perf(base.iloc[h:])
    ro, so = perf(r.loc[OOS_START:]), perf(spy.loc[OOS_START:])
    fa = (r1["Sharpe"] > b1["Sharpe"] and r2["Sharpe"] > b2["Sharpe"]
          and pr["MaxDD"] >= pb["MaxDD"])
    legs = []
    if not r1["Sharpe"] > s1["Sharpe"]:
        legs.append("H1")
    if not r2["Sharpe"] > s2["Sharpe"]:
        legs.append("H2")
    if not ro["Sharpe"] > so["Sharpe"]:
        legs.append("OOS")
    if not abs(pr["MaxDD"]) <= DD_CAP * abs(ps["MaxDD"]):
        legs.append("DD")
    if not pr["CAGR"] >= CAGR_FLOOR * ps["CAGR"]:
        legs.append("CAGR")
    return dict(fa=bool(fa), fb=(len(legs) == 0), fb_fail=",".join(legs) or "-",
                CAGR=pr["CAGR"], Sharpe=pr["Sharpe"], MaxDD=pr["MaxDD"],
                H1=r1["Sharpe"], H2=r2["Sharpe"])


# ================================================================== run
def main():
    say("=" * 100)
    say("IDEA 586 - does the IS-side EPISODE MISMATCH move any published rule-8 pick?")
    say("           (cloud, 2026-09-09)")
    say("=" * 100)

    panels = {}
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    for name, kw in [("U56", dict()), ("B136", dict(broad=True)), ("SMALL439", dict(small=True))]:
        px = load_universe(**kw)
        if name == "SMALL439":
            drop = [c for c in px.columns if c in bad]
            px = px.drop(columns=drop)
            say(f"  SMALL panel: dropped {len(drop)} tickers with max_1d_move >= 1.0 "
                f"(data errors, per data/SMALL_PANEL_README.md)")
        panels[name] = px
        say(f"panel {name:9s} {px.shape[0]:5d} days x {px.shape[1] - 1:4d} names + SPY  "
            f"{px.index[0].date()} .. {px.index[-1].date()}")

    # ---------------------------------------------------------- G1 / G2
    say("\n--- G1  fast_backtest vs engine.backtest (4 real books) ---")
    px = panels["U56"]
    worst = 0.0
    for lbl, b, g, f in [("v2 band 0.03 g0.75 W", 0.03, 0.75, "W"),
                         ("band 0.00 g1.00 W", 0.00, 1.00, "W"),
                         ("band 0.10 g0.50 M", 0.10, 0.50, "M"),
                         ("band 0.20 g0.25 M", 0.20, 0.25, "M")]:
        w = band_book(px.drop(columns=["SPY"]), b, g).reindex(columns=px.columns).fillna(0.0)
        gr, tu, _ = fast_backtest(px, w, freq=f)
        mine = net(gr, tu, PROTO_COST)
        theirs = engine_backtest(px, w, cost_bps=PROTO_COST, freq=f)["returns"]
        d = float((mine - theirs).abs().max())
        worst = max(worst, d)
        say(f"  {lbl:24s} max|diff| = {d:.3e}")
    say(f"  G1 {'PASS' if worst < 1e-12 else 'FAIL'} (bar 1e-12, worst {worst:.3e})")
    assert worst < 1e-12

    say("\n--- G2  band_book(0.03, 0.75) nests baseline.rules_v2_weights ---")
    d2 = float((band_book(px.drop(columns=["SPY"]), 0.03, 0.75)
                - rules_v2_weights(px.drop(columns=["SPY"]))).abs().max().max())
    say(f"  max|diff| = {d2:.3e}   G2 {'PASS' if d2 == 0.0 else 'FAIL'} (bar exactly 0.0)")
    assert d2 == 0.0

    # ---------------------------------------------------------- build the grid
    say("\n--- building the book grid (7 bands x 4 gross x 2 cadences x 3 panels) ---")
    books = {}          # (panel, b, g, f) -> dict(gross_r, turn, gross_path)
    for pname, px in panels.items():
        cols = px.drop(columns=["SPY"], errors="ignore").columns
        for b in BANDS:
            for g in GROSS:
                w = band_book(px[cols], b, g).reindex(columns=px.columns).fillna(0.0)
                for f in FREQS:
                    gr, tu, gp = fast_backtest(px, w, freq=f)
                    books[(pname, b, g, f)] = (gr, tu, gp)
        say(f"  {pname}: {len(BANDS) * len(GROSS) * len(FREQS)} books")

    # ---------------------------------------------------------- G3 / G4
    say("\n--- G3  episode identity: max over disjoint episodes == MaxDD (exactly) ---")
    g3 = 0.0
    for (pname, b, g, f), (gr, tu, _) in books.items():
        r = net(gr, tu, PROTO_COST).loc[panels[pname].index[WARM]:]
        ep = dd_episodes(r)
        g3 = max(g3, abs((ep[0][0] if ep else 0.0) - maxdd(r)))
    for pname, px in panels.items():
        sr = px["SPY"].pct_change().fillna(0.0).loc[px.index[WARM]:]
        ep = dd_episodes(sr)
        g3 = max(g3, abs((ep[0][0] if ep else 0.0) - maxdd(sr)))
    say(f"  max|episode-max - MaxDD| = {g3:.3e}   G3 {'PASS' if g3 == 0.0 else 'FAIL'}")
    assert g3 == 0.0

    say("\n--- G4  structural relation between the conventions ---")
    g4a = 0.0          # SPY arm must nest exactly at theta -> 0
    g4a2 = 0.0         # CE bar may only tighten, never loosen, at any theta
    g4b = 0.0          # book arm must be a SUBWINDOW reading: book_CE - book_RAW <= 0
    g4b_eq = 0
    g4b_n = 0
    for pname, px in panels.items():
        start = px.index[WARM]
        sr = px["SPY"].pct_change().fillna(0.0).loc[start:]
        is_end_pos = int(sr.index.searchsorted(pd.Timestamp(IS_END), "right")) - 1
        spy_is = sr.iloc[:is_end_pos + 1]
        raw_bar = DD_CAP * abs(maxdd(spy_is))
        eps0 = spy_ep_table(spy_is, 0.0)
        eps_th = {th: spy_ep_table(spy_is, th) for th in THETAS}
        for (pn, b, g, f), (gr, tu, gp) in books.items():
            if pn != pname or f != "W":
                continue
            r = net(gr, tu, PROTO_COST).loc[start:]
            raw_bk = abs(maxdd(r.iloc[:is_end_pos + 1]))
            bar0, _bk0, _n0 = ce_bar(sr, r, eps0, 0, is_end_pos)
            g4a = max(g4a, abs(bar0 - raw_bar))
            ls = live_start(gp.loc[start:], r.index)
            for th in THETAS:
                bar, bk, n_ep = ce_bar(sr, r, eps_th[th], ls, is_end_pos)
                if n_ep == 0:
                    continue
                g4b_n += 1
                g4b = max(g4b, bk - raw_bk)                # must be <= 0
                g4b_eq += int(abs(bk - raw_bk) < 1e-12)
                g4a2 = max(g4a2, bar - raw_bar)            # CE bar can only tighten
    say(f"  G4a SPY arm nests at theta->0 : max|CE bar - RAW bar| = {g4a:.3e}  "
        f"{'PASS' if g4a < 1e-12 else 'FAIL'} (bar 1e-12)")
    say(f"  G4a2 CE bar only tightens : max(CE bar - RAW bar) = {g4a2:.3e}  "
        f"{'PASS' if g4a2 <= 1e-12 else 'FAIL'} (must be <= 0)")
    say(f"  G4b book arm is a subwindow reading: max(book_CE - book_RAW) = {g4b:.3e}  "
        f"{'PASS' if g4b <= 1e-12 else 'FAIL'} (must be <= 0)")
    say(f"      equality (book's worst DD sits inside a SPY span) on {g4b_eq}/{g4b_n} "
        f"= {g4b_eq / max(g4b_n, 1):.1%} of book x theta cells")
    say("      => CE tightens BOTH sides of the inequality; the direction of any verdict")
    say("         change is therefore NOT fixed by construction (see Part 2).")
    assert g4a < 1e-12 and g4a2 <= 1e-12 and g4b <= 1e-12

    # ---------------------------------------------------------- PART 1: mismatch
    say("\n" + "=" * 100)
    say("PART 1  REPRODUCE THE DEFECT - whose episode sets each side of the IS DD bar?")
    say("=" * 100)
    rows, eprows = [], []
    for pname, px in panels.items():
        start = px.index[WARM]
        sr = px["SPY"].pct_change().fillna(0.0).loc[start:]
        is_end_pos = int(sr.index.searchsorted(pd.Timestamp(IS_END), "right")) - 1
        spy_is = sr.iloc[:is_end_pos + 1]
        spy_wy = worst_year(spy_is)
        eps = {th: spy_ep_table(sr, th) for th in THETAS}
        for th in THETAS:
            for (s, t, e, d) in eps[th]:
                eprows.append(dict(panel=pname, theta=th,
                                   peak=str(sr.index[s].date()), trough=str(sr.index[t].date()),
                                   end=str(sr.index[e].date()), depth=d,
                                   trough_in_IS=bool(t <= is_end_pos)))
        for (pn, b, g, f), (gr, tu, gp) in books.items():
            if pn != pname:
                continue
            gpw = gp.loc[start:]
            ls = live_start(gpw, gpw.index)
            for c in COSTS:
                r = net(gr, tu, c).loc[start:]
                r_is = r.iloc[:is_end_pos + 1]
                raw_bk = abs(maxdd(r_is))
                raw_bar = DD_CAP * abs(maxdd(spy_is))
                rec = dict(panel=pname, band=b, gross=g, freq=f, cost=c,
                           live_start=str(gpw.index[ls].date()),
                           book_IS_worst_year=worst_year(r_is), spy_IS_worst_year=spy_wy,
                           mismatch=bool(worst_year(r_is) != spy_wy),
                           IS_Sharpe=perf(r_is)["Sharpe"], IS_CAGR=perf(r_is)["CAGR"],
                           spy_IS_Sharpe=perf(spy_is)["Sharpe"], spy_IS_CAGR=perf(spy_is)["CAGR"],
                           RAW_bar_pp=raw_bar * 100, RAW_book_pp=raw_bk * 100,
                           RAW_pass=bool(raw_bk <= raw_bar))
                for th in THETAS:
                    bar, bk, n_ep = ce_bar(sr, r, eps[th], ls, is_end_pos)
                    all_ep = len([1 for (s_, t, _e, _d) in eps[th] if t <= is_end_pos])
                    rec[f"CE{th}_bar_pp"] = bar * 100
                    rec[f"CE{th}_book_pp"] = bk * 100
                    rec[f"CE{th}_nep"] = n_ep
                    rec[f"CE{th}_nep_all"] = all_ep
                    rec[f"CE{th}_excluded"] = all_ep - n_ep
                    rec[f"CE{th}_pass"] = (bool(bk <= bar) if n_ep > 0 else None)
                    ok, wr, wy, ne, wd = em_check(sr, r, eps[th], ls, is_end_pos)
                    rec[f"EM{th}_pass"] = ok
                    rec[f"EM{th}_worst_ratio"] = wr
                    rec[f"EM{th}_bind_year"] = wy
                    rec[f"EM{th}_nep"] = ne
                    rec[f"EM{th}_bind_spy_depth_pp"] = wd * 100
                rows.append(rec)
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    pd.DataFrame(eprows).to_csv(f"{OUT}.episodes.csv", index=False)
    say(f"  {len(G)} grid points written to {Path(OUT).name}.grid.csv")

    say("\n  IS worst-episode year, book vs SPY (PROTO cost rung, both cadences):")
    sub = G[G.cost == PROTO_COST]
    for pname in panels:
        s = sub[sub.panel == pname]
        vc = s.book_IS_worst_year.value_counts()
        say(f"    {pname:9s} book modal IS worst year {vc.index[0]} on {vc.iloc[0]}/{len(s)} "
            f"({vc.iloc[0] / len(s):.0%})  {dict(vc.head(3))}   |  SPY's own IS worst year "
            f"{s.spy_IS_worst_year.iloc[0]}   MISMATCH on {s.mismatch.mean():.0%}")
    hm = sub.groupby("panel").mismatch.mean().min()
    say(f"\n  H_MISMATCH ({'HOLDS' if hm >= 0.80 else 'FAILS'}): "
        f"min panel mismatch share {hm:.0%} vs an 80% bar")

    say("\n  The IS DD bar itself, RAW vs CE (pp of drawdown allowed), PROTO rung:")
    for pname in panels:
        s = sub[sub.panel == pname]
        say(f"    {pname:9s} RAW bar {s.RAW_bar_pp.median():6.2f} pp   "
            + "   ".join(f"CE{th} {s[f'CE{th}_bar_pp'].median():6.2f}" for th in THETAS)
            + f"   | book IS DD median {s.RAW_book_pp.median():5.2f} pp")
    say("\n  WHY CE moves nothing - the live-start filter excludes no episode:")
    for pname in panels:
        s_ = sub[sub.panel == pname]
        say(f"    {pname:9s} book live-start: {s_.live_start.min()} .. {s_.live_start.max()}"
            f"   IS episodes at theta={POINT_THETA}: {int(s_[f'CE{POINT_THETA}_nep_all'].median())} total, "
            f"{int(s_[f'CE{POINT_THETA}_excluded'].median())} excluded by live-start")
    say("    => the two arms already read the SAME episode set; what differs is only WHICH")
    say("       episode each arm takes its maximum on.  That is what EM removes.")

    say("\n  EM (episode-matched) worst ratio  |book DD in e| / (0.60*|SPY DD in e|), PROTO rung:")
    for pname in panels:
        s_ = sub[sub.panel == pname]
        wr = s_[f"EM{POINT_THETA}_worst_ratio"]
        by = s_[f"EM{POINT_THETA}_bind_year"].value_counts()
        say(f"    {pname:9s} median {wr.median():5.2f}  IQR [{wr.quantile(.25):.2f}, "
            f"{wr.quantile(.75):.2f}]  max {wr.max():5.2f}   binding-episode year "
            f"{dict(by.head(3))}  binding SPY depth median "
            f"{s_[f'EM{POINT_THETA}_bind_spy_depth_pp'].median():.1f} pp")

    say("\n  IS THE EM BITE A SHALLOW-EPISODE ARTEFACT?  binding episode depth by theta:")
    for th in THETAS:
        s_ = sub[sub[f"EM{th}_pass"].notna()]
        if s_.empty:
            continue
        fail = s_[~s_[f"EM{th}_pass"].astype(bool)]
        say(f"    theta={th:4.2f}  EM fails {len(fail):3d}/{len(s_):3d}   binding SPY depth on"
            f" the FAILURES: median {fail[f'EM{th}_bind_spy_depth_pp'].median() if len(fail) else float('nan'):5.1f} pp"
            f"  min {fail[f'EM{th}_bind_spy_depth_pp'].min() if len(fail) else float('nan'):5.1f} pp"
            f"   binding years {dict(fail[f'EM{th}_bind_year'].value_counts().head(3)) if len(fail) else {}}")
    say("    A ratio test on a SHALLOW episode is mechanically harsh (0.60 x 8 pp = 4.8 pp of")
    say("    allowance), so the theta ladder is reported in full and theta=0.15 - where the")
    say("    binding episodes are SPY's real 2010/2011 selloffs - is the honest reading.")

    drop_pp = (sub.RAW_bar_pp - sub[f"CE{POINT_THETA}_bar_pp"]).median()
    say(f"\n  H_BAR ({'HOLDS' if drop_pp >= 5.0 else 'FAILS'}): median bar falls "
        f"{drop_pp:.2f} pp at theta={POINT_THETA} vs a 5 pp bar")

    # ---------------------------------------------------------- PART 2: verdict flips
    say("\n" + "=" * 100)
    say("PART 2  DOES THE RE-BASING CHANGE THE IS DD-GATE VERDICT?  (all grid points)")
    say("=" * 100)
    frows = []
    for th in THETAS:
        for c in COSTS:
            s = G[(G.cost == c) & G[f"CE{th}_pass"].notna()]
            und = int((G.cost == c).sum() - len(s))
            ce = s[f"CE{th}_pass"].astype(bool)
            se = G[(G.cost == c) & G[f"EM{th}_pass"].notna()]
            em = se[f"EM{th}_pass"].astype(bool)
            fce = (s.RAW_pass != ce)
            fem = (se.RAW_pass != em)
            frows.append(dict(theta=th, cost=c, n=len(s), undefined=und,
                              RAW_pass=int(s.RAW_pass.sum()),
                              CE_pass=int(ce.sum()), CE_flips=int(fce.sum()),
                              CE_flip_rate=float(fce.mean()) if len(s) else np.nan,
                              EM_n=len(se), EM_pass=int(em.sum()), EM_flips=int(fem.sum()),
                              EM_flip_rate=float(fem.mean()) if len(se) else np.nan,
                              raw_pass_EM_fail=int((se.RAW_pass & ~em).sum()),
                              raw_fail_EM_pass=int((~se.RAW_pass & em).sum())))
    F = pd.DataFrame(frows)
    F.to_csv(f"{OUT}.flips.csv", index=False)
    say(F.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    _r = F[(F.theta == POINT_THETA) & (F.cost == PROTO_COST)].iloc[0]
    fr = float(_r.EM_flip_rate)
    say(f"\n  H_VERDICT ({'HOLDS' if fr >= 0.10 else 'FAILS'}): EM flip rate {fr:.1%} "
        f"(CE {float(_r.CE_flip_rate):.1%}) at theta={POINT_THETA}, {PROTO_COST:.0f} bps, "
        f"vs a 10% bar")

    # ---------------------------------------------------------- PART 3: rule 8
    say("\n" + "=" * 100)
    say("PART 3  RULE 8 - does any pick MOVE?  chooser sees IS only; OOS read once")
    say("=" * 100)
    wf = []
    for pname, px in panels.items():
        start = px.index[WARM]
        sr = px["SPY"].pct_change().fillna(0.0).loc[start:]
        is_end_pos = int(sr.index.searchsorted(pd.Timestamp(IS_END), "right")) - 1
        spy_is = sr.iloc[:is_end_pos + 1]
        eps = {th: spy_ep_table(spy_is, th) for th in THETAS}   # IS slice only: causal
        base_gr, base_tu, _ = fast_backtest(px, rules_v2_weights(px.drop(columns=["SPY"],
                                            errors="ignore")).reindex(columns=px.columns).fillna(0.0), freq="W")
        for c in COSTS:
            base = net(base_gr, base_tu, c).loc[start:]
            spy_perf_o = perf(sr.loc[OOS_START:])
            conv = ([("RAW", None, None)]
                    + [(f"CE{th}", th, "CE") for th in THETAS]
                    + [(f"EM{th}", th, "EM") for th in THETAS])
            for cname, th, kind in conv:
                cands = []
                for b in BANDS:
                    for g in GROSS:
                        gr, tu, gp = books[(pname, b, g, "W")]
                        r = net(gr, tu, c).loc[start:]
                        r_is = r.iloc[:is_end_pos + 1]
                        pi, si = perf(r_is), perf(spy_is)
                        if th is None:
                            dd_ok, n_ep = abs(maxdd(r_is)) <= DD_CAP * abs(maxdd(spy_is)), 1
                        elif kind == "CE":
                            ls = live_start(gp.loc[start:], r.index)
                            bar, bk, n_ep = ce_bar(sr, r, eps[th], ls, is_end_pos)
                            dd_ok = bool(bk <= bar)
                        else:
                            ls = live_start(gp.loc[start:], r.index)
                            em_ok, _wr, _wy, n_ep, _wd = em_check(sr, r, eps[th], ls, is_end_pos)
                            dd_ok = bool(em_ok)
                        if n_ep == 0:
                            continue
                        ok = (pi["Sharpe"] > si["Sharpe"] and dd_ok
                              and pi["CAGR"] >= CAGR_FLOOR * si["CAGR"])
                        if ok:
                            cands.append((pi["Sharpe"], b, g, r))
                if not cands:
                    wf.append(dict(panel=pname, cost=c, convention=cname, pick="NONE ELIGIBLE IS"))
                    say(f"  {pname:9s} {c:.0f}bps {cname:7s}  no (b,g) clears the IS 4b legs")
                    continue
                cands.sort(key=lambda x: -x[0])
                is_sh, b, g, r = cands[0]
                kp = keep_paths(r, sr, base, start)
                po = perf(r.loc[OOS_START:])
                pb_o = perf(base.loc[OOS_START:])
                wf.append(dict(panel=pname, cost=c, convention=cname, pick=f"b{b:.2f}/g{g:.2f}",
                               band=b, gross=g, n_eligible_IS=len(cands), IS_Sharpe=is_sh,
                               OOS_CAGR=po["CAGR"], OOS_Sharpe=po["Sharpe"], OOS_MaxDD=po["MaxDD"],
                               v2_OOS_CAGR=pb_o["CAGR"], v2_OOS_Sharpe=pb_o["Sharpe"],
                               v2_OOS_MaxDD=pb_o["MaxDD"], spy_OOS_CAGR=spy_perf_o["CAGR"],
                               spy_OOS_Sharpe=spy_perf_o["Sharpe"], spy_OOS_MaxDD=spy_perf_o["MaxDD"],
                               full_CAGR=kp["CAGR"], full_Sharpe=kp["Sharpe"], full_MaxDD=kp["MaxDD"],
                               H1=kp["H1"], H2=kp["H2"], keep_4a=kp["fa"], keep_4b=kp["fb"],
                               fb_fail=kp["fb_fail"]))
                say(f"  {pname:9s} {c:.0f}bps {cname:7s}  pick b={b:.2f} g={g:.2f} "
                    f"(of {len(cands):2d} IS-eligible)  OOS {po['CAGR']:6.2%}/{po['Sharpe']:.3f}/"
                    f"{po['MaxDD']:7.2%}  | v2 {pb_o['CAGR']:6.2%}/{pb_o['Sharpe']:.3f} "
                    f"| SPY {spy_perf_o['CAGR']:6.2%}/{spy_perf_o['Sharpe']:.3f}  "
                    f"4a {kp['fa']} 4b {kp['fb']} ({kp['fb_fail']})")
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)

    say("\n  DID ANY PICK MOVE?  (RAW pick vs each CE pick, same panel and rung)")
    moved = 0
    tot = 0
    for pname in panels:
        for c in COSTS:
            raw = W[(W.panel == pname) & (W.cost == c) & (W.convention == "RAW")]
            if raw.empty:
                continue
            rp = raw.pick.iloc[0]
            for cn in [f"CE{th}" for th in THETAS] + [f"EM{th}" for th in THETAS]:
                ce = W[(W.panel == pname) & (W.cost == c) & (W.convention == cn)]
                if ce.empty:
                    continue
                tot += 1
                same = ce.pick.iloc[0] == rp
                moved += (not same)
                say(f"    {pname:9s} {c:.0f}bps  RAW {rp:12s} vs {cn:7s} {ce.pick.iloc[0]:12s}"
                    f"  {'SAME' if same else '*** MOVED ***'}")
    say(f"\n  H_PICK ({'HOLDS' if moved > 0 else 'FAILS'}): {moved} of {tot} "
        f"(panel x rung x convention) picks move under the re-based bar")

    say("\n  Baselines on the same windows (weekly, next-day, PROTO rung):")
    for pname, px in panels.items():
        start = px.index[WARM]
        sr = px["SPY"].pct_change().fillna(0.0).loc[start:]
        bg, bt, _ = fast_backtest(px, rules_v2_weights(px.drop(columns=["SPY"], errors="ignore"))
                                  .reindex(columns=px.columns).fillna(0.0), freq="W")
        b = net(bg, bt, PROTO_COST).loc[start:]
        h = len(b) // 2
        pb, ps = perf(b), perf(sr)
        say(f"    {pname:9s} RULES v2 full {pb['CAGR']:6.2%}/{pb['Sharpe']:.3f}/{pb['MaxDD']:7.2%}"
            f"  H1 {perf(b.iloc[:h])['Sharpe']:.3f} H2 {perf(b.iloc[h:])['Sharpe']:.3f}"
            f"  OOS {perf(b.loc[OOS_START:])['CAGR']:6.2%}/{perf(b.loc[OOS_START:])['Sharpe']:.3f}")
        say(f"    {'':9s} SPY      full {ps['CAGR']:6.2%}/{ps['Sharpe']:.3f}/{ps['MaxDD']:7.2%}"
            f"  H1 {perf(sr.iloc[:h])['Sharpe']:.3f} H2 {perf(sr.iloc[h:])['Sharpe']:.3f}"
            f"  OOS {perf(sr.loc[OOS_START:])['CAGR']:6.2%}/{perf(sr.loc[OOS_START:])['Sharpe']:.3f}")

    # ---------------------------------------------------------- PART 4: census
    say("\n" + "=" * 100)
    say("PART 4  CENSUS - how much of the record's rule-8 output can be re-read FROM DISK?")
    say("=" * 100)
    crows = []
    for p in sorted((ROOT / "research" / "backtests").glob("*.walkforward.csv")):
        try:
            d = pd.read_csv(p, nrows=5)
        except Exception as e:
            crows.append(dict(file=p.name, n_cols=0, readable=False, has_IS_dd=False,
                              has_spy_IS_dd=False, note=type(e).__name__))
            continue
        cols = [c.lower() for c in d.columns]
        has_is_dd = any(("is" in c and ("maxdd" in c or "dd" == c.split("_")[-1])) for c in cols)
        has_spy_is = any(("spy" in c and "is" in c and "dd" in c) for c in cols)
        crows.append(dict(file=p.name, n_cols=len(d.columns), readable=True,
                          has_IS_dd=has_is_dd, has_spy_IS_dd=has_spy_is,
                          rereadable=bool(has_is_dd and has_spy_is), note=""))
    C = pd.DataFrame(crows)
    C.to_csv(f"{OUT}.census.csv", index=False)
    n = len(C)
    say(f"  {n} committed *.walkforward.csv files in research/backtests/")
    say(f"    carry an IS-side book MaxDD column      : {int(C.has_IS_dd.sum())} ({C.has_IS_dd.mean():.1%})")
    say(f"    carry an IS-side SPY  MaxDD column      : {int(C.has_spy_IS_dd.sum())} ({C.has_spy_IS_dd.mean():.1%})")
    say(f"    carry BOTH, i.e. their IS DD gate can be re-read from disk without re-running "
        f"the script: {int(C.get('rereadable', pd.Series(dtype=bool)).sum())}")
    say("  HONEST LIMIT: the record publishes the PICK and its OOS metrics, not the IS-side")
    say("  bar it was chosen under, so 'every committed rule-8 pick' cannot be re-read from")
    say("  the committed CSVs.  The rebuild above is the answer that IS available: the same")
    say("  chooser, the same book family, the same two dials, run under both conventions.")

    # ---------------------------------------------------------- verdict
    say("\n" + "=" * 100)
    say("PRE-REGISTERED HYPOTHESES")
    say("=" * 100)
    say("  G1 PASS   G2 PASS   G3 PASS   G4 PASS")
    say(f"  H_MISMATCH  {'HOLDS' if hm >= 0.80 else 'FAILS'}   (min panel mismatch {hm:.0%} vs 80%)")
    say(f"  H_BAR       {'HOLDS' if drop_pp >= 5.0 else 'FAILS'}   (median bar falls {drop_pp:.2f} pp vs 5 pp)")
    say(f"  H_VERDICT   {'HOLDS' if fr >= 0.10 else 'FAILS'}   (flip rate {fr:.1%} vs 10%)")
    say(f"  H_PICK      {'HOLDS' if moved > 0 else 'FAILS'}   ({moved}/{tot} picks move)")
    Path(f"{OUT}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
