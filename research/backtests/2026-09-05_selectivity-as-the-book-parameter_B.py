#!/usr/bin/env python3
"""Idea 160 - "selectivity-as-the-book-parameter": should a book fix the SHARE q of the
eligible set it holds, instead of fixing the NAME COUNT n and letting q float?

The question
------------
Idea 78 found that the gross ranking payoff inside a panel is governed by selectivity
q = n / n_elig (Spearman(q, spread) = -0.975) and that the raw candidate count is inert
once q is matched.  Idea 153 then found that the standing 4b KEEP transfers from u56 to
broad by its SHARE (n = 47..49, q ~= 0.51-0.54) and NOT by its name count (n = 20 fails
broad's H2 at 0.811).  Both results are about a share held FIXED AT ITS MEAN.

Every book this project runs still fixes n, so the realised q floats with the eligible
count.  On B136 the eligible count runs from single digits to >120 across weeks, so the
book's realised selectivity swings by an order of magnitude week to week with nobody
choosing it.  This run tests the obvious alternative directly:

    FIXQ   n_t = max(1, round(q * E_t))     the top q SHARE of that week's eligible set
    FIXN   n_t = n                          the incumbent construction, n pinned so that
                                            the two arms have the SAME MEAN BOOK SIZE

If idea 78's mechanism is the operative one, holding q fixed should be better than
letting it float at matched mean size.  If it is not, the count-vs-share distinction is
a description of the cross-section and not a book parameter, and RULES keeps its n.

Design
------
Both arms use the SAME composite key, the SAME 200d / vol20 < 0.60 gate, the SAME 75%
gross and the SAME weekly / t+1 / cost convention.  The ONLY difference is how n_t is
set each week.

    Matching.  For each (panel, q) the FIXN arm uses n = round(q * mean E_t) where the
    mean is taken over the IN-SAMPLE window 2009-2016 ONLY, so the control's parameter
    never reads the evaluation period.  The two arms therefore hold the same number of
    names ON AVERAGE and differ only in whether that number tracks E_t.

    Gross convention.  BOTH arms rebuild full gross over their actual holdings
    (w = gross / count_held, "rw").  This is pre-registered, not chosen: the incumbent
    `gross/n` convention (idea 81's "dg") silently de-grosses whenever E_t < n, which
    happens on broad, and would confound count-tracking with exposure-tracking.  The dg
    reading of the incumbent book is reported in pre-check [a] and nowhere else.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. q in {0.10, 0.20, 0.30, 0.40, 0.53, 0.65, 0.80, 1.00}   (8 values; 0.53 is idea
       153's published share, carried in rather than fitted; 1.00 is the EWall control)
    2. the count rule in {FIXQ, FIXN}                          (the instrument itself)
    => 16 grid points per cell, EVERY ONE reported.
Panels and cost rungs are pre-registered axes, not tuned: u56 x broad x {10, 25} bps is
the queue's own specification (4 primary cells).  The 484-name sub-$2B panel is run at
the same 16 points and reported SEPARATELY as secondary, because ideas 39/49/136 show
the 200d gate is inverted there and the panel has produced no defensive book at all.

Pre-checks run BEFORE any new number is read
    [a] harness: idea 2's published U56/CAND20 row (12.7% / 1.093 / -18.3%, halves
        1.088 / 1.103; the CHANGELOG records the re-derivable value as 1.09214 /
        1.08828 / 1.10155) and the live RULES v1 row, both under the incumbent dg
        convention, plus the rw reading of the same book.
    [b] premise 1: the queue's claim that q swings by ~16x on B136 - report the eligible
        count's range and the realised q range of the n=20 book.
    [c] premise 2: idea 78's mechanism where FIXQ would act - bin every rebalance week
        by the realised q of a top-20 book and report the gross (cost-free) selection
        spread per bin.  If the spread does not fall in q, idea 160 has no premise.
    [d] index sanity: the panels must be on a trading-day index (idea 38).

Walk-forward (PROTOCOL rule 8) - selectors fixed before any OOS number was read
    Parameters chosen on 2009-2016 only; 2017-2026 read once, untouched.
    S0  do-nothing control: FIXN at the project's published n = 20, no selection.
    S1  IS-Sharpe argmax over all 16 arms in the cell (the incumbent selector).
    S2  IS-Sharpe argmax over the 8 FIXQ arms only  (this idea's hypothesis).
    S3  IS-Sharpe argmax over the 8 FIXN arms only  (the rival).
    S4  random arm, seed fixed in advance (the size-matched null).
    Reported paired across the 4 primary cells and across all 6 cells.

Verdicts (both KEEP paths, every point)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.
    Also reported: 4b evaluated on the OOS window alone.

Caveats carried
    Survivorship: universe.json, universe_broad.json and the small panel are all current
    constituents (idea 54), one-directional.  It flatters every arm here equally in
    direction but not necessarily in size: a share-tracking book holds MORE names in bad
    weeks, which is exactly the cohort delisted names would sit in, so FIXQ is the arm
    survivorship flatters more.  Stated, not corrected.
    Idea 128: the IS window's SPY drawdown is shallow, which biases every selector here
    identically.
    Idea 126: t+1 execution only, no spread or impact model.
    No IWM in the cache, so the small panel is judged against SPY (stated, not adjusted).

Deterministic, standalone.  Reads baseline.py and engine.py; modifies nothing.
"""
import sys, time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore", category=RuntimeWarning)
from baseline import load_universe, rules_v1_weights, score
from engine import backtest, metrics, rebalance_mask

FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
COSTS = [10, 25]
QS = [0.10, 0.20, 0.30, 0.40, 0.53, 0.65, 0.80, 1.00]
ARMS = ["FIXQ", "FIXN"]
N_PUB = 20                      # the project's published book size (S0 control)
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SEED_S4 = 160_777
SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 600)

_lines = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ------------------------------------------------------------------ book construction
def eligible_mask(px, tradable):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def rank_key(px, elig):
    """Composite WITHOUT /sqrt(vol20) (ideas 1/2/80/81: the divisor is signed against the
    panel), ranked among eligible names only."""
    s = score(px, vol_scale=False)[0]
    return s.where(elig).rank(axis=1, ascending=False)


def book_weights(rank, count_series, gross=GROSS):
    """Top count_series[t] names by rank, full gross rebuilt over the names actually
    held (rw convention).  count_series is per-date."""
    c = count_series.reindex(rank.index).fillna(0)
    sel = rank.le(c, axis=0) & rank.notna()
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.astype(float).div(held, axis=0).mul(gross).fillna(0.0)


def arm_counts(arm, q, elig, n_fix):
    """Per-date target count for each arm."""
    E = elig.sum(axis=1)
    if arm == "FIXQ":
        c = np.maximum(1, np.round(q * E)).astype(int)
        return pd.Series(np.minimum(c.values, E.values), index=E.index).where(E > 0, 0)
    return pd.Series(np.minimum(n_fix, E.values), index=E.index)


# ------------------------------------------------------------------ metric helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail_4a(r, base):
    h1, h2 = half_sharpes(r); b1, b2 = half_sharpes(base)
    f = []
    if not h1 > b1: f.append("H1")
    if not h2 > b2: f.append("H2")
    if not metrics(r)["MaxDD"] >= metrics(base)["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"


def fail_4b(r, spy):
    """Full-sample 4b: halves vs SPY halves, OOS Sharpe vs SPY OOS, DD cap, CAGR floor."""
    h1, h2 = half_sharpes(r); s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    ro, so = r.loc[OOS_START:], spy.loc[OOS_START:]
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(ro)["Sharpe"] > metrics(so)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def fail_4b_window(r, spy):
    """4b evaluated on the OOS window alone (halves of the OOS window)."""
    r, spy = r.loc[OOS_START:], spy.loc[OOS_START:]
    h1, h2 = half_sharpes(r); s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not m["Sharpe"] > ms["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def tstat(x):
    x = pd.Series(x).dropna()
    if len(x) < 3 or x.std() == 0:
        return 0.0
    return float(x.mean() / (x.std() / np.sqrt(len(x))))


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    if ok.sum() < 3:
        return np.nan
    return float(np.corrcoef(a[ok].rank(), b[ok].rank())[0, 1])


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    P("=" * 190)
    P(f"Idea 160 selectivity-as-the-book-parameter (lane B) | {SCRIPT}")
    P("weekly rebalance, next-day execution, 75% gross, full-gross rebuild (rw) on BOTH arms, 10 and 25 bps")
    P("=" * 190)

    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    panels = {
        "u56":   (px56,  set(px56.columns)),
        "broad": (px136, set(px136.columns)),
        "small": (pxs,   set(c for c in pxs.columns if c != "SPY")),
    }
    PRIMARY = ["u56", "broad"]

    # ---------------------------------------------------- [d] index sanity
    P("\n--- pre-check [d] trading-day index (idea 38) ---")
    bad = False
    for k, (p, _) in panels.items():
        yrs = p.index.to_series().groupby(p.index.year).count()
        mx = yrs.loc[2015:2024].max()
        P(f"  {k:<6} rows {p.shape[0]:>5} cols {p.shape[1]:>4}  {p.index[0].date()} -> {p.index[-1].date()}  max rows/yr 2015-24 = {mx}")
        bad |= mx > 300
    if bad:
        P("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)

    # ---------------------------------------------------- [a] harness
    P("\n--- pre-check [a] harness: the published incumbent rows must come back ---")
    e56 = eligible_mask(px56, panels["u56"][1])
    rk56 = rank_key(px56, e56)
    start56 = px56.index[260]
    w_dg = (rk56 <= N_PUB).astype(float) * (GROSS / N_PUB)                 # idea 2's own dg form
    r_dg = backtest(px56, w_dg, cost_bps=10, freq=FREQ)["returns"].loc[start56:]
    m = metrics(r_dg); h1, h2 = half_sharpes(r_dg)
    P(f"  U56/CAND20 dg  {m['CAGR']:.5%} / {m['Sharpe']:.5f} / {m['MaxDD']:.5%}  halves {h1:.5f}/{h2:.5f}")
    P("    [published idea 2 row 12.7% / 1.093 / -18.3% halves 1.088/1.103; CHANGELOG re-derivable 12.65974% / 1.09214 / -18.30835%, 1.08828/1.10155]")
    cnt20 = arm_counts("FIXN", None, e56, N_PUB)
    r_rw = backtest(px56, book_weights(rk56, cnt20), cost_bps=10, freq=FREQ)["returns"].loc[start56:]
    m2 = metrics(r_rw); g1, g2 = half_sharpes(r_rw)
    P(f"  U56/CAND20 rw  {m2['CAGR']:.5%} / {m2['Sharpe']:.5f} / {m2['MaxDD']:.5%}  halves {g1:.5f}/{g2:.5f}   (this run's convention)")
    r_v1 = backtest(px56, rules_v1_weights(px56), cost_bps=10, freq=FREQ)["returns"].loc[start56:]
    mv = metrics(r_v1); v1, v2 = half_sharpes(r_v1)
    P(f"  U56/RULES v1   {mv['CAGR']:.5%} / {mv['Sharpe']:.5f} / {mv['MaxDD']:.5%}  halves {v1:.5f}/{v2:.5f}   [live book: 6.5% / 0.666 / -13.8%]")

    # ---------------------------------------------------- [b] premise 1: does q float?
    P("\n--- pre-check [b] premise 1: how far does realised q float when n is fixed? ---")
    prem_b = []
    for k in ["u56", "broad", "small"]:
        p, tr = panels[k]
        el = eligible_mask(p, tr)
        st = p.index[260]
        mask = rebalance_mask(p.index, FREQ)
        E = el.sum(axis=1).loc[st:][mask.loc[st:].values]
        q20 = (np.minimum(N_PUB, E) / E.replace(0, np.nan))
        prem_b.append(dict(panel=k, n_weeks=len(E), E_min=E.min(), E_p05=E.quantile(.05),
                           E_mean=E.mean(), E_p95=E.quantile(.95), E_max=E.max(),
                           q20_min=q20.min(), q20_mean=q20.mean(), q20_max=q20.max(),
                           q20_swing=q20.max() / max(q20.min(), 1e-9)))
    prem_b = pd.DataFrame(prem_b).set_index("panel")
    P(fmt(prem_b, 3))
    P("  (the queue's claim is B136 n_elig 3..127 -> ~16x swing in q; 'broad' here is B136)")

    # ---------------------------------------------------- [c] premise 2: q vs gross spread
    P("\n--- pre-check [c] premise 2: gross (cost-free) top-20 selection spread by realised-q bin ---")
    prem_c_rows = []
    for k in PRIMARY:
        p, tr = panels[k]
        el = eligible_mask(p, tr)
        rk = rank_key(p, el)
        mask = rebalance_mask(p.index, FREQ)
        dates = p.index[mask.values]
        dates = dates[dates >= p.index[260]]
        fwd = p.loc[dates].pct_change().shift(-1)
        eld, rkd = el.loc[dates], rk.loc[dates]
        E = eld.sum(axis=1)
        ok = E >= 5
        q = (np.minimum(N_PUB, E) / E.replace(0, np.nan))
        top = rkd.le(np.minimum(N_PUB, E), axis=0) & rkd.notna()
        spread = (fwd.where(top).mean(axis=1) - fwd.where(eld).mean(axis=1)).where(ok)
        qq, ss = q[ok], spread[ok]
        bins = pd.qcut(qq, 5, labels=False, duplicates="drop")
        for b in sorted(pd.Series(bins).dropna().unique()):
            sel = bins == b
            prem_c_rows.append(dict(panel=k, qbin=int(b), n=int(sel.sum()),
                                    q_mean=qq[sel].mean(),
                                    spread_ann=ss[sel].mean() * 52, t=tstat(ss[sel])))
        P(f"  {k}: Spearman(realised q, weekly gross spread) over {int(ok.sum())} weeks = {spearman(qq, ss):+.4f}")
    prem_c = pd.DataFrame(prem_c_rows)
    P(fmt(prem_c.set_index(["panel", "qbin"]), 4))

    # ---------------------------------------------------- the grid
    P("\n" + "=" * 190)
    P("GRID: 3 panels x 2 cost rungs x 8 q x 2 count rules = 96 books.  Every point printed.")
    P("=" * 190)

    rows = []
    ret_store = {}
    for k, (p, tr) in panels.items():
        el = eligible_mask(p, tr)
        rk = rank_key(p, el)
        st = p.index[260]
        E = el.sum(axis=1).loc[st:]
        E_is = E.loc[:IS_END]
        spy = p["SPY"].pct_change().fillna(0).loc[st:]
        base = backtest(p, rules_v1_weights(p), cost_bps=10, freq=FREQ)["returns"].loc[st:]
        base25 = backtest(p, rules_v1_weights(p), cost_bps=25, freq=FREQ)["returns"].loc[st:]
        bases = {10: base, 25: base25}
        for q in QS:
            n_fix = int(max(1, round(q * E_is.mean())))
            for arm in ARMS:
                cnt = arm_counts(arm, q, el, n_fix)
                w = book_weights(rk, cnt)
                held = (w > 0).sum(axis=1).loc[st:]
                gross_real = w.sum(axis=1).loc[st:]
                q_real = (held / E.replace(0, np.nan))
                for c in COSTS:
                    res = backtest(p, w, cost_bps=c, freq=FREQ)
                    r = res["returns"].loc[st:]
                    to = res["turnover"].loc[st:].sum() / (len(r) / 252)
                    m = metrics(r); h1, h2 = half_sharpes(r)
                    ro = r.loc[OOS_START:]
                    mo = metrics(ro)
                    yr = (1 + r).groupby(r.index.year).prod() - 1
                    rows.append(dict(
                        panel=k, cost=c, q=q, arm=arm, n_fix=n_fix,
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                        held_mean=held.mean(), q_real_mean=q_real.mean(),
                        q_real_sd=q_real.std(), gross_mean=gross_real.mean(),
                        turnover=to, y2020=yr.get(2020, np.nan), y2022=yr.get(2022, np.nan),
                        fail4a=fail_4a(r, bases[c]), fail4b=fail_4b(r, spy),
                        fail4b_oos=fail_4b_window(r, spy)))
                    ret_store[(k, c, q, arm)] = r
        # references
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        s1, s2 = half_sharpes(spy)
        P(f"\n[{k}] SPY {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%} halves {s1:.3f}/{s2:.3f} | "
          f"SPY OOS {mso['CAGR']:.2%} / {mso['Sharpe']:.3f} / {mso['MaxDD']:.2%} | "
          f"4b bars: CAGR>= {0.70*ms['CAGR']:.2%}, |DD|<= {0.60*abs(ms['MaxDD']):.2%}")
        for c in COSTS:
            mb = metrics(bases[c]); b1, b2 = half_sharpes(bases[c])
            P(f"     RULES v1 @{c}bps {mb['CAGR']:.2%} / {mb['Sharpe']:.3f} / {mb['MaxDD']:.2%} halves {b1:.3f}/{b2:.3f}")
        P(f"     mean eligible count: IS(2009-2016) {E_is.mean():.1f}, full {E.mean():.1f}")

    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    P("\n--- FULL GRID (all 96 points) ---")
    show = ["panel", "cost", "q", "arm", "n_fix", "held_mean", "q_real_mean", "q_real_sd",
            "gross_mean", "turnover", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "y2020", "y2022", "fail4a", "fail4b", "fail4b_oos"]
    for k in ["u56", "broad", "small"]:
        P(f"\n[{k}]")
        P(G[G.panel == k][show].drop(columns=["panel"]).to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------- Q1: paired FIXQ - FIXN
    P("\n" + "=" * 190)
    P("Q1  THE ANSWER: FIXQ minus FIXN at matched mean book size, paired on daily returns")
    P("=" * 190)
    comp = []
    for k in panels:
        for c in COSTS:
            for q in QS:
                a = ret_store[(k, c, q, "FIXQ")]
                b = ret_store[(k, c, q, "FIXN")]
                ga = G[(G.panel == k) & (G.cost == c) & (G.q == q) & (G.arm == "FIXQ")].iloc[0]
                gb = G[(G.panel == k) & (G.cost == c) & (G.q == q) & (G.arm == "FIXN")].iloc[0]
                d = a - b
                comp.append(dict(panel=k, cost=c, q=q, n_fix=int(gb.n_fix),
                                 held_Q=ga.held_mean, held_N=gb.held_mean,
                                 dCAGR=ga.CAGR - gb.CAGR, dSharpe=ga.Sharpe - gb.Sharpe,
                                 dMaxDD=abs(gb.MaxDD) - abs(ga.MaxDD),
                                 dOOS_Sharpe=ga.OOS_Sharpe - gb.OOS_Sharpe,
                                 dTurnover=ga.turnover - gb.turnover,
                                 t_daily=tstat(d), ann_diff=d.mean() * 252,
                                 d2020=ga.y2020 - gb.y2020, d2022=ga.y2022 - gb.y2022))
    C = pd.DataFrame(comp)
    C.to_csv(OUT / f"{STEM}.paired.csv", index=False)
    for k in ["u56", "broad", "small"]:
        P(f"\n[{k}]  (dMaxDD > 0 means FIXQ is SHALLOWER)")
        P(C[C.panel == k].drop(columns=["panel"]).to_string(
            index=False, float_format=lambda x: f"{x:+.4f}"))

    prim = C[C.panel.isin(PRIMARY)]
    P("\n--- summary over the 4 PRIMARY (large-cap) cells x 8 q = 32 comparisons ---")
    P(f"  mean dSharpe {prim.dSharpe.mean():+.4f}   median {prim.dSharpe.median():+.4f}   "
      f"FIXQ wins Sharpe {int((prim.dSharpe > 0).sum())}/{len(prim)}")
    P(f"  mean dCAGR   {prim.dCAGR.mean():+.4%}   FIXQ wins CAGR {int((prim.dCAGR > 0).sum())}/{len(prim)}")
    P(f"  mean dMaxDD  {prim.dMaxDD.mean():+.4%} (positive = FIXQ shallower)  FIXQ shallower {int((prim.dMaxDD > 0).sum())}/{len(prim)}")
    P(f"  mean dOOS_Sharpe {prim.dOOS_Sharpe.mean():+.4f}   FIXQ wins {int((prim.dOOS_Sharpe > 0).sum())}/{len(prim)}")
    P(f"  daily paired t: mean {prim.t_daily.mean():+.3f}, |t|>=2 in {int((prim.t_daily.abs() >= 2).sum())}/{len(prim)}, "
      f"t>=+2 in {int((prim.t_daily >= 2).sum())}, t<=-2 in {int((prim.t_daily <= -2).sum())}")
    P(f"  mean turnover difference {prim.dTurnover.mean():+.2f} x/yr")
    P(f"  2020: mean dReturn {prim.d2020.mean():+.2%}, FIXQ better {int((prim.d2020 > 0).sum())}/{len(prim)}")
    P(f"  2022: mean dReturn {prim.d2022.mean():+.2%}, FIXQ better {int((prim.d2022 > 0).sum())}/{len(prim)}")
    sec = C[C.panel == "small"]
    P(f"\n  [secondary, small panel] mean dSharpe {sec.dSharpe.mean():+.4f}, FIXQ wins {int((sec.dSharpe > 0).sum())}/{len(sec)}; "
      f"mean dCAGR {sec.dCAGR.mean():+.4%}")

    # ---------------------------------------------------- Q2: does q float less? (mechanism)
    P("\n" + "=" * 190)
    P("Q2  MECHANISM: the instrument does what it claims - realised selectivity sd by arm")
    P("=" * 190)
    mech = G[G.cost == 10].pivot_table(index=["panel", "q"], columns="arm",
                                       values=["q_real_mean", "q_real_sd", "held_mean", "turnover"])
    P(fmt(mech, 4))

    # ---------------------------------------------------- Q3: KEEP paths
    P("\n" + "=" * 190)
    P("Q3  BOTH KEEP PATHS, every one of the 96 books")
    P("=" * 190)
    for lbl, col in [("4a (beat the live rules)", "fail4a"),
                     ("4b (capital-worthy, full sample)", "fail4b"),
                     ("4b on the OOS window alone", "fail4b_oos")]:
        n_pass = int((G[col] == "-").sum())
        P(f"\n{lbl}: {n_pass} of {len(G)} pass")
        if n_pass:
            P(G[G[col] == "-"][["panel", "cost", "q", "arm", "n_fix", "CAGR", "Sharpe",
                                "MaxDD", "H1", "H2", "OOS_Sharpe", "turnover"]].to_string(
                index=False, float_format=lambda x: f"{x:.4f}"))
        fc = G[G[col] != "-"][col].str.split(",").explode().value_counts()
        P("  first-failing-bar census (a book can fail several): " +
          ", ".join(f"{i} {v}" for i, v in fc.items()))
    P("\n  4a/4b pass counts by arm (primary large-cap cells only):")
    pg = G[G.panel.isin(PRIMARY)]
    P(fmt(pd.DataFrame({
        "4a": pg.groupby("arm").apply(lambda d: (d.fail4a == "-").sum()),
        "4b": pg.groupby("arm").apply(lambda d: (d.fail4b == "-").sum()),
        "4b_oos": pg.groupby("arm").apply(lambda d: (d.fail4b_oos == "-").sum()),
        "n_books": pg.groupby("arm").size()}), 0))

    # ---------------------------------------------------- Q4: rule 8 walk-forward
    P("\n" + "=" * 190)
    P("Q4  RULE 8 WALK-FORWARD: parameters chosen on 2009-2016 only, 2017-2026 read once")
    P("=" * 190)
    rng = np.random.default_rng(SEED_S4)
    wf = []
    for k in panels:
        p, tr = panels[k]
        st = p.index[260]
        spy = p["SPY"].pct_change().fillna(0).loc[st:]
        spy_o = spy.loc[OOS_START:]
        v1 = backtest(p, rules_v1_weights(p), cost_bps=10, freq=FREQ)["returns"].loc[OOS_START:]
        for c in COSTS:
            cell = G[(G.panel == k) & (G.cost == c)].reset_index(drop=True)
            def pick(sub):
                return sub.loc[sub.IS_Sharpe.idxmax()]
            sels = {
                "S0_donothing_n20": None,
                "S1_IS_all": pick(cell),
                "S2_IS_FIXQ": pick(cell[cell.arm == "FIXQ"]),
                "S3_IS_FIXN": pick(cell[cell.arm == "FIXN"]),
                "S4_random": cell.iloc[int(rng.integers(len(cell)))],
            }
            # S0: the published n=20 book, same convention, no selection
            el = eligible_mask(p, tr); rk = rank_key(p, el)
            r0 = backtest(p, book_weights(rk, arm_counts("FIXN", None, el, N_PUB)),
                          cost_bps=c, freq=FREQ)["returns"].loc[st:]
            for name, row in sels.items():
                if row is None:
                    r, arm, q = r0, "FIXN", np.nan
                else:
                    r = ret_store[(k, c, row.q, row.arm)]; arm, q = row.arm, row.q
                ro = r.loc[OOS_START:]
                m = metrics(ro)
                wf.append(dict(panel=k, cost=c, selector=name, arm=arm, q=q,
                               OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                               SPY_OOS_Sharpe=metrics(spy_o)["Sharpe"],
                               V1_OOS_Sharpe=metrics(v1)["Sharpe"]))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n--- paired means (equal-weighted across cells) ---")
    for lbl, sub in [("4 PRIMARY large-cap cells", W[W.panel.isin(PRIMARY)]),
                     ("all 6 cells", W)]:
        agg = sub.groupby("selector")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].mean()
        base = agg.loc["S0_donothing_n20", "OOS_Sharpe"]
        agg["vs_S0_Sharpe"] = agg["OOS_Sharpe"] - base
        P(f"\n[{lbl}]")
        P(fmt(agg, 4))
        P(f"  SPY OOS Sharpe {sub.SPY_OOS_Sharpe.mean():.4f} | RULES v1 OOS Sharpe {sub.V1_OOS_Sharpe.mean():.4f}")
    P("\n  selector picks (arm, q) per cell:")
    P(W.pivot_table(index=["panel", "cost"], columns="selector",
                    values="q", aggfunc="first").to_string(float_format=lambda x: f"{x:.2f}"))
    P("  arm picked: " + "; ".join(
        f"{s}: " + "/".join(W[W.selector == s].arm.tolist()) for s in sorted(W.selector.unique())))

    # ---------------------------------------------------- Q5: is q the right dial at all?
    P("\n" + "=" * 190)
    P("Q5  Sharpe as a function of q, per arm (is there an interior optimum, or is q inert?)")
    P("=" * 190)
    for k in ["u56", "broad", "small"]:
        for c in COSTS:
            sub = G[(G.panel == k) & (G.cost == c)]
            pv = sub.pivot_table(index="q", columns="arm", values="Sharpe")
            pv["range_over_q"] = np.nan
            P(f"\n[{k} @{c}bps] Sharpe by q")
            P(fmt(pv[ARMS], 4))
            for a in ARMS:
                v = sub[sub.arm == a].sort_values("q")
                P(f"   {a}: argmax q={v.loc[v.Sharpe.idxmax(),'q']:.2f} Sharpe {v.Sharpe.max():.4f}, "
                  f"min {v.Sharpe.min():.4f}, range {v.Sharpe.max()-v.Sharpe.min():.4f}, "
                  f"Spearman(q, Sharpe) {spearman(v.q, v.Sharpe):+.3f}")

    P(f"\nElapsed {time.time()-t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
