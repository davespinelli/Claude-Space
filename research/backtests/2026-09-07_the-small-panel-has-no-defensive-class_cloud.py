#!/usr/bin/env python3
"""Idea 136 — "the-small-panel-has-no-defensive-class" (cloud, 2026-09-07).

QUESTION (QUEUE.md).  Idea 133's small panel contributed 0 of 531 `4b-defensive` class members
at any gross level and left 6 of 18 rule-8 cells empty, while u56/broad gave all 531.  Is that
THE PANEL (no book there clears the halves and OOS bars at all) or THE BARS (SPY's own
reference numbers being wrong for a small-cap panel)?  Decompose which of the FOUR NON-FLOOR
bars fails, and how far, on every small-panel arm.  If it is always H1/H2/OOS rather than the
DD cap, the small panel has no defensive books, not a mis-calibrated screen.

DEFINITIONS (ideas 129/133, carried unchanged).  4b has five bars against a reference:
    H1    Sharpe(first half)  > ref H1
    H2    Sharpe(second half) > ref H2
    OOS   Sharpe(2017-2026)   > ref OOS
    DD    MaxDD               <= 60% of |ref MaxDD|          <- the "cap"
    CAGR  CAGR                >= 70% of ref CAGR             <- the "floor"
An arm is `4b-defensive` (a CLASS MEMBER) when it clears the four NON-FLOOR bars and fails
ONLY the CAGR floor.  This run reports every bar's MARGIN in its own units, not just its sign.

THREE THINGS THE QUEUE'S QUESTION NEEDS, all of them run here.

  (a) THE DECOMPOSITION the queue asks for: per-bar failure counts and margins on every
      small-panel arm, beside the same numbers on U56 and B136.

  (b) A WINDOW CONTROL the queue does not ask for but the comparison cannot survive without.
      The small panel starts 2010-01-04, so its evaluation window opens 2011-01-19; idea 133's
      u56/broad rows were read from 2009.  A panel difference measured across two different
      windows is not a panel difference.  EVERY panel is therefore re-read on the COMMON
      window (the small panel's), and that is the primary table; each panel's own full window
      is reported beside it for continuity with idea 133.

  (c) THE BARS-vs-PANEL TEST the queue names as the alternative.  "SPY's reference numbers
      being wrong for a small-cap panel" is directly testable: re-run all five bars against
      IWM (the Russell 2000 ETF, in data/prices.csv, investable and NOT survivorship-screened)
      instead of SPY, and see whether small-panel arms become defensive.  If they do, the
      screen is mis-calibrated for small caps; if they do not, the panel has no defensive
      books.  SPY remains the PROTOCOL reference — IWM is a diagnostic, never a KEEP bar.

CORPUS (census axes; nothing is selected on outcome, all rows go to .grid.csv)
  panels    SMALL439 (the 483-name sub-$2B panel MINUS the 44 tickers with max_1d_move >= 1.0
            in data/small_meta.csv, per the sprint rule), U56 (56), B136 (136)
  books     TOP5 / TOP10 / TOP20 / TOP40 (v1 composite WITHOUT the /sqrt(vol20) term, eligible
            = above the 200d MA and vol20 < 0.60, equal weight at g/k, k = min(n, E_t))
            and EWALL (equal weight over EVERY eligible name at gross g) — the construction
            that supplied idea 129's Pareto-best defensive members
  overlays  CTRL (none), G200 (de-gross to CASH while lagged panel breadth < 0.50),
            VT10 (vol target 0.10: m = min(1, 0.10 / lagged 20d book vol)),
            DD10 (m = 0.50 while the book's own lagged drawdown is worse than -10%)
            — book-level, idea 41's convention verbatim: r = m*r0,
            turn = m*turn0 + |dm|*gross0.shift(1)
  gross     0.53 (idea 129's published mean gross for its defensive members), 0.75 (the live
            rung), 1.00
  costs     10 and 25 bps, plus a 0-bps DIAGNOSTIC rung (never a KEEP rung) so that
            "the panel has no defensive books" can be separated from "costs ate them"
  => 3 x 5 x 4 x 3 x 3 = 540 rows, each scored against BOTH references on BOTH windows.

TUNED PARAMETERS (max 2, PROTOCOL rule 4): (1) the book width n, (2) the gross rung g.
Panel, overlay, cost rung, reference and window are census axes — every level is reported.

RULE 8 WALK-FORWARD.  (n, g) are chosen on 2011-2016 ONLY, within each (panel, overlay, cost)
cell, by four selectors fixed before any OOS number was read, and 2017-2026 is read once:
    S0  argmax IS Sharpe over the cell.
    S1  argmax IS Sharpe among arms passing ALL FIVE IS-window bars.
    S2  the same with the CAGR floor deleted.
    S3  argmax IS Sharpe among arms that are IS-window `4b-defensive` (four non-floor bars
        pass, floor fails) — the selector aimed at the class.  Cells where S3 has NO candidate
        are counted and reported: that is idea 133's "6 of 18 empty cells", re-measured.
OOS CAGR / Sharpe / MaxDD are reported against the arm's own ungated control, RULES v2 (the
live baseline) and SPY.  Both KEEP paths are evaluated on every row: 4a against RULES v2 on
the same panel at the same cost, 4b against SPY.

GATES (asserted / printed in [0] before any new number is read).
  G1  fast_bt == engine.backtest on returns AND turnover at 0 and 25 bps.
  G2  overlay at OFF (m == 1) == the parent, exactly, on r / turnover / gross.
  G3  the SMALL439 drop list is exactly the 44 max_1d_move >= 1.0 tickers, and no dropped
      ticker survives into the traded panel.
  G4  benchmark columns (SPY, IWM) are never tradeable on the small panel, and IWM is never
      tradeable on any panel: max weight on them is 0.
  G5  the bar arithmetic reproduces baseline's own metrics on RULES v2 (CAGR/Sharpe/MaxDD).
  G6  IWM's own reference numbers are printed beside SPY's, so the recalibration test can be
      audited from the console alone.

CAVEATS carried, not buried.
  (1) SURVIVORSHIP, and it is WORSE here than on the large panels.  All three panels are
      current-constituent lists; the small panel is a screen of names that are sub-$2B TODAY
      and have priced continuously since 2010, so every sub-$2B name that was delisted, taken
      under or went to zero is absent.  That inflates the small panel's CAGR and, critically
      for this question, FLATTERS its drawdowns and its halves Sharpes.  A "no defensive
      books" finding measured on a survivorship-inflated panel is therefore a CONSERVATIVE
      finding; a "the bars are mis-calibrated" finding would not be.
  (2) IWM is investable and not survivorship-screened, so the IWM-referenced bars are the
      HARDER test for the small panel, not the easier one — the small panel's own equal-weight
      path would be circular and is not used as a reference.
  (3) The small panel's evaluation window (2011-2026) contains no 2008-2009 bear market, so
      its drawdown cap is measured on a window that cannot express a deep one (idea 128).
  (4) MaxDD is one number off one path.

Deterministic, standalone.  Reads baseline.py only; modifies nothing.
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights, metrics   # noqa: E402
from engine import backtest, rebalance_mask                           # noqa: E402

OUT = Path(__file__).with_suffix("")
SLUG = OUT.name

MAX_VOL = 0.60
VOL_SCALE = False
FREQ = "W"
WARMUP = 260
NS = [5, 10, 20, 40]                 # tuned parameter 1
GROSS = [0.53, 0.75, 1.00]           # tuned parameter 2
COSTS = [0, 10, 25]        # 0 is a DIAGNOSTIC rung only; PROTOCOL binds at 10
OVERLAYS = ["CTRL", "G200", "VT10", "DD10"]
BOOKS = [f"TOP{n}" for n in NS] + ["EWALL"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70      # 4b's delta and phi, unchanged
BREADTH_B = 0.50
VOL_TARGET = 0.10
DD_TRIG = 0.10
BENCH = ["SPY", "IWM"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 900)

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ panels
def small_drop_list():
    m = pd.read_csv(REPO / "data" / "small_meta.csv")
    return sorted(m.loc[m.max_1d_move >= 1.0, "ticker"].astype(str))


def build_panels():
    """(tag, px, tradeable_cols) for each panel; px always carries SPY and IWM."""
    ref = pd.read_csv(REPO / "data" / "prices.csv", index_col=0, parse_dates=True)
    out = []

    drop = small_drop_list()
    sp = load_universe(small=True)
    sp = sp.drop(columns=[c for c in drop if c in sp.columns])
    iwm = ref["IWM"].reindex(sp.index, method="ffill").rename("IWM")
    sp = pd.concat([sp.drop(columns=["IWM"], errors="ignore"), iwm], axis=1).ffill()
    out.append(("SMALL439", sp, [c for c in sp.columns if c not in BENCH], drop))

    for tag, kw in [("U56", {}), ("B136", {"broad": True})]:
        px = load_universe(**kw).dropna(how="all").ffill()
        i2 = ref["IWM"].reindex(px.index, method="ffill").rename("IWM")
        px = pd.concat([px.drop(columns=["IWM"], errors="ignore"), i2], axis=1).ffill()
        # the record's convention on the large panels: SPY IS a constituent; IWM never is.
        out.append((tag, px, [c for c in px.columns if c != "IWM"], []))
    return out


# ------------------------------------------------------------------ books
def eligible_mask(px, cols):
    _, above, vol20 = score(px)
    el = (above & (vol20 < MAX_VOL))
    return el[cols].reindex(columns=px.columns, fill_value=False)


def book_weights(px, cols, book, g):
    el = eligible_mask(px, cols)
    if book == "EWALL":
        e = el.sum(axis=1).astype(float).clip(lower=1.0)
        return el.astype(float).mul(g / e, axis=0)
    n = int(book[3:])
    rank = score(px, vol_scale=VOL_SCALE)[0].where(el).rank(axis=1, ascending=False)
    e = el.sum(axis=1).astype(float)
    k = np.minimum(float(n), e).clip(lower=1.0)
    return rank.le(k, axis=0).astype(float).mul(g / k, axis=0)


# ------------------------------------------------------------------ simulator
def fast_bt(px, w, freq=FREQ):
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).reindex(columns=px.columns).fillna(0.0).shift(1).fillna(0.0).values
    reb = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n = len(px)
    cur = np.zeros(px.shape[1])
    port = np.empty(n)
    turn = np.zeros(n)
    gr = np.zeros(n)
    for i in range(n):
        if reb[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        port[i] = float((cur * rets[i]).sum())
        gr[i] = float(cur.sum())
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    idx = px.index
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx), pd.Series(gr, index=idx))


def apply_mult(r0, turn0, gross0, m):
    dm = m.diff().abs().fillna(0.0)
    return (m * r0, m * turn0 + dm * gross0.shift(1).fillna(0.0), m * gross0)


# ------------------------------------------------------------------ overlays
def panel_breadth(px, cols):
    q = px[cols]
    above = q > q.rolling(200).mean()
    live = q.notna()
    return (above & live).sum(axis=1) / live.sum(axis=1).replace(0, np.nan)


def overlay_mult(name, px, cols, r0):
    if name == "CTRL":
        return pd.Series(1.0, index=px.index)
    if name == "G200":
        on = (panel_breadth(px, cols).shift(1) < BREADTH_B).fillna(False)
        return pd.Series(np.where(on.values, 0.0, 1.0), index=px.index)
    if name == "VT10":
        v = (r0.rolling(20).std() * np.sqrt(252.0)).shift(1)
        return (VOL_TARGET / v).clip(upper=1.0).fillna(1.0)
    if name == "DD10":
        eq = (1.0 + r0).cumprod()
        dd = (eq / eq.cummax() - 1.0).shift(1).fillna(0.0)
        return pd.Series(np.where(dd.values < -DD_TRIG, 0.50, 1.0), index=px.index)
    raise ValueError(name)


# ------------------------------------------------------------------ metrics
def nm3(r):
    n = len(r)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / n) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    sd = float(np.std(r, ddof=1))
    vol = sd * np.sqrt(252.0)
    sh = (float(r.mean()) * 252.0) / vol if vol else np.nan
    return cagr, sh, dd


def sharpe(r):
    sd = float(np.std(r, ddof=1)) * np.sqrt(252.0)
    return (float(r.mean()) * 252.0) / sd if sd else np.nan


def ref_stats(r, oos_mask):
    """The five reference numbers a 4b bar set is built from."""
    h = len(r) // 2
    c, s, dd = nm3(r)
    return dict(CAGR=c, Sharpe=s, MaxDD=abs(dd), H1=sharpe(r[:h]), H2=sharpe(r[h:]),
                OOS=sharpe(r[oos_mask]))


def bars(r, R, oos_mask):
    """Margins of the five 4b bars, in their own units (positive = passes)."""
    h = len(r) // 2
    c, _, dd = nm3(r)
    return {"H1": sharpe(r[:h]) - R["H1"], "H2": sharpe(r[h:]) - R["H2"],
            "OOS": sharpe(r[oos_mask]) - R["OOS"],
            "DD": DD_CAP * R["MaxDD"] - abs(dd),
            "CAGR": c - CAGR_FLOOR * R["CAGR"]}


NONFLOOR = ["H1", "H2", "OOS", "DD"]


def classify(b):
    fails = [k for k in ("H1", "H2", "OOS", "DD", "CAGR") if b[k] <= 0]
    return dict(pass4b=len(fails) == 0,
                floor_only=(fails == ["CAGR"]),
                n_nonfloor_fail=sum(1 for k in NONFLOOR if b[k] <= 0),
                fails=",".join(fails) or "-")


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    P(f"# {SLUG}")
    P("# idea 136 — is the small panel's empty `4b-defensive` class THE PANEL or THE BARS?")
    P("# every arm's four NON-FLOOR 4b bars decomposed, with margins, on 3 panels")
    P("# + a WINDOW control (all panels re-read on the small panel's window)")
    P("# + a BARS control (all five bars re-referenced to IWM instead of SPY)")
    P(f"# books {BOOKS} x overlays {OVERLAYS} x gross {GROSS} x costs {COSTS}")
    P("")

    panels = build_panels()

    # ================================================================ [0] GATES
    P("=" * 152)
    P("[0] REPRODUCTION GATES")
    gpx, gcols = panels[1][1], panels[1][2]
    gw = book_weights(gpx, gcols, "TOP20", 0.75)
    r0g, tg, grg = fast_bt(gpx, gw)
    g1 = 0.0
    for c in (0, 25):
        eng = backtest(gpx, gw, cost_bps=c, freq=FREQ)
        g1 = max(g1, float((r0g - tg * c / 1e4 - eng["returns"]).abs().max()),
                 float((tg - eng["turnover"]).abs().max()))
    P(f"    G1 fast_bt == engine.backtest (returns AND turnover, c in 0/25 bps): max |d| {g1:.3e}")
    assert g1 < 1e-12, g1

    rB, tB, grB = apply_mult(r0g, tg, grg, pd.Series(1.0, index=gpx.index))
    g2 = max(float((rB - r0g).abs().max()), float((tB - tg).abs().max()),
             float((grB - grg).abs().max()))
    P(f"    G2 overlay at OFF (m == 1) == parent on r / turnover / gross: max |d| {g2:.3e}")
    assert g2 < 1e-12, g2

    drop = panels[0][3]
    spx, scols = panels[0][1], panels[0][2]
    P(f"    G3 SMALL439: data/small_meta.csv lists {len(pd.read_csv(REPO/'data'/'small_meta.csv'))} "
      f"tickers, {len(drop)} with max_1d_move >= 1.0 dropped; traded names {len(scols)}; "
      f"dropped names still present: {len([c for c in drop if c in spx.columns])}")
    assert len([c for c in drop if c in spx.columns]) == 0
    assert len(scols) == 483 - 44, len(scols)

    for tag, px, cols, _ in panels:
        w = book_weights(px, cols, "EWALL", 1.00)
        bad = float(max((w[c].abs().max() if c in w.columns else 0.0)
                        for c in (BENCH if tag == "SMALL439" else ["IWM"])))
        P(f"    G4 {tag:8s}: max weight on benchmark columns "
          f"({'SPY, IWM' if tag == 'SMALL439' else 'IWM'}) = {bad:.3e}")
        assert bad == 0.0

    v2r, v2t, _ = fast_bt(gpx, rules_v2_weights(gpx))
    st = (v2r - v2t * 10 / 1e4).loc[gpx.index[WARMUP]:]
    mm = metrics(st)
    c5, s5, d5 = nm3(st.values)
    g5 = max(abs(mm["CAGR"] - c5), abs(mm["Sharpe"] - s5), abs(mm["MaxDD"] - d5))
    P(f"    G5 bar arithmetic vs engine.metrics on RULES v2 @10bps (U56): max |d| {g5:.3e}")
    assert g5 < 1e-12, g5

    # ================================================================ build
    rows, wf, refs = [], [], []
    common_start = None
    P("")
    for tag, px, cols, _ in panels:
        start = px.index[WARMUP]
        if tag == "SMALL439":
            common_start = start
    P(f"    COMMON WINDOW = the small panel's evaluation window, opening {common_start.date()}")
    P("")

    for tag, px, cols, _ in panels:
        own_start = px.index[WARMUP]
        v2r, v2t, _ = fast_bt(px, rules_v2_weights(px))
        for wtag, wstart in [("own", own_start), ("common", common_start)]:
            if wtag == "common" and wstart < own_start:
                continue
            idx = px.loc[wstart:].index
            oos = np.asarray(idx >= pd.Timestamp(OOS_START))
            ism = np.asarray(idx <= pd.Timestamp(IS_END))
            R = {}
            for b in BENCH:
                R[b] = ref_stats(px[b].pct_change().fillna(0.0).loc[wstart:].values, oos)
            if wtag == "own":
                P("=" * 152)
                P(f"PANEL {tag}: {len(cols)} traded cols | {px.index[0].date()} -> "
                  f"{px.index[-1].date()}")
            P(f"  [{tag} / {wtag} window {wstart.date()} .. {px.index[-1].date()}]  "
              f"IS {int(ism.sum())}d / OOS {int(oos.sum())}d")
            for b in BENCH:
                r_ = R[b]
                P(f"     ref {b}: CAGR {r_['CAGR']:.2%} Sharpe {r_['Sharpe']:.3f} "
                  f"(H1 {r_['H1']:.3f} / H2 {r_['H2']:.3f} / OOS {r_['OOS']:.3f}) MaxDD "
                  f"{-r_['MaxDD']:.2%}  -> 4b bars: DD cap {DD_CAP*r_['MaxDD']:.2%}, "
                  f"CAGR floor {CAGR_FLOOR*r_['CAGR']:.2%}")
                refs.append(dict(panel=tag, window=wtag, ref=b, **r_))
            for c in COSTS:
                v2 = (v2r - v2t * c / 1e4).loc[wstart:].values
                _, v2s, v2dd = nm3(v2)
                h = len(v2) // 2
                R[f"V2_{c}"] = dict(H1=sharpe(v2[:h]), H2=sharpe(v2[h:]), MaxDD=abs(v2dd),
                                    Sharpe=v2s)

            for book in BOOKS:
                for g in GROSS:
                    w = book_weights(px, cols, book, g)
                    pr, pt, pg = fast_bt(px, w)
                    for ov in OVERLAYS:
                        m = overlay_mult(ov, px, cols, pr)
                        orr, otn, ogr = apply_mult(pr, pt, pg, m)
                        rr = orr.loc[wstart:].values
                        tt = otn.loc[wstart:].values
                        for c in COSTS:
                            r = rr - tt * (c / 1e4)
                            cg, sh, dd = nm3(r)
                            row = dict(panel=tag, window=wtag, book=book,
                                       n=(np.nan if book == "EWALL" else int(book[3:])),
                                       gross=g, overlay=ov, cost=c,
                                       mean_gross=float(ogr.loc[wstart:].mean()),
                                       turnover_yr=float(tt.sum())
                                       / ((idx[-1] - idx[0]).days / 365.25),
                                       CAGR=cg, Sharpe=sh, MaxDD=dd,
                                       IS_Sharpe=sharpe(r[ism]), OOS_Sharpe=sharpe(r[oos]),
                                       OOS_CAGR=nm3(r[oos])[0], OOS_MaxDD=nm3(r[oos])[2])
                            for b in BENCH:
                                bb = bars(r, R[b], oos)
                                cl = classify(bb)
                                for k, v in bb.items():
                                    row[f"m{b}_{k}"] = v
                                row[f"pass4b_{b}"] = cl["pass4b"]
                                row[f"floor_only_{b}"] = cl["floor_only"]
                                row[f"nf_fail_{b}"] = cl["n_nonfloor_fail"]
                                row[f"fails_{b}"] = cl["fails"]
                            V = R[f"V2_{c}"]
                            hh = len(r) // 2
                            row["pass4a"] = bool(sharpe(r[:hh]) > V["H1"]
                                                 and sharpe(r[hh:]) > V["H2"]
                                                 and abs(dd) <= V["MaxDD"])
                            row["v2_Sharpe"] = V["Sharpe"]
                            # IS-window bar set, for the rule-8 selectors
                            ir = r[ism]
                            ih = len(ir) // 2
                            icg, _, idd = nm3(ir)
                            iR = R["SPY"]
                            ib = {"H1": sharpe(ir[:ih]) - iR["H1"], "H2": sharpe(ir[ih:]) - iR["H2"],
                                  "OOS": 0.0, "DD": DD_CAP * iR["MaxDD"] - abs(idd),
                                  "CAGR": icg - CAGR_FLOOR * iR["CAGR"]}
                            row["IS_pass_nonfloor"] = bool(ib["H1"] > 0 and ib["H2"] > 0
                                                           and ib["DD"] > 0)
                            row["IS_pass_floor"] = bool(ib["CAGR"] > 0)
                            rows.append(row)

    G = pd.DataFrame(rows)
    RF = pd.DataFrame(refs)

    # ================================================================ [1] the decomposition
    P("")
    P("=" * 152)
    P("[1] THE DECOMPOSITION — which of the four NON-FLOOR bars fails, on every arm")
    for wtag in ("common", "own"):
        sub = G[G.window == wtag]
        if not len(sub):
            continue
        P("")
        P(f"    --- {wtag.upper()} window, reference SPY (the PROTOCOL bar set) ---")
        t = sub.groupby("panel").agg(
            n=("mSPY_H1", "size"),
            fail_H1=("mSPY_H1", lambda x: int((x <= 0).sum())),
            fail_H2=("mSPY_H2", lambda x: int((x <= 0).sum())),
            fail_OOS=("mSPY_OOS", lambda x: int((x <= 0).sum())),
            fail_DD=("mSPY_DD", lambda x: int((x <= 0).sum())),
            fail_CAGR=("mSPY_CAGR", lambda x: int((x <= 0).sum())),
            pass4b=("pass4b_SPY", "sum"), defensive=("floor_only_SPY", "sum"),
            pass4a=("pass4a", "sum"))
        P("      " + t.to_string().replace("\n", "\n      "))
        P("      margins (median [min, max]) of each bar, by panel:")
        for pan in sub.panel.unique():
            s = sub[sub.panel == pan]
            P(f"        {pan:9s} " + "  ".join(
                f"{k} {s[f'mSPY_{k}'].median():+.3f} [{s[f'mSPY_{k}'].min():+.3f}, "
                f"{s[f'mSPY_{k}'].max():+.3f}]" for k in ("H1", "H2", "OOS", "DD", "CAGR")))
        P("      arms with ZERO non-floor failures (the defensive candidate set), by panel:")
        z = sub[sub.nf_fail_SPY == 0].groupby("panel").size()
        P("        " + ", ".join(f"{p} {int(z.get(p, 0))}/{int((sub.panel == p).sum())}"
                                 for p in sub.panel.unique()))

    # ================================================================ [2] panel or bars
    P("")
    P("=" * 152)
    P("[2] PANEL or BARS?  the same arms re-scored against IWM instead of SPY")
    sub = G[G.window == "common"]
    for b in BENCH:
        t = sub.groupby("panel").agg(
            n=(f"m{b}_H1", "size"),
            fail_H1=(f"m{b}_H1", lambda x: int((x <= 0).sum())),
            fail_H2=(f"m{b}_H2", lambda x: int((x <= 0).sum())),
            fail_OOS=(f"m{b}_OOS", lambda x: int((x <= 0).sum())),
            fail_DD=(f"m{b}_DD", lambda x: int((x <= 0).sum())),
            fail_CAGR=(f"m{b}_CAGR", lambda x: int((x <= 0).sum())),
            pass4b=(f"pass4b_{b}", "sum"), defensive=(f"floor_only_{b}", "sum"))
        P(f"    reference {b} (common window):")
        P("      " + t.to_string().replace("\n", "\n      "))
    sm = sub[sub.panel == "SMALL439"]
    P(f"    SMALL439 defensive members: {int(sm.floor_only_SPY.sum())} vs SPY, "
      f"{int(sm.floor_only_IWM.sum())} vs IWM, of {len(sm)} arms.")
    P(f"    SMALL439 arms clearing all four non-floor bars: {int((sm.nf_fail_SPY == 0).sum())} "
      f"vs SPY, {int((sm.nf_fail_IWM == 0).sum())} vs IWM.")

    # ================================================================ [3] where it fails
    P("")
    P("=" * 152)
    P("[3] SMALL439, common window, SPY reference — the failing-bar signature of every arm")
    P("    failing-bar patterns (non-floor bars only):")
    sm2 = sm.copy()
    sm2["nf_pattern"] = sm2.apply(
        lambda r: ",".join(k for k in NONFLOOR if r[f"mSPY_{k}"] <= 0) or "-", axis=1)
    P("      " + sm2.nf_pattern.value_counts().to_string().replace("\n", "\n      "))
    P("")
    P("    how far each non-floor bar misses on SMALL439 (only the FAILING arms):")
    for k in NONFLOOR:
        f = sm2[sm2[f"mSPY_{k}"] <= 0][f"mSPY_{k}"]
        if len(f):
            P(f"      {k:4s} fails {len(f):>3d}/{len(sm2)}  median {f.median():+.3f}  "
              f"worst {f.min():+.3f}  closest {f.max():+.3f}")
        else:
            P(f"      {k:4s} fails   0/{len(sm2)}")
    P("")
    P("    the SMALL439 arms closest to defensive (ranked by their worst non-floor margin):")
    sm2["worst_nf"] = sm2[[f"mSPY_{k}" for k in NONFLOOR]].min(axis=1)
    top = sm2.sort_values("worst_nf", ascending=False).head(12)
    P("      " + top[["book", "gross", "overlay", "cost", "mean_gross", "CAGR", "Sharpe",
                      "MaxDD", "mSPY_H1", "mSPY_H2", "mSPY_OOS", "mSPY_DD", "mSPY_CAGR",
                      "worst_nf", "fails_SPY"]]
      .to_string(index=False, float_format=lambda x: f"{x:.3f}").replace("\n", "\n      "))

    # ================================================================ [4] every row
    P("")
    P("=" * 152)
    P("[4] EVERY GRID POINT (common window, SPY reference; cost 0 is the diagnostic rung)")
    show = sub[["panel", "book", "gross", "overlay", "cost", "mean_gross", "CAGR", "Sharpe",
                "MaxDD", "OOS_Sharpe", "mSPY_H1", "mSPY_H2", "mSPY_OOS", "mSPY_DD",
                "mSPY_CAGR", "nf_fail_SPY", "floor_only_SPY", "pass4b_SPY", "pass4a"]]
    P("    " + show.to_string(index=False, float_format=lambda x: f"{x:.3f}")
      .replace("\n", "\n    "))

    # ================================================================ [5] rule 8
    P("")
    P("=" * 152)
    P("[5] RULE 8 WALK-FORWARD — (n, g) chosen on 2011-2016 only, 2017-2026 read once")
    P("    cells = panel x overlay x cost, common window, PROTOCOL cost rungs only")
    P("    (the 0-bps diagnostic rung is excluded); four selectors fixed in advance.")
    sel_rows, empt = [], 0
    for (pan, ov, c), cell in sub[sub.cost > 0].groupby(["panel", "overlay", "cost"]):
        cand = {
            "S0": cell,
            "S1": cell[cell.IS_pass_nonfloor & cell.IS_pass_floor],
            "S2": cell[cell.IS_pass_nonfloor],
            "S3": cell[cell.IS_pass_nonfloor & ~cell.IS_pass_floor],
        }
        ctrl = cell[cell.overlay == ov]
        spy_oos = RF[(RF.panel == pan) & (RF.window == "common") & (RF.ref == "SPY")].iloc[0]
        for s, cc in cand.items():
            if not len(cc):
                empt += 1
                sel_rows.append(dict(panel=pan, overlay=ov, cost=c, selector=s, pick="EMPTY"))
                continue
            p = cc.loc[cc.IS_Sharpe.idxmax()]
            sel_rows.append(dict(
                panel=pan, overlay=ov, cost=c, selector=s,
                pick=f"{p.book}/g{p.gross:.2f}", IS_Sharpe=p.IS_Sharpe,
                OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe, OOS_MaxDD=p.OOS_MaxDD,
                full_Sharpe=p.Sharpe, full_MaxDD=p.MaxDD,
                spy_OOS_Sharpe=spy_oos["OOS"], v2_Sharpe=p.v2_Sharpe,
                ctrl_OOS_Sharpe=float(ctrl.OOS_Sharpe.max()),
                pass4b=p.pass4b_SPY, pass4a=p.pass4a, defensive=p.floor_only_SPY))
    S = pd.DataFrame(sel_rows)
    P("    " + S.to_string(index=False, float_format=lambda x: f"{x:.3f}")
      .replace("\n", "\n    "))
    P("")
    e = S[S.pick == "EMPTY"].groupby(["panel", "selector"]).size()
    P(f"    EMPTY selector cells: {empt} of {len(S)}"
      + ("" if not len(e) else "\n      " + e.to_string().replace("\n", "\n      ")))
    ok = S[S.pick != "EMPTY"]
    P("    OOS of the IS-chosen arms, by panel x selector (mean):")
    P("      " + ok.groupby(["panel", "selector"])[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]
      .mean().to_string(float_format=lambda x: f"{x:.3f}").replace("\n", "\n      "))
    P(f"    IS-chosen arms beating SPY's OOS Sharpe: "
      f"{int((ok.OOS_Sharpe > ok.spy_OOS_Sharpe).sum())}/{len(ok)}; clearing 4b: "
      f"{int(ok.pass4b.sum())}/{len(ok)}; clearing 4a: {int(ok.pass4a.sum())}/{len(ok)}; "
      f"defensive: {int(ok.defensive.sum())}/{len(ok)}")

    # ================================================================ [6] verdict
    P("")
    P("=" * 152)
    P("[6] VERDICT")
    for pan in ("SMALL439", "U56", "B136"):
        s = sub[sub.panel == pan]
        P(f"    {pan:9s} common window: defensive {int(s.floor_only_SPY.sum())}/{len(s)}, "
          f"4b {int(s.pass4b_SPY.sum())}/{len(s)}, 4a {int(s.pass4a.sum())}/{len(s)}, "
          f"zero non-floor failures {int((s.nf_fail_SPY == 0).sum())}/{len(s)}  |  "
          f"non-floor fail counts H1 {int((s.mSPY_H1 <= 0).sum())} H2 "
          f"{int((s.mSPY_H2 <= 0).sum())} OOS {int((s.mSPY_OOS <= 0).sum())} DD "
          f"{int((s.mSPY_DD <= 0).sum())}")
    ddf = int((sm.mSPY_DD <= 0).sum())
    shf = int(((sm.mSPY_H1 <= 0) | (sm.mSPY_H2 <= 0) | (sm.mSPY_OOS <= 0)).sum())
    if ddf == 0 and shf > 0:
        P("    -> the queue's stated test is MET: on the small panel the DD cap never binds and")
        P("       the failures are entirely H1/H2/OOS Sharpe.  The panel has no defensive books.")
    elif ddf > 0 and shf > 0:
        P(f"    -> the queue's stated test is NOT met: the DD cap binds on {ddf} small-panel arms")
        P(f"       as well as the Sharpe bars on {shf}.  See [2] for whether re-referencing to IWM")
        P("       moves the count, i.e. whether it is the panel or the bars.")
    else:
        P("    -> neither the DD cap nor the Sharpe bars bind as the queue expected; see [1].")

    G.to_csv(f"{OUT}.grid.csv", index=False)
    RF.to_csv(f"{OUT}.refs.csv", index=False)
    S.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("")
    P(f"Wrote {OUT.name}.grid.csv ({len(G)}), .refs.csv ({len(RF)}), "
      f".walkforward.csv ({len(S)})  [{time.time()-t0:.1f}s]")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
