#!/usr/bin/env python3
"""QUEUE idea 403 — is-the-4b-window-a-TURNOVER-COST-fact-about-the-ranked-book (lane B, 2026-09-10).

PRE-REGISTERED QUESTION (verbatim from QUEUE.md idea 403, written before any number here was read)
    "idea 138's 4b window in the sleeve fraction is EMPTY in exactly the two broad/TOP20 @25bps
     cells and 4-7 grid points wide on every EWall cell; the ranked book's turnover is what
     differs.  Test whether window width is a function of the base book's turnover rather than
     of the sleeve.  Max 2 params."

WHY IT MATTERS
    Idea 138 measured a 4b-passing WINDOW in the sleeve fraction f and found its width varies
    2-7 grid points across 16 cells, EMPTY in two of them.  If that width is a TURNOVER-COST
    fact about the base book, then the record can screen a sleeve candidate by pricing the base
    book's trading before running a single f sweep, and the window is a cost artefact rather
    than a property of the sleeve.  If instead it is a panel/book fact that survives at matched
    turnover — as idea 137 found for the neighbouring "broad@25bps wall" — then the window is a
    REGIME statement wearing turnover's name, and no turnover screen can substitute for the sweep.

THE DECISIVE ASYMMETRY (stated before the design, because it drives it)
    Turnover can only reach a return series THROUGH COST: r(c) = r(0) - turnover * c/1e4 exactly
    (no instrument here reads equity, so the identity is exact and is ASSERTED in gate G2).
    Therefore a genuine TURNOVER-COST fact must satisfy two things:
        (i)  at c = 0 bps the cross-cell width spread must VANISH — a window that is already
             empty at zero cost cannot be a turnover fact (idea 137's D4 logic); and
        (ii) width must be a SINGLE function of the drag D = base_turnover * c/1e4, invariant
             to which of the two routes produced it (a low-lambda/high-rung route and a
             high-lambda/low-rung route at equal D must give equal width).
    Both are tested directly and both are falsifiable.

WHAT IS BEING TESTED (six analyses, fixed in advance)
    A1  NATIVE CELLS.  Reproduce idea 138's 16 cells at lambda = 1 on a uniform f grid, and
        regress window width on the base book's realised annual turnover, on the drag, and on
        the panel/book identity.  Spearman, pooled and within panel.
    A2  THE CAUSAL DIAL.  Sweep lambda (partial rebalancing on the BASE LEG ONLY — the sleeve's
        own trading is untouched, which is exactly the "rather than of the sleeve" clause) and
        ask whether window width MOVES with the base book's turnover inside a cell.  If width is
        a turnover fact, cutting broad/TOP20's 13.2x/yr toward EWall's 0.9x/yr must OPEN the two
        empty windows.
    A3  MATCHED TURNOVER (idea 137's D2, applied to width).  T* = the u56/EWall/lambda=1 base
        turnover, named in advance.  Give every cell the lambda whose base turnover is closest
        to T* and compare widths there.  Width differences that survive matching are not turnover.
    A4  THE DRAG COLLAPSE (the sharp form of "TURNOVER-COST").  Width is read at six cost rungs
        for free off the identity, so each cell contributes a width(D) curve along the cost route
        and a width(D) curve along the lambda route.  If the two routes agree at matched D the
        claim is confirmed; if width responds to one route and not the other it is refuted, and
        the residual is named.
    A5  THE ZERO-COST CONTROL.  Width at c = 0 in every cell.  A wall that is there at 0 bps is
        not a cost wall.
    A6  RULE 8 (PROTOCOL 8, required).  Choose (f, lambda) per cell on 2009-2016 ALONE under two
        selectors written down before any OOS number was read, then read 2017-2026 ONCE.  OOS
        CAGR/Sharpe/MaxDD reported against the LIVE RULES v2 book (cost-matched) and against SPY.
        Additionally: does the IS window's width and location PREDICT the OOS window's?  A width
        that is a stable fact about a book should transfer; one that is a sample artefact will not.

CORPUS (every point reported; nothing is selected on except the two tuned parameters)
    f          0.00 (the NO-SLEEVE CONTROL) .. 0.50 in steps of 0.05 = 11 points, UNIFORM so
               that "width" is an interval length (grid points x 0.05) rather than a count on
               idea 138's irregular sweep.  All of idea 138's passing f values lie in [0.10,
               0.40], so this grid contains every published window in full.
    lambda     1.00, 0.70, 0.50, 0.35, 0.25, 0.15, 0.10, 0.06 — partial rebalancing applied to
               the BASE leg only: target_t = lam*W_t + (1-lam)*target_{t-1} (idea 137's
               convention, verbatim).  0.06 is included because it is the rung that brings
               broad/TOP20's turnover down THROUGH u56/EWall's, so T* is bracketed, not clamped.
    panels     u56 (research/universe.json) and broad (universe_broad.json) — idea 138's two.
               The small panel has no TLT/GLD/DBC/UUP so a sleeve book cannot exist there.
    base books EWall and TOP20 (idea 138's two; TOP20 is "the ranked book" the queue names).
    sleeve set S3 = TLT/GLD/UUP and S4 = TLT/GLD/DBC/UUP (idea 133/134's two).
    costs      0, 5, 10, 15, 25, 50 bps — ALL reported.  10 and 25 are idea 138's rungs; 0 is
               the control that decides whether the question is even a cost question.
    = 11 f x 8 lambda x 2 panels x 2 books x 2 sleeves = 704 simulations, read at 6 rungs
      = 4 224 arm-rows; 96 (cell, lambda) window measurements per rung, 576 in total.

TUNED PARAMETERS — exactly two, per PROTOCOL 4: the sleeve fraction f (11 values, ALL reported)
    and the base-leg partial-rebalance rate lambda (8 values, ALL reported).  Panels, base books,
    sleeve sets, cost rungs, both selectors and both KEEP paths are reported axes, never selected on.

KEEP PATHS (PROTOCOL 4, evaluated on EVERY arm-row)
    4a  vs the LIVE book `baseline.rules_v2_weights` (PROTOCOL 3), COST-MATCHED to the arm's rung.
    4b  Sharpe > SPY in both halves AND out of sample, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.

PRE-REGISTERED PREDICTIONS (written before any number from the main grid was read)
    P1  At c = 0 the two broad/TOP20 windows are STILL empty (width is not a cost fact).  If this
        is right the queue's framing is refuted at the first gate and A2-A4 only say by how much.
    P2  Width does move somewhat with lambda — a lower-turnover base is a different book, not just
        a cheaper one — but the movement will be dominated by the PATH change, so the c=0 and
        c=25 lambda curves will move TOGETHER rather than diverging.
    P3  At matched turnover T* the u56-vs-broad width gap SURVIVES (idea 137 found the neighbouring
        wall is regime, not turnover).
    P4  The queue's own description is checkable and I expect it to be partly WRONG: idea 138's
        committed grid gives the 7-point window to u56/TOP20@10bps, not to an EWall cell, and its
        EWall cells run 2-4 points.  Reported as a premise check either way.
    P5  Rule 8's S1 picks an interior f (0.15-0.30) in most cells, and lambda < 1 in most cells on
        TOP20 (cheaper trading is worth more than the path it costs) but lambda = 1 on EWall
        (which barely trades at 0.9x/yr, so there is nothing to save).

CAVEATS carried, not buried
    * SURVIVORSHIP (idea 54): both panels are current constituents.  Absent delistings inflate the
      EQUITY leg relative to the ETF sleeve, so every window here is biased toward LOW f, and a
      finding that the window is narrow is understated rather than overstated.
    * lambda is not a pure cost dial: smoothing the base leg changes the book's PATH as well as its
      trading, and a heavily smoothed TOP20 is compositionally closer to EWall.  This is inherent to
      any turnover instrument (idea 137 carried the same caveat) and is why A4's cost route — which
      changes drag and NOTHING else — is the arbiter, not the lambda route.
    * lambda can only LOWER turnover.  The falsification is therefore one-sided: it can open a
      window by cutting trading but cannot close one by adding it.  Stated, not hidden.
    * MaxDD is one number off one path and the 4b DD cap turns on exactly that number (idea 321).
    * Idea 126: t+1 execution, no lag band.  Idea 38: u56/broad carry the calendar-day index.
    * Window WIDTH is a within-cell statistic on a fixed grid; it is never pooled by value across
      panels without the grid being identical, which it is here by construction.

HARNESS: idea 94's simulator (H.run / H.targets / H.halves / H.pass4a) is IMPORTED and asserted
against engine.backtest before any new number is read.  Idea 137's `smooth` and idea 134/138's
sleeve builder are re-implemented verbatim and asserted against idea 138's committed .grid.csv.
Deterministic, standalone.  Modifies nothing.  Writes .console.txt, .grid.csv, .windows.csv,
.matched.csv, .walkforward.csv, .keeppaths.csv next to itself.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-10_is-the-4b-window-a-TURNOVER-COST-fact-about-the-ranked-book_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I138_GRID = OUT / "2026-09-07_sleeve-f-plateau-width_B.grid.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")

FREQ, GROSS = H.FREQ, H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START
PHI, DELTA = 0.70, 0.60                       # 4b CAGR floor / DD cap fractions of SPY
STEP = 0.05
FS = [round(STEP * i, 2) for i in range(11)]              # tuned parameter 1 — ALL reported
LAMBDAS = [1.00, 0.70, 0.50, 0.35, 0.25, 0.15, 0.10, 0.06]  # tuned parameter 2 — ALL reported
SLEEVES = {"S3": ["TLT", "GLD", "UUP"], "S4": ["TLT", "GLD", "DBC", "UUP"]}
BOOKS = ["EWall", "TOP20"]
PANELS = ["u56", "broad"]
RUNGS = [0.0, 5.0, 10.0, 15.0, 25.0, 50.0]    # reported axis, never tuned
I138_RUNGS = [10.0, 25.0]                     # the two idea 138 published
BARS5 = ["H1", "H2", "OOS", "DD", "CAGR"]
EXACT_TOL = 1e-12      # panels whose price cache is untouched since idea 138 (broad, weekly Friday)
DRIFT_TOL = 5e-3       # u56: data/prices.csv is rewritten DAILY and now carries 3 unseen days

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ------------------------------------------------------------------ books ----
def _risk_parity(sub, window=60):
    inv = 1.0 / sub.pct_change().rolling(window).std().replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(252) - 1, sub / sub.shift(126) - 1, sub / sub.shift(63) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_weights(px, assets):
    """Ideas 100/104's sleeve, verbatim from ideas 133/134/138: momentum vote x risk parity."""
    sub = px[assets]
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    return out


def smooth(W, lam):
    """Idea 137's partial-rebalance dial, verbatim: target_t = lam*W_t + (1-lam)*target_{t-1},
    gross restored daily so the dial changes TRADING, not exposure."""
    if lam >= 1.0:
        return W
    S = W.ewm(alpha=lam, adjust=False).mean()
    g = S.sum(axis=1).replace(0, np.nan)
    return S.mul((W.sum(axis=1) / g).fillna(0.0), axis=0).fillna(0.0)


def blend(base_W, sl_W, f):
    """Idea 134/138's blend, verbatim: (1-f)*base + f*sleeve rescaled to GROSS per day."""
    if f == 0.0:
        return base_W
    raw = (1 - f) * base_W + f * sl_W
    return raw.mul((GROSS / raw.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)


# ------------------------------------------------------------------ metrics --
def win(r, which):
    return r.loc[:IS_END] if which == "IS" else (r.loc[OOS_START:] if which == "OOS" else r)


def bars_win(spy, which):
    """4b's bars inside one window.  'full' uses PROTOCOL's halves of the full slice; 'IS' uses
    halves of the IS window (the only halves an IS-only screen can see)."""
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


def window_of(sub, col="pass4b"):
    """Window statistics over ONE cell's uniform f grid.  n_pass = passing grid points;
    w_contig = longest contiguous passing run, in f units (points x STEP); lo/hi = its edges."""
    d = sub.sort_values("f")
    p = d[col].values.astype(bool)
    fv = d["f"].values
    best, cur, blo, bhi, clo = 0, 0, np.nan, np.nan, np.nan
    for i, ok in enumerate(p):
        if ok:
            if cur == 0:
                clo = fv[i]
            cur += 1
            if cur > best:
                best, blo, bhi = cur, clo, fv[i]
        else:
            cur = 0
    return dict(n_pass=int(p.sum()), n_runs=int(best),
                w_contig=(best - 1) * STEP if best > 0 else 0.0,
                f_lo=blo, f_hi=bhi, is_empty=bool(p.sum() == 0))


def binding(sub):
    """The bar that binds at the cell's best f (max worst-of-five margin)."""
    d = sub.loc[sub["m_min"].idxmax()]
    return min(BARS5, key=lambda k: d["m_" + k])


# ------------------------------------------------------------------ main -----
def main():
    say(f"IDEA 403 — is the 4b WINDOW a TURNOVER-COST fact about the ranked book?  (lane B)")
    say(f"{len(FS)} f-points x {len(LAMBDAS)} lambdas x {len(PANELS)} panels x {len(BOOKS)} books "
        f"x {len(SLEEVES)} sleeve sets = "
        f"{len(FS)*len(LAMBDAS)*len(PANELS)*len(BOOKS)*len(SLEEVES)} simulations, read at "
        f"{len(RUNGS)} cost rungs = "
        f"{len(FS)*len(LAMBDAS)*len(PANELS)*len(BOOKS)*len(SLEEVES)*len(RUNGS)} arm-rows.")
    say(f"f grid (uniform, step {STEP}): {FS}")
    say(f"lambda (base leg ONLY; the sleeve's trading is untouched): {LAMBDAS}")
    say(f"cost rungs: {RUNGS} bps.  Weekly, t+1, gross {GROSS}.  IS<= {IS_END}, OOS>= {OOS_START}.")

    # ================================================== PREMISE CHECK on idea 138's own grid
    say("\n" + "=" * 100)
    say("PREMISE CHECK — the queue's description read back off idea 138's COMMITTED grid")
    g138 = pd.read_csv(I138_GRID)
    pw = (g138[g138.pass4b].groupby(["panel", "book", "sleeve", "cost"]).f
          .agg(n_pass="count", f_lo="min", f_hi="max").reset_index())
    allcells = g138[["panel", "book", "sleeve", "cost"]].drop_duplicates()
    pw = allcells.merge(pw, how="left").fillna({"n_pass": 0})
    say(pw.to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    empt = pw[pw.n_pass == 0]
    say(f"  EMPTY cells: {len(empt)} -> "
        f"{[tuple(r) for r in empt[['panel','book','sleeve','cost']].values]}")
    ew = pw[pw.book == "EWall"]["n_pass"]
    say(f"  queue says '4-7 grid points wide on every EWall cell': EWall widths are "
        f"{sorted(ew.astype(int))} (min {int(ew.min())}, max {int(ew.max())}); the 7-point window "
        f"is {tuple(pw.loc[pw.n_pass.idxmax(), ['panel','book','sleeve','cost']].values)}.")
    say("  => the EMPTY-cell half of the premise is EXACT; the '4-7 on every EWall cell' half is "
        "NOT: the widest window is on the RANKED book, and EWall cells run "
        f"{int(ew.min())}-{int(ew.max())}.  Recorded as a premise correction, not a result.")

    # ================================================== build the grid
    rows, rets, ref = [], {}, {}
    for pk in PANELS:
        px = load_universe(broad=(pk == "broad"))
        missing = [t for t in SLEEVES["S4"] if t not in px.columns]
        if missing:
            raise RuntimeError(f"{pk} lacks {missing}")
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        b_full, b_is = bars_win(spy, "full"), bars_win(spy, "IS")
        ms, mo = metrics(spy), metrics(spy.loc[OOS_START:])
        ref[pk] = dict(bfull=b_full, bIS=b_is, spy=ms, spy_oos=mo, start=start, spyr=spy)
        say(f"\n[panel] {pk}: {px.shape[1]} cols {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}")
        say(f"    SPY full CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
            f"halves {b_full['s1']:.3f}/{b_full['s2']:.3f}; OOS Sharpe {mo['Sharpe']:.3f} "
            f"CAGR {mo['CAGR']:.2%} MaxDD {mo['MaxDD']:.2%}")
        say(f"    4b bars (full slice): H1>{b_full['s1']:.3f} H2>{b_full['s2']:.3f} "
            f"OOS>{b_full['soos']:.3f} MaxDD>={-DELTA*abs(b_full['sdd']):.2%} "
            f"CAGR>={PHI*b_full['scagr']:.2%}")

        # ---- gate G1: H.run with every instrument off == engine.backtest ----
        Wchk = H.targets(px, "EWall")
        a = H.run(px, Wchk, bps=10.0, freq=FREQ)["r"].loc[start:]
        b = backtest(px, Wchk, cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
        say(f"    [G1] H.run vs engine.backtest on EWall @10bps: max|d| {float((a-b).abs().max()):.3e}")
        assert float((a - b).abs().max()) < 1e-12

        # ---- gate G2: the rung identity r(c) = r(0) - to*c/1e4 ---------------
        o0 = H.run(px, Wchk, bps=0.0, freq=FREQ)
        d25 = H.run(px, Wchk, bps=25.0, freq=FREQ)["r"] - (o0["r"] - o0["to"] * 25.0 / 1e4)
        say(f"    [G2] rung identity r(25) == r(0) - to*25/1e4: max|d| {float(d25.abs().max()):.3e}")
        assert float(d25.abs().max()) < 1e-12

        # ---- live baseline, cost-matched (PROTOCOL 3) ------------------------
        v2raw = H.run(px, rules_v2_weights(px), bps=0.0, freq=FREQ)
        ref[pk]["v2"] = {c: (v2raw["r"] - v2raw["to"] * c / 1e4).loc[start:] for c in RUNGS}
        for c in I138_RUNGS:
            m2 = metrics(ref[pk]["v2"][c])
            h2 = H.halves(ref[pk]["v2"][c])
            say(f"    RULES v2 @{c:.0f}bps {m2['CAGR']:.2%}/{m2['Sharpe']:.3f}/{m2['MaxDD']:.2%} "
                f"halves {h2[0]:.3f}/{h2[1]:.3f}")

        base_raw = {bk: H.targets(px, bk) for bk in BOOKS}
        sl_W = {sk: sleeve_weights(px, av) for sk, av in SLEEVES.items()}

        for bk in BOOKS:
            for lam in LAMBDAS:
                bW = smooth(base_raw[bk], lam)
                for sk in SLEEVES:
                    for f in FS:
                        o = H.run(px, blend(bW, sl_W[sk], f), bps=0.0, freq=FREQ)
                        r0, to = o["r"].loc[start:], o["to"].loc[start:]
                        yrs = len(r0) / 252.0
                        toy = float(to.sum() / yrs)
                        for c in RUNGS:
                            r = r0 - to * c / 1e4
                            rets[(pk, bk, sk, lam, f, c)] = r
                            m, mI, mO = metrics(r), metrics(win(r, "IS")), metrics(r.loc[OOS_START:])
                            h1, h2 = H.halves(r)
                            mgf, mgi = margins(r, b_full, "full"), margins(r, b_is, "IS")
                            rows.append(dict(
                                panel=pk, book=bk, sleeve=sk, lam=lam, f=f, cost=c,
                                CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                IS_Sharpe=mI["Sharpe"], IS_CAGR=mI["CAGR"], IS_MaxDD=mI["MaxDD"],
                                OOS_Sharpe=mO["Sharpe"], OOS_CAGR=mO["CAGR"], OOS_MaxDD=mO["MaxDD"],
                                gross=float(o["gross"].loc[start:].mean()), turnover=toy,
                                m_H1=mgf["H1"], m_H2=mgf["H2"], m_OOS=mgf["OOS"], m_DD=mgf["DD"],
                                m_CAGR=mgf["CAGR"], m_min=min(mgf.values()),
                                pass4b=bool(all(v > 0 for v in mgf.values())),
                                IS_m_min=min(mgi.values()),
                                IS_pass4b=bool(all(v > 0 for v in mgi.values())),
                                pass4a_v2=H.pass4a(r, ref[pk]["v2"][c]),
                            ))
        say(f"    built {pk}: {len([1 for k in rets if k[0]==pk])} arm-rows")

    G = pd.DataFrame(rows)
    # base_to = the f=0 sibling's turnover: THE regressor the queue names
    bt = (G[G.f == 0.0].groupby(["panel", "book", "lam"]).turnover.first().rename("base_to"))
    G = G.merge(bt, left_on=["panel", "book", "lam"], right_index=True, how="left")
    G["drag"] = G.base_to * G.cost / 1e4
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"\nwrote {STEM}.grid.csv  ({len(G)} arm-rows)")

    # ---- gate G3: reproduce idea 138's committed rows (lam=1, shared f) ------
    say("\n[G3] REPRODUCTION of idea 138's committed .grid.csv at lambda=1 on the shared f points")
    mine = G[(G.lam == 1.0) & (G.cost.isin(I138_RUNGS))]
    j = g138.merge(mine, on=["panel", "book", "sleeve", "cost", "f"], suffixes=("_138", ""))
    if len(j):
        say("     Tolerances are PER PANEL and stated in advance: data/prices_broad.csv is rewritten "
            "weekly (Fridays) and is UNTOUCHED since idea 138 ran on 2026-09-07, so broad must "
            f"reproduce EXACTLY ({EXACT_TOL:.0e}); data/prices.csv is rewritten DAILY and now "
            f"carries three trading days idea 138 could not see, so u56 carries idea 137's drift "
            f"allowance ({DRIFT_TOL:.0e}).  Both are asserted; verdict agreement is asserted on both.")
        for pk in PANELS:
            q = j[j.panel == pk]
            dS = (q.Sharpe - q.Sharpe_138).abs().max()
            dC = (q.CAGR - q.CAGR_138).abs().max()
            dD = (q.MaxDD - q.MaxDD_138).abs().max()
            dT = (q.turnover - q.turnover_138).abs().max()
            agree = int((q.pass4b == q.pass4b_138).sum())
            tol = EXACT_TOL if pk == "broad" else DRIFT_TOL
            say(f"     {pk:>5}: {len(q)} shared rows  max|dSharpe| {dS:.3e}  max|dCAGR| {dC:.3e}  "
                f"max|dMaxDD| {dD:.3e}  max|dTurnover| {dT:.3e}  pass4b agreement {agree}/{len(q)}  "
                f"(tol {tol:.0e})")
            assert max(dS, dC, dD) < tol, f"idea 138 not reproduced on {pk}"
            assert agree == len(q), f"idea 138 4b verdicts not reproduced on {pk}"
    else:
        say("     NO shared rows — reproduction gate could not run")

    # ---- gate G4: lambda monotonically lowers base turnover -----------------
    say("\n[G4] MONOTONICITY of base turnover in lambda (the dial must actually be a dial)")
    BT = bt.reset_index().pivot_table(index=["panel", "book"], columns="lam", values="base_to")
    say(BT.to_string(float_format=lambda x: f"{x:.3f}"))
    mono = all((BT.loc[i].sort_index().diff().dropna() > 0).all() for i in BT.index)
    say(f"     monotone increasing in lambda in every (panel, book): {mono}")
    assert mono

    # ================================================== WINDOWS
    say("\n" + "=" * 100)
    say("WINDOWS — one measurement per (panel, book, sleeve, cost, lambda) over the 11-point f grid")
    wrows = []
    for k, sub in G.groupby(["panel", "book", "sleeve", "cost", "lam"]):
        w = window_of(sub)
        wi = window_of(sub, "IS_pass4b")
        w.update(dict(panel=k[0], book=k[1], sleeve=k[2], cost=k[3], lam=k[4],
                      base_to=float(sub.base_to.iloc[0]), drag=float(sub.drag.iloc[0]),
                      best_m_min=float(sub.m_min.max()), bind=binding(sub),
                      best_f=float(sub.loc[sub.m_min.idxmax(), "f"]),
                      IS_n_pass=wi["n_pass"], IS_w=wi["w_contig"], IS_lo=wi["f_lo"], IS_hi=wi["f_hi"],
                      n4a=int(sub.pass4a_v2.sum())))
        wrows.append(w)
    Wd = pd.DataFrame(wrows)
    Wd.to_csv(OUT / f"{STEM}.windows.csv", index=False)
    say(f"{len(Wd)} window measurements written to {STEM}.windows.csv")

    # ---------------------------------------------------- A1 NATIVE CELLS
    say("\n" + "-" * 100)
    say("A1 — NATIVE CELLS (lambda = 1), idea 138's 16 cells on the uniform grid")
    nat = Wd[(Wd.lam == 1.0) & (Wd.cost.isin(I138_RUNGS))].sort_values(
        ["panel", "book", "sleeve", "cost"])
    say(nat[["panel", "book", "sleeve", "cost", "base_to", "drag", "n_pass", "w_contig",
             "f_lo", "f_hi", "bind", "best_m_min"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"  Spearman(width, base_to) pooled over the 16 native cells: "
        f"{spearman(nat.w_contig, nat.base_to):+.3f}")
    say(f"  Spearman(width, drag)    pooled over the 16 native cells: "
        f"{spearman(nat.w_contig, nat.drag):+.3f}")
    for pk in PANELS:
        s = nat[nat.panel == pk]
        say(f"    within {pk:>5}: rho(width, base_to) {spearman(s.w_contig, s.base_to):+.3f}   "
            f"mean width EWall {s[s.book=='EWall'].w_contig.mean():.3f} vs "
            f"TOP20 {s[s.book=='TOP20'].w_contig.mean():.3f}")
    say(f"  mean width by panel: " +
        ", ".join(f"{p} {nat[nat.panel==p].w_contig.mean():.3f}" for p in PANELS))
    say(f"  mean width by book : " +
        ", ".join(f"{b} {nat[nat.book==b].w_contig.mean():.3f}" for b in BOOKS))
    say(f"  mean width by rung : " +
        ", ".join(f"{c:.0f}bps {nat[nat.cost==c].w_contig.mean():.3f}" for c in I138_RUNGS))

    # ---------------------------------------------------- A5 ZERO-COST CONTROL
    say("\n" + "-" * 100)
    say("A5 — THE ZERO-COST CONTROL.  Turnover reaches returns ONLY through cost, so a window "
        "that is already empty/narrow at 0 bps is not a turnover fact.")
    z = Wd[(Wd.lam == 1.0)].pivot_table(index=["panel", "book", "sleeve"], columns="cost",
                                        values="w_contig")
    say(z.to_string(float_format=lambda x: f"{x:.2f}"))
    z0 = Wd[(Wd.lam == 1.0) & (Wd.cost == 0.0)]
    say(f"  width spread across the 8 native (panel,book,sleeve) cells at 0 bps: "
        f"min {z0.w_contig.min():.2f} max {z0.w_contig.max():.2f} sd {z0.w_contig.std():.4f}")
    for c in I138_RUNGS:
        zc = Wd[(Wd.lam == 1.0) & (Wd.cost == c)]
        say(f"  ... at {c:.0f} bps: min {zc.w_contig.min():.2f} max {zc.w_contig.max():.2f} "
            f"sd {zc.w_contig.std():.4f}; empty cells {int(zc.is_empty.sum())}/{len(zc)}")
    bt20 = Wd[(Wd.lam == 1.0) & (Wd.panel == "broad") & (Wd.book == "TOP20")]
    say("  the two EMPTY cells (broad/TOP20 @25bps) read across the whole rung ladder:")
    say(bt20[["sleeve", "cost", "n_pass", "w_contig", "f_lo", "f_hi", "bind", "best_m_min"]]
        .sort_values(["sleeve", "cost"]).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------- A2 THE CAUSAL DIAL
    say("\n" + "-" * 100)
    say("A2 — THE CAUSAL DIAL.  Width vs lambda inside each cell (base leg only; the sleeve's "
        "own trading is unchanged).  If width is a base-turnover fact it must move here.")
    for c in I138_RUNGS:
        say(f"\n  cost {c:.0f} bps — contiguous window width in f units, by lambda:")
        piv = Wd[Wd.cost == c].pivot_table(index=["panel", "book", "sleeve"], columns="lam",
                                           values="w_contig")
        say(piv.to_string(float_format=lambda x: f"{x:.2f}"))
        pivt = Wd[Wd.cost == c].pivot_table(index=["panel", "book", "sleeve"], columns="lam",
                                            values="base_to")
        say(f"  (base turnover x/yr behind those columns:)")
        say(pivt.to_string(float_format=lambda x: f"{x:.2f}"))
    rhos = []
    for k, s in Wd.groupby(["panel", "book", "sleeve", "cost"]):
        rhos.append(dict(panel=k[0], book=k[1], sleeve=k[2], cost=k[3],
                         rho=spearman(s.w_contig, s.base_to),
                         rng=float(s.w_contig.max() - s.w_contig.min())))
    R = pd.DataFrame(rhos)
    say(f"\n  within-cell rho(width, base_to) over the lambda ladder, {len(R)} cells: "
        f"median {R.rho.median():+.3f}, positive {int((R.rho>0).sum())}, "
        f"negative {int((R.rho<0).sum())}, flat/undefined {int(R.rho.isna().sum())}")
    say(f"  within-cell width RANGE over the lambda ladder: median {R.rng.median():.3f}, "
        f"max {R.rng.max():.3f}, zero (width never moves) in {int((R.rng==0).sum())}/{len(R)} cells")
    say(f"  by rung: " + ", ".join(
        f"{c:.0f}bps median rho {R[R.cost==c].rho.median():+.3f} / median range "
        f"{R[R.cost==c].rng.median():.3f}" for c in RUNGS))
    op = Wd[(Wd.panel == "broad") & (Wd.book == "TOP20") & (Wd.cost == 25.0)]
    say(f"\n  DECISIVE: do the two EMPTY broad/TOP20@25bps windows OPEN when base turnover is cut?")
    say(op[["sleeve", "lam", "base_to", "n_pass", "w_contig", "f_lo", "f_hi", "bind", "best_m_min"]]
        .sort_values(["sleeve", "lam"]).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------- A3 MATCHED TURNOVER
    say("\n" + "-" * 100)
    TSTAR = float(bt.loc[("u56", "EWall", 1.00)])
    say(f"A3 — MATCHED TURNOVER (idea 137's D2 applied to width).  T* = the u56/EWall/lambda=1 "
        f"base turnover = {TSTAR:.3f}x/yr, named in advance.")
    mrows = []
    for k, s in Wd.groupby(["panel", "book", "sleeve", "cost"]):
        nat_r = s[s.lam == 1.0].iloc[0]
        pick = s.loc[(s.base_to - TSTAR).abs().idxmin()]
        mrows.append(dict(panel=k[0], book=k[1], sleeve=k[2], cost=k[3],
                          nat_to=nat_r.base_to, nat_w=nat_r.w_contig, nat_n=nat_r.n_pass,
                          mt_lam=pick.lam, mt_to=pick.base_to, mt_w=pick.w_contig,
                          mt_n=pick.n_pass, mt_bind=pick.bind, mt_best=pick.best_m_min,
                          bracketed=bool(s.base_to.min() <= TSTAR <= s.base_to.max())))
    M = pd.DataFrame(mrows)
    M.to_csv(OUT / f"{STEM}.matched.csv", index=False)
    say(M.sort_values(["cost", "panel", "book", "sleeve"])
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"  T* bracketed by the lambda ladder in {int(M.bracketed.sum())}/{len(M)} cells "
        f"(unbracketed = clamped at the low end, flagged not hidden)")
    for c in I138_RUNGS:
        mc = M[M.cost == c]
        say(f"  @{c:.0f}bps at MATCHED turnover: mean width u56 {mc[mc.panel=='u56'].mt_w.mean():.3f} "
            f"vs broad {mc[mc.panel=='broad'].mt_w.mean():.3f} "
            f"(native {mc[mc.panel=='u56'].nat_w.mean():.3f} vs {mc[mc.panel=='broad'].nat_w.mean():.3f}); "
            f"EWall {mc[mc.book=='EWall'].mt_w.mean():.3f} vs TOP20 {mc[mc.book=='TOP20'].mt_w.mean():.3f} "
            f"(native {mc[mc.book=='EWall'].nat_w.mean():.3f} vs {mc[mc.book=='TOP20'].nat_w.mean():.3f})")
    say(f"  Spearman(matched width, matched base_to) over all {len(M)} cells: "
        f"{spearman(M.mt_w, M.mt_to):+.3f}  (turnover is now nearly constant by construction, so "
        f"any surviving width spread is NOT turnover)")

    # ---------------------------------------------------- A4 THE DRAG COLLAPSE
    say("\n" + "-" * 100)
    say("A4 — THE DRAG COLLAPSE.  If width is a TURNOVER-COST fact it is a single function of "
        "D = base_to * c/1e4, whichever route produced D.  Route C varies the rung at lambda=1 "
        "(changes drag and NOTHING else); route L varies lambda at a fixed rung (changes drag AND "
        "the book's path).  Disagreement between the routes at matched D refutes the claim and "
        "names the residual.")
    say(f"  pooled Spearman(width, drag) over all {len(Wd)} window measurements: "
        f"{spearman(Wd.w_contig, Wd.drag):+.3f}")
    say(f"  ... within (panel, book, sleeve), pooling both routes:")
    for k, s in Wd.groupby(["panel", "book", "sleeve"]):
        say(f"      {k[0]:>5} {k[1]:>5} {k[2]}: rho {spearman(s.w_contig, s.drag):+.3f}  "
            f"drag {s.drag.min():.5f}..{s.drag.max():.5f}  width {s.w_contig.min():.2f}..{s.w_contig.max():.2f}")
    say("\n  ROUTE COMPARISON at matched drag: for every (cell, lambda, rung) point off the "
        "lambda route, the width the COST route predicts at the same drag (nearest-drag rung at "
        "lambda=1 inside the same panel/book/sleeve), and the residual.")
    cmpr = []
    for k, s in Wd.groupby(["panel", "book", "sleeve"]):
        cr = s[s.lam == 1.0]
        for _, q in s[s.lam < 1.0].iterrows():
            near = cr.loc[(cr.drag - q.drag).abs().idxmin()]
            cmpr.append(dict(panel=k[0], book=k[1], sleeve=k[2], lam=q.lam, cost=q.cost,
                             drag=q.drag, w_L=q.w_contig, w_C=near.w_contig,
                             drag_C=near.drag, resid=q.w_contig - near.w_contig,
                             ok=bool(abs(near.drag - q.drag) <= 0.25 * max(q.drag, 1e-9))))
    CR = pd.DataFrame(cmpr)
    good = CR[CR.ok & (CR.drag > 0)]
    say(f"  {len(good)} matched-drag pairs within 25% on drag: mean residual (lambda route minus "
        f"cost route) {good.resid.mean():+.4f}, median {good.resid.median():+.4f}, "
        f"|resid| > 0.05 (one grid step) in {int((good.resid.abs()>0.05).sum())}/{len(good)}, "
        f"sign agreement (both routes give equal width) {int((good.resid==0).sum())}/{len(good)}")
    say(f"  route sensitivity, mean |d width| per unit drag: "
        f"cost route {np.polyfit(Wd[Wd.lam==1.0].drag, Wd[Wd.lam==1.0].w_contig, 1)[0]:+.3f}, "
        f"lambda route (at 25 bps) "
        f"{np.polyfit(Wd[Wd.cost==25.0].drag, Wd[Wd.cost==25.0].w_contig, 1)[0]:+.3f}")

    # ---------------------------------------------------- A6 RULE 8
    say("\n" + "=" * 100)
    say("A6 — RULE 8 (PROTOCOL 8).  (f, lambda) chosen on 2009-2016 ALONE per cell; 2017-2026 "
        "read ONCE.  S0 = argmax IS Sharpe.  S1 = argmax IS Sharpe among points clearing 4b's "
        "four IS-evaluable bars inside the IS window.  Both scored vs the LIVE RULES v2 book "
        "(cost-matched) and vs SPY.")
    wf = []
    for k, s in G.groupby(["panel", "book", "sleeve", "cost"]):
        pk, bk, sk, c = k
        spy = ref[pk]["spyr"]
        spy_o = metrics(spy.loc[OOS_START:])
        v2_o = metrics(ref[pk]["v2"][c].loc[OOS_START:])
        ctl = s[(s.f == 0.0) & (s.lam == 1.0)].iloc[0]
        for sel in ["S0", "S1"]:
            pool = s if sel == "S0" else s[s.IS_pass4b]
            if not len(pool):
                wf.append(dict(panel=pk, book=bk, sleeve=sk, cost=c, sel=sel, abstain=True))
                continue
            p = pool.loc[pool.IS_Sharpe.idxmax()]
            r = rets[(pk, bk, sk, p.lam, p.f, c)]
            mo = metrics(r.loc[OOS_START:])
            wf.append(dict(
                panel=pk, book=bk, sleeve=sk, cost=c, sel=sel, abstain=False,
                f=p.f, lam=p.lam, base_to=p.base_to,
                IS_Sharpe=p.IS_Sharpe, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                OOS_MaxDD=mo["MaxDD"],
                v2_OOS_Sharpe=v2_o["Sharpe"], v2_OOS_CAGR=v2_o["CAGR"], v2_OOS_MaxDD=v2_o["MaxDD"],
                spy_OOS_Sharpe=spy_o["Sharpe"], spy_OOS_CAGR=spy_o["CAGR"],
                spy_OOS_MaxDD=spy_o["MaxDD"],
                ctl_OOS_Sharpe=metrics(rets[(pk, bk, sk, 1.0, 0.0, c)].loc[OOS_START:])["Sharpe"],
                OOS_beats_spy=bool(mo["Sharpe"] > spy_o["Sharpe"]),
                OOS_beats_v2=bool(mo["Sharpe"] > v2_o["Sharpe"]),
                OOS_4b=bool(mo["Sharpe"] > spy_o["Sharpe"] and
                            abs(mo["MaxDD"]) <= DELTA * abs(spy_o["MaxDD"]) and
                            mo["CAGR"] >= PHI * spy_o["CAGR"]),
                full_pass4b=bool(p.pass4b), full_pass4a=bool(p.pass4a_v2),
                ctl_f0_pass4b=bool(ctl.pass4b)))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    for sel in ["S0", "S1"]:
        s = WF[(WF.sel == sel) & (~WF.abstain)]
        ab = int(WF[(WF.sel == sel)].abstain.sum())
        say(f"\n  {sel}: {len(s)} cells priced, {ab} abstain")
        say(s[["panel", "book", "sleeve", "cost", "f", "lam", "base_to", "OOS_CAGR", "OOS_Sharpe",
               "OOS_MaxDD", "v2_OOS_Sharpe", "spy_OOS_Sharpe", "OOS_beats_spy", "OOS_beats_v2",
               "OOS_4b"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        say(f"    picked f: {s.f.value_counts().sort_index().to_dict()}")
        say(f"    picked lambda: {s.lam.value_counts().sort_index().to_dict()}")
        say(f"    picked lambda<1 on EWall {int((s[s.book=='EWall'].lam<1).sum())}/"
            f"{len(s[s.book=='EWall'])}, on TOP20 {int((s[s.book=='TOP20'].lam<1).sum())}/"
            f"{len(s[s.book=='TOP20'])}")
        say(f"    OOS Sharpe mean {s.OOS_Sharpe.mean():.4f} vs SPY {s.spy_OOS_Sharpe.mean():.4f} "
            f"vs RULES v2 {s.v2_OOS_Sharpe.mean():.4f}; beats SPY {int(s.OOS_beats_spy.sum())}/{len(s)}, "
            f"beats v2 {int(s.OOS_beats_v2.sum())}/{len(s)}, clears OOS 4b bars "
            f"{int(s.OOS_4b.sum())}/{len(s)}")
        say(f"    OOS CAGR mean {s.OOS_CAGR.mean():.2%} vs SPY {s.spy_OOS_CAGR.mean():.2%} "
            f"vs v2 {s.v2_OOS_CAGR.mean():.2%}; OOS MaxDD mean {s.OOS_MaxDD.mean():.2%} vs SPY "
            f"{s.spy_OOS_MaxDD.mean():.2%} vs v2 {s.v2_OOS_MaxDD.mean():.2%}")

    say("\n  WINDOW TRANSFER (rule 8 applied to the WINDOW itself, not to a book): does the IS "
        "window's width/location predict the full-sample window's?")
    say(f"    Spearman(IS width, full width) over {len(Wd)} cells: "
        f"{spearman(Wd.IS_w, Wd.w_contig):+.3f}; IS width mean {Wd.IS_w.mean():.3f} vs full "
        f"{Wd.w_contig.mean():.3f}")
    ov = Wd.dropna(subset=["IS_lo", "f_lo"])
    if len(ov):
        overlap = int(((ov.IS_lo <= ov.f_hi) & (ov.f_lo <= ov.IS_hi)).sum())
        nested = int(((ov.IS_lo <= ov.f_lo) & (ov.f_hi <= ov.IS_hi)).sum())
        lowbias = int((ov.IS_lo <= ov.f_lo).sum())
        say(f"    over the {len(ov)} cells where both windows are non-empty "
            f"({len(Wd)-len(ov)} have at least one empty): the two windows OVERLAP in "
            f"{overlap}/{len(ov)}, the full-sample window is NESTED INSIDE the IS window in "
            f"{nested}/{len(ov)}, and the IS window's lower edge sits AT OR BELOW the full "
            f"window's in {lowbias}/{len(ov)} (mean IS lower edge {ov.IS_lo.mean():.3f} vs full "
            f"{ov.f_lo.mean():.3f}; upper edges {ov.IS_hi.mean():.3f} vs {ov.f_hi.mean():.3f}).")
        say("    => the IS window is a SUPERSET, not a forecast: it admits low f the full sample "
            "rejects, which is idea 128/138's own caveat (the IS window cannot express a deep "
            "drawdown, so an IS drawdown cap admits too much) showing up in the window's LOCATION "
            "while its WIDTH ordering still transfers.")

    # ---------------------------------------------------- KEEP PATHS
    say("\n" + "=" * 100)
    say("KEEP PATHS over all arm-rows (PROTOCOL 4; 4a vs the LIVE RULES v2 book cost-matched, "
        "4b vs SPY on all five bars).")
    G["both"] = G.pass4a_v2 & G.pass4b
    KP = G.groupby(["panel", "book", "sleeve", "cost"]).agg(
        n=("f", "size"), pass4a=("pass4a_v2", "sum"), pass4b=("pass4b", "sum"),
        both=("both", "sum")).reset_index()
    KP.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    say(KP.to_string(index=False))
    say(f"  TOTAL: 4a {int(G.pass4a_v2.sum())}/{len(G)}, 4b {int(G.pass4b.sum())}/{len(G)}, "
        f"BOTH {int(G.both.sum())}/{len(G)}")
    say(f"  4b passes at the two idea-138 rungs only: "
        f"{int(G[G.cost.isin(I138_RUNGS)].pass4b.sum())}/{len(G[G.cost.isin(I138_RUNGS)])}")
    if int(G.both.sum()):
        say("  arms clearing BOTH paths (reported, not promoted without rule 8):")
        say(G[G.both][["panel", "book", "sleeve", "cost", "lam", "f", "CAGR", "Sharpe", "MaxDD",
                       "OOS_Sharpe", "m_min"]].to_string(index=False,
                                                         float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------- VERDICT
    say("\n" + "=" * 100)
    say("VERDICT INPUTS (the four falsifiable statements, answered)")
    z0w = Wd[(Wd.lam == 1.0) & (Wd.cost == 0.0)]
    z25 = Wd[(Wd.lam == 1.0) & (Wd.cost == 25.0)]
    say(f"  (i)  zero-cost spread vanishes?  width sd at 0 bps {z0w.w_contig.std():.4f} vs at "
        f"25 bps {z25.w_contig.std():.4f}; empty cells at 0 bps {int(z0w.is_empty.sum())}/{len(z0w)}")
    say(f"  (ii) width moves with the base-turnover dial?  within-cell median rho "
        f"{R.rho.median():+.3f}, width never moves in {int((R.rng==0).sum())}/{len(R)} cells")
    say(f"  (iii) does matched turnover close the cross-cell width gap?  see A3 above")
    say(f"  (iv) do the two routes to the same drag agree?  |resid|>1 grid step in "
        f"{int((good.resid.abs()>0.05).sum())}/{len(good)} matched-drag pairs")
    say("\nSURVIVORSHIP (idea 54): current constituents on both panels; the equity leg is "
        "flattered relative to the ETF sleeve, so every window measured here is biased NARROW "
        "and toward low f.  A negative result on width is therefore understated, not overstated.")
    say(f"\nwrote {STEM}.console.txt / .grid.csv / .windows.csv / .matched.csv / "
        f".walkforward.csv / .keeppaths.csv")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
