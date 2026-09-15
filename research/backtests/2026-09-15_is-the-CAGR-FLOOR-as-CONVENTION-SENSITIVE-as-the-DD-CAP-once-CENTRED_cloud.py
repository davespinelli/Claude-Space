#!/usr/bin/env python3
"""Idea 879 (cloud lane, idea 2 of 2, 2026-09-15) - is the CAGR FLOOR as CONVENTION-SENSITIVE
as the DD CAP once its MARGINS are CENTRED?

THE CLAIM UNDER TEST
--------------------
Idea 808 ran PROTOCOL 4b's five legs over a family of rebalance calendars (the same book, its
period-end rebalance moved k trading days later) and found:

    median margin/spread ratio   CAGR 0.877   DD 0.466      (DD is the shakier leg by ratio)
    leg-level offset FLIPS       CAGR 3       DD 52         (DD is 17x shakier by flips)

and diagnosed the gap itself: "CAGR is nearly as bad by ratio and looks innocent only because
most books' CAGR margins sit far from zero."  A flip needs a margin small enough for the
calendar's own spread to cross it.  808's 12 books were not selected to sit near the CAGR floor,
so its flip count measures WHERE THE BOOKS WERE, not how sensitive the leg is.

THE TEST.  Build a book population that is deliberately CENTRED on the CAGR floor and ask
whether the flip count converges on DD's.  Gross is the dial that moves CAGR smoothly through
the floor with the book's construction otherwise untouched, so a gross ladder over each book
form sweeps every form's CAGR margin through zero and produces books at any chosen distance
from the floor.  The same ladder produces books centred on the DD cap, which is the matched
control 808 never had.

PRE-REGISTERED HYPOTHESES (stated before any cell was run)
----------------------------------------------------------
    H_CONVERGE  at |margin| <= band, the CAGR leg's flips-per-book comes within a factor of 2
                of the DD leg's flips-per-book on ITS OWN matched band.  If the legs differ only
                in where their books sit, centring both must equalise them.
    H_RATIO     flips-per-book is a function of |margin|/spread ALONE: once that ratio is known,
                leg identity adds nothing.  Tested as Spearman(ratio, flips) per leg plus the
                two legs' flip rates inside matched ratio buckets.
    H_SPREAD    the residual, if any, is a SPREAD fact: the DD leg's calendar spread is larger
                RELATIVE to its own bar than the CAGR leg's, so at equal margins DD still flips
                more.  This is the one way the legs can genuinely differ after centring.

TWO TUNED PARAMETERS (the queue's own), ALL GRID POINTS REPORTED
---------------------------------------------------------------
    margin band  BANDS = {0.5, 1.0, 2.0} pp    (the queue names 1pp; 0.5 and 2.0 bracket it)
    offset grid  MONTHLY (21 calendars) and WEEKLY (5 calendars), both always reported

Costs 10 bps main with 25 bps reported throughout; next-day fills (lag 1) main with lag 2
reported; no shorting, no leverage.  Deterministic, standalone, no network.

SURVIVORSHIP: U56 and B136 are CURRENT-CONSTITUENT lists, so CAGR and drawdown LEVELS are
optimistic.  The quantity this run reports is a WITHIN-BOOK, WITHIN-LEG comparison of a margin
against its own calendar spread, which is far less exposed to that bias than the levels are.

Outputs: .books.csv  .legs.csv  .bands.csv  .walkforward.csv  .console.txt
Modifies nothing else; RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched (rule 6).
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

STAMP = "2026-09-15_is-the-CAGR-FLOOR-as-CONVENTION-SENSITIVE-as-the-DD-CAP-once-CENTRED_cloud"
OUT = ROOT / "research" / "backtests"

COST_MAIN, LAG_MAIN = 10.0, 1
CGRID, LAGS = [10.0, 25.0], [1, 2]
FAMILY = {"MONTHLY": ("M", list(range(21))), "WEEKLY": ("W", list(range(5)))}
BANDS = [0.5, 1.0, 2.0]
FAR_PP = 4.0
GROSSES = [round(0.30 + 0.10 * i, 2) for i in range(13)]          # 0.30 .. 1.50
IS_END, OOS_START = "2016-12-31", "2017-01-01"
MA_WIN, WARMUP, MAX_VOL = 200, 260, 0.60
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]

PUB_808 = dict(ratio_CAGR=0.877, ratio_DD=0.466, flips_CAGR=3, flips_DD=52)

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ book forms (808's, verbatim)
def _elig(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ma_dg_weights(px, g):
    pm = px.notna()
    ma = (px > px.rolling(MA_WIN).mean()) & pm
    cnt = pm.sum(axis=1).replace(0, np.nan)
    return (g * pm.div(cnt, axis=0).fillna(0.0)).where(ma, 0.0)


def top_n_weights(px, n, g):
    s = score(px, vol_scale=False)[0]
    rank = s.where(_elig(px)).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (g / n)


def ew_elig_weights(px, g):
    e = _elig(px).astype(float)
    cnt = e.sum(axis=1).replace(0, np.nan)
    return (g * e.div(cnt, axis=0)).fillna(0.0)


FORMS = {
    "MADG": lambda px, g: ma_dg_weights(px, g),
    "TOP20": lambda px, g: top_n_weights(px, 20, g),
    "TOP40": lambda px, g: top_n_weights(px, 40, g),
    "EWELIG": lambda px, g: ew_elig_weights(px, g),
    "BAND3": lambda px, g: rules_v2_weights(px, band=0.03, gross=g),
}
# 808's own twelve books (6 forms x 2 panels), for the G3 reproduction of its published numbers
BOOKS_808 = [("MADG", 1.00), ("MADG", 0.75), ("TOP20", 0.75), ("TOP40", 1.00),
             ("EWELIG", 0.75), ("BAND3", 0.75)]


def shifted_mask(idx, freq, k):
    m = rebalance_mask(idx, freq).values
    if k == 0:
        return pd.Series(m, index=idx)
    pos = np.flatnonzero(m) + k
    pos = pos[pos < len(idx)]
    out = np.zeros(len(idx), dtype=bool)
    out[pos] = True
    return pd.Series(out, index=idx)


def fast_run(prices, weights, mask, lag):
    """808's vectorised runner: (gross return path before costs, turnover path, realised gross).
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


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def margins(r, spy):
    """PROTOCOL 4b's five legs as MARGINS in their own units, FULL window (808's convention)."""
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    return {"H1": a1 - s1, "H2": a2 - s2,
            "OOS": metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"],
            "DD": (m["MaxDD"] - 0.60 * ms["MaxDD"]) * 100.0,
            "CAGR": (m["CAGR"] - 0.70 * ms["CAGR"]) * 100.0,
            "_CAGR": m["CAGR"], "_Sharpe": m["Sharpe"], "_MaxDD": m["MaxDD"]}


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    if len(a) < 3 or a.nunique() < 2 or b.nunique() < 2:
        return float("nan")
    return float(a.rank().corr(b.rank()))


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


# ================================================================== run
def main():
    t0 = time.time()
    P(f"# {STAMP}")
    P(f"# pandas {pd.__version__} numpy {np.__version__}")
    P("# idea 879, cloud lane, idea 2 of 2.  PROTOCOL: 10 bps, next-day, no shorting/leverage.")
    P(f"# tuned params: margin band {BANDS} pp x offset grid {list(FAMILY)}; "
      f"costs {CGRID} and lags {LAGS} always reported.")

    panels = {"U56": load_universe().dropna(how="all").ffill(),
              "B136": load_universe(broad=True).dropna(how="all").ffill()}
    ctx = {}
    for nm, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base = backtest(px, rules_v2_weights(px), cost_bps=COST_MAIN, freq="W")["returns"].loc[start:]
        ctx[nm] = dict(px=px, start=start, spy=spy, base=base)
        ms = metrics(spy)
        P(f"PANEL {nm}: {px.shape[1]} names x {len(px)} days, {px.index[0].date()}..{px.index[-1].date()}"
          f"  window {start.date()}..  SPY CAGR {ms['CAGR']:.2%} MaxDD {ms['MaxDD']:.2%}"
          f"  -> 4b bars: CAGR floor {0.70*ms['CAGR']:.2%}, DD cap {0.60*ms['MaxDD']:.2%}")
    P("SURVIVORSHIP: both panels are current-constituent lists; LEVELS are optimistic. The "
      "reported quantity is a within-book margin against its own calendar spread.")

    # ---------------------------------------------------------------- G1 engine gate
    c = ctx["U56"]
    w = FORMS["MADG"](c["px"], 1.00)
    rg, tn, _ = fast_run(c["px"], w, shifted_mask(c["px"].index, "M", 0), LAG_MAIN)
    r_fast = (rg - tn * COST_MAIN / 1e4).loc[c["start"]:]
    r_eng = backtest(c["px"], w, cost_bps=COST_MAIN, freq="M")["returns"].loc[c["start"]:]
    g1 = float(np.nanmax(np.abs(r_fast.values - r_eng.values)))
    P(f"\nG1 engine   max|fast_run - engine.backtest| = {g1:.3e}   bar 1e-9   "
      f"{'PASS' if g1 < 1e-9 else 'FAIL'}")

    # ---------------------------------------------------------------- stage A: the ladder
    P("\n" + "=" * 100)
    P("STAGE A  SWEEP GROSS AND FIND WHERE EACH BOOK FORM CROSSES THE 4b CAGR FLOOR")
    P("=" * 100)
    rows = []
    for pn, c in ctx.items():
        px, start, spy = c["px"], c["start"], c["spy"]
        mk0 = shifted_mask(px.index, "M", 0)
        for fm, fn in FORMS.items():
            for g in GROSSES:
                rg, tn, gr = fast_run(px, fn(px, g), mk0, LAG_MAIN)
                r = (rg - tn * COST_MAIN / 1e4).loc[start:]
                mg = margins(r, spy)
                rows.append(dict(panel=pn, form=fm, gross=g,
                                 CAGR=mg["_CAGR"], Sharpe=mg["_Sharpe"], MaxDD=mg["_MaxDD"],
                                 realised_gross=float(gr.loc[start:].mean()),
                                 **{f"m_{L}": mg[L] for L in LEGS}))
    books = pd.DataFrame(rows)
    P(f"ladder: {len(books)} books ({len(panels)} panels x {len(FORMS)} forms x {len(GROSSES)} grosses)"
      f"   ({time.time()-t0:.0f}s)")
    P("\nevery ladder point (CAGR and DD margins in pp; m_CAGR > 0 clears the floor):")
    P(books[["panel", "form", "gross", "realised_gross", "CAGR", "Sharpe", "MaxDD",
             "m_CAGR", "m_DD", "m_H1", "m_H2", "m_OOS"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\nCAGR-floor crossing by form (the gross at which m_CAGR changes sign):")
    for (pn, fm), g in books.groupby(["panel", "form"], sort=False):
        g = g.sort_values("gross")
        sgn = np.sign(g.m_CAGR.values)
        cross = [f"{g.gross.values[i]:.2f}->{g.gross.values[i+1]:.2f}"
                 for i in range(len(g) - 1) if sgn[i] != sgn[i + 1]]
        P(f"  {pn:>5} {fm:<7} m_CAGR {g.m_CAGR.min():+7.2f} .. {g.m_CAGR.max():+7.2f} pp   "
          f"crossing {cross if cross else 'NONE IN LADDER'}")

    # ---------------------------------------------------------------- stage B: the offset family
    P("\n" + "=" * 100)
    P("STAGE B  RUN THE FULL OFFSET FAMILY ON THE CENTRED BOOKS AND THEIR CONTROLS")
    P("=" * 100)
    maxband = max(BANDS)
    sel = books[(books.m_CAGR.abs() <= maxband) | (books.m_DD.abs() <= maxband)
                | (books.m_CAGR.abs() > FAR_PP)].copy()
    # cap the FAR control so it does not swamp the run: 808's own 12 books plus the ladder's
    # far points, thinned to every third gross (pre-registered, not chosen on an outcome)
    far = sel[sel.m_CAGR.abs() > FAR_PP]
    near = sel[sel.m_CAGR.abs() <= maxband]
    nearDD = sel[(sel.m_DD.abs() <= maxband) & (sel.m_CAGR.abs() > maxband)]
    far = far[far.gross.isin(GROSSES[::3])]
    sel = pd.concat([near, nearDD, far]).drop_duplicates(subset=["panel", "form", "gross"])
    P(f"selected {len(sel)} books: CAGR-centred {len(near)}, DD-centred (and not CAGR-centred) "
      f"{len(nearDD)}, FAR control {len(far)} (|m_CAGR| > {FAR_PP}pp, every third gross)")

    cells = []
    for _, bk in sel.iterrows():
        c = ctx[bk.panel]
        px, start, spy, base = c["px"], c["start"], c["spy"], c["base"]
        wts = FORMS[bk.form](px, bk.gross)
        for fam, (freq, offs) in FAMILY.items():
            for k in offs:
                mk = shifted_mask(px.index, freq, k)
                for lag in LAGS:
                    rg, tn, gr = fast_run(px, wts, mk, lag)
                    rg, tn = rg.loc[start:], tn.loc[start:]
                    for cost in CGRID:
                        r = rg - tn * cost / 1e4
                        mg = margins(r, spy)
                        cells.append(dict(panel=bk.panel, form=bk.form, gross=bk.gross,
                                          family=fam, k=k, lag=lag, cost=cost,
                                          CAGR=mg["_CAGR"], Sharpe=mg["_Sharpe"], MaxDD=mg["_MaxDD"],
                                          **{f"m_{L}": mg[L] for L in LEGS},
                                          pass4b=bool(all(mg[L] > 0 for L in LEGS)),
                                          pass4a=keep_4a(r, base)))
    cells = pd.DataFrame(cells)
    P(f"cells: {len(cells)} rows   ({time.time()-t0:.0f}s)")

    # ---------------------------------------------------------------- per-leg spreads and flips
    leg_rows = []
    for (pn, fm, g, fam, lag, cost), grp in cells.groupby(
            ["panel", "form", "gross", "family", "lag", "cost"], sort=False):
        g0 = grp[grp.k == 0].iloc[0]
        for L in LEGS:
            v = grp[f"m_{L}"].values
            m0 = float(g0[f"m_{L}"])
            sp = float(v.max() - v.min())
            sd = float(v.std(ddof=1)) if len(v) > 1 else 0.0
            leg_rows.append(dict(panel=pn, form=fm, gross=g, family=fam, lag=lag, cost=cost, leg=L,
                                 margin0=m0, absmargin0=abs(m0), spread=sp, sd=sd,
                                 ratio_spread=abs(m0) / sp if sp > 0 else np.inf,
                                 pass0=bool(m0 > 0), n_pass=int((v > 0).sum()), n_off=len(v),
                                 flips=int((np.sign(v) != np.sign(m0)).sum())))
    legs = pd.DataFrame(leg_rows)
    main_sel = (legs.lag == LAG_MAIN) & (legs.cost == COST_MAIN)

    # ---------------------------------------------------------------- G3 reproduce 808
    P("\n" + "=" * 100)
    P("G3  REPRODUCE IDEA 808's UNMATCHED RESULT ON ITS OWN TWELVE BOOKS")
    P("=" * 100)
    is808 = legs.apply(lambda r: (r.form, round(float(r.gross), 2)) in set(BOOKS_808), axis=1)
    k808 = legs[main_sel & (legs.family == "MONTHLY") & is808]
    nb = k808.groupby("leg").size().max() if len(k808) else 0
    P(f"808's book set present in this run's selection: {int(nb)} of 12 books "
      f"(a ladder point is only run if it fell in a band or the FAR control)")
    if len(k808):
        t = k808.groupby("leg").agg(median_ratio=("ratio_spread", "median"),
                                    total_flips=("flips", "sum"),
                                    median_absmargin=("absmargin0", "median"),
                                    mean_spread=("spread", "mean")).reindex(LEGS)
        P(t.to_string(float_format=lambda x: f"{x:.3f}"))
        P(f"  808 published median margin/spread CAGR {PUB_808['ratio_CAGR']}, DD {PUB_808['ratio_DD']};"
          f" flips CAGR {PUB_808['flips_CAGR']}, DD {PUB_808['flips_DD']} over its full 12-book set.")
        P("  This run's subset is not 808's population (it is the part of 808's books that fell "
          "inside a band or the FAR control), so the numbers are reported as a DIRECTION check, "
          "not an equality bar: the ORDERING (DD flips > CAGR flips, DD ratio < CAGR ratio) is "
          "what must hold.")
        ok = (t.loc["DD", "total_flips"] > t.loc["CAGR", "total_flips"]) and \
             (t.loc["DD", "median_ratio"] < t.loc["CAGR", "median_ratio"])
        P(f"  ORDERING on 808's books: {'REPRODUCED' if ok else 'NOT REPRODUCED'}")

    # ---------------------------------------------------------------- THE ANSWER
    P("\n" + "=" * 100)
    P("THE ANSWER  FLIPS AT MATCHED |MARGIN| (H_CONVERGE), every band x offset grid printed")
    P("=" * 100)
    band_rows = []
    for fam in FAMILY:
        for band in BANDS:
            for lag in LAGS:
                for cost in CGRID:
                    s = legs[(legs.family == fam) & (legs.lag == lag) & (legs.cost == cost)]
                    cg = s[(s.leg == "CAGR") & (s.absmargin0 <= band)]
                    dd = s[(s.leg == "DD") & (s.absmargin0 <= band)]
                    far_cg = s[(s.leg == "CAGR") & (s.absmargin0 > FAR_PP)]
                    row = dict(family=fam, band=band, lag=lag, cost=cost,
                               n_CAGR=len(cg), flips_CAGR=int(cg.flips.sum()),
                               fpb_CAGR=float(cg.flips.mean()) if len(cg) else np.nan,
                               ratio_CAGR=float(cg.ratio_spread.median()) if len(cg) else np.nan,
                               spread_CAGR=float(cg.spread.median()) if len(cg) else np.nan,
                               n_DD=len(dd), flips_DD=int(dd.flips.sum()),
                               fpb_DD=float(dd.flips.mean()) if len(dd) else np.nan,
                               ratio_DD=float(dd.ratio_spread.median()) if len(dd) else np.nan,
                               spread_DD=float(dd.spread.median()) if len(dd) else np.nan,
                               n_CAGR_far=len(far_cg),
                               fpb_CAGR_far=float(far_cg.flips.mean()) if len(far_cg) else np.nan)
                    row["fpb_ratio_DD_over_CAGR"] = (row["fpb_DD"] / row["fpb_CAGR"]
                                                     if row["fpb_CAGR"] else np.nan)
                    band_rows.append(row)
    bands = pd.DataFrame(band_rows)
    P(bands.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # -------- the same table restricted to UNLEVERAGED books (PROTOCOL rule 2)
    P("\nGROSS > 1.00 IS LEVERAGE, WHICH PROTOCOL RULE 2 FORBIDS UNLESS THE IDEA ASKS FOR IT.")
    P("Idea 879 does not.  The gross ladder is a METHOD for sliding a book's margin through a 4b")
    P("bar, so leveraged rungs are admitted as ladder points and NEVER as capital candidates.")
    P("The whole H_CONVERGE table restricted to gross <= 1.00, so the answer does not rest on them:")
    unlev = legs[legs.gross <= 1.0]
    ul_rows = []
    for fam in FAMILY:
        for band in BANDS:
            s = unlev[(unlev.family == fam) & (unlev.lag == LAG_MAIN) & (unlev.cost == COST_MAIN)]
            cg = s[(s.leg == "CAGR") & (s.absmargin0 <= band)]
            dd = s[(s.leg == "DD") & (s.absmargin0 <= band)]
            fc = s[(s.leg == "CAGR") & (s.absmargin0 > FAR_PP)]
            ul_rows.append(dict(family=fam, band=band, n_CAGR=len(cg),
                                fpb_CAGR=float(cg.flips.mean()) if len(cg) else np.nan,
                                n_DD=len(dd), fpb_DD=float(dd.flips.mean()) if len(dd) else np.nan,
                                ratio=(float(dd.flips.mean()) / float(cg.flips.mean())
                                       if len(cg) and len(dd) and cg.flips.mean() else np.nan),
                                n_CAGR_far=len(fc),
                                fpb_CAGR_far=float(fc.flips.mean()) if len(fc) else np.nan))
    P(pd.DataFrame(ul_rows).to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    m = bands[(bands.lag == LAG_MAIN) & (bands.cost == COST_MAIN) & (bands.band == 1.0)
              & (bands.family == "MONTHLY")]
    if len(m):
        r0 = m.iloc[0]
        conv = (np.isfinite(r0.fpb_ratio_DD_over_CAGR)
                and 0.5 <= r0.fpb_ratio_DD_over_CAGR <= 2.0)
        P(f"\nH_CONVERGE at the queue's own band (1.0pp, MONTHLY, 10bps, lag 1): "
          f"CAGR {r0.fpb_CAGR:.2f} flips/book over {int(r0.n_CAGR)} books, "
          f"DD {r0.fpb_DD:.2f} over {int(r0.n_DD)}, ratio {r0.fpb_ratio_DD_over_CAGR:.2f} "
          f"-> {'CONFIRMED' if conv else 'REFUTED'} (bar: ratio in [0.5, 2.0])")
        P(f"  and the SAME leg uncentred: CAGR {r0.fpb_CAGR_far:.2f} flips/book over "
          f"{int(r0.n_CAGR_far)} books at |margin| > {FAR_PP}pp — this is the quantity 808 "
          f"measured as 3 flips over 12 books.")

    # ---------------------------------------------------------------- H_RATIO / H_SPREAD
    P("\n" + "=" * 100)
    P("H_RATIO  IS THE FLIP COUNT A FUNCTION OF |MARGIN|/SPREAD ALONE?")
    P("=" * 100)
    for fam in FAMILY:
        s = legs[(legs.family == fam) & (legs.lag == LAG_MAIN) & (legs.cost == COST_MAIN)
                 & legs.leg.isin(["CAGR", "DD"]) & np.isfinite(legs.ratio_spread)]
        P(f"\n{fam}:")
        for L in ["CAGR", "DD"]:
            x = s[s.leg == L]
            P(f"  {L:<5} n {len(x):>3}  Spearman(|margin|/spread, flips) = "
              f"{spearman(x.ratio_spread, x.flips):+.3f}   median spread {x.spread.median():.3f}pp")
        P("  flip rate inside matched |margin|/spread buckets (the H_RATIO test):")
        edges = [0.0, 0.25, 0.5, 1.0, 2.0, np.inf]
        for lo, hi in zip(edges[:-1], edges[1:]):
            line = f"    ratio [{lo:.2f}, {hi if np.isfinite(hi) else 'inf'}) :"
            for L in ["CAGR", "DD"]:
                x = s[(s.leg == L) & (s.ratio_spread >= lo) & (s.ratio_spread < hi)]
                line += (f"  {L} n={len(x):>3} flips/book "
                         f"{(x.flips.mean() if len(x) else float('nan')):6.2f}")
            P(line)

    P("\n" + "=" * 100)
    P("H_SPREAD  IS THE RESIDUAL A SPREAD FACT?")
    P("=" * 100)
    s = legs[main_sel & (legs.family == "MONTHLY")]
    t = s.groupby("leg").agg(median_spread=("spread", "median"), median_sd=("sd", "median"),
                             median_absmargin=("absmargin0", "median"),
                             median_ratio=("ratio_spread", "median"),
                             flips=("flips", "sum"), n=("flips", "size")).reindex(LEGS)
    P(t.to_string(float_format=lambda x: f"{x:.3f}"))
    sp_cg = float(s[s.leg == "CAGR"].spread.median())
    sp_dd = float(s[s.leg == "DD"].spread.median())
    P(f"\n  median 21-calendar spread: CAGR {sp_cg:.3f}pp, DD {sp_dd:.3f}pp, "
      f"DD/CAGR = {sp_dd/sp_cg if sp_cg else float('nan'):.2f}x")
    P(f"  H_SPREAD {'CONFIRMED' if sp_dd > sp_cg else 'REFUTED'}: the DD leg's calendar spread is "
      f"{'wider' if sp_dd > sp_cg else 'NOT wider'} than the CAGR leg's in the same pp units.")

    # ---------------------------------------------------------------- rule 8
    P("\n" + "=" * 100)
    P("RULE 8 ON THE BOOKS  (IS-only selector on 2009-2016, OOS 2017-2026 read once)")
    P("=" * 100)
    wf = []
    for pn, c in ctx.items():
        px, start, spy, base = c["px"], c["start"], c["spy"], c["base"]
        ms, mb = metrics(spy), metrics(base)
        s1, s2 = halves(spy)
        b1, b2 = halves(base)
        mk0 = shifted_mask(px.index, "M", 0)
        for _, bk in sel.iterrows():
            if bk.panel != pn:
                continue
            rg, tn, _ = fast_run(px, FORMS[bk.form](px, bk.gross), mk0, LAG_MAIN)
            r = (rg - tn * COST_MAIN / 1e4).loc[start:]
            m = metrics(r)
            a1, a2 = halves(r)
            mo, so = metrics(r.loc[OOS_START:]), metrics(spy.loc[OOS_START:])
            wf.append(dict(panel=pn, book=f"{bk.form}-g{bk.gross:.2f}",
                           IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                           CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=a1, H2=a2,
                           OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                           SPY_CAGR=ms["CAGR"], SPY_Sharpe=ms["Sharpe"], SPY_MaxDD=ms["MaxDD"],
                           SPY_OOS_Sharpe=so["Sharpe"], BASE_Sharpe=mb["Sharpe"],
                           BASE_H1=b1, BASE_H2=b2, BASE_MaxDD=mb["MaxDD"],
                           keep4a=keep_4a(r, base),
                           keep4b=bool(a1 > s1 and a2 > s2 and mo["Sharpe"] > so["Sharpe"]
                                       and m["MaxDD"] >= 0.60 * ms["MaxDD"]
                                       and m["CAGR"] >= 0.70 * ms["CAGR"])))
    wfd = pd.DataFrame(wf)
    P(f"\nevery selected book, MONTHLY k=0, 10bps, lag 1 ({len(wfd)} grid points):")
    P(wfd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\nIS-ONLY PICK PER PANEL (highest 2009-2016 Sharpe), OOS read once.")
    P("PROTOCOL rule 2 forbids leverage, so the pick is taken over UNLEVERAGED books "
      "(gross <= 1.00); the leveraged argmax is printed beside it and is NOT a candidate.")
    wfd["gross"] = wfd.book.str.split("-g").str[-1].astype(float)
    for pn in ctx:
        sub = wfd[(wfd.panel == pn) & (wfd.gross <= 1.0)]
        lev = wfd[(wfd.panel == pn) & (wfd.gross > 1.0)]
        if len(lev):
            pl = lev.loc[lev.IS_Sharpe.idxmax()]
            P(f"  {pn:>5} LEVERAGED argmax (NOT a candidate, gross {pl.gross:.2f}) "
              f"{pl.book:<14} FULL {pl.CAGR:7.2%} / {pl.Sharpe:5.3f} / {pl.MaxDD:7.2%}  "
              f"OOS {pl.OOS_CAGR:7.2%} / {pl.OOS_Sharpe:5.3f}   "
              f"4a {'PASS' if pl.keep4a else 'fail'}  4b {'PASS' if pl.keep4b else 'fail'}")
        pk = sub.loc[sub.IS_Sharpe.idxmax()]
        P(f"  {pn:>5} pick {pk.book:<14} FULL {pk.CAGR:7.2%} / {pk.Sharpe:5.3f} / {pk.MaxDD:7.2%}"
          f"  H {pk.H1:5.3f}/{pk.H2:5.3f}   OOS {pk.OOS_CAGR:7.2%} / {pk.OOS_Sharpe:5.3f} / "
          f"{pk.OOS_MaxDD:7.2%}   4a {'PASS' if pk.keep4a else 'fail'}  "
          f"4b {'PASS' if pk.keep4b else 'fail'}")
        P(f"        SPY {pk.SPY_CAGR:7.2%} / {pk.SPY_Sharpe:5.3f} / {pk.SPY_MaxDD:7.2%} "
          f"(OOS Sharpe {pk.SPY_OOS_Sharpe:5.3f})   RULES v2 base Sharpe {pk.BASE_Sharpe:5.3f} "
          f"(H {pk.BASE_H1:5.3f}/{pk.BASE_H2:5.3f}, MaxDD {pk.BASE_MaxDD:7.2%})")
    ul = wfd[wfd.gross <= 1.0]
    P(f"\nunselected base rate over all {len(wfd)} grid points: "
      f"4a {int(wfd.keep4a.sum())} ({wfd.keep4a.mean():.1%}), "
      f"4b {int(wfd.keep4b.sum())} ({wfd.keep4b.mean():.1%}); "
      f"over the {len(ul)} UNLEVERAGED points: 4a {int(ul.keep4a.sum())} ({ul.keep4a.mean():.1%}), "
      f"4b {int(ul.keep4b.sum())} ({ul.keep4b.mean():.1%})")
    P("NOTE: this book population was built by sweeping gross to sit ON the 4b bars, so its 4b "
      "pass rate is a property of the construction and is NOT evidence for any book.")

    books.to_csv(OUT / f"{STAMP}.books.csv", index=False)
    legs.to_csv(OUT / f"{STAMP}.legs.csv", index=False)
    bands.to_csv(OUT / f"{STAMP}.bands.csv", index=False)
    cells.to_csv(OUT / f"{STAMP}.cells.csv", index=False)
    wfd.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    P(f"\nwall {time.time()-t0:.1f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
