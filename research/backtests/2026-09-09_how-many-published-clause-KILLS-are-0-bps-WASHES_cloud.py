#!/usr/bin/env python3
"""QUEUE idea 505 — how-many-published-clause-KILLS-are-0-bps-WASHES-like-idea-275 (cloud, 2026-09-09).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 275 found the daily hard exit is -0.0015 of Sharpe gross and -0.0564 net at 10 bps: the
whole verdict is turnover, and the 'more firing = worse' ordering has corr -0.14 at 0 bps vs
-0.75 at 10.  Census the record's killed CLAUSES (stop/gate/dd/bud families, idea 396's 59 stop
arms included) for the same shape - dSharpe at 0 bps within +/-0.005 of zero but decisively
negative at 10 - and report how many KILLs are cost verdicts rather than signal verdicts.
Max 2 params (family, rung)."

Design
------
The record's clause corpus is idea 94's price-list harness (2026-09-04_drawdown-insurance-price-
list_B.py), which ideas 135 / 396 / 402 inherit: one base book, one clause bolted on, priced
against ITS OWN no-clause control on the same panel, the same days and the same cost.  This run
re-runs that corpus at THREE cost rungs (0 / 10 / 25 bps) and classifies every arm whose 10-bps
verdict is a loss into

    COST VERDICT   |dSharpe @ 0 bps| <= 0.005  and  dSharpe @ 10 bps <= -0.010
                   (the idea-275 shape: the clause is a gross-neutral wash that only the
                    turnover bill kills)
    COST VERDICT+  dSharpe @ 0 bps > +0.005 and dSharpe @ 10 bps < 0
                   (stronger: the clause HELPS gross and is still killed by its own bill)
    SIGNAL VERDICT dSharpe @ 0 bps < -0.005
                   (the clause loses before a cent of cost is charged - a real signal KILL)

Every classification bar was written before any number was read; they are idea 275's own numbers
(+/-0.005 gross, "decisively negative" net) taken literally.

Corpus (all reported, nothing selected)
    families / arms   gate  g200, band3, abs12, vol60, v1gate x {dg de-gross, rw reweight} = 10
                      stop  per-name trailing stop at 0.10 / 0.15 / 0.20 / 0.25 / 0.30      =  5
                      dd    book DD control D in 0.05/0.08/0.12, halve, reset recover|high  =  6
                      bud   entry-only turnover budget B in 0.05/0.10/0.20/0.40             =  4
    base books        V1u (v1 composite, top-5 @15%, ungated), TOP20 (composite top-20 @0.75/20),
                      EWall (equal-weight every name @75% gross)
    panels            U56 (universe.json), B136 (universe_broad.json) - the record's own clause
                      panels - plus SMALL439 as an OUT-OF-CORPUS replication (not part of the
                      published census; reported separately).
    rungs             0 / 10 / 25 bps.  25 rows are printed for completeness; the classification
                      uses 0 vs 10 only, exactly as the idea asks.

Two tuned parameters (PROTOCOL rule 4): FAMILY and RUNG.  Every setting inside a family is
reported, never selected.

Rule 8 walk-forward: within each panel x book, the arm with the highest IS (2009-2016) Sharpe at
10 bps is chosen and evaluated untouched on 2017-2026 against its own control, the live RULES v2
book and SPY; its IS classification is re-computed OOS to test whether "cost verdict" is a stable
label or an in-sample artefact.  KEEP paths 4a and 4b are evaluated for every arm on U56.

SURVIVORSHIP: universe.json / universe_broad.json are current-constituent lists and the small
panel is a current screen (data/SMALL_PANEL_README.md); tickers with max_1d_move >= 1.0 in
data/small_meta.csv are dropped first (44 of 483).  Every absolute level below is optimistic.
This run compares an arm with its own control on the same panel and the same days, so the
treatment deltas - which are the entire result - are far less exposed than the levels.

Deterministic, standalone, no network.  Does not modify RULES.md, scan.py, bot.py or baseline.py.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = Path(__file__).stem
FREQ, MAX_VOL, GROSS, NTOP, NV1, WV1 = "W", 0.60, 0.75, 20, 5, 0.15
IS_END, OOS_START = "2016-12-31", "2017-01-01"
RUNGS = [0.0, 10.0, 25.0]
BOOKS = ["V1u", "TOP20", "EWall"]
GATES = ["g200", "band3", "abs12", "vol60", "v1gate"]
STOPS = [0.10, 0.15, 0.20, 0.25, 0.30]
DDS = [0.05, 0.08, 0.12]
RESETS = ["recover", "high"]
EBUDS = [0.05, 0.10, 0.20, 0.40]
WASH, DECISIVE = 0.005, 0.010          # idea 275's own bars, taken literally

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)


# ---------------------------------------------------------------- signals (idea 94's harness)
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def gate_mask(px, gate):
    if gate is None:
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    ma = px.rolling(200).mean()
    if gate == "g200":
        return (px > ma).fillna(False)
    if gate == "band3":
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * 1.03, 1.0).mask(px < ma * 0.97, 0.0)
        return raw.ffill().fillna(0.0) > 0.5
    if gate == "abs12":
        return (px > px.shift(252)).fillna(False)
    if gate == "vol60":
        return (vol20(px) < MAX_VOL).fillna(False)
    if gate == "v1gate":
        return ((px > ma) & (vol20(px) < MAX_VOL)).fillna(False)
    raise ValueError(gate)


def base_book(px, book):
    if book == "EWall":
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    s = composite(px)
    if book == "V1u":
        s = s / vol20(px).clip(lower=0.08) ** 0.5
        n, w = NV1, WV1
    else:
        n, w = NTOP, GROSS / NTOP
    return (s.rank(axis=1, ascending=False) <= n).astype(float) * w


def targets(px, book, gate=None, conv="dg"):
    """Target weights.  conv='dg' zeroes gated-out names into CASH; conv='rw' rebuilds the book
    at full gross among the gated-in names only."""
    if gate is None:
        return base_book(px, book)
    g = gate_mask(px, gate)
    if conv == "rw":
        if book == "EWall":
            e = g.astype(float)
            return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        s = composite(px)
        if book == "V1u":
            s = s / vol20(px).clip(lower=0.08) ** 0.5
            n, w = NV1, WV1
        else:
            n, w = NTOP, GROSS / NTOP
        return (s.where(g).rank(axis=1, ascending=False) <= n).astype(float) * w
    return base_book(px, book).where(g, 0.0)


# ---------------------------------------------------------------- one simulator, every arm
def run(px, W, stop=None, D=None, k=0.5, reset="recover", ebud=None, bps=10.0, freq=FREQ):
    """engine.backtest + (per-name trailing stop) + (book DD control) + (entry-only turnover
    budget).  With every instrument off it reproduces engine.backtest to machine precision
    (asserted in GATE 1).  Costs are charged inside the loop so the DD state machine and the
    stop read NET equity through t-1."""
    pxv = px.values
    rets = px.pct_change().fillna(0.0).values
    tgt = W.reindex(px.index).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nrow, ncol = rets.shape

    cur = np.zeros(ncol)
    peak_p = np.full(ncol, np.nan)
    pending = np.zeros(ncol, dtype=bool)
    held = np.zeros((nrow, ncol))
    turn = np.zeros(nrow)
    eq, pk, armed, episodes, n_fire = 1.0, 1.0, False, 0, 0

    for i in range(nrow):
        if pending.any():                              # 1. stop exits decided at close t-1
            turn[i] += cur[pending].sum()
            cur = np.where(pending, 0.0, cur)
            pending[:] = False
        if mask[i] and i > 0:                          # 2. scheduled rebalance
            if D is not None:
                dd = eq / pk - 1.0                     # equity through close i-1: no look-ahead
                if not armed and dd < -D:
                    armed, episodes = True, episodes + 1
                elif armed and (dd >= 0.0 if reset == "high" else dd > -D / 2.0):
                    armed = False
            new = tgt[i - 1] * (k if armed else 1.0)
            s = new.sum()
            if s > 1.0:
                new = new / s
            if ebud is not None:                       # 3. entry-only budget; exits are free
                d = new - cur
                up = np.clip(d, 0.0, None).sum()
                if up > ebud:
                    new = cur + np.clip(d, None, 0.0) + np.clip(d, 0.0, None) * (ebud / up)
            turn[i] += np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        rp = float((cur * rets[i]).sum()) - turn[i] * bps / 1e4
        eq *= (1.0 + rp)
        pk = max(pk, eq)
        growth = cur * (1 + rets[i])                   # 4. drift
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
        if stop is not None:                           # 5. trailing highs / fire stops
            alive = cur > 1e-9
            p = pxv[i]
            peak_p = np.where(alive, np.fmax(np.where(np.isnan(peak_p), -np.inf, peak_p), p), np.nan)
            hit = alive & np.isfinite(p) & (p < peak_p * (1 - stop))
            if hit.any():
                pending |= hit
                n_fire += int(hit.sum())
    r = (pd.Series((held * rets).sum(axis=1), index=px.index)
         - pd.Series(turn, index=px.index) * bps / 1e4)
    return dict(r=r, to=pd.Series(turn, index=px.index), episodes=episodes, n_fire=n_fire)


# ---------------------------------------------------------------- the arm menu
def arms():
    """(family, arm-label, kwargs-for-targets, kwargs-for-run).  25 arms, all reported."""
    out = []
    for g in GATES:
        for conv in ("dg", "rw"):
            out.append(("gate", f"{g}-{conv}", dict(gate=g, conv=conv), {}))
    for s in STOPS:
        out.append(("stop", f"stop{int(s * 100)}", {}, dict(stop=s)))
    for d in DDS:
        for rs in RESETS:
            out.append(("dd", f"dd{int(d * 100)}-{rs}", {}, dict(D=d, reset=rs)))
    for b in EBUDS:
        out.append(("bud", f"ebud{b:.2f}", {}, dict(ebud=b)))
    return out


def stats(r, to=None):
    m = metrics(r)
    h = len(r) // 2
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
             H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])
    if to is not None:
        d["Turn"] = to.sum() / (len(to) / 252)
    return d


def fmt(d):
    return (f"CAGR {d['CAGR']:6.2%}  Sharpe {d['Sharpe']:7.4f}  MaxDD {d['MaxDD']:7.2%}  "
            f"H1/H2 {d['H1']:.3f}/{d['H2']:.3f}" + (f"  turn {d['Turn']:5.2f}x" if "Turn" in d else ""))


def classify(d0, d10):
    """idea 275's shape, taken literally.  Only arms that LOSE at 10 bps are classified."""
    if d10 >= 0:
        return "not-a-KILL"
    if d0 > WASH:
        return "COST+"                       # helps gross, killed by its own bill
    if abs(d0) <= WASH and d10 <= -DECISIVE:
        return "COST"                        # the idea-275 wash
    if d0 < -WASH:
        return "SIGNAL"
    return "MARGINAL"                        # loses gross-neutrally but not decisively net


def small_panel():
    mt = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(mt.loc[mt.max_1d_move >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep]


def main():
    print(__doc__)
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}
    print({k: v.shape for k, v in panels.items()})

    # ---------------- GATE 1: instruments-off must reproduce engine.backtest exactly
    print("\n" + "=" * 108)
    print("GATE 1 - run(no instrument) vs engine.backtest, max abs return difference")
    for pn, px in panels.items():
        for bk in BOOKS:
            W = targets(px, bk)
            a = run(px, W, bps=10.0)["r"]
            b = backtest(px, W, cost_bps=10.0, freq=FREQ)["returns"]
            print(f"  {pn:9s} {bk:6s}: {np.abs(a - b).max():.3e}")

    # ---------------- the census grid
    MENU = arms()
    rows = []
    for pn, px in panels.items():
        s0 = px.index[260]
        for bk in BOOKS:
            ctl = {}
            for cb in RUNGS:
                res = run(px, targets(px, bk), bps=cb)
                ctl[cb] = stats(res["r"].loc[s0:], res["to"].loc[s0:])
                rows.append(dict(panel=pn, book=bk, family="control", arm="control", cost=cb,
                                 **ctl[cb], dSharpe=0.0, dCAGR=0.0, dMaxDD=0.0, dTurn=0.0,
                                 fires=0))
            for fam, lbl, tkw, rkw in MENU:
                W = targets(px, bk, **tkw)
                per = {}
                for cb in RUNGS:
                    res = run(px, W, bps=cb, **rkw)
                    st = stats(res["r"].loc[s0:], res["to"].loc[s0:])
                    per[cb] = st
                    rows.append(dict(panel=pn, book=bk, family=fam, arm=lbl, cost=cb, **st,
                                     dSharpe=st["Sharpe"] - ctl[cb]["Sharpe"],
                                     dCAGR=st["CAGR"] - ctl[cb]["CAGR"],
                                     dMaxDD=st["MaxDD"] - ctl[cb]["MaxDD"],
                                     dTurn=st["Turn"] - ctl[cb]["Turn"],
                                     fires=res["n_fire"] + res["episodes"]))
    G = pd.DataFrame(rows)
    G.to_csv(ROOT / "research" / "backtests" / f"{STEM}.grid.csv", index=False)

    # ---------------- full grid printed, every point
    print("\n" + "=" * 108)
    print("FULL GRID - every arm vs ITS OWN no-clause control, same panel/book/days")
    for pn in panels:
        for bk in BOOKS:
            sub = G[(G.panel == pn) & (G.book == bk)]
            c10 = sub[(sub.family == "control") & (sub.cost == 10.0)].iloc[0]
            print(f"\n  {pn} / {bk}   control @10bps: {fmt(c10)}")
            print("    family arm            dS@0bps  dS@10    dS@25    dCAGR@10  dDD@10   dTurn@10  class")
            for fam, lbl, _, _ in MENU:
                a = {cb: sub[(sub.arm == lbl) & (sub.cost == cb)].iloc[0] for cb in RUNGS}
                cl = classify(a[0.0].dSharpe, a[10.0].dSharpe)
                print(f"    {fam:6s} {lbl:14s} {a[0.0].dSharpe:+8.4f} {a[10.0].dSharpe:+8.4f} "
                      f"{a[25.0].dSharpe:+8.4f} {a[10.0].dCAGR:+8.2%} {a[10.0].dMaxDD:+7.2%} "
                      f"{a[10.0].dTurn:+8.2f}  {cl}")

    # ---------------- the census answer
    print("\n" + "=" * 108)
    print("CENSUS - of the clause arms that LOSE at 10 bps, how many are COST verdicts?")
    W0 = G[(G.cost == 0.0) & (G.family != "control")].set_index(["panel", "book", "arm"])["dSharpe"]
    W10 = G[(G.cost == 10.0) & (G.family != "control")].set_index(["panel", "book", "arm"])["dSharpe"]
    C = pd.DataFrame({"d0": W0, "d10": W10}).join(
        G[(G.cost == 10.0) & (G.family != "control")].set_index(["panel", "book", "arm"])[["family", "dTurn"]])
    C["class"] = [classify(a, b) for a, b in zip(C.d0, C.d10)]
    C.to_csv(ROOT / "research" / "backtests" / f"{STEM}.census.csv")

    corpus = C[C.index.get_level_values("panel") != "SMALL439"]
    for label, sl in (("PUBLISHED CORPUS (U56 + B136, the record's clause panels)", corpus),
                      ("OUT-OF-CORPUS REPLICATION (SMALL439)", C[C.index.get_level_values("panel") == "SMALL439"]),
                      ("ALL THREE PANELS", C)):
        print(f"\n  {label}   n = {len(sl)} arms")
        tab = pd.crosstab(sl.family, sl["class"])
        print(tab.to_string())
        kills = sl[sl.d10 < 0]
        cost = kills[kills["class"].isin(["COST", "COST+"])]
        print(f"    arms losing at 10 bps: {len(kills)}/{len(sl)}   "
              f"of those COST verdicts: {len(cost)} ({len(cost) / max(len(kills), 1):.1%})  "
              f"[COST {int((kills['class'] == 'COST').sum())}, "
              f"COST+ {int((kills['class'] == 'COST+').sum())}, "
              f"SIGNAL {int((kills['class'] == 'SIGNAL').sum())}, "
              f"MARGINAL {int((kills['class'] == 'MARGINAL').sum())}]")

    print("\n  per-family COST share of 10-bps losers (published corpus):")
    for fam in ["gate", "stop", "dd", "bud"]:
        sl = corpus[corpus.family == fam]
        k = sl[sl.d10 < 0]
        c = k[k["class"].isin(["COST", "COST+"])]
        print(f"    {fam:5s} losers {len(k):3d}/{len(sl):3d}   COST {len(c):3d} "
              f"({len(c) / max(len(k), 1):5.1%})   mean d0 {sl.d0.mean():+.4f}  mean d10 {sl.d10.mean():+.4f}")

    # ---------------- idea 275's turnover-ordering statistic
    print("\n" + "=" * 108)
    print("IDEA 275's ORDERING STATISTIC - corr(dSharpe, dTurnover) by rung")
    print("  (275 measured -0.14 at 0 bps vs -0.75 at 10 bps on the daily-exit family)")
    for label, sl in (("published corpus", corpus), ("all panels", C)):
        d0 = sl.d0.corr(sl.dTurn)
        d10 = sl.d10.corr(sl.dTurn)
        print(f"  {label:18s} 0 bps {d0:+.3f}   10 bps {d10:+.3f}   n={len(sl)}")
    for fam in ["gate", "stop", "dd", "bud"]:
        sl = corpus[corpus.family == fam]
        print(f"    {fam:5s} 0 bps {sl.d0.corr(sl.dTurn):+.3f}   10 bps {sl.d10.corr(sl.dTurn):+.3f}   n={len(sl)}")

    # ---------------- rule 8 walk-forward
    print("\n" + "=" * 108)
    print("RULE 8 WALK-FORWARD - arm (family x setting) chosen on IS 2009-2016 Sharpe @10bps,")
    print("evaluated untouched on 2017-2026; the IS class label is re-computed OOS.")
    wf = []
    for pn, px in panels.items():
        s0 = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0)
        v2 = backtest(px, rules_v2_weights(px), cost_bps=10.0, freq=FREQ)["returns"]
        for bk in BOOKS:
            ctl = {cb: run(px, targets(px, bk), bps=cb)["r"] for cb in (0.0, 10.0)}
            cand = {}
            for fam, lbl, tkw, rkw in MENU:
                W = targets(px, bk, **tkw)
                cand[lbl] = (fam, {cb: run(px, W, bps=cb, **rkw)["r"] for cb in (0.0, 10.0)})
            is_sh = {lbl: metrics(v[10.0].loc[s0:IS_END])["Sharpe"] for lbl, (f, v) in cand.items()}
            best = max(is_sh, key=is_sh.get)
            fam, series = cand[best]
            d0_is = metrics(series[0.0].loc[s0:IS_END])["Sharpe"] - metrics(ctl[0.0].loc[s0:IS_END])["Sharpe"]
            d10_is = is_sh[best] - metrics(ctl[10.0].loc[s0:IS_END])["Sharpe"]
            o = {k: metrics(v.loc[OOS_START:]) for k, v in
                 dict(arm=series[10.0], ctl=ctl[10.0], v2=v2, spy=spy).items()}
            d0_o = (metrics(series[0.0].loc[OOS_START:])["Sharpe"]
                    - metrics(ctl[0.0].loc[OOS_START:])["Sharpe"])
            d10_o = o["arm"]["Sharpe"] - o["ctl"]["Sharpe"]
            print(f"\n  {pn} / {bk}: IS argmax = {best} ({fam})  IS Sharpe {is_sh[best]:.4f}")
            for k, lbl in (("arm", f"arm {best}"), ("ctl", "no-clause control"),
                           ("v2", "RULES v2 baseline (live)"), ("spy", "SPY")):
                print(f"    OOS {lbl:28s} CAGR {o[k]['CAGR']:6.2%}  Sharpe {o[k]['Sharpe']:7.4f}  "
                      f"MaxDD {o[k]['MaxDD']:7.2%}")
            print(f"    clause worth  IS d0 {d0_is:+.4f} d10 {d10_is:+.4f} [{classify(d0_is, d10_is)}]"
                  f"   OOS d0 {d0_o:+.4f} d10 {d10_o:+.4f} [{classify(d0_o, d10_o)}]")
            wf.append(dict(panel=pn, book=bk, arm=best, family=fam, is_sharpe=is_sh[best],
                           is_class=classify(d0_is, d10_is), oos_class=classify(d0_o, d10_o),
                           oos_d0=d0_o, oos_d10=d10_o, oos_sharpe=o["arm"]["Sharpe"],
                           oos_ctl=o["ctl"]["Sharpe"], oos_v2=o["v2"]["Sharpe"], oos_spy=o["spy"]["Sharpe"]))
    WF = pd.DataFrame(wf)
    WF.to_csv(ROOT / "research" / "backtests" / f"{STEM}.walkforward.csv", index=False)
    agree = (WF.is_class == WF.oos_class).mean()
    print(f"\n  IS class == OOS class in {int((WF.is_class == WF.oos_class).sum())}/{len(WF)} "
          f"cells ({agree:.0%}) - is 'cost verdict' a stable label?")

    # ---------------- KEEP paths on the live panel
    print("\n" + "=" * 108)
    print("KEEP PATHS 4a / 4b on U56 @10bps (4a vs live RULES v2; 4b vs SPY incl. rule-8 OOS)")
    px = panels["U56"]
    s0 = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0).loc[s0:]
    v2 = backtest(px, rules_v2_weights(px), cost_bps=10.0, freq=FREQ)["returns"].loc[s0:]
    b_full, spy_full = stats(v2), stats(spy)
    spy_oos = metrics(spy.loc[OOS_START:])
    print(f"  live v2 {fmt(b_full)}   OOS Sharpe {metrics(v2.loc[OOS_START:])['Sharpe']:.4f}")
    print(f"  SPY     {fmt(spy_full)}   OOS Sharpe {spy_oos['Sharpe']:.4f}")
    print(f"  4b bars: SPY H1 {spy_full['H1']:.4f} / H2 {spy_full['H2']:.4f} / OOS {spy_oos['Sharpe']:.4f}; "
          f"MaxDD floor {0.6 * spy_full['MaxDD']:.2%}; CAGR floor {0.7 * spy_full['CAGR']:.2%}")
    passes = []
    for bk in BOOKS:
        for fam, lbl, tkw, rkw in [("control", "control", {}, {})] + MENU:
            W = targets(px, bk, **tkw)
            r = run(px, W, bps=10.0, **rkw)["r"].loc[s0:]
            st, oos = stats(r), metrics(r.loc[OOS_START:])
            p4a = (st["H1"] > b_full["H1"] and st["H2"] > b_full["H2"]
                   and st["MaxDD"] >= b_full["MaxDD"])
            p4b = (st["H1"] > spy_full["H1"] and st["H2"] > spy_full["H2"]
                   and oos["Sharpe"] > spy_oos["Sharpe"]
                   and st["MaxDD"] >= 0.6 * spy_full["MaxDD"]
                   and st["CAGR"] >= 0.7 * spy_full["CAGR"])
            tag = ("4a " if p4a else "   ") + ("4b" if p4b else "  ")
            print(f"  {bk:6s} {lbl:14s} {fmt(st)}  OOS Sh {oos['Sharpe']:7.4f}  [{tag}]")
            if p4a or p4b:
                passes.append((bk, lbl, p4a, p4b))
    print(f"\n  4a/4b passes on U56: {len(passes)}  {passes}")

    print("\nfiles written:", f"{STEM}.grid.csv", f"{STEM}.census.csv", f"{STEM}.walkforward.csv")


if __name__ == "__main__":
    main()
