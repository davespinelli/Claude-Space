#!/usr/bin/env python3
"""Idea 46 - "eligible-fraction-vs-n": should the book hold a FIXED COUNT or a FIXED
FRACTION of whatever is eligible that day?

The question
------------
Idea 2 (lane A, 2026-09-04) produced the project's first 4b KEEP-candidate: the top **20**
eligible names, equal-weight at 75% gross, ranked by the v1 composite WITHOUT the
`/sqrt(vol20)` term.  Its own memo flags that the universe averages ~37.5 eligible names a
day but the count swings hard - on the worst days only a handful of names are above their
200d MA.  A fixed n=20 rule therefore does two different things depending on the regime:

  * broad market (50 eligible): it holds the top 40% - a genuine selection.
  * narrow market (12 eligible): it holds 20 of 12, i.e. EVERYTHING that qualifies, and
    because the memo's rule keeps w = 0.75/20 = 3.75% fixed, the book also de-grosses to
    12 x 3.75% = 45% invested.  The selection has silently switched off and an unintended
    exposure lever has switched on.

A fixed-FRACTION rule (hold the top f x E_t names, where E_t is the eligible count that day)
keeps the selection intensity constant and the gross constant, and lets the position count
adapt.  Which is the right rule?  That is the whole idea, and it matters for the RULES
wording the Sunday review is being asked to adopt.

Arms (structural variants, not tuned choices - all reported, none selected on its own result)
--------------------------------------------------------------------------------------------
  N   FIXED-N, memo convention:  hold top n eligible at w = 0.75/n each.  When fewer than n
      are eligible the book holds all of them and the rest goes to cash (gross < 75%).
      This is exactly the KEEP-candidate's construction.
  NF  FIXED-N, gross renormalised: hold top min(n, E_t) at w = 0.75/min(n, E_t).  Always
      75% invested.  This arm exists ONLY to split arm N's behaviour into its two parts, so
      that any N-vs-F difference can be attributed to the adaptive count or to the cash
      sleeve rather than confounded between them.
  F   FIXED-FRACTION: hold the top ceil(f x E_t) eligible at w = 0.75/ceil(f x E_t).  Always
      75% invested, count adapts daily.  f = 1.00 is idea 28's "equal-weight all eligible".

Tuned parameters (PROTOCOL rule 4: at most two)
    arm N / NF: n only.      arm F: f only.
Everything else is RULES v1's own and held fixed: the 200d-MA + vol20 < 0.60 eligibility
filter, the 21-63-126-252d composite lookbacks, 75% gross, weekly rebalance, 10 bps cost,
next-day execution.  The scorer is fixed at OFF (no `/sqrt(vol20)`), the KEEP-candidate's
own scorer; lane A established that the ON arm fails 4b's CAGR floor at every n, so re-running
it here would add 8 points that cannot change the answer.

Grid = 8 n-values x 2 count arms + 8 f-values = 24 points, ALL reported.

Walk-forward (PROTOCOL rule 8) - selection rules fixed before any OOS number is read
------------------------------------------------------------------------------------
Parameters chosen on 2009-2016 ONLY, evaluated untouched on 2017-2026.
    S1 (Sharpe):    within each arm, the parameter with the highest in-sample Sharpe;
                    ties -> the more diversified (larger n / larger f).
    S2 (4b-aware):  the same, restricted to points whose in-sample MaxDD is within 60% of
                    SPY's in-sample MaxDD.  "none" if no point qualifies.
Both rules are reported for all three arms and the OOS column of all 24 points is printed,
so the selection can be audited rather than trusted.

Verdicts (both KEEP paths evaluated for every point)
    4a (beat the book):   Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b (capital-worthy):  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of
                          SPY's, CAGR >= 70% of SPY's.

Data: data/prices.csv on the corrected trading-day index; verified in-script (aborts if the
calendar-day bug of CHANGELOG 2026-09-04 is present).
Survivorship caveat: research/universe.json is a current-constituent list of 56 names, so
absolute CAGRs are optimistic.  This bites harder on the high-f / high-n points, which hold
most of a hand-picked winner list; the N-vs-F comparison is the durable part.

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
MAX_VOL = 0.60           # v1 eligibility, unchanged
GROSS = 0.75             # v1's live gross, FIXED
VOL_SCALE = False        # the KEEP-candidate's scorer: no /sqrt(vol20)
NS = [5, 8, 10, 12, 15, 20, 25, 30]
FS = [0.15, 0.25, 0.35, 0.45, 0.55, 0.70, 0.85, 1.00]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 120)


# ---------------------------------------------------------------- book construction
def eligible_mask(px):
    """RULES v1's own eligibility filter: above the 200d MA and vol20 < 0.60."""
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def _ranked(px):
    elig = eligible_mask(px)
    s = score(px, vol_scale=VOL_SCALE)[0].where(elig)
    return s.rank(axis=1, ascending=False), elig.sum(axis=1)


def weights(px, arm, p):
    """arm 'N'  -> top p eligible at 0.75/p each (gross falls to cash when E_t < p)
       arm 'NF' -> top min(p, E_t) at 0.75/min(p, E_t)   (always 75% gross)
       arm 'F'  -> top ceil(p * E_t) at 0.75/ceil(p * E_t) (always 75% gross)"""
    rank, ecount = _ranked(px)
    if arm == "N":
        k = pd.Series(float(p), index=px.index)
        w_per = GROSS / k
    else:
        if arm == "NF":
            k = np.minimum(float(p), ecount.astype(float))
        else:
            k = np.ceil(float(p) * ecount.astype(float))
        k = k.clip(lower=1.0)
        w_per = GROSS / k
    sel = rank.le(k, axis=0)
    return sel.astype(float).mul(w_per, axis=0)


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
    t = _tests_4b(r, spy, r_oos, spy_oos)
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


def label(arm, p):
    return f"{arm:<2} {'n=' + str(p) if arm != 'F' else 'f=' + format(p, '.2f'):<7}"


def run_arm(px, arm, p, start, spy_oos_dummy=None):
    res = backtest(px, weights(px, arm, p), cost_bps=COST_BPS, freq=FREQ)
    r = res["returns"].loc[start:]
    held = res["weights"].loc[start:]
    return r, res["turnover"].loc[start:], held


# ---------------------------------------------------------------- main
def main():
    px = load_universe()
    yrs = px.index.to_series().groupby(px.index.year).count()
    print("=" * 155)
    print(f"Idea 46 eligible-fraction-vs-n (lane B) | {SCRIPT}")
    print("=" * 155)
    print(f"Universe: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}")
    print(f"Index sanity (must be ~252 rows/yr; the calendar-day bug gave 365): "
          f"2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - results below are not comparable. Aborting.")
        sys.exit(1)

    start = px.index[260]                      # same warm-up skip baseline.compare() uses
    print(f"Eval sample: {start.date()} -> {px.index[-1].date()} | IS <= {IS_END}, OOS >= {OOS_START}")
    print(f"Scorer fixed at OFF (no /sqrt(vol20)); gross fixed at {GROSS:.0%}; weekly; {COST_BPS} bps.")
    print(f"Grid: N x{len(NS)} + NF x{len(NS)} + F x{len(FS)} = {2*len(NS)+len(FS)} points, all reported.\n")

    base_v1 = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]

    # ---- the premise: how much does the eligible count actually move?
    ecount = eligible_mask(px).sum(axis=1).loc[start:]
    print("=" * 155)
    print("PREMISE - the eligible count E_t, which is what a fixed-fraction rule adapts to.")
    print(f"  E_t of {px.shape[1]} names: mean {ecount.mean():.1f}, median {ecount.median():.0f}, "
          f"min {ecount.min():.0f}, max {ecount.max():.0f}; "
          f"pct 5/10/25/75/95 = {ecount.quantile(.05):.0f}/{ecount.quantile(.10):.0f}/"
          f"{ecount.quantile(.25):.0f}/{ecount.quantile(.75):.0f}/{ecount.quantile(.95):.0f}")
    for n in (10, 20, 30):
        print(f"  days with E_t < {n:<2}: {(ecount < n).mean():6.1%}   "
              f"-> arm N n={n} holds everything and de-grosses to <{GROSS*ecount[ecount<n].mean()/n:.0%} on those days"
              if (ecount < n).any() else f"  days with E_t < {n}: 0%")
    print(f"  E_t by year (mean): " +
          "  ".join(f"{y}:{v:.0f}" for y, v in ecount.groupby(ecount.index.year).mean().items()))
    print()

    # ---- run the grid
    rows, series, counts = [], {}, {}
    for arm, ps in (("N", NS), ("NF", NS), ("F", FS)):
        for p in ps:
            r, to, held = run_arm(px, arm, p, start)
            m = metrics(r)
            h1, h2 = half_sharpes(r)
            r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
            m_is, m_oos = metrics(r_is), metrics(r_oos)
            key = label(arm, p)
            series[key] = r
            counts[key] = (held > 0).sum(axis=1)
            rows.append(dict(variant=key, arm=arm, param=p,
                             CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                             H1=h1, H2=h2,
                             IS_Sharpe=m_is["Sharpe"], IS_MaxDD=m_is["MaxDD"],
                             OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"],
                             OOS_MaxDD=m_oos["MaxDD"],
                             names=counts[key].mean(),
                             gross=held.sum(axis=1).mean(),
                             turn=to.sum() / m["Years"],
                             p4a=verdict_4a(r, base_v1), p4b=verdict_4b(r, spy, r_oos, spy_oos),
                             fail4b=fail_4b(r, spy, r_oos, spy_oos)))
    grid = pd.DataFrame(rows).set_index("variant")

    ref = {}
    for nm, r in (("RULES v1 baseline", base_v1), ("SPY", spy)):
        m = metrics(r)
        h1, h2 = half_sharpes(r)
        m_oos = metrics(r.loc[OOS_START:])
        ref[nm] = dict(arm="-", param=np.nan, CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"],
                       MaxDD=m["MaxDD"], H1=h1, H2=h2,
                       IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                       IS_MaxDD=metrics(r.loc[:IS_END])["MaxDD"],
                       OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"], OOS_MaxDD=m_oos["MaxDD"],
                       names=np.nan, gross=np.nan, turn=np.nan, p4a=False, p4b=False, fail4b="-")
    full = pd.concat([grid, pd.DataFrame(ref).T.rename_axis("variant")])

    show = ["CAGR", "Vol", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_MaxDD",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "names", "gross", "turn", "p4a", "p4b", "fail4b"]
    print("=" * 155)
    print("FULL GRID - all 24 points. names = avg positions held, gross = avg invested fraction,")
    print("turn = turnover x/yr, fail4b = which of 4b's five tests fail.")
    print(fmt(full[show]))
    print()

    m_spy = metrics(spy)
    print(f"4b thresholds on this sample: MaxDD cap {-0.60*abs(m_spy['MaxDD']):.1%}, "
          f"CAGR floor {0.70*m_spy['CAGR']:.1%}, SPY halves {half_sharpes(spy)[0]:.3f} / "
          f"{half_sharpes(spy)[1]:.3f}, SPY OOS Sharpe {metrics(spy_oos)['Sharpe']:.3f}")
    print(f"RULES v1 baseline: {metrics(base_v1)['CAGR']:.1%} / {metrics(base_v1)['Sharpe']:.3f} / "
          f"{metrics(base_v1)['MaxDD']:.1%}, halves {half_sharpes(base_v1)[0]:.3f}/{half_sharpes(base_v1)[1]:.3f}")
    print()

    # ---- THE COMPARISON THE IDEA ASKS FOR: matched average book size
    print("=" * 155)
    print("MATCHED BOOK SIZE - each fixed-fraction point against the fixed-n point with the")
    print("closest average position count. This is the idea's actual test: at the same average")
    print("book size, does letting the count adapt to breadth beat pinning it?")
    n_tab = grid[grid.arm == "N"]
    nf_tab = grid[grid.arm == "NF"]
    mrows = []
    for k, r in grid[grid.arm == "F"].iterrows():
        for other, tag in ((n_tab, "N"), (nf_tab, "NF")):
            j = (other.names - r.names).abs().idxmin()
            o = other.loc[j]
            mrows.append(dict(F_point=k.strip(), F_names=r.names, vs=j.strip(), vs_names=o.names,
                              dSharpe=r.Sharpe - o.Sharpe, dCAGR=r.CAGR - o.CAGR,
                              dMaxDD=r.MaxDD - o.MaxDD, dOOS_Sharpe=r.OOS_Sharpe - o.OOS_Sharpe,
                              dH1=r.H1 - o.H1, dH2=r.H2 - o.H2, arm=tag))
    md = pd.DataFrame(mrows).set_index(["arm", "F_point"])
    print(fmt(md))
    print()
    for tag in ("N", "NF"):
        sub = md.loc[tag]
        print(f"  F beats {tag} on Sharpe at {int((sub.dSharpe > 0).sum())}/{len(sub)} matched pairs "
              f"(mean dSharpe {sub.dSharpe.mean():+.3f}); on OOS Sharpe at "
              f"{int((sub.dOOS_Sharpe > 0).sum())}/{len(sub)} (mean {sub.dOOS_Sharpe.mean():+.3f}); "
              f"on CAGR at {int((sub.dCAGR > 0).sum())}/{len(sub)} (mean {sub.dCAGR.mean():+.2%})")
    print()

    # ---- decomposition: is arm N's cash sleeve doing work?
    print("=" * 155)
    print("DECOMPOSITION - arm N (de-grosses when E_t < n) vs arm NF (same count cap, always 75%).")
    print("Any N-NF gap is the unintended cash sleeve, not the position count.")
    dec = pd.DataFrame({
        "N_Sharpe": [grid.loc[label('N', n), 'Sharpe'] for n in NS],
        "NF_Sharpe": [grid.loc[label('NF', n), 'Sharpe'] for n in NS],
        "N_CAGR": [grid.loc[label('N', n), 'CAGR'] for n in NS],
        "NF_CAGR": [grid.loc[label('NF', n), 'CAGR'] for n in NS],
        "N_MaxDD": [grid.loc[label('N', n), 'MaxDD'] for n in NS],
        "NF_MaxDD": [grid.loc[label('NF', n), 'MaxDD'] for n in NS],
        "N_gross": [grid.loc[label('N', n), 'gross'] for n in NS],
    }, index=pd.Index(NS, name="n"))
    print(fmt(dec))
    print()

    # ---- how many names does each F point actually hold, and when?
    print("=" * 155)
    print("ADAPTIVITY - position count held by each rule, by market breadth quintile of E_t.")
    q = pd.qcut(ecount, 5, labels=["E1 narrowest", "E2", "E3", "E4", "E5 broadest"])
    keys = [label("N", 20), label("NF", 20), label("F", 0.45), label("F", 0.55), label("F", 1.00)]
    adapt = pd.DataFrame({k: counts[k].groupby(q, observed=False).mean() for k in keys})
    adapt["E_t mean"] = ecount.groupby(q, observed=False).mean()
    print(fmt(adapt))
    print()

    # ---- matched-vol diagnostic (lane A's, repeated so the two runs are comparable)
    print("=" * 155)
    print("MATCHED-VOL DIAGNOSTIC - every book scaled by a constant to 12% full-sample vol.")
    print("(Uses full-sample vol, so this is a diagnostic, not a tradable rule.)")
    for arm, ps in (("N", NS), ("NF", NS), ("F", FS)):
        out = []
        for p in ps:
            r = series[label(arm, p)]
            m = metrics(r * (0.12 / metrics(r)["Vol"]))
            out.append(f"{('n=' + str(p)) if arm != 'F' else ('f=%.2f' % p)}:{m['CAGR']:.1%}/{m['MaxDD']:.0%}")
        print(f"  {arm:<2} CAGR at 12% vol / MaxDD -> " + "  ".join(out))
    m = metrics(spy * (0.12 / metrics(spy)["Vol"]))
    print(f"  SPY at 12% vol: {m['CAGR']:.1%} / {m['MaxDD']:.0%}")
    print()

    # ---- stress years
    print("=" * 155)
    print("STRESS YEARS (calendar-year total return):")
    keys = [label("N", 20), label("NF", 20), label("F", 0.35), label("F", 0.45),
            label("F", 0.55), label("F", 1.00)]
    yr = pd.DataFrame({k.strip(): (1 + series[k]).groupby(series[k].index.year).prod() - 1 for k in keys})
    yr["RULES v1"] = (1 + base_v1).groupby(base_v1.index.year).prod() - 1
    yr["SPY"] = (1 + spy).groupby(spy.index.year).prod() - 1
    print(yr.to_string(float_format=lambda x: f"{x:+.1%}"))
    print()

    # ---- walk-forward, PROTOCOL rule 8
    print("=" * 155)
    print("WALK-FORWARD (rule 8): parameter chosen on 2009-2016 only, evaluated 2017-2026 untouched.")
    is_dd_cap = 0.60 * abs(metrics(spy_is)["MaxDD"])
    print(f"  In-sample SPY: Sharpe {metrics(spy_is)['Sharpe']:.3f}, MaxDD "
          f"{metrics(spy_is)['MaxDD']:.1%} -> S2 in-sample DD cap {-is_dd_cap:.1%}")
    print(f"  OOS SPY: CAGR {metrics(spy_oos)['CAGR']:.1%}, Sharpe {metrics(spy_oos)['Sharpe']:.3f}, "
          f"MaxDD {metrics(spy_oos)['MaxDD']:.1%}")
    b_oos = metrics(base_v1.loc[OOS_START:])
    print(f"  OOS RULES v1: CAGR {b_oos['CAGR']:.1%}, Sharpe {b_oos['Sharpe']:.3f}, "
          f"MaxDD {b_oos['MaxDD']:.1%}")
    wf_rows = []
    for arm in ("N", "NF", "F"):
        sub = grid[grid.arm == arm]
        s1 = sub.sort_values(["IS_Sharpe", "param"], ascending=[False, False]).index[0]
        ok = sub[sub.IS_MaxDD >= -is_dd_cap]
        s2 = (ok.sort_values(["IS_Sharpe", "param"], ascending=[False, False]).index[0]
              if len(ok) else None)
        for rule, p in (("S1 Sharpe", s1), ("S2 4b-aware", s2)):
            d = dict(rule=f"{arm} / {rule}", pick=(p.strip() if p else "none (no IS point met the DD cap)"))
            if p:
                d.update(grid.loc[p, ["IS_Sharpe", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe",
                                      "OOS_MaxDD", "p4a", "p4b", "fail4b"]].to_dict())
            wf_rows.append(d)
    print(pd.DataFrame(wf_rows).set_index("rule").to_string(float_format=lambda x: f"{x:.3f}"))
    print()

    # ---- robustness: the same N-vs-F question on the broad universe (rule 9)
    # Lane A's KEEP fails 4b's H2 on this list by 0.02, so it is the sharpest available test of
    # whether a fraction rule is more portable across universes than a count rule. NOT a tuning
    # arm; nothing is selected from it.
    print("=" * 155)
    print("ROBUSTNESS - same arms on research/universe_broad.json (rule 9). Also a current-")
    print("constituent list, so this bounds the survivorship bias rather than removing it.")
    try:
        pxb = load_universe(broad=True)
        startb = pxb.index[260]
        spyb = pxb["SPY"].pct_change().fillna(0).loc[startb:]
        eb = eligible_mask(pxb).sum(axis=1).loc[startb:]
        print(f"  Broad universe: {pxb.shape[1]} tickers, sample {startb.date()} -> {pxb.index[-1].date()}; "
              f"E_t mean {eb.mean():.1f}, median {eb.median():.0f}, min {eb.min():.0f}, max {eb.max():.0f}")
        brows = []
        for arm, ps in (("N", NS + [40]), ("F", FS)):
            for p in ps:
                rb = backtest(pxb, weights(pxb, arm, p),
                              cost_bps=COST_BPS, freq=FREQ)["returns"].loc[startb:]
                mb = metrics(rb)
                h1, h2 = half_sharpes(rb)
                brows.append(dict(variant=label(arm, p), CAGR=mb["CAGR"], Vol=mb["Vol"],
                                  Sharpe=mb["Sharpe"], MaxDD=mb["MaxDD"], H1=h1, H2=h2,
                                  OOS_CAGR=metrics(rb.loc[OOS_START:])["CAGR"],
                                  OOS_Sharpe=metrics(rb.loc[OOS_START:])["Sharpe"],
                                  OOS_MaxDD=metrics(rb.loc[OOS_START:])["MaxDD"],
                                  p4b=verdict_4b(rb, spyb, rb.loc[OOS_START:], spyb.loc[OOS_START:]),
                                  fail4b=fail_4b(rb, spyb, rb.loc[OOS_START:], spyb.loc[OOS_START:])))
        bdf = pd.DataFrame(brows).set_index("variant")
        msb = metrics(spyb)
        bdf.loc["SPY(broad sample)"] = dict(CAGR=msb["CAGR"], Vol=msb["Vol"], Sharpe=msb["Sharpe"],
                                            MaxDD=msb["MaxDD"], H1=half_sharpes(spyb)[0],
                                            H2=half_sharpes(spyb)[1],
                                            OOS_CAGR=metrics(spyb.loc[OOS_START:])["CAGR"],
                                            OOS_Sharpe=metrics(spyb.loc[OOS_START:])["Sharpe"],
                                            OOS_MaxDD=metrics(spyb.loc[OOS_START:])["MaxDD"],
                                            p4b=False, fail4b="-")
        print(fmt(bdf))
    except Exception as e:
        print(f"  broad-universe replication unavailable: {type(e).__name__}: {e}")
    print()

    # ---- leaderboard rows
    print("=" * 155)
    print("LEADERBOARD rows (all 24 grid points):")
    today = pd.Timestamp("2026-09-04").date()
    b0 = metrics(base_v1)
    bh1, bh2 = half_sharpes(base_v1)
    for k, r in grid.iterrows():
        v = ("KEEP 4b" if r.p4b else ("KEEP 4a" if r.p4a else f"KILL 4a / KILL 4b ({r.fail4b})"))
        print(f"| {today} | 46 {k.strip()} | {r.CAGR:.1%} | {r.Sharpe:.2f} | {r.MaxDD:.1%} | "
              f"{r.H1:.2f} / {r.H2:.2f} | {b0['Sharpe']:.2f} ({bh1:.2f}/{bh2:.2f}) | {v} | {SCRIPT} |")
    print()
    print(f"Grid points passing 4a: {int(grid.p4a.sum())} / {len(grid)}; "
          f"passing 4b: {int(grid.p4b.sum())} / {len(grid)}")


if __name__ == "__main__":
    main()
