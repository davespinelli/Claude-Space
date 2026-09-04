#!/usr/bin/env python3
"""Idea 49 - "third-universe-portability": do the project's two 4b KEEP-candidates survive a
THIRD, structurally different universe?

The question
------------
Idea 2 (lane A) produced `N n=20`  - top 20 eligible names, equal weight at 75% gross, scored
without `/sqrt(vol20)`, cash when fewer than 20 are eligible.  Idea 46 (lane B) produced
`F f=0.85` - the top 85% of whatever is eligible, same weighting.  The argument for f=0.85
over n=20 was portability: it passes 4b on BOTH research/universe.json (56 current-constituent
mega-caps/ETFs) and research/universe_broad.json (136 names), where n=20 passes on one and
misses 4b's H2 on the other by 0.02.

Two overlapping lists of US large caps is not a replication.  Both lists are dominated by the
same 2009-2026 mega-cap/QQQ regime, and universe_broad.json is close to a superset of
universe.json.  The small-cap panel (data/prices_small.csv.gz, 483 sub-$2B names since 2010)
is the first structurally DIFFERENT universe available offline: different market cap, different
liquidity, different factor exposure, ~8x more names, and a much larger and more volatile
eligible count (E_t averages 141 of 439 here vs 37.5 of 56 on universe.json).

This run re-tests both candidates there, with parameters FIXED IN ADVANCE at n=20 and f=0.85.
Nothing is tuned to the small panel; the whole grid is re-run only so the two pre-registered
points can be read in context.

Arms (identical construction to idea 46, so the numbers are directly comparable)
--------------------------------------------------------------------------------
  N   top n eligible at 0.75/n each; when E_t < n the book holds all of them and the rest
      goes to cash (this is idea 2's KEEP-candidate wording, cash clause included).
  NF  top min(n, E_t) at 0.75/min(n, E_t) - always 75% invested.  Decomposition arm only.
  F   top ceil(f x E_t) at 0.75/ceil(f x E_t) - always 75% invested, count adapts daily.

Tuned parameters (PROTOCOL rule 4: at most two): arm N/NF n only, arm F f only.  Everything
else is RULES v1's own and held fixed: 200d-MA + vol20 < 0.60 eligibility, the 21-63-126-252d
composite lookbacks, 75% gross, weekly rebalance, 10 bps, next-day execution, scorer without
`/sqrt(vol20)`.

Grid = idea 46's exact grid (8 n x 2 count arms + 8 f = 24 points), ALL reported.  Four extra
n values (40/60/90/120) are added as a MATCHED-BOOK-SIZE diagnostic only - a 439-name panel
makes f=0.85 hold ~120 names, which no n in idea 46's grid reaches - and they are EXCLUDED
from every walk-forward selection pool so the replication stays pre-registered.

Walk-forward (PROTOCOL rule 8) - selection rules fixed before any OOS number is read
------------------------------------------------------------------------------------
Parameters chosen on <=2016 ONLY, evaluated untouched 2017-2026.
    S1 (Sharpe):    highest in-sample Sharpe within the arm; ties -> larger n / larger f.
    S2 (4b-aware):  the same, restricted to points whose in-sample MaxDD is within 60% of
                    SPY's in-sample MaxDD.  "none" if no point qualifies.

Benchmarks and verdicts
-----------------------
    4a (beat the book):  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
                         The live book runs on universe.json, so 4a is judged against v1 on
                         universe.json restricted to THIS sample window.  v1 applied to the
                         small panel itself is reported too, as a construction control.
    4b (capital-worthy): Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
                         CAGR >= 70% of SPY's.
Two further controls: equal-weight all 439 names with no filter at all (what the eligibility
filter has to beat), and IWM-free - there is no small-cap benchmark in the cache, so SPY is
the only 4b benchmark available and the comparison is stated as such.

Costs: the panel is sub-$2B names, where 10 bps of one-way turnover is optimistic.  The two
pre-registered points are re-run at 25 and 50 bps as a diagnostic (not a tuning arm).

Data: data/prices_small.csv.gz via baseline.load_universe(small=True), trading-day indexed
(verified in-script).  44 names with max_1d_move >= 1.0 in data/small_meta.csv are excluded
(corrupted/relisted), leaving 439.
SURVIVORSHIP: every one of the 483 names trades through 2026-09-03 - this is a screen of
CURRENT sub-$2B constituents, so the panel contains no delistings and no bankruptcies at all.
Small-cap survivorship is far more severe than large-cap survivorship, so absolute returns
here are optimistic by more than on the other two lists.  A KILL is therefore strong evidence
and a PASS would have been weak evidence; read the verdict with that asymmetry in mind.

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
MAX_VOL = 0.60
GROSS = 0.75
VOL_SCALE = False
NS = [5, 8, 10, 12, 15, 20, 25, 30]          # idea 46's grid - the selection pool
NS_DIAG = [40, 60, 90, 120]                  # matched-book-size diagnostic, NOT selectable
FS = [0.15, 0.25, 0.35, 0.45, 0.55, 0.70, 0.85, 1.00]
PRE = [("N", 20), ("F", 0.85)]               # the two pre-registered candidates
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 200)


# ---------------------------------------------------------------- universe
def small_panel():
    """The 439 investable names (SPY held out as benchmark, 44 corrupted names dropped)."""
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in px.columns if c != "SPY" and c not in bad]
    return px[inv], px["SPY"], sorted(bad)


# ---------------------------------------------------------------- book construction
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def _ranked(px):
    elig = eligible_mask(px)
    s = score(px, vol_scale=VOL_SCALE)[0].where(elig)
    return s.rank(axis=1, ascending=False), elig.sum(axis=1)


def weights(px, arm, p):
    rank, ecount = _ranked(px)
    if arm == "N":
        k = pd.Series(float(p), index=px.index)
    elif arm == "NF":
        k = np.minimum(float(p), ecount.astype(float)).clip(lower=1.0)
    else:
        k = np.ceil(float(p) * ecount.astype(float)).clip(lower=1.0)
    sel = rank.le(k, axis=0)
    return sel.astype(float).mul(GROSS / k, axis=0)


def equal_weight_all(px):
    """Control: hold every name in the panel, no filter, 75% gross."""
    live = px.notna() & (px.shift(1).notna())
    n = live.sum(axis=1).clip(lower=1)
    return live.astype(float).div(n, axis=0) * GROSS


# ---------------------------------------------------------------- metric helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def verdict_4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def _tests_4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    return {"H1": h1 > s1, "H2": h2 > s2,
            "OOS": metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"],
            "DD": abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]),
            "CAGR": m["CAGR"] >= 0.70 * ms["CAGR"]}


def verdict_4b(r, spy, r_oos, spy_oos):
    return all(_tests_4b(r, spy, r_oos, spy_oos).values())


def fail_4b(r, spy, r_oos, spy_oos):
    f = [k for k, v in _tests_4b(r, spy, r_oos, spy_oos).items() if not v]
    return ",".join(f) if f else "-"


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


def label(arm, p):
    return f"{arm:<2} {'n=' + str(p) if arm != 'F' else 'f=' + format(p, '.2f'):<7}"


# ---------------------------------------------------------------- main
def main():
    px, spy_px, bad = small_panel()
    yrs = px.index.to_series().groupby(px.index.year).count()
    print("=" * 155)
    print(f"Idea 49 third-universe-portability (lane B) | {SCRIPT}")
    print("=" * 155)
    print(f"Small-cap panel: {px.shape[1]} investable tickers "
          f"({px.shape[1] + len(bad)} in file, {len(bad)} excluded for max_1d_move >= 1.0), "
          f"{px.index[0].date()} -> {px.index[-1].date()}")
    print(f"  excluded: {', '.join(bad[:12])}{' ...' if len(bad) > 12 else ''}")
    print(f"Index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, "
          f"2024 {yrs.get(2024)}")
    if yrs.loc[2013:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting.")
        sys.exit(1)

    start = px.index[260]
    print(f"Eval sample: {start.date()} -> {px.index[-1].date()} | IS <= {IS_END}, OOS >= {OOS_START}")
    print(f"Scorer OFF (no /sqrt(vol20)); gross {GROSS:.0%}; weekly; {COST_BPS} bps; next-day fill.")
    print(f"Pre-registered points (fixed before this run): N n=20 (idea 2), F f=0.85 (idea 46).")
    print(f"Selection pool = idea 46's grid ({2*len(NS)+len(FS)} points). "
          f"N n={NS_DIAG} are matched-size diagnostics, excluded from selection.\n")

    spy = spy_px.pct_change().fillna(0).loc[start:]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]

    # RULES v1 on universe.json (the LIVE book) restricted to this window = the 4a benchmark
    px_main = load_universe()
    v1_live = backtest(px_main, rules_v1_weights(px_main),
                       cost_bps=COST_BPS, freq=FREQ)["returns"].reindex(px.index).fillna(0).loc[start:]
    # v1 applied to the small panel itself - construction control
    v1_small = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    # no-filter control (idea 50's decisive control, re-run at 75% gross for comparability)
    ew_res = backtest(px, equal_weight_all(px), cost_bps=COST_BPS, freq=FREQ)
    ew_all = ew_res["returns"].loc[start:]
    ew_turn = ew_res["turnover"].loc[start:].sum() / metrics(ew_all)["Years"]

    ecount = eligible_mask(px).sum(axis=1).loc[start:]
    print("=" * 155)
    print("PREMISE - the eligible count E_t on this panel vs the two large-cap lists.")
    print(f"  E_t of {px.shape[1]} names: mean {ecount.mean():.1f}, median {ecount.median():.0f}, "
          f"min {ecount.min():.0f}, max {ecount.max():.0f}; pct 5/25/75/95 = "
          f"{ecount.quantile(.05):.0f}/{ecount.quantile(.25):.0f}/{ecount.quantile(.75):.0f}/"
          f"{ecount.quantile(.95):.0f}")
    print(f"  (universe.json: mean 37.5 of 56.  universe_broad.json: ~90 of 136.)")
    for n in (20, 30):
        print(f"  days with E_t < {n:<3}: {(ecount < n).mean():6.2%}  "
              f"-> the cash clause in arm N n={n} almost never fires here, "
              f"so N and NF should be near-identical")
    print(f"  E_t by year (mean): " +
          "  ".join(f"{y}:{v:.0f}" for y, v in ecount.groupby(ecount.index.year).mean().items()))
    print(f"  f=0.85 therefore holds ~{np.ceil(0.85*ecount).mean():.0f} names at "
          f"{GROSS/np.ceil(0.85*ecount).mean():.2%} each; n=20 holds 20 at {GROSS/20:.2%}.")
    print()

    # ---- grid
    rows, series, counts = [], {}, {}
    for arm, ps, diag in (("N", NS, False), ("N", NS_DIAG, True), ("NF", NS, False), ("F", FS, False)):
        for p in ps:
            res = backtest(px, weights(px, arm, p), cost_bps=COST_BPS, freq=FREQ)
            r = res["returns"].loc[start:]
            held = res["weights"].loc[start:]
            m = metrics(r)
            h1, h2 = half_sharpes(r)
            r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
            key = label(arm, p)
            series[key] = r
            counts[key] = (held > 0).sum(axis=1)
            rows.append(dict(variant=key, arm=arm, param=float(p), diag=diag,
                             CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                             H1=h1, H2=h2,
                             IS_Sharpe=metrics(r_is)["Sharpe"], IS_MaxDD=metrics(r_is)["MaxDD"],
                             OOS_CAGR=metrics(r_oos)["CAGR"], OOS_Sharpe=metrics(r_oos)["Sharpe"],
                             OOS_MaxDD=metrics(r_oos)["MaxDD"],
                             names=counts[key].mean(), gross=held.sum(axis=1).mean(),
                             turn=res["turnover"].loc[start:].sum() / m["Years"],
                             p4a=verdict_4a(r, v1_live), p4b=verdict_4b(r, spy, r_oos, spy_oos),
                             fail4b=fail_4b(r, spy, r_oos, spy_oos)))
    grid = pd.DataFrame(rows).set_index("variant")

    ref = {}
    for nm, r in (("RULES v1 (universe.json, LIVE)", v1_live), ("RULES v1 (small panel)", v1_small),
                  ("EW all 439, no filter", ew_all), ("SPY", spy)):
        m = metrics(r)
        h1, h2 = half_sharpes(r)
        m_oos = metrics(r.loc[OOS_START:])
        ref[nm] = dict(arm="-", param=np.nan, diag=False, CAGR=m["CAGR"], Vol=m["Vol"],
                       Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                       IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                       IS_MaxDD=metrics(r.loc[:IS_END])["MaxDD"],
                       OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"], OOS_MaxDD=m_oos["MaxDD"],
                       names=np.nan, gross=np.nan, turn=np.nan, p4a=False,
                       p4b=verdict_4b(r, spy, r.loc[OOS_START:], spy_oos), fail4b="-")
    full = pd.concat([grid, pd.DataFrame(ref).T.rename_axis("variant")])
    show = ["CAGR", "Vol", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe",
            "OOS_MaxDD", "names", "gross", "turn", "diag", "p4a", "p4b", "fail4b"]
    print("=" * 155)
    print(f"FULL GRID - {len(grid)} points, all reported. diag=True are the matched-size extras")
    print("(excluded from walk-forward selection). names = avg positions, turn = turnover x/yr.")
    print(fmt(full[show]))
    print()

    ms = metrics(spy)
    print(f"4b thresholds on this sample: MaxDD cap {-0.60*abs(ms['MaxDD']):.1%}, CAGR floor "
          f"{0.70*ms['CAGR']:.1%}, SPY halves {half_sharpes(spy)[0]:.3f}/{half_sharpes(spy)[1]:.3f}, "
          f"SPY OOS Sharpe {metrics(spy_oos)['Sharpe']:.3f}")
    print("NOTE: SPY is a large-cap benchmark and the only one in the cache; there is no IWM")
    print("column, so 4b here asks 'does this small-cap book beat SPY', not 'does it beat its")
    print("own asset class'. That makes 4b harder, and is stated rather than adjusted for.")
    print()

    # ---- THE ANSWER: the two pre-registered points, on all three universes
    print("=" * 155)
    print("PRE-REGISTERED TEST - the two 4b KEEP-candidates on this third universe.")
    print("(universe.json / universe_broad.json figures are the published idea 2 and idea 46 rows.)")
    prior = {
        "N  n=20": [("universe.json", "12.7%/1.093/-18.3%", "1.088/1.103", "PASS 4b"),
                    ("universe_broad", "  -  /0.958/-20.1%", "  -  /0.814", "FAIL 4b (H2 by 0.02)")],
        "F  f=0.85": [("universe.json", "11.3%/1.072/-16.7%", "1.092/1.058", "PASS 4b"),
                      ("universe_broad", "11.2%/1.024/-18.6%", "1.128/0.928", "PASS 4b")],
    }
    for arm, p in PRE:
        k = label(arm, p)
        r = grid.loc[k]
        print(f"\n  {k.strip()}")
        for u, a, h, v in prior[k.strip()]:
            print(f"    {u:<16} {a:<22} halves {h:<14} {v}")
        print(f"    {'SMALL PANEL':<16} {r.CAGR:.1%}/{r.Sharpe:.3f}/{r.MaxDD:.1%}".ljust(45) +
              f"halves {r.H1:.3f}/{r.H2:.3f}".ljust(21) +
              f"{'PASS 4b' if r.p4b else 'FAIL 4b (' + r.fail4b + ')'}")
        print(f"    {'':<16} OOS {r.OOS_CAGR:.1%}/{r.OOS_Sharpe:.3f}/{r.OOS_MaxDD:.1%} | "
              f"avg names {r.names:.0f} | turnover {r.turn:.1f}x/yr | "
              f"4a: {'PASS' if r.p4a else 'FAIL'}")
    print()
    print(f"  SPY on this window:            {ms['CAGR']:.1%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.1%}"
          f"  halves {half_sharpes(spy)[0]:.3f}/{half_sharpes(spy)[1]:.3f}  "
          f"OOS {metrics(spy_oos)['CAGR']:.1%}/{metrics(spy_oos)['Sharpe']:.3f}")
    mv = metrics(v1_live)
    print(f"  RULES v1 (live) this window:   {mv['CAGR']:.1%}/{mv['Sharpe']:.3f}/{mv['MaxDD']:.1%}"
          f"  halves {half_sharpes(v1_live)[0]:.3f}/{half_sharpes(v1_live)[1]:.3f}")
    me = metrics(ew_all)
    print(f"  EW all 439 (no filter):        {me['CAGR']:.1%}/{me['Sharpe']:.3f}/{me['MaxDD']:.1%}"
          f"  halves {half_sharpes(ew_all)[0]:.3f}/{half_sharpes(ew_all)[1]:.3f}"
          f"   <- what the eligibility filter must beat")
    print()

    # ---- is the filter's damage costs or timing?
    print("=" * 155)
    print("FILTER vs COSTS - f=1.00 IS 'equal-weight all ELIGIBLE'; EW-all-439 is the same book")
    print("without the 200d/vol20 filter. Re-run both at 0 bps to split the gap into trading")
    print("costs and the filter's own timing.")
    ew0 = backtest(px, equal_weight_all(px), cost_bps=0, freq=FREQ)["returns"].loc[start:]
    f1_0 = backtest(px, weights(px, "F", 1.00), cost_bps=0, freq=FREQ)["returns"].loc[start:]
    ct = pd.DataFrame({
        "EW all 439 (no filter)": [metrics(ew_all)["CAGR"], metrics(ew0)["CAGR"],
                                   metrics(ew_all)["Sharpe"], metrics(ew0)["Sharpe"], ew_turn],
        "F f=1.00 (all eligible)": [metrics(series[label('F', 1.00)])["CAGR"], metrics(f1_0)["CAGR"],
                                    metrics(series[label('F', 1.00)])["Sharpe"], metrics(f1_0)["Sharpe"],
                                    grid.loc[label('F', 1.00), "turn"]],
    }, index=["CAGR @10bps", "CAGR @0bps", "Sharpe @10bps", "Sharpe @0bps", "turnover x/yr"])
    print(fmt(ct))
    gap10 = metrics(ew_all)["CAGR"] - metrics(series[label('F', 1.00)])["CAGR"]
    gap0 = metrics(ew0)["CAGR"] - metrics(f1_0)["CAGR"]
    print(f"\n  Filter costs {gap10:.1%}/yr of CAGR at 10 bps; {gap0:.1%}/yr at 0 bps. "
          f"So {gap10-gap0:.1%}pp is turnover and {gap0:.1%}pp is the filter's own timing.")
    print()

    # ---- matched book size
    print("=" * 155)
    print("MATCHED BOOK SIZE - each F point vs the N point (incl. diagnostics) with the closest")
    print("average position count: at the same book size, does adapting the count to breadth pay?")
    n_tab = grid[(grid.arm == "N")]
    mrows = []
    for k, r in grid[grid.arm == "F"].iterrows():
        j = (n_tab.names - r.names).abs().idxmin()
        o = n_tab.loc[j]
        mrows.append(dict(F_point=k.strip(), F_names=r.names, vs=j.strip(), vs_names=o.names,
                          dSharpe=r.Sharpe - o.Sharpe, dCAGR=r.CAGR - o.CAGR,
                          dMaxDD=r.MaxDD - o.MaxDD, dOOS_Sharpe=r.OOS_Sharpe - o.OOS_Sharpe,
                          dH1=r.H1 - o.H1, dH2=r.H2 - o.H2))
    md = pd.DataFrame(mrows).set_index("F_point")
    print(fmt(md))
    print(f"\n  F beats N on Sharpe at {int((md.dSharpe > 0).sum())}/{len(md)} matched pairs "
          f"(mean dSharpe {md.dSharpe.mean():+.3f}); on OOS Sharpe at "
          f"{int((md.dOOS_Sharpe > 0).sum())}/{len(md)} (mean {md.dOOS_Sharpe.mean():+.3f}); "
          f"on CAGR at {int((md.dCAGR > 0).sum())}/{len(md)} (mean {md.dCAGR.mean():+.2%})")
    print("  (universe.json: F beat N on Sharpe at 3/8, mean -0.002.)")
    print()

    # ---- decomposition N vs NF
    print("=" * 155)
    print("DECOMPOSITION - arm N (cash when E_t < n) vs NF (always 75%). On this panel E_t < n")
    print("is rare, so a near-zero gap here CONFIRMS the cash clause was the whole N-NF story.")
    dec = pd.DataFrame({"N_Sharpe": [grid.loc[label('N', n), 'Sharpe'] for n in NS],
                        "NF_Sharpe": [grid.loc[label('NF', n), 'Sharpe'] for n in NS],
                        "N_CAGR": [grid.loc[label('N', n), 'CAGR'] for n in NS],
                        "NF_CAGR": [grid.loc[label('NF', n), 'CAGR'] for n in NS],
                        "N_gross": [grid.loc[label('N', n), 'gross'] for n in NS]},
                       index=pd.Index(NS, name="n"))
    print(fmt(dec))
    print()

    # ---- stress years
    print("=" * 155)
    print("STRESS YEARS (calendar-year total return):")
    keys = [label("N", 20), label("N", 120), label("F", 0.35), label("F", 0.85), label("F", 1.00)]
    yr = pd.DataFrame({k.strip(): (1 + series[k]).groupby(series[k].index.year).prod() - 1 for k in keys})
    yr["EW all 439"] = (1 + ew_all).groupby(ew_all.index.year).prod() - 1
    yr["RULES v1"] = (1 + v1_live).groupby(v1_live.index.year).prod() - 1
    yr["SPY"] = (1 + spy).groupby(spy.index.year).prod() - 1
    print(yr.to_string(float_format=lambda x: f"{x:+.1%}"))
    print()

    # ---- walk-forward
    print("=" * 155)
    print("WALK-FORWARD (rule 8): parameter chosen on <=2016 only, evaluated 2017-2026 untouched.")
    print("Selection pool excludes the diag=True points.")
    is_dd_cap = 0.60 * abs(metrics(spy_is)["MaxDD"])
    print(f"  In-sample SPY: Sharpe {metrics(spy_is)['Sharpe']:.3f}, MaxDD "
          f"{metrics(spy_is)['MaxDD']:.1%} -> S2 in-sample DD cap {-is_dd_cap:.1%}")
    print(f"  OOS SPY: CAGR {metrics(spy_oos)['CAGR']:.1%}, Sharpe {metrics(spy_oos)['Sharpe']:.3f}, "
          f"MaxDD {metrics(spy_oos)['MaxDD']:.1%}")
    b_oos = metrics(v1_live.loc[OOS_START:])
    print(f"  OOS RULES v1 (live): CAGR {b_oos['CAGR']:.1%}, Sharpe {b_oos['Sharpe']:.3f}, "
          f"MaxDD {b_oos['MaxDD']:.1%}")
    wf = []
    pool = grid[~grid.diag.astype(bool)]
    for arm in ("N", "NF", "F"):
        sub = pool[pool.arm == arm]
        s1 = sub.sort_values(["IS_Sharpe", "param"], ascending=[False, False]).index[0]
        ok = sub[sub.IS_MaxDD >= -is_dd_cap]
        s2 = ok.sort_values(["IS_Sharpe", "param"], ascending=[False, False]).index[0] if len(ok) else None
        for rule, p in (("S1 Sharpe", s1), ("S2 4b-aware", s2)):
            d = dict(rule=f"{arm} / {rule}",
                     pick=(p.strip() if p else "none (no IS point met the DD cap)"))
            if p:
                d.update(grid.loc[p, ["IS_Sharpe", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe",
                                      "OOS_MaxDD", "p4a", "p4b", "fail4b"]].to_dict())
            wf.append(d)
    print(pd.DataFrame(wf).set_index("rule").to_string(float_format=lambda x: f"{x:.3f}"))
    print()

    # ---- cost sensitivity on the pre-registered points
    print("=" * 155)
    print("COST / EXECUTION SENSITIVITY on the two pre-registered points (diagnostic, not tuning).")
    print("Sub-$2B names: 10 bps is optimistic. Also a 5-day execution lag instead of 1 day.")
    crows = []
    for arm, p in PRE:
        w = weights(px, arm, p)
        for c in (10, 25, 50):
            r = backtest(px, w, cost_bps=c, freq=FREQ)["returns"].loc[start:]
            m = metrics(r)
            crows.append(dict(point=label(arm, p).strip(), setting=f"{c} bps",
                              CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"]))
        r = backtest(px, w.shift(4), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        m = metrics(r)
        crows.append(dict(point=label(arm, p).strip(), setting="10 bps, +1wk lag",
                          CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"]))
    print(pd.DataFrame(crows).set_index(["point", "setting"]).to_string(
        float_format=lambda x: f"{x:.3f}"))
    print()

    # ---- leaderboard rows
    print("=" * 155)
    print("LEADERBOARD rows (selection-pool points; diagnostics marked):")
    today = pd.Timestamp("2026-09-04").date()
    b0 = metrics(v1_live)
    bh1, bh2 = half_sharpes(v1_live)
    for k, r in grid.iterrows():
        v = ("KEEP 4b" if r.p4b else ("KEEP 4a" if r.p4a else f"KILL 4a / KILL 4b ({r.fail4b})"))
        tag = " [diag]" if r.diag else ""
        print(f"| {today} | 49 {k.strip()} (small panel){tag} | {r.CAGR:.1%} | {r.Sharpe:.2f} | "
              f"{r.MaxDD:.1%} | {r.H1:.2f} / {r.H2:.2f} | {b0['Sharpe']:.2f} ({bh1:.2f}/{bh2:.2f}) "
              f"| {v} | {SCRIPT} |")
    print()
    print(f"Selection-pool points passing 4a: {int(pool.p4a.sum())} / {len(pool)}; "
          f"passing 4b: {int(pool.p4b.sum())} / {len(pool)}  "
          f"(whole grid incl. diagnostics: 4a {int(grid.p4a.sum())}/{len(grid)}, "
          f"4b {int(grid.p4b.sum())}/{len(grid)})")


if __name__ == "__main__":
    main()
