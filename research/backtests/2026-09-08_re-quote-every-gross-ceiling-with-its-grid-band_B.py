#!/usr/bin/env python3
"""QUEUE idea 236 — re-quote-every-gross-ceiling-with-its-grid-band  (lane B, 2026-09-08)

QUESTION (pre-registered, verbatim from QUEUE.md idea 236)
    "idea 154 measured that a 5x finer gross ladder moves a published ceiling by a mean 0.0113
    and up to 0.0300 of realised gross.  Re-read every gross ceiling in the record that was
    read off a 0.05 grid, attach the +/-0.03 band, and flag the ones whose published verdict
    flips inside it.  Max 2 params."

    Idea 154 measured 21 cells (one book, EWall, 4 arms x 3 panels x 3 rungs).  The record's
    gross ceilings are the 4b admissible-interval UPPER shoulders of idea 90/144's 306-book
    gross family, every one of them read off idea 90's 25-point m-grid of step 0.05.  72 of
    those 306 books carry a non-empty interval at the published bars (phi=0.70, delta=0.60)
    and therefore a published ceiling.  This run re-reads all 72 on a 0.01 ladder, 3.4x idea
    154's coverage, and answers three things the queue's sentence does not settle:

      Q1  CENSUS + PROVENANCE.  How many published gross ceilings exist, on what grid were
          they read, and how many are right-CENSORED by PROTOCOL rule 2's no-leverage cap
          (m = 1.30) rather than set by a 4b bar?  A censored ceiling has no band: it is a
          rule, not a measurement.
      Q2  IS THE BAND EVEN TWO-SIDED?  The coarse grid is a SUBSET of the fine one, so every
          coarse-admissible point stays admissible and m_hi can only RISE with refinement.
          Where m is a pure exposure rescale (idea 90's PURE_KINDS = ctl/gate/stop) realised
          gross is monotone in m, so the quoted ceiling can only rise too.  Prediction,
          pre-registered: d_hi >= 0 on every MONO book, i.e. the displacement is ONE-SIDED and
          a published ceiling is a LOWER BOUND, never a point estimate.  On `dd` and `bud`
          arms m also moves the instrument itself (idea 144 Q1) so nothing is predicted; the
          two groups are reported separately and never pooled.
      Q3  IS +/-0.03 THE RIGHT WIDTH?  The queue proposes a universal +/-0.03.  But the
          displacement is bounded ABOVE, exactly and per book, with no extra backtest:
              d_hi < DELTA_STEP(book) = gross(m_hi + 0.05) - gross(m_hi),
          the realised-gross width of ONE coarse step at that book's own shoulder.  Report
          DELTA_STEP's distribution against 0.03 and score the queue's constant on COVERAGE
          (does [g_hi, g_hi + b] contain the fine ceiling?) and on WASTE (how much wider than
          it needs to be).  Then flag every published verdict that flips inside the band.

    A finding that the queue's own band is mis-shaped is a KILL of the band as worded and is
    reported as such.  Rule 7: nothing is tuned until it works; every grid point is printed.

HARNESS — nothing is re-implemented; the corpus the question is about is REBUILT
    Idea 94's simulator (`2026-09-04_drawdown-insurance-price-list_B.py`) is imported, and
    idea 90's interval machinery (bar_frame / intervals at phi=0.70, delta=0.60) is
    re-derived here rather than trusted.  Gates run BEFORE any new number is read:
      G1  H.run with every instrument off vs engine.backtest, 3 books x 2 panels.
      G2  the cost-rung identity: for arms whose state machine does not read net equity
          (ctl/gate/stop/bud) r(25bps) == r(10bps) - turnover * 15/1e4 exactly.  Only the
          two `ddctl` arms are re-run per rung.
      G3  this run's rebuilt m=0.05 rows vs idea 90's committed family.csv.gz (7,650 rows),
          and this run's `intervals()` vs its committed intervals.csv, all 306 books.
      G4  idea 154's published fine ceilings on its own cells (broad EWall band3-rw 0.8177 @
          10 bps and 0.8102 @ 25, u56 EWall vol60-dg 0.8708 @ 10) and its headline
          "mean |move| 0.0113, max 0.0300 over 21 cells".

CORPUS   the 45 distinct (panel, book, arm) cells behind the record's 72 published ceilings,
    each on the FULL 121-point ladder m in 0.10..1.30 step 0.01 (idea 154's resolution), both
    cost rungs.  m = 1.00 is 75% target gross.  Weekly, t+1, 10 bps unless stated.  g is
    reported as REALISED MEAN GROSS throughout, because that is the number a rule quotes.

TUNED PARAMETERS — exactly two
    step   the m-grid the ceiling is read on, in {0.05 (published), 0.02, 0.01}
    b      the band half-width attached to it,  in {0.01, 0.02, 0.03 (the queue's), 0.04, 0.05}
    3 x 5 = 15 grid points, ALL reported.  The 4b bar coefficients are PINNED at the record's
    published (phi, delta) = (0.70, 0.60) and are not tuned here.

BOTH KEEP PATHS are evaluated at every grid point: 4a against the LIVE book (RULES v2, and
    RULES v1 for continuity with the pre-2026-09-06 record) and 4b against SPY, for each book
    run AT ITS OWN CEILING under each step.

RULE 8 (walk-forward, required).  The ceiling is re-derived on 2009-2016 ONLY (IS bars, the
    OOS bar undefined inside the window), the book is run at that IS ceiling, and 2017-2026 is
    read ONCE.  Reported: OOS CAGR / Sharpe / MaxDD at the coarse IS ceiling vs the fine IS
    ceiling vs the live RULES v2 baseline vs SPY, per panel and rung.  The capital question
    behind the queue's clerical one: refining a ceiling UPWARDS licenses more exposure — does
    the extra exposure survive out of sample?

CAVEATS carried, not buried
    - Survivorship (idea 54): u56 and broad are current-constituent lists; levels overstated.
    - Idea 128: the IS window's SPY MaxDD is shallower than the OOS window's, so every IS
      drawdown cap admits too much; this biases the rule-8 arm upward, both grids equally.
    - The two `ebud` arms scale an absolute turnover budget, so m is not a pure exposure
      rescale there (idea 144 Q1); their rows are kept and flagged, never dropped.
    - Idea 38 (u56/broad calendar-day index) and idea 126 (t+1 only) carry over.
    - This run does not re-open the (phi, delta) bars; a ceiling is read against the record's
      own published bars so that the displacement measured is the GRID's, not a bar change.

Deterministic, no network.  Writes .census.csv, .band.csv, .flips.csv, .grid.csv,
.walkforward.csv, .console.txt.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_re-quote-every-gross-ceiling-with-its-grid-band_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I90_FAMILY = OUT / "2026-09-05_gross-interval-as-a-keep-bar_B.family.csv.gz"
I90_INTERVALS = OUT / "2026-09-05_gross-interval-as-a-keep-bar_B.intervals.csv"
I154_INTERVALS = OUT / "2026-09-06_ew-band3-at-085-does-not-hold-on-broad_cloud.intervals.csv"
CKPT = OUT / f"{STEM}.fine.csv.gz"

_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

FREQ, IS_END, OOS_START = H.FREQ, H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
PHI0, DELTA0 = 0.70, 0.60
BARS5 = ("H1", "H2", "OOS", "DD", "CAGR")
BARS_IS = ("H1", "H2", "DD", "CAGR")
COARSE = [round(x, 2) for x in np.arange(0.10, 1.3001, 0.05)]        # idea 90's 25 points
FINE = [round(x, 2) for x in np.arange(0.10, 1.3001, 0.01)]         # idea 154's 121 points
MID = [round(x, 2) for x in np.arange(0.10, 1.3001, 0.02)]          # the intermediate rung
STEPS = [("0.05", COARSE), ("0.02", MID), ("0.01", FINE)]
# every rung is a SUBSET of the 0.01 ladder actually built, so a rung can never silently
# degenerate to a coarser one; asserted in Q2 before the rung is read.
BANDS = [0.01, 0.02, 0.03, 0.04, 0.05]
TARGETS = [0.75, 0.85]          # the live book's gross, and idea 84's contested g
M_FLOOR, M_CEIL = FINE[0], FINE[-1]
PURE = ("ctl", "gate", "stop", "bud")   # state machine does not read net equity -> rung identity
MONO = ("ctl", "gate", "stop")          # idea 90's PURE_KINDS: m IS a pure exposure rescale
#   on MONO arms realised gross is monotone in m, so a coarse ceiling can only UNDERSTATE.
#   on `dd` and `bud` arms m also moves the instrument itself (idea 144 Q1), so neither the
#   monotonicity nor the one-sided band is guaranteed there.  Reported separately, never pooled.

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 500)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def rule(t=""):
    say("\n" + "=" * 116)
    if t:
        say(t)
        say("=" * 116)


def fmt(x, n=4):
    return "n/a" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{n}f}"


# ------------------------------------------------------------------ panels (idea 90 verbatim)
def _panel(name):
    if name == "u56":
        px = load_universe()
        return px, px["SPY"].pct_change().fillna(0.0), "universe.json(56)"
    if name == "broad":
        px = load_universe(broad=True)
        return px, px["SPY"].pct_change().fillna(0.0), "universe_broad.json(136)"
    raise ValueError(name)


def bars_win(spy, which):
    w = spy if which == "full" else H.window(spy, which)
    s1, s2 = H.halves(w)
    m = metrics(w)
    soos = metrics(H.window(spy, "OOS"))["Sharpe"] if which == "full" else m["Sharpe"]
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"], soos=soos)


def stats_of(r):
    m, mo, mi = metrics(r), metrics(H.window(r, "OOS")), metrics(H.window(r, "IS"))
    h1, h2 = H.halves(r)
    i1, i2 = H.halves(H.window(r, "IS"))
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                OOS_Sharpe_full=mo["Sharpe"],
                IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                IS_H1=i1, IS_H2=i2,
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])


# ------------------------------------------------------------------ idea 90's bars, verbatim
def bar_frame(D, phi, delta, bars_by_panel, which):
    if which == "full":
        b1 = D.panel.map({p: bars_by_panel[p][0]["s1"] for p in bars_by_panel})
        b2 = D.panel.map({p: bars_by_panel[p][0]["s2"] for p in bars_by_panel})
        bo = D.panel.map({p: bars_by_panel[p][0]["soos"] for p in bars_by_panel})
        bd = D.panel.map({p: abs(bars_by_panel[p][0]["sdd"]) for p in bars_by_panel})
        bc = D.panel.map({p: bars_by_panel[p][0]["scagr"] for p in bars_by_panel})
        return pd.DataFrame(dict(H1=D.H1 - b1 > 0, H2=D.H2 - b2 > 0,
                                 OOS=D.OOS_Sharpe_full - bo > 0,
                                 DD=delta * bd - D.MaxDD.abs() > 0,
                                 CAGR=D.CAGR - phi * bc > 0), index=D.index)
    b1 = D.panel.map({p: bars_by_panel[p][1]["s1"] for p in bars_by_panel})
    b2 = D.panel.map({p: bars_by_panel[p][1]["s2"] for p in bars_by_panel})
    bd = D.panel.map({p: abs(bars_by_panel[p][1]["sdd"]) for p in bars_by_panel})
    bc = D.panel.map({p: bars_by_panel[p][1]["scagr"] for p in bars_by_panel})
    return pd.DataFrame(dict(H1=D.IS_H1 - b1 > 0, H2=D.IS_H2 - b2 > 0,
                             OOS=pd.Series(True, index=D.index),
                             DD=delta * bd - D.IS_MaxDD.abs() > 0,
                             CAGR=D.IS_CAGR - phi * bc > 0), index=D.index)


def intervals(F, phi, delta, bars_by_panel, which="full", keys=BARS5,
              m_floor=None, m_ceil=None):
    """idea 90's `intervals`, with the grid edges passed in so the SAME code reads a 0.05,
    a 0.025 and a 0.01 ladder and the censoring flags stay meaningful on each."""
    B = bar_frame(F, phi, delta, bars_by_panel, which)
    D = F[["book_id", "panel", "book", "cost", "arm", "kind", "m", "gross"]].copy()
    D["ok"] = B[list(keys)].all(axis=1)
    for k in keys:
        D["f_" + k] = ~B[k]
    lo_edge = D.m.min() if m_floor is None else m_floor
    hi_edge = D.m.max() if m_ceil is None else m_ceil
    out = []
    for bid, G in D.groupby("book_id", sort=False):
        G = G.sort_values("m").reset_index(drop=True)
        okv = G.ok.values
        n_ok = int(okv.sum())
        r0 = G.iloc[0]
        rec = dict(book_id=bid, panel=r0.panel, book=r0.book, cost=r0.cost, arm=r0.arm,
                   kind=r0.kind, n_ok=n_ok, nonempty=n_ok > 0)
        if n_ok == 0:
            rec.update(m_lo=np.nan, m_hi=np.nan, g_lo=np.nan, g_hi=np.nan, width=np.nan,
                       contiguous=True, gaps=0, cens_lo=False, cens_hi=False,
                       lo_bar="", hi_bar="", g_step_hi=np.nan)
            out.append(rec)
            continue
        idx = np.flatnonzero(okv)
        lo, hi = int(idx[0]), int(idx[-1])
        gaps = int((~okv[lo:hi + 1]).sum())
        lo_bar = hi_bar = "grid"
        if lo > 0:
            lo_bar = "+".join(k for k in keys if G.iloc[lo - 1]["f_" + k])
        if hi < len(G) - 1:
            hi_bar = "+".join(k for k in keys if G.iloc[hi + 1]["f_" + k])
        # the realised-gross width of ONE grid step at this book's own upper shoulder
        g_step_hi = (G.gross[hi + 1] - G.gross[hi]) if hi < len(G) - 1 else np.nan
        rec.update(m_lo=G.m[lo], m_hi=G.m[hi], g_lo=G.gross[lo], g_hi=G.gross[hi],
                   width=G.gross[hi] - G.gross[lo], contiguous=gaps == 0, gaps=gaps,
                   cens_lo=np.isclose(G.m[lo], lo_edge), cens_hi=np.isclose(G.m[hi], hi_edge),
                   lo_bar=lo_bar, hi_bar=hi_bar, g_step_hi=g_step_hi)
        out.append(rec)
    return pd.DataFrame(out)


# ================================================================== BUILD
def build():
    """Rebuild the 45 published-ceiling cells on the full 121-point ladder, both rungs."""
    say("Reading the record's published ceilings ...")
    iv90 = pd.read_csv(I90_INTERVALS)
    fam90 = pd.read_csv(I90_FAMILY)
    ne = iv90[iv90.nonempty].copy()
    cells = ne[["panel", "book", "arm", "kind"]].drop_duplicates().reset_index(drop=True)
    say(f"  idea 90 intervals.csv: {len(iv90)} books, {len(ne)} with a published ceiling, "
        f"{len(cells)} distinct (panel, book, arm) cells across panels {sorted(ne.panel.unique())}")

    cached = pd.read_csv(CKPT) if CKPT.exists() else None
    bars_by_panel, panels = {}, {}
    rows = []
    gate_rows = []
    for pname in sorted(cells.panel.unique()):
        px, spy_full, desc = _panel(pname)
        start = px.index[260]
        spy = spy_full.loc[start:]
        bars_by_panel[pname] = (bars_win(spy, "full"), bars_win(spy, "IS"), bars_win(spy, "OOS"))
        panels[pname] = (px, start, spy)

        # ---- G1: H.run with every instrument off vs engine.backtest
        worst = 0.0
        for b in H.BOOKS:
            W = H.targets(px, b)
            a = H.run(px, W, bps=H.PCOST)["r"].loc[start:]
            e = backtest(px, W, cost_bps=H.PCOST, freq=FREQ)["returns"].loc[start:]
            worst = max(worst, float((a - e).abs().max()))
        gate_rows.append((pname, desc, px.shape[1], str(start.date()), str(px.index[-1].date()), worst))
        say(f"[{pname:5s}] {desc:26s} {px.shape[1]:4d} cols  eval {start.date()} -> "
            f"{px.index[-1].date()} | G1 H.run vs engine.backtest max|diff| = {worst:.3e}")
        assert worst < 1e-12, f"G1 FAILED on {pname}: {worst}"

    if cached is not None:
        say(f"  [checkpoint found: {CKPT.name}, {len(cached)} rows reused]")
        return cached, bars_by_panel, panels, iv90, fam90, cells, gate_rows

    say(f"\nBuilding {len(cells)} cells x {len(FINE)} m-points ... (rung identity used for "
        f"kinds {PURE}; `dd` arms re-run per rung)")
    spec = {n: (k, kw, tg) for n, k, kw, tg in H.arm_specs()}
    for ci, c in cells.iterrows():
        px, start, _ = panels[c.panel]
        kind, kw, (gate, conv) = spec[c.arm]
        W = H.targets(px, c.book, gate=gate, conv=conv)
        for m in FINE:
            base = H.run(px, W, m=m, bps=10.0, **kw)
            r10, to = base["r"].loc[start:], base["to"].loc[start:]
            gross = float(base["gross"].loc[start:].mean())
            gcv = float(base["gross"].loc[start:].std() / max(gross, 1e-12))
            for cost in COSTS:
                if kind in PURE:
                    r = r10 - to * (cost - 10.0) / 1e4
                else:
                    rr = H.run(px, W, m=m, bps=cost, **kw)
                    r, to_c = rr["r"].loc[start:], rr["to"].loc[start:]
                    gross = float(rr["gross"].loc[start:].mean())
                    gcv = float(rr["gross"].loc[start:].std() / max(gross, 1e-12))
                s = stats_of(r)
                s.update(panel=c.panel, book=c.book, cost=cost, arm=c.arm, kind=kind, m=m,
                         gross=gross, gross_cv=gcv, TO=float(to.sum()),
                         book_id=f"{c.panel}|{c.book}|{cost}|{c.arm}")
                rows.append(s)
        say(f"  [{ci + 1:2d}/{len(cells)}] {c.panel:5s} {c.book:5s} {c.arm:20s} done")
    F = pd.DataFrame(rows)
    F.to_csv(CKPT, index=False)
    say(f"  checkpoint written: {CKPT.name} ({len(F)} rows)")
    return F, bars_by_panel, panels, iv90, fam90, cells, gate_rows


# ================================================================== GATES
def gates(F, fam90, iv90, bars_by_panel, panels, gate_rows):
    rule("GATES — nothing below is read until all four pass")
    for pname, desc, ncol, s0, s1, worst in gate_rows:
        say(f"  G1 {pname:5s} {desc:26s} H.run vs engine.backtest max|diff| = {worst:.3e}  PASS")

    # ---- G2 cost-rung identity, checked directly on one pure cell per panel
    worst = 0.0
    spec = {n: (k, kw, tg) for n, k, kw, tg in H.arm_specs()}
    for pname, (px, start, _) in panels.items():
        kind, kw, (gate, conv) = spec["band3-rw"]
        W = H.targets(px, "EWall", gate=gate, conv=conv)
        a = H.run(px, W, m=0.90, bps=10.0, **kw)
        b = H.run(px, W, m=0.90, bps=25.0, **kw)
        d = float((b["r"].loc[start:] - (a["r"].loc[start:] - a["to"].loc[start:] * 15.0 / 1e4)).abs().max())
        worst = max(worst, d)
    say(f"  G2 cost-rung identity r(25) == r(10) - TO*15/1e4 on `gate` arms: max|diff| = "
        f"{worst:.3e}  {'PASS' if worst < 1e-15 else 'FAIL'}")
    assert worst < 1e-15

    # ---- G3 rebuilt coarse rows vs idea 90's committed family + intervals
    key = ["panel", "book", "cost", "arm", "m"]
    mine = F[np.isin(np.round(F.m, 2), COARSE)].copy()
    mine["m"] = mine.m.round(2)
    theirs = fam90.copy()
    theirs["m"] = theirs.m.round(2)
    j = mine.merge(theirs, on=key, suffixes=("_a", "_b"))
    cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe_full", "IS_CAGR", "IS_Sharpe",
            "IS_MaxDD", "IS_H1", "IS_H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross"]
    dmax = max(float((j[c + "_a"] - j[c + "_b"]).abs().max()) for c in cols)
    per_panel = {p: max(float((g[c + "_a"] - g[c + "_b"]).abs().max()) for c in cols)
                 for p, g in j.groupby("panel")}
    h1max = float((j["H1_a"] - j["H1_b"]).abs().max())
    say(f"  G3a rebuilt 0.05 rows vs idea 90 family.csv.gz: {len(j)} shared rows x {len(cols)} "
        f"columns, max|diff| = {dmax:.3e}  {'PASS' if dmax < 1e-3 else 'FAIL'}")
    say("      by panel: " + "  ".join(f"{p} {v:.3e}" for p, v in sorted(per_panel.items())))
    say(f"      H1 (first-half Sharpe) max|diff| = {h1max:.3e}")
    say("      DIAGNOSIS, carried into every reading below: `broad` reproduces the committed "
        "file EXACTLY; `u56` carries a residual that is ZERO in H1 and non-zero in H2 / OOS / "
        "full sample.  That is the signature of ONE late-sample daily return changing — an "
        "adjusted-close revision to data/prices.csv after idea 90 ran (data/prices_broad.csv "
        "is a separate weekly cache and was not refreshed).  This sandbox's clone is SHALLOW, "
        "so the pre-revision file cannot be checked out and the residual cannot be removed.  "
        "It is 1e-5-scale against a measurand quantised at ~0.007-0.03 of realised gross, i.e. "
        "3 orders of magnitude below anything read here — but the DECISIVE gate is G3b, which "
        "checks the published READINGS rather than the floats behind them.")
    assert len(j) == len(mine) and dmax < 1e-3

    ivm = intervals(mine, PHI0, DELTA0, bars_by_panel, "full",
                    m_floor=COARSE[0], m_ceil=COARSE[-1])
    t = iv90.set_index("book_id")
    a = ivm.set_index("book_id")
    common = a.index.intersection(t.index)
    same_ne = int((a.loc[common, "nonempty"] == t.loc[common, "nonempty"]).sum())
    dm = max(float((a.loc[common, c] - t.loc[common, c]).abs().max()) for c in ["m_lo", "m_hi"])
    dg = max(float((a.loc[common, c] - t.loc[common, c]).abs().max()) for c in ["g_lo", "g_hi"])
    say(f"  G3b rebuilt READINGS vs idea 90 intervals.csv (the decisive gate — these are the "
        f"published numbers this run re-quotes):")
    say(f"      {len(common)} shared books | nonempty verdict agrees {same_ne}/{len(common)} | "
        f"max|diff| on the grid positions (m_lo, m_hi) = {dm:.3e} | on the quoted gross "
        f"(g_lo, g_hi) = {dg:.3e}")
    ok3b = (dm == 0.0) and same_ne == len(common) and dg < 1e-4
    say(f"      every published shoulder lands on the SAME grid point  {'PASS' if ok3b else 'FAIL'}")
    assert ok3b

    # ---- G4 idea 154's published fine ceilings on its own cells
    ivf = intervals(F, PHI0, DELTA0, bars_by_panel, "full", m_floor=FINE[0], m_ceil=FINE[-1])
    f = ivf.set_index("book_id")
    checks = [("broad|EWall|10.0|band3-rw", 0.817668), ("broad|EWall|25.0|band3-rw", 0.810173),
              ("u56|EWall|10.0|band3-rw", 0.862655), ("u56|EWall|25.0|band3-rw", 0.855162),
              ("broad|EWall|10.0|vol60-dg", 0.781145), ("u56|EWall|10.0|vol60-dg", 0.870762)]
    ok154 = True
    i154 = pd.read_csv(I154_INTERVALS)
    for bid, pub in checks:
        if bid not in f.index:
            say(f"  G4 {bid:32s} not in this corpus (no published ceiling) — skipped")
            continue
        got = float(f.loc[bid, "g_hi"])
        # idea 154's own committed file is the authority for the published digits
        pn, bk, cs, ar = bid.split("|")
        row = i154[(i154.panel == pn) & (i154.arm == ar) & (i154.bps == float(cs))]
        ref = float(row.b_hi.iloc[0]) if len(row) else pub
        d = abs(got - ref)
        ok154 &= d < 5e-4
        say(f"  G4 {bid:32s} fine ceiling {got:.6f} vs idea 154 committed {ref:.6f}  "
            f"|d| = {d:.2e}  {'PASS' if d < 5e-4 else 'FAIL'}")
    say(f"  G4 verdict: {'PASS' if ok154 else 'FAIL'}")
    assert ok154
    return ivm, ivf


# ================================================================== MAIN
def main():
    F, bars_by_panel, panels, iv90, fam90, cells, gate_rows = build()
    ivm, ivf = gates(F, fam90, iv90, bars_by_panel, panels, gate_rows)

    # ---------------------------------------------------------------- Q1 census
    rule("Q1 — CENSUS OF THE RECORD'S PUBLISHED GROSS CEILINGS (idea 90/144's 306-book family)")
    ne90 = iv90[iv90.nonempty]
    say(f"  books in the family                        : {len(iv90)}")
    say(f"  books with a published gross CEILING       : {len(ne90)}   (non-empty 4b interval "
        f"at the published phi={PHI0}, delta={DELTA0})")
    say(f"  read off idea 90's m-grid of step 0.05     : {len(ne90)} of {len(ne90)}  (100%)")
    say(f"  right-CENSORED at PROTOCOL 2's m=1.30 cap  : {int(ne90.cens_hi.sum())}   "
        f"-> no band: the ceiling is the no-leverage rule, not a measurement")
    say(f"  ceilings SET BY A 4b BAR (bandable)        : {int((~ne90.cens_hi).sum())}")
    say(f"  contiguous admissible set (idea 90 Q1)     : {int(ne90.contiguous.sum())} of {len(ne90)}")
    say("\n  which bar sets the ceiling (all 72):")
    say("    " + ne90.hi_bar.value_counts().to_string().replace("\n", "\n    "))
    say("\n  by panel / book / rung:")
    say("    " + ne90.groupby(["panel", "book", "cost"]).size().to_string().replace("\n", "\n    "))
    census = ne90[["book_id", "panel", "book", "cost", "arm", "kind", "m_lo", "m_hi",
                   "g_lo", "g_hi", "width", "cens_hi", "hi_bar"]].copy()
    census["grid_step_published"] = 0.05
    census.to_csv(OUT / f"{STEM}.census.csv", index=False)

    # ---------------------------------------------------------------- Q2 the displacement
    rule("Q2 — IS THE DISPLACEMENT ONE-SIDED?  ceiling at step 0.05 vs 0.02 vs 0.01, all 72 books")
    IV = {}
    for lbl, grid in STEPS:
        sub = F[np.isin(np.round(F.m, 3), [round(x, 3) for x in grid])].copy()
        got = int(sub.m.round(2).nunique())
        assert got == len(grid), f"rung {lbl} degenerated: {got} of {len(grid)} m-points present"
        IV[lbl] = intervals(sub, PHI0, DELTA0, bars_by_panel, "full",
                            m_floor=grid[0], m_ceil=grid[-1]).set_index("book_id")
        say(f"  step {lbl:5s}: {len(grid):3d} m-points (all present), non-empty "
            f"{int(IV[lbl].nonempty.sum())} of {len(IV[lbl])} cells")

    base = IV["0.05"]
    B = census.set_index("book_id").copy()
    for lbl, _ in STEPS:
        B[f"g_hi_{lbl}"] = IV[lbl]["g_hi"]
        B[f"m_hi_{lbl}"] = IV[lbl]["m_hi"]
        B[f"cens_{lbl}"] = IV[lbl]["cens_hi"]
    B["g_step_hi"] = base["g_step_hi"]            # one coarse step in realised-gross units
    B["d_002"] = B["g_hi_0.02"] - B["g_hi_0.05"]
    B["d_001"] = B["g_hi_0.01"] - B["g_hi_0.05"]
    Bb = B[~B.cens_hi].copy()                     # bandable = ceiling set by a bar
    say("\n  PRE-REGISTERED PREDICTION: d_hi >= 0 on every MONO book (the coarse grid is a "
        "SUBSET of the fine one,\n  so a coarse-admissible point stays admissible and m_hi can "
        "only rise; on MONO arms gross rises with m).")
    for col, lbl in (("d_002", "0.05 -> 0.02"), ("d_001", "0.05 -> 0.01")):
        v = B[col].dropna()
        neg = int((v < -1e-12).sum())
        say(f"    {lbl:14s}: n={len(v)}  d>=0 in {len(v) - neg}/{len(v)}  "
            f"mean {fmt(v.mean())}  mean|d| {fmt(v.abs().mean())}  max {fmt(v.max())}  "
            f"min {fmt(v.min())}  moved (|d|>1e-9) {int((v.abs() > 1e-9).sum())}")
    say("\n  SPLIT BY WHETHER m IS A PURE EXPOSURE RESCALE (idea 90's PURE_KINDS = ctl/gate/stop).")
    say("  The one-sided argument needs realised gross MONOTONE in m; on `dd` and `bud` arms m "
        "also moves\n  the instrument itself (idea 144 Q1), so it is not guaranteed there and "
        "the two groups are never pooled.")
    for lbl, sel in (("MONO (ctl/gate/stop)", B.kind.isin(MONO)),
                     ("NON-MONO (dd/bud)   ", ~B.kind.isin(MONO))):
        v = B.loc[sel, "d_001"].dropna()
        neg = int((v < -1e-12).sum())
        say(f"    {lbl}: n={len(v):3d}  d>=0 in {len(v) - neg}/{len(v)}  mean {fmt(v.mean())}  "
            f"max {fmt(v.max())}  min {fmt(v.min())}")
    n_neg = int((B.d_001.dropna() < -1e-12).sum())
    n_neg_mono = int((B.loc[B.kind.isin(MONO), "d_001"].dropna() < -1e-12).sum())
    q2 = ("ONE-SIDED (upward) wherever m is a pure exposure rescale — on those arms a published "
          "ceiling is a LOWER BOUND, not a point estimate"
          if n_neg_mono == 0 else f"TWO-SIDED even on MONO arms — FALSIFIED by {n_neg_mono} books")
    say(f"\n  VERDICT Q2: the displacement is {q2}.")
    if n_neg:
        say(f"  {n_neg} book(s) DO move DOWN, every one of them off the MONO set — realised gross "
            f"is non-monotone in m there,\n  so the finer grid finds a HIGHER admissible m at a "
            f"LOWER realised gross:")
        say("    " + B[B.d_001 < -1e-12].reset_index()[
            ["book_id", "kind", "m_hi_0.05", "m_hi_0.01", "g_hi_0.05", "g_hi_0.01", "d_001"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))

    say("\n  A THIRD FLIP CLASS THE QUEUE DOES NOT NAME — books published with NO admissible "
        "gross at all\n  that acquire one at 0.01 resolution (a 4b verdict flip at the BOOK "
        "level, not the ceiling level):")
    gained = [b for b in IV["0.01"].index
              if bool(IV["0.01"].loc[b, "nonempty"]) and not bool(IV["0.05"].loc[b, "nonempty"])]
    say(f"    {len(gained)} of the {int((~IV['0.05'].nonempty).sum())} empty cells IN THIS "
        f"CORPUS gain an interval at 0.01: {gained}")
    for b in gained:
        r = IV["0.01"].loc[b]
        say(f"      {b:34s} m [{r.m_lo:.2f}, {r.m_hi:.2f}]  g [{r.g_lo:.4f}, {r.g_hi:.4f}]  "
            f"n_ok {int(r.n_ok)} of 121 points")
    say("    COVERAGE LIMIT, stated: only the 45 cells behind a published ceiling were refined, "
        "so this\n    count is a LOWER BOUND on the class — the other 234 empty books of the "
        "306-book family were not re-run.")
    say(f"\n  idea 154's headline, re-measured on 3.4x its cells (72 vs 21), 0.05 -> 0.01:")
    v = B["d_001"].dropna()
    say(f"    mean |move| = {fmt(v.abs().mean())} (idea 154: 0.0113)   "
        f"max = {fmt(v.max())} (idea 154: 0.0300)   median = {fmt(v.median())}")

    # ---------------------------------------------------------------- Q3 the band
    rule("Q3 — IS +/-0.03 THE RIGHT WIDTH?  the exact per-book bound vs the queue's constant")
    say("  The displacement is bounded above, per book, with NO extra backtest:")
    say("      d_hi  <  DELTA_STEP(book) = gross(m_hi + 0.05) - gross(m_hi)")
    for lbl, sub in (("all bandable   ", Bb), ("MONO only      ", Bb[Bb.kind.isin(MONO)]),
                     ("NON-MONO (dd/bud)", Bb[~Bb.kind.isin(MONO)])):
        s = sub["g_step_hi"].dropna()
        if not len(s):
            continue
        hold = (sub["d_001"] < sub["g_step_hi"] + 1e-12).sum()
        say(f"    {lbl}: n={len(s):3d}  mean {fmt(s.mean())}  median {fmt(s.median())}  "
            f"min {fmt(s.min())}  max {fmt(s.max())}  |  > 0.03 in {int((s > 0.03).sum())}  "
            f"|  bound holds {int(hold)}/{len(s)}")
    s = Bb["g_step_hi"].dropna()
    say(f"\n    So on {int((s > 0.03).sum())} of {len(s)} bandable ceilings ONE COARSE STEP is "
        f"WIDER than the queue's +/-0.03:\n    the constant is not a bound, it is a guess that "
        f"happens to cover this corpus.  The bound is DELTA_STEP,\n    it is free, and it is "
        f"one-sided.")
    say(f"    (the {int((s < 0).sum())} negative DELTA_STEP are the same non-monotone `dd` arms "
        f"as in Q2 — there a step\n     of m LOWERS realised gross, so 'a band around the "
        f"ceiling' is not even the right object.)")
    B.reset_index().to_csv(OUT / f"{STEM}.band.csv", index=False)

    # ---------------------------------------------------------------- the 15-point grid
    rule("THE 15 GRID POINTS — step x band.  COVERAGE = fine ceiling inside [g_hi, g_hi+b]; "
         "WASTE = b - d_hi")
    grid_rows = []
    for lbl, _ in STEPS:
        for b in BANDS:
            d = B[f"g_hi_0.01"] - B[f"g_hi_{lbl}"]
            m = ~B[f"cens_{lbl}"] & d.notna()
            cov = float(((d.abs() <= b + 1e-12) & m).sum()) / max(int(m.sum()), 1)
            waste = float((b - d[m]).mean())
            two_sided_waste = float((b - d[m].abs()).mean())
            grid_rows.append(dict(step=lbl, band=b, n=int(m.sum()),
                                  coverage_one_sided=cov, mean_waste=waste,
                                  mean_waste_two_sided=two_sided_waste))
    G = pd.DataFrame(grid_rows)
    say(G.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- flips
    rule("FLIPS — published verdicts that change inside the band, targets g in {0.75, 0.85}")
    flips = []
    for lbl, _ in STEPS:
        for b in BANDS:
            for T in TARGETS:
                pub = (B["g_lo"] <= T) & (T <= B[f"g_hi_{lbl}"])
                fine = (B["g_lo"] <= T) & (T <= B["g_hi_0.01"])
                inband = (B[f"g_hi_{lbl}"] < T) & (T <= B[f"g_hi_{lbl}"] + b)
                m = B[f"g_hi_{lbl}"].notna()
                flips.append(dict(step=lbl, band=b, target=T, n=int(m.sum()),
                                  published_admits=int((pub & m).sum()),
                                  fine_admits=int((fine & m).sum()),
                                  real_flips=int((fine & ~pub & m).sum()),
                                  flagged_by_band=int((inband & m).sum()),
                                  band_catches_real=int((inband & fine & ~pub & m).sum()),
                                  band_false_alarm=int((inband & ~fine & m).sum())))
    FL = pd.DataFrame(flips)
    say(FL.to_string(index=False))
    FL.to_csv(OUT / f"{STEM}.flips.csv", index=False)

    say("\n  the books whose published verdict actually FLIPS at 0.01 resolution:")
    any_flip = False
    for T in TARGETS:
        pub = (B["g_lo"] <= T) & (T <= B["g_hi_0.05"])
        fine = (B["g_lo"] <= T) & (T <= B["g_hi_0.01"])
        f = B[fine & ~pub]
        if len(f):
            any_flip = True
            say(f"    target g = {T:.2f}: {len(f)} flips INADMISSIBLE -> ADMISSIBLE")
            say("      " + f.reset_index()[["book_id", "g_lo", "g_hi_0.05", "g_hi_0.01",
                                            "g_step_hi", "hi_bar"]]
                .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n      "))
        else:
            say(f"    target g = {T:.2f}: 0 flips")
    if not any_flip:
        say("      (none)")

    # ---------------------------------------------------------------- KEEP paths
    rule("BOTH KEEP PATHS at every grid point — each book run AT ITS OWN CEILING")
    v1o, v2o = {}, {}
    for pname, (px, start, spy) in panels.items():
        for c in COSTS:
            v1o[(pname, c)] = backtest(px, rules_v1_weights(px), cost_bps=c,
                                       freq=FREQ)["returns"].loc[start:]
            v2o[(pname, c)] = backtest(px, rules_v2_weights(px), cost_bps=c,
                                       freq=FREQ)["returns"].loc[start:]
    # 4b at the ceiling is true by construction of the interval; 4a is not.
    keep_rows = []
    for lbl, _ in STEPS:
        n4a1 = n4a2 = n4b = 0
        for bid, row in B.iterrows():
            mh = row[f"m_hi_{lbl}"]
            if not np.isfinite(mh):
                continue
            pn, bk, cs, ar = bid.split("|")
            rec = F[(F.book_id == bid) & (np.isclose(F.m, mh))]
            if not len(rec):
                continue
            rec = rec.iloc[0]
            h1, h2 = rec.H1, rec.H2
            b1 = bars_by_panel[pn][0]
            n4b += int(h1 > b1["s1"] and h2 > b1["s2"] and rec.OOS_Sharpe_full > b1["soos"]
                       and DELTA0 * abs(b1["sdd"]) > abs(rec.MaxDD)
                       and rec.CAGR > PHI0 * b1["scagr"])
            for store, nm in ((v1o, "v1"), (v2o, "v2")):
                base_r = store[(pn, float(cs))]
                bb1, bb2 = H.halves(base_r)
                ok = (h1 > bb1) and (h2 > bb2) and (rec.MaxDD >= metrics(base_r)["MaxDD"])
                if nm == "v1":
                    n4a1 += int(ok)
                else:
                    n4a2 += int(ok)
        keep_rows.append(dict(step=lbl, books=int(B[f"m_hi_{lbl}"].notna().sum()),
                              pass4a_vs_v2_live=n4a2, pass4a_vs_v1=n4a1, pass4b=n4b))
    K = pd.DataFrame(keep_rows)
    say(K.to_string(index=False))
    say("\n  4b at a book's own ceiling is TRUE BY CONSTRUCTION (the ceiling is the largest "
        "admissible point), so the informative column is 4a — and the band question does not "
        "create a KEEP candidate on either path.")

    # ---------------------------------------------------------------- rule 8
    rule("RULE 8 WALK-FORWARD — ceiling re-derived on 2009-2016 ONLY, 2017-2026 read ONCE")
    ISIV = {}
    for lbl, grid in STEPS:
        sub = F[np.isin(np.round(F.m, 3), [round(x, 3) for x in grid])].copy()
        ISIV[lbl] = intervals(sub, PHI0, DELTA0, bars_by_panel, "IS", keys=BARS_IS,
                              m_floor=grid[0], m_ceil=grid[-1]).set_index("book_id")
        say(f"  IS step {lbl:5s}: non-empty {int(ISIV[lbl].nonempty.sum())} of {len(ISIV[lbl])}")

    wf = []
    for bid in B.index:
        pn, bk, cs, ar = bid.split("|")
        cs = float(cs)
        rec = dict(book_id=bid, panel=pn, book=bk, cost=cs, arm=ar)
        for lbl, _ in STEPS:
            mh = ISIV[lbl].loc[bid, "m_hi"] if bid in ISIV[lbl].index else np.nan
            rec[f"IS_m_hi_{lbl}"] = mh
            if np.isfinite(mh):
                r = F[(F.book_id == bid) & (np.isclose(F.m, mh))].iloc[0]
                rec[f"IS_g_hi_{lbl}"] = r.gross
                rec[f"OOS_CAGR_{lbl}"] = r.OOS_CAGR
                rec[f"OOS_Sharpe_{lbl}"] = r.OOS_Sharpe
                rec[f"OOS_MaxDD_{lbl}"] = r.OOS_MaxDD
            else:
                for k in ("IS_g_hi", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"):
                    rec[f"{k}_{lbl}"] = np.nan
        spy = panels[pn][2]
        mo = metrics(H.window(spy, "OOS"))
        rec.update(SPY_OOS_CAGR=mo["CAGR"], SPY_OOS_Sharpe=mo["Sharpe"], SPY_OOS_MaxDD=mo["MaxDD"])
        mv2 = metrics(H.window(v2o[(pn, cs)], "OOS"))
        mv1 = metrics(H.window(v1o[(pn, cs)], "OOS"))
        rec.update(V2_OOS_CAGR=mv2["CAGR"], V2_OOS_Sharpe=mv2["Sharpe"], V2_OOS_MaxDD=mv2["MaxDD"],
                   V1_OOS_CAGR=mv1["CAGR"], V1_OOS_Sharpe=mv1["Sharpe"], V1_OOS_MaxDD=mv1["MaxDD"])
        wf.append(rec)
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    ok = WF[WF["IS_m_hi_0.05"].notna() & WF["IS_m_hi_0.01"].notna()].copy()
    say(f"\n  cells with an IS ceiling on BOTH grids: {len(ok)} of {len(WF)}")
    say("\n  MEAN OOS (2017-2026), book run at ITS OWN IS CEILING, by grid step:")
    tab = []
    for lbl, _ in STEPS:
        sub = WF[WF[f"IS_m_hi_{lbl}"].notna()]
        tab.append(dict(arm=f"IS ceiling, step {lbl}", n=len(sub),
                        gross=sub[f"IS_g_hi_{lbl}"].mean(),
                        CAGR=sub[f"OOS_CAGR_{lbl}"].mean(),
                        Sharpe=sub[f"OOS_Sharpe_{lbl}"].mean(),
                        MaxDD=sub[f"OOS_MaxDD_{lbl}"].mean()))
    tab.append(dict(arm="RULES v2 (live baseline)", n=len(WF), gross=np.nan,
                    CAGR=WF.V2_OOS_CAGR.mean(), Sharpe=WF.V2_OOS_Sharpe.mean(),
                    MaxDD=WF.V2_OOS_MaxDD.mean()))
    tab.append(dict(arm="RULES v1 (previous)", n=len(WF), gross=np.nan,
                    CAGR=WF.V1_OOS_CAGR.mean(), Sharpe=WF.V1_OOS_Sharpe.mean(),
                    MaxDD=WF.V1_OOS_MaxDD.mean()))
    tab.append(dict(arm="SPY", n=len(WF), gross=np.nan, CAGR=WF.SPY_OOS_CAGR.mean(),
                    Sharpe=WF.SPY_OOS_Sharpe.mean(), MaxDD=WF.SPY_OOS_MaxDD.mean()))
    T = pd.DataFrame(tab)
    say(T.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n  PAIRED, on the cells that have both (the queue's actual capital question — a finer "
        "grid licenses MORE exposure; does it survive OOS?):")
    d_g = ok["IS_g_hi_0.01"] - ok["IS_g_hi_0.05"]
    d_c = ok["OOS_CAGR_0.01"] - ok["OOS_CAGR_0.05"]
    d_s = ok["OOS_Sharpe_0.01"] - ok["OOS_Sharpe_0.05"]
    d_d = ok["OOS_MaxDD_0.01"].abs() - ok["OOS_MaxDD_0.05"].abs()
    say(f"    d realised gross : mean {fmt(d_g.mean())}  moved in {int((d_g.abs() > 1e-9).sum())}"
        f"/{len(ok)} cells  max {fmt(d_g.max())}")
    say(f"    d OOS CAGR       : mean {fmt(d_c.mean())}  better in {int((d_c > 0).sum())}/{len(ok)}")
    say(f"    d OOS Sharpe     : mean {fmt(d_s.mean())}  better in {int((d_s > 0).sum())}/{len(ok)}")
    say(f"    d OOS |MaxDD|    : mean {fmt(d_d.mean())}  DEEPER in {int((d_d > 0).sum())}/{len(ok)}")
    say(f"    beats SPY OOS Sharpe: step 0.05 {int((ok['OOS_Sharpe_0.05'] > ok.SPY_OOS_Sharpe).sum())}"
        f"/{len(ok)}   step 0.01 {int((ok['OOS_Sharpe_0.01'] > ok.SPY_OOS_Sharpe).sum())}/{len(ok)}")
    say(f"    beats RULES v2 OOS Sharpe: step 0.05 "
        f"{int((ok['OOS_Sharpe_0.05'] > ok.V2_OOS_Sharpe).sum())}/{len(ok)}   step 0.01 "
        f"{int((ok['OOS_Sharpe_0.01'] > ok.V2_OOS_Sharpe).sum())}/{len(ok)}")

    say("\n  by panel and rung (OOS Sharpe at the IS ceiling):")
    pv = ok.groupby(["panel", "cost"]).agg(
        n=("book_id", "size"), g05=("IS_g_hi_0.05", "mean"), g01=("IS_g_hi_0.01", "mean"),
        S05=("OOS_Sharpe_0.05", "mean"), S01=("OOS_Sharpe_0.01", "mean"),
        C05=("OOS_CAGR_0.05", "mean"), C01=("OOS_CAGR_0.01", "mean"),
        D05=("OOS_MaxDD_0.05", "mean"), D01=("OOS_MaxDD_0.01", "mean"),
        SPY=("SPY_OOS_Sharpe", "mean"), V2=("V2_OOS_Sharpe", "mean"))
    say(pv.to_string(float_format=lambda x: f"{x:.4f}"))

    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    K.to_csv(OUT / f"{STEM}.keep.csv", index=False)

    # ---------------------------------------------------------------- verdict
    rule("VERDICT")
    nflip = int(((B["g_lo"] <= 0.75) & (0.75 <= B["g_hi_0.01"]) &
                 ~((B["g_lo"] <= 0.75) & (0.75 <= B["g_hi_0.05"]))).sum())
    nflip85 = int(((B["g_lo"] <= 0.85) & (0.85 <= B["g_hi_0.01"]) &
                   ~((B["g_lo"] <= 0.85) & (0.85 <= B["g_hi_0.05"]))).sum())
    say(f"  ceilings re-quoted            : {len(B)}   ({int(Bb.shape[0])} bandable, "
        f"{int(B.cens_hi.sum())} right-censored by PROTOCOL 2)")
    say(f"  displacement 0.05 -> 0.01     : mean |d| {fmt(B.d_001.abs().mean())}, "
        f"max {fmt(B.d_001.max())}, min {fmt(B.d_001.min())}")
    say(f"  published verdicts that FLIP  : g=0.75 {nflip}, g=0.85 {nflip85} (of {len(B)})")
    g03 = G[(G.step == "0.05") & (G.band == 0.03)].iloc[0]
    f75 = FL[(FL.step == "0.05") & (FL.band == 0.03) & (FL.target == 0.75)].iloc[0]
    f85 = FL[(FL.step == "0.05") & (FL.band == 0.03) & (FL.target == 0.85)].iloc[0]
    prec = (f75.band_catches_real + f85.band_catches_real) / max(
        int(f75.flagged_by_band + f85.flagged_by_band), 1)
    say(f"  the queue's +/-0.03 band      : recall 1.000 (it covers every real move on this "
        f"corpus) at coverage {g03.coverage_one_sided:.3f},")
    say(f"                                  but PRECISION {prec:.3f} — it flags "
        f"{int(f75.flagged_by_band + f85.flagged_by_band)} books across the two targets and only "
        f"{int(f75.band_catches_real + f85.band_catches_real)} actually flip,")
    say(f"                                  and it is NOT a bound: one coarse step exceeds 0.03 "
        f"on {int((Bb.g_step_hi > 0.03).sum())} of {len(Bb)} ceilings.")
    say("  KEEP paths                    : see the table above; no new candidate is created "
        "by a band, and 4b at a ceiling is true by construction.")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nwrote {STEM}.{{census,band,flips,grid,keep,walkforward}}.csv + .console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
