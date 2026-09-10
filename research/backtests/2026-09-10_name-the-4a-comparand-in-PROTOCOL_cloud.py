#!/usr/bin/env python3
"""Idea 398 - "name-the-4a-comparand-in-PROTOCOL" (cloud lane).

What this run exists to settle
------------------------------
Idea 135's two independent runs agreed at 0.000e+00 on every performance column and disagreed on
`pass4a` for 116 of 748 rows, because one priced 4a against a locally rebuilt v1 book at a FIXED
10 bps and the other against `baseline.rules_v1_weights` at the ARM'S OWN cost rung.  PROTOCOL
rule 3 says "always compare against research/baseline.py: rules_v1_weights (the live paper rules)"
and rule 4a says "Sharpe > current live rules in BOTH halves and MaxDD no worse".  Since
2026-09-06 the live book is RULES v2, and `baseline.compare` judges 4a against v2 while rule 3's
text still names v1.  So "the current live rules" is under-specified in two independent ways:

    WHICH BOOK   v1 (rule 3's literal text) or v2 (the live book, and what compare() uses)
    WHICH RUNG   the comparand priced at the arm's own cost rung, or at a fixed 10 bps

This run measures what that ambiguity is worth, and proposes the one line that removes it.

Questions, stated so they can be answered either way
----------------------------------------------------
    Q1 (CENSUS)   How many committed files carry a 4a verdict, which comparand book do they
                  reference, and how many price that comparand at a FIXED rung while sweeping
                  more than one cost rung themselves (the idea-135 failure mode)?
    Q2 (SPREAD)   How far apart are the four comparands as bars?  Reported as each comparand's
                  own halves and MaxDD per panel per rung - the thing an arm is measured against.
    Q3 (FLIPS)    Re-price a pre-registered arm population under all four comparands and count
                  how many 4a verdicts move.  Idea 135's 116/748 = 15.5% is the number to beat
                  or refute.
    Q4 (WHICH LEG) When a 4a verdict moves, is it the Sharpe leg or the MaxDD leg that moves?
    Q5 (RULE 8)   Under a walk-forward chooser, does the comparand change WHICH ARM is kept, or
                  only how many pass?  A comparand that changes the count but not the pick is a
                  bookkeeping problem; one that changes the pick is a research problem.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. comparand  V2_MATCHED / V2_FIX10 / V1_MATCHED / V1_FIX10
    2. rung       0 / 10 / 25 bps
    12 grid points, ALL reported.

Reported axes, never tuned or selected on
    panel   U56 / B136 / SMALL439
    family  six dial families, pre-registered below, 21 arms per panel

Arm population (pre-registered before any verdict was read; every arm is a book the record
already trades in some file, not a search)
    NDIAL     top-n on the composite (no vol scaler), equal weight, gross 1.00, n in {5,10,20,30,40}
    GROSS     EWALL over the eligible set at gross in {0.50, 0.75, 1.00}
    BAND      RULES v2's 200d band at b in {0.01, 0.03, 0.05, 0.08, 0.16}, gross 0.75
    VOLCAP    RULES v1 with max_vol in {0.30, 0.45, 0.60, 0.90}
    CADENCE   CAND20 at weekly and monthly rebalance
    SCALER    RULES v1 with and without the 1/sqrt(vol) scaler
    = 21 arms x 3 panels x 3 rungs = 189 arm-rows, all reported.

Reproduction gates (section [0], printed before any new number is read)
    G1  derived cost rung r(c) = r(0) - turnover*c/1e4 vs a live engine.backtest(c).
    G2  the queue's own claim about v1's halves: 0.641/0.688 at 10 bps against 0.285/0.346 at
        25 bps.  Measured on all three panels; the panel it belongs to is named, not assumed.
    G3  U56/RULES v1 = 6.4194% / 0.66110 / -13.8278% (idea 486's published triple), vintage drift
        reported rather than hidden.
    G4  the 4a predicate itself: an arm compared against ITSELF passes 4a on every panel and rung
        (Sharpe strictly greater fails on a tie, so this gate is run with the PROTOCOL `>` on
        Sharpe and `>=` on MaxDD and must read FALSE/TRUE exactly as PROTOCOL's asymmetry says).

Data: committed caches only, no network.  SURVIVORSHIP: current-constituent panels, so levels are
optimistic; every number here is a comparand-vs-comparand contrast on one fixed arm population,
which that bias does not manufacture.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights, band_state
from engine import backtest, metrics

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

FREQ = "W"
MAX_VOL = 0.60
RUNGS = [0, 10, 25]
RUNG_HEAD = 10
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
COMPARANDS = ["V2_MATCHED", "V2_FIX10", "V1_MATCHED", "V1_FIX10"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 1500)

LINES = []


def log(s=""):
    print(s)
    LINES.append(str(s))


# ------------------------------------------------------------------ [1] census
def census():
    rows = []
    for f in sorted((REPO / "research").rglob("*.py")):
        t = f.read_text(errors="replace")
        if not re.search(r"p4a|pass4a|verdict_4a", t):
            continue
        # which comparand book does the file reference at all?
        v1 = "rules_v1_weights" in t
        v2 = "rules_v2_weights" in t
        # does the file sweep more than one cost rung?
        rungs = set(int(x) for x in re.findall(r"cost_bps\s*=\s*(\d+)", t))
        sweeps = bool(re.search(r"RUNGS\s*=\s*\[[^\]]*25", t)) or len(rungs) > 1
        # is any backtest call priced at a LITERAL rung (as opposed to a variable)?
        lit = bool(re.search(r"cost_bps\s*=\s*\d+", t))
        var = bool(re.search(r"cost_bps\s*=\s*[A-Za-z_]", t))
        rows.append(dict(file=f.name, ref_v1=v1, ref_v2=v2, sweeps_rungs=sweeps,
                         literal_cost=lit, variable_cost=var,
                         at_risk=bool(sweeps and lit and not var)))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ arms
def ewall_weights(px, gross):
    s, above, vol20 = score(px)
    e = (above & (vol20 < MAX_VOL)).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def candn_weights(px, n, gross=1.00):
    s, above, vol20 = score(px, vol_scale=False)
    elig = s.where(above & (vol20 < MAX_VOL))
    sel = (elig.rank(axis=1, ascending=False) <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(k, axis=0).mul(gross).fillna(0.0)


def band_weights(px, band, gross=0.75):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0)


def arms():
    """(family, name, weights_fn, freq) - pre-registered, never searched."""
    a = []
    for n in (5, 10, 20, 30, 40):
        a.append(("NDIAL", f"TOP{n}", lambda px, n=n: candn_weights(px, n), "W"))
    for g in (0.50, 0.75, 1.00):
        a.append(("GROSS", f"EWALL{g:.2f}", lambda px, g=g: ewall_weights(px, g), "W"))
    for b in (0.01, 0.03, 0.05, 0.08, 0.16):
        a.append(("BAND", f"BAND{b:.2f}", lambda px, b=b: band_weights(px, b), "W"))
    for v in (0.30, 0.45, 0.60, 0.90):
        a.append(("VOLCAP", f"VOLCAP{v:.2f}",
                  lambda px, v=v: rules_v1_weights(px, max_vol=v), "W"))
    a.append(("CADENCE", "CAND20-W", lambda px: candn_weights(px, 20), "W"))
    a.append(("CADENCE", "CAND20-M", lambda px: candn_weights(px, 20), "M"))
    a.append(("SCALER", "V1-SCALED", lambda px: rules_v1_weights(px, vol_scale=True), "W"))
    a.append(("SCALER", "V1-UNSCALED", lambda px: rules_v1_weights(px, vol_scale=False), "W"))
    return a


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def pack(r):
    h1, h2 = half_sharpes(r)
    return (h1, h2, metrics(r)["MaxDD"])


def pass_4a(arm_pack, cmp_pack):
    """PROTOCOL 4a: Sharpe strictly greater in BOTH halves, MaxDD no worse (>=, ties pass)."""
    return bool(arm_pack[0] > cmp_pack[0] and arm_pack[1] > cmp_pack[1]
                and arm_pack[2] >= cmp_pack[2])


def pass_4b(r, spy_pack):
    s1, s2, s_oos, s_dd, s_cagr = spy_pack
    m = metrics(r)
    h1, h2 = half_sharpes(r)
    legs = {"H1": h1 > s1, "H2": h2 > s2,
            "OOS": metrics(r.loc[OOS_START:])["Sharpe"] > s_oos,
            "DD": abs(m["MaxDD"]) <= 0.60 * abs(s_dd), "CAGR": m["CAGR"] >= 0.70 * s_cagr}
    return all(legs.values()), ",".join(k for k, v in legs.items() if not v) or "-"


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]], len(bad)


# ------------------------------------------------------------------ main
def main():
    log("=" * 170)
    log("IDEA 398  name-the-4a-comparand-in-PROTOCOL   (cloud lane)")
    log("=" * 170)

    log("\n[1] Q1 CENSUS - committed research/*.py carrying a 4a verdict")
    cen = census()
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)
    n = len(cen)
    log(f"  files with a 4a verdict: {n}")
    log(f"    reference rules_v1_weights only : {int((cen.ref_v1 & ~cen.ref_v2).sum())}")
    log(f"    reference rules_v2_weights only : {int((cen.ref_v2 & ~cen.ref_v1).sum())}")
    log(f"    reference BOTH                  : {int((cen.ref_v1 & cen.ref_v2).sum())}")
    log(f"    reference NEITHER (a local book): {int((~cen.ref_v1 & ~cen.ref_v2).sum())}")
    log(f"  files that sweep more than one cost rung: {int(cen.sweeps_rungs.sum())}")
    log(f"  AT RISK of idea 135's failure mode (sweeps rungs, every backtest call priced at a")
    log(f"  LITERAL cost, no variable rung anywhere): {int(cen.at_risk.sum())} "
        f"({cen.at_risk.mean():.1%} of files with a 4a verdict)")
    log("  at-risk files:")
    for f in cen[cen.at_risk]["file"]:
        log(f"    {f}")

    u56 = load_universe()
    b136 = load_universe(broad=True)
    small, ndrop = small_panel()
    last = min(u56.index[-1], b136.index[-1], small.index[-1])
    panels = {"U56": u56.loc[:last], "B136": b136.loc[:last], "SMALL439": small.loc[:last]}
    log(f"\n  panels truncated to common last date {last.date()}; SMALL dropped {ndrop} "
        f"max_1d_move >= 1.0 names -> {panels['SMALL439'].shape[1]-1} + SPY")

    # ---------------------------------------------------------- [0] gates
    log("\n[0] REPRODUCTION GATES")
    px = panels["U56"]
    w = ewall_weights(px, 0.75)
    r0, r10 = backtest(px, w, cost_bps=0, freq=FREQ), backtest(px, w, cost_bps=10, freq=FREQ)
    g1 = float((r0["returns"] - r0["turnover"] * 10 / 1e4 - r10["returns"]).abs().max())
    log(f"  G1 cost-rung identity max|d| = {g1:.3e}  {'PASS' if g1 < 1e-12 else 'FAIL'}")

    v1raw = {}
    for pn, ppx in panels.items():
        res = backtest(ppx, rules_v1_weights(ppx), cost_bps=0, freq=FREQ)
        st = ppx.index[260]
        v1raw[pn] = (res["returns"].loc[st:], res["turnover"].loc[st:])
    log("  G2 the queue's v1 halves claim (0.641/0.688 at 10 bps vs 0.285/0.346 at 25 bps):")
    hit = []
    for pn, (r, t) in v1raw.items():
        h10 = half_sharpes(r - t * 10 / 1e4)
        h25 = half_sharpes(r - t * 25 / 1e4)
        ok = abs(h10[0] - 0.641) < 0.01 and abs(h25[0] - 0.285) < 0.01
        hit.append(ok)
        log(f"    {pn:9s} 10 bps {h10[0]:.3f}/{h10[1]:.3f}   25 bps {h25[0]:.3f}/{h25[1]:.3f}"
            f"   {'<= the queue s panel' if ok else ''}")
    log(f"    -> the claim {'IS' if any(hit) else 'IS NOT'} reproduced on one of the three panels")

    m1 = metrics(v1raw["U56"][0] - v1raw["U56"][1] * 10 / 1e4)
    d3 = max(abs(m1["CAGR"] - 0.064194), abs(m1["Sharpe"] - 0.66110), abs(m1["MaxDD"] + 0.138278))
    log(f"  G3 U56/RULES v1 {m1['CAGR']:.4%} / {m1['Sharpe']:.5f} / {m1['MaxDD']:.4%}; max|d| vs "
        f"published {d3:.3e} {'PASS' if d3 < 1e-3 else 'DRIFT (vintage, idea 328/514)'}")

    selfp = pack(v1raw["U56"][0] - v1raw["U56"][1] * 10 / 1e4)
    g4self = pass_4a(selfp, selfp)
    log(f"  G4 4a predicate against ITSELF reads {g4self} (PROTOCOL's Sharpe leg is a strict >, "
        f"so a self-comparison must FAIL) while its MaxDD leg alone reads "
        f"{selfp[2] >= selfp[2]} (>=, so a tie PASSES) - {'PASS' if not g4self else 'FAIL'}")

    # ---------------------------------------------------------- [2] comparand bars
    log("\n[2] Q2 THE FOUR COMPARANDS AS BARS (halves and MaxDD an arm must clear)")
    bars, spy_packs, evals = {}, {}, {}
    for pn, ppx in panels.items():
        st = ppx.index[260]
        evals[pn] = st
        spy = ppx["SPY"].pct_change().fillna(0).loc[st:]
        ms = metrics(spy)
        s1, s2 = half_sharpes(spy)
        spy_packs[pn] = (s1, s2, metrics(spy.loc[OOS_START:])["Sharpe"], ms["MaxDD"], ms["CAGR"])
        v2 = backtest(ppx, rules_v2_weights(ppx), cost_bps=0, freq=FREQ)
        v2r, v2t = v2["returns"].loc[st:], v2["turnover"].loc[st:]
        v1r, v1t = v1raw[pn]
        for c in RUNGS:
            bars[(pn, "V2_MATCHED", c)] = pack(v2r - v2t * c / 1e4)
            bars[(pn, "V1_MATCHED", c)] = pack(v1r - v1t * c / 1e4)
            bars[(pn, "V2_FIX10", c)] = pack(v2r - v2t * 10 / 1e4)
            bars[(pn, "V1_FIX10", c)] = pack(v1r - v1t * 10 / 1e4)
    bt = pd.DataFrame([dict(panel=p, comparand=k, rung=c, H1=v[0], H2=v[1], MaxDD=v[2])
                       for (p, k, c), v in bars.items()])
    log(bt.pivot_table(index=["panel", "rung"], columns="comparand",
                       values=["H1", "H2", "MaxDD"]).to_string(float_format=lambda x: f"{x:.3f}"))
    log("\n  spread between the toughest and softest comparand, per panel x rung:")
    for pn in panels:
        for c in RUNGS:
            hs = [bars[(pn, k, c)][0] for k in COMPARANDS]
            h2s = [bars[(pn, k, c)][1] for k in COMPARANDS]
            dds = [bars[(pn, k, c)][2] for k in COMPARANDS]
            log(f"    {pn:9s} {c:2d} bps  H1 {min(hs):.3f}-{max(hs):.3f} (spread "
                f"{max(hs)-min(hs):.3f})  H2 {min(h2s):.3f}-{max(h2s):.3f} "
                f"({max(h2s)-min(h2s):.3f})  MaxDD {min(dds):.3f}-{max(dds):.3f} "
                f"({max(dds)-min(dds):.3f})")

    # ---------------------------------------------------------- [3] arms
    log("\n[3] Q3 RE-PRICING the pre-registered arm population under all four comparands")
    rows = []
    A = arms()
    for pn, ppx in panels.items():
        st = evals[pn]
        for fam, name, fn, freq in A:
            res = backtest(ppx, fn(ppx), cost_bps=0, freq=freq)
            r, t = res["returns"].loc[st:], res["turnover"].loc[st:]
            for c in RUNGS:
                rc = r - t * c / 1e4
                ap = pack(rc)
                m, mo = metrics(rc), metrics(rc.loc[OOS_START:])
                p4b, f4b = pass_4b(rc, spy_packs[pn])
                d = dict(panel=pn, family=fam, arm=name, rung=c, CAGR=m["CAGR"],
                         Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=ap[0], H2=ap[1],
                         IS_Sharpe=metrics(rc.loc[:IS_END])["Sharpe"], OOS_CAGR=mo["CAGR"],
                         OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"], p4b=p4b, fail4b=f4b,
                         turnover=float(t.sum() / ((len(t)) / 252)))
                for k in COMPARANDS:
                    b = bars[(pn, k, c)]
                    d[f"p4a_{k}"] = pass_4a(ap, b)
                    d[f"sh_{k}"] = bool(ap[0] > b[0] and ap[1] > b[1])
                    d[f"dd_{k}"] = bool(ap[2] >= b[2])
                rows.append(d)
    arm = pd.DataFrame(rows)
    arm.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    log(f"  {len(arm)} arm-rows (21 arms x 3 panels x 3 rungs), all reported in {STEM}.arms.csv")

    log("\n  4a pass counts by comparand x rung (denominator 63 arm-rows per rung):")
    tab = arm.groupby("rung")[[f"p4a_{k}" for k in COMPARANDS]].sum()
    tab["n"] = arm.groupby("rung").size()
    log(tab.to_string())
    log("\n  4a pass counts by comparand x panel (denominator 63 per panel):")
    log(arm.groupby("panel")[[f"p4a_{k}" for k in COMPARANDS]].sum().to_string())
    log(f"\n  4b (comparand-free) passes: {int(arm.p4b.sum())} of {len(arm)}; by rung: "
        + ", ".join(f"{c} bps {int(arm[arm.rung==c].p4b.sum())}" for c in RUNGS))

    log("\n[4] Q3 PAIRWISE DISAGREEMENT between comparands (the idea-135 statistic)")
    dis = []
    for i, a in enumerate(COMPARANDS):
        for b in COMPARANDS[i + 1:]:
            d = arm[f"p4a_{a}"] != arm[f"p4a_{b}"]
            dis.append(dict(A=a, B=b, disagree=int(d.sum()), n=len(arm),
                            share=float(d.mean()),
                            A_only=int((arm[f"p4a_{a}"] & ~arm[f"p4a_{b}"]).sum()),
                            B_only=int((arm[f"p4a_{b}"] & ~arm[f"p4a_{a}"]).sum())))
    dd = pd.DataFrame(dis)
    log(dd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    any_dis = (arm[[f"p4a_{k}" for k in COMPARANDS]].nunique(axis=1) > 1)
    log(f"  arm-rows whose 4a verdict is NOT invariant to the comparand: {int(any_dis.sum())} of "
        f"{len(arm)} ({any_dis.mean():.1%}); idea 135 reported 116 of 748 = 15.5%")
    log("  the non-invariant rows:")
    log(arm[any_dis][["panel", "family", "arm", "rung", "H1", "H2", "MaxDD"]
                     + [f"p4a_{k}" for k in COMPARANDS]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    log("\n[5] Q4 WHICH LEG MOVES when the comparand changes?")
    for a, b in [("V2_MATCHED", "V1_MATCHED"), ("V1_MATCHED", "V1_FIX10"),
                 ("V2_MATCHED", "V2_FIX10")]:
        d = arm[arm[f"p4a_{a}"] != arm[f"p4a_{b}"]]
        sh = int((d[f"sh_{a}"] != d[f"sh_{b}"]).sum())
        dl = int((d[f"dd_{a}"] != d[f"dd_{b}"]).sum())
        log(f"  {a} vs {b}: {len(d)} flips - Sharpe leg moves on {sh}, MaxDD leg on {dl}, "
            f"both on {int(((d[f'sh_{a}'] != d[f'sh_{b}']) & (d[f'dd_{a}'] != d[f'dd_{b}'])).sum())}")

    log("\n[6] TUNED GRID - comparand x rung, ALL 12 POINTS (pass count and pass share)")
    g = []
    for k in COMPARANDS:
        for c in RUNGS:
            s = arm[arm.rung == c]
            g.append(dict(comparand=k, rung=c, n=len(s), pass4a=int(s[f"p4a_{k}"].sum()),
                          share=float(s[f"p4a_{k}"].mean()),
                          sharpe_leg=int(s[f"sh_{k}"].sum()), dd_leg=int(s[f"dd_{k}"].sum())))
    gd = pd.DataFrame(g)
    gd.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    log(gd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    log("\n[7] Q5 PROTOCOL RULE 8 - the arm is chosen on the FIRST HALF by IS Sharpe within each")
    log("    family; the second half is read once.  Does the comparand change the PICK?")
    wf = []
    for (pn, fam, c), g2 in arm.groupby(["panel", "family", "rung"]):
        pick = g2.loc[g2["IS_Sharpe"].idxmax()]
        wf.append(dict(panel=pn, family=fam, rung=c, pick=pick["arm"],
                       OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                       OOS_MaxDD=pick["OOS_MaxDD"], p4b=pick["p4b"], fail4b=pick["fail4b"],
                       **{f"p4a_{k}": pick[f"p4a_{k}"] for k in COMPARANDS}))
    wfd = pd.DataFrame(wf)
    wfd.to_csv(OUT / f"{STEM}.wf.csv", index=False)
    log(f"  {len(wfd)} rule-8 cells (3 panels x 6 families x 3 rungs).  The chooser NEVER sees a")
    log("  comparand - it maximises the arm's own IS Sharpe - so the pick is identical across")
    log("  all four comparands BY CONSTRUCTION; what moves is the verdict attached to it:")
    log(wfd.groupby("rung")[[f"p4a_{k}" for k in COMPARANDS]].sum().to_string())
    nonv = (wfd[[f"p4a_{k}" for k in COMPARANDS]].nunique(axis=1) > 1)
    log(f"  rule-8 picks whose 4a verdict depends on the comparand: {int(nonv.sum())} of "
        f"{len(wfd)} ({nonv.mean():.1%}); picks passing 4b: {int(wfd.p4b.sum())}")
    log(wfd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    log("\n  OOS of the rule-8 picks at 10 bps vs the comparands and SPY:")
    for pn, ppx in panels.items():
        st = evals[pn]
        spy = ppx["SPY"].pct_change().fillna(0).loc[st:]
        v2 = backtest(ppx, rules_v2_weights(ppx), cost_bps=10, freq=FREQ)["returns"].loc[st:]
        v1r, v1t = v1raw[pn]
        mo_s, mo_v2 = metrics(spy.loc[OOS_START:]), metrics(v2.loc[OOS_START:])
        mo_v1 = metrics((v1r - v1t * 10 / 1e4).loc[OOS_START:])
        s = wfd[(wfd.panel == pn) & (wfd.rung == RUNG_HEAD)]
        log(f"    {pn:9s} picks median OOS {s.OOS_CAGR.median():.2%} / "
            f"{s.OOS_Sharpe.median():.3f} / {s.OOS_MaxDD.median():.2%}  ||  v2 "
            f"{mo_v2['CAGR']:.2%} / {mo_v2['Sharpe']:.3f} / {mo_v2['MaxDD']:.2%}  ||  v1 "
            f"{mo_v1['CAGR']:.2%} / {mo_v1['Sharpe']:.3f} / {mo_v1['MaxDD']:.2%}  ||  SPY "
            f"{mo_s['CAGR']:.2%} / {mo_s['Sharpe']:.3f} / {mo_s['MaxDD']:.2%}")

    log("\n[8] THE PROPOSED PROTOCOL LINE (for Sunday review; PROTOCOL.md is NOT edited here)")
    log('    Rule 3/4a: "The 4a comparand is the LIVE book (RULES v2 since 2026-09-06, via')
    log('    baseline.rules_v2_weights), priced at the SAME cost rung, cadence and panel as the')
    log('    arm.  A 4a claim must name the comparand book, its version date and its rung."')

    (OUT / f"{STEM}.txt").write_text("\n".join(LINES) + "\n")
    log(f"\nWrote {STEM}.txt / .census.csv / .arms.csv / .grid.csv / .wf.csv")


if __name__ == "__main__":
    main()
