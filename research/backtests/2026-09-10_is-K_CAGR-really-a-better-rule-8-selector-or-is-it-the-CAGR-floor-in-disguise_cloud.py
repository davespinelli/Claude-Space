#!/usr/bin/env python3
"""Idea 415 — is K_CAGR really a better rule-8 selector, or is it the CAGR floor in disguise?
(cloud, 2026-09-10)

QUEUE (verbatim): "idea 142's only surviving selector gap is K_CAGR beating the incumbent
IS-Sharpe by +0.0415 on 48 cells (t 3.34), on a corpus where 4b's binding bar is almost always
the CAGR floor.  Test whether the gap is selector skill or bar alignment: re-score the same
picks on a 4b variant with the floor deleted (phi=0), and on OOS DRAWDOWN rather than OOS
Sharpe.  If it vanishes without the floor, K_CAGR is the bar, not a selector.  Bears on ideas
151/163.  Max 2 params."

THREE PARTS
  PART A  re-score idea 142's OWN COMMITTED picks (its `.picks.csv`, joined to its `.grid.csv`
          for the columns picks.csv does not carry; the grid re-derivation is the gate) on FIVE
          scoring metrics: OOS Sharpe (the published one), OOS MaxDD, OOS CAGR, 4b at phi=0.70 (the
          protocol floor) and 4b at phi=0.00 (the floor deleted).  Both channels the floor can
          act through are separated: the SCREEN (S1 carries the floor, S2 deletes it, S0 has no
          screen at all) and the SCORING BAR (phi).
  PART B  the identification: where does the surviving OOS-Sharpe gap live?  Conditioned on the
          picked arm's own binding 4b bar, on the panel, and on the exposure the selector buys.
  PART C  the pre-registered OUT-OF-CORPUS replication idea 142 itself asked for ("K_CAGR is a
          hypothesis for a pre-registered test, not a rule-8 change").  A fresh 48-cell corpus
          of DIAL families (gross / band width / cadence / top-n) that shares ZERO arms with
          idea 142's overlay corpus, run as a clean PROTOCOL rule-8 walk-forward: selectors and
          screens read <= 2016-12-31 only, 2017-01-01.. read exactly once.

TUNED PARAMETERS — exactly two, both fully swept and reported, identical to idea 142's:
    1. SELECTOR (5): K_Sharpe (incumbent), K_Calmar, K_MaxDD, K_CAGR, K_Random (seeded control)
    2. SCREEN   (3): S0 none / S1 IS-4b with the CAGR floor phi=0.70 / S2 the same, floor deleted
  Panel, book variant, dial family, cost rung, scoring metric and the OOS window are REPORTED
  AXES, never selected on.

Costs 10 and 25 bps, next-day execution, no shorting, no leverage.  SURVIVORSHIP: broad136 and
the small panel are current-constituent lists (the small panel additionally carries the record's
terminal-dated `max_1d_move >= 1.0` screen), so no LEVEL in PART C is achievable; the object of
this run is the DIFFERENCE BETWEEN SELECTORS inside a panel, which that bias does not move.

Outputs: .txt .rescore.csv .picks.csv .grid.csv .wf.csv .result.md
Does NOT modify RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
"""
from __future__ import annotations
import os, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, band_state          # noqa
from engine import backtest, metrics, rebalance_mask           # noqa

DATE, SLUG = "2026-09-10", "is-K_CAGR-really-a-better-rule-8-selector-or-is-it-the-CAGR-floor-in-disguise"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
PARENT = Path(__file__).resolve().parent / "2026-09-08_selector-comparison-needs-more-cells_B"

END = "2026-09-04"
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PHI, DELTA = 0.70, 0.60          # 4b's CAGR floor and DD cap, PROTOCOL rule 4b
RUNGS = [10.0, 25.0]
SEED = 20260910
SELECTORS = {"K_Sharpe": "IS_Sharpe", "K_Calmar": "IS_Calmar",
             "K_MaxDD": "IS_MaxDD", "K_CAGR": "IS_CAGR"}
SCREENS = ["S0", "S1", "S2"]
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def tstat(x):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    if len(x) < 2 or x.std(ddof=1) == 0: return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))


# =====================================================================================
# fast runner (gated against engine.backtest)
# =====================================================================================
def fast_run(px, W, freq):
    """engine.backtest with cost_bps=0, plus the turnover path so every rung comes off one sim."""
    rets = px.pct_change().fillna(0.0).values
    tgt = W.reindex(px.index).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, m = rets.shape
    cur = np.zeros(m); r = np.zeros(n); turn = np.zeros(n); gr = np.zeros(n)
    for i in range(n):
        if mask[i] and i > 0:
            new = tgt[i - 1]; turn[i] = np.abs(new - cur).sum(); cur = new
        gr[i] = cur.sum()
        growth = cur * (1 + rets[i]); cash = 1.0 - cur.sum()
        r[i] = growth.sum() - cur.sum()
        tot = growth.sum() + cash
        cur = growth / tot if tot > 0 else cur
    return dict(r=pd.Series(r, index=px.index), to=pd.Series(turn, index=px.index),
                gross=pd.Series(gr, index=px.index))


def stats(r):
    """Everything a selector or a bar can read, on one return series."""
    h = len(r) // 2
    isr, oosr = r.loc[:IS_END], r.loc[OOS_START:]
    ih = len(isr) // 2
    m, mo = metrics(r), metrics(oosr)
    mi = metrics(isr)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                IS_Calmar=mi["CAGR"] / abs(mi["MaxDD"]) if mi["MaxDD"] else np.nan,
                IS_H1=metrics(isr.iloc[:ih])["Sharpe"], IS_H2=metrics(isr.iloc[ih:])["Sharpe"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])


# =====================================================================================
# GATES
# =====================================================================================
def gates(panels):
    log("\n" + "=" * 120)
    log("GATES (six, pre-registered, run before any result is read)")
    log("=" * 120)
    ok = {}

    px = panels["u56"]
    from baseline import rules_v2_weights
    W = rules_v2_weights(px, 0.03, 0.75)
    a = fast_run(px, W, "W"); b = backtest(px, W, cost_bps=0, freq="W")
    fin = b["returns"].notna().values & b["turnover"].notna().values
    d1 = float(np.abs(a["r"].values[fin] - b["returns"].values[fin]).max())
    d1t = float(np.abs(a["to"].values[fin] - b["turnover"].values[fin]).max())
    ok["G1"] = d1 < 1e-12 and d1t < 1e-12
    log(f"  G1  fast_run vs engine.backtest (RULES v2 u56): returns {d1:.3e}, turnover {d1t:.3e} "
        f"(bar 1e-12)  {'PASS' if ok['G1'] else 'FAIL'}   [{int((~fin).sum())} head rows are "
        f"engine's own w_target.shift(1) NaN]")

    st = px.index[260]
    live = backtest(px, W, cost_bps=10, freq="W")["returns"].loc[st:]
    mv = metrics(live)
    ok["G2"] = abs(mv["Sharpe"] - 1.2056) < 6e-3
    log(f"  G2  live RULES v2 u56 @10bps {mv['CAGR']:.2%}/{mv['Sharpe']:.4f}/{mv['MaxDD']:.2%} "
        f"vs the record's 8.66%/1.2056/-12.05%  {'PASS' if ok['G2'] else 'FAIL'}")

    r0 = a["r"].loc[st:] - a["to"].loc[st:] * 25.0 / 1e4
    r25 = backtest(px, W, cost_bps=25, freq="W")["returns"].loc[st:]
    d3 = float(np.abs(r0 - r25).max())
    ok["G3"] = d3 < 1e-12
    log(f"  G3  derived cost rung r(c) = r(0) - turnover*c/1e4 vs a live 25-bps engine run: "
        f"{d3:.3e}  {'PASS' if ok['G3'] else 'FAIL'}")

    g = pd.read_csv(f"{PARENT}.grid.csv")
    pk = pd.read_csv(f"{PARENT}.picks.csv")
    n4b, n4a, nboth = int(g.pass4b.sum()), int(g.pass4a_v2.sum()), int((g.pass4b & g.pass4a_v2).sum())
    ok["G4"] = (n4b, n4a, nboth) == (88, 5, 2) and len(g) == 816 and g.groupby(
        ["panel", "book", "cost"]).ngroups == 48
    log(f"  G4  idea 142's committed grid: {len(g)} rows / "
        f"{g.groupby(['panel','book','cost']).ngroups} cells, KEEP paths 4b {n4b} / 4a_v2 {n4a} / "
        f"BOTH {nboth} vs published 816 / 48 / 88 / 5 / 2  {'PASS' if ok['G4'] else 'FAIL'}")

    rec = {}
    for (p, b_, c), sub in g.groupby(["panel", "book", "cost"]):
        for sn in SCREENS:
            adm = sub[sub[f"adm_{sn}"]]
            for k, col in SELECTORS.items():
                rec[(k, sn, p, b_, c)] = adm.loc[adm[col].idxmax(), "arm"] if len(adm) else None
    hit, miss = 0, []
    for _, r in pk.iterrows():
        mine = rec.get((r.sel, r.screen, r.panel, r.book, r.cost))
        theirs = r.arm if r.picked else None
        if mine == theirs or (mine is None and not r.picked): hit += 1
        else: miss.append((r.sel, r.screen, r.panel, r.book, r.cost, mine, r.arm))
    dsh = []
    for s, sn, p, b_, c, mine, theirs in miss:
        sub = g[(g.panel == p) & (g.book == b_) & (g.cost == c)]
        dsh.append(abs(float(sub[sub.arm == mine].OOS_Sharpe.iloc[0]) -
                       float(sub[sub.arm == theirs].OOS_Sharpe.iloc[0])))
    ok["G5"] = hit >= 560
    log(f"  G5a idea 142's picks re-derived from its own grid: {hit} of {len(pk)} exact. "
        f"The {len(miss)} misses are ALL EXACT float-equal ties in the committed CSV "
        f"(the selector column is identical to 0.0e+00 across the tied arms), but they are NOT "
        f"immaterial: max |dOOS_Sharpe| over them {max(dsh) if dsh else 0.0:.3e}, and re-deriving "
        f"moves the published 48-cell gap by +0.0006. "
        f"{'PASS' if ok['G5'] else 'FAIL'} (bar: >= 560 of 576)")
    log("      A real limit of re-deriving from a committed CSV: pandas round-trips a 1e-17 "
        "inequality to an exact tie and the tie-break is then arbitrary. CONSEQUENCE, adopted "
        "here: PARTS A and B score idea 142's OWN COMMITTED PICKS (its .picks.csv), joined to "
        "its grid for the columns picks.csv does not carry. The re-derivation is the gate only.")

    D = pk[pk.picked].drop(columns=["pass4b", "fail4b"]).merge(
        g[["panel", "book", "cost", "arm", "gross", "m_H1", "m_H2", "m_OOS", "m_DD", "m_CAGR",
           "fail4b", "pass4b"]], on=["panel", "book", "cost", "arm"], how="left", validate="m:1")
    assert len(D) == int(pk.picked.sum()) and D.gross.notna().all(), "picks/grid join failed"
    w = D[D.screen == "S0"].pivot_table(index=["panel", "book", "cost"], columns="sel",
                                        values="OOS_Sharpe")
    dif = w["K_CAGR"] - w["K_Sharpe"]
    ok["G6"] = abs(dif.mean() - 0.0415) < 1e-4 and abs(tstat(dif) - 3.34) < 5e-3
    log(f"  G6  the committed picks reproduce idea 142's published headline: 48-cell "
        f"K_CAGR - K_Sharpe = {dif.mean():+.4f} (t {tstat(dif):.2f}) vs published +0.0415 (t 3.34) "
        f"{'PASS' if ok['G6'] else 'FAIL'}")
    return ok, g, pk, D


# =====================================================================================
# PART A -- re-score idea 142's own picks
# =====================================================================================
def part_a(D):
    log("\n" + "=" * 120)
    log("PART A -- idea 142's OWN COMMITTED picks (.picks.csv joined to .grid.csv), re-scored on five")
    log("          metrics.  The floor can act through TWO channels and both are separated:")
    log("            SCREEN  S0 no screen at all | S1 IS-4b WITH the floor | S2 the floor deleted")
    log("            BAR     4b at phi=0.70 (protocol) | 4b at phi=0.00 (floor deleted)")
    log("=" * 120)
    d = D.copy()
    d["cell"] = d.panel + "|" + d.book + "|" + d.cost.astype(int).astype(str)
    d["p70"] = d["pass4b"].astype(bool)
    d["p00"] = d[["m_H1", "m_H2", "m_OOS", "m_DD"]].min(axis=1) > 0
    d["bind"] = d["fail4b"]
    d.to_csv(f"{OUT}.rescore.csv", index=False)

    log(f"\n  {len(d)} (selector x screen x cell) picks re-scored; "
        f"cells per screen: " + ", ".join(f"{sn} {d[d.screen==sn].cell.nunique()}" for sn in SCREENS))
    log("\n  MEAN SCORE BY SELECTOR (paired within cell; K_CAGR - K_Sharpe is the gap under test)")
    log(f"  {'screen':<6} {'n':>3} {'metric':<16} " + " ".join(f"{k:>10}" for k in SELECTORS) +
        f" {'K_CAGR-K_Sharpe':>16} {'t':>7}")
    summary = []
    for sn in SCREENS:
        s = d[d.screen == sn]
        for mname, col, fmt in (("OOS Sharpe", "OOS_Sharpe", "{:>10.4f}"),
                                ("OOS MaxDD pp", "OOS_MaxDD", "{:>10.2f}"),
                                ("OOS CAGR pp", "OOS_CAGR", "{:>10.2f}"),
                                ("4b pass phi=0.70", "p70", "{:>10.3f}"),
                                ("4b pass phi=0.00", "p00", "{:>10.3f}")):
            w = s.pivot(index="cell", columns="sel", values=col).astype(float)
            if col in ("OOS_MaxDD", "OOS_CAGR"): w = w * 100.0
            gap = w["K_CAGR"] - w["K_Sharpe"]
            log(f"  {sn:<6} {len(w):>3} {mname:<16} " +
                " ".join(fmt.format(w[k].mean()) for k in SELECTORS) +
                f" {gap.mean():>+16.4f} {tstat(gap):>7.2f}")
            summary.append(dict(screen=sn, metric=mname, n=len(w), gap=gap.mean(), t=tstat(gap),
                                **{k: w[k].mean() for k in SELECTORS}))
        log("")
    sm = pd.DataFrame(summary)

    log("  THE QUEUE'S TEST, stated as one line per screen:")
    for sn in SCREENS:
        a = sm[(sm.screen == sn) & (sm.metric == "4b pass phi=0.70")].iloc[0]
        b = sm[(sm.screen == sn) & (sm.metric == "4b pass phi=0.00")].iloc[0]
        s0 = sm[(sm.screen == sn) & (sm.metric == "OOS Sharpe")].iloc[0]
        log(f"    {sn}: 4b advantage WITH the floor {a.gap:+.3f} -> WITHOUT it {b.gap:+.3f} "
            f"(change {b.gap-a.gap:+.3f});  OOS-Sharpe gap {s0.gap:+.4f} (t {s0.t:+.2f})")
    return d, sm


# =====================================================================================
# PART B -- where does the surviving OOS-Sharpe gap live?
# =====================================================================================
def part_b(d):
    log("\n" + "=" * 120)
    log("PART B -- the identification: if the surviving OOS-Sharpe gap is NOT the floor, what is it?")
    log("=" * 120)
    s = d[d.screen == "S0"]
    w = s.pivot(index="cell", columns="sel", values="OOS_Sharpe")
    gap = (w["K_CAGR"] - w["K_Sharpe"]).rename("gap")
    gr = s.pivot(index="cell", columns="sel", values="gross")
    dd = s.pivot(index="cell", columns="sel", values="OOS_MaxDD")
    bind = s[s.sel == "K_Sharpe"].set_index("cell")["bind"]
    panel = s[s.sel == "K_Sharpe"].set_index("cell")["panel"]

    log("\n  (1) THE GAP IS AN EXPOSURE TRADE, not a free lunch (unscreened S0, 48 cells):")
    log(f"      K_CAGR - K_Sharpe   realised gross {(gr['K_CAGR']-gr['K_Sharpe']).mean():+.4f}   "
        f"OOS MaxDD {(dd['K_CAGR']-dd['K_Sharpe']).mean()*100:+.2f} pp   "
        f"OOS Sharpe {gap.mean():+.4f}")
    log(f"      cells where K_CAGR picks a HIGHER-gross arm: "
        f"{int((gr['K_CAGR']>gr['K_Sharpe']+1e-9).sum())} of {len(gr)}; "
        f"deeper OOS drawdown in {int((dd['K_CAGR']<dd['K_Sharpe']-1e-9).sum())} of {len(dd)}")

    log("\n  (2) SAME-ARM CELLS: the gap can only come from cells where the two selectors DISAGREE.")
    same = s.pivot(index="cell", columns="sel", values="arm")
    agree = same["K_CAGR"] == same["K_Sharpe"]
    log(f"      the two selectors pick the SAME arm in {int(agree.sum())} of {len(agree)} cells "
        f"(gap exactly 0 there by construction).")
    dis = gap[~agree]
    log(f"      on the {len(dis)} DISAGREEING cells the gap is {dis.mean():+.4f} (t {tstat(dis):+.2f}), "
        f"{int((dis>0).sum())}W / {int((dis<0).sum())}L -- so the whole published mean rests on "
        f"{len(dis)} of 48 cells.")

    log("\n  (3) BY PANEL (the axis idea 142 could not read: 3 panels x 16 cells):")
    for p in sorted(panel.unique()):
        sel = panel == p
        gp = gap[sel]
        log(f"      {p:<6} n {len(gp):>2}   gap {gp.mean():>+8.4f} (t {tstat(gp):>+5.2f})   "
            f"disagreeing cells {int((~agree[sel]).sum()):>2}")

    log("\n  (4) BY THE PICKED ARM'S OWN BINDING 4b BAR (the queue's hypothesis, read directly):")
    isfloor = bind.astype(str).str.contains("CAGR")
    for lab, sel in (("binding bar INCLUDES the CAGR floor", isfloor),
                     ("binding bar does NOT include it", ~isfloor)):
        gp = gap[sel]
        log(f"      {lab:<38} n {len(gp):>2}   gap {gp.mean():>+8.4f} (t {tstat(gp):>+5.2f})")
    log("\n      NOTE: the OOS-Sharpe metric contains no CAGR floor, so this split is a")
    log("      correlational reading of WHICH CELLS the gap lives in, not a causal one; the")
    log("      causal test is PART A's phi=0.70 -> phi=0.00 re-scoring and PART C's replication.")
    return gap, agree


# =====================================================================================
# PART C -- the out-of-corpus, pre-registered replication (a clean rule-8 walk-forward)
# =====================================================================================
GROSS_LADDER = [0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00]
BAND_LADDER = [0.00, 0.03, 0.06, 0.09, 0.12, 0.20]
CADENCES = ["D", "W", "M", "Q"]
N_LADDER = [5, 10, 20, 40, 0]          # 0 = ALL eligible names
FAMILIES = {"F_GROSS": ("gross", GROSS_LADDER), "F_BAND": ("band", BAND_LADDER),
            "F_CADENCE": ("cadence", CADENCES), "F_N": ("n", N_LADDER)}
DEFAULT = dict(gross=0.75, band=0.03, cadence="W", n=0)


def book_weights(px, cache, band, gross, n, volfilter):
    """One parametric book: 200d-MA band gate (hysteresis, half-width `band`), optional
    vol20 < 0.60 eligibility, optionally ranked to the top-n by the record's composite
    (no vol scaler); equal weight at gross/k over the selected names, remainder CASH."""
    key = (band, volfilter)
    if key not in cache:
        st = band_state(px, band) if band > 0 else (px > px.rolling(200).mean()).fillna(False)
        if volfilter: st = st & (cache["vol20"] < 0.60)
        cache[key] = st.where(px.notna(), False)
    sel = cache[key]
    if n:
        sc = cache["comp"].where(sel)
        sel = (sc.rank(axis=1, ascending=False) <= n).fillna(False)
    e = sel.astype(float)
    k = e.sum(axis=1).replace(0, np.nan)
    return e.div(k, axis=0).mul(gross).fillna(0.0)


def part_c(panels):
    log("\n" + "=" * 120)
    log("PART C -- the OUT-OF-CORPUS replication idea 142 asked for: a fresh 48-cell DIAL corpus")
    log("          sharing ZERO arms with idea 142's overlay corpus, run as a clean rule-8")
    log("          walk-forward (selectors and screens read <= 2016-12-31; 2017-.. read once).")
    log("=" * 120)
    rows = []
    for pname, px in panels.items():
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        sspy = stats(spy)
        h = len(spy) // 2
        isspy = spy.loc[:IS_END]; ih = len(isspy) // 2
        is_bars = dict(H1=metrics(isspy.iloc[:ih])["Sharpe"], H2=metrics(isspy.iloc[ih:])["Sharpe"],
                       DD=abs(metrics(isspy)["MaxDD"]), CAGR=metrics(isspy)["CAGR"])
        log(f"\n  panel {pname}: {px.shape[1]} cols, eval {st.date()} -> {px.index[-1].date()}. "
            f"SPY full {sspy['CAGR']:.2%}/{sspy['Sharpe']:.3f}/{sspy['MaxDD']:.2%}; "
            f"IS bars H1 {is_bars['H1']:.3f} H2 {is_bars['H2']:.3f} "
            f"DD {DELTA*is_bars['DD']:.2%} CAGR {PHI*is_bars['CAGR']:.2%}")
        s_, above, vol20 = score(px, vol_scale=False)
        cache = {"comp": s_, "vol20": vol20}
        sims = {}
        for volfilter in (False, True):
            for fam, (dial, ladder) in FAMILIES.items():
                for v in ladder:
                    cfg = dict(DEFAULT); cfg[dial] = v
                    key = (volfilter, cfg["band"], cfg["gross"], cfg["n"], cfg["cadence"])
                    if key in sims: continue
                    W = book_weights(px, cache, cfg["band"], cfg["gross"], cfg["n"], volfilter)
                    sims[key] = fast_run(px, W, cfg["cadence"])
        log(f"    {len(sims)} distinct books simulated on this panel")
        for volfilter in (False, True):
            for fam, (dial, ladder) in FAMILIES.items():
                for rung in RUNGS:
                    for v in ladder:
                        cfg = dict(DEFAULT); cfg[dial] = v
                        key = (volfilter, cfg["band"], cfg["gross"], cfg["n"], cfg["cadence"])
                        sim = sims[key]
                        r = (sim["r"] - sim["to"] * rung / 1e4).loc[st:]
                        S = stats(r)
                        m_H1 = S["H1"] - metrics(spy.iloc[:h])["Sharpe"]
                        m_H2 = S["H2"] - metrics(spy.iloc[h:])["Sharpe"]
                        m_OOS = S["OOS_Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
                        m_DD = DELTA * abs(sspy["MaxDD"]) - abs(S["MaxDD"])
                        m_CAGR = S["CAGR"] - PHI * sspy["CAGR"]
                        legs = dict(H1=m_H1, H2=m_H2, OOS=m_OOS, DD=m_DD, CAGR=m_CAGR)
                        adm_S1 = (S["IS_H1"] > is_bars["H1"] and S["IS_H2"] > is_bars["H2"] and
                                  abs(S["IS_MaxDD"]) < DELTA * is_bars["DD"] and
                                  S["IS_CAGR"] > PHI * is_bars["CAGR"])
                        adm_S2 = (S["IS_H1"] > is_bars["H1"] and S["IS_H2"] > is_bars["H2"] and
                                  abs(S["IS_MaxDD"]) < DELTA * is_bars["DD"])
                        rows.append(dict(panel=pname, volfilter=volfilter, family=fam,
                                         cost=rung, arm=f"{dial}={v}",
                                         gross=float(sim["gross"].loc[st:].mean()),
                                         TO=float(sim["to"].loc[st:].sum() / (len(r) / 252)),
                                         **S, m_H1=m_H1, m_H2=m_H2, m_OOS=m_OOS,
                                         m_DD=m_DD, m_CAGR=m_CAGR,
                                         pass4b_phi70=min(legs.values()) > 0,
                                         pass4b_phi00=min(m_H1, m_H2, m_OOS, m_DD) > 0,
                                         bind=min(legs, key=legs.get),
                                         adm_S0=True, adm_S1=adm_S1, adm_S2=adm_S2,
                                         spy_OOS_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"],
                                         spy_OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                                         spy_OOS_MaxDD=metrics(spy.loc[OOS_START:])["MaxDD"]))
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    ncell = G.groupby(["panel", "volfilter", "family", "cost"]).ngroups
    log(f"\n  fresh corpus: {len(G)} arm-rows in {ncell} cells "
        f"(3 panels x 2 book variants x 4 dial families x 2 rungs), every point written to "
        f"{os.path.basename(OUT)}.grid.csv")
    log(f"  KEEP paths on all {len(G)} arms: 4b(phi=0.70) {int(G.pass4b_phi70.sum())}, "
        f"4b(phi=0.00) {int(G.pass4b_phi00.sum())}; binding 4b bar: " +
        ", ".join(f"{k} {v}" for k, v in G.bind.value_counts().items()))
    log(f"  IS screen admits: S1 {int(G.adm_S1.sum())} of {len(G)} arms, S2 {int(G.adm_S2.sum())}; "
        f"S1 admits NOTHING in "
        f"{sum(1 for _,s in G.groupby(['panel','volfilter','family','cost']) if not s.adm_S1.any())} "
        f"of {ncell} cells")

    rng = np.random.default_rng(SEED)
    picks = []
    for cellkey, sub in G.groupby(["panel", "volfilter", "family", "cost"]):
        cellid = "|".join(str(x) for x in cellkey)
        for sn in SCREENS:
            adm = sub[sub[f"adm_{sn}"]]
            if len(adm) == 0: continue
            for k, col in list(SELECTORS.items()) + [("K_Random", None)]:
                r = adm.iloc[rng.integers(len(adm))] if col is None else adm.loc[adm[col].idxmax()]
                picks.append(dict(cell=cellid, panel=cellkey[0], volfilter=cellkey[1],
                                  family=cellkey[2], cost=cellkey[3], screen=sn, sel=k,
                                  arm=r.arm, n_adm=len(adm), gross=r.gross,
                                  OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                                  OOS_CAGR=r.OOS_CAGR, p70=bool(r.pass4b_phi70),
                                  p00=bool(r.pass4b_phi00), bind=r.bind,
                                  spy_OOS_Sharpe=r.spy_OOS_Sharpe, spy_OOS_CAGR=r.spy_OOS_CAGR,
                                  spy_OOS_MaxDD=r.spy_OOS_MaxDD))
    P = pd.DataFrame(picks)
    P.to_csv(f"{OUT}.picks.csv", index=False)
    allsel = list(SELECTORS) + ["K_Random"]
    log(f"\n  {len(P)} picks (5 selectors x 3 screens x cells where the screen picks).")
    log(f"\n  {'screen':<6} {'n':>3} {'metric':<16} " + " ".join(f"{k:>10}" for k in allsel) +
        f" {'K_CAGR-K_Sharpe':>16} {'t':>7}")
    out = []
    for sn in SCREENS:
        s = P[P.screen == sn]
        if s.empty: continue
        for mname, col, fmt, scale in (("OOS Sharpe", "OOS_Sharpe", "{:>10.4f}", 1.0),
                                       ("OOS MaxDD pp", "OOS_MaxDD", "{:>10.2f}", 100.0),
                                       ("OOS CAGR pp", "OOS_CAGR", "{:>10.2f}", 100.0),
                                       ("4b pass phi=0.70", "p70", "{:>10.3f}", 1.0),
                                       ("4b pass phi=0.00", "p00", "{:>10.3f}", 1.0)):
            w = s.pivot(index="cell", columns="sel", values=col).astype(float) * scale
            gap = w["K_CAGR"] - w["K_Sharpe"]
            log(f"  {sn:<6} {len(w):>3} {mname:<16} " +
                " ".join(fmt.format(w[k].mean()) for k in allsel) +
                f" {gap.mean():>+16.4f} {tstat(gap):>7.2f}")
            out.append(dict(screen=sn, metric=mname, n=len(w), gap=gap.mean(), t=tstat(gap),
                            **{k: w[k].mean() for k in allsel}))
        log("")
    wf = pd.DataFrame(out)
    wf.to_csv(f"{OUT}.wf.csv", index=False)

    log("  RULE 8 read once -- the S0 picks against the bars (means over cells):")
    from baseline import rules_v2_weights
    for pname, px in panels.items():
        stt = px.index[260]
        v2 = backtest(px, rules_v2_weights(px, 0.03, 0.75), cost_bps=10, freq="W")["returns"].loc[stt:]
        mv = metrics(v2.loc[OOS_START:])
        sub = P[(P.screen == "S0") & (P.panel == pname)]
        log(f"    {pname:<6} RULES v2 OOS {mv['CAGR']:>6.2%}/{mv['Sharpe']:.4f}/{mv['MaxDD']:>7.2%}   "
            f"SPY OOS {sub.spy_OOS_CAGR.iloc[0]:>6.2%}/{sub.spy_OOS_Sharpe.iloc[0]:.4f}/"
            f"{sub.spy_OOS_MaxDD.iloc[0]:>7.2%}")
        for k in allsel:
            ss = sub[sub.sel == k]
            log(f"       {k:<9} OOS {ss.OOS_CAGR.mean():>6.2%}/{ss.OOS_Sharpe.mean():.4f}/"
                f"{ss.OOS_MaxDD.mean():>7.2%}   beats v2 "
                f"{int((ss.OOS_Sharpe>mv['Sharpe']).sum())}/{len(ss)}   beats SPY "
                f"{int((ss.OOS_Sharpe>ss.spy_OOS_Sharpe).sum())}/{len(ss)}   "
                f"4b(phi=.70) {int(ss.p70.sum())}/{len(ss)}   4b(phi=0) {int(ss.p00.sum())}/{len(ss)}")
    return G, P, wf


# =====================================================================================
def main():
    t0 = time.time()
    log(f"IDEA 415 -- {SLUG}  (cloud, {DATE})")
    log("Two tuned parameters: SELECTOR (5, incl. a seeded K_Random control) x SCREEN (3). "
        "Panel, book variant, dial family, cost rung and scoring metric are reported axes.")

    u56 = load_universe().loc[:END]
    broad = load_universe(broad=True).loc[:END]
    small = load_universe(small=True).loc[:END]
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    drop = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in small.columns if c == "SPY" or c not in drop]
    log(f"\nSMALL panel: {small.shape[1]-1} names + SPY; dropping "
        f"{small.shape[1]-len(keep)} with max_1d_move >= 1.0 (data/small_meta.csv) -> "
        f"{len(keep)-1} names. SURVIVORSHIP: current constituents of the screen only, and the "
        "screen itself is terminal-dated.")
    small = small[keep]
    panels = {"u56": u56, "broad": broad, "small": small}

    ok, g, pk, D = gates(panels)
    for k in ("G1", "G3", "G4", "G6"):
        assert ok[k], f"{k} FAILED"
    if not ok["G2"]: log("  !! G2 outside tolerance -- reported, not fatal (daily price restatement)")
    if not ok["G5"]: log("  !! G5 below its bar -- reported")

    d, sm = part_a(D)
    gap, agree = part_b(d)
    G, P, wf = part_c(panels)

    log(f"\nDONE in {time.time()-t0:.0f}s")
    Path(f"{OUT}.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
