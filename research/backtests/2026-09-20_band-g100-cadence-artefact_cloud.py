#!/usr/bin/env python3
"""Idea 1753 (lane cloud, 2026-09-20): IS THE STANDING U56 / G=1.00 / WEEKLY 4b PASS A
TRADE-CADENCE ARTEFACT?

THE DEFECT THIS CLOSES.  Idea 1741 priced the band's drawdown credit at three TRADE cadences and
found it positive in 89.4% of weekly books, 81.8% of monthly and **3.0% of quarterly**, the sign
reversing outright at Q.  The record's standing band 4b passer -- U56, the live RULES v2 clause-2
equal-weight band book (c = 0.03, gated weight to CASH), gross 1.00, WEEKLY -- has never been
scored against that ladder as a 4b VERDICT: idea 1694 walked the weekly PHASE (when you look
inside a week) but not the CADENCE itself at G = 1.00, and idea 1761's CAL arm published D / W /
M / Q but neither the 2W rung between them, nor the per-leg MARGINS, nor a rule-8 chooser on the
cadence dial.  If the pass lives on one rung of a dial nobody chose, it is not a candidate.

THE BOOK, unchanged from the record's construction (no new device is introduced here):
    w_t = (gross / N_t) on every priced name whose 200d +/-3% band state is IN, N_t = the count of
    priced instruments that day; gated-out weight goes to CASH and is never re-spread.  Decided at
    close t, applied at t+1 (engine convention).  Identical to `baseline.rules_v2_weights(px,
    0.03, gross)`; gated at G0.

THE TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4):
  DIAL 1  CADENCE LADDER  D / W / 2W / M / Q -- the trade cadence, phase held at the committed
          last-trading-day anchor of each period.  2W = every SECOND weekly anchor; both of its
          two phases are PUBLISHED (2W-a, 2W-b), phase a is the canonical read.
  DIAL 2  PANEL AXIS      U56 / B136 / SMALL.
REPORTED AXES, not tuned, every point published to `_grid.csv`:
  GROSS {0.75, 1.00} (the idea's rung is 1.00; 0.75 is the live book's rung, free to publish)
  COST  {0, 10, 25, 50} bps, reconstructed EXACTLY off the cost-0 leg as
        r(c) = r_0 - turnover * c / 1e4 (idea 1586's identity; gated against the engine at G2).
  3 panels x 6 cadence rungs x 2 gross x 4 cost rungs = 144 scored books, all published.

WHAT WOULD MAKE THIS A FINDING, STATED BEFORE THE RUN.
  (a) the 4b pass holds at every rung of the ladder -> the cadence is not a dial and the standing
      pass is cadence-robust;
  (b) the pass holds on a CONTIGUOUS fast block (say D..M) and dies at Q -> it is a cadence
      WINDOW, publishable as such, and the RULES wording must name the cadence;
  (c) the pass holds at W alone -> it is a one-rung artefact and the book is not a candidate;
  (d) a legal IS-only chooser on the cadence dial lands OUTSIDE the passing set out of sample ->
      the pass is unreachable whatever its ex-post best rung does (rule 8's real question).
All four are reported, with every rung's five 4b legs and its BINDING (failing) leg set.

GATES.  G0 the band book == `baseline.rules_v2_weights` exactly.  G1 the fast runner ==
`engine.backtest` on returns AND turnover.  G2 the cost identity == the engine at 10 and 25 bps.
G3 CROSS-RUN: idea 1761's committed CAL D/W/M/Q cells at gross 1.00 / 10 bps reproduce on all
three panels.  G4 the 2W mask is a strict subset of the W mask with ~half its trades, and its two
phases partition it.  G5 SMALL's `max_1d_move >= 1.0` drop applied and counted.  G6 exactly two
tuned dials.  G7 no chooser reads a row on or after 2017-01-01.  G8 every cell published.
G9 determinism: no RNG is used anywhere in this script.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps headline, no leverage, no shorting); rule 3 (live
RULES v2 AND SPY); rule 4 (both KEEP paths at every cell, 2 dials); rule 8 (walk-forward, IS
2009-2016 chooses, 2017-2026 read exactly once); rule 9 (survivorship stated).  RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  U56 / B136 are CURRENT-constituent lists and SMALL is a CURRENT sub-$2B screen
(483 names since 2010, every ticker with `max_1d_move >= 1.0` in `data/small_meta.csv` dropped
first).  Every CAGR and drawdown LEVEL below is therefore optimistic and both 4b bars are easier
here than on a point-in-time panel; the 4b levels are read against SPY, which is not inflated.
The CADENCE contrasts are same-tape, same-names, same-rule comparisons with only the trade dates
moved, and are first-order immune.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_band-g100-cadence-artefact_cloud.py
"""
from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state      # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask        # noqa: E402

DATE, SLUG = "2026-09-20", "band-g100-cadence-artefact"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

BAND = 0.03
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [0, 10, 25, 50]
COST0 = 10
GROSSES = [0.75, 1.00]
CADENCES = ["D", "W", "2W-a", "2W-b", "M", "Q"]
HEAD = ["D", "W", "2W-a", "M", "Q"]          # the idea's ladder; 2W-b is the published twin phase
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]

_log: list[str] = []
_gates: list[dict] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _log.append(s)


def gate(name, value, target, ok):
    _gates.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    log(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


# ----------------------------------------------------------------------- panels (dial 2)
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.query("max_1d_move >= 1.0").ticker)
    keep = [c for c in px.columns if c not in bad]
    return px[keep], len(px.columns) - len(keep)


def book(px, cols, gross, bs):
    """The band book: gross/N over the PRICED names in `cols`, gated by the band state, gated-out
    weight to CASH.  cols == every column on U56 / B136 (SPY is a constituent of those panels) and
    every column EXCEPT SPY on SMALL, where SPY is only the benchmark joined by
    `baseline.load_universe(small=True)` -- idea 1761's convention, reproduced at G3."""
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    e[cols] = px[cols].notna().astype(float)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(bs, 0.0)


# ----------------------------------------------------------------------- engine replay
def bt_mask(px, w, mask_dec):
    """numpy replay of engine.backtest at cost 0 with an ARBITRARY decision-day mask (shifted
    t -> t+1 exactly as the engine does).  Gated against engine.backtest at G1."""
    R = np.nan_to_num(px.pct_change().values, nan=0.0)
    W = np.nan_to_num(w.reindex(px.index).values, nan=0.0)
    W = np.vstack([np.zeros((1, W.shape[1])), W[:-1]])
    m = np.concatenate([[False], np.asarray(mask_dec, bool)[:-1]])
    n = len(R)
    cur = np.zeros(R.shape[1])
    held = np.empty_like(R)
    turn = np.zeros(n)
    for i in range(n):
        if m[i] or i == 0:
            new = W[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        g = cur * (1.0 + R[i])
        tot = g.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = g / tot
    return (pd.Series((held * R).sum(axis=1), index=px.index),
            pd.Series(turn, index=px.index),
            pd.Series(held.sum(axis=1), index=px.index))


def cadence_mask(idx, tag):
    """Trade-day mask at the committed last-trading-day anchor.  2W keeps every second weekly
    anchor; -a and -b are its two phases and partition the weekly mask exactly (G4)."""
    if tag in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, tag).values.copy()
    w = rebalance_mask(idx, "W").values
    pos = np.flatnonzero(w)
    off = 0 if tag.endswith("a") else 1
    out = np.zeros(len(idx), bool)
    out[pos[off::2]] = True
    return out


def net(r0, t0, c):
    return r0 - t0 * c / 1e4


def mets(r):
    r = r.dropna()
    eq = (1 + r).cumprod()
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252.0)
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs else np.nan,
                Sharpe=(r.mean() * 252.0) / vol if vol else np.nan,
                MaxDD=float((eq / eq.cummax() - 1).min()))


def halves(r):
    h = len(r) // 2
    return mets(r.iloc[:h])["Sharpe"], mets(r.iloc[h:])["Sharpe"]


def leg_margins(m, h1, h2, om, spy):
    """The five 4b legs as PROTOCOL writes them, each margin in its own units, positive = clear."""
    return {"L1_H1": h1 - spy["h1"], "L2_H2": h2 - spy["h2"],
            "L3_OOS": om["Sharpe"] - spy["oos"]["Sharpe"],
            "L4_DD": m["MaxDD"] - DD_CAP * spy["full"]["MaxDD"],
            "L5_CAGR": m["CAGR"] - CAGR_FLOOR * spy["full"]["CAGR"]}


def binding(mar):
    bad = [k for k in LEGS if not (mar[k] > 0)]
    if not bad:
        return "none", 0
    return ("|".join(bad), len(bad))


# ----------------------------------------------------------------------- run
def main():
    log(f"# Idea 1753 (lane cloud, {DATE}) — is the standing U56 / band c={BAND} / gross 1.00 / "
        f"WEEKLY 4b pass a TRADE-CADENCE artefact?")
    log(f"# dials: CADENCE {HEAD} (+2W-b published) x PANEL {{U56,B136,SMALL}} | reported: gross "
        f"{GROSSES}, cost {COSTS} bps | warm-up {WARMUP} rows | IS<={IS_END} OOS>={OOS_START}")
    log("# no RNG is used anywhere in this script (G9)")

    u56 = load_universe()
    b136 = load_universe(broad=True)
    small, dropped = small_panel()
    PX = {"U56": u56, "B136": b136, "SMALL": small}
    gate("G5 SMALL max_1d_move>=1.0 drop", f"{dropped} tickers dropped, {small.shape[1]-1} kept + SPY",
         "drop applied", dropped > 0)
    gate("G6 tuned dials", "CADENCE ladder, PANEL axis", "exactly 2", True)
    for k, v in PX.items():
        log(f"# panel {k}: {v.shape[1]} columns, {v.index[0].date()} -> {v.index[-1].date()} "
            f"({len(v)} rows, {len(v)/252:.1f}y)")

    # ---- G0 / G1 / G2 -------------------------------------------------------------
    px = PX["U56"]
    st0 = px.index[WARMUP]
    wb = rules_v2_weights(px, BAND, 1.00)
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = 1.00 * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    mine = ew.where(band_state(px, BAND), 0.0)
    g0 = max(float(np.abs(mine.values - wb.values).max()),
             float(np.abs(book(px, list(px.columns), 1.00, band_state(px, BAND)).values
                          - wb.values).max()))
    gate("G0 band book == baseline.rules_v2_weights", f"max|d| = {g0:.3e}", "< 1e-15", g0 < 1e-15)

    g1r = g1t = 0.0
    for nm in ("U56", "B136"):
        p = PX[nm]
        w = rules_v2_weights(p, BAND, 1.00)
        a, at, _ = bt_mask(p, w, rebalance_mask(p.index, "W").values)
        b = engine_backtest(p, w, cost_bps=0.0, freq="W")
        g1r = max(g1r, float(np.abs(a.values - b["returns"].values).max()))
        g1t = max(g1t, float(np.abs(at.values - b["turnover"].values).max()))
    gate("G1 bt_mask == engine.backtest", f"returns {g1r:.3e}, turnover {g1t:.3e}", "< 1e-12",
         g1r < 1e-12 and g1t < 1e-12)

    p = PX["U56"]
    w = rules_v2_weights(p, BAND, 1.00)
    r0, t0, _ = bt_mask(p, w, rebalance_mask(p.index, "W").values)
    g2 = 0.0
    for c in (10, 25):
        eb = engine_backtest(p, w, cost_bps=float(c), freq="W")["returns"]
        g2 = max(g2, float(np.abs(net(r0, t0, c).values - eb.values).max()))
    gate("G2 cost identity r(c)=r0-turn*c/1e4", f"max|d| = {g2:.3e}", "< 1e-15", g2 < 1e-15)

    wm = rebalance_mask(p.index, "W").values
    ma, mb = cadence_mask(p.index, "2W-a"), cadence_mask(p.index, "2W-b")
    ok4 = (not (ma & mb).any()) and ((ma | mb) == wm).all() and \
          abs(ma.sum() - wm.sum() / 2) <= 1 and abs(mb.sum() - wm.sum() / 2) <= 1
    gate("G4 2W partitions W", f"W {wm.sum()} = 2W-a {ma.sum()} + 2W-b {mb.sum()}, disjoint",
         "partition, halves", ok4)

    # ---- baselines: live RULES v2 (weekly, per PROTOCOL rule 3) and SPY -------------
    BASE = {}
    for nm, p in PX.items():
        st = p.index[WARMUP]
        cols = [c for c in p.columns if not (nm == "SMALL" and c == "SPY")]
        br0, bt0, _ = bt_mask(p, book(p, cols, 0.75, band_state(p, BAND)),
                              rebalance_mask(p.index, "W").values)
        br0, bt0 = br0.loc[st:], bt0.loc[st:]
        spy = p["SPY"].pct_change().fillna(0.0).loc[st:]
        d = dict(start=st,
                 spy_r=spy,
                 spy=dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]), is_=mets(spy.loc[:IS_END]),
                          h1=halves(spy)[0], h2=halves(spy)[1]))
        for c in COSTS:
            r = net(br0, bt0, c)
            d[f"live{c}"] = dict(full=mets(r), oos=mets(r.loc[OOS_START:]),
                                 h1=halves(r)[0], h2=halves(r)[1])
        BASE[nm] = d
        L, S = d[f"live{COST0}"], d["spy"]
        log(f"# {nm}: LIVE RULES v2 (g=0.75, W, {COST0}bps) {L['full']['CAGR']:.2%} / "
            f"{L['full']['Sharpe']:.4f} / {L['full']['MaxDD']:.2%} (OOS {L['oos']['CAGR']:.2%} / "
            f"{L['oos']['Sharpe']:.4f} / {L['oos']['MaxDD']:.2%}) | SPY {S['full']['CAGR']:.2%} / "
            f"{S['full']['Sharpe']:.4f} / {S['full']['MaxDD']:.2%} (OOS {S['oos']['CAGR']:.2%} / "
            f"{S['oos']['Sharpe']:.4f} / {S['oos']['MaxDD']:.2%})")

    # ---- the grid -------------------------------------------------------------------
    rows = []
    for pname, p in PX.items():
        st = BASE[pname]["start"]
        spy = BASE[pname]["spy"]
        cols = [c for c in p.columns if not (pname == "SMALL" and c == "SPY")]
        bs = band_state(p, BAND)
        for gross in GROSSES:
            w = book(p, cols, gross, bs)
            for cad in CADENCES:
                m = cadence_mask(p.index, cad)
                r0, t0, gs = bt_mask(p, w, m)
                r0, t0, gs = r0.loc[st:], t0.loc[st:], gs.loc[st:]
                yrs = len(r0) / 252.0
                for c in COSTS:
                    r = net(r0, t0, c)
                    mf, mo, mi = mets(r), mets(r.loc[OOS_START:]), mets(r.loc[:IS_END])
                    h1, h2 = halves(r)
                    ih1, ih2 = halves(r.loc[:IS_END])
                    mar = leg_margins(mf, h1, h2, mo, spy)
                    bl, nbad = binding(mar)
                    LV = BASE[pname][f"live{c}"]
                    k4b_full = (h1 > spy["h1"] and h2 > spy["h2"]
                                and mf["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"]
                                and mf["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])
                    k4b_oos = (mo["Sharpe"] > spy["oos"]["Sharpe"]
                               and mo["MaxDD"] >= DD_CAP * spy["oos"]["MaxDD"]
                               and mo["CAGR"] >= CAGR_FLOOR * spy["oos"]["CAGR"])
                    rows.append(dict(
                        panel=pname, cadence=cad, gross=gross, cost=c,
                        trades=int(m[WARMUP:].sum()), turn_py=float(t0.sum() / yrs),
                        gross_real=float(gs.mean()),
                        CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
                        is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
                        is_H1=ih1, is_H2=ih2,
                        oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                        **{k: v for k, v in mar.items()},
                        bind=bl, n_fail=nbad,
                        keep4b_full=bool(k4b_full), keep4b_oos=bool(k4b_oos),
                        keep4b=bool(k4b_full and mar["L3_OOS"] > 0 and k4b_oos),
                        keep4a=bool(h1 > LV["h1"] and h2 > LV["h2"]
                                    and mf["MaxDD"] >= LV["full"]["MaxDD"]),
                        keep4a_oos=bool(mo["Sharpe"] > LV["oos"]["Sharpe"]
                                        and mo["MaxDD"] >= LV["oos"]["MaxDD"]),
                    ))
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}_grid.csv", index=False)
    gate("G8 every cell published", f"{len(df)} rows -> {Path(OUT).name}_grid.csv",
         f"{len(PX)*len(GROSSES)*len(CADENCES)*len(COSTS)}",
         len(df) == len(PX) * len(GROSSES) * len(CADENCES) * len(COSTS))

    # ---- G3 CROSS-RUN against idea 1761's committed CAL cells ------------------------
    ref = ROOT / "research" / "backtests" / "2026-09-20_band-credit-looking-or-trading_cloud_grid.csv"
    if ref.exists():
        old = pd.read_csv(ref).query("kind=='CAL' and gross==1.0 and cost==10")
        mx, n = 0.0, 0
        for _, o in old.iterrows():
            q = df[(df.panel == o.panel) & (df.cadence == o.label) & (df.gross == 1.0) & (df.cost == 10)]
            if len(q) != 1:
                continue
            q = q.iloc[0]
            n += 1
            for a, b in (("CAGR", "CAGR"), ("Sharpe", "Sharpe"), ("MaxDD", "MaxDD"), ("H1", "H1"),
                         ("H2", "H2"), ("oos_CAGR", "oos_CAGR"), ("oos_Sharpe", "oos_Sharpe"),
                         ("oos_MaxDD", "oos_MaxDD"), ("turn_py", "turn_py"),
                         ("gross_real", "gross_real")):
                mx = max(mx, abs(float(o[a]) - float(q[b])))
        gate("G3 cross-run vs idea 1761 CAL cells", f"{n} cells, max|d| = {mx:.3e}", "< 1e-9",
             n == 12 and mx < 1e-9)
    else:
        gate("G3 cross-run vs idea 1761", "reference grid absent", "present", False)

    # ---- headline: the ladder at gross 1.00, 10 bps ----------------------------------
    log("")
    log(f"## THE LADDER — band c={BAND}, gross 1.00, {COST0} bps, every rung's FULL and OOS legs")
    for pname in PX:
        S = BASE[pname]["spy"]
        log(f"\n### {pname}   SPY FULL {S['full']['CAGR']:.2%}/{S['full']['Sharpe']:.4f}/"
            f"{S['full']['MaxDD']:.2%} h {S['h1']:.4f}/{S['h2']:.4f} | SPY OOS "
            f"{S['oos']['CAGR']:.2%}/{S['oos']['Sharpe']:.4f}/{S['oos']['MaxDD']:.2%}")
        log(f"  {'cad':5s} {'trd/yr':>6s} {'CAGR':>7s} {'Shrp':>7s} {'MaxDD':>8s} {'H1':>7s} {'H2':>7s}"
            f" {'oCAGR':>7s} {'oShrp':>7s} {'oMaxDD':>8s} | {'L1_H1':>7s} {'L2_H2':>7s} {'L3_OOS':>7s}"
            f" {'L4_DD':>7s} {'L5_CAGR':>8s} | 4bF 4bO 4b 4a | binding")
        for cad in CADENCES:
            r = df[(df.panel == pname) & (df.cadence == cad) & (df.gross == 1.0) & (df.cost == COST0)].iloc[0]
            log(f"  {cad:5s} {r.turn_py:6.2f} {r.CAGR:7.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} "
                f"{r.H1:7.4f} {r.H2:7.4f} {r.oos_CAGR:7.2%} {r.oos_Sharpe:7.4f} {r.oos_MaxDD:8.2%} | "
                f"{r.L1_H1:+7.4f} {r.L2_H2:+7.4f} {r.L3_OOS:+7.4f} {100*r.L4_DD:+6.2f}p "
                f"{100*r.L5_CAGR:+7.2f}p | {'Y' if r.keep4b_full else '.':^3s} "
                f"{'Y' if r.keep4b_oos else '.':^3s} {'Y' if r.keep4b else '.':^2s} "
                f"{'Y' if r.keep4a else '.':^2s} | {r.bind}")

    # ---- the ladder's shape: cost and gross robustness --------------------------------
    log("")
    log("## 4b (all five legs) PASS SET by cadence, over the reported gross x cost axes")
    for pname in PX:
        for gross in GROSSES:
            s = []
            for cad in CADENCES:
                q = df[(df.panel == pname) & (df.cadence == cad) & (df.gross == gross)]
                s.append(f"{cad}:{int(q.keep4b.sum())}/{len(q)}")
            log(f"  {pname:6s} g={gross:.2f}  " + "  ".join(s) + "   (count of the 4 cost rungs passing full 4b)")

    log("")
    log("## BINDING-LEG CENSUS over all 144 cells (a leg is BINDING when it fails)")
    tot = {k: int((~(df[k] > 0)).sum()) for k in LEGS}
    log("  " + "  ".join(f"{k} {v}" for k, v in tot.items()) + f"   of {len(df)} cells")
    for cad in CADENCES:
        q = df[df.cadence == cad]
        log(f"  {cad:5s} " + "  ".join(f"{k} {int((~(q[k]>0)).sum()):2d}" for k in LEGS)
            + f"   4b pass {int(q.keep4b.sum()):2d}/{len(q)}")

    # ---- RULE 8: choose the cadence IN SAMPLE, read 2017-2026 once --------------------
    log("")
    log("## RULE 8 — the cadence chosen on 2009-2016 only, evaluated on 2017-2026 read ONCE")
    log("   choosers are IS-only by construction: every statistic is computed on r.loc[:2016-12-31]")
    gate("G7 chooser window", "all chooser statistics from r.loc[:%s]" % IS_END,
         "no row >= " + OOS_START, True)
    CH = {"C_ISSHARPE": lambda q: q.is_Sharpe,
          "C_ISCALMAR": lambda q: q.is_CAGR / q.is_MaxDD.abs(),
          "C_ISLEGS": None}   # filled per panel below: IS 4b leg count, IS Sharpe as tie-break
    ch_rows = []
    for pname in PX:
        S, LV = BASE[pname]["spy"], BASE[pname][f"live{COST0}"]
        for gross in GROSSES:
            sub = df[(df.panel == pname) & (df.gross == gross) & (df.cost == COST0)
                     & (df.cadence.isin(HEAD))]
            oracle = sub.loc[sub.oos_Sharpe.idxmax()]
            SI = BASE[pname]["spy"]["is_"]
            sh1, sh2 = halves(BASE[pname]["spy_r"].loc[:IS_END])
            CH["C_ISLEGS"] = lambda q, SI=SI, sh1=sh1, sh2=sh2: (
                (q.is_H1 > sh1).astype(int) + (q.is_H2 > sh2).astype(int)
                + (q.is_Sharpe > SI["Sharpe"]).astype(int)
                + (q.is_MaxDD >= DD_CAP * SI["MaxDD"]).astype(int)
                + (q.is_CAGR >= CAGR_FLOOR * SI["CAGR"]).astype(int)
                + q.is_Sharpe / 1e6)
            for cname, f in CH.items():
                pick = sub.loc[f(sub).idxmax()]
                ch_rows.append(dict(panel=pname, gross=gross, chooser=cname, pick=pick.cadence,
                                    oos_CAGR=pick.oos_CAGR, oos_Sharpe=pick.oos_Sharpe,
                                    oos_MaxDD=pick.oos_MaxDD, keep4b_oos=bool(pick.keep4b_oos),
                                    keep4b=bool(pick.keep4b), keep4a_oos=bool(pick.keep4a_oos),
                                    oracle=oracle.cadence, oracle_oos_Sharpe=oracle.oos_Sharpe))
            for tag, pick in (("C_CANON_W", sub[sub.cadence == "W"].iloc[0]),
                              ("C_ORACLE_OOS", oracle)):
                ch_rows.append(dict(panel=pname, gross=gross, chooser=tag, pick=pick.cadence,
                                    oos_CAGR=pick.oos_CAGR, oos_Sharpe=pick.oos_Sharpe,
                                    oos_MaxDD=pick.oos_MaxDD, keep4b_oos=bool(pick.keep4b_oos),
                                    keep4b=bool(pick.keep4b), keep4a_oos=bool(pick.keep4a_oos),
                                    oracle=oracle.cadence, oracle_oos_Sharpe=oracle.oos_Sharpe))
    ch = pd.DataFrame(ch_rows)
    ch.to_csv(f"{OUT}_choosers.csv", index=False)
    for pname in PX:
        S, LV = BASE[pname]["spy"], BASE[pname][f"live{COST0}"]
        log(f"\n  {pname}  vs LIVE RULES v2 OOS {LV['oos']['CAGR']:.2%}/{LV['oos']['Sharpe']:.4f}/"
            f"{LV['oos']['MaxDD']:.2%}  and SPY OOS {S['oos']['CAGR']:.2%}/{S['oos']['Sharpe']:.4f}/"
            f"{S['oos']['MaxDD']:.2%}")
        for _, r in ch[ch.panel == pname].iterrows():
            log(f"    g={r.gross:.2f} {r.chooser:13s} -> {r['pick']:5s}  OOS {r.oos_CAGR:7.2%} / "
                f"{r.oos_Sharpe:7.4f} / {r.oos_MaxDD:8.2%}   4bOOS {'Y' if r.keep4b_oos else '.'}"
                f"  4b(all legs) {'Y' if r.keep4b else '.'}  4aOOS {'Y' if r.keep4a_oos else '.'}")
    legal = ch[ch.chooser.str.startswith("C_IS")]
    log(f"\n  legal IS-only picks clearing 4b OOS: {int(legal.keep4b_oos.sum())} of {len(legal)};"
        f"  clearing full 4b (all five legs): {int(legal.keep4b.sum())} of {len(legal)};"
        f"  clearing 4a OOS: {int(legal.keep4a_oos.sum())} of {len(legal)}")

    # ---- verdict ---------------------------------------------------------------------
    log("")
    u = df[(df.panel == "U56") & (df.gross == 1.0) & (df.cost == COST0) & (df.cadence.isin(HEAD))]
    passing = list(u[u.keep4b].cadence)
    log(f"## VERDICT INPUT — U56, gross 1.00, {COST0} bps: full-4b passing rungs = {passing} "
        f"of {HEAD}")
    ok = sum(1 for g in _gates if g["pass_"])
    log(f"\n# GATES {ok} of {len(_gates)} PASS")
    pd.DataFrame(_gates).to_csv(f"{OUT}_gates.csv", index=False)
    Path(f"{OUT}.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
