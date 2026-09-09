#!/usr/bin/env python3
"""Idea 575 (lane C, 2026-09-09) - can-SMALL439-clear-a-4b-SHARPE-leg-under-ANY-unlevered-book-form.

QUESTION
--------
Idea 311 swept the gross scalar g on six pre-registered unlevered book-forms (EWall, MA-RS,
MA-DG, TOP20, TOP10, MA20) x three panels x two cadences and found that on SMALL439 EVERY
cell's admissible 4b band is empty for reason SHARPE: at least one of the three Sharpe legs
(H1 > SPY_H1, H2 > SPY_H2, OOS > SPY_OOS) fails at EVERY gross.  Because Sharpe is g-invariant
on a gross-scalar book, that is not a dial question - no placement of g can rescue it.

This run asks whether the failure is a property of the SMALL PANEL or only of that six-form
menu.  It widens the form menu the queue named - vol-target, trend+trim, sector-capped, and
n in 5..60 - and asks: does ANY unlevered small-panel book clear H1, H2 and OOS against SPY?

TUNED PARAMETERS (PROTOCOL rule 4, exactly two): the book FORM family and its size dial n
(for VT the dial is the vol target; it is the same axis slot).  Gross is NOT a third dial:
G3 re-establishes on this panel that the three Sharpe legs are invariant in g, so the whole
menu is screened at a single fixed g = 0.75 and g is only re-opened (17-point ladder) for a
book that has already cleared all three Sharpe legs.  Cadence (W, M) is a reported axis:
every grid point of it is written to .grid.csv.

PRE-REGISTERED HYPOTHESES (written before any book was run)
-----------------------------------------------------------
H_MAIN    : NO book in the widened menu clears all three Sharpe legs on SMALL439.  This is
            the queue's question stated as the null; a single passer refutes it.
H_GINVAR  : on SMALL439 the Sharpe span across g in [0.20, 1.00] is <= 0.0100 for every form
            in the g-gate, i.e. idea 311's invariance carries to the widened menu's families.
            If this fails the single-g screen is not licensed and the run stops there.
H_DEFENS  : if any leg is cleared it will be by a DEFENSIVE form (LOWVOL, IVOL, VT), not by a
            concentrated momentum form - i.e. the small panel's problem is volatility, not
            direction.  Scored as: the best H1/H2/OOS Sharpe margin vs SPY over the menu is
            attained by a defensive family.
H_NARROW  : the binding leg is not the same one everywhere - at least two DIFFERENT Sharpe
            legs are the sole survivor-blocker somewhere in the menu (if one single leg fails
            in 100% of cells, the panel fails for one regime-specific reason, not broadly).
H_4A      : no book clears PROTOCOL 4a either (Sharpe > RULES v2 in BOTH halves with MaxDD no
            worse), so the widened menu does not rescue the panel on the live-book path.

Rule 8 (walk-forward, required, run regardless of verdict): (form, n) is chosen on 2010-2016
ONLY by IS Sharpe over the SAME menu, and 2017-2026 is then read ONCE - reporting OOS
CAGR/Sharpe/MaxDD against the RULES v2 baseline run on the same panel and against SPY.  A
second, stricter selector (best IS Sharpe among books that clear both IS half-legs) is also
carried, because the IS-Sharpe-max book is the one an overfitter would pick.

Costs 10 bps per unit turnover, weights decided at close t and applied t+1 (engine convention),
no shorting, no leverage (gross <= 1.00 everywhere, VT scales gross DOWN only).

SURVIVORSHIP: the small panel is TODAY's sub-$2B screen - current constituents only, so every
level here is biased UP relative to what was investable in 2010.  Names with max_1d_move >= 1.0
in data/small_meta.csv are dropped first, per the record's convention.  The SIC map used by the
SECT form is read from research/deepvalue/universe_under2b.csv, which idea 565 showed is
rewritten nightly; the exact mapping this run used is snapshotted to .sicmap.csv.

GATES (all must pass before any finding is read)
------------------------------------------------
G1  fast_backtest == engine.backtest on a real book of this panel (returns AND turnover).
G2  idea 311's twelve committed SMALL439 rows at g=0.75 (6 forms x 2 cadences) reproduce.
G3  H_GINVAR's g-invariance is measured, not assumed, on this panel.
"""
import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa

STAMP = Path(__file__).name[:-3]
OUT = Path(__file__).resolve().parent
COST = 10.0
MA_WIN = 200
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PANEL_END = "2026-09-04"           # idea 311's PARENT_END, so G2 is comparable
CADENCES = ["W", "M"]
GFIX = 0.75
GGRID = [round(0.20 + 0.05 * i, 2) for i in range(17)]
PARENT = "2026-09-09_does-4b-discriminate-ANYTHING-on-gross-scalar-books_cloud.grid.csv"
G1_TOL, G2_TOL = 1e-12, 1e-9
INVAR_BAR = 0.0100
NGRID = [5, 10, 15, 20, 30, 40, 60]
VTARGETS = [0.08, 0.10, 0.12, 0.15, 0.20]
SECT_CAP = 3                        # names per SIC major group; FIXED, not tuned
TRIM_Q = 0.80                       # trend+trim drops names above this vol pctile; FIXED
VOL_WIN = 60                        # vol windows for LOWVOL / IVOL / VT; FIXED
WARM = 260                          # warm-up rows skipped before ANY metric (idea 311/baseline.compare)

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ vectorised runner
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Vectorised equivalent of engine.backtest (asserted in G1).  Idea 311/312's runner."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
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
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


# ------------------------------------------------------------------------- helpers
def _priced(px, tradable):
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    cols = [c for c in px.columns if c in tradable]
    e[cols] = px[cols].notna().astype(float)
    return e


def _ew(mask, g):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.div(n, axis=0).fillna(0.0)


def above_ma(px, win=MA_WIN):
    return px > px.rolling(win).mean()


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def rowify(r, tn=None):
    m = metrics(r)
    h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])
    if tn is not None:
        d["turnover"] = float(tn.sum() / m["Years"])
    return d


def legs_4b(r, spy):
    """PROTOCOL 4b's five legs on the full sample (OOS leg = post-2017 Sharpe)."""
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    return dict(H1=bool(a1 > s1), H2=bool(a2 > s2),
                OOS=bool(metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]),
                DD=bool(m["MaxDD"] >= 0.60 * ms["MaxDD"]),
                CAGR=bool(m["CAGR"] >= 0.70 * ms["CAGR"]))


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def fail_str(lg):
    f = [k for k, v in lg.items() if not v]
    return ",".join(f) if f else "-"


# ------------------------------------------------------------------------- the panel
def load_small():
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    px = pxs[stk + ["SPY"]].dropna(how="all").ffill().loc[:PANEL_END]
    return px, set(stk)


def sic_groups(tradable):
    """ticker -> SIC 2-digit major group ('UNK' when the filings file has no row)."""
    u = pd.read_csv(ROOT / "research" / "deepvalue" / "universe_under2b.csv").dropna(subset=["ticker"])
    m = {}
    for t, s in zip(u["ticker"], u["sic"]):
        if t in tradable and pd.notna(s):
            m.setdefault(t, f"{int(s) // 100:02d}")
    return {t: m.get(t, "UNK") for t in sorted(tradable)}


# ------------------------------------------------------- the WIDENED book-form menu
def form_weights(fam, n, px, tradable, g, ctx):
    """Unlevered book forms.  fam is the family, n its size dial (vol target for VT).

    EWall   every priced tradable name, equal weight at gross g          (NO-EDGE CONTROL)
    MA-RS   200d gate, re-spread over survivors at gross g               (idea 311 anchor)
    MA-DG   200d gate, de-grossed: gated-out weight goes to CASH         (idea 311 anchor)
    TOP     top n by the RULES composite (vol_scale=False), equal weight  (ranked)
    MA      200d gate INTERSECT top n by the same score                   (gate + ranked)
    LOWVOL  the n LOWEST 60d-vol names among the 200d-gate survivors      (defensive)
    IVOL    gate INTERSECT top n, weighted 1/vol60 instead of equally     (defensive weights)
    TRIM    gate INTERSECT top n, then DROP names whose vol60 is above    (trend + trim)
            the day's 80th cross-sectional percentile
    SECT    top n by score subject to at most SECT_CAP names per SIC      (sector-capped)
            major group, filled greedily best-score-first
    VT      MA-RS vol-targeted: gross g * min(1, n / realised 60d vol of  (vol-target,
            the ungeared MA-RS book, lagged one day) - scales DOWN only    unlevered)
    """
    e = _priced(px, tradable) > 0
    if fam == "EWall":
        return _ew(e, g)
    ma = above_ma(px) & e
    if fam == "MA-RS":
        return _ew(ma, g)
    if fam == "MA-DG":
        den = e.sum(axis=1).replace(0, np.nan)
        return g * ma.astype(float).div(den, axis=0).fillna(0.0)
    s, vol = ctx["score"], ctx["vol"]
    if fam == "TOP":
        return _ew(s.where(e).rank(axis=1, ascending=False) <= n, g)
    if fam == "MA":
        return _ew(s.where(ma).rank(axis=1, ascending=False) <= n, g)
    if fam == "LOWVOL":
        return _ew(vol.where(ma).rank(axis=1, ascending=True) <= n, g)
    if fam == "IVOL":
        sel = s.where(ma).rank(axis=1, ascending=False) <= n
        iv = (1.0 / vol.clip(lower=0.05)).where(sel).fillna(0.0)
        return g * iv.div(iv.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    if fam == "TRIM":
        sel = s.where(ma).rank(axis=1, ascending=False) <= n
        cut = vol.where(e).quantile(TRIM_Q, axis=1)
        return _ew(sel & vol.le(cut, axis=0), g)
    if fam == "SECT":
        return _ew(ctx["sect_masks"][n], g)
    if fam == "VT":
        base = _ew(ma, 1.0)
        rb = fast_backtest(px, base, cost_bps=0.0, freq="D")["returns"]
        rv = (rb.rolling(VOL_WIN).std() * np.sqrt(252)).shift(1)
        sc = (n / rv.clip(lower=1e-6)).clip(upper=1.0).fillna(0.0)
        return _ew(ma, g).mul(sc, axis=0)
    raise ValueError(fam)


def sector_capped_mask(s, e, groups, n, cap=SECT_CAP):
    """Greedy: walk names best-score-first, take one while its SIC group has < cap taken,
    stop at n.  Vectorised over time by ranking WITHIN group first (the k-th best name of a
    group is admissible only if k <= cap), then taking the top n of what remains."""
    sc = s.where(e)
    g = pd.Series(groups)
    out = pd.DataFrame(False, index=sc.index, columns=sc.columns)
    within = pd.DataFrame(np.nan, index=sc.index, columns=sc.columns)
    for grp, cols in g.groupby(g).groups.items():
        cols = [c for c in cols if c in sc.columns]
        within[cols] = sc[cols].rank(axis=1, ascending=False)
    elig = sc.where(within <= cap)
    out = elig.rank(axis=1, ascending=False) <= n
    return out


def menu(groups):
    """The pre-registered (family, n) menu.  n is None for the three fixed anchors."""
    bl = [("EWall", None), ("MA-RS", None), ("MA-DG", None)]
    for fam in ("TOP", "MA", "LOWVOL", "IVOL", "TRIM", "SECT"):
        bl += [(fam, n) for n in NGRID]
    bl += [("VT", t) for t in VTARGETS]
    return bl


def label(fam, n):
    return fam if n is None else f"{fam}{n}" if fam != "VT" else f"VT{int(round(n * 100))}"


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 116)
    P("IDEA 575  can-SMALL439-clear-a-4b-SHARPE-leg-under-ANY-unlevered-book-form  (lane C, 2026-09-09)")
    P("=" * 116)
    P("Idea 311: every SMALL439 cell's 4b band is empty for reason SHARPE at EVERY gross on six")
    P("forms.  Widen the menu (vol-target, trend+trim, sector-capped, n in 5-60) and ask whether")
    P("ANY unlevered small-panel book clears H1, H2 and OOS against SPY.")
    P("Tuned: FORM family x size dial n (2 params).  Gross fixed at 0.75 for the screen (G3),")
    P("re-opened on a 17-point ladder only for a book that clears all three Sharpe legs.")
    P("SURVIVORSHIP: current sub-$2B constituents only - every level below is biased UP.")
    P("")

    px, tradable = load_small()
    stk = sorted(tradable)
    P(f"panel: {len(stk)} tradable names + SPY, {px.index[0].date()} .. {px.index[-1].date()}, "
      f"{len(px)} rows")
    groups = sic_groups(tradable)
    ng = len(set(groups.values()))
    unk = sum(1 for v in groups.values() if v == "UNK")
    P(f"SIC map: {ng} major groups, {unk} names UNK (no filings row); cap {SECT_CAP}/group")
    pd.DataFrame({"ticker": list(groups), "sic2": list(groups.values())}).to_csv(
        OUT / f"{STAMP}.sicmap.csv", index=False)

    ST = px.index[WARM]                      # warm-up skip, idea 311/baseline.compare convention
    spy = px["SPY"].pct_change().fillna(0.0).loc[ST:]
    sc, _, _ = score(px, vol_scale=False)
    vol = px.pct_change().rolling(VOL_WIN).std() * np.sqrt(252)
    ctx = {"score": sc, "vol": vol,
           "sect_masks": {n: sector_capped_mask(sc, _priced(px, tradable) > 0, groups, n)
                          for n in NGRID}}

    # -------------------------------------------------------------------------- gates
    P("-" * 116)
    P("GATES")
    P("-" * 116)
    wtest = form_weights("MA", 20, px, tradable, GFIX, ctx)
    a = fast_backtest(px, wtest, freq="W")
    b = backtest(px, wtest, cost_bps=COST, freq="W")
    d_r = float((a["returns"] - b["returns"]).abs().max())
    d_t = float((a["turnover"] - b["turnover"]).abs().max())
    P(f"G1 fast_backtest == engine.backtest on MA20/W : max|dret| {d_r:.3e}  max|dturn| {d_t:.3e}"
      f"  -> {'PASS' if max(d_r, d_t) < G1_TOL else 'FAIL'}")
    assert max(d_r, d_t) < G1_TOL, "G1"

    par = pd.read_csv(OUT / PARENT)
    par = par[par.panel.astype(str).str.startswith("SMALL") & (par.gross == GFIX)]
    anchor = {"EWall": ("EWall", None), "MA-RS": ("MA-RS", None), "MA-DG": ("MA-DG", None),
              "TOP20": ("TOP", 20), "TOP10": ("TOP", 10), "MA20": ("MA", 20)}
    dmax, nrep = 0.0, 0
    for _, pr in par.iterrows():
        fam, n = anchor[pr["form"]]
        w = form_weights(fam, n, px, tradable, GFIX, ctx)
        r = fast_backtest(px, w, freq=pr["cadence"])["returns"].loc[ST:]
        m = rowify(r)
        for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"):
            dmax = max(dmax, abs(m[k] - float(pr[k])))
        nrep += 1
    P(f"G2 idea 311's {nrep} committed SMALL439 g=0.75 rows reproduce : max|d| {dmax:.3e}"
      f"  -> {'PASS' if dmax < G2_TOL else 'FAIL'}")
    assert dmax < G2_TOL, "G2"

    ginv = []
    for fam, n in (("EWall", None), ("MA", 20), ("LOWVOL", 20), ("IVOL", 20), ("VT", 0.10)):
        sh = []
        for g in (0.20, 0.40, 0.60, 0.80, 1.00):
            r = fast_backtest(px, form_weights(fam, n, px, tradable, g, ctx), freq="W")["returns"].loc[ST:]
            sh.append(metrics(r)["Sharpe"])
        span = max(sh) - min(sh)
        ginv.append(dict(form=label(fam, n), span=span, lo=min(sh), hi=max(sh)))
        P(f"G3 Sharpe span in g, {label(fam, n):<8}: {span:.4f}  ({min(sh):.4f} .. {max(sh):.4f})")
    gmax = max(x["span"] for x in ginv)
    P(f"G3 max Sharpe span across g = {gmax:.4f} vs bar {INVAR_BAR:.4f}"
      f"  -> H_GINVAR {'PASS' if gmax <= INVAR_BAR else 'FAIL'}")
    pd.DataFrame(ginv).to_csv(OUT / f"{STAMP}.ginvar.csv", index=False)
    assert gmax <= INVAR_BAR, "H_GINVAR failed - the single-g screen is not licensed"
    P("")

    # ------------------------------------------------------------------------- the bar
    P("-" * 116)
    P("THE BAR (SPY on this panel's trading days)")
    P("-" * 116)
    ms, s1, s2 = metrics(spy), *halves(spy)
    mso = metrics(spy.loc[OOS_START:])
    msi = metrics(spy.loc[:IS_END])
    P(f"SPY  CAGR {ms['CAGR']:.4f}  Sharpe {ms['Sharpe']:.4f}  MaxDD {ms['MaxDD']:.4f}"
      f"  H1 {s1:.4f}  H2 {s2:.4f}  IS_Sharpe {msi['Sharpe']:.4f}  OOS_Sharpe {mso['Sharpe']:.4f}")
    P(f"4b bars: H1 > {s1:.4f}, H2 > {s2:.4f}, OOS > {mso['Sharpe']:.4f}, "
      f"MaxDD >= {0.60 * ms['MaxDD']:.4f}, CAGR >= {0.70 * ms['CAGR']:.4f}")
    bw = rules_v2_weights(px[stk])
    bwf = bw.reindex(columns=px.columns).fillna(0.0)
    base = {c: fast_backtest(px, bwf, freq=c)["returns"].loc[ST:] for c in CADENCES}
    for c in CADENCES:
        m = metrics(base[c]); b1, b2 = halves(base[c])
        P(f"RULES v2 baseline on this panel, cadence {c}: CAGR {m['CAGR']:.4f}  Sharpe {m['Sharpe']:.4f}"
          f"  MaxDD {m['MaxDD']:.4f}  H1 {b1:.4f}  H2 {b2:.4f}")
    P("")

    # ---------------------------------------------------------------------- the sweep
    P("-" * 116)
    P("A  THE WIDENED MENU  (every grid point; gross fixed 0.75)")
    P("-" * 116)
    books = menu(groups)
    rows = []
    for fam, n in books:
        w = form_weights(fam, n, px, tradable, GFIX, ctx)
        for cad in CADENCES:
            res = fast_backtest(px, w, freq=cad)
            r = res["returns"].loc[ST:]
            d = rowify(r, res["turnover"].loc[ST:])
            lg = legs_4b(r, spy)
            d.update(form=label(fam, n), family=fam, n=(np.nan if n is None else n), cadence=cad,
                     gross=GFIX,
                     **{f"L_{k}": v for k, v in lg.items()},
                     fail4b=fail_str(lg),
                     keep4b=all(lg.values()),
                     sharpe3=all(lg[k] for k in ("H1", "H2", "OOS")),
                     keep4a=keep_4a(r, base[cad]),
                     dH1=d["H1"] - s1, dH2=d["H2"] - s2,
                     dOOS=d["OOS_Sharpe"] - mso["Sharpe"])
            rows.append(d)
    grid = pd.DataFrame(rows)
    cols = ["form", "family", "n", "cadence", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "IS_Sharpe", "IS_CAGR", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "turnover",
            "dH1", "dH2", "dOOS", "L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR", "fail4b", "sharpe3",
            "keep4b", "keep4a"]
    grid = grid[cols]
    grid.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    P(f"{len(grid)} grid points = {len(books)} books x {len(CADENCES)} cadences.  ALL written to .grid.csv")
    P("")
    show = grid.copy()
    P(show.to_string(index=False, float_format=lambda x: f"{x:.4f}",
                     columns=["form", "cadence", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                              "OOS_Sharpe", "dH1", "dH2", "dOOS", "fail4b", "sharpe3", "keep4b",
                              "keep4a"]))
    P("")

    # -------------------------------------------------------------------- the verdict
    P("-" * 116)
    P("B  THE LEGS")
    P("-" * 116)
    npass3 = int(grid.sharpe3.sum())
    P(f"H_MAIN  books clearing ALL THREE Sharpe legs (H1, H2, OOS vs SPY): {npass3} / {len(grid)}"
      f"  -> H_MAIN {'HOLDS (no passer)' if npass3 == 0 else 'REFUTED'}")
    for leg in ("H1", "H2", "OOS"):
        k = int((~grid[f"L_{leg}"]).sum())
        P(f"   leg {leg:<3} fails in {k:>3} / {len(grid)} cells ({k / len(grid):.1%});"
          f"  best margin vs SPY {grid['d' + leg].max():+.4f} at {grid.loc[grid['d' + leg].idxmax(), 'form']}"
          f" ({grid.loc[grid['d' + leg].idxmax(), 'cadence']})")
    solo = {}
    for _, r_ in grid.iterrows():
        f = [k for k in ("H1", "H2", "OOS") if not r_[f"L_{k}"]]
        if len(f) == 1:
            solo[f[0]] = solo.get(f[0], 0) + 1
    P(f"H_NARROW  cells blocked by exactly ONE Sharpe leg, by leg: {solo if solo else '{}'}"
      f"  -> {'PASS' if len(solo) >= 2 else 'FAIL'} (>= 2 distinct legs)")
    DEF = {"LOWVOL", "IVOL", "VT", "MA-DG", "TRIM"}
    best = {leg: grid.loc[grid["d" + leg].idxmax()] for leg in ("H1", "H2", "OOS")}
    ndef = sum(1 for leg in best if best[leg]["family"] in DEF)
    P(f"H_DEFENS  best margin on a defensive family in {ndef} / 3 legs"
      f"  -> {'PASS' if ndef >= 2 else 'FAIL'}")
    n4a = int(grid.keep4a.sum())
    P(f"H_4A  books clearing PROTOCOL 4a vs RULES v2 on this panel: {n4a} / {len(grid)}"
      f"  -> H_4A {'HOLDS' if n4a == 0 else 'REFUTED'}")
    if n4a:
        P(grid[grid.keep4a].to_string(index=False, float_format=lambda x: f"{x:.4f}",
                                      columns=["form", "cadence", "CAGR", "Sharpe", "MaxDD",
                                               "H1", "H2", "fail4b"]))
    P(f"4b passers (all five legs): {int(grid.keep4b.sum())} / {len(grid)}")
    P("")

    # ------------------------------------------- gross ladder for any Sharpe-leg passer
    band = []
    for _, r_ in grid[grid.sharpe3].iterrows():
        fam, n = r_["family"], (None if pd.isna(r_["n"]) else
                                (r_["n"] if fam == "VT" else int(r_["n"])))
        for g in GGRID:
            rr = fast_backtest(px, form_weights(fam, n, px, tradable, g, ctx),
                               freq=r_["cadence"])["returns"].loc[ST:]
            lg = legs_4b(rr, spy)
            m = rowify(rr)
            band.append(dict(form=r_["form"], cadence=r_["cadence"], gross=g, **m,
                             **{f"L_{k}": v for k, v in lg.items()},
                             keep4b=all(lg.values()), fail4b=fail_str(lg)))
    if band:
        bdf = pd.DataFrame(band)
        bdf.to_csv(OUT / f"{STAMP}.band.csv", index=False)
        P("-" * 116)
        P("C  GROSS LADDER for the Sharpe-leg passers (17 points each)")
        P("-" * 116)
        P(bdf.to_string(index=False, float_format=lambda x: f"{x:.4f}",
                        columns=["form", "cadence", "gross", "CAGR", "Sharpe", "MaxDD",
                                 "keep4b", "fail4b"]))
        for (f_, c_), sub in bdf.groupby(["form", "cadence"]):
            ok = sub[sub.keep4b]
            P(f"   {f_}/{c_}: admissible 4b g-band "
              f"{'[' + f'{ok.gross.min():.2f}, {ok.gross.max():.2f}' + ']' if len(ok) else 'EMPTY'}"
              f"  ({len(ok)}/{len(sub)} points)")
    else:
        P("C  GROSS LADDER skipped: no book cleared all three Sharpe legs, and the legs are")
        P("   g-invariant (G3), so no placement of gross can create a passer.")
    P("")

    # ------------------------------------------------------------ rule 8 walk-forward
    P("-" * 116)
    P("D  RULE 8 WALK-FORWARD  (form and n chosen on 2010-2016 only; 2017-2026 read once)")
    P("-" * 116)
    wf = []
    for cad in CADENCES:
        sub = grid[grid.cadence == cad].copy()
        pick = sub.loc[sub.IS_Sharpe.idxmax()]
        ish1 = []
        for _, r_ in sub.iterrows():
            fam, n = r_["family"], (None if pd.isna(r_["n"]) else
                                    (r_["n"] if fam == "VT" else int(r_["n"])))
            rr = fast_backtest(px, form_weights(fam, n, px, tradable, GFIX, ctx),
                               freq=cad)["returns"].loc[ST:IS_END]
            a1, a2 = halves(rr)
            b1, b2 = halves(spy.loc[:IS_END])
            ish1.append(bool(a1 > b1 and a2 > b2))
        sub["IS_half_legs"] = ish1
        strict = sub[sub.IS_half_legs]
        pick2 = strict.loc[strict.IS_Sharpe.idxmax()] if len(strict) else None
        for tag, p_ in (("IS-Sharpe-max", pick), ("IS-Sharpe-max|IS-halves", pick2)):
            if p_ is None:
                P(f"   {cad} {tag}: no book clears both IS half-legs - selector empty")
                continue
            bm = metrics(base[cad].loc[OOS_START:]); bmh = metrics(base[cad])
            wf.append(dict(cadence=cad, selector=tag, form=p_["form"],
                           IS_Sharpe=p_["IS_Sharpe"], IS_CAGR=p_["IS_CAGR"], IS_MaxDD=p_["IS_MaxDD"],
                           OOS_CAGR=p_["OOS_CAGR"], OOS_Sharpe=p_["OOS_Sharpe"],
                           OOS_MaxDD=p_["OOS_MaxDD"],
                           base_OOS_CAGR=bm["CAGR"], base_OOS_Sharpe=bm["Sharpe"],
                           base_OOS_MaxDD=bm["MaxDD"],
                           spy_OOS_CAGR=mso["CAGR"], spy_OOS_Sharpe=mso["Sharpe"],
                           spy_OOS_MaxDD=mso["MaxDD"],
                           beats_base=bool(p_["OOS_Sharpe"] > bm["Sharpe"]),
                           beats_spy=bool(p_["OOS_Sharpe"] > mso["Sharpe"])))
            P(f"   {cad} {tag:<24} -> {p_['form']:<8}  IS Sharpe {p_['IS_Sharpe']:.4f}"
              f" | OOS CAGR {p_['OOS_CAGR']:.4f} Sharpe {p_['OOS_Sharpe']:.4f} MaxDD {p_['OOS_MaxDD']:.4f}"
              f" | base OOS Sharpe {bm['Sharpe']:.4f} | SPY OOS Sharpe {mso['Sharpe']:.4f}"
              f" -> {'beats SPY' if p_['OOS_Sharpe'] > mso['Sharpe'] else 'loses to SPY'}")
        sub.to_csv(OUT / f"{STAMP}.wf_{cad}.csv", index=False)
    pd.DataFrame(wf).to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    P("")
    P("-" * 116)
    P(f"VERDICT: {'KILL' if npass3 == 0 and n4a == 0 else 'SEE ABOVE'} - "
      f"{npass3}/{len(grid)} books clear the three 4b Sharpe legs, {n4a}/{len(grid)} clear 4a.")
    P(f"elapsed {time.time() - t0:.1f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
