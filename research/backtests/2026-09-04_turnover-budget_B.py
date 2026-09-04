#!/usr/bin/env python3
"""Idea 83 - "turnover-budget-instead-of-a-cost-assumption".

The question (pre-registered, from QUEUE)
-----------------------------------------
Idea 11 proved cost enters the engine exactly as  r_t(c) = r_t(0) - turnover_t * c/1e4,
so a book's cost tolerance is 1/turnover up to a constant.  PROTOCOL fixes c = 10 bps by
assumption.  The alternative is to stop assuming a cost and instead CONSTRAIN the quantity
the cost multiplies: cap  sum_i |dw_i|  per rebalance at a budget B, executing only the
largest weight changes.  The pre-registered question is whether that budget buys more 4b
margin per unit of forgone Sharpe than the project's incumbent risk lever - reducing gross
exposure g - which idea 66 showed is an exact lever costing ~1.0 pp of CAGR per pp of MaxDD
and exactly 0.000 of Sharpe.

Two instruments on ONE axis, so the answer is an exchange rate, not a verdict
----------------------------------------------------------------------------
    budget-top   at each rebalance, delta = target - held.  If |delta|_1 > B, sort trades by
                 |delta| descending, fill them whole until the budget would be exceeded, then
                 partially fill the marginal trade with the remainder; everything else is left
                 alone.  This is the QUEUE's literal spec.  It does NOT preserve gross (a
                 truncated trade list is not self-financing), so realised gross is reported.
    budget-pro   same cap, reached by moving lambda = B/|delta|_1 of the way to target on
                 EVERY name.  Gross-preserving.  Included as the implementation-choice control:
                 if the two disagree, the result is about truncation, not about turnover.
    gross        the incumbent instrument: scale the whole book by g.  Idea 66's lever.

Books (both are standing 4b passers, so a lever can only take margin away)
    CAND20   idea 2's standing 4b KEEP-candidate: top-20 eligible by the composite WITHOUT
             /sqrt(vol20), equal weight, 75% gross, weekly.
    EWall    idea 10's `B136/EWall`: equal-weight ALL eligible names at 75% gross, no ranking.
             The project's simplest 4b-passing book.
Eligibility in both = RULES v1's gate (above 200d MA, vol20 < 0.60), unchanged.

Tuned parameters (PROTOCOL rule 4: at most two)
    B  in {0.10, 0.20, 0.40, inf}   turnover budget per rebalance
    g  in {0.75, 0.65, 0.55, 0.45, 0.35}  gross exposure
    Exactly two, and EVERY grid point is reported.  B=inf and g=0.75 are the same arm and
    serve as the shared control from which both exchange rates are measured.

Grid = 2 universes x 2 books x [3 budgets x 2 modes + 1 control + 4 gross levels]
     = 2 x 2 x 11 = 44 arms, each at costs {0, 5, 10, 25} bps  ->  176 reported points,
     plus a continuous 0.5 bp breakeven curve per arm (exact, via the linear cost identity).

Verdicts (both KEEP paths, every point)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than v1, v1 taken at the SAME cost.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample (rule 8), MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.  Five scalar margins are reported alongside the pass flag so a
        lever's effect on 4b can be read continuously rather than as a bit flip.

Walk-forward (PROTOCOL rule 8), selection rules fixed before any OOS number was read
    S-B  among the budget arms (both modes + control), the highest 2009-2016 Sharpe; ties ->
         larger B, then `pro`.  S-G  the same among the gross arms; ties -> larger g.
    Both are then evaluated untouched on 2017-2026 and reported against the control, the
    RULES v1 baseline and SPY.  The separate pre-registered question is whether the IS-optimal
    budget is the OOS-optimal budget at all.

Survivorship: current constituents of both lists, one-directional.  For a TURNOVER study the
bias direction matters and is stated: a survivor panel never has to rotate out of a name that
delisted, so realised turnover here is an underestimate and every budget below is, if
anything, easier to meet than it would have been live.

Deterministic, standalone.  Imports research/baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights
from engine import backtest, rebalance_mask, metrics

FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
N_CAND = 20
BUDGETS = [0.10, 0.20, 0.40]
MODES = ["top", "pro"]
GROSSES = [0.65, 0.55, 0.45, 0.35]          # 0.75 is the shared control
REPORT_COSTS = [0, 5, 10, 25]
PROTOCOL_COST = 10
FINE = np.round(np.arange(0.0, 300.5, 0.5), 1)
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
BOOKS = ["CAND20", "EWall"]
SCRIPT = Path(__file__).name

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 500)


# ---------------------------------------------------------------- books
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def weights(px, book, gross=GROSS):
    elig = eligible_mask(px)
    if book == "EWall":
        cnt = elig.sum(axis=1).replace(0, np.nan)
        return elig.astype(float).div(cnt, axis=0).mul(gross).fillna(0.0)
    s = score(px, vol_scale=False)[0]
    rank = s.where(elig).rank(axis=1, ascending=False)
    return (rank <= N_CAND).astype(float) * (gross / N_CAND)


# ---------------------------------------------------------------- budgeted engine
def _execute(cur, target, budget, mode):
    """Return the post-trade weight vector under a per-rebalance |dw|_1 budget."""
    delta = target - cur
    tot = np.abs(delta).sum()
    if not np.isfinite(tot) or budget is None or tot <= budget:
        return target.copy()
    if mode == "pro":
        return cur + (budget / tot) * delta
    order = np.argsort(-np.abs(delta))                  # largest weight changes first
    new = cur.copy()
    left = budget
    for j in order:
        d = delta[j]
        a = abs(d)
        if a <= 1e-15:
            break
        if a <= left:
            new[j] = target[j]
            left -= a
        else:
            new[j] = cur[j] + np.sign(d) * left         # partial fill of the marginal trade
            left = 0.0
            break
    s = new.sum()
    if s > 1.0:                                          # long-only, no leverage (PROTOCOL 2)
        new = new / s
    return np.clip(new, 0.0, None)


def backtest_budget(prices, w, cost_bps=0.0, freq=FREQ, budget=None, mode="top"):
    """engine.backtest, with a turnover budget applied at each rebalance.
    budget=None reproduces engine.backtest exactly (asserted below)."""
    rets = prices.pct_change().fillna(0.0).values
    wt = w.reindex(prices.index).fillna(0.0).shift(1)
    wt.iloc[0] = 0.0                                     # engine leaves NaN here; pre-warm-up
    wt = wt.values
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False).values
    n = len(prices)
    held = np.zeros((n, prices.shape[1]))
    gross_s = np.zeros(n)
    cur = np.zeros(prices.shape[1])
    turnover = np.zeros(n)
    n_reb = n_bind = 0
    for i in range(n):
        if mask[i] or i == 0:
            want = np.abs(wt[i] - cur).sum()
            new = _execute(cur, wt[i], budget, mode)
            turnover[i] = np.abs(new - cur).sum()
            n_reb += 1
            if budget is not None and want > budget + 1e-12:
                n_bind += 1
            cur = new
        held[i] = cur
        gross_s[i] = cur.sum()
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    port = pd.Series((held * rets).sum(axis=1), index=prices.index) - \
        pd.Series(turnover, index=prices.index) * cost_bps / 1e4
    return {"returns": port, "turnover": pd.Series(turnover, index=prices.index),
            "gross": pd.Series(gross_s, index=prices.index),
            "bind": n_bind / n_reb if n_reb else 0.0}


# ---------------------------------------------------------------- metric helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def net(r0, to, c):
    return r0 - to * c / 1e4


def margins_4b(r, spy, spy_oos, ms):
    """Five continuous 4b margins (positive = passing that bar)."""
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m = metrics(r)
    return dict(m_H1=h1 - s1, m_H2=h2 - s2,
                m_OOS=metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy_oos)["Sharpe"],
                m_DD=0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
                m_CAGR=m["CAGR"] - 0.70 * ms["CAGR"])


def fail_4b(mg):
    f = [k[2:] for k, v in mg.items() if not v > 0]
    return ",".join(f) if f else "-"


def pass_4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def breakeven(r0, to, spy, spy_oos, ms):
    """Highest cost (0.5 bp grid) at which 4b still holds continuously from c=0."""
    if fail_4b(margins_4b(net(r0, to, 0.0), spy, spy_oos, ms)) != "-":
        return np.nan
    lo, hi = 0.0, FINE[-1]
    ok = 0.0
    for c in FINE:
        if fail_4b(margins_4b(net(r0, to, c), spy, spy_oos, ms)) == "-":
            ok = c
        else:
            break
    return ok


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


def spearman(a, b):
    """Rank correlation without scipy (the sandbox has none)."""
    a, b = pd.Series(a).rank(), pd.Series(b).rank()
    return float(a.corr(b))


# ---------------------------------------------------------------- one universe
def run_universe(uname, px):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    spy_oos = spy.loc[OOS_START:]
    ms, mso = metrics(spy), metrics(spy_oos)
    s1, s2 = half_sharpes(spy)

    print("\n" + "=" * 190)
    print(f"UNIVERSE {uname}: {px.shape[1]} names, {px.index[0].date()} -> {px.index[-1].date()}")
    print("=" * 190)
    print(f"Eval {start.date()} -> {px.index[-1].date()} | IS <= {IS_END} | OOS >= {OOS_START}")
    print(f"SPY  CAGR {ms['CAGR']:.2%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.2%}  "
          f"halves {s1:.3f}/{s2:.3f}  OOS Sharpe {mso['Sharpe']:.3f}")
    print(f"4b bars: Sharpe > {s1:.3f}/{s2:.3f} halves, > {mso['Sharpe']:.3f} OOS, "
          f"MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, CAGR >= {0.70*ms['CAGR']:.2%}")

    v1_res = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=FREQ)
    v1_r0, v1_to = v1_res["returns"].loc[start:], v1_res["turnover"].loc[start:]

    # ---- implementation check: budget=None must reproduce the engine bit for bit
    print("\nENGINE-EQUIVALENCE CHECK (budget=None vs engine.backtest, cost-free)")
    worst = 0.0
    for b in BOOKS:
        w = weights(px, b)
        a = backtest_budget(px, w, budget=None)["returns"].loc[start:]
        e = backtest(px, w, cost_bps=0.0, freq=FREQ)["returns"].loc[start:]
        worst = max(worst, float((a - e).abs().max()))
    print(f"  max |budgeted-engine - engine| = {worst:.3e}  "
          f"({'EXACT' if worst < 1e-12 else 'NOT EXACT - results below are unsafe'})")

    # ---- build every arm cost-free, then apply the exact linear cost identity
    arms = {}
    for b in BOOKS:
        w = weights(px, b)
        arms[(b, "control", np.nan)] = backtest_budget(px, w, budget=None)
        for B in BUDGETS:
            for mode in MODES:
                arms[(b, f"budget-{mode}", B)] = backtest_budget(px, w, budget=B, mode=mode)
        for g in GROSSES:
            arms[(b, "gross", g)] = backtest_budget(px, weights(px, b, gross=g), budget=None)

    rows = []
    for (b, inst, p), res in arms.items():
        r0 = res["returns"].loc[start:]
        to = res["turnover"].loc[start:]
        yrs = metrics(r0)["Years"]
        gr = res["gross"].loc[start:].mean()
        for c in REPORT_COSTS:
            r = net(r0, to, c)
            base = net(v1_r0, v1_to, c)
            m = metrics(r)
            h1, h2 = half_sharpes(r)
            roos = r.loc[OOS_START:]
            mg = margins_4b(r, spy, spy_oos, ms)
            rows.append(dict(book=b, inst=inst, param=p, cost=c,
                             CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                             H1=h1, H2=h2,
                             IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                             OOS_CAGR=metrics(roos)["CAGR"], OOS_Sharpe=metrics(roos)["Sharpe"],
                             OOS_MaxDD=metrics(roos)["MaxDD"],
                             TO=to.sum() / yrs, gross=gr,
                             p4a=pass_4a(r, base), **mg))
    df = pd.DataFrame(rows)
    df["f4b"] = [fail_4b({k: v for k, v in row.items() if k.startswith("m_")})
                 for _, row in df.iterrows()]
    df["p4b"] = df["f4b"] == "-"
    df["arm"] = df.apply(lambda r: f"{r.book}/{r.inst}" +
                         ("" if r.inst == "control" else f"{r.param:g}"), axis=1)

    print(f"\nFULL GRID {uname} - {len(df)} points, ALL reported "
          f"({len(arms)} arms x {len(REPORT_COSTS)} costs)")
    cols = ["arm", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
            "OOS_MaxDD", "TO", "gross", "m_DD", "m_CAGR", "p4a", "p4b", "f4b"]
    print(fmt(df[cols].sort_values(["arm", "cost"]).reset_index(drop=True)))

    # ---- THE COMPARISON: exchange rate vs the shared control, at PROTOCOL cost
    print(f"\nEXCHANGE RATE at {PROTOCOL_COST} bps - what each lever costs to buy drawdown")
    print("  dCAGR/dDD = pp of CAGR surrendered per pp of MaxDD removed (idea 74's axis; lower is better)")
    print("  dSharpe   = Sharpe given up vs the control (idea 66 measured 0.000 for gross)")
    print("  d4b_slack = change in min(4b margin) after scaling each margin by its own bar")
    ex = []
    at = df[df.cost == PROTOCOL_COST].set_index("arm")
    for b in BOOKS:
        ctl = at.loc[f"{b}/control"]
        for arm in at.index:
            if not arm.startswith(b + "/") or arm.endswith("control"):
                continue
            a = at.loc[arm]
            dDD = (abs(ctl.MaxDD) - abs(a.MaxDD)) * 100        # pp of MaxDD bought
            dCAGR = (ctl.CAGR - a.CAGR) * 100                  # pp of CAGR surrendered
            slack_c = min(ctl.m_H1, ctl.m_H2, ctl.m_OOS, ctl.m_DD / abs(ms["MaxDD"]),
                          ctl.m_CAGR / abs(ms["CAGR"]))
            slack_a = min(a.m_H1, a.m_H2, a.m_OOS, a.m_DD / abs(ms["MaxDD"]),
                          a.m_CAGR / abs(ms["CAGR"]))
            ex.append(dict(arm=arm, dDD_pp=dDD, dCAGR_pp=dCAGR,
                           rate=dCAGR / dDD if abs(dDD) > 1e-9 else np.nan,
                           dSharpe=a.Sharpe - ctl.Sharpe,
                           dTO=a.TO - ctl.TO, d4b_slack=slack_a - slack_c, p4b=a.p4b))
    exd = pd.DataFrame(ex)
    print(fmt(exd.set_index("arm")))

    # ---- cost tolerance: the premise of the whole idea
    print("\n4b BREAKEVEN COST per arm (exact, 0.5 bp grid; the quantity a budget is supposed to buy)")
    be = []
    for (b, inst, p), res in arms.items():
        r0, to = res["returns"].loc[start:], res["turnover"].loc[start:]
        arm = f"{b}/{inst}" + ("" if inst == "control" else f"{p:g}")
        be.append(dict(arm=arm, TO=to.sum() / metrics(r0)["Years"], bind=res["bind"],
                       breakeven_bps=breakeven(r0, to, spy, spy_oos, ms)))
    bed = pd.DataFrame(be).sort_values("arm").set_index("arm")
    print(fmt(bed))

    # ---- walk-forward (PROTOCOL rule 8)
    print("\nWALK-FORWARD (rule 8): parameters chosen on 2009-2016 Sharpe only, OOS untouched")
    wf_rows = []
    at10 = df[df.cost == PROTOCOL_COST]
    for b in BOOKS:
        for tag, insts, tiekey in [("S-B", ["control", "budget-top", "budget-pro"],
                                    lambda r: (r.IS_Sharpe, 99 if r.inst == "control" else r.param,
                                               r.inst == "budget-pro")),
                                   ("S-G", ["control", "gross"],
                                    lambda r: (r.IS_Sharpe, 0.75 if r.inst == "control" else r.param, 0))]:
            sub = at10[(at10.book == b) & (at10.inst.isin(insts))].copy()
            sub["key"] = [tiekey(r) for _, r in sub.iterrows()]
            pick = sub.sort_values("key", ascending=False).iloc[0]
            wf_rows.append(dict(book=b, rule=tag, picked=pick.arm, IS_Sharpe=pick.IS_Sharpe,
                                OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                                OOS_MaxDD=pick.OOS_MaxDD))
        ctl = at10[(at10.book == b) & (at10.inst == "control")].iloc[0]
        wf_rows.append(dict(book=b, rule="control", picked=ctl.arm, IS_Sharpe=ctl.IS_Sharpe,
                            OOS_CAGR=ctl.OOS_CAGR, OOS_Sharpe=ctl.OOS_Sharpe,
                            OOS_MaxDD=ctl.OOS_MaxDD))
    v1_10 = net(v1_r0, v1_to, PROTOCOL_COST)
    for nm, r in [("RULES v1 baseline", v1_10), ("SPY", spy)]:
        ro = r.loc[OOS_START:]
        wf_rows.append(dict(book="-", rule=nm, picked="-", IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                            OOS_CAGR=metrics(ro)["CAGR"], OOS_Sharpe=metrics(ro)["Sharpe"],
                            OOS_MaxDD=metrics(ro)["MaxDD"]))
    wf = pd.DataFrame(wf_rows)
    print(fmt(wf.set_index(["book", "rule"])))

    print("\nIS-optimal vs OOS-optimal budget (is the selection rule even pointing anywhere?)")
    for b in BOOKS:
        sub = at10[(at10.book == b) & (at10.inst.isin(["control", "budget-top", "budget-pro"]))]
        bi = sub.sort_values("IS_Sharpe").iloc[-1]
        bo = sub.sort_values("OOS_Sharpe").iloc[-1]
        print(f"  {b:<7} IS-best {bi.arm:<22} (IS {bi.IS_Sharpe:.3f}, OOS {bi.OOS_Sharpe:.3f})   "
              f"OOS-best {bo.arm:<22} (OOS {bo.OOS_Sharpe:.3f})  "
              f"Spearman(IS,OOS) over {len(sub)} arms = {spearman(sub.IS_Sharpe, sub.OOS_Sharpe):+.3f}")

    print(f"\n{uname} SUMMARY: 4b passes {int(df.p4b.sum())}/{len(df)} points, "
          f"4a passes {int(df.p4a.sum())}/{len(df)}")
    df["universe"] = uname
    exd["universe"] = uname
    bed = bed.reset_index(); bed["universe"] = uname
    return df, exd, bed


def main():
    outs = []
    for uname, px in [("universe.json(56)", load_universe()),
                      ("universe_broad(136)", load_universe(broad=True))]:
        outs.append(run_universe(uname, px))
    grid = pd.concat([o[0] for o in outs], ignore_index=True)
    exd = pd.concat([o[1] for o in outs], ignore_index=True)
    bed = pd.concat([o[2] for o in outs], ignore_index=True)
    grid.to_csv(REPO / "research" / "backtests" / SCRIPT.replace(".py", ".grid.csv"), index=False)

    print("\n" + "=" * 190)
    print("CROSS-UNIVERSE VERDICT")
    print("=" * 190)
    print(f"Total reported points: {len(grid)}   4b passes: {int(grid.p4b.sum())}   "
          f"4a passes: {int(grid.p4a.sum())}")

    print("\nMean exchange rate by instrument (pp CAGR surrendered per pp MaxDD bought, 10 bps, both universes)")
    exd["instrument"] = exd.arm.str.split("/").str[1].str.replace(r"[\d.]+$", "", regex=True)
    print(fmt(exd.groupby("instrument")[["dDD_pp", "dCAGR_pp", "rate", "dSharpe", "dTO", "d4b_slack"]]
              .agg(["mean", "min", "max"])))

    print("\nDoes a turnover budget beat the gross lever on its own axis?")
    for inst in ["budget-top", "budget-pro", "gross"]:
        s = exd[exd.instrument == inst]
        print(f"  {inst:<11} rate {s.rate.mean():+.3f} (range {s.rate.min():+.3f}..{s.rate.max():+.3f})  "
              f"dSharpe {s.dSharpe.mean():+.3f}  d4b_slack {s.d4b_slack.mean():+.4f}  "
              f"4b kept {int(s.p4b.sum())}/{len(s)}")

    print("\nBreakeven cost by arm, both universes (control = the cost tolerance a budget must raise)")
    bp = bed.pivot_table(index="arm", columns="universe", values="breakeven_bps")
    tp = bed.pivot_table(index="arm", columns="universe", values="TO")
    print(fmt(bp.join(tp, rsuffix="_TO")))

    ctl_be = bed[bed.arm.str.endswith("control")].set_index(["universe", "arm"]).breakeven_bps
    print("\nBudget arms whose 4b breakeven cost EXCEEDS their control's (the idea's success test):")
    hits = []
    for _, r in bed.iterrows():
        if "budget" not in r.arm:
            continue
        book = r.arm.split("/")[0]
        c = ctl_be.get((r.universe, f"{book}/control"), np.nan)
        if np.isfinite(r.breakeven_bps) and np.isfinite(c) and r.breakeven_bps > c:
            hits.append((r.universe, r.arm, c, r.breakeven_bps))
    print("  " + ("NONE" if not hits else
                  "\n  ".join(f"{u} {a}: {c:.1f} -> {b:.1f} bps" for u, a, c, b in hits)))
    print(f"\nScript: {SCRIPT}")


if __name__ == "__main__":
    main()
