#!/usr/bin/env python3
"""Idea 367: does the NUMERAIRE clause screen the record's DD-improving overlay claims?

Idea 351 found that a constant exposure multiplier (the GROSS dial) buys drawdown at an exchange
rate equal to the book's own |MaxDD|/CAGR, at zero Sharpe cost -- i.e. the cheapest drawdown in the
record is free arithmetic, and any real overlay must BEAT it to be worth a rule.  Idea 372 then
CORRECTED the closed form: the ratio you can actually buy on the ladder is 10-13% BELOW
|MaxDD|/CAGR, because MaxDD is not linear in the multiplier, and "which bar you pick flips this
verdict".  The queue asks: apply that bar retrospectively to every DD-improving overlay claim the
record has committed, count how many would have been KILLED ON SIGHT, and -- if the hit rate is
high -- adopt the clause as a pre-screen that saves whole runs.

THE BAR (two versions -- TUNED PARAMETER 1, both reported everywhere):
    CF     bar = |MaxDD_control| / CAGR_control                        (idea 351's closed form)
    MATCH  bar = the realised gross-ladder dDD at the SAME dCAGR       (idea 372's correction)
           i.e. solve the fine ladder m in [0.02, 1.00] for the multiplier that gives up exactly as
           much CAGR as the overlay does, and read the drawdown that ladder point actually buys.
An overlay is KILLED ON SIGHT iff its own ratio (pp of MaxDD bought per pp of CAGR given up,
idea 351's ruler) is BELOW the bar: it paid return for drawdown a free dial would have bought
cheaper.  Points that cost nothing (dCAGR_pp >= -0.05) are not on the ruler at all and are
quarantined, never counted as passes.

TUNED PARAMETER 2: the overlay's own dial (one per family, inherited verbatim from idea 351 so the
grid reproduces).  Panel (U56/B136/SMALL439), book size n in {3,20}, cost rung {0,10,25} bps and the
FAMILY are reported axes, not tuned -- every one of the 306 points is written to the grid CSV.

WHAT THIS FILE DOES
  [0] REPRODUCTION GATES, before any new number: derived rung identity vs engine.backtest; idea
      40/41's published U56 rows; GROSS linearity; and a full rebuild of idea 351's committed
      306-point grid, compared column by column.
  [A] THE BAR, measured per book: CF vs MATCH, and the shrink factor MATCH/CF that idea 372 put at
      0.87-0.90.  This is the only place the census's constant comes from.
  [B] THE CENSUS.  B1: a text census of LEADERBOARD.md (how many committed rows are overlay-class
      and claim a drawdown improvement -- the queue's literal denominator).  B2: the SCOREABLE
      census over every committed grid CSV in research/backtests that pairs a treated row to its own
      control on the same axes; every DD-improving pair is put on the ruler and scored against both
      bars.  Coverage and quarantines are reported, not hidden.
  [C] KEEP paths 4a/4b at all 306 live points x 3 rungs.
  [D] RULE 8 walk-forward: the clause used as a PRE-SCREEN on a menu.  Parameters (family, dial, n)
      are chosen on 2008-2016 only -- once unscreened (argmax IS Sharpe over the whole menu) and
      once screened (drop every point whose IS ratio is below its IS bar, then argmax IS Sharpe) --
      and 2017-2026 is read exactly once, against the overlay-OFF control, RULES v2 (live) and SPY.
  [E] Does the KILL-on-sight verdict AGREE with the verdict a full run would have produced?  The
      confusion matrix of numeraire-KILL against 4b-fail on all 306 live points, which is what
      "saves whole runs" has to mean.

CAVEATS: (1) all three panels are current-constituent lists (SURVIVORSHIP), so drawdown LEVELS are
optimistic; the ruler reads DIFFERENCES against an own-control on the same panel, but the 4b DD cap
in [C] is a level test.  (2) SMALL439 starts 2010-01-04, so its halves are not the same calendar
halves as U56/B136.  (3) CADENCE is not an exposure overlay; it is carried because idea 351 carried
it, and is labelled at every point of use.  (4) The B1 text census is a REGEX over prose and is
reported as a bound, not a measurement; B2 is the measured census.  (5) The census's MATCH bar uses
the shrink factor measured in [A] on six books; its spread is reported and the census is scored at
the median AND at both extremes.

Deterministic, standalone.  Reads baseline.py, engine and the committed record; modifies nothing.
"""
import os, re, sys, glob, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
RESUME = os.environ.get("RESUME") == "1"
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights                            # noqa
from engine import backtest, metrics                                                   # noqa

SLUG = "2026-09-07_does-the-NUMERAIRE-clause-screen-the-queues-open-overlay-ideas_C"
OUT = ROOT / "research" / "backtests"
PARENT = OUT / "2026-09-07_does-any-overlay-move-MaxDD-without-moving-CAGR-more_C.grid.csv"

MAX_VOL, GROSS = 0.60, 0.75
NS = [3, 20]
B_FIXED = 0.30
FAMILIES = {
    "GROSS":   [0.85, 0.75, 0.625, 0.50],
    "VOLTGT":  [0.20, 0.15, 0.12, 0.10],
    "BREADTH": [0.50, 0.25, 0.00],
    "DDCTRL":  [0.10, 0.15, 0.20, 0.25],
    "CADENCE": ["M", "Q"],
}
COSTS = [0, 10, 25]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260
FREE_EPS = 0.05                      # pp; below this the ruler is not defined
LADDER = np.round(np.arange(1.00, 0.019, -0.01), 4)   # the gross dial, finely


# ================================================================ panels / books
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


def base_weights(px, n, drop_spy=False):
    """Idea 40/41's book, reproduced verbatim: top-n eligible by the v1 composite WITHOUT
    /sqrt(vol20), w = GROSS/n."""
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    elig = above & (vol20 < MAX_VOL)
    if drop_spy and "SPY" in px.columns:
        elig = elig.copy(); elig["SPY"] = False
    rank = s.where(elig).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


def breadth(px, drop_spy=False):
    cols = [c for c in px.columns if not (drop_spy and c == "SPY")]
    q = px[cols]
    above = q > q.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def mult_series(fam, dial, r0, br_lag):
    if fam == "GROSS":
        return pd.Series(float(dial), index=r0.index)
    if fam == "VOLTGT":
        v = (r0.rolling(20).std() * np.sqrt(252)).shift(1)
        return (float(dial) / v).clip(upper=1.0).fillna(1.0)
    if fam == "BREADTH":
        on = br_lag.reindex(r0.index).fillna(False)
        return pd.Series(np.where(on.values, float(dial), 1.0), index=r0.index)
    if fam == "DDCTRL":
        eq = (1 + r0).cumprod()
        dd = eq / eq.cummax() - 1
        return pd.Series(np.where(dd.shift(1).fillna(0.0).values < -float(dial), 0.0, 1.0), index=r0.index)
    raise ValueError(fam)


def apply_mult(r0, t0, mult, c):
    dm = np.abs(np.diff(np.concatenate([[1.0], mult.values])))
    return mult.values * (r0.values - t0.values * c / 1e4) - dm * GROSS * c / 1e4, dm


# ================================================================ metric helpers
def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_4b(r, spy):
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), f


def bars_4a(r, base):
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": abs(metrics(base)["MaxDD"]) - abs(metrics(r)["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), f


def summarise(r, spy, base10):
    m = metrics(r); h1, h2 = hs(r)
    ok_b, fb = bars_4b(r, spy); ok_a, fa = bars_4a(r, base10)
    mo = metrics(r.loc[OOS_START:]); mi = metrics(r.loc[:IS_END])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                pass4b=ok_b, fail4b=",".join(fb), pass4a=ok_a, fail4a=",".join(fa))


def ratio_of(dcagr_pp, ddd_pp):
    if dcagr_pp >= -FREE_EPS:
        return np.nan
    return ddd_pp / (-dcagr_pp)


# ================================================================ the numeraire ladder
def ladder_curve(r0, t0, c, window=None):
    """The gross dial priced finely on the SAME book/rung: for every m, what it costs (pp of CAGR)
    and what it buys (pp of MaxDD).  Returns (paid_pp asc, bought_pp, m) plus the control levels."""
    ctl = pd.Series(r0.values - t0.values * c / 1e4, index=r0.index)
    if window is not None:
        ctl = ctl.loc[window[0]:window[1]]
    cm = metrics(ctl)
    paid, bought = [], []
    for m in LADDER:
        mult = pd.Series(float(m), index=r0.index)
        vals, _ = apply_mult(r0, t0, mult, c)
        rr = pd.Series(vals, index=r0.index)
        if window is not None:
            rr = rr.loc[window[0]:window[1]]
        mm = metrics(rr)
        paid.append(100 * (cm["CAGR"] - mm["CAGR"]))          # >= 0: pp of CAGR given up
        bought.append(100 * (abs(cm["MaxDD"]) - abs(mm["MaxDD"])))
    paid, bought = np.array(paid), np.array(bought)
    o = np.argsort(paid)
    return paid[o], bought[o], np.array(LADDER)[o], cm


def bar_match(paid, bought, cost_pp):
    """What the ladder buys for the same pp of CAGR.  Returns (bar, reachable)."""
    if cost_pp <= 0:
        return np.nan, False
    if cost_pp > paid.max():
        return np.nan, False                                   # off the end of the dial
    b = float(np.interp(cost_pp, paid, bought))
    return b / cost_pp, True


# ================================================================ [0] gates
def gate_checks(px, r0, t0, w, br_lag, start, log):
    def chk(name, got, want, tol):
        ok = abs(got - want) <= tol
        log.append(dict(check=name, got=got, want=want, err=abs(got - want), ok=ok))
        print(f"    {'PASS' if ok else 'FAIL':4s} {name:52s} got {got:.6f} want {want:.6f} "
              f"err {abs(got-want):.2e}")
        return ok

    print("\n[0] REPRODUCTION GATES (before any new number)")
    for c in (10.0, 25.0):
        live = backtest(px, w, cost_bps=c, freq="W")["returns"].loc[start:]
        der = r0 - t0 * c / 1e4
        e = float(np.abs(live.values - der.values).max())
        print(f"    {'PASS' if e < 1e-12 else 'FAIL'} rung identity r(c)=r(0)-turnover*c/1e4 @ {c:.0f} bps"
              f"   max|diff| = {e:.3e}")
        log.append(dict(check=f"rung identity @{c:.0f}bps", got=e, want=0.0, err=e, ok=e < 1e-12))
    m3 = metrics(r0 - t0 * 10 / 1e4); h1, h2 = hs(r0 - t0 * 10 / 1e4)
    chk("idea 40/41 U56 n=3 NONE CAGR", m3["CAGR"], 0.2185, 5e-4)
    chk("idea 40/41 U56 n=3 NONE Sharpe", m3["Sharpe"], 1.036, 5e-3)
    chk("idea 40/41 U56 n=3 NONE MaxDD", m3["MaxDD"], -0.2581, 5e-4)
    chk("idea 40/41 U56 n=3 NONE H1", h1, 1.014, 5e-3)
    chk("idea 40/41 U56 n=3 NONE H2", h2, 1.061, 5e-3)
    mult = mult_series("GROSS", 0.75, r0, br_lag)
    vals, _ = apply_mult(r0, t0, mult, 0)
    e = float(np.abs(0.75 * r0.values - vals).max())
    print(f"    {'PASS' if e < 1e-12 else 'FAIL'} GROSS linearity at 0 bps                            "
          f"     max|diff| = {e:.3e}")
    log.append(dict(check="GROSS linearity @0bps", got=e, want=0.0, err=e, ok=e < 1e-12))


# ================================================================ the live grid
def build_grid():
    print("\n[panels]")
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}
    rows, ladders, gatelog = [], [], []
    for pname, px in panels.items():
        drop_spy = (pname == "SMALL439")
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms_ = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
        br_lag = (breadth(px, drop_spy) < B_FIXED).shift(1)
        print(f"\n================ {pname}: {px.shape[1]-1} names + SPY, {px.index[0].date()} -> "
              f"{px.index[-1].date()}, eval from {start.date()}")
        print(f"    SPY CAGR {ms_['CAGR']:.2%} Sharpe {ms_['Sharpe']:.3f} MaxDD {ms_['MaxDD']:.2%} "
              f"H1/H2 {s1:.3f}/{s2:.3f} | OOS Sharpe {so['Sharpe']:.3f}")

        bres = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq="W")
        b0, bt0 = bres["returns"].loc[start:], bres["turnover"].loc[start:]
        base10 = b0 - bt0 * 10 / 1e4
        bm = metrics(base10); bb1, bb2 = hs(base10)
        bo = metrics(base10.loc[OOS_START:])
        print(f"    RULES v2 (live, 10 bps) CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.3f} "
              f"MaxDD {bm['MaxDD']:.2%} H1/H2 {bb1:.3f}/{bb2:.3f} | OOS Sharpe {bo['Sharpe']:.3f}")

        for n in NS:
            w = base_weights(px, n, drop_spy)
            cad = {}
            for f in ["W"] + list(FAMILIES["CADENCE"]):
                res = backtest(px, w, cost_bps=0.0, freq=f)
                cad[f] = (res["returns"].loc[start:], res["turnover"].loc[start:])
            r0, t0 = cad["W"]
            if pname == "U56" and n == 3:
                gate_checks(px, r0, t0, w, br_lag, start, gatelog)

            for c in COSTS:
                paid, bought, mgrid, cm = ladder_curve(r0, t0, c)
                bar_cf = abs(cm["MaxDD"]) / cm["CAGR"] if cm["CAGR"] > 0 else np.nan
                # the achievable ladder: best realised ratio anywhere on the dial
                with np.errstate(divide="ignore", invalid="ignore"):
                    lad_ratio = np.where(paid > FREE_EPS, bought / np.maximum(paid, 1e-12), np.nan)
                ladders.append(dict(panel=pname, n=n, cost=c, bar_CF=bar_cf,
                                    lad_ratio_med=float(np.nanmedian(lad_ratio)),
                                    lad_ratio_min=float(np.nanmin(lad_ratio)),
                                    lad_ratio_max=float(np.nanmax(lad_ratio)),
                                    ctrl_CAGR=cm["CAGR"], ctrl_MaxDD=cm["MaxDD"],
                                    over_CF=int(np.nansum(lad_ratio > bar_cf + 1e-9)),
                                    n_pts=int(np.sum(~np.isnan(lad_ratio)))))
                ctl = pd.Series(r0.values - t0.values * c / 1e4, index=r0.index)
                rows.append(dict(panel=pname, n=n, family="CONTROL", dial="off", cost=c,
                                 ann_turnover=t0.sum() / cm["Years"], sw=0.0,
                                 dCAGR_pp=0.0, dDD_pp=0.0, dSharpe=0.0, ratio=np.nan,
                                 bar_CF=bar_cf, bar_MATCH=np.nan, reach=True,
                                 beats_CF=False, beats_MATCH=False,
                                 IS_ratio=np.nan, IS_bar_MATCH=np.nan, IS_beats_MATCH=False,
                                 **summarise(ctl, spy, base10)))
                # IS ladder (rule 8): the same curve fitted on <= 2016 only
                is_win = (r0.index[0], pd.Timestamp(IS_END))
                ipaid, ibought, _, icm = ladder_curve(r0, t0, c, window=is_win)
                for fam, dials in FAMILIES.items():
                    for dial in dials:
                        if fam == "CADENCE":
                            rr, tt = cad[dial]
                            r = pd.Series(rr.values - tt.values * c / 1e4, index=rr.index)
                            sw, turn = 0.0, tt.sum() / metrics(r)["Years"]
                        else:
                            mult = mult_series(fam, dial, r0, br_lag)
                            vals, dm = apply_mult(r0, t0, mult, c)
                            r = pd.Series(vals, index=r0.index)
                            sw = dm.sum(); turn = (mult * t0).sum() / metrics(r)["Years"]
                        m = metrics(r)
                        dcagr = 100 * (m["CAGR"] - cm["CAGR"])
                        dddp = 100 * (abs(cm["MaxDD"]) - abs(m["MaxDD"]))
                        rat = ratio_of(dcagr, dddp)
                        bm_, reach = bar_match(paid, bought, -dcagr)
                        mi = metrics(r.loc[:IS_END])
                        idc = 100 * (mi["CAGR"] - icm["CAGR"])
                        idd = 100 * (abs(icm["MaxDD"]) - abs(mi["MaxDD"]))
                        irat = ratio_of(idc, idd)
                        ibm, _ = bar_match(ipaid, ibought, -idc)
                        rows.append(dict(panel=pname, n=n, family=fam, dial=dial, cost=c,
                                         ann_turnover=turn, sw=sw,
                                         dCAGR_pp=dcagr, dDD_pp=dddp,
                                         dSharpe=m["Sharpe"] - cm["Sharpe"], ratio=rat,
                                         bar_CF=bar_cf, bar_MATCH=bm_, reach=reach,
                                         beats_CF=bool(rat > bar_cf) if np.isfinite(rat) and np.isfinite(bar_cf) else False,
                                         beats_MATCH=bool(rat > bm_) if np.isfinite(rat) and np.isfinite(bm_) else False,
                                         IS_ratio=irat, IS_bar_MATCH=ibm,
                                         IS_beats_MATCH=bool(irat > ibm) if np.isfinite(irat) and np.isfinite(ibm) else False,
                                         **summarise(r, spy, base10)))
            print(f"    n={n}: grid rows so far {sum(1 for x in rows if x['panel']==pname and x['n']==n)}")
    g = pd.DataFrame(rows)
    lad = pd.DataFrame(ladders)
    g.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    lad.to_csv(OUT / f"{SLUG}.ladder.csv", index=False)
    pd.DataFrame(gatelog).to_csv(OUT / f"{SLUG}.gates.csv", index=False)
    return g, lad


def parent_gate(g):
    """Full rebuild of idea 351's committed 306-point grid, column by column."""
    print("\n[0b] PARENT GRID REPRODUCTION (idea 351's committed 306 points)")
    if not PARENT.exists():
        print("    parent grid not committed -- gate SKIPPED"); return
    p = pd.read_csv(PARENT)
    key = ["panel", "n", "family", "dial", "cost"]
    a = g.copy(); b = p.copy()
    for d in (a, b):
        d["dial"] = d["dial"].astype(str)
    m = a.merge(b, on=key, suffixes=("_new", "_old"))
    print(f"    matched {len(m)} of {len(p)} committed rows on {key}")
    worst = 0.0
    for col in ["dCAGR_pp", "dDD_pp", "dSharpe", "ratio", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "IS_Sharpe", "ann_turnover"]:
        x, y = m[f"{col}_new"].values.astype(float), m[f"{col}_old"].values.astype(float)
        ok = ~(np.isnan(x) & np.isnan(y))
        e = float(np.nanmax(np.abs(x[ok] - y[ok]))) if ok.any() else 0.0
        worst = max(worst, e)
        print(f"    {col:14s} max|diff| = {e:.3e}")
    print(f"    ==> PARENT GATE {'PASS' if worst < 1e-9 else 'FAIL'}  worst {worst:.3e}")


# ================================================================ [B1] leaderboard text census
OVERLAY_RE = re.compile(
    r"overlay|\bgate[sd]?\b|gating|voltgt|vol[- ]tar|ddctrl|drawdown control|stop[- ]?loss|"
    r"de[- ]?gross|gross dial|breadth|cash gate|no[- ]trade band|vol scaler|exposure|sleeve|"
    r"scaler|\bstops?\b|\bband\b", re.I)
DDIMP_RE = re.compile(
    r"dMaxDD\s*\**\s*\+|dDD\s*\**\s*\+|\+\s*[0-9.]+\s*pp of (draw|MaxDD)|"
    r"improv\w*\s+(the\s+)?(MaxDD|drawdown)|drawdown\s+(improv|bought|better|shallower)|"
    r"shallower drawdown|buys? drawdown|DD improvement", re.I)


def leaderboard_census():
    print("\n[B1] LEADERBOARD.md TEXT CENSUS (a bound over prose, not a measurement)")
    txt = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
    rows = [l for l in txt if l.startswith("|") and l.count("|") >= 8
            and not re.match(r"^\|[-\s|]+\|$", l) and not l.startswith("| Date | Idea")]
    ov = [l for l in rows if OVERLAY_RE.search(l)]
    dd = [l for l in ov if DDIMP_RE.search(l)]
    print(f"    committed leaderboard rows          : {len(rows)}")
    print(f"    overlay-class (regex)               : {len(ov)}  ({len(ov)/max(len(rows),1):.1%})")
    print(f"    ... AND claiming a DD improvement   : {len(dd)}  ({len(dd)/max(len(rows),1):.1%})")
    print("    regex OVERLAY :", OVERLAY_RE.pattern[:96], "...")
    print("    regex DD-IMPR :", DDIMP_RE.pattern[:96], "...")
    print("    sample of matched rows (idea column, truncated):")
    for l in dd[:8]:
        f = [c.strip() for c in l.split("|")]
        print(f"      - {f[2][:110] if len(f) > 2 else l[:110]}")
    print("    ==> the record's DD claims are NUMBERS in columns, not prose: the prose census is a")
    print("        floor, and B1b below scores the columns instead.")
    return len(rows), len(ov), len(dd), rows


PCT = r"(-?\d+(?:\.\d+)?)\s*%"
TRIPLE = re.compile(PCT + r"\s*/\s*(-?\d+(?:\.\d+)?)\s*/\s*" + PCT)     # CAGR% / Sharpe / MaxDD%


def leaderboard_numeric(rows, shrink_med):
    """B1b: score the leaderboard's OWN columns.  A row is a DD-improving claim iff its MaxDD
    column beats the MaxDD of the comparator quoted in its own baseline column AND its CAGR is
    lower (it paid return for that drawdown).  The bar is that comparator's |MaxDD|/CAGR."""
    print("\n[B1b] LEADERBOARD.md NUMERIC CENSUS (row's own columns vs the comparator IT quotes)")
    n_par = n_claim = 0; recs = []
    for l in rows:
        f = [c.strip() for c in l.split("|")]
        if len(f) < 9:
            continue
        cg, dd_, bl = f[3], f[5], f[7]
        mc, md = re.search(PCT, cg), re.search(PCT, dd_)
        mb = TRIPLE.search(bl)
        if not (mc and md and mb):
            continue
        a_c, a_d = float(mc.group(1)), abs(float(md.group(1)))
        b_c, b_d = float(mb.group(1)), abs(float(mb.group(3)))
        if b_c <= 0:
            continue
        n_par += 1
        dcagr, dddp = a_c - b_c, b_d - a_d
        if dddp <= 0 or dcagr >= -FREE_EPS:
            continue
        n_claim += 1
        rat, bar = dddp / (-dcagr), b_d / b_c
        recs.append(dict(idea=f[2][:80], ratio=rat, bar_CF=bar, bar_MED=shrink_med * bar,
                         dCAGR_pp=dcagr, dDD_pp=dddp, verdict=f[8][:40],
                         kill_CF=bool(rat < bar), kill_MED=bool(rat < shrink_med * bar)))
    C = pd.DataFrame(recs)
    print(f"    rows with a parseable (CAGR, MaxDD) AND a quoted comparator triple : {n_par}")
    print(f"    ... that BOUGHT drawdown by giving up CAGR (on the ruler)          : {n_claim}")
    if len(C):
        print(f"    KILLED ON SIGHT: CF {int(C['kill_CF'].sum())}/{len(C)} ({C['kill_CF'].mean():.1%})"
              f"   MATCH-med {int(C['kill_MED'].sum())}/{len(C)} ({C['kill_MED'].mean():.1%})")
        print(f"    median ratio {C['ratio'].median():.3f} vs median bar {C['bar_CF'].median():.3f}")
        C.to_csv(OUT / f"{SLUG}.leaderboard.csv", index=False)
        print("    the 10 widest misses (would have been killed on sight):")
        for _, r in C[C["kill_CF"]].assign(gap=lambda d: d["bar_CF"] - d["ratio"]) \
                                   .sort_values("gap", ascending=False).head(10).iterrows():
            print(f"      ratio {r['ratio']:7.3f} vs bar {r['bar_CF']:7.3f}  [{r['verdict'][:22]:22s}] {r['idea'][:64]}")
    return C


# ================================================================ [B2] scoreable CSV census
CTRL_TOK = {"none", "control", "off", "ctrl", "base", "baseline", "ctl", "no", "noneoverlay"}
AXIS_RE = re.compile(r"^(panel|universe|book|corpus|n|k|cost|bps|rung|cad|freq|gross|seed|q|"
                     r"depth|thr|band|source|kind|parent|con|gate|point|Q)$", re.I)
ARM_BLACKLIST = {"verdict", "fails", "fail4a", "fail4b", "pass4a", "pass4b", "check", "field",
                 "claim", "cls", "src", "null_side", "bucket", "axis", "worstbar",
                 "IS_worstbar", "OOS_worstbar"}
OVERLAY_ARM_RE = re.compile(r"gate|stop|vol|dd|breadth|gross|cash|band|sleeve|cap|scal|filt|"
                            r"overlay|instr|tilt|mask|spec|conv|key|arm|family|kind", re.I)


def csv_census(shrink_med, shrink_lo, shrink_hi):
    print("\n[B2] SCOREABLE CENSUS over every committed grid CSV in research/backtests")
    files = sorted(glob.glob(str(OUT / "*.csv")))
    recs, cov = [], []
    for f in files:
        name = Path(f).name
        if name.startswith(SLUG):
            continue                                            # never score this run's own output
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        low = {c.lower(): c for c in df.columns}
        if "cagr" not in low or "maxdd" not in low:
            continue
        ccagr, cmdd = low["cagr"], low["maxdd"]
        armcol = None
        for c in df.columns:
            if c in ARM_BLACKLIST or c.lower() in {k.lower() for k in ARM_BLACKLIST}:
                continue
            if pd.api.types.is_numeric_dtype(df[c]):
                continue
            v = set(str(x).strip().lower() for x in df[c].dropna().unique())
            if (v & CTRL_TOK) and len(v) > 1:
                armcol = c
                break
        if armcol is None:
            continue
        keys = [c for c in df.columns if c != armcol and AXIS_RE.match(c)]
        # unit inference: fractions (0.15) vs percent (15.0)
        med = float(np.nanmedian(np.abs(pd.to_numeric(df[ccagr], errors="coerce"))))
        unit = 100.0 if med > 1.5 else 1.0
        grp = df.groupby(keys, dropna=False) if keys else [((), df)]
        npair = nscored = nfree = 0
        for _, sub in grp:
            mask = sub[armcol].astype(str).str.strip().str.lower().isin(CTRL_TOK)
            if mask.sum() != 1 or (~mask).sum() < 1:
                continue
            ctl = sub[mask].iloc[0]
            c_cagr = pd.to_numeric(pd.Series([ctl[ccagr]]), errors="coerce").iloc[0]
            c_mdd = pd.to_numeric(pd.Series([ctl[cmdd]]), errors="coerce").iloc[0]
            if not np.isfinite(c_cagr) or not np.isfinite(c_mdd) or c_cagr <= 0:
                continue
            c_cagr, c_mdd = c_cagr * unit, abs(c_mdd) * unit
            bar_cf = c_mdd / c_cagr
            for _, row in sub[~mask].iterrows():
                a_cagr = pd.to_numeric(pd.Series([row[ccagr]]), errors="coerce").iloc[0]
                a_mdd = pd.to_numeric(pd.Series([row[cmdd]]), errors="coerce").iloc[0]
                if not np.isfinite(a_cagr) or not np.isfinite(a_mdd):
                    continue
                npair += 1
                dcagr = 100 * (a_cagr * unit - c_cagr)
                dddp = 100 * (c_mdd - abs(a_mdd) * unit)
                if dddp <= 0:
                    continue                                    # not a DD-improving claim
                if dcagr >= -FREE_EPS:
                    nfree += 1                                  # free or better: not on the ruler
                    continue
                rat = dddp / (-dcagr)
                nscored += 1
                recs.append(dict(file=name, arm_col=armcol, arm=str(row[armcol]),
                                 overlay_arm=bool(OVERLAY_ARM_RE.search(armcol) or
                                                  OVERLAY_ARM_RE.search(str(row[armcol]))),
                                 unit=unit, ctrl_CAGR=c_cagr, ctrl_MaxDD=c_mdd,
                                 dCAGR_pp=dcagr, dDD_pp=dddp, ratio=rat, bar_CF=bar_cf,
                                 bar_MED=shrink_med * bar_cf, bar_LO=shrink_lo * bar_cf,
                                 bar_HI=shrink_hi * bar_cf,
                                 kill_CF=bool(rat < bar_cf),
                                 kill_MED=bool(rat < shrink_med * bar_cf),
                                 kill_LO=bool(rat < shrink_lo * bar_cf),
                                 kill_HI=bool(rat < shrink_hi * bar_cf)))
        if npair:
            cov.append(dict(file=name, arm_col=armcol, keys=";".join(keys), unit=unit,
                            pairs=npair, dd_improving_scored=nscored, free_quarantined=nfree))
    C = pd.DataFrame(recs); V = pd.DataFrame(cov)
    C.to_csv(OUT / f"{SLUG}.census.csv", index=False)
    V.to_csv(OUT / f"{SLUG}.coverage.csv", index=False)
    print(f"    CSV files in research/backtests            : {len(files)}")
    print(f"    files with a pairable own-control          : {len(V)}")
    print(f"    treated/control pairs found                : {int(V['pairs'].sum()) if len(V) else 0}")
    print(f"    ... of which DD-IMPROVING and on the ruler : {len(C)}")
    print(f"    ... quarantined as free (dCAGR >= -0.05pp) : {int(V['free_quarantined'].sum()) if len(V) else 0}")
    if not len(C):
        return C, V
    for lbl, col, bar in (("CF   (idea 351 closed form)", "kill_CF", "bar_CF"),
                          ("MATCH-lo  (shrink %.3f)" % shrink_lo, "kill_LO", "bar_LO"),
                          ("MATCH-med (shrink %.3f)" % shrink_med, "kill_MED", "bar_MED"),
                          ("MATCH-hi  (shrink %.3f)" % shrink_hi, "kill_HI", "bar_HI")):
        k = C[col].mean()
        print(f"    KILLED ON SIGHT under {lbl:30s}: {int(C[col].sum()):5d} / {len(C)}  ({k:.1%})")
    D = C.drop_duplicates(subset=["dCAGR_pp", "dDD_pp", "ctrl_CAGR", "ctrl_MaxDD"])
    print(f"    DE-DUPLICATED (three pairs of files in the record commit the same corpus twice): "
          f"{len(D)} distinct points, KILLED CF {D['kill_CF'].mean():.1%}, "
          f"MATCH-med {D['kill_MED'].mean():.1%}")
    sub = C[C["overlay_arm"]]
    if len(sub):
        print(f"    ... restricted to overlay-named arms ({len(sub)} rows): "
              f"CF {sub['kill_CF'].mean():.1%}, MATCH-med {sub['kill_MED'].mean():.1%}")
    print("\n    per-file kill rate (MATCH-med), files with >= 5 scored rows:")
    t = C.groupby("file").agg(rows=("ratio", "size"), kill=("kill_MED", "mean"),
                              med_ratio=("ratio", "median"), med_bar=("bar_MED", "median"))
    t = t[t["rows"] >= 5].sort_values("kill")
    for f, r in t.iterrows():
        print(f"      {r['rows']:5.0f} rows  kill {r['kill']:6.1%}  med ratio {r['med_ratio']:7.3f} "
              f"vs bar {r['med_bar']:7.3f}   {f[:66]}")
    return C, V


# ================================================================ [E] queue census
def queue_census():
    print("\n[E] THE QUEUE'S OPEN IDEAS: how many would the clause pre-screen?")
    q = (ROOT / "research" / "QUEUE.md").read_text().split("\n")
    try:
        i0 = q.index("## Open"); i1 = next(k for k, l in enumerate(q) if l.startswith("## In progress"))
    except Exception:
        print("    QUEUE.md sections not found -- SKIPPED"); return 0, 0
    open_ideas = [l for l in q[i0 + 1:i1] if re.match(r"^\d+\.", l)]
    ov = [l for l in open_ideas if OVERLAY_RE.search(l)]
    dd = [l for l in ov if re.search(r"drawdown|MaxDD|\bDD\b", l, re.I)]
    print(f"    open ideas                                 : {len(open_ideas)}")
    print(f"    overlay-class (same regex as B1)           : {len(ov)}  ({len(ov)/max(len(open_ideas),1):.1%})")
    print(f"    ... that also name drawdown/MaxDD          : {len(dd)}")
    print("    NOTE: this is a keyword classification of PROSE, not a backtest of those ideas.")
    return len(open_ideas), len(dd)


# ================================================================ analysis
def analyse(g, lad):
    pd.set_option("display.width", 200)
    print("\n[A] THE BAR, measured per book (10 bps rung shown; all rungs in the ladder CSV)")
    l10 = lad[lad["cost"] == 10].copy()
    l10["shrink_med"] = l10["lad_ratio_med"] / l10["bar_CF"]
    l10["shrink_max"] = l10["lad_ratio_max"] / l10["bar_CF"]
    print(l10[["panel", "n", "ctrl_CAGR", "ctrl_MaxDD", "bar_CF", "lad_ratio_min", "lad_ratio_med",
               "lad_ratio_max", "shrink_med", "shrink_max", "over_CF", "n_pts"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    la = lad[(lad["ctrl_CAGR"] >= 0.05) & lad["bar_CF"].notna()].copy()   # pre-declared exclusion
    la["shrink"] = la["lad_ratio_med"] / la["bar_CF"]
    sh = la["shrink"].dropna()
    shrink_med, shrink_lo, shrink_hi = float(sh.median()), float(sh.min()), float(sh.max())
    over = int(la["over_CF"].sum()); tot = int(la["n_pts"].sum())
    print(f"\n    EXCLUDED from the shrink estimate: books with control CAGR < 5%/yr "
          f"({len(lad)-len(la)} of {len(lad)} (panel,n,rung) cells -- the closed form's denominator "
          f"is unstable there; SMALL439 n=3 reaches |MaxDD|/CAGR = 1512 at 10 bps)")
    print(f"    idea 372 CHECK: realised ladder ratio ABOVE the closed form in {over} of {tot} "
          f"ladder points ({over/max(tot,1):.1%}); shrink (realised/closed-form) "
          f"median {shrink_med:.3f}, range {shrink_lo:.3f}-{shrink_hi:.3f}")
    print("    (idea 372 published 0/114 above the closed form and a 10-13% overstatement, "
          "i.e. shrink 0.87-0.90)")
    hi = la[la["shrink"] > 1.0]
    print(f"    ==> idea 372's 'never above the closed form' does NOT generalise: the ladder ratio "
          f"EXCEEDS |MaxDD|/CAGR on {len(hi)} of {len(la)} cells, all of them cells whose own "
          f"bar_CF is high (min {hi['bar_CF'].min():.2f} vs {la[la['shrink']<=1]['bar_CF'].max():.2f} "
          f"for the largest cell where it holds)" if len(hi) else "")

    print("\n[C] KEEP paths over the live grid (all 306 points x 3 rungs REPORTED)")
    for c in COSTS:
        s = g[g["cost"] == c]
        print(f"    {c:2d} bps: 4a {int(s['pass4a'].sum()):3d}/{len(s)}   4b {int(s['pass4b'].sum()):3d}/{len(s)}"
              f"   beats CF bar {int(s['beats_CF'].sum()):3d}   beats MATCH bar {int(s['beats_MATCH'].sum()):3d}"
              f"   on-ruler {int(s['ratio'].notna().sum()):3d}")
    o = g[(g["cost"] == 10) & (g["family"] != "CONTROL")].copy()
    print("\n    exchange rate by family @10 bps (median ratio; share beating each bar):")
    for fam, s in o.groupby("family"):
        on = s[s["ratio"].notna()]
        print(f"      {fam:8s} n={len(s):3d}  on-ruler {len(on):3d}  median ratio "
              f"{on['ratio'].median():7.3f}  beats CF {s['beats_CF'].mean():6.1%}  "
              f"beats MATCH {s['beats_MATCH'].mean():6.1%}")

    print("\n[E2] DOES THE SCREEN AGREE WITH THE FULL RUN? (confusion matrix on the live grid, 10 bps)")
    for barcol, lbl in (("beats_CF", "CF"), ("beats_MATCH", "MATCH")):
        s = g[(g["cost"] == 10) & (g["family"] != "CONTROL") & g["ratio"].notna()]
        kill = ~s[barcol]
        f4b = ~s["pass4b"]
        tp = int((kill & f4b).sum()); fp = int((kill & ~f4b).sum())
        fn = int((~kill & f4b).sum()); tn = int((~kill & ~f4b).sum())
        prec = tp / max(tp + fp, 1); rec = tp / max(tp + fn, 1)
        base = float(f4b.mean()); npass = tp and (fp + tn) or (fp + tn)
        print(f"    bar {lbl:5s}: screen-KILL & 4b-fail {tp:3d} | screen-KILL & 4b-PASS {fp:3d} "
              f"(4b passes DESTROYED) | kept & 4b-fail {fn:3d} | kept & 4b-pass {tn:3d}")
        print(f"             precision {prec:.3f} vs base rate {base:.3f}  -> LIFT {prec/max(base,1e-9):.3f}"
              f"   |  of the {fp+tn} 4b PASSES on the ruler the screen destroys {fp} "
              f"({fp/max(fp+tn,1):.1%})   |  runs saved {tp+fp}/{len(s)} ({(tp+fp)/max(len(s),1):.1%})")
    return shrink_med, shrink_lo, shrink_hi


# ================================================================ [D] rule 8
def rule8(g):
    print("\n[D] RULE 8 WALK-FORWARD: the numeraire clause as a PRE-SCREEN on the menu")
    print("    Menu = every (n, family, dial) INCLUDING the overlay-OFF control, at 10 bps.")
    print("    Chosen on 2008-2016 by IS Sharpe, once unscreened and once after dropping every")
    print("    point whose IS ratio is below its IS matched-ladder bar.  2017-2026 read ONCE.")
    out = []
    for pname, s in g[g["cost"] == 10].groupby("panel"):
        menu = s.copy()
        ctrl = menu[menu["family"] == "CONTROL"].sort_values("IS_Sharpe", ascending=False).iloc[0]
        best_oos = menu.sort_values("OOS_Sharpe", ascending=False).iloc[0]
        unscr = menu.sort_values("IS_Sharpe", ascending=False).iloc[0]
        keep = menu[(menu["family"] == "CONTROL") | (menu["IS_beats_MATCH"])]
        scr = keep.sort_values("IS_Sharpe", ascending=False).iloc[0] if len(keep) else ctrl
        for lbl, r in (("control (overlay OFF)", ctrl), ("IS-Sharpe pick, UNSCREENED", unscr),
                       ("IS-Sharpe pick, NUMERAIRE-SCREENED", scr), ("OOS-best (oracle)", best_oos)):
            out.append(dict(panel=pname, arm=lbl, n=r["n"], family=r["family"], dial=r["dial"],
                            IS_Sharpe=r["IS_Sharpe"], OOS_CAGR=r["OOS_CAGR"],
                            OOS_Sharpe=r["OOS_Sharpe"], OOS_MaxDD=r["OOS_MaxDD"],
                            pass4a=r["pass4a"], pass4b=r["pass4b"]))
        print(f"\n    {pname}: menu {len(menu)} points, survivors of the screen "
              f"{int(menu['IS_beats_MATCH'].sum())} (+ control)")
    R = pd.DataFrame(out)
    R.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    print()
    print(R.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n    OOS Sharpe deltas (screened - unscreened / - control / regret vs oracle):")
    for pname, s in R.groupby("panel"):
        d = {r["arm"]: r for _, r in s.iterrows()}
        sc, un, ct, bo = (d["IS-Sharpe pick, NUMERAIRE-SCREENED"], d["IS-Sharpe pick, UNSCREENED"],
                          d["control (overlay OFF)"], d["OOS-best (oracle)"])
        print(f"      {pname:9s} screened {sc['OOS_Sharpe']:+.4f} | vs unscreened "
              f"{sc['OOS_Sharpe']-un['OOS_Sharpe']:+.4f} | vs control "
              f"{sc['OOS_Sharpe']-ct['OOS_Sharpe']:+.4f} | regret {sc['OOS_Sharpe']-bo['OOS_Sharpe']:+.4f}")
    return R


def bench_oos():
    print("\n    OOS (2017-2026) anchors, 10 bps, for the rule-8 table above:")
    for pname, px in (("U56", load_universe()), ("B136", load_universe(broad=True)),
                      ("SMALL439", small_panel())):
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        b = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq="W")
        r = (b["returns"] - b["turnover"] * 10 / 1e4).loc[start:]
        mo, so = metrics(r.loc[OOS_START:]), metrics(spy.loc[OOS_START:])
        print(f"      {pname:5s} RULES v2 OOS CAGR {mo['CAGR']:.2%} Sharpe {mo['Sharpe']:.4f} "
              f"MaxDD {mo['MaxDD']:.2%} | SPY OOS CAGR {so['CAGR']:.2%} Sharpe {so['Sharpe']:.4f} "
              f"MaxDD {so['MaxDD']:.2%}")


# ================================================================ main
def main():
    print(f"=== {SLUG}")
    print("Question: would the numeraire bar have KILLED the record's DD-improving overlay claims")
    print("ON SIGHT, and does that verdict agree with the verdict a full run produces?")
    print(f"Tuned: (1) bar version CF vs MATCH; (2) the dial, one per family {list(FAMILIES)}.")
    print(f"Reported axes: panel x n{NS} x rung {COSTS} bps -- every point written to the grid CSV.")

    gcsv, lcsv = OUT / f"{SLUG}.grid.csv", OUT / f"{SLUG}.ladder.csv"
    if RESUME and gcsv.exists() and lcsv.exists():
        g, lad = pd.read_csv(gcsv), pd.read_csv(lcsv)
        print("\n[RESUME] grid + ladder read from disk")
    else:
        g, lad = build_grid()
    parent_gate(g)
    shrink_med, shrink_lo, shrink_hi = analyse(g, lad)
    _, _, _, lb_rows = leaderboard_census()
    leaderboard_numeric(lb_rows, shrink_med)
    csv_census(shrink_med, shrink_lo, shrink_hi)
    queue_census()
    rule8(g)
    bench_oos()
    print("\n=== done")


if __name__ == "__main__":
    main()
