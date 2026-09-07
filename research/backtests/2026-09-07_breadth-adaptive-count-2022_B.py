#!/usr/bin/env python3
"""Idea 48 - "breadth-adaptive-count-2022": is the fraction rule's 2022 defence worth a
CONDITIONAL clause, i.e. fixed-n in broad markets and fraction-based only when breadth is
in its own bottom quintile?

The question
------------
Idea 46 (lane B, 2026-09-04) KILLED the fixed-FRACTION rule as a general improvement over a
fixed COUNT (at matched book size it beat the count arm on Sharpe at 3/8 pairs, mean dSharpe
-0.002), but noticed one place where it clearly won: 2022, where f=0.35 returned -0.8% and
f=0.45 -1.5% against fixed n=20's -9.0% and SPY's -18.2%.  Full-sample Sharpe hides this
because the fraction rule pays for it in every other year.  The queue's question is whether
the win can be bought WITHOUT the bill: switch to the fraction rule only when the market is
narrow, and run the fixed count the rest of the time.

Honesty note that governs the whole script
------------------------------------------
2022 is inside the OOS window of PROTOCOL rule 8 (2017-2026).  The hypothesis was GENERATED
by looking at 2022, so every full-sample and stress-year number below is contaminated by
that: it is description, not evidence.  The one number that is evidence is the rule-8
walk-forward, where (q, f) are chosen on 2009-2016 alone - a window containing no 2022 - and
2017-2026 is read once.  This script therefore reports the whole grid, but the verdict is
taken from the walk-forward and from whether the conditional clause beats its own
unconditional parents at all.

The rule family
---------------
E_t = eligible count that day under RULES v1's own filter (above 200d MA, vol20 < 0.60).
The regime test must be CAUSAL, so "bottom quintile" is an EXPANDING quantile of E over all
history up to t-1 (min 252 valid observations; before that the rule is in the broad regime
by definition).  A full-sample quantile would leak the future and is reported separately,
once, as a look-ahead diagnostic.

    HYB(q, f):  narrow  if  E_t <= Quantile_q(E_{<=t-1})   ->  hold top ceil(f * E_t)
                broad   otherwise                          ->  hold top min(n0, E_t)
                either way equal weight at GROSS / k_t, so gross is constant at 75%.

Tuned parameters (PROTOCOL rule 4: at most two) - q and f.  ALL 16 grid points reported.
Everything else is fixed in advance and not searched: n0 = 20 (idea 2's KEEP-candidate count),
GROSS = 0.75 (live), scorer without /sqrt(vol20) (idea 2's), 200d+vol20 eligibility, weekly
rebalance, 10 bps, next-day execution, 252-observation minimum for the quantile.

Controls and decomposition (structural arms, NOT tuned, none selected on its own result)
---------------------------------------------------------------------------------------
  N20    fixed n=20 at w = 0.75/20, de-grossing when E_t < 20   -> idea 2's actual book
  NF20   fixed n=20 renormalised to 75% gross                   -> the hybrid's broad leg
  F0.35 / F0.45 / F0.85 / F1.00   the unconditional fraction rules idea 46 ran
  At the PRE-REGISTERED q = 0.20 ("bottom quintile", the queue's own wording), three
  narrow-regime treatments that hold the regime test fixed and vary only what is done in it:
     CASH  narrow -> 0% gross (a pure breadth timing gate, idea 40's mechanism)
     HALF  narrow -> the same n0 names at half gross (exposure, not concentration)
     FRAC  narrow -> ceil(0.35 * E_t) names at full gross (concentration, not exposure)
  This is what tells us whether any 2022 benefit is concentration or just less exposure.

Verdicts (both KEEP paths, every point)
    4a: Sharpe > the LIVE book (RULES v2) in BOTH halves AND MaxDD no worse than it.
    4b: Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

Data: data/prices.csv on the corrected trading-day index (aborts if the calendar-day bug of
CHANGELOG 2026-09-04 is present).  Survivorship: research/universe.json is a
current-constituent list of 56 names, so absolute CAGRs are optimistic; the
HYB-vs-parents comparison is the durable part.

Deterministic, standalone.  Reads baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights
from engine import backtest, metrics

COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60          # v1 eligibility, unchanged
GROSS = 0.75            # live gross, FIXED
VOL_SCALE = False       # idea 2's scorer: no /sqrt(vol20)
N0 = 20                 # idea 2's KEEP-candidate count, FIXED (not a tuned parameter here)
MIN_OBS = 252           # observations required before the causal breadth quantile exists
QS = [0.10, 0.20, 0.30, 0.40]
FS = [0.25, 0.35, 0.45, 0.55]
Q_PRE = 0.20            # the queue's pre-registered "bottom quintile"
F_PRE = 0.35            # idea 46's best 2022 fraction, used only in the decomposition arms
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 200)


# ---------------------------------------------------------------- primitives
def eligible_mask(px):
    """RULES v1's own eligibility filter: above the 200d MA and vol20 < 0.60."""
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def eligible_count(px):
    """E_t, with the pre-warm-up rows (no 200d MA yet) set to NaN so they cannot
    contaminate the expanding quantile."""
    elig = eligible_mask(px)
    e = elig.sum(axis=1).astype(float)
    ma_ok = px.rolling(200).mean().notna().any(axis=1)
    return e.where(ma_ok)


def ranked(px):
    s = score(px, vol_scale=VOL_SCALE)[0].where(eligible_mask(px))
    return s.rank(axis=1, ascending=False)


def narrow_flag(e, q, lookahead=False):
    """Causal bottom-q regime test: E_t <= expanding q-quantile of E over history up to t-1.
    NaN (not enough history) -> broad.  lookahead=True uses the full-sample quantile and is
    reported once, as a diagnostic only."""
    if lookahead:
        thr = pd.Series(e.dropna().quantile(q), index=e.index)
    else:
        thr = e.expanding(min_periods=MIN_OBS).quantile(q).shift(1)
    return (e <= thr).where(thr.notna() & e.notna(), False)


# ---------------------------------------------------------------- book construction
def weights_from_k(rank, k, gross):
    """Top-k by rank at gross/k each; gross may be a Series (regime-dependent exposure)."""
    k = k.clip(lower=1.0)
    w_per = gross / k if np.isscalar(gross) else gross.div(k)
    sel = rank.le(k, axis=0)
    return sel.astype(float).mul(w_per, axis=0)


def build(px, kind, q=None, f=None, n=N0):
    """kind in {N, NF, F, HYB, HYB_CASH, HYB_HALF}."""
    rank = ranked(px)
    e = eligible_count(px).fillna(0.0)
    if kind == "N":                                  # idea 2's book: fixed w, de-grosses
        k = pd.Series(float(n), index=px.index)
        return weights_from_k(rank, k, GROSS)
    if kind == "NF":                                 # fixed count, renormalised to 75%
        return weights_from_k(rank, np.minimum(float(n), e), GROSS)
    if kind == "F":                                  # unconditional fraction
        return weights_from_k(rank, np.ceil(f * e), GROSS)

    nar = narrow_flag(eligible_count(px), q)
    k_broad = np.minimum(float(n), e)
    if kind == "HYB":
        k = k_broad.where(~nar, np.ceil(f * e))
        return weights_from_k(rank, k, GROSS)
    if kind == "HYB_CASH":                           # narrow -> flat
        w = weights_from_k(rank, k_broad, GROSS)
        return w.where(~nar, 0.0)
    if kind == "HYB_HALF":                           # narrow -> same names, half exposure
        g = pd.Series(GROSS, index=px.index).where(~nar, GROSS / 2)
        return weights_from_k(rank, k_broad, g)
    raise ValueError(kind)


# ---------------------------------------------------------------- metric helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def verdict_4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def tests_4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    return {"H1": h1 > s1, "H2": h2 > s2,
            "OOS": metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"],
            "DD": abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]),
            "CAGR": m["CAGR"] >= 0.70 * ms["CAGR"]}


def verdict_4b(r, spy, r_oos, spy_oos):
    return all(tests_4b(r, spy, r_oos, spy_oos).values())


def fail_4b(r, spy, r_oos, spy_oos):
    f = [k for k, v in tests_4b(r, spy, r_oos, spy_oos).items() if not v]
    return ",".join(f) if f else "-"


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


def run(px, w, start):
    res = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
    return (res["returns"].loc[start:], res["turnover"].loc[start:],
            res["weights"].loc[start:])


def summarise(name, r, to, held, spy, spy_oos, base):
    m = metrics(r)
    h1, h2 = half_sharpes(r)
    r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
    m_is, m_oos = metrics(r_is), metrics(r_oos)
    d = dict(variant=name, CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
             H1=h1, H2=h2, IS_Sharpe=m_is["Sharpe"], IS_MaxDD=m_is["MaxDD"],
             OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"], OOS_MaxDD=m_oos["MaxDD"],
             p4a=verdict_4a(r, base), p4b=verdict_4b(r, spy, r_oos, spy_oos),
             fail4b=fail_4b(r, spy, r_oos, spy_oos))
    if held is not None:
        d["names"] = (held > 0).sum(axis=1).mean()
        d["gross"] = held.sum(axis=1).mean()
        d["turn"] = to.sum() / m["Years"]
    return d


# ---------------------------------------------------------------- main
def main():
    px = load_universe()
    yrs = px.index.to_series().groupby(px.index.year).count()
    print("=" * 160)
    print(f"Idea 48 breadth-adaptive-count-2022 (lane B) | {SCRIPT}")
    print("=" * 160)
    print(f"Universe: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}")
    print(f"Index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, "
          f"2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting.")
        sys.exit(1)

    start = px.index[260]
    print(f"Eval sample: {start.date()} -> {px.index[-1].date()} | IS <= {IS_END}, OOS >= {OOS_START}")
    print(f"Fixed, not searched: n0={N0}, gross={GROSS:.0%}, scorer OFF, weekly, {COST_BPS} bps, "
          f"quantile min_obs={MIN_OBS}.")
    print(f"Tuned (2): q in {QS}, f in {FS} -> {len(QS)*len(FS)} HYB points, ALL reported.\n")

    base_v2 = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    base_v1 = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]

    # ---------------- premise: does the causal bottom-quintile test actually fire in 2022?
    e_full = eligible_count(px)
    e = e_full.loc[start:]
    print("=" * 160)
    print("PREMISE - the regime test.  If the causal bottom-quintile flag does not fire in 2022,")
    print("the conditional rule cannot reproduce idea 46's 2022 result no matter how f is set.")
    print(f"  E_t of {px.shape[1]} names: mean {e.mean():.1f}, median {e.median():.0f}, "
          f"min {e.min():.0f}, max {e.max():.0f}")
    reg = pd.DataFrame({f"q={q:.2f}": narrow_flag(e_full, q).loc[start:] for q in QS})
    reg["E_t"] = e
    byyear = reg.groupby(reg.index.year).mean()
    byyear["E_t"] = e.groupby(e.index.year).mean()
    print("  share of days flagged NARROW, by year (last column = mean E_t):")
    print(byyear.to_string(float_format=lambda x: f"{x:.2f}"))
    nq = narrow_flag(e_full, Q_PRE).loc[start:]
    print(f"  q={Q_PRE:.2f} overall narrow share {nq.mean():.1%}; "
          f"days before the quantile exists (forced broad): "
          f"{int((e.notna() & narrow_flag(e_full, Q_PRE).loc[start:].eq(False) & e_full.loc[start:].expanding(min_periods=MIN_OBS).quantile(Q_PRE).shift(1).isna()).sum())}")
    la = narrow_flag(e_full, Q_PRE, lookahead=True).loc[start:]
    print(f"  LOOK-AHEAD DIAGNOSTIC (full-sample quantile, not tradable): narrow share "
          f"{la.mean():.1%}, agreement with the causal flag {float((la == nq).mean()):.1%}")
    print()

    # ---------------- the grid
    rows, series, regimes = [], {}, {}
    controls = [("N20", dict(kind="N")), ("NF20", dict(kind="NF")),
                ("F0.25", dict(kind="F", f=0.25)), ("F0.35", dict(kind="F", f=0.35)),
                ("F0.45", dict(kind="F", f=0.45)), ("F0.55", dict(kind="F", f=0.55)),
                ("F0.85", dict(kind="F", f=0.85)), ("F1.00", dict(kind="F", f=1.00))]
    for name, kw in controls:
        r, to, held = run(px, build(px, **kw), start)
        series[name] = r
        rows.append(dict(family="control", q=np.nan, f=kw.get("f", np.nan),
                         **summarise(name, r, to, held, spy, spy_oos, base_v2)))

    for q in QS:
        for f in FS:
            name = f"HYB q{q:.2f} f{f:.2f}"
            r, to, held = run(px, build(px, kind="HYB", q=q, f=f), start)
            series[name] = r
            regimes[name] = narrow_flag(e_full, q).loc[start:]
            rows.append(dict(family="HYB", q=q, f=f,
                             **summarise(name, r, to, held, spy, spy_oos, base_v2)))

    for name, kw in [("DEC cash q0.20", dict(kind="HYB_CASH", q=Q_PRE)),
                     ("DEC half q0.20", dict(kind="HYB_HALF", q=Q_PRE)),
                     ("DEC frac q0.20 f0.35", dict(kind="HYB", q=Q_PRE, f=F_PRE))]:
        r, to, held = run(px, build(px, **kw), start)
        series[name] = r
        rows.append(dict(family="decomp", q=Q_PRE, f=kw.get("f", np.nan),
                         **summarise(name, r, to, held, spy, spy_oos, base_v2)))

    grid = pd.DataFrame(rows).set_index("variant")

    refs = {}
    for nm, r in (("RULES v2 (live)", base_v2), ("RULES v1", base_v1), ("SPY", spy)):
        refs[nm] = dict(family="ref", q=np.nan, f=np.nan,
                        **summarise(nm, r, None, None, spy, spy_oos, base_v2))
    ref = pd.DataFrame(refs).T.drop(columns=["variant"]).rename_axis("variant")

    show = ["family", "CAGR", "Vol", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_MaxDD",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "names", "gross", "turn", "p4a", "p4b", "fail4b"]
    full = pd.concat([grid, ref])
    print("=" * 160)
    print("FULL GRID - 16 HYB points + 8 unconditional controls + 3 decomposition arms + 3 refs.")
    print("names = avg positions, gross = avg invested fraction, turn = turnover x/yr.")
    print(fmt(full.reindex(columns=show)))
    print()
    ms = metrics(spy)
    print(f"4b thresholds: MaxDD cap {-0.60*abs(ms['MaxDD']):.1%}, CAGR floor {0.70*ms['CAGR']:.1%}, "
          f"SPY halves {half_sharpes(spy)[0]:.3f}/{half_sharpes(spy)[1]:.3f}, "
          f"SPY OOS Sharpe {metrics(spy_oos)['Sharpe']:.3f}")
    print(f"4a comparand RULES v2 (live): {metrics(base_v2)['CAGR']:.1%} / "
          f"{metrics(base_v2)['Sharpe']:.3f} / {metrics(base_v2)['MaxDD']:.1%}, halves "
          f"{half_sharpes(base_v2)[0]:.3f}/{half_sharpes(base_v2)[1]:.3f}")
    print(f"Passing 4a: {int(grid.p4a.sum())}/{len(grid)}   passing 4b: {int(grid.p4b.sum())}/{len(grid)}")
    print(f"  of the 16 HYB points: 4a {int(grid[grid.family=='HYB'].p4a.sum())}/16, "
          f"4b {int(grid[grid.family=='HYB'].p4b.sum())}/16")
    print()

    # ---------------- THE TEST: does the conditional clause beat BOTH its parents?
    print("=" * 160)
    print("H1 - DOES THE CONDITIONAL CLAUSE EARN ITS KEEP?  Each HYB point against the two")
    print("unconditional rules it interpolates: NF20 (its broad leg, run always) and F<f> (its")
    print("narrow leg, run always).  A conditional clause is only worth its complexity if it")
    print("beats BOTH.  dX = HYB - parent.")
    h1rows = []
    for q in QS:
        for f in FS:
            k = f"HYB q{q:.2f} f{f:.2f}"
            r = grid.loc[k]
            for pn in ("NF20", f"F{f:.2f}"):
                p = grid.loc[pn]
                h1rows.append(dict(HYB=k, parent=pn, dSharpe=r.Sharpe - p.Sharpe,
                                   dCAGR=r.CAGR - p.CAGR, dMaxDD=r.MaxDD - p.MaxDD,
                                   dOOS_Sharpe=r.OOS_Sharpe - p.OOS_Sharpe,
                                   dH1=r.H1 - p.H1, dH2=r.H2 - p.H2))
    h1 = pd.DataFrame(h1rows).set_index(["HYB", "parent"])
    print(fmt(h1))
    wide = h1.reset_index()
    vs_nf = wide[wide.parent == "NF20"]
    vs_f = wide[wide.parent != "NF20"]
    print(f"\n  vs NF20 (broad leg alone): HYB wins Sharpe {int((vs_nf.dSharpe>0).sum())}/16 "
          f"(mean {vs_nf.dSharpe.mean():+.4f}), OOS Sharpe {int((vs_nf.dOOS_Sharpe>0).sum())}/16 "
          f"(mean {vs_nf.dOOS_Sharpe.mean():+.4f}), CAGR {int((vs_nf.dCAGR>0).sum())}/16 "
          f"(mean {vs_nf.dCAGR.mean():+.2%}), shallower MaxDD {int((vs_nf.dMaxDD>0).sum())}/16")
    print(f"  vs F<f>  (narrow leg alone): HYB wins Sharpe {int((vs_f.dSharpe>0).sum())}/16 "
          f"(mean {vs_f.dSharpe.mean():+.4f}), OOS Sharpe {int((vs_f.dOOS_Sharpe>0).sum())}/16 "
          f"(mean {vs_f.dOOS_Sharpe.mean():+.4f}), CAGR {int((vs_f.dCAGR>0).sum())}/16 "
          f"(mean {vs_f.dCAGR.mean():+.2%})")
    both = set(vs_nf[vs_nf.dSharpe > 0].HYB) & set(vs_f[vs_f.dSharpe > 0].HYB)
    both_oos = set(vs_nf[vs_nf.dOOS_Sharpe > 0].HYB) & set(vs_f[vs_f.dOOS_Sharpe > 0].HYB)
    print(f"  beats BOTH parents on full-sample Sharpe: {len(both)}/16  {sorted(both)}")
    print(f"  beats BOTH parents on OOS Sharpe:         {len(both_oos)}/16  {sorted(both_oos)}")
    print()

    # ---------------- H2: the 2022 claim itself
    print("=" * 160)
    print("H2 - THE 2022 CLAIM.  Calendar-year total returns.  NOTE: 2022 is the year the")
    print("hypothesis was generated from, so its column is description, not evidence.")
    keys = ["N20", "NF20", "F0.35", "F0.45", "HYB q0.20 f0.35", "HYB q0.20 f0.45",
            "HYB q0.10 f0.35", "HYB q0.40 f0.35", "DEC cash q0.20", "DEC half q0.20"]
    yr = pd.DataFrame({k: (1 + series[k]).groupby(series[k].index.year).prod() - 1 for k in keys})
    yr["RULES v2"] = (1 + base_v2).groupby(base_v2.index.year).prod() - 1
    yr["SPY"] = (1 + spy).groupby(spy.index.year).prod() - 1
    print(yr.to_string(float_format=lambda x: f"{x:+.1%}"))
    print()
    stress = [y for y in (2011, 2015, 2018, 2020, 2022) if y in yr.index]
    print("  stress-year means (2011/2015/2018/2020/2022):")
    print("   " + "  ".join(f"{k}:{yr.loc[stress, k].mean():+.1%}" for k in yr.columns))
    print(f"  2022 only: " + "  ".join(f"{k}:{yr.loc[2022, k]:+.1%}" for k in yr.columns))
    print("  non-2022 years mean:")
    nz = [y for y in yr.index if y != 2022]
    print("   " + "  ".join(f"{k}:{yr.loc[nz, k].mean():+.1%}" for k in yr.columns))
    print()

    # ---------------- H3: concentration vs exposure
    print("=" * 160)
    print("H3 - WHAT DOES THE NARROW LEG ACTUALLY BUY?  Same regime test (q=0.20), three")
    print("treatments: flat (pure timing), half gross (exposure), fraction (concentration).")
    dec = grid.loc[["NF20", "DEC cash q0.20", "DEC half q0.20", "DEC frac q0.20 f0.35"],
                   ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
                    "OOS_MaxDD", "gross", "turn"]]
    dec["2022"] = [yr.loc[2022, k] if k in yr else np.nan
                   for k in ["NF20", "DEC cash q0.20", "DEC half q0.20", "HYB q0.20 f0.35"]]
    print(fmt(dec))
    print()

    # ---------------- H4: conditional return attribution
    print("=" * 160)
    print("H4 - ATTRIBUTION.  Annualised return earned on NARROW days vs BROAD days (q=0.20),")
    print("for the hybrid and for both parents.  Shows where any difference is actually made.")
    nar = narrow_flag(e_full, Q_PRE).loc[start:]
    att = []
    for k in ("NF20", "F0.35", "HYB q0.20 f0.35", "SPY"):
        r = spy if k == "SPY" else series[k]
        for tag, mask in (("narrow", nar), ("broad", ~nar)):
            rr = r[mask]
            att.append(dict(book=k, regime=tag, days=int(mask.sum()),
                            ann_ret=(1 + rr).prod() ** (252 / max(len(rr), 1)) - 1,
                            ann_vol=rr.std() * np.sqrt(252),
                            tot_contrib=(1 + rr).prod() - 1))
    print(pd.DataFrame(att).set_index(["book", "regime"]).to_string(
        float_format=lambda x: f"{x:.3f}"))
    print()

    # ---------------- rule 8 walk-forward
    print("=" * 160)
    print("WALK-FORWARD (PROTOCOL rule 8) - (q, f) chosen on 2009-2016 ONLY; 2017-2026 read once.")
    print("This is the only uncontaminated evidence here, because 2022 is inside the OOS window.")
    is_dd_cap = 0.60 * abs(metrics(spy_is)["MaxDD"])
    print(f"  IS SPY: Sharpe {metrics(spy_is)['Sharpe']:.3f}, MaxDD {metrics(spy_is)['MaxDD']:.1%} "
          f"-> S2 IS DD cap {-is_dd_cap:.1%}")
    print(f"  OOS SPY:      CAGR {metrics(spy_oos)['CAGR']:6.1%}  Sharpe {metrics(spy_oos)['Sharpe']:.3f}  "
          f"MaxDD {metrics(spy_oos)['MaxDD']:.1%}")
    for nm, r in (("OOS RULES v2", base_v2), ("OOS RULES v1", base_v1)):
        m = metrics(r.loc[OOS_START:])
        print(f"  {nm}: CAGR {m['CAGR']:6.1%}  Sharpe {m['Sharpe']:.3f}  MaxDD {m['MaxDD']:.1%}")
    wf = []
    fams = [("HYB (q,f)", grid[grid.family == "HYB"]),
            ("F (f only)", grid[grid.index.str.startswith("F")]),
            ("fixed n (control)", grid.loc[["N20", "NF20"]])]
    for fam, sub in fams:
        s1 = sub.sort_values("IS_Sharpe", ascending=False).index[0]
        ok = sub[sub.IS_MaxDD >= -is_dd_cap]
        s2 = ok.sort_values("IS_Sharpe", ascending=False).index[0] if len(ok) else None
        for rule, p in (("S1 IS-Sharpe", s1), ("S2 4b-aware", s2)):
            d = dict(family=fam, rule=rule, pick=(p if p else "none (no IS point met the DD cap)"))
            if p:
                d.update(grid.loc[p, ["IS_Sharpe", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe",
                                      "OOS_MaxDD", "p4a", "p4b", "fail4b"]].to_dict())
                d["OOS_2022"] = yr.loc[2022, p] if p in yr else (
                    (1 + series[p]).groupby(series[p].index.year).prod() - 1).loc[2022]
            wf.append(d)
    wfdf = pd.DataFrame(wf).set_index(["family", "rule"])
    print(wfdf.to_string(float_format=lambda x: f"{x:.3f}"))
    print()
    print("  OOS column for ALL 16 HYB points (no selection), so the walk-forward pick can be audited:")
    print(fmt(grid[grid.family == "HYB"][["IS_Sharpe", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe",
                                          "OOS_MaxDD", "p4b", "fail4b"]]))
    print()

    # ---------------- rule 9 robustness
    print("=" * 160)
    print("ROBUSTNESS (rule 9) - the same arms on research/universe_broad.json.  Also a")
    print("current-constituent list, so this bounds survivorship rather than removing it.")
    try:
        pxb = load_universe(broad=True)
        sb = pxb.index[260]
        spyb = pxb["SPY"].pct_change().fillna(0).loc[sb:]
        spyb_oos = spyb.loc[OOS_START:]
        eb = eligible_count(pxb)
        bb = backtest(pxb, rules_v2_weights(pxb), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[sb:]
        print(f"  {pxb.shape[1]} tickers, {sb.date()} -> {pxb.index[-1].date()}; "
              f"E_t mean {eb.loc[sb:].mean():.1f}; narrow share at q={Q_PRE:.2f}: "
              f"{narrow_flag(eb, Q_PRE).loc[sb:].mean():.1%} "
              f"(2022 {narrow_flag(eb, Q_PRE).loc['2022'].mean():.1%})")
        brows = []
        for name, kw in [("N20", dict(kind="N")), ("NF20", dict(kind="NF")),
                         ("F0.35", dict(kind="F", f=0.35)), ("F0.45", dict(kind="F", f=0.45)),
                         ("F0.85", dict(kind="F", f=0.85))] + \
                        [(f"HYB q{q:.2f} f{f:.2f}", dict(kind="HYB", q=q, f=f))
                         for q in QS for f in FS]:
            rb = backtest(pxb, build(pxb, **kw), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[sb:]
            brows.append(summarise(name, rb, None, None, spyb, spyb_oos, bb))
        bdf = pd.DataFrame(brows).set_index("variant")
        bdf.loc["SPY(broad)"] = summarise("SPY(broad)", spyb, None, None, spyb, spyb_oos, bb)
        bdf.loc["RULES v2(broad)"] = summarise("RULES v2(broad)", bb, None, None, spyb, spyb_oos, bb)
        print(fmt(bdf.drop(columns=["variant"], errors="ignore")))
        hb = bdf.loc[[i for i in bdf.index if i.startswith("HYB")]]
        print(f"  broad-universe HYB: 4a {int(hb.p4a.sum())}/16, 4b {int(hb.p4b.sum())}/16; "
              f"beats NF20 on Sharpe {int((hb.Sharpe > bdf.loc['NF20','Sharpe']).sum())}/16")
    except Exception as ex:
        print(f"  broad-universe replication unavailable: {type(ex).__name__}: {ex}")
    print()

    # ---------------- leaderboard
    print("=" * 160)
    print("LEADERBOARD rows (all 27 grid points, no selection):")
    today = "2026-09-07"
    b0 = metrics(base_v2)
    bh1, bh2 = half_sharpes(base_v2)
    for k, r in grid.iterrows():
        v = "KEEP 4b" if r.p4b else ("KEEP 4a" if r.p4a else f"KILL (4b fails: {r.fail4b})")
        print(f"| {today} | 48 {k} | {r.CAGR:.1%} | {r.Sharpe:.2f} | {r.MaxDD:.1%} | "
              f"{r.H1:.2f} / {r.H2:.2f} | {b0['Sharpe']:.2f} ({bh1:.2f}/{bh2:.2f}) | {v} | {SCRIPT} |")
    grid.to_csv(Path(__file__).with_suffix(".grid.csv"))
    print(f"\nGrid written to {Path(__file__).with_suffix('.grid.csv').name}")


if __name__ == "__main__":
    main()
