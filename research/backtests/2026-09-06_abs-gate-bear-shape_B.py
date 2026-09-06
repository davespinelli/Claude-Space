#!/usr/bin/env python3
"""QUEUE idea 62 — abs-gate-bear-shape (lane B, 2026-09-06).

Question
--------
Idea 4 found that in the RANKED (`top20`) book the `abs` (12-1 > 0) gate cut 2022
by ~2.3pp relative to the `200d` gate but gave 1.3-3.6pp BACK in 2020.  2022 was a
slow grinding bear; 2020 was a 23-trading-day crash.  Idea 62 asks whether that is
the *shape* of the two instruments: **is `abs`'s edge specifically the SLOW bear and
`200d`'s the FAST crash?**

The queued phrasing — "classify every SPY drawdown episode >10% by peak-to-trough
duration and compare gate performance within each class" — is a DESCRIPTIVE test.
It is also, taken literally, unusable for capital: an episode's peak-to-trough
duration is only known at the trough, i.e. after the loss.  So this script runs two
parts, and only the second can produce a KEEP.

  PART 1 (descriptive, answers the queued question).  Peak-to-trough SPY episodes
          deeper than THRESH, classified FAST/SLOW by duration DSPLIT.  Per-episode
          arm returns, per-class means, and the paired abs-minus-200d difference
          inside each class.  Full grid over THRESH x DSPLIT reported.
  PART 2 (actionable).  The only real-time version of the same claim: a
          SPEED-SWITCHING gate that runs `abs` normally and switches to `200d` when
          the market is falling FAST *as measured so far* (drawdown-to-date deeper
          than DEPTH and accumulated at more than SPEED per trading day since the
          running peak).  Exactly 2 tuned parameters (DEPTH, SPEED); every grid
          point reported; 4a / 4b judged, and PROTOCOL rule 8 walk-forward with both
          dials chosen on 2009-2016 and 2017-2026 read once, untouched.

Design (PROTOCOL rules 1-8)
---------------------------
Universe : research/universe.json (56 names) AND research/universe_broad.json (136),
           both fully reported.  SURVIVORSHIP: current constituents, so absolute
           CAGR/Sharpe are optimistic; the gate-vs-gate contrasts that answer the
           question are far less exposed (every arm draws the same names, same days).
Books    : `top20` (idea 2's ranked construction, n=20, 0.75/20 each) and `ew-all`
           (equal-weight every eligible name at 75% gross).  Both from idea 4's
           script, verbatim, so numbers are directly comparable to the record.
Gates    : none / 200d / abs / both / band3, identical to idea 4, plus PART 2's
           `switch` arm.  The instrument set is NOT tuned here.
Costs    : 5 / 10 / 25 / 50 bps, applied analytically
           (returns(c) = gross - turnover*c/1e4), which is exactly what
           engine.backtest does; a harness identity check below asserts it against a
           real cost_bps=10 run.  Verdicts are read at the PROTOCOL rung, 10 bps.
Execution: weekly rebalance, weights decided at close t applied at t+1 (engine),
           long-only, no leverage, no shorting.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

OUT = Path(__file__).with_suffix("")
FREQ = "W"
GROSS = 0.75
MAX_VOL = 0.60
NPOS = 20
COSTS = [5, 10, 25, 50]
PROTO_COST = 10
GATES = ["none", "200d", "abs", "both", "band3"]
START = "2009-01-01"          # after the 200d/252d warm-up on a 2008-01 panel
OOS_START = "2017-01-01"
IS_END = "2016-12-31"

# PART 1 grid (pre-registered: the queued threshold is 10%, the queued split is
# "fast crash" vs "slow bear"; both are swept so no single choice carries the result)
THRESHS = [0.08, 0.10, 0.15]
DSPLITS = [30, 60, 90]        # trading days peak->trough
Q_THRESH, Q_DSPLIT = 0.10, 60  # the point the queued question names

# PART 2 grid (the 2 tuned parameters)
DEPTHS = [0.05, 0.08, 0.12]           # drawdown-to-date that arms the switch
SPEEDS = [0.0015, 0.0030, 0.0060]     # drawdown per trading day since the peak


# ---------------------------------------------------------------- construction
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def abs_mom(px):
    return px.shift(21) / px.shift(252) - 1


def trend(px, gate):
    if gate == "none":
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    ma = px.rolling(200).mean()
    if gate == "200d":
        return (px > ma).fillna(False)
    if gate == "abs":
        return (abs_mom(px) > 0).fillna(False)
    if gate == "both":
        return ((px > ma) & (abs_mom(px) > 0)).fillna(False)
    if gate.startswith("band"):
        b = int(gate[4:]) / 100.0
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * (1 + b), 1.0).mask(px < ma * (1 - b), 0.0)
        return raw.ffill().fillna(0.0) > 0.5
    raise ValueError(gate)


def fast_flag(px, depth, speed):
    """PART 2's real-time regime flag, computed from SPY ONLY and lagged one day.

    True when the market is in a drawdown deeper than `depth` that has been
    accumulating at more than `speed` per trading day since the running peak.
    Uses only information available at the close of the previous day; the engine
    then applies the resulting weights at t+1, so there is no look-ahead.
    """
    spy = px["SPY"]
    eq = spy / spy.cummax()
    dd = 1 - eq
    peak_idx = pd.Series(np.arange(len(spy)), index=spy.index).where(spy >= spy.cummax()).ffill()
    age = (np.arange(len(spy)) - peak_idx).clip(lower=1)
    flag = (dd > depth) & (dd / age > speed)
    return flag.shift(1).fillna(False)


def trend_switch(px, depth, speed):
    """`abs` normally, `200d` while the fast flag is on."""
    a, d = trend(px, "abs"), trend(px, "200d")
    f = fast_flag(px, depth, speed)
    return d.where(f, a)


def eligible_from_trend(px, tr):
    return (vol20(px) < MAX_VOL) & tr


def w_top20(tr):
    def f(px):
        rank = composite(px).where(eligible_from_trend(px, tr)).rank(axis=1, ascending=False)
        return (rank <= NPOS).astype(float) * (GROSS / NPOS)
    return f


def w_ewall(tr):
    def f(px):
        e = eligible_from_trend(px, tr).astype(float)
        return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * GROSS
    return f


BOOKS = {"top20": w_top20, "ew-all": w_ewall}


# ---------------------------------------------------------------- metrics helpers
def m3(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def net(gross_r, turn, c):
    return gross_r - turn * c / 1e4


def run(px, tr, cost=None):
    """One backtest -> (gross daily returns, turnover), both trimmed to START."""
    book_fn = None  # set by caller via closure; kept explicit below
    raise RuntimeError("unused")


def run_book(px, book, tr):
    res = backtest(px, BOOKS[book](tr)(px), cost_bps=0.0, freq=FREQ)
    return res["returns"].loc[START:], res["turnover"].loc[START:]


# ---------------------------------------------------------------- PART 1: episodes
def spy_episodes(px, thresh):
    """Peak-to-trough SPY drawdown episodes deeper than `thresh`, over [START:].

    An episode starts at a running-peak day, runs to the trough (the minimum equity
    before a new peak is made), and ends at recovery (the day the prior peak is
    regained) or at the sample end.  Returns a list of dicts.
    """
    s = px["SPY"].loc[START:]
    peak = s.cummax()
    dd = s / peak - 1
    eps, i, n = [], 0, len(s)
    while i < n:
        if dd.iloc[i] >= 0:
            i += 1
            continue
        j = i
        while j < n and dd.iloc[j] < 0:
            j += 1                      # j = first recovered day (or n)
        seg = dd.iloc[i:j]
        depth = float(seg.min())
        if -depth >= thresh:
            tpos = int(np.argmin(seg.values))
            p0 = i - 1 if i > 0 else 0  # the peak day itself
            eps.append(dict(
                peak=s.index[p0], trough=s.index[i + tpos],
                end=s.index[min(j, n - 1)], recovered=j < n,
                depth=depth, dur=int(tpos + 1),
                rec_days=int(j - (i + tpos)) if j < n else np.nan,
            ))
        i = j
    return eps


def episode_ret(r, a, b):
    s = r.loc[a:b]
    return float((1 + s).prod() - 1) if len(s) else np.nan


# ---------------------------------------------------------------- main
def main():
    lines = []

    def P(*a):
        t = " ".join(str(x) for x in a)
        print(t)
        lines.append(t)

    panels = {"u56": load_universe(), "broad": load_universe(broad=True)}

    # ---- harness: analytic-cost identity vs a real cost_bps=10 run
    px0 = panels["u56"]
    tr0 = trend(px0, "200d")
    g0, t0 = run_book(px0, "top20", tr0)
    real = backtest(px0, BOOKS["top20"](tr0)(px0), cost_bps=PROTO_COST, freq=FREQ)["returns"].loc[START:]
    err = float((net(g0, t0, PROTO_COST) - real).abs().max())
    P(f"[harness] analytic-cost identity max|err| = {err:.3e}  (must be ~0)")
    assert err < 1e-12

    # ---- build every arm once, per panel/book
    curves = {}      # (panel, book, gate) -> (gross, turnover)
    for pn, px in panels.items():
        for bk in BOOKS:
            for gt in GATES:
                curves[(pn, bk, gt)] = run_book(px, bk, trend(px, gt))
    spy = {pn: px["SPY"].pct_change().fillna(0).loc[START:] for pn, px in panels.items()}

    # ================================================================ PART 1
    P("\n" + "=" * 100)
    P("PART 1 — SPY drawdown episodes, classified by peak-to-trough duration")
    P("=" * 100)

    ep_rows, cls_rows = [], []
    for th in THRESHS:
        eps = spy_episodes(panels["u56"], th)
        for ds in DSPLITS:
            for e in eps:
                klass = "FAST" if e["dur"] <= ds else "SLOW"
                for (pn, bk, gt), (g, t) in curves.items():
                    r = net(g, t, PROTO_COST)
                    ep_rows.append(dict(
                        thresh=th, dsplit=ds, klass=klass, peak=e["peak"].date(),
                        trough=e["trough"].date(), dur=e["dur"], depth=e["depth"],
                        panel=pn, book=bk, gate=gt,
                        ret_p2t=episode_ret(r, e["peak"], e["trough"]),
                        ret_full=episode_ret(r, e["peak"], e["end"]),
                    ))
    ep = pd.DataFrame(ep_rows)
    ep.to_csv(f"{OUT}.episodes.csv", index=False)

    # the queued point, described
    eps_q = spy_episodes(panels["u56"], Q_THRESH)
    P(f"\nSPY episodes deeper than {Q_THRESH:.0%} since {START} (n={len(eps_q)}), "
      f"class split at {Q_DSPLIT} trading days:")
    P(f"{'peak':>12} {'trough':>12} {'dur':>5} {'depth':>8} {'class':>6} {'recov(d)':>9}")
    for e in eps_q:
        P(f"{str(e['peak'].date()):>12} {str(e['trough'].date()):>12} {e['dur']:>5} "
          f"{e['depth']:>8.1%} {('FAST' if e['dur'] <= Q_DSPLIT else 'SLOW'):>6} "
          f"{('' if not e['recovered'] else e['rec_days']):>9}")

    # per-class gate performance, every grid point
    P("\nPeak-to-trough return by gate and class (mean over episodes, @10bps). "
      "d = abs minus 200d, positive = abs loses less.")
    P(f"{'th':>5} {'split':>6} {'panel':>6} {'book':>7} {'class':>5} {'n':>3} " +
      " ".join(f"{g:>8}" for g in GATES) + f" {'d(abs-200d)':>12}")
    for th in THRESHS:
        for ds in DSPLITS:
            for pn in panels:
                for bk in BOOKS:
                    sub = ep[(ep.thresh == th) & (ep.dsplit == ds) & (ep.panel == pn) & (ep.book == bk)]
                    for kl in ("FAST", "SLOW"):
                        s = sub[sub.klass == kl]
                        if s.empty:
                            continue
                        mu = s.groupby("gate").ret_p2t.mean()
                        n = s.gate.nunique() and len(s) // len(GATES)
                        d = mu.get("abs", np.nan) - mu.get("200d", np.nan)
                        # per-episode paired difference -> sign count
                        piv = s.pivot_table(index="peak", columns="gate", values="ret_p2t")
                        wins = int((piv["abs"] > piv["200d"]).sum())
                        cls_rows.append(dict(thresh=th, dsplit=ds, panel=pn, book=bk, klass=kl,
                                             n=n, d_abs_200d=d, abs_wins=wins,
                                             **{f"m_{g}": mu.get(g, np.nan) for g in GATES}))
                        P(f"{th:>5.2f} {ds:>6} {pn:>6} {bk:>7} {kl:>5} {n:>3} " +
                          " ".join(f"{mu.get(g, np.nan):>8.1%}" for g in GATES) +
                          f" {d:>+11.2%} ({wins}/{n})")
    cls = pd.DataFrame(cls_rows)
    cls.to_csv(f"{OUT}.classes.csv", index=False)

    # the headline test: is d(abs-200d) bigger in SLOW than in FAST?
    P("\nHEADLINE — the queued claim is: d(abs-200d) > 0 in SLOW and < 0 in FAST.")
    P(f"{'th':>5} {'split':>6} {'panel':>6} {'book':>7} {'d_FAST':>9} {'d_SLOW':>9} "
      f"{'SLOW-FAST':>10} {'claim':>7}")
    holds = 0
    total = 0
    for _, grp in cls.groupby(["thresh", "dsplit", "panel", "book"]):
        f = grp[grp.klass == "FAST"].d_abs_200d
        s = grp[grp.klass == "SLOW"].d_abs_200d
        if f.empty or s.empty:
            continue
        f, s = float(f.iloc[0]), float(s.iloc[0])
        ok = (s > 0) and (f < 0)
        holds += ok
        total += 1
        k = grp.iloc[0]
        P(f"{k.thresh:>5.2f} {k.dsplit:>6} {k.panel:>6} {k.book:>7} {f:>+8.2%} {s:>+8.2%} "
          f"{s - f:>+9.2%} {'YES' if ok else 'no':>7}")
    P(f"\nqueued claim holds in {holds} of {total} (threshold x split x panel x book) cells.")

    # per-episode detail at the queued point
    P(f"\nPer-episode peak-to-trough returns at th={Q_THRESH:.0%}, split={Q_DSPLIT}d, "
      f"u56 / top20 (@10bps):")
    q = ep[(ep.thresh == Q_THRESH) & (ep.dsplit == Q_DSPLIT) & (ep.panel == "u56") & (ep.book == "top20")]
    piv = q.pivot_table(index=["peak", "dur", "klass"], columns="gate", values="ret_p2t")
    P(piv[GATES].to_string(float_format=lambda x: f"{x:.1%}"))

    # ================================================================ PART 2
    P("\n" + "=" * 100)
    P("PART 2 — the actionable version: a real-time speed-switching gate")
    P("=" * 100)
    P("abs normally; 200d while SPY drawdown-to-date > DEPTH and accruing faster than")
    P("SPEED per trading day since the running peak.  SPY-only signal, lagged 1 day.")

    sw_rows = []
    for pn, px in panels.items():
        sp = spy[pn]
        sc, ss, sdd = m3(sp)
        s1, s2 = halves(sp)
        sp_oos = sp.loc[OOS_START:]
        s_oos = metrics(sp_oos)["Sharpe"]
        base = backtest(px, rules_v2_weights(px), cost_bps=PROTO_COST, freq=FREQ)["returns"].loc[START:]
        bc, bs, bdd = m3(base)
        b1, b2 = halves(base)
        P(f"\n--- panel {pn}: SPY {sc:.2%}/{ss:.3f}/{sdd:.2%} (H {s1:.3f}/{s2:.3f}, OOS {s_oos:.3f})"
          f" | RULES v2 {bc:.2%}/{bs:.3f}/{bdd:.2%} (H {b1:.3f}/{b2:.3f})")
        for bk in BOOKS:
            # reference arms
            for gt in GATES:
                g, t = curves[(pn, bk, gt)]
                sw_rows.append(dict(panel=pn, book=bk, arm=gt, depth=np.nan, speed=np.nan,
                                    **arm_stats(g, t, sp, base)))
            # the switch grid
            for dep in DEPTHS:
                for spd in SPEEDS:
                    g, t = run_book(px, bk, trend_switch(px, dep, spd))
                    sw_rows.append(dict(panel=pn, book=bk, arm="switch", depth=dep, speed=spd,
                                        **arm_stats(g, t, sp, base)))
    sw = pd.DataFrame(sw_rows)
    sw.to_csv(f"{OUT}.grid.csv", index=False)

    P("\nALL grid points @10bps (5 reference gates + 9 switch cells) x 2 books x 2 panels:")
    P(f"{'panel':>6} {'book':>7} {'arm':>7} {'depth':>6} {'speed':>7} {'CAGR':>7} {'Sharpe':>7} "
      f"{'MaxDD':>8} {'H1':>6} {'H2':>6} {'OOS':>6} {'turn':>6} {'4a':>4} {'4b':>18}")
    for _, r in sw.iterrows():
        P(f"{r.panel:>6} {r.book:>7} {r.arm:>7} "
          f"{'' if pd.isna(r.depth) else f'{r.depth:.2f}':>6} "
          f"{'' if pd.isna(r.speed) else f'{r.speed:.4f}':>7} "
          f"{r.CAGR:>7.2%} {r.Sharpe:>7.3f} {r.MaxDD:>8.2%} {r.H1:>6.3f} {r.H2:>6.3f} "
          f"{r.OOS:>6.3f} {r.turn:>6.2f} {('PASS' if r.pass4a else '-'):>4} "
          f"{('PASS' if not r.fail4b else 'fail:' + r.fail4b):>18}")

    P("\ncost ladder for the switch arms and their two parents (Sharpe):")
    P(f"{'panel':>6} {'book':>7} {'arm':>16} " + " ".join(f"{c:>7}bps" for c in COSTS))
    for pn, px in panels.items():
        for bk in BOOKS:
            for gt in ("abs", "200d"):
                g, t = curves[(pn, bk, gt)]
                P(f"{pn:>6} {bk:>7} {gt:>16} " +
                  " ".join(f"{metrics(net(g, t, c))['Sharpe']:>10.3f}" for c in COSTS))
            for dep in DEPTHS:
                for spd in SPEEDS:
                    g, t = run_book(px, bk, trend_switch(px, dep, spd))
                    P(f"{pn:>6} {bk:>7} {f'sw {dep:.2f}/{spd:.4f}':>16} " +
                      " ".join(f"{metrics(net(g, t, c))['Sharpe']:>10.3f}" for c in COSTS))

    # ================================================================ rule 8
    P("\n" + "=" * 100)
    P("PROTOCOL rule 8 — both dials chosen on 2009-2016 by IS Sharpe; 2017-2026 read once")
    P("=" * 100)
    wf_rows = []
    for pn, px in panels.items():
        sp = spy[pn]
        sp_oos = sp.loc[OOS_START:]
        base_oos = backtest(px, rules_v2_weights(px), cost_bps=PROTO_COST, freq=FREQ)["returns"].loc[OOS_START:]
        for bk in BOOKS:
            cand = {}
            for dep in DEPTHS:
                for spd in SPEEDS:
                    g, t = run_book(px, bk, trend_switch(px, dep, spd))
                    cand[(dep, spd)] = net(g, t, PROTO_COST)
            for gt in ("abs", "200d", "band3"):
                g, t = curves[(pn, bk, gt)]
                cand[(gt, None)] = net(g, t, PROTO_COST)
            is_sh = {k: metrics(v.loc[:IS_END])["Sharpe"] for k, v in cand.items()}
            pick = max(is_sh, key=is_sh.get)
            sw_only = {k: v for k, v in is_sh.items() if isinstance(k[0], float)}
            pick_sw = max(sw_only, key=sw_only.get)
            for label, k in (("IS pick (all arms)", pick), ("IS pick (switch only)", pick_sw),
                             ("abs", ("abs", None)), ("200d", ("200d", None)), ("band3", ("band3", None))):
                o = cand[k].loc[OOS_START:]
                c, s, dd = m3(o)
                wf_rows.append(dict(panel=pn, book=bk, label=label, arm=str(k),
                                    IS_Sharpe=is_sh[k], OOS_CAGR=c, OOS_Sharpe=s, OOS_MaxDD=dd))
            sr = pd.Series(is_sh)
            oo = pd.Series({k: metrics(v.loc[OOS_START:])["Sharpe"] for k, v in cand.items()})
            rho = float(sr.rank().corr(oo.rank()))
            wf_rows.append(dict(panel=pn, book=bk, label="Spearman(IS,OOS)", arm=f"{rho:+.3f}",
                                IS_Sharpe=np.nan, OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan))
            oc, os_, odd = m3(sp_oos)
            bc2, bs2, bdd2 = m3(base_oos)
            wf_rows.append(dict(panel=pn, book=bk, label="SPY (OOS)", arm="-", IS_Sharpe=np.nan,
                                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd))
            wf_rows.append(dict(panel=pn, book=bk, label="RULES v2 (OOS)", arm="-", IS_Sharpe=np.nan,
                                OOS_CAGR=bc2, OOS_Sharpe=bs2, OOS_MaxDD=bdd2))
    wf = pd.DataFrame(wf_rows)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(wf.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    Path(f"{OUT}.console.txt").write_text("\n".join(lines) + "\n")


def arm_stats(g, t, sp, base):
    r = net(g, t, PROTO_COST)
    c, s, dd = m3(r)
    h1, h2 = halves(r)
    oos = metrics(r.loc[OOS_START:])["Sharpe"]
    sc, ss, sdd = m3(sp)
    s1, s2 = halves(sp)
    s_oos = metrics(sp.loc[OOS_START:])["Sharpe"]
    bad = []
    if h1 <= s1: bad.append("H1")
    if h2 <= s2: bad.append("H2")
    if oos <= s_oos: bad.append("OOS")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    bh1, bh2 = halves(base)
    _, _, bdd = m3(base)
    p4a = (h1 > bh1) and (h2 > bh2) and (dd >= bdd)
    yrs = len(r) / 252
    return dict(CAGR=c, Sharpe=s, MaxDD=dd, H1=h1, H2=h2, OOS=oos,
                turn=float(t.sum() / yrs), pass4a=p4a, fail4b="+".join(bad))


if __name__ == "__main__":
    main()
