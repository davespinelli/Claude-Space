#!/usr/bin/env python3
"""Idea 77 - "what-predicts-a-panel": decompose idea 73's Spearman(IS Sharpe, OOS Sharpe)
= +0.710 across its 21 (panel, n) points.

The question
------------
Idea 73 killed cross-sectional DISPERSION as a universe clause: the pre-registered
dispersion rule S3 picked SMALL484 and finished last of seven out of sample, and
Spearman(IS dispersion, OOS Sharpe) over the 21 CAND points was only +0.134.  But the
same table showed Spearman(IS Sharpe, OOS Sharpe) = **+0.710**: whatever a panel is, it
is largely persistent, and an in-sample reading of it carries out of sample.  Idea 73's
own closing line was "the panel choice is predictable, dispersion just is not what
predicts it."

This run asks what IS.  Three candidate panel properties, all measured on 2009-2016 only,
all pre-registered with their sign before any OOS number was read:

    LEVEL        the panel just went up.  Sharpe (and CAGR) of the equal-weighted
                 buy-and-hold basket of the panel's tradable names - no gate, no
                 ranking, no costs.  If this is the whole story, "IS Sharpe predicts
                 OOS Sharpe" is a momentum-of-panels statement and, on
                 current-constituent lists, mostly a SURVIVORSHIP thermometer.
    CORRELATION  mean pairwise correlation of daily returns among the panel's names.
                 Pre-registered direction: LOWER correlation should be better (more
                 idiosyncratic variation for a cross-sectional rank to sort).  This is
                 idea 10's original ETF story stated without the dispersion proxy.
    PERSISTENCE  does trend actually pay in this panel.  Two forms, both reported:
                 xs_mom - mean weekly cross-sectional Spearman(12-1 momentum at t,
                          forward 1-week return), i.e. the payoff the ranked book uses;
                 ts_mom - mean across names of corr(12-1 momentum at t, that name's own
                          forward 4-week return), i.e. per-name time-series trend.

Reported alongside, for continuity and as known confounds:
    disp     idea 73's mean cross-sectional sd of 12-1 momentum over the eligible set
    n_elig   mean eligible count (idea 78 showed panel size / selectivity confounds this)
    EWall_S  IS Sharpe of the panel's own equal-weight-all-ELIGIBLE book (the gated
             level, i.e. LEVEL after RULES v1's eligibility gate)

Design
------
Every book, panel, window and convention is idea 73's, imported unchanged, so the
decomposition sits on the table it decomposes.  The run reproduces idea 73's 21-point
IS/OOS table and BOTH of its published Spearmans (+0.710 and +0.134) before any new
number is read; if they do not reproduce, nothing below means anything.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. panel (7)        2. n in {5, 10, 20}
The predictors are MEASUREMENTS of a panel, not fitted parameters: no book construction
reads any of them.  The 200d / vol20 < 0.60 gate, 75% gross, weekly rebalancing, 10 bps
and next-day execution are RULES v1's own and are held fixed everywhere.  Grid = 21 CAND
points + 7 EWall + 7 v1 = 35, ALL reported.

Statistics
    Panel properties are constant within a panel, so the 21 points carry only 7
    independent draws for them.  Every panel-level Spearman is therefore reported with an
    EXACT permutation p-value over all 5,040 orderings of 7 panels, and the 21-point
    Spearmans are labelled as descriptive.  Partial rank correlations separate the three
    candidates from each other and from IS Sharpe.  The between/within decomposition
    shows how much of +0.710 is the panel and how much is the n dial.

Walk-forward (PROTOCOL rule 8) - selectors fixed, with direction, before any OOS read
    S_LVL    highest IS level Sharpe          S_CORR   LOWEST IS mean pairwise corr
    S_XSMOM  highest IS xs momentum efficacy  S_TSMOM  highest IS ts momentum persistence
    S_DISP   highest IS dispersion (idea 73's S3, continuity)
    S_ISS    highest IS Sharpe at n=20        S1       highest IS Sharpe over all 21
    RANDOM   the mean over all 7 panels at n=20 (the expected value of a coin flip)
    NOTHING  U56 at n=20 - the project's own incumbent universe, no selection at all
    Panel selectors are read at n=20 (idea 73's S3 convention); parameters chosen on
    2009-2016, 2017-2026 read once, untouched.  Sign checks (the ARGMIN of a selector
    pre-registered as argmax, and vice versa) are reported and labelled as sign checks.

Verdicts (both KEEP paths, every point)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: all three lists are current constituents, one-directional.  It falls
hardest on STK20 / BSTK100 / SMALL484 and it inflates the LEVEL predictor by
construction, so a finding that LEVEL wins must be read as partly manufactured - stated
again in the result memo.

Deterministic, standalone.  Reads baseline.py; modifies nothing.
"""
import sys
from itertools import permutations
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import json
import numpy as np
import pandas as pd
from baseline import load_universe, score
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
W_FIXED = 0.15
NS = [5, 10, 20]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
MIN_ELIG = 5
MIN_OBS_FRAC = 0.60          # a name needs this share of the IS window to enter a panel property
SCRIPT = Path(__file__).name
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 250)


# ---------------------------------------------------------------- panels (idea 73's, verbatim)
def build_panels():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    broad_g = [t for t in U["broad"] if t not in crypto]
    sect_g = [t for t in U["sectors"] if t not in crypto]
    bfc_g = [t for t in U["bonds_fx_commod"] if t not in crypto]
    stk_g = [t for t in U["megacap"] if t not in crypto]

    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)

    etf36 = broad_g + sect_g + bfc_g
    etf24 = broad_g + sect_g
    b_stk = [t for t in px136.columns if t not in set(etf36)]
    s_stk = [c for c in pxs.columns if c != "SPY"]

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        return p, set(tradable if tradable is not None else cols)

    return {
        "U56":      sub(px56, list(px56.columns)),
        "ETF36":    sub(px56, etf36),
        "ETF24":    sub(px56, etf24),
        "STK20":    sub(px56, stk_g, tradable=stk_g),
        "B136":     sub(px136, list(px136.columns)),
        "BSTK100":  sub(px136, b_stk, tradable=b_stk),
        "SMALL484": sub(pxs, s_stk, tradable=s_stk),
    }


# ---------------------------------------------------------------- books (idea 73's, verbatim)
def eligible_mask(px, tradable):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def weights(px, tradable, kind, n=None):
    if kind == "v1":
        s = score(px, vol_scale=True)[0]
        rank = s.where(eligible_mask(px, tradable)).rank(axis=1, ascending=False)
        return (rank <= 5).astype(float) * W_FIXED
    elig = eligible_mask(px, tradable)
    if kind == "EWall":
        cnt = elig.sum(axis=1).replace(0, np.nan)
        return elig.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)
    s = score(px, vol_scale=False)[0]
    rank = s.where(elig).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


def dispersion_frame(px, tradable):
    mom = px.shift(21) / px.shift(252) - 1
    elig = eligible_mask(px, tradable)
    mask = rebalance_mask(px.index, FREQ)
    m = mom.where(elig)[mask.values]
    n = m.count(axis=1)
    out = pd.DataFrame({"n_elig": n, "sd": m.std(axis=1)})
    return out.where(out["n_elig"] >= MIN_ELIG)


# ---------------------------------------------------------------- panel properties (new)
def panel_properties(px, tradable, start, end):
    """Every property measured on [start, end] only (the IS window when called that way).

    level_S / level_C  equal-weighted buy-and-hold of the tradable names, daily rebalanced,
                       no gate, no ranking, no costs.
    corr               mean off-diagonal pairwise correlation of daily returns.
    xs_mom             mean over weekly rebalance dates of the cross-sectional Spearman
                       between 12-1 momentum at t and the forward 1-week return.
    ts_mom             mean across names of Pearson corr(12-1 momentum at t, that name's
                       own forward 4-week return) over the weekly dates.
    A name enters only if it has >= MIN_OBS_FRAC of the window's days with a live price.
    """
    cols = [c for c in px.columns if c in tradable]
    p = px[cols].loc[start:end]
    live = p.notna().mean()
    cols = [c for c in cols if live[c] >= MIN_OBS_FRAC]
    p = p[cols]
    rets = p.pct_change()

    ew = rets.mean(axis=1).fillna(0.0)
    m_ew = metrics(ew)

    cm = rets.corr()
    iu = np.triu_indices_from(cm.values, k=1)
    corr = float(np.nanmean(cm.values[iu]))

    # momentum needs a 252d look-back: compute on the full series, then restrict to window
    full = px[cols]
    mom_full = full.shift(21) / full.shift(252) - 1
    mask = rebalance_mask(full.index, FREQ)
    dates = full.index[mask.values]
    dates = dates[(dates >= pd.Timestamp(start)) & (dates <= pd.Timestamp(end))]
    mom = mom_full.loc[dates]
    fwd1 = full.loc[dates].pct_change().shift(-1)                       # t -> t+1 week
    fwd4 = full.loc[dates].pct_change(4).shift(-4)                      # t -> t+4 weeks

    xs = []
    for d in dates:
        a, b = mom.loc[d], fwd1.loc[d]
        ok = a.notna() & b.notna()
        if ok.sum() >= MIN_ELIG:
            xs.append(np.corrcoef(a[ok].rank(), b[ok].rank())[0, 1])
    xs_mom = float(np.nanmean(xs)) if xs else np.nan

    ts = []
    for c in cols:
        a, b = mom[c], fwd4[c]
        ok = a.notna() & b.notna()
        if ok.sum() >= 30 and a[ok].std() > 0 and b[ok].std() > 0:
            ts.append(np.corrcoef(a[ok], b[ok])[0, 1])
    ts_mom = float(np.nanmean(ts)) if ts else np.nan

    return dict(n_names=len(cols), level_S=m_ew["Sharpe"], level_C=m_ew["CAGR"],
                corr=corr, xs_mom=xs_mom, ts_mom=ts_mom)


# ---------------------------------------------------------------- stats helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def verdict_4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def fail_4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def spearman(a, b):
    a, b = pd.Series(list(a)), pd.Series(list(b))
    ok = a.notna() & b.notna()
    if ok.sum() < 3:
        return np.nan
    return float(np.corrcoef(a[ok].rank(), b[ok].rank())[0, 1])


def perm_p(x, y):
    """Exact two-sided permutation p for Spearman over a small vector (7! = 5040)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) > 8 or np.isnan(x).any() or np.isnan(y).any():
        return np.nan
    obs = abs(spearman(x, y))
    ry = pd.Series(y).rank().values
    rx = pd.Series(x).rank().values
    hits = tot = 0
    for pm in permutations(range(len(x))):
        s = abs(float(np.corrcoef(rx[list(pm)], ry)[0, 1]))
        hits += s >= obs - 1e-12
        tot += 1
    return hits / tot


def partial_spearman(a, b, c):
    """Rank partial correlation of a and b controlling for c."""
    ra, rb, rc = (pd.Series(list(v)).rank().values for v in (a, b, c))
    rab = np.corrcoef(ra, rb)[0, 1]
    rac = np.corrcoef(ra, rc)[0, 1]
    rbc = np.corrcoef(rb, rc)[0, 1]
    den = np.sqrt(max((1 - rac ** 2) * (1 - rbc ** 2), 1e-12))
    return float((rab - rac * rbc) / den)


def fmt(df, p=3):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- main
def main():
    panels = build_panels()

    print("=" * 200)
    print(f"Idea 77 what-predicts-a-panel (lane B) | {SCRIPT} | {COST_BPS} bps, weekly, next-day execution")
    print("=" * 200)

    px56 = panels["U56"][0]
    yrs = px56.index.to_series().groupby(px56.index.year).count()
    print(f"Index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)

    print("\nPanels:")
    for k, (p, tr) in panels.items():
        print(f"  {k:<9} {len(tr):>3} tradable ({p.shape[1]} cols incl. benchmark)  {p.index[0].date()} -> {p.index[-1].date()}")

    books = [("EWall", None), ("v1", None)] + [("CAND", n) for n in NS]
    res, turn = {}, {}
    for pk, (p, tr) in panels.items():
        for kind, n in books:
            w = weights(p, tr, kind, n)
            r = backtest(p, w, cost_bps=COST_BPS, freq=FREQ)
            key = (pk, kind if n is None else f"CAND{n}")
            res[key] = r["returns"]
            turn[key] = r["turnover"]

    start56 = px56.index[260]
    print("\n--- harness sanity (universe.json window, must match published rows) ---")
    for key, want in [(("U56", "CAND20"), "idea 2 KEEP: 12.7% / 1.093 / -18.3%, halves 1.088/1.103"),
                      (("U56", "v1"), "live v1: 6.5% / 0.666 / -13.8%")]:
        r = res[key].loc[start56:]
        m = metrics(r); h1, h2 = half_sharpes(r)
        print(f"  {key[0]}/{key[1]:<7} {m['CAGR']:.1%} / {m['Sharpe']:.3f} / {m['MaxDD']:.1%}  halves {h1:.3f}/{h2:.3f}   [{want}]")

    start = max(p.index[260] for p, _ in panels.values())
    end = min(p.index[-1] for p, _ in panels.values())
    spy = px56["SPY"].pct_change().fillna(0).loc[start:end]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    ms, ms_is, ms_oos = metrics(spy), metrics(spy_is), metrics(spy_oos)
    cut = lambda s: s.loc[start:end]
    print(f"\nCommon evaluation window (all panels, identical days): {start.date()} -> {end.date()} ({len(spy)} days)")
    print(f"SPY on it: {ms['CAGR']:.1%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.1%}  halves "
          f"{half_sharpes(spy)[0]:.3f}/{half_sharpes(spy)[1]:.3f}  IS {ms_is['Sharpe']:.3f}  OOS {ms_oos['Sharpe']:.3f}")
    print(f"4b bars (full): MaxDD <= {0.60 * abs(ms['MaxDD']):.1%}, CAGR >= {0.70 * ms['CAGR']:.2%}")

    disp = {pk: dispersion_frame(p, tr).loc[start:end] for pk, (p, tr) in panels.items()}

    # ============================================================ 0. REPRODUCE idea 73
    print("\n" + "=" * 200)
    print("0. REPRODUCTION GATE - idea 73's 21 CAND points, IS vs OOS, and its two published Spearmans")
    print("=" * 200)
    rows = []
    for pk in panels:
        for n in NS:
            r = cut(res[(pk, f"CAND{n}")])
            ri, ro = r.loc[:IS_END], r.loc[OOS_START:]
            mi, mo = metrics(ri), metrics(ro)
            rows.append(dict(panel=pk, n=n, IS_disp=disp[pk].loc[:IS_END]["sd"].mean(),
                             IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                             OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"]))
    pts = pd.DataFrame(rows)
    print(fmt(pts.set_index(["panel", "n"])))
    sp_is = spearman(pts["IS_Sharpe"], pts["OOS_Sharpe"])
    sp_dp = spearman(pts["IS_disp"], pts["OOS_Sharpe"])
    print(f"\n  Spearman(IS Sharpe, OOS Sharpe) over 21 points = {sp_is:+.3f}   [idea 73 published +0.710]")
    print(f"  Spearman(IS dispersion, OOS Sharpe) over 21 points = {sp_dp:+.3f}   [idea 73 published +0.134]")
    ok = abs(sp_is - 0.710) < 0.005 and abs(sp_dp - 0.134) < 0.005
    print(f"  REPRODUCTION: {'EXACT' if ok else '*** MISMATCH - everything below is on a different harness ***'}")

    # ============================================================ 1. panel properties, IS only
    print("\n" + "=" * 200)
    print("1. PANEL PROPERTIES, measured on the IS window (2009-2016 portion of the common window) ONLY")
    print("=" * 200)
    prop = {}
    for pk, (p, tr) in panels.items():
        d = panel_properties(p, tr, start, IS_END)
        d["disp"] = disp[pk].loc[:IS_END]["sd"].mean()
        d["n_elig"] = disp[pk].loc[:IS_END]["n_elig"].mean()
        d["EWall_S"] = metrics(cut(res[(pk, "EWall")]).loc[:IS_END])["Sharpe"]
        prop[pk] = d
    ptab = pd.DataFrame(prop).T
    ptab.index.name = "panel"
    # panel-level OOS summary at n=20 and averaged over n
    ptab["ISsh_n20"] = [pts[(pts.panel == pk) & (pts.n == 20)]["IS_Sharpe"].iloc[0] for pk in ptab.index]
    ptab["OOSsh_n20"] = [pts[(pts.panel == pk) & (pts.n == 20)]["OOS_Sharpe"].iloc[0] for pk in ptab.index]
    ptab["OOSsh_meanN"] = [pts[pts.panel == pk]["OOS_Sharpe"].mean() for pk in ptab.index]
    print(fmt(ptab.sort_values("level_S", ascending=False), 4))
    print("\n  level_S/level_C = EW buy-and-hold of the panel's tradable names (no gate, no costs), IS window.")
    print("  corr = mean pairwise daily-return correlation.  xs_mom = mean weekly cross-sectional Spearman")
    print("  (12-1 momentum, forward 1w return).  ts_mom = mean per-name corr(12-1 momentum, own forward 4w return).")

    # ============================================================ 2. the horse race
    print("\n" + "=" * 200)
    print("2. WHAT PREDICTS OOS SHARPE?  Each candidate against the same OOS column")
    print("=" * 200)
    preds = ["level_S", "level_C", "corr", "xs_mom", "ts_mom", "disp", "n_elig", "EWall_S", "ISsh_n20"]
    race = []
    for k in preds:
        x21 = [prop[pk][k] if k in prop[pk] else ptab.loc[pk, k] for pk in pts["panel"]]
        row = dict(predictor=k,
                   rho_21=spearman(x21, pts["OOS_Sharpe"]),
                   rho_7_n20=spearman(ptab[k], ptab["OOSsh_n20"]),
                   rho_7_meanN=spearman(ptab[k], ptab["OOSsh_meanN"]))
        row["perm_p_n20"] = perm_p(ptab[k].values, ptab["OOSsh_n20"].values)
        row["perm_p_meanN"] = perm_p(ptab[k].values, ptab["OOSsh_meanN"].values)
        race.append(row)
    # the incumbent, 21 points, for the top line
    race.append(dict(predictor="IS_Sharpe(21pt)", rho_21=sp_is, rho_7_n20=np.nan,
                     rho_7_meanN=np.nan, perm_p_n20=np.nan, perm_p_meanN=np.nan))
    rtab = pd.DataFrame(race).set_index("predictor")
    print(fmt(rtab, 3))
    print("\n  rho_21 is DESCRIPTIVE ONLY: panel properties are constant within a panel, so the 21 points")
    print("  carry 7 independent draws.  perm_p is the EXACT two-sided permutation p over all 5,040")
    print("  orderings of 7 panels and is the honest test.  With N=7 the smallest attainable p is 2/5040.")

    # ============================================================ 3. between vs within
    print("\n" + "=" * 200)
    print("3. IS +0.710 THE PANEL OR THE n DIAL?  between/within decomposition")
    print("=" * 200)
    bet = pts.groupby("panel")[["IS_Sharpe", "OOS_Sharpe"]].mean()
    print("\n  Panel means over the 3 n values:")
    print(fmt(bet, 3))
    print(f"  BETWEEN panels (N=7): Spearman(mean IS Sharpe, mean OOS Sharpe) = "
          f"{spearman(bet['IS_Sharpe'], bet['OOS_Sharpe']):+.3f}  "
          f"(exact perm p = {perm_p(bet['IS_Sharpe'].values, bet['OOS_Sharpe'].values):.4f})")
    wr = []
    for pk in panels:
        s = pts[pts.panel == pk]
        wr.append(dict(panel=pk, rho_within=spearman(s["IS_Sharpe"], s["OOS_Sharpe"]),
                       IS_best_n=int(s.sort_values("IS_Sharpe", ascending=False)["n"].iloc[0]),
                       OOS_best_n=int(s.sort_values("OOS_Sharpe", ascending=False)["n"].iloc[0])))
    wtab = pd.DataFrame(wr).set_index("panel")
    print("\n  WITHIN each panel, across n in {5,10,20} (3 points each):")
    print(fmt(wtab, 3))
    a = pts["IS_Sharpe"] - pts.groupby("panel")["IS_Sharpe"].transform("mean")
    b = pts["OOS_Sharpe"] - pts.groupby("panel")["OOS_Sharpe"].transform("mean")
    print(f"  pooled panel-demeaned Spearman(IS, OOS) over 21 points = {spearman(a, b):+.3f}   "
          f"IS argmax n matches OOS argmax n in {int((wtab.IS_best_n == wtab.OOS_best_n).sum())} of 7 panels")

    # ============================================================ 4. partial rank correlations
    print("\n" + "=" * 200)
    print("4. PARTIAL RANK CORRELATIONS (N=7 panels, n=20 column) - which candidate survives the others")
    print("=" * 200)
    y = ptab["OOSsh_n20"]
    cands = ["level_S", "corr", "xs_mom", "ts_mom", "disp", "n_elig", "EWall_S", "ISsh_n20"]
    P = pd.DataFrame(index=cands, columns=["rho"] + [f"|{c}" for c in cands], dtype=float)
    for a_ in cands:
        P.loc[a_, "rho"] = spearman(ptab[a_], y)
        for c_ in cands:
            P.loc[a_, f"|{c_}"] = np.nan if a_ == c_ else partial_spearman(ptab[a_], y, ptab[c_])
    print(fmt(P, 3))
    print("\n  Row = predictor's Spearman with OOS Sharpe; column '|X' = the same after controlling for X.")
    print("  A predictor that survives control for the others is the mechanism; one that collapses is a proxy.")

    # ============================================================ 5. rule 8 walk-forward
    print("\n" + "=" * 200)
    print("5. RULE 8 WALK-FORWARD - selectors fixed with direction before any OOS number was read")
    print("=" * 200)
    n20 = pts[pts.n == 20].set_index("panel")
    sel = {
        "S_LVL":   ("level_S",  "max", "highest IS level Sharpe"),
        "S_CORR":  ("corr",     "min", "LOWEST IS mean pairwise correlation"),
        "S_XSMOM": ("xs_mom",   "max", "highest IS cross-sectional momentum efficacy"),
        "S_TSMOM": ("ts_mom",   "max", "highest IS per-name trend persistence"),
        "S_DISP":  ("disp",     "max", "highest IS dispersion (idea 73's S3)"),
        "S_ISS":   ("ISsh_n20", "max", "highest IS Sharpe at n=20"),
    }
    base_oos = cut(res[("U56", "v1")]).loc[OOS_START:]
    mb = metrics(base_oos)
    wf = []

    def oos_row(tag, pk, n, note):
        r = cut(res[(pk, f"CAND{n}")]).loc[OOS_START:]
        m = metrics(r)
        return dict(rule=tag, pick=f"{pk}/CAND{n}", OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"],
                    OOS_MaxDD=m["MaxDD"], vs_SPY=m["Sharpe"] - ms_oos["Sharpe"],
                    vs_v1=m["Sharpe"] - mb["Sharpe"],
                    OOS_4b="PASS" if (m["Sharpe"] > ms_oos["Sharpe"] and
                                      abs(m["MaxDD"]) <= 0.60 * abs(ms_oos["MaxDD"]) and
                                      m["CAGR"] >= 0.70 * ms_oos["CAGR"]) else "FAIL", note=note)

    print("\n  Picks (from IS data only):")
    for tag, (k, how, note) in sel.items():
        pk = ptab[k].idxmax() if how == "max" else ptab[k].idxmin()
        print(f"    {tag:<7} {note:<48} -> {pk:<9} (IS {k} = {ptab.loc[pk, k]:+.4f})")
        wf.append(oos_row(tag, pk, 20, note))
    s1 = pts.sort_values(["IS_Sharpe", "n"], ascending=[False, True]).iloc[0]
    print(f"    {'S1':<7} {'highest IS Sharpe over all 21 points (idea 73 S1)':<48} -> "
          f"{s1['panel']}/n={int(s1['n'])} (IS {s1['IS_Sharpe']:.3f})")
    wf.append(oos_row("S1", s1["panel"], int(s1["n"]), "idea 73's S1"))
    wf.append(oos_row("NOTHING", "U56", 20, "incumbent universe, no selection"))
    wtab2 = pd.DataFrame(wf).set_index("rule")
    rnd_mean = n20["OOS_Sharpe"].mean(); rnd_sd = n20["OOS_Sharpe"].std()
    print("\n  Out of sample (2017-2026), read once:")
    print(fmt(wtab2.drop(columns=["note"]), 3))
    print(f"\n  RANDOM control (mean over the 7 panels at n=20): OOS Sharpe {rnd_mean:.3f} (sd {rnd_sd:.3f}); "
          f"OOS CAGR {n20['OOS_CAGR'].mean():.1%}; OOS MaxDD {n20['OOS_MaxDD'].mean():.1%}")
    print(f"  SPY OOS: {ms_oos['CAGR']:.1%} / {ms_oos['Sharpe']:.3f} / {ms_oos['MaxDD']:.1%}  "
          f"(4b OOS bars: DD <= {0.60 * abs(ms_oos['MaxDD']):.1%}, CAGR >= {0.70 * ms_oos['CAGR']:.2%})")
    print(f"  RULES v1 baseline OOS (U56): {mb['CAGR']:.1%} / {mb['Sharpe']:.3f} / {mb['MaxDD']:.1%}")
    print("\n  Selection premium over a coin flip (OOS Sharpe minus the 7-panel mean at n=20):")
    for _, r_ in wtab2.iterrows():
        print(f"    {r_.name:<8} {r_['OOS_Sharpe'] - rnd_mean:+.3f}")

    print("\n  SIGN CHECKS (the opposite extreme of each pre-registered selector; labelled, not selected):")
    sc = []
    for tag, (k, how, _) in sel.items():
        pk = ptab[k].idxmin() if how == "max" else ptab[k].idxmax()
        sc.append(oos_row(tag + "^rev", pk, 20, "sign check"))
    print(fmt(pd.DataFrame(sc).set_index("rule").drop(columns=["note"]), 3))

    # ============================================================ 6. full grid, both KEEP paths
    print("\n" + "=" * 200)
    print("6. ALL 35 POINTS on the common window - both KEEP paths (idea 73's grid, re-reported)")
    print("=" * 200)
    grid = []
    for pk in panels:
        basep = cut(res[(pk, "v1")])
        ewa = cut(res[(pk, "EWall")])
        for bk in ["v1", "EWall"] + [f"CAND{n}" for n in NS]:
            r = cut(res[(pk, bk)])
            m = metrics(r); h1, h2 = half_sharpes(r)
            grid.append(dict(panel=pk, book=bk, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                             H1=h1, H2=h2, OOS=metrics(r.loc[OOS_START:])["Sharpe"],
                             turn=turn[(pk, bk)].loc[start:end].sum() / m["Years"],
                             dS_vs_EW=m["Sharpe"] - metrics(ewa)["Sharpe"],
                             p4a="Y" if verdict_4a(r, basep) else "n",
                             f4b=fail_4b(r, spy, r.loc[OOS_START:], spy_oos)))
    gtab = pd.DataFrame(grid).set_index(["panel", "book"])
    print(fmt(gtab))

    # ============================================================ 7. CSVs + leaderboard
    stem = SCRIPT.replace(".py", "")
    ptab.to_csv(OUT / f"{stem}.properties.csv")
    rtab.to_csv(OUT / f"{stem}.race.csv")
    P.to_csv(OUT / f"{stem}.partial.csv")
    wtab2.to_csv(OUT / f"{stem}.walkforward.csv")
    gtab.to_csv(OUT / f"{stem}.grid.csv")
    pts.to_csv(OUT / f"{stem}.points.csv", index=False)

    print("\n" + "=" * 200)
    print("7. LEADERBOARD ROWS (common window; baseline = that panel's own RULES v1 book)")
    print("=" * 200)
    today = pd.Timestamp.today().date()
    for pk in panels:
        basep = cut(res[(pk, "v1")])
        bm = metrics(basep); b1, b2 = half_sharpes(basep)
        for bk in [f"CAND{n}" for n in NS]:
            r = cut(res[(pk, bk)])
            m = metrics(r); h1, h2 = half_sharpes(r)
            f = fail_4b(r, spy, r.loc[OOS_START:], spy_oos)
            v = ("KEEP 4b" if f == "-" else f"KILL 4b ({f})")
            if verdict_4a(r, basep):
                v = "4a-pass, " + v
            print(f"| {today} | 77 {pk}/{bk} (IS lvl_S {ptab.loc[pk, 'level_S']:.2f}, corr {ptab.loc[pk, 'corr']:.2f}, "
                  f"xs_mom {ptab.loc[pk, 'xs_mom']:+.3f}) | {m['CAGR']:.1%} | {m['Sharpe']:.2f} | {m['MaxDD']:.1%} | "
                  f"{h1:.2f} / {h2:.2f} | {bm['Sharpe']:.2f} ({b1:.2f}/{b2:.2f}) | {v} | {SCRIPT} |")


if __name__ == "__main__":
    main()
