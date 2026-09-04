#!/usr/bin/env python3
"""Idea 2 - "position-count": how many names should the book hold?

The question, and why it is not the trivial one
------------------------------------------------
RULES v1 holds the top 5 eligible names at a FIXED 15% each, so its position count and its
gross exposure are the same dial: n=3 is a 45%-invested book, n=8 a 120% (levered) one.
Every prior result that varied n (ideas 1 and 40) therefore varied two things at once.
This script separates them:

    Arm A  FIXEDW  - v1's own construction, w = 15% per name, gross = 0.15*n.  n <= 6 only,
                     because PROTOCOL rule 2 forbids leverage and n=7 is already 105%.
    Arm B  EQW     - equal weight at a CONSTANT 75% gross (v1's live gross), w = 0.75/n.
                     This is the idea as queued ("top 3 vs 5 vs 8 equal-weight") and it is
                     the only arm in which n is purely a diversification choice.

Both arms are run twice, once on the live v1 composite and once with the `/sqrt(vol20)` term
removed, because the CHANGELOG's standing diagnosis is that the scaler cancels the momentum
signal (idea 1: worth +10.1%/yr to drop) and because idea 1's nearest 4b miss - OFF n=8 at 75%
gross - failed on H1 Sharpe alone with drawdown to spare.  The open question that follows is
exactly a position-count question: does holding MORE names buy the H1 Sharpe that the n<=8
books lacked?  n is swept out to 20 to answer it.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. n   positions held.
That is the only one.  The two arms (FIXEDW / EQW) and the two scorers (ON / OFF) are
structural variants, not tuned choices: all four combinations are reported in full and none
is selected on the strength of its own result.  Gross (75%), w (15%), the 200d / vol20 < 0.60
eligibility filter, the 21-63-126-252d lookbacks, the weekly schedule, 10 bps costs and
next-day execution are all RULES v1's own and are held fixed.

Grid = ON/OFF x [ FIXEDW n in {2,3,4,5,6} + EQW n in {2,3,4,5,6,8,10,12,15,20} ] = 30 points,
ALL reported.

Walk-forward (PROTOCOL rule 8) - selection rules fixed before any OOS number is read
------------------------------------------------------------------------------------
Parameters chosen on 2009-2016 ONLY, evaluated untouched on 2017-2026.
    S1 (Sharpe):    within each arm, the n with the highest in-sample Sharpe; ties -> smaller n.
    S2 (4b-aware):  the same, restricted to points whose in-sample MaxDD is within 60% of SPY's
                    in-sample MaxDD.  "none" if no point qualifies.
Both rules reported for all four arms, and the OOS column of every one of the 30 points is
printed, so the selection can be audited rather than trusted.

Verdicts (both KEEP paths evaluated for every point)
    4a (beat the book):   Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b (capital-worthy):  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
                          CAGR >= 70% of SPY's.

Data: data/prices.csv on the corrected trading-day index (commit c006b43); verified in-script.
Survivorship caveat: research/universe.json is a current-constituent list, which flatters any
momentum book - the absolute CAGRs below are optimistic, the ranking across n much less so.

Deterministic, standalone.  Reads baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights
from engine import backtest, metrics

COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60          # v1 eligibility, unchanged
GROSS = 0.75            # v1's live gross, FIXED (EQW arm)
W_FIXED = 0.15          # v1's live per-name weight, FIXED (FIXEDW arm)
NS_EQW = [2, 3, 4, 5, 6, 8, 10, 12, 15, 20]
NS_FIXEDW = [2, 3, 4, 5, 6]          # n=7 would be 105% gross -> leverage, excluded
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 100)


# ---------------------------------------------------------------- book construction
def eligible_mask(px):
    """RULES v1's own eligibility filter: above the 200d MA and vol20 < 0.60."""
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def weights(px, n, sizing, vol_scale):
    """Top-n eligible names by the v1 composite (with or without /sqrt(vol20)).

    sizing 'FIXEDW' -> w = 15% each (gross = 0.15n, v1's construction)
    sizing 'EQW'    -> w = 0.75/n   (gross constant at 75%)
    """
    s = score(px, vol_scale=vol_scale)[0]
    rank = s.where(eligible_mask(px)).rank(axis=1, ascending=False)
    w = W_FIXED if sizing == "FIXEDW" else GROSS / n
    return (rank <= n).astype(float) * w


# ---------------------------------------------------------------- metric helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def verdict_4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def verdict_4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    return bool(h1 > s1 and h2 > s2
                and metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]
                and abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"])
                and m["CAGR"] >= 0.70 * ms["CAGR"])


def fail_4b(r, spy, r_oos, spy_oos):
    """Which of 4b's five tests fail, so near-misses can be read off the table."""
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


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


def label(scaler, sizing, n):
    return f"{scaler:<3} {sizing:<6} n={n:<2}"


# ---------------------------------------------------------------- main
def main():
    px = load_universe()
    yrs = px.index.to_series().groupby(px.index.year).count()
    print("=" * 150)
    print(f"Idea 2 position-count (lane A) | {SCRIPT}")
    print("=" * 150)
    print(f"Universe: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}")
    print(f"Index sanity (must be ~252 rows/yr; the calendar-day bug gave 365): "
          f"2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - results below are not comparable. Aborting.")
        sys.exit(1)

    start = px.index[260]                      # same warm-up skip baseline.compare() uses
    print(f"Eval sample: {start.date()} -> {px.index[-1].date()} | IS <= {IS_END}, OOS >= {OOS_START}")
    print(f"Arms: FIXEDW (w={W_FIXED:.0%} each, gross=0.15n, v1's construction, n<=6 to avoid leverage)")
    print(f"      EQW    (w=0.75/n, gross constant {GROSS:.0%}) - the queued 'equal-weight' test")
    print(f"Scorers: ON = v1 composite; OFF = same without /sqrt(vol20). Both fully reported.")
    print(f"Grid: 2 x ({len(NS_FIXEDW)} + {len(NS_EQW)}) = "
          f"{2*(len(NS_FIXEDW)+len(NS_EQW))} points, all reported. Tuned parameter: n only.\n")

    base_v1 = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]

    # how many names are even eligible? n=20 is meaningless if only 12 pass the filter.
    elig = eligible_mask(px).loc[start:]
    ec = elig.sum(axis=1)
    print(f"Eligible names per day: mean {ec.mean():.1f}, median {ec.median():.0f}, "
          f"10th pct {ec.quantile(.10):.0f}, min {ec.min():.0f}, max {ec.max():.0f} "
          f"(of {px.shape[1]}). Days with <20 eligible: {(ec < 20).mean():.0%}; "
          f"<8: {(ec < 8).mean():.0%}\n")

    # ---- run the grid
    rows, series = [], {}
    for vol_scale, tag in ((True, "ON"), (False, "OFF")):
        for sizing, ns in (("FIXEDW", NS_FIXEDW), ("EQW", NS_EQW)):
            for n in ns:
                res = backtest(px, weights(px, n, sizing, vol_scale), cost_bps=COST_BPS, freq=FREQ)
                r = res["returns"].loc[start:]
                to = res["turnover"].loc[start:]
                held = res["weights"].loc[start:]
                m = metrics(r)
                h1, h2 = half_sharpes(r)
                r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                m_is, m_oos = metrics(r_is), metrics(r_oos)
                key = label(tag, sizing, n)
                series[key] = r
                rows.append(dict(variant=key, scaler=tag, sizing=sizing, n=n,
                                 gross=(W_FIXED * n if sizing == "FIXEDW" else GROSS),
                                 CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                 H1=h1, H2=h2,
                                 IS_Sharpe=m_is["Sharpe"], IS_MaxDD=m_is["MaxDD"],
                                 OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"],
                                 OOS_MaxDD=m_oos["MaxDD"],
                                 names=(held > 0).sum(axis=1).mean(),
                                 turn=to.sum() / m["Years"],
                                 p4a=verdict_4a(r, base_v1), p4b=verdict_4b(r, spy, r_oos, spy_oos),
                                 fail4b=fail_4b(r, spy, r_oos, spy_oos)))
    grid = pd.DataFrame(rows).set_index("variant")

    ref = {}
    for nm, r in (("RULES v1 baseline", base_v1), ("SPY", spy)):
        m = metrics(r)
        h1, h2 = half_sharpes(r)
        m_oos = metrics(r.loc[OOS_START:])
        ref[nm] = dict(scaler="-", sizing="-", n=np.nan, gross=np.nan, CAGR=m["CAGR"], Vol=m["Vol"],
                       Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                       IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                       IS_MaxDD=metrics(r.loc[:IS_END])["MaxDD"],
                       OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"], OOS_MaxDD=m_oos["MaxDD"],
                       names=np.nan, turn=np.nan, p4a=False, p4b=False, fail4b="-")
    full = pd.concat([grid, pd.DataFrame(ref).T.rename_axis("variant")])

    show = ["gross", "CAGR", "Vol", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_MaxDD",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "names", "turn", "p4a", "p4b", "fail4b"]
    print("=" * 150)
    print("FULL GRID - all 30 points. H1/H2 = Sharpe by sample half. names = avg positions held "
          "(< n when fewer are eligible). turn = turnover x/yr. fail4b = which 4b tests fail.")
    print(fmt(full[show]))
    print()

    m_spy = metrics(spy)
    print(f"4b thresholds on this sample: MaxDD cap {-0.60*abs(m_spy['MaxDD']):.1%}, "
          f"CAGR floor {0.70*m_spy['CAGR']:.1%}, SPY halves {half_sharpes(spy)[0]:.3f} / "
          f"{half_sharpes(spy)[1]:.3f}, SPY OOS Sharpe {metrics(spy_oos)['Sharpe']:.3f}")
    print()

    # ---- the actual question: is n a diversification dial or a leverage dial?
    print("=" * 150)
    print("DECOMPOSITION - what n does when gross is held constant (EQW) vs when it is not (FIXEDW).")
    for tag in ("ON", "OFF"):
        for sizing in ("FIXEDW", "EQW"):
            sub = grid[(grid.scaler == tag) & (grid.sizing == sizing)]
            print(f"  {tag}/{sizing}: Sharpe by n -> " +
                  "  ".join(f"n={int(r.n)}:{r.Sharpe:.3f}" for r in sub.itertuples()))
            print(f"  {' '*len(tag)} {' '*len(sizing)}  Vol by n    -> " +
                  "  ".join(f"n={int(r.n)}:{r.Vol:.3f}" for r in sub.itertuples()))
            print(f"  {' '*len(tag)} {' '*len(sizing)}  MaxDD by n  -> " +
                  "  ".join(f"n={int(r.n)}:{r.MaxDD:.1%}" for r in sub.itertuples()))
    print()
    # correlation of the EQW books across n: if ~1.0, n is not changing the book, only its noise
    for tag in ("ON", "OFF"):
        cols = [label(tag, "EQW", n) for n in NS_EQW]
        c = pd.DataFrame({k: series[k] for k in cols}).corr()
        print(f"  {tag}/EQW daily-return correlation, n=2 vs n=20: {c.iloc[0, -1]:.3f}; "
              f"n=5 vs n=20: {c.loc[label(tag,'EQW',5), label(tag,'EQW',20)]:.3f}; "
              f"n=5 vs n=8: {c.loc[label(tag,'EQW',5), label(tag,'EQW',8)]:.3f}")
    print()

    # ---- the decisive test: is n anything more than a de-risking lever?
    # Idea 20 established that gross exposure is a pure lever (corr 1.00 with the 100% version).
    # If raising n only lowers vol, it is the same lever wearing a different hat and adds nothing.
    # So scale every EQW book, ex post, by the constant 12%/realised-vol and compare CAGR at
    # matched risk. This is a DIAGNOSTIC, not a tradable rule (the scalar uses full-sample vol).
    print("=" * 150)
    print("MATCHED-VOL TEST - every EQW book scaled by a constant to 12% full-sample vol.")
    print("If n were only a de-risking lever these CAGRs would be flat in n.")
    for tag in ("ON", "OFF"):
        out = []
        for n in NS_EQW:
            r = series[label(tag, "EQW", n)]
            k = 0.12 / metrics(r)["Vol"]
            m = metrics(r * k)
            out.append(f"n={n}:{m['CAGR']:.1%}/{m['MaxDD']:.0%}")
        print(f"  {tag}/EQW  CAGR at 12% vol / MaxDD -> " + "  ".join(out))
    r = spy
    m = metrics(spy * (0.12 / metrics(spy)["Vol"]))
    print(f"  SPY at 12% vol: {m['CAGR']:.1%} / {m['MaxDD']:.0%}")
    print()

    # ---- stress years
    print("=" * 150)
    print("STRESS YEARS (calendar-year total return):")
    keys = [label("ON", "FIXEDW", 5), label("ON", "EQW", 5), label("ON", "EQW", 20),
            label("OFF", "EQW", 5), label("OFF", "EQW", 8), label("OFF", "EQW", 12),
            label("OFF", "EQW", 20)]
    yr = pd.DataFrame({k: (1 + series[k]).groupby(series[k].index.year).prod() - 1 for k in keys})
    yr["RULES v1"] = (1 + base_v1).groupby(base_v1.index.year).prod() - 1
    yr["SPY"] = (1 + spy).groupby(spy.index.year).prod() - 1
    print(yr.to_string(float_format=lambda x: f"{x:+.1%}"))
    print()

    # ---- walk-forward, PROTOCOL rule 8
    print("=" * 150)
    print("WALK-FORWARD (rule 8): n chosen on 2009-2016 only, evaluated on 2017-2026 untouched.")
    is_dd_cap = 0.60 * abs(metrics(spy_is)["MaxDD"])
    print(f"  In-sample SPY: Sharpe {metrics(spy_is)['Sharpe']:.3f}, MaxDD "
          f"{metrics(spy_is)['MaxDD']:.1%} -> S2 in-sample DD cap {-is_dd_cap:.1%}")
    print(f"  OOS SPY: CAGR {metrics(spy_oos)['CAGR']:.1%}, Sharpe {metrics(spy_oos)['Sharpe']:.3f}, "
          f"MaxDD {metrics(spy_oos)['MaxDD']:.1%}")
    print(f"  OOS RULES v1: CAGR {metrics(base_v1.loc[OOS_START:])['CAGR']:.1%}, Sharpe "
          f"{metrics(base_v1.loc[OOS_START:])['Sharpe']:.3f}, MaxDD "
          f"{metrics(base_v1.loc[OOS_START:])['MaxDD']:.1%}")
    wf_rows = []
    for tag in ("ON", "OFF"):
        for sizing in ("FIXEDW", "EQW"):
            sub = grid[(grid.scaler == tag) & (grid.sizing == sizing)]
            s1 = sub.sort_values(["IS_Sharpe", "n"], ascending=[False, True]).index[0]
            ok = sub[sub.IS_MaxDD >= -is_dd_cap]
            s2 = (ok.sort_values(["IS_Sharpe", "n"], ascending=[False, True]).index[0]
                  if len(ok) else None)
            for rule, p in (("S1 Sharpe", s1), ("S2 4b-aware", s2)):
                d = dict(rule=f"{tag}/{sizing} / {rule}",
                         pick=(p if p else "none (no IS point met the DD cap)"))
                if p:
                    d.update(grid.loc[p, ["IS_Sharpe", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe",
                                          "OOS_MaxDD", "p4a", "p4b", "fail4b"]].to_dict())
                wf_rows.append(d)
    print(pd.DataFrame(wf_rows).set_index("rule").to_string(float_format=lambda x: f"{x:.3f}"))
    print()

    # ---- robustness: does the n-effect replicate on a different (broader) universe?
    # NOT a tuning arm and nothing is selected from it. The 56-name universe.json is a
    # current-constituent list, so a book holding the top 20 of ~37 eligible names holds over
    # half the survivorship-selected list - exactly where the bias is worst. If the n-effect is
    # real it should also appear on the 136-name broad list; if it is survivorship it need not.
    print("=" * 150)
    print("ROBUSTNESS - same OFF/EQW n-sweep on research/universe_broad.json (rule 9). Also a")
    print("current-constituent list, so this bounds the bias rather than removing it.")
    try:
        pxb = load_universe(broad=True)
        startb = pxb.index[260]
        spyb = pxb["SPY"].pct_change().fillna(0).loc[startb:]
        brows = []
        for n in NS_EQW + [30, 40]:
            rb = backtest(pxb, weights(pxb, n, "EQW", False),
                          cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
            mb = metrics(rb)
            h1, h2 = half_sharpes(rb)
            brows.append(dict(n=n, CAGR=mb["CAGR"], Vol=mb["Vol"], Sharpe=mb["Sharpe"],
                              MaxDD=mb["MaxDD"], H1=h1, H2=h2,
                              OOS_CAGR=metrics(rb.loc[OOS_START:])["CAGR"],
                              OOS_Sharpe=metrics(rb.loc[OOS_START:])["Sharpe"],
                              OOS_MaxDD=metrics(rb.loc[OOS_START:])["MaxDD"]))
        bdf = pd.DataFrame(brows).set_index("n")
        msb = metrics(spyb)
        bdf.loc["SPY(broad sample)"] = dict(CAGR=msb["CAGR"], Vol=msb["Vol"], Sharpe=msb["Sharpe"],
                                            MaxDD=msb["MaxDD"], H1=half_sharpes(spyb)[0],
                                            H2=half_sharpes(spyb)[1],
                                            OOS_CAGR=metrics(spyb.loc[OOS_START:])["CAGR"],
                                            OOS_Sharpe=metrics(spyb.loc[OOS_START:])["Sharpe"],
                                            OOS_MaxDD=metrics(spyb.loc[OOS_START:])["MaxDD"])
        print(f"  Broad universe: {pxb.shape[1]} tickers, sample {startb.date()} -> "
              f"{pxb.index[-1].date()}")
        print(fmt(bdf))
    except Exception as e:
        print(f"  broad-universe replication unavailable: {type(e).__name__}: {e}")
    print()

    # ---- leaderboard rows
    print("=" * 150)
    print("LEADERBOARD rows (all 30 grid points):")
    today = pd.Timestamp("2026-09-04").date()
    b0 = metrics(base_v1)
    bh1, bh2 = half_sharpes(base_v1)
    for k, r in grid.iterrows():
        v = ("KEEP 4b" if r.p4b else ("KEEP 4a" if r.p4a else
             f"KILL 4a / KILL 4b ({r.fail4b})"))
        print(f"| {today} | 2 {k} | {r.CAGR:.1%} | {r.Sharpe:.2f} | {r.MaxDD:.1%} | "
              f"{r.H1:.2f} / {r.H2:.2f} | {b0['Sharpe']:.2f} ({bh1:.2f}/{bh2:.2f}) | {v} | {SCRIPT} |")
    print()
    print(f"Grid points passing 4a: {int(grid.p4a.sum())} / {len(grid)}; "
          f"passing 4b: {int(grid.p4b.sum())} / {len(grid)}")


if __name__ == "__main__":
    main()
