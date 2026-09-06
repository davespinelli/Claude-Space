#!/usr/bin/env python3
"""QUEUE idea 72 — ew-all-broad-as-the-simple-book (lane B, 2026-09-06).

The question
------------
Idea 10/72's `B136/EWall` passes 4b (10.7% / 1.027 / -17.7%, halves 1.146/0.917,
OOS 1.021) with NO ranking, no vol scaler and no universe choice.  It is the
simplest 4b-passing object the project owns.  The queue asks for it head-to-head
against the three candidates that DO rank:

    EWall      idea 72 : equal-weight every eligible name (200d & vol20<0.60), 75% gross
    top20      idea 2  : composite (no vol scaler), top 20 at 0.75/20  -- the standing KEEP
    frac085    idea 46 : composite, top ceil(0.85 x E_t) at 0.75/k     -- always 75% gross
    ew-band3   idea 57 : EWall with a +/-3% band around the 200d MA    -- always 75% gross
    v1                 : the live RULES v1 book, as the 4a reference

on BOTH universes, at 5/10/25 bps, and under idea 65's cadence-insensitivity bar.

Two corrections the record has learned SINCE idea 72 was queued, both applied here
------------------------------------------------------------------------------------
(A) GROSS (idea 81, today).  `top20` is the only one of the five whose realised gross
    is not 75%: it holds 0.75/20 per name and simply goes to cash when fewer than 20
    names are eligible.  Every published head-to-head against EWall has therefore
    compared two books at DIFFERENT average exposure, and idea 66 established that
    gross is an exact lever.  So each book is run under two conventions:

      LIT    the book exactly as published.
      MATCH  the SAME return stream levered by a constant g = 0.75 / (own mean realised
             gross), i.e. idea 66's exact static lever (scale return AND turnover, the
             remainder in cash at 0%).  All five books then carry the same average
             exposure and the 4b CAGR floor / DD cap compare like with like.

    Because the lever is exact, MATCH leaves every Sharpe UNCHANGED (asserted, gate G3)
    and moves only CAGR and MaxDD.  That is the point: 4b's two ABSOLUTE bars are the
    ones a gross mismatch corrupts, and they are the bars this head-to-head turns on.

(B) RANKABILITY (idea 155).  A name can clear the 200d/vol20 gate while its composite
    is NaN (200 days of history, not the 252 the 12-1 leg needs).  EWall and ew-band3
    then hold names the ranked books CANNOT hold, so part of any EWall-vs-ranked gap is
    coverage, not ranking.  Both equal-weight books are also run on the RANKABLE
    eligible set and the size of the change is printed rather than assumed away.

Design (PROTOCOL rules 1-8)
---------------------------
Panels    : universe.json (u56) and universe_broad.json (B136).  Both are
            CURRENT-CONSTITUENT lists (idea 54) — survivorship is common to all five
            books on the same days, so it cancels in the head-to-head DIFFERENCES and
            does NOT cancel in any level quoted.
Books     : five FIXED, published objects imported from idea 89's audit module rather
            than re-implemented.  No book has a parameter tuned in this run.
Tuned     : exactly TWO dimensions — CADENCE in {D, W, M} and CONVENTION in {LIT, MATCH}
            = 6 grid points, ALL reported.  Cost rung (5/10/25 bps), panel and book are
            reported at every value and are never selected on.
Costs     : one 0-bps simulation per (panel, book, cadence); 5/10/25 bps derived
            analytically as gross - turnover x bps/1e4 (identity asserted, gate G1).
Execution : PROTOCOL rule 2 throughout (weights decided at close t, applied at close t+1;
            `engine.backtest` does this).
Rule 8    : IS <= 2016-12-31 chooses the BOOK and the CADENCE; OOS >= 2017-01-01 read
            ONCE, against RULES v1, SPY and the do-nothing EWall control.
Bars      : both KEEP paths on every arm (4a vs the live book, 4b vs SPY).

Idea 65's cadence bar, made explicit
-------------------------------------
Idea 3 reported `ew-band3` as the only book whose 4b pass survived every cadence
(dSharpe -0.03..+0.00 across D/W/M) while top20 swung +0.11 and v1 +0.30.  The
statistic here is SWING = max(Sharpe) - min(Sharpe) over {D, W, M} within a
(panel, book, convention, cost) cell, plus the count of cadences at which the cell's
4b verdict holds.  A book that passes 4b at one cadence only is passing on a dial.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P1  `top20`'s mean realised gross is below 0.75 on BOTH panels, so MATCH levers it UP
      and deepens its MaxDD; at least one of its published 4b passes dies on the DD cap
      under MATCH.
  P2  MATCH moves no Sharpe by more than 1e-9 (idea 66 as an identity).
  P3  EWall does NOT pass 4b on both panels at 25 bps (idea 82 put its cross-universe
      breakeven at ~0 bps).
  P4  `ew-band3` has the smallest cadence SWING of the five books, on both panels
      (idea 3 / idea 65).
  P5  The rankability correction moves B136/EWall's Sharpe by less than 0.01 (idea 155
      measured 1.0261 -> 1.0253) and u56's by less still.
  P6  Rule 8's IS chooser does NOT pick EWall on either panel — the simplest book is not
      the in-sample winner — and the picked book beats EWall OOS in at most 1 of 2 panels.

CAVEATS carried, not buried
----------------------------
  * Current-constituent survivorship on both panels (idea 54).  It flatters EWall MORE
    than the ranked books, since EWall holds the whole beaten-down cohort a
    delisting-aware panel would kill (idea 155's caveat) — so a KILL of EWall here is
    conservative and a KEEP of it is not.
  * MaxDD is a single realised extremum and is the noisiest column in this run (idea 117).
  * MATCH re-levers with a CONSTANT chosen on the full sample; it is a diagnostic
    convention, not a tradable rule, and no level under MATCH is a tradable estimate.
  * Costs are flat linear bps on turnover, not spread-and-impact (idea 126).
  * Daily cadence at 25 bps is a stress rung, not a proposal.
  * The small panel is deliberately excluded (ideas 39/49/136: the gate is inverted there).

Deterministic, standalone.  Writes .console.txt, .grid.csv, .cadence.csv, .walkforward.csv
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

HERE = Path(__file__).resolve()
STEM = HERE.with_suffix("")


def _load(fname, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "research" / "backtests" / fname)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# idea 89's audit module owns the canonical construction of all four candidate books.
i89 = _load("2026-09-04_one-year-leverage-audit_cloud.py", "i89")
composite = i89.composite
eligible = i89.eligible
GROSS = i89.GROSS

COSTS = [5, 10, 25]
PROTO_COST = 10
CADENCES = ["D", "W", "M"]
CONVS = ["LIT", "MATCH"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
BOOKS = ["EWall", "top20", "frac085", "ew-band3", "v1"]
SIMPLE = "EWall"

_OUT = []


def P(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    _OUT.append(line)


# ------------------------------------------------------------------ constructions
def w_book(px, book, rankable=False):
    """The five published books.  `rankable=True` applies idea 155's correction to the
    two equal-weight books (drop eligible-but-unrankable names)."""
    if book == "v1":
        return rules_v1_weights(px)
    if book == "top20":
        return i89.w_top20(px)
    if book == "frac085":
        return i89.w_frac085(px)
    gate = "band3" if book == "ew-band3" else "200d"
    e = eligible(px, gate)
    if rankable:
        e = e & composite(px).notna()
    e = e.astype(float)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * GROSS


def sim(px, w, cadence):
    """Zero-cost simulation.  Returns (gross returns, turnover, realised gross)."""
    res = backtest(px, w, cost_bps=0.0, freq=cadence)
    return res["returns"], res["turnover"], res["weights"].sum(axis=1)


def at_cost(gross, turn, bps):
    return gross - turn * bps / 1e4


def m3(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def turn_per_yr(t):
    return t.sum() / (len(t) / 252)


def fail4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    bad = []
    if h1 <= b1: bad.append("H1")
    if h2 <= b2: bad.append("H2")
    if m3(r)[2] < m3(base)[2]: bad.append("DD")
    return bad


def fail4b(r, spy, oos_sh, spy_oos_sh):
    c, s, dd = m3(r)
    h1, h2 = halves(r)
    sc, ss, sdd = m3(spy)
    s1, s2 = halves(spy)
    bad = []
    if h1 <= s1: bad.append("H1")
    if h2 <= s2: bad.append("H2")
    if oos_sh <= spy_oos_sh: bad.append("OOS")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


# ------------------------------------------------------------------ gates
def gates(px56, px136):
    P("=" * 108)
    P("GATE G1-G4 — reproduction BEFORE any new number is read")
    P("=" * 108)

    # G1: analytic cost == engine's own cost accounting.
    w = w_book(px56, "EWall")
    g, t, _ = sim(px56, w, "W")
    direct = backtest(px56, w, cost_bps=PROTO_COST, freq="W")["returns"]
    d1 = float((at_cost(g, t, PROTO_COST) - direct).abs().max())
    P(f"  G1 analytic 10bps vs engine cost_bps=10        max|diff| = {d1:.3e}")

    # G2: the four published rows.
    start56, start136 = px56.index[260], px136.index[260]
    for panel, px, start, book, want in [
        ("u56", px56, start56, "top20", "idea 2  12.7% / 1.093 / -18.3%"),
        ("B136", px136, start136, "EWall", "idea 72 10.7% / 1.027 / -17.7%"),
        ("B136", px136, start136, "ew-band3", "idea 57 11.1% / 1.064 / -16.8%"),
        ("u56", px56, start56, "v1", "live     6.5% / 0.664 / -13.8%"),
    ]:
        gg, tt, _ = sim(px, w_book(px, book), "W")
        r = at_cost(gg, tt, PROTO_COST).loc[start:]
        c, s, dd = m3(r)
        h1, h2 = halves(r)
        P(f"  G2 {panel:>5}/{book:<9} {c:7.3%} / {s:.4f} / {dd:7.3%}  halves {h1:.3f}/{h2:.3f}"
          f"   [published: {want}]")

    # G3: MATCH is Sharpe-exact (idea 66).
    gg, tt, inv = sim(px56, w_book(px56, "top20"), "W")
    r = at_cost(gg, tt, PROTO_COST).loc[start56:]
    lev = GROSS / inv.loc[start56:].mean()
    rm = at_cost(gg * lev, tt * lev, PROTO_COST).loc[start56:]
    P(f"  G3 MATCH lever on u56/top20 g={lev:.4f}  |dSharpe| = "
      f"{abs(m3(rm)[1] - m3(r)[1]):.3e}   (idea 66: exact)")

    # G4: idea 155's rankability channel.
    for panel, px, start in [("u56", px56, start56), ("B136", px136, start136)]:
        for book in ["EWall", "ew-band3"]:
            a = at_cost(*sim(px, w_book(px, book), "W")[:2], PROTO_COST).loc[start:]
            b = at_cost(*sim(px, w_book(px, book, rankable=True), "W")[:2], PROTO_COST).loc[start:]
            P(f"  G4 {panel:>5}/{book:<9} Sharpe plain {m3(a)[1]:.4f} -> rankable "
              f"{m3(b)[1]:.4f}  (d {m3(b)[1] - m3(a)[1]:+.4f})")
    return d1


# ------------------------------------------------------------------ the sweep
def sweep(px, panel, rows):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    spy_oos = spy.loc[OOS_START:]
    spy_oos_sh = m3(spy_oos)[1]
    base_r = {}
    raw = {}

    for book in BOOKS:
        for cad in CADENCES:
            g, t, inv = sim(px, w_book(px, book), cad)
            g, t, inv = g.loc[start:], t.loc[start:], inv.loc[start:]
            raw[(book, cad)] = (g, t, float(inv.mean()))

    for cad in CADENCES:
        base_r[cad] = at_cost(*raw[("v1", cad)][:2], PROTO_COST)

    for book in BOOKS:
        for cad in CADENCES:
            g, t, mg = raw[(book, cad)]
            for conv in CONVS:
                lev = 1.0 if conv == "LIT" else GROSS / mg
                gl, tl = g * lev, t * lev
                for bps in COSTS:
                    r = at_cost(gl, tl, bps)
                    c, s, dd = m3(r)
                    h1, h2 = halves(r)
                    oos = r.loc[OOS_START:]
                    oc, os_, odd = m3(oos)
                    a = fail4a(r, base_r[cad])
                    b = fail4b(r, spy, os_, spy_oos_sh)
                    rows.append(dict(panel=panel, book=book, cadence=cad, conv=conv, bps=bps,
                                     gross=mg, lever=lev, CAGR=c, Sharpe=s, MaxDD=dd,
                                     H1=h1, H2=h2, OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd,
                                     turn=turn_per_yr(t), pass4a=not a, pass4b=not b,
                                     fail4a=",".join(a) or "-", fail4b=",".join(b) or "-"))
    return spy, spy_oos_sh, base_r, raw


# ------------------------------------------------------------------ rule 8
def rule8(px, panel, raw, spy):
    """Book AND cadence chosen on 2009-2016 ONLY (max IS Sharpe at the PROTOCOL rung);
    2017-2026 read once.  Reported under both conventions."""
    start = px.index[260]
    spy_oos = spy.loc[OOS_START:]
    out = []
    for conv in CONVS:
        for bps in COSTS:
            best, bestS = None, -np.inf
            for book in BOOKS:
                for cad in CADENCES:
                    g, t, mg = raw[(book, cad)]
                    lev = 1.0 if conv == "LIT" else GROSS / mg
                    r = at_cost(g * lev, t * lev, bps)
                    s_is = m3(r.loc[:IS_END])[1]
                    if s_is > bestS:
                        bestS, best = s_is, (book, cad, lev)
            book, cad, lev = best
            g, t, mg = raw[(book, cad)]
            r_oos = at_cost(g * lev, t * lev, bps).loc[OOS_START:]
            gS, tS, mgS = raw[(SIMPLE, "W")]
            levS = 1.0 if conv == "LIT" else GROSS / mgS
            s_oos = at_cost(gS * levS, tS * levS, bps).loc[OOS_START:]
            gv, tv, mgv = raw[("v1", "W")]
            v_oos = at_cost(gv, tv, bps).loc[OOS_START:]
            out.append(dict(panel=panel, conv=conv, bps=bps, pick=f"{book}/{cad}",
                            IS_Sharpe=bestS,
                            OOS_CAGR=m3(r_oos)[0], OOS_Sharpe=m3(r_oos)[1], OOS_MaxDD=m3(r_oos)[2],
                            ctrl_CAGR=m3(s_oos)[0], ctrl_Sharpe=m3(s_oos)[1], ctrl_MaxDD=m3(s_oos)[2],
                            v1_Sharpe=m3(v_oos)[1],
                            spy_CAGR=m3(spy_oos)[0], spy_Sharpe=m3(spy_oos)[1],
                            spy_MaxDD=m3(spy_oos)[2],
                            regret=m3(s_oos)[1] - m3(r_oos)[1]))
    return out


# ------------------------------------------------------------------ main
def main():
    pd.set_option("display.width", 200)
    px56 = load_universe()
    px136 = load_universe(broad=True)
    P(f"u56  {px56.shape[1]} cols {px56.index[0].date()}..{px56.index[-1].date()}   "
      f"B136 {px136.shape[1]} cols {px136.index[0].date()}..{px136.index[-1].date()}")
    gates(px56, px136)

    rows, w8 = [], []
    for panel, px in [("u56", px56), ("B136", px136)]:
        spy, spy_oos_sh, base_r, raw = sweep(px, panel, rows)
        start = px.index[260]
        c, s, dd = m3(spy)
        h1, h2 = halves(spy)
        P("")
        P("=" * 108)
        P(f"PANEL {panel} — SPY {c:.2%} / {s:.3f} / {dd:.2%} halves {h1:.3f}/{h2:.3f}, "
          f"OOS Sharpe {spy_oos_sh:.3f}; 4b bars: CAGR >= {0.70 * c:.2%}, MaxDD >= {0.60 * dd:.2%}")
        P("=" * 108)
        w8 += rule8(px, panel, raw, spy)

    df = pd.DataFrame(rows)
    df.to_csv(f"{STEM}.grid.csv", index=False)

    # ---------- Q1 the head-to-head, every grid point
    P("")
    P("=" * 118)
    P("Q1 — THE HEAD-TO-HEAD, all 180 grid points (2 panels x 5 books x 3 cadences x "
      "2 conventions x 3 cost rungs)")
    P("=" * 118)
    for panel in ["u56", "B136"]:
        for conv in CONVS:
            P("")
            P(f"  --- {panel} / {conv} " + "-" * 90)
            P(f"  {'book':<9}{'cad':<4}{'bps':>4}{'gross':>7}{'lev':>6}{'CAGR':>8}{'Sharpe':>8}"
              f"{'MaxDD':>8}{'H1':>7}{'H2':>7}{'OOSsh':>7}{'turn':>7}  {'4a':<12}{'4b'}")
            for book in BOOKS:
                for cad in CADENCES:
                    for bps in COSTS:
                        r = df[(df.panel == panel) & (df.book == book) & (df.cadence == cad)
                               & (df.conv == conv) & (df.bps == bps)].iloc[0]
                        P(f"  {book:<9}{cad:<4}{bps:>4}{r.gross:>7.3f}{r.lever:>6.2f}"
                          f"{r.CAGR:>8.2%}{r.Sharpe:>8.3f}{r.MaxDD:>8.2%}{r.H1:>7.3f}"
                          f"{r.H2:>7.3f}{r.OOS_Sharpe:>7.3f}{r.turn:>7.1f}  "
                          f"{('PASS' if r.pass4a else 'KILL ' + r.fail4a):<12}"
                          f"{'PASS' if r.pass4b else 'KILL ' + r.fail4b}")

    # ---------- Q2 does the simplest book win?
    P("")
    P("=" * 108)
    P("Q2 — IS THE SIMPLEST BOOK THE BEST BOOK?  EWall minus each ranked candidate, "
      "paired on (panel, cadence, conv, cost)")
    P("=" * 108)
    P(f"  {'vs':<10}{'cells':>7}{'dSharpe':>10}{'win':>6}{'dCAGR':>9}{'win':>6}"
      f"{'dMaxDD':>9}{'shallower':>11}{'dOOSsh':>9}{'win':>6}")
    for book in [b for b in BOOKS if b != SIMPLE]:
        a = df[df.book == SIMPLE].set_index(["panel", "cadence", "conv", "bps"]).sort_index()
        b = df[df.book == book].set_index(["panel", "cadence", "conv", "bps"]).sort_index()
        ds, dc = a.Sharpe - b.Sharpe, a.CAGR - b.CAGR
        dd, do = a.MaxDD - b.MaxDD, a.OOS_Sharpe - b.OOS_Sharpe
        P(f"  {book:<10}{len(ds):>7}{ds.mean():>+10.4f}{(ds > 0).sum():>4}/{len(ds):<2}"
          f"{dc.mean():>+9.2%}{(dc > 0).sum():>4}/{len(dc):<2}"
          f"{dd.mean():>+9.2%}{(dd > 0).sum():>8}/{len(dd):<2}"
          f"{do.mean():>+9.4f}{(do > 0).sum():>4}/{len(do):<2}")

    P("")
    P("  KEEP-path census over all 180 grid points:")
    P(f"  {'book':<10}{'4a':>8}{'4b':>8}   {'4b passes on BOTH panels at the same '}"
      f"{'(cad, conv, bps)'}")
    for book in BOOKS:
        d = df[df.book == book]
        both = 0
        cells = []
        for cad in CADENCES:
            for conv in CONVS:
                for bps in COSTS:
                    q = d[(d.cadence == cad) & (d.conv == conv) & (d.bps == bps)]
                    if len(q) == 2 and q.pass4b.all():
                        both += 1
                        cells.append(f"{cad}/{conv}/{bps}")
        P(f"  {book:<10}{d.pass4a.sum():>4}/{len(d):<3}{d.pass4b.sum():>4}/{len(d):<3}"
          f"   {both:>2}/18  {' '.join(cells) if cells else '(none)'}")

    P("")
    P("  first-failing 4b bar, counted over all 180 points:")
    for bar in ["H1", "H2", "OOS", "DD", "CAGR"]:
        P(f"    {bar:<5}{int(df.fail4b.str.split(',').apply(lambda x: bar in x).sum()):>5}")

    # ---------- Q3 the gross correction
    P("")
    P("=" * 108)
    P("Q3 — THE GROSS CORRECTION (idea 81).  Mean realised gross, and what MATCH does "
      "to each book's verdict")
    P("=" * 108)
    P(f"  {'panel':<6}{'book':<10}{'gross':>7}{'lever':>7}   "
      f"{'LIT (10bps) CAGR/Sharpe/MaxDD':>34}   {'MATCH (10bps)':>32}   4b LIT -> MATCH")
    for panel in ["u56", "B136"]:
        for book in BOOKS:
            l = df[(df.panel == panel) & (df.book == book) & (df.cadence == "W")
                   & (df.conv == "LIT") & (df.bps == PROTO_COST)].iloc[0]
            mm = df[(df.panel == panel) & (df.book == book) & (df.cadence == "W")
                    & (df.conv == "MATCH") & (df.bps == PROTO_COST)].iloc[0]
            P(f"  {panel:<6}{book:<10}{l.gross:>7.3f}{mm.lever:>7.3f}   "
              f"{l.CAGR:>12.2%}{l.Sharpe:>10.3f}{l.MaxDD:>12.2%}   "
              f"{mm.CAGR:>10.2%}{mm.Sharpe:>9.3f}{mm.MaxDD:>11.2%}   "
              f"{('PASS' if l.pass4b else 'KILL ' + l.fail4b)} -> "
              f"{('PASS' if mm.pass4b else 'KILL ' + mm.fail4b)}")
    flips = 0
    for _, g in df.groupby(["panel", "book", "cadence", "bps"]):
        a = g[g.conv == "LIT"].iloc[0]
        b = g[g.conv == "MATCH"].iloc[0]
        flips += int(a.pass4b != b.pass4b)
    P(f"  4b verdict differs between LIT and MATCH in {flips} of 90 (panel, book, cadence, "
      f"cost) cells; max |dSharpe| across all of them "
      f"{max(abs(g[g.conv == 'LIT'].iloc[0].Sharpe - g[g.conv == 'MATCH'].iloc[0].Sharpe) for _, g in df.groupby(['panel', 'book', 'cadence', 'bps'])):.2e}")

    # ---------- Q4 cadence-insensitivity (idea 65)
    P("")
    P("=" * 108)
    P("Q4 — IDEA 65's CADENCE-INSENSITIVITY BAR.  SWING = max-min Sharpe over {D,W,M}; "
      "4b/3 = cadences passing 4b")
    P("=" * 108)
    P(f"  {'panel':<6}{'book':<10}{'conv':<7}{'bps':>4}{'D':>8}{'W':>8}{'M':>8}"
      f"{'SWING':>8}{'4b/3':>7}")
    cad_rows = []
    for panel in ["u56", "B136"]:
        for book in BOOKS:
            for conv in CONVS:
                for bps in COSTS:
                    q = df[(df.panel == panel) & (df.book == book) & (df.conv == conv)
                           & (df.bps == bps)].set_index("cadence")
                    sh = {c: q.loc[c].Sharpe for c in CADENCES}
                    swing = max(sh.values()) - min(sh.values())
                    n4b = int(q.pass4b.sum())
                    cad_rows.append(dict(panel=panel, book=book, conv=conv, bps=bps,
                                         D=sh["D"], W=sh["W"], M=sh["M"], swing=swing, n4b=n4b))
                    P(f"  {panel:<6}{book:<10}{conv:<7}{bps:>4}{sh['D']:>8.3f}{sh['W']:>8.3f}"
                      f"{sh['M']:>8.3f}{swing:>8.3f}{n4b:>5}/3")
    cd = pd.DataFrame(cad_rows)
    cd.to_csv(f"{STEM}.cadence.csv", index=False)
    P("")
    P("  mean SWING by book (lower = more cadence-insensitive):")
    for book, v in cd.groupby("book").swing.mean().sort_values().items():
        sub = cd[cd.book == book]
        P(f"    {book:<10}{v:>8.4f}   worst cell {sub.swing.max():.4f}   "
          f"cells passing 4b at all 3 cadences: {int((sub.n4b == 3).sum())}/{len(sub)}")

    # ---------- Q5 rule 8
    P("")
    P("=" * 108)
    P("Q5 — RULE 8.  Book AND cadence chosen on 2009-2016 ONLY; 2017-2026 read ONCE.")
    P("=" * 108)
    wf = pd.DataFrame(w8)
    wf.to_csv(f"{STEM}.walkforward.csv", index=False)
    P(f"  {'panel':<6}{'conv':<7}{'bps':>4}{'IS pick':>14}{'IS sh':>8}   "
      f"{'OOS CAGR/Sharpe/MaxDD':>28}   {'EWall/W control OOS':>26}{'regret':>9}"
      f"{'v1 OOS':>8}{'SPY OOS':>9}")
    for _, r in wf.iterrows():
        P(f"  {r.panel:<6}{r.conv:<7}{r.bps:>4}{r['pick']:>14}{r.IS_Sharpe:>8.3f}   "
          f"{r.OOS_CAGR:>10.2%}{r.OOS_Sharpe:>9.3f}{r.OOS_MaxDD:>9.2%}   "
          f"{r.ctrl_CAGR:>9.2%}{r.ctrl_Sharpe:>8.3f}{r.ctrl_MaxDD:>9.2%}"
          f"{r.regret:>+9.4f}{r.v1_Sharpe:>8.3f}{r.spy_Sharpe:>9.3f}")
    P(f"  IS chooser picks {SIMPLE} in {int((wf['pick'].str.startswith(SIMPLE)).sum())} of "
      f"{len(wf)} cells; the do-nothing {SIMPLE}/W control beats the IS pick OOS in "
      f"{int((wf.regret > 0).sum())} of {len(wf)}; mean regret {wf.regret.mean():+.4f}")

    # ---------- Q6 rankability
    P("")
    P("=" * 108)
    P("Q6 — IDEA 155's RANKABILITY CORRECTION on the two equal-weight books (W, 10 bps)")
    P("=" * 108)
    P(f"  {'panel':<6}{'book':<10}{'plain CAGR/Sharpe/MaxDD':>32}   {'rankable':>30}")
    for panel, px in [("u56", px56), ("B136", px136)]:
        start = px.index[260]
        for book in ["EWall", "ew-band3"]:
            a = at_cost(*sim(px, w_book(px, book), "W")[:2], PROTO_COST).loc[start:]
            b = at_cost(*sim(px, w_book(px, book, rankable=True), "W")[:2], PROTO_COST).loc[start:]
            ca, sa, da = m3(a)
            cb, sb, db = m3(b)
            P(f"  {panel:<6}{book:<10}{ca:>12.2%}{sa:>10.4f}{da:>10.2%}   "
              f"{cb:>10.2%}{sb:>10.4f}{db:>10.2%}   (dSharpe {sb - sa:+.4f})")

    with open(f"{STEM}.console.txt", "w") as f:
        f.write("\n".join(_OUT) + "\n")
    print(f"\nwrote {STEM}.console.txt / .grid.csv / .cadence.csv / .walkforward.csv")


if __name__ == "__main__":
    main()
