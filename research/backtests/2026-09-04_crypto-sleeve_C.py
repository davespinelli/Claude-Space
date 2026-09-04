#!/usr/bin/env python3
"""Idea 15 - "crypto-sleeve": allow BTC-USD / ETH-USD at max 10% each under v1 rules.

The question
------------
`baseline.load_universe` has excluded BTC-USD and ETH-USD from every backtest this project
has ever run (`EXCLUDE = {"BTC-USD", "ETH-USD"}`), yet both are cached in data/prices.csv and
both are trend-following instruments of exactly the kind RULES v1's 200d gate is built for.
The queued idea is to let them in as a capped sleeve and see whether the book improves.

The honest constraint, stated before any number is read
------------------------------------------------------
BTC-USD's cache starts 2014-09-17 and ETH-USD's 2017-11-09; the 200d gate makes them
tradeable only from 2015-07-02 and 2018-08-27.  The evaluation window starts 2009-01-13.
Consequences that no amount of care can remove:
  * the FIRST HALF of the evaluation window (2009-01 -> ~2017-11) is 6.5 years of no crypto
    at all followed by 2.4 years that contain BTC's 2017 bubble, so an "H1 Sharpe" for a
    sleeve arm is not comparable to an H1 Sharpe for an equity book: 74% of H1 is inherited
    from the control and the rest is one asset's largest single repricing on record.  The H1
    divergence date and the share of H1 days actually holding crypto are reported;
  * PROTOCOL rule 8's walk-forward (choose on 2009-2016, evaluate 2017-2026) has ~1.5 years
    of BTC and ZERO years of ETH in its in-sample window, so it cannot select the sleeve's
    parameters.  It is run anyway, as required, and reported as uninformative-by-construction.
A secondary walk-forward is therefore also reported on the crypto era alone (IS 2018-09-01 ->
2021-12-31, OOS 2022-01-01 -> 2026-09-03), which is the strongest test the data can support
and is still only ~3.3 years of in-sample.  Both are reported; neither is used to pick a
headline.

Books - structural variants, all reported, none picked on its own result
    v1      RULES v1 exactly as live: top 5 eligible by the composite WITH /sqrt(vol20),
            15% each.  The 4a reference.
    CAND20  idea 2's standing 4b KEEP: top-20 eligible EQUAL-WEIGHT at 75% gross / n, no vol
            scaler.  Literal `GROSS/n` construction, so it reproduces the published row
            (idea 81's de-grossing caveat applies to the control and the sleeve arms alike,
            which is why the sleeve is compared only against its own control).
    EWall   equal-weight ALL eligible names at 75% gross.  The project's no-ranking control
            and idea 10's `B136/EWall` 4b passer.
The equity signal, gate and ranking are computed on the panel WITHOUT crypto in every arm, so
the equity leg is bit-identical to the published books and the sleeve is the only change.

Funding - structural variant, both reported
    matched   total gross is held at the equity book's OWN realised gross that day: the crypto
              sleeve is funded by scaling the equity leg down.  Pre-registered as primary,
              because ideas 66/73/81 showed that any un-matched gross change is an exact
              return lever and has produced two published artefacts already.
    add       crypto weight added on top of an unchanged equity book (gross rises).  Reported
              so the gross effect can be separated from the diversification effect.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. cap c in {0%, 5%, 10%, 15%} per crypto name.  c=0% is the control; 10% is the queued
       value; 5% and 15% bracket it.  Same cap for both names - no per-asset tuning.
    2. gate g in {same, trend}.  `same` applies RULES v1's own eligibility test to crypto
       (above 200d MA AND vol20 < 0.60).  `trend` waives only the vol cap (above 200d MA
       only).  This is the crux: BTC's median vol20 is 0.532 and ETH's 0.714, so v1's 0.60
       cap is a near-binding constraint written for equities and never examined on an asset
       whose whole distribution sits on top of it.
Nothing else is tuned.  200-day MA, vol20 window, 75% gross, weekly rebalance, 10 bps and
next-day execution are RULES v1's own and are held fixed everywhere.

Grid = 2 universes x 3 books x (1 control + 2 funding x 2 gates x 3 caps) = 78 points, ALL
reported.  universe_broad.json carries no crypto columns, so BTC/ETH are joined onto it from
data/prices.csv (identical trading-day index, verified) - the broad list is used exactly as
the second universe for the standard cross-universe 4b test.

Diagnostics that do not depend on any verdict
    - standalone BTC/ETH buy-and-hold and gated-only stats over the eval window;
    - gate hit rates and the number of tradeable days each gate variant buys;
    - correlation of the crypto sleeve leg with the equity leg (the diversification claim);
    - paired daily t of sleeve vs its own control, full sample AND crypto era only;
    - calendar-year returns, with 2018 / 2022 (crypto bears) and 2020 / 2021 / 2024 called out.

Verdicts (both KEEP paths, every point)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.
A point passes cross-universe 4b only if it passes on BOTH lists.

Harness sanity: reproduces idea 2's published KEEP row (12.7% / 1.093 / -18.3%, halves
1.088/1.103) and the live RULES v1 row before any new number is reported, and asserts that
every c=0 arm is bit-identical to the crypto-free book.

Survivorship / data caveats
    * current constituents of both equity lists, one-directional, as always;
    * BTC and ETH are the two crypto survivors - the dead ones (LUNA, FTT, and the 2014-18
      altcoin field) are absent, so the sleeve is flattered in exactly the direction that
      matters.  Any positive result here is an upper bound;
    * crypto trades 24/7 but the price index is equity trading days, so weekend moves land in
      the Monday bar and a Friday-close rebalance cannot react to them.  This understates
      realised crypto drawdown and overstates the tradeability of the gate;
    * 10 bps is an equity assumption; retail crypto spreads and fees are larger.  A cost
      sensitivity column is therefore reported for the best-looking arm.

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
CRYPTO = ["BTC-USD", "ETH-USD"]
CAPS = [0.05, 0.10, 0.15]
GATES = ["same", "trend"]
FUNDS = ["matched", "add"]
BOOKS = ["v1", "CAND20", "EWall"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
CRY_START = "2018-09-01"          # both names have a computable 200d gate from here
CRY_IS_END = "2021-12-31"
CRY_OOS_START = "2022-01-01"
SCRIPT = Path(__file__).name

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 400)


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


# ---------------------------------------------------------------- book construction
def eligible_mask(px_eq):
    _, above, vol20 = score(px_eq)
    return above & (vol20 < MAX_VOL)


def equity_weights(px_eq, book):
    """The published equity book, computed on the crypto-free panel."""
    if book == "v1":
        return rules_v1_weights(px_eq)
    elig = eligible_mask(px_eq)
    if book == "EWall":
        cnt = elig.sum(axis=1).replace(0, np.nan)
        return elig.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)
    if book == "CAND20":
        s = score(px_eq, vol_scale=False)[0]
        rank = s.where(elig).rank(axis=1, ascending=False)
        return (rank <= 20).astype(float) * (GROSS / 20)
    raise ValueError(book)


def crypto_gate(pxc, gate):
    """Eligibility of each crypto name, computed on its own series."""
    above = pxc > pxc.rolling(200).mean()
    if gate == "trend":
        return above.fillna(False)
    vol20 = pxc.pct_change().rolling(20).std() * np.sqrt(252)
    return (above & (vol20 < MAX_VOL)).fillna(False)


def combined_weights(px, px_eq, pxc, book, cap, gate, fund):
    """Full-panel weights.  cap=0 -> the published book, crypto columns all zero."""
    w_eq = equity_weights(px_eq, book).reindex(px.index).fillna(0.0)
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    w[w_eq.columns] = w_eq.values
    if cap <= 0:
        return w
    wc = crypto_gate(pxc, gate).astype(float) * cap          # index x 2
    if fund == "matched":
        g = w_eq.sum(axis=1)                                 # the book's own realised gross
        wc_tot = wc.sum(axis=1)
        keep = wc_tot.clip(upper=g)                          # sleeve never adds exposure
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
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    ms = metrics(spy)

    print("\n" + "=" * 175)
    print(f"UNIVERSE {uname}: {px_eq.shape[1]} equity names + {len(CRYPTO)} crypto, "
          f"{px.index[0].date()} -> {px.index[-1].date()}")
    print("=" * 175)
    print(f"Eval sample: {start.date()} -> {px.index[-1].date()} | IS <= {IS_END}, OOS >= {OOS_START}")
    print(f"SPY: CAGR {ms['CAGR']:.1%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.1%}  "
          f"halves {half_sharpes(spy)[0]:.3f}/{half_sharpes(spy)[1]:.3f}  OOS Sharpe {metrics(spy_oos)['Sharpe']:.3f}")
    msc = metrics(spy.loc[CRY_START:])
    print(f"4b bars: Sharpe > SPY halves & OOS, MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, "
          f"CAGR >= {0.70*ms['CAGR']:.3%}")
    print(f"SPY over the crypto era ({CRY_START}+): CAGR {msc['CAGR']:.1%}  Sharpe {msc['Sharpe']:.3f}  "
          f"MaxDD {msc['MaxDD']:.1%}   -> CRY_* columns below are read against this")

    # ---- crypto diagnostics (no verdict depends on these)
    print(f"\nCRYPTO DIAGNOSTICS ({uname})")
    for t in CRYPTO:
        s = pxc[t].dropna()
        rr = pxc[t].pct_change().fillna(0.0).loc[start:]
        mb = metrics(rr)
        print(f"  {t}: cache {s.index[0].date()} -> {s.index[-1].date()} ({len(s)} bars); "
              f"buy&hold over eval window CAGR {mb['CAGR']:.1%} Sharpe {mb['Sharpe']:.3f} MaxDD {mb['MaxDD']:.1%}")
    for gate in GATES:
        gm = crypto_gate(pxc, gate).loc[start:]
        line = "  ".join(f"{t} {gm[t].mean():.1%} of days ({int(gm[t].sum())})" for t in CRYPTO)
        print(f"  gate '{gate}': eligible {line}; both-on {(gm.all(axis=1)).mean():.1%}, "
              f"either-on {(gm.any(axis=1)).mean():.1%}")
        for t in CRYPTO:
            rg = (pxc[t].pct_change().fillna(0.0) * crypto_gate(pxc, gate)[t].shift(1).fillna(False)).loc[start:]
            mg = metrics(rg)
            print(f"      gated-only {t}: CAGR {mg['CAGR']:.1%} Sharpe {mg['Sharpe']:.3f} MaxDD {mg['MaxDD']:.1%}")
    eqr = pxc.pct_change().fillna(0.0).loc[CRY_START:]
    print(f"  corr(BTC, ETH) daily since {CRY_START}: {eqr['BTC-USD'].corr(eqr['ETH-USD']):+.3f}; "
          f"corr(BTC, SPY): {eqr['BTC-USD'].corr(spy.loc[CRY_START:]):+.3f}; "
          f"corr(ETH, SPY): {eqr['ETH-USD'].corr(spy.loc[CRY_START:]):+.3f}")

    # ---- the grid
    rows, series = [], {}
    arms = [(b, 0.0, "-", "-") for b in BOOKS] + \
           [(b, c, g, f) for b in BOOKS for f in FUNDS for g in GATES for c in CAPS]
    base_v1 = None
    for book, cap, gate, fund in arms:
        w = combined_weights(px, px_eq, pxc, book, cap, gate, fund)
        res = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
        r = res["returns"].loc[start:]
        held = res["weights"].loc[start:]
        m = metrics(r)
        h1, h2 = half_sharpes(r)
        r_oos = r.loc[OOS_START:]
        key = book if cap == 0 else f"{book}/{fund}/{gate}/c{int(cap*100)}"
        series[key] = r
        if book == "v1" and cap == 0:
            base_v1 = r
        cw = held[CRYPTO].sum(axis=1)
        rows.append(dict(
            point=key, book=book, fund=fund, gate=gate, cap=cap,
            CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
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
    print(f"\nRULES v1 (live book, no crypto): CAGR {mb['CAGR']:.1%}  Sharpe {mb['Sharpe']:.3f}  "
          f"MaxDD {mb['MaxDD']:.1%}  halves {half_sharpes(base_v1)[0]:.3f}/{half_sharpes(base_v1)[1]:.3f}")

    print(f"\nFULL GRID {uname} - {len(df)} points, all reported (f4b lists which 4b tests fail)")
    cols = ["book", "fund", "gate", "cap", "CAGR", "Vol", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "CRY_CAGR", "CRY_Sharpe", "CRY_MaxDD",
            "turn", "gross", "cw_mean", "cw_max", "p4a", "p4b", "f4b"]
    print(fmt(df[cols]))
    print(f"  4b passes: {int(df['p4b'].sum())} of {len(df)}  |  4a passes: {int(df['p4a'].sum())} of {len(df)}")

    # ---- sleeve vs its own control, matched days
    print(f"\nHYPOTHESIS TEST ({uname}) - each sleeve arm vs its OWN crypto-free control, same "
          f"days/gate/signal.  dRet = annualised paired mean; t_full over the whole eval window, "
          f"t_cry over {CRY_START}+ only (the window where the sleeve can actually be on).")
    hyp = []
    for book in BOOKS:
        b = series[book]
        for fund in FUNDS:
            for gate in GATES:
                for cap in CAPS:
                    k = f"{book}/{fund}/{gate}/c{int(cap*100)}"
                    a = series[k]
                    t_, dr = paired_t(a, b)
                    tc, drc = paired_t(a.loc[CRY_START:], b.loc[CRY_START:])
                    ma, mbk = metrics(a), metrics(b)
                    hyp.append(dict(book=book, fund=fund, gate=gate, cap=cap,
                                    dCAGR=ma["CAGR"] - mbk["CAGR"], dVol=ma["Vol"] - mbk["Vol"],
                                    dMaxDD=ma["MaxDD"] - mbk["MaxDD"],
                                    dSharpe=ma["Sharpe"] - mbk["Sharpe"],
                                    dRet_ann=dr, t_full=t_,
                                    dSharpe_cry=metrics(a.loc[CRY_START:])["Sharpe"] - metrics(b.loc[CRY_START:])["Sharpe"],
                                    dRet_cry=drc, t_cry=tc))
    hdf = pd.DataFrame(hyp)
    print(fmt(hdf.set_index(["book", "fund", "gate", "cap"])))
    for fund in FUNDS:
        s = hdf[hdf.fund == fund]
        print(f"  fund={fund:<8}: dSharpe > 0 in {(s.dSharpe > 0).sum()}/{len(s)} arms (full), "
              f"{(s.dSharpe_cry > 0).sum()}/{len(s)} (crypto era); "
              f"t_full range [{s.t_full.min():+.2f}, {s.t_full.max():+.2f}], "
              f"t_cry range [{s.t_cry.min():+.2f}, {s.t_cry.max():+.2f}]")
    for gate in GATES:
        s = hdf[hdf.gate == gate]
        print(f"  gate={gate:<8}: mean dSharpe {s.dSharpe.mean():+.3f} (full), "
              f"{s.dSharpe_cry.mean():+.3f} (crypto era); mean dMaxDD {s.dMaxDD.mean():+.2%}")

    # ---- calendar years
    print(f"\nCALENDAR YEARS ({uname}, %) - controls, the queued c=10 arms on CAND20, and the assets")
    yr = pd.DataFrame({b: series[b] for b in BOOKS})
    for fund in FUNDS:
        for gate in GATES:
            yr[f"CAND20/{fund}/{gate}/c10"] = series[f"CAND20/{fund}/{gate}/c10"]
    yr["SPY"] = spy
    yr["BTC"] = pxc["BTC-USD"].pct_change().fillna(0.0).loc[start:]
    yr["ETH"] = pxc["ETH-USD"].pct_change().fillna(0.0).loc[start:]
    print(fmt(yr.groupby(yr.index.year).apply(lambda x: (1 + x).prod() - 1) * 100))

    # ---- walk-forward, PROTOCOL rule 8 (as required) then crypto era (informative)
    def walk(label, is_end, oos_start, sub):
        print(f"\nWALK-FORWARD ({uname}, {label}): chosen on <= {is_end}, evaluated on {oos_start}+")
        spy_i, spy_o = spy.loc[:is_end], spy.loc[oos_start:]
        cap_dd = 0.60 * abs(metrics(spy_i)["MaxDD"])
        so = metrics(spy_o)
        tab = pd.DataFrame({k: dict(IS_Sharpe=metrics(series[k].loc[:is_end])["Sharpe"],
                                    IS_MaxDD=metrics(series[k].loc[:is_end])["MaxDD"],
                                    OOS_CAGR=metrics(series[k].loc[oos_start:])["CAGR"],
                                    OOS_Sharpe=metrics(series[k].loc[oos_start:])["Sharpe"],
                                    OOS_MaxDD=metrics(series[k].loc[oos_start:])["MaxDD"])
                            for k in sub}).T
        print(f"  IS SPY Sharpe {metrics(spy_i)['Sharpe']:.3f} MaxDD {metrics(spy_i)['MaxDD']:.1%} "
              f"-> S2 admits IS MaxDD shallower than {-cap_dd:.1%}")
        print(f"  OOS bars: Sharpe > {so['Sharpe']:.3f}, MaxDD <= {0.60*abs(so['MaxDD']):.1%}, "
              f"CAGR >= {0.70*so['CAGR']:.2%}  (SPY OOS {so['CAGR']:.1%}/{so['Sharpe']:.3f}/{so['MaxDD']:.1%})")
        print("  In-sample table (the only numbers either rule may look at):")
        print(fmt(tab[["IS_Sharpe", "IS_MaxDD"]]))

        def pick(cand_tab, lab):
            if cand_tab.empty:
                print(f"  {lab}: none qualify"); return
            p = cand_tab.sort_values("IS_Sharpe", ascending=False).index[0]
            row = tab.loc[p]
            ok = (row.OOS_Sharpe > so["Sharpe"] and abs(row.OOS_MaxDD) <= 0.60 * abs(so["MaxDD"])
                  and row.OOS_CAGR >= 0.70 * so["CAGR"])
            print(f"  {lab}: {p:<28} -> OOS CAGR {row.OOS_CAGR:.1%}  Sharpe {row.OOS_Sharpe:.3f}  "
                  f"MaxDD {row.OOS_MaxDD:.1%}   clears all OOS 4b bars? {ok}")
        pick(tab, "S1 plain-Sharpe")
        pick(tab[tab.IS_MaxDD >= -cap_dd], "S2 4b-aware   ")
        rho = tab["IS_Sharpe"].rank().corr(tab["OOS_Sharpe"].rank())
        print(f"  Spearman(IS Sharpe, OOS Sharpe) over the {len(tab)} points = {rho:+.3f}")
        # did the IS rule buy any crypto at all?
        for book in BOOKS:
            sb = tab.loc[[i for i in tab.index if i.split("/")[0] == book]]
            best = sb.sort_values("IS_Sharpe", ascending=False).index[0]
            r2 = tab.loc[best]
            print(f"    within {book:<7} S1 picks {best:<28} -> OOS {r2.OOS_CAGR:.1%}/"
                  f"{r2.OOS_Sharpe:.3f}/{r2.OOS_MaxDD:.1%}")

    subset = list(df.index)
    walk("PROTOCOL rule 8", IS_END, OOS_START, subset)
    print(f"    NOTE: BTC is tradeable from 2015-07-02 and ETH from 2018-08-27, so the rule-8 "
          f"in-sample window (<= {IS_END}) contains ~1.5 yr of BTC and NO ETH.  Any sleeve "
          f"parameter it 'selects' is selected on the control's numbers, not the sleeve's.")
    walk("crypto era", CRY_IS_END, CRY_OOS_START, subset)

    df["universe"] = uname
    return df, base_v1, spy, series


# ---------------------------------------------------------------- main
def main():
    print("=" * 175)
    print(f"Idea 15  crypto-sleeve (lane C) | {SCRIPT} | {COST_BPS} bps, weekly, next-day execution")
    print("=" * 175)

    px = load_universe(exclude=set())                       # BTC/ETH kept in
    pxb = load_universe(broad=True)
    assert px.index.equals(pxb.index), "broad index differs from primary; cannot join crypto"
    pxb = pd.concat([pxb.drop(columns=CRYPTO, errors="ignore"), px[CRYPTO]], axis=1)

    yrs = px.index.to_series().groupby(px.index.year).count()
    print(f"Index sanity (must be ~252 rows/yr; the calendar-day bug gave 365): "
          f"2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)

    px_eq, pxc = px.drop(columns=CRYPTO), px[CRYPTO]
    start = px.index[260]
    chk = backtest(px, combined_weights(px, px_eq, pxc, "CAND20", 0.0, "-", "-"),
                   cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    mc = metrics(chk)
    print("\nHARNESS CHECK vs idea 2's published KEEP row (12.7% / 1.093 / -18.3%, halves 1.088/1.103):")
    print(f"  reproduced: {mc['CAGR']:.1%} / {mc['Sharpe']:.3f} / {mc['MaxDD']:.1%}, "
          f"halves {half_sharpes(chk)[0]:.3f}/{half_sharpes(chk)[1]:.3f}")
    v1chk = backtest(px, combined_weights(px, px_eq, pxc, "v1", 0.0, "-", "-"),
                     cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    mv = metrics(v1chk)
    print(f"  live RULES v1: {mv['CAGR']:.1%} / {mv['Sharpe']:.3f} / {mv['MaxDD']:.1%}, "
          f"halves {half_sharpes(v1chk)[0]:.3f}/{half_sharpes(v1chk)[1]:.3f}")
    v1_pure = backtest(px_eq, rules_v1_weights(px_eq), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    print(f"  c=0 equivalence |v1(full panel) - v1(crypto-free panel)| max = "
          f"{float((v1chk - v1_pure).abs().max()):.3e}  (must be 0)")

    d1, b1, spy1, ser1 = run_universe("universe.json", px)
    d2, b2, spy2, ser2 = run_universe("universe_broad.json", pxb)

    # ---- cross-universe 4b
    print("\n" + "=" * 175)
    print("CROSS-UNIVERSE 4b (a point passes only if it passes on BOTH lists)")
    print("=" * 175)
    both = pd.DataFrame({"u56_f4b": d1["f4b"], "broad_f4b": d2["f4b"],
                         "u56_pass": d1["p4b"], "broad_pass": d2["p4b"]})
    both["cross"] = both.u56_pass & both.broad_pass
    print(fmt(both))
    print(f"  cross-universe 4b passes: {int(both['cross'].sum())} of {len(both)}")
    winners = list(both[both.cross].index)
    print(f"  passing points: {winners if winners else 'NONE'}")

    # ---- H1 inheritance check: is the sleeve doing anything in H1 at all?
    print("\nH1 INHERITANCE CHECK (universe.json): how much of H1 is actually a crypto test?")
    for book in BOOKS:
        b = ser1[book]
        h = len(b) // 2
        for gate in GATES:
            k = f"{book}/matched/{gate}/c10"
            d = (ser1[k].iloc[:h] - b.iloc[:h])
            nz = d[d.abs() > 1e-12]
            frac = len(nz) / h
            first = nz.index[0].date() if len(nz) else None
            print(f"  {k:<28} H1 ends {b.index[h-1].date()}; first divergence {first}; "
                  f"{frac:.1%} of H1 days differ from the control")

    # ---- cost sensitivity on the best-looking arm, chosen by full-sample Sharpe (diagnostic only)
    print("\nCOST SENSITIVITY (universe.json, best full-sample-Sharpe sleeve arm; diagnostic only, "
          "10 bps is an equity assumption and crypto costs more)")
    sl = d1[d1.cap > 0].sort_values("Sharpe", ascending=False)
    best = sl.index[0]
    row = d1.loc[best]
    for c in [10, 25, 50, 100]:
        w = combined_weights(px, px_eq, pxc, row.book, row.cap, row.gate, row.fund)
        r = backtest(px, w, cost_bps=c, freq=FREQ)["returns"].loc[start:]
        wb = combined_weights(px, px_eq, pxc, row.book, 0.0, "-", "-")
        rb = backtest(px, wb, cost_bps=c, freq=FREQ)["returns"].loc[start:]
        m, mbb = metrics(r), metrics(rb)
        print(f"  {best} @ {c:>3} bps: CAGR {m['CAGR']:.1%} Sharpe {m['Sharpe']:.3f} MaxDD {m['MaxDD']:.1%} "
              f"| control {mbb['CAGR']:.1%}/{mbb['Sharpe']:.3f}/{mbb['MaxDD']:.1%} "
              f"| dSharpe {m['Sharpe']-mbb['Sharpe']:+.3f}")

    # ---- leaderboard rows
    print("\n" + "=" * 175)
    print("LEADERBOARD ROWS")
    print("=" * 175)
    for uname, d, b in [("u56", d1, b1), ("broad", d2, b2)]:
        bh1, bh2 = half_sharpes(b)
        bs = metrics(b)["Sharpe"]
        for k, row in d.iterrows():
            v = []
            if row.p4a: v.append("4a-pass")
            v.append("4b-pass" if row.p4b else f"KILL 4b ({row.f4b})")
            print(f"| 2026-09-04 | 15 {uname}/{k} | {row.CAGR:.1%} | {row.Sharpe:.2f} | {row.MaxDD:.1%} | "
                  f"{row.H1:.2f} / {row.H2:.2f} | {bs:.2f} ({bh1:.2f}/{bh2:.2f}) | {', '.join(v)} | {SCRIPT} |")

    pd.concat([d1, d2]).to_csv(Path(__file__).with_suffix("").as_posix() + ".grid.csv")
    print(f"\nGrid written to {Path(__file__).stem}.grid.csv")


if __name__ == "__main__":
    main()
