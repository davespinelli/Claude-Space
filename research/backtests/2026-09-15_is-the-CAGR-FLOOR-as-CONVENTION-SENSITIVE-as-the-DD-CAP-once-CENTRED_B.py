#!/usr/bin/env python3
"""Idea 879 (lane B, 2026-09-15) - is-the-CAGR-FLOOR-as-CONVENTION-SENSITIVE-as-the-DD-CAP-once-its-MARGINS-are-CENTRED.

QUESTION
--------
Idea 808 ran 12 books x 21 monthly rebalance offsets and reported, per 4b leg, the ratio
    ratio = margin(k=0) / spread(across offsets)
with ratio < 1 meaning "the published verdict on that leg is a date, not a rule".  It found

    leg    median ratio   books ratio<1   offset flips
    DD          0.466        10 / 12          52
    CAGR        0.877         8 / 12           3

and printed the honest qualification itself: CAGR is nearly as bad on the RATIO and is only
innocent-looking on FLIPS because most books' CAGR margins sit far from zero in either direction,
so few offsets cross the floor.  That qualification is a hypothesis, not a measurement.  This run
measures it: build books that sit DELIBERATELY NEAR the CAGR floor and ask whether the CAGR leg's
flip count converges on the DD leg's.

If it converges, 808's 52-vs-3 is a LOCATION fact about where the shelf's books happen to sit, and
PROTOCOL's CAGR floor is exactly as convention-sensitive as its DD cap.  If it does NOT converge,
the asymmetry is a real property of the two legs and the CAGR floor is the sounder clause.

HOW THE BOOKS ARE CENTRED (the dial is structural, not a third tuned parameter)
------------------------------------------------------------------------------
Long-only de-grossed books move their CAGR almost linearly in the gross dial g, so g is the one
knob that slides a book's CAGR margin through zero without changing what it holds.  A FIXED,
FULLY-REPORTED gross grid g = 0.50 .. 1.00 step 0.05 (11 rungs) is run for all 5 distinct book
forms of idea 808 (MADG, TOP20, TOP40, EWELIG, RULESV2 - 808's MADG100/MADG075 are one form at two
rungs of this very dial) on both panels: 5 x 11 x 2 = 110 books, EVERY ONE reported pass or fail.
Idea 808's own 12 books ARE 12 of these 110 - the (form, gross) pairs it declared - so gate G2 and
every hypothesis below read identical return paths.  The near-floor sets are then SELECTED OUT of
that fixed grid by a declared band, never fitted.

    CAGR-CENTRED set : |CAGR margin at k=0| <= band (percentage points)
    DD-CENTRED set   : |DD  margin at k=0| <= band (percentage points)

Both legs get the same treatment, so the comparison is like-for-like: 808 compared a CAGR leg that
was far from its floor with a DD leg that was near its cap, which is precisely the confound.

THE TWO TUNED PARAMETERS (the queue's own; nothing else is selected on)
  1. MARGIN BAND   b in {0.5, 1.0, 2.0} pp   (the queue names 1pp; 0.5 and 2.0 bracket it)
  2. OFFSET GRID   MONTHLY-21 (k=0..20, idea 805/808's own), MONTHLY-11 (k=0..10),
                   WEEKLY-5 (k=0..4)
All 3 x 3 = 9 grid points are reported for every hypothesis.

REPORTED-NEVER-SELECTED: panel (U56, B136), book form (5), gross rung (11), cost rung (10 / 25 bps),
execution lag (1, 2), window (FULL / IS / OOS), realised gross, both KEEP paths at every cell.

GATES (printed before any hypothesis is read)
  G1 engine : fast_run vs engine.backtest on MADG/U56 g=1.00, monthly k=0, lag 1, 10 bps.  bar 1e-9
  G2 repro  : idea 808's own headline table reproduced on its own 12 books (the 6 forms at their
              declared grosses x 2 panels), MONTHLY-21, FULL, 10 bps, lag 1:
              median ratio DD 0.466 / CAGR 0.877 (bar 0.01), books ratio<1 10/12 and 8/12 (exact),
              flips DD 52 / CAGR 3 (exact).  If this fails, this run is not measuring 808's object
              and it is said so rather than worked around.
  G3 bars   : SPY and RULES v2 (live) printed on both panels with all four 4b bars as numbers.
  G4 census : every band x leg cell reports how many of the 110 books it admits; a band that
              admits fewer than 5 books is reported as underpowered rather than quoted.

PRE-REGISTERED HYPOTHESES (written before any number below was run; the only numbers in hand are
idea 808's published ones, which the queue itself quotes)
  H_CONVERGE : (the queue's) on the CAGR-CENTRED set the CAGR leg's FLIP RATE converges on the DD
               leg's flip rate on the DD-CENTRED set: |rate_CAGR - rate_DD| <= 10pp at the 1pp band.
  H_RAW      : 808's raw 52-vs-3 is a LOCATION artefact of the shelf's own grosses - on 808's own
               12 books the median |ratio| of the CAGR leg is at least 2x the DD leg's.
  H_LOC      : flip rate is a single-index function of |ratio| alone, common to both legs: binned
               on |ratio|, the two legs' flip-rate curves agree within 10pp in every populated bin,
               and leg identity adds < 0.05 to the R^2 of a fit on |ratio|.
  H_SPREADEQ : (the falsifiable alternative to H_CONVERGE) CAGR is INTRINSICALLY less
               convention-noisy - after centring, its flip rate stays more than 10pp BELOW DD's.
               H_CONVERGE and H_SPREADEQ cannot both hold; if neither does the answer is PARTIAL.
  H_NOFREE   : a CAGR-centred book is by construction a coin toss - no book in the 1pp CAGR-centred
               set passes 4b on a strict majority of its offsets.
  H_WF       : (rule 8) a book centred on the IS window is still centred out of sample -
               Spearman rho(IS CAGR margin, OOS CAGR margin) across the 110 books >= +0.5 AND at
               least half of the IS-centred books are still inside the band OOS.  If this fails,
               "near the floor" is not knowable before the outcome window is read and no clause can
               be applied to it ex ante.

RULE 8 WALK-FORWARD (required, run whatever the verdict)
  IS = window start .. 2016-12-31 (read and fitted).  OOS = 2017-01-01 .. end (read once).
  The declared IS-ONLY selector: for each of the 5 forms x 2 panels, take the gross rung that
  MINIMISES |CAGR margin| on the IS window.  That book's OOS CAGR / Sharpe / MaxDD is then read
  once against RULES v2 (live) OOS and SPY OOS, and both KEEP paths are evaluated.  The unselected
  base rate over all 110 books is reported beside it so the selector is not flattered.

KEEP PATHS: 4a (Sharpe > RULES v2 live in BOTH halves and MaxDD no worse) and 4b (Sharpe > SPY in
both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's) evaluated at every cell.

SURVIVORSHIP: U56 and B136 are CURRENT-constituent lists.  Dead names are absent, so every CAGR is
biased upward and the 4b CAGR floor (0.70 x SPY, measured on the same survivor-free benchmark) is
easier to clear than on a point-in-time panel.  This run's object - the SPREAD and the FLIP RATE of
a leg across equally arbitrary calendars - is a within-book quantity and far less exposed to that
bias than the levels are; the levels quoted in the rule-8 section are not corrected for it.

PROTOCOL: 10 bps per unit turnover, next-day fills, no shorting, no leverage.  Deterministic,
standalone, no network.  Modifies nothing but its own outputs:
    .cells.csv  .legs.csv  .centred.csv  .loc.csv  .walkforward.csv  .console.txt
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score, metrics, backtest  # noqa: E402
from engine import rebalance_mask  # noqa: E402

STAMP = "2026-09-15_is-the-CAGR-FLOOR-as-CONVENTION-SENSITIVE-as-the-DD-CAP-once-CENTRED_B"
OUT = ROOT / "research" / "backtests"

COST_MAIN, LAG_MAIN = 10.0, 1
CGRID = [10.0, 25.0]
LAGS = [1, 2]
GROSS = [round(0.50 + 0.05 * i, 2) for i in range(11)]        # 0.50 .. 1.00, fully reported
FAMILY = {"MONTHLY21": ("M", list(range(21))),
          "MONTHLY11": ("M", list(range(11))),
          "WEEKLY5": ("W", list(range(5)))}
BANDS = [0.5, 1.0, 2.0]                                        # tuned param 1 (pp)
IS_END, OOS_START = "2016-12-31", "2017-01-01"
MA_WIN, WARMUP, MAX_VOL = 200, 260, 0.60
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]

# idea 808's own 12 books, at the grosses it declared (for gate G2)
BOOK808 = [("MADG", 1.00, "MADG100"), ("MADG", 0.75, "MADG075"), ("TOP20", 0.75, "TOP20"),
           ("TOP40", 1.00, "TOP40"), ("EWELIG", 0.75, "EWELIG"), ("RULESV2", 0.75, "RULESV2")]
PUB808 = dict(med_ratio_DD=0.466, med_ratio_CAGR=0.877, lt1_DD=10, lt1_CAGR=8,
              flips_DD=52, flips_CAGR=3)

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ the books (808's six forms)
def ma_dg_weights(px, g):
    """MA-DG (idea 805): g/N over all priced names, zeroed below the 200d MA (to cash)."""
    pm = px.notna()
    ma = (px > px.rolling(MA_WIN).mean()) & pm
    cnt = pm.sum(axis=1).replace(0, np.nan)
    return (g * pm.div(cnt, axis=0).fillna(0.0)).where(ma, 0.0)


def _elig(px):
    """RULES v1 eligibility, verbatim: above the 200d MA and vol20 < 0.60."""
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def top_n_weights(px, n, g):
    """Top n eligible by the v1 composite WITHOUT the vol scaler, g/n each (cash if fewer)."""
    s = score(px, vol_scale=False)[0]
    rank = s.where(_elig(px)).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (g / n)


def ew_elig_weights(px, g):
    """Equal weight over ALL eligible names at gross g (2026-09-03 Finding 2)."""
    e = _elig(px).astype(float)
    cnt = e.sum(axis=1).replace(0, np.nan)
    return (g * e.div(cnt, axis=0)).fillna(0.0)


FORMS = {
    "MADG": lambda px, g: ma_dg_weights(px, g),
    "MADG075": None,          # placeholder removed below; MADG075 is MADG at g=0.75
    "TOP20": lambda px, g: top_n_weights(px, 20, g),
    "TOP40": lambda px, g: top_n_weights(px, 40, g),
    "EWELIG": lambda px, g: ew_elig_weights(px, g),
    "RULESV2": lambda px, g: rules_v2_weights(px, band=0.03, gross=g),
}
del FORMS["MADG075"]
FORM_NAMES = list(FORMS)     # MADG, TOP20, TOP40, EWELIG, RULESV2  (5 forms x 11 gross x 2 panels)


def shifted_mask(idx, freq, k):
    """Period-end rebalance calendar moved k TRADING days later (k = 0 is PROTOCOL's own)."""
    m = rebalance_mask(idx, freq).values
    if k == 0:
        return pd.Series(m, index=idx)
    pos = np.flatnonzero(m) + k
    pos = pos[pos < len(idx)]
    out = np.zeros(len(idx), dtype=bool)
    out[pos] = True
    return pd.Series(out, index=idx)


# ------------------------------------------------------------------ vectorised runner (805/808's)
def fast_run(prices, weights, mask, lag):
    """(gross return path before costs, turnover path, realised gross).
    r(c) = r_gross - turn * c/1e4 exactly, because cost is a same-day subtraction."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(lag).fillna(0.0).values
    mk = mask.shift(lag, fill_value=False).values.copy()
    mk[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (pd.Series((held * rets).sum(axis=1), index=idx),
            pd.Series(turn, index=idx),
            pd.Series(held.sum(axis=1), index=idx))


# ------------------------------------------------------------------ 4b arithmetic (808's, verbatim)
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def margins(r, spy, window):
    """The five 4b legs as MARGINS in their own units.  window in {FULL, IS, OOS}.
    Inside IS/OOS the 'OOS' leg collapses into that window's own second half (named, not hidden)."""
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    if window == "FULL":
        oos = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    else:
        oos = a2 - s2
    return {"H1": a1 - s1, "H2": a2 - s2, "OOS": oos,
            "DD": (m["MaxDD"] - 0.60 * ms["MaxDD"]) * 100.0,
            "CAGR": (m["CAGR"] - 0.70 * ms["CAGR"]) * 100.0,
            "_CAGR": m["CAGR"], "_Sharpe": m["Sharpe"], "_MaxDD": m["MaxDD"]}


def spearman(a, b):
    """Rank-then-Pearson; scipy is not installed in the sandbox."""
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    if ok.sum() < 3:
        return float("nan")
    return float(a[ok].rank().corr(b[ok].rank()))


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def keep_4b(mg):
    return bool(mg["H1"] > 0 and mg["H2"] > 0 and mg["OOS"] > 0 and mg["DD"] > 0 and mg["CAGR"] > 0)


# ================================================================== run
def main():
    t0 = time.time()
    P(f"# {STAMP}")
    P(f"# pandas {pd.__version__} numpy {np.__version__}")
    P("# 5 forms x 11 gross rungs x 2 panels = 110 grid books, plus 808's own 12 for gate G2")
    P("# x 26 calendars (21 monthly + 5 weekly, MONTHLY11 a subset of MONTHLY21) x 2 lags x 2 costs")

    panels = {"U56": load_universe().dropna(how="all").ffill(),
              "B136": load_universe(broad=True).dropna(how="all").ffill()}
    for nm, px in panels.items():
        P(f"PANEL {nm}: {px.shape[1]} names x {len(px)} days, {px.index[0].date()} .. {px.index[-1].date()}")
    P("SPY is a tradable constituent of both panels AND the 4b comparand (the record's construction).")

    ctx = {}
    for nm, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base = backtest(px, rules_v2_weights(px), cost_bps=COST_MAIN, freq="W")["returns"].loc[start:]
        ctx[nm] = dict(px=px, start=start, spy=spy, base=base)
        P(f"WINDOW {nm}: {start.date()} .. {px.index[-1].date()}  IS ..{IS_END}  OOS {OOS_START}..")

    # ---------------------------------------------------------------- G1 engine gate
    px = ctx["U56"]["px"]
    w = ma_dg_weights(px, 1.00)
    mk = shifted_mask(px.index, "M", 0)
    rg, tn, gr = fast_run(px, w, mk, LAG_MAIN)
    r_fast = (rg - tn * COST_MAIN / 1e4).loc[ctx["U56"]["start"]:]
    r_eng = backtest(px, w, cost_bps=COST_MAIN, freq="M")["returns"].loc[ctx["U56"]["start"]:]
    g1 = float(np.nanmax(np.abs(r_fast.values - r_eng.values)))
    P(f"\nG1 engine  max|fast_run - engine.backtest| = {g1:.3e}   bar 1e-9   "
      f"{'PASS' if g1 < 1e-9 else 'FAIL'}")

    # ---------------------------------------------------------------- G3 bars
    P("\nG3 comparand bars on this window:")
    for nm in panels:
        c = ctx[nm]
        ms, mb = metrics(c["spy"]), metrics(c["base"])
        s1, s2 = halves(c["spy"])
        P(f"  {nm}: SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} halves {s1:.3f}/{s2:.3f} "
          f"MaxDD {ms['MaxDD']:.2%}  ->  4b bars: DD cap {0.60*ms['MaxDD']:.2%}, "
          f"CAGR floor {0.70*ms['CAGR']:.2%}")
        P(f"       RULES v2 (live, weekly) CAGR {mb['CAGR']:.2%} Sharpe {mb['Sharpe']:.3f} "
          f"MaxDD {mb['MaxDD']:.2%}")

    # ---------------------------------------------------------------- build the book list
    # grid books (the fixed, fully-reported gross ladder) + 808's own 12 (gate G2 only, marked)
    books = []
    for pn in panels:
        for fm in FORM_NAMES:
            for g in GROSS:
                books.append(dict(panel=pn, form=fm, gross=g,
                                  label=f"{fm}@{int(round(g*100)):03d}"))
    B808KEY = {(fm, g) for fm, g, _ in BOOK808}
    P(f"\nBOOKS: {len(books)} GRID books = {len(FORM_NAMES)} forms x {len(GROSS)} gross rungs x 2 panels.")
    P("  idea 808's own 12 books are the 6 (form, gross) pairs it declared, taken OUT of this same")
    P("  grid rather than re-run, so gate G2 and the hypotheses read identical return paths:")
    P("  " + ", ".join(f"{lbl}={fm}@{g:.2f}" for fm, g, lbl in BOOK808))

    # ---------------------------------------------------------------- all cells
    P("\nrunning cells ...")
    rows = []
    n_run = 0
    for pn, c in ctx.items():
        px, start, spy, base = c["px"], c["start"], c["spy"], c["base"]
        wcache = {}
        for bk in [b for b in books if b["panel"] == pn]:
            key = (bk["form"], bk["gross"])
            if key not in wcache:
                wcache[key] = FORMS[bk["form"]](px, bk["gross"])
            wts = wcache[key]
            for fam, (freq, offs) in FAMILY.items():
                if fam == "MONTHLY11":
                    continue          # strict subset of MONTHLY21; re-derived, never re-run
                for k in offs:
                    mk = shifted_mask(px.index, freq, k)
                    for lag in LAGS:
                        rg, tn, gr = fast_run(px, wts, mk, lag)
                        rg, tn, gr = rg.loc[start:], tn.loc[start:], gr.loc[start:]
                        n_run += 1
                        for cost in CGRID:
                            r = rg - tn * cost / 1e4
                            for win, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                                ("OOS", OOS_START, None)):
                                mg = margins(r.loc[lo:hi], spy.loc[lo:hi], win)
                                rows.append(dict(
                                    panel=pn, form=bk["form"], gross=bk["gross"],
                                    label=bk["label"],
                                    is808=((bk["form"], bk["gross"]) in B808KEY),
                                    family=fam, k=k, lag=lag, cost=cost, window=win,
                                    CAGR=mg["_CAGR"], Sharpe=mg["_Sharpe"], MaxDD=mg["_MaxDD"],
                                    realised_gross=float(gr.mean()),
                                    turnover=float(tn.sum() / max(1e-9, (len(tn) / 252.0))),
                                    **{f"m_{L}": mg[L] for L in LEGS},
                                    keep4b=keep_4b(mg),
                                    keep4a=keep_4a(r.loc[lo:hi], base.loc[lo:hi])))
        P(f"  {pn}: {n_run} fast_run calls, {time.time()-t0:.0f}s")
    cells = pd.DataFrame(rows)
    # MONTHLY11 is the k<=10 subset of MONTHLY21 - derived, not re-run
    m11 = cells[(cells.family == "MONTHLY21") & (cells.k <= 10)].copy()
    m11["family"] = "MONTHLY11"
    cells = pd.concat([cells, m11], ignore_index=True)
    cells.to_csv(OUT / f"{STAMP}.cells.csv", index=False)
    P(f"cells: {len(cells)} rows -> {STAMP}.cells.csv   ({time.time()-t0:.0f}s)")

    # ---------------------------------------------------------------- per-book-per-leg legs table
    legrows = []
    for (pn, lbl, bs, fm, g, fam, lag, cost, win), grp in cells.groupby(
            ["panel", "label", "is808", "form", "gross", "family", "lag", "cost", "window"]):
        grp = grp.sort_values("k")
        k0 = grp[grp.k == 0]
        if k0.empty:
            continue
        for L in LEGS:
            v = grp[f"m_{L}"].values
            m0 = float(k0[f"m_{L}"].iloc[0])
            spread = float(np.nanmax(v) - np.nanmin(v))
            sd = float(np.nanstd(v, ddof=1)) if len(v) > 1 else np.nan
            flips = int(np.sum((v > 0) != (m0 > 0)))          # k=0 never flips against itself
            legrows.append(dict(panel=pn, label=lbl, is808=bs, form=fm, gross=g, family=fam,
                                lag=lag, cost=cost, window=win, leg=L, margin0=m0, spread=spread,
                                sd=sd, ratio=(m0 / spread if spread > 0 else np.nan),
                                absratio=(abs(m0) / spread if spread > 0 else np.nan),
                                n_off=len(v), flips=flips, flip_rate=flips / len(v)))
    legs = pd.DataFrame(legrows)
    legs.to_csv(OUT / f"{STAMP}.legs.csv", index=False)
    P(f"legs: {len(legs)} rows -> {STAMP}.legs.csv")

    MAIN = dict(family="MONTHLY21", lag=LAG_MAIN, cost=COST_MAIN, window="FULL")

    def sel(df, **kw):
        m = pd.Series(True, index=df.index)
        for k_, v_ in kw.items():
            m &= (df[k_] == v_)
        return df[m]

    # ---------------------------------------------------------------- G2 reproduction of 808
    P("\nG2 reproduction of idea 808's headline table (its own 12 books, MONTHLY-21, FULL, 10bps, lag 1):")
    b8 = sel(legs, is808=True, **MAIN)
    P("  leg  | median ratio | min ratio | books ratio<1 | offset flips | mean spread")
    g2 = {}
    for L in LEGS:
        s = b8[b8.leg == L]
        g2[L] = dict(med=float(s.ratio.median()), lt1=int((s.ratio < 1).sum()),
                     flips=int(s.flips.sum()), mn=float(s.ratio.min()),
                     spr=float(s.spread.mean()))
        P(f"  {L:<5}| {g2[L]['med']:>12.3f} | {g2[L]['mn']:>9.3f} | {g2[L]['lt1']:>10d}/12 "
          f"| {g2[L]['flips']:>12d} | {g2[L]['spr']:.3f}")
    g2ok = []
    for nm_, got, want, tol in (("med DD", g2["DD"]["med"], PUB808["med_ratio_DD"], 0.01),
                                ("med CAGR", g2["CAGR"]["med"], PUB808["med_ratio_CAGR"], 0.01),
                                ("lt1 DD", g2["DD"]["lt1"], PUB808["lt1_DD"], 0),
                                ("lt1 CAGR", g2["CAGR"]["lt1"], PUB808["lt1_CAGR"], 0),
                                ("flips DD", g2["DD"]["flips"], PUB808["flips_DD"], 0),
                                ("flips CAGR", g2["CAGR"]["flips"], PUB808["flips_CAGR"], 0)):
        ok = abs(got - want) <= tol
        g2ok.append(ok)
        P(f"  G2 {nm_:<11} got {got!r:>8} want {want!r:>8} bar {tol}  {'PASS' if ok else 'FAIL'}")
    P(f"  G2 OVERALL: {sum(g2ok)}/6 {'PASS' if all(g2ok) else 'PARTIAL - stated, not worked around'}")

    # ---------------------------------------------------------------- G4 census of the bands
    P("\nG4 census - how many of the 110 GRID books each band admits "
      "(MONTHLY-21, FULL, 10bps, lag 1):")
    grid = sel(legs, **MAIN)
    cen_rows = []
    for band in BANDS:
        for L in ("CAGR", "DD"):
            s = grid[grid.leg == L]
            n = int((s.margin0.abs() <= band).sum())
            P(f"  band {band:>4}pp  {L:<4}-centred: {n:>3} of {len(s)} books"
              f"{'   UNDERPOWERED (<5)' if n < 5 else ''}")
            cen_rows.append(dict(band=band, leg=L, n_admitted=n, n_total=len(s)))

    # ---------------------------------------------------------------- H_RAW  (location artefact)
    P("\nH_RAW - are the shelf's CAGR margins simply further from zero than its DD margins?")
    P("  (median |ratio| = |margin at k=0| / offset spread; bar: CAGR >= 2x DD)")
    raw_rows = []
    for bs, nm_ in ((True, "808's own 12 books"), (None, "the 110-book gross grid")):
        s = sel(legs, **MAIN) if bs is None else sel(legs, is808=True, **MAIN)
        a = float(s[s.leg == "CAGR"].absratio.median())
        d = float(s[s.leg == "DD"].absratio.median())
        P(f"  {nm_:<24} median |ratio| CAGR {a:.3f}  DD {d:.3f}  x{a/d:.2f}"
          f"  {'PASS' if a >= 2*d else 'below the 2x bar'}")
        raw_rows.append(dict(bookset=("B808" if bs else "GRID"), med_absratio_CAGR=a, med_absratio_DD=d, mult=a/d))
    H_RAW = raw_rows[0]["mult"] >= 2.0
    P(f"  H_RAW ({'CONFIRMED' if H_RAW else 'REFUTED'}) on 808's own book set, the set the queue quotes")

    # ------------------------------------------------ H_CONVERGE / H_SPREADEQ over the 3x3 grid
    P("\nH_CONVERGE / H_SPREADEQ - flip rate of the CENTRED leg, all 9 (band x offset grid) points:")
    P("  band  family     | CAGR-centred: n  flips  rate | DD-centred: n  flips  rate |  gap(pp)")
    conv_rows = []
    for band in BANDS:
        for fam in FAMILY:
            out = {}
            for L in ("CAGR", "DD"):
                s = sel(legs, family=fam, lag=LAG_MAIN, cost=COST_MAIN, window="FULL")
                s = s[(s.leg == L) & (s.margin0.abs() <= band)]
                n, fl = len(s), int(s.flips.sum())
                tot = int(s.n_off.sum())
                out[L] = (n, fl, (fl / tot if tot else np.nan))
            gap = (out["CAGR"][2] - out["DD"][2]) * 100.0
            P(f"  {band:>4}  {fam:<10} |{out['CAGR'][0]:>16d} {out['CAGR'][1]:>6d} "
              f"{out['CAGR'][2]:>6.3f} |{out['DD'][0]:>13d} {out['DD'][1]:>6d} {out['DD'][2]:>6.3f} "
              f"| {gap:>+8.1f}")
            conv_rows.append(dict(band=band, family=fam, n_CAGR=out["CAGR"][0],
                                  flips_CAGR=out["CAGR"][1], rate_CAGR=out["CAGR"][2],
                                  n_DD=out["DD"][0], flips_DD=out["DD"][1], rate_DD=out["DD"][2],
                                  gap_pp=gap))
    conv = pd.DataFrame(conv_rows)
    conv.to_csv(OUT / f"{STAMP}.centred.csv", index=False)
    hdr = conv[(conv.band == 1.0) & (conv.family == "MONTHLY21")].iloc[0]
    H_CONV = bool(abs(hdr.gap_pp) <= 10.0 and hdr.n_CAGR >= 5 and hdr.n_DD >= 5)
    H_SPREADEQ = bool(hdr.gap_pp < -10.0 and hdr.n_CAGR >= 5 and hdr.n_DD >= 5)
    P(f"  HEADLINE (band 1.0pp, MONTHLY-21): CAGR rate {hdr.rate_CAGR:.3f} vs DD rate "
      f"{hdr.rate_DD:.3f}, gap {hdr.gap_pp:+.1f}pp, bar +/-10pp")
    P(f"  H_CONVERGE {'CONFIRMED' if H_CONV else 'REFUTED'} | "
      f"H_SPREADEQ {'CONFIRMED' if H_SPREADEQ else 'REFUTED'}"
      f"{'  (neither -> PARTIAL)' if not (H_CONV or H_SPREADEQ) else ''}")
    P(f"  ALL 9 points agree on H_CONVERGE: "
      f"{int((conv.gap_pp.abs() <= 10.0).sum())} of 9 inside the +/-10pp bar")

    # raw uncentred flip counts on the SAME grid, for the contrast 808 published
    unc = sel(legs, **MAIN)
    P("\n  contrast - UNCENTRED flip totals on the same 110-book grid (what 808 would have seen):")
    for L in LEGS:
        s = unc[unc.leg == L]
        P(f"    {L:<5} flips {int(s.flips.sum()):>5} of {int(s.n_off.sum()):>5} offsets "
          f"(rate {s.flips.sum()/s.n_off.sum():.3f})  median |ratio| {s.absratio.median():.3f}")

    # ---------------------------------------------------------------- H_LOC single-index law
    P("\nH_LOC - is the flip rate a single-index function of |ratio| alone, common to both legs?")
    EDGES = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 1e9]
    lab = ["[0,.25)", "[.25,.5)", "[.5,.75)", "[.75,1)", "[1,1.5)", "[1.5,2)", ">=2"]
    loc = sel(legs, **MAIN).copy()
    loc = loc[loc.leg.isin(["CAGR", "DD"]) & loc.absratio.notna()]
    loc["bin"] = pd.cut(loc.absratio, EDGES, right=False, labels=lab)
    P("  |ratio| bin  |  CAGR n  rate |   DD n  rate |  gap(pp)")
    loc_rows, gaps = [], []
    for b in lab:
        r = {}
        for L in ("CAGR", "DD"):
            s = loc[(loc.bin == b) & (loc.leg == L)]
            tot = int(s.n_off.sum())
            r[L] = (len(s), (int(s.flips.sum()) / tot if tot else np.nan))
        gp = (r["CAGR"][1] - r["DD"][1]) * 100.0
        both = r["CAGR"][0] >= 3 and r["DD"][0] >= 3
        if both and np.isfinite(gp):
            gaps.append(abs(gp))
        P(f"  {b:<12} | {r['CAGR'][0]:>6d} {r['CAGR'][1]:>5.3f} | {r['DD'][0]:>5d} "
          f"{r['DD'][1]:>5.3f} | {gp:>+8.1f}{'' if both else '   (sparse, excluded)'}")
        loc_rows.append(dict(bin=b, n_CAGR=r["CAGR"][0], rate_CAGR=r["CAGR"][1],
                             n_DD=r["DD"][0], rate_DD=r["DD"][1], gap_pp=gp, populated=both))
    pd.DataFrame(loc_rows).to_csv(OUT / f"{STAMP}.loc.csv", index=False)
    # R^2 of flip_rate on |ratio| alone vs |ratio| + leg dummy
    y = loc.flip_rate.values
    x1 = np.column_stack([np.ones(len(loc)), loc.absratio.clip(upper=3).values])
    x2 = np.column_stack([x1, (loc.leg == "CAGR").astype(float).values])

    def r2(X, y):
        b, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ b
        return 1.0 - e @ e / ((y - y.mean()) @ (y - y.mean()))
    r2a, r2b = r2(x1, y), r2(x2, y)
    H_LOC = bool((len(gaps) > 0 and max(gaps) <= 10.0) and (r2b - r2a) < 0.05)
    P(f"  R^2(|ratio|) {r2a:.4f}   R^2(|ratio| + leg dummy) {r2b:.4f}   delta {r2b-r2a:.4f} (bar 0.05)")
    P(f"  max |gap| over populated bins {max(gaps) if gaps else float('nan'):.1f}pp (bar 10pp)")
    P(f"  H_LOC {'CONFIRMED' if H_LOC else 'REFUTED'}")

    # ---------------------------------------------------------------- H_NOFREE
    P("\nH_NOFREE - does any CAGR-centred book pass 4b on a strict majority of its offsets?")
    c0 = sel(cells, **MAIN)
    m0 = sel(legs, **MAIN)
    m0 = m0[(m0.leg == "CAGR") & (m0.margin0.abs() <= 1.0)][["panel", "label"]]
    keyset = set(zip(m0.panel, m0.label))
    nofree_rows = []
    for (pn, lbl), grp in c0.groupby(["panel", "label"]):
        if (pn, lbl) not in keyset:
            continue
        npass = int(grp.keep4b.sum())
        nofree_rows.append(dict(panel=pn, label=lbl, n_off=len(grp), pass4b=npass,
                                pass4a=int(grp.keep4a.sum())))
    nf = pd.DataFrame(nofree_rows)
    if len(nf):
        P(nf.sort_values("pass4b", ascending=False).to_string(index=False))
        H_NOFREE = bool((nf.pass4b > nf.n_off / 2).sum() == 0)
        P(f"  books passing 4b on a strict majority of offsets: "
          f"{int((nf.pass4b > nf.n_off/2).sum())} of {len(nf)}   4a passes: {int(nf.pass4a.sum())}")
    else:
        H_NOFREE = None
        P("  (no CAGR-centred books at the 1pp band - underpowered)")
    P(f"  H_NOFREE {'CONFIRMED' if H_NOFREE else ('REFUTED' if H_NOFREE is False else 'N/A')}")

    # ---------------------------------------------------------------- H_WF / rule 8
    P("\n" + "=" * 100)
    P("RULE 8 WALK-FORWARD - IS .." + IS_END + "  read and fitted; OOS " + OOS_START + ".. read once")
    P("=" * 100)
    lw = sel(legs, family="MONTHLY21", lag=LAG_MAIN, cost=COST_MAIN)
    isw = lw[(lw.window == "IS") & (lw.leg == "CAGR")].set_index(["panel", "label"])
    oow = lw[(lw.window == "OOS") & (lw.leg == "CAGR")].set_index(["panel", "label"])
    j = isw[["margin0", "spread"]].join(oow[["margin0", "spread"]], lsuffix="_IS", rsuffix="_OOS",
                                        how="inner")
    rho_m = spearman(j.margin0_IS, j.margin0_OOS)
    rho_s = spearman(j.spread_IS, j.spread_OOS)
    P(f"H_WF  Spearman rho(IS CAGR margin, OOS CAGR margin) over {len(j)} books = {rho_m:+.3f}  (bar +0.50)")
    P(f"      Spearman rho(IS CAGR spread, OOS CAGR spread)                    = {rho_s:+.3f}")
    wf_rows = []
    for band in BANDS:
        inb = j[j.margin0_IS.abs() <= band]
        still = int((inb.margin0_OOS.abs() <= band).sum())
        frac = still / len(inb) if len(inb) else np.nan
        P(f"      band {band:>4}pp: {len(inb):>3} books centred IS -> {still:>3} still centred OOS "
          f"({frac:.1%}; bar 50%)")
        wf_rows.append(dict(band=band, n_IS_centred=len(inb), n_still_OOS=still, frac=frac))
    hb = [w for w in wf_rows if w["band"] == 1.0][0]
    H_WF = bool(rho_m >= 0.5 and (hb["frac"] >= 0.5 if hb["n_IS_centred"] else False))
    P(f"  H_WF {'CONFIRMED' if H_WF else 'REFUTED'}")

    # does the centred-leg flip finding itself walk forward?
    P("\n  does the H_CONVERGE result itself walk forward?  (centring done on the IS window only,")
    P("  flip rates then read on the OOS window's own offsets)")
    for band in BANDS:
        line = []
        for L in ("CAGR", "DD"):
            isl = lw[(lw.window == "IS") & (lw.leg == L)].set_index(["panel", "label"])
            sel_ = isl[isl.margin0.abs() <= band].index
            o = lw[(lw.window == "OOS") & (lw.leg == L)].set_index(["panel", "label"])
            o = o.loc[o.index.intersection(sel_)]
            tot = int(o.n_off.sum())
            line.append((len(o), int(o.flips.sum()) / tot if tot else np.nan))
        gp = (line[0][1] - line[1][1]) * 100.0
        P(f"    band {band:>4}pp  IS-centred CAGR n={line[0][0]:>3} OOS flip rate {line[0][1]:.3f} | "
          f"IS-centred DD n={line[1][0]:>3} OOS flip rate {line[1][1]:.3f} | gap {gp:+.1f}pp")
        wf_rows[[w["band"] for w in wf_rows].index(band)].update(
            oos_rate_CAGR=line[0][1], oos_rate_DD=line[1][1], oos_gap_pp=gp)
    pd.DataFrame(wf_rows).to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)

    # ---------------------------------------------------------------- rule 8 (b): the books
    P("\nRULE 8 BOOKS - declared IS-ONLY selector: per (form, panel) take the gross rung that")
    P("MINIMISES |CAGR margin| on the IS window; read its OOS triple once.  MONTHLY-21 k=0, 10bps, lag 1.")
    cf = sel(cells, family="MONTHLY21", k=0, lag=LAG_MAIN, cost=COST_MAIN)
    picks = []
    for (pn, fm), grp in cf[cf.window == "IS"].groupby(["panel", "form"]):
        row = grp.iloc[grp.m_CAGR.abs().values.argmin()]
        picks.append((pn, fm, row.gross, row.label))
    P(f"\n{'panel':<6}{'form':<9}{'g*_IS':>6}  {'OOS CAGR':>9}{'OOS Shrp':>9}{'OOS MaxDD':>10}"
      f"  {'FULL CAGR':>9}{'FULL Shrp':>9}{'FULL DD':>9}  4a  4b")
    book_rows = []
    for pn, fm, g, lbl in sorted(picks):
        o = cf[(cf.panel == pn) & (cf.label == lbl) & (cf.window == "OOS")].iloc[0]
        f = cf[(cf.panel == pn) & (cf.label == lbl) & (cf.window == "FULL")].iloc[0]
        P(f"{pn:<6}{fm:<9}{g:>6.2f}  {o.CAGR:>8.2%}{o.Sharpe:>9.3f}{o.MaxDD:>10.2%}"
          f"  {f.CAGR:>8.2%}{f.Sharpe:>9.3f}{f.MaxDD:>9.2%}"
          f"  {'Y' if f.keep4a else 'x'}   {'Y' if f.keep4b else 'x'}")
        book_rows.append(dict(panel=pn, form=fm, gross=g, label=lbl, oos_CAGR=o.CAGR,
                              oos_Sharpe=o.Sharpe, oos_MaxDD=o.MaxDD, full_CAGR=f.CAGR,
                              full_Sharpe=f.Sharpe, full_MaxDD=f.MaxDD,
                              keep4a=bool(f.keep4a), keep4b=bool(f.keep4b)))
    for pn in panels:
        c = ctx[pn]
        mo_s = metrics(c["spy"].loc[OOS_START:])
        mo_b = metrics(c["base"].loc[OOS_START:])
        P(f"  comparands {pn} OOS: RULES v2 (live) {mo_b['CAGR']:.2%} / {mo_b['Sharpe']:.3f} / "
          f"{mo_b['MaxDD']:.2%}   SPY {mo_s['CAGR']:.2%} / {mo_s['Sharpe']:.3f} / {mo_s['MaxDD']:.2%}")
    bp = pd.DataFrame(book_rows)
    P(f"\n  SELECTED books: 4a {int(bp.keep4a.sum())}/{len(bp)}   4b {int(bp.keep4b.sum())}/{len(bp)}")
    allg = sel(cells, family="MONTHLY21", k=0, lag=LAG_MAIN, cost=COST_MAIN,
               window="FULL")
    P(f"  UNSELECTED base rate over all {len(allg)} GRID books at k=0: "
      f"4a {allg.keep4a.mean():.1%}   4b {allg.keep4b.mean():.1%}")
    for pn in panels:
        s = allg[allg.panel == pn]
        P(f"    {pn}: 4a {s.keep4a.mean():.1%}  4b {s.keep4b.mean():.1%}  (n={len(s)})")

    # ---------------------------------------------------------------- robustness axes
    P("\nROBUSTNESS (reported, never selected on) - headline gap(pp) at band 1.0pp, MONTHLY-21:")
    P("  cost  lag | CAGR-centred rate | DD-centred rate |  gap(pp)")
    for cost in CGRID:
        for lag in LAGS:
            o = {}
            for L in ("CAGR", "DD"):
                s = sel(legs, family="MONTHLY21", lag=lag, cost=cost, window="FULL")
                s = s[(s.leg == L) & (s.margin0.abs() <= 1.0)]
                tot = int(s.n_off.sum())
                o[L] = (len(s), int(s.flips.sum()) / tot if tot else np.nan)
            P(f"  {cost:>5.0f} {lag:>3} | {o['CAGR'][1]:>17.3f} | {o['DD'][1]:>15.3f} | "
              f"{(o['CAGR'][1]-o['DD'][1])*100:>+8.1f}   (n {o['CAGR'][0]}/{o['DD'][0]})")

    P("\n4b pass counts over all GRID book-calendar cells (MONTHLY-21, FULL):")
    for cost in CGRID:
        for lag in LAGS:
            s = sel(cells, family="MONTHLY21", lag=lag, cost=cost, window="FULL")
            P(f"  {cost:>5.0f}bps lag {lag}: 4b {int(s.keep4b.sum())} / {len(s)} "
              f"({s.keep4b.mean():.1%})   4a {int(s.keep4a.sum())} / {len(s)}")

    # ---------------------------------------------------------------- verdict block
    P("\n" + "=" * 100)
    P("HYPOTHESIS LEDGER")
    P("=" * 100)
    for nm_, v in (("H_RAW", H_RAW), ("H_CONVERGE", H_CONV), ("H_SPREADEQ", H_SPREADEQ),
                   ("H_LOC", H_LOC), ("H_NOFREE", H_NOFREE), ("H_WF", H_WF)):
        P(f"  {nm_:<12} {'CONFIRMED' if v else ('REFUTED' if v is False else 'N/A')}")
    P(f"  gates: G1 {'PASS' if g1 < 1e-9 else 'FAIL'}  G2 {sum(g2ok)}/6  G3 printed  G4 printed")
    P(f"\ntotal runtime {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


# ================================================================== post pass (reads .cells.csv)
def post():
    """Deterministic second pass over the committed .cells.csv - no backtest is re-run.
    It answers the question the flip census raises: WHY do the two level legs behave alike?
    Run as `python3 <this file> post` after the main pass has written its CSVs."""
    log: list[str] = []

    def Q(*a):
        s_ = " ".join(str(x) for x in a)
        print(s_, flush=True)
        log.append(s_)

    c = pd.read_csv(OUT / f"{STAMP}.cells.csv")
    m = c[(c.family == "MONTHLY21") & (c.lag == LAG_MAIN) & (c.cost == COST_MAIN) &
          (c.window == "FULL")]
    k0 = m[m.k == 0]
    Q("THE GROSS DIAL - 4b's two LEVEL legs are one scalar read from two ends")
    Q(f"{'panel':<6}{'form':<9}{'Sharpe sd over 11 rungs':>25}{'d(CAGR margin)/dg':>19}"
      f"{'d(DD margin)/dg':>17}{'corr':>9}{'both legs +':>14}")
    rows = []
    for (pn, fm), g in k0.groupby(["panel", "form"]):
        g = g.sort_values("gross")
        sc = float(np.polyfit(g.gross, g.m_CAGR, 1)[0]) / 20.0     # pp per 5pp of gross
        sd = float(np.polyfit(g.gross, g.m_DD, 1)[0]) / 20.0
        cr = float(np.corrcoef(g.m_CAGR, g.m_DD)[0, 1])
        adm = int(((g.m_CAGR > 0) & (g.m_DD > 0)).sum())
        Q(f"{pn:<6}{fm:<9}{g.Sharpe.std():>25.4f}{sc:>19.3f}{sd:>17.3f}{cr:>9.4f}"
          f"{adm:>9} of 11")
        rows.append(dict(panel=pn, form=fm, sharpe_sd=g.Sharpe.std(), d_cagr_margin=sc,
                         d_dd_margin=sd, corr=cr, admissible=adm))
    lad = pd.DataFrame(rows)
    Q(f"  median Sharpe sd across the whole dial {lad.sharpe_sd.median():.4f}; "
      f"median corr(CAGR margin, DD margin) {lad['corr'].median():+.4f}; "
      f"admissible rungs {int(lad.admissible.sum())} of 110")

    Q("\nCALENDAR ROBUSTNESS of every GRID book (4b passes over the 21 monthly offsets)")
    g2 = m.groupby(["panel", "label"]).keep4b.sum()
    Q(f"  21 of 21: {int((g2 == 21).sum())}   >=19: {int((g2 >= 19).sum())}   "
      f">=11: {int((g2 >= 11).sum())}   0 of 21: {int((g2 == 0).sum())}   (n={len(g2)})")
    for (pn, lbl), v in g2[g2 == 21].items():
        Q(f"  UNANIMOUS: {pn} {lbl}")

    Q("\nTHE LADDER that produces it - U56 TOP20, the record's 2026-09-04 KEEP 4b, by gross")
    t = m[(m.panel == "U56") & (m.form == "TOP20")]
    Q(f"  {'gross':>6}{'4b/21':>7}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>9}"
      f"{'m_CAGR':>9}{'m_DD':>8}   offsets failing CAGR / DD")
    lrows = []
    for lbl, g in t.groupby("label"):
        z = g[g.k == 0].iloc[0]
        fc, fd = int((g.m_CAGR <= 0).sum()), int((g.m_DD <= 0).sum())
        Q(f"  {z.gross:>6.2f}{int(g.keep4b.sum()):>5}/21{z.CAGR:>8.2%}{z.Sharpe:>8.3f}"
          f"{z.MaxDD:>9.2%}{z.m_CAGR:>+9.2f}{z.m_DD:>+8.2f}   {fc:>2} / {fd:<2}")
        lrows.append(dict(panel="U56", form="TOP20", gross=z.gross, pass4b=int(g.keep4b.sum()),
                          CAGR=z.CAGR, Sharpe=z.Sharpe, MaxDD=z.MaxDD, m_CAGR=z.m_CAGR,
                          m_DD=z.m_DD, off_fail_CAGR=fc, off_fail_DD=fd))
    pd.concat([lad.assign(kind="SLOPE"), pd.DataFrame(lrows).assign(kind="LADDER")],
              ignore_index=True).to_csv(OUT / f"{STAMP}.ladder.csv", index=False)
    (OUT / f"{STAMP}.post.txt").write_text("\n".join(log) + "\n")
    print(f"-> {STAMP}.ladder.csv  {STAMP}.post.txt")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "post":
        post()
    else:
        main()
