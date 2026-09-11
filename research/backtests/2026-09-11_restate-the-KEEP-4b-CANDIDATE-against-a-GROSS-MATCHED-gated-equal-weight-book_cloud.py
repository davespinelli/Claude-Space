#!/usr/bin/env python3
"""
IDEA 672 -- restate-the-KEEP-4b-CANDIDATE-against-a-GROSS-MATCHED-gated-equal-weight-book
==========================================================================================

THE QUEUE'S QUESTION (verbatim intent)
--------------------------------------
  Idea 504 found the 2026-09-04 candidate's edge over its own eligible-equal-weight control is
  99% EXPOSURE (SELECTION -0.0007 vs EXPOSURE +0.0594 median Sharpe on U56 at 10 bps), i.e.
  ranking 20 names out of the eligible set earns CAGR and pays 1.69 pp of drawdown for it
  without earning Sharpe.  Run the candidate head-to-head against a gated equal-weight book at
  identical daily gross on the FULL panels (not draws), both KEEP paths and rule 8, and put the
  simpler book to the Sunday review if it is not worse.  Max 2 params (gross convention, panel).

WHAT IS AT STAKE
----------------
  Idea 504's result is a DRAW-LEVEL median over 40-name sub-panels.  The standing KEEP-4b
  candidate is a FULL-PANEL book.  A median over sub-panels is not the book; if the ranking
  clause is decoration on the real panel too, the live recommendation should be the simpler
  book (hold every eligible name) and the record should say so in RULES wording.  This run is
  the full-panel head-to-head that decision needs.

DESIGN
------
  BOOKS (all through the SAME gate: above the 200d MA and vol20 < 0.60, composite score with
  NO vol scaler, weekly cadence, 10 bps -- the incumbent's own construction, pinned by G3):
    CAND20    top-20 of the panel by composite at a FIXED 0.75/20 per name.  Below 20 eligible
              names it de-grosses to cash; that is the incumbent's convention (G3), and it is
              why the record's usual EW-all comparand is NOT gross-matched to it.
    EWmatched EVERY eligible name, equal weight, at CAND20's OWN realised gross that day.
              Exactly matched day by day (G4b) -> the difference is SELECTION and nothing else.
    EWfixIS   EVERY eligible name, equal weight, at a CONSTANT gross equal to CAND20's mean
              realised gross over the IS half (2009-2016) ONLY.  A tradeable convention: one
              number, fixed before the OOS window, no daily peeking at the ranked book.
    EWfull    EVERY eligible name at a full gross of 0.75 whenever any name is eligible -- the
              record's standard EW-all control, carried so the EXPOSURE leg stays visible.
  TUNED (2) GROSS CONVENTION (matched / fixIS / full) x PANEL (U56 / B136 / SMALL439).
            ALL 3 x 3 = 9 control points are reported, beside the 3 CAND20 points.
  FIXED     n=20, gross 0.75, band gate as above, cadence W, warm-up 260 rows, cost 10 bps
            (PROTOCOL rule 2), IS/OOS split 2016-12-31 / 2017-01-01 (PROTOCOL rule 8).
            None of these was chosen by outcome.
  COST      10 bps is the binding rung for every verdict in this run.  A 0/25 bps appendix is
            printed and written as a LABELLED ROBUSTNESS table; no verdict is taken from it and
            it is not a third tuned axis.

  RULE 8    The chooser picks ONE book per panel by IS (through 2016-12-31) Sharpe and the
            pick is scored on 2017-2026 untouched, against SPY OOS and live RULES v2 OOS.
            A blind-commit column (commit to each book with no chooser) is reported beside it.

PRE-REGISTERED GATES (printed before any new number is read)
------------------------------------------------------------
  G1  fast_backtest == engine.backtest @10 bps                                   bar 1e-12
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                         bar 0.0
  G3  the standing 2026-09-04 KEEP-4b incumbent re-derived on the FULL U56 panel:
      top-20 equal weight, no vol scaler, published 12.66% / 1.0921 / -18.31%    bar 5e-3
  G4a EWfull holds exactly gross 0.75 on every day with an eligible name
  G4b EWmatched's realised daily gross == CAND20's, every day                    bar 1e-12
  G5  SMALL439: every ticker with max_1d_move >= 1.0 in data/small_meta.csv dropped first
  G6  EWfixIS's constant gross is computed from IS rows only (no OOS row touched)

SURVIVORSHIP (PROTOCOL 9)
-------------------------
  B136 is today's constituents and SMALL439 is the current sub-$2B screen only (see
  data/SMALL_PANEL_README.md): names that were acquired, delisted or grew out of the screen are
  absent, so every LEVEL on those two panels is biased upward and none of them is a tradeable
  estimate.  U56 carries the same bias in milder form.  The comparison this run is built on is
  a WITHIN-PANEL difference (CAND20 minus its own gross-matched control over the same names and
  days), which the same bias applies to on both sides and therefore largely differences out.
"""
import sys, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score        # noqa: E402
from engine import backtest, rebalance_mask                                    # noqa: E402

COST0 = 10.0                      # PROTOCOL rule 2 -- the only rung any verdict is taken at
COSTS_APPENDIX = [0.0, 25.0]      # labelled robustness only
FREQ = "W"
BAND0, GROSS0 = 0.03, 0.75
NCAND = 20
VOLCAP = 0.60
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
CONVENTIONS = ["matched", "fixIS", "full"]

KEEP4B_INCUMBENT = dict(CAGR=0.1266, Sharpe=1.0921, MaxDD=-0.1831)

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ------------------------------------------------------------------------------------------
def fast_backtest(prices, weights, freq=FREQ, cost=COST0):
    """Vectorised equivalent of engine.backtest's return stream (G1 pins it at 1e-12)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
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
    return pd.Series((held * rets).sum(axis=1) - turn * cost / 1e4, index=idx)


def M0(r):
    v = r.std() * np.sqrt(252)
    return (r.mean() * 252) / v if v else np.nan


def M(r):
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    vol = r.std() * np.sqrt(252)
    dd = (eq / eq.cummax() - 1).min()
    h = len(r) // 2
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan,
                Sharpe=(r.mean() * 252) / vol if vol else np.nan, MaxDD=dd,
                H1=M0(r.iloc[:h]), H2=M0(r.iloc[h:]))


def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, gross):
    return ew_gross(px, gross).where(band_state(px, band) & px.notna(), 0.0)


def ranked_w(sc, elig, n, gross):
    """Top-n by composite among eligible names at a FIXED gross/n per name (the incumbent)."""
    r = sc.where(elig).rank(axis=1, ascending=False)
    return (r <= n).astype(float) * (gross / n)


def ew_book(elig, gross_series):
    """Every eligible name, equal weight, at the gross given per day."""
    sel = elig.astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.mul(pd.Series(gross_series, index=elig.index) / k, axis=0).fillna(0.0)


def keeppaths(m, oos_s, mb, ms, spy_oos):
    """PROTOCOL rule 4.  4a: Sharpe > live book in BOTH halves and MaxDD no worse.
       4b: Sharpe > SPY in both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    p4a = (m["H1"] > mb["H1"]) and (m["H2"] > mb["H2"]) and (m["MaxDD"] >= mb["MaxDD"])
    p4b = ((m["H1"] > ms["H1"]) and (m["H2"] > ms["H2"]) and (oos_s > spy_oos)
           and (abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]))
           and (m["CAGR"] >= 0.70 * ms["CAGR"]))
    return bool(p4a), bool(p4b)


def fail4b(m, oos_s, ms, spy_oos):
    f = []
    if not m["H1"] > ms["H1"]: f.append("H1")
    if not m["H2"] > ms["H2"]: f.append("H2")
    if not oos_s > spy_oos: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return "+".join(f) if f else "-"


# ------------------------------------------------------------------------------------------
def load_panels():
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in sm.columns if c == "SPY" or c not in bad]
    panels["SMALL439"] = sm[keep]
    return panels, len(sm.columns) - len(keep)


def build_books(px):
    """The four books on the FULL panel, plus the diagnostics the gates need."""
    sc, above, vol20 = score(px, vol_scale=False)
    tr = list(px.columns)                    # baseline ranks SPY with the rest (G3 pins it)
    elig = above[tr] & (vol20[tr] < VOLCAP)
    cand = ranked_w(sc[tr], elig, NCAND, GROSS0)
    g_cand = cand.sum(axis=1)
    g_fix = float(g_cand.loc[px.index[WARM]:IS_END].mean())     # IS rows only (G6)
    books = {
        "CAND20": cand,
        "EWmatched": ew_book(elig, g_cand.values),
        "EWfixIS": ew_book(elig, np.full(len(px), g_fix)),
        "EWfull": ew_book(elig, np.where(elig.any(axis=1).values, GROSS0, 0.0)),
    }
    return books, elig, g_cand, g_fix


def gates(panels, n_dropped):
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- run before any new number is read")
    P("=" * 100)
    ok = True
    px = panels["U56"]
    w = band_book(px, BAND0, GROSS0)
    g2 = float(np.abs(w.values - rules_v2_weights(px, BAND0, GROSS0).values).max())
    P(f"  G2 band_book(0.03,0.75) == rules_v2_weights            : {g2:.3e}  "
      f"{'PASS' if g2 == 0.0 else 'FAIL'}")
    ok &= g2 == 0.0

    slow = backtest(px, w, cost_bps=COST0, freq=FREQ)["returns"]
    fast = fast_backtest(px, w, FREQ, COST0)
    j = px.index[WARM]
    g1 = float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max())
    P(f"  G1 fast_backtest == engine.backtest @10 bps            : {g1:.3e}  "
      f"{'PASS' if g1 < 1e-12 else 'FAIL'}")
    ok &= g1 < 1e-12

    books, elig, g_cand, g_fix = build_books(px)
    m = M(fast_backtest(px, books["CAND20"], FREQ, COST0).loc[j:])
    d = {k: abs(m[k] - v) for k, v in KEEP4B_INCUMBENT.items()}
    P("  G3 2026-09-04 KEEP-4b incumbent (U56 top-20 EW, no vol scaler) re-derived:")
    P(f"     got {m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%}   published "
      f"{KEEP4B_INCUMBENT['CAGR']:.2%} / {KEEP4B_INCUMBENT['Sharpe']:.4f} / "
      f"{KEEP4B_INCUMBENT['MaxDD']:.2%}   max|d| {max(d.values()):.3e}  "
      f"{'PASS' if max(d.values()) < 5e-3 else 'FAIL'}")
    ok &= max(d.values()) < 5e-3

    any_el = elig.any(axis=1)
    g4a = float(np.abs(books["EWfull"].sum(axis=1)[any_el] - GROSS0).max())
    g4b = float(np.abs(books["EWmatched"].sum(axis=1) - g_cand).max())
    P(f"  G4a EWfull holds exactly gross 0.75 when any name eligible: {g4a:.3e}  "
      f"{'PASS' if g4a < 1e-12 else 'FAIL'}")
    P(f"  G4b EWmatched gross == CAND20 gross, every day          : {g4b:.3e}  "
      f"{'PASS' if g4b < 1e-12 else 'FAIL'}")
    ok &= (g4a < 1e-12) and (g4b < 1e-12)

    g6 = float(g_cand.loc[px.index[WARM]:IS_END].mean())
    P(f"  G6 EWfixIS gross from IS rows only: {g_fix:.6f} == {g6:.6f}  "
      f"{'PASS' if abs(g6 - g_fix) < 1e-15 else 'FAIL'}  "
      f"(full-sample mean would be {g_cand.loc[px.index[WARM]:].mean():.6f} -- NOT used)")
    ok &= abs(g6 - g_fix) < 1e-15

    P(f"  G5 SMALL439 dropped {n_dropped} tickers with max_1d_move >= 1.0 : "
      f"{'PASS' if n_dropped > 0 else 'FAIL'}")
    ok &= n_dropped > 0
    P()
    P(f"  GATES: {'ALL PASS' if ok else 'FAILURE -- results below are not trustworthy'}")
    return ok


# ------------------------------------------------------------------------------------------
def run(panels):
    P()
    P("=" * 100)
    P("(B) THE FULL-PANEL HEAD-TO-HEAD -- 3 panels x (CAND20 + 3 gross conventions) @ 10 bps")
    P("=" * 100)
    rows, wf_rows, app_rows = [], [], []
    for pn, px in panels.items():
        start = px.index[WARM]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms, spy_oos = M(spy), M0(spy.loc[OOS_START:])
        spy_o = M(spy.loc[OOS_START:])
        base = fast_backtest(px, rules_v2_weights(px, BAND0, GROSS0), FREQ, COST0).loc[start:]
        mb, base_o = M(base), M(base.loc[OOS_START:])
        books, elig, g_cand, g_fix = build_books(px)
        P()
        P(f"  --- {pn}  ({len(px.columns) - 1} tradable names + SPY, {start.date()} -> "
          f"{px.index[-1].date()}) ---")
        P(f"      SPY            {ms['CAGR']:7.2%} / {ms['Sharpe']:6.3f} / {ms['MaxDD']:7.2%}"
          f"   H1 {ms['H1']:6.3f} H2 {ms['H2']:6.3f}   OOS {spy_o['CAGR']:7.2%} / "
          f"{spy_oos:6.3f} / {spy_o['MaxDD']:7.2%}")
        P(f"      live RULES v2  {mb['CAGR']:7.2%} / {mb['Sharpe']:6.3f} / {mb['MaxDD']:7.2%}"
          f"   H1 {mb['H1']:6.3f} H2 {mb['H2']:6.3f}   OOS {base_o['CAGR']:7.2%} / "
          f"{base_o['Sharpe']:6.3f} / {base_o['MaxDD']:7.2%}")
        P(f"      CAND20 mean realised gross {g_cand.loc[start:].mean():.4f}   "
          f"EWfixIS constant gross (IS only) {g_fix:.4f}   "
          f"mean eligible names {elig.sum(axis=1).loc[start:].mean():.1f}")
        P()
        P("      book        CAGR    Sharpe   MaxDD     H1     H2 |  OOS CAGR  OOS Shp  "
          "OOS DD | 4a  4b  fail4b")
        per = {}
        for bk, wt in books.items():
            r = fast_backtest(px, wt, FREQ, COST0).loc[start:]
            m, mo = M(r), M(r.loc[OOS_START:])
            is_s = M0(r.loc[:IS_END])
            p4a, p4b = keeppaths(m, mo["Sharpe"], mb, ms, spy_oos)
            per[bk] = dict(r=r, m=m, mo=mo, is_s=is_s)
            P(f"      {bk:<10}{m['CAGR']:7.2%} {m['Sharpe']:7.3f} {m['MaxDD']:8.2%} "
              f"{m['H1']:6.3f} {m['H2']:6.3f} | {mo['CAGR']:8.2%} {mo['Sharpe']:8.3f} "
              f"{mo['MaxDD']:7.2%} | {'Y' if p4a else 'n'}   {'Y' if p4b else 'n'}   "
              f"{fail4b(m, mo['Sharpe'], ms, spy_oos)}")
            rows.append(dict(panel=pn, book=bk,
                             convention={"CAND20": "n/a", "EWmatched": "matched",
                                         "EWfixIS": "fixIS", "EWfull": "full"}[bk],
                             cost=COST0, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                             H1=m["H1"], H2=m["H2"], IS_Sharpe=is_s, OOS_CAGR=mo["CAGR"],
                             OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                             keep4a=p4a, keep4b=p4b,
                             fail4b=fail4b(m, mo["Sharpe"], ms, spy_oos),
                             SPY_CAGR=ms["CAGR"], SPY_Sharpe=ms["Sharpe"], SPY_MaxDD=ms["MaxDD"],
                             SPY_OOS_CAGR=spy_o["CAGR"], SPY_OOS_Sharpe=spy_oos,
                             SPY_OOS_MaxDD=spy_o["MaxDD"], v2_Sharpe=mb["Sharpe"],
                             v2_MaxDD=mb["MaxDD"], v2_OOS_Sharpe=base_o["Sharpe"],
                             mean_gross_CAND20=float(g_cand.loc[start:].mean()),
                             gross_fixIS=g_fix))
        # head-to-head deltas, CAND20 minus each control
        P()
        P("      CAND20 minus control (full sample / OOS):")
        for bk in ["EWmatched", "EWfixIS", "EWfull"]:
            a, b = per["CAND20"], per[bk]
            P(f"        vs {bk:<10} dSharpe {a['m']['Sharpe']-b['m']['Sharpe']:+.4f}  "
              f"dCAGR {a['m']['CAGR']-b['m']['CAGR']:+.2%}  "
              f"dMaxDD {a['m']['MaxDD']-b['m']['MaxDD']:+.2%}  |  OOS dSharpe "
              f"{a['mo']['Sharpe']-b['mo']['Sharpe']:+.4f}  dCAGR "
              f"{a['mo']['CAGR']-b['mo']['CAGR']:+.2%}  dMaxDD "
              f"{a['mo']['MaxDD']-b['mo']['MaxDD']:+.2%}")

        # ---- PROTOCOL rule 8: chooser on IS only, scored OOS untouched
        pick = max(per, key=lambda b: per[b]["is_s"])
        for bk in per:
            wf_rows.append(dict(panel=pn, book=bk, IS_Sharpe=per[bk]["is_s"],
                                picked=(bk == pick), OOS_CAGR=per[bk]["mo"]["CAGR"],
                                OOS_Sharpe=per[bk]["mo"]["Sharpe"],
                                OOS_MaxDD=per[bk]["mo"]["MaxDD"],
                                SPY_OOS_CAGR=spy_o["CAGR"], SPY_OOS_Sharpe=spy_oos,
                                SPY_OOS_MaxDD=spy_o["MaxDD"],
                                v2_OOS_CAGR=base_o["CAGR"], v2_OOS_Sharpe=base_o["Sharpe"],
                                v2_OOS_MaxDD=base_o["MaxDD"]))
        mo = per[pick]["mo"]
        is_txt = ", ".join("%s %.3f" % (b, per[b]["is_s"]) for b in per)
        P(f"      RULE 8: IS Sharpe picks {pick} "
          f"({is_txt})  ->  OOS "
          f"{mo['CAGR']:.2%} / {mo['Sharpe']:.3f} / {mo['MaxDD']:.2%}  vs SPY OOS "
          f"{spy_o['CAGR']:.2%} / {spy_oos:.3f} / {spy_o['MaxDD']:.2%}  vs live v2 OOS "
          f"{base_o['CAGR']:.2%} / {base_o['Sharpe']:.3f} / {base_o['MaxDD']:.2%}")

        # ---- labelled cost appendix (NOT a tuned axis, no verdict taken here)
        for c in COSTS_APPENDIX:
            mbc = M(fast_backtest(px, rules_v2_weights(px, BAND0, GROSS0), FREQ, c).loc[start:])
            for bk, wt in books.items():
                r = fast_backtest(px, wt, FREQ, c).loc[start:]
                m, mo2 = M(r), M(r.loc[OOS_START:])
                p4a, p4b = keeppaths(m, mo2["Sharpe"], mbc, ms, spy_oos)
                app_rows.append(dict(panel=pn, book=bk, cost=c, CAGR=m["CAGR"],
                                     Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m["H1"],
                                     H2=m["H2"], OOS_Sharpe=mo2["Sharpe"],
                                     OOS_CAGR=mo2["CAGR"], OOS_MaxDD=mo2["MaxDD"],
                                     keep4a=p4a, keep4b=p4b))
    return pd.DataFrame(rows), pd.DataFrame(wf_rows), pd.DataFrame(app_rows)


def summarise(grid, wf, app):
    P()
    P("=" * 100)
    P("(C) THE ANSWER")
    P("=" * 100)
    piv = grid.pivot_table(index="panel", columns="book",
                           values=["Sharpe", "CAGR", "MaxDD", "OOS_Sharpe"])
    P()
    P("  Head-to-head, CAND20 minus EWmatched (the EXACT gross match -- pure selection):")
    for pn in grid.panel.unique():
        a = grid[(grid.panel == pn) & (grid.book == "CAND20")].iloc[0]
        b = grid[(grid.panel == pn) & (grid.book == "EWmatched")].iloc[0]
        P(f"    {pn:<9} dSharpe {a.Sharpe-b.Sharpe:+.4f}  dCAGR {a.CAGR-b.CAGR:+.2%}  "
          f"dMaxDD {a.MaxDD-b.MaxDD:+.2%}  dOOS_Sharpe {a.OOS_Sharpe-b.OOS_Sharpe:+.4f}  "
          f"dOOS_CAGR {a.OOS_CAGR-b.OOS_CAGR:+.2%}")
    P()
    P("  KEEP paths over the whole 12-point grid @10 bps (PROTOCOL rule 4):")
    P(f"    4a {int(grid.keep4a.sum())}/{len(grid)}   4b {int(grid.keep4b.sum())}/{len(grid)}"
      f"   BOTH {int((grid.keep4a & grid.keep4b).sum())}/{len(grid)}")
    for _, r in grid[grid.keep4b].iterrows():
        P(f"      4b PASS: {r.panel} {r.book}  {r.CAGR:.2%} / {r.Sharpe:.3f} / {r.MaxDD:.2%}"
          f"  OOS {r.OOS_CAGR:.2%} / {r.OOS_Sharpe:.3f} / {r.OOS_MaxDD:.2%}")
    P()
    P("  RULE 8 picks:")
    for _, r in wf[wf.picked].iterrows():
        P(f"    {r.panel:<9} pick {r.book:<10} OOS {r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:6.3f} / "
          f"{r.OOS_MaxDD:7.2%}   SPY OOS {r.SPY_OOS_CAGR:7.2%} / {r.SPY_OOS_Sharpe:6.3f} / "
          f"{r.SPY_OOS_MaxDD:7.2%}   live v2 OOS {r.v2_OOS_CAGR:7.2%} / "
          f"{r.v2_OOS_Sharpe:6.3f} / {r.v2_OOS_MaxDD:7.2%}")
    P()
    P("  COST APPENDIX (labelled robustness, no verdict taken here): 4b passes by rung")
    for c in sorted(app.cost.unique()):
        s = app[app.cost == c]
        P(f"    {c:>5.1f} bps: 4a {int(s.keep4a.sum())}/{len(s)}  4b {int(s.keep4b.sum())}/"
          f"{len(s)}   " + "  ".join(f"{r.panel}/{r.book}" for _, r in s[s.keep4b].iterrows()))
    return piv


def main():
    panels, n_dropped = load_panels()
    ok = gates(panels, n_dropped)
    grid, wf, app = run(panels)
    summarise(grid, wf, app)
    P()
    dump(grid, "grid")
    dump(wf, "walkforward")
    dump(app, "costappendix")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"  wrote {STEM}.console.txt")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
