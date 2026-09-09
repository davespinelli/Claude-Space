#!/usr/bin/env python3
"""QUEUE idea 507 — does-the-DAILY-EXIT-pay-on-a-book-that-does-not-already-churn (cloud, 2026-09-09).

Idea 275 priced RULES v1's 'hard exit any day' clause and found it vacuous on v1 (the book
already turns 23.6x/yr, so a Tuesday exit is at most three days ahead of the schedule) and
net-negative on v2 (weekly, 1.78x/yr).  The queue's objection is that BOTH live books
rebalance often enough to pre-empt the clause, so the test never gave it room to act.

This run re-prices the SAME clause on SLOW books, where a Tuesday exit is up to a full
quarter ahead of the next scheduled trade:

  cadence   W (the rung idea 275 already tested, kept as the control rung)
            M (idea 182's monthly R6 top-20 4b candidate cadence)
            Q (quarterly — 60+ trading days of exposure the clause can cut into)

Two tuned parameters, the queue's own:  x (exit depth) and cadence.  The confirmation-day
dial c is PINNED at 1 (the literal clause) so the parameter count stays at 2.

  x   {0.00, 0.01, 0.03, 0.05, 0.10}  depth below the name's own 200d MA at which a HELD
      name is dumped.  x = 0.00 is v1's literal wording; x = 0.03 is v2's band restatement.

Books (each carries its own daily eligibility, exactly as idea 275 built them):
  R6-20   idea 182's KEEP-4b-candidate book: signal R6 = px/px.shift(126)-1 divided by
          vol20.clip(0.08)**0.5, gate (px > 200dma AND vol20 < 0.60), top-20 equal weight,
          gross 0.75.  Exit fires when px < ma200*(1-x) OR vol20 >= 0.60.
  V2      RULES v2 (live): every name inside the 200d +/-3% band at 0.75/N, de-grossed to
          cash otherwise.  Exit fires when px < ma200*(1-x).

Panels: U56 (universe.json), B136 (universe_broad.json), SMALL439 (sub-$2B panel with the
44 names carrying max_1d_move >= 1.0 dropped per data/small_meta.csv).
SURVIVORSHIP: every panel is a current-constituent list; the small panel especially so
(see data/SMALL_PANEL_README.md).  Read all small-panel numbers as an upper bound.

Mechanics: weights decided at close t, applied at close t+1 (engine convention).  The daily
exit is SELL-ONLY — the sold weight goes to cash and nothing is bought back until the next
scheduled rebalance, so the book de-grosses between rebalances.  Every exit is charged
through the same turnover accumulator at the arm's own cost rung.  Cost rungs 0/10/25 bps
are derived exactly from one zero-cost run per arm (port = gross - turnover*bps/1e4).

ALL grid points are reported.  Rule 8 walk-forward: (x, cadence) chosen on 2009-2016 IS
Sharpe, evaluated untouched on 2017-2026 against the no-exit control, the live RULES v2
baseline and SPY.  Both KEEP paths (4a vs live v2, 4b vs SPY) evaluated on every arm.

Deterministic, standalone, no network.  Does not modify RULES.md, scan.py, bot.py, baseline.py.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import (  # noqa: E402
    load_universe, rules_v2_weights, band_state, metrics, backtest,
)
from engine import rebalance_mask  # noqa: E402

STEM = Path(__file__).stem
OUT = Path(__file__).parent

X_GRID = [0.00, 0.01, 0.03, 0.05, 0.10]
CADENCES = ["W", "M", "Q"]
COST_RUNGS = [0.0, 10.0, 25.0]
C_CONFIRM = 1                      # pinned: the literal clause, keeps the param count at 2
OOS_START = "2017-01-01"
IS_END = "2016-12-31"

_LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _LOG.append(s)


# ------------------------------------------------------------------ engine + sell-only exit
def backtest_exit(prices, weights, exit_sig, freq, lag=1):
    """engine.backtest with a sell-only daily exit, run at ZERO cost.

    Returns gross daily returns and the turnover series; any cost rung is then
    port = gross - turnover * bps / 1e4, which is exact (costs are linear in turnover).
    exit_sig None disables the clause and must reproduce engine.backtest.
    `lag` is the number of index BARS between the decision close and the fill; lag=1 is
    PROTOCOL rule 2's t+1.  A larger lag delays the target, the schedule and the exit by the
    SAME amount (idea 182's convention), so it is a true execution delay, not a stale signal.
    """
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(lag)
    mask = rebalance_mask(prices.index, freq).shift(lag, fill_value=False)
    if exit_sig is None:
        ex_v = np.zeros(prices.shape, dtype=bool)
    else:
        ex_v = exit_sig.reindex(prices.index).fillna(False).shift(lag, fill_value=False).astype(bool).values
    held = np.zeros(prices.shape)
    cur = np.zeros(prices.shape[1])
    turnover = np.zeros(len(prices))
    fires = np.zeros(len(prices))
    r_v, wt_v, mk = rets.values, w_target.values, mask.values
    for i in range(len(prices)):
        if mk[i] or i == 0:
            new = np.nan_to_num(wt_v[i])
            turnover[i] = np.abs(new - cur).sum()
            cur = new.copy()
        else:
            hit = ex_v[i] & (cur > 0)
            if hit.any():
                turnover[i] += cur[hit].sum()
                fires[i] = hit.sum()
                cur = cur.copy()
                cur[hit] = 0.0
        held[i] = cur
        growth = cur * (1 + r_v[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    turnover = pd.Series(turnover, index=prices.index)
    gross = pd.Series((held * rets.values).sum(axis=1), index=prices.index)
    return {"gross": gross, "turnover": turnover,
            "fires": pd.Series(fires, index=prices.index),
            "mean_gross_exp": held.sum(axis=1).mean()}


def net(res, cost_bps):
    return res["gross"] - res["turnover"] * cost_bps / 1e4


# ------------------------------------------------------------------ books
_C = {}


def gates(px):
    k = (id(px), "g")
    if k not in _C:
        ma = px.rolling(200).mean()
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        _C[k] = (ma, px > ma, vol20)
    return _C[k]


def w_r6_20(px, n=20, g=0.75, max_vol=0.60, p=0.5):
    """Idea 182's book, verbatim."""
    ma, above, vol20 = gates(px)
    s = (px / px.shift(126) - 1) / vol20.clip(lower=0.08) ** p
    elig = s.where(above & (vol20 < max_vol))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (g / n)


def w_v2(px):
    return rules_v2_weights(px)


def _confirm(bad, c):
    if c <= 1:
        return bad
    out = bad.copy()
    for k in range(1, c):
        out &= bad.shift(k).fillna(False)
    return out


def ex_r6_20(px, x, c=C_CONFIRM):
    ma, _, vol20 = gates(px)
    return _confirm(((px < ma * (1 - x)) | (vol20 >= 0.60)).fillna(False), c)


def ex_v2(px, x, c=C_CONFIRM):
    ma, _, _ = gates(px)
    return _confirm((px < ma * (1 - x)).fillna(False), c)


BOOKS = {"R6-20": (w_r6_20, ex_r6_20), "V2": (w_v2, ex_v2)}


# ------------------------------------------------------------------ metrics
def stats(r, turn=None):
    m = metrics(r)
    h = len(r) // 2
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
             H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
             OOS=metrics(r.loc[OOS_START:])["Sharpe"],
             OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
             OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"])
    d["Turn"] = np.nan if turn is None else turn.sum() / (len(turn) / 252)
    return d


def fmt(d):
    return (f"CAGR {d['CAGR']:6.2%}  Sharpe {d['Sharpe']:7.4f}  MaxDD {d['MaxDD']:7.2%}  "
            f"H1/H2 {d['H1']:.4f}/{d['H2']:.4f}  OOS {d['OOS']:.4f}  turn {d['Turn']:5.2f}x")


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c not in bad]
    return px[keep], len(bad)


def main():
    print(__doc__)
    _LOG.append(__doc__)

    px_small, n_drop = load_small()
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": px_small}
    P(f"\nSMALL panel: dropped {n_drop} tickers with max_1d_move >= 1.0; "
      f"{px_small.shape[1] - 1} names + SPY benchmark column.")
    for k, v in panels.items():
        P(f"  {k:9s} {v.shape[1]:4d} cols  {v.index[0].date()} -> {v.index[-1].date()}  {len(v)} rows")

    # ------------------------------------------------ GATE: exit-disabled == engine.backtest
    P("\n" + "=" * 108)
    P("GATE 1 — backtest_exit(exit=None) vs engine.backtest, max |return diff| (must be ~0)")
    for pn, px in panels.items():
        for bn, (wfn, _) in BOOKS.items():
            for f in CADENCES:
                a = net(backtest_exit(px, wfn(px), None, f), 10.0)
                b = backtest(px, wfn(px), cost_bps=10.0, freq=f)["returns"]
                P(f"  {pn:9s} {bn:6s} {f}: {np.abs(a - b).max():.3e}")

    # ------------------------------------------------ full grid
    rows, series = [], {}
    for pn, px in panels.items():
        s0 = px.index[260]
        for bn, (wfn, exfn) in BOOKS.items():
            w = wfn(px)
            for f in CADENCES:
                ctl = backtest_exit(px, w, None, f)
                ctl_st = {cb: stats(net(ctl, cb).loc[s0:], ctl["turnover"].loc[s0:]) for cb in COST_RUNGS}
                for cb in COST_RUNGS:
                    rows.append(dict(panel=pn, book=bn, freq=f, x=np.nan, cost=cb, kind="control",
                                     fires=0.0, gross_exp=ctl["mean_gross_exp"], **ctl_st[cb]))
                series[(pn, bn, f, "ctl")] = ctl
                for x in X_GRID:
                    res = backtest_exit(px, w, exfn(px, x), f)
                    series[(pn, bn, f, x)] = res
                    nfire = res["fires"].loc[s0:].sum()
                    for cb in COST_RUNGS:
                        st = stats(net(res, cb).loc[s0:], res["turnover"].loc[s0:])
                        c0 = ctl_st[cb]
                        rows.append(dict(panel=pn, book=bn, freq=f, x=x, cost=cb, kind="exit",
                                         fires=nfire, gross_exp=res["mean_gross_exp"], **st,
                                         dSharpe=st["Sharpe"] - c0["Sharpe"],
                                         dCAGR=st["CAGR"] - c0["CAGR"],
                                         dMaxDD=st["MaxDD"] - c0["MaxDD"],
                                         dTurn=st["Turn"] - c0["Turn"],
                                         dOOS=st["OOS"] - c0["OOS"]))
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    P("\n" + "=" * 108)
    P("FULL GRID at 10 bps — every arm minus its OWN no-exit control at the same panel/book/cadence")
    P("(fires = number of daily forced sells over the sample; gross_exp = mean invested weight)")
    for pn in panels:
        for bn in BOOKS:
            for f in CADENCES:
                sub = G[(G.panel == pn) & (G.book == bn) & (G.freq == f) & (G.cost == 10.0)]
                c0 = sub[sub.kind == "control"].iloc[0]
                P(f"\n  {pn} / {bn} / {f}   control: {fmt(c0)}  exp {c0.gross_exp:.3f}")
                P("    x     CAGR    Sharpe    MaxDD     H1      H2     OOS    turn   "
                  "dSharpe   dCAGR   dMaxDD   dOOS    dTurn  fires   exp")
                for _, r in sub[sub.kind == "exit"].iterrows():
                    P(f"    {r.x:.2f}  {r.CAGR:6.2%}  {r.Sharpe:7.4f}  {r.MaxDD:7.2%}  "
                      f"{r.H1:6.3f}  {r.H2:6.3f}  {r.OOS:6.3f}  {r.Turn:5.2f}  "
                      f"{r.dSharpe:+7.4f}  {r.dCAGR:+6.2%}  {r.dMaxDD:+6.2%}  {r.dOOS:+6.3f}  "
                      f"{r.dTurn:+5.2f}  {r.fires:5.0f}  {r.gross_exp:.3f}")

    # ------------------------------------------------ the queue's own question
    P("\n" + "=" * 108)
    P("THE QUEUE'S QUESTION — does the clause's value rise as the book slows down?")
    P("dSharpe of the daily-exit arm vs its own control, averaged over the 5 x-points, by cadence")
    for cb in COST_RUNGS:
        piv = (G[(G.kind == "exit") & (G.cost == cb)]
               .pivot_table(index=["panel", "book"], columns="freq", values="dSharpe", aggfunc="mean")
               .reindex(columns=CADENCES))
        pos = (G[(G.kind == "exit") & (G.cost == cb)]
               .pivot_table(index=["panel", "book"], columns="freq", values="dSharpe",
                            aggfunc=lambda s: (s > 0).mean())
               .reindex(columns=CADENCES))
        P(f"\n  cost {cb:.0f} bps — mean dSharpe by cadence")
        P(piv.to_string(float_format=lambda v: f"{v:+.4f}"))
        P(f"  cost {cb:.0f} bps — share of the 5 x-points with dSharpe > 0")
        P(pos.to_string(float_format=lambda v: f"{v:.2f}"))
        best = G[(G.kind == "exit") & (G.cost == cb)].groupby("freq")["dSharpe"]
        P(f"  pooled across all 6 (panel,book) cells: " +
          "  ".join(f"{f} mean {best.mean()[f]:+.4f} best {best.max()[f]:+.4f} "
                    f"pos {int((G[(G.kind=='exit')&(G.cost==cb)&(G.freq==f)].dSharpe>0).sum())}"
                    f"/{len(G[(G.kind=='exit')&(G.cost==cb)&(G.freq==f)])}" for f in CADENCES))

    P("\n  TURNOVER HEADROOM — control turnover (x/yr) by cadence, i.e. how much room the clause has")
    P(G[G.kind == "control"][G.cost == 10.0].pivot_table(index=["panel", "book"], columns="freq",
                                                         values="Turn").reindex(columns=CADENCES)
      .to_string(float_format=lambda v: f"{v:.2f}"))

    P("\n  LITERAL CLAUSE (x = 0.00, the wording RULES v2 removed) at 10 bps, by cadence")
    P("    panel     book    freq   dSharpe    dCAGR   dMaxDD    dOOS   dTurn   fires")
    for _, r in G[(G.kind == "exit") & (G.cost == 10.0) & (G.x == 0.00)].iterrows():
        P(f"    {r.panel:9s} {r.book:6s} {r.freq:4s}  {r.dSharpe:+8.4f}  {r.dCAGR:+6.2%}  "
          f"{r.dMaxDD:+6.2%}  {r.dOOS:+6.3f}  {r.dTurn:+5.2f}  {r.fires:5.0f}")

    # ------------------------------------------------ rule 8 walk-forward
    P("\n" + "=" * 108)
    P("RULE 8 WALK-FORWARD — (x, cadence) chosen on 2009-2016 IS Sharpe, 2017-2026 untouched, 10 bps")
    P("The chooser sees the 15 (x, cadence) points of its own book/panel and nothing else.")
    wf = []
    for pn, px in panels.items():
        s0 = px.index[260]
        spy = px["SPY"].pct_change().fillna(0)
        v2live = backtest(px, rules_v2_weights(px), cost_bps=10.0, freq="W")["returns"]
        for bn in BOOKS:
            cand = {}
            for f in CADENCES:
                for x in X_GRID:
                    cand[(x, f)] = net(series[(pn, bn, f, x)], 10.0)
            is_sh = {k: metrics(v.loc[s0:IS_END])["Sharpe"] for k, v in cand.items()}
            pick = max(is_sh, key=is_sh.get)
            # the honest comparand: the SAME chooser run over the no-exit controls
            ctl_c = {f: net(series[(pn, bn, f, "ctl")], 10.0) for f in CADENCES}
            ctl_is = {f: metrics(v.loc[s0:IS_END])["Sharpe"] for f, v in ctl_c.items()}
            ctl_pick = max(ctl_is, key=ctl_is.get)
            r_o = cand[pick].loc[OOS_START:]
            c_o = ctl_c[pick[1]].loc[OOS_START:]          # control at the SAME cadence
            cc_o = ctl_c[ctl_pick].loc[OOS_START:]        # control the chooser would have picked
            P(f"\n  {pn} / {bn}: IS argmax (x, cadence) = ({pick[0]:.2f}, {pick[1]})  "
              f"IS Sharpe {is_sh[pick]:.4f}   |   control IS argmax cadence = {ctl_pick} "
              f"({ctl_is[ctl_pick]:.4f})")
            for lbl, s in ((f"daily-exit x={pick[0]:.2f} {pick[1]}", r_o),
                           (f"no-exit control {pick[1]}", c_o),
                           (f"no-exit control (IS-picked {ctl_pick})", cc_o),
                           ("RULES v2 baseline (live, W)", v2live.loc[OOS_START:]),
                           ("SPY", spy.loc[OOS_START:])):
                m = metrics(s)
                P(f"    OOS {lbl:36s} CAGR {m['CAGR']:6.2%}  Sharpe {m['Sharpe']:7.4f}  MaxDD {m['MaxDD']:7.2%}")
            me, mc = metrics(r_o), metrics(c_o)
            allo = pd.Series({k: metrics(v.loc[OOS_START:])["Sharpe"] - metrics(ctl_c[k[1]].loc[OOS_START:])["Sharpe"]
                              for k, v in cand.items()})
            P(f"    OOS clause worth at the IS pick: dSharpe {me['Sharpe']-mc['Sharpe']:+.4f}  "
              f"dCAGR {me['CAGR']-mc['CAGR']:+.2%}  dMaxDD {me['MaxDD']-mc['MaxDD']:+.2%}")
            P(f"    OOS dSharpe over ALL 15 grid points: mean {allo.mean():+.4f}  median {allo.median():+.4f}  "
              f"best {allo.max():+.4f}  worst {allo.min():+.4f}  positive {int((allo>0).sum())}/15")
            for f in CADENCES:
                sl = allo[[k for k in allo.index if k[1] == f]]
                P(f"      cadence {f}: OOS dSharpe mean {sl.mean():+.4f}  positive {int((sl>0).sum())}/5")
            wf.append(dict(panel=pn, book=bn, pick_x=pick[0], pick_freq=pick[1],
                           is_sharpe=is_sh[pick], oos_dSharpe=me["Sharpe"] - mc["Sharpe"],
                           oos_pos=int((allo > 0).sum()), oos_mean=allo.mean()))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"\n  WALK-FORWARD SUMMARY: {int((W.oos_dSharpe > 0).sum())}/{len(W)} cells where the IS-picked "
      f"clause beats its own control out of sample; mean OOS dSharpe {W.oos_dSharpe.mean():+.4f}")
    P(f"  Across all 6 cells x 15 points = 90 arms, OOS-positive share "
      f"{W.oos_pos.sum()}/{6*15} = {W.oos_pos.sum()/90:.1%}")

    # ------------------------------------------------ KEEP paths
    P("\n" + "=" * 108)
    P("KEEP PATHS — 4a vs the live RULES v2 book (weekly, same panel), 4b vs SPY (incl. rule-8 OOS)")
    keeps = []
    for pn, px in panels.items():
        s0 = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[s0:]
        v2 = backtest(px, rules_v2_weights(px), cost_bps=10.0, freq="W")["returns"].loc[s0:]
        bs, ss = stats(v2), stats(spy)
        P(f"\n  {pn} comparands @10bps:")
        P(f"    live v2   {fmt(bs)}")
        P(f"    SPY       {fmt(ss)}")
        P(f"    4b bars: SPY H1 {ss['H1']:.4f} / H2 {ss['H2']:.4f} / OOS {ss['OOS']:.4f}; "
          f"MaxDD floor {0.6*ss['MaxDD']:.2%}; CAGR floor {0.7*ss['CAGR']:.2%}")
        for bn in BOOKS:
            for f in CADENCES:
                for key in ["ctl"] + X_GRID:
                    for cb in COST_RUNGS:
                        st = stats(net(series[(pn, bn, f, key)], cb).loc[s0:])
                        p4a = (st["H1"] > bs["H1"] and st["H2"] > bs["H2"] and st["MaxDD"] >= bs["MaxDD"])
                        p4b = (st["H1"] > ss["H1"] and st["H2"] > ss["H2"] and st["OOS"] > ss["OOS"]
                               and st["MaxDD"] >= 0.6 * ss["MaxDD"] and st["CAGR"] >= 0.7 * ss["CAGR"])
                        keeps.append(dict(panel=pn, book=bn, freq=f,
                                          x=("ctl" if key == "ctl" else f"{key:.2f}"), cost=cb,
                                          pass4a=p4a, pass4b=p4b, **st))
    K = pd.DataFrame(keeps)
    K.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P("\n  4a / 4b pass counts over the whole corpus (control rows included, "
      f"{len(K)} rows = 3 panels x 2 books x 3 cadences x 6 arms x 3 cost rungs):")
    P(K.groupby(["panel", "book", "cost"])[["pass4a", "pass4b"]].sum().to_string())
    P("\n  Rows that pass EITHER path (all reported):")
    hit = K[K.pass4a | K.pass4b]
    if hit.empty:
        P("    (none)")
    else:
        for _, r in hit.iterrows():
            P(f"    {r.panel:9s} {r.book:6s} {r.freq} x={r.x:5s} {r.cost:4.0f}bps  "
              f"CAGR {r.CAGR:6.2%} Sh {r.Sharpe:7.4f} DD {r.MaxDD:7.2%} "
              f"H1/H2 {r.H1:.3f}/{r.H2:.3f} OOS {r.OOS:.4f}  "
              f"[{'4a' if r.pass4a else '  '} {'4b' if r.pass4b else '  '}]")
    P("\n  Of the passing rows, how many are EXIT arms (x != ctl) vs no-exit controls:")
    if not hit.empty:
        P(f"    exit arms   4a {int(hit[(hit.x!='ctl')].pass4a.sum())}  4b {int(hit[(hit.x!='ctl')].pass4b.sum())}")
        P(f"    controls    4a {int(hit[(hit.x=='ctl')].pass4a.sum())}  4b {int(hit[(hit.x=='ctl')].pass4b.sum())}")
        P("  A clause that PAYS must produce a pass its own control does NOT.")
        for pn in panels:
            for bn in BOOKS:
                for f in CADENCES:
                    for cb in COST_RUNGS:
                        sub = K[(K.panel == pn) & (K.book == bn) & (K.freq == f) & (K.cost == cb)]
                        c = sub[sub.x == "ctl"].iloc[0]
                        e = sub[sub.x != "ctl"]
                        for path in ("pass4a", "pass4b"):
                            gained = e[e[path] & ~c[path]]
                            if len(gained):
                                P(f"    NEW {path[-2:]} from the clause: {pn} {bn} {f} {cb:.0f}bps "
                                  f"x in {list(gained.x)}")

    # ------------------------------------------------ appendix A: is the Q gain just "trade faster"?
    P("\n" + "=" * 108)
    P("APPENDIX A — the CHEAPER COMPARAND. The clause on a Q book buys back some of what the slow")
    P("cadence gave up. So price the Q + daily-exit arm against the SAME book run WEEKLY and")
    P("MONTHLY with no clause at all: if 'just rebalance faster' dominates, the clause is redundant.")
    P("    panel     book   x      Q+exit Sh   W-ctl Sh   M-ctl Sh   dSh vs W   dSh vs M   "
      "Q+exit OOS  W-ctl OOS")
    appA = []
    for pn, px in panels.items():
        s0 = px.index[260]
        for bn in BOOKS:
            wc = stats(net(series[(pn, bn, "W", "ctl")], 10.0).loc[s0:])
            mc = stats(net(series[(pn, bn, "M", "ctl")], 10.0).loc[s0:])
            for x in X_GRID:
                q = stats(net(series[(pn, bn, "Q", x)], 10.0).loc[s0:])
                P(f"    {pn:9s} {bn:6s} {x:.2f}   {q['Sharpe']:8.4f}   {wc['Sharpe']:8.4f}   "
                  f"{mc['Sharpe']:8.4f}   {q['Sharpe']-wc['Sharpe']:+8.4f}   "
                  f"{q['Sharpe']-mc['Sharpe']:+8.4f}   {q['OOS']:9.4f}  {wc['OOS']:9.4f}")
                appA.append(dict(panel=pn, book=bn, x=x, q_sh=q["Sharpe"], w_sh=wc["Sharpe"],
                                 m_sh=mc["Sharpe"], d_w=q["Sharpe"] - wc["Sharpe"],
                                 d_m=q["Sharpe"] - mc["Sharpe"], q_oos=q["OOS"], w_oos=wc["OOS"],
                                 d_w_oos=q["OOS"] - wc["OOS"]))
    A = pd.DataFrame(appA)
    A.to_csv(OUT / f"{STEM}.appendixA.csv", index=False)
    P(f"\n  Q+exit beats the same book's WEEKLY no-clause control: full-sample "
      f"{int((A.d_w > 0).sum())}/{len(A)}, OOS {int((A.d_w_oos > 0).sum())}/{len(A)}")
    P(f"  Q+exit beats the same book's MONTHLY no-clause control: {int((A.d_m > 0).sum())}/{len(A)}")

    # ------------------------------------------------ appendix B: matched mean gross exposure
    P("\n" + "=" * 108)
    P("APPENDIX B — MATCHED-EXPOSURE control (idea 396's bar: does the clause beat simply holding")
    P("less of the same book?).  The Q no-exit control is scaled by a CONSTANT k = exposure(exit)/")
    P("exposure(control) so both books run at the same mean invested weight, then re-run and re-costed.")
    P("    panel     book   x     exp(exit)  exp(ctl)     k     exit Sh   matched Sh   dSharpe    dOOS")
    appB = []
    for pn, px in panels.items():
        s0 = px.index[260]
        for bn, (wfn, _) in BOOKS.items():
            w = wfn(px)
            e_c = series[(pn, bn, "Q", "ctl")]["mean_gross_exp"]
            for x in X_GRID:
                e_e = series[(pn, bn, "Q", x)]["mean_gross_exp"]
                k = e_e / e_c
                mres = backtest_exit(px, w * k, None, "Q")
                ms = stats(net(mres, 10.0).loc[s0:])
                es = stats(net(series[(pn, bn, "Q", x)], 10.0).loc[s0:])
                P(f"    {pn:9s} {bn:6s} {x:.2f}   {e_e:8.3f}  {e_c:8.3f}  {k:6.3f}  "
                  f"{es['Sharpe']:8.4f}   {ms['Sharpe']:9.4f}  {es['Sharpe']-ms['Sharpe']:+8.4f}  "
                  f"{es['OOS']-ms['OOS']:+7.4f}")
                appB.append(dict(panel=pn, book=bn, x=x, exp_exit=e_e, exp_ctl=e_c, k=k,
                                 exit_sh=es["Sharpe"], matched_sh=ms["Sharpe"],
                                 d=es["Sharpe"] - ms["Sharpe"], d_oos=es["OOS"] - ms["OOS"],
                                 exit_dd=es["MaxDD"], matched_dd=ms["MaxDD"],
                                 exit_cagr=es["CAGR"], matched_cagr=ms["CAGR"]))
    B = pd.DataFrame(appB)
    B.to_csv(OUT / f"{STEM}.appendixB.csv", index=False)
    P(f"\n  Q daily-exit beats its own MATCHED-EXPOSURE control: full-sample "
      f"{int((B.d > 0).sum())}/{len(B)} (mean dSharpe {B.d.mean():+.4f}), "
      f"OOS {int((B.d_oos > 0).sum())}/{len(B)} (mean {B.d_oos.mean():+.4f})")
    P(f"  mean dMaxDD vs matched control {(B.exit_dd - B.matched_dd).mean():+.2%}, "
      f"mean dCAGR {(B.exit_cagr - B.matched_cagr).mean():+.2%}")

    # ------------------------------------------------ appendix C: the ZERO-TUNING arm
    P("\n" + "=" * 108)
    P("APPENDIX C — the ZERO-TUNING arm.  Nothing on this line was chosen by this run:")
    P("  book    = idea 182's published R6 top-20 (R6/vol20^0.5, gate 200dma & vol20<0.60, g=0.75)")
    P("  cadence = MONTHLY, idea 182's published value")
    P("  clause  = RULES v1's LITERAL daily hard exit, x = 0.00 (close below its own ma200), c = 1")
    P("Rule 8 is therefore not a parameter question for this arm — there is no parameter to fit.")
    P("Idea 182 reported this book failing 4b on broad in 0 of 9 cells on the drawdown cap;")
    P("the control rows below must reproduce that failure for the comparison to mean anything.")
    P("Execution-lag ladder (idea 182's convention): target, schedule and exit all delayed by")
    P("the same number of BARS, so lag=5/7 is a true delayed fill, not a stale signal.")
    P("\n    panel     arm       lag  cost   CAGR    Sharpe    MaxDD      H1      H2      OOS   "
      "OOS_CAGR  OOS_DD    4a  4b   bind")
    appC = []
    for pn, px in panels.items():
        s0 = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[s0:]
        v2 = backtest(px, rules_v2_weights(px), cost_bps=10.0, freq="W")["returns"].loc[s0:]
        bs, ss = stats(v2), stats(spy)
        w = w_r6_20(px)
        sig = ex_r6_20(px, 0.00)
        for lag in (1, 5, 7):
            for arm, res in (("control", backtest_exit(px, w, None, "M", lag)),
                             ("exit0.00", backtest_exit(px, w, sig, "M", lag))):
                for cb in COST_RUNGS:
                    st = stats(net(res, cb).loc[s0:], res["turnover"].loc[s0:])
                    p4a = (st["H1"] > bs["H1"] and st["H2"] > bs["H2"] and st["MaxDD"] >= bs["MaxDD"])
                    bars = {"H1": st["H1"] - ss["H1"], "H2": st["H2"] - ss["H2"],
                            "OOS": st["OOS"] - ss["OOS"],
                            "DD": st["MaxDD"] - 0.6 * ss["MaxDD"],
                            "CAGR": st["CAGR"] - 0.7 * ss["CAGR"]}
                    p4b = all(v > 0 for v in bars.values())
                    bind = min(bars, key=bars.get)
                    P(f"    {pn:9s} {arm:9s} {lag}  {cb:4.0f}  {st['CAGR']:6.2%}  {st['Sharpe']:7.4f}  "
                      f"{st['MaxDD']:7.2%}  {st['H1']:6.3f}  {st['H2']:6.3f}  {st['OOS']:6.4f}  "
                      f"{st['OOS_CAGR']:6.2%}  {st['OOS_MaxDD']:7.2%}  "
                      f"{'4a' if p4a else '  '}  {'4b' if p4b else '  '}   {bind} {bars[bind]:+.4f}")
                    appC.append(dict(panel=pn, arm=arm, lag=lag, cost=cb, pass4a=p4a, pass4b=p4b,
                                     bind=bind, margin=bars[bind], **st))
        P(f"    {pn:9s} SPY                    {ss['CAGR']:6.2%}  {ss['Sharpe']:7.4f}  "
          f"{ss['MaxDD']:7.2%}  {ss['H1']:6.3f}  {ss['H2']:6.3f}  {ss['OOS']:6.4f}")
        P(f"    {pn:9s} live v2                {bs['CAGR']:6.2%}  {bs['Sharpe']:7.4f}  "
          f"{bs['MaxDD']:7.2%}  {bs['H1']:6.3f}  {bs['H2']:6.3f}  {bs['OOS']:6.4f}")
    C = pd.DataFrame(appC)
    C.to_csv(OUT / f"{STEM}.appendixC.csv", index=False)
    for pn in panels:
        c = C[(C.panel == pn) & (C.arm == "control")]
        e = C[(C.panel == pn) & (C.arm == "exit0.00")]
        P(f"\n  {pn}: control 4b {int(c.pass4b.sum())}/9 cells, zero-tuning exit arm 4b "
          f"{int(e.pass4b.sum())}/9; clause dCAGR {e.CAGR.mean()-c.CAGR.mean():+.2%}, "
          f"dSharpe {e.Sharpe.mean()-c.Sharpe.mean():+.4f}, dMaxDD {e.MaxDD.mean()-c.MaxDD.mean():+.2%}")
        P(f"    binding bar on the exit arm: {sorted(set(e.bind))}, "
          f"worst margin {e.margin.min():+.4f}")

    P(f"\nwrote {STEM}.grid.csv / .walkforward.csv / .keep.csv / .appendixA.csv / "
      f".appendixB.csv / .appendixC.csv / .console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
