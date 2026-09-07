#!/usr/bin/env python3
"""Idea 47 - "fraction-rule-cost-and-lag" (lane cloud).

The question
------------
Idea 46 (2026-09-04) killed the fixed-FRACTION rule as an improvement over fixed-n, but found
one setting that is a 4b KEEP-candidate in its own right: **F f=0.85** (hold the top
`ceil(0.85 * E_t)` eligible names at 0.75/k), the only point in that study passing 4b on BOTH
universe.json (11.3% / 1.072 / -16.7%) and universe_broad.json (11.2% / 1.024 / -18.6%), where
idea 2's KEEP (N n=20) fails H2 on the broad list by 0.02.  Its 4b CAGR margin is only ~0.6 pp
over the floor.  The queue's prediction: **it should die sooner than n=20** under costs and
under a slower execution lag, because it holds ~2x as many names and turns them over more.

This run prices exactly that.  It sweeps the two execution dials on BOTH books at once, on
both large-cap panels plus the small-cap panel, and reports every cell.

What is swept (the two tuned parameters - PROTOCOL rule 4)
----------------------------------------------------------
    cost_bps in {0, 5, 10, 25, 50}          (PROTOCOL's 10 is the anchor; 25/50 per the brief)
    execution lag in {1d, 2d, 1w=5d}        (PROTOCOL's t+1 is the anchor)
15 cells per book per panel, ALL reported.

What is FIXED in advance and NOT searched
------------------------------------------
The two books are the record's own, taken as given:
    F085   top ceil(0.85 * E_t) at GROSS/k                 (idea 46's fraction KEEP-candidate)
    N20    top 20 at GROSS/20, de-grossing when E_t < 20    (idea 2's KEEP, the comparand)
plus two references that isolate the two ways the books differ:
    NF20   top min(20, E_t) at GROSS/min(20,E_t)           (n=20 with the cash sleeve removed)
    F100   top E_t at GROSS/E_t                            (equal-weight all eligible)
Everything else is RULES v1's own: 200d MA + vol20 < 0.60 eligibility, the 21/63/126/252d
composite, scorer with NO /sqrt(vol20) (the candidate's own), 75% gross, weekly rebalance.
IS = start..2016, OOS = 2017.. (rule 8).

Mechanics
---------
Lag   : the engine already executes weights decided at close t at t+1 (the `1d` arm).  The
        `2d` and `1w` arms shift the weight matrix a further 1 and 4 trading days, so a signal
        formed at Friday's close is filled the following Monday / the following Friday.  The
        rebalance schedule is unchanged; only the staleness of the target moves.
Costs : held weights and turnover do not depend on cost_bps, so the five rungs come from ONE
        zero-cost run per (book, lag, panel) as r_c = r_0 - turnover * c/1e4.  Checked against
        engine.backtest to machine precision at 10 bps (harness gate [a]); the script aborts
        if the check fails.
Rule 8: at EVERY (panel, cost, lag) cell independently, the book is chosen among the four on
        2009-2016 only under two rules fixed in advance - plain IS Sharpe, and IS Sharpe
        subject to the IS 4b bars - and that pick is evaluated untouched on 2017-2026 against
        the baseline's and SPY's OOS.  This asks the question the queue actually cares about:
        would an honest chooser standing in 2016 have picked the fraction book, and would it
        still have picked it at 25 bps or with a one-week lag?

SURVIVORSHIP: universe.json (56) and universe_broad.json (136) are current-constituent lists;
SMALL439 is the current constituents of a sub-$2B screen with the README's max_1d_move >= 1.0
names dropped.  Absolute CAGRs are optimistic on all three panels.  The cost and lag
comparisons hold names, days, filter, gross and cadence fixed and are far less exposed than
the levels are - that is the durable part of this run.

Deterministic, standalone.  Reads baseline.py; modifies nothing.
"""
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
VOL_SCALE = False
COSTS = [0, 5, 10, 25, 50]
LAGS = {"1d": 0, "2d": 1, "1w": 4}        # extra shift on top of the engine's own t+1
ANCHOR_COST = 10
BOOKS = [("F085", "F", 0.85), ("N20", "N", 20), ("NF20", "NF", 20), ("F100", "F", 1.00)]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name
OUT = Path(__file__).with_suffix("")

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ---------------------------------------------------------------- book construction
def ranked(px, cols):
    _, above, vol20 = score(px)
    elig = (above & (vol20 < MAX_VOL))[cols]
    s = score(px, vol_scale=VOL_SCALE)[0][cols].where(elig)
    return s.rank(axis=1, ascending=False), elig.sum(axis=1).astype(float)


def weights(rank, ecount, arm, p, extra_lag=0):
    """N  -> top p at GROSS/p (de-grosses to cash when E_t < p)  [idea 2's construction]
       NF -> top min(p, E_t) at GROSS/min(p, E_t)                 [cash sleeve removed]
       F  -> top ceil(p * E_t) at GROSS/ceil(p * E_t)             [idea 46's fraction rule]"""
    if arm == "N":
        k = pd.Series(float(p), index=rank.index)
    elif arm == "NF":
        k = np.minimum(float(p), ecount)
    elif arm == "F":
        k = np.ceil(float(p) * ecount)
    else:
        raise ValueError(arm)
    k = k.clip(lower=1.0)
    w = rank.le(k, axis=0).astype(float).mul(GROSS / k, axis=0)
    return (w.shift(extra_lag) if extra_lag else w), k


# ---------------------------------------------------------------- fast backtest
def fast_bt(px, w):
    """engine.backtest at cost_bps=0, in numpy.  Returns (gross returns, turnover, names)."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).reindex(columns=px.columns).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, FREQ).shift(1, fill_value=False).values
    n = len(px)
    cur = np.zeros(px.shape[1])
    port = np.empty(n)
    turn = np.zeros(n)
    nm = np.zeros(n)
    gr = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        port[i] = float((cur * rets[i]).sum())
        nm[i] = float((cur > 0).sum())
        gr[i] = float(cur.sum())
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    idx = px.index
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx),
            pd.Series(nm, index=idx), pd.Series(gr, index=idx))


# ---------------------------------------------------------------- metrics
def m3(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail_4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    bad = []
    if h1 <= b1: bad.append("H1")
    if h2 <= b2: bad.append("H2")
    if m3(r)[2] < m3(base)[2]: bad.append("DD")
    return ",".join(bad) if bad else "-"


def fail_4b(r, spy):
    c, s, dd = m3(r)
    h1, h2 = halves(r)
    sc, ss, sdd = m3(spy)
    s1, s2 = halves(spy)
    bad = []
    if h1 <= s1: bad.append("H1")
    if h2 <= s2: bad.append("H2")
    if metrics(r.loc[OOS_START:])["Sharpe"] <= metrics(spy.loc[OOS_START:])["Sharpe"]: bad.append("OOS")
    if abs(dd) > 0.60 * abs(sdd): bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return ",".join(bad) if bad else "-"


# ---------------------------------------------------------------- panels
def build_panels():
    px56 = load_universe().dropna(how="all").ffill()
    px136 = load_universe(broad=True).dropna(how="all").ffill()
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_all = [c for c in pxs.columns if c != "SPY"]
    s_stk = [c for c in s_all if c not in bad]
    P(f"  SMALL: {len(s_all)} names in panel, dropped {len(s_all) - len(s_stk)} with "
      f"max_1d_move >= 1.0 (README) -> {len(s_stk)} tradable")
    return [("U56", px56, list(px56.columns)),
            ("B136", px136, list(px136.columns)),
            (f"SMALL{len(s_stk)}", pxs[s_stk + ["SPY"]].dropna(how="all").ffill(), s_stk)]


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    P("=" * 165)
    P(f"Idea 47 fraction-rule-cost-and-lag (cloud) | {SCRIPT}")
    P("=" * 165)
    P(f"Swept (2 params): cost_bps {COSTS} x execution lag {list(LAGS)} = "
      f"{len(COSTS)*len(LAGS)} cells per book per panel, ALL reported.")
    P("Books FIXED in advance, not searched: F085 (idea 46's fraction KEEP-candidate), "
      "N20 (idea 2's KEEP), NF20 and F100 as decomposition references.")
    P("Prediction under test (queue): F085's 4b CAGR margin is ~0.6 pp, so it should die "
      "sooner than N20 as costs rise and execution slows.")
    P("")
    panels = build_panels()

    grid_rows, wf_rows, decay_rows, keep_rows = [], [], [], []

    for panel, px, cols in panels:
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            P("!! CALENDAR-DAY INDEX DETECTED - aborting.")
            sys.exit(1)
        start = px.index[260]
        P("=" * 165)
        P(f"PANEL {panel}: {len(cols)} tradable of {px.shape[1]} columns | "
          f"{px.index[0].date()} -> {px.index[-1].date()} | eval from {start.date()} "
          f"| index sanity 2018={yrs.get(2018)}, 2024={yrs.get(2024)}")

        rank, ecount = ranked(px, cols)
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        base_v2 = backtest(px, rules_v2_weights(px), cost_bps=ANCHOR_COST,
                           freq=FREQ)["returns"].loc[start:]
        base_v1 = backtest(px, rules_v1_weights(px), cost_bps=ANCHOR_COST,
                           freq=FREQ)["returns"].loc[start:]
        sc, ss, sdd = m3(spy)
        s1, s2 = halves(spy)
        P(f"  E_t: mean {ecount.loc[start:].mean():.1f}, median {ecount.loc[start:].median():.0f} "
          f"| SPY {sc:.2%}/{ss:.3f}/{sdd:.1%} (H1 {s1:.3f} H2 {s2:.3f}, OOS "
          f"{metrics(spy.loc[OOS_START:])['Sharpe']:.3f})")
        P(f"  4b bars: H1 > {s1:.4f}, H2 > {s2:.4f}, OOS > "
          f"{metrics(spy.loc[OOS_START:])['Sharpe']:.4f}, MaxDD >= {0.60*sdd:.2%}, "
          f"CAGR >= {0.70*sc:.2%} | 4a bars (RULES v2): H1 > {halves(base_v2)[0]:.4f}, "
          f"H2 > {halves(base_v2)[1]:.4f}, MaxDD >= {m3(base_v2)[2]:.2%}")

        # ---- one zero-cost run per (book, lag)
        raw = {}
        for bname, arm, p in BOOKS:
            for lag, k in LAGS.items():
                w, kser = weights(rank, ecount, arm, p, extra_lag=k)
                g, t, nm, gr = fast_bt(px, w)
                raw[(bname, lag)] = (g.loc[start:], t.loc[start:], nm.loc[start:], gr.loc[start:])

        # ---- harness gate [a]: fast_bt + analytic cost == engine.backtest
        w0, _ = weights(rank, ecount, "F", 0.85)
        eng = backtest(px, w0.reindex(columns=px.columns).fillna(0.0),
                       cost_bps=ANCHOR_COST, freq=FREQ)["returns"].loc[start:]
        g, t = raw[("F085", "1d")][0], raw[("F085", "1d")][1]
        d = float(np.abs((g - t * ANCHOR_COST / 1e4) - eng).max())
        P(f"  [a] fast_bt vs engine.backtest @ {ANCHOR_COST} bps: max |diff| = {d:.2e}")
        if d > 1e-12:
            P("!! HARNESS GATE FAILED - aborting.")
            sys.exit(1)

        # ---- book shape (why the prediction exists)
        P("")
        P("  Book shape at the protocol anchor (lag 1d): names held, realised gross, turnover")
        shape = []
        for bname, _, _ in BOOKS:
            for lag in LAGS:
                g, t, nm, gr = raw[(bname, lag)]
                shape.append(dict(book=bname, lag=lag, names=nm.mean(), gross=gr.mean(),
                                  turnover_x_yr=t.sum() / metrics(g)["Years"],
                                  cost_pp_yr_at_10bps=t.sum() / metrics(g)["Years"] * 10 / 1e4 * 100))
        P(pd.DataFrame(shape).to_string(index=False, float_format=lambda x: f"{x:.3f}"))

        # ---- the full grid
        P("")
        P(f"  FULL GRID on {panel} - every book x lag x cost.  4a vs RULES v2 on the same "
          f"panel/window, 4b vs SPY.")
        P(f"  {'book':<7}{'lag':<5}{'bps':>4}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}"
          f"{'H1':>7}{'H2':>7}{'OOS_CAGR':>10}{'OOS_Sh':>8}{'4a':>6}  4b-fails")
        cells = {}
        for bname, _, _ in BOOKS:
            for lag in LAGS:
                g, t, nm, gr = raw[(bname, lag)]
                for cb in COSTS:
                    r = g - t * cb / 1e4
                    cells[(bname, lag, cb)] = r
                    cg, sh, dd = m3(r)
                    h1, h2 = halves(r)
                    mo = metrics(r.loc[OOS_START:])
                    f4a, f4b = fail_4a(r, base_v2), fail_4b(r, spy)
                    P(f"  {bname:<7}{lag:<5}{cb:4d}{cg:8.2%}{sh:8.3f}{dd:8.2%}{h1:7.3f}{h2:7.3f}"
                      f"{mo['CAGR']:10.2%}{mo['Sharpe']:8.3f}{('PASS' if f4a=='-' else 'fail'):>6}  "
                      f"{'PASS' if f4b == '-' else f4b}")
                    row = dict(panel=panel, book=bname, lag=lag, bps=cb, CAGR=cg, Sharpe=sh,
                               MaxDD=dd, H1=h1, H2=h2, IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                               IS_CAGR=metrics(r.loc[:IS_END])["CAGR"],
                               IS_MaxDD=metrics(r.loc[:IS_END])["MaxDD"],
                               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                               names=nm.mean(), turn=t.sum() / metrics(g)["Years"],
                               p4a=(f4a == "-"), fail4a=f4a, p4b=(f4b == "-"), fail4b=f4b)
                    grid_rows.append(row)
                    if f4b == "-":
                        keep_rows.append(row)

        # ---- where each book dies
        P("")
        P(f"  WHERE EACH BOOK DIES on {panel} (highest cost still passing 4b, per lag):")
        died = []
        for bname, _, _ in BOOKS:
            for lag in LAGS:
                ok = [cb for cb in COSTS if fail_4b(cells[(bname, lag, cb)], spy) == "-"]
                first_fail = next((k for cb in COSTS
                                   for k in [fail_4b(cells[(bname, lag, cb)], spy)] if k != "-"), "-")
                died.append(dict(book=bname, lag=lag,
                                 max_bps_passing_4b=(max(ok) if ok else None),
                                 n_cells_passing=len(ok),
                                 first_failing_bar=first_fail,
                                 CAGR_margin_pp_at10=(m3(cells[(bname, lag, 10)])[0] - 0.70 * sc) * 100,
                                 DD_margin_pp_at10=(0.60 * abs(sdd) - abs(m3(cells[(bname, lag, 10)])[2])) * 100))
        DIED = pd.DataFrame(died)
        P(DIED.to_string(index=False, float_format=lambda x: f"{x:.2f}"))

        # ---- decay slopes
        P("")
        P(f"  COST DECAY (dCAGR and dSharpe per +10 bps over the 0-50 span) and the PRICE OF "
          f"THE LAG at {ANCHOR_COST} bps, vs the 1d arm:")
        dec = []
        for bname, _, _ in BOOKS:
            for lag in LAGS:
                c0, s0, _ = m3(cells[(bname, lag, 0)])
                c5, s5, _ = m3(cells[(bname, lag, 50)])
                ref = cells[(bname, "1d", ANCHOR_COST)]
                cur = cells[(bname, lag, ANCHOR_COST)]
                dser = cur - ref
                tstat = (dser.mean() / dser.std() * np.sqrt(len(dser))) if dser.std() > 0 else np.nan
                dec.append(dict(book=bname, lag=lag,
                                dCAGR_per10bps_pp=(c5 - c0) / 5 * 100,
                                dSharpe_per10bps=(s5 - s0) / 5,
                                lag_dCAGR_pp_yr=(m3(cur)[0] - m3(ref)[0]) * 100,
                                lag_dSharpe=m3(cur)[1] - m3(ref)[1],
                                lag_dMaxDD_pp=(m3(cur)[2] - m3(ref)[2]) * 100,
                                lag_t=tstat))
                decay_rows.append(dict(panel=panel, **dec[-1]))
        P(pd.DataFrame(dec).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

        # ---- rule 8 walk-forward at EVERY (cost, lag) cell
        P("")
        P(f"  RULE 8 WALK-FORWARD on {panel}: at each (cost, lag) the BOOK is chosen on "
          f"<= {IS_END} only, {OOS_START}.. read once.  S1 = best IS Sharpe; "
          f"S2 = best IS Sharpe among books clearing the IS 4b bars (falls back to S1).")
        is_spy = spy.loc[:IS_END]
        is_sc, _, is_sdd = m3(is_spy)
        wf = []
        for lag in LAGS:
            for cb in COSTS:
                cand = []
                for bname, _, _ in BOOKS:
                    r = cells[(bname, lag, cb)]
                    ris = r.loc[:IS_END]
                    cand.append((bname, metrics(ris)["Sharpe"],
                                 abs(m3(ris)[2]) <= 0.60 * abs(is_sdd) and m3(ris)[0] >= 0.70 * is_sc))
                s1p = max(cand, key=lambda x: x[1])[0]
                ok = [c for c in cand if c[2]]
                s2p = (max(ok, key=lambda x: x[1])[0] if ok else s1p)
                for rule, pick in (("S1", s1p), ("S2", s2p)):
                    r = cells[(pick, lag, cb)]
                    mo = metrics(r.loc[OOS_START:])
                    wf.append(dict(lag=lag, bps=cb, rule=rule, pick=pick, OOS_CAGR=mo["CAGR"],
                                   OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                   f4b=fail_4b(r, spy),
                                   F085_OOS_Sharpe=metrics(cells[("F085", lag, cb)].loc[OOS_START:])["Sharpe"],
                                   N20_OOS_Sharpe=metrics(cells[("N20", lag, cb)].loc[OOS_START:])["Sharpe"]))
                    wf_rows.append(dict(panel=panel, **wf[-1]))
        WF = pd.DataFrame(wf)
        P(WF.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        P(f"  -> the chooser picks F085 in {int((WF['pick'] == 'F085').sum())}/{len(WF)} cells "
          f"({int(((WF['pick'] == 'F085') & (WF['rule'] == 'S1')).sum())}/{len(COSTS)*len(LAGS)} under S1, "
          f"{int(((WF['pick'] == 'F085') & (WF['rule'] == 'S2')).sum())}/{len(COSTS)*len(LAGS)} under S2); "
          f"F085 beats N20 OOS in {int((WF['F085_OOS_Sharpe'] > WF['N20_OOS_Sharpe']).sum())}/{len(WF)} cells.")
        for nm_, ser in (("RULES v2 (live)", base_v2), ("RULES v1", base_v1), ("SPY", spy)):
            mo = metrics(ser.loc[OOS_START:])
            P(f"  reference {nm_:<16} full {m3(ser)[0]:7.2%}/{m3(ser)[1]:.3f}/{m3(ser)[2]:7.2%} "
              f"| OOS {mo['CAGR']:7.2%}/{mo['Sharpe']:.3f}/{mo['MaxDD']:7.2%}")
        P(f"  [{time.time()-t0:.0f}s]")

    # ---------------------------------------------------------------- global
    G = pd.DataFrame(grid_rows)
    W = pd.DataFrame(wf_rows)
    D = pd.DataFrame(decay_rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    D.to_csv(f"{OUT}.decay.csv", index=False)

    P("")
    P("=" * 165)
    P("VERDICT - does the fraction book die sooner than n=20 under costs and lag?")
    P("=" * 165)
    for panel in G.panel.unique():
        g = G[G.panel == panel]
        line = []
        for bname, _, _ in BOOKS:
            b = g[g.book == bname]
            line.append(f"{bname} {int(b.p4b.sum())}/{len(b)}")
        P(f"{panel}: 4b passes per book over the 15 (cost,lag) cells -> " + " | ".join(line)
          + f" | 4a passes {int(g.p4a.sum())}/{len(g)}")
    P("")
    tot = G.groupby("book").agg(cells=("p4b", "size"), pass4b=("p4b", "sum"),
                                pass4a=("p4a", "sum"))
    P("Pooled over all 3 panels x 15 cells = 45 per book:")
    P(tot.to_string())
    P("")
    dd = D.groupby("book").agg(dCAGR_per10bps_pp=("dCAGR_per10bps_pp", "mean"),
                               dSharpe_per10bps=("dSharpe_per10bps", "mean"))
    P("Mean cost decay by book (pooled over panels and lags):")
    P(dd.to_string(float_format=lambda x: f"{x:.4f}"))
    P("")
    lagp = D[D.lag != "1d"].groupby(["book", "lag"]).agg(
        lag_dCAGR_pp_yr=("lag_dCAGR_pp_yr", "mean"), lag_dSharpe=("lag_dSharpe", "mean"))
    P("Mean price of the execution lag at 10 bps (vs the 1d arm), pooled over panels:")
    P(lagp.to_string(float_format=lambda x: f"{x:.4f}"))
    P("")
    P(f"Walk-forward pooled: the chooser picks F085 in {int((W['pick']=='F085').sum())}/{len(W)} "
      f"(panel, cost, lag, rule) cells; F085 beats N20 on OOS Sharpe in "
      f"{int((W.F085_OOS_Sharpe > W.N20_OOS_Sharpe).sum())}/{len(W)}.")
    P("")
    P("HEAD-TO-HEAD at the protocol anchor (10 bps, 1d) and at the brief's stress points:")
    hh = G[(G.book.isin(["F085", "N20"]))
           & (((G.bps == 10) & (G.lag == "1d")) | ((G.bps == 25) & (G.lag == "1d"))
              | ((G.bps == 50) & (G.lag == "1d")) | ((G.bps == 10) & (G.lag == "1w")))]
    P(hh[["panel", "book", "lag", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
          "OOS_Sharpe", "names", "turn", "p4b", "fail4b"]]
      .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    P(f"\ntotal {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
