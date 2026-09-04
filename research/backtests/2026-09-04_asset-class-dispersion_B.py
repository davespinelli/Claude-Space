#!/usr/bin/env python3
"""Idea 73 - "asset-class-dispersion": does the payoff to RANKING track cross-sectional
momentum dispersion, and can dispersion be used to decide which panels a momentum rule
may be run on at all?

The question
------------
Idea 10 killed the ETF-only book and left a mechanism claim untested: the ETF panel lost
-6.15%/yr for only -1.3pp of vol, i.e. return fell more than risk.  The natural
explanation is that 36 sector/bond/commodity ETFs are too similar to each other for a
cross-sectional rank to have anything to sort: if every candidate has nearly the same
12-1 momentum, picking the top 5 of them is picking noise, and you pay turnover for it.

That is a testable statement about DISPERSION, not about ETFs.  This run measures the
cross-sectional dispersion of 12-1 momentum in every panel the project has, and tests
whether the payoff to ranking tracks it:

    (a) ACROSS PANELS - is a panel's ranking premium ordered by its dispersion?
    (b) WITHIN A PANEL, OVER TIME - inside one panel, do high-dispersion weeks pay the
        ranked book better than low-dispersion weeks?  This is the stronger test: it
        holds the panel, its names and its survivorship exposure fixed, and it has
        hundreds of observations instead of seven.
    (c) OUT OF SAMPLE - can dispersion measured on 2009-2016 pick the panel that a
        ranked book should be run on in 2017-2026?  (Rule 8, selection rule S3.)

The dependent variable is the RANKING PREMIUM, not raw Sharpe.  Raw Sharpe of a book on
a panel confounds "the ranking works here" with "this panel went up".  The premium is
measured against the same panel's own equal-weight-all-eligible book, which holds the
universe, the eligibility gate, the gross and the days fixed and differs only in whether
the composite is used to pick a subset.  Two versions are reported:

    net Sharpe premium   Sharpe(CAND-n) - Sharpe(EWall), 10 bps, t+1  ... what a book earns
    gross signal spread  mean forward 1-week return of the top-n eligible minus the
                         equal-weighted eligible set, no costs, no drift ... the pure
                         selection payoff, which is what dispersion should govern

Panels (parameter 1 of 2) - all reported, none picked on its own result
    U56      universe.json, 56 names ex-crypto ................. incumbent control
    ETF36    universe.json ETFs only ......................... idea 10's best ETF arm
    ETF24    broad + sector ETFs only ........................ idea 10's literal arm
    STK20    universe.json mega-cap single stocks ............. idea 10's complement
    B136     universe_broad.json, all names .................. second incumbent control
    BSTK100  universe_broad.json single stocks only
    SMALL484 data/prices_small.csv, sub-$2B panel ............. the dispersion extreme
SPY is joined as a benchmark column to every panel and is NOT tradable in the stock-only
panels or in SMALL484.

Books - structural variants, not tuned choices, all reported
    EWall    equal-weight ALL eligible names at 75% gross, no ranking .... the control
    CAND-n   idea 2's construction: top-n eligible equal-weight at 75% gross, composite
             WITHOUT /sqrt(vol20).  n is parameter 2.
    v1       RULES v1 exactly as live (top 5, /sqrt(vol20), 15% each) ... reported for
             continuity with the leaderboard; not part of the dispersion test.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. panel     2. n in {5, 10, 20}
The 200d / vol20 < 0.60 gate, 75% gross, weekly rebalancing, 10 bps and next-day
execution are RULES v1's own and are held fixed everywhere.  Dispersion is a MEASUREMENT
of each panel, not a fitted parameter: nothing in the book construction reads it.

Grid = 7 panels x (EWall + 3 CAND n + v1) = 35 points, ALL reported.

Sample.  The primary cross-panel comparison runs every panel on the SAME days (common
window = the latest panel's warm-up end, driven by SMALL484's 2010 start), because a
Sharpe comparison across panels on different samples is not a comparison.  The large
panels are ALSO reported on universe.json's own window so the numbers line up with the
published leaderboard rows, and the harness reproduces idea 2's KEEP row there before
any new number is read.

Walk-forward (PROTOCOL rule 8) - selection rules fixed before any OOS number was read
    S1 (Sharpe):     over the 21 CAND points, the (panel, n) with the highest 2009-2016
                     Sharpe; ties -> smaller n.
    S2 (4b-aware):   the same, restricted to points whose in-sample MaxDD is within 60%
                     of SPY's in-sample MaxDD.
    S3 (dispersion): the PRE-REGISTERED TEST OF THIS IDEA - at fixed n=20, the panel with
                     the highest in-sample mean eligible-set dispersion.  If dispersion
                     is a usable universe clause, S3 should land on a panel whose OOS
                     ranked book is at or near the best; if it lands on a bad panel, the
                     clause does not belong in RULES however well dispersion correlates
                     in-sample.
Parameters chosen on 2009-2016 only; 2017-2026 read once, untouched.

Verdicts (both KEEP paths, every point)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

Survivorship: current constituents of all three lists, one-directional.  It falls
hardest on STK20/BSTK100/SMALL484 - the high-dispersion panels - which biases this run
TOWARD finding that dispersion pays.  Stated again in the result memo.

Deterministic, standalone.  Reads baseline.py; modifies nothing.
"""
import sys
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
MIN_ELIG = 5            # a cross-section smaller than this has no dispersion to speak of
SCRIPT = Path(__file__).name

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 250)


# ---------------------------------------------------------------- panels
def build_panels():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    broad_g = [t for t in U["broad"] if t not in crypto]
    sect_g = [t for t in U["sectors"] if t not in crypto]
    bfc_g = [t for t in U["bonds_fx_commod"] if t not in crypto]
    stk_g = [t for t in U["megacap"] if t not in crypto]

    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)                      # joins SPY as benchmark itself

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


# ---------------------------------------------------------------- book construction
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


# ---------------------------------------------------------------- dispersion
def dispersion_frame(px, tradable):
    """Weekly cross-sectional dispersion of 12-1 momentum over the ELIGIBLE set.

    Returns a DataFrame indexed on rebalance dates with
        n_elig  names eligible that week
        sd      cross-sectional std of 12-1 momentum
        iqr     cross-sectional p75-p25 of the same
        sd_n    sd normalised by the median annualised vol20 of the eligible names,
                scaled to the momentum window (sqrt(231/252) of a year) - removes the
                mechanical part of dispersion that is just "these names are volatile"
    """
    mom = px.shift(21) / px.shift(252) - 1
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    elig = eligible_mask(px, tradable)
    mask = rebalance_mask(px.index, FREQ)
    m = mom.where(elig)[mask.values]
    v = vol20.where(elig)[mask.values]
    n = m.count(axis=1)
    sd = m.std(axis=1)
    iqr = m.quantile(0.75, axis=1) - m.quantile(0.25, axis=1)
    scale = v.median(axis=1) * np.sqrt(231 / 252)
    out = pd.DataFrame({"n_elig": n, "sd": sd, "iqr": iqr, "sd_n": sd / scale})
    return out.where(out["n_elig"] >= MIN_ELIG)


def signal_spread(px, tradable, n):
    """Weekly gross selection payoff: forward 1-week return of the equal-weighted top-n
    eligible minus the equal-weighted whole eligible set.  No costs, no drift, no
    execution model - this is the pure ranking payoff the dispersion story is about.
    Signal at t, return from t to the next rebalance date (t+1 execution is not modelled
    here; the same one-week lag applies to both legs so the difference is unaffected)."""
    elig = eligible_mask(px, tradable)
    s = score(px, vol_scale=False)[0].where(elig)
    rank = s.rank(axis=1, ascending=False)
    mask = rebalance_mask(px.index, FREQ)
    dates = px.index[mask.values]
    fwd = px.loc[dates].pct_change().shift(-1)           # date t -> return t..t+1 week
    top = rank.loc[dates] <= n
    el = elig.loc[dates]
    a = fwd.where(top).mean(axis=1)
    b = fwd.where(el).mean(axis=1)
    ok = el.sum(axis=1) >= MIN_ELIG
    return (a - b).where(ok)


# ---------------------------------------------------------------- metric helpers
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


def paired_t(a, b):
    d = (a - b).dropna()
    if len(d) < 3 or d.std() == 0:
        return 0.0, 0.0
    return d.mean() / (d.std() / np.sqrt(len(d))), d.mean() * 252


def one_t(d):
    d = pd.Series(d).dropna()
    if len(d) < 3 or d.std() == 0:
        return 0.0
    return d.mean() / (d.std() / np.sqrt(len(d)))


def spearman(a, b):
    a, b = pd.Series(a), pd.Series(b)
    ok = a.notna() & b.notna()
    if ok.sum() < 3:
        return np.nan
    return float(np.corrcoef(a[ok].rank(), b[ok].rank())[0, 1])


def fmt(df, p=3):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- main
def main():
    panels = build_panels()

    print("=" * 200)
    print(f"Idea 73 asset-class-dispersion (lane B) | {SCRIPT} | {COST_BPS} bps, weekly, next-day execution")
    print("=" * 200)

    px56 = panels["U56"][0]
    yrs = px56.index.to_series().groupby(px56.index.year).count()
    print(f"Index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)

    print("\nPanels:")
    for k, (p, tr) in panels.items():
        print(f"  {k:<9} {len(tr):>3} tradable ({p.shape[1]} cols incl. benchmark)  {p.index[0].date()} -> {p.index[-1].date()}")

    # ---------------- run every (panel, book) once, keep the daily return series
    books = [("EWall", None), ("v1", None)] + [("CAND", n) for n in NS]
    res = {}
    turn = {}
    for pk, (p, tr) in panels.items():
        for kind, n in books:
            w = weights(p, tr, kind, n)
            r = backtest(p, w, cost_bps=COST_BPS, freq=FREQ)
            key = (pk, kind if n is None else f"CAND{n}")
            res[key] = r["returns"]
            turn[key] = r["turnover"]

    # ---------------- harness sanity on universe.json's own window
    start56 = px56.index[260]
    spy56 = px56["SPY"].pct_change().fillna(0).loc[start56:]
    print("\n--- harness sanity (universe.json window, must match published rows) ---")
    for key, want in [(("U56", "CAND20"), "idea 2 KEEP: 12.7% / 1.093 / -18.3%, halves 1.088/1.103"),
                      (("U56", "v1"), "live v1: 6.5% / 0.666 / -13.8%")]:
        r = res[key].loc[start56:]
        m = metrics(r); h1, h2 = half_sharpes(r)
        print(f"  {key[0]}/{key[1]:<7} {m['CAGR']:.1%} / {m['Sharpe']:.3f} / {m['MaxDD']:.1%}  halves {h1:.3f}/{h2:.3f}   [{want}]")
    m = metrics(spy56)
    print(f"  SPY        {m['CAGR']:.1%} / {m['Sharpe']:.3f} / {m['MaxDD']:.1%}")

    # ---------------- common window (same days for every panel)
    start = max(p.index[260] for p, _ in panels.values())
    end = min(p.index[-1] for p, _ in panels.values())
    spy = px56["SPY"].pct_change().fillna(0).loc[start:end]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    ms, ms_is, ms_oos = metrics(spy), metrics(spy_is), metrics(spy_oos)
    print(f"\nCommon evaluation window (all panels, identical days): {start.date()} -> {end.date()}  "
          f"({len(spy)} days)   [large-panel-only window would start {start56.date()}]")
    print(f"SPY on it: {ms['CAGR']:.1%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.1%}  halves "
          f"{half_sharpes(spy)[0]:.3f}/{half_sharpes(spy)[1]:.3f}  IS {ms_is['Sharpe']:.3f}  OOS {ms_oos['Sharpe']:.3f}")
    print(f"4b bars on this window: MaxDD <= {0.60 * abs(ms['MaxDD']):.1%}, CAGR >= {0.70 * ms['CAGR']:.2%}")

    cut = lambda s: s.loc[start:end]

    # ---------------- 1. dispersion of every panel
    print("\n" + "=" * 200)
    print("1. CROSS-SECTIONAL DISPERSION OF 12-1 MOMENTUM, eligible set only, weekly, common window")
    print("=" * 200)
    disp = {}
    rows = []
    for pk, (p, tr) in panels.items():
        d = dispersion_frame(p, tr).loc[start:end]
        disp[pk] = d
        dh = d.loc[:IS_END]
        rows.append(dict(panel=pk, n_tradable=len(tr), n_elig=d["n_elig"].mean(),
                         sd=d["sd"].mean(), sd_med=d["sd"].median(), iqr=d["iqr"].mean(),
                         sd_norm=d["sd_n"].mean(), sd_IS=dh["sd"].mean(),
                         sd_H1=d["sd"].iloc[:len(d) // 2].mean(), sd_H2=d["sd"].iloc[len(d) // 2:].mean(),
                         weeks=int(d["sd"].notna().sum())))
    dtab = pd.DataFrame(rows).set_index("panel").sort_values("sd", ascending=False)
    print(fmt(dtab))
    print("\nsd = cross-sectional std of 12-1 momentum among eligible names; sd_norm divides it by the "
          "median annualised vol20 of those names (scaled to the 11-month window), removing the part of "
          "dispersion that is mechanically 'these are volatile names'.")

    # ---------------- 2. every point, both KEEP paths
    print("\n" + "=" * 200)
    print("2. ALL 35 POINTS on the common window (7 panels x 5 books) - both KEEP paths")
    print("=" * 200)
    grid = []
    for pk in panels:
        base = cut(res[(pk, "v1")])
        ewa = cut(res[(pk, "EWall")])
        for bk in ["v1", "EWall"] + [f"CAND{n}" for n in NS]:
            r = cut(res[(pk, bk)])
            m = metrics(r); h1, h2 = half_sharpes(r)
            t, ann = paired_t(r, ewa)
            grid.append(dict(panel=pk, book=bk, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                             H1=h1, H2=h2, OOS=metrics(r.loc[OOS_START:])["Sharpe"],
                             turn=turn[(pk, bk)].loc[start:end].sum() / m["Years"],
                             dS_vs_EW=m["Sharpe"] - metrics(ewa)["Sharpe"],
                             dCAGR_vs_EW=ann, t=t,
                             p4a="Y" if verdict_4a(r, base) else "n",
                             f4b=fail_4b(r, spy, r.loc[OOS_START:], spy_oos)))
    gtab = pd.DataFrame(grid).set_index(["panel", "book"])
    print(fmt(gtab))
    print("\ndS_vs_EW / dCAGR_vs_EW / t = the RANKING PREMIUM: this book minus the same panel's "
          "equal-weight-all-eligible book, same days, same gate, same gross.  f4b '-' = passes 4b.")

    # ---------------- 3. does the premium track dispersion, ACROSS panels?
    print("\n" + "=" * 200)
    print("3. TEST (a): ACROSS PANELS - premium vs dispersion (n=7 panels; report, do not over-read)")
    print("=" * 200)
    for n in NS:
        rows = []
        for pk in panels:
            r = cut(res[(pk, f"CAND{n}")]); ewa = cut(res[(pk, "EWall")])
            sp = signal_spread(*panels[pk], n).loc[start:end]
            t, ann = paired_t(r, ewa)
            rows.append(dict(panel=pk, sd=disp[pk]["sd"].mean(), sd_norm=disp[pk]["sd_n"].mean(),
                             n_elig=disp[pk]["n_elig"].mean(),
                             netSharpe=metrics(r)["Sharpe"], dSharpe=metrics(r)["Sharpe"] - metrics(ewa)["Sharpe"],
                             dCAGR=ann, t_net=t,
                             gross_spread_ann=sp.mean() * 52, t_gross=one_t(sp)))
        t3 = pd.DataFrame(rows).set_index("panel").sort_values("sd", ascending=False)
        print(f"\n  --- CAND{n} vs EWall ---")
        print(fmt(t3))
        print(f"  Spearman(sd, dSharpe) = {spearman(t3['sd'], t3['dSharpe']):+.3f}   "
              f"Spearman(sd, gross_spread) = {spearman(t3['sd'], t3['gross_spread_ann']):+.3f}   "
              f"Spearman(sd_norm, gross_spread) = {spearman(t3['sd_norm'], t3['gross_spread_ann']):+.3f}   "
              f"Spearman(sd, netSharpe) = {spearman(t3['sd'], t3['netSharpe']):+.3f}   "
              f"Spearman(n_elig, gross_spread) = {spearman(t3['n_elig'], t3['gross_spread_ann']):+.3f}")

    # ---------------- 4. within a panel, over time
    print("\n" + "=" * 200)
    print("4. TEST (b): WITHIN EACH PANEL, OVER TIME - gross selection spread by dispersion tercile")
    print("=" * 200)
    print("Terciles are cut on an EXPANDING quantile of that panel's own dispersion history "
          "(>= 104 weeks required), so no future information enters the classification.")
    for n in NS:
        rows = []
        for pk in panels:
            d = disp[pk]["sd"]
            sp = signal_spread(*panels[pk], n).loc[start:end].reindex(d.index)
            # expanding percentile rank of dispersion, using history up to and including t
            pr = d.expanding().rank(pct=True)
            valid = d.notna() & sp.notna() & (np.arange(len(d)) >= 104)
            lo = valid & (pr <= 1 / 3); hi = valid & (pr > 2 / 3); mid = valid & ~lo & ~hi
            rows.append(dict(panel=pk, weeks=int(valid.sum()),
                             lo=sp[lo].mean() * 52, mid=sp[mid].mean() * 52, hi=sp[hi].mean() * 52,
                             hi_minus_lo=(sp[hi].mean() - sp[lo].mean()) * 52,
                             t_hi_lo=(sp[hi].mean() - sp[lo].mean()) /
                                     np.sqrt(sp[hi].var() / max(sp[hi].count(), 1) + sp[lo].var() / max(sp[lo].count(), 1)),
                             t_hi=one_t(sp[hi]), t_lo=one_t(sp[lo]),
                             corr_rank=spearman(d[valid], sp[valid])))
        t4 = pd.DataFrame(rows).set_index("panel")
        print(f"\n  --- CAND{n} minus EW-eligible, annualised, by dispersion tercile ---")
        print(fmt(t4))
        pos = int((t4["hi_minus_lo"] > 0).sum())
        print(f"  hi > lo in {pos} of {len(t4)} panels;  mean within-panel Spearman(dispersion, spread) = "
              f"{t4['corr_rank'].mean():+.3f}")

    # pooled, panel-demeaned
    print("\n  --- pooled across panels, each panel's spread and dispersion-rank demeaned (panel fixed effects) ---")
    for n in NS:
        A, B = [], []
        for pk in panels:
            d = disp[pk]["sd"]
            sp = signal_spread(*panels[pk], n).loc[start:end].reindex(d.index)
            pr = d.expanding().rank(pct=True)
            v = d.notna() & sp.notna() & (np.arange(len(d)) >= 104)
            if v.sum() < 30:
                continue
            A.append(pr[v] - pr[v].mean()); B.append(sp[v] - sp[v].mean())
        a = pd.concat(A); b = pd.concat(B)
        beta = np.polyfit(a, b, 1)[0]
        r_ = np.corrcoef(a, b)[0, 1]
        tt = r_ * np.sqrt(len(a) - 2) / np.sqrt(max(1 - r_ ** 2, 1e-12))
        print(f"   CAND{n}: obs {len(a)}  corr(demeaned dispersion pctile, demeaned weekly spread) = {r_:+.4f} "
              f"(t {tt:+.2f})  slope = {beta * 52:+.3%}/yr per unit of percentile")

    # ---------------- 5. rule 8 walk-forward
    print("\n" + "=" * 200)
    print("5. RULE 8 WALK-FORWARD - parameters chosen on 2009-2016 (in the common window), 2017-2026 read once")
    print("=" * 200)
    isr = {}
    for pk in panels:
        for n in NS:
            r = cut(res[(pk, f"CAND{n}")])
            isr[(pk, n)] = r.loc[:IS_END]
    cand = pd.DataFrame([dict(panel=pk, n=n, IS_Sharpe=metrics(isr[(pk, n)])["Sharpe"],
                              IS_MaxDD=metrics(isr[(pk, n)])["MaxDD"],
                              IS_disp=disp[pk].loc[:IS_END]["sd"].mean())
                         for pk in panels for n in NS])
    print("\nIn-sample (2009-2016 portion of the common window) CAND points:")
    print(fmt(cand.set_index(["panel", "n"])))
    print(f"IS SPY: Sharpe {ms_is['Sharpe']:.3f}  MaxDD {ms_is['MaxDD']:.1%}  (4b IS DD cap {0.60 * abs(ms_is['MaxDD']):.1%})")

    s1 = cand.sort_values(["IS_Sharpe", "n"], ascending=[False, True]).iloc[0]
    ok = cand[cand["IS_MaxDD"].abs() <= 0.60 * abs(ms_is["MaxDD"])]
    s2 = ok.sort_values(["IS_Sharpe", "n"], ascending=[False, True]).iloc[0] if len(ok) else None
    d20 = cand[cand["n"] == 20].sort_values("IS_disp", ascending=False).iloc[0]

    print("\nSelections (rules fixed before any OOS number was read):")
    print(f"  S1 highest IS Sharpe          -> {s1['panel']} n={int(s1['n'])}  (IS {s1['IS_Sharpe']:.3f})")
    print(f"  S2 4b-aware (IS DD under cap) -> " +
          (f"{s2['panel']} n={int(s2['n'])}  (IS {s2['IS_Sharpe']:.3f}, DD {s2['IS_MaxDD']:.1%})" if s2 is not None else "none qualifies"))
    print(f"  S3 highest IS dispersion, n=20-> {d20['panel']} n=20  (IS mean sd {d20['IS_disp']:.3f})")

    oos_rows = []
    for tag, sel in [("S1", s1), ("S2", s2), ("S3", d20)]:
        if sel is None:
            continue
        pk, n = sel["panel"], int(sel["n"])
        r = cut(res[(pk, f"CAND{n}")]).loc[OOS_START:]
        m = metrics(r)
        oos_rows.append(dict(rule=tag, pick=f"{pk}/CAND{n}", CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                             vs_SPY_Sharpe=m["Sharpe"] - ms_oos["Sharpe"],
                             DD_ok="Y" if abs(m["MaxDD"]) <= 0.60 * abs(ms_oos["MaxDD"]) else "n",
                             CAGR_ok="Y" if m["CAGR"] >= 0.70 * ms_oos["CAGR"] else "n",
                             OOS_4b="PASS" if (m["Sharpe"] > ms_oos["Sharpe"] and
                                               abs(m["MaxDD"]) <= 0.60 * abs(ms_oos["MaxDD"]) and
                                               m["CAGR"] >= 0.70 * ms_oos["CAGR"]) else "FAIL"))
    print("\nOut of sample (2017-2026), read once:")
    print(fmt(pd.DataFrame(oos_rows).set_index("rule")))
    print(f"  SPY OOS: CAGR {ms_oos['CAGR']:.1%}  Sharpe {ms_oos['Sharpe']:.3f}  MaxDD {ms_oos['MaxDD']:.1%}  "
          f"(4b OOS bars: DD <= {0.60 * abs(ms_oos['MaxDD']):.1%}, CAGR >= {0.70 * ms_oos['CAGR']:.2%})")

    # full OOS table, so S3's pick can be judged against what was actually available
    oos_all = pd.DataFrame([dict(panel=pk, n=n,
                                 IS_disp=disp[pk].loc[:IS_END]["sd"].mean(),
                                 IS_Sharpe=metrics(isr[(pk, n)])["Sharpe"],
                                 OOS_Sharpe=metrics(cut(res[(pk, f"CAND{n}")]).loc[OOS_START:])["Sharpe"],
                                 OOS_CAGR=metrics(cut(res[(pk, f"CAND{n}")]).loc[OOS_START:])["CAGR"],
                                 OOS_MaxDD=metrics(cut(res[(pk, f"CAND{n}")]).loc[OOS_START:])["MaxDD"])
                            for pk in panels for n in NS])
    print("\nEvery CAND point IS vs OOS (so the selections above can be audited):")
    print(fmt(oos_all.set_index(["panel", "n"])))
    print(f"  Spearman(IS Sharpe, OOS Sharpe) over the 21 points = {spearman(oos_all['IS_Sharpe'], oos_all['OOS_Sharpe']):+.3f}")
    print(f"  Spearman(IS dispersion, OOS Sharpe) over the 21 points = {spearman(oos_all['IS_disp'], oos_all['OOS_Sharpe']):+.3f}")
    n20 = oos_all[oos_all["n"] == 20]
    print(f"  Spearman(IS dispersion, OOS Sharpe) over the 7 panels at n=20 = {spearman(n20['IS_disp'], n20['OOS_Sharpe']):+.3f}")

    # ---------------- 6. leaderboard rows
    print("\n" + "=" * 200)
    print("6. LEADERBOARD ROWS (common window; baseline = that panel's own RULES v1 book)")
    print("=" * 200)
    today = pd.Timestamp.today().date()
    for pk in panels:
        base = cut(res[(pk, "v1")])
        bm = metrics(base); b1, b2 = half_sharpes(base)
        for bk in ["EWall"] + [f"CAND{n}" for n in NS]:
            r = cut(res[(pk, bk)])
            m = metrics(r); h1, h2 = half_sharpes(r)
            f = fail_4b(r, spy, r.loc[OOS_START:], spy_oos)
            v = ("KEEP 4b" if f == "-" else f"KILL 4b ({f})")
            if verdict_4a(r, base):
                v = "4a-pass, " + v
            sd = disp[pk]["sd"].mean()
            print(f"| {today} | 73 {pk}/{bk} (sd {sd:.3f}, dS_EW {m['Sharpe'] - metrics(cut(res[(pk, 'EWall')]))['Sharpe']:+.3f}) | "
                  f"{m['CAGR']:.1%} | {m['Sharpe']:.2f} | {m['MaxDD']:.1%} | {h1:.2f} / {h2:.2f} | "
                  f"{bm['Sharpe']:.2f} ({b1:.2f}/{b2:.2f}) | {v} | research/backtests/{SCRIPT} |")


if __name__ == "__main__":
    main()
