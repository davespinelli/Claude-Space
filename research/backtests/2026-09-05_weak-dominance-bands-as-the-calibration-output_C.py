#!/usr/bin/env python3
"""QUEUE idea 145 — weak-dominance-bands-as-the-calibration-output  (research sprint lane C, 2026-09-05)

QUESTION (pre-registered, from QUEUE.md idea 145)
    Idea 131 found that gamma in [0.57, 0.61] WEAKLY DOMINATES 4b's published CAGR floor on
    all three of the floor's own criteria (loses none of its 29 admissions, saves 6-8 of its
    victims, admits 5-9 static-gross ladder points against the floor's 10).  No single-number
    report would have surfaced that: the published constant is a POINT, and the object that
    actually exists is a BAND.  Ideas 128 and 90 asked PROTOCOL to quote plateau width and
    interval width beside every adopted DIAL.  Idea 145 is the same request for the BARS.

    Q1  Reproduce ideas 129/131's corpus exactly, so the bands are derived on the same rows.
    Q2  For EVERY bar 4b states — the two halves Sharpe bars (sigma1, sigma2), the OOS Sharpe
        bar (sigmaO), the drawdown cap (delta) and the CAGR floor (phi) — derive
          (i)   the INDIFFERENCE band: the maximal interval of the coefficient over which the
                admitted set AND the ladder-leakage count are IDENTICAL to the published point;
          (ii)  the WEAK-DOMINANCE band: coefficients that lose none of the published
                admissions AND admit no more ladder points than the published point;
          (iii) the STRICT-DOMINANCE region, if any: weak dominance plus a strict improvement
                on one of the two remaining criteria (Pareto-best victims saved, or ladder
                points excluded).
        A published point that sits strictly inside its own weak-dominance band is fine and the
        band is a robustness statement.  A published point that is STRICTLY DOMINATED by
        another value of its own coefficient is a calibration error, and is reported as one.
    Q3  Are the bands separable?  Re-derive the phi band at every delta and the delta band at
        every phi (the one pair idea 129 already published), and report the 2-D map.
    Q4  Rule 8.  Re-derive every band on the IS window (2009-2016) ALONE, read OOS once:
        does the IS band contain the published point, does it contain the full-sample band,
        and does moving a coefficient inside its own IS band change the OOS pick or its
        OOS CAGR / Sharpe / MaxDD against RULES v1 and SPY?
    Q5  Both KEEP paths (4a and 4b) counted on all 306 rows at the published point and at
        every band edge.

    This script adjudicates BARS.  It proposes no book and can promote nothing: a "KEEP" here
    would be a proposal about PROTOCOL's wording, not about capital.  Rule 7 stands — no
    coefficient is moved to make anything pass, and every grid point is printed.

HARNESS
    Idea 94's script (`2026-09-04_drawdown-insurance-price-list_B.py`) is IMPORTED, and ideas
    129/131's corpus construction is reproduced EXACTLY.  Four reproduction checks run before
    any new number is read:
      (a) H.run vs engine.backtest on the ungated EWall u56 book — must be exact;
      (b) idea 94's published EWall+vol60-dg u56 @10bps row (11.6% / 1.133 / -16.9%);
      (c) idea 129's census (306 rows / 82 Pareto / 29 pass 4b / 27 floor-only / 11 of 23 on
          the frontier / 342 ladder rows / 97 ladder floor-only, all at m <= 0.80);
      (d) idea 129's IS-screen groups A/B/C = 45/9/252, and idea 131's ladder0 = 10.

CORPUS (nothing new is invented)
    3 panels (u56, broad, small) x 3 books (V1u, TOP20, EWall) x 17 arms x 2 cost rungs
    = 306 arm-rows, plus a 19-point static-gross ladder per cell = 342 reference rows.
    Weekly, t+1 execution, 75% target gross, 10 and 25 bps, IS <= 2016-12-31, OOS >= 2017.

BAR PARAMETERISATION (PROTOCOL 4b, written with its coefficients exposed)
    H1  :  Sharpe_H1  >  sigma1 * SPY_H1        sigma1 = 1.00  (published)
    H2  :  Sharpe_H2  >  sigma2 * SPY_H2        sigma2 = 1.00
    OOS :  Sharpe_OOS >  sigmaO * SPY_OOS       sigmaO = 1.00
    DD  :  |MaxDD|   <=  delta  * |SPY MaxDD|   delta  = 0.60
    CAGR:  CAGR      >=  phi    * SPY CAGR      phi    = 0.70

TUNED PARAMETERS — never more than two at once
    Q2 sweeps ONE coefficient at a time with the other four PINNED at their published values
    (one tuned parameter per sweep).  Q3 is the single two-parameter map (phi x delta), which
    is the pair idea 129 already published.  Q4 re-derives the same one-at-a-time bands on the
    IS window.  All grid points are written to `.bands.csv` / `.pairmap.csv` and the coarse
    grids are printed in full.  Band ENDPOINTS are additionally computed ANALYTICALLY (each
    bar is monotone in its own coefficient, so the admitted set changes only at the finitely
    many per-row crossing values), which makes the reported bands exact rather than grid-
    resolution artefacts.

CAVEATS carried, not buried
    - Survivorship (idea 54): all three panels are current-constituent lists.
    - Idea 128: the IS window's SPY MaxDD is shallower than the OOS window's, so every
      IS-derived drawdown band admits too much; this biases Q4 in one known direction.
    - Idea 38: u56 and broad still carry the calendar-day index.
    - Idea 126: t+1 execution only, no lag band is claimed.
    - The ladder is the only leakage control available (it catches de-grossing, not other ways
      of gaming a drawdown cap), inherited from idea 129.
    - n is small where it matters: 11 Pareto-best floor victims in 4 cells, all EWall, with
      overlapping return series.  Every band is a census of THIS corpus, not an estimate.
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

STEM = "2026-09-05_weak-dominance-bands-as-the-calibration-output_C"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"

_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

FREQ, GROSS, PCOST = H.FREQ, H.GROSS, H.PCOST
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
BOOKS = H.BOOKS
LADDER = H.LADDER
PANELS = ["u56", "broad", "small"]

# published 4b coefficients
PUB = dict(H1=1.00, H2=1.00, OOS=1.00, DD=0.60, CAGR=0.70)
BARS5 = ["H1", "H2", "OOS", "DD", "CAGR"]
# the four bars that are prospectively checkable on an IS window (the OOS bar is not)
BARS_IS = ["H1", "H2", "DD", "CAGR"]

# coarse printed grids (fine analytic endpoints computed separately)
GRIDS = {
    "H1": np.round(np.arange(0.50, 1.501, 0.05), 3),
    "H2": np.round(np.arange(0.50, 1.501, 0.05), 3),
    "OOS": np.round(np.arange(0.50, 1.501, 0.05), 3),
    "DD": np.round(np.arange(0.30, 1.201, 0.05), 3),
    "CAGR": np.round(np.arange(0.00, 1.201, 0.05), 3),
}

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 1500)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ panels (idea 97/118 verbatim)
_PCACHE = {}


def panel(name):
    if name not in _PCACHE:
        _PCACHE[name] = _panel(name)
    return _PCACHE[name]


def _panel(name):
    if name == "u56":
        px = load_universe()
        return px, px["SPY"].pct_change().fillna(0.0), "universe.json(56)"
    if name == "broad":
        px = load_universe(broad=True)
        return px, px["SPY"].pct_change().fillna(0.0), "universe_broad.json(136)"
    if name == "small":
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
        inv = [c for c in px.columns if c != "SPY" and c not in bad]
        return px[inv], px["SPY"].pct_change().fillna(0.0), f"prices_small({len(inv)}, SPY held out)"
    raise ValueError(name)


def bars_win(spy, which):
    """SPY reference numbers for a window (idea 131's bars_win verbatim)."""
    if which == "full":
        s1, s2 = H.halves(spy)
        m = metrics(spy)
        return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                    soos=metrics(spy.loc[OOS_START:])["Sharpe"])
    w = H.window(spy, which)
    s1, s2 = H.halves(w)
    m = metrics(w)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"], soos=m["Sharpe"])


# ------------------------------------------------------------------ raw statistics per row
def raw_stats(r, prefix=""):
    """Everything a bar can be evaluated on, on the FULL window, stored once."""
    h1, h2 = H.halves(r)
    m = metrics(r)
    mo = metrics(r.loc[OOS_START:])
    return {prefix + "CAGR": m["CAGR"], prefix + "Sharpe": m["Sharpe"], prefix + "MaxDD": m["MaxDD"],
            prefix + "H1": h1, prefix + "H2": h2, prefix + "OOSs": mo["Sharpe"]}


def raw_stats_win(r, which):
    """The same five statistics measured INSIDE a window (halves of that window)."""
    w = H.window(r, which)
    h1, h2 = H.halves(w)
    m = metrics(w)
    return dict(H1=h1, H2=h2, OOSs=m["Sharpe"], MaxDD=m["MaxDD"], CAGR=m["CAGR"], Sharpe=m["Sharpe"])


# ------------------------------------------------------------------ bar algebra
def crossings(stats, b):
    """Per-row coefficient value at which each bar flips.  Each bar is monotone in its own
    coefficient, so the admitted set can only change at these values.

      H1 :  passes iff sigma1 <  H1  / SPY_H1     (SPY_H1 > 0)   -> looser = SMALLER sigma
      H2 :  passes iff sigma2 <  H2  / SPY_H2
      OOS:  passes iff sigmaO <  OOS / SPY_OOS
      DD :  passes iff delta  >  |MaxDD| / |SPY_DD|              -> looser = LARGER delta
      CAGR: passes iff phi    <  CAGR / SPY_CAGR                 -> looser = SMALLER phi

    Sign convention is idea 131's `verdict` verbatim: a bar FAILS when its margin is <= 0, so
    every comparison is STRICT and a row sitting exactly on a bar is a failure.
    """
    return dict(H1=stats["H1"] / b["s1"], H2=stats["H2"] / b["s2"], OOS=stats["OOSs"] / b["soos"],
                DD=abs(stats["MaxDD"]) / abs(b["sdd"]), CAGR=stats["CAGR"] / b["scagr"])


# direction in which LOOSENING moves each coefficient: -1 = down, +1 = up
LOOSEN = dict(H1=-1, H2=-1, OOS=-1, DD=+1, CAGR=-1)


def passes(x, bar, c):
    """Does a row with crossing value x[bar] pass `bar` at coefficient c?"""
    if bar == "DD":
        return x < c          # |MaxDD| < delta * |SPY MaxDD|
    return x > c              # Sharpe / CAGR bars: strictly above the coefficient x SPY


def pass_all(X, coef):
    """X: DataFrame of per-row crossing values (columns = BARS5).  Returns boolean Series."""
    ok = pd.Series(True, index=X.index)
    for k in BARS5:
        ok &= passes(X[k], k, coef[k])
    return ok


def pass_all_is(X, coef):
    """The prospectively checkable four-bar version, used by the rule-8 selector."""
    ok = pd.Series(True, index=X.index)
    for k in BARS_IS:
        ok &= passes(X[k], k, coef[k])
    return ok


def fail_set(X, coef):
    """List of failing bars per row."""
    F = pd.DataFrame({k: ~passes(X[k], k, coef[k]) for k in BARS5}, index=X.index)
    return F


def pareto_front(df, s="Sharpe", d="MaxDD"):
    S, D = df[s].values, df[d].values
    out = np.ones(len(df), dtype=bool)
    for i in range(len(df)):
        if not np.isfinite(S[i]) or not np.isfinite(D[i]):
            out[i] = False
            continue
        dom = (S >= S[i]) & (D >= D[i]) & ((S > S[i]) | (D > D[i]))
        out[i] = not dom.any()
    return out


# ------------------------------------------------------------------ one (panel, book, cost) cell
def do_cell(pname, px, spy, book, cost, bfull, bIS, v1_net):
    rows, rets = [], {}
    for arm, kind, kw, (gate, conv) in H.arm_specs():
        W = H.targets(px, book, gate, conv)
        res = H.run(px, W, bps=cost, **kw)
        r = res["r"].loc[spy.index[0]:]
        g = res["gross"].loc[spy.index[0]:]
        rets[arm] = r
        full = raw_stats(r)
        isw = raw_stats_win(r, "IS")
        oosw = raw_stats_win(r, "OOS")
        xf = crossings(full, bfull)
        xi = crossings(isw, bIS)
        rows.append(dict(
            panel=pname, book=book, cost=cost, arm=arm, kind=kind,
            CAGR=full["CAGR"], Sharpe=full["Sharpe"], MaxDD=full["MaxDD"],
            H1=full["H1"], H2=full["H2"], OOS_Sharpe_full=full["OOSs"],
            IS_CAGR=isw["CAGR"], IS_Sharpe=isw["Sharpe"], IS_MaxDD=isw["MaxDD"],
            IS_H1=isw["H1"], IS_H2=isw["H2"],
            OOS_CAGR=oosw["CAGR"], OOS_Sharpe=oosw["Sharpe"], OOS_MaxDD=oosw["MaxDD"],
            x_H1=xf["H1"], x_H2=xf["H2"], x_OOS=xf["OOS"], x_DD=xf["DD"], x_CAGR=xf["CAGR"],
            xi_H1=xi["H1"], xi_H2=xi["H2"], xi_OOS=xi["OOS"], xi_DD=xi["DD"], xi_CAGR=xi["CAGR"],
            pass4a=H.pass4a(r, v1_net),
            gross=float(g.mean()),
            TO=float(res["to"].loc[spy.index[0]:].sum() / (len(r) / 252)),
        ))
    D = pd.DataFrame(rows)
    D["pareto"] = pareto_front(D)
    return D, rets


def ladder_cell(pname, px, spy, book, cost, bfull):
    W = H.targets(px, book)
    rows = []
    for m_ in LADDER:
        res = H.run(px, W, m=m_, bps=cost)
        r = res["r"].loc[spy.index[0]:]
        g = res["gross"].loc[spy.index[0]:]
        full = raw_stats(r)
        xf = crossings(full, bfull)
        rows.append(dict(panel=pname, book=book, cost=cost, m=float(m_),
                         CAGR=full["CAGR"], Sharpe=full["Sharpe"], MaxDD=full["MaxDD"],
                         H1=full["H1"], H2=full["H2"], OOS_Sharpe_full=full["OOSs"],
                         gross=float(g.mean()),
                         x_H1=xf["H1"], x_H2=xf["H2"], x_OOS=xf["OOS"],
                         x_DD=xf["DD"], x_CAGR=xf["CAGR"]))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ band derivation
def scan_bar(XG, XL, bar, grid, pub, pareto_mask, victims_mask):
    """Evaluate one bar's coefficient over `grid`, others pinned at `pub`.  Returns a frame."""
    A0 = pass_all(XG, pub)
    L0 = pass_all(XL, pub)
    n0, l0 = int(A0.sum()), int(L0.sum())
    out = []
    for c in grid:
        coef = dict(pub)
        coef[bar] = float(c)
        A = pass_all(XG, coef)
        L = pass_all(XL, coef)
        lost = int((A0 & ~A).sum())
        gained = int((A & ~A0).sum())
        saved = int((A & ~A0 & victims_mask).sum())
        psaved = int((A & ~A0 & victims_mask & pareto_mask).sum())
        lad = int(L.sum())
        weak = (lost == 0) and (lad <= l0)
        strict = weak and (psaved > 0 or lad < l0)
        out.append(dict(bar=bar, coef=float(c), n_admit=int(A.sum()), n0=n0, lost=lost,
                        gained=gained, victims_saved=saved, pareto_victims_saved=psaved,
                        ladder_admit=lad, ladder0=l0,
                        identical=(lost == 0 and gained == 0 and lad == l0),
                        weak_dominates=weak, strictly_dominates=strict))
    return pd.DataFrame(out)


def exact_band(XG, XL, bar, pub, pareto_mask, victims_mask, lo=-5.0, hi=5.0):
    """Analytic band endpoints.  The admitted set changes only at the per-row crossing values,
    so evaluate at the midpoints between consecutive candidate coefficients and read the exact
    intervals off.  Returns (indifference, weak, strict) as lists of (lo, hi) intervals plus the
    per-interval statistics."""
    lo, hi = SCAN_LO, SCAN_HI
    cand = sorted(set(np.round(np.concatenate([XG[bar].values, XL[bar].values,
                                               [pub[bar]]]), 10)))
    cand = [c for c in cand if np.isfinite(c) and lo <= c <= hi]
    edges = [lo] + cand + [hi]
    mids = []
    for a, b in zip(edges[:-1], edges[1:]):
        if b > a:
            mids.append(0.5 * (a + b))
    # include the crossing values themselves (bar semantics are >= for CAGR, > elsewhere)
    pts = sorted(set(mids + cand))
    G = scan_bar(XG, XL, bar, pts, pub, pareto_mask, victims_mask)
    G["is_crossing"] = G.coef.isin(cand)
    return G


SCAN_LO, SCAN_HI = -5.0, 5.0


def contiguous(G, col, at):
    """Maximal contiguous coefficient interval satisfying G[col], containing `at`.

    Returns (lo, hi, lo_open, hi_open).  Each bar is MONOTONE in its own coefficient, so once
    the scan passes the last per-row crossing value nothing can change again: an interval that
    reaches the end of the scanned range is therefore provably UNBOUNDED in that direction, not
    merely unscanned.  `lo_open` / `hi_open` flag that case so it is never printed as a number.
    """
    G = G.sort_values("coef").reset_index(drop=True)
    idx = (G.coef - at).abs().idxmin()
    if not bool(G.loc[idx, col]):
        return (np.nan, np.nan, False, False)
    i = idx
    while i > 0 and bool(G.loc[i - 1, col]):
        i -= 1
    j = idx
    while j < len(G) - 1 and bool(G.loc[j + 1, col]):
        j += 1
    return (float(G.loc[i, "coef"]), float(G.loc[j, "coef"]), i == 0, j == len(G) - 1)


def band_str(lo, hi, lo_open, hi_open):
    a = "(-inf" if lo_open else f"[{lo:.4f}"
    b = "+inf)" if hi_open else f"{hi:.4f}]"
    w = "unbounded" if (lo_open or hi_open) else f"{hi - lo:.4f}"
    return f"{a}, {b}  width {w}"


# ------------------------------------------------------------------ rule-8 walk-forward
def walk_forward_cell(sub, RET, spy, v1_net, key, coefsets):
    """Selector = argmax IS Sharpe among arms clearing the IS 4b screen at each coefficient set.
    The IS screen uses the four prospectively checkable bars (the OOS bar cannot be screened in
    sample by construction).  Picks are read ONCE on 2017-2026."""
    Xi = sub[["xi_" + k for k in BARS5]].rename(columns={"xi_" + k: k for k in BARS5})
    ms = metrics(spy.loc[OOS_START:])
    mv = metrics(H.window(v1_net, "OOS"))
    mc = metrics(H.window(RET["control"], "OOS"))
    order = sub.OOS_Sharpe.rank(ascending=False)
    best = sub.loc[sub.OOS_Sharpe.idxmax(), "arm"]
    out = []
    for label, coef in coefsets.items():
        ok = pass_all_is(Xi, coef)
        c = sub[ok.values]
        base = dict(sel=label, panel=key[0], book=key[1], cost=key[2],
                    spy_OOS_Sharpe=ms["Sharpe"], spy_OOS_CAGR=ms["CAGR"], spy_OOS_MaxDD=ms["MaxDD"],
                    v1_OOS_Sharpe=mv["Sharpe"], v1_OOS_CAGR=mv["CAGR"], v1_OOS_MaxDD=mv["MaxDD"],
                    ctl_OOS_Sharpe=mc["Sharpe"])
        if len(c) == 0:
            out.append(dict(base, pick="(none)", n_admitted=0, OOS_CAGR=np.nan, OOS_Sharpe=np.nan,
                            OOS_MaxDD=np.nan, beat_spy=np.nan, beat_v1=np.nan, beat_ctl=np.nan,
                            oos_best=np.nan, oos_rank=np.nan))
            continue
        p = c.loc[c.IS_Sharpe.idxmax()]
        r = H.window(RET[p["arm"]], "OOS")
        m = metrics(r)
        out.append(dict(base, pick=p["arm"], n_admitted=int(len(c)), OOS_CAGR=m["CAGR"],
                        OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                        beat_spy=bool(m["Sharpe"] > ms["Sharpe"]),
                        beat_v1=bool(m["Sharpe"] > mv["Sharpe"]),
                        beat_ctl=bool(m["Sharpe"] > mc["Sharpe"]),
                        oos_best=bool(p["arm"] == best), oos_rank=float(order.loc[p.name])))
    return pd.DataFrame(out)


# ------------------------------------------------------------------ main
def main():
    say("=" * 200)
    say("IDEA 145 — WEAK-DOMINANCE BANDS AS THE CALIBRATION OUTPUT   (lane C, 2026-09-05)")
    say(f"corpus = 3 panels x 3 books x 17 arms x 2 costs = {3*3*17*2} arm-rows; "
        f"ladder = {3*3*len(LADDER)*2} reference rows.  IS <= {IS_END}, OOS >= {OOS_START}, "
        f"weekly, t+1, {GROSS:.0%} target gross, costs {COSTS} bps.")
    say(f"published 4b: H1 > {PUB['H1']:.2f}xSPY, H2 > {PUB['H2']:.2f}xSPY, OOS > {PUB['OOS']:.2f}xSPY, "
        f"|MaxDD| <= {PUB['DD']:.2f}x|SPY|, CAGR >= {PUB['CAGR']:.2f}xSPY")
    say("=" * 200)

    GR, LD, RET, V1, SPY, BARS = [], [], {}, {}, {}, {}
    for pname in PANELS:
        px, spy, desc = panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        SPY[pname] = spy
        bfull, bIS = bars_win(spy, "full"), bars_win(spy, "IS")
        BARS[pname] = (bfull, bIS)
        say(f"\n--- PANEL {pname}: {desc} | {px.index[0].date()} -> {px.index[-1].date()} | eval from {start.date()}")
        say(f"    SPY full  CAGR {bfull['scagr']:.2%}  Sharpe {metrics(spy)['Sharpe']:.3f}  "
            f"MaxDD {bfull['sdd']:.2%}  halves {bfull['s1']:.3f}/{bfull['s2']:.3f}  OOS Sharpe {bfull['soos']:.3f}")
        say(f"    SPY IS    CAGR {bIS['scagr']:.2%}  MaxDD {bIS['sdd']:.2%}  "
            f"halves {bIS['s1']:.3f}/{bIS['s2']:.3f}  window Sharpe {bIS['soos']:.3f}")
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        V1[pname] = v1
        for book in BOOKS:
            for c in COSTS:
                D, rets = do_cell(pname, px, spy, book, c, bfull, bIS, v1[c])
                GR.append(D)
                RET[(pname, book, c)] = rets
                LD.append(ladder_cell(pname, px, spy, book, c, bfull))
        say(f"    ... {pname} done")

    G = pd.concat(GR, ignore_index=True)
    L = pd.concat(LD, ignore_index=True)
    XG = G[["x_" + k for k in BARS5]].rename(columns={"x_" + k: k for k in BARS5})
    XL = L[["x_" + k for k in BARS5]].rename(columns={"x_" + k: k for k in BARS5})
    XGi = G[["xi_" + k for k in BARS5]].rename(columns={"xi_" + k: k for k in BARS5})

    A0 = pass_all(XG, PUB)
    L0 = pass_all(XL, PUB)
    F0 = fail_set(XG, PUB)
    G["pass4b"] = A0.values
    G["nfail"] = F0.sum(axis=1).values
    G["failbars"] = F0.apply(lambda r: ",".join([k for k in BARS5 if r[k]]) or "-", axis=1).values
    L["pass4b"] = L0.values
    LF = fail_set(XL, PUB)
    L["failbars"] = LF.apply(lambda r: ",".join([k for k in BARS5 if r[k]]) or "-", axis=1).values

    # ---------------------------------------------------------------- reproduction checks
    say("\n" + "=" * 200)
    say("REPRODUCTION CHECKS (all must pass before any new number is read)")
    px56, spy56, _ = panel("u56")
    s56 = px56.index[260]
    ew = H.targets(px56, "EWall")
    a = H.run(px56, ew, bps=PCOST)["r"].loc[s56:]
    b = backtest(px56, ew, cost_bps=PCOST, freq=FREQ)["returns"].loc[s56:]
    d_ab = float((a - b).abs().max())
    ok_a = d_ab < 1e-12
    say(f"  (a) H.run vs engine.backtest, ungated EWall u56: max|diff| = {d_ab:.2e} -> "
        f"{'PASS' if ok_a else 'FAIL'}")
    pub_row = G[(G.panel == "u56") & (G.book == "EWall") & (G.cost == 10.0) & (G.arm == "vol60-dg")].iloc[0]
    ok_b = (abs(pub_row.CAGR - 0.116) < 5e-4 and abs(pub_row.Sharpe - 1.133) < 5e-3
            and abs(pub_row.MaxDD + 0.169) < 5e-4)
    say(f"  (b) idea 94 published EWall+vol60-dg u56@10bps 11.6%/1.133/-16.9%: got "
        f"{pub_row.CAGR:.3%}/{pub_row.Sharpe:.3f}/{pub_row.MaxDD:.3%} -> {'PASS' if ok_b else 'FAIL'}")
    P = G[G.pareto]
    floor_only = (G.failbars == "CAGR")
    G["floor_only"] = floor_only.values
    lad_floor_only = (L.failbars == "CAGR")
    c129 = dict(rows=len(G), pareto=int(G.pareto.sum()), pass4b=int(A0.sum()),
                floor_only=int(floor_only.sum()),
                p_floor_only=int((floor_only & G.pareto).sum()),
                p_clear4=int(((floor_only | A0.values) & G.pareto).sum()),
                lad_rows=len(L), lad_floor_only=int(lad_floor_only.sum()),
                lad_max_m=float(L.loc[lad_floor_only, "m"].max()) if lad_floor_only.any() else np.nan,
                lad_pass4b=int(L0.sum()))
    tgt = dict(rows=306, pareto=82, pass4b=29, floor_only=27, p_floor_only=11, p_clear4=23,
               lad_rows=342, lad_floor_only=97, lad_max_m=0.80, lad_pass4b=10)
    ok_c = all(abs(c129[k] - tgt[k]) < 1e-9 for k in tgt)
    say(f"  (c) idea 129/131 census reproduced: {c129}")
    say(f"      target                          : {tgt}  -> {'PASS' if ok_c else 'FAIL'}")
    A_is = pass_all_is(XGi, dict(PUB))
    B_is = pass_all_is(XGi, dict(PUB, CAGR=0.00)) & ~A_is
    C_is = ~pass_all_is(XGi, dict(PUB, CAGR=0.00))
    ok_d = (int(A_is.sum()), int(B_is.sum()), int(C_is.sum())) == (45, 9, 252)
    say(f"  (d) idea 129 IS-screen groups A/B/C = {int(A_is.sum())}/{int(B_is.sum())}/{int(C_is.sum())} "
        f"(target 45/9/252) -> {'PASS' if ok_d else 'FAIL'}")
    say(f"  ALL CHECKS: {'PASS' if (ok_a and ok_b and ok_c and ok_d) else 'SEE ABOVE'}")

    # ---------------------------------------------------------------- Q1 the published point
    say("\n" + "=" * 200)
    say("Q1  THE PUBLISHED POINT — what each bar is doing at (1.00, 1.00, 1.00, 0.60, 0.70)")
    say("=" * 200)
    say(f"  arm corpus: {len(G)} rows, {int(A0.sum())} pass 4b, {int(G.pass4a.sum())} pass 4a, "
        f"{int((A0.values & G.pass4a.values).sum())} pass both")
    say(f"  ladder    : {len(L)} rows, {int(L0.sum())} pass 4b  (the leakage control: these are "
        f"pure de-grossing levers, not books)")
    say("\n  sole-cause census (rows failing 4b on exactly ONE bar):")
    sole = []
    for k in BARS5:
        m = (G.failbars == k)
        sole.append(dict(bar=k, coef=PUB[k], sole_victims=int(m.sum()),
                         pareto_victims=int((m & G.pareto).sum()),
                         also_pass4a=int((m & G.pass4a).sum()),
                         ladder_sole=int((L.failbars == k).sum())))
    SOLE = pd.DataFrame(sole)
    say(SOLE.to_string(index=False))
    say(f"\n  rows clearing the other four bars, per bar (denominator of the 'share' statistic):")
    for k in BARS5:
        m = (G.failbars == k)
        say(f"    {k:5s}: {int(m.sum())} sole victims / {int(m.sum()) + int(A0.sum())} clearing the "
            f"other four = {int(m.sum())/(int(m.sum())+int(A0.sum())):.1%}")

    # ---------------------------------------------------------------- Q2 the bands
    say("\n" + "=" * 200)
    say("Q2  DOMINANCE BANDS, ONE COEFFICIENT AT A TIME (other four PINNED at published)")
    say("    criteria (idea 131's, generalised):  (1) lose none of the published admissions;")
    say("    (2) save Pareto-best sole victims;   (3) admit no more ladder points than published.")
    say("    WEAK = (1) and (3).   STRICT = WEAK and a strict gain on (2) or (3).")
    say("=" * 200)
    ALLG, BANDS = [], []
    for k in BARS5:
        victims = (G.failbars == k).values
        Gc = scan_bar(XG, XL, k, GRIDS[k], PUB, G.pareto.values, victims)
        Gc["grid"] = "coarse"
        Ge = exact_band(XG, XL, k, PUB, G.pareto.values, victims)
        Ge["grid"] = "exact"
        ALLG.append(Gc)
        ALLG.append(Ge)
        ind = contiguous(Ge, "identical", PUB[k])
        weak = contiguous(Ge, "weak_dominates", PUB[k])
        st = Ge[Ge.strictly_dominates]
        say(f"\n  --- bar {k}  (published {PUB[k]:.2f})   ALL {len(GRIDS[k])} coarse grid points:")
        say(Gc[["coef", "n_admit", "lost", "gained", "victims_saved", "pareto_victims_saved",
                "ladder_admit", "identical", "weak_dominates", "strictly_dominates"]]
            .to_string(index=False, float_format=lambda x: f"{x:.2f}"))
        say(f"    INDIFFERENCE band (identical admitted set AND identical ladder leakage): "
            f"{band_str(*ind)}")
        say(f"    WEAK-DOMINANCE band containing the published point: {band_str(*weak)}")
        # LOOSEN[k] says which DIRECTION on the coefficient axis loosens bar k: for the three
        # Sharpe bars and the CAGR floor that is DOWN, for the drawdown cap it is UP.  Label by
        # effect, not by sign, or the drawdown cap reads backwards.
        below, above = st[st.coef < PUB[k]], st[st.coef > PUB[k]]
        loose_side, tight_side = (below, above) if LOOSEN[k] < 0 else (above, below)
        if len(st):
            say(f"    STRICT-DOMINANCE region: NON-EMPTY — the published point is DOMINATED "
                f"({len(loose_side)} values LOOSER, {len(tight_side)} TIGHTER)")
            for lab, side in (("looser", loose_side), ("tighter", tight_side)):
                if not len(side):
                    continue
                # the value in this side NEAREST the published point
                e = side.iloc[(side.coef - PUB[k]).abs().values.argmin()]
                say(f"      {lab:8s} range [{side.coef.min():.4f}, {side.coef.max():.4f}] — "
                    f"nearest value {e.coef:.4f}: admits {int(e.n_admit)} (vs 29), loses {int(e.lost)}, "
                    f"saves {int(e.victims_saved)} sole victims of which {int(e.pareto_victims_saved)} "
                    f"Pareto-best, ladder leakage {int(e.ladder_admit)} (vs {int(Ge.ladder0.iloc[0])})")
            if len(loose_side) and len(tight_side):
                say(f"      NOTE: dominated in BOTH directions — the three criteria do not order "
                    f"this bar, so 'dominated' here means UNDETERMINED, not 'move it to X'.")
        else:
            say(f"    STRICT-DOMINANCE region: EMPTY — no value of {k} beats {PUB[k]:.2f} on its "
                f"own three criteria")
        BANDS.append(dict(bar=k, published=PUB[k], ind_lo=ind[0], ind_hi=ind[1],
                          ind_lo_open=ind[2], ind_hi_open=ind[3],
                          ind_width=(np.inf if (ind[2] or ind[3]) else ind[1] - ind[0]),
                          weak_lo=weak[0], weak_hi=weak[1],
                          weak_lo_open=weak[2], weak_hi_open=weak[3],
                          n_strict=int(len(st)), n_strict_looser=int(len(loose_side)),
                          n_strict_tighter=int(len(tight_side)),
                          strict_lo=float(st.coef.min()) if len(st) else np.nan,
                          strict_hi=float(st.coef.max()) if len(st) else np.nan,
                          sole_victims=int(victims.sum()),
                          pareto_sole_victims=int((victims & G.pareto.values).sum()),
                          pub_interior=bool((ind[2] or ind[0] < PUB[k]) and (ind[3] or PUB[k] < ind[1]))))
    B = pd.DataFrame(BANDS)
    say("\n  BAND SUMMARY (the object idea 145 proposes PROTOCOL publish instead of the point):")
    say(B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- Q3 separability
    say("\n" + "=" * 200)
    say("Q3  ARE THE BANDS SEPARABLE?  phi x delta map (the two-parameter grid, all points)")
    say("=" * 200)
    PHIS = np.round(np.arange(0.00, 1.101, 0.10), 2)
    DELTAS = np.round(np.arange(0.30, 1.101, 0.10), 2)
    pm = []
    for d in DELTAS:
        for p in PHIS:
            coef = dict(PUB, DD=float(d), CAGR=float(p))
            A = pass_all(XG, coef)
            Lx = pass_all(XL, coef)
            pm.append(dict(delta=float(d), phi=float(p), n_admit=int(A.sum()),
                           ladder_admit=int(Lx.sum()),
                           pareto_admit=int((A.values & G.pareto.values).sum()),
                           both_paths=int((A.values & G.pass4a.values).sum())))
    PM = pd.DataFrame(pm)
    say("  n admitted (rows = delta, cols = phi):")
    say(PM.pivot(index="delta", columns="phi", values="n_admit").to_string())
    say("\n  ladder points admitted (the leakage control):")
    say(PM.pivot(index="delta", columns="phi", values="ladder_admit").to_string())
    say("\n  phi's indifference band re-derived at every delta (is the band delta-dependent?):")
    sep = []
    for d in DELTAS:
        pub_d = dict(PUB, DD=float(d))
        vict = (fail_set(XG, pub_d).sum(axis=1) == 1) & ~passes(XG["CAGR"], "CAGR", pub_d["CAGR"])
        Ge = exact_band(XG, XL, "CAGR", pub_d, G.pareto.values, vict.values)
        ind = contiguous(Ge, "identical", pub_d["CAGR"])
        wk = contiguous(Ge, "weak_dominates", pub_d["CAGR"])
        ns = int(Ge.strictly_dominates.sum())
        sep.append(dict(delta=float(d), phi_ind_lo=ind[0], phi_ind_hi=ind[1],
                        phi_ind_open=bool(ind[2] or ind[3]),
                        phi_ind_width=(np.inf if (ind[2] or ind[3]) else ind[1] - ind[0]),
                        phi_weak_lo=wk[0], phi_weak_hi=wk[1], n_strict=ns))
    SEP = pd.DataFrame(sep)
    say(SEP.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  delta's indifference band re-derived at every phi:")
    sep2 = []
    for p in PHIS:
        pub_p = dict(PUB, CAGR=float(p))
        vict = (fail_set(XG, pub_p).sum(axis=1) == 1) & ~passes(XG["DD"], "DD", pub_p["DD"])
        Ge = exact_band(XG, XL, "DD", pub_p, G.pareto.values, vict.values)
        ind = contiguous(Ge, "identical", pub_p["DD"])
        wk = contiguous(Ge, "weak_dominates", pub_p["DD"])
        sep2.append(dict(phi=float(p), delta_ind_lo=ind[0], delta_ind_hi=ind[1],
                         delta_ind_open=bool(ind[2] or ind[3]),
                         delta_ind_width=(np.inf if (ind[2] or ind[3]) else ind[1] - ind[0]),
                         delta_weak_lo=wk[0], delta_weak_hi=wk[1],
                         n_strict=int(Ge.strictly_dominates.sum())))
    SEP2 = pd.DataFrame(sep2)
    say(SEP2.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- Q4 rule 8
    say("\n" + "=" * 200)
    say("Q4  RULE 8 — bands re-derived on the IS WINDOW ALONE (2009-2016), read OOS once")
    say("=" * 200)
    say("  NOTE, stated before any number: 4b has FIVE bars but only FOUR are prospectively")
    say("  checkable.  The OOS Sharpe bar cannot be screened on an IS window by construction,")
    say("  so its band can only ever be derived retrospectively.  The IS screen below is the")
    say("  four-bar version idea 131 used (H1, H2, DD, CAGR on the IS window).")
    XLi = XL  # the ladder's IS crossings are not needed: leakage is an adoption question
    isb = []
    for k in BARS_IS:
        victims_i = (fail_set(XGi, PUB).sum(axis=1) == 1) & ~passes(XGi[k], k, PUB[k])
        Ge = exact_band(XGi, XLi, k, PUB, G.pareto.values, victims_i.values)
        ind = contiguous(Ge, "identical", PUB[k])
        wk = contiguous(Ge, "weak_dominates", PUB[k])
        row_full = B[B.bar == k].iloc[0]
        isb.append(dict(bar=k, published=PUB[k], IS_ind_lo=ind[0], IS_ind_hi=ind[1],
                        IS_ind_open=bool(ind[2] or ind[3]),
                        IS_ind_width=(np.inf if (ind[2] or ind[3]) else ind[1] - ind[0]),
                        IS_weak_lo=wk[0], IS_weak_hi=wk[1],
                        full_ind_lo=row_full.ind_lo, full_ind_hi=row_full.ind_hi,
                        contains_pub=bool(ind[0] <= PUB[k] <= ind[1]),
                        overlaps_full=bool(max(ind[0], row_full.ind_lo) <= min(ind[1], row_full.ind_hi))))
    ISB = pd.DataFrame(isb)
    say("\n  IS-derived bands vs full-sample bands (the stability question):")
    say(ISB.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # coefficient sets to run the selector at: published, and each bar at its IS-band edges
    coefsets = {"PUB": dict(PUB)}
    for _, r in ISB.iterrows():
        k = r["bar"]
        lo, hi = r["IS_ind_lo"], r["IS_ind_hi"]
        if not (np.isfinite(lo) and np.isfinite(hi)):
            continue
        coefsets[f"{k}@lo"] = dict(PUB, **{k: float(lo)})
        coefsets[f"{k}@mid"] = dict(PUB, **{k: float(0.5 * (lo + hi))})
        coefsets[f"{k}@hi"] = dict(PUB, **{k: float(hi)})
        if r["IS_ind_open"]:
            say(f"    ({k}'s IS band is unbounded on one side — its open edge IS bar deletion, "
                f"which the NOBARS control already covers; the scanned endpoint is used.)")
    coefsets["NOBARS"] = dict(H1=-9e9, H2=-9e9, OOS=-9e9, DD=9e9, CAGR=-9e9)

    WF = []
    for pname in PANELS:
        spy = SPY[pname]
        for book in BOOKS:
            for c in COSTS:
                sub = G[(G.panel == pname) & (G.book == book) & (G.cost == c)].reset_index(drop=True)
                WF.append(walk_forward_cell(sub, RET[(pname, book, c)], spy, V1[pname][c],
                                            (pname, book, c), coefsets))
    W = pd.concat(WF, ignore_index=True)
    say(f"\n  {len(coefsets)} coefficient sets x 18 cells = {len(W)} selector rows.")
    agg = W.groupby("sel").agg(
        cells_picking=("pick", lambda s: int((s != "(none)").sum())),
        mean_admitted=("n_admitted", "mean"),
        OOS_CAGR=("OOS_CAGR", "mean"), OOS_Sharpe=("OOS_Sharpe", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"),
        beat_spy=("beat_spy", "sum"), beat_v1=("beat_v1", "sum"),
        beat_ctl=("beat_ctl", "sum"), oos_best=("oos_best", "sum")).reset_index()
    pubpicks = W[W.sel == "PUB"].set_index(["panel", "book", "cost"])["pick"]
    moved = []
    for s in coefsets:
        p = W[W.sel == s].set_index(["panel", "book", "cost"])["pick"]
        moved.append(int((p != pubpicks).sum()))
    agg["picks_moved_vs_PUB"] = [moved[list(coefsets).index(s)] for s in agg.sel]
    say("\n  rule-8 selector results (means over cells that pick; OOS read once):")
    say(agg.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # paired comparison on the cells the published screen enters
    pub_cells = set(W[(W.sel == "PUB") & (W.pick != "(none)")]
                    .set_index(["panel", "book", "cost"]).index)
    say(f"\n  PAIRED on the {len(pub_cells)} cells the published screen enters:")
    pr = []
    for s in coefsets:
        d = W[W.sel == s].set_index(["panel", "book", "cost"]).loc[list(pub_cells)]
        pr.append(dict(sel=s, n=len(d), OOS_CAGR=d.OOS_CAGR.mean(), OOS_Sharpe=d.OOS_Sharpe.mean(),
                       OOS_MaxDD=d.OOS_MaxDD.mean(),
                       beat_spy=int(d.beat_spy.sum()), beat_v1=int(d.beat_v1.sum()),
                       moved=int((d["pick"] != pubpicks.loc[list(pub_cells)]).sum())))
    PR = pd.DataFrame(pr)
    say(PR.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    ref = W[W.sel == "PUB"].set_index(["panel", "book", "cost"]).loc[list(pub_cells)]
    say(f"\n  reference OOS on those cells: SPY Sharpe {ref.spy_OOS_Sharpe.mean():.3f} / "
        f"CAGR {ref.spy_OOS_CAGR.mean():.2%} / MaxDD {ref.spy_OOS_MaxDD.mean():.2%};  "
        f"RULES v1 Sharpe {ref.v1_OOS_Sharpe.mean():.3f} / CAGR {ref.v1_OOS_CAGR.mean():.2%} / "
        f"MaxDD {ref.v1_OOS_MaxDD.mean():.2%};  ungated control Sharpe {ref.ctl_OOS_Sharpe.mean():.3f}")
    say("\n  per-cell picks, published vs every band edge that moves one:")
    piv = W.pivot_table(index=["panel", "book", "cost"], columns="sel", values="pick",
                        aggfunc="first")
    movecols = [c for c in piv.columns if (piv[c] != piv["PUB"]).any()]
    if movecols:
        say(piv[["PUB"] + [c for c in movecols if c != "PUB"]].to_string())
    else:
        say("    NO coefficient set inside any IS band moves a single pick in any of the 18 cells.")

    # ---------------------------------------------------------------- Q5 both KEEP paths
    say("\n" + "=" * 200)
    say("Q5  BOTH KEEP PATHS, all 306 rows, at the published point and at every band edge")
    say("=" * 200)
    kp = [dict(coefset="PUB(4b published)", pass4b=int(A0.sum()), pass4a=int(G.pass4a.sum()),
               both=int((A0.values & G.pass4a.values).sum()), ladder=int(L0.sum()))]
    for _, r in B.iterrows():
        for edge, val, open_ in (("ind_lo", r.ind_lo, r.ind_lo_open),
                                 ("ind_hi", r.ind_hi, r.ind_hi_open),
                                 ("weak_lo", r.weak_lo, r.weak_lo_open),
                                 ("weak_hi", r.weak_hi, r.weak_hi_open)):
            if not np.isfinite(val) or open_:
                continue
            coef = dict(PUB, **{r.bar: float(val)})
            A = pass_all(XG, coef)
            Lx = pass_all(XL, coef)
            kp.append(dict(coefset=f"{r.bar}={val:.4f} ({edge})", pass4b=int(A.sum()),
                           pass4a=int(G.pass4a.sum()),
                           both=int((A.values & G.pass4a.values).sum()), ladder=int(Lx.sum())))
    KP = pd.DataFrame(kp).drop_duplicates(subset=["coefset"])
    say(KP.to_string(index=False))
    say(f"\n  No book is promoted by this run.  4a is unaffected by 4b's coefficients "
        f"({int(G.pass4a.sum())} of {len(G)} rows) and is reported for completeness.")

    # ---------------------------------------------------------------- outputs
    ALL = pd.concat(ALLG, ignore_index=True)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    L.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    ALL.to_csv(OUT / f"{STEM}.bands.csv", index=False)
    B.to_csv(OUT / f"{STEM}.bandsummary.csv", index=False)
    PM.to_csv(OUT / f"{STEM}.pairmap.csv", index=False)
    pd.concat([SEP, SEP2], axis=0, ignore_index=True).to_csv(OUT / f"{STEM}.separability.csv", index=False)
    ISB.to_csv(OUT / f"{STEM}.isbands.csv", index=False)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say("\nwrote: .grid.csv .ladder.csv .bands.csv .bandsummary.csv .pairmap.csv "
        ".separability.csv .isbands.csv .walkforward.csv .console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
