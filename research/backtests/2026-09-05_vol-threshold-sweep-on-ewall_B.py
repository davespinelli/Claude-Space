#!/usr/bin/env python3
"""Idea 95 — vol-threshold-sweep-on-ewall  (research sprint lane B, 2026-09-05)

QUESTION (pre-registered, from QUEUE.md idea 95)
    Idea 94's 4b KEEP-candidate `EWall + vol60-dg` — equal-weight EVERY name in the panel at
    75% gross, no ranking, with names whose vol20 >= 0.60 zeroed into cash — inherits the
    0.60 threshold verbatim from RULES v1 and has NEVER been re-derived.  Idea 98 subsequently
    made this book the project's most year-robust candidate (17/18 LOYO on u56, 18/18 on broad)
    and one of only two still passing 4b on both universes at 25 bps, so an unexamined constant
    is now load-bearing for an adoption decision.  Sweep it.

    theta in {0.40, 0.50, 0.60, 0.80, 1.00} x convention in {dg, rw}, on BOTH large-cap
    universes at 10 and 25 bps.  Exactly TWO tuned parameters (theta, convention).  Every one
    of the 5 x 2 x 2 x 2 = 40 points is reported, plus the 4 ungated controls.

    The falsifiable form: if 0.60 is a real threshold the Sharpe/4b surface should have
    interior structure in theta.  If the surface is FLAT in theta, the gate's contribution is
    not a volatility threshold at all and the published 0.60 is arbitrary — which does not kill
    the book but does change what RULES may claim about it.  If the surface has a strong
    interior optimum away from 0.60, the published row is worse than its own neighbourhood and
    the candidate must be re-derived (and rule 8 must then be able to find it, or it is fitting).

HARNESS
    Idea 94's script is IMPORTED, not re-implemented, so every number below sits on the same
    simulator that produced the row being audited.  `targets()` and `gate_mask()` read idea 94's
    module-level MAX_VOL; this run sets that constant per grid point and changes nothing else.
    Three checks run before any new number is read:
      (a) engine-equivalence: the ungated EWall control vs `engine.backtest` — must be exact;
      (b) idea 94's published `EWall + vol60-dg` u56 @10bps row (11.6% / 1.133 / -16.9%);
      (c) theta = 0.60 in this grid must equal (b) to machine precision.

CONSTRUCTION (all inherited, nothing re-tuned)
    weekly rebalance, t+1 execution, long-only, 75% gross, no leverage, no ranking,
    eval starts at px.index[260], IS <= 2016-12-31, OOS >= 2017-01-01.
    dg = gated-out names go to CASH (book de-grosses).   rw = book rebuilt at full 75% gross
    among the gated-in names only (no exposure change, pure composition change).

WALK-FORWARD (PROTOCOL rule 8; both selection rules fixed in writing before any OOS read)
    S1  plain-Sharpe:  argmax IS Sharpe over the 10 (theta, conv) points in the cell.
    S2  4b-aware:      among points whose IS window meets 4b's two ABSOLUTE bars computed on
                       the IS window alone (MaxDD <= 0.60 x |SPY IS MaxDD|, CAGR >= 0.70 x SPY
                       IS CAGR), argmax IS Sharpe.  Picks NOTHING if the admitted set is empty.
    Both are evaluated untouched on 2017-2026 against the ungated control, RULES v1 and SPY.

DECISIVE CONTROL (idea 94's own, kept)
    A 19-point static-gross ladder on the ungated EWall book per cell.  A gate that buys
    drawdown more expensively than simply holding less is dominated; the ladder is the
    reference price.  Idea 123's warning is honoured: the price is reported with its
    denominator (dMaxDD in pp) beside it and is marked unpriceable under BOTH an absolute
    floor (dMaxDD > 0.10 pp, idea 94's) and a RELATIVE floor (dMaxDD >= 10% of the control's
    own |MaxDD|), so no ratio here is quoted without the size of what it divides by.

CAVEATS carried, not buried
    Survivorship: both panels are current-constituent lists (idea 54).  A vol20 gate is
    exactly the instrument that bias flatters — names that blew up and delisted are absent,
    so a LOOSE threshold is flattered more than a tight one, i.e. the bias runs toward
    "the gate does nothing", which is this run's finding.  Stated, not adjusted.
    Calendar-day index (idea 38) is still unfixed for u56/broad.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_vol-threshold-sweep-on-ewall_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"

_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

FREQ, GROSS, PCOST = H.FREQ, H.GROSS, H.PCOST
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
LADDER = H.LADDER
THETAS = [0.40, 0.50, 0.60, 0.80, 1.00]          # tuned parameter 1
CONVS = ["dg", "rw"]                              # tuned parameter 2
BOOK = "EWall"

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 400)


def ew_targets(px, theta, conv):
    """idea 94's EWall book with the vol20 gate at an arbitrary threshold.
    theta is injected into the imported module's MAX_VOL; nothing else is touched."""
    old = H.MAX_VOL
    try:
        H.MAX_VOL = theta
        return H.targets(px, BOOK, "vol60", conv)
    finally:
        H.MAX_VOL = old


def paired_t(a, b):
    """Annualised mean of (a - b) and its paired daily t-stat, on the common index."""
    d = (a - b).dropna()
    if len(d) < 10 or d.std(ddof=1) == 0:
        return np.nan, np.nan
    return float(d.mean() * 252 * 100.0), float(d.mean() / (d.std(ddof=1) / np.sqrt(len(d))))


def stats(r, bars, base, spy):
    h1, h2 = H.halves(r)
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    mg = H.margins(r, bars)
    fail4b = [k for k in ("H1", "H2", "OOS", "DD", "CAGR") if mg[k] <= 0]
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"], m_CAGR=mg["CAGR"],
                pass4b=(len(fail4b) == 0), fail4b=",".join(fail4b) or "-",
                pass4a=H.pass4a(r, base))


def do_universe(uname, kw):
    px = load_universe(**kw)
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars = H.bars_of(spy)
    ms = metrics(spy)
    v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
          for c in COSTS}

    print("\n" + "=" * 200)
    print(f"UNIVERSE {uname}: {px.shape[1]} names, {px.index[0].date()} -> {px.index[-1].date()}"
          f" | eval {start.date()} -> {px.index[-1].date()} | IS <= {IS_END} | OOS >= {OOS_START}")
    print(f"SPY   CAGR {ms['CAGR']:.2%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.2%}  "
          f"halves {bars['s1']:.3f}/{bars['s2']:.3f}  OOS Sharpe {bars['soos']:.3f}")
    for c in COSTS:
        mv = metrics(v1[c])
        print(f"live RULES v1 @{c:.0f}bps: CAGR {mv['CAGR']:.2%}  Sharpe {mv['Sharpe']:.3f}  "
              f"MaxDD {mv['MaxDD']:.2%}  halves {H.halves(v1[c])[0]:.3f}/{H.halves(v1[c])[1]:.3f}  "
              f"OOS Sharpe {metrics(v1[c].loc[OOS_START:])['Sharpe']:.3f}")
    print(f"4b bars: Sharpe > {bars['s1']:.3f}(H1) / {bars['s2']:.3f}(H2) / {bars['soos']:.3f}(OOS), "
          f"MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, CAGR >= {0.70*ms['CAGR']:.2%}")
    print("=" * 200)

    # ---------------- harness checks -------------------------------------------------------
    Wc = H.targets(px, BOOK)
    a = H.run(px, Wc, bps=PCOST)["r"].loc[start:]
    e = backtest(px, Wc, cost_bps=PCOST, freq=FREQ)["returns"].loc[start:]
    print(f"CHECK (a) engine-equivalence, ungated {BOOK} @{PCOST:.0f}bps: max|diff| = "
          f"{float((a-e).abs().max()):.3e}  "
          f"{'EXACT' if float((a-e).abs().max()) < 1e-12 else 'NOT EXACT — results unsafe'}")

    pub = H.run(px, H.targets(px, BOOK, "vol60", "dg"), bps=PCOST)["r"].loc[start:]
    mp = metrics(pub)
    if uname == "universe.json":
        print(f"CHECK (b) idea 94 published EWall+vol60-dg @10bps: CAGR {mp['CAGR']:.1%} (pub 11.6%)  "
              f"Sharpe {mp['Sharpe']:.3f} (pub 1.133)  MaxDD {mp['MaxDD']:.1%} (pub -16.9%)")
    grid_060 = H.run(px, ew_targets(px, 0.60, "dg"), bps=PCOST)["r"].loc[start:]
    print(f"CHECK (c) theta=0.60/dg in THIS grid vs (b): max|diff| = "
          f"{float((grid_060-pub).abs().max()):.3e}")

    # ---------------- static-gross ladder (the reference lever) -----------------------------
    ladders = {}
    for c in COSTS:
        L = []
        for m in LADDER:
            r = H.run(px, Wc, m=float(m), bps=c)["r"].loc[start:]
            mm = metrics(r)
            L.append(dict(m=float(m), CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"]))
        ladders[c] = pd.DataFrame(L)
        sl = H.ladder_slope(ladders[c])
        print(f"static-gross ladder {uname} @{c:.0f}bps: {len(LADDER)} points, "
              f"slope {sl:.3f} pp CAGR per pp MaxDD (the price to beat)")

    # ---------------- the grid --------------------------------------------------------------
    rows, rets = [], {}
    for c in COSTS:
        rc = H.run(px, Wc, bps=c)["r"].loc[start:]
        to_c = H.run(px, Wc, bps=c)["to"].loc[start:].sum() / (len(rc) / 252.0)
        rets[("control", c)] = rc
        rows.append(dict(uni=uname, cost=c, theta=np.nan, conv="control", turn=to_c,
                         gross=float((Wc.loc[start:].sum(axis=1)).mean()),
                         nheld=float((Wc.loc[start:] > 0).sum(axis=1).mean()),
                         dCAGR=0.0, dMaxDD=0.0, price=np.nan, priceable_abs=False,
                         priceable_rel=False, dSharpe=0.0, **stats(rc, bars, v1[c], spy)))
        mc = metrics(rc)
        for theta in THETAS:
            for conv in CONVS:
                W = ew_targets(px, theta, conv)
                out = H.run(px, W, bps=c)
                r = out["r"].loc[start:]
                rets[((theta, conv), c)] = r
                ma = metrics(r)
                dC = (mc["CAGR"] - ma["CAGR"]) * 100.0
                dD = (abs(mc["MaxDD"]) - abs(ma["MaxDD"])) * 100.0
                p_abs = dD > 0.10                                  # idea 94's floor
                p_rel = dD >= 0.10 * abs(mc["MaxDD"]) * 100.0      # idea 123's floor
                dmu, dt = paired_t(r, rc)
                lev_cagr = H.matched_dd(ladders[c], ma["MaxDD"])   # the lever at the SAME MaxDD
                rows.append(dict(
                    uni=uname, cost=c, theta=theta, conv=conv,
                    turn=out["to"].loc[start:].sum() / (len(r) / 252.0),
                    gross=float(W.loc[start:].sum(axis=1).mean()),
                    nheld=float((W.loc[start:] > 0).sum(axis=1).mean()),
                    dCAGR=dC, dMaxDD=dD,
                    price=(dC / dD) if p_abs else np.nan,
                    priceable_abs=bool(p_abs), priceable_rel=bool(p_rel),
                    dSharpe=ma["Sharpe"] - mc["Sharpe"],
                    dmu_ann=dmu, t_vs_ctl=dt,
                    lev_CAGR=lev_cagr,          # ladder CAGR in pp at the arm's OWN MaxDD
                    edge_vs_lever=(ma["CAGR"] * 100.0 - lev_cagr),
                    **stats(r, bars, v1[c], spy)))

    df = pd.DataFrame(rows)
    cols = ["cost", "theta", "conv", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
            "OOS_CAGR", "OOS_MaxDD", "turn", "gross", "nheld", "dSharpe", "dmu_ann", "t_vs_ctl",
            "dCAGR", "dMaxDD", "price", "priceable_abs", "priceable_rel", "lev_CAGR",
            "edge_vs_lever", "pass4a", "pass4b", "fail4b"]
    print(f"\nGRID {uname} — ALL {len(df)} points (5 theta x 2 conv x 2 cost + 2 controls)")
    print(df[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------- rule 8 ----------------------------------------------------------------
    print(f"\nRULE 8 WALK-FORWARD {uname} — (theta, conv) chosen on 2009-{IS_END[:4]} ONLY, "
          f"evaluated untouched on {OOS_START[:4]}-2026")
    spy_i, spy_o = metrics(spy.loc[:IS_END]), metrics(spy.loc[OOS_START:])
    is_dd_cap, is_cagr_floor = 0.60 * abs(spy_i["MaxDD"]), 0.70 * spy_i["CAGR"]
    print(f"  IS bars used by S2: MaxDD <= {is_dd_cap:.2%}, CAGR >= {is_cagr_floor:.2%} "
          f"(SPY IS {spy_i['CAGR']:.2%} / {spy_i['MaxDD']:.2%})")
    wf = []
    for c in COSTS:
        cell = df[(df.cost == c) & (df.conv != "control")].copy()
        ctl_o = metrics(rets[("control", c)].loc[OOS_START:])
        v1_o = metrics(v1[c].loc[OOS_START:])
        for rule, sub in (("S1 plain-Sharpe", cell),
                          ("S2 4b-aware", cell[(cell.IS_MaxDD.abs() <= is_dd_cap)
                                               & (cell.IS_CAGR >= is_cagr_floor)])):
            if sub.empty:
                wf.append(dict(uni=uname, cost=c, rule=rule, pick="NOTHING", theta=np.nan,
                               conv="-", ctl_Sharpe=ctl_o["Sharpe"], v1_Sharpe=v1_o["Sharpe"],
                               spy_Sharpe=spy_o["Sharpe"]))
                continue
            p = sub.sort_values("IS_Sharpe", ascending=False).iloc[0]
            ro = rets[((p.theta, p.conv), c)].loc[OOS_START:]
            mo = metrics(ro)
            oos_rank = int((cell.OOS_Sharpe > mo["Sharpe"]).sum()) + 1
            wf.append(dict(uni=uname, cost=c, rule=rule,
                           pick=f"theta={p.theta:.2f}/{p.conv}", theta=p.theta, conv=p.conv,
                           IS_Sharpe=p.IS_Sharpe, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                           OOS_MaxDD=mo["MaxDD"], OOS_rank=oos_rank, n_arms=len(cell),
                           beat_ctl=bool(mo["Sharpe"] > ctl_o["Sharpe"]),
                           ctl_CAGR=ctl_o["CAGR"], ctl_Sharpe=ctl_o["Sharpe"], ctl_MaxDD=ctl_o["MaxDD"],
                           v1_CAGR=v1_o["CAGR"], v1_Sharpe=v1_o["Sharpe"], v1_MaxDD=v1_o["MaxDD"],
                           spy_CAGR=spy_o["CAGR"], spy_Sharpe=spy_o["Sharpe"], spy_MaxDD=spy_o["MaxDD"],
                           rho=H.spearman(cell.IS_Sharpe.values, cell.OOS_Sharpe.values)))
    W = pd.DataFrame(wf)
    print(W.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------- the flatness test ------------------------------------------------------
    print(f"\nFLATNESS IN THETA {uname} — is 0.60 a threshold or a constant with no surface?")
    for c in COSTS:
        for conv in CONVS:
            s = df[(df.cost == c) & (df.conv == conv)].sort_values("theta")
            ctl = df[(df.cost == c) & (df.conv == "control")].iloc[0]
            rng = s.Sharpe.max() - s.Sharpe.min()
            print(f"  @{c:.0f}bps {conv}: Sharpe " +
                  " ".join(f"{t:.2f}:{v:.3f}" for t, v in zip(s.theta, s.Sharpe)) +
                  f"  | range {rng:.3f} | control {ctl.Sharpe:.3f}"
                  f" | argmax theta={s.loc[s.Sharpe.idxmax(),'theta']:.2f}"
                  f" | mean names held " +
                  " ".join(f"{t:.2f}:{v:.1f}" for t, v in zip(s.theta, s.nheld)))
            print(f"      dCAGR vs ctl (pp/yr, paired t): " +
                  " ".join(f"{t:.2f}:{m:+.2f}(t{tt:+.2f})"
                           for t, m, tt in zip(s.theta, s.dmu_ann, s.t_vs_ctl)))
            print(f"      vs the matched-MaxDD gross lever (pp CAGR, + = gate wins): " +
                  " ".join(f"{t:.2f}:{v:+.2f}" for t, v in zip(s.theta, s.edge_vs_lever)))
    return df, W


def main():
    print(__doc__)
    frames, wfs = [], []
    for uname, kw in (("universe.json", {}), ("universe_broad.json", {"broad": True})):
        d, w = do_universe(uname, kw)
        frames.append(d)
        wfs.append(w)
    D = pd.concat(frames, ignore_index=True)
    Wf = pd.concat(wfs, ignore_index=True)
    D.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    Wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    print("\n" + "=" * 200)
    print("CROSS-UNIVERSE SUMMARY — a candidate must pass 4b on BOTH lists at a cost rung")
    g = D[D.conv != "control"]
    for c in COSTS:
        for theta in THETAS:
            for conv in CONVS:
                sel = g[(g.cost == c) & (g.theta == theta) & (g.conv == conv)]
                n = int(sel.pass4b.sum())
                print(f"  @{c:.0f}bps theta={theta:.2f} {conv}: 4b on {n}/2 universes"
                      f"  [{'  '.join(f'{r.uni.split(chr(46))[0]}:{r.fail4b}' for r in sel.itertuples())}]")
    print(f"\n4b passes: {int(g.pass4b.sum())} of {len(g)} grid points.  "
          f"4a passes: {int(g.pass4a.sum())} of {len(g)}.")
    print(f"controls: 4b {int(D[D.conv=='control'].pass4b.sum())}/4, "
          f"4a {int(D[D.conv=='control'].pass4a.sum())}/4")
    print("=" * 200)


if __name__ == "__main__":
    main()
