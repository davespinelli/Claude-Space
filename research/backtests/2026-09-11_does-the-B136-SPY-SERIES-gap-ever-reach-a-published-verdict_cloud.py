#!/usr/bin/env python3
"""
IDEA 698 -- does-the-B136-SPY-SERIES-gap-ever-reach-a-published-verdict
=======================================================================

THE QUEUE'S QUESTION (verbatim intent)
--------------------------------------
  Idea 517 found `SPY` in data/prices_broad.csv differs from `SPY` in data/prices.csv on
  97.7% of common days (max rel 6.326e-05), so 4b's own comparand is panel-dependent, and
  priced it at <1e-4 of Sharpe, below publishing resolution.  Test whether any committed 4b
  pass sits inside that margin, i.e. whether the bar's own cache ever decides a verdict.

WHAT "INSIDE THE MARGIN" HAS TO MEAN
------------------------------------
  Idea 517 priced the gap as a movement of ONE number (SPY's Sharpe).  A 4b verdict is not
  one number: it is five bars (H1 Sharpe, H2 Sharpe, OOS Sharpe, a DD cap at 0.60x |SPY
  MaxDD|, a CAGR floor at 0.70x SPY CAGR), and a verdict is decided by the cache only if some
  book's margin on some bar is SMALLER than that bar's own movement between the two caches.
  So this run measures (i) the BAR SHIFT -- how far each of the five bars moves when the SPY
  series is swapped -- and (ii) the MARGIN DISTRIBUTION of the record's committed 4b passes,
  and asks whether the two populations ever overlap.

  There is also a SECOND channel idea 517 did not separate.  On B136, `SPY` is not only the
  comparand: `load_universe(broad=True)` returns it as a COLUMN, and the record's books rank
  and can HOLD it.  Swapping the series therefore moves the BOOK as well as the BAR.  This run
  prices the two channels separately.

DESIGN
------
  LEG A -- CENSUS OF THE RECORD'S COMMITTED 4b PASSES.  Every `research/backtests/*.csv` that
  publishes a 4b verdict column beside at least one `SPY*` bar column is read; for every row
  marked PASS, each available 4b leg's MARGIN is recomputed from the file's own published
  numbers (OOS Sharpe margin, DD margin, CAGR margin, H1/H2 margins where published).  The
  headline is the distribution of each pass's SMALLEST margin -- its distance from flipping --
  against the bar shift measured in LEG B.  Nothing is re-simulated here: this is the record's
  own arithmetic, restated with a margin column.

  LEG B -- THE BAR SHIFT AND THE TWO CHANNELS (price).  Three arms on B136, over the common
  calendar of the two caches, so that only the SPY series changes:
    A  NATIVE   bar = prices_broad SPY, panel column = prices_broad SPY   (the status quo)
    B  BAR-SWAP bar = prices.csv   SPY, panel column = prices_broad SPY   (COMPARAND channel)
    C  BOTH     bar = prices.csv   SPY, panel column = prices.csv   SPY   (both channels)
  Book family (pre-registered, not chosen by outcome): CAND-n through the record's RULES v1
  gate with no vol scaler, n in {5,10,15,20,30,40,50} x gross in {0.50,0.75,1.00} = 21, plus
  the live band book (RULES v2, band 0.03) at the same three grosses = 3.  **24 books, all
  reported**, each under all three arms = 72 verdict readings.
    TUNED (2)  BOOK FAMILY (CAND-n ladder x gross) and ARM (which SPY series feeds which
               role).  Both axes are reported in full; no third axis is introduced.
    FIXED      weekly cadence, 10 bps (PROTOCOL rule 2), t+1 execution, 260-row warm-up skip,
               IS <= 2016-12-31 / OOS >= 2017-01-01 (PROTOCOL rule 8).
    COST       10 bps carries every verdict; 0/25 bps is printed as LABELLED ROBUSTNESS only.

  RULE 8 (PROTOCOL 8).  One book per arm chosen by IS Sharpe on IS rows only; 2017-2026 read
  once, against SPY OOS and live RULES v2 OOS, with both KEEP paths.

PRE-REGISTERED GATES (printed before any new number is read)
------------------------------------------------------------
  G1  fast_backtest == engine.backtest @10 bps                                   bar 1e-12
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                         bar 0.0
  G3  IDEA 517 REPRODUCTION: the two SPY series differ on ~97.7% of common days and the max
      relative difference is of order 1e-5 (the published 6.326e-05 was measured on an
      earlier prices.csv vintage; the direction and order of magnitude are what is pinned)
  G4  THE ARMS DIFFER ONLY IN SPY: arm A and arm C panels are identical on every column
      except `SPY`                                                               bar 0.0
  G5  COMMON CALENDAR: all three arms run on the identical index                 bar 0.0
  G6  CAUSALITY: w(px[:d]) is a value-for-value prefix of w(px)[:d]              bar 0.0

SURVIVORSHIP (PROTOCOL 9)
-------------------------
  B136 is today's constituents (research/universe_broad.json), so names that were acquired,
  delisted or dropped from the index are absent and every LEVEL below is biased upward; none
  is a tradeable estimate.  This run's headline is a DIFFERENCE between two readings of the
  same books on the same days, to which the bias applies identically on both sides.
"""
import glob
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score        # noqa: E402
from engine import backtest, rebalance_mask                                    # noqa: E402

COST0 = 10.0
COSTS_APPENDIX = [0.0, 25.0]
FREQ = "W"
BAND0 = 0.03
VOLCAP = 0.60
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
NS = [5, 10, 15, 20, 30, 40, 50]
GROSSES = [0.50, 0.75, 1.00]
DD_MULT, CAGR_MULT = 0.60, 0.70

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ==========================================================================================
def fast_backtest(prices, weights, freq=FREQ, cost=COST0):
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


def cand_book(px, n, gross):
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    r = sc.where(elig).rank(axis=1, ascending=False)
    return (r <= n).astype(float) * (gross / n)


def margins(m, oos_s, ms, spy_oos):
    """Signed distance of each 4b leg from its bar.  Positive = passing, and the size is how
    far the bar would have to move to flip the leg."""
    return dict(mH1=m["H1"] - ms["H1"], mH2=m["H2"] - ms["H2"], mOOS=oos_s - spy_oos,
                mDD=DD_MULT * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
                mCAGR=m["CAGR"] - CAGR_MULT * ms["CAGR"])


def pass4b(mg):
    return all(v > 0 for v in mg.values())


def pass4a(m, mb):
    return (m["H1"] > mb["H1"]) and (m["H2"] > mb["H2"]) and (m["MaxDD"] >= mb["MaxDD"])


# ==========================================================================================
# LEG A -- census of the record's committed 4b passes, with a margin column
# ==========================================================================================
P4B = ("pass4b", "p4b", "4b", "keep4b")
TRUE = ("true", "1", "1.0", "yes", "pass", "keep")


def _find(cols, *names):
    low = {c.lower(): c for c in cols}
    for n in names:
        if n in low:
            return low[n]
    return None


BROAD_TOK = ("b136", "broad", "b13", "bstk")


def _panel_of(val, fname):
    """BROAD / OTHER / UNKNOWN.  The two-cache gap exists ONLY on the broad panel: U56 reads
    its SPY from data/prices.csv and baseline.load_universe(small=True) JOINS the same
    prices.csv SPY onto the small panel, so on those two panels both readings are the SAME
    series and the bar shift is identically zero."""
    s = f"{val}".lower()
    if any(t in s for t in BROAD_TOK):
        return "BROAD"
    if s not in ("nan", "none", ""):
        return "OTHER"
    return "BROAD" if any(t in fname.lower() for t in BROAD_TOK) else "UNKNOWN"


def census():
    P("=" * 100)
    P("(C) LEG A -- CENSUS: every COMMITTED 4b PASS in the record, restated with a MARGIN")
    P("=" * 100)
    rows, files_scanned, files_used = [], 0, 0
    for f in sorted(glob.glob(str(ROOT / "research" / "backtests" / "*.csv"))):
        try:
            head = pd.read_csv(f, nrows=2)
        except Exception:
            continue
        pc = _find(head.columns, *P4B)
        if pc is None:
            continue
        files_scanned += 1
        if not any(c.lower().startswith("spy") for c in head.columns):
            continue
        try:
            d = pd.read_csv(f)
        except Exception:
            continue
        ok = d[pc].astype(str).str.strip().str.lower().isin(TRUE)
        d = d[ok]
        if d.empty:
            continue
        files_used += 1
        cS = _find(d.columns, "oos_sharpe", "sharpe_oos")
        cSs = _find(d.columns, "spy_oos_sharpe", "spy_oos_s", "spyoos_sharpe")
        cC = _find(d.columns, "oos_cagr", "cagr_oos")
        cCs = _find(d.columns, "spy_oos_cagr")
        cD = _find(d.columns, "oos_maxdd", "maxdd_oos")
        cDs = _find(d.columns, "spy_oos_maxdd")
        cFull = _find(d.columns, "cagr")
        cFullS = _find(d.columns, "spy_cagr")
        cFullD = _find(d.columns, "maxdd")
        cFullDs = _find(d.columns, "spy_maxdd")
        cPan = _find(d.columns, "panel", "uni", "universe", "pan", "pool")
        for _, r in d.iterrows():
            mm = {}
            if cS and cSs:
                mm["mOOS"] = float(r[cS]) - float(r[cSs])
            if cC and cCs:
                mm["mCAGR_oos"] = float(r[cC]) - CAGR_MULT * float(r[cCs])
            if cD and cDs:
                mm["mDD_oos"] = DD_MULT * abs(float(r[cDs])) - abs(float(r[cD]))
            if cFull and cFullS:
                mm["mCAGR"] = float(r[cFull]) - CAGR_MULT * float(r[cFullS])
            if cFullD and cFullDs:
                mm["mDD"] = DD_MULT * abs(float(r[cFullDs])) - abs(float(r[cFullD]))
            mm = {k: v for k, v in mm.items() if np.isfinite(v)}
            if not mm:
                continue
            k = min(mm, key=lambda x: abs(mm[x]))
            rows.append(dict(file=Path(f).name, legs=len(mm), tightest_leg=k,
                             tightest_margin=abs(mm[k]),
                             panel=_panel_of(r[cPan] if cPan else np.nan, Path(f).name), **mm))
    c = pd.DataFrame(rows)
    P(f"  files publishing a 4b verdict column          : {files_scanned}")
    P(f"  ...of which also publish a SPY bar column      : {files_used}")
    P(f"  COMMITTED 4b PASSES with a recomputable margin : {len(c)}")
    if c.empty:
        return c
    q = c.tightest_margin
    P(f"  tightest-margin distribution (abs, over {len(c)} passes):")
    for p_ in [0.0, 0.001, 0.01, 0.05, 0.10, 0.25, 0.50]:
        P(f"    p{p_ * 100:>5.1f}  {q.quantile(p_):.6f}")
    P(f"    min {q.min():.3e}   median {q.median():.4f}   max {q.max():.4f}")
    P("  which leg is tightest:")
    for k, v in c.tightest_leg.value_counts().items():
        P(f"    {k:<12} {v:6d}  ({v / len(c):.1%})")
    P("  panel of the pass (the gap EXISTS ONLY on BROAD -- U56 and SMALL both read their SPY")
    P("  from data/prices.csv, so their bar shift is identically zero):")
    for k, v in c.panel.value_counts().items():
        P(f"    {k:<12} {v:6d}  ({v / len(c):.1%})")
    dump(c, "census")
    return c


# ==========================================================================================
def main():
    P("=" * 100)
    P(f"IDEA 698 -- {STEM}")
    P("=" * 100)

    spy_u_raw = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)["SPY"]
    pxb = load_universe(broad=True)
    idx = pxb.index.intersection(spy_u_raw.index)
    pxb = pxb.loc[idx]
    spy_u = spy_u_raw.loc[idx]
    spy_b = pxb["SPY"]

    # ---------------------------------------------------------------- gates
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- run before any new number is read")
    P("=" * 100)
    ok = True
    w = band_book(pxb, BAND0, 0.75)
    g2 = float(np.abs(w.values - rules_v2_weights(pxb, BAND0, 0.75).values).max())
    P(f"  G2 band_book(0.03,0.75) == rules_v2_weights       : {g2:.3e}  {'PASS' if g2 == 0 else 'FAIL'}")
    ok &= g2 == 0.0

    slow = backtest(pxb, w, cost_bps=COST0, freq=FREQ)["returns"]
    fast = fast_backtest(pxb, w, FREQ, COST0)
    j = pxb.index[WARM]
    g1 = float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max())
    P(f"  G1 fast_backtest == engine.backtest @10 bps       : {g1:.3e}  {'PASS' if g1 < 1e-12 else 'FAIL'}")
    ok &= g1 < 1e-12

    dif = (spy_u - spy_b).abs()
    frac = float((dif > 0).mean())
    relmax = float((dif / spy_u.abs()).max())
    g3 = (0.90 < frac < 1.0) and (1e-6 < relmax < 1e-3)
    P(f"  G3 idea 517 reproduction: differ on {frac:.4%} of {len(idx)} common days, "
      f"max abs ${dif.max():.4f}, max rel {relmax:.3e}  {'PASS' if g3 else 'FAIL'}")
    P(f"     (517 published 97.7% and 6.326e-05 on an earlier prices.csv vintage; the gate "
      f"pins direction and order of magnitude, not the digits)")
    ok &= g3

    pxc = pxb.copy()
    pxc["SPY"] = spy_u
    other = [c for c in pxb.columns if c != "SPY"]
    g4 = float(np.abs(pxb[other].fillna(-1).values - pxc[other].fillna(-1).values).max())
    P(f"  G4 arms differ ONLY in the SPY column             : {g4:.3e}  {'PASS' if g4 == 0 else 'FAIL'}")
    ok &= g4 == 0.0

    g5 = bool(pxb.index.equals(pxc.index)) and bool(pxb.index.equals(spy_u.index))
    P(f"  G5 all arms on one common calendar ({len(idx)} rows)  : {'PASS' if g5 else 'FAIL'}")
    ok &= g5

    wf = cand_book(pxb, 20, 0.75)
    cut = pxb.index[int(len(pxb) * 0.7)]
    wt_ = cand_book(pxb.loc[:cut], 20, 0.75)
    g6 = float(np.abs(wt_.values - wf.loc[:cut, wt_.columns].values).max())
    P(f"  G6 CAUSALITY w(px[:d]) prefix of w(px)            : {g6:.3e}  {'PASS' if g6 == 0 else 'FAIL'}")
    ok &= g6 == 0.0
    P(f"  GATES: {'ALL PASS' if ok else 'AT LEAST ONE FAILED -- results below are NOT publishable'}")
    if not ok:
        P("  ABORTING: a pre-registered gate failed.")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
        return 1

    # ---------------------------------------------------------------- the bar shift
    P("=" * 100)
    P("(B) THE BAR SHIFT -- how far each 4b bar moves when the SPY SERIES is swapped")
    P("=" * 100)
    st = pxb.index[WARM]
    r_b = spy_b.pct_change().fillna(0).loc[st:]
    r_u = spy_u.pct_change().fillna(0).loc[st:]
    mb_, mu_ = M(r_b), M(r_u)
    ob_m, ou_m = M(r_b.loc[OOS_START:]), M(r_u.loc[OOS_START:])
    ob, ou = ob_m["Sharpe"], ou_m["Sharpe"]
    bars = pd.DataFrame([
        dict(bar="H1 Sharpe", broad=mb_["H1"], prices=mu_["H1"], shift=abs(mb_["H1"] - mu_["H1"])),
        dict(bar="H2 Sharpe", broad=mb_["H2"], prices=mu_["H2"], shift=abs(mb_["H2"] - mu_["H2"])),
        dict(bar="OOS Sharpe", broad=ob, prices=ou, shift=abs(ob - ou)),
        dict(bar="DD cap (0.60x)", broad=DD_MULT * abs(mb_["MaxDD"]), prices=DD_MULT * abs(mu_["MaxDD"]),
             shift=DD_MULT * abs(abs(mb_["MaxDD"]) - abs(mu_["MaxDD"]))),
        dict(bar="CAGR floor (0.70x)", broad=CAGR_MULT * mb_["CAGR"], prices=CAGR_MULT * mu_["CAGR"],
             shift=CAGR_MULT * abs(mb_["CAGR"] - mu_["CAGR"])),
        dict(bar="OOS CAGR floor (0.70x)", broad=CAGR_MULT * ob_m["CAGR"],
             prices=CAGR_MULT * ou_m["CAGR"],
             shift=CAGR_MULT * abs(ob_m["CAGR"] - ou_m["CAGR"])),
        dict(bar="OOS DD cap (0.60x)", broad=DD_MULT * abs(ob_m["MaxDD"]),
             prices=DD_MULT * abs(ou_m["MaxDD"]),
             shift=DD_MULT * abs(abs(ob_m["MaxDD"]) - abs(ou_m["MaxDD"]))),
    ])
    for _, r in bars.iterrows():
        P(f"  {r.bar:<20} prices_broad {r.broad: .8f}   prices.csv {r.prices: .8f}   "
          f"|shift| {r['shift']:.3e}")
    BARSHIFT = float(bars["shift"].max())
    P(f"  LARGEST BAR SHIFT over the seven 4b bars         : {BARSHIFT:.3e}")
    # each census margin key compared against ITS OWN leg's shift, not the largest one
    LEGSHIFT = {"mOOS": float(bars.loc[bars.bar == "OOS Sharpe", "shift"].iloc[0]),
                "mCAGR": float(bars.loc[bars.bar == "CAGR floor (0.70x)", "shift"].iloc[0]),
                "mCAGR_oos": float(bars.loc[bars.bar == "OOS CAGR floor (0.70x)", "shift"].iloc[0]),
                "mDD": float(bars.loc[bars.bar == "DD cap (0.60x)", "shift"].iloc[0]),
                "mDD_oos": float(bars.loc[bars.bar == "OOS DD cap (0.60x)", "shift"].iloc[0])}
    P("  LEG-MATCHED shifts used for the census test (a margin is only ever compared against")
    P("  the shift of ITS OWN bar):")
    for k, v in LEGSHIFT.items():
        P(f"    {k:<12} {v:.3e}")
    dump(bars, "barshift")
    globals()["LEGSHIFT"] = LEGSHIFT

    # ---------------------------------------------------------------- leg A
    cen = census()

    P("=" * 100)
    P("(D) DOES ANY COMMITTED 4b PASS SIT INSIDE THE BAR SHIFT?")
    P("=" * 100)
    if not cen.empty:
        LS = globals()["LEGSHIFT"]
        # LEG-MATCHED: a pass is decidable by the cache if ANY leg's margin is smaller than
        # that leg's own bar shift.  This is the correct test; the max-shift test below is
        # kept as the looser upper bound idea 517's framing implies.
        dec = pd.Series(False, index=cen.index)
        slack = pd.Series(np.inf, index=cen.index)
        for k, sh in LS.items():
            if k in cen.columns:
                v = cen[k].abs()
                dec |= (v < sh)
                slack = np.minimum(slack, v / sh)
        cen["decidable_legmatched"] = dec
        cen["min_margin_over_own_shift"] = slack
        P(f"  LEG-MATCHED test -- passes decidable by the cache : {int(dec.sum())} / {len(cen)} "
          f"({dec.mean():.4%})")
        brx = cen[cen.panel == "BROAD"]
        P(f"  ...restricted to BROAD (where the gap exists)    : "
          f"{int(brx.decidable_legmatched.sum())} / {len(brx)} "
          f"({brx.decidable_legmatched.mean():.4%})")
        P(f"  smallest BROAD margin as a multiple of its own leg's shift : "
          f"{brx.min_margin_over_own_shift.min():.2f}x")
        dump(cen, "census")
        P("")
        inside = int((cen.tightest_margin < BARSHIFT).sum())
        inside10 = int((cen.tightest_margin < 10 * BARSHIFT).sum())
        inside100 = int((cen.tightest_margin < 100 * BARSHIFT).sum())
        P(f"  committed 4b passes with a margin < the bar shift ({BARSHIFT:.3e}) : "
          f"{inside} / {len(cen)}  ({inside / len(cen):.4%})")
        P(f"  ...< 10x the bar shift                                        : {inside10} / {len(cen)}")
        P(f"  ...< 100x the bar shift                                       : {inside100} / {len(cen)}")
        P(f"  ratio  median tightest margin / bar shift                     : "
          f"{cen.tightest_margin.median() / BARSHIFT:,.0f}x")
        P(f"  ratio  MINIMUM tightest margin / bar shift                    : "
          f"{cen.tightest_margin.min() / BARSHIFT:,.1f}x")
        if inside:
            P("  the passes inside the shift (UNRESTRICTED -- every panel):")
            for _, r in cen[cen.tightest_margin < BARSHIFT].head(20).iterrows():
                P(f"    {r.file[:62]:<62} {r.panel:<8} leg {r.tightest_leg:<12} "
                  f"margin {r.tightest_margin:.3e}")
        P("")
        P("  RESTRICTED TO THE PANEL WHERE THE GAP ACTUALLY EXISTS (BROAD):")
        br = cen[cen.panel == "BROAD"]
        if br.empty:
            P("    no committed BROAD-panel 4b pass carries a recomputable margin.")
        else:
            ib = int((br.tightest_margin < BARSHIFT).sum())
            P(f"    committed BROAD 4b passes                     : {len(br)}")
            P(f"    ...with a margin < the bar shift ({BARSHIFT:.3e})  : {ib}  ({ib / len(br):.4%})")
            P(f"    ...< 10x                                      : "
              f"{int((br.tightest_margin < 10 * BARSHIFT).sum())}")
            P(f"    minimum BROAD margin                          : {br.tightest_margin.min():.3e} "
              f"({br.tightest_margin.min() / BARSHIFT:,.1f}x the shift)")
            for _, r in br[br.tightest_margin < BARSHIFT].head(20).iterrows():
                P(f"      {r.file[:62]:<62} leg {r.tightest_leg:<12} margin {r.tightest_margin:.3e}")
        P("    NOTE: passes on OTHER/UNKNOWN panels are printed above for completeness only.")
        P("    On U56 and SMALL the two readings are the SAME series, so the shift is 0 and no")
        P("    margin, however small, can be decided by this cache.")

    # ---------------------------------------------------------------- leg B
    P("=" * 100)
    P("(E) LEG B -- 24 BOOKS x 3 ARMS ON B136, BOTH CHANNELS SEPARATED (all points reported)")
    P("=" * 100)
    arms = {"A_NATIVE": (pxb, spy_b), "B_BARSWAP": (pxb, spy_u), "C_BOTH": (pxc, spy_u)}
    books = ([(f"CAND{n}@g{g:.2f}", (lambda p, n=n, g=g: cand_book(p, n, g))) for n in NS for g in GROSSES]
             + [(f"BAND@g{g:.2f}", (lambda p, g=g: band_book(p, BAND0, g))) for g in GROSSES])
    rows = []
    for aname, (panel, spyser) in arms.items():
        sr = spyser.pct_change().fillna(0).loc[st:]
        ms, spy_oos = M(sr), M0(sr.loc[OOS_START:])
        base = fast_backtest(panel, rules_v2_weights(panel), FREQ, COST0).loc[st:]
        mbase = M(base)
        for bname, fn in books:
            r = fast_backtest(panel, fn(panel), FREQ, COST0).loc[st:]
            m = M(r)
            mo = M(r.loc[OOS_START:])
            mi = M(r.loc[:IS_END])
            mg = margins(m, mo["Sharpe"], ms, spy_oos)
            rows.append(dict(arm=aname, book=bname, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                             MaxDD=m["MaxDD"], H1=m["H1"], H2=m["H2"], IS_Sharpe=mi["Sharpe"],
                             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                             SPY_CAGR=ms["CAGR"], SPY_Sharpe=ms["Sharpe"], SPY_MaxDD=ms["MaxDD"],
                             SPY_OOS_Sharpe=spy_oos, BASE_Sharpe=mbase["Sharpe"],
                             pass4b=pass4b(mg), pass4a=pass4a(m, mbase),
                             tightest=min(abs(v) for v in mg.values()),
                             tightest_leg=min(mg, key=lambda k: abs(mg[k])), **mg))
    g = pd.DataFrame(rows)
    P(f"  {'book':<16} | {'A 4b':>5} {'B 4b':>5} {'C 4b':>5} | {'A tightest':>11} "
      f"{'leg':<6} | {'|dSharpe| A-B':>13} {'|dSharpe| A-C':>13} | {'flip?':>6}")
    piv = g.pivot(index="book", columns="arm")
    flips_b = flips_c = 0
    for b in [bb for bb, _ in books]:
        a4, b4, c4 = (bool(piv[("pass4b", x)][b]) for x in ("A_NATIVE", "B_BARSWAP", "C_BOTH"))
        dab = abs(piv[("Sharpe", "A_NATIVE")][b] - piv[("Sharpe", "B_BARSWAP")][b])
        dac = abs(piv[("Sharpe", "A_NATIVE")][b] - piv[("Sharpe", "C_BOTH")][b])
        fl = (a4 != b4) or (a4 != c4)
        flips_b += int(a4 != b4)
        flips_c += int(a4 != c4)
        P(f"  {b:<16} | {str(a4):>5} {str(b4):>5} {str(c4):>5} | "
          f"{piv[('tightest', 'A_NATIVE')][b]:>11.3e} {piv[('tightest_leg', 'A_NATIVE')][b]:<6} | "
          f"{dab:>13.3e} {dac:>13.3e} | {str(fl):>6}")
    P(f"  4b verdict flips A->B (COMPARAND channel only) : {flips_b} / {len(books)}")
    P(f"  4b verdict flips A->C (BOTH channels)          : {flips_c} / {len(books)}")
    P(f"  4b passes: A {int(g[g.arm == 'A_NATIVE'].pass4b.sum())}/{len(books)}   "
      f"B {int(g[g.arm == 'B_BARSWAP'].pass4b.sum())}/{len(books)}   "
      f"C {int(g[g.arm == 'C_BOTH'].pass4b.sum())}/{len(books)}")
    P(f"  4a passes: A {int(g[g.arm == 'A_NATIVE'].pass4a.sum())}/{len(books)}   "
      f"B {int(g[g.arm == 'B_BARSWAP'].pass4a.sum())}/{len(books)}   "
      f"C {int(g[g.arm == 'C_BOTH'].pass4a.sum())}/{len(books)}")
    P(f"  smallest tightest-margin over all 24 books (arm A): "
      f"{g[g.arm == 'A_NATIVE'].tightest.min():.3e}  vs bar shift {BARSHIFT:.3e}  "
      f"({g[g.arm == 'A_NATIVE'].tightest.min() / BARSHIFT:,.0f}x)")
    P(f"  BOOK channel size: max |Sharpe(A) - Sharpe(C)| over 24 books = "
      f"{max(abs(piv[('Sharpe', 'A_NATIVE')][b] - piv[('Sharpe', 'C_BOTH')][b]) for b, _ in books):.3e}")
    dump(g, "grid")

    # ---------------------------------------------------------------- rule 8
    P("=" * 100)
    P("(F) PROTOCOL RULE 8 -- one book per arm chosen on IS (<= 2016-12-31), 2017-2026 ONCE")
    P("=" * 100)
    wf = []
    for aname in arms:
        sub = g[g.arm == aname].sort_values(["IS_Sharpe", "book"], ascending=[False, True])
        r = sub.iloc[0]
        wf.append(dict(arm=aname, pick=r.book, IS_Sharpe=r.IS_Sharpe, OOS_CAGR=r.OOS_CAGR,
                       OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                       SPY_OOS_Sharpe=r.SPY_OOS_Sharpe, CAGR=r.CAGR, Sharpe=r.Sharpe,
                       MaxDD=r.MaxDD, H1=r.H1, H2=r.H2, pass4a=bool(r.pass4a),
                       pass4b=bool(r.pass4b), tightest=r.tightest, tightest_leg=r.tightest_leg))
        P(f"  {aname:<10} pick {r.book:<16} IS Sharpe {r.IS_Sharpe:.4f} | OOS CAGR {r.OOS_CAGR:7.2%} "
          f"Sharpe {r.OOS_Sharpe:.4f} MaxDD {r.OOS_MaxDD:7.2%} | SPY OOS {r.SPY_OOS_Sharpe:.4f} "
          f"| 4a {bool(r.pass4a)} 4b {bool(r.pass4b)} tightest {r.tightest:.3e} ({r.tightest_leg})")
    wfd = pd.DataFrame(wf)
    same = wfd["pick"].nunique() == 1
    P(f"  ALL THREE ARMS PICK THE SAME BOOK: {same}")
    dump(wfd, "walkforward")

    # ---------------------------------------------------------------- cost appendix
    P("=" * 100)
    P("(G) LABELLED ROBUSTNESS -- cost appendix (NO verdict is taken from this table)")
    P("=" * 100)
    app = []
    for cst in COSTS_APPENDIX:
        for aname, (panel, spyser) in arms.items():
            sr = spyser.pct_change().fillna(0).loc[st:]
            ms, spy_oos = M(sr), M0(sr.loc[OOS_START:])
            for bname, fn in books:
                r = fast_backtest(panel, fn(panel), FREQ, cst).loc[st:]
                m = M(r)
                mg = margins(m, M0(r.loc[OOS_START:]), ms, spy_oos)
                app.append(dict(cost_bps=cst, arm=aname, book=bname, pass4b=pass4b(mg),
                                tightest=min(abs(v) for v in mg.values())))
    ap = pd.DataFrame(app)
    for cst in COSTS_APPENDIX:
        s = ap[ap.cost_bps == cst].pivot(index="book", columns="arm", values="pass4b")
        fb = int((s["A_NATIVE"] != s["B_BARSWAP"]).sum())
        fc = int((s["A_NATIVE"] != s["C_BOTH"]).sum())
        P(f"  {cst:>5.1f} bps: 4b passes A {int(s['A_NATIVE'].sum())}/{len(s)}  "
          f"flips A->B {fb}  A->C {fc}  min tightest "
          f"{ap[(ap.cost_bps == cst) & (ap.arm == 'A_NATIVE')].tightest.min():.3e}")
    dump(ap, "costappendix")

    P("=" * 100)
    P("(H) SURVIVORSHIP CAVEAT (PROTOCOL 9)")
    P("=" * 100)
    P("  B136 is today's constituents (research/universe_broad.json): names acquired, delisted")
    P("  or dropped from the index are absent, so every LEVEL above is biased upward and none is")
    P("  a tradeable estimate.  The headline here is a DIFFERENCE between two readings of the")
    P("  same 24 books on the same days, to which the bias applies identically on both sides.")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
