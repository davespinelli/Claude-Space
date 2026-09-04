#!/usr/bin/env python3
"""Idea 88 - "vol-cap-as-a-satellite-clause": is RULES v1's `vol20 < 0.60` an absolute number
or a percentile of the instrument's own history?

The question
------------
RULES v1 gates every instrument on `above 200d MA AND vol20 < 0.60`.  Two published results
point in opposite directions about that second clause:

  * idea 15 (crypto-sleeve, PARK) found the 0.60 cap is the ONLY lever that changes which side
    of 4b's drawdown bar a high-vol satellite lands on: `same` (cap applied to crypto) vs
    `trend` (cap waived) gave mean dMaxDD -2.9% vs -7.0%, and every sleeve 4b failure was DD;
  * idea 56 found the same cap is the LARGER destroyer of value on the sub-$2B small-cap panel
    (at n=40: no gate 0.797 Sharpe, 200d only 0.693, vol20 only 0.524, both 0.441).

Both can be true if 0.60 is not one rule but two: it sits at a very high percentile of a
typical large-cap's own vol distribution (so it almost never binds and costs nothing) and at a
low-to-middling percentile of a small cap's or a crypto asset's (so it binds constantly and
either protects or destroys, depending on whether the excluded cohort earns).  If that is the
mechanism, then the number 0.60 carries no information of its own and RULES is really
expressing "exclude this instrument when it is unusually volatile FOR ITSELF" - which is a
percentile statement, not an absolute one.

This run tests the level directly on the satellite sleeve, at a fixed 5% cap, on both lists,
and puts the absolute and percentile expressions of the same clause side by side.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. mode in {abs, pct} - how the vol clause is written.
    2. level - abs in {0.45, 0.60, 0.80, none}; pct in {p50, p70, p90, none}, where pN means
       "vol20 below the Nth percentile of THIS instrument's own vol20 history to date"
       (expanding window, point-in-time, minimum 252 prior observations).  `none` is the same
       point under either mode (200d gate only) and is reported once, so the sweep is 7
       distinct gate specifications plus the crypto-free control.
Nothing else is tuned.  Everything below is held at its published value and never varied:
    cap                 5% per crypto name, FIXED (the queued value; idea 15 swept it)
    funding             `matched` - the sleeve is funded by scaling the equity leg down, so
                        total gross is unchanged.  Idea 15 pre-registered this as primary
                        because ideas 66/73/81 showed an unmatched gross change is an exact
                        return lever; the `add` funding is NOT run here.
    200d trend gate     always on for crypto, in every arm including `none`
    gross 0.75, weekly rebalance, 10 bps, next-day execution, 200d MA, vol20 window - RULES v1's

Books (structural, all reported, none picked on its own result) - idea 15's three
    v1      RULES v1 exactly as live: top-5 eligible by the composite WITH /sqrt(vol20), 15%.
    CAND20  idea 2's standing 4b KEEP: top-20 eligible equal-weight at 75% gross / n.
    EWall   equal-weight ALL eligible at 75% gross; the project's no-ranking control.
The equity signal, gate and ranking are computed on the crypto-free panel in every arm, so the
equity leg is bit-identical to the published books and the vol clause on the SATELLITE is the
only thing that moves.

Grid = 2 universes x 3 books x (1 control + 7 gate specs) = 48 points, ALL reported.

Secondary diagnostic (no verdict depends on it): the same abs-vs-pct question asked of the
EQUITY gate itself, on the EWall book, both lists - because the RULES wording this idea is
supposed to produce has to survive on the asset class the clause was written for, not only on
the satellite.

Verdicts (both KEEP paths, every point)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.
A point passes cross-universe 4b only if it passes on BOTH lists.

Walk-forward (PROTOCOL rule 8) is run as required and reported in full.  It is
uninformative-by-construction here for the same reason idea 15 recorded: BTC is tradeable
(200d computable) from 2015-07-02 and ETH from 2018-08-27, so rule 8's in-sample window
(<= 2016-12-31) holds ~1.5 yr of BTC and ZERO ETH, and any "selection" it makes is made on the
control's numbers.  A second walk-forward on the crypto era (IS 2018-09-01 -> 2021-12-31, OOS
2022-01-01 ->) is therefore also reported.  Neither is used to pick a headline.

Caveats carried from idea 15, none of which this run can remove
    * current-constituent survivorship on both equity lists, one-directional;
    * BTC and ETH are the two crypto SURVIVORS; LUNA, FTT and the 2014-18 altcoin field are
      absent, so every satellite number is an upper bound - and it is an upper bound in exactly
      the direction this idea tests, since a loose vol clause is what would have held the dead
      names;
    * crypto trades 24/7 on an equity-trading-day index: weekend moves land in the Monday bar,
      which understates realised drawdown and overstates the gate's tradeability;
    * 10 bps is an equity assumption; retail crypto costs more.  A cost column is reported.

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
MAX_VOL = 0.60                    # RULES v1's own number, used for the EQUITY gate everywhere
GROSS = 0.75
CAP = 0.05                        # FIXED per-name satellite cap (the queued value)
FUND = "matched"                  # FIXED funding (idea 15's pre-registered primary)
CRYPTO = ["BTC-USD", "ETH-USD"]
BOOKS = ["v1", "CAND20", "EWall"]
MIN_HIST = 252                    # prior vol20 observations before a percentile gate may fire

# the 7 gate specifications, in the order they are reported
SPECS = [("abs", 0.45), ("abs", 0.60), ("abs", 0.80),
         ("pct", 50), ("pct", 70), ("pct", 90),
         ("none", 0)]

IS_END = "2016-12-31"
OOS_START = "2017-01-01"
CRY_START = "2018-09-01"
CRY_IS_END = "2021-12-31"
CRY_OOS_START = "2022-01-01"
SCRIPT = Path(__file__).name

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 500)


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


def spec_name(mode, level):
    if mode == "none":
        return "none"
    return f"abs{level:.2f}" if mode == "abs" else f"p{level}"


# ---------------------------------------------------------------- vol clause
def vol20_of(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def vol_clause(v, mode, level):
    """Boolean DataFrame: does each instrument pass the vol clause on day t?

    abs   v_t < level                                     (RULES v1's form)
    pct   v_t <= the `level`-th percentile of that instrument's OWN v history up to and
          including t, computed on an expanding window and requiring MIN_HIST prior
          observations (before that the instrument fails the clause - conservative, and it
          cannot look ahead).
    none  always True (the 200d gate alone).
    """
    if mode == "none":
        return pd.DataFrame(True, index=v.index, columns=v.columns)
    if mode == "abs":
        return (v < level).fillna(False)
    q = v.expanding(min_periods=MIN_HIST).quantile(level / 100.0)
    return ((v <= q) & q.notna()).fillna(False)


# ---------------------------------------------------------------- book construction
def eligible_mask(px_eq):
    _, above, vol20 = score(px_eq)
    return above & (vol20 < MAX_VOL)


def equity_weights(px_eq, book, elig=None):
    if book == "v1":
        return rules_v1_weights(px_eq)
    if elig is None:
        elig = eligible_mask(px_eq)
    if book == "EWall":
        cnt = elig.sum(axis=1).replace(0, np.nan)
        return elig.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)
    if book == "CAND20":
        s = score(px_eq, vol_scale=False)[0]
        rank = s.where(elig).rank(axis=1, ascending=False)
        return (rank <= 20).astype(float) * (GROSS / 20)
    raise ValueError(book)


def crypto_gate(pxc, mode, level):
    """200d trend gate (always) AND the vol clause under test."""
    above = (pxc > pxc.rolling(200).mean()).fillna(False)
    return above & vol_clause(vol20_of(pxc), mode, level)


def combined_weights(px, px_eq, pxc, book, mode, level):
    """Full-panel weights.  mode='control' -> the published crypto-free book."""
    w_eq = equity_weights(px_eq, book).reindex(px.index).fillna(0.0)
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    w[w_eq.columns] = w_eq.values
    if mode == "control":
        return w
    wc = crypto_gate(pxc, mode, level).astype(float) * CAP
    # `matched` funding: total gross unchanged, equity leg scaled down to pay for the sleeve
    g = w_eq.sum(axis=1)
    wc_tot = wc.sum(axis=1)
    keep = wc_tot.clip(upper=g)
    scale = np.divide(keep, wc_tot.replace(0, np.nan)).fillna(0.0)
    wc = wc.mul(scale, axis=0)
    eq_scale = np.divide(g - keep, g.replace(0, np.nan)).fillna(0.0)
    w[w_eq.columns] = w_eq.mul(eq_scale, axis=0).values
    w[CRYPTO] = wc[CRYPTO].values
    return w


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


# ---------------------------------------------------------------- one universe
def run_universe(uname, px):
    px_eq = px.drop(columns=CRYPTO)
    pxc = px[CRYPTO]
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    spy_oos = spy.loc[OOS_START:]
    ms = metrics(spy)

    print("\n" + "=" * 165)
    print(f"UNIVERSE {uname}: {px_eq.shape[1]} equity names + {len(CRYPTO)} satellite, "
          f"{px.index[0].date()} -> {px.index[-1].date()}")
    print("=" * 165)
    print(f"Eval sample {start.date()} -> {px.index[-1].date()} | cap {CAP:.0%}/name FIXED, "
          f"funding '{FUND}' FIXED, {COST_BPS} bps, {FREQ} rebalance, next-day execution")
    print(f"SPY: CAGR {ms['CAGR']:.1%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.1%}  "
          f"halves {half_sharpes(spy)[0]:.3f}/{half_sharpes(spy)[1]:.3f}  "
          f"OOS Sharpe {metrics(spy_oos)['Sharpe']:.3f}")
    print(f"4b bars: Sharpe > SPY in both halves and OOS, MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, "
          f"CAGR >= {0.70*ms['CAGR']:.3%}")

    # ---------- where does 0.60 sit in each instrument's own vol distribution?
    print(f"\nWHERE 0.60 SITS IN EACH INSTRUMENT'S OWN vol20 DISTRIBUTION ({uname}) - the whole "
          f"question, before any backtest")
    vc, ve = vol20_of(pxc).loc[start:], vol20_of(px_eq).loc[start:]
    diag = []
    for t in CRYPTO:
        s = vc[t].dropna()
        diag.append(dict(instrument=t, n=len(s), med_vol=s.median(),
                         pctile_of_0p45=(s < 0.45).mean() * 100,
                         pctile_of_0p60=(s < 0.60).mean() * 100,
                         pctile_of_0p80=(s < 0.80).mean() * 100,
                         p50=s.quantile(.50), p70=s.quantile(.70), p90=s.quantile(.90)))
    eq_stats = []
    for t in [c for c in ve.columns if c != "SPY"]:
        s = ve[t].dropna()
        if len(s) < 500:
            continue
        eq_stats.append(dict(med_vol=s.median(), pctile_of_0p60=(s < 0.60).mean() * 100,
                             p50=s.quantile(.50), p70=s.quantile(.70), p90=s.quantile(.90)))
    eqs = pd.DataFrame(eq_stats)
    diag.append(dict(instrument=f"[median equity name, n={len(eqs)}]", n=int(ve.shape[0]),
                     med_vol=eqs.med_vol.median(), pctile_of_0p45=np.nan,
                     pctile_of_0p60=eqs.pctile_of_0p60.median(), pctile_of_0p80=np.nan,
                     p50=eqs.p50.median(), p70=eqs.p70.median(), p90=eqs.p90.median()))
    diag.append(dict(instrument="SPY", n=int(ve["SPY"].dropna().shape[0]),
                     med_vol=ve["SPY"].median(), pctile_of_0p45=(ve["SPY"] < 0.45).mean() * 100,
                     pctile_of_0p60=(ve["SPY"] < 0.60).mean() * 100,
                     pctile_of_0p80=(ve["SPY"] < 0.80).mean() * 100,
                     p50=ve["SPY"].quantile(.50), p70=ve["SPY"].quantile(.70),
                     p90=ve["SPY"].quantile(.90)))
    print(fmt(pd.DataFrame(diag).set_index("instrument")))
    print("  read: `pctile_of_0p60` is the share of that instrument's own vol20 days below "
          "RULES v1's cap.  If the cap were a percentile statement the column would be flat.")
    print(f"  equity names with pctile_of_0p60 == 100 (cap NEVER binds): "
          f"{int((eqs.pctile_of_0p60 >= 99.99).sum())} of {len(eqs)}; "
          f"below 90: {int((eqs.pctile_of_0p60 < 90).sum())}")

    # ---------- realised exposure of each gate spec
    print(f"\nGATE SPECIFICATION EXPOSURE ({uname}) - share of eval days each satellite is on")
    ex = []
    for mode, level in SPECS:
        gm = crypto_gate(pxc, mode, level).loc[start:]
        row = dict(spec=spec_name(mode, level), mode=mode)
        for t in CRYPTO:
            row[f"{t}_on"] = gm[t].mean()
            rg = (pxc[t].pct_change().fillna(0.0) * crypto_gate(pxc, mode, level)[t].shift(1).fillna(False)).loc[start:]
            mg = metrics(rg)
            row[f"{t}_CAGR"] = mg["CAGR"]
            row[f"{t}_Sharpe"] = mg["Sharpe"]
            row[f"{t}_MaxDD"] = mg["MaxDD"]
        row["either_on"] = gm.any(axis=1).mean()
        ex.append(row)
    print(fmt(pd.DataFrame(ex).set_index("spec")))
    print("  (*_CAGR/Sharpe/MaxDD = that satellite traded ALONE under the spec, 100% notional, "
          "no cost; a pure signal read, not a book)")

    # ---------- the grid
    rows, series = [], {}
    arms = [(b, "control", 0) for b in BOOKS] + [(b, m, l) for b in BOOKS for m, l in SPECS]
    base_v1 = None
    for book, mode, level in arms:
        w = combined_weights(px, px_eq, pxc, book, mode, level)
        res = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
        r = res["returns"].loc[start:]
        held = res["weights"].loc[start:]
        m = metrics(r)
        h1, h2 = half_sharpes(r)
        r_oos = r.loc[OOS_START:]
        key = book if mode == "control" else f"{book}/{spec_name(mode, level)}"
        series[key] = r
        if book == "v1" and mode == "control":
            base_v1 = r
        cw = held[CRYPTO].sum(axis=1)
        rows.append(dict(
            point=key, book=book, spec=("control" if mode == "control" else spec_name(mode, level)),
            mode=mode, CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
            H1=h1, H2=h2,
            OOS_CAGR=metrics(r_oos)["CAGR"], OOS_Sharpe=metrics(r_oos)["Sharpe"],
            OOS_MaxDD=metrics(r_oos)["MaxDD"],
            IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"], IS_MaxDD=metrics(r.loc[:IS_END])["MaxDD"],
            CRY_CAGR=metrics(r.loc[CRY_START:])["CAGR"], CRY_Sharpe=metrics(r.loc[CRY_START:])["Sharpe"],
            CRY_MaxDD=metrics(r.loc[CRY_START:])["MaxDD"],
            turn=res["turnover"].loc[start:].sum() / m["Years"],
            gross=held.sum(axis=1).mean(), cw_mean=cw.mean(), cw_max=cw.max()))
    df = pd.DataFrame(rows).set_index("point")
    df["p4a"] = [verdict_4a(series[k], base_v1) for k in df.index]
    df["f4b"] = [fail_4b(series[k], spy, series[k].loc[OOS_START:], spy_oos) for k in df.index]
    df["p4b"] = df["f4b"] == "-"

    mb = metrics(base_v1)
    print(f"\nRULES v1 (live book, no satellite): CAGR {mb['CAGR']:.1%}  Sharpe {mb['Sharpe']:.3f}  "
          f"MaxDD {mb['MaxDD']:.1%}  halves {half_sharpes(base_v1)[0]:.3f}/{half_sharpes(base_v1)[1]:.3f}")
    print(f"\nFULL GRID {uname} - {len(df)} points, ALL reported (f4b lists which 4b tests fail)")
    cols = ["book", "spec", "CAGR", "Vol", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
            "OOS_Sharpe", "OOS_MaxDD", "CRY_CAGR", "CRY_Sharpe", "CRY_MaxDD", "turn",
            "gross", "cw_mean", "cw_max", "p4a", "p4b", "f4b"]
    print(fmt(df[cols]))
    print(f"  4b passes: {int(df['p4b'].sum())} of {len(df)}  |  "
          f"4a passes: {int(df['p4a'].sum())} of {len(df)}")

    # ---------- each spec vs its own control
    print(f"\nEACH SPEC vs ITS OWN CONTROL ({uname}) - same book, same days, satellite is the "
          f"only difference.  t_full over the eval window, t_cry over {CRY_START}+ only.")
    hyp = []
    for book in BOOKS:
        b = series[book]
        for mode, level in SPECS:
            k = f"{book}/{spec_name(mode, level)}"
            a = series[k]
            t_, dr = paired_t(a, b)
            tc, drc = paired_t(a.loc[CRY_START:], b.loc[CRY_START:])
            ma, mbk = metrics(a), metrics(b)
            hyp.append(dict(book=book, spec=spec_name(mode, level), mode=mode,
                            dCAGR=ma["CAGR"] - mbk["CAGR"], dVol=ma["Vol"] - mbk["Vol"],
                            dMaxDD=ma["MaxDD"] - mbk["MaxDD"],
                            dSharpe=ma["Sharpe"] - mbk["Sharpe"], dRet_ann=dr, t_full=t_,
                            dSharpe_cry=metrics(a.loc[CRY_START:])["Sharpe"] - metrics(b.loc[CRY_START:])["Sharpe"],
                            dRet_cry=drc, t_cry=tc))
    hdf = pd.DataFrame(hyp)
    print(fmt(hdf.set_index(["book", "spec"]).drop(columns=["mode"])))
    print(f"\n  by SPEC (mean over the 3 books):")
    agg = hdf.groupby("spec")[["dCAGR", "dMaxDD", "dSharpe", "dSharpe_cry", "t_full", "t_cry"]].mean()
    agg["n_dSharpe_pos"] = hdf.groupby("spec").dSharpe.apply(lambda s: int((s > 0).sum()))
    print(fmt(agg.reindex([spec_name(m, l) for m, l in SPECS])))
    print(f"  by MODE: " + " | ".join(
        f"{m}: mean dSharpe {hdf[hdf['mode'] == m].dSharpe.mean():+.3f}, "
        f"mean dMaxDD {hdf[hdf['mode'] == m].dMaxDD.mean():+.2%}"
        for m in ["abs", "pct", "none"]))

    # ---------- calendar years
    print(f"\nCALENDAR YEARS ({uname}, %) - controls, the CAND20 arms, and the raw assets")
    yr = pd.DataFrame({b: series[b] for b in BOOKS})
    for mode, level in SPECS:
        yr[f"CAND20/{spec_name(mode, level)}"] = series[f"CAND20/{spec_name(mode, level)}"]
    yr["SPY"] = spy
    yr["BTC"] = pxc["BTC-USD"].pct_change().fillna(0.0).loc[start:]
    yr["ETH"] = pxc["ETH-USD"].pct_change().fillna(0.0).loc[start:]
    print(fmt(yr.groupby(yr.index.year).apply(lambda x: (1 + x).prod() - 1) * 100))

    # ---------- walk-forward
    def walk(label, is_end, oos_start):
        print(f"\nWALK-FORWARD ({uname}, {label}): chosen on <= {is_end}, evaluated on {oos_start}+")
        spy_i, spy_o = spy.loc[:is_end], spy.loc[oos_start:]
        cap_dd = 0.60 * abs(metrics(spy_i)["MaxDD"])
        so = metrics(spy_o)
        tab = pd.DataFrame({k: dict(IS_Sharpe=metrics(series[k].loc[:is_end])["Sharpe"],
                                    IS_MaxDD=metrics(series[k].loc[:is_end])["MaxDD"],
                                    OOS_CAGR=metrics(series[k].loc[oos_start:])["CAGR"],
                                    OOS_Sharpe=metrics(series[k].loc[oos_start:])["Sharpe"],
                                    OOS_MaxDD=metrics(series[k].loc[oos_start:])["MaxDD"])
                            for k in series}).T
        base_o = metrics(base_v1.loc[oos_start:])
        print(f"  OOS benchmarks: SPY {so['CAGR']:.1%}/{so['Sharpe']:.3f}/{so['MaxDD']:.1%} | "
              f"RULES v1 baseline {base_o['CAGR']:.1%}/{base_o['Sharpe']:.3f}/{base_o['MaxDD']:.1%}")
        print(f"  OOS 4b bars: Sharpe > {so['Sharpe']:.3f}, MaxDD <= {0.60*abs(so['MaxDD']):.1%}, "
              f"CAGR >= {0.70*so['CAGR']:.2%};  IS SPY Sharpe {metrics(spy_i)['Sharpe']:.3f} "
              f"MaxDD {metrics(spy_i)['MaxDD']:.1%} -> S2 admits IS MaxDD shallower than {-cap_dd:.1%}")
        print("  FULL OOS TABLE (every point):")
        print(fmt(tab.sort_values("IS_Sharpe", ascending=False)))

        def pick(cand, lab):
            if cand.empty:
                print(f"  {lab}: none qualify"); return
            p = cand.sort_values("IS_Sharpe", ascending=False).index[0]
            row = tab.loc[p]
            ok = (row.OOS_Sharpe > so["Sharpe"] and abs(row.OOS_MaxDD) <= 0.60 * abs(so["MaxDD"])
                  and row.OOS_CAGR >= 0.70 * so["CAGR"])
            print(f"  {lab}: {p:<20} -> OOS CAGR {row.OOS_CAGR:.1%}  Sharpe {row.OOS_Sharpe:.3f}  "
                  f"MaxDD {row.OOS_MaxDD:.1%}  | vs SPY dSharpe {row.OOS_Sharpe-so['Sharpe']:+.3f}, "
                  f"vs v1 baseline {row.OOS_Sharpe-base_o['Sharpe']:+.3f} | clears all OOS 4b bars? {ok}")
        pick(tab, "S1 plain-Sharpe")
        pick(tab[tab.IS_MaxDD >= -cap_dd], "S2 4b-aware   ")
        rho = tab["IS_Sharpe"].rank().corr(tab["OOS_Sharpe"].rank())
        print(f"  Spearman(IS Sharpe, OOS Sharpe) over the {len(tab)} points = {rho:+.3f}")
        # which SPEC does the in-sample rule buy, within each book?
        for book in BOOKS:
            sb = tab.loc[[i for i in tab.index if i.split("/")[0] == book]]
            best = sb.sort_values("IS_Sharpe", ascending=False).index[0]
            r2 = tab.loc[best]
            print(f"    within {book:<7} S1 picks {best:<20} -> OOS "
                  f"{r2.OOS_CAGR:.1%}/{r2.OOS_Sharpe:.3f}/{r2.OOS_MaxDD:.1%}")

    walk("PROTOCOL rule 8", IS_END, OOS_START)
    print(f"    NOTE: BTC's 200d gate is computable from 2015-07-02 and ETH's from 2018-08-27, "
          f"so rule 8's IS window (<= {IS_END}) contains ~1.5 yr of BTC and NO ETH.  Any spec it "
          f"'selects' is selected on the control's numbers, not the satellite's.")
    walk("crypto era", CRY_IS_END, CRY_OOS_START)

    df["universe"] = uname
    return df, base_v1, spy, series, start


# ---------------------------------------------------------------- equity-side diagnostic
def equity_gate_diagnostic(uname, px):
    """The same abs-vs-pct question asked of the EQUITY gate, EWall book.  No verdict."""
    px_eq = px.drop(columns=CRYPTO)
    start = px.index[260]
    spy = px_eq["SPY"].pct_change().fillna(0).loc[start:]
    _, above, v = score(px_eq)
    print(f"\nEQUITY-SIDE DIAGNOSTIC ({uname}) - EWall with the equity vol clause rewritten. "
          f"No verdict depends on this; it tests whether the percentile wording is safe on the "
          f"asset class RULES v1 was written for.")
    out = []
    for mode, level in [("none", 0), ("abs", 0.45), ("abs", 0.60), ("abs", 0.80),
                        ("pct", 50), ("pct", 70), ("pct", 90)]:
        elig = above & vol_clause(v, mode, level)
        cnt = elig.sum(axis=1).replace(0, np.nan)
        w = elig.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)
        r = backtest(px_eq, w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        m = metrics(r)
        h1, h2 = half_sharpes(r)
        out.append(dict(spec=spec_name(mode, level), mode=mode,
                        pass_rate=elig.loc[start:].sum().sum() / above.loc[start:].sum().sum(),
                        n_elig=cnt.loc[start:].mean(), CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                        MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                        f4b=fail_4b(r, spy, r.loc[OOS_START:], spy.loc[OOS_START:])))
    d = pd.DataFrame(out).set_index("spec")
    print(fmt(d))
    print("  pass_rate = share of ABOVE-200d name-days the vol clause admits (so `none` = 1.000)")
    return d


# ---------------------------------------------------------------- main
def main():
    print("=" * 165)
    print(f"Idea 88  vol-cap-as-a-satellite-clause (lane B) | {SCRIPT} | {COST_BPS} bps, "
          f"weekly, next-day execution")
    print("Question: is RULES v1's `vol20 < 0.60` an absolute number or a percentile of the "
          "instrument's own history?")
    print("=" * 165)

    px = load_universe(exclude=set())                       # BTC/ETH kept in
    pxb = load_universe(broad=True)
    assert px.index.equals(pxb.index), "broad index differs from primary; cannot join satellite"
    pxb = pd.concat([pxb.drop(columns=CRYPTO, errors="ignore"), px[CRYPTO]], axis=1)

    yrs = px.index.to_series().groupby(px.index.year).count()
    print(f"\nIndex sanity (must be ~252 rows/yr; idea 38's calendar-day bug gave 365): "
          f"2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)

    px_eq, pxc = px.drop(columns=CRYPTO), px[CRYPTO]
    start = px.index[260]
    print("\nHARNESS CHECK (must reproduce published rows before any new number is read)")
    chk = backtest(px, combined_weights(px, px_eq, pxc, "CAND20", "control", 0),
                   cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    mc = metrics(chk)
    print(f"  idea 2 KEEP row (published 12.7% / 1.093 / -18.3%, halves 1.088/1.103): "
          f"{mc['CAGR']:.1%} / {mc['Sharpe']:.3f} / {mc['MaxDD']:.1%}, "
          f"halves {half_sharpes(chk)[0]:.3f}/{half_sharpes(chk)[1]:.3f}")
    v1chk = backtest(px, combined_weights(px, px_eq, pxc, "v1", "control", 0),
                     cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    mv = metrics(v1chk)
    print(f"  live RULES v1: {mv['CAGR']:.1%} / {mv['Sharpe']:.3f} / {mv['MaxDD']:.1%}, "
          f"halves {half_sharpes(v1chk)[0]:.3f}/{half_sharpes(v1chk)[1]:.3f}")
    v1_pure = backtest(px_eq, rules_v1_weights(px_eq), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    print(f"  control equivalence |v1(full panel) - v1(crypto-free panel)| max = "
          f"{float((v1chk - v1_pure).abs().max()):.3e}  (must be 0)")
    # the abs0.60 spec must reproduce idea 15's `same` gate at c=5 exactly
    print(f"  spec `abs0.60` is idea 15's `matched/same/c5` by construction; `none` is its "
          f"`matched/trend/c5`.  Idea 15 published both as cross-universe 4b passers on EWall.")
    # no-lookahead assertion for the percentile clause
    vtest = vol20_of(pxc)
    q = vtest.expanding(min_periods=MIN_HIST).quantile(0.70)
    cut = len(vtest) // 2
    q_trunc = vtest.iloc[:cut].expanding(min_periods=MIN_HIST).quantile(0.70)
    dmax = float((q.iloc[:cut] - q_trunc).abs().max().max())
    print(f"  percentile clause look-ahead check: recomputing the expanding p70 on truncated "
          f"data changes it by at most {dmax:.3e} (must be 0)")
    assert dmax == 0.0, "percentile clause leaks future information"

    d1, b1, spy1, ser1, st1 = run_universe("universe.json", px)
    d2, b2, spy2, ser2, st2 = run_universe("universe_broad.json", pxb)

    # ---- cross-universe 4b
    print("\n" + "=" * 165)
    print("CROSS-UNIVERSE 4b (a point passes only if it passes on BOTH lists)")
    print("=" * 165)
    both = pd.DataFrame({"u56_f4b": d1["f4b"], "broad_f4b": d2["f4b"],
                         "u56_pass": d1["p4b"], "broad_pass": d2["p4b"]})
    both["cross"] = both.u56_pass & both.broad_pass
    print(fmt(both))
    winners = list(both[both.cross].index)
    print(f"  cross-universe 4b passes: {int(both['cross'].sum())} of {len(both)}")
    print(f"  passing points: {winners if winners else 'NONE'}")
    print(f"  cross-universe 4a passes: "
          f"{list((d1['p4a'] & d2['p4a'])[d1['p4a'] & d2['p4a']].index) or 'NONE'}")

    # ---- is the ordering of specs stable across universes?
    print("\nIS THE SPEC ORDERING STABLE ACROSS UNIVERSES? (Sharpe rank of the 7 specs within "
          "each book; if the clause is a real design variable the ordering should agree)")
    for book in BOOKS:
        a = d1[(d1.book == book) & (d1.spec != "control")].set_index("spec")["Sharpe"]
        b = d2[(d2.book == book) & (d2.spec != "control")].set_index("spec")["Sharpe"]
        b = b.reindex(a.index)
        print(f"  {book:<7} u56 best {a.idxmax():<8} ({a.max():.3f})  broad best {b.idxmax():<8} "
              f"({b.max():.3f})  Spearman {a.rank().corr(b.rank()):+.3f}")

    # ---- cost sensitivity, both universes, on the abs0.60 and none specs (the two RULES
    #      wordings that are actually on the table), CAND20 and EWall
    print("\nCOST SENSITIVITY (satellite arms vs their own control; 10 bps is an equity "
          "assumption and retail crypto costs more)")
    for uname, pxu in [("u56", px), ("broad", pxb)]:
        pe, pc = pxu.drop(columns=CRYPTO), pxu[CRYPTO]
        s0 = pxu.index[260]
        for book in ["CAND20", "EWall"]:
            for c in [10, 25, 50, 100]:
                line = [f"  {uname:<5} {book:<7} @ {c:>3} bps:"]
                rb = backtest(pxu, combined_weights(pxu, pe, pc, book, "control", 0),
                              cost_bps=c, freq=FREQ)["returns"].loc[s0:]
                mbb = metrics(rb)
                line.append(f"control {mbb['CAGR']:.1%}/{mbb['Sharpe']:.3f}/{mbb['MaxDD']:.1%}")
                for mode, level in [("abs", 0.60), ("pct", 70), ("none", 0)]:
                    r = backtest(pxu, combined_weights(pxu, pe, pc, book, mode, level),
                                 cost_bps=c, freq=FREQ)["returns"].loc[s0:]
                    m = metrics(r)
                    line.append(f"{spec_name(mode, level)} {m['CAGR']:.1%}/{m['Sharpe']:.3f}/"
                                f"{m['MaxDD']:.1%} (d{m['Sharpe']-mbb['Sharpe']:+.3f})")
                print(" | ".join(line))

    # ---- equity-side diagnostic
    e1 = equity_gate_diagnostic("universe.json", px)
    e2 = equity_gate_diagnostic("universe_broad.json", pxb)

    # ---- leaderboard rows
    print("\n" + "=" * 165)
    print("LEADERBOARD ROWS")
    print("=" * 165)
    for uname, d, b in [("u56", d1, b1), ("broad", d2, b2)]:
        bh1, bh2 = half_sharpes(b)
        bs = metrics(b)["Sharpe"]
        for k, row in d.iterrows():
            v = []
            if row.p4a: v.append("4a-pass")
            v.append("4b-pass" if row.p4b else f"KILL 4b ({row.f4b})")
            print(f"| 2026-09-04 | 88 {uname}/{k} | {row.CAGR:.1%} | {row.Sharpe:.2f} | "
                  f"{row.MaxDD:.1%} | {row.H1:.2f} / {row.H2:.2f} | {bs:.2f} ({bh1:.2f}/{bh2:.2f}) "
                  f"| {', '.join(v)} | {SCRIPT} |")

    stem = Path(__file__).with_suffix("").as_posix()
    pd.concat([d1, d2]).to_csv(stem + ".grid.csv")
    pd.concat([e1.assign(universe="u56"), e2.assign(universe="broad")]).to_csv(stem + ".equitygate.csv")
    print(f"\nGrids written to {Path(__file__).stem}.grid.csv and .equitygate.csv")


if __name__ == "__main__":
    main()
