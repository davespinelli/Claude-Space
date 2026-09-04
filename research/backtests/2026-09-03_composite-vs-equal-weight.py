#!/usr/bin/env python3
"""Idea 25 - "composite-vs-equal-weight": does the RULES v1 score add anything over its
own eligibility filter?

RULES v1 does two things: (1) it filters the universe down to names that are above their
200d MA and have vol20 < 0.60, and (2) it ranks those survivors by a composite score
(12-1 / 6m / 3m rank average, tilted by the 200d flag, divided by sqrt(vol20)) and buys
the top 5 at 15% each.  Step (1) is a well-known trend/vol filter.  Step (2) is the part
that claims cross-sectional skill.  This script isolates step (2).

Variants (all weekly rebalance, 10 bps, px = baseline.load_universe()):

  A  equal-weight ALL eligible names (above 200d MA AND vol20 < 0.60), 75% gross.
     Score never used - pure filter.  Same gross as the baseline, so a like-for-like
     comparison of "filter only" vs "filter + score".
  B  same as A at 100% gross (removes the cash-drag confound from the CAGR comparison).
  C  v1 top-5 by score at 75% - this IS the baseline, run as a variant so it sits in the
     same table.  Its numbers must match the baseline row exactly.
  D  BOTTOM-5 by score among eligible names, 75% gross.  This is the falsification test:
     if the score carries cross-sectional information, D must be clearly WORSE than C.
     If C and D are indistinguishable, the score is noise on top of the filter.
  E  top-5 by a single simple signal - 12-1 momentum only (px[t-21]/px[t-252] - 1) - among
     the same eligible names, 75% gross.  Tests whether the 3-factor composite beats one
     plain, untuned momentum number.

Plus the rank information coefficient: at every weekly rebalance, the Spearman correlation
across eligible names between the score at t and the subsequent 1-week and 4-week returns,
averaged over time with a t-stat.  Forward returns are measured on the actually-tradable
grid (entry at t+1's close, the day the engine applies the weights), so the IC measures the
same thing the backtest trades.  The 4-week IC series overlaps 3-deep, so a Newey-West
t-stat (lag 3) is reported alongside the naive one.

No parameter is tuned inside any variant: n=5, w=15%, the 200d and vol20<0.60 gates, and
the composite's 21/63/126/252-day lookbacks are all RULES v1's own, and the 12-1 momentum
in E is the single component already inside that composite.  The only free choice is WHICH
VARIANT, so the walk-forward (PROTOCOL rule 8) picks the best variant on 2009-2016 Sharpe
alone and reports its untouched 2017-2026 result.  OOS numbers for every variant are
printed too, for transparency.

Deterministic, standalone.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights, compare
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
FREQ = "W"
N = 5
W_TOP = 0.15           # v1 sizing: 5 x 15% = 75% gross
GROSS_75 = 0.75
GROSS_100 = 1.00
MAX_VOL = 0.60         # v1 eligibility, unchanged
IS_END = "2016-12-31"  # walk-forward: variant chosen on 2009-2016 only
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name


# ---------------------------------------------------------------- building blocks
def eligible_mask(px):
    """RULES v1's own eligibility filter: above the 200d MA and vol20 < 0.60."""
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def vol20_of(px):
    """20-day realized vol, annualized - the term the score divides by."""
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def mom_12_1(px):
    """The single simple signal: 12-month momentum skipping the last month."""
    return px.shift(21) / px.shift(252) - 1


def _equal_weight(px, gross):
    elig = eligible_mask(px).astype(float)
    n = elig.sum(axis=1)
    w = elig.div(n.where(n > 0), axis=0) * gross
    return w.fillna(0.0)


def _pick_n(sig, elig, n, w, ascending=False):
    """Top-n (or bottom-n if ascending) of `sig` among eligible names, w each."""
    e = sig.where(elig)
    rank = e.rank(axis=1, ascending=ascending)
    return (rank <= n).astype(float) * w


# ---------------------------------------------------------------- weight functions
def variant_A(px):
    """Equal-weight ALL eligible names, 75% gross. Score never used."""
    return _equal_weight(px, GROSS_75)


def variant_B(px):
    """Equal-weight ALL eligible names, 100% gross."""
    return _equal_weight(px, GROSS_100)


def variant_C(px):
    """v1 top-5 by composite score at 75% gross - the live baseline."""
    return rules_v1_weights(px, n=N, w=W_TOP, max_vol=MAX_VOL)


def variant_D(px):
    """BOTTOM-5 by composite score among eligible names, 75% gross (falsification test)."""
    s = score(px)[0]
    return _pick_n(s, eligible_mask(px), N, W_TOP, ascending=True)


def variant_E(px):
    """Top-5 by 12-1 momentum only among eligible names, 75% gross."""
    return _pick_n(mom_12_1(px), eligible_mask(px), N, W_TOP, ascending=False)


def variant_C2(px):
    """Diagnostic (not one of the five): top-5 by the composite WITHOUT the /sqrt(vol20)
    division, 75% gross.  Isolates the vol-scaling term as the difference vs C."""
    s = score(px, vol_scale=False)[0]
    return _pick_n(s, eligible_mask(px), N, W_TOP, ascending=False)


VARIANTS = [
    ("A equal-weight all eligible 75% gross", variant_A),
    ("B equal-weight all eligible 100% gross", variant_B),
    ("C v1 top-5 by score 75% (= baseline)", variant_C),
    ("D BOTTOM-5 by score 75%", variant_D),
    ("E top-5 by 12-1 momentum only 75%", variant_E),
    ("C2 top-5 by composite, no vol-scaling (diagnostic)", variant_C2),
]
# The walk-forward chooses among the four briefed alternatives; C is the incumbent and C2 a
# diagnostic, so neither is a selection candidate.
CANDIDATES = [n for n, _ in VARIANTS if n[0] in "ABDE" and not n.startswith("C")]


# ---------------------------------------------------------------- information coefficient
def trade_grid(px, start):
    """Prices on the grid the engine actually trades: the close AFTER each weekly rebalance.

    rebalance_mask marks the last trading day of each week (decision date t); engine.backtest
    shifts weights by one day, so the position is entered at the close of t+1.  Returning the
    t+1 closes indexed by the decision date t lets us line a signal known at t up against the
    return it actually earns.
    """
    mask = rebalance_mask(px.index, FREQ)
    pos = np.flatnonzero(mask.values)
    pos = pos[(pos + 1) < len(px.index)]
    dec = px.index[pos]                       # decision dates t
    entry = px.iloc[pos + 1]                  # closes at t+1
    entry.index = dec
    keep = dec >= start
    return entry.loc[keep], dec[keep]


def spearman(a, b):
    """Spearman rank correlation of two aligned Series (no scipy in this venv)."""
    ra, rb = a.rank(), b.rank()
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return ra.corr(rb)


def ic_series(sig, px, start, horizons=(1, 4)):
    """Spearman rank correlation, per rebalance date, between sig(t) and forward returns.

    Correlations are computed across ELIGIBLE names only (sig is passed already masked).
    Returns {horizon: Series of per-date IC}.
    """
    entry, dec = trade_grid(px, start)
    s = sig.loc[dec]
    out = {}
    for h in horizons:
        fwd = entry.shift(-h) / entry - 1
        ics = []
        for d in dec:
            a, b = s.loc[d], fwd.loc[d]
            both = a.notna() & b.notna()
            if both.sum() >= 5:               # need a meaningful cross-section
                ics.append((d, spearman(a[both], b[both])))
        out[h] = pd.Series(dict(ics)).dropna()
    return out


def nw_tstat(x, lag):
    """Newey-West t-stat for the mean of an overlapping series."""
    x = np.asarray(x, float)
    n = len(x)
    if n < 3:
        return np.nan
    d = x - x.mean()
    var = (d @ d) / n
    for L in range(1, lag + 1):
        c = (d[L:] @ d[:-L]) / n
        var += 2 * (1 - L / (lag + 1)) * c
    if var <= 0:
        return np.nan
    return x.mean() / np.sqrt(var / n)


def ic_table(px, start):
    elig = eligible_mask(px)
    s_comp = score(px)[0].where(elig)
    signals = {
        "v1 composite score (as traded)": s_comp,
        "  composite before vol-scaling": score(px, vol_scale=False)[0].where(elig),
        "  12-1 momentum only": mom_12_1(px).where(elig),
        "  1/sqrt(vol20) only (the scaler)": (1.0 / vol20_of(px).clip(lower=0.08) ** 0.5).where(elig),
    }
    rows = []
    for name, sig in signals.items():
        ics = ic_series(sig, px, start)
        for h, ser in ics.items():
            lag = max(h - 1, 0)
            rows.append(dict(signal=name, horizon=f"{h}w", n_weeks=len(ser),
                             mean_IC=ser.mean(), std_IC=ser.std(),
                             t_stat=ser.mean() / (ser.std() / np.sqrt(len(ser))),
                             t_NW=nw_tstat(ser, lag) if lag else np.nan,
                             pct_pos=(ser > 0).mean()))
    return pd.DataFrame(rows).set_index(["signal", "horizon"])


# ---------------------------------------------------------------- helpers
def m_row(name, r):
    m = metrics(r)
    return dict(name=name, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def main():
    px = load_universe()
    start = px.index[260]                     # same warm-up skip compare() uses
    print(f"Universe: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}")
    print(f"Eval sample starts {start.date()}  |  IS <= {IS_END}, OOS >= {OOS_START}")
    elig = eligible_mask(px).loc[start:]
    nel = elig.sum(axis=1)
    print(f"Eligible names per day: mean {nel.mean():.1f}, median {nel.median():.0f}, "
          f"min {nel.min():.0f}, max {nel.max():.0f}, zero on {(nel == 0).mean():.2%} of days\n")

    # ---- full-sample leaderboard rows via the standard compare()
    rets, rows = {}, []
    for name, fn in VARIANTS:
        print("=" * 92)
        print(f"### {name}")
        out = compare(name, fn, px, freq=FREQ, cost_bps=COST_BPS)
        # compare() puts the idea name in the last column; PROTOCOL wants the script filename
        rows.append(out["row"].rsplit("|", 2)[0] + f"| {SCRIPT} |")
        res = backtest(px, fn(px), cost_bps=COST_BPS, freq=FREQ)
        rets[name] = res["returns"].loc[start:]
        w = fn(px).loc[start:]
        held = (w > 0).sum(axis=1)
        v20 = vol20_of(px).loc[start:]
        hv = (v20 * (w > 0)).sum(axis=1) / held.replace(0, np.nan)
        print(f"Avg gross exposure: {w.sum(axis=1).mean():.1%}  |  avg names held: {held.mean():.1f}  "
              f"|  avg vol20 of held names: {hv.mean():.1%}  "
              f"|  turnover {res['turnover'].loc[start:].sum() / metrics(rets[name])['Years']:.1f}x/yr")
        print()

    base = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    rets["RULES v1 baseline"] = base
    rets["SPY"] = spy

    print("=" * 92)
    print("LEADERBOARD rows (full sample)")
    for r in rows:
        print(r)
    print()

    # ---- full sample + both halves, all variants vs baseline and SPY
    order = [n for n, _ in VARIANTS] + ["RULES v1 baseline", "SPY"]
    tbl = []
    for n in order:
        r = rets[n]
        m = metrics(r)
        h1, h2 = half_sharpes(r)
        tbl.append(dict(name=n, CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                        H1=h1, H2=h2, corr_base=r.corr(base), corr_spy=r.corr(spy)))
    full = pd.DataFrame(tbl).set_index("name")
    print("Full sample + halves (Sharpe H1/H2), correlations to baseline and SPY")
    print(full.to_string(float_format=lambda x: f"{x:.3f}"))
    print()

    # ---- C vs D: the falsification test, stated plainly
    c, d = rets["C v1 top-5 by score 75% (= baseline)"], rets["D BOTTOM-5 by score 75%"]
    spread = c - d
    mc, md = metrics(c), metrics(d)
    tsp = spread.mean() / (spread.std() / np.sqrt(len(spread)))
    print(f"C - D (top-5 minus bottom-5, same filter, same gross):")
    print(f"  C CAGR {mc['CAGR']:.2%} Sharpe {mc['Sharpe']:.3f} MaxDD {mc['MaxDD']:.2%}")
    print(f"  D CAGR {md['CAGR']:.2%} Sharpe {md['Sharpe']:.3f} MaxDD {md['MaxDD']:.2%}")
    print(f"  long-short spread: {spread.mean() * 252:.2%}/yr, daily t-stat {tsp:.2f}, "
          f"corr(C,D) {c.corr(d):.3f}")
    a = rets["A equal-weight all eligible 75% gross"]
    print(f"  C - A (score minus filter-only, same gross): "
          f"{(c - a).mean() * 252:+.2%}/yr, Sharpe {mc['Sharpe']:.3f} vs {metrics(a)['Sharpe']:.3f}, "
          f"t-stat {(c - a).mean() / ((c - a).std() / np.sqrt(len(c))):.2f}\n")

    # ---- rank information coefficient
    print("=" * 92)
    print("Rank information coefficient (Spearman, across eligible names, per weekly rebalance)")
    ic = ic_table(px, start)
    print(ic.to_string(float_format=lambda x: f"{x:.4f}"))
    print("(t_NW = Newey-West t-stat, lag h-1, for the overlapping 4-week series)\n")

    # ---- walk-forward (PROTOCOL rule 8)
    print("=" * 92)
    wf = []
    for n in order:
        r = rets[n]
        mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
        wf.append(dict(name=n, IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                       OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    wfd = pd.DataFrame(wf).set_index("name")
    print("Walk-forward: IS 2009-2016 (selection) | OOS 2017-2026 (untouched)")
    print(wfd.to_string(float_format=lambda x: f"{x:.3f}"))

    pick = max(CANDIDATES, key=lambda n: metrics(rets[n].loc[:IS_END])["Sharpe"])
    print(f"\nBest variant on 2009-2016 Sharpe alone: {pick}")
    for n in (pick, "RULES v1 baseline", "SPY"):
        mo = metrics(rets[n].loc[OOS_START:])
        print(f"  OOS {n:40s} CAGR {mo['CAGR']:7.1%}  Sharpe {mo['Sharpe']:5.2f}  MaxDD {mo['MaxDD']:7.1%}")

    # IC split IS/OOS for the traded score, since that is the claim under test
    print("\nIC of the v1 composite, split IS/OOS:")
    s_comp = score(px)[0].where(eligible_mask(px))
    ics = ic_series(s_comp, px, start)
    for h, ser in ics.items():
        i, o = ser.loc[:IS_END], ser.loc[OOS_START:]
        for lbl, x in (("IS 2009-2016", i), ("OOS 2017-2026", o)):
            print(f"  {h}w {lbl:14s} n={len(x):4d} mean IC {x.mean():+.4f}  "
                  f"t {x.mean() / (x.std() / np.sqrt(len(x))):+.2f}")


if __name__ == "__main__":
    main()
