#!/usr/bin/env python3
"""QUEUE idea 64 — monthly-drawdown-cost (cloud, 2026-09-06).

Question
--------
Idea 3 found MONTHLY rebalancing worth +2..+4pp of CAGR (t +2.1..+2.6) in 3 of 4 books, paid for
with 3-6pp of extra MaxDD — and that extra drawdown is what breaks 4b on the broad list.  Two
parts, both queued:

  (1) LOCATE the extra drawdown in time.  Which episodes: 2020, 2022, 2025?
  (2) TEST the repair: a book that REBALANCES MONTHLY but honours its GATE ANY WEEK — i.e. a
      monthly book with a weekly EXIT-ONLY check.  Does it keep the monthly return and drop the
      monthly drawdown?

Instrument
----------
`backtest_hybrid` is `engine.backtest` with one addition: on an EXIT date that is not a rebalance
date, the book does not re-anchor to its target (that would be a full rebalance and would undo the
drift).  It only SELLS: every holding whose gate has failed goes to zero, and nothing else trades.
Turnover on such a date is therefore exactly the weight sold.  Gate 3 asserts that with the exit
mask empty this is bit-identical to `engine.backtest(freq='M')`.

Two tuned parameters, and nothing else:
  * dial 1 — EXIT-CHECK CADENCE in {none (plain monthly), W, D};
  * dial 2 — DISPOSAL of the freed weight in {cash (de-gross, RULES v2's convention),
    spread (pro-rata over the surviving holdings until the next month-end)}.
Panel (broad / u56), book (4), and cost rung (10 / 25 bps) are REPORTED at every value and never
selected on.  The plain WEEKLY book is carried as a return reference, not as an arm.

The gate honoured on an exit date is THE BOOK'S OWN gate, not a new one: `top20` and `frac85` use
RULES v1 eligibility (vol20 < 0.60 and price above the 200d MA), `ew-all` the 200d gate, and
`ew-band3` the hysteresis band — so this rule adds no information the monthly book did not
already act on, only timeliness.

Episode windows for part (1) are fixed here, in the source, before any number was read, and are
the record's standard risk episodes; per-calendar-year MaxDD is reported too, so nothing hides in
the choice of window.

Rule 8 (required): both dials chosen on 2009-2016 by IS Sharpe alone, evaluated untouched on
2017-2026 against the plain monthly parent, RULES v2 and SPY.  Pre-registered caveat (idea 111):
2017-2026 is very nearly H2 on this sample, so the OOS bar and 4b's H2 bar overlap.

SURVIVORSHIP: both panels are CURRENT constituents (research/universe.json and
research/universe_broad.json), so absolute CAGR/Sharpe are optimistic for every arm; all
comparisons are between arms on the same panel and the same days.

Outputs: `.console.txt`, `.grid.csv` (every arm x book x panel x rung), `.episodes.csv`
(part 1), `.walkforward.csv` (rule 8).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score            # noqa: E402
from engine import backtest, metrics, rebalance_mask                   # noqa: E402

GROSS, MAX_VOL, BAND = 0.75, 0.60, 0.03
END = "2026-09-03"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
RUNGS = [10, 25]
EXITS = ["none", "W", "D"]                 # tuned dial 1
DISPOSAL = ["cash", "spread"]              # tuned dial 2
OUT = Path(__file__).with_suffix("")

EPISODES = [                               # pre-registered, fixed before any number was read
    ("2010 EU/flash", "2010-04-01", "2010-09-30"),
    ("2011 EU crisis", "2011-05-01", "2011-10-31"),
    ("2015-16 China", "2015-08-01", "2016-02-29"),
    ("2018Q4", "2018-10-01", "2018-12-31"),
    ("2020 COVID", "2020-02-01", "2020-04-30"),
    ("2022 bear", "2022-01-01", "2022-10-31"),
    ("2025", "2025-01-01", "2025-12-31"),
]

_LINES = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _LINES.append(s)


# --------------------------------------------------------------- construction
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def trend(px, gate):
    ma = px.rolling(200).mean()
    if gate == "200d":
        return (px > ma).fillna(False)
    if gate == "band":
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * (1 + BAND), 1.0).mask(px < ma * (1 - BAND), 0.0)
        return raw.ffill().fillna(0.0) > 0.5
    raise ValueError(gate)


def eligible(px, gate):
    if gate == "band":
        return trend(px, "band")                       # RULES v2 has no vol filter
    return (vol20(px) < MAX_VOL) & trend(px, "200d")


def w_topn(px, n=20):
    rank = composite(px).where(eligible(px, "200d")).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


def w_frac(px, f=0.85):
    elig = eligible(px, "200d")
    s = score(px, vol_scale=False)[0].where(elig)
    rank = s.rank(axis=1, ascending=False)
    k = np.ceil(f * elig.sum(axis=1).astype(float)).clip(lower=1.0)
    return rank.le(k, axis=0).astype(float).mul(GROSS / k, axis=0)


def w_ew(px, gate):
    e = eligible(px, gate).astype(float)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * GROSS


# book -> (weights fn, gate name).  The four books idea 3 priced.
BOOKS = {
    "top20 (idea 2)":     (w_topn, "200d"),
    "frac85 (idea 46)":   (w_frac, "200d"),
    "ew-all":             (lambda px: w_ew(px, "200d"), "200d"),
    "ew-band3 (idea 57 / RULES v2 shape)": (lambda px: w_ew(px, "band"), "band"),
}


# ------------------------------------------------------------------ execution
def backtest_hybrid(prices, weights, elig, cost_bps, rmask, emask, disposal):
    """engine.backtest, plus SELL-ONLY gate exits on `emask` dates.

    On a rebalance date the target is the book's weights (identical to the engine).  On an exit
    date that is not a rebalance date, holdings whose gate has failed are sold and NOTHING else
    trades: with disposal='cash' the freed weight sits in cash until the next rebalance; with
    'spread' it is pushed pro-rata onto the surviving holdings.  Gate 3 asserts emask=empty
    reproduces engine.backtest exactly.
    """
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)      # decided t, applied t+1
    E = elig.reindex(prices.index).fillna(False).shift(1).fillna(False).astype(bool)
    rm = rmask.shift(1, fill_value=False)
    em = emask.shift(1, fill_value=False)
    held = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    cur = np.zeros(len(prices.columns))
    turnover = pd.Series(0.0, index=prices.index)
    Ev = E.values
    for i in range(len(prices.index)):
        if rm.iloc[i] or i == 0:
            new = w_target.iloc[i].values
            turnover.iloc[i] = np.abs(new - cur).sum()
            cur = new
        elif em.iloc[i]:
            keep = Ev[i]
            new = np.where(keep, cur, 0.0)
            freed = cur.sum() - new.sum()
            if disposal == "spread" and freed > 0 and new.sum() > 0:
                new = new + freed * new / new.sum()
            t = np.abs(new - cur).sum()
            if t > 0:
                turnover.iloc[i] = t
                cur = new
        held.iloc[i] = cur
        growth = cur * (1 + rets.iloc[i].values)
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    port = (held * rets).sum(axis=1) - turnover * cost_bps / 1e4
    return {"returns": port, "equity": (1 + port).cumprod(), "weights": held, "turnover": turnover}


# --------------------------------------------------------------------- verdicts
def m3(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def maxdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def dd_dates(r):
    eq = (1 + r).cumprod()
    dd = eq / eq.cummax() - 1
    tr = dd.idxmin()
    pk = eq.loc[:tr].idxmax()
    return pk.date(), tr.date()


def path4a(r, base):
    h = len(r) // 2
    bad = []
    if metrics(r.iloc[:h])["Sharpe"] <= metrics(base.iloc[:h])["Sharpe"]: bad.append("H1")
    if metrics(r.iloc[h:])["Sharpe"] <= metrics(base.iloc[h:])["Sharpe"]: bad.append("H2")
    if metrics(r)["MaxDD"] < metrics(base)["MaxDD"]: bad.append("DD")
    return bad


def path4b(r, spy, oos_s, spy_oos_s):
    h = len(r) // 2
    bad = []
    if metrics(r.iloc[:h])["Sharpe"] <= metrics(spy.iloc[:h])["Sharpe"]: bad.append("H1")
    if metrics(r.iloc[h:])["Sharpe"] <= metrics(spy.iloc[h:])["Sharpe"]: bad.append("H2")
    if oos_s <= spy_oos_s: bad.append("OOS")
    if abs(metrics(r)["MaxDD"]) > 0.60 * abs(metrics(spy)["MaxDD"]): bad.append("DD")
    if metrics(r)["CAGR"] < 0.70 * metrics(spy)["CAGR"]: bad.append("CAGR")
    return bad


def vstr(bad, tag):
    return f"KEEP {tag}" if not bad else f"KILL {tag}(" + ",".join(bad) + ")"


# ==================================================================== main
def main():
    pd.set_option("display.width", 240)
    grid, epi, wf = [], [], []

    for panel in ("broad", "u56"):
        px = (load_universe(broad=True) if panel == "broad" else load_universe()).loc[:END]
        P("\n" + "=" * 118)
        P(f"PANEL {panel} — {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}")
        P("=" * 118)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        n = len(spy); h = n // 2; yrs = n / 252.0
        oos = spy.loc[OOS_START:].index
        spy_oos_s = metrics(spy.loc[oos])["Sharpe"]
        mmask = rebalance_mask(px.index, "M")
        wmask = rebalance_mask(px.index, "W")
        dmask = rebalance_mask(px.index, "D")
        v2 = {b: backtest(px, rules_v2_weights(px), cost_bps=b, freq="W")["returns"].loc[start:]
              for b in RUNGS}

        def stats(res, bps):
            r = res["returns"].loc[start:]
            c, s, dd = m3(r)
            oc, os_, odd = m3(r.loc[oos])
            return dict(CAGR=c, Sharpe=s, MaxDD=dd, H1=metrics(r.iloc[:h])["Sharpe"],
                        H2=metrics(r.iloc[h:])["Sharpe"], IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                        OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd,
                        turn=res["turnover"].loc[start:].sum() / yrs,
                        gross=res["weights"].loc[start:].sum(axis=1).mean(), bps=bps, r=r)

        # ------------------------------------------------------- gates (once per panel)
        wt = w_topn(px)
        el = eligible(px, "200d")
        empty = pd.Series(False, index=px.index)
        g_h = backtest_hybrid(px, wt, el, 10, mmask, empty, "cash")["returns"]
        g_e = backtest(px, wt, cost_bps=10, freq="M")["returns"]
        d1 = (g_h - g_e).abs().max()
        P(f"  GATE — backtest_hybrid with an empty exit mask == engine.backtest(freq='M'): "
          f"max|dret| {d1:.3e} {'EXACT' if d1 == 0.0 else 'FAILED'}")
        assert d1 == 0.0, "hybrid backtester does not nest the engine"
        if panel == "broad":
            gotw = m3(backtest(px, wt, cost_bps=10, freq="W")["returns"].loc[start:])
            P(f"  GATE — idea 66's broad `top20-200d` WEEKLY @10bps: {gotw[0]:.2%} / {gotw[1]:.4f} / "
              f"{gotw[2]:.2%}  (published 13.1% / 0.958 / -20.1%)")
            ok = abs(gotw[0] - 0.131) <= 5e-4 and abs(gotw[1] - 0.958) <= 5e-4 and abs(gotw[2] + 0.201) <= 5e-4
            P(f"  GATE: {'3/3 EXACT' if ok else 'FAILED'}")
            assert ok, "published parent not reproduced"

        sc, ss, sdd = m3(spy)
        P(f"\n  SPY: {sc:.2%} / {ss:.3f} / {sdd:.2%}, halves {metrics(spy.iloc[:h])['Sharpe']:.3f}/"
          f"{metrics(spy.iloc[h:])['Sharpe']:.3f}, OOS {spy_oos_s:.3f}")
        P(f"  4b bars: H1 > {metrics(spy.iloc[:h])['Sharpe']:.4f}, H2 > {metrics(spy.iloc[h:])['Sharpe']:.4f}, "
          f"OOS > {spy_oos_s:.4f}, MaxDD >= {-0.60*abs(sdd):.2%}, CAGR >= {0.70*sc:.2%}")
        P(f"  RULES v2 (live, weekly) @10bps: {m3(v2[10])[0]:.2%} / {m3(v2[10])[1]:.3f} / {m3(v2[10])[2]:.2%}")

        # ------------------------------------------------------------- the grid
        P("\n  " + "-" * 114)
        P(f"  ALL ARMS — 4 books x (W ref, M, M+W-cash, M+W-spread, M+D-cash, M+D-spread) x 2 rungs")
        P("  " + "-" * 114)
        P(f"  {'book':38s} {'arm':12s} {'bps':>4s} {'gross':>6s} {'CAGR':>7s} {'Sharpe':>7s} "
          f"{'MaxDD':>8s} {'H1':>7s} {'H2':>7s} {'turn':>6s} {'OOSShrp':>8s}  verdicts")
        series = {}
        for bname, (fn, gate) in BOOKS.items():
            w = fn(px)
            el = eligible(px, gate)
            arms = [("W ref", None, None), ("M", empty, "cash"),
                    ("M+W-cash", wmask, "cash"), ("M+W-spread", wmask, "spread"),
                    ("M+D-cash", dmask, "cash"), ("M+D-spread", dmask, "spread")]
            for aname, em, disp in arms:
                for b in RUNGS:
                    if aname == "W ref":
                        res = backtest(px, w, cost_bps=b, freq="W")
                    else:
                        res = backtest_hybrid(px, w, el, b, mmask, em, disp)
                    d = stats(res, b)
                    series[(bname, aname, b)] = d
                    a4 = path4a(d["r"], v2[b])
                    b4 = path4b(d["r"], spy, d["OOS_Sharpe"], spy_oos_s)
                    P(f"  {bname:38s} {aname:12s} {b:4d} {d['gross']:6.3f} {d['CAGR']:7.2%} "
                      f"{d['Sharpe']:7.3f} {d['MaxDD']:8.2%} {d['H1']:7.3f} {d['H2']:7.3f} "
                      f"{d['turn']:6.2f} {d['OOS_Sharpe']:8.3f}  {vstr(a4,'4a')} / {vstr(b4,'4b')}")
                    grid.append(dict(panel=panel, book=bname, arm=aname, bps=b,
                                     exit_cadence={"W ref": "wref", "M": "none", "M+W-cash": "W",
                                                   "M+W-spread": "W", "M+D-cash": "D",
                                                   "M+D-spread": "D"}[aname],
                                     disposal=(disp or "n/a"),
                                     **{k: d[k] for k in ("gross", "CAGR", "Sharpe", "MaxDD", "H1",
                                                          "H2", "IS_Sharpe", "OOS_CAGR",
                                                          "OOS_Sharpe", "OOS_MaxDD", "turn")},
                                     keep4a=not a4, keep4b=not b4,
                                     fail4a=",".join(a4), fail4b=",".join(b4)))

        # ============================================= PART 1 — locate the drawdown in time
        P("\n  " + "=" * 114)
        P("  PART 1 — WHERE the monthly book's extra drawdown sits (M minus W, @10bps)")
        P("  " + "=" * 114)
        P(f"  {'book':38s} {'arm':7s} {'MaxDD':>8s}  peak -> trough           " +
          "".join(f"{e[0]:>16s}" for e in EPISODES))
        for bname in BOOKS:
            for aname in ("W ref", "M"):
                r = series[(bname, aname, 10)]["r"]
                pk, tr = dd_dates(r)
                cells = "".join(f"{maxdd(r.loc[a:b]):16.2%}" for _, a, b in EPISODES)
                P(f"  {bname:38s} {aname:7s} {maxdd(r):8.2%}  {str(pk):>10s} -> {str(tr):<10s}{cells}")
            rw = series[(bname, "W ref", 10)]["r"]
            rm = series[(bname, "M", 10)]["r"]
            cells = "".join(f"{maxdd(rm.loc[a:b]) - maxdd(rw.loc[a:b]):16.2%}" for _, a, b in EPISODES)
            P(f"  {bname:38s} {'M - W':7s} {maxdd(rm)-maxdd(rw):8.2%}  {'':>10s}    {'':<10s}{cells}")
            for nm, a, b in EPISODES:
                epi.append(dict(panel=panel, book=bname, episode=nm, start=a, end=b,
                                W_dd=maxdd(rw.loc[a:b]), M_dd=maxdd(rm.loc[a:b]),
                                MW_cash_dd=maxdd(series[(bname, "M+W-cash", 10)]["r"].loc[a:b]),
                                MW_spread_dd=maxdd(series[(bname, "M+W-spread", 10)]["r"].loc[a:b]),
                                delta_M_minus_W=maxdd(rm.loc[a:b]) - maxdd(rw.loc[a:b])))

        P("\n  per-calendar-year MaxDD, M minus W @10bps (negative = the monthly book is deeper)")
        yrsl = sorted({d.year for d in px.loc[start:].index})
        P(f"  {'book':38s}" + "".join(f"{y:>8d}" for y in yrsl))
        for bname in BOOKS:
            rw = series[(bname, "W ref", 10)]["r"]
            rm = series[(bname, "M", 10)]["r"]
            P(f"  {bname:38s}" + "".join(
                f"{maxdd(rm[rm.index.year == y]) - maxdd(rw[rw.index.year == y]):8.1%}" for y in yrsl))

        # ============================================= PART 2 — does the weekly exit repair it
        P("\n  " + "=" * 114)
        P("  PART 2 — does a WEEKLY EXIT-ONLY check keep the monthly return and drop the drawdown?")
        P("  (deltas vs the plain monthly arm of the SAME book, @10bps)")
        P("  " + "=" * 114)
        P(f"  {'book':38s} {'arm':12s} {'dCAGR':>7s} {'dSharpe':>8s} {'dMaxDD':>8s} {'dOOSShrp':>9s} "
          f"{'dturn':>7s}  {'4b M':>10s} -> {'4b arm':<14s}")
        for bname in BOOKS:
            base = series[(bname, "M", 10)]
            b4m = path4b(base["r"], spy, base["OOS_Sharpe"], spy_oos_s)
            for aname in ("M+W-cash", "M+W-spread", "M+D-cash", "M+D-spread"):
                d = series[(bname, aname, 10)]
                b4 = path4b(d["r"], spy, d["OOS_Sharpe"], spy_oos_s)
                P(f"  {bname:38s} {aname:12s} {d['CAGR']-base['CAGR']:7.2%} "
                  f"{d['Sharpe']-base['Sharpe']:+8.4f} {d['MaxDD']-base['MaxDD']:+8.2%} "
                  f"{d['OOS_Sharpe']-base['OOS_Sharpe']:+9.4f} {d['turn']-base['turn']:+7.2f}  "
                  f"{vstr(b4m,'4b'):>10s} -> {vstr(b4,'4b'):<14s}")

        # ===================================================================== rule 8
        P("\n  " + "=" * 114)
        P("  RULE 8 — both dials chosen on 2009-2016 by IS Sharpe alone, 2017-2026 untouched")
        P("  " + "=" * 114)
        gp = pd.DataFrame([g for g in grid if g["panel"] == panel])
        for b in RUNGS:
            for bname in BOOKS:
                s = gp[(gp.bps == b) & (gp.book == bname) & (gp.arm != "W ref")]
                ip = s.loc[s.IS_Sharpe.idxmax()]
                par = s[s.arm == "M"].iloc[0]
                rho = s.IS_Sharpe.rank().corr(s.OOS_Sharpe.rank())
                P(f"  @{b}bps {bname:38s} IS pick {ip['arm']:12s} (IS {ip['IS_Sharpe']:.4f} vs M's "
                  f"{par['IS_Sharpe']:.4f}); OOS {ip['OOS_CAGR']:7.2%}/{ip['OOS_Sharpe']:.3f}/"
                  f"{ip['OOS_MaxDD']:7.2%} vs M {par['OOS_CAGR']:7.2%}/{par['OOS_Sharpe']:.3f}/"
                  f"{par['OOS_MaxDD']:7.2%}; dOOS {ip['OOS_Sharpe']-par['OOS_Sharpe']:+.4f}; "
                  f"Spearman(IS,OOS over 5 arms) {rho:+.3f}")
                wf.append(dict(panel=panel, bps=b, book=bname, pick=ip["arm"],
                               IS_Sharpe=ip["IS_Sharpe"], M_IS_Sharpe=par["IS_Sharpe"],
                               OOS_CAGR=ip["OOS_CAGR"], OOS_Sharpe=ip["OOS_Sharpe"],
                               OOS_MaxDD=ip["OOS_MaxDD"], M_OOS_Sharpe=par["OOS_Sharpe"],
                               M_OOS_MaxDD=par["OOS_MaxDD"], spy_OOS_Sharpe=spy_oos_s,
                               v2_OOS_Sharpe=metrics(v2[b].loc[oos])["Sharpe"], spearman=rho))

    G = pd.DataFrame(grid)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    pd.DataFrame(epi).to_csv(f"{OUT}.episodes.csv", index=False)
    pd.DataFrame(wf).to_csv(f"{OUT}.walkforward.csv", index=False)

    # ==================================================================== summary
    P("\n" + "=" * 118)
    P("POOLED SUMMARY — 8 (panel x book) cells per rung")
    P("=" * 118)
    for b in RUNGS:
        s = G[G.bps == b]
        piv = s.pivot_table(index=["panel", "book"], columns="arm",
                            values=["CAGR", "Sharpe", "MaxDD", "turn"])
        for arm in ("M+W-cash", "M+W-spread", "M+D-cash", "M+D-spread"):
            dS = (piv["Sharpe"][arm] - piv["Sharpe"]["M"])
            dC = (piv["CAGR"][arm] - piv["CAGR"]["M"])
            dD = (piv["MaxDD"][arm] - piv["MaxDD"]["M"])
            dT = (piv["turn"][arm] - piv["turn"]["M"])
            P(f"  @{b}bps {arm:12s} vs plain M: dSharpe {dS.mean():+.4f} (wins {int((dS>0).sum())}/8), "
              f"dCAGR {dC.mean():+.2%} (wins {int((dC>0).sum())}/8), "
              f"dMaxDD {dD.mean():+.2%} (shallower {int((dD>0).sum())}/8), dturn {dT.mean():+.2f}x/yr")
        dS = (piv["Sharpe"]["M"] - piv["Sharpe"]["W ref"])
        dC = (piv["CAGR"]["M"] - piv["CAGR"]["W ref"])
        dD = (piv["MaxDD"]["M"] - piv["MaxDD"]["W ref"])
        P(f"  @{b}bps {'M vs W (idea 3s claim)':12s}: dSharpe {dS.mean():+.4f} (wins {int((dS>0).sum())}/8), "
          f"dCAGR {dC.mean():+.2%} (wins {int((dC>0).sum())}/8), "
          f"dMaxDD {dD.mean():+.2%} (shallower {int((dD>0).sum())}/8)")
        P(f"          4b passes: W ref {int(s[s.arm=='W ref'].keep4b.sum())}/8, "
          f"M {int(s[s.arm=='M'].keep4b.sum())}/8, "
          + ", ".join(f"{a} {int(s[s.arm==a].keep4b.sum())}/8" for a in
                      ("M+W-cash", "M+W-spread", "M+D-cash", "M+D-spread"))
          + f"; 4a total {int(s.keep4a.sum())}/{len(s)}")
    P("\n  Pre-registered caveat (idea 111): 2017-2026 is very nearly H2 here, so the rule-8 OOS")
    P("  bar and 4b's H2 bar overlap. SURVIVORSHIP: both panels are current constituents.")
    Path(f"{OUT}.console.txt").write_text("\n".join(_LINES) + "\n")


if __name__ == "__main__":
    main()
